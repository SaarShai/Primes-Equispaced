#!/usr/bin/env python3
"""
Series 3: Densification Budget
===============================
Question: Does Farey benefit more with tight or generous insertion budgets?
Variable: max_new_per_step (10, 20, 30, 50, 100, unlimited)
Fixed: Best params from Series 1+2:
  - 6000 steps, densify interval=200, 256x256, 500 init Gaussians
  - Farey start=45, increment=5 (best from Series 1)

Uses MPS (Apple Silicon GPU).
Saves results incrementally after each config.
"""

import torch
import numpy as np
import time, json, os, sys
from scipy.ndimage import gaussian_filter
from skimage.metrics import structural_similarity as ssim

DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Device: {DEVICE}", flush=True)

RESULTS_DIR = "/Users/saar/Desktop/Farey-Local/experiments/3dgs_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

ALL_RESULTS = []

# ── SCENE: Use the Series 2 scene (256x256, complex) ────────────────

def make_target(size=256):
    """Complex scene: smooth gradient + multiple detail regions at different scales."""
    y, x = np.meshgrid(np.linspace(0, 1, size), np.linspace(0, 1, size))

    # Smooth background
    bg = 0.3 * np.sin(2 * np.pi * x) * np.cos(2 * np.pi * y)

    # High-frequency checkerboard patch (center)
    checker = np.zeros_like(x)
    mask = (x > 0.3) & (x < 0.7) & (y > 0.3) & (y < 0.7)
    checker[mask] = 0.5 * ((((x[mask]*20).astype(int) + (y[mask]*20).astype(int)) % 2) * 2 - 1)

    # Fine detail patch (top-right)
    fine = np.zeros_like(x)
    mask2 = (x > 0.7) & (y > 0.7)
    fine[mask2] = 0.3 * np.sin(40 * np.pi * x[mask2]) * np.sin(40 * np.pi * y[mask2])

    # Medium detail (bottom-left)
    med = np.zeros_like(x)
    mask3 = (x < 0.3) & (y < 0.3)
    med[mask3] = 0.4 * np.sin(10 * np.pi * x[mask3]) * np.cos(15 * np.pi * y[mask3])

    target = bg + checker + fine + med
    target = (target - target.min()) / (target.max() - target.min())
    return torch.tensor(target, dtype=torch.float32, device=DEVICE)


# ── Gaussian Splatting Engine ────────────────────────────────────────

class GaussianField2D:
    def __init__(self, n_init, target_size, device):
        self.device = device
        self.size = target_size

        # Initialize on grid
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
    def n(self):
        return len(self.pos_x)

    def render(self):
        coords_y, coords_x = torch.meshgrid(
            torch.linspace(0, 1, self.size, device=self.device),
            torch.linspace(0, 1, self.size, device=self.device),
            indexing='ij'
        )

        img = torch.zeros(self.size, self.size, device=self.device)
        sx = torch.exp(self.log_sx).clamp(min=0.005)
        sy = torch.exp(self.log_sy).clamp(min=0.005)
        opa = torch.sigmoid(self.opacity)

        for i in range(self.n):
            dx = coords_x - self.pos_x[i]
            dy = coords_y - self.pos_y[i]
            gauss = torch.exp(-0.5 * (dx**2 / sx[i]**2 + dy**2 / sy[i]**2))
            img = img + opa[i] * self.amplitude[i] * gauss

        return img.clamp(0, 1)

    def add_gaussians(self, new_pos_x, new_pos_y, new_sx, new_sy, new_amp):
        """Add new Gaussians to the field."""
        n_new = len(new_pos_x)
        if n_new == 0:
            return

        self.pos_x = torch.cat([self.pos_x.detach(), new_pos_x]).requires_grad_(True)
        self.pos_y = torch.cat([self.pos_y.detach(), new_pos_y]).requires_grad_(True)
        self.log_sx = torch.cat([self.log_sx.detach(), torch.log(new_sx)]).requires_grad_(True)
        self.log_sy = torch.cat([self.log_sy.detach(), torch.log(new_sy)]).requires_grad_(True)
        self.amplitude = torch.cat([self.amplitude.detach(), new_amp]).requires_grad_(True)
        self.opacity = torch.cat([self.opacity.detach(), torch.full((n_new,), 0.5, device=self.device)]).requires_grad_(True)

    def prune(self, min_opacity=0.01):
        """Remove low-opacity Gaussians."""
        opa = torch.sigmoid(self.opacity).detach()
        keep = opa > min_opacity
        if keep.all():
            return
        self.pos_x = self.pos_x.detach()[keep].requires_grad_(True)
        self.pos_y = self.pos_y.detach()[keep].requires_grad_(True)
        self.log_sx = self.log_sx.detach()[keep].requires_grad_(True)
        self.log_sy = self.log_sy.detach()[keep].requires_grad_(True)
        self.amplitude = self.amplitude.detach()[keep].requires_grad_(True)
        self.opacity = self.opacity.detach()[keep].requires_grad_(True)


