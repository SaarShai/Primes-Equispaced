---
schema_version: 1
title: "H1 positive-rank reciprocal residue closure"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
dependencies:
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
  - handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
  - handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
tags: [ec-ndc, h1, positive-rank, reciprocal-residues, rigorous-reduction]
---

# H1 Positive-Rank Closure

## Do Not Promote Unless

- The exact H1 Perron shift for the chosen `W` is proved, including height
  sequence, indentations, offcentral residues, and contour tails.
- The offcentral aggregate satisfies `Z_c(u)+I(u)=o(u^r)` for analytic rank
  `r>=1`, or every non-`o(u^r)` term is retained in an oscillatory theorem.
- Any simple-zero claim is paired with bounded aggregate, absolute convergence,
  reciprocal-derivative bounds, or a source-checked substitute.
- Every multiple zero has effective residue degree `< r`, unless its leading
  coefficients cancel, the kernel kills it, it is retained, or the theorem is
  averaged with proof.
- Kernel decay is stated for every Mellin derivative used by multiple-zero
  residues, not only for `W_hat(it)`.
- The central coefficient is `w_-1/L^(r)(E,1)`, normalized to
  `1/L^(r)(E,1)` when `w_-1=1`; do not restore the cancelled factorial.
- H2 is closed in the same pointwise/oscillatory/averaged mode before product
  stabilization is claimed.
- No BSD, algebraic-rank substitution, cross-curve universality, or finite
  diagnostic evidence is used as theorem input.

Citation protocol: no external theorem is cited as fact here. All analytic
inputs below are hypotheses or local dependencies. Any future external theorem
used to discharge a hypothesis needs the repository protocol:
`curl + pdftotext + short quote + page/equation`.

## Verdict

For analytic rank `r>=1`, positive-rank H1 closes conditionally under the
minimal pointwise condition

```text
Z_c(u)+I(u)=o(u^r),          u=log K,
```

where `Z_c` is the offcentral reciprocal-residue aggregate and `I` is the
post-residue contour remainder. This is exactly the H1 input needed for H1/H2
composition.

A clean sufficient package is:

```text
all uncancelled offcentral residue polynomial degrees are < r,
and every coefficient aggregate of degrees 0,...,r-1 is bounded
or absolutely convergent,
and the shifted contour tail is o(u^r).
```

This closes positive rank as a theorem candidate with explicit hypotheses. It
does not close the fixed-curve theorem from current sources because reciprocal
derivative/Laurent coefficient bounds and the exact contour theorem remain
undischarged.

## Local Residue Algebra

Let

```text
c_E,W(e^u) = (1/(2 pi i)) int e^(uz) W_hat(z)/L(E,1+z) dz,
r = ord_(s=1) L(E,s).
```

For an offcentral zero `rho=1+i gamma`, `gamma != 0`, of multiplicity `m`,
write near `z0=i gamma`

```text
1/L(E,1+z) = sum_(j=1)^m b_(rho,-j) (z-z0)^(-j) + holomorphic.
```

The H1 residue is

```text
R_rho(u) = e^(i gamma u) sum_(ell=0)^(m-1) c_(rho,ell) u^ell,

c_(rho,ell)
 = (1/ell!) sum_(j=ell+1)^m
     b_(rho,-j) W_hat^(j-1-ell)(i gamma)/(j-1-ell)!.
```

For a simple zero this reduces to

```text
R_rho(u) = e^(i gamma u) W_hat(i gamma)/L'(rho).
```

If `W_hat` has zero order `nu_rho` at `i gamma`, then generically

```text
deg R_rho = m - 1 - nu_rho
```

until same-frequency cancellations lower it. If `nu_rho>=m`, that pole is
kernel-cancelled.

## Weakest Exact Condition

After combining all zeros with the same ordinate and choosing the admissible
Perron truncation, write

```text
Z_c(u) = sum_(ell>=0) u^ell Z_ell(u),
Z_ell(u) = sum_gamma c_(gamma,ell) e^(i gamma u).
```

The exact positive-rank pointwise H1 requirement is

```text
sum_(ell>=0) u^ell Z_ell(u) + I(u) = o(u^r).        (H-min-r)
```

This is weakest but tautological. For promotion, use the checkable sufficient
version:

```text
(H-deg)  Z_ell is identically zero, retained, or averaged for every ell>=r.
(H-bd)   Z_ell(u)=O(1) for 0<=ell<r.
(H-tail) I(u)=o(u^r).
```

Then `Z_c(u)=O(u^(r-1))=o(u^r)`.

At the absolute-convergence level, `(H-bd)` is implied by

```text
sum_gamma |c_(gamma,ell)| < infinity,     0<=ell<r.       (H-abs-r)
```

This is the simplest promotable positive-rank residue-control theorem.

## Simple-Zero Closure

If all relevant offcentral zeros are simple, then only `ell=0` occurs:

```text
Z_0(u) = sum_(gamma != 0)
  W_hat(i gamma) L'(1+i gamma)^(-1) e^(i gamma u).
```

For every `r>=1`,

```text
Z_0(u)=O(1)        implies        Z_0(u)=o(u^r).
```

Absolute convergence is sufficient:

```text
sum_(gamma != 0) |W_hat(i gamma)/L'(1+i gamma)| < infinity.
```

With zero counting `N(T,2T) <= C T log T` and kernel decay

```text
|W_hat(i t)| <= C (1+|t|)^(-q),
```

the following shell hypotheses imply absolute convergence:

```text
pointwise: |L'(1+i gamma)|^(-1) <= C |gamma|^A,   A < q-1;

mean-square:
  sum_(T<|gamma|<=2T) |L'(1+i gamma)|^(-2)
    <= C T^theta (log T)^B,                       theta < 2q-1.
```

For the local smoothstep decay `q=2`, these become `A<1` or
`theta<3`. These are hypotheses, not sourced facts.

## Multiple-Zero Constraints

For a finite nonzero residue term `u^ell e^(i gamma u)`:

```text
ell < r     harmless after H2 normalization;
ell = r     constant-scale oscillation, blocks pointwise central limit;
ell > r     grows after H2 normalization.
```

Thus the generic multiplicity condition is

```text
m - 1 - nu_rho < r,
equivalently m <= r + nu_rho.
```

Danger starts at

```text
m >= r + nu_rho + 1.
```

This is only generic because exact same-frequency cancellation or zero
coefficients can lower the effective degree. A promotable theorem must use the
effective degree after combining conjugate/same-frequency residues.

## Laurent Growth Plus Kernel Decay

Let `q_k` be derivative decay for the kernel:

```text
|W_hat^(k)(i t)| <= C_k (1+|t|)^(-q_k) (log(2+|t|))^D_k.
```

Assume multiplicities are bounded by `M`, zero counting is
`N(T,2T)<=C T log T`, and for `1<=j<=M`

```text
|b_(rho,-j)| <= C_j |gamma|^A_j (log(2+|gamma|))^B_j.
```

Then `(H-abs-r)` follows from the shell inequalities

```text
q_(j-1-ell) > A_j + 1
for every 0<=ell<r and ell+1<=j<=M,
```

provided `(H-deg)` handles every `ell>=r`.

A mean-square variant replaces the pointwise Laurent bound by

```text
sum_(T<|gamma|<=2T) |b_(rho,-j)|^2
  <= C_j T^theta_j (log T)^B_j.
```

Then `(H-abs-r)` follows if

```text
theta_j < 2 q_(j-1-ell) - 1
for every 0<=ell<r and ell+1<=j<=M.
```

If multiplicities are not bounded, replace these finite `j<=M` conditions by
the direct coefficient sums `(H-abs-r)`. Kernel decay alone never controls the
Laurent coefficients.

## Central Polynomial Composition

The central residue is

```text
Q_r(u) = Res_(z=0) e^(uz) W_hat(z)/L(E,1+z).
```

With

```text
W_hat(z)=sum_(m=-1)^infty w_m z^m,
1/L(E,1+z)=sum_(j=-r)^infty a_j z^j,
```

the coefficient formula is

```text
Q_r(u)=sum_(ell=0)^r C_ell u^ell,
C_ell=(1/ell!) sum_(h=0)^(r-ell) a_(-r+h) w_(r-ell-h-1).
```

The top coefficient is

```text
C_r = w_-1/L^(r)(E,1).
```

For normalized Agent-3 kernels, `w_-1=1`, hence

```text
Q_r(u)=u^r/L^(r)(E,1)+O(u^(r-1)).
```

Therefore, under `(H-min-r)`,

```text
c_E,W(e^u)=Q_r(u)+o(u^r)
          = (w_-1/L^(r)(E,1)) u^r + o(u^r).
```

If H2 is separately proved in the same pointwise mode,

```text
P_E,W(e^u)=exp(B_E,W) u^(-r)(1+o(1)),
```

then

```text
c_E,W(e^u) P_E,W(e^u)
  -> exp(B_E,W) w_-1/L^(r)(E,1).
```

With `w_-1=1`, the candidate limit is `exp(B_E,W)/L^(r)(E,1)`.

## Gap Map

Closed locally:

```text
central polynomial algebra;
exact offcentral residue polynomial;
positive-rank sufficiency of bounded lower-degree aggregates;
generic multiple-zero danger threshold m>=r+nu_rho+1.
```

Still open for theorem promotion:

```text
exact smoothstep H1 contour shift and tail bound;
fixed-curve reciprocal derivative bounds for simple zeros;
fixed-curve Laurent coefficient bounds for multiple zeros;
kernel derivative decay for every needed order;
same-mode H2 closure;
rank-zero pointwise stabilization, unless oscillatory/averaged/filtered.
```
