---
title: "AGENT04 MinMod Source And Proof Hunt"
date: 2026-05-11
type: theorem-audit
tier: working
status: NO_GO
confidence: 0.88
tags: [breakthrough-wave-5, h1, ec-bfmt, minmod, minimum-modulus, reciprocal-derivative]
---

# Verdict

Status: `NO_GO`.

No source-closed proof of

```text
MinMod(E,c,A,h):  m_rho >= h(T)/T,  h(T)->infinity
```

was found from EC/newform explicit formulae, Hadamard products, selected-height
minimum-modulus theorems, or known negative-moment literature.

The best standard tools give either:

```text
selected horizontal heights:  |L| >= exp(-A_E log T/loglog T)=T^(-o(1))
```

but not near each zero, or local zero-avoidance bounds of Cartan/Jensen type
with scale no better than

```text
m_rho >= exp(-C_E,A log T loglog T)
```

unconditionally from available local zero counts, and at best

```text
m_rho >= T^(-C_E,A)
```

under an RH/Littlewood local-count upgrade.  Neither proves `h(T)/T`.

# Theorem Target

Use the project normalization:

```text
rho = 1+i gamma
```

for noncentral critical zeros of `L(E,s)`.  For fixed `c>0` and dyadic shell
`T<|gamma|<=2T`, the bad set is

```text
B_E(T,c) = {simple rho : dist(rho,Z_E\{rho}) < c/log T}.
```

The target input from Wave 4 Agent 03 is:

```text
MinMod(E,c,A,h):
  for every rho in B_E(T,c), there exists a zero-free boundary circle

    |s-rho| = R_rho,       0<R_rho<=A/log T,

  with cluster C_rho=Z_E cap {|s-rho|<R_rho} and

    m_rho := min_(|s-rho|=R_rho) |L(E,s)| >= h(T)/T,
    h(T)->infinity.
```

This is the minimum-modulus half of the conditional bad-set theorem:

```text
MinMod(E,c,A,h) + ProductLayer(E,c,A,h)
=> sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2).
```

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT03_EC_BFMT_BADSET_BUDGET_2026-05-11.md`:
  local cluster minimum modulus plus inverse-product layer cake proves the
  bad-set budget; pair counts alone do not supply the modulus factor.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md`:
  `MinMod(E,c,A,h)` and `ProductLayer(E,c,A,h)` remain independent H1 blockers.
- `primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT04_EC_BFMT_BADSET_INVERSEGAP_BUDGET_2026-05-11.md`:
  exact cluster product-minimum-modulus theorem; no count-only closure.
- `primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`:
  pointwise rank-one threshold is

  ```text
  |L'(E,rho)| >= h(T) log T / T.
  ```

- Sheth, arXiv:2312.05236, PDF p. 1-2: EC normalization, functional equation
  centered at `s=1`, critical line `Re(s)=1`.  PDF p. 13, Theorem 3.1:

  ```text
  N_E(t)=alpha_E t(log t+c)/pi+O(log t),
  ```

  hence `#Z_E(T,2T)<<_E T log T`.
- Bui-Florea-Milinovich, arXiv:2310.03949, PDF p. 2-3: their zeta theorem is
  over separated zeros; for full negative moments, RH plus simplicity is stated
  as insufficient because `log |zeta'(rho)|` depends on small zero gaps.
- Li-Zaharescu, "Value distribution of L'(rho)", PDF p. 2: the class includes
  holomorphic cusp-form L-functions.  PDF p. 4, Proposition 3.1: each unit
  interval contains a height `t` with

  ```text
  |L(sigma+it)| >= exp(-A log t/loglog t),  1/2<=sigma<=2.
  ```

  This is a selected-height theorem, not a zero-centered local theorem.
- Classical finite-order minimum-modulus literature is global/radial or
  exceptional-set based.  It does not prescribe microscopic circles centered at
  every zero of a fixed arithmetic function.

# Proof Attempts

## 1. Local Factorization

For a bad zero and chosen cluster circle,

```text
L(E,s) = product_(a=0)^(k_rho-1) (s-rho_a) H_rho(s),
```

where `H_rho` is holomorphic and nonvanishing in the disk.  On the boundary,

```text
|L(E,s)| = product_a |s-rho_a| |H_rho(s)|.
```

The maximum principle can transfer a boundary lower bound for `H_rho` to
`H_rho(rho)`, and then to `L'(E,rho)`.  But this is exactly Wave 4 Agent 03's
conditional lemma.  The argument does not produce a lower bound for
`H_rho`; it only consumes one.

## 2. Hadamard Product / Explicit Formula

The completed EC L-function has a canonical product.  Locally, every
Hadamard or explicit-formula lower bound has the schematic form

```text
log |L(E,s)|
  = controlled main term
    + sum_(near zeros rho') log |s-rho'|
    + error.
```

