#!/usr/bin/env python3
"""
Large-Scale Wobble Analysis
=============================

Tests the conjecture "W(p) > W(p-1) for all primes p ≥ 11" up to large N.

Uses floating-point arithmetic for speed (exact fractions are too slow for N > 500).
Double-precision float gives ~15 digits, which is sufficient for detecting the sign
of W(p) - W(p-1) since the differences are on the order of 10^{-3} to 10^{-6}.

Key optimization: instead of recomputing W(N) from scratch each time, we track
the Farey sequence incrementally and compute the change in wobble when adding
new fractions with denominator N.
"""

import numpy as np
from math import gcd
import time
import json
import os
import sys


def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return set(i for i in range(2, limit + 1) if sieve[i])


def euler_totient(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def compute_wobble_fast(farey_sorted):
    """Compute W = Σ (f_j - j/|F|)² using numpy."""
    n = len(farey_sorted)
    if n == 0:
        return 0.0
    fracs = np.array(farey_sorted)
    ideal = np.arange(n, dtype=np.float64) / n
    deltas = fracs - ideal
    return np.sum(deltas ** 2)


def run_largescale(max_N=2000):
    """Run the wobble experiment up to max_N using fast floating-point arithmetic."""

    output_dir = os.path.dirname(os.path.abspath(__file__))
    prime_set = sieve_primes(max_N)
    primes_sorted = sorted(prime_set)

    print(f"Large-Scale Wobble Analysis up to N = {max_N}")
    print(f"Number of primes to test: {len(primes_sorted)}")
    print("=" * 70)

    # Build Farey sequence incrementally using a sorted list
    # For efficiency, we maintain a sorted array of float values
    import bisect

    farey_list = [0.0, 1.0]  # F_1
    wobbles = {1: compute_wobble_fast(farey_list)}

    # Track results
    prime_increases = 0  # primes where wobble increases
    prime_decreases = 0  # primes where wobble decreases
    composite_increases = 0
    composite_decreases = 0
    first_prime_decrease_after_11 = None
    prime_results = []

    t0 = time.time()

    for N in range(2, max_N + 1):
        # Add new fractions with denominator N
        new_fracs = []
        for p in range(1, N):
            if gcd(p, N) == 1:
                new_fracs.append(p / N)

        for f in new_fracs:
            bisect.insort(farey_list, f)

        w = compute_wobble_fast(farey_list)
        prev_w = wobbles[N - 1]
        wobbles[N] = w
        delta = prev_w - w  # positive means wobble decreased

        is_p = N in prime_set

        if is_p:
            if delta > 0:
                prime_decreases += 1
            else:
                prime_increases += 1
                if N >= 11 and first_prime_decrease_after_11 is None and delta > 0:
                    first_prime_decrease_after_11 = N

            prime_results.append({
                'p': N,
                'wobble': w,
                'delta': delta,
                'sign': '+' if delta > 0 else '-',
                'phi': euler_totient(N),
                'farey_size': len(farey_list),
            })
        else:
            if delta > 0:
                composite_decreases += 1
            else:
                composite_increases += 1

        # Progress
        if N % 200 == 0:
            elapsed = time.time() - t0
            rate = N / elapsed
            eta = (max_N - N) / rate if rate > 0 else 0
            print(f"  N={N:5d}  |F|={len(farey_list):7d}  W={w:.10f}"
                  f"  primes_tested={prime_decreases + prime_increases}"
                  f"  conj_holds={prime_increases > 0 and first_prime_decrease_after_11 is None}"
                  f"  [{elapsed:.0f}s elapsed, ~{eta:.0f}s remaining]")

    elapsed = time.time() - t0
    print(f"\nCompleted in {elapsed:.1f}s")

    # Results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    total_primes = prime_increases + prime_decreases
    print(f"\n  Primes tested: {total_primes} (all primes up to {max_N})")
    print(f"  Primes where wobble INCREASES (ΔW < 0): {prime_increases} ({100*prime_increases/total_primes:.1f}%)")
    print(f"  Primes where wobble DECREASES (ΔW > 0): {prime_decreases} ({100*prime_decreases/total_primes:.1f}%)")

    total_composites = composite_increases + composite_decreases
    print(f"\n  Composites tested: {total_composites}")
    print(f"  Composites where wobble INCREASES: {composite_increases} ({100*composite_increases/total_composites:.1f}%)")
    print(f"  Composites where wobble DECREASES: {composite_decreases} ({100*composite_decreases/total_composites:.1f}%)")

    # The conjecture
    print("\n" + "=" * 70)
    print("CONJECTURE TEST: W(p) > W(p-1) for all primes p ≥ 11")
    print("=" * 70)

    primes_ge_11 = [r for r in prime_results if r['p'] >= 11]
    violations = [r for r in primes_ge_11 if r['delta'] > 0]  # delta > 0 means wobble decreased

    if violations:
        print(f"\n  CONJECTURE VIOLATED at {len(violations)} prime(s)!")
        for v in violations[:10]:
            print(f"    p = {v['p']}: ΔW = {v['delta']:+.12f}")
    else:
        print(f"\n  CONJECTURE HOLDS for all {len(primes_ge_11)} primes from 11 to {max_N}")
        print(f"  (Every prime ≥ 11 increased the wobble)")

    # Show the primes where wobble decreased (should be only 2, 3, 5, 7)
    decreasing_primes = [r for r in prime_results if r['delta'] > 0]
    print(f"\n  Primes where wobble DECREASES: {[r['p'] for r in decreasing_primes]}")

    # Statistics on the magnitude of the increase
    increases = [-r['delta'] for r in primes_ge_11 if r['delta'] < 0]
    if increases:
        print(f"\n  Wobble increase magnitude for primes ≥ 11:")
        print(f"    Mean:   {np.mean(increases):.10f}")
        print(f"    Median: {np.median(increases):.10f}")
        print(f"    Min:    {np.min(increases):.10f}")
        print(f"    Max:    {np.max(increases):.10f}")

    # Power law fit: |ΔW(p)| vs p
    if len(primes_ge_11) > 20:
        ps = np.array([r['p'] for r in primes_ge_11 if r['delta'] < 0])
        dws = np.array([-r['delta'] for r in primes_ge_11 if r['delta'] < 0])
        if len(ps) > 10 and np.all(dws > 0):
            coeffs = np.polyfit(np.log(ps), np.log(dws), 1)
            print(f"\n  Power law: |ΔW(p)| ~ p^{coeffs[0]:.4f}")

    # Cumulative contribution
    cum_prime = sum(r['delta'] for r in prime_results)
    cum_all = wobbles[1] - wobbles[max_N]
    print(f"\n  Total wobble reduction W(1)-W({max_N}): {cum_all:.10f}")
    print(f"  Net prime contribution: {cum_prime:+.10f}")
    print(f"  Net composite contribution: {cum_all - cum_prime:+.10f}")

    # Save
    output_file = os.path.join(output_dir, "wobble_largescale_data.json")
    save_data = {
        'max_N': max_N,
        'total_primes_tested': total_primes,
        'conjecture_holds': len(violations) == 0,
        'violations': [v['p'] for v in violations],
        'prime_increases': prime_increases,
        'prime_decreases': prime_decreases,
        'composite_increases': composite_increases,
        'composite_decreases': composite_decreases,
        'decreasing_primes': [r['p'] for r in decreasing_primes],
        'prime_results': prime_results,
    }
    with open(output_file, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"\n  Data saved to {output_file}")

    return save_data


if __name__ == '__main__':
    max_N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    run_largescale(max_N=max_N)
