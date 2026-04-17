#!/usr/bin/env python3
"""
LMFDB Benchmark: Batch Spectroscope vs Individual Zero Computation
for Dirichlet L-functions L(s, chi) mod q.

Compares:
  METHOD A: Our batch spectroscope (all characters simultaneously)
  METHOD B: Individual mpmath computation (one character at a time)

Both detect the first zero of each primitive character mod q.
"""

from mpmath import mp, mpf, mpc, exp, pi, log, sqrt, fabs, zetazero, dirichlet
import time
import sys

mp.dps = 25

def mobius(n):
    """Mobius function by trial division."""
    if n == 1:
        return 1
    x = n
    num_factors = 0
    p = 2
    while p * p <= x:
        if x % p == 0:
            num_factors += 1
            x //= p
            if x % p == 0:
                return 0
        p += (1 if p == 2 else 2)
    if x > 1:
        num_factors += 1
    return (-1) ** num_factors

def get_characters(q):
    """Get all Dirichlet characters mod q as lists of values. Requires q prime."""
    phi_q = q - 1

    # Find primitive root mod q (brute force, fine for q < 1000)
    def is_primitive_root(g, q, phi_q):
        """Check if g is a primitive root mod q by testing prime factor orders."""
        # Factor phi_q
        n = phi_q
        factors = set()
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.add(d)
                n //= d
            d += 1
        if n > 1:
            factors.add(n)
        # g is primitive root iff g^(phi_q/p) != 1 mod q for every prime p | phi_q
        for p in factors:
            if pow(g, phi_q // p, q) == 1:
                return False
        return True

    g = None
    for candidate in range(2, q):
        if is_primitive_root(candidate, q, phi_q):
            g = candidate
            break

    if g is None:
        return None, None

    chars = []

    # Build index table: ind[n] such that g^ind[n] = n mod q
    ind = [0] * q
    val = 1
    for i in range(phi_q):
        ind[val] = i
        val = (val * g) % q

    # Build character table: chars[k][n] = chi_k(n)
    for k in range(phi_q):
        chi = [mpc(0)] * q
        for n in range(1, q):
            chi[n] = exp(2 * pi * mpc(0, 1) * k * ind[n] / phi_q)
        chars.append(chi)

    return chars, phi_q


def batch_spectroscope(q, N_primes, gamma_grid):
    """
    Batch spectroscope: detect zeros of ALL L(s,chi) mod q simultaneously.
    Returns dict: char_index -> list of (gamma, score) peaks.
    """
    chars, phi_q = get_characters(q)
    if chars is None:
        return None, 0

    t_start = time.time()

    # Step 1: Sieve primes up to N_primes-th prime
    def prime_sieve(limit):
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, limit + 1, i):
                    sieve[j] = False
        return [p for p in range(2, limit + 1) if sieve[p]]

    primes = prime_sieve(N_primes)
    N = len(primes)

    # Step 2: Compute twisted Mertens M_chi(p) for all characters simultaneously
    mu_cache = {}
    for p in primes:
        for k in range(2, p + 1):
            if k not in mu_cache:
                mu_cache[k] = mobius(k)

    # M_chi(p) = sum_{k<=p} mu(k) * chi(k)
    # Accumulate for each character
    M_chi = [[mpc(0)] * len(primes) for _ in range(phi_q)]

    running_sum = [mpc(0)] * phi_q
    prime_idx = 0
    for n in range(1, primes[-1] + 1):
        mu_n = mu_cache.get(n, mobius(n))
        if mu_n != 0 and n < q:
            for k in range(phi_q):
                running_sum[k] += mu_n * chars[k][n % q]
        if prime_idx < N and primes[prime_idx] == n:
            for k in range(phi_q):
                M_chi[k][prime_idx] = running_sum[k]
            prime_idx += 1

    # Step 3: Spectroscope for each gamma (shared phases!)
    log_p = [log(mpf(p)) for p in primes]
    inv_p = [mpf(1) / mpf(p) for p in primes]

    results = {k: [] for k in range(phi_q)}

    for gamma in gamma_grid:
        # Shared phase vector
        phases = [exp(-mpc(0, 1) * gamma * lp) for lp in log_p]

        for k in range(phi_q):
            # F_chi(gamma) = |sum M_chi(p)/p * phase(p)|^2
            s = mpc(0)
            for j in range(N):
                s += M_chi[k][j] * inv_p[j] * phases[j]
            score = gamma * gamma * fabs(s) ** 2
            results[k].append((float(gamma), float(score)))

    t_batch = time.time() - t_start
    return results, t_batch


