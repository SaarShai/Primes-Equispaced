---
schema_version: 1
title: "Agent 03 H1 multiple-zero Laurent control"
date: 2026-05-11
agent: "Agent 03 -- EC H1 Multiple-Zero/Laurent Control"
type: theorem-package
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
dependencies:
  - start.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md
  - primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
  - primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md
tags: [ec-ndc, h1, positive-rank, multiple-zeros, laurent-control]
---

# Agent 03 H1 Multiple-Zero Laurent Package

status: `RIGOROUS_REDUCTION`

Status enum used below:

```text
LOCAL_PROOF        algebraic identity from Laurent/residue calculus
CONDITIONAL_CLOSE  valid after stated H1 contour, zero-sum, and tail inputs
BLOCKED_INPUT      theorem input not proved in the local files read here
NOT_PROMOTED       diagnostic or theorem shape explicitly not claimed
```

No external theorem is invoked. Future external inputs must use repository
citation protocol: `curl + pdftotext + short quote + page/equation`.

Analytic rank only:

```text
r = ord_(s=1) L(E,s).
```

No BSD rank substitution, cross-curve universality, finite diagnostic evidence,
or correspondence/email claim is used.

## Setup

Use the H1 Perron object

```text
c_E,W(e^u)
 = (1/(2 pi i)) int e^(u z) W_hat(z)/L(E,1+z) dz,
u = log K.
```

Assume the fixed-kernel H1 contour theorem, height selection, indentation
bookkeeping, zero sums, and shifted-line tail are proved in the declared mode.
Those analytic inputs remain hypotheses here.

At the central zero,

```text
Q_r(u) = Res_(z=0) e^(u z) W_hat(z)/L(E,1+z)
       = (w_-1/L^(r)(E,1)) u^r + O(u^(r-1)).
```

For repository-normalized kernels with `w_-1=1`,

```text
Q_r(u) = u^r/L^(r)(E,1) + O(u^(r-1)).
```

## Local Laurent Algebra

status: `LOCAL_PROOF`

Let `rho != 1` be a crossed zero, put

```text
alpha = rho - 1,
m = ord_(s=rho) L(E,s).
```

Near `z=alpha`,

```text
1/L(E,1+z)
 = sum_(j=1)^m b_(rho,-j)(z-alpha)^(-j) + holomorphic.
```

The exact H1 residue is

```text
R_rho(u)
 = e^(alpha u) sum_(ell=0)^(m-1) A_(rho,ell) u^ell,

A_(rho,ell)
 = (1/ell!) sum_(j=ell+1)^m
     b_(rho,-j) W_hat^(j-1-ell)(alpha)/(j-1-ell)!.
```

For a simple zero,

```text
R_rho(u)=e^(alpha u) W_hat(alpha)/L'(E,rho).
```

For the top Laurent coefficient,

```text
b_(rho,-m)=m!/L^(m)(E,rho).
```

The lower `b_(rho,-j)` are rational polynomials in
`L^(m)(E,rho),...,L^(2m-j)(E,rho)` divided by powers of `L^(m)(E,rho)`.
Therefore kernel decay alone never controls H1 residues; reciprocal Laurent
growth is a separate input.

## Kernel-Zero Filtering

status: `LOCAL_PROOF`

Let

```text
nu_rho = ord_(z=alpha) W_hat(z).
```

Then `A_(rho,ell)=0` for every

```text
ell > m - 1 - nu_rho.
```

If `nu_rho >= m`, the whole pole is kernel-cancelled. If `nu_rho < m`, the
generic leading degree is

```text
d_gen(rho)=m-1-nu_rho,
```

with leading coefficient

```text
b_(rho,-m) W_hat^(nu_rho)(alpha)
/(nu_rho! (m-1-nu_rho)!).
```

This is generic only. Internal Laurent-kernel cancellation can make the actual
degree lower.

For a positive-rank central-only theorem, a single uncancelled multiple zero is
harmless by degree if

```text
m - 1 - nu_rho < r,
equivalently nu_rho >= m-r.
```

It is killed entirely only by the stronger condition `nu_rho >= m`.

Finite signed kernel filtering can impose finitely many such conditions if the
kernel class permits the required moment constraints. Infinite filtering is not
promoted: it needs an entire-function/zero-density theorem and a proof that the
kernel derivative costs do not break the H1/H2 estimates.

