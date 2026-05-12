---
schema_version: 1
title: "Agent 07 H1 Finite-Box DPMV Integration"
date: 2026-05-11
agent: "Top-10 Challenge Wave Agent 07"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.89
dependencies:
  - HANDOFF.md
  - handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md
  - handoff-2026-05-11-breakthrough-wave-3/AGENT07_H1_FINITE_BOX_THEOREM_SECTION_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/AGENT01_BFMT_P25_COEFFICIENT_AUDIT_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/AGENT02_BFMT_P26_P27_MIXED_TERMINAL_AUDIT_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/AGENT03_GL2_DPMV_SOURCE_CLOSURE_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/AGENT04_EC_BFMT_BADSET_INVERSEGAP_BUDGET_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/AGENT05_H1_LOCAL_MINMOD_CERTIFICATE_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/AGENT06_H1_ACTUAL_DYADIC_SHELL_PV_2026-05-11.md
  - handoff-2026-05-11-top10-challenge-wave/TOP10_CHALLENGE_WAVE_SYNTHESIS_2026-05-11.md
tags: [top10-challenge-wave, h1, finite-box, dpmv, bfmt, reciprocal-derivative, no-promotion]
---

# Agent 07 H1 Finite-Box DPMV Integration

Status: `RIGOROUS_REDUCTION`.

No theorem is promoted.  The direct Milinovich-Ng substitution for BFMT is
`NO_GO`; the surviving rank-one H1 statement is conditional on a new homogeneous
GL2 BFMT-DPMV input, an independent bad-set reciprocal budget, and the already
named finite-box boundary and multiple-zero hypotheses.

## Decision Tree

```text
H1-FiniteBox-Conditional(E,W,r)
  result: conditional theorem section already packaged
  needs:
    H1 analytic-rank/Perron/kernel/central-polynomial hypotheses
    legal exponential box heights and no silent right-half residues
    simple reciprocal budget R_E,1(T)=o(T^2 (log T)^(r-1))
    multiple-zero effective-degree control

simple reciprocal budget
  separated simple zeros:
    desired source:
      Homogeneous-GL2-BFMT-DPMV(E,k=1/2)
        => sum_{rho in F_E(T,c)} |L'(E,rho)|^(-1)
           <<_{E,c,delta} T^(1+delta)
    killed source:
      Milinovich-Ng Proposition 4.1/4.3 as black-box BFMT replacement
      result: NO_GO at P2.5 and P2.6

  non-separated simple zeros:
    still needs:
      EC-BFMT-BadSetBudget(E,c)
    source result:
      reduced to local cluster minimum modulus
      plus inverse-product-distance layer cake
    no-go:
      count-only pair correlation/local statistics/simplicity

multiple zeros:
  still governed by H1-MultipleEffectiveDegree(E,W,r)
  D_alpha < r is required for central-only pointwise mode
  lower-degree aggregates still need summability/PV/profile control

rank-one conclusion:
  only conditional:
    c_E,W(e^u) = (w_-1/L'(E,1)) u + o(u)
  normalized kernel:
    c_E,W(e^u) = u/L'(E,1) + o(u)
```

## Direct Milinovich-Ng Route Is Killed

The previous compressed target

```text
GL2-LandauGonek-DPMV(E,theta)
```

must not mean "insert Milinovich-Ng Proposition 4.1/4.3 into BFMT."  Top10
Agents 01 and 02 kill that interpretation.

### P2.5 failure

For BFMT Proposition 2.5, the inner coefficient polynomial passes several local
checks against Milinovich-Ng Proposition 4.1:

```text
support can be made acceptable;
conditions (39) and (40) hold for the unscaled inner polynomial;
the GL2 off-diagonal term vanishes on exact Omega(n)=s_0 support;
fixed bad primes are harmless.
```

The failure is homogeneity.  BFMT recovers

```text
P_{0,v}(gamma)^(s_0) = s_0! A_v(1/2+1/logT+i gamma).
```

Applying Milinovich-Ng to `A_v` and then multiplying by `(s_0!)^2` makes the
generic error

```text
T (log T)^(4-2 eta)
```

and the square-root convolution error too large by a fixed power of `T` at
`k=1/2`.  Applying Proposition 4.1 directly to the scaled coefficients is not
available, because the required coefficient hypotheses are not supplied in that
scaled form.  Milinovich-Ng Proposition 4.3 does not rescue P2.5 because BFMT
uses support up to `T^(1-o(1))`, while Proposition 4.3 has the `T^(2/3)`
support wall.

### P2.6 failure

For BFMT Proposition 2.6, the failure is stronger:

```text
Milinovich-Ng condition (40) is false
```

