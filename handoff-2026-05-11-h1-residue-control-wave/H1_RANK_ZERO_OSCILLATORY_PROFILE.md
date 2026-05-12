---
schema_version: 1
title: "Rank-zero oscillatory H1 profile"
date: 2026-05-11
type: research-note
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.83
dependencies:
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
  - handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
tags: [ec-ndc, h1, rank-zero, reciprocal-residues, oscillatory-profile]
---

# H1 Rank-Zero Oscillatory Profile

## Do Not Promote Unless

- Rank zero is stated as an oscillatory profile, averaged theorem, or
  explicitly filtered theorem; do not call it pointwise constant stabilization.
- The H1 contour shift is proved in the same kernel and Mellin normalization.
- The reciprocal-zero series has a declared convergence mode; for the pointwise
  profile below, use uniform convergence of symmetric truncations or a stronger
  explicit tail bound.
- The contour remainder is controlled after the same truncation used to define
  the zero series.
- All simple offcentral residues are either retained, killed coefficientwise,
  or averaged in a theorem about the product itself.
- Multiple offcentral zeros are ruled out, separately retained as
  polynomial-exponential terms, or handled by a stated finite-part theorem.
- Kernel zero-filtering is not used as evidence for a fixed natural kernel
  unless the full tail after filtering is controlled.
- H2 is composed only in the same mode: pointwise profile with pointwise
  profile, arithmetic average with arithmetic average, geometric average with
  geometric average.
- External theorem citations remain absent here. Any future cited theorem must
  follow the repository protocol: `curl + pdftotext + short quote +
  page/equation`.

## Verdict

For analytic rank zero, the claim-safe fixed-curve H1 object is likely

```text
c_E,W(e^u) = Q_0 + Z_c(u) + o(1),
```

not

```text
c_E,W(e^u) = Q_0 + o(1),
```

unless a separate theorem kills the simple offcentral reciprocal residues.

This is a reduction: once the H1 contour formula and tail estimates are proved,
the displayed profile is the honest theorem-grade rank-zero replacement. It
does not promote a closed EC smoothing theorem.

## Citation Protocol

External theorem citations: none.

This note uses local Laurent algebra and conditional Perron-residue
bookkeeping from the dependency files above. It deliberately does not cite
Perron's formula, EC zero counting, Bohr almost-periodic theory, or derivative
moment results as external theorems. If any of those become load-bearing in a
paper theorem, attach the required source packet first.

## Setup

Fix an elliptic curve `E/Q`, a fixed smoothing kernel `W`, and the H1 Mellin
normalization

```text
c_E,W(K)
 = (1/(2 pi i)) int_(Re z=sigma)
     K^z W_hat(z) / L(E,1+z) dz.
```

Write

```text
u = log K,
r = ord_(s=1) L(E,s).
```

This note is the rank-zero case:

```text
r = 0,
L(E,1) != 0.
```

Assume

```text
W_hat(z) = w_(-1)/z + holomorphic at z=0,
```

with repository-normalized kernels having `w_(-1)=1`.

The central H1 residue is therefore

```text
Q_0
 = Res_(z=0) e^(uz) W_hat(z)/L(E,1+z)
 = w_(-1)/L(E,1).
```

For normalized kernels,

```text
Q_0 = 1/L(E,1).
```

## Reciprocal-Zero Series

Let

```text
Gamma = {gamma in R\{0}: L(E,1+i gamma)=0 and the zero is simple}.
```

For `gamma in Gamma`, define the simple reciprocal residue coefficient

```text
a_gamma = W_hat(i gamma) / L'(E,1+i gamma).
```

For real `W` and the usual real-coefficient symmetry, the conjugate pair
satisfies `a_(-gamma)=conj(a_gamma)`, so the real contribution is

```text
a_gamma e^(i gamma u) + a_(-gamma)e^(-i gamma u)
 = 2 Re(a_gamma e^(i gamma u)).
```

The rank-zero oscillatory term is

```text
Z_c(u) = sum_(gamma in Gamma) a_gamma e^(i gamma u).
```

Same-frequency cancellations, if any, must be applied before naming the final
coefficient. For a single simple zero at each ordinate, the displayed
`a_gamma` is the coefficient.

## Convergence Mode

The pointwise profile should be stated in the uniform almost-periodic mode.
Define symmetric truncations

```text
Z_T(u) = sum_(gamma in Gamma, 0<|gamma|<=T) a_gamma e^(i gamma u),
T avoiding zero ordinates.
```

Assume the explicit tail bound

```text
A(T) = sum_(gamma in Gamma, |gamma|>T) |a_gamma| -> 0.
```

Then `Z_T` converges uniformly on `R` to `Z_c`, and `Z_c` is a uniform limit of
finite exponential polynomials. This is the convergence mode meant here by
almost-periodic.

A weaker Besicovitch/mean-square zero series is a different theorem mode. It
can support averaged statements, but it does not by itself justify the
pointwise `o(1)` profile above.

## Truncated H1 Formula

The contour-shift theorem should first be proved with a finite height. For
admissible `T`, write

```text
c_E,W(e^u) = Q_0 + Z_T(u) + I_T(u),
```

where `I_T(u)` contains:

```text
1. shifted vertical contour;
2. horizontal edges;
3. indentation errors;
4. finite-height truncation and pole-avoidance errors;
5. any non-simple offcentral terms if they have not been separately excluded.
```

Under the uniform tail assumption, the full-profile error satisfies

