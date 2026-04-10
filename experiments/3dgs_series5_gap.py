#!/usr/bin/env python3
"""
Series 5: Gap Threshold
========================
Question: What gap_ratio threshold maximizes Farey's advantage?
Variable: gap_ratio (1.0, 2.0, 4.0, 8.0)
Fixed: Best params from Series 1-4

Uses the hardest scene (make_scene_hard) since that's where Farey should shine most.
Reads best max_new from Series 3 results.
"""

import torch
import numpy as np
import time, json, os
from skimage.metrics import structural_similarity as ssim_metric

DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Device: {DEVICE}", flush=True)

RESULTS_DIR = "/Users/saar/Desktop/Farey-Local/experiments/3dgs_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Read best max_new from Series 3
best_max_new = 30
s3_path = os.path.join(RESULTS_DIR, 'series3_budget.json')
if os.path.exists(s3_path):
    with open(s3_path) as f:
        s3 = json.load(f)
    if s3:
        best = max(s3, key=lambda r: r['delta_db'])
        label = best['name'].split('_')[1]
        best_max_new = 9999 if label == 'unlimited' else int(label)
        print(f"Series 3 best: {best['name']} delta={best['delta_db']:+.2f} dB → max_new={best_max_new}", flush=True)

ALL_RESULTS = []

# ── Scene: Use the hardest scene ─────────────────────────────────────

def make_scene_hard(size=256):
    """Dense high-frequency content EVERYWHERE."""
    y, x = np.meshgrid(np.linspace(0, 1, size), np.linspace(0, 1, size))
    t = (0.2 * np.sin(6*np.pi*x) * np.cos(8*np.pi*y)
         + 0.15 * np.sin(14*np.pi*x) * np.sin(10*np.pi*y)
         + 0.15 * np.cos(20*np.pi*x) * np.sin(18*np.pi*y)
         + 0.1 * ((((x*30).astype(int) + (y*30).astype(int)) % 2) * 2 - 1)
         + 0.1 * np.sin(40*np.pi*x*y))
    target = (t - t.min()) / (t.max() - t.min())
    return torch.tensor(target, dtype=torch.float32, device=DEVICE)


# ── Gaussian Field + Training (same engine) ──────────────────────────

class GaussianField2D:
    def __init__(self, n_init, target_size, device):
        self.device = device; self.size = target_size
        k = int(np.sqrt(n_init))
        gx = np.linspace(0.1, 0.9, k)
        gy = np.linspace(0.1, 0.9, k)
        xx, yy = np.meshgrid(gx, gy)
        pts = np.stack([xx.ravel(), yy.ravel()], axis=1)[:n_init]
        self.pos_x = torch.tensor(pts[:, 0], dtype=torch.float32, device=device, requires_grad=True)
        self.pos_y = torch.tensor(pts[:, 1], dtype=torch.float32, device=device, requires_grad=True)
        self.log_sx = torch.full((len(pts),), np.log(0.05), dtype=torch.float32, device=device, requires_grad=True)
        self.log_sy = torch.full((len(pts),), np.log(0.05), dtype=torch.float32, device=device, requires_grad=True)
        self.amplitude = torch.full((len(pts),), 0.5, dtype=torch.float32, device=device, requires_grad=True)
        self.opacity = torch.full((len(pts),), 0.8, dtype=torch.float32, device=device, requires_grad=True)
    def params(self):
        return [self.pos_x, self.pos_y, self.log_sx, self.log_sy, self.amplitude, self.opacity]
    @property
    def n(self): return len(self.pos_x)
    def render(self):
        coords_y, coords_x = torch.meshgrid(
            torch.linspace(0, 1, self.size, device=self.device),
            torch.linspace(0, 1, self.size, device=self.device), indexing='ij')
        img = torch.zeros(self.size, self.size, device=self.device)
        sx = torch.exp(self.log_sx).clamp(min=0.005)
        sy = torch.exp(self.log_sy).clamp(min=0.005)
        opa = torch.sigmoid(self.opacity)
        for i in range(self.n):
            dx = coords_x - self.pos_x[i]; dy = coords_y - self.pos_y[i]
            gauss = torch.exp(-0.5 * (dx**2/sx[i]**2 + dy**2/sy[i]**2))
            img = img + opa[i] * self.amplitude[i] * gauss
        return img.clamp(0, 1)
    def add_gaussians(self, new_px, new_py, new_sx, new_sy, new_amp):
        n = len(new_px)
        if n == 0: return
        self.pos_x = torch.cat([self.pos_x.detach(), new_px]).requires_grad_(True)
        self.pos_y = torch.cat([self.pos_y.detach(), new_py]).requires_grad_(True)
        self.log_sx = torch.cat([self.log_sx.detach(), torch.log(new_sx)]).requires_grad_(True)
        self.log_sy = torch.cat([self.log_sy.detach(), torch.log(new_sy)]).requires_grad_(True)
        self.amplitude = torch.cat([self.amplitude.detach(), new_amp]).requires_grad_(True)
        self.opacity = torch.cat([self.opacity.detach(), torch.full((n,), 0.5, device=self.device)]).requires_grad_(True)
    def prune(self, min_opacity=0.01):
        opa = torch.sigmoid(self.opacity).detach(); keep = opa > min_opacity
        if keep.all(): return
        self.pos_x = self.pos_x.detach()[keep].requires_grad_(True)
        self.pos_y = self.pos_y.detach()[keep].requires_grad_(True)
        self.log_sx = self.log_sx.detach()[keep].requires_grad_(True)
        self.log_sy = self.log_sy.detach()[keep].requires_grad_(True)
        self.amplitude = self.amplitude.detach()[keep].requires_grad_(True)
        self.opacity = self.opacity.detach()[keep].requires_grad_(True)


