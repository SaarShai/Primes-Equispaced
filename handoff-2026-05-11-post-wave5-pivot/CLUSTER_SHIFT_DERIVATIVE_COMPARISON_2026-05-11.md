---
schema_version: 2
title: "Cluster Shift Derivative Comparison"
type: theorem-reduction
domain: project
tier: working
confidence: 0.82
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/WEAK_SEPARATED_BFMT_PIVOT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT04_MINMOD_SOURCE_AND_PROOF_HUNT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT05_PRODUCT_LAYER_INVERSE_DISTANCE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt
supersedes: []
superseded-by:
tags: [post-wave5, h1, bad-set, cluster, reciprocal-derivative, shifted-values, minmod-bypass]
---

# Cluster Shift Derivative Comparison

Status: `CONDITIONAL_LOCAL_THEOREM`.

No bad-set budget is promoted.  This packet removes the zero-centered
minimum-modulus demand from the local comparison step and replaces it with a
shifted-value estimate plus explicit inverse-product cluster weights.

## Verdict

The cluster-shift comparison route works as a local theorem.

For a simple bad zero `rho0` and `alpha=1/log T`, factor the zeros in a
microscopic cluster around `rho0` and compare `L'(rho0)` to `L(rho0+alpha)`.
The exact factorization gives

```text
|L'(rho0)|^(-1)
  = alpha * prod_(rho_j in C\{rho0})
      |alpha+rho0-rho_j| / |rho0-rho_j|
    * |H_C(rho0+alpha)|/|H_C(rho0)|
    * |L(rho0+alpha)|^(-1).
```

The noncluster ratio satisfies

```text
|H_C(rho0+alpha)|/|H_C(rho0)| <= exp(O_(E,A)(log T/loglog T)) = T^o(1)
```

under fixed-newform RH and the same local zero-count input used by the
separated shift-derivative comparison, provided the cluster contains all zeros
within `A/log T` of `rho0`.

Thus:

```text
ClusterShiftDerivativeComparison(E,A):
  |L'(rho0)|^(-1)
    <= T^o(1) alpha W_C(rho0)
       |L(rho0+alpha)|^(-1),

  W_C(rho0)=prod_(rho_j in C\{rho0})
      (|alpha+rho0-rho_j| / |rho0-rho_j|).
```

This bypasses `MinMod(E,c,A,h)` at the point where `MinMod` was only being used
to lower-bound a zero-centered circle value.  The remaining task is global:
sum the shifted values with the cluster weights.

## Setup

Work with the normalized function

```text
L_E^*(s)=L(E,s+1/2).
```

Write zeros as

```text
rho = 1/2+i gamma
```

for `L_E^*`.  Fix `A>0`, put `alpha=1/log T`, and let `rho0=1/2+i gamma0`
be a simple zero with `T<|gamma0|<=2T`.

Let the cluster be

```text
C_A(rho0) = {rho_j: 0<|rho_j-rho0|<=A/log T} union {rho0}.
```

Define the noncluster factor by

```text
L_E^*(s) = (s-rho0) prod_(rho_j in C_A(rho0)\{rho0}) (s-rho_j) H_A(s).
```

This is a local Hadamard factorization notation: `H_A` absorbs the remaining
zeros, gamma/conductor factor, and nonzero holomorphic factor in the standard
completed-function quotient.

## Exact Identity

Since `rho0` is simple,

```text
(L_E^*)'(rho0)
  = prod_(rho_j in C_A(rho0)\{rho0}) (rho0-rho_j) * H_A(rho0).
```

Also

```text
L_E^*(rho0+alpha)
  = alpha * prod_(rho_j in C_A(rho0)\{rho0})
      (alpha+rho0-rho_j) * H_A(rho0+alpha).
```

Dividing gives the exact comparison:

```text
|(L_E^*)'(rho0)|^(-1)
  = alpha
    prod_(rho_j in C_A(rho0)\{rho0})
      |alpha+rho0-rho_j| / |rho0-rho_j|
    * |H_A(rho0+alpha)|/|H_A(rho0)|
    * |L_E^*(rho0+alpha)|^(-1).
```

