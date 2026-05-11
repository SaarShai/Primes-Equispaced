---
schema_version: 1
title: "Breakthrough Wave 3 Synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.87
tags: [breakthrough-wave-3, h1, reciprocal-derivative, h2, s1, gl1]
---

# Breakthrough Wave 3 Synthesis

Status: `RIGOROUS_REDUCTION`. No theorem is promoted.

Wave 3 sharpened the H1 wall and repaired the H2 S1 target. It did not close
rank-one H1, but it narrowed the next useful theorem search to two named H1
inputs:

```text
GL2-LandauGonek-DPMV(E,theta)
EC-BFMT-BadSetBudget(E,c)
```

It also replaced the literal H2 S1 cut-plane theorem at smoothstep decay by a
renormalized form:

```text
S1-CutPlane-RenormalizedLogGrowth(E,W,eta)
```

or by the stronger-kernel alternative `|W_hat| << |t|^(-2-epsilon)`.

## Packet Ledger

| agent | packet | result | durable outcome |
|---|---|---|---|
| 01 | `AGENT01_GL2_BFMT_ADAPTATION_BLUEPRINT_2026-05-11.md` | `RIGOROUS_REDUCTION` | BFMT adapts only as a conditional separated-zero GL2/EC blueprint. Central missing input is `GL2-LandauGonek-DPMV(E,theta)`. H1 still needs an independent bad-set reciprocal budget. |
| 02 | `AGENT02_FIXED_CURVE_RECIP_DERIV_SOURCE_HUNT_2026-05-11.md` | `NO_GO` | No source-checked fixed-curve GL2/EC theorem was found for the needed reciprocal derivative budget. Li-Zaharescu is adjacent but wrong-direction for absolute upper tails. BFMT remains zeta-only model evidence. |
| 03 | `AGENT03_SEPARATED_ZERO_RECIP_BUDGET_2026-05-11.md` | `RIGOROUS_REDUCTION` | Separation alone is a no-go. Separation plus local boundary minimum modulus proves `S_F(T;c)=o(T^2)`. Pair-correlation and RMT remain non-promotional. |
| 04 | `AGENT04_BAD_SET_COMPLEMENT_BUDGET_2026-05-11.md` | `RIGOROUS_REDUCTION` | Bad sets are theorem-ready only as reciprocal budgets. Count-only controls, spacing statistics, zero-density, and simplicity proportions do not bound `sum X_rho`. |
| 05 | `AGENT05_MINIMUM_MODULUS_LOCAL_FACTOR_2026-05-11.md` | `NO_GO` | Zero-free circles or Cartan/Jensen alone do not give local lower bounds. Exact threshold: if `m_T/r_T >= T^(-alpha)(log T)^lambda`, then `R_E,1(T) <= T^(1+alpha)(log T)^(1-lambda)`, beating rank-one H1 only when `alpha<1` or `alpha=1, lambda>1`. |
| 06 | `AGENT06_ACTUAL_COEFFICIENT_H1_PV_THEOREM_2026-05-11.md` | `NO_GO` | Actual coefficients alone do not prove pointwise moving-window PV. Keep `H1-ActualDyadicShellPV(E,W,r,H)` only as a future theorem or as a consequence of reciprocal-derivative domination. |
| 07 | `AGENT07_H1_FINITE_BOX_THEOREM_SECTION_2026-05-11.md` | `RIGOROUS_REDUCTION` | Extracted the conditional H1 theorem section with stable hypothesis names: analytic rank, kernel decay, fixed Perron identity, central polynomial, legal heights, right-half residue handling, simple reciprocal budget, and multiple effective degree. |
| 08 | `AGENT08_S1_CUTPLANE_LOG_GROWTH_2026-05-11.md` | `RIGOROUS_REDUCTION` | Literal `S1-CutPlane-LogGrowth(E,W,eta)` fails at smoothstep `|t|^-2` because global branch constants can accumulate like `2 pi i N(t)` on the left edge. Repair by renormalized log growth or stronger kernel decay. |
| 09 | `AGENT09_S1_RIGHT_BRANCH_CLASSIFICATION_2026-05-11.md` | `RIGOROUS_REDUCTION` | `NoRightBranch_S1` is not proved. Right branches are shifted right-of-central zeros of `L(E,s)` in the contour range. Legal H2 must retain `B_S1^+(K;E,W,c)` unless a no-right-zero or cancellation theorem is supplied. |
| 10 | `AGENT10_GL1_H1_ACTUAL_PV_COUPLING_2026-05-11.md` | `RIGOROUS_REDUCTION` | One abstract moving-shell PV wrapper covers GL1 and H1 formally, but their arithmetic coefficient hypotheses remain separate. No GL1-to-H1 transfer is available. |

## H1 Outcome

