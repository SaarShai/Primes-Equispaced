#!/usr/bin/env python3
"""
Comprehensive visualization suite for the Farey wobble / prime circle research.
Generates publication-quality figures for all key results.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as MplCircle
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as ticker
from math import gcd
from fractions import Fraction
import csv

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
FIG_DIR = os.path.join(ROOT, "figures")
CSV_20K = os.path.join(BASE, "wobble_c_data_20000.csv")
CSV_50K = os.path.join(BASE, "wobble_primes_50000.csv")

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
PRIME_COLOR = '#E63946'    # red
COMPOSITE_COLOR = '#457B9D' # blue-steel
NEUTRAL_COLOR = '#264653'
ACCENT = '#F4A261'

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def farey_sequence(N):
    """Generate Farey sequence F_N as list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def sieve_mu(limit):
    """Compute Möbius function via sieve up to limit (inclusive)."""
    mu = np.ones(limit + 1, dtype=np.int64)
    is_p = np.ones(limit + 1, dtype=bool)
    is_p[0] = is_p[1] = False
    for p in range(2, limit + 1):
        if is_p[p]:
            for m in range(p, limit + 1, p):
                if m != p:
                    is_p[m] = False
                mu[m] *= -1
            p2 = p * p
            for m in range(p2, limit + 1, p2):
                mu[m] = 0
    return mu


def load_csv(path):
    """Load a CSV file into a dict of numpy arrays."""
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    data = {}
    for key in rows[0]:
        try:
            data[key] = np.array([float(r[key]) for r in rows])
        except ValueError:
            data[key] = np.array([r[key] for r in rows])
    return data


def save(fig, name):
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


# ---------------------------------------------------------------------------
# 1. CIRCLE VISUALIZATION
# ---------------------------------------------------------------------------
def fig_circle_farey():
    print("Generating fig_circle_farey.png ...")
    N = 12
    fracs = farey_sequence(N)

    fig, ax = plt.subplots(figsize=(10, 10))
    theta_circle = np.linspace(0, 2 * np.pi, 500)
    ax.plot(np.cos(theta_circle), np.sin(theta_circle), 'k-', lw=1.2, alpha=0.4)

    prime_x, prime_y = [], []
    comp_x, comp_y = [], []

    for fr in fracs:
        angle = 2 * np.pi * float(fr)
        x, y = np.cos(angle), np.sin(angle)
        denom = fr.denominator
        if is_prime(denom) and denom > 1:
            prime_x.append(x); prime_y.append(y)
            ax.plot([0, x], [0, y], color=PRIME_COLOR, lw=0.4, alpha=0.35)
        else:
            comp_x.append(x); comp_y.append(y)
            ax.plot([0, x], [0, y], color=COMPOSITE_COLOR, lw=0.3, alpha=0.2)

    ax.scatter(comp_x, comp_y, s=30, c=COMPOSITE_COLOR, zorder=5,
               edgecolors='white', linewidths=0.3, label='Composite denominator')
    ax.scatter(prime_x, prime_y, s=50, c=PRIME_COLOR, zorder=6,
               edgecolors='white', linewidths=0.3, label='Prime denominator')

    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect('equal')
    ax.set_title(r'Farey Fractions $F_{12}$ on the Unit Circle', fontsize=16, fontweight='bold')
    ax.legend(loc='lower right', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    return save(fig, "fig_circle_farey.png")


# ---------------------------------------------------------------------------
# 2. CIRCLE PRIME vs COMPOSITE INSERTION
# ---------------------------------------------------------------------------
def fig_circle_insertion():
    print("Generating fig_circle_insertion.png ...")
    f12 = set(farey_sequence(12))
    f13 = set(farey_sequence(13))
    f14 = set(farey_sequence(14))

    new_prime = f13 - f12      # fractions added when N goes 12→13 (prime)
    new_composite = f14 - f13  # fractions added when N goes 13→14 (composite)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    for ax, base_set, new_set, title, color, n_label in [
        (ax1, f12, new_prime,
         r'$F_{12} \to F_{13}$ (prime insertion)', PRIME_COLOR, 13),
        (ax2, f13, new_composite,
         r'$F_{13} \to F_{14}$ (composite insertion)', COMPOSITE_COLOR, 14),
    ]:
        theta_c = np.linspace(0, 2 * np.pi, 500)
        ax.plot(np.cos(theta_c), np.sin(theta_c), 'k-', lw=1, alpha=0.4)

        # existing fractions
        for fr in sorted(base_set):
            angle = 2 * np.pi * float(fr)
            x, y = np.cos(angle), np.sin(angle)
            ax.scatter(x, y, s=15, c='#AAAAAA', zorder=4, edgecolors='none')

        # new fractions
        nx, ny = [], []
        for fr in sorted(new_set):
            angle = 2 * np.pi * float(fr)
            x, y = np.cos(angle), np.sin(angle)
            nx.append(x); ny.append(y)
            ax.plot([0, x], [0, y], color=color, lw=0.8, alpha=0.5)

        ax.scatter(nx, ny, s=70, c=color, zorder=6, edgecolors='white', linewidths=0.5)
        ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.text(0.02, 0.02, f'{len(new_set)} new fractions',
                transform=ax.transAxes, fontsize=11, color=color, fontweight='bold')
        ax.grid(True, alpha=0.3)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#AAAAAA',
               markersize=6, label='Existing fractions'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=PRIME_COLOR,
               markersize=9, label='New (prime N=13)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=COMPOSITE_COLOR,
               markersize=9, label='New (composite N=14)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=11,
               framealpha=0.9, bbox_to_anchor=(0.5, -0.01))
    fig.suptitle('Prime vs Composite Insertions into the Farey Sequence',
                 fontsize=15, fontweight='bold', y=1.01)
    return save(fig, "fig_circle_insertion.png")


