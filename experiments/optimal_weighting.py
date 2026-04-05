#!/usr/bin/env python3
"""
Task 7: Optimal weighting and raw DeltaW spectroscope analysis.

Computes F(gamma) spectroscope under various weighting schemes to find
the optimal way to detect zeta zeros from R(p) data.

Input: R_bound_200K_output.csv (primes with M(p) <= -3, ~6327 rows)
Output: OPTIMAL_WEIGHTING_RESULTS.md + figures/optimal_weighting.png
"""

import numpy as np
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import time

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
GAMMA1 = 14.134725141734693  # first zeta zero
INPUT_CSV = Path.home() / "Desktop/Farey-Local/experiments/R_bound_200K_output.csv"
OUTPUT_MD = Path.home() / "Desktop/Farey-Local/experiments/OPTIMAL_WEIGHTING_RESULTS.md"
OUTPUT_FIG = Path.home() / "Desktop/Farey-Local/figures/optimal_weighting.png"

# Spectroscope grid
GAMMA_MIN, GAMMA_MAX, N_GAMMA = 10.0, 50.0, 10000
gammas = np.linspace(GAMMA_MIN, GAMMA_MAX, N_GAMMA)

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
print("Loading data...")
rows = []
with open(INPUT_CSV, 'r') as f:
    # Skip first 2 status lines
    next(f)
    next(f)
    reader = csv.DictReader(f)
    for row in reader:
        rows.append((float(row['p']), float(row['M_p']), float(row['R']), float(row['min_R_so_far'])))
data = np.array(rows)
N_DATA = len(data)
print(f"  Loaded {N_DATA} rows, p range [{data[0,0]:.0f}, {data[-1,0]:.0f}]")
print(f"  M(p) range [{data[:,1].min():.0f}, {data[:,1].max():.0f}]")

primes = data[:, 0]
M_p = data[:, 1]
R_p = data[:, 2]
log_p = np.log(primes)
sqrt_p = np.sqrt(primes)

# ---------------------------------------------------------------------------
# Helper: compute spectroscope |sum_j w_j * p_j^{-1/2 - i*gamma}|^2
# ---------------------------------------------------------------------------
def compute_spectroscope(weights, p_vals, log_p_vals, sqrt_p_vals, gammas):
    """Vectorised spectroscope: F(gamma) = |sum_j w_j / sqrt(p_j) * exp(-i*gamma*log(p_j))|^2"""
    # weights: (N,), gammas: (G,)
    # phase matrix: (G, N) -- gamma_g * log(p_j)
    # For memory: chunk if needed
    N = len(p_vals)
    G = len(gammas)

    # Precompute amplitude
    amp = weights / sqrt_p_vals  # (N,)

    # Chunk to avoid huge memory (G x N can be 10000 x 6327 = 63M, fine as float64)
    phases = np.outer(gammas, log_p_vals)  # (G, N)
    cos_phases = np.cos(phases)
    sin_phases = np.sin(phases)

    real_part = cos_phases @ amp  # (G,)
    imag_part = sin_phases @ amp  # (G,)

    F = real_part**2 + imag_part**2
    return F


def find_peak_near_gamma1(gammas, F, target=GAMMA1, window=2.0):
    """Find peak nearest to target within +/- window."""
    mask = (gammas >= target - window) & (gammas <= target + window)
    if not mask.any():
        return np.nan, np.nan, np.nan, np.nan
    idx_local = np.argmax(F[mask])
    idx_global = np.where(mask)[0][idx_local]
    peak_pos = gammas[idx_global]
    peak_height = F[idx_global]
    error_pct = abs(peak_pos - target) / target * 100
    median_F = np.median(F)
    snr = peak_height / median_F if median_F > 0 else np.inf
    return peak_pos, error_pct, peak_height, snr


# ---------------------------------------------------------------------------
# 2. FILTER OPTIMIZATION: different M(p) thresholds
#    NOTE: data is pre-filtered to M(p) <= -3, so thresholds -1 and -2
#    are equivalent to -3 on this dataset.
# ---------------------------------------------------------------------------
print("\n=== Part 2: Filter Optimization ===")

