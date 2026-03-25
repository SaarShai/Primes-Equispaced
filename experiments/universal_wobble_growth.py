#!/usr/bin/env python3
"""
Universal Wobble Growth Analysis
=================================

QUESTION: W(p) > W(p-1) for ALL primes 11 <= p <= ~1300.
The first known violation is at p=1399 (M=+8).

This script:
1. Computes W(p)/W(p-1) for primes up to 500 using exact Fraction arithmetic
2. Extends to primes up to 1500 using float to find first W(p) < W(p-1)
3. Checks whether ALL violations have M(p) > 0 (confirming Sign Theorem)
4. Analyzes the transition: smooth decay or sudden drop?
5. Shows how excess = W(p)/W(p-1) - 1 depends on p and M(p)
"""

from fractions import Fraction
from math import gcd, sqrt
import time
import sys


# ─── Sieves ───────────────────────────────────────────────────────────────────

def sieve_primes(limit):
    """Return boolean array where sieve[i] = True iff i is prime."""
    sieve = [False, False] + [True] * (limit - 1)
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return sieve


def mobius_sieve(limit):
    """Compute Mobius function mu(n) for n = 0..limit."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu


def mertens_values(limit):
    """Compute M(n) = sum_{k=1}^{n} mu(k) for n = 0..limit."""
    mu = mobius_sieve(limit)
    M = [0] * (limit + 1)
    for i in range(1, limit + 1):
        M[i] = M[i - 1] + mu[i]
    return M


# ─── Farey / Wobble with Fractions ────────────────────────────────────────────

def farey_set_fractions(N):
    """Build F_N as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def wobble_exact(sorted_fracs):
    """W = sum_{j=0}^{n-1} (f_j - j/n)^2 using exact Fraction arithmetic."""
    n = len(sorted_fracs)
    if n == 0:
        return Fraction(0)
    W = Fraction(0)
    for j, f in enumerate(sorted_fracs):
        delta = f - Fraction(j, n)
        W += delta * delta
    return W


# ─── Farey / Wobble with floats ──────────────────────────────────────────────

def wobble_float_incremental(frac_set_float, N_prev, N_new):
    """
    Add fractions with denominators N_prev+1 .. N_new to frac_set_float,
    then compute wobble from sorted array.
    Returns (wobble_value, updated_frac_set).
    """
    for d in range(N_prev + 1, N_new + 1):
        for a in range(1, d):
            if gcd(a, d) == 1:
                frac_set_float.add(a / d)
    sorted_f = sorted(frac_set_float)
    n = len(sorted_f)
    W = 0.0
    for j, f in enumerate(sorted_f):
        delta = f - j / n
        W += delta * delta
    return W, frac_set_float


# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 1: Exact Fraction arithmetic up to p ~ 500
# ═══════════════════════════════════════════════════════════════════════════════

def phase1_exact(max_p=500):
    print("=" * 78)
    print(f"PHASE 1: Exact Fraction arithmetic for primes up to {max_p}")
    print("=" * 78)

    is_prime = sieve_primes(max_p)
    M = mertens_values(max_p)
    primes = [p for p in range(2, max_p + 1) if is_prime[p]]

    # Build Farey sequences incrementally with Fractions
    farey = sorted([Fraction(0, 1), Fraction(1, 1)])
    W_prev_val = wobble_exact(farey)  # W(1)

    # We need W(N) for each N, stored so we can look up W(p-1)
    W_values = {1: W_prev_val}

    results = []
    t0 = time.time()

    for N in range(2, max_p + 1):
        # Add fractions with denominator N
        new_fracs = []
        for a in range(1, N):
            if gcd(a, N) == 1:
                new_fracs.append(Fraction(a, N))
        farey = sorted(set(farey) | set(new_fracs))
        W_N = wobble_exact(farey)
        W_values[N] = W_N

        if is_prime[N] and N >= 11:
            W_pm1 = W_values[N - 1]
            ratio = W_N / W_pm1
            excess = ratio - 1
            grew = W_N > W_pm1

            results.append({
                'p': N,
                'M': M[N],
                'W_p': W_N,
                'W_pm1': W_pm1,
                'ratio': ratio,
                'excess': float(excess),
                'grew': grew,
            })

            if N <= 50 or N % 50 < 5 or not grew:
                elapsed = time.time() - t0
                print(f"  p={N:4d}  M={M[N]:+3d}  ratio={float(ratio):.10f}  "
                      f"excess={float(excess):+.2e}  grew={grew}  [{elapsed:.1f}s]")

        if N % 100 == 0:
            elapsed = time.time() - t0
            print(f"  ... processed N={N}, elapsed {elapsed:.1f}s")

    # Summary
    violations = [r for r in results if not r['grew']]
    print(f"\n  Primes 11..{max_p}: {len(results)} tested")
    print(f"  Violations (W(p) <= W(p-1)): {len(violations)}")
    if violations:
        for v in violations:
            print(f"    p={v['p']}, M={v['M']}, ratio={float(v['ratio']):.10f}")
    else:
        print("  >>> ZERO violations! W(p) > W(p-1) for ALL primes in range <<<")

    print(f"\n  Excess range: [{min(r['excess'] for r in results):.6e}, "
          f"{max(r['excess'] for r in results):.6e}]")

    # Show how excess decays
    print("\n  Excess decay profile (selected primes):")
    for r in results:
        if r['p'] in [11, 13, 17, 23, 29, 37, 53, 97, 101, 151, 199, 251, 307, 401, 499] or \
           r['p'] == results[-1]['p']:
            print(f"    p={r['p']:4d}  M={r['M']:+3d}  excess={r['excess']:+.8e}")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 2: Float arithmetic up to p ~ 1500
