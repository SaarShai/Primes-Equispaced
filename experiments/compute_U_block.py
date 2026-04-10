#!/usr/bin/env python3
"""
Compute U_{p,m} = sum_{t=0}^5 E_{m+t}(p-(m+t))
where E_r(n) = sum_{n/3 < v <= n/2} ([rv]_n - v)
and [rv]_n = rv mod n (least nonneg residue).

"Admissible" means m+t in {1,...,p-1} for t=0..5, i.e., 1 <= m and m+5 <= p-1,
so m in {1, ..., p-6}. But we also need n = p - (m+t) >= 1 for all t,
which gives m+5 <= p-1, same constraint.

We compute for small primes and ALL valid m.
"""

import sys
from math import floor

def E_r(r, n):
    """E_r(n) = sum_{n/3 < v <= n/2} ([rv]_n - v)"""
    if n <= 0:
        return 0
    total = 0
    lo = n // 3  # we want v > n/3, so v >= floor(n/3) + 1
    hi = n // 2  # we want v <= n/2, so v <= floor(n/2)
    for v in range(lo + 1, hi + 1):
        rv_mod_n = (r * v) % n
        total += rv_mod_n - v
    return total

def U(p, m):
    """U_{p,m} = sum_{t=0}^5 E_{m+t}(p-(m+t))"""
    total = 0
    for t in range(6):
        r = m + t
        n = p - r
        if n <= 0:
            return None  # invalid
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

# Compute for specific primes
test_primes = [p for p in range(7, 200) if is_prime(p)]

print("=" * 80)
print("U_{p,m} for small primes, all admissible m")
print("=" * 80)

min_cases = []  # track (p, m, U_val) where U is smallest

for p in test_primes:
    m_range = range(1, p - 5)  # m from 1 to p-6
    vals = []
    for m in m_range:
        val = U(p, m)
        if val is not None:
            vals.append((m, val))

    if not vals:
        continue

    min_val = min(v for _, v in vals)
    min_m = [m for m, v in vals if v == min_val]

    print(f"\np = {p}: min U = {min_val} at m = {min_m}, p-2 = {p-2}, "
          f"{'PASS' if min_val >= p-2 else 'FAIL'}")

    if min_val < p + 10:  # show interesting cases
        for m, v in vals:
            if v < p + 10:
                print(f"  m={m}: U={v} (U-(p-2)={v-(p-2)})")

    min_cases.append((p, min_val, min_m))

print("\n" + "=" * 80)
print("Summary: cases where min U is close to p-2")
print("=" * 80)
for p, min_val, min_m in min_cases:
    ratio = min_val / (p - 2) if p > 2 else float('inf')
    if ratio < 2.0:
        print(f"p={p}: min U={min_val}, p-2={p-2}, ratio={ratio:.4f}, m={min_m}")

print("\n" + "=" * 80)
print("Equality cases U = p-2:")
print("=" * 80)
for p, min_val, min_m in min_cases:
    if min_val == p - 2:
        print(f"p={p}, m={min_m}")

print("\n" + "=" * 80)
print("Extended computation to p=5000 (just checking min U >= p-2)")
print("=" * 80)
fail_count = 0
equality_cases = []
for p in range(7, 5001):
    if not is_prime(p):
        continue
    m_range = range(1, p - 5)
    min_val = float('inf')
    min_m_list = []
    for m in m_range:
        val = U(p, m)
        if val is not None:
            if val < min_val:
                min_val = val
                min_m_list = [m]
            elif val == min_val:
                min_m_list.append(m)

    if min_val < p - 2:
        print(f"FAIL: p={p}, min U={min_val}, p-2={p-2}, m={min_m_list}")
        fail_count += 1
    elif min_val == p - 2:
        equality_cases.append((p, min_m_list))

if fail_count == 0:
    print(f"ALL primes 7 <= p <= 5000 satisfy U >= p-2")
print(f"Equality cases: {equality_cases}")
