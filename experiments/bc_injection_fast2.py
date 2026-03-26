#!/usr/bin/env python3
"""
BC + INJECTION ANALYSIS (FIXED)
=================================

Fixed version of bc_injection_fast.py.
Key bugs fixed:
  1. Farey generator: append BEFORE update (was skipping 1/N and adding 11/10)
  2. delta(1/1) = 0 (special case for terminal fraction)

Computes for all primes p in [11, P_max]:
  - B+C = (B_raw + delta_sq) / n'^2 > 0?
  - Full margin = new_D_sq + B_raw + delta_sq - dilution_raw > 0?
  - R = B_raw / delta_sq (should have 1+R > 0)
"""

import time
from math import gcd, isqrt, log, pi

start_time = time.time()


def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi


def analyze_prime(p, phi_arr):
    """Full analysis for a single prime p."""
    N = p - 1

    # ---- FIXED Farey generator: append BEFORE updating ----
    fracs = []
    D_dict = {}
    a0, b0, c0, d0 = 0, 1, 1, N
    fracs.append((0, 1))
    while c0 <= N:
        fracs.append((c0, d0))        # FIX: append current BEFORE computing next
        k = (N + b0) // d0
        a0, b0, c0, d0 = c0, d0, k * c0 - a0, k * d0 - b0

    n = len(fracs)
    n_prime = n + p - 1

    # ---- Compute D(a/b) and delta(a/b) ----
    D_vals = []
    delta_vals = []
    old_D_sq = 0.0
    delta_sq = 0.0
    B_raw_half = 0.0

    for j, (a, b) in enumerate(fracs):
        D = j - n * a / b
        D_dict[(a, b)] = D

        # FIX: delta(1/1) = 0 (terminal fraction: all p-1 new fracs are below 1)
        if b == 1 and a == 1:
            delta = 0.0
        else:
            sigma = (p * a) % b
            delta = (a - sigma) / b

        D_vals.append(D)
        delta_vals.append(delta)

        old_D_sq += D * D
        delta_sq += delta * delta
        B_raw_half += D * delta

    B_raw = 2 * B_raw_half
    n_prime_sq = n_prime * n_prime
    n_sq = n * n
    dilution_raw = old_D_sq * (n_prime_sq - n_sq) / n_sq

    # ---- Injection principle: compute new_D_sq ----
    # For each k in {1,...,p-1}:
    #   b = k^{-1} mod p
    #   a = (k*b - 1)//p  (numerator of left Farey neighbor)
    #   c = 1 - n/(p*b)
    #   D_p(k/p) = D_old(a/b) + c + k/p
    new_D_sq = 0.0
    TERM_A = 0.0
    TERM_C_inj = 0.0

    for k in range(1, p):
        b = pow(k, p - 2, p)      # k^{-1} mod p
        a = (k * b - 1) // p      # numerator of left Farey neighbor

        D_j = D_dict.get((a, b), 0.0)
        c = 1.0 - n / (p * b)
        kp = k / p
        corr = c + kp
        D_p_kp = D_j + corr

        new_D_sq += D_p_kp * D_p_kp
        TERM_A += D_j * D_j
        TERM_C_inj += corr * corr

    margin = new_D_sq + B_raw + delta_sq - dilution_raw

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'delta_sq': delta_sq,
        'B_raw': B_raw,
        'new_D_sq': new_D_sq,
        'dilution_raw': dilution_raw,
        'TERM_A': TERM_A,
        'TERM_C_inj': TERM_C_inj,
        'margin': margin,
        'BC_sum': B_raw + delta_sq,
        'R': B_raw / delta_sq if delta_sq > 0 else float('inf'),
        'DA': new_D_sq / dilution_raw if dilution_raw > 0 else 0,
        'CA': delta_sq / dilution_raw if dilution_raw > 0 else 0,
        'TC_r': TERM_C_inj / dilution_raw if dilution_raw > 0 else 0,
        'TA_r': TERM_A / dilution_raw if dilution_raw > 0 else 0,
        'pW': p * old_D_sq / (n * n),
    }


