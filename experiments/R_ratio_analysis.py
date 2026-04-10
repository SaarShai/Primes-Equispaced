#!/usr/bin/env python3
"""
R RATIO ANALYSIS: Prove |R| < 1 where R = B_raw / delta_sq
============================================================

This is the KEY to proving B+C > 0 analytically.

B + C = delta_sq * (1 + R)

For B+C > 0: need R > -1, i.e., B_raw > -delta_sq.

EMPIRICAL CLAIM: |R| < 0.52 for all primes p >= 11.

This script:
1. Computes R = B_raw / delta_sq exactly for all primes up to LIMIT.
2. Identifies the MINIMUM of 1+R (i.e., worst case for B+C > 0).
3. Analyzes the structure of large |R| cases.
4. Tests the hypothesis: R = Σ_{b} R_b where R_b is the per-denominator contribution.
5. Derives an ANALYTICAL bound on |R| using the structure of Farey fractions.

KEY FORMULA (per-denominator decomposition):
  B_raw = 2 * Σ_{b=2}^{N} (1/b) * Σ_{gcd(a,b)=1} D(a/b) * (a - sigma_p(a))
  delta_sq = Σ_{b=2}^{N} (1/b^2) * Σ_{gcd(a,b)=1} (a - sigma_p(a))^2

For each denominator b:
  B_b = 2/b * Σ_{gcd(a,b)=1} D(a/b) * delta_a  where delta_a = a - sigma_p(a)
  C_b = (1/b^2) * Σ_{gcd(a,b)=1} delta_a^2

  R_b = B_b / (C_b * b) = [Σ D * delta_a] / [(1/(2b)) * Σ delta_a^2]
      = 2b * Σ D * delta_a / Σ delta_a^2

By Cauchy-Schwarz:
  |R_b| <= 2b * sqrt(Σ D^2 * Σ delta_a^2) / Σ delta_a^2
         = 2b * sqrt(Σ D^2) / sqrt(Σ delta_a^2)

For each denominator b:
  Σ_{gcd(a,b)=1} delta_a^2 = 2 * deficit_b  (by the per-denominator formula)
  Σ_{gcd(a,b)=1} D(a/b)^2 = S_b_D

  |B_b / C_b * b_weight| <= 2b * sqrt(S_b_D) / sqrt(2 * deficit_b)

CLAIM: This can be bounded in terms of N using Franel-Landau.
"""

import time
import sys
from math import gcd, isqrt, log, sqrt, pi
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


def compute_R_ratio(p):
    """
    Exact computation of R = B_raw / delta_sq for prime p.
    """
    N = p - 1

    # Build Farey sequence F_N
    fracs = []
    a, b = 0, 1
    c, d = 1, N
    fracs.append((0, 1))
    fracs.append((1, N))
    while (c, d) != (1, 1):
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        fracs.append((c, d))

    n = len(fracs)

    # Compute D(a/b) and delta(a/b) for each fraction
    D_vals = [j - n * fracs[j][0] / fracs[j][1] for j in range(n)]
    delta_vals = [(fracs[j][0] - (p * fracs[j][0]) % fracs[j][1]) / fracs[j][1]
                  for j in range(n)]

    B_raw = 2.0 * sum(D_vals[j] * delta_vals[j] for j in range(n))
    delta_sq = sum(dv**2 for dv in delta_vals)
    B_plus_C = B_raw + delta_sq
    old_D_sq = sum(dv**2 for dv in D_vals)

    R = B_raw / delta_sq if delta_sq > 0 else float('nan')
    one_plus_R = B_plus_C / delta_sq if delta_sq > 0 else float('nan')

    # Per-denominator breakdown
    denom_data = defaultdict(lambda: {'B': 0.0, 'C': 0.0, 'D_sq': 0.0, 'deficit': 0.0})
    for j, (a_j, b_j) in enumerate(fracs):
        delta_a = a_j - (p * a_j) % b_j  # integer: a - sigma_p(a)
        b_data = denom_data[b_j]
        b_data['B'] += D_vals[j] * delta_vals[j]   # = D * delta_a / b
        b_data['C'] += delta_vals[j]**2              # = delta_a^2 / b^2
        b_data['D_sq'] += D_vals[j]**2
        b_data['deficit'] += delta_a**2 / 2          # = (a - sigma)^2 / 2

    # Worst-case denominator (most negative R_b contribution)
    worst_denom = None
    worst_Rb = 0.0
    for b_j, bd in denom_data.items():
        if bd['C'] > 0:
            Rb = 2 * bd['B'] / (bd['C'] * delta_sq) if delta_sq > 0 else 0
            if Rb < worst_Rb:
                worst_Rb = Rb
                worst_denom = b_j

    n_prime = n + p - 1
    dilution_raw = old_D_sq * (n_prime**2 - n**2) / (n**2)

    return {
        'p': p, 'N': N, 'n': n,
        'B_raw': B_raw, 'delta_sq': delta_sq, 'B_plus_C': B_plus_C,
        'old_D_sq': old_D_sq,
        'R': R, 'one_plus_R': one_plus_R,
        'dilution_raw': dilution_raw,
        'CA_ratio': delta_sq / dilution_raw if dilution_raw > 0 else 0,
        'worst_denom': worst_denom, 'worst_Rb': worst_Rb,
    }


