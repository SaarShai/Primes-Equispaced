#!/usr/bin/env python3
"""
Farey-Guided Densification vs Standard ADC for 1D Gaussian Splatting
=====================================================================

Demonstrates that Farey-mediant injection controls densification better
than gradient-threshold splitting on a 1D signal reconstruction task.

Target signal has a smooth region and a high-frequency region, so an
ideal densification strategy should place more Gaussians only where
the signal has fine detail.

Uses pure NumPy with analytical gradients for speed.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(42)

# ── target signal ────────────────────────────────────────────────────
X_LO, X_HI = -1.0, 1.5
N_PTS = 500

x_eval = np.linspace(X_LO, X_HI, N_PTS)

def target_signal(x):
    smooth = np.sin(20 * x) * np.exp(-x ** 2)
    burst  = 0.5 * np.sin(50 * x) * ((x > 0.3) & (x < 0.7)).astype(float)
    return smooth + burst

y_true = target_signal(x_eval)

# ── 1-D Gaussian splatting primitives (numpy) ───────────────────────

def predict(x, mu, log_sigma, w):
    """g(x) = sum_i w_i * exp(-(x-mu_i)^2 / (2*sigma_i^2))"""
    sigma = np.exp(log_sigma)
    diff = x[:, None] - mu[None, :]
    gauss = np.exp(-diff**2 / (2 * sigma**2))
    return (gauss * w).sum(axis=1)

def compute_gradients(x, y, mu, log_sigma, w):
    """Analytical gradients of MSE w.r.t. mu, log_sigma, w."""
    N = len(x)
    sigma = np.exp(log_sigma)
    diff = x[:, None] - mu[None, :]
    gauss = np.exp(-diff**2 / (2 * sigma**2))
    pred = (gauss * w).sum(axis=1)
    residual = pred - y

    grad_w = (2.0 / N) * (residual[:, None] * gauss).sum(axis=0)
    grad_mu = (2.0 / N) * (residual[:, None] * w * gauss * diff / sigma**2).sum(axis=0)
    grad_log_sigma = (2.0 / N) * (residual[:, None] * w * gauss * diff**2 / sigma**2).sum(axis=0)

    return grad_mu, grad_log_sigma, grad_w, np.mean(residual**2)


# ── Adam optimiser ───────────────────────────────────────────────────
class AdamState:
    def __init__(self, n, lr=0.01):
        self.lr = lr
        self.beta1, self.beta2, self.eps = 0.9, 0.999, 1e-8
        self.t = 0
        self.m = [np.zeros(n) for _ in range(3)]
        self.v = [np.zeros(n) for _ in range(3)]

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
        """Add zero-initialised Adam state for n_new new parameters."""
        for i in range(3):
            self.m[i] = np.concatenate([self.m[i], np.zeros(n_new)])
            self.v[i] = np.concatenate([self.v[i], np.zeros(n_new)])


def init_params(K=10):
    mu = np.linspace(X_LO + 0.05, X_HI - 0.05, K)
    log_sigma = np.full(K, np.log(0.12))
    w = np.zeros(K)
    return mu, log_sigma, w


# ── Standard ADC (gradient-threshold splitting) ─────────────────────
def train_standard_adc(total_steps=2000, densify_every=100,
                       grad_thresh=0.0002, lr=0.01, max_gauss=60):
    mu, log_sigma, w = init_params(10)
    opt = AdamState(10, lr=lr)

    mse_hist, cnt_hist = [], []

    for step in range(1, total_steps + 1):
        g_mu, g_ls, g_w, mse = compute_gradients(x_eval, y_true, mu, log_sigma, w)
        [mu, log_sigma, w] = opt.step([mu, log_sigma, w], [g_mu, g_ls, g_w])

        mse_hist.append(mse)
        cnt_hist.append(len(mu))

        # densify every N steps, stop 200 steps before end to let params settle
        if step % densify_every == 0 and step < total_steps - 200:
            if len(mu) >= max_gauss:
                continue
            grad_mag = np.abs(g_mu)
            split_idx = np.where(grad_mag > grad_thresh)[0]

            if len(split_idx) > 0:
                sigma = np.exp(log_sigma)
                # budget: each split adds 2, so limit number of splits
                budget = (max_gauss - len(mu)) // 2
                split_idx = split_idx[:max(budget, 0)]

                new_mu, new_ls, new_w = [], [], []
                for i in split_idx:
                    offset = sigma[i] * 0.5
                    new_mu.extend([mu[i] - offset, mu[i] + offset])
                    new_ls.extend([log_sigma[i] + np.log(0.7), log_sigma[i] + np.log(0.7)])
                    new_w.extend([w[i] * 0.5, w[i] * 0.5])

                n_new = len(new_mu)
                mu = np.concatenate([mu, np.array(new_mu)])
                log_sigma = np.concatenate([log_sigma, np.array(new_ls)])
                w = np.concatenate([w, np.array(new_w)])
                opt.extend(n_new)

    return mu, log_sigma, w, mse_hist, cnt_hist


# ── Farey-guided densification ──────────────────────────────────────
def local_mse(x, y, mu, log_sigma, w, edges):
    """MSE in each interval between consecutive edges."""
    pred = predict(x, mu, log_sigma, w)
    errs = []
    for i in range(len(edges) - 1):
        mask = (x >= edges[i]) & (x < edges[i + 1])
        if mask.sum() == 0:
            errs.append(0.0)
        else:
            errs.append(np.mean((pred[mask] - y[mask])**2))
    return errs


def train_farey(total_steps=2000, densify_every=100,
                error_thresh=0.0003, lr=0.01, max_gauss=60):
    """
    Farey-guided densification.

    Key idea: instead of splitting every Gaussian with a large gradient,
    we look at *gaps* between adjacent Gaussians and only inject a new
    Gaussian into a gap when:
      (a) the gap's "Farey denominator" d_gap is admissible (d <= N), and
      (b) the reconstruction error in that gap exceeds a threshold.

    The denominator d_gap = gap_width / (sigma_L + sigma_R) measures how
    "resolved" the gap is — large d means the Gaussians are far apart
    relative to their widths, so the gap needs filling.

    The new Gaussian is placed at the *mediant* position weighted by widths.
    At most one Gaussian is injected per gap (Farey injection principle).
    """
    mu, log_sigma, w = init_params(10)
    opt = AdamState(10, lr=lr)

    mse_hist, cnt_hist = [], []
    farey_level = 2     # refinement level N — increases each round

    for step in range(1, total_steps + 1):
        g_mu, g_ls, g_w, mse = compute_gradients(x_eval, y_true, mu, log_sigma, w)
        [mu, log_sigma, w] = opt.step([mu, log_sigma, w], [g_mu, g_ls, g_w])

        mse_hist.append(mse)
        cnt_hist.append(len(mu))

        if step % densify_every == 0 and step < total_steps - 200:
            if len(mu) >= max_gauss:
                continue
            farey_level += 1
            sigma = np.exp(log_sigma)

            # sort by position
            order = np.argsort(mu)
            mu_s  = mu[order].copy()
            sig_s = sigma[order].copy()
            ls_s  = log_sigma[order].copy()
            w_s   = w[order].copy()

            K = len(mu_s)
            # interval edges at midpoints between adjacent Gaussians
            edges = [X_LO]
            for i in range(K - 1):
                edges.append(0.5 * (mu_s[i] + mu_s[i + 1]))
            edges.append(X_HI)

            loc_err = local_mse(x_eval, y_true, mu_s, ls_s, w_s, edges)

            budget = max_gauss - len(mu)
            add_mu, add_ls, add_w = [], [], []

            for i in range(K - 1):
                if len(add_mu) >= budget:
                    break

                sl, sr = sig_s[i], sig_s[i + 1]
                gap = mu_s[i + 1] - mu_s[i]

                # Farey denominator analog: how many sigma-widths fit in the gap.
                # Large d_gap => under-resolved region needing a new Gaussian.
                d_gap = gap / (sl + sr)

                # Farey admissibility: only inject if d_gap <= N
                # (higher N progressively admits finer gaps)
                if d_gap > farey_level:
                    continue

                # Error gate: only inject where reconstruction is poor
                gap_err = max(loc_err[i], loc_err[i + 1])
                if gap_err < error_thresh:
                    continue

                # Mediant-weighted position (sigma-weighted midpoint)
                mu_new  = (sr * mu_s[i] + sl * mu_s[i + 1]) / (sl + sr)
                sig_new = 0.5 * (sl + sr)
                w_new   = 0.5 * (w_s[i] + w_s[i + 1])

                add_mu.append(mu_new)
                add_ls.append(np.log(sig_new))
                add_w.append(w_new)

            if add_mu:
                n_new = len(add_mu)
                mu = np.concatenate([mu_s, np.array(add_mu)])
                log_sigma = np.concatenate([ls_s, np.array(add_ls)])
                w = np.concatenate([w_s, np.array(add_w)])
                opt.extend(n_new)

    return mu, log_sigma, w, mse_hist, cnt_hist


# ── run both ─────────────────────────────────────────────────────────
print("=" * 60)
print("  1D Gaussian Splatting: Farey-guided vs Standard ADC")
print("=" * 60)

print("\nTraining Standard ADC ...")
mu_a, ls_a, w_a, mse_adc, cnt_adc = train_standard_adc()
print(f"  Final MSE = {mse_adc[-1]:.6f}   Gaussians = {cnt_adc[-1]}")

print("\nTraining Farey-guided ...")
mu_f, ls_f, w_f, mse_far, cnt_far = train_farey()
print(f"  Final MSE = {mse_far[-1]:.6f}   Gaussians = {cnt_far[-1]}")

eff_adc = mse_adc[-1] / cnt_adc[-1]
eff_far = mse_far[-1] / cnt_far[-1]
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

# ── plotting ─────────────────────────────────────────────────────────
OUT = "/Users/saar/Library/CloudStorage/GoogleDrive-saar.shai@gmail.com/My Drive/Farey Folder/experiments"

y_adc = predict(x_eval, mu_a, ls_a, w_a)
y_far = predict(x_eval, mu_f, ls_f, w_f)

# 1) Reconstruction comparison
fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
for ax, y_hat, mus, label, n, mse_val in [
    (axes[0], y_adc, mu_a, "Standard ADC", cnt_adc[-1], mse_adc[-1]),
    (axes[1], y_far, mu_f, "Farey-guided", cnt_far[-1], mse_far[-1])
]:
    ax.plot(x_eval, y_true, "k-", lw=1.0, alpha=0.45, label="Target signal")
    ax.plot(x_eval, y_hat, "r-", lw=1.5,
            label=f"Reconstruction ({n} Gaussians, MSE={mse_val:.5f})")
    ax.scatter(mus, np.zeros_like(mus), marker="|", color="blue", s=100,
               zorder=5, label="Gaussian centres", linewidths=1.5)
    ax.axvspan(0.3, 0.7, alpha=0.07, color="orange", label="High-freq region")
    ax.set_ylabel("f(x)")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title(label, fontsize=12)

axes[1].set_xlabel("x")
fig.suptitle("1D Gaussian Splatting: Farey-guided vs Standard ADC", fontsize=14)
plt.tight_layout()
fig.savefig(f"{OUT}/farey_3dgs_1d_reconstruction.png", dpi=150, bbox_inches="tight")
print("\nSaved reconstruction figure.")

# 2) Gaussian count over training
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(cnt_adc, label=f"Standard ADC (final {cnt_adc[-1]})", lw=1.5, color="#e74c3c")
ax2.plot(cnt_far, label=f"Farey-guided (final {cnt_far[-1]})", lw=1.5, color="#2ecc71")
ax2.set_xlabel("Training step")
ax2.set_ylabel("# Gaussians")
ax2.set_title("Gaussian Count Over Training")
ax2.legend()
plt.tight_layout()
fig2.savefig(f"{OUT}/farey_3dgs_1d_count.png", dpi=150, bbox_inches="tight")
print("Saved count figure.")

# 3) MSE over training (log scale)
fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.semilogy(mse_adc, label="Standard ADC", lw=1.2, alpha=0.85, color="#e74c3c")
ax3.semilogy(mse_far, label="Farey-guided", lw=1.2, alpha=0.85, color="#2ecc71")
ax3.set_xlabel("Training step")
ax3.set_ylabel("MSE (log scale)")
ax3.set_title("Reconstruction Error Over Training")
ax3.legend()
plt.tight_layout()
fig3.savefig(f"{OUT}/farey_3dgs_1d_mse.png", dpi=150, bbox_inches="tight")
print("Saved MSE figure.")

# 4) Summary bar chart
fig4, axes4 = plt.subplots(1, 3, figsize=(12, 4))
methods = ["Standard\nADC", "Farey\nGuided"]
colors  = ["#e74c3c", "#2ecc71"]

axes4[0].bar(methods, [mse_adc[-1], mse_far[-1]], color=colors)
axes4[0].set_title("Final MSE (lower = better)")
axes4[0].set_ylabel("MSE")

axes4[1].bar(methods, [cnt_adc[-1], cnt_far[-1]], color=colors)
axes4[1].set_title("Total Gaussians (fewer = better)")
axes4[1].set_ylabel("Count")

axes4[2].bar(methods, [eff_adc, eff_far], color=colors)
axes4[2].set_title("MSE per Gaussian\n(lower = more efficient)")
axes4[2].set_ylabel("MSE / #Gauss")

fig4.suptitle("Farey-Guided Densification: Efficiency Comparison", fontsize=13)
plt.tight_layout()
fig4.savefig(f"{OUT}/farey_3dgs_1d_summary.png", dpi=150, bbox_inches="tight")
print("Saved summary figure.")

print("\n=== Done ===")
