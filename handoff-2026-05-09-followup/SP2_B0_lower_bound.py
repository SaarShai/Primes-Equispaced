#!/usr/bin/env python3
"""
SP2_B0_lower_bound.py — exact-rational verification of the closed-form
identity for B0(N), the asymptotic decomposition, and the Mertens-restricted
prime sweep for the lower bound `B0(p-1) >= c*(p-1)`.

Closed form (V13, the new identity in this file, all exact-rational):

  B0(N) = 1/12 - (n_hat / 12) * (1 + Σ_{k=1}^N M(floor(N/k))/k)
                - (n_hat / 2) * ‖δ‖_2^2
        = 1/12 - (n_hat / 12) * (2 + S(N))
                - (n_hat / 2) * ‖δ‖_2^2

where

  n_hat   = |F_N|             (Lean fareySet card)
  M(K)    = Σ_{n≤K} μ(n)      (Mertens function)
  S(N)    = Σ_{b=2}^N h(b)/b  with h(b) := prod_{p|b}(1-p)
  ‖δ‖_2^2 = Σ_v (r_v - v/n_hat)^2   where r_v is the v-th Farey fraction

This is verified at exact-rational precision against the V/X/Q-decomposition
already in `R1_B_plus_proof_attempt.md`.

The sub-problem **SP-2** asked for `B0(N) >= c*N` with explicit c > 0.

VERDICT (see SP2_B0_lower_bound.md): RIGOROUS REDUCTION. The closed form
above reduces SP-2 to a Mertens-function lower bound for the explicit
sum 2 + S(N). Empirically, on all 118 Mertens-restricted primes p ≤ 1637
in R1's sweep, the bound B0(p-1) ≥ 0.43*(p-1) holds, with minimum ratio
≈ 0.4383 at p = 13. The bound `B0(N) >= c*N` for ALL N >= N0 with explicit
c is OPEN -- it follows from any explicit Mertens-function lower bound of
the form 2 + S(N) ≤ -c'*N/n_hat for sufficiently large N.

Companion to: SP2_B0_lower_bound.md
"""
from fractions import Fraction
from math import gcd, log
import sys


def stern_brocot_farey(N: int):
    """F_N = pairs (a,b) with 1<=b<=N, 0<=a<=b, gcd(a,b)=1, sorted ascending in [0,1]."""
    if N == 0:
        return [(0, 1)]
    a, b = 0, 1
    c, d = 1, N
    out = [(a, b)]
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        out.append((a, b))
    return out


