---
title: FAPC₂ v2 — Adversarial + Paper-Verified Audit Verdict
date: 2026-05-03
type: audit
supersedes: FAPC2_eta_above_1_PROOF_v2.md (partial)
---

# FAPC₂ v2 Audit — Final Verdict After Direct PDF Verification

## Verbatim quotes from source PDFs

### DFS Lemma 2.4 (arXiv:2210.15782, p. ~10)

> "Lemma 2.4 (Estimated Petersson Formula). Let k be a fixed even integer.
> If N is prime, N² ∤ n and (m, N) = 1, we have
>   Σ_{f∈B*_k(N)} ω_f(N) λ_f(m) λ_f(n) = δ(m,n) + O_{k,ε}((n,N)^{-1/2} N^{-1+ε} (mn)^{1/4+ε})."

**Exponent (mn)^{1/4+ε} CONFIRMED.** Claim A in adversarial issue #2 holds. Claim B (the (mn)^{1/2} concern) was wrong.

### DFS Theorem 1.1 (arXiv:2210.15782, abstract + §1)

> "Θ₂ = 1.866…"  
> "Θ₂ = 1 + √3 / 2"  (from formula display)

**Θ₂ = 1 + √3/2 ≈ 1.866 CONFIRMED.** The 22/9 ≈ 2.444 number cited in MK1 / MASTER_KEY was indeed wrong. FAPC₂-v2 agent correct on this correction.

### ILS Theorem 1.2 (Publ. IHES 91, p. ~62)

> "Theorem 1.2. — Fix any φ ∈ S(R) with the support of φ̂ in (−1, 1). Then we have
>  lim ... Σ D(f, φ) = ∫ φ̂(t) W(SO(even))(t) dt."

**ILS unconditional level-aspect 1-level support: η < 1, NOT η < 3/2.**

The η<2 number (Theorem 1.3) requires extra averaging over both k and N, not the level-aspect family used here.

**Agent claim (ILS η<3/2 unconditional) is WRONG.** Adversarial issue #4 confirmed.

## Net Impact on the 4/3 Headline

The headline "FAPC₂ unconditional at η₁+η₂ < 4/3" needs restriction.

The 4/3 derivation has two ingredients:
- **Off-diagonal piece (BD):** uses DFS Lemma 2.4 only. Threshold η₁+η₂ < 4/3 from PNT partial summation. ✓ Survives.
- **Diagonal-in-zeros subtraction:** needs unconditional 1-level density at support max(η_i). Available only for max(η_i) < 1 (ILS Thm 1.2).

**Surviving rigorous regime:** {(η₁, η₂) : max(η_i) < 1 AND η₁+η₂ < 4/3}.

Concretely:
- ✓ Symmetric η₁=η₂ < 2/3: full 4/3 sum-bound active.
- ✓ Symmetric η₁=η₂ ∈ [2/3, 1): cap is 2η < 4/3, so η < 2/3. **Same as symmetric symmetric corner = 2/3 still holds.**
- ✗ Asymmetric η₁ ≥ 1: dies (ILS doesn't cover diagonal).
- ✗ §6.1 push to 3/2: dies (relied on ILS η<3/2 which doesn't exist).

## Revised confidence

- Sub-region {max < 1, sum < 4/3}, FAPC₂ unconditional: **0.82** (accounting for residual unverified Lemma 2.6 m^ε question + N prime restriction).
- Full η₁+η₂ < 4/3 line: **0.50** (asymmetric corner unproved).
- §6.1 strengthening to 3/2: **0.20** (ILS citation wrong).
- §6.2 strengthening to 1.866: **0.30** (DFS Theorem 1.1 is 1-level, not directly 2-level; agent admits CS use which the §3 route avoided).

## Theorem B level-aspect impact

Per MASTER_KEY equivalence (CFKRS-ratios ⟺ FAPC₂ at η>1), the relevant FAPC₂ regime needs **η in some specific range** that's not just "η > 1" — need to check exactly what the equivalence demands:

- If equivalence needs η > 1 anywhere in the diagonal: surviving regime gives **0** (max < 1).
- If equivalence needs sum η₁+η₂ > 1 with each η_i ≤ 1: surviving regime gives the full needed range. ✓
- If equivalence needs sum η₁+η₂ > 1 with at least one η_i > 1: surviving regime gives **0**.

**Action needed:** re-read MASTER_KEY equivalence statement carefully to determine which case applies. Until then, Theorem B level-aspect lift is **CONDITIONAL ON THIS CHECK** at conf 0.50, not 0.92.

## Outstanding gaps

1. ILS Lemma 2.6 m^ε vs m^{1/4} — still need verbatim quote.
2. Squarefree composite N extension (16-curve ladder is composite squarefree, not prime).
3. CFKRS ⟺ FAPC₂ equivalence regime — needs precise re-check.

## Net verdict

**Partially landed.** The agent caught two real errors in MK1 (Θ_2 = 1.866 not 22/9; threshold structure). The new headline 4/3 has a real restricted regime where it holds rigorously. But the ILS η<3/2 claim was the agent's own fabrication, and the §6.1/§6.2 strengthenings depend on it. Net Theorem B level-aspect lift is uncertain (depends on equivalence regime check) — not 0.78→0.92, more likely 0.78→0.83 once the equivalence is properly read.

**Confidence on revised 4/3 sub-region result: 0.82 (was 0.92).**

## Key takeaway

This is a real partial advance, not a full unconditional Theorem B level-aspect closure. Adversarial review + direct PDF verification caught both an error in old work (22/9) and an error in new work (η<3/2). Net knowledge gained > zero.
