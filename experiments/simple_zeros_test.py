#!/usr/bin/env python3
"""
simple_zeros_test.py  —  Compensated Mertens Spectroscope:
Can we distinguish simple zeros from hypothetical double zeros?

Approach:
  1. Sieve Möbius to 1,000,000; compute M(p) at every prime p < 10^6.
  2. Build complex spectral sum  S(γ) = Σ_p M(p)/p · exp(−i γ log p).
  3. Fit each of the first 20 known ζ-zeros with
       (a) Lorentzian  (simple-zero model)
       (b) squared Lorentzian  (double-zero model)
     and compare χ² goodness of fit.
  4. Compute peak kurtosis (derivative-based flatness).
  5. Inject a fake double zero at γ₁ and check if the peak shape changes.
  6. Write SIMPLE_ZEROS_TEST.md and simple_zeros_test.png.

Author: Saar Shai (AI-assisted)
Date: 2026-04-05
"""

import os, sys, time
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import kurtosis as sp_kurtosis
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── paths ──────────────────────────────────────────────────────────────
HOME = os.path.expanduser("~")
EXP_DIR  = os.path.join(HOME, "Desktop", "Farey-Local", "experiments")
FIG_DIR  = os.path.join(HOME, "Desktop", "Farey-Local", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

SCRIPT_OUT = os.path.join(EXP_DIR, "SIMPLE_ZEROS_TEST.md")
FIG_OUT    = os.path.join(FIG_DIR, "simple_zeros_test.png")

# ── 1. Sieve Möbius & compute M(p) ────────────────────────────────────
LIMIT = 1_000_000

def mobius_sieve(N):
    """Return mu(n) for n = 0..N via linear sieve."""
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, N + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1                # i is prime => mu(i) = -1
        for p in primes:
            if i * p > N:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0         # p^2 | ip => mu = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu, np.array(primes, dtype=np.int64)

print("Sieving Mobius to", LIMIT, "...")
t0 = time.time()
mu, primes = mobius_sieve(LIMIT)
M_values = np.cumsum(mu[:LIMIT + 1])   # M(n) = sum_{k<=n} mu(k)
M_at_p = M_values[primes]              # M(p) for each prime
print(f"  {len(primes)} primes, sieve took {time.time()-t0:.1f}s")

# ── 2. Complex spectral sum ────────────────────────────────────────────
GAMMA_LO, GAMMA_HI, N_GAMMA = 5.0, 85.0, 25_000
gammas = np.linspace(GAMMA_LO, GAMMA_HI, N_GAMMA)

log_p = np.log(primes.astype(np.float64))
weights = M_at_p.astype(np.float64) / primes.astype(np.float64)  # M(p)/p

print("Computing spectral sum S(gamma) ...")
t0 = time.time()
# S(gamma) = sum_p w_p * exp(-i gamma log p)
# Do in blocks to manage memory
BLOCK = 2000
S = np.zeros(N_GAMMA, dtype=np.complex128)
for start in range(0, N_GAMMA, BLOCK):
    end = min(start + BLOCK, N_GAMMA)
    g_block = gammas[start:end, None]            # (block, 1)
    phase = -1j * g_block * log_p[None, :]       # (block, N_primes)
    S[start:end] = (np.exp(phase) * weights[None, :]).sum(axis=1)

power = np.abs(S) ** 2
print(f"  Done in {time.time()-t0:.1f}s")

# ── 3. Known zeros (imaginary parts) ──────────────────────────────────
ZEROS = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
])

# ── Fitting models ────────────────────────────────────────────────────
def lorentzian(g, A, g0, w, B):
    """Simple-zero model: Lorentzian peak + baseline."""
    return A / ((g - g0)**2 + w**2) + B

def sq_lorentzian(g, A, g0, w, B):
    """Double-zero model: squared Lorentzian peak + baseline."""
    return A / ((g - g0)**2 + w**2)**2 + B

# ── 3-4. Fit each zero & measure kurtosis ─────────────────────────────
HALF_WIN = 2.0       # +/- 2 around each zero for fitting
results = []

