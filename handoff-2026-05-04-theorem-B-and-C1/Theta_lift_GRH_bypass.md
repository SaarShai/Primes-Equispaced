---
title: "Theta-lift / Howe-duality bypass for the 4-level density obstruction (Theorem B exact constant 2/(3π))"
type: audit
domain: research
tier: working
confidence: 0.07
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (creative-attack route audit)
sources:
  - GRH_bypass_FAMILY_aspect.md (audit of family-aspect routes; defines obstruction)
  - WebSearch: LMFDB SK-lift; Schmidt "SK lifting and functoriality"; Wikipedia "Saito-Kurokawa lift"
  - WebSearch: Gan 2022 SWC notes "Automorphic forms and theta correspondence"
  - WebSearch: Li 2024 Inventiones 237:697-733 "Moments of quadratic twists of modular L-functions"
  - WebSearch: Soundararajan-Young 2010 (JEMS 12:1097-1116) — GRH-conditional asymptotic
  - WebSearch: Rubinstein 1998 PhD thesis (n-level density, symplectic, GRH-conditional)
  - WebSearch: Levinson-Miller (n ≤ 7 for symplectic n-level density)
  - GRH_bypass_FAMILY_aspect.md §6 (precise obstruction: 4-level density)
tags: [grh-bypass, theta-lift, howe-duality, saito-kurokawa, symplectic, 4-level-density, theorem-B, creative-attack]
---

# Section 1. Howe duality framework for the Petersson family

## 1.1 The obstruction we must bypass

From `GRH_bypass_FAMILY_aspect.md` §6 (verbatim):

> 1-level density on family-aspect: ILS 2000, theorem (orthogonal).
> 2-level density on family-aspect: ILS 2000, theorem (with support restriction).
> 4-level density (= what 2/(3π) needs): CONJECTURE, no unconditional proof.

The exact constant 2/(3π) is the value of a CS 2007 ratios-kernel integral

  R(α,β,γ,δ) = ⟨ L'(s+α,f) L'(1-s-β,f) / (L(s+γ,f) L(1-s-δ,f)) ⟩_F

in the limit α,β,γ,δ → 0. As an n-level density object this is **4-level**:
two L's in the numerator, two in the denominator, each independently shifted
and one differentiation per numerator factor.

The Petersson weight-aspect family F_k = S_k*(N) has **orthogonal symmetry**
(ILS 2000; G4_orthogonal_mult_derivation.md confirms multiplicity m_O = 1
in the Plancherel measure). Unconditional n-level density for orthogonal
families on F_k: only n = 1 and n = 2 (with restricted support).

## 1.2 Howe duality — what it actually gives us

