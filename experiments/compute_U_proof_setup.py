#!/usr/bin/env python3
"""
Setup for the proof of U_{p,m} >= p-2 for m <= p/2, p >= P0.

Strategy:
1. E_r(n) = sum_{n/3 < v <= n/2} (rv mod n - v)
2. For gcd(r,n)=1, use the identity:
   sum_{v in S} (rv mod n) = sum_{v in S} v + n * #{v in S : rv mod n < v} - ...

   Actually, let's use a cleaner approach.

   Write f(v) = rv mod n. For gcd(r,n)=1 and 0<v<n, f(v) = rv - n*floor(rv/n).
   So rv mod n - v = (r-1)v - n*floor(rv/n).

   E_r(n) = (r-1) * sum_{n/3<v<=n/2} v - n * sum_{n/3<v<=n/2} floor(rv/n)

   Let a = floor(n/3), b = floor(n/2).
   sum_{v=a+1}^b v = b(b+1)/2 - a(a+1)/2

   For the floor sum: sum_{v=a+1}^b floor(rv/n)

   By Hermite's formula or by the reciprocity of Dedekind sums,
   this can be related to s(r,n) = sum_{v=1}^{n-1} ((v/n)) ((rv/n))
   where ((x)) = x - floor(x) - 1/2 for x not integer, 0 otherwise.

   But this might be overcomplicating things.

   SIMPLER APPROACH for the lower bound:

   Since gcd(r,n)=1, the values {rv mod n : 1 <= v <= n-1} = {1,...,n-1}.
   Over the interval (n/3, n/2] of length ~n/6, the values rv mod n
   are "equidistributed" but not exactly uniform.

   Key: sum_{v=1}^{n-1} (rv mod n - v) = 0.
   So E_r(n) = -sum_{v not in (n/3,n/2]} (rv mod n - v).

   The complement has ~5n/6 terms.

   Actually, for the PROOF, the simplest approach:

   THEOREM: For p prime and 1 <= m <= (p-11)/2,
   U_{p,m} >= (p-m-5)^2/24 - 5(p-m)/2.

   This suffices since for p >= 289 and m <= (p-11)/2:
   (p-m-5)^2/24 - 5(p-m)/2 >= ((p-5)/2)^2/24 - 5p/2
   = (p-5)^2/96 - 5p/2 >= p^2/96 - 10p/96 - 5p/2 >= p-2
   when p >= 489 (roughly).

   Then verify p < 489 computationally.

   But wait: is the lower bound (p-m-5)^2/24 - error actually true?
   Let me check.
"""

from math import gcd

def E_r(r, n):
    if n <= 0:
        return 0
    total = 0
    lo = n // 3
    hi = n // 2
    for v in range(lo + 1, hi + 1):
        rv_mod_n = (r * v) % n
        total += rv_mod_n - v
    return total

def U(p, m):
    total = 0
    for t in range(6):
        r = m + t
        n = p - r
        if n <= 0:
            return None
        total += E_r(r, n)
    return total

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

primes = [p for p in range(7, 2001) if is_prime(p)]

# Test: is U >= n_min^2/72 - error for some reasonable error?
# n_min = p - m - 5 (smallest n in the block)
# Candidate lower bound: U >= (6/72) * n_min^2 = n_min^2/12
# or U >= n_min^2/12 - C*n_min for some C

print("Testing U >= n_min^2/C - D*n_min for m <= p/2:")
print("n_min = p - m - 5")

