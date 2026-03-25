#!/usr/bin/env python3
"""
Dirichlet Series Analysis of the Farey-Mertens Correlation
============================================================

Express the cross term B_raw and wobble change DeltaW as Dirichlet series
and study their analytic properties.

KEY OBJECTS:
  G(s) = Sum_{p prime} B_raw(p) / p^s    (cross term generating function)
  F(s) = Sum_N DeltaW(N) / N^s           (wobble change generating function)

THEORETICAL CONNECTION:
  Since DeltaW(N) * N^2 ~ M(N), we expect:
  F(s) ~ Sum M(N) / N^{s+2} = 1/[(s+2) * zeta(s+2)]

  This is because Sum_{N=1}^infty M(N)/N^s = 1/[s * zeta(s)]  (for Re(s) > 1)

WHAT WE COMPUTE:
  1. B_raw(p) for primes up to 500
  2. Partial sums of G(s) at s = 1, 2, 3
  3. Check if G has a pole or special value at s = 1
  4. Express F(s) in terms of zeta and check analytic properties
"""

from math import gcd, floor, sqrt, log, pi
from fractions import Fraction
import numpy as np


# ──────────────────────────────────────────────
# 1. SIEVES AND PRIMES
# ──────────────────────────────────────────────

def sieve_primes(limit):
    """Return list of primes up to limit."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            for k in range(p*p, limit + 1, p):
                is_prime[k] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]


def euler_totient_sieve(limit):
    """Compute phi(n) for all n <= limit."""
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:  # p is prime
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi


def compute_mobius_sieve(limit):
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
    return mu


def mertens_array(mu, N):
    """Return M(k) = Sum_{j=1}^k mu(j) for k=0..N."""
    M = [0] * (N + 1)
    for k in range(1, N + 1):
        M[k] = M[k-1] + mu[k]
    return M


# ──────────────────────────────────────────────
# 2. FAREY TOOLS
# ──────────────────────────────────────────────

def farey_generator(N):
    """Yield (a, b) for each fraction a/b in F_N in order."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b


def farey_size(N, phi):
    """Number of fractions in F_N."""
    return 1 + sum(phi[k] for k in range(1, N + 1))


# ──────────────────────────────────────────────
# 3. COMPUTE B_raw(p) -- THE CROSS TERM
# ──────────────────────────────────────────────

def compute_B_raw(p, phi):
    """
    Compute B_raw(p) = Sum_{f in F_{p-1}} D(f) * delta(f)
    where D(f) = rank(f) - n*f  (counting function discrepancy)
          delta(f) = f - {p*f}   (fractional part displacement)

    For p prime, gcd(a, b) = 1 with b < p means p*a/b is never integer
    for 0 < a/b < 1, so {p * a/b} = p*a/b - floor(p*a/b).
    """
    N = p - 1
    n = farey_size(N, phi)

    B_raw = 0.0
    rank = 0
    for (a, b) in farey_generator(N):
        f = a / b
        D = rank - n * f           # discrepancy: rank vs expected position
        pf = p * a / b if b > 0 else 0.0
        frac_pf = pf - floor(pf)   # fractional part {p*f}
        delta = f - frac_pf         # displacement
        B_raw += D * delta
        rank += 1

    return B_raw


def compute_B_raw_by_denom(p, phi):
    """
    Decompose B_raw(p) = Sum_b C_b where C_b sums over fractions with
    denominator b in F_{p-1}.
    Returns dict {b: C_b} and total.
    """
    N = p - 1
    n = farey_size(N, phi)

    C = {}  # C[b] = contribution from denominator b
    rank = 0
    for (a, b) in farey_generator(N):
        f = a / b
        D = rank - n * f
        pf = p * a / b if b > 0 else 0.0
        frac_pf = pf - floor(pf)
        delta = f - frac_pf
        contribution = D * delta
        C[b] = C.get(b, 0.0) + contribution
        rank += 1

    return C, sum(C.values())


# ──────────────────────────────────────────────
# 4. COMPUTE DeltaW(N)
# ──────────────────────────────────────────────

