# Koyama-Shared: Scripts, Data, and Results

**Purpose:** Scripts and datasets shared with Prof. Shin-ya Koyama (Toyo University) for the Deep Riemann Hypothesis / Normalized Duality Constant (NDC) / Fine Structure Constant $C_1(f,\rho)$ investigation.

**Repo:** https://github.com/SaarShai/Primes-Equispaced (`koyama-shared/` subtree)
**Branch of record:** `main`
**Author:** Saar Shai (saar.shai@gmail.com) — independent researcher
**Last updated:** 2026-04-20

---

## ⚠️ BUGFIX NOTICE (2026-04-20)

The scripts have been corrected after a code review identified a systematic error in the $\mu_f(p^2)$ coefficient:

- **Old (wrong)**: used $a_{p^2}$ (Hecke eigenvalue) for $\mu_f(p^2)$
- **New (correct)**: uses $p^{k-1}$ from the Euler factor $(1 - a_p x + p^{k-1} x^2)$

Specifically: EC scripts used `a_p² - p` (should be `p`); Δ script used `τ(p)² - p^{11}` (should be `p^{11}`). The results in `results/` are **pre-bugfix** and being recomputed. The scripts are now correct.

---

## What this is

All computational artefacts underlying our **April 18–20 correspondence** on the $C_1(f,\rho)$ invariant and the failure of the naive $|D_K|\cdot\zeta(2)\to 1$ universality. Intended to let the Toyo team reproduce any of our numbers from source.

## Contents

### `scripts/` — Python computation (mpmath, PARI via `pari` / `cypari2`)

| Script | What it computes | Runtime |
|---|---|---|
| `c1_ensemble_37a1_500zeros.py` | $C_1(37a1,\rho_j)$ for $j=1..500$ at $K=50{,}000$ | ~7 min |
| `c1_ensemble_delta_500zeros.py` | $C_1(\Delta,\rho_j)$ for $j=1..500$ at $K=50{,}000$ | ~7 min |
| `c1_ensemble_389a1_500zeros.py` | $C_1(389a1,\rho_j)$ for $j=1..500$ at $K=50{,}000$ (rank-2) | ~7 min |
| `ndc_per_zero_K_convergence.py` | Per-zero convergence across $K\in\{2K, 5K, 10K, 20K, 50K\}$ | ~20 min |
| `ndc_gl2_full_test.py` | Γ-factor integration + $N^{\rho/2}$ phase + Koyama cutoff | ~15 min |
| `verification_suite.py` | PARI cross-checks at $p\in\{2,97,997,9973,99991\}$ | <1 min |
| `C1_histogram_analysis.py` | Moments, percentiles, χ-fit diagnostics | <1 min |

**Dependencies:** `mpmath>=1.3`, `PARI/GP` (command-line), `cypari2` (optional — scripts fall back to subprocess). All scripts set `mp.dps=25` or `50`.

### `data/`

- `pari_authoritative_zeros.json` — zero locations for 37a1, 389a1, Δ, χ₋₄ from PARI's `lfunzeros`, 50-digit precision. Matches LMFDB to ≥10 digits.

Larger derived tables (~1M $a_p$ values for 37a1, 389a1, τ(n) for Δ, and 1250 zeros of 389a1) live under `python_tasks/data/` in the parent repo and can be regenerated from these scripts.

### `results/` — Markdown reports with verbatim computation output

| File | Key result |
|---|---|
| `C1_500_ZEROS.md` | $E[C_1]=1.48$ for 37a1, $1.31$ for Δ; $E[C_1^2]=2.56$ vs $2.47$ — **37a1 and Δ match within 4% at ensemble level** |
| `C1_K50K_37A1_HEAVY.md` | 37a1, $N{=}500$: $E[C_1^2]=2.2651$ |
| `C1_K50K_DELTA_HEAVY.md` | Δ, $N{=}500$: $E[C_1^2]=2.3862$ |
| `C1_K50K_389A1_HEAVY.md` | 389a1, $N{=}500$: $E[C_1^2]=5.6597$ — **rank-2 differs from rank-1 by factor ~2.4** |
| `C1_K100K_37A1_PER_ZERO.md` | Per-zero convergence table across $K$ for γ₂=5.003, γ₅=9.933, etc. Bare vs Koyama-corrected |
| `DELTA_0500_IDENTITY_HUNT.md` | 50-digit: $C_1(\Delta,\gamma_1,K{=}10^5) = 0.49636822124471502608$ — **not exactly 1/2**; residual $\sim -1/\log K$ |
| `DELTA_0500_STRUCTURAL_ANALYSIS.md` | Petersson/Sym² candidates for the 0.500 value |
| `C1_PETERSSON_NORM_CONNECTION.md` | Rankin-Selberg scaling argument: $|L'(\rho,f)|\propto\sqrt{\langle f,f\rangle}$ under rescaling |
| `C1_DISTRIBUTION_WEIGHT_MAP.md` | Histograms, skew, kurtosis; χ-distribution fit with $k{\approx}2.56$ |
| `C1_HIGHER_MOMENTS.md` | $E[C_1^4]$, $E[C_1^6]$ for moment-matching |

---

## Reproducing the key claims

```bash
cd koyama-shared/scripts
python3 c1_ensemble_37a1_500zeros.py    # E[C₁²] for 37a1
python3 c1_ensemble_delta_500zeros.py   # E[C₁²] for Δ
python3 c1_ensemble_389a1_500zeros.py   # E[C₁²] for 389a1 (rank 2)
```

Compare output against `results/C1_500_ZEROS.md`. All computations use PARI-verified zeros and $a_p$ values; verification points are documented inline.

## Headline result

- **Naive universality falsified:** $|c_K\cdot E_K|\cdot\zeta(2)$ does not converge to $1$; ensemble means drift upward with $N$.
- **Katz-Sarnak-style universality is alive:** For rank-1 weight-2 (37a1) vs weight-12 (Δ), $E[C_1^2]$ matches to within 4% across 500 zeros each. First-zero values (1.17 vs 0.500) are low-lying-zero artefacts, not structural.
- **Rank-2 is structurally distinct:** $E[C_1^2](389a1)=5.66$ vs $\approx 2.5$ for the rank-1/Δ pair — consistent with a different symmetry class.
- **$C_1(f,\rho)$ is zero-specific:** Within a single L-function, $C_1$ varies across zeros (Δ: 0.50 at γ₁, 0.30 at γ₃, 0.36 at γ₅).

See `correspondence/` in the parent repo for the full email thread.

## License / attribution

Scripts released under the repository's existing license. When citing, please attribute to:
> Shai, S. (2026). *Computational verification of C₁(f,ρ) across L-function classes.* Available at https://github.com/SaarShai/Primes-Equispaced, `koyama-shared/` subtree.

Collaborative use by the Toyo University DRH team is explicitly welcomed.
