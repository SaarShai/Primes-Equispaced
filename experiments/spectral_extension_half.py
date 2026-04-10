#!/usr/bin/env python3
"""
SPECTRAL EXTENSION TO s=1/2: NUMERICAL EXPLORATION
====================================================

We explore whether the spectral formula connecting Farey per-step discrepancy
to L(1,chi) can be extended to L(1/2,chi).

CURRENT FORMULA (at s=1):
  The per-step discrepancy kernel K_p has Fourier eigenvalues related to
  |L(1,chi)|^2 for Dirichlet characters chi mod p.

APPROACHES TO s=1/2:
  1. Higher-order Dedekind sums with Bernoulli B_m polynomials -> L(m,chi)
  2. Modified weighting kernel that shifts the eigenvalue from L(1) to L(1/2)
  3. Mellin transform of the step-discrepancy function evaluated at s=1/2
  4. Nyman-Beurling fractional-part kernel approach

We compute candidate formulas and check numerically.
"""

import numpy as np
from math import gcd, isqrt, pi, sqrt, log, exp
from fractions import Fraction
import time
import sys

start = time.time()

# ============================================================
# SIEVE AND ARITHMETIC UTILITIES
# ============================================================

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def mobius_sieve(limit):
    sp = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if sp[i] == 0:
            for j in range(i, limit + 1, i):
                if sp[j] == 0:
                    sp[j] = i
    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        p = sp[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]
    M = [0] * (limit + 1)
    s = 0
    for k in range(1, limit + 1):
        s += mu[k]
        M[k] = s
    return mu, M

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


# ============================================================
# DIRICHLET CHARACTERS AND L-FUNCTIONS
# ============================================================

