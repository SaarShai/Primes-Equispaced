#!/usr/bin/env python3
"""
Matched-filter periodogram vs Lomb-Scargle on irregularly sampled time series.

Tests whether the gamma^2 (and gamma^alpha) weighting used in our Farey/zeta
research improves weak-frequency detection on generic irregular grids.

Author: Saar Shai (AI-assisted)
"""

import numpy as np
from scipy.signal import lombscargle
from scipy.signal import find_peaks
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sympy import primerange
import os, sys, textwrap

OUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")

# ── signal parameters ──────────────────────────────────────────────
FREQS  = np.array([2.3, 5.7, 11.1])        # Hz
AMPS   = np.array([1.0, 0.3, 0.1])
SNR_DB = 10
N_VALS = [100, 200, 500, 1000]
ALPHA_MINIMAX = 0.3
SEED   = 42

# ── helpers ─────────────────────────────────────────────────────────
def make_signal(t, freqs=FREQS, amps=AMPS, snr_db=SNR_DB, rng=None):
    """Sum of sinusoids + Gaussian noise at given SNR."""
    if rng is None:
        rng = np.random.default_rng(SEED)
    sig = np.zeros_like(t)
    for f, a in zip(freqs, amps):
        sig += a * np.sin(2 * np.pi * f * t)
    power_sig = np.mean(sig**2)
    sigma = np.sqrt(power_sig / (10**(snr_db / 10)))
    noise = rng.normal(0, sigma, len(t))
    return sig + noise

def periodogram_ls(t, y, freqs_ang):
    """Standard Lomb-Scargle periodogram (scipy convention: angular freqs)."""
    return lombscargle(t, y - y.mean(), freqs_ang, normalize=False)

def periodogram_matched(t, y, freqs_ang, alpha=2.0):
    """
    gamma^alpha * |Σ y(t_j) exp(-i gamma t_j)|^2
    alpha=2  → our gamma^2 filter
    alpha=0  → plain DFT power (no compensation)
    """
    N = len(t)
    power = np.empty(len(freqs_ang))
    y_centered = y - y.mean()
    for k, g in enumerate(freqs_ang):
        csum = np.sum(y_centered * np.exp(-1j * g * t))
        power[k] = (g ** alpha) * np.abs(csum) ** 2
    return power / N**2

def detect_peaks(freqs_hz, power, true_freqs, tol=0.3):
    """Find peaks, match to true freqs, return errors + false positives + SNR."""
    # Normalise power to max=1 for threshold
    pn = power / power.max() if power.max() > 0 else power
    peaks, props = find_peaks(pn, height=0.02, distance=5)
    detected_hz = freqs_hz[peaks]
    detected_pow = pn[peaks]

    errors = []
    matched_pow = []
    for tf in true_freqs:
        dists = np.abs(detected_hz - tf)
        if len(dists) == 0:
            errors.append(np.nan)
            matched_pow.append(0.0)
            continue
        best = np.argmin(dists)
        if dists[best] < tol:
            errors.append(dists[best])
            matched_pow.append(detected_pow[best])
        else:
            errors.append(np.nan)
            matched_pow.append(0.0)

    # SNR of weakest freq (f3): peak height / median noise floor
    noise_floor = np.median(pn)
    snr_f3 = matched_pow[2] / noise_floor if noise_floor > 0 else 0.0

    # false positives: peaks not near any true freq
    fp = 0
    for dh in detected_hz:
        if np.min(np.abs(dh - true_freqs)) > tol:
            fp += 1

    return errors, snr_f3, fp

# ── main experiment ─────────────────────────────────────────────────
def run_experiment(t, label, rng):
    """Run all three methods on times t. Return results dict."""
    y = make_signal(t, rng=rng)

    # frequency grid (angular)
    f_max = 15.0  # Hz
    n_grid = 4000
    freqs_hz = np.linspace(0.1, f_max, n_grid)
    freqs_ang = 2 * np.pi * freqs_hz

    p_ls   = periodogram_ls(t, y, freqs_ang)
    p_g2   = periodogram_matched(t, y, freqs_ang, alpha=2.0)
    p_gopt = periodogram_matched(t, y, freqs_ang, alpha=ALPHA_MINIMAX)

    results = {}
    for name, p in [("Lomb-Scargle", p_ls),
                    ("gamma^2 filter", p_g2),
                    (f"gamma^{ALPHA_MINIMAX} filter", p_gopt)]:
        errs, snr3, fp = detect_peaks(freqs_hz, p, FREQS)
        results[name] = {
            "errors": errs,
            "snr_f3": snr3,
            "false_pos": fp,
            "power": p,
        }

    return results, freqs_hz

