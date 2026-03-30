#!/usr/bin/env python3
"""
Streaming computation of alpha, rho for M=-3 primes up to 3000.
Uses optimized Farey enumeration (mediant-based).
"""
from math import gcd, log, sqrt
import sys

def mobius_sieve(N):
    """Compute mobius function for all n <= N."""
    mu = [0] * (N + 1)
    mu[1] = 1
    # Smallest prime factor
    spf = list(range(N + 1))
    for i in range(2, N + 1):
        if spf[i] == i:  # i is prime
            for j in range(i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    # Compute mu
    for n in range(2, N + 1):
        p = spf[n]
        m = n // p
        if m % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[m]
    return mu

def mertens_values(N, mu):
    """Compute M(n) for all n <= N."""
    M = [0] * (N + 1)
    for n in range(1, N + 1):
        M[n] = M[n - 1] + mu[n]
    return M

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    d = 5
    while d * d <= n:
        if n % d == 0 or (n + 2) % d == 0: return False
        d += 6
    return True

def compute_streaming(p):
    """Compute alpha, rho using streaming Farey enumeration."""
    N = p - 1

    # Enumerate Farey sequence using mediant property
    # F_N = {a/b : 0 <= a <= b <= N, gcd(a,b) = 1}
    # Using Stern-Brocot / mediant enumeration

    # First pass: count fractions and compute sums for regression
    n = 0  # total count including 0/1 and 1/1
    rank = 0

    # Accumulators
    sum_f = 0.0
    sum_D = 0.0
    sum_f2 = 0.0
    sum_Df = 0.0
    sum_D2 = 0.0
    sum_delta = 0.0
    sum_delta2 = 0.0
    sum_f_delta = 0.0
    sum_D_delta = 0.0
    n_int = 0

    # First: count total n
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                n += 1

    # Second pass: enumerate in order and compute
    # Use sorted enumeration
    # For efficiency, enumerate all fractions, sort, then process
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: x[0] / x[1])

    # Process
    for rank_j, (a, b) in enumerate(fracs):
        if b < 2:
            continue
        f_val = a / b
        D_val = rank_j - n * f_val
        sigma = (p * a) % b
        d_val = (a - sigma) / b

        n_int += 1
        sum_f += f_val
        sum_D += D_val
        sum_f2 += f_val * f_val
        sum_Df += D_val * f_val
        sum_D2 += D_val * D_val
        sum_delta += d_val
        sum_delta2 += d_val * d_val
        sum_f_delta += f_val * d_val
        sum_D_delta += D_val * d_val

    mean_f = sum_f / n_int
    mean_D = sum_D / n_int
    cov_Df = sum_Df / n_int - mean_D * mean_f
    var_f = sum_f2 / n_int - mean_f * mean_f
    alpha = cov_Df / var_f

    C_prime = sum_delta2
    B_prime = 2 * sum_D_delta

    # Compute D_err statistics
    # D_err = D - mean_D - alpha*(f - mean_f)
    # sum(D_err * delta) = sum(D*delta) - mean_D*sum(delta) - alpha*(sum(f*delta) - mean_f*sum(delta))
    sum_Derr_delta = sum_D_delta - mean_D * sum_delta - alpha * (sum_f_delta - mean_f * sum_delta)
    rho = 2 * sum_Derr_delta / C_prime

    # sum(D_err^2) = sum(D^2) - n_int*mean_D^2 - alpha^2*(sum(f^2) - n_int*mean_f^2) - 2*alpha*(sum(D*f) - n_int*mean_D*mean_f)
    # Actually: sum(D_err^2) = sum((D - mean_D)^2) - alpha^2 * sum((f - mean_f)^2)
    sum_Derr2 = (sum_D2 - n_int * mean_D**2) - alpha**2 * (sum_f2 - n_int * mean_f**2)

    R = sqrt(max(0, sum_Derr2) / C_prime) if C_prime > 0 else 0
    if sum_Derr2 > 0 and C_prime > 0:
        corr = sum_Derr_delta / (sqrt(sum_Derr2) * sqrt(C_prime))
    else:
        corr = 0

    return alpha, rho, R, corr

# Main
LIMIT = 3000
print(f"Computing mobius sieve up to {LIMIT}...", file=sys.stderr)
mu = mobius_sieve(LIMIT)
M = mertens_values(LIMIT, mu)

m3_primes = [p for p in range(2, LIMIT + 1) if is_prime(p) and M[p] == -3]
print(f"Found {len(m3_primes)} M=-3 primes up to {LIMIT}", file=sys.stderr)

print(f"{'p':>5} {'alpha':>8} {'rho':>8} {'a+r':>8} {'|rho|':>8} "
      f"{'a-1':>8} {'|r|/(a-1)':>10} {'|r|/slp':>8} {'R':>8} "
      f"{'|c|*sp':>8} {'R/sN':>8}")
print("-" * 120)

for p in m3_primes:
    if p > 1000:
        # Skip some for speed
        if p % 100 > 10:
            continue
    print(f"  p={p}...", file=sys.stderr, end='\r')
    alpha, rho, R, corr = compute_streaming(p)
    rho_abs = abs(rho)
    a_m1 = alpha - 1
    ratio = rho_abs / a_m1 if a_m1 > 0 else float('inf')
    lp = log(p)
    slp = sqrt(lp)
    N = p - 1

    print(f"{p:5d} {alpha:8.4f} {rho:8.4f} {alpha+rho:8.4f} {rho_abs:8.4f} "
          f"{a_m1:8.4f} {ratio:10.4f} {rho_abs/slp:8.4f} {R:8.2f} "
          f"{abs(corr)*sqrt(p):8.4f} {R/sqrt(N):8.4f}")
    sys.stdout.flush()

print("\nDone.", file=sys.stderr)
