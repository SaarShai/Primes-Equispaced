---
schema_version: 1
title: "H1 contour tail and height avoidance"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
dependencies:
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md
tags: [ec-ndc, h1, contour-shift, height-avoidance]
---

# H1 Contour Tail And Height Avoidance

Confidence: 0.84.

Dependencies:
- `handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md`
- Same H1 object:
  `c_E,W(e^u)=(1/(2 pi i)) int e^(uz) W_hat(z)/L(E,1+z) dz`.
- Same analytic rank convention: `r=ord_{s=1} L(E,s)`.

## Do Not Promote Unless

- The initial line `Re z=sigma` is in a declared half-plane where the
  reciprocal Dirichlet series/Mellin inversion is justified. In the
  unnormalized EC local convention this is safely `sigma>1/2`, not merely
  `sigma>0`, unless a nonabsolute Perron theorem is proved.
- The fixed kernel has the stated vertical Mellin decay on the whole crossed
  strip. Smoothstep evidence gives only polynomial decay, effectively `q=2`.
- A legal height sequence is not enough. One needs a quantitative bound for
  `sup_{-eta<=x<=sigma} |1/L(E,1+x+iT_n)|`.
- The shifted line `Re z=-eta` is zero-free, indented with controlled errors,
  or interpreted by an explicitly proved principal-value theorem.
- Every crossed zero with `Re(rho)>1` is ruled out by hypothesis/source or kept
  as an exponentially growing residue.
- Offcentral reciprocal Laurent coefficients are controlled separately.
  Horizontal height avoidance does not bound `1/L'(rho)` or higher Laurent
  coefficients.
- Pointwise H1 closure uses one theorem mode: limit-first, moving-box,
  oscillatory, or averaged. Do not mix modes.

## Verdict

The finite-box contour identity is theorem-grade under elementary meromorphic
calculus. Original-line truncation is also theorem-grade once the start line is
in the absolute-convergence/Mellin-inversion half-plane and `W_hat` is
integrable there.

The remaining H1 contour-tail blocker is the same hard object in another form:
a fixed-curve reciprocal bound for `1/L(E,s)` in the crossed strip, away from
but close to zeros. Standard zero counting gives legal heights and even pure
ordinate separation. It does not give polynomial or subpolynomial bounds for
`1/L(E,s)` on those heights.

Thus the exact H1 contour-tail package reduces to the explicit assumptions
`H-height` and `H-left` below. Those assumptions are not closed by the checked
sources.

## Setup

Let

```text
F_u(z) = e^(uz) W_hat(z)/L(E,1+z),
S(eta,sigma) = {z: -eta <= Re z <= sigma}.
```

Assume `0<eta<1`, `sigma>0`, and `W_hat` is meromorphic on the strip, with no
strip pole except the kernel pole at `z=0` unless extra kernel residues are
explicitly retained.

For tail estimates write the kernel decay hypothesis as

```text
|W_hat(x+it)| <= C_W (1+|t|)^(-q)
uniformly for -eta <= x <= sigma, away from z=0.
```

For the repository smoothstep class, use `q=2` unless a stronger kernel audit is
attached.

## Promotable Finite-Box Identity

For any `T` such that the rectangle boundary contains no pole of `F_u`,
Cauchy's theorem gives

```text
I_sigma(T,u)
 = sum_{z0 in P_T} Res_{z=z0} F_u(z)
   + V_eta(T,u) + H_+(T,u) - H_-(T,u),
```

where `P_T` contains all poles in `-eta<Re z<sigma`, `|Im z|<T`, including
`z=0`, crossed zeros `z=rho-1`, and any extra kernel poles. This is a proof,
not a source-dependent claim.

If a pole lies on the shifted vertical line or on a horizontal edge, either
move the line/height or add explicit indentation contours. The indentation
terms are not automatically small; they are residues plus local reciprocal
Laurent bounds.

## Mellin/Perron Start Line

The smooth Perron identity can be proved locally as follows. If

```text
W(y) = (1/(2 pi i)) int_(Re z=sigma) y^(-z) W_hat(z) dz
```

with absolute convergence on `Re z=sigma`, and

```text
sum_n |mu_E(n)| n^(-1-sigma) < infinity,
```

then Fubini gives

```text
sum_n mu_E(n)/n W(n/e^u)
 = (1/(2 pi i)) int_(Re z=sigma)
     e^(uz) W_hat(z)/L(E,1+z) dz.
```

In the unnormalized EC local convention

