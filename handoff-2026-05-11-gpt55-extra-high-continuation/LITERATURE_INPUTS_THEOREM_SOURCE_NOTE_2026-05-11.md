---
schema_version: 1
title: "Literature inputs theorem-source note"
date: 2026-05-11
agent: "Literature-Inputs"
type: theorem-source-note
tier: working
status: AUDIT_ONLY
confidence: 0.82
tags: [literature-inputs, gl1-perron, h1, h2, sym2, minimum-modulus]
---

# Literature Inputs Theorem-Source Note

No theorem is promoted. I searched the repo first, then spot-checked only
primary source pages/PDFs needed to pin exact names and theorem roles.

## Local Search Base

Primary local packets used:

- `handoff-2026-05-11-gpt55-extra-high-continuation/BIGGEST_CHALLENGES_MATRIX_2026-05-11.md`
- `handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md`
- `handoff-2026-05-11-gpt55-wave/GL1_PERRON_CLOSURE_PATH_2026-05-11.md`
- `handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md`
- `handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md`
- `handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md`
- `handoff-2026-05-11-h1-shell-moment-wave/FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md`
- `handoff-2026-05-11-h1-residue-control-wave/H2_SYM2_SOURCE_CLOSURE.md`
- `handoff-2026-05-11-ec-h2-mertens-sprint/H2A_LITERATURE_AUDIT.md`

## Candidate Source Inputs

### GL1 shifted Perron off-target residues

Source candidates:

- Aoki-Koyama, "Chebyshev's bias against splitting and principal primes in
  global fields", Journal of Number Theory 245 (2023), 233-262, equation
  (1.4). Primary: `https://www.sciencedirect.com/science/article/abs/pii/S0022314X22002335`
  and arXiv `https://arxiv.org/abs/2203.12266`.
- Shota Inoue, "Some explicit formulas for partial sums of Mobius functions",
  Journal de Theorie des Nombres de Bordeaux 33 (2021), 273-315, Theorem 1
  equation (1.4), Theorem 2 equation (2.1), Conjecture 1. Primary:
  `https://www.numdam.org/item/10.5802/jtnb.1162.pdf`.
- K. Soundararajan, "Partial sums of the Mobius function", arXiv:0705.0723,
  Theorem 1. Primary: `https://arxiv.org/pdf/0705.0723`.

Map:

- Aoki-Koyama supports the GL1 Euler-product side:
  `E_K(chi,rho) log K -> L'(rho,chi)/e^gamma` under DRH/EDRH, not
  `L'(rho,chi)/zeta(2)`.
- The Perron target residue is local algebra only:
  `Res_{w=0} K^w/(w L(rho+w,chi)) =
  log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2)`.
- Inoue is the best explicit-formula warning: zero multiplicities and
  reciprocal derivative behavior remain in the formula. It transfers the
  off-target aggregate; it does not remove it.
- Soundararajan gives a total Mobius bound under RH, but it is too coarse to
  isolate `Z_simple(K,T_K)=o(log K)`.

Confidence:

- 0.94 that these sources do not close the shifted Perron nonlocal remainder.
- 0.92 that AK closes only the Euler-product normalization.

Gap:

```text
ShiftedPerronNonlocalRemainder(chi,rho):
  after extracting the target residue from K^w/(wL(rho+w,chi)),
  all off-target residues, trivial residues, rectangle terms, and Perron
  errors are o(log K).
```

No checked source proves this. If off-target multiple zeros are not ruled out,
their Laurent residues must be retained or bounded explicitly.

### GL2/EC minimum modulus and legal heights

Source candidate:

- Junxian Li and Alexandru Zaharescu, "Value distribution of L'(rho)",
  Proposition 3.1 and Theorem 1.1. Primary:
  `https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf`.

Map:

- Proposition 3.1 gives selected heights in every unit interval with a
  subpower lower bound for `|L(s)|` in the normalized strip. After shifting the
  EC center from `1/2` to `1` and using the functional equation on the left
  side, this is a credible source route for H1 horizontal contour heights:
  `|1/L(E,s)| <= exp(A_E log T/log log T) = T^epsilon`.
- This maps to `H-height`, not to reciprocal residues.

Confidence:

- 0.72 that LZ closes the H-height exponent blocker for fixed GL2/EC after the
  normalization/reflection details are written cleanly.

Gaps:

- Need a precise EC normalization lemma: `L(E,s_E)` to normalized newform
  `L(w)` with `s_E=w+1/2`.
- Need left-edge reflection/gamma-factor estimates in the exact H1 rectangle.
- Still no bound for `1/L'(E,1+i gamma)` or multiple-zero Laurent
  coefficients.

### Reciprocal derivative shell moments

Source candidates:

