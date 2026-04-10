"""
APPROACH: Ergodic Theory + Explicit Formula for Unconditional Proof
Marathon session - 2026-03-25

Goal: Attack the unconditional Sign Theorem via:
1. Explicit formula for M(N) and its implications for D/A
2. Ergodic/equidistribution approach to the Farey map
3. Investigate whether C/A = delta_sq/dilution_raw -> const or -> 0
4. Look for a tighter relationship between |1-D/A| and C/A

Key quantities (using raw = without 1/n'^2 normalization):
  A = dilution_raw = old_D_sq * (n'^2 - n^2)/n^2
  C = delta_sq = sum_{f in F_{p-1}} delta(f)^2
  D = new_D_sq = sum_{k=1}^{p-1} D_new(k/p)^2

D/A + C/A >= 1 iff DeltaW <= 0 (when B >= 0, but also sufficient when B < 0 if D/A + C/A > 1)
"""

import sys
sys.setrecursionlimit(100000)
from fractions import Fraction
import math

def euler_totient_sieve(n):
    """Compute phi(k) for k=1..n using sieve."""
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi

def mertens_sieve(n):
    """Compute M(k) for k=1..n using Mobius sieve."""
    mu = [0] * (n + 1)
    mu[1] = 1
    # Sieve
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

    M = [0] * (n + 1)
    for k in range(1, n + 1):
        M[k] = M[k - 1] + mu[k]
    return M

def compute_delta_sq(p):
    """
    Compute delta_sq = sum_{b=2}^{p-1} sum_{a coprime b, 0<a<b} (a - p*a mod b)^2 / b^2
    = sum_b (2/b^2) * deficit_b(p)

    Uses rational arithmetic for exact computation (slow but correct).
    Returns as float for speed.
    """
    N = p - 1
    total = 0.0
    for b in range(2, N + 1):
        # For each denominator b
        s = 0
        for a in range(1, b):
            if math.gcd(a, b) == 1:
                shift = a - (p * a % b)
                s += shift * shift
        total += s / (b * b)
    return total

def compute_delta_sq_fast(p):
    """
    Faster version: for each denominator b, compute sum (a - pa mod b)^2.
    Only loop over coprime a.
    """
    N = p - 1
    total = 0.0
    for b in range(2, N + 1):
        s = 0
        for a in range(1, b):
            if math.gcd(a, b) == 1:
                pa_mod_b = (p * a) % b
                diff = a - pa_mod_b
                s += diff * diff
        if s > 0:
            total += s / (b * b)
    return total

def farey_rank(N, num, den, phi_vals, cumulative_n):
    """
    Compute rank of num/den in F_N.
    rank = #{a/b in F_N : a/b <= num/den, a/b != 0/1 boundary}

    Use the fast formula: rank(a/b) = sum_{j=0}^{b} #{a' in F_N with denom j, a'/j <= a/b}
    Actually easier: rank = #{(a',b') coprime : b' <= N, a'/b' <= a/b} + 1 (for 0/1)
    """
    # This is O(N^2) - too slow. Use alternative approach.
    pass

def compute_old_D_sq_via_formula(p):
    """
    Compute old_D_sq = sum_{f in F_{p-1}} D(f)^2 using a combinatorial formula.

    Note: This is the WOBBLE * n^2, where wobble = sum (f_j - j/n)^2.

    Fast formula: Instead of enumerating all Farey fractions, use the identity:
    old_D_sq = sum_{a/b in F_N} (rank(a/b) - n * a/b)^2

    Alternative: use the Franel-type sum
    old_D_sq = sum_{b=1}^N sum_{a=0,gcd(a,b)=1}^b ...

    For now, use the direct computation with Farey sequence generation.
    """
    N = p - 1
    # Generate Farey sequence F_N
    fracs = []  # list of (numerator, denominator) as integers

    # Farey sequence generation O(n) where n = |F_N|
    a, b = 0, 1
    c, d = 1, N
    fracs.append((a, b))
    while (c, d) != (1, 1):
        fracs.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    fracs.append((1, 1))

    n = len(fracs)

    # Compute D(f) = rank(f) - n * f for each f
    # rank(f_j) = j (0-indexed from 0 to n-1)
    total = 0.0
    for j, (a, b) in enumerate(fracs):
        f = a / b
        D = j - n * f
        total += D * D

    return total, n

def dilution_raw(old_D_sq, n, n_prime):
    """dilution_raw = old_D_sq * (n'^2 - n^2) / n^2"""
    return old_D_sq * (n_prime * n_prime - n * n) / (n * n)

def compute_all_for_prime(p):
    """Compute all key quantities for prime p."""
    N = p - 1

    # Compute old_D_sq and n
    old_D_sq_val, n = compute_old_D_sq_via_formula(p)
    n_prime = n + (p - 1)

    # Dilution
    dil = dilution_raw(old_D_sq_val, n, n_prime)

    # delta_sq
    delta_sq_val = compute_delta_sq_fast(p)

    # Wobble
    W = old_D_sq_val / (n * n)

    # Ratios
    C_A = delta_sq_val / dil
    C_W = N * W  # = N * old_D_sq / n^2

    return {
        'p': p, 'N': N, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq_val, 'delta_sq': delta_sq_val,
        'dilution_raw': dil, 'W': W,
        'C_A': C_A, 'C_W': C_W,
    }

