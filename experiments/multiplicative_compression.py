#!/usr/bin/env python3
"""
Multiplicative Compression Beyond Farey Sequences
===================================================

THE PRINCIPLE (from Farey sequences):
  The exponential sum over ~3N^2/pi^2 Farey fractions collapses to M(N)+1
  (a single integer!) because:
    1. Ramanujan sums c_b(m) = mu(b) compress each denominator to +/-1/0
    2. Multiplicativity of mu makes contributions independent
    3. Summation aggregates to M(N) = sum_{k=1}^N mu(k)

QUESTION: Do other sequences with multiplicative structure exhibit
similar compression? We test 6 families of sequences.

For each sequence S_N of size |S_N|, we compute:
  E(m, N) = sum_{s in S_N} exp(2*pi*i*m*s / PERIOD)
and check whether |E(m,N)| collapses to something much smaller than |S_N|,
ideally to a known number-theoretic function.

COMPRESSION RATIO = |E(m,N)| / |S_N|
  If this -> 0, there is compression.
  If this stays O(1), there is none.
"""

import numpy as np
from math import gcd, pi, sqrt, log
import cmath
from collections import defaultdict
import sys

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

def mertens(mu, N):
    """M(N) = sum_{k=1}^N mu(k)."""
    return sum(mu[1:N+1])

def euler_totient_sieve(limit):
    """Compute phi(n) for all n <= limit."""
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:  # p is prime
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def farey_sequence(N):
    """Generate Farey sequence F_N as list of (a, b) with gcd(a,b)=1, 0<=a<=b<=N."""
    fracs = []
    a, b, c, d = 0, 1, 1, N
    fracs.append((a, b))
    while c <= N:
        fracs.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
    return fracs

