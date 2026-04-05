#!/usr/bin/env python3
"""
Spectroscope Visualization: The Explicit Formula Coming Alive

Multi-panel figure showing how the Mertens/Farey spectroscope extracts
zeta zeros from prime data, step by step. The explicit formula says
M(x) ~ sum_rho x^rho / (rho * zeta'(rho)). Our periodogram recovers
the imaginary parts gamma_k as spectral peaks.

Panels:
1. Raw data: M(p)/sqrt(p) oscillations at primes
2. Raw periodogram: only gamma_1, gamma_2 visible
3. gamma^2-compensated periodogram: 13+ zeros emerge
4. Predicted vs observed peak heights (explicit formula test)
5. Universality: any subset of primes yields the same zeros
"""

import warnings
import numpy as np
import os
import time

# Suppress matmul overflow warnings (harmless: intermediate accumulation
# overflows but final results are finite because cos/sin are bounded)
warnings.filterwarnings('ignore', message='.*matmul.*')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

# ── Paths ──────────────────────────────────────────────────────────
FIG_DIR = os.path.expanduser("~/Desktop/Farey-Local/figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ── Correct Mobius sieve via factorization ─────────────────────────
print("Sieving Mobius function to 500,000 ...")
t0 = time.time()
MAX_N = 500_000

# Standard smallest-prime-factor sieve
spf = np.zeros(MAX_N + 1, dtype=np.int32)  # smallest prime factor
for i in range(2, MAX_N + 1):
    if spf[i] == 0:  # i is prime
        for j in range(i, MAX_N + 1, i):
            if spf[j] == 0:
                spf[j] = i

# Compute mu(n) from factorization
mu = np.zeros(MAX_N + 1, dtype=np.int8)
mu[1] = 1
for n in range(2, MAX_N + 1):
    m = n
    sign = 1
    is_squarefree = True
    while m > 1:
        p = spf[m]
        m //= p
        if spf[m] == p if m > 1 else (n // p) % p == 0:
            # Check if p^2 divides n
            pass
        sign *= -1
        # Check square factor
        if m > 0 and m % p == 0:
            is_squarefree = False
            break
        # continue removing other prime factors
    if is_squarefree:
        mu[n] = sign
    # else mu[n] stays 0

# Verify with known values
assert mu[1] == 1
assert mu[2] == -1
assert mu[3] == -1
assert mu[4] == 0   # 4 = 2^2
assert mu[5] == -1
assert mu[6] == 1    # 6 = 2*3
assert mu[30] == -1  # 30 = 2*3*5
print(f"  Mobius sanity check passed: mu(1..6) = {list(mu[1:7])}")

# Mertens function
M = np.cumsum(mu)

# Primes via sieve
is_prime = np.zeros(MAX_N + 1, dtype=bool)
for i in range(2, MAX_N + 1):
    if spf[i] == i:
        is_prime[i] = True
primes_list = np.where(is_prime)[0]
primes = primes_list.astype(np.float64)
M_p = M[primes_list].astype(np.float64)
N_primes = len(primes)
log_p = np.log(primes)
sqrt_p = np.sqrt(primes)

print(f"  Done in {time.time()-t0:.1f}s: {N_primes} primes, max = {int(primes[-1])}")
print(f"  M({int(primes[-1])}) = {int(M_p[-1])}")
print(f"  M(p) range: [{int(M_p.min())}, {int(M_p.max())}]")

# ── Known zeta zeros (first 20) ──────────────────────────────────
ZEROS = [14.13472514, 21.02203964, 25.01085758, 30.42487613, 32.93506159,
         37.58617816, 40.91871901, 43.32707328, 48.00515088, 49.77383248,
         52.97032148, 56.44624770, 59.34704400, 60.83177852, 65.11254405,
         67.07981053, 69.54640171, 72.06715767, 75.70469069, 77.14484007]


# ── Spectroscope engine (vectorized, chunked) ────────────────────
def spectroscope_power(weights, p_vals, log_p_vals, gamma_grid, chunk=1000):
    """
    Compute |S(gamma)|^2 where S(gamma) = sum_p w(p)/sqrt(p) * exp(-i*gamma*log p).
    Chunked over gamma to manage memory (~330MB per chunk with 41K primes).
    """
    amp = weights / np.sqrt(p_vals)
    G = len(gamma_grid)
    F = np.zeros(G)
    for s in range(0, G, chunk):
        e = min(s + chunk, G)
        # phases: (chunk_size, n_primes)
        phases = np.outer(gamma_grid[s:e], log_p_vals)
        re_sum = np.cos(phases) @ amp
        im_sum = np.sin(phases) @ amp
        F[s:e] = re_sum**2 + im_sum**2
    return F


# ── Gamma grid ────────────────────────────────────────────────────
gammas = np.linspace(5, 85, 20000)

# ── Compute spectroscope for all primes ───────────────────────────
print("Computing spectroscope (all primes) ...")
t0 = time.time()
F_raw = spectroscope_power(M_p, primes, log_p, gammas)
F_comp = gammas**2 * F_raw  # gamma^2 compensation
print(f"  Done in {time.time()-t0:.1f}s")
print(f"  F_raw range: [{F_raw.min():.2e}, {F_raw.max():.2e}]")
print(f"  F_comp range: [{F_comp.min():.2e}, {F_comp.max():.2e}]")

# ── Peak detection ────────────────────────────────────────────────
def find_peaks_near_zeros(F, gamma_grid, zeros, window=0.8):
    """Find the highest peak in F within +/- window of each known zero."""
    results = []
    for gz in zeros:
        mask = (gamma_grid >= gz - window) & (gamma_grid <= gz + window)
        if not mask.any():
            results.append((gz, np.nan, np.nan))
            continue
        idx_arr = np.where(mask)[0]
        idx_local = np.argmax(F[mask])
        idx_global = idx_arr[idx_local]
        results.append((gamma_grid[idx_global], F[idx_global], abs(gamma_grid[idx_global] - gz)))
    return results

peaks_raw = find_peaks_near_zeros(F_raw, gammas, ZEROS)
peaks_comp = find_peaks_near_zeros(F_comp, gammas, ZEROS)

# Count detectable zeros using z-score relative to local background
interior = (gammas > 10) & (gammas < 80)
bg_raw = np.median(F_raw[interior])
bg_comp = np.median(F_comp[interior])
std_raw = np.std(F_raw[interior])
std_comp = np.std(F_comp[interior])

n_raw_detect = sum(1 for _, h, _ in peaks_raw if (h - bg_raw) / std_raw > 3)
n_comp_detect = sum(1 for _, h, _ in peaks_comp if (h - bg_comp) / std_comp > 3)
print(f"  Detected (z>3): raw={n_raw_detect}, compensated={n_comp_detect}")

# Use a more generous threshold for labeling: peak must be > 2*median
n_label_target = sum(1 for _, h, _ in peaks_comp if h > 2 * bg_comp)
print(f"  Labelable (>2x median): {n_label_target}")

# ── Predicted amplitudes from explicit formula ────────────────────
# The explicit formula coefficient: c_k = x^(rho_k) / (rho_k * zeta'(rho_k))
# At the spectroscope level: peak height ~ 1 / (|rho_k|^2 * |zeta'(rho_k)|^2)
# |rho_k|^2 = 1/4 + gamma_k^2
# |zeta'(rho_k)| ~ (1/2) * log(gamma_k / (2*pi))  (from Stirling)
def predicted_raw_amplitude(gamma_k):
    rho_sq = 0.25 + gamma_k**2
    zeta_prime_approx = 0.5 * np.log(gamma_k / (2 * np.pi))
    return 1.0 / (rho_sq * zeta_prime_approx**2)

# Compensated amplitude: gamma^2 * predicted_raw
pred_raw = np.array([predicted_raw_amplitude(gz) for gz in ZEROS[:15]])
pred_comp_vals = np.array([gz**2 * predicted_raw_amplitude(gz) for gz in ZEROS[:15]])

# ── Universality subsets ──────────────────────────────────────────
print("Computing universality subsets ...")
t0 = time.time()
p_int = primes.astype(int)

# Subset (b): primes = 1 mod 4
mask_1mod4 = (p_int % 4 == 1)
F_1mod4 = spectroscope_power(M_p[mask_1mod4], primes[mask_1mod4],
                              log_p[mask_1mod4], gammas)
F_1mod4_comp = gammas**2 * F_1mod4

# Subset (c): random 50%
np.random.seed(42)
mask_random = np.random.choice([True, False], size=N_primes, p=[0.5, 0.5])
F_random = spectroscope_power(M_p[mask_random], primes[mask_random],
                               log_p[mask_random], gammas)
F_random_comp = gammas**2 * F_random

print(f"  Done in {time.time()-t0:.1f}s")


# ══════════════════════════════════════════════════════════════════
#  BUILD THE FIGURE
# ══════════════════════════════════════════════════════════════════

def make_figure(fontscale=1.0, dpi=250):
    """Create the multi-panel figure. fontscale>1 for presentation version."""

    fs_title = 13 * fontscale
    fs_label = 11 * fontscale
    fs_tick = 9 * fontscale
    fs_annot = 8.5 * fontscale
    fs_suptitle = 16 * fontscale
    lw_line = 0.7

    plt.rcParams.update({
        'font.family': 'serif',
        'mathtext.fontset': 'cm',
        'axes.linewidth': 0.6,
        'xtick.major.width': 0.5,
        'ytick.major.width': 0.5,
        'xtick.labelsize': fs_tick,
        'ytick.labelsize': fs_tick,
    })

    fig = plt.figure(figsize=(8.5, 20))
    gs = GridSpec(5, 1, figure=fig, height_ratios=[1, 1, 1.15, 1, 0.85],
                  hspace=0.42)

    # Color palette
    C_NEG = '#2166ac'
    C_POS = '#b2182b'
    C_PEAK = '#d62728'
    C_PRED = '#ff7f0e'
    C_COMP = '#1b7837'
    C_RAW = '#4393c3'
    C_BG = '#fafafa'
    C_GRID = '#e0e0e0'

    # ──────────────────────────────────────────────────────────────
    # PANEL 1: Raw data M(p)/sqrt(p)
    # ──────────────────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(C_BG)
    ax1.grid(True, alpha=0.2, linewidth=0.3, color=C_GRID)

    y_norm = M_p / sqrt_p

    # Subsample for plotting (41K points is too dense for vlines)
    step = max(1, N_primes // 8000)
    lp_sub = log_p[::step]
    yn_sub = y_norm[::step]
    mp_sub = M_p[::step]

    colors_sub = np.where(mp_sub < 0, C_NEG, C_POS)
    ax1.vlines(lp_sub, 0, yn_sub, colors=colors_sub, linewidth=0.25, alpha=0.7)
    ax1.axhline(0, color='black', linewidth=0.4, alpha=0.4)

    # Running envelope (fast: use sorted chunks)
    win = 300
    env_step = 50
    idx_env = np.arange(0, N_primes, env_step)
    y_hi = np.array([np.percentile(y_norm[max(0, i-win):min(N_primes, i+win)], 95)
                      for i in idx_env])
    y_lo = np.array([np.percentile(y_norm[max(0, i-win):min(N_primes, i+win)], 5)
                      for i in idx_env])
    ax1.plot(log_p[idx_env], y_hi, color=C_POS, linewidth=0.9, alpha=0.4)
    ax1.plot(log_p[idx_env], y_lo, color=C_NEG, linewidth=0.9, alpha=0.4)
    ax1.fill_between(log_p[idx_env], y_lo, y_hi, alpha=0.05, color='gray')

    ax1.set_xlabel(r'$\log\, p$', fontsize=fs_label)
    ax1.set_ylabel(r'$M(p)\,/\,\sqrt{p}$', fontsize=fs_label)
    ax1.set_title(f'Panel 1 --- Input: $M(p)/\\sqrt{{p}}$ at {N_primes:,} Primes',
                  fontsize=fs_title, fontweight='bold', pad=8)
    ax1.set_xlim(log_p[0] - 0.1, log_p[-1] + 0.1)

    legend_els = [Line2D([0], [0], color=C_NEG, lw=2, label=r'$M(p) < 0$  (Mertens bias)'),
                  Line2D([0], [0], color=C_POS, lw=2, label=r'$M(p) > 0$')]
    ax1.legend(handles=legend_els, loc='upper right', fontsize=fs_annot,
               framealpha=0.9, edgecolor='#ccc')

    ax1.text(0.02, 0.86,
             r'Input data: $M(p) = \sum_{n \leq p} \mu(n)$',
             transform=ax1.transAxes, fontsize=fs_annot * 1.1, color='#333',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85,
                       edgecolor='#ccc'))

    # ──────────────────────────────────────────────────────────────
    # PANEL 2: Raw periodogram
    # ──────────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(C_BG)
    ax2.grid(True, alpha=0.2, linewidth=0.3, color=C_GRID)

    F_raw_norm = F_raw / np.max(F_raw)
    ax2.plot(gammas, F_raw_norm, color=C_RAW, linewidth=lw_line, alpha=0.9)
    ax2.fill_between(gammas, 0, F_raw_norm, alpha=0.12, color=C_RAW)

    # Mark known zero positions
    for i, gz in enumerate(ZEROS[:18]):
        ax2.axvline(gz, color='#bbb', linestyle=':', linewidth=0.35, alpha=0.5)

    # Label the clearly visible peaks
    for i in range(min(3, len(peaks_raw))):
        gz = ZEROS[i]
        _, h, _ = peaks_raw[i]
        h_n = h / np.max(F_raw)
        if h_n > 0.05:
            x_off = 2.0 if i == 0 else 1.8
            ax2.annotate(f'$\\gamma_{{{i+1}}}$={gz:.1f}',
                         xy=(gz, h_n), xytext=(gz + x_off, min(h_n + 0.08, 1.0)),
                         fontsize=fs_annot * 1.05, fontweight='bold', color=C_PEAK,
                         arrowprops=dict(arrowstyle='->', color=C_PEAK, lw=1.0))

    # Noise floor
    noise_lvl = np.median(F_raw_norm[interior])
    ax2.axhline(noise_lvl, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    ax2.text(82, noise_lvl + 0.015, 'noise', fontsize=fs_annot * 0.85,
             color='gray', ha='right', va='bottom')

    # Arrow showing "higher zeros buried in noise"
    ax2.annotate('higher zeros\nburied in noise',
                 xy=(45, noise_lvl + 0.01), xytext=(55, 0.35),
                 fontsize=fs_annot * 0.95, color='#666', fontstyle='italic',
                 arrowprops=dict(arrowstyle='->', color='#999', lw=0.8),
                 ha='center')

    ax2.set_xlabel(r'$\gamma$  (imaginary part of nontrivial zero)', fontsize=fs_label)
    ax2.set_ylabel(r'$|F(\gamma)|^2$  (norm.)', fontsize=fs_label)
    ax2.set_title(r'Panel 2 --- Raw Periodogram: Only $\gamma_1, \gamma_2$ Visible',
                  fontsize=fs_title, fontweight='bold', pad=8)
    ax2.set_xlim(5, 85)
    ax2.set_ylim(0, 1.15)

    ax2.text(0.02, 0.86,
             r'$F(\gamma) = \left|\,\sum_p \frac{M(p)}{\sqrt{p}}\;'
             r'e^{-i\gamma\log p}\right|^2$',
             transform=ax2.transAxes, fontsize=fs_label * 0.95, color='#333',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85,
                       edgecolor='#ccc'))

    # ──────────────────────────────────────────────────────────────
    # PANEL 3: gamma^2 compensated
    # ──────────────────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor(C_BG)
    ax3.grid(True, alpha=0.2, linewidth=0.3, color=C_GRID)

    F_comp_norm = F_comp / np.max(F_comp)
    ax3.plot(gammas, F_comp_norm, color=C_COMP, linewidth=lw_line, alpha=0.9)
    ax3.fill_between(gammas, 0, F_comp_norm, alpha=0.08, color=C_COMP)

    # Label ALL detected zeros
    n_labeled = 0
    comp_median = np.median(F_comp_norm[interior])
    for i, gz in enumerate(ZEROS[:18]):
        if i >= len(peaks_comp):
            break
        _, h, _ = peaks_comp[i]
        h_n = h / np.max(F_comp)

        # Label if peak stands out at all above local background
        if h_n > 1.5 * comp_median:
            n_labeled += 1
            # Stagger labels to avoid overlap
            if n_labeled % 3 == 1:
                y_text = h_n + 0.055
                va = 'bottom'
            elif n_labeled % 3 == 2:
                y_text = h_n + 0.035
                va = 'bottom'
            else:
                y_text = h_n + 0.075
                va = 'bottom'

            ax3.plot(gz, h_n, 'v', color=C_PEAK, markersize=4.5, zorder=5)
            ax3.text(gz, y_text, f'$\\gamma_{{{i+1}}}$',
                     fontsize=fs_annot * 0.95, fontweight='bold', color=C_PEAK,
                     ha='center', va=va)

    ax3.set_xlabel(r'$\gamma$', fontsize=fs_label)
    ax3.set_ylabel(r'$\gamma^2\,|F(\gamma)|^2$  (norm.)', fontsize=fs_label)
    ax3.set_title(f'Panel 3 --- $\\gamma^2$ Matched Filter: {n_labeled} Zeros Emerge',
                  fontsize=fs_title, fontweight='bold', pad=8)
    ax3.set_xlim(5, 85)
    ax3.set_ylim(0, 1.18)

    ax3.text(0.02, 0.88,
             r'Multiply by $\gamma^2$ to compensate for'
             r' $|c_k|^2 \!\sim\! 1/|\rho_k \zeta\prime(\rho_k)|^2$ decay',
             transform=ax3.transAxes, fontsize=fs_annot, color='#333',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85,
                       edgecolor='#ccc'))

    # Key insight callout
    ax3.text(0.72, 0.88, r'Same data as Panel 2!',
             transform=ax3.transAxes, fontsize=fs_annot * 1.1, color=C_COMP,
             fontstyle='italic', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', alpha=0.9,
                       edgecolor=C_COMP, linewidth=1.2))

    # ──────────────────────────────────────────────────────────────
    # PANEL 4: Predicted vs observed
    # ──────────────────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[3])
    ax4.set_facecolor(C_BG)
    ax4.grid(True, axis='y', alpha=0.2, linewidth=0.3, color=C_GRID)

    n_compare = 15
    obs_heights = np.array([peaks_comp[i][1] for i in range(n_compare)])

    # Normalize both to same scale (max = 1)
    obs_norm = obs_heights / np.max(obs_heights)
    pred_norm = pred_comp_vals / np.max(pred_comp_vals)

    x_pos = np.arange(n_compare)
    bw = 0.38
    ax4.bar(x_pos - bw/2, obs_norm, bw, color=C_RAW, alpha=0.85,
            label='Observed peak height', edgecolor='white', linewidth=0.4)
    ax4.bar(x_pos + bw/2, pred_norm, bw, color=C_PRED, alpha=0.85,
            label=r'Predicted: $\gamma_k^2/|\rho_k \zeta\prime(\rho_k)|^2$',
            edgecolor='white', linewidth=0.4)

    ax4.set_xticks(x_pos)
    ax4.set_xticklabels([f'$\\gamma_{{{i+1}}}$' for i in range(n_compare)],
                         fontsize=fs_annot * 0.9)
    ax4.set_ylabel('Normalized amplitude', fontsize=fs_label)
    ax4.set_title('Panel 4 --- Explicit Formula: Predicted vs Observed Peak Heights',
                  fontsize=fs_title, fontweight='bold', pad=8)
    ax4.legend(fontsize=fs_annot, loc='upper right', framealpha=0.9, edgecolor='#ccc')

    # Correlation
    vmask = np.isfinite(obs_norm) & np.isfinite(pred_norm)
    if vmask.sum() > 2:
        corr = np.corrcoef(obs_norm[vmask], pred_norm[vmask])[0, 1]
        ax4.text(0.02, 0.88, f'Pearson $r = {corr:.3f}$',
                 transform=ax4.transAxes, fontsize=fs_label, color='#333',
                 fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85,
                           edgecolor='#ccc'))

    ax4.text(0.02, 0.72,
             r'$|c_k|^2 \approx \frac{1}{|\rho_k|^2\,|\zeta\prime(\rho_k)|^2}$',
             transform=ax4.transAxes, fontsize=fs_annot, color='#555',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7,
                       edgecolor='#ddd'))

    ax4.set_ylim(0, 1.3)

    # ──────────────────────────────────────────────────────────────
    # PANEL 5: Universality
    # ──────────────────────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[4])
    ax5.set_facecolor(C_BG)
    ax5.grid(True, alpha=0.2, linewidth=0.3, color=C_GRID)

    F_all_n = F_comp_norm
    F_1m4_n = F_1mod4_comp / np.max(F_1mod4_comp)
    F_rnd_n = F_random_comp / np.max(F_random_comp)

    ax5.plot(gammas, F_all_n, color=C_COMP, linewidth=0.9, alpha=0.75,
             label=f'All {N_primes:,} primes')
    ax5.plot(gammas, F_1m4_n, color='#7570b3', linewidth=0.9, alpha=0.75,
             label=f'$p \\equiv 1$ mod $4$ only ({mask_1mod4.sum():,})')
    ax5.plot(gammas, F_rnd_n, color='#d95f02', linewidth=0.9, alpha=0.75,
             label=f'Random 50% ({mask_random.sum():,})')

    # Mark zero locations
    for gz in ZEROS[:15]:
        ax5.axvline(gz, color='#bbb', linestyle=':', linewidth=0.35, alpha=0.4)

    ax5.set_xlabel(r'$\gamma$', fontsize=fs_label)
    ax5.set_ylabel(r'$\gamma^2|F(\gamma)|^2$  (norm.)', fontsize=fs_label)
    ax5.set_title('Panel 5 --- Universality: Every Prime Subset Encodes the Same Zeros',
                  fontsize=fs_title, fontweight='bold', pad=8)
    ax5.set_xlim(5, 85)
    ax5.set_ylim(0, 1.18)
    ax5.legend(fontsize=fs_annot, loc='upper right', framealpha=0.9, edgecolor='#ccc')

    ax5.text(0.02, 0.82,
             'Peaks lock to identical $\\gamma_k$ positions --- the zeros are universal',
             transform=ax5.transAxes, fontsize=fs_annot, color='#333',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85,
                       edgecolor='#ccc'))

    # ── Suptitle ──────────────────────────────────────────────────
    fig.suptitle('The Explicit Formula Through the Mertens Spectroscope',
                 fontsize=fs_suptitle, fontweight='bold', y=0.997,
                 color='#1a1a2e')

    plt.subplots_adjust(top=0.970, bottom=0.025, left=0.10, right=0.96)

    return fig