def main():
    LIMIT = 3000
    print("BC + INJECTION ANALYSIS (FIXED)")
    print(f"Primes p in [11, {LIMIT}]")
    print("=" * 80)

    phi_arr = euler_totient_sieve(LIMIT)
    primes = [p for p in sieve_primes(LIMIT) if p >= 11]
    print(f"  Testing {len(primes)} primes")
    print()

    print(f"{'p':>5} {'R':>9} {'1+R':>7} {'DA':>7} {'CA':>7} "
          f"{'TC_r':>7} {'TA_r':>7} {'margin_r':>9}")
    print("-" * 75)

    all_data = []
    violations_BC = []
    violations_margin = []
    min_1pR = float('inf')
    min_1pR_p = 0
    min_margin_r = float('inf')
    min_margin_r_p = 0

    for i, p in enumerate(primes):
        r = analyze_prime(p, phi_arr)
        all_data.append(r)

        one_pR = 1 + r['R']
        margin_r = r['margin'] / r['dilution_raw'] if r['dilution_raw'] > 0 else 0

        if one_pR < min_1pR:
            min_1pR = one_pR
            min_1pR_p = p
        if margin_r < min_margin_r:
            min_margin_r = margin_r
            min_margin_r_p = p

        if one_pR <= 0:
            violations_BC.append(r)
        if margin_r <= 0:
            violations_margin.append(r)

        should_print = (i < 25 or i % 60 == 0 or i == len(primes) - 1 or
                        one_pR < 0.4 or margin_r < 0.05)
        if should_print:
            print(f"{p:5d} {r['R']:9.4f} {one_pR:7.4f} {r['DA']:7.4f} {r['CA']:7.4f} "
                  f"{r['TC_r']:7.4f} {r['TA_r']:7.4f} {margin_r:9.4f}")

        if i > 0 and i % 100 == 0:
            elapsed = time.time() - start_time
            print(f"  ... [{elapsed:.1f}s] {i}/{len(primes)}, min(1+R)={min_1pR:.4f}")

    elapsed = time.time() - start_time
    print()
    print("=" * 80)
    print(f"RESULTS [{elapsed:.1f}s]")
    print("=" * 80)
    print(f"  Primes tested: {len(primes)}")
    print(f"  B+C > 0 violations (1+R<=0):    {len(violations_BC)}")
    if violations_BC:
        for v in violations_BC[:8]:
            print(f"    p={v['p']}: 1+R={1+v['R']:.6f}")
    print(f"  Full margin violations (<=0):    {len(violations_margin)}")
    if violations_margin:
        for v in violations_margin[:5]:
            print(f"    p={v['p']}: margin_r={v['margin']/v['dilution_raw']:.6f}")

    print(f"\n  min(1+R):     {min_1pR:.6f} at p = {min_1pR_p}")
    print(f"  min(margin_r): {min_margin_r:.6f} at p = {min_margin_r_p}")

    # Worst cases
    worst = sorted(all_data, key=lambda x: 1 + x['R'])[:12]
    print()
    print("WORST-CASE PRIMES (smallest 1+R):")
    print(f"{'rank':>4} {'p':>5} {'1+R':>8} {'R':>9} {'B_raw':>12} {'dlt_sq':>12}")
    for i, r in enumerate(worst):
        print(f"{i+1:4d} {r['p']:5d} {1+r['R']:8.5f} {r['R']:9.4f} "
              f"{r['B_raw']:12.3f} {r['delta_sq']:12.3f}")

    # Asymptotic trends
    print()
    print("ASYMPTOTIC TRENDS:")
    ranges = [(11, 100), (100, 500), (500, 1000), (1000, 2000), (2000, 3000)]
    print(f"{'range':>15} {'min(1+R)':>9} {'avg(1+R)':>9} {'min(marg)':>10} "
          f"{'avg(DA)':>8} {'avg(CA)':>8}")
    for lo, hi in ranges:
        sub = [r for r in all_data if lo <= r['p'] <= hi]
        if not sub:
            continue
        oneRs = [1 + r['R'] for r in sub]
        margs = [r['margin'] / r['dilution_raw'] for r in sub if r['dilution_raw'] > 0]
        DAs = [r['DA'] for r in sub]
        CAs = [r['CA'] for r in sub]
        print(f"  [{lo:5d},{hi:5d}] {min(oneRs):9.5f} {sum(oneRs)/len(oneRs):9.5f} "
              f"{min(margs):10.5f} {sum(DAs)/len(DAs):8.5f} {sum(CAs)/len(CAs):8.5f}")

    print()
    print("PROOF CONCLUSIONS:")
    if not violations_BC:
        print(f"  VERIFIED: B+C > 0 for all {len(primes)} primes in [11, {primes[-1]}]")
    if not violations_margin:
        print(f"  VERIFIED: Full condition ## for all {len(primes)} primes in [11, {primes[-1]}]")
    print(f"  min(1+R) = {min_1pR:.6f} at p={min_1pR_p}")
    print(f"  min(margin/dil) = {min_margin_r:.6f} at p={min_margin_r_p}")

    print(f"\nTotal: {time.time()-start_time:.1f}s")


if __name__ == '__main__':
    main()
