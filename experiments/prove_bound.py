#!/usr/bin/env python3
"""
PROVING the lower bound E_r(n) >= -n^2/24 - n for gcd(r,n)=1.

For r = 3, n even: v in (n/3, n/2].
3v ranges from n+3 to 3n/2. So 3v mod n ranges from 3 to n/2.
E_3(n) = sum_{n/3<v<=n/2} (3v mod n - v) = sum (3v - n - v) = sum (2v - n)
       = 2 * sum v - |I| * n where |I| = n/6.
sum v = (n/6)(5n/12) approximately.
E_3(n) ~ 2*(n/6)*(5n/12) - (n/6)*n = (n/6)(10n/12 - n) = (n/6)(10n/12 - 12n/12) = (n/6)(-2n/12) = -n^2/36

Wait but the data says E_3/n^2 ~ -0.028 ~ -1/36 for large even n. Let me verify.

Actually, for n divisible by 6, n = 6k:
a = 2k, b = 3k. v ranges from 2k+1 to 3k. That's k terms.
3v ranges from 6k+3 to 9k.
3v mod 6k: for v = 2k+j (j=1,...,k), 3v = 6k+3j, mod 6k = 3j.
So 3v mod n - v = 3j - (2k+j) = 2j - 2k.
Sum = sum_{j=1}^k (2j - 2k) = 2*k(k+1)/2 - 2k^2 = k^2+k-2k^2 = k-k^2 = k(1-k)
So E_3(6k) = k(1-k) for k >= 1.
E_3(6k)/n^2 = k(1-k)/36k^2 = (1-k)/36k -> -1/36 as k -> inf.

For n = 6k+2: a = 2k, b = 3k+1. v from 2k+1 to 3k+1, that's k+1 terms.
For v = 2k+j (j=1,...,k+1): 3v = 6k+3j, mod (6k+2).
When 3j < 6k+2: 3v mod n = 3j. So rv mod n - v = 3j - 2k - j = 2j - 2k.
When 3j = 6k+2: not possible since j <= k+1 and 3(k+1) = 3k+3 > 6k+2 only if k < 1.
When 3j > 6k+2: possible only if j > (6k+2)/3 = 2k+2/3, so j >= 2k+1.
But j <= k+1, so 3j <= 3k+3. 3j > 6k+2 means j > 2k+2/3.
For k >= 2: 2k+2/3 > k+1, so 3j < 6k+2 for all j in range. Good.
For k = 1 (n=8): j ranges 1 to 2. 3j = 3, 6: both < 8. OK.

So for n = 6k+2, E_3 = sum_{j=1}^{k+1} (2j - 2k) = 2*(k+1)(k+2)/2 - 2k(k+1) = (k+1)(k+2-2k) = (k+1)(2-k).
E_3(6k+2)/(6k+2)^2 = (k+1)(2-k)/(6k+2)^2 -> -k^2/(36k^2) = -1/36.

So min E_r(n)/n^2 -> -1/36 (NOT -1/24 as I thought earlier).
Wait, but the data showed -0.042 for some n. Let me check n=31:
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

# Check the actual minimizers more carefully
for n in [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
    min_e = float('inf')
    min_r = 0
    for r in range(1, n):
        if gcd(r, n) != 1:
            continue
        e = E_r(r, n)
        if e < min_e:
            min_e = e
            min_r = r
    # Also check r=3 explicitly
    e3 = E_r(3, n) if gcd(3, n) == 1 else "N/A"
    print(f"n={n}: min at r={min_r}, E={min_e}, E/n^2={min_e/n**2:.6f}; E_3={e3}")

# Check r = (n+1)/3 (which should map v ~ n/3 to v ~ (n+1)/3 * n/3 ~ n/9... no)
# The min is at r where rv mod n clusters near 0 for v in (n/3, n/2]

# Let me find what makes the absolute minimum across ALL n:
print("\n\nAbsolute minimum E_r(n)/n^2 for n up to 500:")
abs_min = 0
abs_case = None
for n in range(6, 501):
    for r in range(1, n):
        if gcd(r, n) != 1:
            continue
        e = E_r(r, n)
        ratio = e / n**2
        if ratio < abs_min:
            abs_min = ratio
            abs_case = (n, r, e)
            if n <= 100:
                print(f"  New min: n={n}, r={r}, E={e}, E/n^2={ratio:.6f}")

print(f"\nAbsolute minimum: n={abs_case[0]}, r={abs_case[1]}, E={abs_case[2]}, E/n^2={abs_min:.8f}")
print(f"Limit should be -1/24 = {-1/24:.8f}")

# It's approaching -1/24. Why?
# For n prime and r such that 3r ≡ 1 mod n (i.e., r = (n+1)/3 when 3|n+1):
# Then for v in (n/3, n/2], rv mod n ranges over specific values.

# Let me check: for n prime with n ≡ 2 mod 3, r = (n+1)/3:
for n in [11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89]:
    if n % 3 != 2:
        continue
    r = (n + 1) // 3
    e = E_r(r, n)
    print(f"n={n} (≡2 mod 3), r=(n+1)/3={r}: E={e}, E/n^2={e/n**2:.6f}")

# And n ≡ 1 mod 3, r = (n+2)/3:
for n in [13, 19, 31, 37, 43, 61, 67, 73, 79, 97]:
    if n % 3 != 1:
        continue
    r = (n + 2) // 3
    if gcd(r, n) != 1:
        continue
    e = E_r(r, n)
    print(f"n={n} (≡1 mod 3), r=(n+2)/3={r}: E={e}, E/n^2={e/n**2:.6f}")
