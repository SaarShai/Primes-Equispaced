---
title: "AGENT05 H1 reciprocal tail theorem"
date: 2026-05-11
status: RIGOROUS_REDUCTION
tags: [h1, rank-one, reciprocal-derivative, layer-cake, minimum-modulus, negative-moments, bfmt]
---

## Verdict

No fixed-curve theorem proving

```text
R_E,1(T) =
  sum_(T<|gamma|<=2T, simple) |L'(E,1+i gamma)|^(-1)
  = o(T^2)
```

is source-closed here.

The direct attack gives a rigorous reduction:

```text
full reciprocal tail
or
separated BFMT reciprocal moment + complement reciprocal tail
or
stronger negative-moment / EC-WMC analogue
=> R_E,1(T)=o(T^2).
```

The exact source gap is still an upper tail for very small
`|L'(E,1+i gamma)|` at fixed-curve zeros, especially on the non-separated
complement.

## Theorem Target

Fix an elliptic curve `E/Q`. In project normalization, write offcentral
critical zeros as

```text
rho = 1+i gamma.
```

For a dyadic shell set

```text
S_T = {rho=1+i gamma : T<|gamma|<=2T, rho simple},
X_rho = |L'(E,rho)|^(-1),
R_E,1(T)=sum_(rho in S_T) X_rho.
```

Rank-one H1 simple-zero closure needs exactly

```text
R_E,1(T)=o(T^2).
```

For a separation parameter `c>0`, put

```text
F_T(c) = {rho in S_T :
  dist(rho,Z_E\{rho}) >= c/log T},
B_T(c)=S_T\F_T(c).
```

## Source Anchors

- `H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`:
  rank-one H1 reduces to `R_E,1(T)=o(T^2)`; layer cake is the exact
  reciprocal-tail formulation.
- `AGENT06_H1_RECIPROCAL_DERIVATIVE_TAIL_2026-05-11.md`: not present under
  `primes-equispaced` by `rg --files`; no exact prior packet was available.
- `BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`: separated EC-BFMT at `k=1/2`
  would give
  `sum_(rho in F_T(c)) X_rho <<_(E,c,delta) T^(1+delta)`, conditional on
  local GL2 shift-derivative and prime-polynomial lower-bound inputs.
- `/tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt`: BFMT proves
  zeta negative derivative moment upper bounds on separated zeros; for the
  full zeta zero family, it records a WMC route via convergence of
  `sum 1/(|rho zeta'(rho)|^2)`.
- `/tmp/farey-homogeneous-bfmt-20260511/sheth_ec_arxiv_2312.05236.txt`:
  Theorem 3.1 gives `N_E(t)=alpha_E t(log t+c)/pi+O(log t)`, hence
  `#S_T <<_E T log T`; Corollary 3.2 gives `sum 1/|rho|^2<infinity`.
- `/tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt`:
  supplies fixed-newform zero counts, `S_f(t)=O(log t/loglog t)` on RH,
  positive moments of `L_f'(rho_f)`, and upper large-value estimates for
  shifted `L`; it does not supply an upper negative moment of `L_f'(rho_f)`.

## Tail/Layers Attempt

Define the reciprocal tail count

```text
A_T(V) = #{rho in S_T : X_rho > V}.
```

Layer cake gives the identity

```text
R_E,1(T)=int_0^infinity A_T(V) dV.
```

By Sheth's zero count,

```text
int_0^1 A_T(V) dV <= #S_T <<_E T log T = o(T^2).
```

Therefore the target is equivalent to the high-tail statement

```text
int_1^infinity A_T(V) dV = o(T^2).             (Tail_E)
```

Splitting into separated and complement tails,

```text
A_T(V)=A_F(T,c;V)+A_B(T,c;V),
R_E,1(T)=R_F(T,c)+R_B(T,c).
```

If the conditional EC-BFMT separated theorem is closed, then for any fixed
`delta<1`,

```text
R_F(T,c) <<_(E,c,delta) T^(1+delta)=o(T^2).
```

The remaining condition is exactly

```text
int_1^infinity A_B(T,c;V) dV=o(T^2),
```

or equivalently `R_B(T,c)=o(T^2)`.

Minimum-modulus layer.  For each `rho in B_T(c)` choose a zero-centered disk
of radius `r_rho<=A/log T`, with cluster

```text
C_rho={rho=rho_0,rho_1,...,rho_(k_rho-1)}
```

and no zeros on the boundary.  Let

```text
m_rho = min_(|s-rho|=r_rho) |L(E,s)|,
D_rho = product_(a=1)^(k_rho-1) |rho-rho_a|.
```

Factoring

```text
L(E,s)=(s-rho) product_(a>=1)(s-rho_a) h_rho(s)
```

and applying the maximum principle to `1/h_rho` gives

```text
X_rho <= r_rho (2r_rho)^(k_rho-1)/(m_rho D_rho).       (MM)
```

Thus the complement is controlled if

```text
sum_(rho in B_T(c))
  r_rho (2r_rho)^(k_rho-1)/(m_rho D_rho)
  = o(T^2).
```

For pair clusters, with `d_rho=min_(rho'!=rho)|rho-rho'|`,
`r_rho<=A/logT`, and `m_rho>=h(T)/T`, `h(T)->infinity`,