## Effective Degrees

status: `LOCAL_PROOF`

Group terms by the same exponent `alpha`. Define net coefficients

```text
A_(alpha,ell)^net
 = sum_(rho: rho-1=alpha) A_(rho,ell)
```

plus any declared exact same-exponent contributions from the same contour
package. The effective degree is

```text
D_alpha = max { ell : A_(alpha,ell)^net != 0 },
```

with `D_alpha=-infinity` if all net coefficients vanish.

For real kernels and conjugate zeros, the pair is a real oscillation

```text
2 Re(A_(i gamma,ell)^net e^(i gamma u)) u^ell.
```

This cancels pointwise only when the relevant net coefficient is zero. Distinct
nonzero frequencies do not cancel a finite top-degree exponential polynomial
to `o(u^d)`. For infinite aggregates, the same conclusion requires a proved
summability, principal-value, or averaged theorem; it cannot be inferred from
formal pairing.

## Positive-Rank Survival Theorem

status: `CONDITIONAL_CLOSE`

Let `r>=1`. Suppose the H1 contour expansion in the chosen mode gives

```text
c_E,W(e^u)
 = Q_r(u)
   + sum_(Re alpha=0, alpha!=0) e^(alpha u)
       sum_(ell=0)^(D_alpha) A_(alpha,ell)^net u^ell
   + Z_left(u) + Z_exp(u) + I_H1(u).
```

Then the central-only positive-rank H1 asymptotic

```text
c_E,W(e^u)=Q_r(u)+o(u^r)
```

follows if all of the following hold:

```text
S1. Z_exp(u)=0, or every Re(alpha)>0 term is explicitly retained outside the
    central-only claim.

S2. For every critical-line exponent alpha!=0, D_alpha < r.

S3. The lower-degree critical-line aggregate satisfies
    sum_(ell=0)^(r-1) u^ell Z_ell(u)=o(u^r),
    where Z_ell(u)=sum_(Re alpha=0) A_(alpha,ell)^net e^(alpha u).

S4. Z_left(u)+I_H1(u)=o(u^r).
```

A clean sufficient version of `S3` is

```text
Z_ell(u)=O(1) for every 0<=ell<r.
```

An even more checkable sufficient version is absolute convergence:

```text
sum_(Re alpha=0) |A_(alpha,ell)^net| < infinity,
0<=ell<r.
```

Thus multiple offcentral zeros do not by themselves kill positive-rank H1.
They kill the central-only pointwise theorem exactly when an omitted effective
degree `D_alpha >= r` survives, or when the lower-degree aggregate is not
proved `o(u^r)`.

## Individual-Zero Corollaries

status: `CONDITIONAL_CLOSE`

For one critical-line multiple zero of multiplicity `m`:

```text
D_alpha < r
```

is the exact degree condition after kernel zeros and coefficient cancellations.

The generic sufficient condition is

```text
m <= r + nu_rho.
```

The generic obstruction begins at

```text
m >= r + nu_rho + 1.
```

Examples:

```text
r=1, simple zero: degree 0; harmless only after reciprocal-derivative
                  aggregate control.

r=1, double zero, no kernel zero: degree 1; blocks central-only pointwise H1
                                  unless cancelled, retained, or averaged.

r=1, double zero, simple kernel zero: degree <=0; survives by degree, still
                                      needs Laurent coefficient summability.

r=2, triple zero, no kernel zero: degree 2; blocks central-only pointwise H1.

r=2, triple zero, simple kernel zero: degree <=1; survives by degree, still
                                      needs coefficient control.
```

## Laurent Growth Criteria

status: `CONDITIONAL_CLOSE`

Assume critical-line zero counting

```text
N(T,2T) <= C T log T,
```

bounded multiplicity `m<=M`, and kernel derivative decay

```text
|W_hat^(a)(i t)|
 <= C_a (1+|t|)^(-q_a) (log(2+|t|))^D_a.
```

Pointwise Laurent bounds

```text
|b_(rho,-j)|
 <= C_j |gamma|^A_j (log(2+|gamma|))^B_j
```

imply absolute convergence of every degree `ell<r` coefficient sum if

```text
q_(j-1-ell) > A_j + 1
for every 0<=ell<r and ell+1<=j<=M.
```

Mean-square Laurent bounds

```text
sum_(T<|gamma|<=2T) |b_(rho,-j)|^2
 <= C_j T^theta_j (log T)^B_j
```

