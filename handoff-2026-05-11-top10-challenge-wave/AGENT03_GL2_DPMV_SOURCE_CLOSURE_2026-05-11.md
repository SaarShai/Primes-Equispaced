---
schema_version: 1
title: "Agent 03 GL2 DPMV Source Closure"
date: 2026-05-11
agent: "Agent 03"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.90
tags: [top10-challenge-wave, h1, gl2, dpmv, bfmt, milinovich-ng, li-zaharescu]
---

# Agent 03 GL2 DPMV Source Closure

Status: `RIGOROUS_REDUCTION`. No theorem promoted.

## Verdict

`BFMT-CoefficientDPMV(E,k=1/2)` is not source-closed by the checked papers.

The strongest source-backed theorem available for one fixed elliptic curve/newform is:

```text
MN-DiscreteMeanSquare-GL2(f,eta):
  Let f be one fixed normalized holomorphic newform in the Milinovich-Ng
  normalization, and assume RH_f. For A(s)=sum_{n<=Y} a(n)n^(-s), Y asymp T,
  if a(n) satisfies Milinovich-Ng (39) and (40), then the zero-discrete
  mean-square formula (41) holds over T<gamma_f<=2T.
```

This gives a real GL2 DPMV layer, but not BFMT's zeta-layer strength. The precise missing check is still:

```text
BFMT-CoefficientErrorCheck(E,k=1/2):
  Every BFMT coefficient family in Propositions 2.5, 2.6, and 2.7 must satisfy
  Milinovich-Ng (39),(40), and the extra GL2 terms
    Re sum ((Lambda_f*a)(n) conjugate(a(n)))/n
    T logT sum |(Lambda_f*a)(n)|^2 / n^(1+1/logT)
  must be absorbed at the exact BFMT k=1/2 target T^(1+delta).
```

Milinovich-Ng Proposition 4.3 adds useful prime-block high moments, but only under the support wall `x^m <= T^(2/3)`. BFMT's own parameter constraints allow cumulative support up to `T^(1-o(1))`, so Proposition 4.3 does not by itself reproduce BFMT's Section 5 coefficient theorem.

Li-Zaharescu Theorem 4.1 is not a BFMT coefficient DPMV. It is a mollified moment asymptotic for general Selberg-class `L` under RH plus almost-all-simple zeros. It can support contour/mollifier discussions, but it does not replace BFMT Theorem 3.1 for arbitrary coefficient families.

## Source Protocol

Workspace:

```bash
/tmp/farey-agent03-dpmv-20260511
```

Commands:

```bash
curl -L --fail -sS -o xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac-4.06.tar.gz

curl -L --fail -sS -o bfmt_2310_03949.pdf \
  https://arxiv.org/pdf/2310.03949
curl -L --fail -sS -o milinovich_ng_1306_0854.pdf \
  https://arxiv.org/pdf/1306.0854
curl -L --fail -sS -o li_zaharescu_DLrho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'

./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  bfmt_2310_03949.pdf bfmt_2310_03949.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  milinovich_ng_1306_0854.pdf milinovich_ng_1306_0854.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  li_zaharescu_DLrho.pdf li_zaharescu_DLrho.txt
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_2310_03949.pdf
7429a8705e1d7e790a925bd7a410338a52e24ab060e890bdb13f9b8780810f10  milinovich_ng_1306_0854.pdf
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011  li_zaharescu_DLrho.pdf
```

## Source Claims

BFMT Theorem 3.1, PDF p. 8, is the zeta coefficient theorem BFMT needs. It assumes RH and gives a mean square over zeta zeros for coefficients `a_n` of length `x`; quote: "any sequence of complex numbers". Its formula has the zeta off-diagonal von Mangoldt term and an error of shape

```text
O( x (log(xT))^2 sum_{n<=x} |a_n|^2/n ).
```

BFMT Theorem 1.1, PDF p. 2, equation (1.2), gives the separated-zero negative moment target. At `k=1/2`, the second case gives

```text
sum_{gamma in F} |zeta'(rho)|^(-1) << T^(1+delta).
```

BFMT Propositions 2.5, 2.6, and 2.7, PDF p. 8, are the coefficient-family estimates driven by Theorem 3.1. Their support hypotheses are:

```text
beta0*s0 <= 1 - loglogT/logT,
sum_{h<=j} ell_h beta_h + s_{j+1} beta_{j+1} <= 1 - loglogT/logT,
sum_{h<=K} ell_h beta_h <= 1 - loglogT/logT.
```

BFMT parameter choices, PDF p. 15, equations (5.4),(5.5), choose `beta_K <= c` and explicitly state the conditions ensure the cumulative supports above remain below `1 - loglogT/logT`. For `k=1/2`, BFMT falls into the `2k(1+epsilon)>1` branch, PDF p. 15, equations (5.6),(5.7), but still reaches the same `T^(1+delta)` target after equations (5.17) and the final relabeling on PDF p. 18.

Milinovich-Ng set the GL2 object, PDF p. 11, equations (17),(18): normalized holomorphic newforms and the associated `L(s,f)`. Quote: "critical line ... is Re(s)=1/2". For the requested fixed elliptic curve/newform setup, this packet states the sourced DPMV theorem for the fixed newform; translating EC notation to this normalized center is bookkeeping, not a new DPMV input.

