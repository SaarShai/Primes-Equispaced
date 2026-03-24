#!/usr/bin/env python3
"""
GEOMETRIC EXPLORER: Novel geometric structures in Farey sequences and primes
=============================================================================

Explores 6 geometric directions:
1. Farey Walk Shape (complex exponential walks)
2. Prime Fingerprints (binary gap-filling vectors)
3. Angular Momentum Spectrum (power spectrum |L_m|^2)
4. Voronoi Entropy on the Circle
5. Modular Inverse Map as Geometry
6. Geodesics / Triangulation Changes

Generates publication-quality figures in ../figures/
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize, LinearSegmentedColormap
import matplotlib.cm as cm
from math import gcd, log, pi, sqrt, ceil
from fractions import Fraction
from collections import defaultdict
import json

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
FIG_DIR = os.path.join(ROOT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Style
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except Exception:
    try:
        plt.style.use('seaborn-whitegrid')
    except Exception:
        pass

DPI = 200

# Color palette
C_RED = '#E63946'
C_BLUE = '#457B9D'
C_DARK = '#264653'
C_ORANGE = '#F4A261'
C_GREEN = '#2A9D8F'
C_PURPLE = '#7B2D8E'

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]

def sieve_mu(limit):
    """Mobius function via sieve."""
    mu = np.ones(limit + 1, dtype=np.int64)
    is_p = np.ones(limit + 1, dtype=bool)
    is_p[0] = is_p[1] = False
    for p in range(2, limit + 1):
        if is_p[p]:
            for m in range(p, limit + 1, p):
                if m != p: is_p[m] = False
                mu[m] *= -1
            p2 = p * p
            for m in range(p2, limit + 1, p2):
                mu[m] = 0
    return mu

def mertens_function(limit):
    """Compute M(n) = sum of mu(k) for k=1..n."""
    mu = sieve_mu(limit)
    M = np.cumsum(mu)
    M[0] = 0
    return M

def farey_sequence(N):
    """Generate F_N as sorted list of floats (fast version)."""
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append(a / b)
    fracs.sort()
    return fracs

def farey_sequence_frac(N):
    """Generate F_N as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def farey_mediant_build(N):
    """Build F_N using the mediant property (faster, returns (a,b) pairs)."""
    # Start with F_1 = {0/1, 1/1}
    fracs = [(0, 1), (1, 1)]
    for n in range(2, N + 1):
        new_fracs = []
        for i in range(len(fracs) - 1):
            a1, b1 = fracs[i]
            a2, b2 = fracs[i + 1]
            new_fracs.append((a1, b1))
            if b1 + b2 == n:
                new_fracs.append((a1 + a2, b1 + b2))
        new_fracs.append(fracs[-1])
        fracs = new_fracs
    return fracs

def wobble(N):
    """Compute W(N) = sum of (f_j - j/(n-1))^2."""
    F = farey_sequence(N)
    n = len(F)
    if n <= 1: return 0.0
    return sum((F[j] - j / (n - 1))**2 for j in range(n))

def save_fig(fig, name):
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {path}")
    return path

# ===========================================================================
# EXPLORATION 1: FAREY WALK SHAPE
# ===========================================================================

def farey_walk(N):
    """
    Compute the Farey walk z_j = sum_{k<=j} exp(2*pi*i*f_k)
    where f_k are the Farey fractions in F_N.
    Returns array of complex positions.
    """
    F = farey_sequence(N)
    steps = np.exp(2j * np.pi * np.array(F))
    walk = np.cumsum(steps)
    return np.concatenate([[0], walk]), F

def walk_metrics(walk):
    """Compute geometric metrics of a walk in the complex plane."""
    max_dist = np.max(np.abs(walk))

    # Total curvature: sum of absolute turning angles
    if len(walk) < 3:
        return {'max_dist': max_dist, 'winding': 0, 'curvature': 0, 'fractal_dim': 1}

    diffs = np.diff(walk)
    angles = np.angle(diffs)
    turns = np.diff(angles)
    # Wrap to [-pi, pi]
    turns = (turns + np.pi) % (2 * np.pi) - np.pi
    total_curvature = np.sum(np.abs(turns))
    winding = np.sum(turns) / (2 * np.pi)

    # Fractal dimension estimate (box-counting approximation)
    # Use the displacement vs step relationship
    n = len(walk)
    total_length = np.sum(np.abs(diffs))
    diameter = max_dist * 2 if max_dist > 0 else 1
    # D = log(N) / log(N * diameter / total_length) approximately
    if total_length > 0 and diameter > 0 and n > 1:
        # Divider method approximation
        fractal_dim = log(n) / log(n * diameter / total_length) if n * diameter / total_length > 1 else 1.0
    else:
        fractal_dim = 1.0

    return {
        'max_dist': max_dist,
        'winding': winding,
        'curvature': total_curvature,
        'fractal_dim': fractal_dim,
        'total_length': total_length,
        'diameter': diameter
    }