def densify_error_gated(field, target, max_new, max_gauss):
    if field.n >= max_gauss: return
    with torch.no_grad():
        rendered = field.render(); error_map = (target - rendered)**2
        error_flat = error_map.reshape(-1)
        topk = min(max_new*5, error_flat.numel())
        _, top_idx = torch.topk(error_flat, topk)
        top_y = top_idx // field.size; top_x = top_idx % field.size
        cand_x = top_x.float()/field.size; cand_y = top_y.float()/field.size
        new_x, new_y, new_sx, new_sy, new_amp = [], [], [], [], []
        for i in range(len(cand_x)):
            if len(new_x) >= max_new or field.n+len(new_x) >= max_gauss: break
            cx, cy = cand_x[i], cand_y[i]
            dists = ((field.pos_x.detach()-cx)**2 + (field.pos_y.detach()-cy)**2).sqrt()
            if dists.min().item() > 0.02:
                new_x.append(cx); new_y.append(cy)
                new_sx.append(torch.tensor(dists.min().item()*0.5, device=field.device))
                new_sy.append(torch.tensor(dists.min().item()*0.5, device=field.device))
                new_amp.append(torch.tensor(target[top_y[i], top_x[i]].item(), device=field.device))
        if new_x:
            field.add_gaussians(torch.stack(new_x), torch.stack(new_y),
                                torch.stack(new_sx), torch.stack(new_sy), torch.stack(new_amp))


def densify_farey(field, target, max_new, max_gauss, farey_level, gap_ratio_threshold=2.0):
    """Farey densification with configurable gap_ratio threshold."""
    if field.n >= max_gauss: return
    with torch.no_grad():
        rendered = field.render(); error_map = (target - rendered)**2
        pos_x = field.pos_x.detach(); pos_y = field.pos_y.detach()
        sx = torch.exp(field.log_sx.detach()).clamp(min=0.005)
        sy = torch.exp(field.log_sy.detach()).clamp(min=0.005)
        candidates = []
        for axis in ['x', 'y']:
            if axis == 'x':
                si = torch.argsort(pos_x)
                s_a, s_b, s_sa, s_sb = pos_x[si], pos_y[si], sx[si], sy[si]
            else:
                si = torch.argsort(pos_y)
                s_a, s_b, s_sa, s_sb = pos_y[si], pos_x[si], sy[si], sx[si]
            for i in range(len(s_a)-1):
                gap = (s_a[i+1]-s_a[i]).item()
                avg_s = (s_sa[i].item()+s_sa[i+1].item())/2
                if avg_s < 1e-6: continue
                d_gap = gap / avg_s
                # Use gap_ratio_threshold instead of farey_level for admission
                if d_gap >= gap_ratio_threshold and d_gap <= farey_level:
                    w1 = 1.0/(s_sa[i].item()+1e-8); w2 = 1.0/(s_sa[i+1].item()+1e-8)
                    med_a = (w1*s_a[i].item()+w2*s_a[i+1].item())/(w1+w2)
                    med_b = (w1*s_b[i].item()+w2*s_b[i+1].item())/(w1+w2)
                    if axis == 'x': mx, my = med_a, med_b
                    else: mx, my = med_b, med_a
                    px = max(0, min(field.size-1, int(mx*field.size)))
                    py = max(0, min(field.size-1, int(my*field.size)))
                    err = error_map[py, px].item()
                    candidates.append((err, mx, my, gap*0.3, gap*0.3, target[py, px].item()))
        candidates.sort(key=lambda c: -c[0])
        new_x, new_y, new_sx, new_sy, new_amp = [], [], [], [], []
        used = set()
        for err, mx, my, nsx, nsy, amp in candidates:
            if len(new_x) >= max_new or field.n+len(new_x) >= max_gauss: break
            key = (round(mx,3), round(my,3))
            if key in used: continue
            used.add(key)
            if err > 0.001:
                new_x.append(torch.tensor(mx, device=field.device))
                new_y.append(torch.tensor(my, device=field.device))
                new_sx.append(torch.tensor(max(nsx,0.005), device=field.device))
                new_sy.append(torch.tensor(max(nsy,0.005), device=field.device))
                new_amp.append(torch.tensor(amp, device=field.device))
        if new_x:
            field.add_gaussians(torch.stack(new_x), torch.stack(new_y),
                                torch.stack(new_sx), torch.stack(new_sy), torch.stack(new_amp))


