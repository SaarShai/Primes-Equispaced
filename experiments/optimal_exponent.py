#!/usr/bin/env python3
"""
Optimal Compensation Exponent for the Mertens Spectroscope
===========================================================

The compensated periodogram is F_alpha(gamma) = |S(gamma)|^2 * gamma^alpha.
Currently alpha=2 is used. This script tests a range of exponents and two
log-hybrid forms to find the exponent that maximizes MINIMUM z-score
across all 20 known zeta zeros (minimax criterion).

Sieve Mobius to 1,000,000 (78,498 primes).
Spectroscope: S(gamma) = sum M(p)/p * exp(-i*gamma*log(p)) on [5,85], 20000 pts.

Author: Saar (with Claude assistance)
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
import time
import os
import gc

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Paths ────────────────────────────────────────────────────────────
FIG_DIR = os.path.expanduser("~/Desktop/Farey-Local/figures")
EXP_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")
os.makedirs(FIG_DIR, exist_ok=True)

# ── Known zeta zeros (imaginary parts) ───────────────────────────────
ZEROS = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
         37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
         52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
         67.0798, 69.5464, 72.0672, 75.7047, 77.1448]

# ── Parameters ───────────────────────────────────────────────────────
MAX_N = 1_000_000
N_GAMMA = 20_000
GAMMA_MIN, GAMMA_MAX = 5.0, 85.0
LOCAL_WINDOW = 8.0
EXCLUSION_RADIUS = 1.5
GAMMA_CHUNK = 1000
PRIME_CHUNK = 80_000

ALPHA_VALUES = [0.0, 0.5, 1.0, 1.5, 1.8, 2.0, 2.2, 2.5, 3.0]
SPECIAL_LABELS = ["gamma^2 * log(gamma)", "gamma^2 / log(gamma)"]


# =====================================================================
# Sieve
# =====================================================================
def linear_sieve_mobius(MAX_N):
    t0 = time.time()
    mu = np.zeros(MAX_N + 1, dtype=np.int8)
    mu[1] = 1
    is_composite = np.zeros(MAX_N + 1, dtype=np.bool_)
    primes_list = []

    for i in range(2, MAX_N + 1):
        if not is_composite[i]:
            primes_list.append(i)
            mu[i] = -1
        for p in primes_list:
            ip = i * p
            if ip > MAX_N:
                break
            is_composite[ip] = True
            if i % p == 0:
                mu[ip] = 0
                break
            mu[ip] = -mu[i]

    elapsed = time.time() - t0
    print(f"  Linear sieve to {MAX_N:,}: {len(primes_list):,} primes, {elapsed:.1f}s")
    del is_composite
    gc.collect()
    return mu, primes_list


# =====================================================================
# Mertens at primes
# =====================================================================
def compute_mertens_at_primes(mu, primes_list):
    t0 = time.time()
    M = np.cumsum(mu)
    M_p = np.array([M[p] for p in primes_list], dtype=np.float64)
    elapsed = time.time() - t0
    print(f"  Mertens at primes: {elapsed:.1f}s, M range [{M_p.min():.0f}, {M_p.max():.0f}]")
    del M
    gc.collect()
    return M_p


# =====================================================================
# Spectroscope: compute raw S(gamma) = sum M(p)/p * exp(-i*gamma*log(p))
# Returns |S|^2 (power spectrum), before any compensation
# =====================================================================
def spectroscope_raw(gammas, log_p, amp):
    G = len(gammas)
    N = len(log_p)
    S_re = np.zeros(G, dtype=np.float64)
    S_im = np.zeros(G, dtype=np.float64)

    total_chunks = ((G + GAMMA_CHUNK - 1) // GAMMA_CHUNK) * \
                   ((N + PRIME_CHUNK - 1) // PRIME_CHUNK)
    chunk_count = 0
    t0 = time.time()

    for g_start in range(0, G, GAMMA_CHUNK):
        g_end = min(g_start + GAMMA_CHUNK, G)
        g_slice = gammas[g_start:g_end]

        for p_start in range(0, N, PRIME_CHUNK):
            p_end = min(p_start + PRIME_CHUNK, N)
            lp = log_p[p_start:p_end]
            a = amp[p_start:p_end]

            phases = np.outer(g_slice, lp)
            S_re[g_start:g_end] += np.cos(phases) @ a
            S_im[g_start:g_end] -= np.sin(phases) @ a

            del phases
            chunk_count += 1

            if chunk_count % 20 == 0 or chunk_count == total_chunks:
                elapsed = time.time() - t0
                pct = chunk_count / total_chunks * 100
                rate = chunk_count / elapsed if elapsed > 0 else 0
                eta = (total_chunks - chunk_count) / rate if rate > 0 else 0
                print(f"    Chunk {chunk_count}/{total_chunks} ({pct:.0f}%), "
                      f"elapsed={elapsed:.0f}s, ETA={eta:.0f}s", flush=True)

    power = S_re**2 + S_im**2
    total_time = time.time() - t0
    print(f"  Spectroscope done: {total_time:.1f}s, "
          f"{G} gammas x {N} primes = {G*N/1e9:.2f}G ops")
    return power


# =====================================================================
# Local z-score
# =====================================================================
def local_zscore(F, gammas, target_gamma, window=LOCAL_WINDOW,
                 exclusion=EXCLUSION_RADIUS, known_zeros=ZEROS):
    peak_mask = (gammas >= target_gamma - 1.2) & (gammas <= target_gamma + 1.2)
    if not peak_mask.any():
        return np.nan, np.nan, np.nan

    peak_indices = np.where(peak_mask)[0]
    best_local = np.argmax(F[peak_indices])
    peak_idx = peak_indices[best_local]
    peak_gamma = gammas[peak_idx]
    peak_val = F[peak_idx]

    bg_mask = (gammas >= target_gamma - window) & (gammas <= target_gamma + window)
    for gz in known_zeros:
        exclude = (gammas >= gz - exclusion) & (gammas <= gz + exclusion)
        bg_mask = bg_mask & ~exclude

    if bg_mask.sum() < 10:
        return peak_gamma, peak_val, np.nan

    bg_vals = F[bg_mask]
    bg_mean = np.mean(bg_vals)
    bg_std = np.std(bg_vals)

    if bg_std < 1e-30:
        return peak_gamma, peak_val, np.nan

    z = (peak_val - bg_mean) / bg_std
    return peak_gamma, peak_val, z


# =====================================================================
# Evaluate one compensation function
# =====================================================================
def evaluate_compensation(power, gammas, comp_func, label):
    F = power * comp_func
    zscores = []
    for gz in ZEROS:
        _, _, z = local_zscore(F, gammas, gz)
        zscores.append(z)
    zscores = np.array(zscores)
    valid = ~np.isnan(zscores)
    n_valid = valid.sum()
    n_detected = (zscores[valid] > 2.0).sum() if n_valid > 0 else 0
    avg_z = np.nanmean(zscores) if n_valid > 0 else np.nan
    med_z = np.nanmedian(zscores) if n_valid > 0 else np.nan
    min_z = np.nanmin(zscores) if n_valid > 0 else np.nan
    max_z = np.nanmax(zscores) if n_valid > 0 else np.nan
    return {
        'label': label,
        'zscores': zscores,
        'avg_z': avg_z,
        'med_z': med_z,
        'min_z': min_z,
        'max_z': max_z,
        'n_detected': n_detected,
        'n_valid': n_valid
    }


# =====================================================================
# Main
# =====================================================================
def main():
    print("=" * 70)
    print("OPTIMAL COMPENSATION EXPONENT FOR MERTENS SPECTROSCOPE")
    print("=" * 70)
    t_start = time.time()

    # Step 1: Sieve
    print("\n[1] Sieving Mobius function ...")
    mu, primes = linear_sieve_mobius(MAX_N)
    print(f"    {len(primes):,} primes up to {MAX_N:,}")

    # Step 2: Mertens at primes
    print("\n[2] Computing Mertens values at primes ...")
    M_p = compute_mertens_at_primes(mu, primes)
    del mu
    gc.collect()

    primes_arr = np.array(primes, dtype=np.float64)
    log_p = np.log(primes_arr)
    amp = M_p / primes_arr  # weights: M(p)/p

    # Step 3: Raw spectroscope (compute once, reuse for all alphas)
    print("\n[3] Computing raw spectroscope |S(gamma)|^2 ...")
    gammas = np.linspace(GAMMA_MIN, GAMMA_MAX, N_GAMMA)
    power = spectroscope_raw(gammas, log_p, amp)

    # Step 4: Test all compensation exponents
    print("\n[4] Testing compensation exponents ...")
    results = []

    # Pure power-law: gamma^alpha
    for alpha in ALPHA_VALUES:
        label = f"gamma^{alpha}"
        comp = gammas ** alpha
        r = evaluate_compensation(power, gammas, comp, label)
        r['alpha'] = alpha
        r['is_special'] = False
        results.append(r)
        print(f"  {label:25s}: avg_z={r['avg_z']:6.2f}  med_z={r['med_z']:6.2f}  "
              f"min_z={r['min_z']:6.2f}  max_z={r['max_z']:6.2f}  "
              f"detected={r['n_detected']}/{r['n_valid']}")

    # Special: gamma^2 * log(gamma)
    label = "gamma^2 * log(gamma)"
    comp = gammas**2 * np.log(gammas)
    r = evaluate_compensation(power, gammas, comp, label)
    r['alpha'] = 2.0
    r['is_special'] = True
    results.append(r)
    print(f"  {label:25s}: avg_z={r['avg_z']:6.2f}  med_z={r['med_z']:6.2f}  "
          f"min_z={r['min_z']:6.2f}  max_z={r['max_z']:6.2f}  "
          f"detected={r['n_detected']}/{r['n_valid']}")

    # Special: gamma^2 / log(gamma)
    label = "gamma^2 / log(gamma)"
    comp = gammas**2 / np.log(gammas)
    r = evaluate_compensation(power, gammas, comp, label)
    r['alpha'] = 2.0
    r['is_special'] = True
    results.append(r)
    print(f"  {label:25s}: avg_z={r['avg_z']:6.2f}  med_z={r['med_z']:6.2f}  "
          f"min_z={r['min_z']:6.2f}  max_z={r['max_z']:6.2f}  "
          f"detected={r['n_detected']}/{r['n_valid']}")

    # Step 5: Fine grid around best alpha
    print("\n[5] Fine-grid search around best alpha ...")
    power_law_results = [r for r in results if not r['is_special']]
    best_coarse = max(power_law_results, key=lambda r: r['min_z'])
    best_alpha_coarse = best_coarse['alpha']
    print(f"    Best coarse alpha = {best_alpha_coarse} (min_z = {best_coarse['min_z']:.3f})")

    fine_alphas = np.arange(
        max(0, best_alpha_coarse - 0.5),
        best_alpha_coarse + 0.55,
        0.05
    )
    fine_alphas = [a for a in fine_alphas if a not in ALPHA_VALUES]

    fine_results = []
    for alpha in fine_alphas:
        label = f"gamma^{alpha:.2f}"
        comp = gammas ** alpha
        r = evaluate_compensation(power, gammas, comp, label)
        r['alpha'] = alpha
        r['is_special'] = False
        fine_results.append(r)
        print(f"  {label:25s}: avg_z={r['avg_z']:6.2f}  med_z={r['med_z']:6.2f}  "
              f"min_z={r['min_z']:6.2f}  detected={r['n_detected']}/{r['n_valid']}")

    all_results = results + fine_results

    # Step 6: Find overall best (minimax criterion)
    print("\n[6] RESULTS SUMMARY")
    print("-" * 90)
    print(f"{'Compensation':28s} {'avg_z':>8s} {'med_z':>8s} {'min_z':>8s} {'max_z':>8s} {'detected':>10s}")
    print("-" * 90)

    # Sort by min_z descending
    all_sorted = sorted(all_results, key=lambda r: r['min_z'] if not np.isnan(r['min_z']) else -999, reverse=True)
    for r in all_sorted:
        marker = " ***" if r == all_sorted[0] else ""
        print(f"  {r['label']:26s} {r['avg_z']:8.3f} {r['med_z']:8.3f} "
              f"{r['min_z']:8.3f} {r['max_z']:8.3f} {r['n_detected']:5d}/20{marker}")

    best = all_sorted[0]
    print(f"\n  OPTIMAL (minimax): {best['label']}  (min z-score = {best['min_z']:.3f})")

    # Also report best by average
    best_avg = max(all_results, key=lambda r: r['avg_z'] if not np.isnan(r['avg_z']) else -999)
    print(f"  BEST (avg z):     {best_avg['label']}  (avg z-score = {best_avg['avg_z']:.3f})")

    # Also report best by detection count
    best_det = max(all_results, key=lambda r: r['n_detected'])
    print(f"  BEST (detection): {best_det['label']}  ({best_det['n_detected']}/20 detected)")

    # Step 7: Per-zero z-score table for top 5
    print("\n[7] Per-zero z-scores for top 5 compensations:")
    top5 = all_sorted[:5]
    header = f"{'gamma':>8s}"
    for r in top5:
        header += f" {r['label']:>14s}"
    print(header)
    print("-" * (8 + 15 * len(top5)))
    for i, gz in enumerate(ZEROS):
        row = f"{gz:8.4f}"
        for r in top5:
            z = r['zscores'][i]
            row += f" {z:14.2f}"
        print(row)

    # Step 8: Plots
    print("\n[8] Generating plots ...")

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Optimal Compensation Exponent for Mertens Spectroscope\n"
                 f"N = {MAX_N:,}, {len(primes):,} primes, {N_GAMMA:,} gamma points on [5, 85]",
                 fontsize=13, fontweight='bold')

    # Filter to power-law only for clean alpha-axis plots
    pw_results = sorted([r for r in all_results if not r['is_special']],
                        key=lambda r: r['alpha'])
    alphas_plot = [r['alpha'] for r in pw_results]
    avg_zs = [r['avg_z'] for r in pw_results]
    min_zs = [r['min_z'] for r in pw_results]
    n_dets = [r['n_detected'] for r in pw_results]

    # Panel 1: avg z-score vs alpha
    ax = axes[0]
    ax.plot(alphas_plot, avg_zs, 'b.-', markersize=8, linewidth=1.5)
    ax.set_xlabel(r'$\alpha$', fontsize=12)
    ax.set_ylabel('Average z-score', fontsize=12)
    ax.set_title('Mean z-score across 20 zeros')
    ax.axhline(y=2, color='r', linestyle='--', alpha=0.5, label='z=2 threshold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Mark the special forms
    for r in all_results:
        if r['is_special']:
            ax.axhline(y=r['avg_z'], color='green', linestyle=':', alpha=0.6,
                       label=r['label'])
    ax.legend(fontsize=8)

    # Panel 2: min z-score vs alpha
    ax = axes[1]
    ax.plot(alphas_plot, min_zs, 'r.-', markersize=8, linewidth=1.5)
    ax.set_xlabel(r'$\alpha$', fontsize=12)
    ax.set_ylabel('Minimum z-score', fontsize=12)
    ax.set_title('Min z-score (minimax criterion)')
    ax.axhline(y=2, color='gray', linestyle='--', alpha=0.5, label='z=2 threshold')
    ax.grid(True, alpha=0.3)

    # Highlight optimal
    opt_alpha = best['alpha'] if not best['is_special'] else 2.0
    opt_min_z = best['min_z']
    ax.plot(opt_alpha, opt_min_z, 'k*', markersize=15, zorder=5,
            label=f'Optimal: {best["label"]}')
    ax.legend(fontsize=9)

    # Panel 3: detection count vs alpha
    ax = axes[2]
    ax.plot(alphas_plot, n_dets, 'g.-', markersize=8, linewidth=1.5)
    ax.set_xlabel(r'$\alpha$', fontsize=12)
    ax.set_ylabel('Zeros detected (z > 2)', fontsize=12)
    ax.set_title('Detection count')
    ax.set_ylim(-0.5, 21)
    ax.axhline(y=20, color='gray', linestyle='--', alpha=0.5, label='All 20')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)

    plt.tight_layout()
    fig_path = os.path.join(FIG_DIR, "optimal_exponent.png")
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"  Figure saved: {fig_path}")
    plt.close(fig)

    # Step 9: Save results to markdown
    print("\n[9] Saving results ...")
    md_path = os.path.join(EXP_DIR, "OPTIMAL_EXPONENT_RESULTS.md")
    with open(md_path, 'w') as f:
        f.write("# Optimal Compensation Exponent for Mertens Spectroscope\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Setup\n\n")
        f.write(f"- Mobius sieve to N = {MAX_N:,}\n")
        f.write(f"- Primes used: {len(primes):,}\n")
        f.write(f"- Gamma range: [{GAMMA_MIN}, {GAMMA_MAX}], {N_GAMMA:,} points\n")
        f.write(f"- Z-score: local window = {LOCAL_WINDOW}, exclusion = {EXCLUSION_RADIUS}\n")
        f.write(f"- Detection threshold: z > 2\n\n")

        f.write("## Summary Table\n\n")
        f.write("| Compensation | Avg z | Med z | Min z | Max z | Detected |\n")
        f.write("|:---|---:|---:|---:|---:|---:|\n")
        for r in all_sorted:
            marker = " **BEST**" if r == all_sorted[0] else ""
            f.write(f"| {r['label']}{marker} | {r['avg_z']:.3f} | {r['med_z']:.3f} | "
                    f"{r['min_z']:.3f} | {r['max_z']:.3f} | {r['n_detected']}/20 |\n")

        f.write(f"\n## Optimal Result\n\n")
        f.write(f"**Minimax criterion (maximizes minimum z-score):** `{best['label']}`\n\n")
        f.write(f"- Min z-score: {best['min_z']:.3f}\n")
        f.write(f"- Avg z-score: {best['avg_z']:.3f}\n")
        f.write(f"- Detected: {best['n_detected']}/20 zeros\n\n")

        if best_avg != best:
            f.write(f"**Best average z-score:** `{best_avg['label']}` (avg = {best_avg['avg_z']:.3f})\n\n")

        f.write("## Per-Zero z-Scores (Top 5 Compensations)\n\n")
        header = "| gamma |"
        for r in top5:
            header += f" {r['label']} |"
        f.write(header + "\n")
        sep = "|---:|"
        for _ in top5:
            sep += "---:|"
        f.write(sep + "\n")
        for i, gz in enumerate(ZEROS):
            row = f"| {gz:.4f} |"
            for r in top5:
                z = r['zscores'][i]
                row += f" {z:.2f} |"
            f.write(row + "\n")

        f.write(f"\n## Interpretation\n\n")
        f.write("The compensation gamma^alpha corrects for the natural decay of peak heights "
                "at higher frequencies. The explicit formula predicts peak height ~ 1/|rho * zeta'(rho)|, "
                "which grows roughly as gamma for large gamma. The power spectrum |S|^2 thus decays "
                "roughly as 1/gamma^2, motivating the gamma^2 baseline.\n\n")
        f.write(f"![Optimal Exponent](../figures/optimal_exponent.png)\n")

    print(f"  Results saved: {md_path}")

    total_time = time.time() - t_start
    print(f"\nTotal runtime: {total_time:.1f}s")
    print("DONE.")


if __name__ == "__main__":
    main()