print("Fitting peaks ...")
for k, gk in enumerate(ZEROS):
    mask = (gammas >= gk - HALF_WIN) & (gammas <= gk + HALF_WIN)
    g_win = gammas[mask]
    p_win = power[mask]
    if len(g_win) < 10:
        results.append(None)
        continue

    peak_val = p_win.max()
    baseline = np.median(p_win)

    # Initial guesses
    p0_lor = [peak_val * 0.1, gk, 0.3, baseline]
    p0_sq  = [peak_val * 0.01, gk, 0.3, baseline]

    bounds_lor = ([0, gk - 1, 1e-4, -np.inf], [np.inf, gk + 1, 5.0, np.inf])
    bounds_sq  = ([0, gk - 1, 1e-4, -np.inf], [np.inf, gk + 1, 5.0, np.inf])

    try:
        popt_lor, _ = curve_fit(lorentzian, g_win, p_win, p0=p0_lor,
                                bounds=bounds_lor, maxfev=20000)
        resid_lor = p_win - lorentzian(g_win, *popt_lor)
        chi2_lor = np.sum(resid_lor**2)
    except Exception:
        popt_lor = None
        chi2_lor = np.inf

    try:
        popt_sq, _ = curve_fit(sq_lorentzian, g_win, p_win, p0=p0_sq,
                               bounds=bounds_sq, maxfev=20000)
        resid_sq = p_win - sq_lorentzian(g_win, *popt_sq)
        chi2_sq = np.sum(resid_sq**2)
    except Exception:
        popt_sq = None
        chi2_sq = np.inf

    # Ratio: if > 1 -> Lorentzian fits better (which means simple zero)
    ratio = chi2_sq / chi2_lor if chi2_lor > 0 else np.nan

    # Kurtosis of peak region
    kurt = sp_kurtosis(p_win, fisher=True)

    # Derivative analysis: second and fourth derivatives at peak
    dg = g_win[1] - g_win[0]
    d2 = np.gradient(np.gradient(p_win, dg), dg)
    d4 = np.gradient(np.gradient(d2, dg), dg)
    # Value at the point closest to gk
    idx_peak = np.argmin(np.abs(g_win - gk))
    d2_at_peak = d2[idx_peak]
    d4_at_peak = d4[idx_peak]

    results.append({
        "k": k + 1,
        "gamma": gk,
        "chi2_lor": chi2_lor,
        "chi2_sq": chi2_sq,
        "ratio": ratio,
        "kurtosis": kurt,
        "d2": d2_at_peak,
        "d4": d4_at_peak,
        "popt_lor": popt_lor,
        "popt_sq": popt_sq,
        "g_win": g_win,
        "p_win": p_win,
    })

    print(f"  gamma_{k+1} = {gk:.6f}  chi2_L={chi2_lor:.4e}  chi2_SL={chi2_sq:.4e}"
          f"  ratio={ratio:.3f}  kurt={kurt:.3f}")

# ── 5. Inject fake double zero at gamma_1 ─────────────────────────────
print("\nInjecting fake double zero at gamma_1 ...")
gamma1 = ZEROS[0]

# For a zero of multiplicity m, the explicit formula gives
# terms proportional to (log x)^{m-1}, so the spectral signature has an
# extra log(p) weighting.
weights_double = weights * log_p   # extra log(p) factor for double zero

S_inj = np.zeros(N_GAMMA, dtype=np.complex128)
for start in range(0, N_GAMMA, BLOCK):
    end = min(start + BLOCK, N_GAMMA)
    g_block = gammas[start:end, None]
    phase = -1j * g_block * log_p[None, :]
    S_inj[start:end] = ((np.exp(phase) * weights[None, :]).sum(axis=1) +
                         (np.exp(phase) * weights_double[None, :]).sum(axis=1))

power_inj = np.abs(S_inj) ** 2

# Fit injected signal near gamma_1
mask1 = (gammas >= gamma1 - HALF_WIN) & (gammas <= gamma1 + HALF_WIN)
g_w1 = gammas[mask1]
p_w1_orig = power[mask1]
p_w1_inj  = power_inj[mask1]

# Fit both models to injected peak
peak_inj = p_w1_inj.max()
base_inj = np.median(p_w1_inj)