# ---------------------------------------------------------------------------
# 3. WOBBLE TRAJECTORY
# ---------------------------------------------------------------------------
def fig_wobble_trajectory():
    print("Generating fig_wobble_trajectory.png ...")
    d = load_csv(CSV_20K)
    N = d['N']
    W = d['wobble']
    isp = d['is_prime'].astype(int)

    fig, ax = plt.subplots(figsize=(14, 7))

    # composites first (below)
    mask_c = isp == 0
    mask_p = isp == 1
    ax.scatter(N[mask_c], W[mask_c], s=0.6, c=COMPOSITE_COLOR, alpha=0.35,
               label='Composite N', rasterized=True)
    ax.scatter(N[mask_p], W[mask_p], s=1.5, c=PRIME_COLOR, alpha=0.6,
               label='Prime N', rasterized=True)

    # O(1/N) envelope
    nn = np.linspace(2, 20000, 2000)
    ax.plot(nn, 1.0 / nn, 'k--', lw=1.2, alpha=0.6, label=r'$O(1/N)$ envelope')

    ax.set_yscale('log')
    ax.set_xlabel(r'$N$', fontsize=13)
    ax.set_ylabel(r'$W(N)$', fontsize=13)
    ax.set_title(r'Farey Wobble $W(N)$ — Trajectory to $N=20{,}000$',
                 fontsize=15, fontweight='bold')
    ax.legend(fontsize=11, loc='upper right', framealpha=0.9)
    ax.set_xlim(0, 20200)
    ax.grid(True, alpha=0.3, which='both')
    return save(fig, "fig_wobble_trajectory.png")


