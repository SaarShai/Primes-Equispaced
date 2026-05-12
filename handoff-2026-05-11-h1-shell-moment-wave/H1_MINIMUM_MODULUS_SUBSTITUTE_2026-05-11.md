---
schema_version: 1
title: "H1 minimum-modulus substitute"
date: 2026-05-11
type: theorem-reduction
tier: working
status: PROOF_CANDIDATE
verdict: "Li-Zaharescu minimum-modulus heights close H-height; H1 residue control still open"
confidence: 0.78
dependencies:
  - handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md
  - handoff-2026-05-11-h1-shell-moment-wave/TC_HEIGHT_EXPONENT_AUDIT.md
  - handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
tags: [ec-ndc, h1, minimum-modulus, contour-tail, gl2]
---

# H1 Minimum-Modulus Substitute

Status: `PROOF_CANDIDATE` for the contour height input only.

Decision: the generic Cartan/Jensen route still does not prove `A_TC<2`, but
there is a sharper known-theorem route. Li-Zaharescu Proposition 3.1 gives
selected heights in every unit interval with

```text
|L(sigma+it)| >= exp(-A log t / log log t)
```

uniformly in the fixed strip of the normalized `L`-function. After shifting the
elliptic-curve normalization and reflecting the left half of the H1 rectangle
by the functional equation, this gives

```text
sup_{1-eta<=x<=1+sigma} |1/L(E,x+iT_n)|
  <= exp(A_E log T_n / log log T_n)
  <= T_n^epsilon
```

for every fixed `epsilon>0`, all large `n`, and any fixed
`eta>1/2`, `0<sigma<3/2` covered by the normalized strip.

Thus the contour assumption can be replaced by:

```text
H-height-LZ(E,eta,sigma):
  there are legal heights T_n -> infinity, one in each large unit interval,
  with M(T_n) <= exp(A_E log T_n / log log T_n).
```

For the current smoothstep-scale kernel `q=2`, this is stronger than the needed
fixed exponent threshold `A_TC<2`.

## What This Closes

For fixed `u`, the horizontal edge bound becomes

```text
H_horiz(T_n,u)
  << e^(sigma_z u) T_n^(-q+epsilon).
```

With `q=2`, choose any `epsilon<2`. Then

```text
H_horiz(T_n,u) -> 0.
```

For moving-box use, choose legal heights near a growth scale
`Y(u)=exp(Bu)`. Since the theorem gives an admissible height in each unit
interval, take `T(u) in [Y(u),Y(u)+1]`. Then

```text
e^(sigma_z u) T(u)^(-q+epsilon)
 = exp((sigma_z - B(q-epsilon))u),
```

so the horizontal tail is `o(u^r)` after choosing

```text
B > sigma_z/(q-epsilon).
```

This removes the `A_TC<2` height-exponent blocker for the H1 contour tails.

## Normalization Check

Li-Zaharescu use the standard automorphic normalization with critical line
`Re s=1/2` and absolute convergence to the right of `1`. The Hasse-Weil
elliptic-curve convention in the EC packets has center `1` and absolute
convergence to the right of `3/2`.

Set

```text
F_E(w) = L(E,w+1/2).
```

For an elliptic curve over `Q`, modularity identifies this normalized object
with the holomorphic newform `L`-function attached to `E`; this is the class
covered by the LZ source packet. The real EC coefficients give the required
conjugation symmetry when the reflected point has height `-T`.

Then the LZ strip

```text
1/2 <= Re w <= 2
```

corresponds to

```text
1 <= Re s_E <= 5/2.
```

The right half of the H1 horizontal segment

```text
1 <= Re s_E <= 1+sigma
```

is covered if `sigma<3/2`. The left half

```text
1-eta <= Re s_E <= 1
```

reflects under the EC functional equation to

```text
1 <= Re(2-s_E) <= 1+eta.
```

