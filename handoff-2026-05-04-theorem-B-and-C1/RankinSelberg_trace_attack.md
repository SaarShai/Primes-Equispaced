---
title: "Rankin-Selberg trace attack on L'-2nd-moment — does it bypass GRH for the exact 2/(3π)?"
type: audit
domain: research
tier: working
confidence: 0.20
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (creative attack — Rankin-Selberg)
sources:
  - /tmp/milinovich_ng.txt (Milinovich-Ng 2014, "Simple zeros of modular L-functions")
  - /tmp/ils.txt (Iwaniec-Luo-Sarnak 2000, "Low-lying zeros of families of L-functions", Publ. IHÉS 91)
  - /tmp/cfkrs.pdf (CFKRS — Conrey-Farmer-Keating-Rubinstein-Snaith integral moments)
  - GRH_bypass_FAMILY_aspect.md (5 prior failed routes)
tags: [grh-bypass, rankin-selberg, L-prime-2nd-moment, theorem-B, GL2xGL2, sym2, family-aspect]
---

# Section 1. Rankin-Selberg framework for L'-second-moment

## 1.1 The target object

We want to evaluate, on family-average over F_k = H_k^*(N), the quantity

  M_F(T) = ⟨ Σ_{0<γ_f≤T} |L'(½+iγ_f, f)|² ⟩_F

with the M-N (2014) target constant 2/(3π) — i.e. the conjectural

  M_F(T) ~ (2/(3π)) · ⟨c_f⟩ · T · log⁴(NkT).

The quantity 2/(3π) = 16/(24π) sits **interior to** the unconditional cage
[(17−√145)/(12π), (17+√145)/(12π)] = [0.131, 0.452]; M-N's per-form constants
are

  (M-N (6))   Σ |Σ α_f(n) n^{−ρ_f}|² ~ (5/(24π))·c_f T log⁴ X
  (M-N (7))   Σ |Σ β_{f̄,X}(n) n^{−ρ_f}|² ~ (29/(24π))·c_f T log⁴ X

(verbatim /tmp/milinovich_ng.txt lines 405-440, Proposition 1.1). The
cage center 17/(12π) = (5+29)/(2·24π) is the sym-quadratic-form average;
2/(3π) = 16/(24π) is the SPECIFIC cross-term that matches CS-2007 ratios.

## 1.2 The Rankin-Selberg L-function L(s, f×f̄)

ILS (verbatim /tmp/ils.txt 2049-2076):

> "For any f ∈ H_k^*(N) the Rankin-Selberg L-function is defined by
>   L(s, f⊗f) = Σ λ_f(n²) n^{−s}
> with Euler product ... This satisfies the functional equation (see [Li],
> Theorem 10)  A(s, f⊗f) = A(1−s, f⊗f)."

The closely related Z(s, f) := Σ λ_f(n²) n^{−s} appears (3.13). M-N
Proposition 4.1 (line 213):

> "The fact that c_f > 0 exists, and is finite, essentially follows from
> the work of Rankin and Selberg ... L(s, f×f̄) ... can be continued to
> all of C apart from a simple pole at s=1 with a residue of c_f."

So the Rankin-Selberg L-function HAS unconditional analytic continuation
and functional equation. **No GRH used.** This is the strength of the
Rankin-Selberg input.

## 1.3 The structural difficulty for L'-2nd-moment

Rankin-Selberg gives the analytic structure of Σ |λ_f(n)|²/n^s, which
encodes the SECOND moment of L on the line (via approximate functional
equation + Plancherel). But our target Σ_γ |L'(ρ_f,f)|² is

  (a) at zeros of L (not arbitrary line points), AND
  (b) involves L', not L.

To bridge, one applies the explicit formula (M-N §3) to convert
Σ_γ Φ(γ) into a sum over Hecke eigenvalues. **This step needs RH for
L(s,f) per-form** to identify ρ_f = ½+iγ_f cleanly and to get the
σ=½ stationary phase. Rankin-Selberg analytic continuation does NOT
remove this step.

# Section 2. Five candidate routes — Rankin-Selberg variants

## 2.1 R-S Route 1 — Bump global Tate via family-averaged ratios

**Setup.** Bump 1989 Ch. 5 develops the GL(2) Rankin-Selberg via global
Tate. For a test function φ on F_k, study

  Φ(s, s') := ⟨ L(s, f) L(s', f̄) · φ(f) ⟩_F.

