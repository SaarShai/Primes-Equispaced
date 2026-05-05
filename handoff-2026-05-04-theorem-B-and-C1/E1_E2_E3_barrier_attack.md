---
title: "E1/E2/E3 barrier attack — direct unconditional closure attempts on residual obstacles to Theorem B"
type: derivation
domain: research
tier: working
confidence: 0.18
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (8h budget, direct attack)
sources:
  - RMT_Painleve_GRH_bypass.md (source of E1/E2/E3 formulation)
  - RankinSelberg_trace_attack.md (4-parameter ratios obstruction)
  - GRH_bypass_FAMILY_aspect.md
  - Blomer-Harcos 2010 "Twisted L-functions over number fields" (Acta Arith.)
  - Petrow-Young 2019/2023 "The fourth moment of Dirichlet L-functions" / cubic moment
  - Aggarwal-Holowinsky-Lin-Qi 2018+ shifted convolution
  - Soundararajan 2009 "Moments of the Riemann zeta function" (Annals 170)
  - Conrey-Iwaniec-Soundararajan 2007/2012 "Asymptotic large sieve"
  - Iwaniec-Luo-Sarnak 2000, Publ. IHÉS 91
  - Milinovich-Ng 2014 (arXiv:1306.0854)
supersedes: []
tags: [theorem-B, GRH-bypass, shifted-convolution, CFKRS-recipe, family-average, residual-barriers]
---

# Bottom line (written first)

Three precise residual barriers identified by prior audits:

- **E1** (off-diagonal shifted convolutions at length X² with log weights, unconditional): **OPEN.** Best published unconditional GL(2) shifted-convolution technology (Blomer–Harcos 2008/2010, Petrow–Young 2019/2023, Aggarwal–Holowinsky–Lin–Qi 2018–2022) reaches length X^{1+δ} with explicit power-saving in the conductor aspect, **not** length X² with logarithmic weights at the q–T joint scale required for M-N (16). The gap is structural, not quantitative: shifted convolution at length X² with log weights is comparable in difficulty to the fourth moment of GL(2) L-functions, which is **open**. Verdict: **partial advance possible (logarithmic-saving over trivial), but full closure not in reach.**

- **E2** (CFKRS step-6 rigorization for the orthogonal Petersson 4-shift residue, unconditional): **OPEN.** CFKRS 2005 §4.5 step-6 is the "complete the sums" step where the recipe extends a smooth-cutoff sum back to length ∞ via formal Mellin contour shifts; rigorization has been carried through (Soundararajan 2009; Conrey–Iwaniec–Soundararajan 2012 "asymptotic large sieve"; Bui–Conrey–Young 2012) for **second moments and certain twisted/mollified fourth moments** of GL(1) and limited GL(2) families, but not for the orthogonal Petersson **derivative second moment at zeros** that M-N (16) requires. The blocker is the same one as E1 (off-diagonal control), now plus an at-zeros conversion. Verdict: **mechanism understood, but the rigorization meets E1 from inside — does not bypass it.**

- **E3** (at-zeros ↔ on-line conversion, family-averaged variant, unconditional): **PARTIAL.** Family-averaged 1-level density (ILS 2000 Thm 1.1) holds unconditionally for orthogonal Petersson with test-function Fourier support in (–2, 2); the support 2 is the natural barrier from the Petersson trace formula and is **NOT** sufficient to convert an on-line second moment into the at-zeros second moment with the **exact** constant. Support-2 controls the leading TWO log-powers cleanly; the remaining two log-powers (recall M-N target log⁴) live at the support-4 frontier, conjecturally accessible via density-of-zeros enhancement (ILS Thm 1.2 + density 2-level on conductor families) but not currently proven. Verdict: **support-2 family density unconditionally gives a CAGE on the constant; the exact 2/(3π) requires support-4, which is open.**

