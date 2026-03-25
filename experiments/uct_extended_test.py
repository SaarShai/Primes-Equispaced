#!/usr/bin/env python3
"""
Universal Compression Thesis — Extended Test Suite
====================================================

THESIS: Compression of exponential sums occurs if and only if the
underlying set is definable via Mobius inversion.

We test 14 new sequence families (A through N) across multiple N values,
measuring:
  - |E(m, N)| = |sum_{s in S} exp(2*pi*i*m*s/N)| for several m
  - compression ratio = |E| / |S|
  - compression exponent alpha where ratio ~ N^{-alpha}

A positive alpha means compression; alpha ~ 0 means none.
"""

import numpy as np
from math import gcd, pi, sqrt, log, isqrt
from collections import defaultdict
import sys
import time

# =====================================================================
# UTILITIES
# =====================================================================

def mobius_sieve(limit):
    """Compute mu(n) for all n <= limit."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime = [True] * (limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu, primes

def prime_sieve(limit):
    """Simple sieve of Eratosthenes. Returns boolean array."""
    is_prime = [False, False] + [True] * (limit - 1)
    for i in range(2, isqrt(limit) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return is_prime

def omega_sieve(limit):
    """Compute omega(n) = number of distinct prime factors for n <= limit."""
    omega = [0] * (limit + 1)
    for p in range(2, limit + 1):
        if omega[p] == 0:  # p is prime
            for k in range(p, limit + 1, p):
                omega[k] += 1
    return omega

def bigomega_sieve(limit):
    """Compute Omega(n) = number of prime factors with multiplicity."""
    Omega = [0] * (limit + 1)
    for p in range(2, limit + 1):
        if Omega[p] == 0:  # p is prime
            pk = p
            while pk <= limit:
                for k in range(pk, limit + 1, pk):
                    Omega[k] += 1
                pk *= p
    return Omega

def sigma_sieve(limit):
    """Compute sigma(n) = sum of divisors for n <= limit."""
    sigma = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for k in range(d, limit + 1, d):
            sigma[k] += d
    return sigma

def totient_sieve(limit):
    """Compute Euler's totient phi(n) for n <= limit."""
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:  # p is prime
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

# =====================================================================
# EXPONENTIAL SUM COMPUTATION
# =====================================================================

def exp_sum(elements, N, m=1):
    """Compute sum_{s in elements} exp(2*pi*i*m*s/N)."""
    if len(elements) == 0:
        return 0.0
    arr = np.array(elements, dtype=np.float64)
    phases = 2.0 * np.pi * m * arr / N
    return abs(np.sum(np.exp(1j * phases)))

def measure_compression(name, set_generator, N_values, m_values=[1, 2, 3, 5, 7]):
    """
    Measure compression for a sequence family across multiple N.
    set_generator(N) should return a list of elements in [1, N].
    Returns dict with results.
    """
    results = {
        'name': name,
        'N_values': [],
        'set_sizes': [],
        'E_values': [],       # average |E| over m values
        'ratios': [],         # average |E|/|S| over m values
        'E_by_m': {},         # |E| for each m
    }
    for m in m_values:
        results['E_by_m'][m] = []

    for N in N_values:
        elements = set_generator(N)
        S = len(elements)
        if S == 0:
            continue

        results['N_values'].append(N)
        results['set_sizes'].append(S)

        E_vals = []
        for m in m_values:
            E = exp_sum(elements, N, m)
            results['E_by_m'][m].append(E)
            E_vals.append(E)

        avg_E = np.mean(E_vals)
        results['E_values'].append(avg_E)
        results['ratios'].append(avg_E / S)

    return results

def fit_exponent(N_values, values):
    """Fit values ~ C * N^beta, return beta."""
    if len(N_values) < 2 or min(values) <= 0:
        return 0.0
    log_N = np.log(np.array(N_values, dtype=np.float64))
    log_V = np.log(np.array(values, dtype=np.float64))
    # Linear regression in log space
    A = np.vstack([log_N, np.ones(len(log_N))]).T
    result = np.linalg.lstsq(A, log_V, rcond=None)
    beta = result[0][0]
    return beta

# =====================================================================
# SEQUENCE GENERATORS (A through N)
# =====================================================================

# Precompute sieves at max N
MAX_N = 50000

