#!/usr/bin/env python3
"""
Find the exact threshold P0 such that for all primes p >= P0,
U_{p,m} >= p-2 for all 1 <= m <= (p-11)/2.

Also find all exceptions for p < P0.
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

primes = [p for p in range(7, 5001) if is_prime(p)]

# For each prime, check if U >= p-2 for ALL m in {1,...,floor((p-11)/2)}
# This ensures n = p-m-5 >= (p+1)/2 > p/2 - 3, so n >= p/2 - 2.
# Actually n = p - m - t >= p - (p-11)/2 - 5 = (p+1)/2 >= p/2.

print("Checking U >= p-2 for m <= (p-11)/2")
print("=" * 60)

last_fail = 0
fail_primes = []
all_pass_start = None

for p in primes:
    m_max = (p - 11) // 2
    if m_max < 1:
        continue

    failed = False
    worst_m = None
    worst_val = float('inf')

    for m in range(1, m_max + 1):
        val = U(p, m)
        if val is None or val < p - 2:
            failed = True
            if val is not None and val < worst_val:
                worst_val = val
                worst_m = m

    if failed:
        last_fail = p
        fail_primes.append((p, worst_m, worst_val))
        if p <= 200:
            print(f"FAIL: p={p}, worst m={worst_m}, U={worst_val}, p-2={p-2}")
    else:
        if all_pass_start is None and p > last_fail:
            # Check if this could be the start
            pass

print(f"\nLast failing prime: {last_fail}")
print(f"\nAll failing primes:")
for p, m, v in fail_primes:
    print(f"  p={p}: m={m}, U={v}, deficit={v-(p-2)}")

# Find first prime after which ALL subsequent primes pass
print(f"\nChecking consecutive passes from p=67:")
consecutive_passes = 0
first_all_pass = None
for p in primes:
    m_max = (p - 11) // 2
    if m_max < 1:
        continue

    passed = True
    for m in range(1, m_max + 1):
        val = U(p, m)
        if val is None or val < p - 2:
            passed = False
            break

    if passed:
        consecutive_passes += 1
        if first_all_pass is None:
            first_all_pass = p
    else:
        consecutive_passes = 0
        first_all_pass = None

    if consecutive_passes >= 50:
        print(f"50 consecutive passes starting from p={first_all_pass}")
        break

# Now check with m <= p/2 (slightly wider range)
print("\n\nChecking U >= p-2 for m <= p/2 (wider range)")
last_fail2 = 0
fail_primes2 = []
for p in primes:
    m_max = p // 2
    if m_max < 1:
        continue

    failed = False
    worst_m = None
    worst_val = float('inf')

    for m in range(1, m_max + 1):
        val = U(p, m)
        if val is None or val < p - 2:
            failed = True
            if val is not None and val < worst_val:
                worst_val = val
                worst_m = m

    if failed:
        last_fail2 = p
        fail_primes2.append((p, worst_m, worst_val))

print(f"Last failing prime (m <= p/2): {last_fail2}")
print(f"Failing primes:")
for p, m, v in fail_primes2:
    print(f"  p={p}: m={m}, U={v}, deficit={v-(p-2)}")

# Exact threshold: first prime such that ALL primes >= it pass
consecutive = 0
threshold = None
for p in primes:
    m_max = p // 2
    passed = True
    for m in range(1, m_max + 1):
        val = U(p, m)
        if val is None or val < p - 2:
            passed = False
            break
    if passed:
        consecutive += 1
        if threshold is None:
            threshold = p
    else:
        consecutive = 0
        threshold = None

    if consecutive >= 100:
        print(f"\nThreshold (m <= p/2): ALL primes >= {threshold} pass (verified 100 consecutive)")
        break
