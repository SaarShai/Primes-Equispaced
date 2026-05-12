---
schema_version: 1
title: "S1-B source audit: smoothed EC prime trace explicit formula"
date: 2026-05-11
type: source-audit
tier: working
status: LITERATURE_BLOCKED
confidence: 0.74
sources:
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2A_LITERATURE_AUDIT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
  - /tmp/s1b-ec-explicit-src/ils_math_9901141.pdf
  - /tmp/s1b-ec-explicit-src/kuo_murty_cjm_2005.pdf
  - /tmp/s1b-ec-explicit-src/conrad_cjm_2005.pdf
  - /tmp/s1b-ec-explicit-src/sheth_ec_arxiv_2312.05236.pdf
tags: [ec-ndc, s1, explicit-formula, gl2, source-audit]
---

# S1-B Source Audit

status: `LITERATURE_BLOCKED`

## Question

Audit whether existing verified sources imply an explicit formula for

```text
S_1,W(K) = sum_p W(p/K) a_p/p
```

in one of the theorem modes required by the S1 manifest:

```text
pointwise:   S_1,W(K) = main loglog term + C_E,W + o(1)
oscillatory: S_1,W(K) = main loglog term + C_E,W + Z_E,W(log K) + o(1)
averaged:    a logarithmic u=log K average has a finite part
```

H2-B/H2-C identify the coefficient target, before any zero term, as

```text
(1/2 + kappa_sym/2 - r) log log K,
r = ord_{s=1} L(E,s).
```

In the H2 notation, setting `kappa_sym=0` gives `(1/2-r) log log K`, but this
audit did not independently close the symmetric-square finite-part theorem.

## Verdict

No audited source gives the exact `S_1,W(K)` formula for a fixed elliptic curve,
the sprint smoothstep/endpoint weight `W(p/K)`, and `K -> infinity`.

What the sources do support:

- GL(2) explicit formulas contain the prime-linear trace term
  `lambda_f(p)/sqrt(p) = a_p/p`, but in conductor-scaled zero-density weights,
  not as the fixed-curve endpoint sum `W(p/K)`.
- EC partial Euler product formulas contain explicit noncentral zero sums and
  prove sharp BSD-Mertens-type products only with exceptional-set or strong
  error hypotheses.
- BSD-Mertens product asymptotics are equivalent to a prime-power error
  condition stronger than RH-level input in the audited sources.
- Oscillation is structurally supported for related product remainders, but no
  verified source gives the exact zero series `Z_E,W(log K)` for this S1 sum.

Therefore:

| Mode | Source-implied? | Audit decision |
|---|---:|---|
| Pointwise `C+o(1)` | No | Do not promote. Needs a new derivation proving all noncentral zero terms are `o(1)` for this `W`. |
| Oscillatory | Not exactly | Best pointwise theorem target, but the coefficients and scale must be derived in S1-A/S1-C. |
| Averaged | No | Plausible fallback only after an oscillatory formula plus termwise/log-mean control. |

## Source Protocol

Protocol executed in `/tmp/s1b-ec-explicit-src`:

```bash
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -v
curl -L --fail -o ils_math_9901141.pdf https://arxiv.org/pdf/math/9901141
curl -L --fail -o kuo_murty_cjm_2005.pdf https://mast.queensu.ca/~murty/Kuo-Murty-CJM.pdf
curl -L --fail -o conrad_cjm_2005.pdf https://kconrad.math.uconn.edu/articles/eulerprod.pdf
curl -L --fail -o sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236
for f in ils_math_9901141 kuo_murty_cjm_2005 conrad_cjm_2005 sheth_ec_arxiv_2312.05236; do
  ./xpdf-tools-mac-4.06/binARM/pdftotext -layout "$f.pdf" "$f.txt"
done
```

`pdftotext` was Xpdf 4.06. System `pdftotext` was not installed.

## Verified Source Anchors

### Iwaniec-Luo-Sarnak, arXiv:math/9901141

Verified PDF: `/tmp/s1b-ec-explicit-src/ils_math_9901141.pdf`.

Anchor: PDF p. 1 identifies the paper as "Low Lying Zeros of Families of
L-Functions" by H. Iwaniec, W. Luo, and P. Sarnak.

Verbatim quote: "explicit formula relating the zeros" (PDF p. 12,
Proposition 3).

Relevant equation: PDF p. 36, Proposition 4, equation displayed before (140),
has the prime-linear term

```text
-(2/log N) sum_{p not | N} lambda_f(p) log p/sqrt(p)
  * phi_hat(log p/log N)
```

