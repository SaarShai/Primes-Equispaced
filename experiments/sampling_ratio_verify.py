#!/usr/bin/env python3
"""
Verify the sampling ratio: Sum E(k/p)^2 / [(p-1)/n * Sum D(f)^2] -> 2

where:
  E(k/p) = #{f in F_N : f <= k/p} - n*(k/p)   (Farey counting error at k/p)
  D(f) = rank(f) - n*f                          (Farey displacement)
  n = |F_N|, N = p-1

Also decompose the ratio to understand WHERE the factor of 2 comes from.
"""

from fractions import Fraction
from math import gcd
import sys

def farey_sequence(N):
    """Generate Farey sequence F_N as list of Fraction objects."""
    fracs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.append(Fraction(a, b))
    fracs = sorted(set(fracs))
    return fracs

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

def mertens(n):
    """Compute M(n) = sum_{k=1}^{n} mu(k)."""
    if n <= 0: return 0
    mu = [0] * (n + 1)
    mu[1] = 1
    for i in range(1, n + 1):
        if mu[i] == 0 and i > 1:
            continue
        for j in range(2*i, n + 1, i):
            mu[j] -= mu[i]
        # Actually let's use sieve
    # Redo with proper Mobius sieve
    mu2 = [0] * (n + 1)
    mu2[1] = 1
    for i in range(1, n + 1):
        for j in range(2*i, n + 1, i):
            mu2[j] -= mu2[i]
    return sum(mu2[1:n+1])

def analyze_prime(p):
    """Full analysis for a single prime p."""
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)

    # Compute D(f) = rank(f) - n*f for each f in F_N
    D = {}
    for i, f in enumerate(F_N):
        D[f] = Fraction(i) - n * f  # rank is i (0-indexed)

    # Sum D(f)^2
    sum_D_sq = sum(d*d for d in D.values())

    # Compute E(k/p) = #{f in F_N : f <= k/p} - n*(k/p)
    # This is the counting error at rational point k/p
    E = {}
    for k in range(1, p):
        x = Fraction(k, p)
        # Count fractions <= x
        count = sum(1 for f in F_N if f <= x)
        E[k] = count - n * x

    # Sum E(k/p)^2
    sum_E_sq = sum(e*e for e in E.values())

    # The ratio
    factor = Fraction(p - 1, n)
    ratio = sum_E_sq / (factor * sum_D_sq)

    # Also compute integral of D(x)^2 approximation
    # integral ~ old_D_sq / n
    integral_approx = sum_D_sq / n

    # Riemann sum of D_old^2 at k/p points
    riemann_D_sq = sum(E[k]*E[k] for k in range(1, p))
    # Note: E(k/p) = N_{F_N}(k/p) - n*(k/p) = D_old(k/p) essentially
    # Actually E(k/p) IS D_old(k/p) evaluated at x=k/p

    # Decompose: boundary vs interior
    E_boundary_sq = E[1]*E[1] + E[p-1]*E[p-1]  # k=1 and k=p-1
    E_interior_sq = sum(E[k]*E[k] for k in range(2, p-1))

    # What fraction of sum_E_sq comes from boundary?
    boundary_frac = float(E_boundary_sq) / float(sum_E_sq) if sum_E_sq > 0 else 0

    # Interior per-point average vs Farey average
    interior_avg = float(E_interior_sq) / (p - 3) if p > 3 else 0
    farey_avg = float(sum_D_sq) / n
    interior_ratio = interior_avg / farey_avg if farey_avg > 0 else 0

    M_p = mertens(p)

    return {
        'p': p,
        'N': N,
        'n': n,
        'M_p': M_p,
        'sum_D_sq': float(sum_D_sq),
        'sum_E_sq': float(sum_E_sq),
        'ratio': float(ratio),
        'boundary_frac': boundary_frac,
        'interior_ratio': interior_ratio,
        'E_1': float(E[1]),
        'E_pm1': float(E[p-1]),
        'n_new': n + p - 1,
    }

# Test primes
primes = [p for p in range(5, 200) if is_prime(p)]

print(f"{'p':>5} {'n':>6} {'M(p)':>5} {'ratio':>8} {'bdy_frac':>9} {'int_ratio':>10} {'E(1/p)':>10} {'E((p-1)/p)':>12}")
print("-" * 80)

for p in primes:
    r = analyze_prime(p)
    print(f"{r['p']:>5} {r['n']:>6} {r['M_p']:>5} {r['ratio']:>8.4f} {r['boundary_frac']:>9.4f} {r['interior_ratio']:>10.4f} {r['E_1']:>10.4f} {r['E_pm1']:>12.4f}")

print("\n\n=== FOURIER ANALYSIS ===\n")

# For a few small primes, do the DFT decomposition
for p in [11, 23, 47, 67, 89]:
    if not is_prime(p):
        continue
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)

    # E(k/p) for k=1..p-1
    E_vals = []
    for k in range(1, p):
        x = Fraction(k, p)
        count = sum(1 for f in F_N if f <= x)
        E_vals.append(float(count - n * x))

    # DFT of E values
    import numpy as np
    E_arr = np.array(E_vals)
    E_hat = np.fft.fft(E_arr)

    # Parseval: sum |E|^2 = (1/p') sum |E_hat|^2 where p' = p-1
    parseval_check = np.sum(np.abs(E_hat)**2) / (p - 1)
    direct_sum = np.sum(E_arr**2)

    # Power spectrum
    power = np.abs(E_hat)**2 / (p - 1)

    # Top 5 frequencies
    top_idx = np.argsort(power)[::-1][:10]

    print(f"p = {p}: sum_E^2 = {direct_sum:.4f}, Parseval check = {parseval_check:.4f}")
    print(f"  Top frequencies (m, power, fraction of total):")
    for idx in top_idx:
        frac = power[idx] / direct_sum
        print(f"    m={idx:>4}: power={power[idx]:>10.4f}, frac={frac:.4f}")
    print()

print("\n=== CORRELATION STRUCTURE ===\n")
# Check: is E(k/p) correlated with D(f) for f nearest to k/p?
for p in [47, 89]:
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)

    D_vals = []
    for i, f in enumerate(F_N):
        D_vals.append(float(i - n * f))

    E_vals = []
    for k in range(1, p):
        x = Fraction(k, p)
        count = sum(1 for f in F_N if f <= x)
        E_vals.append(float(count - n * x))

    # The key identity: E(k/p) = D(f_j) where f_j is the largest Farey fraction <= k/p
    # plus k - j (number of other new fractions before k/p)...
    # Actually E(k/p) = count(F_N, k/p) - n*k/p where count uses F_N only
    # So E(k/p) is the Farey discrepancy function evaluated at x=k/p

    # Compare: mean of E^2 vs mean of D^2
    mean_E_sq = sum(e**2 for e in E_vals) / len(E_vals)
    mean_D_sq = sum(d**2 for d in D_vals) / len(D_vals)

    print(f"p={p}: mean(E^2) = {mean_E_sq:.4f}, mean(D^2) = {mean_D_sq:.4f}, ratio = {mean_E_sq/mean_D_sq:.4f}")

    # The ratio mean(E^2)/mean(D^2) should be ~ 2*n/(p-1) if the overall ratio is 2
    predicted = 2 * n / (p - 1)
    print(f"  Predicted ratio (if overall=2): {predicted:.4f}")
    print()
