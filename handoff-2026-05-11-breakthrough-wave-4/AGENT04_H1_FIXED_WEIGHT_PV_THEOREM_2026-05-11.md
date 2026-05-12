---
title: "AGENT04 H1 fixed-weight PV theorem"
date: 2026-05-11
status: CONDITIONAL_THEOREM
tags: [h1, fixed-weight-pv, elliptic-curve, reciprocal-derivative, dyadic-window, breakthrough-wave-4]
---

# Verdict

`CONDITIONAL_THEOREM`.

No unconditional fixed-curve EC theorem is promoted.  The deterministic closure
is a uniform dyadic-window theorem for the actual fixed coefficients

```text
a_gamma = W_hat(i gamma) / L'(E,1+i gamma).
```

The load-bearing hypothesis is not EC smoothing, not finite C2 gates, and not a
spacing or moment surrogate.  It is the actual shell maximal cancellation
budget below.  Existing anchors do not prove that budget.

# Theorem Target

Fix an elliptic curve `E/Q`, analytic rank

```text
r = ord_(s=1) L(E,s) >= 1,
u = log K,
```

and a fixed endpoint kernel `W` with the same H1 contour normalization and
vertical decay used in the prior packets:

```text
W_hat(z) = 1/z + O(1) near z=0,
|W_hat(i t)| <<_W (1+|t|)^(-2).
```

For simple offcentral zeros `rho=1+i gamma`, `gamma != 0`, set

```text
a_gamma = W_hat(i gamma) / L'(E,1+i gamma).
```

For a legal contour height function

```text
H(U) = exp(CU+O(1))
```

define the symmetric finite principal-value truncation

```text
Z_H(u) =
  sum_(0<|gamma|<=H(U), simple) a_gamma e^(i gamma u).
```

Target:

```text
sup_(u in [U,2U]) |Z_H(u)| = o(U^r).
```

For `r=1`, this is exactly the rank-one H1 offcentral scale needed to make the
fixed-weight zero residue contribution lower order than the central term.

# Source Anchors

- `primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`: absolute rank-one route is `R_E,1(T)=o(T^2)`; fixed-weight PV is a separate theorem.
- `primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT05_H1_PV_CANCELLATION_FRONTIER_2026-05-11.md`: not present under that path after `rg --files`; nearest present PV packets are the next two anchors.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT02_H1_FIXED_WEIGHT_PV_2026-05-11.md`: pointwise uniform PV is `NO_GO` from current spacing and `l2` inputs; direct shell target `B_E,W(T,U)` is named.
- `primes-equispaced/handoff-2026-05-11-all-in-wave/H1_FIXED_WEIGHT_PV_PACKET_2026-05-11.md`: same fixed-weight PV obstruction and profile/product-average substitutes.
- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`: conditional separated-zero reciprocal derivative estimate; bad set remains independent.
- `/tmp/farey-homogeneous-bfmt-20260511/sheth_ec_arxiv_2312.05236.txt`: supplies RH zero count scale and `sum_rho |rho|^(-2)<infty`; it does not control `1/L'(rho)` or fixed-weight PV.

# Deterministic PV Candidate

Name:

```text
H1-UDW-PV(E,W,r;H)
```

For dyadic `T`, define the actual shell maximal function

```text
B_E,W(T,U) =
  sup_(u in [U,2U])
  | sum_(T<|gamma|<=2T, simple)
      W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma) |.
```

Hypotheses:

```text
H0. Legal H1 finite-box contour identity holds with height H(U)=exp(CU+O(1)),
    and shifted-line, horizontal, original-line, and indentation remainders are
    o(U^r) uniformly for u in [U,2U].

H1. Offcentral multiple-zero Laurent terms are absent, kernel-killed, retained
    outside this theorem, or have effective polynomial degree < r.

H2. Actual fixed-coefficient dyadic-window budget:

    sum_(T dyadic, 1<=T<=H(U)) B_E,W(T,U) = o(U^r).
```

Then

```text
sup_(u in [U,2U]) |Z_H(u)| = o(U^r),
```

and the H1 contribution satisfies

```text
c_E,W(e^u) =
  Q_E,W(u) + o(U^r)
```

