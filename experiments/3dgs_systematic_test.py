#!/usr/bin/env python3
"""
3DGS Systematic Ablation: Series 2g-C through Series 5
======================================================
Picks up from where the previous run crashed.

Series 2g: Complete 6000 steps, interval=100 (C only - B already done: 25.83 dB)
Series 3: Scene complexity (more challenging targets)
Series 4: Gaussian budget caps (200, 500, 1000, 2000)
Series 5: max_new_per_step (5, 15, 30, 60)

Uses MPS (Apple Silicon GPU) via PyTorch.
"""

import torch
import numpy as np
import time, json, os, sys

DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Device: {DEVICE}")

RESULTS_DIR = "/Users/saar/Desktop/Farey-Local/experiments/3dgs_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

ALL_RESULTS = []

# ── Target scene generators ─────────────────────────────────────────

def make_scene_simple(size=128):
    """Smooth gradient + checkerboard patch (baseline scene)."""
    y = torch.linspace(0, 1, size, device=DEVICE)
    x = torch.linspace(0, 1, size, device=DEVICE)
    X, Y = torch.meshgrid(x, y, indexing='ij')
    img = 0.3 * torch.sin(2*np.pi*X) * torch.cos(2*np.pi*Y) + 0.5
    freq = 16
    checker = 0.5 * (torch.sign(torch.sin(freq*np.pi*X) * torch.sin(freq*np.pi*Y)) + 1)
    mask = ((X >= 0.3) & (X <= 0.7) & (Y >= 0.3) & (Y <= 0.7)).float()
    img = img * (1 - mask) + checker * mask
    return img

def make_scene_complex(size=128):
    """Multiple frequency regions + edges + noise."""
    y = torch.linspace(0, 1, size, device=DEVICE)
    x = torch.linspace(0, 1, size, device=DEVICE)
    X, Y = torch.meshgrid(x, y, indexing='ij')

    # base: smooth
    img = 0.5 + 0.2*torch.sin(4*np.pi*X)*torch.cos(6*np.pi*Y)

    # high-freq patch 1 (top-left)
    m1 = ((X < 0.3) & (Y < 0.3)).float()
    img = img*(1-m1) + 0.5*(torch.sign(torch.sin(30*np.pi*X)*torch.sin(30*np.pi*Y))+1)*m1

    # high-freq patch 2 (bottom-right, different freq)
    m2 = ((X > 0.7) & (Y > 0.7)).float()
    img = img*(1-m2) + 0.5*(torch.sign(torch.sin(20*np.pi*X)*torch.sin(40*np.pi*Y))+1)*m2

    # sharp edge (diagonal)
    edge = (X + Y > 1.0).float() * 0.3
    img = img + edge * (1-m1) * (1-m2)

    return img.clamp(0, 1)

def make_scene_natural(size=128):
    """Simulated natural scene: gabor-like textures + smooth gradients."""
    y = torch.linspace(0, 1, size, device=DEVICE)
    x = torch.linspace(0, 1, size, device=DEVICE)
    X, Y = torch.meshgrid(x, y, indexing='ij')

    img = torch.zeros_like(X)
    # Multiple gabor patches at different orientations/frequencies
    for cx, cy, freq, angle, sigma in [
        (0.25, 0.25, 12, 0.3, 0.15),
        (0.75, 0.25, 20, 1.0, 0.12),
        (0.25, 0.75, 8, 0.7, 0.18),
        (0.75, 0.75, 25, 1.5, 0.10),
        (0.50, 0.50, 15, 0.0, 0.20),
    ]:
        dx = X - cx
        dy = Y - cy
        gauss = torch.exp(-(dx**2 + dy**2)/(2*sigma**2))
        oriented = dx*np.cos(angle) + dy*np.sin(angle)
        img = img + gauss * (0.5*torch.sin(freq*np.pi*oriented) + 0.5)

    img = img / img.max()
    return img.clamp(0, 1)

# ── Core 2D Gaussian splatting engine ────────────────────────────────

def render_gaussians(pos, sigma, opacity, amp, size):
    """Render 2D isotropic Gaussians onto an image grid."""
    y = torch.linspace(0, 1, size, device=DEVICE)
    x = torch.linspace(0, 1, size, device=DEVICE)
    X, Y = torch.meshgrid(x, y, indexing='ij')  # [size, size]

    img = torch.zeros(size, size, device=DEVICE)
    for i in range(len(pos)):
        dx = X - pos[i, 0]
        dy = Y - pos[i, 1]
        g = torch.exp(-(dx**2 + dy**2) / (2 * sigma[i]**2 + 1e-8))
        img = img + opacity[i] * amp[i] * g
    return img

