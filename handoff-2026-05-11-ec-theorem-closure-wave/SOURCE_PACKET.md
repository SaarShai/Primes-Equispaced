---
schema_version: 1
title: "Source packet: EC theorem closure wave"
date: 2026-05-11
type: source-packet
tier: working
status: AUDIT_ONLY
confidence: 0.82
tags: [ec-ndc, sources, s1, h2, perron, sym2, mertens]
---

# Source Packet

Status: `AUDIT_ONLY`; exact fixed-curve endpoint-smoothed S1/H2/H1 theorem remains `LITERATURE_BLOCKED`.

Verdict: narrow inputs closed only for ordinary prime-Mertens and EC zero-counting/summability of pure multiplicity weights. No verified source proves the exact Agent 3 fixed-curve smoothstep theorem for `S_1,W(K)`, `S_sym,W(K)`, pointwise `H2`, or reciprocal Perron `H1`.

## Protocol

Run directory:

```bash
/tmp/agent6-source-packet-20260511
```

Tooling:

```bash
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -v
```

PDF fetches:

```bash
curl -L --fail -o ils_math_9901141.pdf https://arxiv.org/pdf/math/9901141
curl -L --fail -o kuo_murty_cjm_2005.pdf https://mast.queensu.ca/~murty/Kuo-Murty-CJM.pdf
curl -L --fail -o conrad_cjm_2005.pdf https://kconrad.math.uconn.edu/articles/eulerprod.pdf
curl -L --fail -o sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236
curl -L --fail -o friedlander_iwaniec_opera_ch1.pdf https://assets.press.princeton.edu/chapters/s8585.pdf
curl -L --fail -o hoffstein_lockhart_maass_siegel.pdf https://www.math.columbia.edu/~goldfeld/CoeffMaassForms.pdf
```

Text extraction:

```bash
for f in ils_math_9901141 kuo_murty_cjm_2005 conrad_cjm_2005 sheth_ec_arxiv_2312.05236 friedlander_iwaniec_opera_ch1 hoffstein_lockhart_maass_siegel; do ./xpdf-tools-mac-4.06/binARM/pdftotext -layout "$f.pdf" "$f.txt"; done
```

SHA256:

```text
5072c63324c329250f70c4ef4e2648a0e8ff465d6b9c241c3d3646d4c6759997  ils_math_9901141.pdf
067e6b30245aa9a1872b36450a72e504963e902c3d4e1c611bbf9752c94e0488  kuo_murty_cjm_2005.pdf
f47a79e230d3be630e1c5a28e842d62416b403602bc4d11f9e9d3a4438dc8b6a  conrad_cjm_2005.pdf
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_arxiv_2312.05236.pdf
080fbff5d5f122678cddd78a1b0561a79952c5fe72b49cf2fbc6b014edc0e8dc  friedlander_iwaniec_opera_ch1.pdf
031de26f73977602225ec96b2207f3070cfc7d6b3cfc2371faed52ee254fb632  hoffstein_lockhart_maass_siegel.pdf
```

## Dependency Verdicts

| Dependency | Source status | Decision |
|---|---|---|
| S1 explicit formula for `sum_p W(p/K)a_p/p` | adjacent only | `LITERATURE_BLOCKED`; prove in repo. |
| EC zero counting for pure multiplicity weighted branch sums | source-supported | Closed for `sum m_gamma |W_hat(i gamma)|` if `W_hat=O(|gamma|^-2)`. |
| Reciprocal-zero derivative/summability for H1 | not sourced | `LITERATURE_BLOCKED`; Sheth zero counting is not `1/L'(rho)` control. |
| Sym2 finite part for exact good-prime `a_p^2/p-1` object | adjacent only | `LITERATURE_BLOCKED`; source a GL(3)/adjoint finite-part theorem or prove in repo. |
| Ordinary prime-Mertens finite part | source-supported | Closed unweighted; weighted smoothstep finite part is an in-repo Abel/Stieltjes lemma. |
| Perron/Mellin smoothing | standard Perron source only | Exact smoothstep contour shift remains in-repo proof obligation. |
| EC pointwise BSD-Mertens/H2 product | adjacent only | Kuo-Murty/Conrad/Sheth do not prove pointwise all-`K` H2. |

## Verified Sources

### Iwaniec-Luo-Sarnak, arXiv:math/9901141

URL: `https://arxiv.org/pdf/math/9901141`

Verified anchors:
- PDF p. 12, Proposition 3. Quote: "explicit formula relating the zeros".
- PDF p. 36, Proposition 4 near equation (140). Quote: "approximate explicit formula".
  Separate prime-linear `f(p)` and prime-square `f(p^2)` terms occur.
