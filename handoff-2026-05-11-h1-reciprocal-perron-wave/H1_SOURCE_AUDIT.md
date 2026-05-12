---
schema_version: 1
title: "H1 source audit for reciprocal Perron"
date: 2026-05-11
agent: "H1 Agent 5"
type: source-audit
tier: working
status: LITERATURE_BLOCKED
confidence: 0.86
tags: [ec-ndc, h1, reciprocal-perron, sources, zeros, derivatives]
---

# H1 Source Audit

Status: `LITERATURE_BLOCKED` for the exact H1 theorem. This is an
`AUDIT_ONLY` packet; no cross-curve universality, BSD, H2, or fixed-curve
stabilization theorem is promoted.

## Verdict

The exact H1 input needed by the EC smoothing route is not source-closed:

```text
c_E,W(K) = sum_n mu_E(n)/n W(n/K)
         = (1/2 pi i) integral_(sigma)
             K^z W_hat(z) / L(E,1+z) dz
```

with a contour shift proving that all noncentral reciprocal-pole residues and
new-contour terms are `o((log K)^r)` for positive analytic rank `r`, or `o(1)`
for rank zero.

Source-supported pieces:

- sharp Perron background exists, but not the exact smoothstep H1 contour shift;
- GL(1) explicit formulas show residue sums with zero multiplicities retained;
- EC zero counting gives pure multiplicity summability such as `sum 1/|gamma|^2`;
- exceptional-set BSD-Mertens product results exist under RH;
- GL(2) simple-zero lower bounds exist.

Missing:

- no fetched theorem gives EC/GL(2) bounds or moments for `1/L'(rho)` at zeros;
- no fetched theorem proves all offcentral zeros are simple, or bounded
  multiplicity, for a fixed EC/GL(2) L-function;
- no fetched theorem proves the H1 residue aggregate
  `sum W_hat(i gamma) K^(i gamma)/L'(1+i gamma)` is negligible pointwise.

## H1 Local Algebra

This section is local algebra, not an external citation.

If `rho = 1 + i gamma` is a noncentral zero of multiplicity `m`, write

```text
L(E,s) = a_m (s-rho)^m + a_(m+1)(s-rho)^(m+1) + ...
```

Then near `z0 = rho - 1`,

```text
1/L(E,1+z) = a_m^(-1)(z-z0)^(-m) + lower pole orders.
```

The H1 residue of

```text
K^z W_hat(z) / L(E,1+z)
```

contains a top term

```text
K^z0 (log K)^(m-1) W_hat(z0) / ((m-1)! a_m)
```

plus lower powers of `log K` and derivatives of `W_hat`. For a simple zero:

```text
Res_(z=i gamma) = K^(i gamma) W_hat(i gamma) / L'(E,1+i gamma).
```

There is no H2-style `1/log K` branch loss. Smooth `W` can damp large `|gamma|`
through `W_hat(i gamma)`, but it does not bound `1/L'(rho)` or remove fixed
low-zero oscillations.

At the central zero of order `r`,

```text
L(E,1+z) = L^(r)(E,1) z^r/r! + ...
W_hat(z) = 1/z + holomorphic
K^z = exp(z log K),
```

so the central residue is a polynomial in `log K` of degree `r`, with leading
term

```text
(log K)^r / L^(r)(E,1).
```

## Source Protocol

Run directory:

```bash
/tmp/h1-source-audit-20260511
```

System `pdftotext` was unavailable, so I fetched Xpdf and used its `pdftotext`:

```bash
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -v
```

Xpdf reported `pdftotext version 4.06`.

SHA256 for fetched source files:

