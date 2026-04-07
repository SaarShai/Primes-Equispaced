#!/usr/bin/env python3
"""
Matched-filter comparison: gamma^2 periodogram vs Lomb-Scargle
across three domains (finance, seismic, medical).

gamma^2 power: P(f) = (2*pi*f)^2 * |sum_j x_j * exp(-2*pi*i*f*t_j)|^2
LS power:      scipy.signal.lombscargle
"""

import numpy as np
from scipy.signal import lombscargle
import time

np.random.seed(42)

def gamma2_periodogram(t, x, freqs):
    """Compute gamma^2 weighted periodogram."""
    power = np.zeros(len(freqs))
    for i, f in enumerate(freqs):
        phase = 2 * np.pi * f * t
        S = np.sum(x * np.exp(-2j * np.pi * f * t))
        power[i] = (2 * np.pi * f) ** 2 * np.abs(S) ** 2
    return power

def snr_at_freq(freqs, power, target_freq, bandwidth=0.005):
    """SNR = peak power near target / median power away from target."""
    near = np.abs(freqs - target_freq) < bandwidth
    far = np.abs(freqs - target_freq) > 3 * bandwidth
    if not np.any(near) or not np.any(far):
        return 0.0
    peak = np.max(power[near])
    noise_median = np.median(power[far])
    if noise_median == 0:
        return float('inf')
    return peak / noise_median

def run_test(name, t, x, target_freq, freq_range, desc):
    """Run both methods and report SNR."""
    freqs = np.linspace(freq_range[0], freq_range[1], 5000)
    angular_freqs = 2 * np.pi * freqs

    # Lomb-Scargle (expects angular frequencies)
    x_centered = x - np.mean(x)
    ls_power = lombscargle(t, x_centered, angular_freqs, normalize=False)

    # gamma^2 periodogram
    g2_power = gamma2_periodogram(t, x_centered, freqs)

    # SNR
    snr_ls = snr_at_freq(freqs, ls_power, target_freq)
    snr_g2 = snr_at_freq(freqs, g2_power, target_freq)

    winner = "gamma^2" if snr_g2 > snr_ls else "Lomb-Scargle"
    ratio = max(snr_g2, snr_ls) / max(min(snr_g2, snr_ls), 1e-10)

    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"  {desc}")
    print(f"  N = {len(t)}, target freq = {target_freq} Hz")
    print(f"  Lomb-Scargle SNR:  {snr_ls:.2f}")
    print(f"  gamma^2 SNR:       {snr_g2:.2f}")
    print(f"  VERDICT: {winner} wins (ratio {ratio:.1f}x)")
    print(f"{'='*60}")

    return {
        'name': name, 'desc': desc, 'N': len(t),
        'target_freq': target_freq,
        'snr_ls': snr_ls, 'snr_g2': snr_g2,
        'winner': winner, 'ratio': ratio
    }


# ============================================================
# TEST 1: FINANCIAL
# ============================================================
print("Running TEST 1: FINANCIAL ...")
N_fin = 10000
gaps = np.random.exponential(0.5, N_fin)
t_fin = np.cumsum(gaps)

f_signal = 0.1  # Hz
amplitude = 0.0001  # 0.01% of price
noise_std = amplitude * 10

# Random walk + weak periodic signal + noise
price_walk = np.cumsum(np.random.randn(N_fin) * 0.001)
signal_fin = amplitude * np.sin(2 * np.pi * f_signal * t_fin)
noise_fin = noise_std * np.random.randn(N_fin)
x_fin = price_walk + signal_fin + noise_fin

r1 = run_test("FINANCIAL", t_fin, x_fin, 0.1, (0.01, 0.5),
              "10K trades, Poisson gaps (0.5s), 0.01% signal @ 0.1Hz, noise 10x signal")


# ============================================================
# TEST 2: SEISMIC (Omori law aftershocks)
# ============================================================
print("\nRunning TEST 2: SEISMIC ...")
N_seis = 500
c = 0.1  # Omori constant
# Generate Omori-law times via inverse CDF: t = c*(exp(u/K) - 1)
# Rate: r(t) = K/(t+c), cumulative N(t) = K*ln((t+c)/c)
# Use thinning: generate more, then subsample
K = 50
t_max_seis = 200.0
# Generate via inverse transform
u = np.sort(np.random.uniform(0, 1, N_seis))
# N(t)/N(T) = ln((t+c)/c) / ln((T+c)/c)
# t = c * exp(u * ln((T+c)/c)) - c
t_seis = c * np.exp(u * np.log((t_max_seis + c) / c)) - c

f_seis = 0.05  # Hz
# Inject weak periodic modulation on magnitudes
mag_base = 2.0 + np.random.exponential(0.5, N_seis)
mag_mod = 0.1 * np.sin(2 * np.pi * f_seis * t_seis)
x_seis = mag_base + mag_mod

r2 = run_test("SEISMIC", t_seis, x_seis, 0.05, (0.01, 0.2),
              "500 aftershocks (Omori law), 0.05Hz modulation on magnitude")


# ============================================================
# TEST 3: MEDICAL (HRV / respiratory sinus arrhythmia)
# ============================================================
print("\nRunning TEST 3: MEDICAL ...")
N_med = 1000
mean_rr = 0.8  # seconds
std_rr = 0.05

