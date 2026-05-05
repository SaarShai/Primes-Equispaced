---
schema_version: 2
title: "B1 — a_2(f) Closed Form: Verification Report (Opus 4.7 1M, 2026-05-03)"
type: verification
domain: research
tier: working
confidence: 0.55
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - B1_5_RESOLVED_2026-05-02.md (claimed conf 0.85)
  - B1_5_a2_derivation.md (v1, conf 0.55, structurally wrong)
  - B1_5_a2_derivation_v2.md (v2, conf 0.70, established cumulant structure)
  - B1_5_a2_derivation_v3.md (v3, conf 0.55, double-count diagnosis)
  - B1_5_a2_v2_compute.gp (pari/gp computation script)
  - B1_5_a2_v3_fit.py (LSQ fit of clean fractions)
  - "Conrey-Snaith 2007, arXiv:math/0509480, Theorem 7.3"
  - LMFDB cross-check via pari/gp ellap (this report)
supersedes: [B1_5_RESOLVED_2026-05-02.md]
superseded-by: null
tags: [farey, w2, ratios-conjecture, a2, sym2, verification, opus-4-7]
---

# Bottom line

**The B1.5 RESOLVED claim of confidence 0.85 is too high.** This verification audit
finds the structural framework `a_2/a_4 = 12 − 12·B + 6·B² + 6·κ_2` is justified
(confidence ≥ 0.85 on that piece alone), and the numerical claim **MAE = 0.0726 is
reproduced exactly** with the documented closed form. However, the specific
coefficients `(3/4, −1/2, −1/4, −log 2π)` for κ_2 are **not derived rigorously
in any source file** and are **not LSQ-optimal**.

**Recommended confidence: 0.55–0.60**, not 0.95+. Promotion to publication-grade
requires either (a) a rigorous Conrey–Snaith order-Y² residue contour computation
that produces exactly `(3/4, −1/2, −1/4, −log 2π)`, or (b) ≥ 30 additional curves
showing the same MAE, or both.

# What was verified (publication-ready claims)

## Claim V1: Numerical MAE = 0.0726 reproduced

I independently re-ran the prediction formula

```
κ_2(f)  = (3/4)·L_cum(f) − (1/2)·k2_mult(f) − (1/4)·k2_add(f) − log(2π)
δ_2(f)  = −12·B(f) + 6·B(f)² + 6·κ_2(f)
a_2/a_4 = 12 + δ_2
r(f)    = (−4 + 4·B(f))/Y + (a_2/a_4)/Y²        (Y = log X = log(√N · T_max/(2π)))
```

against the 16-curve table in `B1_5_a2_v3_fit.py`. Result: **MAE 0.0726, max
deviation 0.2505 (curve 20a1)**, exactly matching `B1_5_RESOLVED_2026-05-02.md`.

Per-curve table (this verification, computed independently):

| curve   | r_obs   | r_pred  | diff    |
|---------|--------:|--------:|--------:|
| 11a1    | +0.7825 | +0.8034 | −0.0209 |
| 14a1    | +0.9296 | +0.9343 | −0.0047 |
| 15a1    | +1.0850 | +1.0331 | +0.0519 |
| 17a1    | +0.6168 | +0.6210 | −0.0042 |
| 19a1    | +0.3847 | +0.4325 | −0.0478 |
| 20a1    | +1.0612 | +1.3117 | **−0.2505** |
| 21a1    | +0.7052 | +0.7417 | −0.0365 |
| 24a1    | +1.1921 | +1.1054 | +0.0867 |
| 100a1   | +1.0013 | +1.0656 | −0.0643 |
| 106c1   | +0.3166 | +0.4000 | −0.0834 |
| 200a1   | +0.3065 | +0.4364 | −0.1299 |
| 221a1   | −0.1615 | −0.1780 | +0.0165 |
| 240a1   | +0.7112 | +0.5667 | +0.1445 |
| 496b1   | +0.5377 | +0.5292 | +0.0085 |
| 510a1   | +0.5679 | +0.4840 | +0.0839 |
| 5005b1  | +0.6251 | +0.4973 | +0.1278 |

Wrap baseline MAE 0.1014. Beating by ≈ 30%. Clean reproduction.

## Claim V2: LMFDB cross-check of a_p inputs (11a1, 14a1, 17a1)

Re-computed via pari/gp `ellap`:

| curve | a_2 | a_3 | a_5 | a_7 | a_11 | conductor |
|-------|----:|----:|----:|----:|-----:|----------:|
| 11a1  | −2  | −1  | +1  | −2  | +1   | 11 (mult) |
| 14a1  | −1  | −2  | 0   | +1  | 0    | 14 (mult, mult) |
| 17a1  | −1  | 0   | −2  | +4  | 0    | 17 (mult) |

