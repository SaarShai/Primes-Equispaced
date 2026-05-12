---
title: "AGENT08 H1 Finite Box Closure Referee"
date: 2026-05-11
type: theorem-referee
tier: final
status: NO_GO
confidence: 0.91
tags: [breakthrough-wave-5, h1, finite-box, bfmt, gl2, reciprocal-derivative, multiple-zeros, no-go]
---

## Verdict

Status: `NO_GO`.

Do not promote H1 finite-box closure from Wave 5 Agents 01-07.

The first unclosed blocker is already inside the separated simple-zero branch:

```text
ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2).
```

Agents 01, 02, and 03 independently reject the required separated EC-BFMT
estimate from the current inputs.  The obstruction is the fixed-curve GL2
analytic conductor:

```text
log C_E(t) = 2 log T + O_E(1).
```

In BFMT Section 5 this changes the load-bearing coefficient from `2k` to `4k`.
At `k=1/2`, the printed BFMT support regime would need

```text
a(2d-1) > 2
```

or in the large-branch normalization

```text
a(2d-1)/r > 2.
```

That inequality is unavailable.  Therefore the separated estimate

```text
sum_(rho in F_E(T,c)) |L'(E,rho)|^(-1)
  <<_(E,c,delta) T^(1+delta)
```

is not proved.

Downstream blockers remain real but are not first: Agent04 reports `MinMod`
`NO_GO`; Agent05 gives only a rigorous product-layer reduction; Agent06 gives
only a rigorous direct-tail reduction; Agent07 replaces the misleading
multiple-zero condition by an explicit disposition/profile condition.  None of
these repairs the separated branch.

## Theorem Target

Finite-box H1 target, in project normalization:

```text
E/Q fixed,
r = ord_(s=1) L(E,s) >= 1,
u = log K,
rho = 1+i gamma.
```

For a fixed H1 kernel `W`,

```text
c_E,W(e^u)
  = (1/(2 pi i)) int e^(u z) W_hat(z)/L(E,1+z) dz.
```

The central-only target is

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r)
           = (w_-1/L^(r)(E,1)) u^r + o(u^r).
```

The simple-zero absolute route needs

```text
R_E,1(T) =
  sum_(T<|gamma|<=2T, rho simple) |L'(E,1+i gamma)|^(-1)
  = o(T^2).
```

For fixed `c>0`,

```text
F_E(T,c) = {simple zeros in the shell separated from all other zeros
            by at least c/log T},
B_E(T,c) = {simple zeros in the shell not in F_E(T,c)}.
```

No simple-zero assumption is hidden: multiple zeros are outside `R_E,1(T)` and
must be handled separately by `H1-MultipleZeroDisposition(E,W,r)` or retained
as an explicit profile.  A retained-profile theorem has the different
conclusion

```text
c_E,W(e^u) = Q_E,W(u) + P_mult,box(u) + o(u^r),
```

not the central-only conclusion.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT01_SECTION5_GL2_CONDUCTOR_AUDIT_2026-05-11.md`: Section 5 audit is `NO_GO`; `log C_E(t)=2logT+O_E(1)` changes `2k` to `4k` and forces `a(2d-1)>2` at `k=1/2`.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT02_BFMT_EPSILON_DELTA_MARGIN_REFEREE_2026-05-11.md`: margin referee is `NO_GO`; fixed polylogs and `T^o(1)` losses are harmless, but the doubled conductor coefficient creates a fixed exponent gap.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT03_SEPARATED_EC_BFMT_FINAL_THEOREM_2026-05-11.md`: final separated EC-BFMT theorem is `NO_GO`; the failed step is BFMT Lemma 2.4 into Section 5 equation `(5.13)`.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT04_MINMOD_SOURCE_AND_PROOF_HUNT_2026-05-11.md`: `MinMod(E,c,A,h)` is `NO_GO`; standard minimum-modulus and selected-height tools do not prove `m_rho >= h(T)/T`.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT05_PRODUCT_LAYER_INVERSE_DISTANCE_2026-05-11.md`: `ProductLayer` is a `RIGOROUS_REDUCTION` from rooted inverse-product correlation, not a sourced theorem from ordinary pair or fixed-test correlations.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT06_DIRECT_COMPLEMENT_TAIL_2026-05-11.md`: direct complement tail is a `RIGOROUS_REDUCTION`; no fixed-EC reciprocal derivative tail, negative moment, WMC analogue, or mollifier majorant is sourced.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT07_MULTIPLE_ZERO_REMOVAL_OR_RETAINED_PROFILE_2026-05-11.md`: replace `H1-MultipleEffectiveDegree-BFMT` by `H1-MultipleZeroDisposition(E,W,r)`; BFMT does not control multiple zeros.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md`: Wave 4 conditional H1 stack named Section 5 GL2 conductor audit as the first new blocker, then bad-set complement and multiple-zero control.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT06_H1_FINITE_BOX_ASSEMBLY_REFEREE_2026-05-11.md`: finite-box assembly requires separated EC-BFMT, bad-set complement, and multiple-zero control before central-only H1 follows.

