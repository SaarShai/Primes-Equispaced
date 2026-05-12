---
schema_version: 2
title: "Rooted Inverse Product Correlation 2 Reduction"
type: theorem-reduction
domain: project
tier: working
confidence: 0.81
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/SHIFTED_CLUSTER_WEIGHT_CRITERION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT05_PRODUCT_LAYER_INVERSE_DISTANCE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT03_EC_BFMT_BADSET_BUDGET_2026-05-11.md
supersedes: []
superseded-by:
tags: [post-wave5, h1, bad-set, cluster-weights, rooted-correlation, inverse-product, gap-repulsion]
---

# Rooted Inverse Product Correlation 2 Reduction

Status: `RIGOROUS_REDUCTION_NOT_PROVED`.

No H1 theorem is promoted.

## Verdict

After the `q=2` shifted BFMT audit, the bad-set route has one sharp remaining
simple-zero blocker:

```text
RootedInvProdCorr_2(E,A):
  sum_(rho0 in S_E(T)) W_A(rho0)^2 <<_(E,A) T log T.
```

This packet rewrites that blocker into exact singular rooted correlation
statistics.  It also separates what pair repulsion can and cannot prove.

Pair layer:

```text
Q_1(T;u) << T log T * u^beta,     beta>2
```

uniformly for `0<u<=A` implies the one-mate contribution

```text
J_1^(2)(T;A) << T log T.
```

This is compatible with the GUE cubic-repulsion model `beta=3`.

Higher layers:

ordinary fixed-window `n`-level counts do not suffice.  One needs either the
direct square singular statistic, a product-threshold layer cake, or a rooted
Palm/repulsion majorant with summable cluster-size constants.

The next exact target is therefore:

```text
RootedPalmRepulsionExpMoment_2(E,A)
```

or any equivalent theorem implying the exponential square inverse-product
bound below.

## Setup

Use the normalized critical-line notation of the post-Wave-5 packets.  Let

```text
alpha = 1/log T,
S_E(T) = {simple zeros rho0=1/2+i gamma0 : T<|gamma0|<=2T},
u(rho0,rho) = log T * |rho-rho0|.
```

For fixed `A>0`, define the close-mate set

```text
C_A'(rho0) = {rho != rho0 : 0<u(rho0,rho)<=A}.
```

The cluster-shift packet gives

```text
|(L_E^*)'(rho0)|^(-1)
 <= T^o(1) alpha W_A(rho0) |L_E^*(rho0+alpha)|^(-1),
```

where

```text
W_A(rho0)
 = prod_(rho in C_A'(rho0))
     |alpha+rho0-rho| / |rho0-rho|.
```

Under the RH/local critical-line normalization used in that packet,

```text
|alpha+rho0-rho| / |rho0-rho|
 = sqrt(1+u(rho0,rho)^2) / u(rho0,rho)
 <= C_A / u(rho0,rho)
```

for `0<u<=A`.

## Exact Square Expansion

Put

```text
g(rho0,rho) = C_A^2 * u(rho0,rho)^(-2).
```

Then

```text
W_A(rho0)^2 <= prod_(rho in C_A'(rho0)) g(rho0,rho)
             <= prod_(rho in C_A'(rho0)) (1+g(rho0,rho)).
```

Expanding the final product gives

```text
sum_(rho0 in S_E(T)) W_A(rho0)^2
 <= #S_E(T)
    + sum_(m>=1) C_A^(2m)/m! * J_m^(2)(T;A),
```

where

```text
J_m^(2)(T;A)
 =
 sum_(rho0 in S_E(T))
 sum_(rho1,...,rhom distinct; 0<u_j<=A)
   prod_(j=1)^m u_j^(-2),

u_j = u(rho0,rhoj).
```

Therefore a sufficient and essentially exact square cluster condition is

```text
SquareRootedInvProdExp(E,A):
  sum_(m>=1) C_A^(2m)/m! * J_m^(2)(T;A)
    <<_(E,A) T log T.
```