These match LMFDB canonical values exactly. `Lprime(2,sym²f)/L(2,sym²f) = 0.197410…`
for 11a1 reproduces the script's tabulated `LpL`. The pari `lfunsympow` convention
is verified: weight-2 `f` → sym²f has conductor 121 = 11² for 11a1, completed
analytic conductor 1/2-shifted, so the script's evaluations at "s=2" are the
arithmetic-normalized point one above the edge — i.e. the point where the
Euler product converges and the sum-of-cumulants representation is well-defined.

**Note:** `B1_5_RESOLVED_2026-05-02.md` line 30 writes `(L''/L)(1, sym²f)` — this
is a documentation typo. The actual quantity used (and the correct one for
convergence of the prime-cumulant sum) is **(L''/L)(2, sym²f)** in arithmetic
normalization (= edge + 1 for sym²). All numerical results use s=2, so the
final output is unaffected, but the derivation document needs this corrected
before any publication. (Alternative: state in analytic normalization where
sym² has center s=1/2 and edge s=1, then "s=1" means edge — but that point is
where the prime sum diverges, so still wrong without explicit renormalization.)

## Claim V3: Structural framework `12 − 12κ_1 + 6κ_1² + 6κ_2` is justified

The expansion `a_{4−k}/a_4 = Σ C(k,j)·u_{4,j}·m_{k−j}(κ_1, …, κ_{k−j})` where
`u_{4,j}` are the universal IBP coefficients of `Y⁴ − 4Y³ + 12Y² − 24Y + 24`
and `m_n` is the n-th Bell polynomial in cumulants is a textbook consequence
of (a) Bell-polynomial expansion of `exp(Σ κ_k ε^k/k!)`, (b) integration-by-parts
on the moment integral. For k=2:

```
a_2/a_4 = u_{4,0}·m_2 + u_{4,1}·(−1)·m_1 + u_{4,2}·m_0
        = 1·(κ_1² + κ_2) + (−4)·(−κ_1) + 12·1                     (sign convention)
```

Resolving signs to match the verified `a_3/a_4 = −4 + 4·B(f)` pinpoints
`κ_1 = B(f)` and gives **the (12, −12, +6, +6) pattern with confidence ≥ 0.85**.

# What was NOT verified (publication-blocking gaps)

## Gap G1: The coefficients (3/4, −1/2, −1/4) are not derived

**v2 derivation** (`B1_5_a2_derivation_v2.md`, conf 0.70) gives the natural
closed form with **unit prefactors**:

```
κ_2 = κ_2^{good} + κ_2^{mult} + κ_2^{add} + (L''/L − (L'/L)²) + (ζ''/ζ − (ζ'/ζ)²)(2)
```

(coefficients (1, 1, 1, 1, 1) on (k2_good, k2_mult, k2_add, L_cum, ζ_cum)).

**v3 diagnosis** (`B1_5_a2_derivation_v3.md`, conf 0.55): the v2 form has the
good-prime sum `Σ_p Cum_2(log h_p)(1)` **divergent** as `(log P)³/3` for
truncation P → ∞. This is correct: empirically `k2_good` clusters at −40 to −44
for P = 10⁴ and grows. The fix per v3 is to drop the good-prime sum entirely
because `(L''/L) − (L'/L)²` (defined by analytic continuation) **already
encodes** the renormalized prime sum. Then v3's LSQ regression on 5 curves
yields fractional weights `(0.235, −0.199, −0.111, −1.213)` — **NOT (3/4, −1/2,
−1/4, −log 2π)**.

**The RESOLVED file's coefficients (3/4, −1/2, −1/4, −log 2π) appear with the
provenance**:
> "deepseek-r1:32b derivation (clean form 3/4, 1/2, 1/4)"

with a caveat in §Caveats:
> "deepseek-r1:32b derivation invoked Conrey-Snaith Thm 7.3 by reference;
>  would benefit from direct paper-equation citation in formal write-up."

**This is the core publication-blocking gap.** The coefficients were proposed
by an LLM derivation that was never independently checked against
Conrey–Snaith Theorem 7.3 nor against an independent cumulant-Bell expansion.

## Gap G2: The MAE 0.0726 result is not statistically robust

I computed an LSQ fit directly minimizing **r-prediction MAE** (not κ_2 MAE)
across all 16 curves, fitting

```
κ_2 = c_L · L_cum + c_M · k2_mult + c_A · k2_add + C
```

with all four coefficients free. Result:

| coefficient | claimed (RESOLVED) | LSQ-on-r-optimal |
|-------------|-------------------:|-----------------:|
| c_L         | +0.75              | +0.770           |
| c_M         | −0.50              | −0.215           |
| c_A         | −0.25              | −0.228           |
| C           | −1.838 (= −log 2π) | −2.369           |
| r-MAE       | **0.0726**         | **0.0539**       |

The LSQ-optimal r-MAE of **0.0539** is meaningfully better than the documented
0.0726, which means **the documented (3/4, −1/2, −1/4, −log 2π) is not
the optimal closed form** — it is a structural guess that happens to land
within 30% of optimal. Other ansätze achieve similar quality:

| ansatz                                   | r-MAE  | max  |
|------------------------------------------|-------:|-----:|
| (1/2, −1/2, −1/2, +ζ_cum)                | 0.525  | 0.85 |
| (1/2, −1/2, −1/4, −log 2π)               | 0.096  | 0.28 |
| (3/4, −1/2, −1/4, −log 2π) [DOCUMENTED]  | 0.073  | 0.25 |
| (3/4, −1/2, −1/2, −log 2π)               | 0.098  | 0.26 |
| (3/4, −1/4, −1/2, −log 2π) [M↔A swap]    | 0.130  | 0.26 |
| Pure r-LSQ                                | 0.054  | 0.21 |

With 4 free parameters and 16 data points, multiple "clean" fractional ansätze
achieve r-MAE < 0.10, and the gap between the documented form and the LSQ
optimum is 0.02 — the noise level of one curve. **This is not statistically
sufficient to commit to specific clean fractions for publication.**

## Gap G3: Curve 20a1 anomaly

Curve 20a1 has residual **−0.2505** under the documented form, by far the
largest. Three of the four worst residuals (20a1, 24a1, 240a1) have nonzero
`k2_add` contribution, suggesting the additive-bad-prime closed form
inherited from v1 may have a systematic error not captured by the universal
coefficient `−1/4`. v3 already flagged this, and v3's regression on a different
subset gives `c_A` with opposite sign in some hypotheses. Until 20a1 is
explained (or the additive-prime closed form re-derived from local Euler
factors with a Γ-completion check), the claim is fragile.

## Gap G4: The constant −log(2π) lacks first-principles derivation

`B1_5_RESOLVED_2026-05-02.md` justifies `C = −log(2π)` with:
> "naturally suggested by the analytic conductor X = √N · T/(2π)."

This is heuristic. The constant should fall out as the **specific Y-shift**
in the IBP polynomial when the contour passes near the analytic conductor.
v3 also notes the LSQ-suggested constant is closer to **−1.6** than to
**−1.838 = −log 2π**; the difference is again at the 0.03–0.05 level which
multiple curves can absorb.

# Verified algebraic structure (publication-ready)

```
a_2(f)/a_4 = 12 − 12·κ_1(f) + 6·κ_1(f)² + 6·κ_2(f)
```
with `κ_1(f) = B(f) = γ_E + H_unram(f) + S_mult(f) + S_add(f)`.

This **structural identity** is rigorous (Bell-polynomial / IBP universal,
sees no curve-specific input beyond κ_1 and κ_2). **Confidence on this piece
alone: 0.90.**

# Unverified component (publication-blocking)

```
κ_2(f) ≟ (3/4)·[(L''/L)(2, sym²f) − ((L'/L)(2, sym²f))²]
       − (1/2)·S_mult^(2)(N) − (1/4)·S_add^(2)(N) − log(2π)
```

with the bad-prime cumulants

```
S_mult^(2)(N) = Σ_{p‖N} (log p)² · [p/(p+1)² + 2 (1/p)/(1+1/p)]
S_add^(2)(N)  = Σ_{p²|N} (log p)² · [1/(1−1/p)² + (1/p)²/(1−1/p²)²]
```

**Confidence on these specific coefficients: 0.55–0.60.** Empirical fit MAE
0.073, but multiple alternative clean ansätze achieve MAE 0.08–0.10, and
the LSQ-optimum (0.054) sits 0.02 below.

# What is needed to lift to publication-grade (≥ 0.95)

## Required (any one of):

1. **Rigorous Conrey–Snaith Thm 7.3 contour residue at order Y²** with explicit
   evaluation of the universal Y² coefficient produced by the 4-shift mollified
   ratio integrand. The output should be an exact closed form whose coefficients
   on `L_cum`, `k2_mult`, `k2_add`, and constant are matched (or not) to (3/4,
   −1/2, −1/4, −log 2π).

   *Suggested next step:* delegate to Aristotle (deepseek-r1:32b) with the
   explicit prompt to produce a 30-line derivation citing equation numbers
   from Conrey–Snaith 2007, with all Γ-factor / completion contributions
   tracked separately.

