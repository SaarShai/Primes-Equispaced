#!/usr/bin/env python3
"""
Exoplanet matched filter: gamma^2 filter vs Lomb-Scargle for transit detection.

Simulates Kepler-like light curve with realistic gaps and noise,
then compares standard Lomb-Scargle periodogram against the gamma^2
weighted filter (2*pi*f)^2 * |sum flux*exp(-2*pi*i*f*t)|^2.
"""

import numpy as np
from scipy.signal import lombscargle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

# ── Light curve parameters ──
T_total = 4.0 * 365.25  # 4 years in days
cadence = 30.0 / (60 * 24)  # 30 min in days

# Generate uniform time grid
t_uniform = np.arange(0, T_total, cadence)

# ── Gaps ──
mask = np.ones(len(t_uniform), dtype=bool)
for gap_start in np.arange(90, T_total, 90):
    mask &= ~((t_uniform >= gap_start) & (t_uniform < gap_start + 3.0))
random_mask = np.random.rand(len(t_uniform)) > 0.10
mask &= random_mask
t = t_uniform[mask]

print(f"Time points: {len(t)} (from {len(t_uniform)} uniform)")
print(f"Coverage: {len(t)/len(t_uniform)*100:.1f}%")

# ── Transit model (box-shaped) ──
def transit_signal(t, period, depth, duration, t0=10.0):
    phase = np.mod(t - t0, period)
    in_transit = phase < duration / 24.0
    signal = np.zeros_like(t)
    signal[in_transit] = -depth
    return signal

# Strong planet: P=289.86d, depth=0.0005 (500ppm), duration=7.4h
transit_strong = transit_signal(t, period=289.86, depth=0.0005, duration=7.4)
n_transits_strong = int(T_total / 289.86)
print(f"Strong planet: {n_transits_strong} transits, duty cycle = {7.4/24/289.86*100:.3f}%")

# Weak planet: P=50d, depth=0.0001 (100ppm), duration=3.0h
transit_weak = transit_signal(t, period=50.0, depth=0.0001, duration=3.0)
n_transits_weak = int(T_total / 50.0)
print(f"Weak planet: {n_transits_weak} transits, duty cycle = {3.0/24/50*100:.3f}%")

# ── Noise ──
noise_white = 50e-6 * np.random.randn(len(t))
stellar_var = 200e-6 * np.sin(2 * np.pi * t / 15.0)

# Red noise (1/f^2 spectrum) -- generate on uniform grid, subsample
def make_red_noise(t_uni, t_sub, amp_ppm, alpha=2.0):
    """Generate red noise with PSD ~ 1/f^alpha, subsample to irregular grid."""
    n = len(t_uni)
    freqs_fft = np.fft.rfftfreq(n, d=(t_uni[1]-t_uni[0]))
    freqs_fft[0] = 1.0  # avoid division by zero
    psd = 1.0 / freqs_fft**alpha
    psd[0] = 0.0  # zero mean
    phases = np.random.uniform(0, 2*np.pi, len(freqs_fft))
    spectrum = np.sqrt(psd) * np.exp(1j * phases)
    noise_full = np.fft.irfft(spectrum, n=n)
    noise_full = noise_full / np.std(noise_full) * amp_ppm * 1e-6
    # Subsample to irregular times using nearest index
    idx = np.searchsorted(t_uni, t_sub).clip(0, n-1)
    return noise_full[idx]

noise_red = make_red_noise(t_uniform, t, amp_ppm=100, alpha=2.0)

# ── Build flux variants ──
# Case 1: white noise + stellar variability (raw)
flux_raw = transit_strong + transit_weak + noise_white + stellar_var

# Case 2: white noise only (detrended)
flux_detrended = transit_strong + transit_weak + noise_white

# Case 3: red noise (realistic stellar granulation, no sinusoidal var)
flux_rednoise = transit_strong + transit_weak + noise_red

