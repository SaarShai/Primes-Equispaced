---
schema_version: 1
title: "Shell moment source audit"
date: 2026-05-11
agent: "Agent 1"
type: source-audit
tier: working
status: AUDIT_ONLY
verdict: close-but-insufficient
confidence: 0.88
dependencies:
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md
tags: [ec-ndc, h1, shell-moment, source-audit, reciprocal-derivative]
---

# Shell Moment Source Audit

## Do Not Promote Unless

- A fixed-curve EC/GL2 theorem proves
  `J_E,2(T)=sum_{T<|gamma|<=2T}|L'(E,1+i gamma)|^(-2)
  <= C_E T^(3-delta)` for all relevant central-line zeros, with simple-zero
  hypotheses stated or multiple-zero Laurent terms retained.
- A direct fixed-weight theorem proves dyadically summable bounds for
  `sum_{T<|gamma|<=2T} W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)`
  uniformly in `u`, or an equivalent contour-principal-value statement.
- Li-Zaharescu is used only as a lower-bound/mollifier template unless a new
  theorem removes the fixed-weight and upper-bound gaps.
- Zeta negative-moment results are cited only as zeta analogues, never as GL2
  or elliptic-curve proof.
- Simple-zero lower bounds are not upgraded to all-simple zeros or derivative
  lower bounds.
- EC zero counting is not used as reciprocal-derivative control.

Status: `AUDIT_ONLY`.

Verdict: `close-but-insufficient`.

Confidence: `0.88`.

Dependencies:

- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md`

## Target

For a fixed elliptic curve, with central line normalized as `s=1+i gamma`,
audit whether primary sources prove or imply

```text
J_E,2(T) =
  sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-2)
  <= C_E T^(3-delta)
```

or directly prove fixed-weight H1 shell control

```text
sum_{T<|gamma|<=2T}
  W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)
```

with dyadically summable bounds, uniformly in `u`.

## Executive Decision

No checked primary source gives the fixed-curve EC/GL2 shell upper bound, and
no checked primary source gives a direct fixed-weight H1 upper bound.

The closest source is Li-Zaharescu: it works for automorphic/Selberg-class
`L'(rho)` and includes the exact reciprocal derivative `1/L'(rho)` in
mollified sums. But its theorem direction is lower bound/extreme-small-value,
and its usable sums carry Dirichlet-polynomial weights `X(rho)Y(1-rho)` of
length `M=T^theta`, not the fixed H1 weight
`W_hat(i gamma)e^(i gamma u)`.

Thus the audit is not source-closed. It is close-but-insufficient because
there are adjacent GL2/automorphic and zeta theorems, but every one misses at
least one load-bearing requirement: upper bound, full zero set, fixed curve,
fixed H1 weight, or multiple-zero/Laurent control.

## Source Protocol

Run directory:

```bash
/tmp/h1-shell-moment-source-audit-20260511
```

Tool:

```bash
/tmp/h1-source-audit-20260511/xpdf-tools-mac-4.06/binARM/pdftotext
```

Protocol used for each source:

```bash
curl -L --fail -s -o SOURCE.pdf URL
shasum -a 256 SOURCE.pdf
pdftotext -layout -enc UTF-8 SOURCE.pdf SOURCE.txt
pdftotext -layout -enc UTF-8 -f PAGE -l PAGE SOURCE.pdf -
rg -n "theorem|moment|reciprocal|simple|zeros|..." SOURCE.txt
```

## Primary Sources

### Li-Zaharescu, Value Distribution Of L'(rho)

URL:
`https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf`

SHA256:

```text
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011
```

Protocol:

```bash
curl -L --fail -s -o li_zaharescu_value_distribution_Lprime_rho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
pdftotext -layout -enc UTF-8 li_zaharescu_value_distribution_Lprime_rho.pdf \
  li_zaharescu_value_distribution_Lprime_rho.txt
```

Verified anchors:

- PDF p. 2, Theorem 1.1. Quote: "lower bound for the negative moment".
- PDF p. 4, equations (9)-(11). Quote: "`S1 = ... L (rho)^-1 X(rho)Y(1-rho)`".
- PDF p. 7, Theorem 4.1. Quote: "`M = T^theta, theta < 1`".
- PDF p. 14, proof of Theorem 1.1. Quote: "`theta < 2/5 is a valid choice`".

Use:

- Closest automorphic/Selberg-class source for reciprocal derivative sums.
- Shows the right object `1/L'(rho)` appears in mollified contour machinery.

Limit:

- Theorem 1.1 is a lower bound for `sum |L'(rho)|^-2`, not an upper bound.
- Theorem 4.1 evaluates a weighted `S1`; it does not control the fixed H1
  weight `W_hat(i gamma)e^(i gamma u)`.
- It assumes RH/Selberg normality and almost-all simplicity; H1 still needs
  all relevant zeros handled.

Decision: `close-but-insufficient`.

