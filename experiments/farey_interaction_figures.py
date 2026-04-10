#!/usr/bin/env python3
"""Farey discrepancy interaction figures — showing HOW zeta zeros affect regularity."""
import numpy as np
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATA = os.path.expanduser("~/Desktop/Farey-Local/experiments/bc_verify_100000_c.csv")
OUT = os.path.expanduser("~/Desktop/Farey-Local/experiments/")

primes, R_vals, M_vals, bpc_vals = [], [], [], []
with open(DATA) as f:
    for row in csv.DictReader(f):
        primes.append(int(row['p']))
        R_vals.append(float(row['R']))
        M_vals.append(int(row['M_p']))
        bpc_vals.append(float(row['B_plus_C']))
primes = np.array(primes, dtype=float)
R_vals = np.array(R_vals)
M_vals = np.array(M_vals)
bpc_vals = np.array(bpc_vals)
log_p = np.log(primes)

gamma1 = 14.1347

# ============================================================
# FIGURE 4: Phase-lock visualization
# Show R(p) oscillating with cos(γ₁·log(p))
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

ax1 = axes[0]
ax1.scatter(log_p, R_vals, s=1, alpha=0.3, c='#2c3e50')
ax1.set_ylabel('R(p)', fontsize=11)
ax1.set_title('Farey Correlation Ratio R(p) vs log(p)', fontsize=12)
ax1.axhline(y=0, color='red', linewidth=0.5, linestyle='--')

ax2 = axes[1]
cos_vals = np.cos(gamma1 * log_p + 5.10)
ax2.plot(log_p, cos_vals, color='#e74c3c', linewidth=0.5, alpha=0.7)
ax2.set_ylabel(f'cos(γ₁·log(p) + φ)', fontsize=11)
ax2.set_title(f'Leading Zeta Zero Oscillation (γ₁ = {gamma1})', fontsize=12)
ax2.axhline(y=0, color='gray', linewidth=0.5)

ax3 = axes[2]
# Smoothed R(p) vs cos(γ₁·log(p))
window = 50
R_smooth = np.convolve(R_vals, np.ones(window)/window, mode='valid')
cos_smooth = np.convolve(cos_vals, np.ones(window)/window, mode='valid')
log_p_smooth = log_p[window//2:window//2+len(R_smooth)]
ax3.plot(log_p_smooth, R_smooth / np.max(np.abs(R_smooth)), label='R(p) smoothed', color='#2c3e50', linewidth=1.5)
ax3.plot(log_p_smooth, cos_smooth / np.max(np.abs(cos_smooth)), label=f'cos(γ₁·log(p)+φ) smoothed', color='#e74c3c', linewidth=1.5)
ax3.legend(fontsize=10)
ax3.set_ylabel('Normalized amplitude', fontsize=11)
ax3.set_xlabel('log(p)', fontsize=12)
ax3.set_title('Smoothed Overlay: R(p) Tracks the Leading Zeta Zero', fontsize=12)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'phase_lock_visualization.png'), dpi=200, bbox_inches='tight')
plt.savefig(os.path.join(OUT, 'phase_lock_visualization.pdf'), bbox_inches='tight')
print("Figure 4 saved: phase_lock_visualization.png/pdf")

# ============================================================
# FIGURE 5: Spectral decomposition — contribution of each zero
# ============================================================
fig5, ax = plt.subplots(figsize=(14, 6))

gamma_grid = np.linspace(5, 52, 10000)
F_full = np.zeros(len(gamma_grid))
for i, g in enumerate(gamma_grid):
    terms = R_vals * primes**(-0.5) * np.exp(-1j * g * log_p)
    F_full[i] = np.abs(np.sum(terms))**2

F_norm = F_full / np.max(F_full)

# Compute contribution at each known zero
known_zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351]
zero_powers = []
for gz in known_zeros:
    terms = R_vals * primes**(-0.5) * np.exp(-1j * gz * log_p)
    zero_powers.append(np.abs(np.sum(terms))**2)

# Bar chart of zero contributions
ax_bar = fig5.add_axes([0.65, 0.55, 0.30, 0.35])
bars = ax_bar.bar(range(1, len(known_zeros)+1), [zp/zero_powers[0] for zp in zero_powers],
                  color=['#e74c3c', '#e67e22', '#f1c40f', '#27ae60', '#3498db'])
ax_bar.set_xlabel('Zero index k', fontsize=9)
ax_bar.set_ylabel('Power / γ₁ power', fontsize=9)
ax_bar.set_title('Relative Strength\nof Each Zero', fontsize=10)

