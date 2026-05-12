---
schema_version: 1
title: "Post Wave 5 Weak Separated BFMT Pivot"
date: 2026-05-11
type: research-pivot
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.82
tags: [post-wave5, h1, bfmt, gl2, separated-zeros, reciprocal-derivative, bad-set]
---

# Post Wave 5 Weak Separated BFMT Pivot

## Verdict

No theorem is promoted, but Wave 5 likely over-targeted the separated branch.

Wave 5 correctly kills the strong statement

```text
SeparatedEC-BFMT(E,c,k=1/2):
  sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  << T^(1+delta).
```

That is not the exact H1 need.  Rank-one H1 only requires the total simple-zero
shell budget

```text
R_E,1(T)=o(T^2).
```

Therefore a weaker separated theorem would already be enough:

```text
WeakSeparatedEC-BFMT-H1(E,c):
  sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  << T^(theta+delta)
  for some theta<2.
```

The conductor-doubled BFMT ledger in Wave 5 appears to land at

```text
theta = 3/2,
```

not at a useless exponent.  If source-checked, this closes the separated
simple-zero contribution for H1.  The next true H1 blocker would then be the
close-zero/bad-set complement, not the strong Section 5 sign lemma.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md`: records the `NO_GO` for the strong `T^(1+delta)` separated target and the `2k -> 4k` obstruction.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT01_SECTION5_GL2_CONDUCTOR_AUDIT_2026-05-11.md`: states that the conductor-normalized ledger gives a `T^(3/2+o(1))`-type output rather than `T^(1+delta)`.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT03_SEPARATED_EC_BFMT_FINAL_THEOREM_2026-05-11.md`: rejects `SeparatedEC-BFMT(E,c,k=1/2)` but also records the literal inserted ledger as `T^(3/2+o(1))` type.
- `primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`: rank-one H1 simple-zero closure needs exactly `R_E,1(T)=o(T^2)`.
- `primes-equispaced/handoff-2026-05-11-all-in-wave/H1_LEGAL_HEIGHT_L1_CLOSURE_2026-05-11.md`: positive-rank legal-height target is `R_E,1(T)=o(T^2(logT)^(r-1))`; rank one is `o(T^2)`.
- `/tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt`: BFMT Theorem 1.1 has the second branch `T^(k+1/2+delta)` for zeta when `2k(1+epsilon)>1`; Wave 5 shows the degree-2 conductor changes the effective branch for `k=1/2`.

## Key Observation

Wave 5 answered this question:

```text
Can the fixed-EC separated branch match zeta BFMT at T^(1+delta)?
```

Answer:

```text
No, not with the printed BFMT Section 5 ledger.
```

But the H1 finite-box problem asks a different question:

```text
Can the separated branch contribute o(T^2)?
```

For rank one, if the conductor-normalized BFMT argument proves

```text
sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  << T^(3/2+delta),
```

then for any fixed `delta<1/2`,

```text
T^(3/2+delta)=o(T^2).
```

Thus separated zeros would be harmless for H1.  The strong
`ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2)` is needed only to recover
the zeta-quality `T^(1+delta)` theorem, not necessarily to reach H1.

## Required Audit

The immediate next task is not another attempt to force `2k -> 2k`.  It is:

```text
WeakSeparatedEC-BFMT-H1-Audit(E,c).
```

Target statement:

```text
Under the Wave 4 local inputs and homogeneous zero-sampling transcription,
the conductor-normalized Section 5 ledger proves

sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  <<_(E,c,delta) T^(3/2+delta).
```

The audit must check:

```text
1. The Wave 5 `T^(3/2+o(1))` statement is actually source-derived from
   BFMT equations (5.10), (5.17), (5.12), and the conductor-doubled (5.13),
   not just heuristic wording.

2. The homogeneous zero-sampling replacement for Propositions 2.5-2.7 remains
   legal in the second-branch parameter regime.

3. The derivative-shift comparison still costs only T^o(1) on F_E(T,c).