# ── Densification Strategies ─────────────────────────────────────────

def densify_error_gated(field, target, max_new, max_gauss):
    """B: Error-gated densification (fair baseline — not naive ADC)."""
    if field.n >= max_gauss:
        return

    with torch.no_grad():
        rendered = field.render()
        error_map = (target - rendered) ** 2

        # Find high-error regions not covered by existing Gaussians
        px = (field.pos_x.detach() * field.size).long().clamp(0, field.size - 1)
        py = (field.pos_y.detach() * field.size).long().clamp(0, field.size - 1)

        # Sample candidate positions from high-error pixels
        error_flat = error_map.reshape(-1)
        topk = min(max_new * 5, error_flat.numel())
        _, top_idx = torch.topk(error_flat, topk)
        top_y = top_idx // field.size
        top_x = top_idx % field.size

        # Filter: only keep candidates far enough from existing Gaussians
        cand_x = top_x.float() / field.size
        cand_y = top_y.float() / field.size

        new_x, new_y, new_sx, new_sy, new_amp = [], [], [], [], []
        for i in range(len(cand_x)):
            if len(new_x) >= max_new or field.n + len(new_x) >= max_gauss:
                break
            cx, cy = cand_x[i], cand_y[i]
            # Min distance to existing Gaussians
            dists = ((field.pos_x.detach() - cx)**2 + (field.pos_y.detach() - cy)**2).sqrt()
            min_dist = dists.min().item()
            if min_dist > 0.02:  # Don't place too close to existing
                new_x.append(cx)
                new_y.append(cy)
                new_sx.append(torch.tensor(min_dist * 0.5, device=field.device))
                new_sy.append(torch.tensor(min_dist * 0.5, device=field.device))
                new_amp.append(torch.tensor(target[top_y[i], top_x[i]].item(), device=field.device))

        if new_x:
            field.add_gaussians(
                torch.stack(new_x), torch.stack(new_y),
                torch.stack(new_sx), torch.stack(new_sy),
                torch.stack(new_amp)
            )