```text
good p: mu_E(p)=-a_p,  mu_E(p^2)=p,
```

the safe absolute-convergence start is `sigma>1/2` using the usual Hasse-size
input. If the theorem starts at `0<sigma<=1/2`, the Perron identity itself is a
new analytic input, not a consequence of absolute convergence.

## Original-Line Truncation

Assume

```text
B_sigma = sup_t |1/L(E,1+sigma+it)| < infinity
```

on the start line. This is standard if the line is in the absolute convergence
half-plane and the Euler product is nonzero there.

Then for `q>1`,

```text
|I_sigma(infty,u)-I_sigma(T,u)|
 <= C e^(sigma u) int_T^infty (1+t)^(-q) dt
 <= C e^(sigma u) T^(1-q).
```

Promotion:

```text
fixed u:       tail -> 0 if q>1.
moving T(u):   e^(sigma u) T(u)^(1-q) = o(u^r).
```

For smoothstep `q=2`, moving-box pointwise use requires

```text
T(u) >> e^(sigma u) u^(-r) times a diverging factor.
```

This tail is not the hard part.

## Horizontal Edges

Define the height reciprocal bound

```text
M(T) = sup_{-eta<=x<=sigma, eps=+-1}
       |1/L(E,1+x+eps iT)|.
```

The horizontal edges obey the direct estimate

```text
|H_+(T,u)|+|H_-(T,u)|
 <= C (sigma+eta) e^(sigma u) (1+T)^(-q) M(T).
```

Therefore the following is sufficient:

```text
H-height(A):  there exist legal T_n -> infinity with M(T_n) <= C T_n^A.
```

Consequences:

```text
fixed u:       horizontal edges vanish if A<q.
moving T(u):   e^(sigma u) T(u)^(A-q) = o(u^r).
```

For smoothstep `q=2`, this needs `A<2` even for fixed-`u` limiting along
`T_n`. If only `M(T_n)=T_n^(o(1))`, then fixed-`u` horizontal decay is fine for
any `q>0`.

No checked EC/GL2 source supplies `H-height(A)`.

## Shifted Vertical Line

The shifted edge satisfies

```text
|V_eta(T,u)|
 <= e^(-eta u)/(2 pi)
    int_{-T}^T |W_hat(-eta+it)/L(E,1-eta+it)| dt.
```

The clean limit-first condition is

```text
H-left: J_eta := int_R |W_hat(-eta+it)/L(E,1-eta+it)| dt < infinity.
```

Then

```text
V_eta(infty,u) = O(e^(-eta u)) = o(u^r) for r>=0,
```

with `o(1)` in rank zero.

A sufficient polynomial version is

```text
|1/L(E,1-eta+it)| <= C (1+|t|)^B
and q > B+1.
```

For smoothstep `q=2`, this requires `B<1`. This is a strong reciprocal-growth
input, not a zero-counting corollary.

If only the truncated integral is known,

```text
J_eta(T) <= C T^B,
```

then moving-box use requires

```text
e^(-eta u) T(u)^B = o(u^r).
```

This can conflict with the large `T(u)` demanded by original/horizontal tails.
The limit-first mode avoids that conflict only if `H-left` and the residue
limit are already proved.

## Pole Avoidance Near Zeros

What standard zero counting gives:

1. Legal heights exist because zeros are isolated and finite in bounded
   rectangles.
2. With EC zero counting `N_E(T+1)-N_E(T) <<_E log T`, one can choose
   `T_* in [T,T+1]` with

```text
dist(T_*, {Im rho: T-1 <= Im rho <= T+2}) >= c_E / log T.
```

Proof: remove intervals of radius `c_E/log T` around the `O_E(log T)` zero
ordinates in the unit window and choose `c_E` small.

What this does not give:

```text
sup_x |1/L(E,1+x+iT_*)| <= T_*^A.
```

Near a zero `rho` of multiplicity `m`,

```text
1/L(E,s) = b_{rho,-m}(s-rho)^(-m) + ... .
```

Distance `>= c/log T` only changes the local blow-up into
`|b_{rho,-m}| (log T)^m`. Without bounds for multiplicities and Laurent
coefficients, especially `1/L'(rho)` at simple zeros, no usable horizontal
bound follows.

Thus:

```text
promote:     existence of legal/separated heights.
do not promote: quantitative reciprocal height avoidance.
```

## Crossed-Strip Reciprocal Growth

The needed crossed-strip input is exactly:

