# ΔW(p) Scaling Law — Empirical Analysis
**Date:** 2026-04-13
**Method:** Python exact Farey, p=11..499

## Result: No clean power law

Joint regression log|ΔW| ~ α·log(p) + β·log|M(p)|:
- α = -5.74, β = 5.56 — physically implausible, extreme noise
- Individual |M| bands: slopes range from -19 to +12 (all noise)
- Overall regression (all M<0 primes): |ΔW| ~ 0.109 · p^{-1.45}

## Interpretation

ΔW = A - B - C + 1 - D_term - 1/n'²
Near-cancellation: A/D_term ∈ [0.97, 1.12].
Residual is dominated by B+C terms which depend on FULL arithmetic structure of p.

No simple f(M(p), p) law exists (consistent with DELTAW_EXACT_FORMULA_RESEARCH.md conclusion).

## Benchmark values
- p~100: |ΔW| ~ 10^{-4} (for M~-3), ~ 10^{-3} (for M~-10)
- p~500: |ΔW| ~ 10^{-5} to 10^{-4}

## Paper note
Add to computational section as remark: "ΔW(p) does not follow a simple power law in p and M(p); the near-cancellation between dilution and new-fraction discrepancy makes the per-step change highly sensitive to arithmetic structure."

## Status
NEGATIVE RESULT — no scaling law. Consistent with no closed form for B.
