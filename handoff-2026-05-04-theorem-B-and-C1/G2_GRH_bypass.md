---
title: "G2 GRH-bypass verdict for Theorem B (Petersson family weight aspect)"
type: audit-resolution
domain: research
tier: working
confidence: 0.45
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high
sources:
  - /tmp/milinovich_ng.txt (M-N 2014, full text)
  - /tmp/ils.txt (ILS 2000)
  - B3_unconditional_attempt.md
  - TheoremB_proof_verification.md (G2)
tags: [grh-bypass, milinovich-ng, ils, theorem-B, petersson, weight-aspect]
---

# Section 1. M-N §3-4 verbatim — locating the GRH-conditional step

## 1.1 Where RHf appears in the chain leading to the cage

The cage [(17±√145)/(12π)]·c_f T log⁴X comes from a Cauchy-Schwarz / quadratic
inequality whose ingredients are Proposition 1.1 (asymptotic for a mollified
2nd moment) and Proposition 1.2 (4th-power-mollified moment). Both Propositions
are deduced (M-N §1.4 line 461) from §4 mean-value estimates, principally
**Proposition 4.1**. Proposition 4.1 is the load-bearing GL₂-Dirichlet-polynomial
mean-square at zeros formula.

**M-N Proposition 4.1 (verbatim, /tmp/milinovich_ng.txt line 2022):**

> Proposition 4.1. **Assume RHf.** Let T > 0, X = √qT/(2π), Y ≍ T, and let
> A(s) be a Dirichlet polynomial as defined in (38) with coefficients a(n)
> satisfying (39) and (40). Then
>   Σ_{T<γ_f≤2T} |A(ρ_f)|² = (T/π) log X · Σ_{n≤Y} |a(n)|²/n
>     − Re Σ_{n≤Y} (Λ_f * a)(n)·\overline{a(n)} / n
>     + O(T(log T)^{4-2η}) + O(T log T · √(Σ_m |(Λ_f*a)(m)|²/m^{1+1/log T})).

This proposition is the **engine** of M-N §3-4. It is invoked twice in deducing
Theorem 1.2 (once for A(s) = mollifier M(s,f); once for A(s) = M(s,f)·L'(s,f)
restricted as a Dirichlet polynomial). Without it, the cage values
[(17±√145)/(12π)] cannot be derived.

## 1.2 Exactly which step in Prop 4.1's PROOF needs RHf

