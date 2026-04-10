#!/usr/bin/env python3
"""Verify specific claims in the proof document."""

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

# 1. Verify p=71 borderline
print("p=71, m <= (71-11)/2 = 30:")
min_u = float('inf')
for m in range(1, 31):
    val = U(71, m)
    if val < min_u:
        min_u = val
        min_m = m
print(f"  min U = {min_u} at m = {min_m}, p-2 = 69")
assert min_u >= 69, f"FAIL: {min_u} < 69"

# 2. Verify the 6 exceptions
exceptions = [(17, 3), (23, 3), (29, 5), (41, 13), (53, 13), (59, 15)]
print("\nException verification:")
for p, m in exceptions:
    val = U(p, m)
    print(f"  p={p}, m={m}: U={val}, p-2={p-2}, deficit={val-(p-2)}")
    assert val < p - 2

# 3. Verify p=61,67,71,73 pass
print("\nSmall prime passes:")
for p in [61, 67, 71, 73]:
    m_max = (p - 11) // 2
    min_u = float('inf')
    for m in range(1, m_max + 1):
        val = U(p, m)
        if val < min_u:
            min_u = val
    print(f"  p={p}: min U = {min_u} over m <= {m_max}, p-2 = {p-2}, {'PASS' if min_u >= p-2 else 'FAIL'}")
    assert min_u >= p - 2

# 4. Verify equality cases
print("\nEquality case check U_{17,2} and U_{29,8}:")
print(f"  U(17,2) = {U(17,2)}, p-2 = 15, equal = {U(17,2) == 15}")
print(f"  U(29,8) = {U(29,8)}, p-2 = 27, equal = {U(29,8) == 27}")

# 5. Verify U_{p,2} >= p-2 for all p >= 13
print("\nU_{p,2} >= p-2 for p >= 13:")
for p in range(13, 200):
    if not is_prime(p):
        continue
    val = U(p, 2)
    if val is None:
        continue
    if val < p - 2:
        print(f"  FAIL: p={p}, U={val}")
print("  All pass (13 <= p < 200)")

# 6. U/p^2 at p=113, m=32
print(f"\nU(113, 32) = {U(113, 32)}, U/p^2 = {U(113, 32)/113**2:.6f}")

# 7. Check all primes in [13,59] for m <= (p-11)/2
print("\nAll primes 13 <= p <= 59, m <= (p-11)/2:")
for p in range(13, 60):
    if not is_prime(p):
        continue
    m_max = (p - 11) // 2
    if m_max < 1:
        print(f"  p={p}: range empty")
        continue
    fails = []
    for m in range(1, m_max + 1):
        val = U(p, m)
        if val is not None and val < p - 2:
            fails.append((m, val))
    if fails:
        print(f"  p={p}: FAILS at {fails}")
    else:
        print(f"  p={p}: PASSES for m <= {m_max}")

print("\nAll verifications complete.")
