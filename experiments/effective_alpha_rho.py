#!/usr/bin/env python3
"""
EFFECTIVE ALPHA-RHO ANALYSIS

Goal: Prove alpha + rho > 1 for all primes p >= 43 with M(p) = -3.

Strategy: The unconditional bound is |corr(D_err, delta)| = O(sqrt(log p)).
This was dismissed as "trivial" because it doesn't give decorrelation.
BUT: we don't need decorrelation! We only need |rho| < alpha - 1.

Key relationship:
  rho = 2 * sum(D_err * delta) / C'
      = 2 * corr(D_err, delta) * ||D_err||_2 * ||delta||_2 / C'
      = 2 * corr(D_err, delta) * ||D_err||_2 / ||delta||_2

since C' = ||delta||_2^2 = sum(delta^2).

So: |rho| <= 2 * |corr| * ||D_err||_2 / ||delta||_2

If |corr| = O(sqrt(log p)) and ||D_err||_2 / ||delta||_2 = R(p),
then |rho| <= 2 * C_corr * sqrt(log p) * R(p).

We need: 2 * C_corr * sqrt(log p) * R(p) < alpha(p) - 1 ~ c_1 * log(p) - c_2.

This holds if R(p) grows slower than sqrt(log p).

COMPUTATION: Find R(p) = ||D_err||_2 / ||delta||_2 exactly at all M=-3 primes.

Also: verify Sigma(delta) != 0 for interior fractions and compute the correction.
"""

from fractions import Fraction
from math import gcd, log, sqrt
import sys

def mobius(n):
    if n == 1: return 1
    temp = n
    d = 2
    factors = 0
    while d * d <= temp:
        if temp % d == 0:
            factors += 1
            temp //= d
            if temp % d == 0: return 0
        d += 1
    if temp > 1: factors += 1
    return (-1) ** factors

def mertens(N):
    return sum(mobius(k) for k in range(1, N+1))

def farey_sequence(N):
    """Generate Farey sequence F_N as list of (a, b) with 0/1 <= a/b <= 1."""
    fracs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: Fraction(x[0], x[1]))
    return fracs