```text
af20e8afc632f1992a0bd1012d2b34ee353fd6174f318ae4442658ecfb3ac45f  inoue_jtnb_1162.pdf
080fbff5d5f122678cddd78a1b0561a79952c5fe72b49cf2fbc6b014edc0e8dc  fi_opera_ch1.pdf
067e6b30245aa9a1872b36450a72e504963e902c3d4e1c611bbf9752c94e0488  kuo_murty_cjm_2005.pdf
f47a79e230d3be630e1c5a28e842d62416b403602bc4d11f9e9d3a4438dc8b6a  conrad_cjm_2005.pdf
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_arxiv_2312.05236.pdf
92f7bca8f11a5e521b7e9ed38ce8cc37dd36f054b8d8e55a5a768847158caee3  faveri_simple_gl2.pdf
69c5c14b17512f66626440f955056636857770c5b9210798239da5e004934088  barrett_gl2_gaps_derivative_moments.pdf
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmn_negative_zeta_derivative.pdf
9bacaa0c6bbaf687091d8be7b9f0df3e58727339002c9cabcb4de90e33f41fa7  sound_mobius_0705.0723.pdf
```

Blocked source:

- Booker-Cho-Kim Cambridge final PDF URL downloaded as HTML under `curl`;
  marked `LITERATURE_BLOCKED` and not cited below. De Faveri JEMS was accessible
  and enough for the simple-zero lower-bound audit.

## Audited Sources

### Friedlander-Iwaniec, Chapter 1

URL: `https://assets.press.princeton.edu/chapters/s8585.pdf`

Fetched as `fi_opera_ch1.pdf`; extracted with:

```bash
./xpdf-tools-mac-4.06/binARM/pdftotext -layout fi_opera_ch1.pdf fi_opera_ch1.txt
```

Anchors:

- PDF p. 11, Lemma 1.1, equation (1.4.7). Quote: "Perron's formula".
- PDF p. 17, Theorem 1.2, equation (1.4.17). Quote: "Mertens' Prime Number Theorem".

Use:

- source for standard sharp Perron background;
- source for ordinary prime Mertens if an H2/Mertens comparison is needed.

Limit:

- does not prove the exact compact-support smooth Mellin H1 formula;
- does not shift `1/L(E,1+z)` contours;
- does not control EC reciprocal zero residues.

Decision: `ADJACENT_ONLY`.

### Inoue 2021, Mobius Explicit Formulas

URL: `https://www.numdam.org/item/10.5802/jtnb.1162.pdf`

Fetched as `inoue_jtnb_1162.pdf`; extracted with:

```bash
./xpdf-tools-mac-4.06/binARM/pdftotext -layout inoue_jtnb_1162.pdf inoue_jtnb_1162.txt
```

Anchors:

- Journal p. 274, Theorem 1, equation (1.4). Quote: "m(rho) indicates the multiplicity".
- Journal p. 275. Quote: "We do not know even the boundedness".
- Journal p. 276, Theorem 2, equation (2.1). Quote: "following truncated formula".

Use:

- source for GL(1) Mobius explicit formulas where zero residues and
  multiplicities remain explicit;
- warning that multiplicity and derivative behavior are real obstructions.

Limit:

- Dirichlet/abelian Mobius setting, not elliptic curve or GL(2) H1;
- does not prove the shifted smooth H1 theorem;
- does not provide `1/L'(rho)` summability for EC/GL(2).

Decision: `ADJACENT_ONLY`; supports the obstruction, not closure.

### Kuo-Murty 2005

URL: `https://mast.queensu.ca/~murty/Kuo-Murty-CJM.pdf`

Fetched as `kuo_murty_cjm_2005.pdf`; extracted with:

```bash
./xpdf-tools-mac-4.06/binARM/pdftotext -layout kuo_murty_cjm_2005.pdf kuo_murty_cjm_2005.txt
```

Anchors:

- PDF p. 2 / journal p. 329, Theorems 2 and 3. Quote: "if and only if".
- PDF p. 2 / journal p. 329, Theorem 4/Proposition 5 summary. Quote: "R(x) oscillates".

Use:

- source that the hard BSD-Mertens product is equivalent to a deep
  prime-power error condition;
- source warning that product remainders can oscillate.

Limit:

- does not prove the hard product unconditionally;
- does not prove smoothed H2 pointwise;
- does not prove H1 reciprocal Perron.

Decision: `H2_ADJACENT_ONLY`.

### Conrad 2005

URL: `https://kconrad.math.uconn.edu/articles/eulerprod.pdf`

Fetched as `conrad_cjm_2005.pdf`; extracted with:

```bash
./xpdf-tools-mac-4.06/binARM/pdftotext -layout conrad_cjm_2005.pdf conrad_cjm_2005.txt
```

Anchors:

- PDF p. 1, equations (1.1)-(1.2). Quote: "equals the reciprocal".
- PDF p. 3, Theorem 1.3/equation (1.4). Quote: "is equivalent to".

Use:

- source for the local bridge between `#E_ns(F_p)/p` and the reciprocal
  local Euler factor at `s=1`;
- source that the pointwise product asymptotic is stronger than RH-level input.

Limit:

- does not prove the product asymptotic;
- does not prove endpoint-smoothed H2;
- does not address H1 `1/L(E,1+z)` residue control.

Decision: `H2_ADJACENT_ONLY`.

### Sheth 2026

URL: `https://arxiv.org/pdf/2312.05236`

Fetched as `sheth_ec_arxiv_2312.05236.pdf`; extracted with:

```bash
./xpdf-tools-mac-4.06/binARM/pdftotext -layout sheth_ec_arxiv_2312.05236.pdf sheth_ec_arxiv_2312.05236.txt
```

Anchors:

- PDF p. 3, Theorem B / Theorem 4.2. Quote: "finite logarithmic measure".
- PDF p. 10, Theorem 2.4. Quote: "counted with multiplicity".
- PDF p. 13, Theorem 3.1. Quote: "number of zeros".
- PDF p. 13, Corollary 3.2. Quote: "converges".

Use:

- source for RH-conditional EC Euler product asymptotic outside a finite
  logarithmic measure exceptional set;
- source for EC zero counting `N_E(t)=O_E(t log t)`;
- source for `sum 1/|gamma|^2 < infinity` over EC zeros.

Limit:

- exceptional-set result is not pointwise all large `K`;
- zero counting and `sum 1/|gamma|^2` do not bound `1/L'(rho)`;
- logarithmic-derivative explicit formulas are not reciprocal Perron formulas.

Decision: `SOURCE_SUPPORTED` for zero counting and exceptional-set product;
`LITERATURE_BLOCKED` for H1.

### de Faveri 2024/2025 JEMS

URL: `https://ems.press/content/serial-article-files/48859`

Fetched as `faveri_simple_gl2.pdf`; extracted with:

```bash
./xpdf-tools-mac-4.06/binARM/pdftotext -layout faveri_simple_gl2.pdf faveri_simple_gl2.txt
```

Anchors:

- PDF p. 1, abstract. Quote: "first power bound".
- PDF p. 2, Theorem 1.1. Quote: "Power bound for arbitrary level".
- PDF p. 1, introduction. Quote: "are all simple".

Use:

- source that primitive holomorphic GL(2) L-functions have a power lower
  bound for simple zeros;
- relevant to elliptic curves after modular normalization.

Limit:

- does not prove all zeros are simple;
- does not prove bounded multiplicity;
- does not bound reciprocal derivatives at zeros.

Decision: `SOURCE_SUPPORTED` for existence/power lower bound of simple zeros;
`NO_CLOSURE` for H1 zero simplicity needs.

### Barrett et al. 2015

URL: `https://arxiv.org/pdf/1410.7765`

Fetched as `barrett_gl2_gaps_derivative_moments.pdf`; extracted with:

```bash
./xpdf-tools-mac-4.06/binARM/pdftotext -layout barrett_gl2_gaps_derivative_moments.pdf barrett_gl2_gaps_derivative_moments.txt
```

Anchors:

- PDF p. 1, abstract. Quote: "mixed second moments of derivatives".
- PDF p. 3, Theorem 1.5. Quote: "non-negative integers".

Use:

- adjacent GL(2) source for continuous positive derivative moments on the
  critical line.

Limit:

- not a discrete moment over zeros;
- not a negative moment;
- no theorem for `sum |L'(rho)|^{-q}` or weighted `1/L'(rho)` aggregates.

Decision: `ADJACENT_ONLY`; does not close H1.

### Bui-Florea-Milinovich 2023

URL: `https://arxiv.org/pdf/2310.03949`

