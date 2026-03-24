#!/usr/bin/env python3
"""
LARGE-SCALE FAREY-MERTENS COMPUTATION
======================================

Using the batch Farey sum algorithm:
  S(m,N) = M(N) + 1 + sum_{d|m, d>=2} d * M(floor(N/d))

After precomputing M[] via sieve in O(N log log N), each S(m,N)
query costs only O(tau(m)) -- the number of divisors of m.

COMPUTATIONS:
1. Violation prediction at scale: all primes 11 <= p <= 500,000
2. M <= -3 conjecture extended to 500K
3. Character Mertens statistics (chi_3, chi_4, chi_5)
4. Spectral correlations at N=100,000
5. New pattern search
"""

import numpy as np
from math import sqrt, log, pi, cos, sin, gcd, floor
from collections import defaultdict, Counter
import time
import json
import sys
import os

# ================================================================
# CORE SIEVES
# ================================================================

def mobius_sieve(N):
    """
    Compute mu[n] and M[n] (Mertens function) for n=0..N.
    Uses linear sieve: O(N) time.
    Also returns is_prime array.
    """
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    is_prime = np.ones(N + 1, dtype=np.bool_)
    is_prime[0] = is_prime[1] = False
    primes = []

    for i in range(2, N + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]

    # Cumulative Mertens
    M = np.zeros(N + 1, dtype=np.int32)
    M[1] = 1
    for n in range(2, N + 1):
        M[n] = M[n-1] + mu[n]

    return mu, M, is_prime, primes


def divisors(n):
    """Return sorted list of divisors of n."""
    divs = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
        i += 1
    return sorted(divs)


