---
schema_version: 1
title: "Rank-zero product-average package"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.79
dependencies:
  - handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md
tags: [ec-ndc, h1, rank-zero, product-average]
---

# Rank-Zero Product-Average Package

Confidence: 0.79.

Dependencies:

- `handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md`

## Do Not Promote Unless

- Rank zero H1 is stated as `Q_0 + Z_c(u) + o(1)`, not as a pointwise constant,
  unless every nonzero H1 residue is killed, cancelled, filtered with tail
  control, subtracted, or averaged in the same theorem mode.
- Pointwise profile mode and product-average mode stay separate.
- The H1 contour shift, height avoidance, indentation, and contour tails are
  proved for the same fixed kernel and Mellin normalization.
- The reciprocal-zero series has a declared convergence mode. For the pointwise
  theorem below, use uniform convergence of symmetric truncations or a stronger
  explicit tail bound.
- Multiple offcentral zeros are absent, coefficient-killed, or retained as
  polynomial-exponential profile terms. In rank zero, any retained degree
  `j >= 1` term is growing and blocks bounded pointwise/profile constants.
- Product averaging averages `c_E,W(e^u) P_E,W(e^u)` itself in dyadic log
  windows. It is not an averaged-log or geometric-mean theorem.
- The product-average constant includes `d_0` and every matching-frequency
  diagonal `a_gamma d_(-gamma)`.
- H2 input supplies mean coefficients of `G(u)=exp(Z_P(u))`, not only mean
  coefficients of `Z_P(u)` or `log P`.
- No external theorem is cited unless accompanied by the mandatory packet:
  `curl + pdftotext + short verbatim quote + page/equation`.

External theorem citations: none. This package uses only local residue algebra
and theorem scaffolds from the dependency files above.

## Normalization

Fix an elliptic curve `E/Q`, a fixed admissible kernel `W`, and

```text
u = log K,
r = ord_(s=1) L(E,s).
```

The H1 object is normalized as

```text
c_E,W(K)
 = (1/(2 pi i)) int_(Re z=sigma)
     K^z W_hat(z) / L(E,1+z) dz.
```

This package is the rank-zero case:

```text
r = 0,
L(E,1) != 0,
W_hat(z) = w_(-1)/z + holomorphic at z=0.
```

Repository-normalized kernels have `w_(-1)=1`.

## Exact H1 Profile

The central rank-zero residue is

```text
Q_0
 = Res_(z=0) e^(uz) W_hat(z)/L(E,1+z)
 = w_(-1)/L(E,1).
```

For normalized kernels:

```text
Q_0 = 1/L(E,1).
```

For a simple offcentral zero

```text
rho = 1 + i gamma,
gamma != 0,
L(rho)=0,
L'(rho) != 0,
```

the H1 reciprocal-pole residue is

```text
a_gamma e^(i gamma u),
a_gamma = W_hat(i gamma)/L'(E,1+i gamma).
```

After combining equal frequencies, define

```text
Z_c(u) = sum_(gamma != 0) a_gamma e^(i gamma u).
```

For real `W` and real-coefficient symmetry,

```text
a_(-gamma) = conjugate(a_gamma),
a_gamma e^(i gamma u) + a_(-gamma)e^(-i gamma u)
 = 2 Re(a_gamma e^(i gamma u)).
```

Uniform pointwise mode means symmetric truncations

```text
Z_T(u) = sum_(0<|gamma|<=T) a_gamma e^(i gamma u)
```

converge uniformly, for example under the explicit tail condition

```text
A(T) = sum_(|gamma|>T) |a_gamma| -> 0.
```

## Theorem A: Rank-Zero Pointwise Profile

Assume:

```text
H1-contour:
  finite-height H1 contour shift holds for admissible T:
  c_E,W(e^u) = Q_0 + Z_T(u) + I_T(u).

H1-simple-or-retained:
  every offcentral term not in Z_T is absent, killed, or placed in an
  explicit polynomial-exponential profile.

H1-uniform-zero-tail:
  A(T)=sum_(|gamma|>T)|a_gamma| -> 0.

H1-contour-tail:
  there is admissible T(u)->infinity with |I_(T(u))(u)| + A(T(u)) -> 0.
```

Then

```text
c_E,W(e^u)
 = w_(-1)/L(E,1)
   + sum_(gamma != 0)
       W_hat(i gamma) e^(i gamma u) / L'(E,1+i gamma)
   + o(1),
```

with the zero series converging uniformly in `u`.

