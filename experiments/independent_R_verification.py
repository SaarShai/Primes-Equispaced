#!/usr/bin/env python3
"""
Independent verification of the claim |R(p)| = O(log p / p).

Definitions (from the claim):
- F_{n} = Farey sequence of order n = {a/b : 0 <= a <= b <= n, gcd(a,b)=1}, sorted
- rank(x in F_n) = position of x in F_n (0-indexed from 0/1)
- D(a/b) = rank(a/b in F_{p-1}) - |F_{p-1}| * (a/b)   [Farey displacement]
- delta(a/b) = (a - p*a mod b) / b                       [multiplicative shift]
- C(p,b) = sum over a=1..b-1, gcd(a,b)=1 of D(a/b) * delta(a/b)
- V(b)   = sum over a=1..b-1, gcd(a,b)=1 of delta(a/b)^2
- R(p)   = sum_{b=2}^{p-1} C(p,b) / sum_{b=2}^{p-1} V(b)

We compute R(p) exactly using Fraction arithmetic for all primes up to 97.

Author: Independent verification agent
Date: 2026-03-29
"""

from fractions import Fraction
from math import gcd, log, sqrt
import sys

def farey_sequence(n):
    """Generate Farey sequence F_n as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, n + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def farey_rank_map(n):
    """Return dict mapping each fraction in F_n to its 0-based rank."""
    seq = farey_sequence(n)
    return {f: i for i, f in enumerate(seq)}

def farey_size(n):
    """Return |F_n|."""
    count = 0
    for b in range(1, n + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                count += 1
    return count

def compute_delta(a, b, p):
    """
    delta(a/b) = (a - p*a mod b) / b
    Here 'p*a mod b' is taken in range [0, b-1].
    """
    pa_mod_b = (p * a) % b
    return Fraction(a - pa_mod_b, b)

def compute_R(p):
    """Compute R(p) exactly using Fraction arithmetic."""
    n = p - 1  # Farey order

    # Build Farey sequence and rank map
    rank_map = farey_rank_map(n)
    F_size = Fraction(len(rank_map))

    total_C = Fraction(0)
    total_V = Fraction(0)

    for b in range(2, p):
        for a in range(1, b):
            if gcd(a, b) != 1:
                continue

            frac = Fraction(a, b)

            # D(a/b) = rank(a/b in F_{p-1}) - |F_{p-1}| * (a/b)
            if frac not in rank_map:
                # a/b with b <= p-1 should be in F_{p-1}
                # But if b > p-1, it won't be. Let's check.
                # Since b ranges 2..p-1 and a < b with gcd(a,b)=1,
                # we have b <= p-1, so a/b IS in F_{p-1}.
                raise ValueError(f"{a}/{b} not in F_{n}!")

            D = Fraction(rank_map[frac]) - F_size * frac
            delta = compute_delta(a, b, p)

            total_C += D * delta
            total_V += delta * delta

    if total_V == 0:
        return None, total_C, total_V

    R = total_C / total_V
    return R, total_C, total_V

def dedekind_sum(h, k):
    """
    Classical Dedekind sum s(h,k) = sum_{r=1}^{k-1} ((r/k)) * ((hr/k))
    where ((x)) = x - floor(x) - 1/2 if x not integer, 0 if x integer.
    """
    s = Fraction(0)
    for r in range(1, k):
        x1 = Fraction(r, k)
        x2 = Fraction(h * r % k, k)

        # ((x)) for x1
        if x1.denominator == 1:  # integer
            saw1 = Fraction(0)
        else:
            saw1 = x1 - int(x1) - Fraction(1, 2)

        # ((x)) for x2
        if x2 == 0:
            saw2 = Fraction(0)
        else:
            saw2 = x2 - int(x2) - Fraction(1, 2)

        s += saw1 * saw2
    return s

def mobius(n):
    """Mobius function mu(n)."""
    if n == 1:
        return 1
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            temp //= d
            if temp % d == 0:
                return 0  # squared factor
        d += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)

def divisors(n):
    """Return all divisors of n."""
    divs = []
    for i in range(1, n + 1):
        if n % i == 0:
            divs.append(i)
    return divs

def verify_dedekind_relation(p, b):
    """
    Check if C(p,b) = sum_{d|b} mu(d) * s(p, b/d).
    Returns (C_computed, dedekind_sum_formula, match).
    """
    n = p - 1
    rank_map = farey_rank_map(n)
    F_size = Fraction(len(rank_map))

    # Compute C(p,b) directly
    C = Fraction(0)
    for a in range(1, b):
        if gcd(a, b) != 1:
            continue
        frac = Fraction(a, b)
        if frac not in rank_map:
            continue
        D = Fraction(rank_map[frac]) - F_size * frac
        delta = compute_delta(a, b, p)
        C += D * delta

    # Compute sum_{d|b} mu(d) * s(p, b/d)
    ds_formula = Fraction(0)
    for d in divisors(b):
        mu_d = mobius(d)
        if mu_d == 0:
            continue
        ds_formula += mu_d * dedekind_sum(p, b // d)

    return C, ds_formula, C == ds_formula

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# ============================================================
# MAIN COMPUTATION
# ============================================================

primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

print("=" * 90)
print("INDEPENDENT VERIFICATION: |R(p)| = O(log p / p)")
print("=" * 90)
print()

results = []

print(f"{'p':>4} | {'R(p) (decimal)':>20} | {'|R(p)|':>14} | {'|R|*p/log(p)':>14} | {'|R|*p':>14} | {'|R|*sqrt(p)':>14}")
print("-" * 90)

for p in primes:
    R, C_total, V_total = compute_R(p)
    if R is None:
        print(f"{p:>4} | {'V=0, undefined':>20} | {'N/A':>14} | {'N/A':>14} | {'N/A':>14} | {'N/A':>14}")
        continue

    R_float = float(R)
    abs_R = abs(R_float)
    ratio_log = abs_R * p / log(p)
    ratio_p = abs_R * p
    ratio_sqrt = abs_R * sqrt(p)

    results.append({
        'p': p,
        'R': R,
        'R_float': R_float,
        'abs_R': abs_R,
        'ratio_log': ratio_log,
        'ratio_p': ratio_p,
        'ratio_sqrt': ratio_sqrt,
        'C_total': C_total,
        'V_total': V_total,
    })

    print(f"{p:>4} | {R_float:>20.12f} | {abs_R:>14.10f} | {ratio_log:>14.8f} | {ratio_p:>14.8f} | {ratio_sqrt:>14.8f}")

print()
print("=" * 90)
print("ANALYSIS")
print("=" * 90)

if results:
    ratio_logs = [r['ratio_log'] for r in results]
    ratio_ps = [r['ratio_p'] for r in results]
    ratio_sqrts = [r['ratio_sqrt'] for r in results]

    print(f"\n|R(p)| * p / log(p):")
    print(f"  min = {min(ratio_logs):.8f}")
    print(f"  max = {max(ratio_logs):.8f}")
    print(f"  first 5 values: {[f'{x:.6f}' for x in ratio_logs[:5]]}")
    print(f"  last 5 values:  {[f'{x:.6f}' for x in ratio_logs[-5:]]}")

    # Check if growing or bounded
    if ratio_logs[-1] > 2 * ratio_logs[0]:
        print("  => GROWING: inconsistent with O(log p / p)")
    else:
        print("  => Appears BOUNDED: consistent with O(log p / p)")

    print(f"\n|R(p)| * p:")
    print(f"  min = {min(ratio_ps):.8f}")
    print(f"  max = {max(ratio_ps):.8f}")
    print(f"  first 5 values: {[f'{x:.6f}' for x in ratio_ps[:5]]}")
    print(f"  last 5 values:  {[f'{x:.6f}' for x in ratio_ps[-5:]]}")

    if ratio_ps[-1] > 2 * ratio_ps[0]:
        print("  => GROWING: |R(p)| decays slower than O(1/p)")
    else:
        print("  => Appears BOUNDED: consistent with O(1/p) or faster")

    print(f"\n|R(p)| * sqrt(p):")
    print(f"  min = {min(ratio_sqrts):.8f}")
    print(f"  max = {max(ratio_sqrts):.8f}")
    print(f"  first 5 values: {[f'{x:.6f}' for x in ratio_sqrts[:5]]}")
    print(f"  last 5 values:  {[f'{x:.6f}' for x in ratio_sqrts[-5:]]}")

    if ratio_sqrts[-1] > 2 * ratio_sqrts[0]:
        print("  => GROWING: |R(p)| decays slower than O(1/sqrt(p))")
    else:
        print("  => Appears BOUNDED: consistent with O(1/sqrt(p)) or faster")

# ============================================================
# DEDEKIND SUM RELATION CHECK for p=13
# ============================================================

print()
print("=" * 90)
print("DEDEKIND SUM RELATION CHECK: p = 13, b = 2..12")
print("=" * 90)
print()
print(f"Checking: C(13, b) =? sum_{{d|b}} mu(d) * s(13, b/d)")
print()
print(f"{'b':>3} | {'C(13,b)':>30} | {'Dedekind formula':>30} | {'Match?':>6}")
print("-" * 75)

all_match = True
for b in range(2, 13):
    C_val, ds_val, match = verify_dedekind_relation(13, b)
    all_match = all_match and match
    C_str = str(C_val) if len(str(C_val)) <= 28 else f"{float(C_val):.10f}"
    ds_str = str(ds_val) if len(str(ds_val)) <= 28 else f"{float(ds_val):.10f}"
    print(f"{b:>3} | {C_str:>30} | {ds_str:>30} | {'YES' if match else 'NO':>6}")

print()
if all_match:
    print("ALL MATCH: The Dedekind sum relation holds exactly for p=13, b=2..12.")
else:
    print("MISMATCH FOUND: The Dedekind sum relation does NOT hold for all b.")

# ============================================================
# DETAILED EXACT VALUES
# ============================================================

print()
print("=" * 90)
print("EXACT R(p) VALUES (as fractions)")
print("=" * 90)
print()
for r in results:
    print(f"p = {r['p']:>3}: R(p) = {r['R']}")
    print(f"         C_total = {r['C_total']}")
    print(f"         V_total = {r['V_total']}")
    print()