## Dependency Graph

Current Wave 5 graph:

```text
Fixed-newform RH/GRH and explicit-formula package
  -> GL2-ShiftDerivativeComparison(E,c)                         [local input]
  -> GL2-BFMT-PrimePolynomialLowerBound(E), conductor-normalized [local input]

conductor-normalized lower bound
  + derivative-shift comparison
  + zero-sampling coefficient transcription
  -> SeparatedEC-BFMT(E,c,k=1/2)                                 [NO_GO]

SeparatedEC-BFMT(E,c,k=1/2)
  + EC-BFMT-BadSetBudget(E,c)
  -> R_E,1(T)=o(T^2)                                             [blocked]

MinMod(E,c,A,h) + ProductLayer(E,c,A,h)
  -> EC-BFMT-BadSetBudget(E,c)                                   [conditional only]

RootedInvProdCorr(E,A)
  -> ProductLayer(E,c,A,h)                                       [rigorous reduction]

DirectComplementTail(E,c)
  -> EC-BFMT-BadSetBudget(E,c)                                   [rigorous reduction]

Finite-box contour package
  + no-silent-right-half-residue rule
  + R_E,1(T)=o(T^2)
  + H1-MultipleZeroDisposition(E,W,r)
  -> c_E,W(e^u)=Q_E,W(u)+o(u^r)                                  [not reached]
```

The first broken arrow is

```text
conductor-normalized lower bound
+ derivative-shift comparison
+ zero-sampling transcription
-> SeparatedEC-BFMT(E,c,k=1/2).
```

## Referee Report

### Agents 01-03: separated simple zeros

Accepted as a negative referee result.  The three packets agree on the same
failure.

The derivative-shift comparison costs only

```text
exp(O_(E,c)(log T/log log T)) = T^o(1).
```

The coefficient-side zero-sampling and EC coefficient insertions cost fixed
polylogarithmic or `T^o(1)` factors in the audited supports.

Those losses are not first.  The conductor main term is first.  In BFMT block
notation,

```text
T^(beta_j) = exp(2 pi Delta_j),
alpha = 1/log T,
2 pi alpha Delta_j = beta_j.
```

The zeta term contributes

```text
beta_j^(-1) log(1-exp(-beta_j)).
```

The fixed-curve EC term contributes

```text
(2+o(1)) beta_j^(-1) log(1-exp(-beta_j)).
```

After inversion and BFMT power `2k`, Section 5 carries `4k` where the zeta
proof carries `2k`.  At `k=1/2`, the small-block sign changes from needing to
beat `1` to needing to beat `2`.  The printed support/truncation regime does
not provide that room.  Therefore `SeparatedEC-BFMT(E,c,k=1/2)` is not an
available input to the finite-box theorem.

### Agent 04: minimum modulus

Accepted as `NO_GO`.

The bad-set cluster route needs

```text
m_rho = min_(|s-rho|=R_rho) |L(E,s)| >= h(T)/T,
h(T)->infinity,
0<R_rho<=A/log T.
```

Agent04 found no source-closed proof.  Selected-height lower bounds are not
zero-centered microscopic-circle bounds.  Standard Cartan/Jensen/local
avoidance gives scales such as

```text
exp(-C_E,A log T log log T)
```

or at best `T^(-C_E,A)` under stronger local-count upgrades, not `h(T)/T`.

Thus the bad-set route is not closed even if the separated branch were repaired.

### Agent 05: product layer

Accepted as a rigorous reduction.

Agent05 sharpens the geometric half of the bad-set condition to the rooted
singular statistic

