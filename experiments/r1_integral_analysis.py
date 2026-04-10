#!/usr/bin/env python3
"""
CORRECTED R_1 INTEGRAL ANALYSIS
================================

R_1 = Sum_{k=1}^{p-1} D_old(k/p)^2 / dilution_raw

KEY INSIGHT:
  D_old(k/p) for k/p in the interval (f_j, f_{j+1}) equals (j+1) - n*(k/p)
  (NOT D_vals[j] = j - n*f_j which is the value AT f_j, not in the interval)

This script:
1. Computes R_1 DIRECTLY (sum over k/p)
2. Also computes the CORRECT integral using (D_j+1) values
3. Verifies that R_1 ≈ n * correct_integral / (2 * old_D_sq)
4. Shows the floor-error structure

Key formula:
  Sum_{k in interval j} D_old(k/p)^2 = Sum_k [(j+1) - n*(k/p)]^2
  ≠ D_vals[j]^2 * floor(p * gap_j)   (this was the ERROR in bc_extended_verification.py)
"""

import time
from math import gcd, isqrt
import sys

start_time = time.time()


def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def compute_r1_and_integral(p, verbose=False):
    """
    Compute:
      - R_1 = Sum_{k=1}^{p-1} D_old(k/p)^2 / dilution_raw  (EXACT via Farey sweep)
      - integral_correct = integral_0^1 D_old^2 dx  (using correct post-jump values)
      - integral_wrong = Sum_j D(f_j)^2 * gap_j  (incorrect formula from previous script)

    D_old(x) = N_N(x) - n*x where N_N(x) = #{f in F_N: f <= x}.
    For x in (f_j, f_{j+1}): N_N(x) = j+1, so D_old(x) = (j+1) - n*x.
    AT f_j itself: D_old(f_j) = j+1 - n*f_j [inclusive rank convention]
    OR D_old(f_j) = j - n*f_j [exclusive rank convention]

    We use INCLUSIVE: D_old(f_j) = (j+1) - n*f_j = D_val_incl[j].
    """
    N = p - 1

    # Build F_N using mediant algorithm
    # Track: (a/b) fracs in order
    fracs = [(0, 1)]
    a, b = 0, 1
    c, d = 1, N
    fracs.append((1, N))
    while (c, d) != (1, 1):
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        fracs.append((c, d))

    n = len(fracs)
    n_prime = n + p - 1

    # Compute D values using INCLUSIVE convention: D(f_j) = (j+1) - n*f_j
    # [rank = #{f' <= f_j} = j+1 with 0-indexed j]
    # Wait: if fracs[0] = (0,1) = 0/1 and fracs[n-1] = (1,1) = 1, then
    # rank(fracs[0]) = 1 (fracs[0] itself is counted) if inclusive.
    # D_inclusive(fracs[j]) = (j+1) - n*(a_j/b_j).
    # But this means D(0/1) = 1 - 0 = 1, not 0.

    # STANDARD convention: D(f) = rank(f) - n*f where rank(f) = #{f' in F_N: f' < f}.
    # D_exclusive(fracs[j]) = j - n*(a_j/b_j).
    # D(0/1) = 0, D(1/N) = 1 - n/N, etc.

    # For x STRICTLY BETWEEN f_j and f_{j+1}:
    # #{f' < x} = j+1 (since f_0,...,f_j are all < x, f_{j+1} > x)
    # D_old(x) = (j+1) - n*x [same for both conventions since k/p is not a Farey frac]

    # old_D_sq = Sum D(f)^2 using EXCLUSIVE convention (rank = strict)
    old_D_sq = 0.0
    for j, (a_j, b_j) in enumerate(fracs):
        x = a_j / b_j
        D_excl = j - n * x  # exclusive rank = j
        old_D_sq += D_excl * D_excl

    dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2

    # -------------------------------------------------------
    # DIRECT COMPUTATION of Sum_{k=1}^{p-1} D_old(k/p)^2
    # For each k/p, find which Farey interval it's in,
    # then use D_old(k/p) = (j+1) - n*(k/p)
    # -------------------------------------------------------
    # Use binary search: for each k, find j such that fracs[j] <= k/p < fracs[j+1]
    # since fracs are sorted, we can use bisect.

    # Precompute float values of Farey fractions for binary search
    frac_vals = [a / b for (a, b) in fracs]

    # Find interval index for k/p using linear scan (for small p only)
    # For large p, we need binary search
    from bisect import bisect_right

    riemann_sum = 0.0
    for k in range(1, p):
        x = k / p
        # j = largest index with frac_vals[j] <= x
        # bisect_right returns insertion point for x in frac_vals
        j = bisect_right(frac_vals, x) - 1
        # j is in [0, n-1], with frac_vals[j] <= x < frac_vals[j+1]
        D_old_kp = (j + 1) - n * x  # using D_old(x) = (j+1) - n*x for x in (f_j, f_{j+1})
        riemann_sum += D_old_kp * D_old_kp

    R_1_direct = riemann_sum / dilution_raw if dilution_raw > 0 else 0.0

    # -------------------------------------------------------
    # CORRECT INTEGRAL: integral_0^1 D_old^2 dx
    # = Sum_j integral_{f_j}^{f_{j+1}} [(j+1) - n*x]^2 dx
    # = Sum_j [v_j^2 * g_j - v_j * n * g_j^2 + n^2 * g_j^3 / 3]
    # where v_j = (j+1) - n*f_j [= D_exclusive(f_j) + 1]
    # -------------------------------------------------------
    integral_correct = 0.0
    integral_wrong = 0.0   # Sum_j D_excl(f_j)^2 * g_j (previous incorrect formula)
    integral_post_jump = 0.0  # Sum_j (D_excl(f_j)+1)^2 * g_j (dominant term)
    active_error = 0.0

    for j in range(n - 1):
        a_j, b_j = fracs[j]
        a_j1, b_j1 = fracs[j+1]
        bp = b_j * b_j1  # denominator product
        g = 1.0 / bp      # gap

        f_j = a_j / b_j
        D_excl_j = j - n * f_j  # exclusive value at f_j
        v_j = D_excl_j + 1       # value just after the jump at f_j (for x in (f_j, f_{j+1}))

        # Correct integral in this interval
        integral_correct += v_j * v_j * g - v_j * n * g * g + n * n * g * g * g / 3

        # Wrong formula from previous script (uses D_excl^2, not v_j^2)
        integral_wrong += D_excl_j * D_excl_j * g

        # Post-jump dominant term
        integral_post_jump += v_j * v_j * g

        # Active gap (floor(p/(b*b')) >= 1)
        if bp <= p:
            active_error += D_excl_j * D_excl_j

    # integral ratios
    if old_D_sq > 0:
        int_ratio_correct = n * integral_correct / (2 * old_D_sq)
        int_ratio_wrong = n * integral_wrong / (2 * old_D_sq)
        int_ratio_postjump = n * integral_post_jump / (2 * old_D_sq)
    else:
        int_ratio_correct = int_ratio_wrong = int_ratio_postjump = 0.0

    if dilution_raw > 0:
        active_ratio = active_error / dilution_raw
    else:
        active_ratio = 0.0

    return {
        'p': p, 'n': n,
        'old_D_sq': old_D_sq,
        'dilution_raw': dilution_raw,
        'riemann_sum': riemann_sum,
        'R_1_direct': R_1_direct,
        'integral_correct': integral_correct,
        'integral_wrong': integral_wrong,
        'integral_post_jump': integral_post_jump,
        'int_ratio_correct': int_ratio_correct,
        'int_ratio_wrong': int_ratio_wrong,
        'int_ratio_postjump': int_ratio_postjump,
        'active_ratio': active_ratio,
    }