For normalized kernels:

```text
c_E,W(e^u) = 1/L(E,1) + Z_c(u) + o(1).
```

This is a pointwise profile theorem. It is not a constant-limit theorem.

### Constant Special Case

A pointwise rank-zero constant follows only after an added theorem proves

```text
a_gamma = 0 for every retained gamma != 0
```

or proves exact same-frequency cancellation, full tail-killing by a filtered
kernel, explicit subtraction, or an averaging theorem. Without this added
mechanism, any nonzero `a_gamma` survives at constant scale.

Direct coefficient test: if a uniformly convergent nonzero-frequency profile
`Z_c(u)` had limit `0`, then for each retained `lambda != 0`,

```text
a_lambda
 = lim_(U->infinity) (1/U) int_0^U Z_c(u)e^(-i lambda u) du
 = 0.
```

Thus a nonzero simple residue cannot be hidden in `o(1)`.

## Product-Average Mode

This is a different theorem mode. Define the dyadic logarithmic product
average

```text
A_U^prod(F)
 = (1/U) int_U^(2U) F(u) du
 = (1/U) int_exp(U)^exp(2U) F(log K) dK/K.
```

The target is the arithmetic average

```text
A_U^prod(c_E,W(e^u) P_E,W(e^u)).
```

It is not

```text
exp(A_U^prod(log(c_E,W(e^u)P_E,W(e^u)))).
```

For Agent 3 H2 factors,

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)),
```

with

```text
A_p(1) = 1 - a_p/p + 1/p    for good p,
A_p(1) = 1 - a_p/p          for bad p.
```

The exact H2 finite-part constant is imported only in the bookkeeping form

```text
B_H2(E,W)
 = C1_E,W
   + (1/2) Csym_E,W
   - (1/2) CM_E,W
   + Cge3_E
   + Bbad_E,
```

where these constants are the finite parts of `S1_W`, `Ssym_W`, `Mgood_W`,
`Rge3_W`, and the bad-prime term in
`H2_POINTWISE_THEOREM_PACKAGE.md`.

In rank zero the product-mode H2 input should be written

```text
P_E,W(e^u)
 = exp(B_H2(E,W)) G(u)(1 + eps_P(u)),
G(u) = exp(Z_P(u)).
```

Mean coefficients are coefficients of `G`, not of `Z_P`:

```text
d_eta = Mean_dyadic(G(u)e^(-i eta u)).
```

## Theorem B: Rank-Zero Product Arithmetic Average

Assume Theorem A in average-compatible form, and write

```text
H_c(u) = q_0 + sum_(gamma != 0) a_gamma e^(i gamma u),
q_0 = w_(-1)/L(E,1).
```

Assume:

```text
P-product-form:
  P_E,W(e^u)=exp(B_H2(E,W))G(u)(1+eps_P(u)).

H2-mean-coefficients:
  G(u) has dyadic mean coefficients d_eta.

Joint-tail:
  finite truncations H_Y and G_Y approximate H_c and G well enough in
  dyadic product mean to pass zero-frequency extraction to the limit.

Product-error-small:
  A_U^prod(|H_c(u)G(u)| |eps_P(u)|) -> 0,
  and the H1 contour/profile errors are product-mean small.

No-growing-H1:
  no rank-zero offcentral H1 term with polynomial degree j>=1 survives in the
  unrenormalized average.
```

Then

```text
A_U^prod(c_E,W(e^u) P_E,W(e^u))
 -> C_E,W^prod,
```

where the diagonal constant is

```text
C_E,W^prod
 = exp(B_H2(E,W))
   (q_0 d_0 + sum_(gamma != 0) a_gamma d_(-gamma)).
```

Equivalently,

```text
C_E,W^prod
 = exp(B_H2(E,W)) Mean_dyadic(H_c(u)G(u)).
```

If H2 is pointwise nonoscillatory in the product mode, then `G=1`, `d_0=1`,
and `d_eta=0` for `eta != 0`, so

```text
C_E,W^prod = exp(B_H2(E,W)) w_(-1)/L(E,1).
```

For normalized kernels this becomes

```text
C_E,W^prod = exp(B_H2(E,W)) / L(E,1).
```

This last display is an arithmetic product-average constant. It is not a
pointwise constant limit for `c_E,W(e^u)`.

## Dependency Graph

```text
H1 Mellin normalization
  -> finite-height contour shift and height avoidance
  -> central residue Q_0 = w_(-1)/L(E,1)
  -> offcentral simple residues a_gamma = W_hat(i gamma)/L'(E,1+i gamma)
  -> reciprocal-zero tail and contour-tail control
  -> Theorem A: Q_0 + Z_c(u) + o(1)

