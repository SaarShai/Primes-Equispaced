---
title: "AGENT09 H2 Sym2 Composition Final"
date: 2026-05-11
status: CONDITIONAL_THEOREM
tags: [breakthrough-wave-4, h2, sym2, h1, composition, fixed-curve]
---

## Verdict

`CONDITIONAL_THEOREM`.

The H2/Sym2 finite-part side composes cleanly with the current H1 spine only
after the theorem mode is declared. The exact Agent 3 H2 bookkeeping gives the
right `-r log log K` coefficient, with the Sym2 central order canceling out of
the product coefficient. The final fixed-curve pointwise theorem for

```text
c_E,W(e^u) P_E,W(e^u)
```

is conditional on:

```text
H2: log P_E,W(e^u) = -r log u + B_H2(E,W) + o(1),
H1: c_E,W(e^u) = u^r/L^(r)(E,1) + o(u^r),
r = ord_{s=1} L(E,s).
```

If H2 keeps a right-lip/profile term, or H1 keeps reciprocal-zero residues at
central scale, the theorem is not a pointwise finite limit. It is a profile or
product-average theorem with those terms retained.

## Theorem Target

Let `E/Q` be fixed, `W` be the same admissible smoothing kernel on both sides,
`u=log K`, and

```text
r = ord_{s=1} L(E,s).
```

Use the exact Agent 3 local factor convention:

```text
A_p(1) = 1 - a_p/p + 1/p    for good p,
A_p(1) = 1 - a_p/p          for bad p,
P_E,W(K) = product_p A_p(1)^(-W(p/K)).
```

The desired pointwise target is:

```text
c_E,W(e^u) P_E,W(e^u)
 -> exp(B_H2(E,W)) / L^(r)(E,1).
```

This is fixed-curve only. It does not assert any cross-curve universality, BSD
input, script-rank equality, or Theorem B consequence.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md`
  supplies the exact good-prime Sym2 convention, the Sym2 finite-part shape,
  the `kappa_sym` ledger, and the coefficient cancellation in H2.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md`
  supplies the exact H2 decomposition, the named dependencies `D0` through
  `D5`, the conditional pointwise H2 candidate, and the oscillatory/log-average
  fallback.
- `primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md`
  supplies the current H1 spine: H1 is reciprocal-pole calculus, not H2
  logarithmic-branch calculus, and product convergence only needs
  `Z_c(u)+E_c(u)=o(u^r)`.
- `primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT08_H2_S1_RENORMALIZED_LOG_GROWTH_2026-05-11.md`
  blocks unconditional H2 promotion: right branches require full cut-lip
  retention unless absence, smallness, or cancellation is proved.
- `primes-equispaced/L2_facts/farey-current-state.md` fixes the project-level
  warning: use arithmetic normalization and analytic rank carefully; numerical
  W2 evidence is not a theorem input here.

## Composition Audit

Good-prime local algebra:

```text
S1_W(K)     = sum_{p good} W(p/K) a_p/p,
Ssym_W(K)  = sum_{p good} W(p/K) (a_p^2/p - 1)/p,
Mgood_W(K) = sum_{p good} W(p/K)/p.
```

Exact H2 decomposition:

```text
log P_E,W(K)
 = S1_W(K)
   + (1/2) Ssym_W(K)
   - (1/2) Mgood_W(K)
   + Rge3_W(K)
   + Bbad_W(K).
```

Conditional finite parts:

```text
S1_W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C1_E,W + Z1_W(K) + o(1),

Ssym_W(K)
 = -kappa_sym log log K
   + Csym_E,W + Zsym_W(K) + o(1),

Mgood_W(K)
 = log log K + CM_E,W + o(1),

Rge3_W(K) = Cge3_E + o(1),
Bbad_W(K) = Bbad_E + o(1).
```

Coefficient check:

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

Thus:

```text
log P_E,W(K)
 = -r log log K + B_H2(E,W) + Z_H2(K) + o(1),

B_H2(E,W)
 = C1_E,W
   + (1/2) Csym_E,W
   - (1/2) CM_E,W
   + Cge3_E
   + Bbad_E,

Z_H2(K) = Z1_W(K) + (1/2) Zsym_W(K)
```

plus any retained right-lip term from the S1 cut-plane theorem. The
non-profile pointwise H2 theorem requires all retained H2 profile terms to be
`o(1)`.

H1 spine:

