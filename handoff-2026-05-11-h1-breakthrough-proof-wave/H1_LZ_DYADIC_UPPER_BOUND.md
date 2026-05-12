---
schema_version: 1
title: "H1 Li-Zaharescu dyadic upper-bound attempt"
date: 2026-05-11
agent: "H1 breakthrough proof wave Agent 1"
type: proof-attempt
tier: working
status: NO_GO
confidence: 0.86
dependencies:
  - handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
tags: [ec-ndc, h1, reciprocal-residues, li-zaharescu, no-go]
---

# H1 Li-Zaharescu Dyadic Upper Bound

Status: `NO_GO`.

Confidence: `0.86`.

## Do Not Promote Unless

- A fixed-curve fixed-kernel upper bound is proved for the H1 shell
  `sum_{T<|gamma|<=2T} W_hat(i gamma) exp(i gamma u)/L'(E,1+i gamma)`,
  uniformly in `u`, or an absolute/square-root summable substitute below is
  proved.
- Li-Zaharescu is used only as a contour/mollifier template. Its checked
  theorems do not give the H1 fixed-weight upper bound.
- Any shell statement specifies the Mellin decay exponent `q` of the actual
  fixed kernel and verifies dyadic summability.
- Multiple zeros are ruled out, kernel-killed, retained, or controlled by
  Laurent-coefficient shell bounds for every needed derivative of `W_hat`.
- Positive-rank closure is claimed only after the exact H1 contour tail is
  `o(u^r)` in the same fixed-kernel theorem mode.
- Rank zero is not converted to a pointwise constant; surviving nonzero
  frequencies are retained, filtered with tail proof, or averaged.

## Verdict

The Li-Zaharescu route does not currently produce an H1 reciprocal-residue
upper-bound theorem.

What can be proved locally is the following sharp dyadic reduction: if a new
fixed-curve upper bound for reciprocal derivatives is supplied, then the H1
simple-zero residue aggregate is uniformly bounded in `u` and hence is
harmless for every positive analytic rank `r>=1`.

The genuinely new missing assumption is a fixed-curve shell upper bound such as

```text
J_E,2(T) :=
  sum_{T<|gamma|<=2T, simple} |L'(E,1+i gamma)|^(-2)
  <= C_E T^theta (log T)^B
```

with

```text
theta < 2q - 1,
```

where

```text
|W_hat(i t)| <= C_W (1+|t|)^(-q).
```

For the local smoothstep class `q=2`, this asks for

```text
J_E,2(T) <= C_E T^(3-delta)
```

for some `delta>0`. Li-Zaharescu does not prove this. Their checked result is
mollified and lower-bound oriented, not a full fixed-weight upper bound.

## Local Dyadic Lemma

Let `E/Q` be fixed. Assume all offcentral zeros in the shell are simple. Let

```text
A_T(u) =
  sum_{T<|gamma|<=2T}
    W_hat(i gamma) exp(i gamma u) / L'(E,1+i gamma).
```

Assume the shell zero count as a hypothesis:

```text
N_E(T,2T) := #{gamma: T<|gamma|<=2T} <= C_E T log T.
```

Assume kernel decay on the same dyadic range:

```text
|W_hat(i t)| <= C_W T^(-q),       T<|t|<=2T.
```

Assume the reciprocal-derivative square moment:

```text
J_E,2(T) <= C_E T^theta (log T)^B.
```

Then, uniformly for all real `u`,

```text
|A_T(u)|
  <= C T^((1 - 2q + theta)/2) (log T)^((B+1)/2).
```

Proof:

```text
|A_T(u)|
 <= (sum_shell |W_hat(i gamma)|^2)^(1/2)
    (sum_shell |L'(E,1+i gamma)|^(-2))^(1/2)
 <= (C_W^2 T^(-2q) C_E T log T)^(1/2)
    (C_E T^theta (log T)^B)^(1/2).
```

The phase `exp(i gamma u)` has modulus `1`, so the estimate is fully uniform in
`u`.

The dyadic series over `T=2^n` converges if

```text
1 - 2q + theta < 0,
```

equivalently `theta < 2q-1`. Therefore the simple-zero aggregate

```text
Z_W(u) =
  sum_{gamma != 0}
    W_hat(i gamma) exp(i gamma u) / L'(E,1+i gamma)
```

converges absolutely and uniformly in `u`.

Consequences:

```text
Z_W(u)=O(1) uniformly in u.
```

If analytic rank `r>=1` and the post-residue H1 contour remainder satisfies
`I(u)=o(u^r)`, then

