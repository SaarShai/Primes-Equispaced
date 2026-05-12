---
schema_version: 1
title: "H1 weighted-l1 attack packet"
date: 2026-05-11
type: theorem-reduction
tier: working
status: REFINED_TARGET_NO_THEOREM_PROMOTED
confidence: 0.82
sources:
  - handoff-2026-05-11-all-in-wave/H1_SHELL_ANTI_SMALL_DERIVATIVE_PACKET_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/H1_FIXED_WEIGHT_PV_PACKET_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_ANALYTIC_ATTEMPT.md
  - handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md
tags: [ec-ndc, h1, weighted-l1, reciprocal-derivative, positive-rank]
---

# H1 Weighted-l1 Attack Packet

status: `REFINED_TARGET_NO_THEOREM_PROMOTED`

## Verdict

No fixed-curve H1 theorem is promoted. The useful progress is a sharper target
hierarchy.

The previous sufficient target

```text
R_E,1(T) =
  sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-1)
  <= C_E T^(2-epsilon)
```

is enough for smoothstep-scale `|W_hat(it)| << |t|^(-2)`, but it is stronger
than the actual positive-rank need. For positive rank, H1 only needs the
weighted offcentral residue aggregate to be `o(u^r)` along the same finite-box
Perron heights.

## Setup

Let

```text
u = log K,
r = ord_{s=1} L(E,s) >= 1,
A_W(T) =
  sum_{T<|gamma|<=2T, simple}
    |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1).
```

For smoothstep-scale kernels:

```text
|W_hat(i gamma)| << |gamma|^(-2),
so A_W(T) << T^(-2) R_E,1(T).
```

Let `T_box(u)` be the height cutoff used by the H1 finite-box Perron identity.
The simple-zero offcentral absolute majorant up to that height is

```text
M_W(u) =
  sum_{2^j <= T_box(u)} A_W(2^j).
```

A clean positive-rank sufficient condition is:

```text
M_W(u) = o(u^r).        (H1-l1-growth)
```

This is weaker than absolute convergence of the full residue series.

## Target Hierarchy

For smoothstep-scale `q=2`, the following implications hold:

```text
R_E,1(T) <= C T^(2-epsilon)
  => A_W(T) <= C T^(-epsilon)
  => sum_j A_W(2^j) < infinity
  => M_W(u)=O(1)=o(u^r).
```

But absolute convergence already follows from the weaker log-saving target

```text
R_E,1(T) <= C T^2 (log T)^(-1-delta).       (H1-l1-log-save)
```

because

```text
A_W(2^j) << j^(-1-delta),
sum_j j^(-1-delta) < infinity.
```

For positive rank only, even this can be weakened if `T_box(u)` is controlled.
If

```text
R_E,1(T) <= C T^2 (log T)^B,                (H1-l1-polylog-loss)
```

then

```text
A_W(2^j) << j^B,
M_W(u) << (log T_box(u))^(B+1).
```

Thus `H1-l1-growth` follows whenever

```text
(log T_box(u))^(B+1) = o(u^r).
```

Examples:

```text
T_box(u) <= u^M:
  any fixed B is harmless for every r>=1.

T_box(u) <= exp(u^beta):
  need beta(B+1) < r.
```

This does not remove the contour-tail problem: `T_box(u)` must still be legal
for the same H1 Perron shift and horizontal height bounds. It only refines the
offcentral residue size target.

## Exact Conditional Closure

Assume:

1. the finite-box reciprocal Perron identity is proved for the chosen `W`;
2. central algebra is normalized, so the leading central term is
   `u^r/L^(r)(E,1)`;
3. all multiple-zero effective residue degrees are `< r`, killed, retained, or
   handled in a declared averaged/profile mode;
4. contour tails are `o(u^r)` along `T_box(u)`;
5. simple-zero residue majorant satisfies `H1-l1-growth`.

Then the simple offcentral residues are `o(u^r)` absolutely:

```text
|sum_{0<|gamma|<=T_box(u)}
  W_hat(i gamma) e^(i gamma u)/L'(E,1+i gamma)|
<= M_W(u) = o(u^r).
```

