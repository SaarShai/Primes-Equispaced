---
schema_version: 1
title: "Rank-zero profile/product-average theorem section package"
date: 2026-05-11
agent: RankZero-Profile-Package
type: theorem-section-outline
tier: working
status: CLAIM_SAFE_CONDITIONAL_PACKAGE
sources:
  - ../handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
  - ../handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
  - ../handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - ../handoff-2026-05-11-h1-shell-moment-wave/RANK_ZERO_FALLBACK_PAPER_SKELETON.md
  - ../handoff-2026-05-11-ec-theorem-closure-wave/H2_SYM2_PRODUCT_AVERAGE_PACKAGE.md
  - ../handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
  - ../handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
tags: [ec-ndc, h1, h2, rank-zero, oscillatory-profile, product-average]
---

# Rank-Zero Profile/Product-Average Theorem Section Package

Verdict: paper-ready as a conditional/profile section, not as fixed-curve
pointwise stabilization. The rank-zero H1 main scale is

```text
q_0 + Z_c(u),    u = log K,
```

so a constant theorem is unsafe unless all retained nonzero H1 coefficients
vanish, cancel, are kernel-killed, or are explicitly subtracted.

## Section Outline

Use this as a theorem section after the global EC smoothing reduction and
before any positive-rank pointwise theorem.

1. Kernel and product normalizations.
2. Rank-zero H1 reciprocal-Perron profile.
3. No constant limit without coefficient death.
4. H2 local algebra and product-form input.
5. Arithmetic dyadic product average.
6. Proof skeleton and promotion boundary.

## Definitions

Fix an elliptic curve `E/Q`. Write

```text
u = log K,
r = ord_(s=1) L(E,s).
```

This package is the rank-zero case:

```text
r = 0,
L(E,1) != 0.
```

An admissible kernel `W` is fixed once and for all. The local class
used here is:

```text
W:[0,infty)->R is compactly supported in [0,1],
W is regular enough for Mellin inversion on Re z = sigma > 0,
W_hat(z)=int_0^infty W(t)t^(z-1)dt,
W_hat(z)=w_(-1)/z + holomorphic at z=0,
```

and `W_hat` continues meromorphically to the strip used in the H1 contour
shift, with no unaccounted pole in that strip. The condition `W(t)=1` near
`0+` is a sufficient repository-normalized way to get

```text
w_(-1)=1.
```

For the smoothstep class used in the numerical lead, the available local decay
is only the finite strip bound

```text
W_hat(sigma+i tau) = O_W,sigma((1+|tau|)^(-2))
```

away from `z=0`. Any faster decay is an extra theorem hypothesis.

Define the H1 Perron object

```text
c_E,W(K)
 = (1/(2 pi i)) int_(Re z=sigma)
     K^z W_hat(z) / L(E,1+z) dz.
```

For good primes define the Agent-3 local factor

```text
A_p(1) = 1 - a_p/p + 1/p,
```

and for bad primes

```text
A_p(1) = 1 - a_p/p.
```

The H2 product is

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)),
log P_E,W(K) = - sum_p W(p/K) log A_p(1),
```

with the positive real log branch used by the reproducer.

The arithmetic dyadic product average is

```text
A_U(F) = (1/U) int_U^(2U) F(u) du
       = (1/U) int_exp(U)^exp(2U) F(log K) dK/K.
```

When it exists, write

```text
Mean_dyadic(F) = lim_(U->infinity) A_U(F).
```

This averages product values. It is not

```text
exp(A_U(log F)).
```

## Theorem 1: Rank-Zero H1 Oscillatory Profile

Let `E/Q` have analytic rank zero. Fix an admissible `W` in the above H1
normalization. Define

```text
q_0 = w_(-1)/L(E,1).
```

Let

```text
Gamma = { gamma in R\{0}: L(E,1+i gamma)=0 and the zero is simple }.
```

For `gamma in Gamma`, define

```text
a_gamma = W_hat(i gamma) / L'(E,1+i gamma).
```

For real `W`, conjugate symmetry gives

```text
a_(-gamma) = conjugate(a_gamma),
```

after combining equal frequencies and residue cancellations.

Assume:

```text
(H1-rz-1) The Mellin/Perron identity and finite-height H1 contour shift hold
          for the same fixed W. For admissible heights T,

          c_E,W(e^u) = q_0 + Z_T(u) + I_T(u).