For `eta<3/2`, this is also inside the covered strip. The gamma-factor ratio
on the left half is at most polynomially decaying or bounded:

```text
|Gamma(a+iT)/Gamma(2-a-iT)| ~= T^(2a-2),   a<=1.
```

So the right-half minimum-modulus height controls the whole H1 horizontal
segment. The existing `H-left` argument remains: choose `eta>1/2` to put the
left vertical line under absolute reciprocal Euler-product control after
reflection.

Recommended fixed contour range:

```text
1/2 < eta < 1,
1/2 < sigma_z < 3/2,
q=2.
```

Here `sigma_z` is the Perron start-line real part in the `z` variable, so
`s_E=1+z`.

## What This Does Not Close

This does not control H1 reciprocal residues:

```text
sum_gamma W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma).
```

It does not prove the shell moment

```text
J_E,2(T) <= C_E T^(3-delta),
```

and it does not prove direct fixed-weight PV cancellation. It only removes the
horizontal contour-tail blocker previously phrased as `TC-height(A<2)`.

Pointwise positive-rank H1 still needs one of:

```text
H1-shell-moment(E,delta): J_E,2(T) <= C_E T^(3-delta),
```

or

```text
H1-fixed-weight-PV(E,W,r):
  Z_PV(u)=o(u^r) in the required windows.
```

Rank zero still needs an oscillatory/profile/product-average statement unless
every surviving nonzero H1 residue is killed.

## Claim-Safe Replacement

Replace the contour-tail line

```text
Assume TC-height(E,1-eta,1+sigma; A_TC) with A_TC<2.
```

by the sourced theorem input

```text
Use Li-Zaharescu minimum-modulus heights:
M(T_n) <= exp(A_E log T_n/log log T_n).
```

Then the H1 theorem statement can list only these remaining H1 hypotheses:

```text
1. eta>1/2 and fixed strip parameters inside the normalization range;
2. H1 reciprocal residue control: shell moment or fixed-weight PV;
3. multiple-zero Laurent exceptional handling;
4. H2/Sym2 closure in the same pointwise/profile/average mode.
```

## Source Packet

Run directory:

```bash
/tmp/h1-minmod-substitute-20260511
```

Fetch/extract:

```bash
curl -L --fail -s -o /tmp/h1-minmod-substitute-20260511/li_zaharescu_Lprime_rho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
shasum -a 256 /tmp/h1-minmod-substitute-20260511/li_zaharescu_Lprime_rho.pdf
curl -L --fail -s -o /tmp/h1-minmod-substitute-20260511/xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf /tmp/h1-minmod-substitute-20260511/xpdf-tools-mac-4.06.tar.gz \
  -C /tmp/h1-minmod-substitute-20260511
/tmp/h1-minmod-substitute-20260511/xpdf-tools-mac-4.06/binARM/pdftotext \
  -layout -enc UTF-8 \
  /tmp/h1-minmod-substitute-20260511/li_zaharescu_Lprime_rho.pdf \
  /tmp/h1-minmod-substitute-20260511/li_zaharescu_Lprime_rho.txt
```

SHA256:

```text
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011  li_zaharescu_Lprime_rho.pdf
```

Verified anchors:

- Li-Zaharescu, `Value Distribution Of L'(rho)`, PDF p. 1: class `S` includes
  automorphic `GL(m)` examples and holomorphic cusp-form `L`-functions.
- PDF p. 4, Proposition 3.1: each interval `[T,T+1]` has a height with the
  displayed lower bound for `1/2 <= sigma <= 2`.
- PDF pp. 22-23, proof of Proposition 3.1: the selected height is obtained
  after averaging local zero-factor losses in the near-critical strip.

## Bottom Line

The minimum-modulus blocker should be downgraded from open to source-routed:

```text
H-height(A<2): closed by LZ selected heights, after EC normalization checks.
```

Do not upgrade the full EC theorem. The H1 shell/PV reciprocal-residue blocker
is still the theorem killer.