print("Precomputing sieves up to", MAX_N, "...")
t0 = time.time()
MU, PRIMES = mobius_sieve(MAX_N)
IS_PRIME = prime_sieve(MAX_N)
OMEGA = omega_sieve(MAX_N)
BIGOMEGA = bigomega_sieve(MAX_N)
SIGMA = sigma_sieve(MAX_N)
PHI = totient_sieve(MAX_N)
PRIME_SET = set(p for p in range(2, MAX_N + 1) if IS_PRIME[p])
print(f"  Sieves done in {time.time() - t0:.1f}s")


# A. ARITHMETIC PROGRESSIONS: {n <= N : n = a mod q}
def arith_prog(a, q):
    def gen(N):
        return [n for n in range(a, N + 1, q)]
    return gen

# B. PRIMES
def primes_set(N):
    return [p for p in range(2, N + 1) if IS_PRIME[p]]

# C. TWIN PRIME CANDIDATES: {n <= N : gcd(n(n+2), P#) = 1}
def twin_prime_candidates(N):
    """Numbers n where both n and n+2 are coprime to the primorial P#
    (we use P = product of primes up to some bound)."""
    # Use primorial of 30 (= 2*3*5*7*11*13*17*19*23*29)
    small_primes = [2, 3, 5, 7, 11, 13]
    results = []
    for n in range(1, N + 1):
        ok = True
        for p in small_primes:
            if n % p == 0 or (n + 2) % p == 0:
                ok = False
                break
        if ok:
            results.append(n)
    return results

# D. NUMBERS WITH EXACTLY k PRIME FACTORS
def exact_omega_k(k):
    """omega(n) = k (distinct prime factors)."""
    def gen(N):
        return [n for n in range(2, N + 1) if OMEGA[n] == k]
    return gen

def exact_bigomega_k(k):
    """Omega(n) = k (prime factors with multiplicity)."""
    def gen(N):
        return [n for n in range(2, N + 1) if BIGOMEGA[n] == k]
    return gen

# E. PERFECT POWERS
def perfect_powers(N):
    """n = m^k for some m >= 2, k >= 2."""
    result = set()
    for k in range(2, int(log(N) / log(2)) + 2):
        m = 2
        while m ** k <= N:
            result.add(m ** k)
            m += 1
    return sorted(result)

# F. FIBONACCI NUMBERS in [1, N]
def fibonacci_numbers(N):
    fibs = []
    a, b = 1, 1
    while a <= N:
        fibs.append(a)
        a, b = b, a + b
    return fibs

# G. PALINDROMES in base 10
def palindromes_base10(N):
    return [n for n in range(1, N + 1) if str(n) == str(n)[::-1]]

# H. HIGHLY COMPOSITE NUMBERS (approximation: numbers with many divisors)
def highly_composite_approx(N):
    """Numbers whose divisor count exceeds all smaller numbers."""
    # Compute divisor counts
    d_count = [0] * (N + 1)
    for k in range(1, N + 1):
        for j in range(k, N + 1, k):
            d_count[j] += 1
    result = []
    max_d = 0
    for n in range(1, N + 1):
        if d_count[n] > max_d:
            max_d = d_count[n]
            result.append(n)
    return result

# I. PRACTICAL NUMBERS
def is_practical(n, sigma_arr):
    """Check if n is a practical number:
    every integer m with 1 <= m <= sigma(n) can be represented
    as a sum of distinct divisors of n.
    Simplified check using Stewart's theorem:
    n is practical iff n=1 or for each prime factor p of n,
    p <= 1 + sigma(n / p^a) where p^a || n."""
    if n == 1:
        return True
    if n % 2 != 0 and n > 1:
        return False
    # Factor n
    temp = n
    factors = []  # list of (p, a)
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            a = 0
            while temp % d == 0:
                a += 1
                temp //= d
            factors.append((d, a))
        d += 1
    if temp > 1:
        factors.append((temp, 1))
    factors.sort()

    # Stewart's criterion
    product = 1
    for p, a in factors:
        if p > 1 + sigma_of(product, sigma_arr):
            return False
        product *= p ** a
    return True

def sigma_of(n, sigma_arr):
    """Sum of divisors of n."""
    if n <= len(sigma_arr) - 1:
        return sigma_arr[n]
    # Fallback
    s = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            s += d
            if d != n // d:
                s += n // d
    return s