def densify_farey(field, target, max_new, max_gauss, farey_level):
    """C: Farey-guided densification with mediant placement."""
    if field.n >= max_gauss:
        return

    with torch.no_grad():
        rendered = field.render()
        error_map = (target - rendered) ** 2

        pos_x = field.pos_x.detach()
        pos_y = field.pos_y.detach()
        sx = torch.exp(field.log_sx.detach()).clamp(min=0.005)
        sy = torch.exp(field.log_sy.detach()).clamp(min=0.005)

        # Sort by x for gap analysis
        sort_idx = torch.argsort(pos_x)
        sorted_x = pos_x[sort_idx]
        sorted_y = pos_y[sort_idx]
        sorted_sx = sx[sort_idx]
        sorted_sy = sy[sort_idx]

        # Compute gap ratios (Farey-style denominator analysis)
        candidates = []
        for i in range(len(sorted_x) - 1):
            gap_x = (sorted_x[i+1] - sorted_x[i]).item()
            avg_scale = (sorted_sx[i].item() + sorted_sx[i+1].item()) / 2

            if avg_scale < 1e-6:
                continue

            d_gap = gap_x / avg_scale  # "denominator" — larger = wider gap

            if d_gap <= farey_level:
                # Compute mediant position (sigma-weighted)
                w1 = 1.0 / (sorted_sx[i].item() + 1e-8)
                w2 = 1.0 / (sorted_sx[i+1].item() + 1e-8)
                med_x = (w1 * sorted_x[i].item() + w2 * sorted_x[i+1].item()) / (w1 + w2)
                med_y = (w1 * sorted_y[i].item() + w2 * sorted_y[i+1].item()) / (w1 + w2)

                # Check error at mediant position
                px = int(med_x * field.size)
                py = int(med_y * field.size)
                px = max(0, min(field.size - 1, px))
                py = max(0, min(field.size - 1, py))
                local_err = error_map[py, px].item()

                candidates.append((local_err, med_x, med_y, gap_x * 0.3, gap_x * 0.3,
                                    target[py, px].item()))

        # Also check y-axis gaps
        sort_idy = torch.argsort(pos_y)
        sorted_x2 = pos_x[sort_idy]
        sorted_y2 = pos_y[sort_idy]
        sorted_sy2 = sy[sort_idy]
        sorted_sx2 = sx[sort_idy]

        for i in range(len(sorted_y2) - 1):
            gap_y = (sorted_y2[i+1] - sorted_y2[i]).item()
            avg_scale = (sorted_sy2[i].item() + sorted_sy2[i+1].item()) / 2

            if avg_scale < 1e-6:
                continue

            d_gap = gap_y / avg_scale

            if d_gap <= farey_level:
                w1 = 1.0 / (sorted_sy2[i].item() + 1e-8)
                w2 = 1.0 / (sorted_sy2[i+1].item() + 1e-8)
                med_y = (w1 * sorted_y2[i].item() + w2 * sorted_y2[i+1].item()) / (w1 + w2)
                med_x = (w1 * sorted_x2[i].item() + w2 * sorted_x2[i+1].item()) / (w1 + w2)

                px = int(med_x * field.size)
                py = int(med_y * field.size)
                px = max(0, min(field.size - 1, px))
                py = max(0, min(field.size - 1, py))
                local_err = error_map[py, px].item()

                candidates.append((local_err, med_x, med_y, gap_y * 0.3, gap_y * 0.3,
                                    target[py, px].item()))

        # Sort by error (highest first), take top max_new
        candidates.sort(key=lambda c: -c[0])

        new_x, new_y, new_sx, new_sy, new_amp = [], [], [], [], []
        used_positions = set()

        for err, mx, my, nsx, nsy, amp in candidates:
            if len(new_x) >= max_new or field.n + len(new_x) >= max_gauss:
                break

            # Quantize to avoid duplicates
            key = (round(mx, 3), round(my, 3))
            if key in used_positions:
                continue
            used_positions.add(key)

            # Only insert if error is above threshold
            if err > 0.001:
                new_x.append(torch.tensor(mx, device=field.device))
                new_y.append(torch.tensor(my, device=field.device))
                new_sx.append(torch.tensor(max(nsx, 0.005), device=field.device))
                new_sy.append(torch.tensor(max(nsy, 0.005), device=field.device))
                new_amp.append(torch.tensor(amp, device=field.device))

        if new_x:
            field.add_gaussians(
                torch.stack(new_x), torch.stack(new_y),
                torch.stack(new_sx), torch.stack(new_sy),
                torch.stack(new_amp)
            )


# ── Training Loop ────────────────────────────────────────────────────