Fetched as `bfmn_negative_zeta_derivative.pdf`; extracted with:

```bash
./xpdf-tools-mac-4.06/binARM/pdftotext -layout bfmn_negative_zeta_derivative.pdf bfmn_negative_zeta_derivative.txt
```

Anchors:

- PDF p. 1, abstract. Quote: "negative discrete moments".
- PDF p. 2, Theorem 1.1. Quote: "Assume the Riemann hypothesis".
- PDF p. 3, discussion. Quote: "simplicity of zeros is not enough".

Use:

- zeta-only warning: even for zeta, negative derivative moments are delicate,
  conditional, and often restricted to subfamilies or extra hypotheses.

Limit:

- not EC;
- not GL(2);
- cannot be imported to H1 reciprocal Perron.

Decision: `MODEL_ONLY`; not a source for EC/GL(2) H1.

## Dependencies And Decisions

| H1 ingredient | Source status | Decision |
|---|---|---|
| Mellin identity for fixed compact `W` | standard/in-repo | Prove locally; FI only supports sharp Perron background. |
| Central pole polynomial | local algebra | Closed algebraically once analytic rank and Taylor coefficient are declared. |
| Offcentral simple residue formula | local algebra | Formula closed; aggregate control not closed. |
| Offcentral multiple zeros | Inoue/de Faveri warn indirectly | No all-simple or bounded-multiplicity theorem found for fixed EC/GL(2). |
| EC zero counting | Sheth Theorem 3.1/Cor. 3.2 | Pure multiplicity sums with `|gamma|^-2` are source-supported. |
| `1/L'(rho)` bounds/moments | none for EC/GL(2) found | `LITERATURE_BLOCKED`. |
| H1 pointwise residue aggregate | no source | `LITERATURE_BLOCKED`. |
| Exceptional-set BSD-Mertens | Sheth Theorem 4.2 | Source-supported only off finite logarithmic measure; not pointwise H1/H2. |
| Hard product equivalence | Kuo-Murty/Conrad | Source-supported as equivalence/depth warning, not proof. |
| GL(2) simple zeros | de Faveri | Some/power many simple zeros; not all zeros simple. |

## What Sources Do Not Prove

1. They do not prove

```text
sum_{rho != 1} K^(rho-1) W_hat(rho-1)/L'(rho) = o((log K)^r)
```

pointwise for a fixed elliptic curve.

2. They do not prove absolute convergence of

```text
sum_{gamma != 0} |W_hat(i gamma)/L'(1+i gamma)|.
```

Sheth gives `sum 1/|gamma|^2 < infinity`, but no derivative denominator.

3. They do not rule out offcentral multiple zeros. A zero of multiplicity `m`
can give `K^(i gamma)(log K)^(m-1)` in H1.

4. They do not give rank-zero pointwise stabilization. Simple offcentral
residues are constant scale when `r=0`.

5. They do not let H1 inherit H2/S1 `1/log K` branch damping. H1 has
reciprocal poles, not logarithmic branches.

6. They do not upgrade Sheth's finite-log-measure exceptional set to an
all-large-`K` pointwise theorem.

7. They do not prove an EC/GL(2) Gonek-Hejhal analogue for negative moments
of `L'(rho)`.

8. They do not justify replacing analytic rank `ord_{s=1} L(E,s)` by
algebraic rank.

## Do Not Promote Unless

- H1 is proved or sourced as its own reciprocal-pole theorem.
- The same smoothing kernel and Mellin normalization are used throughout.
- Analytic rank `r = ord_{s=1} L(E,s)` is stated before any algebraic rank.
- Offcentral simple residues are either absolutely summable, canceled below
  `o((log K)^r)`, retained as an oscillatory term, or averaged in a declared
  averaged theorem.
- Offcentral multiple zeros are ruled out, bounded below main scale, retained,
  or averaged.
- Rank zero is separated.
- Sheth is not cited as H1 control.
- Kuo-Murty/Conrad are not cited as proving pointwise BSD-Mertens.
- de Faveri is not cited as all-zero simplicity.
- Barrett et al. is not cited as reciprocal derivative control.
- Bui-Florea-Milinovich is not cited outside zeta.