- Li-Zaharescu, "Value distribution of L'(rho)", Theorem 1.1: lower bound for
  a second negative moment in an automorphic/Selberg-class setting.
- Hung M. Bui, Alexandra Florea, and Micah B. Milinovich, "Negative discrete
  moments of the derivative of the Riemann zeta-function", arXiv:2310.03949,
  Theorem 1.1. Primary: `https://arxiv.org/pdf/2310.03949`.
- Micah B. Milinovich and Nathan Ng, "A note on a conjecture of Gonek",
  arXiv:1106.1160. Primary: `https://arxiv.org/pdf/1106.1160`.

Map:

- These justify the shape of the H1 target
  `J_E,2(T)=sum_{T<|gamma|<=2T}|L'(E,1+i gamma)|^{-2}
  <= C_E T^(3-delta)` for smoothstep `q=2`.
- They do not prove it for fixed EC/GL2. LZ is lower-bound/mollified-template
  direction. BFM is zeta-only and subfamily upper-bound. Milinovich-Ng is
  zeta-only and lower-bound.

Confidence:

- 0.88 that the fixed EC/GL2 shell upper bound remains unsourced.
- 0.80 that this is the cleanest positive-rank H1 hypothesis to name.

Gap:

```text
H1-shell-moment(E,delta):
  sum_{T<|gamma|<=2T}|L'(E,1+i gamma)|^{-2}
  <= C_E T^(3-delta).
```

For smoother kernels with `|W_hat(it)|<<|t|^{-q}`, replace `3-delta` by
`2q-1-delta` for absolute pointwise closure.

### Fixed-weight principal value bounds

Source candidates:

- Li-Zaharescu, "Value distribution of L'(rho)", equations defining mollified
  sums `S0`, `S1`, `S2` and Theorem 4.1.
- BFM zeta negative moment paper as an analogue for rare small derivative
  control, not fixed-weight cancellation.

Map:

- H1 needs direct control of
  `sum W_hat(i gamma) exp(i gamma u)/L'(E,1+i gamma)`.
- LZ studies reciprocal derivatives with Dirichlet-polynomial mollifier
  weights, not the fixed H1 Mellin weight uniformly in `u`.
- Pair correlation or zero spacing can support averaged/profile modes only
  after magnitude input; it is not pointwise PV cancellation.

Confidence:

- 0.86 that no checked source closes fixed-weight H1 PV.

Gap:

```text
H1-fixed-weight-PV(E,W,r):
  legal-height principal values converge to Z_PV(u), and
  sup_{u in [U,2U]} |Z_PV(u)| = O(U^beta), beta<r.
```

Rank zero still needs profile/averaging/filtering unless all nonzero
frequencies are killed.

### EC H2 and Mertens-normalized Euler products

Source candidates:

- Arshay Sheth, "Euler Product Asymptotics for L-functions of Elliptic
  Curves", arXiv:2312.05236, Theorem 3.1, Corollary 3.2, Theorem B/Corollary B.
  Primary: `https://arxiv.org/pdf/2312.05236`.
- Wentang Kuo and M. Ram Murty, "On a Conjecture of Birch and
  Swinnerton-Dyer", Canadian Journal of Mathematics 57 (2005), 328-337,
  Theorems 2 and 3. Primary:
  `https://mast.queensu.ca/~murty/Kuo-Murty-CJM.pdf`.
- Keith Conrad, "Partial Euler Products on the Critical Line", Canadian
  Journal of Mathematics 57 (2005), 267-297, Theorem 1.3 and Theorem 6.3.
  Primary: `https://kconrad.math.uconn.edu/articles/eulerprod.pdf`.
