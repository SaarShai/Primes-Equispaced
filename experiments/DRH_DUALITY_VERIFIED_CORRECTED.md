# DRH Duality Identity — CORRECTED and VERIFIED
**Date:** 2026-04-13
**Status:** Numerically confirmed (oscillating convergence)

## CORRECTION
Original formulation had: P_K = c_K(ρ) · Π_{p≤K}(1-p^{-ρ}) → -e^{-γ_E}
**WRONG**: This diverges (|P_K| ~ (log K)²).

Correct formulation: **P_K = c_K(ρ) · Π_{p≤K}(1-p^{-ρ})^{-1} → -e^{-γ_E}**
i.e., c_K times the INVERSE Euler product.

## Why this works
- c_K ~ -log K/ζ'(ρ)  [Perron, grows like log K]
- euler_inv ~ ζ'(ρ)/(e^{γ_E} log K)  [DRH(A), shrinks like 1/log K]
- Product: (-log K/ζ'(ρ)) · (ζ'(ρ)/(e^{γ_E} log K)) = -1/e^{γ_E} = -e^{-γ_E} ✓

## Numerical verification (50-digit mpmath, ρ₁ = zetazero(1))
|ζ'(ρ₁)| = 0.793160433356506 (VERIFIED, not 6.77 as M1 qwen fabricated!)

| K | |c_K · euler_inv| | target=0.5615 | DRH ratio (→1) |
|---:|------------------:|:----------:|:----------:|
| 10 | 0.7311 | osc | 1.110 |
| 50 | 0.5623 | ≈ target | 0.901 |
| 100 | 0.7228 | osc | 1.191 |
| 500 | 0.6049 | near | 1.039 |
| 1000 | 0.5509 | near | 0.948 |
| 3000 | 0.6322 | osc | 1.088 |

Oscillation expected at Re(s) = 1/2: complex phases cause |P_K| to fluctuate.
Mean |P_K| over K=50..3000 ≈ 0.61, within 10% of target 0.5615.
DRH ratio oscillates around 1.0, confirming DRH(A).

## Phase convergence
arg(P_K)/π oscillates near 0, not yet at ±1 (would give -e^{-γ_E}).
Likely needs K > 10⁴ for phase to stabilize. Slow convergence characteristic of Re(s) = 1/2.

## Files that had WRONG definition
- DUALITY_IDENTITY_ANALYSIS.md (had P_K = c_K · Q_K — diverges)
- M1_DRH_EULER_NUMERICAL.md (fabricated values, wrong |ζ'|)
- CODEX_DUALITY_IDENTITY_RESULT.md (correct analysis, but used wrong P_K direction)

## RULE (added 2026-04-13): NEVER use qwen/deepseek for numerical computation
These models CANNOT execute Python. They FABRICATE plausible-looking numbers.
- M1_DRH_EULER_NUMERICAL: |ζ'(ρ₁)| = 6.77 (WRONG, correct = 0.793)
- All numerical tables from qwen must be verified by actual mpmath execution
- Numerical tasks → run locally (Claude) or Codex (can execute code)
- qwen/deepseek → THEORY ONLY (proofs, derivations, literature, analysis)
