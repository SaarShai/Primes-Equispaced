#!/usr/bin/env python3
"""
Chowla conjecture verification: Is there REAL structure in the pre-whitened
mu(n) spectroscope residual, or is it an artifact?

Author: Saar Shai (AI-assisted)
"""

import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.stats import chi2 as chi2_dist
import time, sys

P = lambda *a, **k: print(*a, **k, flush=True)

# ─── Parameters ───
N = 200_000
GAMMA_LO, GAMMA_HI = 5.0, 80.0
N_GAMMA = 10_000       # enough resolution (75/10000 = 0.0075 spacing)
N_NULL = 30            # null shuffles
N_GAMMA_NULL = 5_000   # coarser grid for null (speed)

# Known zeta zeros (imaginary parts)
KNOWN_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
]

gamma_grid = np.linspace(GAMMA_LO, GAMMA_HI, N_GAMMA)
gamma_grid_null = np.linspace(GAMMA_LO, GAMMA_HI, N_GAMMA_NULL)

# ─── Step 1: Mobius sieve ───
P("Step 1: Mobius sieve up to N =", N)
t0 = time.time()
mu = np.zeros(N + 1, dtype=np.int8)
mu[1] = 1
# smallest prime factor sieve
spf = np.zeros(N + 1, dtype=np.int32)
for i in range(2, N + 1):
    if spf[i] == 0:  # i is prime
        for j in range(i, N + 1, i):
            if spf[j] == 0:
                spf[j] = i

for n in range(2, N + 1):
    remaining = n
    sign = 1
    square_free = True
    while remaining > 1:
        p = spf[remaining]
        count = 0
        while remaining % p == 0:
            remaining //= p
            count += 1
        if count >= 2:
            square_free = False
            break
        sign *= -1
    mu[n] = sign if square_free else 0

P(f"  Sieve done in {time.time()-t0:.1f}s")
P(f"  mu(1)={mu[1]}, mu(2)={mu[2]}, mu(3)={mu[3]}, mu(4)={mu[4]}, mu(5)={mu[5]}, mu(6)={mu[6]}")
P(f"  Nonzero mu count: {np.count_nonzero(mu[1:])} out of {N}")

# ─── Step 2: Spectroscope F(gamma) over ALL integers ───
P("\nStep 2: Computing spectroscope F(gamma) = |sum mu(n)/n * exp(-i*gamma*log(n))|^2")
t0 = time.time()

# Precompute: only need n where mu(n) != 0
nz_idx = np.where(mu[1:] != 0)[0] + 1  # 1-based indices
mu_nz = mu[nz_idx].astype(np.float64)
log_nz = np.log(nz_idx.astype(np.float64))
inv_nz = 1.0 / nz_idx.astype(np.float64)
weights = mu_nz * inv_nz  # mu(n)/n

P(f"  {len(nz_idx)} nonzero mu values")

def compute_spectroscope(gamma_pts, w, log_n, chunk=500):
    """Compute |sum w * exp(-i*gamma*log_n)|^2 for each gamma."""
    Ng = len(gamma_pts)
    F = np.zeros(Ng)
    for i in range(0, Ng, chunk):
        end = min(i + chunk, Ng)
        g = gamma_pts[i:end, None]  # (chunk, 1)
        phase = g * log_n[None, :]  # (chunk, len_n)
        S = np.sum(w[None, :] * np.exp(-1j * phase), axis=1)
        F[i:end] = np.abs(S) ** 2
    return F

F_all = compute_spectroscope(gamma_grid, weights, log_nz, chunk=500)

P(f"  Spectroscope done in {time.time()-t0:.1f}s")
P(f"  F range: [{F_all.min():.6f}, {F_all.max():.6f}], mean={F_all.mean():.6f}")

# ─── Step 3: Find peaks, match to known zeros ───
P("\nStep 3: Peak detection and matching to known zeta zeros")
peaks_idx, props = find_peaks(F_all, height=F_all.mean() + 3 * F_all.std(), distance=10)
peak_gammas = gamma_grid[peaks_idx]
peak_heights = F_all[peaks_idx]

