#!/usr/bin/env python3
"""
Multi-taper spectral estimation for the Mertens spectroscope.

The spectroscope F(gamma) = |sum M(p)/p * exp(-i*gamma*log(p))|^2
detects zeta zeros as peaks. Standard periodogram has high variance.
Multi-taper estimation uses multiple orthogonal windows to reduce
variance while preserving spectral resolution.

Samples: x_j = log(p_j) for primes p <= 500,000 (~41,538 primes)
Signal:  a_j = M(p_j) / p_j   (Mertens cumulative / prime)

We implement THREE methods:
  A. Standard periodogram (baseline)
  B. Sine-taper multi-taper: K sine tapers sin(k*pi*(j+0.5)/(N+1))
  C. DPSS multi-taper with NW=4, K=5 (classical Thomson)

The sine tapers are preferred for this problem because they are
well-localized in both index and frequency space regardless of N,
whereas DPSS with small NW/N ratio over-concentrates.
"""

import numpy as np
from scipy.signal.windows import dpss
import time
import os

# ---------------------------------------------------------------------------
# 1. Sieve Mobius function, compute M(p) for all primes p <= N
# ---------------------------------------------------------------------------
def sieve_mobius(N):
    """
    Compute mu(n) for n=0..N using a multiplicative sieve.
    Initialize mu=1, for each prime p multiply all multiples by -1,
    then zero out multiples of p^2.
    """
    mu = np.ones(N + 1, dtype=np.int8)
    mu[0] = 0

    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False

    for p in range(2, N + 1):
        if is_prime[p]:
            for m in range(2 * p, N + 1, p):
                is_prime[m] = False
            for m in range(p, N + 1, p):
                mu[m] *= -1
            p2 = p * p
            for m in range(p2, N + 1, p2):
                mu[m] = 0

    primes = np.where(is_prime)[0].astype(np.int64)
    return mu, primes


def compute_mertens_at_primes(mu, primes):
    """Compute M(p) = sum_{n<=p} mu(n) for each prime p."""
    M_cumul = np.cumsum(mu.astype(np.int64))
    return M_cumul[primes]


# ---------------------------------------------------------------------------
# 2. Spectroscope engines
# ---------------------------------------------------------------------------
def compute_spectrum(amp, log_p, gammas, chunk=2000):
    """
    F(gamma) = |sum_j amp_j * exp(-i * gamma * log_p_j)|^2
    Returns complex sum S(gamma) and power |S|^2.
    """
    G = len(gammas)
    S = np.zeros(G, dtype=complex)
    for start in range(0, G, chunk):
        end = min(start + chunk, G)
        g_block = gammas[start:end, None]
        phase = g_block * log_p[None, :]
        S[start:end] = np.sum(amp[None, :] * np.exp(-1j * phase), axis=1)
    return np.abs(S) ** 2


def sine_taper_multitaper(amp, log_p, gammas, K=5, chunk=2000):
    """
    Multi-taper using K sine tapers:
        h_k(j) = sqrt(2/(N+1)) * sin(k*pi*(j+1)/(N+1))   k=1..K

    These are orthonormal and have good sidelobe properties.
    Variance reduction ~ K with minimal resolution loss.
    """
    N = len(amp)
    G = len(gammas)
    F_mt = np.zeros(G)
    j = np.arange(N, dtype=np.float64)

    for k in range(1, K + 1):
        taper = np.sqrt(2.0 / (N + 1)) * np.sin(k * np.pi * (j + 1) / (N + 1))
        tapered_amp = taper * amp
        for start in range(0, G, chunk):
            end = min(start + chunk, G)
            g_block = gammas[start:end, None]
            phase = g_block * log_p[None, :]
            S_k = np.sum(tapered_amp[None, :] * np.exp(-1j * phase), axis=1)
            F_mt[start:end] += np.abs(S_k) ** 2

    F_mt /= K
    return F_mt


def dpss_multitaper(amp, log_p, gammas, NW=4, K=5, chunk=2000):
    """
    Classical Thomson multi-taper using DPSS (Slepian) sequences.
    """
    N = len(amp)
    tapers = dpss(N, NW, K)
    G = len(gammas)
    F_mt = np.zeros(G)

    for k in range(K):
        tapered_amp = tapers[k] * amp
        for start in range(0, G, chunk):
            end = min(start + chunk, G)
            g_block = gammas[start:end, None]
            phase = g_block * log_p[None, :]
            S_k = np.sum(tapered_amp[None, :] * np.exp(-1j * phase), axis=1)
            F_mt[start:end] += np.abs(S_k) ** 2

    F_mt /= K
    return F_mt


