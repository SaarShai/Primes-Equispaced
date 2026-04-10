#!/usr/bin/env python3
"""
Find the correct theorem. Two approaches:
1. For m <= alpha*p, U >= p-2 holds for p >= P0(alpha).
2. Determine the exact threshold m_max(p) and its asymptotic behavior.

Also: investigate the main-term formula more carefully.
E_r(n) for the specific summation range n/3 < v <= n/2.
"""

from math import gcd, floor, ceil

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

# For each prime, find the EXACT m_max where U >= p-2 for all m <= m_max
# and also the EXACT m_max2 where U >= 0 for all m <= m_max2
print("p, m_max(U>=p-2), m_max(U>=0), m_max/p, m_max2/p")
for p in primes:
    m_max_p2 = 0
    m_max_0 = 0
    for m in range(1, p - 5):
        val = U(p, m)
        if val is None:
            break
        if val >= p - 2:
            m_max_p2 = m
        else:
            break  # first failure
    for m in range(1, p - 5):
        val = U(p, m)
        if val is None:
            break
        if val >= 0:
            m_max_0 = m
        else:
            break
    r1 = m_max_p2 / p
    r2 = m_max_0 / p
    if p <= 200 or p % 100 < 10:
        print(f"p={p}: m_max(>=p-2)={m_max_p2} ({r1:.4f}), m_max(>=0)={m_max_0} ({r2:.4f})")

# Now: the main term analysis.
# For gcd(r,n) = 1, what is E_r(n) on average?
# sum_{n/3 < v <= n/2} (rv mod n - v)
# = sum_{n/3 < v <= n/2} rv mod n - sum_{n/3 < v <= n/2} v
# The second sum: sum v from a+1 to b = b(b+1)/2 - a(a+1)/2 where a = floor(n/3), b = floor(n/2)
# The first sum: for random r, rv mod n is ~uniform on {0,...,n-1}, so sum ~ (n-1)/2 * (b-a) terms
# Net: E_r(n) ~ (b-a) * ((n-1)/2 - (a+b+1)/2) = (b-a) * (n - a - b - 2)/2

# With a = n/3, b = n/2: (b-a) ~ n/6, (n-a-b-2)/2 ~ (n - n/3 - n/2)/2 = n/12
# So E_r(n) ~ n/6 * n/12 = n^2/72 per term? No wait...
# (b-a) * ((n-1)/2 - (a+b+1)/2) with a~n/3, b~n/2:
# average v ~ (a+b)/2 ~ 5n/12
# average rv mod n ~ (n-1)/2
# contribution per term: (n-1)/2 - 5n/12 = n/12 - 1/2
# Number of terms: n/6
# Total: n/6 * (n/12 - 1/2) ~ n^2/72

# But from data: U_{p,2} at p=97 is 1034 ~ (95^2+94^2+93^2+92^2+91^2+90^2)/72 ~ 6*90^2/72 ~ 675
# Actual is higher, so the heuristic underestimates.

# Let me compute the Dedekind-sum based exact formula.
# Actually, for p prime and 1 <= r < n = p-r (so r < p/2), gcd(r,n) = gcd(r, p-r) = gcd(r,p) = 1.
# The sum sum_{v=1}^{n-1} (rv mod n) = n(n-1)/2.
# But we only sum over n/3 < v <= n/2, so we need partial sums of the "saw-tooth" function.

print("\n\nRatio U_{p,m} / n_0^2 where n_0 = p-m (size of first term):")
for p in [97, 199, 499, 997]:
    if not is_prime(p):
        continue
    print(f"\np = {p}:")
    for m in [1, 2, 5, 10, p//4, p//3, p//2 - 3]:
        if m < 1 or m >= p - 5:
            continue
        val = U(p, m)
        n0 = p - m
        if val is not None and n0 > 0:
            print(f"  m={m}: U={val}, n_0={n0}, U/n_0^2={val/n0**2:.6f}")
