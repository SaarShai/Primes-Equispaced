---
schema_version: 1
title: "H2/Sym2 source closure for H1 pairing"
date: 2026-05-11
type: closure-packet
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.79
dependencies:
  - handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md
  - handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_RECIPROCAL_PERRON_SYNTHESIS_2026-05-11.md
tags: [ec-ndc, h2, sym2, s1, source-closure, h1-pairing]
---

# H2/Sym2 Source Closure For H1 Pairing

Status: `RIGOROUS_REDUCTION`

Confidence: `0.79`

Dependencies: exact Agent 3 local factors; analytic rank
`r=ord_{s=1}L(E,s)`; fixed admissible endpoint-smoothed kernel `W`;
S1 branch-only continuation; source-verified EC zero counting; exact
good-prime Sym2 finite-part theorem or explicit Sym2 branch hypothesis; H1
reciprocal-pole theorem in the same theorem mode.

## Do Not Promote Unless

- H2 uses exactly: good `1-a_p/p+1/p`, bad `1-a_p/p`.
- `S_1,W`, `S_sym,W`, `M_good,W`, `R_ge3,W`, and `B_bad,E` are all present.
- S1 branch-only continuation is proved for the endpoint kernel, not inferred
  from zero summability.
- `S_sym,W` is proved for `chi_sym2(p)=a_p^2/p-1` in the good-prime
  normalization, or its branch sum is retained explicitly.
- `kappa_sym=0` is not inserted unless it is verified for this exact object.
- H1 is closed separately as reciprocal-pole calculus; no H2 `1/log K`
  branch damping is imported into H1.
- The final theorem mode is declared once: pointwise, oscillatory, or averaged.
- Rank zero is separated.
- Any new external theorem has `curl + pdftotext + SHA/page/equation + short
  quote`, matching `SOURCE_PACKET.md`.

## Verdict

No H2 theorem is promoted.

The H2/Sym2 side is reduced to a precise conditional theorem package. Local
Agent 3 bookkeeping is closed. Pure EC zero summability for the S1 branch is
source-supported through the existing source packet. The remaining H2-side
blocks are:

1. branch-only continuation and contour tails for the exact endpoint-smoothed
   `S_1,W`;
2. exact Sym2 finite-part theorem for
   `chi_sym2(p)=a_p^2/p-1`, including Sym2 zero/pole summability;
3. source-verified value or convention-preserving retention of `kappa_sym`.

Thus the correct handoff to H1 is a rigorous reduction, not a closed proof.

## Exact H2 Algebra

For Agent 3,

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)),

A_p(1) = 1 - a_p/p + 1/p    if p is good,
A_p(1) = 1 - a_p/p          if p is bad.
```

At a good prime define

```text
lambda_p = a_p/sqrt(p),
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Then

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E,W(K),
```

where

```text
S_1,W(K)    = sum_{p good} W(p/K) a_p/p,
S_sym,W(K) = sum_{p good} W(p/K) chi_sym2(p)/p,
M_good,W(K)= sum_{p good} W(p/K)/p,
B_bad,E,W(K)= -sum_{p bad} W(p/K) log(1-a_p/p).
```

The remainder `R_ge3,W` is the absolutely convergent good-prime local tail
after subtracting

```text
a_p/p + (a_p^2-2p)/(2p^2)
 = a_p/p + (1/2)chi_sym2(p)/p - 1/(2p).
```

This identity is the non-negotiable H2 local closure. Dropping the
Sym2 or harmonic term gives the wrong coefficient.

## S1 Branch Continuation

Conditional branch formula:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + Z_1,E,W(log K)/log K
   + O((log K)^(-2)) + O(K^(-eta)).
```

For a noncolliding zero `rho=1+i gamma` of `L(E,s)` with multiplicity
`m_gamma`,

```text
contribution = -m_gamma K^(i gamma) W_hat(i gamma)/log K
               + O_gamma,W((log K)^(-2)).
```

This is a proof candidate once the branch-contour hypothesis is proved:
`A_E(z)=sum_{p good}a_p p^(-1-z)` must continue in the shifted strip with
logarithmic branches only, no offcentral poles on `Re z>=0`, and integrable
shifted-line/horizontal remainders. The existing literature packet does not
source this exact endpoint-smoothed fixed-curve theorem.

## Zero Summability

The S1 pure multiplicity zero sum is closed under the existing source packet
plus the smoothstep Mellin decay:

```text
N_E(T) = O_E(T log T),
W_hat(i gamma), W_hat'(i gamma-v) = O_W((1+|gamma|)^(-2)).
```

Dyadic summation gives

