#!/usr/bin/env python3
"""
Per-denominator Cauchy-Schwarz approach to proving |R| < 1.

We decompose:
  Σ D·δ = Σ_b C_b  where C_b = Σ_{a coprime b} D(a/b)·δ(a/b)

Since Σ_a δ(a/b) = 0 for each b (coprime permutation), C_b is a covariance:
  |C_b| ≤ SD_b(D) · SD_b(δ) · φ(b)   by Cauchy-Schwarz.

And Σδ² = Σ_b φ(b)·Var_b(δ) = Σ_b φ(b)·SD_b(δ)².

We need: |Σ D·δ| < (1/2)·Σδ²
i.e.:  Σ_b SD_b(D)·SD_b(δ)·φ(b) < (1/2)·Σ_b φ(b)·SD_b(δ)²
i.e.:  Σ_b φ(b)·SD_b(δ)·[SD_b(δ)/2 - SD_b(D)] > 0

This holds if SD_b(D) < SD_b(δ)/2 for most b (weighted by φ(b)·SD_b(δ)).

We compute these quantities exactly for several primes and analyze the ratios.
"""

import time
from fractions import Fraction
from math import gcd, isqrt, sqrt
from collections import defaultdict

start_time = time.time()

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def farey_sequence_sorted(N):
    """Return sorted Farey sequence F_N as list of (a, b) tuples."""
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: x[0] / x[1])
    return fracs


def analyze_prime(p):
    """
    For prime p, compute per-denominator SD(D), SD(δ), and the ratio.
    Returns dict with all per-denom data and global aggregates.
    """
    N = p - 1
    fracs = farey_sequence_sorted(N)
    n = len(fracs)

    # Group by denominator, compute D and δ for each fraction
    by_denom = defaultdict(list)
    for j, (a, b) in enumerate(fracs):
        if (a == 0 and b == 1) or (a == 1 and b == 1):
            continue
        D = Fraction(j) - Fraction(n * a, b)
        pa_mod_b = (p * a) % b
        delta = Fraction(a - pa_mod_b, b)
        by_denom[b].append((a, D, delta))

    per_denom = {}
    for b in sorted(by_denom.keys()):
        entries = by_denom[b]
        phi_b = len(entries)

        # Means
        mean_D = sum(e[1] for e in entries) / phi_b
        mean_delta = sum(e[2] for e in entries) / phi_b

        # Variances
        var_D = sum((e[1] - mean_D)**2 for e in entries) / phi_b
        var_delta = sum((e[2] - mean_delta)**2 for e in entries) / phi_b

        # Cross term C_b = Σ (D - mean_D)(δ - mean_δ) = Σ D·δ - φ(b)·mean_D·mean_δ
        # But since mean_delta ≈ 0 (exact for coprime permutation), C_b ≈ Σ D·δ
        cross = sum((e[1] - mean_D) * (e[2] - mean_delta) for e in entries) / phi_b

        sd_D = sqrt(float(var_D)) if var_D > 0 else 0.0
        sd_delta = sqrt(float(var_delta)) if var_delta > 0 else 0.0
        ratio = sd_D / sd_delta if sd_delta > 0 else float('inf')

        per_denom[b] = {
            'phi_b': phi_b,
            'mean_D': float(mean_D),
            'mean_delta': float(mean_delta),
            'var_D': var_D,
            'var_delta': var_delta,
            'sd_D': sd_D,
            'sd_delta': sd_delta,
            'ratio': ratio,  # SD_b(D) / SD_b(δ)
            'cross': cross,  # covariance
        }

    return per_denom


