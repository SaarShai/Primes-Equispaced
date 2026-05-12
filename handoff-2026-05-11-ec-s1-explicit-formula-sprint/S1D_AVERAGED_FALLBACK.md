---
schema_version: 1
title: "S1-D averaged fallback theorem for persistent zero oscillations"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.66
do_not_promote: true
sources:
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
tags: [ec-ndc, s1, h2, averaged, explicit-formula, do-not-promote]
---

# S1-D Averaged Fallback

Status: `RIGOROUS_REDUCTION`

do-not-promote: this is a fallback theorem shape. It does not promote
pointwise H2, pointwise T1, or the original EC smoothing claim.

No external citation is used here.

## Verdict

If the smoothed prime-linear term

```text
S_1,W(K) = sum_p W(p/K) a_p/p
```

has persistent noncentral-zero oscillations pointwise, the claim-safe fallback
is a logarithmic average in `u = log K`. This can recover the finite part of
`S_1,W` and the geometric/log finite part of H2. It is still too weak for the
original EC smoothing goal unless H1 and the final `c_E,W(K)P_E,W(K)` theorem
are also stated in the same averaged mode.

The obstruction is simple: averaging `log P_E,W` kills additive Fourier terms,
but the original proxy uses `P_E,W` itself. If
`log P_E,W(e^u)` contains a persistent `Z_P(u)`, then `P_E,W(e^u)` contains
`exp(Z_P(u))`; its average is not determined by the average of `Z_P`.

## Averaging Convention

For a function `F(K)`, define the dyadic log-K average

```text
A_U F = 1/U * integral_U^(2U) F(exp u) du.
```

All limits below are as `U -> infinity`, with fixed elliptic curve `E/Q`, fixed
admissible kernel `W`, and analytic rank

```text
r = ord_{s=1} L(E,s).
```

The H2 local-factor convention is the Agent 3/H2E convention:

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E,W(K).
```

Let `kappa_sym` be the coefficient defined by

```text
S_sym,W(K) = -kappa_sym log log K + finite part + error.
```

Then the central coefficient required for the S1 term is

```text
A_1 = 1/2 + kappa_sym/2 - r.
```

## S1 Averaged Theorem

Assume the smoothed S1 explicit formula has the oscillatory form

```text
S_1,W(e^u)
 = A_1 log u + C_1,E,W + Z_1,E,W(u) + E_1(u),
```

where

```text
Z_1,E,W(u) = sum_(gamma in Gamma_E) c_gamma e^(i gamma u)
```

in a truncated or mean-square sense, and `Gamma_E` is the noncentral zero
frequency set. The central zero frequency `gamma = 0` is not included; its
contribution is already the displayed `A_1 log u` and constant term.

Sufficient averaging hypotheses:

1. No zero-frequency leakage: every frequency in `Gamma_E` has `gamma != 0`.
2. The zero series can be averaged termwise, or else has a mean-square tail
   bound strong enough to imply `A_U Z_1,E,W = o(1)`.
3. The pointwise error is log-average small: `A_U E_1 = o(1)`.

A concrete rate version is:

```text
E_1(u) = O(u^(-eta_1))
sum_(gamma in Gamma_E) |c_gamma|/|gamma| < infinity.
```

Then

```text
A_U (S_1,W - A_1 log log K)
 = C_1,E,W + O(U^(-min(eta_1,1))).
```

More generally, for a truncation height `Y = Y(U)`,

```text
error_S1(U)
 <= A_U |E_1|
    + 2/U * sum_(0 < |gamma| <= Y) |c_gamma|/|gamma|
    + A_U |Z_1 - Z_1,<=Y|.
```

This tends to zero whenever the right side tends to zero. The same formula
also shows the small-frequency risk: if noncentral frequencies with
`|gamma| <= 1/U` carry non-negligible mass, the dyadic average does not kill
them at that scale.

## Averaged H2 From Averaged S1

Assume, in the same log-average sense,

```text
A_U (S_sym,W + kappa_sym log log K)
 = C_sym,E,W + O(error_sym(U)),

A_U (M_good,W - log log K)
 = M_good,E,W + O(error_M(U)),

A_U R_ge3,W
 = C_ge3,E,W + O(error_ge3(U)),
```

with `B_bad,E,W` fixed by the finite bad-prime convention. Combine these with
the averaged S1 theorem. Then

```text
A_U (log P_E,W + r log log K)
 = B_E,W + O(error_H2(U)),
```

where

```text
B_E,W
 = C_1,E,W
   + (1/2) C_sym,E,W
   - (1/2) M_good,E,W
   + C_ge3,E,W
   + B_bad,E,W,

error_H2(U)
 = error_S1(U)
   + (1/2) error_sym(U)
   + (1/2) error_M(U)
   + error_ge3(U).
