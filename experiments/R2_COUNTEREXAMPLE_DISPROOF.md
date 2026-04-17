# R₂ Positivity — DISPROVED
**Date:** 2026-04-13
**Source:** Codex analysis + local mpmath verification

## Result

**R₂(N) > 0 for all primes N ≥ 5 is FALSE.**

Counterexamples (locally verified, exact Farey arithmetic):
| p | R₂ |
|---|-----|
| 191 | +1.875e-05 |
| 193 | +4.625e-06 |
| **197** | **-2.831e-06** ← FIRST NEGATIVE |
| **199** | **-1.384e-05** ← NEGATIVE |
| 211 | +1.975e-05 |

## What WAS proved (p=5..79)

R₂ > 0 for all primes tested 5..79 — this was a small-prime accident, not a theorem.

## Proof of general failure (Codex)

Exact formula [PROVED]:
R₂ = 2·Σ_f d_f·ε_f − Σ_f ε_f²

where:
- d_f = f - k/(n_old-1) = old rank discrepancy of f
- ε_f = (old_ideal - new_ideal) = k/(n_old-1) - j(f)/(n_new-1) = shift in ideal position
- j(f) = old_rank(f) + ⌊Nf⌋ = new rank of f in F_N

The sum 2·Σ d_f·ε_f is a covariance term between old discrepancy and ideal shift.
This is sign-indefinite — it can be negative when d_f and ε_f are anti-correlated.

General counterexample [PROVED by Codex]:
x = (0, 2/5, 1) ⊂ (0, 1/5, 2/5, 1):
  (2/5 - 1/2)² - (2/5 - 2/3)² = 1/100 - 16/225 < 0

## Impact on Paper A

The four-term decomposition ΔW = A - B - C - D:
- A (dilution) = Σ D(f)² · (1/n² - 1/n'²) > 0 ALWAYS (trivial, 1/n² > 1/n'²)
- R₂ is a DIFFERENT quantity from A — more subtle, not always positive
- The Sign Theorem proof path (bypassing R₂) is UNAFFECTED

## Required fixes

1. ✅ Abstract: Removed "R₂ > 0 for all p ≥ 5" claim
2. Paper A body §4 (four-term decomposition): Do NOT claim R₂ > 0 — state it oscillates
3. New direction: characterize when R₂ < 0 (first occurs p=197). Related to M(p)?
4. VERIFIED_CONSTANTS.md: Flagged R₂ > 0 as DISPROVED

## Open questions

1. What is P(R₂(p) < 0) over primes? Is it ~50%?
2. Is sign of R₂(p) correlated with M(p)?
3. What replaces R₂ > 0 in the Sign Theorem proof? (The current proof uses A not R₂.)

## Status
DISPROVED. Abstract fixed. Body needs scan for any R₂ > 0 claims.
