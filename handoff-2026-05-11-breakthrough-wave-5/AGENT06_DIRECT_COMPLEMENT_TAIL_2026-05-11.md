---
title: "AGENT06 direct complement tail"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.88
tags: [breakthrough-wave-5, h1, direct-tail, reciprocal-derivative, negative-moments, wmc, mollifiers, bad-set]
---

## Verdict

Status: `RIGOROUS_REDUCTION`.

No direct complement theorem is source-closed from the listed anchors.

The bypass target

```text
sum_(rho in B_E(T,c)) |L'(E,rho)|^(-1) = o(T^2)
```

is exactly equivalent to an integrated reciprocal tail on bad zeros.  It would
follow from any fixed-curve negative moment, EC-WMC reciprocal-square analogue,
or genuine mollifier majorant listed below.  None is present in the available
sources.  Milinovich-Ng gives positive derivative/shifted-value moments for
fixed newforms, not reciprocal derivative upper tails.  BFMT gives zeta
negative moments on separated zeros and a zeta WMC full-family route, not the
fixed-EC bad-set input.

## Theorem Target

Fix an elliptic curve `E/Q` and `c>0`.  In the project normalization write
simple critical zeros as

```text
rho = 1+i gamma.
```

For a dyadic shell,

```text
S_E(T) = {rho=1+i gamma simple : T<|gamma|<=2T},
F_E(T,c) = {rho in S_E(T) : dist(rho,Z_E\{rho}) >= c/log T},
B_E(T,c) = S_E(T)\F_E(T,c).
```

Put

```text
X_rho = |L'(E,rho)|^(-1),
R_B(T,c) = sum_(rho in B_E(T,c)) X_rho.
```

The direct complement target is

```text
DirectComplementTail(E,c):  R_B(T,c)=o(T^2).
```

