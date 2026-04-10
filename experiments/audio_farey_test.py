#!/usr/bin/env python3
"""
Quick validation: Farey quantization vs. uniform/mu-law for audio signals.

Test: quantize a 1D audio-like signal to N levels using different schemes.
Compare SNR.
"""

import numpy as np
import time

np.random.seed(42)

# === Generate test signal ===
# Sum of sinusoids at different frequencies and amplitudes (music-like)
fs = 8000  # 8kHz sample rate (telephony)
duration = 1.0  # 1 second
t = np.arange(0, duration, 1.0 / fs)

# Signal: mix of frequencies with varying amplitudes
signal = (
    0.5 * np.sin(2 * np.pi * 440 * t) +      # A4 note
    0.3 * np.sin(2 * np.pi * 880 * t) +       # A5
    0.1 * np.sin(2 * np.pi * 1320 * t) +      # harmonic
    0.05 * np.sin(2 * np.pi * 220 * t) +      # sub-harmonic
    0.02 * np.random.randn(len(t))              # noise floor
)

# Normalize to [-1, 1]
signal = signal / np.max(np.abs(signal))


# === Quantization methods ===

def quantize_uniform(sig, n_levels):
    """Uniform quantization to n_levels."""
    # Map [-1,1] to [0, n_levels-1]
    quantized_idx = np.round((sig + 1) / 2 * (n_levels - 1)).astype(int)
    quantized_idx = np.clip(quantized_idx, 0, n_levels - 1)
    reconstructed = quantized_idx / (n_levels - 1) * 2 - 1
    return reconstructed


def quantize_mu_law(sig, n_levels, mu=255):
    """Mu-law companding + uniform quantization."""
    # Compress
    compressed = np.sign(sig) * np.log1p(mu * np.abs(sig)) / np.log1p(mu)
    # Uniform quantize the compressed signal
    quantized_idx = np.round((compressed + 1) / 2 * (n_levels - 1)).astype(int)
    quantized_idx = np.clip(quantized_idx, 0, n_levels - 1)
    # Reconstruct compressed domain
    recon_compressed = quantized_idx / (n_levels - 1) * 2 - 1
    # Expand
    reconstructed = np.sign(recon_compressed) * (1.0 / mu) * ((1 + mu) ** np.abs(recon_compressed) - 1)
    return reconstructed


def farey_levels(n):
    """Generate Farey sequence F_n scaled to [-1, 1]."""
    fractions = set()
    for q in range(1, n + 1):
        for p in range(0, q + 1):
            fractions.add(p / q)
    levels = sorted(fractions)
    # Scale from [0,1] to [-1,1]
    levels = [2 * x - 1 for x in levels]
    return np.array(levels)


def quantize_farey(sig, order):
    """Quantize to nearest Farey fraction of given order."""
    levels = farey_levels(order)
    # For each sample, find nearest level
    # Vectorized: use searchsorted
    idx = np.searchsorted(levels, sig)
    idx = np.clip(idx, 1, len(levels) - 1)
    # Choose between idx-1 and idx
    d_left = np.abs(sig - levels[idx - 1])
    d_right = np.abs(sig - levels[idx])
    best_idx = np.where(d_left <= d_right, idx - 1, idx)
    return levels[best_idx]


# === Run comparison ===
print("=" * 70)
print("Audio Quantization: Uniform vs. Mu-Law vs. Farey")
print("=" * 70)
print(f"Signal: sum of sinusoids, {len(signal)} samples at {fs} Hz")
print()

def compute_snr(original, reconstructed):
    noise = original - reconstructed
    signal_power = np.mean(original ** 2)
    noise_power = np.mean(noise ** 2)
    if noise_power == 0:
        return float('inf')
    return 10 * np.log10(signal_power / noise_power)


# Test at various bit depths
for n_bits in [4, 6, 8]:
    n_uniform = 2 ** n_bits

    print(f"\n--- {n_bits}-bit quantization ({n_uniform} uniform levels) ---")

    # Uniform
    t0 = time.time()
    recon_uni = quantize_uniform(signal, n_uniform)
    t_uni = time.time() - t0
    snr_uni = compute_snr(signal, recon_uni)

    # Mu-law
    t0 = time.time()
    recon_mu = quantize_mu_law(signal, n_uniform)
    t_mu = time.time() - t0
    snr_mu = compute_snr(signal, recon_mu)

    # Farey: pick order so |F_n| ~ n_uniform
    # |F_n| ~ 3n^2/pi^2, so n ~ sqrt(pi^2 * N / 3)
    farey_order = int(np.sqrt(np.pi ** 2 * n_uniform / 3))
    farey_lvls = farey_levels(farey_order)
    n_farey = len(farey_lvls)

    t0 = time.time()
    recon_far = quantize_farey(signal, farey_order)
    t_far = time.time() - t0
    snr_far = compute_snr(signal, recon_far)

    print(f"{'Method':<20} {'Levels':<10} {'SNR (dB)':<12} {'Time (ms)':<12}")
    print("-" * 55)
    print(f"{'Uniform':<20} {n_uniform:<10} {snr_uni:<12.2f} {t_uni*1000:<12.2f}")
    print(f"{'Mu-law (mu=255)':<20} {n_uniform:<10} {snr_mu:<12.2f} {t_mu*1000:<12.2f}")
    print(f"{'Farey F_{farey_order}':<20} {n_farey:<10} {snr_far:<12.2f} {t_far*1000:<12.2f}")

# === Diagnostic: Farey level distribution ===
print("\n" + "=" * 70)
print("Farey Level Distribution Analysis")
print("=" * 70)
for order in [4, 6, 8]:
    lvls = farey_levels(order)
    gaps = np.diff(lvls)
    print(f"\nF_{order}: {len(lvls)} levels, gap range [{gaps.min():.4f}, {gaps.max():.4f}], "
          f"mean gap {gaps.mean():.4f}, std {gaps.std():.4f}")

print("\nMu-law effective level distribution (mu=255, 16 levels):")
uniform_levels = np.linspace(-1, 1, 16)
# Expand to see where mu-law places its effective levels
mu = 255
compressed_levels = uniform_levels
expanded = np.sign(compressed_levels) * (1.0 / mu) * ((1 + mu) ** np.abs(compressed_levels) - 1)
gaps = np.diff(sorted(expanded))
print(f"  16 levels, gap range [{gaps.min():.4f}, {gaps.max():.4f}], "
      f"mean gap {gaps.mean():.4f}, std {gaps.std():.4f}")

print("\n" + "=" * 70)
print("ANALYSIS")
print("=" * 70)
print("""
Farey fractions F_n give the "most spread out" rationals with denominator <= n.
They are UNIFORMLY distributed in the limit (equidistribution theorem).

This means Farey quantization levels are approximately uniformly spaced,
just like uniform quantization -- but with slightly irregular gaps.

Mu-law wins because it concentrates levels near zero where speech energy
is concentrated (small amplitudes are more common and perceptually important).

Farey levels have NO such concentration. They are quasi-uniform.
They do NOT adapt to signal statistics at all.

The theoretical "best rational approximation" property of Farey sequences
is irrelevant here because:
1. Audio samples are not rational numbers that need approximation
2. The quality metric is SNR, not "closeness of rational approximation"
3. The denominator structure carries no meaning for audio amplitude values

CONCLUSION: Farey quantization offers no advantage over uniform quantization
for audio. Mu-law (and modern learned quantizers like RVQ in EnCodec/SoundStream)
are superior because they adapt to signal statistics. Farey fractions are
quasi-uniform and signal-agnostic.
""")
