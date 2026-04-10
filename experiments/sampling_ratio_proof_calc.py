#!/usr/bin/env python3
"""
PRECISE proof calculation for the sampling ratio.

The approach:
1. Express E(k/p) exactly via the Mertens representation
2. Compute sum E(k/p)^2 as a quadratic form in M(floor(N/m)) values
3. Connect to sum D(f)^2 via the Franel-Landau identity
4. Show that the ratio is 2 + O(1/p)

Key identities needed:
- T(r) = sum_{j=1}^{p-1} j*(rj mod p) for r in Z_p^*
  T(1) = p(p-1)(2p-1)/6
  avg T(r) over r != 1 = p(p-1)(3p-1)/12

- N_{F_N}(x) = 1 + sum_{m=1}^N M(floor(N/m)) * floor(mx)  [Franel-Landau]

- E(x) = N_{F_N}(x) - nx

CRITICAL: The representation E(k/p) = -sum_m c_m * {mk/p} + (linear in k)
captures the sawtooth structure. The sum E^2 is a bilinear form in c_m values
evaluated through T(r) correlations mod p.
"""

import numpy as np
from fractions import Fraction
from math import gcd

def farey_sequence(N):
    fracs = set()
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def mertens_values(N):
    mu = [0] * (N + 1)
    mu[1] = 1
    for i in range(1, N + 1):
        for j in range(2*i, N + 1, i):
            mu[j] -= mu[i]
    M = [0] * (N + 1)
    for k in range(1, N + 1):
        M[k] = M[k-1] + mu[k]
    return M, mu

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

print("=== EXACT DECOMPOSITION OF SUM E(k/p)^2 ===\n")

