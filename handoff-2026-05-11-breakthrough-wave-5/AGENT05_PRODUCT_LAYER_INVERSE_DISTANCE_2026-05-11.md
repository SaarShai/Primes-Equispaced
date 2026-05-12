---
title: "AGENT05 ProductLayer Inverse Distance"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.86
tags: [breakthrough-wave-5, h1, ec-bfmt, product-layer, inverse-distance, higher-correlation, minmod]
---

# Verdict

Status: `RIGOROUS_REDUCTION`.

`ProductLayer(E,c,A,h)` is sharpened to a rooted singular local-correlation
condition.  It is not sourced from ordinary pair-correlation or count-only
`n`-level input.

The usable theorem is:

```text
rooted inverse-product correlation at scale 1/log T
+ summable cluster-size tail
=> ProductLayer(E,c,A,h).
```

Since this gives a natural-scale `O(T)` product budget, it is enough for
`o(h(T)T)` whenever `h(T)->infinity`.  Combined with `MinMod(E,c,A,h)`, Agent03
then gives

```text
sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2).
```

The exact missing higher-cluster statistic is the weighted rooted inverse
product

```text
J_m(T;A) =
  sum_(rho0 in S_E(T))
  sum_(rho1,...,rhom distinct)
    prod_(j=1)^m (log T |rhoj-rho0|)^(-1),
```

where the inner sum is restricted by `0<|rhoj-rho0|<=A/log T`.  For `m>=2`,
ordinary higher-correlation counts are insufficient unless they control this
singular weight, or an equivalent product-threshold layer cake.

# Theorem Target

Fix `E/Q`, `c>0`, `A>c`, and `h(T)->infinity`.  In the project normalization
critical zeros are written

```text
rho = 1+i gamma.
```

Let

```text
S_E(T) = {simple zeros rho=1+i gamma : T<|gamma|<=2T},
F_E(T,c) = {rho in S_E(T) : dist(rho,Z_E\{rho}) >= c/log T},
B_E(T,c) = S_E(T) \ F_E(T,c).
```

For `rho in B_E(T,c)`, let a close cluster be

```text
C_rho = Z_E cap {|s-rho| < R_rho}
      = {rho=rho0,rho1,...,rho_(k_rho-1)},
0 < R_rho <= A/log T,
```

with zero-free boundary.  Define

```text
D_rho = product_(a=1)^(k_rho-1) |rho-rho_a|.
```

The product-layer target is

```text
ProductLayer(E,c,A,h):
  W_E(T;A) :=
  sum_(k>=2) A(2A)^(k-1)/(log T)^k
    * sum_(rho in B_E(T,c), k_rho=k) 1/D_rho
  = o(h(T)T).
```

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT03_EC_BFMT_BADSET_BUDGET_2026-05-11.md`,
  lines 55-87: `MinMod + ProductLayer` implies the bad-set budget.
- Same file, lines 124-184: local factorization gives the pointwise reciprocal
  derivative bound feeding the product layer.
- Same file, lines 186-208: `ProductLayer` is exactly the inverse-product
  layer cake.
- `primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT04_EC_BFMT_BADSET_INVERSEGAP_BUDGET_2026-05-11.md`,
  lines 227-300: pair inverse-gap layer cake closes only with a reciprocal cap
  such as minimum modulus.
- Same file, lines 302-334: higher clusters require inverse product-distance
  layers, not plain local-density counts.
- Same file, lines 336-363: count-only, pair-correlation-only, and
  local-statistics-only inputs cannot imply reciprocal derivative control.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md`,
  lines 34-40 and 75-80: `MinMod` and `ProductLayer` remain independent H1
  blockers after the separated BFMT branch.
- `/tmp/farey-homogeneous-bfmt-20260511/sheth_ec_arxiv_2312.05236.txt`,
  lines 907-912: `N_E(t)=alpha_E t(log t+c)/pi+O(log t)`, hence
  `#S_E(T) <<_E T log T`.

# Product-Layer Attempt

Set `m=k-1`.  Define the normalized rooted inverse-product statistic

```text
J_m(T;A) =
  sum_(rho0 in S_E(T))
  sum_(rho1,...,rhom distinct; 0<|rhoj-rho0|<=A/log T)
    prod_(j=1)^m (log T |rhoj-rho0|)^(-1).
```

For a bad zero with `k_rho=m+1`, all cluster mates lie in the rooted ball
`|s-rho|<=A/log T`.  The ordered rooted tuple sum contains the `m!` orderings
of exactly those mates.  Therefore

```text
sum_(rho in B_E(T,c), k_rho=m+1) 1/D_rho
  <= (log T)^m / m! * J_m(T;A).
```

Substitute this into `W_E(T;A)`:

