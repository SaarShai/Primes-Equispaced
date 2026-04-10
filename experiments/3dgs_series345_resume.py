#!/usr/bin/env python3
"""
Series 3 (resume) + 4 + 5
==========================
Series 3: Budget sweep (3_30, 3_100, 3_unlimited) — skipping 3_20/3_50
Series 4: Scene complexity (4 scenes from easy to very hard)
Series 5: Gap threshold sweep (4 values)

All on MPS. 6000 steps, interval=200, best Farey params.
"""

import torch
import numpy as np
import time, json, os
from scipy.ndimage import gaussian_filter
from skimage.metrics import structural_similarity as ssim

DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Device: {DEVICE}", flush=True)

RESULTS_DIR = "/Users/saar/Desktop/Farey-Local/experiments/3dgs_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── SCENES ──────────────────────────────────────────────────────────

def make_scene_easy(size=256):
    """Single smooth gradient — easy to reconstruct"""
    y, x = np.mgrid[0:size, 0:size] / size
    img = 0.5 + 0.4 * np.sin(2 * np.pi * x) * np.cos(2 * np.pi * y)
    return torch.tensor(img, dtype=torch.float32, device=DEVICE)

def make_scene_medium(size=256):
    """Smooth background + one checkerboard patch (our standard scene)"""
    y, x = np.mgrid[0:size, 0:size] / size
    bg = 0.5 + 0.3 * np.sin(4 * np.pi * x) * np.cos(6 * np.pi * y)
    patch = 0.5 * (1 + np.sign(np.sin(20 * np.pi * x) * np.sin(20 * np.pi * y)))
    mask = ((x > 0.3) & (x < 0.7) & (y > 0.3) & (y < 0.7)).astype(float)
    img = bg * (1 - mask) + patch * mask
    return torch.tensor(img.astype(np.float32), device=DEVICE)

def make_scene_hard(size=256):
    """Multi-scale: 3 detail patches at different frequencies"""
    y, x = np.mgrid[0:size, 0:size] / size
    bg = 0.5 + 0.2 * np.sin(2 * np.pi * x)
    # Low freq patch
    p1 = 0.5 * (1 + np.sign(np.sin(10 * np.pi * x) * np.sin(10 * np.pi * y)))
    m1 = ((x > 0.05) & (x < 0.35) & (y > 0.05) & (y < 0.35)).astype(float)
    # Med freq patch
    p2 = 0.5 * (1 + np.sign(np.sin(20 * np.pi * x) * np.sin(20 * np.pi * y)))
    m2 = ((x > 0.4) & (x < 0.7) & (y > 0.3) & (y < 0.6)).astype(float)
    # High freq patch
    p3 = 0.5 * (1 + np.sign(np.sin(40 * np.pi * x) * np.sin(40 * np.pi * y)))
    m3 = ((x > 0.6) & (x < 0.95) & (y > 0.6) & (y < 0.95)).astype(float)
    combined_mask = np.clip(m1 + m2 + m3, 0, 1)
    patches = p1 * m1 + p2 * m2 + p3 * m3
    img = bg * (1 - combined_mask) + patches * combined_mask
    return torch.tensor(img.astype(np.float32), device=DEVICE)

def make_scene_extreme(size=256):
    """Dense high-frequency everywhere — hardest possible"""
    y, x = np.mgrid[0:size, 0:size] / size
    img = (0.3 * np.sin(30 * np.pi * x) * np.cos(30 * np.pi * y) +
           0.2 * np.sin(50 * np.pi * x) * np.sin(50 * np.pi * y) +
           0.15 * np.cos(70 * np.pi * (x + y)) +
           0.35)
    return torch.tensor(img.astype(np.float32), device=DEVICE)

# ── GAUSSIAN MODEL ──────────────────────────────────────────────────

