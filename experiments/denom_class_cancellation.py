#!/usr/bin/env python3
"""
Investigate WHY the cross term <D^osc, delta> is so small compared to CS bound.

The cross term = Σ_f D^osc(f) * delta(f)
= Σ_b Σ_{a/b in F_N} [D(a/b) - D_mean_b] * [(a - pa mod b)/b]

Since D(a/b) = rank(a/b) - |F_N|*(a/b), and D_mean_b = mean of D over denom b,
the oscillatory part is how the rank deviates from its mean within a denominator class.

delta(a/b) = (a - sigma(a))/b where sigma is multiplication by p mod b.

For the cross term to cancel, we need D^osc and delta to be "nearly orthogonal".

HYPOTHESIS: D^osc within denominator b is approximately a smooth function of a/b,
while delta = (a - pa mod b)/b is a "pseudorandom" permutation.
Smooth functions are nearly orthogonal to pseudorandom permutations.

Let's test: decompose D^osc(a/b) into a Fourier series within each denominator class
and see if it's smooth.
"""

from fractions import Fraction
from math import gcd, sqrt, pi, cos, sin
from collections import defaultdict
import cmath

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

def analyze_fourier_within_denom(p):
    """For each denominator b, compute Fourier coefficients of D^osc
    with respect to the group (Z/bZ)*."""
    N = p - 1
    F = farey_sequence(N)
    size_F = len(F)
    rank_map = {f: i for i, f in enumerate(F)}

    D_map = {f: float(rank_map[f]) - size_F * float(f) for f in F}

    denom_groups = defaultdict(list)
    for f in F:
        denom_groups[f.denominator].append(f)

    print(f"\n{'='*70}")
    print(f"FOURIER ANALYSIS OF D^osc WITHIN DENOMINATORS, p={p}")
    print(f"{'='*70}")

    for b in sorted(denom_groups.keys()):
        if b <= 2:
            continue
        fracs_b = denom_groups[b]
        phi_b = len(fracs_b)
        if phi_b < 3:
            continue

        D_vals = [D_map[f] for f in fracs_b]
        D_mean = sum(D_vals) / phi_b
        D_osc = [d - D_mean for d in D_vals]

        # Get the a values (numerators)
        a_vals = [f.numerator for f in fracs_b]

        # Compute "Fourier" coefficients: project onto e^{2pi i k a/b}
        # for k = 1, ..., b-1
        total_energy = sum(d*d for d in D_osc)
        if total_energy < 1e-10:
            continue

        fourier_energies = []
        for k in range(1, b):
            coeff = sum(d * cmath.exp(2j * pi * k * a / b) for d, a in zip(D_osc, a_vals))
            energy = abs(coeff)**2 / phi_b
            fourier_energies.append((k, energy))

        # Sort by energy
        fourier_energies.sort(key=lambda x: -x[1])

        # How much energy is in low frequencies?
        low_k = [k for k in range(1, min(4, b)) ]  # k=1,2,3
        low_energy = sum(e for k, e in fourier_energies if k in low_k or (b-k) in low_k)
        high_energy = total_energy - low_energy

        if b <= 20 or b >= N - 5:
            print(f"\n  b={b}: phi(b)={phi_b}, total ||D_osc||^2={total_energy:.4f}")
            print(f"    Top 3 Fourier modes: {[(k, f'{e:.4f}') for k, e in fourier_energies[:3]]}")
            print(f"    Low-freq energy (k=1,2,3): {low_energy:.4f} ({100*low_energy/total_energy:.1f}%)")
            print(f"    High-freq energy: {high_energy:.4f} ({100*high_energy/total_energy:.1f}%)")

def analyze_delta_fourier(p):
    """Compute Fourier structure of delta within each denominator."""
    N = p - 1

    print(f"\n{'='*70}")
    print(f"FOURIER ANALYSIS OF DELTA WITHIN DENOMINATORS, p={p}")
    print(f"{'='*70}")

    for b in range(3, min(p, 30)):
        if gcd(p, b) != 1:
            continue
        phi_b = euler_phi(b)
        if phi_b < 3:
            continue

        # a coprime to b, in {1, ..., b-1}
        units = [a for a in range(1, b) if gcd(a, b) == 1]
        delta_vals = [(a - (p*a) % b) / b for a in units]

        total_energy = sum(d*d for d in delta_vals)
        if total_energy < 1e-10:
            continue

        # Fourier analysis
        fourier_energies = []
        for k in range(1, b):
            coeff = sum(d * cmath.exp(2j * pi * k * a / b) for d, a in zip(delta_vals, units))
            energy = abs(coeff)**2 / phi_b
            fourier_energies.append((k, energy))

        fourier_energies.sort(key=lambda x: -x[1])

        print(f"\n  b={b}: phi(b)={phi_b}, ||delta||^2={total_energy:.4f}")
        print(f"    Top 3 modes: {[(k, f'{e:.4f}') for k, e in fourier_energies[:3]]}")