With only the source-checked zero count, a unit vertical window contains
`O_E(log T)` zeros.  Choosing a zero-free radius near `1/log T` can avoid the
radial distances, but the available clearance and the possible number of
nearby zeros still allow

```text
sum log |s-rho'| >= -C_E,A log T loglog T.
```

Thus the local output is at best

```text
m_rho >= exp(-C_E,A log T loglog T)=T^(-C_E,A loglog T),
```

far below `h(T)/T`.

Under a stronger RH/Littlewood-style local count, the same proof shape may
replace `O(log T)` by `O(log T/loglog T)` in microscopic intervals, yielding
only

```text
m_rho >= T^(-C_E,A).
```

The constant is not forced below `1`, and there is no diverging factor.  This
still does not imply `h(T)/T`.

## 3. EC/Newform Euler Product Formulae

Sheth's EC explicit formula and partial Euler product asymptotics work in the
right half of the critical strip and route zero contributions through explicit
zero sums.  Near a boundary circle centered at `rho`, the zero term
`rho-s` is singular or nearly singular, and the formula gives no signed lower
bound for the remaining nonzero factor.

The method controls partial Euler products outside logarithmically exceptional
sets in the Euler-product variable.  It does not give a uniform lower bound on
all microscopic circles around all zeros in a dyadic zero shell.

## 4. Selected Heights

Li-Zaharescu gives unit-spaced heights with

```text
|L(sigma+it)| >= exp(-A log t/loglog t)
```

uniformly in a vertical strip.  This is stronger than `T^{-1}` in size, but it
is located on one horizontal line per unit interval.  A bad zero at height
`gamma` needs a circle at distance `O(1/log T)` from `gamma`.

There is no maximum/minimum principle that transports a lower bound from a
selected horizontal line across a region containing unknown zeros to every
zero-centered microscopic boundary circle.

## 5. Negative Moment Literature

BFMT proves zeta upper bounds only on separated zero subfamilies.  Their own
setup identifies small gaps as the obstruction to full-family negative moment
upper bounds.

Li-Zaharescu proves lower negative-moment and extreme-small-value statements
for `L'(rho)`.  These are the wrong direction for `MinMod`: they show the
presence/size of small derivatives under hypotheses, not a uniform lower cap
on reciprocal derivatives or local boundary minima.

# Weakest Valid Replacement

The source-safe replacements are:

```text
SelectedHeight-MinMod(E):
  under the normalized EC/newform zero-location hypotheses needed by the
  selected-height theorem, every large unit interval contains a height tau
  such that

    min_(strip sigma) |L(E,sigma+i tau)|
      >= exp(-A_E log tau/loglog tau).
```

This is useful for horizontal contour tails only.  It has no direct bad-set
reciprocal-derivative consequence.

For local zero-centered circles, the strongest standard-tool statement to
carry forward is only:

```text
StandardLocalAvoidance(E,A):
  for each rho, one can choose a zero-free circle R_rho<=A/log T
  outside the finite set of local zero radii, but the sourced lower scale is

    m_rho >= exp(-C_E,A log T loglog T)

  unconditionally, or at best m_rho >= T^(-C_E,A) after an RH/Littlewood
  local-count upgrade.
```

This is not promoted as a new proof route.  It is the already-known
Cartan/Jensen/minimum-modulus obstruction scale, recorded only to show why it
does not reach the H1 target.

# Obstruction

The target lower bound is logarithmically sharp:

```text
log m_rho >= -log T + log h(T).
```

Standard tools lose more than this before any arithmetic cancellation enters.
The loss comes from two independent places:

```text
near-zero product loss:
  sum log |s-rho'| can be as negative as
  -C log T loglog T with sourced zero counts;

cofactor loss:
  no explicit formula, Euler product, or selected-height theorem gives a
  pointwise lower bound for the nonvanishing local factor H_rho on every
  bad-zero cluster.
```

Even replacing the zero-count loss by an RH/Littlewood `T^(-C)` scale would
not close MinMod unless one proves `C<1` with a diverging spare factor.  No
source located supplies that constant control, and the known negative-moment
literature is built around avoiding or separately budgeting precisely these
near-collision cases.

# Dependency Impact

`MinMod(E,c,A,h)` remains unsourced.

Consequences:

```text
Agent03 bad-set theorem remains conditional on MinMod + ProductLayer.
Agent05 ProductLayer cannot close the bad set without MinMod.
Separated EC-BFMT does not control B_E(T,c).
H1 finite-box closure still needs either:
  MinMod(E,c,A,h),
  a direct complement tail,
  or a full reciprocal-derivative high-tail theorem.
```

No H1 theorem should cite EC explicit formulae, selected heights, pair counts,
or classical minimum-modulus literature as closing the bad-set minimum-modulus
input.
