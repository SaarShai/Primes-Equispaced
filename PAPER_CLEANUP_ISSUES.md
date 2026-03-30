# Paper Cleanup Issues (from Codex Reviewer)
## Priority: CRITICAL before any submission

### P0: Sign Theorem proof section is self-contradictory
- Lines 2082-2093: Claims unconditional, then RH-conditional, then "no explicit crossover"
- FIX: Rewrite entirely using the ACTUAL proof chain:
  1. Random model E[Σδ²] = N²/(2π²) (proved, Steps 1-5)
  2. Dedekind reciprocity: S(p) = O(p²/logp) (SIGNED_FLUCTUATION_PROOF.md)
  3. Σδ² ≥ cN² for p ≥ P₀
  4. Computational base for p ≤ P₀
- Remove ALL references to Kloosterman pointwise bounds (they FAIL)
- State clearly: "The proof is unconditional, using Dedekind reciprocity for the fluctuation bound and El Marraki for effective Mertens"

### P0: Tail argument uses empirical constants
- deficit ≤ 0.006p² is verified to p=500 only
- B ≥ 0 is computational (p ≤ 3000)
- FIX: The bypass doesn't need B ≥ 0. It needs C+D > A, which follows from Σδ² ≥ cN² (proved via Dedekind). Rewrite to make clear that B ≥ 0 is an EMPIRICAL observation, not a proof ingredient.

### P1: Shift-squared proof mechanism mismatch
- Paper says Kloosterman, actual proof uses Dedekind reciprocity
- FIX: Replace Kloosterman discussion with the actual proof from SIGNED_FLUCTUATION_PROOF.md

### P1: Lean files incomplete in handoff
- Full project has 19 files, handoff had 5
- FIX: Include complete RequestProject/ directory in any submission

### P1: Computational artifacts not included
- No .py, .c, .csv files in handoff
- FIX: Create reproducibility package with all scripts

### P1: Remark about "no explicit crossover" contradicts proof
- FIX: Either compute P₀ explicitly or remove the remark

## New sections to ADD:
1. Triangular distribution theorem (TRIANGULAR_DISTRIBUTION_PROOF.md)
2. Composites healing section (COMPOSITES_HEAL_CLOSE.md)
3. Zero spectrum figure (ZERO_PAIR_DETECTION_TEST.md)
4. Spectral positivity (CODEX_NEXT_TASK_PROGRESS_2026_03_29.md)
5. Updated abstract mentioning three bridges (honestly stated)