def is_primitive_root(g, p, prime_factors_of_p_minus_1):
    """Check if g is a primitive root mod p."""
    for q in prime_factors_of_p_minus_1:
        if pow(g, (p - 1) // q, p) == 1:
            return False
    return True

def prime_factors(n):
    """Return set of prime factors of n."""
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors

# =====================================================================
# A. FAREY BASELINE — Verify the known compression
# =====================================================================

def test_farey_compression(N_values, m=1):
    """
    Baseline: Farey exponential sum should give M(N) + 1.
    E(m=1, N) = sum_{a/b in F_N} exp(2*pi*i*a/b) = M(N) + 1
    """
    print("=" * 70)
    print("A. FAREY SEQUENCE BASELINE (m=1)")
    print("=" * 70)

    max_N = max(N_values)
    mu, _ = mobius_sieve(max_N)

    results = []
    for N in N_values:
        farey = farey_sequence(N)
        farey_size = len(farey)

        # Exponential sum
        E = sum(cmath.exp(2j * pi * a / b) for a, b in farey)
        M_N = mertens(mu, N)

        predicted = M_N + 1
        error = abs(E - predicted)
        compression = abs(E) / farey_size

        results.append({
            'N': N, 'size': farey_size, 'E_real': E.real, 'E_imag': E.imag,
            'M_N': M_N, 'predicted': predicted, 'error': error,
            'compression': compression
        })

        print(f"  N={N:4d}: |F_N|={farey_size:6d}, E={E.real:+10.6f}+{E.imag:+.6f}i, "
              f"M(N)+1={predicted:+4d}, err={error:.2e}, compress={compression:.6f}")

    return results


# =====================================================================
# B. SQUARE-FREE NUMBERS
# =====================================================================

def test_squarefree_compression(N_values, m_values=[1, 2, 3, 5, 7]):
    """
    Square-free numbers: {n <= N : mu(n)^2 = 1}
    Count ~ 6N/pi^2

    Exponential sum: S(m, N) = sum_{n sqfree, n<=N} exp(2*pi*i*m*n/N)

    THEORY: The indicator function of square-free numbers is mu^2(n) = sum_{d^2|n} mu(d).
    So S(m,N) = sum_{n<=N} mu^2(n) * exp(2*pi*i*m*n/N)
              = sum_{d<=sqrt(N)} mu(d) * sum_{k<=N/d^2} exp(2*pi*i*m*d^2*k/N)

    The inner sum is a geometric series that may telescope.
    """
    print("\n" + "=" * 70)
    print("B. SQUARE-FREE NUMBERS")
    print("=" * 70)

    max_N = max(N_values)
    mu, _ = mobius_sieve(max_N)

    results = []
    for N in N_values:
        sqfree = [n for n in range(1, N + 1) if mu[n] != 0]
        size = len(sqfree)
        expected_size = 6 * N / pi**2

        print(f"\n  N={N}: |sqfree|={size} (expected ~{expected_size:.1f})")

        for m in m_values:
            # Direct exponential sum
            E = sum(cmath.exp(2j * pi * m * n / N) for n in sqfree)
            compression = abs(E) / size if size > 0 else 0

            # Theoretical prediction via Mobius decomposition
            # S(m,N) = sum_{d<=sqrt(N)} mu(d) * sum_{k<=N/d^2} exp(2*pi*i*m*d^2*k/N)
            E_theory = complex(0)
            for d in range(1, int(sqrt(N)) + 1):
                if mu[d] == 0:
                    continue
                inner = sum(cmath.exp(2j * pi * m * d * d * k / N)
                            for k in range(1, N // (d * d) + 1))
                E_theory += mu[d] * inner

            theory_error = abs(E - E_theory)

            # Check if |E| is close to an integer or known function
            E_rounded = round(E.real)
            near_int = abs(E.real - E_rounded) < 0.01 and abs(E.imag) < 0.01

            results.append({
                'N': N, 'm': m, 'size': size, 'E_abs': abs(E),
                'E_real': E.real, 'E_imag': E.imag,
                'compression': compression, 'near_integer': near_int,
                'theory_match': theory_error < 0.01
            })

            marker = " *** INTEGER!" if near_int else ""
            print(f"    m={m}: E={E.real:+12.4f}+{E.imag:+10.4f}i, "
                  f"|E|={abs(E):10.4f}, compress={compression:.4f}, "
                  f"theory_err={theory_error:.2e}{marker}")

    return results


# =====================================================================
# C. PRIMITIVE ROOTS mod p
# =====================================================================

def test_primitive_root_compression(primes_to_test):
    """
    For prime p, primitive roots mod p form a subset of size phi(p-1).

    Exponential sum: E(m, p) = sum_{g primitive root mod p} exp(2*pi*i*m*g/p)

    These are related to Ramanujan sums over the group (Z/pZ)*.
    The number of primitive roots = phi(p-1).

    THEORETICAL CONNECTION: If chi ranges over characters of order d|(p-1),
    the sum over primitive roots involves Ramanujan sums over the index group.
    """
    print("\n" + "=" * 70)
    print("C. PRIMITIVE ROOTS mod p")
    print("=" * 70)

    results = []
    for p in primes_to_test:
        pf = prime_factors(p - 1)

        # Find all primitive roots
        prim_roots = []
        for g in range(1, p):
            if is_primitive_root(g, p, pf):
                prim_roots.append(g)

        size = len(prim_roots)
        phi_pm1 = size  # Should equal phi(p-1)

        print(f"\n  p={p}: phi(p-1)={phi_pm1}, p-1={p-1}, factors={pf}")

        for m in [1, 2, 3]:
            E = sum(cmath.exp(2j * pi * m * g / p) for g in prim_roots)
            compression = abs(E) / size if size > 0 else 0

            # Known result: sum of primitive roots mod p = mu(p-1)
            # More precisely, sum_{g prim root} e^{2pi i g/p} = mu(p-1) (Ramanujan-type)
            # This is because the primitive roots generate characters of maximal order
            mu_pm1_sieve, _ = mobius_sieve(p)
            mu_pm1 = mu_pm1_sieve[p - 1]

            near_mu = abs(E.real - mu_pm1) < 0.5 and abs(E.imag) < 0.5

            # For m > 1, the sum is related to Ramanujan sums
            results.append({
                'p': p, 'm': m, 'size': size, 'E_abs': abs(E),
                'E_real': E.real, 'E_imag': E.imag,
                'compression': compression, 'mu_p_minus_1': mu_pm1,
                'matches_mu': near_mu
            })

            match_str = f" = mu({p-1})={mu_pm1} !!!" if near_mu else ""
            print(f"    m={m}: E={E.real:+12.6f}+{E.imag:+10.6f}i, "
                  f"|E|={abs(E):10.4f}, compress={compression:.6f}{match_str}")

    return results


# =====================================================================
# D. SMOOTH NUMBERS (B-smooth: all prime factors <= B)
# =====================================================================

def test_smooth_compression(N_values, B_values=[5, 10, 20]):
    """
    B-smooth numbers up to N: {n <= N : largest prime factor of n <= B}

    Count given by Dickman's function: Psi(N, B) ~ N * rho(log N / log B)

    These have multiplicative structure: a B-smooth number is a product
    of primes <= B. But they lack the Mobius inversion that makes Farey work.
    """
    print("\n" + "=" * 70)
    print("D. SMOOTH NUMBERS")
    print("=" * 70)

    max_N = max(N_values)

    # Sieve for largest prime factor
    lpf = [0] * (max_N + 1)  # largest prime factor
    lpf[1] = 1
    for i in range(2, max_N + 1):
        if lpf[i] == 0:  # i is prime
            for j in range(i, max_N + 1, i):
                lpf[j] = i

    results = []
    for N in N_values:
        for B in B_values:
            if B >= N:
                continue

            smooth = [n for n in range(1, N + 1) if lpf[n] <= B]
            size = len(smooth)

            if size < 2:
                continue

            print(f"\n  N={N}, B={B}: |smooth|={size}")

            for m in [1, 2, 3]:
                E = sum(cmath.exp(2j * pi * m * n / N) for n in smooth)
                compression = abs(E) / size if size > 0 else 0

                near_int = abs(E.real - round(E.real)) < 0.1 and abs(E.imag) < 0.1

                results.append({
                    'N': N, 'B': B, 'm': m, 'size': size, 'E_abs': abs(E),
                    'E_real': E.real, 'compression': compression,
                    'near_integer': near_int
                })

                marker = f" *** ~{round(E.real)}" if near_int else ""
                print(f"    m={m}: E={E.real:+12.4f}+{E.imag:+10.4f}i, "
                      f"|E|={abs(E):10.4f}, compress={compression:.4f}{marker}")

    return results


# =====================================================================
# E. MULTIPLICATIVE WEIGHTED FAREY SUMS
# =====================================================================

def test_weighted_farey(N_values, m=1):
    """
    For completely multiplicative f, define:
      S_f(N) = sum_{a/b in F_N} f(b) * exp(2*pi*i*a/b)

    For m=1, the Ramanujan sum identity gives:
      S_f(N) = 1 + sum_{b=2}^N (f*mu)(b)

    where (f*mu)(b) = sum_{d|b} f(d)*mu(b/d) is the Dirichlet convolution.

    For completely multiplicative f: (f*mu)(n) = f(n) * mu(n) * ... no,
    actually f*mu = product over primes of (f(p) - f(p)^2 + ...)

    We test specific multiplicative f:
    1. f(n) = n^s (Dirichlet series weight)
    2. f(n) = chi(n) (Dirichlet character)
    3. f(n) = lambda(n) (Liouville function)
    """
    print("\n" + "=" * 70)
    print("E. MULTIPLICATIVE WEIGHTED FAREY SUMS")
    print("=" * 70)

    max_N = max(N_values)
    mu, primes = mobius_sieve(max_N)

    # Compute Liouville function: lambda(n) = (-1)^Omega(n)
    liouville = [0] * (max_N + 1)
    liouville[1] = 1
    omega = [0] * (max_N + 1)  # number of prime factors with multiplicity
    for p in primes:
        if p > max_N:
            break
        pk = p
        while pk <= max_N:
            for j in range(pk, max_N + 1, pk):
                omega[j] += 1
            pk *= p
    for n in range(1, max_N + 1):
        liouville[n] = (-1) ** omega[n]

    results = []

    for N in N_values:
        farey = farey_sequence(N)
        farey_size = len(farey)

        print(f"\n  N={N}: |F_N|={farey_size}")

        # --- Weight 1: f(n) = 1 (baseline, should give M(N)+1) ---
        E_1 = sum(cmath.exp(2j * pi * a / b) for a, b in farey)
        M_N = mertens(mu, N)
        print(f"    f=1:       E={E_1.real:+12.6f}, M(N)+1={M_N+1}")

        # --- Weight 2: f(b) = liouville(b) ---
        E_liou = sum(liouville[b] * cmath.exp(2j * pi * a / b) for a, b in farey)

        # Theoretical: sum should be 1 + sum_{b=2}^N (liouville * mu)(b)
        # For Liouville: (lambda * mu)(n) = |mu(n)| * lambda(n) ...
        # Actually lambda * mu = mu_2 (the indicator of squarefree numbers... no)
        # lambda(n) = product_{p|n} (-1)^{v_p(n)}
        # (lambda * mu)(p) = lambda(p)*mu(1) + lambda(1)*mu(p) = -1 + (-1) = -2
        # (lambda * mu)(p^2) = lambda(p^2)*mu(1) + lambda(p)*mu(p) + lambda(1)*mu(p^2)
        #                    = 1 + 1 + 0 = 2
        # So this is a complicated convolution.

        # Direct computation of 1 + sum (lambda * mu)(b)
        lam_mu_sum = 0
        for b in range(2, N + 1):
            conv = sum(liouville[d] * mu[b // d]
                      for d in range(1, b + 1) if b % d == 0)
            lam_mu_sum += conv
        E_liou_theory = 1 + lam_mu_sum

        liou_error = abs(E_liou - E_liou_theory)
        liou_compress = abs(E_liou) / farey_size

        # Does sum_{b=1}^N (lambda*mu)(b) have a nice closed form?
        # It should be related to sum_{b sqfree, b<=N} lambda(b) = sum_{b sqfree} (-1)^{omega(b)}
        L_N = sum(liouville[k] for k in range(1, N + 1))  # Summatory Liouville

        print(f"    f=lambda:  E={E_liou.real:+12.6f}+{E_liou.imag:+.6f}i, "
              f"theory={E_liou_theory:+12.6f}, err={liou_error:.2e}, "
              f"compress={liou_compress:.6f}, L(N)={L_N}")

        results.append({
            'N': N, 'weight': 'liouville', 'E_real': E_liou.real,
            'theory': E_liou_theory, 'error': liou_error,
            'compression': liou_compress, 'L_N': L_N
        })

        # --- Weight 3: f(b) = b^{-1/2} (fractional Dirichlet weight) ---
        E_sqrt = sum(b ** (-0.5) * cmath.exp(2j * pi * a / b) for a, b in farey)

        # Theory: 1 + sum_{b=2}^N (b^{-1/2} . mu)(b) via Dirichlet convolution
        # (n^{-s} * mu)(n) = product_p (1 - p^{-s}) over p|n for squarefree n
        sqrt_mu_sum = 0
        for b in range(2, N + 1):
            conv = sum((d ** (-0.5)) * mu[b // d]
                      for d in range(1, b + 1) if b % d == 0)
            sqrt_mu_sum += conv
        E_sqrt_theory = 1 + sqrt_mu_sum
        sqrt_error = abs(E_sqrt - E_sqrt_theory)
        sqrt_compress = abs(E_sqrt) / (farey_size ** 0.5)  # normalize differently

        print(f"    f=b^-1/2: E={E_sqrt.real:+12.6f}+{E_sqrt.imag:+.6f}i, "
              f"theory={E_sqrt_theory:+12.6f}, err={sqrt_error:.2e}")

        results.append({
            'N': N, 'weight': 'sqrt', 'E_real': E_sqrt.real,
            'theory': E_sqrt_theory, 'error': sqrt_error
        })

        # --- Weight 4: f(b) = mu(b) itself (double Mobius) ---
        E_mu = sum(mu[b] * cmath.exp(2j * pi * a / b) for a, b in farey)

        # Theory: 1 + sum_{b=2}^N (mu * mu)(b) = 1 + sum |mu(b)|
        # Wait: (mu * mu)(n) = sum_{d|n} mu(d) mu(n/d) = [n=1]? No.
        # Actually sum_{d|n} mu(d) mu(n/d) = (mu*mu)(n)
        # This is the Mobius function of the Mobius function.
        # It's related to: (mu*mu)(n) = |mu(n)| if n squarefree, 0 otherwise? No.
        # (mu*mu)(p) = mu(1)mu(p) + mu(p)mu(1) = -1-1 = -2
        # (mu*mu)(p^2) = mu(1)mu(p^2) + mu(p)mu(p) + mu(p^2)mu(1) = 0+1+0 = 1

        mu_mu_sum = 0
        for b in range(2, N + 1):
            conv = sum(mu[d] * mu[b // d]
                      for d in range(1, b + 1) if b % d == 0)
            mu_mu_sum += conv
        E_mu_theory = 1 + mu_mu_sum
        mu_error = abs(E_mu - E_mu_theory)
        mu_compress = abs(E_mu) / farey_size

        # Q(N) = sum_{n=1}^N |mu(n)| = count of squarefree numbers
        Q_N = sum(1 for k in range(1, N + 1) if mu[k] != 0)

        print(f"    f=mu:      E={E_mu.real:+12.6f}+{E_mu.imag:+.6f}i, "
              f"theory={E_mu_theory:+12.6f}, err={mu_error:.2e}, "
              f"compress={mu_compress:.6f}, Q(N)={Q_N}")

        results.append({
            'N': N, 'weight': 'mu', 'E_real': E_mu.real,
            'theory': E_mu_theory, 'error': mu_error,
            'compression': mu_compress, 'Q_N': Q_N
        })

    return results


# =====================================================================
# F. GAUSSIAN INTEGER "FAREY" SEQUENCE
# =====================================================================

def test_gaussian_farey(N_values):
    """
    Gaussian Farey sequence: fractions a/b where a, b are Gaussian integers
    with |b| <= N, gcd(a, b) = 1 (Gaussian gcd), 0 <= Re(a/b), Im(a/b) < 1.

    Instead of a full 2D Farey, we use a simpler variant:
    Gaussian rationals with denominator norm <= N^2.

    The Gaussian analogue of mu is mu_K(a) for Gaussian integers,
    which is multiplicative over Gaussian primes.
    """
    print("\n" + "=" * 70)
    print("F. GAUSSIAN INTEGER FAREY ANALOGUE")
    print("=" * 70)

    def gaussian_gcd(a, b):
        """GCD of two Gaussian integers (as complex numbers with integer parts)."""
        while b != 0:
            q = complex(round((a / b).real), round((a / b).imag))
            r = a - q * b
            a, b = b, r
        return a

    results = []
    for N in N_values:
        # Generate Gaussian integers b with 1 <= |b|^2 <= N^2
        # For each b, find coprime a with 0 <= Re(a/b), Im(a/b) < 1
        # This is actually the "fundamental domain" approach

        # Simpler: use b = x + iy with x^2 + y^2 <= N^2, x > 0 or (x=0, y>0)
        # For each such b, the "Farey fractions" are a/b with
        # a in {c+di : 0 <= c < x, 0 <= d < y} and gcd_gauss(a,b) = unit

        # For computational feasibility, enumerate b with small norm
        gauss_fracs = []

        for bx in range(-N, N + 1):
            for by in range(-N, N + 1):
                norm_b = bx * bx + by * by
                if norm_b == 0 or norm_b > N * N:
                    continue
                b = complex(bx, by)

                # Only use b in first quadrant (up to units)
                if bx <= 0 or by < 0:
                    continue

                # Enumerate a with 0 <= Re(a/b) < 1, 0 <= Im(a/b) < 1
                for ax in range(0, int(sqrt(norm_b)) + 2):
                    for ay in range(0, int(sqrt(norm_b)) + 2):
                        a = complex(ax, ay)
                        ratio = a / b
                        if 0 <= ratio.real < 1 and 0 <= ratio.imag < 1:
                            # Check coprimality
                            g = gaussian_gcd(a, b)
                            gnorm = g.real**2 + g.imag**2
                            if abs(gnorm - 1) < 0.01:  # gcd is a unit
                                gauss_fracs.append((a, b))

        size = len(gauss_fracs)
        print(f"\n  N={N}: |Gauss Farey|={size}")

        if size < 2:
            continue

        # Exponential sum: sum exp(2*pi*i * Re(a/b))
        # (Using just the real part projection)
        E_real_proj = sum(cmath.exp(2j * pi * (a / b).real) for a, b in gauss_fracs)
        compress_real = abs(E_real_proj) / size

        # Full 2D exponential sum: sum exp(2*pi*i * (Re(a/b) + Im(a/b)))
        E_full = sum(cmath.exp(2j * pi * ((a/b).real + (a/b).imag)) for a, b in gauss_fracs)
        compress_full = abs(E_full) / size

        # Gaussian Mertens: M_K(N) = sum_{|a|^2 <= N^2} mu_K(a)
        # where mu_K is the Mobius function for Gaussian integers
        # For now just record what we get

        near_int_real = abs(E_real_proj.real - round(E_real_proj.real)) < 0.5
        near_int_full = abs(E_full.real - round(E_full.real)) < 0.5

        results.append({
            'N': N, 'size': size,
            'E_real_proj': abs(E_real_proj), 'compress_real': compress_real,
            'E_full': abs(E_full), 'compress_full': compress_full
        })

        print(f"    Real proj: E={E_real_proj.real:+10.4f}+{E_real_proj.imag:+.4f}i, "
              f"|E|={abs(E_real_proj):.4f}, compress={compress_real:.4f}")
        print(f"    Full 2D:   E={E_full.real:+10.4f}+{E_full.imag:+.4f}i, "
              f"|E|={abs(E_full):.4f}, compress={compress_full:.4f}")

    return results


# =====================================================================
# G. BEATTY SEQUENCES
# =====================================================================

def test_beatty_compression(N_values, alphas=None):
    """
    Beatty sequence: B_alpha = {floor(n*alpha) : n = 1, ..., N}

    For irrational alpha, these are equidistributed mod 1 by Weyl's theorem.
    The exponential sum sum_{n=1}^N exp(2*pi*i*m*floor(n*alpha)/P) should
    show cancellation related to the continued fraction expansion of alpha.

    KEY QUESTION: Does the "discrepancy" of the Beatty sequence connect
    to a Mertens-like function when alpha has multiplicative structure
    in its continued fraction?
    """
    print("\n" + "=" * 70)
    print("G. BEATTY SEQUENCES")
    print("=" * 70)

    if alphas is None:
        alphas = {
            'golden': (1 + sqrt(5)) / 2,
            'sqrt2': sqrt(2),
            'sqrt3': sqrt(3),
            'e': 2.718281828459045,
            'pi': 3.141592653589793,
            'sqrt5': sqrt(5),
        }

    results = []
    for name, alpha in alphas.items():
        print(f"\n  alpha = {name} = {alpha:.8f}")

        for N in N_values:
            beatty = [int(n * alpha) for n in range(1, N + 1)]
            # Remove duplicates and sort
            beatty_set = sorted(set(beatty))
            size = len(beatty_set)

            # Use period P = max value + 1
            P = max(beatty_set) + 1

            for m in [1]:
                E = sum(cmath.exp(2j * pi * m * s / P) for s in beatty_set)
                compression = abs(E) / size if size > 0 else 0

                near_int = abs(E.real - round(E.real)) < 0.5 and abs(E.imag) < 0.5

                results.append({
                    'alpha': name, 'N': N, 'size': size,
                    'E_abs': abs(E), 'E_real': E.real,
                    'compression': compression, 'near_integer': near_int
                })

                marker = f" ~{round(E.real)}" if near_int else ""
                print(f"    N={N:4d}: size={size:4d}, "
                      f"E={E.real:+10.4f}+{E.imag:+.4f}i, "
                      f"|E|={abs(E):8.4f}, compress={compression:.4f}{marker}")

    return results


# =====================================================================
# H. VISIBLE LATTICE POINTS (Euler product structure)
# =====================================================================

def test_visible_lattice_compression(N_values):
    """
    Visible lattice points: {(a, b) : 1 <= a, b <= N, gcd(a, b) = 1}
    Count ~ 6N^2/pi^2

    Exponential sum: sum_{gcd(a,b)=1} exp(2*pi*i*(a+b)/(2N))

    This has direct multiplicative structure through Mobius inversion:
    sum_{gcd(a,b)=1} f(a,b) = sum_{d=1}^N mu(d) sum_{a,b} f(da, db)
    """
    print("\n" + "=" * 70)
    print("H. VISIBLE LATTICE POINTS")
    print("=" * 70)

    max_N = max(N_values)
    mu, _ = mobius_sieve(max_N)

    results = []
    for N in N_values:
        # Direct computation (expensive for large N)
        E_direct = complex(0)
        count = 0
        for a in range(1, N + 1):
            for b in range(1, N + 1):
                if gcd(a, b) == 1:
                    E_direct += cmath.exp(2j * pi * (a + b) / (2 * N))
                    count += 1

        # Mobius inversion formula
        E_mobius = complex(0)
        for d in range(1, N + 1):
            if mu[d] == 0:
                continue
            # sum_{a=1}^{N/d} sum_{b=1}^{N/d} exp(2*pi*i*d*(a+b)/(2N))
            Nd = N // d
            s1 = sum(cmath.exp(2j * pi * d * a / (2 * N)) for a in range(1, Nd + 1))
            # s1 * s1 because the sum factors
            E_mobius += mu[d] * s1 * s1

        mobius_error = abs(E_direct - E_mobius)
        compression = abs(E_direct) / count if count > 0 else 0

        near_int = abs(E_direct.real - round(E_direct.real)) < 0.5

        results.append({
            'N': N, 'count': count, 'E_abs': abs(E_direct),
            'compression': compression, 'near_integer': near_int,
            'mobius_error': mobius_error
        })

        M_N = mertens(mu, N)
        print(f"  N={N:3d}: visible={count:6d}, "
              f"E={E_direct.real:+12.4f}+{E_direct.imag:+10.4f}i, "
              f"|E|={abs(E_direct):10.4f}, compress={compression:.4f}, "
              f"mobius_err={mobius_error:.2e}, M(N)={M_N}")

    return results


# =====================================================================
# I. TOTIENT-WEIGHTED SUM (deep test of multiplicative compression)
# =====================================================================

def test_totient_compression(N_values):
    """
    The Farey sequence has |F_N| = 1 + sum_{k=1}^N phi(k) fractions.

    Test: sum_{b=1}^N phi(b) * (sum_{a: gcd(a,b)=1, 1<=a<b} exp(2*pi*i*a/b)) / phi(b)

    The inner sum over a coprime to b is a Ramanujan sum c_b(1) = mu(b).
    So: sum_{b=1}^N mu(b) = M(N). This IS the Farey identity in disguise.

    NEW TEST: What if we weight by phi(b)^s for various s?
    sum_{b=1}^N phi(b)^s * c_b(m)
    = sum_{b=1}^N phi(b)^s * mu(b)  [when m and b are coprime]

    This is a Dirichlet series evaluation. Does it have nice values?
    """
    print("\n" + "=" * 70)
    print("I. TOTIENT-WEIGHTED RAMANUJAN SUMS")
    print("=" * 70)

    max_N = max(N_values)
    mu, _ = mobius_sieve(max_N)
    phi = euler_totient_sieve(max_N)

    results = []
    for N in N_values:
        print(f"\n  N={N}:")

        M_N = mertens(mu, N)
        print(f"    M(N) = sum mu(b) = {M_N}")

        for s in [0.5, 1, 1.5, 2, -0.5, -1]:
            weighted = sum(phi[b] ** s * mu[b] for b in range(1, N + 1))

            # Normalization: compare to sum phi(b)^s
            total_weight = sum(phi[b] ** s for b in range(1, N + 1))
            norm_ratio = weighted / total_weight if total_weight != 0 else 0

            # Check for nice closed forms
            near_int = abs(weighted - round(weighted)) < 0.5

            results.append({
                'N': N, 's': s, 'weighted_sum': weighted,
                'total_weight': total_weight, 'ratio': norm_ratio,
                'near_integer': near_int
            })

            marker = f" ~{round(weighted)}" if near_int else ""
            print(f"    s={s:+5.1f}: sum phi^s * mu = {weighted:+14.4f}, "
                  f"total phi^s = {total_weight:14.4f}, "
                  f"ratio = {norm_ratio:+.6f}{marker}")

    return results


# =====================================================================
# J. DIRECT COMPRESSION TEST: various multiplicative functions
# =====================================================================

def test_direct_exponential_sums(N_values):
    """
    For a set S defined by a multiplicative condition, compute
    E_S(m, N) = sum_{n in S, n <= N} exp(2*pi*i*m*n/N)
    and check the compression ratio |E_S| / |S|.

    Sets tested:
    1. Squarefree (mu^2 = 1)
    2. Powerful numbers (p^2 | n for all p | n)
    3. Numbers with odd number of prime factors (Liouville = -1)
    4. Numbers where mu(n) = +1
    5. Numbers where mu(n) = -1
    """
    print("\n" + "=" * 70)
    print("J. DIRECT EXPONENTIAL SUMS OVER MULTIPLICATIVE SETS")
    print("=" * 70)

    max_N = max(N_values)
    mu, primes = mobius_sieve(max_N)

    # Classify numbers
    omega = [0] * (max_N + 1)
    for p in primes:
        if p > max_N:
            break
        pk = p
        while pk <= max_N:
            for j in range(pk, max_N + 1, pk):
                omega[j] += 1
            pk *= p

    results = []
    for N in N_values:
        sets = {
            'squarefree': [n for n in range(1, N+1) if mu[n] != 0],
            'mu_plus': [n for n in range(1, N+1) if mu[n] == 1],
            'mu_minus': [n for n in range(1, N+1) if mu[n] == -1],
            'powerful': [n for n in range(1, N+1) if all(
                n % (p*p) == 0 for p in prime_factors(n) if n > 1) and n > 1],
            'odd_omega': [n for n in range(1, N+1) if omega[n] % 2 == 1],
            'even_omega': [n for n in range(1, N+1) if omega[n] % 2 == 0 and n > 0],
        }

        print(f"\n  N={N}:")
        for set_name, S in sets.items():
            size = len(S)
            if size < 2:
                continue

            # Exponential sum with m=1
            E = sum(cmath.exp(2j * pi * n / N) for n in S)
            compression = abs(E) / size

            M_N = mertens(mu, N)
            near_M = abs(E.real - M_N) < 1.0
            near_int = abs(E.real - round(E.real)) < 0.5 and abs(E.imag) < 0.5

            marker = ""
            if near_int:
                marker = f" ~{round(E.real)}"

            results.append({
                'N': N, 'set': set_name, 'size': size,
                'E_abs': abs(E), 'E_real': E.real, 'E_imag': E.imag,
                'compression': compression, 'near_integer': near_int
            })

            print(f"    {set_name:12s}: |S|={size:5d}, "
                  f"E={E.real:+10.4f}+{E.imag:+.4f}i, "
                  f"|E|={abs(E):8.4f}, compress={compression:.4f}{marker}")

    return results


# =====================================================================
# K. SCALING ANALYSIS: How compression ratio scales with N
# =====================================================================

def scaling_analysis():
    """
    For each sequence type, compute compression ratio at many N values
    to determine the scaling law.

    If compression ratio ~ N^{-alpha}, that's genuine compression.
    If it stays O(1), no compression.
    """
    print("\n" + "=" * 70)
    print("K. SCALING ANALYSIS: Compression ratio vs N")
    print("=" * 70)

    N_range = [10, 20, 30, 50, 75, 100, 150, 200, 300, 400, 500]
    max_N = max(N_range)
    mu, primes = mobius_sieve(max_N)

    # Track compression ratios
    data = {
        'farey': [], 'squarefree': [], 'mu_plus': [],
        'primitive_roots': [], 'smooth_5': [], 'beatty_golden': []
    }

    phi_val = (1 + sqrt(5)) / 2

    for N in N_range:
        # Farey
        farey = farey_sequence(N)
        E_f = sum(cmath.exp(2j * pi * a / b) for a, b in farey)
        data['farey'].append((N, abs(E_f) / len(farey)))

        # Squarefree
        sqfree = [n for n in range(1, N+1) if mu[n] != 0]
        if len(sqfree) > 1:
            E_sq = sum(cmath.exp(2j * pi * n / N) for n in sqfree)
            data['squarefree'].append((N, abs(E_sq) / len(sqfree)))

        # mu = +1
        mu_plus = [n for n in range(1, N+1) if mu[n] == 1]
        if len(mu_plus) > 1:
            E_mp = sum(cmath.exp(2j * pi * n / N) for n in mu_plus)
            data['mu_plus'].append((N, abs(E_mp) / len(mu_plus)))

        # Beatty golden ratio
        beatty = sorted(set(int(n * phi_val) for n in range(1, N + 1)))
        if len(beatty) > 1:
            P = max(beatty) + 1
            E_b = sum(cmath.exp(2j * pi * s / P) for s in beatty)
            data['beatty_golden'].append((N, abs(E_b) / len(beatty)))

    # Primitive roots (only for primes)
    test_primes = [p for p in primes if 10 <= p <= 500]
    for p in test_primes:
        pf = prime_factors(p - 1)
        roots = [g for g in range(1, p) if is_primitive_root(g, p, pf)]
        if len(roots) > 1:
            E_pr = sum(cmath.exp(2j * pi * g / p) for g in roots)
            data['primitive_roots'].append((p, abs(E_pr) / len(roots)))

    # Print scaling results
    from math import log as ln
    for name, vals in data.items():
        if len(vals) < 3:
            continue

        Ns = [v[0] for v in vals]
        ratios = [v[1] for v in vals]

        # Fit log(ratio) = alpha * log(N) + const
        log_N = [ln(n) for n in Ns]
        log_r = [ln(max(r, 1e-15)) for r in ratios]

        if len(log_N) >= 2:
            # Simple linear regression
            n_pts = len(log_N)
            mx = sum(log_N) / n_pts
            my = sum(log_r) / n_pts
            sxx = sum((x - mx)**2 for x in log_N)
            sxy = sum((x - mx) * (y - my) for x, y in zip(log_N, log_r))
            alpha = sxy / sxx if sxx > 0 else 0

            print(f"\n  {name:20s}: ratio ~ N^({alpha:+.3f})")
            print(f"    N values: {Ns[:5]}...")
            print(f"    ratios:   {[f'{r:.4f}' for r in ratios[:5]]}...")

            if alpha < -0.3:
                print(f"    >>> COMPRESSION DETECTED: ratio decreases as N^({alpha:.2f})")
            elif alpha < -0.05:
                print(f"    >>> WEAK compression: ratio slowly decreases")
            else:
                print(f"    >>> NO compression: ratio does not decrease with N")

    return data


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("MULTIPLICATIVE COMPRESSION: BEYOND FAREY SEQUENCES")
    print("=" * 70)
    print()

    # Parameters
    small_N = [10, 20, 50, 100, 200]
    medium_N = [50, 100, 200, 500]
    large_N = [100, 200, 500]

    all_results = {}

    # A. Farey baseline
    all_results['farey'] = test_farey_compression(small_N + [300, 500])

    # B. Square-free numbers
    all_results['squarefree'] = test_squarefree_compression(medium_N)

    # C. Primitive roots
    # Use primes where p-1 has varied factorizations
    test_primes = [5, 7, 11, 13, 23, 29, 37, 41, 53, 59, 67, 71, 83, 97,
                   101, 127, 131, 151, 167, 173, 191, 197, 199, 211, 251]
    all_results['primitive_roots'] = test_primitive_root_compression(test_primes)

    # D. Smooth numbers
    all_results['smooth'] = test_smooth_compression(medium_N)

    # E. Weighted Farey sums
    all_results['weighted_farey'] = test_weighted_farey([20, 50, 100, 200])

    # F. Gaussian Farey (small due to computational cost)
    all_results['gaussian'] = test_gaussian_farey([3, 5, 7, 10])

    # G. Beatty sequences
    all_results['beatty'] = test_beatty_compression([50, 100, 200, 500])

    # H. Visible lattice points (small due to O(N^2) cost)
    all_results['visible'] = test_visible_lattice_compression([10, 20, 30, 50])

    # I. Totient-weighted sums
    all_results['totient'] = test_totient_compression([50, 100, 200, 500])

    # J. Direct exponential sums over multiplicative sets
    all_results['direct'] = test_direct_exponential_sums([100, 200, 500])

    # K. Scaling analysis
    print("\n\n" + "#" * 70)
    print("SCALING ANALYSIS — THE KEY TEST")
    print("#" * 70)
    all_results['scaling'] = scaling_analysis()

    # =====================================================================
    # SUMMARY
    # =====================================================================
    print("\n\n" + "=" * 70)
    print("SUMMARY OF FINDINGS")
    print("=" * 70)

    print("""
    COMPRESSION means: |exponential sum| / |set size| -> 0 as N -> infinity.

    The Farey sequence achieves compression ratio ~ N^{-1} because:
      |E| = |M(N) + 1| ~ O(N^{1/2+eps}) while |F_N| ~ 3N^2/pi^2

    For each tested sequence, the key question is:
    Does the compression ratio DECREASE with N?
    """)
