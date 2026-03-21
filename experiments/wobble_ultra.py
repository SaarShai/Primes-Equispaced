#!/usr/bin/env python3
"""
Ultra-Fast Wobble Analysis using Stern-Brocot / Mediant-Based Farey Generation
===============================================================================

The bottleneck in the previous approach was sorting millions of fractions.
This version uses the classical O(N) Farey generation algorithm that produces
fractions in sorted order WITHOUT sorting, then computes wobble in one pass.

The algorithm: given F_N in order, F_{N+1} is obtained by inserting mediants
(a+c)/(b+d) between consecutive neighbors a/b, c/d whenever b+d = N+1.

But for our purposes, we regenerate F_N from scratch each time using the
next-term algorithm: given a/b in F_N, the next term c/d is determined by
c/d = (floor((N+b)/d_prev) * c_prev - a_prev) / ...

Actually, the fastest approach: generate F_N directly using the standard
next-term recurrence, compute wobble in one O(|F_N|) pass.
"""

import numpy as np
from math import gcd
import time
import sys
import json
import os


def farey_sequence_generator(N):
    """Generate Farey sequence F_N in order using the next-term algorithm.
    Yields (numerator, denominator) pairs.
    This is O(|F_N|) time and O(1) space — no sorting needed.
    """
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b


def compute_wobble_from_generator(N):
    """Compute W(N) = Σ (f_j - j/|F_N|)² by generating F_N in order.

    Two-pass approach: first count |F_N|, then compute wobble.
    Actually we can compute in one pass if we know |F_N| in advance.
    |F_N| = 1 + Σ_{k=1}^{N} φ(k).
    """
    # Pre-compute |F_N| using totient sieve
    phi = list(range(N + 1))
    for p in range(2, N + 1):
        if phi[p] == p:  # p is prime
            for k in range(p, N + 1, p):
                phi[k] -= phi[k] // p
    farey_size = 1 + sum(phi[1:N+1])

    # Now compute wobble in one pass
    w = 0.0
    for j, (a, b) in enumerate(farey_sequence_generator(N)):
        f = a / b
        ideal = j / farey_size
        delta = f - ideal
        w += delta * delta

    return w, farey_size


def sieve_primes(limit):
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return sieve


def run_ultra(max_N=5000):
    output_dir = os.path.dirname(os.path.abspath(__file__))
    is_prime = sieve_primes(max_N)
    primes_list = [i for i in range(2, max_N + 1) if is_prime[i]]

    print(f"Ultra-Fast Wobble Analysis up to N = {max_N}")
    print(f"Primes to test: {len(primes_list)}")
    print("=" * 70)

    wobbles = {}
    prime_results = []
    composite_results = []

    t0 = time.time()

    for N in range(1, max_N + 1):
        w, fs = compute_wobble_from_generator(N)
        wobbles[N] = w

        if N >= 2:
            delta = wobbles[N-1] - w

            if is_prime[N]:
                prime_results.append({
                    'p': N,
                    'delta': delta,
                    'wobble': w,
                    'farey_size': fs,
                })
            else:
                composite_results.append({
                    'n': N,
                    'delta': delta,
                })

        if N % 500 == 0:
            elapsed = time.time() - t0
            rate = N / elapsed if elapsed > 0 else 0
            eta = (max_N - N) / rate if rate > 0 else 0
            n_primes_done = len(prime_results)
            n_violations = sum(1 for r in prime_results if r['p'] >= 11 and r['delta'] > 0)
            print(f"  N={N:5d}  |F|={fs:8d}  W={w:.10f}"
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

    # Violations
    viol_primes = [v['p'] for v in violations]
    print(f"\n  Violations (primes ≥ 11 decreasing wobble): {len(violations)}")
    print(f"  Violation primes: {viol_primes}")

    # Cluster analysis
    if viol_primes:
        clusters = [[viol_primes[0]]]
        for p in viol_primes[1:]:
            if p - clusters[-1][-1] <= 50:
                clusters[-1].append(p)
            else:
                clusters.append([p])
        print(f"\n  Violation clusters (gap > 50 = new cluster):")
        for i, cl in enumerate(clusters):
            print(f"    Cluster {i+1}: {cl} (size {len(cl)}, span {cl[-1]-cl[0]})")

        cluster_sizes = [len(cl) for cl in clusters]
        print(f"\n  Cluster sizes: {cluster_sizes}")
        print(f"  ALL CLUSTERS SIZE 5? {all(s == 5 for s in cluster_sizes)}")

    # Streak analysis
    all_p = [(r['p'], r['delta']) for r in prime_results if r['p'] >= 11]
    streaks = []
    current = 0
    for p, delta in all_p:
        if delta < 0:
            current += 1
        else:
            if current > 0:
                streaks.append(current)
            current = 0
    if current > 0:
        streaks.append(current)

    violation_streaks = []
    current = 0
    for p, delta in all_p:
        if delta > 0:
            current += 1
        else:
            if current > 0:
                violation_streaks.append(current)
            current = 0
    if current > 0:
        violation_streaks.append(current)

    print(f"\n  Increasing streaks (between violation clusters): {streaks}")
    print(f"  Violation streak sizes: {violation_streaks}")

    # Violation rate by range
    print(f"\n  Violation rate by range:")
    for lo in range(0, max_N, 1000):
        hi = lo + 1000
        in_range = [r for r in primes_ge11 if lo <= r['p'] < hi]
        viols = [r for r in in_range if r['delta'] > 0]
        if in_range:
            print(f"    [{lo:5d}, {hi:5d}): {len(in_range):3d} primes, {len(viols):2d} violations ({100*len(viols)/len(in_range):.1f}%)")

    # Power law
    ps = np.array([r['p'] for r in primes_ge11 if r['delta'] < 0])
    dws = np.array([-r['delta'] for r in primes_ge11 if r['delta'] < 0])
    if len(ps) > 10 and np.all(dws > 0):
        coeffs = np.polyfit(np.log(ps), np.log(dws), 1)
        print(f"\n  Power law: |ΔW(p)| ~ p^{coeffs[0]:.4f}")

    # Save
    output_file = os.path.join(output_dir, "wobble_ultra_data.json")
    save_data = {
        'max_N': max_N,
        'total_primes': total_p,
        'violations': viol_primes,
        'all_decreasing_primes': [r['p'] for r in prime_results if r['delta'] > 0],
        'cluster_sizes': cluster_sizes if viol_primes else [],
        'increasing_streaks': streaks,
        'violation_streaks': violation_streaks,
        'prime_results': prime_results,
    }
    with open(output_file, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"\n  Data saved to {output_file}")


if __name__ == '__main__':
    max_N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run_ultra(max_N=max_N)
