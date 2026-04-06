#!/usr/bin/env python3
"""
Simple Zeros Test at N=10,000,000 (10M)
Compensated Mertens Spectroscope with Lorentzian vs Squared-Lorentzian fitting.

OPTIMIZATIONS for 10M:
- Local windows only: compute spectrum only around each zero (±0.5, 64 pts each)
  instead of full [5,85] at 25K pts. This reduces gamma evaluations from 25K to ~1300.
- Pre-compute log_p and weights once, reuse across zeros and MC shuffles.
- MC null: 50 shuffles, each re-computes only the local windows.

Linear sieve for Mobius.
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import kurtosis as sp_kurtosis
import time

# ── 1. Linear sieve for Mobius function up to N ──────────────────────────

def linear_sieve_mobius(N):
    """Linear sieve: O(N) time and memory. Returns mu[0..N]."""
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    primes = []
    is_composite = np.zeros(N + 1, dtype=np.bool_)

    for i in range(2, N + 1):
        if not is_composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N:
                break
            is_composite[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]

    return mu, np.array(primes, dtype=np.int64)


def mertens_at_primes(mu, primes):
    cumsum = np.cumsum(mu.astype(np.int64))
    return cumsum[primes]


# ── 2. Compute spectrum at specific gamma values ────────────────────────

def compute_spectrum_at_gammas(log_p, weights, gammas, batch_size=2000):
    """
    S(gamma) = sum_p w_p * exp(-i*gamma*log_p)
    where w_p = M(p)/p.

    Batched over primes. For small n_gamma (order ~1000), use large batches.
    Memory per batch: batch_size * n_gamma * 16 bytes.
    2000 * 1280 * 16 = 41MB per batch -- fine.
    """
    n_gamma = len(gammas)
    n_primes = len(log_p)
    S = np.zeros(n_gamma, dtype=np.complex128)

    for b in range(0, n_primes, batch_size):
        e = min(b + batch_size, n_primes)
        lp = log_p[b:e]     # (batch,)
        w = weights[b:e]     # (batch,)
        phase = np.outer(lp, gammas)
        S += (w[:, None] * np.exp(-1j * phase)).sum(axis=0)

    return S


# ── 3. Build gamma grids around zeros ───────────────────────────────────

def build_local_grids(zeros_list, half_window=0.5, n_pts=64):
    """Build dense gamma grids around each zero. Returns list of arrays."""
    grids = []
    for g0 in zeros_list:
        grids.append(np.linspace(g0 - half_window, g0 + half_window, n_pts))
    return grids


# ── 4. Also compute a coarse full spectrum for overview ──────────────────

def compute_full_spectrum(log_p, weights, gamma_lo, gamma_hi, n_pts,
                          batch_size=1000, report_every=100000):
    """Coarse full spectrum for overview plot context."""
    gammas = np.linspace(gamma_lo, gamma_hi, n_pts)
    n_primes = len(log_p)
    S = np.zeros(n_pts, dtype=np.complex128)

    for b in range(0, n_primes, batch_size):
        e = min(b + batch_size, n_primes)
        lp = log_p[b:e]
        w = weights[b:e]
        phase = np.outer(lp, gammas)
        S += (w[:, None] * np.exp(-1j * phase)).sum(axis=0)
        if e % report_every < batch_size:
            print(f"    Full spectrum: {e:,}/{n_primes:,}", flush=True)

    return gammas, S


# ── 5. Fitting functions ────────────────────────────────────────────────

def lorentzian(g, A, g0, w, B):
    return A / ((g - g0)**2 + w**2) + B

def sq_lorentzian(g, A, g0, w, B):
    return A / ((g - g0)**2 + w**2)**2 + B

def fit_peak_on_grid(g, f, gamma_k):
    """Fit Lorentzian and squared-Lorentzian on a pre-built local grid."""
    if len(g) < 8:
        return None

    peak_idx = np.argmax(f)
    A_init = f[peak_idx] * 0.01
    g0_init = g[peak_idx]
    w_init = 0.1
    B_init = np.median(f)

    results = {}
    for name, func, p0_A in [
        ("lorentzian", lorentzian, A_init),
        ("sq_lorentzian", sq_lorentzian, A_init * 0.001),
    ]:
        try:
            popt, _ = curve_fit(
                func, g, f,
                p0=[p0_A, g0_init, w_init, B_init],
                maxfev=10000,
                bounds=([-np.inf, gamma_k - 0.5, 1e-6, -np.inf],
                        [np.inf, gamma_k + 0.5, 2.0, np.inf])
            )
            residuals = f - func(g, *popt)
            chi2 = np.sum(residuals**2)
            results[name] = {"popt": popt, "chi2": chi2}
        except Exception:
            results[name] = None

    try:
        kurt = float(sp_kurtosis(f, fisher=True))
    except Exception:
        kurt = np.nan

    return {"g": g, "f": f, "fits": results, "kurtosis": kurt}


# ── 6. Monte Carlo null ─────────────────────────────────────────────────

def monte_carlo_null(log_p, weights_orig, grids, zeros_list, M_at_p,
                     primes_float, n_shuffles=50):
    """
    Shuffle M(p), recompute weights, compute local spectra, fit, get ratios.
    """
    rng = np.random.default_rng(42)
    null_ratios = []

    # Stack all gamma grids into one array for single batch computation
    all_gammas = np.concatenate(grids)
    grid_sizes = [len(g) for g in grids]
    grid_splits = np.cumsum(grid_sizes)[:-1]

    for s in range(n_shuffles):
        t0 = time.time()
        M_shuffled = rng.permutation(M_at_p)
        w_shuf = M_shuffled.astype(np.float64) / primes_float

        # Compute spectrum at all local gammas in one shot
        S_all = compute_spectrum_at_gammas(log_p, w_shuf, all_gammas,
                                           batch_size=500)
        F_all = all_gammas**2 * np.abs(S_all)**2

        # Split back into per-zero arrays
        F_splits = np.split(F_all, grid_splits)

        ratios_this = []
        for i, gamma_k in enumerate(zeros_list):
            g = grids[i]
            f = F_splits[i]
            res = fit_peak_on_grid(g, f, gamma_k)
            if res and res["fits"].get("lorentzian") and \
               res["fits"].get("sq_lorentzian"):
                r = (res["fits"]["sq_lorentzian"]["chi2"] /
                     res["fits"]["lorentzian"]["chi2"])
                ratios_this.append(r)
            else:
                ratios_this.append(np.nan)
        null_ratios.append(ratios_this)
        dt = time.time() - t0
        print(f"  MC shuffle {s+1}/{n_shuffles} done ({dt:.1f}s)", flush=True)

    return np.array(null_ratios)


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    N = 10_000_000
    gamma_lo, gamma_hi = 5.0, 85.0
    n_local_pts = 64      # points per local window
    half_window = 0.5
    n_full_pts = 5000     # coarse full spectrum

    zeros_list = [
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
        67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    ]

    print(f"=== Simple Zeros Test at N={N:,} ===\n", flush=True)

    # Step 1: Sieve
    print("Step 1: Linear sieve for Mobius...", flush=True)
    t0 = time.time()
    mu, all_primes = linear_sieve_mobius(N)
    dt = time.time() - t0
    print(f"  Sieve done in {dt:.1f}s. {len(all_primes):,} primes found.",
          flush=True)

    # Step 2: Mertens at primes
    print("\nStep 2: Mertens function at primes...", flush=True)
    t0 = time.time()
    M_at_p = mertens_at_primes(mu, all_primes)
    dt = time.time() - t0
    print(f"  Done in {dt:.1f}s. M(p_max) = {M_at_p[-1]}", flush=True)
    del mu

    # Pre-compute
    primes_float = all_primes.astype(np.float64)
    log_p = np.log(primes_float)
    weights = M_at_p.astype(np.float64) / primes_float

    # Step 3a: Build local grids
    grids = build_local_grids(zeros_list, half_window, n_local_pts)
    all_local_gammas = np.concatenate(grids)
    total_local = len(all_local_gammas)
    print(f"\nStep 3: Computing spectrum at {total_local} local gamma points "
          f"(20 zeros x {n_local_pts} pts)...", flush=True)

    t0 = time.time()
    S_local = compute_spectrum_at_gammas(log_p, weights, all_local_gammas,
                                         batch_size=500)
    dt = time.time() - t0
    print(f"  Local spectrum done in {dt:.1f}s.", flush=True)

    F_local = all_local_gammas**2 * np.abs(S_local)**2

    # Split into per-zero arrays
    grid_sizes = [len(g) for g in grids]
    grid_splits = np.cumsum(grid_sizes)[:-1]
    F_splits = np.split(F_local, grid_splits)

    # Step 3b: Coarse full spectrum for context
    print(f"\nStep 3b: Coarse full spectrum ({n_full_pts} pts)...", flush=True)
    t0 = time.time()
    gammas_full, S_full = compute_full_spectrum(
        log_p, weights, gamma_lo, gamma_hi, n_full_pts,
        batch_size=500, report_every=100000)
    dt = time.time() - t0
    F_full = gammas_full**2 * np.abs(S_full)**2
    print(f"  Full spectrum done in {dt:.1f}s.", flush=True)

    # Step 4-5: Fit each zero
    print("\nStep 4-5: Fitting peaks at 20 known zeros...\n", flush=True)
    results_table = []

    for k, gamma_k in enumerate(zeros_list):
        g = grids[k]
        f = F_splits[k]
        res = fit_peak_on_grid(g, f, gamma_k)

        if res is None:
            results_table.append({
                "k": k + 1, "gamma": gamma_k,
                "chi2_lor": np.nan, "chi2_sq": np.nan,
                "ratio": np.nan, "kurtosis": np.nan, "preferred": "N/A"
            })
            continue

        fits = res["fits"]
        chi2_lor = fits["lorentzian"]["chi2"] if fits.get("lorentzian") else np.nan
        chi2_sq = fits["sq_lorentzian"]["chi2"] if fits.get("sq_lorentzian") else np.nan

        if not np.isnan(chi2_lor) and not np.isnan(chi2_sq) and chi2_lor > 0:
            ratio = chi2_sq / chi2_lor
            preferred = "Simple" if ratio > 1.0 else "Double?"
        else:
            ratio = np.nan
            preferred = "N/A"

        results_table.append({
            "k": k + 1, "gamma": gamma_k,
            "chi2_lor": chi2_lor, "chi2_sq": chi2_sq,
            "ratio": ratio, "kurtosis": res["kurtosis"],
            "preferred": preferred,
        })
        print(f"  Zero {k+1:2d}: gamma={gamma_k:8.4f}  "
              f"chi2(L)={chi2_lor:.3e}  chi2(SL)={chi2_sq:.3e}  "
              f"ratio={ratio:.4f}  kurt={res['kurtosis']:.3f}  "
              f"{preferred}", flush=True)

    n_simple = sum(1 for r in results_table if r["preferred"] == "Simple")
    n_double = sum(1 for r in results_table if r["preferred"] == "Double?")
    valid_ratios = [r["ratio"] for r in results_table if not np.isnan(r["ratio"])]
    avg_ratio = np.mean(valid_ratios) if valid_ratios else np.nan
    valid_kurt = [r["kurtosis"] for r in results_table if not np.isnan(r["kurtosis"])]
    avg_kurt = np.mean(valid_kurt) if valid_kurt else np.nan

    print(f"\n  Summary: {n_simple}/20 Simple, {n_double}/20 Double?")
    print(f"  Average chi2 ratio: {avg_ratio:.4f}")
    print(f"  Average kurtosis: {avg_kurt:.4f}")

    # Step 6: Monte Carlo null
    print(f"\nStep 6: Monte Carlo null (50 shuffles)...", flush=True)
    t0 = time.time()
    null_ratios = monte_carlo_null(
        log_p, weights, grids, zeros_list, M_at_p, primes_float,
        n_shuffles=50)
    dt = time.time() - t0
    print(f"  MC done in {dt:.1f}s.", flush=True)

    # Compute p-values for each zero
    print("\nStep 6 results: p-values per zero", flush=True)
    pvalues = []
    for i, gamma_k in enumerate(zeros_list):
        real_ratio = results_table[i]["ratio"]
        if np.isnan(real_ratio):
            pvalues.append(np.nan)
            continue
        null_col = null_ratios[:, i]
        null_valid = null_col[~np.isnan(null_col)]
        if len(null_valid) == 0:
            pvalues.append(np.nan)
            continue
        pval = np.mean(null_valid >= real_ratio)
        pvalues.append(pval)
        print(f"  Zero {i+1:2d} (gamma={gamma_k:8.4f}): "
              f"ratio={real_ratio:.4f}, "
              f"null mean={np.mean(null_valid):.4f} +/- {np.std(null_valid):.4f}, "
              f"p={pval:.3f}", flush=True)

    # Global test
    real_avg = np.nanmean([r["ratio"] for r in results_table])
    null_avg_per_shuffle = np.nanmean(null_ratios, axis=1)
    global_pval = np.mean(null_avg_per_shuffle >= real_avg)
    print(f"\n  Global: real avg ratio = {real_avg:.4f}")
    print(f"  Null avg ratio: mean={np.mean(null_avg_per_shuffle):.4f} "
          f"+/- {np.std(null_avg_per_shuffle):.4f}")
    print(f"  Global p-value = {global_pval:.4f}")

    # ── 7. Write report ──────────────────────────────────────────────────
    report_path = "/Users/saar/Desktop/Farey-Local/experiments/SIMPLE_ZEROS_10M.md"
    improved = n_simple > 11
    improved_str = "stronger" if improved else "comparable"

    with open(report_path, "w") as f:
        f.write("# Simple Zeros Test: N=10,000,000\n\n")
        f.write(f"**Date:** 2026-04-06  \n")
        f.write(f"**Mobius sieve limit:** {N:,}  \n")
        f.write(f"**Primes:** {len(all_primes):,}  \n")
        f.write(f"**Local spectral points:** {n_local_pts} per zero "
                f"(window +/-{half_window})  \n")
        f.write(f"**Full spectrum:** {n_full_pts} pts on "
                f"[{gamma_lo}, {gamma_hi}]  \n")
        f.write(f"**Monte Carlo shuffles:** 50\n\n")

        f.write("## Method\n\n")
        f.write("Same as SIMPLE_ZEROS_TEST.md (N=1M) but with 10x more primes.\n")
        f.write("Linear sieve for Mobius, vectorized spectral computation.\n")
        f.write("Optimization: compute dense local spectra around each zero\n")
        f.write(f"({n_local_pts} pts in +/-{half_window} window) instead of "
                f"full 25K-point sweep.\n")
        f.write("Lorentzian vs squared-Lorentzian fitting with chi-squared "
                "comparison.\n")
        f.write("Added: 50-shuffle Monte Carlo null hypothesis test.\n\n")

        f.write("## Results: Per-Zero Analysis\n\n")
        f.write("| k | gamma_k | chi2(Lor) | chi2(SqLor) | Ratio | "
                "Kurtosis | Preferred | MC p-val |\n")
        f.write("|---|---------|-----------|-------------|-------|"
                "----------|-----------|----------|\n")
        for i, r in enumerate(results_table):
            pv = pvalues[i]
            pv_str = f"{pv:.3f}" if not np.isnan(pv) else "N/A"
            f.write(f"| {r['k']} | {r['gamma']:.6f} | "
                    f"{r['chi2_lor']:.3e} | {r['chi2_sq']:.3e} | "
                    f"{r['ratio']:.3f} | {r['kurtosis']:.3f} | "
                    f"{r['preferred']} | {pv_str} |\n")

        f.write(f"\n## Summary Statistics\n\n")
        f.write(f"- **Zeros where Lorentzian preferred (Simple):** "
                f"{n_simple}/20\n")
        f.write(f"- **Zeros where Sq-Lorentzian preferred (Double?):** "
                f"{n_double}/20\n")
        f.write(f"- **Average chi2 ratio (sq/simple):** {avg_ratio:.4f}\n")
        f.write(f"- **Average peak kurtosis:** {avg_kurt:.4f}\n\n")

        f.write("## Comparison with N=1M\n\n")
        f.write("| Metric | N=1M | N=10M |\n")
        f.write("|--------|------|-------|\n")
        f.write(f"| Primes | 78,498 | {len(all_primes):,} |\n")
        f.write(f"| Simple preferred | 11/20 | {n_simple}/20 |\n")
        f.write(f"| Avg chi2 ratio | 1.037 | {avg_ratio:.4f} |\n")
        f.write(f"| Avg kurtosis | 0.997 | {avg_kurt:.4f} |\n\n")

        f.write("## Monte Carlo Null Hypothesis Test\n\n")
        f.write("Under the null (shuffled M(p)), the spectral peaks have no "
                "special relationship\nto zeta zeros. We compare the "
                "chi-squared ratio distribution:\n\n")
        f.write(f"- **Real average ratio:** {real_avg:.4f}\n")
        f.write(f"- **Null average ratio:** "
                f"{np.mean(null_avg_per_shuffle):.4f} +/- "
                f"{np.std(null_avg_per_shuffle):.4f}\n")
        f.write(f"- **Global p-value:** {global_pval:.4f}\n\n")

        if global_pval < 0.05:
            f.write("The real data shows **statistically significant** "
                    "preference for Lorentzian peaks\n"
                    "(simple zeros) compared to the shuffled null "
                    "(p < 0.05).\n\n")
        else:
            f.write("The real data does NOT show statistically significant "
                    "preference for Lorentzian peaks\n"
                    "compared to the shuffled null at the 0.05 level.\n\n")

        f.write("## Conclusion\n\n")
        if improved:
            f.write(f"**10M IMPROVES discrimination:** {n_simple}/20 zeros "
                    f"prefer Lorentzian (vs 11/20 at 1M).\n")
        else:
            f.write(f"**10M does NOT clearly improve discrimination:** "
                    f"{n_simple}/20 zeros prefer Lorentzian "
                    f"(vs 11/20 at 1M).\n")
        f.write(f"Average chi2 ratio moved from 1.037 to {avg_ratio:.4f}.\n")
        f.write(f"Monte Carlo global p-value = {global_pval:.4f}.\n\n")
        f.write(f"The compensated Mertens spectroscope at N=10^7 provides "
                f"{improved_str} evidence\n"
                f"for the Simple Zeros Hypothesis compared to N=10^6.\n")

    print(f"\nReport written to {report_path}")
    print("Done.")


if __name__ == "__main__":
    main()
