#!/usr/bin/env python3
"""
Detailed analysis: what's the true lower bound on U_{p,m}?
For each (p,m), n_t = p - m - t for t=0..5.
E_r(n) = sum_{n/3 < v <= n/2} (rv mod n - v)

Key question: what causes U to be negative for large m?
When m is large, n = p-m is small, and E_r(n) for large r can be negative.

Let's understand E_r(n) better.
For v in (n/3, n/2], rv mod n - v.
If r < n, then rv mod n depends on whether rv overflows n.

For gcd(r,n) = 1 (which happens when p is prime and r,n < p):
sum_{v=1}^{n-1} (rv mod n) = n(n-1)/2
So the average of rv mod n is (n-1)/2.
The sum over (n/3, n/2] should be roughly n/6 terms, each contributing ~(n-1)/2 - v ~ 0.
Actually more carefully: E_r(n) = sum (rv mod n - v) over n/6 terms.

Let me compute the "main term" prediction vs actual.
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

# For p=97, print each E_r(n) contribution
print("Detailed breakdown for p=97:")
for m in [2, 10, 30, 50, 70, 80, 85, 90]:
    print(f"\n  m={m}:")
    total = 0
    for t in range(6):
        r = m + t
        n = 97 - r
        e = E_r(r, n)
        num_terms = n//2 - n//3
        print(f"    t={t}: r={r}, n={n}, E_r={e}, #terms={num_terms}")
        total += e
    print(f"    Total U = {total}, p-2 = 95")

# Key insight: for large m, n = p-m-t is small.
# When n < 6 (since t goes up to 5), some terms become trivially small.
# Let's see the n values for various m.
print("\n\nMinimum n in block for various m (p=97):")
for m in range(1, 92):
    min_n = 97 - m - 5
    if min_n <= 6:
        print(f"  m={m}: min n = {min_n}")

# What's the actual lower bound on U_{p,m} as function of n_min = p-m-5?
print("\n\nU_{p,m} as function of n_min = p-m-5:")
primes = [p for p in range(7, 500) if is_prime(p)]
data = {}  # n_min -> list of U values
for p in primes:
    for m in range(1, p-5):
        n_min = p - m - 5
        val = U(p, m)
        if val is not None:
            if n_min not in data:
                data[n_min] = []
            data[n_min].append((p, m, val))

# For each n_min, what's the min U / n_min^2?
print("\nn_min -> min(U), min(U/n_min^2):")
for n_min in sorted(data.keys()):
    if n_min <= 0:
        continue
    min_u = min(v for _, _, v in data[n_min])
    ratio = min_u / n_min**2 if n_min > 0 else 0
    if n_min <= 30 or n_min % 10 == 0:
        print(f"  n_min={n_min}: min U = {min_u}, min U/n_min^2 = {ratio:.4f}")

# The RIGHT parameterization: express everything in terms of n_min
# U ~ sum of 6 terms each ~ n_t^2 * S_I where n_t ~ n_min + (5-t)
# For large n_min, U ~ 6 * n_min^2 * (1/12) = n_min^2/2

# But we need U >= p-2 = (n_min + m + 5) - 2 = n_min + m + 3
# Since m = p - n_min - 5, we need U >= (p - n_min - 5) + n_min + 3 = p - 2
# So the constraint is U >= p-2 where p = n_min + m + 5

# For m = 1: p = n_min + 6, need U >= n_min + 4. Since U ~ n_min^2/2, easy for large n_min.
# For m = p/2: p = 2m + 5 + 2*n_min... wait let me think differently.

# Actually: for m <= p/2 - 3, n = p-m >= p/2 + 3, so n_min = p-m-5 >= p/2 - 2.
# U ~ 6 * n^2/12 = n^2/2 >= (p/2)^2/2 = p^2/8 >> p.
# The problem is only when n is small, i.e., m close to p.

# True question: for what n_min does U >= p-2 ALWAYS hold?
# p-2 = n_min + m + 3. But p = n_min + m + 5.
# So p-2 = n_min + m + 3 can be at most n_min + (p-6) + 3 = n_min + p - 3.
# But p = n_min + m + 5, so p-2 depends on m.

# Better: fix n_min. Then over all (p,m) with p-m-5 = n_min,
# p = n_min + m + 5, so p-2 = n_min + m + 3.
# U depends on r = m+t and n_t = n_min + 5 - t.
# The U depends on BOTH m and n_min separately.

# Let me check: for fixed n_min, does U grow with m?
print("\n\nFor fixed n_min = 40, U vs m:")
for p in primes:
    for m in range(1, p-5):
        n_min = p - m - 5
        if n_min == 40:
            val = U(p, m)
            print(f"  p={p}, m={m}: U={val}, p-2={p-2}, diff={val-(p-2)}")

print("\nFor fixed n_min = 20, U vs m:")
for p in primes:
    for m in range(1, p-5):
        n_min = p - m - 5
        if n_min == 20:
            val = U(p, m)
            print(f"  p={p}, m={m}: U={val}, p-2={p-2}, diff={val-(p-2)}")