```text
c_E,W(e^u) = Q_r(u) + Z_c(u) + E_c(u),
Q_r(u) = u^r/L^(r)(E,1) + lower powers of u.
```

H2 branch damping does not transfer to H1. H1 offcentral zeros are reciprocal
poles; a simple zero contributes `e^(i gamma u) W_hat(i gamma)/L'(rho)`, with
no `1/u` loss. The composition only needs the normalized aggregate:

```text
Z_c(u) + E_c(u) = o(u^r)
```

for pointwise fixed-curve convergence. For `r=0`, bounded oscillation is not
enough; the H1 residue profile must be `o(1)`, retained, or averaged.

## Theorem Modes

### Mode 1: Pointwise Finite Limit

Assume:

```text
log P_E,W(e^u) = -r log u + B_H2(E,W) + o(1),
c_E,W(e^u) = u^r/L^(r)(E,1) + o(u^r).
```

Then:

```text
c_E,W(e^u) P_E,W(e^u)
 -> exp(B_H2(E,W)) / L^(r)(E,1).
```

This mode needs pointwise H2 closure: `Z1_W`, `Zsym_W`, and any S1 right-lip
term are `o(1)` or absent. It also needs the H1 reciprocal-pole aggregate to
be `o(u^r)`.

### Mode 2: Profile Theorem

Assume H2 is only closed after retaining a profile:

```text
log P_E,W(e^u)
 = -r log u + B_H2(E,W) + Phi_H2(u) + o(1),
```

where `Phi_H2` contains the retained S1/Sym2 offcentral or right-lip terms.
Assume H1 is closed as:

```text
c_E,W(e^u) = Q_r(u) + Z_c(u) + E_c(u).
```

Then the honest composed profile is:

```text
exp(-Phi_H2(u)) c_E,W(e^u) P_E,W(e^u)
 = exp(B_H2(E,W)) u^(-r)
   (Q_r(u) + Z_c(u) + E_c(u))
   (1 + o(1)).
```

If `Z_c(u)+E_c(u)=o(u^r)`, this normalized profile has the same limit as Mode
1. If not, the final statement must retain

```text
exp(B_H2(E,W)) u^(-r) Z_c(u)
```

or an equivalent H1 profile. Do not state an unprofiled pointwise limit in this
case.

### Mode 3: Product-Average Theorem

Separate H1 and H2 averages are insufficient. A product-average theorem needs
an explicit joint correlation input. One clean sufficient condition is:

```text
(1/T) int_T^(2T)
  exp(Phi_H2(u)) u^(-r) (Q_r(u) + Z_c(u) + E_c(u)) du
 -> 1/L^(r)(E,1).
```

Together with the H2 profile expansion, this gives:

```text
(1/T) int_T^(2T) c_E,W(e^u) P_E,W(e^u) du
 -> exp(B_H2(E,W)) / L^(r)(E,1).
```

This mode is not implied by a logarithmic average for `log P_E,W` alone. It is
a separate arithmetic/correlation theorem for the product.

## Missing Lemma or Closure

No unconditional promotion. The missing H2 closure for the non-profile
pointwise theorem is:

```text
H2-PointwiseFinitePartClosure(E,W,eta;c).
```

Required content:

```text
log P_E,W(e^u) + r log u -> B_H2(E,W)
```

in the exact Agent 3 local convention, including:

- `S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c)` with no silently dropped
  right branch;
- `RightBranchAbsentOrFullLipCancellation(E,W,eta;c)` or
  `R_S1^+(e^u;E,W,eta,c)=o(1)`;
- `Sym2-ZeroLedger-RegularLog(E,W,eta;c)` in the same good-prime Sym2
  convention;
- ordinary weighted good-prime Mertens finite part;
- absolute convergence of `Rge3_W` and finite bad-prime constants.

For the product theorem there is a separate H1 closure:

```text
H1-ReciprocalPoleAggregate(E,W): Z_c(u)+E_c(u)=o(u^r)
```

or retained-profile/product-average replacement. This H1 closure is not
supplied by H2/Sym2.

## Dependency Impact

- H2/Sym2 bookkeeping is internally coherent and conditionally composes with
  H1.
- The final pointwise `c_E,W(e^u)P_E,W(e^u)` limit is conditional, fixed-curve,
  and analytic-rank based.
- Rank zero remains a separate danger case: H1 bounded residues can survive in
  the product.
- An averaged H2 finite part does not by itself imply an averaged product
  theorem.
- No Theorem B, cross-curve, BSD, or numerical-regression impact is promoted.
