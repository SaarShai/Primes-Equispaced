---
schema_version: 1
title: "Fixed H1 weight principal-value route"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.79
dependencies:
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
tags: [ec-ndc, h1, fixed-weight, principal-value, cancellation]
---

# Fixed Weight Principal-Value Route

Status: `RIGOROUS_REDUCTION`.

Confidence: `0.79`.

## Do Not Promote Unless

- The theorem mode is declared before composition: pointwise principal value
  along legal heights, dyadic log-Cesaro average, Besicovitch `B^2`, or an
  explicit oscillatory profile.
- The displayed simple-zero sum is used only after all same-ordinate terms are
  combined and all multiple-zero Laurent polynomial terms are ruled out,
  kernel-killed, retained, or averaged.
- A fixed-weight cancellation estimate is proved for

  ```text
  sum W_hat(i gamma) e^(i gamma u)/L'(E,1+i gamma),
  ```

  not inferred from zero counting, zero spacing, or reciprocal-derivative
  magnitude moments alone.
- Uniformity in `u` is stated on the scale needed by H1: fixed `u`, dyadic
  windows `u in [U,2U]`, or all real `u`. Fixed-`u` convergence alone is not a
  positive-rank asymptotic.
- The same legal height sequence controls the Perron contour remainder:
  horizontal edges, shifted vertical edge, original-line truncation, and
  indentation errors.
- Rank zero is not promoted to pointwise constant stabilization. Surviving
  simple residues are retained as an oscillatory/profile term or averaged.
- Product statements use the product-average diagonal constant, including
  H1/H2 matching-frequency correlations.
- External theorem citations remain absent here. Any future external theorem
  used to discharge a hypothesis must attach the repository source packet:
  `curl + pdftotext + short quote + page/equation`.

## Source Protocol

External theorem citations: none.

This note uses only local handoff dependencies listed above and conditional
hypotheses stated below. In particular, all zero-spacing, phase-cancellation,
and reciprocal-derivative moment assertions below are theorem assumptions, not
sourced facts.

## Object

For simple offcentral critical-line zeros `rho=1+i gamma`, set

```text
a_gamma = W_hat(i gamma)/L'(E,1+i gamma),
S_T(u)  = sum_(0<|gamma|<=T) a_gamma e^(i gamma u),
u       = log K,
r       = ord_(s=1) L(E,s).
```

The route asks whether `S_T(u)` can be interpreted without absolute
convergence.

For real kernels and the usual conjugation symmetry,

```text
a_(-gamma) = conjugate(a_gamma),
```

so symmetric truncation over `+-gamma` gives

```text
a_gamma e^(i gamma u) + a_(-gamma)e^(-i gamma u)
 = 2 Re(a_gamma e^(i gamma u)).
```

This is not cancellation. It is a real oscillation unless the net coefficient
at that frequency is zero.

## Verdict

The direct principal-value route can close positive-rank H1 only in the strong
pointwise mode:

```text
there are legal heights T_n -> infinity such that
S_(T_n)(u) converges to Z_PV(u),
Z_PV(u) = o(u^r),
and the contour remainder along the same T_n is o(u^r).
```

For `r>=1`, a stronger but convenient sufficient form is

```text
sup_(u in [U,2U]) |Z_PV(u)| <= C U^beta,      beta < r.
```

Then the simple-zero aggregate is lower order and positive-rank H1 closes,
provided all multiple-zero effective degrees are `< r` or otherwise handled.

But this is a new fixed-weight principal-value theorem. It is not supplied by
zero spacing or reciprocal-derivative magnitude moments alone. Those inputs can
support a Besicovitch/log-average/profile theorem, not a pointwise H1 theorem,
unless a separate phase-cancellation estimate is added.

Claim-safe decision:

```text
Strong uniform PV cancellation assumed/proved -> positive-rank H1 can close.
Spacing + square moments only                 -> averaged/profile theorem.
Rank zero                                     -> oscillatory/profile theorem.
```

## Mode 1: Pointwise Principal Value Along Heights

Legal height mode:

```text
Z_PV(u) = lim_(n->infinity) S_(T_n)(u),
```

where `T_n` avoids zero ordinates and is the same sequence used in the H1
finite-box contour identity.

A non-absolute but checkable shell formulation is:

```text
B_k(U) =
  sup_(u in [U,2U])
  |sum_(2^k<|gamma|<=2^(k+1)) a_gamma e^(i gamma u)|.
```

Pointwise positive-rank closure follows if:

```text
1. the shell tails are Cauchy in the same dyadic windows;
2. sum_k B_k(U) = O(U^beta) with beta < r;
3. the contour remainder along the corresponding legal heights is o(U^r);
4. every offcentral multiple-zero term has effective degree < r, or is
   cancelled, kernel-killed, retained, or averaged.
```

