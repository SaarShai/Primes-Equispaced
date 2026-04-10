#!/usr/bin/env python3
# Run with: PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 python3 farey_3dgs_displacement_guided.py
"""
Displacement-Guided Farey Densification for 3D Gaussian Splatting
=================================================================
Novel method: uses Farey displacement D(f) = rank(f) - K*f as a local
error estimator to guide WHERE to densify. High |D| means the local
approximation is spatially uneven — prioritize densification there.

Compares THREE methods:
1. Standard ADC (baseline) — split highest-gradient Gaussians
2. Classical Farey (mediant insertion in Delaunay gaps)
3. Displacement-guided Farey (NEW) — combined gradient + displacement score
   Score = grad_magnitude * (1 + alpha * |D|/max(|D|))
   Tests alpha = 0 (pure gradient), alpha = 1 (balanced), alpha = 2 (heavy)

Same benchmark as v2: 50 multi-scale bumps, budget 1500, 7000 steps, 50K samples.
Output: ~/Desktop/Farey-Local/experiments/3dgs_results/displacement_guided_results.json
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
BATCH_SIZE = 8000      # For N*K intermediates on MPS

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
def eval_density_batched(pts, mu, log_sigma, w, batch_size=BATCH_SIZE):
    """Evaluate density in batches to avoid OOM with large N*K."""
    N = pts.shape[0]
    K = mu.shape[0]
    sigma = torch.exp(log_sigma)

    if N * K < 50_000_000:
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


def eval_density_pred_only(pts, mu, log_sigma, w, batch_size=BATCH_SIZE):
    """Lightweight prediction: returns only pred (N,), no intermediates."""
    N = pts.shape[0]
    K = mu.shape[0]
    sigma = torch.exp(log_sigma)
    pred = torch.zeros(N, device=pts.device)

    for start in range(0, N, batch_size):
        end = min(start + batch_size, N)
        pts_b = pts[start:end]
        diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)
        sq_dist_b = (diff_b ** 2).sum(dim=2)
        exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
        gauss_b = torch.exp(exponent_b)
        pred[start:end] = (gauss_b * w.unsqueeze(0)).sum(dim=1)
        del diff_b, sq_dist_b, exponent_b, gauss_b

    return pred


def compute_loss_and_grads(pts, target, mu, log_sigma, w, batch_size=BATCH_SIZE):
    """MSE loss and analytical gradients (batched for MPS memory)."""
    N = pts.shape[0]
    K = mu.shape[0]
    sigma = torch.exp(log_sigma)

    if N * K > 50_000_000:
        # Memory-efficient batched computation
        grad_mu = torch.zeros_like(mu)
        grad_ls = torch.zeros(K, device=mu.device)
        grad_w = torch.zeros(K, device=mu.device)
        total_sq_err = 0.0

        for start in range(0, N, batch_size):
            end = min(start + batch_size, N)
            pts_b = pts[start:end]
            target_b = target[start:end]

            diff_b = pts_b.unsqueeze(1) - mu.unsqueeze(0)
            sq_dist_b = (diff_b ** 2).sum(dim=2)
            exponent_b = -sq_dist_b / (2.0 * sigma.unsqueeze(0) ** 2)
            gauss_b = torch.exp(exponent_b)
            pred_b = (gauss_b * w.unsqueeze(0)).sum(dim=1)
            residual_b = pred_b - target_b
            total_sq_err += (residual_b ** 2).sum().item()

            common_b = (2.0 / N) * residual_b.unsqueeze(1) * gauss_b
            grad_w += common_b.sum(dim=0)
            weighted_b = common_b * w.unsqueeze(0)
            for d in range(3):
                grad_mu[:, d] += (weighted_b * diff_b[:, :, d] / (sigma.unsqueeze(0) ** 2)).sum(dim=0)
            grad_ls += (weighted_b * sq_dist_b / (sigma.unsqueeze(0) ** 2)).sum(dim=0)

            del diff_b, sq_dist_b, exponent_b, gauss_b, pred_b, residual_b, common_b, weighted_b

        mse = total_sq_err / N
        return mse, grad_mu, grad_ls, grad_w

    # Non-batched path
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


# ══════════════════════════════════════════════════════════════════════
#  DISPLACEMENT SCORE COMPUTATION
# ══════════════════════════════════════════════════════════════════════
def compute_displacement_scores(mu):
    """
    Compute Farey displacement D(i) for each Gaussian.

    For 3D positions, we project onto each axis and average the displacement.
    D_axis(i) = rank(i along axis) - K * normalized_position(i along axis)
    D(i) = mean(|D_x|, |D_y|, |D_z|)

    High |D| = Gaussian is far from its "expected" uniform position => uneven coverage.
    """
    K = mu.shape[0]
    if K < 2:
        return torch.zeros(K, device=mu.device)

    displacement = torch.zeros(K, device=mu.device)

    for axis in range(3):
        positions = mu[:, axis]
        # Normalize to [0, 1] for displacement calculation
        p_min = positions.min()
        p_max = positions.max()
        span = p_max - p_min
        if span < 1e-8:
            continue
        normalized = (positions - p_min) / span  # [0, 1]

        # Rank each Gaussian along this axis (0-indexed)
        sorted_indices = torch.argsort(positions)
        ranks = torch.zeros(K, device=mu.device)
        ranks[sorted_indices] = torch.arange(K, device=mu.device, dtype=torch.float32)

        # D(i) = rank(i) - K * normalized_position(i)
        d_axis = ranks - K * normalized
        displacement += torch.abs(d_axis)

    # Average over 3 axes
    displacement = displacement / 3.0
    return displacement


# ══════════════════════════════════════════════════════════════════════
#  METHOD 1: Standard ADC (baseline)
# ══════════════════════════════════════════════════════════════════════
def train_standard_adc():
    print("\n  [1/5] Training Standard ADC ...")
    print(f"  Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, N_SAMPLE={N_SAMPLE}")
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


# ══════════════════════════════════════════════════════════════════════
#  METHOD 2: Classical Farey (mediant insertion)
# ══════════════════════════════════════════════════════════════════════
def train_farey():
    print("\n  [2/5] Training Classical Farey ...")
    print(f"  Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, N_SAMPLE={N_SAMPLE}")
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


# ══════════════════════════════════════════════════════════════════════
#  METHOD 3: Displacement-Guided Farey Densification (NOVEL)
# ══════════════════════════════════════════════════════════════════════
def train_displacement_guided(alpha=1.0, label="alpha=1"):
    """
    Displacement-guided densification: combines gradient magnitude with
    Farey displacement to prioritize splitting Gaussians that are BOTH
    high-gradient AND poorly positioned (high |D|).

    Score(i) = grad_mag(i) * (1 + alpha * |D(i)| / max(|D|))

    alpha=0 => pure gradient (equivalent to ADC with split direction)
    alpha=1 => balanced gradient + displacement
    alpha=2 => displacement-heavy
    """
    tag = f"disp_a{alpha:.0f}"
    print(f"\n  Training Displacement-Guided Farey ({label}) ...")
    print(f"  Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, alpha={alpha}")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []
    disp_hist = []  # Track displacement statistics
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

        # Displacement-guided densification
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 1000 and mu.shape[0] < MAX_GAUSS:
            K = mu.shape[0]
            grad_mag = torch.norm(grad_mu, dim=1)

            # Compute Farey displacement scores
            disp = compute_displacement_scores(mu)
            max_disp = disp.max()
            if max_disp < 1e-8:
                max_disp = torch.tensor(1.0, device=DEVICE)

            # Normalized displacement: |D| / max(|D|) in [0, 1]
            norm_disp = disp / max_disp

            # Combined score: gradient * (1 + alpha * normalized_displacement)
            score = grad_mag * (1.0 + alpha * norm_disp)

            # Track displacement statistics
            if step % (DENSIFY_EVERY * 5) == 0:
                disp_hist.append({
                    "step": step,
                    "mean_disp": disp.mean().item(),
                    "max_disp": max_disp.item(),
                    "mean_grad": grad_mag.mean().item(),
                    "correlation": torch.corrcoef(torch.stack([grad_mag, disp]))[0, 1].item()
                        if K > 2 else 0.0
                })

            # Select Gaussians to split based on combined score
            # Use same gradient threshold but rank by combined score
            grad_mask = grad_mag > grad_thresh
            split_idx = torch.where(grad_mask)[0]

            if len(split_idx) > 0:
                budget = (MAX_GAUSS - mu.shape[0]) // 2
                # Sort by COMBINED score (not just gradient)
                sorted_idx = split_idx[torch.argsort(-score[split_idx])]
                sorted_idx = sorted_idx[:max(budget, 0)]

                if len(sorted_idx) > 0:
                    sigma = torch.exp(log_sigma)

                    # Split direction: use gradient direction (same as ADC)
                    directions = grad_mu[sorted_idx]
                    dir_norms = torch.norm(directions, dim=1, keepdim=True).clamp(min=1e-8)
                    directions = directions / dir_norms

                    # Split offset proportional to sigma
                    # For high-displacement Gaussians, use slightly larger offsets
                    # to better fill the gap
                    disp_factor = 1.0 + 0.3 * norm_disp[sorted_idx]
                    offsets = directions * sigma[sorted_idx].unsqueeze(1) * 0.5 * disp_factor.unsqueeze(1)

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
    print(f"  {tag} done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed, disp_hist


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

    # Per-region
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

    methods = list(method_data.keys())
    colors = {
        "adc": "#e74c3c",
        "farey": "#2ecc71",
        "disp_a0": "#9b59b6",
        "disp_a1": "#3498db",
        "disp_a2": "#f39c12",
    }
    labels = {
        "adc": "Standard ADC",
        "farey": "Classical Farey",
        "disp_a0": "Disp alpha=0",
        "disp_a1": "Disp alpha=1",
        "disp_a2": "Disp alpha=2",
    }

    # 1) Training curves
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    for key in methods:
        md = method_data[key]
        c = colors.get(key, "#666666")
        lbl = labels.get(key, key)
        axes[0].semilogy(md["mse_hist"], label=f"{lbl} ({md['mse_hist'][-1]:.6f})", lw=1.3, color=c)
        axes[1].plot(md["cnt_hist"], label=f"{lbl} ({md['cnt_hist'][-1]})", lw=1.3, color=c)

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

    fig.suptitle("Displacement-Guided 3DGS: Training Curves", fontsize=13, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/displacement_training_curves.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 2) Summary bar chart
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    method_names = [labels.get(m, m) for m in methods]
    method_colors = [colors.get(m, "#666") for m in methods]

    test_mses = [all_results[m]["test_mse"] for m in methods]
    test_psnrs = [all_results[m]["test_psnr"] for m in methods]
    gauss_counts = [all_results[m]["final_gaussians"] for m in methods]
    times = [all_results[m]["training_time_s"] for m in methods]

    axes[0].bar(range(len(methods)), test_mses, color=method_colors, tick_label=method_names)
    axes[0].set_title("Test MSE\n(lower = better)")
    axes[0].set_ylabel("MSE")
    axes[0].tick_params(axis='x', rotation=30)

    axes[1].bar(range(len(methods)), test_psnrs, color=method_colors, tick_label=method_names)
    axes[1].set_title("Test PSNR (dB)\n(higher = better)")
    axes[1].set_ylabel("PSNR")
    axes[1].tick_params(axis='x', rotation=30)

    axes[2].bar(range(len(methods)), gauss_counts, color=method_colors, tick_label=method_names)
    axes[2].set_title("Total Gaussians")
    axes[2].set_ylabel("Count")
    axes[2].tick_params(axis='x', rotation=30)

    axes[3].bar(range(len(methods)), times, color=method_colors, tick_label=method_names)
    axes[3].set_title("Training Time (s)")
    axes[3].set_ylabel("Seconds")
    axes[3].tick_params(axis='x', rotation=30)

    fig.suptitle("Displacement-Guided 3DGS: Summary Comparison", fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/displacement_summary_bars.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 3) Detail vs Smooth region comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    mse_details = [all_results[m]["test_mse_detail"] for m in methods]
    mse_smooths = [all_results[m]["test_mse_smooth"] for m in methods]

    x = range(len(methods))
    axes[0].bar(x, mse_details, color=method_colors, tick_label=method_names)
    axes[0].set_title("Detail Region MSE (x > 0.4)\n(lower = better)")
    axes[0].set_ylabel("MSE")
    axes[0].tick_params(axis='x', rotation=30)

    axes[1].bar(x, mse_smooths, color=method_colors, tick_label=method_names)
    axes[1].set_title("Smooth Region MSE (core, x < 0)\n(lower = better)")
    axes[1].set_ylabel("MSE")
    axes[1].tick_params(axis='x', rotation=30)

    fig.suptitle("Regional Performance: Detail vs Smooth", fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/displacement_regional.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  Saved figures to {OUT}/")


# ── Main ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("  Displacement-Guided Farey Densification Benchmark")
    print("  Novel: D(f) = rank(f) - K*f as local error estimator")
    print(f"  Device: {DEVICE}")
    print(f"  Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, SAMPLES={N_SAMPLE}")
    print(f"  Target: 50 multi-scale bumps (8 coarse + 18 medium + 24 fine)")
    print(f"  Init: {INIT_K}^3 = {INIT_K**3} Gaussians")
    print(f"  Methods: ADC, Classical Farey, Disp alpha=0/1/2")
    print("=" * 70)
    sys.stdout.flush()

    # Store all method data for plotting
    method_data = {}

    # Method 1: Standard ADC
    mu_a, ls_a, w_a, mse_adc, cnt_adc, time_adc = train_standard_adc()
    method_data["adc"] = {"mse_hist": mse_adc, "cnt_hist": cnt_adc}

    # Method 2: Classical Farey
    mu_f, ls_f, w_f, mse_far, cnt_far, time_far = train_farey()
    method_data["farey"] = {"mse_hist": mse_far, "cnt_hist": cnt_far}

    # Method 3a: Displacement-guided alpha=0 (pure gradient baseline)
    print("\n  [3/5] Displacement-guided alpha=0 (gradient only) ...")
    mu_d0, ls_d0, w_d0, mse_d0, cnt_d0, time_d0, disp_d0 = train_displacement_guided(alpha=0.0, label="alpha=0")
    method_data["disp_a0"] = {"mse_hist": mse_d0, "cnt_hist": cnt_d0}

    # Method 3b: Displacement-guided alpha=1 (balanced)
    print("\n  [4/5] Displacement-guided alpha=1 (balanced) ...")
    mu_d1, ls_d1, w_d1, mse_d1, cnt_d1, time_d1, disp_d1 = train_displacement_guided(alpha=1.0, label="alpha=1")
    method_data["disp_a1"] = {"mse_hist": mse_d1, "cnt_hist": cnt_d1}

    # Method 3c: Displacement-guided alpha=2 (displacement-heavy)
    print("\n  [5/5] Displacement-guided alpha=2 (displacement-heavy) ...")
    mu_d2, ls_d2, w_d2, mse_d2, cnt_d2, time_d2, disp_d2 = train_displacement_guided(alpha=2.0, label="alpha=2")
    method_data["disp_a2"] = {"mse_hist": mse_d2, "cnt_hist": cnt_d2}

    # Evaluate all methods
    print("\n  Evaluating on test set ...")
    eval_data = [
        ("adc", mu_a, ls_a, w_a, time_adc, mse_adc, cnt_adc),
        ("farey", mu_f, ls_f, w_f, time_far, mse_far, cnt_far),
        ("disp_a0", mu_d0, ls_d0, w_d0, time_d0, mse_d0, cnt_d0),
        ("disp_a1", mu_d1, ls_d1, w_d1, time_d1, mse_d1, cnt_d1),
        ("disp_a2", mu_d2, ls_d2, w_d2, time_d2, mse_d2, cnt_d2),
    ]

    all_results = {}
    for name, mu, ls, w, t_train, mse_h, cnt_h in eval_data:
        test_mse, psnr, mse_smooth, mse_detail = evaluate_on_test_set(mu, ls, w)
        spatial = spatial_analysis(mu, ls)
        all_results[name] = {
            "final_train_mse": mse_h[-1],
            "test_mse": test_mse,
            "test_psnr": psnr,
            "test_mse_smooth": mse_smooth,
            "test_mse_detail": mse_detail,
            "final_gaussians": cnt_h[-1],
            "training_time_s": round(t_train, 1),
            "mse_per_gaussian": test_mse / max(cnt_h[-1], 1),
            "spatial": spatial,
        }

    # Add displacement tracking data for alpha=1
    if disp_d1:
        all_results["disp_a1"]["displacement_tracking"] = disp_d1

    # Build comparison summary
    best_method = min(all_results.keys(), key=lambda k: all_results[k]["test_mse"])
    worst_method = max(all_results.keys(), key=lambda k: all_results[k]["test_mse"])

    comparison = {
        "best_overall_mse": best_method,
        "best_mse_value": all_results[best_method]["test_mse"],
        "worst_mse_value": all_results[worst_method]["test_mse"],
        "improvement_best_vs_adc_pct": round(
            (1 - all_results[best_method]["test_mse"] / all_results["adc"]["test_mse"]) * 100, 2
        ),
        "improvement_best_vs_farey_pct": round(
            (1 - all_results[best_method]["test_mse"] / all_results["farey"]["test_mse"]) * 100, 2
        ),
        "disp_a1_vs_adc_pct": round(
            (1 - all_results["disp_a1"]["test_mse"] / all_results["adc"]["test_mse"]) * 100, 2
        ),
        "disp_a1_vs_farey_pct": round(
            (1 - all_results["disp_a1"]["test_mse"] / all_results["farey"]["test_mse"]) * 100, 2
        ),
    }

    # Full output
    output = {
        "benchmark": "displacement_guided_v1",
        "description": "Novel: Farey displacement D(f)=rank(f)-K*f as local error estimator for 3DGS densification",
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
            "batch_size": BATCH_SIZE,
        },
        "methods": all_results,
        "comparison": comparison,
    }

    # Print results table
    print(f"\n{'='*80}")
    print(f"  RESULTS: Displacement-Guided Farey Densification")
    print(f"{'='*80}")

    header = f"{'Metric':<35}"
    for name in ["adc", "farey", "disp_a0", "disp_a1", "disp_a2"]:
        header += f"  {name:>10}"
    print(f"\n{header}")
    print("-" * 90)

    for metric, fmt in [
        ("test_mse", ".6f"),
        ("test_psnr", ".2f"),
        ("test_mse_smooth", ".6f"),
        ("test_mse_detail", ".6f"),
        ("final_gaussians", "d"),
        ("training_time_s", ".1f"),
    ]:
        row = f"{metric:<35}"
        for name in ["adc", "farey", "disp_a0", "disp_a1", "disp_a2"]:
            val = all_results[name][metric]
            if fmt == "d":
                row += f"  {val:>10d}"
            else:
                row += f"  {val:>10{fmt}}"
        print(row)

    print(f"\n  Best overall (test MSE): {best_method}")
    print(f"  Disp alpha=1 vs ADC: {comparison['disp_a1_vs_adc_pct']:.2f}%")
    print(f"  Disp alpha=1 vs Classical Farey: {comparison['disp_a1_vs_farey_pct']:.2f}%")
    print(f"  Best vs ADC: {comparison['improvement_best_vs_adc_pct']:.2f}%")

    json_path = f"{OUT}/displacement_guided_results.json"
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved to {json_path}")

    print("\nGenerating figures ...")
    save_figures(all_results, method_data)

    print("\n=== Displacement-Guided Benchmark Complete ===")
