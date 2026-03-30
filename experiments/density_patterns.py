#!/usr/bin/env python3
"""
density_patterns.py

Comprehensive analysis of T(N) > 0 patterns among M(p)=-3 primes.
Reads density_patterns_all.csv produced by density_patterns.c.

Outputs:
  - density_patterns_plots.png (multi-panel figure)
  - density_patterns_analysis.txt (detailed statistics)
"""

import numpy as np
import csv
import os
from collections import Counter

# ----- Load data -----
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(DATA_DIR, "density_patterns_all.csv")

primes = []
with open(csv_path, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        primes.append({
            'p': int(row['p']),
            'N': int(row['N']),
            'T': float(row['T_N']),
            'M_half': int(row['M_half']),
            'M_third': int(row['M_third']),
            'M_fifth': int(row['M_fifth']),
            'M_sixth': int(row['M_sixth']),
            'M_seventh': int(row['M_seventh']),
            'p_mod6': int(row['p_mod6']),
            'p_mod12': int(row['p_mod12']),
            'p_mod30': int(row['p_mod30']),
            'p_mod24': int(row['p_mod24']),
        })

n_total = len(primes)
ps = np.array([d['p'] for d in primes])
Ts = np.array([d['T'] for d in primes])
logps = np.log(ps)
is_pos = Ts > 0

print(f"Total M(p)=-3 primes: {n_total}")
print(f"T > 0 count: {np.sum(is_pos)} ({100*np.mean(is_pos):.1f}%)")
print(f"T range: [{Ts.min():.2f}, {Ts.max():.2f}]")
print()

out_lines = []
def report(s):
    print(s)
    out_lines.append(s)

report("=" * 70)
report("DENSITY PATTERNS ANALYSIS: T(N) > 0 among M(p)=-3 primes")
report("=" * 70)
report(f"Total primes: {n_total}")
report(f"T > 0: {np.sum(is_pos)} ({100*np.mean(is_pos):.1f}%)")
report(f"T < 0: {np.sum(~is_pos)} ({100*np.mean(~is_pos):.1f}%)")
report(f"T range: [{Ts.min():.2f}, {Ts.max():.2f}]")
report(f"Mean T: {Ts.mean():.4f}")
report(f"Median T: {np.median(Ts):.4f}")
report("")

# ===== Q1: DENSITY TREND BY DECADE =====
report("=" * 70)
report("Q1: DENSITY TREND (fraction of T>0 in [10^k, 10^{k+1}])")
report("=" * 70)

for k in range(1, 8):
    lo, hi = 10**k, 10**(k+1)
    mask = (ps >= lo) & (ps < hi)
    if np.sum(mask) == 0:
        continue
    n_win = np.sum(mask)
    n_pos = np.sum(is_pos[mask])
    frac = n_pos / n_win if n_win > 0 else 0
    report(f"  [{lo:>10}, {hi:>10}): {n_win:>4} primes, {n_pos:>3} T>0, fraction = {frac:.4f}")

report("")

# ===== Q2: CLUSTERING =====
report("=" * 70)
report("Q2: CLUSTERING of T>0 primes")
report("=" * 70)

pos_indices = np.where(is_pos)[0]
neg_indices = np.where(~is_pos)[0]

# Run-length analysis
runs_pos = []
runs_neg = []
current_sign = is_pos[0]
current_len = 1
for i in range(1, n_total):
    if is_pos[i] == current_sign:
        current_len += 1
    else:
        if current_sign:
            runs_pos.append(current_len)
        else:
            runs_neg.append(current_len)
        current_sign = is_pos[i]
        current_len = 1
if current_sign:
    runs_pos.append(current_len)
else:
    runs_neg.append(current_len)

report(f"  T>0 run lengths: count={len(runs_pos)}, max={max(runs_pos) if runs_pos else 0}, "
       f"mean={np.mean(runs_pos):.2f}" if runs_pos else "  T>0 runs: none")
report(f"  T<0 run lengths: count={len(runs_neg)}, max={max(runs_neg) if runs_neg else 0}, "
       f"mean={np.mean(runs_neg):.2f}" if runs_neg else "  T<0 runs: none")

# Distribution of T>0 run lengths
if runs_pos:
    rp_counter = Counter(runs_pos)
    report(f"  T>0 run length distribution: {dict(sorted(rp_counter.items()))}")
if runs_neg:
    rn_counter = Counter(runs_neg)
    report(f"  T<0 run length distribution (top 10): "
           f"{dict(sorted(rn_counter.items(), key=lambda x: -x[1])[:10])}")

# Gaps between consecutive T>0 primes (in index space)
if len(pos_indices) >= 2:
    idx_gaps = np.diff(pos_indices)
    report(f"  Gaps between T>0 primes (index): min={idx_gaps.min()}, max={idx_gaps.max()}, "
           f"mean={idx_gaps.mean():.2f}, median={np.median(idx_gaps):.1f}")
    # Gaps in prime value space
    p_gaps = np.diff(ps[pos_indices])
    report(f"  Gaps between T>0 primes (value): min={p_gaps.min()}, max={p_gaps.max()}, "
           f"mean={p_gaps.mean():.0f}")

report("")

# ===== Q3: CORRELATION WITH M(N/2), M(N/3) =====
report("=" * 70)
report("Q3: CORRELATION WITH M(N/2), M(N/3)")
report("=" * 70)

M_half = np.array([d['M_half'] for d in primes])
M_third = np.array([d['M_third'] for d in primes])
M_fifth = np.array([d['M_fifth'] for d in primes])

# Leading terms of T(N): M(N/2)/2 + M(N/3)/3 + M(N/4)/4 + M(N/5)/5 + ...
# So a positive M(N/2) or M(N/3) pushes T toward positive.
leading_term = M_half / 2.0 + M_third / 3.0

report(f"  Correlation(T, M(N/2)): {np.corrcoef(Ts, M_half)[0,1]:.4f}")
report(f"  Correlation(T, M(N/3)): {np.corrcoef(Ts, M_third)[0,1]:.4f}")
report(f"  Correlation(T, M(N/5)): {np.corrcoef(Ts, M_fifth)[0,1]:.4f}")
report(f"  Correlation(T, M(N/2)/2+M(N/3)/3): {np.corrcoef(Ts, leading_term)[0,1]:.4f}")
report("")

# Among T>0 vs T<0
report("  Among T>0 primes:")
report(f"    Mean M(N/2) = {M_half[is_pos].mean():.2f} (vs {M_half[~is_pos].mean():.2f} for T<0)")
report(f"    Mean M(N/3) = {M_third[is_pos].mean():.2f} (vs {M_third[~is_pos].mean():.2f} for T<0)")
report(f"    Fraction M(N/2) > 0: {np.mean(M_half[is_pos] > 0):.3f} (vs {np.mean(M_half[~is_pos] > 0):.3f})")
report(f"    Fraction M(N/3) > 0: {np.mean(M_third[is_pos] > 0):.3f} (vs {np.mean(M_third[~is_pos] > 0):.3f})")
report("")

# Breakdown: fraction with T>0 conditioned on sign of M(N/2)
for sign_label, cond in [("M(N/2) > 0", M_half > 0), ("M(N/2) <= 0", M_half <= 0),
                          ("M(N/2) > 5", M_half > 5), ("M(N/2) < -5", M_half < -5)]:
    n_c = np.sum(cond)
    if n_c > 0:
        frac = np.mean(is_pos[cond])
        report(f"    P(T>0 | {sign_label}) = {frac:.3f}  (n={n_c})")

report("")

# ===== Q4: RESIDUE CLASSES =====
report("=" * 70)
report("Q4: RESIDUE CLASSES")
report("=" * 70)

for mod_name, mod_vals in [("mod 6", [d['p_mod6'] for d in primes]),
                            ("mod 12", [d['p_mod12'] for d in primes]),
                            ("mod 30", [d['p_mod30'] for d in primes]),
                            ("mod 24", [d['p_mod24'] for d in primes])]:
    report(f"\n  p {mod_name}:")
    mod_arr = np.array(mod_vals)
    residues = sorted(set(mod_arr))
    for r in residues:
        mask_r = mod_arr == r
        n_r = np.sum(mask_r)
        if n_r < 3:
            continue
        n_r_pos = np.sum(is_pos[mask_r])
        frac = n_r_pos / n_r
        report(f"    r={r:>2}: {n_r:>4} primes, {n_r_pos:>3} T>0, frac={frac:.3f}")

report("")

# ===== Q5: SPACING DISTRIBUTION =====
report("=" * 70)
report("Q5: SPACING DISTRIBUTION")
report("=" * 70)

# Gaps between consecutive primes in the M=-3 list
all_gaps = np.diff(ps)
pos_ps = ps[is_pos]
neg_ps = ps[~is_pos]

if len(pos_ps) >= 2:
    pos_gaps = np.diff(pos_ps)
    report(f"  T>0 prime gaps: mean={pos_gaps.mean():.0f}, median={np.median(pos_gaps):.0f}, "
           f"std={pos_gaps.std():.0f}")
    report(f"    min={pos_gaps.min()}, max={pos_gaps.max()}")
    report(f"    quartiles: Q1={np.percentile(pos_gaps, 25):.0f}, Q3={np.percentile(pos_gaps, 75):.0f}")

if len(neg_ps) >= 2:
    neg_gaps = np.diff(neg_ps)
    report(f"  T<0 prime gaps: mean={neg_gaps.mean():.0f}, median={np.median(neg_gaps):.0f}, "
           f"std={neg_gaps.std():.0f}")
    report(f"    min={neg_gaps.min()}, max={neg_gaps.max()}")

report(f"  All M=-3 prime gaps: mean={all_gaps.mean():.0f}, median={np.median(all_gaps):.0f}")
report("")

# Normalized gaps
if len(pos_ps) >= 2:
    pos_norm_gaps = pos_gaps / pos_gaps.mean()
    report(f"  Normalized T>0 gaps: P(gap < 0.5*mean) = {np.mean(pos_norm_gaps < 0.5):.3f}")
    report(f"                       P(gap < 1.0*mean) = {np.mean(pos_norm_gaps < 1.0):.3f}")
    report(f"                       P(gap > 2.0*mean) = {np.mean(pos_norm_gaps > 2.0):.3f}")

report("")

# ===== Q6: ZETA ZERO RESONANCES =====
report("=" * 70)
report("Q6: ZETA ZERO RESONANCES")
report("=" * 70)
report("  Under GRH, M(x) ~ sum x^rho / rho where rho = 1/2 + i*gamma.")
report("  T(N) = sum_{m=2}^N M(N/m)/m involves M at multiple scales.")
report("  The leading oscillation of M(x) has period ~ 2*pi/gamma_1 in log(x).")
report("  gamma_1 ~ 14.1347 (first zeta zero imaginary part).")
report("")

gamma1 = 14.134725
gamma2 = 21.022040
gamma3 = 25.010858

# Check if T>0 primes cluster at particular phases of the zeta oscillation
# The oscillatory part of M(x) ~ -2*Re(x^(1/2+i*gamma_1) / (1/2+i*gamma_1))
# ~ -2*sqrt(x) * cos(gamma_1*log(x) - arg(1/2+i*gamma_1)) / |1/2+i*gamma_1|

phases_1 = (gamma1 * logps) % (2 * np.pi)
phases_2 = (gamma2 * logps) % (2 * np.pi)

# Compare phase distributions
n_bins = 12
report(f"  Phase of gamma_1 * log(p) mod 2pi (bins of pi/6):")
for i in range(n_bins):
    lo_phase = 2 * np.pi * i / n_bins
    hi_phase = 2 * np.pi * (i + 1) / n_bins
    mask_phase = (phases_1 >= lo_phase) & (phases_1 < hi_phase)
    n_phase = np.sum(mask_phase)
    n_phase_pos = np.sum(is_pos[mask_phase])
    frac = n_phase_pos / n_phase if n_phase > 0 else 0
    report(f"    [{lo_phase:.2f}, {hi_phase:.2f}): n={n_phase:>4}, T>0={n_phase_pos:>3}, frac={frac:.3f}")

# Circular mean test
from scipy import stats as scipy_stats
try:
    # Watson two-sample test or simpler: compare means
    pos_phases = phases_1[is_pos]
    neg_phases = phases_1[~is_pos]
    # Circular mean
    cm_pos = np.arctan2(np.mean(np.sin(pos_phases)), np.mean(np.cos(pos_phases)))
    cm_neg = np.arctan2(np.mean(np.sin(neg_phases)), np.mean(np.cos(neg_phases)))
    R_pos = np.sqrt(np.mean(np.cos(pos_phases))**2 + np.mean(np.sin(pos_phases))**2)
    R_neg = np.sqrt(np.mean(np.cos(neg_phases))**2 + np.mean(np.sin(neg_phases))**2)
    report(f"\n  Circular mean (gamma_1 phase): T>0 = {cm_pos:.3f}, T<0 = {cm_neg:.3f}")
    report(f"  Resultant length: T>0 = {R_pos:.4f}, T<0 = {R_neg:.4f}")
    report(f"  (Resultant ~ 0 means uniform; > 0.1 means clustering)")
except:
    report("  (scipy not available for circular stats)")

report("")

# ===== Q7: RUBINSTEIN-SARNAK PREDICTION =====
report("=" * 70)
report("Q7: RUBINSTEIN-SARNAK PREDICTION / ASYMPTOTIC DENSITY")
report("=" * 70)
report("  Rubinstein-Sarnak (1994) showed the logarithmic density of")
report("  {x : pi(x) > li(x)} is about 0.00000026 (Chebyshev bias).")
report("  The density of {N : M(N) > 0} is about 0 (Mertens oscillation).")
report("  For T(N) = sum M(N/m)/m, T is a smoothed/averaged version of M.")
report("  The smoothing should INCREASE the fraction of positive values")
report("  (since averaging reduces extreme negative excursions).")
report("")

# Running fraction of T>0
report("  Running fraction of T>0 among first k M=-3 primes:")
cum_pos = np.cumsum(is_pos)
for k in [50, 100, 174, 200, 300, 400, 500, 600, 700, 800, 900, 922]:
    if k <= n_total:
        frac = cum_pos[k-1] / k
        report(f"    k={k:>4}: fraction = {frac:.4f} (count={int(cum_pos[k-1])})")

# Check if the fraction is stabilizing, increasing, or decreasing
# Use windows of 100
report("\n  Fraction in sliding windows of 100 primes:")
for start in range(0, n_total - 99, 100):
    end = start + 100
    frac = np.mean(is_pos[start:end])
    p_lo, p_hi = ps[start], ps[min(end-1, n_total-1)]
    report(f"    primes [{start+1}-{end}] (p in [{p_lo}, {p_hi}]): frac = {frac:.3f}")

report("")

# ===== ADDITIONAL: T(N) statistics in windows =====
report("=" * 70)
report("ADDITIONAL: T(N) statistics by decade")
report("=" * 70)

for k in range(1, 8):
    lo, hi = 10**k, 10**(k+1)
    mask = (ps >= lo) & (ps < hi)
    if np.sum(mask) == 0:
        continue
    T_win = Ts[mask]
    report(f"  [{lo:>10}, {hi:>10}): mean T = {T_win.mean():>10.3f}, "
           f"std = {T_win.std():>8.3f}, min = {T_win.min():>10.3f}, max = {T_win.max():>10.3f}")

report("")

# ===== PLOTS =====
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.suptitle("Density Patterns: T(N) > 0 among M(p)=-3 primes to 10^7", fontsize=14, fontweight='bold')

# Panel 1: T(N) vs log(p)
ax = axes[0, 0]
ax.scatter(logps[~is_pos], Ts[~is_pos], c='blue', s=3, alpha=0.5, label='T<0')
ax.scatter(logps[is_pos], Ts[is_pos], c='red', s=6, alpha=0.7, label='T>0')
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_xlabel('log(p)')
ax.set_ylabel('T(N)')
ax.set_title('T(N) vs log(p) for all 922 M(p)=-3 primes')
ax.legend(fontsize=8)

# Panel 2: Running fraction of T>0
ax = axes[0, 1]
running_frac = cum_pos / (np.arange(1, n_total+1))
ax.plot(logps, running_frac, 'k-', linewidth=1)
ax.axhline(y=0.268, color='red', linewidth=0.5, linestyle='--', label='overall 26.8%')
ax.set_xlabel('log(p)')
ax.set_ylabel('Fraction T>0')
ax.set_title('Running fraction of T(N) > 0')
ax.legend(fontsize=8)
ax.set_ylim([0, 0.5])

# Panel 3: Histogram of T(N)
ax = axes[0, 2]
ax.hist(Ts, bins=80, color='steelblue', edgecolor='black', linewidth=0.3)
ax.axvline(x=0, color='red', linewidth=1.5, label='T=0')
ax.set_xlabel('T(N)')
ax.set_ylabel('Count')
ax.set_title('Distribution of T(N) values')
ax.legend(fontsize=8)

# Panel 4: T>0 fraction by decade
ax = axes[1, 0]
decades = []
fracs_by_decade = []
for k in range(1, 8):
    lo, hi = 10**k, 10**(k+1)
    mask = (ps >= lo) & (ps < hi)
    if np.sum(mask) > 0:
        decades.append(k + 0.5)
        fracs_by_decade.append(np.mean(is_pos[mask]))
ax.bar(decades, fracs_by_decade, width=0.7, color='coral', edgecolor='black')
ax.set_xlabel('Decade (10^k to 10^{k+1})')
ax.set_ylabel('Fraction T>0')
ax.set_title('Q1: Density trend by decade')
ax.set_xticks(decades)
ax.set_xticklabels([f"10^{int(d-0.5)}-10^{int(d+0.5)}" for d in decades], rotation=30, fontsize=7)

# Panel 5: Run length distribution
ax = axes[1, 1]
if runs_pos:
    max_run = max(max(runs_pos), 15)
    bins_run = np.arange(0.5, min(max_run, 30) + 1.5, 1)
    ax.hist(runs_pos, bins=bins_run, alpha=0.7, color='red', label='T>0 runs', edgecolor='black')
    ax.hist(runs_neg, bins=bins_run, alpha=0.5, color='blue', label='T<0 runs', edgecolor='black')
    ax.set_xlabel('Run length')
    ax.set_ylabel('Count')
    ax.set_title('Q2: Run length distribution')
    ax.legend(fontsize=8)
    ax.set_xlim([0, 30])

# Panel 6: T(N) vs M(N/2)
ax = axes[1, 2]
ax.scatter(M_half, Ts, c=['red' if p else 'blue' for p in is_pos], s=5, alpha=0.5)
ax.set_xlabel('M(N/2)')
ax.set_ylabel('T(N)')
ax.set_title('Q3: T(N) vs M(N/2)')
ax.axhline(y=0, color='black', linewidth=0.5)
ax.axvline(x=0, color='black', linewidth=0.5)

# Panel 7: Zeta zero phase
ax = axes[2, 0]
n_bins_plot = 24
bin_edges = np.linspace(0, 2*np.pi, n_bins_plot+1)
pos_hist, _ = np.histogram(phases_1[is_pos], bins=bin_edges)
all_hist, _ = np.histogram(phases_1, bins=bin_edges)
frac_hist = np.where(all_hist > 0, pos_hist / all_hist, 0)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
ax.bar(bin_centers, frac_hist, width=2*np.pi/n_bins_plot*0.8, color='purple', alpha=0.7, edgecolor='black')
ax.axhline(y=np.mean(is_pos), color='red', linestyle='--', label=f'overall {np.mean(is_pos):.3f}')
ax.set_xlabel('gamma_1 * log(p) mod 2pi')
ax.set_ylabel('Fraction T>0')
ax.set_title('Q6: Zeta zero phase dependence')
ax.legend(fontsize=8)

# Panel 8: T(N) vs leading terms M(N/2)/2 + M(N/3)/3
ax = axes[2, 1]
ax.scatter(leading_term, Ts, c=['red' if p else 'blue' for p in is_pos], s=5, alpha=0.5)
ax.plot([leading_term.min(), leading_term.max()],
        [leading_term.min(), leading_term.max()], 'k--', linewidth=0.5, label='y=x')
ax.set_xlabel('M(N/2)/2 + M(N/3)/3')
ax.set_ylabel('T(N)')
ax.set_title('T(N) vs leading terms')
ax.legend(fontsize=8)

# Panel 9: Gap distribution
ax = axes[2, 2]
if len(pos_ps) >= 2 and len(neg_ps) >= 2:
    pos_gaps = np.diff(pos_ps)
    neg_gaps = np.diff(neg_ps)
    max_gap_plot = np.percentile(np.concatenate([pos_gaps, neg_gaps]), 95)
    bins_gap = np.linspace(0, max_gap_plot, 50)
    ax.hist(pos_gaps, bins=bins_gap, alpha=0.6, color='red', label='T>0 gaps', density=True)
    ax.hist(neg_gaps, bins=bins_gap, alpha=0.4, color='blue', label='T<0 gaps', density=True)
    ax.set_xlabel('Gap between consecutive primes')
    ax.set_ylabel('Density')
    ax.set_title('Q5: Spacing distribution')
    ax.legend(fontsize=8)

plt.tight_layout()
plot_path = os.path.join(DATA_DIR, "density_patterns_plots.png")
plt.savefig(plot_path, dpi=150)
print(f"\nPlots saved to {plot_path}")

# Save analysis
analysis_path = os.path.join(DATA_DIR, "density_patterns_analysis.txt")
with open(analysis_path, "w") as f:
    f.write("\n".join(out_lines))
print(f"Analysis saved to {analysis_path}")
