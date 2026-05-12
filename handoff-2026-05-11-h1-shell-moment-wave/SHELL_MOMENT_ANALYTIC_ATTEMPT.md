---
schema_version: 1
title: "H1 shell moment analytic attempt"
date: 2026-05-11
type: proof-attempt
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.87
dependencies:
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/BREAKTHROUGH_WAVE_REFEREE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md
tags: [ec-ndc, h1, shell-moment, reciprocal-derivative]
---

# H1 Shell Moment Analytic Attempt

Status: `RIGOROUS_REDUCTION`

Confidence: `0.87`

External citations: none. All analytic inputs below are stated as hypotheses
or imported from the listed local handoff files. Any future external theorem
used to discharge a hypothesis must follow the project protocol:
`curl + pdftotext + short quote + page/eq`.

## Do Not Promote Unless

- The shell moment is stated only over simple zeros, or every offcentral zero
  in the shell is proved simple. A multiple zero makes `L'(rho)=0` and the
  displayed reciprocal square infinite.
- A zero-count input is either proved locally, cited by source protocol, or
  retained as a hypothesis.
- GRH, simple zeros, zero spacing, or zero repulsion are not treated as
  derivative lower bounds unless an explicit minimum-modulus or reciprocal
  strip estimate is also supplied.
- Mollifier estimates are used only if they give a positive upper majorant or
  a relative approximation to `1/L'(rho)`. Signed mollified first moments and
  lower bounds for negative moments do not imply the needed upper bound.
- The smoothstep `q=2` H1 closure uses a genuinely dyadic bound
  `J_E,2(T) <= C_E T^(3-delta)`, not a fixed-weight transfer with low shells
  omitted.
- Multiple-zero Laurent terms remain governed by the exceptional-term package;
  this file only addresses the simple-zero shell moment.

## Target

For a fixed elliptic curve normalization whose critical line is written
`s=1+i gamma`, define the simple-zero shell moment

```text
J_E,2(T)
 = sum_{T<|gamma|<=2T, L(E,1+i gamma)=0 simple}
     |L'(E,1+i gamma)|^(-2).
```

The H1 smoothstep-scale target is

```text
J_E,2(T) <= C_E T^(3-delta)
```

for some `delta>0`. The previous breakthrough synthesis explains why this is
exactly the dyadic input needed when `|W_hat(i t)| << (1+|t|)^(-2)`: with
`q=2`, the Cauchy-Schwarz shell criterion is `theta < 2q-1 = 3`.

## Conditional Theorem A: Pointwise Derivative Lower Bound

Assume, for all `T>=T0`, the shell zero count

```text
N_E(T,2T)
 := #{gamma: T<|gamma|<=2T, L(E,1+i gamma)=0}
 <= C_N T (log T)^B_N.
```

Assume all zeros in the shell are simple and that for some `alpha<1`,

```text
|L'(E,1+i gamma)|
 >= c_D T^(-alpha) (log T)^(-B_D)
```

for every zero in `T<|gamma|<=2T`.

Then

```text
J_E,2(T)
 <= C T^(1+2 alpha) (log T)^(B_N+2B_D).
```

Consequently, for every

```text
0 < delta < 2(1-alpha),
```

after increasing the constant and `T0`,

```text
J_E,2(T) <= C_{E,delta} T^(3-delta).
```

Proof:

```text
|L'(E,1+i gamma)|^(-2)
 <= c_D^(-2) T^(2 alpha) (log T)^(2B_D).
```

Multiplying by the shell count gives

```text
J_E,2(T)
 <= C_N c_D^(-2) T^(1+2 alpha) (log T)^(B_N+2B_D).
```

Since `alpha<1`, the logarithm is absorbed into `T^(2(1-alpha)-delta)` for any
fixed `delta<2(1-alpha)`.

Equivalent parametrization: if

```text
|L'(E,1+i gamma)| >= c_D T^(-1+eta) (log T)^(-B_D)
```

with `eta>0`, then the target holds for every `delta<2 eta`.

This is a valid theorem candidate, but it is not a proof of the desired
analytic input. The pointwise lower bound is stronger than the shell-moment
conclusion in the small-derivative direction.

## Conditional Theorem B: Small-Derivative Tail Criterion

Let

```text
R(gamma) = |L'(E,1+i gamma)|^(-1),
N_E(T;V) = #{gamma: T<|gamma|<=2T, R(gamma)>V}.
```

Assume all shell zeros are simple and the shell zero count from Theorem A. If
for some `0<delta0<2`, `epsilon>0`,

```text
N_E(T;V) <= C T^(3-delta0) V^(-2-epsilon)
```

for all `V>=1`, then

```text
J_E,2(T) <= C' T^(3-delta0).
```

Proof by layer cake:

```text
sum R(gamma)^2
 <= N_E(T,2T) + int_1^infty 2V N_E(T;V) dV
 <= C_N T(log T)^B_N
    + C T^(3-delta0) int_1^infty 2V^(-1-epsilon) dV.
```

Since `delta0<2`, the zero-count term is absorbed into
`T^(3-delta0)` after increasing the constant for large `T`.

A borderline version also works. If

```text
N_E(T;V) <= C T^(3-delta0) V^(-2)
```

for `1<=V<=T^A`, and a polynomial reciprocal cap

```text
R(gamma) <= T^A
```

holds on the shell, then

```text
J_E,2(T) <= C_A T^(3-delta0) log T.
```

Thus the target follows with every `delta<delta0`. This is an exact reduction
to a quantitative anti-concentration statement for small `L'(rho)`.

## Conditional Theorem C: Zero Repulsion Plus Minimum Modulus

Zero repulsion becomes useful only when paired with a lower bound for `|L|` on
a zero-free circle.

