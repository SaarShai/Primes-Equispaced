#!/usr/bin/env python3
"""
Farey-Guided Densification vs Standard ADC for 3D Gaussian Splatting
=====================================================================

Extends the validated 1D (33x) and 2D (2.4x) demos to 3D point cloud
density reconstruction. Uses isotropic 3D Gaussians (position, scale,
weight) with no rendering pipeline — pure density field matching.

Target: A sphere with a high-detail patch on one side (denser sampling
needed there), analogous to the 1D high-frequency burst and the 2D
checkerboard patch.

Two strategies compared:
  1. Standard ADC — split Gaussians with large gradient magnitude
  2. Farey-guided — inject Gaussians at mediant positions in under-resolved
     Delaunay gaps, gated by local reconstruction error

Uses pure NumPy + scipy.spatial.Delaunay.
"""

import numpy as np
from scipy.spatial import Delaunay, KDTree
import time

np.random.seed(42)

# ── Configuration ─────────────────────────────────────────────────────
MAX_GAUSS = 300
INIT_K = 4          # 4x4x4 = 64 initial Gaussians
TOTAL_STEPS = 2000
DENSIFY_EVERY = 150
LR = 0.008
N_SAMPLE = 2000     # sample points for loss evaluation

OUT = "/Users/saar/Library/CloudStorage/GoogleDrive-saar.shai@gmail.com/My Drive/Farey Folder/experiments"

# ── Target density field ──────────────────────────────────────────────
def make_target_samples():
    """
    Generate sample points from a 3D density field:
    - A unit sphere with smooth Gaussian density
    - A high-detail patch (small-scale bumps) in the +x octant

    Returns: positions (N,3), target_density (N,)
    """
    # Sample points uniformly in [-1.5, 1.5]^3
    pts = np.random.uniform(-1.5, 1.5, (N_SAMPLE, 3))

    # Base density: smooth sphere centered at origin, radius ~1
    r = np.linalg.norm(pts, axis=1)
    density = np.exp(-2.0 * r**2)

    # High-detail patch: multiple small Gaussian bumps in the +x octant
    # This creates a region that needs fine-grained coverage
    bump_centers = np.array([
        [0.7, 0.3, 0.0],
        [0.8, -0.2, 0.1],
        [0.6, 0.0, 0.4],
        [0.9, 0.1, -0.2],
        [0.7, -0.1, -0.3],
        [0.5, 0.4, 0.2],
        [0.8, 0.2, -0.1],
        [0.6, -0.3, 0.1],
        [0.75, 0.15, 0.25],
        [0.65, -0.15, -0.15],
        [0.85, 0.0, 0.0],
        [0.55, 0.25, -0.2],
    ])
    for bc in bump_centers:
        d = np.linalg.norm(pts - bc, axis=1)
        density += 0.6 * np.exp(-25.0 * d**2)

    return pts, density


# Pre-generate target
sample_pts, target_density = make_target_samples()


# ── 3D Gaussian density primitives ────────────────────────────────────
def eval_density(pts, mu, log_sigma, w):
    """
    Evaluate density field: sum_i w_i * exp(-||x - mu_i||^2 / (2*sigma_i^2))

    pts: (N, 3)
    mu: (K, 3)
    log_sigma: (K,) — isotropic scale (log)
    w: (K,) — weight

    Returns: (N,) density at each sample point
    """
    sigma = np.exp(log_sigma)  # (K,)
    # (N, K, 3)
    diff = pts[:, None, :] - mu[None, :, :]
    # (N, K)
    sq_dist = np.sum(diff**2, axis=2)
    exponent = -sq_dist / (2.0 * sigma[None, :]**2)
    gauss = np.exp(exponent)  # (N, K)
    pred = (gauss * w[None, :]).sum(axis=1)  # (N,)
    return pred, gauss, diff, sigma


def compute_loss_and_grads(pts, target, mu, log_sigma, w):
    """MSE loss and analytical gradients for 3D isotropic Gaussians."""
    N = len(pts)
    K = len(mu)
    pred, gauss, diff, sigma = eval_density(pts, mu, log_sigma, w)
    residual = pred - target  # (N,)
    mse = np.mean(residual**2)

    # Common factor: (2/N) * residual * gauss -> (N, K)
    common = (2.0 / N) * residual[:, None] * gauss  # (N, K)

    # d(MSE)/d(w_i)
    grad_w = common.sum(axis=0)  # (K,)

    # d(MSE)/d(mu_i) — vector gradient (K, 3)
    # diff = pts - mu, so d/d(mu) has a sign flip
    grad_mu = np.zeros((K, 3))
    for d in range(3):
        grad_mu[:, d] = (common * w[None, :] * diff[:, :, d] / sigma[None, :]**2).sum(axis=0)

    # d(MSE)/d(log_sigma_i)
    grad_log_sigma = (common * w[None, :] * sq_dist_from_cache(diff, sigma)).sum(axis=0)

    return mse, grad_mu, grad_log_sigma, grad_w


