---
schema_version: 1
title: "Agent 07 H1 finite-box theorem section"
date: 2026-05-11
agent: "Breakthrough Wave 3 Agent 07 -- H1 Finite-Box Paper Theorem Extraction"
type: theorem-section
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.86
source_packet: "primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT04_H1_FINITE_BOX_THEOREM_ASSEMBLY_2026-05-11.md"
tags: [breakthrough-wave-3, h1, finite-box, theorem-section, legal-heights]
---

# Agent 07 H1 Finite-Box Paper Theorem Section

status: RIGOROUS_REDUCTION

No theorem is promoted. This file extracts Wave 2 Agent 04 into a compact
conditional theorem section. Use the hypothesis labels below verbatim in future
papers.

No new external theorem claim is made here. Any later replacement of a named
hypothesis by an imported theorem must redo the required source protocol:
`curl + pdftotext`, short quote, and page/equation.

## Named Hypotheses

`H1-AnalyticRank(E)`. `E/Q` is fixed and

```text
r = ord_(s=1) L(E,s) >= 1
```

is the analytic rank. No BSD or algebraic-rank substitution is allowed.

`H1-KernelPoleDecay(W)`. The fixed H1 kernel satisfies

```text
W_hat(z) = w_-1/z + holomorphic at z=0,
|W_hat(x+it)| << (1+|t|)^(-2)
```

on the contour strips used below, with the derivative decay needed for any
crossed multiple-zero residue audit.

`H1-FixedKernelPerron(E,W,sigma)`. For some

```text
1/2 < sigma < 3/2,
u = log K,
```

the exact fixed-kernel H1 Mellin/Perron identity holds on `Re z=sigma`:

```text
c_E,W(e^u) = (1/(2 pi i)) int_(Re z=sigma)
  e^(u z) W_hat(z)/L(E,1+z) dz.
```

This includes whatever indentation, convergence, and boundary-avoidance
conditions are needed to make the object legitimate.

`H1-CentralPolynomialNormalization(E,W,r)`. Define

```text
F_u(z) = e^(u z) W_hat(z)/L(E,1+z),
Q_E,W(u) = Res_(z=0) F_u(z).
```

Then

```text
Q_E,W(u) = sum_(ell=0)^r C_ell u^ell,
C_r = w_-1/L^(r)(E,1).
```

This is not factorial-renormalized. If `w_-1=1`, the top term is

```text
u^r/L^(r)(E,1).
```

`H1-LegalExponentialHeights(E,W,sigma,eta,C)`. Fix

```text
1/2 < eta < 1,
C > sigma,
T_box(u) in [exp(Cu), exp(Cu)+1].
```

For

```text
I_sigma(T,u) = (1/(2 pi i)) int_(sigma-iT)^(sigma+iT) F_u(z) dz,
V_eta(T,u)   = (1/(2 pi i)) int_(-eta-iT)^(-eta+iT) F_u(z) dz,
H_+(T,u)     = (1/(2 pi i)) int_(-eta)^sigma F_u(x+iT) dx,
H_-(T,u)     = (1/(2 pi i)) int_(-eta)^sigma F_u(x-iT) dx,
```

the finite box identity is legal at `T=T_box(u)` and the boundary terms satisfy

```text
Tail_sigma(T_box,u) = o(u^r),
V_eta(T_box,u) = o(u^r),
H_+(T_box,u) - H_-(T_box,u) = o(u^r).
```

The original-line tail requires exponential height: with the source-safe line
`sigma>1/2` and `|W_hat(sigma+it)| << |t|^(-2)`,

```text
Tail_sigma(T,u) << e^(sigma u) T^(-1),
```

so polynomial or ad hoc heights are not legal for this pointwise box.

`H1-NoSilentRightHalfResidues(E,W,sigma,eta)`. Every crossed pole with
`Re z>0` is either absent under an explicit zero-location hypothesis,
explicitly retained in the formula, or handled by a separately proved theorem
mode. Silent deletion is forbidden.

`H1-SimpleReciprocalBudget(E,r)`. For simple critical-line zeros write

```text
R_E,1(T) =
  sum_(T<|gamma|<=2T, simple) |L'(E,1+i gamma)|^(-1).
```

The required fixed-curve budget is

```text
R_E,1(T) = o(T^2 (log T)^(r-1)).
```

With `H1-KernelPoleDecay(W)`,

