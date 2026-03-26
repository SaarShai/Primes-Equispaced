#!/usr/bin/env python3
"""
Farey-Guided Densification vs Standard ADC for 2D Gaussian Splatting
=====================================================================

Extends the 1D demo to 2D image reconstruction. A 256x256 test image with
a smooth gradient background and a high-frequency checkerboard patch is
reconstructed using 2D Gaussians.

Two strategies are compared:
  1. Standard ADC — split Gaussians with large gradient magnitude
  2. Farey-guided — inject Gaussians at mediant positions in under-resolved
     gaps, gated by local reconstruction error (tensor-product per axis)

Uses pure NumPy with analytical gradients.
"""

import numpy as np
from scipy.spatial import Delaunay
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time

np.random.seed(42)

# ── constants ────────────────────────────────────────────────────────
IMG_SIZE = 256
MAX_GAUSS = 200
INIT_K = 5          # 5x5 = 25 initial Gaussians
TOTAL_STEPS = 3000
DENSIFY_EVERY = 200
LR = 0.005

OUT = "/Users/saar/Library/CloudStorage/GoogleDrive-saar.shai@gmail.com/My Drive/Farey Folder/experiments"

# ── target image ─────────────────────────────────────────────────────
def make_target_image(size=IMG_SIZE):
    """Smooth gradient + high-frequency checkerboard patch in [0.3,0.7]^2."""
    y_coords = np.linspace(0, 1, size)
    x_coords = np.linspace(0, 1, size)
    X, Y = np.meshgrid(x_coords, y_coords)

    # smooth gradient background
    img = 0.3 * np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y) + 0.5

    # high-frequency checkerboard in [0.3, 0.7] x [0.3, 0.7]
    freq = 24
    checker = 0.5 * (np.sign(np.sin(freq * np.pi * X) * np.sin(freq * np.pi * Y)) + 1)
    mask = ((X >= 0.3) & (X <= 0.7) & (Y >= 0.3) & (Y <= 0.7)).astype(float)
    img = img * (1 - mask) + checker * mask

    return img.astype(np.float64)


target = make_target_image()

# pixel grid coordinates (normalised to [0,1])
pix_y, pix_x = np.mgrid[0:IMG_SIZE, 0:IMG_SIZE]
pix_x = pix_x.astype(np.float64) / (IMG_SIZE - 1)
pix_y = pix_y.astype(np.float64) / (IMG_SIZE - 1)
pix_x_flat = pix_x.ravel()   # (N,)
pix_y_flat = pix_y.ravel()   # (N,)
target_flat = target.ravel()  # (N,)
N_PIX = IMG_SIZE * IMG_SIZE


# ── 2D Gaussian splatting primitives ─────────────────────────────────
def render_image(mu_x, mu_y, log_sx, log_sy, w, theta):
    """Render image as sum of 2D Gaussians (no rotation for speed).

    Each Gaussian: w_i * exp(-0.5 * ((x-mx)^2/sx^2 + (y-my)^2/sy^2))
    We ignore rotation (theta) in the render for simplicity — axis-aligned.
    """
    K = len(mu_x)
    sx = np.exp(log_sx)
    sy = np.exp(log_sy)

    # Vectorised: (N_PIX, K)
    dx = pix_x_flat[:, None] - mu_x[None, :]  # (N, K)
    dy = pix_y_flat[:, None] - mu_y[None, :]  # (N, K)

    exponent = -0.5 * (dx**2 / sx**2 + dy**2 / sy**2)
    gauss = np.exp(exponent)  # (N, K)

    pred = (gauss * w[None, :]).sum(axis=1)  # (N,)
    return pred, gauss, dx, dy, sx, sy


