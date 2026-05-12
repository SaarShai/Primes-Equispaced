---
schema_version: 1
title: "H2/Sym2 and product-average theorem package"
date: 2026-05-11
type: theorem-package
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.78
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
  - handoff-2026-05-11-h1-residue-control-wave/H2_SYM2_SOURCE_CLOSURE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md
tags: [ec-ndc, h2, sym2, product-average, theorem-package]
---

# H2/Sym2 And Product-Average Theorem Package

Status: `RIGOROUS_REDUCTION`.

Bottom line: no unconditional fixed-curve EC stabilization theorem is available
from the current files. No unconditional EC product-average theorem is
available either. The clean package is:

1. unconditional local H2 algebra for the exact Agent 3 product;
2. conditional H2 pointwise theorem from S1 and Sym2 finite-part inputs;
3. unconditional finite-exponential diagonal averaging lemma;
4. conditional arithmetic product-average theorem with an explicit diagonal
   constant;
5. conditional positive-rank fixed-curve theorem if H1 and H2 are both closed
   in pointwise mode.

All ranks below are analytic ranks

```text
r = ord_(s=1) L(E,s).
```

Using algebraic or script rank requires a separate rank-equality input.

## Objects

Fix an elliptic curve `E/Q`, a fixed admissible kernel `W`, and set

```text
u = log K.
```

Agent 3 local factors:

```text
A_p(1) = 1 - a_p/p + 1/p    if p is good,
A_p(1) = 1 - a_p/p          if p is bad.
```

The H2 product is

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)),
log P_E,W(K) = - sum_p W(p/K) log A_p(1),
```

with the positive real log branch used by the reproducer.

The H1 Perron object is

```text
c_E,W(K) = (1/(2 pi i)) int_(Re z=sigma)
             K^z W_hat(z) / L(E,1+z) dz,
```

with the same `W` and Mellin normalization. Repository-normalized kernels have
`W_hat(z)=1/z+O(1)` at `z=0`.

The arithmetic product average is

```text
A_U(F) = (1/U) int_U^(2U) F(u) du
       = (1/U) int_exp(U)^exp(2U) F(log K) dK/K.
```

It averages product values. It is not an averaged logarithm or a geometric
mean.

## Proposition 1: Exact H2 Local Algebra

For good primes set

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

Then

```text
log P_E,W(K)
 = S1_W(K)
   + (1/2) Ssym_W(K)
   - (1/2) Mgood_W(K)
   + Rge3_W(K)
   + Bbad_W(K).
```

Moreover the good-prime remainder is absolutely convergent:

```text
sum_(p good) |R_p| < infinity,
```

using the Hasse bound through the `m>=3` local-log expansion.

This proposition is algebraic/local. It is the only H2 component that is
unconditional in the present package. Omitting `Ssym_W` or `Mgood_W` loses the
exact coefficient.

Proof skeleton:

1. Factor the good local term as
   `(1-alpha_p/p)(1-beta_p/p)`.
2. Expand the logarithm:

   ```text
   -log(1-a_p/p+1/p)
    = a_p/p + (a_p^2-2p)/(2p^2) + R_p.
   ```

3. Rewrite

   ```text
   (a_p^2-2p)/(2p^2)
    = chi_sym2(p)/(2p) - 1/(2p).
   ```

4. Sum with `W(p/K)` over good primes and add the finite bad-prime term.

## Proposition 2: Conditional H2 Pointwise Limit

Let `kappa_sym` be the central order of the exact good-prime Sym2/adjoint
object used for `chi_sym2(p)=a_p^2/p-1`, with the convention:

```text
kappa_sym > 0  means zero,
kappa_sym = 0  means finite nonzero value,
kappa_sym < 0  means pole.
```

Assume the following finite-part inputs:

```text
S1_W(K)
 = (1/2 + kappa_sym/2 - r) log u
   + C1_E,W + e1(u),

Ssym_W(K)
 = -kappa_sym log u
   + Csym_E,W + esym(u),

Mgood_W(K)
 = log u + CM_E,W + eM(u),

Rge3_W(K)
 = Cge3_E + ege3(u),

Bbad_W(K)
 = Bbad_E + ebad(u),
```

with all errors `o(1)` as `u->infinity`.

Then

```text
log P_E,W(e^u)
 = -r log u + B_H2(E,W) + o(1),
```

where

```text
B_H2(E,W)
 = C1_E,W
   + (1/2) Csym_E,W
   - (1/2) CM_E,W
   + Cge3_E
   + Bbad_E.
