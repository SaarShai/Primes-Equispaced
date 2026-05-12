---
schema_version: 1
title: "Zero-Sampling Route To Homogeneous BFMT DPMV"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.78
tags: [h1, gl2, ec, bfmt, dpmv, zero-sampling, reciprocal-derivative]
---

# Zero-Sampling Route To Homogeneous BFMT DPMV

Status: `RIGOROUS_REDUCTION`.

No EC smoothing theorem and no H1 theorem is promoted.  However the direct H1
target has a new route that bypasses both Milinovich-Ng obstructions from the
top-10 wave.

## Verdict

The live target

```text
Homogeneous-GL2-BFMT-DPMV(E,k=1/2)
```

should be split again.  The sharp source-backed Milinovich-Ng formula is not
needed for a first homogeneous BFMT replacement.  A cruder zero-sampling large
sieve gives, for every Dirichlet polynomial of length `N<=T`,

```text
sum_{T<gamma<=2T} |A(1/2+i gamma)|^2
  <<_E T (log T)^3 sum_{n<=N} |a_n|^2/n,

A(s)=sum_{n<=N} a_n n^(-s),
```

under the fixed-curve RH/critical-line mode and the standard EC zero count.
This estimate is homogeneous in the actual coefficients.  It therefore does
not care about the `(s_0!)^2` scaling that killed BFMT P2.5 against
Milinovich-Ng Proposition 4.1, and it does not require Milinovich-Ng conditions
(39)/(40), which killed BFMT P2.6.

Continuation update: the finite BFMT substitution audit is now recorded in
`ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` and passes at the visible
BFMT Section 4/5 bookkeeping level.  The remaining work is the final
EC/newform coefficient transcription, not a new Milinovich-Ng-style DPMV
theorem.

The audit target was:

```text
ZeroSample-BFMT-SubstitutionAudit(E,k=1/2):
  replace each use of BFMT Theorem 3.1 in Propositions 2.5, 2.6, and 2.7
  by the zero-sampling bound above, and verify the extra (log T)^O(1)
  factor is absorbed by BFMT's T^delta slack.
```

The source lines inspected here suggested the audit would pass; the follow-up
substitution audit records that pass and should be used for the current state.

## Source Protocol

Workspace:

```bash
/tmp/farey-homogeneous-bfmt-20260511
```

Commands:

```bash
curl -L --fail --max-time 60 -sS -o milinovich_ng_1306_0854.pdf \
  https://arxiv.org/pdf/1306.0854
curl -L --fail --max-time 60 -sS -o sheth_ec_arxiv_2312.05236.pdf \
  https://arxiv.org/pdf/2312.05236
curl -L --fail --max-time 60 -sS -o bfmt_2310_03949.pdf \
  https://arxiv.org/pdf/2310.03949
/tmp/farey-agent03-dpmv-20260511/xpdf-tools-mac-4.06/binARM/pdftotext \
  -layout -enc UTF-8 milinovich_ng_1306_0854.pdf \
  milinovich_ng_1306_0854.txt
/tmp/farey-agent03-dpmv-20260511/xpdf-tools-mac-4.06/binARM/pdftotext \
  -layout -enc UTF-8 sheth_ec_arxiv_2312.05236.pdf \
  sheth_ec_arxiv_2312.05236.txt
/tmp/farey-agent03-dpmv-20260511/xpdf-tools-mac-4.06/binARM/pdftotext \
  -layout -enc UTF-8 bfmt_2310_03949.pdf bfmt_2310_03949.txt
shasum -a 256 *.pdf
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_2310_03949.pdf
7429a8705e1d7e790a925bd7a410338a52e24ab060e890bdb13f9b8780810f10  milinovich_ng_1306_0854.pdf
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_arxiv_2312.05236.pdf
```

Checked anchors:

- Sheth, arXiv:2312.05236, PDF p. 13, Theorem 3.1: `N_E(t)` is
  `alpha_E t(log t+c)/pi + O(log t)`.
- Same source, PDF p. 13: "number of terms" in a unit zero-ordinate interval
  is `<< log t`.
- Milinovich-Ng, arXiv:1306.0854, PDF p. 19: their Lemma 4.1 states
  Montgomery-Vaughan's mean-value theorem for Dirichlet polynomials.
- BFMT, arXiv:2310.03949, PDF p. 8, Theorem 3.1: zeta zero mean value for
  "any sequence of complex numbers".
- BFMT, PDF p. 11: "Using Theorem 3.1" starts the proof of Propositions
  2.5, 2.6, and 2.7.
- BFMT, PDF p. 18, equation (5.14): final bound is `<< T^(1+delta)`.

## Lemma: Homogeneous Zero-Sampling Bound

Let `E/Q` be fixed.  Assume all zeros being sampled are on the critical line
in the normalized variable.  Let