This implies `RootedInvProdCorr_2(E,A)` and, with the q=2 shifted BFMT audit,
the bad-set estimate

```text
R_B(T,c) << T^(7/4+epsilon+o(1)).
```

## Pair Layer

Define the rooted close-pair counting function

```text
Q_1(T;u)
 =
 #{(rho0,rho1): rho0 in S_E(T), rho1 != rho0,
   log T |rho1-rho0| <= u}.
```

Then

```text
J_1^(2)(T;A) = int_(0,A] u^(-2) dQ_1(T;u).
```

If

```text
Q_1(T;u) <<_(E,A) T log T * u^beta
```

uniformly for `0<u<=A`, with `beta>2`, Stieltjes integration by parts gives

```text
J_1^(2)(T;A)
 <= A^(-2) Q_1(T;A)
    + 2 int_0^A Q_1(T;u) u^(-3) du
 <<_(E,A,beta) T log T.
```

The threshold is exactly `beta>2`.  A cubic close-pair law is enough for this
layer.  A pair law with only `beta<=2` is not enough for the square weight.

This pair estimate proves only the `m=1` part of
`SquareRootedInvProdExp(E,A)`.

## Higher Layers

For `m>=2`, let `nu_(m,T,A)` be the rooted ordered local measure placing one
atom at

```text
(u_1,...,u_m)
```

for each tuple in the definition of `J_m^(2)(T;A)`.  Then

```text
J_m^(2)(T;A)
 = int_(0,A]^m (u_1...u_m)^(-2) dnu_(m,T,A).
```

The required input is not a plain count

```text
nu_(m,T,A)((0,A]^m) << T log T.
```

The singularity sits at the coordinate hyperplanes `u_j=0`.  Thus the needed
estimate must control how often one or more mates approach the root.

Three sufficient forms are useful:

```text
Direct:
  J_m^(2)(T;A) <= C_m(E,A) T log T
  and sum_m C_A^(2m) C_m(E,A)/m! < infinity.
```

```text
Box-repulsion:
  nu_(m,T,A)(prod_j (0,u_j])
    <= C_m(E,A) T log T * prod_j u_j^beta
  for some beta>2, with summable constants.
```

```text
Rooted Palm majorant:
  dnu_(m,T,A)(u)
    <= C_m(E,A) T log T
       prod_j u_j^2 * H_m(u) du,
```

where

```text
int_(0,A]^m H_m(u) du < infinity
```

and the resulting constants are summable after the factor `C_A^(2m)/m!`.

The GUE/Palm heuristic has exactly this shape: the root-point repulsion
contributes `prod_j u_j^2`, cancelling the square inverse-root singularity.
That heuristic is evidence for the right target, not a source-closed EC
theorem.

## Boundary

Promote only the reduction:

```text
SquareRootedInvProdExp(E,A) => RootedInvProdCorr_2(E,A).
```

and the pair-layer consequence:

```text
Q_1(T;u) << T log T * u^beta, beta>2
=> J_1^(2)(T;A) << T log T.
```

Do not promote:

```text
RootedInvProdCorr_2(E,A),
SquareRootedInvProdExp(E,A),
RootedPalmRepulsionExpMoment_2(E,A),
DirectComplementTail(E,c),
full H1.
```

Multiple-zero disposition is still separate.  Any multiple zero or zero
coincidence at the root scale would create an atom at `u=0`, which is invisible
to fixed-window count statements but fatal for the square inverse-product
integral.

## Next Task

The high-leverage continuation is no longer another BFMT conductor audit.  It
is a zero-statistics theorem:

```text
RootedPalmRepulsionExpMoment_2(E,A):
  prove a fixed-curve rooted local correlation majorant strong enough to imply
  SquareRootedInvProdExp(E,A).
```

A bounded-cluster-size theorem plus direct `J_m^(2)` estimates for every
allowed `m` would also suffice.
