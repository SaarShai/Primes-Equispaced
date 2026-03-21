#!/usr/bin/env python3
"""
Fast Large-Scale Wobble Analysis using numpy
=============================================

Optimized for N up to 5000+. Key optimizations:
- Use numpy arrays instead of Python lists
- Batch-insert new fractions and re-sort (numpy sort is fast)
- Vectorized wobble computation
"""

import numpy as np
from math import gcd
import time
import json
import os
import sys


def sieve_primes(limit):
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return sieve


def euler_totient_sieve(limit):
    """Compute φ(n) for all n up to limit using a sieve."""
    phi = np.arange(limit + 1, dtype=np.int64)
    for p in range(2, limit + 1):
        if phi[p] == p:  # p is prime
            phi[p::p] -= phi[p::p] // p
    return phi


def compute_wobble(sorted_fracs):
    """Compute W = Σ (f_j - j/n)² vectorized."""
    n = len(sorted_fracs)
    if n == 0:
        return 0.0
    ideal = np.arange(n, dtype=np.float64) / n
    deltas = sorted_fracs - ideal
    return np.dot(deltas, deltas)


def run_fast(max_N=5000):
    output_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"Fast Wobble Analysis up to N = {max_N}")
    print("=" * 70)

    is_prime = sieve_primes(max_N)
    phi = euler_totient_sieve(max_N)
    primes_list = np.where(is_prime)[0]
    print(f"Primes to test: {len(primes_list)}")

    # Build Farey fractions incrementally using a set for uniqueness
    # then sort into numpy array for wobble computation
    frac_set = {0.0, 1.0}

    wobbles = np.zeros(max_N + 1)
    wobbles[1] = 0.25  # W(F_1) for {0, 1}

    # Track results
    prime_results = []
    composite_results = []

    t0 = time.time()

    for N in range(2, max_N + 1):
        # Generate new fractions with denominator N
        new_fracs = []
        for p in range(1, N):
            if gcd(p, N) == 1:
                new_fracs.append(p / N)

        frac_set.update(new_fracs)

        # Sort and compute wobble
        sorted_arr = np.array(sorted(frac_set))
        w = compute_wobble(sorted_arr)
        wobbles[N] = w

        delta = wobbles[N-1] - w  # positive = wobble decreased

        if is_prime[N]:
            prime_results.append({
                'p': int(N),
                'delta': float(delta),
                'wobble': float(w),
                'phi': int(phi[N]),
                'farey_size': len(sorted_arr),
            })
        else:
            composite_results.append({
                'n': int(N),
                'delta': float(delta),
            })

        if N % 500 == 0:
            elapsed = time.time() - t0
            rate = N / elapsed if elapsed > 0 else 0
            eta = (max_N - N) / rate if rate > 0 else 0
            n_primes_done = len(prime_results)
            n_violations = sum(1 for r in prime_results if r['p'] >= 11 and r['delta'] > 0)
            print(f"  N={N:5d}  |F|={len(sorted_arr):8d}  W={w:.10f}"
                  f"  primes={n_primes_done}  violations={n_violations}"
                  f"  [{elapsed:.0f}s, ~{eta:.0f}s left]")

    elapsed = time.time() - t0
    print(f"\nCompleted in {elapsed:.1f}s")

    # Analysis
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    primes_ge11 = [r for r in prime_results if r['p'] >= 11]
    violations = [r for r in primes_ge11 if r['delta'] > 0]

    total_p = len(prime_results)
    p_increase = sum(1 for r in prime_results if r['delta'] < 0)
    p_decrease = sum(1 for r in prime_results if r['delta'] > 0)

    total_c = len(composite_results)
    c_increase = sum(1 for r in composite_results if r['delta'] < 0)
    c_decrease = sum(1 for r in composite_results if r['delta'] > 0)

    print(f"\n  Primes: {total_p} total")
    print(f"    Wobble INCREASES: {p_increase} ({100*p_increase/total_p:.1f}%)")
    print(f"    Wobble DECREASES: {p_decrease} ({100*p_decrease/total_p:.1f}%)")

    print(f"\n  Composites: {total_c} total")
    print(f"    Wobble INCREASES: {c_increase} ({100*c_increase/total_c:.1f}%)")
    print(f"    Wobble DECREASES: {c_decrease} ({100*c_decrease/total_c:.1f}%)")

    print(f"\n  Primes ≥ 11 where wobble DECREASES (violations): {len(violations)}")
    if violations:
        print(f"  Violation primes: {[v['p'] for v in violations]}")
        # Group violations into clusters (consecutive primes within gap ≤ 30)
        vp = sorted([v['p'] for v in violations])
        clusters = [[vp[0]]]
        for p in vp[1:]:
            if p - clusters[-1][-1] <= 30:
                clusters[-1].append(p)
            else:
                clusters.append([p])
        print(f"  Violation clusters: {clusters}")

    decreasing_primes = [r['p'] for r in prime_results if r['delta'] > 0]
    print(f"\n  ALL primes where wobble decreases: {decreasing_primes[:20]}{'...' if len(decreasing_primes) > 20 else ''}")

    # Power law
    if len(primes_ge11) > 20:
        ps = np.array([r['p'] for r in primes_ge11 if r['delta'] < 0])
        dws = np.array([-r['delta'] for r in primes_ge11 if r['delta'] < 0])
        if len(ps) > 10 and np.all(dws > 0):
            coeffs = np.polyfit(np.log(ps), np.log(dws), 1)
            print(f"\n  Power law: |ΔW(p)| ~ p^{coeffs[0]:.4f}")

    # Violation rate by range
    print("\n  Violation rate by range:")
    for lo in range(0, max_N, 1000):
        hi = lo + 1000
        in_range = [r for r in primes_ge11 if lo <= r['p'] < hi]
        viols = [r for r in in_range if r['delta'] > 0]
        if in_range:
            print(f"    [{lo:5d}, {hi:5d}): {len(in_range):3d} primes, {len(viols):2d} violations ({100*len(viols)/len(in_range):.1f}%)")

    # Save
    output_file = os.path.join(output_dir, "wobble_fast_data.json")
    save_data = {
        'max_N': max_N,
        'total_primes': total_p,
        'prime_increases_wobble': p_increase,
        'prime_decreases_wobble': p_decrease,
        'composite_increases_wobble': c_increase,
        'composite_decreases_wobble': c_decrease,
        'violations': [v['p'] for v in violations],
        'all_decreasing_primes': decreasing_primes,
        'prime_results': prime_results,
    }
    with open(output_file, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"\n  Data saved to {output_file}")

    return save_data


if __name__ == '__main__':
    max_N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    run_fast(max_N=max_N)