The rank-one H1 target remains:

```text
R_E,1(T)=o(T^2).
```

The broad source hunt is now killed. The next useful H1 theorem route is not a
generic literature hunt; it is this paired target:

```text
GL2-LandauGonek-DPMV(E,theta)
```

with the coefficient ranges needed to adapt BFMT on separated zeros, plus

```text
EC-BFMT-BadSetBudget(E,c):
sum_{gamma notin F_E(T,c)} |L'(E,1+i gamma)|^(-1)=o(T^2).
```

Only the pair can close rank-one H1.

Minimum-modulus work is also narrowed. It is useful only if it proves a
zero-centered boundary certificate with

```text
m_T/r_T >= T^(-alpha)(log T)^lambda
```

where either `alpha<1` or `alpha=1, lambda>1`. Zero-freeness, Cartan/Jensen,
Hadamard products, and selected horizontal heights do not supply this on their
own.

The pointwise actual-coefficient PV route is not dead as a possible theorem,
but it is dead as a consequence of current inputs. Name it explicitly:

```text
H1-ActualDyadicShellPV(E,W,r,H).
```

Do not substitute spacing, square moments, profile modes, or H2 branch damping
for it.

## H1 Paper Package

Wave 3 produced the claim-safe conditional H1 theorem section:

```text
H1-FiniteBox-Conditional.
```

Its named inputs are:

```text
H1-AnalyticRank(E)
H1-KernelPoleDecay(W)
H1-FixedKernelPerron(E,W,sigma)
H1-CentralPolynomialNormalization(E,W,r)
H1-LegalExponentialHeights(E,W,sigma,eta,C)
H1-NoSilentRightHalfResidues(E,W,sigma,eta)
H1-SimpleReciprocalBudget(E,r)
H1-MultipleEffectiveDegree(E,W,r)
```

This section is ready for conditional paper use, but it is not a promoted EC
stabilization theorem.

## H2 Outcome

Wave 2 had reduced H2 to `S1-CutPlane-LogGrowth(E,W,eta)`. Wave 3 found that
the literal global-branch version is not legal for smoothstep-scale
`|W_hat| << |t|^-2`: branch constants can accumulate like zero counts, so the
left-edge absolute integral behaves like

```text
int (t log t) t^(-2) dt,
```

which diverges.

The legal replacement is:

```text
S1-CutPlane-RenormalizedLogGrowth(E,W,eta),
```

where local branch logs are subtracted and cut-lip jumps are retained, or else
use a stronger kernel with `|W_hat|, |W_hat'| << |t|^(-2-epsilon)`.

Right branches cannot be silently dropped. In the standard EC normalization,
they are exactly shifted right-of-central zeros of `L(E,s)` in the contour
range. The legal retained-term H2 mode includes:

```text
B_S1^+(K;E,W,c)
 = -(1/log K) sum_{rho in Z_S1^+(E;c)}
      m_rho K^(rho-1) W_hat(rho-1).
```

If no-right-branch input is unavailable, state H2 with `B_S1^+` retained or
subtracted.

## GL1 Outcome

Use the shared wrapper name only as a deterministic final step:

```text
AbstractActualMovingShellPV(Omega,b,H,Phi).
```

The arithmetic hypotheses remain separate:

```text
H1-ActualDyadicShellPV(E,W,r,H)
GL1-ActualMovingShellPV(chi,rho,T)
```

GL1 sharp cutoff still needs its own target-dependent coefficient theorem for

```text
1 / ((lambda-rho)L'(lambda,chi)).
```

## Acceptance Check

Wave 3 succeeds by strict reduction and no-go pruning:

- broad fixed-curve reciprocal derivative source hunt is `NO_GO`;
- BFMT adaptation is reduced to `GL2-LandauGonek-DPMV(E,theta)` plus
  `EC-BFMT-BadSetBudget(E,c)`;
- minimum-modulus route has an exact exponent threshold and no standalone
  proof;
- actual-coefficient pointwise PV is `NO_GO` from current inputs;
- H2 S1 is repaired to renormalized log growth or stronger-kernel mode;
- right branches are classified and must be retained unless excluded.

No theorem is promoted.

## Next Single Highest-Leverage Target

The next highest-leverage theorem target is:

```text
GL2-LandauGonek-DPMV(E,theta)
```

for fixed `E`, with exactly the coefficient ranges needed by the BFMT
separated-zero adaptation.

Reason: if it fails, the BFMT-style separated-zero route is dead. If it
succeeds, the only remaining H1 analytic target is the explicit bad-set
reciprocal budget `EC-BFMT-BadSetBudget(E,c)`.

For H2, the next target is secondary:

```text
S1-CutPlane-RenormalizedLogGrowth(E,W,eta)
```

plus retained right-branch bookkeeping.