(H1-rz-2) Every offcentral reciprocal pole in the shifted strip is either:
          simple and included in Gamma; kernel-killed; residue-cancelled; or
          retained in a separate explicit polynomial-exponential profile.

(H1-rz-3) No unrenormalized positive-degree offcentral term survives in this
          bounded profile theorem. In rank zero, any such term grows on the
          H1 scale.

(H1-rz-4) The simple-zero symmetric truncations

          Z_T(u) = sum_(gamma in Gamma, 0<|gamma|<=T)
                    a_gamma e^(i gamma u)

          converge in the declared pointwise profile mode. A sufficient
          pointwise mode is the uniform tail bound

          A(T) = sum_(gamma in Gamma, |gamma|>T) |a_gamma| -> 0.

(H1-rz-5) There are admissible legal heights T(u)->infinity such that

          |I_(T(u))(u)| + A(T(u)) -> 0.
```

Then

```text
c_E,W(e^u)
 = q_0 + Z_c(u) + o(1),

Z_c(u) = sum_(gamma in Gamma) a_gamma e^(i gamma u),
```

where the sum is interpreted in the declared convergence mode. For
repository-normalized kernels:

```text
c_E,W(e^u)
 = 1/L(E,1)
   + sum_(gamma in Gamma)
       W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)
   + o(1).
```

This is a pointwise oscillatory profile theorem. It is not a pointwise
constant-limit theorem.

## Lemma 2: No Constant Limit Without Coefficient Death

Assume `Z_c` is a uniform almost-periodic profile

```text
Z_c(u) = sum_(lambda in Lambda) b_lambda e^(i lambda u)
```

with the usual mean coefficient identity

```text
b_lambda = lim_(U->infinity) (1/U) int_0^U
             Z_c(u)e^(-i lambda u) du.
```

If `Z_c(u)` has a pointwise limit as `u->infinity`, then every coefficient
with `lambda != 0` is zero. Hence a rank-zero constant theorem

```text
c_E,W(e^u) = q_0 + o(1)
```

requires coefficient death:

```text
a_gamma = 0
```

for every retained nonzero H1 frequency after equal-frequency combination.
For simple zeros this means a genuine residue cancellation or
`W_hat(i gamma)=0`. Finite kernel filtering is a different renormalized
theorem unless it includes tail control for all remaining zeros.

## Proposition 3: Exact H2 Local Algebra

At good primes set

```text
lambda_p = a_p/sqrt(p),
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Define

```text
S1_W(K)     = sum_(p good) W(p/K) a_p/p,
Ssym_W(K)  = sum_(p good) W(p/K) chi_sym2(p)/p,
Mgood_W(K) = sum_(p good) W(p/K)/p,

R_p = -log(1 - a_p/p + 1/p)
      - a_p/p
      - (a_p^2 - 2p)/(2p^2),

Rge3_W(K)  = sum_(p good) W(p/K) R_p,
Bbad_W(K)  = -sum_(p bad) W(p/K) log(1-a_p/p).
```

Then the exact Agent-3 product satisfies

```text
log P_E,W(K)
 = S1_W(K)
   + (1/2) Ssym_W(K)
   - (1/2) Mgood_W(K)
   + Rge3_W(K)
   + Bbad_W(K).
```

The `m>=3` good-prime remainder is absolutely convergent by the local log
expansion and Hasse bound. This proposition is local algebra only; it does not
prove the endpoint-smoothed finite parts for `S1_W`, `Ssym_W`, or `Mgood_W`.