```text
c_E,W(e^u) - Q_0 - Z_c(u)
 = I_T(u) - (Z_c(u)-Z_T(u)),
```

hence

```text
|c_E,W(e^u) - Q_0 - Z_c(u)|
 <= |I_T(u)| + A(T).
```

Thus the theorem-grade sufficient condition is:

```text
there exists an admissible T=T(u)->infinity such that
|I_T(u)| + A(T) -> 0.
```

Equivalently, if a stronger contour theorem gives a bound

```text
|I_T(u)| <= B(u,T),
```

then the quantitative profile is

```text
c_E,W(e^u)
 = Q_0 + Z_c(u) + O(A(T) + B(u,T)),
```

with `T=T(u)` chosen so that `A(T)+B(u,T)=o(1)`.

## Candidate Statement

Assume:

```text
H1-rank0-contour:
  the finite-height H1 formula above is valid for admissible T;

H1-simple:
  every offcentral zero retained in the main profile is simple, or
  all nonsimple contributions are placed into a separate explicit profile;

H1-AP:
  A(T)=sum_(|gamma|>T)|W_hat(i gamma)/L'(E,1+i gamma)| -> 0;

H1-tail:
  for some admissible T(u)->infinity, |I_(T(u))(u)|=o(1).
```

Then

```text
c_E,W(e^u)
 = w_(-1)/L(E,1)
   + sum_(gamma in Gamma)
       W_hat(i gamma) e^(i gamma u) / L'(E,1+i gamma)
   + o(1),
```

with the zero series converging uniformly in `u`.

For normalized kernels:

```text
c_E,W(e^u)
 = 1/L(E,1) + Z_c(u) + o(1).
```

This is the honest rank-zero fixed-kernel H1 profile.

## Why This Blocks Constant Stabilization

If the uniform almost-periodic `Z_c` has a pointwise limit as `u->infinity`,
then every nonzero-frequency coefficient is zero.

Direct check: for each retained frequency `lambda`,

```text
a_lambda
 = lim_(U->infinity) (1/U) int_0^U Z_c(u)e^(-i lambda u) du,
```

where the identity follows first for finite `Z_T` and then by uniform
convergence. If `Z_c(u)->0`, this mean is zero. Hence all `a_lambda=0`.

Therefore a nonzero simple offcentral residue

```text
W_hat(i gamma)/L'(E,1+i gamma) != 0
```

survives at constant scale. It cannot be hidden in `o(1)`.

## What Would Kill `Z_c`

Pointwise constant rank-zero stabilization requires one of the following.

1. Coefficientwise death:

```text
W_hat(i gamma)/L'(E,1+i gamma)=0
for every retained gamma != 0.
```

For simple zeros this means `W_hat(i gamma)=0`, since
`L'(E,1+i gamma) != 0`.

2. Exact same-frequency cancellation:

```text
sum_(rho with frequency gamma) Res_rho = 0
for every gamma != 0.
```

Conjugate pairs do not cancel a real oscillation unless the coefficient itself
is zero.

3. Kernel filtering:

```text
W_hat(i gamma)=0
```

for the relevant offcentral ordinates, plus a theorem controlling the
unfiltered tail. Finite filtering only removes finitely many named residues.

4. Explicit subtraction:

```text
c_E,W(e^u) - Z_c(u) = Q_0 + o(1).
```

This is a renormalized theorem, not stabilization of the original H1 object.

5. Averaging:

use a declared logarithmic, geometric, or arithmetic average that is proved for
`c_E,W` or for the product `c_E,W P_E,W`. Averaged `log P` alone does not kill
`Z_c` in the product.

Without one of these mechanisms, the constant claim is not rank-zero safe.

## Product Compatibility

If H2 is pointwise nonoscillatory in rank zero,

```text
P_E,W(e^u) = exp(B_E,W)(1+o(1)),
```

then the composed product profile is

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_E,W)(Q_0+Z_c(u)) + o(1).
```

If H2 has its own pointwise oscillatory factor

```text
P_E,W(e^u)=exp(B_E,W) exp(Z_P(u))(1+o(1)),
```

then the profile becomes

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_E,W)(Q_0+Z_c(u)) exp(Z_P(u)) + o(1).
```

An arithmetic average of this product needs zero-frequency extraction from the
joint H1/H2 expansion. It is not determined by the mean of `Z_c` or `Z_P`
separately.

## Multiple-Zero Boundary

This file targets simple offcentral residues. If an offcentral zero
`rho=1+i gamma` has multiplicity `m>1`, the reciprocal pole contributes

```text
e^(i gamma u) P_rho(u),
```

where `P_rho` is a polynomial of degree at most `m-1` involving Laurent
coefficients of `1/L(E,s)` and derivatives of `W_hat`.

In rank zero, any degree `>=1` term is growing on the H1 scale. Such terms must
be ruled out, kernel-cancelled, explicitly retained as a larger profile, or
put into a finite-part/averaged theorem. They are not part of the bounded
almost-periodic `Z_c` above.

## Decision

Yes: `c_E,W(e^u)=Q_0+Z_c(u)+o(1)` is likely the right claim-safe rank-zero H1
object for a fixed curve and fixed kernel when simple offcentral residues
survive.

The constant-only statement is claim-safe only after a coefficient-killing,
tail-killing, or product-average theorem is proved in the same mode. The
oscillatory profile is the least dishonest fixed-curve replacement because it
keeps exactly the residues that smoothing does not remove.

## Changed Files

```text
handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
```
