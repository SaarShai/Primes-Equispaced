#!/usr/bin/env python3
"""
Pink Noise & Zeta-Zero Correlations in ΔW Fluctuations
=======================================================

The sign-magnitude agent discovered that |ΔW| magnitude fluctuations behave
as pink noise with spectral slope f^{-1.18} and autocorrelation 0.91.

This script rigorously tests whether these fluctuations encode information
about the non-trivial zeros of the Riemann zeta function.

Four investigations:
1. Spectral density of {ΔW(p_n)·p_n²} — is f^{-1.18} robust? Compare to GUE f^{-1}.
2. Full autocorrelation function — does it match Montgomery's pair correlation?
3. Fourier peaks at zeta-zero imaginary parts γ_k.
4. Mertens function oscillations in ΔW — detecting zeta-zero content.
"""

import numpy as np
import pandas as pd
from scipy import signal, fft
from scipy.stats import linregress
import warnings
warnings.filterwarnings('ignore')

# ─── Load data ───────────────────────────────────────────────────────────────

DATA_PATH = "wobble_primes_100000.csv"
df = pd.read_csv(DATA_PATH)

primes = df['p'].values.astype(float)
delta_w = df['delta_w'].values.astype(float)
mertens = df['mertens_p'].values.astype(float)
N = len(primes)

print(f"Loaded {N} primes from {primes[0]:.0f} to {primes[-1]:.0f}")
print(f"Mean ΔW = {np.mean(delta_w):.6e}")
print(f"Std  ΔW = {np.std(delta_w):.6e}")
print()

# The scaled sequence: ΔW(p_n) · p_n²
scaled_dw = delta_w * primes**2

print(f"Scaled sequence ΔW·p²: mean={np.mean(scaled_dw):.4f}, std={np.std(scaled_dw):.4f}")
print()

# Known first 30 zeta zeros (imaginary parts)
ZETA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
]

results = {}

# ═══════════════════════════════════════════════════════════════════════════════
# INVESTIGATION 1: Spectral Density of {ΔW·p²}
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("INVESTIGATION 1: SPECTRAL DENSITY OF {ΔW(p_n)·p_n²}")
print("=" * 72)

# Detrend and window the signal
x = scaled_dw - np.mean(scaled_dw)
window = signal.windows.hann(N)
x_windowed = x * window

