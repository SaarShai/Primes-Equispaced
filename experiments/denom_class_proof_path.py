#!/usr/bin/env python3
"""
Focused analysis for the proof path.

KEY FINDINGS so far:
1. The ratio ||D_b^osc||/||delta_b|| is NOT < 1/2 -- it's often >> 1.
   So the per-denominator Cauchy-Schwarz approach FAILS.
2. But the TOTAL cross term is much smaller than Cauchy-Schwarz allows.
3. Negative denominators exist but |neg|/pos ratio stays bounded (~0.29 max).
4. delta=0 when b | (p-1), contributing nothing.

NEW PROOF STRATEGY: Don't try to bound per denominator.
Instead, use the GLOBAL structure:

B+C = ||delta||^2_total + 2 * <D^osc_total, delta_total>

where D^osc_total(f) = D(f) - D_mean_b(f) for f with denominator b.

Key: D^osc is "orthogonal to constants within each denominator class".
delta is determined by the multiplication-by-p map.

Can we show |<D^osc, delta>| ≤ (1-epsilon) * ||delta||^2/2 for some epsilon > 0?

This requires understanding the correlation between Farey discrepancy oscillations
and the arithmetic permutation delta.
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

def euler_phi(n):
    result = n
    temp = n
    pp = 2
    while pp * pp <= temp:
        if temp % pp == 0:
            while temp % pp == 0:
                temp //= pp
            result -= result // pp
        pp += 1
    if temp > 1:
        result -= result // temp
    return result

def compute_global(p):
    """Compute global quantities for the proof."""
    N = p - 1
    F = farey_sequence(N)
    size_F = len(F)
    rank_map = {f: i for i, f in enumerate(F)}

    D_map = {f: Fraction(rank_map[f]) - Fraction(size_F) * f for f in F}
    delta_map = {}
    for f in F:
        a, b = f.numerator, f.denominator
        pa_mod_b = (p * a) % b
        delta_map[f] = Fraction(a - pa_mod_b, b)

    # Compute D^osc per denominator
    denom_groups = defaultdict(list)
    for f in F:
        denom_groups[f.denominator].append(f)

    D_osc_map = {}
    for b, fracs_b in denom_groups.items():
        D_mean = sum(D_map[f] for f in fracs_b) / len(fracs_b)
        for f in fracs_b:
            D_osc_map[f] = D_map[f] - D_mean

    # Global norms
    total_D_osc_sq = sum(v*v for v in D_osc_map.values())
    total_delta_sq = sum(v*v for v in delta_map.values())
    total_cross = sum(D_osc_map[f] * delta_map[f] for f in F)
    BC = 2 * total_cross + total_delta_sq

    # Correlation coefficient
    if total_D_osc_sq > 0 and total_delta_sq > 0:
        corr = float(total_cross) / sqrt(float(total_D_osc_sq) * float(total_delta_sq))
    else:
        corr = 0

    return {
        'p': p,
        'N': N,
        'size_F': size_F,
        'D_osc_sq': total_D_osc_sq,
        'delta_sq': total_delta_sq,
        'cross': total_cross,
        'BC': BC,
        'corr': corr,
    }

def analyze_proof_ingredients(p):
    """
    Compute the key quantities for a potential proof:

    1. ||delta||^2 ~ what? As p -> infty, how does it scale?
    2. |<D^osc, delta>| ~ what?
    3. ||D^osc||^2 ~ what?

    Standard results:
    - |F_N| ~ 3N^2/pi^2
    - ||D||^2 (full discrepancy) ~ N^2 * log(N) / pi^2 (Franel-Landau type)
    - ||D^osc||^2 should be similar since the mean part is smooth

    For delta: ||delta||^2 = Σ_b Σ_{a coprime b} (a - pa mod b)^2 / b^2
    This is a sum over all Farey fractions of a quantity involving multiplication by p.
    """
    N = p - 1
    F = farey_sequence(N)
    size_F = len(F)
    rank_map = {f: i for i, f in enumerate(F)}

    D_map = {f: Fraction(rank_map[f]) - Fraction(size_F) * f for f in F}
    delta_map = {}
    for f in F:
        a, b = f.numerator, f.denominator
        delta_map[f] = Fraction(a - (p * a) % f.denominator, f.denominator)

    # ||D||^2 total
    D_sq = sum(v*v for v in D_map.values())

    # ||delta||^2 total
    delta_sq = sum(v*v for v in delta_map.values())

    # delta restricted to b not dividing p-1
    delta_sq_nondiv = Fraction(0)
    delta_sq_div = Fraction(0)
    for f in F:
        b = f.denominator
        if N % b == 0:  # b | (p-1), so delta = 0
            delta_sq_div += delta_map[f]**2
        else:
            delta_sq_nondiv += delta_map[f]**2

    return {
        'p': p,
        'N': N,
        'size_F': size_F,
        'D_sq': D_sq,
        'delta_sq': delta_sq,
        'delta_sq_nondiv': delta_sq_nondiv,
        'delta_sq_div': delta_sq_div,
    }

def main():
    print("=" * 80)
    print("GLOBAL CORRELATION ANALYSIS")
    print("=" * 80)
    print(f"{'p':>5} {'|F|':>6} {'||D_osc||^2':>14} {'||delta||^2':>14} {'cross':>14} {'B+C':>14} {'corr':>10} {'BC/delta^2':>11}")

    for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        g = compute_global(p)
        bc_over_d = float(g['BC'] / g['delta_sq']) if g['delta_sq'] > 0 else 0
        print(f"{g['p']:>5} {g['size_F']:>6} {float(g['D_osc_sq']):>14.2f} {float(g['delta_sq']):>14.4f} {float(g['cross']):>14.4f} {float(g['BC']):>14.4f} {g['corr']:>10.6f} {bc_over_d:>11.4f}")

    print("\n" + "=" * 80)
    print("SCALING ANALYSIS: how do quantities grow with p?")
    print("=" * 80)
    print(f"{'p':>5} {'||D||^2':>14} {'||delta||^2':>14} {'D^2/N^2logN':>14} {'delta^2/N^2':>14} {'delta^2/N':>14}")

    for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        ing = analyze_proof_ingredients(p)
        N = ing['N']
        logN = log(N) if N > 1 else 1
        print(f"{p:>5} {float(ing['D_sq']):>14.2f} {float(ing['delta_sq']):>14.4f} "
              f"{float(ing['D_sq'])/(N*N*logN):>14.6f} {float(ing['delta_sq'])/(N*N):>14.6f} "
              f"{float(ing['delta_sq'])/N:>14.6f}")

    print("\n" + "=" * 80)
    print("KEY RATIO: B+C / ||delta||^2 = 1 + 2*cross/delta^2")
    print("For B+C > 0, need this ratio > 0, i.e., cross/delta^2 > -1/2")
    print("=" * 80)
    print(f"{'p':>5} {'cross/delta^2':>14} {'margin to -1/2':>16} {'B+C/N':>10}")

    for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        g = compute_global(p)
        if g['delta_sq'] > 0:
            ratio = float(g['cross'] / g['delta_sq'])
            margin = ratio + 0.5
            bc_over_N = float(g['BC']) / (p-1)
            print(f"{p:>5} {ratio:>14.6f} {margin:>16.6f} {bc_over_N:>10.4f}")

    # CRITICAL: What's the minimum of cross/delta^2 over all primes?
    print("\n" + "=" * 80)
    print("MINIMUM cross/delta^2 (must stay > -1/2 for B+C > 0)")
    print("=" * 80)
    min_ratio = 999
    min_p = 0
    for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
              101, 103, 107, 109, 113]:
        g = compute_global(p)
        if g['delta_sq'] > 0:
            ratio = float(g['cross'] / g['delta_sq'])
            if ratio < min_ratio:
                min_ratio = ratio
                min_p = p

    print(f"  Minimum cross/delta^2 = {min_ratio:.6f} at p={min_p}")
    print(f"  Margin to -1/2: {min_ratio + 0.5:.6f}")

    # Global Cauchy-Schwarz bound
    print("\n" + "=" * 80)
    print("CAUCHY-SCHWARZ vs ACTUAL cross")
    print("=" * 80)
    print(f"{'p':>5} {'|cross|':>14} {'CS bound':>14} {'|cross|/CS':>14} {'||D_osc||/||delta||':>20}")

    for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        g = compute_global(p)
        cs = sqrt(float(g['D_osc_sq']) * float(g['delta_sq']))
        actual = abs(float(g['cross']))
        ratio = actual / cs if cs > 0 else 0
        norm_ratio = sqrt(float(g['D_osc_sq'])) / sqrt(float(g['delta_sq'])) if g['delta_sq'] > 0 else 0
        print(f"{p:>5} {actual:>14.4f} {cs:>14.4f} {ratio:>14.6f} {norm_ratio:>20.4f}")

if __name__ == '__main__':
    main()
