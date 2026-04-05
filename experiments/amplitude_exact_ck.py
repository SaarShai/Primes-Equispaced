#!/usr/bin/env python3
"""
Exact amplitude matching for the Mertens spectroscope.
Uses mpmath for high-precision ζ'(ρ_k) instead of Stirling approximation.
"""
import numpy as np
from scipy import stats
import time, os

# ── 1. High-precision ζ'(ρ_k) via mpmath ──────────────────────────────────
from mpmath import mp, mpf, mpc, diff, zeta

mp.dps = 50  # 50-digit precision

gamma_k = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
           37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
           52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
           67.0798, 69.5464, 72.0672, 75.7047, 77.1448]

print("Computing ζ'(ρ_k) at 50-digit precision...")
t0 = time.time()

zprime_vals = []
ck_sq_vals = []
zprime_abs_vals = []

for k, g in enumerate(gamma_k, 1):
    rho = mpc(0.5, g)
    zp = diff(zeta, rho)
    zp_abs = float(abs(zp))
    rho_abs = float(abs(rho))
    ck_sq = 1.0 / (rho_abs * zp_abs)**2
    zprime_vals.append(zp)
    zprime_abs_vals.append(zp_abs)
    ck_sq_vals.append(ck_sq)
    print(f"  k={k:2d}  γ={g:8.4f}  |ζ'(ρ)|={zp_abs:.12f}  |c_k|²={ck_sq:.6e}")

print(f"  Done in {time.time()-t0:.1f}s")

# ── 2. Mobius sieve to 500K, M(p) for all primes ──────────────────────────
print("\nSieving Möbius to 500K...")
t0 = time.time()
LIMIT = 500_000

mu = np.ones(LIMIT + 1, dtype=np.int8)
mu[0] = 0

# Sieve of Eratosthenes for smallest prime factor + squarefree detection
is_prime = np.ones(LIMIT + 1, dtype=bool)
is_prime[0] = is_prime[1] = False

for p in range(2, int(LIMIT**0.5) + 1):
    if is_prime[p]:
        is_prime[p*p::p] = False
        # mu: flip sign for each prime factor
        mu[p::p] *= -1
        # mu: zero for square-free violation
        p2 = p * p
        mu[p2::p2] = 0

primes = np.where(is_prime)[0]
print(f"  Found {len(primes)} primes up to {LIMIT}")

# Mertens function M(n) = Σ_{k=1}^{n} μ(k)
M_cumsum = np.cumsum(mu.astype(np.int64))
M_at_primes = M_cumsum[primes]  # M(p) for each prime

print(f"  Sieve done in {time.time()-t0:.1f}s")

# ── 3. Spectral power F_comp(γ) ───────────────────────────────────────────
print("\nComputing F_comp(γ) on grid [5,85], 20000 points...")
t0 = time.time()

gamma_grid = np.linspace(5, 85, 20000)
log_primes = np.log(primes.astype(np.float64))
weights = M_at_primes.astype(np.float64) / primes.astype(np.float64)

F_comp = np.zeros(len(gamma_grid))

# Vectorized: for each gamma, compute |Σ w_j * e^{-iγ log p_j}|²
# Do in chunks to manage memory
CHUNK = 500
for i in range(0, len(gamma_grid), CHUNK):
    chunk = gamma_grid[i:i+CHUNK]
    # phase[j, p] = chunk[j] * log_primes[p]
    phase = np.outer(chunk, log_primes)
    # sum_val[j] = Σ_p weights[p] * e^{-i phase[j,p]}
    sum_val = np.sum(weights[None, :] * np.exp(-1j * phase), axis=1)
    F_comp[i:i+CHUNK] = chunk**2 * np.abs(sum_val)**2

print(f"  Done in {time.time()-t0:.1f}s")

# ── 4. Extract observed peaks at each γ_k ─────────────────────────────────
print("\nExtracting observed peak heights...")

observed_peaks = []
for g in gamma_k:
    idx = np.argmin(np.abs(gamma_grid - g))
    # Search in small window around γ_k for local max
    lo = max(0, idx - 50)
    hi = min(len(F_comp), idx + 51)
    local_max = np.max(F_comp[lo:hi])
    observed_peaks.append(local_max)
    
