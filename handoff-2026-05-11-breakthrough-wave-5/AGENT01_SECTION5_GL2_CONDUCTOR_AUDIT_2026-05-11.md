---
title: "AGENT01 Section 5 GL2 Conductor Audit"
date: 2026-05-11
type: theorem-audit
tier: working
status: NO_GO
confidence: 0.87
tags: [breakthrough-wave-5, h1, gl2, bfmt, conductor, negative-derivative-moment, section-5]
---

## Verdict

NO_GO.

The separated BFMT Section 5 proof does not survive Wave 4 Agent01's
conductor-normalized GL2 lower bound at `k=1/2`.

The obstruction is not prime powers, bad primes, zero-sampling, or the
derivative-shift comparison.  It is the main conductor/gamma term.  Replacing
BFMT's zeta `log T` archimedean factor by

```text
log C_E(t) = 2 log T + O_E(1)
```

doubles the small-block penalty in Lemma 2.4 and then in Section 5 equation
`(5.13)`.  The BFMT sign condition that makes the small-`Delta_j` part decay is
lost.

Thus the audit does not prove

```text
sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  <<_(E,c,delta) T^(1+delta).
```

## Theorem Target

Target under audit:

```text
SeparatedEC-BFMT(E,c,k=1/2):
  sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
    <<_(E,c,delta) T^(1+delta)
```

where

```text
F_E(T,c) = {gamma in (T,2T]:
  L(E,1+i gamma)=0 is simple and
  |gamma-gamma'| >= c/log T for every other zero ordinate gamma'}.
```

BFMT's notation uses `|zeta'(rho)|^(-2k)`, so the reciprocal first derivative
moment corresponds to `k=1/2`.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md`: names `Section5-GL2-ConductorAudit(E,k=1/2)` as the next task and records `C_E(t) asymp_E T^2`.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md`: supplies the corrected GL2 lower bound with
  `A_E(t;alpha,Delta) = [log C_E(t)+O_E(1)]/(2 pi Delta) log(1-exp(-2 pi alpha Delta)) + O_E(1)`.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md`: supplies the separated zero derivative-shift loss
  `exp(O_(E,c)(log T/log log T)) = T^o(1)`.
- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`: previous transcription treated conductor/gamma as absorbable polylog; this audit rejects that point.
- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md`: coefficient-side zero-sampling losses are fixed polylog and remain harmless.
- `/tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt`: BFMT Lemma 2.3, Lemma 2.4, and Section 5 equations `(5.9)`, `(5.12)`, `(5.13)`, `(5.14)-(5.17)`.
- `/tmp/farey-homogeneous-bfmt-20260511/bui_florea_2302_07226.txt`: Bui-Florea Lemma 2.1 displays the same Carneiro-Chandee lower-bound term and the generalized `Delta alpha` bookkeeping.

## Section 5 Audit

Use BFMT's block convention

```text
T^(beta_j) = exp(2 pi Delta_j),
alpha = 1/log T.
```

Then

```text
2 pi alpha Delta_j = beta_j.
```

In the zeta BFMT lower bound, the archimedean main term is

```text
A_zeta(j) = (log T)/(2 pi Delta_j) log(1-exp(-beta_j))
          = beta_j^(-1) log(1-exp(-beta_j)).
```

Agent01's fixed-EC GL2 lower bound gives instead

```text
A_E(j) = (log C_E(t)+O_E(1))/(2 pi Delta_j) log(1-exp(-beta_j)) + O_E(1)
       = (2+o(1)) beta_j^(-1) log(1-exp(-beta_j)).
```

After inversion and raising to BFMT power `2k`, this changes the Section 5
conductor factor from

```text
exp((2k/beta_j) log(1/(1-exp(-beta_j))))
```

to

```text
exp(((4k+o(1))/beta_j) log(1/(1-exp(-beta_j)))).
```

Equivalently, in the small-block range `beta_j -> 0`,

```text
(2k/beta_j) log(1/beta_j)
```

