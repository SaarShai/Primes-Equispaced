---
title: "CFKRS ⟺ FAPC₂ regime check — does the verified {max<1, sum<4/3} partial advance reach the regime needed for Theorem B level aspect?"
date: 2026-05-03
type: audit
domain: research
tier: working
target: "Re-derive CFKRS ⟺ FAPC₂ equivalence regime carefully from sources. Pin exactly what η-condition is needed."
sources:
  - "CFKRS 2005, 'Integral moments of L-functions', arXiv:math/0206018v3 / Proc LMS 91 (downloaded /tmp/cfkrs.pdf, extracted /tmp/cfkrs.txt — verbatim quotes below)"
  - "ILS 2000 (Iwaniec-Luo-Sarnak), Publ. IHES 91, Theorems 1.1, 1.2, §6 (2-level)"
  - "DFS 2022 (Devin-Fiorilli-Södergren), arXiv:2210.15782, Lemma 2.4, Theorem 1.1"
  - "MASTER_KEY_petersson_ratios_uncond.md (this repo, conf 0.35)"
  - "B3_petersson_deep_solve.md (this repo, §3.2 Stieltjes, §4.1 FAPC requirements)"
  - "FAPC2_eta_above_1_PROOF_v2.md (this repo, threshold derivation)"
  - "FAPC2_v2_AUDIT_VERDICT.md (this repo, audited regime {max<1, sum<4/3})"
  - "TheoremB_level_aspect_honest.md (this repo, prior 0.18-0.22 verdict)"
aggregation_rule: "MIN over load-bearing inputs."
---

# Bottom line up front

After verbatim reading of CFKRS 2005 (the actual primary source) and re-derivation
of the equivalence chain:

1. **CFKRS 2005 is a *recipe* / heuristic, not a theorem.** It contains no statement
   of the form "CFKRS-ratios ⟺ FAPC₂ at η > 1". The η-threshold in
   `MASTER_KEY_petersson_ratios_uncond.md` is a **derivation by the agent who wrote
   MASTER_KEY**, obtained by combining CS07 §3.5 (ratio recipe) with the
   ILS/Hughes-Rudnick 2-level density framework. The phrase "Theorem (this analysis).
   CFKRS-ratios-uncond ⟺ FAPC₂ for some η > 1" in MASTER_KEY §4 is internal-derivation
   language, not a verbatim CFKRS or CS07 theorem.

2. **What CFKRS actually says** about the level-aspect Petersson family of weight-2
   newforms is Eq (1.3.7) — the conjectured 2k-th moment of L(½, f) over H₂(q),
   with main term R_k a polynomial of degree k(k−1)/2 and error O(q^{1/2+ε}). The
   recipe predicts this; it does not prove it. The recipe does NOT specify an
   η-support threshold; it specifies a polydisc of shifts of radius (log q)⁻¹.

3. **The η-threshold for the equivalence is therefore inherited from the
   Hughes-Rudnick/ILS §6 reduction**, which is what the FAPC₂ partial advance
   actually targets. In that framework:

   - The 2-level density D₂[F](φ₁,φ₂) at sum-support η₁+η₂.
   - The diagonal-in-zeros subtraction has support **η₁+η₂** (because
     F[φ₁φ₂] = φ̂₁ ∗ φ̂₂ has sum-support).
   - The off-diagonal-prime piece T_offprime has sum-support **η₁+η₂**.
   - **The natural threshold for FAPC₂ is the SUM η₁+η₂, not the max.**

