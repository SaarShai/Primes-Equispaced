#!/usr/bin/env python3
"""
SPECTRAL EXTENSION TO s=1/2 — VERSION 2: Refined analysis
===========================================================

Key observations from v1:
1. The ratio K_alpha * n * p / sum|L(alpha/2)|^2 is NOT constant but DECREASING in p.
   This means we need a different normalization.

2. For alpha=2 (standard L2), ratio ~ 1/pi^2 * something. The decrease suggests
   we're missing a factor of log(p) or similar.

3. The CV test (Part 5) shows that s=1 gives the LOWEST CV (most constant ratio),
   meaning the standard formula is best at s=1. Moving to s=1/2 makes things worse.

NEW APPROACH: Instead of sum chi(b) disc^2 / |L(s,chi)|^2, try:
   sum chi(b) |disc|^{2s} / |L(s,chi)|^2

or better: use the EXACT Ramanujan sum decomposition identity and see how
it analytically extends.

Also: test whether the Nyman-Beurling kernel rho(x) = {1/x} gives a natural
bridge to s=1/2.
"""

import numpy as np
from math import gcd, isqrt, pi, sqrt, log, exp
import time

start = time.time()

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

def primitive_root(p):
    if p == 2:
        return 1
    phi_p = p - 1
    factors = set()
    n = phi_p
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
            if pow(g, phi_p // f, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None

def dirichlet_characters(p):
    g = primitive_root(p)
    dlog = [0] * p
    val = 1
    for k in range(p - 1):
        dlog[val] = k
        val = (val * g) % p
    chars = []
    for j in range(p - 1):
        omega = np.exp(2j * pi * j / (p - 1))
        chi = np.zeros(p, dtype=complex)
        for a in range(1, p):
            chi[a] = omega ** dlog[a]
        chars.append(chi)
    return chars

def L_function_fast(s, chi_vals, p, num_terms=30000):
    ns = np.arange(1, num_terms + 1, dtype=np.float64)
    residues = ns.astype(int) % p
    chi_n = chi_vals[residues]
    return np.sum(chi_n / ns**s)

def farey_generator(N):
    a, b = 0, 1
    c, d = 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b


# ============================================================
# KEY ANALYTICAL INSIGHT: The Ramanujan sum identity
# ============================================================
#
# The universal formula gives:
#   S(m, N) = sum_{f in F_N} e(m*f) = sum_{d|m, d<=N} d * M(N/d)  + [boundary]
#
# The L2 discrepancy is:
#   W(N) = sum_j (f_j - j/n)^2 = (1/n^2) sum_{m=1}^{inf} |S(m,N)|^2 / (2pi m)^2
#
# More precisely, by Parseval:
#   sum (f_j - j/n)^2 = (1/n^2) * sum_{m != 0} |S(m,N)|^2 / (2pi m)^2
#
# Now |S(m,N)|^2 = |sum_{d|m} d * M(N/d)|^2
#
# If we replace 1/(2pi m)^2 with 1/(2pi m)^alpha, we get:
#   K_alpha(N) = (1/n^2) * sum_{m=1}^{inf} |S(m,N)|^2 / (2pi m)^alpha
#
# The question is: what does this relate to at the critical line?
#
# KEY: The Ramanujan-sum representation of S(m,N) involves the SAME
# arithmetic that produces L-function values. Specifically:
#
#   sum_{m=1}^{inf} |S(m,N)|^2 / m^{2s}
#     = sum_{d1, d2 <= N} d1 d2 M(N/d1) M(N/d2) * sum_{lcm(d1,d2)|m} 1/m^{2s}
#     = sum_{d1, d2} d1 d2 M(N/d1) M(N/d2) / lcm(d1,d2)^{2s} * zeta(2s)
#
# At s = 1/2: zeta(1) DIVERGES! This is why the alpha=1 kernel discrepancy
# grows relative to sum |L(1/2)|^2 — the zeta(1) pole contaminates.
#
# FIX: Use the REGULARIZED kernel
#   K_reg(N) = sum_{m=1}^{inf} |S(m,N) - delta_{m,0}*n|^2 / m^{2s}
#
# Or use partial zeta functions that avoid the pole.


def main():
    print("=" * 78)
    print("SPECTRAL EXTENSION v2: REFINED ANALYSIS")
    print("=" * 78)

    LIMIT = 200
    phi_arr = euler_totient_sieve(LIMIT)
    mu, M = mobius_sieve(LIMIT)
    primes = sieve_primes(LIMIT)
    test_primes = [p for p in primes if 5 <= p <= 97]

    # -------------------------------------------------------
    # TEST A: Exact Ramanujan sum identity verification
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("TEST A: Verify S(m,N) = sum_{d|m, d<=N} d * M(N/d)")
    print("=" * 78)

    for N in [10, 20, 50]:
        fracs = [a/b for a, b in farey_generator(N)]
        n = len(fracs)
        fracs_arr = np.array(fracs)

        print(f"\n  N={N}, n={n}:")
        for m in [1, 2, 3, 4, 5, 6]:
            # Direct computation
            Sm_direct = np.sum(np.exp(2j * pi * m * fracs_arr))
            # Ramanujan sum formula
            Sm_formula = 0
            for d in range(1, N + 1):
                if m % d == 0:
                    Sm_formula += d * M[N // d]
            # Add the "1" for the 0/1 term (it contributes e(0) = 1 always,
            # but M captures sum mu(k) which already accounts for 0/1... check)
            print(f"    m={m}: direct={Sm_direct.real:+.6f}{Sm_direct.imag:+.6f}j, "
                  f"formula={Sm_formula:+d}, diff={abs(Sm_direct - Sm_formula):.2e}")

    # -------------------------------------------------------
    # TEST B: The Dirichlet series sum |S(m)|^2 / m^{2s}
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("TEST B: D(s,N) = sum_{m=1}^H |S(m,N)|^2 / m^{2s}")
    print("Compare to sum_{d1,d2} ... at different s values")
    print("=" * 78)

    for N in [10, 20, 50]:
        fracs_arr = np.array([a/b for a, b in farey_generator(N)])
        n = len(fracs_arr)

        print(f"\n  N={N}, n={n}:")
        H = 200

        for s_val in [1.0, 0.75, 0.6, 0.51]:
            D_s = 0.0
            for m in range(1, H + 1):
                Sm = np.sum(np.exp(2j * pi * m * fracs_arr))
                D_s += abs(Sm)**2 / m**(2 * s_val)

            # Compare to the formula
            D_formula = 0.0
            for d1 in range(1, N + 1):
                for d2 in range(1, N + 1):
                    l = d1 * d2 // gcd(d1, d2)  # lcm
                    if l <= H:
                        coeff = d1 * d2 * M[N // d1] * M[N // d2]
                        # sum_{m: lcm|m, m<=H} 1/m^{2s}
                        partial = sum(1.0 / (l * k)**(2 * s_val)
                                      for k in range(1, H // l + 1))
                        D_formula += coeff * partial

            print(f"    s={s_val:.2f}: D_direct={D_s:.4f}, D_formula={D_formula:.4f}, "
                  f"ratio={D_s/D_formula:.6f}" if D_formula != 0 else
                  f"    s={s_val:.2f}: D_direct={D_s:.4f}, D_formula=0")

    # -------------------------------------------------------
    # TEST C: The KEY observation — subtract the m=0 mode
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("TEST C: Centered kernel discrepancy (subtract mean)")
    print("K_alpha_centered = sum_{m>=1} |S(m) - delta_m0 * n|^2 / m^alpha")
    print("= sum_{m>=1} |S(m)|^2 / m^alpha   (since m>=1 already excludes m=0)")
    print("The zeta(2s) pole at s=1/2 comes from m-independent terms.")
    print("After subtraction, does the L(1/2) relationship emerge?")
    print("=" * 78)

    # Actually, S(m) for m >= 1 already has the mean subtracted.
    # The issue is that sum |S(m)|^2 / m still diverges like log(H).
    # We need to REGULARIZE.

    # Approach: Use the completed L-function Lambda(s,chi) = (q/pi)^{s/2} Gamma((s+a)/2) L(s,chi)
    # which satisfies the functional equation Lambda(s,chi) = epsilon(chi) Lambda(1-s, chi_bar).
    # At s=1/2: Lambda(1/2, chi) relates to the central value.

    # Instead, let's try: for each CHARACTER, compute the per-character
    # kernel discrepancy directly.

    print("\n  Per-character kernel discrepancy:")
    print("  For chi mod p: K(chi, alpha) = sum_m chi(m) * |S(m)|^2 / m^alpha")
    print("  This should diagonalize to something involving L(alpha/2, chi).")

    for p in [7, 11, 13, 17, 23]:
        N = p - 1
        fracs_arr = np.array([a/b for a, b in farey_generator(N)])
        n = len(fracs_arr)
        chars = dirichlet_characters(p)
        H = 300

        # Precompute |S(m)|^2 for m = 1..H
        S_m = np.zeros(H + 1, dtype=complex)
        for m in range(1, H + 1):
            S_m[m] = np.sum(np.exp(2j * pi * m * fracs_arr))
        S_sq = np.abs(S_m)**2

        print(f"\n  p={p}, N={N}, n={n}:")
        print(f"    {'chi_j':>5s}  {'K(chi,2)':>12s}  {'K(chi,1)':>12s}  "
              f"{'|L(1)|^2':>10s}  {'|L(.5)|^2':>10s}  "
              f"{'K2/L1^2':>10s}  {'K1/L05^2':>10s}")
        print("    " + "-" * 75)

        for j in range(1, min(p - 1, 8)):
            chi = chars[j]
            K_chi_2 = 0.0
            K_chi_1 = 0.0
            for m in range(1, H + 1):
                chi_m = chi[m % p]
                K_chi_2 += (chi_m * S_sq[m] / m**2).real
                K_chi_1 += (chi_m * S_sq[m] / m**1).real

            L1 = L_function_fast(1.0, chi, p)
            Lhalf = L_function_fast(0.5, chi, p)
            L1_sq = abs(L1)**2
            Lhalf_sq = abs(Lhalf)**2

            r2 = K_chi_2 / L1_sq if L1_sq > 1e-15 else 0
            r1 = K_chi_1 / Lhalf_sq if Lhalf_sq > 1e-15 else 0

            print(f"    {j:5d}  {K_chi_2:12.6f}  {K_chi_1:12.6f}  "
                  f"{L1_sq:10.6f}  {Lhalf_sq:10.6f}  "
                  f"{r2:10.4f}  {r1:10.4f}")

    # -------------------------------------------------------
    # TEST D: The CORRECT approach — Gauss sum weighted Farey sum
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("TEST D: Gauss-sum weighted Farey exponential sum")
    print("T(s, chi) = sum_{a/b in F_N} chi(b) / b^s * e(m * a/b)")
    print("This is a twisted version where the b^{-s} weight directly")
    print("connects to L(s, chi) via the Euler product.")
    print("=" * 78)

    for p in [7, 11, 13, 17, 23, 29, 31]:
        N = p - 1
        fracs_list = []
        denoms_list = []
        for a, b in farey_generator(N):
            fracs_list.append(a / b)
            denoms_list.append(b)
        fracs_arr = np.array(fracs_list)
        denoms_arr = np.array(denoms_list, dtype=np.float64)
        n = len(fracs_arr)
        chars = dirichlet_characters(p)

        print(f"\n  p={p}, N={N}:")

        for s_val in [1.0, 0.5]:
            # Compute T(s, chi, m=1) = sum_{a/b} chi(b)/b^s * e(a/b)
            print(f"    s={s_val:.1f}:")
            print(f"      {'j':>3s}  {'|T(s,chi,m=1)|^2':>18s}  "
                  f"{'|L(s,chi)|^2':>14s}  {'ratio':>10s}")
            print(f"      " + "-" * 50)

            for j in range(1, min(p - 1, 6)):
                chi = chars[j]
                denoms_int = denoms_arr.astype(int)
                chi_b = chi[denoms_int % p]
                weights = chi_b / denoms_arr**s_val
                T_m1 = np.sum(weights * np.exp(2j * pi * fracs_arr))

                Ls = L_function_fast(s_val, chi, p)
                Ls_sq = abs(Ls)**2
                T_sq = abs(T_m1)**2

                ratio = T_sq / Ls_sq if Ls_sq > 1e-15 else 0
                print(f"      {j:3d}  {T_sq:18.8f}  {Ls_sq:14.6f}  {ratio:10.4f}")

    # -------------------------------------------------------
    # TEST E: The Nyman-Beurling approach
    # -------------------------------------------------------
    print("\n" + "=" * 78)
    print("TEST E: Nyman-Beurling kernel")
    print("rho(theta, x) = {theta/x} - theta * {1/x}")
    print("sum |rho(a/b, ...)|^2 and its connection to zeta zeros")
    print("=" * 78)

    for N in [10, 20, 50, 100]:
        fracs_arr = np.array([a/b for a, b in farey_generator(N)])
        n = len(fracs_arr)
        ideal = np.arange(n, dtype=np.float64) / n
        discs = fracs_arr - ideal

        # Compute sum of |{1/(b*f)}|^2 for the Farey fractions
        # weighted by the disc — this is the Nyman-Beurling inner product
        NB_sum = 0.0
        for j in range(1, n):  # skip 0/1
            f = fracs_arr[j]
            if f > 0:
                rho = 1.0/f - int(1.0/f)  # {1/f}
                NB_sum += rho * discs[j]

        # Also compute the Mertens weighted version
        Mertens_weighted = 0.0
        for k in range(1, N + 1):
            Mertens_weighted += M[k] / sqrt(k)

        print(f"  N={N:4d}: n={n:5d}, NB_sum={NB_sum:12.6f}, "
              f"M_weighted(1/2)={Mertens_weighted:10.4f}, "
              f"W(N)={np.dot(discs,discs):12.8f}")

    elapsed = time.time() - start
    print(f"\nTotal time: {elapsed:.1f}s")

if __name__ == '__main__':
    main()
