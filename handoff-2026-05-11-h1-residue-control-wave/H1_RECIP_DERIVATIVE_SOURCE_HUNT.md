---
schema_version: 1
title: "H1 reciprocal derivative source hunt"
date: 2026-05-11
agent: "H1 residue-control Agent 1"
type: source-hunt
tier: working
status: LITERATURE_BLOCKED
confidence: 0.80
dependencies:
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md
  - handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
tags: [ec-ndc, h1, reciprocal-derivative, laurent-control, source-hunt]
---

# H1 Reciprocal Derivative Source Hunt

Status: `LITERATURE_BLOCKED`.

Confidence: `0.80`. The negative verdict is strong for the fetched fixed-curve
EC/GL2-adjacent sources, but not an exhaustion claim over all automorphic
L-function literature.

## Do Not Promote Unless

- A fixed-curve theorem controls `1/L'(rho)` at every offcentral simple zero,
  or controls the full H1 aggregate directly.
- Multiple offcentral zeros are ruled out, have effective residue degree `< r`,
  are kernel-cancelled, or have sourced Laurent coefficient bounds.
- "Many simple zeros" is not upgraded to "all offcentral zeros simple".
- A negative-moment lower bound is not used as an upper bound.
- Li-Zaharescu-style mollified sums are not used for H1 unless converted to the
  fixed weight `W_hat(i gamma) exp(i gamma u)` with uniform tail control.
- Rank zero remains separated.
- The exact contour shift and H2 theorem mode match the same fixed `W`.

## Target Input

For `u=log K`, analytic rank `r=ord_(s=1)L(E,s)>=1`, and

```text
c_E,W(e^u) = (1/(2 pi i)) int e^(uz) W_hat(z)/L(E,1+z) dz,
```

the positive-rank target is

```text
c_E,W(e^u) = Q_r(u) + o(u^r).
```

Using `H1_POSITIVE_RANK_CLOSURE.md`, it is enough to prove the contour shift
and then, after combining equal frequencies,

```text
no surviving offcentral term u^ell exp(i gamma u) has ell >= r,
sum_gamma |c_(gamma,ell)| < infinity for 0 <= ell < r,
contour tail = o(u^r).
```

For all offcentral zeros simple, this reduces to the clean sufficient condition

```text
sum_(gamma != 0) |W_hat(i gamma)/L'(1+i gamma)| < infinity.
```

No fetched source proves this for a fixed elliptic curve or fixed GL2
L-function.

## Source Verdict

No source found closes any of the needed fixed-curve inputs:

- all offcentral zeros simple;
- bounded offcentral multiplicity tied to the rank threshold `m<=r`;
- upper bounds or moments for `1/L'(rho)` over all zeros;
- higher Laurent coefficient bounds for `1/L(s)` at multiple zeros;
- direct pointwise control of
  `sum W_hat(i gamma) exp(i gamma u)/L'(1+i gamma)`.

The closest fetched source is Li-Zaharescu: it has automorphic negative
derivative moments and mollified reciprocal-derivative sums, but in the wrong
direction for H1 closure. It gives lower bounds and selected dyadic
mollified asymptotics, not an absolute or pointwise upper bound for the fixed
H1 residue aggregate.

## Route Ledger

| route | source state | H1 decision |
|---|---|---|
| Absolute reciprocal derivative summability | not sourced | Would imply positive-rank H1 for simple zeros. |
| Li-Zaharescu mollified reciprocal sums | fetched, adjacent | Possible proof template only; not fixed `W_hat(i gamma)e^(i gamma u)` control. |
| All offcentral simple zeros | not sourced | Booker/de Faveri give infinitely/power-many simple zeros, not all. |
| Bounded multiplicity | not sourced | Needed at least as `m<=r` after kernel cancellation; no fetched theorem. |
| Laurent coefficient bounds | not sourced | Needed for multiple zeros; no fetched theorem. |
| Kernel zero filtering | local reduction only | Finite filtering is diagnostic; infinite/tail control still needs residue bounds. |

## Verified Source Hooks

Run directory:

```bash
/tmp/h1-residue-control-agent1
```