uniformly for `u in [U,2U]`, where `Q_E,W` is the central zero polynomial with
leading term `u^r/L^(r)(E,1)` under the chosen normalization.

Proof is deterministic: decompose `Z_H` into dyadic shells and apply the
triangle inequality to the finite shell maximal functions.  H0 and H1 then
insert this PV bound into the already-isolated finite-box H1 contour identity.

Checkability: for fixed `U,T`, `B_E,W(T,U)` is a finite exponential-polynomial
supremum over the computed zeros in that shell.  If

```text
A_E,W(T) =
  sum_(T<|gamma|<=2T, simple) |W_hat(i gamma)/L'(E,1+i gamma)|,
```

then the shell derivative is bounded by `2T A_E,W(T)`, so a mesh of
`[U,2U]` certifies `B_E,W(T,U)` to any prescribed finite tolerance.  This is
only a deterministic certification mechanism for the named hypothesis; finite
certificates do not imply the asymptotic theorem.

BFMT split corollary:

Fix `c>0` and let `F_E(T,c)` be the separated simple-zero set.  Assume the
conditional separated estimate

```text
sum_(gamma in F_E(T,c)) |L'(E,1+i gamma)|^(-1)
  <<_(E,c,delta) T^(1+delta)       for every fixed delta>0,
```

and define `B_E,W^bad(T,U;c)` by restricting the shell sum to
`gamma notin F_E(T,c)`.  If

```text
sum_(T dyadic, 1<=T<=H(U)) B_E,W^bad(T,U;c) = o(U^r),
```

then `H1-UDW-PV(E,W,r;H)` follows.  Indeed the separated part is absolutely
bounded by

```text
T^(-2) * T^(1+delta) = T^(-1+delta),
```

which is dyadically summable for any fixed `delta<1`.  Thus all nontrivial PV
work is pushed onto the close-zero/bad set.

# Obstruction Model

Spacing plus `l2` or profile-scale shell moments cannot imply H2.

For any `alpha in (1/2,1]`, set

```text
gamma_n = n,
a_n = a_(-n) = 1/(2 n^alpha).
```

Then the frequencies have perfect unit spacing and

```text
sum_n |a_n|^2 < infinity.
```

If `|W_hat(i n)| ~ n^(-2)`, this model corresponds to reciprocal-derivative
sizes `|L'(rho_n)|^(-1) ~ n^(2-alpha)`, giving the profile-threshold shell
scale

```text
sum_(T<n<=2T) |L'(rho_n)|^(-2) ~ T^(5-2 alpha) < T^4.
```

So it satisfies the smoothstep `B^2` threshold `theta<4` from the earlier PV
packets.

But for every large `U`, the interval `[U,2U]` contains a point
`u=2 pi m`.  At that point,

```text
sum_(T<n<=2T) a_n e^(i n u) + a_(-n)e^(-i n u)
  ~
    T^(1-alpha)       if alpha<1,
    log 2             if alpha=1.
```

Summing dyadic shells up to `H(U)=exp(CU+O(1))` gives exponential growth in
`U` for `alpha<1`, and size `asymp U` for `alpha=1`.  Hence the required
uniform dyadic PV bound fails; at the endpoint `alpha=1` it fails exactly at
rank-one scale.

This is not an EC counterexample.  It is a sharp logical obstruction: any
argument using only zero spacing, zero count, simple zeros, pair correlation,
or square-summable/profile-size coefficients would prove a false statement in
this model.  A real proof must use arithmetic phase information in the actual
coefficients `W_hat(i gamma)/L'(E,1+i gamma)`.

# Dependency Impact

- Current H1 pointwise closure remains conditional on `H1-UDW-PV(E,W,r;H)` or
  a stronger absolute route such as `R_E,1(T)=o(T^2)` in rank one.
- Conditional BFMT separated-zero control, if fully source-closed, makes the
  separated zeros absolutely harmless and reduces PV work to the close-zero
  bad set.
- Sheth/Gallagher zero-count and finite-log-exception tools help contour and
  explicit-formula estimates; they do not estimate `L'(E,1+i gamma)` or the
  fixed-weight Fourier supremum.
- H2 branch damping, EC smoothing, finite numerical C2 gates, and
  Besicovitch/profile convergence do not promote the pointwise PV theorem.