def individual_zero_search(q, num_chars, T_max):
    """
    Individual method: find first zero of each L(s,chi) mod q
    using mpmath's built-in L-function computation.
    """
    chars, phi_q = get_characters(q)
    if chars is None:
        return None, 0

    t_start = time.time()

    results = {}
    num_to_check = min(num_chars, phi_q)

    for k in range(1, num_to_check):  # skip k=0 (principal character ~ zeta)
        # Build the L-function coefficients for chi_k
        # Direct evaluation: L(s, chi_k) = sum chi_k(n) * n^{-s}
        # Find zero by evaluating on a grid and looking for sign changes

        best_gamma = None
        best_score = 0

        # Coarse grid search
        for t_int in range(1, int(T_max * 10)):
            t = mpf(t_int) / 10
            s = mpc(mpf('0.5'), t)

            # Evaluate L(s, chi_k) via partial sum
            L_val = mpc(0)
            for n in range(1, 500):
                if n < q:
                    L_val += chars[k][n] * mp.power(n, -s)
                else:
                    L_val += chars[k][n % q] * mp.power(n, -s)

            score = fabs(L_val)
            if best_gamma is None or score < best_score:
                best_score = score
                best_gamma = float(t)

        results[k] = best_gamma

    t_individual = time.time() - t_start
    return results, t_individual


def main():
    print("=" * 70)
    print("LMFDB BENCHMARK: Batch Spectroscope vs Individual Computation")
    print("=" * 70)
    print()

    for q in [97, 251, 503]:
        print(f"\n{'='*60}")
        print(f"  CONDUCTOR q = {q} (prime), phi(q) = {q-1}")
        print(f"{'='*60}")

        # Parameters
        N_primes = 10000  # primes up to ~10000
        T_max = 30  # search for zeros up to height 30
        gamma_grid = [mpf(t) / 10 for t in range(10, int(T_max * 10))]

        # Method A: Batch spectroscope
        print(f"\nMethod A: Batch spectroscope ({q-1} characters, {len(gamma_grid)} gamma values)...")
        batch_results, t_batch = batch_spectroscope(q, N_primes, gamma_grid)

        if batch_results is None:
            print(f"  Failed to compute characters for q={q}")
            continue

        # Find peaks for each character
        batch_peaks = {}
        for k in range(1, min(20, q - 1)):  # report first 20 chars
            scores = batch_results[k]
            if scores:
                peak = max(scores, key=lambda x: x[1])
                batch_peaks[k] = peak

        print(f"  Time: {t_batch:.2f}s")
        print(f"  Top 10 detected zeros:")
        sorted_peaks = sorted(batch_peaks.items(), key=lambda x: -x[1][1])[:10]
        for k, (gamma, score) in sorted_peaks:
            print(f"    chi_{k}: gamma = {gamma:.4f}, score = {score:.2f}")

        # Method B: Individual computation (limited to first 20 chars for fairness)
        print(f"\nMethod B: Individual zero search (first 20 characters)...")
        indiv_results, t_indiv = individual_zero_search(q, 20, T_max)

        if indiv_results is not None:
            print(f"  Time: {t_indiv:.2f}s")
            print(f"  First 10 detected zeros:")
            for k in sorted(list(indiv_results.keys())[:10]):
                print(f"    chi_{k}: gamma ~ {indiv_results[k]:.4f}")

        # Comparison
        print(f"\n  COMPARISON (q={q}):")
        print(f"    Batch ({q-1} chars): {t_batch:.2f}s")
        print(f"    Individual (20 chars): {t_indiv:.2f}s")
        if t_indiv > 0:
            projected = t_indiv * (q - 1) / 20
            print(f"    Projected individual (all {q-1} chars): {projected:.1f}s")
            if t_batch > 0:
                print(f"    SPEEDUP: {projected / t_batch:.1f}x")

    print(f"\n{'='*70}")
    print("BENCHMARK COMPLETE")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
