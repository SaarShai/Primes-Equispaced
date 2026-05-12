---
schema_version: 1
title: "H1 fixed-weight PV no-go and conditional theorem package"
date: 2026-05-11
agent: "H1-FixedWeight-PV"
type: theorem-reduction
tier: working
status: NO_GO_CONDITIONAL
confidence: 0.86
dependencies:
  - handoff-2026-05-11-h1-shell-moment-wave/FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md
  - handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
tags: [ec-ndc, h1, fixed-weight, principal-value, no-go, conditional]
---

# H1 Fixed-Weight PV No-Go And Conditional Package

Status: `NO_GO_CONDITIONAL`.

Verdict: no closed proof path was found from the current shell/PV/residue
inputs. The positive-rank H1 theorem can close if a new fixed-weight PV
cancellation theorem is assumed or proved. Spacing plus square moments cannot
prove that theorem; they support only averaged/profile modes unless a separate
pointwise exponential-sum estimate is added.

## Object

Use the H1 normalization

```text
c_E,W(e^u) = (1/(2 pi i)) int e^(u z) W_hat(z)/L(E,1+z) dz,
u = log K,
r = ord_(s=1) L(E,s).
```

For simple offcentral critical-line zeros `rho=1+i gamma`, after combining
same-ordinate contributions, set

```text
a_gamma = W_hat(i gamma)/L'(E,1+i gamma),
Z_T(u) = sum_(0<|gamma|<=T) a_gamma e^(i gamma u),
```

with symmetric legal heights `T` avoiding zero ordinates and the contour
boundary.

## Exact Conditional Theorem

`H1-fixed-weight-PV(E,W,r)` means the following package.

Assume:

```text
(A) finite-height H1 contour identity:
    c_E,W(e^u) = Q_E,W(u) + Z_T(u) + M_T(u) + I_T(u)
    at every legal height T.

(B) central polynomial:
    Q_E,W(u) has degree r and leading coefficient
    w_(-1)/L^(r)(E,1), hence 1/L^(r)(E,1) for normalized W.

(C) multiple-zero terms:
    every uncancelled offcentral multiple-zero residue in M_T has effective
    degree < r, or is kernel-killed, retained explicitly, or averaged in the
    theorem mode.

(D) fixed-weight PV cancellation:
    along legal heights T_n -> infinity, Z_(T_n)(u) converges to Z_PV(u)
    in the declared dyadic windows, and

      sup_(u in [U,2U]) |Z_PV(u)| = o(U^r).

(E) contour tails in the same height scheme:
    the shifted-line, horizontal, original-line, and indentation remainders
    converge to I_PV(u) with

      sup_(u in [U,2U]) |I_PV(u)| = o(U^r).
```