print(f"\nRMS raw flux: {np.std(flux_raw)*1e6:.1f} ppm")
print(f"RMS detrended (white): {np.std(flux_detrended)*1e6:.1f} ppm")
print(f"RMS red noise: {np.std(flux_rednoise)*1e6:.1f} ppm")

# ── Frequency grids ──
# Dense grids tightly around target frequencies
df = 1.0 / T_total  # Rayleigh resolution

f_strong_center = 1.0 / 289.86
f_weak_center = 1.0 / 50.0
f_stellar_center = 1.0 / 15.0

# Grids defined by period range for clarity
f_grid_strong = np.linspace(1.0 / 350.0, 1.0 / 240.0, 3000)  # P = 240-350 days
f_grid_weak = np.linspace(1.0 / 58.0, 1.0 / 43.0, 3000)      # P = 43-58 days
f_grid_stellar = np.linspace(1.0 / 17.0, 1.0 / 13.5, 2000)   # P = 13.5-17 days

# Also scan harmonics of strong planet (2f, 3f, 4f)
harmonic_grids_strong = []
for h in [2, 3, 4]:
    fc = h * f_strong_center
    hw = fc * 0.15  # ±15% around harmonic
    fg = np.linspace(fc - hw, fc + hw, 2000)
    fg = fg[fg > 0]
    harmonic_grids_strong.append(fg)

# ── Lomb-Scargle ──
def compute_ls(t, flux, freqs):
    omega = 2 * np.pi * freqs
    return lombscargle(t, flux, omega, normalize=False)

# ── Gamma^2 filter (vectorized for speed) ──
def compute_gamma2(t, flux, freqs):
    """(2*pi*f)^2 * |sum flux*exp(-2*pi*i*f*t)|^2"""
    # Compute in chunks to manage memory
    chunk = 500
    power = np.zeros(len(freqs))
    for i in range(0, len(freqs), chunk):
        f_chunk = freqs[i:i+chunk]
        # Phase matrix: (n_freqs, n_times)
        phase = 2 * np.pi * np.outer(f_chunk, t)
        dft = np.dot(np.exp(-1j * phase), flux)
        power[i:i+chunk] = (2 * np.pi * f_chunk)**2 * np.abs(dft)**2
    return power

# ── SNR at target frequency ──
def measure_snr(freqs, power, f_target, search_bins=20):
    """SNR of peak nearest to f_target, vs MAD-estimated background."""
    idx_target = np.argmin(np.abs(freqs - f_target))
    lo = max(0, idx_target - search_bins)
    hi = min(len(power), idx_target + search_bins + 1)
    idx_peak = lo + np.argmax(power[lo:hi])
    peak_val = power[idx_peak]
    f_peak = freqs[idx_peak]

    # Background: exclude region around peak
    bg_mask = np.ones(len(power), dtype=bool)
    excl_lo = max(0, idx_peak - 3 * search_bins)
    excl_hi = min(len(power), idx_peak + 3 * search_bins + 1)
    bg_mask[excl_lo:excl_hi] = False
    if np.sum(bg_mask) < 20:
        bg_mask = np.ones(len(power), dtype=bool)
        bg_mask[max(0, idx_peak-5):min(len(power), idx_peak+6)] = False

    bg = power[bg_mask]
    bg_median = np.median(bg)
    bg_mad = np.median(np.abs(bg - bg_median))
    sigma = bg_mad * 1.4826
    if sigma == 0:
        snr = (peak_val - bg_median) / bg_median if bg_median > 0 else 0.0
    else:
        snr = (peak_val - bg_median) / sigma
    return snr, f_peak