Text-layer note: `pdftotext` drops the prime glyph in parts of this PDF and
renders `L'(rho)` as `L (rho)`. The title and formulas identify the derivative.

### Sheth, Euler Product Asymptotics For L-Functions Of Elliptic Curves

URL:
`https://arxiv.org/pdf/2312.05236`

SHA256:

```text
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d
```

Protocol:

```bash
curl -L --fail -s -o sheth_ec_zero_count.pdf \
  'https://arxiv.org/pdf/2312.05236'
pdftotext -layout -enc UTF-8 sheth_ec_zero_count.pdf sheth_ec_zero_count.txt
```

Verified anchors:

- PDF p. 13, Theorem 3.1. Quote: "`number of zeros`".
- PDF p. 13, Corollary 3.2. Quote: "`converges`".
- PDF p. 16, Theorem 4.2. Quote: "`finite logarithmic measure`".

Use:

- Sources EC zero counting `N_E(T)=O_E(T log T)`.
- Sources convergence of `sum 1/|rho|^2` over EC zeros.

Limit:

- Zero counting does not bound `1/L'(rho)`.
- Corollary 3.2 controls pure zero weights, not reciprocal derivatives.
- Theorem 4.2 is an exceptional-set Euler-product theorem, not H1 shell
  control.

Decision: `insufficient`.

### de Faveri, Simple Zeros Of GL(2) L-Functions

URL:
`https://ems.press/content/serial-article-files/48859`

SHA256:

```text
92f7bca8f11a5e521b7e9ed38ce8cc37dd36f054b8d8e55a5a768847158caee3
```

Protocol:

```bash
curl -L --fail -s -o defaveri_simple_gl2.pdf \
  'https://ems.press/content/serial-article-files/48859'
pdftotext -layout -enc UTF-8 defaveri_simple_gl2.pdf defaveri_simple_gl2.txt
```

Verified anchors:

- PDF p. 1, abstract. Quote: "`first power bound`".
- PDF p. 1, introduction. Quote: "`are all simple`" as conjectural context.
- PDF p. 2, Theorem 1.1. Quote: "`Power bound for arbitrary level`".

Use:

- Sources power-many simple zeros for primitive holomorphic GL2 forms.
- Relevant to the simplicity side of the H1 obstruction.

Limit:

- Does not prove all central-line/offcentral zeros are simple.
- Does not prove bounded multiplicity for the remaining zeros.
- Does not bound `1/L'(rho)`.

Decision: `insufficient`.

### Barrett-McDonald-Miller-Ryan-Turnage-Butterbaugh-Winsor, Gaps Between Zeros Of GL(2) L-Functions

URL:
`https://arxiv.org/pdf/1410.7765`

SHA256:

```text
69c5c14b17512f66626440f955056636857770c5b9210798239da5e004934088
```

Protocol:

```bash
curl -L --fail -s -o barrett_gl2_gaps_derivative_moments.pdf \
  'https://arxiv.org/pdf/1410.7765'
pdftotext -layout -enc UTF-8 \
  barrett_gl2_gaps_derivative_moments.pdf \
  barrett_gl2_gaps_derivative_moments.txt
```

Verified anchors:

- PDF p. 1, abstract. Quote: "`mixed second moments of derivatives`".
- PDF p. 4, Theorem 1.5. Quote: "`non-negative integers`".
- PDF p. 4, equation (1.12). Quote: "`T log T`".

Use:

- Sources continuous positive derivative moments for fixed primitive GL2
  L-functions.

Limit:

- Integral over `t`, not discrete sum over zeros.
- Positive moments of derivatives, not negative/reciprocal moments.
- Does not imply `sum |L'(rho)|^-2` upper bounds.

Decision: `adjacent-only`.

### Inoue, Some Explicit Formulas For Partial Sums Of Mobius Functions

URL:
`https://www.numdam.org/item/10.5802/jtnb.1162.pdf`

SHA256:

```text
af20e8afc632f1992a0bd1012d2b34ee353fd6174f318ae4442658ecfb3ac45f
```

Protocol:

```bash
curl -L --fail -s -o inoue_mobius_explicit_formulas.pdf \
  'https://www.numdam.org/item/10.5802/jtnb.1162.pdf'
pdftotext -layout -enc UTF-8 inoue_mobius_explicit_formulas.pdf \
  inoue_mobius_explicit_formulas.txt
```

Verified anchors:

- PDF p. 3 / journal p. 274, Theorem 1, equation (1.4). Quote:
  "`m(rho) indicates the multiplicity`".
- PDF p. 4 / journal p. 275. Quote: "`We do not know even the boundedness`".
- PDF p. 4 / journal p. 275. Quote: "`behavior of zeta'(rho)`".

Use:

- GL1 analogue for direct reciprocal-zero explicit formulas.
- Good warning that multiplicity and `zeta'(rho)` are real obstructions even
  before GL2/EC.

Limit:

- Dirichlet/GL1 analogue only.
- Does not prove a GL2/EC shell upper bound.
- Does not give fixed-weight H1 control.