def primitive_root(p):
    """Find a primitive root mod p (for prime p)."""
    if p == 2:
        return 1
    phi = p - 1
    factors = set()
    n = phi
    for f in range(2, isqrt(n) + 2):
        if n % f == 0:
            factors.add(f)
            while n % f == 0:
                n //= f
    if n > 1:
        factors.add(n)

    for g in range(2, p):
        ok = True
        for f in factors:
            if pow(g, phi // f, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None

def dirichlet_characters(p):
    """
    Return all Dirichlet characters mod p (prime p).
    Returns list of arrays chi where chi[a] = chi(a) for 0 <= a < p.
    chi[0] = 0 for all non-principal characters.
    """
    g = primitive_root(p)
    if g is None:
        return []

    # Build discrete log table
    dlog = [0] * p
    val = 1
    for k in range(p - 1):
        dlog[val] = k
        val = (val * g) % p

    chars = []
    for j in range(p - 1):  # j indexes the character
        omega = np.exp(2j * pi * j / (p - 1))
        chi = np.zeros(p, dtype=complex)
        for a in range(1, p):
            chi[a] = omega ** dlog[a]
        chars.append(chi)

    return chars

def L_function(s, chi, num_terms=10000):
    """
    Compute L(s, chi) = sum_{n=1}^{num_terms} chi(n) / n^s.
    chi is an array of length p where chi[a] = chi(a mod p).
    """
    p = len(chi)
    result = 0.0 + 0.0j
    for n in range(1, num_terms + 1):
        result += chi[n % p] / n**s
    return result

def L_function_fast(s, chi_vals, p, num_terms=50000):
    """
    Faster L-function computation using vectorized operations.
    chi_vals: array of length p with character values.
    """
    ns = np.arange(1, num_terms + 1, dtype=np.float64)
    residues = ns.astype(int) % p
    chi_n = chi_vals[residues]
    return np.sum(chi_n / ns**s)


# ============================================================
# FAREY SEQUENCE AND DISCREPANCY
# ============================================================

def farey_generator(N):
    """Generate Farey sequence F_N as (a,b) pairs."""
    a, b = 0, 1
    c, d = 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b

def compute_wobble_and_discrepancies(N):
    """
    Compute Farey sequence F_N, wobble W(N), and return arrays of:
    - fracs: the Farey fractions as floats
    - discs: the discrepancies f_j - j/n
    """
    fracs = []
    for a, b in farey_generator(N):
        fracs.append(a / b)
    fracs = np.array(fracs)
    n = len(fracs)
    ideal = np.arange(n, dtype=np.float64) / n
    discs = fracs - ideal
    W = np.dot(discs, discs)
    return fracs, discs, W, n


# ============================================================
# APPROACH 1: Higher-order Dedekind sums
# ============================================================

def generalized_dedekind_sum(h, k, m):
    """
    Compute the generalized Dedekind sum s_m(h,k) using
    periodized Bernoulli polynomial B_m.

    s_m(h,k) = sum_{j=0}^{k-1} B_bar_1(j/k) * B_bar_m(jh/k)

    where B_bar_m(x) = B_m({x}) is the periodic Bernoulli polynomial.

    For m=1: this is the classical Dedekind sum s(h,k).
    For general m: connects to L(m, chi) via character decomposition.
    """
    from scipy.special import bernoulli as bernoulli_coeffs

    # Get Bernoulli polynomial coefficients
    # B_m(x) = sum_{j=0}^{m} C(m,j) * B_j * x^{m-j}
    bern = bernoulli_coeffs(m)

    def B_poly(m_val, x):
        """Evaluate B_m(x) using Bernoulli numbers."""
        result = 0.0
        bern_m = bernoulli_coeffs(m_val)
        for j in range(m_val + 1):
            from math import comb
            result += comb(m_val, j) * bern_m[j] * x**(m_val - j)
        return result

    def B_bar(m_val, x):
        """Periodic Bernoulli function."""
        return B_poly(m_val, x - int(x))

    total = 0.0
    for j in range(k):
        total += B_bar(1, j / k) * B_bar(m, (j * h) / k)
    return total


# ============================================================
# APPROACH 2: Modified kernel for L(1/2, chi)
# ============================================================

def compute_weighted_discrepancy_s(N, s_val, phi_arr=None):
    """
    Compute a weighted discrepancy sum where each fraction a/b
    is weighted by b^{1-2s}.

    The idea: if the standard discrepancy sum (uniform weights)
    gives eigenvalues ~ |L(1,chi)|^2, then weighting by b^{1-2s}
    should shift the spectral information to L(s,chi).

    For s=1: weight = b^{-1}, recovering (roughly) the standard formula.
    For s=1/2: weight = b^{0} = 1, so all fractions weighted equally.

    Returns: sum_{a/b in F_N} w(b) * (f_j - j/n)^2  with w(b) = b^{1-2s}
    """
    total = 0.0
    fracs = []
    denoms = []
    for a, b in farey_generator(N):
        fracs.append(a / b)
        denoms.append(b)

    fracs = np.array(fracs)
    denoms = np.array(denoms, dtype=np.float64)
    n = len(fracs)
    ideal = np.arange(n, dtype=np.float64) / n
    discs = fracs - ideal

    weights = denoms ** (1 - 2 * s_val)
    return np.sum(weights * discs**2), np.sum(weights * discs), n


def compute_character_weighted_discrepancy(N, chi_vals, p):
    """
    Compute sum_{a/b in F_N} chi(b) * (f_j - j/n)^2

    If characters diagonalize this, the eigenvalue should relate to
    some L-function value.
    """
    total = 0.0 + 0.0j
    fracs = []
    denoms = []
    for a, b in farey_generator(N):
        fracs.append(a / b)
        denoms.append(b)

    fracs_arr = np.array(fracs)
    denoms_arr = np.array(denoms, dtype=int)
    n = len(fracs_arr)
    ideal = np.arange(n, dtype=np.float64) / n
    discs = fracs_arr - ideal

    chi_weights = chi_vals[denoms_arr % p]
    return np.sum(chi_weights * discs**2)


# ============================================================
# APPROACH 3: Mellin transform of step-discrepancy
# ============================================================

def mellin_step_discrepancy(N, s_val, mu, M):
    """
    Compute a Mellin-type transform of the step-discrepancy.

    The Farey discrepancy function D(x) = #{f in F_N : f <= x} - n*x
    has the property that its "Dirichlet series" relates to zeta.

    We compute: sum_{k=1}^{N} |M(N/k)|^2 / k^{2s}

    At s=1: this is the Franel-Landau sum (related to W(N))
    At s=1/2: this gives a sum weighted by 1/k, which should
    relate to L-function values at the critical line.
    """
    total = 0.0
    for k in range(1, N + 1):
        Mk = M[N // k]
        total += Mk**2 / k**(2 * s_val)
    return total


def nyman_beurling_sum(N, s_val, mu, M):
    """
    Nyman-Beurling type sum:
    sum_{k=1}^{N} M(k) * k^{s-1}

    This is related to the Mellin transform of the Mertens function.
    At s = 1/2, this gives sum M(k) / sqrt(k), which under RH is O(N^epsilon).
    """
    total = 0.0
    for k in range(1, N + 1):
        total += M[k] * k**(s_val - 1)
    return total


# ============================================================
# APPROACH 4: Fractional-part kernel (Nyman-Beurling style)
# ============================================================

def fractional_part_kernel_sum(N, s_val):
    """
    Compute the kernel sum K_s(N) = sum_{a/b in F_N} {b * s_val} * disc(a/b)
    where {x} = x - floor(x) is the fractional part.

    This is inspired by the Nyman-Beurling criterion where
    rho(x) = {1/x} - 1/x plays a key role.
    """
    total = 0.0
    fracs = []
    denoms = []
    for a, b in farey_generator(N):
        fracs.append(a / b)
        denoms.append(b)

    fracs_arr = np.array(fracs)
    denoms_arr = np.array(denoms, dtype=np.float64)
    n = len(fracs_arr)
    ideal = np.arange(n, dtype=np.float64) / n
    discs = fracs_arr - ideal

    # Weight by {b^s / N^s}
    weights = (denoms_arr / N) ** s_val
    return np.sum(weights * discs**2)


# ============================================================
# MAIN COMPUTATION
# ============================================================

def main():
    print("=" * 78)
    print("SPECTRAL EXTENSION TO s=1/2: NUMERICAL EXPLORATION")
    print("=" * 78)

    LIMIT = 500
    phi_arr = euler_totient_sieve(LIMIT)
    mu, M = mobius_sieve(LIMIT)
    primes = sieve_primes(LIMIT)

    # -------------------------------------------------------
    # PART 1: Baseline — L(1, chi) and standard wobble
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("PART 1: L(1,chi) vs L(1/2,chi) for small primes")
    print("Computing L-function values and Farey discrepancies...")
    print("=" * 78)

    test_primes = [p for p in primes if 5 <= p <= 97]

    print(f"\n{'p':>4s}  {'W(p-1)':>12s}  {'sum|L(1,chi)|^2':>16s}  "
          f"{'sum|L(1/2,chi)|^2':>18s}  {'ratio_1':>10s}  {'ratio_half':>12s}")
    print("-" * 80)

    results = []
    for p in test_primes:
        N = p - 1
        fracs, discs, W, n = compute_wobble_and_discrepancies(N)

        # Compute all Dirichlet characters mod p
        chars = dirichlet_characters(p)

        # Compute sum of |L(1,chi)|^2 and |L(1/2,chi)|^2 over non-principal chars
        sum_L1_sq = 0.0
        sum_Lhalf_sq = 0.0

        for j, chi in enumerate(chars):
            if j == 0:  # skip principal character
                continue
            L1 = L_function_fast(1.0, chi, p, num_terms=20000)
            Lhalf = L_function_fast(0.5, chi, p, num_terms=20000)
            sum_L1_sq += abs(L1)**2
            sum_Lhalf_sq += abs(Lhalf)**2

        ratio_1 = W * p / sum_L1_sq if sum_L1_sq > 0 else float('inf')
        ratio_half = W * p / sum_Lhalf_sq if sum_Lhalf_sq > 0 else float('inf')

        print(f"{p:4d}  {W:12.8f}  {sum_L1_sq:16.6f}  "
              f"{sum_Lhalf_sq:18.6f}  {ratio_1:10.6f}  {ratio_half:12.6f}")

        results.append({
            'p': p, 'W': W, 'n': n,
            'sum_L1_sq': sum_L1_sq, 'sum_Lhalf_sq': sum_Lhalf_sq,
            'ratio_1': ratio_1, 'ratio_half': ratio_half,
        })

    # -------------------------------------------------------
    # PART 2: Character-weighted discrepancy
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("PART 2: Character-weighted discrepancy sums")
    print("sum chi(b) * disc(a/b)^2 vs |L(s,chi)|^2")
    print("=" * 78)

    for p in [7, 11, 13, 17, 23]:
        if p > LIMIT:
            continue
        N = p - 1
        chars = dirichlet_characters(p)

        print(f"\n  p = {p}, N = {N}:")
        print(f"  {'j':>3s}  {'sum chi*disc^2':>16s}  {'|L(1,chi)|^2':>14s}  "
              f"{'|L(1/2,chi)|^2':>16s}  {'ratio_1':>10s}  {'ratio_1/2':>12s}")
        print("  " + "-" * 78)

        for j, chi in enumerate(chars):
            if j == 0:
                continue

            chi_disc_sq = compute_character_weighted_discrepancy(N, chi, p)
            L1 = L_function_fast(1.0, chi, p, num_terms=20000)
            Lhalf = L_function_fast(0.5, chi, p, num_terms=20000)

            L1_sq = abs(L1)**2
            Lhalf_sq = abs(Lhalf)**2

            r1 = abs(chi_disc_sq) / L1_sq if L1_sq > 1e-15 else float('inf')
            rhalf = abs(chi_disc_sq) / Lhalf_sq if Lhalf_sq > 1e-15 else float('inf')

            print(f"  {j:3d}  {abs(chi_disc_sq):16.8f}  {L1_sq:14.6f}  "
                  f"{Lhalf_sq:16.6f}  {r1:10.6f}  {rhalf:12.6f}")

    # -------------------------------------------------------
    # PART 3: Weight by b^{1-2s} to shift eigenvalues
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("PART 3: Weighted discrepancy sum_b b^{1-2s} * disc^2")
    print("Testing if weight b^{1-2s} shifts eigenvalue from L(1) to L(s)")
    print("=" * 78)

    print(f"\n{'p':>4s}  {'W_s1':>12s}  {'W_s05':>12s}  {'W_s0':>12s}  "
          f"{'sum|L1|^2':>12s}  {'sum|L05|^2':>12s}  "
          f"{'r(s=1)':>10s}  {'r(s=.5)':>10s}")
    print("-" * 90)

    for p in test_primes[:10]:
        N = p - 1
        W_s1, _, n = compute_weighted_discrepancy_s(N, 1.0)
        W_s05, _, _ = compute_weighted_discrepancy_s(N, 0.5)
        W_s0, _, _ = compute_weighted_discrepancy_s(N, 0.0)

        chars = dirichlet_characters(p)
        sum_L1_sq = 0.0
        sum_Lhalf_sq = 0.0
        for j, chi in enumerate(chars):
            if j == 0:
                continue
            L1 = L_function_fast(1.0, chi, p, num_terms=20000)
            Lhalf = L_function_fast(0.5, chi, p, num_terms=20000)
            sum_L1_sq += abs(L1)**2
            sum_Lhalf_sq += abs(Lhalf)**2

        r1 = W_s1 * p / sum_L1_sq if sum_L1_sq > 0 else float('inf')
        r05 = W_s05 * p / sum_Lhalf_sq if sum_Lhalf_sq > 0 else float('inf')

        print(f"{p:4d}  {W_s1:12.6f}  {W_s05:12.6f}  {W_s0:12.6f}  "
              f"{sum_L1_sq:12.6f}  {sum_Lhalf_sq:12.6f}  "
              f"{r1:10.6f}  {r05:10.6f}")

    # -------------------------------------------------------
    # PART 4: Mellin-type transform at different s
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("PART 4: Mellin-type sums sum M(N/k)^2 / k^{2s}")
    print("=" * 78)

    print(f"\n{'N':>5s}  {'s=1.0':>12s}  {'s=0.75':>12s}  {'s=0.5':>12s}  "
          f"{'s=0.25':>12s}  {'N*W(N)':>12s}")
    print("-" * 70)

    for N in [10, 20, 50, 100, 200, 500]:
        if N > LIMIT:
            continue
        fracs, discs, W, n = compute_wobble_and_discrepancies(N)

        m1 = mellin_step_discrepancy(N, 1.0, mu, M)
        m075 = mellin_step_discrepancy(N, 0.75, mu, M)
        m05 = mellin_step_discrepancy(N, 0.5, mu, M)
        m025 = mellin_step_discrepancy(N, 0.25, mu, M)

        print(f"{N:5d}  {m1:12.4f}  {m075:12.4f}  {m05:12.4f}  "
              f"{m025:12.4f}  {N*W:12.8f}")

    # -------------------------------------------------------
    # PART 5: The key test — does sum chi(b)|disc|^2 / |L(s,chi)|^2
    #         become constant for some specific s?
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("PART 5: CRITICAL TEST")
    print("For each character chi mod p, compute:")
    print("  R(s) = sum_{a/b in F_N} chi(b) disc^2 / |L(s,chi)|^2")
    print("If R(s) is constant across characters for some s, we have a spectral formula.")
    print("=" * 78)

    for p in [7, 11, 13, 17]:
        N = p - 1
        chars = dirichlet_characters(p)

        print(f"\n  p = {p}:")

        for s_val in [1.0, 0.75, 0.5]:
            ratios = []
            for j, chi in enumerate(chars):
                if j == 0:
                    continue
                chi_disc = compute_character_weighted_discrepancy(N, chi, p)
                Ls = L_function_fast(s_val, chi, p, num_terms=30000)
                Ls_sq = abs(Ls)**2
                if Ls_sq > 1e-15:
                    ratios.append(abs(chi_disc) / Ls_sq)

            if ratios:
                ratios = np.array(ratios)
                cv = np.std(ratios) / np.mean(ratios) if np.mean(ratios) > 0 else float('inf')
                print(f"    s={s_val:.2f}: mean(R)={np.mean(ratios):.6f}, "
                      f"std={np.std(ratios):.6f}, CV={cv:.4f}, "
                      f"min={np.min(ratios):.6f}, max={np.max(ratios):.6f}")

    # -------------------------------------------------------
    # PART 6: Approach 4 — modified KERNEL instead of modified s
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("PART 6: Modified kernel approach")
    print("Instead of changing s, change the kernel K(x,y).")
    print("The Karvonen-Zhigljavsky Matern-1/2 kernel gives RH equivalence.")
    print("We test: K_alpha(x,y) = sum_{m=1}^{inf} e(m(x-y)) / m^alpha")
    print("At alpha=2: standard L2 discrepancy -> L(1,chi)")
    print("At alpha=1: Matern-1/2 -> should relate to L(1/2,chi)")
    print("=" * 78)

    for p in [7, 11, 13, 17, 23]:
        N = p - 1
        fracs_list = []
        denoms_list = []
        for a, b in farey_generator(N):
            fracs_list.append(a / b)
            denoms_list.append(b)
        fracs_arr = np.array(fracs_list)
        denoms_arr = np.array(denoms_list)
        n_frac = len(fracs_arr)

        print(f"\n  p = {p}, N = {N}, n = {n_frac}:")

        for alpha in [2.0, 1.5, 1.0]:
            # Compute kernel discrepancy: sum_{m=1}^{H} (1/m^alpha) * |S_m|^2 / n^2
            # where S_m = sum_{f in F_N} e(m*f)
            H = min(500, 10 * p)
            kernel_disc = 0.0
            for m in range(1, H + 1):
                Sm = np.sum(np.exp(2j * pi * m * fracs_arr))
                kernel_disc += abs(Sm)**2 / m**alpha
            kernel_disc /= n_frac**2

            # Compare to character sums
            chars = dirichlet_characters(p)

            # The theoretical prediction for alpha=2 is related to sum |L(1,chi)|^2
            # For alpha=1 it should relate to sum |L(1/2,chi)|^2  (THIS IS THE KEY)
            sum_L1_sq = 0.0
            sum_Lhalf_sq = 0.0
            sum_L3q_sq = 0.0
            for j, chi in enumerate(chars):
                if j == 0:
                    continue
                L1 = L_function_fast(1.0, chi, p, num_terms=20000)
                Lhalf = L_function_fast(0.5, chi, p, num_terms=20000)
                L3q = L_function_fast(0.75, chi, p, num_terms=20000)
                sum_L1_sq += abs(L1)**2
                sum_Lhalf_sq += abs(Lhalf)**2
                sum_L3q_sq += abs(L3q)**2

            # The key ratios
            r1 = kernel_disc * n_frac * p / sum_L1_sq if sum_L1_sq > 0 else 0
            r05 = kernel_disc * n_frac * p / sum_Lhalf_sq if sum_Lhalf_sq > 0 else 0
            r_alpha = kernel_disc * n_frac * p / sum_L3q_sq if sum_L3q_sq > 0 else 0

            s_match = alpha / 2.0  # Hypothesis: alpha kernel -> L(alpha/2)
            print(f"    alpha={alpha:.1f}: K_disc={kernel_disc:.8f}  "
                  f"r_L(1)={r1:.6f}  r_L(.75)={r_alpha:.6f}  r_L(.5)={r05:.6f}  "
                  f"(expect stable at s={s_match:.2f})")

    # -------------------------------------------------------
    # PART 7: Direct test of alpha/2 hypothesis
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("PART 7: DIRECT HYPOTHESIS TEST")
    print("Hypothesis: K_alpha discrepancy ~ C * sum |L(alpha/2, chi)|^2 / (p * n)")
    print("Test: ratio should be constant across primes p")
    print("=" * 78)

    for alpha in [2.0, 1.5, 1.0]:
        s_target = alpha / 2.0
        print(f"\n  alpha = {alpha:.1f}, target s = {s_target:.2f}:")
        print(f"  {'p':>4s}  {'K_disc':>14s}  {'sum|L(s)|^2':>14s}  {'ratio':>12s}")
        print("  " + "-" * 50)

        for p in [7, 11, 13, 17, 23, 29, 31, 37, 41, 43]:
            N = p - 1
            fracs_arr = np.array([a/b for a,b in farey_generator(N)])
            n_frac = len(fracs_arr)

            H = min(500, 10 * p)
            kernel_disc = 0.0
            for m in range(1, H + 1):
                Sm = np.sum(np.exp(2j * pi * m * fracs_arr))
                kernel_disc += abs(Sm)**2 / m**alpha
            kernel_disc /= n_frac**2

            chars = dirichlet_characters(p)
            sum_Ls_sq = 0.0
            for j, chi in enumerate(chars):
                if j == 0:
                    continue
                Ls = L_function_fast(s_target, chi, p, num_terms=20000)
                sum_Ls_sq += abs(Ls)**2

            ratio = kernel_disc * n_frac * p / sum_Ls_sq if sum_Ls_sq > 0 else 0
            print(f"  {p:4d}  {kernel_disc:14.8f}  {sum_Ls_sq:14.6f}  {ratio:12.6f}")

    elapsed = time.time() - start
    print(f"\n\nTotal time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