```text
sum_{gamma != 0} |m_gamma W_hat(i gamma)| < infinity,
sum_gamma m_gamma sup_{0<=v<=eta}
  (|W_hat(i gamma-v)|+|W_hat'(i gamma-v)|) < infinity.
```

This proves that the S1 offcentral branch aggregate is `O(1/log K)` if the
branch formula is valid. It does not prove branch continuation, Sym2 zero
summability, or H1 reciprocal-residue summability.

## Sym2 Finite-Part Reduction

Use the exact good-prime object

```text
L_sym,E^good(s)
 = product_{p good}
   (1-u_p^2 p^(-s))^(-1)
   (1-p^(-s))^(-1)
   (1-v_p^2 p^(-s))^(-1),
```

with `u_p v_p=1`, `u_p+v_p=lambda_p`. Its first prime coefficient is exactly

```text
u_p^2 + 1 + v_p^2 = lambda_p^2 - 1 = a_p^2/p - 1.
```

Set

```text
D_sym,E(s) = sum_{p good} chi_sym2(p) p^(-s),
kappa_sym = ord_{s=1} L_sym,E^good(s),
```

with positive `kappa_sym` for a zero and negative `kappa_sym` for a pole.
If

```text
log L_sym,E^good(s)
 = kappa_sym log(s-1) + log L_sym,E^*(1) + o(1)
```

and the higher-prime-power correction is finite at `s=1`, then

```text
S_sym,W(K)
 = -kappa_sym log log K
   + C_sym,E
   - (1/log K) sum_{rho != 1}
       m_rho K^(rho-1) W_hat(rho-1)
   + lower terms.
```

A pointwise finite part follows if the Sym2 zero/pole branch sum is finite and
has no uncancelled `Re(rho)>1` term. The source packet verifies only adjacent
Sym2 automorphic facts; it does not prove this exact good-prime finite-part
theorem or the needed Sym2 zero summability. Therefore the Sym2 analytic input
remains source/proof-blocked.

## Kappa Convention

The convention is closed:

```text
kappa_sym = ord_{s=1} L_sym,E^good(s).
positive: zero at s=1
zero: finite nonzero value at s=1
negative: pole at s=1
```

H2 does not need the numeric value of `kappa_sym` for the coefficient if S1
and Sym2 use the same convention:

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

But any claim `S_sym,W(K)=C+o(1)` does need `kappa_sym=0`. That value is not
source-closed in the current packet for the exact good-prime normalization.

## Pairing With H1

H2 can pair with the H1 residue-control wave only in matched theorem mode.
Pointwise positive-rank composition needs:

```text
H2: log P_E,W(K) = -r log log K + B_E,W + o(1),
H1: c_E,W(e^u) = Q_r(u) + o(u^r),  u=log K, r>=1.
```

Rank zero needs the stronger H1 condition `Z_c(u)=o(1)`, or else the final
theorem must retain the H1 oscillatory profile or average the product itself.
H2 branch damping does not help H1 reciprocal poles:

```text
H2/S1 zero: logarithmic branch -> K^(i gamma) W_hat(i gamma)/log K.
H1 zero: reciprocal pole -> K^(i gamma) W_hat(i gamma)/L'(1+i gamma).
```

## Citation Ledger

No new external theorem is introduced here. External facts are used only
through `handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md`, which
records the required fetch/extraction hashes and short anchors.

- Sheth, arXiv:2312.05236, PDF p. 13, Theorem 3.1 anchor "number of zeros";
  Corollary 3.2 anchor "converges". Use: EC zero counting and reciprocal-square
  pure multiplicity summability only.
- Friedlander-Iwaniec chapter PDF, PDF p. 17, Theorem 1.2 anchor "Mertens'
  Prime Number Theorem". Use: ordinary unweighted prime-Mertens; weighted
  smoothstep transfer remains in-repo.
- Iwaniec-Luo-Sarnak, arXiv:math/9901141, PDF p. 11 anchor "Euler product of
  degree 3 is entire". Use: adjacent Sym2/GL(3) context only, not the exact
  `S_sym,W` theorem.
- Hoffstein-Lockhart, Annals 140 (1994), PDF p. 3 anchor "adjoint square
  lift". Use: adjacent adjoint/Sym2 context only, not `kappa_sym=0`.

## Final Classification

H2/Sym2 is ready to pair with H1 only as a conditional reduction:

```text
Exact local H2 algebra: closed.
S1 zero summability: source-supported for pure L(E) zeros.
S1 branch continuation: proof candidate, not source-closed.
Sym2 finite part: rigorous reduction, exact theorem source/proof-blocked.
kappa_sym convention: closed; value not source-closed.
H1 pairing: compatible only after separate H1 reciprocal-pole control.
```