# ═══════════════════════════════════════════════════════════════════════════════

def phase2_float(max_p=1500):
    print("\n" + "=" * 78)
    print(f"PHASE 2: Float arithmetic for primes up to {max_p}")
    print("=" * 78)

    is_prime = sieve_primes(max_p)
    M = mertens_values(max_p)
    primes = [p for p in range(2, max_p + 1) if is_prime[p]]

    # Build Farey incrementally with floats
    frac_set = {0.0, 1.0}
    W_values = {}
    W_values[1] = 0.25

    results = []
    first_violation = None
    t0 = time.time()

    for N in range(2, max_p + 1):
        for a in range(1, N):
            if gcd(a, N) == 1:
                frac_set.add(a / N)
        # Compute wobble
        sorted_f = sorted(frac_set)
        n = len(sorted_f)
        W = 0.0
        for j in range(n):
            delta = sorted_f[j] - j / n
            W += delta * delta
        W_values[N] = W

        if is_prime[N] and N >= 11:
            W_pm1 = W_values[N - 1]
            if W_pm1 > 0:
                ratio = W / W_pm1
                excess = ratio - 1.0
            else:
                ratio = float('inf')
                excess = float('inf')
            grew = W > W_pm1

            results.append({
                'p': N,
                'M': M[N],
                'W_p': W,
                'W_pm1': W_pm1,
                'ratio': ratio,
                'excess': excess,
                'grew': grew,
            })

            if not grew and first_violation is None:
                first_violation = results[-1]
                print(f"\n  *** FIRST VIOLATION at p={N}, M={M[N]}, "
                      f"ratio={ratio:.12f}, excess={excess:.6e} ***\n")

        if N % 200 == 0:
            elapsed = time.time() - t0
            print(f"  ... processed N={N}, elapsed {elapsed:.1f}s")

    # Summary
    violations = [r for r in results if not r['grew']]
    pos_M_violations = [v for v in violations if v['M'] > 0]
    neg_M_violations = [v for v in violations if v['M'] <= 0]

    print(f"\n  Primes 11..{max_p}: {len(results)} tested")
    print(f"  Violations (W(p) <= W(p-1)): {len(violations)}")
    print(f"    with M(p) > 0:  {len(pos_M_violations)}")
    print(f"    with M(p) <= 0: {len(neg_M_violations)}")

    if neg_M_violations:
        print("\n  !!! SIGN THEOREM COUNTEREXAMPLES (M <= 0 but W decreased):")
        for v in neg_M_violations[:10]:
            print(f"      p={v['p']}, M={v['M']}, ratio={v['ratio']:.12f}")
    else:
        print("\n  >>> SIGN THEOREM CONFIRMED: all violations have M(p) > 0 <<<")

    if violations:
        print("\n  All violations:")
        for v in violations:
            print(f"    p={v['p']:5d}  M={v['M']:+3d}  ratio={v['ratio']:.12f}  "
                  f"excess={v['excess']:+.6e}")

    # Show transition zone
    print("\n  Transition zone (primes near first violation):")
    if first_violation:
        fp = first_violation['p']
        zone = [r for r in results if abs(r['p'] - fp) < 200]
    else:
        zone = results[-20:]
    for r in zone:
        marker = " ***" if not r['grew'] else ""
        print(f"    p={r['p']:5d}  M={r['M']:+3d}  excess={r['excess']:+.8e}{marker}")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 3: Analysis of excess dependence on p and M