def compute_psnr(img, target):
    mse = ((img - target)**2).mean().item()
    if mse < 1e-10:
        return 50.0
    return -10 * np.log10(mse)

def compute_ssim_simple(img, target):
    """Simplified SSIM approximation."""
    mu_x = img.mean()
    mu_y = target.mean()
    sig_x = img.var()
    sig_y = target.var()
    sig_xy = ((img - mu_x) * (target - mu_y)).mean()
    c1, c2 = 0.01**2, 0.03**2
    ssim = ((2*mu_x*mu_y + c1)*(2*sig_xy + c2)) / ((mu_x**2 + mu_y**2 + c1)*(sig_x + sig_y + c2))
    return ssim.item()

# ── ADC densification ────────────────────────────────────────────────

def densify_adc(pos, sigma, opacity, amp, target, max_gauss, max_new=30):
    """Standard ADC: split Gaussians with highest gradient magnitude."""
    n = len(pos)
    if n >= max_gauss:
        return pos, sigma, opacity, amp

    pos_g = pos.grad
    if pos_g is None:
        return pos, sigma, opacity, amp

    grad_mag = pos_g.norm(dim=1)
    threshold = grad_mag.quantile(0.8).item()
    mask = grad_mag > threshold

    if mask.sum() == 0:
        return pos, sigma, opacity, amp

    indices = mask.nonzero(as_tuple=True)[0]
    n_new = min(len(indices), max_new, max_gauss - n)
    if n_new <= 0:
        return pos, sigma, opacity, amp

    idx = indices[:n_new]
    offset = torch.randn(n_new, 2, device=DEVICE) * sigma[idx].unsqueeze(1) * 0.5

    new_pos = pos[idx] + offset
    new_sigma = sigma[idx] * 0.7
    new_opacity = opacity[idx] * 0.8
    new_amp = amp[idx].clone()

    pos = torch.cat([pos, new_pos.detach()])
    sigma = torch.cat([sigma, new_sigma.detach()])
    opacity = torch.cat([opacity, new_opacity.detach()])
    amp = torch.cat([amp, new_amp.detach()])

    return pos, sigma, opacity, amp

# ── Farey densification ─────────────────────────────────────────────

def densify_farey(pos, sigma, opacity, amp, target, max_gauss, step, total_steps, max_new=30):
    """Farey-guided: inject at mediant positions in under-resolved gaps."""
    n = len(pos)
    if n >= max_gauss:
        return pos, sigma, opacity, amp

    size = target.shape[0]
    rendered = render_gaussians(pos.detach(), sigma.detach(), opacity.detach(), amp.detach(), size)
    error_map = (rendered - target).abs()

    # Farey level increases over training
    farey_level = 2 + int(8 * step / total_steps)

    # Sort by x, find gaps
    sx = pos[:, 0].detach().cpu().numpy()
    sy = pos[:, 1].detach().cpu().numpy()
    ss = sigma.detach().cpu().numpy()

    order_x = np.argsort(sx)

    candidates = []
    for i in range(len(order_x) - 1):
        i0, i1 = order_x[i], order_x[i+1]
        gap = abs(sx[i1] - sx[i0])
        r_sum = ss[i0] + ss[i1]
        if r_sum < 1e-8:
            continue
        d_gap = gap / r_sum

        if d_gap <= farey_level:
            # Mediant position (sigma-weighted)
            w0 = 1.0 / (ss[i0] + 1e-8)
            w1 = 1.0 / (ss[i1] + 1e-8)
            mx = (w0 * sx[i0] + w1 * sx[i1]) / (w0 + w1)
            my = (w0 * sy[i0] + w1 * sy[i1]) / (w0 + w1)

            # Check local error
            px = int(np.clip(mx * size, 0, size-1))
            py = int(np.clip(my * size, 0, size-1))
            local_err = error_map[max(0,px-3):min(size,px+4), max(0,py-3):min(size,py+4)].mean().item()

            candidates.append((local_err, mx, my, (ss[i0] + ss[i1])/2 * 0.5))

    # Also check y-gaps
    order_y = np.argsort(sy)
    for i in range(len(order_y) - 1):
        i0, i1 = order_y[i], order_y[i+1]
        gap = abs(sy[i1] - sy[i0])
        r_sum = ss[i0] + ss[i1]
        if r_sum < 1e-8:
            continue
        d_gap = gap / r_sum

        if d_gap <= farey_level:
            w0 = 1.0 / (ss[i0] + 1e-8)
            w1 = 1.0 / (ss[i1] + 1e-8)
            mx = (w0 * sx[i0] + w1 * sx[i1]) / (w0 + w1)
            my = (w0 * sy[i0] + w1 * sy[i1]) / (w0 + w1)

            px = int(np.clip(mx * size, 0, size-1))
            py = int(np.clip(my * size, 0, size-1))
            local_err = error_map[max(0,px-3):min(size,px+4), max(0,py-3):min(size,py+4)].mean().item()

            candidates.append((local_err, mx, my, (ss[i0] + ss[i1])/2 * 0.5))

    if not candidates:
        return pos, sigma, opacity, amp

    # Sort by error (highest first), take top max_new
    candidates.sort(key=lambda x: -x[0])
    n_new = min(len(candidates), max_new, max_gauss - n)
    if n_new <= 0:
        return pos, sigma, opacity, amp

    new_pos_list = []
    new_sigma_list = []
    for err, mx, my, ms in candidates[:n_new]:
        new_pos_list.append([mx, my])
        new_sigma_list.append(ms)

    new_pos = torch.tensor(new_pos_list, device=DEVICE, dtype=torch.float32)
    new_sigma = torch.tensor(new_sigma_list, device=DEVICE, dtype=torch.float32)
    new_opacity = torch.ones(n_new, device=DEVICE) * 0.5
    new_amp = torch.ones(n_new, device=DEVICE) * 0.5

    pos = torch.cat([pos, new_pos])
    sigma = torch.cat([sigma, new_sigma])
    opacity = torch.cat([opacity, new_opacity])
    amp = torch.cat([amp, new_amp])

    return pos, sigma, opacity, amp

