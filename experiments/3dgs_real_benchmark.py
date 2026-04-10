#!/usr/bin/env python3
"""
2D Gaussian Splatting Real Image Benchmark
==========================================
Compares Farey densification vs ADC (and other methods) on the Kodak dataset.

Follows the GaussianImage (ECCV 2024) paradigm: represent a real photograph
using 2D Gaussians with learned positions, scales, rotations, colors, opacities.

Key differences from our synthetic benchmark:
- RGB images (3 channels)
- Full anisotropic 2D Gaussians (rotation + 2 scale params)
- Proper SSIM via scikit-image
- Kodak dataset (standard benchmark, 768x512)
- Multiple seeds for statistical rigor
- Budget-matched comparison mode

Usage:
  python3 3dgs_real_benchmark.py --mode quick    # 1 image, 1 seed, low steps
  python3 3dgs_real_benchmark.py --mode full     # all 24 images, 5 seeds
  python3 3dgs_real_benchmark.py --mode budget   # budget-matched comparison
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import time
import json
import os
import sys
import argparse
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────

DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
DATA_DIR = Path(__file__).parent / "3dgs_benchmark_data" / "kodak"
RESULTS_DIR = Path(__file__).parent / "3dgs_results"
RESULTS_DIR.mkdir(exist_ok=True)

print(f"Device: {DEVICE}")
print(f"Data dir: {DATA_DIR}")


# ── Image loading ────────────────────────────────────────────────────

def load_image(path, max_size=None):
    """Load image as torch tensor [H, W, 3] in [0, 1]."""
    from PIL import Image
    img = Image.open(path).convert("RGB")
    if max_size is not None:
        # Downsample for speed while maintaining aspect ratio
        w, h = img.size
        scale = min(max_size / max(w, h), 1.0)
        if scale < 1.0:
            new_w, new_h = int(w * scale), int(h * scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)
    arr = np.array(img).astype(np.float32) / 255.0
    return torch.from_numpy(arr).to(DEVICE)


def list_kodak_images():
    """Return sorted list of Kodak image paths."""
    images = sorted(DATA_DIR.glob("kodim*.png"))
    if not images:
        raise FileNotFoundError(
            f"No Kodak images found in {DATA_DIR}. "
            "Download from http://r0k.us/graphics/kodak/kodak/kodimXX.png"
        )
    return images


# ── Proper SSIM ──────────────────────────────────────────────────────

def compute_ssim(img, target):
    """Compute SSIM using scikit-image (proper implementation)."""
    from skimage.metrics import structural_similarity as ssim
    img_np = img.detach().cpu().numpy()
    target_np = target.detach().cpu().numpy()
    return ssim(img_np, target_np, channel_axis=2, data_range=1.0)


def compute_psnr(img, target):
    """Compute PSNR in dB."""
    mse = ((img - target) ** 2).mean().item()
    if mse < 1e-10:
        return 60.0
    return -10.0 * np.log10(mse)


# ── 2D Gaussian Splatting Model ──────────────────────────────────────

class GaussianModel2D(nn.Module):
    """
    2D anisotropic Gaussian splatting model.

    Each Gaussian has:
    - position (x, y) in [0, 1]
    - log_scale (sx, sy) for anisotropic extent
    - rotation angle theta
    - color (r, g, b) as logits (sigmoid-activated)
    - opacity logit (sigmoid-activated)

    Total: 8 parameters per Gaussian (same as GaussianImage ECCV 2024).
    """

    def __init__(self, n_gaussians, H, W):
        super().__init__()
        self.H = H
        self.W = W
        self.n_init = n_gaussians

        # Initialize on a grid
        n_side = int(np.ceil(np.sqrt(n_gaussians)))
        xs = torch.linspace(0.05, 0.95, n_side)
        ys = torch.linspace(0.05, 0.95, n_side)
        gx, gy = torch.meshgrid(xs, ys, indexing='ij')
        positions = torch.stack([gx.flatten(), gy.flatten()], dim=1)[:n_gaussians]

        self.positions = nn.Parameter(positions)  # [N, 2]
        self.log_scales = nn.Parameter(
            torch.full((n_gaussians, 2), np.log(1.0 / n_side))
        )  # [N, 2]
        self.rotations = nn.Parameter(torch.zeros(n_gaussians))  # [N]
        self.color_logits = nn.Parameter(torch.zeros(n_gaussians, 3))  # [N, 3]
        self.opacity_logits = nn.Parameter(torch.full((n_gaussians,), 2.0))  # [N]

    @property
    def n_gaussians(self):
        return self.positions.shape[0]

    def get_colors(self):
        return torch.sigmoid(self.color_logits)

    def get_opacities(self):
        return torch.sigmoid(self.opacity_logits)

    def get_scales(self):
        return torch.exp(self.log_scales).clamp(min=1e-5, max=1.0)

    def render(self, H=None, W=None):
        """
        Render all Gaussians onto an [H, W, 3] image.
        Uses accumulated summation (GaussianImage ECCV 2024 style).
        Each Gaussian contributes: opacity * gaussian_weight * color, summed directly.
        """
        if H is None:
            H = self.H
        if W is None:
            W = self.W

        positions = self.positions  # [N, 2]
        scales = self.get_scales()  # [N, 2]
        theta = self.rotations     # [N]
        colors = self.get_colors() # [N, 3]
        alpha = self.get_opacities()  # [N]

        N = positions.shape[0]

        # Create pixel grid (normalized to [0, 1])
        ys = torch.linspace(0, 1, H, device=positions.device)
        xs = torch.linspace(0, 1, W, device=positions.device)
        grid_y, grid_x = torch.meshgrid(ys, xs, indexing='ij')  # [H, W]

        # Process in chunks to avoid OOM on large images
        chunk_size = max(1, min(N, 256))
        accumulated = torch.zeros(H, W, 3, device=positions.device)

        for start in range(0, N, chunk_size):
            end = min(start + chunk_size, N)
            n_chunk = end - start

            pos_chunk = positions[start:end]     # [C, 2]
            scale_chunk = scales[start:end]      # [C, 2]
            theta_chunk = theta[start:end]       # [C]
            color_chunk = colors[start:end]      # [C, 3]
            alpha_chunk = alpha[start:end]       # [C]

            # Offset from each pixel to each Gaussian center
            dx = grid_x.unsqueeze(-1) - pos_chunk[:, 1].view(1, 1, n_chunk)  # [H, W, C]
            dy = grid_y.unsqueeze(-1) - pos_chunk[:, 0].view(1, 1, n_chunk)  # [H, W, C]

            # Rotation
            cos_t = torch.cos(theta_chunk).view(1, 1, n_chunk)
            sin_t = torch.sin(theta_chunk).view(1, 1, n_chunk)
            rx = cos_t * dx + sin_t * dy   # [H, W, C]
            ry = -sin_t * dx + cos_t * dy  # [H, W, C]

            # Anisotropic Gaussian
            sx = scale_chunk[:, 0].view(1, 1, n_chunk)
            sy = scale_chunk[:, 1].view(1, 1, n_chunk)
            exponent = -0.5 * ((rx / sx) ** 2 + (ry / sy) ** 2)
            weights = alpha_chunk.view(1, 1, n_chunk) * torch.exp(exponent)  # [H, W, C]

            # Accumulated summation: sum(weight_i * color_i) directly
            weighted_colors = weights.unsqueeze(-1) * color_chunk.view(1, 1, n_chunk, 3)
            accumulated += weighted_colors.sum(dim=2)

        return accumulated.clamp(0, 1)

    def add_gaussians(self, new_positions, new_log_scales=None, new_rotations=None,
                      new_color_logits=None, new_opacity_logits=None):
        """Add new Gaussians to the model."""
        n_new = new_positions.shape[0]
        if n_new == 0:
            return

        device = self.positions.device

        if new_log_scales is None:
            new_log_scales = torch.full((n_new, 2), np.log(0.02), device=device)
        if new_rotations is None:
            new_rotations = torch.zeros(n_new, device=device)
        if new_color_logits is None:
            new_color_logits = torch.zeros(n_new, 3, device=device)
        if new_opacity_logits is None:
            new_opacity_logits = torch.full((n_new,), 1.0, device=device)

        self.positions = nn.Parameter(
            torch.cat([self.positions.data, new_positions.to(device)], dim=0)
        )
        self.log_scales = nn.Parameter(
            torch.cat([self.log_scales.data, new_log_scales.to(device)], dim=0)
        )
        self.rotations = nn.Parameter(
            torch.cat([self.rotations.data, new_rotations.to(device)], dim=0)
        )
        self.color_logits = nn.Parameter(
            torch.cat([self.color_logits.data, new_color_logits.to(device)], dim=0)
        )
        self.opacity_logits = nn.Parameter(
            torch.cat([self.opacity_logits.data, new_opacity_logits.to(device)], dim=0)
        )

    def prune_gaussians(self, keep_mask):
        """Remove Gaussians where keep_mask is False."""
        self.positions = nn.Parameter(self.positions.data[keep_mask])
        self.log_scales = nn.Parameter(self.log_scales.data[keep_mask])
        self.rotations = nn.Parameter(self.rotations.data[keep_mask])
        self.color_logits = nn.Parameter(self.color_logits.data[keep_mask])
        self.opacity_logits = nn.Parameter(self.opacity_logits.data[keep_mask])


# ── Densification Strategies ─────────────────────────────────────────

def densify_adc(model, target, grad_accum, step, max_gaussians, max_new=30):
    """
    Adaptive Density Control (ADC) - standard 3DGS method.
    Split/clone Gaussians with large positional gradients.
    """
    n = model.n_gaussians
    if n >= max_gaussians:
        return

    if grad_accum is None or grad_accum.shape[0] != n:
        return

    grad_mag = grad_accum.norm(dim=1)
    if grad_mag.max() < 1e-6:
        return

    threshold = grad_mag.quantile(0.8).item()
    mask = grad_mag > threshold

    if mask.sum() == 0:
        return

    indices = mask.nonzero(as_tuple=True)[0]
    n_new = min(len(indices), max_new, max_gaussians - n)
    if n_new <= 0:
        return

    idx = indices[:n_new]
    scales = model.get_scales()

    # Clone small Gaussians, split large ones
    avg_scale = scales.mean().item()
    large_mask = scales[idx].mean(dim=1) > avg_scale

    new_positions = []
    new_log_scales = []
    new_rotations = []
    new_color_logits = []
    new_opacity_logits = []

    for i, gi in enumerate(idx):
        pos = model.positions.data[gi]
        if large_mask[i]:
            # Split: offset by scale
            offset = torch.randn(2, device=DEVICE) * scales[gi] * 0.5
            new_positions.append(pos + offset)
            new_log_scales.append(model.log_scales.data[gi] - np.log(1.6))
        else:
            # Clone: small offset
            offset = torch.randn(2, device=DEVICE) * 0.01
            new_positions.append(pos + offset)
            new_log_scales.append(model.log_scales.data[gi].clone())

        new_rotations.append(model.rotations.data[gi:gi+1])
        new_color_logits.append(model.color_logits.data[gi:gi+1])
        new_opacity_logits.append(model.opacity_logits.data[gi:gi+1])

    new_pos = torch.stack(new_positions)
    new_ls = torch.stack(new_log_scales)
    new_rot = torch.cat(new_rotations)
    new_col = torch.cat(new_color_logits)
    new_opa = torch.cat(new_opacity_logits)

    model.add_gaussians(new_pos, new_ls, new_rot, new_col, new_opa)


def densify_farey(model, target, grad_accum, step, total_steps, max_gaussians, max_new=30):
    """
    Farey-guided densification.

    Core idea: use Farey mediant positions to identify optimal placement
    for new Gaussians in under-resolved gaps, guided by local error.

    1. Sort Gaussians by position (x and y separately)
    2. For consecutive pairs, compute gap/radius ratio
    3. At Farey level k, inject mediants where gap ratio <= k AND local error is high
    4. New Gaussian inherits interpolated properties from neighbors
    """
    n = model.n_gaussians
    if n >= max_gaussians:
        return

    H, W = model.H, model.W

    # Compute error map
    with torch.no_grad():
        rendered = model.render()
        error_map = (rendered - target).pow(2).sum(dim=-1)  # [H, W]

    # Farey level increases over training (adaptive refinement)
    progress = step / max(total_steps, 1)
    farey_level = 2 + int(8 * progress)

    pos = model.positions.data.cpu().numpy()   # [N, 2]
    scales = model.get_scales().data.cpu().numpy()  # [N, 2]
    avg_scales = scales.mean(axis=1)  # [N]

    candidates = []

    # Check gaps along both axes
    for axis in [0, 1]:
        order = np.argsort(pos[:, axis])
        for i in range(len(order) - 1):
            i0, i1 = order[i], order[i + 1]
            gap = abs(pos[i1, axis] - pos[i0, axis])
            r_sum = avg_scales[i0] + avg_scales[i1]
            if r_sum < 1e-8:
                continue
            d_gap = gap / r_sum

            if d_gap > farey_level:
                continue

            # Farey mediant: weighted by inverse scale (finer Gaussians pull more)
            w0 = 1.0 / (avg_scales[i0] + 1e-6)
            w1 = 1.0 / (avg_scales[i1] + 1e-6)
            w_total = w0 + w1
            mediant = (w0 * pos[i0] + w1 * pos[i1]) / w_total

            # Check local error at mediant position
            py = int(np.clip(mediant[0] * H, 0, H - 1))
            px = int(np.clip(mediant[1] * W, 0, W - 1))
            r = 4  # error neighborhood radius
            patch = error_map[max(0, py-r):min(H, py+r+1), max(0, px-r):min(W, px+r+1)]
            local_err = patch.mean().item()

            # Interpolate properties for new Gaussian
            new_log_scale = (
                model.log_scales.data[i0] + model.log_scales.data[i1]
            ).cpu().numpy() / 2.0 - np.log(1.3)  # slightly smaller
            new_rotation = (
                model.rotations.data[i0] + model.rotations.data[i1]
            ).item() / 2.0
            new_color = (
                model.color_logits.data[i0] + model.color_logits.data[i1]
            ).cpu().numpy() / 2.0

            candidates.append({
                'error': local_err,
                'position': mediant,
                'log_scale': new_log_scale,
                'rotation': new_rotation,
                'color_logits': new_color,
            })

    if not candidates:
        return

    # Sort by error (highest first), deduplicate nearby positions
    candidates.sort(key=lambda x: -x['error'])

    # Deduplicate: skip candidates too close to already-selected ones
    selected = []
    min_dist = 0.02  # minimum distance between new Gaussians
    for c in candidates:
        too_close = False
        for s in selected:
            if np.linalg.norm(c['position'] - s['position']) < min_dist:
                too_close = True
                break
        if not too_close:
            selected.append(c)
        if len(selected) >= max_new:
            break

    n_new = min(len(selected), max_gaussians - n)
    if n_new <= 0:
        return

    selected = selected[:n_new]

    new_pos = torch.tensor(
        np.array([c['position'] for c in selected]), dtype=torch.float32
    )
    new_ls = torch.tensor(
        np.array([c['log_scale'] for c in selected]), dtype=torch.float32
    )
    new_rot = torch.tensor(
        [c['rotation'] for c in selected], dtype=torch.float32
    )
    new_col = torch.tensor(
        np.array([c['color_logits'] for c in selected]), dtype=torch.float32
    )
    new_opa = torch.full((n_new,), 1.0)

    model.add_gaussians(new_pos, new_ls, new_rot, new_col, new_opa)


def densify_random(model, target, grad_accum, step, total_steps, max_gaussians, max_new=30):
    """
    Random densification baseline: add Gaussians at random positions
    weighted by error map. Controls for whether structured placement matters.
    """
    n = model.n_gaussians
    if n >= max_gaussians:
        return

    H, W = model.H, model.W

    with torch.no_grad():
        rendered = model.render()
        error_map = (rendered - target).pow(2).sum(dim=-1)  # [H, W]

    n_new = min(max_new, max_gaussians - n)
    if n_new <= 0:
        return

    # Sample positions weighted by error
    flat_err = error_map.flatten()
    probs = flat_err / (flat_err.sum() + 1e-8)
    indices = torch.multinomial(probs.cpu(), n_new, replacement=True)
    rows = indices // W
    cols = indices % W

    new_pos = torch.stack([
        rows.float() / H,
        cols.float() / W
    ], dim=1)

    model.add_gaussians(new_pos)


def densify_uniform(model, target, grad_accum, step, total_steps, max_gaussians, max_new=30):
    """
    Uniform grid refinement baseline: subdivide the grid uniformly.
    No error guidance at all.
    """
    n = model.n_gaussians
    if n >= max_gaussians:
        return

    n_new = min(max_new, max_gaussians - n)
    if n_new <= 0:
        return

    new_pos = torch.rand(n_new, 2)  # uniform random positions
    model.add_gaussians(new_pos)


def densify_error_guided(model, target, grad_accum, step, total_steps, max_gaussians, max_new=30):
    """
    Error-guided densification: place new Gaussians at highest-error regions.
    Like Farey but without the mediant structure -- just error peaks.
    This ablation tests whether Farey structure matters beyond error guidance.
    """
    n = model.n_gaussians
    if n >= max_gaussians:
        return

    H, W = model.H, model.W

    with torch.no_grad():
        rendered = model.render()
        error_map = (rendered - target).pow(2).sum(dim=-1)  # [H, W]

    n_new = min(max_new, max_gaussians - n)
    if n_new <= 0:
        return

    # Find top-k error peaks with non-maximum suppression
    err_np = error_map.cpu().numpy()
    from scipy.ndimage import maximum_filter
    local_max = maximum_filter(err_np, size=15) == err_np
    peaks = np.argwhere(local_max)
    peak_vals = err_np[local_max]

    # Sort by error value descending
    order = np.argsort(-peak_vals)
    peaks = peaks[order]

    selected = []
    min_dist_px = 10
    for py, px in peaks:
        too_close = False
        for sy, sx in selected:
            if abs(py - sy) + abs(px - sx) < min_dist_px:
                too_close = True
                break
        if not too_close:
            selected.append((py, px))
        if len(selected) >= n_new:
            break

    if not selected:
        return

    new_pos = torch.tensor(
        [[py / H, px / W] for py, px in selected], dtype=torch.float32
    )
    n_actual = min(len(new_pos), n_new)
    model.add_gaussians(new_pos[:n_actual])


# ── Pruning ──────────────────────────────────────────────────────────

def prune_model(model, min_opacity=0.005):
    """Remove Gaussians with very low opacity."""
    opacities = model.get_opacities()
    keep = opacities > min_opacity
    if keep.sum() < 10:  # keep at least 10
        return
    model.prune_gaussians(keep)


# ── Training loop ────────────────────────────────────────────────────

METHODS = {
    'adc': ('ADC (Standard 3DGS)', densify_adc),
    'farey': ('Farey Densification', densify_farey),
    'random': ('Random (Error-weighted)', densify_random),
    'uniform': ('Uniform Random', densify_uniform),
    'error_guided': ('Error-Guided (no structure)', densify_error_guided),
    'none': ('No Densification', None),
}


def train_one(target, method_name, config):
    """
    Train 2D Gaussian splatting on a target image.

    Args:
        target: [H, W, 3] tensor
        method_name: key into METHODS
        config: dict with training hyperparameters

    Returns:
        dict with metrics
    """
    H, W, _ = target.shape
    n_init = config.get('n_init', 64)
    steps = config.get('steps', 3000)
    densify_interval = config.get('densify_interval', 100)
    densify_start = config.get('densify_start', 200)
    densify_end = config.get('densify_end', int(steps * 0.8))
    max_gaussians = config.get('max_gaussians', 2000)
    max_new = config.get('max_new', 20)
    prune_every = config.get('prune_every', 500)
    lr_pos = config.get('lr_pos', 0.005)
    lr_scale = config.get('lr_scale', 0.005)
    lr_color = config.get('lr_color', 0.01)
    lr_opacity = config.get('lr_opacity', 0.01)
    lr_rotation = config.get('lr_rotation', 0.005)
    log_interval = config.get('log_interval', 500)

    method_label, densify_fn = METHODS[method_name]

    model = GaussianModel2D(n_init, H, W).to(DEVICE)

    optimizer = torch.optim.Adam([
        {'params': [model.positions], 'lr': lr_pos},
        {'params': [model.log_scales], 'lr': lr_scale},
        {'params': [model.rotations], 'lr': lr_rotation},
        {'params': [model.color_logits], 'lr': lr_color},
        {'params': [model.opacity_logits], 'lr': lr_opacity},
    ])

    # Gradient accumulation for ADC
    grad_accum = None
    grad_count = 0

    t0 = time.time()
    history = []

    for step in range(steps):
        optimizer.zero_grad()
        rendered = model.render()
        loss = F.mse_loss(rendered, target)

        # Optional: add L1 loss for sharper edges
        l1_loss = F.l1_loss(rendered, target)
        total_loss = 0.8 * loss + 0.2 * l1_loss

        total_loss.backward()

        # Accumulate position gradients for ADC
        if model.positions.grad is not None:
            if grad_accum is None or grad_accum.shape[0] != model.n_gaussians:
                grad_accum = model.positions.grad.data.clone()
                grad_count = 1
            else:
                grad_accum += model.positions.grad.data
                grad_count += 1

        optimizer.step()

        # Clamp positions to valid range
        with torch.no_grad():
            model.positions.data.clamp_(0.0, 1.0)

        # Densify
        if (densify_fn is not None and
            step >= densify_start and
            step < densify_end and
            step % densify_interval == 0):

            with torch.no_grad():
                avg_grad = grad_accum / max(grad_count, 1) if grad_accum is not None else None

                if method_name == 'adc':
                    densify_fn(model, target, avg_grad, step, max_gaussians, max_new)
                elif method_name in ('farey', 'random', 'uniform', 'error_guided'):
                    densify_fn(model, target, avg_grad, step, steps, max_gaussians, max_new)

            # Rebuild optimizer after densification
            optimizer = torch.optim.Adam([
                {'params': [model.positions], 'lr': lr_pos},
                {'params': [model.log_scales], 'lr': lr_scale},
                {'params': [model.rotations], 'lr': lr_rotation},
                {'params': [model.color_logits], 'lr': lr_color},
                {'params': [model.opacity_logits], 'lr': lr_opacity},
            ])
            grad_accum = None
            grad_count = 0

        # Prune
        if step > 0 and step % prune_every == 0:
            with torch.no_grad():
                prune_model(model)
            optimizer = torch.optim.Adam([
                {'params': [model.positions], 'lr': lr_pos},
                {'params': [model.log_scales], 'lr': lr_scale},
                {'params': [model.rotations], 'lr': lr_rotation},
                {'params': [model.color_logits], 'lr': lr_color},
                {'params': [model.opacity_logits], 'lr': lr_opacity},
            ])
            grad_accum = None
            grad_count = 0

        # Logging
        if step % log_interval == 0 or step == steps - 1:
            with torch.no_grad():
                psnr = compute_psnr(rendered, target)
                elapsed = time.time() - t0
                n_g = model.n_gaussians
                history.append({
                    'step': step, 'psnr': psnr, 'n_gaussians': n_g, 'time': elapsed
                })
                print(f"    [{method_label}] Step {step:5d}: "
                      f"PSNR={psnr:.2f}dB  G={n_g}  "
                      f"loss={loss.item():.6f}  t={elapsed:.0f}s",
                      flush=True)

    # Final evaluation
    with torch.no_grad():
        final_rendered = model.render()
        final_psnr = compute_psnr(final_rendered, target)
        final_ssim = compute_ssim(final_rendered, target)
        elapsed = time.time() - t0

    result = {
        'method': method_name,
        'method_label': method_label,
        'psnr': final_psnr,
        'ssim': final_ssim,
        'n_gaussians': model.n_gaussians,
        'time': elapsed,
        'steps': steps,
        'history': history,
    }

    print(f"    [{method_label}] FINAL: PSNR={final_psnr:.2f}dB  "
          f"SSIM={final_ssim:.4f}  G={model.n_gaussians}  time={elapsed:.0f}s\n",
          flush=True)

    return result


# ── Benchmark Modes ──────────────────────────────────────────────────

def run_quick_test():
    """Quick sanity check: 1 image, 1 seed, low resolution."""
    images = list_kodak_images()
    target = load_image(images[0], max_size=256)
    H, W, _ = target.shape
    print(f"\nQuick test: {images[0].name} ({W}x{H})")

    config = {
        'n_init': 36,
        'steps': 1000,
        'densify_interval': 50,
        'densify_start': 100,
        'densify_end': 800,
        'max_gaussians': 500,
        'max_new': 15,
        'prune_every': 300,
        'log_interval': 200,
    }

    results = {}
    for method in ['adc', 'farey', 'error_guided']:
        print(f"\n--- {method} ---")
        results[method] = train_one(target, method, config)

    # Summary
    print("\n" + "=" * 60)
    print("QUICK TEST SUMMARY")
    print("=" * 60)
    print(f"{'Method':<25} {'PSNR':>8} {'SSIM':>8} {'#Gauss':>8} {'Time':>8}")
    print("-" * 60)
    for method, r in results.items():
        print(f"{r['method_label']:<25} {r['psnr']:>8.2f} {r['ssim']:>8.4f} "
              f"{r['n_gaussians']:>8d} {r['time']:>7.0f}s")

    out_path = RESULTS_DIR / "real_quick_test.json"
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {out_path}")
    return results


def run_full_benchmark(n_images=24, n_seeds=5, methods=None, max_size=384):
    """
    Full benchmark on Kodak dataset.

    Args:
        n_images: number of Kodak images to use (1-24)
        n_seeds: number of random seeds
        methods: list of method names (default: all)
        max_size: max image dimension (384 for speed, None for full 768x512)
    """
    if methods is None:
        methods = ['adc', 'farey', 'error_guided', 'random', 'uniform', 'none']

    images = list_kodak_images()[:n_images]

    config = {
        'n_init': 64,
        'steps': 5000,
        'densify_interval': 100,
        'densify_start': 200,
        'densify_end': 4000,
        'max_gaussians': 2000,
        'max_new': 25,
        'prune_every': 500,
        'log_interval': 1000,
    }

    all_results = []

    for img_idx, img_path in enumerate(images):
        target = load_image(img_path, max_size=max_size)
        H, W, _ = target.shape
        print(f"\n{'='*70}")
        print(f"Image {img_idx+1}/{len(images)}: {img_path.name} ({W}x{H})")
        print(f"{'='*70}")

        for seed in range(n_seeds):
            torch.manual_seed(seed * 1000 + img_idx)
            np.random.seed(seed * 1000 + img_idx)

            print(f"\n  Seed {seed+1}/{n_seeds}")

            for method in methods:
                result = train_one(target, method, config)
                result['image'] = img_path.name
                result['seed'] = seed
                all_results.append(result)

                # Save incrementally
                out_path = RESULTS_DIR / "real_benchmark_results.json"
                with open(out_path, 'w') as f:
                    json.dump(all_results, f, indent=2, default=str)

    # Compute aggregated statistics
    summary = compute_summary(all_results)

    out_path = RESULTS_DIR / "real_benchmark_results.json"
    final = {'config': config, 'results': all_results, 'summary': summary}
    with open(out_path, 'w') as f:
        json.dump(final, f, indent=2, default=str)

    print_summary(summary)
    print(f"\nFull results saved to {out_path}")
    return final


def run_budget_matched(n_images=24, n_seeds=5, budgets=None, max_size=384):
    """
    Budget-matched comparison: all methods constrained to same Gaussian count.

    This is the fairest comparison: same budget, different allocation strategy.
    """
    if budgets is None:
        budgets = [100, 274, 500, 1000]  # 274 = Farey natural count

    methods = ['adc', 'farey', 'error_guided', 'random', 'none']
    images = list_kodak_images()[:n_images]

    all_results = []

    for budget in budgets:
        config = {
            'n_init': min(budget // 2, 64),
            'steps': 5000,
            'densify_interval': 100,
            'densify_start': 200,
            'densify_end': 4000,
            'max_gaussians': budget,
            'max_new': max(5, budget // 20),
            'prune_every': 500,
            'log_interval': 1000,
        }

        print(f"\n{'#'*70}")
        print(f"BUDGET: {budget} Gaussians")
        print(f"{'#'*70}")

        for img_idx, img_path in enumerate(images):
            target = load_image(img_path, max_size=max_size)
            H, W, _ = target.shape
            print(f"\n  Image {img_idx+1}/{len(images)}: {img_path.name}")

            for seed in range(n_seeds):
                torch.manual_seed(seed * 1000 + img_idx)
                np.random.seed(seed * 1000 + img_idx)

                for method in methods:
                    result = train_one(target, method, config)
                    result['image'] = img_path.name
                    result['seed'] = seed
                    result['budget'] = budget
                    all_results.append(result)

                    # Save incrementally
                    out_path = RESULTS_DIR / "real_budget_matched_results.json"
                    with open(out_path, 'w') as f:
                        json.dump(all_results, f, indent=2, default=str)

    out_path = RESULTS_DIR / "real_budget_matched_results.json"
    with open(out_path, 'w') as f:
        json.dump({'results': all_results}, f, indent=2, default=str)

    print(f"\nBudget-matched results saved to {out_path}")
    return all_results


# ── Analysis / Summary ───────────────────────────────────────────────

def compute_summary(results):
    """Compute per-method aggregate statistics."""
    from collections import defaultdict

    by_method = defaultdict(lambda: {'psnr': [], 'ssim': [], 'n_gaussians': [], 'time': []})

    for r in results:
        m = r['method']
        by_method[m]['psnr'].append(r['psnr'])
        by_method[m]['ssim'].append(r['ssim'])
        by_method[m]['n_gaussians'].append(r['n_gaussians'])
        by_method[m]['time'].append(r['time'])

    summary = {}
    for method, vals in by_method.items():
        summary[method] = {
            'psnr_mean': np.mean(vals['psnr']),
            'psnr_std': np.std(vals['psnr']),
            'ssim_mean': np.mean(vals['ssim']),
            'ssim_std': np.std(vals['ssim']),
            'n_gaussians_mean': np.mean(vals['n_gaussians']),
            'time_mean': np.mean(vals['time']),
            'n_runs': len(vals['psnr']),
        }

    return summary


def print_summary(summary):
    """Print formatted summary table."""
    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)
    print(f"{'Method':<25} {'PSNR':>10} {'SSIM':>10} {'#Gauss':>10} {'Time':>10} {'N':>5}")
    print("-" * 80)

    # Sort by PSNR descending
    sorted_methods = sorted(summary.items(), key=lambda x: -x[1]['psnr_mean'])

    for method, s in sorted_methods:
        label = METHODS.get(method, (method,))[0]
        print(f"{label:<25} "
              f"{s['psnr_mean']:>7.2f}+/-{s['psnr_std']:<5.2f}"
              f"{s['ssim_mean']:>7.4f}+/-{s['ssim_std']:<6.4f}"
              f"{s['n_gaussians_mean']:>8.0f}  "
              f"{s['time_mean']:>7.0f}s "
              f"{s['n_runs']:>5d}")

    # Compute deltas vs ADC
    if 'adc' in summary and 'farey' in summary:
        delta_psnr = summary['farey']['psnr_mean'] - summary['adc']['psnr_mean']
        delta_ssim = summary['farey']['ssim_mean'] - summary['adc']['ssim_mean']
        print(f"\nFarey vs ADC: {delta_psnr:+.2f} dB PSNR, {delta_ssim:+.4f} SSIM")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="2D Gaussian Splatting Real Image Benchmark")
    parser.add_argument('--mode', choices=['quick', 'full', 'budget', 'custom'],
                        default='quick', help='Benchmark mode')
    parser.add_argument('--n-images', type=int, default=24, help='Number of Kodak images')
    parser.add_argument('--n-seeds', type=int, default=5, help='Number of random seeds')
    parser.add_argument('--max-size', type=int, default=384, help='Max image dimension')
    parser.add_argument('--methods', nargs='+', default=None,
                        help='Methods to compare (adc farey random uniform error_guided none)')

    args = parser.parse_args()

    if args.mode == 'quick':
        run_quick_test()
    elif args.mode == 'full':
        run_full_benchmark(
            n_images=args.n_images,
            n_seeds=args.n_seeds,
            methods=args.methods,
            max_size=args.max_size,
        )
    elif args.mode == 'budget':
        run_budget_matched(
            n_images=args.n_images,
            n_seeds=args.n_seeds,
            max_size=args.max_size,
        )
    elif args.mode == 'custom':
        # For interactive use
        print("Custom mode: import and call functions directly")
        print("  from 3dgs_real_benchmark import *")
        print("  results = run_quick_test()")


if __name__ == '__main__':
    main()