def sq_dist_from_cache(diff, sigma):
    """Compute sq_dist / sigma^2 for the log_sigma gradient."""
    # diff: (N, K, 3), sigma: (K,)
    sq_dist = np.sum(diff**2, axis=2)  # (N, K)
    return sq_dist / sigma[None, :]**2


# ── Adam optimizer (3D version) ───────────────────────────────────────
class Adam3D:
    def __init__(self, K, lr=LR):
        self.lr = lr
        self.beta1, self.beta2, self.eps = 0.9, 0.999, 1e-8
        self.t = 0
        # State for: mu (K,3), log_sigma (K,), w (K,)
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

        # mu (K,3)
        self.m_mu = self.beta1 * self.m_mu + (1 - self.beta1) * grad_mu
        self.v_mu = self.beta2 * self.v_mu + (1 - self.beta2) * grad_mu**2
        mu_new = mu - self.lr * (self.m_mu / bc1) / (np.sqrt(self.v_mu / bc2) + self.eps)

        # log_sigma (K,)
        self.m_ls = self.beta1 * self.m_ls + (1 - self.beta1) * grad_log_sigma
        self.v_ls = self.beta2 * self.v_ls + (1 - self.beta2) * grad_log_sigma**2
        ls_new = log_sigma - self.lr * (self.m_ls / bc1) / (np.sqrt(self.v_ls / bc2) + self.eps)

        # w (K,)
        self.m_w = self.beta1 * self.m_w + (1 - self.beta1) * grad_w
        self.v_w = self.beta2 * self.v_w + (1 - self.beta2) * grad_w**2
        w_new = w - self.lr * (self.m_w / bc1) / (np.sqrt(self.v_w / bc2) + self.eps)

        return mu_new, ls_new, w_new

    def extend(self, n_new):
        """Add zero-initialized state for n_new new Gaussians."""
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
    log_sigma = np.full(n, np.log(0.4))
    w = np.full(n, 0.3)
    return mu, log_sigma, w


# ── Standard ADC (3D) ─────────────────────────────────────────────────
def train_standard_adc():
    """Standard adaptive density control: split Gaussians with large position gradients."""
    print("  Training Standard ADC (3D) ...")
    mu, log_sigma, w = init_gaussians_3d()
    K = len(mu)
    opt = Adam3D(K)

    mse_hist, cnt_hist = [], []
    grad_thresh = 0.0001

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)

        mse_hist.append(mse)
        cnt_hist.append(len(mu))

        if step % 500 == 0:
            print(f"    step {step:4d}  MSE={mse:.6f}  K={len(mu)}")

        # Densify
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 300 and len(mu) < MAX_GAUSS:
            grad_mag = np.linalg.norm(grad_mu, axis=1)  # position gradient magnitude
            split_idx = np.where(grad_mag > grad_thresh)[0]

            if len(split_idx) > 0:
                budget = (MAX_GAUSS - len(mu)) // 2
                split_idx = split_idx[np.argsort(-grad_mag[split_idx])]
                split_idx = split_idx[:max(budget, 0)]

                sigma = np.exp(log_sigma)
                new_mu_list, new_ls_list, new_w_list = [], [], []

                for i in split_idx:
                    # Split along random direction (simplified)
                    direction = grad_mu[i] / (np.linalg.norm(grad_mu[i]) + 1e-8)
                    offset = direction * sigma[i] * 0.5

                    new_mu_list.append(mu[i] - offset)
                    new_mu_list.append(mu[i] + offset)
                    shrink = np.log(0.7)
                    new_ls_list.extend([log_sigma[i] + shrink, log_sigma[i] + shrink])
                    new_w_list.extend([w[i] * 0.5, w[i] * 0.5])

                n_new = len(new_mu_list)
                mu = np.vstack([mu, np.array(new_mu_list)])
                log_sigma = np.concatenate([log_sigma, np.array(new_ls_list)])
                w = np.concatenate([w, np.array(new_w_list)])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  ADC done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    return mu, log_sigma, w, mse_hist, cnt_hist


