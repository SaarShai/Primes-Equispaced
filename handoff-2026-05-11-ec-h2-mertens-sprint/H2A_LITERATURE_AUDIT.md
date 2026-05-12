---
schema_version: 1
title: "H2-A literature audit: EC smoothed Mertens product"
date: 2026-05-11
type: literature-audit
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.76
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
  - handoff-2026-05-11-ec-smoothing-blockers/T2_STOCHASTIC_EULER_PRODUCT_MODEL.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - /tmp/h2a-ec-mertens-src/kuo_murty_cjm_2005.pdf
  - /tmp/h2a-ec-mertens-src/conrad_cjm_2005.pdf
  - /tmp/h2a-ec-mertens-src/sheth_ec_arxiv_2312.05236.pdf
tags: [ec-ndc, h2, mertens, euler-product, literature-audit]
---

# H2-A Literature Audit

status: `RIGOROUS_REDUCTION`

## Verdict

No audited source gives H2 as stated:

```text
log P_E,W(K) = -rank(E) log log K + B_E,W + o(1)
```

for the exact Agent3 smoothed local inverse factors at `s=1`, pointwise for all
`K -> infinity`.

What is citation-supported:

1. The Agent3 sharp product is the reciprocal of the original BSD product,
   up to finite bad-prime conventions.
2. The pointwise sharp product asymptotic is equivalent to a deep prime-power
   error condition, not known from RH alone in the older audited literature.
3. A 2026 arXiv version of Sheth proves an RH-conditional sharp product
   asymptotic only off a set of finite logarithmic measure.
4. If one assumes the pointwise sharp product asymptotic with analytic order
   `r = ord_{s=1} L(E,s)`, then the Agent3 smoothstep version follows by
   Stieltjes/Abel smoothing. Replacing `r` by algebraic `rank(E)` additionally
   requires BSD rank equality.

Therefore H2 is available only as a conditional reduction, not as a theorem
closed by current audited citations.

## Exact Local Factor Match

Agent3 uses, for `s=1`,

```text
good p: A_p(1) = 1 - a_p/p + 1/p
bad  p: A_p(1) = 1 - a_p/p
P_E,W(K) = product_p A_p(1)^(-W(p/K)).
```

For good primes, `A_p(1) = #E(F_p)/p`. For the bad-prime convention used in
Sheth, if `N_p = #E_ns(F_p)` and `a_p = p - N_p`, then `A_p(1) = N_p/p` also.
Conrad explicitly records the all-prime local-factor bridge: "#Ens(Fp)/p equals
the reciprocal" of the local factor at `s=1` (Conrad 2005, p. 1, eqs. (1.1)-(1.2)).

Finite omissions or alternate bad-prime factors change only `B_E,W`, not the
coefficient of `log log K`.

## Source Protocol

Protocol was executed in `/tmp/h2a-ec-mertens-src`:

```bash
curl -L --fail -o kuo_murty_cjm_2005.pdf https://mast.queensu.ca/~murty/Kuo-Murty-CJM.pdf
curl -L --fail -o conrad_cjm_2005.pdf https://kconrad.math.uconn.edu/articles/eulerprod.pdf
curl -L --fail -o sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -layout <pdf> <txt>
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -f <page> -l <page> <pdf> -
```

`pdftotext` was Xpdf 4.06 because system `pdftotext`/Poppler was not installed.

Verified source anchors:

| Source | Anchor | Verified content |
|---|---|---|
| Kuo-Murty, "On a Conjecture of Birch and Swinnerton-Dyer", Canad. J. Math. 57 (2005), 328-337 | p. 328-329, p. 333-335 | Original BSD product and equivalence. Quote: "if and only if C~(x)=o(x)" (p. 329). |
| Conrad, "Partial Euler Products on the Critical Line", Canad. J. Math. 57 (2005), 267-297 | p. 1-3, eqs. (1.1)-(1.4) | Reciprocal product `Prod(E,x)` and equivalence. Quote: "Equation (1.2) is equivalent to" (p. 3). |
| Sheth, "Euler Product Asymptotics for L-functions of Elliptic Curves", arXiv:2312.05236v4, 2026-01-15 | p. 1-4, Theorem A, Theorem B, Corollary B | RH-conditional sharp product only outside exceptions. Quote: "finite logarithmic measure" (p. 3). |

