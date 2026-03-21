#!/usr/bin/env python3
"""
T_N Operator Eigenvalue Statistics
====================================

This experiment constructs the operator T_N that averages a function over
all Farey-type rotations, and studies whether its eigenvalue statistics
match the GUE (Gaussian Unitary Ensemble) predictions from random matrix theory.

THE OPERATOR:
T_N acts on functions on the Farey fractions of order N. For each Farey
fraction f_j, T_N maps it to a weighted average of values at nearby fractions,
where "nearby" is defined by the Farey neighbor relationship.

WHY THIS MATTERS:
- Montgomery-Odlyzko showed zeta zeros have GUE statistics
- Farey fractions have their own gap distribution (Hall, 1970) — different from GUE
- The question is: does an operator BUILT FROM Farey structure have GUE eigenvalues?
- If yes, this would be a new connection between Farey sequences and random matrix theory
- This would support the Hilbert-Pólya conjecture (RH zeros as eigenvalues of a self-adjoint operator)

WHAT WE COMPUTE:
1. Build a matrix M where M[i,j] = 1 if f_i and f_j are Farey neighbors (|b*c - a*d| = 1)
2. Compute eigenvalues
3. Compute nearest-neighbor spacing distribution
4. Compare to GUE (Wigner surmise) and Poisson predictions
"""

import numpy as np
from math import gcd, pi
from fractions import Fraction
from scipy import linalg
import json
import os


def farey_sequence(N):
    """Generate Farey sequence F_N as sorted list of (numerator, denominator) pairs."""
    fracs = set()
    for q in range(1, N + 1):
        for p in range(0, q + 1):
            if gcd(p, q) == 1:
                fracs.add((p, q))
    return sorted(fracs, key=lambda x: x[0] / x[1])


def are_farey_neighbors(f1, f2):
    """Check if two Farey fractions are neighbors: |b*c - a*d| = 1."""
    a, b = f1
    c, d = f2
    return abs(b * c - a * d) == 1


def build_farey_adjacency(N):
    """Build the adjacency matrix of the Farey neighbor graph."""
    fracs = farey_sequence(N)
    n = len(fracs)
    M = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            if are_farey_neighbors(fracs[i], fracs[j]):
                M[i, j] = 1
                M[j, i] = 1

    return M, fracs


def build_rotation_operator(N):
    """
    Build the rotation-averaging operator T_N.

    T_N[i,j] = 1/|F_N| if there exist k,n with 1 < n ≤ N, gcd(k,n)=1,
    such that f_j = f_i + k/n (mod 1). Weight by 1/n for normalization.

    Simpler version: T_N[i,j] = exp(2πi(f_j - f_i)) summed over Farey rotations.
    We use the real symmetric version: T_N[i,j] = cos(2π(f_j - f_i) * n) averaged.
    """
    fracs = farey_sequence(N)
    n_fracs = len(fracs)
    T = np.zeros((n_fracs, n_fracs))

    # For each Farey fraction k/m with m ≤ N and gcd(k,m)=1,
    # this is a "rotation" of the circle by angle 2πk/m.
    # T averages over all such rotations.
    frac_values = np.array([p / q for p, q in fracs])

    rotations = []
    for m in range(2, N + 1):
        for k in range(1, m):
            if gcd(k, m) == 1:
                rotations.append(k / m)

    for rot in rotations:
        for i in range(n_fracs):
            shifted = (frac_values[i] + rot) % 1.0
            # Find the closest Farey fraction to the shifted value
            diffs = np.abs(frac_values - shifted)
            j = np.argmin(diffs)
            if diffs[j] < 1e-12:  # Exact match (shifted lands on a Farey fraction)
                T[i, j] += 1.0

    # Normalize
    if len(rotations) > 0:
        T /= len(rotations)

    return T, fracs


def wigner_surmise(s):
    """GUE Wigner surmise: P(s) = (32/π²) s² exp(-4s²/π)."""
    return (32 / (pi**2)) * s**2 * np.exp(-4 * s**2 / pi)


def poisson_distribution(s):
    """Poisson level spacing: P(s) = exp(-s)."""
    return np.exp(-s)


def goe_surmise(s):
    """GOE Wigner surmise: P(s) = (π/2) s exp(-πs²/4)."""
    return (pi / 2) * s * np.exp(-pi * s**2 / 4)


def analyze_spacing(eigenvalues, label=""):
    """Analyze nearest-neighbor spacing distribution of eigenvalues."""
    # Sort eigenvalues
    eigs = np.sort(np.real(eigenvalues))

    # Remove duplicates (eigenvalues that are effectively equal)
    eigs = eigs[np.concatenate([[True], np.diff(eigs) > 1e-10])]

    if len(eigs) < 10:
        print(f"  [{label}] Too few distinct eigenvalues ({len(eigs)}) for spacing analysis")
        return None

    # Unfold: normalize so mean spacing = 1
    spacings = np.diff(eigs)
    mean_spacing = np.mean(spacings)
    if mean_spacing <= 0:
        print(f"  [{label}] Mean spacing is zero or negative")
        return None

    normalized_spacings = spacings / mean_spacing

    # Compute statistics
    stats = {
        'label': label,
        'n_eigenvalues': len(eigs),
        'n_spacings': len(normalized_spacings),
        'mean_spacing': float(mean_spacing),
        'var_spacing': float(np.var(normalized_spacings)),
        'min_spacing': float(np.min(normalized_spacings)),
        'max_spacing': float(np.max(normalized_spacings)),
    }

    # The key diagnostic: variance of normalized spacings
    # Poisson: var = 1.0
    # GOE: var ≈ 0.286
    # GUE: var ≈ 0.178
    print(f"  [{label}] {len(eigs)} eigenvalues, {len(normalized_spacings)} spacings")
    print(f"  [{label}] Spacing variance: {stats['var_spacing']:.4f}"
          f"  (Poisson=1.000, GOE=0.286, GUE=0.178)")

    # Level repulsion: fraction of spacings near zero
    small_frac = np.mean(normalized_spacings < 0.1)
    stats['fraction_small'] = float(small_frac)
    print(f"  [{label}] Fraction with s < 0.1: {small_frac:.4f}"
          f"  (Poisson=0.095, GOE≈0.005, GUE≈0.0002)")

    stats['spacings'] = normalized_spacings.tolist()
    return stats


