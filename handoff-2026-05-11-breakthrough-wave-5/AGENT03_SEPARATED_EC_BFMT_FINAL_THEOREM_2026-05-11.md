---
title: "AGENT03 Separated EC BFMT Final Theorem"
date: 2026-05-11
type: theorem-packet
tier: final
status: NO_GO
confidence: 0.88
tags: [breakthrough-wave-5, h1, elliptic-curve, gl2, bfmt, separated-zeros, conductor, no-go]
---

## Verdict

NO_GO.

The separated-zero BFMT assembly for a fixed elliptic curve does not prove

```text
SeparatedEC-BFMT(E,c,k=1/2):
  sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
    <<_(E,c,delta) T^(1+delta).
```

The shift-derivative comparison is available.  The zero-sampling replacement is
available on the coefficient side.  The GL2 log lower bound is available only
in conductor-normalized form.  That last point is fatal for the printed BFMT
Section 5 ledger at `k=1/2`.

The exact break is:

```text
BFMT Lemma 2.4 -> Section 5 equation (5.13):
  2k is replaced by 4k
```

because the fixed-curve GL2 analytic conductor satisfies

```text
log C_E(t) = 2 log T + O_E(1).
```

At `k=1/2`, the small-block sign condition becomes

```text
a(2d-1) > 2,
```

or, in Agent02's large-branch normalization,

```text
a(2d-1)/r > 2.
```

This is not available under BFMT's support/truncation regime.  Therefore the
target theorem must not be promoted.

## Theorem Target

Let

```text
L_E^*(s) = L(E,s+1/2),
rho = 1/2+i gamma,
alpha = 1/log T.
```

Define the separated simple-zero set

```text
F_E(T,c) = {gamma in (T,2T]:
  L(E,1+i gamma)=0 is simple and
  |gamma-gamma'| >= c/log T for every other zero ordinate gamma'}.
```

The intended BFMT-separated target was:

```text
For every fixed E, c>0, and delta>0,
sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  <<_(E,c,delta) T^(1+delta).
```

This packet rejects that target from the currently assembled Wave 4/Wave 5
inputs.  It does not decide the truth of the target by some other method.

## Source Anchors

Required anchors:

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT01_SECTION5_GL2_CONDUCTOR_AUDIT_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`

Additional Wave 5 referee anchor:

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT02_BFMT_EPSILON_DELTA_MARGIN_REFEREE_2026-05-11.md`

## Assembly Attempt

The attempted assembly has four inputs.

1. Shift from derivative to nearby value.

Agent02 Wave 4 proves, conditional on fixed-newform RH and the standard
Hadamard/Kirila comparison, that for `gamma in F_E(T,c)`,

```text
|L'(E,1+i gamma)|^(-1)
  <= exp(O_(E,c)(log T/log log T))
     |L(E,1+1/log T+i gamma)|^(-1).
```

This loss is `T^o(1)` and is harmless for a final `T^delta` margin.

2. Lower-bound the shifted value by a prime polynomial.

Agent01 Wave 4 proves the GL2 analogue of the BFMT log lower bound, but only
with the conductor-normalized archimedean main term

```text
A_E(t;alpha,Delta)
 = [log C_E(t)+O_E(1)]/(2 pi Delta)
     log(1-exp(-2 pi alpha Delta)) + O_E(1),

C_E(t) asymp_E T^2.
```

Prime squares, higher prime powers, and bad primes cost only `O_E(log log T)`.
Those are not the obstruction.

3. Replace BFMT's zeta zero DPMV by homogeneous zero-sampling.

The zero-sampling audit closes BFMT Propositions 2.5, 2.6, and 2.7 with only a
fixed polylogarithmic loss.  EC coefficient insertions are controlled by
Rankin-Selberg/Deligne-type divisor losses in the audited supports.  These
losses remain `T^o(1)` or fixed powers of `log T`.

4. Run BFMT Section 5.

All non-conductor losses can be reserved inside an internal epsilon/delta
budget.  The conductor-normalized main term cannot.  With BFMT's block
normalization