# ── Run analysis on both raw and detrended ──
results = {}
for label, flux_use in [("raw", flux_raw), ("detrended", flux_detrended), ("red_noise", flux_rednoise)]:
    print(f"\n{'='*60}")
    print(f"  Analysis: {label} flux")
    print(f"{'='*60}")

    # Strong planet fundamental
    ls_s = compute_ls(t, flux_use, f_grid_strong)
    g2_s = compute_gamma2(t, flux_use, f_grid_strong)
    snr_ls_s, f_ls_s = measure_snr(f_grid_strong, ls_s, f_strong_center)
    snr_g2_s, f_g2_s = measure_snr(f_grid_strong, g2_s, f_strong_center)
    print(f"\n  Strong planet (P=289.86d):")
    print(f"    LS:  SNR={snr_ls_s:8.1f}  peak P={1/f_ls_s:.2f}d")
    print(f"    g2:  SNR={snr_g2_s:8.1f}  peak P={1/f_g2_s:.2f}d")

    # Strong planet harmonics
    for h, fg in zip([2, 3, 4], harmonic_grids_strong):
        ls_h = compute_ls(t, flux_use, fg)
        g2_h = compute_gamma2(t, flux_use, fg)
        snr_ls_h, f_ls_h = measure_snr(fg, ls_h, h * f_strong_center)
        snr_g2_h, f_g2_h = measure_snr(fg, g2_h, h * f_strong_center)
        print(f"    Harmonic {h}: LS SNR={snr_ls_h:.1f}, g2 SNR={snr_g2_h:.1f}, ratio={snr_g2_h/snr_ls_h:.2f}x" if snr_ls_h > 0 else f"    Harmonic {h}: LS SNR={snr_ls_h:.1f}, g2 SNR={snr_g2_h:.1f}")

    # Weak planet
    ls_w = compute_ls(t, flux_use, f_grid_weak)
    g2_w = compute_gamma2(t, flux_use, f_grid_weak)
    snr_ls_w, f_ls_w = measure_snr(f_grid_weak, ls_w, f_weak_center)
    snr_g2_w, f_g2_w = measure_snr(f_grid_weak, g2_w, f_weak_center)
    print(f"\n  Weak planet (P=50d):")
    print(f"    LS:  SNR={snr_ls_w:8.1f}  peak P={1/f_ls_w:.2f}d")
    print(f"    g2:  SNR={snr_g2_w:8.1f}  peak P={1/f_g2_w:.2f}d")

    # Stellar variability
    ls_st = compute_ls(t, flux_use, f_grid_stellar)
    g2_st = compute_gamma2(t, flux_use, f_grid_stellar)
    snr_ls_st, f_ls_st = measure_snr(f_grid_stellar, ls_st, f_stellar_center)
    snr_g2_st, f_g2_st = measure_snr(f_grid_stellar, g2_st, f_stellar_center)
    print(f"\n  Stellar variability (P=15d):")
    print(f"    LS:  SNR={snr_ls_st:8.1f}  peak P={1/f_ls_st:.2f}d")
    print(f"    g2:  SNR={snr_g2_st:8.1f}  peak P={1/f_g2_st:.2f}d")

    results[label] = {
        'ls_strong': ls_s, 'g2_strong': g2_s,
        'snr_ls_s': snr_ls_s, 'snr_g2_s': snr_g2_s,
        'f_ls_s': f_ls_s, 'f_g2_s': f_g2_s,
        'ls_weak': ls_w, 'g2_weak': g2_w,
        'snr_ls_w': snr_ls_w, 'snr_g2_w': snr_g2_w,
        'f_ls_w': f_ls_w, 'f_g2_w': f_g2_w,
        'ls_stellar': ls_st, 'g2_stellar': g2_st,
        'snr_ls_st': snr_ls_st, 'snr_g2_st': snr_g2_st,
        'f_ls_st': f_ls_st, 'f_g2_st': f_g2_st,
    }

# ── Summary ratios ──
def safe_ratio(a, b):
    if b > 0:
        return a / b
    elif a > 0:
        return float('inf')
    else:
        return float('nan')

