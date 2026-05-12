---
schema_version: 2
title: "Shifted Cluster Weight Criterion"
type: theorem-reduction
domain: project
tier: working
confidence: 0.84
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/WEAK_SEPARATED_BFMT_H1_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT05_PRODUCT_LAYER_INVERSE_DISTANCE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT06_DIRECT_COMPLEMENT_TAIL_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT05_H1_RECIPROCAL_TAIL_THEOREM_2026-05-11.md
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt
supersedes: []
superseded-by:
tags: [post-wave5, h1, bad-set, shifted-values, cluster-weights, holder, reciprocal-derivative]
---

# Shifted Cluster Weight Criterion

Status: `RIGOROUS_REDUCTION`.

No bad-set theorem is promoted.

## Verdict

The cluster-shift route reduces the bad-set complement to two precise global
inputs:

```text
Degree2WeakShiftedNeg_q(E):
  sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-q)
    << T^(q+1/2+epsilon)

RootedInvProdCorr_p(E,A):
  sum_(rho in S_E(T)) W_A(rho)^p << T log T
```

for conjugate exponents

```text
q>1,        p=q/(q-1).
```

Then

```text
R_B(T,c)=sum_(rho in B_E(T,c)) |(L_E^*)'(rho)|^(-1)=o(T^2).
```

The exponent arithmetic has real slack:

```text
R_B(T,c)
  << T^(2-1/(2q)+epsilon+o(1)).
```

Thus any fixed `q>1` works if both inputs are available with enough epsilon
margin.

The catch is that `RootedInvProdCorr_p` is stronger than the previous
ProductLayer statistic.  It requires `p`-th inverse-product integrability, not
just first inverse-product integrability.  For pair clusters, GUE-strength
cubic close-pair repulsion would allow only `p<3`, i.e. `q>3/2`.  Higher
clusters need the corresponding singular `p`-integrability.

## Setup

Let

```text
alpha=1/log T,
X(rho)=|L_E^*(rho+alpha)|^(-1).
```

For a bad simple zero `rho`, define the cluster weight from the local
comparison packet:

```text
W_A(rho)
 = prod_(rho_j in C_A(rho)\{rho})
     |alpha+rho-rho_j| / |rho-rho_j|.
```

The local comparison gives

```text
|(L_E^*)'(rho)|^(-1)
  <= T^o(1) alpha W_A(rho) X(rho).
```

Therefore

```text
R_B(T,c)
 <= T^o(1) alpha
    sum_(rho in B_E(T,c)) W_A(rho) X(rho).
```

## Holder Step

For `q>1` and `p=q/(q-1)`, Holder gives

```text
sum_B W_A(rho) X(rho)
 <= (sum_B X(rho)^q)^(1/q)
    (sum_B W_A(rho)^p)^(1/p).
```

It is enough to bound the first sum over all simple zeros in the shell:

```text
sum_B X(rho)^q <= sum_(rho in S_E(T)) X(rho)^q.
```

Assume

```text
ShiftedNeg_q(E):
  sum_(rho in S_E(T)) X(rho)^q << T^mu_q.
```

and

```text
ClusterWeight_p(E,A):
  sum_(rho in B_E(T,c)) W_A(rho)^p << T^nu_p (log T)^C.
```

Then

```text
R_B(T,c)
  << T^o(1) (log T)^(-1)
     T^(mu_q/q) T^(nu_p/p) (log T)^(C/p).
```

Thus the clean criterion is:

```text
mu_q/q + nu_p/p < 2.
```

If equality holds, one needs an explicit logarithmic saving strong enough to
beat the `T^o(1)` loss from the local comparison.

## Natural BFMT/Cluster Exponents

The degree-2 BFMT weak ledger predicts the shifted negative moment exponent

```text
mu_q = q + 1/2,
```

where `q=2k`.  This is the same calculation as the weak separated audit at
`q=1`, but it must be separately audited for the desired `q>1`.

The natural cluster-weight target is

```text
nu_p = 1,
```

because there are `T log T` zeros in the dyadic shell and local random-matrix
statistics should have bounded `p`-weighted rooted cluster integral when the
singularity is integrable.

Substituting

```text
mu_q=q+1/2,       nu_p=1,       1/p=1-1/q
```

gives

```text
mu_q/q + nu_p/p
 = (q+1/2)/q + 1/p
 = 1 + 1/(2q) + 1 - 1/q
 = 2 - 1/(2q)
 < 2.
```

Therefore the route closes the bad set with a fixed power saving:

```text
R_B(T,c) << T^(2-1/(2q)+epsilon+o(1)).
```

## Cluster Statistic Needed

Let

```text
u_j = log T * |rho_j-rho|.
```

For `m>=1`, define the `p`-singular rooted inverse-product statistic

```text
J_m^(p)(T;A)
 =
 sum_(rho0 in S_E(T))
 sum_(rho1,...,rhom distinct; 0<u_j<=A)
   prod_(j=1)^m u_j^(-p).
```

The sufficient cluster condition is

```text
RootedInvProdCorr_p(E,A):
  sum_(m>=1) C_A^m/m! * J_m^(p)(T;A)
    <<_(E,A,p) T log T.
```

This implies

```text
sum_(rho in B_E(T,c)) W_A(rho)^p << T log T.
```

This is strictly stronger than Wave 5 Agent05's first-power condition
`RootedInvProdCorr(E,A)`, which corresponds to `p=1`.

For pair clusters, if

```text
Q_1(T;u)
 = #{(rho0,rho1): log T |rho1-rho0| <= u}
 << T log T * u^beta,
```

then

```text
J_1^(p)(T;A) << T log T
```

follows when

```text
beta > p.
```

The GUE/zeta cubic-repulsion model has `beta=3`, so the pair layer suggests
choosing

```text
p<3,        equivalently q>3/2.
```

Higher clusters require the analogous integrability near every coordinate
hyperplane and diagonal collision; ordinary fixed-test `n`-level correlations
still do not suffice.

## Source Status

Closed in this packet:

```text
ClusterShiftDerivativeComparison
+ Holder
+ ShiftedNeg_q(E)
+ RootedInvProdCorr_p(E,A)
=> DirectComplementTail(E,c).
```

Not closed:

```text
Degree2WeakShiftedNeg_q(E) for any q>1,
RootedInvProdCorr_p(E,A) for any p>1,
multiple-zero control.
```

The next exact source/audit task is:

```text
Degree2WeakShiftedNeg_q-Audit(E,q):
  rerun the conductor-normalized BFMT second-branch ledger for a fixed q>1,
  preferably q>3/2, and verify that the shifted-value moment over EC zero
  ordinates has exponent q+1/2+epsilon.
```

The next exact statistics task is:

```text
RootedInvProdCorr_p(E,A):
  prove or assume p-singular rooted inverse-product correlation at scale
  1/log T, with p=q/(q-1).
```

## Dependency Impact

If both tasks pass for one fixed `q>3/2`, then the H1 simple-zero budget is
conditionally closed:

```text
WeakSeparatedEC-BFMT-H1(E,c)        handles F_E(T,c),
ShiftedClusterWeightCriterion      handles B_E(T,c),
```

leaving only multiple-zero disposition and finite-box contour hypotheses for
the full rank-one H1 package.

