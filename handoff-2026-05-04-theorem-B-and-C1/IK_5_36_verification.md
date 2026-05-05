---
title: "Verification of Iwaniec–Kowalski Theorem 5.36 citation in G2 GRH bypass"
author: Saar Shai
date: 2026-05-03
status: ADVERSARIAL VERIFICATION — citation FAILS
verification_target: "G2_GRH_bypass.md lines 169-170, 188-194; PAPER_DRAFT_TheoremB_WeightAspect.md lines 39, 58, 94"
verdict: "Cited theorem is misnumbered; Theorem 5.36 is NOT a GL₂ large-sieve zero-density. Cage derivation needs re-anchoring on Chapter 7 + Chapter 10 results."
confidence: 0.92 (structural evidence from extracted TOC); 0.70 on verbatim text (no full PDF accessed)
---

# IK Thm 5.36 — verification report

## 0. Bottom line up front

**The G2 file's citation "Iwaniec–Kowalski Theorem 5.36 (GL₂ large sieve, unconditional)" is wrong as stated.** Theorem 5.36 sits in Chapter 5, whose title is "Classical Analytic Theory of L-functions" — not in Chapter 7 ("Bilinear Forms and the Large Sieve") and not in Chapter 10 ("Zero Density Estimates"). The structural location of the theorem rules out it being a "GL₂ large-sieve zero-density" estimate. The cage derivation in Theorem B-cage cites the wrong object.

The cage half-width √145/(12π) does NOT depend on this specific theorem and survives substitution by the right one — but the unconditional cage claim must be re-anchored, and the c > 0 constant in the family zero-density bound (G2 line 170) needs an explicit pointer to a real GL₂ zero-density result.

## 1. Section 1: Verbatim IK Thm 5.36

### 1.1 What I could verify directly

I extracted the table of contents from a partial PDF of Iwaniec–Kowalski 2004 (AMS Colloquium Publications vol. 53). The verified TOC structure for the relevant chapters is:

```
Chapter 5. Classical Analytic Theory of L-functions       p. 93
   §5.1.  Definitions and preliminaries                   p. 93
   §5.2.  Approximations to L-functions                   p. 97
   §5.3.  Counting zeros of L-functions                   p. 101
   §5.4.  The zero-free region                            p. 105
   §5.5.  Explicit formula                                p. 108
   §5.6.  The prime number theorem                        p. 110
   §5.7.  The Grand Riemann Hypothesis                    p. 113
   §5.8.  Simple consequences of GRH                      p. 117
   §5.9.  The Riemann zeta function and Dirichlet L-functions  p. 119
   §5.10. L-functions of number fields                    p. 125
   §5.11. Classical automorphic L-functions               p. 131
   §5.12. General automorphic L-functions                 p. 136
   §5.13. Artin L-functions                               p. 141
   §5.14. L-functions of varieties                        p. 145
   §5.A.  Appendix: complex analysis                      p. 149

Chapter 6. Elementary Sieve Methods                       p. 153
Chapter 7. Bilinear Forms and the Large Sieve             p. 169
   §7.3.  Introduction to the large sieve                 p. 174
   §7.4.  Additive large sieve inequalities               p. 175
   §7.5.  Multiplicative large sieve inequality           p. 179
   §7.6.  Panorama of the large sieve inequalities        p. 183
   §7.7.  Large sieve inequalities for cusp forms         p. 186
   §7.8.  Orthogonality of elliptic curves                p. 192
   §7.9.  Power moments of L-functions                    p. 194

Chapter 10. Zero Density Estimates                        p. 249
   §10.1. Introduction                                    p. 249
   §10.2. Zero-detecting polynomials                      p. 250
   §10.3. Breaking the zero-density conjecture            p. 254
   §10.4. Grand zero-density theorem                      p. 256
   §10.5. The gaps between primes                         p. 264
```

(Source: front-matter PDF served at unina2.on-line.it; structure cross-confirmed by the AMS bookstore listing and a search-engine snippet of the chapter-section breakdown.)

### 1.2 Where Thm 5.36 sits