# ── Pruning ──────────────────────────────────────────────────────────

def prune(pos, sigma, opacity, amp, min_opacity=0.01):
    """Remove low-opacity Gaussians."""
    mask = opacity > min_opacity
    if mask.sum() < 10:
        return pos, sigma, opacity, amp
    return pos[mask], sigma[mask], opacity[mask], amp[mask]

# ── Training loop ────────────────────────────────────────────────────

def train_run(target, method, steps, densify_interval, max_gauss, max_new=30, init_k=10, prune_every=500):
    """Run one training configuration. method='adc' or 'farey'."""
    size = target.shape[0]

    # Init grid
    g = torch.linspace(0.1, 0.9, init_k, device=DEVICE)
    gx, gy = torch.meshgrid(g, g, indexing='ij')
    pos = torch.stack([gx.flatten(), gy.flatten()], dim=1).clone()
    n_init = len(pos)
    sigma = torch.ones(n_init, device=DEVICE) * (0.8 / init_k)
    opacity = torch.ones(n_init, device=DEVICE) * 0.5
    amp = torch.ones(n_init, device=DEVICE) * 0.5

    pos.requires_grad_(True)
    sigma.requires_grad_(True)
    opacity.requires_grad_(True)
    amp.requires_grad_(True)

    opt = torch.optim.Adam([pos, sigma, opacity, amp], lr=0.005)

    t0 = time.time()
    for step in range(steps):
        opt.zero_grad()
        rendered = render_gaussians(pos, sigma, opacity, amp, size)
        loss = ((rendered - target)**2).mean()
        loss.backward()
        opt.step()

        with torch.no_grad():
            sigma.clamp_(min=0.001, max=0.5)
            opacity.clamp_(min=0.0, max=1.0)
            pos.clamp_(min=0.0, max=1.0)

        # Densify
        if step > 0 and step % densify_interval == 0:
            with torch.no_grad():
                if method == 'adc':
                    pos, sigma, opacity, amp = densify_adc(
                        pos, sigma, opacity, amp, target, max_gauss, max_new)
                else:
                    pos, sigma, opacity, amp = densify_farey(
                        pos, sigma, opacity, amp, target, max_gauss, step, steps, max_new)

            pos = pos.detach().requires_grad_(True)
            sigma = sigma.detach().requires_grad_(True)
            opacity = opacity.detach().requires_grad_(True)
            amp = amp.detach().requires_grad_(True)
            opt = torch.optim.Adam([pos, sigma, opacity, amp], lr=0.005)

        # Prune
        if step > 0 and step % prune_every == 0:
            with torch.no_grad():
                pos, sigma, opacity, amp = prune(pos, sigma, opacity, amp)
            pos = pos.detach().requires_grad_(True)
            sigma = sigma.detach().requires_grad_(True)
            opacity = opacity.detach().requires_grad_(True)
            amp = amp.detach().requires_grad_(True)
            opt = torch.optim.Adam([pos, sigma, opacity, amp], lr=0.005)

        if step % 500 == 0:
            psnr = compute_psnr(rendered.detach(), target)
            print(f"    Step {step:5d}: PSNR={psnr:.2f} dB  G={len(pos)}  t={time.time()-t0:.0f}s", flush=True)

    with torch.no_grad():
        final_img = render_gaussians(pos, sigma, opacity, amp, size)
        psnr = compute_psnr(final_img, target)
        ssim = compute_ssim_simple(final_img, target)

    elapsed = time.time() - t0
    return {
        'psnr': psnr, 'ssim': ssim, 'n_gauss': len(pos),
        'time': elapsed, 'method': method
    }