The all-`u` uniform version is:

```text
sum_k sup_(u in R)
  |sum_(2^k<|gamma|<=2^(k+1)) a_gamma e^(i gamma u)|
< infinity.
```

This gives a bounded uniformly convergent PV profile and closes every positive
rank `r>=1` after the contour tail is controlled. It is stronger than needed
but clean.

### What Must Be Proved

This mode needs genuine cancellation in the twisted coefficients

```text
a_gamma e^(i gamma u).
```

Magnitude information such as

```text
J_E,2(T) =
  sum_(T<|gamma|<=2T) |L'(E,1+i gamma)|^(-2)
```

does not control the phases of `1/L'(rho)` and therefore does not control
`S_T(u)` pointwise. Zero spacing controls frequencies, not coefficient
alignment. At `u=0`, for example, the phases are just `arg(a_gamma)`.

Thus a pointwise PV theorem needs a direct weighted exponential-sum bound, for
example a square-root-cancellation hypothesis:

```text
sup_(u in [U,2U])
|sum_(T<|gamma|<=2T) a_gamma e^(i gamma u)|
<= C_(T,U)
   (sum_(T<|gamma|<=2T) |a_gamma|^2)^(1/2),
```

with

```text
sum_(T dyadic) C_(T,U) (sum_shell |a_gamma|^2)^(1/2)
 = O(U^beta),       beta<r.
```

This is the direct fixed-weight theorem. It cannot be replaced by pair
correlation alone.

## Moment Thresholds

Assume Mellin decay

```text
|W_hat(i t)| <= C_W (1+|t|)^(-q).
```

On a shell,

```text
sum_(T<|gamma|<=2T) |a_gamma|^2
 <= C_W^2 T^(-2q) J_E,2(T).
```

If

```text
J_E,2(T) <= C T^(theta) (log T)^B,
```

then coefficient square-summability follows from

```text
theta < 2q.
```

For the smoothstep-scale case `q=2`, this is

```text
J_E,2(T) <= C T^(4-delta).
```

This is enough for a Besicovitch `B^2` route, and it is enough for pointwise PV
only after adding the square-root shell cancellation above.

By contrast, the absolute-convergence route from the breakthrough synthesis
uses zero counting plus Cauchy-Schwarz and needs

```text
theta < 2q - 1,
```

namely `theta<3` for `q=2`.

So cancellation would buy one power in the reciprocal-derivative shell moment:

```text
absolute route:       J_E,2(T) << T^(2q-1-delta);
PV/B^2 cancellation:  J_E,2(T) << T^(2q-delta),
```

but only if the missing phase-cancellation theorem is supplied for the actual
fixed H1 weight.

## Mode 2: Dyadic Log-Cesaro Average

Use the same log average as the product-average theorem:

```text
A_U F = (1/U) int_U^(2U) F(u) du.
```

For a finite frequency set,

```text
A_U e^(i gamma u)
 = (e^(2 i gamma U)-e^(i gamma U))/(i gamma U),
gamma != 0.
```

Thus finite nonzero H1 frequencies average to zero. For the infinite sum, a
claim-safe sufficient hypothesis is:

```text
there exists Y(U)->infinity such that

(1/U) sum_(0<|gamma|<=Y(U)) |a_gamma|/|gamma| -> 0,

and

A_U |sum_(|gamma|>Y(U)) a_gamma e^(i gamma u)| -> 0.
```

Then

```text
A_U Z(u) -> 0
```

for the simple-zero H1 aggregate `Z`.

For positive rank, if the normalized aggregate is mean-bounded, then

```text
A_U |u^(-r) Z(u)| -> 0,       r>=1.
```

This is an averaged H1 theorem, not pointwise H1 closure. It composes with H2
only in the arithmetic product-average mode, where matching H1/H2 frequencies
produce diagonal constants.

For rank zero, Cesaro averaging may kill the mean of `Z` itself, but the
pointwise object remains

```text
Q_0 + Z(u) + o(1)
```

unless every nonzero coefficient is killed.

## Mode 3: Besicovitch `B^2`

Define the mean-square mode by completion of finite exponential polynomials in
the seminorm

```text
||F||_(B^2)^2 =
  limsup_(U->infinity) (1/U) int_U^(2U) |F(u)|^2 du.
```

After same-frequency combination, finite exponential polynomials have
orthogonal nonzero frequencies in the limiting mean. Therefore the clean
conditional input is

```text
sum_gamma |a_gamma|^2 < infinity.
```

A sufficient shell moment is

```text
J_E,2(T) <= C T^(2q-delta).
```

For `q=2`, this is `J_E,2(T) <= C T^(4-delta)`.

Then the simple-zero series defines a Besicovitch profile

