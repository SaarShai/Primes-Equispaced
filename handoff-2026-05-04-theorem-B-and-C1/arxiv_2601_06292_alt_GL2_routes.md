---
title: "arXiv:2601.06292 — Alternative GL(2) extension routes (independent audit)"
type: audit
domain: research
tier: working
confidence: 0.35
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (alt-route, parallel to main verifier)
sources:
  - /tmp/2601.06292.txt (Durkan-Hughes-Pearce-Crump 2026, full PDF text)
  - GRH_bypass_FAMILY_aspect.md (5 prior failed routes, baseline)
  - Theorem_B_literature_research.md
tags: [grh-bypass, theorem-B, durkan-hughes-pearce-crump, gl2-extension, mixed-derivatives]
---

# Section 1. arXiv:2601.06292 structural summary (verbatim from PDF)

## 1.1 Object and result

Verbatim (lines 17-26):

> "I(µ, ν) := I(µ, ν; T ) = Σ_{0<γ≤T} ζ^(µ)(ρ)ζ^(ν)(1 − ρ) … We will establish a full asymptotic expansion for this sum, with a power-saving error term under the Riemann Hypothesis."

Theorem 1 (lines 188-206):

> "I(µ,ν) = (T/2π) · P_{µ,ν}(log(T/2π)) + O( T · exp(−C √log T) )"

Under RH the error is O(T^{1/2+ε}).

## 1.2 Proof structure (verbatim outline, §3 lines 464-528)

The technique is a direct contour-integral / Cauchy-residue derivation:

**Step A.** Cauchy on the rectangle R with vertices c±i, c±iT (c = 1+1/log T):
> "I(µ, ν) = (1/2πi) ∮_R (ζ′/ζ)(s) ζ^(µ)(s) ζ^(ν)(1 − s) ds = I_1 + I_2 + I_3 + I_4"

**Step B.** I_4 = O(1), I_2 = O(T^{1/2+ε}) (Gonek), so the work is in I_1 (right vertical) and I_3 (left vertical).

**Step C** (right vertical, §4). Apply functional-equation expansion (Lemma 1):
> "ζ^(ν)(1−s) = (−1)^ν χ(1−s) Σ_k C(ν,k) (log(t/2π))^{ν−k} ζ^(k)(s) + O(t^{σ−3/2}(log t)^ν)"

This converts I_1 into ν+1 integrals each of the shape
∫ (ζ′/ζ)(c+it) ζ^(µ)(c+it) ζ^(k)(c+it) χ(1−c−it) (log(t/2π))^{ν−k} dt.

**Step D** (Gonek Lemma 2 / stationary phase, lines 706-746): reduces each integral to a finite Dirichlet sum
Σ_{n≤T/2π} A_n^{(µ,k)} (log n)^{ν−k} + O(T^{c−1/2}(log T)^m) with
A_n^{(µ,k)} = (−1)^{µ+k+1} Σ_{n_1n_2n_3=n} Λ(n_1) (log n_2)^µ (log n_3)^k.

**Step E** (Perron + residue, Lemma 3-4, lines 800-983). Perron gives
Σ_{n≤Y} A_n^{(µ,k)} = Res_{s=1} [(ζ′/ζ)(s) ζ^(µ)(s) ζ^(k)(s) · Y^s/s] + E_1(Y,V).

The unconditional error E_1 = Y exp(−C √log Y) **comes from the classical zero-free region**: lines 1062-1063,
> "As noted in Titchmarsh [22, p.54], there exists some absolute constant C > 0 such that for c′ = 1 − C/log V, any zero of ζ(s) lies a distance ≫ 1/log V away from the line between c′ − iV and c′ + iV."

Combined with Gonek's bound (ζ′/ζ)(σ±iV) ≪ (log V)^2 uniformly for −1 ≤ σ ≤ 2 (line 1067).

**Step F.** Partial summation reinserts (log n)^{ν−k}.

## 1.3 The KEY structural ingredients (the "engine")

For the unconditional power-saving, the proof uses ONLY:

(E1) Functional equation ζ(s) = χ(s)ζ(1−s) and its derivative expansion (Lemma 1).
(E2) Stationary phase (Gonek Lemma 5 — purely analytic, works for any
     Dirichlet series with bounded coefficients).
(E3) **Perron's formula on the diagonal Dirichlet series** Σ A_n^{(µ,k)} n^{−s}
     which equals (−1)^{µ+k+1} (ζ′/ζ)(s) ζ^(µ)(s) ζ^(k)(s).
