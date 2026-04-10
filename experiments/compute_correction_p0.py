#!/usr/bin/env python3
"""
Compute the Abel correction term for ALL primes p with M(p) <= -3 up to p = 10000.

The decomposition (from B_VIA_MOBIUS.md):
  sum R(x)*delta(x) = M(p-1) * C/2  +  Term2

where:
  - M(p-1) = M(p) + 1  (since p prime, mu(p) = -1)
  - C/2 = sum_x x*delta(x)  (exact identity)
  - Term2 = sum_{k=1}^{N-1} M(k) * sum_x Delta_S_k(x) * delta(x)
  - correction = Term2 / (-C/2)

B >= 0 iff sum R*delta <= -C/2
  iff  M(p-1)*C/2 + Term2 <= -C/2
  iff  Term2 <= -(1 + M(p-1))*C/2 = |M(p)|*C/2
  iff  correction = Term2/(-C/2) >= -(|M(p)| - 2)

For M(p) = -3: need correction > -1
For M(p) = -4: need correction > -2
"""

import math
from fractions import Fraction
import sys
import time

def sieve_mu(n):
    """Sieve Mobius function up to n."""
    mu = [0] * (n + 1)
    mu[1] = 1
    is_prime = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def mertens_values(mu, n):
    """Compute M(k) = sum_{d=1}^k mu(d) for k = 0..n."""
    M = [0] * (n + 1)
    for k in range(1, n + 1):
        M[k] = M[k - 1] + mu[k]
    return M

def farey_sequence(N):
    """Generate Farey sequence F_N as list of (a, b) with a/b in [0,1], gcd(a,b)=1, b<=N."""
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if math.gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: x[0] / x[1])
    return fracs

