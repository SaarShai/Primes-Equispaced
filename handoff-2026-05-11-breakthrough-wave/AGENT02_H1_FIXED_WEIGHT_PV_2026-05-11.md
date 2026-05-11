---
schema_version: 1
title: "Agent 02 - EC H1 fixed-weight principal-value cancellation"
date: 2026-05-11
agent: "Agent 02 - EC H1 Fixed-Weight PV"
type: theorem-obstruction-packet
tier: working
status: NO_GO
confidence: 0.87
tags: [ec-ndc, h1, fixed-weight, principal-value, besicovitch, log-cesaro, product-average]
---

# Agent 02 - H1 Fixed-Weight PV

Status: `NO_GO`.

No fixed-curve EC theorem is promoted. The pointwise uniform cancellation
theorem for

```text
Z_T(u) =
  sum_(0<|gamma|<=T)
    W_hat(i gamma) e^(i gamma u) / L'(E,1+i gamma)
```

is exactly a missing H1 input. Current packets prove a rigorous reduction:
positive analytic rank closes if this PV theorem is assumed together with the
same legal-height contour tails and multiple-zero degree control. They do not
prove the PV theorem.

## Setup

Use analytic rank only:

```text
u = log K,
r = ord_(s=1) L(E,s).
```

For simple critical-line offcentral zeros `rho=1+i gamma`, after combining
same-ordinate residues,

```text
a_gamma = W_hat(i gamma) / L'(E,1+i gamma).
```

Multiple-zero Laurent terms are not hidden in `Z_T`; they must be killed,
retained, averaged, or proved to have effective degree `< r`. H2 branch damping
is not available for these H1 reciprocal-pole residues.

## Pointwise PV Mode

The needed theorem is:

```text
H1-fixed-weight-PV(E,W,r):
  legal heights T_n -> infinity exist such that
  Z_(T_n)(u) -> Z_PV(u)
  in the same dyadic windows used by the H1 contour, and

    sup_(u in [U,2U]) |Z_PV(u)| = o(U^r),

  while the shifted-line, horizontal, original-line, and indentation remainders
  are also o(U^r) in that same height scheme.
```

Then, with the central polynomial

```text
Q_E,W(u) = u^r/L^(r)(E,1) + lower powers
```

for normalized `Res_(z=0) W_hat(z)=1`, the finite-box H1 identity gives

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r)       (r >= 1).
```

This is a valid conditional theorem, not a proof of uniform cancellation.

The direct shell target is:

```text
B_E,W(T,U) =
  sup_(u in [U,2U])
  |sum_(T<|gamma|<=2T) a_gamma e^(i gamma u)|,

sum_(T dyadic) B_E,W(T,U) = o(U^r)
```

along legal heights. No local packet or checked source proves this fixed-weight
bound.

## No-Go For Current Inputs

Spacing plus square moments cannot imply pointwise PV cancellation.

Model:

```text
gamma_n = n,
a_n = a_(-n) = 1/(2n).
```

Then the frequencies are perfectly spaced and the coefficients are globally
square-summable, but symmetric truncations give

```text
Z_T(u) = sum_(1<=n<=T) cos(nu)/n.
```

At `u=2 pi m`, `Z_T(u)` diverges like `log T`. Away from resonance it converges
to the logarithmic Fourier profile with singularities. Therefore any proof
using only spacing and `l^2` coefficient control would prove a false statement
in this model.

This is not an EC counterexample. It is a logical obstruction to the available
proof strategy. A promotable proof must use the actual phases of
`W_hat(i gamma)/L'(E,1+i gamma)` coupled to the ordinates.

## Besicovitch/Profile Mode

Assume

```text
sum_gamma |a_gamma|^2 < infinity
```

plus whatever weighted close-pair estimate is needed for quantitative dyadic
windows. Then the series defines a Besicovitch `B^2` profile

```text
Z_B(u) = sum_gamma a_gamma e^(i gamma u)
```

and for `r>=1`,

```text
u^(-r) Z_B(u) -> 0
```

in dyadic mean square. This supports

```text
c_E,W(e^u) = Q_r(u) + Z_B(u) + profile-small error
```

in `B^2`/profile mode. It does not give pointwise convergence, pointwise
boundedness, or dyadic sup-norm H1 closure.

If

```text
|W_hat(it)| <= C(1+|t|)^(-q),
J_E,2(T)=sum_(T<|gamma|<=2T)|L'(E,1+i gamma)|^(-2)
       <= C T^theta(log T)^B,
```

then `sum |a_gamma|^2 < infinity` follows from `theta < 2q`. For the current
smoothstep-scale `q=2`, the profile threshold is `theta<4`. The absolute
pointwise route needs the stronger `theta<2q-1`, hence `theta<3`.

Both are hypotheses here, not closed EC theorems.

## Dyadic Log-Cesaro Mode

Let

```text
A_U F = (1/U) int_U^(2U) F(u) du.
```

For fixed `gamma != 0`,

