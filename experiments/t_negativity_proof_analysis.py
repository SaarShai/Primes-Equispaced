#!/usr/bin/env python3
"""
Analysis for proving T(N) < 0 for all N >= 42 with M(N) = -2.

We have: T(N) = 3 + 6 * E(N), where E(N) = sum_{q=2}^{N} e(q)
and e(q) = prod_{p|q}(1-p) / (6q).

So T(N) < 0 iff E(N) < -1/2.

Strategy:
1. Decompose E(N) by omega(q) (number of distinct prime factors).
2. Show that the omega=1 (primes + prime powers) contribution dominates and is < -1/2.
3. Bound the omega >= 2 contributions.

Key: E_1(N) = sum_{q<=N, omega(q)=1} e(q)
           = sum_{p<=N} sum_{k=1}^{v_p(N)} (1-p)/(6*p^k)
           = sum_{p<=N} (1-p)/(6p) * (1 - p^{-v_p(N)}) / (1 - 1/p) ... no, simpler:
           = (1/6) * sum_{p<=N} (1-p)/p * [1 + 1/p + ... + 1/p^{v_p-1}]

Actually: sum_{k=1}^{a} (1-p)/(6*p^k) = (1-p)/6 * (1/p + 1/p^2 + ... + 1/p^a)
         = (1-p)/6 * (1/p)*(1 - 1/p^a)/(1 - 1/p)
         = (1-p)/6 * (1 - p^{-a}) / (p - 1)
         = -(1 - p^{-a})/6

So E_1(N) = -(1/6) * sum_{p<=N} (1 - p^{-v_p(N)}) where v_p(N) = floor(log_p(N)).

For p <= sqrt(N): v_p >= 2, so 1 - p^{-v_p} >= 1 - 1/p^2 >= 3/4.
For p > sqrt(N): v_p = 1, so 1 - 1/p.

Therefore: E_1(N) = -(1/6) * [sum_{p<=sqrt(N)} (1 - p^{-v_p}) + sum_{sqrt(N)<p<=N} (1 - 1/p)]

The second sum dominates:
  sum_{sqrt(N)<p<=N} (1 - 1/p) = pi(N) - pi(sqrt(N)) - sum_{sqrt(N)<p<=N} 1/p

For the omega >= 2 contribution, the key is that it CANCELS most of E_1.
But we need to show the net E(N) < -1/2.
"""

from math import log, sqrt, gcd
import sys

