#!/usr/bin/env python3
"""
Direct test of Chowla conjecture via lag-h correlations.

Chowla conjecture: sum_{n<=N} mu(n)*mu(n+h) = o(N) for all h >= 1.

Tests:
1. S_h / N -> 0 as N -> inf (Chowla)
2. |S_h| / sqrt(N) ~ O(1) (random walk heuristic)
3. Power spectrum of mu(n) ~ white noise under Chowla
4. Convergence rate across multiple N values
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import time

NMAX = 500_000
LAGS = list(range(1, 51))
N_VALUES = [10_000, 50_000, 100_000, 500_000]

def mobius_sieve(N):
    """Compute mu(n) for n=0..N using sieve."""
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    primes = []

    # First: smallest prime factor sieve
    spf = np.zeros(N + 1, dtype=np.int32)
    for i in range(2, N + 1):
        if is_prime[i]:
            primes.append(i)
            spf[i] = i
            for j in range(i * i, N + 1, i):
                is_prime[j] = False
                if spf[j] == 0:
                    spf[j] = i

    # Compute mu via factorization
    mu[1] = 1
    for n in range(2, N + 1):
        if spf[n] == n:  # prime
            mu[n] = -1
        else:
            p = spf[n]
            m = n // p
            if m % p == 0:
                mu[n] = 0  # p^2 | n
            else:
                mu[n] = -mu[m]

    return mu

def compute_lag_correlations(mu, N, lags):
    """Compute S_h = sum_{n=1}^{N-h} mu(n)*mu(n+h) for each lag h."""
    results = {}
    for h in lags:
        S_h = np.sum(mu[1:N-h+1].astype(np.int64) * mu[1+h:N+1].astype(np.int64))
        results[h] = int(S_h)
    return results

def compute_power_spectrum(mu, N, n_freqs=500):
    """Compute power spectrum of mu(n) at n_freqs equally spaced frequencies in [0, 0.5]."""
    mu_seq = mu[1:N+1].astype(np.float64)
    freqs = np.linspace(0, 0.5, n_freqs, endpoint=False)
    # Use FFT for efficiency
    fft_vals = np.fft.rfft(mu_seq)
    power = np.abs(fft_vals) ** 2 / N
    # Sample at evenly spaced frequencies
    fft_freqs = np.fft.rfftfreq(N)
    # Interpolate to our grid
    from scipy.interpolate import interp1d
    interp = interp1d(fft_freqs, power, kind='linear', fill_value='extrapolate')
    P = interp(freqs)
    return freqs, P

def main():
    print("=" * 70)
    print("CHOWLA CONJECTURE: LAG-h CORRELATION TEST")
    print("=" * 70)

    # Step 1: Mobius sieve
    t0 = time.time()
    print(f"\n[1] Computing mu(n) for n=1..{NMAX}...")
    mu = mobius_sieve(NMAX)
    t1 = time.time()
    print(f"    Done in {t1-t0:.2f}s")

    # Quick sanity check
    n_nonzero = np.count_nonzero(mu[1:NMAX+1])
    n_squarefree = n_nonzero
    frac_sf = n_squarefree / NMAX
    print(f"    Squarefree fraction: {frac_sf:.6f} (expected ~6/pi^2 = {6/np.pi**2:.6f})")
    print(f"    sum mu(n) for n<=N: {np.sum(mu[1:NMAX+1])}")

    # Step 2: Lag correlations for multiple N
    print(f"\n[2] Computing lag correlations S_h for h=1..{max(LAGS)}...")
    all_results = {}
    for N in N_VALUES:
        results = compute_lag_correlations(mu, N, LAGS)
        all_results[N] = results

    # Print table for N=500000
    N = NMAX
    results = all_results[N]
    print(f"\n    N = {N}:")
    print(f"    {'h':>4s}  {'S_h':>12s}  {'S_h/N':>12s}  {'|S_h|/sqrt(N)':>14s}")
    print(f"    {'---':>4s}  {'---':>12s}  {'---':>12s}  {'---':>14s}")
    for h in LAGS:
        S_h = results[h]
        ratio = S_h / N
        normalized = abs(S_h) / np.sqrt(N)
        print(f"    {h:4d}  {S_h:12d}  {ratio:12.8f}  {normalized:14.4f}")

    # Step 3: Convergence analysis
    print(f"\n[3] Convergence of S_h/N across N values (h=1):")
    print(f"    {'N':>8s}  {'S_1/N':>12s}  {'|S_1|/sqrt(N)':>14s}  {'|S_1|/N^0.5':>12s}")
    for N in N_VALUES:
        S1 = all_results[N][1]
        print(f"    {N:8d}  {S1/N:12.8f}  {abs(S1)/np.sqrt(N):14.4f}  {abs(S1)/N**0.5:12.4f}")

    # Step 4: Check decay rate - fit |S_h(N)| ~ N^alpha
    print(f"\n[4] Decay rate analysis: fitting |S_1(N)| ~ N^alpha")
    log_N = np.log(np.array(N_VALUES, dtype=float))
    log_S = np.log(np.array([abs(all_results[N][1]) for N in N_VALUES], dtype=float))
    # Linear fit
    coeffs = np.polyfit(log_N, log_S, 1)
    alpha = coeffs[0]
    print(f"    Fitted exponent alpha = {alpha:.4f}")
    print(f"    (Chowla predicts alpha < 1; random walk gives alpha ~ 0.5)")

    # Average over all lags
    alphas = []
    for h in LAGS[:20]:
        vals = [abs(all_results[N][h]) for N in N_VALUES]
        if all(v > 0 for v in vals):
            c = np.polyfit(log_N, np.log(np.array(vals, dtype=float)), 1)
            alphas.append(c[0])
    avg_alpha = np.mean(alphas) if alphas else float('nan')
    print(f"    Average alpha over h=1..20: {avg_alpha:.4f}")

    # Step 5: Power spectrum
    print(f"\n[5] Power spectrum of mu(n) for N={NMAX}...")
    freqs, P = compute_power_spectrum(mu, NMAX)
    mean_P = np.mean(P)
    std_P = np.std(P)
    cv = std_P / mean_P if mean_P > 0 else float('inf')
    print(f"    Mean power: {mean_P:.6f}")
    print(f"    Std power:  {std_P:.6f}")
    print(f"    Coefficient of variation: {cv:.4f}")
    print(f"    (White noise CV ~ 1/sqrt(n_bins) for chi-squared; actual value depends on bin count)")

    # Expected density of squarefree: 6/pi^2
    expected_power = 6 / np.pi**2  # approximate expected power per frequency
    print(f"    Expected mean power (heuristic ~6/pi^2): {expected_power:.6f}")

    # Step 6: Autocorrelation function check
    print(f"\n[6] Autocorrelation C(h) = S_h / S_0 for N={NMAX}:")
    S_0 = np.sum(mu[1:NMAX+1].astype(np.int64) ** 2)  # = number of squarefree integers
    print(f"    S_0 (squarefree count) = {S_0}")
    print(f"    {'h':>4s}  {'C(h)':>12s}")
    for h in LAGS[:20]:
        C_h = all_results[NMAX][h] / S_0
        print(f"    {h:4d}  {C_h:12.8f}")

    # ===== PLOTS =====
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: S_h/N vs h for different N
    ax = axes[0, 0]
    for N in N_VALUES:
        ratios = [all_results[N][h] / N for h in LAGS]
        ax.plot(LAGS, ratios, 'o-', markersize=3, label=f'N={N:,}')
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax.set_xlabel('Lag h')
    ax.set_ylabel('S_h / N')
    ax.set_title('Chowla: S_h/N vs h (should → 0)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 2: |S_h|/sqrt(N) vs h
    ax = axes[0, 1]
    for N in N_VALUES:
        norms = [abs(all_results[N][h]) / np.sqrt(N) for h in LAGS]
        ax.plot(LAGS, norms, 'o-', markersize=3, label=f'N={N:,}')
    ax.set_xlabel('Lag h')
    ax.set_ylabel('|S_h| / sqrt(N)')
    ax.set_title('Random walk normalization (should be O(1))')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 3: Convergence of S_1/N
    ax = axes[1, 0]
    for h in [1, 2, 5, 10, 25, 50]:
        ratios = [abs(all_results[N][h]) / N for N in N_VALUES]
        ax.plot(N_VALUES, ratios, 'o-', markersize=5, label=f'h={h}')
    ax.set_xlabel('N')
    ax.set_ylabel('|S_h| / N')
    ax.set_title('Convergence: |S_h|/N vs N')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 4: Power spectrum
    ax = axes[1, 1]
    # Subsample for plotting
    step = max(1, len(freqs) // 200)
    ax.plot(freqs[::step], P[::step], '-', alpha=0.7, linewidth=0.8)
    ax.axhline(y=mean_P, color='r', linestyle='--', label=f'Mean = {mean_P:.4f}')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Power')
    ax.set_title(f'Power spectrum of mu(n), N={NMAX:,} (CV={cv:.3f})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/saar/Desktop/Farey-Local/experiments/chowla_lag_test.png', dpi=150)
    print(f"\n    Plot saved to chowla_lag_test.png")

    # ===== VERDICT =====
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    # Check 1: S_h/N decreasing?
    max_ratio_500k = max(abs(all_results[NMAX][h]) / NMAX for h in LAGS)
    max_ratio_10k = max(abs(all_results[10_000][h]) / 10_000 for h in LAGS)
    decreasing = max_ratio_500k < max_ratio_10k

    print(f"\n  1. S_h/N DECREASING with N?")
    print(f"     max|S_h/N| at N=10K:  {max_ratio_10k:.8f}")
    print(f"     max|S_h/N| at N=500K: {max_ratio_500k:.8f}")
    print(f"     Decreasing: {'YES' if decreasing else 'NO'}")

    # Check 2: Random walk scaling?
    rw_ratios = [abs(all_results[N][1]) / np.sqrt(N) for N in N_VALUES]
    rw_stable = max(rw_ratios) / min(rw_ratios) < 10 if min(rw_ratios) > 0 else False
    print(f"\n  2. |S_1|/sqrt(N) STABLE (random walk)?")
    for i, N in enumerate(N_VALUES):
        print(f"     N={N:>8,}: {rw_ratios[i]:.4f}")
    print(f"     Max/Min ratio: {max(rw_ratios)/min(rw_ratios):.2f}" if min(rw_ratios) > 0 else "     N/A")
    print(f"     Roughly stable: {'YES' if rw_stable else 'NO/UNCLEAR'}")

    # Check 3: Power spectrum flat?
    print(f"\n  3. Power spectrum FLAT (white noise)?")
    print(f"     CV = {cv:.4f}")
    # For white noise with 500 bins, CV ~ 1.0 (exponential distribution)
    print(f"     (For exponential distribution CV=1; observed CV should be ~1)")
    flat = 0.5 < cv < 2.0
    print(f"     Approximately flat: {'YES' if flat else 'NO'}")

    # Check 4: Decay exponent
    print(f"\n  4. Growth exponent alpha (|S_h| ~ N^alpha)?")
    print(f"     alpha = {avg_alpha:.4f}")
    chowla_consistent = avg_alpha < 0.9  # well below 1
    print(f"     Chowla requires alpha < 1; random walk gives ~0.5")
    print(f"     Consistent with Chowla: {'YES' if chowla_consistent else 'NO'}")

    n_pass = sum([decreasing, rw_stable, flat, chowla_consistent])
    print(f"\n  OVERALL: {n_pass}/4 checks passed.")
    if n_pass >= 3:
        print(f"  CONCLUSION: STRONG computational evidence FOR Chowla conjecture at N={NMAX:,}.")
    elif n_pass >= 2:
        print(f"  CONCLUSION: Moderate computational evidence for Chowla conjecture at N={NMAX:,}.")
    else:
        print(f"  CONCLUSION: Mixed/weak evidence. Larger N may be needed.")

    # Return summary dict for report
    return {
        'max_ratio_10k': max_ratio_10k,
        'max_ratio_500k': max_ratio_500k,
        'decreasing': decreasing,
        'avg_alpha': avg_alpha,
        'cv': cv,
        'n_pass': n_pass,
        'rw_ratios': rw_ratios,
    }

if __name__ == '__main__':
    summary = main()
