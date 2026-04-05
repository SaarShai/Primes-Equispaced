#!/usr/bin/env python3
"""Quick check: does D(a/p) correlate with M(q_{m-1})?
This is the ONE GAP in the Spectral Enhancement Theorem."""
import math
from fractions import Fraction

def mobius(n):
    """Compute μ(n)."""
    if n == 1: return 1
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            temp //= d
            if temp % d == 0: return 0  # squared factor
        d += 1
    if temp > 1: factors.append(temp)
    return (-1)**len(factors)

def mertens(n):
    """M(n) = Σ_{k=1}^n μ(k)."""
    return sum(mobius(k) for k in range(1, n+1))

def farey(n):
    """Generate F_n as sorted list of Fraction objects."""
    a, b, c, d = 0, 1, 1, n
    seq = [Fraction(0, 1)]
    while c <= n:
        k = (n + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        seq.append(Fraction(a, b))
    return seq

def cf_penultimate_denom(a, p):
    """Get q_{m-1} (penultimate convergent denominator) for a/p."""
    # CF expansion of a/p
    nums = [a, p]
    while nums[-1] != 0:
        q, r = divmod(nums[-2], nums[-1])
        nums.append(r)
    # Convergents: use the standard recursion
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    x, y = a, p
    while y != 0:
        q = x // y
        h_prev, h_curr = h_curr, q * h_curr + h_prev
        k_prev, k_curr = k_curr, q * k_curr + k_prev
        x, y = y, x % y
    # k_prev is q_{m-1} (penultimate denominator)
    return k_prev

for p in [13, 19, 31, 43, 61]:
    fp = farey(p - 1)
    fp_set = set(fp)
    n_fp = len(fp)

    D_vals = []
    M_vals = []

    for a in range(1, p):
        if math.gcd(a, p) != 1: continue
        f = Fraction(a, p)
        # Rank of a/p in F_{p-1}
        rank = sum(1 for x in fp if x <= f)
        D = rank - n_fp * float(f)

        q_prev = cf_penultimate_denom(a, p)
        M_q = mertens(q_prev)

        D_vals.append(D)
        M_vals.append(M_q)

    # Correlation
    D_arr = [float(x) for x in D_vals]
    M_arr = [float(x) for x in M_vals]
    n = len(D_arr)
    mean_D = sum(D_arr) / n
    mean_M = sum(M_arr) / n
    cov = sum((D_arr[i] - mean_D) * (M_arr[i] - mean_M) for i in range(n))
    var_D = sum((x - mean_D)**2 for x in D_arr)
    var_M = sum((x - mean_M)**2 for x in M_arr)

    if var_D > 0 and var_M > 0:
        corr = cov / math.sqrt(var_D * var_M)
    else:
        corr = 0.0

    print(f"p={p:3d}: {n:3d} fracs, corr(D, M(q_prev)) = {corr:+.4f}, "
          f"mean |D|={sum(abs(x) for x in D_arr)/n:.2f}, "
          f"mean |M|={sum(abs(x) for x in M_arr)/n:.2f}")
