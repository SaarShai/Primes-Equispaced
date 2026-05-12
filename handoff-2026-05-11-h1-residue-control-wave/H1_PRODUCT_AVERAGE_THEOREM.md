---
schema_version: 1
title: "H1 product-average theorem reduction"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.74
dependencies:
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
tags: [ec-ndc, h1, product-average, residue-control]
---

# H1 Product-Average Theorem

Confidence: 0.74.

Confidence rule: the product-mean algebra is closed conditionally; confidence is
capped by the weakest unsourced analytic input, namely H1 reciprocal-zero
control and H2 exponential branch-series mean control.

## Do Not Promote Unless

- The averaged object is `A_U[c_E,W(e^u) P_E,W(e^u)]` itself.
- Do not replace it by averaged `log P`, a geometric mean, or pointwise `c`
  times a log-average of `P`.
- The averaging mode is declared as dyadic Cesaro in `u=log K`, equivalently a
  logarithmic `dK/K` average in `K`; no logarithm of the product is taken.
- The H2 input supplies mean coefficients of `G(u)=exp(Z_P(u))`, not only mean
  coefficients of `Z_P(u)`.
- The constant includes all diagonal H1/H2 frequency correlations
  `h_gamma d_(-gamma)`.
- Rank zero is separated: simple H1 reciprocal residues are main-scale terms.
- Offcentral H1 reciprocal-pole terms of degree `j>r` are absent, cancelled, or
  explicitly renormalized; otherwise this finite average is not closed.
- Same fixed curve `E`, same kernel `W`, same Mellin normalization, same
  analytic rank `r=ord_{s=1}L(E,s)`, and exact Agent-3 local factors are used.
- No external theorem is cited unless the project protocol
  `curl + pdftotext + verbatim quote + page/equation` is attached.

## Dependencies

- H1 reciprocal Perron expansion: central polynomial, offcentral Laurent
  residue degrees, reciprocal derivative/Laurent coefficient control, and
  contour tails.
- H2 exact Agent-3 product package: `S1_W`, `Ssym_W`, `Mgood_W`, `Rge3_W`, bad
  primes, and the constant `B_H2(E,W)`.
- H2 branch/exponential package: an expansion for `log P` with branch series
  `Z_P`, plus dyadic mean coefficients for `exp(Z_P)`.
- Joint H1/H2 mean extraction: diagonal terms survive and offdiagonal/tail terms
  vanish in the same dyadic windows.

Internal provenance only:

- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md`
- No external theorem citation is used in this deliverable.

## Mode And Measure

Let

```text
u = log K.
```

The product average is

```text
A_U^prod(F)
  = (1/U) int_U^(2U) F(u) du
  = (1/U) int_exp(U)^exp(2U) F(log K) dK/K.
```

The target is the arithmetic average

```text
A_U^prod(c_E,W(e^u) P_E,W(e^u)).
```

This is a log-Cesaro average of product values. It is not the geometric mean

```text
exp(A_U^prod(log(c_E,W(e^u) P_E,W(e^u)))).
```

## Conditional Product-Average Theorem

Fix an elliptic curve `E/Q`, a real admissible kernel `W`, and

```text
r = ord_(s=1) L(E,s).
```

Assume the normalized H1 reciprocal expansion has the form

```text
c_E,W(e^u)
 = Q_r(u)
   + sum_(gamma != 0) sum_(j >= 0) a_(gamma,j) u^j e^(i gamma u)
   + E_c(u),

Q_r(u) = q_r u^r + q_(r-1) u^(r-1) + ... + q_0.
```

For the normalized kernels in the H1 synthesis,

```text
q_r = 1 / L^(r)(E,1).
```

With another Mellin residue convention, replace `q_r` by the corresponding H1
central leading coefficient.

The offcentral coefficients `a_(gamma,j)` are the combined reciprocal-pole
Laurent residues at frequency `gamma` and degree `j`, after combining equal
frequencies and kernel cancellations. For a zero of multiplicity `m`, the
possible degrees are at most `m-1` before kernel cancellation.

Assume no term with `j>r` survives in the unrenormalized product average. Define
the retained H1 mean-scale profile

```text
H_c(u) = q_r + sum_(gamma in Gamma_r) h_gamma e^(i gamma u),

h_gamma = a_(gamma,r).
```

All lower H1 degrees, central lower powers, and H1 contour errors are assumed
average-small after product normalization:

```text
A_U^prod(
  |u^(-r)c_E,W(e^u) - H_c(u)| |G(u)|
) -> 0.
```

Assume the H2 product has a branch/exponential form

```text
log P_E,W(e^u)
 = -r log u + B_H2(E,W) + Z_P(u) + eps_P(u),

