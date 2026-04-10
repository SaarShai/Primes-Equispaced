#!/usr/bin/env python3
"""
Hilbert+Farey 3D Kill-or-Promote Test
======================================

Idea: Map 3D Gaussian positions → 1D via Morton/Hilbert curve → apply
Farey mediant densification along 1D ordering → map back to 3D.

Compares 4 strategies:
  1. Standard ADC (gradient-based split in 3D)
  2. Direct Farey (3D Delaunay + mediant insertion — existing method)
  3. Hilbert+Farey (1D Farey along space-filling curve)
  4. Hilbert+Bisection (control: same curve, midpoint instead of mediant)

Same scene: sphere with high-detail patch.
Budget: MAX_GAUSS=1500, 7000 steps, 50K sample points.

Kill criterion: Hilbert+Farey must beat Hilbert+Bisection or it's dead.
"""

import numpy as np
from scipy.spatial import Delaunay, KDTree
import time
import json
import os

np.random.seed(42)

# ── Configuration ─────────────────────────────────────────────────────
MAX_GAUSS = 1500
INIT_K = 6            # 6^3 = 216 initial Gaussians
TOTAL_STEPS = 7000
DENSIFY_EVERY = 200
LR = 0.006
N_SAMPLE = 50000      # 50K sample points
MAX_PER_ROUND = 40    # max new Gaussians per densification round

OUT_DIR = "/Users/saar/Desktop/Farey-Local/experiments"

print(f"Hilbert+Farey 3D Test")
print(f"Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, SAMPLES={N_SAMPLE}")
print(f"Init: {INIT_K}^3 = {INIT_K**3} Gaussians")
print()

# ── Target density field ──────────────────────────────────────────────
def make_target_samples(n=N_SAMPLE, seed=42):
    """
    Sphere + high-detail patch in +x octant.
    Returns: positions (N,3), target_density (N,)
    """
    rng = np.random.RandomState(seed)
    pts = rng.uniform(-1.5, 1.5, (n, 3))

    r = np.linalg.norm(pts, axis=1)
    density = np.exp(-2.0 * r**2)

    bump_centers = np.array([
        [0.7, 0.3, 0.0], [0.8, -0.2, 0.1], [0.6, 0.0, 0.4],
        [0.9, 0.1, -0.2], [0.7, -0.1, -0.3], [0.5, 0.4, 0.2],
        [0.8, 0.2, -0.1], [0.6, -0.3, 0.1], [0.75, 0.15, 0.25],
        [0.65, -0.15, -0.15], [0.85, 0.0, 0.0], [0.55, 0.25, -0.2],
    ])
    for bc in bump_centers:
        d = np.linalg.norm(pts - bc, axis=1)
        density += 0.6 * np.exp(-25.0 * d**2)

    return pts, density


print("Generating target field (50K points)...")
sample_pts, target_density = make_target_samples()
print(f"  Target range: [{target_density.min():.4f}, {target_density.max():.4f}]")


# ── Morton code (Z-order curve) for 3D → 1D mapping ──────────────────
def interleave_bits_3d(x, y, z, bits=21):
    """
    Interleave bits of x, y, z to form a 63-bit Morton code.
    x, y, z are unsigned integers in [0, 2^bits).
    """
    code = np.zeros(len(x), dtype=np.uint64)
    for b in range(bits):
        bx = ((x >> b) & 1).astype(np.uint64)
        by = ((y >> b) & 1).astype(np.uint64)
        bz = ((z >> b) & 1).astype(np.uint64)
        code |= (bx << (3 * b)) | (by << (3 * b + 1)) | (bz << (3 * b + 2))
    return code


def morton_encode_3d(positions, bounds=(-1.5, 1.5), bits=21):
    """
    Map 3D float positions to Morton codes (Z-order curve).
    Quantizes to 2^bits levels per axis then interleaves bits.
    """
    lo, hi = bounds
    n_levels = (1 << bits) - 1
    # Normalize to [0, 1]
    norm = (positions - lo) / (hi - lo)
    norm = np.clip(norm, 0.0, 1.0)
    # Quantize
    ix = (norm[:, 0] * n_levels).astype(np.uint64)
    iy = (norm[:, 1] * n_levels).astype(np.uint64)
    iz = (norm[:, 2] * n_levels).astype(np.uint64)
    return interleave_bits_3d(ix, iy, iz, bits)


