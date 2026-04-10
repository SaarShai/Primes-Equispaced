#!/usr/bin/env python3
"""
Deep analysis of denominator-class decomposition:
1. Where do negative contributions come from?
2. What is the cumulative sum pattern?
3. Can we bound negative contributions by positive ones?
4. What about grouping: b and p-1-b together?
5. Key: when b | (p-1), delta_b = 0. These are "free" positive terms.
6. What fraction of total comes from b with delta=0 vs delta!=0?
"""

from fractions import Fraction
from math import gcd, sqrt
from collections import defaultdict

def farey_sequence(N):
    fracs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.append(Fraction(a, b))
    fracs.sort()
    return fracs

def euler_phi(n):
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

def compute_all(p):
    N = p - 1
    F = farey_sequence(N)
    size_F = len(F)
    rank_map = {f: i for i, f in enumerate(F)}

    D_map = {f: Fraction(rank_map[f]) - Fraction(size_F) * f for f in F}

    delta_map = {}
    for f in F:
        a, b = f.numerator, f.denominator
        pa_mod_b = (p * a) % b
        delta_map[f] = Fraction(a - pa_mod_b, b)

    denom_groups = defaultdict(list)
    for f in F:
        denom_groups[f.denominator].append(f)

    results = {}
    for b in sorted(denom_groups.keys()):
        fracs_b = denom_groups[b]
        D_vals = [D_map[f] for f in fracs_b]
        delta_vals = [delta_map[f] for f in fracs_b]
        D_mean = sum(D_vals) / len(D_vals)
        D_osc = [d - D_mean for d in D_vals]

        D_osc_sq = sum(d*d for d in D_osc)
        delta_sq = sum(d*d for d in delta_vals)
        cross = sum(d*e for d, e in zip(D_osc, delta_vals))
        net = 2 * cross + delta_sq
        sum_delta = sum(delta_vals)

        results[b] = {
            'phi_b': len(fracs_b),
            'D_osc_sq': D_osc_sq,
            'delta_sq': delta_sq,
            'cross': cross,
            'net': net,
            'sum_delta': sum_delta,
            'D_mean': D_mean,
        }

    return results, size_F

def analyze_divisibility(p, results):
    """Key insight: when b | (p-1), multiplication by p is the identity mod b,
    so delta(a/b) = (a - pa mod b)/b = (a-a)/b = 0 for all a.
    These denominators contribute net = 0 (both delta_sq and cross are 0).

    When p ≡ 1 mod b, same thing.
    When p ≡ -1 mod b (i.e. b | p+1), delta(a/b) = (a - (-a mod b))/b = (2a-b)/b or similar.
    """
    N = p - 1
    print(f"\n{'='*70}")
    print(f"p = {p}, N = {N}")
    print(f"{'='*70}")

    # Classify denominators
    zero_delta = []  # b where all delta = 0
    pos_net = []
    neg_net = []

    total_pos = Fraction(0)
    total_neg = Fraction(0)
    total_BC = Fraction(0)

    for b in sorted(results.keys()):
        r = results[b]
        net = r['net']
        total_BC += net

        if r['delta_sq'] == 0:
            zero_delta.append(b)
        elif net > 0:
            pos_net.append(b)
            total_pos += net
        elif net < 0:
            neg_net.append(b)
            total_neg += net
        # net == 0 with delta != 0 goes to neither

    print(f"\n  Denominators with delta=0 (p ≡ 1 mod b): {zero_delta}")
    print(f"    These are divisors of p-1={N}: ", [b for b in zero_delta if N % b == 0])

    print(f"\n  Positive contributors: {pos_net}")
    print(f"    Total positive: {float(total_pos):.6f}")

    print(f"\n  Negative contributors: {neg_net}")
    print(f"    Total negative: {float(total_neg):.6f}")

    print(f"\n  B+C = {float(total_BC):.6f}")
    print(f"  Ratio |neg|/pos = {float(-total_neg/total_pos):.6f}" if total_pos > 0 else "")

    # Key: for negative contributors, show why they're negative
    print(f"\n  Negative contributor details:")
    for b in neg_net:
        r = results[b]
        p_mod_b = p % b
        print(f"    b={b}: p mod b = {p_mod_b}, cross={float(r['cross']):.4f}, "
              f"delta_sq={float(r['delta_sq']):.4f}, net={float(r['net']):.4f}, "
              f"|cross|/delta_sq = {float(abs(r['cross'])/r['delta_sq']):.4f}")

