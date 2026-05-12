---
schema_version: 1
title: "TC-height exponent audit"
date: 2026-05-11
type: proof-audit
tier: working
status: NO_GO
verdict: "generic Cartan/Jensen does not close A_TC<2"
confidence: 0.83
dependencies:
  - handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
  - handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
tags: [ec-ndc, h1, contour-tail, tc-height, exponent-audit]
---

# TC-Height Exponent Audit

Status: `NO_GO` for deriving `A_TC<2` from the generic Cartan/Jensen route.

Confidence: `0.83`.

No new external source is cited here. This audit uses the source packets and
local reductions already recorded in:

- `RECIPROCAL_STRIP_BOUNDS.md`;
- `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md`.

Any future paper use of a Titchmarsh-Cartan or GL2 minimum-modulus theorem
still needs the project source protocol: `curl + pdftotext + short quote +
page/equation`.

## Do Not Promote Unless

- A fixed EC/GL2 minimum-modulus theorem is proved or cited in the exact strip
  needed for `1/L(E,s)`.
- The theorem gives a numerical exponent and proves `A_TC<q`; for the current
  smoothstep kernel this means `A_TC<2`.
- The same legal-height sequence also satisfies the moving-box condition
  `e^(sigma u)T(u)^(A_TC-q)=o(u^r)` if a pointwise asymptotic in `u` is being
  claimed.
- The proof does not replace bounds for `1/L(E,s)` by zero counting or
  ordinate separation alone.
- Any multiple-zero or Laurent coefficient issue remains in the separate H1
  exceptional-term package.

## Target

The contour package needs legal heights `T_n` such that

```text
M(T_n)
 = sup_{1-eta<=x<=1+sigma} |1/L(E,x+iT_n)|
 <= C T_n^(A_TC),
```

and for the current smoothstep-scale kernel:

```text
A_TC < q = 2.
```

`RECIPROCAL_STRIP_BOUNDS.md` already closes `H-left` for `eta>1/2`. This file
only audits the horizontal height exponent.

## Decision

The generic Cartan/Jensen proof shape may justify a named finite-exponent
height hypothesis if all analytic details are supplied. It does not justify
the quantitative inequality `A_TC<2`.

More sharply: the naive local-zero bookkeeping points in the wrong direction.
With only polynomial growth, a right-line nonzero anchor, and local zero count
`O_E(log T)`, the zero-factor loss around a horizontal segment is naturally of
size

```text
exp(O(log T log log T)) = T^(O(log log T)),
```

unless an additional minimum-modulus theorem gives cancellation or structure
beyond local zero counting. That is weaker than any fixed exponent, and far
weaker than the required fixed exponent below `2`.

Thus the next contour target should not be phrased as "finish the routine
Cartan proof and hope `A<2`." It should be phrased as:

```text
Find/prove a fixed EC/GL2 minimum-modulus theorem with explicit exponent
A_TC<2, or change the kernel/theorem mode.
```

## Why The Generic Proof Loses Too Much

Work in a fixed thickened rectangle around

```text
1-eta <= Re s <= 1+sigma,
Im s ~ T.
```

The available source-backed zero count gives, in a bounded-height window,

```text
N_local(T) = O_E(log T).
```

Legal height separation alone gives at best a height `T_*` in a unit interval
whose distance from all relevant zero ordinates is on the order of

```text
1/log T.
```

If a local factorization contains `N=O(log T)` nearby zero factors, the raw
zero-product lower bound along the horizontal segment has the shape

```text
prod_j |s-rho_j| >= (c/log T)^(C log T)
               = exp(-C log T log log T)
               = T^(-C log log T).
```

After inversion this is

```text
T^(C log log T),
```

before any additional loss from the zero-free factor. This is not a fixed
polynomial exponent.

Cartan covering gives the same warning in another language. If a polynomial
with `N=O(log T)` local zero factors is small on bad disks of total radius
`H`, outside those disks the generic lower bound contains a factor comparable
to

```text
(H/(eN))^N.
```

With `N=O(log T)` and fixed usable total radius `H`, this again has reciprocal
size

```text
exp(O(log T log log T)).
```

Therefore the generic Cartan/Jensen package is not enough to produce

```text
M(T_n) <= T_n^A
```

with fixed `A`, let alone `A<2`.

## What A Real TC Theorem Would Need

A promotion-grade theorem must add something beyond local zero count. Possible
forms:

```text
TC-height-strong(E,eta,sigma,A):
  There are legal heights T_n -> infinity such that
    sup_{1-eta<=x<=1+sigma}|1/L(E,x+iT_n)| <= C T_n^A.
```

For the current endpoint kernel it must prove:

```text
A < 2.
```

Potential sources of such strength would be:

1. a fixed GL2 analogue of Titchmarsh's zeta minimum-modulus height theorem
   with explicit exponent;
2. a lower bound for the completed L-function on selected horizontal
   segments, not merely distance from zeros;
3. reciprocal derivative/Laurent coefficient control strong enough to turn
   zero separation into reciprocal segment control;
4. a stronger kernel with vertical decay `q>A_TC`, if only a larger finite
   exponent is available.

None of these is present in the checked packets.

## Kernel Consequence

If a future proof only gives a finite exponent `A_TC`, the contour theorem
becomes kernel-dependent:

```text
horizontal tail << e^(sigma u) T_n^(A_TC-q).
```

Fixed-`u` limiting needs:

```text
q > A_TC.
```

Moving-box pointwise use needs:

```text
e^(sigma u) T(u)^(A_TC-q)=o(u^r).
```

For the current smoothstep class, `q=2`. Therefore:

```text
finite A_TC alone is not enough;
A_TC=2 is not enough;
A_TC<2 is the exact fixed-u threshold;
moving-box mode is stricter because T(u) must also dominate original-line
truncation and residue-tail requirements.
```

## Safe Roadmap Replacement

Replace:

```text
Prove TC-height by standard Cartan and close H-height(A<2).
```

with:

```text
Either:
  source/prove GL2 minimum modulus with explicit A_TC<2;
or:
  design a kernel with q>A_TC after a finite-exponent theorem is known;
or:
  stay in a limit-first/profile theorem mode where H-height is an explicit
  assumption.
```

## Classification

| Item | Decision |
|---|---|
| `H-left` for `eta>1/2` | closed by prior reciprocal-strip packet |
| legal heights avoiding zeros | closed by zero discreteness/counting |
| separated heights with gap `~1/log T` | closed by zero counting |
| generic Cartan/Jensen finite `A_TC` | not closed; bookkeeping is at best too weak without a stronger minimum-modulus theorem |
| generic Cartan/Jensen `A_TC<2` | `NO_GO` |
| fixed smoothstep H1 contour theorem | still conditional on explicit `H-height(A<2)` or a stronger kernel |

## Bottom Line

`H-height(A<2)` should remain a named open hypothesis. The generic
Cartan/Jensen route is useful for locating the right theorem, but it does not
close the current `q=2` H1 contour tail. Future work must either bring in a
real fixed EC/GL2 minimum-modulus theorem with explicit exponent below `2`, or
change the kernel/theorem mode.