Theorem A in average-compatible form
  + exact Agent 3 H2 local decomposition
  + H2 finite part B_H2(E,W)
  + mean coefficients of G(u)=exp(Z_P(u))
  + joint H1/H2 diagonal extraction
  -> Theorem B: product arithmetic average with C_E,W^prod

Missing proof/source inputs
  -> fixed-curve H1 contour tails
  -> reciprocal derivative or Laurent coefficient control
  -> multiple-zero handling
  -> H2 S1/Sym2/Mgood finite parts
  -> joint infinite-frequency mean extraction
```

## Proof Skeleton

Pointwise profile:

1. Start from the finite-height H1 contour formula in the same `W` and Mellin
   convention.
2. Compute the central residue at `z=0`: `Q_0=w_(-1)/L(E,1)`.
3. Compute each simple offcentral reciprocal-pole residue:
   `a_gamma e^(i gamma u)`.
4. Combine equal frequencies and conjugate pairs.
5. Prove the zero-series convergence mode, e.g. `A(T)->0`.
6. Choose admissible `T(u)->infinity` so `|I_T(u)|+A(T)->0`.
7. Conclude `c_E,W(e^u)=Q_0+Z_c(u)+o(1)`.
8. Add the coefficient test to forbid a constant limit unless all retained
   nonzero-frequency coefficients vanish.

Product average:

1. Normalize H1 to the mean-scale rank-zero profile `H_c(u)`.
2. Insert the exact H2 product form
   `P=exp(B_H2)G(1+eps_P)`.
3. Prove product-mean smallness for H1 and H2 errors.
4. Approximate `H_c` and `G` by finite exponential sums.
5. Average finite terms:

   ```text
   A_U^prod(e^(i(gamma+eta)u)) -> 1 if gamma+eta=0,
   A_U^prod(e^(i(gamma+eta)u)) -> 0 if gamma+eta!=0.
   ```

6. Pass to infinite sums using the joint-tail hypothesis.
7. Collect the diagonal terms
   `q_0 d_0 + sum_gamma a_gamma d_(-gamma)`.

## Multiple-Zero Caveat

If an offcentral zero `rho=1+i gamma` has multiplicity `m>1`, H1 can contribute

```text
e^(i gamma u) P_rho(u),
deg P_rho <= m-1.
```

In rank zero, any nonzero degree `>=1` term grows. The theorem package above
therefore requires such terms to be ruled out, killed by kernel zeros or
coefficient cancellations, explicitly retained as a growing profile, or moved
to a separate renormalized/finite-part theorem.

## Paper Section Path

Use this as a self-contained section in an EC smoothing paper, after the H1
reciprocal-Perron contour section and before any H1/H2 composition theorem:

```text
Section: Rank-Zero Residues and Product Averages

1. H1 normalization and rank-zero central residue.
2. The rank-zero oscillatory profile theorem.
3. Lemma: no pointwise constant without coefficient death or averaging.
4. Product-average mode and dyadic log-Cesaro measure.
5. H2 product-form input and B_H2 bookkeeping.
6. Product arithmetic-average theorem and diagonal constant.
7. Promotion caveats and citation obligations.
```

Suggested local source map:

```text
H1 contour/residue setup:
  handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md

Rank-zero profile:
  handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md

Product arithmetic average:
  handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md

H2 constant bookkeeping:
  handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
```

Do not insert this into the current Farey/Mertens paper as a proved theorem.
It belongs to a guarded EC smoothing section or appendix unless the listed
analytic and citation dependencies close.

## Claim-Safe Summary

Allowed:

```text
Rank-zero H1 has a conditional pointwise oscillatory profile
Q_0 + Z_c(u) + o(1). A separate arithmetic product-average theorem, under
joint H1/H2 mean extraction, has constant
exp(B_H2)(q_0 d_0 + sum a_gamma d_(-gamma)).
```

Forbidden:

```text
Rank-zero H1 stabilizes pointwise to 1/L(E,1).
Smoothing alone kills H1 reciprocal poles.
Averaged log P determines the arithmetic average of cP.
H2 branch damping transfers to H1 reciprocal poles.
The EC smoothing theorem is proved.
```

Changed file list:

- `handoff-2026-05-11-h1-breakthrough-proof-wave/RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md`