(E4) **Classical zero-free region of ζ** (Korobov-Vinogradov is not used; the
     standard de la Vallée Poussin zero-free region C/log V suffices for the
     exp(−C√log T) error).
(E5) Gonek's uniform (log V)^2 bound for ζ′/ζ on −1 ≤ σ ≤ 2 outside zeros.
(E6) Convexity bounds for ζ^(µ) inside critical strip (Cauchy estimate from
     Ivić's bound, line 1079).

The proof is **EXTREMELY classical**. There is no new analytic ingredient.

# Section 2. Five alternative GL(2) extension routes

The target is GL(2): unconditional asymptotic for
  Σ_{γ_f ≤ T} L^(µ)(ρ_f, f) L^(ν)(1−ρ_f, f),    f a fixed Hecke newform of level N, weight k.

The decisive question for each route: **does the engine survive when (ζ, ζ′/ζ) is
replaced by (L(s,f), L′/L(s,f))?**

## 2.1 Route A — L-function factorization at the central point

**Idea.** If L(s,f) factored as ζ(s+α)·ζ(s+β)·(elementary), one could apply
arXiv:2601.06292 to each ζ-factor with shifted argument and recombine.

**Reality check.** L(s,f) for a non-CM cuspidal newform is a primitive degree-2
L-function — by Booker (2003) and Kaczorowski-Perelli (Selberg class theory),
**it does not factor over the Selberg class**. The Euler product
∏_p (1 − a_p p^{−s} + p^{1−2s})^{−1} does not split into degree-1 factors with
real shifts.

For CM forms L(s,f) = L(s, ψ) with ψ a Hecke Grossencharacter — this IS a
degree-1 L-function over an imaginary quadratic field, but that's a Hecke
L-function over Q(√−d), not a product of ζ-factors over Q.

**Verdict: ROUTE A FAILS structurally.** Cannot reduce GL(2) to ζ-factors.

## 2.2 Route B — Eisenstein-series approximation

**Idea.** For Eisenstein series E(z, s) on SL(2,Z)\H, the L-function attached to
E(·, 1/2 + it) factors as ζ(s + it)·ζ(s − it). Apply the engine of
arXiv:2601.06292 to each shifted ζ.

**This actually works for the Eisenstein case.** Let
  L_E(s, t) := ζ(s+it) ζ(s−it).
Then
  L_E^(µ)(ρ_E, t) L_E^(ν)(1−ρ_E, t)
expands to a finite linear combination of products
  ζ^(a)(ρ_E + it) ζ^(b)(ρ_E − it) ζ^(c)(1−ρ_E + it) ζ^(d)(1−ρ_E − it),
and the zeros ρ_E of L_E are zeros of ζ(s+it) ∪ zeros of ζ(s−it) — i.e. shifted
zeros of ζ. Summing over γ_E ≤ T splits into two sums, each amenable to the
DHP-C engine with shifted argument.

The shifted DHP-C analog is just (4.1)-style functional equation replaced by
χ(s+it) variant — which exists with the same exp(−C√log T) zero-free region
(translates of de la Vallée Poussin region cover any fixed t). Step E (Perron
on Σ Λ(n)(log n)^µ ... n^{−s−it}) still terminates at residue at s = 1−it,
which is a regular pole giving the same polynomial structure.

**Pre-existing literature: Conrey 1989** "More than two-fifths of the zeros of
ζ are on the critical line" essentially uses the Eisenstein-mollified sum. **The
DHP-C engine extends to the shifted ζ pair without new ingredients.**

**But the prize is GL(2) cuspidal, not Eisenstein.**

The Eisenstein L-function is degree 2 but reducible. The cuspidal L(s, f) is
**primitive** and irreducible — the leap from Eisenstein to cusp is exactly the
content of the spectral theory of automorphic forms. There is no continuous
deformation from one to the other within the same engine (see Route C below).

**Verdict: ROUTE B WORKS for Eisenstein — provides a FORMAL ANALOG, but does
NOT extend to cuspidal L. It establishes the technique reaches "GL(1)×GL(1)
isobaric" not "GL(2) cuspidal".**

This is non-trivial: it shows the DHP-C engine is degree-1-shift-extensible.
But it does not unconditionally resolve Theorem B.

## 2.3 Route C — Holomorphic-to-Maass / weight-k → ∞ interpolation

**Idea.** Maass forms of Laplace eigenvalue 1/4 (the "ζ analog") have explicit
spectral parameter; holomorphic newforms of weight k are limits k → ∞ in the
Eichler-Shimura / principal series sense. If DHP-C handles the Maass case at
parameter 0, interpolate.

**Reality check.**

(i) DHP-C does NOT handle the Maass case. It handles ζ on Q. The Selberg zeta
    function for SL(2,Z)\H has a different proof structure (Selberg trace
    formula, not Cauchy-Perron). The "Maass form ζ-analog" attached to
    SL(2,Z)\H is the Selberg zeta function Z_Γ(s), whose zeros are 1/2 ± ir_n
    where r_n^2 + 1/4 are Laplace eigenvalues. That object has Σ_ρ properties
    radically different from ζ — its zero-counting is N_Γ(T) ~ T²/4π (Weyl
    law), not (T/2π) log(T/2π).

(ii) Even granting (i), the interpolation k → ∞ is over weight, not over
     spectral parameter. The standard test-function deformation (Iwaniec-Luo-
     Sarnak) sends k → ∞ in the holomorphic family — but the SUM over zeros
     of L(s,f) for fixed f does NOT vary continuously with k because the zero
     set changes discontinuously between weights.

(iii) The Petersson trace formula DOES interpolate well over weight, but it
      averages over f within fixed weight — not what we want.

**Verdict: ROUTE C FAILS — the interpolation hypothesis is incoherent. There
is no single object from which both ζ-zeros and L(s,f)-zeros emerge as limits.**

## 2.4 Route D — Test-function approach with orthogonal symmetry

**Idea.** DHP-C uses no special test function structure — it's pure contour +
Perron. Replace the contour integral by a smoothed version Σ φ(γ/T)·... with
test function φ adapted to the orthogonal symmetry of the GL(2) holomorphic
family.

**Two distinct sub-routes:**

(D1) **Per-form smoothed**. Replace I(µ,ν;T) by Σ_{γ_f} φ(γ_f/T) L^(µ)(ρ_f,f) L^(ν)(1−ρ_f,f).
The DHP-C engine via Cauchy + functional equation still applies — but Step C
(functional equation expansion) for L(s,f) uses the GL(2) functional equation:
L(s,f) = ε_f · N^{1/2−s} · γ(s,f)/γ(1−s,f) · L(1−s, f̄).
The χ(1−s) factor now has γ-quotient = (Γ_C(s+(k−1)/2)/Γ_C(1−s+(k−1)/2)). The
analog of Lemma 2 (stationary phase) goes through with the GL(2) gamma factor.

The blocker is **Step E**, Perron + residue. The Dirichlet series produced
after stationary phase is
  Σ_n B_n^{(µ,k)}(f) n^{−s},    B_n = (−1)^{...} Σ_{n_1n_2n_3=n} Λ_f(n_1) (log n_2)^µ (log n_3)^k a_f(n_2) a_f(n_3) (?)
where the sum has L(s,f)-arithmetic factors. Specifically, this Dirichlet
series equals (L′/L)(s,f) · L^(µ)(s,f) · L^(k)(s,f), which has a TRIPLE pole
type singularity at... wait: L(s,f) does NOT have a pole at s = 1 — it is
ENTIRE for cuspidal f. So Step E's residue computation produces ZERO (no pole
to extract).