def compute_mobius_sieve(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime = [True] * (limit + 1)
    primes = []
    for p in range(2, limit + 1):
        if is_prime[p]:
            primes.append(p)
            mu[p] = -1
        for j, q in enumerate(primes):
            if p * q > limit:
                break
            is_prime[p * q] = False
            if p % q == 0:
                mu[p * q] = 0
                break
            else:
                mu[p * q] = -mu[p]
    return mu, primes

def prime_factors(n, primes):
    """Return set of distinct prime factors."""
    factors = []
    for p in primes:
        if p * p > n:
            break
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
    if n > 1:
        factors.append(n)
    return factors

def e_of_q(q, primes):
    """e(q) = prod_{p|q}(1-p) / (6q)."""
    product = 1
    for p in prime_factors(q, primes):
        product *= (1 - p)
    return product / (6 * q)

def main():
    LIMIT = 200000
    print(f"Sieving up to {LIMIT}...")
    mu, primes = compute_mobius_sieve(LIMIT)
    primes_set = set(primes)

    # Compute M(n)
    M = [0] * (LIMIT + 1)
    for n in range(1, LIMIT + 1):
        M[n] = M[n-1] + mu[n]

    # E(N) = sum_{q=2}^{N} e(q)
    # E_1(N) = omega=1 contribution
    # E_2(N) = omega=2 contribution
    # etc.

    # Track: among all N >= 42 with M(N) = -2, the max E(N)
    cum_E = 0.0
    cum_E1 = 0.0  # omega = 1
    cum_E2 = 0.0  # omega = 2
    cum_E3 = 0.0  # omega >= 3

    max_E_m2 = -float('inf')
    worst_N = None
    count_violates = 0

    # Also track: does E(N) < -1/2 always hold?
    print(f"\n{'N':>8} {'E(N)':>10} {'E1(om=1)':>10} {'E2(om=2)':>10} {'E3(om>=3)':>10} {'M(N)':>5} {'T(N)':>10}")

    for N in range(2, LIMIT + 1):
        eq = e_of_q(N, primes)
        pf = prime_factors(N, primes)
        om = len(pf)
        cum_E += eq
        if om == 1:
            cum_E1 += eq
        elif om == 2:
            cum_E2 += eq
        else:
            cum_E3 += eq

        if N >= 42 and M[N] == -2:
            T = 3 + 6 * cum_E
            if cum_E > max_E_m2:
                max_E_m2 = cum_E
                worst_N = N
            if cum_E >= -0.5:
                count_violates += 1
                print(f"{N:>8} {cum_E:>10.6f} {cum_E1:>10.4f} {cum_E2:>10.4f} {cum_E3:>10.4f} {M[N]:>5} {T:>10.4f} *** VIOLATION")

            # Print key milestones
            if N <= 200 or N == worst_N or N % 10000 == 0:
                print(f"{N:>8} {cum_E:>10.6f} {cum_E1:>10.4f} {cum_E2:>10.4f} {cum_E3:>10.4f} {M[N]:>5} {T:>10.4f}")

    print(f"\n=== RESULT ===")
    print(f"Max E(N) among N >= 42 with M(N) = -2: {max_E_m2:.8f} at N = {worst_N}")
    print(f"T(worst) = {3 + 6*max_E_m2:.6f}")
    print(f"Number of violations (E >= -0.5): {count_violates}")
    if count_violates == 0:
        print(f"CONFIRMED: E(N) < -0.5 for all N >= 42 with M(N) = -2 (up to {LIMIT})")
    else:
        print(f"VIOLATIONS FOUND!")

    # Now the key theoretical question:
    # The E_1(N) = -(1/6)*sum_{p<=N}(1 - p^{-v_p}) formula.
    # Compute E_1 directly via this formula and verify.
    print(f"\n=== E_1(N) formula verification ===")
    for N_test in [42, 100, 500, 1000, 10000]:
        E1_formula = 0.0
        for p in primes:
            if p > N_test:
                break
            vp = 1
            pk = p
            while pk * p <= N_test:
                pk *= p
                vp += 1
            E1_formula -= (1 - p**(-vp)) / 6

        E1_direct = sum(e_of_q(q, primes) for q in range(2, N_test+1) if len(prime_factors(q, primes)) == 1)
        print(f"  N={N_test}: E1_formula = {E1_formula:.8f}, E1_direct = {E1_direct:.8f}, match = {abs(E1_formula - E1_direct) < 1e-8}")

    # KEY INSIGHT: E_1(N) = -(1/6)*[pi(N) - sum_{p<=N} p^{-v_p(N)}]
    # The correction term sum p^{-v_p} is bounded:
    # For p > sqrt(N): v_p = 1, contributes 1/p. Sum ~ log log N.
    # For p <= sqrt(N): contributes at most 1/p^2. Sum < sum 1/p^2 = P(2) ~ 0.4522.
    # Total: sum p^{-v_p} <= log log N + P(2) + O(1/log N)

    # So E_1(N) = -(1/6)*[pi(N) - log log N - P(2) - O(1/log N)]

    # For the composite contributions E_2 + E_3 + ...:
    # These are bounded by the "excess" from semiprimes etc.
    # The KEY fact: sum_{q<=N} e(q) = sum_{q<=N} g(q)/(6q) where g = sum_{d|q} mu(d)*d.
    # This is (1/6) * sum_{q<=N} g(q)/q.

    # Using Dirichlet series: sum g(q)/q^s = prod_p (1 + (1-p)/p^s + (1-p)/p^{2s} + ...)
    # = prod_p (1 + (1-p)/(p^s(1-p^{-s})))
    # = prod_p (1 + (1-p)/(p^s - 1))
    # = prod_p ((p^s - 1 + 1 - p)/(p^s - 1))
    # = prod_p ((p^s - p)/(p^s - 1))
    # = prod_p (p(p^{s-1} - 1)/(p^s - 1))

    # At s=1: this becomes prod_p (p*(1-1)/(p-1)) which is 0! So the partial sums
    # sum g(q)/q converge to 0... but slowly. Actually the partial sums oscillate.

    # More useful: sum_{q<=N} g(q)/q = sum_{q<=N} (sum_{d|q} mu(d)*d)/q
    #            = sum_{d<=N} mu(d)*d * sum_{k<=N/d} 1/(dk)
    #            = sum_{d<=N} mu(d) * H(N/d)

    # So E(N) = (1/6)*sum_{d<=N} mu(d)*H(floor(N/d))

    # And we showed: sum_{m=1}^{N} M(floor(N/m))/m = sum_{k=1}^{N} mu(k)*H(floor(N/k))
    # (hyperbolic identity).

    # So 6*E(N) = sum mu(k)*H(floor(N/k)) = sum M(floor(N/m))/m = 6R(N) - 1.
    # Since 6R(N) = 2 + 6*E(N), we have 6*E(N) = 6R(N) - 2... wait.

    # R(N) = 1/3 + E(N), so 6R(N) = 2 + 6E(N). And sum M(fl)/m = 6R(N) - 1 = 1 + 6E(N).
    # Check: E(N) = (1/6)*sum mu(k)*H(fl(N/k)), so sum mu(k)*H = 6E(N). And sum M(fl)/m = sum mu(k)*H.
    # So sum M(fl)/m = 6E(N). But also sum M(fl)/m = 6R(N) - 1. So 6E(N) = 6R(N) - 1,
    # i.e., E(N) = R(N) - 1/6. And R(N) = 1/3 + E(N) = 1/3 + R(N) - 1/6 => 0 = 1/6.
    # CONTRADICTION! Something is wrong.

    # Let me recheck. R(N) = sum f_i^2 - n/3. The identity from CORRECTION_NEGATIVITY:
    # R(N) = 1/6 + (1/6)*sum_{m=1}^{N} M(floor(N/m))/m.
    # From R_NEGATIVE_PROOF: R(N) = 1/3 + sum_{q=2}^{N} e(q).
    # So: 1/3 + E(N) = 1/6 + (1/6)*S, where S = sum M(fl)/m.
    # => S = 6*(1/3 + E(N)) - 6*(1/6) = 2 + 6E(N) - 1 = 1 + 6E(N).
    # But also S = sum mu(k)*H(fl(N/k)) (hyperbolic identity).
    # And E(N) = (1/6)*sum mu(k)*H(fl(N/k))? Let me verify...

    # E(N) = sum_{q=2}^{N} e(q) = sum_{q=2}^{N} (sum_{d|q} mu(d)*d)/(6q)
    #       = (1/6)*sum_{q=2}^{N} (sum_{d|q} mu(d)*d)/q
    #       = (1/6)*sum_{d=1}^{N} mu(d)*d * sum_{k=1}^{floor(N/d)} 1/(dk) ... for d*k = q
    #       BUT we need q >= 2, so we exclude q=1 (d=1, k=1).

    # sum_{q=1}^{N} (sum_{d|q} mu(d)*d)/q = sum_{d=1}^{N} mu(d) * sum_{k=1}^{floor(N/d)} 1/k
    #                                      = sum_{d=1}^{N} mu(d) * H(floor(N/d))

    # The q=1 term: (sum_{d|1} mu(d)*d)/1 = mu(1)*1 = 1.
    # So sum_{q=2}^{N} = sum_{q=1}^{N} - 1 = sum mu(d)*H(fl(N/d)) - 1.
    # Therefore E(N) = (1/6)*(sum mu(d)*H(fl(N/d)) - 1).

    # Check: S = sum M(fl(N/m))/m = sum mu(k)*H(fl(N/k)).
    # And E(N) = (1/6)*(S - 1).
    # From above: S = 1 + 6E(N). So E(N) = (1/6)*(1 + 6E(N) - 1) = E(N). Consistent!

    # Now: T(N) = S - M(N) = S + 2 (since M(N) = -2).
    # S = 1 + 6E(N).
    # T(N) = 3 + 6E(N). Confirmed.
    # T(N) < 0 iff E(N) < -1/2.

    # E(N) = (1/6)*(S - 1) = (1/6)*(sum mu(d)*H(fl(N/d)) - 1).

    print("\n=== Now the key bound ===")
    print("We need E(N) < -1/2 for all N >= 42 with M(N) = -2.")
    print("Equivalently: sum mu(d)*H(floor(N/d)) < -2.")
    print()

    # From the formula: E(N) = R(N) - 1/6 where R(N) = 1/3 + E(N)...
    # Wait, R(N) = 1/3 + E(N), and 6R(N) = 2 + 6E(N) = S + 1. OK.

    # The approach: use the Dirichlet series connection.
    # S = sum_{m=1}^{N} M(fl(N/m))/m.
    # For M(N) = -2: the m=1 term is -2, the m=2 term is M(fl(N/2))/2, etc.
    # T(N) = S + 2 = sum_{m=2}^{N} M(fl(N/m))/m + (-2) + 2 = sum_{m>=2} M(fl)/m.
    # Wait no: T(N) = sum_{m>=2} M(fl(N/m))/m. And S = -2 + T(N).
    # T(N) < 0 iff S < -2 iff sum mu(d)*H < -2.

    # Hmm, but S = -2 + T(N), and we need T(N) < 0, so S < -2.
    # And S = sum mu(d)*H(fl(N/d)).
    # With H(x) = ln x + gamma + O(1/x):
    #   S ≈ sum mu(d)*(ln(N/d) + gamma) = (ln N + gamma)*M(N) - sum mu(d)*ln(d)
    #     = -2*(ln N + gamma) - sum mu(d)*ln(d)

    # The sum -sum mu(d)*ln(d) is related to the PNT: sum_{d<=x} mu(d)*ln(d) = -x + error.
    # So -sum mu(d)*ln(d) ≈ N.
    # And S ≈ -2*ln(N) - 2*gamma + N.
    # For N = 42: -2*ln(42) - 2*0.577 + 42 ≈ -7.47 - 1.15 + 42 = 33.38.
    # But actual S at N=42 is about -2.895 + (-2) = let me compute...

    # S(42) = sum M(fl(42/m))/m for m=1..42.
    S_42 = sum(M[42 // m] / m for m in range(1, 43))
    print(f"S(42) = {S_42:.6f}")
    print(f"T(42) = S(42) + 2 = {S_42 + 2:.6f}")

    # The PNT-based estimate is wildly off for small N because
    # sum mu(d)*ln(d) = -N + o(N) is only asymptotic.
    # For small N, the sum is much smaller than N.

    # Let me check: -sum mu(d)*ln(d) for d=1..42
    pnt_sum_42 = -sum(mu[d] * log(d) for d in range(1, 43))
    print(f"-sum mu(d)*ln(d) for d=1..42: {pnt_sum_42:.6f} (vs N=42)")

    # DIFFERENT APPROACH: Use the Perron formula interpretation.
    # The key identity: sum_{m=1}^{N} M(fl(N/m))/m = (1/2pi*i) integral (N^s/s) * (1/zeta(s)) * zeta(s+1) ds
    # The residue at s=0: since 1/zeta(0) = 0... wait, zeta(0) = -1/2, so 1/zeta(0) = -2.
    # And zeta(1) has a pole... This needs more careful analysis.

    # BETTER APPROACH: Use the identity from the convolution:
    # sum_{n<=x} M(x/n)/n = sum_{n<=x} 1/n * sum_{d<=x/n} mu(d)
    # = sum_{dn<=x} mu(d)/n = sum_{d<=x} mu(d) * sum_{n<=x/d} 1/n
    # = sum_{d<=x} mu(d) * H(x/d)
    # This is the Dirichlet convolution of mu * (1/n) summed up to x.

    # In Dirichlet series: sum mu(n)/n^s * sum 1/n^s = 1/zeta(s) * zeta(s).
    # Wait, that gives sum (sum_{d|n} mu(d))/n^s = sum [n=1 ? 1 : 0] / n^s = 1.
    # So sum_{n<=x} sum_{d|n} mu(d) = [x] (floor of x) = exactly 1 for x >= 1.
    # This is the well-known Dirichlet identity.

    # But what we have is sum mu(d) * H(x/d), which is the convolution of mu with H.
    # H(n) = sum_{k<=n} 1/k, so in Dirichlet form: generating function of H(n) is
    # sum H(n)/n^s = sum (sum_{k<=n} 1/k)/n^s.

    # Actually the partial sum version: sum_{d<=x} mu(d)*H(x/d) relates to
    # the "1/zeta" sum weighted by harmonic numbers.

    # Let me try the Selberg-Delange method. Actually, the cleanest approach is:

    # CLAIM: For N >= 12 with M(N) = -2, T(N) < 0.
    # PROOF: Split T(N) into small m and large m parts.

    # T(N) = sum_{m=2}^{N} M(fl(N/m))/m
    # The m=2 term: M(fl(N/2))/2.
    # For M(N) = -2: since mu is multiplicative and M(N-1) or M(N-2) may differ...
    # We can't say much about M(fl(N/2)) individually.

    # APPROACH: Use El Marraki bound.
    # |M(x)| <= 0.6438 * x / log(x) for all x > 1.
    #
    # sum_{m=2}^{N} M(fl(N/m))/m
    # = sum_{m=2}^{N} [M(fl(N/m))/fl(N/m)] * [fl(N/m)/m]
    #
    # Now fl(N/m)/m <= N/m^2.
    # |M(fl(N/m))/fl(N/m)| <= 0.6438/log(fl(N/m)) <= 0.6438/log(N/m - 1)
    #
    # This gives: |T(N)| <= sum 0.6438 * N / (m^2 * log(N/m))
    # which is bounded but doesn't help with the SIGN.

    # SIGN ANALYSIS: We need to show the sum is negative, not just bounded.
    # The key is the M(N) = -2 constraint.

    # NOTE: From the computation, the MINIMUM |T(N)| among M(N)=-2, N>=42 is at N=42:
    # T(42) = -0.895. Wait, that's from the first script showing T(42) = -2.895.
    # Let me double check...

    T_42 = sum(M[42//m] / m for m in range(2, 43))
    print(f"\nDirect T(42) = {T_42:.6f}")

    T_12 = sum(M[12//m] / m for m in range(2, 13))
    print(f"Direct T(12) = {T_12:.6f}")

    # The m=2 to m=6 terms at N=42:
    print("\nN=42 details:")
    for m in range(2, 7):
        v = 42 // m
        print(f"  m={m}: fl(42/{m})={v}, M({v})={M[v]}, contrib={M[v]/m:.4f}")

    # All contributions from m=2..6 are negative because M(v) <= -1 for all v = fl(42/m).
    # This is because M(N) = -2 and M is "sticky" near its value.

    # THE REAL APPROACH: Use the convolution identity with Ramanujan's formula.
    # sum_{k<=N} mu(k) * H(N/k) can be related to sum_{k<=N} mu(k)/k by partial summation.
    #
    # Alternatively, use the identity:
    # sum_{m=1}^{N} M(N/m)/m = sum_{n=1}^{N} 1/n * sum_{d|n} mu(d) ... no, that's different.

    # Actually the cleanest route: use the EXPLICIT FORMULA.
    # The Perron formula gives:
    #   sum_{m=1}^{N} M(fl(N/m))/m = integral_{2-iT}^{2+iT} N^s/(s*zeta(s)) * zeta(s+1) ds + error
    #
    # The integrand has:
    # - A pole at s=0 from 1/s, with residue (1/zeta(0))*zeta(1)... but zeta(1) diverges.
    # - Actually zeta(s+1) has a pole at s=0 with residue 1.
    # - And 1/zeta(0) = 1/(-1/2) = -2.
    # - So the residue of N^s/(s*zeta(s)) * zeta(s+1) at s=0 is lim_{s->0} N^s/zeta(s) * res(zeta(s+1),0)
    #   = 1/zeta(0) * 1 = -2.
    #
    # Wait, let me be more careful. zeta(s+1) near s=0: zeta(s+1) = 1/s + gamma + O(s).
    # So the integrand near s=0: (N^s/s) * (1/zeta(s)) * (1/s + gamma + ...)
    #   = N^s/(s^2 * zeta(s)) + gamma * N^s/(s * zeta(s)) + ...
    #
    # The pole at s=0 is order 2 (from 1/s^2).
    # zeta(s) near 0: zeta(0) = -1/2, zeta'(0) = -(1/2)*ln(2*pi).
    # 1/zeta(s) near 0: 1/zeta(0) + (1/zeta(0))' * s + ... = -2 + ...
    # N^s = 1 + s*ln(N) + ...
    #
    # So N^s/(s^2*zeta(s)) ≈ (1 + s*ln(N))/(s^2 * (-1/2 + ...)) = -2/s^2 + (-2*ln(N) + ...)/s + ...
    # Residue = coefficient of 1/s = -2*ln(N) + (derivative terms).

    # This is getting complicated. Let me try a cleaner approach.

    # CLEANEST APPROACH: Direct bound using the M(N)=-2 structure.
    #
    # Write F(N) = sum_{m=1}^{N} M(fl(N/m))/m. We know F(N) = 1 + 6*E(N) = 6R(N) - 1.
    # We need F(N) < -2, i.e., 6R(N) < -1.
    #
    # From CORRECTION_NEGATIVITY_PROOF: R(N) = 1/6 + (1/6)*F(N).
    # 6R(N) = 1 + F(N). Need F(N) < -2.
    #
    # F(N) = M(N) + T(N) = -2 + T(N). Need -2 + T(N) < -2, i.e., T(N) < 0.

    # Let me try a different approach entirely. Compute S(N) = sum_{m=1}^{N} M(fl(N/m))/m
    # using the hyperbolic method efficiently for larger N, and track which N with M(N)=-2
    # give the largest values.

    # The approach that will WORK for the proof:
    # 1. Verify T(N) < 0 computationally for all N <= N_0 with M(N) = -2.
    # 2. For N > N_0, use an analytical bound.

    # For step 2, the key bound:
    # T(N) = sum_{m=2}^{N} M(fl(N/m))/m
    #
    # Using El Marraki: |M(x)| <= c_0 * x / log(x) where c_0 = 0.6438 for all x > 1.
    # This means each term |M(fl(N/m))/m| <= c_0 * fl(N/m) / (m * log(fl(N/m))).
    # But this bounds |T(N)|, not T(N) itself. We need to show T(N) < 0.

    # The constraint M(N) = -2 is KEY. It means sum_{k=1}^{N} mu(k) = -2.
    # The m=1 term of F(N) is M(N) = -2. All other terms contribute T(N).
    #
    # If we could show that T(N) = O(1) or T(N) = o(log N), then for large N,
    # the m=1 term -2 would dominate and F(N) < 0. But actually T(N) grows like log(N)!
    # The whole point is that F(N) = -2 + T(N) and we need T(N) < 0.
    # T(N) is NOT bounded by 2 -- in fact it goes to -infinity!

    # So the proof structure should be:
    # T(N) < 0 for all N >= 12 with M(N) = -2.

    # Hmm, but T(N) = sum_{m>=2} M(fl(N/m))/m. Each M(fl(N/m)) value depends on N.
    # When M(N) = -2, the values M(fl(N/m)) for m >= 2 tend to also be negative
    # (because M is "smooth" in some sense -- if M(N) = -2, M values near N tend to
    # also be around -2 to -3).

    # PROOF STRATEGY: Use the CONVOLUTION structure.
    # T(N) = sum_{m=2}^{N} M(fl(N/m))/m = sum_{j=1}^{fl(N/2)} (1/j) * [some mu sums]
    # After hyperbolic swap: T(N) + M(N) = sum_{k=1}^{N} mu(k) * H(fl(N/k))
    # So T(N) = sum mu(k) * H(fl(N/k)) + 2.

    # Split: T(N) = mu(1)*H(N) + sum_{k=2}^{N} mu(k)*H(fl(N/k)) + 2
    #       = H(N) + sum_{k=2}^{N} mu(k)*H(fl(N/k)) + 2

    # We need this < 0, i.e., sum_{k=2}^{N} mu(k)*H(fl(N/k)) < -2 - H(N).
    # But H(N) ~ ln(N) + gamma. So we need the sum to be < -(ln N + gamma + 2).

    # This sum involves both positive and negative mu values.
    # For k prime: mu(k) = -1, contributing -H(fl(N/k)).
    # For k semiprime (squarefree): mu(k) = +1, contributing +H(fl(N/k)).
    # For k with squared factors: mu(k) = 0, no contribution.

    # So T(N) = H(N) + 2 - sum_{p<=N} H(fl(N/p)) + sum_{pq<=N, p<q} H(fl(N/pq)) - ...

    # The dominant negative term is -sum_{p<=N} H(fl(N/p)).
    # H(fl(N/p)) ≈ ln(N/p) + gamma ≈ ln(N) - ln(p) + gamma.
    # sum_{p<=N} H(fl(N/p)) ≈ pi(N)*(ln N + gamma) - sum_{p<=N} ln(p).
    # By PNT: sum_{p<=N} ln(p) = theta(N) ~ N (Chebyshev).
    # So sum H(fl(N/p)) ≈ pi(N)*(ln N + gamma) - N.

    # Then T(N) ≈ ln(N) + gamma + 2 - pi(N)*(ln N + gamma) + N + [composite terms]
    #           = (1 - pi(N))*(ln N + gamma) + N + 2 + [composite terms]

    # For N >= 42: pi(N) >= 13, ln(42)+gamma ≈ 4.31, so (1-13)*4.31 = -51.7.
    # And N = 42, plus composite terms. The estimate gives T ≈ -51.7 + 42 + 2 + composite ≈ -7.7 + composite.
    # Composites contribute positively, but less than the -7.7 gap.

    # This is getting messy. Let me try a cleaner analytical bound.

    # Use Chebyshev-type bounds directly on the sum.
    # Key reference: the identity sum_{n<=x} M(x/n)/n = sum mu(k)*H(x/k)
    # relates to the "smooth sum" of M.

    # EFFECTIVE APPROACH: Prove that for N >= N_0, the sum is controlled by
    # the leading-order terms which are negative.

    # For the PROOF document, I'll use:
    # 1. Computational verification for N <= 200000
    # 2. Analytical argument using Chebyshev theta function for N > 200000

    print("\n=== Data for the proof ===")
    print("All N >= 10 with M(N) = -2, and their T(N) values (worst 20):")

    results = []
    for N in range(10, LIMIT + 1):
        if M[N] == -2:
            T = sum(M[N//m] / m for m in range(2, N+1)) if N <= 5000 else None
            if N <= 5000:
                results.append((T, N))

    results.sort(reverse=True)
    for T, N in results[:20]:
        print(f"  N={N:>6}: T(N) = {T:.6f}")

    print(f"\n  Total N with M(N)=-2 and N in [10, 5000]: {len(results)}")
    print(f"  All T(N) < 0: {all(T < 0 for T, N in results)}")
    print(f"  Max T(N): {results[0][0]:.6f} at N={results[0][1]}")

if __name__ == '__main__':
    main()
