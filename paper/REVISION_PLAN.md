# Paper 1 Revision Plan — Based on Reviewer Feedback
Date: 2026-04-06

## CRITICAL FIXES (must do)

### 1. Abstract — rewrite in plain words (lines 53-84)
Remove undefined symbols from abstract. Explain in simple language what the paper does.

### 2. Nomenclature — define before use
- δ(f), D(f): used in abstract (line 66) before definition (line 246, 252). Move defs earlier or remove from abstract.
- R(p): formula in abstract (line 70), formal definition at line 1207. Remove from abstract.
- B, C: used at line 467, defined at line 750. Add forward reference or reorder.
- δ_b: used at lines 790, 960, 1070+ but NEVER formally defined. ADD DEFINITION.

### 3. "Wobble" attribution — line 113, 152
Claimed "following the Franel tradition" but no ref to Franel using this term. Either find ref or say "which we call the wobble."

### 4. Casual tone — fix headings and language
- Line 161: "The observation that started it all" → "Motivating observation" or "Per-step asymmetry"
- Line 533: "When adding a prime p" → clarify N=p-1 explicitly
- Line 767: "almost exactly cancels" → "cancels to within O(1/p)"
- Line 772: "18% additional margin" → quantify precisely

### 5. Expand short proofs — Theorems 3.5, 3.9, 3.12
Reviewer says proofs too brief. Add intermediate steps.

### 6. Observation vs Proof — clarify status
All 6 observations already state evidence level (scan confirms ✓). But add explicit [Computational] tag to each.

### 7. Conjecture structure (Section 4)
Reviewer says "bringing up conjecture you disprove immediately is not interesting."
FIX: Remove the "Historical conjecture" label. Just state the natural question and immediately give the counterexample as motivation for the M≤-3 threshold.

### 8. Cite reviewer's paper
Add citation to https://www.mdpi.com/2227-7390/13/1/140 and discuss relationship between our R(f) and their local discrepancy.

### 9. Bridge Identity — clarify novelty
Line 274-277 says "new in this form." Need to be more precise: the exponential sum identity is classical (Ramanujan), our contribution is the per-step framework.

## REVIEWER 1 REQUEST: Formal proof ΔW → zeros
This is the Dedekind sum gap (POST-8 HIGHEST priority). The local models are working on this now (PHASE_CONSTANT_RECONCILE, R2_DEDEKIND_PROOF tasks). If we can derive the explicit formula for ΔW, this addresses Reviewer 1 directly.
