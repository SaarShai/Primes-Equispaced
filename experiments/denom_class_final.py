#!/usr/bin/env python3
"""
Final focused analysis:
1. The per-denominator approach FAILS (ratio >> 1/2 for large b).
2. The global approach works: cross/delta^2 stays > -1/2.
3. KEY: |cross|/sqrt(D_osc_sq * delta_sq) ~ 0.01-0.18 (tiny correlation).
4. The linear part of cross is POSITIVE, the residual is NEGATIVE.
5. They nearly cancel, leaving a small net.

PROOF STRATEGY:
B+C = ||delta||^2 + 2*<D^osc, delta>

We need: <D^osc, delta> > -||delta||^2/2

By Cauchy-Schwarz: |<D^osc, delta>| ≤ ||D^osc|| * ||delta||

So B+C ≥ ||delta||^2 - 2*||D^osc||*||delta|| = ||delta||(||delta|| - 2*||D^osc||)

This is positive iff ||D^osc|| < ||delta||/2, which FAILS because ||D^osc|| >> ||delta||.

So Cauchy-Schwarz alone is NOT enough. We need to use structural cancellation.

KEY OBSERVATION: D^osc grows like N*sqrt(log N) while delta grows like N.
Wait -- let me check the actual scaling more carefully.
"""

from fractions import Fraction
from math import gcd, sqrt, log
from collections import defaultdict

def farey_sequence(N):
    fracs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.append(Fraction(a, b))
    fracs.sort()
    return fracs

def compute_norms(p):
    N = p - 1
    F = farey_sequence(N)
    size_F = len(F)
    rank_map = {f: i for i, f in enumerate(F)}

    D_map = {f: Fraction(rank_map[f]) - Fraction(size_F) * f for f in F}
    delta_map = {}
    for f in F:
        a, b = f.numerator, f.denominator
        delta_map[f] = Fraction(a - (p * a) % b, b)

    denom_groups = defaultdict(list)
    for f in F:
        denom_groups[f.denominator].append(f)

    D_osc_map = {}
    for b, fracs_b in denom_groups.items():
        D_mean = sum(D_map[f] for f in fracs_b) / len(fracs_b)
        for f in fracs_b:
            D_osc_map[f] = D_map[f] - D_mean

    D_osc_sq = sum(v*v for v in D_osc_map.values())
    delta_sq = sum(v*v for v in delta_map.values())
    cross = sum(D_osc_map[f] * delta_map[f] for f in F)
    BC = 2 * cross + delta_sq

    # Also compute ||D||^2 (full, not oscillatory)
    D_sq = sum(v*v for v in D_map.values())

    # ||D_mean||^2 (the smooth/mean part)
    D_mean_sq = D_sq - D_osc_sq  # since D = D_mean + D_osc and they're orthogonal within each denom

    # Actually D_mean_sq = Σ_b phi_b * (D_mean_b)^2
    D_mean_sq_check = Fraction(0)
    for b, fracs_b in denom_groups.items():
        D_mean = sum(D_map[f] for f in fracs_b) / len(fracs_b)
        D_mean_sq_check += len(fracs_b) * D_mean * D_mean

    return {
        'p': p, 'N': N, 'size_F': size_F,
        'D_sq': D_sq,
        'D_osc_sq': D_osc_sq,
        'D_mean_sq': D_mean_sq_check,
        'delta_sq': delta_sq,
        'cross': cross,
        'BC': BC,
    }

def main():
    print("SCALING ANALYSIS (exact arithmetic)")
    print("=" * 120)
    print(f"{'p':>5} {'N':>4} {'||D||^2/N^2':>12} {'||D_osc||^2/N^2':>16} {'||D_mean||^2/N^2':>17} "
          f"{'||delta||^2/N':>14} {'cross/N':>12} {'BC/N':>10} {'corr':>10}")

    for p in [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,
              101,103,107,109,113,127,131]:
        r = compute_norms(p)
        N = r['N']
        N2 = N * N

        D_sq_scaled = float(r['D_sq']) / N2
        D_osc_scaled = float(r['D_osc_sq']) / N2
        D_mean_scaled = float(r['D_mean_sq']) / N2
        delta_scaled = float(r['delta_sq']) / N
        cross_scaled = float(r['cross']) / N
        BC_scaled = float(r['BC']) / N

        # Correlation
        if r['D_osc_sq'] > 0 and r['delta_sq'] > 0:
            corr = float(r['cross']) / sqrt(float(r['D_osc_sq']) * float(r['delta_sq']))
        else:
            corr = 0

        print(f"{p:>5} {N:>4} {D_sq_scaled:>12.4f} {D_osc_scaled:>16.4f} {D_mean_scaled:>17.4f} "
              f"{delta_scaled:>14.4f} {cross_scaled:>12.4f} {BC_scaled:>10.4f} {corr:>10.4f}")

    # Detailed analysis: ||D_osc||^2 / N^2 should grow like log(N)/pi^2
    # ||delta||^2 / N should be roughly constant
    print("\n\nSCALING FIT:")
    print("=" * 80)
    print(f"{'p':>5} {'||D_osc||^2/(N^2 logN)':>24} {'||delta||^2/N':>14} {'BC/N':>10}")

    for p in [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,
              101,103,107,109,113,127,131]:
        r = compute_norms(p)
        N = r['N']
        logN = log(N)

        D_osc_fit = float(r['D_osc_sq']) / (N * N * logN)
        delta_fit = float(r['delta_sq']) / N
        BC_fit = float(r['BC']) / N

        print(f"{p:>5} {D_osc_fit:>24.6f} {delta_fit:>14.4f} {BC_fit:>10.4f}")

    # KEY: Is B+C/N bounded below?
    print("\n\nB+C/N LOWER BOUND CHECK:")
    print("=" * 80)
    min_bc_n = 999
    min_p = 0
    for p in [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,
              101,103,107,109,113,127,131]:
        r = compute_norms(p)
        bc_n = float(r['BC']) / r['N']
        if bc_n < min_bc_n:
            min_bc_n = bc_n
            min_p = p
        print(f"  p={p:>5}: B+C/N = {bc_n:.6f}")

    print(f"\n  Minimum B+C/N = {min_bc_n:.6f} at p={min_p}")

    # Check: does B+C grow like N or faster?
    print("\n\nGROWTH RATE OF B+C:")
    print("=" * 80)
    prev_bc = None
    prev_n = None
    for p in [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,
              101,103,107,109,113,127,131]:
        r = compute_norms(p)
        bc = float(r['BC'])
        n = r['N']
        if prev_bc is not None and prev_n is not None:
            # log(BC)/log(N) ratio
            if bc > 0 and prev_bc > 0:
                growth = log(bc / prev_bc) / log(n / prev_n) if n != prev_n else 0
            else:
                growth = 0
        else:
            growth = 0
        print(f"  p={p:>5}: B+C = {bc:>12.4f}, N = {n:>4}, B+C/N = {bc/n:>8.4f}, local growth exponent: {growth:.2f}")
        prev_bc = bc
        prev_n = n

if __name__ == '__main__':
    main()
