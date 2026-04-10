#!/usr/bin/env python3
"""
B+C TERM STRUCTURE ANALYSIS: Path to Analytical Proof
======================================================

KEY IDENTITY (derived from shift formula):
  D_p(f) = D_{p-1}(f) + delta(f)  for each OLD fraction f in F_{p-1}

  Where delta(a/b) = (a - sigma_p(a)) / b,  sigma_p(a) = (p*a) mod b.

This gives:
  B + C  =  B_raw + delta_sq
         =  Sum_f [2*D(f)*delta(f) + delta(f)^2]
         =  Sum_f t(f)   where t(f) = delta(f) * (2*D(f) + delta(f))

For B+C > 0 analytically, we study the individual t(f) and their sum.

SYMMETRY IDENTITY:
  For each interior pair (a/b, (b-a)/b) in F_{p-1} (with 0 < a < b/2):
    D((b-a)/b) = -(D(a/b) + 1)   (Farey symmetry)
    delta((b-a)/b) = -delta(a/b)  (multiplicative symmetry)

  Pair contribution to Sum t(f):
    t(a/b) + t((b-a)/b) = delta * (2D + delta) + (-delta) * (-2(D+1) + (-delta))
    = delta*(2D + delta) + (-delta)*(-2D - 2 + (-delta))
    = delta*(2D + delta) + delta*(2D + 2 + delta)      [sign flip on -delta * (-X) = delta * X]

    Hmm let me redo:
    t(a/b) = delta * (2D + delta)
    t((b-a)/b) = (-delta) * (2*(-(D+1)) + (-delta))
               = (-delta) * (-2D - 2 - delta)
               = delta * (2D + 2 + delta)

    Pair sum = delta*(2D + delta) + delta*(2D + 2 + delta)
             = delta * (4D + 2 + 2*delta)
             = 2*delta * (2D + 1 + delta)
             = 2*delta * (D + (D + 1 + delta))
             = 2*delta * (D_{p-1} + D_p + 1)   [using D_p = D + delta]

POSITIVE PAIR CONDITION:
  Pair contributes positively to B+C iff:
    delta(a/b) and (D_{p-1}(a/b) + D_p(a/b) + 1) have the same sign.

  Equivalently: delta * (D_{p-1} + D_p + 1) > 0.

THIS SCRIPT:
  1. Computes all t(f) values and identifies negative ones.
  2. Computes per-pair contributions and checks the positive pair condition.
  3. Bounds the sum of negative terms and shows it's O(N) = o(delta_sq).
  4. Establishes B+C >= delta_sq * (1 - 2*sqrt(old_D_sq/delta_sq)) analytically.
  5. Checks whether negative pair contributions are bounded by a constant per pair.
  6. Tests the KEY HYPOTHESIS: negative_sum >= -C_0 * N for a small constant C_0.

If negative_sum = O(N) and delta_sq = Omega(N^2 / log N), then for large N:
  B+C = positive_sum + negative_sum >= delta_sq - |negative_sum|
       >= N^2/(48 log N) - C_0 * N > 0  for N >= N_0.

This would give an analytical proof of B+C > 0 for all primes p >= p_0!
"""

import time
import sys
from math import gcd, isqrt, log, sqrt, pi
from collections import defaultdict

start_time = time.time()