This is the structural showstopper: the DHP-C asymptotic comes from the simple
pole of ζ at s=1 producing the (T/2π) main term. For cuspidal L(s,f), there
is no s=1 pole, so the residue method gives no main term, only error terms.

**The actual main term for Σ L'(ρ_f,f) L'(1−ρ_f,f) must come from a different
source** — and this is exactly the Conrey-Snaith / Milinovich-Ng family
heuristic that gives ((T/2π) log²(T/2π))/12 + lower, where the log² (not log^4
as for ζ) comes from the orthogonal symmetry type SO(odd)/SO(even) of the GL(2)
holomorphic family in Katz-Sarnak.

(D2) **Family-averaged**. Average over f ∈ H_k(N) in the harmonic-weighted
sense. Now the residue at s=1 of an *averaged* L′/L · L^(µ) · L^(k) does
appear — because Σ_f ω_f a_f(p)² = δ-function + Petersson off-diagonal, and
the diagonal piece does have a pole at s=1 from Σ_p (log p)/p^s ~ 1/(s−1).

This is exactly what Milinovich-Ng (2014) analyze for the family-averaged
L'-second-moment. They get the right main term **conditionally on RH_f**. The
question is whether DHP-C's unconditional engine bypasses RH_f.

The answer is: **NO, because Step C (Lemma 1, the functional equation
derivative expansion) requires the integrand on the line σ = c > 1 to be
written as an absolutely convergent Dirichlet series**, which works on
σ > 1 but the FE jump to σ < 1 picks up zeros — and the analog of Step E's
contour push past the zero-free region of L(s,f) requires the zero-free
region for L(s,f).