class GaussianModel2D:
    def __init__(self, n_init, target_size, device):
        pts = np.random.rand(n_init, 2)
        self.device = device
        self.pos_x = torch.tensor(pts[:, 0], dtype=torch.float32, device=device, requires_grad=True)
        self.pos_y = torch.tensor(pts[:, 1], dtype=torch.float32, device=device, requires_grad=True)
        self.log_sx = torch.full((len(pts),), np.log(0.05), dtype=torch.float32, device=device, requires_grad=True)
        self.log_sy = torch.full((len(pts),), np.log(0.05), dtype=torch.float32, device=device, requires_grad=True)
        self.logit_a = torch.full((len(pts),), 2.0, dtype=torch.float32, device=device, requires_grad=True)
        self.color = torch.full((len(pts),), 0.5, dtype=torch.float32, device=device, requires_grad=True)
        self.size = target_size

    def params(self):
        return [self.pos_x, self.pos_y, self.log_sx, self.log_sy, self.logit_a, self.color]

    def render(self):
        y_coords = torch.linspace(0, 1, self.size, device=self.device)
        x_coords = torch.linspace(0, 1, self.size, device=self.device)
        gy, gx = torch.meshgrid(y_coords, x_coords, indexing='ij')

        px = self.pos_x.unsqueeze(-1).unsqueeze(-1)
        py = self.pos_y.unsqueeze(-1).unsqueeze(-1)
        sx = torch.exp(self.log_sx).unsqueeze(-1).unsqueeze(-1)
        sy = torch.exp(self.log_sy).unsqueeze(-1).unsqueeze(-1)
        alpha = torch.sigmoid(self.logit_a).unsqueeze(-1).unsqueeze(-1)
        col = self.color.unsqueeze(-1).unsqueeze(-1)

        dx = (gx.unsqueeze(0) - px) / sx
        dy = (gy.unsqueeze(0) - py) / sy
        gauss = torch.exp(-0.5 * (dx**2 + dy**2))
        weighted = alpha * col * gauss
        canvas = weighted.sum(dim=0)
        norm = (alpha * gauss).sum(dim=0) + 1e-6
        return canvas / norm

    def n(self):
        return len(self.pos_x)

    def add_gaussians(self, new_x, new_y, new_sx, new_sy, new_a, new_c):
        with torch.no_grad():
            self.pos_x = torch.cat([self.pos_x.detach(), new_x]).requires_grad_(True)
            self.pos_y = torch.cat([self.pos_y.detach(), new_y]).requires_grad_(True)
            self.log_sx = torch.cat([self.log_sx.detach(), new_sx]).requires_grad_(True)
            self.log_sy = torch.cat([self.log_sy.detach(), new_sy]).requires_grad_(True)
            self.logit_a = torch.cat([self.logit_a.detach(), new_a]).requires_grad_(True)
            self.color = torch.cat([self.color.detach(), new_c]).requires_grad_(True)

    def prune(self, keep_mask):
        with torch.no_grad():
            self.pos_x = self.pos_x.detach()[keep_mask].requires_grad_(True)
            self.pos_y = self.pos_y.detach()[keep_mask].requires_grad_(True)
            self.log_sx = self.log_sx.detach()[keep_mask].requires_grad_(True)
            self.log_sy = self.log_sy.detach()[keep_mask].requires_grad_(True)
            self.logit_a = self.logit_a.detach()[keep_mask].requires_grad_(True)
            self.color = self.color.detach()[keep_mask].requires_grad_(True)


# ── DENSIFICATION ───────────────────────────────────────────────────