observed_peaks = np.array(observed_peaks)
ck_sq_arr = np.array(ck_sq_vals)

# ── 5. Correlations ───────────────────────────────────────────────────────
print("\nCorrelation analysis:")

# Pearson
r_pearson, p_pearson = stats.pearsonr(ck_sq_arr, observed_peaks)
print(f"  Pearson r = {r_pearson:.6f}  (p = {p_pearson:.4e})")

# Spearman rank
r_spearman, p_spearman = stats.spearmanr(ck_sq_arr, observed_peaks)
print(f"  Spearman ρ = {r_spearman:.6f}  (p = {p_spearman:.4e})")

# Consecutive ratio correlation
ratios_pred = ck_sq_arr[1:] / ck_sq_arr[:-1]
ratios_obs = observed_peaks[1:] / observed_peaks[:-1]
r_ratio, p_ratio = stats.pearsonr(ratios_pred, ratios_obs)
print(f"  Consecutive ratio r = {r_ratio:.6f}  (p = {p_ratio:.4e})")

# Log-space Pearson (often better for power-law data)
r_log, p_log = stats.pearsonr(np.log(ck_sq_arr), np.log(observed_peaks))
print(f"  Log-space Pearson r = {r_log:.6f}  (p = {p_log:.4e})")

# ── 6. Write results markdown ─────────────────────────────────────────────
outpath = os.path.expanduser("~/Desktop/Farey-Local/experiments/AMPLITUDE_EXACT_RESULTS.md")

lines = []
lines.append("# Exact Amplitude Matching: Mertens Spectroscope")
lines.append("")
lines.append("**Date:** " + time.strftime("%Y-%m-%d %H:%M"))
lines.append("**Method:** mpmath ζ'(ρ_k) at 50-digit precision (NOT Stirling approximation)")
lines.append(f"**Möbius sieve:** N = {LIMIT:,}")
lines.append(f"**Primes used:** {len(primes):,}")
lines.append(f"**Spectral grid:** {len(gamma_grid):,} points on [5, 85]")
lines.append("")
lines.append("## Correlation Metrics")
lines.append("")
lines.append(f"| Metric | Value | p-value |")
lines.append(f"|--------|-------|---------|")
lines.append(f"| Pearson r (|c_k|² vs peak) | {r_pearson:.6f} | {p_pearson:.4e} |")
lines.append(f"| Spearman ρ (rank) | {r_spearman:.6f} | {p_spearman:.4e} |")
lines.append(f"| Consecutive ratio r | {r_ratio:.6f} | {p_ratio:.4e} |")
lines.append(f"| Log-space Pearson r | {r_log:.6f} | {p_log:.4e} |")
lines.append("")
lines.append("**Previous result (Stirling approx):** Pearson r = -0.035")
lines.append("")
lines.append("## Per-Zero Table")
lines.append("")
lines.append("| k | γ_k | |ζ'(ρ_k)| | |c_k|² | Observed Peak | Pred/Obs Ratio |")
lines.append("|---:|---:|---:|---:|---:|---:|")
for k in range(20):
    ratio = ck_sq_arr[k] / observed_peaks[k] if observed_peaks[k] > 0 else 0
    lines.append(f"| {k+1} | {gamma_k[k]:.4f} | {zprime_abs_vals[k]:.12f} | {ck_sq_arr[k]:.6e} | {observed_peaks[k]:.2f} | {ratio:.6e} |")

lines.append("")
lines.append("## Interpretation")
lines.append("")
lines.append("The exact |ζ'(ρ_k)| values replace the Stirling approximation that gave")
lines.append("r = -0.035. The predicted amplitudes |c_k|² = 1/|ρ_k·ζ'(ρ_k)|² should track")
lines.append("the observed spectral peaks F_comp(γ_k) = γ²|Σ M(p)/p · e^{-iγ log p}|².")
lines.append("")
lines.append("Key observations:")
lines.append("- Both |c_k|² and observed peaks decrease with k (larger γ_k), but at different rates")
lines.append("- The log-space correlation removes the dominant 1/γ² scaling trend")
lines.append("- Consecutive ratios test whether zero-to-zero fluctuations match")
lines.append("")

with open(outpath, 'w') as f:
    f.write('\n'.join(lines))

print(f"\nResults saved to {outpath}")
print("Done!")