def analyze_cross_cancellation_mechanism(p):
    """
    KEY INSIGHT CHECK: The cross term Σ D^osc(a/b) * delta(a/b)
    might cancel because:

    D^osc(a/b) ≈ smooth function of position a/b in [0,1]
    delta(a/b) = (a - pa mod b)/b = arithmetic permutation displacement

    For b not dividing p-1, the map a -> pa mod b is a nontrivial
    permutation of (Z/bZ)*. The displacement (a - pa mod b) has
    character-sum structure.

    Let's explicitly compute: for each b,
    <D^osc, delta>_b = Σ_a D^osc(a/b) * delta(a/b)

    And decompose D^osc ≈ linear + oscillatory.
    The linear part of D is related to a/b, and for the smooth Franel-type discrepancy,
    D(a/b) should be approximately a smooth function of a/b.

    Cross of linear part with delta:
    Σ_a (c_0 + c_1 * a/b) * (a - pa mod b)/b
    = c_1/b^2 * Σ a*(a - pa mod b)
    = c_1/b^2 * [Σ a^2 - p*Σ a^2 + b*Σ a*floor(pa/b)]
    = c_1/b^2 * [(1-p)*S2 + b*Σ a*floor(pa/b)]
    """
    N = p - 1
    F = farey_sequence(N)
    size_F = len(F)
    rank_map = {f: i for i, f in enumerate(F)}
    D_map = {f: float(rank_map[f]) - size_F * float(f) for f in F}

    denom_groups = defaultdict(list)
    for f in F:
        denom_groups[f.denominator].append(f)

    print(f"\n{'='*70}")
    print(f"CROSS TERM DECOMPOSITION for p={p}")
    print(f"{'='*70}")
    print(f"  {'b':>4} {'<D_osc,delta>':>14} {'<D_lin,delta>':>14} {'<D_res,delta>':>14} {'D_osc_norm':>12} {'delta_norm':>12}")

    total_cross = 0
    total_lin_cross = 0
    total_res_cross = 0

    for b in sorted(denom_groups.keys()):
        if b <= 1:
            continue
        fracs_b = denom_groups[b]
        phi_b = len(fracs_b)

        D_vals = [D_map[f] for f in fracs_b]
        a_vals = [float(f) for f in fracs_b]  # positions in [0,1]
        D_mean = sum(D_vals) / phi_b
        D_osc = [d - D_mean for d in D_vals]

        delta_vals = [(f.numerator - (p * f.numerator) % f.denominator) / f.denominator for f in fracs_b]

        # Fit linear to D_osc within this denom class
        # D_osc ≈ alpha * (a/b - mean(a/b))
        pos_mean = sum(a_vals) / phi_b
        pos_centered = [a - pos_mean for a in a_vals]
        var_pos = sum(x*x for x in pos_centered)

        if var_pos > 1e-10:
            alpha = sum(d * x for d, x in zip(D_osc, pos_centered)) / var_pos
            D_lin = [alpha * x for x in pos_centered]
            D_res = [d - l for d, l in zip(D_osc, D_lin)]
        else:
            D_lin = [0] * phi_b
            D_res = list(D_osc)

        cross = sum(d * e for d, e in zip(D_osc, delta_vals))
        lin_cross = sum(d * e for d, e in zip(D_lin, delta_vals))
        res_cross = sum(d * e for d, e in zip(D_res, delta_vals))

        total_cross += cross
        total_lin_cross += lin_cross
        total_res_cross += res_cross

        D_osc_norm = sqrt(sum(d*d for d in D_osc))
        delta_norm = sqrt(sum(d*d for d in delta_vals))

        if b <= 25 or abs(cross) > 1:
            print(f"  {b:>4} {cross:>14.6f} {lin_cross:>14.6f} {res_cross:>14.6f} {D_osc_norm:>12.4f} {delta_norm:>12.4f}")

    print(f"\n  Totals:")
    print(f"    Total cross: {total_cross:.6f}")
    print(f"    Linear part: {total_lin_cross:.6f}")
    print(f"    Residual part: {total_res_cross:.6f}")

def main():
    for p in [17, 23, 37, 53, 71, 97]:
        analyze_cross_cancellation_mechanism(p)

    # Trend: does |cross|/delta^2 converge to 0?
    print(f"\n\n{'='*70}")
    print(f"DOES cross/delta^2 -> 0 as p -> infty?")
    print(f"{'='*70}")
    print(f"{'p':>5} {'cross/delta^2':>14} {'|cross|/sqrt(D*d)':>18}")

    from fractions import Fraction as Fr
    for p in [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]:
        N = p - 1
        F = farey_sequence(N)
        size_F = len(F)
        rank_map = {f: i for i, f in enumerate(F)}

        D_map = {}
        delta_map = {}
        denom_groups = defaultdict(list)

        for f in F:
            D_map[f] = Fr(rank_map[f]) - Fr(size_F) * f
            a, b = f.numerator, f.denominator
            delta_map[f] = Fr(a - (p*a) % b, b)
            denom_groups[f.denominator].append(f)

        D_osc_map = {}
        for b, fracs_b in denom_groups.items():
            D_mean = sum(D_map[f] for f in fracs_b) / len(fracs_b)
            for f in fracs_b:
                D_osc_map[f] = D_map[f] - D_mean

        D_osc_sq = sum(v*v for v in D_osc_map.values())
        delta_sq = sum(v*v for v in delta_map.values())
        cross = sum(D_osc_map[f] * delta_map[f] for f in F)

        if delta_sq > 0:
            r1 = float(cross / delta_sq)
            r2 = abs(float(cross)) / sqrt(float(D_osc_sq) * float(delta_sq))
            print(f"{p:>5} {r1:>14.6f} {r2:>18.6f}")

if __name__ == '__main__':
    main()