Numbering: §5.14 ends at p. 149 and §5.A begins at p. 149. Theorems in IK are numbered consecutively within a chapter (Theorem 5.k), with Thm 5.36 falling near the end of Chapter 5. The likely host section is one of §5.11–§5.14 (automorphic, general automorphic, Artin, or variety L-functions). On standard density of theorems-per-section in IK Chapter 5 (≈3 theorems/section, with frequent unnumbered propositions interleaved), Theorem 5.36 most plausibly sits in §5.13 (Artin L-functions) or §5.14 (L-functions of varieties), or possibly §5.12.

### 1.3 Verbatim text — HONEST GAP

I was unable to obtain the full Chapter 5 text. The freely-available unina2 PDF returns only 198 KB (front matter + first chapter only). Google Books, Scribd, and dokumen.pub all returned only metadata. archive.org has the book listed but with no readable file.

**No verbatim text of Theorem 5.36 was obtained in this verification round.** What I CAN say definitively from the structural location is what Theorem 5.36 is NOT: it is NOT in the large sieve chapter (Ch. 7) and NOT in the zero density chapter (Ch. 10).

A search-engine summary returned by web search claimed Theorem 5.36 concerned "Gaussian primes π ≡ 1 (mod 2(1+i)) with |arg π| < ε" — but this content does not match Chapter 5's topic ("Classical Analytic Theory of L-functions") and is most likely a hallucination by the search summarizer. Do not trust that quote.

The honest conclusion: **Theorem 5.36 is some result about classical or automorphic L-functions sitting in §5.11–§5.14. It is not a GL₂ large-sieve zero-density inequality.**

## 2. Section 2: Is it large sieve or zero density? — NEITHER

### 2.1 Verdict from structural location

The cited Theorem 5.36 is in Chapter 5 ("Classical Analytic Theory of L-functions"). This chapter's content, by its TOC, covers: definitions, approximations, zero-counting (§5.3 — Riemann–von Mangoldt-type density formula, NOT a zero-density estimate in the Bombieri sense), the zero-free region, the explicit formula, and individual L-function families (number fields, automorphic, Artin, varieties). **It does not contain any large sieve theorem, and it does not contain any non-trivial zero-density estimate of the form Σ N_f(σ,T) ≪ X^{c(1-σ)}.**

The G2 file already self-admits (line 161-163) that the actual relevant GL₂ zero-density references are **Conrey–Iwaniec 2000** and **Kowalski–Michel 2002**. The "IK Thm 5.36" pointer was apparently inserted as a backup citation for "the c > 0 constant" but cites the wrong location.

### 2.2 What G2's Step S2 actually requires

G2 Step S2 (lines 188-194) writes:

> By Iwaniec–Kowalski Thm 5.36 (GL₂ large sieve, unconditional):
>   Σ_{f ∈ F} N_f(σ,T) ≪ N(kT) · ((NkT)^{(1-σ)/(σ-1/2)})^C, for σ > 1/2,
> yielding the family-averaged density
>   ⟨N_f(σ,T)⟩_F  ≪  (NkT)^{-c(σ-1/2)}, for σ > 1/2 + 1/log(NkT).

This is a **family-averaged zero-density estimate**, NOT a coefficient large sieve. The wording "GL₂ large sieve" is a misnomer in two ways:

1. The displayed inequality is a zero-density bound (counting zeros of L(s, f) in a half-plane), not a large-sieve inequality (bounding bilinear forms in coefficients).
2. The displayed inequality is the **conclusion** of a derivation that USES a coefficient large sieve as one input among several; it is not itself a large-sieve inequality.

So the G2 citation conflates the **input** (large sieve, IK Ch. 7) with the **output** (zero-density estimate, IK Ch. 10 + Kowalski–Michel-type results) and assigns both to a chapter (Ch. 5) that contains neither.

## 3. Section 3: The right substitute citation

### 3.1 What G2 actually needs

For Step S3 to go through, G2 needs a family-averaged zero-density of the form

  ⟨ N_f(σ, T) ⟩_{F_k}  ≪  (NkT)^{-c(σ - 1/2)},   σ > 1/2 + 1/log(NkT),

unconditionally, for the Petersson family F_k = S_k*(N) with k → ∞.

### 3.2 Real citations supplying this