```text
A(s)=sum_{n<=N} a_n n^(-s),       N<=T,       T>=3.
```

Define

```text
D(A)=sum_{n<=N} |a_n|^2/n.
```

Then

```text
sum_{T<gamma<=2T} |A(1/2+i gamma)|^2
  <<_E T (log T)^3 D(A).
```

The sum is over the ordinates of nontrivial zeros of `L(E,s)` in the normalized
critical-line mode.

### Proof

Partition `[T,2T]` into unit intervals `I_m=[m,m+1]`, and let
`J_m=[m-1,m+2]`.  The source zero count gives

```text
# {gamma in I_m} <<_E log T.
```

For `F(t)=A(1/2+it)`, the one-dimensional Sobolev inequality on `J_m` gives

```text
sup_{t in I_m} |F(t)|^2
  << int_{J_m} ( |F(t)|^2 + |F'(t)|^2 ) dt.
```

Hence, by bounded overlap of the `J_m`,

```text
sum_{T<gamma<=2T} |A(1/2+i gamma)|^2
  <<_E log T
      int_{T-1}^{2T+2} ( |F(t)|^2 + |F'(t)|^2 ) dt.
```

Apply Montgomery-Vaughan to

```text
F(t)=sum_{n<=N} (a_n n^(-1/2)) n^(-it)
```

and to

```text
F'(t)=sum_{n<=N} (-i log n) (a_n n^(-1/2)) n^(-it).
```

Since `N<=T`,

```text
int |F(t)|^2 dt
  << T D(A),

int |F'(t)|^2 dt
  << T (log T)^2 D(A).
```

Substitution gives the stated `T(logT)^3 D(A)` bound.

This proof is intentionally crude.  It uses no Landau-Gonek formula, no
Milinovich-Ng coefficient hypotheses, and no off-diagonal sign information.

## Why This Bypasses The Top-10 Obstructions

### P2.5 factorial scaling

Top-10 Agent 01 killed the direct Milinovich-Ng route because BFMT writes

```text
P_{0,v}(gamma)^(s_0) = s_0! A_v(1/2+1/logT+i gamma),
```

and Milinovich-Ng Proposition 4.1 has a nonhomogeneous
`T(logT)^(4-2eta)` error.  Multiplying by `(s_0!)^2` made that error too
large.

The zero-sampling bound has no coefficient-free additive error.  Applying it
directly to the actual scaled coefficients gives exactly

```text
T(logT)^3 * sum |a_BFMT(n)|^2/n.
```

The factorials appear only inside the natural `l2` norm, which is precisely
how BFMT's combinatorial estimates already handle them.

### P2.6 coefficient condition failure

Top-10 Agent 02 killed the Milinovich-Ng route because BFMT P2.6 mixed
terminal coefficients violate condition (40).  The zero-sampling bound has no
conditions (39)/(40).  It is an arbitrary-coefficient estimate, like the upper
bound part of BFMT Theorem 3.1, but with an extra polylogarithmic factor.

### Support wall

Milinovich-Ng Proposition 4.3 has the `T^(2/3)` support wall.  The
zero-sampling bound only requires

```text
N<=T.
```

BFMT Propositions 2.5, 2.6, and 2.7 impose support below

```text
T^(1-loglogT/logT) = T/logT,
```

so this route reaches the needed support range.

## Follow-Up Audit Result

The follow-up substitution audit states:

```text
ZeroSample-Homogeneous-GL2-BFMT-DPMV(E,k=1/2):
  Under fixed EC RH/critical-line normalization and finite ramified-prime
  removal, BFMT Propositions 2.5, 2.6, and 2.7 remain valid with their
  right sides multiplied by at most (log T)^C.
```

The audit passes for the printed BFMT Proposition 2.5, 2.6, 2.7, and Section
5 bookkeeping. This is enough for the coefficient-DPMV part of the
separated-zero H1 branch because BFMT's final negative-moment target is
`T^(1+delta)` and a fixed power of `log T` is absorbed by reducing `delta`.

The remaining exact work is:

```text
BFMT-EC-Transcription(E,k=1/2):
  write the GL2 logarithmic approximation and coefficient families with
  lambda_f factors, insert the zero-sampling propositions, and verify the
  final separated negative first derivative moment.
```

## Boundary

This packet does not prove:

```text
R_E,1(T)=o(T^2);
EC-BFMT-BadSetBudget(E,c);
H1 finite-box closure;
multiple-zero Laurent control;
H2 S1/Sym2 closure;
GL1 sharp Perron-leading.
```

If the substitution audit passes, it closes only the separated simple-zero
coefficient-DPMV input.  The bad-set and multiple-zero H1 inputs remain
independent.

No Koyama correspondence or email drafts were read or edited.