def practical_numbers(N):
    return [n for n in range(1, N + 1) if is_practical(n, SIGMA)]

# J. NILPOTENT NUMBERS: n where Z_n is nilpotent (iff n is cubefree and
# for each prime p | n, p does not divide phi(n/p^a) where p^a || n).
# Simpler characterization: n is a product of prime powers p^a where
# p^a are pairwise coprime and each p^a is a prime power (always true).
# Actually: Z_n is nilpotent iff n is squarefree... No.
# Z_n is nilpotent iff every Sylow subgroup is normal, which for Z_n
# (abelian) is ALWAYS true. So ALL positive integers are nilpotent numbers
# in this sense. The term "nilpotent number" sometimes means n such that
# every group of order n is nilpotent. This happens iff n = p1^a1 * ... * pk^ak
# with pi != pj and pi does not divide pj^aj - 1 for all i,j.
def nilpotent_numbers(N):
    """n such that every group of order n is nilpotent.
    Criterion: n is cubefree, and for primes p|n, q|n with p<q,
    q is not congruent to 1 mod p. (Pakianathan-Shankar)
    Simplified: just check all prime pairs."""
    result = []
    for n in range(1, N + 1):
        # Factor n
        temp = n
        pf = []
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                a = 0
                while temp % d == 0:
                    a += 1
                    temp //= d
                pf.append((d, a))
            d += 1
        if temp > 1:
            pf.append((temp, 1))

        # Check: for all primes p < q dividing n, q^(a_q) not cong 1 mod p
        is_nilp = True
        primes_of_n = [p for p, a in pf]
        for i, p in enumerate(primes_of_n):
            for j in range(i + 1, len(primes_of_n)):
                q = primes_of_n[j]
                # Check: q^a_q mod p != 1 and p^a_p mod q != 1
                # More precisely: p does not divide q^a - 1 for the exponent a of q
                a_q = [a for (pp, a) in pf if pp == q][0]
                if (pow(q, a_q, p) - 1) % p == 0 and p > 1:
                    # p divides q^a_q - 1, not nilpotent
                    # But need more careful check: p | (q^b - 1) for some b | a_q
                    is_nilp = False
                    break
            if not is_nilp:
                break
        if is_nilp:
            result.append(n)
    return result

# K. TOTIENT VALUES: {n : phi(m) = n for some m}
def totient_values(N):
    """Numbers that appear as phi(m) for some m."""
    vals = set()
    # phi(m) <= m, so we need m up to some bound.
    # phi(m) = n can have m up to ~2n for even n.
    bound = min(2 * N + 100, MAX_N)
    for m in range(1, bound + 1):
        v = PHI[m]
        if v <= N:
            vals.add(v)
    return sorted(vals)

# L. SUM OF TWO SQUARES: {n <= N : n = a^2 + b^2}
def sum_of_two_squares(N):
    """n representable as a^2 + b^2.
    Characterization: n = a^2 + b^2 iff in the prime factorization of n,
    every prime p = 3 mod 4 occurs to an even power."""
    result = []
    for n in range(1, N + 1):
        temp = n
        ok = True
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                a = 0
                while temp % d == 0:
                    a += 1
                    temp //= d
                if d % 4 == 3 and a % 2 == 1:
                    ok = False
                    break
            d += 1
        if ok and temp > 1 and temp % 4 == 3:
            ok = False
        if ok:
            result.append(n)
    return result

# M. NUMBERS COPRIME TO n! (small n)
def coprime_to_factorial(n):
    """Numbers in [1, N] coprime to n!.
    Equivalent to: numbers whose smallest prime factor > n."""
    small_primes = [p for p in range(2, n + 1) if IS_PRIME[p]]
    def gen(N):
        result = []
        for k in range(1, N + 1):
            ok = True
            for p in small_primes:
                if k % p == 0:
                    ok = False
                    break
            if ok:
                result.append(k)
        return result
    return gen

# N. SQUAREFULL NUMBERS: all prime factors appear >= 2 times
def squarefull_numbers(N):
    """n such that if p | n then p^2 | n."""
    result = []
    for n in range(1, N + 1):
        if n == 1:
            result.append(1)
            continue
        temp = n
        ok = True
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                a = 0
                while temp % d == 0:
                    a += 1
                    temp //= d
                if a < 2:
                    ok = False
                    break
            d += 1
        if temp > 1:  # leftover prime factor with exponent 1
            ok = False
        if ok:
            result.append(n)
    return result

