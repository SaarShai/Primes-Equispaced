#!/usr/bin/env python3
"""
Deeper analysis: understand WHEN and WHY alpha goes negative.

Key question: Is alpha > 0 the right claim? Or should the theorem be restricted?

Approach:
1. Check if alpha < 0 only at isolated N, or in long runs
2. Check if alpha < 0 at any PRIME N (since the Sign Theorem is about primes)
3. Understand what causes R to flip sign
"""

from math import gcd
import sys
import time

def farey_next(a1, b1, a2, b2, N):
    k = (N + b1) // b2
    return k * a2 - a1, k * b2 - b1

def compute_alpha_R(N):
    fracs = []
    a1, b1 = 0, 1
    a2, b2 = 1, N
    fracs.append((a1, b1))
    fracs.append((a2, b2))
    while not (a2 == 1 and b2 == 1):
        a3, b3 = farey_next(a1, b1, a2, b2, N)
        fracs.append((a3, b3))
        a1, b1 = a2, b2
        a2, b2 = a3, b3

    n = len(fracs)
    sum_f = 0.0
    sum_f2 = 0.0
    sum_Df = 0.0

    for idx, (a, b) in enumerate(fracs):
        i = idx + 1
        f = a / b
        D = i - n * f
        sum_f += f
        sum_f2 += f * f
        sum_Df += D * f

    R = sum_f2 - n / 3.0
    E_f = sum_f / n
    sum_D = n * (n + 1) / 2.0 - n * sum_f
    E_D = sum_D / n
    Cov = sum_Df / n - E_D * E_f
    Var_f = sum_f2 / n - E_f * E_f
    alpha = Cov / Var_f if Var_f > 0 else None
    return N, n, R, alpha

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

# PART 1: Check all primes N up to 2000 -- is alpha ever negative at a prime?
print("=" * 80)
print("PART 1: Alpha at PRIME N values (N = 7 to 2000)")
print("=" * 80)
primes = [p for p in range(7, 2001) if is_prime(p)]
print(f"Checking {len(primes)} primes...")

alpha_neg_primes = []
min_alpha_prime = float('inf')
min_alpha_prime_N = None

for p in primes:
    _, n, R, alpha = compute_alpha_R(p)
    if alpha is not None:
        if alpha <= 0:
            alpha_neg_primes.append((p, n, R, alpha))
        if alpha < min_alpha_prime:
            min_alpha_prime = alpha
            min_alpha_prime_N = p
    if p % 200 < 10 and is_prime(p):
        print(f"  p={p}: n={n}, R={R:.6f}, alpha={alpha:.6f}")

print(f"\nPrimes with alpha <= 0: {alpha_neg_primes}")
print(f"Minimum alpha at a prime: {min_alpha_prime:.6f} at p={min_alpha_prime_N}")

# PART 2: Check the "gap" N values 1417-1418 neighborhood
# What is the pattern? Is there a run of consecutive alpha<0?
print("\n" + "=" * 80)
print("PART 2: Consecutive N around 1417")
print("=" * 80)
print(f"{'N':>6} {'n':>8} {'R':>14} {'alpha':>10} {'prime':>6}")
print("-" * 50)
for N in range(1410, 1430):
    _, n, R, alpha = compute_alpha_R(N)
    p = "P" if is_prime(N) else ""
    marker = " <<<" if (alpha is not None and alpha <= 0) else ""
    print(f"{N:>6} {n:>8} {R:>14.8f} {alpha:>10.6f} {p:>6}{marker}")

# PART 3: For ALL N=7..2000, compute R and see its distribution
print("\n" + "=" * 80)
print("PART 3: R distribution statistics for N = 100..2000")
print("=" * 80)

R_values = []
for N in range(100, 2001):
    _, n, R, _ = compute_alpha_R(N)
    R_values.append((N, R))

R_vals = [r for _, r in R_values]
print(f"min R = {min(R_vals):.6f}")
print(f"max R = {max(R_vals):.6f}")
print(f"mean R = {sum(R_vals)/len(R_vals):.6f}")
print(f"R > 0 count: {sum(1 for r in R_vals if r > 0)} out of {len(R_vals)}")

# Show the top-10 most positive R values
R_sorted = sorted(R_values, key=lambda x: -x[1])[:20]
print("\nTop 20 most positive R(N):")
for N, R in R_sorted:
    print(f"  N={N}: R={R:.8f}")

# PART 4: For primes only, check R
print("\n" + "=" * 80)
print("PART 4: R at primes (showing worst cases)")
print("=" * 80)
R_prime_vals = []
for p in primes:
    if p >= 100:
        _, _, R, alpha = compute_alpha_R(p)
        R_prime_vals.append((p, R, alpha))

R_prime_sorted = sorted(R_prime_vals, key=lambda x: -x[1])[:20]
print("Top 20 most positive R(p) at primes:")
for p, R, alpha in R_prime_sorted:
    print(f"  p={p}: R={R:.8f}, alpha={alpha:.6f}")

# PART 5: What is Mertens function at N=1417?
print("\n" + "=" * 80)
print("PART 5: Mertens function near 1417")
print("=" * 80)

# Simple Mertens computation
def mobius_sieve(N):
    mu = [0] * (N + 1)
    mu[1] = 1
    for i in range(1, N + 1):
        if mu[i] == 0 and i > 1:
            continue
        for j in range(2 * i, N + 1, i):
            mu[j] -= mu[i]
        # Check if i is squarefree
    # Actually need a proper sieve
    is_prime_arr = [True] * (N + 1)
    primes_list = []
    mu2 = [0] * (N + 1)
    mu2[1] = 1
    for i in range(2, N + 1):
        if is_prime_arr[i]:
            primes_list.append(i)
            mu2[i] = -1
        for p in primes_list:
            if i * p > N:
                break
            is_prime_arr[i * p] = False
            if i % p == 0:
                mu2[i * p] = 0
                break
            else:
                mu2[i * p] = -mu2[i]
    return mu2

mu = mobius_sieve(1500)
M = 0
print(f"{'N':>6} {'M(N)':>8}")
for n in range(1, 1501):
    M += mu[n]
    if n >= 1410 and n <= 1425:
        p = "PRIME" if is_prime(n) else ""
        print(f"{n:>6} {M:>8} {p}")
