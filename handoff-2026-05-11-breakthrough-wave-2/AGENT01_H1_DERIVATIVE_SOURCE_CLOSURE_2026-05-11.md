---
schema_version: 1
title: "Agent 01 H1 derivative source closure"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 01 -- H1 Anti-Small-Derivative Source Closure"
type: source-closure
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.86
tags: [breakthrough-wave-2, h1, ec-ndc, reciprocal-derivative, source-closure]
---

# Agent 01 H1 Derivative Source Closure

status: `RIGOROUS_REDUCTION`

## Verdict

No fixed-curve theorem is promoted.

For analytic rank one, the live simple-zero target remains

```text
R_E,1(T) =
  sum_(T<|gamma|<=2T, simple) |L'(E,1+i gamma)|^(-1)
  = o(T^2).
```

The checked external sources do not prove this, nor the pointwise lower bound

```text
|L'(E,1+i gamma)| >= h(T) log T / T,    h(T)->infinity,
```

nor a layer-cake small-derivative tail. The route is not killed as false; it is
source-blocked at an exact theorem input.

Best reduction:

```text
Prove a fixed-curve GL2/EC negative first moment theorem over all simple zeros,
or over a separated subfamily plus a reciprocal-budget bound for the complement.
```

## Context Read

- `start.md`
- `token-economy.yaml`
- `L0_rules.md`
- `L1_index.md`
- `primes-equispaced/L1_index.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT01_H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md`
- `primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md`
- `primes-equispaced/handoff-2026-05-11-all-in-wave/H1_WEIGHTED_L1_ATTACK_PACKET_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/DISPATCH_MANIFEST_2026-05-11.md`

I did not read broad archives. `AGENT04_H2_SYM2_ENDPOINT_CLOSURE` was not needed:
H2 branch damping is irrelevant to H1 reciprocal poles.

## Source Packet

Run directory:

```bash
/tmp/agent01-h1-derivative-source-closure-20260511
```

Text extractor:

```bash
curl -L --fail -s -o xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac-4.06.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -v
```

Xpdf reported `pdftotext version 4.06`.

### Li-Zaharescu, Value Distribution Of L'(rho)

Fetch/extract:

```bash
curl -L --fail -s -o li_zaharescu_Lprime_rho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  li_zaharescu_Lprime_rho.pdf li_zaharescu_Lprime_rho.txt
shasum -a 256 li_zaharescu_Lprime_rho.pdf
```

SHA256:

```text
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011
```

Anchors:

- PDF p. 2, class examples. Quote: "holomorphic cusp forms".
- PDF p. 2, Theorem 1.1, equation (5). Quote: "second negative moment".
- PDF p. 2, Theorem 1.2, equation (6). Gives an extreme-small-value upper
  bound for `min |L'(rho)|`.
- PDF p. 4, equations (9)-(11). Defines mollified sums `S0,S1,S2`; `S1`
  contains `L'(rho)^(-1) X(rho) Y(1-rho)`.
- PDF p. 4, Proposition 3.1. Quote: "Each interval [T, T + 1] contains".
- PDF p. 7, Theorem 4.1. Quote: "almost all zeros".

Extraction note: the text layer drops the prime in some displayed `L'(rho)`
instances; the title and formulas identify the derivative.

Decision: `ADJACENT_ONLY`.

Use:

- Source-closes selected horizontal minimum-modulus heights for contour tails.
- Supplies lower negative-moment and small-value results, not upper tails.
- Supplies mollified reciprocal-derivative sums for Dirichlet-polynomial
  weights, not the fixed H1 weight `W_hat(i gamma) exp(i gamma u)`.

Limits:

- Theorem 1.1 is a lower bound for a negative moment, wrong direction for
  `R_E,1(T)=o(T^2)`.
- Theorem 1.2 proves existence of small derivatives; it does not give a lower
  bound at every zero.
- Proposition 3.1 gives selected ordinates for horizontal contour avoidance,
  not zero-centered circles around every `rho`.
- Theorem 4.1 assumes a mollifier length `M=T^theta`, `theta<1`, and
  almost-all simplicity; it is not a fixed-weight pointwise H1 theorem.

### de Faveri, Simple Zeros Of GL(2) L-Functions

Fetch/extract:

```bash
curl -L --fail -s -o defaveri_simple_gl2.pdf \
  https://ems.press/content/serial-article-files/48859
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  defaveri_simple_gl2.pdf defaveri_simple_gl2.txt
shasum -a 256 defaveri_simple_gl2.pdf
```

SHA256:

```text
92f7bca8f11a5e521b7e9ed38ce8cc37dd36f054b8d8e55a5a768847158caee3
```

Anchors:

- PDF p. 1, abstract. Quote: "first power bound".
- PDF p. 2, Theorem 1.1. Quote: "primitive holomorphic modular form".

Decision: `ADJACENT_ONLY`.

Use: source for power-many simple zeros of GL2 holomorphic modular forms.

Limit: a lower bound for how many zeros are simple does not prove all
offcentral zeros are simple, zero repulsion for every zero, or any upper bound
for `|L'(rho)|^(-1)`.