# ── Run a config ─────────────────────────────────────────────────────

def run_config(name, target, steps, densify_interval, max_gauss=500, max_new=30, init_k=10):
    print(f"\n{'='*50}", flush=True)
    print(f"  {name} ({steps} steps, int={densify_interval}, max_g={max_gauss}, max_new={max_new})", flush=True)
    print(f"{'='*50}", flush=True)

    print(f"\n  --- B_adc_{name} ---", flush=True)
    res_b = train_run(target, 'adc', steps, densify_interval, max_gauss, max_new, init_k)
    print(f"    RESULT: PSNR={res_b['psnr']:.2f} dB  SSIM={res_b['ssim']:.4f}  G={res_b['n_gauss']}  time={res_b['time']:.0f}s", flush=True)

    print(f"\n  --- C_farey_{name} ---", flush=True)
    res_c = train_run(target, 'farey', steps, densify_interval, max_gauss, max_new, init_k)
    print(f"    RESULT: PSNR={res_c['psnr']:.2f} dB  SSIM={res_c['ssim']:.4f}  G={res_c['n_gauss']}  time={res_c['time']:.0f}s", flush=True)

    delta = res_c['psnr'] - res_b['psnr']
    print(f"  >>> {name}: B={res_b['psnr']:.2f}  C={res_c['psnr']:.2f}  Delta={delta:+.2f} dB <<<", flush=True)

    result = {'name': name, 'adc': res_b, 'farey': res_c, 'delta_db': delta}
    ALL_RESULTS.append(result)

    # Save incrementally
    with open(os.path.join(RESULTS_DIR, 'all_results.json'), 'w') as f:
        json.dump(ALL_RESULTS, f, indent=2)

    return result

# ══════════════════════════════════════════════════════════════════════
# SERIES 3: Scene complexity
# ══════════════════════════════════════════════════════════════════════

print("\n" + "="*60, flush=True)
print("  SERIES 3: Scene Complexity (4000 steps, int=200)", flush=True)
print("="*60, flush=True)

target_simple = make_scene_simple(128)
target_complex = make_scene_complex(128)
target_natural = make_scene_natural(128)

run_config("3a_simple", target_simple, 4000, 200, 500, 30)
run_config("3b_complex", target_complex, 4000, 200, 500, 30)
run_config("3c_natural", target_natural, 4000, 200, 500, 30)

# ══════════════════════════════════════════════════════════════════════
# SERIES 4: Gaussian budget
# ══════════════════════════════════════════════════════════════════════

print("\n" + "="*60, flush=True)
print("  SERIES 4: Gaussian Budget (4000 steps, int=200, complex scene)", flush=True)
print("="*60, flush=True)

for max_g in [200, 500, 1000]:
    run_config(f"4_{max_g}gauss", target_complex, 4000, 200, max_g, 30)

# ══════════════════════════════════════════════════════════════════════
# SERIES 5: max_new_per_step
# ══════════════════════════════════════════════════════════════════════

print("\n" + "="*60, flush=True)
print("  SERIES 5: Max New Per Step (4000 steps, int=200, complex scene)", flush=True)
print("="*60, flush=True)

for mn in [5, 15, 30, 60]:
    run_config(f"5_maxnew{mn}", target_complex, 4000, 200, 500, mn)

# ══════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════════

print("\n" + "="*60, flush=True)
print("  FINAL SUMMARY", flush=True)
print("="*60, flush=True)
print(f"{'Config':<25} {'ADC PSNR':>10} {'Farey PSNR':>12} {'Delta':>8}", flush=True)
print("-"*60, flush=True)
for r in ALL_RESULTS:
    print(f"{r['name']:<25} {r['adc']['psnr']:>10.2f} {r['farey']['psnr']:>12.2f} {r['delta_db']:>+8.2f}", flush=True)

avg_delta = np.mean([r['delta_db'] for r in ALL_RESULTS])
print(f"\nAverage Delta: {avg_delta:+.2f} dB across {len(ALL_RESULTS)} configs", flush=True)

# Save final
with open(os.path.join(RESULTS_DIR, 'all_results.json'), 'w') as f:
    json.dump(ALL_RESULTS, f, indent=2)
print(f"\nResults saved to {RESULTS_DIR}/all_results.json", flush=True)