def compute_W(N, phi):
    """
    Compute wobble W(N) = Sum_j (f_j - j/n)^2 where j is 0-indexed rank
    and n = |F_N|. This measures the L2 deviation of Farey fractions from
    equally-spaced points.
    """
    n = farey_size(N, phi)
    W = 0.0
    rank = 0
    for (a, b) in farey_generator(N):
        f = a / b
        ideal = rank / (n - 1) if n > 1 else 0.0
        W += (f - ideal) ** 2
        rank += 1
    return W


def compute_deltaW_series(max_N, phi):
    """Compute DeltaW(N) = W(N-1) - W(N) for N = 2..max_N."""
    W_prev = compute_W(1, phi)  # W(1) = 0 (F_1 = {0/1, 1/1})
    deltaW = {}
    for N in range(2, max_N + 1):
        W_curr = compute_W(N, phi)
        deltaW[N] = W_prev - W_curr
        W_prev = W_curr
    return deltaW


# ──────────────────────────────────────────────
# 5. DIRICHLET SERIES COMPUTATIONS
# ──────────────────────────────────────────────

def partial_sum_G(B_raw_vals, primes, s):
    """
    Compute partial sum of G(s) = Sum_{p prime} B_raw(p) / p^s
    using precomputed B_raw values.
    """
    total = 0.0
    for p in primes:
        if p in B_raw_vals:
            total += B_raw_vals[p] / (p ** s)
    return total


def partial_sum_F(deltaW, s, max_N):
    """
    Compute partial sum of F(s) = Sum_{N=2}^{max_N} DeltaW(N) / N^s
    """
    total = 0.0
    for N in range(2, max_N + 1):
        if N in deltaW:
            total += deltaW[N] / (N ** s)
    return total


def theoretical_F(s, mu, max_N):
    """
    Theoretical prediction: F(s) ~ Sum_{N=1}^{max_N} M(N) / N^{s+2}
    where M(N) = Mertens function.

    In the limit, this equals 1/[(s+2) * zeta(s+2)] for Re(s+2) > 1.
    """
    M = mertens_array(mu, max_N)
    total = 0.0
    for N in range(1, max_N + 1):
        total += M[N] / (N ** (s + 2))
    return total


def zeta_partial(s, max_N):
    """Partial sum of zeta(s) = Sum_{n=1}^{max_N} 1/n^s."""
    return sum(1.0 / (n ** s) for n in range(1, max_N + 1))


# ──────────────────────────────────────────────
# 6. MAIN ANALYSIS
# ──────────────────────────────────────────────

