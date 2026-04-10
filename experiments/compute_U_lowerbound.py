#!/usr/bin/env python3
"""
Find the actual minimum of U_{p,m}/n^2 where n = p-m, over all primes p and 1 <= m <= p/2.
This tells us the constant c in U >= c*n^2 - lower_order.

Also: what's the minimum of U_{p,m} over all (p,m) with m <= p/2?
And the minimum of U_{p,m} - (p-2)?
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

# For m <= p/2, find min U/(p-m)^2 and min (U - (p-2))
print("For m <= p/2:")
min_ratio = float('inf')
min_ratio_case = None
min_excess = float('inf')
min_excess_case = None

for p in primes:
    for m in range(1, p//2 + 1):
        val = U(p, m)
        if val is None:
            continue
        n0 = p - m
        ratio = val / n0**2 if n0 > 0 else 0
        excess = val - (p - 2)
        if ratio < min_ratio:
            min_ratio = ratio
            min_ratio_case = (p, m, val, n0)
        if excess < min_excess:
            min_excess = excess
            min_excess_case = (p, m, val)

print(f"min U/n^2 = {min_ratio:.6f} at p={min_ratio_case[0]}, m={min_ratio_case[1]}, "
      f"U={min_ratio_case[2]}, n={min_ratio_case[3]}")
print(f"min (U-(p-2)) = {min_excess} at p={min_excess_case[0]}, m={min_excess_case[1]}, "
      f"U={min_excess_case[2]}")

# For m <= p/3:
print("\nFor m <= p/3:")
min_ratio = float('inf')
min_excess = float('inf')
for p in primes:
    for m in range(1, p//3 + 1):
        val = U(p, m)
        if val is None:
            continue
        n0 = p - m
        ratio = val / n0**2
        excess = val - (p - 2)
        if ratio < min_ratio:
            min_ratio = ratio
            min_ratio_case = (p, m, val, n0)
        if excess < min_excess:
            min_excess = excess
            min_excess_case = (p, m, val)

print(f"min U/n^2 = {min_ratio:.6f} at p={min_ratio_case[0]}, m={min_ratio_case[1]}")
print(f"min (U-(p-2)) = {min_excess} at p={min_excess_case[0]}, m={min_excess_case[1]}")

# For m <= p/4:
print("\nFor m <= p/4:")
min_ratio = float('inf')
min_excess = float('inf')
for p in primes:
    for m in range(1, p//4 + 1):
        val = U(p, m)
        if val is None:
            continue
        n0 = p - m
        ratio = val / n0**2
        excess = val - (p - 2)
        if ratio < min_ratio:
            min_ratio = ratio
            min_ratio_case = (p, m, val, n0)
        if excess < min_excess:
            min_excess = excess
            min_excess_case = (p, m, val)

print(f"min U/n^2 = {min_ratio:.6f} at p={min_ratio_case[0]}, m={min_ratio_case[1]}")
print(f"min (U-(p-2)) = {min_excess} at p={min_excess_case[0]}, m={min_excess_case[1]}")

# What's U_{p,m} for the WORST m ~ p/2?
print("\n\nU at m = floor(p/2) for small primes:")
for p in primes[:40]:
    m = p // 2
    val = U(p, m)
    if val is not None:
        n0 = p - m
        print(f"p={p}, m={m}: U={val}, n0={n0}, U/n0^2={val/n0**2:.4f}, U-(p-2)={val-(p-2)}")

# Check: for m = floor(p/2), is U always >= 0?
print("\n\nFor m = floor(p/2), is U >= 0?")
for p in primes:
    m = p // 2
    val = U(p, m)
    if val is not None and val < 0:
        print(f"  NEGATIVE: p={p}, m={m}, U={val}")

# Key computation: for m <= p/2, what's the smallest p where U >= p-2 always holds?
print("\n\nSmallest p where U_{p,m} >= p-2 for ALL m <= p/2:")
for p in primes:
    all_pass = True
    for m in range(1, p//2 + 1):
        val = U(p, m)
        if val is None or val < p - 2:
            all_pass = False
            break
    if all_pass:
        print(f"p = {p} PASSES")
        if p > 200:
            break