for the mixed coefficients because the terminal `P_{j+1,v}^{s_{j+1}}` factor
contains factorial-size multinomial coefficients.  The first mixed support
also has

```text
theta_mix(0) = 1 - eps/(2(1-eps)) + o(1) > 2/3
```

in the BFMT small-`eps` regime, so Milinovich-Ng Proposition 4.3 is outside its
support range.  Proposition 2.7 is not fatal by itself, but BFMT needs
Proposition 2.6, so the black-box MN route is dead.

## Required Replacement DPMV Source

The surviving DPMV input must be stated as a new theorem, not as a source-closed
citation:

```text
Homogeneous-GL2-BFMT-DPMV(E,k=1/2).
```

Required content:

```text
1. Fixed elliptic curve/newform normalization, with finite ramified primes
   removed or absorbed in fixed constants.

2. Zero-discrete mean-value estimates for every BFMT coefficient family in
   Propositions 2.5, 2.6, and 2.7 at k=1/2.

3. Errors homogeneous in the actual BFMT coefficients after factorial
   expansion, matching the role of BFMT Theorem 3.1 rather than the
   nonhomogeneous Milinovich-Ng Proposition 4.1 errors.

4. Support reaching T^(1-o(1)); a T^(2/3)-only prime-power theorem is
   insufficient for the mixed P2.6 family.

5. GL2 convolution and off-diagonal terms either absent, sign-favorable, or
   absorbable in the exact BFMT T^(1+delta) final bound.
```

If this theorem is proved, the separated simple-zero output allowed in the H1
tree is:

```text
sum_{rho in F_E(T,c)}
  |L'(E,rho)|^(-1)
  <<_{E,c,delta} T^(1+delta)
```

for fixed `delta<1`.  This is enough for the separated part of
`R_E,1(T)=o(T^2(log T)^(r-1))`, and in rank one it is enough for
`o(T^2)`.

If this theorem fails, the BFMT-separated H1 route is dead.  The remaining
routes are genuinely different hypotheses:

```text
H1-ActualDyadicShellPV(E,W,r,H),
H1-LocalMinModCertificate(E) plus bad reciprocal budget,
or a different full reciprocal-derivative tail theorem.
```

Top10 Agent 06 leaves the direct PV route `NO_GO`, and Top10 Agent 05 kills
standard complex-analysis derivations of the local minimum-modulus certificate.

## Bad-Set Budget Still Independent

Even after `Homogeneous-GL2-BFMT-DPMV(E,k=1/2)`, the separated estimate controls
only

```text
F_E(T,c) = {simple zeros rho : dist(rho,Z_E\{rho}) >= c/logT}.
```

The complement still requires:

```text
EC-BFMT-BadSetBudget(E,c):
  sum_{rho notin F_E(T,c), simple}
    |L'(E,rho)|^(-1)
  = o(T^2)
```

for the rank-one theorem.  In general rank `r`, the finite-box simple-budget
slot is

```text
o(T^2 (log T)^(r-1)).
```

The top10 bad-set packet gives the exact remaining sufficient input:

```text
EC-BFMT-ClusterProductBudget(E,c):
  for each clustered simple zero, a zero-centered local minimum-modulus
  certificate plus

  sum_{rho in B_E(T,c)}
    R_rho (2R_rho)^(k_rho-1)/(m_rho D_rho)
  = o(T^2).
```

This implies the rank-one bad-set budget.  Count-only close-pair laws,
pair-correlation, local zero statistics, zero-density, and simplicity
proportions do not imply it.  They do not cap
`|L'(E,rho)|^(-1)`.

## Multiple-Zero Entry Point

BFMT/DPMV controls only simple reciprocal derivatives.  Multiple zeros remain
inside the finite-box theorem as Laurent residues.

For a crossed zero `rho=1+alpha` of multiplicity `m`,

```text
1/L(E,1+z)
  = sum_{j=1}^m b_{rho,-j}(z-alpha)^(-j) + holomorphic,
```

and its finite-box residue has shape

```text
R_rho(u) = e^(alpha u) sum_{ell=0}^{m-1} A_{rho,ell} u^ell.
```

After kernel zeros, Laurent cancellations, and same-exponent netting, define

```text
D_alpha = max{ell : A_{alpha,ell}^{net} != 0}.
```

Pointwise central-only H1 requires:

```text
D_alpha < r
```

for every retained critical-line exponent.  For rank one this means
`D_alpha <= 0`, and the remaining degree-zero aggregate must still be controlled
in the declared mode.  A retained degree-one oscillation is the same size as
the central rank-one term and blocks the pointwise central-only statement.

This hypothesis is independent of the DPMV separated/bad-set split.

## Rank-One Statement Available

The exact rank-one theorem statement allowed by the current hierarchy is:

