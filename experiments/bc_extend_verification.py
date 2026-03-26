#!/usr/bin/env python3
"""
EXTENDED VERIFICATION: B + C > 0 for all primes p with M(p) <= -3
==================================================================

Extends the B+C > 0 verification to large primes. The key filter is that
we ONLY need to check primes where the Mertens function M(p) <= -3,
since for M(p) >= -2 the result holds by other arguments.

Computation method:
  - Sieve mu(k) and accumulate M(p) = Sum_{k=1}^p mu(k) for all primes p
  - For primes with M(p) <= -3, generate the Farey sequence F_{p-1} via
    the mediant algorithm and compute:
      B_raw = 2 * Sum D(f) * delta(f)
      delta_sq = Sum delta(f)^2
      B + C = B_raw + delta_sq
  - Report violations, minimum R = B_raw/delta_sq, etc.

Target: p <= 10000 first (minutes), then p <= 50000 (hours).
"""

import time
import sys
import csv
import os
from math import isqrt, log

start_time = time.time()

BASE = os.path.dirname(os.path.abspath(__file__))


def sieve_mu(limit):
    """Compute mu(k) for k = 0..limit using a sieve."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    # Smallest prime factor sieve
    spf = list(range(limit + 1))
    for i in range(2, isqrt(limit) + 1):
        if spf[i] == i:  # i is prime
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i

    for n in range(2, limit + 1):
        if spf[n] == n:
            # n is prime
            mu[n] = -1
        else:
            p = spf[n]
            m = n // p
            if m % p == 0:
                # p^2 divides n => mu = 0
                mu[n] = 0
            else:
                mu[n] = -mu[m]
    return mu


def sieve_primes(limit):
    """Return list of primes up to limit."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def compute_BC_fast(p):
    """
    Fast computation of B_raw, delta_sq, B+C for prime p.
    Uses Farey mediant algorithm: O(|F_{p-1}|) time, O(p) space for phi.

    Returns: (B_plus_C, B_raw, delta_sq, n_farey)
    """
    N = p - 1

    # Compute |F_N| = 1 + sum_{k=1}^N phi(k) via Euler sieve
    phi = list(range(N + 1))
    for i in range(2, N + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, N + 1, i):
                phi[j] -= phi[j] // i
    n = 1 + sum(phi[k] for k in range(1, N + 1))

    # Traverse F_N via mediant algorithm, accumulating B_raw and delta_sq
    B_raw_half = 0.0  # Sum D * delta (we'll double at end)
    delta_sq = 0.0

    # Start: 0/1, next = 1/N
    a, b, c, d = 0, 1, 1, N
    rank = 0
    # Process 0/1: D=0, delta=0 => contributes nothing

    while c <= N:
        rank += 1
        # Current fraction is c/d
        f_val = c / d
        D = rank - n * f_val
        sigma = (p * c) % d
        delta_val = (c - sigma) / d
        B_raw_half += D * delta_val
        delta_sq += delta_val * delta_val

        # Advance mediant
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

    B_raw = 2.0 * B_raw_half
    B_plus_C = B_raw + delta_sq
    return B_plus_C, B_raw, delta_sq, n


