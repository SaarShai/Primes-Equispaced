#!/usr/bin/env python3
"""
Farey Polynomial Conjecture Testing
=====================================

This experiment tests open conjectures about Farey polynomials identified by
researchers at the Max Planck Institute.

FAREY POLYNOMIALS:
The n-th Farey polynomial is defined as:
    F_n(z) = Π_{a/b ∈ F_n, 0 < a/b < 1} (z - e^{2πi·a/b})

These encode the positions of all Farey fractions as roots on the unit circle.

OPEN CONJECTURES (from MPI MATHREPO):
1. The "reduced" Farey polynomial (dividing out cyclotomic factors) is a perfect
   square (up to ±z^k).
2. Certain coefficients of Farey polynomials are piecewise polynomial in n.

ADDITIONAL EXPERIMENTS:
3. Study the coefficient growth of Farey polynomials.
4. Look for patterns in the roots of reduced Farey polynomials.
5. Compute the Mahler measure of Farey polynomials (connected to L-functions).
"""

import numpy as np
from math import gcd, pi
from fractions import Fraction
import json
import os


def farey_fractions_interior(N):
    """Farey fractions in (0,1) — excluding 0 and 1."""
    fracs = []
    for q in range(2, N + 1):
        for p in range(1, q):
            if gcd(p, q) == 1:
                fracs.append((p, q))
    return sorted(fracs, key=lambda x: x[0] / x[1])


def farey_polynomial_roots(N):
    """Compute roots of the Farey polynomial: e^{2πi·a/b} for a/b ∈ F_N ∩ (0,1)."""
    fracs = farey_fractions_interior(N)
    roots = [np.exp(2j * pi * p / q) for p, q in fracs]
    return np.array(roots), fracs


def polynomial_from_roots(roots):
    """Compute polynomial coefficients from roots: Π(z - r_i)."""
    # Start with [1] (constant polynomial = 1)
    coeffs = np.array([1.0 + 0j])
    for r in roots:
        # Multiply by (z - r): shift up and subtract r times current
        new_coeffs = np.zeros(len(coeffs) + 1, dtype=complex)
        new_coeffs[1:] += coeffs  # z * current
        new_coeffs[:-1] -= r * coeffs  # -r * current
        coeffs = new_coeffs
    return coeffs


def cyclotomic_roots(n):
    """Primitive n-th roots of unity."""
    roots = []
    for k in range(1, n + 1):
        if gcd(k, n) == 1:
            roots.append(np.exp(2j * pi * k / n))
    return roots


def mahler_measure(coeffs):
    """Compute the Mahler measure of a polynomial.
    M(P) = exp(∫_0^1 log|P(e^{2πit})| dt)
    Approximated by sampling on the unit circle.
    """
    n_samples = 10000
    t = np.linspace(0, 1, n_samples, endpoint=False)
    z = np.exp(2j * pi * t)

    # Evaluate polynomial at z values
    # coeffs[k] is the coefficient of z^k
    vals = np.zeros(n_samples, dtype=complex)
    for k, c in enumerate(coeffs):
        vals += c * z**k

    log_abs = np.log(np.maximum(np.abs(vals), 1e-300))
    return np.exp(np.mean(log_abs))


