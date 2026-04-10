#!/usr/bin/env python3
"""
Farey-Guided Densification vs Standard ADC for 3D Gaussian Splatting
=====================================================================
GPU-accelerated (MPS) benchmark — scaled up from the original demo.

Uses PyTorch on Apple MPS for all tensor operations.
Pure density-field matching with isotropic 3D Gaussians.

Target: Sphere with high-detail patch (12 small bumps in +x octant).

Two strategies:
  1. Standard ADC — split Gaussians with large position gradient magnitude
  2. Farey-guided — inject Gaussians at mediant positions in under-resolved
     Delaunay gaps, gated by local reconstruction error

Output: ~/Desktop/Farey-Local/experiments/3dgs_results/
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
MAX_GAUSS = 3000
INIT_K = 6            # 6x6x6 = 216 initial Gaussians
TOTAL_STEPS = 5000
DENSIFY_EVERY = 100
LR = 0.005
N_SAMPLE = 10000      # sample points for loss evaluation
N_TEST = 10000        # test set size

OUT = os.path.expanduser("~/Desktop/Farey-Local/experiments/3dgs_results")
os.makedirs(OUT, exist_ok=True)

torch.manual_seed(42)
np.random.seed(42)

# ── Target density field ──────────────────────────────────────────────
BUMP_CENTERS = torch.tensor([
    [0.7, 0.3, 0.0], [0.8, -0.2, 0.1], [0.6, 0.0, 0.4],
    [0.9, 0.1, -0.2], [0.7, -0.1, -0.3], [0.5, 0.4, 0.2],
    [0.8, 0.2, -0.1], [0.6, -0.3, 0.1], [0.75, 0.15, 0.25],
    [0.65, -0.15, -0.15], [0.85, 0.0, 0.0], [0.55, 0.25, -0.2],
], device=DEVICE, dtype=torch.float32)


def compute_target_density(pts):
    """Compute target density at given points (on device)."""
    r = torch.norm(pts, dim=1)
    density = torch.exp(-2.0 * r ** 2)
    for bc in BUMP_CENTERS:
        d = torch.norm(pts - bc.unsqueeze(0), dim=1)
        density = density + 0.6 * torch.exp(-25.0 * d ** 2)
    return density


# Pre-generate training samples
sample_pts = torch.rand(N_SAMPLE, 3, device=DEVICE) * 3.0 - 1.5
target_density = compute_target_density(sample_pts)


# ── 3D Gaussian density evaluation (fully vectorized, on GPU) ─────────
def eval_density(pts, mu, log_sigma, w):
    """
    Evaluate density field on device.
    pts: (N, 3), mu: (K, 3), log_sigma: (K,), w: (K,)
    Returns: pred (N,), gauss (N, K)
    """
    sigma = torch.exp(log_sigma)  # (K,)
    diff = pts.unsqueeze(1) - mu.unsqueeze(0)  # (N, K, 3)
    sq_dist = (diff ** 2).sum(dim=2)  # (N, K)
    exponent = -sq_dist / (2.0 * sigma.unsqueeze(0) ** 2)
    gauss = torch.exp(exponent)  # (N, K)
    pred = (gauss * w.unsqueeze(0)).sum(dim=1)  # (N,)
    return pred, gauss, diff, sigma, sq_dist


def compute_loss_and_grads(pts, target, mu, log_sigma, w):
    """MSE loss and analytical gradients (all on device)."""
    N = pts.shape[0]
    pred, gauss, diff, sigma, sq_dist = eval_density(pts, mu, log_sigma, w)
    residual = pred - target  # (N,)
    mse = (residual ** 2).mean()

    common = (2.0 / N) * residual.unsqueeze(1) * gauss  # (N, K)

    grad_w = common.sum(dim=0)  # (K,)

    # grad_mu: (K, 3) — note sign: diff = pts - mu, derivative flips sign
    weighted_common = common * w.unsqueeze(0)  # (N, K)
    # For each dim d: sum over N of weighted_common * diff[:,:,d] / sigma^2
    grad_mu = torch.zeros_like(mu)
    for d in range(3):
        grad_mu[:, d] = (weighted_common * diff[:, :, d] / (sigma.unsqueeze(0) ** 2)).sum(dim=0)

    # grad_log_sigma: (K,)
    grad_log_sigma = (weighted_common * sq_dist / (sigma.unsqueeze(0) ** 2)).sum(dim=0)

    return mse.item(), grad_mu, grad_log_sigma, grad_w


# ── Adam optimizer (GPU tensors) ──────────────────────────────────────
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
    log_sigma = torch.full((n,), float(np.log(0.35)), device=DEVICE)
    w = torch.full((n,), 0.3, device=DEVICE)
    return mu, log_sigma, w


# ── Standard ADC (3D, GPU) ───────────────────────────────────────────
def train_standard_adc():
    print("\n  Training Standard ADC (3D, GPU) ...")
    print(f"  Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, N_SAMPLE={N_SAMPLE}")
    mu, log_sigma, w = init_gaussians_3d()
    K = mu.shape[0]
    opt = AdamGPU(K)

    mse_hist, cnt_hist = [], []
    grad_thresh = 0.00005

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

        # Densify
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 500 and mu.shape[0] < MAX_GAUSS:
            grad_mag = torch.norm(grad_mu, dim=1)
            split_mask = grad_mag > grad_thresh
            split_idx = torch.where(split_mask)[0]

            if len(split_idx) > 0:
                budget = (MAX_GAUSS - mu.shape[0]) // 2
                # Sort by gradient magnitude descending
                sorted_idx = split_idx[torch.argsort(-grad_mag[split_idx])]
                sorted_idx = sorted_idx[:max(budget, 0)]

                if len(sorted_idx) > 0:
                    sigma = torch.exp(log_sigma)
                    directions = grad_mu[sorted_idx]
                    dir_norms = torch.norm(directions, dim=1, keepdim=True).clamp(min=1e-8)
                    directions = directions / dir_norms
                    offsets = directions * sigma[sorted_idx].unsqueeze(1) * 0.5

                    new_mu1 = mu[sorted_idx] - offsets
                    new_mu2 = mu[sorted_idx] + offsets
                    new_mu = torch.cat([new_mu1, new_mu2], dim=0)

                    shrink = float(np.log(0.7))
                    new_ls = torch.cat([
                        log_sigma[sorted_idx] + shrink,
                        log_sigma[sorted_idx] + shrink
                    ])
                    new_w = torch.cat([w[sorted_idx] * 0.5, w[sorted_idx] * 0.5])

                    n_new = new_mu.shape[0]
                    mu = torch.cat([mu, new_mu])
                    log_sigma = torch.cat([log_sigma, new_ls])
                    w = torch.cat([w, new_w])
                    opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  ADC done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ── Delaunay helpers (CPU, since scipy needs numpy) ───────────────────
def extract_delaunay_edges(simplices):
    edges = set()
    for simplex in simplices:
        n = len(simplex)
        for i in range(n):
            for j in range(i + 1, n):
                edges.add((min(simplex[i], simplex[j]),
                           max(simplex[i], simplex[j])))
    return edges


# ── Farey-guided 3D densification (GPU + CPU Delaunay) ────────────────
def train_farey():
    print("\n  Training Farey-guided (3D, GPU) ...")
    print(f"  Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, N_SAMPLE={N_SAMPLE}")
    mu, log_sigma, w = init_gaussians_3d()
    K = mu.shape[0]
    opt = AdamGPU(K)

    mse_hist, cnt_hist = [], []
    farey_level = 2
    error_thresh = 0.0005
    max_per_round = 40

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

        # Farey densification via Delaunay edges
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 500 and mu.shape[0] < MAX_GAUSS:
            farey_level += 1
            sigma = torch.exp(log_sigma)

            # Current prediction for error gating
            pred, _, _, _, _ = eval_density(sample_pts, mu, log_sigma, w)

            budget = MAX_GAUSS - mu.shape[0]
            candidates = []

            # Transfer to CPU for Delaunay
            mu_np = mu.detach().cpu().numpy()

            if len(mu_np) >= 5:
                try:
                    tri = Delaunay(mu_np)
                    edges = extract_delaunay_edges(tri.simplices)

                    sigma_np = sigma.detach().cpu().numpy()
                    pred_np = pred.detach().cpu().numpy()
                    target_np = target_density.detach().cpu().numpy()
                    pts_np = sample_pts.detach().cpu().numpy()
                    w_np = w.detach().cpu().numpy()

                    for (i, j) in edges:
                        ri, rj = sigma_np[i], sigma_np[j]
                        dist = np.linalg.norm(mu_np[i] - mu_np[j])

                        d_edge = dist / (ri + rj + 1e-8)

                        if d_edge <= 1.0 or d_edge > farey_level:
                            continue

                        t_w = ri / (ri + rj + 1e-8)
                        p_new = mu_np[i] + t_w * (mu_np[j] - mu_np[i])

                        # Local error in a sphere around candidate point
                        dists = np.linalg.norm(pts_np - p_new, axis=1)
                        mask = dists < 0.25
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

                add_mu = torch.tensor(
                    np.array([c[1] for c in selected]), dtype=torch.float32, device=DEVICE)
                add_ls = torch.tensor(
                    np.array([c[2] for c in selected]), dtype=torch.float32, device=DEVICE)
                add_w = torch.tensor(
                    np.array([c[3] for c in selected]), dtype=torch.float32, device=DEVICE)

                n_new = len(selected)
                mu = torch.cat([mu, add_mu])
                log_sigma = torch.cat([log_sigma, add_ls])
                w = torch.cat([w, add_w])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  Farey done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    return mu, log_sigma, w, mse_hist, cnt_hist, elapsed


# ── Evaluation ────────────────────────────────────────────────────────
def evaluate_on_test_set(mu, log_sigma, w, n_test=N_TEST):
    torch.manual_seed(999)
    test_pts = torch.rand(n_test, 3, device=DEVICE) * 3.0 - 1.5
    test_density = compute_target_density(test_pts)

    pred, _, _, _, _ = eval_density(test_pts, mu, log_sigma, w)
    mse = ((pred - test_density) ** 2).mean().item()

    # PSNR (treating density as signal, max ~1.6 for our field)
    max_val = test_density.max().item()
    psnr = 10 * np.log10(max_val ** 2 / (mse + 1e-12))

    # Per-region
    r = torch.norm(test_pts, dim=1)
    smooth_mask = (r < 0.5) & (test_pts[:, 0] < 0.3)
    detail_mask = test_pts[:, 0] > 0.4

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
def save_figures(mu_a, ls_a, w_a, mse_adc, cnt_adc,
                 mu_f, ls_f, w_f, mse_far, cnt_far,
                 time_adc, time_far, results):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  matplotlib not available, skipping figures.")
        return

    # Convert to numpy for plotting
    mu_a_np = mu_a.cpu().numpy()
    mu_f_np = mu_f.cpu().numpy()
    sigma_a_np = torch.exp(ls_a).cpu().numpy()
    sigma_f_np = torch.exp(ls_f).cpu().numpy()
    w_a_np = w_a.cpu().numpy()
    w_f_np = w_f.cpu().numpy()

    # 1) MSE over training (log scale)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].semilogy(mse_adc, label=f"Standard ADC (final {mse_adc[-1]:.6f})", lw=1.3, color="#e74c3c")
    axes[0].semilogy(mse_far, label=f"Farey-guided (final {mse_far[-1]:.6f})", lw=1.3, color="#2ecc71")
    axes[0].set_xlabel("Training step")
    axes[0].set_ylabel("MSE (log scale)")
    axes[0].set_title("Training MSE Over Time")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(cnt_adc, label=f"ADC (final {cnt_adc[-1]})", lw=1.3, color="#e74c3c")
    axes[1].plot(cnt_far, label=f"Farey (final {cnt_far[-1]})", lw=1.3, color="#2ecc71")
    axes[1].set_xlabel("Training step")
    axes[1].set_ylabel("# Gaussians")
    axes[1].set_title("Gaussian Count Over Training")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.suptitle(f"3D Gaussian Splatting Benchmark: Farey vs ADC\n"
                 f"MAX_GAUSS={MAX_GAUSS}, {TOTAL_STEPS} steps, {N_SAMPLE} samples, MPS GPU",
                 fontsize=13, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/training_curves.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 2) Summary bar chart
    fig, axes = plt.subplots(1, 5, figsize=(20, 5))
    methods = ["Standard\nADC", "Farey\nGuided"]
    colors = ["#e74c3c", "#2ecc71"]

    axes[0].bar(methods, [results["adc"]["test_mse"], results["farey"]["test_mse"]], color=colors)
    axes[0].set_title("Test MSE\n(lower = better)")
    axes[0].set_ylabel("MSE")

    axes[1].bar(methods, [results["adc"]["test_psnr"], results["farey"]["test_psnr"]], color=colors)
    axes[1].set_title("Test PSNR (dB)\n(higher = better)")
    axes[1].set_ylabel("PSNR")

    axes[2].bar(methods, [results["adc"]["final_gaussians"], results["farey"]["final_gaussians"]], color=colors)
    axes[2].set_title("Total Gaussians\n(fewer = better)")
    axes[2].set_ylabel("Count")

    axes[3].bar(methods, [time_adc, time_far], color=colors)
    axes[3].set_title("Training Time (s)\n(lower = better)")
    axes[3].set_ylabel("Seconds")

    # Efficiency: MSE per Gaussian
    eff_a = results["adc"]["test_mse"] / results["adc"]["final_gaussians"]
    eff_f = results["farey"]["test_mse"] / results["farey"]["final_gaussians"]
    axes[4].bar(methods, [eff_a, eff_f], color=colors)
    axes[4].set_title("MSE per Gaussian\n(lower = more efficient)")
    axes[4].set_ylabel("MSE / #Gauss")
    axes[4].ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

    fig.suptitle("3D Gaussian Splatting Benchmark: Summary", fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/summary_bars.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 3) 3D scatter (Gaussian positions)
    fig = plt.figure(figsize=(16, 7))

    ax1 = fig.add_subplot(121, projection='3d')
    # Subsample if too many
    n_plot = min(1000, len(mu_a_np))
    idx_a = np.random.choice(len(mu_a_np), n_plot, replace=False) if len(mu_a_np) > n_plot else np.arange(len(mu_a_np))
    sc1 = ax1.scatter(mu_a_np[idx_a, 0], mu_a_np[idx_a, 1], mu_a_np[idx_a, 2],
                       c=w_a_np[idx_a], cmap='RdYlBu_r', s=5, alpha=0.5, edgecolors='none')
    ax1.set_title(f"Standard ADC\n{len(mu_a_np)} Gaussians", fontsize=11)
    ax1.set_xlabel("X"); ax1.set_ylabel("Y"); ax1.set_zlabel("Z")
    plt.colorbar(sc1, ax=ax1, label="Weight", shrink=0.6)

    ax2 = fig.add_subplot(122, projection='3d')
    n_plot = min(1000, len(mu_f_np))
    idx_f = np.random.choice(len(mu_f_np), n_plot, replace=False) if len(mu_f_np) > n_plot else np.arange(len(mu_f_np))
    sc2 = ax2.scatter(mu_f_np[idx_f, 0], mu_f_np[idx_f, 1], mu_f_np[idx_f, 2],
                       c=w_f_np[idx_f], cmap='RdYlBu_r', s=5, alpha=0.5, edgecolors='none')
    ax2.set_title(f"Farey-Guided\n{len(mu_f_np)} Gaussians", fontsize=11)
    ax2.set_xlabel("X"); ax2.set_ylabel("Y"); ax2.set_zlabel("Z")
    plt.colorbar(sc2, ax=ax2, label="Weight", shrink=0.6)

    plt.tight_layout()
    fig.savefig(f"{OUT}/gaussian_positions_3d.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 4) X-axis density histogram
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].hist(mu_a_np[:, 0], bins=40, color="#e74c3c", alpha=0.7, label="ADC")
    axes[0].hist(mu_f_np[:, 0], bins=40, color="#2ecc71", alpha=0.7, label="Farey")
    axes[0].axvspan(0.4, 1.5, alpha=0.1, color="orange", label="Detail region")
    axes[0].set_xlabel("X position")
    axes[0].set_ylabel("# Gaussians")
    axes[0].set_title("Gaussian Distribution Along X-axis")
    axes[0].legend()

    # Per-region average sigma
    data_labels = ["ADC\nSmooth", "ADC\nDetail", "Farey\nSmooth", "Farey\nDetail"]
    smooth_a = mu_a_np[:, 0] <= 0.0
    detail_a = mu_a_np[:, 0] > 0.4
    smooth_f = mu_f_np[:, 0] <= 0.0
    detail_f = mu_f_np[:, 0] > 0.4
    data_vals = [
        sigma_a_np[smooth_a].mean() if smooth_a.sum() > 0 else 0,
        sigma_a_np[detail_a].mean() if detail_a.sum() > 0 else 0,
        sigma_f_np[smooth_f].mean() if smooth_f.sum() > 0 else 0,
        sigma_f_np[detail_f].mean() if detail_f.sum() > 0 else 0,
    ]
    bar_colors = ["#e74c3c", "#c0392b", "#2ecc71", "#27ae60"]
    axes[1].bar(data_labels, data_vals, color=bar_colors)
    axes[1].set_title("Average Scale by Region")
    axes[1].set_ylabel("Avg sigma")

    plt.tight_layout()
    fig.savefig(f"{OUT}/distribution_analysis.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  Saved figures to {OUT}/")


# ── Main ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("  3D Gaussian Splatting GPU Benchmark")
    print("  Farey-Guided Densification vs Standard ADC")
    print(f"  Device: {DEVICE}")
    print(f"  Config: MAX_GAUSS={MAX_GAUSS}, STEPS={TOTAL_STEPS}, SAMPLES={N_SAMPLE}")
    print(f"  Init: {INIT_K}^3 = {INIT_K**3} Gaussians")
    print("=" * 70)

    # Run both methods
    mu_a, ls_a, w_a, mse_adc, cnt_adc, time_adc = train_standard_adc()
    mu_f, ls_f, w_f, mse_far, cnt_far, time_far = train_farey()

    # Evaluate on test set
    test_mse_a, psnr_a, test_smooth_a, test_detail_a = evaluate_on_test_set(mu_a, ls_a, w_a)
    test_mse_f, psnr_f, test_smooth_f, test_detail_f = evaluate_on_test_set(mu_f, ls_f, w_f)

    dist_a = spatial_analysis(mu_a, ls_a)
    dist_f = spatial_analysis(mu_f, ls_f)

    # Build results dict
    results = {
        "config": {
            "device": str(DEVICE),
            "max_gaussians": MAX_GAUSS,
            "total_steps": TOTAL_STEPS,
            "n_sample": N_SAMPLE,
            "n_test": N_TEST,
            "init_grid": f"{INIT_K}^3={INIT_K**3}",
            "learning_rate": LR,
            "densify_every": DENSIFY_EVERY,
        },
        "adc": {
            "final_train_mse": mse_adc[-1],
            "test_mse": test_mse_a,
            "test_psnr": psnr_a,
            "test_mse_smooth": test_smooth_a,
            "test_mse_detail": test_detail_a,
            "final_gaussians": cnt_adc[-1],
            "training_time_s": round(time_adc, 1),
            "mse_per_gaussian": test_mse_a / cnt_adc[-1] if cnt_adc[-1] > 0 else 0,
            "spatial": dist_a,
        },
        "farey": {
            "final_train_mse": mse_far[-1],
            "test_mse": test_mse_f,
            "test_psnr": psnr_f,
            "test_mse_smooth": test_smooth_f,
            "test_mse_detail": test_detail_f,
            "final_gaussians": cnt_far[-1],
            "training_time_s": round(time_far, 1),
            "mse_per_gaussian": test_mse_f / cnt_far[-1] if cnt_far[-1] > 0 else 0,
            "spatial": dist_f,
        },
    }

    # Comparison metrics
    if test_mse_f < test_mse_a:
        results["comparison"] = {
            "winner_mse": "farey",
            "mse_improvement_pct": round((1 - test_mse_f / test_mse_a) * 100, 2),
            "psnr_improvement_db": round(psnr_f - psnr_a, 2),
        }
    else:
        results["comparison"] = {
            "winner_mse": "adc",
            "mse_improvement_pct": round((1 - test_mse_a / test_mse_f) * 100, 2),
            "psnr_improvement_db": round(psnr_a - psnr_f, 2),
        }

    eff_a = test_mse_a / cnt_adc[-1] if cnt_adc[-1] > 0 else 0
    eff_f = test_mse_f / cnt_far[-1] if cnt_far[-1] > 0 else 0
    if eff_f < eff_a and eff_f > 0:
        results["comparison"]["efficiency_ratio"] = round(eff_a / eff_f, 2)
        results["comparison"]["winner_efficiency"] = "farey"
    elif eff_a > 0:
        results["comparison"]["efficiency_ratio"] = round(eff_f / eff_a, 2)
        results["comparison"]["winner_efficiency"] = "adc"

    # Print results
    print(f"\n{'='*70}")
    print(f"  RESULTS: 3D Farey-Guided vs Standard ADC (GPU Benchmark)")
    print(f"{'='*70}")

    print(f"\n{'Metric':<40}  {'ADC':>12}  {'Farey':>12}")
    print("-" * 70)
    print(f"{'Final Train MSE':<40}  {mse_adc[-1]:>12.6f}  {mse_far[-1]:>12.6f}")
    print(f"{'Test MSE (full)':<40}  {test_mse_a:>12.6f}  {test_mse_f:>12.6f}")
    print(f"{'Test PSNR (dB)':<40}  {psnr_a:>12.2f}  {psnr_f:>12.2f}")
    print(f"{'Test MSE (smooth region)':<40}  {test_smooth_a:>12.6f}  {test_smooth_f:>12.6f}")
    print(f"{'Test MSE (detail region)':<40}  {test_detail_a:>12.6f}  {test_detail_f:>12.6f}")
    print(f"{'# Gaussians (final)':<40}  {cnt_adc[-1]:>12d}  {cnt_far[-1]:>12d}")
    print(f"{'Training time (s)':<40}  {time_adc:>12.1f}  {time_far:>12.1f}")
    print(f"{'MSE per Gaussian':<40}  {eff_a:>12.2e}  {eff_f:>12.2e}")
    print(f"{'Gaussians in detail (x>0.4)':<40}  {dist_a['n_detail']:>12d}  {dist_f['n_detail']:>12d}")
    print(f"{'Fraction in detail region':<40}  {dist_a['frac_detail']:>12.3f}  {dist_f['frac_detail']:>12.3f}")
    print(f"{'Avg sigma (smooth)':<40}  {dist_a['avg_sigma_smooth']:>12.4f}  {dist_f['avg_sigma_smooth']:>12.4f}")
    print(f"{'Avg sigma (detail)':<40}  {dist_a['avg_sigma_detail']:>12.4f}  {dist_f['avg_sigma_detail']:>12.4f}")

    print(f"\n  Winner (test MSE): {results['comparison']['winner_mse'].upper()}")
    print(f"  MSE improvement: {results['comparison']['mse_improvement_pct']:.2f}%")
    print(f"  PSNR improvement: {results['comparison']['psnr_improvement_db']:.2f} dB")
    if 'efficiency_ratio' in results['comparison']:
        print(f"  Efficiency winner: {results['comparison']['winner_efficiency'].upper()} "
              f"({results['comparison']['efficiency_ratio']:.2f}x)")

    # Save results JSON
    json_path = f"{OUT}/benchmark_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {json_path}")

    # Save figures
    print("\nGenerating figures ...")
    save_figures(mu_a, ls_a, w_a, mse_adc, cnt_adc,
                 mu_f, ls_f, w_f, mse_far, cnt_far,
                 time_adc, time_far, results)

    print("\n=== Benchmark Complete ===")
