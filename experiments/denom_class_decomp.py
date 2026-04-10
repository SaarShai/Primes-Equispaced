#!/usr/bin/env python3
"""
Denominator-class decomposition for B+C positivity proof.

For prime p, N = p-1, Farey sequence F_N:
  D(a/b) = rank(a/b in F_N) - |F_N| * (a/b)
  delta(a/b) = (a - (p*a mod b)) / b

B + C = sum_b [ 2<D_b^osc, delta_b> + ||delta_b||^2 ]

where D_b^osc = D_b - mean(D_b) is the oscillatory part of D restricted to denom b.

All arithmetic is exact using fractions.
"""

from fractions import Fraction
from math import gcd
from collections import defaultdict
import sys

def farey_sequence(N):
    """Generate Farey sequence F_N as list of Fraction(a, b) with 0 <= a/b <= 1."""
    fracs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.append(Fraction(a, b))
    fracs.sort()
    return fracs

def compute_all(p):
    """Compute full denominator-class decomposition for prime p."""
    N = p - 1
    F = farey_sequence(N)
    size_F = len(F)

    # Build rank map: rank(f) = index in F (0-based)
    rank_map = {}
    for i, f in enumerate(F):
        rank_map[f] = i

    # Compute D(a/b) = rank(a/b) - |F_N| * (a/b)
    D_map = {}
    for f in F:
        D_map[f] = Fraction(rank_map[f]) - Fraction(size_F) * f

    # Compute delta(a/b) = (a - (p*a mod b)) / b
    delta_map = {}
    for f in F:
        a, b = f.numerator, f.denominator
        pa_mod_b = (p * a) % b
        delta_map[f] = Fraction(a - pa_mod_b, b)

    # Group by denominator
    denom_groups = defaultdict(list)
    for f in F:
        denom_groups[f.denominator].append(f)

    # Per-denominator analysis
    results = {}
    total_BC = Fraction(0)
    total_cross = Fraction(0)
    total_delta_sq = Fraction(0)

    for b in sorted(denom_groups.keys()):
        fracs_b = denom_groups[b]
        phi_b = len(fracs_b)  # should be phi(b) + indicator for b=1

        # D values for this denominator
        D_vals = [D_map[f] for f in fracs_b]
        delta_vals = [delta_map[f] for f in fracs_b]

        # Mean of D over this denominator class
        D_mean = sum(D_vals) / len(D_vals)

        # D_b^osc = D - mean
        D_osc = [d - D_mean for d in D_vals]

        # Verify: sum of delta should be 0 per denominator class
        sum_delta = sum(delta_vals)

        # Verify: sum of D_osc should be 0
        sum_D_osc = sum(D_osc)

        # ||D_b^osc||^2
        D_osc_sq = sum(d*d for d in D_osc)

        # ||delta_b||^2
        delta_sq = sum(d*d for d in delta_vals)

        # <D_b^osc, delta_b>
        cross = sum(d*e for d, e in zip(D_osc, delta_vals))

        # Net contribution: 2*cross + delta_sq
        net = 2 * cross + delta_sq

        # Ratio ||D_b^osc|| / ||delta_b|| (if delta_sq > 0)
        # We compare D_osc_sq vs delta_sq/4 (ratio < 1/2 iff D_osc_sq < delta_sq/4)
        ratio_sq = None
        if delta_sq > 0:
            ratio_sq = D_osc_sq / delta_sq  # this is (ratio)^2

        total_BC += net
        total_cross += cross
        total_delta_sq += delta_sq

        results[b] = {
            'phi_b': phi_b,
            'D_osc_sq': D_osc_sq,
            'delta_sq': delta_sq,
            'cross': cross,
            'net': net,
            'sum_delta': sum_delta,
            'sum_D_osc': sum_D_osc,
            'ratio_sq': ratio_sq,
            'D_mean': D_mean,
        }

    return results, total_BC, total_cross, total_delta_sq, size_F

def euler_phi(n):
    """Euler totient."""
    result = n
    temp = n
    pp = 2
    while pp * pp <= temp:
        if temp % pp == 0:
            while temp % pp == 0:
                temp //= pp
            result -= result // pp
        pp += 1
    if temp > 1:
        result -= result // temp
    return result