### Bui-Florea-Milinovich, Negative Discrete Moments Of zeta'(rho)

Fetch/extract:

```bash
curl -L --fail -s -o bfmt_negative_zeta_derivative.pdf \
  https://arxiv.org/pdf/2310.03949
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  bfmt_negative_zeta_derivative.pdf bfmt_negative_zeta_derivative.txt
shasum -a 256 bfmt_negative_zeta_derivative.pdf
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d
```

Anchors:

- PDF p. 1, abstract. Quote: "conditional upper bounds".
- PDF p. 2, definition of `J_-k(T)`, equation (1.1).
- PDF pp. 2-3, Theorem 1.1, equation (1.2).
- PDF p. 3, full-family warning. Quote: "simplicity of zeros is not enough".

Decision: `MODEL_ONLY`.

Use: this is the closest proven shape to the desired input. For zeta only, RH
plus a separated subfamily gives negative-moment upper bounds; with `k=1/2`,
equation (1.2) gives a `sum |zeta'(rho)|^(-1)` bound of size `T^(1+delta)`
on that subfamily.

Limit: it is zeta-only, conditional, and not over all zeros without extra
spacing/exception handling. It cannot be imported to a fixed elliptic curve.

## Route Map

| route | status | reason |
|---|---:|---|
| Pointwise `h(T) log T/T` lower bound | `RIGOROUS_REDUCTION` | Would prove `R_E,1=o(T^2)` from local zero count, but no checked source proves it. |
| Layer-cake tail `int_1^infty N_E(T;V)dV=o(T^2)` | `RIGOROUS_REDUCTION` | Equivalent to the target under local zero count; no checked source proves the tail. |
| LZ negative moment | `NO_GO` | Lower bound / small-value direction; not an upper reciprocal-tail theorem. |
| LZ selected heights | `NO_GO` | Closes horizontal contour height avoidance only; not derivative lower bounds at zeros. |
| LZ mollified `S1` | `NO_GO` | Dirichlet-polynomial weights and length restrictions do not transfer to fixed `W_hat(i gamma)e^(i gamma u)` without a new upper reciprocal theorem. |
| de Faveri simple-zero count | `NO_GO` | Many simple zeros do not control reciprocal derivatives and do not handle every zero. |
| Zero spacing alone | `NO_GO` | Spacing does not lower-bound the nonzero local factor `g_rho(rho)` in `L(s)=(s-rho)g_rho(s)`. |
| Minimum-modulus circle at each zero | `RIGOROUS_REDUCTION` | Sufficient if it is zero-centered and quantitative; no checked source supplies it. |
| BFMT-style separated negative moment | `RIGOROUS_REDUCTION` | Exact proof model for zeta; needs a fixed-curve GL2/EC analogue plus bad-set reciprocal budget. |

## Local Minimum-Modulus Reduction

For a simple zero `rho=1+i gamma`, write

```text
L(E,s)=(s-rho) g_rho(s),    g_rho(rho)=L'(E,rho).
```

If a circle `|s-rho|=r_T` is zero-free and

```text
min_(|s-rho|=r_T) |L(E,s)| >= m_T,
```

then on the circle `|g_rho(s)|>=m_T/r_T`. Applying the maximum principle to
`1/g_rho` gives

```text
|L'(E,rho)| >= m_T/r_T.
```

Thus the pointwise H1 route closes if every simple zero in the shell has such
a circle with

```text
m_T/r_T >= h(T) log T / T,    h(T)->infinity.
```

This is the exact minimum-modulus theorem needed. LZ Proposition 3.1 does not
provide it because the selected ordinate is not tied to each zero, and the
bound is horizontal-line avoidance rather than a zero-centered boundary lower
bound.

## Sharper External Theorem Input

The next source target should be one theorem, not another broad hunt:

```text
EC/GL2-BFMT-k=1/2-with-budget.

For fixed E and dyadic T, let F_T be simple zeros with nearest-neighbor
spacing at least c/log T, or another explicit separated condition. Prove

  sum_(gamma in F_T) |L'(E,1+i gamma)|^(-1) << T^(1+epsilon)

and prove the complement reciprocal budget

  sum_(gamma notin F_T, simple) |L'(E,1+i gamma)|^(-1) = o(T^2).
```

This would source-close `R_E,1(T)=o(T^2)`. Without the complement budget, it
only controls a subfamily and does not close H1.

Equivalent but less source-shaped target:

```text
For fixed E,
int_1^infty #{T<|gamma|<=2T simple: |L'(E,1+i gamma)|^(-1)>V} dV
  = o(T^2).
```

## Verification Notes

- Analytic rank only.
- No H2 branch damping used as H1 reciprocal-pole damping.
- Numerical EC work not used.
- No Koyama correspondence or email drafts touched.
- External theorem claims above use `curl + pdftotext`, short quotes, and
  page/equation anchors.
- No theorem promoted.

## Changed Files

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT01_H1_DERIVATIVE_SOURCE_CLOSURE_2026-05-11.md`