# ---------------------------------------------------------------------------
# 4. DELTA W SIGN PLOT
# ---------------------------------------------------------------------------
def fig_delta_w_signs():
    print("Generating fig_delta_w_signs.png ...")
    d = load_csv(CSV_20K)
    # Filter to primes >= 11
    mask = (d['is_prime'].astype(int) == 1) & (d['N'] >= 11)
    primes = d['N'][mask]
    dw = d['delta_w'][mask]

    fig, ax = plt.subplots(figsize=(14, 6))

    violations = dw > 0
    ax.bar(primes[~violations], dw[~violations], width=8, color=COMPOSITE_COLOR,
           alpha=0.7, label=r'$\Delta W < 0$ (normal)', rasterized=True)
    ax.bar(primes[violations], dw[violations], width=8, color=PRIME_COLOR,
           alpha=0.85, label=r'$\Delta W > 0$ (violation)', rasterized=True)

    # Shade violation clusters: find contiguous groups of violations
    viol_primes = primes[violations]
    if len(viol_primes) > 0:
        # Group violations that are within 200 of each other
        groups = []
        current_group = [viol_primes[0]]
        for p in viol_primes[1:]:
            if p - current_group[-1] < 300:
                current_group.append(p)
            else:
                groups.append(current_group)
                current_group = [p]
        groups.append(current_group)

        for grp in groups:
            if len(grp) >= 2:
                ax.axvspan(grp[0] - 30, grp[-1] + 30, alpha=0.08,
                           color=PRIME_COLOR, zorder=0)

    ax.axhline(0, color='black', lw=0.8)
    ax.set_xlabel(r'Prime $p$', fontsize=13)
    ax.set_ylabel(r'$\Delta W(p)$', fontsize=13)
    ax.set_title(r'Per-Prime Wobble Change $\Delta W(p)$ — Violations in Red',
                 fontsize=15, fontweight='bold')
    ax.legend(fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    return save(fig, "fig_delta_w_signs.png")


# ---------------------------------------------------------------------------
# 5. MERTENS FUNCTION vs VIOLATIONS
# ---------------------------------------------------------------------------
def fig_mertens_violations():
    print("Generating fig_mertens_violations.png ...")
    d = load_csv(CSV_20K)
    N = d['N']
    mertens = d['mertens']
    m_norm = mertens / np.sqrt(N)

    # Violation info from primes
    mask_p = (d['is_prime'].astype(int) == 1) & (N >= 11)
    p_vals = N[mask_p]
    dw_vals = d['delta_w'][mask_p]
    violations = dw_vals > 0

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True,
                                    gridspec_kw={'height_ratios': [2, 1]})

    # Top: M(N)/sqrt(N)
    pos_mask = m_norm > 0
    neg_mask = ~pos_mask
    # Plot as a line, but color segments
    ax1.fill_between(N, m_norm, 0, where=pos_mask, color=PRIME_COLOR,
                     alpha=0.35, label=r'$M(N) > 0$')
    ax1.fill_between(N, m_norm, 0, where=neg_mask, color=COMPOSITE_COLOR,
                     alpha=0.35, label=r'$M(N) \leq 0$')
    ax1.plot(N, m_norm, 'k-', lw=0.3, alpha=0.5)
    ax1.axhline(0, color='black', lw=0.8)
    ax1.set_ylabel(r'$M(N)/\sqrt{N}$', fontsize=13)
    ax1.set_title(r'Mertens Function and Wobble Violations', fontsize=15, fontweight='bold')
    ax1.legend(fontsize=11, framealpha=0.9, loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Bottom: violation density (rolling window of 200 primes)
    window = 200
    viol_arr = violations.astype(float)
    if len(viol_arr) > window:
        density = np.convolve(viol_arr, np.ones(window) / window, mode='valid')
        density_x = p_vals[:len(density)]
    else:
        density = viol_arr
        density_x = p_vals

    ax2.fill_between(density_x, density, 0, color=PRIME_COLOR, alpha=0.5)
    ax2.plot(density_x, density, color=PRIME_COLOR, lw=0.8)
    ax2.set_ylabel('Violation density\n(200-prime window)', fontsize=11)
    ax2.set_xlabel(r'$N$', fontsize=13)
    ax2.set_ylim(0, max(density) * 1.15 if len(density) > 0 else 1)
    ax2.grid(True, alpha=0.3)

    fig.align_ylabels()
    return save(fig, "fig_mertens_violations.png")


# ---------------------------------------------------------------------------
# 6. BURST-QUIET PATTERN
# ---------------------------------------------------------------------------
def fig_burst_quiet():
    print("Generating fig_burst_quiet.png ...")
    d = load_csv(CSV_50K)
    p = d['p']
    viol = d['violation'].astype(int)
    n_primes = len(p)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 6),
                                    gridspec_kw={'height_ratios': [1, 1.5]},
                                    sharex=True)

    # Top: strip chart
    idx = np.arange(n_primes)
    colors = np.where(viol == 1, PRIME_COLOR, COMPOSITE_COLOR)
    ax1.scatter(idx, np.ones(n_primes), c=colors, s=0.5, marker='|',
                linewidths=0.5, rasterized=True)
    ax1.set_yticks([])
    ax1.set_ylabel('Violation\nstrip', fontsize=11)
    ax1.set_title(r'Burst-Quiet Pattern in Wobble Violations ($N \leq 50{,}000$)',
                  fontsize=15, fontweight='bold')

    # Shade burst regions (rolling average > threshold)
    window = 50
    if n_primes > window:
        rolling = np.convolve(viol.astype(float), np.ones(window) / window, mode='same')
        threshold = 0.15
        burst_mask = rolling > threshold
        ax1.fill_between(idx, 0, 2, where=burst_mask, color=PRIME_COLOR,
                         alpha=0.12, transform=ax1.get_xaxis_transform())

    # Bottom: cumulative violation rate
    cum_viols = np.cumsum(viol)
    cum_rate = cum_viols / (idx + 1)
    ax2.plot(idx, cum_rate, color=NEUTRAL_COLOR, lw=1.2)
    ax2.fill_between(idx, cum_rate, 0, color=NEUTRAL_COLOR, alpha=0.15)
    ax2.set_xlabel('Prime index', fontsize=13)
    ax2.set_ylabel('Cumulative\nviolation rate', fontsize=11)
    ax2.grid(True, alpha=0.3)

    legend_elements = [
        Line2D([0], [0], marker='|', color=PRIME_COLOR, lw=0, markersize=10,
               markeredgewidth=2, label='Violation'),
        Line2D([0], [0], marker='|', color=COMPOSITE_COLOR, lw=0, markersize=10,
               markeredgewidth=2, label='No violation'),
    ]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.9)

    fig.align_ylabels()
    return save(fig, "fig_burst_quiet.png")