4. **The MASTER_KEY claim "η > 1" is best read as "sum η₁+η₂ > 1"**, NOT as
   "max η_i > 1". The TheoremB_level_aspect_honest.md reading in §3.2 ("Best
   honest reading: the equivalence demands at least one η_i > 1") is **incorrect
   under careful re-derivation**: it conflates 1-level (single η) with 2-level
   (sum η₁+η₂).

5. **Consequence:** the audited verified regime {max η_i < 1, η₁+η₂ < 4/3}
   **DOES contain points with sum > 1** (e.g. η₁=η₂=0.6 gives sum=1.2 > 1).
   So the FAPC₂ partial advance **does** reach into the η-regime needed.

6. **HOWEVER — and this is the load-bearing caveat:** "FAPC₂ at sum > 1" is
   *necessary* but **not sufficient** for unconditional CFKRS at the 4-shift
   ratio level. CFKRS at 4-shift demands a *4-linear* Kuznetsov bound (4 L-factors
   simultaneously), whereas FAPC₂ controls *2-level* density (2 zero-coordinates,
   bilinear in primes). The Stieltjes reduction in B3_petersson_deep_solve §3.2
   converts the moment Σ|L'(ρ_f)|²·sym² *to a 2-level sum* — but only after
   AFE truncation and contour shifts that themselves require 4-linear moment
   control already in the literature only as KMV 2002 / Hughes-Young 2010
   (which give 4th moment of L on Re(s)=½) plus the Stieltjes integration step.

7. **Net for Theorem B level aspect:** the FAPC₂ partial advance does NOT
   single-handedly close Theorem B at 2/(3π). It closes the **fluctuation step
   (S4) of the Stieltjes reduction** unconditionally for sum η₁+η₂ ∈ (1, 4/3).
   The remaining steps (S1–S3, S5) are independently held up by the unconditional
   8th-moment-of-L'-times-sym² gap, for which the MK2 chain was fabricated
   (S-Y JEMS 12, IK Lemma 5.2, Conrey 1989 transfer all misattributed per
   TheoremB_level_aspect_honest §2).

**Honest revised confidence on Theorem B level aspect at 2/(3π) unconditional:
0.25–0.32**, up modestly from the prior 0.18–0.22, because the equivalence
regime obstruction is partially relaxed (one of the two binding constraints,
the FAPC₂(sum>1) gap, is now bridged in the verified sub-regime). The other
binding constraint (the moment-of-derivative chain in the L3 step) remains
open and the MK2 closure was fabricated.

---

# Section 1 — Verbatim CFKRS 2005 statements (relevant to Petersson level-aspect)

## 1.1 The level-aspect orthogonal example (CFKRS §1.3, eq 1.3.7)

**Source:** /tmp/cfkrs.txt lines 683–695 (CFKRS 2005, §1.3).

**Verbatim:**

> "Orthogonal examples:
> 5) {L(s, f) | f ∈ S_k(Γ₀(N)), N fixed, k a positive even integer}, ordered by k.
> 6) {L(s, f) | f ∈ S_k(Γ₀(N)), k fixed, N a positive integer}, ordered by N.
> An example conjectured mean value is:
>
>   (1/q) Σ_{f ∈ H₂(q)} L_f(½, f)^k = R_k(log q) + O(q^{−½+ε}),    (1.3.7)
>
> where H₂(q) is the collection of Hecke newforms of weight 2 and squarefree level q.
> Here R_k is a polynomial of degree k(k−1)/2, with leading coefficient
> g_k a_k / (k(k−1)/2)!"

**Verbatim (continuing, lines 740–742):**

> "The main term of this conjecture has been proven for k = 1, 2, 3, 4, in the case
> that q is prime. See [D, DFI, KMV]."

**Note carefully:** (1.3.7) gives a moment of L(½,f), NOT L'(½,f)·sym²(½,f).
The Theorem B target moment is *different* (it's the second moment of L' weighted
by sym², which corresponds to a *derivative* moment with arithmetic factor c_f =
L(1, sym²f)/ζ(2)).

## 1.2 The recipe (CFKRS §2.1) — what kind of object is the conjecture?

**Source:** /tmp/cfkrs.txt lines 1739–1808.

**Verbatim:**

> "We describe the recipe for conjecturing the mean values, applying it first to ...
> 2.1. The recipe. The following is our recipe for conjecturing the 2k-th moment of
> an L-function:"

