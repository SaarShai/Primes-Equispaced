---
schema_version: 1
title: "Kernel zero-filtering for H1 reciprocal residues"
date: 2026-05-11
type: research-note
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.82
dependencies:
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
  - handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
do_not_promote_unless:
  - H1 reciprocal residues are controlled after the chosen filtering, not merely for finitely many displayed zeros.
  - The kernel class is declared: positive/signed, compact log-support/Schwartz, fixed/family, curve-dependent/curve-independent.
  - Any infinite zero-filtering theorem is source-closed with a real entire-function theorem and zero-density hypotheses.
  - Rank-zero is stated as oscillatory, averaged, or explicitly filtered; do not call it a pointwise constant limit.
tags: [ec-ndc, smoothing, h1, kernels, residue-control]
---

# Kernel Zero-Filtering For H1 Reciprocal Residues

## Verdict

Finite kernel filtering is a useful control experiment and can be made into a
conditional reduction. It is not, by itself, an asymptotic stabilization theorem.

The H1 obstruction is

```text
Z_c(u) = sum_{gamma != 0} A_gamma W_hat(i gamma) e^(i gamma u)
```

for simple offcentral zeros, with

```text
A_gamma = 1/L'(E,1+i gamma).
```

For a zero of multiplicity `m`, the contribution is an exponential times a
polynomial in `u` of degree at most `m-1`, with coefficients involving the
Laurent expansion of `1/L(E,s)` and derivatives of `W_hat`.

Thus smoothing stabilizes H1 only in one of four declared ways:

1. residue control: `Z_c(u)=o(u^r)` for positive rank `r`;
2. explicit profile: retain `Z_c(u)` in the theorem;
3. product-level averaging: average `c_E,W(e^u) P_E,W(e^u)` itself;
4. kernel filtering: force `W_hat(i gamma)=0` for a controlled set of zeros.

## Finite Filtering

Let `Gamma_0={gamma_1,...,gamma_J}` be a finite set of offcentral ordinates.
If the admissible kernel class allows signed smooth perturbations, then finite
filtering is a linear constraint problem:

```text
W_hat(i gamma_j) = int_0^infty W(t) t^(i gamma_j-1) dt = 0,
1 <= j <= J.
```

In log variables `t=e^x`, this is a Fourier constraint on

```text
Phi(x) = W(e^x).
```

The constraints are

```text
int Phi(x) e^(i gamma_j x) dx = 0.
```

For signed `C_c^\infty` or Schwartz kernels, this is finite codimension. One
can keep the normalization `W_hat(0)=1` and impose finitely many complex
constraints, provided the chosen test bump family has a nonsingular moment
matrix. This gives a practical diagnostic:

```text
filter the first J offcentral H1 residues, then measure whether the residual
tail behaves like o(u^r) or remains main-scale.
```

This is useful because the first few low zeros are exactly the ones least
affected by ordinary smooth decay.

## Positivity Tradeoff

If `W>=0`, the same constraint becomes a characteristic-function zero for a
positive measure in log scale. Such zeros can occur, but arbitrary finite
prescription is no longer a free finite-codimension operation. Exact positivity
plus exact zero constraints may be incompatible for a chosen support and
normalization.

Therefore a filtered theorem must say which kernel class is allowed:

```text
signed kernel theorem: plausible finite filtering;
positive kernel theorem: requires a separate feasibility proof;
fixed natural kernel theorem: no filtering, only decay/control;
curve-dependent kernel theorem: mathematically useful but weaker as a
universality explanation.
```

## Infinite Filtering Obstruction

An asymptotic pointwise rank-zero constant would require all surviving
main-scale reciprocal residues to vanish or cancel. Kernel filtering all
offcentral zeros would require

```text
W_hat(i gamma)=0
```

for infinitely many ordinates.

For compact log-support kernels, `W_hat` is an entire function of exponential
type. A nonzero fixed kernel cannot generally be expected to vanish on the
full zero set of a GL(2) L-function, whose ordinate count grows faster than
linearly by the usual zero-counting scale. Making this a theorem requires a
source-closed entire-function zero-density input; until then, record it as the
structural obstruction, not as a promoted theorem.

If the support is allowed to grow with `U`, a family `W_U` can filter more
zeros as `U` grows. That may produce a valid approximation scheme, but it is
no longer the same fixed smoothing theorem. It becomes a two-parameter theorem
requiring a rate relation between:

```text
number of filtered zeros J(U),
support/oscillation cost of W_U,
growth of W_U derivatives,
tail control of unfiltered residues,
and H2/Sym2 error terms.
```

## Claim-Safe Kernel Program

The honest next experiment/theorem target is:

```text
Given a finite zero set Gamma_0 and analytic rank r, construct an admissible
signed kernel W_{Gamma_0} with W_hat(0)=1 and W_hat(i gamma)=0 for gamma in
Gamma_0. Prove

c_E,W(e^u) = Q_r(u) + Z_{tail,Gamma_0}(u) + error,

where Z_{tail,Gamma_0} omits those ordinates.
```

Then test whether increasing `Gamma_0` stabilizes finite data. If it does, the
theorem still says "finite-zero filtered profile," not "smoothing alone proves
pointwise stabilization."

## Best Use

Kernel zero-filtering should be used as a microscope:

- isolate whether the finite proxy is dominated by the first few H1 residues;
- distinguish low-zero oscillation from endpoint covariance;
- produce cleaner rank-zero diagnostics;
- suggest which zeros must be retained in an oscillatory profile.

It should not be used as a way to hide the reciprocal derivative problem.

## Promotion Decision

Promote only this reduction:

```text
Fixed smoothing does not automatically remove H1 offcentral reciprocal poles.
Finite signed kernel filtering can remove finitely many named residues, but
asymptotic stabilization still needs tail/residue control or an explicit
oscillatory/averaged theorem.
```

Do not promote a closed EC smoothing theorem from kernel filtering alone.