def compute_loss_and_grads(mu_x, mu_y, log_sx, log_sy, w, theta):
    """MSE loss and analytical gradients."""
    pred, gauss, dx, dy, sx, sy = render_image(mu_x, mu_y, log_sx, log_sy, w, theta)
    residual = pred - target_flat  # (N,)
    mse = np.mean(residual**2)

    # Common factor: (2/N) * residual * gauss  -> (N, K)
    common = (2.0 / N_PIX) * residual[:, None] * gauss  # (N, K)

    grad_w = (common).sum(axis=0)                            # (K,) -- d/dw
    grad_mu_x = (common * w[None, :] * dx / sx**2).sum(axis=0)   # d/d(mu_x)
    grad_mu_y = (common * w[None, :] * dy / sy**2).sum(axis=0)   # d/d(mu_y)
    grad_log_sx = (common * w[None, :] * dx**2 / sx**2).sum(axis=0)  # d/d(log_sx)
    grad_log_sy = (common * w[None, :] * dy**2 / sy**2).sum(axis=0)  # d/d(log_sy)

    return mse, [grad_mu_x, grad_mu_y, grad_log_sx, grad_log_sy, grad_w]


# ── Adam optimiser ───────────────────────────────────────────────────
class Adam:
    def __init__(self, n_params, lr=LR):
        self.lr = lr
        self.beta1, self.beta2, self.eps = 0.9, 0.999, 1e-8
        self.t = 0
        self.m = [np.zeros(n_params) for _ in range(5)]
        self.v = [np.zeros(n_params) for _ in range(5)]

    def step(self, params, grads):
        self.t += 1
        out = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g**2
            m_hat = self.m[i] / (1 - self.beta1**self.t)
            v_hat = self.v[i] / (1 - self.beta2**self.t)
            out.append(p - self.lr * m_hat / (np.sqrt(v_hat) + self.eps))
        return out

    def extend(self, n_new):
        for i in range(5):
            self.m[i] = np.concatenate([self.m[i], np.zeros(n_new)])
            self.v[i] = np.concatenate([self.v[i], np.zeros(n_new)])


def init_gaussians_2d(K=INIT_K):
    """K x K grid of initial Gaussians in [0,1]^2."""
    gx = np.linspace(0.1, 0.9, K)
    gy = np.linspace(0.1, 0.9, K)
    GX, GY = np.meshgrid(gx, gy)
    mu_x = GX.ravel()
    mu_y = GY.ravel()
    n = len(mu_x)
    log_sx = np.full(n, np.log(0.12))
    log_sy = np.full(n, np.log(0.12))
    w = np.full(n, 0.5)
    theta = np.zeros(n)
    return mu_x, mu_y, log_sx, log_sy, w, theta


# ── PSNR ─────────────────────────────────────────────────────────────
def psnr(mse_val, max_val=1.0):
    if mse_val < 1e-15:
        return 100.0
    return 10 * np.log10(max_val**2 / mse_val)