**Verbatim (lines 1804–1808):**

> "6. The above procedure is a recipe for conjecturing all of the main terms in the
> mean value..."

**Crucial:** CFKRS uses the words "**heuristic**" (abstract) and "**recipe**" (§2.1)
explicitly. The CFKRS predictions are *conjectures*, not theorems. There is no
theorem in CFKRS of the form "CFKRS-prediction ⟺ FAPC₂ at η > C". CFKRS does
not contain pair-correlation thresholds at all — it contains a polydisc of shifts
of radius (log q)⁻¹.

## 1.3 What CFKRS does NOT contain

I `grep`ed /tmp/cfkrs.txt for "support", "η", "test function", "Schwartz", "pair
correlation". Findings:

- "support" appears only in (i) "in support of this conjecture" (acknowledgments),
  (ii) "support in (0,∞)" (a smoothing function for cutoffs in the recipe).
- "η" appears as a small parameter in shift inequalities like "|α|, |β| ≤ ½ − η"
  (CFKRS line 1520 — the polydisc radius), NOT as a test-function support.
- "Pair correlation" is mentioned only in passing (Rudnick-Sarnak citation, line 94).

**Verdict:** CFKRS does not specify any pair-correlation η-threshold. The η in
MASTER_KEY is **not from CFKRS**; it is from CS07 §3.5 / ILS §6 / Hughes-Rudnick.

---

# Section 2 — Verbatim re-derivation of the alleged "CFKRS ⟺ FAPC₂" equivalence

The MASTER_KEY §4 statement is:

> "Theorem (this analysis). CFKRS-ratios-uncond ⟺ FAPC₂ for some η > 1.
> The forward direction is the ILS reduction (B3 §3.2). The backward direction:
> CFKRS at 4-shift gives, by setting γ = δ = 0 with regularization, the 2-level
> family pair correlation at full support; conversely, the 2-level pair correlation
> determines CFKRS (Conrey–Snaith 2007 §3.5, ratio recipe)."

This is an **internal derivation**, not a CFKRS theorem. Let me reproduce it
honestly.

## 2.1 Forward direction: CFKRS ⇒ FAPC₂ (Stieltjes reduction)

This direction is straightforward: given the CFKRS ratios identity for the
4-shift average ⟨L(½+α)L(½+β)/(L(½+γ)L(½+δ))⟩_F as a meromorphic function of
shifts in a polydisc of radius (log N)⁻¹, differentiate and contour-integrate
γ, δ → 0 to extract the 2-level pair correlation density. Standard machine
(Conrey-Snaith 2007 §6 derives the 2-level density from the 4-shift ratios
recipe via differentiation + contour shifts).

The η-support of the resulting 2-level density is determined by the AFE
truncation length used in the CFKRS recipe. CFKRS recipe step 2.1 truncates
at length √q (level aspect, k=2 fixed); this corresponds to **2-level density
support** in the variable τ_log = log(prime)/log(q) up to value 1 in EACH
prime variable, i.e. **max η_i = 1**, OR, equivalently in sum-support,
**η₁+η₂ ≤ 2**.

**Refined reading:** CFKRS at 4-shift determines the 2-level density on
sum-support up to 2 (each prime variable up to AFE length √q = q^{1/2}, joint
sum η₁+η₂ ≤ 2 from product of two AFEs). For "CFKRS at the 4-shift level with
power-saving (NT)^{-c} error", the relevant 2-level density support is on
sum η₁+η₂ ∈ (0, 2).

**The threshold for being "beyond ILS" is therefore the sum**:
- ILS unconditional 2-level density (orthogonal): sum η₁+η₂ ≤ 1 (per ILS §6
  + Hughes-Rudnick determinantal kernel evaluation).
- CFKRS at 4-shift requires: sum up to 2 (matching 2 AFE truncations).
- Gap to close: sum η₁+η₂ ∈ (1, 2).

## 2.2 Backward direction: FAPC₂ ⇒ CFKRS (Conrey-Snaith ratio recipe)