def compute_all(p, use_fraction=True):
    """Compute all quantities for prime p using exact or float arithmetic."""
    N = p - 1
    fracs = farey_sequence(N)
    n = len(fracs)  # includes 0/1 and 1/1

    # Interior fractions (denominator >= 2)
    interior = [(a, b) for (a, b) in fracs if b >= 2]
    n_int = len(interior)

    if use_fraction:
        F = Fraction
    else:
        F = lambda a, b=1: a / b if isinstance(a, int) and b != 1 else float(a)

    # Compute delta for each interior fraction
    deltas = {}
    for (a, b) in interior:
        sigma = (p * a) % b
        deltas[(a, b)] = Fraction(a - sigma, b)

    # Compute rank for each fraction in full Farey sequence
    rank_map = {}
    for j, (a, b) in enumerate(fracs):
        rank_map[(a, b)] = j  # 0-indexed

    # D(f) = rank - n*f for all fractions
    D_map = {}
    for (a, b) in fracs:
        f_val = Fraction(a, b)
        D_map[(a, b)] = Fraction(rank_map[(a, b)]) - n * f_val

    # Compute B' and C' over interior fractions
    B_prime = Fraction(0)
    C_prime = Fraction(0)
    for (a, b) in interior:
        d = deltas[(a, b)]
        D_val = D_map[(a, b)]
        B_prime += 2 * D_val * d
        C_prime += d * d

    correction = (C_prime - B_prime) / 2

    # Now compute alpha (regression of D on f over interior fractions)
    # alpha = Cov(D, f) / Var(f) where f = a/b
    # Using interior fractions only

    sum_f = Fraction(0)
    sum_D = Fraction(0)
    sum_f2 = Fraction(0)
    sum_Df = Fraction(0)
    sum_D2 = Fraction(0)

    for (a, b) in interior:
        f_val = Fraction(a, b)
        D_val = D_map[(a, b)]
        sum_f += f_val
        sum_D += D_val
        sum_f2 += f_val * f_val
        sum_Df += D_val * f_val
        sum_D2 += D_val * D_val

    mean_f = sum_f / n_int
    mean_D = sum_D / n_int

    # Cov(D, f) = E[Df] - E[D]E[f]
    cov_Df = sum_Df / n_int - mean_D * mean_f
    var_f = sum_f2 / n_int - mean_f * mean_f
    var_D = sum_D2 / n_int - mean_D * mean_D

    alpha = cov_Df / var_f

    # Compute D_err = D - mean_D - alpha*(f - mean_f)
    sum_Derr2 = Fraction(0)
    sum_Derr_delta = Fraction(0)
    sum_delta = Fraction(0)
    sum_delta2 = Fraction(0)
    sum_f_delta = Fraction(0)

    for (a, b) in interior:
        f_val = Fraction(a, b)
        D_val = D_map[(a, b)]
        d = deltas[(a, b)]

        D_err = D_val - mean_D - alpha * (f_val - mean_f)

        sum_Derr2 += D_err * D_err
        sum_Derr_delta += D_err * d
        sum_delta += d
        sum_delta2 += d * d
        sum_f_delta += f_val * d

    # Verify C' = sum_delta2
    assert C_prime == sum_delta2, f"C' mismatch: {C_prime} vs {sum_delta2}"

    # rho = 2 * sum(D_err * delta) / C'
    rho = 2 * sum_Derr_delta / C_prime

    # ||D_err||_2 and ||delta||_2
    norm_Derr = sum_Derr2  # This is ||D_err||_2^2
    norm_delta = sum_delta2  # This is ||delta||_2^2 = C'

    # Ratio R = ||D_err||_2 / ||delta||_2
    # R^2 = sum_Derr2 / sum_delta2
    R_squared = sum_Derr2 / sum_delta2

    # Correlation
    # corr = sum(D_err * delta) / (||D_err||_2 * ||delta||_2)
    # corr^2 = (sum_Derr_delta)^2 / (sum_Derr2 * sum_delta2)
    corr_sq = (sum_Derr_delta * sum_Derr_delta) / (sum_Derr2 * sum_delta2)

    # Verify: rho = 2 * corr * R (with signs)
    # rho = 2 * sum_Derr_delta / C' = 2 * corr * sqrt(sum_Derr2) / sqrt(sum_delta2)
    # = 2 * corr * R
    # where R = sqrt(sum_Derr2/sum_delta2), and corr has the same sign as sum_Derr_delta

    # Verify B'/C' = alpha + rho identity
    BoverC = B_prime / C_prime
    alpha_plus_rho = alpha + rho

    # Also check: is there a correction from sum(delta) != 0?
    # B'/C' should equal alpha + rho + 2*mean_D * sum_delta / C'
    # (if mean_D != 0 and sum_delta != 0)
    # Wait: D_err = D - mean_D - alpha*(f - mean_f)
    # So D = mean_D + alpha*(f - mean_f) + D_err
    # B' = 2*sum(D*delta) = 2*mean_D*sum_delta + 2*alpha*sum((f-mean_f)*delta) + 2*sum(D_err*delta)
    # = 2*mean_D*sum_delta + 2*alpha*(sum_f_delta - mean_f*sum_delta) + 2*sum_Derr_delta
    #
    # B'/C' = 2*mean_D*sum_delta/C' + 2*alpha*(sum_f_delta - mean_f*sum_delta)/C' + rho

    term_meanD = 2 * mean_D * sum_delta / C_prime
    term_alpha_raw = 2 * alpha * (sum_f_delta - mean_f * sum_delta) / C_prime

    # The "alpha" we defined as Cov(D,f)/Var(f) should make the second term = alpha*something
    # Let's check what sum((f - mean_f) * delta) / (C'/2) equals
    sum_fmeanf_delta = sum_f_delta - mean_f * sum_delta
    alpha_coeff = 2 * sum_fmeanf_delta / C_prime

    # So B'/C' = term_meanD + alpha * alpha_coeff + rho
    # We need alpha_coeff and see if it's 1

    # Convert key quantities to float for display
    alpha_f = float(alpha)
    rho_f = float(rho)
    BoverC_f = float(BoverC)
    R_f = float(R_squared) ** 0.5
    corr_f = float(sum_Derr_delta) / (float(sum_Derr2)**0.5 * float(sum_delta2)**0.5)
    correction_f = float(correction)
    C_prime_f = float(C_prime)
    sum_delta_f = float(sum_delta)
    alpha_coeff_f = float(alpha_coeff)
    term_meanD_f = float(term_meanD)
    mean_D_f = float(mean_D)
    var_D_f = float(var_D)

    return {
        'p': p,
        'N': N,
        'n': n,
        'n_int': n_int,
        'alpha': alpha_f,
        'rho': rho_f,
        'alpha_plus_rho': float(alpha_plus_rho),
        'BoverC': BoverC_f,
        'identity_check': float(alpha_plus_rho - BoverC),
        'R': R_f,
        'corr': corr_f,
        'sum_delta': sum_delta_f,
        'correction_over_C': float(correction / C_prime),
        'C_prime': C_prime_f,
        'alpha_coeff': alpha_coeff_f,
        'term_meanD': term_meanD_f,
        'mean_D': mean_D_f,
        'var_D': var_D_f,
        'norm_Derr2': float(sum_Derr2),
        'norm_delta2': float(sum_delta2),
        'sum_Derr_delta': float(sum_Derr_delta),
        # Exact Fraction values for key identities
        'BoverC_exact': BoverC,
        'alpha_plus_rho_exact': alpha_plus_rho,
        'decomp_check': float(term_meanD + alpha * alpha_coeff + rho - BoverC),
    }