```text
Z_B(u) = sum_gamma a_gamma e^(i gamma u)
```

in `B^2`. For `r>=1`,

```text
u^(-r) Z_B(u) -> 0
```

in dyadic mean square. This supports:

```text
c_E,W(e^u) = Q_r(u) + Z_B(u) + error
```

as a `B^2`/profile statement, and after normalization the simple-zero profile
is lower order in mean square.

It does not give pointwise convergence of `S_T(u)`, pointwise boundedness of
`Z_B(u)`, or a pointwise H1 theorem.

### Spacing Needed For Quantitative Windows

Abstract `B^2` convergence uses limiting orthogonality after finite
truncation. If the theorem needs uniform finite-window estimates before taking
limits, add a weighted spacing or pair-correlation hypothesis such as control
of

```text
sum_(gamma != eta, |gamma|,|eta|<=Y)
  |a_gamma a_eta| min(1, 1/(U |gamma-eta|)).
```

Equivalently, use a weighted large-sieve/pair-count statement for close
ordinate pairs. This is a spacing hypothesis. It still does not control the
phases of `a_gamma`, so it remains an averaged theorem unless combined with a
pointwise shell-cancellation estimate.

## Hypotheses By Type

Zero spacing:

```text
PV contour:
  legal heights T_n avoiding zero ordinates and giving reciprocal strip bounds.

Besicovitch:
  distinct frequencies after same-ordinate combination; quantitative windows
  require weighted close-pair control.

Pointwise sup_u:
  spacing is not enough; it must feed a weighted exponential-sum theorem.
```

Phases:

```text
Conjugate symmetry only makes the profile real. It does not cancel it.

Pointwise PV requires cancellation of arg(a_gamma)+gamma u in every required
u-window.

Cesaro/log average supplies cancellation of fixed nonzero frequencies in u,
but only after tails justify passage to the infinite sum.
```

Reciprocal derivative moments:

```text
absolute pointwise closure:
  J_E,2(T) << T^(2q-1-delta).

B^2/profile closure:
  J_E,2(T) << T^(2q-delta).

pointwise PV via square-root shell cancellation:
  J_E,2(T) << T^(2q-delta), plus the separate uniform cancellation theorem.
```

Uniformity in `u`:

```text
fixed u:
  defines a value of a PV series, but does not prove an asymptotic as u->infty.

u in [U,2U]:
  enough for positive-rank H1 if the bound is O(U^beta), beta<r.

all u:
  strongest and cleanest; gives bounded AP-like profile if tails converge.

Cesaro/B^2:
  no pointwise uniformity; the theorem is only mean/profile mode.
```

## Positive-Rank Decision

For simple zeros, a direct principal-value theorem can close positive-rank H1
in the following exact form:

```text
Assume:
  r>=1;
  all surviving critical-line offcentral residues are simple, or all multiple
  terms have effective degree < r after kernel zeros and cancellations;
  legal-height PV sums converge to Z_PV(u);
  sup_(u in [U,2U]) |Z_PV(u)| = O(U^beta), beta<r;
  the shifted-contour and horizontal/original-line remainders are o(U^r)
  in the same legal-height scheme.

Then:
  c_E,W(e^u) = Q_r(u) + o(u^r).
```

This is a correct theorem template.

It is not a closed proof route from known local inputs. The load-bearing new
input is the uniform fixed-weight PV cancellation estimate. If that estimate is
not proved, the route should be demoted to:

```text
Besicovitch/profile H1 theorem,
dyadic log-Cesaro theorem,
or product-average diagonal theorem.
```

## Rank-Zero Decision

For `r=0`, even a convergent principal-value profile is main scale:

```text
c_E,W(e^u) = Q_0 + Z_PV(u) + o(1).
```

The pointwise constant theorem requires

```text
Z_PV(u) -> 0,
```

which for a nonzero almost-periodic or Besicovitch frequency profile is an
extra coefficient-killing theorem, not a consequence of PV summability.

Thus rank zero can only be promoted as:

```text
oscillatory profile,
explicit filtering/subtraction theorem,
dyadic log-Cesaro average,
or product-average theorem with diagonal correlations.
```

## Bottom Line

The direct fixed-weight cancellation route is useful as a named reduction:

```text
prove uniform PV shell cancellation for the actual H1 coefficients
=> positive-rank H1 closes conditionally.
```

But the natural weaker package

```text
zero spacing + J_E,2(T) << T^(2q-delta)
```

does not close pointwise H1. It gives a Besicovitch/log-average/profile route.
For theorem promotion, the project should label this as an averaged/profile
fallback unless the strong uniform PV theorem is independently proved.

## Changed Files

```text
handoff-2026-05-11-h1-shell-moment-wave/FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md
```