def train_run(target, method, steps, densify_interval, max_gauss, max_new, n_init=500,
              farey_start=45, farey_increment=5):
    """Train one run. method='adc' or 'farey'."""
    size = target.shape[0]
    field = GaussianField2D(n_init, size, DEVICE)

    optimizer = torch.optim.Adam(field.params(), lr=0.005)

    farey_level = farey_start
    t0 = time.time()

    for step in range(steps):
        optimizer.zero_grad()
        rendered = field.render()
        loss = ((target - rendered) ** 2).mean()
        loss.backward()
        optimizer.step()

        # Densification
        if step > 0 and step % densify_interval == 0:
            if method == 'adc':
                densify_error_gated(field, target, max_new, max_gauss)
            else:
                densify_farey(field, target, max_new, max_gauss, farey_level)
                farey_level += farey_increment

            # Prune
            field.prune(min_opacity=0.01)

            # Reset optimizer
            optimizer = torch.optim.Adam(field.params(), lr=0.005 * (0.95 ** (step // 500)))

        if step % 500 == 0:
            elapsed = time.time() - t0
            psnr = -10 * np.log10(loss.item() + 1e-10)
            print(f"    Step {step:5d}: PSNR={psnr:.2f} dB  G={field.n}  t={elapsed:.0f}s", flush=True)

    # Final metrics
    with torch.no_grad():
        rendered = field.render()
        mse = ((target - rendered) ** 2).mean().item()
        psnr = -10 * np.log10(mse + 1e-10)

        rendered_np = rendered.cpu().numpy()
        target_np = target.cpu().numpy()
        ssim_val = ssim(target_np, rendered_np, data_range=1.0)

    elapsed = time.time() - t0
    return {
        'psnr': psnr, 'ssim': ssim_val, 'mse': mse,
        'n_gauss': field.n, 'time': elapsed
    }


# ── Run Config ───────────────────────────────────────────────────────

def run_config(name, target, steps, densify_interval, max_gauss, max_new, n_init=500):
    """Run B (error-gated) and C (Farey), compare."""
    print(f"\n{'='*50}", flush=True)
    print(f"  {name} ({steps} steps, int={densify_interval}, max_g={max_gauss}, max_new={max_new})", flush=True)
    print(f"{'='*50}", flush=True)

    print(f"\n  --- B_errgate_{name} ---", flush=True)
    res_b = train_run(target, 'adc', steps, densify_interval, max_gauss, max_new, n_init)
    print(f"    RESULT: PSNR={res_b['psnr']:.2f} dB  SSIM={res_b['ssim']:.4f}  G={res_b['n_gauss']}  time={res_b['time']:.0f}s", flush=True)

    print(f"\n  --- C_farey_{name} ---", flush=True)
    res_c = train_run(target, 'farey', steps, densify_interval, max_gauss, max_new, n_init)
    print(f"    RESULT: PSNR={res_c['psnr']:.2f} dB  SSIM={res_c['ssim']:.4f}  G={res_c['n_gauss']}  time={res_c['time']:.0f}s", flush=True)

    delta = res_c['psnr'] - res_b['psnr']
    print(f"  >>> {name}: B={res_b['psnr']:.2f}  C={res_c['psnr']:.2f}  Delta={delta:+.2f} dB <<<", flush=True)

    result = {'name': name, 'adc': res_b, 'farey': res_c, 'delta_db': delta}
    ALL_RESULTS.append(result)

    # Save incrementally
    with open(os.path.join(RESULTS_DIR, 'series3_budget.json'), 'w') as f:
        json.dump(ALL_RESULTS, f, indent=2)

    return result


# ══════════════════════════════════════════════════════════════════════
# SERIES 3: Densification Budget
# Best params from Series 1+2: 6000 steps, interval=200, 256x256, 500 init
# ══════════════════════════════════════════════════════════════════════

print("\n" + "="*60, flush=True)
print("  SERIES 3: Densification Budget (6000 steps, int=200, 256x256)", flush=True)
print("="*60, flush=True)

target = make_target(256)

for max_new in [10, 20, 30, 50, 100, 9999]:
    label = "unlimited" if max_new == 9999 else str(max_new)
    run_config(f"3_{label}", target, 6000, 200, 2000, max_new, n_init=500)

# ── Summary ──────────────────────────────────────────────────────────

print("\n" + "="*60, flush=True)
print("  SERIES 3 SUMMARY", flush=True)
print("="*60, flush=True)
print(f"{'Config':<25} {'B PSNR':>10} {'C PSNR':>10} {'Delta':>8} {'B Gauss':>8} {'C Gauss':>8}", flush=True)
print("-"*70, flush=True)
for r in ALL_RESULTS:
    print(f"{r['name']:<25} {r['adc']['psnr']:>10.2f} {r['farey']['psnr']:>10.2f} {r['delta_db']:>+8.2f} {r['adc']['n_gauss']:>8} {r['farey']['n_gauss']:>8}", flush=True)

avg_delta = np.mean([r['delta_db'] for r in ALL_RESULTS])
print(f"\nAverage Delta: {avg_delta:+.2f} dB across {len(ALL_RESULTS)} configs", flush=True)
print(f"\nBest config saved. Use max_new={ALL_RESULTS[np.argmax([r['delta_db'] for r in ALL_RESULTS])]['name'].split('_')[1]} for Series 4.", flush=True)