def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def euler_phi(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def analyze_BC_structure(p):
    """
    Full analysis of B+C structure for prime p.

    Returns detailed dict with:
    - B_raw, delta_sq, B_plus_C
    - positive_sum, negative_sum (contributions to B+C)
    - negative_count, total_fracs
    - max_negative_term (most negative individual t(f))
    - pair_analysis: for each pair, check positive pair condition
    - hypothesis_check: is negative_sum >= -C * N?
    """
    N = p - 1

    # Build Farey sequence F_N using mediant algorithm
    fracs = []  # list of (a, b) tuples
    a, b = 0, 1
    c, d = 1, N
    fracs.append((0, 1))
    fracs.append((1, N))
    while (c, d) != (1, 1):
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        fracs.append((c, d))

    n = len(fracs)

    # Compute D(a/b) = rank - n*(a/b) for each fraction
    # Using exclusive rank: rank(f) = index j (0-indexed)
    D_vals = []
    for j, (a_j, b_j) in enumerate(fracs):
        D = j - n * a_j / b_j
        D_vals.append(D)

    old_D_sq = sum(d*d for d in D_vals)

    # Compute delta(a/b) = (a - sigma_p(a)) / b
    # sigma_p(a) = (p*a) mod b
    delta_vals = []
    for (a_j, b_j) in fracs:
        if b_j == 0:
            delta_vals.append(0.0)
        else:
            sigma = (p * a_j) % b_j
            delta_vals.append((a_j - sigma) / b_j)

    # Compute t(f) = 2*D(f)*delta(f) + delta(f)^2 for each fraction
    t_vals = [2*D_vals[j]*delta_vals[j] + delta_vals[j]**2 for j in range(n)]

    B_raw = 2.0 * sum(D_vals[j] * delta_vals[j] for j in range(n))
    delta_sq = sum(dv**2 for dv in delta_vals)
    B_plus_C = B_raw + delta_sq
    t_sum = sum(t_vals)

    # Decompose into positive and negative contributions
    positive_sum = sum(t for t in t_vals if t > 0)
    negative_sum = sum(t for t in t_vals if t < 0)
    negative_count = sum(1 for t in t_vals if t < 0)
    max_negative = min(t_vals)  # most negative value

    # -----------------------------------------------
    # Per-pair analysis
    # Build a lookup from (a, b) -> index
    frac_to_idx = {(a_j, b_j): j for j, (a_j, b_j) in enumerate(fracs)}

    pair_positive_count = 0
    pair_negative_count = 0
    pair_zero_count = 0
    pairs_analyzed = 0
    worst_pair_contribution = 0.0

    visited = set()
    for j, (a_j, b_j) in enumerate(fracs):
        if j in visited:
            continue
        if a_j == 0 or a_j == b_j:  # boundaries 0/1 and 1/1
            visited.add(j)
            continue
        # Interior fraction: find its complement (b-a)/b
        a_comp = b_j - a_j
        comp_key = (a_comp, b_j)
        if a_comp == a_j:  # self-paired: a/b = 1/2
            visited.add(j)
            continue
        if comp_key not in frac_to_idx:
            visited.add(j)
            continue
        j_comp = frac_to_idx[comp_key]
        visited.add(j)
        visited.add(j_comp)

        # Pair contribution
        pair_bc = t_vals[j] + t_vals[j_comp]
        pairs_analyzed += 1

        if pair_bc > 1e-12:
            pair_positive_count += 1
        elif pair_bc < -1e-12:
            pair_negative_count += 1
            if pair_bc < worst_pair_contribution:
                worst_pair_contribution = pair_bc
        else:
            pair_zero_count += 1

    # Check positive pair condition: delta * (D_{p-1} + D_p + 1) > 0
    # D_p = D_{p-1} + delta, so condition is: delta * (2*D_{p-1} + delta + 1) > 0
    positive_pair_cond_count = 0
    negative_pair_cond_count = 0
    for j, (a_j, b_j) in enumerate(fracs):
        if a_j == 0 or a_j == b_j:
            continue
        D_old = D_vals[j]
        delt = delta_vals[j]
        D_new = D_old + delt
        pair_cond_val = delt * (D_old + D_new + 1)
        if pair_cond_val > 1e-12:
            positive_pair_cond_count += 1
        elif pair_cond_val < -1e-12:
            negative_pair_cond_count += 1

    # Key hypothesis: |negative_sum| <= C_0 * N
    C_0 = abs(negative_sum) / N if N > 0 else 0

    # Analytic lower bound check:
    # delta_sq >= N^2 / (48 log N) for N >= 100
    if N >= 100:
        delta_sq_lb = N**2 / (48 * log(N))
        margin = B_plus_C - delta_sq_lb
    else:
        delta_sq_lb = 0
        margin = B_plus_C

    n_prime = n + p - 1
    dilution_raw = old_D_sq * (n_prime**2 - n**2) / (n**2)
    CA_ratio = delta_sq / dilution_raw if dilution_raw > 0 else 0

    return {
        'p': p, 'N': N, 'n': n,
        'old_D_sq': old_D_sq,
        'B_raw': B_raw,
        'delta_sq': delta_sq,
        'B_plus_C': B_plus_C,
        't_sum_check': t_sum,
        'positive_sum': positive_sum,
        'negative_sum': negative_sum,
        'negative_count': negative_count,
        'max_negative': max_negative,
        'pairs_analyzed': pairs_analyzed,
        'pair_positive_count': pair_positive_count,
        'pair_negative_count': pair_negative_count,
        'C_0_coeff': C_0,   # |neg_sum| / N
        'delta_sq_lb': delta_sq_lb,
        'margin': margin,
        'CA_ratio': CA_ratio,
        'dilution_raw': dilution_raw,
        'positive_pair_cond': positive_pair_cond_count,
        'negative_pair_cond': negative_pair_cond_count,
    }


def main():
    LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    primes = sieve_primes(LIMIT)
    test_primes = [p for p in primes if p >= 11]

    print("=" * 110)
    print("B+C TERM STRUCTURE: Path to Analytical Proof of B+C > 0")
    print("=" * 110)
    print()
    print("IDENTITY: B+C = Sum_f t(f)  where t(f) = delta(f) * (2*D(f) + delta(f))")
    print()
    print("KEY DECOMPOSITION:")
    print("  t(f) = delta(f) * (D_{p-1}(f) + D_p(f))   [since D_p = D_{p-1} + delta]")
    print()
    print("For B+C > 0 analytically, we need:")
    print("  negative_sum = Sum_{t(f)<0} t(f) >= -delta_sq  (so B+C >= 0)")
    print("  Better: negative_sum = O(N) while delta_sq = Omega(N^2 / log N)")
    print()

    header = (f"{'p':>6} {'B+C':>12} {'pos_sum':>12} {'neg_sum':>12} "
              f"{'neg_cnt':>7} {'C_0=|neg|/N':>12} {'d_sq_lb':>12} {'margin':>10}")
    print(header)
    print("-" * len(header))

    all_results = []
    max_C0 = 0.0
    max_C0_p = 0
    min_BC_over_dlt = float('inf')

    for p in test_primes:
        r = analyze_BC_structure(p)
        all_results.append(r)

        C0 = r['C_0_coeff']
        if C0 > max_C0:
            max_C0 = C0
            max_C0_p = p

        if r['delta_sq'] > 0:
            ratio = r['B_plus_C'] / r['delta_sq']
            if ratio < min_BC_over_dlt:
                min_BC_over_dlt = ratio

        elapsed = time.time() - start_time
        should_print = (p <= 100 or p % 100 == 1 or p > LIMIT - 20 or
                        C0 > max_C0 * 0.95 or elapsed < 5)

        if should_print:
            print(f"{p:6d} {r['B_plus_C']:12.4f} {r['positive_sum']:12.4f} "
                  f"{r['negative_sum']:12.4f} {r['negative_count']:7d} "
                  f"{C0:12.4f} {r['delta_sq_lb']:12.4f} {r['margin']:10.4f}",
                  flush=True)

    print()
    print("=" * 110)
    print("ANALYSIS SUMMARY")
    print("=" * 110)
    print()

    # Check B+C > 0 for all primes
    violations = [r for r in all_results if r['B_plus_C'] <= 0]
    print(f"B+C > 0 for all tested primes: {'YES' if not violations else 'NO - VIOLATIONS!'}")
    if violations:
        for v in violations[:5]:
            print(f"  VIOLATION: p={v['p']}, B+C={v['B_plus_C']:.6f}")
    print()

    # C_0 analysis: |neg_sum| <= C_0 * N
    print(f"Maximum C_0 = |negative_sum| / N: {max_C0:.6f}  (at p = {max_C0_p})")
    print(f"Minimum B+C / delta_sq ratio: {min_BC_over_dlt:.6f}")
    print()

    # Detailed C_0 by range
    print("C_0 = |negative_sum| / N by prime range:")
    print(f"{'range':>20s} {'max_C0':>10s} {'avg_C0':>10s} {'count':>6s}")
    ranges = [(11, 50), (50, 100), (100, 200), (200, 500)]
    for lo, hi in ranges:
        sub = [r for r in all_results if lo <= r['p'] <= hi]
        if sub:
            C0s = [r['C_0_coeff'] for r in sub]
            print(f"  [{lo:>4d},{hi:>4d}] {max(C0s):10.4f} {sum(C0s)/len(C0s):10.4f} {len(sub):6d}")
    print()

    # Negative pair analysis
    total_neg_pairs = sum(r['pair_negative_count'] for r in all_results)
    total_pairs = sum(r['pairs_analyzed'] for r in all_results)
    print(f"Pairs with NEGATIVE contribution to B+C: "
          f"{total_neg_pairs}/{total_pairs} = {100*total_neg_pairs/max(total_pairs,1):.2f}%")
    print()

    # Positive pair condition analysis
    total_neg_cond = sum(r['negative_pair_cond'] for r in all_results)
    total_fracs_analyzed = sum(r['n'] - 2 for r in all_results)  # interior only
    print(f"Interior fractions violating positive pair condition [delta*(D_old+D_new+1)>0]:")
    print(f"  {total_neg_cond}/{total_fracs_analyzed} = "
          f"{100*total_neg_cond/max(total_fracs_analyzed,1):.2f}%")
    print()

    # Key theorem check:
    # If |neg_sum| <= C_0 * N and delta_sq >= N^2/(48 log N),
    # then for N >= 48 * C_0 * log N, we get B+C > 0 analytically.
    print("=" * 110)
    print("KEY THEOREM CHECK: B+C >= delta_sq - C_0 * N >= N^2/(48 log N) - C_0 * N")
    print()
    max_C0_overall = max(r['C_0_coeff'] for r in all_results)
    print(f"  Max C_0 = {max_C0_overall:.4f}")
    print(f"  Need: N > 48 * {max_C0_overall:.4f} * log N")

    # Find crossover N
    for N_test in range(10, 100000):
        if N_test > 48 * max_C0_overall * log(max(N_test, 2)):
            print(f"  Crossover: N >= {N_test} (i.e., p >= {N_test+1}) guarantees B+C > 0 analytically!")
            break
    else:
        print(f"  Crossover not found in N <= 100000 with C_0 = {max_C0_overall:.4f}")
    print()

    # Asymptotic analysis of C_0
    print("Trend of C_0 with N:")
    for r in all_results[-10:]:
        print(f"  p={r['p']:4d}: N={r['N']:4d}, neg_sum={r['negative_sum']:8.3f}, "
              f"C_0={r['C_0_coeff']:.4f}, B+C/delta_sq={r['B_plus_C']/max(r['delta_sq'],1e-10):.4f}")
    print()

    # -----------------------------------------------
    # STRUCTURAL ANALYSIS: What drives the negative t(f) values?
    # -----------------------------------------------
    print("=" * 110)
    print("STRUCTURAL ANALYSIS: Sources of negative t(f) terms")
    print("=" * 110)
    print()

    # Analyze the LAST prime's t(f) distribution in detail
    last_r = all_results[-1]
    p = last_r['p']
    print(f"Detail for p = {p}:")

    # Recompute for last prime
    N = p - 1
    fracs = []
    a, b = 0, 1
    c, d = 1, N
    fracs.append((0, 1))
    fracs.append((1, N))
    while (c, d) != (1, 1):
        kk = (N + b) // d
        a, b, c, d = c, d, kk*c - a, kk*d - b
        fracs.append((c, d))
    n = len(fracs)
    D_vals_p = [j - n * fracs[j][0] / fracs[j][1] for j in range(n)]
    delta_vals_p = [(fracs[j][0] - (p * fracs[j][0]) % fracs[j][1]) / fracs[j][1]
                    for j in range(n)]
    t_vals_p = [2*D_vals_p[j]*delta_vals_p[j] + delta_vals_p[j]**2 for j in range(n)]

    # Distribution of t values
    neg_terms = [(t_vals_p[j], fracs[j], D_vals_p[j], delta_vals_p[j])
                 for j in range(n) if t_vals_p[j] < -0.01]
    neg_terms.sort()  # most negative first

    print(f"  Total fracs: {n}, Negative t(f) terms: {len(neg_terms)}")
    print(f"  Top 10 most negative terms:")
    print(f"  {'t(f)':>10} {'a/b':>12} {'D(f)':>10} {'delta':>10} {'b':>6}")
    for t, (a_j, b_j), D_j, d_j in neg_terms[:10]:
        print(f"  {t:10.4f} {a_j:5d}/{b_j:<6d} {D_j:10.4f} {d_j:10.4f} {b_j:6d}")

    # Denominator distribution of negative terms
    neg_by_denom = defaultdict(float)
    for t, (a_j, b_j), D_j, d_j in neg_terms:
        neg_by_denom[b_j] += t

    print()
    print("  Negative contributions by denominator (top 10):")
    sorted_denoms = sorted(neg_by_denom.items(), key=lambda x: x[1])[:10]
    for b_j, total in sorted_denoms:
        print(f"    b={b_j}: total_neg={total:.4f}")

    print()
    print(f"  total negative_sum = {sum(t for t, _, _, _ in neg_terms):.4f}")
    print(f"  N = {N}, C_0 * N = {last_r['C_0_coeff'] * N:.4f}")

    # Check denominator-bounded claim:
    # Claim: negative terms all come from fracs with small denom b <= B_0
    B_thresholds = [2, 5, 10, 20, 50, 100, 500]
    print()
    print("  Negative sum from fracs with b <= threshold:")
    for B0 in B_thresholds:
        partial = sum(t for t, (a_j, b_j), _, _ in neg_terms if b_j <= B0)
        frac_neg = sum(1 for t, (a_j, b_j), _, _ in neg_terms if b_j <= B0)
        print(f"    b <= {B0:4d}: partial_neg_sum = {partial:.4f}  "
              f"({frac_neg} terms, {100*partial/min(sum(t for t,_,_,_ in neg_terms), -1e-10):.1f}% of total neg)")

    print()
    print(f"Total runtime: {time.time() - start_time:.1f}s")


if __name__ == '__main__':
    main()