# RR intervals with respiratory modulation
rr_base = mean_rr + std_rr * np.random.randn(N_med)
# Beat times
t_med = np.cumsum(rr_base)

# Respiratory sinus arrhythmia: modulate RR intervals
f_resp = 0.25  # Hz (15 breaths/min)
rsa_amplitude = 0.01  # seconds
rr_modulated = rr_base + rsa_amplitude * np.sin(2 * np.pi * f_resp * t_med)
t_med = np.cumsum(rr_modulated)

# The signal to analyze: RR intervals themselves
x_med = rr_modulated

r3 = run_test("MEDICAL", t_med, x_med, 0.25, (0.05, 0.5),
              "1000 heartbeats (RR=0.8s +/- 0.05s), RSA at 0.25Hz (amp=0.01s)")


# ============================================================
# SUMMARY
# ============================================================
results = [r1, r2, r3]
print("\n\n" + "="*70)
print("SUMMARY TABLE")
print("="*70)
print(f"{'Domain':<15} {'LS SNR':>10} {'gamma^2 SNR':>12} {'Winner':>15} {'Ratio':>8}")
print("-"*70)
for r in results:
    print(f"{r['name']:<15} {r['snr_ls']:>10.2f} {r['snr_g2']:>12.2f} {r['winner']:>15} {r['ratio']:>7.1f}x")
print("="*70)

# ============================================================
# Write markdown report
# ============================================================
report_path = "/Users/saar/Desktop/Farey-Local/experiments/MATCHED_FILTER_FINANCE_SEISMIC.md"
with open(report_path, 'w') as f:
    f.write("# Matched-Filter Comparison: gamma^2 vs Lomb-Scargle\n\n")
    f.write("Three-domain benchmark testing the gamma^2 periodogram against\n")
    f.write("standard Lomb-Scargle for weak signal detection in irregularly sampled data.\n\n")

    f.write("## Method\n\n")
    f.write("- **gamma^2 periodogram**: P(f) = (2*pi*f)^2 * |sum_j x_j * exp(-2*pi*i*f*t_j)|^2\n")
    f.write("- **Lomb-Scargle**: scipy.signal.lombscargle (standard)\n")
    f.write("- **SNR**: peak power at target freq / median power away from target\n\n")

    f.write("## Results\n\n")
    f.write("| Domain | N | Target (Hz) | LS SNR | gamma^2 SNR | Winner | Ratio |\n")
    f.write("|--------|---|-------------|--------|-------------|--------|-------|\n")
    for r in results:
        f.write(f"| {r['name']} | {r['N']} | {r['target_freq']} | "
                f"{r['snr_ls']:.2f} | {r['snr_g2']:.2f} | "
                f"{r['winner']} | {r['ratio']:.1f}x |\n")
    f.write("\n")

    f.write("## Test Details\n\n")
    for r in results:
        f.write(f"### {r['name']}\n")
        f.write(f"- {r['desc']}\n")
        f.write(f"- LS SNR = {r['snr_ls']:.2f}, gamma^2 SNR = {r['snr_g2']:.2f}\n")
        f.write(f"- **VERDICT**: {r['winner']} wins by {r['ratio']:.1f}x\n\n")

    f.write("## Interpretation\n\n")

    # Dynamic interpretation
    g2_wins = sum(1 for r in results if r['winner'] == 'gamma^2')
    if g2_wins >= 2:
        f.write("The gamma^2 filter shows advantage in the majority of tested domains.\n")
        f.write("The (2*pi*f)^2 weighting amplifies higher-frequency signals relative to\n")
        f.write("low-frequency drift/noise, acting as a matched filter for oscillatory\n")
        f.write("components embedded in non-stationary, irregularly-sampled data.\n\n")
    elif g2_wins == 1:
        f.write("Mixed results: gamma^2 and Lomb-Scargle each have domain-specific strengths.\n")
        f.write("The f^2 weighting helps when the target frequency is well above the\n")
        f.write("dominant noise frequencies, but can amplify high-frequency noise otherwise.\n\n")
    else:
        f.write("Lomb-Scargle dominates across domains in this configuration.\n")
        f.write("The gamma^2 weighting may require tuning or different signal conditions.\n\n")

    f.write("### Domain-specific verdicts\n\n")
    for r in results:
        f.write(f"- **{r['name']}**: {r['winner']} ({r['ratio']:.1f}x). ")
        if r['name'] == 'FINANCIAL':
            if r['winner'] == 'gamma^2':
                f.write("The f^2 weight suppresses random-walk drift, boosting periodic detection.\n")
            else:
                f.write("Random-walk dominance at low freq makes LS competitive here.\n")
        elif r['name'] == 'SEISMIC':
            if r['winner'] == 'gamma^2':
                f.write("Omori-law clustering creates strong low-freq power; f^2 cuts through it.\n")
            else:
                f.write("The sparse, clustered sampling may limit gamma^2 advantage.\n")
        elif r['name'] == 'MEDICAL':
            if r['winner'] == 'gamma^2':
                f.write("HRV's 1/f noise profile makes the f^2 boost highly effective at respiratory band.\n")
            else:
                f.write("Near-regular sampling reduces the advantage of irregular-sampling methods.\n")

    f.write(f"\n**Overall**: gamma^2 wins {g2_wins}/3 domains.\n")

print(f"\nReport written to: {report_path}")