threshold_results = []

# Hard thresholds
for thresh in [-1, -2, -3, -4, -5]:
    mask = M_p <= thresh
    n_primes = mask.sum()
    if n_primes < 10:
        threshold_results.append({
            'label': f'M(p) <= {thresh}',
            'N_primes': n_primes,
            'peak_pos': np.nan, 'error_pct': np.nan,
            'peak_height': np.nan, 'snr': np.nan
        })
        continue

    w = R_p[mask]
    F = compute_spectroscope(w, primes[mask], log_p[mask], sqrt_p[mask], gammas)
    peak_pos, error_pct, peak_height, snr = find_peak_near_gamma1(gammas, F)
    threshold_results.append({
        'label': f'M(p) <= {thresh}',
        'N_primes': n_primes,
        'peak_pos': peak_pos, 'error_pct': error_pct,
        'peak_height': peak_height, 'snr': snr
    })
    print(f"  {threshold_results[-1]['label']:15s}  N={n_primes:5d}  peak={peak_pos:.4f}  err={error_pct:.4f}%  SNR={snr:.1f}")

# No filter, R(p) weight (all data, since all have M(p)<=-3)
F_all_R = compute_spectroscope(R_p, primes, log_p, sqrt_p, gammas)
pp, ep, ph, snr_val = find_peak_near_gamma1(gammas, F_all_R)
threshold_results.append({
    'label': 'All, w=R(p)',
    'N_primes': len(primes),
    'peak_pos': pp, 'error_pct': ep,
    'peak_height': ph, 'snr': snr_val
})
print(f"  {'All, w=R(p)':15s}  N={len(primes):5d}  peak={pp:.4f}  err={ep:.4f}%  SNR={snr_val:.1f}")

# No filter, M(p)/sqrt(p) weight
w_mertens = M_p / sqrt_p
F_all_M = compute_spectroscope(w_mertens, primes, log_p, sqrt_p, gammas)
pp, ep, ph, snr_val = find_peak_near_gamma1(gammas, F_all_M)
threshold_results.append({
    'label': 'All, w=M/sqrt(p)',
    'N_primes': len(primes),
    'peak_pos': pp, 'error_pct': ep,
    'peak_height': ph, 'snr': snr_val
})
print(f"  {'All, w=M/sqrt(p)':15s}  N={len(primes):5d}  peak={pp:.4f}  err={ep:.4f}%  SNR={snr_val:.1f}")

# ---------------------------------------------------------------------------
# 3. SOFT WEIGHTING schemes
# ---------------------------------------------------------------------------
print("\n=== Part 3: Soft Weighting ===")

soft_results = []

# (a) w = |R(p)|
w_abs = np.abs(R_p)
F_abs = compute_spectroscope(w_abs, primes, log_p, sqrt_p, gammas)
pp, ep, ph, snr_val = find_peak_near_gamma1(gammas, F_abs)
soft_results.append({
    'label': 'w = |R(p)|',
    'N_primes': len(primes),
    'peak_pos': pp, 'error_pct': ep,
    'peak_height': ph, 'snr': snr_val
})
print(f"  {'w = |R(p)|':25s}  peak={pp:.4f}  err={ep:.4f}%  SNR={snr_val:.1f}")

# (b) w = R(p) * max(0, -M(p))^0.5
neg_M = np.maximum(0, -M_p)
w_soft05 = R_p * neg_M**0.5
F_soft05 = compute_spectroscope(w_soft05, primes, log_p, sqrt_p, gammas)
pp, ep, ph, snr_val = find_peak_near_gamma1(gammas, F_soft05)
soft_results.append({
    'label': 'w = R * (-M)^0.5',
    'N_primes': len(primes),
    'peak_pos': pp, 'error_pct': ep,
    'peak_height': ph, 'snr': snr_val
})
print(f"  {'w = R * (-M)^0.5':25s}  peak={pp:.4f}  err={ep:.4f}%  SNR={snr_val:.1f}")

