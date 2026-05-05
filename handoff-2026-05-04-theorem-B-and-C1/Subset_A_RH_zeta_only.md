---
title: "Subset A under RH(ζ): structural decomposition of the constant 2/(3π) for the modular L'-second moment, with honest gap identification"
type: note
domain: research
tier: working
confidence: 0.85
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
author: Saar Shai
sources:
  - "Conrey–Ghosh–Gonek 1989, Number Theory, Trace Formulas and Discrete Groups, Academic Press, 185–199"
  - "Gonek, S.M., Mean values of the Riemann zeta-function and its derivatives, Invent. Math. 75 (1984) 123–141"
  - "Milinovich, M., Ng, N., Simple zeros of modular L-functions, arXiv:1306.0854 (2014)"
  - "Conrey, B., Farmer, D., Keating, J., Rubinstein, M., Snaith, N. (CFKRS), Integral moments of L-functions, Proc. London Math. Soc. (3) 91 (2005) 33–104"
  - "Conrey, B., Snaith, N., Applications of the L-functions ratios conjecture, Proc. London Math. Soc. (3) 94 (2007) 594–646"
  - "Rankin, R.A., Contributions to the theory of Ramanujan's function τ(n), Proc. Cambridge Philos. Soc. 35 (1939) 351–372"
  - "Selberg, A., Bemerkungen über eine Dirichletsche Reihe, Arch. Math. Naturvid. 43 (1940) 47–50"
supersedes: []
tags: [theorem-B, constant-2-over-3pi, RH-zeta, CFKRS, structural-note]
---

> **Honesty banner.** This note does **not** prove Theorem B-exact under
> RH(ζ). The original framing — "Theorem B-exact follows from
> {NC₈, NC₁₁, NC₁₂} under RH(ζ) only" — is incorrect, as documented in
> `Subset_A_VERIFICATION.md`. What this note *does* offer is a clean
> structural decomposition of the conjectural constant 2/(3π) and
> a verbatim location of the surviving open gap. The decomposition is
> publishable as expository content; the conditional theorem under
> RH(ζ) is **not**.

# Abstract

Let f ∈ H_k(q, χ) be a holomorphic Hecke newform with non-trivial zeros
ρ_f = β_f + iγ_f of L(s, f). Write
$$M_f(T) := \sum_{0 < \gamma_f \le T} |L'(\rho_f, f)|^2.$$
Milinovich–Ng [MN, Conjecture (16)] state that
$$M_f(T) \sim \frac{2}{3\pi}\, c_f\, T\, \log^4 X, \qquad X = \frac{\sqrt{q}\,T}{2\pi},$$
where c_f is the Rankin–Selberg residue at s=1.

This note documents the **structural identity**
$$\boxed{\frac{2}{3\pi} \;=\; \underbrace{\frac{1}{24\pi}}_{\text{baseline (RH(ζ))}} \times \underbrace{16}_{\text{algebraic boost (unconditional)}}}$$
and traces each factor to a verbatim source. The 1/(24π) baseline is
**Gonek 1989** under RH(ζ); the factor 16 = 2⁴ is the algebraic conductor-
differentiation identity verified by sympy. The decomposition matches
the CFKRS recipe-output prediction d^{2k} / ((2k)! · π) at (d=2, k=2).

**The decomposition is not a proof of M-N (16) under RH(ζ).** Section 4
identifies the surviving gap (CFKRS recipe transfer from d=1 to d=2)
and quotes verbatim from M-N 2014 to show that the gap is independent of
RH(ζ).

---

# Section 1. Theorem statement (target) and what we actually establish

**Conjecture (Milinovich–Ng (16), 2014).** For f ∈ H_k(q, χ),
$$M_f(T) = \tfrac{2}{3\pi}\, c_f\, T\, \log^4 X + O(T \log^3 X),$$
under GRH for L(s, f).

**What this note establishes (Theorem 1, structural).**

The constant 2/(3π) decomposes as a product of three independent factors:
- (a) a Plancherel factor 1/π (critical-line measure);
- (b) a combinatorial / Barnes-G factor 1/(2k)!|_{k=2} = 1/24, equivalent to the
  unitary Hughes–Mezzadri leading constant for the d=1 case (under RH(ζ));
