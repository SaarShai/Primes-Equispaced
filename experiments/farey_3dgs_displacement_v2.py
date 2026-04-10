#!/usr/bin/env python3
# Run with: PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 python3 farey_3dgs_displacement_v2.py
"""
Displacement-Guided Farey Densification v2: Sparse-Detail Target
=================================================================
TEST RATIONALE: The 50-bump target was too uniform — Farey's natural gap-filling
handled it well, leaving no room for displacement guidance to shine. This test
uses a SPARSE-DETAIL target: a smooth background blob with 5 tiny, hard-to-find
high-amplitude features. ADC and classical Farey both waste Gaussians on the
smooth background. Displacement guidance should detect under-resolved pockets.

NEW DISPLACEMENT FORMULATION:
- Instead of global rank deviation D(i) = rank(i) - K*position(i)
- Use LOCAL displacement: for each Gaussian, compute the ratio of its Voronoi
  cell volume to the expected uniform volume. High ratio = under-covered region.
- Score = gradient * local_voronoi_displacement

Compares FOUR methods:
1. Standard ADC (baseline)
2. Classical Farey (mediant insertion in Delaunay gaps)
3. Displacement-guided Farey (LOCAL Voronoi formulation) — NEW
4. Displacement-guided Farey (global rank, from v1, for comparison)

Output: ~/Desktop/Farey-Local/experiments/3dgs_results/displacement_v2_results.json
"""

import torch
import numpy as np
from scipy.spatial import Delaunay, Voronoi, ConvexHull
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
BATCH_SIZE = 8000

OUT = os.path.expanduser("~/Desktop/Farey-Local/experiments/3dgs_results")
os.makedirs(OUT, exist_ok=True)

torch.manual_seed(42)
np.random.seed(42)


# ══════════════════════════════════════════════════════════════════════
#  TARGET: SPARSE DETAIL — smooth background + 5 tiny hidden features
# ══════════════════════════════════════════════════════════════════════
def make_sparse_detail_target():
    """
    Mostly-smooth density with 5 very small, high-amplitude bumps.
    The challenge: most Gaussians are wasted on the smooth background.
    """
    # 5 tiny high-amplitude features at specific locations
    hidden_features = [
        (np.array([0.6, 0.6, 0.6]),   100.0, 2.0),   # sigma~0.07, amp=2
        (np.array([-0.5, 0.4, -0.3]), 120.0, 2.5),   # sigma~0.065
        (np.array([0.2, -0.6, 0.5]),  150.0, 3.0),   # sigma~0.058
        (np.array([-0.7, -0.5, 0.7]), 130.0, 2.0),   # sigma~0.062
        (np.array([0.0, 0.0, -0.8]),  160.0, 2.5),   # sigma~0.056
    ]
    return hidden_features


HIDDEN_FEATURES = make_sparse_detail_target()
FEAT_CENTERS_T = torch.tensor(
    np.array([f[0] for f in HIDDEN_FEATURES]), device=DEVICE, dtype=torch.float32)
FEAT_SCALES_T = torch.tensor(
    np.array([f[1] for f in HIDDEN_FEATURES]), device=DEVICE, dtype=torch.float32)
FEAT_AMPS_T = torch.tensor(
    np.array([f[2] for f in HIDDEN_FEATURES]), device=DEVICE, dtype=torch.float32)


def compute_target_density(pts):
    """Smooth background + 5 tiny hidden bumps."""
    r = torch.norm(pts, dim=1)
    # Broad smooth Gaussian background — easy to fit
    density = 1.0 * torch.exp(-0.5 * r ** 2)

    # 5 tiny, high-amplitude bumps — hard to find
    for i in range(len(HIDDEN_FEATURES)):
        d = torch.norm(pts - FEAT_CENTERS_T[i].unsqueeze(0), dim=1)
        density = density + FEAT_AMPS_T[i] * torch.exp(-FEAT_SCALES_T[i] * d ** 2)
    return density


# Pre-generate training samples
print("Generating sample points ...")
sample_pts = torch.rand(N_SAMPLE, 3, device=DEVICE) * 3.0 - 1.5
target_density = compute_target_density(sample_pts)
print(f"  Target density range: [{target_density.min().item():.3f}, {target_density.max().item():.3f}]")
print(f"  Target density mean: {target_density.mean().item():.4f}")