Text tool:

```bash
/tmp/h1-source-audit-20260511/xpdf-tools-mac-4.06/binARM/pdftotext
```

### Booker, Simple Zeros Of Degree 2 L-Functions

Fetch/extract:

```bash
curl -L --fail -o booker_simple_degree2.pdf \
  https://people.maths.bris.ac.uk/~maarb/papers/simple.pdf
/tmp/h1-source-audit-20260511/xpdf-tools-mac-4.06/binARM/pdftotext \
  -layout -enc UTF-8 booker_simple_degree2.pdf \
  booker_simple_degree2.utf8.txt
```

SHA256:

```text
487b03bd35b8a5fe1fe602bcc66406e6cf47ab288117f36bbed8f4bce92a5a3c
```

PDF p. 1, Theorem 1. Quote: "has inﬁnitely many simple zeros."

PDF p. 1, introduction. Quote: "conjectures have not yet been shown".

Use: source for existence of infinitely many simple zeros of holomorphic
newform L-functions. Limit: not all zeros simple; no `1/L'(rho)` control.

### de Faveri, Simple Zeros Of GL(2) L-Functions

Fetch/extract:

```bash
curl -L --fail -o defaveri_simple_gl2.pdf \
  https://ems.press/content/serial-article-files/48859
/tmp/h1-source-audit-20260511/xpdf-tools-mac-4.06/binARM/pdftotext \
  -layout -enc UTF-8 defaveri_simple_gl2.pdf \
  defaveri_simple_gl2.utf8.txt
```

SHA256:

```text
92f7bca8f11a5e521b7e9ed38ce8cc37dd36f054b8d8e55a5a768847158caee3
```

PDF p. 1, abstract. Quote: "the first power bound in this problem".

PDF p. 2, Theorem 1.1. Quote: "Power bound for arbitrary level".

Use: source for power-many simple zeros for primitive holomorphic GL2 forms.
Limit: still not all offcentral zeros simple; no bounded multiplicity; no
reciprocal derivative upper/moment bound.

### Li-Zaharescu, Value Distribution Of L'(rho)

Extraction note: Xpdf drops the prime glyph in this PDF's text layer, rendering
`L'(rho)` as `L (rho)`. The source title and formulas are still the derivative
paper; I do not use typography beyond the extracted equations.

Fetch/extract:

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

PDF p. 2, Theorem 1.1. Quote: "lower bound for the negative moment".

PDF p. 4, equations (9)-(11). Quote: "molliﬁed moments of L (ρ)".

PDF p. 7, Theorem 4.1. Quote: "almost all zeros of L(s) are simple".

Use: closest fetched proof route for reciprocal-derivative sums in an
automorphic/Selberg-class setting. Limits:

- Theorem 1.1 is a lower bound for a negative moment, not an upper bound.
- Theorem 4.1 handles `S1` with Dirichlet polynomial weights and assumptions;
  it does not control the fixed H1 weight `W_hat(i gamma) exp(i gamma u)`.
- "Almost all simple" does not remove the exceptional multiple zeros that H1
  cannot ignore.

## Proof Route To Try If Continuing

The only plausible non-literature route from fetched material is a new theorem
modelled on Li-Zaharescu's contour for `L(s)^(-1)X(s)Y(1-s)`, replacing the
Dirichlet-polynomial weights by a dyadic smooth vertical partition of

```text
W_hat(i gamma) exp(i gamma u).
```

To promote it, one would still need:

```text
uniformity in u,
absolute or square-summable dyadic upper bounds,
handling of exceptional multiple zeros,
summation over dyadic T against the actual Mellin decay of W_hat,
and the same H1 contour tail.
```

This is a research program, not a sourced theorem.

## Bottom Line

For positive analytic rank, H1 remains source-blocked exactly at reciprocal
derivative/Laurent control. Current verified GL2 simple-zero literature supplies
many simple zeros, while the direct reciprocal-derivative literature supplies
negative-moment lower bounds and mollified templates. Neither implies

```text
c_E,W(e^u) = Q_r(u) + o(u^r),     r>=1.
```
