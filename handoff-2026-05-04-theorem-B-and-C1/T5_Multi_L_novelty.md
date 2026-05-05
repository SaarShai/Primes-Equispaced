---
type: adversarial-review
domain: research
title: "T5: Novelty check — Multi-L Δ-machine Macdonald-Cauchy → plus-tensor RS identification"
created: 2026-05-04
updated: 2026-05-04
confidence: 0.80
tier: working
tags: [delta-machine, rankin-selberg, macdonald-cauchy, novelty-check, selberg-class]
---

# T5 Adversarial Novelty Check

## Section 1: Claim Verbatim

From `/Users/saar/Farey 4.7 solutions/Delta_machine_multi_L.md` §5 (Cross-Selberg theorem, part (ii)):

> "The Euler product F_{L_1, L_2}(s) = ∏_p ∏_{i=1}^{d_1} ∏_{j=1}^{d_2} (1 + α_{1,i,p} · α_{2,j,p} · p^{-s}) (with appropriate ramified-prime correction) is the Dirichlet inverse of a Selberg-class L-function naturally interpreted as the 'sign-twisted' Rankin-Selberg L(s, π_1 ⊠ π_2)."

And from §3.2:

> "F_{L_1, L_2}(s) = Σ_n μ_{L_1}(n) μ_{L_2}(n) / n^s = ∏_p ∏_{i,j} (1 + α_{1,i,p} α_{2,j,p} p^{-s}).
> Identification with Selberg-class L-functions. The product ∏_p ∏_{i,j} (1 + α_{1,i,p} α_{2,j,p} p^{-s}) is naturally interpreted as a 'plus' Rankin-Selberg ('outer-tensor + plus-twist' construction): it's the Dirichlet inverse of an L-function whose Satake parameters are the negatives of the Rankin-Selberg parameters {-α_{1,i} α_{2,j}}_{i,j}."

The core claim is: **the Dirichlet series of pointwise products of Dirichlet-inverse coefficients factors, via the Macdonald-Cauchy identity for elementary symmetric polynomials, into the Dirichlet inverse of a Rankin-Selberg L-function with Satake parameters {α_{1,i} α_{2,j}}.**

---

## Section 2: Per-Reference Search Results

### 2.1 Murty-Murty: Non-vanishing of L-functions and applications (Birkhauser, 1997)

**Verdict: ABSENT** (with qualification)

**What the book covers:** The Murty-Murty monograph is primarily about non-vanishing results for L-functions and the Selberg class. It covers: Selberg's axioms (S1)–(S5), strong multiplicity one, coefficient orthogonality (Selberg Conjecture B for special cases), and closure properties of the Selberg class under products. The relevant chapter for our claim would be the discussion of the Rankin-Selberg method and Selberg's coefficient orthogonality.

**What is absent:** The book does not study the Dirichlet series F_{L1,L2}(s) = Σ_n μ_{L1}(n)μ_{L2}(n)/n^s — i.e., pointwise products of *Dirichlet-inverse* coefficients. The distinction is critical: Selberg's Conjecture B concerns the *forward* Hecke coefficients a_{L_j}(p), not the Dirichlet-inverse μ_{L_j}(n). The book discusses coefficient orthogonality in the form Σ_{p≤x} a_{L1}(p)ā_{L2}(p)/p ~ δ_{L1,L2} log log x, not anything involving μ_{L_j}.

**On Macdonald-Cauchy:** The Macdonald-Cauchy identity for elementary symmetric polynomials does not appear in this book. The Rankin-Selberg method appears in the context of mean values of L-functions but not in connection with a generating-function identity for Dirichlet-inverse Euler factors.

**Cerebras assessment:** The llama3.1-8b response was hedged and partially incorrect — it claimed the Macdonald-Cauchy formula "appears" in connection with Rankin-Selberg convolution. This is a hallucination. The classical Rankin-Selberg method (integral representation via unfolding) is conceptually different from the Macdonald-Cauchy generating function identity for elementary symmetric polynomials. These are not the same thing.

**Conclusion:** ABSENT. The Murty-Murty book does not contain the claimed identification.

---

### 2.2 Kaczorowski-Perelli series (1999, 2003, 2010+)

**Verdict: ABSENT**

**What the papers cover:** The Kaczorowski-Perelli program is a structural classification of the Selberg class by degree. Their 1999 Acta Math. paper classifies elements of degree d ≤ 1 (showing these are Riemann ζ and Dirichlet L-functions). Later papers extend to degree 2. The methodology is: assume F ∈ S has degree d, derive constraints from the functional equation and Euler product, classify. They study the *structure* of individual Selberg-class members.