## Confidence

Confidence: `0.86`.

Reason: the negative verdict is strongly supported by fresh source checks and by
agreement with prior in-repo audits. Residual uncertainty remains because I did
not exhaust every possible GL(2) reciprocal-derivative paper; therefore the exact
missing theorem is `LITERATURE_BLOCKED`, not "false."

## Changed Files

- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md`

No edits were made by me to `HANDOFF.md`,
`L2_facts/farey-claim-ledger.md`, `log.md`, or other agent files.

## Commands Run

Local startup/context:

```bash
sed -n '1,220p' start.md
./te doctor
sed -n '1,220p' token-economy.yaml
sed -n '1,220p' L0_rules.md
sed -n '1,260p' L1_index.md
sed -n '1,260p' HANDOFF.md
sed -n '1,260p' L2_facts/farey-claim-ledger.md
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
```

Source fetches:

```bash
mkdir -p /tmp/h1-source-audit-20260511
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac.tar.gz
curl -L --fail -o inoue_jtnb_1162.pdf https://www.numdam.org/item/10.5802/jtnb.1162.pdf
curl -L --fail -o fi_opera_ch1.pdf https://assets.press.princeton.edu/chapters/s8585.pdf
curl -L --fail -o kuo_murty_cjm_2005.pdf https://mast.queensu.ca/~murty/Kuo-Murty-CJM.pdf
curl -L --fail -o conrad_cjm_2005.pdf https://kconrad.math.uconn.edu/articles/eulerprod.pdf
curl -L --fail -o sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236
curl -L --fail -o faveri_simple_gl2.pdf https://ems.press/content/serial-article-files/48859
curl -L --fail -o barrett_gl2_gaps_derivative_moments.pdf https://arxiv.org/pdf/1410.7765
curl -L --fail -o bfmn_negative_zeta_derivative.pdf https://arxiv.org/pdf/2310.03949
curl -L --fail -o sound_mobius_0705.0723.pdf https://arxiv.org/pdf/0705.0723
```

Extraction/search:

```bash
for f in inoue_jtnb_1162 fi_opera_ch1 kuo_murty_cjm_2005 conrad_cjm_2005 sheth_ec_arxiv_2312.05236 sound_mobius_0705.0723 faveri_simple_gl2 bfmn_negative_zeta_derivative barrett_gl2_gaps_derivative_moments; do ./xpdf-tools-mac-4.06/binARM/pdftotext -layout "$f.pdf" "$f.txt"; done
rg -n "1/L'|L'\\(|reciprocal|negative|discrete moments|zeta'|derivative|simple zeros|multiplicity" *.txt
rg -n "Theorem 1|Theorem 2|multiplicity|We do not know" inoue_jtnb_1162.txt
rg -n "Perron|Lemma 1\\.1|Mertens|Theorem 1\\.2" fi_opera_ch1.txt
rg -n "if and only if|oscillates|Theorem" kuo_murty_cjm_2005.txt
rg -n "reciprocal|equivalent|Theorem 1\\.3|Theorem 6\\.2" conrad_cjm_2005.txt
rg -n "finite logarithmic measure|Theorem 2\\.4|Theorem 3\\.1|Corollary 3\\.2" sheth_ec_arxiv_2312.05236.txt
rg -n "Theorem|simple zeros|Power bound" faveri_simple_gl2.txt
rg -n "Theorem 1\\.5|mixed second moments|derivatives" barrett_gl2_gaps_derivative_moments.txt
rg -n "negative discrete moments|Theorem 1\\.1|simplicity of zeros is not enough" bfmn_negative_zeta_derivative.txt
shasum -a 256 *.pdf
```

Write/verify:

```bash
mkdir -p handoff-2026-05-11-h1-reciprocal-perron-wave
mv '/Users/za/Documents/Farey NOW/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md' '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md'
rmdir '/Users/za/Documents/Farey NOW/handoff-2026-05-11-h1-reciprocal-perron-wave'
git status --short -- HANDOFF.md L2_facts/farey-claim-ledger.md log.md handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md
```
