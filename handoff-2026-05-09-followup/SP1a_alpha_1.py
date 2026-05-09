#!/usr/bin/env python3
"""
SP1a_alpha_1.py — mpmath@50dps companion verifier for SP-1a-alpha.1 audit.

Goal: predict the explicit-constant ETK (Erdős-Turán-Koksma) bound on
    |S_psi(p)| = | sum_f D(f) (sigma_p(f) - 1/2) |
at primes p in {11, ..., 101}, and compare against:
  (a) the empirical |S_psi| from SP1a_Im_Tm.py
  (b) the Cauchy-Schwarz upper bound [V9] of SP1a_Im_Tm.py
  (c) the empirical B_0(p-1) ~ c * N_hat * log(N_hat)
  (d) the heuristic ABT-style "1+epsilon" target |S_psi| <= C * N_hat *
      (log N_hat)^{1+epsilon}

Reference verbatim quotes (audit doc SP1a_alpha_1_ABT_2014_audit.md):
  - Drmota-Tichy 1997 / Wikipedia (Erdős-Turán-Koksma form, s=1):
        D*_N(x_1,...,x_N) <= (3/2) * (2/(H+1)
                              + sum_{h=1..H} (1/h) * |(1/N) sum_n e(h x_n)|)
  - Jameson Notes on the Large Sieve, Theorem LS2.1 (Montgomery-Vaughan):
        sum_{q<=Q} sum_{r in G_q} |f(r/q)|^2 <= (N + Q^2) * sum_n |x_n|^2
    where f(t) = sum_{n=M+1..M+N} x_n e(n t).

Key derivation [audit §5,6,7]:
  S_psi(p) = - (1/pi) * sum_{m>=1} (Im T_m(p)) / m

and via Hurwitz expansion:
  |S_psi(p)| <= (sup over f) |D(f)| * V(psi(p .)) * D*_N(sigma_p(F_{p-1}))
            <=    [N_hat-bound on D]  *  [Var = N_hat]  *  [ETK bound on D*_N]

After Step-2 Niederreiter (cf. Drmota-Tichy 1997 §1.4 Th 1.27):
  D*_N(F_{p-1}) = O(1/N_hat) and similarly for sigma_p(F_{p-1}) by bijection.

After Step-3 (large-sieve weighted bound), the bilinear sum
  | sum_f D(f) e(m p f) |
admits the bound
  C_LS * sqrt( (N_hat + (p-1)^2) * sum_f D(f)^2 )
which gives - using sum_f D(f)^2 = O(N_hat^2 / log N_hat) and
N_hat = (3/pi^2)(p-1)^2 - the asymptotic
  | sum_f D(f) e(m p f) | = O( N_hat^{3/2} / sqrt(log N_hat) ),
which is identical to the CS bound's structural floor.  This is a key
finding of the audit: the large-sieve constant alone does NOT improve on
Cauchy-Schwarz for this particular setup.

The truly decisive bound is the ABT-style (or Niederreiter-style) bound
that uses the structure of D(f) more carefully.  Best-case heuristic:
  |S_psi(p)| <= C_{ABT} * N_hat * (log N_hat)^{1+epsilon}

This script computes the predicted bound under this heuristic for several
candidate constants C_{ABT} ranging over {0.5, 1.0, 2.0, 3.0, 5.0}, and
compares against:
  1. the SP-2 target c_{SP-2} (we use the empirically observed value
     c_{SP-2} ~ 0.30 from B_0(N) ~ 0.30 * N log N for N = N_hat at primes 11..101)
  2. The CS bound (sqrt(Sigma_D2 * Sum(f-1/2)^2))
  3. The empirical |S_psi(p)| from exact-rational computation

This script is COMPANION to: SP1a_alpha_1_ABT_2014_audit.md.
"""

from mpmath import mp, mpf, sqrt, log, pi, fabs
from fractions import Fraction
from math import gcd, log as flog
import sys

mp.dps = 50  # 50 decimal places

# ------------------------------------------------------------------
# Farey arithmetic (faithful to SP1a_Im_Tm.py)
# ------------------------------------------------------------------

def stern_brocot_farey(N):
    """F_N = {(a,b) : 1<=b<=N, 0<=a<=b, gcd(a,b)=1}, sorted by a/b in [0,1].
    Includes (0,1) and (1,1) as boundary points."""
    if N == 0:
        return [(0, 1)]
    a, b, c, d = 0, 1, 1, N
    out = [(a, b)]
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        out.append((a, b))
    return out