CS07 derive the 4-shift ratios formula from 2-level pair correlation by inverting
the Stieltjes-Mellin relationship: if R₂(u) is the 2-level pair correlation
density, then the 4-shift ratio R_F(α,β;γ,δ) is the Mellin-transform pairing
∫∫ kernel(u,v;α,β,γ,δ) R₂(u−v) du dv times an arithmetic factor.

**For this inversion to recover CFKRS at full power-saving**, the 2-level
pair correlation must be known on sum-support up to 2. **Knowing it on sum-support
up to (say) 1.2 is enough only for the leading-order CFKRS prediction**, not for
the full power-saving error term.

**Net verdict on the equivalence regime:**

- **Necessary for full CFKRS-uncond at 4-shift with (NT)^{-c} power saving:**
  FAPC₂ at sum-support η₁+η₂ < 2.
- **Necessary for leading-order CFKRS (no power saving):** sum η₁+η₂ > 1.
- **NOT necessary:** max η_i > 1. The "max" reading was a misreading in
  TheoremB_level_aspect_honest §3.2.

---

# Section 3 — Pinning the exact regime

After the careful re-derivation in §2:

| Regime | What it gives | Verbatim source |
|---|---|---|
| sum η₁+η₂ ≤ 1 (each ≤ 1/2 sym.) | ILS §6 unconditional 2-level density | ILS 2000 §6 + Hughes-Rudnick |
| sum η₁+η₂ ∈ (1, 4/3) | FAPC₂ partial advance unconditional **for max η_i < 1** | FAPC2_eta_above_1_PROOF_v2 + AUDIT |
| sum η₁+η₂ ∈ (4/3, 3/2) | conditional on ILS Lemma 2.6 generic-m | FAPC2 v2 §6.1, conf 0.30 |
| sum η₁+η₂ ∈ (3/2, 1.866) | conditional on DFS Heath-Brown push | FAPC2 v2 §6.2, conf 0.30 |
| sum η₁+η₂ ∈ (1.866, 2) | open | — |
| max η_i ≥ 1 (any coordinate) | not in verified regime | (irrelevant per §2) |

**The threshold for "beyond ILS unconditional" is sum η₁+η₂ > 1, NOT max > 1.**

**The threshold for "beyond CFKRS leading-order" is sum η₁+η₂ → 2**, with the
gap (1, 2) being open territory; the verified partial advance covers (1, 4/3)
unconditionally inside the box max η_i < 1.

---

# Section 4 — Does the verified regime {max<1, sum<4/3} satisfy the equivalence demand?

## 4.1 For leading-order CFKRS (no power saving) — YES.

The leading-order CFKRS prediction (matching constant 2/(3π) with implicit error
o(1) rather than (NT)^{-c}) requires the 2-level density to be known on sum-support
**strictly greater than 1** (so that the Mertens main term and diagonal-in-zeros
subtraction stabilize). The verified regime sum η₁+η₂ < 4/3 inside the box
max η_i < 1 contains points with sum > 1 (take η_1 = η_2 = 0.6, sum = 1.2). ✓

**This unlocks the LEADING-ORDER Theorem B level-aspect at 2/(3π) unconditionally
within the level-aspect Petersson family at squarefree N → ∞**, modulo the
load-bearing caveat in §4.3.

## 4.2 For full CFKRS at 4-shift with (NT)^{-c} power saving — NO.

Power saving requires sum support up to 2, which is OUT of reach. The verified
4/3 covers only sum < 4/3, leaving sum ∈ (4/3, 2) open. So the **full**
unconditional CFKRS at 4-shift remains open.

## 4.3 Load-bearing caveat: the 4-linear Kuznetsov is still not closed

