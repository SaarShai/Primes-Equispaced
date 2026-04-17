#!/usr/bin/env python3
"""
Test the Deep Riemann Hypothesis (DRH) numerically via partial Euler products.

What this script does:
1. Computes E_P(1/2 + i*gamma_j) = prod_{p<=P} (1 - p^{-1/2-i*gamma_j})^{-1}
   for P in {10, 30, 100, 500} at the first 100 zeta zeros.
2. Computes E_P at 1000 generic points t in [0, 500], chosen uniformly and
   rejected if they fall too close to any zero below 500.
3. Reports mean/max |E_P| at zeros versus generic points and the amplification
   ratio mean_at_zeros / mean_at_generic.
4. Computes a finite Möbius truncation
      c_P(s) = sum_{1 <= n <= P} mu(n) * n^{-s}
   which is the requested smooth-number/Mobius diagnostic truncation.
   Because n <= P, the "P-smooth" condition is automatic; only squarefree n
   contribute. The exact inverse of the finite Euler product would require the
   infinite squarefree P-smooth sum, so this finite sum is a practical
   approximation.
5. Prints a summary table, including a check of the approximate inverse relation
   E_P(s) * c_P(s) ~ 1 at the zeros.

Requirements satisfied:
- mp.dps = 30
- uses mpmath.zetazero(j).imag
- primes precomputed by sympy.primerange if available, otherwise manual sieve
- partial Euler product computed term by term
- no files written
"""

import random
from mpmath import mp

try:
    from sympy import primerange
except Exception:
    primerange = None

mp.dps = 30


P_VALUES = [10, 30, 100, 500]
T_MAX = mp.mpf("500")
N_ZERO_SAMPLE = 100
N_GENERIC = 1000
AVOID_TOL = mp.mpf("0.1")
GENERIC_SEED = 20260412


def fmt(x, digits=10):
    if x == mp.inf:
        return "inf"
    return mp.nstr(x, digits)


