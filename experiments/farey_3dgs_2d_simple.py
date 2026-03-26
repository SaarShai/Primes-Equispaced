#!/usr/bin/env python3
"""
Farey-Guided 2D Gaussian Splatting (Simple Version)
====================================================

2D extension of the 1D Farey-vs-ADC demo.

Target: 128x128 image with a smooth gradient background and a sharp-edged
40x40 square in the centre (Gaussian-blurred edges).

Gaussians: isotropic only (mu_x, mu_y, sigma, weight).
Optimiser: Adam with analytical gradients (pure NumPy).

Two strategies compared:
  1. Standard ADC: split high-gradient Gaussians
  2. Farey 2D (tensor product): insert mediants into x/y gaps with high error
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

np.random.seed(42)

# ── target image ────────────────────────────────────────────────────
IMG_SIZE = 128
SQUARE_SIZE = 40

def make_target():
    """Smooth gradient + sharp square with blurred edges."""
    y_coords, x_coords = np.mgrid[0:IMG_SIZE, 0:IMG_SIZE]
    # normalise to [0, 1]
    xn = x_coords / (IMG_SIZE - 1)
    yn = y_coords / (IMG_SIZE - 1)

    # smooth radial gradient background (value 0 to 0.3)
    bg = 0.3 * np.sqrt((xn - 0.5)**2 + (yn - 0.5)**2) / 0.7071

    # sharp square mask
    cx, cy = IMG_SIZE // 2, IMG_SIZE // 2
    half = SQUARE_SIZE // 2
    mask = np.zeros((IMG_SIZE, IMG_SIZE))
    mask[cy - half:cy + half, cx - half:cx + half] = 1.0

    # blur edges slightly
    mask = gaussian_filter(mask, sigma=2.0)

    return bg + 0.7 * mask

target = make_target()

# pixel coordinates (normalised to [0, 1])
px = np.arange(IMG_SIZE, dtype=np.float64) / (IMG_SIZE - 1)
py = np.arange(IMG_SIZE, dtype=np.float64) / (IMG_SIZE - 1)
PX, PY = np.meshgrid(px, py)  # shape (H, W)
px_flat = PX.ravel()  # (H*W,)
py_flat = PY.ravel()


# ── 2D isotropic Gaussian rendering ────────────────────────────────

def render(mu_x, mu_y, log_sigma, w):
    """Render all Gaussians onto a flat pixel array.
    Returns shape (H*W,)."""
    sigma = np.exp(log_sigma)
    # diff_x: (N_pix, K), diff_y: (N_pix, K)
    dx = px_flat[:, None] - mu_x[None, :]
    dy = py_flat[:, None] - mu_y[None, :]
    gauss = np.exp(-(dx**2 + dy**2) / (2 * sigma**2))
    return (gauss * w).sum(axis=1)


def compute_gradients(mu_x, mu_y, log_sigma, w):
    """Analytical gradients of MSE w.r.t. all params."""
    N = IMG_SIZE * IMG_SIZE
    sigma = np.exp(log_sigma)
    dx = px_flat[:, None] - mu_x[None, :]
    dy = py_flat[:, None] - mu_y[None, :]
    r2 = dx**2 + dy**2
    gauss = np.exp(-r2 / (2 * sigma**2))
    pred = (gauss * w).sum(axis=1)
    residual = pred - target.ravel()

    res_col = residual[:, None]  # (N, 1)

    grad_w = (2.0 / N) * (res_col * gauss).sum(axis=0)
    grad_mx = (2.0 / N) * (res_col * w * gauss * dx / sigma**2).sum(axis=0)
    grad_my = (2.0 / N) * (res_col * w * gauss * dy / sigma**2).sum(axis=0)
    grad_ls = (2.0 / N) * (res_col * w * gauss * r2 / sigma**2).sum(axis=0)

    mse = np.mean(residual**2)
    return grad_mx, grad_my, grad_ls, grad_w, mse


# ── Adam optimiser ──────────────────────────────────────────────────

class Adam:
    def __init__(self, n, lr=0.005):
        self.lr = lr
        self.b1, self.b2, self.eps = 0.9, 0.999, 1e-8
        self.t = 0
        self.m = [np.zeros(n) for _ in range(4)]
        self.v = [np.zeros(n) for _ in range(4)]

    def step(self, params, grads):
        self.t += 1
        out = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * g**2
            mh = self.m[i] / (1 - self.b1**self.t)
            vh = self.v[i] / (1 - self.b2**self.t)
            out.append(p - self.lr * mh / (np.sqrt(vh) + self.eps))
        return out

    def extend(self, n_new):
        for i in range(4):
            self.m[i] = np.concatenate([self.m[i], np.zeros(n_new)])
            self.v[i] = np.concatenate([self.v[i], np.zeros(n_new)])


def init_params(grid_k=4):
    """Initialise K=grid_k^2 Gaussians on a regular grid."""
    gx = np.linspace(0.1, 0.9, grid_k)
    gy = np.linspace(0.1, 0.9, grid_k)
    mx, my = np.meshgrid(gx, gy)
    mu_x = mx.ravel()
    mu_y = my.ravel()
    K = len(mu_x)
    log_sigma = np.full(K, np.log(0.12))
    w = np.full(K, 0.01)
    return mu_x, mu_y, log_sigma, w


# ── Standard ADC ────────────────────────────────────────────────────

def train_adc(total_steps=1500, densify_every=100,
              grad_thresh=0.00005, lr=0.005, max_gauss=100):
    mu_x, mu_y, log_sigma, w = init_params(4)
    opt = Adam(len(mu_x), lr=lr)

    mse_hist, cnt_hist = [], []

    for step in range(1, total_steps + 1):
        g_mx, g_my, g_ls, g_w, mse = compute_gradients(mu_x, mu_y, log_sigma, w)
        [mu_x, mu_y, log_sigma, w] = opt.step(
            [mu_x, mu_y, log_sigma, w], [g_mx, g_my, g_ls, g_w])

        mse_hist.append(mse)
        cnt_hist.append(len(mu_x))

        if step % densify_every == 0 and step < total_steps - 200:
            if len(mu_x) >= max_gauss:
                continue
            grad_mag = np.sqrt(g_mx**2 + g_my**2)
            split_idx = np.where(grad_mag > grad_thresh)[0]

            if len(split_idx) > 0:
                sigma = np.exp(log_sigma)
                budget = (max_gauss - len(mu_x)) // 2
                split_idx = split_idx[:max(budget, 0)]

                new_mx, new_my, new_ls, new_w = [], [], [], []
                for i in split_idx:
                    # random direction offset
                    angle = np.random.uniform(0, 2 * np.pi)
                    off_x = sigma[i] * 0.5 * np.cos(angle)
                    off_y = sigma[i] * 0.5 * np.sin(angle)
                    for sign in [1, -1]:
                        new_mx.append(mu_x[i] + sign * off_x)
                        new_my.append(mu_y[i] + sign * off_y)
                        new_ls.append(log_sigma[i] + np.log(0.7))
                        new_w.append(w[i] * 0.5)

                n_new = len(new_mx)
                mu_x = np.concatenate([mu_x, np.array(new_mx)])
                mu_y = np.concatenate([mu_y, np.array(new_my)])
                log_sigma = np.concatenate([log_sigma, np.array(new_ls)])
                w = np.concatenate([w, np.array(new_w)])
                opt.extend(n_new)

        if step % 300 == 0 or step == total_steps:
            print(f"    ADC step {step:5d}  MSE={mse:.6f}  K={len(mu_x)}")

    return mu_x, mu_y, log_sigma, w, mse_hist, cnt_hist


# ── Farey 2D (tensor-product gap analysis) ──────────────────────────

def train_farey(total_steps=1500, densify_every=100,
                error_thresh=0.0001, lr=0.005, max_gauss=100):
    mu_x, mu_y, log_sigma, w = init_params(4)
    opt = Adam(len(mu_x), lr=lr)

    mse_hist, cnt_hist = [], []
    farey_level = 2

    for step in range(1, total_steps + 1):
        g_mx, g_my, g_ls, g_w, mse = compute_gradients(mu_x, mu_y, log_sigma, w)
        [mu_x, mu_y, log_sigma, w] = opt.step(
            [mu_x, mu_y, log_sigma, w], [g_mx, g_my, g_ls, g_w])

        mse_hist.append(mse)
        cnt_hist.append(len(mu_x))

        if step % densify_every == 0 and step < total_steps - 200:
            if len(mu_x) >= max_gauss:
                continue
            farey_level += 1
            sigma = np.exp(log_sigma)

            # Current prediction for local error
            pred_flat = render(mu_x, mu_y, log_sigma, w)
            err_img = (pred_flat - target.ravel())**2
            err_img = err_img.reshape(IMG_SIZE, IMG_SIZE)

            budget = max_gauss - len(mu_x)
            new_mx, new_my, new_ls, new_w = [], [], [], []

            # --- X-gap analysis (sort by x, find gaps) ---
            order_x = np.argsort(mu_x)
            mx_s = mu_x[order_x]
            my_s = mu_y[order_x]
            sig_s = sigma[order_x]
            w_s = w[order_x]
            ls_s = log_sigma[order_x]

            K = len(mu_x)
            for i in range(K - 1):
                if len(new_mx) >= budget:
                    break
                gap = mx_s[i + 1] - mx_s[i]
                sl, sr = sig_s[i], sig_s[i + 1]
                d_gap = gap / (sl + sr + 1e-8)

                if d_gap > farey_level or d_gap < 0.5:
                    continue

                # Check local error in the gap region
                x_lo = int(mx_s[i] * (IMG_SIZE - 1))
                x_hi = int(mx_s[i + 1] * (IMG_SIZE - 1))
                x_lo = max(0, x_lo)
                x_hi = min(IMG_SIZE - 1, x_hi)
                if x_hi <= x_lo:
                    continue
                gap_err = err_img[:, x_lo:x_hi + 1].mean()

                if gap_err < error_thresh:
                    continue

                # Mediant position (sigma-weighted)
                new_x = (sr * mx_s[i] + sl * mx_s[i + 1]) / (sl + sr)
                # y position: weighted average of the two neighbours
                new_y = (sr * my_s[i] + sl * my_s[i + 1]) / (sl + sr)
                new_sig = 0.5 * (sl + sr)
                new_weight = 0.5 * (w_s[i] + w_s[i + 1])

                new_mx.append(new_x)
                new_my.append(new_y)
                new_ls.append(np.log(new_sig))
                new_w.append(new_weight)

            # --- Y-gap analysis (sort by y, find gaps) ---
            if len(new_mx) < budget:
                order_y = np.argsort(mu_y)
                mx_sy = mu_x[order_y]
                my_sy = mu_y[order_y]
                sig_sy = sigma[order_y]
                w_sy = w[order_y]

                for i in range(K - 1):
                    if len(new_mx) >= budget:
                        break
                    gap = my_sy[i + 1] - my_sy[i]
                    sl, sr = sig_sy[i], sig_sy[i + 1]
                    d_gap = gap / (sl + sr + 1e-8)

                    if d_gap > farey_level or d_gap < 0.5:
                        continue

                    y_lo = int(my_sy[i] * (IMG_SIZE - 1))
                    y_hi = int(my_sy[i + 1] * (IMG_SIZE - 1))
                    y_lo = max(0, y_lo)
                    y_hi = min(IMG_SIZE - 1, y_hi)
                    if y_hi <= y_lo:
                        continue
                    gap_err = err_img[y_lo:y_hi + 1, :].mean()

                    if gap_err < error_thresh:
                        continue

                    new_y_pos = (sr * my_sy[i] + sl * my_sy[i + 1]) / (sl + sr)
                    new_x_pos = (sr * mx_sy[i] + sl * mx_sy[i + 1]) / (sl + sr)
                    new_sig = 0.5 * (sl + sr)
                    new_weight = 0.5 * (w_sy[i] + w_sy[i + 1])

                    new_mx.append(new_x_pos)
                    new_my.append(new_y_pos)
                    new_ls.append(np.log(new_sig))
                    new_w.append(new_weight)

            if new_mx:
                n_new = len(new_mx)
                mu_x = np.concatenate([mu_x, np.array(new_mx)])
                mu_y = np.concatenate([mu_y, np.array(new_my)])
                log_sigma = np.concatenate([log_sigma, np.array(new_ls)])
                w = np.concatenate([w, np.array(new_w)])
                opt.extend(n_new)

        if step % 300 == 0 or step == total_steps:
            print(f"    Farey step {step:5d}  MSE={mse:.6f}  K={len(mu_x)}")

    return mu_x, mu_y, log_sigma, w, mse_hist, cnt_hist


# ── run both ────────────────────────────────────────────────────────

OUT = "/Users/saar/Library/CloudStorage/GoogleDrive-saar.shai@gmail.com/My Drive/Farey Folder/experiments"

print("=" * 60)
print("  2D Gaussian Splatting: Farey-guided vs Standard ADC")
print("=" * 60)
print(f"  Image: {IMG_SIZE}x{IMG_SIZE}, target: gradient + {SQUARE_SIZE}x{SQUARE_SIZE} square")

print("\nTraining Standard ADC ...")
mx_a, my_a, ls_a, w_a, mse_adc, cnt_adc = train_adc()

print("\nTraining Farey-guided ...")
mx_f, my_f, ls_f, w_f, mse_far, cnt_far = train_farey()

# ── summary ─────────────────────────────────────────────────────────
eff_adc = mse_adc[-1] / max(cnt_adc[-1], 1)
eff_far = mse_far[-1] / max(cnt_far[-1], 1)

print(f"\n{'Metric':<30}  {'ADC':>12}  {'Farey':>12}")
print("-" * 58)
print(f"{'Final MSE':<30}  {mse_adc[-1]:>12.6f}  {mse_far[-1]:>12.6f}")
print(f"{'# Gaussians':<30}  {cnt_adc[-1]:>12d}  {cnt_far[-1]:>12d}")
print(f"{'MSE / Gaussian':<30}  {eff_adc:>12.8f}  {eff_far:>12.8f}")

if eff_far > 0 and eff_adc > 0:
    if eff_far < eff_adc:
        print(f"\n  -> Farey is {eff_adc/eff_far:.1f}x more efficient per Gaussian")
    else:
        print(f"\n  -> ADC is {eff_far/eff_adc:.1f}x more efficient per Gaussian")

# ── plotting ────────────────────────────────────────────────────────

# Render final images
img_adc = render(mx_a, my_a, ls_a, w_a).reshape(IMG_SIZE, IMG_SIZE)
img_far = render(mx_f, my_f, ls_f, w_f).reshape(IMG_SIZE, IMG_SIZE)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

# Row 0: images
axes[0, 0].imshow(target, cmap="viridis", vmin=0, vmax=1)
axes[0, 0].set_title("Target Image")
axes[0, 0].axis("off")

axes[0, 1].imshow(img_adc, cmap="viridis", vmin=0, vmax=1)
axes[0, 1].scatter(mx_a * (IMG_SIZE - 1), my_a * (IMG_SIZE - 1),
                   c="red", s=8, alpha=0.6, marker="x")
axes[0, 1].set_title(f"ADC ({cnt_adc[-1]} Gauss, MSE={mse_adc[-1]:.5f})")
axes[0, 1].axis("off")

axes[0, 2].imshow(img_far, cmap="viridis", vmin=0, vmax=1)
axes[0, 2].scatter(mx_f * (IMG_SIZE - 1), my_f * (IMG_SIZE - 1),
                   c="red", s=8, alpha=0.6, marker="x")
axes[0, 2].set_title(f"Farey ({cnt_far[-1]} Gauss, MSE={mse_far[-1]:.5f})")
axes[0, 2].axis("off")

# Row 1: error maps + convergence
err_adc = np.abs(target - img_adc)
err_far = np.abs(target - img_far)
vmax_err = max(err_adc.max(), err_far.max())

axes[1, 0].imshow(err_adc, cmap="hot", vmin=0, vmax=vmax_err)
axes[1, 0].set_title("ADC |error|")
axes[1, 0].axis("off")

axes[1, 1].imshow(err_far, cmap="hot", vmin=0, vmax=vmax_err)
axes[1, 1].set_title("Farey |error|")
axes[1, 1].axis("off")

# MSE convergence
axes[1, 2].semilogy(mse_adc, label=f"ADC (final {cnt_adc[-1]})", color="#e74c3c", lw=1.2)
axes[1, 2].semilogy(mse_far, label=f"Farey (final {cnt_far[-1]})", color="#2ecc71", lw=1.2)
axes[1, 2].set_xlabel("Step")
axes[1, 2].set_ylabel("MSE (log)")
axes[1, 2].set_title("Convergence")
axes[1, 2].legend(fontsize=8)

fig.suptitle("2D Gaussian Splatting: Farey-guided vs Standard ADC", fontsize=14)
plt.tight_layout()
fig.savefig(f"{OUT}/farey_3dgs_2d_comparison.png", dpi=150, bbox_inches="tight")
print(f"\nSaved: {OUT}/farey_3dgs_2d_comparison.png")
print("=== Done ===")