def primes_up_to(P):
    sieve = [True] * (P + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(P**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, P + 1, i):
                sieve[j] = False
    return [p for p in range(2, P + 1) if sieve[p]]


def mertens_table(P):
    spf = list(range(P + 1))
    for i in range(2, P + 1):
        if spf[i] == i:
            for j in range(i * i, P + 1, i):
                if spf[j] == j:
                    spf[j] = i
    mu = [0] * (P + 1)
    mu[1] = 1
    for n in range(2, P + 1):
        m = n
        s = 1
        ok = True
        while m > 1:
            q = spf[m]
            cnt = 0
            while m % q == 0:
                m //= q
                cnt += 1
            if cnt >= 2:
                ok = False
                break
            s = -s
        mu[n] = s if ok else 0
    M = [0] * (P + 1)
    for n in range(1, P + 1):
        M[n] = M[n - 1] + mu[n]
    return mu, M


def factorize_primes(n):
    ps = []
    p = 2
    nn = n
    while p * p <= nn:
        if nn % p == 0:
            ps.append(p)
            while nn % p == 0:
                nn //= p
        p += 1
    if nn > 1:
        ps.append(nn)
    return ps


def h_arith(b):
    """h(b) = prod_{p|b}(1 - p). h(1) = 1 (empty product)."""
    if b == 1:
        return 1
    primes = factorize_primes(b)
    r = 1
    for q in primes:
        r *= (1 - q)
    return r


def B0_direct(N):
    """B0(N) = sum D(f) (f - 1/2) directly, exact rational, Lean canonical."""
    F = stern_brocot_farey(N)
    n = len(F)
    s = Fraction(0)
    for i, (a, b) in enumerate(F):
        f = Fraction(a, b)
        D = Fraction(i + 1) - n * f
        s += D * (f - Fraction(1, 2))
    return s, n


def B0_via_VX(N):
    """B0(N) = V - n_hat * X - n_hat / 4. (R1 V10.)"""
    F = stern_brocot_farey(N)
    n = len(F)
    V = Fraction(0); X = Fraction(0)
    for i, (a, b) in enumerate(F):
        f = Fraction(a, b)
        V += (i + 1) * f
        X += f * f
    return V - n * X - Fraction(n, 4), n


def S_function(N, mu_table=None, M_table=None):
    """S(N) := sum_{b=2}^N h(b)/b, exact rational. Equivalently:
    1 + S(N) = sum_{k=1}^N M(floor(N/k))/k  (verified by V11 below).
    """
    s = Fraction(0)
    for b in range(2, N + 1):
        s += Fraction(h_arith(b), b)
    return s


def S_via_Mertens(N, M_table):
    """1 + S(N) = sum_{k=1}^N M(N // k) / k."""
    return sum(Fraction(M_table[N // k], k) for k in range(1, N + 1))


def B0_via_closed_form(N, M_table):
    """B0(N) = 1/12 - n/12 * (1 + (1 + S(N))) - n * ||δ||^2 / 2,
    using 1 + S(N) = sum_{k=1}^N M(N/k)/k."""
    F = stern_brocot_farey(N)
    n = len(F)
    one_plus_S = S_via_Mertens(N, M_table)
    delta_sq = Fraction(0)
    for i, (a, b) in enumerate(F):
        v = i + 1
        delta = Fraction(a, b) - Fraction(v, n)
        delta_sq += delta * delta
    # B0 = 1/12 - n/12 * (1 + (1 + S)) - n * delta_sq / 2
    #     = 1/12 - n/12 * (2 + S(N))   - n * delta_sq / 2
    # Note: 2 + S(N) = 1 + (1 + S(N)).
    return Fraction(1, 12) - n * (Fraction(1) + one_plus_S) / 12 - n * delta_sq / 2, n


# -------- Main verifications --------

def main():
    print("=" * 72)
    print("SP2_B0_lower_bound.py — closed-form B0 identity + Mertens-prime sweep")
    print("=" * 72)
    failures = []

    PMAX = 200  # exact-rational identity verifications up to this N

    # V11: Verify  1 + S(N) = sum_{k=1}^N M(floor(N/k))/k  (Mobius identity)
    print("\n[V11] Identity:  1 + S(N) = sum_{k=1}^N M(floor(N/k))/k")
    pmax_for_table = PMAX + 10
    _, M_table = mertens_table(pmax_for_table)
    fail_v11 = 0
    for N in range(1, PMAX + 1):
        L = Fraction(1) + S_function(N)
        R = S_via_Mertens(N, M_table)
        if L != R:
            fail_v11 += 1
            failures.append(f"V11: 1+S(N) Mobius identity fails at N={N}")
    print(f"  Verified for N in [1, {PMAX}]: {fail_v11} failures.  "
          f"{'OK' if fail_v11 == 0 else 'FAIL'}")

    # V12: Verify the X(N) closed form:
    #   X(N) = 1 + (n_hat - 2)/3 + S(N)/6
    print("\n[V12] X(N) closed form: X(N) = 1 + (n_hat - 2)/3 + S(N)/6")
    fail_v12 = 0
    for N in range(2, PMAX + 1):
        F = stern_brocot_farey(N)
        n = len(F)
        X_direct = sum(Fraction(a, b) ** 2 for (a, b) in F)
        S = S_function(N)
        X_pred = Fraction(1) + Fraction(n - 2, 3) + S / 6
        if X_direct != X_pred:
            fail_v12 += 1
            failures.append(f"V12: X(N) closed form fails at N={N}")
    print(f"  Verified for N in [2, {PMAX}]: {fail_v12} failures.  "
          f"{'OK' if fail_v12 == 0 else 'FAIL'}")

    # V13: Closed form for B0(N) using S(N) and ||delta||^2
    print("\n[V13] Closed form: B0(N) = 1/12 - n_hat * (2 + S(N))/12 - n_hat * ||delta||^2 / 2")
    fail_v13 = 0
    for N in range(2, PMAX + 1):
        B0_a, n_a = B0_direct(N)
        B0_b, n_b = B0_via_closed_form(N, M_table)
        assert n_a == n_b
        if B0_a != B0_b:
            fail_v13 += 1
            failures.append(f"V13: B0 closed form fails at N={N}")
    print(f"  Verified for N in [2, {PMAX}]: {fail_v13} failures.  "
          f"{'OK' if fail_v13 == 0 else 'FAIL'}")

    # V14: Cross-check against V10 (V/X/Q decomposition)
    print("\n[V14] Cross-check B0_direct vs B0_via_VX (R1's V10)")
    fail_v14 = 0
    for N in range(2, PMAX + 1):
        a, _ = B0_direct(N)
        b, _ = B0_via_VX(N)
        if a != b:
            fail_v14 += 1
            failures.append(f"V14: V10 fails at N={N}")
    print(f"  Verified for N in [2, {PMAX}]: {fail_v14} failures.  "
          f"{'OK' if fail_v14 == 0 else 'FAIL'}")

    # Numerical verification table
    print("\n--- B0(N) closed-form decomposition (numerical) ---\n")
    print(f"{'N':>5} {'n_hat':>8} {'B0(N)':>14} {'1/12':>8} {'-n*(2+S)/12':>14} "
          f"{'-n*||δ||²/2':>14} {'B0/N':>10} {'B0/n':>10}")
    Ns = [10, 30, 50, 100, 130, 198, 300]
    for N in Ns:
        F = stern_brocot_farey(N)
        n = len(F)
        S = S_function(N)
        delta_sq = Fraction(0)
        for i, (a, b) in enumerate(F):
            v = i + 1
            delta = Fraction(a, b) - Fraction(v, n)
            delta_sq += delta * delta
        B0v, _ = B0_direct(N)
        term_S = -n * (Fraction(2) + S) / 12
        term_delta = -n * delta_sq / 2
        print(f'{N:>5d} {n:>8d} {float(B0v):>14.4f} {1/12:>8.4f} '
              f'{float(term_S):>14.4f} {float(term_delta):>14.4f} '
              f'{float(B0v)/N:>10.4f} {float(B0v)/n:>10.4f}')

    # Mertens-restricted prime sweep
    print("\n--- Mertens-restricted prime sweep: B0(p-1) > 0? ---\n")
    PRIME_MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    primes = primes_up_to(PRIME_MAX)
    _, M_t = mertens_table(PRIME_MAX)
    positive = 0
    total = 0
    min_ratio = float('inf')
    min_p = 0
    fail_primes = []
    for p in primes:
        if p < 5:
            continue
        Mp = M_t[p]
        if Mp > -3:
            continue
        total += 1
        N = p - 1
        B0v, n = B0_direct(N)
        B0f = float(B0v)
        if B0f > 0:
            positive += 1
            ratio = B0f / N
            if ratio < min_ratio:
                min_ratio = ratio
                min_p = p
        else:
            fail_primes.append((p, Mp, B0f))
    print(f"  Total Mertens-restricted primes p ≤ {PRIME_MAX}: {total}")
    print(f"  With B0(p-1) > 0: {positive}/{total}  "
          f"{'OK' if positive == total else 'FAIL'}")
    if fail_primes:
        print(f"  FAILURES (counterexamples to B+):")
        for p, Mp, B0f in fail_primes:
            print(f"    p={p}, M(p)={Mp}, B0(p-1)={B0f:.6f}")
    else:
        print(f"  Min B0(p-1)/(p-1) over Mertens-restricted primes: "
              f"{min_ratio:.6f} (at p={min_p})")
        print(f"  Empirical lower bound: B0(p-1) >= {min_ratio:.4f} * (p-1)")

    # Final summary
    print("\n" + "=" * 72)
    print(f"VERDICT: {'ALL PASS' if not failures else 'FAILURES'}")
    if failures:
        print("First 5 failures:")
        for f in failures[:5]:
            print(f"  - {f}")
    print("=" * 72)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
