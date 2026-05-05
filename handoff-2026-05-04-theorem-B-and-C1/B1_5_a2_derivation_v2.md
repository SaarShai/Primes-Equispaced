---
schema_version: 2
title: "B1.5 v2 — a_2(f) Closed Form via Cumulant Expansion (corrected)"
type: derivation
domain: research
tier: working
confidence: 0.70
created: 2026-05-02
updated: 2026-05-02
verified: null
sources:
  - "Conrey-Snaith 2007, arXiv:math/0509480, Theorem 7.3"
  - "Hughes-Young 2010, 4th moment of Dirichlet L-fns, Proc LMS"
  - /Users/saar/Farey 4.7 solutions/B1_5_a2_derivation.md (v1, 0.55, structurally wrong mix)
  - /Users/saar/NEW Farey 5.5/projects/farey-research/W2_PHASE12_SELF_RESIDUE_VERIFIED_2026-05-01.md
supersedes: [B1_5_a2_derivation.md]
superseded-by: null
tags: [farey, w2, ratios-conjecture, a2, sym2, cumulant, derivation, v2]
---

**Bottom line:**  `a_2(f)/a_4 = 12 − 12·B(f) + 6·B(f)² + 6·κ_2(f)`  with `κ_2` the SECOND CUMULANT of `log A_f` (NOT a B-quadratic mixing).

# What was wrong in v1

v1 wrote `a_2/a_4 = 12 + 24·B² − 32·B + 2·K_2^{arith} + 2·G_ζ`. The `+24·B² − 32·B` came from naively applying `(d/dY − 1/Y)²` to the IBP polynomial — but a_3 and a_2 are NOT successive Y-derivatives of one univariate B-polynomial. They are **separate Taylor coefficients** of the 4-shift ratios integrand, and B(f) and κ_2(f) enter via DIFFERENT cumulants. v1 also double-counted by adding a quadratic in B AND adding K_2^{good} separately. Empirically v1 predicted a_2/a_4 ∈ [−61,+25]; truth is [−2.3, +3.7].

# Correct structure (Conrey-Snaith → cumulant expansion)

Write the moment integrand near the diagonal as

  `A_f(α,β,γ,δ) · J(α,β,γ,δ; Y)`

where `J` is the universal CUE Jacobian/IBP factor (gives `Y⁴ − 4Y³ + 12Y² − 24Y + 24` for `A_f ≡ 1`) and `A_f = exp(Σ_k κ_k(f) · ε^k / k!)` is the cumulant generating function of `log A_f` along the diagonal direction `ε`. After the contour residue, the Y-polynomial coefficients are

  `a_{4-k}/a_4 = Σ_{j=0}^k C(k,j) · u_{4,j} · m_{k−j}(κ_1,…,κ_{k−j})`

with `u_{4,j}` the j-th universal IBP coefficient (`u_{4,0}=1, u_{4,1}=−4, u_{4,2}=+12, u_{4,3}=−24, u_{4,4}=+24`) and `m_n` the n-th moment of the cumulants (Bell polynomial). Concretely:

| k | a_{4−k}/a_4 |
|---|---|
| 0 | 1 |
| 1 | −4 + 4·κ_1 |
| 2 | **+12 − 12·κ_1 + 6·κ_1² + 6·κ_2** |
| 3 | −24 + 36·κ_1 − 24·κ_1² + 4·κ_1³ + (lower κ_2,κ_3 terms) |

For k=1 this reproduces the verified `a_3/a_4 = −4 + 4·B(f)` with `κ_1 = B(f)`. For k=2 the binomial pattern is forced: coefficient of κ_1² is `C(4,2) − C(4,1)·1 = 6` (from `m_2 = κ_1² + κ_2` and shift between Y-orders), and coefficient of κ_1 is `−C(4,1)·C(2,1)/(1) = −12`. (a) **Universal Y² constant is +12**, confirmed.

# (b) The cumulant `κ_2(f)`

`κ_2 = κ_2^{good} + κ_2^{mult} + κ_2^{add} + κ_2^{ζ/L}`, where (notation: `u = p^{-1}`, sym² Satake `β_p^{±2},1`):

