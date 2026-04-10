#!/usr/bin/env python3
"""
Verify the analytical lower bound used in the proof.

Claim: For p prime and 1 <= m <= (p-11)/2,
each n_t = p - m - t >= (p+1)/2 >= 7 (for p >= 13).
Since gcd(m+t, n_t) = 1 (as (m+t) + n_t = p, prime),

E_r(n) = sum_{n/3 < v <= n/2} (rv mod n - v)

We use the AVERAGE identity:
(1/phi(n)) * sum_{gcd(r,n)=1} E_r(n) = sum_{n/3<v<=n/2} ((n-1)/2 - v)
                                        = |I| * (n-1)/2 - sum_{v in I} v

where I = {v : floor(n/3) < v <= floor(n/2)}.

Let a = floor(n/3), b = floor(n/2).
|I| = b - a
sum_{v in I} v = b(b+1)/2 - a(a+1)/2 = (b-a)(a+b+1)/2

Average E_r(n) = (b-a) * [(n-1)/2 - (a+b+1)/2] = (b-a)(n-a-b-2)/2

For n = 6k:   a = 2k, b = 3k, |I| = k, sum = k(5k+1)/2
  avg = k * (6k - 2k - 3k - 2)/2 = k(k-2)/2

For n = 6k+1: a = 2k, b = 3k, |I| = k, sum = k(5k+1)/2
  avg = k * (6k+1 - 2k - 3k - 2)/2 = k(k-1)/2

For n = 6k+2: a = 2k, b = 3k+1, |I| = k+1, sum = (k+1)(5k+2)/2
  avg = (k+1)(6k+2 - 2k - 3k - 1 - 2)/2 = (k+1)(k-1)/2

For n = 6k+3: a = 2k+1, b = 3k+1, |I| = k, sum = k(5k+3)/2
  avg = k(6k+3 - 2k - 1 - 3k - 1 - 2)/2 = k(k-1)/2

For n = 6k+4: a = 2k+1, b = 3k+2, |I| = k+1, sum = (k+1)(5k+4)/2
  avg = (k+1)(6k+4 - 2k - 1 - 3k - 2 - 2)/2 = (k+1)(k-1)/2

For n = 6k+5: a = 2k+1, b = 3k+2, |I| = k+1, sum = (k+1)(5k+4)/2
  avg = (k+1)(6k+5 - 2k - 1 - 3k - 2 - 2)/2 = (k+1)k/2

In all cases, avg E_r(n) ~ k^2/2 ~ n^2/72.

More precisely: avg E_r(n) >= (floor(n/6)-1)^2 / 2 for n >= 12.
Actually: avg E_r(n) >= (n/6 - 2)^2/2 = (n-12)^2/72

Hmm but the AVERAGE doesn't help directly since we need a LOWER bound for SPECIFIC r.

DIFFERENT APPROACH: Use the Erdos-Turan inequality or explicit Dedekind sum bounds.

Actually, for the proof with m <= (p-11)/2, we have n = p-m-t >= (p+1)/2.
When n >= (p+1)/2, we need U >= p-2 where U has 6 terms each with n >= (p-5)/2.

Even if each E_r is at its MINIMUM of ~-n^2/24, we get
U >= 6 * (-n^2/24) = -n^2/4.
But we need U >= p-2, so this doesn't help.

The actual minimum of E_r(n)/n^2 is ~-1/24 = -0.042.
But the KEY INSIGHT is: the minimum is achieved for r such that r/n ~ 1/2 ± small.
For 6 consecutive r values, they CAN'T all be near n/2.

Let me verify: when does E_r(n) achieve its minimum?
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

# For each n, find which r minimizes E_r(n)
print("r that minimizes E_r(n), and r/n:")
for n in range(10, 201, 10):
    min_e = float('inf')
    min_r = 0
    for r in range(1, n):
        if gcd(r, n) != 1:
            continue
        e = E_r(r, n)
        if e < min_e:
            min_e = e
            min_r = r
    print(f"n={n}: r={min_r}, r/n={min_r/n:.4f}, E={min_e}, E/n^2={min_e/n**2:.6f}")

# So the minimum is at r ~ n/2 (since (n+1)/2 gives the most "scrambling").
# For our U_{p,m}, r = m+t and n = p-m-t. So r + n = p.
# r/n = (m+t)/(p-m-t). For m ~ p/4: r/n ~ 1/3. For m = p/2: r/n ~ 1.
# The minimum of E_r(n) occurs at r/n ~ 1/2, meaning m+t ~ (p-m-t)/2, i.e., m ~ p/3.

# So for m <= (p-11)/2, the worst case for individual terms is m ~ p/3.
# But in the SUM of 6 terms, the cancellation helps.

# Let me compute: for m = p/3, what's the sum U?
print("\n\nU at m = p/3:")
for p in [61, 97, 127, 199, 499, 997]:
    if not all(p % d != 0 for d in range(2, int(p**0.5)+1)):
        continue
    m = p // 3
    val = 0
    for t in range(6):
        r = m + t
        n = p - r
        e = E_r(r, n)
        val += e
    n0 = p - m
    print(f"p={p}, m={m}: U={val}, n0={n0}, U/n0^2={val/n0**2:.6f}, U-(p-2)={val-(p-2)}")

# CONCRETE LOWER BOUND via Dedekind sums:
# E_r(n) = (r-1)*S1 - n*S2 where S1 = sum_{a<v<=b} v, S2 = sum_{a<v<=b} floor(rv/n)
# For the full sum: sum_{v=1}^{n-1} floor(rv/n) = (r-1)(n-1)/2 - s(r,n)*(something)

# Alternative direct approach:
# For gcd(r,n)=1, sum_{v=1}^{n-1} {rv/n} = (n-1)/2
# So sum_{v=1}^{n-1} (rv mod n) = n * sum {rv/n} = n(n-1)/2
# And sum_{v=1}^{n-1} (rv mod n - v) = 0

# Partition {1,...,n-1} into I = (n/3, n/2] and J = {1,...,n-1} \ I.
# sum_I (rv mod n - v) + sum_J (rv mod n - v) = 0
# So E_r(n) = -sum_J (rv mod n - v)

# Now J has 5n/6 + O(1) elements. On J, sum (rv mod n) = n(n-1)/2 - sum_I(rv mod n).
# And sum_J v = n(n-1)/2 - sum_I v.
# So sum_J(rv mod n - v) = (n(n-1)/2 - sum_I(rv mod n)) - (n(n-1)/2 - sum_I v)
#                         = sum_I v - sum_I(rv mod n)
#                         = -E_r(n)
# Tautology! No new info.

# Direct lower bound:
# E_r(n) = sum_{v in I} (rv mod n - v)
# Trivial lower bound: rv mod n >= 0, so E_r(n) >= -sum_I v = -(b(b+1)/2 - a(a+1)/2) ~ -5n^2/72
# Trivial upper bound: rv mod n <= n-1, so E_r(n) <= |I|*(n-1) - sum_I v ~ n^2/6 - 5n^2/72 = 7n^2/72

# For a better lower bound, we need to use that rv mod n takes each value in {0,...,n-1}
# exactly once, so the values in I can't ALL be small.

# KEY: Among the values {rv mod n : v in I}, these are |I| ~ n/6 distinct elements of {0,...,n-1}.
# The minimum sum of n/6 distinct elements from {0,...,n-1} is 0+1+...+(n/6-1) = (n/6)(n/6-1)/2.
# So sum_I(rv mod n) >= (n/6)(n/6-1)/2 ~ n^2/72.
# And E_r(n) >= n^2/72 - 5n^2/72 = -4n^2/72 = -n^2/18.

# But we already know min is -n^2/24, which is LESS negative than -n^2/18.
# So this bound is not tight. Can we do better?

# The tighter bound uses the fact that v is restricted to (n/3, n/2].
# For the map v -> rv mod n with v in (n/3, n/2], the images are spread out.

# Actually the computation shows min E_r/n^2 -> -1/24 ~ -0.04167.
# Let's prove min E_r(n) >= -n^2/24 - O(n).

# At r = (n+1)/2 (for odd n), rv mod n = v(n+1)/2 mod n.
# When v is even: v(n+1)/2 = vn/2 + v/2, so mod n this is v/2.
# When v is odd: v(n+1)/2 = v(n+1)/2, and mod n this is (v+n)/2 = (v+n)/2 mod n.
# Actually for v odd: v(n+1)/2 mod n = (vn+v)/2 mod n = v/2 mod n. But v/2 isn't integer.
# Let me just compute directly.

print("\n\nE_r(n) for r=(n+1)/2, r=(n-1)/2:")
for n in [11, 17, 23, 29, 37, 41, 47, 53, 59, 67, 71, 97, 101]:
    r1 = (n + 1) // 2
    r2 = (n - 1) // 2
    e1 = E_r(r1, n) if gcd(r1, n) == 1 else "N/A"
    e2 = E_r(r2, n) if gcd(r2, n) == 1 else "N/A"
    print(f"n={n}: E_{{{r1}}}={e1} ({e1/n**2 if isinstance(e1,int) else 'N/A'}), "
          f"E_{{{r2}}}={e2} ({e2/n**2 if isinstance(e2,int) else 'N/A'})")
