#!/usr/bin/env python3
"""
FT of per-prime DeltaW to detect zeta zero pairs (MPR-34).
Compares DeltaW spectroscope with M(p)/p spectroscope.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import gcd
import time, sys, os, bisect

OUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")

# ---------- 1. Prime sieve ----------
def sieve(n):
    is_p = bytearray(b'\x01') * (n + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return [i for i in range(2, n + 1) if is_p[i]]

# ---------- 2. Moebius sieve ----------
def moebius_sieve(n):
    mu = np.zeros(n + 1, dtype=int)
    mu[1] = 1
    smallest_pf = list(range(n + 1))
    is_prime = bytearray(b'\x01') * (n + 1)
    is_prime[0] = is_prime[1] = 0
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            smallest_pf[i] = i
        for p in primes:
            if p > smallest_pf[i] or i * p > n:
                break
            is_prime[i * p] = 0
            smallest_pf[i * p] = p
    for i in range(2, n + 1):
        x = i
        mu_val = 1
        while x > 1:
            p = smallest_pf[x]
            count = 0
            while x % p == 0:
                x //= p
                count += 1
            if count > 1:
                mu_val = 0
                break
            mu_val *= -1
        mu[i] = mu_val
    return mu

# ---------- 3. Known zeta zeros ----------
ZETA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
]

# ---------- MAIN ----------
def main():
    MAX_P = 2000

    # Speed test
    print("Speed test...")
    t0 = time.time()
    farey = [0.0, 1.0]
    for n in range(2, 501):
        for a in range(1, n):
            if gcd(a, n) == 1:
                bisect.insort(farey, a / n)
    t_500 = time.time() - t0
    print(f"Incremental Farey up to n=500 took {t_500:.2f}s, |F_500|={len(farey)}")

    est_2000 = t_500 * (2000/500)**2.3  # slightly superquadratic due to insort
    print(f"Estimated time for n=2000: {est_2000:.0f}s")

    if est_2000 > 120:
        MAX_P = 1000
        print(f"Reducing to MAX_P={MAX_P}")
    elif est_2000 > 60:
        MAX_P = 1500
        print(f"Adjusting to MAX_P={MAX_P}")
    else:
        print(f"Proceeding with MAX_P={MAX_P}")

    primes = sieve(MAX_P)
    n_primes = len(primes)
    print(f"Found {n_primes} primes up to {MAX_P}")

    needed_n = set()
    for p in primes:
        needed_n.add(p - 1)
        needed_n.add(p)

    max_n = max(needed_n)
    print(f"Need W for {len(needed_n)} distinct n, max n={max_n}")

    # Build Farey incrementally from scratch (not reusing the speed test)
    print("\nBuilding Farey sequences incrementally...")
    farey = [0.0, 1.0]
    W_cache = {}
    if 1 in needed_n:
        N = len(farey)
        w = sum((farey[j] - j/N)**2 for j in range(N))
        W_cache[1] = w

    t_start = time.time()
    last_report = t_start

    for n in range(2, max_n + 1):
        new_fracs = []
        for a in range(1, n):
            if gcd(a, n) == 1:
                new_fracs.append(a / n)
        for f in new_fracs:
            bisect.insort(farey, f)

        if n in needed_n:
            N = len(farey)
            w = 0.0
            for j in range(N):
                diff = farey[j] - j / N
                w += diff * diff
            W_cache[n] = w

        now = time.time()
        if now - last_report > 10.0:
            elapsed = now - t_start
            frac_done = n / max_n
            eta = elapsed / frac_done * (1 - frac_done) if frac_done > 0 else 0
            print(f"  n={n}/{max_n}, |F_n|={len(farey)}, elapsed={elapsed:.0f}s, ETA={eta:.0f}s")
            last_report = now

    elapsed = time.time() - t_start
    print(f"Farey computation done in {elapsed:.1f}s, |F_{max_n}|={len(farey)}")

    # Compute DeltaW
    delta_w = np.zeros(n_primes)
    for i, p in enumerate(primes):
        delta_w[i] = W_cache[p - 1] - W_cache[p]

    primes_arr = np.array(primes, dtype=float)
    print(f"\nDeltaW stats: mean={np.mean(delta_w):.6e}, std={np.std(delta_w):.6e}")
    print(f"  min={np.min(delta_w):.6e}, max={np.max(delta_w):.6e}")

    # ---------- Mertens ----------
    print("\nComputing Mertens function...")
    mu = moebius_sieve(MAX_P)
    M = np.cumsum(mu)

    Mp_over_p = np.zeros(n_primes)
    for i, p in enumerate(primes):
        Mp_over_p[i] = M[p] / p

    # ---------- Spectroscopes ----------
    print("Computing spectroscopes...")
    gamma_grid = np.linspace(5, 60, 10000)
    spec_dw = np.zeros(len(gamma_grid))
    spec_mp = np.zeros(len(gamma_grid))
    log_p = np.log(primes_arr)
    p_half = primes_arr**(-0.5)

    for ig, g in enumerate(gamma_grid):
        phase = -g * log_p
        cos_ph = np.cos(phase)
        sin_ph = np.sin(phase)

        w_dw = delta_w * p_half
        s_dw_re = np.dot(w_dw, cos_ph)
        s_dw_im = np.dot(w_dw, sin_ph)
        spec_dw[ig] = g**2 * (s_dw_re**2 + s_dw_im**2)

        w_mp = Mp_over_p * p_half
        s_mp_re = np.dot(w_mp, cos_ph)
        s_mp_im = np.dot(w_mp, sin_ph)
        spec_mp[ig] = g**2 * (s_mp_re**2 + s_mp_im**2)

        if (ig + 1) % 2500 == 0:
            print(f"  gamma point {ig+1}/{len(gamma_grid)}")

    print("Spectroscopes done.")

    # ---------- Z-scores ----------
    print("\nComputing z-scores...")
    window_half = 2.0
    narrow = 5

    results = []
    for iz, gz in enumerate(ZETA_ZEROS):
        idx_center = np.argmin(np.abs(gamma_grid - gz))
        idx_lo = np.searchsorted(gamma_grid, gz - window_half)
        idx_hi = np.searchsorted(gamma_grid, gz + window_half)
        idx_peak_lo = max(idx_center - narrow, 0)
        idx_peak_hi = min(idx_center + narrow + 1, len(gamma_grid))

        peak_dw = np.max(spec_dw[idx_peak_lo:idx_peak_hi])
        window_dw = np.concatenate([spec_dw[idx_lo:idx_peak_lo], spec_dw[idx_peak_hi:idx_hi]])
        z_dw = (peak_dw - np.mean(window_dw)) / (np.std(window_dw) + 1e-30) if len(window_dw) > 2 else 0.0

        peak_mp = np.max(spec_mp[idx_peak_lo:idx_peak_hi])
        window_mp = np.concatenate([spec_mp[idx_lo:idx_peak_lo], spec_mp[idx_peak_hi:idx_hi]])
        z_mp = (peak_mp - np.mean(window_mp)) / (np.std(window_mp) + 1e-30) if len(window_mp) > 2 else 0.0

        results.append((iz + 1, gz, peak_dw, z_dw, peak_mp, z_mp))

    # ---------- Print table ----------
    print("\n" + "=" * 80)
    print("COMPARISON: DeltaW vs M(p)/p spectroscope at zeta zeros")
    print(f"Primes up to {MAX_P} ({n_primes} primes)")
    print("=" * 80)
    header = f"{'#':>3} {'gamma':>10} {'DW_peak':>12} {'DW_z':>8} {'Mp_peak':>12} {'Mp_z':>8}"
    print(header)
    print("-" * len(header))
    for (idx, gz, pk_dw, z_dw, pk_mp, z_mp) in results:
        print(f"{idx:>3} {gz:>10.4f} {pk_dw:>12.4e} {z_dw:>8.2f} {pk_mp:>12.4e} {z_mp:>8.2f}")

    z_dw_arr = np.array([r[3] for r in results])
    z_mp_arr = np.array([r[5] for r in results])
    corr = np.corrcoef(z_dw_arr, z_mp_arr)[0, 1] if len(z_dw_arr) > 1 else 0.0
    mean_z_dw = np.mean(z_dw_arr)
    mean_z_mp = np.mean(z_mp_arr)
    print(f"\nZ-score correlation (DW vs Mp): {corr:.4f}")
    print(f"Mean z-score: DW = {mean_z_dw:.2f}, Mp = {mean_z_mp:.2f}")

    # ---------- Plot ----------
    print("\nGenerating plot...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    ax1.plot(gamma_grid, spec_dw, 'b-', linewidth=0.5, label='DeltaW spectroscope')
    for gz in ZETA_ZEROS:
        ax1.axvline(gz, color='red', alpha=0.5, linestyle='--', linewidth=0.8)
    ax1.set_ylabel('F_DW(gamma)')
    ax1.set_title(f'DeltaW Spectroscope (primes up to {MAX_P})')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(gamma_grid, spec_mp, 'g-', linewidth=0.5, label='M(p)/p spectroscope')
    for gz in ZETA_ZEROS:
        ax2.axvline(gz, color='red', alpha=0.5, linestyle='--', linewidth=0.8)
    ax2.set_xlabel('gamma')
    ax2.set_ylabel('F_M(gamma)')
    ax2.set_title(f'M(p)/p Spectroscope (primes up to {MAX_P})')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plot_path = os.path.join(OUT_DIR, 'ft_deltaw_zeros.png')
    plt.savefig(plot_path, dpi=150)
    print(f"Plot saved: {plot_path}")

    # ---------- Report ----------
    if mean_z_dw > 2.0 and mean_z_mp > 2.0:
        conclusion = ("Both DeltaW and M(p)/p spectroscopes show strong peaks at zeta zeros. "
                      "Raw DeltaW carries the SAME zeta-zero information as M(p)/p.")
    elif mean_z_dw > 1.5:
        conclusion = ("DeltaW spectroscope shows moderate peaks at zeta zeros. "
                      "The signal is present but weaker than in M(p)/p.")
    elif mean_z_dw > 0.5:
        conclusion = ("DeltaW spectroscope shows weak but detectable peaks at zeta zeros. "
                      "The zeta-zero signal in raw DeltaW is attenuated compared to M(p)/p.")
    else:
        conclusion = ("DeltaW spectroscope does NOT show clear peaks at zeta zeros with this prime range. "
                      "The raw DeltaW signal may require filtering or larger prime ranges "
                      "to reveal zeta-zero content.")

    report_path = os.path.join(OUT_DIR, 'FT_DELTAW_ZEROS.md')
    with open(report_path, 'w') as f:
        f.write("# FT of DeltaW: Zeta Zero Detection (MPR-34)\n\n")
        f.write(f"**Date:** 2026-04-06\n")
        f.write(f"**Prime range:** 2 to {MAX_P} ({n_primes} primes)\n")
        f.write(f"**Gamma range:** [5, 60], 10000 points\n\n")

        f.write("## Method\n\n")
        f.write("For each prime p, we compute:\n")
        f.write("- Farey sequences F_{p-1} and F_p (built incrementally)\n")
        f.write("- Weyl discrepancy W(F_n) = sum_j (f_j - j/N)^2\n")
        f.write("- DeltaW(p) = W(F_{p-1}) - W(F_p)\n\n")
        f.write("Spectroscopes:\n")
        f.write("- DeltaW: F_DW(gamma) = gamma^2 * |sum_p DeltaW(p) * p^{-1/2-i*gamma}|^2\n")
        f.write("- M(p)/p: F_M(gamma) = gamma^2 * |sum_p (M(p)/p) * p^{-1/2-i*gamma}|^2\n\n")

        f.write("## DeltaW Statistics\n\n")
        f.write(f"- Mean: {np.mean(delta_w):.6e}\n")
        f.write(f"- Std: {np.std(delta_w):.6e}\n")
        f.write(f"- Min: {np.min(delta_w):.6e}\n")
        f.write(f"- Max: {np.max(delta_w):.6e}\n\n")

        f.write("## Comparison Table\n\n")
        f.write("| # | gamma | DW_peak | DW_z | Mp_peak | Mp_z |\n")
        f.write("|---|-------|---------|------|---------|------|\n")
        for (idx, gz, pk_dw, z_dw, pk_mp, z_mp) in results:
            f.write(f"| {idx} | {gz:.4f} | {pk_dw:.4e} | {z_dw:.2f} | {pk_mp:.4e} | {z_mp:.2f} |\n")

        f.write(f"\n**Z-score correlation (DW vs Mp):** {corr:.4f}\n")
        f.write(f"**Mean z-score:** DW = {mean_z_dw:.2f}, Mp = {mean_z_mp:.2f}\n\n")

        f.write("## Conclusion\n\n")
        f.write(conclusion + "\n\n")

        f.write("## Plot\n\n")
        f.write("![DeltaW vs M(p)/p Spectroscopes](ft_deltaw_zeros.png)\n")

    print(f"Report saved: {report_path}")
    print("\nDone!")

if __name__ == "__main__":
    main()