```

Equivalently,

```text
P_E,W(e^u) = exp(B_H2(E,W)) u^(-r) (1+o(1)).
```

The coefficient check is exact:

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

If all five finite-part inputs have errors `O(u^(-eta))`, the H2 conclusion
has an `O(u^(-eta'))` rate for some `eta'>0`.

Proof skeleton: insert the five finite-part inputs into Proposition 1 and
collect the `log u` and constant terms.

Unresolved inputs for this proposition:

- endpoint-smoothed S1 branch continuation for
  `sum_(p good) W(p/K)a_p/p`;
- exact good-prime Sym2 finite part for `chi_sym2(p)=a_p^2/p-1`;
- source-verified or in-repo proof of `kappa_sym` for the exact convention, if
  a numeric value such as `0` is used;
- weighted zero/pole summability and shifted-contour tails;
- ordinary weighted prime-Mertens finite part for the same `W`;
- external citation packets for any theorem used to close the inputs.

## Proposition 3: Branch Criterion For H2 Offcentral Terms

This is a proof criterion, not a closed theorem.

Suppose the S1 or Sym2 prime Dirichlet series has only logarithmic branches in
the shifted strip. Near an offcentral singularity `rho != 1`, write

```text
D(1+z) = m_rho log(z-(rho-1)) + holomorphic.
```

If the contour shift and branch-cut calculation are valid, the corresponding
smoothed prime sum contribution is

```text
-(1/u) m_rho e^((rho-1)u) W_hat(rho-1)
 + O(u^(-2) e^((Re rho-1)u)
       (|W_hat(rho-1)|+|W_hat'(rho-1)|)).
```

Consequences:

- If all crossed offcentral singularities satisfy `Re rho<=1` and the
  displayed weighted zero/pole series is summable, the aggregate is `O(1/u)`.
- A zero on `Re rho=1`, `rho != 1`, gives a `1/u` branch term, not a
  persistent H2-scale oscillation.
- A singularity with `Re rho>1` breaks the pointwise H2 finite part unless it
  is explicitly cancelled or retained.

This criterion repairs the older persistent-H2-obstruction warning only after
the branch formula itself is proved. It does not apply to H1, where zeros of
`L(E,s)` are reciprocal poles of `1/L(E,s)`.

## Proposition 4: Unconditional Finite Diagonal Averaging

Let

```text
H(u) = sum_(gamma in Gamma) h_gamma e^(i gamma u),
G(u) = sum_(eta in Lambda) d_eta e^(i eta u),
```

where `Gamma` and `Lambda` are finite sets. Then

```text
lim_(U->infinity) A_U(HG)
 = sum_(gamma in Gamma, eta in Lambda, gamma+eta=0)
     h_gamma d_eta.
```

Proof:

```text
A_U(e^(i omega u)) = 1                         if omega=0,
A_U(e^(i omega u)) =
  (e^(2i omega U)-e^(i omega U))/(i omega U)    if omega!=0.
```

The offdiagonal terms vanish termwise. This proposition is unconditional, but
it is only finite exponential algebra. It is not an unconditional EC product
average until the H1/H2 profiles and infinite-tail passage are proved.

## Theorem 5: Conditional Arithmetic Product Average

Assume H1 has a mean-scale profile

```text
c_E,W(e^u)
 = u^r H_c(u) + error_c(u),

H_c(u) = q_r + sum_(gamma in Gamma_r) h_gamma e^(i gamma u),
```

where `q_r=1/L^(r)(E,1)` in the repository H1 normalization. For rank zero,
`Gamma_r` contains the retained simple reciprocal residues and
`h_gamma=W_hat(i gamma)/L'(E,1+i gamma)` when zeros are simple.

Assume H2 has product form

```text
P_E,W(e^u)
 = exp(B_H2(E,W)) u^(-r) G(u)(1+eps_P(u)),
```

where `G(u)=exp(Z_P(u))` admits dyadic mean coefficients

```text
d_eta = Mean_dyadic(G(u)e^(-i eta u)).
```

Assume the H1 error, H2 error, and tails in the infinite frequency expansions
are small in product mean, enough to pass Proposition 4 from finite truncations
to the limit.

Then

```text
A_U(c_E,W(e^u) P_E,W(e^u))
 -> C_E,W^prod,
```

with diagonal constant

```text
C_E,W^prod
 = exp(B_H2(E,W))
   (q_r d_0 + sum_(gamma in Gamma_r) h_gamma d_(-gamma)).
```

Special cases:

1. If H2 is pointwise nonoscillatory in product form, then `G=1`,
   `d_0=1`, and `d_eta=0` for `eta!=0`, so

   ```text
   C_E,W^prod = exp(B_H2(E,W)) q_r.
   ```

2. In rank zero with normalized kernels and nonoscillatory H2, this becomes

   ```text
   C_E,W^prod = exp(B_H2(E,W)) / L(E,1),
   ```

   as an arithmetic product average only. It is not a pointwise limit unless
   all retained H1 nonzero-frequency residues vanish, cancel, are filtered, or
   are explicitly subtracted.

Proof skeleton:

1. Multiply the H1 profile and H2 product form:

   ```text
   c_E,W(e^u)P_E,W(e^u)
    = exp(B_H2(E,W)) H_c(u)G(u) + mean-small error.
   ```

2. Approximate `H_c` and `G` by finite exponential sums.
3. Apply Proposition 4.
4. Pass to the infinite series using the joint-tail hypothesis.

Unresolved inputs:

- H1 finite-height contour shift and tail bounds for the exact fixed `W`;
- fixed-curve reciprocal derivative bounds for simple zeros, or Laurent
  coefficient control for multiple zeros;
- absence, cancellation, filtering, or retention of H1 terms with degree
  `j>r`;
- H2 Proposition 2 or an H2 product-form/profile replacement;
- mean coefficients of `G(u)=exp(Z_P(u))`, not merely means of `Z_P` or
  averaged `log P`;
- infinite diagonal/offdiagonal tail extraction.

## Theorem 6: Conditional Fixed-Curve Pointwise Stabilization

Assume `r>=1`. Assume H2 Proposition 2. Assume the H1 pointwise leading input

```text
c_E,W(e^u) = q_r u^r + o(u^r),
q_r = 1/L^(r)(E,1)
```

in the repository normalization. Equivalently, all offcentral H1 reciprocal
residue terms and contour errors are `o(u^r)` after combining lower central
powers.

Then

```text
c_E,W(e^u) P_E,W(e^u)
 -> exp(B_H2(E,W)) / L^(r)(E,1).
```

If the full Agent 3 proxy also includes the absolutely convergent `L(E,2)^r`
tail and the external `zeta(2)` factor in the existing normalization, and if
the rank in that denominator is the same analytic rank `r`, then the fixed
curve proxy limit is

```text
zeta(2) exp(B_H2(E,W))
  / (L^(r)(E,1) L(E,2)^r).
```

Rank zero is not covered by this pointwise theorem. For `r=0`, the honest H1
shape is

```text
c_E,W(e^u) = 1/L(E,1) + Z_c(u) + o(1),
```

unless all retained nonzero H1 residues are killed or cancelled. Use Theorem 5
for the product-average mode, or retain the oscillatory profile pointwise.

Proof skeleton:

1. H2 gives `P_E,W(e^u)=exp(B_H2)u^(-r)(1+o(1))`.
2. H1 gives `c_E,W(e^u)=q_r u^r+o(u^r)`.
3. Multiply and cancel `u^r` against `u^(-r)`.
4. Add the absolutely convergent `L(E,2)^r` and `zeta(2)` factors only after
   their separate tail input is stated.

## Current Promotion Boundary

Allowed statements:

```text
Exact H2 local algebra is closed for the Agent 3 factors.
H2 pointwise closure is conditional on S1 branch continuation and exact Sym2
finite parts.
Finite diagonal averaging is unconditional for finite exponential sums.
The EC product-average theorem is conditional on H1/H2 profiles plus joint
tail extraction.
Positive-rank fixed-curve stabilization is conditional on separate H1
reciprocal-pole control and H2 finite-part closure.
```

Forbidden statements:

```text
The fixed-curve EC theorem is proved.
The arithmetic product average is unconditional for EC.
An averaged log of P determines A_U(cP).
H2 branch damping controls H1 reciprocal poles.
Rank-zero pointwise stabilization follows from smoothing.
The Sym2 finite part is closed just from adjacent automorphy facts.
```

## Minimal Next Inputs

To convert this package into a theorem, close these in order:

1. H2 S1 branch continuation for the endpoint-smoothed fixed `W`.
2. H2 exact good-prime Sym2 finite part for
   `chi_sym2(p)=a_p^2/p-1`, including `kappa_sym` convention/value.
3. H1 finite-height reciprocal-Perron contour theorem with shifted-line and
   height tails.
4. H1 fixed-curve reciprocal derivative/Laurent control, or explicit
   profile/average retention.
5. Joint product-average tail theorem for `H_c(u)G(u)` if using Theorem 5.
6. Rank equality if any external-facing statement uses algebraic rank.
7. Source packets for every external theorem: `curl + pdftotext + short quote
   + page/equation`.
