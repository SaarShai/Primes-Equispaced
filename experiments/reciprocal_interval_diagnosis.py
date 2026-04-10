#!/usr/bin/env python3
"""
Compare the Cauchy-Schwarz lower bound with the actual spectral sum.
Diagnose exactly HOW MUCH Cauchy-Schwarz loses.
"""
import numpy as np
import math

def mertens_table(N):
    mu = np.zeros(N+1, dtype=np.int64)
    mu[1] = 1
    for i in range(1, N+1):
        for j in range(2*i, N+1, i):
            mu[j] -= mu[i]
    return np.cumsum(mu)

def dirichlet_chars(p):
    """Compute all Dirichlet characters mod p using discrete log."""
    # Find primitive root
    for g in range(2, p):
        seen = set()
        val = 1
        for _ in range(p-1):
            seen.add(val)
            val = (val * g) % p
        if len(seen) == p-1:
            break

    # Discrete log table
    dlog = [0] * p
    val = 1
    for k in range(p-1):
        dlog[val] = k
        val = (val * g) % p

    # Characters: chi_j(n) = omega^(j * dlog[n]) where omega = e^(2*pi*i/(p-1))
    omega = np.exp(2j * np.pi / (p-1))

    chars = []
    parity = []  # +1 for even, -1 for odd
    for j in range(p-1):
        chi = np.zeros(p, dtype=complex)
        for n in range(1, p):
            chi[n] = omega ** (j * dlog[n])
        chars.append(chi)
        # Parity: chi(-1) = chi(p-1) = omega^(j * dlog[p-1])
        # dlog[p-1] = (p-1)/2 since g^((p-1)/2) = -1 mod p
        par = omega ** (j * (p-1)//2)
        parity.append(round(par.real))

    return chars, parity, dlog

max_N = 2000
M = mertens_table(max_N)

print(f"{'p':>5} {'actual_sum':>12} {'CS_bound':>12} {'ratio':>8} "
      f"{'actual/(p^2*logp)':>20} {'CS/(p^2*logp)':>15}")
print("-"*80)

from sympy import primerange

for p in primerange(5, 500):
    N = p - 1
    if N > max_N:
        break

    chars, parity, dlog = dirichlet_chars(p)

    # Compute lambda_p
    lam = np.zeros(N+1)
    for m in range(1, N+1):
        lam[m] = M[N // m]

    # Compute Lambda_p(chi) and L(1,chi) for odd characters
    actual_sum = 0.0
    J_real = 0.0  # Sigma_{chi odd} L(1,chi) * conj(Lambda(chi))

    for j in range(p-1):
        if parity[j] != -1:  # skip non-odd
            continue

        chi = chars[j]

        # Lambda_p(chi) = sum lambda_p(m) chi(m)
        Lambda_chi = sum(lam[m] * chi[m] for m in range(1, N+1))

        # L(1,chi) approximated by partial sum
        L1_chi = sum(chi[n] / n for n in range(1, N+1))

        actual_sum += abs(L1_chi)**2 * abs(Lambda_chi)**2
        J_real += (L1_chi * np.conj(Lambda_chi)).real

    # The J we computed from I(p):
    Ip = sum(M[N // n] / n for n in range(1, N+1))
    Istar = sum(M[N // n] / (N + 1 - n) for n in range(1, N+1))
    J_theory = (p-1)/2 * (Ip - Istar)

    # Cauchy-Schwarz bound: actual_sum >= |J|^2 / ((p-1)/2)
    num_odd = sum(1 for par in parity if par == -1)
    CS_bound = J_real**2 / num_odd if num_odd > 0 else 0

    logp = math.log(p)

    print(f"{p:5d} {actual_sum:12.2f} {CS_bound:12.2f} {actual_sum/CS_bound if CS_bound > 0 else float('inf'):8.1f} "
          f"{actual_sum/(p**2 * logp):20.6f} {CS_bound/(p**2 * logp):15.6f}")