- (c) an algebraic conductor-differentiation factor d^{2k}|_{d=2,k=2} = 16,
  unconditional.

The product (1/π) · (1/24) · 16 = 16/(24π) = 2/(3π) matches the M-N constant
exactly, with all three factors traceable to a verbatim source. The single
ingredient that requires a hypothesis is (b), which inherits RH(ζ) from
Gonek 1989; (c) is unconditional, and (a) is purely measure-theoretic.

**What this note does NOT establish.** Theorem 1 above is a structural
identification of the three factors; it is **not** a proof of M-N (16). The
chain (a) × (b) × (c) = 2/(3π) at the level of *factors* does not promote
the d=1 ζ result (Gonek 1989, under RH(ζ)) to the d=2 modular result
(M-N (16), under GRH-for-f-plus-CS07-ratios). See §4 for the surviving gap.

---

# Section 2. Proof of Theorem 1 (structural decomposition)

Three ingredients, denoted NC₈, NC₁₁, NC₁₂ following the audit in
`Necessary_conditions_inverse.md`.

## 2.1 NC₈: Rankin–Selberg residue (unconditional)

For f ∈ H_k(q, χ), the convolution L-function
$L(s, f \times \bar f) = \sum_{n \ge 1} |\lambda_f(n)|^2 / n^s$ (ℜ s > 1)
admits meromorphic continuation to ℂ with a simple pole at s=1 of residue
$$c_f = \frac{(4\pi)^k}{\Gamma(k) \cdot \mathrm{vol}(\Gamma_0(q) \backslash \mathfrak{h})} \, \|f\|^2$$
[Rankin 1939; Selberg 1940; M-N 2014, eq. (1)]. Equivalently,
c_f = lim_{x→∞} (1/x) Σ_{n≤x} |λ_f(n)|² (M-N 2014 lines 209-211).

This residue carries the entire arithmetic content of the d=2 family at
the level of the leading constant. It is independent of RH(ζ), GRH-for-f,
or any other unproven hypothesis.

## 2.2 NC₁₁: 16 = 2⁴ algebraic boost (unconditional)

The CFKRS recipe [CFKRS 2005, §3-§4] writes the (2k)-th moment of L(½, f)
as a contour integral over 2k auxiliary shifts, then sets all shifts to
zero with explicit residue/derivative manipulations. For the 2nd moment of
the *derivative* L'(ρ_f, f) at zeros, the analog has 2k = 4 differentiation
operations, each pulling down a factor of log 𝔮(t) where 𝔮(t) is the
analytic conductor of L(s, f) at height t.

For ζ (degree d=1): log 𝔮(t) = log t + O(1).
For L(s, f) (degree d=2): log 𝔮(t) = log q + 2 log t + O(1).

Expanding (log q + 2 log t)^4 (sympy 1.14, `expand`):
$$\big(\log q + 2 \log t\big)^4 = 16 \log^4 t + 32 \log^3 t \cdot \log q + 24 \log^2 t \cdot \log^2 q + 8 \log t \cdot \log^3 q + \log^4 q.$$

The leading coefficient of log⁴ t is **16 = 2⁴**, which is the d=2 conductor-
differentiation factor. This is an algebraic identity (sympy
`Rational(16, 24) = Rational(2, 3)`), independent of any analytic
hypothesis.

## 2.3 NC₁₂: ζ-baseline 1/(24π) under RH(ζ)

**[Gonek 1989, verbatim quoted via M-N 2014 lines 869-877]:**

> Σ_{0 < ℑ(ρ) ≤ T} |ζ'(ρ)|² = (T / (24π)) · log⁴ T + O(T log³ T)
> assuming the Riemann hypothesis where ρ runs through the non-trivial
> zeros of the Riemann zeta-function.

Reference: Conrey, J.B., Ghosh, A., Gonek, S.M., "Mean values of the
Riemann zeta-function with application to the distribution of zeros," in
*Number Theory, Trace Formulas and Discrete Groups*, Academic Press, 1989,
pp. 185-199; building on Gonek, Invent. Math. 75 (1984) 123-141.

