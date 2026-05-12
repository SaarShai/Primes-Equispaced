---
schema_version: 1
title: "H1 legal-height weighted-l1 closure"
date: 2026-05-11
type: theorem-reduction
tier: working
status: REFINED_TARGET_NO_THEOREM_PROMOTED
confidence: 0.84
sources:
  - handoff-2026-05-11-all-in-wave/H1_WEIGHTED_L1_ATTACK_PACKET_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
  - handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md
  - handoff-2026-05-11-gpt55-extra-high-continuation/H1_LZ_HEIGHT_VERIFICATION_2026-05-11.md
tags: [ec-ndc, h1, legal-heights, weighted-l1, reciprocal-derivative]
---

# H1 Legal-Height Weighted-l1 Closure

status: `REFINED_TARGET_NO_THEOREM_PROMOTED`

## Verdict

No fixed-curve H1 theorem is promoted.

The useful new refinement is that the current legal moving-box contour regime is
exponential in `u=log K`, not polynomial, if the H1 Perron identity starts from
the source-safe absolute-convergence line `sigma>1/2` and uses the fixed
smoothstep-scale decay `q=2`.

Under that legal-height regime, the positive-rank weighted-l1 target becomes
rank-thresholded:

```text
R_E,1(T) = o(T^2 (log T)^(r-1))
```

is sufficient for the simple-zero weighted residue aggregate to satisfy

```text
M_W(u)=o(u^r).
```

More quantitatively,

```text
R_E,1(T) <= C T^2 (log T)^B
```

suffices whenever

```text
B < r-1.
```

The borderline `B=r-1` needs a little-o improvement or another saving. This is
strictly weaker than the old absolute-convergence target when `r>=1`, but it is
still a real reciprocal-derivative theorem and remains unproved in the checked
sources.

## Legal Moving Height

Use the existing H1 contour setup:

```text
c_E,W(e^u) = (1/(2 pi i)) int_(Re z=sigma)
  e^(uz) W_hat(z)/L(E,1+z) dz,
```

with smoothstep-scale

```text
|W_hat(x+it)| << (1+|t|)^(-q),     q=2.
```

The contour-tail packet records that the safe absolute-convergence start is

```text
sigma > 1/2.
```

If `0<sigma<=1/2`, the Perron identity itself becomes a new analytic input, not
a source-safe consequence of absolute convergence.

Original-line truncation gives

```text
Tail_sigma(T,u) << e^(sigma u) T^(1-q).
```

For `q=2`, a moving-box theorem needs

```text
e^(sigma u) T(u)^(-1) = o(u^r),
```

so polynomial `T(u)` is not legal in the current pointwise moving-box mode.

The conditional Li-Zaharescu height packet gives legal selected heights in each
large unit interval with reciprocal horizontal bound

```text
M(T) <= exp(A_E log T / log log T)=T^o(1).
```

Therefore one may choose, conditionally on that contour-height input,

```text
T_box(u) in [exp(Cu), exp(Cu)+1]
```

with fixed

```text
C > sigma.
```

Then original-line, horizontal, and shifted-left tails are compatible with
`o(u^r)`:

```text
Tail_sigma(T_box,u) << exp((sigma-C)u) = o(u^r),
```

and for any small epsilon with `C(2-epsilon)>sigma`,

```text
H_horiz(T_box,u) << exp((sigma-C(2-epsilon))u)=o(u^r).
```

The shifted-left line is already closed by `eta>1/2` in the reciprocal-strip
packet.

This does not prove H1: Li-Zaharescu selected heights only address contour
height, not reciprocal residues, principal values, or multiple-zero Laurent
coefficients.

## Weighted-l1 Consequence

Let

```text
r = ord_(s=1) L(E,s) >= 1,
A_W(T) =
  sum_(T<|gamma|<=2T, simple)
    |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1),
```

and

```text
M_W(u) = sum_(2^j <= T_box(u)) A_W(2^j).
```

For `q=2`,

```text
A_W(T) << T^(-2) R_E,1(T),
R_E,1(T)=sum_(T<|gamma|<=2T) |L'(E,1+i gamma)|^(-1).
```

If

```text
R_E,1(T)=o(T^2 (log T)^(r-1)),
```

then

```text
A_W(2^j)=o(j^(r-1)).
```

Since the legal moving height has

```text
log T_box(u) = C u + O(e^(-Cu)),
```

the number of dyadic shells is `N(u)=O(u)`. Positivity gives the summation
lemma

```text
sum_(j<=N) o(j^(r-1)) = o(N^r),
```

hence

```text
M_W(u)=o(u^r).
```

This is exactly the simple-zero positive-rank condition needed by the weighted
l1 packet and the positive-rank closure packet.

## Rank Table

For a power-log shell bound

```text
R_E,1(T) <= C T^2 (log T)^B,
```

the legal exponential height gives

```text
M_W(u) <<
  1,                  B < -1,
  log u,              B = -1,
  u^(B+1),            B > -1.
```

Thus:

| rank `r` | sufficient finite-box target |
|---:|---|
| `1` | `R_E,1(T)=o(T^2)`; any log saving `T^2/(log T)^delta`, `delta>0`, suffices |
| `2` | `R_E,1(T)<=C T^2 (log T)^B` for any `B<1`; in particular `O(T^2)` suffices |
| `r>=3` | `R_E,1(T)<=C T^2 (log T)^B` for any `B<r-1` |

Absolute convergence remains stronger:

```text
R_E,1(T) <= C T^2 (log T)^(-1-delta)
```

gives a bounded full simple-zero residue series and does not need the moving
finite-box rank threshold.

## What This Corrects

The earlier weighted-l1 packet correctly observed that if

```text
T_box(u) <= u^M,
```

then any fixed polylogarithmic loss in `R_E,1(T)` is harmless for positive rank.

That observation is not currently usable for the source-safe H1 moving-box
contour theorem, because the existing absolute-convergence start line
`sigma>1/2` forces exponential `T_box(u)` when `q=2`.

Polynomial `T_box(u)` would require a new theorem mode, for example:

```text
sigma=sigma(u)=O(log u/u)
```

with uniform Perron/Mellin inversion and start-line reciprocal bounds near
`Re s=1`, or a limit-first theorem with absolute convergence of the full
residue series. Neither is presently supplied by the checked packets.

## Remaining Blockers

This packet only narrows the simple-zero reciprocal-derivative target. It does
not close:

- fixed-curve bounds for `R_E,1(T)`;
- multiple-zero effective-degree and Laurent-coefficient control;
- fixed-weight principal-value cancellation as an alternative to absolute l1;
- the exact smoothstep H1 Perron identity outside the declared contour
  hypotheses;
- H2/S1/Sym2 endpoint closure in the same pointwise theorem mode;
- rank-zero pointwise stabilization.

## Best Next Target

For positive analytic rank `r`, the narrowest current H1 simple-zero target is:

```text
H1-legal-l1-rank-threshold(E,W,r):
  R_E,1(T) = o(T^2 (log T)^(r-1)).
```

For rank one this is the especially clean anti-small-derivative target:

```text
R_E,1(T)=o(T^2).
```

It is weaker than absolute convergence and weaker than the old polynomial
saving target, but it still requires a genuine fixed-curve theorem controlling
small values of `L'(E,1+i gamma)`.
