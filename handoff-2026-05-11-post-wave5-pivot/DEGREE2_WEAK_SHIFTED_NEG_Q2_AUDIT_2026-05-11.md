---
schema_version: 2
title: "Degree2 Weak Shifted Negative Moment q=2 Audit"
type: theorem-audit
domain: project
tier: working
confidence: 0.82
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/SHIFTED_CLUSTER_WEIGHT_CRITERION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/WEAK_SEPARATED_BFMT_H1_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt
supersedes: []
superseded-by:
tags: [post-wave5, h1, shifted-values, negative-moment, bfmt, gl2, conductor-audit]
---

# Degree2 Weak Shifted Negative Moment q=2 Audit

Status: `CONDITIONAL_PASS_FOR_SHIFTED_Q2`.

No H1 theorem is promoted.

## Verdict

The fixed-EC degree-2 BFMT ledger gives the concrete shifted-value input needed
by the cluster-weight criterion at `q=2`:

```text
Degree2WeakShiftedNeg_2(E):
  sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-2)
    <<_(E,epsilon) T^(5/2+epsilon).
```

This uses the same Wave 4 local inputs as the weak separated audit:

```text
GL2-BFMT-PrimePolynomialLowerBound(E) in conductor-normalized form,
ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1),
fixed-newform RH/explicit-formula normalization.
```

Unlike the derivative moment, this shifted moment does not require the
separated derivative-shift comparison.  BFMT Lemma 2.4 is already a direct
upper majorant for shifted reciprocal values at all zero ordinates.

The remaining bad-set input is therefore the square cluster statistic

```text
RootedInvProdCorr_2(E,A):
  sum_(rho in S_E(T)) W_A(rho)^2 << T log T.
```

Together with the cluster-shift local comparison, these imply

```text
R_B(T,c) << T^(7/4+epsilon+o(1)) = o(T^2).
```

## Target

Let

```text
alpha=1/log T,
X(rho)=|L_E^*(rho+alpha)|^(-1),
S_E(T)={simple critical zeros rho=1/2+i gamma: T<|gamma|<=2T}.
```

The audited target is

```text
sum_(rho in S_E(T)) X(rho)^2 << T^(5/2+epsilon).
```

This is the `q=2` case of

```text
Degree2WeakShiftedNeg_q(E):
  sum X(rho)^q << T^(q+1/2+epsilon).
```

## Source Check

BFMT Lemma 2.4 states that for every zero ordinate `gamma in (T,2T]`, either
the first block polynomial is large, or

```text
|zeta(1/2+1/logT+i gamma)|^(-2k) <= S1(gamma)+S2(gamma).
```

This is a shifted-value statement over all zero ordinates.  It does not use
the separated set `F`.  The separated set enters later only when BFMT compares
`zeta'(rho)` to `zeta(rho+1/logT)`.

BFMT Proposition 2.5 bounds the large first-block contribution, while
Propositions 2.6 and 2.7 bound the `S2` and `S1` terms.  The zero-sampling
substitution audit already replaces these coefficient estimates for fixed EC
with only fixed polylogarithmic losses.  The only load-bearing EC change is the
degree-2 conductor term from Wave 4 Agent01:

```text
log C_E(t)=2logT+O_E(1).
```

Therefore the same second-branch bookkeeping as the weak separated audit
applies, but now with `q=2`, i.e.

```text
2k=q=2,        k=1.
```

For the degree-2 conductor rerun, the BFMT second-branch power becomes

```text
N_E(T) * T^((1+delta) 2k * (4k-A)/(4k-A+B)) * exp(o(logT)),
```

with

```text
A=a(2d-1)/r=1+O(epsilon),
B=2d-1=1+O(epsilon).
```

At `k=1`,

```text
2k=2,        4k=4,
```

so the exponent is

```text
1 + 2 * (4-1)/(4-1+1) + O(epsilon)
  = 1 + 3/2 + O(epsilon)
  = 5/2 + O(epsilon).
```

After relabeling small parameters:

```text
sum_(rho in S_E(T)) X(rho)^2 << T^(5/2+epsilon).
```

## Bad-Set Consequence

Use the cluster-shift local comparison:

```text
|L_E^*'(rho)|^(-1)
 <= T^o(1) alpha W_A(rho) X(rho).
```

By Cauchy,

```text
sum_(rho in B_E(T,c)) W_A(rho)X(rho)
 <= (sum X(rho)^2)^(1/2)
    (sum W_A(rho)^2)^(1/2).
```

If

```text
sum X(rho)^2 << T^(5/2+epsilon),
sum W_A(rho)^2 << T log T,
```

then

```text
R_B(T,c)
 <= T^o(1) (logT)^(-1)
    T^(5/4+epsilon) T^(1/2)(logT)^(1/2)
 << T^(7/4+epsilon+o(1)).
```

This is `o(T^2)`.

## Boundary

Promote only:

```text
Degree2WeakShiftedNeg_2(E)
```

as a conditional audit result from the BFMT/zero-sampling/conductor-normalized
stack.

Do not promote:

```text
RootedInvProdCorr_2(E,A),
DirectComplementTail(E,c),
R_E,1(T)=o(T^2),
full H1.
```

The new first blocker for the bad-set route is now sharply:

```text
RootedInvProdCorr_2(E,A).
```

For pair clusters this asks for square inverse-gap integrability; cubic
close-pair repulsion would be enough for the pair layer, but higher clusters
still need the corresponding singular inverse-product statistic.