The Hughes thesis (2001) and Hughes–Mezzadri provide the random-matrix-
theoretic interpretation of the constant: 1/(24π) = (1/(2π)) · (1/12),
where 1/(2π) is the Plancherel factor on the critical line and 1/12 =
G(3)²/G(5) is the Barnes-G ratio for the unitary 2nd-moment-of-derivative.

Hypothesis: **RH(ζ)**.

## 2.4 Combining (NC₈) + (NC₁₁) + (NC₁₂) — at the level of factors

Multiplying:
$$\frac{1}{24\pi} \times 16 \times c_f \;=\; \frac{16}{24\pi} \cdot c_f \;=\; \frac{2}{3\pi}\, c_f.$$

Numerical verification (mpmath, 50 digits):
- 2/(3π)  = 0.21220659078919378102517835116335248271261286098728
- 1/(24π) = 0.01326291192432461131407364694770953016953830381170
- ratio   = 16.0 (exact)
- sympy:  Rational(16, 24) = Rational(2, 3) ✓

**This establishes Theorem 1 (factor-level decomposition).** ∎

---

# Section 3. Verbatim citations

## 3.1 Conrey–Ghosh–Gonek 1989 / Gonek 1989 (NC₁₂)

Quoted via M-N 2014 (verbatim, lines 869-877):

> "Note that this is consistent with Theorem 1.2 and is analogous to a
>  result of Gonek [21] which states that
>    Σ_{0<ℑ(ρ)≤T} |ζ'(ρ)|² = (T / (24π)) log⁴ T + O(T log³ T)
>  assuming the Riemann hypothesis where ρ runs through the non-trivial
>  zeros of the Riemann zeta-function."

The 1/(24π) constant is the leading coefficient under RH(ζ). M-N reference
[21] is Gonek's Inventiones paper plus the Conrey–Ghosh–Gonek 1989
refinement.

## 3.2 Milinovich–Ng 2014 Conjecture (16)

Verbatim, lines 846-867:

> "Conjecture. Let f ∈ H_k(q, χ), let c_f be the constant in (1), and let
>  X = √qT/(2π). Then we have
>    Σ_{0<γ_f≤T} |L'(ρ_f, f)|² = (2/(3π))·c_f·T·log⁴X + O(T·log³X),
>  where the implied constant depends only on f."

This is the target identity. M-N 2014 prove only the **cage** statement
(Theorem 1.2 of M-N): under GRH for L(s, f), the second moment is bounded
between A_f T log⁴X and B_f T log⁴X with A_f, B_f = (17 ∓ √145)/(12π) · c_f.
The exact constant 2/(3π) lies inside this cage but is not isolated by
M-N's argument.

## 3.3 Milinovich–Ng 2014 difficulty statement

Verbatim, lines 884-896:

> "However, since L(s, f) is a degree two L-function, establishing (16) is
>  comparable to establishing the conjectural formula
>    Σ_{0<ℑ(ρ)≤T} |ζ'(ρ)|⁴ = (T / (2880π³)) · log⁹ T + O(T log⁸ T).
>  Such a result appears to be unattainable using current techniques
>  without some significantly new ideas. (See [41] for some history and
>  some results in this direction.) Likewise, we expect that some
>  substantially new ideas are necessary in order to establish the above
>  conjecture for the second moment of L'(ρ_f, f)."

This is the decisive verbatim passage establishing that the d=2 second
moment is, in M-N's own assessment, of the same difficulty as the d=1
**fourth** moment under RH(ζ) — both currently open.

## 3.4 CFKRS 2005 recipe shape

Conrey–Farmer–Keating–Rubinstein–Snaith 2005 (PLMS 91, p. 36, eq.
(1.3.1)–(1.3.3)) write the leading polynomial of degree k² for the (2k)-th
moment of L(½, f) as a contour integral with shift parameters
α₁, …, α_{2k}, then take residues at coalescing shifts. The leading log-
power coefficient depends on:
- the degree d of L (each shift derivative pulls down d · log t);
- the symmetry type (orthogonal here, by Katz–Sarnak / ILS 2000);
- the local Euler-product factor c_f.

The output formula matches the structural decomposition d^{2k} / ((2k)! π)
in §2.

---

# Section 4. **HONEST GAP IDENTIFICATION** — why §2 is not a proof of M-N (16)