```text
H1-RankOne-HomogeneousDPMV-BadSet-Conditional(E,W,c).
```

Assume:

```text
1. H1-AnalyticRank(E) with r=1.
2. H1-KernelPoleDecay(W), H1-FixedKernelPerron(E,W,sigma),
   and H1-CentralPolynomialNormalization(E,W,1).
3. H1-LegalExponentialHeights(E,W,sigma,eta,C).
4. H1-NoSilentRightHalfResidues(E,W,sigma,eta).
5. Homogeneous-GL2-BFMT-DPMV(E,k=1/2), giving the separated simple-zero
   reciprocal bound above.
6. EC-BFMT-BadSetBudget(E,c).
7. H1-MultipleEffectiveDegree(E,W,1), including aggregate control for all
   retained lower-degree multiple-zero terms.
```

Then, in the same pointwise finite-box mode,

```text
c_E,W(e^u) = (w_-1/L'(E,1)) u + o(u).
```

For normalized kernels `w_-1=1`,

```text
c_E,W(e^u) = u/L'(E,1) + o(u).
```

This is not an unconditional theorem, not an EC stabilization theorem, and not
an H1/H2 product theorem.  It is a paper-ready conditional H1 finite-box
statement with two major unproved analytic inputs:

```text
Homogeneous-GL2-BFMT-DPMV(E,k=1/2),
EC-BFMT-BadSetBudget(E,c),
```

plus the finite-box boundary and multiple-zero hypotheses already named in the
Wave 3 Agent 07 theorem section.

## No-Promotion Rules

Do not cite this packet as proving any of:

```text
Milinovich-Ng => BFMT-CoefficientDPMV(E,k=1/2);
GL2-LandauGonek alone => reciprocal derivative budget;
separated-zero DPMV => full R_E,1(T) without EC-BFMT-BadSetBudget;
pair correlation/local statistics => bad reciprocal budget;
standard Cartan/Jensen/Borel-Caratheodory/Hadamard => H1 local min modulus;
log-Cesaro/profile/product-average => pointwise H1 finite-box theorem;
simple-zero budget => multiple-zero Laurent control;
rank-zero pointwise stabilization;
H1/H2 product theorem.
```

Analytic rank only.  No BSD rank substitution.  No H2 branch damping is used as
H1 reciprocal-pole damping.  No correspondence or email draft is used.

## Source Notes

This packet introduces no new external citation claim.  It integrates the
source-checked claims already recorded in the required packets:

```text
BFMT arXiv:2310.03949:
  zeta separated negative derivative moments and Theorem 3.1 coefficient
  engine, as audited in top10 Agents 01-03.

Milinovich-Ng arXiv:1306.0854:
  GL2 Landau-Gonek, Proposition 4.1 coefficient-conditional DPMV, and
  Proposition 4.3 T^(2/3)-support high moments, as audited in DPMV
  continuation and top10 Agents 01-03.

Wave 3 Agent 07:
  finite-box H1 conditional theorem section and named boundary/multiple-zero
  hypotheses.

Top10 Agents 04-06:
  bad-set layer-cake reduction, local-minimum-modulus no-go, and actual
  dyadic-shell PV no-go.
```

## Verification Notes

Read scope:

```text
HANDOFF.md
handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-3/AGENT07_H1_FINITE_BOX_THEOREM_SECTION_2026-05-11.md
handoff-2026-05-11-top10-challenge-wave/AGENT01_BFMT_P25_COEFFICIENT_AUDIT_2026-05-11.md
handoff-2026-05-11-top10-challenge-wave/AGENT02_BFMT_P26_P27_MIXED_TERMINAL_AUDIT_2026-05-11.md
handoff-2026-05-11-top10-challenge-wave/AGENT03_GL2_DPMV_SOURCE_CLOSURE_2026-05-11.md
handoff-2026-05-11-top10-challenge-wave/AGENT04_EC_BFMT_BADSET_INVERSEGAP_BUDGET_2026-05-11.md
handoff-2026-05-11-top10-challenge-wave/AGENT05_H1_LOCAL_MINMOD_CERTIFICATE_2026-05-11.md
handoff-2026-05-11-top10-challenge-wave/AGENT06_H1_ACTUAL_DYADIC_SHELL_PV_2026-05-11.md
handoff-2026-05-11-top10-challenge-wave/TOP10_CHALLENGE_WAVE_SYNTHESIS_2026-05-11.md
```

Project-local `./te` and `token-economy.yaml` were absent inside
`primes-equispaced`; `L0_rules.md` and `L1_index.md` were loaded.

Changed file:

```text
primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT07_H1_FINITE_BOX_DPMV_INTEGRATION_2026-05-11.md
```