# (c) w = R(p) * max(0, -M(p))^1.0
w_soft10 = R_p * neg_M**1.0
F_soft10 = compute_spectroscope(w_soft10, primes, log_p, sqrt_p, gammas)
pp, ep, ph, snr_val = find_peak_near_gamma1(gammas, F_soft10)
soft_results.append({
    'label': 'w = R * (-M)^1.0',
    'N_primes': len(primes),
    'peak_pos': pp, 'error_pct': ep,
    'peak_height': ph, 'snr': snr_val
})
print(f"  {'w = R * (-M)^1.0':25s}  peak={pp:.4f}  err={ep:.4f}%  SNR={snr_val:.1f}")

# ---------------------------------------------------------------------------
# 4. MERTENS SPECTROSCOPE: G(gamma) = |sum M(p)/sqrt(p) * p^{-1/2-igamma}|^2
# ---------------------------------------------------------------------------
print("\n=== Part 4: Mertens Spectroscope ===")

# Pure Mertens: weight = M(p)/sqrt(p), amplitude already has /sqrt(p) inside
# Actually the spectroscope function divides by sqrt(p) internally, so
# for "M(p)/sqrt(p) * p^{-1/2-igamma}" we want w = M(p)/sqrt(p) passed in
# and the function does w/sqrt(p) = M(p)/p.
# Let me be explicit:
# G(gamma) = |sum_p M(p)/sqrt(p) * p^{-1/2} * e^{-igamma*log(p)}|^2
#           = |sum_p M(p)/p * e^{-igamma*log(p)}|^2
# Our function computes |sum w/sqrt(p) * e^{-igamma*log(p)}|^2
# So we need w = M(p)/sqrt(p).

w_mertens_spec = M_p / sqrt_p
F_mertens = compute_spectroscope(w_mertens_spec, primes, log_p, sqrt_p, gammas)
pp_m, ep_m, ph_m, snr_m = find_peak_near_gamma1(gammas, F_mertens)
print(f"  Mertens spectroscope:  peak={pp_m:.4f}  err={ep_m:.4f}%  SNR={snr_m:.1f}")

# R(p) spectroscope for comparison (already computed as F_all_R)
pp_r, ep_r, ph_r, snr_r = find_peak_near_gamma1(gammas, F_all_R)
print(f"  R(p)    spectroscope:  peak={pp_r:.4f}  err={ep_r:.4f}%  SNR={snr_r:.1f}")

# ---------------------------------------------------------------------------
# 5. INFORMATIVENESS: contribution of each prime to F(gamma_1)
# ---------------------------------------------------------------------------
print("\n=== Part 5: Most Informative Primes ===")

# contrib(p) = R(p) * p^{-1/2} * cos(gamma_1 * log(p))
contrib = R_p / sqrt_p * np.cos(GAMMA1 * log_p)
abs_contrib = np.abs(contrib)
top_idx = np.argsort(abs_contrib)[::-1][:20]

print(f"  {'Rank':>4s}  {'p':>8s}  {'M(p)':>6s}  {'R(p)':>10s}  {'contrib':>12s}  {'|contrib|':>12s}")
for rank, idx in enumerate(top_idx, 1):
    print(f"  {rank:4d}  {int(primes[idx]):8d}  {int(M_p[idx]):6d}  {R_p[idx]:10.4f}  {contrib[idx]:12.6f}  {abs_contrib[idx]:12.6f}")

# ---------------------------------------------------------------------------
# 6. FIGURE: 4 panels
# ---------------------------------------------------------------------------
print("\nGenerating figure...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Optimal Weighting Analysis for Farey Spectroscope', fontsize=14, fontweight='bold')

# --- Panel (a): SNR vs threshold ---
ax = axes[0, 0]
# Use only hard-threshold results (first 5) + all/R + all/M
labels_a = [r['label'] for r in threshold_results]
snrs_a = [r['snr'] for r in threshold_results]
colors_a = ['#2196F3'] * 5 + ['#4CAF50', '#FF9800']  # blue for thresholds, green/orange for alternatives
bars = ax.bar(range(len(labels_a)), snrs_a, color=colors_a, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(labels_a)))
ax.set_xticklabels(labels_a, rotation=45, ha='right', fontsize=8)
ax.set_ylabel('SNR (peak / median)')
ax.set_title('(a) SNR vs Weighting Scheme')
ax.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='SNR=1 (no detection)')
ax.legend(fontsize=8)
for bar, v in zip(bars, snrs_a):
    if not np.isnan(v):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{v:.1f}', ha='center', va='bottom', fontsize=7)