and a separate prime-square term

```text
-(2/log N) sum_{p not | N} lambda_f(p^2) log p/p
  * phi_hat(2 log p/log N).
```

Relevance to S1: for an elliptic curve/newform normalization,
`lambda_f(p)/sqrt(p)=a_p/p`. This is a verified GL(2) explicit-formula
appearance of the S1 prime trace.

Limit: the formula is conductor-scaled and zero-density oriented. It does not
state a fixed-curve limit as `K -> infinity` with endpoint weight `W(p/K)`, and
it keeps the prime-square term rather than proving the H2 finite part needed to
isolate S1.

### Kuo-Murty, Canad. J. Math. 57 (2005)

Verified PDF: `/tmp/s1b-ec-explicit-src/kuo_murty_cjm_2005.pdf`.

Anchor: PDF p. 1 defines `N_p=p+1-a_p` and the original BSD product; PDF p. 2
states the main equivalence.

Verbatim quote: "if and only if C~(x) = o(x)" (PDF p. 2).

Relevant equations/statements:

```text
C(x) := sum_{p^k <= x} (alpha_p^k + beta_p^k)/(k p^k)
```

appears in the definition on PDF pp. 3-4, with

```text
C(x) = -r log log x + A + o(1)
```

in Lemma 1 on PDF p. 4, conditional on the BSD product. The paper also states
`R(x) oscillates` in Theorem 4 on PDF p. 9.

Relevance to S1: the `k=1` piece of `C(x)` is the hard-cut trace
`sum_{p <= x} a_p/p`; the `k=2` and higher pieces are exactly the
quadratic/symmetric-square and absolutely convergent tail that H2-B says must
not be dropped.

Limit: this is not a smoothed S1 formula. It is a sharp full-log-product
statement, conditional/equivalent to a strong prime-power condition. The
oscillation theorem is for the product remainder `R(x)`, not an explicit
zero-Fourier formula for `S_1,W`.

### Conrad, Canad. Math. J. 57 (2005)

Verified PDF: `/tmp/s1b-ec-explicit-src/conrad_cjm_2005.pdf`.

Anchor: PDF p. 1, equations (1.1)-(1.2), match the EC product convention.

Verbatim quote: "#Ens(Fp)/p equals the reciprocal" (PDF p. 1).

Relevant equations/statements:

```text
Prod(E,x) = product_{p<=x} 1/(#E_ns(F_p)/p)              (1.2)
```

and

```text
Equation (1.2) is equivalent to E(x)=o(x log x).          (1.4)
```

are on PDF pp. 1-3. Theorem 6.2 on PDF pp. 15-16 gives the general finite-part
criterion for normalized Euler products, and PDF p. 20 warns that convergence
at logarithmic singularities on the critical line fails: "does not converge at
logarithmic singularities".

Relevance to S1: Conrad verifies that the EC product finite part is a strong
prime-power error theorem, not a consequence of local factor algebra. This
supports H2's reduction status and blocks citing a pointwise S1 finite part
from product folklore.

Limit: Conrad does not provide the sprint's smoothed `W(p/K)` S1 formula, and
the theorem is stated for hard-cut Euler product/Dirichlet-series finite parts.

### Sheth, arXiv:2312.05236v4

Verified PDF: `/tmp/s1b-ec-explicit-src/sheth_ec_arxiv_2312.05236.pdf`.

Anchor: PDF p. 1 identifies arXiv:2312.05236v4, dated 15 Jan 2026.

Verbatim quote: "outside a set of finite logarithmic measure" (PDF p. 1 and
Theorem B on PDF p. 3).

Relevant equations/statements:

Theorem 2.3 on PDF pp. 6-7 gives an explicit formula for a prime-power
Dirichlet sum with zeros of `L(E,s)` included. Theorem 2.4 on PDF p. 10 gives
an RH-conditional partial Euler product formula

```text
product_{p<=x} (...) = L(E,s) exp(-r I_s(x) - R_s(x) + U_s(x) + error),
```

where `R_s(x)` is the noncentral-zero term and `U_s(x)` is the prime-square
term. Theorem 4.2 on PDF p. 16 gives the BSD product asymptotic outside the
finite-log-measure exceptional set.

Relevance to S1: Sheth is the closest audited EC source. It explicitly retains
zero terms and square terms in the product formula, exactly the two features
the S1 sprint must handle.

