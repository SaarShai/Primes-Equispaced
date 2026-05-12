---
title: "AGENT02 GL2 Shift Derivative Comparison"
date: 2026-05-11
type: theorem-reduction
tier: working
status: CONDITIONAL_THEOREM
confidence: 0.90
tags: [breakthrough-wave-4, h1, gl2, elliptic-curve, bfmt, derivative-shift, separated-zeros]
---

## Verdict

`GL2-ShiftDerivativeComparison(E,c)` is proved as a fixed-newform conditional
theorem, assuming RH for the fixed newform attached to `E`.

The input needed by the BFMT separated branch is available:

```text
|L'(E,1+i gamma)|^(-1)
  <= exp(O_(E,c)(log T/log log T))
     |L(E,1+1/log T+i gamma)|^(-1)
```

for every simple separated zero ordinate `gamma in F_E(T,c)`.

This closes only the local derivative-shift comparison.  It does not close H1,
the BFMT prime-polynomial lower bound, the bad-set budget, or any multiple-zero
residue problem.

## Theorem Target

Let

```text
L_E^*(s) := L(E,s+1/2)
```

be the normalized fixed-newform L-function, so its critical line is
`Re s = 1/2`.  Let `rho = 1/2+i gamma`, let `alpha = 1/log T`, and define

```text
F_E(T,c) = {gamma in (T,2T]:
  L_E^*(1/2+i gamma)=0 is simple and
  |gamma-gamma'| >= c/log T for every other nontrivial zero ordinate gamma'}.
```

Assume RH for `L_E^*`.  Then, for fixed `E` and fixed `c>0`,

```text
log |(L_E^*)'(rho)|^(-1)
  <= log |L_E^*(rho+alpha)|^(-1)
     + O_(E,c)(log T/log log T)
```

uniformly for `gamma in F_E(T,c)`.  In original elliptic-curve variables this is

```text
log |L'(E,1+i gamma)|^(-1)
  <= log |L(E,1+1/log T+i gamma)|^(-1)
     + O_(E,c)(log T/log log T).
```

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT01_GL2_BFMT_ADAPTATION_BLUEPRINT_2026-05-11.md`: names `GL2-ShiftDerivativeComparison(E,c)` as the fixed-curve analogue of BFMT Lemma 2.1 and isolates it from the remaining BFMT inputs.
- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`: records the exact needed comparison and notes that Milinovich-Ng supply the fixed-newform `S_f(t)` bound on RH.
- `/tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt`: BFMT Lemma 2.1 uses Kirila equation `(2.1)` to compare `log |zeta'(rho)|` with `log |zeta(rho+1/log T)|`, then bounds the zero sum by separation plus Littlewood's RH bound for `S(t)`.
- `/tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt`: Milinovich-Ng define normalized holomorphic newform L-functions with critical line `Re s=1/2`; Lemma 3.1 gives `N_f(t)=theta_f(t)+S_f(t)`, `theta_f'(t)=O_f(log t)`, and on RH `S_f(t)=O_f(log t/log log t)`.

## Proof Attempt

Work with the completed fixed-newform function

```text
Lambda_E^*(s) = Q_E(s) L_E^*(s),
```

where `Q_E(s)` is the fixed conductor/gamma factor.  It is entire of order one.
For a simple nontrivial zero `rho=1/2+i gamma`, the Hadamard quotient for
`Lambda_E^*(rho+alpha)/((rho+alpha-rho)(Lambda_E^*)'(rho))`, followed by
Stirling on the fixed gamma factor, gives the Kirila-style identity

```text
log |(L_E^*)'(rho)|
 = log |L_E^*(rho+alpha)| - log alpha
   - (1/2) sum_(rho' != rho)
       log(1 + alpha^2/(gamma-gamma')^2)
   + O_E(1).
```

Here the sum is over nontrivial zeros with multiplicity.  The conductor and
gamma-factor quotient contributes only `O_E(alpha log T)+O_E(1)=O_E(1)` since
`alpha=1/log T`; trivial-zero/gamma bookkeeping is included in this Stirling
term.

After inversion,

```text
log |(L_E^*)'(rho)|^(-1)
 <= log |L_E^*(rho+alpha)|^(-1)
    + (1/2) M_E(gamma,alpha) + O_E(1),
```

because `log alpha <= 0`, where

```text
M_E(gamma,alpha)
 := sum_(rho' != rho) log(1 + alpha^2/(gamma-gamma')^2).
```

It remains to prove

```text
M_E(gamma,alpha) <<_(E,c) log T/log log T.
```

Let `R(T)=log T/log log T`.  Milinovich-Ng Lemma 3.1 gives, under RH,

```text
N_E^*(t+u)-N_E^*(t-u) <<_E u log T + R(T) + 1
```

for `t asymp T` and `0<u<=T`, by combining `theta_E'(t)=O_E(log t)` with
`S_E(t)=O_E(R(T))`.

Split the zero sum at `alpha`.

For `|gamma-gamma'|<alpha`, separation gives
`|gamma-gamma'|>=c alpha`; the local zero-count bound gives at most
`O_E(R(T))` zeros with multiplicity, and each summand is
`O_c(1)`.  Hence this part is `O_(E,c)(R(T))`.

For `|gamma-gamma'|>=alpha`, use dyadic annuli

```text
2^j alpha <= |gamma-gamma'| < 2^(j+1) alpha.
```

The same zero-count bound gives

```text
#annulus_j <<_E 2^j + R(T)
```

while the summand is `O(2^(-2j))`.  Therefore

```text
sum_j (2^j + R(T)) 2^(-2j) << R(T).
```

Zeros outside the comparable-height range contribute `O_E(1)` by the standard
convergent tail in the Hadamard/Stirling quotient.  Thus

```text
M_E(gamma,alpha) <<_(E,c) R(T),
```

and the theorem follows.

## Obstruction or Closure

Closure for this named input:

```text
GL2-ShiftDerivativeComparison(E,c): closed under fixed-newform RH.
```

No extra source is missing for the local comparison once the standard
Hadamard/Kirila quotient is allowed and Milinovich-Ng Lemma 3.1 supplies the
fixed-newform `S_f(t)` bound.  The result is conditional because the RH input is
conditional.

Not closed here:

```text
GL2-BFMT-PrimePolynomialLowerBound(E)
EC-BFMT-BadSetBudget(E,c)
multiple-zero Laurent/residue control
full H1 rank-one reciprocal-derivative sum
```

## Dependency Impact

The separated BFMT route may now remove `GL2-ShiftDerivativeComparison(E,c)`
from its missing-input list.  The remaining separated-branch analytic input is
the fixed-curve BFMT prime-polynomial lower bound, together with the already
audited zero-sampling coefficient estimates.

This packet gives no control over `F_E(T,c)^c`; pair-correlation or zero counts
still do not bound reciprocal derivatives on clustered zeros.