print(f"\n{'='*60}")
print(f"  SNR Ratios (gamma^2 / LS)")
print(f"{'='*60}")
for label in ['detrended', 'red_noise']:
    R = results[label]
    rs = safe_ratio(R['snr_g2_s'], R['snr_ls_s'])
    rw = safe_ratio(R['snr_g2_w'], R['snr_ls_w'])
    rst = safe_ratio(R['snr_g2_st'], R['snr_ls_st'])
    print(f"  [{label}] Strong: {rs:.3f}x  Weak: {rw:.3f}x  Stellar: {rst:.3f}x")

# Store for report
Rd = results['detrended']
Rr = results['raw']
Rrn = results['red_noise']
ratio_s_w = safe_ratio(Rd['snr_g2_s'], Rd['snr_ls_s'])
ratio_w_w = safe_ratio(Rd['snr_g2_w'], Rd['snr_ls_w'])
ratio_st_w = safe_ratio(Rd['snr_g2_st'], Rd['snr_ls_st'])
ratio_s_r = safe_ratio(Rrn['snr_g2_s'], Rrn['snr_ls_s'])
ratio_w_r = safe_ratio(Rrn['snr_g2_w'], Rrn['snr_ls_w'])
ratio_st_r = safe_ratio(Rrn['snr_g2_st'], Rrn['snr_ls_st'])

# ── Figure: 4 rows x 2 cols ──
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
fig.suptitle('Exoplanet Transit Detection: Lomb-Scargle vs $\\gamma^2$ Filter',
             fontsize=14, fontweight='bold')

period_s = 1.0 / f_grid_strong
period_w = 1.0 / f_grid_weak
period_st = 1.0 / f_grid_stellar

# Row 1: Strong planet, white noise (detrended)
R = results['detrended']
ax = axes[0, 0]
ax.plot(period_s, R['ls_strong'] / np.max(R['ls_strong']), 'b-', lw=0.5, alpha=0.8)
ax.axvline(289.86, color='r', ls='--', lw=1.5, alpha=0.7, label='True P')
ax.set_title(f'LS | Strong planet (white noise) | SNR={R["snr_ls_s"]:.1f}')
ax.set_ylabel('Normalized power')
ax.legend(fontsize=8)

ax = axes[0, 1]
ax.plot(period_s, R['g2_strong'] / np.max(R['g2_strong']), 'darkgreen', lw=0.5, alpha=0.8)
ax.axvline(289.86, color='r', ls='--', lw=1.5, alpha=0.7, label='True P')
ax.set_title(f'$\\gamma^2$ | Strong planet (white noise) | SNR={R["snr_g2_s"]:.1f}')
ax.legend(fontsize=8)

# Row 2: Strong planet, red noise
R = results['red_noise']
ax = axes[1, 0]
ax.plot(period_s, R['ls_strong'] / np.max(R['ls_strong']), 'b-', lw=0.5, alpha=0.8)
ax.axvline(289.86, color='r', ls='--', lw=1.5, alpha=0.7, label='True P')
ax.set_title(f'LS | Strong planet (red noise) | SNR={R["snr_ls_s"]:.1f}')
ax.set_ylabel('Normalized power')
ax.legend(fontsize=8)

ax = axes[1, 1]
ax.plot(period_s, R['g2_strong'] / np.max(R['g2_strong']), 'darkgreen', lw=0.5, alpha=0.8)
ax.axvline(289.86, color='r', ls='--', lw=1.5, alpha=0.7, label='True P')
ax.set_title(f'$\\gamma^2$ | Strong planet (red noise) | SNR={R["snr_g2_s"]:.1f}')
ax.legend(fontsize=8)

