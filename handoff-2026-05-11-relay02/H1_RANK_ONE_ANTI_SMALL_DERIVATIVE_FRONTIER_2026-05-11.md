---
schema_version: 1
title: "H1 rank-one anti-small-derivative frontier"
date: 2026-05-11
relay: "Relay[02]: farey-g3-h1-relay"
type: theorem-reduction
tier: working
status: REFINED_TARGET_NO_THEOREM_PROMOTED
confidence: 0.84
sources:
  - handoff-2026-05-11-all-in-wave/H1_LEGAL_HEIGHT_L1_CLOSURE_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/H1_SHELL_ANTI_SMALL_DERIVATIVE_PACKET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/H1_WEIGHTED_L1_ATTACK_PACKET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/H1_FIXED_WEIGHT_PV_PACKET_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-all-in-wave/H2_SYM2_ENDPOINT_PACKET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/EC_G3_FAILURE_DIAGNOSTIC_2026-05-11.md
tags: [ec-ndc, h1, rank-one, weighted-l1, reciprocal-derivative]
---

# H1 Rank-One Anti-Small-Derivative Frontier

status: `REFINED_TARGET_NO_THEOREM_PROMOTED`

## Verdict

No fixed-curve EC theorem is promoted.

For analytic rank one, the current legal-height H1 simple-zero target is exactly

```text
R_E,1(T)
 = sum_(T<|gamma|<=2T, simple) |L'(E,1+i gamma)|^(-1)
 = o(T^2).
```

This is the weakest currently named absolute-value route for the simple-zero
H1 residue aggregate in the source-safe exponential-height contour mode. It is
weaker than:

```text
R_E,1(T) <= T^(2-epsilon),
R_E,1(T) <= T^2 (log T)^(-1-delta),
J_E,2(T) <= T^(3-delta).
```

It is still a real anti-small-derivative theorem. H2 branch damping, selected
Li-Zaharescu horizontal heights, zero count, zero spacing, and the failed G3
finite numerics do not imply it.

## Exact Rank-One Reduction

Let `u=log K`, `r=1`, and use the same endpoint-smoothed `W` as the H1 contour
packet with

```text
|W_hat(it)| << (1+|t|)^(-2).
```

For dyadic shells put

```text
A_W(T) =
  sum_(T<|gamma|<=2T, simple)
    |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1).
```

Then

```text
A_W(T) << T^(-2) R_E,1(T).
```

The legal source-safe contour mode uses selected heights

```text
T_box(u) = exp(Cu + O(1))
```

for fixed `C>sigma>1/2`. Hence the number of dyadic shells below the box is

```text
N(u) = (C/log 2)u + O(1).
```

If

```text
R_E,1(T)=o(T^2),
```

then

```text
A_W(2^j)=o(1).
```

By the Cesaro lemma for nonnegative shells,

```text
sum_(j<=N(u)) A_W(2^j) = o(N(u)) = o(u).
```

Therefore the simple-zero offcentral absolute majorant satisfies

```text
M_W(u)=o(u),
```

which is exactly the rank-one H1 scale needed to make simple offcentral
residues lower order than the central term

```text
u/L'(E,1).
```

This proves only a reduction: the shell statement `R_E,1(T)=o(T^2)` remains
unproved.

## Layer-Cake Criterion

Define reciprocal derivative values

```text
R(gamma)=|L'(E,1+i gamma)|^(-1)
```

and the tail count

```text
N_E(T;V)=#{T<|gamma|<=2T, simple: R(gamma)>V}.
```

Since the values are nonnegative,

```text
R_E,1(T) = int_0^infty N_E(T;V) dV.
```

With the standard fixed-curve zero-count scale

```text
N_E(T,2T) << T log T,
```

the contribution of `0<=V<=1` is already `o(T^2)`. Thus rank-one H1 is
equivalent to the high-reciprocal tail condition

```text
int_1^infty N_E(T;V) dV = o(T^2).
```

Useful sufficient forms:

```text
Power tail:
  N_E(T;V) <= C T^2 Phi(T)^(-1) V^(-1-alpha),  V>=1,
  alpha>0, Phi(T)->infty
  => R_E,1(T)=o(T^2).

Borderline capped tail:
  N_E(T;V) <= C T^2 Phi(T)^(-1) V^(-1),  1<=V<=T^A,
  R(gamma)<=T^A,
  Phi(T)/log T -> infinity
  => R_E,1(T)=o(T^2).
```

These are cleaner rank-one targets than the older naked second-moment target.

## Pointwise Route

The uniform lower bound

```text
|L'(E,1+i gamma)| >= h(T) (log T)/T
```

for all simple zeros in `T<|gamma|<=2T`, with `h(T)->infinity`, implies

```text
R_E,1(T)
 <= N_E(T,2T) T/(h(T) log T)
 << T^2/h(T)
 = o(T^2).
```

So the rank-one pointwise threshold is not polynomial. It is only a diverging
factor above

```text
(log T)/T.
```

The common log-saving version

```text
|L'(E,1+i gamma)| >= (log T)^(1+delta)/T
```

is enough, but it is stronger than necessary.

## Sparse-Exception Budget

Rank one also allows sparse very-small-derivative exceptions. Suppose in a
dyadic shell:

```text
good zeros: R(gamma) <= T/(h(T) log T),  h(T)->infinity,
bad zeros:  #bad <= B(T),  R(gamma) <= C(T).
```

Then

```text
R_E,1(T) << T^2/h(T) + B(T)C(T).
```

Thus the rank-one H1 target follows if

```text
B(T)C(T)=o(T^2).
```

This is the most concrete next anti-small-derivative route: prove a tail
budget for rare near-multiple behavior rather than a uniform derivative lower
bound for every zero.

## What Does Not Close It

- Li-Zaharescu selected heights route horizontal contour bounds only; they do
  not give local lower bounds for `L'(rho)`.
- H2 S1/Sym2 branch terms have an extra `1/u`; H1 reciprocal poles do not.
- Fixed-weight PV can replace absolute `l1` only after a separate uniform
  phase-cancellation theorem for the actual coefficients
  `W_hat(i gamma)/L'(rho)`.
- G3 finite EC smoothing numerics failed the predeclared empirical-p gates and
  remain non-promotional.
- Rank zero is outside this closure; retained offcentral H1 terms are main
  scale unless killed, cancelled, subtracted, profiled, or averaged.

## Next Proof Target

For rank one, attack one of:

```text
Tail:
  int_1^infty N_E(T;V) dV = o(T^2).

Pointwise:
  min_(T<|gamma|<=2T) |L'(E,1+i gamma)|
    >= h(T)(log T)/T,  h(T)->infinity.

Sparse-exception:
  R(gamma) <= T/(h(T)log T) off a bad set with B(T)C(T)=o(T^2).

PV replacement:
  sum_T sup_(u in [U,2U])
    |sum_(T<|gamma|<=2T)
      W_hat(i gamma)e^(i gamma u)/L'(rho)|
  = o(U)
  along the same legal-height scheme.
```

Until one of these is proved for the fixed curve and exact kernel, the
positive-rank EC pointwise theorem spine stays conditional.