# ── Standard ADC ─────────────────────────────────────────────────────
def train_standard_adc():
    print("  Training Standard ADC ...")
    mu_x, mu_y, log_sx, log_sy, w, theta = init_gaussians_2d()
    K = len(mu_x)
    opt = Adam(K)

    mse_hist, cnt_hist = [], []
    grad_thresh = 0.00005

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grads = compute_loss_and_grads(mu_x, mu_y, log_sx, log_sy, w, theta)
        [mu_x, mu_y, log_sx, log_sy, w] = opt.step(
            [mu_x, mu_y, log_sx, log_sy, w], grads)

        # Clamp positions to [0,1]
        mu_x = np.clip(mu_x, 0, 1)
        mu_y = np.clip(mu_y, 0, 1)

        mse_hist.append(mse)
        cnt_hist.append(len(mu_x))

        if step % 500 == 0:
            print(f"    step {step:4d}  MSE={mse:.6f}  K={len(mu_x)}")

        # Densify
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 400 and len(mu_x) < MAX_GAUSS:
            grad_mag = np.sqrt(grads[0]**2 + grads[1]**2)  # position gradient magnitude
            split_idx = np.where(grad_mag > grad_thresh)[0]

            if len(split_idx) > 0:
                budget = (MAX_GAUSS - len(mu_x)) // 2
                # Sort by gradient magnitude, split the worst ones first
                split_idx = split_idx[np.argsort(-grad_mag[split_idx])]
                split_idx = split_idx[:max(budget, 0)]

                sx = np.exp(log_sx)
                sy = np.exp(log_sy)
                new_mx, new_my, new_lsx, new_lsy, new_w = [], [], [], [], []

                for i in split_idx:
                    # Split along axis of largest scale
                    if sx[i] >= sy[i]:
                        off_x, off_y = sx[i] * 0.5, 0
                    else:
                        off_x, off_y = 0, sy[i] * 0.5

                    new_mx.extend([mu_x[i] - off_x, mu_x[i] + off_x])
                    new_my.extend([mu_y[i] - off_y, mu_y[i] + off_y])
                    shrink = np.log(0.7)
                    new_lsx.extend([log_sx[i] + shrink, log_sx[i] + shrink])
                    new_lsy.extend([log_sy[i] + shrink, log_sy[i] + shrink])
                    new_w.extend([w[i] * 0.5, w[i] * 0.5])

                n_new = len(new_mx)
                mu_x = np.concatenate([mu_x, np.array(new_mx)])
                mu_y = np.concatenate([mu_y, np.array(new_my)])
                log_sx = np.concatenate([log_sx, np.array(new_lsx)])
                log_sy = np.concatenate([log_sy, np.array(new_lsy)])
                w = np.concatenate([w, np.array(new_w)])
                theta = np.concatenate([theta, np.zeros(n_new)])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  ADC done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    return mu_x, mu_y, log_sx, log_sy, w, theta, mse_hist, cnt_hist


# ── Farey-guided 2D densification (tensor product) ──────────────────
def compute_local_error_map(pred_flat, patch_size=16):
    """Compute per-patch MSE on a grid for error-gating."""
    pred_img = pred_flat.reshape(IMG_SIZE, IMG_SIZE)
    n_patches = IMG_SIZE // patch_size
    err_map = np.zeros((n_patches, n_patches))
    for py in range(n_patches):
        for px in range(n_patches):
            y0, y1 = py * patch_size, (py + 1) * patch_size
            x0, x1 = px * patch_size, (px + 1) * patch_size
            err_map[py, px] = np.mean((target[y0:y1, x0:x1] - pred_img[y0:y1, x0:x1])**2)
    return err_map


def get_patch_error(err_map, x_pos, y_pos, patch_size=16):
    """Look up error at a normalised (x,y) position."""
    n_patches = err_map.shape[0]
    px = min(int(x_pos * n_patches), n_patches - 1)
    py = min(int(y_pos * n_patches), n_patches - 1)
    return err_map[py, px]


