---
title: "AGENT03 EC-BFMT BadSet Budget"
date: 2026-05-11
type: theorem-reduction
tier: working
status: CONDITIONAL_THEOREM
confidence: 0.90
tags: [breakthrough-wave-4, h1, ec-bfmt, bad-set, minimum-modulus, layer-cake, reciprocal-derivative]
---

# Verdict

Status: `CONDITIONAL_THEOREM`.

`EC-BFMT-BadSetBudget(E,c)` closes conditionally from two non-count inputs:

```text
local cluster minimum modulus at scale 1/log T
+ inverse-product-distance layer cake for bad clusters
=> sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2).
```

This is stronger than a diagnostic no-go and weaker than the trivial direct
assumption on the reciprocal derivative sum.  Pair-correlation or close-pair
counts may supply only the inverse-distance side.  They still do not supply the
minimum-modulus side and therefore cannot close the bad set alone.

# Theorem Target

Fix an elliptic curve `E/Q` and `c>0`.  In the project normalization, critical
zeros are written

```text
rho = 1+i gamma.
```

For a dyadic shell, let

```text
S_E(T) = {simple zeros rho=1+i gamma : T<|gamma|<=2T},
F_E(T,c) = {rho in S_E(T) : dist(rho,Z_E\{rho}) >= c/log T},
B_E(T,c) = S_E(T) \ F_E(T,c).
```

Distances are complex distances unless the critical-line/RH normalization is
being imposed, in which case they are ordinate distances.

The target is

```text
EC-BFMT-BadSetBudget(E,c):
  sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2).
```

## Conditional Cluster-Layer Theorem

Assume there are constants `A>c`, a function `h(T)->infinity`, and for every
`rho in B_E(T,c)` a zero-free boundary circle

```text
0 < R_rho <= A/log T,
C_rho = Z_E cap {|s-rho| < R_rho}
      = {rho=rho_0,rho_1,...,rho_(k_rho-1)}
```

with

```text
m_rho := min_(|s-rho|=R_rho) |L(E,s)| >= h(T)/T.
```

Define

```text
D_rho = product_(a=1)^(k_rho-1) |rho-rho_a|,
Y_rho = 1/D_rho.
```

Assume the weighted inverse-product layer cake

```text
sum_(k>=2) A(2A)^(k-1)/(log T)^k
  * sum_(rho in B_E(T,c), k_rho=k) Y_rho
  = o(h(T) T).
```

Then `EC-BFMT-BadSetBudget(E,c)` holds.

Useful natural-scale corollary: if the bad clusters have bounded size
`k_rho<=K`, the same min-modulus certificate holds, and for each `2<=k<=K`

```text
sum_(rho in B_E(T,c), k_rho=k) 1/D_rho
  <<_(E,c,A,K) T (log T)^k,
```

then the bad-set contribution is

```text
<<_(E,c,A,K) T^2/h(T) = o(T^2).
```

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`,
  lines 41-55: separated EC-BFMT gives the good-set branch conditionally, while
  the bad-set budget remains the independent complement.
- Same packet, lines 252-272: the separated BFMT side keeps only `T^o(1)`
  losses after GL2 local inputs; this packet attacks only the complement.
- `primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT04_EC_BFMT_BADSET_INVERSEGAP_BUDGET_2026-05-11.md`,
  lines 148-225: local cluster minimum-modulus factorization gives the pointwise
  reciprocal derivative bound.
- Same packet, lines 227-334: pair inverse-gap and higher product-distance
  layer cakes are the right count-side budgets.
- Same packet, lines 336-376: count-only, pair-correlation-only, simplicity-only,
  and local-statistics-only routes are no-go without a reciprocal cap.
- `primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`,
  lines 86-118: the global shell condition `R_E,1(T)=o(T^2)` remains unproved
  and is exactly the H1 anti-small-derivative scale.
- `/tmp/farey-homogeneous-bfmt-20260511/sheth_ec_arxiv_2312.05236.txt`,
  lines 907-912: `N_E(t)=alpha_E t(log t+c)/pi+O(log t)`, hence dyadic zero
  count is `<<_E T log T`.

# Proof Attempt

For fixed `rho in B_E(T,c)`, factor inside the disk:

```text
L(E,s) = product_(a=0)^(k_rho-1) (s-rho_a) h_rho(s),
```

where `h_rho` is holomorphic and nonvanishing in `|s-rho|<R_rho`.
On the boundary,

```text
|s-rho| = R_rho,
|s-rho_a| <= 2R_rho  for a>=1.
```

Thus

```text
product_(a=0)^(k_rho-1) |s-rho_a|
  <= R_rho (2R_rho)^(k_rho-1).
