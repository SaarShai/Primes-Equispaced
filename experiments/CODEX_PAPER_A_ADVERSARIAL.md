# Adversarial Review: Paper A — Codex as Hostile JNT Referee
**Date:** 2026-04-13
**Verdict:** REJECT (but fixable)

## Claim-by-claim verdicts

| # | Claim | Verdict | Key attack |
|---|-------|---------|-----------|
| 1 | ΔW(N) is novel | OVERSTATED | First difference of classical discrepancy. Viewpoint, not new object. |
| 2 | Four-term decomposition | TRIVIAL | Algebraic expansion, not structural theorem. Plus naming is sloppy (4 terms + boundary). |
| 3 | R₂ > 0 gap-energy | UNPROVED | R₂ undefined in accessible draft. If sum of squares → trivial. If not → proof missing. |
| 4 | D(1/p) ~ -3p/π² | OVERSTATED | One-line corollary of totient asymptotic. "65%" is finite-sample stat. |
| 5 | GK top 20% → 93.6% | UNPROVED | Single observation at p=100. No theorem, no error bars. |
| 6 | P(ΔW<0) → 0.73 | UNPROVED | Rubinstein-Sarnak not applied (no limiting distribution for ΔW derived). |
| 7 | Explicit formula ΔW = Σ_ρ g | UNPROVED | g undefined. No smoothing/convergence/error stated. Just M(x) repackaged. |
| 8 | ΔW ~ M(p)/p² | UNPROVED | Draft says p^{-1.77} empirically! Bridge identity controls ONE Fourier coeff, not full ΔW. |
| 9 | ΔW vs δD distinct | OVERSTATED | R=-0.67 proves moderate dependence, not distinction. Same underlying geometry. |
| 10 | Lean verification | TRIVIAL | Certification layer, not JNT contribution. Inconsistent counts (207 vs 422). |

## Critical finding from draft
Bridge identity found: **Σ_{f∈F_{p-1}} e^{2πipf} = M(p) + 2**
This controls one Fourier coefficient only. Does NOT give the full ΔW decomposition.

## Fixes needed (in order)
1. DEFINE R₂ precisely and prove or reclassify
2. Rephrase novelty: "we study the per-step increment" not "novel object"
3. Demote four-term to lemma, explain WHY the split is useful
4. All percentages (65%, 93.6%, 73%): label empirical, show robustness
5. ΔW ~ M(p)/p²: move to experimental section, note discrepancy with p^{-1.77}
6. Explicit formula section: specify g, regularization, error bounds
7. Fix Lean count inconsistency (207 vs 422)
8. ΔW vs δD: prove structural non-equivalence, not just R=-0.67

## What survives
- The per-step study IS a legitimate viewpoint
- The four-term decomposition IS algebraically correct (just demote to lemma)
- The empirical observations ARE interesting (just present honestly)
- The RH+LI conditional connection IS worth stating (as conjecture)