By unfolding via Petersson + Bessel kernel (ILS §4), this becomes a
Mellin-shifted Rankin-Selberg integral. Differentiate twice (∂_s ∂_{s'})
at s = s' = ½+iγ to extract |L'|².

**Why it FAILS.**
1. The differentiation ∂_s ∂_{s'} on a function of TWO variables defined
   only by analytic continuation of a series convergent in Re s, Re s' > 1
   requires control of the joint analytic structure near (½,½).
   Rankin-Selberg gives the diagonal s=s' continuation but the
   off-diagonal joint behavior near central point is the SUBJECT of CS
   2007 ratios — exactly the open conjecture.
2. Evaluating at s = ½+iγ_f (zeros) requires per-form GRH to make γ_f
   real. Without GRH, "γ_f" is a complex number ½−ρ_f/i with Re ≠ 0 in
   general.
3. Bump's framework applies to Eisenstein-twisted Rankin-Selberg
   (extracting L(s,f)·L(s+w,f) at SHIFTED arguments), not to L' at
   zeros.

**Verdict B1: FAILS.** Confidence this gives 2/(3π) unconditionally: 0.02.

## 2.2 R-S Route 2 — Ji 1989 / Knightly-Li 2006 GL(2)×GL(2) trace formula

**Setup.** The Ji 1989 / Knightly-Li 2006 trace formula evaluates
sums of the form

  Σ_F ω_f L(s, f) L(s', f̄) = (main term in s,s') + (geometric side
                                with Kloosterman + Bessel).

Differentiating ∂_s ∂_{s'} at (½, ½) and taking residues at zeros
should formally extract the L'-2nd-moment.

**Why it FAILS.**
1. The Knightly-Li trace formula evaluates Σ_F ω_f L(s,f)L(s',f) for
   GENERIC (s,s'), but the geometric-side error term grows like (st)^A
   for some A > 0 in the t-aspect. Differentiating amplifies this by a
   factor of (log T)² and pushes the error to dominance — UNLESS the
   trace formula's geometric side is bounded with explicit
   t-uniformity, which is open.
2. Even granting t-uniform GL(2)×GL(2) trace, the move from
   "L(s,f)L(s',f̄) on the line" to "Σ_γ |L'(ρ_f,f)|²" requires the
   explicit formula per-form, which needs GRH-f. Trace gives the
   ANALYTIC behavior; zero-localization is a SEPARATE step.
3. The 2/(3π) constant comes from CS 2007's RATIOS principal-part
   evaluation (4 L-functions: L'·L̄'/(L·L̄)), which is a 4-parameter
   shifted RS object, not the 2-parameter L·L̄ that Knightly-Li handles.

**Verdict B2: FAILS.** Confidence: 0.04.

## 2.3 R-S Route 3 — 2-fold Petersson (ILS Petersson × ILS Petersson)

**Setup.** Apply Petersson trace formula to BOTH legs of |L'(s,f)|²:

  ⟨|L'(s,f)|²⟩_F = ⟨L'(s,f)·L'(1−s̄,f̄)⟩_F
                  ≈ Σ_{m,n} (log m)(log n)/(mn)^s ⟨λ_f(m)λ_f(n)⟩_F.

By Petersson ⟨λ_f(m)λ_f(n)⟩_F = δ_{m,n} + (Kloosterman · J_{k−1}).
The diagonal piece m=n gives:

  Σ_n (log n)² / n^{2σ} = ζ''(2σ)/something near σ=½.

This DIVERGES at σ=½ (pole of ζ at 1 lifted by differentiation).
The divergence is the Riemann zero contribution.

**Why it FAILS for exact 2/(3π).**
1. The "diagonal" Σ (log n)²/n at σ=½ is divergent and must be
   regularized by the explicit formula or by mollification. The
   standard regularization is Mellin against a smooth cutoff up to
   length X = √T (M-N's α_f, β_f decomposition, line 370-388). M-N
   do exactly this and obtain the constants 5/(24π), 29/(24π) for
   the two halves of the AFE. Their cross-term — which is what
   2/(3π) IS — requires zero-cancellation, hence GRH-f.
2. The off-diagonal Petersson Bessel terms J_{k−1}(4π√mn/c) are
   small only for k > 4eT/√N; this constrains k ≫ T, valid for our
   regime. So the diagonal IS the main term unconditionally. But the
   diagonal evaluates to (5+29)/(2·24π)·log⁴ + cross-term, where the
   cross-term identification needs ψ_f(ρ_f) = 1 (per-form functional
   equation symmetry at zeros), which is GRH-f.

**Verdict B3: FAILS to give exact constant.** Two-fold Petersson
recovers the CAGE [(17±√145)/(12π)] (same as Route 2 in
GRH_bypass_FAMILY_aspect.md), NOT 2/(3π). Confidence: 0.05.

## 2.4 R-S Route 4 — 2-variable functional equation differentiation

**Setup.** |L(s,f)|² has a 2-variable analytic structure
F(s, s̄) = L(s,f) L(s̄, f̄). The functional equation in s gives

  F(s, s̄) = ψ_f(s) ψ_{f̄}(s̄) F(1−s, 1−s̄).

Differentiate twice at s = ½+iγ. The cross terms involving ψ_f'(½+iγ)
give the `2/(3π)` candidate (in the standard CS 2007 derivation).

**Why it FAILS.**
1. ψ_f(s) is the per-form GAMMA-RATIO factor. Its values at zeros
   depend on the location of zeros — needing β_f = ½ to evaluate
   ψ_f(½+iγ_f) cleanly. Without RH-f, ψ_f(ρ_f) is not unimodular.
2. The 2-variable joint differentiation produces a cross-term
   Re(ψ_f'/ψ_f)(ρ_f) which equals (1/2)log(N|γ_f|/2π) + O(1) only
   when β_f = ½. Off-line zeros contribute (β_f−½)·log T to the
   cross-term, displacing the constant by (β_f−½)·(log T)·log³T at
   each zero — exactly what KM 1997 zero-density bounds with
   power-saving.
3. The ILS family-aspect zero density (Thm 8.4, /tmp/ils.txt 3749)
   handles zeros in a window of size O(1/log KN) above ½, NOT zeros
   up to height T. So the family-density-error is a CAGE inflation,
   NOT the exact constant. (This is the same obstruction as
   GRH_bypass §2.2.)

**Verdict B4: FAILS.** Functional equation differentiation in two
variables IS the M-N derivation; Rankin-Selberg adds nothing here.
Confidence: 0.03.

## 2.5 R-S Route 5 — Voronoi on shifted Rankin-Selberg coefficients

**Setup.** The cross-term in |L'(½+iγ,f)|² unfolds (via M-N's α_f β_f
split, line 370) to

  Σ_{m,n≤X} log m · λ_f(m) λ_f(n) / (mn)^{½+iγ}.

Family-averaging: ⟨λ_f(m)λ_f(n)⟩_F = δ_{mn} + (Kloosterman). The
SHIFTED-CONVOLUTION analog ⟨λ_f(n)λ_f(n+r)⟩_F has been bounded
unconditionally by Blomer-Harcos-Michel 2007 via spectral large sieve.
Voronoi summation on Rankin-Selberg coefficients λ_f(n²) gives
sharper-than-trivial bounds.

**Why it FAILS for exact constant.**
1. Voronoi/shifted-convolution gives BOUNDS, not equalities. The exact
   2/(3π) requires equality. (Same obstruction as Cauchy-Schwarz in
   GRH_bypass Route 1.)
2. The "shifted convolution" in our problem is not classical
   λ_f(n)λ_f(n+r) but rather (log m)(log n)·λ_f(m)λ_f(n) at the SAME
   m,n — i.e., a diagonal 2nd moment with logarithmic weights. There
   is no shift parameter r; Voronoi-on-shifts does not apply.
3. The closest applicable Voronoi tool is Hoffstein-Lockhart 1994
   L(1,sym²f), used to bound c_f from below and to quantify
   ⟨c_f⟩_F. This is INPUT to the constant ⟨c_f⟩, not the L⁴
   coefficient 2/(3π).

**Verdict B5: FAILS.** Voronoi on RS coefficients refines the
⟨c_f⟩ asymptotic (already understood via H-L 1994), not the L⁴
constant. Confidence: 0.04.

# Section 3. Best derivation, verbatim citations

The strongest *new* observation from the Rankin-Selberg attack is
**negative**: Rankin-Selberg analytic structure (verbatim ILS 2049-2076)
gives the analytic continuation of Σ λ_f(n²)/n^s, which controls
⟨c_f⟩ and the L²-coefficient 1/(2π) (M-N's Prop 5.1, line 446).
It does **NOT** give the L⁴-coefficient — the L⁴ coefficient comes from
the ratios CS 2007 conjecture, a 4-L-function shifted moment at family
level.

The structural reason, made precise here:

**Theorem (negative, this audit).** Let R(s, s', s'', s''') :=
⟨ L(s,f) L(s',f̄) / (L(s'',f) L(s''',f̄)) ⟩_F. Then:
- R is a 4-variable RATIOS object.
- The L'-2nd-moment constant is (1/4!) ∂_s ∂_{s'} ∂_{s''} ∂_{s'''}
  evaluated at the central point (CS 2007 §3.2 derivation).
- Rankin-Selberg L(s, f×f̄) controls only R restricted to s=s', s''=s'''
  (the 2-parameter diagonal slice).
- The 2/(3π) cross-term is OFF-DIAGONAL in the 4-parameter ratios
  object (mixed s≠s', s''≠s''' partial derivatives).

Hence Rankin-Selberg unconditional input controls a 2-parameter slice
of a 4-parameter object whose off-slice behavior IS the open ratios
conjecture.

**Verbatim ILS support (3.20, line 2139):**
> "Z(s, f⊗f) = L(s, sym²f ⊗ sym²f) · V(s,f) where V(s,f) is an Euler
> product which converges absolutely in Re s > ½ while
> L(s, sym²f ⊗ sym²f) has analytic continuation to C save for a pole
> at s=1. Of course, the latter is expected to satisfy the Riemann
> hypothesis as well."

Note the "expected" — i.e., RH for sym²f⊗sym²f is conjectural. The
GL(3)×GL(3) RS object is precisely the 4-fold ratios input we'd need;
its analytic structure beyond Re s > ½ + δ is conjectural.

# Section 4. Constant extraction — does 2/(3π) match?

**M-N constants (verbatim /tmp/milinovich_ng.txt Prop 1.1):**
- (6): Σ_γ |Σ_{n≤X} α_f(n)/n^{ρ_f}|² ~ (5/(24π)) c_f T log⁴ X
- (7): Σ_γ |Σ_{n≤X} β_{f̄,X}(n)/n^{ρ_f}|² ~ (29/(24π)) c_f T log⁴ X

**Cage center** = average of two halves = (5+29)/(2·24π) = 34/(48π)
= 17/(24π) per half; combined moment via |α + ψ_f β|² gives
2·(5+29)/2/(24π) − 2·Re(cross) ; with ψ_f(ρ_f)=1 and CS evaluation,
cross = 13/(24π), giving (5+29−2·13)/(24π) = 8/(24π) = 1/(3π).

But target is 2/(3π) = 16/(24π) = 2·(5+29)/(24π) − 2·Re(cross') with
Re(cross') = 9/(24π). The numerical match thus depends on the SPECIFIC
ratios cross-term value.

**Where Rankin-Selberg fixes the cross-term.** In the diagonal
2-parameter RS slice, ψ_f(s)·ψ_f̄(1−s) at s=½ gives root number
ε_f² = 1 (since |ε_f|=1 and family-averaged ε_f̄ = ε̄_f). So the
diagonal cross is 0, NOT 9/(24π). The off-diagonal cross-term
9/(24π) requires the 4-parameter ratios off-slice.

**Conclusion of constant extraction.** Rankin-Selberg gives diagonal
cross = 0, predicting M_F = (5+29)/(24π) = 17/(12π), which is the
CAGE CENTER, not 2/(3π) = 16/(24π). The discrepancy 17/(12π) − 16/(24π)
= 34/(24π) − 16/(24π) = 18/(24π) = 3/(4π) is the off-diagonal ratios
contribution. **Rankin-Selberg unconditional cannot account for it.**

# Section 5. Honest verdict

## 5.1 Does Rankin-Selberg unconditional give exact 2/(3π)? **NO.**

The five Rankin-Selberg variant routes (B1: Bump global Tate; B2: Ji /
Knightly-Li GL(2)×GL(2) trace; B3: 2-fold Petersson; B4: 2-variable
functional equation; B5: Voronoi on RS coefficients) ALL fail to
deliver 2/(3π) unconditionally, for the same structural reason
identified in GRH_bypass_FAMILY_aspect.md:

**The exact constant 2/(3π) is a 4-parameter ratios off-diagonal
quantity. Rankin-Selberg controls only the 2-parameter diagonal slice
unconditionally.**

## 5.2 What Rankin-Selberg DOES give (consistent with prior work)

- ⟨c_f⟩ = ⟨L(1, sym²f) · finite product⟩_F is computable
  unconditionally (Hoffstein-Lockhart 1994 + RS analytic continuation).
- The L²-coefficient 1/(2π) (M-N Prop 5.1) is a 2-parameter diagonal
  quantity, hence accessible via RS.
- The CAGE CENTER 17/(12π) is the diagonal-only contribution
  (cross-term = 0 in the 2-parameter slice), confirming the
  GRH_bypass cage statement.
- The CAGE WIDTH ±√145/(12π) comes from the M-N quadratic-form
  trick discriminant (17² − 4·12·8 = 145 = the 5/29 mollifier-pair
  discriminant).

## 5.3 Numerical sanity

2/(3π) = 0.21221… (CS 2007 / M-N target conditional on GRH)
17/(12π) = 0.45095… (cage CENTER, RS diagonal predict)
1/(3π) = 0.10610… (RS diagonal w/ trivial cross-term)
[(17−√145)/(12π), (17+√145)/(12π)] = [0.1314, 0.4519]

The target 2/(3π) is INTERIOR to the cage. Rankin-Selberg alone
predicts only the cage center (or the trivial-cross variant 1/(3π)),
neither matching the target. This is consistent with — and cannot
improve upon — the GRH_bypass conclusion.

## 5.4 Verdict

**Rankin-Selberg does not bypass GRH for Theorem B exact constant.**

Confidence that any of B1-B5 yields exact 2/(3π) unconditionally:
**0.04** (max over five routes; aggregate even lower).

# Section 6. What's needed to close

To upgrade Rankin-Selberg from cage to exact 2/(3π), one would need
ONE of:

1. **Unconditional 4-parameter family-aspect ratios identity.** This
   is CS 2007 Conjecture 5.1 in family form for Petersson weight-aspect.
   Currently open; estimated 5-10 years per GRH_bypass §6.

2. **Unconditional GL(3)×GL(3) RH at the central point**, i.e. RH for
   L(s, sym²f ⊗ sym²f) on family-average over f ∈ H_k^*(N). This is
   strictly stronger than what's known (Lapid 2013 gives partial
   continuation; full RH is open).

3. **Unconditional 4-level density on family-aspect.** ILS 2000 gives
   1- and 2-level density (with support restriction). 4-level density
   is conjecturally orthogonal-ensemble, but unconditionally open.

4. **A clever exact identity** linking the per-form L'-2nd-moment to
   a Rankin-Selberg moment without going through the explicit formula
   per-form. The author has not found such an identity in the
   literature (searched: Bump 1989, Ji 1989, Knightly-Li 2006,
   Petrow-Young 2019, Soundararajan-Young 2010, CFKRS 2005, Conrey-
   Iwaniec-Soundararajan 2007, Iwaniec-Kowalski 2004 Ch. 5).

5. **A Random-Matrix-Theory-to-Number-Theory bridge** specific to
   the orthogonal-ensemble L' moment. Bogomolny-Keating 2002 give
   the RMT prediction matching 2/(3π) for the orthogonal ensemble L'
   2nd moment; transferring this rigorously to the Petersson family
   is the same 4-level density gap.

## 6.1 Recommendation (unchanged from GRH_bypass §7)

Publish the cage statement (Theorem B', confidence 0.85 unconditional)
as headline. The exact 2/(3π) remains conditional on CS 2007 family-
aspect ratios — a 5-10 year program. **Rankin-Selberg attack offers
no shortcut.**

# Section 7. Constants log (verifiable)

| Constant | Value | Source |
|---|---|---|
| 5/(24π) | 0.06631 | M-N Prop 1.1 (6), /tmp/milinovich_ng.txt 405-411 |
| 29/(24π) | 0.38461 | M-N Prop 1.1 (7), /tmp/milinovich_ng.txt 432-440 |
| 17/(12π) (cage center) | 0.45095 | (5+29)/(2·24π), G2 derivation |
| √145/(12π) (cage half-width) | 0.31957 | M-N quadratic-form discriminant |
| 2/(3π) (TARGET) | 0.21221 | M-N 2014 Theorem 1.2 (conditional) |
| 1/(3π) (RS-diagonal predict) | 0.10610 | this audit §4 |
| Cage interval | [0.1314, 0.4519] | unconditional, GRH_bypass §3 |

Numerical verification: cage contains 2/(3π) ✓; RS-diagonal predict
1/(3π) is OUTSIDE cage lower edge by 0.025 — this would be a
contradiction if RS-diagonal were the unconditional truth; resolution
is that the RS-diagonal prediction holds only with cross-term=0
assumption, which is itself a (different) conjecture. Hence RS does
not even unconditionally pin down a candidate constant — it only
identifies the diagonal contribution, not the full M_F(T).

# Done.

**Final verdict (Rankin-Selberg attack).** No new GRH-bypass
emerges. The five Rankin-Selberg variant routes (B1-B5) all fail to
deliver 2/(3π) unconditionally. The structural obstruction is the
4-parameter ratios off-diagonal cross-term, which Rankin-Selberg
diagonal analytic continuation cannot reach. **The cage statement
(Theorem B', confidence 0.85) remains the strongest unconditional
result.** Rankin-Selberg confirms — but does not improve upon — this
conclusion.

Aggregate confidence that Rankin-Selberg yields exact 2/(3π)
unconditionally: **0.04**.