def analyze_complementary_pairs(p, results):
    """Check if pairing b with (p-1)/gcd(b, p-1) or other natural pairs helps."""
    N = p - 1
    print(f"\n--- Complementary pair analysis for p={p} ---")

    # Try pairing b with N+1-b = p-b (note: p-b might not be in range)
    # Actually try: for each b, pair with the "complementary" denominator

    # Better: cumulative sum from b=2 upward
    cum = Fraction(0)
    print(f"  {'b':>4} {'net':>14} {'cumulative':>14}")
    for b in sorted(results.keys()):
        if b == 1:
            continue  # skip b=1 (special case)
        r = results[b]
        cum += r['net']
        marker = " ***" if r['net'] < 0 else ""
        print(f"  {b:>4} {float(r['net']):>14.6f} {float(cum):>14.6f}{marker}")

def analyze_cross_term_structure(p, results):
    """
    The cross term <D_b^osc, delta_b> can be negative.
    Key question: is |<D_b^osc, delta_b>| ≤ delta_sq/2 always?
    If so, net = 2*cross + delta_sq ≥ 0.

    By Cauchy-Schwarz: |cross| ≤ ||D_osc|| * ||delta||
    So net ≥ delta_sq - 2*||D_osc||*||delta|| = ||delta||(||delta|| - 2*||D_osc||)
    This is ≥ 0 iff ||D_osc|| ≤ ||delta||/2.

    But we KNOW this fails. So need different approach.

    Alternative: net = ||D_osc + delta||^2 - ||D_osc||^2
    = ||D_osc||^2 + 2*cross + delta_sq - ||D_osc||^2 = 2*cross + delta_sq. OK same.

    BUT: the TOTAL sum might still be analyzable.
    Total B+C = Σ_b [2*cross_b + delta_sq_b]
    = Σ_b delta_sq_b + 2*Σ_b cross_b
    = ||delta||^2_total + 2*<D^osc, delta>_total

    And <D^osc, delta>_total = Σ_b <D_b^osc, delta_b>
    But D^osc and delta live in DIFFERENT decompositions...
    Actually no: D_b^osc and delta_b are BOTH restricted to denominator b fractions.
    So <D^osc, delta>_total = Σ_{all fractions} D^osc(f)*delta(f).
    """
    print(f"\n--- Cross term structure for p={p} ---")
    total_cross = sum(r['cross'] for r in results.values())
    total_delta_sq = sum(r['delta_sq'] for r in results.values())
    total_D_osc_sq = sum(r['D_osc_sq'] for r in results.values())

    print(f"  Σ ||D_osc||^2 = {float(total_D_osc_sq):.6f}")
    print(f"  Σ ||delta||^2 = {float(total_delta_sq):.6f}")
    print(f"  Σ <D_osc, delta> = {float(total_cross):.6f}")
    print(f"  B+C = 2*cross + delta_sq = {float(2*total_cross + total_delta_sq):.6f}")

    # By global Cauchy-Schwarz:
    # |Σ cross_b| ≤ sqrt(Σ D_osc_sq) * sqrt(Σ delta_sq)
    cs_bound = sqrt(float(total_D_osc_sq)) * sqrt(float(total_delta_sq))
    print(f"  CS bound on |total cross|: {cs_bound:.6f}")
    print(f"  Actual |total cross|: {abs(float(total_cross)):.6f}")
    print(f"  CS slack: {cs_bound - abs(float(total_cross)):.6f}")

    # For B+C > 0, need 2*cross > -delta_sq, i.e., cross > -delta_sq/2
    # This holds if total_cross > -total_delta_sq/2
    print(f"  Need: cross > -{float(total_delta_sq/2):.6f}")
    print(f"  Have: cross = {float(total_cross):.6f}")
    print(f"  Margin: {float(total_cross + total_delta_sq/2):.6f}")