- Friedlander-Iwaniec, Opera de Cribro chapter 1, Lemma 1.1 and Theorem 1.2
  (Mertens' Prime Number Theorem). Primary:
  `https://assets.press.princeton.edu/chapters/s8585.pdf`.

Map:

- Sheth supports EC zero counting and `sum 1/|rho|^2` for pure zero weights,
  plus a sharp BSD product asymptotic outside a set of finite logarithmic
  measure under RH and rank equality. It does not prove pointwise all-large-K
  H2.
- Kuo-Murty and Conrad identify the hard pointwise BSD product with stronger
  prime-power error conditions (`Ctilde(x)=o(x)` / `psi_E(x)=o(x log x)`).
- Friedlander-Iwaniec supports the ordinary prime-harmonic finite part
  `sum_{p<=x}1/p = log log x + C + o(1)`. Weighted smooth transfer is an
  in-repo Abel/Stieltjes lemma.

Confidence:

- 0.84 that H2 should remain conditional or exceptional-set/profile, not
  pointwise sourced.
- 0.90 that the prime-harmonic Mertens piece is source-supported.

Gap:

```text
Pointwise EC H2:
  log P_E,W(K) = -r log log K + B_E,W + o(1)
```

requires exact Agent-3 local factors, S1 branch continuation, Sym2 finite
part, weighted prime-Mertens transfer, and no silent upgrade of Sheth's
exceptional-set theorem.

### Symmetric-square Rankin-Selberg finite parts

Source candidates:

- Stephen Gelbart and Herve Jacquet, "A relation between automorphic
  representations of GL(2) and GL(3)", Annales scientifiques de l'Ecole
  Normale Superieure 11 (1978), 471-542. Primary:
  `https://numdam.org/item/ASENS_1978_4_11_4_471_0/`.
- Jeffrey Hoffstein and Paul Lockhart, "Coefficients of Maass forms and the
  Siegel zero", Annals of Mathematics 140 (1994), 161-181. Primary:
  `https://annals.math.princeton.edu/1994/140-1/p04` and PDF
  `https://www.math.columbia.edu/~goldfeld/CoeffMaassForms.pdf`.
- Iwaniec-Luo-Sarnak, "Low lying zeros of families of L-functions",
  arXiv:math/9901141, Proposition 3/4 context. Primary:
  `https://arxiv.org/abs/math/9901141`.

Map:

- Gelbart-Jacquet is the right automorphy source for the adjoint/symmetric
  square GL3 object.
- Hoffstein-Lockhart supplies adjacent nonvanishing/lower-bound technology for
  adjoint-square values, including holomorphic-form applicability.
- ILS is adjacent explicit-formula/family evidence that prime-linear and
  prime-square/Sym2 terms both occur.

Confidence:

- 0.70 that these are the correct source family for Sym2 finite parts.
- 0.55 that they close the exact repo theorem without more work.

Gap:

The exact needed statement is still not sourced:

```text
Sym2FinitePart(E,W):
  for chi_sym2(p)=a_p^2/p-1 over good primes,
  S_sym,W(K) = -kappa_sym log log K + C_sym,E,W
               + O(1/log K)
```

with ramified local corrections removed, the value/convention of
`kappa_sym=ord_{s=1}L_sym,E^good(s)` stated, and weighted zero/pole branch
summability proved. Adjacent automorphy is not the same as this endpoint
finite-part theorem.

### GL2 simple zeros

Source candidates:

- Alexandre de Faveri, "Simple zeros of GL(2) L-functions", Journal of the
  European Mathematical Society, Theorem 1.1. Primary:
  `https://ems.press/journals/jems/articles/14298254`.
- Andrew R. Booker, "Simple zeros of degree 2 L-functions". Primary:
  `https://people.maths.bris.ac.uk/~maarb/papers/simple.pdf`.

Map:

- Supports "many/power-many simple zeros" for holomorphic GL2 forms.
- Does not prove all offcentral zeros simple, bounded multiplicity, or any
  reciprocal derivative bounds.

Confidence:

- 0.90 for adjacent simplicity evidence.
- 0.96 that it does not close H1.

## Best Theorem Targets

1. `ShiftedPerronNonlocalRemainder(chi,rho)`: GL1-Perron closure. No checked
   source. Must include off-target higher-order residues or all-simple plus
   simple-residue cancellation.

2. `H-height-LZ(E,eta,sigma)`: H1 contour-height input. Likely source-routed
   by Li-Zaharescu Proposition 3.1 after EC normalization/reflection.

3. `H1-shell-moment(E,delta)`: positive-rank H1 reciprocal derivative
   closure. No checked fixed EC/GL2 source.

4. `H1-fixed-weight-PV(E,W,r)`: possible nonabsolute H1 route. No checked
   source; LZ is only a mollifier template.

5. `PointwiseH2(E,W)`: conditional on exact S1, Sym2, Mertens, and bad-prime
   factor finite parts. Sheth is exceptional-set only.

6. `Sym2FinitePart(E,W)`: promising source family is Gelbart-Jacquet plus
   Hoffstein-Lockhart/Jacquet-Shalika-style nonvanishing, but exact good-prime
   endpoint theorem still needs a source packet or in-repo proof.

## Commands / Web Spot Checks

Local commands included `rg` over the handoff/source packets and `sed -n`
reads of the files listed above.

Primary web spot checks:

- Aoki-Koyama ScienceDirect/arXiv pages.
- Inoue JTNB PDF.
- Soundararajan arXiv PDF.
- Li-Zaharescu author PDF.
- Sheth arXiv PDF.
- Kuo-Murty PDF.
- Conrad PDF.
- Friedlander-Iwaniec publisher chapter PDF.
- Gelbart-Jacquet Numdam and author PDF.
- Hoffstein-Lockhart Annals page and author PDF.
- Iwaniec-Luo-Sarnak arXiv page.
- de Faveri EMS page.
- Booker author PDF.
- Bui-Florea-Milinovich arXiv PDF.
- Milinovich-Ng arXiv PDF.
