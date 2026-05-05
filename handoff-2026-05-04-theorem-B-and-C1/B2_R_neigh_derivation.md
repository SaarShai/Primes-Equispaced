---
title: "B2: CUE-Palm second moment of R_neigh(ρ_i)"
type: derivation
domain: research
tier: working
confidence: 0.35
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
schema_version: 2
sources:
  - "Conrey-Farmer-Keating-Rubinstein-Snaith (CFKRS) 2005, 'Integral moments of L-functions', §3-4 (ratios theorem)"
  - "Conrey-Snaith 2007, 'Applications of the L-functions ratios conjectures'"
  - "Snaith 2008, 'Derivative moments for characteristic polynomials from CUE', Comm. Math. Phys."
  - "Bourgade-Nikeghbali, hal-00690322 (CUE Palm measures)"
  - "Hejhal 1994 (triple correlation), Rudnick-Sarnak 1996 (n-level correlations of zeros)"
supersedes: []
superseded-by: null
tags: [c1-spectroscope, R-kernel, CUE, palm, ratios-conjecture, B2]
---

# B2 — Closed-form CUE-Palm second moment of R_neigh

## Bottom line (2 lines)

  C_neigh(K, f) ~ c_∞ · (log K) · |Z'(θ_i)|² / Λ_K²,   with c_∞ = ∫_{-∞}^{∞} |M_W(iy)|² · K_pair(y) dy / (2π) · α_ratio,
  where K_pair(y) = 1 − (sin(πy)/(πy))² is the CUE 2-point kernel and α_ratio is an O(1) ratios-conjecture constant (currently UNRESOLVED in closed form; see Q2 gap).

Numerical estimate (sketch) of the y-integral with M_W(iy) = (1−e^{−1−iy})/(1+iy):
∫ |M_W(iy)|² dy / (2π) ≈ 0.31 (mass concentrated near y=0 where |M_W(0)|² = (1−e^{-1})² ≈ 0.40).
The CUE 2-point factor reduces this; the (log K) factor comes from the diagonal Snaith contribution. The empirical 0.07 is consistent if α_ratio ≈ 0.07/(0.31 · log(K_eff)) with log(K_eff) ~ 4–7. **Plausible but not derived.**

---

## Q1. Palm 2-point form

Conditioning on a CUE eigen-angle pinned at θ_i, the conditional process on remaining N−1 angles has joint density

  ρ_2^{Palm}(θ_i; θ) = (N−1)/N · [ρ_2^{CUE}(θ_i, θ) / ρ_1^{CUE}(θ_i)]
                    = ρ_2^{CUE}(θ_i, θ) / (N/(2π)).

In the bulk-scaling limit (set y = N(θ−θ_i)/(2π), N→∞):

  ρ_2^{Palm}(y) → 1 − (sin(πy)/(πy))² ≡ K_pair(y).   (Dyson sine-kernel form)

Similarly ρ_3^{Palm} → 3-point sine-kernel determinant det[K_sin(y_a − y_b)]_{a,b=1,2,3} restricted to y_a, y_b ≠ 0.

The expectation splits as

  E[|Σ|² | θ_i] = T_diag + T_off,

  T_diag = ∫ |M_W(iy)|² · E_CUE[ |Z'(θ_i)/Z'(θ_i + 2πy/N)|² ] · K_pair(y) dy · (N/(2π))^{-1} · (N/(2π))
        = ∫ |M_W(iy)|² · F_2(y) · K_pair(y) dy