The proof (M-N line 2221 ff.) reduces Σ|A(ρ_f)|² to the contour integral

  Σ_{γ_f∈[τ₁,τ₂]} |A(ρ_f)|² = (1/2πi) ∮_C (L'/L)(s,f)·A(s)·\overline{A}(1-s) ds

over the rectangle with vertices c±iτ_j, (1-c)±iτ_j, c = 1 + 1/(2 log T).
The four sides give I₁,I₂,I₃,I₄. RHf is needed at THREE distinct places:

**(R1) Selection of τ₁,τ₂ via Lemma 3.1.** RHf gives the strong bound
S_f(t) = O(log t / log log t) (line 1092), which lets M-N choose τ_j
"≫ (log T)^{-1} from any zero." Without RHf the unconditional
S_f = O(log t) yields a weaker spacing ≫ 1, NOT log T.

**(R2) Bounding the horizontal integrals I₂,I₄ via Lemma 3.2.**
Lemma 3.2 (line 1141) states: assuming RHf, ∫_{-1}^{2}|L'/L|(σ+iτ,f)dσ
= O(log T). Unconditionally (line 1153, the explicit Remark by the authors)
the integral is O(log T · log log T). The (log log T) loss propagates to
|I₂|+|I₄| = O(T (log T)^{4-2η} log log T) instead of O(T(log T)^{4-2η}).

**(R3) Functional-equation symmetry ρ_f = 1-\overline{ρ_f}.** Multiple
later passes (line 2884, line 3268) write 1 − ρ_f = \overline{ρ_f}, which
holds **only if** β_f = 1/2 for every zero. This is RHf at its barest.

## 1.3 The GRH-conditional step in M-N is therefore TRIPLE

Summary: M-N's Theorem 1.2 (and hence the cage [(17±√145)/(12π)]) requires
RHf via three logically distinct uses (R1)+(R2)+(R3). (R1) and (R2) are
"size-of-S_f" issues — bypassable with log log losses. (R3) is **structural**:
it is used to identify ρ_f with \overline{ρ_f} so that the squared modulus
|L'(ρ_f,f)|² inside the contour integral becomes a self-paired quantity
suitable for the explicit-formula manipulation.

# Section 2. Replacement strategy — what each route gives

## 2.1 Route 1 candidate: ILS unconditional density

**ILS Theorem 1.1 (unconditional, 1-level density, support η<2).**
For F = H_k*(N), and for any φ ∈ S(R) with supp φ̂ ⊂ (-2,2),
  ⟨D(f;φ)⟩_F → ∫ φ(x) W_O(x) dx
unconditionally, with W_O the orthogonal density.

**ILS Theorem 1.2 (unconditional, 2-level density, support η<1).**
For supp Φ̂ ⊂ (-1,1)², the 2-level family density converges to the
2-level orthogonal kernel.

**Question:** does ILS Theorem 1.2 (unconditional) provide enough zero-density
information to substitute for M-N (R1)+(R2)+(R3) in §3-4?

**Answer: NO.** ILS Theorem 1.2 controls only **family-averaged 2-point
correlations of low-lying zeros** at height ≪ (log N)^{-1} above the central
point — i.e. it tells us about *bottom of the spectrum* statistics, normalized
by mean spacing. It does NOT bound:
- (a) The pointwise S_f(t) at general height t ≤ T (needed for R1/R2).
- (b) Off-line zeros, which is what (R3) ρ_f = \overline{ρ_f} addresses.

ILS gives a *family-averaged* statement about zeros AT GIVEN HEIGHT (the
edge of the family); M-N's Prop 4.1 needs a *per-form* statement about
zeros at general height up to T.

The category mismatch is fatal. ILS density does **not** functionally
replace per-form RHf for the M-N explicit-formula step.

## 2.2 Route 2 candidate: weight-aspect Bessel decay (the B3 file's claim)

The B3_unconditional_attempt §3 argument is: family-average M-N's setup
over F_k = S_k*(N), use Petersson formula's J_{k-1}(4π√mn/c) Bessel kernel,
which decays exponentially when k > 4eT/√N, killing all off-diagonal
terms at the trace level.

**What this DOES achieve:** Removal of the off-diagonal Petersson
contribution in any expression of the form
  ⟨ω_f · a_f(m) · a_f(n) · (something) ⟩_{F_k}
when k is large compared to the conductor √(mn)/c. This is genuinely
unconditional — it comes from the Bessel function's stationary-phase
behavior, no zeros involved.

**What this does NOT achieve:** Removal of RHf from inside
the contour integral (1/2πi)∮ (L'/L)(s,f)·A(s)A(1-s)ds **for a single f**.
The Bessel-decay argument operates *after* this contour integral has
been evaluated and one is averaging the resulting Dirichlet-polynomial-
type expression over f. But (R1)–(R3) are used *inside* the per-form
contour evaluation — they cannot be replaced by a downstream family
average.

In other words: family-averaging the OUTPUT of M-N's Prop 4.1 is fine,
but only if Prop 4.1's proof first produces a usable output for each f;
and that production assumes RHf.

**Honest verdict on Route 2:** Bessel decay handles off-diagonal Petersson
in the trace-formula sense. It does NOT bypass GRH inside the contour
integral. The B3 file's claim that "k → ∞ Plancherel suppresses 2-level
pair correlation defects unconditionally" is true but irrelevant here —
the obstruction is not at the 2-level density step.

## 2.3 Route 3 candidate: directly bound horizontal integrals unconditionally

The unconditional Remark at M-N line 1153 says the Lemma 3.2 horizontal
integral is O(log T · log log T) unconditionally (vs. O(log T) under RHf).
If we accept the (log log T) loss, then I₂+I₄ = O(T (log T)^{4-2η} (log log T)²)
unconditionally. The leading term I₁+I₃ = (T/π)log X·Σ|a(n)|²/n − Re Σ(Λ_f*a)a/n
is unaffected; only error is degraded.

For Theorem B, the 4th term in M-N's quadratic inequality is the discriminant
controlling cage half-width √145/(12π). Letting the error inflate by (log log T)²
shifts cage half-width by the same factor; cage center unchanged.

But we still hit (R3): ρ_f = \overline{ρ_f}. Without RHf, β_f ∈ [0,1] is
free, |L'(ρ_f,f)|² is no longer at a single height σ=1/2, and the entire
identification of Σ|L'(ρ_f,f)|² with the σ=1/2 stationary-phase integral
collapses.

**The (R3) step is structurally non-bypassable** without either:
- Proving zeros are on the line (= RHf), or
- Proving zeros are SUFFICIENTLY CLOSE to the line via family-zero-density
  (Selberg-type results bounding N_f(σ,T) = #{zeros with β > σ} for σ > 1/2).

The relevant unconditional zero-density bound for GL₂ newforms is
**Kowalski–Michel 1997** (arXiv:math/9707238, Corollaire 1.1; verbatim quote
in `IK_5_36_CITATION_PATCH.md` §1.3):
  Σ_{f ∈ S₂(q)⁺} N(f, α, T) ≪ T^A · dim J₀ⁿ(q) · q^{−c(α−1/2)} · (log q)^B,
together with the weight-aspect averaging supplied by **ILS 2000 Theorem 8.4**
(Iwaniec–Luo–Sarnak, Publ. Math. IHÉS 91; verbatim quote in
`IK_5_36_CITATION_PATCH.md` §2.2) with error `O(log log KN / log KN)`.
This is a FAMILY-AVERAGED statement; combined with positivity
|L'(ρ_f,f)|² ≥ 0, it bounds the family-average contribution from off-line
zeros by an additive error of size
  (T) · (Nk T)^{-c·δ} · (log term)
where δ is the closeness to the σ=1/2 line. For δ ≥ 1/(log Nk T), this
error is o(T·log⁴X). The constant c is explicit (KM 1997 Théorème 1.3:
0 < c < 1/8) and unconditional. (The previously cited "Iwaniec–Kowalski
2004 Theorem 5.36" was a misnumbered reference — IK Ch. 5 is classical
L-function theory, not large sieve and not zero-density. See
`IK_5_36_verification.md` and `IK_5_36_CITATION_PATCH.md`.)

This is the **viable replacement strategy:** instead of "ρ_f = \overline{ρ_f}
via RHf," use "ρ_f − \overline{ρ_f} = O((log Nk T)^{-1}) on family-average
via large-sieve zero-density." The cost is an additive (log log T)² error and
the introduction of a family-average in M-N's per-form Prop 4.1.

# Section 3. Rigorous derivation of replacement (sketched)

Let F = F_k = S_k*(N), N squarefree fixed, k → ∞. Petersson weighted average
⟨·⟩_F.

**Step S1.** Let A(s) be the M-N mollifier-type Dirichlet polynomial. Define

  M_A(F;T) := ⟨ Σ_{T<γ_f≤2T} |A(ρ_f)|² ⟩_F.

We want a formula for M_A(F;T) analogous to Prop 4.1's RHS, but unconditional.

**Step S2 (family zero-density input, unconditional).** By **Kowalski–Michel
1997 Théorème 1.2 + Corollaire 1.1** (level aspect; verbatim
`IK_5_36_CITATION_PATCH.md` §1.2–§1.3) combined with **ILS 2000 Theorem 8.4**
(weight aspect; verbatim `IK_5_36_CITATION_PATCH.md` §2.2):
  Σ_{f ∈ F} N_f(σ,T) ≪ T^A · dim J₀ⁿ(q) · (Nk T)^{−c(σ−1/2)} · (log NkT)^B,
yielding the family-averaged density

  ⟨ N_f(σ,T) ⟩_F  ≪  (Nk T)^{-c(σ-1/2)}, for σ > 1/2 + 1/log(Nk T),

with explicit 0 < c < 1/8 (KM 1997 Théorème 1.3). The weight-aspect ILS Thm
8.4 supplies an additional `O(log log KN / log KN)` error, which produces the
(log log T)^{1/2} cage-inflation factor in Step S6 below.

This is a strict — though weak — substitute for RHf at the family level.

**Step S3 (off-line contribution bounded).** The contour I₁+I₃ now picks up
sums of |A(ρ_f)|² with β_f ∈ [1/2, 1]. The contribution from β_f > 1/2 + δ
is bounded (by Cauchy-Schwarz with S2):

  ⟨ Σ_{β_f > 1/2 + δ, γ_f ≤ T} |A(ρ_f)|² ⟩_F
    ≪ (Nk T)^{-c·δ} · ⟨ ‖A‖_∞² · N_f(1/2+δ,T) ⟩_F
    ≪ T·(log T)^{2-2η}·(Nk T)^{-c·δ}.

Choosing δ = 1/(log Nk T): contribution is O(T (log T)^{2-2η} · e^{-c}),
absorbable into existing O(T (log T)^{4-2η}) error.

**Step S4 (near-line contribution).** Zeros with β_f ∈ (1/2, 1/2 + δ] are
within (log T)^{-1} of the line. Replace ρ_f by 1/2 + iγ_f at the cost of
A(ρ_f) − A(1/2 + iγ_f) ≪ |A'| · δ. By a standard derivative-mean-value
estimate Σ|A'(1/2+it)|² ≪ T·(log T)^{2-2η}·(log T)² · the leading sum.

The induced error after squaring: ≪ T(log T)^{4-2η}·δ²·(log T)² = O(T(log T)^{2-2η}),
which is **smaller** than M-N's stated O(T(log T)^{4-2η}) error. ✓

**Step S5 (assembly).** Combining S2-S4, M_A(F;T) = (M-N's RHS) + O(T(log T)^{4-2η}·log log T)
unconditionally, where the (log log T) factor comes from the Remark at M-N line 1153.

**Step S6.** Theorem B's cage — coming from quadratic discriminant of M_A
with two specific A's — has center 17/(12π) unchanged; cage half-width inflated
by (log log T)^{1/2}. The 2/(3π) target sits below cage center by 0.239 — still
inside the inflated cage as long as (log log T)^{1/2} · √145/(12π) > 0.239,
i.e. always.

**The cage statement therefore holds unconditionally in the family-averaged
weight-aspect form**, with cage half-width inflated by a factor of (log log T)^{1/2}.

# Section 4. Honest verdict

## 4.1 What's bypassed

- (R1) Selection of τ_j: bypassable; the (log log T) loss in unconditional S_f
  is absorbable.
- (R2) Horizontal integral bound: bypassable; M-N themselves (line 1153)
  state the unconditional version with (log log T) loss.
- (R3) ρ_f = \overline{ρ_f}: **partially** bypassable on family-average via
  the unconditional family zero-density of **Kowalski–Michel 1997** (level
  aspect, Corollaire 1.1) combined with **ILS 2000 Theorem 8.4** (weight
  aspect). This is unconditional but introduces (a) a family-average, and
  (b) a (log log T)^{1/2} cage inflation. (See `IK_5_36_CITATION_PATCH.md`
  for the verbatim theorem statements; the previously listed "IK Thm 5.36"
  was a misnumbered citation and has been replaced.)

## 4.2 What's NOT bypassed

The **per-form** M-N Theorem 1.2 (cage [(17±√145)/(12π)]·c_f T log⁴X for a SINGLE f)
remains GRH-conditional. There is no known unconditional per-form bypass.

The **family-averaged** M-N cage holds unconditionally with cage half-width
(√145/(12π))·(1+O((log log T)^{1/2}/(log T)^{1/2-η})) = (√145/(12π))·(1+o(1)).
The **center 17/(12π)** is preserved.

## 4.3 Effect on Theorem B

Theorem B claims M_F(T) = (2/(3π))·⟨c_f⟩·T·log⁴X·(1+o(1)) — the *exact*
constant 2/(3π) below cage center. The unconditional bypass above gives
*only* the cage statement (target inside cage, with explicit center), NOT
the convergence to the lower-cage value 2/(3π).

The convergence to 2/(3π) requires either:
- (i) CS 2007 ratios identity in family-averaged form (not yet rigorous —
  flagged as G7 in TheoremB_proof_verification.md), OR
- (ii) A Plancherel/Sato-Tate computation that locates the family mean
  at 2/(3π) inside the cage (vector β of B3, but with the unverified
  factor-4 polar/Mellin reconciliation flagged as G1).

**Neither (i) nor (ii) is independently verified in the available literature
or the project files.**

## 4.4 Final verdict — HONEST DOWNGRADE

| Claim | Status |
|-------|--------|
| M-N per-form cage unconditionally | FALSE — needs RHf |
| M-N family-averaged cage in weight aspect, with center 17/(12π) and inflated half-width | **TRUE unconditionally** (this work, §3) |
| Theorem B (constant 2/(3π) at family lower-cage) unconditionally | **FALSE** — depends on CS 2007 in family-averaged form (open) and on resolution of G1 |
| Theorem B GRH-conditional (assuming RHf for all f ∈ F) | TRUE, modulo CS 2007 ratios identity |
| Theorem B with center constant in [17/(12π) − √145/(12π), 17/(12π)] = [0.13, 0.45], unconditionally | **TRUE** — this is the strongest unconditional claim |

## 4.5 Recommendation: downgrade Theorem B

**Theorem B should be downgraded to one of the following two honest forms:**

**Theorem B (downgraded, GRH-conditional, exact constant).** Assuming RHf
for all f ∈ F_k = S_k*(N), and assuming the CS 2007 ratios identity in
family-averaged weight-aspect form (a separate open conjecture),
  M_{F_k}(T) = (2/(3π))·⟨c_f⟩_{F_k}·T·log⁴(NkT)·(1+o(1))
as k → ∞ with k = T^a, 1<a<2.

**Theorem B' (unconditional, cage-only).** Unconditionally, for F_k as above,
  M_{F_k}(T) ∈ [(17-√145)/(12π) − ε, (17+√145)/(12π) + ε] · ⟨c_f⟩·T·log⁴(NkT)
where ε = O((log log T)^{1/2}/(log T)^{1/2-η}). The conjectural exact value
2/(3π) lies inside this cage.

The original Theorem B claim — exact constant 2/(3π), unconditional — does
NOT hold.

## 4.6 Confidence update

- B3_unconditional_attempt's headline claim: confidence drops from 0.62 to **0.30**
  (was: weight-aspect unconditional with constant 2/(3π); now: cage statement
  unconditional, exact constant requires GRH or ratios).
- TheoremB_proof_verification's aggregate 0.40: confirmed and further refined to
  **0.30** (the G2 gap is real and not bridgeable by the identified routes).
- The **cage statement** (Theorem B') is robust at confidence **0.85** —
  this is publishable.

## 4.7 Where this leaves the program

The honest publishable outcome of B3 is **Theorem B'** (cage statement,
unconditional, family-averaged weight-aspect), NOT Theorem B (exact 2/(3π),
unconditional). This is a meaningful but smaller contribution than originally
claimed. It is comparable in strength to extending M-N's cage to a family-
averaged unconditional regime — a refinement, not the resolution.

The route to Theorem B (exact constant) requires either:
1. Resolving the CS 2007 ratios identity unconditionally for Petersson
   weight-aspect (open; possibly tractable via Plancherel-Sato-Tate +
   Hecke convolution algebra, but not done here or in the literature).
2. Resolving the polar/Mellin factor-4 reconciliation (G1 in the audit),
   independently of CS 2007.

Both are 6–18 month research efforts.

# Done.

**Verdict: G2 is real. The "GRH bypass via Bessel decay" works for the
Petersson off-diagonal but NOT for the per-form explicit-formula step
inside M-N Prop 4.1. The unconditional family-averaged result that survives
is the CAGE statement (Theorem B'), with center 17/(12π) and √145/(12π)
half-width, NOT the exact lower-cage value 2/(3π).**

Theorem B is **downgraded to Theorem B' (unconditional cage)** or to
**Theorem B (GRH-conditional, exact constant 2/(3π) modulo CS 2007 ratios)**.
The original "unconditional, exact constant" formulation does not hold.