Milinovich-Ng Lemma 3.3, PDF p. 14, is the GL2 Landau-Gonek formula. Quote: "version of the Landau-Gonek explicit formula". It gives

```text
sum_{0<gamma_f<=T} x^(rho_f)
 = -T Lambda_f(x)/(2*pi)
   + O(x log(2xT) loglog(3x))
   + O(log x min(T, x/<x>))
   + O(log(2T) min(T, 1/log x)).
```

This source-closes only the explicit-formula ingredient.

Milinovich-Ng conditions (39),(40), PDF p. 18, require for some `0<eta<=1/2`:

```text
sum_{n<=x} |a(n)|   << x log(xT) (log x)^(-eta),
sum_{n<=x} |a(n)|^2 << x (log(xT))^2,
```

uniformly for `x>=1`.

Milinovich-Ng Proposition 4.1, PDF p. 19, equation (41), is the strongest fixed-newform GL2 DPMV theorem checked here. Quote: "coefficients a(n) satisfying (39) and (40)". It states, under RH_f, with `X=sqrt(q)T/(2*pi)` and `Y asymp T`,

```text
sum_{T<gamma_f<=2T} |A(rho_f)|^2
 = T log X/pi * sum_{n<=Y} |a(n)|^2/n
   - Re sum_{n<=Y} ((Lambda_f*a)(n) conjugate(a(n)))/n
   + O( T(logT)^(4-2eta)
        + T logT sum_{n>=1} |(Lambda_f*a)(n)|^2/n^(1+1/logT) ).
```

Milinovich-Ng Proposition 4.3, PDF p. 19, equations (43),(44), is the prime-supported high-moment supplement. Quote: "xm <= T2/3". For any complex `a(p)`, `Re(w)>=0`, and `x^m<=T^(2/3)`, it gives the two `2m`-th moment bounds for prime sums over zeros, with constants depending only on `f`.

Li-Zaharescu include holomorphic cusp form L-functions in their class, PDF p. 2; quote: "holomorphic cusp forms". Theorem 4.1, PDF p. 7, assumes RH and quote: "almost all zeros ... simple". With `M=T^theta`, `theta<1`, it gives an asymptotic for the mollified moment `S1` plus an explicit error. This is a different theorem type: mollified `S1`, not arbitrary BFMT coefficients and not a BFMT separated-zero coefficient DPMV.

## Comparison

| Source | What it gives | BFMT-CoefficientDPMV relevance | Gap |
|---|---|---|---|
| BFMT Theorem 3.1 | Zeta zero mean square for arbitrary `a_n` | Exactly the zeta coefficient engine used in Propositions 2.5-2.7 | Zeta only |
| Milinovich-Ng Lemma 3.3 | GL2 Landau-Gonek explicit formula | Source-closes `LG-Explicit-GL2(f)` | No coefficient mean square by itself |
| Milinovich-Ng Proposition 4.1 | GL2 zero mean square for `A(s)` | Strongest fixed-newform DPMV layer | Needs (39),(40) and new convolution/off-diagonal absorption |
| Milinovich-Ng Proposition 4.3 | Prime-block high moments | Useful for Soundararajan-style short blocks | `x^m<=T^(2/3)` wall, below BFMT near-`T` support |
| Li-Zaharescu Theorem 4.1 | General Selberg-class mollified `S1` asymptotic | May support contour/mollifier side arguments | Assumes almost-all-simple zeros; not arbitrary coefficient DPMV |

## Exact Gap To `BFMT-CoefficientDPMV(E,k=1/2)`

For a fixed elliptic curve/newform, the source-backed theorem is:

```text
MN-DiscreteMeanSquare-GL2(f,eta) + MN-PrimeHighMoment-GL2(f,2/3).
```

The desired theorem is stronger:

```text
BFMT-CoefficientDPMV(E,k=1/2):
  BFMT Propositions 2.5, 2.6, and 2.7 remain true with zeta zeros replaced by
  zeros of L(s,f), after EC/newform normalization and finite bad-prime removal,
  with final separated-zero bound T^(1+delta).
```

The missing proof obligations are finite and exact:

1. Transcribe every BFMT `k=1/2` coefficient family from Propositions 2.5, 2.6, and 2.7.
2. Prove Milinovich-Ng (39) for each family.
3. Prove Milinovich-Ng (40) for each family.
4. Bound

```text
T logT sum |(Lambda_f*a_BFMT)(n)|^2 / n^(1+1/logT)
```

within the same log-log budget BFMT uses.

5. Bound or sign-dispose of

```text
Re sum ((Lambda_f*a_BFMT)(n) conjugate(a_BFMT(n)))/n.
```

6. Check that finite ramified primes of `E` can be removed from BFMT prime blocks or absorbed into constants without changing exponents.
7. Do not use Milinovich-Ng Proposition 4.3 beyond `x^m<=T^(2/3)`; BFMT's cumulative support can reach `T^(1-o(1))`.

## Decision

`LG-Explicit-GL2(f)` is `SOURCE_CLOSED`.

`DPMV-GL2-GeneralA(f,eta)` is `SOURCE_BACKED`.

`DPMV-GL2-PrimePowerHighMoment(f,2/3)` is `SOURCE_BACKED`.

`BFMT-CoefficientDPMV(E,k=1/2)` is `OPEN`: not disproved, but not source-closed. The live blocker is exactly `BFMT-CoefficientErrorCheck(E,k=1/2)`.

No Koyama correspondence or email drafts touched.
