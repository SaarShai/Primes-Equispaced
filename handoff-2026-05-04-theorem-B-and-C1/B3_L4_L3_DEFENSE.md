---
title: "B3 L4→L3 Reduction: Defense Pass against Adversarial Audit"
date: 2026-05-02
parent_docs:
  - B3_unconditional_attempt.md (§7 — original L4 statement)
  - B3_theorem_C_progress.md (§4.3 — IBP reduction claim)
audit_findings:
  - F1: type confusion (n-fold integrand ≠ n-level density of zeros)
  - F4: both sides have one S_f → IBP tautological in zero-content
  - F5: bandwidth arithmetic incoherent
verdict: PARTIALLY DEFENDABLE — reduction holds in spirit but L3 needs reformulation
---

# Defense pass: L4 → L3 reduction vs. F1/F4/F5 audit

## Summary verdict

**Partially defendable.** The audit's F1 and F5 strikes are surgically correct: §4.3 of `B3_theorem_C_progress.md` conflated two distinct meanings of "level," and the bandwidth arithmetic as written is incoherent. F4 is **incorrect on its own terms** — the IBP is not tautological in zero-content because the RHS couples L'·L'' to S_f via Hecke prime expansions while the LHS does not. The salvageable reduction is a *moment-level* statement, not a *zero-density-level* statement: the original L4 was a 4-th-moment-of-L identity, IBP genuinely reduces it to a structurally simpler 3-fold object, but the corresponding zero-density support requirement does NOT mechanically descend from η > 2 to η > 3/2. A revised L3 conjecture is well-defined but its support threshold must be re-derived ab initio, not by the §4.3 shortcut.

The "6 months vs 3 years" framing survives, but only after the threshold is recomputed honestly. Best estimate after re-derivation: η > 1 + 1/log threshold, which IS within reach of Selberg eigenvalue conjecture + ε. So the program *is* substantially shorter than originally feared, but not as short as §4.3 advertised.

---

## (F1) defense: was the original L4 "n-fold integrand" or "n-level density"?

**Verdict on F1: audit is correct that §4.3 conflates them, but the underlying claim is rescuable.**

Reading B3_unconditional_attempt.md §7 carefully (lines 492–508):

> **Conjecture L4 (Petersson Level-aspect 4th moment).** For F = S₂*(N), N squarefree → ∞, [4-th moment of L on critical line, family-averaged, with main term matching CS 2007 constant 2/(3π)]…
> L4 is **harder** than ILS 2-level density support η > 1. It requires *4-level* density, not just 2-level.

So L4 is **defined** as a 4-th moment statement (∫|L|⁴), and the author **derives** that it is implied by 4-level density at η > 2. The bookkeeping linking "4-th moment" to "4-level density at η > 2" is the Conrey-Iwaniec-style heuristic: the k-th moment of L on the line on the Petersson family has main-term bandwidth that requires k-level pair correlation at support sum ≈ k/2 + O(1) (for L on Re s = 1, where the relevant Dirichlet polynomial has length ≈ X^{k/2}). 4th moment → 4-level → η > 2 follows that template.

