#!/usr/bin/env python3
"""
Koyama_C1.py — mpmath verifier for the C_1 subleading-term identity.

Statement (Saar's 2026-04-15 email, verbatim):

    c_K(rho, chi) = log(K)/L'(rho, chi) + C_1(rho, chi) + o(1)

with

    C_1(rho, chi) = -L''(rho, chi) / (2 L'(rho, chi)^2).

This script:
  1. For each of Saar's 4 (chi, rho) pairs:
       (a) refines rho via Newton iteration on L(s, chi),
       (b) computes L'(rho), L''(rho), and C_1,
       (c) computes c_K = sum_{n<=K} mu(n) chi(n) n^{-rho} for K in {2e5, 1e6, 2e6},
       (d) reports residual = c_K - log(K)/L'(rho) - C_1.
  2. Confirms residual scales like O(log(K)/sqrt(K)) (the Soundararajan-style RH tail).

Precision: mpmath at 50 dps.
"""

import time
from mpmath import (
    mp, mpc, mpf, zeta, log as mlog, exp as mexp,
    nstr, diff, findroot, pi, sqrt
)

mp.dps = 50  # ≥ 50 decimal digits of precision

# -----------------------------------------------------------------------------
# Dirichlet L-function via Hurwitz zeta:  L(s, chi) = q^{-s} sum chi(a) zeta(s, a/q)
# -----------------------------------------------------------------------------

def make_L(chi_vals, q):
    """chi_vals: length-q list of chi(0), chi(1), ..., chi(q-1)."""
    def L(s):
        return mpc(q) ** (-s) * sum(
            chi_vals[a] * zeta(s, mpf(a) / q) for a in range(q) if chi_vals[a] != 0
        )
    return L


# -----------------------------------------------------------------------------
# Define Saar's 4 characters
# -----------------------------------------------------------------------------

# chi_{-4}: real, order 2, mod 4: chi(p)=1 if p=1(4), -1 if p=3(4)
chi_m4_vals = [0, 1, 0, -1]

# chi_5: complex, order 4, mod 5: d = {1:0, 2:1, 4:2, 3:3}, chi(n) = i^{d(n)}
chi_5_vals = [mpc(0), mpc(1), mpc(0, 1), mpc(0, -1), mpc(-1)]

# chi_{11}: complex, order 10, mod 11
d11 = {1: 0, 2: 1, 4: 2, 8: 3, 5: 4, 10: 5, 9: 6, 7: 7, 3: 8, 6: 9}


def make_chi11():
    arr = [mpc(0)] * 11
    for n, dn in d11.items():
        arr[n] = mexp(2 * pi * mpc(0, 1) * dn / 10)
    return arr


chi_11_vals = make_chi11()

# Per-character mod for chi(n) lookup
CHARACTER_TABLE = {
    "chi_-4/z1": (chi_m4_vals, 4),
    "chi_-4/z2": (chi_m4_vals, 4),
    "chi_5":     (chi_5_vals, 5),
    "chi_11":    (chi_11_vals, 11),
}

PAIRS = [
    ("chi_-4/z1", make_L(chi_m4_vals, 4),  mpc('0.5', '6.020948904697')),
    ("chi_-4/z2", make_L(chi_m4_vals, 4),  mpc('0.5', '10.2437')),
    ("chi_5",     make_L(chi_5_vals,  5),  mpc('0.5', '6.184')),
    ("chi_11",    make_L(chi_11_vals, 11), mpc('0.5', '3.547')),
]


# -----------------------------------------------------------------------------
# Linear Möbius sieve
# -----------------------------------------------------------------------------

def linear_sieve_mu(K):
    mu = [0] * (K + 1)
    mu[1] = 1
    primes = []
    smallest = [0] * (K + 1)
    for n in range(2, K + 1):
        if smallest[n] == 0:
            smallest[n] = n
            primes.append(n)
            mu[n] = -1
        for p in primes:
            if p > smallest[n] or p * n > K:
                break
            smallest[p * n] = p
            if n % p == 0:
                mu[p * n] = 0
                break
            else:
                mu[p * n] = -mu[n]
    return mu


# -----------------------------------------------------------------------------
# c_K computation:   sum_{n<=K} mu(n) chi(n) n^{-rho}
# -----------------------------------------------------------------------------