This is the central section. The §2 decomposition is *factor-level*; it
does not constitute a theorem-transfer.

## 4.1 What §2 actually shows

§2.4 multiplies three factors:
- 1/(24π) — the leading coefficient of a *theorem* about ζ' (under RH(ζ));
- 16 — an algebraic identity about how log⁴ Q expands;
- c_f — a residue formula for d=2.

The product equals 2/(3π) · c_f. **This product matches M-N's conjectured
constant for d=2 numerically and structurally.** This match is non-trivial
and confirms the CFKRS recipe shape.

## 4.2 What §2 does NOT show

The product **does not establish** the asymptotic
$$\sum_\gamma |L'(\rho_f, f)|^2 \sim \tfrac{2}{3\pi} c_f T \log^4 X.$$

To go from "the factors multiply to the right number" to "the asymptotic
holds" requires the **CFKRS recipe to actually be correct for the modular
family at the level of the 2nd moment of L'**, which is exactly M-N (16)
itself.

In standard CFKRS terminology, this requires:
- Off-diagonal control of the 4-shift Rankin–Selberg sum (the ratios
  conjecture in family-averaged form), at the precision needed to extract
  the log⁴ coefficient.
- For an individual f: GRH-for-f plus the per-form ratios identity (CS07
  §7) made rigorous.

**Neither of these is implied by RH(ζ).** They are independent hypotheses
about the modular L-function.

## 4.3 Concrete demonstration that RH(ζ) is not enough — verbatim from G2 audit

The (R3) step in M-N 2014's proof of Theorem 1.2 (the cage) requires the
identity ρ_f = 1 - \overline{ρ_f}, which holds only if β_f = 1/2 for the
zeros of L(s, f). This is **RH for L(s, f)** (denoted RHf), not RH(ζ).

`G2_GRH_bypass.md` §1.2 (R3) verbatim:

> "(R3) Functional-equation symmetry ρ_f = 1−\overline{ρ_f}. Multiple
>  later passes (line 2884, line 3268 of M-N 2014) write 1 − ρ_f =
>  \overline{ρ_f}, which holds **only if** β_f = 1/2 for every zero. This
>  is RHf at its barest."

RH(ζ) constrains zeros of ζ. RHf constrains zeros of L(s, f). For non-
trivial cusp forms, these are independent statements; there is no known
reduction.

## 4.4 The CS07 ratios gap survives even under GRH-for-the-family

The G2 audit further shows that **even** under (RHf for every f in F),
Theorem B-exact requires the **CS07 ratios identity in family-averaged
form** — denoted G7 in the project's gap catalog. This is a recipe / off-
diagonal control gap **independent** of any RH statement. RH(ζ), RHf, or
GRH for the entire family does not close G7.

Therefore, the original prompt's framing — "Theorem B-exact under RH(ζ)
only, weaker than GRH-for-family" — is **dominated** by an independent
gap that GRH-for-family also fails to close. RH(ζ) alone is strictly
weaker than GRH-for-family, and both fail at the same recipe-transfer
step.

## 4.5 Comparison to the full GRH-conditional version

| Hypothesis | Status of M-N (16) |
|---|---|
| Unconditional | OPEN (cage statement, family-averaged, holds at confidence 0.85) |
| RH(ζ) only | OPEN — RH(ζ) does not constrain ρ_f |
| RHf for the single f under consideration | OPEN — gives M-N cage, not exact constant |
| GRH for L(s, f) for all f in F | OPEN — gives family cage, not exact constant; CS07 ratios gap survives |
| GRH for L(s, f) for all f in F + CS07 ratios in family-averaged form | M-N (16) holds ✓ |

The minimum hypothesis set known to imply M-N (16) is the last row.
**RH(ζ) is not in this hypothesis set in any non-trivial way.**

## 4.6 Honest verdict

The decomposition 2/(3π) = 16/(24π) is **structurally clean** and
**informatively factorizes** the constant into independent ingredients.
But the decomposition is **recipe-data**, not theorem-transfer:

- The 16 boost is a property of the CFKRS recipe output formula, not a
  proven transfer rule between two separately-proven theorems.
- The 1/(24π) baseline is a proven theorem under RH(ζ) for ζ alone.
- Multiplying these factors is a *consistency check on the recipe*, not a
  proof for d=2.

