#!/usr/bin/env python3
"""
Deeper analysis of the sampling ratio.

Key question: WHY does sum E(k/p)^2 = 2 * (p-1)/n * sum D(f)^2?

Approach: Use the Ramanujan sum expansion of the counting function.

The Farey counting function N_{F_N}(x) = sum_{b=1}^N sum_{a/b <= x, gcd(a,b)=1} 1
can be written via Mobius inversion as:
  N_{F_N}(x) = sum_{b=1}^N floor(bx) * sum_{d|b} mu(d) [Nope, need more care]

Actually, more directly:
  N_{F_N}(x) = 1 + sum_{m=1}^N M(floor(N/m)) * floor(mx)

where M is the Mertens function. This is the Franel-Landau representation.

So E(x) = N_{F_N}(x) - nx = 1 + sum_{m=1}^N M(floor(N/m)) * (floor(mx) - mx) + [n - sum M(N/m)*m]*x
        = 1 + sum_{m=1}^N M(floor(N/m)) * B_1(mx) + correction

where B_1(x) = {x} - 1/2 is the first Bernoulli periodic function, and we used
floor(mx) = mx - {mx} = mx - (1/2 - B_1(mx)).

Actually let's be more precise. Let psi(x) = {x} - 1/2.
floor(mx) = mx - {mx} = mx - 1/2 - psi(mx).

So N_{F_N}(x) = 1 + sum_m M(N/m)(mx - 1/2 - psi(mx))
             = 1 + nx - n/2 - sum_m M(N/m)*psi(mx) + correction

Wait, sum_m M(N/m)*m = sum_m M(N/m)*m. This needs a separate identity.

Let me just compute things numerically to understand the Fourier structure.

For E(x) = N_{F_N}(x) - nx, we have E sampled at x=k/p for k=1,...,p-1.

The DFT of E(k/p) over k is:
  E_hat(h) = sum_{k=1}^{p-1} E(k/p) * exp(-2*pi*i*h*k/p)

By Parseval: sum |E(k/p)|^2 = (1/(p-1)) sum |E_hat(h)|^2.

Now, using N_{F_N}(x) = 1 + sum_m M(N/m) floor(mx):
E(x) = 1 + sum_m M(N/m) floor(mx) - nx
     = 1 + sum_m M(N/m) [mx - {mx}] - nx
     = 1 + sum_m M(N/m)*mx - sum_m M(N/m)*{mx} - nx

The first sum: sum_m M(N/m)*m = sum_m M(N/m)*m. Note sum_{m=1}^N mu(m) = M(N),
and sum_{m=1}^N m*mu(m) is related to phi.

Actually: sum_{d=1}^N phi(d) = (1/2) sum_{d=1}^N mu(d) * floor(N/d) * (floor(N/d)+1)
Hmm, this is getting complicated. Let me just check the Parseval identity numerically
and see if the "aliasing" interpretation works.
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
    """Return M(k) for k=0,...,N."""
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

# For each prime p, decompose E(k/p) using the Mertens representation
# and understand the aliasing

for p in [23, 47, 89, 127, 199]:
    if not is_prime(p):
        continue
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)
    M_vals, mu = mertens_values(N)

    # E(k/p) = N_{F_N}(k/p) - n*k/p
    # Using: N_{F_N}(x) = 1 + sum_{m=1}^N M(floor(N/m)) * floor(mx)

    E_exact = []
    for k in range(1, p):
        x = Fraction(k, p)
        count = sum(1 for f in F_N if f <= x)
        E_exact.append(float(count - n * x))

    # Now decompose E(k/p) using Mertens:
    # E(k/p) = 1 + sum_m c_m * floor(mk/p) - n*k/p
    # where c_m = M(floor(N/m))
    # = 1 + sum_m c_m * (mk/p - {mk/p}) - n*k/p
    # = 1 + (k/p) * (sum_m c_m*m - n) - sum_m c_m * {mk/p}
    # The first part is a linear correction (should be 0 or small)
    # The second part involves sawtooth functions sampled at k/p

    c = [0] * (N + 1)
    for m in range(1, N + 1):
        c[m] = M_vals[N // m]

    linear_coeff = sum(c[m] * m for m in range(1, N + 1)) - n
    print(f"\np = {p}, N = {N}, n = {n}")
    print(f"  Linear coefficient (sum c_m*m - n) = {linear_coeff}")

    # Sawtooth sum: -sum_m c_m * {{mk/p}}
    # where {{x}} = {x} = x - floor(x)

    # The key insight: {mk/p} for k=1,...,p-1 with m < p
    # If gcd(m,p) = 1 (which it is since p is prime and 1<=m<=N=p-1):
    # k -> mk mod p is a permutation of {1,...,p-1}
    # So {mk/p} = (mk mod p)/p

    # Therefore: sum_{k=1}^{p-1} {mk/p}^2 = sum_{j=1}^{p-1} (j/p)^2 = (p-1)(2p-1)/(6p^2)
    # This is the SAME for all m! (as long as gcd(m,p)=1)

    # This means the "sawtooth energy" is the same at each frequency m.
    # The total sum E^2 involves cross terms between different m values.

    # Let's verify the Mertens representation:
    E_mertens = []
    for k in range(1, p):
        val = 1.0
        for m in range(1, N + 1):
            val += c[m] * (m * k // p)  # floor(mk/p)
        val -= n * k / p
        E_mertens.append(val)

    # Check agreement
    max_diff = max(abs(E_exact[i] - E_mertens[i]) for i in range(p - 1))
    print(f"  Max |E_exact - E_mertens| = {max_diff:.6f}")

    # Now compute: sum E^2 using the Mertens decomposition
    # E(k/p) = constant + linear*k/p - sum_m c_m * {mk/p}
    # The {mk/p} part is the sawtooth.

    # Key formula: sum_{k=1}^{p-1} E(k/p)^2
    # The sawtooth part: S(k) = sum_m c_m * {mk/p}
    # sum S(k)^2 = sum_{m,m'} c_m c_{m'} sum_k {mk/p}{m'k/p}

    # Now: sum_{k=1}^{p-1} {mk/p} * {m'k/p}
    # = sum_{k=1}^{p-1} ((mk mod p)/p) * ((m'k mod p)/p)

    # If m = m': sum = sum_{j=1}^{p-1} (j/p)^2 = (p-1)(2p-1)/(6p^2)

    # If m != m': Let r = m'/m mod p. Then m'k mod p = r*(mk mod p) mod p.
    # So sum = (1/p^2) sum_{j=1}^{p-1} j * (rj mod p)
    # This is a MULTIPLICATIVE correlation sum!

    # Let T(r) = sum_{j=1}^{p-1} j * (rj mod p) for r != 0 mod p
    # = sum_j j * {rj - p*floor(rj/p)} hmm, rj mod p for j in {1,...,p-1}

    # For r=1: T(1) = sum j^2 = p(p-1)(2p-1)/6
    # For general r: T(r) = sum_j j*(rj mod p)

    # Note: sum_{k=1}^{p-1} {mk/p}{m'k/p} = T(m'm^{-1} mod p) / p^2

    # Diagonal: T(1)/p^2 = (p-1)(2p-1)/(6p)
    # Off-diagonal: T(r)/p^2 for r != 1

    # The total: sum E^2 involves sum_{m,m'} c_m c_{m'} T(m'm^{-1})/p^2

    # Now the key: what is T(r) for r != 1?

    # T(r) = sum_{j=1}^{p-1} j * (rj mod p)
    # Let sigma_r(j) = rj mod p (a permutation of {1,...,p-1})
    # T(r) = sum_j j * sigma_r(j) = correlation between identity and sigma_r

    # Known: for random permutation, E[sum j*sigma(j)] = (p-1)^2 * p/4
    # And T(1) = sum j^2 = p(p-1)(2p-1)/6 ~ p^3/3
    # While E[T] ~ p^3/4

    # For r != 1 mod p:
    # T(r) = sum_j j*rj - p*sum_j j*floor(rj/p)
    # = r*sum j^2 - p*sum j*floor(rj/p)
    # = r*p(p-1)(2p-1)/6 - p*S(r)

    # where S(r) = sum_{j=1}^{p-1} j*floor(rj/p)

    # Hmm, this is getting into Dedekind sum territory.

    # Let me just compute T(r) for small p and check patterns.

    if p <= 89:
        T = {}
        for r in range(1, p):
            val = sum(j * ((r * j) % p) for j in range(1, p))
            T[r] = val

        T_diag = T[1]  # = sum j^2 = p(p-1)(2p-1)/6
        T_diag_formula = p * (p - 1) * (2 * p - 1) // 6
        print(f"  T(1) = {T_diag}, formula = {T_diag_formula}")

        # Average of T(r) for r != 1
        T_off = [T[r] for r in range(2, p)]
        T_off_avg = sum(T_off) / len(T_off)
        print(f"  avg T(r), r!=1: {T_off_avg:.2f}")
        print(f"  (p-1)^2*p/4 = {(p-1)**2 * p / 4:.2f}")  # expected for uniform

        # Key: sum over all r: sum_{r=1}^{p-1} T(r) = sum_j j * sum_r (rj mod p)
        # = sum_j j * sum_{s=1}^{p-1} s = sum_j j * p(p-1)/2 = p(p-1)/2 * p(p-1)/2
        T_total = sum(T.values())
        print(f"  sum T(r) = {T_total}, (p(p-1)/2)^2 = {(p*(p-1)//2)**2}")

        # So avg T(r) = T_total/(p-1) = p(p-1)^2/4...no
        # sum_r T(r) = (p(p-1)/2)^2, so avg = p^2(p-1)^2/(4(p-1)) = p^2(p-1)/4
        # Hmm let me recheck
        avg_all = T_total / (p - 1)
        print(f"  avg T(r) all r: {avg_all:.2f}, p^2(p-1)/4 = {p**2*(p-1)/4:.2f}")

        # Off-diagonal average:
        # (T_total - T(1))/(p-2) = (p^2(p-1)^2/4 - p(p-1)(2p-1)/6) / (p-2)
        off_diag_avg_formula = ((p*(p-1)/2)**2 - p*(p-1)*(2*p-1)/6) / (p - 2)
        print(f"  Off-diag avg: {T_off_avg:.2f}, formula: {off_diag_avg_formula:.2f}")

        # Now the CRUCIAL calculation:
        # sum E^2 involves (ignoring the linear/constant part):
        # sum_k (sum_m c_m {mk/p})^2 = (1/p^2) sum_{m,m'} c_m c_{m'} T(m' m^{-1})
        #
        # Diagonal (m=m'): (1/p^2) sum_m c_m^2 * T(1) = T(1)/p^2 * sum c_m^2
        # Off-diagonal: (1/p^2) sum_{m!=m'} c_m c_{m'} T(m' m^{-1})
        #
        # If the off-diagonal sum ~ (avg T off-diag) * (sum c_m)^2 - sum c_m^2)
        #   = off_diag_avg * ((sum c_m)^2 - sum c_m^2)

        sum_c = sum(c[m] for m in range(1, N + 1))
        sum_c_sq = sum(c[m]**2 for m in range(1, N + 1))

        print(f"\n  sum c_m = {sum_c}, sum c_m^2 = {sum_c_sq}")
        print(f"  (sum c_m)^2 = {sum_c**2}")

        # Exact quadratic form:
        # Q = sum_{m,m'=1}^N c_m c_{m'} T(m' * m_inv mod p) / p^2
        # Note: m_inv = inverse of m mod p (exists since p prime, m < p)
        # Actually m ranges 1..N=p-1, all coprime to p

        Q = 0
        for m1 in range(1, N + 1):
            m1_inv = pow(m1, p - 2, p)  # Fermat's little theorem
            for m2 in range(1, N + 1):
                r = (m2 * m1_inv) % p
                Q += c[m1] * c[m2] * T[r]
        Q /= p**2

        print(f"  Quadratic form Q = {Q:.4f}")
        print(f"  Actual sum E^2 = {sum(e**2 for e in E_exact):.4f}")

        # Diagonal contribution
        Q_diag = sum_c_sq * T_diag / p**2
        Q_off = Q - Q_diag
        print(f"  Q_diag = {Q_diag:.4f}, Q_off = {Q_off:.4f}")
        print(f"  Q_diag/Q = {Q_diag/Q:.4f}, Q_off/Q = {Q_off/Q:.4f}")

        # The factor of 2: does Q_diag ~ Q_off?
        # If off-diag contributes equally to diag, total ~ 2 * diag

        # Connection to D(f)^2:
        # sum D(f)^2 relates to sum c_m^2 via Franel's theorem
        sum_D_sq = sum(float(Fraction(i, 1) - n*f)**2 for i, f in enumerate(F_N))
        print(f"\n  sum D(f)^2 = {sum_D_sq:.4f}")

        # The ratio we want:
        ratio = sum(e**2 for e in E_exact) / ((p-1)/n * sum_D_sq)
        print(f"  Ratio sum_E^2 / [(p-1)/n * sum_D^2] = {ratio:.4f}")

        # Franel: sum D^2 ~ sum_{m=1}^N M(N/m)^2 / (something)
        # Actually the exact identity is more complex.
        # sum c_m^2 = sum M(floor(N/m))^2

        franel_sum = sum(M_vals[N // m]**2 for m in range(1, N + 1))
        print(f"  sum M(N/m)^2 = {franel_sum}")
        print(f"  sum c_m^2 = {sum_c_sq}")  # should be same
        # Yes, c_m = M(floor(N/m)), so sum c_m^2 = sum M(floor(N/m))^2

        # CRITICAL INSIGHT:
        # Q_diag = sum_c_sq * T(1)/p^2 = sum M(N/m)^2 * p(p-1)(2p-1)/(6p^2)
        #        = sum M(N/m)^2 * (p-1)(2p-1)/(6p)
        # For large p: ~ sum M(N/m)^2 * p/3

        # And sum_E^2 / [(p-1)/n * sum D^2] ~ 2
        # means sum_E^2 ~ 2(p-1)/n * sum D^2

        # If Q = sum_E^2 and Q_diag ~ Q/2, then:
        # Q ~ 2 * Q_diag = 2 * sum_c_sq * (p-1)(2p-1)/(6p^2)

        # But we need to connect sum_c_sq to sum D^2...

print("\n\n=== KEY INSIGHT: DIAGONAL VS OFF-DIAGONAL ===\n")
print("If the off-diagonal contribution equals the diagonal, we get factor 2.")
print("The question is: why does this happen?\n")
print("Diagonal: sum_m c_m^2 * T(1)/p^2")
print("Off-diag: sum_{m!=m'} c_m c_{m'} * T(m'm^{-1})/p^2")
print()
print("For T(r) with r random in Z_p^*: E[T(r)] = off_diag_avg")
print("The off-diagonal has (N^2 - N) terms, each with weight ~ off_diag_avg/p^2")
print("vs diagonal with N terms, each with weight T(1)/p^2 = (2p-1)(p-1)/(6p)")

# Final quantitative check
for p in [47, 89, 127]:
    if not is_prime(p):
        continue
    N = p - 1
    T1 = p * (p-1) * (2*p-1) // 6  # T(1) = sum j^2
    T_avg_off = ((p*(p-1)//2)**2 - T1) / (p - 2)  # average off-diagonal T(r)

    print(f"\np={p}:")
    print(f"  T(1) = {T1}")
    print(f"  T_off_avg = {T_avg_off:.2f}")
    print(f"  T_off_avg / T(1) = {T_avg_off/T1:.4f}")
    print(f"  (p+1)/(2(2p-1)) [prediction] = {(p+1)/(2*(2*p-1)):.4f}")
    # For the off-diagonal average:
    # T_off_avg = (p^2(p-1)^2/4 - p(p-1)(2p-1)/6) / (p-2)
    # = p(p-1)[(p(p-1)/4 - (2p-1)/6)] / (p-2)
    # = p(p-1)[3p(p-1) - 2(2p-1)] / (12(p-2))
    # = p(p-1)(3p^2 - 3p - 4p + 2) / (12(p-2))
    # = p(p-1)(3p^2 - 7p + 2) / (12(p-2))
    # = p(p-1)(3p-1)(p-2) / (12(p-2))
    # = p(p-1)(3p-1)/12

    T_off_formula = p * (p-1) * (3*p - 1) / 12
    print(f"  T_off exact formula: p(p-1)(3p-1)/12 = {T_off_formula:.2f}")
    print(f"  vs computed: {T_avg_off:.2f}")

    # So T_off / T(1) = [p(p-1)(3p-1)/12] / [p(p-1)(2p-1)/6]
    # = (3p-1) / (2(2p-1))
    # For large p: -> 3/(2*2) = 3/4
    ratio_TT = (3*p - 1) / (2 * (2*p - 1))
    print(f"  T_off/T(1) = (3p-1)/(2(2p-1)) = {ratio_TT:.4f}")