def densify_errgate(model, target, max_gauss, max_new, **kwargs):
    """Error-gated ADC (fair baseline)"""
    if model.n() >= max_gauss:
        return
    rendered = model.render().detach()
    err_map = (rendered - target) ** 2
    with torch.no_grad():
        px = model.pos_x.detach().cpu().numpy()
        py = model.pos_y.detach().cpu().numpy()
        sx = torch.exp(model.log_sx).detach().cpu().numpy()
        sy = torch.exp(model.log_sy).detach().cpu().numpy()
        alpha_val = torch.sigmoid(model.logit_a).detach().cpu().numpy()
        col = model.color.detach().cpu().numpy()
        err_np = err_map.cpu().numpy()
        S = target.shape[0]

        local_err = np.zeros(len(px))
        for i in range(len(px)):
            ix, iy = int(px[i] * S), int(py[i] * S)
            ix, iy = max(0, min(S-1, ix)), max(0, min(S-1, iy))
            r = max(3, int(max(sx[i], sy[i]) * S))
            x0, x1 = max(0, ix - r), min(S, ix + r)
            y0, y1 = max(0, iy - r), min(S, iy + r)
            if x1 > x0 and y1 > y0:
                local_err[i] = err_np[y0:y1, x0:x1].mean()

        threshold = np.percentile(local_err[local_err > 0], 70) if np.any(local_err > 0) else 0.01
        candidates = np.where(local_err > threshold)[0]
        if len(candidates) == 0:
            return
        candidates = candidates[np.argsort(-local_err[candidates])][:max_new]

        new_x, new_y, new_sx, new_sy, new_a, new_c = [], [], [], [], [], []
        for idx in candidates:
            if model.n() + len(new_x) >= max_gauss:
                break
            offset_x = np.random.randn() * sx[idx] * 0.5
            offset_y = np.random.randn() * sy[idx] * 0.5
            nx = np.clip(px[idx] + offset_x, 0.01, 0.99)
            ny = np.clip(py[idx] + offset_y, 0.01, 0.99)
            new_x.append(nx)
            new_y.append(ny)
            new_sx.append(np.log(sx[idx] * 0.7))
            new_sy.append(np.log(sy[idx] * 0.7))
            new_a.append(1.0)
            new_c.append(col[idx])

        if new_x:
            model.add_gaussians(
                torch.tensor(new_x, dtype=torch.float32, device=model.device),
                torch.tensor(new_y, dtype=torch.float32, device=model.device),
                torch.tensor(new_sx, dtype=torch.float32, device=model.device),
                torch.tensor(new_sy, dtype=torch.float32, device=model.device),
                torch.tensor(new_a, dtype=torch.float32, device=model.device),
                torch.tensor(new_c, dtype=torch.float32, device=model.device),
            )


def densify_farey(model, target, max_gauss, max_new, farey_level=45, gap_ratio=2.0, **kwargs):
    """Farey-guided densification"""
    if model.n() >= max_gauss:
        return
    rendered = model.render().detach()
    err_map = (rendered - target) ** 2
    with torch.no_grad():
        px = model.pos_x.detach().cpu().numpy()
        py = model.pos_y.detach().cpu().numpy()
        sx = torch.exp(model.log_sx).detach().cpu().numpy()
        sy = torch.exp(model.log_sy).detach().cpu().numpy()
        alpha_val = torch.sigmoid(model.logit_a).detach().cpu().numpy()
        col = model.color.detach().cpu().numpy()
        err_np = err_map.cpu().numpy()
        S = target.shape[0]

        order_x = np.argsort(px)
        order_y = np.argsort(py)

        candidates = []
        for order, pos_arr, sig_arr in [(order_x, px, sx), (order_y, py, sy)]:
            for k in range(len(order) - 1):
                i, j = order[k], order[k + 1]
                gap = pos_arr[j] - pos_arr[i]
                combined_sig = sig_arr[i] + sig_arr[j]
                if combined_sig < 1e-8:
                    continue
                d_gap = gap / combined_sig
                if d_gap <= gap_ratio:
                    continue
                mid_x = (px[i] * sig_arr[j] + px[j] * sig_arr[i]) / (sig_arr[i] + sig_arr[j])
                mid_y = (py[i] * sig_arr[j] + py[j] * sig_arr[i]) / (sig_arr[i] + sig_arr[j])
                ix_m, iy_m = int(mid_x * S), int(mid_y * S)
                ix_m, iy_m = max(0, min(S-1, ix_m)), max(0, min(S-1, iy_m))
                r = max(3, int(gap * S * 0.3))
                x0, x1 = max(0, ix_m - r), min(S, ix_m + r)
                y0, y1 = max(0, iy_m - r), min(S, iy_m + r)
                local_e = err_np[y0:y1, x0:x1].mean() if (x1 > x0 and y1 > y0) else 0
                candidates.append((local_e, mid_x, mid_y, i, j, gap))

        candidates.sort(key=lambda c: -c[0])
        used_positions = set()
        new_x, new_y, new_sx, new_sy, new_a, new_c = [], [], [], [], [], []
        for err_val, mx, my, i, j, gap in candidates:
            if model.n() + len(new_x) >= max_gauss or len(new_x) >= max_new:
                break
            grid_key = (int(mx * 50), int(my * 50))
            if grid_key in used_positions:
                continue
            used_positions.add(grid_key)
            if err_val < 0.001:
                continue
            new_x.append(np.clip(mx, 0.01, 0.99))
            new_y.append(np.clip(my, 0.01, 0.99))
            new_scale = gap * 0.4
            new_sx.append(np.log(max(new_scale, 0.005)))
            new_sy.append(np.log(max(new_scale, 0.005)))
            new_a.append(1.0)
            avg_col = (col[i] + col[j]) / 2
            new_c.append(avg_col)

        if new_x:
            model.add_gaussians(
                torch.tensor(new_x, dtype=torch.float32, device=model.device),
                torch.tensor(new_y, dtype=torch.float32, device=model.device),
                torch.tensor(new_sx, dtype=torch.float32, device=model.device),
                torch.tensor(new_sy, dtype=torch.float32, device=model.device),
                torch.tensor(new_a, dtype=torch.float32, device=model.device),
                torch.tensor(new_c, dtype=torch.float32, device=model.device),
            )