P(f"  Found {len(peaks_idx)} significant peaks (z > 3)")
P(f"  {'Peak gamma':>12s} {'Height':>10s} {'Nearest zero':>14s} {'Delta':>8s}")
for pg, ph in sorted(zip(peak_gammas, peak_heights), key=lambda x: -x[1])[:25]:
    dists = np.abs(np.array(KNOWN_ZEROS) - pg)
    nearest = KNOWN_ZEROS[np.argmin(dists)]
    delta = pg - nearest
    P(f"  {pg:12.4f} {ph:10.4f} {nearest:14.6f} {delta:+8.4f}")

# ─── Step 4: Pre-whiten by fitting Lorentzians at each known zero ───
P("\nStep 4: Pre-whitening — fitting Lorentzian at each known zero")

def lorentzian(gamma, A, gamma0, w):
    """Lorentzian: A * w^2 / ((gamma - gamma0)^2 + w^2)"""
    return A * w**2 / ((gamma - gamma0)**2 + w**2)

def fit_lorentzians(gamma_pts, F_data, zeros, window=3.0, max_width=5.0):
    """Fit Lorentzians at each zero, return total model on gamma_pts."""
    model = np.zeros(len(gamma_pts))
    results = []
    for gz in zeros:
        if gz < gamma_pts[0] - 5 or gz > gamma_pts[-1] + 5:
            continue
        mask = np.abs(gamma_pts - gz) < window
        if mask.sum() < 10:
            continue
        try:
            idx_center = np.argmin(np.abs(gamma_pts - gz))
            A0 = F_data[idx_center] - np.median(F_data)
            if A0 < 0:
                A0 = 0.01
            popt, _ = curve_fit(lorentzian, gamma_pts[mask], F_data[mask],
                                p0=[A0, gz, 0.5],
                                bounds=([0, gz - 2, 0.01], [A0 * 10, gz + 2, max_width]),
                                maxfev=5000)
            model += lorentzian(gamma_pts, *popt)
            results.append((gz, popt))
        except Exception as e:
            results.append((gz, None))
    return model, results

model_total, fit_results = fit_lorentzians(gamma_grid, F_all, KNOWN_ZEROS)

for gz, popt in fit_results:
    if popt is not None:
        P(f"  Zero {gz:.4f}: A={popt[0]:.4f}, center={popt[1]:.4f}, width={popt[2]:.4f}")
    else:
        P(f"  Zero {gz:.4f}: fit FAILED")

residual = F_all - model_total

P(f"\n  Model subtracted. Residual range: [{residual.min():.6f}, {residual.max():.6f}]")
P(f"  Residual mean={residual.mean():.6f}, std={residual.std():.6f}")

# ─── Step 5: Statistical tests on residual ───
P("\nStep 5: Statistical tests on residual")

def binned_chi2(resid, gamma_pts, n_bins=100):
    """Compute binned chi-squared statistic for residual flatness."""
    bin_edges = np.linspace(gamma_pts[0], gamma_pts[-1], n_bins + 1)
    bin_size = len(gamma_pts) // n_bins
    bin_means = []
    for i in range(n_bins):
        mask = (gamma_pts >= bin_edges[i]) & (gamma_pts < bin_edges[i + 1])
        if mask.sum() > 0:
            bin_means.append(resid[mask].mean())
        else:
            bin_means.append(0)
    bin_means = np.array(bin_means)
    overall_mean = resid.mean()
    overall_var = resid.var()
    if overall_var == 0 or bin_size == 0:
        return 0.0, 1.0, n_bins - 1
    expected_var = overall_var / bin_size
    chi2_val = np.sum((bin_means - overall_mean)**2) / expected_var
    dof = n_bins - 1
    p_val = 1.0 - chi2_dist.cdf(chi2_val, dof)
    return chi2_val, p_val, dof

