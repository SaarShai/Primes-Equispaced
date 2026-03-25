#!/usr/bin/env python3
"""
B+C Extended Verification: All primes p in [11, 2000]
=======================================================

This script extends the verification of B+C > 0 from p <= 500 to p <= 2000.
It also computes the "integral ratio" integral_0^1 D_old^2 dx / (old_D_sq/n),
which is the KEY QUANTITY for the non-circular proof of R_1 ~ 1.

KEY FORMULA (non-circular):
  R_1 = Sum_k D_old(k/p)^2 / dilution_raw
      = n * integral / (2 * old_D_sq) + O(active_error / dilution_raw)

where integral = Sum_j D_old(f_j)^2 * gap_j (exact, uses Farey structure)
and active_error = Sum_{j: b_j*b_{j+1} <= p} D_j^2 (floor-rounding error).

CLAIM: active_error / dilution_raw = O(log^2(N)/N) -> 0 for small-b fractions.

This would give R_1 >= n * integral / (2 * old_D_sq) - O(log^2 N / N)
and if integral >= 2 * old_D_sq / n, then R_1 >= 1 - O(log^2 N / N).

COMPUTATIONAL GOAL:
  1. Verify B+C > 0 for all primes p in [11, 2000].
  2. Compute and tabulate the integral ratio.
  3. Compute active_error / dilution_raw for several primes.
  4. Show that the floor-error approach is asymptotically valid.
"""

import time
import sys
from math import gcd, isqrt, log, pi
from collections import defaultdict

start_time = time.time()

# ============================================================
# UTILITIES
# ============================================================

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def farey_next(a, b, c, d, N):
    """Return the fraction after a/b in F_N using the mediant algorithm."""
    k = (N + b) // d
    return k*c - a, k*d - b

def build_farey_with_data(N, p):
    """
    Build F_N incrementally and compute:
      - D(a/b) = rank - n*(a/b)  for each interior fraction
      - delta(a/b) = (a - (p*a mod b))/b
      - gap_j = b_j * b_{j+1} (denominator product = 1/gap)
      - b_left, b_right (neighboring denominators)

    Returns (fracs, D_vals, delta_vals, denom_prods) as lists.
    fracs: (a, b) tuples in order
    D_vals[j]: D(a_j/b_j) as float
    delta_vals[j]: delta(a_j/b_j) as float
    denom_prods[j]: b_j * b_{j+1} (for gap j = between fracs[j] and fracs[j+1])
    """
    # Use the O(n) Farey generation algorithm
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
    # rank[j] = j (0-indexed)
    # D[j] = j - n * (a_j/b_j)

    D_vals = []
    delta_vals = []
    denom_prods = []

    for j, (a_j, b_j) in enumerate(fracs):
        x = a_j / b_j
        D_j = j - n * x
        D_vals.append(D_j)

        if b_j >= 2 and a_j > 0:  # interior, non-endpoint fractions
            sigma = (p * a_j) % b_j
            delta_j = (a_j - sigma) / b_j
        else:
            delta_j = 0.0
        delta_vals.append(delta_j)

    # Denominator products (gap denominators)
    for j in range(len(fracs) - 1):
        denom_prods.append(fracs[j][1] * fracs[j+1][1])

    return fracs, n, D_vals, delta_vals, denom_prods


def compute_bc(p, verbose=False):
    """
    Compute B+C, R, delta_sq, B_raw for prime p.

    Also computes:
    - integral = Sum_j D_j^2 * gap_j = Sum_j D_j^2 / (b_j * b_{j+1})
    - integral_ratio = n * integral / (2 * old_D_sq)
    - active_error = Sum_{j: b_j*b_{j+1} <= p} D_j^2
    """
    N = p - 1
    fracs, n, D_vals, delta_vals, denom_prods = build_farey_with_data(N, p)

    # Compute sums (skip endpoints 0/1 and 1/1)
    B_raw_half = 0.0   # Sum D*delta
    delta_sq = 0.0     # Sum delta^2
    old_D_sq = 0.0     # Sum D^2

    for j, (a, b) in enumerate(fracs):
        if a == 0 or (a == 1 and b == 1):
            old_D_sq += D_vals[j] ** 2
            continue
        D = D_vals[j]
        d = delta_vals[j]
        B_raw_half += D * d
        delta_sq += d * d
        old_D_sq += D * D

    # Also include 0/1: D(0)=0, delta(0)=0; 1/1: D=-1, delta=0

    B_raw = 2 * B_raw_half
    B_plus_C = B_raw + delta_sq

    if delta_sq > 0:
        R = B_raw / delta_sq
    else:
        R = 0.0

    # Integral = Sum_j D_j^2 / (b_j * b_{j+1})
    integral = 0.0
    active_error = 0.0
    for j in range(len(fracs) - 1):
        bp = denom_prods[j]  # b_j * b_{j+1}
        D_j = D_vals[j]
        integral += D_j * D_j / bp
        if bp <= p:
            active_error += D_j * D_j

    # dilution_raw = old_D_sq * (n'^2 - n^2) / n^2
    n_prime = n + p - 1
    dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2

    # integral_ratio = n * integral / (2 * old_D_sq)
    if old_D_sq > 0:
        integral_ratio = n * integral / (2 * old_D_sq)
    else:
        integral_ratio = 0.0

    if dilution_raw > 0:
        active_ratio = active_error / dilution_raw
        R1_approx = n * integral / (2 * old_D_sq)
    else:
        active_ratio = 0.0
        R1_approx = 0.0

    return {
        'p': p, 'n': n,
        'B_plus_C': B_plus_C,
        'B_raw': B_raw,
        'delta_sq': delta_sq,
        'R': R,
        'old_D_sq': old_D_sq,
        'dilution_raw': dilution_raw,
        'integral': integral,
        'integral_ratio': integral_ratio,  # = n*integral/(2*old_D_sq)
        'active_error': active_error,
        'active_ratio': active_ratio,      # active_error/dilution_raw
        'R1_approx': R1_approx,            # non-circular approx to R_1
    }