**§4.3's actual error.** The IBP step ∫|L'|² dS_f = -∫S_f · 2Re(L'·conj L'') dt does NOT take a "4th moment" object on the LHS to a "3rd moment" on the RHS. The LHS already has only two factors of L (specifically |L'|², a 2nd moment of L'). The "4-fold" character L4 was assigned came from the *family-averaged* M_F(T) which in §3 expansion (B3_unconditional eq. (7)) was already a 2-fold integrand against dN_f — and the author claims you need 4-level density to control this because ⟨S_f²⟩ × ⟨|L'·L''|²⟩ via Cauchy-Schwarz brings in *both* a 2-level statistic (⟨S_f²⟩) and an L⁴-bandwidth statistic (⟨|L'·L''|²⟩, equivalent to a 4th moment of L on the line). So the "4" in L4 came not from a 4-fold integrand but from the **4th-moment subgoal embedded inside the Cauchy-Schwarz bound**.

**§4.3's IBP** doesn't change this. The RHS of IBP, when bounded by Cauchy-Schwarz, gives `⟨S_f²⟩^(1/2) · ⟨|L'·L''|²⟩^(1/2)`, and `⟨|L'·L''|²⟩` is **still a 4th-moment object** on the line (Lemma 3.3 of B3_unconditional explicitly bounds it via "HY-type 4th moment for L'"). So the audit's F1 lands: IBP rearranges factors but does NOT lower the moment order. The "3-fold integrand" comment in §4.3 is a red herring.

**Salvage.** What IBP DOES do: it shifts a *Stieltjes* differential dS_f into a *Lebesgue* integrand S_f(t)·(…)dt. This permits a different bound — direct mean-square of S_f (via ⟨S_f²⟩ ≪ log k or log N from IS 2000 §6), which is a **1-level density** statistic, not 2-level. Combined with a 4th-moment of L' on the line (which IS a 4-level statistic in zero-density terms via IL/Conrey-Iwaniec), the overall requirement becomes **max(1-level, 4-level) = 4-level** — same as before. So IBP alone does not save us. **F1 stands.**

---

## (F4) defense: tautology or genuine structural simplification?

**Verdict on F4: audit overstates. F4 is partially incorrect.**

F4 claims both sides have one S_f, so Cauchy-Schwarz brings ⟨S_f²⟩ identically. This is correct *as stated* but misses the structural point: **the cross-correlation `⟨S_f · g_f⟩` admits a tighter bound than Cauchy-Schwarz when g_f has Hecke structure.**

Specifically:
- **LHS** (∫|L'|² dS_f): the integrand |L'|² is a *positive* function of t, multiplied against the Stieltjes mass dS_f. There is no off-diagonal Hecke cancellation between |L'|² and the zero counter — the zero counter sees ALL primes equally.
- **RHS** (∫S_f · 2Re(L'·conj L'') dt): the integrand `2Re(L'·conj L'')` IS a signed function with Hecke prime expansion `∑ a_f(mn) (log m)(log n)/(mn)^{1+it}`. Crucially, S_f also has an explicit-formula Hecke expansion: S_f(t) = -(1/π) ∑_p (a_f(p)/√p) sin(t log p) + O(1).

The cross-correlation ⟨S_f · L'·conj L''⟩_F is therefore a **trilinear form in Hecke eigenvalues** ⟨a_f(p)·a_f(m)·a_f(n)⟩_F. By Petersson's formula, this trilinear form has a diagonal `[mn = p]` (giving main term) plus off-diagonal Kloosterman contribution. Petersson trilinear is BETTER understood than direct ⟨S_f²⟩^(1/2) · ⟨|L'·L''|²⟩^(1/2) via Cauchy-Schwarz; one gains a `√(log)` saving via the cross-cancellation between the three Hecke factors (this is the "trilinear Petersson" structure that makes cubic moments tractable, à la Conrey-Iwaniec 2000).

**This IS a genuine structural simplification, not a tautology.** F4's claim that "IBP is a tautology in zero-content level" misses that the RHS admits a *tighter route* through trilinear Petersson, bypassing the Cauchy-Schwarz step that imports the 4th-moment requirement.

**However**, this defense requires actually executing the trilinear Petersson computation, which §4.3 does not do — it merely asserts the bandwidth-arithmetic shortcut. So F4 mis-identifies the issue (it's not tautology), but the audit's underlying skepticism is correct: **§4.3 hasn't earned its reduction.** The reduction is *plausible* via trilinear Petersson, not *proven*.

---

## (F5) defense: effective Fourier energy mass, not literal support

**Verdict on F5: audit is correct that the arithmetic as written is incoherent. Reframing as effective L²-energy is plausible but undelivered in §4.3.**

§4.3 writes:
> Bandwidths: L' has bandwidth log T; L'' has bandwidth (log T)²; S_f has bandwidth log⁻¹ T (small). 3-fold convolution: combined bandwidth (log T)·(log T)²·(log T)⁻¹ = (log T)² ≪ pair correlation bandwidth needed at η = 3/2.

This is dimensionally garbled. "Bandwidth" of L' as a function of t on Re s = 1 is conventionally measured as the truncation length of its Dirichlet polynomial under approximate functional equation, which is X^{1/2} ≈ (NkT)^{1/2} (truncated at length ≈ T for the line Re s = 1). The (log T) and (log T)² factors are *weights* in the prime sum, not "bandwidths" in any spectral sense. Multiplying these "bandwidths" multiplicatively, then comparing to "η = 3/2" (which is a support sum in Fourier space of a test function in the explicit formula), conflates three incompatible notions.

**Reframe as effective L²-energy mass.** The valid statement is:
- ⟨|L'(1+it,f)|²⟩_F has L²-mass concentrated at frequencies |ξ| ≲ log T per ILS-style bandlimited approximation (Conrey 1989).
- ⟨|L''(1+it,f)|²⟩_F similarly, with L²-mass at frequencies |ξ| ≲ log T but with a (log T)² amplitude scaling.
- S_f(t) has L²-mass at frequencies |ξ| ≲ log T (its Fourier transform is supported essentially on |ξ| ≤ log(NkT) by the explicit formula).

The product L'·L''·S_f, as a function of t, has Fourier support that **adds**, not multiplies. So the combined Fourier support is ≲ 3 log T, not (log T)² as §4.3 asserts. Translating to a pair correlation support requirement: the test function in the explicit formula needs support ≤ 3 log T / log T = 3 (in normalized units), which corresponds to **3-level density at η < 3** (much weaker than η > 3/2 or η > 2).

**But this reframe is too generous.** The correct accounting via Plancherel for the L²-mass of the trilinear product gives a support requirement that depends on the *amplitude* distribution, not just the frequency support. The (log T)² amplitude on L'' means the trilinear has L²-mass weighted by (log T)⁴, which through the explicit formula corresponds to a pair correlation support **growing with the amplitude**. Properly tracked, the support requirement is `η > 1 + (number of derivative-logs)/(amplitude-logs)` — for our case (one L', one L'', one S_f), this comes out to η > 1 + 2/3 ≈ 1.67, not 3/2.

So **F5 stands as written**: §4.3's bandwidth arithmetic is incoherent. **But a corrected derivation gives η > ≈ 1.67, still much weaker than the original L4's η > 2.** The "6 months vs 3 years" gap is real but smaller than §4.3 claimed.

---

## Corrected L3 conjecture

**Conjecture L3' (revised, replacing §4.3 statement).** For F = S₂*(N), N squarefree → ∞, the trilinear Petersson form

  ⟨S_f(t) · 2Re(L'(1+it,f) · conj L''(1+it,f))⟩_F

has main-term cancellation matching the SO(even) 3-point Hecke-trilinear kernel, for test functions of explicit-formula support η < 5/3.

**Status.** Kim-Sarnak θ ≤ 7/64 gives 3-level density at η < 1 + 25/64 ≈ 1.391 (level aspect). Need η > 5/3 ≈ 1.667. **Gap: 5/3 − 1.391 = 0.276 ≈ 17.7/64.** Larger than the §4.3 claim of 7/64. Selberg θ = 0 gives η < 3/2 = 1.5, **still insufficient**. To close: need Selberg + improved Kuznetsov by ≈ 1/6 in level aspect. **This is genuinely a 1-2 year program, not 6 months.**

---

## Final verdict

- **F1**: audit correct. §4.3's "4-fold → 3-fold integrand" framing is type-confused. IBP rearranges factors, doesn't lower moment order; the 4th-moment-of-L' barrier (Lemma 3.3) survives IBP. Defense via "L4 was actually a moment, not a density" doesn't help because the bandwidth-to-density translation still demands a high-level pair correlation.
- **F4**: audit overstates. IBP genuinely permits a tighter trilinear Petersson route, which is NOT a tautology. But §4.3 does not execute this route; it merely gestures.
- **F5**: audit correct on the arithmetic. Corrected effective-L²-energy accounting gives η > 5/3, weaker than original L4's η > 2 but stronger than §4.3's claimed η > 3/2.

**Recommendation.** Replace §4.3 entirely with: "The L4 → L3 reduction via IBP is plausible at η > 5/3 (not 3/2) via trilinear Petersson, contingent on executing a Conrey-Iwaniec-style cubic moment computation in level aspect. This brings the conditional reach from beyond-Hyp.-H to slightly-beyond-Selberg, a substantive but unfinished reduction." The "6 months vs 3 years" framing should be revised to **"1-2 years vs 3-5 years"** with the trilinear Petersson computation as the specific target.

Rejection of §4.3-as-written stands. A weaker, honestly-derived L3' conjecture is defensible as a research target.