chi2_val, chi2_p, chi2_dof = binned_chi2(residual, gamma_grid)

P(f"  5A: Binned chi-squared test")
P(f"      chi2 = {chi2_val:.2f}, dof = {chi2_dof}, p-value = {chi2_p:.6e}")
if chi2_p < 0.001:
    P(f"      --> STRUCTURE DETECTED (p < 0.001)")
elif chi2_p < 0.05:
    P(f"      --> Marginal structure (p < 0.05)")
else:
    P(f"      --> Consistent with flat (p = {chi2_p:.4f})")

# 5B: Peaks in residual
res_mean = residual.mean()
res_std = residual.std()
z_scores = (residual - res_mean) / res_std
n_high_z = (z_scores > 3.0).sum()
expected_high_z = N_GAMMA * (1 - 0.9987)
P(f"\n  5B: Residual peaks with z > 3")
P(f"      Found {n_high_z} points with z > 3 (expected ~{expected_high_z:.1f} if Gaussian)")

res_peaks_idx, _ = find_peaks(residual, height=res_mean + 3 * res_std, distance=10)
res_peak_gammas = gamma_grid[res_peaks_idx]
P(f"      {len(res_peaks_idx)} distinct peaks in residual with z > 3")
if len(res_peaks_idx) > 0:
    for rg in res_peak_gammas[:15]:
        z_at = (residual[np.argmin(np.abs(gamma_grid - rg))] - res_mean) / res_std
        dists = np.abs(np.array(KNOWN_ZEROS) - rg)
        nearest_zero_dist = dists.min()
        nearest_zero = KNOWN_ZEROS[np.argmin(dists)]
        flag = " <-- NEAR ZERO (tail artifact?)" if nearest_zero_dist < 2.0 else ""
        P(f"      gamma={rg:.4f}, z={z_at:.2f}, nearest zero at {nearest_zero:.4f} (dist={nearest_zero_dist:.2f}){flag}")

# ─── 5C: Null distribution (CRITICAL) ───
P(f"\n  5C: Null distribution ({N_NULL} shuffles, coarse grid {N_GAMMA_NULL} pts)")
t0 = time.time()

# Also compute real spectroscope on coarse grid for fair comparison
F_all_coarse = compute_spectroscope(gamma_grid_null, weights, log_nz, chunk=500)
model_coarse, _ = fit_lorentzians(gamma_grid_null, F_all_coarse, KNOWN_ZEROS)
residual_coarse = F_all_coarse - model_coarse
chi2_real_coarse, _, _ = binned_chi2(residual_coarse, gamma_grid_null, n_bins=50)

null_chi2_vals = []
null_peak_counts = []

for trial in range(N_NULL):
    # Shuffle mu values (preserving which n are square-free, just randomizing signs)
    mu_shuf = mu_nz.copy()
    np.random.shuffle(mu_shuf)
    weights_shuf = mu_shuf * inv_nz

    F_null = compute_spectroscope(gamma_grid_null, weights_shuf, log_nz, chunk=500)

    # Pre-whiten null: fit its OWN Lorentzians (more fair than using real model)
    # Actually: null should NOT have peaks at zeta zeros. So subtracting real model
    # is the right null test: does the residual have MORE structure than random?
    # But also test: fit null's own peaks
    null_residual = F_null - model_coarse

    c2, _, _ = binned_chi2(null_residual, gamma_grid_null, n_bins=50)
    null_chi2_vals.append(c2)

    null_mean = null_residual.mean()
    null_std = null_residual.std()
    if null_std > 0:
        null_pk, _ = find_peaks(null_residual, height=null_mean + 3 * null_std, distance=5)
        null_peak_counts.append(len(null_pk))
    else:
        null_peak_counts.append(0)

    if (trial + 1) % 5 == 0:
        P(f"    Null trial {trial+1}/{N_NULL} done ({time.time()-t0:.0f}s)")