# ── TRAINING LOOP ───────────────────────────────────────────────────

def train_run(target, method, steps, densify_interval, max_gauss, max_new, n_init,
              farey_start=45, farey_inc=5, gap_ratio=2.0):
    torch.manual_seed(42)
    np.random.seed(42)
    S = target.shape[0]
    model = GaussianModel2D(n_init, S, DEVICE)
    optimizer = torch.optim.Adam(model.params(), lr=0.01)
    farey_level = farey_start
    t0 = time.time()

    for step in range(steps):
        rendered = model.render()
        loss = ((rendered - target) ** 2).mean()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step > 0 and step % densify_interval == 0:
            if method == 'farey':
                densify_farey(model, target, max_gauss, max_new,
                              farey_level=farey_level, gap_ratio=gap_ratio)
                farey_level += farey_inc
            else:
                densify_errgate(model, target, max_gauss, max_new)
            # Prune low-opacity
            with torch.no_grad():
                alpha = torch.sigmoid(model.logit_a)
                keep = alpha > 0.01
                if keep.sum() < model.n():
                    model.prune(keep)
            optimizer = torch.optim.Adam(model.params(), lr=0.01)

        if step % 500 == 0:
            elapsed = time.time() - t0
            with torch.no_grad():
                psnr = -10 * torch.log10(loss).item()
            print(f"    Step {step:5d}: PSNR={psnr:.2f} dB  G={model.n()}  t={elapsed:.0f}s", flush=True)

    with torch.no_grad():
        final_render = model.render()
        final_mse = ((final_render - target) ** 2).mean().item()
        final_psnr = -10 * np.log10(final_mse + 1e-10)
        render_np = final_render.cpu().numpy()
        target_np = target.cpu().numpy()
        final_ssim = ssim(target_np, render_np, data_range=1.0)

    return {
        'psnr': round(final_psnr, 2),
        'ssim': round(final_ssim, 4),
        'n_gauss': model.n(),
        'time': round(time.time() - t0, 1),
    }


def run_config(name, target, steps, densify_interval, max_gauss, max_new, n_init=500,
               farey_start=45, farey_inc=5, gap_ratio=2.0, series_results=None):
    print(f"\n{'='*50}", flush=True)
    print(f"  {name} ({steps} steps, int={densify_interval}, max_g={max_gauss}, max_new={max_new})", flush=True)
    print(f"{'='*50}", flush=True)

    print(f"\n  --- B_errgate_{name} ---", flush=True)
    res_b = train_run(target, 'errgate', steps, densify_interval, max_gauss, max_new, n_init,
                      farey_start=farey_start, farey_inc=farey_inc, gap_ratio=gap_ratio)
    print(f"    RESULT: PSNR={res_b['psnr']:.2f} dB  SSIM={res_b['ssim']:.4f}  G={res_b['n_gauss']}  time={res_b['time']:.0f}s", flush=True)

    print(f"\n  --- C_farey_{name} ---", flush=True)
    res_c = train_run(target, 'farey', steps, densify_interval, max_gauss, max_new, n_init,
                      farey_start=farey_start, farey_inc=farey_inc, gap_ratio=gap_ratio)
    print(f"    RESULT: PSNR={res_c['psnr']:.2f} dB  SSIM={res_c['ssim']:.4f}  G={res_c['n_gauss']}  time={res_c['time']:.0f}s", flush=True)

    delta = res_c['psnr'] - res_b['psnr']
    print(f"  >>> {name}: B={res_b['psnr']:.2f}  C={res_c['psnr']:.2f}  Delta={delta:+.2f} dB <<<", flush=True)

    result = {'name': name, 'adc': res_b, 'farey': res_c, 'delta_db': round(delta, 2)}
    if series_results is not None:
        series_results.append(result)
    return result