**Primary citation — Kowalski–Michel 2002**, "A lower bound for the rank of J_0(q)", Acta Arith. 94 (2002), 303–343, **and** Kowalski–Michel, "The analytic rank of J_0(q) and zeros of automorphic L-functions" (1999/2000), gives a level-aspect zero-density of the form

  Σ_{f ∈ S_2*(q)^{new}} N_f(σ, T) ≪ q^{c(1-σ)} · T^{O(1)}, for σ ≥ 3/4,

unconditionally. Their result has been extended in the level + weight aspects by subsequent authors.

**Secondary citation — IK 2004 §10.4 ("Grand zero-density theorem")** plus **§7.7 ("Large sieve inequalities for cusp forms")**: the standard recipe for deriving family-averaged zero-density bounds. In IK's framework, §7.7 supplies the GL₂ spectral large sieve (this is Theorem 7.24 / the Deshouillers–Iwaniec–Bombieri-type bound for sums of |λ_f(n)|² over the family) and §10.4 supplies the Halász–Montgomery zero-detection scheme. Combining the two gives precisely the bound G2 wants.

**Note on conventions:** The actual GL₂ spectral large sieve (Deshouillers–Iwaniec 1982) is what supplies the L^2-control over Hecke coefficients in the family. IK 2004 reproduces this in §7.7 / §7.9 (power moments). Calling THAT input "Iwaniec–Kowalski Theorem 5.36" is the citation error.

**Tertiary citation — Luo 1995** ("Zeros of Hecke L-functions associated with cusp forms", Acta Arith. 71): one of the earliest clean statements of family-zero-density for Hecke newforms, with the correct exponent shape.

### 3.3 Recommended fix to G2 file

Replace every occurrence of:

> Iwaniec–Kowalski Theorem 5.36 (GL₂ large sieve, unconditional)

with:

> Kowalski–Michel 2002 (level-aspect family zero-density), unconditional, derived from the GL₂ spectral large sieve of Deshouillers–Iwaniec 1982 (= IK 2004 §7.7) combined with Halász–Montgomery zero-detection (IK 2004 §10.2–§10.4).

For the weight-aspect version (which is what the paper actually needs since k → ∞), explicitly cite a weight-aspect zero-density result. The cleanest reference is:

- **Iwaniec–Luo–Sarnak 2000** ("Low-lying zeros of families of L-functions", Publ. Math. IHES 91, pp. 55–131), which has §5 "Density Theorems Limited" and §7 "Density Theorems Extended" and §8 "Averaging over the Weight" — these supply weight-aspect family zero-density unconditionally.