null_chi2_vals = np.array(null_chi2_vals)
null_peak_counts = np.array(null_peak_counts)

P(f"\n  Null chi2 distribution: mean={null_chi2_vals.mean():.2f}, std={null_chi2_vals.std():.2f}")
P(f"  Null chi2 range: [{null_chi2_vals.min():.2f}, {null_chi2_vals.max():.2f}]")
P(f"  Real chi2 (coarse): {chi2_real_coarse:.2f}")
rank = np.sum(null_chi2_vals < chi2_real_coarse)
P(f"  Rank of real chi2 among null: {rank}/{N_NULL} (percentile: {100*rank/N_NULL:.1f}%)")

if rank >= N_NULL:
    P(f"  --> Real chi2 EXCEEDS all null values: possible real structure")
elif rank >= 0.95 * N_NULL:
    P(f"  --> Real chi2 in top 5%: marginal")
else:
    P(f"  --> Real chi2 WITHIN null distribution: NO evidence of structure beyond artifact")

P(f"\n  Null peak counts: mean={null_peak_counts.mean():.1f}, std={null_peak_counts.std():.1f}")
P(f"  Real peak count (coarse): {len(find_peaks(residual_coarse, height=residual_coarse.mean() + 3*residual_coarse.std(), distance=5)[0])}")

# ─── Step 6: Check pre-whitening quality ───
P("\nStep 6: Pre-whitening quality check")

P("  Residual near each known zero (checking for tail artifacts):")
for gz in KNOWN_ZEROS:
    if gz < GAMMA_LO or gz > GAMMA_HI:
        continue
    mask_near = np.abs(gamma_grid - gz) < 1.5
    mask_far = (np.abs(gamma_grid - gz) > 3.0) & (np.abs(gamma_grid - gz) < 8.0)
    if mask_near.sum() == 0 or mask_far.sum() == 0:
        continue
    near_resid = residual[mask_near].mean()
    far_resid = residual[mask_far].mean()
    ratio = near_resid / far_resid if abs(far_resid) > 1e-10 else float('inf')
    flag = " <-- TAIL LEAK" if abs(near_resid) > 3 * abs(far_resid) and abs(near_resid) > res_std else ""
    P(f"  Zero {gz:7.3f}: near_mean={near_resid:+.6f}, far_mean={far_resid:+.6f}, ratio={ratio:+.2f}{flag}")

# Iterative re-fit with wider window
P("\n  Iterative re-fit (wider window=4.0, max_width=8.0):")
model_v2, _ = fit_lorentzians(gamma_grid, F_all, KNOWN_ZEROS, window=4.0, max_width=8.0)
residual_v2 = F_all - model_v2
v2_chi2, v2_p, _ = binned_chi2(residual_v2, gamma_grid)
P(f"  V2 (wider fit): chi2={v2_chi2:.2f}, p={v2_p:.6e}")
P(f"  V1 (original):  chi2={chi2_val:.2f}, p={chi2_p:.6e}")
if v2_chi2 < chi2_val * 0.5:
    P(f"  --> Wider fit HALVED chi2: original 'structure' was largely tail artifacts")
elif v2_chi2 < chi2_val * 0.8:
    P(f"  --> Wider fit reduced chi2 significantly: partial tail artifact")
else:
    P(f"  --> Wider fit did NOT reduce chi2 much: structure may be real")

# ─── Step 7: Primes-only vs all-n comparison ───
P("\nStep 7: Primes-only spectroscope vs all-n")
t0 = time.time()

primes = np.array([p for p in range(2, N + 1) if spf[p] == p])
P(f"  {len(primes)} primes up to {N}")

log_primes = np.log(primes.astype(np.float64))
inv_primes = 1.0 / primes.astype(np.float64)
weights_primes = -inv_primes  # mu(p) = -1

F_primes = compute_spectroscope(gamma_grid, weights_primes, log_primes, chunk=500)
P(f"  Primes spectroscope done in {time.time()-t0:.1f}s")