def explore_farey_walks():
    """
    EXPLORATION 1: Farey Walk Shape
    Plot walks for primes with M(p) > 0 and M(p) < 0.
    """
    print("\n" + "="*70)
    print("EXPLORATION 1: FAREY WALK SHAPE")
    print("="*70)

    target_primes = [11, 23, 47, 97, 197, 499]
    M = mertens_function(600)

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Farey Walks in the Complex Plane\n'
                 r'$z_j = \sum_{k \leq j} e^{2\pi i f_k}$, $f_k \in \mathcal{F}_p$',
                 fontsize=16, fontweight='bold')

    metrics_data = []

    for idx, p in enumerate(target_primes):
        ax = axes[idx // 3][idx % 3]
        walk, F = farey_walk(p)
        m = walk_metrics(walk)
        m['p'] = p
        m['M_p'] = int(M[p])
        m['n_fracs'] = len(F)
        metrics_data.append(m)

        # Color by Mertens sign
        color = C_RED if M[p] > 0 else (C_BLUE if M[p] < 0 else C_DARK)

        # Plot walk with gradient coloring
        points = np.array([(z.real, z.imag) for z in walk])
        segments = np.array([[points[i], points[i+1]] for i in range(len(points)-1)])

        t = np.linspace(0, 1, len(segments))
        colors_arr = plt.cm.viridis(t)

        lc = LineCollection(segments, colors=colors_arr, linewidths=1.2, alpha=0.8)
        ax.add_collection(lc)

        # Mark start and end
        ax.plot(0, 0, 'o', color=C_GREEN, markersize=8, zorder=5, label='Start')
        ax.plot(walk[-1].real, walk[-1].imag, '*', color=C_RED,
                markersize=12, zorder=5, label=f'End (M={int(M[p])}+2)')

        # Auto-scale
        margin = 0.1 * m['max_dist'] if m['max_dist'] > 0 else 1
        ax.set_xlim(points[:,0].min() - margin, points[:,0].max() + margin)
        ax.set_ylim(points[:,1].min() - margin, points[:,1].max() + margin)
        ax.set_aspect('equal')

        mertens_str = f'M(p)={int(M[p])}'
        ax.set_title(f'p = {p}  ({mertens_str})\n'
                     f'|F_p| = {len(F)}, max dist = {m["max_dist"]:.2f}',
                     fontsize=11, color=color, fontweight='bold')
        ax.legend(fontsize=8, loc='upper right')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig, 'fig_farey_walks.png')

    # Print metrics table
    print("\n  Farey Walk Metrics:")
    print(f"  {'p':>5} {'M(p)':>5} {'|F_p|':>6} {'MaxDist':>8} {'Winding':>8} "
          f"{'Curvature':>10} {'FracDim':>8} {'Length':>8}")
    print("  " + "-"*72)
    for m in metrics_data:
        print(f"  {m['p']:5d} {m['M_p']:5d} {m['n_fracs']:6d} {m['max_dist']:8.3f} "
              f"{m['winding']:8.3f} {m['curvature']:10.2f} {m['fractal_dim']:8.4f} "
              f"{m['total_length']:8.2f}")

    # NOVEL CHECK: correlation between walk shape and M(p)
    mvals = [m['M_p'] for m in metrics_data]
    maxds = [m['max_dist'] for m in metrics_data]
    winds = [m['winding'] for m in metrics_data]
    if len(set(mvals)) > 1:
        corr_md = np.corrcoef(mvals, maxds)[0,1]
        corr_wd = np.corrcoef(mvals, winds)[0,1]
        print(f"\n  Correlation M(p) vs MaxDist: {corr_md:.4f}")
        print(f"  Correlation M(p) vs Winding: {corr_wd:.4f}")

    return metrics_data

# ===========================================================================
# EXPLORATION 2: PRIME FINGERPRINTS
# ===========================================================================

def get_gaps(N):
    """Return the list of gap sizes in F_N."""
    F = farey_sequence(N)
    return [F[i+1] - F[i] for i in range(len(F) - 1)]

def prime_fingerprint(p, F_prev):
    """
    Binary vector: for each gap in F_{p-1}, does a fraction k/p land there?
    Returns binary array of length |gaps(F_{p-1})|.
    """
    n = len(F_prev)
    gaps_filled = np.zeros(n - 1, dtype=int)

    # For each k/p, find which gap it lands in
    new_fracs = sorted([k / p for k in range(1, p)])
    j = 0
    for f in new_fracs:
        while j < n - 1 and F_prev[j + 1] <= f:
            j += 1
        if j < n - 1:
            gaps_filled[j] = 1

    return gaps_filled

def fingerprint_distance(fp1, fp2):
    """Compute normalized Hamming distance between two fingerprints."""
    # Pad shorter to match longer
    maxlen = max(len(fp1), len(fp2))
    a = np.zeros(maxlen)
    b = np.zeros(maxlen)
    a[:len(fp1)] = fp1
    b[:len(fp2)] = fp2
    return np.sum(a != b) / maxlen

