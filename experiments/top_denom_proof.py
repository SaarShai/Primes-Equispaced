#!/usr/bin/env python3
"""
TOP DENOMINATOR PROOF: TERM_A >= 0.55 * dilution_raw
=====================================================

STRATEGY:
  Sum the D^2 contributions from the LARGEST denominators in the Farey sequence.
  For each denominator b in {p-1, p-2, ..., 2}, determine which fraction a_b/b
  is selected by the injection map (left neighbor of some k/p), compute D(a_b/b)^2
  exactly, and check whether the sum of the top contributions exceeds 0.55 * dilution.

  Key identity:
    TERM_A = sum_{k=1}^{p-1} D(f_{j(k)})^2
  where f_{j(k)} is the left Farey neighbor of k/p in F_{p-1}.

  The left neighbor of k/p in F_{p-1} is the fraction a/b where b is the
  denominator and a = floor(k*b/p) when gcd(a,b)=1 and b <= p-1.

  For b = p-1: exactly one Farey fraction with denominator p-1 is selected,
  and its D^2 contribution is large because fractions near 0 and 1 have
  extreme rank-deviation.

ALL COMPUTATIONS USE EXACT Fraction ARITHMETIC for p <= 200.
"""

import time
from math import gcd, isqrt
from fractions import Fraction
from collections import defaultdict

# ============================================================
# UTILITIES
# ============================================================

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

def farey_generator(N):
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))


# ============================================================
# EXACT COMPUTATION: Per-denominator D^2 contributions to TERM_A
# ============================================================