# ── 3D Gaussian density primitives ────────────────────────────────────
def eval_density(pts, mu, log_sigma, w):
    """
    Evaluate density field: sum_i w_i * exp(-||x - mu_i||^2 / (2*sigma_i^2))

    Chunked to avoid OOM with 50K samples x 1500 Gaussians.
    """
    N = len(pts)
    K = len(mu)
    pred = np.zeros(N)

    CHUNK = 5000  # process in chunks to limit memory
    for start in range(0, N, CHUNK):
        end = min(start + CHUNK, N)
        p = pts[start:end]  # (chunk, 3)
        sigma = np.exp(log_sigma)
        diff = p[:, None, :] - mu[None, :, :]  # (chunk, K, 3)
        sq_dist = np.sum(diff**2, axis=2)       # (chunk, K)
        gauss = np.exp(-sq_dist / (2.0 * sigma[None, :]**2))  # (chunk, K)
        pred[start:end] = (gauss * w[None, :]).sum(axis=1)

    return pred


def eval_density_with_grads(pts, mu, log_sigma, w):
    """MSE loss and analytical gradients. Chunked for memory."""
    N = len(pts)
    K = len(mu)
    sigma = np.exp(log_sigma)

    pred = np.zeros(N)
    grad_mu = np.zeros((K, 3))
    grad_ls = np.zeros(K)
    grad_w = np.zeros(K)

    target = target_density  # global

    CHUNK = 5000
    for start in range(0, N, CHUNK):
        end = min(start + CHUNK, N)
        p = pts[start:end]
        t = target[start:end]
        cn = end - start

        diff = p[:, None, :] - mu[None, :, :]  # (cn, K, 3)
        sq_dist = np.sum(diff**2, axis=2)
        gauss = np.exp(-sq_dist / (2.0 * sigma[None, :]**2))
        chunk_pred = (gauss * w[None, :]).sum(axis=1)
        pred[start:end] = chunk_pred

        residual = chunk_pred - t
        common = (2.0 / N) * residual[:, None] * gauss  # (cn, K)

        grad_w += common.sum(axis=0)

        for d in range(3):
            grad_mu[:, d] += (common * w[None, :] * diff[:, :, d] / (sigma[None, :]**2)).sum(axis=0)

        grad_ls += (common * w[None, :] * sq_dist / (sigma[None, :]**2)).sum(axis=0)

    mse = np.mean((pred - target)**2)
    return mse, grad_mu, grad_ls, grad_w, pred


# ── Adam optimizer ────────────────────────────────────────────────────
class Adam3D:
    def __init__(self, K, lr=LR):
        self.lr = lr
        self.beta1, self.beta2, self.eps = 0.9, 0.999, 1e-8
        self.t = 0
        self.m_mu = np.zeros((K, 3))
        self.v_mu = np.zeros((K, 3))
        self.m_ls = np.zeros(K)
        self.v_ls = np.zeros(K)
        self.m_w = np.zeros(K)
        self.v_w = np.zeros(K)

    def step(self, mu, log_sigma, w, grad_mu, grad_log_sigma, grad_w):
        self.t += 1
        bc1 = 1 - self.beta1**self.t
        bc2 = 1 - self.beta2**self.t

        self.m_mu = self.beta1 * self.m_mu + (1 - self.beta1) * grad_mu
        self.v_mu = self.beta2 * self.v_mu + (1 - self.beta2) * grad_mu**2
        mu_new = mu - self.lr * (self.m_mu / bc1) / (np.sqrt(self.v_mu / bc2) + self.eps)

        self.m_ls = self.beta1 * self.m_ls + (1 - self.beta1) * grad_log_sigma
        self.v_ls = self.beta2 * self.v_ls + (1 - self.beta2) * grad_log_sigma**2
        ls_new = log_sigma - self.lr * (self.m_ls / bc1) / (np.sqrt(self.v_ls / bc2) + self.eps)

        self.m_w = self.beta1 * self.m_w + (1 - self.beta1) * grad_w
        self.v_w = self.beta2 * self.v_w + (1 - self.beta2) * grad_w**2
        w_new = w - self.lr * (self.m_w / bc1) / (np.sqrt(self.v_w / bc2) + self.eps)

        return mu_new, ls_new, w_new

    def extend(self, n_new):
        self.m_mu = np.vstack([self.m_mu, np.zeros((n_new, 3))])
        self.v_mu = np.vstack([self.v_mu, np.zeros((n_new, 3))])
        self.m_ls = np.concatenate([self.m_ls, np.zeros(n_new)])
        self.v_ls = np.concatenate([self.v_ls, np.zeros(n_new)])
        self.m_w = np.concatenate([self.m_w, np.zeros(n_new)])
        self.v_w = np.concatenate([self.v_w, np.zeros(n_new)])