Goldfeld 1982 and the BSD 1965 original paper were not independently audited;
I do not use them as standalone sources. Their relevant claims are only used
through the audited Kuo-Murty, Conrad, and Sheth text above.

## What The Sources Imply

Let

```text
Q_E(x) = product_{p <= x} A_p(1)^(-1).
```

The original BSD product is the reciprocal:

```text
product_{p <= x} A_p(1) ~ C_E (log x)^r
```

with the appropriate local convention. Thus the sharp H2 analogue is

```text
log Q_E(x) = -r log log x + B_E + o(1).
```

Kuo-Murty and Conrad do not prove this unconditionally. They identify it with
a deeper error condition. Kuo-Murty's notation gives `C~(x)=o(x)`. Conrad's
equivalent condition is `E(x)=o(x log x)` in eq. (1.4). Both sources say RH
alone is not enough for that pointwise condition in the known technology.

Sheth proves a partial converse under RH: with

```text
r = ord_{s=1} L(E,s),
```

the sharp BSD product has the expected `C (log x)^r` asymptotic for `x` outside
a set of finite logarithmic measure. Corollary B adds algebraic `rank(E)` only
when `ord_{s=1} L(E,s) = rank(E)` is assumed.

This is not enough for H2 as used by T1/H2 because H2 is pointwise in every
large `K` and has a fixed smooth kernel over the full endpoint shell.

## Conditional Smoothing Reduction

Assume the pointwise sharp input

```text
B_sharp(x) := sum_{p <= x} -log A_p(1)
            = -r log log x + B_E + o(1).
```

Let `W` be the Agent3 smoothstep: compactly supported on `[0,1]`, `W(0)=1`,
`W(1)=0`, bounded variation, and `C^1` on the taper interval. Then

```text
log P_E,W(K) = integral W(t/K) dB_sharp(t).
```

Stieltjes integration by parts gives

```text
log P_E,W(K)
  = -r log log K + B_E,W + o(1).
```

For `alpha > 0`, this is immediate from the plateau:

```text
B_sharp(alpha K) = -r log log K + B_E + o(1),
```

and the taper contributes only `O(1/log K) + o(1)`. For `alpha = 0`, the
smoothstep has `W'(u)=O(u)` near `0`, so the lower endpoint contributes a
constant and the same `-r log log K` coefficient.

This is a rigorous reduction from pointwise sharp BSD-Mertens to smoothed H2.
It is not a proof of the sharp input.

## Decision

H2 should be packaged only conditionally:

```text
Assume the pointwise BSD-Mertens product for the exact local factors, or
equivalently a Kuo-Murty/Conrad prime-power error condition strong enough to
give B_sharp(x) = -r log log x + B_E + o(1). Then the Agent3 smoothstep product
satisfies H2 with coefficient -r. If BSD rank equality is also assumed, this is
-rank(E).
```

Do not cite Sheth as proving H2. It gives a sharp-product asymptotic off a
finite-log-measure exceptional set under RH, not the pointwise smoothed theorem
needed here.

## Dependencies

- `D1`: exact local factor convention `A_p(1)=N_p/p` for good primes and a
  finite bad-prime convention compatible up to constants.
- `D2`: pointwise sharp product asymptotic, or Kuo-Murty/Conrad condition
  strong enough to imply it.
- `D3`: analytic rank equals algebraic rank if H2 is stated with `rank(E)`.
- `D4`: smoothing transfer written explicitly for the chosen Agent3 `W_alpha`.
- `D5`: H2-D numerical slope diagnostics do not contradict `-rank(E)`.

## Do Not Promote Unless

- the coefficient is stated first as `-ord_{s=1}L(E,s)`;
- algebraic `-rank(E)` is used only with a BSD-rank assumption or theorem;
- Sheth's finite-log-measure exceptional set is not silently upgraded to
  pointwise `K -> infinity`;
- the exact Agent3 bad-prime factors are included or absorbed into `B_E,W`;
- the smoothing transfer from sharp to `W_alpha` is written as a lemma;
- H2-B/H2-E either prove the needed prime-power error condition or label it as
  an explicit hypothesis.
