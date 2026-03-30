#!/usr/bin/env python3
"""
Detailed analysis for the T(N) < 0 proof.

Key identity: T(N) = S_H(N) + 2, where S_H(N) = sum_{k=1}^{N} mu(k) * H(floor(N/k)).

We use the hyperbolic method to write:
  S_H(N) = sum_{m=1}^{N} M(floor(N/m)) / m  [the original form]

Alternative via Dirichlet series: the generating function of M(n)/n is 1/(s*zeta(s)).

Approach: Use the explicit formula
  S_H(N) = sum_{m=1}^{N} M(floor(N/m)) / m

Split at U = floor(sqrt(N)):
  S_H(N) = sum_{m=1}^{U} M(floor(N/m)) / m  +  sum_{m=U+1}^{N} M(floor(N/m)) / m

For the second sum, note floor(N/m) takes values v = 1, 2, ..., floor(N/(U+1)).
For each value v, the range of m is floor(N/(v+1)) < m <= floor(N/v).

So: sum_{m>U} M(v)/m = sum_{v=1}^{V} M(v) * [H(floor(N/v)) - H(floor(N/(v+1)))]
where V = floor(N/(U+1)).

But we need to be more careful. Let's instead use the key decomposition:

  6R(N) = 1 + sum_{m=1}^{N} M(floor(N/m)) / m = 1 + M(N) + T(N)

For M(N) = -2: 6R(N) = -1 + T(N), so T(N) = 6R(N) + 1.

We need T(N) < 0, i.e., 6R(N) < -1, i.e., R(N) < -1/6.

From R_NEGATIVE_PROOF.md, R(N) = 1/3 + (1/6)*sum_{q=2}^{N} e(q) where
e(q) = prod_{p|q}(1-p) / (6q).

So 6R(N) = 2 + sum_{q=2}^{N} e(q) = 2 + sum_{q=2}^{N} prod_{p|q}(1-p) / (6q).

We need 6R(N) < -1, i.e., sum_{q=2}^{N} e(q) < -3.

Now sum_{q=2}^{N} e(q) = sum_{q=2}^{N} prod_{p|q}(1-p) / (6q).

The dominant contribution comes from primes: e(p) = (1-p)/(6p) ~ -1/6.
The sum over primes up to N: sum_{p<=N} e(p) = sum_{p<=N} (1-p)/(6p) = -sum_{p<=N} (p-1)/(6p)
    = -(1/6) * [pi(N) - sum_{p<=N} 1/p].

By Mertens' theorem, sum_{p<=N} 1/p = log log N + M_1 + o(1) where M_1 ~ 0.2615.
By PNT, pi(N) ~ N/log N.

So the prime contribution ~ -(1/6)*[N/log N - log log N] ~ -N/(6 log N).

For N >= 42: N/(6 log N) >= 42/(6*ln(42)) = 42/22.4 = 1.87. Since the prime
contribution alone gives ~ -1.87 and we need the total < -3, we also need the
contribution from composites.

Wait - but for primes ONLY up to N, the sum is:
  sum_{p<=42} (1-p)/(6p) = (1-2)/12 + (1-3)/18 + (1-5)/30 + (1-7)/42 +
                            (1-11)/66 + (1-13)/78 + (1-17)/102 + (1-19)/114 +
                            (1-23)/138 + (1-29)/174 + (1-31)/186 + (1-37)/222 + (1-41)/246

Let me compute this explicitly.
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

def omega(n, primes):
    """Number of distinct prime factors."""
    count = 0
    for p in primes:
        if p * p > n:
            break
        if n % p == 0:
            count += 1
            while n % p == 0:
                n //= p
    if n > 1:
        count += 1
    return count

def e_of_q(q, primes):
    """e(q) = prod_{p|q}(1-p) / (6q)."""
    product = 1
    temp = q
    for p in primes:
        if p * p > temp:
            break
        if temp % p == 0:
            product *= (1 - p)
            while temp % p == 0:
                temp //= p
    if temp > 1:
        product *= (1 - temp)
    return product / (6 * q)

def main():
    LIMIT = 100000
    mu, primes = compute_mobius_sieve(LIMIT)
    primes_set = set(primes)

    # Compute sum e(q) for q=2..N, split by omega
    print("=== Cumulative sum of e(q) for q=2..N ===")
    print(f"{'N':>8} {'sum_e(q)':>12} {'prime_sum':>12} {'semiprime':>12} {'3-factor':>12} {'6R(N)':>10}")

    cum_total = 0.0
    cum_prime = 0.0  # omega=1
    cum_semi = 0.0   # omega=2
    cum_three = 0.0  # omega=3

    for q in range(2, LIMIT + 1):
        eq = e_of_q(q, primes)
        om = omega(q, primes)
        cum_total += eq
        if om == 1:
            cum_prime += eq
        elif om == 2:
            cum_semi += eq
        elif om == 3:
            cum_three += eq

        if q in [10, 20, 42, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]:
            sixR = 2 + cum_total
            print(f"{q:>8} {cum_total:>12.4f} {cum_prime:>12.4f} {cum_semi:>12.4f} {cum_three:>12.4f} {sixR:>10.4f}")

    # Now the key: for M(N) = -2, we need 6R(N) < -1
    # i.e., 2 + sum_{q=2}^{N} e(q) < -1
    # i.e., sum_{q=2}^{N} e(q) < -3

    # Compute sum_{p<=N} (p-1)/(6p) = sum_{p<=N} [1/6 - 1/(6p)]
    print("\n=== Prime contribution: sum_{p<=N} -(p-1)/(6p) ===")
    prime_sum = 0.0
    for i, p in enumerate(primes):
        prime_sum += -(p - 1) / (6 * p)
        if p in [5, 10, 20, 42, 50, 100, 200, 500, 1000, 5000, 10000, 50000]:
            print(f"  sum to p={p}: {prime_sum:.6f}, pi(p)={i+1}, -pi(p)/6={-(i+1)/6:.4f}, diff={prime_sum+(i+1)/6:.6f}")

    # The diff should approach sum 1/(6p) = (1/6)*log(log N) + const
    # So the prime contribution is approximately -pi(N)/6 + (1/6)*log(log N) + const

    # Now compute e(q) for prime powers p^k with k >= 2
    print("\n=== Prime power contribution (k >= 2): sum e(p^k) ===")
    pp_sum = 0.0
    for p in primes:
        pk = p * p
        while pk <= LIMIT:
            pp_sum += (1 - p) / (6 * pk)
            pk *= p
    print(f"  Total prime power (k>=2) contribution up to {LIMIT}: {pp_sum:.6f}")

    # So the omega=1 contribution = prime contribution + prime power contribution
    print(f"  Omega=1 total: {cum_prime:.6f}")
    print(f"  Check: prime + pp = {prime_sum + pp_sum:.6f}")

    # Now for the M(N) = -2 constraint analysis
    print("\n\n=== KEY ANALYSIS: Can sum e(q) >= -3 when M(N) = -2? ===")

    # Compute M(n) for the sieve
    M = [0] * (LIMIT + 1)
    for n in range(1, LIMIT + 1):
        M[n] = M[n-1] + mu[n]

    # For each N with M(N) = -2, compute sum e(q) for q=2..N
    print(f"{'N':>8} {'sum_e':>10} {'6R(N)':>10} {'T(N)':>10} {'prime_contr':>12} {'composite':>10}")

    for N in range(5, min(LIMIT, 1000) + 1):
        if M[N] != -2:
            continue
        se = sum(e_of_q(q, primes) for q in range(2, N + 1))
        sixR = 2 + se
        T = sixR + 1  # T(N) = 6R(N) + 1

        # Prime contribution only
        pc = sum(-(p-1)/(6*p) for p in primes if p <= N)
        composite = se - pc  # approximate; includes prime powers in pc

        if N <= 50 or N in [70, 100, 106, 130, 172, 178, 200, 500, 1000]:
            print(f"{N:>8} {se:>10.4f} {sixR:>10.4f} {T:>10.4f} {pc:>12.4f} {composite:>10.4f}")

    # Analysis: lower bound on |sum e(q)| for q=2..N
    # The prime contribution is -sum_{p<=N} (p-1)/(6p) = -(1/6)*sum_{p<=N} (1 - 1/p)
    # = -(1/6)*[pi(N) - sum_{p<=N} 1/p]
    # By Mertens: sum_{p<=N} 1/p = log(log N) + M_1 + O(1/log N) where M_1 = 0.2615...
    # So prime contribution ~ -(1/6)*[pi(N) - log(log N) - 0.2615]

    # The composite contribution is bounded:
    # For omega=2 (semiprimes pq): e(pq) = (p-1)(q-1)/(6pq) > 0
    # Their sum is bounded above by sum_{pq<=N} 1/6 = pi_2(N)/6 ~ N*log(log N)/(6*log N)
    # For omega=3 (3-almost-primes): e(pqr) < 0
    # Net composite contribution oscillates but is smaller order

    # KEY BOUND: For N >= 42, the prime contribution alone gives:
    #   |prime_contr| = sum_{p<=N} (p-1)/(6p) >= pi(N)/6 - (1/6)*sum 1/p
    # Using Rosser-Schoenfeld: pi(N) >= N/(log N) * (1 + 1/(2 log N)) for N >= 55
    # And sum 1/p <= log(log N) + 0.2615 + 1/(2*log^2 N)

    print("\n=== Rosser-Schoenfeld lower bound on prime contribution ===")
    for N in [42, 50, 100, 200, 500, 1000, 5000, 10000]:
        piN = sum(1 for p in primes if p <= N)
        sum_inv_p = sum(1/p for p in primes if p <= N)
        prime_contr_exact = sum(-(p-1)/(6*p) for p in primes if p <= N)
        rs_bound = -(piN - sum_inv_p) / 6
        print(f"  N={N:>6}: pi(N)={piN:>5}, sum 1/p={sum_inv_p:.4f}, "
              f"prime_contr={prime_contr_exact:.4f}, bound={rs_bound:.4f}")

    # Now the CRUCIAL question: can composites cancel enough primes to make sum > -3?
    # For N with M(N) = -2, the condition means sum mu(k) for k=1..N is -2.
    # This means there are 2 more mu=-1 values than mu=+1 values.
    # But e(q) depends on the PRIME FACTORIZATION of q, not on mu(q) directly.
    # The constraint M(N) = -2 restricts which integers are "present" up to N
    # but doesn't directly control the e(q) sum.

    # Actually, the constraint is just on N itself. e(q) is summed for ALL q from 2 to N.
    # The M(N) = -2 condition means sum_{k=1}^{N} mu(k) = -2, but this doesn't constrain
    # which q values appear in the sum of e(q) -- they all do.

    # So the question is really: for which N >= 42 is sum_{q=2}^{N} e(q) >= -3?
    # And can such N have M(N) = -2?

    print("\n=== All N >= 10 where sum e(q) >= -3 ===")
    cum = 0.0
    for N in range(2, LIMIT + 1):
        cum += e_of_q(N, primes) if N >= 2 else 0
        if N >= 10 and cum >= -3:
            print(f"  N={N}: sum_e = {cum:.6f}, M(N) = {M[N]}")
            if N > 200:
                break

    # Check: what's the FIRST N >= 42 where sum e(q) < -3?
    cum = 0.0
    for N in range(2, LIMIT + 1):
        cum += e_of_q(N, primes)
        if N == 41:
            print(f"\n  sum e(q) at N=41: {cum:.6f}")
        if N == 42:
            print(f"  sum e(q) at N=42: {cum:.6f}")
        if N >= 42 and cum < -3 and N <= 43:
            print(f"  First N >= 42 with sum < -3: N={N}, sum_e={cum:.6f}")

    # IMPORTANT: sum e(q) can be ABOVE -3 even for large N (it oscillates)
    # So we can't just use "prime contribution dominates" for a pure lower bound.
    # The question is whether the oscillation can push sum e(q) above -3
    # AT THE SAME TIME as M(N) = -2.

    # Let's check: among N with M(N) = -2 and N >= 42, what is max(sum e(q))?
    print("\n=== Among N >= 42 with M(N) = -2: max sum e(q) ===")
    cum = 0.0
    max_se_m2 = -float('inf')
    worst_N_m2 = None
    for N in range(2, LIMIT + 1):
        cum += e_of_q(N, primes) if N >= 2 else 0
        if N >= 42 and M[N] == -2:
            if cum > max_se_m2:
                max_se_m2 = cum
                worst_N_m2 = N
    print(f"  Max sum e(q) among M(N)=-2, N>=42: {max_se_m2:.6f} at N={worst_N_m2}")
    print(f"  This gives 6R(N) = {2 + max_se_m2:.6f}, T(N) = {3 + max_se_m2:.6f}")
    if max_se_m2 < -3:
        print(f"  CONFIRMED: sum e(q) < -3 for ALL N >= 42 with M(N) = -2 (up to {LIMIT})")
    else:
        print(f"  WARNING: sum e(q) >= -3 occurs!")

    # Also check without the M(N) = -2 constraint: how high can sum e(q) get?
    cum = 0.0
    max_se_all = -float('inf')
    worst_N_all = None
    for N in range(42, LIMIT + 1):
        cum += e_of_q(N, primes)
        if cum > max_se_all:
            max_se_all = cum
            worst_N_all = N
    print(f"\n  Max sum e(q) for ANY N >= 42: {max_se_all:.6f} at N={worst_N_all}")
    print(f"  Without M(N)=-2 constraint, 6R can be as high as {2+max_se_all:.6f}")

if __name__ == '__main__':
    main()
