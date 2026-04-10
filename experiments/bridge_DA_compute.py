#!/usr/bin/env python3
"""
Rigorous computation of 1 - D/A and its relationship to M(p).

Computes with EXACT rational arithmetic for small primes,
then extends to larger primes with floating point.

Key outputs:
1. Exact values of 1 - D/A for p = 5,7,11,13,17,19,23,29,31
2. The formula: 1 - D/A = (B + C + n'^2 * DeltaW) / dilution_raw
3. Relationship of each term to M(p)
4. Verification of the bound |1 - D/A| <= c / log(p)
"""

import time
from math import gcd, floor, sqrt, isqrt, pi, log, exp
from fractions import Fraction
from collections import defaultdict
import bisect

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def mobius_sieve(limit):
    smallest_prime = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if smallest_prime[i] == 0:
            for j in range(i, limit + 1, i):
                if smallest_prime[j] == 0:
                    smallest_prime[j] = i
    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        p = smallest_prime[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]
    return mu

def mertens_values(mu, limit):
    M = [0] * (limit + 1)
    running = 0
    for n in range(1, limit + 1):
        running += mu[n]
        M[n] = running
    return M

def farey_generator(N):
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))

# ======================================================================
# EXACT COMPUTATION (rational arithmetic)
# ======================================================================

def exact_decomposition(p, phi_arr):
    """Full exact rational arithmetic computation of all terms."""
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    old_fracs = list(farey_generator(N))
    old_frac_vals = sorted(Fraction(a, b) for a, b in old_fracs)

    # Old D_sq
    old_D_sq = Fraction(0)
    for idx, fv in enumerate(old_frac_vals):
        D = idx - n * fv
        old_D_sq += D * D

    # B (cross term) and C (shift squared)
    B_raw = Fraction(0)  # = sum 2*D*delta
    C_raw = Fraction(0)  # = sum delta^2

    for idx, (a, b) in enumerate(old_fracs):
        fv = Fraction(a, b)
        D = idx - n * fv
        if a == 0 or a == b:
            delta = Fraction(0)
        else:
            sigma = (p * a) % b
            delta = Fraction(a - sigma, b)
        B_raw += 2 * D * delta
        C_raw += delta * delta

    # New fractions: D_new(k/p) = D_old(k/p) + k/p
    new_D_sq = Fraction(0)
    sum_Dold = Fraction(0)
    sum_Dold_sq = Fraction(0)
    sum_kp_Dold = Fraction(0)
    sum_kp_sq = Fraction(0)

    for k in range(1, p):
        target = Fraction(k, p)
        # Binary search for rank in old sequence
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if old_frac_vals[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        D_old = lo - n * target
        D_new = D_old + target  # = D_old + k/p
        new_D_sq += D_new * D_new
        sum_Dold += D_old
        sum_Dold_sq += D_old * D_old
        sum_kp_Dold += target * D_old
        sum_kp_sq += target * target

    # Dilution
    dilution_raw = old_D_sq * Fraction(n_prime**2 - n**2, n**2)

    # D/A ratio
    DA_ratio = new_D_sq / dilution_raw

    # Wobble
    W_old = old_D_sq / Fraction(n * n)
    total_new = old_D_sq + B_raw + C_raw + new_D_sq
    W_new = total_new / Fraction(n_prime * n_prime)
    delta_W = W_old - W_new

    # The exact identity: D/A = 1 - (B + C + n'^2 * dW) / dilut
    correction = (B_raw + C_raw + n_prime**2 * delta_W) / dilution_raw
    one_minus_DA = Fraction(1) - DA_ratio

    # Verify identity
    identity_check = abs(float(one_minus_DA - correction))

    # Sum of D_old(k/p) relates to Mertens
    # D_old(k/p) = #{a/b in F_{p-1} : a/b <= k/p} - n*(k/p)
    # Sum_{k=1}^{p-1} D_old(k/p) should relate to M(p-1)

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'new_D_sq': new_D_sq,
        'B_raw': B_raw,
        'C_raw': C_raw,
        'dilution_raw': dilution_raw,
        'DA_ratio_exact': DA_ratio,
        'DA_ratio_float': float(DA_ratio),
        'one_minus_DA_exact': one_minus_DA,
        'one_minus_DA_float': float(one_minus_DA),
        'correction_exact': correction,
        'W_old': float(W_old),
        'W_new': float(W_new),
        'delta_W': float(delta_W),
        'sum_Dold': float(sum_Dold),
        'sum_Dold_sq': float(sum_Dold_sq),
        'sum_kp_Dold': float(sum_kp_Dold),
        'sum_kp_sq': float(sum_kp_sq),
        'identity_check': identity_check,
    }