def main():
    LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    M_THRESHOLD = -3

    print(f"EXTENDED B+C VERIFICATION for primes with M(p) <= {M_THRESHOLD}, p <= {LIMIT}")
    print("=" * 90)
    print()

    # Step 1: Sieve mu and compute Mertens function
    print(f"[1] Sieving mu(k) for k <= {LIMIT}...", flush=True)
    t0 = time.time()
    mu = sieve_mu(LIMIT)
    print(f"    Done in {time.time()-t0:.1f}s", flush=True)

    # Step 2: Compute M(p) for all primes
    print(f"[2] Computing M(p) for all primes up to {LIMIT}...", flush=True)
    primes = sieve_primes(LIMIT)
    M_cumulative = 0
    prime_mertens = {}  # p -> M(p)
    j = 0
    for k in range(1, LIMIT + 1):
        M_cumulative += mu[k]
        if j < len(primes) and primes[j] == k:
            prime_mertens[k] = M_cumulative
            j += 1

    # Filter: primes with M(p) <= threshold
    target_primes = sorted([p for p in primes if prime_mertens[p] <= M_THRESHOLD and p >= 11])
    all_test_primes = [p for p in primes if p >= 11]

    print(f"    Total primes in [11, {LIMIT}]: {len(all_test_primes)}")
    print(f"    Primes with M(p) <= {M_THRESHOLD}: {len(target_primes)}")
    if target_primes:
        print(f"    Range: p in [{target_primes[0]}, {target_primes[-1]}]")
        # Distribution of M(p) values
        m_vals = [prime_mertens[p] for p in target_primes]
        print(f"    M(p) range: [{min(m_vals)}, {max(m_vals)}]")
    print()

    # Step 3: Compute B+C for target primes
    print(f"[3] Computing B+C for {len(target_primes)} primes with M(p) <= {M_THRESHOLD}...")
    print()
    print(f"{'p':>7} {'M(p)':>5} {'B+C':>16} {'B_raw':>16} {'delta_sq':>14} {'R=B/dsq':>9} {'|F_N|':>10} {'time':>7}")
    print("-" * 95)

    violations = []
    min_R = float('inf')
    min_R_p = 0
    min_BC = float('inf')
    min_BC_p = 0
    results = []

    prev_print_time = 0
    for idx, p in enumerate(target_primes):
        t0 = time.time()
        BC, B_raw, dsq, n_farey = compute_BC_fast(p)
        dt = time.time() - t0

        R = B_raw / dsq if dsq > 0 else float('inf')

        if BC < min_BC:
            min_BC = BC
            min_BC_p = p
        if R < min_R:
            min_R = R
            min_R_p = p
        if BC <= 0:
            violations.append((p, prime_mertens[p], BC, B_raw, dsq))

        results.append({
            'p': p,
            'M': prime_mertens[p],
            'BC': BC,
            'B_raw': B_raw,
            'delta_sq': dsq,
            'R': R,
            'n_farey': n_farey,
        })

        elapsed = time.time() - start_time
        # Print first few, last few, new minima, violations, and periodic updates
        should_print = (
            idx < 5 or
            idx >= len(target_primes) - 3 or
            BC <= 0 or
            R < min_R * 1.01 or
            elapsed - prev_print_time > 30 or
            idx % 100 == 0
        )

        if should_print:
            print(f"{p:7d} {prime_mertens[p]:5d} {BC:16.4f} {B_raw:16.4f} {dsq:14.4f} {R:9.4f} {n_farey:10d} {dt:6.1f}s",
                  flush=True)
            prev_print_time = elapsed

    elapsed_total = time.time() - start_time
    print()
    print("=" * 90)
    print("VERIFICATION SUMMARY")
    print("=" * 90)
    print(f"  Target:               p <= {LIMIT}, M(p) <= {M_THRESHOLD}")
    print(f"  Primes tested:        {len(target_primes)}")
    print(f"  Violations (B+C<=0):  {len(violations)}")
    if violations:
        print()
        print("  VIOLATIONS:")
        for v in violations:
            print(f"    p={v[0]}, M(p)={v[1]}, B+C={v[2]:.6e}, B_raw={v[3]:.6e}, dsq={v[4]:.6e}")
    print()
    print(f"  Min B+C:              {min_BC:.6f}  at p={min_BC_p} (M={prime_mertens.get(min_BC_p, '?')})")
    print(f"  Min R = B_raw/dsq:    {min_R:.6f}  at p={min_R_p} (M={prime_mertens.get(min_R_p, '?')})")
    print()

    if not violations:
        print(f"  *** B + C > 0 VERIFIED for ALL {len(target_primes)} primes with M(p)<={M_THRESHOLD} up to p={LIMIT} ***")
    else:
        print(f"  *** FAILED: {len(violations)} violations found ***")

    print()

    # Step 4: Write CSV
    csv_path = os.path.join(BASE, f"bc_verify_{LIMIT}.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["p", "M(p)", "B_plus_C", "B_raw", "delta_sq", "R", "n_farey"])
        for r in results:
            writer.writerow([r['p'], r['M'], f"{r['BC']:.10f}", f"{r['B_raw']:.10f}",
                             f"{r['delta_sq']:.10f}", f"{r['R']:.10f}", r['n_farey']])
    print(f"  Results saved to {csv_path}")

    # Step 5: Statistics by M(p) value
    print()
    print("STATISTICS BY M(p) VALUE:")
    print("-" * 70)
    from collections import defaultdict
    by_m = defaultdict(list)
    for r in results:
        by_m[r['M']].append(r)

    print(f"{'M(p)':>6} {'count':>6} {'min_R':>10} {'min_BC':>14} {'worst_p':>8}")
    for m in sorted(by_m.keys()):
        group = by_m[m]
        worst = min(group, key=lambda r: r['R'])
        worst_bc = min(group, key=lambda r: r['BC'])
        print(f"{m:6d} {len(group):6d} {worst['R']:10.4f} {worst_bc['BC']:14.4f} {worst['p']:8d}")

    print()
    print(f"Total runtime: {elapsed_total:.1f}s")


if __name__ == '__main__':
    main()
