---
title: "G7 — Verification of Conrey–Snaith 2007 §7 Eq. (7.32) citation"
type: verification
domain: research
tier: working
confidence: 0.30
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Conrey–Snaith, 'Applications of the L-functions ratios conjectures', arXiv:math/0509480v2 (2007)"
  - "B3_CS_7_32_FROM_SCRATCH.md (this project)"
  - "B3_CS_eq_7_32_rigorous.md (this project)"
  - "TheoremB_proof_verification.md (G7 gap)"
tags: [theorem-B, CS-7-32, citation-audit, orthogonal-Plancherel-mult, gap-G7]
---

# Bottom line (HONEST)

The Theorem B proof currently cites **Conrey–Snaith 2007 §7 Theorem 7.3,
Eq. (7.32)** as "the source of orthogonal Plancherel multiplicity 1" for
the Petersson weight-aspect derivative-moment computation.

**Direct verification against the actual paper (arXiv:math/0509480v2)
shows this citation is incorrect.** §7 of CS 2007 treats the **unitary
(Riemann zeta)** discrete moments, not the orthogonal Petersson family,
and Eq. (7.32) is one step inside the derivation of the **fourth** moment
of ζ′(ρ) (Theorem 7.6) — not the second moment, not orthogonal, and not
in weight aspect.

The orthogonal Plancherel multiplicity claim therefore stands without an
explicit black-box source in CS 2007. It must be derived from-scratch
(B3_CS_7_32_FROM_SCRATCH.md attempts this) or sourced from
Conrey–Farmer–Zirnbauer 2008 / Iwaniec–Luo–Sarnak 2000 / Iwaniec–Sarnak
2000, none of which contain an off-the-shelf statement of the precise
fact "orthogonal Plancherel mult = 1 for the Petersson family
weight-aspect L′ second moment".

**Confidence in the existing CS 2007 citation: 0.30** (citation is
formally wrong; the constant 2/(3π) it is meant to support is correct
by triangulation, but the cited equation does not contain it).

---

# 1. Verbatim quotes from CS 2007

Source: arXiv:math/0509480v2 (Conrey–Snaith, *Applications of the
L-functions ratios conjectures*), pdftotext extraction.

## 1.1 §7 heading and scope

> "**7. Discrete moments of the Riemann zeta function and its derivatives.**
> So far in this paper we've considered integer moments. Another kind of
> average which gives useful information about the distribution of zeros
> is a discrete moment summing the zeta function, or its derivatives, at
> or near the zeros."

§7 is therefore **unitary** (Riemann zeta on the critical strip,
sums over γ with ρ = 1/2 + iγ). It does not address Petersson newforms.

## 1.2 Theorem 7.3 (verbatim, the second-moment statement)

> "**Theorem 7.3.** Assuming the ratio conjecture as indicated in (7.11),
> we have
>   Σ_{γ<T} |ζ′(ρ)|² = ∫₀^T [ (1/(24π)) log⁴(t/(2π)) + (γ/(3π)) log³(t/(2π))
>     + ((γ²/π) − (γ₁/π)) log²(t/(2π)) − (γ³/π + 5γγ₁/π + γ₂/π) log(t/(2π))
>     + γ⁴/π + 6γ²γ₁/π + 7γ₁²/π + 4γγ₂/π + 5γ₃/(3π) ](1+O(t^{-1/2+ε})) dt
>   = (T/(24π)) log⁴ T + O(T log³ T)."

(Constants γ, γ₁, γ₂, γ₃ are Stieltjes constants in the Laurent expansion
ζ(1+s) = 1/s + γ − γ₁s + γ₂s²/2! − γ₃s³/3! + …, eq. (7.18).)

The leading constant **1/(24π)** is the **unitary** discrete-second-moment
constant for ζ′ at zeros (Gonek 1984). It has nothing directly to do with
the orthogonal mult-1 claim. It does, however, encode the **unitary**
Plancherel multiplicity 3 implicitly — see §3 below.

## 1.3 Eq. (7.32) (verbatim)

Eq. (7.32) is inside §7.2 ("Fourth moment of the derivative") and is part
of the fold-back identity used in evaluating I_L (the contour piece on
the line σ = 1−c):

> "(7.32)  I_L = (1/(2π)) ∫₀^T [ log(t/(2π)) + O(1/(t+1)) ] |ζ′(½+it)|⁴ dt + I_R
>             = I_R + (d/dα)(d/dβ)(d/dγ)(d/dδ) (1/(2π)) ∫₀^T [ log(t/(2π))
>               + O(1/(t+1)) ] · ζ(½+it+α)ζ(½+it+β)ζ(½−it+γ)ζ(½−it+δ) dt
>               |_{α=β=γ=δ=0}"

This is an **algebraic identity** rewriting the discrete fourth moment of
ζ′ as the (continuous) fourth moment of ζ with shift derivatives. It is
**not** a theorem about orthogonal multiplicities; it is a manipulation
internal to the unitary Riemann-ζ computation.