# =====================================================================
# MAIN EXPERIMENT
# =====================================================================

def run_all_tests():
    N_values = [500, 1000, 2000, 5000, 10000, 20000, 50000]
    # For slow generators, use smaller N
    N_small = [500, 1000, 2000, 5000, 10000]
    N_tiny = [500, 1000, 2000, 5000]

    families = []

    print("\n" + "=" * 70)
    print("UNIVERSAL COMPRESSION THESIS — EXTENDED TEST")
    print("=" * 70)

    # A. Arithmetic progressions (a=1 mod 3, a=1 mod 6, a=1 mod 30)
    print("\n[A] Arithmetic progressions...")
    for q, a in [(3, 1), (6, 1), (30, 1)]:
        r = measure_compression(f"AP a={a} mod {q}", arith_prog(a, q), N_values)
        families.append(r)

    # B. Primes
    print("[B] Primes...")
    r = measure_compression("Primes", primes_set, N_values)
    families.append(r)

    # C. Twin prime candidates
    print("[C] Twin prime candidates...")
    r = measure_compression("Twin prime candidates", twin_prime_candidates, N_values)
    families.append(r)

    # D. Exactly k prime factors
    print("[D] Exactly k distinct prime factors...")
    for k in [1, 2, 3]:
        r = measure_compression(f"omega(n)={k}", exact_omega_k(k), N_values)
        families.append(r)
    print("[D'] Exactly k prime factors with multiplicity...")
    for k in [1, 2, 3]:
        r = measure_compression(f"Omega(n)={k}", exact_bigomega_k(k), N_values)
        families.append(r)

    # E. Perfect powers
    print("[E] Perfect powers...")
    r = measure_compression("Perfect powers", perfect_powers, N_values)
    families.append(r)

    # F. Fibonacci numbers
    print("[F] Fibonacci numbers...")
    r = measure_compression("Fibonacci numbers", fibonacci_numbers, N_values)
    families.append(r)

    # G. Palindromes
    print("[G] Base-10 palindromes...")
    r = measure_compression("Palindromes (base 10)", palindromes_base10, N_values)
    families.append(r)

    # H. Highly composite numbers
    print("[H] Highly composite numbers...")
    r = measure_compression("Highly composite", highly_composite_approx, N_small)
    families.append(r)

    # I. Practical numbers
    print("[I] Practical numbers...")
    r = measure_compression("Practical numbers", practical_numbers, N_small)
    families.append(r)

    # J. Nilpotent numbers
    print("[J] Nilpotent numbers...")
    r = measure_compression("Nilpotent numbers", nilpotent_numbers, N_tiny)
    families.append(r)

    # K. Totient values
    print("[K] Totient values...")
    r = measure_compression("Totient values", totient_values, N_small)
    families.append(r)

    # L. Sum of two squares
    print("[L] Sum of two squares...")
    r = measure_compression("Sum of two squares", sum_of_two_squares, N_small)
    families.append(r)

    # M. Coprime to n!
    print("[M] Coprime to n!...")
    for n in [3, 5, 7]:
        r = measure_compression(f"Coprime to {n}!", coprime_to_factorial(n), N_values)
        families.append(r)

    # N. Squarefull numbers
    print("[N] Squarefull numbers...")
    r = measure_compression("Squarefull numbers", squarefull_numbers, N_values)
    families.append(r)

    # =====================================================================
    # ANALYSIS: FIT EXPONENTS
    # =====================================================================

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"\n{'Family':<30} {'|S| ~ N^':<12} {'|E| ~ N^':<12} "
          f"{'Ratio ~ N^':<12} {'Verdict':<15}")
    print("-" * 81)

    all_results = []

    for r in families:
        if len(r['N_values']) < 2:
            continue
        N_arr = r['N_values']
        S_arr = r['set_sizes']
        E_arr = r['E_values']
        R_arr = r['ratios']

        beta_S = fit_exponent(N_arr, S_arr) if min(S_arr) > 0 else 0
        beta_E = fit_exponent(N_arr, E_arr) if min(E_arr) > 1e-10 else -99
        alpha = beta_S - beta_E  # compression exponent = S growth - E growth

        # Also fit ratio directly
        beta_R = fit_exponent(N_arr, R_arr) if min(R_arr) > 1e-10 else -99

        if alpha > 0.5:
            verdict = "STRONG"
        elif alpha > 0.15:
            verdict = "MODERATE"
        elif alpha > 0.05:
            verdict = "WEAK"
        else:
            verdict = "NONE"

        print(f"{r['name']:<30} {beta_S:>+8.2f}     {beta_E:>+8.2f}     "
              f"{beta_R:>+8.2f}     {verdict}")

        all_results.append({
            'name': r['name'],
            'beta_S': beta_S,
            'beta_E': beta_E,
            'beta_R': beta_R,
            'alpha': alpha,
            'verdict': verdict,
            'N_values': N_arr,
            'set_sizes': S_arr,
            'E_values': E_arr,
            'ratios': R_arr,
        })

    # =====================================================================
    # DETAILED OUTPUT
    # =====================================================================

    print("\n" + "=" * 70)
    print("DETAILED DATA")
    print("=" * 70)

    for r in families:
        if len(r['N_values']) < 2:
            continue
        print(f"\n--- {r['name']} ---")
        print(f"  {'N':>8}  {'|S|':>8}  {'|E| (m=1)':>12}  {'ratio':>10}")
        for i, N in enumerate(r['N_values']):
            E1 = r['E_by_m'].get(1, [None]*len(r['N_values']))[i]
            if E1 is not None:
                print(f"  {N:>8}  {r['set_sizes'][i]:>8}  {E1:>12.2f}  "
                      f"{E1/r['set_sizes'][i]:>10.4f}")

    # =====================================================================
    # THESIS EVALUATION
    # =====================================================================

    print("\n" + "=" * 70)
    print("UNIVERSAL COMPRESSION THESIS EVALUATION")
    print("=" * 70)

    # Categorize
    mobius_definable = {
        "AP a=1 mod 3", "AP a=1 mod 6", "AP a=1 mod 30",
        "Primes",
        "Twin prime candidates",
        "Coprime to 3!", "Coprime to 5!", "Coprime to 7!",
        # omega/Omega = k are NOT directly Mobius-definable
    }

    not_mobius = {
        "Perfect powers", "Fibonacci numbers", "Palindromes (base 10)",
        "Highly composite", "Squarefull numbers",
    }

    multiplicative_char = {
        "Sum of two squares",  # multiplicative characterization via chi_4
    }

    ambiguous = {
        "omega(n)=1", "omega(n)=2", "omega(n)=3",
        "Omega(n)=1", "Omega(n)=2", "Omega(n)=3",
        "Practical numbers", "Nilpotent numbers", "Totient values",
    }

    print("\n--- Expected to COMPRESS (Mobius-definable) ---")
    for res in all_results:
        if res['name'] in mobius_definable:
            status = "OK" if res['alpha'] > 0.1 else "FAIL"
            print(f"  [{status}] {res['name']:<30} alpha={res['alpha']:>+.2f}  {res['verdict']}")

    print("\n--- Expected NOT to compress ---")
    for res in all_results:
        if res['name'] in not_mobius:
            status = "OK" if res['alpha'] < 0.1 else "FAIL"
            print(f"  [{status}] {res['name']:<30} alpha={res['alpha']:>+.2f}  {res['verdict']}")

    print("\n--- Multiplicative characterization (interesting test) ---")
    for res in all_results:
        if res['name'] in multiplicative_char:
            print(f"  [??] {res['name']:<30} alpha={res['alpha']:>+.2f}  {res['verdict']}")

    print("\n--- Ambiguous / unclear Mobius status ---")
    for res in all_results:
        if res['name'] in ambiguous:
            print(f"  [??] {res['name']:<30} alpha={res['alpha']:>+.2f}  {res['verdict']}")

    # Count hits/misses
    hits = 0
    misses = 0
    for res in all_results:
        if res['name'] in mobius_definable:
            if res['alpha'] > 0.1:
                hits += 1
            else:
                misses += 1
        elif res['name'] in not_mobius:
            if res['alpha'] < 0.1:
                hits += 1
            else:
                misses += 1

    total = hits + misses
    print(f"\n--- THESIS SCORECARD ---")
    print(f"  Correct predictions: {hits}/{total}")
    print(f"  Accuracy: {100*hits/total:.0f}%" if total > 0 else "  N/A")

    return all_results


if __name__ == "__main__":
    results = run_all_tests()