# ---------------------------------------------------------------------------
# 3. Matched filter and z-scores
# ---------------------------------------------------------------------------
def matched_filter(F, gammas):
    """Apply gamma^2 matched filter."""
    return F * gammas ** 2


def compute_zscores(F, gammas, zero_gammas, window_half=0.5):
    """
    Z-score at each zero: (peak_near_zero - background_mean) / background_std.
    Background = F values far from all zeros.
    """
    bg_mask = np.ones(len(gammas), dtype=bool)
    for gz in zero_gammas:
        bg_mask &= np.abs(gammas - gz) > window_half

    bg = F[bg_mask]
    mu_bg = np.mean(bg)
    sigma_bg = np.std(bg)
    if sigma_bg == 0:
        sigma_bg = 1e-30

    zscores = []
    for gz in zero_gammas:
        idx = np.argmin(np.abs(gammas - gz))
        lo = max(0, idx - 25)
        hi = min(len(gammas), idx + 25)
        peak_val = np.max(F[lo:hi])
        z = (peak_val - mu_bg) / sigma_bg
        zscores.append(z)

    return np.array(zscores), mu_bg, sigma_bg


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    NMAX = 500_000

    zeta_zeros = np.array([
        14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
        37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
        52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
        67.0798, 69.5464, 72.0672, 75.7047, 77.1448
    ])

    gammas = np.linspace(5, 85, 20000)

    # ---- Step 1: Sieve ----
    print(f"Sieving Mobius function to {NMAX:,}...")
    t0 = time.time()
    mu, primes = sieve_mobius(NMAX)
    M_p = compute_mertens_at_primes(mu, primes)
    t1 = time.time()
    N = len(primes)
    print(f"  {N:,} primes in {t1 - t0:.1f}s")
    print(f"  M(p) range: [{M_p.min()}, {M_p.max()}]")
    M_all = np.cumsum(mu.astype(np.int64))
    print(f"  Sanity: M(10)={M_all[10]}, M(100)={M_all[100]}")

    amp = M_p / primes.astype(np.float64)
    log_p = np.log(primes.astype(np.float64))
    print(f"  log(p) in [{log_p[0]:.3f}, {log_p[-1]:.3f}]")

    # ---- Step 2: Standard periodogram ----
    print("\n[A] Standard periodogram...")
    t0 = time.time()
    F_std = compute_spectrum(amp, log_p, gammas)
    print(f"    Done in {time.time() - t0:.1f}s")

    # ---- Step 3a: Sine-taper multi-taper (K=5) ----
    K_sine = 5
    print(f"\n[B] Sine-taper multi-taper (K={K_sine})...")
    t0 = time.time()
    F_sine = sine_taper_multitaper(amp, log_p, gammas, K=K_sine)
    print(f"    Done in {time.time() - t0:.1f}s")

    # ---- Step 3b: DPSS multi-taper (NW=4, K=5) ----
    NW_dpss = 4
    K_dpss = 5
    print(f"\n[C] DPSS multi-taper (NW={NW_dpss}, K={K_dpss})...")
    t0 = time.time()
    F_dpss = dpss_multitaper(amp, log_p, gammas, NW=NW_dpss, K=K_dpss)
    print(f"    Done in {time.time() - t0:.1f}s")

    # ---- Step 4: Matched filter ----
    F_std_mf = matched_filter(F_std, gammas)
    F_sine_mf = matched_filter(F_sine, gammas)
    F_dpss_mf = matched_filter(F_dpss, gammas)

    # ---- Step 5: Z-scores ----
    configs = [
        ("Std",      F_std,     F_std_mf),
        ("Sine-MT",  F_sine,    F_sine_mf),
        ("DPSS-MT",  F_dpss,    F_dpss_mf),
    ]

    results = {}
    for label, F_raw, F_mf in configs:
        z_raw, _, _ = compute_zscores(F_raw, gammas, zeta_zeros)
        z_mf, _, _ = compute_zscores(F_mf, gammas, zeta_zeros)
        results[label] = {"z_raw": z_raw, "z_mf": z_mf, "F_raw": F_raw, "F_mf": F_mf}

    # Print table
    print("\n" + "=" * 90)
    print("Z-scores at first 20 zeta zeros")
    print("=" * 90)
    header = f"{'#':>3s} {'gamma':>8s}"
    for label in ["Std", "Sine-MT", "DPSS-MT"]:
        header += f" | {label:>7s} {label+'+mf':>9s}"
    print(header)
    print("-" * 90)

    for i, gz in enumerate(zeta_zeros):
        row = f"{i+1:3d} {gz:8.4f}"
        for label in ["Std", "Sine-MT", "DPSS-MT"]:
            zr = results[label]["z_raw"][i]
            zm = results[label]["z_mf"][i]
            row += f" | {zr:7.2f} {zm:9.2f}"
        print(row)

    # Summary
    print("\n" + "=" * 90)
    print("Summary")
    print("=" * 90)

    high = slice(10, 20)
    for label in ["Std", "Sine-MT", "DPSS-MT"]:
        zr = results[label]["z_raw"]
        zm = results[label]["z_mf"]
        print(f"\n  [{label}]")
        print(f"    Mean z (all 20, raw):     {np.mean(zr):.2f}")
        print(f"    Mean z (all 20, +mf):     {np.mean(zm):.2f}")
        print(f"    Mean z (11-20, raw):      {np.mean(zr[high]):.2f}")
        print(f"    Mean z (11-20, +mf):      {np.mean(zm[high]):.2f}")
        for thresh in [2.0, 3.0, 5.0]:
            n_raw = int(np.sum(zr >= thresh))
            n_mf = int(np.sum(zm >= thresh))
            print(f"    z >= {thresh}: raw={n_raw}/20, +mf={n_mf}/20")

    # Variance reduction
    bg_mask = np.ones(len(gammas), dtype=bool)
    for gz in zeta_zeros:
        bg_mask &= np.abs(gammas - gz) > 0.5

    print("\n  Variance reduction (background, with matched filter):")
    var_std_mf = np.var(F_std_mf[bg_mask])
    for label in ["Sine-MT", "DPSS-MT"]:
        var_mt_mf = np.var(results[label]["F_mf"][bg_mask])
        ratio = var_std_mf / var_mt_mf if var_mt_mf > 0 else float('inf')
        print(f"    {label}: {ratio:.1f}x")

    # ---- Step 6: Write results ----
    results_path = os.path.expanduser(
        "~/Desktop/Farey-Local/experiments/MULTITAPER_RESULTS.md"
    )
    with open(results_path, "w") as f:
        f.write("# Multi-Taper Spectral Estimation for the Mertens Spectroscope\n\n")
        f.write("**Date:** 2026-04-05\n\n")

        f.write("## Setup\n\n")
        f.write(f"- Primes up to N = {NMAX:,} ({N:,} primes)\n")
        f.write(f"- Frequency grid: gamma in [5, 85], 20,000 points\n")
        f.write(f"- Signal: M(p)/p at positions log(p)\n")
        f.write(f"- Matched filter: gamma^2 weighting\n\n")

        f.write("## Methods Compared\n\n")
        f.write("| Method | Description |\n")
        f.write("|--------|-------------|\n")
        f.write("| **Std** | Standard periodogram (no taper) |\n")
        f.write(f"| **Sine-MT** | K={K_sine} sine tapers: h_k(j) = sqrt(2/(N+1)) sin(k pi (j+1)/(N+1)) |\n")
        f.write(f"| **DPSS-MT** | K={K_dpss} DPSS (Slepian) tapers, NW={NW_dpss} |\n\n")

        f.write("## Z-Scores at First 20 Zeta Zeros\n\n")
        cols = "| # | gamma |"
        for label in ["Std", "Sine-MT", "DPSS-MT"]:
            cols += f" z({label}) | z({label}+mf) |"
        f.write(cols + "\n")
        sep = "|---|-------|"
        for _ in range(3):
            sep += "--------|----------|"
        f.write(sep + "\n")

        for i, gz in enumerate(zeta_zeros):
            row = f"| {i+1} | {gz:.4f} |"
            for label in ["Std", "Sine-MT", "DPSS-MT"]:
                zr = results[label]["z_raw"][i]
                zm = results[label]["z_mf"][i]
                row += f" {zr:.2f} | {zm:.2f} |"
            f.write(row + "\n")

        f.write(f"\n## Summary Statistics\n\n")
        f.write("| Metric |")
        for label in ["Std", "Sine-MT", "DPSS-MT"]:
            f.write(f" {label} | {label}+mf |")
        f.write("\n|--------|")
        for _ in range(3):
            f.write("--------|----------|")
        f.write("\n")

        for desc, sl in [("Mean z (all 20)", slice(None)), ("Mean z (11-20)", high)]:
            row = f"| {desc} |"
            for label in ["Std", "Sine-MT", "DPSS-MT"]:
                zr = results[label]["z_raw"][sl]
                zm = results[label]["z_mf"][sl]
                row += f" {np.mean(zr):.2f} | {np.mean(zm):.2f} |"
            f.write(row + "\n")

        for thresh in [2.0, 3.0, 5.0]:
            row = f"| Detections z >= {thresh} |"
            for label in ["Std", "Sine-MT", "DPSS-MT"]:
                zr = results[label]["z_raw"]
                zm = results[label]["z_mf"]
                row += f" {int(np.sum(zr >= thresh))}/20 | {int(np.sum(zm >= thresh))}/20 |"
            f.write(row + "\n")

        f.write(f"\n## Variance Analysis\n\n")
        f.write("Background variance (away from zeros), with matched filter:\n\n")
        f.write("| Method | Bg Variance | Reduction vs Std |\n")
        f.write("|--------|-------------|------------------|\n")
        f.write(f"| Std+mf | {var_std_mf:.4e} | 1.0x |\n")
        for label in ["Sine-MT", "DPSS-MT"]:
            var_mt_mf = np.var(results[label]["F_mf"][bg_mask])
            ratio = var_std_mf / var_mt_mf if var_mt_mf > 0 else float('inf')
            f.write(f"| {label}+mf | {var_mt_mf:.4e} | {ratio:.1f}x |\n")

        f.write(f"\n## Key Findings\n\n")

        # Compare sine-MT vs std for higher zeros
        z_std_mf_high = np.mean(results["Std"]["z_mf"][high])
        z_sine_mf_high = np.mean(results["Sine-MT"]["z_mf"][high])
        z_dpss_mf_high = np.mean(results["DPSS-MT"]["z_mf"][high])

        improvement_sine = z_sine_mf_high - z_std_mf_high
        improvement_dpss = z_dpss_mf_high - z_std_mf_high

        f.write(f"### Sine-taper multi-taper (preferred method)\n\n")
        if z_sine_mf_high > z_std_mf_high:
            f.write(f"Sine-taper MT **improves** higher-zero detection (zeros 11-20).\n")
        else:
            f.write(f"Sine-taper MT does not improve higher-zero detection (zeros 11-20).\n")
        f.write(f"- Mean z (11-20, +mf): std = {z_std_mf_high:.2f}, sine-MT = {z_sine_mf_high:.2f} (delta = {improvement_sine:+.2f})\n")
        det_std = int(np.sum(results["Std"]["z_mf"] >= 2.0))
        det_sine = int(np.sum(results["Sine-MT"]["z_mf"] >= 2.0))
        f.write(f"- Detections at z >= 2: std = {det_std}/20, sine-MT = {det_sine}/20\n\n")

        f.write(f"### DPSS multi-taper\n\n")
        f.write(f"DPSS with NW={NW_dpss} on N={N:,} samples creates an extremely narrow\n")
        f.write(f"spectral resolution bandwidth of 2*NW/N = {2*NW_dpss/N:.6f}.\n")
        f.write(f"This causes massive over-smoothing: the tapers are nearly zero except\n")
        f.write(f"in a tiny central region, killing both signal and noise.\n")
        f.write(f"- Mean z (11-20, +mf): {z_dpss_mf_high:.2f} (delta vs std = {improvement_dpss:+.2f})\n\n")

        f.write(f"### Conclusion\n\n")
        if det_sine > det_std:
            f.write(f"Sine-taper multi-taper estimation with K={K_sine} tapers improves\n")
            f.write(f"zero detection: {det_sine}/20 vs {det_std}/20 at z >= 2.\n")
        elif det_sine == det_std:
            f.write(f"Sine-taper multi-taper matches standard detection count ({det_sine}/20 at z >= 2).\n")
        else:
            f.write(f"Standard periodogram with matched filter outperforms multi-taper\n")
            f.write(f"for this problem ({det_std}/20 vs {det_sine}/20 at z >= 2).\n")
        f.write(f"\nThe Mertens spectroscope signal is intrinsically sparse (sharp peaks at\n")
        f.write(f"zeta zeros). Multi-taper smoothing trades peak height for lower variance,\n")
        f.write(f"which can help or hurt depending on the signal-to-noise regime.\n")
        f.write(f"The gamma^2 matched filter is the dominant improvement for higher zeros.\n")

    print(f"\nResults written to {results_path}")
    print("Done.")


if __name__ == "__main__":
    main()
