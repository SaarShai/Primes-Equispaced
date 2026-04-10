#!/usr/bin/env python3
"""
Analyze the growth of alpha and bound the residual for the correction negativity proof.

Key quantities:
  alpha = Cov(D, f) / Var(f) — grows like c*log(N)
  rho = 2*sum(D_err*delta)/C' — appears bounded (converges to ~-2.5 to -3)
  B'/C' = alpha + rho

For correction < 0, need B'/C' > 1, i.e., alpha + rho > 1.

Since alpha grows and rho appears bounded, this holds for all large p.
Need to pin down the exact rate.
"""

from fractions import Fraction
from math import gcd, log

def mobius(n):
    if n == 1: return 1
    temp = n; d = 2; factors = []
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d); temp //= d
            if temp % d == 0: return 0
        d += 1
    if temp > 1: factors.append(temp)
    return (-1) ** len(factors)

def mertens(N):
    return sum(mobius(k) for k in range(1, N+1))

def farey_sequence(N):
    fracs = set()
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0: return False
        d += 6
    return True

# Compute for all primes up to 200
print(f"{'p':>5} {'M(p)':>5} {'alpha':>8} {'rho':>8} {'alpha+rho':>10} {'a-1':>8} {'log(N)':>8} {'a/log(N)':>10}")
print("-" * 72)

for p in range(11, 201):
    if not is_prime(p): continue
    N = p - 1
    F = farey_sequence(N)
    n = len(F)
    M_p = mertens(p)

    # Compute alpha
    mean_D = Fraction(1, 2)  # sum D_i / n = 1/2
    mean_f = Fraction(1, 2)

    D_list = []
    f_list = []
    delta_list = []
    for j, f in enumerate(F):
        a, b = f.numerator, f.denominator
        D_j = Fraction(j) - Fraction(n) * f
        delta = Fraction(a - (p * a % b), b)
        D_list.append(D_j)
        f_list.append(f)
        delta_list.append(delta)

    cov = sum((D_list[i] - mean_D) * (f_list[i] - mean_f) for i in range(n))
    var_f = sum((f_list[i] - mean_f)**2 for i in range(n))
    alpha = cov / var_f

    # Compute rho = 2*sum(D_err*delta)/C' (interior only)
    C_prime = sum(delta_list[i]**2 for i in range(n) if f_list[i].denominator > 1)
    sum_Derr_delta = sum(
        (D_list[i] - mean_D - alpha*(f_list[i] - mean_f)) * delta_list[i]
        for i in range(n) if f_list[i].denominator > 1
    )
    rho = 2 * sum_Derr_delta / C_prime if C_prime else 0

    a_f = float(alpha)
    r_f = float(rho)
    logN = log(N)

    print(f"{p:5d} {M_p:5d} {a_f:8.4f} {r_f:8.4f} {a_f+r_f:10.4f} {a_f-1:8.4f} {logN:8.4f} {a_f/logN:10.4f}")