# ── Farey-guided 3D densification ─────────────────────────────────────
def extract_delaunay_edges(simplices):
    """Extract unique edges from Delaunay tetrahedra."""
    edges = set()
    for simplex in simplices:
        n = len(simplex)
        for i in range(n):
            for j in range(i + 1, n):
                edges.add((min(simplex[i], simplex[j]),
                           max(simplex[i], simplex[j])))
    return edges


def compute_local_error_3d(pts, target, pred, query_point, radius=0.3):
    """Compute MSE in a local sphere around query_point."""
    dists = np.linalg.norm(pts - query_point, axis=1)
    mask = dists < radius
    if mask.sum() < 3:
        return 0.0
    return np.mean((target[mask] - pred[mask])**2)


def train_farey():
    """
    Farey-guided 3D densification using Delaunay tetrahedralization.

    Generalizes the 2D approach:
    - Build 3D Delaunay on Gaussian centers
    - For each edge (i,j): compute gap metric d_edge = dist / (r_i + r_j)
    - Inject mediant Gaussian if d_edge admissible AND local error high
    - At most one injection per edge per round (Farey principle)
    """
    print("  Training Farey-guided (3D) ...")
    mu, log_sigma, w = init_gaussians_3d()
    K = len(mu)
    opt = Adam3D(K)

    mse_hist, cnt_hist = [], []
    farey_level = 2
    error_thresh = 0.001
    max_per_round = 20

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grad_mu, grad_ls, grad_w = compute_loss_and_grads(
            sample_pts, target_density, mu, log_sigma, w)
        mu, log_sigma, w = opt.step(mu, log_sigma, w, grad_mu, grad_ls, grad_w)

        mse_hist.append(mse)
        cnt_hist.append(len(mu))

        if step % 500 == 0:
            print(f"    step {step:4d}  MSE={mse:.6f}  K={len(mu)}")

        # Farey densification via Delaunay edges
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 300 and len(mu) < MAX_GAUSS:
            farey_level += 1
            sigma = np.exp(log_sigma)

            # Current prediction for error gating
            pred, _, _, _ = eval_density(sample_pts, mu, log_sigma, w)

            budget = MAX_GAUSS - len(mu)
            candidates = []

            # Build 3D Delaunay
            if len(mu) >= 5:  # need at least 5 points for 3D Delaunay
                try:
                    tri = Delaunay(mu)
                    edges = extract_delaunay_edges(tri.simplices)

                    for (i, j) in edges:
                        # Effective radii (isotropic, so just sigma)
                        ri, rj = sigma[i], sigma[j]
                        dist = np.linalg.norm(mu[i] - mu[j])

                        # Farey denominator: how many radii fit in the gap
                        d_edge = dist / (ri + rj + 1e-8)

                        # Admissibility: only inject if gap is within current level
                        if d_edge <= 1.0 or d_edge > farey_level:
                            continue

                        # Mediant-weighted position (sigma-weighted)
                        t_w = ri / (ri + rj + 1e-8)
                        p_new = mu[i] + t_w * (mu[j] - mu[i])

                        # Error gate: check local reconstruction quality
                        local_err = compute_local_error_3d(
                            sample_pts, target_density, pred, p_new, radius=0.3)
                        if local_err < error_thresh:
                            continue

                        # New Gaussian parameters
                        s_new = 0.35 * (sigma[i] + sigma[j])
                        w_new = 0.5 * (w[i] + w[j])

                        candidates.append((local_err, p_new, np.log(s_new), w_new))

                except Exception:
                    pass  # Delaunay can fail with degenerate configurations

            # Sort by error (highest first), inject top candidates
            if candidates:
                candidates.sort(key=lambda c: -c[0])
                selected = candidates[:min(budget, max_per_round)]

                add_mu = np.array([c[1] for c in selected])
                add_ls = np.array([c[2] for c in selected])
                add_w = np.array([c[3] for c in selected])

                n_new = len(selected)
                mu = np.vstack([mu, add_mu])
                log_sigma = np.concatenate([log_sigma, add_ls])
                w = np.concatenate([w, add_w])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  Farey done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    return mu, log_sigma, w, mse_hist, cnt_hist


