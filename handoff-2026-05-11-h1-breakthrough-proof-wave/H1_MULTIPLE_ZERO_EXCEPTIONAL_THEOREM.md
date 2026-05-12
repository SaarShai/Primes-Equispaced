---
schema_version: 1
title: "H1 multiple-zero exceptional theorem package"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
dependencies:
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
  - handoff-2026-05-11-h1-residue-control-wave/RESIDUE_CONTROL_ADVERSARIAL_REFEREE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
tags: [ec-ndc, h1, multiple-zeros, reciprocal-residues, exceptional-profile]
---

# H1 Multiple-Zero Exceptional Theorem Package

## Do Not Promote Unless

- The fixed-kernel Mellin/Perron identity and finite-height contour shift are
  proved for the exact `W`, including original-line, horizontal, shifted-line,
  indentation, truncation, and height-avoidance errors.
- Every crossed zero with `Re(rho)>1` is either ruled out or retained as an
  exponentially growing exceptional term. It cannot be absorbed into any
  polynomial central error.
- The reciprocal Laurent coefficients
  `b_(rho,-j)` are bounded, summed, or truncated in the same mode as the
  contour shift. Mellin decay of `W_hat` alone is not residue control.
- Kernel derivative decay is stated through the highest derivative appearing
  in every multiple-zero residue.
- Effective degrees are computed after kernel zeros and exact same-exponent
  coefficient cancellations. Generic degree `m-1-h` is not enough if a
  cancellation theorem is being used.
- For pointwise positive rank, every critical-line exceptional degree
  `>= r` is killed, cancelled, retained in the theorem, or moved to a proved
  averaged/finite-part mode.
- For rank zero, nonzero simple residues are stated as profile/average terms.
  They are not hidden in `o(1)`.
- Ordinary averaging is used only for terms it actually controls. Polynomial
  terms of normalized positive degree require subtraction, finite part, or a
  stronger averaging theorem.
- H2 is composed only in the same mode: pointwise, oscillatory profile,
  arithmetic average, geometric/log average, or finite part.
- External theorem citations: none in this file. Any future source used to
  discharge a hypothesis must follow the repository protocol:
  `curl + pdftotext + short quote + page/equation`.

## Theorem Object

Use the H1 normalization

```text
c_E,W(e^u)
 = (1/(2 pi i)) int_(Re z=sigma)
     e^(u z) W_hat(z)/L(E,1+z) dz,
u = log K,
r = ord_(s=1) L(E,s).
```

Shift to `Re z=-eta`. Let `Omega` be the crossed noncentral zeros
`rho != 1` of `L(E,s)`, with

```text
z_rho = rho - 1,
m_rho = ord_(s=rho) L(E,s).
```

Assume the finite-height contour identity of the dependency files and a
declared convergence mode for the zero sums and contour remainders.

## Central Polynomial

At `z=0`, write

```text
1/L(E,1+z) = sum_(j=-r)^infty a_j z^j,
W_hat(z)  = sum_(m=-1)^infty w_m z^m.
```

The central residue is

```text
Q_r(u) = Res_(z=0) e^(u z) W_hat(z)/L(E,1+z)
       = sum_(ell=0)^r C_ell u^ell,

C_ell = (1/ell!) sum_(h=0)^(r-ell)
          a_(-r+h) w_(r-ell-h-1).
```

The top coefficient is

```text
C_r = w_-1/L^(r)(E,1).
```

For repository-normalized kernels, `w_-1=1`, so

```text
Q_r(u) = u^r/L^(r)(E,1) + O(u^(r-1)).
```

The central polynomial depends on

```text
L^(r)(E,1), ..., L^(2r)(E,1)
and
w_-1, ..., w_(r-1).
```

## Offcentral Laurent Algebra

For `rho in Omega`, write locally

```text
1/L(E,1+z)
 = sum_(j=1)^(m_rho) b_(rho,-j)(z-z_rho)^(-j) + holomorphic.
```

If

```text
L(E,s) = sum_(n=m_rho)^infty ell_(rho,n)(s-rho)^n,
ell_(rho,n)=L^(n)(E,rho)/n!,
```

then

