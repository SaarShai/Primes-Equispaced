#!/usr/bin/env python3
"""
Analytical lower bound for E_r(n) when gcd(r,n) = 1.

E_r(n) = sum_{n/3 < v <= n/2} (rv mod n - v)

For gcd(r,n)=1, the map v -> rv mod n is a bijection on Z/nZ.
As v ranges over (n/3, n/2], the values rv mod n are "random-looking".

Key identity: sum_{v=1}^{n-1} (rv mod n) = n(n-1)/2 for gcd(r,n)=1.
So sum_{v=1}^{n-1} (rv mod n - v) = 0.
This means: E_r(n) = -sum_{v not in (n/3,n/2]} (rv mod n - v)

The number of terms in E_r: |{v : n/3 < v <= n/2}| = floor(n/2) - floor(n/3)

For large n, this is approximately n/6.

Lower bound approach:
Each term rv mod n - v >= -v (since rv mod n >= 0).
Worst case: all rv mod n = 0, giving E_r(n) >= -sum v = -(n/2)(n/2+1)/2 + (n/3)(n/3+1)/2
                                                      ~ -5n^2/72

But that's too loose. For gcd(r,n)=1, rv mod n = 0 only when v = 0 mod n, impossible for 0 < v < n.

Better: rv mod n takes each value in {0,...,n-1} exactly once as v ranges over {0,...,n-1}.
For v in (n/3, n/2], we pick ~n/6 of these values.
The minimum possible sum of rv mod n values is 0+1+...+(n/6-1) = (n/6)(n/6-1)/2 ~ n^2/72.
The sum of v values is sum_{n/3 < v <= n/2} v ~ (n/6)(5n/12) = 5n^2/72.
So E_r(n) >= n^2/72 - 5n^2/72 = -4n^2/72 = -n^2/18 in the WORST case.

But this worst case requires rv mod n to take the values {0,1,...,n/6-1}, which is very constrained.

Actually, for our purpose we need a LOWER bound on U = sum of 6 terms.
Each E_{m+t}(p-m-t) uses a different r and different n.
If gcd(m+t, p-m-t) = 1 for all t (which happens when p is prime since gcd(r, p-r) | p):
gcd(m+t, p-m-t) divides p, so it's 1 or p. Since m+t < p and p-m-t > 0, it's 1.

So ALL six terms have gcd(r,n) = 1. Good.

Now I need the average of E_r(n): for RANDOM r with gcd(r,n)=1,
E[rv mod n | gcd(r,n)=1] = (n-1)/2 for each v (by symmetry of the bijection).
So E[E_r(n)] = sum_{n/3<v<=n/2} ((n-1)/2 - v)
             = |I| * (n-1)/2 - sum_{v in I} v
where I = (n/3, n/2].

|I| ~ n/6, sum_v ~ 5n^2/72.
E[E_r(n)] ~ n/6 * (n-1)/2 - 5n^2/72 = n(n-1)/12 - 5n^2/72 = n^2/72 * (6-5) - n/12 = n^2/72 - n/12

So the expected value of each E_r(n) is roughly n^2/72.
And U ~ 6 * (n^2/72) = n^2/12 (where n ~ p-m).

For m <= p/2: n >= p/2, so U ~ (p/2)^2/12 = p^2/48 >> p.

The question is: what's the MINIMUM over all r (with gcd(r,n)=1)?

Let me compute min E_r(n) / n^2 as n grows:
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

# For each n, compute min E_r(n)/n^2 over all r with gcd(r,n)=1
print("n, min_E/n^2, max_E/n^2, avg_E/n^2")
for n in range(6, 200):
    min_e = float('inf')
    max_e = float('-inf')
    total_e = 0
    count = 0
    for r in range(1, n):
        if gcd(r, n) != 1:
            continue
        e = E_r(r, n)
        min_e = min(min_e, e)
        max_e = max(max_e, e)
        total_e += e
        count += 1
    if count > 0:
        avg = total_e / count
        if n % 10 == 0 or n < 20 or min_e < 0:
            print(f"n={n}: min_E/n^2 = {min_e/n**2:.6f}, max_E/n^2 = {max_e/n**2:.6f}, "
                  f"avg_E/n^2 = {avg/n**2:.6f}, min_E = {min_e}")

# The key question: is min E_r(n) always >= -cn^2 for some small c?
# And can we get min E_r(n) >= 0?
print("\n\nNegative E_r values:")
neg_cases = 0
for n in range(2, 200):
    for r in range(1, n):
        if gcd(r, n) != 1:
            continue
        e = E_r(r, n)
        if e < 0:
            neg_cases += 1
            if n <= 30:
                print(f"  n={n}, r={r}: E_r = {e}")
print(f"Total negative cases for n < 200: {neg_cases}")

# Since E_r can be negative, we need the SUM of 6 consecutive terms to be positive.
# The key saving grace: consecutive r values tend to have E_r values that partially cancel.
print("\n\nSum of 6 consecutive E_r(n) for fixed n, varying starting r:")
for n in [20, 50, 100]:
    print(f"\nn={n}:")
    min_sum = float('inf')
    for r_start in range(1, n-5):
        s = sum(E_r(r_start + t, n) for t in range(6))
        if s < min_sum:
            min_sum = s
            best_r = r_start
    print(f"  min sum of 6 = {min_sum} at r_start={best_r}")
    print(f"  min_sum/n^2 = {min_sum/n**2:.6f}")