- PDF p. 11, equations (13)-(15), symmetric-square setup. Quote: "Euler product of degree 3 is entire".

Use allowed:
- Cite as adjacent GL(2)/family explicit-formula evidence that prime-linear and prime-square terms both occur.
- Cite as adjacent support that symmetric-square analytic input is a real automorphic object.

Limit:
- Does not prove fixed elliptic-curve `K -> infinity` endpoint-smoothed `W(p/K)` formula.
- Does not prove the exact Agent 3 `S_sym,W` finite part.

### Kuo-Murty, Canad. J. Math. 57 (2005)

URL: `https://mast.queensu.ca/~murty/Kuo-Murty-CJM.pdf`

Verified anchors:
- PDF p. 2/journal p. 329. Quote: "if and only if C~(x) = o(x)".
- PDF p. 4/journal p. 331, Lemma 1. Quote: "C(x) = -r log log x".
- PDF pp. 9-10/journal pp. 336-337, Theorem 4/Proposition 5. Quote: "R(x) oscillates".

Use allowed:
- Cite for hard-cut EC BSD-product equivalence to a strong prime-power error condition.
- Cite for warning that product remainders can oscillate.

Limit:
- Does not prove the product asymptotic unconditionally.
- Does not state endpoint-smoothed `S_1,W`, `S_sym,W`, or Agent 3 H2.

### Conrad, Canad. Math. J. 57 (2005)

URL: `https://kconrad.math.uconn.edu/articles/eulerprod.pdf`

Verified anchors:
- PDF p. 1, equations (1.1)-(1.2). Quote: "#Ens(Fp)/p equals the reciprocal".
- PDF p. 3, Theorem 1.3/equation (1.4). Quote: "Equation (1.2) is equivalent to".
- PDF pp. 15-16, Theorem 6.2. Quote: "conditions are equivalent".
- PDF p. 20. Quote: "does not converge at logarithmic singularities".

Use allowed:
- Cite local-factor bridge between `#E_ns(F_p)/p` and reciprocal Euler factors.
- Cite pointwise hard-product asymptotic as deeper than RH-level input.

Limit:
- Does not prove Agent 3 smoothed H2.
- Does not supply S1 branch continuation or zero-summability for the endpoint kernel.

### Sheth, arXiv:2312.05236v4

URL: `https://arxiv.org/pdf/2312.05236`

Verified anchors:
- PDF p. 1 abstract. Quote: "outside a set of finite logarithmic measure".
- PDF pp. 6-7, Theorem 2.3. Quote: "the sum over rho".
- PDF p. 10, Theorem 2.4. Quote: "Assume the Riemann Hypothesis".
- PDF p. 13, Theorem 3.1. Quote: "number of zeros".
- PDF p. 13, Corollary 3.2. Quote: "converges".
- PDF p. 16, Theorem 4.2. Quote: "finite logarithmic measure".

Use allowed:
- Cite EC zero counting: Theorem 3.1 gives `N_E(t)=O_E(t log t)`, and Corollary 3.2 gives convergence of the reciprocal-square zero sum.
- Thus, with in-repo smoothstep decay `W_hat(i gamma)=O(|gamma|^-2)`, the pure multiplicity sum `sum |m_gamma W_hat(i gamma)|` is source-supported.
- Cite as adjacent EC product explicit formula with zero and square terms retained.

Limit:
- Does not prove all-large-`K` pointwise H2; it has finite-log-measure exceptions.
- Does not prove the endpoint-smoothed S1 branch theorem.
- Does not control H1 reciprocal residues `1/L'(rho)` or multiple-zero Laurent coefficients.

### Friedlander-Iwaniec, chapter PDF

URL: `https://assets.press.princeton.edu/chapters/s8585.pdf`

Verified anchors:
- PDF p. 11, Lemma 1.1/equation (1.4.7). Quote: "we have".
- PDF p. 17, Theorem 1.2/equation (1.4.17). Quote: "Mertens' Prime Number Theorem".

Use allowed:
- Cite ordinary prime-Mertens:
  `sum_{p<=x} 1/p = log log x + C + o(1)`.
- Removing finitely many bad primes changes only the constant.
- Weighted smoothstep finite part follows by an in-repo Stieltjes/Abel transfer for the same `W`; do not cite this source as already proving the exact weighted theorem.
- Cite standard Perron only as background. The exact Mellin inversion and contour shifts for the smoothstep theorem still need in-repo proof.

Limit:
- Not an EC source.
- Does not prove S1/H2/H1 smoothing.

### Hoffstein-Lockhart, Annals 140 (1994)

URL: `https://www.math.columbia.edu/~goldfeld/CoeffMaassForms.pdf`