```

Equivalently, if the full log-product has an oscillatory expansion

```text
log P_E,W(e^u)
 = -r log u + B_E,W + Z_P,E,W(u) + E_P(u),
```

and `A_U Z_P,E,W = o(1)`, `A_U E_P = o(1)`, then

```text
A_U (log P_E,W + r log log K)
 = B_E,W + o(1).
```

This is H2-avg. It is not H2-limit.

## Frequency Conditions

Pure Fourier terms are killed by the log average:

```text
|A_U e^(i gamma u)| <= 2/(U |gamma|),   gamma != 0.
```

Thus finite zero sums average out at rate `O(1/U)`. Infinite zero sums average
out if one can pass the average through the sum or control the tail. Usable
conditions include either:

```text
sum_gamma |c_gamma|/|gamma| < infinity,
```

or a truncation/mean-square condition of the form

```text
2/U * sum_(0 < |gamma| <= Y(U)) |c_gamma|/|gamma|
  + A_U |sum_(|gamma| > Y(U)) c_gamma e^(i gamma u)|
  = o(1).
```

The central frequency must be separated first. Any `gamma = 0` term is not
averaged away; it is part of the logarithmic main term or the finite constant.

Polynomial-weighted noncentral terms are dangerous. A term

```text
u^j e^(i gamma u),   j >= 1,
```

does not vanish under the unnormalized dyadic average after division only by
the interval length. Such terms must be absent, lower-order after the same
normalization used in the theorem, or explicitly included in the averaged
constant/correlation term. This matters most for H1, where multiple reciprocal
zeros can create powers of `log K`.

## How H1 Must Change

The pointwise T1 composition cannot use H2-avg. The final theorem mode must
match the weakest input.

### Log/geometric averaged route

If positive-rank H1 is strengthened to the log-average statement

```text
A_U (log c_E,W - r log log K)
 = -log L^(r)(E,1) + o(1),
```

with a fixed branch/sign convention making the logarithm meaningful, then H2-avg
gives only a geometric-average conclusion:

```text
A_U log(c_E,W P_E,W)
 = B_E,W - log L^(r)(E,1) + o(1).
```

With the T1 `H3` tail this becomes

```text
A_U log X_E,W
 = log zeta(2)
   + B_E,W
   - log L^(r)(E,1)
   - r log L(E,2)
   + o(1).
```

This is meaningful as a finite-part/geometric-mean theorem. It does not prove
that the values `X_E,W(K)` stabilize pointwise or have small ordinary CV.

### Arithmetic averaged route

To average the actual proxy values, one needs a direct joint statement:

```text
A_U (c_E,W P_E,W)
 = C_E,W^arith + o(1).
```

If

```text
P_E,W(e^u)
 = exp(B_E,W) u^(-r) exp(Z_P(u)) (1 + o(1))
```

with persistent `Z_P`, then for simple positive-rank H1 residues below the
central scale one expects at best

```text
C_E,W^arith
 = exp(B_E,W)/L^(r)(E,1) * Mean(exp(Z_P))
```

plus any surviving H1/H2 zero-frequency correlations. In rank zero, H1
offcentral residues are already constant-scale, so the correlation terms are
load-bearing:

```text
Mean((1/L(E,1) + Z_c(u)) exp(Z_P(u))).
```

The log-averaged H2 theorem does not determine these arithmetic constants.
They require an averaged H1 theorem for the same window and a joint
zero-frequency/correlation analysis.

## Meaning For EC Smoothing

Meaningful:

- claim-safe fallback if S1 pointwise has persistent zero oscillations;
- isolates the finite parts `C_1,E,W` and `B_E,W` without pretending the
  oscillations are lower order;
- gives a possible theorem for logarithmic/geometric averages;
- provides a diagnostic target for zero-frequency numerical tests.

Too weak for the original goal:

- does not imply pointwise H2;
- does not close T1 as written;
- does not justify ordinary stabilization or small CV of `X_E,W(K)`;
- does not preserve the original fixed-curve constant unless
  `Mean(exp(Z_P)) = 1` and H1/H2 correlations vanish, which is an extra
  theorem, not a consequence of log averaging;
- does not explain cross-curve universality.

Therefore the fallback is mathematically meaningful only after the EC smoothing
claim is explicitly weakened to a log-K averaged or geometric-mean statement.
For the original pointwise/arithmetic proxy goal, it is too weak.

## Do Not Promote

- Do not cite this as pointwise H2.
- Do not use this to close pointwise T1.
- Do not replace analytic rank `ord_{s=1}L(E,s)` by script/algebraic rank
  without a separate rank-equality input.
- Do not omit the symmetric-square/quadratic term from H2 bookkeeping.
- Do not infer arithmetic averages of `P_E,W` from averages of `log P_E,W`.
- Do not infer small CV or pointwise stabilization of `X_E,W(K)`.
- Do not claim cross-curve universality.
- Do not use external source claims unless they follow the sprint source
  protocol.