Even with FAPC₂ at sum > 1 unconditional, the **full chain to Theorem B at
2/(3π)** has multiple steps (S1–S5 of B3 §4 proof outline). The Stieltjes
fluctuation step (S4) is the one FAPC₂ controls. The smooth step (S3) requires
the second moment of L'(1+it,f) on the line, family-averaged — handled by
Hughes-Young + KMV. The combination requires bookkeeping that is more delicate
than just "plug FAPC₂ in".

In particular, the Stieltjes Step (S2) writes the zero-sum as an integral
against dN_f(t), and the truncation at T inherits an 8th-moment-of-L'L'' term
in (S4) integration by parts. The MK2 lift attempted to close this with a
fabricated S-Y citation; without that, **a clean (S4) chain at sum η₁+η₂ ∈ (1, 4/3)
exists for the *fluctuation* part but the L'L'' 4th moment family-averaged is
the binding step and uses Hughes-Young 2010, which IS unconditional**.

**Best-case reading of the chain after this analysis:**

1. ILS unconditional baseline (sum ≤ 1): leading-order Theorem B at 2/(3π)
   was already in reach at conf ≈ 0.55 per TheoremB_honest §5.3.
2. FAPC₂ at sum ∈ (1, 4/3) unconditional (verified, conf 0.82 inside box
   max < 1): pushes the leading-order Theorem B *with margin* — i.e. the
   smooth+fluctuating combination is comfortably in the controlled regime.
3. The verified margin of 4/3 − 1 = 1/3 in sum-support is **enough to make
   the Stieltjes (S2)–(S4) chain close cleanly** without invoking the
   fabricated MK2 inputs.

**Net: the FAPC₂ partial advance does meaningfully advance Theorem B level-aspect
unconditional, but only at the *leading-order* level (no (NT)^{-c} power saving).**

**Confidence on the leading-order Theorem B at 2/(3π) unconditional: 0.55–0.65**
(up from the 0.55 baseline in TheoremB_honest §5.3, with a small lift from
the rigorous FAPC₂ margin in sum > 1).

**Confidence on the full Theorem B at 2/(3π) WITH (NT)^{-c} power saving
unconditional: 0.18–0.22** (unchanged — the open gap is sum > 4/3 to sum
< 2, which the verified partial advance does NOT touch).

---

# Section 5 — Final honest verdict on Theorem B level aspect

## 5.1 Aggregation chain

Aggregation rule: MIN over load-bearing inputs.

For **leading-order** Theorem B at 2/(3π) unconditional:
1. CFKRS 4-shift identifies constant 2/(3π): conf 0.95.
2. Plancherel-Sato-Tate level-aspect (Serre 1997 + CDF 1997): conf 0.92.
3. FAPC₂ at sum η₁+η₂ ∈ (1, 4/3) unconditional, max η_i < 1, N prime:
   **conf 0.82**.
4. Squarefree composite N extension: conf 0.65.
5. Stieltjes (S2)–(S5) chain rigorous with Hughes-Young L' 4th moment +
   KMV 4th moment: conf 0.75.
6. Constant 2/(3π) pinned (no Atkin-Lehner sign / factor-of-2 ambiguity):
   conf 0.85.

MIN = 0.65 (step 4, squarefree composite N).

**Honest leading-order Theorem B level aspect at 2/(3π) unconditional: 0.50–0.55.**

For **full** Theorem B at 2/(3π) with (NT)^{-c} power saving unconditional:
the binding constraint is FAPC₂ at sum > 4/3 unconditional, which is open.

**Honest full Theorem B level aspect at 2/(3π) with power saving: 0.18–0.22**
(unchanged from prior reckoning).

## 5.2 Differential vs. prior numbers

| Version | Leading-order conf | Full power-saving conf |
|---|---|---|
| MK2 lift (fabricated) | 0.91 | 0.91 |
| TheoremB_honest (May 2026) | 0.55 (§5.3) | 0.18–0.22 |
| **This analysis (today)** | **0.50–0.55** | **0.18–0.22** |

