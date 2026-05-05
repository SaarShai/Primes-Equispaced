---
title: "BCL 2024 q-averaged route — does the (-4,4) support transfer to the Petersson weight aspect for Theorem B?"
author: Saar Shai
date: 2026-05-03
status: NEGATIVE — premise was wrong; BCL 2024 is GRH-conditional, not unconditional
related:
  - E1_E2_E3_barrier_attack.md (E3 = support-4 fixed level, open)
  - Theorem_B_field_landscape.md (claims BCL is unconditional — WRONG; this file corrects it)
  - Theorem_B_literature_research.md
sources:
  - arXiv:2310.07606v3 (Baluyot–Chandee–Li, "Low-lying zeros of a large orthogonal family of automorphic L-functions", 31 Aug 2024)
  - /tmp/bcl_2024.pdf, /tmp/bcl_2024.txt
verdict: HEADLINE FACT WAS WRONG. BCL gives support (-4,4) UNDER GRH (not unconditionally). The route as posed collapses immediately. A weaker route (different premise) discussed in §5–§7.
tags: [theorem-B, BCL-2024, low-lying-zeros, orthogonal-family, q-averaging, Petersson, GRH-bypass-FAILED]
---

# BCL 2024 q-averaged route — verdict

**One-line summary.** The user's premise — "BCL 2024 achieves support 4 for 1-level UNCONDITIONALLY in q-averaged family" — is **factually incorrect**. BCL 2024 Theorem 1.1 is explicitly stated **"Assume GRH"** (verbatim, line 215 of /tmp/bcl_2024.txt). The proposed route — "if Petersson weight aspect can be reframed as q-averaged in the right way, BCL gives support-4 unconditional → Theorem B unconditional" — does not exist, because BCL itself is not unconditional. **Route is closed.**

A secondary issue exists in `Theorem_B_field_landscape.md` line 83, which mis-characterized BCL as "support 4 (i.e., (-2,2) unconditional) for q-averaged family." That line is wrong on **both** counts: BCL's support is `(-4, 4)` (not `(-2, 2)`), and the result is GRH-conditional (not unconditional). This file should be corrected.

---

## Section 1 — Verbatim BCL 2024 main theorem

From /tmp/bcl_2024.txt L215–226:

> **Theorem 1.1.** *Assume GRH.* Let Φ be an even Schwartz function with Φ̂ compactly supported in (−4, 4). Then with notation as before,
>
>   lim_{Q→∞} OL(Q) = ∫_{−∞}^{∞} Φ(x) (1 + ½ δ₀(x)) dx,
>
> where δ₀(x) is the Dirac δ distribution at x = 0.

(Caveman quote; preserved verbatim per single-confidence rule.)

**Family setup** (L42–62, L168–212). Fix weight k ≥ 3. For each squarefree level q, let H_k(q) be the Hecke-newform basis of S_k(q). For Ψ smooth on R_{>0} with Ψ̂(0) ≠ 0, define

  OL(Q) := (1/N(Q)) · Σ_q Ψ(q/Q) · Σ_{f ∈ H_k(q)}^h Σ_{γ_f} Φ((γ_f / 2π) log q),

where N(Q) ≍ Q · Ψ̂(0). The h-superscript denotes the harmonic average (1.3): weighted by Γ(k−1) / ((4π)^{k−1} ‖f‖²).

**Conditional structure.** GRH is invoked twice in the proof:

1. **L1894 (verbatim):** "we use … GRH on L(s, sym²(f))". Used to bound the second sum in (4.6) — i.e., the contribution of `n = p^ℓ` with ℓ ≥ 2 in the sum-over-primes after the explicit formula.
2. **L1452, L4019 (verbatim L4019):** "follows from GRH (or Siegel's theorem, with an ineffective implied constant)". GRH for Hecke L-functions L(s,χ) and L(s,f) is used to bound the prime-sum Σ_{p≍P} (log p / √p) λ_g(p) by O(log² Q), where λ_g is a Hecke eigenvalue from a Maass form / Eisenstein-series basis after the Kuznetsov inversion.