# ============================================================
# MAIN ANALYSIS
# ============================================================

if __name__ == '__main__':
    max_p = int(sys.argv[1]) if len(sys.argv) > 1 else 1000

    primes = sieve_primes(max_p)
    test_primes = [p for p in primes if p >= 11]

    print("=" * 90)
    print(f"B+C VERIFICATION AND INTEGRAL RATIO ANALYSIS for p in [11, {max_p}]")
    print("=" * 90)
    print()

    results = []
    failures = []
    min_BpC = float('inf')
    min_R = float('inf')
    max_active_ratio = 0.0

    print(f"{'p':>6} {'B+C>0':>6} {'R':>8} {'int_ratio':>10} "
          f"{'act_ratio':>10} {'R1_approx':>10} {'time(s)':>8}")
    print("-" * 90)

    for p in test_primes:
        t0 = time.time()
        res = compute_bc(p)
        dt = time.time() - t0
        results.append(res)

        ok = res['B_plus_C'] > 0
        if not ok:
            failures.append(p)

        if res['B_plus_C'] < min_BpC:
            min_BpC = res['B_plus_C']
        if res['R'] < min_R:
            min_R = res['R']
        if res['active_ratio'] > max_active_ratio:
            max_active_ratio = res['active_ratio']

        # Print every 5th prime to keep output manageable
        if p <= 200 or p % 50 == 1 or not ok:
            print(f"{p:6d} {'YES' if ok else 'FAIL':>6} {res['R']:+8.4f} "
                  f"{res['integral_ratio']:10.4f} {res['active_ratio']:10.4f} "
                  f"{res['R1_approx']:10.4f} {dt:8.3f}s")

    print()
    print("=" * 90)
    print("SUMMARY")
    print("=" * 90)
    print(f"  Total primes checked:     {len(test_primes)}")
    print(f"  Failures (B+C <= 0):      {len(failures)}")
    if failures:
        print(f"  Failing primes:           {failures}")
    print(f"  Min B+C value:            {min_BpC:.6e}")
    print(f"  Min R value:              {min_R:.6f}")
    print(f"  Max active_error/dil:     {max_active_ratio:.6f}")
    print()

    if len(failures) == 0:
        print("  *** ALL PRIMES PASS: B+C > 0 verified for p in [11, {}] ***".format(max_p))
    else:
        print(f"  *** FAILURES DETECTED at: {failures} ***")

    print()
    print("=" * 90)
    print("INTEGRAL RATIO ANALYSIS (n * integral / (2 * old_D_sq))")
    print("=" * 90)
    print()
    print("The integral ratio is the non-circular approximation to R_1 = D/A.")
    print("If integral_ratio >= 1 - epsilon, then R_1 >= 1 - epsilon - active_ratio.")
    print("Key finding: is integral_ratio consistently close to 1?")
    print()

    # Show integral ratio by range
    ranges = [(11, 50), (50, 100), (100, 200), (200, 500), (500, max_p+1)]
    for lo, hi in ranges:
        subset = [r for r in results if lo <= r['p'] < hi]
        if not subset:
            continue
        ir_vals = [r['integral_ratio'] for r in subset]
        ar_vals = [r['active_ratio'] for r in subset]
        print(f"  p in [{lo:5d},{hi:5d}):  "
              f"mean_int_ratio={sum(ir_vals)/len(ir_vals):.4f}  "
              f"min={min(ir_vals):.4f}  max={max(ir_vals):.4f}  "
              f"max_active_ratio={max(ar_vals):.4f}")

    print()
    print("=" * 90)
    print("FLOOR-ERROR ANALYSIS")
    print("=" * 90)
    print()
    print("Key question: Is active_error / dilution_raw -> 0?")
    print("If YES: R_1 = integral_ratio + o(1), and integral_ratio >= 1 proves R_1 >= 1 - o(1).")
    print()

    for r in results:
        p = r['p']
        if p in [11, 23, 47, 97, 199, 307, 499, 997, max_p]:
            N = p - 1
            print(f"  p={p:6d}: active_error/dil = {r['active_ratio']:.4f}, "
                  f"log^2(N)/N = {log(N)**2/N:.4f}, "
                  f"ratio/theory = {r['active_ratio'] / (log(N)**2/N + 1e-10):.2f}")

    print()
    print(f"Total time: {time.time() - start_time:.1f}s")