def save_results(filename, results):
    with open(os.path.join(RESULTS_DIR, filename), 'w') as f:
        json.dump(results, f, indent=2)


def print_summary(title, results):
    print(f"\n{'='*60}", flush=True)
    print(f"  {title}", flush=True)
    print(f"{'='*60}", flush=True)
    print(f"{'Config':<25} {'B PSNR':>10} {'C PSNR':>10} {'Delta':>8} {'B G':>6} {'C G':>6}", flush=True)
    print("-"*70, flush=True)
    for r in results:
        print(f"{r['name']:<25} {r['adc']['psnr']:>10.2f} {r['farey']['psnr']:>10.2f} {r['delta_db']:>+8.2f} {r['adc']['n_gauss']:>6} {r['farey']['n_gauss']:>6}", flush=True)
    avg = np.mean([r['delta_db'] for r in results])
    print(f"\nAverage Delta: {avg:+.2f} dB", flush=True)


# ══════════════════════════════════════════════════════════════════════
# SERIES 3 RESUME: Budget (3_30, 3_100, unlimited)
# ══════════════════════════════════════════════════════════════════════

print("\n" + "="*60, flush=True)
print("  SERIES 3 RESUME: Budget (6000 steps, int=200)", flush=True)
print("="*60, flush=True)

target_medium = make_scene_medium(256)
s3_results = []

for max_new in [30, 100, 9999]:
    label = "unlimited" if max_new == 9999 else str(max_new)
    run_config(f"3_{label}", target_medium, 6000, 200, 2000, max_new, n_init=500,
               series_results=s3_results)
    save_results('series3_resume.json', s3_results)

print_summary("SERIES 3 RESUME RESULTS", s3_results)


# ══════════════════════════════════════════════════════════════════════
# SERIES 4: Scene Complexity
# Question: Does Farey benefit more on harder scenes?
# ══════════════════════════════════════════════════════════════════════

print("\n\n" + "="*60, flush=True)
print("  SERIES 4: Scene Complexity (6000 steps, int=200, max_new=30)", flush=True)
print("="*60, flush=True)

s4_results = []
scenes = [
    ("4a_easy", make_scene_easy(256)),
    ("4b_medium", make_scene_medium(256)),
    ("4c_hard_multiscale", make_scene_hard(256)),
    ("4d_extreme_dense", make_scene_extreme(256)),
]

for name, scene_target in scenes:
    run_config(name, scene_target, 6000, 200, 2000, 30, n_init=500,
               series_results=s4_results)
    save_results('series4_complexity.json', s4_results)

print_summary("SERIES 4: SCENE COMPLEXITY", s4_results)


# ══════════════════════════════════════════════════════════════════════
# SERIES 5: Gap Threshold
# Question: What's the optimal gap_ratio for Farey insertion?
# ══════════════════════════════════════════════════════════════════════

print("\n\n" + "="*60, flush=True)
print("  SERIES 5: Gap Threshold (6000 steps, int=200, max_new=30, hard scene)", flush=True)
print("="*60, flush=True)

target_hard = make_scene_hard(256)
s5_results = []

for gap_ratio in [1.0, 2.0, 4.0, 8.0]:
    run_config(f"5_gap{gap_ratio:.1f}", target_hard, 6000, 200, 2000, 30, n_init=500,
               gap_ratio=gap_ratio, series_results=s5_results)
    save_results('series5_threshold.json', s5_results)

print_summary("SERIES 5: GAP THRESHOLD", s5_results)


# ══════════════════════════════════════════════════════════════════════
# GRAND SUMMARY
# ══════════════════════════════════════════════════════════════════════

print("\n\n" + "="*60, flush=True)
print("  ALL SERIES COMPLETE", flush=True)
print("="*60, flush=True)
all_deltas = [r['delta_db'] for r in s3_results + s4_results + s5_results]
print(f"Total configs: {len(all_deltas)}", flush=True)
print(f"Average delta: {np.mean(all_deltas):+.2f} dB", flush=True)
print(f"Max delta: {max(all_deltas):+.2f} dB", flush=True)
print(f"Min delta: {min(all_deltas):+.2f} dB", flush=True)
print(f"Configs where Farey wins: {sum(1 for d in all_deltas if d > 0)}/{len(all_deltas)}", flush=True)