model_primes, _ = fit_lorentzians(gamma_grid, F_primes, KNOWN_ZEROS, window=4.0, max_width=8.0)
residual_primes = F_primes - model_primes

p_chi2, p_p_val, _ = binned_chi2(residual_primes, gamma_grid)

P(f"\n  All-n residual:    chi2={chi2_val:.2f}, p={chi2_p:.6e}")
P(f"  Primes residual:   chi2={p_chi2:.2f}, p={p_p_val:.6e}")
corr = np.corrcoef(residual[::5], residual_primes[::5])[0,1]
P(f"  Correlation between all-n and primes residuals: {corr:.4f}")

if p_chi2 > chi2_val * 1.5:
    P(f"  --> Primes have MORE structure: composites are smoothing, not creating")
elif p_chi2 < chi2_val * 0.5:
    P(f"  --> Primes have LESS structure: composites contribute the 'structure'")
else:
    P(f"  --> Similar structure in both: not composite-driven")

# ─── VERDICT ───
P("\n" + "=" * 70)
P("VERDICT")
P("=" * 70)

evidence_for_artifact = []
evidence_for_real = []

# Null test
if rank < 0.95 * N_NULL:
    evidence_for_artifact.append(f"Real chi2 ({chi2_real_coarse:.1f}) within null distribution (rank {rank}/{N_NULL})")
else:
    evidence_for_real.append(f"Real chi2 ({chi2_real_coarse:.1f}) exceeds {100*rank/N_NULL:.0f}% of null values")

# Tail artifacts
if v2_chi2 < chi2_val * 0.7:
    evidence_for_artifact.append(f"Wider Lorentzian fit reduced chi2 from {chi2_val:.1f} to {v2_chi2:.1f} (tail artifacts)")
else:
    evidence_for_real.append(f"Wider fit did not eliminate structure (chi2: {chi2_val:.1f} -> {v2_chi2:.1f})")

# Residual peaks near zeros
near_zero_peaks = 0
total_res_peaks = len(res_peaks_idx)
if total_res_peaks > 0:
    for rg in res_peak_gammas:
        dists = np.abs(np.array(KNOWN_ZEROS) - rg)
        if dists.min() < 2.0:
            near_zero_peaks += 1
    if near_zero_peaks > total_res_peaks * 0.5:
        evidence_for_artifact.append(f"{near_zero_peaks}/{total_res_peaks} residual peaks near known zeros (tail leak)")
    else:
        evidence_for_real.append(f"Only {near_zero_peaks}/{total_res_peaks} residual peaks near zeros")

# Chi2 p-value itself
if chi2_p > 0.01:
    evidence_for_artifact.append(f"Chi2 p-value = {chi2_p:.4f} (not highly significant)")
elif chi2_p < 1e-10:
    evidence_for_real.append(f"Chi2 p-value = {chi2_p:.2e} (highly significant)")

P("\nEvidence FOR artifact (not real):")
for e in evidence_for_artifact:
    P(f"  - {e}")

P("\nEvidence FOR real structure:")
for e in evidence_for_real:
    P(f"  + {e}")

if len(evidence_for_artifact) > len(evidence_for_real):
    P(f"\nCONCLUSION: The 'Chowla violation' is MOST LIKELY AN ARTIFACT")
    P("  Primary cause: imperfect Lorentzian pre-whitening leaving residual")
    P("  peak tails from known zeta zeros.")
elif len(evidence_for_real) > len(evidence_for_artifact):
    P(f"\nCONCLUSION: There MAY be real structure beyond zeta-zero peaks.")
    P("  But this needs: (1) better pre-whitening, (2) larger N, (3) more null trials.")
    P("  DO NOT claim Chowla violation without rigorous follow-up.")
else:
    P(f"\nCONCLUSION: INCONCLUSIVE. Evidence is balanced.")
    P("  The structure could be real or artifact. Need better methods.")

P("\nDone.")