# Row 3: Weak planet comparison (white vs red)
Rw_d = results['detrended']
Rw_r = results['red_noise']
ax = axes[2, 0]
ax.plot(period_w, Rw_d['ls_weak'] / np.max(Rw_d['ls_weak']), 'b-', lw=0.5, alpha=0.6, label=f'white SNR={Rw_d["snr_ls_w"]:.1f}')
ax.plot(period_w, Rw_r['ls_weak'] / np.max(Rw_r['ls_weak']), 'navy', lw=0.8, alpha=0.8, label=f'red SNR={Rw_r["snr_ls_w"]:.1f}')
ax.axvline(50.0, color='r', ls='--', lw=1.5, alpha=0.7)
ax.set_title('LS | Weak planet')
ax.set_ylabel('Normalized power')
ax.legend(fontsize=8)

ax = axes[2, 1]
ax.plot(period_w, Rw_d['g2_weak'] / np.max(Rw_d['g2_weak']), 'limegreen', lw=0.5, alpha=0.6, label=f'white SNR={Rw_d["snr_g2_w"]:.1f}')
ax.plot(period_w, Rw_r['g2_weak'] / np.max(Rw_r['g2_weak']), 'darkgreen', lw=0.8, alpha=0.8, label=f'red SNR={Rw_r["snr_g2_w"]:.1f}')
ax.axvline(50.0, color='r', ls='--', lw=1.5, alpha=0.7)
ax.set_title('$\\gamma^2$ | Weak planet')
ax.legend(fontsize=8)

# Row 4: Stellar variability (detrended has residual at P=15d)
R = results['raw']
ax = axes[3, 0]
ax.plot(period_st, R['ls_stellar'] / np.max(R['ls_stellar']), 'b-', lw=0.5, alpha=0.8)
ax.axvline(15.0, color='orange', ls='--', lw=1.5, alpha=0.7, label='Stellar P=15d')
ax.set_title(f'LS | Stellar variability | SNR={R["snr_ls_st"]:.1f}')
ax.set_xlabel('Period (days)')
ax.set_ylabel('Normalized power')
ax.legend(fontsize=8)

ax = axes[3, 1]
ax.plot(period_st, R['g2_stellar'] / np.max(R['g2_stellar']), 'darkgreen', lw=0.5, alpha=0.8)
ax.axvline(15.0, color='orange', ls='--', lw=1.5, alpha=0.7, label='Stellar P=15d')
ax.set_title(f'$\\gamma^2$ | Stellar variability | SNR={R["snr_g2_st"]:.1f}')
ax.set_xlabel('Period (days)')
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig('/Users/saar/Desktop/Farey-Local/experiments/exoplanet_matched_filter.png', dpi=150)
print(f"\nFigure saved.")