is replaced by

```text
(4k/beta_j) log(1/beta_j).
```

This is exactly the coefficient that BFMT carries into `(5.13)`.  The zeta
small-`Delta_j` exponent has the load-bearing sign term

```text
(log beta_j)/beta_j * (a(2d-1) - 2k).
```

With the GL2 conductor-normalized term it becomes

```text
(log beta_j)/beta_j * (a(2d-1) - 4k)
```

up to lower-order `T^o(1)` factors.

At `k=1/2`, BFMT needs the zeta inequality behind line `(5.14)`:

```text
2k - a(2d-1) < 0
```

after choosing the admissible Section 5 parameters.  The GL2 rerun needs the
stronger condition

```text
4k - a(2d-1) < 0,
```

i.e.

```text
a(2d-1) > 2.
```

That condition is not available in the printed BFMT Section 5 parameter
regime.  The support constraints used for Propositions 2.5, 2.6, and 2.7 keep
the same length budget

```text
beta_0 s_0 <= 1 - loglogT/logT,
sum_(h<=j) ell_h beta_h + s_(j+1) beta_(j+1)
  <= 1 - loglogT/logT,
sum_(h<=K) ell_h beta_h <= 1 - loglogT/logT.
```

They do not provide enough room to double the archimedean coefficient and still
retain the negative small-block exponent used in `(5.13)-(5.14)`.

## Parameter Bookkeeping

The non-harmless factor can be seen already at the first small block.  With

```text
beta_0 asymp loglogT/logT,
```

the extra GL2 conductor degree contributes, for `k=1/2`,

```text
exp((1+o(1)) beta_0^(-1) log(1/beta_0))
  = exp((1+o(1)) (logT/loglogT)(loglogT-logloglogT))
  = T^(1-o(1)).
```

This is not a fixed polylogarithm and not `T^o(1)`.

The other Wave 4 and homogeneous-transcription losses remain absorbable:

```text
prime powers and bad primes:        exp(O_E(loglogT)) = (logT)^O_E(1),
zero-sampling substitution:         (logT)^C,
lambda_E coefficient insertion:     T^o(1) or fixed polylog in the audited supports,
derivative-shift comparison:        exp(O_(E,c)(logT/loglogT)) = T^o(1).
```

None of these changes the obstruction.  The break occurs before those losses
matter.

## Closure or Obstruction

Obstruction:

```text
BFMT Lemma 2.4 -> Section 5 equation (5.13)
```

with the substitution

```text
2k  ->  4k
```

in the conductor/gamma contribution forced by

```text
log C_E(t) = 2 log T + O_E(1).
```

The exact failed step is the zeta small-block decay used to reach BFMT `(5.14)`
and then `(5.16)`.  Under the GL2 conductor-normalized lower bound, the
corresponding exponent is positive at `k=1/2`; the proof is pushed into the
large-shift/high-archimedean branch.  The BFMT-shaped output is then of
`T^(3/2+o(1))` type, not `T^(1+delta)`.

Therefore:

```text
SeparatedEC-BFMT(E,c,k=1/2)
```

is not closed by Wave 4 Agent01 + Agent02 + zero-sampling substitution.

## Dependency Impact

Do not promote the separated reciprocal-derivative theorem.

Still valid as local inputs:

```text
GL2-BFMT-PrimePolynomialLowerBound(E) in conductor-normalized form,
GL2-ShiftDerivativeComparison(E,c),
ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2).
```

Invalid dependency claim:

```text
conductor/gamma terms only cost a fixed power of log T in Section 5.
```

Required replacement:

```text
Degree-2 shifted negative-moment theorem at alpha=1/logT strong enough to
recover T^(1+delta), or a new GL2-specific Section 5 argument that cancels or
beats the extra conductor degree.
```

Independent blockers remain independent:

```text
EC-BFMT-BadSetBudget(E,c),
multiple-zero effective-degree control,
finite-box H1 contour/right-residue assumptions.
```
