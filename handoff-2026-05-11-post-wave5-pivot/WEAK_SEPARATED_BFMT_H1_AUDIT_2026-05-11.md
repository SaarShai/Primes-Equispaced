---
schema_version: 2
title: "Weak Separated BFMT H1 Audit"
type: theorem-audit
domain: project
tier: working
confidence: 0.86
created: 2026-05-11
updated: 2026-05-11
verified: 2026-05-11
sources:
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/WEAK_SEPARATED_BFMT_PIVOT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT01_SECTION5_GL2_CONDUCTOR_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT02_BFMT_EPSILON_DELTA_MARGIN_REFEREE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT03_SEPARATED_EC_BFMT_FINAL_THEOREM_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt
supersedes: []
superseded-by:
tags: [post-wave5, h1, bfmt, gl2, separated-zeros, reciprocal-derivative, conductor-audit]
---

# Weak Separated BFMT H1 Audit

Status: `CONDITIONAL_PASS_FOR_SEPARATED_H1`.

No full H1 theorem is promoted.  The bad-set complement and multiple-zero
disposition remain open.

## Verdict

The post-Wave-5 pivot is correct.

Wave 5 killed the strong zeta-quality separated target

```text
sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  << T^(1+delta).
```

It did not kill the weaker rank-one H1 target.  With the fixed-curve GL2
conductor term inserted, BFMT Section 5 moves to the second-branch ledger and
gives the source-audited bound

```text
sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  <<_(E,c,delta) T^(3/2+delta).
```

For any fixed `delta<1/2`, this is `o(T^2)`.  Therefore the separated
simple-zero contribution is conditionally harmless for rank-one H1, assuming
the Wave 4 local inputs and zero-sampling coefficient transcription.

The first H1 blocker should now be recorded as the bad-set complement, not the
degree-2 Section 5 sign lemma.  The sign lemma remains first only for the
stronger `T^(1+delta)` separated theorem.

## Target

Let

```text
L_E^*(s)=L(E,s+1/2),        alpha=1/log T,
rho=1/2+i gamma.
```

Let `F_E(T,c)` be the simple separated zero ordinates:

```text
F_E(T,c) = {gamma in (T,2T]:
  L(E,1+i gamma)=0 is simple and
  |gamma-gamma'| >= c/log T for every other zero ordinate gamma'}.
```

The audited weak target is:

```text
WeakSeparatedEC-BFMT-H1(E,c):
  for every delta>0,
  sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
    <<_(E,c,delta) T^(3/2+delta).
```

## Inputs Consumed

Closed conditional local inputs:

```text
GL2-ShiftDerivativeComparison(E,c):
  |L'(E,1+i gamma)|^(-1)
    <= T^o(1) |L(E,1+1/log T+i gamma)|^(-1)
  on F_E(T,c).

GL2-BFMT-PrimePolynomialLowerBound(E):
  BFMT lower bound with conductor-normalized archimedean term
  log C_E(t)=2 log T+O_E(1).

ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2):
  BFMT Propositions 2.5, 2.6, 2.7 survive with fixed polylog loss.
```

These are conditional on fixed-newform RH/GRH and the standard fixed-newform
explicit-formula package recorded in the Wave 4 packets.

## Source Check

BFMT Theorem 1.1 has two branches:

```text
T^(1+delta)             if 2k(1+epsilon)<=1,
T^(k+1/2+delta)         if 2k(1+epsilon)>1.
```

For the reciprocal first derivative moment, `2k=1`, so `k=1/2`.  BFMT is in
the second branch for every fixed `epsilon>0`.  The old EC transcription
incorrectly treated `k=1/2` as first-branch after choosing `epsilon` small.
Wave 5 correctly fixed that branch error.

In BFMT Section 5, equations `(5.10)` and `(5.17)` have the same large-branch
power shape:

```text
N(T) * T^((1+delta) k * (2k-A)/(2k-A+B)) * exp(o(log T)),
```

where

```text
A = a(2d-1)/r = 1+O(epsilon),
B = 2d-1 = 1+O(epsilon).
```

For zeta, this gives

```text
1 + k * (2k-1)/(2k) = k+1/2
```

after letting `epsilon` go to zero, matching BFMT Theorem 1.1.

For fixed GL2/EC, Wave 4 Agent01 changes the conductor/archimedean term from
`log T` to `2 log T+O_E(1)`.  The same Section 5 slot therefore changes

```text
2k -> 4k
```

and the pointwise/initial large-branch conductor load changes

```text
k -> 2k.
```

Thus the degree-2 rerun has power

```text
N_E(T) * T^((1+delta) 2k * (4k-A)/(4k-A+B)) * exp(o(log T)).
```

At `k=1/2`,

```text
2k=1,        4k=2,        A=1+O(epsilon),        B=1+O(epsilon),
```

so the exponent above is

```text
1 + 1 * (2-1)/(2-1+1) + O(epsilon) + O(delta)
  = 3/2 + O(epsilon) + O(delta).
```

After relabeling the small parameters, the separated simple-zero sum is

```text
<<_(E,c,delta) T^(3/2+delta).
```

This is the `T^(3/2+o(1))` ledger mentioned in Wave 5.  It is not a heuristic
description of failure; it is the second-branch BFMT power with the degree-2
conductor coefficient inserted.

## Audit Checklist

1. Wave 5 `T^(3/2+o(1))` source derivation:
   `PASS`.  It follows from BFMT equations `(5.10)`, `(5.12)`, `(5.13)`, and
   `(5.17)` after replacing the zeta conductor coefficient by the GL2
   coefficient.  The small-block sign no-go blocks only the stronger
   `T^(1+delta)` target.

2. Zero-sampling in the second branch:
   `PASS`.  The coefficient substitution adds fixed powers of `log T` in
   Propositions 2.5, 2.6, and 2.7.  BFMT `(5.10)` and `(5.17)` already carry
   `exp(o(log T))` slack, and `(5.12)` is already `N(T)(log T)^O(1)`.

3. Derivative-shift comparison:
   `PASS`.  Wave 4 Agent02 gives only `exp(O_(E,c)(log T/loglog T))=T^o(1)`
   on separated simple zeros.

4. Prime powers, bad primes, gamma endpoint errors, and `lambda_E` factors:
   `PASS`.  Wave 4 Agent01 and the zero-sampling audit keep these losses
   within fixed polylog or `T^o(1)` ranges.

5. H1 exponent threshold:
   `PASS`.  `T^(3/2+delta)=o(T^2)` for any fixed `delta<1/2`.

## Dependency Impact

Promote only this conditional separated statement:

```text
Wave 4 local inputs
+ zero-sampling coefficient transcription
+ conductor-normalized BFMT second-branch audit
=> WeakSeparatedEC-BFMT-H1(E,c).
```

Do not promote:

```text
SeparatedEC-BFMT(E,c,k=1/2) with T^(1+delta),
EC-BFMT-BadSetBudget(E,c),
R_E,1(T)=o(T^2) over all simple zeros,
multiple-zero control,
full H1 pointwise EC smoothing.
```

## Next Blocker

After this audit, the next live rank-one H1 target is the bad-set complement:

```text
R_B(T,c) =
  sum_(gamma notin F_E(T,c), simple) |L'(E,1+i gamma)|^(-1)
  = o(T^2).
```

The zero-centered `MinMod` route remains source-blocked.  The best follow-up is
the cluster-shift comparison route recorded in
`CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md`.

