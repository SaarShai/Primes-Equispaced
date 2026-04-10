#!/usr/bin/env python3
"""
For each prime p, find the maximum m_max such that U_{p,m} >= p-2 for all 1 <= m <= m_max.
Also check: for fixed small m (like m=1,2), does U always exceed p-2 for large p?
"""

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

primes = [p for p in range(7, 1001) if is_prime(p)]

# For each p, find max m such that U_{p,m'} >= p-2 for ALL m' in 1..m
print("=" * 70)
print("Max m_max such that U_{p,m} >= p-2 for all 1 <= m <= m_max")
print("=" * 70)
for p in primes:
    m_max = 0
    for m in range(1, p - 5):
        val = U(p, m)
        if val is None or val < p - 2:
            break
        m_max = m
    ratio = m_max / p if p > 0 else 0
    if p <= 200 or m_max == 0:
        print(f"p={p}: m_max={m_max}, ratio={ratio:.4f}")

# For fixed m, find min p where U >= p-2
print("\n" + "=" * 70)
print("For fixed m, U_{p,m} vs p-2:")
print("=" * 70)
for m_fixed in [1, 2, 3, 4, 5]:
    print(f"\nm = {m_fixed}:")
    for p in primes:
        if p <= m_fixed + 5:
            continue
        val = U(p, m_fixed)
        if val is not None:
            status = "PASS" if val >= p - 2 else "FAIL"
            if p <= 100 or status == "FAIL":
                print(f"  p={p}: U={val}, p-2={p-2}, {status}")

# Growth analysis: U_{p,1} and U_{p,2} vs p^2
print("\n" + "=" * 70)
print("Growth: U_{p,m}/p^2 for m=1,2")
print("=" * 70)
for m_fixed in [1, 2]:
    print(f"\nm = {m_fixed}:")
    for p in primes[:30]:
        if p <= m_fixed + 5:
            continue
        val = U(p, m_fixed)
        if val is not None:
            print(f"  p={p}: U/p^2 = {val/p**2:.6f}")