# ── Evaluation metrics ────────────────────────────────────────────────
def evaluate_on_test_set(mu, log_sigma, w, n_test=5000):
    """Evaluate on fresh test points (not the training samples)."""
    np.random.seed(999)
    test_pts = np.random.uniform(-1.5, 1.5, (n_test, 3))
    # Recompute target density at test points
    r = np.linalg.norm(test_pts, axis=1)
    test_density = np.exp(-2.0 * r**2)

    bump_centers = np.array([
        [0.7, 0.3, 0.0], [0.8, -0.2, 0.1], [0.6, 0.0, 0.4],
        [0.9, 0.1, -0.2], [0.7, -0.1, -0.3], [0.5, 0.4, 0.2],
        [0.8, 0.2, -0.1], [0.6, -0.3, 0.1], [0.75, 0.15, 0.25],
        [0.65, -0.15, -0.15], [0.85, 0.0, 0.0], [0.55, 0.25, -0.2],
    ])
    for bc in bump_centers:
        d = np.linalg.norm(test_pts - bc, axis=1)
        test_density += 0.6 * np.exp(-25.0 * d**2)

    pred, _, _, _ = eval_density(test_pts, mu, log_sigma, w)
    mse = np.mean((pred - test_density)**2)

    # Per-region analysis
    # Smooth region: ||x|| < 0.5 and x[0] < 0.3
    smooth_mask = (np.linalg.norm(test_pts, axis=1) < 0.5) & (test_pts[:, 0] < 0.3)
    # Detail region: x[0] > 0.4
    detail_mask = test_pts[:, 0] > 0.4

    mse_smooth = np.mean((pred[smooth_mask] - test_density[smooth_mask])**2) if smooth_mask.sum() > 10 else 0
    mse_detail = np.mean((pred[detail_mask] - test_density[detail_mask])**2) if detail_mask.sum() > 10 else 0

    np.random.seed(42)  # restore seed
    return mse, mse_smooth, mse_detail


def spatial_distribution_analysis(mu, sigma_vals):
    """Analyze how Gaussians are distributed spatially."""
    # Count Gaussians in the detail region (x > 0.4) vs smooth region
    detail_mask = mu[:, 0] > 0.4
    smooth_mask = mu[:, 0] <= 0.0

    n_detail = detail_mask.sum()
    n_smooth = smooth_mask.sum()
    n_total = len(mu)

    avg_sigma_detail = sigma_vals[detail_mask].mean() if n_detail > 0 else 0
    avg_sigma_smooth = sigma_vals[smooth_mask].mean() if n_smooth > 0 else 0

    return {
        "total": n_total,
        "n_detail": int(n_detail),
        "n_smooth": int(n_smooth),
        "frac_detail": n_detail / n_total if n_total > 0 else 0,
        "avg_sigma_detail": avg_sigma_detail,
        "avg_sigma_smooth": avg_sigma_smooth,
    }


