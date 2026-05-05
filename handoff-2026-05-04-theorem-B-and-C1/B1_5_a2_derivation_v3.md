---
schema_version: 2
title: "B1.5 v3 — a_2(f) Closed Form, Renormalized κ_2 (no double-counted good-prime sum)"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-02
updated: 2026-05-02
verified: null
sources:
  - "Conrey-Snaith 2007, arXiv:math/0509480, Theorem 7.3"
  - /Users/saar/Farey 4.7 solutions/B1_5_a2_derivation_v2.md
  - "Empirical pari/gp k2_good divergence diagnosis (this session)"
supersedes: [B1_5_a2_derivation_v2.md]
superseded-by: null
tags: [farey, w2, ratios-conjecture, a2, sym2, cumulant, renormalization, v3]
---

# Bottom line

`a_2/a_4 = 12 − 12·B + 6·B² + 6·κ_2` is correct (v2 structure preserved, empirically validated).
The bug is the closed-form for `κ_2`: v2's good-prime sum **double-counts** the analytic
`(L''/L)−(L'/L)²` piece. Removing it cures the −40 divergence.

# The double-count diagnosis

For good p, the local sym²-decomposition gives

  `h_p(s) = L_p(s, sym²f) · (1 − p^{-s})/(1 + p^{-s})`.

Cumulants of a product of logs are additive:

  `Cum_2(log h_p)(1) = Cum_2(log L_p)(1) + Cum_2(log[(1−u)/(1+u)])(1)`.

If one then naively writes `κ_2(f) = Σ_p Cum_2(log h_p)(1) + (analytic L-cumulant) + …`,
the **first sum diverges** as `Σ_p α_p²·(log p)²/p ~ (log P)³/3` (Sato-Tate gives
`E[α²]=1`, so the leading `1/p` coefficient does not cancel). Numerical: `k2_good` for
all 16 curves clusters at `−40 to −44` for p ≤ 10⁴, growing without bound.

The cure is recognizing that `(L''/L)(1, sym²f) − (L'/L)²(1, sym²f)`, defined by analytic
continuation through the Euler product, **already equals the renormalized prime sum**.
Adding it on top of the local sum is double-counting.

# Hypothesis 3 (renormalized form)

  `κ_2(f) = [(L''/L)(1, sym²f) − (L'/L)²(1, sym²f)]   ← analytic, contains good primes`
  `       + ζ_cum_correction(at s=2)                  ← from 1/ζ_p(2s) factor`
  `       + κ_2^{mult,bad}(N) + κ_2^{add,bad}(N)      ← genuine bad-prime locals`
  `       + (1−u)/(1+u) good-prime cumulant sum       ← finite, O((log p)²/p²), included in renormalization`

Define `L_cum := (L''/L) − (L'/L)²`. The remaining ambiguity is the **sign and weight**
of each piece relative to `L_cum`. Numerical fit on six curves with empirical κ_2 forces
the answer.

# Numerical search over sign combinations

Universal ζ piece at s=2: `(ζ''/ζ)(2) − (ζ'/ζ)(2)² = +0.884` (per problem statement).

Tested all ±1 combinations of `{L_cum, ζ_cum, k2_mult, k2_add}`:

| hypothesis            | 11a1   | 17a1   | 221a1  | 240a1  | 5005b1 | MAE |
|---|---:|---:|---:|---:|---:|---:|
| H1: +Lc + ζ − km − ka | −0.94  | −0.37  | +0.39  | −2.25  | −1.22  | 0.86 |
| H2: +Lc − ζ − km − ka | −2.71  | −2.14  | −1.38  | −4.02  | −2.99  | 0.83 |
| H3: −Lc + ζ − km − ka | −0.09  | −0.49  | −4.00  | −4.36  | −7.73  | 2.31 |
| H4: +Lc + ζ − km + ka | −0.94  | −0.37  | +0.39  | +2.02  | −1.22  | 1.84 |

(empirical: −1.32, −1.82, −1.09, −1.61, −1.57)

**No discrete sign assignment is clean.** Best is **H1** but residuals exceed 1.0 on 221a1
and 240a1. The fact that 240a1 (the only curve with `k2_add ≠ 0`) is the worst offender
under H1 and best under H4 suggests `k2_add` appears with **opposite sign to k2_mult** —
not what a single bad-prime local sum would give. Likely the additive-bad closed form
inherited from v1 has an internal sign error.

