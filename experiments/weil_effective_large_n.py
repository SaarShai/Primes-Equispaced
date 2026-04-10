#!/usr/bin/env python3
"""
Large-n scan to determine the true scaling of max|Sigma(m,n)|.
Focus on worst-case m near n/2.
"""
import math

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
        e = E_r(r, n)
        i = I_r(r)
        total += e - n * n * i
    return total

# Test larger n but only check worst-case region m ~ n/2
# The worst m is always near n/2, so focus there

print("n        worst_m   max|Sigma|     /n        /n^1.5      /n^2        /(n*sqrt(n/2))  /n*log(n)")
print("-" * 110)

for n in [100, 200, 500, 1000, 2000, 3000, 5000, 7000]:
    max_abs = 0
    worst_m = 0
    # Only scan m near n/2 where the worst case lives
    k_start = max(0, (n // 2 - 60) // 6)
    k_end = n // 12 + 1
    for k in range(0, k_end):
        m = 6 * k + 2
        if m + 5 > n:
            break
        sig = six_term_error(m, n)
        if abs(sig) > max_abs:
            max_abs = abs(sig)
            worst_m = m

    ratio_n = max_abs / n
    ratio_n32 = max_abs / (n ** 1.5)
    ratio_n2 = max_abs / (n ** 2)
    ratio_nsqrtn2 = max_abs / (n * math.sqrt(n / 2))
    ratio_nlogn = max_abs / (n * math.log(n))
    print(f"{n:>6}   {worst_m:>6}   {max_abs:>12.2f}   {ratio_n:>8.4f}   {ratio_n32:>10.6f}  {ratio_n2:>10.8f}   {ratio_nsqrtn2:>12.6f}    {ratio_nlogn:>8.4f}")

# Also check the actual growth of C(m) = lim |Sigma(m,n)|/n for fixed m
print("\n\nC(m) estimates from n=5000:")
n = 5000
print(f"{'m':>6} {'|Sigma|/n':>12} {'sqrt(m)':>8} {'|Sig|/(n*sqrt(m))':>18}")
for k in range(0, 50):
    m = 6 * k + 2
    if m + 5 > n:
        break
    sig = six_term_error(m, n)
    ratio = abs(sig) / n
    sqm = math.sqrt(m)
    ratio2 = abs(sig) / (n * sqm) if m > 0 else 0
    if k < 20 or k % 5 == 0:
        print(f"{m:>6} {ratio:>12.4f} {sqm:>8.2f} {ratio2:>18.6f}")
