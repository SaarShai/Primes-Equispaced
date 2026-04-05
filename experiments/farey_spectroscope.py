#!/usr/bin/env python3
"""Farey Spectroscope — visualizing zeta zeros from Farey sequence data.
Creates publication-quality figures."""

import numpy as np
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

DATA = os.path.expanduser("~/Desktop/Farey-Local/experiments/bc_verify_100000_c.csv")
OUT = os.path.expanduser("~/Desktop/Farey-Local/experiments/")

# Load data
primes, R_vals = [], []
with open(DATA) as f:
    for row in csv.DictReader(f):
        primes.append(int(row['p']))
        R_vals.append(float(row['R']))
primes = np.array(primes, dtype=float)
R_vals = np.array(R_vals)
log_p = np.log(primes)

# Known zeta zeros
known_zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
               37.5862, 40.9187, 43.3271, 48.0052]
zero_labels = [f'γ₁={known_zeros[0]:.1f}', f'γ₂={known_zeros[1]:.1f}',
               f'γ₃={known_zeros[2]:.1f}', f'γ₄={known_zeros[3]:.1f}',
               f'γ₅={known_zeros[4]:.1f}']

# Compute spectral function
gamma_grid = np.linspace(5, 52, 10000)
F_gamma = np.zeros(len(gamma_grid))
for i, gamma in enumerate(gamma_grid):
    terms = R_vals * primes**(-0.5) * np.exp(-1j * gamma * log_p)
    F_gamma[i] = np.abs(np.sum(terms))**2

# Normalize
F_norm = F_gamma / np.max(F_gamma)

# ============================================================
# FIGURE 1: The Farey Spectroscope
# ============================================================
fig, axes = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [3, 1]})

# Top panel: Farey spectral function
ax1 = axes[0]
ax1.plot(gamma_grid, F_norm, color='#1a5276', linewidth=0.8, alpha=0.9)
ax1.fill_between(gamma_grid, 0, F_norm, alpha=0.15, color='#2980b9')

# Mark known zeros
for i, gz in enumerate(known_zeros):
    color = '#e74c3c' if i == 0 else '#e67e22' if i < 5 else '#95a5a6'
    ax1.axvline(x=gz, color=color, linestyle='--', alpha=0.7, linewidth=1.2)
    if i < 5:
        ax1.annotate(zero_labels[i], xy=(gz, 0.95 - 0.12*i),
                    fontsize=9, color=color, fontweight='bold',
                    xycoords=('data', 'axes fraction'))

ax1.set_xlim(5, 52)
ax1.set_ylim(0, 1.05)
ax1.set_ylabel('Normalized spectral power', fontsize=12)
ax1.set_title('The Farey Spectroscope: Zeta Zeros from Farey Sequence Data',
              fontsize=14, fontweight='bold')
ax1.text(0.02, 0.92, f'N = {len(primes)} qualifying primes, p ≤ {int(primes[-1])}',
         transform=ax1.transAxes, fontsize=10, color='gray',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Bottom panel: Classical zeta zero positions (reference)
ax2 = axes[1]
ax2.set_xlim(5, 52)
ax2.set_ylim(-0.5, 0.5)
for i, gz in enumerate(known_zeros):
    ax2.plot(gz, 0, 'o', color='#e74c3c', markersize=10, zorder=5)
    ax2.annotate(f'ρ_{i+1}', xy=(gz, -0.3), ha='center', fontsize=8)
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.set_ylabel('Critical line\nIm(ρ)', fontsize=10)
ax2.set_xlabel('γ (imaginary part of zeta zero)', fontsize=12)
ax2.set_title('Known nontrivial zeros of ζ(s) on the critical line Re(s) = ½',
              fontsize=11)
ax2.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'farey_spectroscope.png'), dpi=200, bbox_inches='tight')
plt.savefig(os.path.join(OUT, 'farey_spectroscope.pdf'), bbox_inches='tight')
print(f"Figure 1 saved: farey_spectroscope.png/pdf")

# ============================================================
# FIGURE 2: Convergence — how many primes needed?
# ============================================================
fig2, ax = plt.subplots(figsize=(12, 6))

subsets = [100, 200, 500, 1000, 2000, len(primes)]
colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(subsets)))

