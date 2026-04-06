#!/usr/bin/env python3
"""
Psi vs Mertens Spectroscope Comparison
=======================================
Compare three spectroscopes for detecting zeta zeros:
  1. Mertens: F_M(gamma) = gamma^2 * |sum M(p)/p * exp(-i*gamma*log(p))|^2
  2. Psi error: F_psi(gamma) = gamma^2 * |sum (psi(p)-p)/p * exp(-i*gamma*log(p))|^2
  3. Von Mangoldt-like: F_log(gamma) = gamma^2 * |sum log(p)/p * exp(-i*gamma*log(p))|^2

The key theoretical difference:
  - Mertens explicit formula coefficients: c_k = 1/(rho_k * zeta'(rho_k))
  - Chebyshev psi explicit formula coefficients: -x^rho / rho  (NO zeta' in denominator)
  - So psi peaks decay as 1/gamma, Mertens peaks decay as 1/(gamma * |zeta'|)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import time
import sys

# ── Sieve of Eratosthenes ──────────────────────────────────────────
def sieve_primes(N):
    """Return sorted array of primes up to N."""
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(N**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return np.where(is_prime)[0]

# ── Mobius function via sieve ───────────────────────────────────────
def mobius_sieve(N):
    """Compute mu(n) for n = 0..N using a sieve."""
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    # smallest prime factor
    spf = np.zeros(N + 1, dtype=np.int32)
    for i in range(2, N + 1):
        if spf[i] == 0:  # i is prime
            for j in range(i, N + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    # compute mu
    for n in range(2, N + 1):
        p = spf[n]
        if (n // p) % p == 0:
            mu[n] = 0  # p^2 | n
        else:
            mu[n] = -mu[n // p]
    return mu

# ── Known zeta zeros (first 30) ────────────────────────────────────
ZETA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
]

def main():
    N = 1_000_000
    print(f"Sieving primes up to {N:,}...")
    t0 = time.time()
    primes = sieve_primes(N)
    print(f"  Found {len(primes):,} primes in {time.time()-t0:.1f}s")

    print("Computing Mobius function...")
    t0 = time.time()
    mu = mobius_sieve(N)
    print(f"  Done in {time.time()-t0:.1f}s")

    # ── Compute M(p), psi(p), psi_error(p) at each prime ───────────
    print("Computing arithmetic functions at primes...")
    M_vals = np.cumsum(mu[primes])          # M(p) = sum_{n<=p} mu(n) ... wait, M(p) = sum_{n<=p} mu(n)
    # Actually M(p) = sum_{n=1}^{p} mu(n), not just at primes
    # We need the running sum of mu up to each prime
    cummu = np.cumsum(mu)  # cummu[n] = sum_{k=0}^{n} mu(k) = sum_{k=1}^{n} mu(k) since mu[0]=0
    M_at_primes = cummu[primes]  # M(p) for each prime p

    # psi(p) = sum_{q prime, q<=p} log(q)  (prime part of Chebyshev; ignoring prime powers for simplicity)
    log_primes = np.log(primes.astype(np.float64))
    psi_at_primes = np.cumsum(log_primes)   # psi(p) at each prime

    # psi_error(p) = psi(p) - p
    psi_error = psi_at_primes - primes.astype(np.float64)

    # ── Spectroscope computation ────────────────────────────────────
    # Scan gamma from 10 to 110 with fine resolution
    gamma_min, gamma_max = 10.0, 110.0
    n_gamma = 8000
    gammas = np.linspace(gamma_min, gamma_max, n_gamma)

    # Precompute log(p) and 1/p
    logp = log_primes
    inv_p = 1.0 / primes.astype(np.float64)

    # Weights for each spectroscope
    w_mertens = M_at_primes.astype(np.float64) * inv_p      # M(p)/p
    w_psi     = psi_error * inv_p                             # (psi(p)-p)/p
    w_log     = log_primes * inv_p                            # log(p)/p

    print(f"Computing 3 spectroscopes over {n_gamma} gamma values...")
    t0 = time.time()

    F_mertens = np.zeros(n_gamma)
    F_psi     = np.zeros(n_gamma)
    F_log     = np.zeros(n_gamma)

    # Vectorized: for each gamma, compute sum of w * exp(-i*gamma*log(p))
    # This is O(n_gamma * n_primes) which is ~8000 * 78498 ~ 6e8 -- use chunking
    chunk_size = 200
    n_chunks = (n_gamma + chunk_size - 1) // chunk_size

    for ci in range(n_chunks):
        i0 = ci * chunk_size
        i1 = min(i0 + chunk_size, n_gamma)
        g_chunk = gammas[i0:i1]  # shape (chunk,)

        # phase matrix: shape (chunk, n_primes)
        phase = np.outer(g_chunk, logp)  # gamma * log(p)

        # exp(-i * phase)
        cos_phase = np.cos(phase)
        sin_phase = np.sin(phase)

        # Mertens spectroscope
        re_m = cos_phase @ w_mertens
        im_m = -sin_phase @ w_mertens
        F_mertens[i0:i1] = g_chunk**2 * (re_m**2 + im_m**2)

        # Psi spectroscope
        re_p = cos_phase @ w_psi
        im_p = -sin_phase @ w_psi
        F_psi[i0:i1] = g_chunk**2 * (re_p**2 + im_p**2)

        # Log spectroscope
        re_l = cos_phase @ w_log
        im_l = -sin_phase @ w_log
        F_log[i0:i1] = g_chunk**2 * (re_l**2 + im_l**2)

        if (ci + 1) % 10 == 0:
            elapsed = time.time() - t0
            pct = 100 * (ci + 1) / n_chunks
            print(f"  {pct:.0f}% ({elapsed:.1f}s)")

    elapsed = time.time() - t0
    print(f"  Spectroscope computation done in {elapsed:.1f}s")

    # ── Z-score computation ─────────────────────────────────────────
    def compute_zscores(gammas, F_vals, zeros, window_half=2.0, peak_half=0.3):
        """
        For each zero, compute z-score = (peak - local_mean) / local_std.
        local statistics from [gamma-window_half, gamma+window_half] excluding [gamma-peak_half, gamma+peak_half].
        """
        results = []
        for gamma0 in zeros:
            if gamma0 < gammas[0] or gamma0 > gammas[-1]:
                results.append((gamma0, np.nan, np.nan))
                continue
            # Background region
            bg_mask = (np.abs(gammas - gamma0) <= window_half) & (np.abs(gammas - gamma0) > peak_half)
            bg = F_vals[bg_mask]
            if len(bg) < 10:
                results.append((gamma0, np.nan, np.nan))
                continue
            bg_mean = np.mean(bg)
            bg_std = np.std(bg)
            # Peak value
            peak_mask = np.abs(gammas - gamma0) <= peak_half
            if not np.any(peak_mask):
                results.append((gamma0, np.nan, np.nan))
                continue
            peak_val = np.max(F_vals[peak_mask])
            zscore = (peak_val - bg_mean) / bg_std if bg_std > 0 else 0.0
            results.append((gamma0, peak_val, zscore))
        return results

    first_20_zeros = ZETA_ZEROS[:20]

    print("\nComputing z-scores for first 20 zeta zeros...")
    zs_mertens = compute_zscores(gammas, F_mertens, first_20_zeros)
    zs_psi     = compute_zscores(gammas, F_psi, first_20_zeros)
    zs_log     = compute_zscores(gammas, F_log, first_20_zeros)

    # ── Print comparison table ──────────────────────────────────────
    print("\n" + "="*90)
    print(f"{'Zero':>10s}  {'Mertens z':>10s}  {'Psi z':>10s}  {'Log z':>10s}  {'Winner':>10s}")
    print("="*90)

    n_detected = {'mertens': 0, 'psi': 0, 'log': 0}
    z_sums = {'mertens': 0.0, 'psi': 0.0, 'log': 0.0}
    z_threshold = 3.0
    winners = {'mertens': 0, 'psi': 0, 'log': 0}

    for i in range(20):
        gm, _, zm = zs_mertens[i]
        _, _, zp = zs_psi[i]
        _, _, zl = zs_log[i]

        if not np.isnan(zm): z_sums['mertens'] += zm
        if not np.isnan(zp): z_sums['psi'] += zp
        if not np.isnan(zl): z_sums['log'] += zl

        if not np.isnan(zm) and zm >= z_threshold: n_detected['mertens'] += 1
        if not np.isnan(zp) and zp >= z_threshold: n_detected['psi'] += 1
        if not np.isnan(zl) and zl >= z_threshold: n_detected['log'] += 1

        scores = {'mertens': zm if not np.isnan(zm) else -999,
                  'psi': zp if not np.isnan(zp) else -999,
                  'log': zl if not np.isnan(zl) else -999}
        winner = max(scores, key=scores.get)
        winners[winner] += 1

        print(f"{gm:10.3f}  {zm:10.2f}  {zp:10.2f}  {zl:10.2f}  {winner:>10s}")

    print("="*90)
    print(f"\nDetections (z >= {z_threshold}):")
    print(f"  Mertens: {n_detected['mertens']}/20")
    print(f"  Psi:     {n_detected['psi']}/20")
    print(f"  Log:     {n_detected['log']}/20")

    avg_z = {k: v/20 for k, v in z_sums.items()}
    print(f"\nAverage z-score:")
    print(f"  Mertens: {avg_z['mertens']:.2f}")
    print(f"  Psi:     {avg_z['psi']:.2f}")
    print(f"  Log:     {avg_z['log']:.2f}")

    print(f"\nWins (highest z per zero):")
    print(f"  Mertens: {winners['mertens']}/20")
    print(f"  Psi:     {winners['psi']}/20")
    print(f"  Log:     {winners['log']}/20")

    # ── Compute normalized versions for plotting ────────────────────
    # Normalize each to its own max for visual comparison
    F_m_norm = F_mertens / np.max(F_mertens) if np.max(F_mertens) > 0 else F_mertens
    F_p_norm = F_psi / np.max(F_psi) if np.max(F_psi) > 0 else F_psi
    F_l_norm = F_log / np.max(F_log) if np.max(F_log) > 0 else F_log

    # ── Figure: 3-panel overlay ─────────────────────────────────────
    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

    colors = ['#2196F3', '#E91E63', '#4CAF50']
    labels = ['Mertens: $\\gamma^2 |\\sum M(p)/p \\cdot e^{-i\\gamma\\log p}|^2$',
              'Psi error: $\\gamma^2 |\\sum (\\psi(p)-p)/p \\cdot e^{-i\\gamma\\log p}|^2$',
              'Von Mangoldt: $\\gamma^2 |\\sum \\log(p)/p \\cdot e^{-i\\gamma\\log p}|^2$']
    F_all = [F_mertens, F_psi, F_log]
    F_norm_all = [F_m_norm, F_p_norm, F_l_norm]
    zscores_all = [zs_mertens, zs_psi, zs_log]
    names = ['Mertens', 'Psi error', 'Von Mangoldt']
    dict_keys = ['mertens', 'psi', 'log']

    for ax_idx, (ax, F_raw, F_norm, color, label, name, zscores, dkey) in enumerate(
            zip(axes, F_all, F_norm_all, colors, labels, names, zscores_all, dict_keys)):

        ax.plot(gammas, F_norm, color=color, linewidth=0.5, alpha=0.8)
        ax.fill_between(gammas, 0, F_norm, color=color, alpha=0.15)

        # Mark zeta zeros
        for i, (gamma0, peak, zscore) in enumerate(zscores):
            if gamma0 < gammas[0] or gamma0 > gammas[-1]:
                continue
            if not np.isnan(zscore):
                lw = 1.5 if zscore >= z_threshold else 0.5
                alpha = 0.9 if zscore >= z_threshold else 0.3
                ax.axvline(gamma0, color='red', linewidth=lw, alpha=alpha, linestyle='--')
                if zscore >= z_threshold and i < 20:
                    ax.text(gamma0, 0.95, f'z={zscore:.1f}', transform=ax.get_xaxis_transform(),
                            fontsize=6, ha='center', va='top', color='red', rotation=90)

        ax.set_ylabel('Normalized power', fontsize=10)
        ax.set_title(f'{name} spectroscope  (detections: {n_detected[dkey]}/20, '
                     f'avg z: {avg_z[dkey]:.1f})',
                     fontsize=11, fontweight='bold')
        ax.set_ylim(0, 1.1)
        ax.legend([label], loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel('$\\gamma$ (imaginary part of zeta zeros)', fontsize=11)

    fig.suptitle(f'Spectroscope Comparison: Mertens vs Chebyshev $\\psi$ vs Von Mangoldt\n'
                 f'$N = {N:,}$ primes sieved, $\\gamma^2$ matched filter, first 20 zeros',
                 fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    figpath = '/Users/saar/Desktop/Farey-Local/figures/psi_vs_mertens.png'
    plt.savefig(figpath, dpi=150, bbox_inches='tight')
    print(f"\nFigure saved to {figpath}")

    # ── Write markdown report ───────────────────────────────────────
    md_path = '/Users/saar/Desktop/Farey-Local/experiments/PSI_VS_MERTENS.md'
    with open(md_path, 'w') as f:
        f.write("# Psi vs Mertens Spectroscope Comparison\n\n")
        f.write(f"**Date:** 2026-04-05  \n")
        f.write(f"**Sieve limit:** N = {N:,}  \n")
        f.write(f"**Primes:** {len(primes):,}  \n")
        f.write(f"**Gamma range:** [{gamma_min}, {gamma_max}] with {n_gamma} points  \n")
        f.write(f"**Z-score threshold:** {z_threshold}  \n\n")

        f.write("## Theoretical Background\n\n")
        f.write("The explicit formulas for Mertens and Chebyshev differ in a crucial way:\n\n")
        f.write("- **Mertens M(x):** coefficients `c_k = 1/(rho_k * zeta'(rho_k))` -- peaks decay as `1/(gamma * |zeta'|)`\n")
        f.write("- **Chebyshev psi(x):** coefficients `-x^rho / rho` -- peaks decay as `1/gamma` (NO zeta' denominator)\n\n")
        f.write("This means psi-based spectroscopy should show **cleaner peaks** at higher zeros ")
        f.write("because there's no `|zeta'(rho)|` in the denominator to amplify noise.\n\n")

        f.write("## Three Spectroscopes\n\n")
        f.write("All use `gamma^2` matched filter:\n\n")
        f.write("1. **Mertens:** `F_M(gamma) = gamma^2 * |sum M(p)/p * exp(-i*gamma*log(p))|^2`\n")
        f.write("2. **Psi error:** `F_psi(gamma) = gamma^2 * |sum (psi(p)-p)/p * exp(-i*gamma*log(p))|^2`\n")
        f.write("3. **Von Mangoldt:** `F_log(gamma) = gamma^2 * |sum log(p)/p * exp(-i*gamma*log(p))|^2`\n\n")

        f.write("## Results\n\n")
        f.write("### Detection Summary\n\n")
        f.write("| Metric | Mertens | Psi error | Von Mangoldt |\n")
        f.write("|--------|---------|-----------|-------------|\n")
        f.write(f"| Detections (z >= {z_threshold}) | {n_detected['mertens']}/20 | {n_detected['psi']}/20 | {n_detected['log']}/20 |\n")
        f.write(f"| Avg z-score | {avg_z['mertens']:.2f} | {avg_z['psi']:.2f} | {avg_z['log']:.2f} |\n")
        f.write(f"| Best at zero (wins) | {winners['mertens']}/20 | {winners['psi']}/20 | {winners['log']}/20 |\n\n")

        f.write("### Per-Zero Detail\n\n")
        f.write("| Zero gamma | Mertens z | Psi z | Log z | Winner |\n")
        f.write("|-----------|----------|-------|-------|--------|\n")
        for i in range(20):
            gm, _, zm = zs_mertens[i]
            _, _, zp = zs_psi[i]
            _, _, zl = zs_log[i]
            scores = {'Mertens': zm if not np.isnan(zm) else -999,
                      'Psi': zp if not np.isnan(zp) else -999,
                      'Log': zl if not np.isnan(zl) else -999}
            winner = max(scores, key=scores.get)
            zm_s = f"{zm:.2f}" if not np.isnan(zm) else "N/A"
            zp_s = f"{zp:.2f}" if not np.isnan(zp) else "N/A"
            zl_s = f"{zl:.2f}" if not np.isnan(zl) else "N/A"
            f.write(f"| {gm:.3f} | {zm_s} | {zp_s} | {zl_s} | {winner} |\n")

        f.write("\n### Figure\n\n")
        f.write("![Psi vs Mertens spectroscope](../figures/psi_vs_mertens.png)\n\n")

        # Determine overall winner
        best_detect = max(n_detected, key=n_detected.get)
        best_avg = max(avg_z, key=avg_z.get)
        best_wins = max(winners, key=winners.get)

        f.write("## Analysis\n\n")
        f.write(f"- **Most detections:** {best_detect} ({n_detected[best_detect]}/20)\n")
        f.write(f"- **Highest avg z-score:** {best_avg} ({avg_z[best_avg]:.2f})\n")
        f.write(f"- **Most per-zero wins:** {best_wins} ({winners[best_wins]}/20)\n\n")

        if best_avg == 'psi' or best_detect == 'psi':
            f.write("### Psi advantage confirmed\n\n")
            f.write("The Chebyshev psi spectroscope performs well, consistent with the theoretical prediction:\n")
            f.write("without `|zeta'(rho)|` in the denominator, the signal-to-noise ratio improves.\n\n")
        elif best_avg == 'mertens' or best_detect == 'mertens':
            f.write("### Mertens advantage observed\n\n")
            f.write("Despite the theoretical disadvantage of the `|zeta'(rho)|` factor, the Mertens spectroscope\n")
            f.write("still performs well. The Mobius function's multiplicativity may provide compensating structure.\n\n")
        elif best_avg == 'log' or best_detect == 'log':
            f.write("### Von Mangoldt advantage observed\n\n")
            f.write("The `log(p)/p` weighting captures the prime counting contribution most directly.\n\n")

        f.write("## Implications for Farey Research\n\n")
        f.write("The spectroscope comparison reveals which arithmetic function most cleanly resonates\n")
        f.write("with zeta zeros. This informs the choice of weighting in the Farey discrepancy spectroscope:\n")
        f.write("if psi-weighting is superior, we should consider `log(p)` corrections to the Farey weights.\n")

    print(f"Report saved to {md_path}")

if __name__ == '__main__':
    main()
