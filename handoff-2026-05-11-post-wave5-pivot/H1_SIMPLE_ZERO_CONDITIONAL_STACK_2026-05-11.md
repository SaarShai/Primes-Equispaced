---
schema_version: 2
title: "H1 Simple Zero Conditional Stack"
type: theorem-reduction
domain: project
tier: working
confidence: 0.84
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/WEAK_SEPARATED_BFMT_H1_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/SHIFTED_CLUSTER_WEIGHT_CRITERION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_INVPROD_CORR2_REDUCTION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/UNIFORM_SMALL_GAP_SOURCE_HUNT_2026-05-11.md
supersedes: []
superseded-by:
tags: [post-wave5, h1, simple-zeros, conditional-stack, reciprocal-derivative, bfmt, rooted-correlation]
---

# H1 Simple Zero Conditional Stack

Status: `CONDITIONAL_SIMPLE_ZERO_CLOSURE`.

No full H1 theorem is promoted.

## Verdict

The post-Wave-5 pivot now gives a clean conditional simple-zero budget:

```text
WeakSeparatedEC-BFMT-H1-Audit(E,c)
+ Degree2WeakShiftedNeg_2(E)
+ RootedPalmRepulsionExpMoment_2(E,A)
=> R_E,1^simp(T) = o(T^2).
```

Here

```text
R_E,1^simp(T)
 = sum_(rho simple, T<|gamma|<=2T) |(L_E^*)'(rho)|^(-1).
```

This is exactly the rank-one simple-zero reciprocal derivative scale needed by
the H1 finite-box residue branch.

The only unresolved simple-zero input is now the zero-statistics condition

```text
RootedPalmRepulsionExpMoment_2(E,A).
```

The BFMT/shifted-value side is no longer the first blocker in this branch.

## Decomposition

Fix `c>0` and split the simple zeros in a dyadic shell:

```text
S_E(T) = F_E(T,c) union B_E(T,c),
```

where `F_E(T,c)` is the separated set and `B_E(T,c)` is its close-cluster
complement.

Then

```text
R_E,1^simp(T) = R_F(T,c) + R_B(T,c).
```

## Separated Branch

The weak separated BFMT audit gives, conditionally on the Wave 4 local GL2
inputs and zero-sampling transcription,

```text
R_F(T,c) <<_(E,c,epsilon) T^(3/2+epsilon).
```

This is already

```text
o(T^2).
```

The key point is that rank-one H1 does not need the stronger zeta-quality
`T^(1+delta)` separated bound killed by Wave 5.

## Bad-Set Branch

The cluster-shift comparison gives

```text
|(L_E^*)'(rho)|^(-1)
 <= T^o(1) (logT)^(-1) W_A(rho)
    |L_E^*(rho+1/logT)|^(-1).
```

The q=2 shifted BFMT audit gives

```text
sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-2)
  <<_(E,epsilon) T^(5/2+epsilon).
```

If

```text
RootedInvProdCorr_2(E,A):
  sum_(rho in S_E(T)) W_A(rho)^2 <<_(E,A) TlogT,
```

then Cauchy gives

```text
R_B(T,c)
 << T^o(1) (logT)^(-1)
    T^(5/4+epsilon) (TlogT)^(1/2)
 << T^(7/4+epsilon+o(1)).
```

Thus

```text
R_B(T,c)=o(T^2).
```

The square cluster statistic follows from the stronger but cleaner condition

```text
RootedPalmRepulsionExpMoment_2(E,A):
  sum_m C_A^(2m)/m! J_m^(2)(T;A) << TlogT.
```

## Combined Simple-Zero Budget

Combining the branches:

```text
R_E,1^simp(T)
 << T^(3/2+epsilon) + T^(7/4+epsilon+o(1))
 = o(T^2).
```

This is the best current theorem-shaped result of the post-Wave-5 pivot.

## Boundary

Promote only the conditional stack:

```text
Assuming Wave 4 local inputs, zero-sampling transcription, and
RootedPalmRepulsionExpMoment_2(E,A), the simple-zero H1 reciprocal derivative
budget closes.
```

Do not promote:

```text
RootedPalmRepulsionExpMoment_2(E,A),
RootedInvProdCorr_2(E,A),
multiple-zero disposition,
finite-box H1 contour closure,
full H1.
```

## Remaining H1 Blockers

The live blockers after this stack are:

```text
1. RootedPalmRepulsionExpMoment_2(E,A)
   or equivalent fixed-curve uniform rooted small-gap/Palm majorant.

2. H1-MultipleZeroDisposition(E,W,r)
   for non-simple offcentral zeros and any effective-degree contribution.

3. Finite-box contour hypotheses already tracked in the H1 finite-box packets.
```

No further conductor-normalized BFMT audit should be first in queue unless it
attacks a different moment exponent or removes the Palm statistics input.