# ═══════════════════════════════════════════════════════════════════════════════

def phase3_analysis(results_exact, results_float):
    print("\n" + "=" * 78)
    print("PHASE 3: Analysis of excess = W(p)/W(p-1) - 1")
    print("=" * 78)

    # Combine results (prefer exact where available)
    exact_primes = {r['p'] for r in results_exact}
    combined = list(results_exact)
    for r in results_float:
        if r['p'] not in exact_primes:
            combined.append(r)
    combined.sort(key=lambda r: r['p'])

    # 1. How does excess scale with p?
    print("\n  Excess vs p (log scale behavior):")
    import math
    for r in combined:
        if r['p'] in [11, 23, 47, 97, 199, 397, 503, 701, 997, 1009, 1201, 1399, 1499]:
            log_excess = math.log10(abs(r['excess'])) if r['excess'] != 0 else float('-inf')
            print(f"    p={r['p']:5d}  excess={r['excess']:+.8e}  "
                  f"log10|excess|={log_excess:.3f}  M={r['M']:+3d}")

    # 2. Positive-M primes vs negative-M primes
    pos_M = [r for r in combined if r['M'] > 0]
    neg_M = [r for r in combined if r['M'] <= 0]
    zero_M = [r for r in combined if r['M'] == 0]

    print(f"\n  Primes with M > 0:  {len(pos_M)}")
    print(f"  Primes with M <= 0: {len(neg_M)}")
    print(f"  Primes with M = 0:  {len(zero_M)}")

    if pos_M:
        pos_excesses = [r['excess'] for r in pos_M]
        print(f"    M>0  excess range: [{min(pos_excesses):.6e}, {max(pos_excesses):.6e}]")
        pos_violations = [r for r in pos_M if not r['grew']]
        print(f"    M>0  violations: {len(pos_violations)}")

    if neg_M:
        neg_excesses = [r['excess'] for r in neg_M]
        print(f"    M<=0 excess range: [{min(neg_excesses):.6e}, {max(neg_excesses):.6e}]")
        neg_violations = [r for r in neg_M if not r['grew']]
        print(f"    M<=0 violations: {len(neg_violations)}")

    # 3. Correlation between M and excess
    print("\n  Does larger |M| push excess negative?")
    # Group by M value
    from collections import defaultdict
    by_M = defaultdict(list)
    for r in combined:
        by_M[r['M']].append(r['excess'])

    print("    M value -> avg excess:")
    for m_val in sorted(by_M.keys()):
        vals = by_M[m_val]
        avg = sum(vals) / len(vals)
        print(f"      M={m_val:+3d}:  avg_excess={avg:+.6e}  (n={len(vals)})")

    # 4. Is the transition smooth or abrupt?
    print("\n  Smoothness analysis (running average of excess, window=5):")
    window = 5
    for i in range(0, len(combined) - window + 1, max(1, len(combined) // 20)):
        chunk = combined[i:i + window]
        avg_excess = sum(r['excess'] for r in chunk) / window
        p_range = f"{chunk[0]['p']}-{chunk[-1]['p']}"
        has_viol = any(not r['grew'] for r in chunk)
        marker = " ***" if has_viol else ""
        print(f"    primes {p_range:>12s}  avg_excess={avg_excess:+.8e}{marker}")


# ═══════════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("Universal Wobble Growth: W(p) > W(p-1) Investigation")
    print("=" * 78)
    print()

    # Phase 1: exact up to 500 (will be slow for large p, but correct)
    # Use a smaller limit if too slow
    exact_limit = 200  # Fraction arithmetic is O(n^2) per prime
    results_exact = phase1_exact(max_p=exact_limit)

    # Phase 2: float up to 1500
    results_float = phase2_float(max_p=1500)

    # Phase 3: combined analysis
    phase3_analysis(results_exact, results_float)

    print("\n" + "=" * 78)
    print("DONE")
    print("=" * 78)