# ── Initialization ────────────────────────────────────────────────────
def init_gaussians_3d(K=INIT_K):
    """K x K x K grid of initial Gaussians in [-1, 1]^3."""
    g = np.linspace(-0.8, 0.8, K)
    GX, GY, GZ = np.meshgrid(g, g, g)
    mu = np.column_stack([GX.ravel(), GY.ravel(), GZ.ravel()])
    n = len(mu)
    log_sigma = np.full(n, np.log(0.35))
    w = np.full(n, 0.2)
    return mu, log_sigma, w


# ── Helper: local error around a 3D point ─────────────────────────────
def local_error_3d(pts, target, pred, query, radius=0.3):
    dists = np.linalg.norm(pts - query, axis=1)
    mask = dists < radius
    if mask.sum() < 5:
        return 0.0
    return np.mean((target[mask] - pred[mask])**2)


# ══════════════════════════════════════════════════════════════════════
# STRATEGY 1: Standard ADC (gradient-based 3D split)
# ══════════════════════════════════════════════════════════════════════
def train_adc():
    print("=" * 60)
    print("STRATEGY 1: Standard ADC (gradient-based 3D)")
    print("=" * 60)

    mu, log_sigma, w = init_gaussians_3d()
    K = len(mu)
    opt = Adam3D(K)

    mse_hist, cnt_hist = [], []
    grad_thresh = 0.00005

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w, pred = eval_density_with_grads(
            sample_pts, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)

        mse_hist.append(mse)
        cnt_hist.append(len(mu))

        if step % 1000 == 0:
            print(f"  step {step:5d}  MSE={mse:.8f}  K={len(mu)}")

        # Densify
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 500 and len(mu) < MAX_GAUSS:
            grad_mag = np.linalg.norm(grad_mu, axis=1)
            split_idx = np.where(grad_mag > grad_thresh)[0]

            if len(split_idx) > 0:
                budget = min((MAX_GAUSS - len(mu)) // 2, MAX_PER_ROUND)
                split_idx = split_idx[np.argsort(-grad_mag[split_idx])][:budget]

                sigma = np.exp(log_sigma)
                new_mu, new_ls, new_w = [], [], []

                for i in split_idx:
                    direction = grad_mu[i] / (np.linalg.norm(grad_mu[i]) + 1e-8)
                    offset = direction * sigma[i] * 0.5
                    new_mu.append(mu[i] - offset)
                    new_mu.append(mu[i] + offset)
                    shrink = np.log(0.7)
                    new_ls.extend([log_sigma[i] + shrink, log_sigma[i] + shrink])
                    new_w.extend([w[i] * 0.5, w[i] * 0.5])

                n_new = len(new_mu)
                mu = np.vstack([mu, np.array(new_mu)])
                log_sigma = np.concatenate([log_sigma, np.array(new_ls)])
                w = np.concatenate([w, np.array(new_w)])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  ADC DONE: {elapsed:.1f}s  Final MSE={mse_hist[-1]:.8f}  K={cnt_hist[-1]}")
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ══════════════════════════════════════════════════════════════════════
# STRATEGY 2: Direct Farey (3D Delaunay + mediant)
# ══════════════════════════════════════════════════════════════════════
def extract_delaunay_edges(simplices):
    edges = set()
    for simplex in simplices:
        n = len(simplex)
        for i in range(n):
            for j in range(i + 1, n):
                edges.add((min(simplex[i], simplex[j]),
                           max(simplex[i], simplex[j])))
    return edges


def train_farey_delaunay():
    print("=" * 60)
    print("STRATEGY 2: Direct Farey (3D Delaunay)")
    print("=" * 60)

    mu, log_sigma, w = init_gaussians_3d()
    K = len(mu)
    opt = Adam3D(K)

    mse_hist, cnt_hist = [], []
    farey_level = 2
    error_thresh = 0.0005

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w, pred = eval_density_with_grads(
            sample_pts, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)

        mse_hist.append(mse)
        cnt_hist.append(len(mu))

        if step % 1000 == 0:
            print(f"  step {step:5d}  MSE={mse:.8f}  K={len(mu)}")

        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 500 and len(mu) < MAX_GAUSS:
            farey_level += 1
            sigma = np.exp(log_sigma)
            budget = MAX_GAUSS - len(mu)
            candidates = []

            if len(mu) >= 5:
                try:
                    tri = Delaunay(mu)
                    edges = extract_delaunay_edges(tri.simplices)

                    for (i, j) in edges:
                        ri, rj = sigma[i], sigma[j]
                        dist = np.linalg.norm(mu[i] - mu[j])
                        d_edge = dist / (ri + rj + 1e-8)

                        if d_edge <= 1.0 or d_edge > farey_level:
                            continue

                        t_w = ri / (ri + rj + 1e-8)
                        p_new = mu[i] + t_w * (mu[j] - mu[i])

                        local_err = local_error_3d(sample_pts, target_density, pred, p_new)
                        if local_err < error_thresh:
                            continue

                        s_new = 0.35 * (sigma[i] + sigma[j])
                        w_new = 0.5 * (w[i] + w[j])
                        candidates.append((local_err, p_new, np.log(s_new), w_new))
                except Exception as e:
                    print(f"    Delaunay failed at step {step}: {e}")

            if candidates:
                candidates.sort(key=lambda c: -c[0])
                selected = candidates[:min(budget, MAX_PER_ROUND)]
                n_new = len(selected)
                mu = np.vstack([mu, np.array([c[1] for c in selected])])
                log_sigma = np.concatenate([log_sigma, np.array([c[2] for c in selected])])
                w = np.concatenate([w, np.array([c[3] for c in selected])])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  Farey-Delaunay DONE: {elapsed:.1f}s  Final MSE={mse_hist[-1]:.8f}  K={cnt_hist[-1]}")
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ══════════════════════════════════════════════════════════════════════
# STRATEGY 3: Hilbert+Farey (Morton curve → 1D Farey mediant)
# ══════════════════════════════════════════════════════════════════════
def hilbert_densify_farey(mu, log_sigma, w, pred, max_new=MAX_PER_ROUND, error_thresh=0.0005):
    """
    1. Compute Morton codes for all Gaussian centers
    2. Sort by Morton code → 1D ordering
    3. For consecutive pairs in 1D: compute gap metric
    4. Insert mediant (sigma-weighted) at largest gaps with high local error
    """
    K = len(mu)
    if K < 3:
        return np.zeros((0, 3)), np.zeros(0), np.zeros(0)

    sigma = np.exp(log_sigma)

    # Morton encoding
    codes = morton_encode_3d(mu)
    order = np.argsort(codes)

    candidates = []
    for idx in range(len(order) - 1):
        i = order[idx]
        j = order[idx + 1]

        # 3D gap
        dist = np.linalg.norm(mu[i] - mu[j])
        ri, rj = sigma[i], sigma[j]
        gap_ratio = dist / (ri + rj + 1e-8)

        # Only consider significant gaps (Farey admissibility)
        if gap_ratio <= 1.0 or gap_ratio > 20:
            continue

        # Farey mediant: sigma-weighted interpolation
        t_w = ri / (ri + rj + 1e-8)
        p_new = mu[i] + t_w * (mu[j] - mu[i])

        # Error gate
        local_err = local_error_3d(sample_pts, target_density, pred, p_new, radius=0.3)
        if local_err < error_thresh:
            continue

        s_new = 0.35 * (sigma[i] + sigma[j])
        w_new = 0.5 * (w[i] + w[j])

        candidates.append((local_err * gap_ratio, p_new, np.log(s_new), w_new))

    if not candidates:
        return np.zeros((0, 3)), np.zeros(0), np.zeros(0)

    candidates.sort(key=lambda c: -c[0])
    selected = candidates[:max_new]

    add_mu = np.array([c[1] for c in selected])
    add_ls = np.array([c[2] for c in selected])
    add_w = np.array([c[3] for c in selected])

    return add_mu, add_ls, add_w


def train_hilbert_farey():
    print("=" * 60)
    print("STRATEGY 3: Hilbert+Farey (Morton curve + mediant)")
    print("=" * 60)

    mu, log_sigma, w = init_gaussians_3d()
    K = len(mu)
    opt = Adam3D(K)

    mse_hist, cnt_hist = [], []

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w, pred = eval_density_with_grads(
            sample_pts, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)

        mse_hist.append(mse)
        cnt_hist.append(len(mu))

        if step % 1000 == 0:
            print(f"  step {step:5d}  MSE={mse:.8f}  K={len(mu)}")

        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 500 and len(mu) < MAX_GAUSS:
            budget = MAX_GAUSS - len(mu)
            add_mu, add_ls, add_w = hilbert_densify_farey(
                mu, log_sigma, w, pred,
                max_new=min(budget, MAX_PER_ROUND))

            if len(add_mu) > 0:
                n_new = len(add_mu)
                mu = np.vstack([mu, add_mu])
                log_sigma = np.concatenate([log_sigma, add_ls])
                w = np.concatenate([w, add_w])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  Hilbert+Farey DONE: {elapsed:.1f}s  Final MSE={mse_hist[-1]:.8f}  K={cnt_hist[-1]}")
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ══════════════════════════════════════════════════════════════════════
# STRATEGY 4: Hilbert+Bisection (control — midpoint instead of mediant)
# ══════════════════════════════════════════════════════════════════════
def hilbert_densify_bisection(mu, log_sigma, w, pred, max_new=MAX_PER_ROUND, error_thresh=0.0005):
    """Same as Hilbert+Farey but uses midpoint instead of sigma-weighted mediant."""
    K = len(mu)
    if K < 3:
        return np.zeros((0, 3)), np.zeros(0), np.zeros(0)

    sigma = np.exp(log_sigma)

    codes = morton_encode_3d(mu)
    order = np.argsort(codes)

    candidates = []
    for idx in range(len(order) - 1):
        i = order[idx]
        j = order[idx + 1]

        dist = np.linalg.norm(mu[i] - mu[j])
        ri, rj = sigma[i], sigma[j]
        gap_ratio = dist / (ri + rj + 1e-8)

        if gap_ratio <= 1.0 or gap_ratio > 20:
            continue

        # KEY DIFFERENCE: simple midpoint, not sigma-weighted mediant
        p_new = 0.5 * (mu[i] + mu[j])

        local_err = local_error_3d(sample_pts, target_density, pred, p_new, radius=0.3)
        if local_err < error_thresh:
            continue

        # Also use uniform scale/weight instead of weighted average
        s_new = 0.35 * (sigma[i] + sigma[j])
        w_new = 0.5 * (w[i] + w[j])

        candidates.append((local_err * gap_ratio, p_new, np.log(s_new), w_new))

    if not candidates:
        return np.zeros((0, 3)), np.zeros(0), np.zeros(0)

    candidates.sort(key=lambda c: -c[0])
    selected = candidates[:max_new]

    add_mu = np.array([c[1] for c in selected])
    add_ls = np.array([c[2] for c in selected])
    add_w = np.array([c[3] for c in selected])

    return add_mu, add_ls, add_w


def train_hilbert_bisection():
    print("=" * 60)
    print("STRATEGY 4: Hilbert+Bisection (control — midpoint)")
    print("=" * 60)

    mu, log_sigma, w = init_gaussians_3d()
    K = len(mu)
    opt = Adam3D(K)

    mse_hist, cnt_hist = [], []

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w, pred = eval_density_with_grads(
            sample_pts, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)

        mse_hist.append(mse)
        cnt_hist.append(len(mu))

        if step % 1000 == 0:
            print(f"  step {step:5d}  MSE={mse:.8f}  K={len(mu)}")

        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 500 and len(mu) < MAX_GAUSS:
            budget = MAX_GAUSS - len(mu)
            add_mu, add_ls, add_w = hilbert_densify_bisection(
                mu, log_sigma, w, pred,
                max_new=min(budget, MAX_PER_ROUND))

            if len(add_mu) > 0:
                n_new = len(add_mu)
                mu = np.vstack([mu, add_mu])
                log_sigma = np.concatenate([log_sigma, add_ls])
                w = np.concatenate([w, add_w])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  Hilbert+Bisection DONE: {elapsed:.1f}s  Final MSE={mse_hist[-1]:.8f}  K={cnt_hist[-1]}")
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ══════════════════════════════════════════════════════════════════════
# Test-set evaluation
# ══════════════════════════════════════════════════════════════════════
def evaluate_test(mu, log_sigma, w, label, n_test=10000):
    """Evaluate on fresh test points."""
    test_pts, test_density = make_target_samples(n=n_test, seed=999)
    pred = eval_density(test_pts, mu, log_sigma, w)
    mse = np.mean((pred - test_density)**2)

    # Per-region: smooth (center) vs detail (+x octant)
    smooth_mask = (np.linalg.norm(test_pts, axis=1) < 0.5) & (test_pts[:, 0] < 0.3)
    detail_mask = (test_pts[:, 0] > 0.4) & (np.linalg.norm(test_pts, axis=1) < 1.2)

    smooth_mse = np.mean((pred[smooth_mask] - test_density[smooth_mask])**2) if smooth_mask.sum() > 10 else 0
    detail_mse = np.mean((pred[detail_mask] - test_density[detail_mask])**2) if detail_mask.sum() > 10 else 0

    print(f"  {label} TEST: MSE={mse:.8f}  smooth={smooth_mse:.8f}  detail={detail_mse:.8f}  K={len(mu)}")
    return mse, smooth_mse, detail_mse


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    results = {}

    # Run all 4 strategies
    for name, train_fn in [
        ("ADC", train_adc),
        ("Farey-Delaunay", train_farey_delaunay),
        ("Hilbert+Farey", train_hilbert_farey),
        ("Hilbert+Bisection", train_hilbert_bisection),
    ]:
        print()
        mu, ls, w, mse_hist, cnt_hist, elapsed = train_fn()
        test_mse, smooth_mse, detail_mse = evaluate_test(mu, ls, w, name)
        results[name] = {
            "final_train_mse": float(mse_hist[-1]),
            "test_mse": float(test_mse),
            "test_smooth_mse": float(smooth_mse),
            "test_detail_mse": float(detail_mse),
            "final_K": int(cnt_hist[-1]),
            "time_s": float(elapsed),
            "mse_at_1000": float(mse_hist[999]) if len(mse_hist) >= 1000 else None,
            "mse_at_3000": float(mse_hist[2999]) if len(mse_hist) >= 3000 else None,
            "mse_at_5000": float(mse_hist[4999]) if len(mse_hist) >= 5000 else None,
        }
        print()

    # ── Summary ───────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)
    print(f"{'Method':<20} {'Test MSE':>12} {'Detail MSE':>12} {'K':>6} {'Time':>8}")
    print("-" * 70)
    for name in ["ADC", "Farey-Delaunay", "Hilbert+Farey", "Hilbert+Bisection"]:
        r = results[name]
        print(f"{name:<20} {r['test_mse']:>12.8f} {r['test_detail_mse']:>12.8f} {r['final_K']:>6d} {r['time_s']:>7.1f}s")

    # Kill-or-promote verdict
    hf = results["Hilbert+Farey"]["test_mse"]
    hb = results["Hilbert+Bisection"]["test_mse"]
    ratio = hb / hf if hf > 0 else 0

    print()
    print("=" * 70)
    print("KILL-OR-PROMOTE VERDICT")
    print("=" * 70)
    print(f"  Hilbert+Farey  MSE = {hf:.8f}")
    print(f"  Hilbert+Bisect MSE = {hb:.8f}")
    print(f"  Ratio (bisect/farey) = {ratio:.4f}")

    if ratio > 1.05:
        print(f"  >>> PROMOTE: Hilbert+Farey beats bisection by {(ratio-1)*100:.1f}%")
    elif ratio > 1.0:
        print(f"  >>> MARGINAL: Hilbert+Farey marginally better ({(ratio-1)*100:.1f}%) — needs more testing")
    else:
        print(f"  >>> KILL: Hilbert+Farey does NOT beat bisection. Mediant has no advantage in Hilbert ordering.")

    # Also compare against Farey-Delaunay
    fd = results["Farey-Delaunay"]["test_mse"]
    print()
    print(f"  vs Farey-Delaunay: Hilbert+Farey/Delaunay = {hf/fd:.4f}")
    if hf < fd:
        print(f"  >>> Hilbert routing FASTER than Delaunay (avoid O(n log n) tetrahedralization)")
    else:
        print(f"  >>> Delaunay still better — Hilbert curve loses too much spatial structure")

    adc = results["ADC"]["test_mse"]
    print(f"  vs ADC: best Farey variant / ADC = {min(hf, fd) / adc:.4f}")

    # Save results
    out_path = os.path.join(OUT_DIR, "hilbert_farey_3d_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    print("\nDONE.")