def main_small_p():
    """
    Compute for small primes with M(p) <= -3.
    Focus: verify scaling of C/A and C_W.
    """
    print("Computing Mertens function...")
    MAX_P = 2000  # Start small to verify
    M_vals = mertens_sieve(MAX_P)

    from sympy import isprime

    print(f"{'p':>6} {'M(p)':>6} {'n':>8} {'C_W':>8} {'C/A':>10} {'D/A':>10}")
    print("-" * 60)

    results = []
    for p in range(11, MAX_P + 1, 2):
        if not isprime(p):
            continue
        if M_vals[p] > -3:
            continue

        try:
            data = compute_all_for_prime(p)
        except Exception as e:
            print(f"Error at p={p}: {e}")
            continue

        # Compute new_D_sq to get D/A
        # D_new(k/p) = D_old(k/p) + k/p
        # = (rank of k/p in F_{p-1}) - n*(k/p) + k/p
        # = rank_old(k/p) - (n-1)*(k/p)
        N = p - 1
        n = data['n']

        # Generate F_{p-1} and compute D_old at k/p
        fracs_sorted = []
        a, b = 0, 1
        c, d = 1, N
        fracs_sorted.append((a, b))
        while (c, d) != (1, 1):
            fracs_sorted.append((c, d))
            k = (N + b) // d
            a, b, c, d = c, d, k * c - a, k * d - b
        fracs_sorted.append((1, 1))

        # For each new fraction k/p, find its rank in F_{p-1}
        # by binary search in the sorted Farey sequence
        new_D_sq = 0.0
        for k in range(1, p):
            kp = k / p
            # Binary search for rank = #{f in F_{p-1} : f <= k/p}
            lo, hi = 0, n
            while lo < hi:
                mid = (lo + hi) // 2
                a_m, b_m = fracs_sorted[mid]
                if a_m * p <= k * b_m:  # a_m/b_m <= k/p
                    lo = mid + 1
                else:
                    hi = mid
            rank_old = lo  # = #{f <= k/p}
            D_old = rank_old - n * kp
            D_new = D_old + kp
            new_D_sq += D_new * D_new

        D_A = new_D_sq / data['dilution_raw']

        print(f"{p:>6} {M_vals[p]:>6} {n:>8} {data['C_W']:>8.4f} {data['C_A']:>10.6f} {D_A:>10.6f}")
        results.append({**data, 'M': M_vals[p], 'D_A': D_A})

    return results

def analyze_scaling(results):
    """
    Fit log-log slopes to understand C/A and C_W scaling with p.
    """
    if len(results) < 5:
        return

    import numpy as np

    ps = [r['p'] for r in results]
    CAs = [r['C_A'] for r in results]
    CWs = [r['C_W'] for r in results]
    delta_sqs = [r['delta_sq'] for r in results]
    dilutions = [r['dilution_raw'] for r in results]
    ns = [r['n'] for r in results]

    log_p = [math.log(p) for p in ps]

    # Fit delta_sq ~ p^alpha
    log_d = [math.log(d) for d in delta_sqs]
    alpha_d = (log_d[-1] - log_d[0]) / (math.log(ps[-1]) - math.log(ps[0]))

    # Fit dilution_raw ~ p^alpha
    log_dil = [math.log(d) for d in dilutions]
    alpha_dil = (log_dil[-1] - log_dil[0]) / (math.log(ps[-1]) - math.log(ps[0]))

    # Fit C/A ~ p^alpha (negative = decreasing)
    log_CA = [math.log(c) for c in CAs if c > 0]
    ps_for_CA = [ps[i] for i, c in enumerate(CAs) if c > 0]
    if len(ps_for_CA) >= 2:
        alpha_CA = (math.log(ps_for_CA[-1]/ps_for_CA[0]) and
                   (log_CA[-1] - log_CA[0]) / (math.log(ps_for_CA[-1]) - math.log(ps_for_CA[0])))

    # Fit C_W ~ p^alpha
    log_CW = [math.log(c) for c in CWs if c > 0]
    ps_for_CW = [ps[i] for i, c in enumerate(CWs) if c > 0]

    print("\n=== SCALING ANALYSIS ===")
    print(f"delta_sq ~ p^{alpha_d:.3f}")
    print(f"dilution_raw ~ p^{alpha_dil:.3f}")
    print(f"n ~ p^{math.log(ns[-1]/ns[0]) / math.log(ps[-1]/ps[0]):.3f}")
    print(f"C/A = delta_sq/dilution ~ p^{alpha_d-alpha_dil:.3f}")
    print(f"  If < 0: C/A -> 0 (bad for unconditional proof)")
    print(f"  If > 0: C/A -> infty (great!)")
    print(f"  If = 0: C/A -> const (good if const > 0)")

    print(f"\nC/A range: [{min(CAs):.4f}, {max(CAs):.4f}]")
    print(f"C_W range: [{min(CWs):.4f}, {max(CWs):.4f}]")
    print(f"  If C_W -> 0: C/A = pi^2/(72*C_W) -> infty (great!)")
    print(f"  If C_W -> const: C/A = const (good)")
    print(f"  If C_W -> infty: C/A -> 0 (bad)")


if __name__ == '__main__':
    import time

    print("=== ERGODIC/EXPLICIT FORMULA ATTACK ===")
    print("Computing key quantities for small M(p) <= -3 primes")
    print()

    t0 = time.time()
    results = main_small_p()
    t1 = time.time()

    print(f"\nTime: {t1-t0:.1f}s")
    analyze_scaling(results)

    # Save results
    import json
    output = {
        'results': results,
        'note': 'Computed for M(p) <= -3 primes to analyze C/A asymptotics'
    }
    with open('/Users/saar/Desktop/Farey-Local/experiments/ca_scaling_data.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("Saved to ca_scaling_data.json")