Limit: it does not prove the pointwise smoothed S1 formula. It proves a sharp
product result outside an exceptional set under RH, not an all-large-`K`
endpoint-smoothed prime trace theorem.

## What Existing Sources Imply For S1

### Pointwise formula

Not implied.

The verified sources do not give

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K + C_1,E,W + o(1)
```

for the sprint kernel. Conrad/Kuo-Murty make the hard product finite part
equivalent to a strong prime-power error condition. Sheth obtains a related
sharp product only off a finite-log-measure exceptional set. ILS gives a
different smooth/log-weighted explicit formula in the conductor aspect.

### Oscillatory formula

Structurally supported, not source-closed.

Sheth's `R_s(x)` and ILS's zero-density explicit formula both show that
noncentral zeros enter adjacent GL(2)/EC prime formulas. Kuo-Murty's Theorem 4
supports oscillation in the related product remainder. But none of the audited
sources derives the exact coefficient, convergence class, or scale of

```text
Z_E,W(log K) = sum_{gamma != 0} c_E,W(gamma) exp(i gamma log K)
```

for `S_1,W(K)`. In particular, this audit cannot decide from sources alone
between the H2-B `K^(i gamma)/log K` branch and the H2-C persistent
`K^(i gamma)` branch.

### Averaged formula

Not implied.

A logarithmic average in `u=log K` would still require a summable
nonzero-frequency expansion, and no audited source states the required
fixed-curve averaged theorem for `S_1,W(exp u)`. ILS averages over families of
forms, not over `u` for one fixed elliptic curve. Sheth's exceptional-set
result is not the same as an averaged finite-part theorem for the
endpoint-smoothed S1 sum.

## Source-Closed Inferences Only

The following are safe to carry into S1-A/S1-C/S1-D:

1. Any S1 theorem must keep the prime-square/symmetric-square companion until
   its finite part is proved. This is visible in ILS Proposition 4 and Sheth
   Theorem 2.4, and matches H2-B.
2. The central coefficient should be stated with analytic rank
   `r=ord_{s=1}L(E,s)` before any algebraic-rank replacement.
3. Noncentral zeros cannot be silently dropped. They appear explicitly in the
   audited EC/GL(2) formulas.
4. A pointwise `C+o(1)` theorem is not available from the audited literature.
   It requires a new derivation or a stronger source not yet verified.

## Not Verified As Standalone Sources

These names appear in the audited PDFs or local handoffs, but I did not execute
the source protocol on them, so this audit does not cite them as facts:

```text
Goldfeld 1982, Birch-Swinnerton-Dyer 1965, Montgomery-Vaughan,
Iwaniec-Kowalski, Rubinstein 2013, Qu 2007, Gallagher 1980,
Selberg/Kimura-Koyama-Murty zero-count inputs, Gelbart-Jacquet/symmetric-square
finite-part sources.
```

## Dependencies

- `D1`: exact normalization from EC coefficients to newform coefficients:
  `lambda_f(p)=a_p/sqrt(p)` at good primes.
- `D2`: a Mellin/Stieltjes derivation for the exact endpoint kernel
  `W(p/K)`, not only conductor-scaled `phi_hat(log p/log N)`.
- `D3`: symmetric-square finite-part theorem for
  `sum_p W(p/K)(lambda_p^2-1)/p`.
- `D4`: explicit calculation of noncentral zero terms for the S1 weight,
  deciding `K^(i gamma)/log K`, persistent `K^(i gamma)`, or an averaged-only
  theorem.
- `D5`: branch convention for `log L(E,s)` and multiplicities at
  `s=1+i gamma`.
- `D6`: if using algebraic `rank(E)`, a BSD-rank equality assumption or
  per-curve analytic-rank verification.

## Do Not Promote

- Do not cite ILS as proving fixed-curve endpoint-smoothed S1.
- Do not cite Sheth as proving pointwise smoothed H2 or S1.
- Do not upgrade finite-log-measure exceptional-set results to all large `K`.
- Do not drop the `p^2`/symmetric-square term when extracting the S1
  coefficient.
- Do not state `-rank(E)` or `(1/2-rank(E))` before stating the analytic-rank
  version.
- Do not claim the averaged fallback until the oscillatory formula is available
  with summability or mean-square control.

## Confidence

Confidence `0.74`.

The negative conclusion is strong for the audited sources: they do not contain
the exact S1 theorem. Confidence is below `0.85` because the audit was focused
on the most relevant EC/GL(2) product and explicit-formula sources, not an
exhaustive search through all automorphic explicit-formula literature.