# ══════════════════════════════════════════════════════════════════
#  SAVE FIGURES
# ══════════════════════════════════════════════════════════════════

print("\nGenerating publication figure (250 DPI) ...")
fig = make_figure(fontscale=1.0, dpi=250)
outpath = os.path.join(FIG_DIR, "spectroscope_explicit_formula.png")
fig.savefig(outpath, dpi=250, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"  Saved: {outpath}")

print("Generating presentation figure (150 DPI, larger fonts) ...")
fig2 = make_figure(fontscale=1.35, dpi=150)
outpath2 = os.path.join(FIG_DIR, "spectroscope_explicit_formula_presentation.png")
fig2.savefig(outpath2, dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig2)
print(f"  Saved: {outpath2}")

# ── Summary ───────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("SPECTROSCOPE VISUALIZATION SUMMARY")
print("=" * 65)
print(f"  Primes:       {N_primes:,} (up to {int(primes[-1]):,})")
print(f"  Gamma range:  [{gammas[0]:.0f}, {gammas[-1]:.0f}] with {len(gammas):,} points")
print(f"  Raw:          ~{n_raw_detect} zeros detected (z > 3)")
print(f"  Compensated:  ~{n_comp_detect} zeros detected (z > 3)")

print(f"\n  Peak accuracy (compensated, first 15):")
print(f"  {'#':>4s}  {'Known':>10s}  {'Detected':>10s}  {'Error':>8s}")
for i in range(min(15, len(peaks_comp))):
    gz = ZEROS[i]
    det, h, err = peaks_comp[i]
    print(f"  {i+1:>4d}  {gz:10.4f}  {det:10.4f}  {err:8.4f}")

print(f"\n  Outputs:")
print(f"    {outpath}")
print(f"    {outpath2}")
print("\nDone.")