def primes_upto(n):
    """Return all primes <= n using sympy.primerange if available."""
    if n < 2:
        return []
    if primerange is not None:
        return [int(p) for p in primerange(2, n + 1)]
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    limit = int(n**0.5)
    for p in range(2, limit + 1):
        if sieve[p]:
            start = p * p
            sieve[start : n + 1 : p] = b"\x00" * (((n - start) // p) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]


def mobius_sieve(n, primes):
    """
    Möbius sieve up to n.

    mu[1] = 1
    mu[n] = 0 if n has a squared prime factor
    mu[n] = (-1)^k if n is a product of k distinct primes
    """
    mu = [1] * (n + 1)
    mu[0] = 0
    for p in primes:
        for k in range(p, n + 1, p):
            mu[k] = -mu[k]
        p2 = p * p
        if p2 <= n:
            for k in range(p2, n + 1, p2):
                mu[k] = 0
    return mu


def partial_euler_product(s, primes):
    """Compute E_P(s) = prod_{p<=P} (1 - p^{-s})^{-1} term by term."""
    prod = mp.mpc(1)
    for p in primes:
        prod *= 1 / (1 - mp.power(p, -s))
    return prod


def finite_mobius_truncation(s, K, mu):
    """
    Finite Möbius truncation:
        c_K(s) = sum_{1 <= n <= K} mu(n) * n^{-s}

    Since n <= K, every n is automatically K-smooth. Only squarefree n
    contribute because mu(n)=0 for nonsquarefree n.
    """
    total = mp.mpc(0)
    for n in range(1, K + 1):
        if mu[n] != 0:
            total += mu[n] * mp.power(n, -s)
    return total


def zeros_up_to(t_max):
    """Return all nontrivial zeta zero ordinates gamma_j with gamma_j <= t_max."""
    zeros = []
    j = 1
    while True:
        z = mp.zetazero(j)
        t = mp.mpf(z.imag)
        if t > t_max:
            break
        zeros.append(t)
        j += 1
    return zeros


def min_distance_to_points(x, points):
    if not points:
        return mp.inf
    return min(abs(x - y) for y in points)


def generic_points_uniform(n_points, t_max, zeros_to_avoid, tol, seed=0):
    """
    Draw uniform points in [0, t_max], rejecting points closer than tol to any
    zero in zeros_to_avoid.
    """
    rng = random.Random(seed)
    points = []
    attempts = 0
    max_attempts = 200000
    while len(points) < n_points:
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError("Failed to generate enough generic points; try a smaller tolerance.")
        t = mp.mpf(rng.random()) * t_max
        if min_distance_to_points(t, zeros_to_avoid) >= tol:
            points.append(t)
    return points


def mean_abs(values):
    return sum(values, mp.mpf("0")) / len(values)


def analyze_cutoff(P, zero_ts, generic_ts, mu, primes_all):
    primes = [p for p in primes_all if p <= P]

    zero_abs_E = []
    zero_abs_c = []
    zero_inv_defect = []

    for t in zero_ts:
        s = mp.mpc(mp.mpf("0.5"), t)
        E = partial_euler_product(s, primes)
        c = finite_mobius_truncation(s, P, mu)
        zero_abs_E.append(abs(E))
        zero_abs_c.append(abs(c))
        zero_inv_defect.append(abs(E * c - 1))

    generic_abs_E = []
    for t in generic_ts:
        s = mp.mpc(mp.mpf("0.5"), t)
        E = partial_euler_product(s, primes)
        generic_abs_E.append(abs(E))

    mean_zero = mean_abs(zero_abs_E)
    mean_generic = mean_abs(generic_abs_E)
    max_zero = max(zero_abs_E)
    max_generic = max(generic_abs_E)
    amp_ratio = mean_zero / mean_generic if mean_generic != 0 else mp.inf

    return {
        "P": P,
        "nprimes": len(primes),
        "mean_zero": mean_zero,
        "mean_generic": mean_generic,
        "max_zero": max_zero,
        "max_generic": max_generic,
        "amp_ratio": amp_ratio,
        "mean_c_zero": mean_abs(zero_abs_c),
        "mean_inv_defect": mean_abs(zero_inv_defect),
    }


def main():
    max_P = max(P_VALUES)

    print(f"mp.dps = {mp.dps}")
    print(f"Computing primes up to {max_P}...")
    primes_all = primes_upto(max_P)
    mu = mobius_sieve(max_P, primes_all)

    print(f"Computing zeta zeros up to {T_MAX} for generic-point rejection...")
    all_zeros = zeros_up_to(T_MAX)
    zero_sample = all_zeros[:N_ZERO_SAMPLE]

    if len(zero_sample) < N_ZERO_SAMPLE:
        raise RuntimeError("Not enough zeta zeros below t=500 to form the first 100 zeros sample.")

    print(f"Generating {N_GENERIC} generic points in [0, {T_MAX}] with rejection tolerance {AVOID_TOL}...")
    generic_ts = generic_points_uniform(
        N_GENERIC,
        T_MAX,
        all_zeros,
        AVOID_TOL,
        seed=GENERIC_SEED,
    )

    rows = []
    for P in P_VALUES:
        print(f"Analyzing P = {P}...")
        rows.append(analyze_cutoff(P, zero_sample, generic_ts, mu, primes_all))

    print()
    print("DRH / partial Euler product summary")
    print(f"Zero sample: first {N_ZERO_SAMPLE} zeta zeros (gamma_j = mpmath.zetazero(j).imag)")
    print(f"Generic sample: {N_GENERIC} uniform points in [0, {T_MAX}]")
    print(
        "Generic points are rejected if they fall within "
        f"{AVOID_TOL} of any zeta zero with gamma <= {T_MAX}."
    )
    print()

    header = (
        f"{'P':>5} {'#primes':>7} "
        f"{'mean|E|_zeros':>16} {'mean|E|_generic':>16} "
        f"{'max|E|_zeros':>16} {'max|E|_generic':>16} "
        f"{'amp ratio':>12} "
        f"{'mean|c_P|_zeros':>16} {'mean|E*c_P-1|_zeros':>20}"
    )
    print(header)
    print("-" * len(header))

    for row in rows:
        print(
            f"{row['P']:>5d} {row['nprimes']:>7d} "
            f"{fmt(row['mean_zero'], 10):>16} {fmt(row['mean_generic'], 10):>16} "
            f"{fmt(row['max_zero'], 10):>16} {fmt(row['max_generic'], 10):>16} "
            f"{fmt(row['amp_ratio'], 10):>12} "
            f"{fmt(row['mean_c_zero'], 10):>16} {fmt(row['mean_inv_defect'], 10):>20}"
        )

    print()
    print("Interpretation:")
    print("- Amplification ratio > 1 means |E_P| is larger at zeros than at generic points.")
    print("- If the ratio grows with P, that is consistent with the DRH-style pole effect.")
    print("- Mean |E_P * c_P - 1| near zero indicates the finite Möbius truncation is")
    print("  behaving like an approximate inverse to the partial Euler product.")


if __name__ == "__main__":
    main()
