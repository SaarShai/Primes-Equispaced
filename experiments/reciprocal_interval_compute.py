#!/usr/bin/env python3
"""
Compute the inner product I(p) = sum_{n=1}^{N} lambda_p(n)/n
where lambda_p(n) = M(floor(N/n)), N = p-1.

Also compute I*(p) = sum_{n=1}^{N} M(floor(N/n))/(N+1-n)
and the difference I - I*.

Goal: determine growth rate of I(p) and |I(p) - I*(p)|.
"""

import numpy as np
from sympy import isprime, primerange, mobius

def mertens_table(N):
    """Compute M(k) = sum_{j<=k} mu(j) for k = 0, ..., N."""
    mu = np.zeros(N+1, dtype=np.int64)
    mu[1] = 1
    for i in range(1, N+1):
        for j in range(2*i, N+1, i):
            mu[j] -= mu[i]
    M = np.cumsum(mu)
    return M

def compute_I(N, M):
    """I(p) = sum_{n=1}^{N} M(floor(N/n)) / n"""
    total = 0.0
    for n in range(1, N+1):
        total += M[N // n] / n
    return total

def compute_Istar(N, M):
    """I*(p) = sum_{n=1}^{N} M(floor(N/n)) / (N+1-n)"""
    total = 0.0
    for n in range(1, N+1):
        total += M[N // n] / (N + 1 - n)
    return total

def compute_lambda_energy(N, M):
    """sum |lambda_p(n)|^2 = sum M(floor(N/n))^2"""
    total = 0
    for n in range(1, N+1):
        total += M[N // n] ** 2
    return total

# Compute for primes up to 5000
print(f"{'p':>6} {'N':>6} {'I(p)':>10} {'I*(p)':>10} {'I-I*':>10} "
      f"{'I/logp':>10} {'(I-I*)/logp':>12} {'|I-I*|^2/p':>12} "
      f"{'|I-I*|^2/(p*logp)':>18}")
print("-" * 120)

max_N = 10000
M = mertens_table(max_N)

for p in primerange(3, 10001):
    N = p - 1
    if N > max_N:
        break
    Ip = compute_I(N, M)
    Istar = compute_Istar(N, M)
    diff = Ip - Istar
    logp = np.log(p)

    print(f"{p:6d} {N:6d} {Ip:10.4f} {Istar:10.4f} {diff:10.4f} "
          f"{Ip/logp:10.4f} {diff/logp:12.4f} {diff**2/p:12.4f} "
          f"{diff**2/(p*logp):18.4f}")
