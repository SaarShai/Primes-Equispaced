#!/usr/bin/env python3
"""
NON-HEALING COMPOSITES: Deep Investigation
=============================================

Q1: WHY do prime squares (121=11^2, 169=13^2) not heal?
     What do 94=2*47, 146=2*73, 166=2*83 have in common?
     Can we PREDICT which composites won't heal?

Q2: WHY are primorials least disruptive?
     Is it just about phi(N)/N being small, or something deeper?

Q3: Can we prove the 96% healing rate analytically?
     What's the rate for composites up to 1000, 10000?
     Does it converge to a specific limit?

Uses exact Fraction arithmetic to avoid rounding errors.
"""

from fractions import Fraction
from math import gcd, log, prod
from collections import defaultdict
import time
import sys
import os

# ============================================================
# UTILITIES
# ============================================================

def euler_phi(n):
    result = n
    temp = n
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True


def is_prime_power(n):
    """Check if n = p^k for prime p and k >= 2."""
    factors = factorize(n)
    return len(factors) == 1 and list(factors.values())[0] >= 2


def is_semiprime_2p(n):
    """Check if n = 2 * prime."""
    return n % 2 == 0 and is_prime(n // 2)


def largest_prime_factor(n):
    lpf = 1
    d = 2
    while d * d <= n:
        while n % d == 0:
            lpf = d
            n //= d
        d += 1
    if n > 1:
        lpf = n
    return lpf


def smallest_prime_factor(n):
    if n < 2: return n
    if n % 2 == 0: return 2
    d = 3
    while d * d <= n:
        if n % d == 0: return d
        d += 2
    return n


def num_distinct_prime_factors(n):
    return len(factorize(n))


def classify(n):
    """Human-readable classification."""
    factors = factorize(n)
    parts = []
    for p in sorted(factors):
        if factors[p] == 1:
            parts.append(str(p))
        else:
            parts.append(f"{p}^{factors[p]}")
    return " * ".join(parts)


def primorial(k):
    """Product of first k primes."""
    primes = []
    n = 2
    while len(primes) < k:
        if is_prime(n):
            primes.append(n)
        n += 1
    return prod(primes)


# ============================================================
# FAST WOBBLE COMPUTATION (float, using numpy for speed)
# ============================================================

import numpy as np

def compute_wobble_float(sorted_fracs):
    """W = sum (f_j - j/(n-1))^2"""
    n = len(sorted_fracs)
    if n <= 1:
        return 0.0
    ideal = np.linspace(0, 1, n)
    deltas = sorted_fracs - ideal
    return float(np.dot(deltas, deltas))


def compute_all_wobbles(max_N):
    """Compute W(N) for all N from 1 to max_N using incremental Farey build."""
    print(f"  Computing wobbles up to N={max_N}...")
    frac_set = {0.0, 1.0}
    wobbles = np.zeros(max_N + 1)
    wobbles[1] = compute_wobble_float(np.array([0.0, 1.0]))

    t0 = time.time()
    for N in range(2, max_N + 1):
        # Add new fractions with denominator N
        for a in range(1, N):
            if gcd(a, N) == 1:
                frac_set.add(a / N)

        sorted_arr = np.array(sorted(frac_set))
        wobbles[N] = compute_wobble_float(sorted_arr)

        if N % 100 == 0:
            elapsed = time.time() - t0
            rate = N / elapsed if elapsed > 0 else 0
            print(f"    N={N:5d}  |F|={len(sorted_arr):7d}  W={wobbles[N]:.10f}  [{elapsed:.1f}s]")

    print(f"  Done in {time.time() - t0:.1f}s")
    return wobbles


# ============================================================
# Q1: NON-HEALING COMPOSITES
# ============================================================

def investigate_nonhealing(max_N=500):
    """Find and classify all non-healing composites up to max_N."""
    print("\n" + "=" * 70)
    print(f"Q1: NON-HEALING COMPOSITES UP TO N={max_N}")
    print("=" * 70)

    wobbles = compute_all_wobbles(max_N)

    # Find non-healing composites: W(N) >= W(N-1) and N is composite
    nonhealing = []
    all_composites = []
    healing = []

    for N in range(4, max_N + 1):
        if is_prime(N):
            continue
        delta = wobbles[N - 1] - wobbles[N]  # positive = healing
        phi_N = euler_phi(N)
        phi_ratio = phi_N / N
        factors = factorize(N)
        lpf = largest_prime_factor(N)
        spf = smallest_prime_factor(N)
        omega = len(factors)  # distinct prime factors
        bigOmega = sum(factors.values())  # total prime factors with multiplicity

        entry = {
            'N': N,
            'delta': delta,
            'heals': delta > 0,
            'factorization': classify(N),
            'phi': phi_N,
            'phi_ratio': phi_ratio,
            'lpf': lpf,
            'spf': spf,
            'omega': omega,
            'bigOmega': bigOmega,
            'is_prime_sq': is_prime_power(N) and bigOmega == 2,
            'is_2p': is_semiprime_2p(N),
            'W_N': wobbles[N],
            'W_prev': wobbles[N - 1],
            'lpf_over_N': lpf / N,
        }
        all_composites.append(entry)

        if delta <= 0:
            nonhealing.append(entry)
        else:
            healing.append(entry)

    total_comp = len(all_composites)
    total_nh = len(nonhealing)
    heal_rate = len(healing) / total_comp * 100

    print(f"\n  Total composites in [4, {max_N}]: {total_comp}")
    print(f"  Healing composites:     {len(healing)} ({heal_rate:.1f}%)")
    print(f"  Non-healing composites: {total_nh} ({100 - heal_rate:.1f}%)")

    print(f"\n  ALL NON-HEALING COMPOSITES:")
    print(f"  {'N':>5s}  {'Factorization':<20s}  {'phi/N':>6s}  {'LPF':>4s}  {'LPF/N':>6s}  {'omega':>5s}  {'deltaW':>12s}  {'Type'}")
    print(f"  {'-'*5}  {'-'*20}  {'-'*6}  {'-'*4}  {'-'*6}  {'-'*5}  {'-'*12}  {'-'*20}")

    for e in nonhealing:
        typ = ""
        if e['is_prime_sq']:
            typ = "PRIME SQUARE"
        elif e['is_2p']:
            typ = f"2 * prime({e['N']//2})"
        elif e['omega'] == 1:
            typ = f"PRIME POWER"
        else:
            typ = f"composite"
        print(f"  {e['N']:>5d}  {e['factorization']:<20s}  {e['phi_ratio']:>6.3f}  {e['lpf']:>4d}  {e['lpf_over_N']:>6.3f}  {e['omega']:>5d}  {e['delta']:>12.2e}  {typ}")

    # ---- PATTERN ANALYSIS ----
    print(f"\n  PATTERN ANALYSIS:")

    # Check: are all non-healing N such that LPF/N is large?
    nh_lpf_ratios = [e['lpf_over_N'] for e in nonhealing]
    h_lpf_ratios = [e['lpf_over_N'] for e in healing]
    print(f"\n  LPF/N for non-healing: min={min(nh_lpf_ratios):.3f}  max={max(nh_lpf_ratios):.3f}  mean={np.mean(nh_lpf_ratios):.3f}")
    print(f"  LPF/N for healing:     min={min(h_lpf_ratios):.3f}  max={max(h_lpf_ratios):.3f}  mean={np.mean(h_lpf_ratios):.3f}")

    # Check: phi/N
    nh_phi = [e['phi_ratio'] for e in nonhealing]
    h_phi = [e['phi_ratio'] for e in healing]
    print(f"\n  phi/N for non-healing:  min={min(nh_phi):.3f}  max={max(nh_phi):.3f}  mean={np.mean(nh_phi):.3f}")
    print(f"  phi/N for healing:      min={min(h_phi):.3f}  max={max(h_phi):.3f}  mean={np.mean(h_phi):.3f}")

    # Check: omega (distinct prime factors)
    nh_omega = [e['omega'] for e in nonhealing]
    h_omega = [e['omega'] for e in healing]
    print(f"\n  omega for non-healing:  min={min(nh_omega)}  max={max(nh_omega)}  mean={np.mean(nh_omega):.2f}")
    print(f"  omega for healing:      min={min(h_omega)}  max={max(h_omega)}  mean={np.mean(h_omega):.2f}")

    # Classify non-healing by type
    type_counts = defaultdict(list)
    for e in nonhealing:
        if e['is_prime_sq']:
            type_counts['prime_square'].append(e['N'])
        elif e['is_2p']:
            type_counts['2*large_prime'].append(e['N'])
        elif e['omega'] == 1:
            type_counts['prime_power'].append(e['N'])
        elif e['omega'] == 2 and e['spf'] == 2:
            type_counts['2*composite'].append(e['N'])
        else:
            type_counts['other'].append(e['N'])

    print(f"\n  NON-HEALING BY TYPE:")
    for typ, vals in sorted(type_counts.items()):
        print(f"    {typ}: {vals}")

    # KEY HYPOTHESIS: non-healing happens when N has few NEW fractions
    # relative to the size of F_{N-1}, AND the largest prime factor is close to N
    print(f"\n  KEY OBSERVATION: LPF/N ratio")
    print(f"  For 2*p composites that DON'T heal: LPF = p = N/2, so LPF/N = 0.500")
    print(f"  For prime squares p^2: LPF = p = sqrt(N), so LPF/N = 1/sqrt(N)")

    # Check: do all composites with LPF/N >= some threshold fail to heal?
    for threshold in [0.45, 0.40, 0.35, 0.30]:
        high_lpf = [e for e in all_composites if e['lpf_over_N'] >= threshold]
        high_lpf_nh = [e for e in high_lpf if not e['heals']]
        if high_lpf:
            print(f"    LPF/N >= {threshold}: {len(high_lpf)} composites, {len(high_lpf_nh)} non-healing ({100*len(high_lpf_nh)/len(high_lpf):.1f}%)")

    # Deeper: among 2*p semiprimes, which ones DON'T heal?
    semiprimes_2p = [e for e in all_composites if e['is_2p']]
    sp_nh = [e for e in semiprimes_2p if not e['heals']]
    sp_h = [e for e in semiprimes_2p if e['heals']]
    print(f"\n  SEMIPRIMES 2*p (p prime):")
    print(f"    Total: {len(semiprimes_2p)}")
    print(f"    Non-healing: {[e['N'] for e in sp_nh]}")
    print(f"    Healing: {[e['N'] for e in sp_h[:20]]}...")

    if sp_nh:
        print(f"\n    Non-healing 2p have p = {[e['N']//2 for e in sp_nh]}")
        print(f"    These primes are: {[classify(e['N']//2) for e in sp_nh]}")

    # Among prime squares
    prime_sqs = [e for e in all_composites if e['is_prime_sq']]
    psq_nh = [e for e in prime_sqs if not e['heals']]
    psq_h = [e for e in prime_sqs if e['heals']]
    print(f"\n  PRIME SQUARES p^2:")
    print(f"    Total: {len(prime_sqs)}")
    print(f"    Non-healing: {[e['N'] for e in psq_nh]} = {[classify(e['N']) for e in psq_nh]}")
    print(f"    Healing:     {[e['N'] for e in psq_h]} = {[classify(e['N']) for e in psq_h]}")

    # What makes p^2 heal vs not heal?
    if psq_nh and psq_h:
        nh_ratios = [f"{e['phi_ratio']:.3f}" for e in psq_nh]
        h_ratios = [f"{e['phi_ratio']:.3f}" for e in psq_h]
        print(f"\n    Non-healing p^2: phi/N = {nh_ratios}")
        print(f"    Healing p^2:     phi/N = {h_ratios}")

    # Look at delta_W / W(N-1) ratio -- relative disruption
    print(f"\n  RELATIVE DISRUPTION (deltaW / W(N-1)):")
    for e in nonhealing:
        rel = e['delta'] / e['W_prev'] if e['W_prev'] != 0 else 0
        print(f"    N={e['N']:>5d}  deltaW/W = {rel:>10.6f}  ({e['factorization']})")

    return wobbles, nonhealing, all_composites


# ============================================================
# Q2: PRIMORIAL ANALYSIS
# ============================================================

def investigate_primorials(wobbles, max_N):
    """Analyze why primorials are least disruptive."""
    print("\n\n" + "=" * 70)
    print("Q2: WHY ARE PRIMORIALS LEAST DISRUPTIVE?")
    print("=" * 70)

    # First few primorials: 2, 6, 30, 210, ...
    primorials = []
    n = 1
    while True:
        p = primorial(n)
        if p > max_N:
            break
        primorials.append(p)
        n += 1

    print(f"\n  Primorials up to {max_N}: {primorials}")

    # For each primorial, compute its wobble statistics
    print(f"\n  {'Primorial':>10s}  {'Factorize':<15s}  {'phi/N':>6s}  {'W(N)':>12s}  {'W(N-1)':>12s}  {'deltaW':>12s}  {'deltaW/W':>10s}")
    print(f"  {'-'*10}  {'-'*15}  {'-'*6}  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*10}")

    for p in primorials:
        if p >= len(wobbles):
            continue
        phi = euler_phi(p)
        delta = wobbles[p - 1] - wobbles[p]
        rel = delta / wobbles[p - 1] if wobbles[p - 1] > 0 else 0
        print(f"  {p:>10d}  {classify(p):<15s}  {phi/p:>6.3f}  {wobbles[p]:>12.6e}  {wobbles[p-1]:>12.6e}  {delta:>12.6e}  {rel:>10.6f}")

    # Compare primorials to other numbers with similar phi/N
    print(f"\n  COMPARISON: primorials vs non-primorials with similar phi/N")
    for prim in primorials:
        if prim >= len(wobbles) or prim < 6:
            continue
        phi_ratio_prim = euler_phi(prim) / prim
        delta_prim = wobbles[prim - 1] - wobbles[prim]

        # Find composites near prim with similar phi/N
        nearby = []
        for N in range(max(4, prim - 20), min(len(wobbles), prim + 20)):
            if N == prim or is_prime(N):
                continue
            pr = euler_phi(N) / N
            if abs(pr - phi_ratio_prim) < 0.05:
                delta_N = wobbles[N - 1] - wobbles[N]
                nearby.append((N, pr, delta_N, classify(N)))

        if nearby:
            print(f"\n    Primorial {prim} (phi/N={phi_ratio_prim:.3f}, deltaW={delta_prim:.6e}):")
            for N, pr, dw, cl in nearby:
                marker = "***" if dw < delta_prim else ""
                print(f"      N={N:>5d}  phi/N={pr:.3f}  deltaW={dw:.6e}  [{cl}] {marker}")

    # Compare healing magnitude: for each composite, rank by deltaW/W
    all_deltas = []
    for N in range(4, len(wobbles)):
        if is_prime(N):
            continue
        if wobbles[N - 1] == 0:
            continue
        delta = wobbles[N - 1] - wobbles[N]
        rel = delta / wobbles[N - 1]
        all_deltas.append((N, delta, rel, euler_phi(N) / N, classify(N)))

    # Sort by relative delta (most healing first)
    all_deltas.sort(key=lambda x: -x[2])

    print(f"\n  TOP 20 MOST HEALING COMPOSITES (by deltaW/W):")
    print(f"  {'Rank':>4s}  {'N':>5s}  {'Factorize':<20s}  {'phi/N':>6s}  {'deltaW/W':>10s}")
    for i, (N, delta, rel, pr, cl) in enumerate(all_deltas[:20]):
        is_prim = "<<< PRIMORIAL" if N in primorials else ""
        print(f"  {i+1:>4d}  {N:>5d}  {cl:<20s}  {pr:>6.3f}  {rel:>10.6f}  {is_prim}")

    # Where do primorials rank?
    for prim in primorials:
        if prim >= len(wobbles):
            continue
        rank = next((i+1 for i, (N, *_) in enumerate(all_deltas) if N == prim), None)
        if rank is not None:
            print(f"\n    Primorial {prim} rank: #{rank} out of {len(all_deltas)} composites")

    # HYPOTHESIS: among all N with the same set of prime factors, primorials minimize deltaW
    # because they have exponent 1 for each prime (no repeated factors)
    print(f"\n  HYPOTHESIS: primorials = product of distinct primes, no repeats")
    print(f"  Compare p1*p2*...*pk vs p1^a1 * p2^a2 with same primes:")

    # Compare 2*3=6 vs 2^2*3=12 vs 2*3^2=18 vs 2^2*3^2=36
    test_groups = [
        ("Primes {2,3}", [6, 12, 18, 36]),
        ("Primes {2,3,5}", [30, 60, 90, 120, 150, 180]),
        ("Primes {2,5}", [10, 20, 50, 100]),
        ("Primes {2,7}", [14, 28, 56, 98]),
    ]

    for label, group in test_groups:
        print(f"\n    {label}:")
        for N in group:
            if N >= len(wobbles):
                continue
            delta = wobbles[N - 1] - wobbles[N]
            rel = delta / wobbles[N - 1] if wobbles[N - 1] > 0 else 0
            is_prim = " <<< PRIMORIAL" if N in primorials else ""
            print(f"      N={N:>4d}  {classify(N):<15s}  phi/N={euler_phi(N)/N:.3f}  deltaW/W={rel:.6f}{is_prim}")


# ============================================================
# Q3: HEALING RATE CONVERGENCE
# ============================================================

def investigate_healing_rate(wobbles):
    """Track healing rate as N grows. Does 96% converge?"""
    max_N = len(wobbles) - 1

    print("\n\n" + "=" * 70)
    print("Q3: HEALING RATE CONVERGENCE")
    print("=" * 70)

    # Compute healing rate in windows
    windows = []
    running_comp = 0
    running_heal = 0

    print(f"\n  {'Range':<15s}  {'Composites':>10s}  {'Healing':>8s}  {'Rate':>7s}  {'Cumulative':>10s}")
    print(f"  {'-'*15}  {'-'*10}  {'-'*8}  {'-'*7}  {'-'*10}")

    window_size = 50 if max_N <= 500 else 100
    for lo in range(4, max_N + 1, window_size):
        hi = min(lo + window_size - 1, max_N)
        comp_count = 0
        heal_count = 0
        for N in range(lo, hi + 1):
            if is_prime(N):
                continue
            comp_count += 1
            delta = wobbles[N - 1] - wobbles[N]
            if delta > 0:
                heal_count += 1

        running_comp += comp_count
        running_heal += heal_count
        rate = heal_count / comp_count * 100 if comp_count > 0 else 0
        cum_rate = running_heal / running_comp * 100 if running_comp > 0 else 0
        windows.append((lo, hi, comp_count, heal_count, rate, cum_rate))
        print(f"  [{lo:>5d},{hi:>5d}]  {comp_count:>10d}  {heal_count:>8d}  {rate:>6.1f}%  {cum_rate:>9.1f}%")

    print(f"\n  OVERALL: {running_heal}/{running_comp} composites heal = {running_heal/running_comp*100:.2f}%")

    # Non-healing rate by number of distinct prime factors
    print(f"\n  NON-HEALING RATE BY omega (# distinct prime factors):")
    omega_stats = defaultdict(lambda: [0, 0])  # [total, nonhealing]
    for N in range(4, max_N + 1):
        if is_prime(N):
            continue
        omega = num_distinct_prime_factors(N)
        omega_stats[omega][0] += 1
        delta = wobbles[N - 1] - wobbles[N]
        if delta <= 0:
            omega_stats[omega][1] += 1

    for omega in sorted(omega_stats):
        total, nh = omega_stats[omega]
        print(f"    omega={omega}: {total:>5d} composites, {nh:>4d} non-healing ({100*nh/total:.1f}%)")

    # Non-healing rate by phi/N bucket
    print(f"\n  NON-HEALING RATE BY phi/N BUCKET:")
    phi_buckets = defaultdict(lambda: [0, 0])
    for N in range(4, max_N + 1):
        if is_prime(N):
            continue
        pr = euler_phi(N) / N
        bucket = round(pr * 10) / 10  # bucket to nearest 0.1
        phi_buckets[bucket][0] += 1
        delta = wobbles[N - 1] - wobbles[N]
        if delta <= 0:
            phi_buckets[bucket][1] += 1

    for bucket in sorted(phi_buckets):
        total, nh = phi_buckets[bucket]
        if total >= 3:
            print(f"    phi/N ~ {bucket:.1f}: {total:>5d} composites, {nh:>4d} non-healing ({100*nh/total:.1f}%)")

    # Non-healing rate by LPF/N bucket
    print(f"\n  NON-HEALING RATE BY LPF/N BUCKET:")
    lpf_buckets = defaultdict(lambda: [0, 0])
    for N in range(4, max_N + 1):
        if is_prime(N):
            continue
        lpf = largest_prime_factor(N)
        ratio = lpf / N
        bucket = round(ratio * 10) / 10
        lpf_buckets[bucket][0] += 1
        delta = wobbles[N - 1] - wobbles[N]
        if delta <= 0:
            lpf_buckets[bucket][1] += 1

    for bucket in sorted(lpf_buckets):
        total, nh = lpf_buckets[bucket]
        if total >= 2:
            print(f"    LPF/N ~ {bucket:.1f}: {total:>5d} composites, {nh:>4d} non-healing ({100*nh/total:.1f}%)")

    # PREDICTIVE MODEL: can we predict non-healing?
    print(f"\n  PREDICTIVE MODEL TEST:")
    print(f"  Hypothesis: N is non-healing iff omega(N)=1 or (omega(N)=2 and LPF/N > threshold)")

    # Test different thresholds
    for threshold in [0.40, 0.42, 0.44, 0.46, 0.48, 0.50]:
        tp, fp, fn, tn = 0, 0, 0, 0
        for N in range(4, max_N + 1):
            if is_prime(N):
                continue
            omega = num_distinct_prime_factors(N)
            lpf = largest_prime_factor(N)
            lpf_ratio = lpf / N
            delta = wobbles[N - 1] - wobbles[N]
            actual_nh = delta <= 0

            # Predict: non-healing if omega <= 1 (prime power) or (omega=2 and lpf/N > threshold)
            predicted_nh = (omega == 1) or (omega == 2 and lpf_ratio >= threshold)

            if predicted_nh and actual_nh:
                tp += 1
            elif predicted_nh and not actual_nh:
                fp += 1
            elif not predicted_nh and actual_nh:
                fn += 1
            else:
                tn += 1

        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        accuracy = (tp + tn) / (tp + fp + fn + tn)
        print(f"    threshold={threshold:.2f}: TP={tp} FP={fp} FN={fn} TN={tn}  precision={precision:.2f} recall={recall:.2f} accuracy={accuracy:.3f}")
        if fn > 0:
            # Show false negatives (non-healing that we didn't predict)
            for N in range(4, max_N + 1):
                if is_prime(N): continue
                omega = num_distinct_prime_factors(N)
                lpf = largest_prime_factor(N)
                lpf_ratio = lpf / N
                delta = wobbles[N - 1] - wobbles[N]
                actual_nh = delta <= 0
                predicted_nh = (omega == 1) or (omega == 2 and lpf_ratio >= threshold)
                if not predicted_nh and actual_nh:
                    print(f"      MISSED: N={N} = {classify(N)}, omega={omega}, LPF/N={lpf_ratio:.3f}")


# ============================================================
# DEEP DIVE: WHY specific composites fail
# ============================================================

def deep_dive_nonhealing(wobbles, nonhealing_list):
    """For each non-healing composite, analyze the Farey gap structure."""
    print("\n\n" + "=" * 70)
    print("DEEP DIVE: Mechanism of Non-Healing")
    print("=" * 70)

    print(f"\n  When a composite N is inserted into F_{{N-1}}:")
    print(f"  - phi(N) new fractions are added")
    print(f"  - Each goes into a gap of F_{{N-1}} (injection principle)")
    print(f"  - Healing happens when new fractions REDUCE the overall displacement")
    print(f"  - Non-healing: new fractions land where they INCREASE displacement")

    print(f"\n  For N = p^2 (prime square):")
    print(f"  - phi(p^2) = p(p-1) new fractions")
    print(f"  - But many fractions with denom p already exist!")
    print(f"  - New fractions cluster near existing p-fractions")
    print(f"  - This creates LOCAL over-density without fixing the gaps")

    print(f"\n  For N = 2p (twice a large prime):")
    print(f"  - phi(2p) = p-1 new fractions (half are from odd numerators)")
    print(f"  - The fractions a/(2p) with odd a and gcd(a,2p)=1")
    print(f"  - These all have large denominator but cluster near a/2p ~ a/(2p)")
    print(f"  - When p is large relative to N, the fractions are too few to heal")

    # For small non-healing composites, show the actual gap structure
    small_nh = [e for e in nonhealing_list if e['N'] <= 200]
    for entry in small_nh[:6]:
        N = entry['N']
        print(f"\n  --- N = {N} = {entry['factorization']} ---")
        print(f"  phi({N}) = {entry['phi']}, phi/N = {entry['phi_ratio']:.3f}")

        # Compute F_{N-1} and F_N
        frac_prev = set()
        for d in range(1, N):
            for a in range(0, d + 1):
                if gcd(a, d) == 1:
                    frac_prev.add(a / d)
        frac_prev = sorted(frac_prev)

        # New fractions
        new_fracs = sorted([a / N for a in range(1, N) if gcd(a, N) == 1])
        print(f"  |F_{{N-1}}| = {len(frac_prev)}, new fracs = {len(new_fracs)}")

        # Fill fraction
        fill = len(new_fracs) / (len(frac_prev) - 1)
        print(f"  Fill fraction: {len(new_fracs)}/{len(frac_prev)-1} = {fill:.4f}")

        # Show distribution of new fractions across the unit interval
        # Divide [0,1] into 10 bins
        bins = [0] * 10
        for f in new_fracs:
            b = min(int(f * 10), 9)
            bins[b] += 1
        print(f"  New frac distribution across [0,1] (10 bins): {bins}")


# ============================================================
# MAIN
# ============================================================

def main():
    max_N = 500
    if len(sys.argv) > 1:
        max_N = int(sys.argv[1])

    print("NON-HEALING COMPOSITES: Deep Investigation")
    print("=" * 70)
    print(f"Computing up to N = {max_N}")

    t0 = time.time()

    # Q1: Find and classify all non-healing composites
    wobbles, nonhealing, all_composites = investigate_nonhealing(max_N)

    # Q2: Why primorials are special
    investigate_primorials(wobbles, max_N)

    # Q3: Healing rate convergence
    investigate_healing_rate(wobbles)

    # Deep dive into mechanisms
    deep_dive_nonhealing(wobbles, nonhealing)

    total_time = time.time() - t0
    print(f"\n\n{'=' * 70}")
    print(f"Total computation time: {total_time:.1f}s")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