def train_farey():
    """
    Farey-guided 2D densification using Delaunay triangulation.

    Key idea: The 2D generalization of "adjacent Gaussians" in 1D is the
    set of Delaunay edges. For each edge (i,j) in the Delaunay graph:
      - Compute the "Farey denominator" d_edge = dist(i,j) / (r_i + r_j)
        where r = sqrt(sx*sy) is the effective radius
      - Only inject a new Gaussian if d_edge <= farey_level (admissibility)
        AND the local reconstruction error at the midpoint is high
      - New Gaussian placed at sigma-weighted mediant position
      - At most one injection per edge (Farey injection principle)
    """
    print("  Training Farey-guided ...")
    mu_x, mu_y, log_sx, log_sy, w, theta = init_gaussians_2d()
    K = len(mu_x)
    opt = Adam(K)

    mse_hist, cnt_hist = [], []
    farey_level = 2
    error_thresh = 0.001
    max_per_round = 15

    t0 = time.time()
    for step in range(1, TOTAL_STEPS + 1):
        mse, grads = compute_loss_and_grads(mu_x, mu_y, log_sx, log_sy, w, theta)
        [mu_x, mu_y, log_sx, log_sy, w] = opt.step(
            [mu_x, mu_y, log_sx, log_sy, w], grads)

        mu_x = np.clip(mu_x, 0, 1)
        mu_y = np.clip(mu_y, 0, 1)

        mse_hist.append(mse)
        cnt_hist.append(len(mu_x))

        if step % 500 == 0:
            print(f"    step {step:4d}  MSE={mse:.6f}  K={len(mu_x)}")

        # Farey densification via Delaunay edges
        if step % DENSIFY_EVERY == 0 and step < TOTAL_STEPS - 400 and len(mu_x) < MAX_GAUSS:
            farey_level += 1
            sx = np.exp(log_sx)
            sy = np.exp(log_sy)

            # Current reconstruction for error map
            pred_flat, _, _, _, _, _ = render_image(mu_x, mu_y, log_sx, log_sy, w, theta)
            err_map = compute_local_error_map(pred_flat)

            budget = MAX_GAUSS - len(mu_x)
            candidates = []

            # Build Delaunay triangulation of Gaussian centres
            points = np.column_stack([mu_x, mu_y])
            if len(points) >= 4:
                try:
                    tri = Delaunay(points)
                    # Extract unique edges from simplices
                    edges = set()
                    for simplex in tri.simplices:
                        for k in range(3):
                            e = tuple(sorted((simplex[k], simplex[(k+1) % 3])))
                            edges.add(e)

                    for (i, j) in edges:
                        # Effective radii (geometric mean of scales)
                        ri = np.sqrt(sx[i] * sy[i])
                        rj = np.sqrt(sx[j] * sy[j])
                        dist = np.sqrt((mu_x[i] - mu_x[j])**2 + (mu_y[i] - mu_y[j])**2)

                        # Farey denominator: how many "radii" fit in the gap
                        d_edge = dist / (ri + rj + 1e-8)

                        # Admissibility: only inject if gap is resolvable at current level
                        if d_edge > farey_level:
                            continue

                        # Mediant-weighted position (sigma-weighted)
                        t_w = ri / (ri + rj + 1e-8)  # weight toward j (larger sigma of i => closer to j)
                        new_mx = mu_x[i] + t_w * (mu_x[j] - mu_x[i])
                        new_my = mu_y[i] + t_w * (mu_y[j] - mu_y[i])

                        # Error gate
                        local_err = get_patch_error(err_map, new_mx, new_my)
                        if local_err < error_thresh:
                            continue

                        # New Gaussian gets smaller scale — gap needs finer resolution
                        new_sx_val = 0.35 * (sx[i] + sx[j])
                        new_sy_val = 0.35 * (sy[i] + sy[j])
                        new_w_val = 0.5 * (w[i] + w[j])

                        candidates.append((local_err, new_mx, new_my,
                                          np.log(new_sx_val), np.log(new_sy_val), new_w_val))
                except Exception:
                    pass  # Delaunay can fail with degenerate configs

            # Sort by error (highest first), pick top candidates
            if candidates:
                candidates.sort(key=lambda c: -c[0])
                selected = candidates[:min(budget, max_per_round)]

                add_mx = np.array([c[1] for c in selected])
                add_my = np.array([c[2] for c in selected])
                add_lsx = np.array([c[3] for c in selected])
                add_lsy = np.array([c[4] for c in selected])
                add_w = np.array([c[5] for c in selected])

                n_new = len(selected)
                mu_x = np.concatenate([mu_x, add_mx])
                mu_y = np.concatenate([mu_y, add_my])
                log_sx = np.concatenate([log_sx, add_lsx])
                log_sy = np.concatenate([log_sy, add_lsy])
                w = np.concatenate([w, add_w])
                theta = np.concatenate([theta, np.zeros(n_new)])
                opt.extend(n_new)

    elapsed = time.time() - t0
    print(f"  Farey done in {elapsed:.1f}s  Final MSE={mse_hist[-1]:.6f}  K={cnt_hist[-1]}")
    return mu_x, mu_y, log_sx, log_sy, w, theta, mse_hist, cnt_hist