## H2 Product-Form Input

For rank zero, the H2 input compatible with Theorem 1 should be stated as a
product-form hypothesis:

```text
P_E,W(e^u) = exp(B_H2(E,W)) G(u)(1+eps_P(u)),
G(u) = exp(Z_P(u)).
```

The nonoscillatory H2 special case is

```text
G(u)=1,
eps_P(u)=o(1).
```

The pointwise finite-part route is the special case obtained from

```text
S1_W(e^u)
 = (1/2 + kappa_sym/2) log u + C1_E,W + e1(u),

Ssym_W(e^u)
 = -kappa_sym log u + Csym_E,W + esym(u),

Mgood_W(e^u)
 = log u + CM_E,W + eM(u),

Rge3_W(e^u)
 = Cge3_E + ege3(u),

Bbad_W(e^u)
 = Bbad_E + ebad(u),
```

with all errors `o(1)`. Then the log coefficients cancel exactly:

```text
(1/2 + kappa_sym/2) + (1/2)(-kappa_sym) - 1/2 = 0,
```

and

```text
B_H2(E,W)
 = C1_E,W
   + (1/2) Csym_E,W
   - (1/2) CM_E,W
   + Cge3_E
   + Bbad_E.
```

If offcentral H2 terms persist, keep them in `Z_P(u)`. Do not replace a
profile theorem for `log P` by a theorem for `P` unless exponentiating the error
is controlled.

## Theorem 4: Rank-Zero Arithmetic Product Average

Assume Theorem 1 in average-compatible form. Put

```text
H_c(u) = q_0 + sum_(gamma in Gamma) a_gamma e^(i gamma u).
```

Assume the H2 product form

```text
P_E,W(e^u) = exp(B_H2(E,W)) G(u)(1+eps_P(u)).
```

Assume `G` has dyadic mean coefficients

```text
d_eta = Mean_dyadic(G(u)e^(-i eta u)).
```

A sufficient joint-tail formulation is: there are finite exponential
truncations

```text
H_Y(u) = q_0 + sum_(gamma in Gamma(Y)) a_gamma e^(i gamma u),
G_Y(u) = sum_(eta in Lambda(Y)) d_eta e^(i eta u),
```

such that

```text
lim_(Y->infinity) limsup_(U->infinity)
  A_U( |H_c-H_Y| |G| + |H_Y| |G-G_Y| ) = 0,
```

the diagonal sums converge,

```text
D_Y =
 q_0 d_0
 + sum_(gamma in Gamma(Y), eta in Lambda(Y), gamma+eta=0)
     a_gamma d_eta
 -> D,
```

and the H1/H2 product errors are mean-small:

```text
A_U( |error_c(u)| |G(u)| ) -> 0,
A_U( |H_c(u)G(u)| |eps_P(u)| ) -> 0,
```

with the obvious harmless replacement of `eps_P` by
`exp(eps_log_P)-1` if H2 is first proved logarithmically.

Then

```text
A_U(c_E,W(e^u)P_E,W(e^u))
 -> C_E,W^prod,
```

where

```text
C_E,W^prod
 = exp(B_H2(E,W))
   (q_0 d_0 + sum_(gamma in Gamma) a_gamma d_(-gamma)).
```

Equivalently,

```text
C_E,W^prod = exp(B_H2(E,W)) Mean_dyadic(H_c(u)G(u)).
```

In the nonoscillatory H2 special case `G=1`,

```text
d_0=1,
d_eta=0 for eta != 0,
C_E,W^prod = exp(B_H2(E,W)) q_0.
```

For repository-normalized kernels this becomes

```text
C_E,W^prod = exp(B_H2(E,W))/L(E,1).
```

This is an arithmetic average of the product. It is not a pointwise limit for
`c_E,W(e^u)`, and it is not determined by an averaged theorem for `log P`
alone.

## Optional Corollary: Pointwise Product Profile