**The classical zero-free region for L(s,f) cuspidal IS known unconditionally**:
de la Vallée Poussin region L(σ+it, f) ≠ 0 for σ > 1 − c/log(t·N·k) (Iwaniec
2002 Thm 5.10, see also Goldfeld 2006 §5). This is the same shape as for ζ.

So Step E adapts. The remaining issue: Gonek's (log V)^2 bound for ζ′/ζ on
−1 ≤ σ ≤ 2 outside zeros — the GL(2) analog (L′/L)(σ+it,f) ≪ (log V)^2 also
holds in the corresponding region, by the same proof (logarithmic derivative
of an L-function with classical zero-free region).

**This means Route D2 (family-averaged DHP-C with cuspidal L) MAY actually
work.** Let me check the residue structure more carefully.

The averaged Dirichlet series at s = 1:
  ⟨ (L′/L)(s,f) · L^(µ)(s,f) · L^(k)(s,f) ⟩_F
For f cuspidal, individual L(s,f) is entire, so each f has no s=1 pole. The
average might still develop a "diagonal" pole from Petersson:
  Σ_f ω_f a_f(m) a_f(n) = δ_{m=n} + Bessel-decay off-diagonal
substituted in the triple product gives a diagonal Dirichlet series whose
Mellin transform has a pole at s=1 from the Λ(n_1)/n_1^s factor.

**This is genuinely promising** — the DHP-C engine, when family-averaged via
Petersson, could give an unconditional family-averaged GL(2) main term.

But: this is exactly the Milinovich-Ng family route, where the OBSTRUCTION
identified in GRH_bypass_FAMILY_aspect.md (R3) was **per-form ρ_f vs ρ̄_f
identification** — which IS bypassed in family aspect (F1). So Route D2 might
produce the family-averaged main term unconditionally.

The remaining obstruction: the EXACT CONSTANT 2/(3π) for Theorem B. The DHP-C
engine produces a polynomial whose leading coefficient is the residue
computation. For the family-averaged GL(2), this leading coefficient is
**exactly the Milinovich-Ng cage** — not necessarily the conjectured
2/(3π) = 0.21221.

**Verdict: ROUTE D2 plausibly delivers an unconditional family-averaged
ASYMPTOTIC, but the coefficient is the cage, not 2/(3π).** The exact constant
requires additional input (Conrey-Snaith CUE/SO heuristic, which is conjectural).

This matches the failure pattern of the 5 prior routes documented in
GRH_bypass_FAMILY_aspect.md.

## 2.5 Route E — Diagonal-only GL(2) via Petersson + DHP-C engine

**Idea.** Apply DHP-C engine to JUST the diagonal piece of the Petersson trace
formula, treating off-diagonal Bessel-decay as error.

**Setup.** Petersson:
  Σ_f ω_f a_f(m) a_f(n) = δ_{m,n} + 2π i^{−k} Σ_{c≥1} S(m,n;c)/c · J_{k−1}(4π√(mn)/c)

The Bessel sum is bounded by (mn)^{1/2}/c^{1−ε} via Weil + standard estimates,
giving for m,n ≤ T:
  off-diagonal contribution ≤ T^{1+ε} / (small power)
which IS smaller than the expected main term (T/2π)·log²(T/2π) provided we
gain a small power of T from c-summation.

**Problem.** The product L^(µ)(ρ_f,f)·L^(ν)(1−ρ_f,f) involves SQUARE-ROOT
many a_f-coefficients (after taking the residue), so the off-diagonal isn't
just (mn)^{1/2}. The actual triple-coefficient sum is
  Σ_{n₁n₂n₃ = n} Λ(n_1) a_f(n_2) a_f(n_3) (log)·(log)
and the off-diagonal Bessel decay gives
  Σ_{c} S(m,n;c)/c · J_{k−1}(4π√(mn)/c) · |a_f(n_2)·a_f(n_3) shifted| ≪ ?