# --- Panel (b): error% vs threshold ---
ax = axes[0, 1]
# Combine threshold + soft results
all_results = threshold_results + soft_results
labels_b = [r['label'] for r in all_results]
errors_b = [r['error_pct'] for r in all_results]
colors_b = ['#2196F3'] * 5 + ['#4CAF50', '#FF9800'] + ['#9C27B0'] * 3
bars = ax.bar(range(len(labels_b)), errors_b, color=colors_b, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(labels_b)))
ax.set_xticklabels(labels_b, rotation=45, ha='right', fontsize=7)
ax.set_ylabel('Error from gamma_1 (%)')
ax.set_title('(b) Detection Error vs Weighting Scheme')
ax.axhline(y=0.1, color='green', linestyle='--', alpha=0.5, label='0.1% error')
ax.legend(fontsize=8)
for bar, v in zip(bars, errors_b):
    if not np.isnan(v):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{v:.3f}%', ha='center', va='bottom', fontsize=6)

# --- Panel (c): Mertens vs R(p) spectroscope overlay ---
ax = axes[1, 0]
# Normalise both for visual comparison
F_mertens_norm = F_mertens / np.max(F_mertens)
F_R_norm = F_all_R / np.max(F_all_R)
ax.plot(gammas, F_R_norm, color='#2196F3', linewidth=1.0, label='R(p) spectroscope', alpha=0.9)
ax.plot(gammas, F_mertens_norm, color='#FF5722', linewidth=1.0, label='Mertens spectroscope', alpha=0.7)
ax.axvline(x=GAMMA1, color='black', linestyle='--', linewidth=0.8, alpha=0.6, label=f'gamma_1 = {GAMMA1:.4f}')
# Mark known zeros
known_zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052]
for z in known_zeros[1:]:
    ax.axvline(x=z, color='gray', linestyle=':', linewidth=0.5, alpha=0.4)
ax.set_xlabel('gamma')
ax.set_ylabel('F(gamma) / max(F)')
ax.set_title('(c) Mertens vs R(p) Spectroscope (normalised)')
ax.legend(fontsize=8)
ax.set_xlim(GAMMA_MIN, GAMMA_MAX)