Combined with the finite-box identity:

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r),       r>=1.
```

This is a theorem reduction, not a theorem closure: the reciprocal-derivative
growth input and the finite-box contour theorem remain unproved in current
sources.

## Equivalent Tail Criteria

Let

```text
R(gamma)=|L'(E,1+i gamma)|^(-1),
N_E(T;V)=#{T<|gamma|<=2T: R(gamma)>V}.
```

Layer cake gives

```text
R_E,1(T) <= N_E(T,2T) + int_1^infty N_E(T;V) dV.
```

So each of the following is sufficient:

### Polynomial Saving

```text
N_E(T;V) <= C T^(2-epsilon) V^(-1-alpha),  V>=1.
```

Then `R_E,1(T) << T^(2-epsilon)`.

### Log Saving

```text
N_E(T;V) <= C T^2 (log T)^(-1-delta) V^(-1-alpha),  V>=1.
```

Then `H1-l1-log-save` holds.

### Capped Borderline Tail

For `1<=V<=T^A`,

```text
N_E(T;V) <= C T^2 (log T)^(-2-delta) V^(-1),
R(gamma) <= T^A.
```

Then

```text
R_E,1(T) << T^2 (log T)^(-1-delta)
```

after the layer-cake logarithm, hence absolute convergence of the weighted
residue series.

### Finite-Box Growth Tail

If

```text
N_E(T;V) <= C T^2 (log T)^B V^(-1-alpha)
```

then `R_E,1(T) << T^2 (log T)^B`, and positive-rank H1 still closes whenever
`(log T_box(u))^(B+1)=o(u^r)`.

## Pointwise Derivative Route

The pointwise lower bound

```text
|L'(E,1+i gamma)| >= c T^(-1) (log T)^(1+delta)
```

already gives

```text
R_E,1(T) << T^2 (log T)^(-delta)
```

up to the standard zero count `N_E(T,2T)<<T log T`. For absolute convergence
via `H1-l1-log-save`, one needs slightly more:

```text
|L'(E,1+i gamma)| >= c T^(-1) (log T)^(2+delta).
```

For finite-box positive-rank closure with polynomial `T_box(u)`, even

```text
|L'(E,1+i gamma)| >= c T^(-1) (log T)^(-B)
```

can be enough, because it gives only a polylogarithmic residue majorant.

This is still a genuine anti-small-derivative theorem. It is just weaker than
the earlier `T^(-1+eta)` pointwise route.

## Local Minimum-Modulus Route

For a simple zero `rho=1+i gamma`, suppose there is a zero-free circle

```text
|s-rho| = r_T = T^(-kappa) (log T)^(-b)
```

and

```text
min_{|s-rho|=r_T} |L(E,s)|
  >= c T^(-mu) (log T)^(-B).
```

Then, writing `L(E,s)=(s-rho)g(s)` and applying maximum modulus to `1/g`,

```text
|L'(E,rho)| = |g(rho)|
  >= c T^(-(mu-kappa)) (log T)^(-(B-b)).
```

Thus the log-saving l1 route only needs:

```text
mu-kappa <= 1
and enough logarithmic surplus in b-B.
```

The older polynomial-saving route needed `mu-kappa<1`. The boundary case
`mu-kappa=1` is still useful if logarithms are favorable.

## What Still Does Not Work

The following do not prove the needed H1 input by themselves:

- RH/no-right-half-zero;
- zero counting;
- all zeros simple;
- spacing or pair correlation alone;
- positive moments of `L'(rho)`;
- RMT heuristics;
- Li-Zaharescu selected horizontal heights;
- fixed-weight mollifier transfer with signed errors;
- H2/S1 branch damping.

Reason: none prevents a sparse set of simple zeros with very small derivative
unless it includes a small-derivative tail, a pointwise lower bound, or a
local minimum-modulus theorem at the zeros.

## Best Next Proof Target

The narrowest useful theorem to attack is now:

```text
H1-l1-growth(E,W,r,T_box):
  sum_{2^j <= T_box(u)}
    sum_{2^j<|gamma|<=2^(j+1)}
      |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1)
  = o(u^r).
```

For smoothstep-scale kernels this can be discharged by any of:

```text
R_E,1(T) <= C T^(2-epsilon)
R_E,1(T) <= C T^2 (log T)^(-1-delta)
R_E,1(T) <= C T^2 (log T)^B with controlled T_box(u)
```

This is the current best H1 target because it matches the positive-rank
central scale directly and avoids demanding the stronger `J_E,2(T)` unless
Cauchy-Schwarz is the only available route.