2. **Cross-validation on 30+ curves**, drawn from independent rank-0 cohorts
   (small conductor, mid conductor, large conductor; mixed bad-reduction
   types). Target: MAE on hold-out set within 20% of MAE on training set.
   This is the standard cross-validation test that the current 16-curve fit
   does not pass. (No held-out set was used — all 16 curves contributed to
   both fitting and reporting MAE.)

3. **Independent re-derivation by one or more LLMs** of the κ_2 coefficients
   from the renormalized residue formula, with each derivation producing the
   same (3/4, −1/2, −1/4) up to provable equivalences. Currently we have
   exactly **one** LLM derivation (deepseek-r1:32b) and one numerical fit;
   no independent confirmation.

## Helpful (any of):

4. Re-derivation of `S_mult^(2)` and `S_add^(2)` from the local Euler factors
   using the **completed** L-function `Λ(s, sym²f)`. If the Γ-factor
   contributions yield natural prefactors of `1/4` or `1/2`, that would
   ground the (−1/2, −1/4) pattern.

5. Resolve the 20a1 residual −0.2505: either by including a κ_3 correction
   (sub-sub-leading Y term `a_1`), or by identifying a missing additive-prime
   contribution at p=2.

6. Fix the "s=1" → "s=2" documentation typo in
   `B1_5_RESOLVED_2026-05-02.md` and `B1_5_a2_derivation.md`.

# Final assessment

| Component                                   | Confidence | Status |
|---------------------------------------------|-----------:|--------|
| Structural identity (12, −12, +6, +6)·(B, B², κ_2) | 0.90 | **Publication-ready** |
| Universal cumulant decomposition of κ_2     | 0.80       | Solid (v2) |
| Renormalization (drop k2_good)              | 0.85       | Solid (v3 diagnosis) |
| Specific coefficients (3/4, −1/2, −1/4)     | 0.55       | **Not derived** |
| Constant C = −log(2π)                       | 0.50       | **Heuristic** |
| Numerical MAE 0.0726 reproducibility        | 1.00       | Verified |
| Statistical robustness of MAE 0.0726        | 0.40       | Sensitive to clean-fraction choice |
| Cross-validation                            | 0.30       | No hold-out test |
| LMFDB consistency of a_p inputs              | 1.00       | Verified |

**Overall: 0.55–0.60**, NOT 0.85 (RESOLVED claim) and far from publication-grade
0.95+.

# Caveats

- I did not re-derive `B(f)` or its decomposition. Confidence on `B(f)`
  inherits from the B1 phase (already published in `B1_RESOLVED_2026-05-02.md`).
- The `Y` per curve is taken as given from `W2_CF_RESOLVED.json` (read into
  `B1_5_a2_v3_fit.py`); not re-verified here.
- The pari/gp computation `B1_5_a2_v2_compute.gp` includes `k2_good` in
  `kappa2_total`, but the `B1_5_a2_v3_fit.py` regression uses `L_cum`,
  `k2m`, `k2a` only (drops `k2_good`). The 16-curve table in this verification
  uses the v3-corrected formula. The `kappa2_total` column in the input data
  is therefore **not what was used** for the documented closed form — it
  is an intermediate diagnostic that confirms the divergence problem.
- The v3 derivation file claims confidence 0.55. The RESOLVED file claims
  0.85. The supersession chain `v1 → v2 → v3` does not include RESOLVED
  as a child; RESOLVED appears to have been written **after v3** but with
  higher claimed confidence than either parent — a metadata anomaly.

# Recommendation

Do not submit a paper section claiming `(3/4, −1/2, −1/4, −log 2π)` as a
proven closed form. Two safe paper-section framings:

**Option A (conservative):**
> "We propose the structural identity `a_2/a_4 = 12 − 12B + 6B² + 6κ_2`
>  and identify κ_2 as a second cumulant. Numerically, the empirical fit
>  `κ_2 ≈ (3/4)·L_cum − (1/2)·k2_mult − (1/4)·k2_add − log(2π)` achieves
>  MAE 0.073 on 16 weight-2 newforms; we conjecture this closed form and
>  leave its rigorous derivation as an open problem."

**Option B (deferred):**
> Drop the explicit κ_2 closed form; report only the structural identity
> and the empirical fact that **some** linear combination of L_cum, k2_mult,
> k2_add, and a curve-independent constant produces MAE < 0.1.

Either framing is publishable now. The current "MAE 0.073, confidence 0.85"
framing is not.