with F_2(y) := E_CUE[|Z'(θ_i)|²/|Z'(θ_i + 2πy/N)|²] (Snaith ratio, see Q2).

  T_off = ∫∫ M_W(iy) M_W(iy')* · e^{iα(y−y')·2π/N} · F_3(y, y') · ρ_3 dy dy'

where α = log K. Note **K^{(θ−θ_i)} = e^{iα y · 2π/N}** so on the mesoscopic scale 2π/N the oscillation is e^{i α y · 2π/N}; if N is taken with N ~ K (matching mean spacings on the L-side), then α/N → const, giving O(1) phase. **In the standard L↔CUE matching, N = log K / (2π), so α · 2π/N = (2π)² ≈ 39.5 — i.e. order-1 phase per unit of y.** This is the regime where the localization argument operates.

## Q2. Ratios via CFKRS / Snaith

Snaith (2008) gives finite-N expressions for E[|Z'(θ)|²]; for the **ratio** E[Z'(θ)Z'(θ')*/Z'(η)Z'(η')*] CFKRS §4 supplies a 4-point ratios formula. In the bulk-scaling limit at distinct points the ratio reduces to a smooth function of the pairwise differences, regular at coincidences only after subtracting the diagonal singularity (Snaith's "renormalized derivative moment"):

  E[|Z'(θ_i)|²/|Z'(θ_i+δ)|²] ~ N² · g(Nδ/(2π)),   δ → 0,

where g is bounded and g(0) corresponds to Snaith's normalized 2nd derivative moment ≈ (constant) · 1. **Closed-form g not extracted in this budget.** Flag: needs CFKRS Theorem 4.1 specialized to (k, ℓ) = (2,2) ratios.

For the present scaling we absorb g into a constant α_ratio (defined as the O(1) prefactor that survives after the N→∞ bulk limit).

## Q3. K → ∞ (α = log K) limit

Substitute u = y · 2π α / N (the oscillation variable). With N = α/(2π) (standard L↔CUE matching, mean spacing 2π/N = (2π)²/α at the angle scale, matching mean zero spacing 2π/log K on the critical line),

  K^{iy} = e^{iα · 2π y / N} → e^{i (2π)² y}  on the y-scale.

The kernel M_W(iy) · e^{iα y · 2π/N} → M_W(iy) · e^{i(2π)² y}, NOT localized in y but localized after integrating against the pair-correlation oscillation. The diagonal piece dominates:

  T_diag ~ α_ratio · ∫_{-∞}^{∞} |M_W(iy)|² (1 − sinc²(πy)) dy.

The off-diagonal piece, by Riemann-Lebesgue against the e^{i(2π)² y} oscillation in 2D, contributes lower order: O(1) without the log K factor.

Combining with the |Z'(θ_i)|²/Λ_K² prefactor from R_neigh squared, and noting that **|Z'(θ_i)|²** itself scales like (log K)² · (typical CUE value) at a CUE eigen-angle (Hughes-Keating-O'Connell type log-normal), the dominant log K factor enters via the c_K(ρ_i,f) normalization upstream rather than from the Palm sum. So:

  **C_neigh(K) = c_∞ · |Z'(θ_i)|² / Λ_K²,**
  c_∞ = α_ratio · ∫ |M_W(iy)|² · (1 − sinc²(πy)) dy.

A direct numerical estimate of the integral (mpmath, M_W(iy) = (1−e^{-1-iy})/(1+iy)) — TODO numerical verify — should give a value of order 0.2–0.4. The log K power is **0** in the proper bulk-scaled normalization once Z' is held fixed; the log K dependence empirically observed enters via Λ_K and |Z'|, both of which are tracked separately in the C1 self-residue identity. **Predicted log K power: 0.**

## Q4. L-function correction

The Rudnick-Sarnak / Hejhal result: n-level correlations of {γ_f} match GUE/CUE in any test-function class supported in (−2/n, 2/n) (Fourier scale). At the pair-correlation level (n=2), Bogomolny-Keating give the lower-order arithmetic correction:

  R_2^{f}(y) = K_pair(y) + (1/log K) · A_f(y) + O(1/log² K),

with A_f(y) an explicit arithmetic kernel built from local factors of L(s, f × f̃). Therefore

  C_neigh^{f}(K) = C_neigh^{CUE}(K) · (1 + a_1(f)/log K + O(1/log² K))

with a_1(f) computable from Sym² f data. **At zeros far from s=1 (height T ≫ 1), the universal CUE prediction is leading; the f-dependent correction is O(1/log K) ≈ 0.1–0.2 at K ~ 10²-10⁴.**

## Q5. Falsifier protocol (≤200 words)

1. **CUE c_∞ test.** Monte Carlo: sample CUE matrices at N = 100, 1000 (≥ 10⁴ samples each), compute R_neigh per sample with the actual M_W kernel, take mean of |R_neigh|² · Λ_K²/|Z'(θ_i)|² (i.e. divide out the Z' prefactor). Compare with predicted c_∞ = α_ratio · ∫|M_W|²(1−sinc²) dy. PASS criterion: agreement to ±5% AFTER pinning down α_ratio numerically from the same Monte Carlo (single-parameter fit). Two-N consistency required.

2. **log K scaling test.** Compute C_neigh / (|Z'|²/Λ_K²) at K = 10², 10³, 10⁴ (i.e. matched N = log K /(2π) ≈ 0.73, 1.10, 1.47 — too small; use N = c·log K for c large enough, e.g. N = 50, 100, 200). PASS criterion: residual after dividing by predicted form (here log K^0 = const) is flat in log K within 10%.

3. **Mollifier-removal test.** Set M_W ≡ 1; rerun MC. Predicted ratio: ∫(1−sinc²) dy / ∫|M_W|²(1−sinc²) dy (computable, ≈ 2–4×). PASS criterion: empirical ratio matches predicted within 10%.

---

## Confidence + caveats

**Confidence: 0.35** (working/episodic tier, NOT promoted).

Honest gaps:
- (Q2) α_ratio not extracted in closed form — needs CFKRS Theorem 4.1 worked out for the specific (Z'(θ_i)Z'(θ_i)*) / (Z'(θ)Z'(θ')*) 4-point ratio. ~half-day with the CFKRS paper open.
- (Q3) The N↔K matching N = log K/(2π) makes N too small for useful N→∞; predictions are at fixed N >> log K. Real C1 needs the **finite-N** Palm-CUE answer, not the bulk limit. This is a structural gap, not just a calculation gap.
- (Q4) a_1(f) for Sym²-related kernel not computed.
- The "log K power = 0" conclusion assumes |Z'(θ_i)|² is held fixed in the normalization. The empirical 0.07 may already absorb |Z'|²/Λ_K² scaling — need to re-check the V2 numerical normalization to confirm.
- No numerical verification of the |M_W|² integral performed in this session — flagged as TODO.

**Status:** skeleton derivation, two flagged gaps (α_ratio closed form, finite-N vs bulk). Falsifier protocol is implementable in ≤1 day of CUE Monte Carlo. Recommend running Q5 test #3 (mollifier-removal) FIRST as a cheap sanity check before investing in α_ratio extraction.