```text
W_E(T;A)
 <= sum_(m>=1) A(2A)^m/(log T)^(m+1)
      * (log T)^m/m! * J_m(T;A)

 = 1/log T * sum_(m>=1) A(2A)^m/m! * J_m(T;A).
```

Thus a sufficient correlation-side product layer is

```text
sum_(m>=1) A(2A)^m/m! * J_m(T;A)
  = O_A,E(T log T).
```

Then

```text
W_E(T;A) = O_A,E(T) = o(h(T)T).
```

This proves `ProductLayer(E,c,A,h)` from rooted inverse-product correlation.
It deliberately overcounts clusters by rooted ordered tuples; the overcount is
harmless and makes the condition compatible with correlation inputs.

For `m=1`, let

```text
Q_1(T;u) =
  #{(rho0,rho1): rho0 in S_E(T), rho1 != rho0,
    log T |rho1-rho0| <= u}.
```

If uniformly for `0<u<=A`

```text
Q_1(T;u) <<_E T log T * u^beta,    beta>1,
```

then the inverse-gap layer cake gives

```text
J_1(T;A)
 <= A^(-1) Q_1(T;A)
    + int_(1/A)^infinity Q_1(T;1/v) dv
 <<_(E,A,beta) T log T.
```

So a GUE-strength close-pair repulsion law can close the pair product layer.
It still does not close the reciprocal derivative budget without `MinMod`.

# Higher-Cluster Requirements

For `m>=2`, define the rooted ordered counting measure

```text
dnu_(m,T,A)(u1,...,um)
```

by placing a unit atom at

```text
uj = log T |rhoj-rho0| in (0,A]
```

for every rooted ordered tuple of distinct zeros in the shell.  Then

```text
J_m(T;A) =
  int_(0,A]^m (u1...um)^(-1) dnu_(m,T,A)(u1,...,um).
```

The needed higher-cluster input is one of the following equivalent/sufficient
forms.

1. Direct singular correlation:

```text
J_m(T;A) <= C_m(A,E) T log T
and
sum_(m>=2) A(2A)^m C_m(A,E)/m! < infinity.
```

2. Bounded cluster size `m<=M` plus the same bound for `2<=m<=M`.

3. Product-threshold layer cake, in cluster language:

```text
sum_(k>=3) A(2A)^(k-1)/(log T)^k
  * int_0^infinity M_k(T;V) dV
  = O_A,E(T),
```

where

```text
M_k(T;V) =
  #{rho in B_E(T,c): k_rho=k, D_rho^(-1)>V}.
```

4. A repulsive local `m`-correlation majorant strong enough to make

```text
int_(0,A]^m (u1...um)^(-1) dmu_m(u1,...,um) < infinity
```

with `dnu_(m,T,A) <= C_m T log T dmu_m`, summably in `m`.

Plain statements of the form

```text
Q_m(T;A,...,A) << T log T
```

do not suffice.  They count rooted clusters but do not control concentration
near the coordinate hyperplanes `uj=0`, exactly where the inverse product is
singular.

# Closure or Obstruction

Closure:

```text
RootedInvProdCorr(E,A):
  sum_(m>=1) A(2A)^m/m! * J_m(T;A)
    = O_A,E(T log T)
```

implies

```text
ProductLayer(E,c,A,h)
```

for every `h(T)->infinity`.

Then Agent03 gives, under the independent minimum-modulus input

```text
m_rho := min_(|s-rho|=R_rho) |L(E,s)| >= h(T)/T,
```

the bad-set reciprocal budget

```text
sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2).
```

Obstruction:

```text
pair-correlation counts alone
ordinary fixed-test n-level correlations alone
cluster counts without inverse-product weights
```

do not prove `RootedInvProdCorr`.  The exact missing statistic is

```text
J_m(T;A) =
  int_(0,A]^m (u1...um)^(-1) dnu_(m,T,A)
```

for `m>=2`, with the weighted summability in `m`.  Equivalently, at the
cluster level it is the higher product-threshold integral

```text
int_0^infinity M_k(T;V) dV
```

with the weights appearing in `ProductLayer`.

# Dependency Impact

If `RootedInvProdCorr(E,A)` is supplied, `ProductLayer(E,c,A,h)` is no longer a
separate blocker; it contributes `O(T)` and becomes negligible against
`h(T)T`.

`MinMod(E,c,A,h)` remains load-bearing and independent.  Product-distance
geometry does not lower-bound `L(E,s)` on cluster boundaries.

Pair input can discharge only the `k=2` layer.  The remaining dependency is the
singular higher-cluster statistic `J_m` or the equivalent `M_k` product-layer
integral.  Without that statistic, the complement branch remains a rigorous
reduction, not a proved EC theorem.
