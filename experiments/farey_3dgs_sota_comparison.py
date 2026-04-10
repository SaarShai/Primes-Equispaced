#!/usr/bin/env python3
# Run with: PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 python3 farey_3dgs_sota_comparison.py
# This allows MPS to use all available GPU memory instead of the default 70% cap.
"""
SOTA Densification Comparison for 3D Gaussian Splatting
========================================================
Compares Farey-guided densification against:
1. Standard ADC (baseline)
2. 3DGS-MCMC (NeurIPS 2024 Spotlight) — SGLD + relocalization
3. Revising Densification (ECCV 2024) — pixel-error driven + opacity correction
4. SteepGS (CVPR 2025) — steepest descent saddle-point escape
5. Mini-Splatting (ECCV 2024) — importance sampling + blur split + aggressive pruning
6. AbsGS (ACM MM 2024) — absolute gradient-based densification (homodirectional gradient)
7. Pixel-GS (ECCV 2024) — pixel-aware gradient weighting for densification

All methods use the same:
- Target: 50 multi-scale bumps (8 coarse + 18 medium + 24 fine)
- Budget: MAX_GAUSS=1500
- Steps: 7000
- Init: 4^3=64 Gaussians
- Evaluation: 20K test points

Output: ~/Desktop/Farey-Local/experiments/3dgs_results/sota_comparison.json
"""

import torch
import numpy as np
from scipy.spatial import Delaunay
import time
import json
import os
import sys

# ── Device setup ──────────────────────────────────────────────────────
if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
    print(f"Using MPS (Apple Metal GPU)")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print(f"Using CUDA GPU")
else:
    DEVICE = torch.device("cpu")
    print(f"Using CPU (no GPU acceleration)")

# ── Configuration ─────────────────────────────────────────────────────
MAX_GAUSS = 1500
INIT_K = 4             # 4^3 = 64 initial Gaussians
TOTAL_STEPS = 7000
DENSIFY_EVERY = 80
LR = 0.006
N_SAMPLE = 50000
N_TEST = 20000

OUT = os.path.expanduser("~/Desktop/Farey-Local/experiments/3dgs_results")
os.makedirs(OUT, exist_ok=True)

torch.manual_seed(42)
np.random.seed(42)

# ── Target density field (multi-scale, complex) ──────────────────────
def make_bump_centers():
    """Generate 50 bumps at multiple scales."""
    rng = np.random.RandomState(123)
    bumps = []
    for _ in range(8):
        c = rng.uniform(-0.8, 0.8, 3)
        scale = rng.uniform(4.0, 8.0)
        amp = rng.uniform(0.3, 0.8)
        bumps.append((c, scale, amp))
    for _ in range(18):
        c = rng.uniform(0.0, 1.0, 3)
        c[1] = rng.uniform(-0.7, 0.7)
        c[2] = rng.uniform(-0.7, 0.7)
        scale = rng.uniform(15.0, 35.0)
        amp = rng.uniform(0.4, 1.0)
        bumps.append((c, scale, amp))
    for _ in range(24):
        c = rng.uniform(0.4, 0.9, 3)
        c[1] = rng.uniform(-0.3, 0.3)
        c[2] = rng.uniform(-0.3, 0.3)
        scale = rng.uniform(40.0, 80.0)
        amp = rng.uniform(0.3, 0.7)
        bumps.append((c, scale, amp))
    return bumps

BUMPS = make_bump_centers()
BUMP_CENTERS_T = torch.tensor(np.array([b[0] for b in BUMPS]), device=DEVICE, dtype=torch.float32)
BUMP_SCALES_T = torch.tensor(np.array([b[1] for b in BUMPS]), device=DEVICE, dtype=torch.float32)
BUMP_AMPS_T = torch.tensor(np.array([b[2] for b in BUMPS]), device=DEVICE, dtype=torch.float32)


def compute_target_density(pts):
    """Complex multi-scale density field."""
    r = torch.norm(pts, dim=1)
    density = 0.5 * torch.exp(-1.5 * r ** 2)
    for i in range(len(BUMPS)):
        d = torch.norm(pts - BUMP_CENTERS_T[i].unsqueeze(0), dim=1)
        density = density + BUMP_AMPS_T[i] * torch.exp(-BUMP_SCALES_T[i] * d ** 2)
    return density


# Pre-generate training samples
print("Generating sample points ...")
sample_pts = torch.rand(N_SAMPLE, 3, device=DEVICE) * 3.0 - 1.5
target_density = compute_target_density(sample_pts)
print(f"  Target density range: [{target_density.min().item():.3f}, {target_density.max().item():.3f}]")
print(f"  Target density mean: {target_density.mean().item():.4f}")


# ── Batched density evaluation ────────────────────────────────────────
def eval_density_batched(pts, mu, log_sigma, w, batch_size=10000):
    N = pts.shape[0]
    K = mu.shape[0]
    sigma = torch.exp(log_sigma)

    if N * K < 100_000_000:
        diff = pts.unsqueeze(1) - mu.unsqueeze(0)
        sq_dist = (diff ** 2).sum(dim=2)
        exponent = -sq_dist / (2.0 * sigma.unsqueeze(0) ** 2)
        gauss = torch.exp(exponent)
        pred = (gauss * w.unsqueeze(0)).sum(dim=1)
        return pred, gauss, diff, sigma, sq_dist

    pred = torch.zeros(N, device=pts.device)
    all_gauss = torch.zeros(N, K, device=pts.device)
    all_diff = torch.zeros(N, K, 3, device=pts.device)

    for start in range(0, N, batch_size):
        end = min(start + batch_size, N)
        pts_b = pts[start:end]
        diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)
        sq_dist_b = (diff_b ** 2).sum(dim=2)
        exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
        gauss_b = torch.exp(exponent_b)
        pred[start:end] = (gauss_b * w.unsqueeze(0)).sum(dim=1)
        all_gauss[start:end] = gauss_b
        all_diff[start:end] = diff_b

    sq_dist_full = (all_diff ** 2).sum(dim=2)
    return pred, all_gauss, all_diff, sigma, sq_dist_full


def eval_density_pred_only(pts, mu, log_sigma, w, batch_size=5000):
    """Lightweight prediction: returns only pred (N,), no intermediate tensors."""
    N = pts.shape[0]
    K = mu.shape[0]
    sigma = torch.exp(log_sigma)
    pred = torch.zeros(N, device=pts.device)

    for start in range(0, N, batch_size):
        end = min(start + batch_size, N)
        pts_b = pts[start:end]
        diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)  # (B, K, 3)
        sq_dist_b = (diff_b ** 2).sum(dim=2)  # (B, K)
        exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
        gauss_b = torch.exp(exponent_b)  # (B, K)
        pred[start:end] = (gauss_b * w.unsqueeze(0)).sum(dim=1)
        del diff_b, sq_dist_b, exponent_b, gauss_b

    return pred


def compute_loss_and_grads(pts, target, mu, log_sigma, w, batch_size=0):
    """MSE loss and analytical gradients.
    If batch_size > 0, compute in sub-batches to reduce peak memory (for MCMC/large K).
    """
    N = pts.shape[0]
    K = mu.shape[0]
    sigma = torch.exp(log_sigma)

    if batch_size > 0 and N * K > 50_000_000:
        # Memory-efficient batched computation
        grad_mu = torch.zeros_like(mu)
        grad_ls = torch.zeros(K, device=mu.device)
        grad_w = torch.zeros(K, device=mu.device)
        total_sq_err = 0.0

        for start in range(0, N, batch_size):
            end = min(start + batch_size, N)
            pts_b = pts[start:end]
            target_b = target[start:end]
            B = end - start

            diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)  # (B, K, 3)
            sq_dist_b = (diff_b ** 2).sum(dim=2)  # (B, K)
            exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
            gauss_b = torch.exp(exponent_b)  # (B, K)
            pred_b = (gauss_b * w.unsqueeze(0)).sum(dim=1)  # (B,)
            residual_b = pred_b - target_b
            total_sq_err += (residual_b ** 2).sum().item()

            common_b = (2.0 / N) * residual_b.unsqueeze(1) * gauss_b  # (B, K)
            grad_w += common_b.sum(dim=0)
            weighted_b = common_b * w.unsqueeze(0)
            for d in range(3):
                grad_mu[:, d] += (weighted_b * diff_b[:, :, d] / (sigma.unsqueeze(0) ** 2)).sum(dim=0)
            grad_ls += (weighted_b * sq_dist_b / (sigma.unsqueeze(0) ** 2)).sum(dim=0)

            del diff_b, sq_dist_b, exponent_b, gauss_b, pred_b, residual_b, common_b, weighted_b

        mse = total_sq_err / N
        return mse, grad_mu, grad_ls, grad_w

    # Original non-batched path
    pred, gauss, diff, sigma_val, sq_dist = eval_density_batched(pts, mu, log_sigma, w)
    residual = pred - target
    mse = (residual ** 2).mean()

    common = (2.0 / N) * residual.unsqueeze(1) * gauss

    grad_w = common.sum(dim=0)

    weighted_common = common * w.unsqueeze(0)
    grad_mu = torch.zeros_like(mu)
    for d in range(3):
        grad_mu[:, d] = (weighted_common * diff[:, :, d] / (sigma_val.unsqueeze(0) ** 2)).sum(dim=0)

    grad_log_sigma = (weighted_common * sq_dist / (sigma_val.unsqueeze(0) ** 2)).sum(dim=0)

    return mse.item(), grad_mu, grad_log_sigma, grad_w