Verified anchors:
- PDF p. 3, equations (0.6)-(0.8). Quote: "adjoint square lift".
- PDF p. 5. Quote: "applied to holomorphic".

Use allowed:
- Adjacent source that adjoint/symmetric-square automorphic input is the correct family of objects.
- Helps justify looking for a GL(3)/adjoint finite-part theorem.

Limit:
- Does not prove the exact `S_sym,W(K)` finite part for the Agent 3 good-prime normalization.
- Do not use it alone to set `kappa_sym=0` in the current theorem package.

## Closed Narrow Inputs

### Ordinary Mertens

Closed as external unweighted theorem:

```text
sum_{p<=x} 1/p = log log x + C + o(1).
```

Required in-repo transfer:

```text
M_good,W(K) = sum_{p good} W(p/K)/p
            = log log K + C_M,E,W^good + o(1).
```

This transfer is elementary once ordinary Mertens is accepted and `W` is fixed compact support with `W(t)->1` at zero. Finite bad primes subtract `sum_{p bad}1/p` from the constant.

### EC Zero Counting For S1 Branch Sum

Closed for pure multiplicity weights:

```text
N_E(T)=O_E(T log T),
sum_gamma 1/|gamma|^2 < infinity.
```

With smoothstep `W_hat(i gamma)=O(|gamma|^-2)`, this supports:

```text
sum_{gamma != 0} |m_gamma W_hat(i gamma)| < infinity.
```

This closes only the `ZC` input in `S1_ZERO_SUMMABILITY.md` for zeros of `L(E,s)`. It does not close branch continuation, contour tails, Sym2 zeros, or H1 reciprocal derivative sums.

## Still In-Repo Proof Territory

1. `S_1,W` branch theorem for the exact fixed curve and smoothstep endpoint kernel.
2. Local proof that offcentral S1 singularities are logarithmic branches, not poles.
3. Contour-shift and horizontal-edge estimates for that branch theorem.
4. `S_sym,W` finite part for the exact good-prime object with `chi_sym2(p)=a_p^2/p-1`.
5. Source-verified or in-repo proof that `kappa_sym=0` for the exact normalization, if used.
6. Sym2 zero/pole counting and weighted branch summability in the same shifted strip.
7. H1 reciprocal Perron theorem, including `1/L'(rho)` or higher Laurent coefficient control.
8. Pointwise all-`K` H2. Sheth is exceptional-set only; Kuo-Murty/Conrad are equivalence/obstruction sources.

## Do Not Promote Unless

- Analytic rank `r=ord_{s=1}L(E,s)` is stated before script/algebraic rank.
- Exact Agent 3 local factors are retained:
  good `1-a_p/p+1/p`, bad `1-a_p/p`.
- `S_1,W`, `S_sym,W`, `M_good,W`, `R_ge3`, and bad-prime constants are all present before claiming H2 coefficient `-r`.
- Sheth is not cited as proving pointwise smoothed H2.
- ILS is not cited as proving fixed-curve endpoint-smoothed S1.
- Kuo-Murty/Conrad are not cited as proving the BSD product asymptotic; they identify equivalent/deeper conditions.
- Sheth zero counting is not used as reciprocal-derivative control for H1.
- Any new Sym2/GL(3), H1, or smoothing theorem citation gets the same `curl + pdftotext + quote + page/equation` treatment.

## Commands Used For Spot Checks

```bash
rg -n "explicit formula|Proposition 3|Proposition 4|lambda_f|prime-square|sym" ils_math_9901141.txt
rg -n "if and only if|C\(x\)|R\(x\)|oscillates|N_p|Birch" kuo_murty_cjm_2005.txt
rg -n "Equation \(1\.2\)|equivalent|finite part|logarithmic singularities|#E|Ens|Theorem 6\.2|Prod" conrad_cjm_2005.txt
rg -n "finite logarithmic measure|Theorem 2\.3|Theorem 2\.4|R_s|U_s|outside|zeros|Theorem B|Corollary" sheth_ec_arxiv_2312.05236.txt
rg -n "Mertens|Theorem 1\.2|Perron|Lemma 1\.1|log log|\(1\.4\.17\)|\(1\.4\.7\)" friedlander_iwaniec_opera_ch1.txt
rg -n "symmetric square|Sym|L\(1, sym|non-zero|nonzero|entire|holomorphic|Gelbart|Jacquet|Theorem" hoffstein_lockhart_maass_siegel.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -f 13 -l 13 sheth_ec_arxiv_2312.05236.pdf -
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -f 17 -l 17 friedlander_iwaniec_opera_ch1.pdf -
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -f 36 -l 36 ils_math_9901141.pdf -
```