def train_run(target, method, steps, densify_interval, max_gauss, max_new, n_init=500,
              farey_start=45, farey_increment=5, gap_ratio=2.0):
    size = target.shape[0]
    field = GaussianField2D(n_init, size, DEVICE)
    optimizer = torch.optim.Adam(field.params(), lr=0.005)
    farey_level = farey_start; t0 = time.time()
    for step in range(steps):
        optimizer.zero_grad()
        rendered = field.render()
        loss = ((target - rendered)**2).mean()
        loss.backward(); optimizer.step()
        if step > 0 and step % densify_interval == 0:
            if method == 'adc':
                densify_error_gated(field, target, max_new, max_gauss)
            else:
                densify_farey(field, target, max_new, max_gauss, farey_level, gap_ratio)
                farey_level += farey_increment
            field.prune(min_opacity=0.01)
            optimizer = torch.optim.Adam(field.params(), lr=0.005*(0.95**(step//500)))
        if step % 500 == 0:
            elapsed = time.time()-t0
            psnr = -10*np.log10(loss.item()+1e-10)
            print(f"    Step {step:5d}: PSNR={psnr:.2f} dB  G={field.n}  t={elapsed:.0f}s", flush=True)
    with torch.no_grad():
        rendered = field.render()
        mse = ((target-rendered)**2).mean().item()
        psnr = -10*np.log10(mse+1e-10)
        ssim_val = ssim_metric(target.cpu().numpy(), rendered.cpu().numpy(), data_range=1.0)
    return {'psnr': psnr, 'ssim': ssim_val, 'mse': mse, 'n_gauss': field.n, 'time': time.time()-t0}


def run_config(name, target, gap_ratio, max_new):
    print(f"\n{'='*50}", flush=True)
    print(f"  {name} (gap_ratio={gap_ratio}, max_new={max_new})", flush=True)
    print(f"{'='*50}", flush=True)

    print(f"\n  --- B_errgate_{name} ---", flush=True)
    res_b = train_run(target, 'adc', 6000, 200, 2000, max_new, 500)
    print(f"    RESULT: PSNR={res_b['psnr']:.2f} dB  SSIM={res_b['ssim']:.4f}  G={res_b['n_gauss']}  time={res_b['time']:.0f}s", flush=True)

    print(f"\n  --- C_farey_{name} ---", flush=True)
    res_c = train_run(target, 'farey', 6000, 200, 2000, max_new, 500, gap_ratio=gap_ratio)
    print(f"    RESULT: PSNR={res_c['psnr']:.2f} dB  SSIM={res_c['ssim']:.4f}  G={res_c['n_gauss']}  time={res_c['time']:.0f}s", flush=True)

    delta = res_c['psnr'] - res_b['psnr']
    print(f"  >>> {name}: B={res_b['psnr']:.2f}  C={res_c['psnr']:.2f}  Delta={delta:+.2f} dB <<<", flush=True)

    result = {'name': name, 'gap_ratio': gap_ratio, 'adc': res_b, 'farey': res_c, 'delta_db': delta}
    ALL_RESULTS.append(result)
    with open(os.path.join(RESULTS_DIR, 'series5_gap.json'), 'w') as f:
        json.dump(ALL_RESULTS, f, indent=2)
    return result


# ══════════════════════════════════════════════════════════════════════
# SERIES 5: Gap Threshold on hardest scene
# ══════════════════════════════════════════════════════════════════════

print(f"\n{'='*60}", flush=True)
print(f"  SERIES 5: Gap Threshold (6000 steps, hard scene, max_new={best_max_new})", flush=True)
print(f"{'='*60}", flush=True)

target = make_scene_hard(256)

for gap_ratio in [1.0, 2.0, 4.0, 8.0]:
    run_config(f"5_gap{gap_ratio}", target, gap_ratio, best_max_new)

# Summary
print(f"\n{'='*60}", flush=True)
print("  SERIES 5 SUMMARY", flush=True)
print(f"{'='*60}", flush=True)
print(f"{'Config':<25} {'Gap Ratio':>10} {'B PSNR':>10} {'C PSNR':>10} {'Delta':>8}", flush=True)
print("-"*65, flush=True)
for r in ALL_RESULTS:
    print(f"{r['name']:<25} {r['gap_ratio']:>10.1f} {r['adc']['psnr']:>10.2f} {r['farey']['psnr']:>10.2f} {r['delta_db']:>+8.2f}", flush=True)
avg = np.mean([r['delta_db'] for r in ALL_RESULTS])
print(f"\nAverage Delta: {avg:+.2f} dB", flush=True)
