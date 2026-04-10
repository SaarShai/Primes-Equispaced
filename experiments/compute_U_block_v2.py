#!/usr/bin/env python3
"""
Investigate: for which (p,m) pairs does U_{p,m} >= p-2?
Maybe "admissible" has a restricted meaning.
Check: m=2 only? m in specific residue classes? m <= sqrt(p)?
"""

from math import floor, sqrt

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

primes = [p for p in range(7, 501) if is_prime(p)]

# Check 1: For m=2 (the claimed equality case at (17,2))
print("=" * 60)
print("U_{p,2} for primes:")
print("=" * 60)
for p in primes[:30]:
    val = U(p, 2)
    if val is not None:
        print(f"p={p}: U={val}, p-2={p-2}, diff={val-(p-2)}")
    else:
        print(f"p={p}: U=None (invalid)")

# Check 2: For each p, find ALL m where U >= p-2
print("\n" + "=" * 60)
print("m values where U_{p,m} >= p-2:")
print("=" * 60)
for p in primes[:30]:
    good_m = []
    for m in range(1, p-5):
        val = U(p, m)
        if val is not None and val >= p - 2:
            good_m.append((m, val))
    if good_m:
        print(f"p={p}: {good_m}")
    else:
        print(f"p={p}: NONE")

# Check 3: Maybe the definition of E_r is different?
# Try E_r(n) = sum_{1 <= v <= n/2} instead of n/3 < v <= n/2
print("\n" + "=" * 60)
print("Alternative: E_r(n) = sum_{1 <= v <= n/2} ([rv]_n - v)")
print("=" * 60)

def E_r_alt(r, n):
    if n <= 0:
        return 0
    total = 0
    hi = n // 2
    for v in range(1, hi + 1):
        rv_mod_n = (r * v) % n
        total += rv_mod_n - v
    return total

def U_alt(p, m):
    total = 0
    for t in range(6):
        r = m + t
        n = p - r
        if n <= 0:
            return None
        total += E_r_alt(r, n)
    return total

for p in primes[:20]:
    vals = []
    for m in range(1, p-5):
        val = U_alt(p, m)
        if val is not None:
            vals.append((m, val))
    if vals:
        min_val = min(v for _, v in vals)
        min_m = [m for m, v in vals if v == min_val]
        print(f"p={p}: min U_alt={min_val} at m={min_m}, p-2={p-2}, "
              f"{'PASS' if min_val >= p-2 else 'FAIL'}")

# Check 4: Maybe E_r(n) = sum_{v=1}^{n-1} {rv/n} (fractional part sum)?
print("\n" + "=" * 60)
print("Alternative: E_r(n) = sum_{v=1}^{n-1} {rv/n} = (n-gcd(r,n))/2")
print("(Ramanujan/Dedekind sum related)")
print("=" * 60)

from math import gcd

def E_r_frac(r, n):
    """sum_{v=1}^{n-1} {rv/n} = (n - gcd(r,n))/2"""
    if n <= 0:
        return 0
    return (n - gcd(r, n)) / 2

def U_frac(p, m):
    total = 0
    for t in range(6):
        r = m + t
        n = p - r
        if n <= 0:
            return None
        total += E_r_frac(r, n)
    return total

for p in primes[:30]:
    vals = []
    for m in range(1, p-5):
        val = U_frac(p, m)
        if val is not None:
            vals.append((m, val))
    if vals:
        min_val = min(v for _, v in vals)
        min_m = [m for m, v in vals if v == min_val]
        print(f"p={p}: min U_frac={min_val} at m={min_m}, p-2={p-2}, "
              f"{'PASS' if min_val >= p-2 else 'FAIL'}")

# Check 5: Maybe U is sum of |E_r| (absolute values)?
print("\n" + "=" * 60)
print("Alternative: U = sum |E_r(n)|")
print("=" * 60)

def U_abs(p, m):
    total = 0
    for t in range(6):
        r = m + t
        n = p - r
        if n <= 0:
            return None
        total += abs(E_r(r, n))
    return total

for p in primes[:30]:
    vals = []
    for m in range(1, p-5):
        val = U_abs(p, m)
        if val is not None:
            vals.append((m, val))
    if vals:
        min_val = min(v for _, v in vals)
        min_m = [m for m, v in vals if v == min_val]
        print(f"p={p}: min |U|={min_val} at m={min_m}, p-2={p-2}, "
              f"{'PASS' if min_val >= p-2 else 'FAIL'}")

# Check 6: Maybe admissible means m ≡ 2 mod 6?
print("\n" + "=" * 60)
print("Restricted to m ≡ 2 mod 6:")
print("=" * 60)
for p in primes[:30]:
    vals = []
    for m in range(2, p-5, 6):
        val = U(p, m)
        if val is not None:
            vals.append((m, val))
    if vals:
        min_val = min(v for _, v in vals)
        min_m = [m for m, v in vals if v == min_val]
        print(f"p={p}: min U={min_val} at m={min_m}, p-2={p-2}, "
              f"{'PASS' if min_val >= p-2 else 'FAIL'}")

# Check 7: Maybe "admissible" means gcd(m, p) = 1 AND m <= p/3?
print("\n" + "=" * 60)
print("Restricted to gcd(m,p)=1 AND m <= p/3:")
print("=" * 60)
for p in primes[:30]:
    vals = []
    for m in range(1, p//3 + 1):
        if gcd(m, p) == 1:
            val = U(p, m)
            if val is not None:
                vals.append((m, val))
    if vals:
        min_val = min(v for _, v in vals)
        min_m = [m for m, v in vals if v == min_val]
        print(f"p={p}: min U={min_val} at m={min_m}, p-2={p-2}, "
              f"{'PASS' if min_val >= p-2 else 'FAIL'}")