```text
b_(rho,-m_rho) = 1/ell_(rho,m_rho)
               = m_rho!/L^(m_rho)(E,rho),

b_(rho,-m_rho+h)
 = -(1/ell_(rho,m_rho))
    sum_(nu=1)^h ell_(rho,m_rho+nu)
      b_(rho,-m_rho+h-nu).
```

Thus the degree-`ell` offcentral coefficient depends on the Laurent
coefficients `b_(rho,-j)` with `j>=ell+1` and on kernel derivatives
`W_hat^(a)(z_rho)` with `0<=a<=m_rho-1-ell`.

## Exceptional Terms

The exact residue of `rho` is

```text
R_rho(u)
 = e^(u z_rho)
   sum_(j=1)^(m_rho) b_(rho,-j)
     sum_(ell=0)^(j-1)
       u^ell/ell! *
       W_hat^(j-1-ell)(z_rho)/(j-1-ell)!.
```

Equivalently,

```text
R_rho(u) = e^(u z_rho) P_rho(u),
P_rho(u)=sum_(ell=0)^(m_rho-1) A_(rho,ell) u^ell,

A_(rho,ell)
 = (1/ell!) sum_(j=ell+1)^(m_rho)
     b_(rho,-j) W_hat^(j-1-ell)(z_rho)/(j-1-ell)!.
```

For a simple zero,

```text
R_rho(u) = e^(u z_rho) W_hat(z_rho)/L'(E,rho).
```

For a critical-line simple zero `rho=1+i gamma`,

```text
R_rho(u) = e^(i gamma u) W_hat(i gamma)/L'(E,1+i gamma).
```

Let

```text
h_rho = ord_(z=z_rho) W_hat(z).
```

If `h_rho>=m_rho`, the pole is kernel-cancelled. If `h_rho<m_rho`, the generic
individual degree is

```text
d_rho = m_rho - 1 - h_rho,
```

with leading term

```text
e^(u z_rho)
 b_(rho,-m_rho) W_hat^(h_rho)(z_rho)
 u^d_rho /(h_rho! d_rho!).
```

The effective degree used in theorem statements is not the generic degree. It
is

```text
D_alpha = max {ell : A_(alpha,ell)^net != 0},
```

after grouping all terms with the same exponent `alpha=z_rho` and after all
declared coefficient cancellations. For critical-line real profiles, conjugate
pairs are grouped as the real oscillation at frequencies `+-gamma`; they
cancel only when the net coefficient is zero.

## Clean Exceptional-Term Theorem

Assume:

```text
H1-contour:
  the finite-height contour shift is valid and its tails are controlled in
  the declared mode;

H1-zero-sums:
  the simple-zero and multiple-zero residue sums converge absolutely,
  by principal value, by a specified T(u), or in a stated averaged/profile
  topology;

H1-laurent:
  all coefficient sums involving
  b_(rho,-j) W_hat^(a)(z_rho)
  that occur in the retained degrees are controlled;

H1-left:
  residues with Re(z_rho)<0 and the shifted contour are lower order in the
  target mode;

H1-exp:
  residues with Re(z_rho)>0 are absent, cancelled, or explicitly retained.
```

Then, in that same mode,

```text
c_E,W(e^u)
 = Q_r(u)
   + Z_simple(u)
   + Z_mult(u)
   + Z_exp(u)
   + I_H1(u),
```

where

```text
Z_simple(u)
 = sum_(rho simple, Re z_rho=0, rho!=1)
     e^(u z_rho) W_hat(z_rho)/L'(E,rho),

Z_mult(u)
 = sum_(rho multiple, Re z_rho=0)
     e^(u z_rho) P_rho(u),

Z_exp(u)
 = sum_(rho, Re z_rho>0)
     e^(u z_rho) P_rho(u),
```

and `I_H1(u)` contains the shifted-line remainder, decaying left-strip
residues if not retained, and the truncation/tail error. This is the honest H1
statement: multiple offcentral zeros appear as explicit
polynomial-exponential terms.

## Positive-Rank Closure

For `r>=1`, the central-only H1 asymptotic

```text
c_E,W(e^u) = Q_r(u) + o(u^r)
```

follows from the theorem package if:

```text
1. Z_exp(u)=0, or every exponential-growth term is outside the central-only
   claim;
2. every critical-line effective degree satisfies D_alpha < r;
3. the aggregate of degree < r terms is O(u^(r-1)) or otherwise o(u^r);
4. I_H1(u)=o(u^r).
```

Sufficient absolute conditions are

```text
sum_alpha |A_(alpha,ell)^net| < infinity
for every retained critical-line degree 0<=ell<r,
```

plus no uncancelled degree `ell>=r`.

With derivative decay

```text
|W_hat^(a)(i t)| <= C_a (1+|t|)^(-q_a),
```

zero counting `N(T,2T)<=C T log T`, bounded multiplicity `m<=M`, and pointwise
Laurent growth

```text
|b_(rho,-j)| <= C_j |gamma|^A_j (log(2+|gamma|))^B_j,
```

absolute convergence of degree `ell<r` follows from the shell criterion

```text
q_(j-1-ell) > A_j + 1
for every ell<r and j>=ell+1.
```

A mean-square Laurent substitute

```text
sum_(T<|gamma|<=2T) |b_(rho,-j)|^2
 <= C_j T^theta_j (log T)^B_j
```

suffices when

```text
theta_j < 2 q_(j-1-ell) - 1.
```

If these hold and H2 is separately proved pointwise as
`P_E,W(e^u)=exp(B_E,W)u^(-r)(1+o(1))`, then the product central limit candidate
is

```text
c_E,W(e^u)P_E,W(e^u)
 -> exp(B_E,W) w_-1/L^(r)(E,1).
```

## Profile And Average Cases

If `r>=1` and some critical-line term has `D_alpha=r`, central-only pointwise
closure fails, but an oscillatory product profile can still be honest:

```text
u^(-r)c_E,W(e^u)
 = w_-1/L^(r)(E,1)
   + sum_(D_alpha=r) A_(alpha,r)^net e^(alpha u)
   + o(1),
```

provided all `D_alpha>r` and all `Re(alpha)>0` terms are absent, cancelled,
subtracted, or separately retained with growth.

For rank zero,

```text
Q_0 = w_-1/L(E,1).
```

A nonzero simple critical-line residue gives the honest profile

```text
c_E,W(e^u)
 = w_-1/L(E,1)
   + sum_(gamma != 0)
       W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)
   + multiple-zero terms
   + o(1),
```

in the same convergence mode. If the simple-zero series is absolutely
convergent, its logarithmic/Cesaro mean is zero after justifying passage of the
average through the series. Thus rank zero may become an averaged theorem with
central H1 mean `w_-1/L(E,1)`.

Rank-zero multiple zeros with effective degree `D_alpha>=1` are not killed by
ordinary first averaging of `c_E,W(e^u)`. They require explicit subtraction,
finite part, stronger averaging, kernel cancellation, or a theorem that keeps
the growing polynomial-exponential profile.

## Impossible Claims

The following theorem forms are impossible under the displayed package unless
the listed obstruction is separately removed.

```text
Pointwise central H1, any rank:
  impossible if any uncancelled Re(z_rho)>0 term is omitted.

Pointwise central H1, r>=1:
  impossible if an uncancelled critical-line effective degree D_alpha>=r is
  omitted from the theorem.

Pointwise constant H1, r=0:
  impossible if any nonzero critical-line simple residue or multiple-zero
  term survives.

Ordinary averaged rank-zero H1:
  impossible from this package alone if a surviving critical-line term has
  effective degree >=1.

Product stabilization:
  impossible if H1 and H2 are proved in mismatched modes, or if H1 retains a
  degree-r profile while the final statement claims a constant.
```

Finite examples, zero-counting alone, simple-zero assertions alone, or kernel
decay alone do not remove these obstructions.

## Minimal Promotion Inputs

To upgrade this reduction, supply:

```text
1. fixed-kernel H1 contour theorem with quantified tails;
2. zero-free or explicit-treatment statement for Re(rho)>1 crossed zeros;
3. reciprocal derivative bounds for simple zeros;
4. Laurent coefficient bounds for multiple zeros;
5. kernel derivative decay through all required orders;
6. exact effective-degree audit after kernel zeros and coefficient
   cancellations;
7. same-mode H2 closure before product composition.
```