```text
sum_(rho in B_T(c)) X_rho
  <= 2A^2 T/(h(T)(log T)^2)
     sum_(rho in B_T(c)) 1/d_rho.
```

The inverse-gap layer cake is

```text
sum_(rho in B_T(c)) 1/d_rho
 <= (logT/c) P_T(c/logT)
    + int_(logT/c)^infinity P_T(1/u) du,
```

where `P_T(delta)=#{rho in B_T(c): d_rho<=delta}`.  A GUE-strength pair count

```text
P_T(delta) <<_E T log T (delta log T)^beta,
0<delta<=c/logT, beta>1,
```

then gives `sum 1/d_rho <<_E T(logT)^2`, hence the pair-cluster complement is
`O(T^2/h(T))=o(T^2)`.  The count input alone is insufficient; `(MM)` supplies
the reciprocal cap.

Negative-moment layer.  For any `p>1`, Holder and `#S_T<<TlogT` give

```text
R_E,1(T)
 <= (#S_T)^(1-1/p) (sum_(rho in S_T) X_rho^p)^(1/p).
```

Therefore the stronger sufficient condition

```text
sum_(rho in S_T) |L'(E,rho)|^(-p)
  = o(T^(p+1)/(logT)^(p-1))
```

implies `R_E,1(T)=o(T^2)`.  For `p=2`, it is enough to prove

```text
sum_(rho in S_T) |L'(E,rho)|^(-2)=o(T^3/logT).
```

EC-WMC analogue.  If one could prove the zeta-WMC-style fixed-EC condition

```text
sum_(rho simple) 1/(|rho|^2 |L'(E,rho)|^2) < infinity,
```

then, for the dyadic shell,

```text
R_E,1(T)
 <= (sum_(rho in S_T) 1/(|rho|^2 |L'(E,rho)|^2))^(1/2)
    (sum_(rho in S_T) |rho|^2)^(1/2)
 << o(1) * T^(3/2)(logT)^(1/2)
 = o(T^2).
```

This is a stronger sufficient criterion than the H1 target and is modeled on
the BFMT/Titchmarsh zeta-WMC discussion, but no EC source here proves it.

## Sufficient Criterion

Any one of the following closes the simple-zero rank-one target:

```text
DirectTail(E):
  int_1^infinity #{rho in S_T : |L'(E,rho)|^(-1)>V} dV=o(T^2).
```

```text
SeparatedPlusComplement(E,c):
  SeparatedEC-BFMT(E,c,k=1/2)
  and
  int_1^infinity #{rho in B_T(c) : |L'(E,rho)|^(-1)>V} dV=o(T^2).
```

```text
ClusterMinModBudget(E,c):
  sum_(rho in B_T(c))
    r_rho (2r_rho)^(k_rho-1)/(m_rho D_rho)
  = o(T^2),
  plus the separated EC-BFMT estimate.
```

```text
NegativeMoment_p(E):
  for some p>1,
  sum_(rho in S_T) |L'(E,rho)|^(-p)
  = o(T^(p+1)/(logT)^(p-1)).
```

```text
EC-WMC-ReciprocalSquare(E):
  sum_(rho simple) 1/(|rho|^2 |L'(E,rho)|^2) < infinity.
```

The last two are stronger than needed but have clean one-line implications.

## Source Gap

The missing theorem is not zero count, spacing count, or positive derivative
moment information.  It is an upper tail for reciprocal derivatives.

Current source boundaries:

- Sheth supplies `#S_T<<TlogT` and `sum 1/|rho|^2<infinity`; neither contains
  `L'(rho)`.
- Milinovich-Ng supplies positive moments and shifted-value upper tools. These
  can detect many simple zeros but do not upper-bound
  `sum |L'(rho)|^(-1)`.
- BFMT supplies zeta separated negative moments, and a zeta WMC full-family
  route.  The EC transcription remains conditional, and even if it closes, it
  handles only `F_T(c)`.
- The complement `B_T(c)` still needs a direct reciprocal tail or the local
  minimum-modulus/product-distance budget above.
- Mollified signed reciprocal sums, such as Li-Zaharescu-type `S1`, are not
  absolute tail estimates.  Without a positivity/majorant step they cannot
  control H1 absolute residues.

Exact gap:

```text
prove DirectTail(E)
or prove SeparatedEC-BFMT(E,c,k=1/2) plus the complement tail/minmod budget
or prove a fixed-EC EC-WMC-ReciprocalSquare/negative-moment upper theorem.
```

No generic Cartan/Jensen or selected-height H1 closure was rerun.

## Dependency Impact

- Rank-one H1 simple-zero residues close once any sufficient criterion above
  is proved, because the legal-height packet already reduces H1 to
  `R_E,1(T)=o(T^2)`.
- Separated BFMT progress alone is not enough; the complement remains an
  independent reciprocal-tail input.
- The strongest clean carry-forward target is
  `EC-WMC-ReciprocalSquare(E)` or, less strongly, `NegativeMoment_p(E)` for
  any `p>1`.
- Multiple offcentral zeros are not handled by this packet; they remain under
  the separate Laurent/effective-degree rules.
- H2 branch damping has no role in this H1 reciprocal-pole estimate.