# ── Adam optimizer ────────────────────────────────────────────────────
class AdamGPU:
    def __init__(self, K, lr=LR):
        self.lr = lr
        self.beta1, self.beta2, self.eps = 0.9, 0.999, 1e-8
        self.t = 0
        self.m_mu = torch.zeros(K, 3, device=DEVICE)
        self.v_mu = torch.zeros(K, 3, device=DEVICE)
        self.m_ls = torch.zeros(K, device=DEVICE)
        self.v_ls = torch.zeros(K, device=DEVICE)
        self.m_w = torch.zeros(K, device=DEVICE)
        self.v_w = torch.zeros(K, device=DEVICE)

    def step(self, mu, log_sigma, w, grad_mu, grad_log_sigma, grad_w):
        self.t += 1
        bc1 = 1 - self.beta1 ** self.t
        bc2 = 1 - self.beta2 ** self.t

        self.m_mu = self.beta1 * self.m_mu + (1 - self.beta1) * grad_mu
        self.v_mu = self.beta2 * self.v_mu + (1 - self.beta2) * grad_mu ** 2
        mu_new = mu - self.lr * (self.m_mu / bc1) / (torch.sqrt(self.v_mu / bc2) + self.eps)

        self.m_ls = self.beta1 * self.m_ls + (1 - self.beta1) * grad_log_sigma
        self.v_ls = self.beta2 * self.v_ls + (1 - self.beta2) * grad_log_sigma ** 2
        ls_new = log_sigma - self.lr * (self.m_ls / bc1) / (torch.sqrt(self.v_ls / bc2) + self.eps)

        self.m_w = self.beta1 * self.m_w + (1 - self.beta1) * grad_w
        self.v_w = self.beta2 * self.v_w + (1 - self.beta2) * grad_w ** 2
        w_new = w - self.lr * (self.m_w / bc1) / (torch.sqrt(self.v_w / bc2) + self.eps)

        return mu_new, ls_new, w_new

    def extend(self, n_new):
        self.m_mu = torch.cat([self.m_mu, torch.zeros(n_new, 3, device=DEVICE)])
        self.v_mu = torch.cat([self.v_mu, torch.zeros(n_new, 3, device=DEVICE)])
        self.m_ls = torch.cat([self.m_ls, torch.zeros(n_new, device=DEVICE)])
        self.v_ls = torch.cat([self.v_ls, torch.zeros(n_new, device=DEVICE)])
        self.m_w = torch.cat([self.m_w, torch.zeros(n_new, device=DEVICE)])
        self.v_w = torch.cat([self.v_w, torch.zeros(n_new, device=DEVICE)])

    def replace_at(self, idx, n_new):
        """For MCMC relocalization: zero out momentum at relocated indices."""
        self.m_mu[idx] = 0.0
        self.v_mu[idx] = 0.0
        self.m_ls[idx] = 0.0
        self.v_ls[idx] = 0.0
        self.m_w[idx] = 0.0
        self.v_w[idx] = 0.0


# ── Initialization ────────────────────────────────────────────────────
def init_gaussians_3d(K=INIT_K):
    g = torch.linspace(-0.8, 0.8, K, device=DEVICE)
    GX, GY, GZ = torch.meshgrid(g, g, g, indexing='ij')
    mu = torch.stack([GX.reshape(-1), GY.reshape(-1), GZ.reshape(-1)], dim=1)
    n = mu.shape[0]
    log_sigma = torch.full((n,), float(np.log(0.4)), device=DEVICE)
    w = torch.full((n,), 0.3, device=DEVICE)
    return mu, log_sigma, w


# ── Delaunay helpers ──────────────────────────────────────────────────
def extract_delaunay_edges(simplices):
    edges = set()
    for simplex in simplices:
        n = len(simplex)
        for i in range(n):
            for j in range(i + 1, n):
                edges.add((min(simplex[i], simplex[j]),
                           max(simplex[i], simplex[j])))
    return edges


# ═══════════════════════════════════════════════════════════════════════
#  METHOD 1: Standard ADC (baseline)
# ═══════════════════════════════════════════════════════════════════════
def train_standard_adc():
    print("\n  [1/8] Training Standard ADC ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []
    grad_thresh = 0.00002

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)
        mse_hist.append(mse)
        cnt_hist.append(mu.shape[0])

        if step % 500 == 0:
            elapsed = time.time() - t0
            print(f"    step {step:5d}  MSE={mse:.6f}  K={mu.shape[0]:5d}  t={elapsed:.1f}s")
            sys.stdout.flush()

        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 1000 and mu.shape[0] < MAX_GAUSS:
            grad_mag = torch.norm(grad_mu, dim=1)
            split_mask = grad_mag > grad_thresh
            split_idx = torch.where(split_mask)[0]
            if len(split_idx) > 0:
                budget = (MAX_GAUSS - mu.shape[0]) // 2
                sorted_idx = split_idx[torch.argsort(-grad_mag[split_idx])]
                sorted_idx = sorted_idx[:max(budget, 0)]
                if len(sorted_idx) > 0:
                    sigma = torch.exp(log_sigma)
                    directions = grad_mu[sorted_idx]
                    dir_norms = torch.norm(directions, dim=1, keepdim=True).clamp(min=1e-8)
                    directions = directions / dir_norms
                    offsets = directions * sigma[sorted_idx].unsqueeze(1) * 0.5
                    new_mu = torch.cat([mu[sorted_idx] - offsets, mu[sorted_idx] + offsets])
                    shrink = float(np.log(0.7))
                    new_ls = torch.cat([log_sigma[sorted_idx] + shrink] * 2)
                    new_w = torch.cat([w[sorted_idx] * 0.5] * 2)
                    n_new = new_mu.shape[0]
                    mu = torch.cat([mu, new_mu])
                    log_sigma = torch.cat([log_sigma, new_ls])
                    w = torch.cat([w, new_w])
                    opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  ADC done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ═══════════════════════════════════════════════════════════════════════
#  METHOD 2: Farey-guided densification
# ═══════════════════════════════════════════════════════════════════════
def train_farey():
    print("\n  [2/8] Training Farey-guided ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []
    farey_level = 2
    error_thresh = 0.0003
    max_per_round = 30

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)
        mse_hist.append(mse)
        cnt_hist.append(mu.shape[0])

        if step % 500 == 0:
            elapsed = time.time() - t0
            print(f"    step {step:5d}  MSE={mse:.6f}  K={mu.shape[0]:5d}  t={elapsed:.1f}s")
            sys.stdout.flush()

        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 1000 and mu.shape[0] < MAX_GAUSS:
            farey_level += 1
            sigma = torch.exp(log_sigma)
            with torch.no_grad():
                pred = eval_density_pred_only(sample_pts, mu, log_sigma, w)
            budget = MAX_GAUSS - mu.shape[0]
            candidates = []

            mu_np = mu.detach().cpu().numpy()
            sigma_np = sigma.detach().cpu().numpy()
            pred_np = pred.detach().cpu().numpy()
            target_np = target_density.detach().cpu().numpy()
            pts_np = sample_pts.detach().cpu().numpy()
            w_np = w.detach().cpu().numpy()

            if len(mu_np) >= 5:
                try:
                    tri = Delaunay(mu_np)
                    edges = extract_delaunay_edges(tri.simplices)
                    for (i, j) in edges:
                        ri, rj = sigma_np[i], sigma_np[j]
                        dist = np.linalg.norm(mu_np[i] - mu_np[j])
                        d_edge = dist / (ri + rj + 1e-8)
                        if d_edge <= 1.0 or d_edge > farey_level:
                            continue
                        t_w = ri / (ri + rj + 1e-8)
                        p_new = mu_np[i] + t_w * (mu_np[j] - mu_np[i])
                        dists = np.linalg.norm(pts_np - p_new, axis=1)
                        mask = dists < 0.2
                        if mask.sum() < 5:
                            continue
                        local_err = np.mean((target_np[mask] - pred_np[mask]) ** 2)
                        if local_err < error_thresh:
                            continue
                        s_new = 0.35 * (sigma_np[i] + sigma_np[j])
                        w_new_val = 0.5 * (w_np[i] + w_np[j])
                        candidates.append((local_err, p_new, np.log(s_new), w_new_val))
                except Exception:
                    pass

            if candidates:
                candidates.sort(key=lambda c: -c[0])
                selected = candidates[:min(budget, max_per_round)]
                add_mu = torch.tensor(np.array([c[1] for c in selected]), dtype=torch.float32, device=DEVICE)
                add_ls = torch.tensor(np.array([c[2] for c in selected]), dtype=torch.float32, device=DEVICE)
                add_w = torch.tensor(np.array([c[3] for c in selected]), dtype=torch.float32, device=DEVICE)
                n_new = len(selected)
                mu = torch.cat([mu, add_mu])
                log_sigma = torch.cat([log_sigma, add_ls])
                w = torch.cat([w, add_w])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  Farey done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ═══════════════════════════════════════════════════════════════════════