def S_farey(m, N, M):
    """
    Compute S(m,N) = sum_{f in F_N} e^{2*pi*i*m*f} using the universal formula.
    S(m,N) = M(N) + 1 + sum_{d|m, d>=2, d<=N} d * M[N//d]

    Returns a real integer (since S(m,N) is always an integer for integer m).
    """
    result = int(M[N]) + 1
    # Find divisors of m that are >= 2 and <= N
    i = 2
    while i * i <= m:
        if m % i == 0:
            if i <= N:
                result += i * int(M[N // i])
            j = m // i
            if j != i and j >= 2 and j <= N:
                result += j * int(M[N // j])
        i += 1
    # m itself as a divisor (if m >= 2 and m <= N)
    if m >= 2 and m <= N:
        result += m * int(M[N // m])
    return result


def S_farey_with_divisors(m, N, M, divs):
    """S(m,N) using precomputed divisor list."""
    result = int(M[N]) + 1
    for d in divs:
        if d < 2:
            continue
        if d > N:
            break
        result += d * int(M[N // d])
    return result


# ================================================================
# COMPUTATION 1: VIOLATION PREDICTION AT SCALE
# ================================================================

def computation_1_violation_prediction(M, is_prime, primes, N_MAX):
    """
    For all primes 11 <= p <= 500,000:
    - Compute M(p) and M(p)/sqrt(p)
    - Classify by sigmoid bin
    - Count predicted violations vs actual M > 0 rate
    """
    print("=" * 78)
    print("COMPUTATION 1: VIOLATION PREDICTION AT SCALE (primes to 500K)")
    print("=" * 78)
    t0 = time.time()

    # Collect data for all primes >= 11
    prime_list = [p for p in primes if p >= 11 and p <= N_MAX]
    n_primes = len(prime_list)
    print(f"  Primes in [11, {N_MAX}]: {n_primes}")

    # Compute M(p)/sqrt(p) for all primes
    m_norm = np.array([M[p] / sqrt(p) for p in prime_list])
    m_vals = np.array([int(M[p]) for p in prime_list])

    # Basic statistics
    print(f"\n  M(p)/sqrt(p) statistics:")
    print(f"    Mean:   {np.mean(m_norm):.6f}")
    print(f"    Median: {np.median(m_norm):.6f}")
    print(f"    Std:    {np.std(m_norm):.6f}")
    print(f"    Min:    {np.min(m_norm):.6f} at p={prime_list[np.argmin(m_norm)]}")
    print(f"    Max:    {np.max(m_norm):.6f} at p={prime_list[np.argmax(m_norm)]}")

    # M(p) > 0 rate (positive Mertens at primes)
    m_positive = m_vals > 0
    print(f"\n  M(p) > 0 rate: {np.sum(m_positive)} / {n_primes} = {100*np.mean(m_positive):.2f}%")

    # Sigmoid prediction model:
    # P(violation | M(p)/sqrt(p) = x) ~ sigmoid(a*(x - b))
    # From prior work, violations correlate with M(p)/sqrt(p) > ~0.15
    # We'll bin by M(p)/sqrt(p) and measure actual M>0 rate in each bin

    print(f"\n  M(p) > 0 rate by M(p)/sqrt(p) bin:")
    bin_edges = [-1.0, -0.6, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 1.0]
    print(f"  {'Bin':>16} {'Count':>7} {'M>0':>6} {'Rate':>7}")
    for i in range(len(bin_edges) - 1):
        lo, hi = bin_edges[i], bin_edges[i+1]
        mask = (m_norm >= lo) & (m_norm < hi)
        cnt = np.sum(mask)
        if cnt > 0:
            pos = np.sum(m_positive & mask)
            rate = 100 * pos / cnt
            print(f"  [{lo:+.2f},{hi:+.2f}) {cnt:7d} {pos:6d} {rate:6.1f}%")

    # By range of p (does prediction accuracy change at large p?)
    print(f"\n  M(p)>0 rate and mean |M(p)/sqrt(p)| by prime range:")
    print(f"  {'Range':>20} {'Primes':>7} {'M>0':>6} {'Rate':>7} {'Mean|M/sqrtp|':>14} {'Max M/sqrtp':>12}")

    range_size = 50000
    for lo in range(0, N_MAX + 1, range_size):
        hi = lo + range_size
        mask = np.array([(lo <= p < hi) for p in prime_list])
        cnt = np.sum(mask)
        if cnt == 0:
            continue
        pos = np.sum(m_positive & mask)
        rate = 100 * pos / cnt
        mean_abs = np.mean(np.abs(m_norm[mask]))
        max_val = np.max(m_norm[mask])
        print(f"  [{lo:>6d},{hi:>6d}) {cnt:7d} {pos:6d} {rate:6.1f}%  {mean_abs:13.6f}  {max_val:+11.6f}")

    # Sigmoid fit: P(M>0) as function of M/sqrt(p)
    # Use empirical bins
    print(f"\n  Empirical sigmoid: P(M(p)>0 | M(p)/sqrt(p) in bin)")
    fine_bins = np.linspace(-0.8, 0.8, 33)
    sigmoid_data = []
    print(f"  {'Bin center':>12} {'Count':>7} {'P(M>0)':>8}")
    for i in range(len(fine_bins) - 1):
        lo, hi = fine_bins[i], fine_bins[i+1]
        center = (lo + hi) / 2
        mask = (m_norm >= lo) & (m_norm < hi)
        cnt = np.sum(mask)
        if cnt > 10:
            pos = np.sum(m_positive & mask)
            rate = pos / cnt
            sigmoid_data.append((center, rate, cnt))
            print(f"  {center:+12.4f} {cnt:7d} {rate:8.4f}")

    # NOTE: M(p)/sqrt(p) IS the normalized Mertens value, and M(p)>0 is
    # trivially correlated because M(p)>0 iff M(p)/sqrt(p)>0.
    # The real question is about WOBBLE violations.
    # Since we don't have wobble data at 500K, we check the M>0 rate
    # as a proxy: from earlier data, wobble violations cluster near M>0 zones.

    # KEY FINDING: Does the distribution of M(p)/sqrt(p) change?
    print(f"\n  Distribution of M(p)/sqrt(p) by range (checking RH consistency):")
    print(f"  {'Range':>20} {'Mean':>9} {'Std':>9} {'Skew':>9} {'Kurt':>9}")
    for lo in range(0, N_MAX + 1, 100000):
        hi = lo + 100000
        mask = np.array([(lo <= p < hi) for p in prime_list])
        vals = m_norm[mask]
        if len(vals) > 100:
            z = (vals - np.mean(vals)) / np.std(vals)
            sk = float(np.mean(z**3))
            ku = float(np.mean(z**4)) - 3
            print(f"  [{lo:>6d},{hi:>6d}) {np.mean(vals):+9.5f} {np.std(vals):9.5f} {sk:+9.5f} {ku:+9.5f}")

    t1 = time.time()
    print(f"\n  Time: {t1-t0:.2f}s")

    return m_norm, m_vals, prime_list


# ================================================================
# COMPUTATION 2: M <= -3 CONJECTURE EXTENDED
# ================================================================

def computation_2_m_leq_minus3(M, is_prime, primes, N_MAX):
    """
    Among all primes with M(p) <= -3 up to 500K:
    - How many are there?
    - Systematic trends?
    - Tightest M(p)/sqrt(p)?
    """
    print("\n" + "=" * 78)
    print("COMPUTATION 2: M(p) <= -3 CONJECTURE EXTENDED TO 500K")
    print("=" * 78)
    t0 = time.time()

    prime_list = [p for p in primes if p >= 11 and p <= N_MAX]

    # Find primes where M(p) <= -3
    m3_primes = [(p, int(M[p]), M[p]/sqrt(p)) for p in prime_list if M[p] <= -3]

    print(f"\n  Primes with M(p) <= -3: {len(m3_primes)} out of {len(prime_list)}")
    print(f"  Rate: {100*len(m3_primes)/len(prime_list):.2f}%")

    if m3_primes:
        # Sort by M(p)/sqrt(p) (closest to 0 = tightest)
        m3_primes.sort(key=lambda x: x[2], reverse=True)  # closest to 0 first

        print(f"\n  Tightest M(p)/sqrt(p) values among M(p) <= -3 primes:")
        print(f"  {'p':>8} {'M(p)':>7} {'M(p)/sqrt(p)':>14}")
        for p, mv, mn in m3_primes[:20]:
            print(f"  {p:8d} {mv:7d} {mn:+14.8f}")

        print(f"\n  Most negative M(p)/sqrt(p) among M(p) <= -3 primes:")
        for p, mv, mn in m3_primes[-10:]:
            print(f"  {p:8d} {mv:7d} {mn:+14.8f}")

        # Distribution of M values at these primes
        m_at_m3 = [mv for _, mv, _ in m3_primes]
        m_counter = Counter(m_at_m3)
        print(f"\n  Distribution of M(p) values among M(p) <= -3 primes:")
        for mv in sorted(m_counter.keys()):
            print(f"    M(p) = {mv:4d}: {m_counter[mv]:6d} primes")

        # Trend: does M(p) <= -3 rate change with p?
        print(f"\n  M(p) <= -3 rate by range:")
        print(f"  {'Range':>20} {'Primes':>7} {'M<=-3':>7} {'Rate':>7} {'Min M':>7} {'MinM/sqrtp':>11}")
        range_size = 50000
        for lo in range(0, N_MAX + 1, range_size):
            hi = lo + range_size
            ps_range = [p for p in prime_list if lo <= p < hi]
            m3_range = [(p, int(M[p]), M[p]/sqrt(p)) for p in ps_range if M[p] <= -3]
            if ps_range:
                min_m = min(int(M[p]) for p in ps_range)
                min_mn = min(M[p]/sqrt(p) for p in ps_range)
                rate = 100 * len(m3_range) / len(ps_range) if ps_range else 0
                print(f"  [{lo:>6d},{hi:>6d}) {len(ps_range):7d} {len(m3_range):7d} {rate:6.1f}%  {min_m:7d} {min_mn:+11.6f}")

        # Check: does the minimum M(p)/sqrt(p) approach 0 from below?
        # This would suggest an eventual counterexample to M(p) <= -3 conjecture
        print(f"\n  Trajectory of tightest M(p)/sqrt(p) among M<=-3 primes:")
        print(f"  (checking if it approaches 0, suggesting eventual counterexample)")
        checkpoints = [1000, 5000, 10000, 50000, 100000, 200000, 300000, 400000, 500000]
        for cp in checkpoints:
            if cp > N_MAX:
                break
            m3_up_to = [(p, mv, mn) for p, mv, mn in m3_primes if p <= cp]
            if m3_up_to:
                tightest = max(m3_up_to, key=lambda x: x[2])
                print(f"    Up to {cp:>7d}: tightest M/sqrt(p) = {tightest[2]:+.8f} at p={tightest[0]}")

    # Extended: check M(p) <= -K for various K
    print(f"\n  M(p) <= -K counts:")
    print(f"  {'K':>4} {'Count':>8} {'Rate':>7} {'Tightest M/sqrtp':>18}")
    for K in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]:
        mk_primes = [(p, M[p]/sqrt(p)) for p in prime_list if M[p] <= -K]
        if mk_primes:
            tightest = max(mk_primes, key=lambda x: x[1])
            print(f"  {K:4d} {len(mk_primes):8d} {100*len(mk_primes)/len(prime_list):6.1f}%  {tightest[1]:+18.8f} at p={tightest[0]}")
        else:
            print(f"  {K:4d} {0:8d} {0:6.1f}%  (none)")

    t1 = time.time()
    print(f"\n  Time: {t1-t0:.2f}s")


# ================================================================
# COMPUTATION 3: CHARACTER MERTENS STATISTICS
# ================================================================

def computation_3_character_mertens(mu, M, N_MAX):
    """
    Compute character-twisted Mertens sums:
    M_chi(N) = sum_{n=1}^{N} chi(n) * mu(n)

    For chi_3 (mod 3), chi_4 (mod 4), chi_5 (mod 5).
    Check GRH consistency: |M_chi(N)|/sqrt(N) bounded.
    """
    print("\n" + "=" * 78)
    print("COMPUTATION 3: CHARACTER MERTENS STATISTICS")
    print("=" * 78)
    t0 = time.time()

    LIMIT = min(N_MAX, 500000)

    # Define Dirichlet characters
    # chi_3 (mod 3): Legendre symbol. chi_3(1)=1, chi_3(2)=-1, chi_3(0)=0
    # chi_4 (mod 4): chi_4(1)=1, chi_4(3)=-1, chi_4(0)=chi_4(2)=0
    # chi_5 (mod 5): chi_5(1)=1, chi_5(2)=i, chi_5(3)=-i, chi_5(4)=-1, chi_5(0)=0
    #   For real part: use the Legendre symbol chi_5(n) = (n/5)
    #   chi_5(1)=1, chi_5(2)=-1, chi_5(3)=-1, chi_5(4)=1, chi_5(0)=0

    def chi3(n):
        r = n % 3
        if r == 0: return 0
        if r == 1: return 1
        return -1

    def chi4(n):
        r = n % 4
        if r == 1: return 1
        if r == 3: return -1
        return 0

    def chi5(n):
        """Legendre symbol (n/5)"""
        r = n % 5
        if r == 0: return 0
        if r in (1, 4): return 1
        return -1  # r in (2, 3)

    characters = [("chi_3 (mod 3)", chi3), ("chi_4 (mod 4)", chi4), ("chi_5 (Legendre mod 5)", chi5)]

    # Also compute standard M(N) = sum mu(n) for comparison
    # M is already precomputed

    for name, chi in characters:
        print(f"\n  --- {name} ---")

        # Compute M_chi(N) = sum_{n=1}^{N} chi(n)*mu(n)
        M_chi = np.zeros(LIMIT + 1, dtype=np.float64)
        for n in range(1, LIMIT + 1):
            M_chi[n] = M_chi[n-1] + chi(n) * mu[n]

        # Normalized: M_chi(N) / sqrt(N)
        checkpoints = [100, 1000, 10000, 50000, 100000, 200000, 300000, 400000, 500000]
        print(f"  {'N':>8} {'M_chi(N)':>10} {'M_chi/sqrtN':>12} {'|M_chi|/sqrtN':>14}")
        for cp in checkpoints:
            if cp > LIMIT:
                break
            val = M_chi[cp]
            norm = val / sqrt(cp)
            abs_norm = abs(val) / sqrt(cp)
            print(f"  {cp:8d} {val:10.0f} {norm:+12.6f} {abs_norm:14.6f}")

        # Find maximum |M_chi(N)|/sqrt(N)
        norms = np.abs(M_chi[2:]) / np.sqrt(np.arange(2, LIMIT + 1))
        max_norm = np.max(norms)
        max_idx = np.argmax(norms) + 2
        print(f"  Max |M_chi(N)|/sqrt(N) = {max_norm:.6f} at N={max_idx}")

        # GRH check: should stay bounded (under ~2 conjecturally)
        # Track running maximum
        print(f"\n  Running max |M_chi(N)|/sqrt(N):")
        running_max = 0
        for cp in [100, 500, 1000, 5000, 10000, 50000, 100000, 200000, 500000]:
            if cp > LIMIT:
                break
            local_norms = np.abs(M_chi[2:cp+1]) / np.sqrt(np.arange(2, cp + 1))
            running_max = max(running_max, np.max(local_norms))
            print(f"    Up to N={cp:>7d}: max|M_chi|/sqrtN = {running_max:.6f}")

    # Compare growth rates of all three
    print(f"\n  --- COMPARISON OF GROWTH RATES ---")
    print(f"  {'N':>8}", end="")
    for name, _ in characters:
        short = name.split()[0]
        print(f"  {'|'+short+'|/sqN':>14}", end="")
    print(f"  {'|M|/sqrtN':>14}")

    for cp in [1000, 10000, 50000, 100000, 200000, 500000]:
        if cp > LIMIT:
            break
        print(f"  {cp:8d}", end="")
        for name, chi in characters:
            mc = sum(int(chi(n)) * int(mu[n]) for n in range(1, cp+1))
            print(f"  {abs(mc)/sqrt(cp):14.6f}", end="")
        print(f"  {abs(int(M[cp]))/sqrt(cp):14.6f}")

    t1 = time.time()
    print(f"\n  Time: {t1-t0:.2f}s")


# ================================================================
# COMPUTATION 4: SPECTRAL CORRELATIONS
# ================================================================

def computation_4_spectral_correlations(M, is_prime, N_TARGET=100000):
    """
    At N = 100,000:
    - Compute S(m, N) for m = 1..10000
    - Study distribution of S values
    - Compare prime vs composite frequencies
    - Look for correlation structure
    """
    print("\n" + "=" * 78)
    print(f"COMPUTATION 4: SPECTRAL CORRELATIONS AT N={N_TARGET}")
    print("=" * 78)
    t0 = time.time()

    N = N_TARGET
    M_N = int(M[N])
    print(f"  M({N}) = {M_N}")
    print(f"  M({N})/sqrt({N}) = {M_N/sqrt(N):.6f}")

    M_MAX = 10000
    print(f"\n  Computing S(m, {N}) for m = 1..{M_MAX}...")

    S_vals = np.zeros(M_MAX + 1, dtype=np.int64)
    t_batch = time.time()

    for m in range(1, M_MAX + 1):
        S_vals[m] = S_farey(m, N, M)

    t_batch = time.time() - t_batch
    print(f"  Batch time: {t_batch:.3f}s ({M_MAX/t_batch:.0f} queries/sec)")

    # Basic statistics of S values
    sv = S_vals[1:]
    print(f"\n  S(m, {N}) statistics (m=1..{M_MAX}):")
    print(f"    Mean:   {np.mean(sv):.2f}")
    print(f"    Median: {np.median(sv):.0f}")
    print(f"    Std:    {np.std(sv):.2f}")
    print(f"    Min:    {np.min(sv)} at m={np.argmin(sv)+1}")
    print(f"    Max:    {np.max(sv)} at m={np.argmax(sv)+1}")

    # Note: S(m,N) = M(N)+1 for all m coprime to all d <= N
    # For prime p > N: S(p,N) = M(N)+1 (no divisors of p in [2,N])
    # For prime p <= N: S(p,N) = M(N)+1 + p*M(N//p)

    # Check: how many have S = M(N)+1 (the "baseline")?
    baseline = M_N + 1
    n_baseline = np.sum(sv == baseline)
    print(f"\n  S(m,{N}) = M(N)+1 = {baseline}: {n_baseline} values ({100*n_baseline/M_MAX:.1f}%)")
    print(f"  (These are m with no divisors in [2,{N}], i.e., primes > {N})")

    # Distribution of |S(m,N)|
    abs_sv = np.abs(sv)
    print(f"\n  Distribution of |S(m,{N})|:")
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    for p in percentiles:
        print(f"    {p:3d}th percentile: {np.percentile(abs_sv, p):.0f}")

    # Prime vs composite frequencies
    print(f"\n  Prime vs composite frequency analysis:")
    prime_m = [m for m in range(2, M_MAX+1) if is_prime[m]]
    comp_m = [m for m in range(2, M_MAX+1) if not is_prime[m] and m > 1]

    s_prime = np.array([S_vals[m] for m in prime_m])
    s_comp = np.array([S_vals[m] for m in comp_m])

    print(f"    Prime frequencies (n={len(prime_m)}):")
    print(f"      Mean S: {np.mean(s_prime):.2f}")
    print(f"      Std S:  {np.std(s_prime):.2f}")
    print(f"      Mean |S|: {np.mean(np.abs(s_prime)):.2f}")

    print(f"    Composite frequencies (n={len(comp_m)}):")
    print(f"      Mean S: {np.mean(s_comp):.2f}")
    print(f"      Std S:  {np.std(s_comp):.2f}")
    print(f"      Mean |S|: {np.mean(np.abs(s_comp)):.2f}")

    # For primes p <= N: S(p,N) = M(N)+1 + p*M(N//p)
    # So |S(p,N)| depends heavily on M(N//p)
    print(f"\n  S(p,{N}) decomposition for small primes:")
    print(f"  {'p':>7} {'M(N//p)':>8} {'p*M(N//p)':>10} {'S(p,N)':>10} {'S-baseline':>12}")
    for p in prime_m[:20]:
        if p <= N:
            correction = p * int(M[N//p])
            print(f"  {p:7d} {int(M[N//p]):8d} {correction:10d} {S_vals[p]:10d} {S_vals[p]-baseline:+12d}")

    # Spectral gaps: are there values that S never takes?
    s_set = set(sv)
    s_range = range(int(np.min(sv)), int(np.max(sv)) + 1)
    gaps = [v for v in s_range if v not in s_set]
    print(f"\n  Spectral gaps in S(m,{N}) for m=1..{M_MAX}:")
    print(f"    Range: [{np.min(sv)}, {np.max(sv)}]")
    print(f"    Distinct values: {len(s_set)}")
    print(f"    Gap count: {len(gaps)}")
    if gaps and len(gaps) < 100:
        print(f"    Gaps: {gaps[:50]}{'...' if len(gaps)>50 else ''}")

    # Correlation between S(m) and S(2m), S(3m), etc.
    print(f"\n  Correlations between S(m,N) and S(km,N) for small k:")
    for k in [2, 3, 5, 7, 11]:
        pairs_m = [m for m in range(1, M_MAX//k + 1)]
        s1 = np.array([S_vals[m] for m in pairs_m])
        s2 = np.array([S_vals[k*m] for m in pairs_m])
        if len(s1) > 10:
            corr = np.corrcoef(s1, s2)[0, 1]
            print(f"    corr(S(m), S({k}m)) = {corr:+.6f}  (n={len(pairs_m)})")

    # S(m,N) at different N values to check cross-N correlations
    print(f"\n  S(m,N) at multiple N (m=1..100):")
    N_vals = [10000, 20000, 50000, 100000]
    N_vals = [n for n in N_vals if n <= len(M) - 1]

    print(f"  {'m':>5}", end="")
    for n in N_vals:
        print(f"  {'S(m,'+str(n//1000)+'K)':>12}", end="")
    print()

    for m in [1, 2, 3, 5, 6, 10, 12, 30, 60, 100]:
        print(f"  {m:5d}", end="")
        for n in N_vals:
            s = S_farey(m, n, M)
            print(f"  {s:12d}", end="")
        print()

    # Cross-N correlation for fixed m
    if len(N_vals) >= 2:
        print(f"\n  Cross-N correlations (S(m,N1) vs S(m,N2), m=1..1000):")
        for i in range(len(N_vals)):
            for j in range(i+1, len(N_vals)):
                n1, n2 = N_vals[i], N_vals[j]
                s1_arr = np.array([S_farey(m, n1, M) for m in range(1, 1001)])
                s2_arr = np.array([S_farey(m, n2, M) for m in range(1, 1001)])
                corr = np.corrcoef(s1_arr, s2_arr)[0, 1]
                print(f"    corr(S(m,{n1}), S(m,{n2})) = {corr:+.6f}")

    t1 = time.time()
    print(f"\n  Time: {t1-t0:.2f}s")

    return S_vals


# ================================================================
# COMPUTATION 5: NEW PATTERN SEARCH
# ================================================================

def computation_5_new_patterns(M, is_prime, primes, mu, N_MAX):
    """
    Search for any new patterns in the data.
    """
    print("\n" + "=" * 78)
    print("COMPUTATION 5: NEW PATTERN SEARCH")
    print("=" * 78)
    t0 = time.time()

    # Pattern 1: Consecutive prime Mertens values
    print(f"\n  --- Pattern 1: Consecutive prime M(p) values ---")
    prime_list = [p for p in primes if p >= 11 and p <= N_MAX]
    m_at_primes = [int(M[p]) for p in prime_list]

    # Count consecutive same-sign M(p) runs
    runs = []
    current_sign = np.sign(m_at_primes[0])
    current_len = 1
    for i in range(1, len(m_at_primes)):
        s = np.sign(m_at_primes[i])
        if s == current_sign:
            current_len += 1
        else:
            runs.append((current_sign, current_len, prime_list[i - current_len]))
            current_sign = s
            current_len = 1
    runs.append((current_sign, current_len, prime_list[len(m_at_primes) - current_len]))

    pos_runs = [r for r in runs if r[0] > 0]
    neg_runs = [r for r in runs if r[0] < 0]
    zero_count = sum(1 for m in m_at_primes if m == 0)

    print(f"  M(p) = 0 at {zero_count} primes")
    if pos_runs:
        longest_pos = max(pos_runs, key=lambda x: x[1])
        print(f"  Longest positive run: {longest_pos[1]} primes starting at p={longest_pos[2]}")
        print(f"  Mean positive run length: {np.mean([r[1] for r in pos_runs]):.1f}")
    if neg_runs:
        longest_neg = max(neg_runs, key=lambda x: x[1])
        print(f"  Longest negative run: {longest_neg[1]} primes starting at p={longest_neg[2]}")
        print(f"  Mean negative run length: {np.mean([r[1] for r in neg_runs]):.1f}")

    # Pattern 2: M(p) modular structure
    print(f"\n  --- Pattern 2: M(p) mod small numbers ---")
    for mod in [3, 4, 5, 6, 7, 8]:
        counts = Counter(int(M[p]) % mod for p in prime_list)
        total = len(prime_list)
        print(f"  M(p) mod {mod}:", end="")
        for r in range(mod):
            c = counts.get(r, 0)
            print(f"  [{r}]:{100*c/total:.1f}%", end="")
        print()

    # Pattern 3: Twin prime Mertens correlation
    print(f"\n  --- Pattern 3: Twin prime M(p) values ---")
    twin_primes = [(prime_list[i], prime_list[i+1])
                   for i in range(len(prime_list)-1)
                   if prime_list[i+1] - prime_list[i] == 2]
    if twin_primes:
        m_diffs = [int(M[q]) - int(M[p]) for p, q in twin_primes]
        print(f"  Twin prime pairs found: {len(twin_primes)}")
        print(f"  M(q)-M(p) for twin primes (p,q=p+2):")
        print(f"    Mean: {np.mean(m_diffs):.4f}")
        print(f"    Std:  {np.std(m_diffs):.4f}")
        diff_counts = Counter(m_diffs)
        print(f"    Distribution: ", end="")
        for d in sorted(diff_counts.keys()):
            if diff_counts[d] > 10:
                print(f"[{d:+d}]:{diff_counts[d]}", end=" ")
        print()
        # M(q) - M(p) = mu(p+1) + mu(p+2) since M is cumulative
        # For twin primes p, p+2: the intermediate value p+1 is even
        # So mu(p+1) can be nonzero. mu(p+2) = -1 (since p+2 is prime).
        # So M(q)-M(p) = mu(p+1) + (-1) = mu(p+1) - 1
        print(f"  Theory: M(p+2)-M(p) = mu(p+1) - 1 (since mu(p+2)=-1)")
        predicted = [int(mu[p+1]) - 1 for p, _ in twin_primes]
        match = sum(1 for a, b in zip(m_diffs, predicted) if a == b)
        print(f"  Verification: {match}/{len(twin_primes)} match ({100*match/len(twin_primes):.1f}%)")

    # Pattern 4: Mertens at prime powers
    print(f"\n  --- Pattern 4: M(p^k) values ---")
    print(f"  {'p':>7} {'M(p)':>7} {'M(p^2)':>8} {'M(p^3)':>8} {'Ratio M(p^2)/M(p)':>18}")
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
        vals = []
        pk = p
        while pk <= N_MAX:
            vals.append((pk, int(M[pk])))
            pk *= p
        if len(vals) >= 2 and vals[0][1] != 0:
            line = f"  {p:7d} {vals[0][1]:7d}"
            for i in range(1, min(3, len(vals))):
                line += f" {vals[i][1]:8d}"
            ratio = vals[1][1] / vals[0][1] if vals[0][1] != 0 else float('inf')
            line += f" {ratio:18.4f}"
            print(line)

    # Pattern 5: S(m,N) at highly composite numbers
    print(f"\n  --- Pattern 5: S(m,N) for highly composite m ---")
    N_test = min(100000, N_MAX)
    hc_numbers = [2, 4, 6, 12, 24, 36, 48, 60, 120, 180, 240, 360, 720,
                  1260, 2520, 5040, 7560, 10080, 15120, 20160, 25200, 27720,
                  45360, 50400, 55440, 83160]
    print(f"  {'m':>7} {'tau(m)':>7} {'S(m,{0})'.format(N_test):>12} {'S/tau':>10}")
    for m in hc_numbers:
        if m <= N_test:
            divs = divisors(m)
            s = S_farey_with_divisors(m, N_test, M, divs)
            tau = len(divs)
            print(f"  {m:7d} {tau:7d} {s:12d} {s/tau:10.1f}")

    # Pattern 6: "Spectrogram" slice -- how S(m,N) varies with N for fixed m
    print(f"\n  --- Pattern 6: S(m,N) vs N trajectory for fixed m ---")
    for m in [2, 3, 6, 12, 30, 60]:
        print(f"\n  m={m}:")
        print(f"    {'N':>8} {'S(m,N)':>10} {'M(N)':>8} {'Correction':>12}")
        for N in [100, 500, 1000, 5000, 10000, 50000, 100000, 200000, 500000]:
            if N > N_MAX:
                break
            s = S_farey(m, N, M)
            corr = s - int(M[N]) - 1
            print(f"    {N:8d} {s:10d} {int(M[N]):8d} {corr:+12d}")

    # Pattern 7: Distribution of S(m, N) - M(N) - 1 (the "correction" term)
    print(f"\n  --- Pattern 7: Distribution of correction term S(m,N)-M(N)-1 ---")
    N_test = min(100000, N_MAX)
    corrections = []
    for m in range(1, 5001):
        s = S_farey(m, N_test, M)
        corrections.append(s - int(M[N_test]) - 1)
    corrections = np.array(corrections)
    print(f"  N={N_test}, m=1..5000:")
    print(f"    Mean correction: {np.mean(corrections):.2f}")
    print(f"    Std correction:  {np.std(corrections):.2f}")
    print(f"    Min: {np.min(corrections)}")
    print(f"    Max: {np.max(corrections)}")
    print(f"    Zero corrections: {np.sum(corrections == 0)} (primes > N_test)")

    # Pattern 8: Autocorrelation of M(n) sequence
    print(f"\n  --- Pattern 8: Autocorrelation of M(n) ---")
    ACLEN = min(200000, N_MAX)
    m_seq = np.array([M[n] for n in range(1, ACLEN+1)], dtype=np.float64)
    m_seq -= np.mean(m_seq)
    var = np.var(m_seq)
    if var > 0:
        print(f"  Autocorrelation of M(n) for n=1..{ACLEN}:")
        for lag in [1, 2, 3, 5, 10, 50, 100, 500, 1000]:
            if lag < ACLEN:
                ac = np.mean(m_seq[:-lag] * m_seq[lag:]) / var
                print(f"    lag={lag:>5d}: {ac:+.6f}")

    t1 = time.time()
    print(f"\n  Time: {t1-t0:.2f}s")


# ================================================================
# MAIN
# ================================================================

def main():
    N_MAX = 500000

    print("=" * 78)
    print(f"LARGE-SCALE FAREY-MERTENS COMPUTATION (N_MAX = {N_MAX})")
    print("=" * 78)
    print(f"Using batch Farey sum: S(m,N) = M(N)+1 + sum_{{d|m}} d*M(N//d)")
    print(f"After O(N log log N) sieve, each query costs O(tau(m))")
    print()

    t_start = time.time()

    # Step 0: Precompute
    print("Step 0: Precomputing Mobius sieve...")
    t0 = time.time()
    mu, M, is_prime, primes = mobius_sieve(N_MAX)
    t1 = time.time()
    print(f"  Sieve time: {t1-t0:.2f}s")
    print(f"  Primes found: {len(primes)}")
    print(f"  M({N_MAX}) = {M[N_MAX]}")
    print(f"  M({N_MAX})/sqrt({N_MAX}) = {M[N_MAX]/sqrt(N_MAX):.6f}")

    # Run all computations
    m_norm, m_vals, prime_list = computation_1_violation_prediction(M, is_prime, primes, N_MAX)
    computation_2_m_leq_minus3(M, is_prime, primes, N_MAX)
    computation_3_character_mertens(mu, M, N_MAX)
    S_vals = computation_4_spectral_correlations(M, is_prime, N_MAX)
    computation_5_new_patterns(M, is_prime, primes, mu, N_MAX)

    t_total = time.time() - t_start
    print(f"\n{'='*78}")
    print(f"TOTAL COMPUTATION TIME: {t_total:.1f}s")
    print(f"{'='*78}")


if __name__ == "__main__":
    main()