No minimum-modulus lower bound appears in this identity.

## Noncluster Ratio Bound

It remains to bound

```text
R_A(rho0) := |H_A(rho0+alpha)|/|H_A(rho0)|.
```

For every zero outside `C_A(rho0)`,

```text
|rho-rho0| > A alpha.
```

Under RH the nontrivial zeros lie on the same vertical line as `rho0`, while
the shift `alpha` is horizontal.  Therefore the logarithm of each zero-factor
ratio is bounded by a constant times

```text
min(1, alpha^2/|rho-rho0|^2)
```

on the local range; the usual completed-function Hadamard quotient handles the
far tail together with the gamma/conductor factor.
Use the fixed-newform zero-count input from Wave 4 Agent02:

```text
N_E(t+u)-N_E(t-u) <<_E u log T + log T/loglog T + 1
```

for `t asymp T`.

Dyadic annuli

```text
2^j A alpha < |rho-rho0| <= 2^(j+1) A alpha
```

give total logarithmic ratio

```text
sum_j (2^j A + log T/loglog T) * 2^(-2j)/A^2
  <<_A log T/loglog T.
```

The gamma/conductor quotient over a shift of length `alpha` is `O_E(1)`.
Therefore

```text
log R_A(rho0) <<_(E,A) log T/loglog T,
R_A(rho0) <= T^o(1).
```

This is the same quality of loss as the separated derivative-shift comparison.

## Consequence

For every simple zero `rho0` in the dyadic shell,

```text
|(L_E^*)'(rho0)|^(-1)
  <= T^o(1) alpha W_A(rho0)
     |L_E^*(rho0+alpha)|^(-1),
```

where

```text
W_A(rho0)
 = prod_(rho_j in C_A(rho0)\{rho0})
     |alpha+rho0-rho_j| / |rho0-rho_j|.
```

For a cluster mate with normalized distance

```text
u_j = log T * |rho_j-rho0|,
```

the weight is

```text
|alpha+rho0-rho_j| / |rho0-rho_j|
  <= (1+u_j)/u_j
  <<_A u_j^(-1)
```

when `0<u_j<=A`, up to an `A`-dependent harmless constant.  Thus the old
ProductLayer rooted inverse-product weights reappear naturally, but now
attached to a shifted reciprocal value instead of a zero-centered
minimum-modulus certificate.

## Bad-Set Closure Target

The bad-set complement would follow from a weighted shifted negative-moment
theorem of the form

```text
sum_(rho0 in B_E(T,c))
  W_A(rho0) |L_E^*(rho0+alpha)|^(-1)
  << T^(2-eta) log T
```

for some fixed `eta>0`, because the prefactor is `alpha=1/log T` and the
`T^o(1)` ratio can then be absorbed.  A softer `o(T^2 log T)` bound is not by
itself enough unless its saving is quantified strongly enough to beat the
`T^o(1)` loss.

A plausible sufficient package is:

```text
1. weak shifted negative moments over zero ordinates:
   sum |L_E^*(rho+alpha)|^(-q) << T^(1+eta_q);

2. rooted inverse-product cluster correlations J_m(T;A);

3. a Holder split matching the cluster weight exponent to q.
```

This is now the sharp follow-up target:

```text
ShiftedValueWithClusterWeights(E,A,q).
```

## Boundary

This packet proves only the local comparison under fixed-newform RH and the
standard local zero-count/Hadamard inputs.

It does not prove:

```text
R_B(T,c)=o(T^2),
RootedInvProdCorr(E,A),
shifted negative moments with cluster weights,
multiple-zero control,
full H1.
```

It does replace the local use of

```text
MinMod(E,c,A,h)
```

by an explicit shifted-value comparison.  That is the real advantage: no
pointwise lower bound for `L` on zero-centered microscopic boundary circles is
asked for.