#  METHOD 3: 3DGS-MCMC (NeurIPS 2024)
#  Core idea: Stochastic Gradient Langevin Dynamics (SGLD) updates
#  + relocalization of dead Gaussians instead of clone/split
# ═══════════════════════════════════════════════════════════════════════
def train_mcmc():
    print("\n  [3/8] Training 3DGS-MCMC ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []

    # MCMC hyperparameters (adapted from paper, tuned for our scale)
    noise_lr = 0.5          # noise learning rate (paper uses 5e5 but at much smaller LR)
    opacity_reg = 0.001     # L1 regularizer on weights
    scale_reg = 0.001       # L1 regularizer on scales
    relocate_every = 100    # how often to relocalize dead Gaussians
    dead_thresh = 0.005     # weight threshold for "dead" Gaussians
    add_every = 200         # how often to add new Gaussians to fill budget
    max_add_per_round = 25

    # Use smaller sub-batches for MCMC to avoid MPS OOM
    mcmc_batch_size = 8000

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w, batch_size=mcmc_batch_size)

        # Add L1 regularization gradients
        grad_w = grad_w + opacity_reg * torch.sign(w)
        grad_ls = grad_ls + scale_reg * torch.sign(log_sigma)

        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)
        del grad_mu, grad_ls, grad_w

        # SGLD noise injection on positions only (key MCMC ingredient)
        # Noise scale inversely proportional to weight (well-placed Gaussians get less noise)
        if step < TOTAL_STEPS - 1500:
            # Anneal noise: start at noise_lr, decay linearly to 0.1*noise_lr
            progress = step / (TOTAL_STEPS - 1500)
            current_noise = noise_lr * (1.0 - 0.9 * progress)
            noise_scale = current_noise * LR  # scale with lr
            w_abs = torch.abs(w).clamp(min=1e-6)
            # Lower weight = more noise (encourages exploration of underfitted regions)
            noise_weight = (1.0 / w_abs).clamp(max=10.0)
            noise_weight = noise_weight / noise_weight.max()
            sqrt_val = float(np.sqrt(max(2 * noise_scale, 1e-10)))
            noise = torch.randn_like(mu) * sqrt_val * noise_weight.unsqueeze(1)
            mu = mu + noise
            del noise, noise_weight, w_abs

        mse_hist.append(mse)
        cnt_hist.append(mu.shape[0])

        if step % 500 == 0:
            elapsed = time.time() - t0
            print(f"    step {step:5d}  MSE={mse:.6f}  K={mu.shape[0]:5d}  t={elapsed:.1f}s")
            sys.stdout.flush()

        # Relocalization: move dead Gaussians to high-error regions
        if step % relocate_every == 0 and step < TOTAL_STEPS - 1000:
            w_abs = torch.abs(w)
            dead_mask = w_abs < dead_thresh
            dead_idx = torch.where(dead_mask)[0]

            if len(dead_idx) > 0:
                # Find high-error regions using lightweight prediction
                with torch.no_grad():
                    pred = eval_density_pred_only(sample_pts, mu, log_sigma, w)
                    sq_err = (pred - target_density) ** 2
                    del pred

                # Sample new positions proportional to error
                err_probs = sq_err / sq_err.sum()
                n_relocate = min(len(dead_idx), 50)
                reloc_sample_idx = torch.multinomial(err_probs, n_relocate, replacement=True)
                del sq_err, err_probs

                # Move dead Gaussians to high-error sample points + small noise
                mu[dead_idx[:n_relocate]] = sample_pts[reloc_sample_idx] + \
                    torch.randn(n_relocate, 3, device=DEVICE) * 0.05
                log_sigma[dead_idx[:n_relocate]] = float(np.log(0.2))
                w[dead_idx[:n_relocate]] = 0.1
                opt.replace_at(dead_idx[:n_relocate], n_relocate)

        # Budget filling: add new Gaussians if under budget
        if step % add_every == 0 and step < TOTAL_STEPS - 1500 and mu.shape[0] < MAX_GAUSS:
            budget_remaining = MAX_GAUSS - mu.shape[0]
            n_add = min(budget_remaining, max_add_per_round)
            if n_add > 0:
                with torch.no_grad():
                    pred = eval_density_pred_only(sample_pts, mu, log_sigma, w)
                    sq_err = (pred - target_density) ** 2
                    del pred

                err_probs = sq_err / sq_err.sum()
                add_sample_idx = torch.multinomial(err_probs, n_add, replacement=True)
                del sq_err, err_probs

                new_mu = sample_pts[add_sample_idx] + torch.randn(n_add, 3, device=DEVICE) * 0.03
                new_ls = torch.full((n_add,), float(np.log(0.15)), device=DEVICE)
                new_w = torch.full((n_add,), 0.1, device=DEVICE)

                mu = torch.cat([mu, new_mu])
                log_sigma = torch.cat([log_sigma, new_ls])
                w = torch.cat([w, new_w])
                opt.extend(n_add)

    elapsed = time.time() - t0
    print(f"  MCMC done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ═══════════════════════════════════════════════════════════════════════
#  METHOD 4: Revising Densification (ECCV 2024)
#  Core idea: pixel-error driven densification + opacity bias correction
#  Instead of gradient threshold, uses per-Gaussian reconstruction error
#  Also corrects opacity after cloning (halves weight properly)
# ═══════════════════════════════════════════════════════════════════════
def train_revising():
    print("\n  [4/8] Training Revising Densification ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []

    # Revising densification hyperparameters
    error_percentile = 90    # densify Gaussians in top error percentile
    max_per_round = 40
    min_opacity = 0.005      # prune threshold

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)
        mse_hist.append(mse)
        cnt_hist.append(mu.shape[0])

        if step % 500 == 0:
            elapsed = time.time() - t0
            print(f"    step {step:5d}  MSE={mse:.6f}  K={mu.shape[0]:5d}  t={elapsed:.1f}s")
            sys.stdout.flush()

        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 1000 and mu.shape[0] < MAX_GAUSS:
            sigma = torch.exp(log_sigma)
            K = mu.shape[0]

            # KEY DIFFERENCE: pixel-error driven criterion instead of gradient threshold
            # Compute per-Gaussian reconstruction error contribution (batched for memory)
            with torch.no_grad():
                per_gauss_err = torch.zeros(K, device=DEVICE)
                rev_batch = 8000
                for _s in range(0, N_SAMPLE, rev_batch):
                    _e = min(_s + rev_batch, N_SAMPLE)
                    pts_b = sample_pts[_s:_e]
                    target_b = target_density[_s:_e]
                    diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)  # (B, K, 3)
                    sq_dist_b = (diff_b ** 2).sum(dim=2)
                    exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
                    gauss_b = torch.exp(exponent_b)
                    pred_b = (gauss_b * w.unsqueeze(0)).sum(dim=1)
                    residual_b = pred_b - target_b

                    gauss_contrib_b = gauss_b * torch.abs(w).unsqueeze(0)
                    total_contrib_b = gauss_contrib_b.sum(dim=1, keepdim=True).clamp(min=1e-8)
                    resp_b = gauss_contrib_b / total_contrib_b
                    per_gauss_err += (resp_b * (residual_b ** 2).unsqueeze(1)).sum(dim=0)
                    del diff_b, sq_dist_b, exponent_b, gauss_b, pred_b, residual_b, gauss_contrib_b, total_contrib_b, resp_b

            # Densify Gaussians with highest error
            err_threshold = torch.quantile(per_gauss_err, error_percentile / 100.0)
            split_mask = per_gauss_err >= err_threshold
            split_idx = torch.where(split_mask)[0]

            if len(split_idx) > 0:
                budget = (MAX_GAUSS - mu.shape[0]) // 2
                sorted_idx = split_idx[torch.argsort(-per_gauss_err[split_idx])]
                sorted_idx = sorted_idx[:min(budget, max_per_round)]

                if len(sorted_idx) > 0:
                    # Split decision: large sigma -> split, small sigma -> clone
                    median_sigma = sigma.median()
                    is_large = sigma[sorted_idx] > median_sigma

                    new_mus = []
                    new_lss = []
                    new_ws = []

                    for k, idx_val in enumerate(sorted_idx):
                        idx_int = idx_val.item()
                        if is_large[k]:
                            # SPLIT: create two offspring displaced along gradient direction
                            direction = grad_mu[idx_int]
                            dir_norm = torch.norm(direction).clamp(min=1e-8)
                            direction = direction / dir_norm
                            offset = direction * sigma[idx_int] * 0.5

                            new_mus.append(mu[idx_int] - offset)
                            new_mus.append(mu[idx_int] + offset)
                            # Shrink scale for both children
                            shrink = float(np.log(0.7))
                            new_lss.append(log_sigma[idx_int].item() + shrink)
                            new_lss.append(log_sigma[idx_int].item() + shrink)
                            # OPACITY BIAS CORRECTION: properly halve weight
                            # Standard ADC doesn't account for the overlap between children
                            # Correct formula: w_child = w_parent * 0.5 (not w_parent * 0.7)
                            new_ws.append(w[idx_int].item() * 0.5)
                            new_ws.append(w[idx_int].item() * 0.5)
                        else:
                            # CLONE: duplicate at same position with perturbation
                            perturbation = torch.randn(3, device=DEVICE) * sigma[idx_int] * 0.3
                            new_mus.append(mu[idx_int] + perturbation)
                            new_lss.append(log_sigma[idx_int].item())
                            # Opacity correction for clone: halve both original and clone
                            w_half = w[idx_int].item() * 0.5
                            new_ws.append(w_half)
                            w[idx_int] = w_half  # correct parent too

                    if new_mus:
                        add_mu = torch.stack(new_mus).to(DEVICE)
                        add_ls = torch.tensor(new_lss, device=DEVICE, dtype=torch.float32)
                        add_w = torch.tensor(new_ws, device=DEVICE, dtype=torch.float32)

                        n_new = add_mu.shape[0]
                        mu = torch.cat([mu, add_mu])
                        log_sigma = torch.cat([log_sigma, add_ls])
                        w = torch.cat([w, add_w])
                        opt.extend(n_new)

            # Pruning: remove near-zero weight Gaussians (avoids needle-like artifacts)
            if step % (DENSIFY_EVERY * 3) == 0 and mu.shape[0] > INIT_K ** 3:
                keep_mask = torch.abs(w) > min_opacity
                if keep_mask.sum() < mu.shape[0] and keep_mask.sum() >= INIT_K ** 3:
                    mu = mu[keep_mask]
                    log_sigma = log_sigma[keep_mask]
                    w = w[keep_mask]
                    # Rebuild optimizer state
                    opt = AdamGPU(mu.shape[0])

    elapsed = time.time() - t0
    print(f"  Revising done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ═══════════════════════════════════════════════════════════════════════
#  METHOD 5: SteepGS (CVPR 2025)
#  Core idea: identify Gaussians at saddle points, split along
#  steepest descent direction to escape saddle
# ═══════════════════════════════════════════════════════════════════════
def train_steepgs():
    print("\n  [5/8] Training SteepGS ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []

    # SteepGS hyperparameters
    saddle_check_every = DENSIFY_EVERY
    grad_history_len = 5     # track gradient history for saddle detection
    grad_history_mu = []     # list of recent grad_mu tensors
    stagnation_thresh = 0.3  # ratio threshold for saddle detection
    max_per_round = 35

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)
        mse_hist.append(mse)
        cnt_hist.append(mu.shape[0])

        # Track gradient history (only position gradients, padded to current size)
        if step % (saddle_check_every // 2) == 0:
            grad_history_mu.append(grad_mu.clone().detach())
            if len(grad_history_mu) > grad_history_len:
                grad_history_mu.pop(0)

        if step % 500 == 0:
            elapsed = time.time() - t0
            print(f"    step {step:5d}  MSE={mse:.6f}  K={mu.shape[0]:5d}  t={elapsed:.1f}s")
            sys.stdout.flush()

        if step % saddle_check_every == 0 and step < TOTAL_STEPS - 1000 and mu.shape[0] < MAX_GAUSS:
            K = mu.shape[0]
            sigma = torch.exp(log_sigma)

            # SADDLE POINT DETECTION
            # A Gaussian is at a saddle if:
            #   1. It has non-negligible gradient magnitude (not converged)
            #   2. Its gradient direction has been oscillating (not making progress)
            # We approximate this by checking if gradient magnitude is moderate
            # but the position hasn't changed much (stagnation)

            grad_mag = torch.norm(grad_mu, dim=1)
            median_grad = grad_mag.median()

            # Stagnation criterion: gradient is not small but above some threshold
            # AND loss contribution is high (batched for memory)
            with torch.no_grad():
                per_gauss_loss = torch.zeros(K, device=DEVICE)
                sg_batch = 8000
                for _s in range(0, N_SAMPLE, sg_batch):
                    _e = min(_s + sg_batch, N_SAMPLE)
                    pts_b = sample_pts[_s:_e]
                    target_b = target_density[_s:_e]
                    diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)
                    sq_dist_b = (diff_b ** 2).sum(dim=2)
                    exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
                    gauss_b = torch.exp(exponent_b)
                    pred_b = (gauss_b * w.unsqueeze(0)).sum(dim=1)
                    residual_b = pred_b - target_b
                    gauss_w_b = gauss_b * torch.abs(w).unsqueeze(0)
                    per_gauss_loss += (gauss_w_b * (residual_b ** 2).unsqueeze(1)).sum(dim=0)
                    del diff_b, sq_dist_b, exponent_b, gauss_b, pred_b, residual_b, gauss_w_b
                per_gauss_loss = per_gauss_loss / N_SAMPLE

            # Saddle condition: moderate gradient + high loss contribution
            # These are "stuck" Gaussians that can't improve via gradient alone
            grad_not_small = grad_mag > median_grad * 0.3
            high_loss = per_gauss_loss > per_gauss_loss.median()

            # Additional check: if we have gradient history, detect oscillation
            if len(grad_history_mu) >= 3:
                # Compute gradient direction consistency over history
                # Low consistency = oscillating = saddle behavior
                recent_grads = []
                for gh in grad_history_mu[-3:]:
                    # Pad/truncate to current size
                    min_k = min(gh.shape[0], K)
                    recent_grads.append(gh[:min_k])

                min_k = min(g.shape[0] for g in recent_grads)
                if min_k > 0:
                    # Cosine similarity between consecutive gradient directions
                    g1 = recent_grads[-2][:min_k]
                    g2 = recent_grads[-1][:min_k]
                    g1_norm = torch.norm(g1, dim=1, keepdim=True).clamp(min=1e-8)
                    g2_norm = torch.norm(g2, dim=1, keepdim=True).clamp(min=1e-8)
                    cos_sim = (g1 / g1_norm * g2 / g2_norm).sum(dim=1)

                    # Low cosine similarity = direction is unstable = saddle-like
                    oscillating = torch.zeros(K, dtype=torch.bool, device=DEVICE)
                    oscillating[:min_k] = cos_sim < stagnation_thresh
                    saddle_mask = grad_not_small & high_loss & oscillating
                else:
                    saddle_mask = grad_not_small & high_loss
            else:
                saddle_mask = grad_not_small & high_loss

            saddle_idx = torch.where(saddle_mask)[0]

            if len(saddle_idx) > 0:
                budget = (MAX_GAUSS - mu.shape[0]) // 2
                # Prioritize by loss contribution
                sorted_idx = saddle_idx[torch.argsort(-per_gauss_loss[saddle_idx])]
                sorted_idx = sorted_idx[:min(budget, max_per_round)]

                if len(sorted_idx) > 0:
                    # STEEPEST DESCENT SPLITTING
                    # For each saddle Gaussian, compute the steepest descent direction
                    # using a local Hessian approximation

                    new_mus = []
                    new_lss = []
                    new_ws = []

                    for idx_val in sorted_idx:
                        idx_int = idx_val.item()
                        parent_mu = mu[idx_int]
                        parent_sigma = sigma[idx_int]
                        parent_w = w[idx_int]
                        parent_grad = grad_mu[idx_int]

                        # Approximate steepest descent direction from gradient
                        grad_norm = torch.norm(parent_grad).clamp(min=1e-8)
                        descent_dir = -parent_grad / grad_norm  # steepest descent

                        # Compute split offset: along steepest descent direction
                        # The paper uses analytical solution for optimal displacement
                        # We approximate: offset = sigma * direction (escape saddle)
                        offset = descent_dir * parent_sigma * 0.6

                        # Create two children displaced along +/- descent direction
                        new_mus.append(parent_mu + offset)
                        new_mus.append(parent_mu - offset)

                        # Opacity normalization (analytical solution from paper):
                        # w_child = w_parent / 2 (to preserve total contribution)
                        w_half = parent_w.item() * 0.5
                        new_ws.append(w_half)
                        new_ws.append(w_half)

                        # Scale shrink
                        shrink = float(np.log(0.65))  # slightly more aggressive shrink
                        ls_val = log_sigma[idx_int].item() + shrink
                        new_lss.append(ls_val)
                        new_lss.append(ls_val)

                    if new_mus:
                        add_mu = torch.stack(new_mus).to(DEVICE)
                        add_ls = torch.tensor(new_lss, device=DEVICE, dtype=torch.float32)
                        add_w = torch.tensor(new_ws, device=DEVICE, dtype=torch.float32)
                        n_new = add_mu.shape[0]
                        mu = torch.cat([mu, add_mu])
                        log_sigma = torch.cat([log_sigma, add_ls])
                        w = torch.cat([w, add_w])
                        opt.extend(n_new)

                        # Update gradient history size tracking
                        for i in range(len(grad_history_mu)):
                            pad = torch.zeros(n_new, 3, device=DEVICE)
                            grad_history_mu[i] = torch.cat([grad_history_mu[i], pad])

    elapsed = time.time() - t0
    print(f"  SteepGS done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ═══════════════════════════════════════════════════════════════════════
#  METHOD 6: Mini-Splatting (ECCV 2024)
#  Core idea: importance-weighted sampling + blur split + pruning
#  Instead of deterministic pruning, uses stochastic sampling weighted
#  by Gaussian importance (accumulated contribution) to maintain geometry.
#  Blur split targets large Gaussians covering many sample points.
# ═══════════════════════════════════════════════════════════════════════
def train_minisplatting():
    print("\n  [6/8] Training Mini-Splatting ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []

    # Mini-Splatting hyperparameters
    importance_accum = None          # accumulated importance per Gaussian
    blur_split_every = DENSIFY_EVERY
    prune_every = DENSIFY_EVERY * 4  # aggressive pruning schedule
    blur_thresh_frac = 0.15          # fraction of N_SAMPLE for "blurry" Gaussian
    target_prune_ratio = 0.15        # prune bottom 15% by importance
    max_split_per_round = 35
    min_weight = 0.003               # minimum weight to survive pruning

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w, batch_size=8000)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)
        mse_hist.append(mse)
        cnt_hist.append(mu.shape[0])

        if step % 500 == 0:
            elapsed = time.time() - t0
            print(f"    step {step:5d}  MSE={mse:.6f}  K={mu.shape[0]:5d}  t={elapsed:.1f}s")
            sys.stdout.flush()

        # Accumulate importance scores (blending weight contribution)
        # In our 3D setting: importance = sum of |w_k * gauss(x_n, mu_k)| over all samples
        if step % (blur_split_every // 2) == 0 and step < TOTAL_STEPS - 1000:
            K = mu.shape[0]
            sigma = torch.exp(log_sigma)
            if importance_accum is None or importance_accum.shape[0] != K:
                importance_accum = torch.zeros(K, device=DEVICE)

            with torch.no_grad():
                ms_batch = 8000
                contribution = torch.zeros(K, device=DEVICE)
                coverage_count = torch.zeros(K, device=DEVICE)
                for _s in range(0, N_SAMPLE, ms_batch):
                    _e = min(_s + ms_batch, N_SAMPLE)
                    pts_b = sample_pts[_s:_e]
                    diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)
                    sq_dist_b = (diff_b ** 2).sum(dim=2)
                    exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
                    gauss_b = torch.exp(exponent_b)  # (B, K)
                    # Importance: sum of absolute blending weights
                    contribution += (gauss_b * torch.abs(w).unsqueeze(0)).sum(dim=0)
                    # Coverage: count samples where Gaussian has significant contribution
                    coverage_count += (gauss_b > 0.01).float().sum(dim=0)
                    del diff_b, sq_dist_b, exponent_b, gauss_b

                # Exponential moving average of importance
                importance_accum = 0.7 * importance_accum + 0.3 * contribution

        # BLUR SPLIT: split large Gaussians that cover too many samples
        if step % blur_split_every == 0 and step < TOTAL_STEPS - 1000 and mu.shape[0] < MAX_GAUSS:
            K = mu.shape[0]
            sigma = torch.exp(log_sigma)
            blur_threshold = blur_thresh_frac * N_SAMPLE

            with torch.no_grad():
                # Compute coverage count for each Gaussian
                ms_batch = 8000
                cov_count = torch.zeros(K, device=DEVICE)
                for _s in range(0, N_SAMPLE, ms_batch):
                    _e = min(_s + ms_batch, N_SAMPLE)
                    pts_b = sample_pts[_s:_e]
                    diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)
                    sq_dist_b = (diff_b ** 2).sum(dim=2)
                    exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
                    gauss_b = torch.exp(exponent_b)
                    cov_count += (gauss_b > 0.01).float().sum(dim=0)
                    del diff_b, sq_dist_b, exponent_b, gauss_b

            # Blur split criterion: Gaussians covering too many samples
            blur_mask = cov_count > blur_threshold
            blur_idx = torch.where(blur_mask)[0]

            if len(blur_idx) > 0:
                budget = (MAX_GAUSS - mu.shape[0]) // 2
                # Sort by coverage (split most blurry first)
                sorted_idx = blur_idx[torch.argsort(-cov_count[blur_idx])]
                sorted_idx = sorted_idx[:min(budget, max_split_per_round)]

                if len(sorted_idx) > 0:
                    new_mus = []
                    new_lss = []
                    new_ws = []

                    for idx_val in sorted_idx:
                        idx_int = idx_val.item()
                        parent_sigma = sigma[idx_int]
                        # Split along gradient direction (like depth reinitialization)
                        direction = grad_mu[idx_int]
                        dir_norm = torch.norm(direction).clamp(min=1e-8)
                        direction = direction / dir_norm
                        offset = direction * parent_sigma * 0.5

                        new_mus.append(mu[idx_int] - offset)
                        new_mus.append(mu[idx_int] + offset)
                        shrink = float(np.log(0.65))
                        new_lss.append(log_sigma[idx_int].item() + shrink)
                        new_lss.append(log_sigma[idx_int].item() + shrink)
                        new_ws.append(w[idx_int].item() * 0.5)
                        new_ws.append(w[idx_int].item() * 0.5)

                    if new_mus:
                        add_mu = torch.stack(new_mus).to(DEVICE)
                        add_ls = torch.tensor(new_lss, device=DEVICE, dtype=torch.float32)
                        add_w = torch.tensor(new_ws, device=DEVICE, dtype=torch.float32)
                        n_new = add_mu.shape[0]
                        mu = torch.cat([mu, add_mu])
                        log_sigma = torch.cat([log_sigma, add_ls])
                        w = torch.cat([w, add_w])
                        opt.extend(n_new)
                        # Extend importance accumulator
                        if importance_accum is not None:
                            importance_accum = torch.cat([importance_accum, torch.zeros(n_new, device=DEVICE)])

        # IMPORTANCE-WEIGHTED PRUNING: stochastic sampling to maintain geometry
        if step % prune_every == 0 and step < TOTAL_STEPS - 1500 and mu.shape[0] > INIT_K ** 3 + 20:
            K = mu.shape[0]
            # Combine importance with weight magnitude
            if importance_accum is not None and importance_accum.shape[0] == K:
                # Normalize importance to [0, 1]
                imp_max = importance_accum.max().clamp(min=1e-8)
                imp_norm = importance_accum / imp_max
                # Combined score: importance + weight magnitude
                combined_score = imp_norm + torch.abs(w) / torch.abs(w).max().clamp(min=1e-8)
            else:
                combined_score = torch.abs(w)

            # Stochastic sampling: keep Gaussians with probability proportional to importance
            # Instead of hard pruning, use sampling to preserve geometry better
            n_target = max(int(K * (1.0 - target_prune_ratio)), INIT_K ** 3)
            n_target = min(n_target, K)  # don't try to keep more than we have

            if n_target < K:
                # Also hard-prune near-zero weight Gaussians
                weight_ok = torch.abs(w) > min_weight
                # Sampling probability proportional to combined score
                probs = combined_score.clone()
                probs[~weight_ok] = 0.0  # zero out dead Gaussians
                probs = probs / probs.sum().clamp(min=1e-8)

                # Sample without replacement
                n_keep = min(n_target, weight_ok.sum().item())
                if n_keep > 0 and n_keep < K:
                    keep_idx = torch.multinomial(probs, n_keep, replacement=False)
                    keep_idx = keep_idx.sort()[0]
                    mu = mu[keep_idx]
                    log_sigma = log_sigma[keep_idx]
                    w = w[keep_idx]
                    if importance_accum is not None:
                        importance_accum = importance_accum[keep_idx]
                    # Rebuild optimizer (simpler than selective indexing)
                    opt = AdamGPU(mu.shape[0])

    elapsed = time.time() - t0
    print(f"  Mini-Splatting done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ═══════════════════════════════════════════════════════════════════════
#  METHOD 7: AbsGS (ACM MM 2024, arXiv 2404.10484)
#  Core idea: use absolute value of per-component gradients before summing
#  to avoid "gradient collision" where opposing gradient directions cancel.
#  Standard ADC: grad_accum = sum(dL/dmu_k), then ||grad_accum||
#  AbsGS: grad_accum = sum(|dL_j/dmu_k,x|, |dL_j/dmu_k,y|, ...), then ||grad_accum||
#  This homodirectional gradient better identifies over-reconstructed regions.
# ═══════════════════════════════════════════════════════════════════════
def train_absgs():
    print("\n  [7/8] Training AbsGS ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []

    # AbsGS hyperparameters
    # Higher threshold because absolute gradients are always larger than signed
    abs_grad_thresh = 0.00006  # ~3x standard threshold (0.00002)
    max_per_round = 40
    min_opacity = 0.003

    # Accumulated absolute gradients (homodirectional)
    abs_grad_accum = None
    accum_count = 0

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        K = mu.shape[0]
        sigma = torch.exp(log_sigma)

        # Compute per-sample, per-Gaussian gradients for absolute accumulation
        # We need component-wise gradients, so we compute them in batches
        if step % DENSIFY_EVERY >= (DENSIFY_EVERY - 10) or step % DENSIFY_EVERY < 10:
            # Near densification steps: accumulate absolute gradients
            # This is the "homodirectional" gradient: sum |dL_j/dmu_k,d| for each d
            abs_batch = 8000

            if abs_grad_accum is None or abs_grad_accum.shape[0] != K:
                abs_grad_accum = torch.zeros(K, 3, device=DEVICE)
                accum_count = 0

            with torch.no_grad():
                for _s in range(0, N_SAMPLE, abs_batch):
                    _e = min(_s + abs_batch, N_SAMPLE)
                    pts_b = sample_pts[_s:_e]
                    target_b = target_density[_s:_e]
                    B = _e - _s

                    diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)  # (B, K, 3)
                    sq_dist_b = (diff_b ** 2).sum(dim=2)           # (B, K)
                    exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
                    gauss_b = torch.exp(exponent_b)                # (B, K)
                    pred_b = (gauss_b * w.unsqueeze(0)).sum(dim=1) # (B,)
                    residual_b = pred_b - target_b                 # (B,)

                    # Per-sample gradient of mu: dL/dmu_k = 2*residual * w_k * gauss * (x-mu)/sigma^2
                    common_b = (2.0 / N_SAMPLE) * residual_b.unsqueeze(1) * gauss_b * w.unsqueeze(0)  # (B, K)
                    for d in range(3):
                        per_sample_grad_d = common_b * diff_b[:, :, d] / (sigma.unsqueeze(0) ** 2)  # (B, K)
                        # KEY ABSGS DIFFERENCE: take absolute value before summing over samples
                        abs_grad_accum[:, d] += torch.abs(per_sample_grad_d).sum(dim=0)

                    del diff_b, sq_dist_b, exponent_b, gauss_b, pred_b, residual_b, common_b
                accum_count += 1

        # Standard loss and gradient computation for optimizer step
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w, batch_size=8000)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)
        mse_hist.append(mse)
        cnt_hist.append(mu.shape[0])

        if step % 500 == 0:
            elapsed = time.time() - t0
            print(f"    step {step:5d}  MSE={mse:.6f}  K={mu.shape[0]:5d}  t={elapsed:.1f}s")
            sys.stdout.flush()

        # Densification using homodirectional (absolute) gradient
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 1000 and mu.shape[0] < MAX_GAUSS:
            if abs_grad_accum is not None and accum_count > 0:
                # Average the accumulated absolute gradients
                avg_abs_grad = abs_grad_accum / max(accum_count, 1)
                # Homodirectional gradient magnitude: L2 norm of component-wise absolute sums
                homo_grad_mag = torch.norm(avg_abs_grad, dim=1)  # (K,)

                # Split/clone based on homodirectional gradient threshold
                split_mask = homo_grad_mag > abs_grad_thresh
                split_idx = torch.where(split_mask)[0]

                if len(split_idx) > 0:
                    sigma = torch.exp(log_sigma)
                    budget = (MAX_GAUSS - mu.shape[0]) // 2
                    sorted_idx = split_idx[torch.argsort(-homo_grad_mag[split_idx])]
                    sorted_idx = sorted_idx[:max(min(budget, max_per_round), 0)]

                    if len(sorted_idx) > 0:
                        median_sigma = sigma.median()
                        new_mus = []
                        new_lss = []
                        new_ws = []

                        for idx_val in sorted_idx:
                            idx_int = idx_val.item()
                            parent_sigma = sigma[idx_int]

                            if parent_sigma > median_sigma:
                                # SPLIT: large Gaussian in over-reconstructed region
                                direction = grad_mu[idx_int]
                                dir_norm = torch.norm(direction).clamp(min=1e-8)
                                direction = direction / dir_norm
                                offset = direction * parent_sigma * 0.5

                                new_mus.append(mu[idx_int] - offset)
                                new_mus.append(mu[idx_int] + offset)
                                shrink = float(np.log(0.7))
                                new_lss.append(log_sigma[idx_int].item() + shrink)
                                new_lss.append(log_sigma[idx_int].item() + shrink)
                                new_ws.append(w[idx_int].item() * 0.5)
                                new_ws.append(w[idx_int].item() * 0.5)
                            else:
                                # CLONE: small Gaussian in under-reconstructed region
                                perturbation = torch.randn(3, device=DEVICE) * parent_sigma * 0.3
                                new_mus.append(mu[idx_int] + perturbation)
                                new_lss.append(log_sigma[idx_int].item())
                                new_ws.append(w[idx_int].item())

                        if new_mus:
                            add_mu = torch.stack(new_mus).to(DEVICE)
                            add_ls = torch.tensor(new_lss, device=DEVICE, dtype=torch.float32)
                            add_w = torch.tensor(new_ws, device=DEVICE, dtype=torch.float32)
                            n_new = add_mu.shape[0]
                            mu = torch.cat([mu, add_mu])
                            log_sigma = torch.cat([log_sigma, add_ls])
                            w = torch.cat([w, add_w])
                            opt.extend(n_new)

                # Reset accumulator after densification
                abs_grad_accum = None
                accum_count = 0

            # Pruning: remove near-zero weight Gaussians
            if step % (DENSIFY_EVERY * 3) == 0 and mu.shape[0] > INIT_K ** 3:
                keep_mask = torch.abs(w) > min_opacity
                if keep_mask.sum() < mu.shape[0] and keep_mask.sum() >= INIT_K ** 3:
                    mu = mu[keep_mask]
                    log_sigma = log_sigma[keep_mask]
                    w = w[keep_mask]
                    abs_grad_accum = None
                    accum_count = 0
                    opt = AdamGPU(mu.shape[0])

    elapsed = time.time() - t0
    print(f"  AbsGS done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ═══════════════════════════════════════════════════════════════════════
#  METHOD 8: Pixel-GS (ECCV 2024)
#  Core idea: weight gradient accumulation by the number of pixels (samples)
#  each Gaussian covers. Large Gaussians that participate in many sample
#  computations but contribute only a few pixels per view have their
#  gradients under-counted by standard averaging. Pixel-GS fixes this
#  by using coverage-weighted gradient averaging.
# ═══════════════════════════════════════════════════════════════════════
def train_pixelgs():
    print("\n  [8/8] Training Pixel-GS ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []

    # Pixel-GS hyperparameters
    pixel_grad_thresh = 0.00003  # slightly higher than standard ADC (0.00002)
    max_per_round = 40
    min_opacity = 0.003
    coverage_thresh = 0.01       # Gaussian activation threshold for "covering" a sample
    distance_scale_factor = 1.5  # suppress growth of Gaussians near boundaries (floater suppression)

    # Accumulated pixel-weighted gradients
    pixel_grad_accum = None
    pixel_grad_count = None
    accum_steps = 0

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        K = mu.shape[0]
        sigma = torch.exp(log_sigma)

        # Compute pixel-aware gradient accumulation near densification steps
        if step % DENSIFY_EVERY >= (DENSIFY_EVERY - 10) or step % DENSIFY_EVERY < 10:
            pg_batch = 8000

            if pixel_grad_accum is None or pixel_grad_accum.shape[0] != K:
                pixel_grad_accum = torch.zeros(K, 3, device=DEVICE)
                pixel_grad_count = torch.zeros(K, device=DEVICE)
                accum_steps = 0

            with torch.no_grad():
                for _s in range(0, N_SAMPLE, pg_batch):
                    _e = min(_s + pg_batch, N_SAMPLE)
                    pts_b = sample_pts[_s:_e]
                    target_b = target_density[_s:_e]
                    B = _e - _s

                    diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)  # (B, K, 3)
                    sq_dist_b = (diff_b ** 2).sum(dim=2)           # (B, K)
                    exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
                    gauss_b = torch.exp(exponent_b)                # (B, K)
                    pred_b = (gauss_b * w.unsqueeze(0)).sum(dim=1) # (B,)
                    residual_b = pred_b - target_b                 # (B,)

                    # Per-sample gradient for each Gaussian
                    common_b = (2.0 / N_SAMPLE) * residual_b.unsqueeze(1) * gauss_b * w.unsqueeze(0)

                    # Coverage mask: which samples does each Gaussian "cover"?
                    covers = gauss_b > coverage_thresh  # (B, K) bool

                    # Pixel count per Gaussian for this batch: number of covered samples
                    pixel_count_b = covers.float().sum(dim=0)  # (K,)

                    # Distance-based scaling: suppress gradients from Gaussians near domain boundary
                    # (analogous to Pixel-GS's camera-distance suppression of floaters)
                    dist_from_center = torch.norm(mu, dim=1)  # (K,)
                    dist_scale = torch.exp(-distance_scale_factor * dist_from_center)  # closer to center = more weight

                    # Pixel-aware gradient: weight by coverage count
                    # Standard ADC divides by total observation count (views in real 3DGS)
                    # Pixel-GS divides by coverage-weighted count instead
                    for d in range(3):
                        grad_d = common_b * diff_b[:, :, d] / (sigma.unsqueeze(0) ** 2)  # (B, K)
                        # Weight each sample's gradient contribution by its coverage
                        weighted_grad_d = (grad_d * covers.float()).sum(dim=0)  # (K,)
                        pixel_grad_accum[:, d] += weighted_grad_d * dist_scale

                    # Track total pixel coverage for averaging
                    pixel_grad_count += pixel_count_b

                    del diff_b, sq_dist_b, exponent_b, gauss_b, pred_b, residual_b, common_b, covers
                accum_steps += 1

        # Standard loss and gradient computation for optimizer step
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w, batch_size=8000)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)
        mse_hist.append(mse)
        cnt_hist.append(mu.shape[0])

        if step % 500 == 0:
            elapsed = time.time() - t0
            print(f"    step {step:5d}  MSE={mse:.6f}  K={mu.shape[0]:5d}  t={elapsed:.1f}s")
            sys.stdout.flush()

        # Densification using pixel-aware gradient
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 1000 and mu.shape[0] < MAX_GAUSS:
            if pixel_grad_accum is not None and accum_steps > 0:
                # Average by pixel coverage count (key Pixel-GS difference)
                # Standard ADC would divide by accum_steps (uniform average)
                # Pixel-GS divides by pixel_count (coverage-weighted average)
                safe_count = pixel_grad_count.clamp(min=1.0)
                avg_pixel_grad = pixel_grad_accum / safe_count.unsqueeze(1)
                pixel_grad_mag = torch.norm(avg_pixel_grad, dim=1)  # (K,)

                # Split/clone based on pixel-aware gradient threshold
                split_mask = pixel_grad_mag > pixel_grad_thresh
                split_idx = torch.where(split_mask)[0]

                if len(split_idx) > 0:
                    sigma = torch.exp(log_sigma)
                    budget = (MAX_GAUSS - mu.shape[0]) // 2
                    sorted_idx = split_idx[torch.argsort(-pixel_grad_mag[split_idx])]
                    sorted_idx = sorted_idx[:max(min(budget, max_per_round), 0)]

                    if len(sorted_idx) > 0:
                        median_sigma = sigma.median()
                        new_mus = []
                        new_lss = []
                        new_ws = []

                        for idx_val in sorted_idx:
                            idx_int = idx_val.item()
                            parent_sigma = sigma[idx_int]

                            if parent_sigma > median_sigma:
                                # SPLIT: large Gaussian
                                direction = grad_mu[idx_int]
                                dir_norm = torch.norm(direction).clamp(min=1e-8)
                                direction = direction / dir_norm
                                offset = direction * parent_sigma * 0.5

                                new_mus.append(mu[idx_int] - offset)
                                new_mus.append(mu[idx_int] + offset)
                                shrink = float(np.log(0.7))
                                new_lss.append(log_sigma[idx_int].item() + shrink)
                                new_lss.append(log_sigma[idx_int].item() + shrink)
                                new_ws.append(w[idx_int].item() * 0.5)
                                new_ws.append(w[idx_int].item() * 0.5)
                            else:
                                # CLONE: small Gaussian in under-reconstructed region
                                perturbation = torch.randn(3, device=DEVICE) * parent_sigma * 0.3
                                new_mus.append(mu[idx_int] + perturbation)
                                new_lss.append(log_sigma[idx_int].item())
                                new_ws.append(w[idx_int].item())

                        if new_mus:
                            add_mu = torch.stack(new_mus).to(DEVICE)
                            add_ls = torch.tensor(new_lss, device=DEVICE, dtype=torch.float32)
                            add_w = torch.tensor(new_ws, device=DEVICE, dtype=torch.float32)
                            n_new = add_mu.shape[0]
                            mu = torch.cat([mu, add_mu])
                            log_sigma = torch.cat([log_sigma, add_ls])
                            w = torch.cat([w, add_w])
                            opt.extend(n_new)

                # Reset accumulator
                pixel_grad_accum = None
                pixel_grad_count = None
                accum_steps = 0

            # Pruning: remove near-zero weight Gaussians
            if step % (DENSIFY_EVERY * 3) == 0 and mu.shape[0] > INIT_K ** 3:
                keep_mask = torch.abs(w) > min_opacity
                if keep_mask.sum() < mu.shape[0] and keep_mask.sum() >= INIT_K ** 3:
                    mu = mu[keep_mask]
                    log_sigma = log_sigma[keep_mask]
                    w = w[keep_mask]
                    pixel_grad_accum = None
                    pixel_grad_count = None
                    accum_steps = 0
                    opt = AdamGPU(mu.shape[0])

    elapsed = time.time() - t0
    print(f"  Pixel-GS done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ── Evaluation ────────────────────────────────────────────────────────
def evaluate_on_test_set(mu, log_sigma, w, n_test=N_TEST):
    torch.manual_seed(999)
    test_pts = torch.rand(n_test, 3, device=DEVICE) * 3.0 - 1.5
    test_density = compute_target_density(test_pts)
    with torch.no_grad():
        pred = eval_density_pred_only(test_pts, mu, log_sigma, w)
    mse = ((pred - test_density) ** 2).mean().item()
    max_val = test_density.max().item()
    psnr = 10 * np.log10(max_val ** 2 / (mse + 1e-12))

    detail_mask = test_pts[:, 0] > 0.4
    smooth_mask = (torch.norm(test_pts, dim=1) < 0.5) & (test_pts[:, 0] < 0.0)
    mse_smooth = ((pred[smooth_mask] - test_density[smooth_mask]) ** 2).mean().item() if smooth_mask.sum() > 10 else 0
    mse_detail = ((pred[detail_mask] - test_density[detail_mask]) ** 2).mean().item() if detail_mask.sum() > 10 else 0

    torch.manual_seed(42)
    return mse, psnr, mse_smooth, mse_detail


def spatial_analysis(mu, log_sigma):
    sigma = torch.exp(log_sigma)
    detail_mask = mu[:, 0] > 0.4
    smooth_mask = mu[:, 0] <= 0.0
    n_total = mu.shape[0]
    n_detail = detail_mask.sum().item()
    n_smooth = smooth_mask.sum().item()
    return {
        "total": n_total,
        "n_detail": n_detail,
        "n_smooth": n_smooth,
        "frac_detail": n_detail / n_total if n_total > 0 else 0,
        "avg_sigma_detail": sigma[detail_mask].mean().item() if n_detail > 0 else 0,
        "avg_sigma_smooth": sigma[smooth_mask].mean().item() if n_smooth > 0 else 0,
    }


# ── Plotting ──────────────────────────────────────────────────────────
def save_figures(all_results, method_data):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  matplotlib not available, skipping figures.")
        return

    methods = list(all_results.keys())
    colors = {
        "adc": "#e74c3c",
        "farey": "#2ecc71",
        "mcmc": "#3498db",
        "revising": "#9b59b6",
        "steepgs": "#f39c12",
        "minisplatting": "#1abc9c",
        "absgs": "#e67e22",
        "pixelgs": "#8e44ad",
    }
    labels = {
        "adc": "Standard ADC",
        "farey": "Farey-Guided",
        "mcmc": "3DGS-MCMC",
        "revising": "Revising Dens.",
        "steepgs": "SteepGS",
        "minisplatting": "Mini-Splatting",
        "absgs": "AbsGS",
        "pixelgs": "Pixel-GS",
    }

    # 1) Training MSE curves
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for m in methods:
        mse_hist = method_data[m]["mse_hist"]
        cnt_hist = method_data[m]["cnt_hist"]
        axes[0].semilogy(mse_hist, label=f"{labels[m]} (final {mse_hist[-1]:.6f})",
                        lw=1.5, color=colors[m])
        axes[1].plot(cnt_hist, label=f"{labels[m]} (final {cnt_hist[-1]})",
                    lw=1.5, color=colors[m])

    axes[0].set_xlabel("Training step")
    axes[0].set_ylabel("MSE (log scale)")
    axes[0].set_title("Training MSE Over Time")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel("Training step")
    axes[1].set_ylabel("# Gaussians")
    axes[1].set_title("Gaussian Count Over Training")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    fig.suptitle(f"SOTA Comparison: {len(methods)} Methods (50 bumps, budget {MAX_GAUSS}, {TOTAL_STEPS} steps)",
                 fontsize=13, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/sota_training_curves.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 2) Summary bar charts
    fig, axes = plt.subplots(1, 5, figsize=(22, 5))
    method_names = [labels[m] for m in methods]
    method_colors = [colors[m] for m in methods]

    # Test MSE
    vals = [all_results[m]["test_mse"] for m in methods]
    axes[0].bar(range(len(methods)), vals, color=method_colors)
    axes[0].set_xticks(range(len(methods)))
    axes[0].set_xticklabels([labels[m].replace(" ", "\n") for m in methods], fontsize=7)
    axes[0].set_title("Test MSE\n(lower = better)")
    axes[0].set_ylabel("MSE")

    # Test PSNR
    vals = [all_results[m]["test_psnr"] for m in methods]
    axes[1].bar(range(len(methods)), vals, color=method_colors)
    axes[1].set_xticks(range(len(methods)))
    axes[1].set_xticklabels([labels[m].replace(" ", "\n") for m in methods], fontsize=7)
    axes[1].set_title("Test PSNR (dB)\n(higher = better)")
    axes[1].set_ylabel("PSNR")

    # Gaussian count
    vals = [all_results[m]["final_gaussians"] for m in methods]
    axes[2].bar(range(len(methods)), vals, color=method_colors)
    axes[2].set_xticks(range(len(methods)))
    axes[2].set_xticklabels([labels[m].replace(" ", "\n") for m in methods], fontsize=7)
    axes[2].set_title("Total Gaussians")
    axes[2].set_ylabel("Count")

    # Training time
    vals = [all_results[m]["training_time_s"] for m in methods]
    axes[3].bar(range(len(methods)), vals, color=method_colors)
    axes[3].set_xticks(range(len(methods)))
    axes[3].set_xticklabels([labels[m].replace(" ", "\n") for m in methods], fontsize=7)
    axes[3].set_title("Training Time (s)")
    axes[3].set_ylabel("Seconds")

    # Efficiency (MSE per Gaussian)
    vals = [all_results[m]["mse_per_gaussian"] for m in methods]
    axes[4].bar(range(len(methods)), vals, color=method_colors)
    axes[4].set_xticks(range(len(methods)))
    axes[4].set_xticklabels([labels[m].replace(" ", "\n") for m in methods], fontsize=7)
    axes[4].set_title("MSE per Gaussian\n(lower = more efficient)")
    axes[4].set_ylabel("MSE / #Gauss")
    axes[4].ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

    fig.suptitle("SOTA Densification Comparison: Summary", fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/sota_summary_bars.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 3) Detail vs Smooth MSE comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    vals_smooth = [all_results[m]["test_mse_smooth"] for m in methods]
    vals_detail = [all_results[m]["test_mse_detail"] for m in methods]

    x = range(len(methods))
    axes[0].bar(x, vals_smooth, color=method_colors)
    axes[0].set_xticks(list(x))
    axes[0].set_xticklabels([labels[m].replace(" ", "\n") for m in methods], fontsize=7)
    axes[0].set_title("Smooth Region MSE\n(lower = better)")
    axes[0].set_ylabel("MSE")

    axes[1].bar(x, vals_detail, color=method_colors)
    axes[1].set_xticks(list(x))
    axes[1].set_xticklabels([labels[m].replace(" ", "\n") for m in methods], fontsize=7)
    axes[1].set_title("Detail Region MSE\n(lower = better)")
    axes[1].set_ylabel("MSE")

    fig.suptitle("Region-Specific Reconstruction Quality", fontsize=13, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/sota_region_comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 4) Radar chart: normalized metrics
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    categories = ['PSNR', 'Efficiency\n(1/MSE*K)', 'Smooth\nQuality', 'Detail\nQuality', 'Compactness']
    n_cats = len(categories)
    angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
    angles += angles[:1]

    for m in methods:
        r = all_results[m]
        # Normalize: higher is better for all
        psnr_norm = r["test_psnr"] / max(all_results[mx]["test_psnr"] for mx in methods)
        eff = 1.0 / (r["mse_per_gaussian"] + 1e-12)
        eff_norm = eff / max(1.0 / (all_results[mx]["mse_per_gaussian"] + 1e-12) for mx in methods)
        smooth_err = r["test_mse_smooth"]
        smooth_norm = min(all_results[mx]["test_mse_smooth"] for mx in methods) / max(smooth_err, 1e-12)
        smooth_norm = min(smooth_norm, 1.5)
        detail_err = r["test_mse_detail"]
        detail_norm = min(all_results[mx]["test_mse_detail"] for mx in methods) / max(detail_err, 1e-12)
        detail_norm = min(detail_norm, 1.5)
        compact_norm = min(all_results[mx]["final_gaussians"] for mx in methods) / max(r["final_gaussians"], 1)

        values = [psnr_norm, eff_norm, smooth_norm, detail_norm, compact_norm]
        values += values[:1]
        ax.plot(angles, values, 'o-', linewidth=1.5, label=labels[m], color=colors[m])
        ax.fill(angles, values, alpha=0.1, color=colors[m])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 1.5)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=8)
    ax.set_title("Normalized Performance Radar", fontsize=12, y=1.08)
    plt.tight_layout()
    fig.savefig(f"{OUT}/sota_radar.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  Saved SOTA comparison figures to {OUT}/")