imply the same absolute convergence if

```text
theta_j < 2 q_(j-1-ell) - 1
for every 0<=ell<r and ell+1<=j<=M.
```

If multiplicities are unbounded, replace bounded-`M` shell criteria by the
direct coefficient sums

```text
sum_(Re alpha=0) |A_(alpha,ell)^net| < infinity,
0<=ell<r,
```

plus explicit removal, retention, or averaging of every `ell>=r` term.

## Same-Frequency Cancellation Rule

status: `LOCAL_PROOF`

At a fixed top degree `d`, a finite critical-line obstruction has the form

```text
u^d sum_k C_k e^(i gamma_k u),
gamma_k distinct and nonzero.
```

This is `o(u^d)` pointwise only if every same-frequency net coefficient
`C_k` is zero. Conjugate terms merely rewrite the same obstruction as real
sines/cosines. They do not produce a pointwise limit unless the coefficient
vanishes.

Therefore all theorem statements must compute `D_alpha` after:

```text
1. kernel vanishing at alpha;
2. internal cancellation among the Laurent/kernel-derivative terms in
   A_(rho,ell);
3. exact same-exponent netting;
4. declared summability/PV/averaged cancellation for infinite aggregates.
```

Only steps already proved in the theorem mode may be used to lower
`D_alpha`.

## Product Composition

status: `CONDITIONAL_CLOSE`

If the positive-rank H1 conditions above hold and H2 is separately proved in
the same pointwise mode as

```text
P_E,W(e^u)=exp(B_E,W) u^(-r)(1+o(1)),
```

then

```text
c_E,W(e^u)P_E,W(e^u)
 -> exp(B_E,W) w_-1/L^(r)(E,1).
```

For `w_-1=1`, the candidate limit is

```text
exp(B_E,W)/L^(r)(E,1).
```

If an effective degree `D_alpha=r` is retained, the honest result is an
oscillatory profile after multiplying by `u^(-r)`, not a constant pointwise
limit. If `D_alpha>r`, ordinary first averaging is not automatically enough;
subtraction, finite part, stronger damping, or a proved averaged theorem is
required.

## Blockers

status: `BLOCKED_INPUT`

Open inputs before theorem promotion:

```text
1. Exact fixed-kernel H1 contour shift with height sequence, indentations,
   crossed residues, and tails.
2. Treatment of every Re(rho)>1 crossed zero: absent, cancelled, or retained.
3. Reciprocal derivative bounds for simple zeros.
4. Reciprocal Laurent coefficient bounds for multiple zeros.
5. Kernel derivative decay through every derivative order used by residues,
   after any zero-filtering perturbation.
6. Effective-degree audit after kernel zeros, internal coefficient
   cancellations, and same-frequency netting.
7. Infinite aggregate theorem if relying on PV, cancellation, or averaging
   instead of absolute convergence.
8. Same-mode H2 closure before any product stabilization claim.
```

Rank zero remains outside this positive-rank package. Rank-zero central-only
pointwise H1 is blocked by any nonzero critical-line residue at main scale
unless it is killed, cancelled, retained, subtracted, or averaged in a proved
mode.

## Do Not Promote

status: `NOT_PROMOTED`

Do not promote any of the following from this package:

```text
fixed-curve EC theorem with no reciprocal Laurent estimates;
simple-zero theorem from zero counting alone;
multiple-zero theorem from kernel decay alone;
pointwise constant theorem with a retained degree-r oscillation;
infinite kernel-zero filtering for a fixed compactly supported kernel;
H1/H2 product theorem with mismatched pointwise/profile/averaged modes;
any statement using algebraic rank, BSD, or finite numerics as theorem input.
```

## Verification Notes

Read locally:

```text
start.md
token-economy.yaml
L0_rules.md
primes-equispaced/L1_index.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md
primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md
```

No archive pages were opened. No web search was used. `./te doctor` returned
`ok: true`.

Checks performed:

```text
local algebra reconciled with the named H1 residue files;
positive-rank survival stated only as conditional reduction;
kernel-zero filtering separated from Laurent coefficient control;
same-frequency cancellation not assumed across distinct frequencies;
external theorem citation protocol noted but no external theorem claimed.
```

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT03_H1_MULTIPLE_ZERO_LAURENT_2026-05-11.md
```