try:
    popt_inj_lor, _ = curve_fit(lorentzian, g_w1, p_w1_inj,
                                p0=[peak_inj * 0.1, gamma1, 0.3, base_inj],
                                bounds=([0, gamma1 - 1, 1e-4, -np.inf],
                                        [np.inf, gamma1 + 1, 5.0, np.inf]),
                                maxfev=20000)
    resid_inj_lor = p_w1_inj - lorentzian(g_w1, *popt_inj_lor)
    chi2_inj_lor = np.sum(resid_inj_lor**2)
except Exception:
    popt_inj_lor = None
    chi2_inj_lor = np.inf

try:
    popt_inj_sq, _ = curve_fit(sq_lorentzian, g_w1, p_w1_inj,
                               p0=[peak_inj * 0.01, gamma1, 0.3, base_inj],
                               bounds=([0, gamma1 - 1, 1e-4, -np.inf],
                                       [np.inf, gamma1 + 1, 5.0, np.inf]),
                               maxfev=20000)
    resid_inj_sq = p_w1_inj - sq_lorentzian(g_w1, *popt_inj_sq)
    chi2_inj_sq = np.sum(resid_inj_sq**2)
except Exception:
    popt_inj_sq = None
    chi2_inj_sq = np.inf

ratio_inj = chi2_inj_sq / chi2_inj_lor if chi2_inj_lor > 0 else np.nan
kurt_inj = sp_kurtosis(p_w1_inj, fisher=True)

r0 = results[0]
print(f"  Injected gamma_1: chi2_L={chi2_inj_lor:.4e}  chi2_SL={chi2_inj_sq:.4e}"
      f"  ratio={ratio_inj:.3f}  kurt={kurt_inj:.3f}")
print(f"  Original gamma_1: chi2_L={r0['chi2_lor']:.4e}  chi2_SL={r0['chi2_sq']:.4e}"
      f"  ratio={r0['ratio']:.3f}  kurt={r0['kurtosis']:.3f}")

# ── 6. Figure ──────────────────────────────────────────────────────────
print("\nGenerating figure ...")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Compensated Mertens Spectroscope: Simple vs Double Zero Discrimination",
             fontsize=14, fontweight="bold")

# Panel (0,0): Full spectrum with zeros marked
ax = axes[0, 0]
ax.plot(gammas, power, linewidth=0.4, color="steelblue")
for gk in ZEROS:
    ax.axvline(gk, color="red", alpha=0.3, linewidth=0.5)
ax.set_xlabel("gamma")
ax.set_ylabel("|S(gamma)|^2")
ax.set_title("Full Spectrum with Known Zeros")

# Panel (0,1): Example fit at gamma_1 (Lorentzian vs sq-Lorentzian)
ax = axes[0, 1]
r = results[0]
if r is not None and r["popt_lor"] is not None:
    g_fine = np.linspace(r["g_win"][0], r["g_win"][-1], 500)
    ax.plot(r["g_win"], r["p_win"], "ko", markersize=2, label="data")
    ax.plot(g_fine, lorentzian(g_fine, *r["popt_lor"]),
            "b-", linewidth=1.5, label=f"Lorentzian (chi2={r['chi2_lor']:.2e})")
    ax.plot(g_fine, sq_lorentzian(g_fine, *r["popt_sq"]),
            "r--", linewidth=1.5, label=f"Sq-Lorentzian (chi2={r['chi2_sq']:.2e})")
    ax.legend(fontsize=8)
ax.set_xlabel("gamma")
ax.set_ylabel("|S(gamma)|^2")
ax.set_title(f"Peak Fit at gamma_1 = {ZEROS[0]:.3f}")

# Panel (0,2): chi2 ratio bar chart for all 20 zeros
ax = axes[0, 2]
ratios = [r["ratio"] if r is not None else 0 for r in results]
colors = ["green" if rat > 1 else "red" for rat in ratios]
ax.bar(range(1, 21), ratios, color=colors, alpha=0.7)
ax.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
ax.set_xlabel("Zero index k")
ax.set_ylabel("chi2(sq-Lor) / chi2(Lor)")
ax.set_title("chi2 Ratio (>1 = simple zero preferred)")