def print_results(p, results, total_BC, total_cross, total_delta_sq, size_F):
    print(f"\n{'='*80}")
    print(f"PRIME p = {p}, N = {p-1}, |F_N| = {size_F}")
    print(f"{'='*80}")

    print(f"\n{'b':>4} {'phi(b)':>6} {'||D_osc||^2':>20} {'||delta||^2':>20} {'<D_osc,delta>':>20} {'net=2cr+d^2':>20} {'ratio^2':>12} {'ratio<1/2?':>10}")
    print(f"{'-'*4:>4} {'-'*6:>6} {'-'*20:>20} {'-'*20:>20} {'-'*20:>20} {'-'*20:>20} {'-'*12:>12} {'-'*10:>10}")

    neg_denoms = []
    for b in sorted(results.keys()):
        r = results[b]
        D_osc_sq = r['D_osc_sq']
        delta_sq = r['delta_sq']
        cross = r['cross']
        net = r['net']
        ratio_sq = r['ratio_sq']

        # Format ratio
        if ratio_sq is not None and ratio_sq > 0:
            ratio_float = float(ratio_sq)**0.5
            ratio_str = f"{ratio_float:.6f}"
            below_half = "YES" if ratio_sq < Fraction(1, 4) else "NO"
        elif delta_sq == 0:
            ratio_str = "N/A"
            below_half = "N/A"
        else:
            ratio_str = "0"
            below_half = "YES"

        net_sign = "+" if net > 0 else ("-" if net < 0 else "0")

        print(f"{b:>4} {r['phi_b']:>6} {float(D_osc_sq):>20.8f} {float(delta_sq):>20.8f} {float(cross):>20.8f} {float(net):>20.8f} {ratio_str:>12} {below_half:>10}")

        if net < 0:
            neg_denoms.append(b)

        # Verify sum_delta = 0
        if r['sum_delta'] != 0:
            print(f"  *** WARNING: sum(delta) for b={b} is {r['sum_delta']}, not 0!")

    print(f"\n--- Totals ---")
    print(f"  Total B+C = {float(total_BC):.10f}  (exact: {total_BC})")
    print(f"  Total 2*cross = {float(2*total_cross):.10f}")
    print(f"  Total ||delta||^2 = {float(total_delta_sq):.10f}")
    print(f"  B+C > 0? {total_BC > 0}")

    if neg_denoms:
        print(f"\n  Negative contributors: b = {neg_denoms}")
    else:
        print(f"\n  ALL denominator contributions are non-negative!")

    return neg_denoms

def analyze_ratio_bounds(p, results):
    """Analyze the ratio ||D_b^osc||/||delta_b|| and compare to generic bounds."""
    print(f"\n--- Ratio Analysis for p={p} ---")
    print(f"{'b':>4} {'phi(b)':>6} {'||D_osc||^2':>14} {'||delta||^2':>14} {'phi*b^2/6':>14} {'delta/generic':>14} {'ratio^2':>12}")

    for b in sorted(results.keys()):
        r = results[b]
        if r['delta_sq'] == 0:
            continue

        phi_b = euler_phi(b) if b > 1 else 1
        # "Generic permutation" bound: phi(b) * b^2 / 6
        # Actually for delta, we need to think about what the generic value is
        # delta(a/b) = (a - p*a mod b)/b, sum over a coprime to b
        # ||delta||^2 = sum (a - pa mod b)^2 / b^2
        # If sigma: a -> pa mod b is a permutation of units mod b (true for prime p not dividing b),
        # then sum (a - sigma(a))^2 for random permutation ~ phi(b) * something

        generic_bound = Fraction(phi_b * b * b, 6)  # rough estimate
        ratio_to_generic = float(r['delta_sq']) / float(generic_bound) if generic_bound > 0 else 0

        ratio_sq = r['ratio_sq']
        ratio_sq_f = float(ratio_sq) if ratio_sq is not None else 0

        print(f"{b:>4} {r['phi_b']:>6} {float(r['D_osc_sq']):>14.6f} {float(r['delta_sq']):>14.6f} {float(generic_bound):>14.6f} {ratio_to_generic:>14.6f} {ratio_sq_f:>12.8f}")