def analyze_delta_sq_formula(p):
    """
    For prime p and denominator b with gcd(p,b)=1:
    sigma: a -> pa mod b is a permutation of (Z/bZ)*.
    delta(a/b) = (a - sigma(a))/b
    ||delta_b||^2 = (1/b^2) Σ_{a in (Z/bZ)*} (a - sigma(a))^2

    = (1/b^2) [Σ a^2 + Σ sigma(a)^2 - 2 Σ a*sigma(a)]
    = (1/b^2) [2*S2 - 2*Σ a*(pa mod b)]
    where S2 = Σ_{a coprime to b} a^2

    Key: Σ a*(pa mod b) = Σ a*sigma(a) is a character sum!
    If sigma(a) = pa mod b, then Σ a*sigma(a) = p * Σ a^2 mod ... no, not quite.

    Actually: Σ_{gcd(a,b)=1} a * (pa mod b) where "pa mod b" means the representative in {0,...,b-1}.
    Since gcd(p,b)=1, pa mod b = pa - b*floor(pa/b), so
    Σ a*(pa mod b) = p*Σ a^2 - b * Σ a*floor(pa/b)

    The first term is p*S2. The second involves Dedekind-like sums.
    """
    N = p - 1
    print(f"\n--- Delta^2 formula analysis for p={p} ---")
    for b in range(2, p):
        if gcd(p, b) != 1:
            continue

        S2 = sum(a*a for a in range(1, b) if gcd(a, b) == 1)
        cross_sum = sum(a * ((p*a) % b) for a in range(1, b) if gcd(a, b) == 1)
        delta_sq = Fraction(2*S2 - 2*cross_sum, b*b)

        phi_b = euler_phi(b)
        # For random permutation, E[Σ a*sigma(a)] = (1/phi(b)) * S2
        # (each sigma(a) averages to mean of units)
        # Actually E[a*sigma(a)] = a * mean, mean = S1/phi(b) where S1 = Σ units
        S1 = sum(a for a in range(1, b) if gcd(a, b) == 1)
        random_cross = Fraction(S1 * S1, phi_b)  # Σ a * E[sigma(a)] = Σ a * S1/phi_b = S1^2/phi_b
        random_delta_sq = Fraction(2*S2 - 2*int(random_cross), b*b)  # approximate

        actual_ratio = float(cross_sum) / S2 if S2 > 0 else 0

        if b <= 15 or delta_sq == 0:
            print(f"  b={b}: S2={S2}, cross_sum={cross_sum}, cross/S2={actual_ratio:.4f}, "
                  f"p mod b={p%b}, delta_sq={float(delta_sq):.6f}")

def analyze_when_delta_zero(p):
    """When is delta identically 0 for denominator b?
    delta(a/b) = (a - pa mod b)/b
    If p ≡ 1 (mod b), then pa mod b = a, so delta = 0 for all a.
    This happens iff b | (p-1).

    When p ≡ -1 (mod b), pa mod b = (-a) mod b = b-a.
    Then delta(a/b) = (a - (b-a))/b = (2a-b)/b.
    ||delta||^2 = Σ (2a-b)^2/b^2
    """
    N = p - 1
    print(f"\n--- When delta=0 analysis for p={p} ---")
    print(f"  p-1 = {N}, divisors of p-1: ", [d for d in range(1, N+1) if N % d == 0])

    count_zero = 0
    count_nonzero = 0
    phi_zero = 0
    phi_nonzero = 0

    for b in range(2, p):
        if p % b == 1:  # p ≡ 1 mod b, i.e., b | (p-1)
            phi_b = euler_phi(b)
            phi_zero += phi_b
            count_zero += 1
        else:
            phi_b = euler_phi(b)
            phi_nonzero += phi_b
            count_nonzero += 1

    total_phi = phi_zero + phi_nonzero
    print(f"  Denominators with delta=0: {count_zero} (covering {phi_zero} fractions, {100*phi_zero/total_phi:.1f}%)")
    print(f"  Denominators with delta!=0: {count_nonzero} (covering {phi_nonzero} fractions, {100*phi_nonzero/total_phi:.1f}%)")

def main():
    primes = [13, 17, 23, 29, 37, 41, 43, 47, 53, 59]

    for p in primes:
        results, size_F = compute_all(p)
        analyze_divisibility(p, results)
        analyze_complementary_pairs(p, results)
        if p <= 37:
            analyze_cross_term_structure(p, results)
        analyze_when_delta_zero(p)

    # Extended: check B+C positivity up to larger primes
    print(f"\n\n{'='*70}")
    print(f"B+C TOTALS AND NEGATIVE FRACTION")
    print(f"{'='*70}")
    print(f"{'p':>5} {'B+C':>14} {'|neg|':>14} {'pos':>14} {'|neg|/pos':>10} {'#neg_b':>7}")

    for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]:
        results, size_F = compute_all(p)
        total_pos = Fraction(0)
        total_neg = Fraction(0)
        neg_count = 0
        for b, r in results.items():
            if b == 1:
                continue
            if r['net'] > 0:
                total_pos += r['net']
            elif r['net'] < 0:
                total_neg += r['net']
                neg_count += 1
        total_BC = total_pos + total_neg
        ratio = float(-total_neg / total_pos) if total_pos > 0 else 0
        print(f"{p:>5} {float(total_BC):>14.4f} {float(-total_neg):>14.4f} {float(total_pos):>14.4f} {ratio:>10.4f} {neg_count:>7}")

if __name__ == '__main__':
    main()