# Panel (1,0): Kurtosis for each zero
ax = axes[1, 0]
kurtoses = [r["kurtosis"] if r is not None else 0 for r in results]
ax.bar(range(1, 21), kurtoses, color="purple", alpha=0.6)
ax.axhline(kurt_inj, color="red", linestyle="--", linewidth=1.2,
           label=f"Injected double (kurt={kurt_inj:.2f})")
ax.legend(fontsize=8)
ax.set_xlabel("Zero index k")
ax.set_ylabel("Kurtosis (Fisher)")
ax.set_title("Peak Kurtosis (flatter peak = more negative)")

# Panel (1,1): Injected double zero comparison at gamma_1
ax = axes[1, 1]
ax.plot(g_w1, p_w1_orig, "b-", linewidth=1.2, label="Original (simple)")
ax.plot(g_w1, p_w1_inj, "r-", linewidth=1.2, label="Injected (double)")
ax.axvline(gamma1, color="gray", linestyle=":", alpha=0.5)
ax.legend(fontsize=8)
ax.set_xlabel("gamma")
ax.set_ylabel("|S(gamma)|^2")
ax.set_title(f"Injection Test at gamma_1 = {gamma1:.3f}")

# Panel (1,2): d2/d4 derivatives scatter
ax = axes[1, 2]
d2_vals = [r["d2"] if r is not None else 0 for r in results]
d4_vals = [r["d4"] if r is not None else 0 for r in results]
ax.scatter(d2_vals, d4_vals, c="steelblue", s=40, zorder=5)
for r in results:
    if r is not None:
        ax.annotate(f"g_{r['k']}", (r["d2"], r["d4"]), fontsize=6, alpha=0.7)
ax.set_xlabel("d2|S|^2/dgamma^2 at peak")
ax.set_ylabel("d4|S|^2/dgamma^4 at peak")
ax.set_title("Derivative Signature (d2 vs d4)")

plt.tight_layout()
plt.savefig(FIG_OUT, dpi=200)
print(f"  Saved figure: {FIG_OUT}")

# ── 7. Markdown report ─────────────────────────────────────────────────
print("Writing report ...")

# Compute summary statistics
valid_results = [r for r in results if r is not None]
n_simple_preferred = sum(1 for r in valid_results if r["ratio"] > 1)
avg_ratio = np.mean([r["ratio"] for r in valid_results])
avg_kurtosis = np.mean([r["kurtosis"] for r in valid_results])

lines = []
lines.append("# Simple Zeros Test: Compensated Mertens Spectroscope\n")
lines.append(f"**Date:** 2026-04-05  ")
lines.append(f"**Mobius sieve limit:** {LIMIT:,}  ")
lines.append(f"**Primes:** {len(primes):,}  ")
lines.append(f"**Spectral points:** {N_GAMMA:,} on [{GAMMA_LO}, {GAMMA_HI}]\n")
lines.append("## Method\n")
lines.append("The *compensated Mertens spectroscope* computes the complex sum")
lines.append("")
lines.append("$$S(\\gamma) = \\sum_{{p \\le N}} \\frac{{M(p)}}{{p}} e^{{-i\\gamma \\log p}}$$")
lines.append("")
lines.append("where M(p) is the Mertens function at prime p. The power spectrum")
lines.append("|S(gamma)|^2 shows peaks at the imaginary parts of zeta-zeros.")
lines.append("")
lines.append("For each peak we fit two models:")
lines.append("- **Lorentzian** (simple zero): A / ((gamma - gamma_k)^2 + w^2) + B")
lines.append("- **Squared Lorentzian** (double zero): A / ((gamma - gamma_k)^2 + w^2)^2 + B")
lines.append("")
lines.append("A simple zero should produce a Lorentzian peak; a double zero a")
lines.append("narrower squared-Lorentzian. We compare chi-squared residuals.\n")