# Compute power spectral density using Welch's method
# Use several segment lengths to test robustness
slopes_welch = []
for nperseg in [512, 1024, 2048, 4096]:
    if nperseg > N:
        continue
    freqs_w, psd_w = signal.welch(x, nperseg=nperseg, noverlap=nperseg // 2)
    # Fit log-log slope excluding DC
    mask = freqs_w > 0
    log_f = np.log10(freqs_w[mask])
    log_p = np.log10(psd_w[mask])
    # Fit in the middle range (avoid edges)
    mid = (log_f > np.percentile(log_f, 10)) & (log_f < np.percentile(log_f, 90))
    slope, intercept, r_value, p_value, std_err = linregress(log_f[mid], log_p[mid])
    slopes_welch.append((nperseg, slope, r_value**2, std_err))
    print(f"  Welch (nperseg={nperseg}): slope = {slope:.4f}, R² = {r_value**2:.4f}, SE = {std_err:.4f}")

# Also use periodogram (raw FFT)
freqs_p, psd_p = signal.periodogram(x, window='hann')
mask = freqs_p > 0
log_f = np.log10(freqs_p[mask])
log_p = np.log10(psd_p[mask] + 1e-30)

# Bin the periodogram for cleaner fit
n_bins = 200
bin_edges = np.linspace(log_f.min(), log_f.max(), n_bins + 1)
bin_centers = []
bin_means = []
for i in range(n_bins):
    in_bin = (log_f >= bin_edges[i]) & (log_f < bin_edges[i + 1])
    if np.sum(in_bin) > 0:
        bin_centers.append((bin_edges[i] + bin_edges[i + 1]) / 2)
        bin_means.append(np.mean(log_p[in_bin]))

bin_centers = np.array(bin_centers)
bin_means = np.array(bin_means)

# Fit over different frequency ranges to check robustness
print("\n  Binned periodogram slopes over different frequency ranges:")
for lo_pct, hi_pct, label in [(5, 95, "full"), (5, 50, "low-freq"), (50, 95, "high-freq"), (20, 80, "mid-range")]:
    lo = np.percentile(bin_centers, lo_pct)
    hi = np.percentile(bin_centers, hi_pct)
    mask_fit = (bin_centers >= lo) & (bin_centers <= hi)
    if np.sum(mask_fit) < 5:
        continue
    sl, inter, rv, pv, se = linregress(bin_centers[mask_fit], bin_means[mask_fit])
    print(f"    {label:12s}: slope = {sl:.4f}, R² = {rv**2:.4f}")

# Consensus slope
all_slopes = [s[1] for s in slopes_welch]
mean_slope = np.mean(all_slopes)
print(f"\n  >>> Consensus Welch slope: {mean_slope:.4f} ± {np.std(all_slopes):.4f}")
print(f"  >>> GUE prediction: -1.0")
print(f"  >>> Previous measurement: -1.18")

results['spectral_slope'] = mean_slope
results['spectral_slope_std'] = np.std(all_slopes)

# Test: is the spectrum consistent with f^{-1} (GUE)?
gue_deviation = abs(mean_slope - (-1.0))
print(f"  >>> Deviation from GUE f^{{-1}}: {gue_deviation:.4f}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# INVESTIGATION 2: Full Autocorrelation Function vs Montgomery Pair Correlation
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("INVESTIGATION 2: AUTOCORRELATION vs MONTGOMERY PAIR CORRELATION")
print("=" * 72)

# Compute autocorrelation of |ΔW| magnitudes (as the agent measured)
mag_dw = np.abs(delta_w)
mag_dw_centered = mag_dw - np.mean(mag_dw)

# Full autocorrelation via FFT
fft_mag = np.fft.fft(mag_dw_centered, n=2 * N)
acf_raw = np.fft.ifft(np.abs(fft_mag) ** 2).real[:N]
acf_normalized = acf_raw / acf_raw[0]

print(f"  Autocorrelation of |ΔW| at lag k (consecutive primes):")
for k in range(11):
    print(f"    lag {k:2d}: r = {acf_normalized[k]:.6f}")

# Also compute autocorrelation of the scaled sequence
sc_centered = scaled_dw - np.mean(scaled_dw)
fft_sc = np.fft.fft(sc_centered, n=2 * N)
acf_sc_raw = np.fft.ifft(np.abs(fft_sc) ** 2).real[:N]
acf_sc = acf_sc_raw / acf_sc_raw[0]

print(f"\n  Autocorrelation of ΔW·p² at lag k:")
for k in range(11):
    print(f"    lag {k:2d}: r = {acf_sc[k]:.6f}")

# Montgomery's pair correlation: 1 - (sin(πu)/(πu))²
# For discrete lags, u relates to normalized spacing
# The prediction is that for large random matrices (GUE), the pair correlation
# function g(u) = 1 - (sin(πu)/(πu))² describes the correlations between
# zeta zeros. For our prime-indexed sequence, we check if the ACF decay
# follows this shape.

print(f"\n  Montgomery pair correlation comparison:")
print(f"  The Montgomery conjecture predicts: g(u) = 1 - (sin(πu)/(πu))²")
print(f"  This gives g(0)=0, g(1)=1, with specific decay shape.")
print()

# Fit exponential decay to ACF
lags_fit = np.arange(1, 50)
acf_vals = acf_normalized[1:50]
# log fit for exponential: log(acf) ~ -λ·k
valid = acf_vals > 0
if np.sum(valid) > 5:
    log_acf = np.log(acf_vals[valid])
    lag_valid = lags_fit[valid]
    sl, inter, rv, _, _ = linregress(lag_valid, log_acf)
    decay_rate = -sl
    correlation_length = 1.0 / decay_rate if decay_rate > 0 else float('inf')
    print(f"  Exponential decay rate: λ = {decay_rate:.6f}")
    print(f"  Correlation length: 1/λ = {correlation_length:.2f} prime steps")
    print(f"  R² of exponential fit: {rv**2:.4f}")
    results['acf_decay_rate'] = decay_rate
    results['correlation_length'] = correlation_length

# Power-law fit
valid2 = (acf_vals > 0) & (lags_fit > 0)
if np.sum(valid2) > 5:
    sl2, inter2, rv2, _, _ = linregress(np.log(lags_fit[valid2]), np.log(acf_vals[valid2]))
    print(f"  Power-law exponent: α = {sl2:.4f}, R² = {rv2**2:.4f}")
    results['acf_power_law'] = sl2

print()

# ═══════════════════════════════════════════════════════════════════════════════
# INVESTIGATION 3: Fourier Peaks at Zeta Zero Locations
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("INVESTIGATION 3: FOURIER PEAKS AT ZETA ZERO IMAGINARY PARTS")
print("=" * 72)

# The explicit formula for the prime counting function π(x) involves
# oscillations at frequencies related to log(p). If ΔW encodes zeta info,
# the Fourier transform of ΔW(p_n) against log(p_n) should show peaks at γ_k.

# Method: compute the "explicit formula" type transform
# F(t) = Σ_n ΔW(p_n) · p_n² · p_n^{it}
# which is essentially a Mellin-like transform.

# But simpler: use log(p) as the "time" coordinate, take FFT
log_primes = np.log(primes)

# Uniformly resample in log-space for FFT
n_resample = 8192
log_p_uniform = np.linspace(log_primes[0], log_primes[-1], n_resample)
# Interpolate scaled_dw onto uniform log-prime grid
dw_interp = np.interp(log_p_uniform, log_primes, scaled_dw)
dw_interp -= np.mean(dw_interp)

# Apply window
win = signal.windows.hann(n_resample)
dw_windowed = dw_interp * win

# FFT
FT = np.fft.rfft(dw_windowed)
power = np.abs(FT) ** 2

# Frequency axis: the "angular frequency" in units of 1/log(p)
delta_logp = log_p_uniform[1] - log_p_uniform[0]
freqs = np.fft.rfftfreq(n_resample, d=delta_logp)
# Convert to angular frequency (the γ values are in the convention Im(ρ)=γ)
omega = 2 * np.pi * freqs

print(f"  Frequency resolution: Δω = {omega[1] - omega[0]:.4f}")
print(f"  Max frequency: ω_max = {omega[-1]:.2f}")
print(f"  First 10 zeta zeros to check: γ₁={ZETA_ZEROS[0]:.2f} ... γ₁₀={ZETA_ZEROS[9]:.2f}")
print()

# Check each zeta zero: is there a peak nearby?
print(f"  {'Zero':>5s}  {'γ_k':>8s}  {'Nearest ω':>10s}  {'Power':>12s}  {'Local SNR':>10s}  {'Peak?':>6s}")
print(f"  {'-'*5}  {'-'*8}  {'-'*10}  {'-'*12}  {'-'*10}  {'-'*6}")

peak_snrs = []
for i, gamma in enumerate(ZETA_ZEROS[:15]):
    # Find nearest frequency bin
    idx = np.argmin(np.abs(omega - gamma))
    nearest_omega = omega[idx]

    # Local power: peak vs neighborhood
    half_win = 20
    lo = max(0, idx - half_win)
    hi = min(len(power), idx + half_win + 1)
    local_power = power[lo:hi]
    local_mean = np.mean(local_power)
    local_std = np.std(local_power)
    peak_power = power[idx]

    # Also check max in neighborhood (in case of slight offset)
    local_max_idx = lo + np.argmax(power[lo:hi])
    local_max_power = power[local_max_idx]
    local_max_omega = omega[local_max_idx]

    snr = (local_max_power - local_mean) / (local_std + 1e-30)
    is_peak = "YES" if snr > 2.0 else "no"
    peak_snrs.append(snr)

    print(f"  γ_{i+1:>2d}   {gamma:8.3f}  {local_max_omega:10.3f}  {local_max_power:12.4e}  {snr:10.2f}  {is_peak:>6s}")

results['mean_zeta_snr'] = np.mean(peak_snrs)
results['max_zeta_snr'] = np.max(peak_snrs)
results['peaks_above_2sigma'] = sum(1 for s in peak_snrs if s > 2.0)

print(f"\n  Mean SNR at zeta zeros: {results['mean_zeta_snr']:.2f}")
print(f"  Max  SNR at zeta zeros: {results['max_zeta_snr']:.2f}")
print(f"  Zeros with SNR > 2σ:   {results['peaks_above_2sigma']}/{len(peak_snrs)}")

# Null test: random frequencies
np.random.seed(42)
random_gammas = np.random.uniform(10, 110, 100)
random_snrs = []
for gamma in random_gammas:
    idx = np.argmin(np.abs(omega - gamma))
    lo = max(0, idx - half_win)
    hi = min(len(power), idx + half_win + 1)
    local_p = power[lo:hi]
    local_max = np.max(local_p)
    local_m = np.mean(local_p)
    local_s = np.std(local_p) + 1e-30
    random_snrs.append((local_max - local_m) / local_s)

print(f"\n  Null test (100 random frequencies):")
print(f"    Mean SNR: {np.mean(random_snrs):.2f}")
print(f"    Max  SNR: {np.max(random_snrs):.2f}")
print(f"    Fraction > 2σ: {sum(1 for s in random_snrs if s > 2.0)}/{len(random_snrs)}")

results['null_mean_snr'] = np.mean(random_snrs)
results['null_frac_2sigma'] = sum(1 for s in random_snrs if s > 2.0) / len(random_snrs)
print()

# ─── Alternative: Direct Dirichlet-type sum ─────────────────────────────────
print("  --- Direct sum test: F(t) = Σ ΔW(p_n)·p_n² · exp(i·t·log(p_n)) ---")
print()

t_values = np.linspace(0, 120, 12000)
direct_sum = np.zeros(len(t_values))

# Vectorized computation
log_p = np.log(primes)
weights = scaled_dw

for j, t in enumerate(t_values):
    direct_sum[j] = np.abs(np.sum(weights * np.exp(1j * t * log_p))) ** 2

# Normalize
direct_sum /= np.max(direct_sum)

# Check zeta zeros
print(f"  {'Zero':>5s}  {'γ_k':>8s}  {'|F(γ)|²':>10s}  {'Local max':>10s}  {'At ω':>8s}  {'SNR':>6s}")
print(f"  {'-'*5}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*8}  {'-'*6}")

dt = t_values[1] - t_values[0]
direct_peak_snrs = []
for i, gamma in enumerate(ZETA_ZEROS[:15]):
    idx = np.argmin(np.abs(t_values - gamma))
    val = direct_sum[idx]

    # Local neighborhood
    hw = int(2.0 / dt)
    lo = max(0, idx - hw)
    hi = min(len(direct_sum), idx + hw + 1)
    local = direct_sum[lo:hi]
    local_max_pos = lo + np.argmax(local)
    local_max_val = direct_sum[local_max_pos]
    local_max_t = t_values[local_max_pos]

    # SNR against broader background
    bg_hw = int(10.0 / dt)
    bg_lo = max(0, idx - bg_hw)
    bg_hi = min(len(direct_sum), idx + bg_hw + 1)
    bg = direct_sum[bg_lo:bg_hi]
    bg_mean = np.mean(bg)
    bg_std = np.std(bg) + 1e-30
    snr = (local_max_val - bg_mean) / bg_std

    direct_peak_snrs.append(snr)
    print(f"  γ_{i+1:>2d}   {gamma:8.3f}  {val:10.4f}    {local_max_val:10.4f}  {local_max_t:8.3f}  {snr:6.2f}")

results['direct_mean_snr'] = np.mean(direct_peak_snrs)
results['direct_peaks_above_2sigma'] = sum(1 for s in direct_peak_snrs if s > 2.0)

print(f"\n  Direct sum: mean SNR at zeros = {results['direct_mean_snr']:.2f}")
print(f"  Peaks above 2σ: {results['direct_peaks_above_2sigma']}/15")

# Random null for direct sum
null_direct_snrs = []
for gamma in random_gammas[:30]:
    idx = np.argmin(np.abs(t_values - gamma))
    hw = int(2.0 / dt)
    lo = max(0, idx - hw)
    hi = min(len(direct_sum), idx + hw + 1)
    local_max_val = np.max(direct_sum[lo:hi])
    bg_hw = int(10.0 / dt)
    bg_lo = max(0, idx - bg_hw)
    bg_hi = min(len(direct_sum), idx + bg_hw + 1)
    bg = direct_sum[bg_lo:bg_hi]
    bg_mean = np.mean(bg)
    bg_std = np.std(bg) + 1e-30
    null_direct_snrs.append((local_max_val - bg_mean) / bg_std)

print(f"  Null (30 random): mean SNR = {np.mean(null_direct_snrs):.2f}")
print()

# ═══════════════════════════════════════════════════════════════════════════════
# INVESTIGATION 4: Mertens Function Oscillations in ΔW
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("INVESTIGATION 4: MERTENS FUNCTION & ZETA-ZERO OSCILLATIONS IN ΔW")
print("=" * 72)

# The Mertens function has the explicit formula:
#   M(x) = Σ_ρ x^ρ / ρ  (summed over zeta zeros ρ = 1/2 + iγ)
# Each term oscillates as x^{1/2} · cos(γ·log(x)) / |ρ|
#
# If ΔW(p) encodes Mertens-like behavior, we should see similar oscillations.

# Method: extract the oscillatory part of M(p)/sqrt(p) and correlate with ΔW·p²

m_scaled = mertens / np.sqrt(primes)

# Detrend both signals
from numpy.polynomial import polynomial as P
# Remove slow trend from m_scaled
coeffs = P.polyfit(log_primes, m_scaled, deg=3)
m_trend = P.polyval(log_primes, coeffs)
m_osc = m_scaled - m_trend

# Same for scaled ΔW
coeffs_dw = P.polyfit(log_primes, scaled_dw, deg=3)
dw_trend = P.polyval(log_primes, coeffs_dw)
dw_osc = scaled_dw - dw_trend

# Cross-correlation
cross_corr = np.correlate(
    (m_osc - np.mean(m_osc)) / (np.std(m_osc) * len(m_osc)),
    (dw_osc - np.mean(dw_osc)) / np.std(dw_osc),
    mode='full'
)
center = len(m_osc) - 1
lag0_corr = cross_corr[center]

print(f"  Cross-correlation between M(p)/√p and ΔW·p² (detrended):")
print(f"    Lag 0: r = {lag0_corr:.6f}")
for lag in [1, 2, 3, 5, 10]:
    print(f"    Lag {lag:2d}: r = {cross_corr[center + lag]:.6f}")
print()

results['mertens_dw_corr'] = lag0_corr

# Spectral coherence between M/√p oscillations and ΔW·p² oscillations
f_coh, coherence = signal.coherence(m_osc, dw_osc, nperseg=min(1024, N // 4))
omega_coh = 2 * np.pi * f_coh / delta_logp  # rough conversion

print(f"  Spectral coherence between M/√p and ΔW·p² at zeta zeros:")
for i, gamma in enumerate(ZETA_ZEROS[:10]):
    idx = np.argmin(np.abs(omega_coh - gamma))
    hw = 3
    lo = max(0, idx - hw)
    hi = min(len(coherence), idx + hw + 1)
    max_coh = np.max(coherence[lo:hi])
    print(f"    γ_{i+1:>2d} = {gamma:8.3f}: max coherence = {max_coh:.4f}")

mean_coh_at_zeros = np.mean([
    np.max(coherence[max(0, np.argmin(np.abs(omega_coh - g)) - 3):
                      min(len(coherence), np.argmin(np.abs(omega_coh - g)) + 4)])
    for g in ZETA_ZEROS[:10]
])
mean_coh_overall = np.mean(coherence)
print(f"\n  Mean coherence at zeta zeros: {mean_coh_at_zeros:.4f}")
print(f"  Mean coherence overall:       {mean_coh_overall:.4f}")
print(f"  Ratio (enrichment):           {mean_coh_at_zeros / mean_coh_overall:.2f}x")
print()

results['coherence_at_zeros'] = mean_coh_at_zeros
results['coherence_overall'] = mean_coh_overall

# ─── Direct oscillation detection via least-squares fit ──────────────────────
print("  --- Fitting cos(γ·log(p)) oscillations to ΔW·p² ---")
print()

# For each zeta zero, fit: ΔW·p² ≈ A·cos(γ·log(p)) + B·sin(γ·log(p)) + C
# and compute the amplitude √(A²+B²) and significance

log_p = np.log(primes)
y = scaled_dw

print(f"  {'Zero':>5s}  {'γ_k':>8s}  {'Amplitude':>10s}  {'Phase':>8s}  {'t-stat':>8s}  {'Signif':>7s}")
print(f"  {'-'*5}  {'-'*8}  {'-'*10}  {'-'*8}  {'-'*8}  {'-'*7}")

amplitudes = []
for i, gamma in enumerate(ZETA_ZEROS[:15]):
    cos_g = np.cos(gamma * log_p)
    sin_g = np.sin(gamma * log_p)
    ones = np.ones(N)

    # Design matrix
    X = np.column_stack([cos_g, sin_g, ones, log_p])
    # Least squares
    beta, residuals, rank, sv = np.linalg.lstsq(X, y, rcond=None)

    A, B = beta[0], beta[1]
    amplitude = np.sqrt(A**2 + B**2)
    phase = np.arctan2(B, A)

    # t-statistic for the amplitude
    y_pred = X @ beta
    mse = np.mean((y - y_pred)**2)
    # Covariance of beta
    try:
        cov_beta = mse * np.linalg.inv(X.T @ X)
        se_A = np.sqrt(cov_beta[0, 0])
        se_B = np.sqrt(cov_beta[1, 1])
        # Approximate t-stat for amplitude (F-test would be better)
        t_stat = amplitude / np.sqrt(se_A**2 + se_B**2) * np.sqrt(2)
    except:
        t_stat = 0.0

    signif = "***" if t_stat > 3.0 else "**" if t_stat > 2.0 else "*" if t_stat > 1.5 else ""
    amplitudes.append((gamma, amplitude, t_stat))

    print(f"  γ_{i+1:>2d}   {gamma:8.3f}  {amplitude:10.6f}  {phase:8.3f}  {t_stat:8.2f}  {signif:>7s}")

results['mean_amplitude'] = np.mean([a[1] for a in amplitudes])
results['signif_zeros'] = sum(1 for a in amplitudes if a[2] > 2.0)

# Null: random frequencies
null_amplitudes = []
for gamma in np.random.uniform(10, 110, 50):
    cos_g = np.cos(gamma * log_p)
    sin_g = np.sin(gamma * log_p)
    X = np.column_stack([cos_g, sin_g, np.ones(N), log_p])
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    null_amplitudes.append(np.sqrt(beta[0]**2 + beta[1]**2))

print(f"\n  Mean amplitude at zeta zeros:  {results['mean_amplitude']:.6f}")
print(f"  Mean amplitude at random freq: {np.mean(null_amplitudes):.6f}")
print(f"  Ratio: {results['mean_amplitude'] / np.mean(null_amplitudes):.2f}x")
print(f"  Zeros with t > 2: {results['signif_zeros']}/15")

results['amplitude_ratio'] = results['mean_amplitude'] / np.mean(null_amplitudes)
print()

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("SUMMARY OF FINDINGS")
print("=" * 72)

print(f"""
1. SPECTRAL SLOPE:
   Measured: f^{{{results['spectral_slope']:.2f}}} ± {results['spectral_slope_std']:.2f}
   GUE prediction: f^{{-1}}
   Previous agent: f^{{-1.18}}
   Verdict: {"CONSISTENT with pink noise / GUE" if abs(results['spectral_slope'] + 1.0) < 0.3 else "DEVIATES from GUE"}

2. AUTOCORRELATION:
   Lag-1: {acf_normalized[1]:.4f} (agent reported 0.91)
   Decay: {"exponential" if results.get('acf_decay_rate', 0) > 0 else "power-law"} with characteristic length ~{results.get('correlation_length', 0):.1f} prime steps
   Power-law exponent: {results.get('acf_power_law', 0):.3f}

3. FOURIER PEAKS AT ZETA ZEROS:
   FFT method: {results['peaks_above_2sigma']}/15 zeros above 2σ (null: {results['null_frac_2sigma']*100:.0f}% of random)
   Direct sum: {results['direct_peaks_above_2sigma']}/15 zeros above 2σ
   Mean SNR at zeros: {results['mean_zeta_snr']:.2f} (FFT), {results['direct_mean_snr']:.2f} (direct)
   Mean SNR at random: {results['null_mean_snr']:.2f}

4. MERTENS-ΔW CONNECTION:
   Cross-correlation M/√p vs ΔW·p²: r = {results['mertens_dw_corr']:.4f}
   Coherence at zeros vs overall: {results['coherence_at_zeros']:.4f} vs {results['coherence_overall']:.4f} ({results['coherence_at_zeros']/results['coherence_overall']:.1f}x enrichment)
   Oscillation fit: {results['signif_zeros']}/15 zeros significant, amplitude {results['amplitude_ratio']:.2f}x above noise
""")

# Save results dict
import json
with open("pink_noise_results.json", "w") as f:
    json.dump({k: float(v) if isinstance(v, (np.floating, float)) else int(v)
               for k, v in results.items()}, f, indent=2)
print("Results saved to pink_noise_results.json")