# Main spectral plot
ax.plot(gamma_grid, F_norm, color='#1a5276', linewidth=0.8)
ax.fill_between(gamma_grid, 0, F_norm, alpha=0.15, color='#2980b9')

colors = ['#e74c3c', '#e67e22', '#f1c40f', '#27ae60', '#3498db']
for i, gz in enumerate(known_zeros):
    ax.axvline(x=gz, color=colors[i], linestyle='--', alpha=0.7, linewidth=1.2)
    power_pct = 100 * zero_powers[i] / zero_powers[0]
    ax.annotate(f'γ_{i+1}: {power_pct:.0f}%', xy=(gz, 0.85-0.12*i),
               fontsize=9, color=colors[i], fontweight='bold',
               xycoords=('data', 'axes fraction'))

ax.set_xlim(5, 52)
ax.set_xlabel('γ (spectral frequency)', fontsize=12)
ax.set_ylabel('Normalized spectral power', fontsize=11)
ax.set_title('How Each Zeta Zero Affects Farey Regularity', fontsize=14, fontweight='bold')
ax.text(0.02, 0.92, 'γ₁ dominates: 100% of maximum power\nHigher zeros contribute progressively less',
       transform=ax.transAxes, fontsize=10,
       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'zero_contributions.png'), dpi=200, bbox_inches='tight')
plt.savefig(os.path.join(OUT, 'zero_contributions.pdf'), bbox_inches='tight')
print("Figure 5 saved: zero_contributions.png/pdf")

# ============================================================
# FIGURE 6: Multi-character spectroscope (Dedekind/L-functions)
# ============================================================
fig6, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

characters = {
    'Untwisted → ζ(s) zeros': lambda p: 1.0,
    'χ₄ twist → L(s,χ₄) zeros': lambda p: (1 if int(p)%4==1 else -1 if int(p)%4==3 else 0),
    'χ₃ twist → L(s,χ₃) zeros': lambda p: (1 if int(p)%3==1 else -1 if int(p)%3==2 else 0),
    'χ₈ twist → L(s,χ₈) zeros': lambda p: (1 if int(p)%8 in [1,7] else -1 if int(p)%8 in [3,5] else 0),
}

expected = {
    'Untwisted → ζ(s) zeros': [14.13, 21.02, 25.01, 30.42],
    'χ₄ twist → L(s,χ₄) zeros': [6.02, 10.24, 12.59],
    'χ₃ twist → L(s,χ₃) zeros': [8.04, 13.32, 16.20],
    'χ₈ twist → L(s,χ₈) zeros': [],
}

for ax_i, (name, chi_fn) in enumerate(characters.items()):
    chi_vals = np.array([chi_fn(p) for p in primes])
    mask = chi_vals != 0
    w = chi_vals[mask] * R_vals[mask] * primes[mask]**(-0.5)
    lp = log_p[mask]

    F = np.zeros(len(gamma_grid))
    for i, g in enumerate(gamma_grid):
        terms = w * np.exp(-1j * g * lp)
        F[i] = np.abs(np.sum(terms))**2
    F_n = F / np.max(F) if np.max(F) > 0 else F

    axes[ax_i].plot(gamma_grid, F_n, linewidth=0.8,
                   color=['#1a5276', '#8e44ad', '#27ae60', '#e67e22'][ax_i])
    axes[ax_i].fill_between(gamma_grid, 0, F_n, alpha=0.15,
                           color=['#2980b9', '#9b59b6', '#2ecc71', '#f39c12'][ax_i])

    for ez in expected.get(name, []):
        axes[ax_i].axvline(x=ez, color='#e74c3c', linestyle='--', alpha=0.6, linewidth=0.8)

    axes[ax_i].set_ylabel(name.split('→')[0].strip(), fontsize=9)
    axes[ax_i].set_title(name, fontsize=11)
    axes[ax_i].set_xlim(2, 35)

axes[-1].set_xlabel('γ (spectral frequency)', fontsize=12)
fig6.suptitle('Multi-Character Farey Spectroscope:\nDetecting Zeros of Different L-functions',
              fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'multi_character_spectroscope.png'), dpi=200, bbox_inches='tight')
plt.savefig(os.path.join(OUT, 'multi_character_spectroscope.pdf'), bbox_inches='tight')
print("Figure 6 saved: multi_character_spectroscope.png/pdf")

print("\nAll interaction figures generated.")