The proof for d=2 still requires the CFKRS recipe to be rigorously
correct at the d=2 level — which is M-N (16) itself.

This note's structural decomposition is **publishable as expository
content** (matching CS07 §7 and CFKRS_symbolic_verification.md), but it
is **not a new conditional theorem** beyond what M-N 2014 already
conjecture under their stated hypotheses.

---

# Section 5. Significance

## 5.1 What is genuinely new in this note

(a) The clean factorization 2/(3π) = (1/(2π)) × (1/12) × 16 — three
independent factors with three independent sources — is sharper than
the typical "2/(3π) ≈ 0.21" treatment. It locates the algebraic content
(NC₁₁, the 16 boost) and isolates it from the analytic content (NC₁₂,
the 1/(24π) baseline).

(b) The verbatim location of M-N 2014 lines 884-892 establishes that the
d=2 second moment is, in M-N's own assessment, of difficulty comparable
to the d=1 fourth moment under RH(ζ) — a fact that, while implicit in
the M-N text, deserves being highlighted as a structural barrier.

(c) The audit `Subset_A_VERIFICATION.md` clarifies that the gap
surviving in §4 is independent of RH(ζ); it is the CFKRS recipe transfer.

## 5.2 What this note does NOT claim

- It does not weaken the hypothesis of M-N (16) below GRH-for-the-family
  + CS07-ratios.
- It does not give a new conditional theorem under RH(ζ) only.
- It does not bypass the wall (4-shift Rankin–Selberg / CS07 ratios).

## 5.3 Recommendation for further work

The structural decomposition in §2 is consistent with the CFKRS recipe
output. The remaining open question is whether the recipe can be proven
rigorously at the d=2 second-moment level. The forward attacks (RMT,
Voronoi-Kuznetsov, theta lift, family Bessel, family large sieve) and
the inverse attacks (necessary conditions, structural decomposition)
all hit the same wall: the 4-fold shifted convolution / off-diagonal
Rankin-Selberg control.

The narrowest remaining lead documented in the project is **NC₁₅ —
period identity for 2/(3π)** (`Necessary_conditions_inverse.md` §5),
which would attack the constant from the geometric (rather than
analytic) side. Numerical search to date has not located such an
identity, but the search has been limited.

---

# Appendix A. Numerical compatibility

(mpmath, 50 dps; sympy 1.14)

```
2/(3π)  = 0.21220659078919378102517835116335248271261286098728
1/(24π) = 0.01326291192432461131407364694770953016953830381170
16/(24π) = 0.21220659078919378...  (matches 2/(3π) at 30+ digits)
sympy:    Rational(16, 24) = Rational(2, 3)  ✓ exact
expand((log(q) + 2*log(t))**4) leading log⁴t coefficient = 16  ✓ exact

Hughes/Barnes-G unitary derivative-moment ratios:
  k=1: G(2)²/G(3)  = 1
  k=2: G(3)²/G(5)  = 1/12
  k=3: G(4)²/G(7)  = 1/8640

Recipe formula d^{2k} / ((2k)! π) at (d=2, k=2):
  16 / (24π) = 0.21220659078919378...
matches 2/(3π) exactly.
```

# Appendix B. What "Subset A" means precisely

In the audit `Necessary_conditions_inverse.md`, Subset A = {NC₈, NC₁₁, NC₁₂}
denotes the structural triple:

- NC₈: Rankin–Selberg pole + residue c_f at s=1 (unconditional).
- NC₁₁: algebraic conductor-differentiation 16 = 2⁴ (unconditional).
- NC₁₂: ζ-baseline Σ|ζ'(ρ)|² ∼ (T/(24π)) log⁴ T (under RH(ζ); Gonek 1989).

The "subset" terminology refers to the question: do these three conditions
together imply Theorem B-exact under RH(ζ) only? The answer, established
in §4 above and `Subset_A_VERIFICATION.md`, is **NO** — the chain has a
hidden CFKRS-recipe-transfer hypothesis that is independent of RH(ζ) and
strictly stronger than RH for L(s, f) for every f in the family.

Subset A is therefore documented here as a **structural observation** about
the constant 2/(3π), not as a proof.