This packet deliberately does not use the MinMod/ProductLayer cluster
factorization.  It attacks `R_B(T,c)` only through reciprocal tails, negative
moments, WMC-type weighted reciprocal squares, and mollifier-majorant criteria.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT05_H1_RECIPROCAL_TAIL_THEOREM_2026-05-11.md`:
  identifies the global rank-one H1 condition
  `sum_(S_E(T)) |L'(E,rho)|^(-1)=o(T^2)` and states direct tail, negative
  moment, and EC-WMC sufficient forms.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT03_EC_BFMT_BADSET_BUDGET_2026-05-11.md`:
  closes the bad set only conditionally through local minimum modulus plus
  inverse-product layer cake; this route is excluded for the present packet.
- `primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`:
  gives the layer-cake frontier and shows zero count handles only the
  `0<=X_rho<=1` part.
- `/tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt`:
  Theorems 1.1-1.2 prove zeta negative derivative moments on separated zero
  families; Section 1.2 records that WMC implies convergence of
  `sum 1/(|rho zeta'(rho)|^2)` and then full-family zeta negative-moment
  bounds.
- `/tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt`:
  Theorems 1.2-1.4 give fixed-newform lower/upper positive derivative moments
  and shifted-value large-value estimates under GRH.  They do not give
  negative moments of `L'(rho,f)` or reciprocal tails.

## Direct Tail Attempt

Define the bad-set reciprocal tail

```text
A_B(T,c;V) = #{rho in B_E(T,c) : X_rho > V}.
```

For nonnegative `X_rho`,

```text
R_B(T,c) = int_0^infinity A_B(T,c;V) dV.
```

The zero-count bound inherited in the rank-one frontier gives

```text
int_0^1 A_B(T,c;V) dV <= #S_E(T) <<_E T log T = o(T^2).
```

Therefore the direct complement theorem is equivalent to

```text
int_1^infinity A_B(T,c;V) dV = o(T^2).          (BadTail)
```

This is the exact direct bypass of MinMod/ProductLayer.

Negative moments give a clean sufficient condition.  For any `p>1`, Holder
gives

```text
R_B(T,c)
 <= (#B_E(T,c))^(1-1/p)
    (sum_(rho in B_E(T,c)) X_rho^p)^(1/p).
```

Since `#B_E(T,c) <= #S_E(T) <<_E T log T`, it is enough to prove

```text
sum_(rho in B_E(T,c)) |L'(E,rho)|^(-p)
  = o(T^(p+1)/(log T)^(p-1))                 (NegMom_B,p)
```

for one fixed `p>1`.  More sharply, if `M_B(T,c)=#B_E(T,c)`, the exact Holder
threshold is

```text
sum_(rho in B_E(T,c)) X_rho^p
  = o(T^(2p)/M_B(T,c)^(p-1)).
```

The WMC analogue is also direct.  Let

```text
W_B(T,c) =
  sum_(rho in B_E(T,c)) 1/(|rho|^2 |L'(E,rho)|^2).
```

Then Cauchy's inequality gives

```text
R_B(T,c)
 <= W_B(T,c)^(1/2)
    (sum_(rho in B_E(T,c)) |rho|^2)^(1/2)
 <<_E W_B(T,c)^(1/2) T^(3/2)(log T)^(1/2).
```

Thus the direct complement follows from the dyadic weighted condition

```text
W_B(T,c) = o(T/log T).                         (WeightedRecipSquare_B)
```

A fixed-EC WMC-style convergence theorem

```text
sum_(rho simple) 1/(|rho|^2 |L'(E,rho)|^2) < infinity
```

would imply `W_B(T,c)=o(1)`, hence much more than needed.

Mollifiers do not close the target unless they produce a pointwise or
exception-controlled reciprocal majorant.  A sufficient mollifier theorem would
be:

```text
exists M_rho with |1-L'(E,rho)M_rho| <= 1/2 for all rho in B_E(T,c)
and sum_(rho in B_E(T,c)) |M_rho| = o(T^2).
```

Then `X_rho <= 2|M_rho|` on `B_E(T,c)`.  Mean-square mollifier approximation
alone is not enough: a small exceptional set can still carry arbitrarily large
`|L'(E,rho)|^(-1)` and dominate the absolute H1 residue sum.

## Candidate Sufficient Criteria

Any one of the following closes `DirectComplementTail(E,c)` without
MinMod/ProductLayer:

```text
BadTail(E,c):
  int_1^infinity #{rho in B_E(T,c): |L'(E,rho)|^(-1)>V} dV=o(T^2).
```

```text
PowerTail_B(E,c):
  A_B(T,c;V) <= C_E T^2 Phi(T)^(-1) V^(-1-alpha)
  for all V>=1, with alpha>0 and Phi(T)->infinity.
```

```text
BorderlineCappedTail_B(E,c):
  A_B(T,c;V) <= C_E T^2 Phi(T)^(-1) V^(-1), 1<=V<=T^A,
  X_rho <= T^A on B_E(T,c),
  and Phi(T)/log T -> infinity.
```

```text
NegMom_B,p(E,c):
  for some p>1,
  sum_(rho in B_E(T,c)) |L'(E,rho)|^(-p)
    = o(T^(p+1)/(log T)^(p-1)).
```

```text
WeightedRecipSquare_B(E,c):
  sum_(rho in B_E(T,c)) 1/(|rho|^2 |L'(E,rho)|^2)
    = o(T/log T).
```

```text
EC-WMC-ReciprocalSquare(E):
  sum_(rho simple) 1/(|rho|^2 |L'(E,rho)|^2) < infinity.
```

```text
MollifierMajorant_B(E,c):
  construct M_rho with pointwise reciprocal control
  |1-L'(E,rho)M_rho| <= 1/2 on B_E(T,c)
  and sum_(B_E(T,c)) |M_rho|=o(T^2).
```

## Source Gap or Closure

No closure from the listed sources.

Exact fixed-curve source gap:

```text
prove one fixed-EC bad-set reciprocal upper-tail theorem:
  BadTail(E,c)
  or NegMom_B,p(E,c) for some p>1
  or WeightedRecipSquare_B(E,c)
  or EC-WMC-ReciprocalSquare(E)
  or a true MollifierMajorant_B(E,c).
```

Why the anchors do not supply it:

- BFMT is a zeta theorem.  Its negative moment estimates are restricted to
  separated zero families `F` or `F_enl`; its full-family route is conditional
  on zeta WMC and uses convergence of `sum 1/(|rho zeta'(rho)|^2)`.
- Milinovich-Ng is fixed-newform and close in family type, but its theorems are
  positive moments of `L'(rho_f,f)` and positive shifted moments
  `L(rho_f+w,f)`.  Positive moments and large-value estimates do not upper-bound
  reciprocal derivatives.
- The existing bad-set packet proves only a conditional cluster theorem using
  minimum modulus and product-distance layer cake.  That is exactly the route
  this task asked to bypass.
- Zero count, simple-zero density, close-pair counts, and shifted-value upper
  tails do not prevent a sparse set of bad zeros from having huge
  `|L'(E,rho)|^(-1)`.
- Signed or mollified sums cannot replace the absolute H1 majorant unless a
  separate positivity/majorant or exception-tail theorem is supplied.

Thus the direct complement theorem remains unproved.  The blocker is not an
epsilon bookkeeping issue; it is the absence of a fixed-curve reciprocal
derivative tail theorem on `B_E(T,c)`.

## Dependency Impact

- Agents 04-05 remain necessary for the current conditional bad-set path unless
  an external fixed-EC reciprocal-tail theorem is added.
- A proof of `NegMom_B,p`, `WeightedRecipSquare_B`, or
  `EC-WMC-ReciprocalSquare` would bypass MinMod/ProductLayer entirely and feed
  directly into the H1 finite-box closure.
- Separated EC-BFMT alone still cannot close rank-one H1: it controls only
  `F_E(T,c)`, while this packet shows the exact independent condition needed on
  `B_E(T,c)`.
- The highest-leverage source hunt is a fixed-newform reciprocal derivative
  moment theorem or an EC analogue of the zeta WMC implication
  `sum 1/(|rho L'(rho)|^2)<infinity`.