4. Prime powers, bad primes, gamma endpoint errors, and lambda_E coefficient
   factors stay below T^delta.

5. The final exponent is strictly below 2 after all small losses.
```

If this audit passes, the separated part of the H1 rank-one simple-zero budget
is closed conditionally on the existing fixed-newform RH/explicit-formula
package.  The synthesis should then stop calling the conductor sign lemma the
first H1 blocker.  It remains the first blocker only for the stronger
zeta-quality separated theorem.

## Bad-Set Breakthrough Route

After the weak separated audit, the real H1 wall is:

```text
R_B(T,c)=sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1)=o(T^2).
```

Wave 5 showed:

```text
MinMod(E,c,A,h)          NO_GO from current sources,
ProductLayer             reduced to rooted inverse-product correlations J_m,
DirectComplementTail      reduced to fixed-EC reciprocal derivative tails.
```

The next promising route is not zero-centered minimum modulus.  It is a
cluster-aware shifted-value comparison.

For a bad simple zero `rho` with nearby cluster

```text
C_rho={rho=rho_0,rho_1,...,rho_(m)}
```

and `alpha=1/logT`, factor locally:

```text
L(E,s)=(s-rho_0) product_(j=1)^m (s-rho_j) H_rho(s).
```

Then formally,

```text
|L'(E,rho_0)|^(-1)
  <= T^o(1)
     alpha product_(j=1)^m |alpha+rho_0-rho_j| / |rho_0-rho_j|
     |L(E,rho_0+alpha)|^(-1),
```

provided the noncluster factor ratio `H_rho(rho_0+alpha)/H_rho(rho_0)` is
controlled by local zero counting/Hadamard, not by a zero-centered minimum
modulus.

This suggests a new target:

```text
ClusterShiftDerivativeComparison(E,A):
  bad-zero reciprocal derivatives are bounded by shifted reciprocal values
  times explicit normalized inverse-product cluster weights, with T^o(1) loss.
```

If paired with:

```text
1. a weak shifted negative moment
   sum |L(E,1+1/logT+i gamma)|^(-q) << T^(1+eta_q),

2. rooted inverse-product correlation bounds J_m(T;A),
```

then the bad-set complement may close without `MinMod`.

This route is attractive because it uses the shifted value that BFMT already
knows how to estimate.  It avoids asking for a pointwise lower bound for
`|L|` on tiny zero-centered boundary circles, the exact source gap that killed
`MinMod`.

## Next Breakthrough Tasks

1. `WeakSeparatedEC-BFMT-H1-Audit(E,c)`  
   Verify the conductor-normalized BFMT ledger gives `T^(3/2+delta)` for
   separated reciprocal first derivatives.  Success closes the separated H1
   contribution.

2. `ClusterShiftDerivativeComparison(E,A)`  
   Prove the local cluster comparison from `L'(rho)` to
   `L(rho+1/logT)` with explicit inverse-product weights and only `T^o(1)`
   loss.  This is the best route around `MinMod`.

3. `ShiftedValueWithClusterWeights(E,A,q)`  
   Combine weak shifted negative moments with rooted inverse-product
   correlations.  The goal is a bad-set bound `R_B(T,c)=o(T^2)` without
   pointwise minimum-modulus certificates.

4. `H1-MultipleZeroDisposition(E,W,r)`  
   Keep the Wave 5 multiple-zero cleanup as a theorem statement choice:
   central-negligible, kernel-killed, absent by named simplicity, or retained
   profile.

## Updated Breakthrough Map

Old Wave 5 map:

```text
First blocker = ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2).
```

Refined map:

```text
For zeta-quality separated theorem:
  first blocker = ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2).

For H1 rank-one closure:
  first task = audit WeakSeparatedEC-BFMT-H1(E,c).
  if it passes, first blocker = bad-set complement without MinMod.
```

This is a better breakthrough path because it uses exactly the H1 threshold
instead of trying to recover a stronger zeta-quality bound that H1 does not
need.