G(u) = exp(Z_P(u)),
```

and that exponentiating the H2 error is harmless in product mean:

```text
A_U^prod(
  |u^(-r)c_E,W(e^u) G(u)| |exp(eps_P(u))-1|
) -> 0.
```

Assume finally that `H_c` and `G` admit joint dyadic mean extraction. One
sufficient formulation is:

```text
H_Y(u) = sum_(gamma in Gamma(Y)) h_gamma e^(i gamma u),
G_Y(u) = sum_(eta in Lambda(Y)) d_eta e^(i eta u),
```

with finite `Gamma(Y), Lambda(Y)`, tail condition

```text
lim_(Y->infty) limsup_(U->infty)
  A_U^prod( |H_c-H_Y| |G| + |H_Y| |G-G_Y| ) = 0,
```

and convergent diagonal sums

```text
D_Y = sum_(gamma in Gamma(Y), eta in Lambda(Y), gamma+eta=0)
        h_gamma d_eta
    -> D.
```

Then

```text
A_U^prod(c_E,W(e^u) P_E,W(e^u))
  -> C_E,W^prod,

C_E,W^prod = exp(B_H2(E,W)) D.
```

When the limiting H2 coefficients are written directly as

```text
d_eta = Mean_dyadic(G(u) e^(-i eta u)),
```

the constant is

```text
C_E,W^prod
 = exp(B_H2(E,W))
   (q_r d_0 + sum_(gamma in Gamma_r) h_gamma d_(-gamma)).
```

Equivalently, the product profile is

```text
c_E,W(e^u) P_E,W(e^u)
 = exp(B_H2(E,W)) H_c(u) G(u)
   + average-small error,
```

and the theorem states the dyadic mean of that profile.

## Diagonal And Offdiagonal Treatment

For finite truncations,

```text
A_U^prod(H_Y G_Y)
 = sum_(gamma,eta) h_gamma d_eta A_U^prod(e^(i(gamma+eta)u)).
```

If `gamma+eta=0`, then

```text
A_U^prod(e^(i(gamma+eta)u)) = 1.
```

These are the diagonal terms. They produce exactly

```text
sum_(gamma+eta=0) h_gamma d_eta.
```

If `gamma+eta != 0`, then

```text
A_U^prod(e^(i(gamma+eta)u))
 = (e^(2i(gamma+eta)U)-e^(i(gamma+eta)U))
   /(i(gamma+eta)U),
```

so each fixed offdiagonal term tends to `0`. The finite offdiagonal part
therefore vanishes as `U->infty`. The tail hypothesis is exactly what permits
passing from finite truncations to the infinite H1/H2 frequency series.

No source theorem is hidden here: this is direct finite exponential algebra
plus the stated tail hypothesis.

## Case Constants

If H2 is pointwise nonoscillatory, then `G=1`, `d_0=1`, and `d_eta=0` for
`eta != 0`. Hence

```text
C_E,W^prod = exp(B_H2(E,W)) q_r
```

under the same H1 tail hypothesis. The nonzero retained H1 frequencies average
away because there is no matching H2 frequency. For the normalized H1
convention this is

```text
exp(B_H2(E,W)) / L^(r)(E,1).
```

If H2 has persistent oscillation but H1 has no retained degree-`r` offcentral
term, then

```text
C_E,W^prod = exp(B_H2(E,W)) q_r d_0,

d_0 = Mean_dyadic(exp(Z_P(u))).
```

This is not the geometric constant unless `d_0=1` is proved.

For rank zero, simple H1 reciprocal residues are retained because `j=r=0`:

```text
C_E,W^prod
 = exp(B_H2(E,W))
   (q_0 d_0 + sum_(gamma != 0) a_(gamma,0) d_(-gamma)).
```

If additionally `G=1`, the nonzero H1 frequencies average away under the same
tail hypothesis and the constant reduces to

```text
exp(B_H2(E,W)) / L(E,1).
```

If an offcentral H1 term with `j>r` survives, the unrenormalized finite product
average has no closed constant here. Offdiagonal oscillation does not by itself
save it: averaging `u^(j-r)e^(i omega u)` over `[U,2U]` leaves boundary terms
of size at least constant scale when `j-r>=1`.

## What This Proves And Does Not Prove

This proves a conditional product-level averaged fallback: once the H1
mean-scale reciprocal-zero profile and H2 exponential branch profile have a
joint dyadic mean, the averaged product has the explicit diagonal constant
above.

It does not prove the fixed-curve EC smoothing theorem. The remaining gaps are:

- H1 reciprocal Perron expansion is not source-closed.
- H1 reciprocal derivative/Laurent coefficient control is not source-closed.
- H2 branch and symmetric-square finite parts are not source-closed.
- Mean coefficients of `exp(Z_P)` are not supplied by an averaged theorem for
  `Z_P` or `log P`.
- Infinite diagonal/offdiagonal extraction needs its own tail or mean-square
  proof.
- Rank-zero and multiple offcentral zeros remain load-bearing cases.

Thus the only claim-safe promotion path is:

```text
prove H1 reciprocal-zero profile
+ prove H2 exponential branch-series mean
+ prove joint diagonal/offdiagonal tail control
=> product-level dyadic log-Cesaro average with C_E,W^prod above.
```

Changed file list:

- `handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md`