def run_eigenvalue_experiment(max_N=30, output_dir=None):
    """Run the full eigenvalue experiment for Farey operators."""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    print("T_N Operator Eigenvalue Statistics")
    print("=" * 60)

    all_results = {}

    for N in [8, 12, 16, 20, 25, 30]:
        if N > max_N:
            break

        print(f"\n--- N = {N} ---")

        # 1. Adjacency matrix (Farey neighbor graph)
        print(f"  Building Farey adjacency matrix for N={N}...")
        A, fracs = build_farey_adjacency(N)
        print(f"  |F_{N}| = {len(fracs)}, adjacency density = {np.sum(A) / (len(fracs)**2):.4f}")

        eigs_A = linalg.eigvalsh(A)
        stats_A = analyze_spacing(eigs_A, f"Adjacency N={N}")

        # 2. Rotation operator
        print(f"  Building rotation operator T_{N}...")
        T, _ = build_rotation_operator(N)
        print(f"  T_{N} density = {np.sum(np.abs(T) > 1e-10) / (len(fracs)**2):.4f}")

        eigs_T = linalg.eigvalsh(T)
        stats_T = analyze_spacing(eigs_T, f"Rotation N={N}")

        # 3. Laplacian of Farey graph
        D = np.diag(np.sum(A, axis=1))
        L = D - A
        eigs_L = linalg.eigvalsh(L)
        # Remove the zero eigenvalue(s)
        eigs_L_nonzero = eigs_L[eigs_L > 1e-8]
        stats_L = analyze_spacing(eigs_L_nonzero, f"Laplacian N={N}")

        all_results[N] = {
            'farey_size': len(fracs),
            'adjacency': stats_A,
            'rotation': stats_T,
            'laplacian': stats_L,
            'eigenvalues_adjacency': eigs_A.tolist(),
            'eigenvalues_rotation': eigs_T.tolist(),
        }

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY: Spacing variance by N")
    print("=" * 60)
    print(f"{'N':>4s} {'|F_N|':>6s} {'Adj var':>10s} {'Rot var':>10s} {'Lap var':>10s}")
    for N, data in all_results.items():
        adj_var = data['adjacency']['var_spacing'] if data['adjacency'] else float('nan')
        rot_var = data['rotation']['var_spacing'] if data['rotation'] else float('nan')
        lap_var = data['laplacian']['var_spacing'] if data['laplacian'] else float('nan')
        print(f"{N:4d} {data['farey_size']:6d} {adj_var:10.4f} {rot_var:10.4f} {lap_var:10.4f}")

    print(f"\nReference: Poisson=1.000, GOE=0.286, GUE=0.178")

    output_file = os.path.join(output_dir, "eigenvalue_data.json")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nData saved to {output_file}")

    return all_results


def plot_eigenvalue_results(results, output_dir=None):
    """Plot eigenvalue spacing distributions."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    # Find the largest N
    max_N = max(results.keys())
    data = results[max_N]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(f'Eigenvalue Spacing Distributions (N={max_N}, |F_N|={data["farey_size"]})',
                 fontsize=13, fontweight='bold')

    s_range = np.linspace(0, 4, 200)

    for ax, (label, stats_key) in zip(axes, [
        ('Adjacency Matrix', 'adjacency'),
        ('Rotation Operator', 'rotation'),
        ('Graph Laplacian', 'laplacian'),
    ]):
        stats = data[stats_key]
        if stats and 'spacings' in stats:
            spacings = np.array(stats['spacings'])
            ax.hist(spacings, bins=30, density=True, alpha=0.7, color='steelblue',
                    label=f'Data (var={stats["var_spacing"]:.3f})')
            ax.plot(s_range, wigner_surmise(s_range), 'r-', linewidth=2,
                    label='GUE (var=0.178)')
            ax.plot(s_range, goe_surmise(s_range), 'g--', linewidth=2,
                    label='GOE (var=0.286)')
            ax.plot(s_range, poisson_distribution(s_range), 'k:', linewidth=2,
                    label='Poisson (var=1.000)')
            ax.set_xlabel('Normalized spacing s')
            ax.set_ylabel('P(s)')
            ax.set_title(label)
            ax.legend(fontsize=8)
            ax.set_xlim(0, 4)
        else:
            ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center',
                    transform=ax.transAxes)
            ax.set_title(label)

    plt.tight_layout()
    plot_file = os.path.join(output_dir, "eigenvalue_spacing.png")
    plt.savefig(plot_file, dpi=150)
    print(f"  Plot saved to {plot_file}")
    plt.close()


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    results = run_eigenvalue_experiment(max_N=30, output_dir=output_dir)
    plot_eigenvalue_results(results, output_dir=output_dir)