The actual numerical evaluation of the fourth-moment leading constant
takes place several pages later in Theorem 7.6, and is unitary mult-3
based.

## 1.4 What §7 of CS 2007 actually contains

| Item | Family | What it says |
|---|---|---|
| Conjecture 7.1 | unitary (ζ) | HKO 2k-th discrete moment of ζ′ |
| Theorem 7.3   | unitary (ζ) | second discrete moment of ζ′ from ratios → 1/(24π)·T log⁴ T |
| Eq. (7.31)    | unitary (ζ) | contour integral form of second moment |
| Eq. (7.32)    | unitary (ζ) | I_L identity inside fourth-moment derivation |
| Theorem 7.6   | unitary (ζ) | fourth discrete moment of ζ′, polynomial of deg 9 in log T |
| Theorem 7.7   | unitary (ζ) | second moment of ζ at shifted zeros (Fujii) |

There is **no orthogonal example in §7**. The only orthogonal example
in the entire paper is §5.3 ("Orthogonal example"), which treats
**mollified second moment of L_Δ(½, χ_d) in the d-aspect** — a
**quadratic-twist family**, not the Petersson weight-aspect family of
Theorem B. The d-aspect orthogonal mollifier formula in §5.3 is also
unrelated to the discrete moment ⟨Σ |L′(ρ_f, f)|²⟩ used in Theorem B.

# 2. Step-by-step verification of the orthogonal-multiplicity-1 derivation

The from-scratch derivation in B3_CS_7_32_FROM_SCRATCH.md derives mult 1
**without** using any equation from CS 2007. Its actual ingredients are:

1. **Stieltjes-by-parts** (B3 §2): exact algebra. ✓
2. **Approximate functional equation** for L′(1+it,f) (Iwaniec–Kowalski Ch. 5). ✓
3. **Selberg expansion** of the fluctuation S_f(t) (Selberg 1946; ILS 2000 §2). ✓
4. **Petersson trace formula** (IK Eq. (14.14), Th. 14.5). ✓
5. **Bessel decay** J_{k−1}(x) ≪ (x/k)^{k−1} for x ≤ k, applied at threshold
   k > 4eT/√N (Iwaniec 1990). ✓
6. **Hecke convolution** (Petersson newforms, squarefree level): λ_f(m)·λ_f(n)
   = Σ_{d|(m,n)} λ_f(mn/d²). ✓ Elementary.
7. **Sato–Tate orthogonality at k → ∞** for Petersson family
   (Iwaniec–Sarnak 2000 §7 Th. 7.1; ILS 2000 §6): ⟨λ_f(p)²⟩ = 1, ⟨λ_f(p)⟩ = 0.
   ✓ Numerically reproduced: ∫₀^π (2cos θ)² (2/π) sin²θ dθ = 1.000000 (dps=25).
8. **Triple-correlation reduction**: applying (4a)+(4b) to ⟨λ(p)λ(m)λ(n)⟩
   collapses to a single Hecke-convolution diagonal pm = n at leading
   order. The "1" in mult-1 is the cardinality of this single diagonal.
9. **Mellin integral evaluation**: J = 1/3 (matches Lemma 3.1 numerically
   to 0.99998). ✓

**Verdict.** The mult-1 claim is independently derivable from
ILS 2000 + IS 2000 + Hecke convolution + Bessel decay. The CS 2007
citation is unnecessary for the substance, and incorrect as a literal
reference. **The argument survives, the citation does not.**

# 3. Comparison with the unitary mult-3 case (and Conrey 1989 analog)

For ζ on the critical line, the "Plancherel multiplicity" in the
4-shift moment ⟨ζ(½+α)ζ(½+β)ζ̄(½−γ)ζ̄(½−δ)⟩ is **3**, counting the
three pairings of shifts that produce diagonal residues:

  (α↔γ, β↔δ),  (α↔δ, β↔γ),  (α↔β, γ↔δ).

Each contributes one copy of the same Mellin integral (here = 1/3). So:

  Unitary 4-shift residue mass = 3 × (1/3) × (1/π) [GL₁ density] = 1/π.

CS 2007 §7.2 Theorem 7.6 records this implicitly via the constant
1/(24π) for the second moment of ζ′ (Gonek/Theorem 7.3) and the higher
constants for the fourth moment.

For Petersson newforms, the "shift swap" (α ↔ β) is enforced by
Hecke commutativity (λ_f(m)λ_f(n) = λ_f(n)λ_f(m)) but the diagonal
Hecke-convolution reduction collapses **all three pairings to one
combinatorial diagonal** at the leading order, because the off-diagonal
contributions vanish under Sato–Tate orthogonality:

  ⟨λ_f(p)·λ_f(m)·λ_f(n)⟩ → δ(n = pm) + small corrections.

Hence orthogonal Plancherel mult = 1.

