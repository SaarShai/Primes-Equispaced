# Review Context for Gemini 3.1 Pro
Updated: 2026-04-05

## Instructions
You are a hostile referee for Mathematics of Computation. Review the attached paper (main.tex) thoroughly. This paper has been through 10 independent reviews and many fixes. Your job: find what's STILL wrong.

## What This Paper Claims
1. A novel "per-step Farey discrepancy" ΔW(p) = W(F_{p-1}) - W(F_p)
2. Its sign correlates strongly with cos(γ₁·log(p)) — a Chebyshev bias in Farey sequences
3. A "Farey Spectroscope" F(γ) detects the first 3 zeta zeros from Farey data
4. D(1/p) = 2 - |F_p|/p = 1 + 1/p - |F_{p-1}|/p proved exactly (65% of damage)
5. Damage/response mechanism: primes damage (R₁ < 0), old fractions overcompensate (R_resp > 0)
6. Composites with φ(n)/n < 1/3 always heal (conjecture, verified n≤400)
7. Lean 4 formal verification of 258 results (1 open conjecture = sorry)

## Previous Reviews Applied (10 rounds)
- **Codex (3 rounds):** Fixed R(p) definition, Sign Theorem→Observation, figure captions, missing refs, Σ D_{F_p}(k/p) corrected to (p-1)/2
- **Opus:** Fixed R(p) factor-of-2, "Sign Pattern" naming, Ingham claim, novelty claim
- **Gemma4:** Fixed "correlates strongly" (was "phase-locked"), selection bias note, 6 theorems→lemmas
- **Gemini Flash:** Displacement-Cosine→Observation, classical results flagged
- **Gemini 3.1 + Gemini 3 (3 rounds):** Prop 3.9 confirmed correct, R(p)/R₂ notation unified, "Master Involution Principle"→explicit involution, Deficit Minimality attributed to Rademacher, Shift-Squared→Conjecture, Fisher Information labeled elementary, "intentional sorry"→"open conjecture"
- **Codex (Kloosterman):** PROVED the Kloosterman bound approach is FALSE. T_b - E[T_b] is a Dedekind sum convolution, not a Kloosterman sum. Paper corrected from "Kloosterman" to "Dedekind" throughout.
- **Codex (Cauchy-Schwarz):** Quantified: 75% within-denominator cancellation, 16.6× looseness (not 44× as previously stated). Remark added.
- **Self-review:** All 14 "Proof sketch" labels upgraded to "Proof". Null hypothesis control figure added (Figure 17).

## What Has Changed Since Last Review
1. "Kloosterman estimate" → "Dedekind sum estimate" throughout (Codex proved Kloosterman is wrong)
2. Cauchy-Schwarz gap Remark added to Open Questions (75%/25% decomposition, 16.6×)
3. Null hypothesis control figure added (random weights = no peaks, confirming spectroscope is real)
4. All proof sketches relabeled as proofs
5. Classical results explicitly attributed (Hardy-Wright, Rademacher)
6. AI Use Declaration section (per STM 2025 guidelines, AI not listed as author)

## What To Check Now
1. Is the Dedekind sum formulation in the analytic gap correct?
2. Are all proofs now complete (no remaining "proof sketch" labels)?
3. Is the notation fully consistent (R(p), R_resp, R₁, δ, δ₁)?
4. Does the null control figure adequately address selection bias?
5. Are there any remaining overstatements or mathematical errors?
6. Is this ready for arXiv submission?

## Key Numbers To Verify
- 3,829 qualifying primes (M(p)≤-3) up to p≈84K for spectroscope
- 4,617 qualifying primes up to p=100K for sign pattern
- R > 0 for all qualifying primes (min R=0.0068 at p=64,781)
- Amplitude correlation r=0.997 (n=10 zeros, p<10⁻⁸)
- γ₁ at 14.08 (0.4%), γ₂ at 20.86 (0.8%), γ₃ at 24.94 (0.3%)
- D(1/p)·δ₁(1/p) → -3/π² ≈ -0.304
- φ(n)/n < 1/3 → 100% heal (21/21 composites, n≤400)
- Cauchy-Schwarz gap: 16.6× at p=997 (75% within-denominator)
- 258 Lean 4 results, 1 open conjecture (sorry)
- Kloosterman bound is FALSE for this problem (Dedekind sums instead)
