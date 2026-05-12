---
schema_version: 1
title: "H1 q>2 Bad-Set Route"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION_NO_THEOREM_PROMOTED
confidence: 0.84
tags: [h1, bad-set, reciprocal-derivative, shifted-negative-moment, rooted-correlation]
---

# H1 q>2 Bad-Set Route

Status: `RIGOROUS_REDUCTION_NO_THEOREM_PROMOTED`.

## Verdict

The next H1 bad-set attack should not try to prove the square rooted Palm
statistic first. Use the Holder family:

```text
q > 2,
p = q/(q-1) < 2.
```

Target:

```text
Degree2WeakShiftedNeg_q(E):
  sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-q)
    <<_(E,q,eps) T^(q+1/2+eps)

RootedInvProdCorr_p(E,A):
  sum_(rho in S_E(T)) W_A(rho)^p <<_(E,A,p) T log T.
```

Then cluster-shift plus Holder gives:

```text
R_B(T,c) << T^(2 - 1/(2q) + eps + o(1)) = o(T^2).
```

With the separated branch

```text
R_F(T,c) << T^(3/2+eps),
```

this closes the rank-one simple-zero budget conditionally on the two new
inputs.

## Exact Lemma Stack

Use these names:

```text
WeakSeparatedEC-BFMT-H1(E,c)
ClusterShiftDerivativeComparison(E,A)
Degree2WeakShiftedNeg_q(E)
RootedInvProdCorr_p(E,A)
RootedPalmRepulsionExpMoment_p(E,A)
H1-MultipleZeroDisposition(E,W,r)
```

Do not rename the multiple-zero condition as BFMT-specific; BFMT/shifted-value
tools only handle simple zeros.

## Derivation

The cluster comparison gives

```text
|(L_E^*)'(rho)|^(-1)
 <= T^o(1)(logT)^(-1) W_A(rho)
    |L_E^*(rho+1/logT)|^(-1).
```

Holder with exponents `q` and `p=q/(q-1)` yields

```text
R_B(T,c)
 << T^o(1)(logT)^(-1)
    (sum |L_E^*(rho+1/logT)|^(-q))^(1/q)
    (sum W_A(rho)^p)^(1/p).
```

Insert the two targets:

```text
R_B(T,c)
 << T^o(1)(logT)^(-1)
    T^(1+1/(2q)+eps)
    (TlogT)^(1-1/q)
 << T^(2 - 1/(2q) + eps + o(1)).
```

For `q=3`, this is `T^(11/6+eps+o(1))`.
For `q=4`, this is `T^(15/8+eps+o(1))`.
Both are `o(T^2)`.

## Source State

Current local source audits still do not close the singular rooted statistic.
The source gap is narrower than before: for `p=3/2` or `4/3`, the singularity
threshold is weaker than the old square `p=2` condition.

External primary-source scan:

- Bui-Milinovich-Turnage-Butterbaugh style negative-moment tools remain
  adjacent but not source-closed for this exact fixed-curve shifted zero
  sample.
- GL(2) gap papers and higher-level correlation papers support the model but
  do not supply uniform singular rooted inverse-product bounds.
- Recent upper-gap papers address existence or upper bounds on gaps, not the
  rooted Palm moment needed here.

Relevant external primary sources checked:

- arXiv:1410.7765, "Gaps between zeros of GL(2) L-functions".
- arXiv:2303.01095, "Multiplicity of nontrivial zeros of primitive
  L-functions via higher-level correlations".
- arXiv:2511.13898, "Upper bounds on gaps between zeros of L-functions".

## Next Actions

1. Audit whether the existing BFMT shifted-value argument extends from `q=2`
   to `q=3` and `q=4` with exponent `T^(q+1/2+eps)`.
2. Source-hunt/prove `RootedInvProdCorr_p(E,A)` for `p=3/2`, then `p=4/3`.
3. If no source closes it, state simple-zero H1 conditionally on this
   `p<2` rooted statistic and move effort to H2 endpoint and multiple-zero
   profile packaging.

## Boundary

Do not promote:

```text
RootedInvProdCorr_p(E,A)
RootedPalmRepulsionExpMoment_p(E,A)
full H1
EC fixed-curve stabilization
```

