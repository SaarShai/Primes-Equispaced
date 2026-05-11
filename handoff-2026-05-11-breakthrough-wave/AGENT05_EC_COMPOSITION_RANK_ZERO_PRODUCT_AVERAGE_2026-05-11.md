---
schema_version: 1
title: "Agent 05 EC composition: rank-zero profile and product average"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.78
sources:
  - start.md
  - L1_index.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/EC_POINTWISE_THEOREM_SPINE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/H2_SYM2_ENDPOINT_PACKET_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
tags: [agent05, ec-ndc, h1, h2, composition, rank-zero, product-average]
---

# Agent 05 EC Composition Packet

status: `RIGOROUS_REDUCTION`

mode label: `CONDITIONAL_COMPOSITION_PACKET_NO_THEOREM_PROMOTED`

## Verdict

No fixed-curve EC theorem is promoted here.

The H1/H2 composition is paper-ready only as a conditional theorem schema with
three distinct modes:

1. pointwise stabilization, valid only when the normalized H1 offcentral
   reciprocal-pole aggregate is `o(1)` after the H2 `u^(-r)` normalization;
2. pointwise oscillatory profile, valid when main-scale H1/H2 oscillations are
   retained explicitly;
3. arithmetic dyadic product average, valid when the product itself has joint
   H1/H2 mean extraction.

Rank zero is not a pointwise constant theorem. In analytic rank zero the honest
H1 object is

```text
c_E,W(e^u) = Q_0 + Z_c(u) + o(1),
```

unless every retained nonzero H1 reciprocal residue is killed, cancelled,
subtracted, or placed inside a proved averaged theorem.

All ranks below are analytic ranks:

```text
r = ord_(s=1) L(E,s).
```

No algebraic or script rank may be substituted without a separate equality
input.

## Common Setup

Fix an elliptic curve `E/Q`, one admissible endpoint-smoothed kernel `W`, and

```text
u = log K.
```

The H1 and H2 objects must use the same curve, the same kernel, the same scale,
and the same Mellin normalization.

H1 is written in reciprocal-Perron form:

```text
c_E,W(K)
 = (1/(2 pi i)) int_(Re z=sigma)
     K^z W_hat(z) / L(E,1+z) dz.
```

H2 uses the exact Agent-3 local factors from the endpoint packet:

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)).
```

The conditional H2 finite-part output has the form

```text
P_E,W(e^u)
 = exp(B_H2(E,W)) u^(-r) G(u)(1+eps_P(u)),
```

where `G(u)=1` in the pointwise nonoscillatory H2 theorem and
`G(u)=exp(Z_P(u))` in the retained oscillatory/product-average theorem mode.

The conditional H1 reciprocal expansion is organized as

```text
c_E,W(e^u)
 = Q_r(u)
   + sum_(gamma != 0) sum_(j >= 0) a_(gamma,j) u^j e^(i gamma u)
   + E_c(u),

Q_r(u) = q_r u^r + q_(r-1)u^(r-1) + ... + q_0.
```

For the repository-normalized H1 convention,

```text
q_r = 1/L^(r)(E,1).
```

The coefficients `a_(gamma,j)` are the combined H1 reciprocal-pole Laurent
residues at frequency `gamma`, after same-frequency cancellations and kernel
zeroes have been applied. A zero of multiplicity `m` can contribute powers up
to degree `m-1` before cancellations or filtering.

## Conditional Theorem A: Pointwise Composition

Assume:

```text
H2-pointwise:
  P_E,W(e^u) = exp(B_H2(E,W)) u^(-r)(1+o(1)).

H1-leading:
  c_E,W(e^u) = q_r u^r + o(u^r).
```

Equivalently, the H1 central lower powers, contour error, and offcentral
reciprocal-pole aggregate satisfy

```text
Q_r(u)-q_r u^r
 + sum_(gamma != 0) sum_(j >= 0) a_(gamma,j) u^j e^(i gamma u)
 + E_c(u)
 = o(u^r).