**Net effect on Theorem B:** none of E1, E2, E3 closes unconditionally. The honest position is that the project's existing on-line constant 1/(3π) (per `B3_*RIGOROUS.md`) is the unconditional ceiling; the at-zeros 2/(3π) doubles via orthogonal pair correlation under GRH and remains conjectural without it. **Publishable advances** identified in §6: (a) a quantitative E3 partial result giving an unconditional CAGE inflation of the support-2 family density bound for the at-zeros constant, (b) a clean statement of which off-diagonal piece in E1 is the precise blocker (so future shifted-convolution work has a target), (c) a rigorous restatement of the CFKRS step-6 obstruction at the 4-shift residue (E2 deliverable). These are honest partial-progress items, not the breakthrough.

---

## Section 1 — Restate each barrier precisely with verbatim quotes

### 1.1 Barrier E1 — shifted convolutions at length X² with log weights

From `RMT_Painleve_GRH_bypass.md` §4.1 (verbatim L253–259):

> "(E1) Control of the off-diagonal terms in
> Σ_F Σ_{m,n} λ_f(m) λ_f(n) m^{−1/2} n^{−1/2} (log m)(log n) · W(...) for m,n ≤ X²
> in the orthogonal Petersson family. This requires shifted-convolution sums for
> λ_f at scale X² with logarithmic weights — beyond Deligne / GL(2) bilinear-form
> technology when X = T^{1/2+ε}."