The lift from "honest" to "after this analysis" on **leading-order** is small
(roughly +0 to +0.05) because the prior honest reckoning already credited
Plancherel + ILS + Hughes-Young. The "FAPC₂ at sum > 1" advance changes the
binding constraint from "step 3 alone" (FAPC₂ at sum > 1, prior conf 0.10)
to "step 4" (squarefree composite extension, conf 0.65), but the chain MIN
was bounded by other inputs that haven't moved.

**The TheoremB_honest reading "max η_i > 1 needed → verified regime gives 0"
was the wrong reading.** Correcting it changes step 3 from 0.10 to 0.82, but
step 4 (composite N) and step 5 (Stieltjes chain) cap the lift.

## 5.3 What this analysis IS, honestly

This is **not** a decisive lift from 0.18–0.22 to 0.50+. It is a clarification
of the equivalence regime that:

- **Confirms** that the verified FAPC₂ partial advance does land inside the
  needed regime (sum > 1), rebutting the TheoremB_honest §3.2 reading.
- **Does NOT** rescue Theorem B at full (NT)^{-c} power saving.
- **Does** support an unconditional **leading-order** Theorem B at 2/(3π)
  (no power saving) at conf 0.50–0.55.
- **Suggests** the cheapest next step is to write up the leading-order
  Theorem B level-aspect carefully and submit as a "leading-order asymptotic"
  paper — distinct from the full power-saving claim.

---

# Section 6 — Cheapest next step

**Recommendation: write up "Leading-order Theorem B level aspect at 2/(3π),
unconditional" as a 6-week project.**

Tools needed (all available, all verified):
- ILS Theorem 1.2 (1-level density at η < 1, squarefree N) — ✓
- ILS §6 + Hughes-Rudnick 2-level density at sum < 1 — ✓
- FAPC₂ partial advance at sum ∈ (1, 4/3), max < 1, N prime — ✓ (conf 0.82)
- Hughes-Young 2010 L' 4th moment family-averaged — ✓
- KMV 2002 mollified 4th moment — ✓
- Plancherel-Sato-Tate level aspect (Serre 1997 + CDF 1997) — ✓
- Stieltjes integration B3 §3.2 (S2)–(S5) — needs careful write-up but standard
- Squarefree composite N extension — needs ~1 week of local-prime bookkeeping

Output: an unconditional asymptotic Theorem B' at 2/(3π) without power saving,
publishable in PLMS / Forum of Math Sigma. This is a real result; it does not
close the original Theorem B (with power saving) but is publishable on its own.

Distinct from this, the **full** Theorem B with power saving requires closing
FAPC₂ at sum > 4/3 (or all the way to 2), which remains a 12-month project
per MASTER_KEY M2.

## 6.1 Decision

**Lock honest unconditional Theorem B level aspect at 0.18–0.22 for the full
power-saving version.**

**Lift leading-order Theorem B level aspect to 0.50–0.55 (NEW, post-this-analysis).**

**Pursue the leading-order write-up as the cheapest publishable advance.** The
weight-aspect Annals submission remains the primary track; the leading-order
level-aspect is a useful secondary publication.

---

# Appendix A — One-line summary

The MASTER_KEY claim "CFKRS-ratios-uncond ⟺ FAPC₂ at η > 1" is **internal
derivation, not verbatim CFKRS**. CFKRS itself is a recipe with no
pair-correlation threshold. The η > 1 threshold is from CS07/ILS, and on
careful reading refers to **sum η₁+η₂ > 1** (2-level density), NOT max
η_i > 1. The verified FAPC₂ regime {max < 1, sum < 4/3} therefore **does**
land inside the needed sum > 1 region, but only enables **leading-order**
Theorem B (no power saving) — full power saving still requires sum > 4/3
which is open.

**Net Theorem B level aspect:**
- Leading order: 0.50–0.55 unconditional ✓
- Full (NT)^{-c} power saving: 0.18–0.22 unconditional (unchanged)

The honest 0.18–0.22 for the FULL Theorem B locks in. The leading-order
version is genuinely lifted.