Assume every shell zero `rho=1+i gamma` is simple, and for each such `rho`
there is a radius

```text
r_T = T^(-kappa) (log T)^(-b)
```

such that the punctured disk `0<|s-rho|<=r_T` contains no zero of `L(E,s)`.
Assume also the boundary minimum-modulus bound

```text
min_{|s-rho|=r_T} |L(E,s)|
 >= c_M T^(-mu) (log T)^(-B_M).
```

Then

```text
|L'(E,rho)|
 >= c_M T^(-(mu-kappa)) (log T)^(-(B_M-b)).
```

Indeed, write

```text
L(E,s) = (s-rho) g_rho(s).
```

The function `g_rho` is holomorphic and nonzero in the disk. On the boundary,

```text
|g_rho(s)| = |L(E,s)|/r_T.
```

The minimum principle for the nonvanishing holomorphic function `g_rho` gives

```text
|L'(E,rho)| = |g_rho(rho)|
 >= min_{|s-rho|=r_T} |g_rho(s)|
 >= c_M T^(-(mu-kappa)) (log T)^(-(B_M-b)).
```

Therefore Theorem A applies with

```text
alpha = mu-kappa.
```

If `mu-kappa<1`, then

```text
J_E,2(T) <= C_{E,delta} T^(3-delta)
```

for every `delta<2(1-mu+kappa)`.

This reduction explains the limitation of spacing alone. A lower gap between
zeros gives a legal circle, but the derivative lower bound comes from the
minimum-modulus input, equivalently a local reciprocal bound for `1/L`.

## Conditional Theorem D: Positive Mollifier Majorant

Let `M_T(gamma)` be a mollifier or approximant on the shell. Suppose either:

```text
|M_T(gamma) - 1/L'(E,1+i gamma)|
 <= eps |1/L'(E,1+i gamma)|,       0<=eps<1,
```

for every shell zero, and

```text
sum_shell |M_T(gamma)|^2 <= C T^(3-delta),
```

or more generally there is a positive majorant `B_T(gamma)` such that

```text
|L'(E,1+i gamma)|^(-2) <= B_T(gamma),
sum_shell B_T(gamma) <= C T^(3-delta).
```

Then the target shell moment follows immediately. In the relative-approximation
case,

```text
|M_T(gamma)| >= (1-eps)|1/L'(E,1+i gamma)|,
```

so

```text
J_E,2(T) <= (1-eps)^(-2) sum_shell |M_T(gamma)|^2.
```

This is the correct shape of a mollifier route. The Li-Zaharescu-style data
audited in the dependency files do not supply this positive majorant for the
fixed H1 weight, and a signed mollified first moment cannot be converted into
this inequality without new input.

## Why GRH, Simplicity, And Spacing Do Not Suffice

GRH locates zeros on the line. It does not quantify `L'(rho)`.

Simple zeros say `L'(rho) != 0`. They give no lower rate such as
`|L'(rho)| >= T^(-1+eta)`. A sequence of simple zeros with
`|L'(rho)|` much smaller than any power is not excluded by simplicity alone.

Zero spacing or pairwise repulsion controls distances between zeros. It does
not control the leading coefficient in the local factorization

```text
L(E,s) = (s-rho) g_rho(s).
```

The shell moment is a sum of `|g_rho(rho)|^(-2)`. Spacing makes it possible to
choose a zero-free disk, but the value `g_rho(rho)` is controlled from below
only by a minimum-modulus or reciprocal estimate on that disk.

Almost-all simplicity is also insufficient. If the target sum includes all
zeros and even one shell zero has multiplicity `>1`, then `L'(rho)=0` and the
shell moment is infinite. If the sum is restricted to simple zeros, multiple
zeros still remain in the H1 Laurent exceptional package and cannot be erased
from the contour theorem.

## Exact No-Go Boundary

The desired bound is not presently derivable from the local wave inputs. The
following implications are invalid without an added anti-small-derivative
hypothesis:

```text
GRH + simple zeros
  => J_E,2(T) <= T^(3-delta).

GRH + simple zeros + zero spacing
  => J_E,2(T) <= T^(3-delta).

Many simple zeros
  => J_E,2(T) <= T^(3-delta) over all offcentral zeros.

Negative-moment lower bounds
  => negative-moment upper bounds.

Signed mollified reciprocal sums
  => fixed-weight positive reciprocal-square upper bound.

Li-Zaharescu ratio-polynomial weights
  => fixed H1 weight W_hat(i gamma) exp(i gamma u) on every shell.
```

The fixed-weight obstruction from the prior wave remains: ratio-polynomial
weights of length `M=T^theta` cannot uniformly represent the phase
`exp(i gamma u)` through the low and medium shells `T<exp(u/theta)`, and the
residual estimate already needs a reciprocal-derivative upper bound.

## Promotion-Ready Hypothesis

The clean named hypothesis to carry forward is:

```text
H1-shell-moment(E,delta):
  there exist C_E, T0, delta>0 such that for all T>=T0,
  J_E,2(T) <= C_E T^(3-delta),
  with the sum over simple zeros, and with multiple zeros handled separately
  by the Laurent exceptional-term theorem.
```

Sufficient ways to prove it are exactly:

```text
1. pointwise derivative lower bound with exponent alpha<1;
2. small-derivative tail bound stronger than V^(-2), or V^(-2) plus a
   polynomial reciprocal cap;
3. zero repulsion plus boundary minimum-modulus with mu-kappa<1;
4. a positive mollifier majorant or relative reciprocal approximation whose
   square norm is O(T^(3-delta)).
```

Current state: rigorous reduction, not a sourced proof of `H1-shell-moment`.
The bound should be promoted only as a named open hypothesis or as a conditional
theorem with one of the displayed anti-small-derivative inputs.