The **central role** of GRH (L396, verbatim): "*In most cases, we can use an appropriate choice of basis and GRH to bound the resulting sums over p.*" GRH is essential to the (-4, 4) extension; it is not a trivial assumption that can be peeled off.

**Compare to Drappeau–Pratt–Radziwill 2020+** (L279–284, verbatim):

> Recently, Drappeau, Pratt and Radziwill [15] considered the one level density for the similar large family of Dirichlet L-functions attached to all primitive characters modulo q for all q ≍ Q and showed that the support of Φ̂ can be extended to be within (−2−50/1093, 2+50/1093) **unconditionally**. It remains a challenging problem to extend the support to something closer to (−4, 4) without additional hypotheses.

DPR 2020 is the **actual** unconditional support-extension result, and it gets only ≈ 2.046, not 4. The unconditional support-4 result the user thought existed does not exist in the literature as of 2024. The 2026 landscape file confused BCL with this DPR result.

---

## Section 2 — q-averaging structure and what it requires

BCL's q-averaging is the outermost sum `Σ_q Ψ(q/Q)` over **squarefree levels** q ∈ [Q/c₁, c₂Q] for some c₁, c₂ > 0 (smooth weight Ψ supported on [1/2, 3] is typical). The **family size** is

  Σ_q (Σ_{f ∈ H_k(q)} 1) ≍ Q² (since #H_k(q) ≍ q · (k/12) for fixed k, and Σ_{q ≍ Q} q ≍ Q²).

So this is a **Q²-size family** with conductors of size ≍ Q. The conductor-log scaling factor in the test function is `log q ≍ log Q`.

**What the q-averaging buys** (L228–254, paraphrased not quoted to respect copyright):

The key technical mechanism is the "complementary level trick" (L243–254): when bounding the off-diagonal Petersson sum after Kuznetsov, the q-sum allows an interchange that effectively replaces the modulus q ≍ Q by a smaller derived modulus c ≪ Q^{1−δ/2}, by a Poisson-summation-style move on the m,n,c indices. The geometric mean √(mn) versus arithmetic mean (m+n)/2 distinction is critical: at one-level density the relevant range is m ≍ Q^{4−δ}, n = 1, and √(mn) ≪ Q^{2−δ/2}, far smaller than (m+n)/2 ≍ Q^{4−δ}.

This is **structurally a q-aspect mechanism**, not a weight-aspect mechanism. The conductor of f ∈ H_k(q) is q, and the sum over f is naturally double-indexed: outer over q, inner over f|q. The q-average is what creates the 4-fold support extension because the new families being averaged have **different conductors**, allowing Poisson summation in the q-modulus.

**Required structural input for the BCL technology to apply:**

(R1) The L-functions in the family must be indexed by a parameter q (or pair (q, f|q)) such that the conductor scales with q, **and** the family has size ≫ q. (Necessary for the asymptotic large sieve / Poisson-in-q.)

(R2) The trace formula on the inner f-sum must produce **Kloosterman sums modulo cq** — i.e., the modulus must factor as `(level multiplier) × q` so that the q-sum can be interchanged with the c-sum.

(R3) After Kuznetsov inversion (which converts the Kloosterman sum back to a spectral sum on a different group of forms), the spectral parameter / new level must be ≪ Q^{1−δ}, i.e., the q-sum must allow a **non-trivial conductor reduction**. This is the heart of the gain.

(R4) GRH (used to bound the spectral sums Σ_{p≍P} (log p / √p) λ_g(p) ≪ log² Q for P ≍ Q^{4−δ}). **Without (R4), the support is at best (−2−ε, 2+ε)**, by the same large-sieve barrier as DPR 2020.

---

## Section 3 — Mapping attempts to Petersson weight aspect (5+ candidates)

Theorem B's required input is the on-line / at-zeros **second moment of L'(s, f)** for f in a single fixed family, with an asymptotic having an explicit constant tying down to 2/(3π) · log⁴ X. The Petersson family at issue is

  F = ⊔_k S_k^*(N), N squarefree fixed, k → ∞ (weight aspect)

or alternatively, with `k` fixed and `N → ∞` (level aspect, ILS family). Theorem B wants a **support-4 1-level density** statement (or the equivalent at-zeros conversion) for this family **unconditionally**. We attempt 5 mappings:

### 3.1 Candidate A — Direct: re-index the Petersson weight family by a fictitious "q"

**Idea.** Pretend k plays the role of q. Set q := k, sum Σ_k Ψ(k/K) f∈S_k^*(N).

**Problem.** The conductor of f ∈ S_k^*(N) is N (independent of k). So Σ_{k} (size of S_k^*(N)) ≍ Σ_k k/12 ≍ K². But the conductor stays at N. Requirement (R1) is satisfied in the **counting** sense (Q²-size family, K² forms) but not in the **structural** sense — the conductor doesn't scale with k. The Kloosterman sum from Petersson is mod c·N, not mod c·k. The complementary-level trick (R2) doesn't apply because the modulus carries N, not k. **Verdict: FAILS at (R2).**

### 3.2 Candidate B — Average over a SET of levels {N : N ≤ X squarefree}

**Idea.** Sum Σ_{N ≤ X, N squarefree} Φ((γ_f/2π) log N) over f ∈ S_k^*(N) at fixed weight k.

**This IS exactly the BCL setup**, with q = N. So if we want to apply BCL to "Theorem B in level-aspect family", we get support-(−4, 4) under GRH. The output is a family-averaged 1-level density statement for the level-aspect family, with the conductor playing the role naturally.

**Problem for Theorem B.** Theorem B's input requires the **second moment of L'(½+iγ_f, f)** over the family, not the 1-level density of γ_f. BCL controls the first moment of zeros (1-level density), not the second moment of L'. The translation 1-level-density → at-zeros-second-moment requires either (a) the explicit formula applied to a different test function (which gives at-zeros first moment of L'L̄', not second moment), or (b) 2-level density which BCL does not provide.

To get at-zeros second moment of L' from a level-density input, one needs **2-level density** at the corresponding support; BCL extends 1-level only. The 4-fold residue at the 2-fold shift level — the CFKRS step-6 issue (E2) — is not addressed by BCL's technology. **Verdict: FAILS — BCL extends 1-level density, but Theorem B needs at-zeros second moment of L', which is 2-level (or shifted-convolution at scale X²).**

### 3.3 Candidate C — Average over weights {k ≤ K}

**Idea.** Sum Σ_{k ≤ K} Σ_{f ∈ S_k^*(N)} … with N fixed.

**Problem.** Conductor independent of k (same as Candidate A); no q-aspect modulus to Poisson over. The Petersson trace formula at fixed N has Kloosterman sums S(m,n;cN) and Bessel J_{k−1}(4π√mn / (cN)). The k-sum hits the J_{k−1} only, and via the Bessel-to-Bessel reciprocity (Petersson's "spectral large sieve" in k-aspect), it gives at most an extra log K saving on the diagonal — **not** a 4-fold support extension. The k-aspect average is what ILS already use, and the result is support (−2, 2) under GRH per ILS Thm 1.1 (and (−1, 1) unconditional per ILS Thm 1.2). **Verdict: FAILS — k-aspect averaging is what ILS already exhausted, no new support extension.**

### 3.4 Candidate D — Twist by Dirichlet characters mod q, q ≍ Q

**Idea.** Sum over twisted L-functions `L(s, f ⊗ χ)` for χ mod q, q ≍ Q, with f ∈ S_k^*(N) fixed.

**Problem A.** The conductor of L(s, f ⊗ χ) is N · q² (for χ primitive mod q, (q, N)=1). So the conductor scales with q² — good for (R1).

**Problem B.** This is no longer the "Petersson family" of f; it's the **Rankin–Selberg twist family** of f. The L'(½+iγ_{f⊗χ}, f⊗χ) values are zeros of a different L-function each. To recover Theorem B's input — moments of L' for f over its **own** zeros — this twist average is irrelevant. **Verdict: WRONG OBJECT — even if BCL-style technology applied here (and it might, via Soundararajan–Young 2010 / Li 2024 / Kumar–Mallesham–Sharma–Singh 2023), the output is about twist-zeros, not f-zeros.**

### 3.5 Candidate E — Hybrid (k, N) average, k ≤ K, N ≤ Y

**Idea.** Sum Σ_{k ≤ K} Σ_{N ≤ Y, sqfree} Σ_{f ∈ S_k^*(N)} … — averaging over both weight and level.

**Problem.** Decomposes as outer Σ_k, inner Σ_N. The inner Σ_N is exactly Candidate B (BCL applies, support (−4, 4) under GRH). The outer Σ_k is a benign pre-average that doesn't change the conditional/unconditional status. The output is still a 1-level density statement, not the at-zeros 2-level / second-moment object Theorem B needs. Same verdict as B. Plus: doesn't help unconditionality — GRH is still required.

### 3.6 Candidate F — Kuznetsov + Bessel-decay + q-twist reformulation

**Idea.** Convert Petersson trace formula on f ∈ S_k^*(N) to Kuznetsov on the same family, then use a fictitious q-twist parameter.

**Problem.** Kuznetsov inverts the Petersson trace formula: it expresses ∆_q(m,n) (a sum over forms) as Kloosterman sums + Bessel transforms. Going the other way (from a single L'(½+iγ_f,f) sum over zeros to a Kuznetsov-inverted spectral sum) requires the explicit formula, which is GRH-controlled, plus a separate Kuznetsov step. There's no q-twist in the original problem, so the reformulation introduces a fictitious q that must be chosen — but the choice that makes the "complementary level trick" non-trivial requires the family conductor to actually scale with this q. As in Candidate A, fixed N means fixed conductor, and the trick fails. **Verdict: FAILS at the conductor-scaling step.**

---

## Section 4 — Best mapping (Candidate B) — full derivation of what BCL would buy

The **least bad** of the five candidates is Candidate B (3.2): take the Petersson family with **level varying** rather than weight varying — i.e., k fixed, N varies. This IS the BCL family. Under GRH, BCL gives support-(−4, 4) for the 1-level density. So:

**Result of applying BCL directly:** For the level-aspect family

  F_lev := { f ∈ H_k(q) : q ≍ Q, q squarefree },

the 1-level density of low-lying zeros has support (−4, 4) **under GRH** with the predicted Katz-Sarnak orthogonal kernel.

**Step 1 (translation to L' second moment, attempted).** From 1-level density to at-zeros first moment of L', use the explicit formula. From 1-level density to at-zeros **second** moment of L', one needs 2-level density. **BCL provides 1-level only.** Their §1 (L9, L236–237) explicitly anticipates higher moments (sixth, eighth) and 2-level as future work but doesn't deliver them.

**Step 2 (suppose 2-level were available, hypothetically).** If a 2-level density at support (−4, 4) under GRH existed for F_lev (it doesn't), then via the orthogonal Katz–Sarnak formula and the explicit-formula expansion, we could (in principle) extract the at-zeros second moment of L'. But this would be a **family-averaged second moment** Σ_q Ψ(q/Q) Σ_{f ∈ H_k(q)}^h |L'(½+iγ_f, f)|², not a per-form second moment. The Theorem B input is the **per-form** second moment with leading constant 2/(3π) · log⁴ X. The family-averaging dilutes the per-form constant — the average constant might or might not equal 2/(3π) · c_f's family average — and this is what E1+E2+E3 collectively address in the existing barrier analysis.

**Step 3 (S₄ + cage strengthening, original premise).** The user's note suggests that family-averaged at-zeros second moment, if achievable at support 4, plus the cage-strengthening argument from `RankinSelberg_trace_attack.md`, would close Theorem B. **This is plausible IF one had unconditional 2-level density at support 4 for F_lev.** That input does not exist:
- BCL gives 1-level at support 4 under GRH (not 2-level, not unconditional).
- 2-level for orthogonal Petersson at support > 2 unconditionally is OPEN.
- The level-aspect 2-level density (closest analog to BCL's q-aspect 1-level extension) is not in the literature as of 2026-05-03 to my knowledge from the read files.

**Step 4 (failure mode).** The chain is:

| Step | Status | Source |
|---|---|---|
| F_lev = level-aspect Petersson family with q ≍ Q | exists | standard |
| 1-level density at support (−4, 4) for F_lev | **GRH-conditional** | BCL Thm 1.1 |
| 2-level density at support (−4, 4) for F_lev | **OPEN**, not in BCL | — |
| at-zeros family-avg 2nd moment of L' from 2-level | conditional on prior | standard explicit-formula expansion |
| family-avg 2nd moment → per-form 2nd moment with constant 2/(3π) | conditional on density-of-zeros + cage | E1+E2+E3 unresolved |

**Each link in the chain is either unproven or GRH-conditional.** The route does not give Theorem B unconditional even if all the individual links worked under GRH — one would only recover Theorem B under GRH, which is the existing M-N (16) status.

---

## Section 5 — Verdict: does this lift Theorem B unconditional?

**No.** The route fails at the very first step: BCL 2024 Theorem 1.1 is itself **GRH-conditional**, not unconditional. The user's premise was incorrect. Even if it had been unconditional, the route would still require:

1. Lifting from 1-level density (BCL's output) to 2-level density (Theorem B's structural need) — OPEN.
2. Lifting from level-aspect to weight-aspect, OR accepting level-aspect family as the family for Theorem B — possible but changes the theorem statement.
3. Lifting from family-averaged second moment of L' to per-form second moment with the exact constant 2/(3π) — this is the E2/E3 barrier from `E1_E2_E3_barrier_attack.md` and is open.

**Cross-reference with prior 9 attacks (E1/E2/E3 barrier file, BCL_geq_0_*, FirstPrinciples, RankinSelberg, theorem-b-five-routes):**

| File | Attack route | Failure mode | Re-evaluated against BCL? |
|---|---|---|---|
| E1_E2_E3_barrier_attack.md | Direct unconditional E1+E2+E3 | E1 = X² shifted-conv unconditional OPEN; E2 = CFKRS step-6 OPEN; E3 = 2-level at support 4 OPEN | YES — BCL doesn't help E1 or E2; for E3 it gives only 1-level at support 4 under GRH |
| Theorem_B_field_landscape.md L83 | Mis-stated BCL as "support 4 unconditional" | wrong fact | THIS FILE CORRECTS IT |
| RankinSelberg_trace_attack.md | Cage refinement via Rankin-Selberg | Cage center 17/(12π); off-diagonal mass not pinned to 2/(3π) | NO — independent route, not affected |
| B_geq_0_petersson_attack.md / B_geq_0_dedekind_attack.md | Variants on Petersson family second moment | Same E1/E2/E3 barriers | NO — independent variants |
| FirstPrinciples_creative_attack.md | First-principles re-derivation | not BCL-related | NO |
| theorem-b-five-routes.md | Five routes overview | enumeration | reconfirms BCL is one of the dead paths |

**Conclusion.** This is **NOT a real lead.** The headline "BCL gives EXACTLY the support-4 we've been blocked on" is wrong about BCL's status (GRH-conditional), and it conflates 1-level with 2-level density. The route is closed.

---

## Section 6 — If yes, error term + final constant

N/A — see §5.

---

## Section 7 — Precise structural obstruction

The structural obstruction is **two-fold**:

### 7.1 Conditional status of BCL itself

BCL Theorem 1.1's proof uses GRH at L1894 (for L(s, sym²(f))) and at L4019 (for L(s, χ) Hecke L-functions, controlling Σ_{p ≍ P} (log p / √p) λ_g(p) ≪ log² Q with P ≍ Q^{4−δ}). Both are essential for the (−4, 4) support extension; without them, the unconditional ceiling drops to roughly the DPR 2020 level, ≈ (−2.046, 2.046), per the comparison in BCL §1 (L279–284).

**To remove GRH from BCL Thm 1.1**, one would need either:
- (a) an unconditional bound Σ_{p ≍ P} (log p / √p) λ_g(p) ≪_ε P^{ε} log² Q for P ≍ Q^{4−δ}, uniform in g over the spectral family — this is a deep prime-sum estimate equivalent in difficulty to a strong zero-free region for L(s, g);
- (b) a different proof of the (−4, 4) support that bypasses the prime-sum bound entirely — no known such proof.

Neither is plausibly in reach with current technology.

### 7.2 1-level vs 2-level wall

Even if BCL were unconditional, it gives **1-level density** with support 4. Theorem B's input — the at-zeros second moment of L'(½+iγ_f, f) — is structurally a **2-level density** statement (or equivalently, a shifted-convolution sum at scale X²). The 1→2 level lift requires either:

- new 2-level density technology for orthogonal Petersson at support > 2 — OPEN unconditionally and OPEN even under GRH at support > some threshold;
- direct shifted-convolution sums for λ_f(m)λ_f(n) at scale mn ≍ X² with logarithmic weights — OPEN per E1.

Both are at the same difficulty level as the unconditional fourth moment of GL(2) L-functions, which is **a genuine open problem in analytic number theory** (E1 file §2.1–§2.4 audit).

### 7.3 Per-form vs family-averaged

The third obstruction (E3 in barrier file) is that BCL-style results give family-averaged statements; Theorem B (M-N Conjecture 16) is **per-form**. Converting family → per-form requires either a strong density-of-zeros result (Selberg-type 1/N convergence) or GRH for the individual form. Neither is available unconditionally for the orthogonal Petersson family at the precision required (constant 2/(3π) with leading log⁴, not just upper-bound-with-correct-log-power).

**Net structural verdict:** BCL 2024 is a beautiful GRH-conditional q-aspect 1-level density extension. It does NOT structurally apply to the Petersson weight aspect (Candidate A,C,F fail at conductor scaling), and even where it applies (Candidate B = level aspect), it neither removes GRH nor lifts 1-level to 2-level. The "support-4 wall" for Theorem B is intact.

---

## Provenance

- /tmp/bcl_2024.pdf — downloaded from arXiv:2310.07606v3, 2026-05-03, 449457 bytes
- /tmp/bcl_2024.txt — pdftotext extraction, 5333 lines
- Direct verbatim quotations: L6–9 (abstract), L215–226 (Thm 1.1), L279–284 (DPR comparison), L396 (GRH centrality), L1894 (sym² use), L4019 (Siegel/GRH alternative)
- Cross-references read: `E1_E2_E3_barrier_attack.md` (full grep), `Theorem_B_field_landscape.md` (literature audit table)
- Single-confidence rule applied: the only claim made with high confidence is the verbatim quote of Thm 1.1 and the GRH-conditionality. All transfer-attempt verdicts are conditional on that reading.

## Action item

**Correct `Theorem_B_field_landscape.md` L83.** Currently reads (verbatim):

> Baluyot–Chandee–Li 2024 | Support 4 (i.e., (-2,2) unconditional) for q-averaged family | q-aspect averaging reduces to support-2 problem | arXiv:2310.07606

Should read:

> Baluyot–Chandee–Li 2024 | Support (-4,4) for q-averaged level family **under GRH** | Complementary-level trick + Kuznetsov; GRH used for prime-sum bounds and sym²(f) | arXiv:2310.07606

This audit error propagated the false impression that BCL was unconditional, which seeded the present (failed) attack vector.