```

Then

```text
c_E,W(e^u) P_E,W(e^u)
 -> exp(B_H2(E,W)) q_r.
```

In the repository-normalized convention this is

```text
c_E,W(e^u) P_E,W(e^u)
 -> exp(B_H2(E,W)) / L^(r)(E,1).
```

For positive rank `r>=1`, bounded simple H1 residues are lower order after
the H2 factor `u^(-r)`. More generally, every retained offcentral H1 term must
have effective degree `< r`, or it must be killed, cancelled, subtracted, or
the theorem mode must be changed.

For rank zero, the condition becomes

```text
Z_c(u)+E_c(u) = o(1).
```

This is not automatic. Simple offcentral H1 reciprocal residues are already at
the main scale when `r=0`.

## Conditional Theorem B: Pointwise Oscillatory Composition

Assume a pointwise normalized H1 profile

```text
u^(-r)c_E,W(e^u) = H_c(u) + o(1),
```

where

```text
H_c(u) = q_r + sum_(gamma in Gamma_r) h_gamma e^(i gamma u)
```

contains exactly the retained H1 terms of degree `r`. Terms of degree `< r`
are absorbed into `o(1)` after normalization. Terms of degree `> r` are not
covered by this bounded-profile theorem and must be ruled out, cancelled,
renormalized, or stated as a higher-order profile.

Assume also a pointwise H2 profile

```text
P_E,W(e^u)
 = exp(B_H2(E,W)) u^(-r) G(u)(1+o(1)).
```

Then

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_H2(E,W)) H_c(u)G(u) + o(1).
```

This is the correct nonconstant pointwise theorem mode when retained
main-scale oscillations survive.

### Rank-Zero Specialization

For analytic rank zero,

```text
r = 0,
Q_0 = 1/L(E,1)
```

in the repository-normalized convention. If offcentral simple reciprocal
residues converge in the stated H1 profile mode, define

```text
Z_c(u)
 = sum_(gamma != 0) a_gamma e^(i gamma u),

a_gamma = W_hat(i gamma) / L'(E,1+i gamma)
```

after same-frequency aggregation. Then the claim-safe H1 statement is

```text
c_E,W(e^u) = Q_0 + Z_c(u) + o(1).
```

If H2 is pointwise nonoscillatory in rank zero, then

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_H2(E,W))(Q_0+Z_c(u)) + o(1).
```

If H2 has a retained pointwise oscillatory factor `G(u)`, then

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_H2(E,W))(Q_0+Z_c(u))G(u) + o(1).
```

The rank-zero pointwise constant

```text
exp(B_H2(E,W))/L(E,1)
```

is valid only after one of the following additional mechanisms is proved in
the same kernel and normalization:

```text
coefficient death:
  a_gamma = 0 for every retained gamma != 0;

same-frequency cancellation:
  the aggregated H1 residue at every gamma != 0 is 0;

explicit subtraction:
  c_E,W(e^u) - Z_c(u) = Q_0 + o(1);

averaging:
  the stated theorem is an arithmetic product average of c_E,W P_E,W,
  not a pointwise limit.
```

Conjugate pairing does not remove a real oscillation unless the aggregated
coefficient itself is zero.

## Conditional Theorem C: Arithmetic Product Average

Define the dyadic arithmetic average in `u=log K` by

```text
A_U(F) = (1/U) int_U^(2U) F(u) du
       = (1/U) int_exp(U)^exp(2U) F(log K) dK/K.
```

This is an arithmetic average of product values. It is not

```text
exp(A_U(log(c_E,W(e^u)P_E,W(e^u)))).
```

Assume the H1 normalized profile is valid in product mean:

```text
u^(-r)c_E,W(e^u) = H_c(u) + mean-small error,

H_c(u) = q_r + sum_(gamma in Gamma_r) h_gamma e^(i gamma u).
```