# --- Panel (d): Top-20 informative primes bar chart ---
ax = axes[1, 1]
top_primes = primes[top_idx].astype(int)
top_contribs = contrib[top_idx]
colors_d = ['#4CAF50' if c > 0 else '#F44336' for c in top_contribs]
ax.barh(range(19, -1, -1), top_contribs, color=colors_d, edgecolor='black', linewidth=0.3)
ax.set_yticks(range(19, -1, -1))
ax.set_yticklabels([f'p={p}' for p in top_primes], fontsize=7)
ax.set_xlabel('Contribution to F(gamma_1)')
ax.set_title('(d) Top-20 Most Informative Primes')
ax.axvline(x=0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig(OUTPUT_FIG, dpi=200, bbox_inches='tight')
print(f"  Figure saved: {OUTPUT_FIG}")

# ---------------------------------------------------------------------------
# 7. OUTPUT: Markdown summary
# ---------------------------------------------------------------------------
print("\nWriting summary...")

# Find overall best
all_combined = threshold_results + soft_results
best_snr = max(all_combined, key=lambda r: r['snr'] if not np.isnan(r['snr']) else -1)
best_err = min(all_combined, key=lambda r: r['error_pct'] if not np.isnan(r['error_pct']) else 999)

lines = []
lines.append("# Optimal Weighting Results\n")
lines.append(f"**Date:** 2026-04-05\n")
lines.append(f"**Input:** R_bound_200K_output.csv ({N_DATA} primes, p in [{int(primes[0])}, {int(primes[-1])}])\n")
lines.append(f"**Note:** Input data pre-filtered to M(p) <= -3. Thresholds -1 and -2 are identical to -3.\n")
lines.append("")

lines.append("## Filter Optimization (Hard Thresholds)\n")
lines.append("| Scheme | N_primes | Peak position | Error% | Peak height | SNR |")
lines.append("|--------|----------|---------------|--------|-------------|-----|")
for r in threshold_results:
    lines.append(f"| {r['label']} | {r['N_primes']} | {r['peak_pos']:.4f} | {r['error_pct']:.4f}% | {r['peak_height']:.2f} | {r['snr']:.1f} |")
lines.append("")

lines.append("## Soft Weighting Schemes\n")
lines.append("| Scheme | N_primes | Peak position | Error% | Peak height | SNR |")
lines.append("|--------|----------|---------------|--------|-------------|-----|")
for r in soft_results:
    lines.append(f"| {r['label']} | {r['N_primes']} | {r['peak_pos']:.4f} | {r['error_pct']:.4f}% | {r['peak_height']:.2f} | {r['snr']:.1f} |")
lines.append("")

lines.append("## Mertens vs R(p) Spectroscope\n")
lines.append("| Spectroscope | Peak position | Error% | SNR |")
lines.append("|--------------|---------------|--------|-----|")
lines.append(f"| R(p) | {pp_r:.4f} | {ep_r:.4f}% | {snr_r:.1f} |")
lines.append(f"| Mertens M(p)/sqrt(p) | {pp_m:.4f} | {ep_m:.4f}% | {snr_m:.1f} |")
lines.append("")

lines.append("## Best Performers\n")
lines.append(f"- **Highest SNR:** {best_snr['label']} (SNR = {best_snr['snr']:.1f}, error = {best_snr['error_pct']:.4f}%)")
lines.append(f"- **Lowest error:** {best_err['label']} (error = {best_err['error_pct']:.4f}%, SNR = {best_err['snr']:.1f})")
lines.append("")

lines.append("## Top-20 Most Informative Primes\n")
lines.append("| Rank | p | M(p) | R(p) | Contribution | |Contribution| |")
lines.append("|------|------|------|------|--------------|---------------|")
for rank, idx in enumerate(top_idx, 1):
    lines.append(f"| {rank} | {int(primes[idx])} | {int(M_p[idx])} | {R_p[idx]:.4f} | {contrib[idx]:.6f} | {abs_contrib[idx]:.6f} |")
lines.append("")

lines.append("## Key Observations\n")

# Compute some derived insights
snr_all_R = [r for r in threshold_results if r['label'] == 'All, w=R(p)'][0]['snr']
snr_m3 = [r for r in threshold_results if r['label'] == 'M(p) <= -3'][0]['snr']
snr_m5 = [r for r in threshold_results if r['label'] == 'M(p) <= -5'][0]['snr']

lines.append(f"1. **Data pre-filtering note:** All data has M(p) <= -3, so thresholds -1, -2, -3 are identical ({threshold_results[0]['N_primes']} primes each).")
lines.append(f"2. **Stricter filtering (M(p)<=-5):** Reduces to {[r for r in threshold_results if r['label']=='M(p) <= -5'][0]['N_primes']} primes with SNR={snr_m5:.1f}.")
lines.append(f"3. **Soft weighting:** R*(-M)^1.0 amplifies large-|M| primes, SNR = {soft_results[2]['snr']:.1f}.")
lines.append(f"4. **Mertens spectroscope:** SNR = {snr_m:.1f} vs R(p) spectroscope SNR = {snr_r:.1f}.")
if snr_m > snr_r:
    lines.append("   --> Mertens weighting OUTPERFORMS R(p) weighting for gamma_1 detection.")
else:
    lines.append("   --> R(p) weighting outperforms Mertens for gamma_1 detection.")
lines.append(f"5. **Top informative prime:** p={int(primes[top_idx[0]])}, |contrib|={abs_contrib[top_idx[0]]:.6f}.")
lines.append("")

md_text = "\n".join(lines)
OUTPUT_MD.write_text(md_text)
print(f"  Summary saved: {OUTPUT_MD}")

print("\nDone.")