# ---------------------------------------------------------------------------
# 7. MERTENS PREDICTOR ACCURACY
# ---------------------------------------------------------------------------
def fig_predictor_accuracy():
    print("Generating fig_predictor_accuracy.png ...")
    d = load_csv(CSV_20K)
    mask = (d['is_prime'].astype(int) == 1) & (d['N'] >= 11)
    primes = d['N'][mask]
    dw = d['delta_w'][mask]
    mertens = d['mertens'][mask]
    m_over_sqrt = mertens / np.sqrt(primes)
    violations = dw > 0

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.scatter(m_over_sqrt[~violations], dw[~violations], s=8, c=COMPOSITE_COLOR,
               alpha=0.4, label=r'$\Delta W < 0$ (normal)', rasterized=True)
    ax.scatter(m_over_sqrt[violations], dw[violations], s=25, c=PRIME_COLOR,
               alpha=0.8, label=r'$\Delta W > 0$ (violation)', zorder=5)

    ax.axvline(0, color='black', lw=1.5, ls='--', alpha=0.7, label=r'$M(p)/\sqrt{p} = 0$')
    ax.axhline(0, color='gray', lw=0.8, alpha=0.5)

    # Annotation: count violations to the right
    v_right = np.sum(violations & (m_over_sqrt > 0))
    v_left = np.sum(violations & (m_over_sqrt <= 0))
    v_total = np.sum(violations)
    ax.text(0.97, 0.97,
            f'Violations: {v_total}\n'
            f'  Right of line: {v_right}\n'
            f'  Left of line: {v_left}',
            transform=ax.transAxes, fontsize=11, va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.9))

    ax.set_xlabel(r'$M(p)/\sqrt{p}$', fontsize=13)
    ax.set_ylabel(r'$\Delta W(p)$', fontsize=13)
    ax.set_title(r'Mertens Function as Wobble Violation Predictor',
                 fontsize=15, fontweight='bold')
    ax.legend(fontsize=11, framealpha=0.9, loc='lower right')
    ax.grid(True, alpha=0.3)
    return save(fig, "fig_predictor_accuracy.png")