Whatever the exact bound, it's almost certainly **at most (mn)^{1/2−δ}** for
some δ > 0 by Weil + spectral large sieve (Deshouillers-Iwaniec 1982). For
mn ≤ T^2, this gives error ≤ T^{1−δ+ε}, which IS power-saving.

**This is essentially the same as Route D2 family-averaged, expressed in
Petersson language.** The diagonal δ_{m,n} piece reproduces the Σ_n A_n / n^s
Dirichlet series structure, and the off-diagonal is power-saving.

**Verdict: ROUTE E coincides with ROUTE D2.** It is a re-packaging, and gives
the family-averaged main term unconditionally (assuming the off-diagonal
analysis goes through, which is standard).

# Section 3. Best route — full derivation attempt (Route D2/E)

I attempt the family-averaged DHP-C engine for the GL(2) holomorphic family.

## 3.1 Setup

Let H_k(N) = orthonormal basis of weight-k level-N newforms. Define
  J(µ,ν;T) := Σ_{f∈H_k(N)} ω_f Σ_{γ_f≤T} L^(µ)(ρ_f, f) L^(ν)(1−ρ_f, f)
where ω_f = Γ(k−1)/((4π)^{k−1}⟨f,f⟩) are harmonic weights.

## 3.2 Cauchy contour (Step A analog)