```text
T^(beta_j) = exp(2 pi Delta_j),
alpha = 1/log T,
2 pi alpha Delta_j = beta_j,
```

the zeta archimedean contribution is

```text
A_zeta(j)
 = beta_j^(-1) log(1-exp(-beta_j)).
```

The fixed-curve GL2 contribution is

```text
A_E(j)
 = (2+o(1)) beta_j^(-1) log(1-exp(-beta_j)).
```

After inversion and raising to BFMT power `2k`, this changes the Section 5
linear conductor load from

```text
(2k/beta_j) log(1/(1-exp(-beta_j)))
```

to

```text
((4k+o(1))/beta_j) log(1/(1-exp(-beta_j))).
```

For small `beta_j`, the extra degree contributes

```text
(2k/beta_j) log(1/beta_j),
```

which is a fixed-power obstruction in the first small block, not a
polylogarithmic loss.

## Exact Obstruction or Closure

Closed local inputs:

```text
GL2-ShiftDerivativeComparison(E,c)
  closed conditionally under fixed-newform RH.

GL2-BFMT-PrimePolynomialLowerBound(E)
  closed conditionally only in conductor-normalized form.

ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2)
  closed as a rigorous coefficient-side reduction with fixed polylog loss.
```

Not closed:

```text
ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2).
```

Precise missing lemma:

```text
There exists a legal BFMT Section 5 parameter system satisfying the printed
support constraints for Propositions 2.5, 2.6, and 2.7, while also making the
degree-2 conductor-normalized small-block exponent negative at k=1/2.
```

Equivalently, in Agent01's small-block notation, BFMT's decay term changes
from

```text
(log beta_j)/beta_j * (a(2d-1) - 2k)
```

to

```text
(log beta_j)/beta_j * (a(2d-1) - 4k).
```

At `k=1/2`, decay would require

```text
a(2d-1) > 2.
```

That inequality is outside the BFMT support regime.  Agent02's Wave 5 margin
referee confirms the same fixed gap in the second-branch bookkeeping: the
printed parameters force `a(2d-1)/r < 1`, while the GL2 conductor-normalized
term requires beating `4k=2`.

Thus the failed step is not a soft loss in zero-sampling, bad primes, prime
powers, or derivative shifting.  It is the main archimedean/conductor term in
BFMT Lemma 2.4 as it enters Section 5 equation `(5.13)`.

## Weakest Replacement

The strongest honest replacement from the current packets is a rigorous
reduction plus a no-go boundary:

```text
SeparatedEC-BFMT(E,c,k=1/2)
follows from the closed local inputs above plus the missing lemma
ConductorNormalized-BFMT-Section5-SignLemma(E,k=1/2).
```

Without that new lemma, the available closed statement is only the separated
shift reduction:

```text
sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
 <= exp(O_(E,c)(log T/log log T))
    sum_(gamma in F_E(T,c)) |L(E,1+1/log T+i gamma)|^(-1),
```

conditional on fixed-newform RH.  The BFMT coefficient machinery can then be
applied only up to the conductor-normalized Section 5 obstruction.

If the printed BFMT Section 5 inequalities are retained with the GL2 conductor
term inserted literally, the resulting ledger is of `T^(3/2+o(1))` type rather
than `T^(1+delta)` type.  This is not a replacement for the H1 separated
reciprocal-derivative budget.

## Dependency Impact

Do not promote:

```text
SeparatedEC-BFMT(E,c,k=1/2)
H1 rank-one reciprocal-derivative theorem
R_E,1(T)=o(T^2)
```

Retain as valid dependencies:

```text
GL2-ShiftDerivativeComparison(E,c)
GL2-BFMT-PrimePolynomialLowerBound(E) in conductor-normalized form
ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2)
```

Invalidate this dependency claim:

```text
The GL2 conductor/gamma term costs only a fixed power of log T in BFMT
Section 5.
```

Next possible rescue target:

```text
Prove a genuinely degree-2 Section 5 argument that offsets the doubled
archimedean coefficient while preserving the BFMT support constraints, or
prove a different shifted negative-moment theorem for fixed GL2 newforms at
alpha=1/log T strong enough to recover T^(1+delta).
```
