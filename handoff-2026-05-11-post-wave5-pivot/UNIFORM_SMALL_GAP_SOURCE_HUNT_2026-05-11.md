---
schema_version: 2
title: "Uniform Small Gap Source Hunt"
type: source-audit
domain: project
tier: working
confidence: 0.78
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_INVPROD_CORR2_REDUCTION_2026-05-11.md
  - https://arxiv.org/abs/1810.08843
  - https://arxiv.org/abs/1410.7765
  - https://arxiv.org/abs/2604.05733
  - https://eprints.whiterose.ac.uk/id/eprint/7669/
supersedes: []
superseded-by:
tags: [post-wave5, h1, source-audit, small-gaps, pair-correlation, gl2, rooted-correlation, source-gap]
---

# Uniform Small Gap Source Hunt

Status: `SOURCE_GAP_WITH_PARTIAL_INPUTS`.

No `RootedPalmRepulsionExpMoment_2` theorem is promoted.

## Verdict

The available small-gap literature gives useful partial evidence and sometimes
existence/proportion statements, but not the uniform near-zero upper law needed
for the q=2 bad-set branch:

```text
Q_1(T;u) << T log T * u^beta,        beta>2,
0<u<=A.
```

Nor does it give the higher rooted singular moment

```text
sum_m C_A^(2m)/m! J_m^(2)(T;A) << TlogT.
```

Thus the blocker remains:

```text
RootedPalmRepulsionExpMoment_2(E,A).
```

## Sources Checked

### Chirre-Goncalves, Pair Correlation Estimates

The arXiv abstract states that the paper studies zeros of `zeta` and other
L-functions via Montgomery's pair-correlation approach, improving bounds for
distinct zeros, small-gap counts, and multiplicity sums using semidefinite
programming.

This is adjacent and valuable.  It still works through pair-correlation
auxiliary functions and proportion/count bounds, not a uniform inverse-square
rooted moment.  It does not appear to supply a bound strong enough to integrate

```text
int_0^A u^(-2) dQ_1(T;u)
```

with endpoint convergence.

### Barrett-McDonald-Miller-Ryan-Turnage-Butterbaugh-Winsor

The GL2 gaps paper proves large gaps for fixed primitive GL2 forms and, using
Murty-Perelli pair correlation, proves existence of small gaps for primitive
Selberg-class L-functions.  In particular, for primitive holomorphic GL2 cusp
forms, it obtains gaps at most about `0.823` times average spacing under the
stated assumptions.

This is the right GL2 neighborhood.  But it is an existence result for small
gaps, not a uniform upper bound on the number of very small rooted gaps as
`u->0`.  It is not enough for `J_1^(2)`, and it gives no higher-rooted
singular moment.

### Inoue 2026 Small-Gap Improvement

The 2026 zeta paper introduces a resonance-correlation method and proves, under
RH, an improved liminf small-gap bound `mu<0.50895`.

This is current and relevant for zeta small-gap technology.  It is still an
existence/liminf theorem, not a uniform upper law or Palm repulsion theorem.
It also concerns `zeta`, not fixed GL2/EC zeros.

### Hall Extreme-Value Input

Hall's result on extreme values of `zeta` between critical-line zeros includes
`theta^3`-type behavior for small `theta`, described as positive evidence for
the small-gap side of Montgomery pair correlation.

This is useful heuristic support for cubic repulsion, but it is not stated as a
rooted pair-count upper law and does not control higher clusters.

## Why These Inputs Still Miss The Target

The q=2 cluster branch is sensitive to arbitrarily close root-mate collisions:

```text
J_1^(2)(T;A) = int_(0,A] u^(-2) dQ_1(T;u).
```

Existence of small gaps has the opposite direction from what is needed.  It
shows some gaps are small, while the inverse-square moment requires that very
small gaps are not too numerous.

A positive proportion or density-one simplicity result also misses the target.
The exceptional set can have zero density and still dominate an inverse-square
sum.

The higher terms are stricter:

```text
J_m^(2)(T;A)
 = int_(0,A]^m (u_1...u_m)^(-2) dnu_(m,T,A).
```

They require rooted repulsion near every coordinate hyperplane and a summable
cluster-size tail.

## Usable Conditional Replacement

The exact paper-safe condition remains:

```text
UniformRootedSmallGap_2(E,A):
  Q_1(T;u) << TlogT * u^beta, beta>2, 0<u<=A,
```

for the pair layer, plus

```text
HigherRootedPalmSquare(E,A):
  sum_(m>=2) C_A^(2m)/m! J_m^(2)(T;A) << TlogT.
```

Together these are equivalent in use to

```text
RootedPalmRepulsionExpMoment_2(E,A).
```

## Boundary

Promote:

```text
Small-gap literature: adjacent and supportive, but SOURCE_GAP for the q=2
rooted inverse-square cluster statistic.
```

Do not promote:

```text
UniformRootedSmallGap_2(E,A),
HigherRootedPalmSquare(E,A),
RootedPalmRepulsionExpMoment_2(E,A),
RootedInvProdCorr_2(E,A),
DirectComplementTail(E,c),
full H1.
```

## Next Task

Assemble the current simple-zero H1 branch conditionally:

```text
Weak separated BFMT audit
+ q=2 shifted BFMT audit
+ RootedPalmRepulsionExpMoment_2(E,A)
=> rank-one simple-zero reciprocal derivative budget.
```

Then keep multiple-zero disposition as a separate named blocker.
