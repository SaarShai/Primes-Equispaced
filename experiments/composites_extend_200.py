#!/usr/bin/env python3
"""
Extend composite healing check to N=200 with float arithmetic (faster).
Focus on finding ALL non-healing composites and characterizing them.
"""

from math import gcd
import numpy as np


def euler_phi(n):
    result = n
    temp = n
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True


def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def classify(n):
    factors = factorize(n)
    parts = []
    for p in sorted(factors):
        if factors[p] == 1:
            parts.append(str(p))
        else:
            parts.append(f"{p}^{factors[p]}")
    return " * ".join(parts)


def largest_prime_factor(n):
    lpf = 1
    d = 2
    while d * d <= n:
        while n % d == 0:
            lpf = d
            n //= d
        d += 1
    if n > 1:
        lpf = n
    return lpf


def compute_wobble(sorted_fracs):
    n = len(sorted_fracs)
    if n <= 1:
        return 0.0
    ideal = np.linspace(0, 1, n)
    deltas = sorted_fracs - ideal
    return float(np.dot(deltas, deltas))


def mertens_function(max_n):
    mu = [0] * (max_n + 1)
    mu[1] = 1
    is_p = [True] * (max_n + 1)
    is_p[0] = is_p[1] = False
    primes = []
    for i in range(2, max_n + 1):
        if is_p[i]:
            primes.append(i)
            mu[i] = -1
        for q in primes:
            if i * q > max_n: break
            is_p[i * q] = False
            if i % q == 0:
                mu[i * q] = 0
                break
            else:
                mu[i * q] = -mu[i]
    M = [0] * (max_n + 1)
    for k in range(1, max_n + 1):
        M[k] = M[k - 1] + mu[k]
    return M


def main():
    MAX_N = 300

    print(f"Computing wobbles for all N up to {MAX_N}...")

    frac_set = {0.0, 1.0}
    wobbles = [0.0] * (MAX_N + 1)
    wobbles[1] = compute_wobble(np.array([0.0, 1.0]))

    for N in range(2, MAX_N + 1):
        for a in range(1, N):
            if gcd(a, N) == 1:
                frac_set.add(a / N)
        sorted_arr = np.array(sorted(frac_set))
        wobbles[N] = compute_wobble(sorted_arr)

    M = mertens_function(MAX_N)

    # Find all non-healing composites
    nonhealing = []
    total_comp = 0

    for N in range(4, MAX_N + 1):
        if is_prime(N):
            continue
        total_comp += 1
        dW = wobbles[N-1] - wobbles[N]
        if dW <= 1e-15:  # account for float precision
            lpf = largest_prime_factor(N)
            omega = len(factorize(N))
            nonhealing.append({
                'N': N,
                'dW': dW,
                'fact': classify(N),
                'phi_N': euler_phi(N),
                'phi_ratio': euler_phi(N) / N,
                'lpf': lpf,
                'lpf_ratio': lpf / N,
                'omega': omega,
                'M_N': M[N],
            })

    heal_rate = (total_comp - len(nonhealing)) / total_comp * 100

    print(f"\nTotal composites in [4, {MAX_N}]: {total_comp}")
    print(f"Healing: {total_comp - len(nonhealing)} ({heal_rate:.1f}%)")
    print(f"Non-healing: {len(nonhealing)} ({100 - heal_rate:.1f}%)")

    print(f"\nALL NON-HEALING COMPOSITES:")
    print(f"{'N':>5} {'Factorization':>20} {'phi/N':>7} {'LPF/N':>7} {'omega':>5} {'DeltaW':>14} {'M(N)':>5}")
    print("-" * 70)
    for e in nonhealing:
        print(f"{e['N']:5d} {e['fact']:>20s} {e['phi_ratio']:7.4f} {e['lpf_ratio']:7.4f} {e['omega']:5d} {e['dW']:14.2e} {e['M_N']:5d}")

    # Analysis: are all non-healing composites of form 2*p with large p?
    print(f"\nPATTERN CHECK:")
    for e in nonhealing:
        N = e['N']
        if N % 2 == 0 and is_prime(N // 2):
            p = N // 2
            print(f"  N={N} = 2*{p}  M(N)={e['M_N']}  M({p})={M[p]}  M({N-1})={M[N-1]}")
        else:
            print(f"  N={N} = {e['fact']}  NOT of form 2*p!")

    # Check 2*p specifically: which ones heal, which don't?
    print(f"\n2*p ANALYSIS (all 2*p composites):")
    print(f"{'N':>5} {'p':>5} {'DeltaW':>14} {'Heals':>6} {'M(N)':>5} {'M(p)':>5} {'M(N-1)':>6}")
    for N in range(6, MAX_N + 1, 2):
        p = N // 2
        if not is_prime(p) or p <= 2:
            continue
        dW = wobbles[N-1] - wobbles[N]
        heals = dW > 1e-15
        print(f"{N:5d} {p:5d} {dW:14.6e} {'YES' if heals else '**NO**':>6s} {M[N]:5d} {M[p]:5d} {M[N-1]:6d}")


if __name__ == '__main__':
    main()