def float_decomposition(p, phi_arr):
    """Fast floating-point computation."""
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    old_fracs = list(farey_generator(N))
    frac_values = [a/b for (a,b) in old_fracs]

    old_D_sq = 0.0
    B_raw = 0.0
    C_raw = 0.0

    for idx, (a, b) in enumerate(old_fracs):
        f = a / b
        D = idx - n * f
        old_D_sq += D * D
        if a == 0 or a == b:
            delta = 0.0
        else:
            sigma = (p * a) % b
            delta = (a - sigma) / b
        B_raw += 2 * D * delta
        C_raw += delta * delta

    sum_Dold_sq = 0.0
    sum_kp_Dold = 0.0
    sum_kp_sq = 0.0
    sum_Dold = 0.0

    for k in range(1, p):
        x = k / p
        rank_old = bisect.bisect_left(frac_values, x)
        D_old_x = rank_old - n * x
        sum_Dold_sq += D_old_x ** 2
        sum_kp_Dold += x * D_old_x
        sum_kp_sq += x ** 2
        sum_Dold += D_old_x

    new_D_sq = sum_Dold_sq + 2 * sum_kp_Dold + sum_kp_sq
    dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2
    DA_ratio = new_D_sq / dilution_raw

    W_old = old_D_sq / (n * n)
    total_new_sq = old_D_sq + B_raw + C_raw + new_D_sq
    W_new = total_new_sq / (n_prime * n_prime)
    delta_W = W_old - W_new

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'new_D_sq': new_D_sq,
        'B_raw': B_raw,
        'C_raw': C_raw,
        'dilution_raw': dilution_raw,
        'DA_ratio': DA_ratio,
        'one_minus_DA': 1.0 - DA_ratio,
        'W_old': W_old,
        'W_new': W_new,
        'delta_W': delta_W,
        'sum_Dold': sum_Dold,
        'sum_Dold_sq': sum_Dold_sq,
        'sum_kp_Dold': sum_kp_Dold,
        'sum_kp_sq': sum_kp_sq,
    }