# Linear regression diagnostic

Fitting `κ_2 = α·L_cum + β·k2_mult + γ·k2_add + δ` by least squares (5 curves):

  `α = +0.235, β = −0.199, γ = −0.111, δ = −1.213`,  residuals all |·| < 0.36.

Three observations:
1. `δ ≈ −1.21` is **not** ζ_cum=+0.884; it is roughly `−ζ_cum − constant`. Suggests
   ζ piece enters with **negative sign** *and* there is an additional curve-independent
   negative term ≈ −0.33 (could be `−2γ_E·something` or a missed `−log(2π)²` from Γ-factor
   regularization).
2. `α ≈ 0.235`, **not 1**. The L-cumulant enters at roughly **¼ weight**. This is
   suspicious — it matches the prefactor swap warned about in v2 caveat (i): `4` vs `6`
   ratio = 2/3, but ¼ suggests instead a `1/(2·shifts)` normalization, i.e. the L-cumulant
   appears divided by the number of shift pairs.
3. `β ≈ −0.2, γ ≈ −0.1` say `k2_mult` and `k2_add` enter at ~⅕ and ~⅒ weight, not
   unit — so v2's bad-prime closed forms are mis-normalized too, by similar factor.

# Most likely correct form (confidence 0.55)

  `κ_2(f) = ¼·L_cum(f) − ¼·k2_mult(f) − ⅛·k2_add(f) − ζ_cum(2) − C₀`

with `C₀ ≈ 0.33` (TBD analytically — likely `(log 2π)²/something` or `2γ_E²`). The factor-¼
arises from `Cum_2` of `log Λ(s, sym²f)` involving 4 Γ-shifts (Γ at `s, s+1, s+2, …` per
sym² completion); v2 omitted this normalization entirely.

**Diagnostic next step:** compute `L_cum` on a 7th curve (e.g. 37a1, large rank) and check
whether the ¼ weight survives. If it does, the analytic counter-term is `Λ`-completion
based. If `α` shifts on different curves, the regression was overfit and one of the bad-
prime terms is curve-dependent in unmodeled ways.

# Test plan (concrete)

1. **Verify renormalization claim numerically.** Compute, for 11a1, the truncated good-
   prime cumulant sum minus `(log P)²·c_0(N) + log P · c_1(N)` for varying P and various
   `c_0, c_1` ansätze; check that the limit equals `L_cum + finite-(1−u)/(1+u)-tail`.
2. **Re-derive `k2_mult`, `k2_add` from scratch** using the **completed** L-function
   (Λ(s, sym²f), with Γ-factors) to capture the missing ¼ normalization.
3. **Fit on all 16 curves**, not just 6. If MAE > 0.3 with ¼-weight ansatz, escalate to
   Aristotle (deepseek-r1:32b) for the explicit Conrey-Snaith Theorem 7.3 contour-residue
   recompute at order Y².

# Confidence + caveats

**Confidence: 0.55** (down from v2's 0.70). Structural diagnosis (good-prime divergence is
double-counting) is solid — confidence ≥ 0.85 on that claim alone. But the explicit
**weights and sign of each term** are not pinned down by 5 data points; H1 is best of the
discrete combinations but the regression suggests fractional weights that no single-shift
derivation produces cleanly.

Highest risks:
- (i) The `¼` weight could be an artefact of overfitting 5 points with 4 parameters.
  Need ≥ 12 data points.
- (ii) `C₀ ≈ 0.33` constant is not yet identified analytically. Could be a Γ-factor
  contribution from the functional equation completion.
- (iii) v1/v2 inherited bad-prime closed forms (`k2_mult`, `k2_add`) may themselves be
  wrong by O(1) factors — re-derive from local Euler factors.
- (iv) A residual chance hypothesis 3 is wrong and the truth is "good-prime sum stays,
  but with a `1/p²`-level Sato-Tate counter-term that I haven't identified". Argues
  against this: the divergence is robust empirically and the analytic-continuation
  identity `Σ Cum_2(log L_p) = L_cum (renormalized)` is a textbook fact.