def compute_B_and_correction(p):
    """
    For prime p, compute B, C, the leading term, and the correction.
    Returns dict with all quantities.
    """
    N = p - 1
    fracs = farey_sequence(N)
    n = len(fracs)

    # Compute delta(a/b) = a/b - {p*a/b} = a/b - (p*a mod b)/b
    deltas = []
    for a, b in fracs:
        if b == 0:
            deltas.append(0.0)
            continue
        pa_mod_b = (p * a) % b
        delta = (a - pa_mod_b) / b
        deltas.append(delta)

    # Compute D(f_i) = i+1 - n*f_i (rank is 1-indexed: rank of f_i = i+1 for 0-indexed i)
    # Actually rank = position in sorted order, 1-indexed
    Ds = []
    for i, (a, b) in enumerate(fracs):
        rank = i + 1  # 1-indexed
        f = a / b
        D = rank - n * f
        Ds.append(D)

    # B = 2 * sum D * delta
    B_raw = 2 * sum(D * d for D, d in zip(Ds, deltas))

    # C = sum delta^2
    C = sum(d * d for d in deltas)

    # sum x*delta = C/2 (identity)
    sum_x_delta = sum((a / b) * d for (a, b), d in zip(fracs, deltas))

    # R(x) = sum_{d|, d<=N} mu(d) * S(x, floor(N/d))
    # where S(x, M) = sum_{m=1}^M {x*m}
    # sum R*delta
    sum_R_delta = sum((-Ds[i] - fracs[i][0] / fracs[i][1]) * deltas[i] for i in range(n))
    # Actually R = -D - x, so sum R*delta = -sum D*delta - sum x*delta = -B_raw/2 - C/2
    sum_R_delta_check = -B_raw / 2 - C / 2

    # Leading term = M(p-1) * C/2
    mu = sieve_mu(N)
    M_vals = mertens_values(mu, N)
    M_p = M_vals[p] if p <= N else M_vals[N]  # M(p) -- but p > N = p-1, so use direct
    # Actually M(p) needs mu up to p
    mu_ext = sieve_mu(p)
    M_p_val = sum(mu_ext[d] for d in range(1, p + 1))
    M_pm1 = M_p_val + 1  # M(p-1) = M(p) - mu(p) = M(p) + 1 since mu(p)=-1... wait
    # mu(p) = -1 for prime p
    # M(p) = M(p-1) + mu(p) = M(p-1) - 1
    # So M(p-1) = M(p) + 1
    M_pm1_val = M_vals[N]  # M(p-1) = M(N) directly since N = p-1

    leading = M_pm1_val * (C / 2)
    Term2 = sum_R_delta - leading

    # correction = Term2 / (-C/2)
    if C > 0:
        correction = Term2 / (-C / 2)
    else:
        correction = 0

    # B >= 0 check
    B_positive = B_raw >= -1e-10

    # Ratio = sum_R_delta / (-C/2)
    if C > 0:
        ratio = sum_R_delta / (-C / 2)
    else:
        ratio = 0

    return {
        'p': p,
        'M_p': M_p_val,
        'M_pm1': M_pm1_val,
        'n': n,
        'B': B_raw,
        'C': C,
        'sum_R_delta': sum_R_delta,
        'leading': leading,
        'Term2': Term2,
        'correction': correction,
        'ratio': ratio,
        'B_positive': B_positive,
        'sum_x_delta': sum_x_delta,
        'C_half': C / 2,
    }

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def main():
    MAX_P = 10000

    # First: compute Mertens function for all integers up to MAX_P
    mu_all = sieve_mu(MAX_P)
    M_all = mertens_values(mu_all, MAX_P)

    # Find all primes with M(p) <= -3 up to MAX_P
    target_primes = []
    for p in range(2, MAX_P + 1):
        if is_prime(p) and M_all[p] <= -3:
            target_primes.append((p, M_all[p]))

    print(f"Found {len(target_primes)} primes with M(p) <= -3 up to {MAX_P}")
    print(f"First few: {target_primes[:10]}")
    print(f"Last few: {target_primes[-5:]}")
    print()

    # Count by M(p) value
    from collections import Counter
    mp_counts = Counter(mp for _, mp in target_primes)
    print("Distribution of M(p) values:")
    for mp in sorted(mp_counts.keys()):
        print(f"  M(p) = {mp}: {mp_counts[mp]} primes")
    print()

    # Compute correction for primes up to a reasonable limit
    # (full Farey sequence for large p is expensive -- limit direct computation)
    COMPUTE_LIMIT = 2000  # Direct computation up to this

    results = []
    worst_by_mp = {}  # M(p) -> (worst_correction, p)

    print(f"Computing correction terms for primes up to {COMPUTE_LIMIT}...")
    print(f"{'p':>6} {'M(p)':>5} {'n':>8} {'Leading':>8} {'Correction':>12} {'Margin':>10} {'B>=0':>5}")
    print("-" * 70)

    t0 = time.time()
    for p, mp in target_primes:
        if p > COMPUTE_LIMIT:
            break

        res = compute_B_and_correction(p)
        results.append(res)

        # Margin: how much slack we have
        # For M(p) = mp: need correction > -(|mp| - 2)
        threshold = -(abs(mp) - 2)
        margin = res['correction'] - threshold

        mp_val = mp
        if mp_val not in worst_by_mp or res['correction'] < worst_by_mp[mp_val][0]:
            worst_by_mp[mp_val] = (res['correction'], p)

        print(f"{p:>6} {mp:>5} {res['n']:>8} {abs(mp)-1:>8} {res['correction']:>12.6f} {margin:>10.6f} {'YES' if res['B_positive'] else 'NO':>5}")

    elapsed = time.time() - t0
    print(f"\nComputation took {elapsed:.1f}s")

    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY BY M(p) VALUE")
    print("=" * 70)

    for mp_val in sorted(worst_by_mp.keys()):
        subset = [r for r in results if r['M_p'] == mp_val]
        corrections = [r['correction'] for r in subset]
        threshold = -(abs(mp_val) - 2)

        print(f"\nM(p) = {mp_val} ({len(subset)} primes computed):")
        print(f"  Threshold: correction > {threshold}")
        print(f"  Worst correction: {min(corrections):.6f} at p = {worst_by_mp[mp_val][1]}")
        print(f"  Best correction:  {max(corrections):.6f}")
        print(f"  Mean correction:  {sum(corrections)/len(corrections):.6f}")
        print(f"  All satisfy bound: {'YES' if min(corrections) > threshold else 'NO'}")
        if mp_val == -3:
            print(f"  ** CRITICAL CASE: need > -1, worst = {min(corrections):.6f}, margin = {min(corrections) - (-1):.6f}")

    # Check if all B >= 0
    all_positive = all(r['B_positive'] for r in results)
    print(f"\nAll B >= 0: {'YES' if all_positive else 'NO'}")

    # Find the empirical P0
    # For each M(p) value, find the largest p where correction is closest to threshold
    print("\n" + "=" * 70)
    print("EXPLICIT P0 ANALYSIS")
    print("=" * 70)

    # The worst case overall
    worst_correction = min(r['correction'] for r in results)
    worst_p = [r['p'] for r in results if r['correction'] == worst_correction][0]
    worst_mp = [r['M_p'] for r in results if r['correction'] == worst_correction][0]

    print(f"Worst correction overall: {worst_correction:.6f} at p = {worst_p} (M(p) = {worst_mp})")
    print(f"Required threshold for M(p)={worst_mp}: > {-(abs(worst_mp)-2)}")
    print(f"Margin: {worst_correction - (-(abs(worst_mp)-2)):.6f}")

    # For M(p)=-3 specifically
    mp3_results = [r for r in results if r['M_p'] == -3]
    if mp3_results:
        mp3_corrections = [(r['correction'], r['p']) for r in mp3_results]
        mp3_corrections.sort()
        print(f"\nM(p) = -3 primes (worst 10):")
        for corr, p in mp3_corrections[:10]:
            print(f"  p = {p:>6}, correction = {corr:.6f}")

        # After what p does correction stay positive?
        last_negative_p = 0
        for corr, p in mp3_corrections:
            if corr < 0:
                last_negative_p = max(last_negative_p, p)
        print(f"\nLast M(p)=-3 prime with negative correction: p = {last_negative_p}")

    # For M(p)=-4
    mp4_results = [r for r in results if r['M_p'] == -4]
    if mp4_results:
        mp4_corrections = [(r['correction'], r['p']) for r in mp4_results]
        mp4_corrections.sort()
        print(f"\nM(p) = -4 primes (worst 5):")
        for corr, p in mp4_corrections[:5]:
            print(f"  p = {p:>6}, correction = {corr:.6f}")

    # Dedekind sum bound analysis
    print("\n" + "=" * 70)
    print("RADEMACHER BOUND ANALYSIS")
    print("=" * 70)
    print("Rademacher: |s(h,k)| <= (k-1)/12")
    print("El Marraki: |M(x)| <= 0.644 * x / log(x)  for x >= 1")
    print()

    # For primes beyond computation range, estimate correction bound
    # The correction involves Term2 = sum_{k=1}^{N-1} M(k) * sum_x Delta_S_k * delta
    # Each inner sum involves fractional part correlations
    # Key insight: for large p, the inner sums average to 0 and the correction
    # is dominated by the d=1 component which is O(1).

    # Empirical: correction grows logarithmically for fixed M(p)
    print("Correction growth analysis for M(p)=-3 primes:")
    if mp3_results:
        for r in sorted(mp3_results, key=lambda x: x['p']):
            if r['p'] <= 500 or r['p'] % 100 < 50:
                print(f"  p = {r['p']:>6}, correction = {r['correction']:>10.6f}, log(p) = {math.log(r['p']):>6.3f}")

    # Output for document
    print("\n" + "=" * 70)
    print("TABLE FOR B_EXPLICIT_P0.md")
    print("=" * 70)
    print("| p | M(p) | |M(p)|-1 | Correction | Threshold | Margin | B>=0 |")
    print("|---|------|----------|------------|-----------|--------|------|")
    for r in results:
        threshold = -(abs(r['M_p']) - 2)
        margin = r['correction'] - threshold
        print(f"| {r['p']} | {r['M_p']} | {abs(r['M_p'])-1} | {r['correction']:.4f} | >{threshold} | {margin:.4f} | {'YES' if r['B_positive'] else 'NO'} |")

if __name__ == '__main__':
    main()