# ---------------------------------------------------------------------------
# 8. CLUSTER GROWTH
# ---------------------------------------------------------------------------
def fig_cluster_growth():
    print("Generating fig_cluster_growth.png ...")
    d = load_csv(CSV_50K)
    p = d['p']
    viol = d['violation'].astype(int)

    # Identify clusters: consecutive violations (allowing gaps of <=2 primes)
    clusters = []
    i = 0
    while i < len(viol):
        if viol[i] == 1:
            start = i
            j = i
            while j < len(viol) - 1:
                # look ahead: if next 3 primes have any violation, extend
                lookahead = min(j + 4, len(viol))
                if np.any(viol[j + 1:lookahead] == 1):
                    j = j + 1
                    while j < lookahead and viol[j] == 0:
                        j += 1
                    if j >= lookahead:
                        break
                else:
                    break
            end = j
            cluster_size = np.sum(viol[start:end + 1])
            if cluster_size >= 2:
                center = (p[start] + p[end]) / 2
                clusters.append((center, cluster_size, p[start], p[end]))
            i = end + 1
        else:
            i += 1

    if not clusters:
        print("  No clusters found, skipping.")
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'No violation clusters detected', transform=ax.transAxes,
                ha='center', va='center', fontsize=14)
        return save(fig, "fig_cluster_growth.png")

    centers = np.array([c[0] for c in clusters])
    sizes = np.array([c[1] for c in clusters])

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(centers, sizes, s=40, c=PRIME_COLOR, alpha=0.6, edgecolors='white',
               linewidths=0.3, zorder=5)

    # Fit sqrt trend
    from numpy.polynomial import polynomial as P
    # Fit size ~ a * sqrt(center) + b
    valid = centers > 0
    sqrt_c = np.sqrt(centers[valid])
    coeffs = np.polyfit(sqrt_c, sizes[valid], 1)
    fit_x = np.linspace(np.min(centers[valid]), np.max(centers[valid]), 200)
    fit_y = coeffs[0] * np.sqrt(fit_x) + coeffs[1]
    ax.plot(fit_x, fit_y, 'k--', lw=1.8, alpha=0.7,
            label=rf'Fit: $\sim {coeffs[0]:.3f}\sqrt{{N}} + {coeffs[1]:.1f}$')

    ax.set_xlabel(r'Cluster center location $N$', fontsize=13)
    ax.set_ylabel('Cluster size (# violations)', fontsize=13)
    ax.set_title('Growing Violation Clusters', fontsize=15, fontweight='bold')
    ax.legend(fontsize=12, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    return save(fig, "fig_cluster_growth.png")


# ---------------------------------------------------------------------------
# 9. ZETA ZEROS CONNECTION
# ---------------------------------------------------------------------------
def fig_zeta_connection():
    print("Generating fig_zeta_connection.png ...")
    limit = 30000
    print("  Computing Möbius sieve up to 30000 ...")
    mu = sieve_mu(limit)
    M = np.cumsum(mu)
    nn = np.arange(1, limit + 1)
    m_norm = M[1:] / np.sqrt(nn)

    # Zeta zeros
    gamma1 = 14.134725
    gamma2 = 21.022040

    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True,
                              gridspec_kw={'height_ratios': [2, 0.6, 1.5]})

    # Top: M(N)/sqrt(N)
    ax = axes[0]
    ax.plot(nn, m_norm, 'k-', lw=0.3, alpha=0.5)
    pos = m_norm > 0
    ax.fill_between(nn, m_norm, 0, where=pos, color=PRIME_COLOR, alpha=0.4,
                    label=r'$M(N) > 0$')
    ax.fill_between(nn, m_norm, 0, where=~pos, color=COMPOSITE_COLOR, alpha=0.3,
                    label=r'$M(N) \leq 0$')
    ax.axhline(0, color='black', lw=0.8)
    ax.set_ylabel(r'$M(N)/\sqrt{N}$', fontsize=13)
    ax.set_title('Zeta Zeros Drive Mertens Oscillation', fontsize=15, fontweight='bold')
    ax.legend(fontsize=11, framealpha=0.9, loc='upper right')
    ax.grid(True, alpha=0.3)

    # Middle: hot zones (M > 0)
    ax2 = axes[1]
    ax2.fill_between(nn, 0, 1, where=pos, color=PRIME_COLOR, alpha=0.6)
    ax2.fill_between(nn, 0, 1, where=~pos, color=COMPOSITE_COLOR, alpha=0.15)
    ax2.set_yticks([])
    ax2.set_ylabel('Hot zones', fontsize=11)

    # Bottom: zeta zero interference
    ax3 = axes[2]
    log_n = np.log(nn.astype(float))
    cos1 = np.cos(gamma1 * log_n)
    cos2 = np.cos(gamma2 * log_n)
    combined = cos1 + cos2

    ax3.plot(nn, cos1, color=ACCENT, lw=0.6, alpha=0.6,
             label=rf'$\cos(\gamma_1 \ln N)$, $\gamma_1={gamma1}$')
    ax3.plot(nn, cos2, color='#2A9D8F', lw=0.6, alpha=0.6,
             label=rf'$\cos(\gamma_2 \ln N)$, $\gamma_2={gamma2}$')
    ax3.plot(nn, combined, color=NEUTRAL_COLOR, lw=1.0, alpha=0.8,
             label='Sum (interference)')
    ax3.axhline(0, color='black', lw=0.5)
    ax3.set_xlabel(r'$N$', fontsize=13)
    ax3.set_ylabel('Amplitude', fontsize=13)
    ax3.legend(fontsize=10, framealpha=0.9, loc='upper right')
    ax3.grid(True, alpha=0.3)

    fig.align_ylabels()
    return save(fig, "fig_zeta_connection.png")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Farey Wobble / Prime Circle Visualization Suite")
    print("=" * 60)
    generated = []

    generated.append(fig_circle_farey())
    generated.append(fig_circle_insertion())
    generated.append(fig_wobble_trajectory())
    generated.append(fig_delta_w_signs())
    generated.append(fig_mertens_violations())
    generated.append(fig_burst_quiet())
    generated.append(fig_predictor_accuracy())
    generated.append(fig_cluster_growth())
    generated.append(fig_zeta_connection())

    print("\n" + "=" * 60)
    print(f"All {len(generated)} figures generated:")
    for p in generated:
        print(f"  {p}")
    print("=" * 60)


if __name__ == "__main__":
    main()
