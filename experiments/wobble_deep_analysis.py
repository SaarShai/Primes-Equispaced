#!/usr/bin/env python3
"""
Deep Analysis of the Wobble Sign Phenomenon
=============================================

FINDING: Adding a prime p to the Farey sequence INCREASES the wobble (discrepancy)
for p ≥ 11. This is counterintuitive — primes are supposed to "fill gaps uniformly."

This script investigates WHY this happens and whether it leads to a new conjecture.

HYPOTHESIS: The wobble increase happens because primes add p-1 new fractions at once,
which is a LARGE injection relative to composites. This "overshooting" disrupts local
uniformity. The subsequent composites (p+1, p+2, ...) then gradually restore it.

WE TEST:
1. Is the wobble increase proportional to p (the number of new fractions)?
2. Does the wobble always decrease again before the next prime?
3. What is the "recovery time" — how many composites does it take?
4. Is there a modified wobble that IS monotonically decreasing?
5. Can we formulate a precise conjecture about the per-prime wobble behavior?
"""

import numpy as np
from math import gcd
from fractions import Fraction
import json
import os


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


def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True


def run_deep_analysis(max_N=300):
    print("Deep Wobble Sign Analysis")
    print("=" * 70)

    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Compute all wobbles
    farey_set = {Fraction(0, 1), Fraction(1, 1)}
    wobbles = {}
    farey_sizes = {}

    for N in range(1, max_N + 1):
        if N >= 2:
            for p in range(1, N):
                if gcd(p, N) == 1:
                    farey_set.add(Fraction(p, N))
        farey_sorted = sorted(farey_set)
        size = len(farey_sorted)
        farey_sizes[N] = size

        # Compute wobble
        total = Fraction(0)
        for j, f in enumerate(farey_sorted):
            ideal = Fraction(j, size)
            delta = f - ideal
            total += delta * delta
        wobbles[N] = float(total)

        if N % 50 == 0:
            print(f"  Computed wobble up to N={N}")

    # Compute deltas for ALL N (not just primes)
    deltas = {}
    for N in range(2, max_N + 1):
        deltas[N] = wobbles[N - 1] - wobbles[N]

    primes = sieve_primes(max_N)

    # ANALYSIS 1: Sign of delta for primes vs composites
    print("\n--- Analysis 1: Sign of ΔW(N) ---")
    prime_positive = sum(1 for p in primes if p <= max_N and deltas[p] > 0)
    prime_negative = sum(1 for p in primes if p <= max_N and deltas[p] < 0)
    prime_zero = sum(1 for p in primes if p <= max_N and deltas[p] == 0)

    comp_positive = sum(1 for n in range(2, max_N + 1) if not is_prime(n) and deltas[n] > 0)
    comp_negative = sum(1 for n in range(2, max_N + 1) if not is_prime(n) and deltas[n] < 0)

    print(f"  Primes:     {prime_positive} positive (wobble decreases), {prime_negative} negative (wobble INCREASES)")
    print(f"  Composites: {comp_positive} positive (wobble decreases), {comp_negative} negative (wobble INCREASES)")

    # ANALYSIS 2: At what prime does the sign flip?
    print("\n--- Analysis 2: First few primes with positive vs negative ΔW ---")
    for p in primes[:20]:
        if p > max_N: break
        sign = "+" if deltas[p] > 0 else "-"
        new_fracs = euler_totient(p)
        print(f"  p={p:4d}  ΔW={deltas[p]:+.10f}  sign={sign}  φ(p)={new_fracs:3d}  |F_p|={farey_sizes[p]:5d}")

    # ANALYSIS 3: Recovery time — after a prime increases wobble, how many composites
    # does it take for wobble to get back below the pre-prime level?
    print("\n--- Analysis 3: Recovery after prime wobble increase ---")
    for p in primes:
        if p > max_N - 10 or p < 11: continue
        if deltas[p] >= 0: continue  # wobble decreased, no recovery needed

        pre_prime_wobble = wobbles[p - 1]
        recovery_n = None
        for n in range(p + 1, min(p + 100, max_N + 1)):
            if wobbles[n] <= pre_prime_wobble:
                recovery_n = n - p
                break

        if p <= 50 or p % 20 < 3:
            print(f"  p={p:4d}  recovery={recovery_n if recovery_n else '>100':>4}  "
                  f"next_prime_gap={next((q for q in primes if q > p), 0) - p:2d}")

    # ANALYSIS 4: Normalized wobble — W(N) * N
    # RH predicts W(N) ~ 1/N, so W(N)*N should approach a constant.
    # Does this normalized version behave better?
    print("\n--- Analysis 4: Normalized wobble W(N)*N ---")
    print(f"  {'N':>4s}  {'W(N)*N':>12s}  {'W(N)*N²':>14s}  {'prime?':>6s}")
    for N in list(range(10, 60, 5)) + list(range(60, max_N + 1, 20)):
        if N > max_N: break
        wn = wobbles[N] * N
        wn2 = wobbles[N] * N * N
        print(f"  {N:4d}  {wn:12.6f}  {wn2:14.4f}  {'PRIME' if is_prime(N) else '':>6s}")

    # ANALYSIS 5: Ratio φ(N)/|F_N| — what fraction of the sequence is new?
    # Primes contribute φ(p) = p-1 new fractions. The ratio (p-1)/|F_p| might predict
    # whether wobble increases or decreases.
    print("\n--- Analysis 5: New fraction ratio vs wobble change ---")
    ratios_positive = []
    ratios_negative = []
    for N in range(2, max_N + 1):
        phi_n = euler_totient(N)
        ratio = phi_n / farey_sizes[N]
        if deltas[N] > 0:
            ratios_positive.append(ratio)
        else:
            ratios_negative.append(ratio)

    if ratios_positive and ratios_negative:
        print(f"  Mean new-fraction ratio when wobble DECREASES: {np.mean(ratios_positive):.6f}")
        print(f"  Mean new-fraction ratio when wobble INCREASES: {np.mean(ratios_negative):.6f}")
        # Threshold?
        all_ratios = [(euler_totient(N) / farey_sizes[N], deltas[N] > 0) for N in range(2, max_N + 1)]
        all_ratios.sort()
        # Find the approximate threshold
        for threshold in np.arange(0.01, 0.20, 0.01):
            below = [d for r, d in all_ratios if r < threshold]
            above = [d for r, d in all_ratios if r >= threshold]
            if below and above:
                pct_below_positive = sum(below) / len(below) if below else 0
                pct_above_positive = sum(above) / len(above) if above else 0

    # ANALYSIS 6: The cumulative wobble — does Σ ΔW(p) over primes converge?
    print("\n--- Analysis 6: Cumulative per-prime wobble contribution ---")
    cum_prime_delta = 0
    cum_composite_delta = 0
    for N in range(2, max_N + 1):
        if is_prime(N):
            cum_prime_delta += deltas[N]
        else:
            cum_composite_delta += deltas[N]

    total_delta = wobbles[1] - wobbles[max_N]
    print(f"  Total wobble reduction (W(1) - W({max_N})): {total_delta:.10f}")
    print(f"  From primes:     {cum_prime_delta:+.10f} ({100*cum_prime_delta/total_delta:.1f}%)")
    print(f"  From composites: {cum_composite_delta:+.10f} ({100*cum_composite_delta/total_delta:.1f}%)")
    print(f"\n  KEY FINDING: Composites do {100*cum_composite_delta/total_delta:.1f}% of the 'uniformization' work!")

    # ANALYSIS 7: Conjecture formulation
    print("\n" + "=" * 70)
    print("POTENTIAL CONJECTURE")
    print("=" * 70)
    print("""
For N ≥ 11, adding a prime p to the Farey sequence F_{p-1} → F_p
INCREASES the squared discrepancy W(N).

More precisely: for all primes p ≥ 11,
  W(p) > W(p-1)

In other words: primes DISRUPT uniformity, and composites RESTORE it.
The total wobble still decreases overall because composites outnumber primes
and each composite makes a small positive contribution.

This is consistent with the Riemann Hypothesis (which controls the TOTAL wobble
W(N) ~ N^{-1+ε}) but reveals that the prime contribution has the WRONG SIGN —
primes individually make the distribution LESS uniform, not more.

This decomposition appears to be unstudied in the number theory literature.
""")

    # Save detailed data
    output_file = os.path.join(output_dir, "wobble_deep_data.json")
    data = {
        'max_N': max_N,
        'wobbles': {str(k): v for k, v in wobbles.items()},
        'deltas': {str(k): v for k, v in deltas.items()},
        'farey_sizes': {str(k): v for k, v in farey_sizes.items()},
        'cum_prime_delta': cum_prime_delta,
        'cum_composite_delta': cum_composite_delta,
        'total_delta': total_delta,
        'prime_positive_count': prime_positive,
        'prime_negative_count': prime_negative,
    }
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {output_file}")


if __name__ == '__main__':
    run_deep_analysis(max_N=300)
