#!/usr/bin/env python3
"""
Prove E_{n-2}(n) -> -n^2/24.

For r = n-2: rv mod n = (n-2)v mod n = nv - 2v mod n = -2v mod n = n - 2v (when 2v < n, i.e., v <= n/2)
                                                                    = 2n - 2v (when n < 2v < 2n)

For v in (n/3, n/2]:
  All have 2v <= n, so (n-2)v mod n = n - 2v.

E_{n-2}(n) = sum_{n/3 < v <= n/2} ((n-2v) - v) = sum_{n/3 < v <= n/2} (n - 3v)

Let a = floor(n/3), b = floor(n/2).
E_{n-2}(n) = (b-a)*n - 3*(b(b+1)/2 - a(a+1)/2)
           = (b-a)*n - 3(b-a)(a+b+1)/2

For n = 6k (exact case):
a = 2k, b = 3k, b-a = k, a+b+1 = 5k+1
E = k*6k - 3k(5k+1)/2 = 6k^2 - k(15k+3)/2 = 6k^2 - 15k^2/2 - 3k/2
  = 12k^2/2 - 15k^2/2 - 3k/2 = -3k^2/2 - 3k/2 = -3k(k+1)/2
E/n^2 = -3k(k+1)/(2*36k^2) = -(k+1)/(24k) -> -1/24

For n = 6k+1 (prime-like):
a = 2k, b = 3k, b-a = k, a+b+1 = 5k+1
E = k(6k+1) - 3k(5k+1)/2 = 6k^2+k - 15k^2/2 - 3k/2
  = 12k^2/2 + 2k/2 - 15k^2/2 - 3k/2 = -3k^2/2 - k/2 = -k(3k+1)/2
E/n^2 = -k(3k+1)/(2(6k+1)^2) -> -3k^2/(72k^2) = -1/24

Great! So E_{n-2}(n) ~ -n^2/24 exactly.

Now for the SUM: U_{p,m} with m <= (p-11)/2.
r = m+t ranges from m to m+5, n = p-r = p-m-t ranges from p-m down to p-m-5.
r + n = p (prime), so gcd(r,n) = 1.
r/n = (m+t)/(p-m-t).

The worst E_r(n) is when r = n-2, i.e., r + 2 = n, i.e., m+t+2 = p-m-t, i.e., m = (p-2-2t)/2.
For this to apply to all 6 terms simultaneously is impossible (different t give different m).

For a SINGLE worst term: the worst E_r(n) ~ -n^2/24.
For the OTHER 5 terms: since their r values differ from n-2,
they each contribute MORE than the minimum.

KEY STRUCTURAL FACT: if r = m+t and n = p-m-t, then r = n-2 means m+t = (p-2)/2.
Only ONE value of t satisfies this (approximately), so at most 1 of the 6 terms
is near the minimum.

For the remaining 5 terms: their r values satisfy |r - (n-2)| >= 1,
which means r/n differs from 1-2/n significantly.

Let me compute: for the 5 "non-worst" terms, what's the typical E_r(n)?
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

# For large primes, look at U_{p,m} with m ~ (p-2)/2 (worst case)
print("U_{p,m} at m = (p-2)/2 ± 3:")
for p in [101, 199, 499, 997, 1999]:
    if not is_prime(p):
        continue
    m_base = (p - 2) // 2
    for dm in range(-3, 4):
        m = m_base + dm
        if 1 <= m <= (p-11)//2:
            terms = []
            for t in range(6):
                r = m + t
                n = p - r
                e = E_r(r, n)
                terms.append(e)
            val = sum(terms)
            print(f"  p={p}, m={m}: terms={terms}, U={val}, p-2={p-2}, diff={val-(p-2)}")

# For m near (p-2)/2, the term with t such that m+t ~ (p-2)/2 is the most negative.
# But the other terms have r that are offset, so they're less negative.

# PROOF STRATEGY:
# Sum of 6 terms = sum E_{m+t}(p-m-t)
# Writing n_t = p-m-t, r_t = m+t = p - n_t:
# E_{r_t}(n_t) = E_{p-n_t}(n_t)
#
# By the identity E_{n-r}(n) = -E_r(n) + (|I|-1)? No, that's wrong.
# Actually: (n-r)v mod n = -(rv mod n) mod n = n - (rv mod n) when rv mod n > 0.
# So E_{n-r}(n) = sum_{v in I} (n - rv mod n - v) = |I|*n - sum(rv mod n) - sum v
#               = |I|*n - (sum(rv mod n) + sum v)
#               = |I|*n - (E_r(n) + 2*sum_I v)
# Hmm, not a clean reflection.

# Let me just verify computationally that the sum of 6 terms is always
# >= (something useful) for large n.

# For n >= 50 and m <= (p-11)/2, check U >= p^2/100:
print("\n\nChecking U >= p^2/100 for p >= 61 and m <= (p-11)/2:")
primes = [p for p in range(61, 2001) if is_prime(p)]
worst_ratio = float('inf')
for p in primes:
    m_max = (p - 11) // 2
    for m in range(1, m_max + 1):
        val = U(p, m)
        if val is not None:
            ratio = val / p**2
            if ratio < worst_ratio:
                worst_ratio = ratio
                worst_case = (p, m, val)

print(f"Worst U/p^2 = {worst_ratio:.8f} at p={worst_case[0]}, m={worst_case[1]}, U={worst_case[2]}")

# For m <= (p-11)/2, the MINIMUM n is (p+1)/2.
# Worst single term: -n^2/24 ~ -p^2/96.
# Average term: n^2/72 ~ p^2/288.
# 6 terms average: p^2/48.
# Even 1 worst + 5 average: -p^2/96 + 5*p^2/288 = p^2(-1/96 + 5/288) = p^2(-3+5)/288 = p^2/144 > 0.
# So U > 0 (approximately) for all valid m, large p.

# But we need U >= p-2, which is much weaker.
# p^2/144 >> p for p >= 145. With exact bounds it should work for p >= 61.

# EXPLICIT BOUND:
# For each term, E_{m+t}(p-m-t) >= -((p-m-t)^2)/24 - (p-m-t).
# The smallest n is n_5 = p-m-5 >= (p-1)/2.
# So each term >= -(p-m)^2/24 - (p-m).
# U >= 6 * (-(p-m)^2/24 - (p-m)) = -(p-m)^2/4 - 6(p-m).
# For m <= (p-11)/2: (p-m) <= (p+11)/2, so
# U >= -(p+11)^2/16 - 3(p+11) = -(p^2+22p+121)/16 - 3p - 33
# This is NEGATIVE for all p. Too loose!

# The issue: we can't just use the worst case for ALL 6 terms.
# We need the AVERAGE behavior of consecutive terms.

# Better approach: use the exact formula for E_{n-2}(n) and bound the rest.
# Only 1 of the 6 terms can be near its minimum.
# The other 5 must each contribute at least something nontrivial.

# Let me compute: for fixed n, and r ranging over consecutive values,
# what's the sum of 6 consecutive E_r(n)?
print("\n\nMin sum of 6 consecutive E_r(n) for single n:")
for n in [50, 100, 200, 500]:
    min_sum = float('inf')
    for r_start in range(1, n-5):
        all_coprime = all(gcd(r_start+t, n) == 1 for t in range(6))
        if not all_coprime:
            continue
        s = sum(E_r(r_start + t, n) for t in range(6))
        if s < min_sum:
            min_sum = s
            best_r = r_start
    print(f"n={n}: min sum of 6 = {min_sum} at r={best_r}, "
          f"ratio to n^2 = {min_sum/n**2:.6f}")