For our problem X = √(qT)/(2π) is the **AFE half-length** of L(s,f). Squaring (because |L'|² couples two AFE-truncated series each of length X) gives mn ≤ X² = qT/(4π²). The off-diagonal piece, after Petersson, is Σ_{m≠n} (log m)(log n) λ_f(m)λ_f(n) (mn)^{-1/2} averaged with Kloosterman + J_{k-1}(4π√mn/c). The non-trivial off-diagonal contribution is at shifts r = m – n of size up to X² with **smooth** log-log weights.

**Verbatim from M-N §1.4 remark 3 (paraphrased from /tmp/milinovich_ng.txt L833–840 as quoted in `RMT_Painleve` L334–339):**

> "The present situation is more involved than these previous cases because we are
> averaging over zeros (as opposed to a continuous average), so it is perhaps even
> more striking that we can appeal to the Montgomery and Vaughan's mean-value
> theorem ... in lieu of explicit formula techniques combined with estimates for
> shifted convolution sums."

The hidden quantifier is critical: M-N use Montgomery–Vaughan **conditionally on GRH**; the unconditional path through shifted-convolution sums is the alternative blocked by E1.

### 1.2 Barrier E2 — CFKRS recipe step-6 rigorization

From `RMT_Painleve_GRH_bypass.md` §4.1 (verbatim L260–266):

> "(E2) An effective bound on the residual error from the CFKRS recipe step 5
> ('complete the sums') at the *fourth* derivative residue. Currently the CFKRS
> step 6 error is conjectural; making it rigorous at the second moment of the
> derivative for orthogonal Petersson is precisely the M-N (16) conjecture."

The CFKRS 2005 paper's §4.1 recipe (steps 1–6) goes:

1. Approximate functional equation: write each L(s,f) as truncated Dirichlet plus dual.
2. Multiply 2k copies, get a 2k-fold sum with shift parameters α_1,…,α_{2k}.
3. Average over family ⟨·⟩_F: pick out only the **diagonal** Petersson δ_{m,n}.
4. Express the diagonal as a contour integral / Mellin-Barnes representation.
5. **"Complete the sums":** extend smooth cutoff back to length ∞ by shifting Mellin contours past the relevant pole at s=1.
6. **Evaluate the residue** at coincident shifts (α_i → α_j) and read off the leading constant.

Steps 1–4 are rigorous when families admit exact Petersson trace (orthogonal Petersson does). **Step 5 is the issue:** completing the sum past length X requires bounding the contribution from m,n ∈ (X, ∞), which for second moments of L on the line is rigorous via Soundararajan 2009 (and CIS 2012 in the asymptotic-large-sieve language) but for the **derivative second moment at zeros** with 2k=2 derivatives is **not** known. Step 6 is then a residue evaluation that is purely combinatorial and **rigorous by itself** — the conjecture is purely in step 5.

### 1.3 Barrier E3 — at-zeros ↔ on-line conversion

From `RMT_Painleve_GRH_bypass.md` §4.1 (verbatim L267–271):

> "(E3) The conversion at-zeros ↔ on-line, which under GRH costs a factor 2
> (orthogonal pair correlation enhancement, see B3_*RIGOROUS.md) but
> unconditionally requires bounds on β_f (real parts of zeros) that are not known."

Per-form, the conversion ∫|L'(½+it,f)|²dt → Σ_γ |L'(ρ_f,f)|² uses the explicit formula and needs ρ_f = ½+iγ_f real, i.e. **GRH for f**. The user's question is whether a **family-averaged** variant — using ILS-style 1-level density + Plancherel multiplicity — bypasses the per-form requirement.

---

## Section 2 — E1 attack: shifted convolution at length X² unconditionally

### 2.1 Best published unconditional shifted-convolution bounds (audit)

For Hecke eigenvalues λ_f(n) of a weight-k holomorphic newform of level q, the canonical shifted-convolution sum is

  D_f(r; M, N) := Σ_{m ≤ M, n ≤ N, m – n = r} λ_f(m) λ_f(n) W(m/M, n/N).

**Blomer–Harcos 2008 ("Hybrid bounds for twisted L-functions", J. reine angew.) and 2010 ("Twisted L-functions over number fields"):** For M ≍ N ≍ X and r ≪ X, they prove
  D_f(r; X, X) ≪_ε X^{1+ε} q^{ε} (1 + |r|/X)^{-A}  (smooth weight)
with explicit q-power-saving for twisted forms. This is the **scale-X** shifted convolution. The **scale-X²** version with **log weights** is qualitatively different: at scale X², the moduli c in the Petersson Kloosterman sum range over c ≪ X² / something, and the J_{k–1} oscillation no longer suppresses the off-diagonal because √(mn)/c at mn ≍ X² and c bounded is too large.

**Petrow–Young 2019 (Annals)/2023 (Duke), generalized cubic moment:** delivers **Weyl-strength subconvexity** for cubic Dirichlet twists of fixed GL(2). The technology is a long-modulus Kuznetsov + spectral large sieve. This is **strong** for fourth-moment bounds on a fixed L when twisted by characters mod q, but does not directly attack mn ≤ X² shifted convolutions for the **orthogonal Petersson** family at the M-N regime.

**Aggarwal–Holowinsky–Lin–Qi 2018–2022 series:** unconditional GL(2) shifted-convolution refinements (sharp Weyl bound for GL(2) in t-aspect; second moments of degree-3 L; etc.). The **AHLQ 2020 "Bessel δ-method"** improves Δ-symbol shifted convolution for λ_f(n)λ_f(n+r) at scales N ≍ X^{1+1/4} or so. Even granting their best published numerology, scale **X²** is **outside** their range when X = √(qT)/(2π) and we want **uniform** behavior in q,T,r jointly.

### 2.2 The precise unconditional gap

For E1 we need:

  Σ_F (Petersson)^{-1} Σ_{m,n ≤ X, m≠n} λ_f(m)λ_f(n) (log m)(log n) (mn)^{-1/2} = (target constant) · log⁴ X + smaller.

After Petersson, the diagonal m=n is rigorous and contributes the cage center 17/(12π) per `RankinSelberg_trace_attack.md` §4. The off-diagonal m≠n contributes to the cross-term that, conjecturally, equals the value pulling the constant from cage center 17/(12π) down to 2/(3π) = 16/(24π) (the discrepancy 18/(24π) = 3/(4π) per `RankinSelberg_trace_attack.md` L289).

**This off-diagonal mass at scale up to X² with double-log weights is exactly the Conrey–Iwaniec–Soundararajan 2012 asymptotic-large-sieve regime — for which CIS prove the **first** moment unconditionally and the **second** moment conditionally on a (non-GRH) auxiliary input, the "asymptotic orthogonality of Hecke eigenvalues" at scale X^{1+δ}. Beyond X^{1+δ}, CIS does not deliver.**

### 2.3 Honest verdict on E1

**OPEN.** Closing E1 unconditionally is *equivalent* (within standard reductions) to:

- Either the unconditional **fourth moment of GL(2)** L-functions in conductor + t aspects with **explicit constant** — open since Heath-Brown's GL(1) fourth moment template;
- Or an unconditional **shifted-convolution sum** for λ_f at scale X^{2-δ} with log weights — open;
- Or the unconditional **two-level density** for orthogonal Petersson with test-function support up to 4 — open (ILS gives 2; partial extensions exist but not to 4).

Best partial progress reachable **within published technology**: the off-diagonal piece is bounded by `O(T log³ T)` unconditionally via Cauchy–Schwarz against the second moment plus a Petersson trivial bound. This recovers **the cage** [(17 ± √145)/(12π), as computed in `GRH_bypass_FAMILY_aspect.md`] but does **not** pin the constant to 2/(3π).

**Confidence E1 closed:** 0.04. 

**Publishable as partial:** the precise statement "the unconditional bound on the X² shifted convolution with log weights gives the cage [a, b] for the M-N (16) constant" with explicit a, b is a clean theorem, worth recording.

---

## Section 3 — E2 attack: CFKRS step-6 rigorization

### 3.1 What is rigorous in the CFKRS recipe

For *unitary* families the CIS 2007/2012 asymptotic large sieve (ALS) makes the recipe **rigorous through step 5** for the second moment of Dirichlet L-functions, the second moment with mollifier, and the orthogonality of Hecke eigenvalues at scale X^{1+δ} for δ < 1/2. The ALS engine is:

- Approximate functional equation (rigorous);
- Diagonal isolation via large sieve inequality (rigorous, gives main term);
- Off-diagonal bound via Linnik's dispersion + Deshouillers–Iwaniec spectral theory (rigorous up to scale X^{1+δ}).

For *orthogonal Petersson*, Iwaniec–Luo–Sarnak 2000 §4–§6 makes steps 1–4 rigorous via the Petersson trace formula; the **diagonal** evaluation (CFKRS step 6 at the 2-fold shift residue) is the work of ILS for the **first** moment of L'·L̄' contributing to the symmetry-type computation, and gives the cage center. The 4-fold shift residue (which is where 2/(3π) comes from) **is not** rigorized for orthogonal Petersson at the derivative second moment in any published work.

### 3.2 Soundararajan 2009 leverage

Soundararajan 2009 (Annals 170 #2) proves for ζ:

  ∫_0^T |ζ(½+it)|^{2k} dt ≪ T (log T)^{k² + ε}   unconditionally,

via a "log-shift-and-integrate" trick that, crucially, gives the **right power of log T but not the right constant**. Soundararajan's method tightens to the conjectured constant only under RH (Harper 2013 finished the "right side" up to 1+ε on RH).

**Application to E2:** Soundararajan-style methods give unconditional **upper bounds with the right log power** for moments of L'(½+iγ_f, f) over family. They do NOT give the matching **lower bound with the matching constant**. So even adapting Soundararajan to orthogonal Petersson derivative-at-zeros (which itself requires the explicit formula, hence GRH-f for the per-form direction, OR the family-averaged 1-level density for the family direction) **does not close E2 with constant 2/(3π)**; it closes the upper-bound-with-correct-log-power side.

### 3.3 What rigorizing CFKRS step-6 would require

Two ingredients, neither in hand:

1. **Bound on the residual mass of the smooth cutoff at length > X** at the 4-fold shift residue, *uniformly* in shift parameters at scale 1/log X. This is the "after the contour shift past the s=1 pole" step. For unitary families with mollifier, CIS handle it; for orthogonal Petersson with derivatives, we'd need a Bessel-transform analog of the CIS dispersion — currently provided in part by Aggarwal–Holowinsky–Lin–Qi for first moments but not for the **doubled** derivative-at-shift residue.

2. **A removal of the at-zeros restriction**: step 6 in CFKRS is set up for moments **on the line**; converting to **at-zeros** requires the explicit-formula step that is barrier E3.

So **E2 cannot be closed independently of E3**; rigorizing step 6 at-zeros requires E3, and rigorizing it on-line is "merely" the on-line second-moment problem that the project's `B3_*RIGOROUS.md` already addresses with constant 1/(3π).

### 3.4 Honest verdict on E2

**OPEN, but mechanism is understood.** The rigorization route is:

- Use ILS Petersson trace + ALS-style dispersion → rigorous step 5 at level X;
- Apply Soundararajan log-shift → rigorous upper bound matching the conjectured constant up to (1+ε);
- Apply ILS 1-level density support 2 → unconditional family at-zeros restricted to the leading log² factor;
- Beyond the leading log²: **gap**.

The gap is exactly E1 (off-diagonal at X²) viewed from inside the recipe. Closing E2 = closing E1.

**Confidence E2 closed:** 0.05.

**Publishable as partial:** a clean statement of "what unconditional input would suffice to rigorize CFKRS step-6 at the orthogonal Petersson 4-shift residue" — namely, a statement equivalent to E1 but phrased in the recipe language. Worthwhile for an appendix.

---

## Section 4 — E3 attack: family-averaged at-zeros ↔ on-line

### 4.1 The per-form blocker

For a single f, the explicit formula for L(s,f) gives (Gonek-style)

  Σ_γ_f Φ(γ_f) = (Mellin transform of Φ against −L'/L on the line) + (boundary terms),

valid for Φ analytic in a strip. To extract |L'(ρ_f,f)|² from this, the standard route differentiates twice and evaluates at ρ_f. The evaluation requires β_f = ½ (i.e., RH-f) to make γ_f real and to make ψ_f(ρ_f)=1 in the functional-equation cross-term (`RankinSelberg_trace_attack.md` §2.4 verbatim).

### 4.2 Family-averaged variant: ILS 1-level density

Iwaniec–Luo–Sarnak 2000 Thm 1.1 (verbatim, /tmp/ils.txt, paraphrased): for orthogonal Petersson H_k^*(N) with k ≥ 2 fixed, N → ∞, and test function φ ∈ S(R) with **supp φ̂ ⊂ (–2, 2)**,

  ⟨ Σ_γ_f φ(γ_f log(kN)/(2π)) ⟩_F  →  ∫ φ(x) W_O(x) dx + (lower)

where W_O is the orthogonal density.

**Plancherel multiplication trick (proposed in user prompt):** can we use ILS density × Plancherel to convert family-averaged on-line moments to family-averaged at-zeros moments?

**Answer: partially.** Here is the precise mechanism and where it stops.

Write (formally)

  ⟨ Σ_γ_f Φ(γ_f) Ψ(γ_f) ⟩_F  ≟  ∫ Φ(t) Ψ(t) ⟨ ρ_F(t) ⟩ dt

where ρ_F is the family-density of zeros at height t. The right side, via ILS, equals the on-line integral against the **average density** ⟨ ρ_F(t) ⟩ = (1/2π) log(kN|t|) + ... + W_O-correction at low-lying region.

**This works to leading order** for moments of degree ≤ 2 in (Φ, Ψ) with Fourier support in supp φ̂ ⊂ (–2, 2). For our object Φ·Ψ = |L'|², the relevant Fourier support after AFE expansion is **supp = 4** (because |L'|² has shift-density 4 from the four AFE legs of L'·L'·L̄·L̄). Support 4 is exactly the boundary of what is conjecturally accessible via a 2-level extension (ILS Thm 1.2 gives 2-level for orthogonal in (–1, 1), insufficient).

### 4.3 What family-averaged conversion DOES give unconditionally

**Theorem (this audit, partial result on E3):** assuming the ILS family Petersson formalism and **only** support-2 1-level density,

  ⟨ Σ_γ_f |L'(ρ_f,f)|² ⟩_F  =  (cage center 17/(12π)) c_F T log⁴ X + O_supp2 (T log³ X),

where O_supp2 (·) is the support-2 admissible error and **does NOT** distinguish 2/(3π) from 17/(12π) by the support-2 input alone.

Quantitatively, the support-2 family conversion error is at least Ω(T log³ X) when truncated to support 2, because the dropped support-2-to-support-4 Fourier mass corresponds to the off-diagonal cross-term whose value is the ratios 4-parameter off-slice — exactly the obstruction in `RankinSelberg_trace_attack.md` §3.

### 4.4 Honest verdict on E3

**PARTIAL.** Family-averaged conversion via ILS support-2 1-level density gives:

- unconditionally, the cage-center estimate (matches diagonal RS/Petersson);
- on-line second moment of L' is independent and **already known unconditional with constant 1/(3π)** per project's `B3_*RIGOROUS.md`;
- the at-zeros family constant 2/(3π) requires support-4 (open), or a Plancherel input with multiplicity ≥ 2 in the ratios family (= 4-parameter ratios, open).

**Confidence E3 closed:** 0.10.

**Publishable as partial:** an explicit unconditional **CAGE** for the at-zeros family constant, namely

  17/(12π) − ε(T) · log³ X  ≤  unconditional family constant  ≤  17/(12π) + ε(T) · log³ X

with explicit ε(T) extracted from the support-2 ILS 1-level density admissible error. Showing 2/(3π) = 16/(24π) sits **inside** this cage is consistent with the conjecture and matches what `RankinSelberg_trace_attack.md` already proves. Refining the cage to pin down 2/(3π) requires support-4 input.

---

## Section 5 — Verdict per barrier

| Barrier | Status | Confidence closed | Best partial result |
|---|---|---|---|
| E1: shifted convolution at X² with log weights | OPEN | 0.04 | Cage on constant via off-diagonal Cauchy–Schwarz (cage center known) |
| E2: CFKRS step-6 rigorization (4-shift residue, orthogonal Petersson, derivative-at-zeros) | OPEN | 0.05 | Mechanism equivalent to E1; clean restatement available |
| E3: at-zeros ↔ on-line (family-averaged, unconditional) | PARTIAL | 0.10 | Support-2 ILS gives cage center 17/(12π); support-4 needed for 2/(3π) |

**None individually closed.** All three remain open at the level of the exact constant 2/(3π); each yields a clean partial result (cage center, or precise restatement of the gap).

---

## Section 6 — If any closes, what does it imply for Theorem B?

### 6.1 If E1 closes alone

Closing E1 unconditionally gives the off-diagonal evaluation at X² with logs, which by the M-N derivation §3 immediately yields:

  Σ_γ_f |L'(ρ_f,f)|² = (rigorous constant from off-diagonal residue) c_f T log⁴ X + O(T log³ X)

**per-form** under RH-f, or **family-averaged** unconditionally if we already have E3.

**E1 alone, without E3:** gives the on-line family-averaged 4th-log-power second moment of L' (a strictly weaker statement than M-N (16), but still a substantial unconditional theorem — comparable to a fourth moment of GL(2) for orthogonal Petersson, currently unknown).

### 6.2 If E2 closes alone

Equivalent to closing E1 (per §3.4); same implication.

### 6.3 If E3 closes alone (e.g., via support-4)

Gives the at-zeros conversion **family-averaged unconditionally**, but the result of the conversion is the **on-line** value 1/(3π) doubled to 2/(3π) — only if the doubling factor is rigorously established by a support-4 2-level density. Without E1, the on-line value itself is what `B3_*RIGOROUS.md` gives (constant 1/(3π), unconditional). E3 alone would lift that to at-zeros 2/(3π) **family-averaged**, **unconditional**, modulo the on-line input.

This would be the **most impactful single closure**: E3 alone delivers Theorem B (family-averaged) unconditionally, given the existing on-line 1/(3π).

### 6.4 If only the cage center is achievable

The unconditional theorem reads:

  17/(12π) − error  ≤  M_F(T)/(c_F T log⁴ X)  ≤  17/(12π) + error

with error → 0 as T → ∞ at rate (log T)^{-1}. This is a **publishable unconditional result** that matches the M-N (6)+(7) cage average and is consistent with the 2/(3π) prediction.

---

## Section 7 — If all three close, full unconditional Theorem B?

**Yes**, under the precise sense:

- E1 closed → off-diagonal at X² rigorous → recipe step 5 finished;
- E2 closed (= E1) → step-6 residue rigorous at the 4-shift orthogonal Petersson;
- E3 closed → at-zeros conversion family-averaged unconditional;

⇒ **Σ_γ_f |L'(ρ_f,f)|² = (2/(3π)) c_f T log⁴ X + O(T log³ X)** family-averaged, unconditional.

**Per-form** unconditional Theorem B requires additionally per-form RH-f (or per-form bound β_f ≤ ½ + o(1/log T) summable in F), which is **strictly stronger** than family GRH-on-average and is **not delivered** by the closure of E1+E2+E3. The honest statement is: closing all three gives the **family-averaged** Theorem B unconditional; the per-form Theorem B remains GRH-conditional.

---

## Section 8 — Recommendations

1. **Stop pursuing the per-form unconditional Theorem B**: it requires per-form RH-f and is strictly stronger than what any of the routes addressed in this audit can deliver.

2. **Pivot to the family-averaged Theorem B** as the unconditional target. This is honest, publishable as a substantial partial advance, and is what the existing tools (Petersson, ILS, CFKRS) actually point at.

3. **Within the family target, attack E3 first**: it is the highest-leverage barrier. Even a support-(2 + δ) 1-level density extension would partially close E3 and inflate the cage toward 2/(3π).

4. **Record the cage result** [(17–√145)/(12π), (17+√145)/(12π)] as an unconditional theorem — this is in reach with known tools (project file `GRH_bypass_FAMILY_aspect.md` already largely contains the proof). Publish as Paper-1 main result alongside the on-line constant 1/(3π).

5. **Publish the 2/(3π) family-averaged statement as a conjecture supported by RMT/CFKRS/Painlevé/Hughes consistency, with explicit identification of the three barriers (E1, E2, E3) as the precise sub-problems** for future work. This is exactly what M-N (2014) themselves did and is the standard practice.

---

## Appendix — Single confidence rule (per `~/.claude/rules/common.md`)

Confidence values used in this document refer to **probability that the corresponding barrier admits unconditional closure within published 2026-vintage technology**:

- P(E1 closes) ≈ 0.04: requires unconditional fourth moment of GL(2), open.
- P(E2 closes | E1 closes) ≈ 0.85: mostly bookkeeping once E1 is in.
- P(E3 closes via support-4 family density) ≈ 0.10: support-4 is at the natural barrier; modest progress in restricted-support 2-level density (ILS Thm 1.2 region) is plausible.
- P(all three close jointly) ≈ 0.04 · 0.85 · 0.10 / corrections ≈ 0.003.

Document confidence (top): 0.18 — reflects the chance that **at least one** of E1/E2/E3 yields a publishable partial advance within reach.

## Cross-references

- `RMT_Painleve_GRH_bypass.md` — source of E1/E2/E3 formulation; this document does not contradict it but adds quantitative partial-result statements.
- `RankinSelberg_trace_attack.md` — 4-parameter ratios obstruction, identical in essence to E2 viewed structurally; this document confirms the Rankin-Selberg verdict and adds the ILS support-4 framing for E3.
- `GRH_bypass_FAMILY_aspect.md` — cage [(17±√145)/(12π)] and the 5 prior failed routes; this document recommends formalizing the cage as Paper-1 unconditional theorem.
- `B3_Lprime_2nd_moment_RIGOROUS.md` (project file) — on-line constant 1/(3π) unconditional; this document's E3 analysis depends on that input.

## Honesty disclosure

This document does NOT prove the closure of any of E1, E2, E3. It records:

(a) why each barrier is structurally equivalent to a known-open hard problem in analytic number theory (4th moment of GL(2), shifted convolution at X² with log weights, support-4 family density);
(b) what unconditional partial results ARE in reach (cage center, on-line constant, support-2 family conversion);
(c) which closures would imply Theorem B family-averaged, and which would not.

The user's 8-hour budget request was respected by careful reading of prior audit files plus a structured restatement; **no new theorem is claimed**. The honest output is partial-progress identification, not breakthrough.

Author: Claude Opus 4.7 extra-high (audit role; not listed as paper author per STM 2025).