# ── Main ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("  3DGS SOTA Densification Comparison")
    print("  Methods: ADC | Farey | MCMC | Revising | SteepGS | Mini-Splatting | AbsGS | Pixel-GS")
    print(f"  Device: {DEVICE}")
    print(f"  Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, SAMPLES={N_SAMPLE}")
    print(f"  Target: 50 multi-scale bumps (8 coarse + 18 medium + 24 fine)")
    print(f"  Init: {INIT_K}^3 = {INIT_K**3} Gaussians (underfitting regime)")
    print("=" * 70)
    sys.stdout.flush()

    # Train all methods
    trainers = {
        "adc": train_standard_adc,
        "farey": train_farey,
        "mcmc": train_mcmc,
        "revising": train_revising,
        "steepgs": train_steepgs,
        "minisplatting": train_minisplatting,
        "absgs": train_absgs,
        "pixelgs": train_pixelgs,
    }

    all_results = {}
    method_data = {}

    for name, trainer in trainers.items():
        torch.manual_seed(42)
        np.random.seed(42)

        # Clear MPS cache between methods
        import gc
        gc.collect()
        if DEVICE.type == 'mps':
            torch.mps.empty_cache()

        try:
            mu, log_sigma, w_val, mse_hist, cnt_hist, elapsed = trainer()
        except Exception as e:
            print(f"\n  ERROR in {name}: {e}")
            print(f"  Skipping {name} and continuing...")
            sys.stdout.flush()
            continue

        test_mse, psnr, mse_smooth, mse_detail = evaluate_on_test_set(mu, log_sigma, w_val)
        dist = spatial_analysis(mu, log_sigma)

        all_results[name] = {
            "final_train_mse": mse_hist[-1],
            "test_mse": test_mse,
            "test_psnr": psnr,
            "test_mse_smooth": mse_smooth,
            "test_mse_detail": mse_detail,
            "final_gaussians": cnt_hist[-1],
            "training_time_s": round(elapsed, 1),
            "mse_per_gaussian": test_mse / max(cnt_hist[-1], 1),
            "spatial": dist,
        }
        method_data[name] = {"mse_hist": mse_hist, "cnt_hist": cnt_hist}

        # Free trainer tensors after recording results
        del mu, log_sigma, w_val
        gc.collect()
        if DEVICE.type == 'mps':
            torch.mps.empty_cache()

    # Compute pairwise comparisons vs Farey
    comparisons = {}
    farey_r = all_results["farey"]
    for name in ["adc", "mcmc", "revising", "steepgs", "minisplatting", "absgs", "pixelgs"]:
        if name not in all_results:
            continue
        other = all_results[name]
        comp = {
            "farey_mse": farey_r["test_mse"],
            "other_mse": other["test_mse"],
            "mse_ratio": other["test_mse"] / max(farey_r["test_mse"], 1e-12),
            "psnr_diff_db": farey_r["test_psnr"] - other["test_psnr"],
            "farey_gaussians": farey_r["final_gaussians"],
            "other_gaussians": other["final_gaussians"],
            "gaussian_ratio": other["final_gaussians"] / max(farey_r["final_gaussians"], 1),
            "farey_wins_mse": farey_r["test_mse"] < other["test_mse"],
            "farey_wins_psnr": farey_r["test_psnr"] > other["test_psnr"],
            "farey_wins_efficiency": farey_r["mse_per_gaussian"] < other["mse_per_gaussian"],
        }
        if farey_r["test_mse"] < other["test_mse"]:
            comp["farey_mse_improvement_pct"] = round((1 - farey_r["test_mse"] / other["test_mse"]) * 100, 2)
        else:
            comp["farey_mse_improvement_pct"] = -round((1 - other["test_mse"] / farey_r["test_mse"]) * 100, 2)
        comparisons[f"farey_vs_{name}"] = comp

    # Rankings
    ranking_mse = sorted(all_results.keys(), key=lambda m: all_results[m]["test_mse"])
    ranking_psnr = sorted(all_results.keys(), key=lambda m: -all_results[m]["test_psnr"])
    ranking_efficiency = sorted(all_results.keys(), key=lambda m: all_results[m]["mse_per_gaussian"])
    ranking_compact = sorted(all_results.keys(), key=lambda m: all_results[m]["final_gaussians"])

    # Assemble output
    output = {
        "benchmark": "sota_comparison_v1",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": {
            "device": str(DEVICE),
            "max_gaussians": MAX_GAUSS,
            "total_steps": TOTAL_STEPS,
            "n_sample": N_SAMPLE,
            "n_test": N_TEST,
            "n_bumps": 50,
            "init_grid": f"{INIT_K}^3={INIT_K**3}",
            "learning_rate": LR,
            "densify_every": DENSIFY_EVERY,
        },
        "methods": {
            "adc": {"description": "Standard ADC: gradient-threshold split/clone (3DGS baseline)"},
            "farey": {"description": "Farey-guided: Delaunay + mediant placement + local error criterion"},
            "mcmc": {"description": "3DGS-MCMC (NeurIPS 2024): SGLD noise + relocalization of dead Gaussians"},
            "revising": {"description": "Revising Densification (ECCV 2024): pixel-error driven + opacity bias correction"},
            "steepgs": {"description": "SteepGS (CVPR 2025): saddle-point detection + steepest descent splitting"},
            "minisplatting": {"description": "Mini-Splatting (ECCV 2024): importance sampling + blur split + aggressive pruning"},
            "absgs": {"description": "AbsGS (ACM MM 2024): homodirectional absolute gradient densification"},
            "pixelgs": {"description": "Pixel-GS (ECCV 2024): pixel-aware coverage-weighted gradient densification"},
        },
        "results": all_results,
        "comparisons_vs_farey": comparisons,
        "rankings": {
            "by_test_mse": ranking_mse,
            "by_test_psnr": ranking_psnr,
            "by_efficiency": ranking_efficiency,
            "by_compactness": ranking_compact,
        },
    }

    # Print results table
    print(f"\n{'='*90}")
    print(f"  RESULTS: SOTA Densification Comparison")
    print(f"{'='*90}")

    all_method_keys = [m for m in ["adc", "farey", "mcmc", "revising", "steepgs",
                                    "minisplatting", "absgs", "pixelgs"] if m in all_results]

    header = f"{'Metric':<30}"
    for m in all_method_keys:
        header += f"  {m:>14}"
    print(f"\n{header}")
    print("-" * (30 + 16 * len(all_method_keys)))

    for metric, fmt in [
        ("final_train_mse", ".6f"),
        ("test_mse", ".6f"),
        ("test_psnr", ".2f"),
        ("test_mse_smooth", ".6f"),
        ("test_mse_detail", ".6f"),
        ("final_gaussians", "d"),
        ("training_time_s", ".1f"),
        ("mse_per_gaussian", ".2e"),
    ]:
        row = f"{metric:<30}"
        for m in all_method_keys:
            val = all_results[m][metric]
            row += f"  {val:>14{fmt}}"
        print(row)

    print(f"\n  Rankings (best to worst):")
    print(f"    Test MSE:    {' > '.join(ranking_mse)}")
    print(f"    Test PSNR:   {' > '.join(ranking_psnr)}")
    print(f"    Efficiency:  {' > '.join(ranking_efficiency)}")
    print(f"    Compactness: {' > '.join(ranking_compact)}")

    print(f"\n  Farey vs SOTA:")
    for name in ["adc", "mcmc", "revising", "steepgs", "minisplatting", "absgs", "pixelgs"]:
        if f"farey_vs_{name}" not in comparisons:
            continue
        c = comparisons[f"farey_vs_{name}"]
        win_str = "WINS" if c["farey_wins_mse"] else "LOSES"
        print(f"    vs {name:>10}: Farey {win_str} MSE by {abs(c['farey_mse_improvement_pct']):.1f}% "
              f"(PSNR diff: {c['psnr_diff_db']:+.2f}dB, "
              f"Gaussians: {c['farey_gaussians']} vs {c['other_gaussians']})")

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            import numpy as np
            import torch
            # Check bool before int since bool is a subclass of int
            if isinstance(obj, (bool, np.bool_)):
                return int(obj)
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, torch.Tensor):
                if obj.dtype == torch.bool:
                    return obj.tolist()
                return obj.item() if obj.numel() == 1 else obj.tolist()
            return super().default(obj)

    json_path = f"{OUT}/sota_comparison.json"
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    print(f"\n  Results saved to {json_path}")

    print("\nGenerating SOTA comparison figures ...")
    save_figures(all_results, method_data)

    print("\n=== SOTA Comparison Complete ===")