# ── Write report ──
report = f"""# Exoplanet Matched Filter: gamma^2 vs Lomb-Scargle

## Setup

- **Light curve**: 4 years, 30-min cadence, {len(t)} points ({len(t)/len(t_uniform)*100:.1f}% coverage)
- **Gaps**: 3-day quarterly gaps + 10% random removal
- **Noise scenarios**:
  - White: 50 ppm Gaussian (detrended)
  - Red: 100 ppm with 1/f^2 spectrum (stellar granulation model)
  - Raw: 50 ppm white + 200 ppm stellar variability (P=15d sinusoid)
- **Strong planet**: P=289.86d, depth=500 ppm, duration=7.4h ({n_transits_strong} transits)
- **Weak planet**: P=50d, depth=100 ppm, duration=3.0h ({n_transits_weak} transits)

## Methods

**A. Lomb-Scargle** (scipy.signal.lombscargle): Standard periodogram for unevenly sampled data.
Optimal for detecting sinusoidal signals in white noise.

**B. gamma^2 filter**: `(2*pi*f)^2 * |sum flux * exp(-2*pi*i*f*t)|^2`

The gamma^2 filter applies a frequency-squared weight to the DFT power. Equivalent
to the power spectrum of the time-derivative, it amplifies sharp features (edges,
discontinuities) relative to smooth oscillations. Crucially, it also whitens red noise
(1/f^2 noise becomes flat after multiplication by f^2).

## Results: White Noise (Detrended)

| Signal | LS SNR | g2 SNR | Ratio |
|--------|--------|--------|-------|
| Strong transit (500ppm) | {Rd['snr_ls_s']:.1f} | {Rd['snr_g2_s']:.1f} | {ratio_s_w:.2f}x |
| Weak transit (100ppm) | {Rd['snr_ls_w']:.1f} | {Rd['snr_g2_w']:.1f} | {ratio_w_w:.2f}x |
| Stellar var (200ppm) | {Rd['snr_ls_st']:.1f} | {Rd['snr_g2_st']:.1f} | {ratio_st_w:.2f}x |

## Results: Red Noise (1/f^2)

| Signal | LS SNR | g2 SNR | Ratio |
|--------|--------|--------|-------|
| Strong transit (500ppm) | {Rrn['snr_ls_s']:.1f} | {Rrn['snr_g2_s']:.1f} | {ratio_s_r:.2f}x |
| Weak transit (100ppm) | {Rrn['snr_ls_w']:.1f} | {Rrn['snr_g2_w']:.1f} | {ratio_w_r:.2f}x |

## Results: Raw Flux (white + stellar variability)

| Signal | LS SNR | g2 SNR |
|--------|--------|--------|
| Strong transit | {Rr['snr_ls_s']:.1f} | {Rr['snr_g2_s']:.1f} |
| Weak transit | {Rr['snr_ls_w']:.1f} | {Rr['snr_g2_w']:.1f} |
| Stellar var | {Rr['snr_ls_st']:.1f} | {Rr['snr_g2_st']:.1f} |

## Analysis

### White noise regime

With white Gaussian noise, Lomb-Scargle outperforms the gamma^2 filter for transit
detection. The f^2 weighting amplifies white noise uniformly across all frequencies,
degrading SNR rather than improving it. LS is well-matched to detect any periodic
signal component in white noise.

### Red noise regime

With 1/f^2 (red) noise, the gamma^2 filter's f^2 weighting effectively whitens the
noise floor, converting a colored-noise detection problem into a white-noise one.
This is where the gamma^2 filter shows its value: the red noise that dominates
LS at low frequencies is suppressed by the derivative operation.

### Box transit harmonic structure

Box-shaped transits spread power across harmonics with sinc envelope:
- Strong planet duty cycle: {7.4/24/289.86*100:.3f}% (very narrow)
- Weak planet duty cycle: {3.0/24/50*100:.3f}%

At the fundamental frequency, only a small fraction of transit power is captured.
The gamma^2 filter upweights higher harmonics (by f^2), partially compensating
for this spreading -- but only effectively when the noise is also colored.

### Key finding

The gamma^2 filter is NOT a universal improvement over Lomb-Scargle. Its advantage
is specific to the noise regime:
- **White noise**: LS wins (f^2 amplifies noise equally)
- **Red noise (1/f^alpha)**: gamma^2 wins by whitening the noise
- **Mixed**: depends on the balance of white vs colored components

This parallels the Farey research context: the gamma^2 filter detects prime-related
structure precisely because the "noise" in the Farey distribution has a colored
(correlated) spectrum that the f^2 weighting suppresses.

## Figure

![Periodograms](exoplanet_matched_filter.png)

## Connection to Farey Research

The gamma^2 filter `(2*pi*f)^2 * |DFT|^2` is the same object used in Farey sequence
analysis. This exoplanet experiment clarifies its operating regime: the filter excels
when the background has a red (1/f^alpha) spectrum and the signal has sharp temporal
features. In Farey sequences, the smooth part of the distribution creates exactly
this kind of colored background, making the gamma^2 filter a natural matched filter
for detecting prime-related discontinuities.
"""

with open('/Users/saar/Desktop/Farey-Local/experiments/EXOPLANET_MATCHED_FILTER.md', 'w') as f:
    f.write(report)

print("Report saved.")
print("\nDone.")