```text
H-strip(q):
there are legal heights T_n such that
  sup_{-eta<=x<=sigma} |1/L(E,1+x+iT_n)| = o(T_n^q),
and the shifted-line integral H-left holds.
```

For the fixed smoothstep `q=2`, `H-strip(2)` plus `H-left` is enough for
fixed-`u` contour passage. For a moving-box asymptotic, the stronger rate
conditions above must be imposed in the same `T(u)` scheme as the residue
aggregate.

This is a new assumption for fixed EC H1 unless a GL2 reciprocal-height theorem
is supplied. RH removes zeros with `Re(rho) != 1` but does not bound
`1/L'(rho)`, multiplicity, or small values of `L` between zeros.

## Promotion Table

| Item | Decision |
|---|---|
| Finite rectangle residue identity | promote under meromorphicity and legal boundary |
| Smooth Perron/Mellin identity | promote only on an absolute-convergence start line; otherwise assume/prove |
| Original-line truncation | promote if `q>1` and `1/L` bounded on start line |
| Legal height existence | promote |
| Height separated from zero ordinates by `c/log T` | promote from zero counting |
| Horizontal edge decay | reduce to `H-height(A)` with `A<q` |
| Shifted vertical decay | reduce to `H-left` or polynomial `B<q-1` |
| Pole avoidance with reciprocal bounds | new assumption; equivalent to local reciprocal control |
| Crossed zeros with `Re(rho)>1` | retain or rule out; never discard |
| Growth of `1/L(E,s)` in crossed strip | not source-closed for fixed EC/GL2 |

## Source Packet

Run directory:

```bash
/tmp/h1-contour-tail-20260511
```

Tooling:

```bash
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -v
```

Xpdf reported `pdftotext version 4.06`.

Fetched and extracted:

```bash
curl -L --fail -o fi_opera_ch1.pdf https://assets.press.princeton.edu/chapters/s8585.pdf
curl -L --fail -o sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236
curl -L --fail -o inoue_jtnb_1162.pdf https://www.numdam.org/item/10.5802/jtnb.1162.pdf
for f in fi_opera_ch1 sheth_ec_arxiv_2312.05236 inoue_jtnb_1162; do
  ./xpdf-tools-mac-4.06/binARM/pdftotext -layout "$f.pdf" "$f.txt"
done
```

SHA256:

```text
080fbff5d5f122678cddd78a1b0561a79952c5fe72b49cf2fbc6b014edc0e8dc  fi_opera_ch1.pdf
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_arxiv_2312.05236.pdf
af20e8afc632f1992a0bd1012d2b34ee353fd6174f318ae4442658ecfb3ac45f  inoue_jtnb_1162.pdf
```

Cited anchors:

- Friedlander-Iwaniec, `Opera de Cribro`, Ch. 1 sample PDF, PDF p. 11,
  Lemma 1.1, eq. (1.4.7). Short quote: "The first tool". PDF p. 12,
  eq. (1.4.10). Short quote: "Perron's formula itself". Use: standard sharp
  Perron background only; the fixed smooth Mellin identity above is still
  proved/assumed locally for `W`.
- Sheth, `Euler product asymptotics for L-functions of elliptic curves`,
  arXiv:2312.05236, PDF p. 13, Theorem 3.1. Short quote: "number of zeros".
  Same page, Corollary 3.2. Short quote: "converges". Use: EC zero counting
  and pure ordinate separation. Limit: no reciprocal derivative or
  crossed-strip `1/L` bound.
- Inoue, `Some explicit formulas for partial sums of Mobius functions`, PDF
  p. 274, Theorem 1, eq. (1.4). Short quote: "m(rho) indicates the
  multiplicity". PDF p. 275. Short quote: "We do not know even the
  boundedness". PDF p. 288, Corollary 1, eq. (4.5). Short quote:
  "Corollary 1. We have". Use: GL1 model showing that reciprocal height control
  is a separate theorem. Limit: Dirichlet source, not fixed EC/GL2 closure.

## Bottom Line

The contour-tail package can be promoted only as:

```text
finite-box identity
+ original-line truncation
+ legal height existence
+ explicit assumptions H-height and H-left.
```

It cannot be promoted to the desired fixed-curve H1 asymptotic from standard
EC zero counting, RH, or smooth Mellin decay alone. The new assumption is
quantitative reciprocal control of `1/L(E,s)` in the crossed strip, compatible
with the same height sequence and residue aggregation mode.

## Changed Paths

- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md`