for si, (n_use, col) in enumerate(zip(subsets, colors)):
    idx = slice(0, min(n_use, len(primes)))
    F_sub = np.zeros(len(gamma_grid))
    for i, gamma in enumerate(gamma_grid):
        terms = R_vals[idx] * primes[idx]**(-0.5) * np.exp(-1j * gamma * log_p[idx])
        F_sub[i] = np.abs(np.sum(terms))**2
    F_sub_norm = F_sub / np.max(F_sub) if np.max(F_sub) > 0 else F_sub
    label = f'{min(n_use, len(primes))} primes (p ≤ {int(primes[min(n_use, len(primes))-1])})'
    ax.plot(gamma_grid, F_sub_norm + si*0.3, color=col, linewidth=0.8, label=label)

for gz in known_zeros[:5]:
    ax.axvline(x=gz, color='#e74c3c', linestyle=':', alpha=0.4, linewidth=0.8)

ax.set_xlim(10, 40)
ax.set_ylabel('Spectral power (offset for clarity)', fontsize=11)
ax.set_xlabel('γ', fontsize=12)
ax.set_title('Convergence: Zeta Zero Detection Improves with More Primes',
             fontsize=13, fontweight='bold')
ax.legend(loc='upper right', fontsize=9)
ax.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'farey_spectroscope_convergence.png'), dpi=200, bbox_inches='tight')
plt.savefig(os.path.join(OUT, 'farey_spectroscope_convergence.pdf'), bbox_inches='tight')
print(f"Figure 2 saved: farey_spectroscope_convergence.png/pdf")

# ============================================================
# FIGURE 3: Juxtaposition — classical Z(t) vs Farey spectral
# ============================================================
# Compute a rough version of Z(t) = Re(exp(iθ(t))·ζ(1/2+it))
# using the Riemann-Siegel approximation for comparison
try:
    import mpmath
    mpmath.mp.dps = 15

    fig3, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Top: Classical Hardy Z-function
    t_grid = np.linspace(10, 52, 2000)
    Z_vals = []
    for t in t_grid:
        z = complex(mpmath.siegelz(t))
        Z_vals.append(z.real if isinstance(z, complex) else float(z))
    Z_vals = np.array(Z_vals)

    ax_top = axes[0]
    ax_top.plot(t_grid, Z_vals, color='#8e44ad', linewidth=0.8)
    ax_top.fill_between(t_grid, 0, Z_vals, where=Z_vals > 0, alpha=0.2, color='#8e44ad')
    ax_top.fill_between(t_grid, 0, Z_vals, where=Z_vals < 0, alpha=0.2, color='#e74c3c')
    ax_top.axhline(y=0, color='black', linewidth=0.5)
    for gz in known_zeros[:5]:
        ax_top.axvline(x=gz, color='#e74c3c', linestyle='--', alpha=0.5, linewidth=0.8)
    ax_top.set_ylabel('Z(t) (Hardy function)', fontsize=11)
    ax_top.set_title('Classical: Zeta Zeros as Sign Changes of Z(t)',
                     fontsize=13, fontweight='bold')
    ax_top.text(0.02, 0.85, 'Zeros of ζ(½+it) = sign changes of Z(t)',
               transform=ax_top.transAxes, fontsize=10, style='italic',
               bbox=dict(boxstyle='round', facecolor='#f5eef8', alpha=0.8))

    # Bottom: Farey spectroscope
    ax_bot = axes[1]
    ax_bot.plot(gamma_grid, F_norm, color='#1a5276', linewidth=0.8)
    ax_bot.fill_between(gamma_grid, 0, F_norm, alpha=0.2, color='#2980b9')
    for gz in known_zeros[:5]:
        ax_bot.axvline(x=gz, color='#e74c3c', linestyle='--', alpha=0.5, linewidth=0.8)
    ax_bot.set_ylabel('Farey spectral power', fontsize=11)
    ax_bot.set_xlabel('γ (imaginary part)', fontsize=12)
    ax_bot.set_title('New: Zeta Zeros as Spectral Peaks in Farey Data',
                     fontsize=13, fontweight='bold')
    ax_bot.text(0.02, 0.85, f'F(γ) = |Σ R(p)·p^{{-½-iγ}}|²  ({len(primes)} primes)',
               transform=ax_bot.transAxes, fontsize=10, style='italic',
               bbox=dict(boxstyle='round', facecolor='#eaf2f8', alpha=0.8))
    ax_bot.set_xlim(10, 52)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'farey_vs_classical_zeros.png'), dpi=200, bbox_inches='tight')
    plt.savefig(os.path.join(OUT, 'farey_vs_classical_zeros.pdf'), bbox_inches='tight')
    print(f"Figure 3 saved: farey_vs_classical_zeros.png/pdf")
except ImportError:
    print("mpmath not available — skipping Figure 3 (classical Z(t) comparison)")

print("\nDone. All figures in ~/Desktop/Farey-Local/experiments/")