If Theorem 1 holds pointwise and H2 holds pointwise in product form with
`eps_P(u)=o(1)`, then

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_H2(E,W)) H_c(u)G(u) + o(1)
```

provided the multiplication of H1 and H2 errors is controlled. In the
nonoscillatory H2 case this is

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_H2(E,W))(q_0+Z_c(u)) + o(1).
```

This is still an oscillatory profile, not stabilization.

## Proof Skeleton

H1 profile:

1. Prove Mellin inversion for the exact fixed `W`.
2. Shift the contour through legal heights for
   `exp(uz)W_hat(z)/L(E,1+z)`.
3. Compute the central residue:

   ```text
   Res_(z=0) exp(uz)W_hat(z)/L(E,1+z) = w_(-1)/L(E,1).
   ```

4. At simple offcentral zeros `1+i gamma`, compute

   ```text
   Res_(z=i gamma) exp(uz)W_hat(z)/L(E,1+z)
    = W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma).
   ```

5. Combine equal frequencies and conjugate pairs.
6. Exclude, kill, cancel, or explicitly retain every multiple-zero or
   positive-degree polynomial-exponential term.
7. Use the reciprocal-zero tail and legal-height contour bound to get `o(1)`.

H2:

1. Expand the exact good local logarithm through order two.
2. Rewrite the quadratic term using `chi_sym2(p)=a_p^2/p-1`.
3. Keep all five terms:
   `S1_W`, `(1/2)Ssym_W`, `-(1/2)Mgood_W`, `Rge3_W`, `Bbad_W`.
4. Insert finite-part/profile hypotheses and define `B_H2`.
5. If an H2 oscillatory term remains, exponentiate only under a product-form
   error hypothesis.

Product average:

1. Multiply

   ```text
   c_E,W(e^u)P_E,W(e^u)
    = exp(B_H2)H_c(u)G(u) + mean-small error.
   ```

2. Replace `H_c` and `G` by finite exponential truncations.
3. Average finite exponentials:

   ```text
   A_U(e^(i omega u)) -> 1 if omega=0,
   A_U(e^(i omega u)) -> 0 if omega!=0.
   ```

4. Keep exactly the diagonal terms `gamma+eta=0`.
5. Pass to infinite profiles using the joint-tail hypothesis.

## Remaining Assumptions

The section is claim-safe only if these are theorem hypotheses or proved
before publication:

- exact fixed-kernel H1 Mellin/Perron identity;
- legal finite-height H1 contour shift for the same `W`;
- reciprocal derivative or Laurent coefficient control at offcentral zeros;
- exclusion, cancellation, kernel killing, or explicit retention of rank-zero
  positive-degree multiple-zero terms;
- pointwise or mean convergence mode for the reciprocal-zero profile;
- endpoint-smoothed H2 finite parts for `S1_W`, `Ssym_W`, and `Mgood_W`, or a
  declared H2 product-form profile replacing them;
- control of exponentiating H2 logarithmic errors;
- mean coefficients of `G=exp(Z_P)`, not merely mean coefficients of `Z_P`;
- joint H1/H2 diagonal and offdiagonal tail extraction;
- product-error smallness in the same arithmetic averaging mode.

## No-Promotion Language

Safe:

```text
For analytic rank zero, under explicit reciprocal-residue and contour-tail
hypotheses, H1 has an oscillatory profile
c_E,W(e^u)=1/L(E,1)+Z_c(u)+o(1). Separately, under H2 product-form and joint
tail hypotheses, the dyadic arithmetic average of c_E,W(e^u)P_E,W(e^u) has the
diagonal constant C_E,W^prod.
```

Unsafe:

```text
c_E,W(e^u) -> 1/L(E,1).
The rank-zero fixed-curve EC smoothing product stabilizes pointwise.
The product-average theorem follows from an averaged-log theorem for P.
Finite kernel filtering proves the fixed natural-kernel theorem.
The arithmetic product average is unconditional for EC.
```