def explore_prime_fingerprints():
    """
    EXPLORATION 2: Prime Fingerprints
    Compare gap-filling patterns across primes.
    """
    print("\n" + "="*70)
    print("EXPLORATION 2: PRIME FINGERPRINTS")
    print("="*70)

    # Compute fingerprints for primes up to ~100
    primes = primes_up_to(100)
    M = mertens_function(110)

    fingerprints = {}
    delta_ws = {}

    for p in primes:
        F_prev = farey_sequence(p - 1)
        fp = prime_fingerprint(p, F_prev)
        fingerprints[p] = fp

        # Compute delta_W
        W_prev = wobble(p - 1)
        W_cur = wobble(p)
        delta_ws[p] = W_prev - W_cur

    # Twin primes comparison
    twin_pairs = [(p, p+2) for p in primes if p+2 in primes and p+2 <= 100]
    print(f"\n  Twin prime pairs found: {twin_pairs}")

    twin_dists = []
    for p, q in twin_pairs:
        d = fingerprint_distance(fingerprints[p], fingerprints[q])
        twin_dists.append(d)
        print(f"    ({p},{q}): Hamming dist = {d:.4f}")

    # Non-twin consecutive primes
    non_twin_dists = []
    for i in range(len(primes) - 1):
        p, q = primes[i], primes[i+1]
        if q - p != 2:
            d = fingerprint_distance(fingerprints[p], fingerprints[q])
            non_twin_dists.append(d)

    print(f"\n  Mean twin-prime fingerprint distance: {np.mean(twin_dists):.4f}")
    print(f"  Mean non-twin consecutive distance:   {np.mean(non_twin_dists):.4f}")

    # Residue class mod 6 comparison
    mod6_groups = defaultdict(list)
    for p in primes:
        if p > 3:
            mod6_groups[p % 6].append(p)

    print(f"\n  Primes mod 6:")
    for r, ps in sorted(mod6_groups.items()):
        print(f"    {r} mod 6: {ps[:10]}...")

    # Within-class vs between-class distances
    within_dists = []
    between_dists = []

    for r1 in mod6_groups:
        ps = mod6_groups[r1]
        for i in range(len(ps)):
            for j in range(i+1, min(len(ps), i+5)):
                d = fingerprint_distance(fingerprints[ps[i]], fingerprints[ps[j]])
                within_dists.append(d)

    keys = sorted(mod6_groups.keys())
    if len(keys) >= 2:
        for p1 in mod6_groups[keys[0]][:8]:
            for p2 in mod6_groups[keys[1]][:8]:
                d = fingerprint_distance(fingerprints[p1], fingerprints[p2])
                between_dists.append(d)

    print(f"\n  Within residue class distance:  {np.mean(within_dists):.4f} +/- {np.std(within_dists):.4f}")
    print(f"  Between residue class distance: {np.mean(between_dists):.4f} +/- {np.std(between_dists):.4f}")

    # Correlation: fingerprint density vs delta_W
    fp_densities = []
    dw_vals = []
    for p in primes:
        if p >= 5:
            fp_densities.append(np.mean(fingerprints[p]))
            dw_vals.append(delta_ws[p])

    corr = np.corrcoef(fp_densities, dw_vals)[0,1] if len(fp_densities) > 2 else 0
    print(f"\n  Correlation(fingerprint density, delta_W): {corr:.4f}")

    # ---- VISUALIZATION ----
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Prime Fingerprints: Gap-Filling Patterns',
                 fontsize=16, fontweight='bold')

    # Panel 1: Fingerprint heatmap for small primes
    ax = axes[0][0]
    small_primes = [p for p in primes if p <= 31]
    max_len = max(len(fingerprints[p]) for p in small_primes)
    fp_matrix = np.zeros((len(small_primes), max_len))
    for i, p in enumerate(small_primes):
        fp = fingerprints[p]
        fp_matrix[i, :len(fp)] = fp

    im = ax.imshow(fp_matrix, aspect='auto', cmap='YlOrRd', interpolation='nearest')
    ax.set_yticks(range(len(small_primes)))
    ax.set_yticklabels([str(p) for p in small_primes])
    ax.set_xlabel('Gap index in F_{p-1}')
    ax.set_ylabel('Prime p')
    ax.set_title('Fingerprint Heatmap (gaps filled = orange)')
    plt.colorbar(im, ax=ax, label='Filled')

    # Panel 2: Distance comparison (twin vs non-twin)
    ax = axes[0][1]
    data_to_plot = []
    labels_to_plot = []
    if twin_dists:
        data_to_plot.append(twin_dists)
        labels_to_plot.append(f'Twin primes\n(n={len(twin_dists)})')
    if non_twin_dists:
        data_to_plot.append(non_twin_dists)
        labels_to_plot.append(f'Non-twin\n(n={len(non_twin_dists)})')
    if within_dists:
        data_to_plot.append(within_dists)
        labels_to_plot.append(f'Same mod 6\n(n={len(within_dists)})')
    if between_dists:
        data_to_plot.append(between_dists)
        labels_to_plot.append(f'Diff mod 6\n(n={len(between_dists)})')

    bp = ax.boxplot(data_to_plot, tick_labels=labels_to_plot, patch_artist=True)
    colors_box = [C_RED, C_BLUE, C_GREEN, C_ORANGE]
    for patch, color in zip(bp['boxes'], colors_box[:len(data_to_plot)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_ylabel('Fingerprint Distance')
    ax.set_title('Fingerprint Distances by Category')

    # Panel 3: Fingerprint density vs delta_W
    ax = axes[1][0]
    ps_plot = [p for p in primes if p >= 5]
    fp_dens = [np.mean(fingerprints[p]) for p in ps_plot]
    dw_plot = [delta_ws[p] for p in ps_plot]
    m_vals = [int(M[p]) for p in ps_plot]

    colors_scatter = [C_RED if m > 0 else C_BLUE for m in m_vals]
    ax.scatter(fp_dens, dw_plot, c=colors_scatter, s=60, alpha=0.7, edgecolors='black', linewidth=0.5)
    for i, p in enumerate(ps_plot):
        ax.annotate(str(p), (fp_dens[i], dw_plot[i]), fontsize=7, alpha=0.7)
    ax.set_xlabel('Fingerprint Density (fraction of gaps filled)')
    ax.set_ylabel(r'$\Delta W(p) = W(p-1) - W(p)$')
    ax.set_title(f'Density vs Delta W  (corr = {corr:.3f})')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    # Panel 4: Filling fraction convergence
    ax = axes[1][1]
    primes_ext = primes_up_to(200)
    fill_fracs = []
    for p in primes_ext:
        F_prev = farey_sequence(p - 1)
        fp = prime_fingerprint(p, F_prev)
        fill_fracs.append(np.mean(fp))

    ax.plot(primes_ext, fill_fracs, 'o-', color=C_DARK, markersize=4, linewidth=1)
    ax.set_xlabel('Prime p')
    ax.set_ylabel('Fraction of gaps filled')
    ax.set_title('Gap-Filling Rate Convergence')
    ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='All gaps filled')
    ax.legend()

    plt.tight_layout()
    save_fig(fig, 'fig_prime_fingerprints.png')

    return {
        'twin_dist_mean': np.mean(twin_dists) if twin_dists else None,
        'non_twin_dist_mean': np.mean(non_twin_dists) if non_twin_dists else None,
        'within_mod6_mean': np.mean(within_dists) if within_dists else None,
        'between_mod6_mean': np.mean(between_dists) if between_dists else None,
        'density_deltaW_corr': corr
    }

# ===========================================================================
# EXPLORATION 3: ANGULAR MOMENTUM SPECTRUM
# ===========================================================================

def angular_momentum_spectrum(N, max_m=None):
    """
    Compute |L_m|^2 = |sum_j exp(2*pi*i*m*f_j)|^2 for the Farey sequence F_N.
    This is the power spectrum of the point set {f_j} at frequency m.
    """
    F = np.array(farey_sequence(N))
    if max_m is None:
        max_m = N
    spectrum = np.zeros(max_m)
    for m in range(1, max_m + 1):
        L = np.sum(np.exp(2j * np.pi * m * F))
        spectrum[m - 1] = abs(L)**2
    return spectrum

def explore_angular_spectrum():
    """
    EXPLORATION 3: Angular Momentum Spectrum
    Compute and visualize the power spectrum for several primes.
    """
    print("\n" + "="*70)
    print("EXPLORATION 3: ANGULAR MOMENTUM SPECTRUM")
    print("="*70)

    target_primes = [11, 23, 47, 97]
    M = mertens_function(200)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(r'Angular Momentum Spectrum: $|L_m|^2 = |\sum_j e^{2\pi i m f_j}|^2$',
                 fontsize=16, fontweight='bold')

    spectra_data = {}

    for idx, p in enumerate(target_primes):
        ax = axes[idx // 2][idx % 2]
        max_m = min(p * 2, 200)
        spectrum = angular_momentum_spectrum(p, max_m=max_m)
        spectra_data[p] = spectrum

        ms = np.arange(1, max_m + 1)
        color = C_RED if M[p] > 0 else C_BLUE

        ax.semilogy(ms, spectrum + 1, '-', color=color, linewidth=0.8, alpha=0.7)

        # Highlight m = p (the prime itself)
        if p <= max_m:
            ax.axvline(x=p, color=C_ORANGE, linestyle='--', alpha=0.7, label=f'm = p = {p}')
            ax.plot(p, spectrum[p-1] + 1, 'v', color=C_ORANGE, markersize=10, zorder=5)

        # Highlight m = 1
        ax.plot(1, spectrum[0] + 1, 's', color=C_GREEN, markersize=8, zorder=5, label=f'|L_1|^2 = {spectrum[0]:.1f}')

        # |F_p|
        n_F = len(farey_sequence(p))
        ax.axhline(y=n_F, color='gray', linestyle=':', alpha=0.5, label=f'|F_p| = {n_F}')

        ax.set_xlabel('Frequency m')
        ax.set_ylabel(r'$|L_m|^2 + 1$ (log scale)')
        ax.set_title(f'p = {p}, M(p) = {int(M[p])}', fontweight='bold', color=color)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Print key values
        peak_m = np.argmax(spectrum) + 1
        print(f"\n  p = {p}: |F_p| = {n_F}, M(p) = {int(M[p])}")
        print(f"    |L_1|^2 = {spectrum[0]:.4f}")
        print(f"    |L_p|^2 = {spectrum[p-1]:.4f}" if p <= max_m else "    (p > max_m)")
        print(f"    Peak at m = {peak_m}, |L_peak|^2 = {spectrum[peak_m-1]:.4f}")
        print(f"    Mean |L_m|^2 = {np.mean(spectrum):.4f}")

    plt.tight_layout()
    save_fig(fig, 'fig_angular_spectrum.png')

    # Summary plot: how |L_1|^2 relates to M(p)
    all_primes = primes_up_to(150)
    L1_vals = []
    M_vals = []
    M = mertens_function(160)

    for p in all_primes:
        if p >= 5:
            F = np.array(farey_sequence(p))
            L1 = abs(np.sum(np.exp(2j * np.pi * F)))**2
            L1_vals.append(L1)
            M_vals.append(int(M[p]))

    fig2, ax = plt.subplots(figsize=(10, 6))
    colors_scat = [C_RED if m > 0 else C_BLUE for m in M_vals]
    ax.scatter(M_vals, L1_vals, c=colors_scat, s=50, alpha=0.7, edgecolors='black', linewidth=0.5)

    # Annotate some
    ps_annot = [p for p in all_primes if p >= 5]
    for i, p in enumerate(ps_annot):
        if p in [5, 11, 23, 47, 97]:
            ax.annotate(str(p), (M_vals[i], L1_vals[i]), fontsize=9, fontweight='bold')

    corr = np.corrcoef(M_vals, L1_vals)[0,1] if len(M_vals) > 2 else 0
    ax.set_xlabel('M(p)', fontsize=13)
    ax.set_ylabel(r'$|L_1|^2$', fontsize=13)
    ax.set_title(f'First Angular Momentum vs Mertens Function\n(correlation = {corr:.4f})',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_fig(fig2, 'fig_L1_vs_mertens.png')

    print(f"\n  Correlation |L_1|^2 vs M(p): {corr:.4f}")

    return {'L1_M_corr': corr, 'spectra': spectra_data}

# ===========================================================================
# EXPLORATION 4: VORONOI ENTROPY ON THE CIRCLE
# ===========================================================================

def voronoi_entropy(fracs):
    """
    Compute Shannon entropy of the arc-length distribution when
    fractions are placed on the circle [0,1).
    """
    if len(fracs) < 2:
        return 0
    F = sorted(fracs)
    # Arc lengths (including wraparound)
    arcs = [F[i+1] - F[i] for i in range(len(F) - 1)]
    arcs.append(1.0 - F[-1] + F[0])  # wraparound

    # Normalize
    total = sum(arcs)
    probs = [a / total for a in arcs if a > 0]

    # Shannon entropy
    H = -sum(p * log(p) for p in probs if p > 0)
    return H

def explore_voronoi_entropy():
    """
    EXPLORATION 4: Voronoi Entropy on the Circle
    Track how entropy changes as N increases, comparing primes vs composites.
    """
    print("\n" + "="*70)
    print("EXPLORATION 4: VORONOI ENTROPY ON THE CIRCLE")
    print("="*70)

    max_N = 120
    Ns = list(range(2, max_N + 1))
    entropies = []
    max_entropies = []  # log(n) for n points = maximum entropy

    for N in Ns:
        F = farey_sequence(N)
        H = voronoi_entropy(F)
        entropies.append(H)
        max_entropies.append(log(len(F)))

    # Compute entropy deficit = H_max - H
    deficits = [max_entropies[i] - entropies[i] for i in range(len(Ns))]

    # Separate primes and composites
    prime_Ns = [N for N in Ns if is_prime(N)]
    comp_Ns = [N for N in Ns if not is_prime(N) and N > 3]
    prime_H = [entropies[N - 2] for N in prime_Ns]
    comp_H = [entropies[N - 2] for N in comp_Ns]
    prime_def = [deficits[N - 2] for N in prime_Ns]
    comp_def = [deficits[N - 2] for N in comp_Ns]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Voronoi Entropy on the Farey Circle',
                 fontsize=16, fontweight='bold')

    # Panel 1: Entropy vs N
    ax = axes[0][0]
    ax.plot(Ns, entropies, '-', color=C_DARK, linewidth=0.8, alpha=0.5, label='All N')
    ax.scatter(prime_Ns, prime_H, c=C_RED, s=30, zorder=3, label='Prime N', alpha=0.7)
    ax.scatter(comp_Ns, comp_H, c=C_BLUE, s=15, zorder=2, label='Composite N', alpha=0.5)
    ax.plot(Ns, max_entropies, '--', color='gray', linewidth=1, label=r'$H_{max} = \ln |F_N|$')
    ax.set_xlabel('N')
    ax.set_ylabel('Shannon Entropy H')
    ax.set_title('Entropy of Arc-Length Distribution')
    ax.legend(fontsize=9)

    # Panel 2: Entropy deficit
    ax = axes[0][1]
    ax.plot(Ns, deficits, '-', color=C_DARK, linewidth=0.8, alpha=0.5)
    ax.scatter(prime_Ns, prime_def, c=C_RED, s=30, zorder=3, label='Prime N')
    ax.scatter(comp_Ns, comp_def, c=C_BLUE, s=15, zorder=2, label='Composite N')
    ax.set_xlabel('N')
    ax.set_ylabel(r'$H_{max} - H$')
    ax.set_title('Entropy Deficit (deviation from uniform)')
    ax.legend(fontsize=9)

    # Panel 3: Delta entropy at primes
    ax = axes[1][0]
    delta_H = []
    for p in prime_Ns:
        if p >= 3:
            dH = entropies[p - 2] - entropies[p - 3]
            delta_H.append((p, dH))

    M = mertens_function(max_N + 5)
    ps_dH = [x[0] for x in delta_H]
    dHs = [x[1] for x in delta_H]
    colors_dH = [C_RED if M[p] > 0 else C_BLUE for p in ps_dH]
    ax.bar(ps_dH, dHs, color=colors_dH, alpha=0.7, width=1.5)
    ax.set_xlabel('Prime p')
    ax.set_ylabel(r'$\Delta H = H(F_p) - H(F_{p-1})$')
    ax.set_title(r'Entropy Change at Primes (red: $M(p)>0$, blue: $M(p)<0$)')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    # Panel 4: Is entropy monotonic?
    ax = axes[1][1]
    monotonic_violations = []
    for i in range(1, len(Ns)):
        if entropies[i] < entropies[i-1]:
            monotonic_violations.append(Ns[i])

    ax.plot(Ns[1:], [entropies[i] - entropies[i-1] for i in range(1, len(Ns))],
            '-', color=C_DARK, linewidth=0.8)

    # Mark violations
    for v in monotonic_violations[:30]:
        ax.axvline(x=v, color=C_RED, alpha=0.15, linewidth=1)

    prime_violations = [v for v in monotonic_violations if is_prime(v)]
    comp_violations = [v for v in monotonic_violations if not is_prime(v)]

    ax.set_xlabel('N')
    ax.set_ylabel(r'$H(F_N) - H(F_{N-1})$')
    ax.set_title(f'Monotonicity Check\n{len(monotonic_violations)} violations '
                 f'({len(prime_violations)} at primes, {len(comp_violations)} at composites)')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    plt.tight_layout()
    save_fig(fig, 'fig_voronoi_entropy.png')

    print(f"\n  Total N values checked: {len(Ns)}")
    print(f"  Monotonicity violations: {len(monotonic_violations)}")
    print(f"    At primes: {len(prime_violations)} ({prime_violations[:10]}...)")
    print(f"    At composites: {len(comp_violations)} ({comp_violations[:10]}...)")

    # Check if entropy is eventually monotonic
    last_violation = max(monotonic_violations) if monotonic_violations else 0
    print(f"  Last violation at N = {last_violation}")

    return {
        'n_violations': len(monotonic_violations),
        'prime_violations': prime_violations,
        'comp_violations': comp_violations,
        'last_violation': last_violation
    }

# ===========================================================================
# EXPLORATION 5: MODULAR INVERSE MAP AS GEOMETRY
# ===========================================================================

def mod_inverse_cycles(p):
    """
    Compute the cycle structure of k -> k^{-1} mod p on {1, ..., p-1}.
    Returns list of cycles.
    """
    visited = set()
    cycles = []
    for start in range(1, p):
        if start in visited:
            continue
        cycle = []
        k = start
        while k not in visited:
            visited.add(k)
            cycle.append(k)
            k = pow(k, -1, p)
        if cycle:
            cycles.append(cycle)
    return cycles

def explore_modular_inverse_map():
    """
    EXPLORATION 5: Modular Inverse Map as Geometry
    Visualize k -> k^{-1} mod p on the unit circle and analyze cycle structure.
    """
    print("\n" + "="*70)
    print("EXPLORATION 5: MODULAR INVERSE MAP AS GEOMETRY")
    print("="*70)

    target_primes = [11, 23, 47, 97]

    fig, axes = plt.subplots(2, 2, figsize=(16, 16))
    fig.suptitle(r'Modular Inverse Map: $k \mapsto k^{-1}\ \mathrm{mod}\ p$ on the Circle',
                 fontsize=16, fontweight='bold')

    cycle_data = {}

    for idx, p in enumerate(target_primes):
        ax = axes[idx // 2][idx % 2]

        cycles = mod_inverse_cycles(p)
        cycle_data[p] = cycles

        # Place elements k on circle at angle 2*pi*k/p
        theta = {k: 2 * np.pi * k / p for k in range(1, p)}
        x = {k: np.cos(theta[k]) for k in range(1, p)}
        y = {k: np.sin(theta[k]) for k in range(1, p)}

        # Draw unit circle
        circle_t = np.linspace(0, 2*np.pi, 200)
        ax.plot(np.cos(circle_t), np.sin(circle_t), '-', color='gray', linewidth=0.5, alpha=0.3)

        # Color each cycle differently
        cycle_colors = plt.cm.Set2(np.linspace(0, 1, max(len(cycles), 1)))

        fixed_points = []
        two_cycles = 0
        long_cycles = []

        for ci, cycle in enumerate(cycles):
            color = cycle_colors[ci % len(cycle_colors)]

            if len(cycle) == 1:
                fixed_points.append(cycle[0])
                ax.plot(x[cycle[0]], y[cycle[0]], 'o', color=C_RED,
                        markersize=10, zorder=5)
            elif len(cycle) == 2:
                two_cycles += 1
                k1, k2 = cycle
                ax.annotate('', xy=(x[k2], y[k2]), xytext=(x[k1], y[k1]),
                            arrowprops=dict(arrowstyle='<->', color=color, lw=1.5, alpha=0.6))
            else:
                long_cycles.append(len(cycle))
                for i in range(len(cycle)):
                    k1 = cycle[i]
                    k2 = cycle[(i+1) % len(cycle)]
                    ax.annotate('', xy=(x[k2], y[k2]), xytext=(x[k1], y[k1]),
                                arrowprops=dict(arrowstyle='->', color=color,
                                               lw=1.2, alpha=0.5,
                                               connectionstyle='arc3,rad=0.2'))

        # Draw all points
        for k in range(1, p):
            if k not in fixed_points:
                ax.plot(x[k], y[k], 'o', color=C_DARK, markersize=4, zorder=4)

        # Labels for small p
        if p <= 30:
            for k in range(1, p):
                offset = 0.12
                ax.text(x[k] * (1 + offset), y[k] * (1 + offset), str(k),
                        fontsize=7, ha='center', va='center', alpha=0.7)

        ax.set_aspect('equal')
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)

        cycle_lengths = sorted([len(c) for c in cycles], reverse=True)
        ax.set_title(f'p = {p}\nFixed pts: {fixed_points}, '
                     f'Cycles: {cycle_lengths}',
                     fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.2)

        print(f"\n  p = {p}:")
        print(f"    Fixed points (k = k^-1 mod p): {fixed_points}")
        print(f"    Two-cycles: {two_cycles}")
        print(f"    Cycle structure: {cycle_lengths}")
        print(f"    Number of cycles: {len(cycles)}")

    plt.tight_layout()
    save_fig(fig, 'fig_modular_inverse_map.png')

    # Summary statistics
    print("\n  Cycle Structure Summary:")
    all_primes = primes_up_to(200)
    cycle_counts = []
    fixed_counts = []
    for p in all_primes:
        if p >= 5:
            cycles = mod_inverse_cycles(p)
            cycle_counts.append(len(cycles))
            n_fixed = sum(1 for c in cycles if len(c) == 1)
            fixed_counts.append(n_fixed)

    # Fixed points of k -> k^{-1} mod p are k where k^2 = 1 mod p
    # i.e. k = 1 or k = p-1 (always exactly 2 for p >= 3)
    print(f"  Fixed point counts: {set(fixed_counts)}")
    print(f"  (Expected: always 2, since k^2 = 1 mod p => k = 1 or k = p-1)")

    # Number of 2-cycles = (p-3)/2 for odd prime p
    print(f"  Two-cycles for p=11: {(11-3)//2} = {(11-3)//2} (expected)")

    return cycle_data

# ===========================================================================
# EXPLORATION 6: TRIANGULATION / FAREY GRAPH CHANGES
# ===========================================================================

def explore_farey_triangulation():
    """
    EXPLORATION 6: Farey Graph Triangulation Changes
    Visualize how the Farey graph changes when a prime is added.
    The Farey graph connects a/b -- c/d iff |ad - bc| = 1 (Farey neighbors).
    """
    print("\n" + "="*70)
    print("EXPLORATION 6: FAREY GRAPH TRIANGULATION")
    print("="*70)

    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Farey Triangulation Changes When Primes Insert',
                 fontsize=16, fontweight='bold')

    primes_to_show = [5, 7, 11]

    for col, p in enumerate(primes_to_show):
        # Before: F_{p-1}
        F_before = farey_sequence_frac(p - 1)
        # After: F_p
        F_after = farey_sequence_frac(p)

        # New fractions
        new_set = set(F_after) - set(F_before)

        for row, (F, title, is_after) in enumerate([
            (F_before, f'$\\mathcal{{F}}_{{{p-1}}}$', False),
            (F_after, f'$\\mathcal{{F}}_{{{p}}}$', True)
        ]):
            ax = axes[row][col]

            # Place fractions on the unit semicircle (Ford circles / Stern-Brocot style)
            # x = fraction value, y = 1/(2*denom^2) (Ford circle radius)
            xs = [float(f) for f in F]
            ys = [1.0 / (2 * f.denominator**2) if f.denominator > 0 else 0.5 for f in F]

            # Draw Farey edges (connect neighbors)
            for i in range(len(F) - 1):
                a, b = F[i].numerator, F[i].denominator
                c, d = F[i+1].numerator, F[i+1].denominator
                if abs(a * d - b * c) == 1:
                    color = C_DARK
                    alpha = 0.3
                    lw = 0.8
                    # If one of them is new, highlight
                    if is_after and (F[i] in new_set or F[i+1] in new_set):
                        color = C_RED
                        alpha = 0.8
                        lw = 1.5
                    ax.plot([xs[i], xs[i+1]], [ys[i], ys[i+1]],
                            '-', color=color, linewidth=lw, alpha=alpha)

            # Draw points
            for i, f in enumerate(F):
                if is_after and f in new_set:
                    ax.plot(xs[i], ys[i], 'o', color=C_RED, markersize=8, zorder=5)
                else:
                    ax.plot(xs[i], ys[i], 'o', color=C_BLUE, markersize=5, zorder=4)

            # Labels for small sequences
            if len(F) <= 30:
                for i, f in enumerate(F):
                    label = f"{f.numerator}/{f.denominator}" if f.denominator > 1 else str(f.numerator)
                    yoff = ys[i] + 0.01
                    ax.text(xs[i], yoff, label, fontsize=6, ha='center', va='bottom',
                            rotation=45, alpha=0.7)

            ax.set_xlim(-0.05, 1.05)
            ax.set_ylim(-0.02, max(ys) * 1.5)
            n_new = len(new_set) if is_after else 0
            ax.set_title(f'{title}  |F| = {len(F)}' +
                         (f'  (+{n_new} new)' if is_after else ''),
                         fontsize=11)
            if col == 0:
                ax.set_ylabel('Ford circle height\n1/(2q^2)')
            ax.set_xlabel('Fraction value')

    plt.tight_layout()
    save_fig(fig, 'fig_farey_triangulation.png')

    # Count new edges and triangles
    print("\n  Triangulation Changes:")
    for p in [5, 7, 11, 13, 17, 19, 23]:
        F_before = farey_sequence_frac(p - 1)
        F_after = farey_sequence_frac(p)

        def count_edges(F):
            edges = 0
            for i in range(len(F)):
                for j in range(i+1, len(F)):
                    a, b = F[i].numerator, F[i].denominator
                    c, d = F[j].numerator, F[j].denominator
                    if abs(a * d - b * c) == 1:
                        edges += 1
            return edges

        e_before = count_edges(F_before)
        e_after = count_edges(F_after)
        new_fracs = len(F_after) - len(F_before)

        print(f"    p = {p}: |F|: {len(F_before)} -> {len(F_after)} (+{new_fracs}), "
              f"edges: {e_before} -> {e_after} (+{e_after - e_before})")

    return {}

# ===========================================================================
# BONUS: COMBINED WALK + SPECTRUM CORRELATION ANALYSIS
# ===========================================================================

def explore_walk_spectrum_correlation():
    """
    BONUS: Check if walk shape metrics correlate with spectral features.
    This bridges Explorations 1 and 3.
    """
    print("\n" + "="*70)
    print("BONUS: WALK-SPECTRUM CORRELATION ANALYSIS")
    print("="*70)

    primes_list = primes_up_to(100)
    M = mertens_function(110)

    walk_maxdist = []
    walk_winding = []
    L1_squared = []
    Lp_squared = []
    mertens_vals = []
    delta_w_vals = []

    for p in primes_list:
        if p < 5:
            continue

        # Walk
        walk, F = farey_walk(p)
        wm = walk_metrics(walk)
        walk_maxdist.append(wm['max_dist'])
        walk_winding.append(wm['winding'])

        # Spectrum
        F_arr = np.array(farey_sequence(p))
        L1 = abs(np.sum(np.exp(2j * np.pi * F_arr)))**2
        Lp = abs(np.sum(np.exp(2j * np.pi * p * F_arr)))**2
        L1_squared.append(L1)
        Lp_squared.append(Lp)

        mertens_vals.append(int(M[p]))

        # Delta W
        W_prev = wobble(p - 1)
        W_cur = wobble(p)
        delta_w_vals.append(W_prev - W_cur)

    # Correlation matrix
    data_dict = {
        'MaxDist': walk_maxdist,
        'Winding': walk_winding,
        'L1^2': L1_squared,
        'Lp^2': Lp_squared,
        'M(p)': mertens_vals,
        'DeltaW': delta_w_vals
    }

    keys = list(data_dict.keys())
    n = len(keys)
    corr_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            corr_matrix[i, j] = np.corrcoef(data_dict[keys[i]], data_dict[keys[j]])[0, 1]

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(keys, rotation=45, ha='right')
    ax.set_yticklabels(keys)

    for i in range(n):
        for j in range(n):
            color = 'white' if abs(corr_matrix[i, j]) > 0.5 else 'black'
            ax.text(j, i, f'{corr_matrix[i, j]:.3f}', ha='center', va='center',
                    fontsize=10, color=color)

    plt.colorbar(im, ax=ax, label='Correlation')
    ax.set_title('Correlation Matrix: Walk Geometry x Spectral Features x Arithmetic',
                 fontsize=13, fontweight='bold')

    plt.tight_layout()
    save_fig(fig, 'fig_correlation_matrix.png')

    print("\n  Correlation Matrix:")
    print(f"  {'':>10}", end='')
    for k in keys:
        print(f"  {k:>8}", end='')
    print()
    for i, ki in enumerate(keys):
        print(f"  {ki:>10}", end='')
        for j in range(n):
            print(f"  {corr_matrix[i,j]:8.4f}", end='')
        print()

    # Flag notable correlations
    print("\n  Notable correlations (|r| > 0.5):")
    for i in range(n):
        for j in range(i+1, n):
            if abs(corr_matrix[i, j]) > 0.5:
                print(f"    {keys[i]} <-> {keys[j]}: r = {corr_matrix[i,j]:.4f}")

    return corr_matrix

# ===========================================================================
# MAIN
# ===========================================================================

def main():
    print("="*70)
    print("GEOMETRIC EXPLORER: Novel Structures in Farey Sequences & Primes")
    print("="*70)

    results = {}

    # Run all explorations
    results['walks'] = explore_farey_walks()
    results['fingerprints'] = explore_prime_fingerprints()
    results['spectrum'] = explore_angular_spectrum()
    results['voronoi'] = explore_voronoi_entropy()
    results['inverse_map'] = explore_modular_inverse_map()
    results['triangulation'] = explore_farey_triangulation()
    results['correlations'] = explore_walk_spectrum_correlation()

    print("\n" + "="*70)
    print("ALL EXPLORATIONS COMPLETE")
    print("="*70)
    print(f"\nFigures saved to: {FIG_DIR}/")

    return results

if __name__ == '__main__':
    results = main()
