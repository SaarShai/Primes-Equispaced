#!/usr/bin/env python3
"""
Focused scaling test: is max|Sigma| ~ n^{3/2}*log(n)?
Or is it n^{3/2}*sqrt(log(n))? Or just n^{3/2}?

Also: for the APPLICATION we need |Sigma(m, p-m)| not worst case.
The worst m is always near n/2, but in the application m ranges from 2 to p/2,
and n = p - m, so worst case is m ~ p/2 => n ~ p/2.

Key test: what is |Sigma(m, p-m)| / p^{3/2} when maximized over m for actual primes?
"""
import math

def E_r(r, n):
    if n <= 0:
        return 0
    total = 0
    lo = n // 3
    hi = n // 2
    for v in range(lo + 1, hi + 1):
        total += (r * v) % n - v
    return total

def B2(t):
    return t*t - t + 1.0/6.0

def I_r(r):
    frac_r2 = (r / 2.0) - math.floor(r / 2.0)
    frac_r3 = (r / 3.0) - math.floor(r / 3.0)
    return 1.0/72.0 + (B2(frac_r2) - B2(frac_r3)) / (2.0 * r)

def six_term_error(m, n):
    total = 0.0
    for t in range(6):
        r = m + t
        total += E_r(r, n) - n * n * I_r(r)
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

# Test: for fixed m, the worst n gives |Sigma| ~ C(m) * n
# and C(m) ~ A * sqrt(m).
# So max over m of |Sigma(m,n)| / n = max C(m) for m<=n/2 ~ A*sqrt(n/2)
# => max|Sigma| ~ A * sqrt(n/2) * n = A/sqrt(2) * n^{3/2}
# This should give a STABLE C_eff if C(m) ~ A*sqrt(m).

# But C(m) values oscillate wildly. Let's check the ENVELOPE.

print("=== C(m) = |Sigma(m,5000)|/5000 for m up to 2498 ===")
print("Checking if envelope(C(m)) ~ sqrt(m)...")
n = 5000
max_C_so_far = 0
envelope_data = []
for k in range(0, n // 12 + 1):
    m = 6 * k + 2
    if m + 5 > n:
        break
    sig = abs(six_term_error(m, n))
    C_m = sig / n
    if C_m > max_C_so_far:
        max_C_so_far = C_m
        envelope_data.append((m, C_m))

print(f"{'m':>6} {'C(m)':>10} {'C/sqrt(m)':>10} {'C/m^0.4':>10} {'C/log(m)':>10}")
for m, C in envelope_data:
    sqm = math.sqrt(m)
    print(f"{m:>6} {C:>10.4f} {C/sqm:>10.4f} {C/m**0.4:>10.4f} {C/math.log(m) if m>1 else 0:>10.4f}")

# For the APPLICATION: what matters is the positivity test
# U_{p,m} ~ n^2/12 - |Sigma(m,n)| - O(n) > 0
# where n = p - m
# The critical case is large m (late q=1 tail) where n is small

print("\n\n=== APPLICATION: Positivity check for actual U_{p,m} ===")
print("For primes p, compute min over m of (U_{p,m}/p^2)")
print("where U_{p,m} = sum_{t=0}^5 E_{m+t}(p-m-t)\n")

def U_pm(p, m):
    total = 0
    for t in range(6):
        r = m + t
        n = p - r
        if n <= 0:
            return None
        total += E_r(r, n)
    return total

test_primes = [p for p in range(500, 5001) if is_prime(p)]
# Sample every 10th prime
sample = test_primes[::10]

print(f"{'p':>6} {'min U/p^2':>12} {'worst_m':>8} {'min_U':>12} {'margin':>10}")
for p in sample[:20]:
    min_U = float('inf')
    worst_m = 0
    for k in range(0, (p - 7) // 6 + 1):
        m = 6 * k + 2
        if m + 5 >= p:
            break
        u = U_pm(p, m)
        if u is not None and u < min_U:
            min_U = u
            worst_m = m
    margin = min_U / p**2 if min_U != float('inf') else 0
    print(f"{p:>6} {margin:>12.6f} {worst_m:>8} {min_U:>12} {'OK' if min_U > 0 else 'FAIL!':>10}")

# Now the key: effective bound computation
# For the proof: we need C such that |Sigma(m,n)| <= C * n * sqrt(m) for all m,n.
# From data: C ~ 2-3 but with outliers.

print("\n\n=== EFFECTIVE BOUND: max |Sigma(m,n)| / (n * sqrt(m)) over all m ===")
for n in [500, 1000, 2000, 5000]:
    max_ratio = 0
    worst_m = 0
    for k in range(0, n // 12 + 1):
        m = 6 * k + 2
        if m + 5 > n:
            break
        sig = abs(six_term_error(m, n))
        ratio = sig / (n * math.sqrt(m))
        if ratio > max_ratio:
            max_ratio = ratio
            worst_m = m
    print(f"  n={n:>5}: max|Sig|/(n*sqrt(m)) = {max_ratio:.4f} at m={worst_m}")

# Check: worst m near n/2 gives ratio ~ 2.5
# For m=2: ratio ~ 2.2 (inflated by small m)
# Overall: the constant A ~ 2.5 seems reasonable

print("\n\n=== EFFECTIVE BOUND (excluding m<20): max |Sigma(m,n)| / (n * sqrt(m)) ===")
for n in [500, 1000, 2000, 5000]:
    max_ratio = 0
    worst_m = 0
    for k in range(3, n // 12 + 1):  # m >= 20
        m = 6 * k + 2
        if m + 5 > n:
            break
        sig = abs(six_term_error(m, n))
        ratio = sig / (n * math.sqrt(m))
        if ratio > max_ratio:
            max_ratio = ratio
            worst_m = m
    print(f"  n={n:>5}: max|Sig|/(n*sqrt(m)) = {max_ratio:.4f} at m={worst_m}")