```text
sum_(T<|gamma|<=2T, simple)
  |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1)
<< T^(-2) R_E,1(T),
```

so the simple-zero residue aggregate below `T_box(u)` is `o(u^r)`.
For analytic rank one the exact live target is

```text
R_E,1(T) = o(T^2).
```

`H1-MultipleEffectiveDegree(E,W,r)`. For a crossed zero `rho` of multiplicity
`m`, put `alpha=rho-1` and expand

```text
1/L(E,1+z) =
  sum_(j=1)^m b_(rho,-j)(z-alpha)^(-j) + holomorphic.
```

Its residue contribution has the form

```text
R_rho(u) =
  e^(alpha u) sum_(ell=0)^(m-1) A_(rho,ell) u^ell,

A_(rho,ell) =
  (1/ell!) sum_(j=ell+1)^m
    b_(rho,-j) W_hat^(j-1-ell)(alpha)/(j-1-ell)!.
```

After kernel zeros, internal Laurent/kernel cancellation, and exact
same-exponent netting, define

```text
D_alpha = max { ell : A_(alpha,ell)^net != 0 }.
```

Pointwise central-only H1 requires every retained critical-line effective degree
to satisfy

```text
D_alpha < r.
```

Lower-degree multiple-zero aggregates still require absolute summability or a
proved bounded/PV/averaged theorem in the declared mode. The generic individual
condition

```text
m <= r + ord_(z=alpha) W_hat(z)
```

is only a sufficient local screen; it does not replace the effective-degree
audit.

## Theorem: H1-FiniteBox-Conditional

Assume

```text
H1-AnalyticRank(E),
H1-KernelPoleDecay(W),
H1-FixedKernelPerron(E,W,sigma),
H1-CentralPolynomialNormalization(E,W,r),
H1-LegalExponentialHeights(E,W,sigma,eta,C),
H1-NoSilentRightHalfResidues(E,W,sigma,eta),
H1-SimpleReciprocalBudget(E,r),
H1-MultipleEffectiveDegree(E,W,r).
```

Then, in the same declared pointwise finite-box mode,

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r)
           = (w_-1/L^(r)(E,1)) u^r + o(u^r).
```

For normalized kernels with `w_-1=1`,

```text
c_E,W(e^u) = u^r/L^(r)(E,1) + o(u^r).
```

Rank-one specialization is conditional on the exact simple-zero target
`R_E,1(T)=o(T^2)` and the same boundary and multiple-zero hypotheses.

## Proof Skeleton

Apply the finite rectangle identity to `F_u` at
`T=T_box(u)`:

```text
I_sigma(T,u)
 = sum_(z0 in P_T) Res_(z=z0) F_u(z)
   + V_eta(T,u) + H_+(T,u) - H_-(T,u).
```

The central pole gives `Q_E,W(u)` with top coefficient
`w_-1/L^(r)(E,1)`. `H1-LegalExponentialHeights` kills the original-line tail,
shifted-left line, and horizontal edges at `o(u^r)`. `H1-SimpleReciprocalBudget`
kills simple critical-line residues. `H1-MultipleEffectiveDegree` keeps every
retained multiple-zero term below central degree and controls the lower-degree
aggregate in the declared mode. `H1-NoSilentRightHalfResidues` prevents hidden
offcritical promotion. The remaining contribution is `Q_E,W(u)+o(u^r)`.

## No-Promotion Boundaries

Do not cite this section as any of the following:

```text
unconditional EC H1 theorem;
rank-one H1 theorem without R_E,1(T)=o(T^2);
positive-rank H1 theorem without R_E,1(T)=o(T^2(log T)^(r-1)) or a proved substitute;
multiple-zero closure from kernel decay alone;
pointwise central-only theorem with a retained D_alpha>=r oscillation;
Li-Zaharescu as unconditional H-height closure;
H1 reciprocal-pole damping from H2 branch damping;
rank-zero pointwise constant stabilization;
H1/H2 product theorem without same-mode H2 closure;
theorem using BSD rank, finite numerics, cross-curve universality, or Koyama correspondence/email material as analytic input.
```

H2 branch damping is not used as H1 reciprocal-pole damping.

## Extraction Notes

Read scope was restricted to the requested context:

```text
start.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3-plan.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT04_H1_FINITE_BOX_THEOREM_ASSEMBLY_2026-05-11.md
```

No broad wiki, raw archive, web search, Koyama correspondence, or email draft
was opened.