**Howe (1989), "Remarks on classical invariant theory," Trans. AMS 313:539-570.**
The local Howe duality theorem (over a non-archimedean local field of odd
residue char) gives a bijection between irreducible admissible representations
on the two sides of a reductive dual pair (G, G') ⊂ Sp. For the orthogonal-
symplectic pair (O(V), Sp(W)), this is the local theta correspondence.

What Howe duality is: a **bijection of representations** (Π ↔ θ(Π)),
preserving certain L-parameters via the local Langlands correspondence.

What Howe duality is NOT: a transfer of FAMILY-AVERAGED L-function statistics.
The lift is at the level of individual representations, NOT at the level of
density measures on the spectrum.

This distinction is the central conceptual mistake to avoid in the present
attack. We must check, for EACH proposed lift, whether the n-level density
on the source family transfers to a LOWER n-level density on the image
family — or whether it is just an n-level density on a different family
(no help) or an even higher-level density (worse).

# Section 2. Five route candidates evaluated

## 2.1 R1 — Direct theta lift to GL(2) symplectic side

**Setup.** Lift f ∈ S_k*(N) to a symplectic automorphic form via the
classical theta correspondence for the dual pair (O(2,1), Sp(2)).

**What the lift produces.** The Shimura correspondence (Waldspurger 1980,
Compositio 54:173-242) lifts a holomorphic newform f of weight 2k to a
half-integral weight form g of weight k+1/2 in Kohnen's plus space, with

  L(s, f) ↔ L(s, g) related via the Shimura zeta function identity.

In particular, L(s, g) on the half-integral weight side does NOT have the
same Euler product structure as L(s, f) — Waldspurger's relation is

  L(s+½, f) · χ(d) = (something involving |g(d)|² and L-values of f⊗χ_d)

at the central point (Waldspurger's central-value formula).

**Why this fails for our 4-level → 2-level reduction.**

(a) The half-integral weight form g lives on a **metaplectic** group, not
genuinely on Sp(2). Its associated L-function is L(s, f), the SAME degree-2
L-function. There is no Sp(2) L-function distinct from L(s, f) sitting on
this side.

(b) Family-on-family: the family {g} lifted from {f ∈ F_k} is just
{g_f : f ∈ F_k}, one-to-one. Density statistics on {g_f} reduce to density
statistics on {f}, by the L-identity. No reduction in n-level.

(c) Even if we replaced Shimura by a deeper theta lift (e.g. (O(2,2), Sp(4))),
the lifted L-function on Sp(4) would be a degree-4 L-function whose
n-level density unconditionally is at most n = 1 (the Sp(4) symplectic-symmetry
density on quadratic-twist families, Rubinstein 1998 + Gao 2014, **GRH-conditional**
for n ≥ 1 with sum-of-supports < 2).

**Verdict R1: FAILS.** The Shimura half-integral lift is a bijection of
representations, not a reduction of n-level density. The L-function is
unchanged. **Confidence: 0.02.**

## 2.2 R2 — Saito-Kurokawa lift to Sp(4)

**Setup.** Lift f ∈ S_{2k-2}(SL_2(ℤ)) to a Siegel modular form F_SK ∈ S_k(Sp_4(ℤ))
in Maass's "Spezialschar."

**Verbatim L-function factorization (LMFDB / Schmidt "SK lifting and
functoriality" / Wikipedia, all consistent).**

For level 1 SK lift σ_k from weight 2k-2 elliptic forms to weight k Siegel forms:

  L(s, σ_k(f), spin) = ζ(s − k + 2) · ζ(s − k + 1) · L(s, f)        (*)

After arithmetic normalization (recentering critical strip to s ↔ 1-s),
this becomes

  Λ(s, F_SK) = ζ(s + ½) · ζ(s − ½) · L(s, f)                        (**)

**The 4-level density on the SK-family is computed FROM the 4-level
density on the f-family, NOT to it.**

To see this, write the L'-second moment over the SK family:

  M_SK(T) := ⟨ Σ_γ |L'(½+iγ, F_SK)|² ⟩_{F_SK ∈ Sp(4)-family}

By (**),

  log L(s, F_SK) = log ζ(s + ½) + log ζ(s − ½) + log L(s, f)

so

  L'/L (s, F_SK) = ζ'/ζ(s+½) + ζ'/ζ(s-½) + L'/L(s, f).

The zeros of L(s, F_SK) are the union of:
- zeros of ζ(s+½) (i.e., zeros of ζ shifted by -½)
- zeros of ζ(s-½) (i.e., zeros of ζ shifted by +½)
- zeros of L(s, f)

|L'(ρ, F_SK)|² at a zero ρ of L(s, F_SK):
- if ρ is a zero of ζ(s±½), |L'(ρ, F_SK)|² = |ζ'(ρ ± ½)|² · |ζ(ρ ∓ 1)|² · |L(ρ, f)|²
  — this brings BACK ζ' moments at zeros of ζ, which is the **original
  Conrey 1988 problem** for ζ — also conditional on RH.
- if ρ is a zero of L(s, f), |L'(ρ, F_SK)|² = |ζ(ρ + ½)|² · |ζ(ρ − ½)|² · |L'(ρ, f)|²
  — this is exactly the original GL(2) L'-2nd moment, multiplied by a ζ factor.

The family-averaged sum over zeros decomposes as

  M_SK(T) = M_ζ-shift+(T) + M_ζ-shift-(T) + ⟨ Σ_γ_f |ζ(γ_f + ½)|² · |ζ(γ_f − ½)|² · |L'(½+iγ_f, f)|² ⟩_{f ∈ F}

The third term contains the original M_F(T) **multiplied by a ζ-factor product**.
Far from being a 2-level density, this is now a **mixed 4-level + 2-level**
object. The first two terms are GRH-for-ζ-conditional (Conrey 1988) at the
required level of precision.

**Why this fails for 4-level → 2-level reduction.**

(a) The SK L-function FACTORIZES, so its zeros and zero-derivatives split
into disjoint sets. The zeros from L(s,f) on the SK side carry **the original
GL(2) data**, weighted by extra ζ-factors which are GRH-conditional to control.

(b) The "symplectic family" of SK lifts is parametrized BY the orthogonal
family of f's (one SK lift per f, modulo Maass-relations). Family averaging
is the same operation, dressed up. The dual symmetry type (orthogonal →
symplectic) does NOT reduce statistical complexity on this branch — it
re-encodes it with extra ζ factors.

(c) Worse: the SK-lifted family is **NOT a generic symplectic family**.
SK lifts are NON-CUSPIDAL members in the broader Sp(4)/Siegel modular family
(per WebSearch: "Saito-Kurokawa lifts from SL(2,ℤ) are the non-cuspidal
members of families of L-functions for Sp(4,ℤ)"). The genuinely cuspidal
Sp(4) family does NOT come from elliptic GL(2) f's; it comes from generic
GSp(4) representations (Yoshida lifts, Ikeda lifts, genuine Siegel cusp
forms not of SK type). So the "symplectic dual" of F_k is NOT the SK image —
it is a DIFFERENT family.

**Verdict R2: FAILS.** SK factorization re-encodes the 4-level GL(2) data
with GRH-for-ζ baggage; the SK image is non-cuspidal in Sp(4) and not the
"symplectic dual family" Howe duality would predict. **Confidence: 0.04.**

## 2.3 R3 — Asai L-function lift (GL(2) over imaginary quadratic field)

**Setup.** For a Hilbert modular form f over ℚ(√−d), the Asai L-function
L(s, f, As) is a degree-4 L-function on GL(4)/ℚ. It detects whether f
is a base-change from GL(2)/ℚ.

**Asai 1977 ("On certain Dirichlet series associated with Hilbert modular
forms and Rankin's method," Math. Ann. 226:81-94, verbatim citation
unverified — flagged).**
Krishnamurthy 2003 ("The Asai transfer to GL(4) via the Langlands-Shahidi
method," IMRN 2003:2547-2576) establishes Asai transfer.

**Why this fails.** The Asai construction takes Hilbert modular forms
(NOT classical GL(2)/ℚ forms) and produces a degree-4 L-function. Our
target family is F_k = S_k*(N) over **ℚ**, not over an imaginary quadratic
field. There is no Asai-style L-function intrinsic to the Petersson
family on GL(2)/ℚ.

If we tried to artificially construct Asai by base-changing each f ∈ F_k
to a Hilbert modular form over ℚ(√−d) and then taking Asai, we would get
back exactly L(s, f) · L(s, f ⊗ χ_d) (for χ_d the quadratic character of
ℚ(√−d)), since base-change of GL(2)/ℚ to GL(2)/ℚ(√−d) and then Asai
recovers the symmetric/anti-symmetric pieces. This is again no genuine
4-level → 2-level reduction; it is a re-expression with the SAME complexity.

**Verdict R3: FAILS.** Asai is for forms over imaginary quadratic fields,
not for our Petersson/ℚ family. Base-changing introduces a quadratic twist
factor that re-encodes the same 4-level density. **Confidence: 0.03.**

## 2.4 R4 — Rankin-Selberg L(s, f×f) = L(s, sym²f)·ζ(s)

**Setup.** L(s, f × f) = L(s, sym²f) · ζ(s) is a degree-4 GL(4) L-function
(degree 4 = degree 3 sym² + degree 1 ζ).

**The hope.** The Petersson family of f maps (under Gelbart-Jacquet 1978)
to a family of sym²f's. The L'-2nd moment of L(s, f × f) = L(s, sym²f)·ζ(s)
factors:

  L'/L (s, f × f) = L'/L(s, sym²f) + ζ'/ζ(s).

Zeros of L(s, f × f) split into zeros of L(s, sym²f) (a degree-3
sym²-family) and zeros of ζ.

**Symmetry type of {sym²f}.** Per Conrey-Snaith 2007 §7 (verbatim citation
unverified — flagged) and Gelbart-Jacquet, the {sym²f}_f family has
**SYMPLECTIC** symmetry (since sym² of a 2-dim symplectic representation
is a 3-dim orthogonal representation, but the family parameter inverts
the symmetry — careful here: the source is SO(2,1) ≅ PGL(2), so sym² is
the standard rep on SO(3), giving ORTHOGONAL not symplectic).

**Actually** the correct symmetry type for the {L(s, sym²f)} family is
**SO(odd) = ORTHOGONAL** (not symplectic), per Rubinstein-Sarnak / Sarnak
2008 "Definition of families." [Caveat: I have not verified this against
a specific paper PDF; this is a known folklore statement that should be
PDF-checked before citing.]

If {sym²f} is orthogonal, then the L'-2nd moment over {sym²f} is **another
orthogonal-family 4-level object** — same obstruction, no reduction.

If by some accident it were symplectic, the symplectic 4-level density
unconditionally is at most n = 1 (Rubinstein 1998 unconditional support
0; Levinson-Miller GRH-conditional up to n = 7), so the reduction
4-level orth → 4-level symp is still GRH-conditional at the 4-level we need.

**Why this fails.**

(a) Symmetry-type of sym²f family is most plausibly orthogonal, NOT
symplectic. The "lift" 4-level → 4-level same symmetry type is no help.

(b) Even if symplectic: unconditional symplectic 4-level density is unproven
(Rubinstein 1998 covers only restricted support; Li 2024 Inventiones gives
the unconditional 2nd moment of L at the CENTRAL POINT for quadratic twists,
not 4-level density on the line).

(c) The factor ζ'/ζ(s) on the f×f side brings ζ-zero data, which requires
RH for ζ to control as it would otherwise.

**Verdict R4: FAILS.** sym² family symmetry type does not give symplectic
reduction; even if it did, unconditional symplectic 4-level density is
unproven. **Confidence: 0.05.**

## 2.5 R5 — Orthogonal-to-unitary specialization SO(2N) → U(N)

**Setup.** The orthogonal random-matrix ensemble SO(2N) embeds U(N) as a
subgroup. Maybe a "unitary version" of Theorem B is unconditional, then
orthogonal version follows by specialization.

**Why this fails immediately.**

(a) The unitary family analogue of F_k = S_k*(N) is the family of
**Dirichlet L-functions** L(s, χ) over primitive Dirichlet characters χ
mod q (Katz-Sarnak). The 4-level density on the unitary Dirichlet family
is **also conjectural at full support**. Hughes-Rudnick 2003 give 1- and
2-level density unconditionally (with restricted support); higher level
densities are GRH-conditional.

(b) Even if we had the unitary 4-level density unconditionally, the
"specialization" SO(2N) → U(N) at the random-matrix level does NOT give
a corresponding "specialization" of unconditional theorems at the
arithmetic L-function level. The arithmetic results sit on different
families (Petersson vs Dirichlet), not on a single family with both
symmetries available by ensemble restriction.

(c) Petrow-Young 2019 "The fourth moment of Dirichlet L-functions along
the critical line" (Ann. of Math.) is a specific unconditional result on
the unitary Dirichlet family — but it computes 4th moment of L on the line,
not 4-level density of L'. The two are different statistical objects.

**Verdict R5: FAILS.** Random-matrix specialization does not transfer to
arithmetic theorems; unitary-side 4-level density is also conjectural.
**Confidence: 0.02.**

# Section 3. Best route — full derivation

**There is no best route.** Every theta-lift / Howe-duality avenue
considered either:

(a) re-encodes the 4-level GL(2) data in a different parametrization with
the SAME or HIGHER complexity (R1, R2, R3),

(b) lifts to a family whose unconditional density theorems are still
restricted to n ≤ 2 (R4, R5),

(c) introduces additional GRH-for-ζ baggage from factorization terms
(R2 explicitly; R4 and R5 implicitly via lower-rank L's appearing as
factors).

The closest to "almost works" is **R2 (Saito-Kurokawa)**, which is
attractive because it provides an EXPLICIT factorization (**) and an
EXPLICIT statistic transfer. But the analysis in §2.2 shows the transfer
goes the WRONG way: it expresses M_SK(T) IN TERMS OF M_F(T) plus extra
ζ-mixed terms, not vice versa. Inverting this to extract M_F(T) from
unconditional knowledge of M_SK(T) requires controlling the ζ-mixed terms,
which themselves need RH for ζ.

# Section 4. Does the 4-level orthogonal obstruction lift to a 2-level symplectic?

## 4.1 The conceptual answer: NO.

The Howe-duality bijection acts on **representations**, not on **density
measures**. The n-level density of a family at the L-function level is a
statistical property of the **distribution of zero locations** in the
spectrum, not a property of any individual representation. There is no
mechanism in the local theta correspondence (Howe 1989; Kudla-Rallis "On
first occurrence in the local theta correspondence" Lecture Notes in Math
1812; Gan 2022 SWC notes) by which n-level statistics on one side of a
dual pair are guaranteed to match (n−2)-level statistics on the other side.

In random-matrix language: the symmetry types orthogonal SO(2N) and
symplectic Sp(2N) have DIFFERENT n-level densities for every n. There is
no formula expressing the orthogonal n-density as the symplectic
(n−2)-density of any related family.

## 4.2 The technical answer: also NO, by counting.

The CS 2007 ratios kernel R(α,β,γ,δ) for the Petersson orthogonal family,
in the limit α,β,γ,δ → 0, yields the EXACT 2/(3π) constant via a contour
integral computation that depends on:

- The **symmetry type weight** (orthogonal: -1/2 trace; symplectic: +1/2; unitary: 0)
- The **Plancherel multiplicity** (orth m_O = 1, symp m_Sp = 1, but different sign)
- The **Fourier-Mellin kernel** of the test function

Substituting the symplectic kernel for the orthogonal kernel in CS 2007
§3 changes the constant to a DIFFERENT number, NOT to 2/(3π). The constant
2/(3π) is INTRINSIC to the orthogonal symmetry type.

So even if we COULD lift unconditionally to a symplectic family with
2-level density available, the resulting constant would not be 2/(3π) —
it would be the symplectic analogue, which is a different constant
(Conrey-Snaith 2007 Tab. 1 lists per-symmetry-type constants).

To recover 2/(3π) we need the ORTHOGONAL 4-level density, period.

## 4.3 Where this diagnosis differs from the brief

The brief claims "4-level density on orthogonal might LIFT to 2-level
density on symplectic." The technical content of this claim:

- Howe duality at the local-rep level: TRUE (bijection of reps).
- Density-measure transfer at the n-level statistic level: FALSE in
  literature. No theorem in Howe 1989, Kudla-Rallis CMS volume,
  Roberts 2001 ("Global L-packets for GSp(2) and theta lifts"), Gan 2014
  ("Theta correspondence: recent progress and applications," ICM 2014),
  or Mok-Sakellaridis-Wang asserts a density-level bijection.
- The proper analogue would be a result like: "n-level density on family
  X = (n-2)-level density on Howe-dual family Y, plus computable error."
  No such result exists in the literature.

# Section 5. Honest verdict

## 5.1 Does the theta-lift bypass work? **NO.**

Five route candidates evaluated. None reduces the 4-level orthogonal
density requirement to a 2-level (or 1-level) computation on the
Howe-dual side.

The conceptual reason: Howe duality is a representation-level bijection,
not a density-level transfer. The n-level density of a family is a
statistic of the EMPIRICAL distribution of zeros, which has no
representation-theoretic interpretation that would let it transfer
across a dual-pair boundary.

The technical reason: even granting a hypothetical density-level transfer,
the symplectic (n-2)-level density unconditionally is also restricted
(Rubinstein 1998 GRH-conditional; Li 2024 unconditional only at central
point, not on the line). Additionally, the constant 2/(3π) is intrinsic
to the orthogonal symmetry type and cannot be obtained from a symplectic
computation by substitution.

## 5.2 Specific factual corrections to the brief

The brief contained two factual errors (relevant to verifying claims):

(E1) "Symplectic family (e.g. quadratic twists L(s, f, χ_d) over d) is
symplectic symmetry. … 2-level density on symplectic, which IS
unconditional (e.g. Soundararajan-Young 2010)."

**Correction:** Soundararajan-Young 2010 (JEMS 12:1097-1116) prove the
asymptotic for the second moment of L(½, f ⊗ χ_d) over d **conditionally
on GRH**, with only a matching lower bound unconditionally. The asymptotic
was made unconditional only in **Li 2024 (Inventiones 237:697-733)**, and
even then it is at the **central point** s = ½, not a 2-level density on
the critical line.

(E2) "Asai L-function: GL(2) over imaginary quadratic field lifts."

**Correction:** Asai applies to Hilbert modular forms (forms over a real
or imaginary quadratic field), not to GL(2)/ℚ. The Petersson family on
GL(2)/ℚ does not have a natural Asai L-function intrinsic to it.

## 5.3 What CAN we say honestly?

The cage statement (Theorem B', GRH_bypass_FAMILY_aspect.md §3.1) is the
unconditional result. The exact constant 2/(3π) requires CS 2007 family-
aspect ratios identity, which is a 4-level density statement on the
orthogonal Petersson family — open in the literature, not bypassable by
theta lifts.

# Section 6. If the route worked, what would the explicit error term be?

This section is **vacuous** because none of the five routes works. For
completeness, the closest-to-working route (R2, Saito-Kurokawa) would
deliver, IF the ζ-mixed terms could be controlled unconditionally:

  M_F(T) = M_SK(T) − M_ζ-shift+(T) − M_ζ-shift−(T) + (cross-terms with ζ × L)

With error term

  Error = O(M_ζ-shift terms) + O(cross-terms)

The M_ζ-shift terms scale as T·log³T (Conrey 1988 for ζ' at zeros of ζ,
GRH-conditional unconditionally only as O(T·log⁵T)). The cross-terms
scale as T·log³T or larger.

So even hypothetically, the error term in this route would dominate the
main term 2/(3π)·T·log⁴T at any unconditional level of control, by a
factor ≥ T^ε. This confirms route R2 cannot succeed even with optimal
ζ-side bounds short of GRH.

# Section 7. Confidence aggregation (single rule)

Probability theta-lift bypass yields exact 2/(3π) unconditionally:

  P_bypass = max over routes (P_route) where
    P(R1) = 0.02 (Shimura is bijection, no density reduction)
    P(R2) = 0.04 (SK factorization re-encodes; ζ-baggage GRH-conditional)
    P(R3) = 0.03 (Asai not applicable to GL(2)/ℚ)
    P(R4) = 0.05 (sym² symmetry type ≠ symplectic; even if so, 4-level
                  symplectic density unconditional unproven)
    P(R5) = 0.02 (no arithmetic transfer of RMT specialization)

  P_bypass = 0.05 (dominated by R4)

Adjustment for "we missed a route" (epistemic uncertainty):
  +0.02 (some Howe-duality machinery I haven't surveyed; Mok-Sakellaridis-Wang
         on relative trace formulas, recent IMRN 2025 Howe-duality results)

**Final P(theta-lift bypass works) = 0.07.**

Confidence this analysis is correct (no errors in the negative verdict):
**0.85** (subject to PDF verification of Conrey-Snaith 2007 §7 symmetry
types and Asai 1977 statement; flagged in §2 above).

# Section 8. Summary table

| Route | Description | Verdict | Why fails | Confidence |
|---|---|---|---|---|
| R1 | Direct Shimura → half-int weight g | FAILS | Bijection, no density reduction | 0.02 |
| R2 | Saito-Kurokawa → Sp(4) | FAILS | Factorization re-encodes; ζ-baggage GRH-cond | 0.04 |
| R3 | Asai L-function | FAILS | Not applicable to GL(2)/ℚ | 0.03 |
| R4 | Rankin-Selberg L(s, f×f) | FAILS | sym² is orthogonal not symplectic; if symp, 4-lvl unconditional missing | 0.05 |
| R5 | Orth → Unitary specialization | FAILS | No arithmetic-level transfer | 0.02 |

Aggregate: **theta-lift bypass does NOT deliver Theorem B-exact unconditionally.**

# Section 9. Recommendation

Stand by GRH_bypass_FAMILY_aspect.md §7: publish the cage statement
(Theorem B', confidence 0.85) as the headline. The exact 2/(3π) remains
conditional on CS 2007 family-aspect ratios — a 5-10 year open problem.
Theta lifts and Howe duality, despite their elegance, do NOT shortcut
this gap.

**Done.**

# Appendix A. Citation flags requiring PDF verification

The following citations were used in the analysis but were assembled from
WebSearch summaries and prior knowledge, not direct PDF reading. They
should be PDF-verified before public use:

(F1) Howe 1989 "Remarks on classical invariant theory," Trans. AMS 313:539-570
     — used in §1.2 for the bijection statement. Public Trans. AMS, easy to verify.

(F2) Conrey-Snaith 2007 "Applications of the L-functions ratios conjecture,"
     Proc. LMS 94:594-646 — §7 claimed to discuss orthogonal vs symplectic
     ratios. Verify Tab. 1 / §7 directly.

(F3) Saito-Kurokawa L-function factorization (**) — verified across THREE
     independent sources (LMFDB, Schmidt SK-functoriality paper, Wikipedia)
     all agreeing. High confidence.

(F4) Soundararajan-Young 2010, GRH-conditional asymptotic — verified via
     WebSearch on JEMS 12:1097-1116 abstract; Li 2024 made unconditional.

(F5) Asai 1977 Math. Ann. 226:81-94 — flagged. Statement used is generic
     "Asai is for Hilbert modular forms," which is standard.

(F6) Rubinstein 1998 PhD thesis — n-level density for symplectic
     quadratic-twist family GRH-conditional. Verified via WebSearch.

(F7) Petrow-Young 2019 "Fourth moment of Dirichlet L-functions" Ann. of Math.
     — central point, not 4-level density. Verified via prior project notes
     (G2_GRH_bypass.md §2.5 cites this).

The verdict (theta-lift route fails) does NOT depend on (F1)-(F2) precise
constants — only on the structural statement that Howe duality is a
representation-level bijection, which is the universally-acknowledged
content of the theorem. The verdict is robust to PDF-verification outcomes
on (F1)-(F2).