```

Since `|L(E,s)|>=m_rho` on the same boundary,

```text
|h_rho(s)| >= m_rho/[R_rho(2R_rho)^(k_rho-1)].
```

Apply the maximum principle to `1/h_rho`.  The same lower bound holds at
`s=rho`.  As `rho` is simple,

```text
L'(E,rho) = D_rho h_rho(rho),
```

so

```text
|L'(E,rho)|^(-1)
  <= R_rho(2R_rho)^(k_rho-1)/(m_rho D_rho).
```

Using `R_rho<=A/log T` and `m_rho>=h(T)/T`,

```text
|L'(E,rho)|^(-1)
  <= A(2A)^(k_rho-1) T
     /[h(T)(log T)^k_rho D_rho].
```

Summing over bad zeros gives

```text
sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1)
 <= T/h(T) *
    sum_(k>=2) A(2A)^(k-1)/(log T)^k
      * sum_(rho in B_E(T,c), k_rho=k) 1/D_rho.
```

The stated layer-cake assumption makes the right side `o(T^2)`.

# Layer-Cake Budget

For fixed cluster size `k`, set

```text
M_k(T;V) =
  #{rho in B_E(T,c) : k_rho=k and 1/D_rho > V}.
```

Then the exact layer-cake identity is

```text
sum_(rho in B_E(T,c), k_rho=k) 1/D_rho
  = int_0^infinity M_k(T;V) dV.
```

Therefore the theorem can be stated equivalently as

```text
sum_(k>=2) A(2A)^(k-1)/(log T)^k
  * int_0^infinity M_k(T;V) dV
  = o(h(T) T).
```

For pair clusters, write

```text
d_rho = min_(rho' != rho) |rho-rho'|,
P_T(delta) = #{rho in B_E(T,c) : d_rho <= delta}.
```

Since bad zeros have `d_rho<=c/log T`,

```text
sum_(rho in B_E(T,c), k_rho=2) 1/d_rho
 <= (log T/c) P_T(c/log T)
    + int_(log T/c)^infinity P_T(1/u) du.
```

Thus the pair part closes if

```text
sum_(rho in B_E(T,c), k_rho=2) 1/d_rho
  = o(h(T) T (log T)^2).
```

A GUE-strength close-pair upper law with exponent `beta>1`,

```text
P_T(delta) <<_E T log T (delta log T)^beta
  uniformly for 0<delta<=c/log T,
```

gives

```text
sum_(rho in B_E(T,c), k_rho=2) 1/d_rho
  <<_E T (log T)^2,
```

and hence the pair contribution is `<<_E T^2/h(T)=o(T^2)`.  This is the
precise way pair-correlation-style information can help: it controls the
inverse-gap layer cake, not the derivative scale.

# Obstruction or Closure

Closure is conditional on both inputs:

```text
MinMod(E,c,A,h):
  m_rho >= h(T)/T on zero-free cluster boundaries, h(T)->infinity.

ProductLayer(E,c,A,h):
  weighted inverse-product layer cake = o(h(T)T).
```

The assumptions are weaker than directly assuming

```text
sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1)=o(T^2),
```

because they separate value size from zero geometry.  In the natural bounded
cluster regime they require only

```text
sum 1/D_rho << T(log T)^k
```

and a diverging factor in the boundary minimum modulus.

Count-only routes still cannot close the target.  Zero counts give at most
`#B_E(T,c)<<_E T log T`.  Close-pair counts, pair correlation, n-level
correlations, local-density estimates, and simplicity proportions are all
invariant under locally multiplying an analytic model by a nonzero scalar; zero
locations and spacings stay fixed, while all `L'(rho)` scale by that scalar and
all reciprocal derivatives scale by its inverse.  For the normalized EC
`L`-function the scalar is fixed, but a proof using only location data has no
mechanism to recover the missing value-scale lower bound.

Hence:

```text
pair correlation alone: NO_GO;
count of bad zeros alone: NO_GO;
GUE beta>1 inverse-gap law + MinMod h(T)/T: closes pair clusters;
full product-distance layer cake + MinMod h(T)/T: closes all bad clusters.
```

# Dependency Impact

- If Agents 01-02 close the separated EC-BFMT inputs, this packet supplies the
  exact independent complement needed for the BFMT bad set, but only
  conditionally on `MinMod + ProductLayer`.
- No unconditional H1 theorem is promoted.
- No pair-correlation count-only closure is promoted.
- The next high-leverage target is a fixed-curve local minimum-modulus theorem
  at radius `A/log T`; after that, GUE-strength inverse-gap/product-distance
  estimates become useful rather than merely diagnostic.