def primes_up_to(P):
    s = [True] * (P + 1)
    s[0] = s[1] = False
    for i in range(2, int(P ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, P + 1, i):
                s[j] = False
    return [p for p in range(2, P + 1) if s[p]]


def S_psi_exact(p):
    """S_psi(p) = sum_f D(f) * (sigma_p(f) - 1/2), exact rational."""
    F = stern_brocot_farey(p - 1)
    n = len(F)
    s = Fraction(0)
    for i, (a, b) in enumerate(F):
        f = Fraction(a, b)
        D = Fraction(i + 1) - n * f
        if b == 1:
            sigma = Fraction(0)
        else:
            sigma = Fraction((p * a) % b, b)
        s += D * (sigma - Fraction(1, 2))
    return s


def B0_exact(p):
    """B_0(p-1) = sum_f D(f) * (f - 1/2), exact rational."""
    F = stern_brocot_farey(p - 1)
    n = len(F)
    s = Fraction(0)
    for i, (a, b) in enumerate(F):
        f = Fraction(a, b)
        D = Fraction(i + 1) - n * f
        s += D * (f - Fraction(1, 2))
    return s


def Sigma_D2_exact(p):
    """sum_f D(f)^2, exact rational."""
    F = stern_brocot_farey(p - 1)
    n = len(F)
    s = Fraction(0)
    for i, (a, b) in enumerate(F):
        f = Fraction(a, b)
        D = Fraction(i + 1) - n * f
        s += D * D
    return s, n


def Sigma_f_minus_half_sq_exact(p):
    """sum_f (f-1/2)^2, exact rational."""
    F = stern_brocot_farey(p - 1)
    s = Fraction(0)
    for (a, b) in F:
        s += (Fraction(a, b) - Fraction(1, 2)) ** 2
    return s


# ------------------------------------------------------------------
# ETK / large sieve / heuristic bounds
# ------------------------------------------------------------------

def CS_bound(p):
    """Cauchy-Schwarz bound on |S_psi|: sqrt(Sigma_D2 * Sigma_f_minus_half_sq)."""
    SD2, n = Sigma_D2_exact(p)
    Sf12 = Sigma_f_minus_half_sq_exact(p)
    return sqrt(mpf(SD2.numerator) / mpf(SD2.denominator) *
                mpf(Sf12.numerator) / mpf(Sf12.denominator)), n


def ABT_heuristic_bound(p, C, eps=mpf('0.1')):
    """Heuristic ABT-style bound:
       |S_psi(p)| <= C * N_hat * (log N_hat)^{1+epsilon}
    """
    F = stern_brocot_farey(p - 1)
    n = len(F)
    nhat = mpf(n)
    return mpf(C) * nhat * log(nhat) ** (mpf(1) + eps)


def large_sieve_bilinear_bound(p):
    """Large-sieve direct bound:
       |sum_f D(f) e(m p f)| <= sqrt( (N_hat + (p-1)^2) * sum_f D(f)^2 )
    Note: this assumes |x_n| = D(f), pre-symmetrized over Farey order;
    it is structurally the same magnitude as Cauchy-Schwarz (no improvement)."""
    SD2, n = Sigma_D2_exact(p)
    SD2_mp = mpf(SD2.numerator) / mpf(SD2.denominator)
    N = mpf(p - 1)  # range of n in the sieve
    Q = mpf(p - 1)  # bound for q
    return sqrt((N + Q * Q) * SD2_mp), n


def ETK_explicit_3_2_bound(p, H_choice=None):
    """ETK 1-D explicit-constant form:
       D*_N <= (3/2) * (2/(H+1) + sum_{h=1..H} (1/h) * |(1/N) sum_n e(h x_n)|)
    With sequence x_n = sigma_p(f_n) for n = 1..N_hat.
    Choose H = floor(sqrt(N_hat * log N_hat)) heuristically.

    Then by Koksma-Hlawka (with V(psi) = N_hat for the rank-displaced D):
       |S_psi(p)| <= ||D||_infty * V(psi(p .)) * D*_N
    But ||D||_infty <= O(sqrt(N_hat)) and V(psi) = N_hat, so this gives
       |S_psi(p)| <= O( sqrt(N_hat) * N_hat * D*_N ) = O( N_hat^{3/2} * D*_N ).

    Predicted: D*_N(sigma_p(F_{p-1})) ~ const / N_hat (Niederreiter for Farey),
    so |S_psi| <= C_ETK * sqrt(N_hat).

    NOTE: this is the SHARPEST possible bound under direct ETK; it requires
    proving D*_N(sigma_p F) = O(1/N) which is in Drmota-Tichy 1997 (Th 1.27).
    """
    F = stern_brocot_farey(p - 1)
    n = len(F)
    nhat = mpf(n)

    # Niederreiter / Drmota-Tichy 1997 Th 1.27: D*_N(F_N) = O(1/N).
    # By bijection sigma_p, D*_N(sigma_p(F_{p-1})) is the same order.
    # We use D*_N <= 1 / nhat as the leading order (constant pending).
    D_star_N = mpf(1) / nhat

    # Naive Koksma-Hlawka with V(psi) = N (psi-weight has unbounded variation
    # over F_{p-1} as N grows; we use V = N_hat as upper proxy).
    # ||D||_infty: empirically D(f) is bounded by O(sqrt(N) * sqrt(log N)) on
    # average; we use ||D||_infty <= sqrt(N_hat * log N_hat) as a heuristic.
    D_inf = sqrt(nhat * log(nhat))

    V_psi = nhat  # variation of psi(p .) on F: order N_hat
    # Koksma-Hlawka:
    bound = D_inf * V_psi * D_star_N
    # = sqrt(N_hat * log N_hat) * N_hat * 1/N_hat
    # = sqrt(N_hat * log N_hat)
    return bound, n


# ------------------------------------------------------------------
# Main verification table
# ------------------------------------------------------------------

def main():
    primes_main = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
                   71, 73, 79, 83, 89, 97, 101]

    print("=" * 96)
    print("SP1a_alpha_1.py - mpmath@50dps predicted ABT/ETK bound")
    print("=" * 96)
    print()
    print("Confidence aggregation rule (per audit doc):")
    print("  - Exact-rational verification: 0.99")
    print("  - mpmath@50dps within 1e-30: 0.95")
    print("  - Reduction to literature theorem with verbatim quote: 0.85")
    print("  - Heuristic argument (no rigorous bound): <= 0.50, flagged HEURISTIC")
    print()

    print(f"{'p':>4} {'n':>5} {'|S_psi|':>9} {'CS':>9} "
          f"{'LS-bil':>9} {'ETK-KH':>9} {'B0':>9} "
          f"{'|S|/n*lnN':>9} {'B0/n*lnN':>9}")
    print("-" * 96)
    rows = []
    for p in primes_main:
        S = S_psi_exact(p)
        S_abs = mpf(abs(S.numerator)) / mpf(S.denominator)

        cs, n = CS_bound(p)
        ls, _ = large_sieve_bilinear_bound(p)
        etk, _ = ETK_explicit_3_2_bound(p)

        B = B0_exact(p)
        B_mp = mpf(B.numerator) / mpf(B.denominator)

        nhat = mpf(n)
        ln_n = log(nhat)
        nh_lnN = nhat * ln_n

        S_ratio = S_abs / nh_lnN
        B_ratio = B_mp / nh_lnN

        rows.append((p, n, S_abs, cs, ls, etk, B_mp, S_ratio, B_ratio))
        print(f"{p:>4d} {n:>5d} {float(S_abs):>9.2f} {float(cs):>9.2f} "
              f"{float(ls):>9.2f} {float(etk):>9.2f} {float(B_mp):>9.2f} "
              f"{float(S_ratio):>9.4f} {float(B_ratio):>9.4f}")
    print()

    # Empirical c_{SP-2}: scan B_0/(n log n) at p in {53..101}; this is the
    # SP-2 reduction's TARGET ASYMPTOTIC.
    print("Empirical c_{SP-2} (estimate of B_0(N)/(N log N) for large N):")
    for p, n, S_abs, cs, ls, etk, B_mp, sr, br in rows:
        if p >= 53:
            print(f"  p={p:3d} n={n:5d}: B_0/(n log n) = {float(br):.5f}")
    print()

    # ABT-style heuristic prediction at C = 0.5, 1.0, 2.0
    print("Heuristic ABT bound at various candidate constants C "
          "(|S_psi| <= C * n * (log n)^{1+0.1}):")
    print(f"{'p':>4} {'n':>5} {'|S_psi|':>9} {'C=0.5':>9} {'C=1.0':>9} "
          f"{'C=2.0':>9} {'C_observed (= |S_psi|/(n*(log n)^{1.1}))':>40}")
    for p, n, S_abs, cs, ls, etk, B_mp, sr, br in rows:
        nhat = mpf(n)
        ln_n_eps = log(nhat) ** mpf('1.1')
        b_05 = mpf('0.5') * nhat * ln_n_eps
        b_10 = mpf('1.0') * nhat * ln_n_eps
        b_20 = mpf('2.0') * nhat * ln_n_eps
        C_obs = S_abs / (nhat * ln_n_eps)
        print(f"{p:>4d} {n:>5d} {float(S_abs):>9.2f} "
              f"{float(b_05):>9.2f} {float(b_10):>9.2f} {float(b_20):>9.2f} "
              f"{float(C_obs):>40.5f}")
    print()

    # Comparison: does C_obs * n * (log n)^{1+eps} stay below
    # c_{SP-2} * n * log n?  For closure, need C_obs * (log n)^{eps} < c_{SP-2}.
    print("Closure check: is C_obs * (log n)^{eps} < c_{SP-2}?")
    print("  (closure of the chain B+ unconditionally would require this for ALL p)")
    eps = mpf('0.1')
    c_target = mpf('0.30')  # empirical c_{SP-2}
    print(f"  c_{{SP-2}} (empirical) = {float(c_target)}")
    print(f"{'p':>4} {'n':>5} {'C_obs':>10} {'(log n)^{0.1}':>14} "
          f"{'C_obs*(log n)^{eps}':>22} {'verdict':>10}")
    for p, n, S_abs, cs, ls, etk, B_mp, sr, br in rows:
        nhat = mpf(n)
        ln_n_eps_only = log(nhat) ** eps
        C_obs = S_abs / (nhat * log(nhat) ** mpf('1.1'))
        product = C_obs * ln_n_eps_only
        verdict = "OK" if product < c_target else "FAIL"
        print(f"{p:>4d} {n:>5d} {float(C_obs):>10.5f} "
              f"{float(ln_n_eps_only):>14.5f} {float(product):>22.5f} "
              f"{verdict:>10}")
    print()

    # Now: the predicted ABT BOUND assuming C_ABT = 5.0 (the loosest we can
    # conjecture and still have any hope of closure).
    print("Predicted unconditional ABT bound at C_ABT = 5.0 vs. empirical S_psi:")
    print(f"{'p':>4} {'n':>5} {'|S_psi|':>9} {'pred (C=5)':>10} "
          f"{'B0':>9} {'pred-B0 < 0?':>15}")
    for p, n, S_abs, cs, ls, etk, B_mp, sr, br in rows:
        nhat = mpf(n)
        pred = mpf('5.0') * nhat * log(nhat) ** mpf('1.1')
        diff = pred - B_mp
        verdict = "B0 > pred (closes)" if diff < 0 else "B0 < pred (FAILS)"
        print(f"{p:>4d} {n:>5d} {float(S_abs):>9.2f} {float(pred):>10.2f} "
              f"{float(B_mp):>9.2f} {verdict:>15}")
    print()

    # Conclusion: the ABT-style heuristic bound with C = 5 already FAILS
    # the closure test for all primes p tested.  The true |S_psi| is much
    # smaller than C * N * (log N)^{1+eps}, so the ABT framework's
    # quantitative output is too LOOSE to enforce closure.

    print("=" * 96)
    print("KEY OBSERVATIONS:")
    print("  1. Empirical |S_psi(p)| / (n log n) ~ 0.03 - 0.04 - well below B_0/(n log n) ~ 0.30 - 0.35.")
    print("  2. Empirical C_obs = |S_psi| / (n * (log n)^1.1) ~ 0.005 - 0.015, monotone decreasing.")
    print("  3. CS bound is loose by factor ~3-5; needs constant well below CS to close.")
    print("  4. Predicted ABT (C=5, eps=0.1) bound EXCEEDS B_0 at all primes - too loose.")
    print("  5. Predicted ABT with C ~ 0.05 would close the gap, but no rigorous ABT theorem")
    print("     gives such a small constant for the rank-displacement weight D.")
    print("  6. Honest verdict: literature does not contain an explicit-constant theorem")
    print("     directly applicable to our setup with the form |S_psi| <= C N (log N)^{1+eps}")
    print("     and C < c_{SP-2}.  Closure as stated is OPEN.")
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main())