```text
A_U e^(i gamma u)
 = (e^(2i gamma U)-e^(i gamma U))/(i gamma U) -> 0.
```

For the infinite H1 zero sum this is claim-safe under a tail condition such as

```text
there exists Y(U)->infinity with
  (1/U) sum_(0<|gamma|<=Y(U)) |a_gamma|/|gamma| -> 0,

and
  A_U |sum_(|gamma|>Y(U)) a_gamma e^(i gamma u)| -> 0.
```

Then

```text
A_U Z(u) -> 0.
```

For `r>=1`, this gives averaged lower-order H1 after normalization if the
remaining normalized terms are mean-controlled. For `r=0`, it kills the mean
of nonzero frequencies but leaves the pointwise object

```text
Q_0 + Z(u) + o(1).
```

Thus log-Cesaro is an averaged theorem, not pointwise H1 stabilization.

## Product-Average Mode

The arithmetic averaged product must be stated for product values:

```text
A_U [c_E,W(e^u) P_E,W(e^u)].
```

It is not implied by an averaged statement for `log P`.

Assume the normalized H1 mean-scale profile is

```text
u^(-r)c_E,W(e^u) = H_c(u) + average-small,
H_c(u)=q_r + sum_gamma h_gamma e^(i gamma u),
q_r = 1/L^(r)(E,1),
```

where `h_gamma` are only retained H1 terms of polynomial degree `r`. Terms with
degree `>r` must be absent, cancelled, or renormalized.

Assume H2 has

```text
log P_E,W(e^u)
 = -r log u + B_H2(E,W) + Z_P(u) + eps_P(u),
G(u)=exp(Z_P(u))=sum_eta d_eta e^(i eta u)
```

in a joint dyadic mean mode with H1. Then the minimal arithmetic product
average is

```text
A_U[c_E,W(e^u) P_E,W(e^u)]
 -> exp(B_H2(E,W))
    (q_r d_0 + sum_gamma h_gamma d_(-gamma)).
```

This is the diagonal H1/H2 frequency constant. If H2 is pointwise
nonoscillatory, then `d_0=1` and `d_eta=0` for `eta != 0`, reducing the
constant to `exp(B_H2) q_r`. Without that extra H2 fact, `d_0` and the
cross-correlations are load-bearing.

Rank zero is main-scale:

```text
C_E,W^prod
 = exp(B_H2(E,W))
   (q_0 d_0 + sum_(gamma != 0) a_gamma d_(-gamma)).
```

Do not rewrite this as a pointwise constant theorem or as an averaged-log
statement.

## Minimal Substitute Theorem

Claim-safe replacement:

```text
Assume the finite-height H1 contour identity, central polynomial algebra,
legal-height contour tails in the declared mode, and multiple-zero effective
degree control.

Then:
  1. If H1-fixed-weight-PV(E,W,r) is proved, positive-rank H1 closes
     pointwise as c_E,W(e^u)=Q_E,W(u)+o(u^r).

  2. If only sum |a_gamma|^2 plus weighted close-pair control is proved,
     H1 closes only as a Besicovitch/profile theorem; after normalization,
     the simple-zero profile is lower order in dyadic mean square for r>=1.

  3. If the log-Cesaro tail condition is proved, fixed nonzero H1 frequencies
     average to zero in u, but pointwise oscillations remain.

  4. If H1 and H2 profiles have joint dyadic mean extraction, the product has
     the arithmetic diagonal constant
       exp(B_H2)(q_r d_0 + sum h_gamma d_(-gamma)).
```

This is the minimal substitute theorem. It preserves theorem mode and does not
promote uniform PV cancellation.

## Required Next Input

To promote the pointwise theorem, prove one of:

```text
sum_(T dyadic) B_E,W(T,U) = o(U^r)
```

for the actual fixed H1 coefficients, uniformly in `u in [U,2U]`, or the
stronger absolute route

```text
sum_gamma |W_hat(i gamma)/L'(E,1+i gamma)| < infinity.
```

For the current smoothstep-scale `q=2`, a sufficient absolute shell hypothesis
is

```text
J_E,2(T) <= C_E T^(3-delta).
```

The weaker `J_E,2(T) <= C_E T^(4-delta)` supports only the `B^2`/profile route
unless a separate pointwise exponential-sum theorem is added.

## Verification Notes

Read first/local:

```text
start.md
token-economy.yaml
L0_rules.md
primes-equispaced/L0_rules.md
primes-equispaced/L1_index.md
```

Required packets:

```text
primes-equispaced/handoff-2026-05-11-all-in-wave/H1_FIXED_WEIGHT_PV_PACKET_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md
```

Directly relevant H1 PV/source/profile packets:

```text
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_FIXED_WEIGHT_PV_NOGO_CONDITIONAL_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md
primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave/DISPATCH_MANIFEST_2026-05-11.md
```

External theorem claims: none added. Existing local source-audit claims were
used only as local audit conclusions; no new external citation is introduced,
so no new `curl + pdftotext` packet is required.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT02_H1_FIXED_WEIGHT_PV_2026-05-11.md
```