```text
c_E,W(e^u)=Q_E,W(u)+o(u^r).
```

This closes the H1 positive-rank residue part conditionally. It does not prove
the fixed-curve theorem because `J_E,2(T)` is a new input.

## Pointwise Alternative

A pointwise lower derivative hypothesis also works. If

```text
|L'(E,1+i gamma)|^(-1) <= C_E T^A
```

on `T<|gamma|<=2T`, then

```text
sum_shell |W_hat(i gamma)/L'(E,1+i gamma)|
  <= C T^(1 + A - q) log T.
```

Dyadic summability requires

```text
A < q - 1.
```

For `q=2`, this requires `A<1`. This is also a new fixed-curve input. It is
stronger pointwise than the square-moment route and is not supplied by
Li-Zaharescu.

## Square-Summable Substitute

Plain coefficient square-summability

```text
sum_gamma |W_hat(i gamma)/L'(E,1+i gamma)|^2 < infinity
```

is not enough for pointwise positive-rank H1 closure uniformly in `u`. It gives
an averaged/Besicovitch-style target only after adding spacing or Hilbert-type
control.

A square-summable substitute strong enough for pointwise closure is instead
the dyadic root-sum condition

```text
sum_{T dyadic}
  (sum_shell |W_hat(i gamma)|^2)^(1/2)
  (sum_shell |L'(E,1+i gamma)|^(-2))^(1/2)
  < infinity.
```

This is exactly the Cauchy-Schwarz condition above. It is "square" in proof
shape but absolute in conclusion: it implies uniform absolute convergence of
the H1 residue series.

## Multiple Zeros

If `rho=1+i gamma` has multiplicity `m`, write

```text
1/L(E,1+z) =
  sum_{j=1}^m b_(rho,-j) (z-i gamma)^(-j) + holomorphic.
```

Then the H1 residue is

```text
R_rho(u) =
  exp(i gamma u) sum_{ell=0}^{m-1} c_(rho,ell) u^ell,
```

with

```text
c_(rho,ell)
 = (1/ell!) sum_{j=ell+1}^m
     b_(rho,-j) W_hat^(j-1-ell)(i gamma)/(j-1-ell)!.
```

For positive rank `r`, every surviving degree `ell>=r` blocks pointwise H1
closure unless it is kernel-killed, coefficient-cancelled, retained in the
theorem, or averaged with proof.

For `0<=ell<r`, the same dyadic Cauchy-Schwarz argument works only under new
Laurent-coefficient square-moment bounds. If

```text
sum_{T<|gamma|<=2T} |b_(rho,-j)|^2
  <= C_j T^theta_j (log T)^B_j
```

and

```text
|W_hat^(k)(i t)| <= C_k (1+|t|)^(-q_k),
```

then the dyadic contribution to the `ell` coefficient is summable if

```text
theta_j < 2 q_(j-1-ell) - 1
```

for all `j>=ell+1` that can occur. If multiplicity is unbounded, no finite
version of this package closes H1; use the direct coefficient-sum hypothesis
instead.

Kernel zero order matters. If `W_hat` vanishes to order `nu_rho` at
`i gamma`, then the generic effective degree is

```text
m - 1 - nu_rho.
```

Positive-rank pointwise closure needs this effective degree to be `< r`, after
same-frequency combination.

## Why Li-Zaharescu Does Not Give The Bound

The checked Li-Zaharescu theorem controls different objects.

Their main contour sum is a mollified Dirichlet-polynomial sum

```text
S1 =
  sum_{L(rho)=0, T1<rho<T2}
    L'(rho)^(-1) X(rho) Y(1-rho),
```

with `X` and `Y` Dirichlet polynomials of length `M=T^theta`, `theta<1`.

H1 needs the fixed kernel weight

```text
W_hat(i gamma) exp(i gamma u),
```

uniformly in `u`, with no adjustable Dirichlet-polynomial mollifier and no
zero-dependent coefficients.

The transfer gap is fatal:

```text
X(rho)Y(1-rho) approximates W_hat(i gamma) exp(i gamma u)
```

would have to hold on the zero set with error small after multiplication by
`1/L'(rho)`. Proving that weighted approximation error is small already
requires the reciprocal-derivative control sought by H1. Thus the transfer is
circular unless a new theorem supplies a priori control of the bad weights.

The direction is also wrong. Li-Zaharescu use their mollified sums to obtain
negative-moment lower bounds and extreme small values of `L'(rho)`. H1 needs
upper control of reciprocal derivatives on every dyadic shell. A lower bound
for

```text
sum |L'(rho)|^(-2)
```