# Find the tightest C: max n_min^2 / U
worst_ratio = 0
worst_case = None
for p in primes:
    for m in range(1, p//2 + 1):
        val = U(p, m)
        if val is None or val <= 0:
            continue
        n_min = p - m - 5
        if n_min <= 0:
            continue
        ratio = n_min**2 / val
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_case = (p, m, val, n_min)

print(f"Worst n_min^2/U = {worst_ratio:.4f} at p={worst_case[0]}, m={worst_case[1]}, "
      f"U={worst_case[2]}, n_min={worst_case[3]}")
print(f"This means U >= n_min^2 / {worst_ratio:.1f}")

# Better: fit U >= a * n_min^2 + b * n_min + c
# For each (p,m) with m <= p/2, compute (n_min, U) pairs
import numpy as np

ns = []
us = []
for p in primes:
    for m in range(1, p//2 + 1):
        val = U(p, m)
        if val is None:
            continue
        n_min = p - m - 5
        if n_min > 0:
            ns.append(n_min)
            us.append(val)

ns = np.array(ns, dtype=float)
us = np.array(us, dtype=float)

# For the LOWER ENVELOPE: find the worst case U/n^2 for each n range
print("\nLower envelope by n_min ranges:")
for n_lo in range(0, 500, 20):
    n_hi = n_lo + 20
    mask = (ns >= n_lo) & (ns < n_hi)
    if mask.sum() > 0:
        min_u = us[mask].min()
        avg_ratio = (us[mask] / ns[mask]**2).min()
        print(f"  n_min in [{n_lo},{n_hi}): min U = {min_u:.0f}, min U/n^2 = {avg_ratio:.6f}")

# The empirical lower bound: what fraction of n^2 is the minimum U?
# For n_min >= 20, is U always >= n_min^2/200?
print("\n\nChecking U >= n_min^2/200 for n_min >= 6:")
violations = 0
for p in primes:
    for m in range(1, p//2 + 1):
        val = U(p, m)
        if val is None:
            continue
        n_min = p - m - 5
        if n_min >= 6:
            bound = n_min**2 / 200
            if val < bound:
                violations += 1
                if violations <= 20:
                    print(f"  VIOLATION: p={p}, m={m}, U={val}, n_min={n_min}, bound={bound:.1f}")
print(f"Total violations of U >= n^2/200: {violations}")

print("\n\nChecking U >= n_min^2/100 for n_min >= 6:")
violations = 0
for p in primes:
    for m in range(1, p//2 + 1):
        val = U(p, m)
        if val is None:
            continue
        n_min = p - m - 5
        if n_min >= 6:
            bound = n_min**2 / 100
            if val < bound:
                violations += 1
                if violations <= 10:
                    print(f"  VIOLATION: p={p}, m={m}, U={val}, n_min={n_min}, bound={bound:.1f}")
print(f"Total violations of U >= n^2/100: {violations}")

# Since avg E_r(n)/n^2 ~ 1/72, and we have 6 terms, avg U/n^2 ~ 6/72 = 1/12 ~ 0.083
# The minimum is around 0.01 for n near p/2, but that's at m = p/2 where r ~ p/2.
# For m small, U/n^2 is around 0.08-0.12.
# The problem is for m ~ p/2 where both r and n are ~ p/2.

# Let's check: E_r(n) when r ~ n
print("\n\nE_r(n) for r close to n:")
for n in [20, 50, 100]:
    print(f"\nn = {n}:")
    for r in range(max(1, n-10), n):
        if gcd(r, n) == 1:
            e = E_r(r, n)
            print(f"  r={r}: E_r(n)={e}, E_r/n^2={e/n**2:.6f}")
    # Also r = n-1 (which is the Dedekind "reciprocal" case)
    r = n - 1
    if gcd(r, n) == 1:
        e = E_r(r, n)
        print(f"  r=n-1={r}: E_r(n)={e} (this is the 'complementary' case)")

# E_{n-1}(n): rv mod n = (n-1)v mod n = n - v (for 0 < v < n)
# So E_{n-1}(n) = sum_{n/3 < v <= n/2} ((n-v) - v) = sum (n - 2v)
# = |I|*n - 2*sum v where |I| ~ n/6
# ~ (n/6)*n - 2*(5n^2/72) = n^2/6 - 10n^2/72 = n^2(12-10)/72 = 2n^2/72 = n^2/36
print("\n\nE_{n-1}(n) analytical check:")
for n in [20, 50, 100, 200]:
    a = n // 3
    b = n // 2
    num_terms = b - a
    sum_v = b*(b+1)//2 - a*(a+1)//2
    predicted = num_terms * n - 2 * sum_v  # E_{n-1}(n)
    actual = E_r(n-1, n)
    print(f"  n={n}: predicted={predicted}, actual={actual}, n^2/36={n**2/36:.1f}")