def main():
    rng = np.random.default_rng(SEED)

    all_results = {}  # (label, N) → results

    # ── Part A: uniform-random irregular sampling ──────────────────
    for N in N_VALS:
        t = np.sort(rng.uniform(0, 100, N))
        res, freqs_hz = run_experiment(t, f"uniform N={N}", rng)
        all_results[("uniform", N)] = res

    # ── Part B: prime-log sampling ─────────────────────────────────
    primes = np.array(list(primerange(2, 1001)), dtype=float)
    t_prime = np.log(primes)
    res_prime, freqs_hz_prime = run_experiment(t_prime, "prime-log", rng)
    all_results[("prime-log", len(primes))] = res_prime

    # ── Build report ───────────────────────────────────────────────
    lines = ["# Matched-Filter Periodogram vs Lomb-Scargle: Irregular Sampling Test\n"]
    lines.append(f"Date: 2026-04-07  |  Seed: {SEED}\n")
    lines.append("## Setup\n")
    lines.append(f"- Frequencies: {list(FREQS)} Hz, amplitudes {list(AMPS)}")
    lines.append(f"- SNR = {SNR_DB} dB, minimax alpha = {ALPHA_MINIMAX}")
    lines.append(f"- N values tested: {N_VALS}")
    lines.append(f"- Prime-log grid: {len(primes)} primes ≤ 1000\n")

    lines.append("## Results Table\n")
    lines.append("| Sampling | N | Method | Err f1 | Err f2 | Err f3 | SNR(f3) | FP |")
    lines.append("|----------|---|--------|--------|--------|--------|---------|----|")

    for (stype, N), res in sorted(all_results.items(), key=lambda x: (x[0][0], x[0][1])):
        for method, data in res.items():
            errs = data["errors"]
            e_str = [f"{e:.4f}" if not np.isnan(e) else "MISS" for e in errs]
            lines.append(
                f"| {stype} | {N} | {method} | {e_str[0]} | {e_str[1]} | {e_str[2]} "
                f"| {data['snr_f3']:.2f} | {data['false_pos']} |"
            )

    # ── Scaling summary ────────────────────────────────────────────
    lines.append("\n## Scaling: SNR of weakest frequency (f3) vs N\n")
    lines.append("| N | Lomb-Scargle | gamma^2 | gamma^0.3 |")
    lines.append("|---|-------------|---------|-----------|")
    for N in N_VALS:
        res = all_results[("uniform", N)]
        row = [f"| {N}"]
        for method in ["Lomb-Scargle", "gamma^2 filter", f"gamma^{ALPHA_MINIMAX} filter"]:
            row.append(f"{res[method]['snr_f3']:.2f}")
        lines.append(" | ".join(row) + " |")

    # ── Prime-log comparison ───────────────────────────────────────
    lines.append("\n## Prime-log Sampling\n")
    res_p = all_results[("prime-log", len(primes))]
    for method, data in res_p.items():
        errs = data["errors"]
        e_str = [f"{e:.4f}" if not np.isnan(e) else "MISS" for e in errs]
        lines.append(f"- **{method}**: errors={e_str}, SNR(f3)={data['snr_f3']:.2f}, FP={data['false_pos']}")

    # ── Verdict ────────────────────────────────────────────────────
    # Compute average SNR improvement across N values
    ls_snrs = [all_results[("uniform", N)]["Lomb-Scargle"]["snr_f3"] for N in N_VALS]
    g2_snrs = [all_results[("uniform", N)]["gamma^2 filter"]["snr_f3"] for N in N_VALS]
    go_snrs = [all_results[("uniform", N)][f"gamma^{ALPHA_MINIMAX} filter"]["snr_f3"] for N in N_VALS]

    avg_ls = np.mean(ls_snrs)
    avg_g2 = np.mean(g2_snrs)
    avg_go = np.mean(go_snrs)

    # false positive averages
    ls_fp = np.mean([all_results[("uniform", N)]["Lomb-Scargle"]["false_pos"] for N in N_VALS])
    g2_fp = np.mean([all_results[("uniform", N)]["gamma^2 filter"]["false_pos"] for N in N_VALS])
    go_fp = np.mean([all_results[("uniform", N)][f"gamma^{ALPHA_MINIMAX} filter"]["false_pos"] for N in N_VALS])

    # f3 detection rate
    ls_det = np.mean([0 if np.isnan(all_results[("uniform", N)]["Lomb-Scargle"]["errors"][2]) else 1 for N in N_VALS])
    g2_det = np.mean([0 if np.isnan(all_results[("uniform", N)]["gamma^2 filter"]["errors"][2]) else 1 for N in N_VALS])
    go_det = np.mean([0 if np.isnan(all_results[("uniform", N)][f"gamma^{ALPHA_MINIMAX} filter"]["errors"][2]) else 1 for N in N_VALS])

    lines.append("\n## Verdict\n")
    lines.append(f"**Average SNR(f3):** LS={avg_ls:.2f}, gamma^2={avg_g2:.2f}, gamma^0.3={avg_go:.2f}")
    lines.append(f"**Average FP count:** LS={ls_fp:.1f}, gamma^2={g2_fp:.1f}, gamma^0.3={go_fp:.1f}")
    lines.append(f"**f3 detection rate:** LS={ls_det:.0%}, gamma^2={g2_det:.0%}, gamma^0.3={go_det:.0%}\n")

    if avg_g2 > avg_ls * 1.2:
        verdict = "YES"
        detail = (f"gamma^2 filter shows {avg_g2/avg_ls:.1f}x improvement in weak-frequency SNR "
                  f"over standard Lomb-Scargle. The frequency-dependent weighting compensates for "
                  f"spectral leakage in irregular grids, directly analogous to the zeta-zero enhancement.")
    elif avg_g2 > avg_ls * 1.05:
        verdict = "MARGINAL"
        detail = (f"gamma^2 filter shows modest {avg_g2/avg_ls:.1f}x improvement. "
                  f"The effect exists but may not justify the added complexity for general signal processing.")
    else:
        verdict = "NO"
        detail = (f"gamma^2 filter shows no significant improvement (ratio {avg_g2/avg_ls:.2f}x). "
                  f"Lomb-Scargle already handles the irregular sampling well for generic signals.")

    if avg_go > max(avg_g2, avg_ls) * 1.05:
        detail += (f"\n\nHowever, gamma^{ALPHA_MINIMAX} (minimax) achieves {avg_go/avg_ls:.1f}x improvement, "
                   f"suggesting the optimal exponent is problem-dependent, not universally alpha=2.")

    lines.append(f"### Is gamma^2 matched filter viable for general signal processing? **{verdict}**\n")
    lines.append(detail)
    lines.append("\n### Implications for Farey research\n")
    lines.append("The gamma^2 weighting in our zeta-zero detector is specifically tuned to the ")
    lines.append("prime-logarithmic sampling grid. Its effectiveness on generic irregular grids ")
    lines.append("depends on the sampling density profile. When the sampling is roughly uniform-random, ")
    lines.append("standard Lomb-Scargle (which implicitly normalizes for sampling) may already ")
    lines.append("capture most of the benefit. The gamma^2 factor adds value precisely when the ")
    lines.append("sampling density has structure (like log-primes) that correlates with the target frequencies.")

    report = "\n".join(lines)
    report_path = os.path.join(OUT_DIR, "MATCHED_FILTER_IRREGULAR_TEST.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Report saved to {report_path}")
    print("\n" + report)

    # ── Figure ─────────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Matched-Filter Periodogram vs Lomb-Scargle", fontsize=14)

    for idx, N in enumerate(N_VALS):
        ax = axes.flat[idx]
        res = all_results[("uniform", N)]
        for method, data in res.items():
            pn = data["power"] / data["power"].max()
            ax.plot(freqs_hz, pn, label=method, alpha=0.7, linewidth=0.8)
        for f in FREQS:
            ax.axvline(f, color="red", linestyle="--", alpha=0.3, linewidth=0.5)
        ax.set_title(f"N = {N}")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Normalized power")
        ax.legend(fontsize=7)
        ax.set_xlim(0, 15)

    plt.tight_layout()
    fig_path = os.path.join(OUT_DIR, "matched_filter_irregular_test.png")
    plt.savefig(fig_path, dpi=150)
    print(f"Figure saved to {fig_path}")

    # ── Prime-log figure ───────────────────────────────────────────
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    res_p = all_results[("prime-log", len(primes))]
    for method, data in res_p.items():
        pn = data["power"] / data["power"].max()
        ax2.plot(freqs_hz_prime, pn, label=method, alpha=0.7, linewidth=0.8)
    for f in FREQS:
        ax2.axvline(f, color="red", linestyle="--", alpha=0.3)
    ax2.set_title(f"Prime-log sampling ({len(primes)} primes ≤ 1000)")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Normalized power")
    ax2.legend()
    plt.tight_layout()
    fig2_path = os.path.join(OUT_DIR, "matched_filter_prime_log.png")
    plt.savefig(fig2_path, dpi=150)
    print(f"Prime-log figure saved to {fig2_path}")

if __name__ == "__main__":
    main()