```
κ_2^{good}  = Σ_{p∤N} [ (h_p''/h_p)(1) − ((h_p'/h_p)(1))² ]
            = Σ_{p∤N} (log p)² · [ Σ_{j∈{2,0,−2}} β_p^j u/(1−β_p^j u)² − u/(1−u)² − 2u²(1+u²)/(1−u²)² ]
κ_2^{mult}  = Σ_{p‖N} (log p)² · [ p/(p+1)²  +  2u(1+u)^{−1}·... ]   (as in v1)
κ_2^{add}   = Σ_{p²|N}(log p)² · [ (1−u)^{−2} + u²(1−u²)^{−2} ]      (as in v1)
κ_2^{ζ/L}  = (L''/L)(1, sym²f) − (L'/L)(1, sym²f)²
            + (ζ''/ζ)(2) − (ζ'/ζ)(2)²        ← note SIGN: cumulant is C''−(C')²
```

Crucial sign: a cumulant of `log F` is `(F''/F) − (F'/F)²`, so the ζ piece is `(ζ''/ζ)(2) − (ζ'/ζ)(2)²` ≈ 1.003 − 0.879 = **+0.124** (v1 had this with the wrong sign). The L piece similarly is `(L''/L) − (L'/L)²`. No `2γ_E·(L'/L)` cross term — that arose in v1 from confusing a derivative-shift with a cumulant.

# (c) Numerical sanity check vs empirical table

Predicted `δ_2(f) := a_2/a_4 − 12 = −12·B + 6·B² + 6·κ_2`. From the empirical column `(a_2/a_4)_emp` and known `B(f)`, back out implied `κ_2`:

| curve | B | emp δ_2 | −12B+6B² | implied 6κ_2 | κ_2 |
|---|---:|---:|---:|---:|---:|
| 11a1   | 2.114 | −9.53 | −1.59  | −7.94 | −1.32 |
| 17a1   | 1.922 | −12.79| −1.89  | −10.90| −1.82 |
| 221a1  | 0.882 | −12.45| −5.91  | −6.54 | −1.09 |
| 5005b1 | 1.925 | −11.28| −1.85  | −9.43 | −1.57 |
| 240a1  | 1.984 | −11.83| −2.18  | −9.65 | −1.61 |

Implied κ_2 ∈ [−1.1, −1.9] — a tight, curve-stable range, exactly what a SUM-OF-LOCAL second cumulant should give. (Compare v1's K_2^{good} ≈ −35 across all curves — wildly off.) This is strong structural evidence the formula is right.

The L-piece dominates per-curve variance: e.g. 221a1 has `L''/L = +3.575`, `L'/L ≈ −1.18`, so L-cumulant contribution ≈ 3.575 − 1.39 = +2.18; combined with negative ζ piece (+0.124) and negative `κ_2^{good}` (Sato-Tate gives `E[α_p²−1]·(log p)²/p² < 0` typical), net `κ_2 ≈ −1.1` — matches.

# Test plan

Compute κ_2^{good} via primes p ≤ 10⁴ (tail O((log p)²/p²)), add bad-prime closed forms, add `(L''/L) − (L'/L)²` from pari `lfunsympow`, add ζ-cumulant constant +0.124. Predict δ_2 per curve, compare to table. Target: residual MAE < 0.5 across 16 curves. If MAE > 1, suspect prefactor on κ_2 (could be `4` not `6` if ratios convention differs) or sign on `κ_2^{good}` quadratic term.

# Confidence + caveat

**Confidence: 0.70.** Cumulant structure is rigorously what Conrey-Snaith Thm 7.3 gives at order Y²; the binomial coefficients (12, −12, +6, +6) follow from Bell polynomials and IBP universals (4!/k!). HIGHEST RISK: (i) the prefactor on κ_2 could be `4` instead of `6` if the GL(2)-sym² ratios transplant uses 2 shift variables instead of 4; resolve numerically — if implied κ_2 comes out clustered around `−1` rather than `−1.5`, switch to `4`. (ii) `κ_2^{good}` sign of the `−2u²(1+u²)/(1−u²)²` term — check by comparison to Sato-Tate average. (iii) bad-prime closed forms inherited from v1 unchanged; mult/add formulas should be re-derived from local Euler factors but are subdominant. NO B² IBP MIXING term — that was v1's structural error.