if __name__ == '__main__':
    max_p = int(sys.argv[1]) if len(sys.argv) > 1 else 100

    primes = sieve_primes(max_p)
    test_primes = [p for p in primes if p >= 11]

    print("=" * 100)
    print("CORRECTED R_1 INTEGRAL ANALYSIS")
    print("=" * 100)
    print()
    print(f"{'p':>6} {'R_1_direct':>12} {'int_ratio_corr':>14} {'int_ratio_wrong':>15} "
          f"{'int_ratio_pj':>12} {'active_ratio':>12}")
    print("-" * 100)

    results = []
    for p in test_primes:
        t0 = time.time()
        res = compute_r1_and_integral(p)
        dt = time.time() - t0
        results.append(res)

        print(f"{p:6d} {res['R_1_direct']:12.4f} {res['int_ratio_correct']:14.4f} "
              f"{res['int_ratio_wrong']:15.4f} {res['int_ratio_postjump']:12.4f} "
              f"{res['active_ratio']:12.4f}")

    print()
    print("=" * 100)
    print("ANALYSIS")
    print("=" * 100)
    print()
    print("KEY QUESTION: Does int_ratio_correct ≈ R_1_direct?")
    print("If YES: R_1 = n * integral_0^1 D_old^2 / (2 * old_D_sq) [non-circular!]")
    print()

    for res in results:
        p = res['p']
        disc = abs(res['R_1_direct'] - res['int_ratio_correct'])
        print(f"  p={p:4d}: R_1={res['R_1_direct']:.4f}  int_ratio_corr={res['int_ratio_correct']:.4f}  "
              f"diff={disc:.4f}  (diff/R_1={disc/max(res['R_1_direct'],1e-10):.3f})")

    print()
    print("CONCLUSION: int_ratio_correct vs R_1_direct comparison:")
    max_diff = max(abs(r['R_1_direct'] - r['int_ratio_correct']) for r in results)
    print(f"  Maximum |R_1 - int_ratio_correct|: {max_diff:.4f}")
    print(f"  This represents the 'floor-error' contribution.")
    print()

    print(f"Total time: {time.time() - start_time:.1f}s")
