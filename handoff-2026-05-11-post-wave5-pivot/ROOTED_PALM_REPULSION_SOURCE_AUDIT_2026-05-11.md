---
schema_version: 2
title: "Rooted Palm Repulsion Source Audit"
type: source-audit
domain: project
tier: working
confidence: 0.80
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/ROOTED_INVPROD_CORR2_REDUCTION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT05_PRODUCT_LAYER_INVERSE_DISTANCE_2026-05-11.md
  - https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf
  - https://arxiv.org/abs/2303.01095
  - https://arxiv.org/abs/2503.15449
supersedes: []
superseded-by:
tags: [post-wave5, h1, source-audit, rooted-correlation, pair-correlation, n-level-correlation, source-gap]
---

# Rooted Palm Repulsion Source Audit

Status: `SOURCE_GAP`.

No zero-statistics theorem is promoted.

## Verdict

The standard pair/n-level correlation sources do not currently supply

```text
RootedPalmRepulsionExpMoment_2(E,A)
```

or the equivalent square rooted inverse-product bound

```text
sum_(m>=1) C_A^(2m)/m! * J_m^(2)(T;A) << T log T.
```

They support the GUE target and justify it as the right conjectural local
model, but they are not a source-closed proof of the singular moment needed by
the q=2 bad-set route.

## What The Sources Give

Rudnick-Sarnak compute n-level correlations for zeros of primitive principal
L-functions in a restricted Fourier-support regime.  Their setup uses smooth
test functions satisfying symmetry, translation invariance, and rapid decay on
the difference hyperplane, and Theorem 1.1 assumes restricted support for the
Fourier transform.  Under RH, Theorem 1.2 gives GUE n-level correlations for
those restricted tests.

This is the right ambient theorem for ordinary local statistics.

Recent higher-level-correlation work also uses the Hejhal/Rudnick-Sarnak
asymptotic to bound zero multiplicity proportions.  That confirms the source
family is strong enough for some diagonal/multiplicity questions, but it does
not by itself produce inverse-square rooted moment bounds.

Recent pair-correlation work records that PCC can imply density-one simplicity
and critical-line conclusions.  That is valuable but still weaker than the
weighted close-pair estimate required here.

## Why This Does Not Close The q=2 Blocker

The needed pair layer is not just a fixed-window pair-correlation limit.  It is
a uniform near-zero upper law:

```text
Q_1(T;u) << T log T * u^beta,        beta>2,
0<u<=A.
```

Only then does

```text
J_1^(2)(T;A)
 = int_(0,A] u^(-2) dQ_1(T;u)
```

converge at the lower endpoint.

Likewise, higher n-level convergence against smooth fixed tests does not imply

```text
J_m^(2)(T;A)
 = int_(0,A]^m (u_1...u_m)^(-2) dnu_(m,T,A)
 << T log T.
```

The test weight is singular at `u_j=0`.  Approximating it by smooth cutoffs
would require quantitative error control as the cutoff shrinks with `T`, plus a
uniform rooted density majorant near the coordinate hyperplanes.  The cited
correlation results are not stated in that form.

Density-one simplicity is also insufficient.  A zero-density exceptional set
can still carry a large inverse-square cluster weight.

## Exact Missing Source

The source gap is now narrow:

```text
RootedPalmRepulsionExpMoment_2(E,A):
  for fixed E and A, the rooted local zero process has enough uniform
  root-point repulsion and cluster-size tail to imply
  sum_m C_A^(2m)/m! J_m^(2)(T;A) << TlogT.
```

A source could close this in any of the following forms:

```text
1. Direct singular moment bounds for J_m^(2), summable in m.
2. A uniform rooted Palm density majorant with prod_j u_j^2 repulsion.
3. Uniform box laws nu_m(prod_j (0,u_j]) << TlogT prod_j u_j^beta
   with beta>2 and summable constants.
4. A bounded-cluster theorem plus direct J_m^(2) bounds for all allowed m.
```

## Boundary

Promote:

```text
Existing pair/n-level correlation sources: useful GUE model and ordinary
correlation evidence, but SOURCE_GAP for RootedPalmRepulsionExpMoment_2.
```

Do not promote:

```text
RootedPalmRepulsionExpMoment_2(E,A),
RootedInvProdCorr_2(E,A),
DirectComplementTail(E,c),
full H1.
```

## Next Task

The next source hunt should be explicit:

```text
Search for uniform small-gap upper laws or Palm correlation majorants for
zeros of fixed GL2 L-functions, not ordinary fixed-test n-level convergence.
```

If no such theorem exists, the paper route should state the q=2 bad-set branch
conditionally on `RootedPalmRepulsionExpMoment_2(E,A)` and keep the RMT
argument as heuristic support only.