does not imply an upper bound for the same sum or for the fixed-weight
aggregate.

The simplicity assumption is also insufficient. "Almost all simple" leaves an
exceptional set of multiple zeros. In H1, even one uncancelled multiple zero of
effective degree `>=r` can obstruct pointwise positive-rank closure, and any
multiple zero contributes Laurent coefficients not controlled by the simple
`1/L'(rho)` estimates.

## Uniformity In `u`

Absolute dyadic bounds are automatically uniform in `u`:

```text
|exp(i gamma u)|=1.
```

Any route relying on cancellation among the phases must state the interval of
`u`, the dependence on `T`, and the truncation rule. A bound that holds for
each fixed `u` but loses like `exp(C|u|)` or depends on an unsummable power of
`u` is not enough for H1/H2 positive-rank closure.

The useful target is therefore:

```text
sup_{u in R}
|sum_{T<|gamma|<=2T} W_hat(i gamma) exp(i gamma u)/L'(E,1+i gamma)|
 <= B_T,

sum_{T dyadic} B_T < infinity.
```

This is stronger than needed but theorem-safe. It gives bounded `Z_W(u)` and
therefore `Z_W(u)=o(u^r)` for every `r>=1`.

## Mellin Decay Accounting

Let the fixed kernel have vertical decay `q`:

```text
|W_hat(i t)| <= C (1+|t|)^(-q).
```

Then:

```text
pointwise derivative route:  A < q-1;
square-moment route:         theta < 2q-1.
```

For smoothstep `q=2`:

```text
A<1,     or     theta<3.
```

For a `C^infty`/Schwartz endpoint kernel with super-polynomial Mellin decay,
any fixed polynomial reciprocal-derivative moment would be summable. That is a
different kernel class and must be declared; it cannot be silently substituted
for the current smoothstep theorem mode.

For multiple zeros, every derivative `W_hat^(k)` used in the Laurent residue
needs its own decay exponent `q_k`. Decay of `W_hat` alone does not control the
higher Laurent terms.

## Gap Map

Closed here:

```text
1. A dyadic Cauchy-Schwarz theorem that converts fixed-curve reciprocal
   derivative shell upper bounds into uniform H1 residue control.
2. Exact summability thresholds in terms of q:
   theta < 2q-1 and A < q-1.
3. Multiple-zero Laurent shell thresholds:
   theta_j < 2 q_(j-1-ell)-1 for harmless degrees ell<r.
4. Positive-rank implication:
   uniform bounded residues plus H1 contour tail o(u^r) imply H1 closure.
```

Not closed:

```text
1. Fixed elliptic-curve upper bounds for J_E,2(T).
2. Fixed elliptic-curve pointwise lower bounds for |L'(E,1+i gamma)|.
3. A non-circular approximation of W_hat(i gamma) exp(i gamma u) by
   Li-Zaharescu Dirichlet-polynomial weights with reciprocal-derivative
   weighted error.
4. Treatment of exceptional multiple zeros or Laurent coefficients.
5. Exact same-kernel H1 contour tail and height-avoidance theorem.
6. Rank-zero pointwise stabilization.
```

## Source Packet

Only Li-Zaharescu is cited as an external theorem source here. All dyadic
estimates above are local Cauchy-Schwarz reductions, not external theorem
claims.

Run directory:

```bash
/tmp/h1-lz-dyadic-agent1
```

Fetch and extract:

```bash
curl -L --fail -o li_zaharescu_Lprime_rho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
/tmp/h1-source-audit-20260511/xpdf-tools-mac-4.06/binARM/pdftotext \
  -layout -enc UTF-8 li_zaharescu_Lprime_rho.pdf \
  li_zaharescu_Lprime_rho.utf8.txt
```

SHA256:

```text
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011
```

Text-layer note: the extracted PDF text drops the prime glyph in many places,
rendering `L'(rho)` as `L (rho)`. The title, formulas, and context identify
the derivative object.

Verified hooks:

- PDF p. 2, Theorem 1.1. Quote: "lower bound for the negative moment".
- PDF p. 4, equations (9)-(11). Quote: "mollified moments".
- PDF p. 7, Theorem 4.1. Quote: "almost all zeros of L(s) are simple".
- PDF p. 7, Theorem 4.1. Quote: "theta < 1".

Use: source for the adjacent Li-Zaharescu contour/mollifier template.

Limit: no fixed H1 weight, no uniform-in-`u` dyadic upper bound, no full
simple-zero theorem, no multiple-zero Laurent control.

## Changed Paths

- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md`