def compute_global_bound(per_denom):
    """
    Check whether the per-denom Cauchy-Schwarz bound gives |R| < 1.

    CS bound: |Σ D·δ| ≤ Σ_b φ(b)·SD_b(D)·SD_b(δ)
    Denominator: Σδ² = Σ_b φ(b)·SD_b(δ)²  (since mean_δ ≈ 0)

    So |R| = 2|Σ D·δ|/Σδ² ≤ 2·Σ_b φ(b)·SD_b(D)·SD_b(δ) / Σ_b φ(b)·SD_b(δ)²

    We want this < 1, i.e. need:
      Σ_b φ(b)·SD_b(δ)·[SD_b(δ)/2 - SD_b(D)] > 0
    """
    numerator_CS = 0.0  # Σ_b φ(b)·SD_b(D)·SD_b(δ)
    denominator = 0.0   # Σ_b φ(b)·SD_b(δ)²
    surplus = 0.0       # Σ_b φ(b)·SD_b(δ)·[SD_b(δ)/2 - SD_b(D)]

    # Also compute actual cross term
    actual_cross = 0.0  # Σ_b φ(b)·cov_b

    # Weighted average ratio
    weight_sum = 0.0
    weighted_ratio_sum = 0.0

    for b, data in per_denom.items():
        phi_b = data['phi_b']
        sd_D = data['sd_D']
        sd_delta = data['sd_delta']
        cov = float(data['cross'])

        numerator_CS += phi_b * sd_D * sd_delta
        denominator += phi_b * sd_delta**2
        surplus += phi_b * sd_delta * (sd_delta / 2 - sd_D)
        actual_cross += phi_b * cov

        w = phi_b * sd_delta
        weight_sum += w
        weighted_ratio_sum += w * data['ratio']

    R_bound = 2 * numerator_CS / denominator if denominator > 0 else float('inf')
    R_actual = 2 * actual_cross / denominator if denominator > 0 else 0.0
    avg_ratio = weighted_ratio_sum / weight_sum if weight_sum > 0 else float('inf')

    return {
        'R_bound_CS': R_bound,
        'R_actual': R_actual,
        'surplus': surplus,
        'weighted_avg_ratio': avg_ratio,
        'numerator_CS': numerator_CS,
        'denominator': denominator,
    }