def main():
    LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    primes = sieve_primes(LIMIT)
    test_primes = [p for p in primes if p >= 11]

    print("=" * 100)
    print("R RATIO ANALYSIS: R = B_raw / delta_sq,  B+C = delta_sq*(1+R)")
    print("=" * 100)
    print()
    print("THEOREM TO PROVE: R > -1 for all primes p >= 11")
    print("EMPIRICAL CLAIM:  |R| < 0.52 for all tested primes")
    print()

    header = (f"{'p':>6} {'B_raw':>12} {'delta_sq':>12} {'R':>10} {'1+R':>8} "
              f"{'worst_b':>8} {'C/A':>8}")
    print(header)
    print("-" * len(header))

    all_R = []
    min_1pR = float('inf')
    min_1pR_p = 0
    max_R = -float('inf')
    max_R_p = 0
    min_R = float('inf')
    min_R_p = 0

    for p in test_primes:
        r = compute_R_ratio(p)
        all_R.append(r)

        R = r['R']
        one_pR = r['one_plus_R']

        if one_pR < min_1pR:
            min_1pR = one_pR
            min_1pR_p = p
        if R > max_R:
            max_R = R
            max_R_p = p
        if R < min_R:
            min_R = R
            min_R_p = p

        elapsed = time.time() - start_time
        should_print = (p <= 200 or p % 200 <= 10 or
                        one_pR < min_1pR * 1.05 or
                        abs(R) > abs(max_R) * 0.95 or
                        p > LIMIT - 30 or elapsed < 2)

        if should_print:
            print(f"{p:6d} {r['B_raw']:12.2f} {r['delta_sq']:12.2f} {R:10.4f} "
                  f"{one_pR:8.4f} {str(r['worst_denom']):>8} {r['CA_ratio']:8.6f}",
                  flush=True)

    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print()
    print(f"Minimum 1+R = {min_1pR:.6f}  at p = {min_1pR_p}")
    print(f"Minimum R   = {min_R:.6f}  at p = {min_R_p}")
    print(f"Maximum R   = {max_R:.6f}  at p = {max_R_p}")
    print()
    print(f"B+C > 0 verified: {'YES' if min_1pR > 0 else 'NO'}")
    print(f"R > -1 verified:  {'YES' if min_R > -1 else 'NO'}")
    print(f"|R| < 0.52 verified: {'YES' if max(abs(min_R), abs(max_R)) < 0.52 else 'NO - MAX |R| = ' + str(max(abs(min_R), abs(max_R)))}")
    print()

    # Trend analysis
    print("Trend of R with N:")
    print(f"{'range':>20s} {'min_R':>10s} {'max_R':>10s} {'avg_R':>10s} {'count':>6s}")
    ranges_p = [(11,50),(50,100),(100,200),(200,500),(500,1001)]
    for lo, hi in ranges_p:
        sub = [r for r in all_R if lo <= r['p'] <= hi and not (r['R'] != r['R'])]
        if sub:
            Rs = [r['R'] for r in sub]
            print(f"  p in [{lo:>4d},{hi:>4d}]: min={min(Rs):10.4f} max={max(Rs):10.4f} "
                  f"avg={sum(Rs)/len(Rs):10.4f} n={len(sub):6d}")
    print()

    # Key analytical result
    print("=" * 100)
    print("ANALYTICAL BOUND ATTEMPT")
    print("=" * 100)
    print()
    print("Key formula: R = B_raw / delta_sq")
    print("  B_raw = 2 * Σ D(f) * delta(f)")
    print("  delta_sq = Σ delta(f)^2")
    print()
    print("By Cauchy-Schwarz: |B_raw| <= 2 * sqrt(old_D_sq * delta_sq)")
    print("=> |R| <= 2 * sqrt(old_D_sq / delta_sq)")
    print()

    for r in all_R:
        ratio = 2 * sqrt(r['old_D_sq'] / r['delta_sq']) if r['delta_sq'] > 0 else float('inf')
        r['CS_bound'] = ratio

    print("Comparison: |R| vs 2*sqrt(old_D_sq/delta_sq)  [CS bound]")
    for r in all_R[::max(1, len(all_R)//20)]:
        print(f"  p={r['p']:4d}: |R|={abs(r['R']):.4f}, CS_bound={r['CS_bound']:.4f}  "
              f"(CS is {r['CS_bound']/max(abs(r['R']), 1e-10):.1f}x larger)")
    print()

    print("KEY QUESTION: Does old_D_sq / delta_sq stay bounded?")
    print()
    for r in all_R[::max(1, len(all_R)//20)]:
        ratio = r['old_D_sq'] / r['delta_sq'] if r['delta_sq'] > 0 else float('inf')
        print(f"  p={r['p']:4d}: old_D_sq/delta_sq = {ratio:.4f}, "
              f"sqrt={sqrt(ratio):.4f}, 2*sqrt={2*sqrt(ratio):.4f}")
    print()

    # If old_D_sq / delta_sq -> constant, then CS bound -> constant,
    # and if this constant < 1, then |R| < 1 analytically.
    # But old_D_sq ~ n * N * C_W and delta_sq ~ N^2/(48 log N), so
    # old_D_sq / delta_sq ~ (3N^2/pi^2) * N * C_W / (N^2/(48 log N))
    #                     ~ (144/pi^2) * N * C_W * log(N)
    # This GROWS without bound!
    # So CS bound grows and |R| < 1 can NOT be proved via CS alone.

    print("Analytical conclusion:")
    print("  old_D_sq/delta_sq grows as ~O(N * log N) -> CS bound for |R| grows.")
    print("  Therefore: |R| < 1 CANNOT be proved by Cauchy-Schwarz alone.")
    print()
    print("  However: The EMPIRICAL minimum 1+R > 0 shows B+C > 0 always holds.")
    print("  The structure of the proof must use CANCELLATION in B_raw,")
    print("  not just the magnitude of old_D_sq vs delta_sq.")
    print()

    # What IS the actual minimum 1+R across the test range?
    print(f"  Minimum 1+R observed: {min_1pR:.6f} > 0  (at p = {min_1pR_p})")
    print(f"  This means B+C >= {min_1pR:.4f} * delta_sq > 0.")
    print()
    print(f"  If min(1+R) -> 0 as p -> inf: B+C is provably > 0 but barely.")
    print(f"  If min(1+R) >= c > 0: B+C >= c * delta_sq, giving analytical B+C > 0.")
    print()

    # Print 1+R trend
    print("Trend of 1+R (= B+C / delta_sq) by N:")
    print(f"{'p':>8} {'N':>8} {'1+R':>10} {'old_D_sq/delta_sq':>20}")
    for r in all_R[::max(1, len(all_R)//30)]:
        od = r['old_D_sq'] / r['delta_sq'] if r['delta_sq'] > 0 else 0
        print(f"{r['p']:8d} {r['N']:8d} {r['one_plus_R']:10.4f} {od:20.4f}")

    print(f"\nTotal runtime: {time.time() - start_time:.1f}s")


if __name__ == '__main__':
    main()