for p in [11, 23, 47, 67, 89, 127]:
    if not is_prime(p): continue
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)
    M, mu = mertens_values(N)

    c = [0] * (N + 1)
    for m in range(1, N + 1):
        c[m] = M[N // m]

    # E(k/p) exactly
    E_vals = []
    for k in range(1, p):
        x = Fraction(k, p)
        count = sum(1 for f in F_N if f <= x)
        E_vals.append(float(count - n * x))

    sum_E_sq = sum(e**2 for e in E_vals)
    sum_D_sq = sum(float(Fraction(i, 1) - n * f)**2 for i, f in enumerate(F_N))

    # The ratio
    ratio = sum_E_sq / ((p - 1) / n * sum_D_sq)

    # Now compute the Franel-Landau connection:
    # By Franel's theorem (simplified form for our purposes):
    # sum_{f in F_N} D(f)^2 = sum related to M(N/m)
    #
    # More precisely, the Franel identity gives:
    # sum_{j=0}^{n-1} (f_j - j/n)^2 = ... involving M(N/m)
    # But D(f_j) = j - n*f_j, so sum D^2 = n^2 * sum (f_j - j/n)^2

    # What we really need: sum D^2 vs sum c_m^2
    sum_c_sq = sum(c[m]**2 for m in range(1, N + 1))

    # Direct connection attempt:
    # E(k/p) = 1 + sum_m c_m * floor(mk/p) - n*k/p
    #
    # Note floor(mk/p) = (mk - (mk mod p)) / p for integer m,k and p prime
    # So E(k/p) = 1 + sum_m c_m * (mk - (mk mod p))/p - n*k/p
    #           = 1 + (k/p)*(sum_m c_m*m) - (1/p)*sum_m c_m*(mk mod p) - n*k/p
    #
    # sum_m c_m * m = n - 1 (this is a known identity: n = 1 + sum_m M(N/m)*m)
    # So (k/p)*(sum_m c_m*m) - n*k/p = (k/p)*(n-1-n) = -k/p
    #
    # Therefore: E(k/p) = 1 - k/p - (1/p)*sum_m c_m*(mk mod p)
    #                    = (p-k)/p - (1/p)*sum_m c_m*(mk mod p)

    # Let S(k) = sum_m c_m * (mk mod p). Then:
    # E(k/p) = (p-k)/p - S(k)/p

    # Verify this identity:
    for k_test in [1, 2, p//2, p-1]:
        if k_test < 1 or k_test >= p: continue
        S_k = sum(c[m] * ((m * k_test) % p) for m in range(1, N + 1))
        E_formula = (p - k_test) / p - S_k / p
        E_direct = E_vals[k_test - 1]
        if abs(E_formula - E_direct) > 1e-8:
            print(f"  MISMATCH at k={k_test}: formula={E_formula:.6f}, direct={E_direct:.6f}")

    # Now: sum_{k=1}^{p-1} E(k/p)^2
    # = (1/p^2) * sum_k [(p-k) - S(k)]^2
    # = (1/p^2) * [sum_k (p-k)^2 - 2 sum_k (p-k)*S(k) + sum_k S(k)^2]

    # Term 1: sum_k (p-k)^2 = sum_{j=1}^{p-1} j^2 = p(p-1)(2p-1)/6
    T1 = p * (p - 1) * (2*p - 1) // 6

    # Term 2: sum_k (p-k)*S(k)
    # = sum_k (p-k) * sum_m c_m * (mk mod p)
    # = sum_m c_m * sum_k (p-k)*(mk mod p)
    # Now k -> mk mod p is a permutation of {1,...,p-1}, so let j = mk mod p.
    # Then k = m^{-1}*j mod p, so p-k = p - (m^{-1}*j mod p).
    # This is complicated. Let's use: sum_k (p-k)*(mk mod p) = sum_k (p-k)*sigma_m(k)
    # where sigma_m is the mult-by-m permutation.
    # = p*sum_k sigma_m(k) - sum_k k*sigma_m(k)
    # = p * p(p-1)/2 - T(m)
    # where T(m) = sum_k k*(mk mod p)

    # So Term 2 = sum_m c_m * [p^2(p-1)/2 - T(m)]
    #           = p^2(p-1)/2 * sum_m c_m - sum_m c_m * T(m)

    # sum_m c_m = M(N) (since c_m = M(N/m) and we evaluate at m=1: c_1=M(N))
    # Wait, sum c_m = sum_{m=1}^N M(floor(N/m)). This equals:
    # sum_{m=1}^N sum_{j=1}^{floor(N/m)} mu(j) = sum_{j=1}^N mu(j) * floor(N/j)
    # = sum_{j=1}^N mu(j) * floor(N/j)
    # But n - 1 = sum_{d=1}^N phi(d) = sum_{j=1}^N mu(j) * floor(N/j) * (floor(N/j)+1) / 2
    # Hmm, not the same.
    # Actually sum_{m=1}^N M(floor(N/m)) = sum_{m=1}^N sum_{j=1}^{floor(N/m)} mu(j)
    # = sum_{j=1}^N mu(j) * #{m: floor(N/m) >= j} = sum_{j=1}^N mu(j) * floor(N/j)
    # This is not 1. Let me compute it.

    sum_c = sum(c[m] for m in range(1, N + 1))
    sum_c_times_m = sum(c[m] * m for m in range(1, N + 1))

    # Compute T(m) for all m
    T_m = {}
    for m in range(1, min(N + 1, p)):
        T_m[m] = sum(k * ((m * k) % p) for k in range(1, p))

    # Term 2
    term2 = sum(c[m] * (p**2 * (p-1) // 2 - T_m.get(m, 0)) for m in range(1, N + 1))

    # Term 3: sum_k S(k)^2 = sum_{m,m'} c_m c_{m'} sum_k (mk mod p)(m'k mod p)
    # sum_k (mk mod p)(m'k mod p) = T(m' * m^{-1} mod p)
    # (since k -> mk mod p permutes {1,...,p-1})
    # Wait: sum_k sigma_m(k) * sigma_{m'}(k) = sum_k (mk mod p)*(m'k mod p)
    # Let j = mk mod p, then k = m^{-1}j mod p, and m'k mod p = m'm^{-1}j mod p.
    # So sum = sum_j j * (m'm^{-1}j mod p) = T(m'm^{-1} mod p).

    # Hmm but we need T for argument being m'm^{-1} mod p, which is in {1,...,p-1}.
    # m, m' range from 1 to N = p-1, so m'm^{-1} ranges over all of Z_p^*.
    # And T is defined on Z_p^* via T(r) = sum_j j*(rj mod p).

    # We already know:
    # T(1) = p(p-1)(2p-1)/6
    # sum_r T(r) = (p(p-1)/2)^2
    # avg T(r) for r != 1 = p(p-1)(3p-1)/12

    # Term 3 = sum_{m,m'} c_m c_{m'} T(m'm^{-1})
    # = sum_c_sq * T(1) + sum_{m!=m'} c_m c_{m'} * T(m'm^{-1})

    # The off-diagonal part: for each pair (m,m') with m!=m', r = m'm^{-1} mod p
    # ranges over all of Z_p^* \ {1}.

    # KEY INSIGHT: For fixed m, as m' ranges over {1,...,N}\{m},
    # r = m'm^{-1} mod p ranges over {1,...,p-1}\{1} = all non-identity elements.
    # And this is a bijection! So for each fixed m:
    # sum_{m'!=m} c_{m'} * T(m'm^{-1}) = sum_{r!=1} c_{m*r mod p} * T(r)
    #   (where m*r mod p maps back to the index m')

    # But c_{m'} = M(floor(N/(m'))), so c_{m*r mod p} = M(floor(N/(m*r mod p)))
    # This is NOT simply c_r or anything nice -- it depends on both m and r.

    # However, in the SUM over all m, we get:
    # Term 3 = sum_{m} sum_{m'} c_m c_{m'} T(m'm^{-1})
    #         = sum_r T(r) * [sum_{m} c_m * c_{mr mod p}]

    # Define: C(r) = sum_{m=1}^{N} c_m * c_{mr mod p}
    # (autocorrelation of c under multiplicative shifts mod p)

    # Then Term 3 = sum_{r=1}^{p-1} T(r) * C(r)

    # The ratio sum_E^2 / [(p-1)/n * sum_D^2] = 2 translates to:
    # sum_E^2 = 2(p-1)/n * sum_D^2
    # The left side involves T(r) and C(r).
    # The right side involves sum_D^2 which connects to c_m via Franel.

    # Let's compute C(r) for each r
    C_r = {}
    for r in range(1, p):
        val = 0
        for m in range(1, N + 1):
            mp = (m * r) % p
            if 1 <= mp <= N:
                val += c[m] * c[mp]
        C_r[r] = val

    # C(1) = sum c_m^2 = sum_c_sq
    print(f"\np={p}: n={n}, N={N}")
    print(f"  C(1) = sum c_m^2 = {C_r[1]}, sum_c_sq = {sum_c_sq}")

    # Average C(r) for r != 1
    C_off_avg = sum(C_r[r] for r in range(2, p)) / (p - 2)
    print(f"  avg C(r), r!=1: {C_off_avg:.4f}")
    print(f"  (sum c)^2 / (p-1) = {sum_c**2 / (p-1):.4f}")

    # Full computation
    term3 = sum(T_m.get(r, 0) * C_r.get(r, 0) for r in range(1, p))

    # Put it all together:
    # sum E^2 = (1/p^2) [T1 - 2*term2 + term3]
    sum_E_computed = (T1 - 2 * term2 + term3) / p**2
    print(f"  sum_E^2: direct={sum_E_sq:.4f}, computed={sum_E_computed:.4f}")
    print(f"  T1/p^2={T1/p**2:.4f}, 2*term2/p^2={2*term2/p**2:.4f}, term3/p^2={term3/p**2:.4f}")

    # The crucial decomposition for the ratio:
    # sum E^2 = (T1 - 2*term2 + term3) / p^2
    #
    # T1/p^2 = (p-1)(2p-1)/(6p) ~ p/3
    #
    # For the factor-of-2 identity, we need to show that this equals
    # 2*(p-1)/n * sum_D^2

    # Let's see what 2*(p-1)/n * sum_D^2 is
    target = 2 * (p - 1) / n * sum_D_sq
    print(f"  2(p-1)/n * sum_D^2 = {target:.4f}")
    print(f"  RATIO = {sum_E_sq / target:.6f}")

    # Connection via T(r) and C(r):
    # The dominant term in term3 is T(1)*C(1) = T(1) * sum_c_sq
    print(f"\n  Decomposition of term3:")
    t3_diag = T_m.get(1, 0) * C_r.get(1, 0)
    t3_off = term3 - t3_diag
    print(f"  T(1)*C(1) = {t3_diag}")
    print(f"  Off-diagonal = {t3_off}")
    print(f"  Off/Diag = {t3_off/t3_diag:.4f}")

    # The factor 2 question reduces to understanding the structure of C(r) * T(r).

    # Key test: what if C(r) were constant for all r?
    # Then C(r) = C_avg = sum_{r} C(r) / (p-1)
    # sum_r C(r) = sum_r sum_m c_m c_{mr} = sum_m c_m sum_r c_{mr}
    # For each m: sum_r c_{mr mod p} = sum_{m'=1}^{N} c_{m'} = sum_c
    # (since mr mod p bijects {1,...,p-1} to {1,...,p-1})
    # So sum_r C(r) = sum_c * sum_c = sum_c^2

    sum_C = sum(C_r.values())
    print(f"\n  sum C(r) = {sum_C}, (sum c)^2 = {sum_c**2}")

    # So C_avg = (sum_c)^2 / (p-1) which is very small (sum_c = M(N) which is ~1)

    # The non-trivial part: C(1) = sum c_m^2 is MUCH larger than C_avg.
    # For r != 1: C(r) = sum c_m * c_{mr} represents the "correlation" of the
    # Mertens values under multiplicative shift by r.

    # These correlations C(r) for r != 1 carry the information about
    # whether the off-diagonal terms amplify or suppress the sum.

    # Print a few C(r) values
    if p <= 89:
        C_list = [(r, C_r[r]) for r in range(1, p)]
        C_list.sort(key=lambda x: abs(x[1]), reverse=True)
        print(f"\n  Top |C(r)| values:")
        for r, val in C_list[:10]:
            print(f"    r={r:>4}: C(r)={val:>8}")

print("\n\n=== ALTERNATIVE: INTEGRAL APPROACH ===\n")
# Instead of the bilinear form, let's directly verify the integral identity:
# integral_0^1 E(x)^2 dx = sum_D^2 / n
# and the Riemann sum approximation:
# (1/(p-1)) sum_{k=1}^{p-1} E(k/p)^2 = 2 * integral + o(integral)

for p in [47, 89, 127, 199]:
    if not is_prime(p): continue
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)

    # D(f) values
    D_vals = [float(Fraction(i, 1) - n * f) for i, f in enumerate(F_N)]
    sum_D_sq = sum(d**2 for d in D_vals)

    # E(k/p)
    E_vals = []
    for k in range(1, p):
        x = Fraction(k, p)
        count = sum(1 for f in F_N if f <= x)
        E_vals.append(float(count - n * x))

    sum_E_sq = sum(e**2 for e in E_vals)

    # Numerical integral of E(x)^2 using trapezoidal rule on a fine grid
    # E(x) is piecewise linear between consecutive Farey fractions
    # At each Farey fraction f_j, E(f_j) = D(f_j) (since the count jumps by 1)
    # Between f_j and f_{j+1}, E(x) = j+1 - n*x (count stays at j+1)

    # Actually E(x) = N_{F_N}(x) - n*x
    # N_{F_N} is a step function that jumps at each f_j.
    # Between f_j and f_{j+1}: N_{F_N}(x) = j+1 (for x in (f_j, f_{j+1}])
    # So E(x) = (j+1) - n*x on (f_j, f_{j+1}]

    # integral of E(x)^2 from f_j to f_{j+1}:
    # integral of ((j+1) - nx)^2 dx from a to b
    # = integral (j+1)^2 - 2(j+1)nx + n^2 x^2 dx
    # = (j+1)^2 (b-a) - (j+1)n(b^2-a^2) + n^2(b^3-a^3)/3

    integral_E_sq = 0
    for j in range(len(F_N) - 1):
        a = float(F_N[j])
        b = float(F_N[j + 1])
        c_val = j + 1  # E(x) = c_val - n*x on (a,b]
        # Actually E(x) = N_{F_N}(x) - n*x. For x in (f_j, f_{j+1}),
        # N_{F_N}(x) = j+1 (0-indexed: f_0,...,f_{n-1}; after f_j we've counted j+1 fractions)
        # Wait, we need to be careful with 0-indexing.
        # f_0 = 0/1, f_1, ..., f_{n-1} = 1/1
        # For x in (f_j, f_{j+1}]: N_{F_N}(x) = j + 1
        # So E(x) = (j+1) - n*x

        c_j = j + 1
        integral_E_sq += c_j**2 * (b - a) - c_j * n * (b**2 - a**2) + n**2 * (b**3 - a**3) / 3

    print(f"p={p}: integral E^2 = {integral_E_sq:.4f}")
    print(f"  sum D^2 / n = {sum_D_sq / n:.4f}")
    print(f"  Ratio integral / (sum_D^2/n) = {integral_E_sq / (sum_D_sq / n):.6f}")
    print(f"  Riemann sum (1/(p-1)) sum E^2 = {sum_E_sq / (p-1):.4f}")
    print(f"  Riemann / integral = {(sum_E_sq / (p-1)) / integral_E_sq:.6f}")
    print(f"  Overall ratio = {sum_E_sq / ((p-1)/n * sum_D_sq):.6f}")
    print()