# Find M=-3 primes
def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    d = 5
    while d * d <= n:
        if n % d == 0 or (n + 2) % d == 0: return False
        d += 6
    return True

def find_m3_primes(limit):
    primes = []
    for p in range(2, limit + 1):
        if is_prime(p) and mertens(p) == -3:
            primes.append(p)
    return primes

if __name__ == '__main__':
    limit = 200  # Exact computation feasible up to ~200
    m3_primes = find_m3_primes(limit)
    print(f"M(p) = -3 primes up to {limit}: {m3_primes}")
    print(f"Count: {len(m3_primes)}")
    print()

    # Header
    print(f"{'p':>5} {'alpha':>8} {'rho':>8} {'a+r':>8} {'B/C':>8} {'id_err':>10} "
          f"{'R':>8} {'corr':>10} {'sum_d':>8} {'a_coeff':>8} {'mD_term':>8} {'decomp':>10}")
    print("-" * 130)

    results = []
    for p in m3_primes:
        print(f"Computing p = {p}...", file=sys.stderr)
        r = compute_all(p)
        results.append(r)
        print(f"{r['p']:5d} {r['alpha']:8.4f} {r['rho']:8.4f} {r['alpha_plus_rho']:8.4f} "
              f"{r['BoverC']:8.4f} {r['identity_check']:10.2e} "
              f"{r['R']:8.4f} {r['corr']:10.6f} {r['sum_delta']:8.2f} "
              f"{r['alpha_coeff']:8.4f} {r['term_meanD']:8.4f} {r['decomp_check']:10.2e}")

    print()
    print("=" * 80)
    print("KEY ANALYSIS: Can |corr| = O(sqrt(log p)) bound give |rho| < alpha - 1?")
    print("=" * 80)
    print()
    print(f"{'p':>5} {'alpha':>8} {'|rho|':>8} {'a-1':>8} {'|rho|/(a-1)':>12} "
          f"{'R':>8} {'|corr|':>10} {'2|c|R':>10} {'|rho|':>8} {'match?':>8}")
    print("-" * 110)

    for r in results:
        a = r['alpha']
        rho_abs = abs(r['rho'])
        a_minus_1 = a - 1
        ratio = rho_abs / a_minus_1 if a_minus_1 > 0 else float('inf')
        R = r['R']
        corr_abs = abs(r['corr'])
        two_cR = 2 * corr_abs * R
        print(f"{r['p']:5d} {a:8.4f} {rho_abs:8.4f} {a_minus_1:8.4f} {ratio:12.4f} "
              f"{R:8.4f} {corr_abs:10.6f} {two_cR:10.4f} {rho_abs:8.4f} "
              f"{'YES' if abs(two_cR - rho_abs) < 0.001 else 'NO':>8}")

    print()
    print("=" * 80)
    print("SCALING ANALYSIS: How do R and |corr| scale with p?")
    print("=" * 80)
    print()
    print(f"{'p':>5} {'log(p)':>8} {'sqrt_lp':>8} {'R':>8} {'R/sqrt(lp)':>12} "
          f"{'|corr|':>10} {'|c|/sqrt(lp)':>14} {'|c|*p^0.5':>12}")
    print("-" * 100)

    for r in results:
        lp = log(r['p'])
        slp = sqrt(lp)
        R = r['R']
        corr_abs = abs(r['corr'])
        print(f"{r['p']:5d} {lp:8.4f} {slp:8.4f} {R:8.4f} {R/slp:12.4f} "
              f"{corr_abs:10.6f} {corr_abs/slp:14.6f} {corr_abs*sqrt(r['p']):12.4f}")

    print()
    print("=" * 80)
    print("FULL DECOMPOSITION: B'/C' = mean_D_term + alpha*alpha_coeff + rho")
    print("=" * 80)
    print()
    print(f"{'p':>5} {'B/C':>8} {'mD_term':>8} {'a*a_c':>8} {'rho':>8} {'sum':>8} {'err':>10}")
    print("-" * 70)

    for r in results:
        a_ac = r['alpha'] * r['alpha_coeff']
        total = r['term_meanD'] + a_ac + r['rho']
        err = total - r['BoverC']
        print(f"{r['p']:5d} {r['BoverC']:8.4f} {r['term_meanD']:8.4f} {a_ac:8.4f} "
              f"{r['rho']:8.4f} {total:8.4f} {err:10.2e}")

    print()
    print("NOTE: If alpha_coeff != 1, then the identity B'/C' = alpha + rho needs correction.")
    print("The actual identity is: B'/C' = term_meanD + alpha*alpha_coeff + rho")
    print("where term_meanD = 2*mean_D*sum(delta)/C' and alpha_coeff = 2*sum((f-mean_f)*delta)/C'")