This contrast (unitary 3 vs orthogonal 1) is **standard folklore** in
the random-matrix-theory + L-functions literature (Katz–Sarnak 1999;
ILS 2000; CFZ 2008) but is **not stated as a theorem** in CS 2007. It
is the conjectural content of CFZ 2008 ("Autocorrelation of ratios of
L-functions") for the orthogonal symmetry type, and is what
Milinovich–Ng 2014 §3–§4 use to predict 2/(3π).

# 4. Effect of the G1 correction (ratio = 16, not 4)

If G1 has corrected the multiplicative-decomposition ratio for the
weight-aspect Petersson family from 4 to 16, that affects the
**relationship between the smooth term and the pair-correlation term**,
not the Plancherel multiplicity itself. The mult-1 statement is a
combinatorial fact about ⟨λ_f(p)λ_f(m)λ_f(n)⟩_{F_k} as k → ∞ — it does
not depend on which test function is integrated against.

What G1's correction *would* affect: the assertion in
B3_CS_7_32_FROM_SCRATCH.md §7 that "Total = (1+1) × Smooth = 2 × (T/(3π))"
relies on an enhancement factor (smooth → smooth + paircorr) of 2. If
the correct enhancement factor is actually 4 (giving 4 × (T/(3π)) =
(4T)/(3π), or some other ratio compatible with the M–N target 2/(3π)),
then the mult-1 derivation must be reconsidered: either the
Mellin-integral constant or the density count would need to absorb the
factor.

**Honest read**: the from-scratch derivation in
B3_CS_7_32_FROM_SCRATCH.md hits the M–N target 2/(3π) with mult 1 +
Mellin 1/3 + density 1/π + smooth-paircorr enhancement 2. If
G1 says the enhancement is 16/4 = 4 instead of 2, then the smooth
constant 1/(3π) and the paircorr constant 1/(3π) cannot both stand —
one of them needs a factor 1/2 (to keep Total = 2/(3π)), or the
paircorr Plancherel multiplicity is 3 (not 1). This is a real open
question.

# 5. Honest confidence

| Claim | Confidence | Status |
|---|---|---|
| CS 2007 §7 Eq. (7.32) is the source of orthogonal mult 1 | **0.05** | FALSE. §7 is unitary. (7.32) is the I_L fold-back inside the unitary fourth-moment derivation. |
| Orthogonal Plancherel mult = 1 holds for the Petersson family at k → ∞ | 0.85 | TRUE by Hecke convolution + Sato–Tate orthogonality (ILS 2000 + IS 2000). Not a black-box from CS 2007. |
| The constant 2/(3π) for ⟨Σ |L′(ρ_f,f)|²⟩ in the Petersson weight-aspect family | 0.80 | Triangulated: (a) Heath-Brown 1979 ζ analog, (b) M–N 2014 prediction, (c) from-scratch derivation in B3_CS_7_32_FROM_SCRATCH.md. No single off-the-shelf source. |
| The Theorem B proof is unconditional in weight aspect | 0.65 | Modulo G1's ratio-4-vs-16 correction and the mechanical log-counting in §5–6 of B3_CS_7_32_FROM_SCRATCH.md. |

# 6. Recommended fix to Theorem B's proof

Replace the citation "by Conrey–Snaith 2007 §7 Theorem 7.3 Eq. (7.32)"
with one of:

(a) "by the orthogonal Hecke-convolution + Sato–Tate orthogonality
mechanism developed in §X (this paper), generalising the unitary
Plancherel argument of Conrey–Snaith 2007 §7 to the Petersson family";

(b) "conjecturally by the orthogonal ratios prediction of
Conrey–Farmer–Zirnbauer 2008 (CFZ Recipe), and unconditionally in
the weight aspect by ILS 2000 §6 + Iwaniec–Sarnak 2000 §7 + Hecke
convolution"; or

(c) Remove the CS 2007 citation entirely from the orthogonal-mult-1
location and only cite it as the unitary precursor in a remark.

Option (a) is honest. Option (b) is the cleanest historical attribution.
Option (c) is the safest if one wants no risk of overclaiming a source.

# 7. Done

CS 2007 §7 Eq. (7.32) does **not** state the orthogonal Plancherel
multiplicity 1 for the Petersson weight-aspect family. The citation in
the current Theorem B proof is incorrect. The substantive claim
(mult = 1) survives via the from-scratch Hecke-convolution derivation
in B3_CS_7_32_FROM_SCRATCH.md, but should be cited correctly to
ILS 2000 + IS 2000 + Hecke + Sato–Tate, or to CFZ 2008 (with appropriate
"conjecturally / unconditionally in weight aspect" caveats).

Gap G7 status: the **black-box citation** is removed; the **substance**
is preserved at confidence 0.85 via independent ingredients. The overall
Theorem B proof confidence is unaffected by the citation correction
itself, but is bottlenecked by G1 (ratio 4 vs 16) and the unfinished
log-counting bookkeeping in B3 §5–6.