def main():
    LIMIT = 5100
    phi_arr = euler_totient_sieve(LIMIT)
    mu_arr = mobius_sieve(LIMIT)
    M_arr = mertens_values(mu_arr, LIMIT)
    primes = sieve_primes(LIMIT)

    print("=" * 120)
    print("BRIDGE DERIVATION: Exact relationship between 1 - D/A and M(p)")
    print("=" * 120)

    # ===== SECTION 1: Exact rational values =====
    print("\n" + "=" * 120)
    print("SECTION 1: EXACT RATIONAL ARITHMETIC")
    print("=" * 120)
    print(f"\n{'p':>4} {'n':>6} {'M(p)':>5} {'1-D/A (exact)':>22} {'sum_Dold':>14} {'B/dilut':>12} {'C/dilut':>12} {'check':>10}")
    print("-" * 100)

    exact_results = []
    for p in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        r = exact_decomposition(p, phi_arr)
        r['M'] = M_arr[p]
        exact_results.append(r)
        print(f"{p:4d} {r['n']:6d} {r['M']:5d} {r['one_minus_DA_float']:+22.14f} "
              f"{r['sum_Dold']:14.6f} {float(r['B_raw'])/float(r['dilution_raw']):+12.8f} "
              f"{float(r['C_raw'])/float(r['dilution_raw']):12.8f} {r['identity_check']:10.2e}")

    # ===== SECTION 2: Relationship to M(p) =====
    print("\n" + "=" * 120)
    print("SECTION 2: RELATIONSHIP sum_Dold vs M(p)")
    print("=" * 120)
    print("\nKey identity: sum_{k=1}^{p-1} D_old(k/p) = sum_{k} [#{a/b <= k/p in F_{p-1}} - n*k/p]")
    print("This telescopes to: sum_Dold = sum_{j=0}^{n-1} ceil(p*f_j) - (p-1) - n*(p-1)/2")
    print("                  which connects to M(p-1) via the Franel-Landau bridge.\n")

    print(f"{'p':>4} {'M(p)':>5} {'M(p-1)':>7} {'sum_Dold':>14} {'(sum_Dold+n*(p-1)/2)/(p-1)':>28} {'M(p-1)':>7}")
    print("-" * 80)

    for r in exact_results:
        p = r['p']
        n = r['n']
        # The Franel-Landau connection:
        # sum_{k=1}^{p-1} D_old(k/p) relates to sum of fractional parts
        # Let's compute the normalized version
        adj = (r['sum_Dold'] + n * (p-1) / 2) / (p - 1) if p > 2 else 0
        print(f"{p:4d} {r['M']:5d} {M_arr[p-1]:7d} {r['sum_Dold']:14.6f} {adj:28.6f} {M_arr[p-1]:7d}")

    # ===== SECTION 3: Float computation for larger primes =====
    print("\n" + "=" * 120)
    print("SECTION 3: FLOAT COMPUTATION (all primes to 5000)")
    print("=" * 120)

    all_results = []
    for p in primes:
        if p < 5 or p > 5000:
            continue
        r = float_decomposition(p, phi_arr)
        r['M'] = M_arr[p]
        all_results.append(r)

    # ===== SECTION 4: Decompose 1-D/A into meaningful parts =====
    print("\n" + "=" * 120)
    print("SECTION 4: DECOMPOSITION OF 1 - D/A")
    print("=" * 120)
    print("\n1 - D/A = (B + C + n'^2 * dW) / dilut")
    print("       = B/dilut + C/dilut + (n'^2 * dW)/dilut")
    print()
    print(f"{'p':>6} {'M(p)':>5} {'1-D/A':>14} {'B/dilut':>12} {'C/dilut':>12} "
          f"{'n2dW/dilut':>14} {'|1-D/A|*p':>12} {'|1-D/A|*logp':>14}")
    print("-" * 110)

    for r in all_results:
        p = r['p']
        if p <= 50 or p in [97, 199, 499, 997, 1999, 2999, 4999] or abs(r['M']) >= 10:
            Bd = r['B_raw'] / r['dilution_raw']
            Cd = r['C_raw'] / r['dilution_raw']
            nDWd = r['n_prime']**2 * r['delta_W'] / r['dilution_raw']
            omDA = r['one_minus_DA']
            print(f"{p:6d} {r['M']:5d} {omDA:+14.10f} {Bd:+12.8f} {Cd:12.8f} "
                  f"{nDWd:+14.8f} {abs(omDA)*p:12.4f} {abs(omDA)*log(p):14.6f}")

    # ===== SECTION 5: Does |1-D/A| correlate with M(p)? =====
    print("\n" + "=" * 120)
    print("SECTION 5: CORRELATION OF 1-D/A WITH M(p)")
    print("=" * 120)

    # Group by |M(p)|
    from collections import defaultdict
    groups = defaultdict(list)
    for r in all_results:
        groups[abs(r['M'])].append(r)

    print(f"\n{'|M(p)|':>7} {'count':>6} {'mean(1-D/A)':>14} {'std(1-D/A)':>14} "
          f"{'mean |1-D/A|':>14} {'max |1-D/A|':>14}")
    print("-" * 80)

    for absM in sorted(groups.keys()):
        if absM <= 15:
            vals = [r['one_minus_DA'] for r in groups[absM]]
            mean_v = sum(vals) / len(vals)
            absvals = [abs(v) for v in vals]
            mean_abs = sum(absvals) / len(absvals)
            max_abs = max(absvals)
            var_v = sum((v - mean_v)**2 for v in vals) / len(vals) if len(vals) > 1 else 0
            std_v = sqrt(var_v)
            print(f"{absM:7d} {len(vals):6d} {mean_v:+14.8f} {std_v:14.8f} "
                  f"{mean_abs:14.8f} {max_abs:14.8f}")

    # ===== SECTION 6: Direct formula attempts =====
    print("\n" + "=" * 120)
    print("SECTION 6: TESTING FORMULA |1-D/A| ~ c*|M(p)|/(p*log(p))")
    print("=" * 120)

    print(f"\n{'p':>6} {'M(p)':>5} {'1-D/A':>14} {'|M(p)|/(p*logp)':>18} "
          f"{'ratio':>12} {'|M(p)|/p':>12} {'ratio2':>12}")
    print("-" * 100)

    for r in all_results:
        p = r['p']
        if p in [13, 19, 31, 97, 199, 499, 997, 1999, 2999, 4999]:
            Mp = r['M']
            omDA = r['one_minus_DA']
            pred1 = abs(Mp) / (p * log(p)) if p > 1 else 0
            ratio1 = omDA / pred1 if pred1 > 1e-15 else float('inf')
            pred2 = abs(Mp) / p
            ratio2 = omDA / pred2 if pred2 > 1e-15 else float('inf')
            print(f"{p:6d} {Mp:5d} {omDA:+14.10f} {pred1:18.10f} "
                  f"{ratio1:+12.4f} {pred2:12.8f} {ratio2:+12.4f}")

    # ===== SECTION 7: The effective Mertens bound =====
    print("\n" + "=" * 120)
    print("SECTION 7: BOUNDING |1-D/A| USING MERTENS BOUNDS")
    print("=" * 120)
    print("\nEl Marraki (1995): |M(x)| <= 0.571 * x / sqrt(log x)  for x >= 685")
    print("This gives: |M(p)|/p <= 0.571/sqrt(log p)")
    print()
    print("We test whether |1-D/A| <= C * exp(-c' * sqrt(log p)) for some constants.")
    print()

    # Fit: log|1-D/A| vs sqrt(log p) for p >= 100
    import numpy as np
    ps = []
    vals = []
    for r in all_results:
        if r['p'] >= 100 and abs(r['one_minus_DA']) > 1e-15:
            ps.append(r['p'])
            vals.append(abs(r['one_minus_DA']))

    log_vals = [log(v) for v in vals]
    sqrt_logp = [sqrt(log(p)) for p in ps]
    logp = [log(p) for p in ps]

    # Linear regression: log|1-D/A| = a + b*sqrt(log p)
    n_pts = len(ps)
    mean_x = sum(sqrt_logp) / n_pts
    mean_y = sum(log_vals) / n_pts
    cov_xy = sum((x - mean_x)*(y - mean_y) for x,y in zip(sqrt_logp, log_vals)) / n_pts
    var_x = sum((x - mean_x)**2 for x in sqrt_logp) / n_pts
    b_sqrt = cov_xy / var_x if var_x > 0 else 0
    a_sqrt = mean_y - b_sqrt * mean_x

    # Also try: log|1-D/A| = a + b*log(p)  (power law)
    mean_x2 = sum(logp) / n_pts
    cov_xy2 = sum((x - mean_x2)*(y - mean_y) for x,y in zip(logp, log_vals)) / n_pts
    var_x2 = sum((x - mean_x2)**2 for x in logp) / n_pts
    b_log = cov_xy2 / var_x2 if var_x2 > 0 else 0
    a_log = mean_y - b_log * mean_x2

    print(f"Regression: log|1-D/A| = {a_sqrt:.4f} + {b_sqrt:.4f} * sqrt(log p)")
    print(f"   => |1-D/A| ~ {exp(a_sqrt):.4f} * exp({b_sqrt:.4f} * sqrt(log p))")
    print()
    print(f"Alt regression: log|1-D/A| = {a_log:.4f} + {b_log:.4f} * log(p)")
    print(f"   => |1-D/A| ~ {exp(a_log):.4f} * p^{b_log:.4f}")
    print()

    # Compute residuals for both fits
    resid_sqrt = [abs(y - (a_sqrt + b_sqrt*x)) for x,y in zip(sqrt_logp, log_vals)]
    resid_log = [abs(y - (a_log + b_log*x)) for x,y in zip(logp, log_vals)]
    print(f"  sqrt(log p) fit: mean residual = {sum(resid_sqrt)/len(resid_sqrt):.4f}, max = {max(resid_sqrt):.4f}")
    print(f"  log(p) fit:      mean residual = {sum(resid_log)/len(resid_log):.4f}, max = {max(resid_log):.4f}")

    # ===== SECTION 8: Explicit bound verification =====
    print("\n" + "=" * 120)
    print("SECTION 8: EXPLICIT BOUND VERIFICATION")
    print("=" * 120)
    print("\nTest: |1 - D/A| <= C / log(p)  for various C")
    print()

    # Find the tightest C such that |1-D/A| <= C/log(p) for all p >= P0
    for P0 in [11, 47, 100, 500]:
        subset = [r for r in all_results if r['p'] >= P0]
        if subset:
            C_needed = max(abs(r['one_minus_DA']) * log(r['p']) for r in subset)
            print(f"  P0 = {P0:5d}: Need C >= {C_needed:.6f}")

    print()
    print("Test: |1 - D/A| <= C * exp(-c' * sqrt(log p))")
    print()

    # For each (c, c'), check if bound holds
    for c_prime in [0.5, 1.0, 1.5, 2.0]:
        worst = 0
        worst_p = 0
        for r in all_results:
            if r['p'] >= 47:
                bound = exp(-c_prime * sqrt(log(r['p'])))
                ratio = abs(r['one_minus_DA']) / bound if bound > 0 else float('inf')
                if ratio > worst:
                    worst = ratio
                    worst_p = r['p']
        print(f"  c' = {c_prime:.1f}: need c >= {worst:.6f} (worst at p={worst_p})")

    # ===== SECTION 9: The actual formula =====
    print("\n" + "=" * 120)
    print("SECTION 9: EXACT FORMULA FOR 1-D/A")
    print("=" * 120)
    print()
    print("From the identity:")
    print("  1 - D/A = (B + C + n'^2 * DeltaW) / dilution_raw")
    print()
    print("We decompose further. DeltaW = W(p-1) - W(p) = (A - B - C - D)/n'^2")
    print("So n'^2 * DeltaW = A_raw - B - C - D_raw where A_raw = dilution_raw")
    print()
    print("Thus: 1 - D/A = (B + C + dilut - B - C - new_D_sq) / dilut")
    print("             = (dilut - new_D_sq) / dilut")
    print("             = 1 - new_D_sq / dilut")
    print("             = 1 - D/A    (TAUTOLOGY!)")
    print()
    print("The identity is tautological. To get a USEFUL formula, we need to")
    print("express new_D_sq and dilution_raw separately in terms of M(p).")
    print()

    # Express new_D_sq in terms of its components
    print("new_D_sq = sum_{k=1}^{p-1} (D_old(k/p) + k/p)^2")
    print("         = sum D_old(k/p)^2 + 2*sum (k/p)*D_old(k/p) + sum (k/p)^2")
    print()
    print("sum (k/p)^2 = (p-1)(2p-1)/(6p)  [exact]")
    print()
    print("The key: sum D_old(k/p) and sum D_old(k/p)^2 connect to M(p-1).")
    print()

    # ===== SECTION 10: The Franel sum =====
    print("=" * 120)
    print("SECTION 10: THE FRANEL CONNECTION")
    print("=" * 120)
    print()
    print("D_old(k/p) = #{a/b in F_{p-1} : a/b <= k/p} - n*(k/p)")
    print()
    print("sum_{k=1}^{p-1} D_old(k/p) = sum_k #{a/b <= k/p} - n*sum_k (k/p)")
    print("                            = sum_k #{a/b <= k/p} - n*(p-1)/2")
    print()
    print("Now sum_k #{a/b <= k/p} counts, for each old fraction f=a/b,")
    print("the number of k in {1,...,p-1} with k/p >= a/b, i.e., k >= ceil(p*a/b).")
    print("So sum_k #{a/b <= k/p} = sum_{a/b in F_{p-1}} (p - ceil(p*a/b))")
    print("  for a/b < 1, plus contributions from a/b = 1.")
    print()

    # Verify this connection
    print("Verification of sum_Dold formula:")
    print(f"{'p':>4} {'sum_Dold':>14} {'formula':>14} {'diff':>12}")
    print("-" * 50)

    for r in exact_results[:10]:
        p = r['p']
        N = p - 1
        n = r['n']
        # Compute sum_k #{a/b <= k/p} directly
        old_fracs_list = list(farey_generator(N))
        total = 0
        for a, b in old_fracs_list:
            if a == 0:
                total += p - 1  # all k >= 1 satisfy k/p >= 0
            elif a == b:
                total += 0  # k/p >= 1 requires k >= p, none
            else:
                import math
                ceil_pa_b = math.ceil(p * a / b)
                if ceil_pa_b <= p - 1:
                    total += p - 1 - ceil_pa_b + 1
                elif ceil_pa_b == p:
                    # k/p >= a/b requires k >= p*a/b, ceil = p means k=p not in range
                    total += 0
                else:
                    total += 0
        formula_val = total - n * (p - 1) / 2.0
        print(f"{p:4d} {r['sum_Dold']:14.6f} {formula_val:14.6f} {r['sum_Dold']-formula_val:12.2e}")

    # ===== SECTION 11: M(p) connection to sum_Dold =====
    print("\n" + "=" * 120)
    print("SECTION 11: SUM D_OLD vs MERTENS")
    print("=" * 120)
    print()
    print("The Franel-Landau identity: sum |D(j/N)| or sum D(j/N)^2 relates to Mertens.")
    print("Specifically, the FIRST MOMENT: sum_{k=0}^{N} D_{F_N}(k/N) = M(N).")
    print()
    print("But our sum is: sum_{k=1}^{p-1} D_old(k/p), evaluation at different points!")
    print()

    # Compute the standard Franel sum for comparison
    print(f"{'p':>4} {'N':>4} {'M(N)':>5} {'M(p)':>5} {'sum_Dold':>14} {'sum_Dold/p':>12} {'M(N)/p':>10}")
    print("-" * 70)

    for r in exact_results:
        p = r['p']
        N = p - 1
        print(f"{p:4d} {N:4d} {M_arr[N]:5d} {M_arr[p]:5d} {r['sum_Dold']:14.6f} "
              f"{r['sum_Dold']/p:12.6f} {M_arr[N]/p:10.6f}")

    # ===== SECTION 12: Direct bound on 1-D/A =====
    print("\n" + "=" * 120)
    print("SECTION 12: BOUNDING 1-D/A DIRECTLY")
    print("=" * 120)
    print()
    print("Since 1 - D/A = 1 - new_D_sq/dilution_raw,")
    print("and dilution_raw = old_D_sq * (n'^2 - n^2)/n^2,")
    print("we need to bound |dilution_raw - new_D_sq| / dilution_raw.")
    print()
    print("From the four-term decomposition:")
    print("  dilution_raw - new_D_sq = B + C + n'^2 * DeltaW")
    print("                          = B + C - (B + C + new_D_sq - dilution_raw)")
    print("  This is circular. Instead:")
    print()
    print("  dilution_raw - new_D_sq = B_raw + C_raw - (W_new - old_D_sq/n^2 + old_D_sq/n'^2)*n'^2")
    print()
    print("Actually, the non-tautological approach:")
    print("  new_D_sq = sum (D_old(k/p) + k/p)^2 = R1*dilut + R2*dilut + R3*dilut")
    print("  where R1 + R2 + R3 = D/A")
    print()
    print("  R3 = sum(k/p)^2 / dilut = (p-1)(2p-1)/(6p) / dilut  [KNOWN EXACTLY]")
    print("  R2 = 2*sum (k/p)*D_old(k/p) / dilut  [the CROSS term involving Mertens]")
    print("  R1 = sum D_old(k/p)^2 / dilut  [the VARIANCE term]")
    print()
    print("  So 1 - D/A = 1 - R1 - R2 - R3 = (1 - R1 - R3) - R2")
    print()

    # Show R1, R2, R3 for all primes
    print(f"{'p':>6} {'M(p)':>5} {'R1':>12} {'R2':>14} {'R3':>12} {'1-D/A':>14} {'1-R1-R3':>14}")
    print("-" * 100)

    for r in all_results:
        p = r['p']
        if p <= 50 or p in [97, 199, 499, 997, 1999, 2999, 4999]:
            R1 = r['sum_Dold_sq'] / r['dilution_raw']
            R2 = 2 * r['sum_kp_Dold'] / r['dilution_raw']
            R3 = r['sum_kp_sq'] / r['dilution_raw']
            omDA = r['one_minus_DA']
            print(f"{p:6d} {r['M']:5d} {R1:12.8f} {R2:+14.10f} {R3:12.8f} "
                  f"{omDA:+14.10f} {1-R1-R3:+14.10f}")

    # ===== SECTION 13: The KEY: R2 drives 1-D/A =====
    print("\n" + "=" * 120)
    print("SECTION 13: R2 AS THE DRIVER OF 1 - D/A")
    print("=" * 120)
    print()
    print("Observation: 1 - R1 - R3 is SMALL and POSITIVE.")
    print("The SIGN of 1-D/A is determined by whether R2 > or < (1 - R1 - R3).")
    print()
    print("R2 = 2 * sum_{k=1}^{p-1} (k/p) * D_old(k/p) / dilution_raw")
    print()
    print("Since D_old(k/p) ~ -M(p)/p near k ~ p/2 (heuristic), and k/p ~ 1/2,")
    print("we get R2 ~ -M(p)/p * something.")
    print()
    print("More precisely: sum (k/p)*D_old(k/p) is a weighted sum of discrepancies")
    print("with monotone weights k/p. This correlates with M(p-1).")
    print()

    # Verify: does R2 * dilut / p correlate with M(p)?
    print(f"{'p':>6} {'M(p)':>5} {'R2*dilut':>14} {'R2*dilut/p':>14} {'M(p)/p':>12}")
    print("-" * 70)

    for r in all_results:
        p = r['p']
        if p in [13, 19, 31, 97, 199, 499, 997, 1999]:
            R2_raw = 2 * r['sum_kp_Dold']
            print(f"{p:6d} {r['M']:5d} {R2_raw:14.4f} {R2_raw/p:14.6f} {r['M']/p:12.8f}")

    # ===== SECTION 14: Summary table =====
    print("\n" + "=" * 120)
    print("SECTION 14: SUMMARY - EXPLICIT BOUND TABLE")
    print("=" * 120)
    print()

    # For each prime, compute |1-D/A| and various candidate bounds
    print(f"{'p':>6} {'M(p)':>5} {'|1-D/A|':>14} {'0.571/sqrt(logp)':>18} {'2/logp':>12} "
          f"{'1/(logp)^2':>12} {'exp(-sqrt(logp))':>18}")
    print("-" * 100)

    for r in all_results:
        p = r['p']
        if p >= 47 and (p <= 100 or p in [199, 499, 997, 1999, 2999, 4999] or p % 1000 < 5):
            absDA = abs(r['one_minus_DA'])
            b1 = 0.571 / sqrt(log(p))
            b2 = 2.0 / log(p)
            b3 = 1.0 / (log(p))**2
            b4 = exp(-sqrt(log(p)))
            print(f"{p:6d} {r['M']:5d} {absDA:14.10f} {b1:18.10f} {b2:12.8f} "
                  f"{b3:12.8f} {b4:18.10f}")

    print()
    print("CONCLUSION: |1 - D/A| is bounded by a slowly decreasing function.")
    print("The tightest simple bound appears to be |1-D/A| <= C/log(p).")
    print()

    # Final: check if |1-D/A| * log(p) is bounded
    max_product = 0
    argmax_p = 0
    for r in all_results:
        if r['p'] >= 47:
            prod = abs(r['one_minus_DA']) * log(r['p'])
            if prod > max_product:
                max_product = prod
                argmax_p = r['p']
    print(f"max |1-D/A| * log(p) over p >= 47:  {max_product:.8f}  at p = {argmax_p}")

    max_product2 = 0
    argmax_p2 = 0
    for r in all_results:
        if r['p'] >= 47:
            prod = abs(r['one_minus_DA']) * log(r['p'])**2
            if prod > max_product2:
                max_product2 = prod
                argmax_p2 = r['p']
    print(f"max |1-D/A| * log(p)^2 over p >= 47:  {max_product2:.8f}  at p = {argmax_p2}")

    max_product3 = 0
    argmax_p3 = 0
    for r in all_results:
        if r['p'] >= 47:
            prod = abs(r['one_minus_DA']) * sqrt(log(r['p']))
            if prod > max_product3:
                max_product3 = prod
                argmax_p3 = r['p']
    print(f"max |1-D/A| * sqrt(log p) over p >= 47:  {max_product3:.8f}  at p = {argmax_p3}")


if __name__ == '__main__':
    main()