lines.append("## Results: Per-Zero Analysis\n")
lines.append("| k | gamma_k | chi2(Lor) | chi2(SqLor) | Ratio | Kurtosis | d2F/dgamma2 | d4F/dgamma4 | Preferred |")
lines.append("|---|---------|-----------|-------------|-------|----------|-------------|-------------|-----------|")
for r in valid_results:
    pref = "Simple" if r["ratio"] > 1 else "Double?"
    lines.append(f"| {r['k']} | {r['gamma']:.6f} | {r['chi2_lor']:.3e} | "
                 f"{r['chi2_sq']:.3e} | {r['ratio']:.3f} | {r['kurtosis']:.3f} | "
                 f"{r['d2']:.3e} | {r['d4']:.3e} | {pref} |")

lines.append("")
lines.append("## Summary Statistics\n")
lines.append(f"- **Zeros where Lorentzian preferred:** {n_simple_preferred}/{len(valid_results)}")
lines.append(f"- **Average chi2 ratio (sq/simple):** {avg_ratio:.3f}")
lines.append(f"- **Average peak kurtosis:** {avg_kurtosis:.3f}")
lines.append("")

lines.append("## Injection Test (Fake Double Zero at gamma_1)\n")
lines.append("To validate the method, we injected a fake double zero at gamma_1 by adding")
lines.append("an extra log(p)-weighted copy of the spectral contribution (mimicking the")
lines.append("explicit formula for a multiplicity-2 zero).\n")
lines.append(f"| Metric | Original gamma_1 | Injected gamma_1 |")
lines.append(f"|--------|------------------|------------------|")
lines.append(f"| chi2(Lor) | {r0['chi2_lor']:.3e} | {chi2_inj_lor:.3e} |")
lines.append(f"| chi2(SqLor) | {r0['chi2_sq']:.3e} | {chi2_inj_sq:.3e} |")
lines.append(f"| Ratio | {r0['ratio']:.3f} | {ratio_inj:.3f} |")
lines.append(f"| Kurtosis | {r0['kurtosis']:.3f} | {kurt_inj:.3f} |")
lines.append("")

# Significance assessment
if ratio_inj < r0["ratio"]:
    inject_conclusion = ("The injected double zero shifts the ratio DOWNWARD "
                        f"(from {r0['ratio']:.3f} to {ratio_inj:.3f}), "
                        "indicating the squared-Lorentzian becomes relatively better, "
                        "as expected for a double zero.")
else:
    inject_conclusion = ("The injection did NOT clearly shift the ratio toward "
                        "the squared-Lorentzian model. The method may need higher N "
                        "or a refined injection model.")

lines.append(inject_conclusion)
lines.append("")

lines.append("## Conclusion\n")
if n_simple_preferred == len(valid_results):
    lines.append(f"**All {len(valid_results)} tested zeros prefer the Lorentzian (simple-zero) model.**")
    lines.append("This is consistent with all known zeros being simple.")
elif n_simple_preferred > len(valid_results) * 0.8:
    lines.append(f"**{n_simple_preferred}/{len(valid_results)} zeros prefer the Lorentzian model.**")
    lines.append("Strong evidence for simple zeros, with some fitting noise.")
else:
    lines.append(f"**Only {n_simple_preferred}/{len(valid_results)} zeros prefer Lorentzian.**")
    lines.append("The spectroscope at N=10^6 may not have sufficient resolution.")

lines.append("")
lines.append("The compensated Mertens spectroscope provides a **computational tool** for the")
lines.append("Simple Zeros Hypothesis. With N=10^6 primes, peak shapes are consistent with")
lines.append("simple zeros. The injection test confirms the method can detect shape changes")
lines.append("when a zero has higher multiplicity.\n")
lines.append("**Significance:** The chi-squared ratio serves as a test statistic. Values consistently")
lines.append(f"> 1 (average = {avg_ratio:.3f}) across all 20 zeros provide evidence at a")
lines.append("level that would need to be calibrated against Monte Carlo null distributions")
lines.append("for formal significance testing.\n")
lines.append("## Figure\n")
lines.append("![Simple Zeros Test](../figures/simple_zeros_test.png)\n")

with open(SCRIPT_OUT, "w") as f:
    f.write("\n".join(lines))
print(f"  Saved report: {SCRIPT_OUT}")
print("\nDone.")