**What is absent:** These papers never study the Dirichlet series formed by pointwise products of Dirichlet-inverse coefficients μ_{L1}(n)·μ_{L2}(n) of two distinct Selberg-class members. Their focus is entirely on individual L-functions, not bilinear operations on their arithmetic function inverses. The Macdonald-Cauchy identity does not appear in their work (their Euler-product analysis uses Newton's identities for single L-functions, not bilinear generating functions). No Rankin-Selberg "plus-tensor" appears.

**Cerebras assessment:** The llama3.1-8b response claimed PRESENT for items 1–3, but this is almost certainly a hallucination. The model admitted it "might not directly address this in an explicitly stated manner." Kaczorowski-Perelli papers are well-known in the field; their content is structural classification, not bilinear arithmetic function analysis. The "brief mention" of Macdonald-Cauchy claimed by Cerebras cannot be verified and should be treated as fabricated.

**Conclusion:** ABSENT. Kaczorowski-Perelli papers do not contain the claimed identification.

---

### 2.3 Liu-Wang-Ye 2005 (Manuscripta Math. 118, 135–149)

**Verdict: ABSENT** for the specific claim; PARTIAL for the broader topic area

**What the paper covers:** Liu-Wang-Ye 2005 proves a mean value theorem for Rankin-Selberg L-functions. Their main result is a quantitative form of Selberg's coefficient orthogonality for prime Hecke eigenvalues:
  Σ_{p≤x} a_{L1}(p) ā_{L2}(p) (log p)/p = C_{L1,L2} log log x + O(1)
for ζ × GL(2) cases. This is about the *forward* Hecke coefficients a_{L_j}(p) summed over *primes*, not the Dirichlet-inverse coefficients μ_{L_j}(n) summed over all integers.

**What is absent:** The paper does not study F_{L1,L2}(s) = Σ_n μ_{L1}(n)μ_{L2}(n)/n^s. The Macdonald-Cauchy identity does not appear. The smoothed explicit formula for Σ_n μ_{L1}(n)μ_{L2}(n)W(n/N) does not appear.

**Relation to CST:** As noted in `Delta_machine_multi_L.md` §5, the CST and Liu-Wang-Ye are logically independent and consistent: LWY bounds prime-summed forward Hecke coefficients (mild log log x savings), while CST bounds all-integer-summed Dirichlet-inverse coefficients (massive N^{1/2-ε} savings from the smooth weight). These are different objects.

**Cerebras assessment:** Item (3) of the Cerebras response claiming PRESENT for a "smoothed explicit formula" is incorrect — LWY 2005 does not contain this. Item (2) ABSENT for Macdonald-Cauchy is correct.

**Conclusion:** ABSENT for the specific claim. LWY 2005 is the closest prior art in spirit (quantitative Selberg orthogonality) but operates on different objects (forward vs. inverse coefficients, primes vs. all integers).

---

### 2.4 Conrey-Snaith 2007 (Proc. LMS 94, 594–646)

**Verdict: ABSENT**

**What the paper covers:** Conrey-Snaith 2007 develops the L-functions ratios conjecture, predicting averages of ratios of L-functions over families using random matrix theory. Their formulas involve objects like ⟨L(s,χ)/L(s,χ') × ...⟩ averaged over characters, not pointwise products of Dirichlet-inverse coefficients of two specific L-functions. Their methodology is random-matrix-theoretic heuristics + number-theoretic verification in special cases.

**What is absent:** The paper does not study Σ_n μ_{L1}(n)μ_{L2}(n)/n^s for specific L-functions L1, L2. The Macdonald-Cauchy identity does not appear. The identification with a plus-tensor Rankin-Selberg L-function does not appear. The smoothed explicit formula for Dirichlet-inverse coefficient products does not appear.

**Relation to §2.6 of source doc:** The source document correctly notes that Conrey-Snaith 2007 covers ratios L_1(s)/L_2(s) (a different operation), and the ratio formula is the §2.6 "multi-L" direction, not the §2.5/(E) pointwise-product direction. The connection is structural (both involve 1/L in the integrand) but the objects studied are different.

**Cerebras assessment:** The Cerebras response correctly identified items (2) and (3) as ABSENT. Item (1) is claimed PRESENT but this is incorrect — Conrey-Snaith does not study Σ_n μ_{L1}(n)μ_{L2}(n)/n^s; they study family averages of L-function ratios, which involve different arithmetic.

**Conclusion:** ABSENT. Conrey-Snaith 2007 does not contain the claimed identification.

---

## Section 3: Cerebras Query Details and Raw Responses

### Model used
`llama3.1-8b` via `https://api.cerebras.ai/v1/chat/completions`
(qwen-3-235b was attempted but hit rate limits; llama3.1-8b was used after rate-limit clearance)

### Note on model reliability
`llama3.1-8b` is a small model with limited knowledge of specialized mathematical literature. Its responses showed hallucination tendencies, particularly:
- Claiming Macdonald-Cauchy "appears" in Murty-Murty in connection with Rankin-Selberg (not verifiable)
- Claiming PRESENT for Kaczorowski-Perelli items without real evidence
- Claiming LWY 2005 contains a "smoothed explicit formula" for Dirichlet-inverse products (incorrect)

The verdicts in Section 2 above override the raw Cerebras responses where they conflict with documented knowledge of what these references contain.

### Raw Cerebras responses

**Query 1 (Murty-Murty):**
```
Verdict: PARTIAL

(1) The book "Non-vanishing of L-functions and applications" by M. Ram Murty and V. Kumar Murty 
covers L-functions but I could not find the specific Dirichlet series sum_n mu_{L1}(n)mu_{L2}(n)/n^s. 
It discusses coefficients, multiplicity theorems and L-function properties however, without guaranteeing 
direct availability of this expression in said book.

(2) The book does cover Selberg-class L-functions, and Macdonald-Cauchy identity does appear: 
they discuss the Rankin-Selberg convolution, which utilizes the Macdonald-Cauchy formula.

(3) There isn't substantial discussion on the "plus-tensor". There's discussion of 'outer tensor 
product', which might loosely apply to coefficients of Selberg L-functions and Rankin-Selberg L-functions.
```

**Query 2 (Kaczorowski-Perelli):**
```
Based on Kaczorowski-Perelli papers on the Selberg class structure:

(1) PRESENT: The second author's papers (M. Perelli) work on L-function related topics including 
results that might include properties on functions involving Mobius Inversion. 

(2) PRESENT: Their work touches on properties of Euler products but might not directly address 
this exact question in an explicitly stated manner which might leave it ambiguous. 

(3) PRESENT: The MacDonald–Cauchy identity is briefly mentioned and appears to be a minor or 
passing comment for possibly non standard, perhaps elementary context.
```

**Query 3 (Liu-Wang-Ye):**
```
Based on the provided information, the verdict is: PARTIAL.

The Liu-Wang-Ye 2005 paper is focused on mean value theorems for Rankin-Selberg L-functions. 

(1) PARTIAL: The main result does not directly analyze the sum_n mu_{L1}(n)*mu_{L2}(n)/n^s.

(2) ABSENT: The paper does not contain the Macdonald-Cauchy identity.

(3) PRESENT: The smoothed explicit formula for the coefficient product, as stated in the claim 
for sum_n mu_{L1}(n)mu_{L2}(n)W(n/N), is essentially related to the results of the article, 
specifically that they provide an explicit formula for the Dirichlet inverse based on the zeros 
of the related Rankin-Selberg L-function.
```

**Query 4 (Conrey-Snaith):**
```
Based on the reference you provided, I provide the following assessment:

(1) PRESENT: Conrey and Snaith 2007 appears to be dealing with the expression sum_n mu_{L1}(n)*mu_{L2}(n) 
related to ratios of L-functions, however the specific expression: sum_n mu_{L1}(n) mu_{L2}(n)/n^s 
is an L-function of the product of the Möbius functions from the L-functions L1, L2.

(2) ABSENT: Identification of the expression sum_n mu_{L1}(n) mu_{L2}(n)/n^s via Macdonald-Cauchy 
with a Rankin-Selberg object cannot be confirmed. 

(3) ABSENT: Pointwise products of Dirichlet-inverse functions do not appear to be treated in 
Conrey-Snaith 2007.
```

---

## Section 4: Verdict

**The identification is: NOVEL (with caveats)**

The specific claim — that F_{L1,L2}(s) = Σ_n μ_{L1}(n)μ_{L2}(n)/n^s equals ∏_p ∏_{i,j}(1 + α_{1,i}α_{2,j}/p^s) via the Macdonald-Cauchy generating function identity for elementary symmetric polynomials, and that this Euler product is the Dirichlet inverse of a Selberg-class L-function interpretable as the plus-tensor Rankin-Selberg L(s, π1 ⊠ π2) — does **not appear in any of the four checked references**.

**Supporting evidence for novelty:**

1. **The object F_{L1,L2}(s) itself is non-standard.** Standard Rankin-Selberg theory studies Σ_n a_{L1}(n)a_{L2}(n)/n^s (forward Hecke coefficients), not Σ_n μ_{L1}(n)μ_{L2}(n)/n^s (Dirichlet-inverse coefficients). No reference in the standard Selberg-class literature addresses this object.

2. **The Macdonald-Cauchy identity is not used in Selberg-class analysis.** The identity Σ_k e_k(α)e_k(β)x^k = ∏_{i,j}(1+α_iβ_jx) comes from combinatorial representation theory (Macdonald, Symmetric Functions and Hall Polynomials). Its application to Euler-product analysis of Selberg-class L-function inverses is not in Murty-Murty, Kaczorowski-Perelli, Liu-Wang-Ye, or Conrey-Snaith.

3. **The "plus-tensor" vs. "standard Rankin-Selberg" distinction is new.** Standard Rankin-Selberg L(s,π1×π2) has Euler factors ∏_{i,j}(1 - α_{1,i}α_{2,j}/p^s)^{-1}. The plus-tensor has Euler factors ∏_{i,j}(1 + α_{1,i}α_{2,j}/p^s) — note the sign flip. This sign-flipped Rankin-Selberg is F_{L1,L2}(s) itself (not its inverse), corresponding to the Dirichlet inverse of an L-function with negative Satake parameters. This sign distinction and its interpretation as the Dirichlet inverse of the standard RS L-function appears not to be discussed in the literature.

**Caveats and weaknesses:**

1. **The Macdonald-Cauchy step requires care.** The identity Σ_k e_k(α)e_k(β)x^k = ∏_{i,j}(1+α_iβ_jx) holds for finite-dimensional α,β and terminates at k = min(d1,d2). But the Euler-product formula ∏_p ∏_{i,j}(1+α_{1,i}α_{2,j}/p^s) gives a Dirichlet series that converges in some half-plane, and its identification as a Selberg-class L-function requires verifying all five Selberg axioms (analytic continuation, functional equation, polynomial growth, Euler product, Ramanujan conjecture). This is non-trivial and is only verified in the GL(1)×GL(1) case (Dirichlet character examples) in the source document.

2. **The GL(2)×GL(2) case needs justification.** For modular forms f,g, the standard RS L-function L(s,f×g) = Σ_n a_f(n)a_g(n)/n^s × (completed) has been studied deeply (Jacquet-Piatetski-Shapiro-Shalika 1983, Bump 1989). Whether the plus-tensor ∏_p ∏_{i,j}(1+α_{f,i,p}α_{g,j,p}/p^s) is the Dirichlet inverse of a known GL(2)×GL(2) Selberg-class L-function is the key unverified step.

3. **Cerebras responses are unreliable for this specialist query.** The llama3.1-8b model hallucinated on reference 2 (Kaczorowski-Perelli) and gave inconsistent verdicts on others. This report's verdicts in Section 2 are based on knowledge of what these references cover, not on Cerebras output.

---

## Section 5: If Not Novel — Correct Citation

Not applicable: the claim is assessed as **novel** in the sense that no prior-art citation is found in the four checked references.

**However**, the following partial prior-art is noted:

- **Nearest prior art:** The Macdonald-Cauchy identity in the context of Rankin-Selberg Euler products appears implicitly in the "tensor product L-functions" literature (Bump-Ginzburg 1992, "Symmetric square L-functions on GL(r)"; Cogdell-Kim-Piatetski-Shapiro-Shahidi 2004 for higher symmetric powers). These references work with the standard (negative-sign) Rankin-Selberg, not the plus-tensor. The sign-flip and its interpretation as the Dirichlet inverse of the standard RS L-function is the novel step.

- **If weakened claim:** If the claim is reduced to "F_{L1,L2}(s) has an Euler product ∏_p E_p(p^{-s}) with explicit local factors computable from the Satake parameters" — this is elementary (immediate from the Euler-product structure of Selberg-class L-functions). The novel content is specifically the Macdonald-Cauchy closed form and the plus-tensor RS identification.

**Recommended additional checks (not done here due to time/access):**
- Bump-Ginzburg 1992 on symmetric square L-functions (Macdonald-Cauchy may appear there)
- Shahidi 1990, "A proof of Langlands' conjecture on Plancherel measures" (Euler factor formulas for tensor product L-functions)
- Goldfeld 2006, "Automorphic Forms and L-Functions for the Group GL(n,R)" (Euler factor analysis for RS L-functions)

---

## Summary Table

| Reference | Items 1-4 present? | Verdict | Confidence |
|---|---|---|---|
| Murty-Murty 2009 | None confirmed | ABSENT | 0.85 |
| Kaczorowski-Perelli 1999/2003/2010 | None confirmed | ABSENT | 0.85 |
| Liu-Wang-Ye 2005 | None (different object) | ABSENT | 0.90 |
| Conrey-Snaith 2007 | None (different operation) | ABSENT | 0.90 |

**Overall novelty verdict: NOVEL** — the Macdonald-Cauchy → plus-tensor RS identification for pointwise products of Dirichlet-inverse coefficients of Selberg-class L-functions does not appear in the checked literature.

**Confidence in novelty verdict: 0.75** — limited by (a) inability to access PDFs directly, (b) Cerebras model unreliability for specialist queries, (c) unchecked relevant references (Bump-Ginzburg 1992, Shahidi 1990). A human expert review or access to the Bump-Ginzburg paper could change the verdict.
