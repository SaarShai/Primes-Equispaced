#!/usr/bin/env python3
"""
Fingerprint Density Identity Investigation
===========================================
Question: Is the r = -0.9963 correlation between d(p) and ΔW(p) TRIVIAL
(both scale with p) or STRUCTURAL (d(p) carries info beyond p)?

d(p) = (p-1)/(n-1)  where n = |F_{p-1}| = farey_size_p in the CSV
Asymptotically d(p) ~ π²/(3p), so d(p) is essentially ~1/p.

If ΔW also scales as ~1/p^α, the correlation is trivial.
We test this by removing the p-scaling and checking what remains.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# ── Load data ──────────────────────────────────────────────────────────
CSV = Path(__file__).parent / "wobble_primes_100000.csv"
df = pd.read_csv(CSV)
p = df['p'].values.astype(float)
dw = df['delta_w'].values.astype(float)
n = df['farey_size_p'].values.astype(float)
M = df['mertens_p'].values.astype(float)

# ── Compute fingerprint density ────────────────────────────────────────
d_p = (p - 1) / (n - 1)   # exact fingerprint density

# Also compute the asymptotic approximation
d_p_approx = np.pi**2 / (3 * p)

print("=" * 70)
print("FINGERPRINT DENSITY IDENTITY INVESTIGATION")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════
# PART 1: Reproduce the basic correlation
# ═══════════════════════════════════════════════════════════════════════
r_dw_dp, pval1 = stats.pearsonr(d_p, dw)
r_dw_M, pval2 = stats.pearsonr(M, dw)
r_dw_p, pval3 = stats.pearsonr(1/p, dw)

print(f"\n── BASIC CORRELATIONS ──")
print(f"  corr(d(p), ΔW)     = {r_dw_dp:.6f}")
print(f"  corr(M(p), ΔW)     = {r_dw_M:.6f}")
print(f"  corr(1/p,  ΔW)     = {r_dw_p:.6f}")
print(f"  corr(d(p), 1/p)    = {stats.pearsonr(d_p, 1/p)[0]:.6f}")

# ═══════════════════════════════════════════════════════════════════════
# PART 2: Is d(p) just 1/p in disguise?
# ═══════════════════════════════════════════════════════════════════════
# Compute the "excess" of d(p) over its asymptotic form
d_excess = d_p - d_p_approx  # how d(p) deviates from π²/(3p)
d_ratio = d_p / d_p_approx   # should → 1

print(f"\n── d(p) vs π²/(3p) ──")
print(f"  d(p)/[π²/(3p)] range: [{d_ratio.min():.6f}, {d_ratio.max():.6f}]")
print(f"  d(p)/[π²/(3p)] mean:  {d_ratio.mean():.6f}")
print(f"  d(p)/[π²/(3p)] std:   {d_ratio.std():.6f}")

# ═══════════════════════════════════════════════════════════════════════
# PART 3: Remove p-scaling — the key test
# ═══════════════════════════════════════════════════════════════════════
# If ΔW ~ c/p^α, then ΔW·p^α ~ const. Find α first.
# Fit log|ΔW| = α·log(p) + const
mask = dw != 0
log_abs_dw = np.log(np.abs(dw[mask]))
log_p = np.log(p[mask])
slope_dw, intercept_dw, r_fit, _, _ = stats.linregress(log_p, log_abs_dw)

print(f"\n── POWER LAW FIT: |ΔW| ~ p^α ──")
print(f"  α (slope) = {slope_dw:.4f}")
print(f"  r² = {r_fit**2:.6f}")
print(f"  → ΔW scales as ~ p^({slope_dw:.3f})")

# Similarly for d(p)
log_dp = np.log(d_p[mask])
slope_dp, _, r_dp_fit, _, _ = stats.linregress(log_p, log_dp)
print(f"  d(p) scales as ~ p^({slope_dp:.3f})")

# Now remove the p-scaling: multiply by p^|α|
alpha = abs(slope_dw)
dw_rescaled = dw * p**alpha       # should be ~ O(1)
dp_rescaled = d_p * p              # d(p)·p → π²/3 + correction

print(f"\n── RESCALED CORRELATIONS (p-dependence removed) ──")
r_rescaled, _ = stats.pearsonr(dp_rescaled, dw_rescaled)
print(f"  corr(d(p)·p, ΔW·p^{alpha:.2f}) = {r_rescaled:.6f}")

# Also try: does M(p) explain the rescaled ΔW?
r_M_rescaled, _ = stats.pearsonr(M[mask], (dw * p**alpha)[mask])
print(f"  corr(M(p), ΔW·p^{alpha:.2f})   = {r_M_rescaled:.6f}")

# ═══════════════════════════════════════════════════════════════════════
# PART 4: Test the product formula ΔW = c · d(p) · M(p)
# ═══════════════════════════════════════════════════════════════════════
product = d_p * M
mask_prod = product != 0
r_product, _ = stats.pearsonr(product[mask_prod], dw[mask_prod])

# Linear fit: ΔW = a · d(p)·M(p) + b
slope_prod, intercept_prod, r_prod_fit, _, _ = stats.linregress(product, dw)

print(f"\n── PRODUCT FORMULA: ΔW ≈ c · d(p) · M(p) ──")
print(f"  corr(d(p)·M(p), ΔW) = {r_product:.6f}")
print(f"  Linear fit: ΔW = {slope_prod:.6e} · d(p)·M(p) + {intercept_prod:.6e}")
print(f"  r² = {r_prod_fit**2:.6f}")

# ═══════════════════════════════════════════════════════════════════════
# PART 5: The ratio test — ΔW / d(p) vs M(p)
# ═══════════════════════════════════════════════════════════════════════
mask_dp = d_p != 0
ratio = dw[mask_dp] / d_p[mask_dp]

r_ratio_M, _ = stats.pearsonr(ratio, M[mask_dp])
r_ratio_p, _ = stats.pearsonr(ratio, p[mask_dp])

print(f"\n── RATIO TEST: ΔW/d(p) ──")
print(f"  corr(ΔW/d(p), M(p))  = {r_ratio_M:.6f}")
print(f"  corr(ΔW/d(p), p)     = {r_ratio_p:.6f}")
print(f"  corr(ΔW/d(p), 1/p)   = {stats.pearsonr(ratio, 1/p[mask_dp])[0]:.6f}")
print(f"  corr(ΔW/d(p), M/√p)  = {stats.pearsonr(ratio, M[mask_dp]/np.sqrt(p[mask_dp]))[0]:.6f}")

# Fit: ΔW/d(p) = a·M(p)/p + b (the next natural scaling)
ratio2 = M[mask_dp] / p[mask_dp]
slope_r2, intercept_r2, r_r2_fit, _, _ = stats.linregress(ratio2, ratio)
print(f"  Fit ΔW/d(p) vs M/p: slope={slope_r2:.4f}, r²={r_r2_fit**2:.6f}")

# ═══════════════════════════════════════════════════════════════════════
# PART 6: Deeper — ΔW · p² vs M(p)
# ═══════════════════════════════════════════════════════════════════════
# Since d(p) ~ 1/p, ΔW/d(p) ~ ΔW·p. If ΔW ~ 1/p^α with α≈2-3,
# then ΔW·p ~ 1/p^(α-1). Try ΔW·p² and ΔW·p³
for exp in [1, 2, 2.5, 3]:
    scaled = dw * p**exp
    r_m, _ = stats.pearsonr(scaled, M)
    r_1, _ = stats.pearsonr(scaled, 1/p)
    r_p, _ = stats.pearsonr(scaled, p)
    std = np.std(scaled)
    print(f"  ΔW·p^{exp}: corr(M)={r_m:.4f}, corr(1/p)={r_1:.4f}, corr(p)={r_p:.4f}, std={std:.4e}")

# ═══════════════════════════════════════════════════════════════════════
# PART 7: Residual analysis — what controls ΔW beyond d(p)?
# ═══════════════════════════════════════════════════════════════════════
# Fit ΔW = a·d(p) + b, compute residuals
slope_d, intercept_d, _, _, _ = stats.linregress(d_p, dw)
resid_d = dw - (slope_d * d_p + intercept_d)

r_resid_M, _ = stats.pearsonr(resid_d, M)
r_resid_p, _ = stats.pearsonr(resid_d, p)
r_resid_1p, _ = stats.pearsonr(resid_d, 1/p)

print(f"\n── RESIDUALS: ΔW - (a·d(p) + b) ──")
print(f"  Linear fit: ΔW = {slope_d:.6e}·d(p) + {intercept_d:.6e}")
print(f"  Residual std: {np.std(resid_d):.6e}  (vs ΔW std: {np.std(dw):.6e})")
print(f"  Variance explained by d(p): {r_dw_dp**2 * 100:.2f}%")
print(f"  corr(residual, M(p))  = {r_resid_M:.6f}")
print(f"  corr(residual, p)     = {r_resid_p:.6f}")
print(f"  corr(residual, 1/p)   = {r_resid_1p:.6f}")

# Now fit residuals against M(p)/p²
Mp2 = M / p**2
r_resid_Mp2, _ = stats.pearsonr(resid_d, Mp2)
print(f"  corr(residual, M/p²)  = {r_resid_Mp2:.6f}")

# Two-variable regression: ΔW = a·d(p) + b·M(p)/p² + c
from numpy.linalg import lstsq
X = np.column_stack([d_p, Mp2, np.ones(len(p))])
coeffs, resid_2var, _, _ = lstsq(X, dw, rcond=None)
pred_2var = X @ coeffs
r_2var = stats.pearsonr(pred_2var, dw)[0]
print(f"\n  Two-variable fit: ΔW = {coeffs[0]:.4e}·d(p) + {coeffs[1]:.4e}·M/p² + {coeffs[2]:.4e}")
print(f"  r = {r_2var:.6f}, r² = {r_2var**2:.6f}")

# ═══════════════════════════════════════════════════════════════════════
# PART 8: The DEFINITIVE test — partial correlation
# ═══════════════════════════════════════════════════════════════════════
# Partial correlation of d(p) with ΔW, controlling for 1/p
# This directly answers: does d(p) carry info beyond p?
def partial_corr(x, y, z):
    """Partial correlation of x,y controlling for z."""
    rx = stats.linregress(z, x)
    ry = stats.linregress(z, y)
    resid_x = x - (rx.slope * z + rx.intercept)
    resid_y = y - (ry.slope * z + ry.intercept)
    return stats.pearsonr(resid_x, resid_y)[0]

pc_dp_dw_given_p = partial_corr(d_p, dw, 1/p)
pc_dp_dw_given_p2 = partial_corr(d_p, dw, 1/p**2)
pc_M_dw_given_p = partial_corr(M, dw, 1/p)

print(f"\n── PARTIAL CORRELATIONS (controlling for p) ──")
print(f"  pcorr(d(p), ΔW | 1/p)  = {pc_dp_dw_given_p:.6f}")
print(f"  pcorr(d(p), ΔW | 1/p²) = {pc_dp_dw_given_p2:.6f}")
print(f"  pcorr(M(p), ΔW | 1/p)  = {pc_M_dw_given_p:.6f}")

# Also partial corr controlling for 1/p AND M
def partial_corr_2(x, y, z1, z2):
    """Partial correlation of x,y controlling for z1 and z2."""
    Z = np.column_stack([z1, z2, np.ones(len(z1))])
    cx, _, _, _ = lstsq(Z, x, rcond=None)
    cy, _, _, _ = lstsq(Z, y, rcond=None)
    resid_x = x - Z @ cx
    resid_y = y - Z @ cy
    return stats.pearsonr(resid_x, resid_y)[0]

pc_dp_dw_given_p_M = partial_corr_2(d_p, dw, 1/p, M)
print(f"  pcorr(d(p), ΔW | 1/p, M) = {pc_dp_dw_given_p_M:.6f}")

# ═══════════════════════════════════════════════════════════════════════
# PART 9: Try to find an exact identity
# ═══════════════════════════════════════════════════════════════════════
# Hypothesis: ΔW(p) = d(p)² · f(M(p))
# Since d(p) ~ 1/p and ΔW ~ 1/p^α, we need α ≈ 2 for this.
# Then f(M) should be ~ M or similar.

print(f"\n── SEARCHING FOR EXACT IDENTITY ──")

# Test: ΔW / d(p)²
ratio_d2 = dw / d_p**2
r_d2_M, _ = stats.pearsonr(ratio_d2, M)
r_d2_p, _ = stats.pearsonr(ratio_d2, p)
print(f"  ΔW/d(p)²: corr(M)={r_d2_M:.4f}, corr(p)={r_d2_p:.4f}, mean={np.mean(ratio_d2):.4f}")

# Test: ΔW · n (Farey size) — a natural "un-normalizing"
dw_times_n = dw * n
r_dn_M, _ = stats.pearsonr(dw_times_n, M)
r_dn_p, _ = stats.pearsonr(dw_times_n, p)
r_dn_1p, _ = stats.pearsonr(dw_times_n, 1/p)
print(f"  ΔW·n:  corr(M)={r_dn_M:.4f}, corr(p)={r_dn_p:.4f}, corr(1/p)={r_dn_1p:.4f}")

# Test: ΔW · n² — does this remove all p-dependence?
dw_times_n2 = dw * n**2
r_dn2_M, _ = stats.pearsonr(dw_times_n2, M)
r_dn2_p, _ = stats.pearsonr(dw_times_n2, p)
print(f"  ΔW·n²: corr(M)={r_dn2_M:.4f}, corr(p)={r_dn2_p:.4f}, mean={np.mean(dw_times_n2):.4f}")

# Best candidate: ΔW = (something) / n
# Since n ~ 3p²/π², ΔW·n ~ 3p²/π² · ΔW
# If ΔW ~ M/p², then ΔW·n ~ M·(3/π²) = constant-ish times M

# Comprehensive scan: ΔW · p^a · n^b for various a, b
print(f"\n── SCAN: corr(ΔW · p^a · n^b, M(p)) ──")
best_r = 0
best_ab = (0, 0)
for a_10 in range(-10, 11):
    for b_10 in range(-10, 11):
        a = a_10 / 5.0
        b = b_10 / 5.0
        trial = dw * p**a * n**b
        if np.any(np.isnan(trial)) or np.any(np.isinf(trial)):
            continue
        r_trial, _ = stats.pearsonr(trial, M)
        if abs(r_trial) > abs(best_r):
            best_r = r_trial
            best_ab = (a, b)

print(f"  Best: corr(ΔW · p^{best_ab[0]:.1f} · n^{best_ab[1]:.1f}, M) = {best_r:.6f}")

# Refine around best
a0, b0 = best_ab
best_r2 = 0
best_ab2 = best_ab
for da in np.linspace(-0.3, 0.3, 61):
    for db in np.linspace(-0.3, 0.3, 61):
        a = a0 + da
        b = b0 + db
        trial = dw * p**a * n**b
        if np.any(np.isnan(trial)) or np.any(np.isinf(trial)):
            continue
        r_trial, _ = stats.pearsonr(trial, M)
        if abs(r_trial) > abs(best_r2):
            best_r2 = r_trial
            best_ab2 = (a, b)

print(f"  Refined: corr(ΔW · p^{best_ab2[0]:.2f} · n^{best_ab2[1]:.2f}, M) = {best_r2:.6f}")

# Evaluate the best transformation
a_best, b_best = best_ab2
transformed = dw * p**a_best * n**b_best
slope_best, intercept_best, r_best_fit, _, _ = stats.linregress(M, transformed)
print(f"  Fit: ΔW·p^{a_best:.2f}·n^{b_best:.2f} = {slope_best:.6e}·M + {intercept_best:.6e}")
print(f"  → ΔW ≈ ({slope_best:.4e}·M + {intercept_best:.4e}) / (p^{a_best:.2f} · n^{b_best:.2f})")

# ═══════════════════════════════════════════════════════════════════════
# PART 10: Direct test — is d(p) just a proxy for 1/p?
# ═══════════════════════════════════════════════════════════════════════
# Compute d(p) - π²/(3p) = the Farey sequence correction term
correction = d_p - np.pi**2 / (3*p)
r_corr_dw, _ = stats.pearsonr(correction, dw)
r_corr_resid, _ = stats.pearsonr(correction, resid_d)

print(f"\n── d(p) CORRECTION TERM: d(p) - π²/(3p) ──")
print(f"  corr(correction, ΔW)     = {r_corr_dw:.6f}")
print(f"  corr(correction, resid)  = {r_corr_resid:.6f}")
print(f"  correction range: [{correction.min():.6e}, {correction.max():.6e}]")
print(f"  |correction/d(p)| mean:  {np.mean(np.abs(correction/d_p)):.6f}")

# ═══════════════════════════════════════════════════════════════════════
# PLOTS
# ═══════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(3, 3, figsize=(18, 16))

# Plot 1: ΔW vs d(p) — the raw correlation
ax = axes[0, 0]
ax.scatter(d_p[::10], dw[::10], s=1, alpha=0.5, c='steelblue')
ax.set_xlabel('d(p) = (p-1)/(n-1)')
ax.set_ylabel('ΔW(p)')
ax.set_title(f'ΔW vs d(p), r = {r_dw_dp:.4f}')

# Plot 2: d(p) vs 1/p — how close are they?
ax = axes[0, 1]
ax.scatter(1/p[::10], d_p[::10], s=1, alpha=0.5, c='steelblue')
x_line = np.linspace(0, max(1/p), 100)
ax.plot(x_line, np.pi**2/3 * x_line, 'r-', label='π²/(3p)', linewidth=2)
ax.set_xlabel('1/p')
ax.set_ylabel('d(p)')
ax.set_title('d(p) vs 1/p')
ax.legend()

# Plot 3: d(p)·p vs p — showing deviation from π²/3
ax = axes[0, 2]
ax.scatter(p[::10], dp_rescaled[::10], s=1, alpha=0.5, c='steelblue')
ax.axhline(np.pi**2/3, color='r', linestyle='--', label=f'π²/3 ≈ {np.pi**2/3:.4f}')
ax.set_xlabel('p')
ax.set_ylabel('d(p) · p')
ax.set_title('d(p)·p converges to π²/3')
ax.legend()

# Plot 4: Rescaled — ΔW·p^α vs d(p)·p
ax = axes[1, 0]
ax.scatter(dp_rescaled[::10], dw_rescaled[::10], s=1, alpha=0.5, c='darkorange')
ax.set_xlabel('d(p)·p')
ax.set_ylabel(f'ΔW·p^{alpha:.2f}')
ax.set_title(f'Rescaled: r = {r_rescaled:.4f}')

# Plot 5: ΔW/d(p) vs M(p)
ax = axes[1, 1]
ax.scatter(M[mask_dp][::10], ratio[::10], s=1, alpha=0.5, c='green')
ax.set_xlabel('M(p)')
ax.set_ylabel('ΔW(p) / d(p)')
ax.set_title(f'ΔW/d(p) vs M, r = {r_ratio_M:.4f}')

# Plot 6: Residual (ΔW - a·d(p) - b) vs M(p)
ax = axes[1, 2]
ax.scatter(M[::10], resid_d[::10], s=1, alpha=0.5, c='crimson')
ax.axhline(0, color='k', linestyle='--', alpha=0.3)
ax.set_xlabel('M(p)')
ax.set_ylabel('Residual: ΔW - (a·d(p)+b)')
ax.set_title(f'Residual vs M(p), r = {r_resid_M:.4f}')

# Plot 7: Best transformation vs M
ax = axes[2, 0]
ax.scatter(M[::10], transformed[::10], s=1, alpha=0.5, c='purple')
M_line = np.linspace(M.min(), M.max(), 100)
ax.plot(M_line, slope_best * M_line + intercept_best, 'r-', linewidth=2)
ax.set_xlabel('M(p)')
ax.set_ylabel(f'ΔW · p^{a_best:.1f} · n^{b_best:.1f}')
ax.set_title(f'Best identity: r = {best_r2:.4f}')

# Plot 8: ΔW·n vs M — testing ΔW ~ M/n
ax = axes[2, 1]
ax.scatter(M[::10], dw_times_n[::10], s=1, alpha=0.5, c='teal')
ax.set_xlabel('M(p)')
ax.set_ylabel('ΔW · n')
ax.set_title(f'ΔW·n vs M, r = {r_dn_M:.4f}')

# Plot 9: Partial correlation visualization
ax = axes[2, 2]
# Residualize both d(p) and ΔW against 1/p
rx = stats.linregress(1/p, d_p)
ry = stats.linregress(1/p, dw)
resid_dp = d_p - (rx.slope/p + rx.intercept)
resid_dw = dw - (ry.slope/p + ry.intercept)
ax.scatter(resid_dp[::10], resid_dw[::10], s=1, alpha=0.5, c='darkblue')
ax.set_xlabel('d(p) residual (after removing 1/p)')
ax.set_ylabel('ΔW residual (after removing 1/p)')
ax.set_title(f'Partial corr(d(p),ΔW|1/p) = {pc_dp_dw_given_p:.4f}')

plt.tight_layout()
plt.savefig(Path(__file__).parent / "fingerprint_density_plots.png", dpi=150)
print(f"\nPlots saved to experiments/fingerprint_density_plots.png")

# ═══════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SUMMARY OF FINDINGS")
print("=" * 70)

if abs(pc_dp_dw_given_p) < 0.1:
    verdict = "TRIVIAL"
    explanation = ("The partial correlation of d(p) with ΔW, after controlling for 1/p, "
                   f"is only {pc_dp_dw_given_p:.4f}. "
                   "This means d(p) is essentially just a proxy for 1/p. "
                   "The high raw correlation (r = -0.9963) comes from both quantities "
                   "scaling as ~1/p, not from any structural relationship.")
elif abs(pc_dp_dw_given_p) < 0.3:
    verdict = "MOSTLY TRIVIAL with small structural component"
    explanation = (f"Partial corr = {pc_dp_dw_given_p:.4f}. "
                   "Most of the correlation is from p-scaling, but d(p) carries "
                   "a small amount of information beyond 1/p.")
else:
    verdict = "STRUCTURAL"
    explanation = (f"Partial corr = {pc_dp_dw_given_p:.4f}. "
                   "d(p) carries significant information about ΔW beyond just the p-scaling. "
                   "The Farey sequence structure matters.")

print(f"\n  VERDICT: The correlation is {verdict}")
print(f"\n  {explanation}")

if abs(best_r2) > 0.5:
    print(f"\n  BEST IDENTITY FOUND:")
    print(f"    ΔW(p) ≈ ({slope_best:.4e} · M(p) + {intercept_best:.4e}) / (p^{a_best:.2f} · n^{b_best:.2f})")
    print(f"    correlation: r = {best_r2:.4f}")

print(f"\n  KEY NUMBERS:")
print(f"    raw corr(d(p), ΔW)              = {r_dw_dp:.6f}")
print(f"    corr(1/p, ΔW)                   = {r_dw_p:.6f}")
print(f"    partial corr(d(p), ΔW | 1/p)    = {pc_dp_dw_given_p:.6f}")
print(f"    partial corr(M(p), ΔW | 1/p)    = {pc_M_dw_given_p:.6f}")
print(f"    corr(d(p)·M(p), ΔW)             = {r_product:.6f}")
print(f"    ΔW scales as p^({slope_dw:.3f})")
print(f"    d(p) scales as p^({slope_dp:.3f})")