# Also generate separate test points near each hidden feature
# to measure per-feature reconstruction quality
feature_test_pts = []
feature_test_targets = []
for feat in HIDDEN_FEATURES:
    center = torch.tensor(feat[0], device=DEVICE, dtype=torch.float32)
    # Sample in small sphere around feature
    local_pts = center.unsqueeze(0) + 0.15 * (torch.rand(500, 3, device=DEVICE) - 0.5)
    local_target = compute_target_density(local_pts)
    feature_test_pts.append(local_pts)
    feature_test_targets.append(local_target)
print(f"  Generated {len(HIDDEN_FEATURES)} feature-local test sets (500 pts each)")


# ── Batched density evaluation ────────────────────────────────────────
def eval_density_batched(pts, mu, log_sigma, w, batch_size=BATCH_SIZE):
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
    N = pts.shape[0]
    K = mu.shape[0]
    sigma = torch.exp(log_sigma)

    if N * K > 50_000_000:
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
#  DISPLACEMENT SCORES
# ══════════════════════════════════════════════════════════════════════

def compute_displacement_global_rank(mu):
    """
    Global rank displacement: D(i) = rank(i) - K*normalized_position(i)
    averaged over 3 axes. (Same as v1.)
    """
    K = mu.shape[0]
    if K < 2:
        return torch.zeros(K, device=mu.device)

    displacement = torch.zeros(K, device=mu.device)
    for axis in range(3):
        positions = mu[:, axis]
        p_min = positions.min()
        p_max = positions.max()
        span = p_max - p_min
        if span < 1e-8:
            continue
        normalized = (positions - p_min) / span
        sorted_indices = torch.argsort(positions)
        ranks = torch.zeros(K, device=mu.device)
        ranks[sorted_indices] = torch.arange(K, device=mu.device, dtype=torch.float32)
        d_axis = ranks - K * normalized
        displacement += torch.abs(d_axis)

    displacement = displacement / 3.0
    return displacement


def compute_displacement_local_voronoi(mu):
    """
    LOCAL Voronoi displacement: for each Gaussian, compute the ratio of its
    Voronoi cell volume to the expected uniform volume (total_volume / K).

    High ratio = this Gaussian "owns" a large region = under-covered.
    Low ratio  = crowded region = well-covered.

    Returns log-ratio: log(voronoi_vol / expected_vol) so it's centered at 0.
    We take abs() so both over- and under-coverage are flagged.

    Falls back to k-NN volume estimate when Voronoi is degenerate.
    """
    K = mu.shape[0]
    if K < 5:
        return torch.zeros(K, device=mu.device)

    mu_np = mu.detach().cpu().numpy()

    # Estimate local volume using k-nearest-neighbor distances
    # This is more robust than exact Voronoi in 3D with few points
    from scipy.spatial import cKDTree
    tree = cKDTree(mu_np)
    # Use k=min(7, K-1) nearest neighbors
    k_nn = min(7, K - 1)
    dists, _ = tree.query(mu_np, k=k_nn + 1)  # +1 because self is included
    # Exclude self (distance 0)
    nn_dists = dists[:, 1:]  # shape (K, k_nn)

    # Local volume estimate: product of nn distances (geometric mean proxy)
    # More precisely, use the volume of the sphere with radius = mean nn dist
    mean_nn_dist = nn_dists.mean(axis=1)  # (K,)
    local_vol = (4.0 / 3.0) * np.pi * mean_nn_dist ** 3

    # Expected uniform volume
    # Estimate total volume from convex hull
    try:
        hull = ConvexHull(mu_np)
        total_vol = hull.volume
    except Exception:
        # Fallback: bounding box volume
        bbox = mu_np.max(axis=0) - mu_np.min(axis=0)
        total_vol = max(np.prod(bbox), 1e-10)

    expected_vol = total_vol / K

    # Log-ratio: positive means under-covered, negative means crowded
    ratio = local_vol / (expected_vol + 1e-10)
    log_ratio = np.log(ratio + 1e-10)

    # Use absolute value — both extremes indicate non-uniformity
    displacement = np.abs(log_ratio)

    return torch.tensor(displacement, device=mu.device, dtype=torch.float32)


# ══════════════════════════════════════════════════════════════════════
#  Per-feature MSE evaluation
# ══════════════════════════════════════════════════════════════════════
def evaluate_per_feature(mu, log_sigma, w):
    """Compute MSE near each hidden feature separately."""
    results = []
    with torch.no_grad():
        for i, (pts, tgt) in enumerate(zip(feature_test_pts, feature_test_targets)):
            pred = eval_density_pred_only(pts, mu, log_sigma, w)
            mse = ((pred - tgt) ** 2).mean().item()
            results.append(mse)
    return results