# ── SSIM (simplified) ───────────────────────────────────────────────
def ssim_simple(img1, img2, window_size=11):
    """Simplified SSIM using uniform window."""
    from numpy.lib.stride_tricks import sliding_window_view
    C1, C2 = 0.01**2, 0.03**2

    # Pad to handle edges
    pad = window_size // 2
    h, w_img = img1.shape

    ssim_map = np.zeros((h - 2*pad, w_img - 2*pad))
    for i in range(pad, h - pad):
        for j in range(pad, w_img - pad):
            win1 = img1[i-pad:i+pad+1, j-pad:j+pad+1]
            win2 = img2[i-pad:i+pad+1, j-pad:j+pad+1]
            mu1, mu2 = win1.mean(), win2.mean()
            s1, s2 = win1.var(), win2.var()
            s12 = ((win1 - mu1) * (win2 - mu2)).mean()
            ssim_map[i-pad, j-pad] = ((2*mu1*mu2 + C1)*(2*s12 + C2)) / \
                                      ((mu1**2 + mu2**2 + C1)*(s1 + s2 + C2))
    return ssim_map.mean()


# ── Main ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print("  2D Gaussian Splatting: Farey-guided vs Standard ADC")
    print("=" * 65)

    # Run both methods
    mx_a, my_a, lsx_a, lsy_a, w_a, th_a, mse_adc, cnt_adc = train_standard_adc()
    mx_f, my_f, lsx_f, lsy_f, w_f, th_f, mse_far, cnt_far = train_farey()

    # Render final images
    pred_adc, _, _, _, _, _ = render_image(mx_a, my_a, lsx_a, lsy_a, w_a, th_a)
    pred_far, _, _, _, _, _ = render_image(mx_f, my_f, lsx_f, lsy_f, w_f, th_f)
    img_adc = np.clip(pred_adc.reshape(IMG_SIZE, IMG_SIZE), 0, 1)
    img_far = np.clip(pred_far.reshape(IMG_SIZE, IMG_SIZE), 0, 1)

    # Metrics
    mse_adc_final = mse_adc[-1]
    mse_far_final = mse_far[-1]
    psnr_adc = psnr(mse_adc_final)
    psnr_far = psnr(mse_far_final)
    eff_adc = mse_adc_final / cnt_adc[-1]
    eff_far = mse_far_final / cnt_far[-1]

    print("\nComputing SSIM (this may take a moment)...")
    ssim_adc = ssim_simple(target, img_adc, window_size=7)
    ssim_far = ssim_simple(target, img_far, window_size=7)

    print(f"\n{'Metric':<25}  {'ADC':>12}  {'Farey':>12}")
    print("-" * 55)
    print(f"{'Final MSE':<25}  {mse_adc_final:>12.6f}  {mse_far_final:>12.6f}")
    print(f"{'PSNR (dB)':<25}  {psnr_adc:>12.2f}  {psnr_far:>12.2f}")
    print(f"{'SSIM':<25}  {ssim_adc:>12.4f}  {ssim_far:>12.4f}")
    print(f"{'# Gaussians':<25}  {cnt_adc[-1]:>12d}  {cnt_far[-1]:>12d}")
    print(f"{'MSE / Gaussian':<25}  {eff_adc:>12.8f}  {eff_far:>12.8f}")
    if eff_far > 0 and eff_adc > 0:
        if eff_far < eff_adc:
            print(f"\n  -> Farey is {eff_adc/eff_far:.1f}x more efficient per Gaussian")
        else:
            print(f"\n  -> ADC is {eff_far/eff_adc:.1f}x more efficient per Gaussian")

    # ── Figures ──────────────────────────────────────────────────────
    print("\nSaving figures ...")

    # 1) Target image
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(target, cmap="gray", vmin=0, vmax=1, origin="upper")
    ax.set_title("Target Image (256x256)\nSmooth gradient + checkerboard patch", fontsize=11)
    ax.axis("off")
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_2d_target.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 2) ADC reconstruction + Gaussian positions
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    axes[0].imshow(img_adc, cmap="gray", vmin=0, vmax=1, origin="upper")
    axes[0].set_title(f"Standard ADC Reconstruction\nMSE={mse_adc_final:.5f}  PSNR={psnr_adc:.1f}dB  K={cnt_adc[-1]}", fontsize=10)
    axes[0].axis("off")

    # Gaussian positions on target
    axes[1].imshow(target, cmap="gray", vmin=0, vmax=1, origin="upper", alpha=0.4)
    axes[1].scatter(mx_a * (IMG_SIZE-1), my_a * (IMG_SIZE-1),
                    s=8, c="red", alpha=0.7, edgecolors="none")
    axes[1].set_title(f"ADC Gaussian Positions ({cnt_adc[-1]} Gaussians)", fontsize=10)
    axes[1].set_xlim(0, IMG_SIZE-1)
    axes[1].set_ylim(IMG_SIZE-1, 0)
    axes[1].axis("off")
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_2d_adc.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 3) Farey reconstruction + Gaussian positions
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    axes[0].imshow(img_far, cmap="gray", vmin=0, vmax=1, origin="upper")
    axes[0].set_title(f"Farey-Guided Reconstruction\nMSE={mse_far_final:.5f}  PSNR={psnr_far:.1f}dB  K={cnt_far[-1]}", fontsize=10)
    axes[0].axis("off")

    axes[1].imshow(target, cmap="gray", vmin=0, vmax=1, origin="upper", alpha=0.4)
    axes[1].scatter(mx_f * (IMG_SIZE-1), my_f * (IMG_SIZE-1),
                    s=8, c="green", alpha=0.7, edgecolors="none")
    axes[1].set_title(f"Farey Gaussian Positions ({cnt_far[-1]} Gaussians)", fontsize=10)
    axes[1].set_xlim(0, IMG_SIZE-1)
    axes[1].set_ylim(IMG_SIZE-1, 0)
    axes[1].axis("off")
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_2d_farey.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 4) MSE over time
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.semilogy(mse_adc, label=f"Standard ADC (final {mse_adc_final:.5f})", lw=1.3, color="#e74c3c")
    ax.semilogy(mse_far, label=f"Farey-guided (final {mse_far_final:.5f})", lw=1.3, color="#2ecc71")
    ax.set_xlabel("Training step")
    ax.set_ylabel("MSE (log scale)")
    ax.set_title("2D Gaussian Splatting: Reconstruction Error Over Training")
    ax.legend()
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_2d_mse.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 5) Gaussian count over time
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(cnt_adc, label=f"Standard ADC (final {cnt_adc[-1]})", lw=1.3, color="#e74c3c")
    ax.plot(cnt_far, label=f"Farey-guided (final {cnt_far[-1]})", lw=1.3, color="#2ecc71")
    ax.set_xlabel("Training step")
    ax.set_ylabel("# Gaussians")
    ax.set_title("Gaussian Count Over Training")
    ax.legend()
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_2d_count.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 6) Combined comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(target, cmap="gray", vmin=0, vmax=1, origin="upper")
    axes[0].set_title("Target", fontsize=12)
    axes[0].axis("off")

    axes[1].imshow(img_adc, cmap="gray", vmin=0, vmax=1, origin="upper")
    axes[1].set_title(f"Standard ADC\nMSE={mse_adc_final:.5f}  K={cnt_adc[-1]}", fontsize=11)
    axes[1].axis("off")

    axes[2].imshow(img_far, cmap="gray", vmin=0, vmax=1, origin="upper")
    axes[2].set_title(f"Farey-Guided\nMSE={mse_far_final:.5f}  K={cnt_far[-1]}", fontsize=11)
    axes[2].axis("off")

    fig.suptitle("2D Gaussian Splatting: Farey-Guided vs Standard ADC", fontsize=14, y=1.02)
    plt.tight_layout()
    fig.savefig(f"{OUT}/farey_3dgs_2d_comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"\nSaved figures to {OUT}/farey_3dgs_2d_*.png")
    print("\n=== Done ===")