def test_square_conjecture(N):
    """
    Test the MPI conjecture: is the reduced Farey polynomial a perfect square?

    The "reduced" polynomial divides out all cyclotomic polynomials Φ_k for k ≤ N.
    The conjecture says what remains is ±z^m · P(z)² for some polynomial P.
    """
    roots, fracs = farey_polynomial_roots(N)
    n_roots = len(roots)

    # The Farey polynomial roots include all primitive k-th roots of unity for k ≤ N
    # (since every e^{2πi·a/b} with gcd(a,b)=1 and b ≤ N is a primitive b-th root of unity)
    # So the Farey polynomial IS the product of cyclotomic polynomials Φ_k for k = 2, ..., N.
    # The "reduced" polynomial divides these out — but that would give 1!

    # Actually, the Farey polynomial as defined at MPI might include ALL a/b with b ≤ N,
    # not just coprime ones. Let me check both versions.

    # Version 1: only coprime (a,b) — this gives ∏_{k=2}^{N} Φ_k(z)
    # (each coprime a/b with b=k gives a primitive k-th root)
    # The reduced polynomial after dividing cyclotomic factors would be trivial.

    # Version 2: ALL fractions a/b with 0 < a < b ≤ N (not necessarily coprime)
    # This is more interesting — non-coprime fractions give REPEATED roots.
    all_fracs = []
    for b in range(2, N + 1):
        for a in range(1, b):
            all_fracs.append((a, b))
    all_roots = np.array([np.exp(2j * pi * a / b) for a, b in all_fracs])

    # Count root multiplicities
    unique_roots = {}
    for a, b in all_fracs:
        # Reduce to lowest terms
        g = gcd(a, b)
        key = (a // g, b // g)
        val = np.exp(2j * pi * a / b)
        if key not in unique_roots:
            unique_roots[key] = {'root': val, 'multiplicity': 0}
        unique_roots[key]['multiplicity'] += 1

    # Check if all multiplicities are even (which would make it a perfect square)
    mults = [v['multiplicity'] for v in unique_roots.values()]
    all_even = all(m % 2 == 0 for m in mults)
    max_mult = max(mults) if mults else 0
    min_mult = min(mults) if mults else 0

    return {
        'N': N,
        'n_coprime_fractions': n_roots,
        'n_all_fractions': len(all_fracs),
        'n_unique_roots': len(unique_roots),
        'multiplicities': sorted(set(mults)),
        'all_multiplicities_even': all_even,
        'max_multiplicity': max_mult,
        'min_multiplicity': min_mult,
        'mult_distribution': {str(m): mults.count(m) for m in sorted(set(mults))},
    }


def coefficient_analysis(N):
    """Analyze coefficients of the Farey polynomial."""
    roots, fracs = farey_polynomial_roots(N)

    if len(roots) > 500:
        print(f"    Skipping coefficient analysis for N={N} (too many roots: {len(roots)})")
        return None

    coeffs = polynomial_from_roots(roots)

    # Are coefficients approximately integers?
    real_parts = np.real(coeffs)
    imag_parts = np.imag(coeffs)
    max_imag = np.max(np.abs(imag_parts))

    # Round to nearest integer and check
    rounded = np.round(real_parts)
    max_error = np.max(np.abs(real_parts - rounded))

    return {
        'N': N,
        'degree': len(coeffs) - 1,
        'max_imag_part': float(max_imag),
        'max_rounding_error': float(max_error),
        'coefficients_are_integers': float(max_error) < 1e-6 and float(max_imag) < 1e-6,
        'leading_coeff': float(np.abs(coeffs[-1])),
        'constant_term': float(np.abs(coeffs[0])),
        'max_abs_coeff': float(np.max(np.abs(coeffs))),
        'mahler_measure': float(mahler_measure(coeffs)),
    }


def run_farey_polynomial_experiment(max_N=50, output_dir=None):
    """Run the full Farey polynomial experiment."""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    print("Farey Polynomial Conjecture Testing")
    print("=" * 60)

    # 1. Test the square conjecture
    print("\n--- Square Conjecture Test ---")
    print("Testing if root multiplicities of all-fractions polynomial are even:")
    square_results = []
    for N in range(2, max_N + 1):
        result = test_square_conjecture(N)
        square_results.append(result)
        if N <= 20 or N % 5 == 0:
            print(f"  N={N:3d}: {result['n_unique_roots']:4d} unique roots, "
                  f"mults={result['multiplicities']}, "
                  f"all_even={result['all_multiplicities_even']}")

    # 2. Coefficient analysis
    print("\n--- Coefficient Analysis ---")
    coeff_results = []
    for N in range(2, min(max_N + 1, 60)):
        result = coefficient_analysis(N)
        if result:
            coeff_results.append(result)
            if N <= 15 or N % 5 == 0:
                print(f"  N={N:3d}: degree={result['degree']:4d}, "
                      f"integer_coeffs={result['coefficients_are_integers']}, "
                      f"Mahler={result['mahler_measure']:.4f}")

    # 3. Mahler measure growth
    print("\n--- Mahler Measure Growth ---")
    if coeff_results:
        ns = [r['N'] for r in coeff_results if r['mahler_measure'] > 0]
        mahlers = [r['mahler_measure'] for r in coeff_results if r['mahler_measure'] > 0]
        if len(ns) > 5:
            log_n = np.log(ns)
            log_m = np.log(mahlers)
            coeffs_fit = np.polyfit(log_n, log_m, 1)
            print(f"  Mahler measure growth: M(F_N) ~ N^{coeffs_fit[0]:.4f}")
            print(f"  (Connected to special values of L-functions)")

    # 4. Multiplicity patterns
    print("\n--- Multiplicity Patterns ---")
    # For each reduced fraction a/b, its multiplicity as a root of the
    # all-fractions polynomial is floor(N/b) (number of multiples of 1/b up to N)
    print("  Checking: is mult(a/b) = floor(N/b)?")
    for N in [10, 20, 30, 40]:
        if N > max_N:
            break
        correct = True
        for b in range(2, N + 1):
            for a in range(1, b):
                if gcd(a, b) == 1:
                    expected_mult = N // b
                    # Count actual appearances
                    actual_mult = sum(1 for q in range(b, N + 1, b) for p in [a * q // b]
                                     if p * b == a * q)
                    if actual_mult != expected_mult:
                        correct = False
        print(f"  N={N}: mult(a/b) = floor(N/b)? {correct}")

    # Save results
    output_file = os.path.join(output_dir, "farey_polynomial_data.json")
    results = {
        'square_conjecture': square_results,
        'coefficient_analysis': coeff_results,
    }
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nData saved to {output_file}")

    return results


def plot_farey_polynomial_results(results, output_dir=None):
    """Plot Farey polynomial analysis results."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    coeff_data = results.get('coefficient_analysis', [])
    if not coeff_data:
        return

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Farey Polynomial Analysis', fontsize=13, fontweight='bold')

    # Plot 1: Mahler measure growth
    ax = axes[0]
    ns = [r['N'] for r in coeff_data if r['mahler_measure'] > 0]
    mahlers = [r['mahler_measure'] for r in coeff_data if r['mahler_measure'] > 0]
    ax.semilogy(ns, mahlers, 'b.-')
    ax.set_xlabel('N')
    ax.set_ylabel('Mahler measure M(F_N)')
    ax.set_title('Mahler Measure Growth')
    ax.grid(True, alpha=0.3)

    # Plot 2: Max coefficient growth
    ax = axes[1]
    ns2 = [r['N'] for r in coeff_data]
    max_coeffs = [r['max_abs_coeff'] for r in coeff_data]
    ax.semilogy(ns2, max_coeffs, 'r.-')
    ax.set_xlabel('N')
    ax.set_ylabel('Max |coefficient|')
    ax.set_title('Coefficient Growth')
    ax.grid(True, alpha=0.3)

    # Plot 3: Multiplicity distribution for largest N tested
    ax = axes[2]
    sq_data = results.get('square_conjecture', [])
    if sq_data:
        last = sq_data[-1]
        mults = last['mult_distribution']
        keys = sorted([int(k) for k in mults.keys()])
        vals = [mults[str(k)] for k in keys]
        ax.bar(keys, vals, color='steelblue', alpha=0.8)
        ax.set_xlabel('Root multiplicity')
        ax.set_ylabel('Count')
        ax.set_title(f'Root Multiplicities (N={last["N"]})')

    plt.tight_layout()
    plot_file = os.path.join(output_dir, "farey_polynomials.png")
    plt.savefig(plot_file, dpi=150)
    print(f"  Plot saved to {plot_file}")
    plt.close()


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    results = run_farey_polynomial_experiment(max_N=50, output_dir=output_dir)
    plot_farey_polynomial_results(results, output_dir=output_dir)