```text
J_m(T;A) =
  sum_(rho0 in S_E(T))
  sum_(rho1,...,rhom distinct)
    prod_(j=1)^m (log T |rhoj-rho0|)^(-1),
```

with the inner sum restricted to `0<|rhoj-rho0|<=A/log T`.  A summable bound
for these `J_m` gives `ProductLayer(E,c,A,h)`.

This does not prove `MinMod`.  Ordinary close-pair counts or fixed-test
`n`-level correlations do not control the singular inverse-product weight
near coordinate hyperplanes.

### Agent 06: direct complement tail

Accepted as a rigorous reduction.

The direct bypass of `MinMod + ProductLayer` is exactly

```text
sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2),
```

equivalently the integrated reciprocal tail

```text
int_1^infinity
  #{rho in B_E(T,c): |L'(E,rho)|^(-1)>V} dV
  = o(T^2).
```

It would follow from a fixed-EC bad-set negative moment, weighted reciprocal
square/WMC analogue, or genuine pointwise mollifier majorant.  No listed source
supplies any of these.  This is a downstream blocker, not a repair to Agents
01-03.

### Agent 07: multiple zeros

Accepted as theorem packaging and required disposition.

Do not use

```text
H1-MultipleEffectiveDegree-BFMT(E,W,r).
```

Use

```text
H1-MultipleZeroDisposition(E,W,r).
```

Every crossed offcentral multiple-zero residue must be in exactly one declared
mode:

```text
absent by named offcentral simplicity;
kernel-killed to full pole order;
retained in an explicit multiple-zero profile;
or central-negligible by effective-degree and aggregate control.
```

BFMT controls no multiple zeros.  The finite-box central-only theorem cannot
assume them away.  If a profile is retained, the theorem conclusion changes by
including `P_mult,box(u)`.

## First Blocker or Conditional Stack

First blocker:

```text
ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2).
```

Explicit failed implication:

```text
GL2-ShiftDerivativeComparison(E,c)
+ GL2-BFMT-PrimePolynomialLowerBound(E), conductor-normalized
+ ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2)
does not imply
SeparatedEC-BFMT(E,c,k=1/2)
```

from the current Wave 5 inputs.

The precise failed step is BFMT Lemma 2.4 entering Section 5 equation `(5.13)`.
The substitution

```text
log T -> log C_E(t) = 2 log T + O_E(1)
```

forces

```text
2k -> 4k.
```

For `k=1/2`, the small-block decay condition becomes

```text
a(2d-1) > 2,
```

while the BFMT support regime does not make that inequality legal.  The
resulting ledger is of fixed-power-loss type, not a polylogarithmic or `T^o(1)`
loss.  Hence the desired separated bound `T^(1+delta)` is unavailable.

Only the following external conditional stack would give central-only H1, and
it is not proved by Agents 01-07:

```text
C0. r=ord_(s=1)L(E,s)>=1.
C1. Fixed-kernel Mellin/Perron identity and central normalization.
C2. Legal exponential finite-box heights and contour tails.
C3. No silent right-half residues.
C4. Fixed-newform RH/GRH and explicit-formula package.
C5. A new degree-2 separated negative-moment theorem replacing the failed
    ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2).
C6. Bad-set complement:
    DirectComplementTail(E,c), or
    MinMod(E,c,A,h)+ProductLayer(E,c,A,h), or
    a stronger fixed-EC reciprocal-tail/negative-moment/WMC theorem.
C7. H1-MultipleZeroDisposition(E,W,r), with central-only smallness or explicit
    retained profile in the conclusion.
```

Since `C5` is exactly the first no-go, this packet does not promote the
conditional theorem as a Wave 5 closure result.

## Dependency Impact

- Do not cite Wave 5 as proving `SeparatedEC-BFMT(E,c,k=1/2)`.
- Do not cite Wave 5 as proving `R_E,1(T)=o(T^2)`.
- Do not cite Wave 5 as proving central-only finite-box H1.
- Do not hide an offcentral simplicity assumption; use
  `H1-MultipleZeroDisposition(E,W,r)` or retain the multiple-zero profile.
- The next analytic rescue target is a genuinely degree-2 separated
  negative-moment theorem at `alpha=1/log T`, or a new Section 5 argument that
  offsets the doubled conductor coefficient while preserving BFMT support.
- If that separated blocker is repaired, the next independent blockers are the
  bad-set complement (`MinMod` or direct reciprocal tail) and the declared
  multiple-zero disposition.