# ── Plotting ──────────────────────────────────────────────────────────
def save_figures(mu_a, ls_a, w_a, mse_adc, cnt_adc,
                 mu_f, ls_f, w_f, mse_far, cnt_far):
    """Generate and save comparison figures."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        print("  matplotlib not available, skipping figures.")
        return

    sigma_a = np.exp(ls_a)
    sigma_f = np.exp(ls_f)

    # 1) 3D scatter: Gaussian positions colored by weight
    fig = plt.figure(figsize=(16, 7))

    ax1 = fig.add_subplot(121, projection='3d')
    sc1 = ax1.scatter(mu_a[:, 0], mu_a[:, 1], mu_a[:, 2],
                       c=w_a, cmap='RdYlBu_r', s=15 * sigma_a / sigma_a.max(),
                       alpha=0.6, edgecolors='none')
    ax1.set_title(f"Standard ADC\n{len(mu_a)} Gaussians, MSE={mse_adc[-1]:.6f}", fontsize=11)
    ax1.set_xlabel("X"); ax1.set_ylabel("Y"); ax1.set_zlabel("Z")
    ax1.set_xlim(-1.5, 1.5); ax1.set_ylim(-1.5, 1.5); ax1.set_zlim(-1.5, 1.5)
    plt.colorbar(sc1, ax=ax1, label="Weight", shrink=0.6)

    ax2 = fig.add_subplot(122, projection='3d')
    sc2 = ax2.scatter(mu_f[:, 0], mu_f[:, 1], mu_f[:, 2],
                       c=w_f, cmap='RdYlBu_r', s=15 * sigma_f / sigma_f.max(),
                       alpha=0.6, edgecolors='none')
    ax2.set_title(f"Farey-Guided\n{len(mu_f)} Gaussians, MSE={mse_far[-1]:.6f}", fontsize=11)
    ax2.set_xlabel("X"); ax2.set_ylabel("Y"); ax2.set_zlabel("Z")
    ax2.set_xlim(-1.5, 1.5); ax2.set_ylim(-1.5, 1.5); ax2.set_zlim(-1.5, 1.5)
    plt.colorbar(sc2, ax=ax2, label="Weight", shrink=0.6)

    fig.suptitle("3D Gaussian Splatting: Farey-Guided vs Standard ADC\nGaussian Positions",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_3d_positions.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 2) MSE over training
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.semilogy(mse_adc, label=f"Standard ADC (final {mse_adc[-1]:.6f})", lw=1.3, color="#e74c3c")
    ax.semilogy(mse_far, label=f"Farey-guided (final {mse_far[-1]:.6f})", lw=1.3, color="#2ecc71")
    ax.set_xlabel("Training step")
    ax.set_ylabel("MSE (log scale)")
    ax.set_title("3D Density Reconstruction: MSE Over Training")
    ax.legend()
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_3d_mse.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 3) Gaussian count over training
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(cnt_adc, label=f"Standard ADC (final {cnt_adc[-1]})", lw=1.3, color="#e74c3c")
    ax.plot(cnt_far, label=f"Farey-guided (final {cnt_far[-1]})", lw=1.3, color="#2ecc71")
    ax.set_xlabel("Training step")
    ax.set_ylabel("# Gaussians")
    ax.set_title("Gaussian Count Over Training")
    ax.legend()
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_3d_count.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 4) Summary comparison
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    methods = ["Standard\nADC", "Farey\nGuided"]
    colors = ["#e74c3c", "#2ecc71"]

    axes[0].bar(methods, [mse_adc[-1], mse_far[-1]], color=colors)
    axes[0].set_title("Final MSE\n(lower = better)")
    axes[0].set_ylabel("MSE")

    axes[1].bar(methods, [cnt_adc[-1], cnt_far[-1]], color=colors)
    axes[1].set_title("Total Gaussians\n(fewer = better)")
    axes[1].set_ylabel("Count")

    eff_a = mse_adc[-1] / cnt_adc[-1] if cnt_adc[-1] > 0 else 0
    eff_f = mse_far[-1] / cnt_far[-1] if cnt_far[-1] > 0 else 0
    axes[2].bar(methods, [eff_a, eff_f], color=colors)
    axes[2].set_title("MSE per Gaussian\n(lower = more efficient)")
    axes[2].set_ylabel("MSE / #Gauss")

    # Spatial distribution: fraction in detail region
    dist_a = spatial_distribution_analysis(mu_a, sigma_a)
    dist_f = spatial_distribution_analysis(mu_f, sigma_f)
    axes[3].bar(methods, [dist_a["frac_detail"], dist_f["frac_detail"]], color=colors)
    axes[3].set_title("Fraction in Detail Region\n(higher = more adaptive)")
    axes[3].set_ylabel("Fraction (x > 0.4)")

    fig.suptitle("3D Farey-Guided Densification: Summary", fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_3d_summary.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 5) X-axis density histogram (shows spatial adaptation)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].hist(mu_a[:, 0], bins=30, color="#e74c3c", alpha=0.7, label="ADC")
    axes[0].hist(mu_f[:, 0], bins=30, color="#2ecc71", alpha=0.7, label="Farey")
    axes[0].axvspan(0.4, 1.5, alpha=0.1, color="orange", label="Detail region")
    axes[0].set_xlabel("X position")
    axes[0].set_ylabel("# Gaussians")
    axes[0].set_title("Gaussian Distribution Along X-axis")
    axes[0].legend()

    # Scale distribution by region
    ax_detail = axes[1]
    detail_mask_a = mu_a[:, 0] > 0.4
    detail_mask_f = mu_f[:, 0] > 0.4
    smooth_mask_a = mu_a[:, 0] <= 0.0
    smooth_mask_f = mu_f[:, 0] <= 0.0

    data_labels = ["ADC\nSmooth", "ADC\nDetail", "Farey\nSmooth", "Farey\nDetail"]
    data_vals = [
        sigma_a[smooth_mask_a].mean() if smooth_mask_a.sum() > 0 else 0,
        sigma_a[detail_mask_a].mean() if detail_mask_a.sum() > 0 else 0,
        sigma_f[smooth_mask_f].mean() if smooth_mask_f.sum() > 0 else 0,
        sigma_f[detail_mask_f].mean() if detail_mask_f.sum() > 0 else 0,
    ]
    bar_colors = ["#e74c3c", "#c0392b", "#2ecc71", "#27ae60"]
    ax_detail.bar(data_labels, data_vals, color=bar_colors)
    ax_detail.set_title("Average Scale by Region")
    ax_detail.set_ylabel("Avg sigma")

    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_3d_distribution.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  Saved figures to {OUT}/farey_3dgs_3d_*.png")


# ── Main ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print("  3D Gaussian Splatting: Farey-guided vs Standard ADC")
    print("  Target: Sphere with high-detail patch (density field)")
    print("=" * 65)

    # Run both methods
    mu_a, ls_a, w_a, mse_adc, cnt_adc = train_standard_adc()
    mu_f, ls_f, w_f, mse_far, cnt_far = train_farey()

    # ── Metrics ───────────────────────────────────────────────────
    mse_adc_final = mse_adc[-1]
    mse_far_final = mse_far[-1]

    eff_adc = mse_adc_final / cnt_adc[-1] if cnt_adc[-1] > 0 else 0
    eff_far = mse_far_final / cnt_far[-1] if cnt_far[-1] > 0 else 0

    # Test set evaluation
    test_mse_a, test_smooth_a, test_detail_a = evaluate_on_test_set(mu_a, ls_a, w_a)
    test_mse_f, test_smooth_f, test_detail_f = evaluate_on_test_set(mu_f, ls_f, w_f)

    # Spatial distribution
    sigma_a = np.exp(ls_a)
    sigma_f = np.exp(ls_f)
    dist_a = spatial_distribution_analysis(mu_a, sigma_a)
    dist_f = spatial_distribution_analysis(mu_f, sigma_f)

    print(f"\n{'='*65}")
    print(f"  RESULTS: 3D Farey-Guided vs Standard ADC")
    print(f"{'='*65}")

    print(f"\n{'Metric':<35}  {'ADC':>12}  {'Farey':>12}")
    print("-" * 65)
    print(f"{'Final Train MSE':<35}  {mse_adc_final:>12.6f}  {mse_far_final:>12.6f}")
    print(f"{'Test MSE (full)':<35}  {test_mse_a:>12.6f}  {test_mse_f:>12.6f}")
    print(f"{'Test MSE (smooth region)':<35}  {test_smooth_a:>12.6f}  {test_smooth_f:>12.6f}")
    print(f"{'Test MSE (detail region)':<35}  {test_detail_a:>12.6f}  {test_detail_f:>12.6f}")
    print(f"{'# Gaussians':<35}  {cnt_adc[-1]:>12d}  {cnt_far[-1]:>12d}")
    print(f"{'MSE / Gaussian':<35}  {eff_adc:>12.8f}  {eff_far:>12.8f}")
    print(f"{'Gaussians in detail (x>0.4)':<35}  {dist_a['n_detail']:>12d}  {dist_f['n_detail']:>12d}")
    print(f"{'Fraction in detail region':<35}  {dist_a['frac_detail']:>12.3f}  {dist_f['frac_detail']:>12.3f}")
    print(f"{'Avg sigma (smooth)':<35}  {dist_a['avg_sigma_smooth']:>12.4f}  {dist_f['avg_sigma_smooth']:>12.4f}")
    print(f"{'Avg sigma (detail)':<35}  {dist_a['avg_sigma_detail']:>12.4f}  {dist_f['avg_sigma_detail']:>12.4f}")

    if eff_far > 0 and eff_adc > 0:
        if eff_far < eff_adc:
            ratio = eff_adc / eff_far
            print(f"\n  -> Farey is {ratio:.1f}x more efficient per Gaussian")
        else:
            ratio = eff_far / eff_adc
            print(f"\n  -> ADC is {ratio:.1f}x more efficient per Gaussian")

    if test_mse_f < test_mse_a:
        pct = (1 - test_mse_f / test_mse_a) * 100
        print(f"  -> Farey achieves {pct:.1f}% lower test MSE")
    else:
        pct = (1 - test_mse_a / test_mse_f) * 100
        print(f"  -> ADC achieves {pct:.1f}% lower test MSE")

    # ── Figures ───────────────────────────────────────────────────
    print("\nSaving figures ...")
    save_figures(mu_a, ls_a, w_a, mse_adc, cnt_adc,
                 mu_f, ls_f, w_f, mse_far, cnt_far)

    print("\n=== Done ===")