def exact_top_denom_analysis(p, phi_arr):
    """
    For prime p, compute TERM_A and dilution_raw with exact arithmetic.
    Return per-denominator breakdown of contributions to TERM_A.
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    # Build Farey sequence with exact fractions
    farey_pairs = list(farey_generator(N))
    num_farey = len(farey_pairs)
    farey_fracs = [Fraction(a, b) for a, b in farey_pairs]
    farey_denoms = [b for _, b in farey_pairs]

    # D(f) = rank(f) - n * f, where rank = index in Farey sequence
    D_vals = [Fraction(j) - n * farey_fracs[j] for j in range(num_farey)]
    D_sq_vals = [d * d for d in D_vals]

    old_D_sq = sum(D_sq_vals)
    T_factor = Fraction(n_prime**2 - n**2, n**2)
    dilution_raw = old_D_sq * T_factor

    # For each k in {1,...,p-1}, find left neighbor via exact comparison
    # Track per-denominator contributions
    denom_TERM_A = defaultdict(lambda: Fraction(0))
    denom_count = defaultdict(int)  # how many k map to this denom
    denom_fractions = defaultdict(set)  # which fractions are selected
    TERM_A = Fraction(0)

    for k in range(1, p):
        target = Fraction(k, p)

        # Binary search for left neighbor (largest farey_frac < target)
        lo, hi = 0, num_farey - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if farey_fracs[mid] < target:
                lo = mid
            else:
                hi = mid - 1
        j = lo

        b_j = farey_denoms[j]
        a_j = farey_pairs[j][0]
        D_sq_j = D_sq_vals[j]

        TERM_A += D_sq_j
        denom_TERM_A[b_j] += D_sq_j
        denom_count[b_j] += 1
        denom_fractions[b_j].add((a_j, b_j))

    fill_fraction = TERM_A / dilution_raw if dilution_raw != 0 else Fraction(0)

    # Also compute total D^2 per denominator (for comparison)
    denom_total_D_sq = defaultdict(lambda: Fraction(0))
    denom_total_count = defaultdict(int)
    for j in range(num_farey):
        b = farey_denoms[j]
        denom_total_D_sq[b] += D_sq_vals[j]
        denom_total_count[b] += 1

    return {
        'p': p,
        'n': num_farey,
        'n_prime': n_prime,
        'TERM_A': TERM_A,
        'dilution_raw': dilution_raw,
        'old_D_sq': old_D_sq,
        'T_factor': T_factor,
        'fill_fraction': fill_fraction,
        'denom_TERM_A': dict(denom_TERM_A),
        'denom_count': dict(denom_count),
        'denom_fractions': dict(denom_fractions),
        'denom_total_D_sq': dict(denom_total_D_sq),
        'denom_total_count': dict(denom_total_count),
    }


def print_top_denoms(info, top_k=15):
    """Print the top contributing denominators sorted by TERM_A contribution."""
    p = info['p']
    dilution_raw = info['dilution_raw']

    print(f"\n{'='*70}")
    print(f"  p = {p}, n = {info['n']}, fill_fraction = {float(info['fill_fraction']):.6f}")
    print(f"  TERM_A = {float(info['TERM_A']):.6f}")
    print(f"  dilution_raw = {float(info['dilution_raw']):.6f}")
    print(f"  old_D_sq = {float(info['old_D_sq']):.6f}")
    print(f"{'='*70}")

    # Sort denominators by TERM_A contribution (descending)
    denoms = sorted(info['denom_TERM_A'].keys(),
                    key=lambda b: info['denom_TERM_A'][b], reverse=True)

    print(f"\n  Top {min(top_k, len(denoms))} denominators by TERM_A contribution:")
    print(f"  {'b':>6} {'TERM_A_b':>14} {'frac_of_dilut':>14} {'#filled':>8} "
          f"{'#total':>8} {'fractions selected':>30}")
    print(f"  {'-'*84}")

    cumulative = Fraction(0)
    for i, b in enumerate(denoms[:top_k]):
        ta_b = info['denom_TERM_A'][b]
        cumulative += ta_b
        frac_dilut = float(ta_b / dilution_raw) if dilution_raw != 0 else 0
        fc = info['denom_count'].get(b, 0)
        tc = info['denom_total_count'].get(b, 0)
        fracs = info['denom_fractions'].get(b, set())
        frac_strs = [f"{a}/{b}" for a, bb in sorted(fracs)][:5]
        frac_str = ", ".join(frac_strs)
        if len(fracs) > 5:
            frac_str += f" ... ({len(fracs)} total)"

        print(f"  {b:6d} {float(ta_b):14.6f} {frac_dilut:14.6f} {fc:8d} {tc:8d}  {frac_str}")

    cum_frac = float(cumulative / dilution_raw) if dilution_raw != 0 else 0
    print(f"\n  Cumulative top-{min(top_k, len(denoms))} contribution: "
          f"{float(cumulative):.6f} = {cum_frac:.6f} of dilution")
    print(f"  Remaining: {float(info['TERM_A'] - cumulative):.6f} = "
          f"{float((info['TERM_A'] - cumulative) / dilution_raw):.6f} of dilution")


def analyze_b_p_minus_1(info):
    """
    Detailed analysis of the b = p-1 denominator contribution.

    For b = p-1 in F_{p-1}, the only fractions with denominator p-1 are:
      1/(p-1), 2/(p-1), ..., (p-2)/(p-1)  (those with gcd(a, p-1) = 1)

    The D value at fraction a/(p-1) is:
      D(a/(p-1)) = rank(a/(p-1)) - n * a/(p-1)
    """
    p = info['p']
    n = info['n']
    dilution_raw = info['dilution_raw']
    b = p - 1

    ta_b = info['denom_TERM_A'].get(b, Fraction(0))
    total_b = info['denom_total_D_sq'].get(b, Fraction(0))
    filled_fracs = info['denom_fractions'].get(b, set())
    num_filled = info['denom_count'].get(b, 0)
    num_total = info['denom_total_count'].get(b, 0)

    print(f"\n  --- b = {b} (= p-1) analysis ---")
    print(f"  phi({b}) = {num_total} fractions with denom {b} in F_{{{b}}}")
    print(f"  {num_filled} of them contribute to TERM_A")
    print(f"  TERM_A contribution: {float(ta_b):.6f} = "
          f"{float(ta_b / dilution_raw):.6f} of dilution")
    print(f"  Total D^2 for denom {b}: {float(total_b):.6f} = "
          f"{float(total_b / dilution_raw):.6f} of dilution")

    if filled_fracs:
        print(f"  Selected fractions: {sorted(filled_fracs)[:10]}")


def exact_D_for_fraction(a, b, farey_fracs, n):
    """Compute D(a/b) = rank(a/b, F_N) - n * (a/b) exactly."""
    target = Fraction(a, b)
    # rank = index in sorted Farey sequence
    rank = 0
    for f in farey_fracs:
        if f <= target:
            rank += 1
        else:
            break
    rank -= 1  # 0-indexed
    return Fraction(rank) - n * target


# ============================================================
# CUMULATIVE ANALYSIS: Sum top-b contributions and track threshold
# ============================================================

def cumulative_threshold_analysis(p, phi_arr):
    """
    For each prime p, compute TERM_A/dilution and determine how many
    top denominators are needed to exceed 0.55.
    """
    info = exact_top_denom_analysis(p, phi_arr)
    dilution_raw = info['dilution_raw']

    denoms_sorted = sorted(info['denom_TERM_A'].keys(),
                           key=lambda b: info['denom_TERM_A'][b], reverse=True)

    cumulative = Fraction(0)
    threshold_reached = None

    for i, b in enumerate(denoms_sorted):
        cumulative += info['denom_TERM_A'][b]
        ratio = float(cumulative / dilution_raw) if dilution_raw != 0 else 0
        if ratio >= 0.55 and threshold_reached is None:
            threshold_reached = (i + 1, b, ratio)

    return {
        'p': p,
        'fill_fraction': float(info['fill_fraction']),
        'threshold_info': threshold_reached,
        'num_denoms_with_contribution': len(denoms_sorted),
        'top_denom': denoms_sorted[0] if denoms_sorted else None,
        'top_denom_frac': float(info['denom_TERM_A'][denoms_sorted[0]] / dilution_raw)
            if denoms_sorted and dilution_raw != 0 else 0,
    }


# ============================================================
# EXACT b=p-1 FORMULA VERIFICATION
# ============================================================

def verify_b_p_minus_1_formula(p, phi_arr):
    """
    Verify the exact D^2 for the b=p-1 contribution.

    Fractions with denominator p-1 in F_{p-1}:
      a/(p-1) where 1 <= a <= p-2 and gcd(a, p-1) = 1

    For each such fraction, D = rank - n * value.
    The key fraction (p-2)/(p-1) has rank = n-2 (second-to-last), value ~ 1.
    D((p-2)/(p-1)) = (n-2) - n*(p-2)/(p-1) = -2 + 2n/(p-1)

    Similarly 1/(p-1) has rank = 1 (second element), value ~ 0.
    D(1/(p-1)) = 1 - n/(p-1)
    """
    N = p - 1
    n = farey_size(N, phi_arr)

    # Build Farey sequence for exact rank computation
    farey_pairs = list(farey_generator(N))
    farey_fracs = [Fraction(a, b) for a, b in farey_pairs]
    num_farey = len(farey_pairs)

    print(f"\n  {'='*60}")
    print(f"  b = p-1 = {p-1} formula verification for p = {p}")
    print(f"  n = |F_{{p-1}}| = {n}")
    print(f"  {'='*60}")

    # Check each fraction with denominator p-1
    b = p - 1
    fracs_with_b = [(a, b) for a in range(1, b) if gcd(a, b) == 1]

    print(f"\n  Fractions with denominator {b}: {len(fracs_with_b)}")
    print(f"  {'a/(p-1)':>12} {'rank':>8} {'D_exact':>18} {'D_formula':>18} {'D^2':>18} {'match':>6}")
    print(f"  {'-'*84}")

    for a_val, b_val in fracs_with_b:
        target = Fraction(a_val, b_val)
        # Find rank (0-indexed position in Farey sequence)
        rank = None
        for j, f in enumerate(farey_fracs):
            if f == target:
                rank = j
                break

        if rank is None:
            print(f"  {a_val}/{b_val}: NOT FOUND in Farey sequence!")
            continue

        D_exact = Fraction(rank) - n * target
        D_sq = D_exact * D_exact

        # For a/(p-1): formula D = rank - n*a/(p-1)
        # For (p-2)/(p-1): D = (n-2) - n*(p-2)/(p-1)
        D_formula = Fraction(rank) - Fraction(n * a_val, b_val)

        match = "YES" if D_exact == D_formula else "NO"

        if a_val <= 3 or a_val >= b_val - 3:
            print(f"  {a_val:3d}/{b_val:<5d} {rank:8d} {float(D_exact):18.8f} "
                  f"{float(D_formula):18.8f} {float(D_sq):18.8f} {match:>6}")

    # Special: verify D((p-2)/(p-1)) = -2 + 2n/(p-1)
    a_top = p - 2
    target_top = Fraction(a_top, b)
    rank_top = None
    for j, f in enumerate(farey_fracs):
        if f == target_top:
            rank_top = j
            break

    D_top = Fraction(rank_top) - n * target_top
    D_formula_top = Fraction(-2) + Fraction(2 * n, p - 1)

    print(f"\n  Verification: D((p-2)/(p-1)) = -2 + 2n/(p-1)")
    print(f"    D_computed = {float(D_top):.10f}")
    print(f"    D_formula  = {float(D_formula_top):.10f}")
    print(f"    Match: {D_top == D_formula_top}")
    print(f"    D^2 = {float(D_top**2):.10f}")

    # Also verify D(1/(p-1)) = 1 - n/(p-1)
    target_low = Fraction(1, b)
    rank_low = None
    for j, f in enumerate(farey_fracs):
        if f == target_low:
            rank_low = j
            break

    D_low = Fraction(rank_low) - n * target_low
    D_formula_low = Fraction(1) - Fraction(n, p - 1)

    print(f"\n  Verification: D(1/(p-1)) = 1 - n/(p-1)")
    print(f"    D_computed = {float(D_low):.10f}")
    print(f"    D_formula  = {float(D_formula_low):.10f}")
    print(f"    Match: {D_low == D_formula_low}")
    print(f"    D^2 = {float(D_low**2):.10f}")

    return D_top, D_low


# ============================================================
# RATIO WITHOUT old_D_sq: Can we express TERM_A_b / dilution
# without depending on old_D_sq?
# ============================================================

def ratio_decomposition(p, phi_arr):
    """
    Investigate: TERM_A / dilution_raw = TERM_A / (old_D_sq * T)
    = (TERM_A / old_D_sq) / T = fill_rate / T

    where fill_rate = TERM_A / old_D_sq = fraction of old D^2 captured.
    T = (n'^2 - n^2) / n^2 = (2(p-1) + (p-1)^2/n^2 ... )

    Key question: is fill_rate * n^2 / (n'^2 - n^2) >= 0.55 provably?
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    farey_pairs = list(farey_generator(N))
    num_farey = len(farey_pairs)
    farey_fracs = [Fraction(a, b) for a, b in farey_pairs]
    farey_denoms = [b for _, b in farey_pairs]

    D_vals = [Fraction(j) - n * farey_fracs[j] for j in range(num_farey)]
    D_sq_vals = [d * d for d in D_vals]

    old_D_sq = sum(D_sq_vals)
    T_factor = Fraction(n_prime**2 - n**2, n**2)

    # TERM_A
    TERM_A = Fraction(0)
    for k in range(1, p):
        target = Fraction(k, p)
        lo, hi = 0, num_farey - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if farey_fracs[mid] < target:
                lo = mid
            else:
                hi = mid - 1
        TERM_A += D_sq_vals[lo]

    fill_rate = TERM_A / old_D_sq  # fraction of old_D_sq captured
    fill_frac = TERM_A / (old_D_sq * T_factor)  # = fill_rate / T

    # T_factor = (n'^2 - n^2)/n^2 = (2n(p-1) + (p-1)^2) / n^2
    # For n ~ 3p^2/pi^2, T ~ 2(p-1)/n + (p-1)^2/n^2
    # ~ 2pi^2/(3p) + pi^4/(9p^2)

    T_approx = 2 * (p - 1) / n + (p - 1)**2 / n**2

    print(f"\n  p = {p:4d}: fill_rate = {float(fill_rate):.6f}, "
          f"T = {float(T_factor):.6f} (approx {T_approx:.6f}), "
          f"fill_frac = fill_rate/T = {float(fill_frac):.6f}")

    return fill_rate, T_factor, fill_frac


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 80)
    print("TOP DENOMINATOR PROOF: TERM_A >= 0.55 * dilution_raw")
    print("  Sum D^2 from LARGEST denominators, exact Fraction arithmetic")
    print("=" * 80)

    MAX_PRIME = 200
    phi = euler_totient_sieve(MAX_PRIME)
    primes = [p for p in sieve_primes(MAX_PRIME) if p >= 5]

    # ==============================================================
    # SECTION 1: Per-denominator breakdown for small primes
    # ==============================================================
    print("\n" + "=" * 70)
    print("SECTION 1: Per-denominator D^2 contributions (exact arithmetic)")
    print("=" * 70)

    key_primes = [p for p in [5, 7, 11, 13, 23, 29, 37, 53, 67, 97, 101, 127, 151, 197]
                  if p in primes]

    for p in key_primes[:6]:  # Detailed for small primes
        info = exact_top_denom_analysis(p, phi)
        print_top_denoms(info, top_k=10)

    # ==============================================================
    # SECTION 2: b=p-1 formula verification
    # ==============================================================
    print("\n" + "=" * 70)
    print("SECTION 2: b = p-1 formula verification")
    print("  D((p-2)/(p-1)) = -2 + 2n/(p-1)")
    print("  D(1/(p-1))     = 1 - n/(p-1)")
    print("=" * 70)

    for p in [5, 7, 11, 13, 23, 37, 53, 97]:
        if p in primes:
            verify_b_p_minus_1_formula(p, phi)

    # ==============================================================
    # SECTION 3: Cumulative threshold analysis
    # ==============================================================
    print("\n" + "=" * 70)
    print("SECTION 3: How many top denominators needed to exceed 0.55?")
    print("=" * 70)

    print(f"\n{'p':>6} {'fill_frac':>12} {'#denoms_to_0.55':>16} {'top_denom':>10} "
          f"{'top_frac':>10} {'total_denoms':>12}")
    print("-" * 70)

    for p in primes:
        result = cumulative_threshold_analysis(p, phi)
        thresh = result['threshold_info']
        thresh_count = thresh[0] if thresh else "N/A"
        thresh_denom = thresh[1] if thresh else "N/A"
        thresh_ratio = f"{thresh[2]:.4f}" if thresh else "N/A"

        print(f"{p:6d} {result['fill_fraction']:12.6f} {str(thresh_count):>16} "
              f"{str(result['top_denom']):>10} {result['top_denom_frac']:10.4f} "
              f"{result['num_denoms_with_contribution']:12d}")

    # ==============================================================
    # SECTION 4: b=p-1 contribution as fraction of dilution (scaling)
    # ==============================================================
    print("\n" + "=" * 70)
    print("SECTION 4: b=p-1 contribution / dilution_raw (scaling with p)")
    print("=" * 70)

    print(f"\n{'p':>6} {'D((p-2)/(p-1))^2':>20} {'contrib/dilut':>14} "
          f"{'n':>8} {'n/(p-1)':>10}")
    print("-" * 62)

    for p in primes:
        info = exact_top_denom_analysis(p, phi)
        b = p - 1
        ta_b = info['denom_TERM_A'].get(b, Fraction(0))
        ratio = float(ta_b / info['dilution_raw']) if info['dilution_raw'] != 0 else 0
        n = info['n']
        n_over_pm1 = n / (p - 1)

        print(f"{p:6d} {float(ta_b):20.6f} {ratio:14.6f} {n:8d} {n_over_pm1:10.4f}")

    # ==============================================================
    # SECTION 5: fill_rate = TERM_A / old_D_sq decomposition
    # ==============================================================
    print("\n" + "=" * 70)
    print("SECTION 5: fill_rate = TERM_A / old_D_sq and T decomposition")
    print("  fill_fraction = fill_rate / T")
    print("  T = (n'^2 - n^2) / n^2")
    print("=" * 70)

    for p in primes:
        ratio_decomposition(p, phi)

    # ==============================================================
    # SECTION 6: PROOF VERIFICATION -- TERM_A >= 0.55 * dilution
    # ==============================================================
    print("\n" + "=" * 70)
    print("SECTION 6: EXACT VERIFICATION: TERM_A >= 0.55 * dilution_raw")
    print("  Using exact Fraction arithmetic for ALL primes up to", MAX_PRIME)
    print("=" * 70)

    all_pass = True
    min_ff = float('inf')
    min_ff_p = 0

    print(f"\n{'p':>6} {'TERM_A':>18} {'0.55*dilut':>18} {'TERM_A >= 0.55*d':>18} "
          f"{'fill_frac':>12}")
    print("-" * 76)

    for p in primes:
        info = exact_top_denom_analysis(p, phi)
        threshold = Fraction(55, 100) * info['dilution_raw']
        passes = info['TERM_A'] >= threshold
        ff = float(info['fill_fraction'])

        if ff < min_ff:
            min_ff = ff
            min_ff_p = p

        marker = "PASS" if passes else "FAIL"
        if not passes:
            all_pass = False

        if p <= 60 or p >= 100 or not passes:
            print(f"{p:6d} {float(info['TERM_A']):18.8f} {float(threshold):18.8f} "
                  f"{marker:>18} {ff:12.6f}")

    print(f"\n{'='*70}")
    print(f"  MINIMUM fill_fraction = {min_ff:.6f} at p = {min_ff_p}")
    print(f"  ALL primes 5..{MAX_PRIME} pass TERM_A >= 0.55 * dilution: "
          f"{'YES' if all_pass else 'NO'}")
    print(f"{'='*70}")

    # ==============================================================
    # SECTION 7: Top-5 denominators summed contribution
    # ==============================================================
    print("\n" + "=" * 70)
    print("SECTION 7: Sum of top-5 denominators' D^2 / dilution")
    print("  Can the top 5 alone exceed 0.55?")
    print("=" * 70)

    print(f"\n{'p':>6} {'top1':>10} {'top2':>10} {'top3':>10} {'top4':>10} "
          f"{'top5':>10} {'sum_top5':>10} {'>=0.55?':>8}")
    print("-" * 76)

    for p in primes:
        info = exact_top_denom_analysis(p, phi)
        dilution_raw = info['dilution_raw']

        denoms_sorted = sorted(info['denom_TERM_A'].keys(),
                               key=lambda b: info['denom_TERM_A'][b], reverse=True)

        top_vals = []
        for b in denoms_sorted[:5]:
            ratio = float(info['denom_TERM_A'][b] / dilution_raw) if dilution_raw != 0 else 0
            top_vals.append(ratio)
        while len(top_vals) < 5:
            top_vals.append(0.0)

        total = sum(top_vals)
        marker = "YES" if total >= 0.55 else "no"

        print(f"{p:6d} {top_vals[0]:10.4f} {top_vals[1]:10.4f} {top_vals[2]:10.4f} "
              f"{top_vals[3]:10.4f} {top_vals[4]:10.4f} {total:10.4f} {marker:>8}")

    # ==============================================================
    # SECTION 8: Identify the pattern in top denominators
    # ==============================================================
    print("\n" + "=" * 70)
    print("SECTION 8: Which denominators are consistently in the top?")
    print("  For each p, list the top-5 denominators by TERM_A contribution")
    print("=" * 70)

    for p in [11, 23, 37, 53, 67, 97, 127, 151, 197]:
        if p not in primes:
            continue
        info = exact_top_denom_analysis(p, phi)
        denoms_sorted = sorted(info['denom_TERM_A'].keys(),
                               key=lambda b: info['denom_TERM_A'][b], reverse=True)

        top5 = denoms_sorted[:5]
        top5_as_offset = [p - 1 - b for b in top5]
        print(f"  p={p:4d}: top denoms = {top5}, offsets from p-1 = {top5_as_offset}")


if __name__ == "__main__":
    main()
