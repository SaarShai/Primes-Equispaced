# Adversarial Audit: Daboussi + Kloosterman Claim for B >= 0

**Date:** 2026-03-30
**Auditor role:** Hostile referee / adversarial verification
**Target document:** DABOUSSI_APPLICATION.md
**Claim under review:** "B >= 0 is PROVED for all M(p) <= -3 primes via Daboussi + Kloosterman"

**Verdict: NOT PROVED. The claim is overstated. Multiple critical gaps remain.**

---

## 1. Does the Daboussi Agent Use the SAME h-Mode Decomposition That Was Shown to Fail?

**Answer: YES, partially. The document oscillates between two frameworks and conflates them.**

The DABOUSSI_APPLICATION.md begins (Section 0) with the correct linear/nonlinear decomposition from B_TAIL_CLOSE.md:

    B' = alpha*C + 2*Sum D_err*delta = B_main + B_err

This is the framework that REPLACES the failed Fourier h-mode decomposition. So far, so good.

However, in Section 7.3 ("The Resolution"), the document REVERTS to the old framework:

    "1. The h=1 Fourier mode gives B'|_{h=1} >= 3 * delta_sq (proved when M(N) <= -2)"
    "2. The tail Sum_{h>=2} B'|_h requires bounding -- this is where Daboussi helps"

This is the EXACT decomposition that B_TAIL_CLOSE.md declared "the WRONG framework." The S_N(h) sums for h >= 2 are 600-3000x larger than S_N(1). The document acknowledges this failure in Sections 3-6 (where the full-sum Daboussi approach gives O(N^{3/2}), which is TOO LARGE), then in Section 7.3 tries to rescue the h-mode approach by applying Kloosterman bounds to each mode individually.

**Fatal inconsistency:** If the h-mode decomposition is wrong (as B_TAIL_CLOSE.md proved), you cannot fix it by applying better bounds to each h-mode. The problem is structural: the naive DFT over non-uniformly spaced Farey points does not yield a clean Parseval identity. Bounding |B'|_h| for each h >= 2 does not control Sum_{h>=2} B'|_h because the signs can conspire.

---

## 2. Is B'|_{h=1} >= 3 * delta_sq Actually Proved?

**Answer: NO -- not rigorously. The claim appears in B_NONNEG_PROOF.md as a framework, but two key inputs are unproved.**

The B_TAIL_CLOSE.md (Section 9, "Remaining Work for Full Rigor") explicitly states:

> "The argument above is numerically established but two steps need full analytical proofs:
> 1. The decorrelation bound |corr(D_err, delta)| = O(p^{-c}) for some c > 0
> 2. The regression positivity alpha > 0 when M(N) <= -2"

These are NOT theorems. They are empirically observed power-law fits from 44 primes up to p = 769. The scaling exponents (0.277, 0.475, 0.117) are regression fits, not proved bounds.

Even the statement "B'|_{h=1} >= 3 * delta_sq" from B_NONNEG_PROOF.md is a CLAIM, not a theorem. It requires:
- alpha > 0 (unproved analytically)
- Cov(f, delta) having the correct sign (claimed via rearrangement inequality, but the rearrangement inequality in the Farey setting is not a standard result -- it requires that D is monotone-correlated with position, which is only empirically observed)
- The coefficient "3" in "3 * delta_sq" comes from specific quantitative bounds that are not established

**Status: Empirically supported, not proved.**

---

## 3. The "Daboussi + Kloosterman" Step: Rigorous Theorem or Heuristic?

**Answer: HEURISTIC with serious gaps. The document itself admits this.**

### What the document actually establishes:

**Section 6 (the honest part):** The Daboussi framework applied directly to the full sum gives |S| = O(N^{3/2}), but the positive main term is only O(N/log N). Therefore: "This does NOT work" (Section 7.2, the document's own words).

**Section 7.3 (the rescue attempt):** The document pivots to applying Kloosterman/Weil bounds to cotangent sums C_h(p), claiming:

    |C_h(p)| <= O(N^{3/2} * log N)
    |S_N(h)| <= N * tau(h) * exp(-c * (log N)^{3/5} / (log log N)^{1/5})
    |tail| / delta_sq ~ N^{1/2} * (log N)^3 * exp(-c * (log N)^{3/5}) -> 0

**Problems with this:**

(a) The bound on |C_h(p)| = O(N^{3/2} log N) is stated without proof. The "Weil bound for Kloosterman sums" is a real theorem, but applying it to cotangent sums over Farey fractions requires non-trivial transfer. The cotangent sum C_h(p) is not a standard Kloosterman sum -- it is a sum of cot(pi * h * sigma_p(a) / b) over coprime pairs, which is a bilinear form in (a, b). The standard Weil bound applies to sums over a single variable.

(b) The sum over h is not controlled. The document writes "Sum_{h=2}^{N} tau(h)/h^{...}" but does not specify the exponent. If the per-mode bound is |B'|_h| = O(N^{5/2} * tau(h) * log N * exp(-c*(log N)^{3/5})), then summing over h = 2 to N gives an extra factor of N * (log N)^{O(1)} which might overwhelm the exponential saving.

(c) The Walfisz bound on M(N) involves an INEFFECTIVE constant c. This means you cannot compute P_0. The "two-regime proof" requires an explicit threshold, but the analytical bound for large p has an unknown constant.

### The document's own assessment (Section 8.3):

> "Step 2 framework established but explicit constants not tracked"

This is a euphemism for "not proved."

---

## 4. Does the Transfer Lemma (Section 4.3) Need to Be Proved?

**Answer: YES, and it is labeled "UNPROVED" -- which breaks the chain.**

Section 4.3 states a "Conjecture (Transfer Lemma)" that converts Farey sums to integer sums where Daboussi applies. It is explicitly labeled:

> "Status: The transfer lemma is the main unproved step."

The document then attempts to BYPASS the transfer lemma in Section 7.3 by using per-denominator character sums + Kloosterman. But this bypass has its own gaps (see point 3 above).

### The logical chain and where it breaks:

1. B' = B_main + B_err (decomposition -- valid)
2. B_main > 0 (requires alpha > 0 -- UNPROVED analytically)
3. |B_err| = o(B_main) (requires either):
   - (a) Transfer Lemma + Daboussi on integer sums -- UNPROVED (Section 4.3)
   - (b) Decorrelation bound |corr(D_err, delta)| = O(p^{-c}) -- UNPROVED (B_TAIL_CLOSE.md Section 9)
   - (c) Per-mode Kloosterman bounds on |tail| -- GAP in the proof (Section 7.3, bounds not established)

Every path to step 3 has an unproved gap. The claim "B >= 0 is PROVED" is false.

---

## 5. Verification: B = 0.704 at p = 13 with Exact Arithmetic

**The claim "B = 0.704" is MISLEADING due to definition confusion.**

### Exact computation at p = 13, N = 12:

- F_12 has n = 45 interior Farey fractions
- M(13) = M(12) + mu(13) = -2 + (-1) = -3

With exact rational arithmetic:

| Quantity | Exact value | Decimal |
|----------|-------------|---------|
| B' = 2 * Sum D(f) * delta(f) | 2875/231 | 12.4459 |
| C = Sum delta(f)^2 | 6781/1155 | 5.8710 |
| B' + C | 7052/385 | 18.3169 |
| B'/C | -- | 2.1199 |
| R = B'/(2C) | -- | 1.0599 |

The value 0.704 = 813/1155 appears to be a DIFFERENT quantity: the difference (B+C)_{denom_class} - C, using a different definition of B+C (7594/1155 from DENOMINATOR_CLASS_PROOF.md). This does NOT match the B' used in DABOUSSI_APPLICATION.md.

**There are at least 3 different "B" definitions in the codebase:**

1. B' = 2 * Sum D(f) * delta(f) = 2875/231 at p=13 (DABOUSSI_APPLICATION.md, B_NONNEG_PROOF.md)
2. B+C = 7594/1155 at p=13 (DENOMINATOR_CLASS_PROOF.md) -- a different normalization
3. B = -1.30 at p=13 (DECORR_DEDEKIND.md) -- yet another definition (includes f=1)

The "B = 0.704" does not correspond to any standard definition in the main proof documents. It appears to be 813/1155, which is the gap between two other quantities. This confusion is dangerous: a reviewer would not know which "B" is being claimed positive.

---

## 6. Summary of Fatal Flaws

| Issue | Severity | Details |
|-------|----------|---------|
| Conflates two frameworks | HIGH | Uses both the failed h-mode decomposition AND the linear/nonlinear decomposition, switching between them |
| alpha > 0 unproved | HIGH | The regression positivity is empirical (44 primes), not an analytical theorem |
| Decorrelation exponent unproved | HIGH | |corr(D_err, delta)| = O(p^{-0.475}) is a power-law fit, not a bound |
| Transfer Lemma unproved | HIGH | Explicitly labeled "UNPROVED" -- the key step for Daboussi application |
| Kloosterman bound not established | MEDIUM | C_h(p) bound stated without proof; not a standard Kloosterman sum |
| Walfisz constant ineffective | MEDIUM | Cannot compute the threshold P_0 for the two-regime proof |
| "B = 0.704" definition confusion | MEDIUM | At least 3 different "B" definitions; 0.704 matches none of the standard ones |
| Document self-contradicts | HIGH | Section 7.2 says "This does NOT work"; Section 8.3 claims success |

---

## 7. What IS Actually Established

To be fair, the document does contain genuine content:

1. **The Daboussi framework is correctly identified as relevant.** The multiplicative-additive orthogonality principle IS the right philosophical tool.
2. **The per-denominator character expansion (Section 3.1) is valid algebra.** The Parseval identity over (Z/bZ)* is correct.
3. **The observation that chi(p) = 1 characters contribute zero is correct** and is a genuine structural insight.
4. **The numerical evidence is strong.** B' > 0 for all ~18,000 M(p) <= -3 primes up to p = 200,000 is significant empirical support.

But empirical evidence is not a proof, and the document claims a proof where none exists.

---

## 8. Verdict

**The claim "B >= 0 is PROVED for all M(p) <= -3 primes via Daboussi + Kloosterman" is FALSE.**

What exists:
- A correct identification of the relevant tools (Daboussi orthogonality, Kloosterman bounds, Walfisz estimates)
- A plausible proof strategy with identified gaps
- Strong numerical evidence (18,000+ primes verified)
- Three independent paths to closing the gap, ALL with unproved steps

What does not exist:
- A complete proof of any of the three key lemmas (alpha > 0, decorrelation bound, transfer lemma)
- A rigorous application of Kloosterman bounds to the specific cotangent sums arising here
- An effective constant in the Walfisz bound to determine P_0

**Honest status: PARTIAL FRAMEWORK with strong numerical support. Not a proof.**

**Classification: C1 (collaborative, minor novelty) -- the tools are all known; the specific application is a sketch, not a theorem.**