Assume the H2 product has an exponential branch profile in product mean:

```text
P_E,W(e^u)
 = exp(B_H2(E,W)) u^(-r) G(u)(1+mean-small error),

G(u) = exp(Z_P(u)).
```

Assume finite truncations

```text
H_Y(u) = sum_(gamma in Gamma(Y)) h_gamma e^(i gamma u),
G_Y(u) = sum_(eta in Lambda(Y)) d_eta e^(i eta u)
```

with joint tail control strong enough to pass from finite exponential
polynomials to the infinite H1/H2 profiles, and assume the diagonal sums

```text
D_Y =
 sum_(gamma in Gamma(Y), eta in Lambda(Y), gamma+eta=0)
   h_gamma d_eta
```

converge to `D`. Then

```text
A_U(c_E,W(e^u)P_E,W(e^u))
 -> exp(B_H2(E,W)) D.
```

Equivalently, when the limiting H2 mean coefficients are written as `d_eta`,

```text
D = q_r d_0 + sum_(gamma in Gamma_r) h_gamma d_(-gamma),
```

so

```text
A_U(c_E,W(e^u)P_E,W(e^u))
 -> exp(B_H2(E,W))
    (q_r d_0 + sum_(gamma in Gamma_r) h_gamma d_(-gamma)).
```

If H2 is pointwise nonoscillatory, then `G=1`, `d_0=1`, and `d_eta=0` for
`eta != 0`. Under the same H1 mean-tail hypotheses the product average reduces
to

```text
exp(B_H2(E,W)) q_r.
```

In rank zero this is

```text
exp(B_H2(E,W)) / L(E,1),
```

but only as an arithmetic dyadic product average. It is not a pointwise
constant limit unless `Z_c` is removed by one of the mechanisms in Theorem B.

## Mode Discipline

The three modes are not interchangeable.

- H2 branch damping gives `1/u` for H2 logarithmic branch terms, but H1
  reciprocal zeros are poles and do not receive this damping.
- An averaged theorem for `log P_E,W` does not imply an arithmetic average for
  `c_E,W P_E,W`.
- The product-average constant needs mean coefficients of `G(u)=exp(Z_P(u))`,
  not only mean coefficients of `Z_P(u)`.
- Diagonal correlations `h_gamma d_(-gamma)` are part of the arithmetic
  product-average constant and cannot be dropped without proof.
- Multiple offcentral H1 zeros with effective degree `>= r` block pointwise
  stabilization unless they are ruled out, cancelled, retained explicitly, or
  renormalized.

## Remaining Closure Conditions

The theorem packet remains conditional on:

1. H1 finite-box reciprocal Perron expansion for the same `W`;
2. H1 reciprocal-derivative/Laurent coefficient control and contour tails;
3. H1 convergence or mean-control mode for the retained zero profile;
4. H2 S1 branch continuation and contour legality;
5. H2 exact good-prime Sym2 finite part for the stated normalization;
6. weighted good-prime Mertens transfer for the same `W`;
7. mean coefficients of `G(u)=exp(Z_P(u))` when product averaging is used;
8. joint H1/H2 diagonal and tail extraction for the arithmetic product
   average.

No external theorem is cited here. Any future source-promoted theorem must
attach the repository citation packet: `curl + pdftotext + short quote +
page/equation`.

## Verification Notes

- Ran `./te doctor`: repository and wiki root reported OK.
- Read only the requested context files plus `start.md`, `token-economy.yaml`,
  `L0_rules.md`, and the two `L1_index.md` files.
- Used analytic rank only:

```text
r = ord_(s=1) L(E,s).
```

- Did not cite external theorems.
- Did not touch Koyama correspondence or email drafts.
- Did not promote fixed-curve EC stabilization, unconditional EC product
  average, or rank-zero pointwise stabilization.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT05_EC_COMPOSITION_RANK_ZERO_PRODUCT_AVERAGE_2026-05-11.md
```