def print_denom_table(per_denom, top_n=20):
    """Print a table of per-denominator stats, sorted by φ(b)·SD(δ) weight."""
    items = [(b, d) for b, d in per_denom.items() if d['sd_delta'] > 0]
    items.sort(key=lambda x: -x[1]['phi_b'] * x[1]['sd_delta'])

    print(f"  {'b':>4} {'φ(b)':>5} {'SD(D)':>10} {'SD(δ)':>10} {'ratio':>8} {'δ/2-D':>10} {'weight':>10}")
    print(f"  {'':->4} {'':->5} {'':->10} {'':->10} {'':->8} {'':->10} {'':->10}")
    for b, d in items[:top_n]:
        gap = d['sd_delta'] / 2 - d['sd_D']
        weight = d['phi_b'] * d['sd_delta']
        print(f"  {b:4d} {d['phi_b']:5d} {d['sd_D']:10.4f} {d['sd_delta']:10.4f} "
              f"{d['ratio']:8.4f} {gap:10.4f} {weight:10.2f}")

    # Count how many have ratio < 0.5
    below = sum(1 for _, d in items if d['ratio'] < 0.5)
    above = sum(1 for _, d in items if d['ratio'] >= 0.5)
    print(f"  Denominators with ratio < 0.5: {below}/{below+above}")


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    primes = sieve_primes(500)
    test_primes = [p for p in primes if p >= 11]

    # For quick overview, use a selection
    overview_primes = [p for p in test_primes if p <= 100] + [p for p in test_primes if p > 100 and p <= 500][::3]

    print("=" * 80)
    print("PER-DENOMINATOR CAUCHY-SCHWARZ ANALYSIS")
    print("=" * 80)
    print()

    results = []

    for p in overview_primes:
        t0 = time.time()
        per_denom = analyze_prime(p)
        gb = compute_global_bound(per_denom)
        elapsed = time.time() - t0

        results.append((p, gb))

        print(f"p = {p:4d}  |  R_actual = {gb['R_actual']:+.6f}  |  "
              f"R_bound(CS) = {gb['R_bound_CS']:.6f}  |  "
              f"avg_ratio = {gb['weighted_avg_ratio']:.4f}  |  "
              f"surplus = {gb['surplus']:+.2f}  |  {elapsed:.2f}s")

    print()
    print("=" * 80)
    print("DETAILED ANALYSIS FOR SELECTED PRIMES")
    print("=" * 80)

    for p in [11, 13, 23, 37, 53, 97, 199, 307]:
        if p not in [q for q in sieve_primes(500)]:
            continue
        print(f"\n--- p = {p} ---")
        per_denom = analyze_prime(p)
        print_denom_table(per_denom)
        gb = compute_global_bound(per_denom)
        print(f"  R_actual = {gb['R_actual']:+.6f}")
        print(f"  R_bound(CS per-denom) = {gb['R_bound_CS']:.6f}")
        print(f"  Weighted avg SD(D)/SD(δ) = {gb['weighted_avg_ratio']:.4f}")
        print(f"  Surplus = {gb['surplus']:+.4f}")
        print(f"  BOUND PROVES |R|<1? {'YES' if gb['R_bound_CS'] < 1.0 else 'NO'}")

    print()
    print("=" * 80)
    print("SUMMARY: Does per-denom CS prove |R| < 1?")
    print("=" * 80)

    all_proved = True
    for p, gb in results:
        proved = gb['R_bound_CS'] < 1.0
        if not proved:
            all_proved = False
        mark = "OK" if proved else "FAIL"
        print(f"  p={p:4d}: R_bound={gb['R_bound_CS']:.4f}  avg_ratio={gb['weighted_avg_ratio']:.4f}  [{mark}]")

    print()
    if all_proved:
        print("ALL primes satisfy per-denom CS bound < 1. The approach works!")
    else:
        fails = [p for p, gb in results if gb['R_bound_CS'] >= 1.0]
        print(f"FAILED primes: {fails}")
        print("The naive per-denom CS is too loose for these primes.")

    # ============================================================
    # Additional analysis: distribution of ratios
    # ============================================================
    print()
    print("=" * 80)
    print("RATIO DISTRIBUTION for p=499")
    print("=" * 80)

    per_denom = analyze_prime(499)
    items = [(b, d) for b, d in per_denom.items() if d['sd_delta'] > 0]

    # Histogram of ratios
    bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 999]
    counts = [0] * (len(bins) - 1)
    weighted_counts = [0.0] * (len(bins) - 1)
    for b, d in items:
        r = d['ratio']
        w = d['phi_b'] * d['sd_delta']
        for i in range(len(bins) - 1):
            if bins[i] <= r < bins[i+1]:
                counts[i] += 1
                weighted_counts[i] += w
                break

    total_w = sum(weighted_counts)
    print(f"  {'Ratio range':>15} {'Count':>6} {'Weight':>10} {'Wt%':>8}")
    for i in range(len(bins) - 1):
        label = f"[{bins[i]:.1f}, {bins[i+1]:.1f})"
        pct = 100 * weighted_counts[i] / total_w if total_w > 0 else 0
        print(f"  {label:>15} {counts[i]:6d} {weighted_counts[i]:10.2f} {pct:7.1f}%")

    # Max ratio by weight
    items.sort(key=lambda x: -x[1]['ratio'])
    print(f"\n  Top 10 denominators by ratio SD(D)/SD(δ):")
    for b, d in items[:10]:
        print(f"    b={b:4d}  φ(b)={d['phi_b']:3d}  SD(D)={d['sd_D']:.4f}  "
              f"SD(δ)={d['sd_delta']:.4f}  ratio={d['ratio']:.4f}")

    # ============================================================
    # DIAGNOSTIC: Why is R_actual small but CS bound huge?
    # The C_b terms must CANCEL across b. Let's check.
    # ============================================================
    print()
    print("=" * 80)
    print("CANCELLATION ANALYSIS: Per-denom cross terms C_b")
    print("=" * 80)

    for p in [53, 97, 199, 499]:
        print(f"\n--- p = {p} ---")
        N = p - 1
        fracs = farey_sequence_sorted(N)
        n_total = len(fracs)

        by_denom = defaultdict(list)
        for j, (a, b) in enumerate(fracs):
            if (a == 0 and b == 1) or (a == 1 and b == 1):
                continue
            D = Fraction(j) - Fraction(n_total * a, b)
            pa_mod_b = (p * a) % b
            delta = Fraction(a - pa_mod_b, b)
            by_denom[b].append((a, D, delta))

        # C_b = Σ_{a coprime b} D(a/b)·δ(a/b)
        cb_list = []
        total_cross = Fraction(0)
        total_abs = Fraction(0)
        for b in sorted(by_denom.keys()):
            entries = by_denom[b]
            cb = sum(e[1] * e[2] for e in entries)
            cb_list.append((b, cb, len(entries)))
            total_cross += cb
            total_abs += abs(cb)

        cancellation_ratio = float(abs(total_cross)) / float(total_abs) if total_abs > 0 else 0
        print(f"  Σ C_b = {float(total_cross):.4f}")
        print(f"  Σ|C_b| = {float(total_abs):.4f}")
        print(f"  |Σ C_b| / Σ|C_b| = {cancellation_ratio:.6f}  (cancellation = {1-cancellation_ratio:.4f})")

        # Show top positive and negative C_b
        cb_list.sort(key=lambda x: float(x[1]))
        print(f"  Most negative C_b:")
        for b, cb, phi in cb_list[:5]:
            print(f"    b={b:4d}  φ(b)={phi:3d}  C_b={float(cb):+.4f}")
        print(f"  Most positive C_b:")
        for b, cb, phi in cb_list[-5:]:
            print(f"    b={b:4d}  φ(b)={phi:3d}  C_b={float(cb):+.4f}")

    # ============================================================
    # APPROACH 2: D_fluct decomposition
    # Split D = D_smooth + D_fluct where D_smooth is the "trend"
    # within each denominator. If D_smooth ⊥ δ, only D_fluct matters.
    # ============================================================
    print()
    print("=" * 80)
    print("D_FLUCT DECOMPOSITION: Does D_smooth ⊥ δ?")
    print("=" * 80)

    for p in [53, 97, 199, 307, 499]:
        print(f"\n--- p = {p} ---")
        N = p - 1
        fracs = farey_sequence_sorted(N)
        n_total = len(fracs)

        sum_D_delta = Fraction(0)
        sum_Dsmooth_delta = Fraction(0)
        sum_Dfluct_delta = Fraction(0)
        sum_delta_sq = Fraction(0)
        sum_Dfluct_sq = Fraction(0)
        sum_D_sq = Fraction(0)

        by_denom = defaultdict(list)
        for j, (a, b) in enumerate(fracs):
            if (a == 0 and b == 1) or (a == 1 and b == 1):
                continue
            D = Fraction(j) - Fraction(n_total * a, b)
            pa_mod_b = (p * a) % b
            delta = Fraction(a - pa_mod_b, b)
            by_denom[b].append((a, D, delta))

        for b in sorted(by_denom.keys()):
            entries = by_denom[b]
            phi_b = len(entries)
            mean_D = sum(e[1] for e in entries) / phi_b

            for a, D, delta in entries:
                D_smooth = mean_D  # simplest: D_smooth = mean of D within denom class
                D_fluct = D - D_smooth

                sum_D_delta += D * delta
                sum_Dsmooth_delta += D_smooth * delta
                sum_Dfluct_delta += D_fluct * delta
                sum_delta_sq += delta * delta
                sum_Dfluct_sq += D_fluct * D_fluct
                sum_D_sq += D * D

        R_actual = float(2 * sum_D_delta / sum_delta_sq) if sum_delta_sq != 0 else 0
        R_fluct_only = float(2 * sum_Dfluct_delta / sum_delta_sq) if sum_delta_sq != 0 else 0
        R_smooth_only = float(2 * sum_Dsmooth_delta / sum_delta_sq) if sum_delta_sq != 0 else 0

        # CS bound using D_fluct only
        fluct_CS = float(2 * (sum_Dfluct_sq * sum_delta_sq).limit_denominator(10**30))
        fluct_CS_ratio = 2 * sqrt(float(sum_Dfluct_sq) / float(sum_delta_sq)) if sum_delta_sq > 0 else 0

        print(f"  R_actual          = {R_actual:+.6f}")
        print(f"  R_smooth_part     = {R_smooth_only:+.6f}")
        print(f"  R_fluct_part      = {R_fluct_only:+.6f}")
        print(f"  Σ D² / Σ δ²       = {float(sum_D_sq / sum_delta_sq):.4f}")
        print(f"  Σ D_fluct² / Σ δ² = {float(sum_Dfluct_sq / sum_delta_sq):.4f}")
        print(f"  Global CS bound (D_fluct): 2·sqrt(Σ D_fluct²/Σ δ²) = {fluct_CS_ratio:.4f}")
        print(f"  Does fluct-CS prove |R|<1? {'YES' if fluct_CS_ratio < 1.0 else 'NO'}")

    # ============================================================
    # APPROACH 3: Better decomposition - remove LINEAR trend in a/b
    # D_smooth(a/b) = α_b + β_b·(a/b) where α_b, β_b are chosen
    # to minimize Σ (D - D_smooth)² within each denom class.
    # ============================================================
    print()
    print("=" * 80)
    print("LINEAR TREND REMOVAL: D = (α + β·x) + D_fluct per denom")
    print("=" * 80)

    for p in [53, 97, 199, 307, 499]:
        print(f"\n--- p = {p} ---")
        N = p - 1
        fracs = farey_sequence_sorted(N)
        n_total = len(fracs)

        by_denom = defaultdict(list)
        for j, (a, b) in enumerate(fracs):
            if (a == 0 and b == 1) or (a == 1 and b == 1):
                continue
            D = Fraction(j) - Fraction(n_total * a, b)
            pa_mod_b = (p * a) % b
            delta = Fraction(a - pa_mod_b, b)
            by_denom[b].append((a, float(D), float(delta), float(Fraction(a, b))))

        sum_Dfluct_sq = 0.0
        sum_Dfluct_delta = 0.0
        sum_delta_sq = 0.0
        sum_D_sq = 0.0

        for b in sorted(by_denom.keys()):
            entries = by_denom[b]
            phi_b = len(entries)
            if phi_b < 2:
                # Can't fit linear trend with < 2 points, use mean only
                mean_D = sum(e[1] for e in entries) / phi_b
                for a, D, delta, x in entries:
                    D_fluct = D - mean_D
                    sum_Dfluct_sq += D_fluct**2
                    sum_Dfluct_delta += D_fluct * delta
                    sum_delta_sq += delta**2
                    sum_D_sq += D**2
                continue

            # Fit D = α + β·x by least squares within this denom class
            sx = sum(e[3] for e in entries)
            sy = sum(e[1] for e in entries)
            sxx = sum(e[3]**2 for e in entries)
            sxy = sum(e[3] * e[1] for e in entries)
            n = phi_b
            denom = n * sxx - sx * sx
            if abs(denom) < 1e-15:
                beta = 0.0
                alpha = sy / n
            else:
                beta = (n * sxy - sx * sy) / denom
                alpha = (sy - beta * sx) / n

            for a, D, delta, x in entries:
                D_smooth = alpha + beta * x
                D_fluct = D - D_smooth
                sum_Dfluct_sq += D_fluct**2
                sum_Dfluct_delta += D_fluct * delta
                sum_delta_sq += delta**2
                sum_D_sq += D**2

        R_fluct = 2 * sum_Dfluct_delta / sum_delta_sq if sum_delta_sq > 0 else 0
        fluct_CS = 2 * sqrt(sum_Dfluct_sq / sum_delta_sq) if sum_delta_sq > 0 else 0
        print(f"  Σ D² / Σ δ²             = {sum_D_sq / sum_delta_sq:.4f}")
        print(f"  Σ D_fluct² / Σ δ² (lin) = {sum_Dfluct_sq / sum_delta_sq:.4f}")
        print(f"  R via D_fluct only       = {R_fluct:+.6f}")
        print(f"  CS bound (lin detrend)    = {fluct_CS:.4f}")
        print(f"  Proves |R|<1? {'YES' if fluct_CS < 1.0 else 'NO'}")

    elapsed_total = time.time() - start_time
    print(f"\nTotal time: {elapsed_total:.1f}s")