For each f, take the DHP-C rectangle. Then by Cauchy:
  Σ_{γ_f≤T} L^(µ)(ρ_f,f) L^(ν)(1−ρ_f,f) = (1/2πi) ∮_R (L'/L)(s,f) L^(µ)(s,f) L^(ν)(1−s,f) ds.

## 3.3 Functional equation expansion (Step C analog)

L(s,f) = ε_f N^{1/2−s} γ(s,f)/γ(1−s,f) · L(1−s, f̄). Differentiating:
  L^(ν)(1−s,f) = (−1)^ν χ_f(1−s) Σ_{k=0}^ν C_f(ν,k,t) L^(k)(s, f̄) + error,
where C_f(ν,k,t) is a polynomial in log(tN/2π) of degree ν−k (analog of
Lemma 1 with t replaced by tN/2π for level N).

## 3.4 Stationary phase (Step D analog)

Gonek's Lemma 5 is purely analytic and applies. The χ_f(1−c−it) factor
oscillates, and Gonek's bound localizes the integral to n ≤ tN/2π in the
Dirichlet series Σ b_n^{f,(µ,k)} n^{−c−it} where
  b_n^{f,(µ,k)} = (−1)^{...} Σ_{n₁n₂n₃=n} Λ_f(n_1) λ_f(n_2)(log n_2)^µ λ_f(n_3)(log n_3)^k

Here Λ_f is the f-von-Mangoldt: −L'(s,f)/L(s,f) = Σ Λ_f(n)/n^s, and λ_f are
Hecke eigenvalues.

## 3.5 Family average + Perron (Step E analog) — the critical step

Sum over f with Petersson weights:
  Σ_f ω_f b_n^{f,(µ,k)} = (−1)^{...} Σ_{n₁n₂n₃=n} Λ̃(n_1, n₂, n₃) (log n_2)^µ (log n_3)^k
where Λ̃ is Petersson-averaged. By Petersson:
  Σ_f ω_f λ_f(n_2) λ_f(n_3) = δ_{n₂=n₃} + Bessel.

The DIAGONAL piece (n_2 = n_3) gives
  Σ_n (1/n^s) · Σ_{n₁ n²₂=n} Λ_f-diag(n_1) (log n_2)^{µ+k}
The averaged f-von-Mangoldt for a specific f remains:
  ⟨Λ_f(n_1)⟩_F = ?
This is the key issue. **Λ_f(p^j) = α_p^j + β_p^j (Satake) and is NOT
naturally δ-function** under Petersson. It's a Hecke trace.

So Σ_f ω_f Λ_f(n_1) λ_f(n_2)² is a **deeper trace** that doesn't simplify to
ζ-arithmetic.

The averaged Dirichlet series is roughly
  ⟨ (L'/L)(s,f) ⟩_F · ⟨ L^(µ)(s,f) L^(k)(s,f) ⟩_F  (factorization heuristic)
which is NOT the residue of a single nice object — it's a triple product
where the (L'/L) factor has zero-mean over f (by Plancherel) up to lower
order, and the L^(µ)·L^(k) factor has the Rankin-Selberg pole.

**The pole structure under family average:**
- Σ_f ω_f L(s,f)·L(s,f̄) has a pole at s=1 from Rankin-Selberg L(s, f×f̄) ~
  ζ(s)·L(s, sym²f), giving residue prop. to L(1, sym²f).
- The triple product Σ_f ω_f (L'/L)(s,f) L^(µ)(s,f) L^(k)(s,f) has more
  delicate analytic structure.

**This computation is exactly the Milinovich-Ng (2014) computation in their
§4.** Their Prop 4.1 gives:
  J(µ,ν;T) = (T/2π) · Q_{µ,ν,f}(log(T·N/2π)) + (error)
**under RH_f**, where Q is a polynomial with leading coefficient
(L(1,sym²f))^{...}/(... )

The unconditional version of M-N Prop 4.1 fails on (R3) — see G2_GRH_bypass.md.
**(R3) per-form is structural and unbypassable** as documented in
GRH_bypass_FAMILY_aspect.md §1.1.

The DHP-C engine provides the analytic pipeline for ζ — **but the f-von-Mangoldt /
Petersson-averaging step has no DHP-C analog**, because DHP-C is mono-arithmetic
(works with one arithmetic function Λ from one L-function, ζ).

## 3.6 The structural obstruction (specific to DHP-C extension)

DHP-C Step E reduces to a **single residue at s=1** of (ζ′/ζ)·ζ^(µ)·ζ^(k).
This residue is finite because ζ has order-1 pole at s=1 and ζ^(µ) has
order-(µ+1) pole at s=1.

For GL(2) cuspidal: L(s,f) is **entire**. To get a pole at s=1 we need to
average — but then the averaged object is L(s,f×f̄) (Rankin-Selberg) which
has order-1 pole. The triple product (L'/L)·L^(µ)·L^(k) under Petersson average
becomes (∂/∂s log L(s,f)) · L^(µ)(s,f) L^(k)(s,f̄) averaged — a quartic-in-L
object, NOT a triple product of a single L-function.

**The DHP-C engine does NOT extend to this quartic-averaged object.** There is
no Perron formula for the average; the residue is taken AFTER averaging, but
the averaging mixes the analytic structure (introduces Rankin-Selberg
correlations) so the pole structure is genuinely different.

# Section 4. Verdict on unconditional Theorem B-exact via this approach

**The DHP-C arXiv:2601.06292 engine, by all 5 alternative extension routes,
does NOT unconditionally deliver the EXACT GL(2) Theorem B constant 2/(3π).**

Specifically:
- Route A (factorization): impossible (L primitive).
- Route B (Eisenstein): works only for Eisenstein L = ζ-shift product; gives
  the GL(1)×GL(1) isobaric case unconditionally, but NOT cuspidal.
- Route C (Maass/k→∞ interpolation): incoherent — no continuous family.
- Route D2 (test-function/family-average): hits the SAME obstruction as
  Milinovich-Ng — the engine reduces to averaging quartic L-products, where
  DHP-C has no analog.
- Route E (Petersson diagonal): equivalent to D2.

**The strongest unconditional output is Route B: arXiv:2601.06292's engine
generalizes to Eisenstein L-functions L(s, E) = ζ(s+α)·ζ(s+β), giving an
unconditional asymptotic for Σ L^(µ)(ρ_E)·L^(ν)(1−ρ_E) where ρ_E ranges over
zeros of ζ(s+α)·ζ(s+β). This is a non-trivial new result (a GL(1)×GL(1)
isobaric extension), but it is NOT Theorem B, which is GL(2) cuspidal.**

## 4.1 Where the DHP-C engine actually saves work

For the prior failed family routes (G2 → 5 routes in GRH_bypass_FAMILY_aspect.md),
DHP-C provides a **cleaner alternative to the contour estimate (R2)**: where
M-N Prop 4.1 used Lemma 3.2 with bound O(log T · log log T), DHP-C's Lemma 4
gives a clean exp(−C√log T) bound. So DHP-C upgrades **(R2) from cosmetic
log log loss to power-saving**.

But (R3) — the per-form ρ_f vs ρ̄_f identification — remains the structural
blocker. DHP-C does not address (R3) because the ζ analog of (R3) is trivially
satisfied (zeros of ζ are symmetric under s → 1−s̄ under RH; without RH the
DHP-C proof avoids this by working directly on the contour, never needing
ρ vs ρ̄ identification).

**For GL(2) cuspidal, the analog of "DHP-C avoids ρ vs ρ̄" requires the
contour to be pushed past the GL(2) zero-free region — which is known but
gives the WRONG MAIN TERM** (no s=1 pole for cuspidal L). To recover a main
term, you must either (a) use RH_f (pushed contour to σ=1/2), or (b) family-
average (which introduces Rankin-Selberg). DHP-C's avoidance of (R3) trick
does not transfer.

# Section 5. Honest blockers

1. **L(s,f) is entire for cuspidal f.** The DHP-C engine's main term comes from
   Res_{s=1}, which is identically zero for entire L. Without a pole, the
   asymptotic is hidden in the lower-order zero-free-region error term — which
   is too small to give a (T log² T) main term.

2. **Family averaging introduces Rankin-Selberg correlations** that the
   DHP-C engine does not handle. Specifically Σ_f ω_f a_f(p)² ≠ a Hecke
   eigenvalue trace amenable to Perron on a single L-function.

3. **The exact constant 2/(3π) requires Conrey-Snaith CUE matrix-integral
   evaluation**, which is conjectural. No DHP-C-style classical engine has
   ever produced an exact Katz-Sarnak constant unconditionally — even for ζ
   (where DHP-C does work), the polynomial coefficients involve Stieltjes γ_n
   from ζ around s=1, which is the ζ-analog of CUE constants. For GL(2) the
   analog is L(1, sym²f), L'(1, sym²f), etc., which are not unconditional
   constants.

4. **The 5 prior failed routes (HB-4th, KMV-2002, ILS-density, S-Y-twist,
   Petrow-Young cubic) all have this same shape:** they bound or evaluate
   simpler family-averages but leave the EXACT-constant gap. DHP-C is the 6th
   such route and exhibits the same gap.

# Section 6. Comparison to main verifier's verdict

At time of writing (2026-05-03), the main verifier output file
`/Users/saar/Farey 4.7 solutions/arxiv_2601_06292_analysis.md` does **not yet
exist**. So no direct comparison is possible from this side.

**Predicted main verifier conclusion** (based on the same paper structure): the
direct generalization will hit either obstruction (1) or (2) above. Most likely
the main verifier will identify obstruction (2) — Petersson-averaging breaks
the single-L-function Perron pipeline.

**Cross-reference protocol when main verifier reports:**
- If main verifier finds a working direct extension → recheck obstruction (1)
  carefully, since L cuspidal entire is a hard fact.
- If main verifier confirms structural failure → both audits agree, and the
  obstruction is GENUINE.
- If main verifier reports ambiguous → my Route B (Eisenstein) is the
  consolation prize: unconditional GL(1)×GL(1) isobaric extension.

# Section 7. Recommendation

**For Theorem B unconditional via DHP-C arXiv:2601.06292: NO.**

**Possible derivative results worth pursuing:**

(a) **Eisenstein extension (Route B)**: write up the unconditional asymptotic
    for Σ_{γ_E≤T} L_E^(µ)(ρ_E, t) L_E^(ν)(1−ρ_E, t) where L_E(s,t) =
    ζ(s+it) ζ(s−it). This is degree-2 reducible. The proof is essentially
    DHP-C-mechanical with shifted χ. **Confidence this works: 0.80.** Worth
    1–2 days of writing.

(b) **Family-averaged GL(2) "cage" via DHP-C-cleaner Prop 4.1**: redo
    Milinovich-Ng Prop 4.1 with DHP-C's contour push to get the unconditional
    asymptotic in the cage, with cleaner error term exp(−C√log T) instead of
    log log T. The constant is still in the cage, not 2/(3π).
    **Confidence: 0.40.** Worth investigating but doesn't resolve B-exact.

(c) **Pivot away from DHP-C for Theorem B-exact.** The true unconditional path
    likely requires NEW input, not a refinement of contour techniques.
    Candidates: Petrow-Young cubic moment generalization to GL(2)
    L'-moments (currently only L-moments are known), or a new Kuznetsov-based
    identity for L'(ρ_f,f) (none known).

**Bottom line: DHP-C 2026 is a beautiful paper for ζ, but it does NOT
unconditionally prove Theorem B-exact.** The structural obstruction to GL(2)
extension (entire-ness of cuspidal L + Rankin-Selberg under averaging) is the
same wall hit by 5 prior routes.