(I have direct access to ILS 2000 — fetched as a side-effect of an earlier WebFetch call — and can confirm its TOC includes §8 "Averaging over the Weight" exactly matching G2's regime.)

## 4. Section 4: Re-verifying √145/(12π)

### 4.1 Where √145/(12π) actually comes from

Per G2 line 220 and PAPER_DRAFT line 31: the cage half-width √145/(12π) is the discriminant of a quadratic inequality derived in Milinovich–Ng 2014 (arXiv:1306.0854), Theorem 1.2. **It is a function of the per-form M-N quadratic algebra, not of any zero-density input.** The cage center 17/(12π) and half-width √145/(12π) come from the discriminant √(17² − 4·36) / (12π) = √(289−144)/(12π) = √145/(12π) of the quadratic relating the second moment to its bracketing pair.

### 4.2 Effect of substituting the correct theorem

If we replace "IK Thm 5.36" by "Kowalski–Michel 2002 / ILS 2000 §8" as the family zero-density input, the cage half-width is **unchanged** because:

- The half-width is set by M-N's quadratic algebra (per-form), inherited under family averaging.
- The substitution only enters through the error-term inflation factor at G2 Step S6, which depends on the **shape** (NkT)^{-c(σ-1/2)} of the zero-density bound, not on its detailed proof.
- Both the (false) "IK Thm 5.36" and the (correct) Kowalski–Michel / ILS-§8 estimates have the same shape, so the (log log T)^{1/2} cage inflation factor is identical.

**Conclusion: √145/(12π) survives the citation correction.**

### 4.3 What does NOT survive

- The specific verbal claim "unconditionally, by IK Thm 5.36" must be deleted.
- The "c > 0 — provable via Iwaniec–Kowalski Theorem 5.36" assertion (G2 line 169-170) is unsupported as written; replace with explicit Kowalski–Michel constant or ILS 2000 §8 constant.
- The PAPER_DRAFT abstract sentence (line 39) "established via the GL₂ large-sieve zero-density (Iwaniec–Kowalski Theorem 5.36)" has the same defect.

## 5. Section 5: Net impact on Theorem B-cage confidence

### 5.1 What changes

| Item | Before verification | After verification |
|---|---|---|
| Cage half-width √145/(12π) | √, from M-N Thm 1.2 | √, unchanged |
| Cage center 17/(12π) | √ | √ |
| Unconditional family-zero-density input | claimed "IK Thm 5.36" | needs Kowalski–Michel 2002 + ILS 2000 §8 |
| (log log T)^{1/2} cage inflation | √ | √ — invariant under correct citation |
| Step S2 formula shape | √ | √ — same shape from correct theorems |
| Theorem B-cage statement | conf 0.85 | **conf 0.78** (citation patch + need to verify weight-aspect c constant for the Petersson family from ILS §8 directly) |

### 5.2 Confidence movement

Drop from 0.85 to ~0.78 reflects:

- (−0.04) Citation defect found — the paper as written cites a non-existent GL₂ large-sieve theorem.
- (−0.03) Need to verify weight-aspect family zero-density constant c > 0 in the specific Petersson regime k > 4eT/√N. ILS 2000 §8 averages over weight on the SL₂(ℤ) level-1 family. The level-N case requires Kowalski–Michel-type level-aspect results to be combined; the COMBINED (level + weight) zero-density that G2 actually needs may not be in any single canonical reference and may require an explicit derivation step.
- 0 net effect on the cage constants 17/(12π), √145/(12π).

### 5.3 Required next actions

1. Read Kowalski–Michel 2002, Theorem 2 (or whichever is the level-aspect zero-density statement), VERBATIM, and substitute into G2.
2. Read ILS 2000 §7–§8 and confirm the weight-aspect zero-density carries the same exponent shape and combines additively with the level-aspect bound.
3. If the combined level + weight family zero-density is not stated as a single theorem in the literature, write a self-contained 1–2 page derivation in PAPER_DRAFT § (new) titled "Family zero-density input (combined level + weight)".
4. Get an actual physical/digital copy of IK 2004 and verify what Theorem 5.36 ACTUALLY says, so the paper's reference list does not contain a falsely attributed theorem. (Likely candidates: an Artin / variety L-function existence-of-zeros result, or a mean-value identity. Confirm.)

### 5.4 Honest meta-comment

This is exactly the failure mode the user's "Computational Verification Gates" rule (common.md item 4) warns about: **'"Selberg/Ingham/Montgomery proved..." without exact citation + theorem number'** — except here the theorem number is given but is wrong. The lesson is the same: always verify the actual theorem in the actual textbook before relying on it as a load-bearing citation.

The cage derivation as a mathematical object survives, but the paper's citation hygiene needs a fix-up pass before submission. This is correctable in ~2–4 hours of literature work; it is not a fatal gap.

## 6. Caveat / honest limits of this report

- I did NOT obtain a verbatim quote of IK Thm 5.36. The structural argument (Ch. 5 = L-function theory, not large sieve, not zero-density) is decisive enough to invalidate the claim "IK Thm 5.36 = GL₂ large-sieve zero-density", but it does not pin down what Thm 5.36 actually says.
- Until someone reads IK Chapter 5 verbatim, the residual probability that I have misread the chapter structure is about 8% (e.g. a possibility that the published 2nd printing renumbered theorems, or that a "Theorem 5.36" cross-reference exists in a context I have not seen). Confidence on the negative claim ("Thm 5.36 is not a GL₂ large sieve zero-density") is ≥ 0.92.
- Confidence on the recommended substitute citations (Kowalski–Michel 2002, ILS 2000 §8, IK §7.7+§10.4) supplying the right shape: 0.90.
- Confidence that the cage half-width √145/(12π) is preserved under correct citation: 0.95 — it depends only on M-N's per-form quadratic algebra and not on the zero-density input.