Then, for `r>=1`,

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r)
```

uniformly in dyadic windows. This is the exact positive-rank H1 closure
statement.

For `r=0`, the theorem becomes

```text
c_E,W(e^u) = Q_0 + Z_PV(u) + I_PV(u).
```

A pointwise constant rank-zero theorem needs the stronger input
`Z_PV(u)+I_PV(u)=o(1)`. Mere PV convergence leaves a main-scale oscillatory
profile.

## Proof Route If The PV Input Is Supplied

The proof is bookkeeping, not a new residue argument.

1. Start from the finite-box contour identity in
   `H1_CONTOUR_SHIFT_THEOREM.md`.
2. Insert the central residue polynomial `Q_E,W(u)`.
3. Combine same-ordinate simple residues into `Z_T(u)`.
4. Put all multiple-zero Laurent residue polynomials into `M_T(u)` and apply
   the effective-degree condition.
5. Pass to the legal-height PV limit. Assumptions `(D)` and `(E)` give
   `Z_PV(u)+I_PV(u)=o(u^r)`.
6. Since all retained offcentral polynomial degrees are `< r`, their total is
   `O(u^(r-1))` in the pointwise bounded/summable mode, hence `o(u^r)`.

This closes positive-rank H1 conditionally. It does not prove the PV input.

## No-Go: Spacing Plus Square Moments

Spacing and square moments do not imply `H1-fixed-weight-PV`.

Abstract model:

```text
gamma_n = n,
a_n = a_(-n) = 1/(2n),        n>=1.
```

Then the frequencies have perfect spacing and

```text
sum_(T<n<=2T) (|a_n|^2 + |a_(-n)|^2) << T^(-1),
```

so the coefficient sequence is globally square-summable and satisfies far
stronger dyadic square-moment bounds than the Besicovitch/profile route needs.
But the symmetric sums are

```text
Z_T(u) = sum_(1<=n<=T) cos(nu)/n.
```

At `u=2 pi m`,

```text
Z_T(u) = sum_(1<=n<=T) 1/n -> infinity.
```

Away from those points the limit is the logarithmic Fourier series
`-log(2|sin(u/2)|)`, with singularities at the same resonant points. Thus
excellent spacing plus `l^2` coefficients does not even force pointwise PV
convergence for all `u`, and cannot force the dyadic uniform bound
`Z_PV(u)=o(u^r)`.

This is not an EC counterexample. It is a logical insufficiency test: any
argument using only spacing and coefficient square moments would also apply
to this model, where the desired PV conclusion is false.

## What The Weaker Inputs Do Prove

If

```text
sum_gamma |a_gamma|^2 < infinity
```

and the zero ordinates satisfy a weighted close-pair or large-sieve estimate,
then finite sums are controlled in dyadic mean square:

```text
(1/U) int_U^(2U) |sum a_gamma e^(i gamma u)|^2 du
```

is bounded by the diagonal plus controlled close-pair terms. This gives a
Besicovitch/profile theorem. For `r>=1`, it gives

```text
u^(-r) Z(u) -> 0
```

in dyadic mean square, not pointwise or uniformly.

A log-Cesaro theorem can also kill fixed nonzero frequencies after tails are
justified. That is an averaged theorem. It does not replace the pointwise H1
input.

## Only Viable Direct Proof Path

A promotable proof must estimate the actual fixed H1 exponential sums

```text
B_E,W(T,U) =
  sup_(u in [U,2U])
  |sum_(T<|gamma|<=2T) a_gamma e^(i gamma u)|.
```

A sufficient theorem is

```text
sum_(T dyadic) B_E,W(T,U) = o(U^r),
```

with the same legal heights used in the contour shift. A square-root version
would be

```text
B_E,W(T,U)
 <= C_E,W(T,U)
    (sum_(T<|gamma|<=2T) |a_gamma|^2)^(1/2),

sum_T C_E,W(T,U)
    (sum_(T<|gamma|<=2T) |a_gamma|^2)^(1/2)
 = o(U^r).
```

This is a new fixed-curve theorem about the phases of
`1/L'(E,1+i gamma)` coupled to the zero ordinates. Pair correlation, zero
counting, simple zeros, and reciprocal-derivative square moments do not supply
it by themselves.

## Claim-Safe Package

Use one of these theorem modes.

```text
Pointwise positive rank:
  assume/prove H1-fixed-weight-PV(E,W,r) plus contour tails and multiple-zero
  effective-degree control. Then c_E,W(e^u)=Q_E,W(u)+o(u^r).

Rank zero:
  state c_E,W(e^u)=Q_0+Z_PV(u)+o(1), or average/filter/subtract Z_PV.
  Do not state a constant limit unless Z_PV(u)->0 is separately proved.

Averaged/profile fallback:
  spacing + square moments may justify Besicovitch, dyadic log-Cesaro, or
  product-average statements. Keep that mode explicit through H2 composition.
```

## Unresolved Inputs

- A fixed-curve exponential-sum theorem for
  `sum W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)` uniformly in the required
  `u` windows.
- Or a stronger absolute route, such as
  `sum |W_hat(i gamma)/L'(E,1+i gamma)| < infinity`.
- Fixed-curve reciprocal-derivative upper bounds or anti-small-derivative
  estimates strong enough for the chosen kernel decay.
- Legal height sequence and contour tail bounds, including `H-height` with
  exponent below the Mellin decay available for `W`.
- Multiple-zero Laurent coefficient control, kernel killing, or explicit
  retained polynomial profiles.
- Same theorem mode for H2 before composing any EC smoothing statement.

## Changed Files

```text
handoff-2026-05-11-h1-shell-moment-wave/H1_FIXED_WEIGHT_PV_NOGO_CONDITIONAL_2026-05-11.md
```