# ══════════════════════════════════════════════════════════════════════
#  METHOD 1: Standard ADC
# ══════════════════════════════════════════════════════════════════════
def train_standard_adc():
    print("\n  [1/4] Training Standard ADC ...")
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
    feat_mse = evaluate_per_feature(mu, log_sigma, w)
    print(f"  ADC done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    print(f"  Per-feature MSE: {[f'{m:.6f}' for m in feat_mse]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed, feat_mse


# ══════════════════════════════════════════════════════════════════════
#  METHOD 2: Classical Farey
# ══════════════════════════════════════════════════════════════════════
def train_farey():
    print("\n  [2/4] Training Classical Farey ...")
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
    feat_mse = evaluate_per_feature(mu, log_sigma, w)
    print(f"  Farey done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    print(f"  Per-feature MSE: {[f'{m:.6f}' for m in feat_mse]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed, feat_mse


# ══════════════════════════════════════════════════════════════════════
#  METHOD 3: Displacement-Guided Farey (LOCAL Voronoi) — NEW
# ══════════════════════════════════════════════════════════════════════
def train_displacement_local_voronoi(alpha=1.5, label="local_voronoi"):
    """
    Local Voronoi displacement: for each Gaussian, compute how much local
    volume it "owns" vs expected. Score = grad * (1 + alpha * voronoi_disp).

    Gaussians far from hidden features have normal Voronoi cells.
    Gaussians near under-resolved features have LARGE Voronoi cells
    (because no other Gaussians are nearby to share the load).
    """
    print(f"\n  Training Displacement-Guided ({label}, alpha={alpha}) ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []
    disp_hist = []
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
            K_cur = mu.shape[0]
            grad_mag = torch.norm(grad_mu, dim=1)

            # Compute LOCAL Voronoi displacement
            disp = compute_displacement_local_voronoi(mu)
            max_disp = disp.max()
            if max_disp < 1e-8:
                max_disp = torch.tensor(1.0, device=DEVICE)
            norm_disp = disp / max_disp

            # Combined score
            score = grad_mag * (1.0 + alpha * norm_disp)

            # Track stats periodically
            if step % (DENSIFY_EVERY * 5) == 0:
                disp_hist.append({
                    "step": step,
                    "mean_disp": disp.mean().item(),
                    "max_disp": max_disp.item(),
                    "mean_grad": grad_mag.mean().item(),
                    "correlation": float(torch.corrcoef(
                        torch.stack([grad_mag, disp]))[0, 1].item()) if K_cur > 2 else 0.0
                })

            # Select by combined score
            grad_mask = grad_mag > grad_thresh
            split_idx = torch.where(grad_mask)[0]

            if len(split_idx) > 0:
                budget = (MAX_GAUSS - mu.shape[0]) // 2
                sorted_idx = split_idx[torch.argsort(-score[split_idx])]
                sorted_idx = sorted_idx[:max(budget, 0)]

                if len(sorted_idx) > 0:
                    sigma = torch.exp(log_sigma)
                    directions = grad_mu[sorted_idx]
                    dir_norms = torch.norm(directions, dim=1, keepdim=True).clamp(min=1e-8)
                    directions = directions / dir_norms

                    # Larger split offset for high-displacement (under-covered) Gaussians
                    disp_factor = 1.0 + 0.5 * norm_disp[sorted_idx]
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
    feat_mse = evaluate_per_feature(mu, log_sigma, w)
    print(f"  {label} done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    print(f"  Per-feature MSE: {[f'{m:.6f}' for m in feat_mse]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed, feat_mse, disp_hist


# ══════════════════════════════════════════════════════════════════════
#  METHOD 4: Displacement-Guided Farey (GLOBAL rank, from v1)
# ══════════════════════════════════════════════════════════════════════
def train_displacement_global_rank(alpha=1.5, label="global_rank"):
    """Global rank displacement from v1 for comparison."""
    print(f"\n  Training Displacement-Guided ({label}, alpha={alpha}) ...")
    mu, log_sigma, w = init_gaussians_3d()
    opt = AdamGPU(mu.shape[0])
    mse_hist, cnt_hist = [], []
    disp_hist = []
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
            K_cur = mu.shape[0]
            grad_mag = torch.norm(grad_mu, dim=1)

            # Global rank displacement (from v1)
            disp = compute_displacement_global_rank(mu)
            max_disp = disp.max()
            if max_disp < 1e-8:
                max_disp = torch.tensor(1.0, device=DEVICE)
            norm_disp = disp / max_disp

            score = grad_mag * (1.0 + alpha * norm_disp)

            if step % (DENSIFY_EVERY * 5) == 0:
                disp_hist.append({
                    "step": step,
                    "mean_disp": disp.mean().item(),
                    "max_disp": max_disp.item(),
                    "mean_grad": grad_mag.mean().item(),
                    "correlation": float(torch.corrcoef(
                        torch.stack([grad_mag, disp]))[0, 1].item()) if K_cur > 2 else 0.0
                })

            grad_mask = grad_mag > grad_thresh
            split_idx = torch.where(grad_mask)[0]

            if len(split_idx) > 0:
                budget = (MAX_GAUSS - mu.shape[0]) // 2
                sorted_idx = split_idx[torch.argsort(-score[split_idx])]
                sorted_idx = sorted_idx[:max(budget, 0)]

                if len(sorted_idx) > 0:
                    sigma = torch.exp(log_sigma)
                    directions = grad_mu[sorted_idx]
                    dir_norms = torch.norm(directions, dim=1, keepdim=True).clamp(min=1e-8)
                    directions = directions / dir_norms

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
    feat_mse = evaluate_per_feature(mu, log_sigma, w)
    print(f"  {label} done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    print(f"  Per-feature MSE: {[f'{m:.6f}' for m in feat_mse]}")
    sys.stdout.flush()
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed, feat_mse, disp_hist


# ══════════════════════════════════════════════════════════════════════
#  EVALUATION ON HELD-OUT TEST SET
# ══════════════════════════════════════════════════════════════════════
def evaluate_on_test(mu, log_sigma, w, label):
    test_pts = torch.rand(N_TEST, 3, device=DEVICE) * 3.0 - 1.5
    test_target = compute_target_density(test_pts)
    with torch.no_grad():
        test_pred = eval_density_pred_only(test_pts, mu, log_sigma, w)
    mse = ((test_pred - test_target) ** 2).mean().item()
    mae = (torch.abs(test_pred - test_target)).mean().item()

    # Also compute MSE on background-only region (far from features)
    min_feat_dist = torch.inf * torch.ones(N_TEST, device=DEVICE)
    for feat in HIDDEN_FEATURES:
        c = torch.tensor(feat[0], device=DEVICE, dtype=torch.float32)
        d = torch.norm(test_pts - c.unsqueeze(0), dim=1)
        min_feat_dist = torch.minimum(min_feat_dist, d)
    bg_mask = min_feat_dist > 0.3  # far from all features
    fg_mask = min_feat_dist < 0.15  # near a feature

    bg_mse = ((test_pred[bg_mask] - test_target[bg_mask]) ** 2).mean().item() if bg_mask.sum() > 10 else float('nan')
    fg_mse = ((test_pred[fg_mask] - test_target[fg_mask]) ** 2).mean().item() if fg_mask.sum() > 10 else float('nan')

    print(f"  Test {label:25s}: MSE={mse:.6f}  MAE={mae:.4f}  BG_MSE={bg_mse:.6f}  FG_MSE={fg_mse:.6f}")
    print(f"    (background pts: {bg_mask.sum().item()}, feature pts: {fg_mask.sum().item()})")
    return {"mse": mse, "mae": mae, "bg_mse": bg_mse, "fg_mse": fg_mse,
            "n_bg": int(bg_mask.sum().item()), "n_fg": int(fg_mask.sum().item())}


# ══════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 70)
    print("Displacement-Guided Farey 3DGS v2: Sparse-Detail Target")
    print("=" * 70)
    print(f"Target: smooth background + 5 tiny hidden features")
    print(f"Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, BATCH={BATCH_SIZE}")
    print(f"Device: {DEVICE}")
    print()

    results = {}
    all_start = time.time()

    # ── Method 1: ADC ────────────────────────────────────────────────
    mu1, ls1, w1, mse1, cnt1, t1, feat1 = train_standard_adc()
    test1 = evaluate_on_test(mu1, ls1, w1, "ADC")
    results["adc"] = {
        "final_mse": mse1[-1], "final_k": cnt1[-1], "time": t1,
        "mse_history": mse1[::100], "count_history": cnt1[::100],
        "test": test1, "per_feature_mse": feat1
    }
    del mu1, ls1, w1
    if DEVICE.type == "mps":
        torch.mps.empty_cache()

    # ── Method 2: Classical Farey ────────────────────────────────────
    mu2, ls2, w2, mse2, cnt2, t2, feat2 = train_farey()
    test2 = evaluate_on_test(mu2, ls2, w2, "Classical Farey")
    results["farey"] = {
        "final_mse": mse2[-1], "final_k": cnt2[-1], "time": t2,
        "mse_history": mse2[::100], "count_history": cnt2[::100],
        "test": test2, "per_feature_mse": feat2
    }
    del mu2, ls2, w2
    if DEVICE.type == "mps":
        torch.mps.empty_cache()

    # ── Method 3: Local Voronoi Displacement (NEW) ───────────────────
    mu3, ls3, w3, mse3, cnt3, t3, feat3, dh3 = train_displacement_local_voronoi(
        alpha=1.5, label="local_voronoi_a1.5")
    test3 = evaluate_on_test(mu3, ls3, w3, "Local Voronoi (a=1.5)")
    results["disp_local_voronoi"] = {
        "final_mse": mse3[-1], "final_k": cnt3[-1], "time": t3,
        "mse_history": mse3[::100], "count_history": cnt3[::100],
        "test": test3, "per_feature_mse": feat3,
        "displacement_stats": dh3, "alpha": 1.5
    }
    del mu3, ls3, w3
    if DEVICE.type == "mps":
        torch.mps.empty_cache()

    # ── Method 4: Global Rank Displacement (from v1) ─────────────────
    mu4, ls4, w4, mse4, cnt4, t4, feat4, dh4 = train_displacement_global_rank(
        alpha=1.5, label="global_rank_a1.5")
    test4 = evaluate_on_test(mu4, ls4, w4, "Global Rank (a=1.5)")
    results["disp_global_rank"] = {
        "final_mse": mse4[-1], "final_k": cnt4[-1], "time": t4,
        "mse_history": mse4[::100], "count_history": cnt4[::100],
        "test": test4, "per_feature_mse": feat4,
        "displacement_stats": dh4, "alpha": 1.5
    }
    del mu4, ls4, w4
    if DEVICE.type == "mps":
        torch.mps.empty_cache()

    total_time = time.time() - all_start

    # ── Summary ──────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY — Sparse-Detail Target")
    print("=" * 70)
    print(f"{'Method':<30s} {'Final MSE':>12s} {'Test MSE':>12s} {'BG MSE':>12s} {'FG MSE':>12s} {'K':>6s} {'Time':>8s}")
    print("-" * 92)
    for name, r in results.items():
        print(f"{name:<30s} {r['final_mse']:12.6f} {r['test']['mse']:12.6f} "
              f"{r['test']['bg_mse']:12.6f} {r['test']['fg_mse']:12.6f} "
              f"{r['final_k']:6d} {r['time']:7.1f}s")

    print(f"\nPer-feature MSE breakdown:")
    for name, r in results.items():
        feat_str = "  ".join([f"F{i}={m:.6f}" for i, m in enumerate(r['per_feature_mse'])])
        print(f"  {name:<30s}: {feat_str}")

    # Find best method for foreground (feature detection)
    fg_mses = {name: r['test']['fg_mse'] for name, r in results.items()}
    best_fg = min(fg_mses, key=fg_mses.get)
    worst_fg = max(fg_mses, key=fg_mses.get)
    if fg_mses[worst_fg] > 0:
        improvement = (fg_mses[worst_fg] - fg_mses[best_fg]) / fg_mses[worst_fg] * 100
        print(f"\nBest feature detection: {best_fg} ({improvement:.1f}% better FG MSE than {worst_fg})")

    print(f"\nTotal experiment time: {total_time:.1f}s")

    # ── Save results ─────────────────────────────────────────────────
    results["metadata"] = {
        "experiment": "displacement_v2_sparse_detail",
        "target": "smooth_background_5_tiny_features",
        "max_gauss": MAX_GAUSS,
        "total_steps": TOTAL_STEPS,
        "n_sample": N_SAMPLE,
        "batch_size": BATCH_SIZE,
        "device": str(DEVICE),
        "total_time": total_time,
        "feature_locations": [f[0].tolist() for f in HIDDEN_FEATURES],
        "feature_scales": [float(f[1]) for f in HIDDEN_FEATURES],
        "feature_amplitudes": [float(f[2]) for f in HIDDEN_FEATURES],
    }

    out_path = os.path.join(OUT, "displacement_v2_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=lambda x: float(x) if hasattr(x, 'item') else str(x))
    print(f"\nResults saved to {out_path}")
    print("DONE.")
