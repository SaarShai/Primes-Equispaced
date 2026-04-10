#!/usr/bin/env python3
"""
FAST LARGE-SCALE VERIFICATION: B+C > 0 for all primes up to LIMIT
==================================================================

Uses fast Farey generation (mediant algorithm) to verify B+C > 0
for all primes up to 5000.

KEY QUANTITIES:
  B + C = 2*Sigma_{F_{p-1}} D(f)*delta(f) + Sigma delta(f)^2
        = Sigma_{F_{p-1}} [2*D(f)*delta(f) + delta(f)^2]
        = Sigma_{F_{p-1}} t(f)

  delta(a/b) = (a - (p*a mod b)) / b

FAST ALGORITHM:
  - Generate F_{p-1} via mediant algorithm (O(n) time).
  - For each fraction, compute D and delta together.
  - Sum t(f) = 2*D*delta + delta^2 incrementally.

Also computes:
  - 1+R = B+C / delta_sq (monitor that it stays positive)
  - old_D_sq, delta_sq separately
  - Minimum margin: min over all p of (B+C)
"""

import time
import sys
from math import isqrt, log

start_time = time.time()


def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def compute_BC_fast(p):
    """
    Fast computation of B+C for prime p using Farey mediant algorithm.

    Returns: (B_plus_C, delta_sq, old_D_sq, n)
    """
    N = p - 1

    # Farey mediant generation: track a, b, c, d
    a, b = 0, 1
    c, d = 1, N

    n = 1 + sum(1 for _ in range(0))   # will count during generation

    # First pass: count n = |F_N|
    # Use the formula n = 1 + sum phi(k) for k=1..N
    # We need n to compute D = rank - n*f
    # Use Euler sieve for phi
    phi = list(range(N + 1))
    for i in range(2, N + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, N + 1, i):
                phi[j] -= phi[j] // i
    n = 1 + sum(phi[k] for k in range(1, N + 1))

    # Second pass: compute B+C using mediant algorithm
    B_plus_C = 0.0
    delta_sq = 0.0
    old_D_sq = 0.0

    # Iterate through F_N using mediant algorithm
    # Current fraction is (a/b), next is (c/d)
    a, b, c, d = 0, 1, 1, N
    rank = 0

    # Process (0/1)
    f = 0.0  # a/b = 0/1
    D = rank - n * f  # = 0
    delta_a = 0  # sigma_p(0) = 0, delta = 0/1 = 0
    delta = 0.0
    t = 2 * D * delta + delta * delta
    B_plus_C += t
    delta_sq += delta * delta
    old_D_sq += D * D

    while c <= N:
        rank += 1
        # Current fraction is c/d
        f_cd = c / d
        D = rank - n * f_cd
        sigma = (p * c) % d
        delta_a_val = c - sigma
        delta = delta_a_val / d
        t = 2 * D * delta + delta * delta
        B_plus_C += t
        delta_sq += delta * delta
        old_D_sq += D * D

        # Advance mediant
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

    return B_plus_C, delta_sq, old_D_sq, n


def main():
    LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"Fast verification of B+C > 0 for all primes in [11, {LIMIT}]", flush=True)
    print("=" * 80)
    print()

    primes = sieve_primes(LIMIT)
    test_primes = [p for p in primes if p >= 11]

    min_1pR = float('inf')
    min_1pR_p = 0
    min_BC = float('inf')
    min_BC_p = 0
    violations = []

    print(f"{'p':>6} {'B+C':>14} {'delta_sq':>14} {'1+R':>8} {'elapsed':>8}")
    print("-" * 60)

    prev_print = 0
    for i, p in enumerate(test_primes):
        BC, dsq, odsq, n = compute_BC_fast(p)

        one_pR = BC / dsq if dsq > 0 else float('inf')

        if BC < min_BC:
            min_BC = BC
            min_BC_p = p
        if one_pR < min_1pR:
            min_1pR = one_pR
            min_1pR_p = p
        if BC <= 0:
            violations.append((p, BC, dsq))

        elapsed = time.time() - start_time
        should_print = (p <= 100 or i % 200 == 0 or
                        one_pR < min_1pR * 1.05 or
                        BC < min_BC * 1.05 or
                        elapsed - prev_print > 15 or
                        p > LIMIT - 20)

        if should_print:
            print(f"{p:6d} {BC:14.2f} {dsq:14.2f} {one_pR:8.4f} {elapsed:8.1f}s",
                  flush=True)
            prev_print = elapsed

    print()
    print("=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"  Primes tested: {len(test_primes)} (all in [11, {test_primes[-1]}])")
    print(f"  Violations (B+C <= 0): {len(violations)}")
    if violations:
        for v in violations:
            print(f"    VIOLATION: p={v[0]}, B+C={v[1]:.6f}, delta_sq={v[2]:.6f}")
    print()
    print(f"  Minimum B+C: {min_BC:.4f}  at p = {min_BC_p}")
    print(f"  Minimum 1+R = B+C/delta_sq: {min_1pR:.6f}  at p = {min_1pR_p}")
    print()
    if not violations:
        print(f"  *** B+C > 0 VERIFIED for ALL primes in [11, {test_primes[-1]}] ***")
    print()

    # Key analysis
    if min_1pR > 0:
        print(f"  The minimum 1+R = {min_1pR:.4f} > 0 means:")
        print(f"  B + C >= {min_1pR:.4f} * delta_sq > 0  for all tested primes.")
        print()
        print(f"  Since delta_sq >= N^2/(48 log N) for N >= 100, this gives:")
        p_cross = min_1pR_p
        N_cross = p_cross - 1
        if N_cross >= 100:
            from math import log
            dlt_lb = N_cross**2 / (48 * log(N_cross))
            print(f"  At p={min_1pR_p}: B+C >= {min_1pR:.4f} * {dlt_lb:.2f} = {min_1pR * dlt_lb:.2f}")
        print()
        print(f"  For p > {test_primes[-1]}: B+C > 0 needs further verification or proof.")

    print(f"\nTotal runtime: {time.time() - start_time:.1f}s")


if __name__ == '__main__':
    main()