def compute_c_K(K, mu, chi_lookup, rho):
    """chi_lookup(n) returns chi(n) as an mpc value; mu is precomputed list."""
    # Iterate, skipping mu(n)*chi(n) == 0
    acc = mpc(0)
    # precompute log(n) on the fly via mpf(n).log() is expensive; mlog is fine
    for n in range(1, K + 1):
        m = mu[n]
        if m == 0:
            continue
        c = chi_lookup(n)
        if c == 0:
            continue
        # n^{-rho} = exp(-rho * ln(n))
        term = mexp(-rho * mlog(n))
        acc += m * c * term
    return acc


# -----------------------------------------------------------------------------
# Main verification
# -----------------------------------------------------------------------------

def main():
    print(f"mpmath dps = {mp.dps}")
    print("=" * 80)

    # Step 1: refine rho, compute L', L'', C_1 for each pair
    derived = {}
    for name, L, rho_guess in PAIRS:
        print(f"\n=== {name} ===")
        rho = findroot(L, rho_guess, tol=mpf('1e-40'))
        Lp  = diff(L, rho)
        Lpp = diff(L, rho, 2)
        C1  = -Lpp / (2 * Lp ** 2)
        derived[name] = dict(rho=rho, Lp=Lp, Lpp=Lpp, C1=C1)
        print(f"  rho       = {nstr(rho,  20)}")
        print(f"  L(rho)    = {nstr(L(rho), 6)}   (numerical zero check)")
        print(f"  L'(rho)   = {nstr(Lp,  12)}   |L'|  = {nstr(abs(Lp),  10)}")
        print(f"  L''(rho)  = {nstr(Lpp, 12)}")
        print(f"  C_1       = {nstr(C1,  12)}   |C_1| = {nstr(abs(C1), 8)}")

    # Step 2: build sieve once, compute c_K at multiple K's
    K_max = 2_000_000
    print(f"\nBuilding Möbius sieve to K = {K_max} ...")
    t0 = time.time()
    mu = linear_sieve_mu(K_max)
    print(f"  done in {time.time()-t0:.2f}s")

    K_grid = [200_000, 1_000_000, 2_000_000]

    print("\n" + "=" * 80)
    print(f"{'pair':<14} {'K':>10}  {'|c_K - log(K)/L'' - C1|':>26}  "
          f"{'predicted O(log K/√K)':>22}")
    print("=" * 80)

    for name, L, _ in PAIRS:
        d = derived[name]
        rho = d['rho']
        Lp = d['Lp']
        C1 = d['C1']

        chi_vals, q = CHARACTER_TABLE[name]
        def chi_lookup(n, _cv=chi_vals, _q=q):
            return _cv[n % _q]

        # Compute c_K for each K. Reuse partial sums where possible: build
        # cumulative sum incrementally up through K_max.
        cum = {}
        acc = mpc(0)
        K_set = set(K_grid)
        for n in range(1, K_max + 1):
            m = mu[n]
            if m != 0:
                c = chi_lookup(n)
                if c != 0:
                    acc += m * c * mexp(-rho * mlog(n))
            if n in K_set:
                cum[n] = acc

        for K in K_grid:
            cK = cum[K]
            logK = mlog(K)
            predicted_main = logK / Lp
            residual = cK - predicted_main - C1
            # Predicted scale: log(K) / sqrt(K)
            scale = logK / sqrt(K)
            print(f"{name:<14} {K:>10}  {nstr(abs(residual), 6):>26}  "
                  f"{nstr(scale, 6):>22}")

        print()

    # Step 3: spell out the leading-asymptotic ratio
    print("=" * 80)
    print("Leading-order check:  c_K · L'(rho) / log K  →  1  (rate O(1/log K))")
    print("=" * 80)

    for name, L, _ in PAIRS:
        d = derived[name]
        rho, Lp = d['rho'], d['Lp']
        chi_vals, q = CHARACTER_TABLE[name]
        # Reuse final cumulative; recompute briefly at K = 2e6
        # (we lose the cum dict above; recompute final)
        acc = mpc(0)
        for n in range(1, K_max + 1):
            m = mu[n]
            if m != 0:
                c = chi_vals[n % q]
                if c != 0:
                    acc += m * c * mexp(-rho * mlog(n))
        ratio = acc * Lp / mlog(K_max)
        print(f"{name:<14}  c_K * L'/log K = {nstr(ratio, 8)}   "
              f"|ratio - 1| = {nstr(abs(ratio - 1), 6)}")


if __name__ == "__main__":
    main()