Decision: `analogue-only`.

## Zeta Analogues Only

These are useful for scale and difficulty. They are not GL2/EC proof.

### Milinovich-Ng, A Note On A Conjecture Of Gonek

URL:
`https://arxiv.org/pdf/1106.1160`

SHA256:

```text
6a6a2a368d122c32afcb27096e250c2cc4eb607f8762362f214a3d46decc08a6
```

Protocol:

```bash
curl -L --fail -s -o milinovich_ng_gonek_conjecture.pdf \
  'https://arxiv.org/pdf/1106.1160'
pdftotext -layout -enc UTF-8 milinovich_ng_gonek_conjecture.pdf \
  milinovich_ng_gonek_conjecture.txt
```

Verified anchors:

- PDF p. 1, conjecture/equation (1.1). Quote: "`zeros of zeta(s) are simple`".
- PDF p. 2, theorem/equation (1.3). Quote: "`for any fixed epsilon > 0`".
- PDF p. 2, discussion. Quote: "`lower bound`".

Use:

- Zeta analogue for the expected `J_-1(T) ~ const*T` scale.
- Shows the classical problem concerns `sum |zeta'(rho)|^-2`.

Limit:

- Lower bound, not upper bound.
- Zeta only.
- Conditional on RH and simple zeros.

Decision: `analogue-only`.

### Bui-Florea-Milinovich, Negative Discrete Moments Of The Derivative Of The Riemann Zeta-Function

URL:
`https://arxiv.org/pdf/2310.03949`

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d
```

Protocol:

```bash
curl -L --fail -s -o bfm_negative_discrete_zeta_derivative.pdf \
  'https://arxiv.org/pdf/2310.03949'
pdftotext -layout -enc UTF-8 bfm_negative_discrete_zeta_derivative.pdf \
  bfm_negative_discrete_zeta_derivative.txt
```

Verified anchors:

- PDF p. 1, abstract. Quote: "`conditional upper bounds`".
- PDF p. 1, equation (1.1). Quote: "`J_-k(T)`".
- PDF p. 2, main results. Quote: "`No upper bounds are known`".
- PDF p. 2, Theorem 1.1. Quote: "`Assume the Riemann hypothesis`".
- PDF p. 3, section 1.2. Quote: "`simplicity of zeros is not enough`".

Use:

- Strong zeta analogue showing full negative discrete upper bounds are hard
  even for `zeta`.
- Subfamily upper bounds show what a proof shape might resemble.

Limit:

- Zeta only.
- The upper bounds are over subfamilies, not the full zero set.
- Does not imply any GL2/EC theorem.

Decision: `analogue-only`.

## Decision Table

| Source route | Gives target? | Decision |
|---|---:|---|
| Li-Zaharescu automorphic `L'(rho)` negative moments | no | close-but-insufficient: lower bound and mollified weights only |
| EC zero counting / `sum |rho|^-2` | no | insufficient: no derivative denominator |
| GL2 simple-zero lower bounds | no | insufficient: not all zeros and no derivative size |
| GL2 continuous positive derivative moments | no | adjacent-only: wrong sign/object |
| GL1/zeta direct reciprocal explicit formulas | no | analogue-only: confirms obstruction |
| Milinovich-Ng/BFM zeta negative derivative moments | no | analogue-only: zeta/subfamily/lower-bound limits |

## What Would Be Enough

For the simple-zero H1 reduction with `|W_hat(it)| <= C(1+|t|)^(-q)`, a source
would close the shell route if it proved

```text
sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-2)
  <= C_E T^theta(log T)^B,
theta < 2q - 1.
```

For the smoothstep-scale case `q=2`, this is exactly

```text
J_E,2(T) <= C_E T^(3-delta).
```

Alternatively, a direct fixed-weight theorem could bypass absolute convergence
by proving

```text
sup_u
|sum_{T<|gamma|<=2T}
  W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)|
  <= B_T,
sum_{T dyadic} B_T < infinity,
```

or a contour principal-value substitute with the same positive-rank
`o(u^r)` consequence.

No checked source proves either statement.

## Bottom Line

The known theorem landscape is close enough to justify a named open hypothesis,
not close enough to promote an EC smoothing theorem.

Allowed wording:

```text
The fixed H1 shell moment is a new fixed-curve reciprocal-derivative input.
Existing primary sources give EC zero counting, GL2 simple-zero lower bounds,
GL2 positive derivative moments, and zeta/automorphic negative-moment analogues,
but no fixed-curve EC/GL2 upper bound for J_E,2(T) and no direct fixed-weight H1
upper bound.
```

Forbidden wording:

```text
Li-Zaharescu proves fixed H1.
Zeta negative-moment bounds transfer to EC/GL2.
GL2 simple-zero theorems control reciprocal derivatives.
EC zero counting controls 1/L'(rho).
Continuous derivative moments imply discrete reciprocal moments at zeros.
```