def analyze_delta_structure(p, results_data):
    """Deep dive into delta structure per denominator."""
    N = p - 1
    F = farey_sequence(N)

    denom_groups = defaultdict(list)
    for f in F:
        denom_groups[f.denominator].append(f)

    print(f"\n--- Delta Structure for p={p} ---")
    for b in sorted(denom_groups.keys()):
        if b <= 1:
            continue
        fracs_b = denom_groups[b]
        print(f"\n  b={b}: fractions = {[str(f) for f in fracs_b]}")
        for f in fracs_b:
            a = f.numerator
            pa_mod_b = (p * a) % b
            delta_val = Fraction(a - pa_mod_b, b)
            print(f"    a/b={f}: a={a}, pa mod b = {pa_mod_b}, delta = {delta_val} = {float(delta_val):.6f}")

def compute_delta_sq_exact(p, b):
    """
    Compute ||delta_b||^2 = (1/b^2) sum_{a: gcd(a,b)=1, 0<=a<=b} (a - pa mod b)^2
    Note: a=0 gives delta=0, a=b gives delta=0 (if b|p... but p prime, b<p so gcd(p,b)=1 for b>1)
    Actually a=b means a/b=1, and gcd(b,b)=b, so only in F_N if b=1.
    For b>1, a ranges over 1..b-1 with gcd(a,b)=1, plus a=0 if b=1.
    """
    total = Fraction(0)
    count = 0
    for a in range(0, b+1):
        if gcd(a, b) == 1:
            pa_mod_b = (p * a) % b
            diff = a - pa_mod_b
            total += Fraction(diff * diff, b * b)
            count += 1
    return total, count

def main():
    primes = [13, 17, 23, 29, 37]

    all_results = {}
    all_neg_denoms = {}

    for p in primes:
        results, total_BC, total_cross, total_delta_sq, size_F = compute_all(p)
        neg = print_results(p, results, total_BC, total_cross, total_delta_sq, size_F)
        analyze_ratio_bounds(p, results)
        all_results[p] = results
        all_neg_denoms[p] = neg

    # Summary
    print(f"\n\n{'='*80}")
    print(f"SUMMARY OF NEGATIVE DENOMINATOR CONTRIBUTIONS")
    print(f"{'='*80}")
    for p in primes:
        neg = all_neg_denoms[p]
        if neg:
            print(f"  p={p}: negative at b = {neg}")
        else:
            print(f"  p={p}: ALL positive")

    # Max ratio analysis
    print(f"\n{'='*80}")
    print(f"MAX RATIO ||D_b^osc||/||delta_b|| ACROSS ALL DENOMINATORS")
    print(f"{'='*80}")
    for p in primes:
        max_ratio_sq = Fraction(0)
        max_b = None
        for b, r in all_results[p].items():
            if r['ratio_sq'] is not None and r['ratio_sq'] > max_ratio_sq:
                max_ratio_sq = r['ratio_sq']
                max_b = b
        if max_b is not None:
            print(f"  p={p}: max ratio = {float(max_ratio_sq)**0.5:.8f} at b={max_b}  (ratio^2 = {float(max_ratio_sq):.8f}, threshold = 0.25)")
            print(f"         ratio < 1/2? {max_ratio_sq < Fraction(1,4)}")

    # Detailed view for small p
    print(f"\n{'='*80}")
    print(f"DETAILED DELTA STRUCTURE FOR p=13")
    print(f"{'='*80}")
    analyze_delta_structure(13, all_results[13])

    # KEY QUESTION: scaling of ||D_b^osc||^2 and ||delta_b||^2 with b
    print(f"\n{'='*80}")
    print(f"SCALING ANALYSIS: ||D_b^osc||^2 vs phi(b), ||delta_b||^2 vs phi(b)")
    print(f"{'='*80}")
    for p in primes:
        print(f"\n  p={p}:")
        print(f"  {'b':>4} {'phi(b)':>6} {'D_osc^2/phi':>14} {'delta^2/phi':>14} {'delta^2/(phi*b^2)':>18}")
        for b in sorted(all_results[p].keys()):
            r = all_results[p][b]
            phi_b = euler_phi(b) if b > 1 else 1
            if phi_b == 0 or r['delta_sq'] == 0:
                continue
            d_osc_per_phi = float(r['D_osc_sq']) / phi_b
            delta_per_phi = float(r['delta_sq']) / phi_b
            delta_per_phi_b2 = float(r['delta_sq']) / (phi_b * b * b) if b > 0 else 0
            print(f"  {b:>4} {phi_b:>6} {d_osc_per_phi:>14.6f} {delta_per_phi:>14.6f} {delta_per_phi_b2:>18.8f}")

if __name__ == '__main__':
    main()