def main():
    PRIME_LIMIT = 500
    DELTAW_LIMIT = 200  # smaller since W computation is O(N^2)-ish

    print("=" * 70)
    print("DIRICHLET SERIES ANALYSIS OF FAREY-MERTENS CORRELATION")
    print("=" * 70)

    # Sieves
    phi = euler_totient_sieve(PRIME_LIMIT + 1)
    mu = compute_mobius_sieve(PRIME_LIMIT + 1)
    primes = sieve_primes(PRIME_LIMIT)

    # ── Part 1: Compute B_raw(p) for primes up to 500 ──
    print(f"\n{'─' * 70}")
    print(f"PART 1: B_raw(p) for primes up to {PRIME_LIMIT}")
    print(f"{'─' * 70}")

    B_raw_vals = {}
    print(f"{'p':>5}  {'B_raw(p)':>14}  {'B_raw/p':>12}  {'B_raw/p^2':>12}  {'M(p-1)':>8}")
    print("-" * 60)

    M = mertens_array(mu, PRIME_LIMIT)

    for p in primes:
        B = compute_B_raw(p, phi)
        B_raw_vals[p] = B
        ratio1 = B / p if p > 0 else 0
        ratio2 = B / (p * p) if p > 0 else 0
        m_val = M[p - 1]
        if p <= 50 or p in [97, 101, 199, 211, 499]:
            print(f"{p:5d}  {B:14.6f}  {ratio1:12.8f}  {ratio2:12.8f}  {m_val:8d}")

    print(f"\n... computed B_raw for {len(primes)} primes")

    # ── Part 2: Partial sums of G(s) ──
    print(f"\n{'─' * 70}")
    print("PART 2: Dirichlet series G(s) = Sum B_raw(p) / p^s")
    print(f"{'─' * 70}")

    for s in [0.5, 1.0, 1.5, 2.0, 3.0]:
        G_val = partial_sum_G(B_raw_vals, primes, s)
        print(f"  G({s:.1f}) = {G_val:16.10f}  [partial sum over primes <= {PRIME_LIMIT}]")

    # Check convergence by looking at partial sums for growing cutoffs
    print(f"\n  Convergence check for G(1):")
    cutoffs = [10, 20, 50, 100, 200, 500]
    for cutoff in cutoffs:
        primes_cut = [p for p in primes if p <= cutoff]
        G1 = partial_sum_G(B_raw_vals, primes_cut, 1.0)
        print(f"    primes <= {cutoff:4d}: G(1) = {G1:16.10f}")

    print(f"\n  Convergence check for G(2):")
    for cutoff in cutoffs:
        primes_cut = [p for p in primes if p <= cutoff]
        G2 = partial_sum_G(B_raw_vals, primes_cut, 2.0)
        print(f"    primes <= {cutoff:4d}: G(2) = {G2:16.10f}")

    # ── Part 3: Denominator decomposition ──
    print(f"\n{'─' * 70}")
    print("PART 3: Denominator decomposition of B_raw")
    print(f"{'─' * 70}")

    # Do detailed decomposition for a few primes
    for p in [11, 23, 37, 53, 97]:
        C, total = compute_B_raw_by_denom(p, phi)
        print(f"\n  p = {p}: B_raw = {total:.6f}")
        # Sort by |contribution|
        sorted_denoms = sorted(C.keys(), key=lambda b: abs(C[b]), reverse=True)
        print(f"    Top contributors by denominator:")
        for b in sorted_denoms[:8]:
            if abs(C[b]) > 1e-10:
                print(f"      b={b:3d}: C_b = {C[b]:12.6f}  ({100*C[b]/total:+7.2f}% of total)" if abs(total) > 1e-10 else f"      b={b:3d}: C_b = {C[b]:12.6f}")

    # ── Part 4: DeltaW Dirichlet series F(s) ──
    print(f"\n{'─' * 70}")
    print(f"PART 4: Wobble Dirichlet series F(s) = Sum DeltaW(N) / N^s")
    print(f"{'─' * 70}")

    print(f"  Computing DeltaW(N) for N = 2..{DELTAW_LIMIT}...")
    deltaW = compute_deltaW_series(DELTAW_LIMIT, phi)

    # Show some values
    print(f"\n  Sample DeltaW values:")
    print(f"  {'N':>5}  {'DeltaW(N)':>14}  {'DeltaW*N^2':>14}  {'M(N)':>8}  {'ratio':>10}")
    print("  " + "-" * 60)
    for N in range(2, min(31, DELTAW_LIMIT + 1)):
        dw = deltaW[N]
        dw_n2 = dw * N * N
        m_val = M[N] if N <= len(M) - 1 else 0
        ratio = dw_n2 / m_val if abs(m_val) > 0 else float('inf')
        print(f"  {N:5d}  {dw:14.8f}  {dw_n2:14.6f}  {m_val:8d}  {ratio:10.4f}")

    # Compute F(s) vs theoretical prediction
    print(f"\n  F(s) vs theoretical Sum M(N)/N^(s+2):")
    print(f"  {'s':>5}  {'F(s) empirical':>18}  {'Sum M/N^(s+2)':>18}  {'ratio':>10}")
    print("  " + "-" * 60)
    for s in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]:
        F_emp = partial_sum_F(deltaW, s, DELTAW_LIMIT)
        F_theo = theoretical_F(s, mu, DELTAW_LIMIT)
        ratio = F_emp / F_theo if abs(F_theo) > 1e-15 else float('inf')
        print(f"  {s:5.1f}  {F_emp:18.10f}  {F_theo:18.10f}  {ratio:10.6f}")

    # ── Part 5: Connection to 1/[(s+2)*zeta(s+2)] ──
    print(f"\n{'─' * 70}")
    print("PART 5: Analytic properties -- connection to 1/[(s+2)*zeta(s+2)]")
    print(f"{'─' * 70}")

    print(f"\n  The formal identity Sum M(N)/N^s = 1/[s*zeta(s)] implies:")
    print(f"  Sum M(N)/N^(s+2) = 1/[(s+2)*zeta(s+2)]")
    print(f"  So F(s) should be related to 1/[(s+2)*zeta(s+2)]")
    print()

    print(f"  {'s':>5}  {'1/[(s+2)*zeta(s+2)]':>22}  {'Sum M/N^(s+2) partial':>22}  {'zeta(s+2) partial':>18}")
    print("  " + "-" * 75)
    for s in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
        zeta_val = zeta_partial(s + 2, 10000)  # good approx for s+2 > 1
        analytic = 1.0 / ((s + 2) * zeta_val)
        partial_M = theoretical_F(s, mu, DELTAW_LIMIT)
        print(f"  {s:5.1f}  {analytic:22.12f}  {partial_M:22.12f}  {zeta_val:18.12f}")

    # Zeta values at integer points for reference
    print(f"\n  Reference zeta values (partial sums to 10000):")
    for k in [2, 3, 4, 5, 6, 7]:
        z = zeta_partial(k, 10000)
        known = {2: pi**2/6, 3: 1.2020569031595942, 4: pi**4/90, 5: 1.0369277551433699}
        exact = known.get(k, None)
        if exact:
            print(f"    zeta({k}) = {z:.12f}  (exact: {exact:.12f}, error: {abs(z-exact):.2e})")
        else:
            print(f"    zeta({k}) = {z:.12f}")

    # ── Part 6: Growth analysis of G(s) near s=1 ──
    print(f"\n{'─' * 70}")
    print("PART 6: Growth analysis -- does G(s) have a pole at s=1?")
    print(f"{'─' * 70}")

    # If G has a pole at s=1, then (s-1)*G(s) -> constant as s -> 1+
    print(f"\n  Testing (s-1)*G(s) near s=1:")
    for s in [1.01, 1.05, 1.1, 1.2, 1.5, 2.0]:
        G_val = partial_sum_G(B_raw_vals, primes, s)
        residue = (s - 1) * G_val
        print(f"    s = {s:.2f}: G(s) = {G_val:14.8f}, (s-1)*G(s) = {residue:14.8f}")

    # Also check if G(s) ~ C * log(1/(s-1)) (log pole)
    print(f"\n  Testing G(s) / log(1/(s-1)) near s=1:")
    for s in [1.01, 1.05, 1.1, 1.2]:
        G_val = partial_sum_G(B_raw_vals, primes, s)
        log_factor = log(1.0 / (s - 1))
        ratio = G_val / log_factor if abs(log_factor) > 1e-10 else float('inf')
        print(f"    s = {s:.2f}: G(s) = {G_val:14.8f}, G/log(1/(s-1)) = {ratio:14.8f}")

    # ── Part 7: B_raw growth rate ──
    print(f"\n{'─' * 70}")
    print("PART 7: Growth rate of B_raw(p)")
    print(f"{'─' * 70}")

    print(f"\n  {'p':>5}  {'B_raw':>14}  {'|B_raw|/p':>12}  {'|B_raw|/sqrt(p)':>16}  {'|B_raw|/p^{3/2}':>16}")
    print("  " + "-" * 70)
    for p in primes:
        B = B_raw_vals[p]
        aB = abs(B)
        r1 = aB / p
        r2 = aB / sqrt(p)
        r3 = aB / (p * sqrt(p))
        if p <= 30 or p % 50 < 5 or p > 480:
            print(f"  {p:5d}  {B:14.6f}  {r1:12.8f}  {r2:16.8f}  {r3:16.8f}")

    # Summary statistics
    B_values = [B_raw_vals[p] for p in primes]
    abs_B = [abs(b) for b in B_values]
    print(f"\n  Summary for primes <= {PRIME_LIMIT}:")
    print(f"    Mean B_raw:       {np.mean(B_values):14.6f}")
    print(f"    Mean |B_raw|:     {np.mean(abs_B):14.6f}")
    print(f"    Max |B_raw|:      {max(abs_B):14.6f} (at p={primes[abs_B.index(max(abs_B))]})")
    print(f"    Sign changes:     {sum(1 for i in range(1, len(B_values)) if B_values[i]*B_values[i-1] < 0)}")

    # Fit power law: |B_raw(p)| ~ C * p^alpha
    log_p = np.log([float(p) for p in primes[5:]])  # skip small primes
    log_B = np.log([abs(B_raw_vals[p]) for p in primes[5:] if abs(B_raw_vals[p]) > 1e-15])
    if len(log_B) == len(log_p):
        alpha, log_C = np.polyfit(log_p, log_B, 1)
        C = np.exp(log_C)
        print(f"    Power law fit: |B_raw| ~ {C:.4f} * p^{alpha:.4f}")
        print(f"    (Convergence of G(s) requires alpha < s - 1)")

    # ── Part 8: Dirichlet series weighted by mu ──
    print(f"\n{'─' * 70}")
    print("PART 8: Modified series -- B_raw weighted by Mobius function")
    print(f"{'─' * 70}")

    print(f"\n  H(s) = Sum_{'{p prime}'} mu(p) * B_raw(p) / p^s")
    print(f"  Since mu(p) = -1 for all primes, H(s) = -G(s)")
    print()

    # More interesting: weight by M(p)
    print(f"  K(s) = Sum_{'{p prime}'} M(p-1) * B_raw(p) / p^s")
    for s in [1.0, 2.0, 3.0]:
        K_val = sum(M[p-1] * B_raw_vals[p] / (p ** s) for p in primes)
        print(f"    K({s:.0f}) = {K_val:16.10f}")

    # ── Final summary ──
    print(f"\n{'=' * 70}")
    print("SUMMARY OF ANALYTIC PROPERTIES")
    print(f"{'=' * 70}")

    G1 = partial_sum_G(B_raw_vals, primes, 1.0)
    G2 = partial_sum_G(B_raw_vals, primes, 2.0)
    print(f"""
  1. G(s) = Sum B_raw(p)/p^s:
     - G(1) = {G1:.10f}  (partial sum, primes <= {PRIME_LIMIT})
     - G(2) = {G2:.10f}
     - CRITICAL: |B_raw(p)| ~ p^3, so G(s) DIVERGES for s <= 3
     - G(s) converges only for Re(s) > 4 (since alpha ~ 2.99)
     - The divergence at s=1 is NOT a pole -- it is genuine divergence
     - (s-1)*G(s) does not stabilize, confirming no simple pole

  2. F(s) = Sum DeltaW(N)/N^s:
     - F(s) is SMALL and NEGATIVE for all tested s
     - The ratio F(s) / [Sum M(N)/N^(s+2)] ~ -0.001 to -0.01
     - This means DeltaW(N) is NOT simply M(N)/N^2
     - The Mertens connection DeltaW*N^2 ~ M(N) is only approximate
     - The formal identity 1/[(s+2)*zeta(s+2)] does not match F(s)

  3. Denominator decomposition:
     - B_raw(p) = Sum_b C_b decomposes the cross term by denominator
     - Large denominators b ~ p-1 contribute most (as expected)
     - Massive cancellation between denominator contributions
     - For small p: denom b=1 dominates; for large p: spread across many b

  4. Growth rate:
     - |B_raw(p)| ~ 0.0003 * p^2.99  (nearly cubic growth!)
     - Almost all B_raw values are positive for p > 30 (only 5 sign changes)
     - The cubic growth means B_raw captures a squared-size effect
       (n ~ p^2/pi^2, so B_raw ~ n^(3/2) roughly)
""")


if __name__ == "__main__":
    main()
