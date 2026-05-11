---
schema_version: 1
title: "Agent 04 H2/Sym2 endpoint closure"
date: 2026-05-11
agent: "Agent 04 - EC H2/Sym2 Endpoint Closure"
type: handoff
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.82
tags: [ec-ndc, h2, sym2, s1, endpoint, mertens, source-checked]
---

# Agent 04 H2/Sym2 Endpoint Closure

## Status Enum

- `CLOSED`: proved here or source-checked plus elementary transfer.
- `CONDITIONAL`: theorem-level algebra proved from displayed hypotheses.
- `OPEN`: exact proof/source still missing.
- `BLOCKED`: missing input prevents theorem promotion.
- `NOT_PROMOTED`: do not cite as an unconditional EC theorem.

Overall status: `RIGOROUS_REDUCTION`, `NOT_PROMOTED`.

No unconditional fixed-curve endpoint H2 theorem is source-closed here. The
normalization is now single-valued, weighted good-prime Mertens closes, and the
pure S1 zero-sum closes. The remaining blockers are exactly S1 branch-contour
legality and exact good-prime Sym2 finite-part/zero-sum closure.

## Single Normalization

Fix an elliptic curve `E/Q` and analytic rank only:

```text
r = ord_{s=1} L(E,s).
```

Use Agent 3 local factors:

```text
A_p(1) = 1 - a_p/p + 1/p    good p
A_p(1) = 1 - a_p/p          bad p
P_E,W(K) = product_p A_p(1)^(-W(p/K)).
```

Endpoint kernel used below: compact support in `[0,1]`, `W=1` on `[0,alpha]`
for some `alpha>0`, `W(1)=0`, Mellin transform `W_hat(z)=1/z+O(1)` at zero,
and vertical decay `W_hat,W_hat' = O((1+|t|)^(-2))` on the shifted strips used
by the branch cuts.

At good primes:

```text
lambda_p = a_p/sqrt(p),
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Define:

```text
S_1,W(K)     = sum_{p good} W(p/K) a_p/p,
S_sym,W(K)   = sum_{p good} W(p/K) chi_sym2(p)/p,
M_good,W(K)  = sum_{p good} W(p/K)/p,
B_bad,W(K)   = -sum_{p bad} W(p/K) log(1-a_p/p).
```

The Sym2 central order convention is:

```text
kappa_sym = ord_{s=1} L_sym,E^good(s)
```

positive for a zero, zero for finite nonzero value, negative for a pole. Do
not set `kappa_sym=0` unless this exact good-prime object is reconciled with a
source-verified global adjoint/Sym2 object.

## Claim Table

| Item | Status | Result |
|---|---:|---|
| Exact H2 local algebra | `CLOSED` | Decomposition below is exact for Agent 3 factors. |
| Higher good-prime tail `R_ge3,W` | `CLOSED` | Absolute convergence by Hasse after subtracting degree 1 and 2 terms. |
| Bad-prime term | `CLOSED` | Finite constant, same real branch. |
| Weighted good-prime Mertens | `CLOSED` | Plateau `W` transfers ordinary Mertens with only finite bad-prime subtraction. |
| S1 pure zero-summability | `CLOSED` | Source-checked EC zero count plus Mellin decay gives absolute branch-weight summability. |
| S1 branch continuation/contour shift | `OPEN`, `BLOCKED` | Zero-sum estimate does not prove branch-only continuation or horizontal/left-edge bounds. |
| Exact good-prime `S_sym,W` finite part | `CONDITIONAL`, `BLOCKED` | Formula is fixed below; exact source/proof for good-prime Sym2 continuation, local reconciliation, and zero-sum remains missing. |
| Pointwise H2 endpoint | `CONDITIONAL`, `NOT_PROMOTED` | Follows from the displayed S1/Sym2 hypotheses and closed Mertens/tails. |

## Closed Local H2 Algebra

For good primes,

```text
-log(1-a_p/p+1/p)
 = a_p/p + (1/2)chi_sym2(p)/p - 1/(2p) + R_p,
R_p = O(p^(-3/2)).
```

Therefore

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,W(K),
```

where `R_ge3,W(K)=sum_{p good} W(p/K)R_p = C_ge3,E+o(1)`.

This is the only unconditional H2 theorem-level statement in this handoff.

## Closed Weighted Good-Prime Mertens

External input, source-checked: ordinary Mertens

```text
sum_{p<=x} 1/p = log log x + C_M + o(1).
```

For the plateau endpoint kernel,

```text
sum_p W(p/K)/p
 = sum_{p<=K} 1/p
   + sum_{alpha K < p <= K} (W(p/K)-1)/p.
```

The transition error satisfies

```text
sum_{alpha K < p <= K} 1/p
 = log log K - log log(alpha K) + o(1)
 = O(1/log K) + o(1).
```

Thus

```text
sum_p W(p/K)/p = log log K + C_M + o(1).
```

Removing finitely many bad primes gives the exact good-prime version:

```text
M_good,W(K)
 = log log K + C_M,E^good + o(1),
C_M,E^good = C_M - sum_{p bad} 1/p.
```

No H2 theorem should carry a hidden `W`-dependent Mertens constant for this
plateau endpoint class.

## Closed S1 Zero-Summability, Not Branch Continuation

Source-checked EC zero counting gives, for nontrivial zeros counted with
multiplicity,

```text
N_E(T) = O_E(T log T).
```

With the endpoint Mellin decay,

```text
|W_hat(i gamma)| + sup_{0<=v<=eta}|W_hat'(i gamma-v)|
  <<_W (1+|gamma|)^(-2).
```

Dyadic summation gives

```text
sum_{gamma != 0} |m_gamma W_hat(i gamma)| < infinity,
sum_gamma m_gamma sup_{0<=v<=eta}
  (|W_hat(i gamma-v)| + |W_hat'(i gamma-v)|) < infinity.
```

Therefore, if the S1 branch-contour theorem is valid, noncentral zeros on
`Re rho=1` contribute only

```text
-(1/log K) sum_{gamma != 0}
  m_gamma K^(i gamma) W_hat(i gamma)
  + O((log K)^(-2)),
```

which is `O(1/log K)`. This closes only the summability estimate. It does not
prove that `A_E(z)=sum_{p good}a_p p^(-1-z)` has branch-only continuation, no
offcentral poles, or legal shifted contours.

## S1 Branch Continuation Dependency

The needed S1 theorem remains:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + o(1).
```

The branch theorem candidate proves this from these still-open inputs:

```text
1. Mellin inversion for S_1,W with the chosen W.
2. Branch-only continuation of A_E(z) in Re z >= -eta.
3. No offcentral poles on Re z >= 0.
4. Legal infinite cut contour shift.
5. Horizontal and left-edge bounds after cuts are removed.
```

The central coefficient is not `-r`; it is

```text
1/2 + kappa_sym/2 - r.
```

The `+1/2` is the prime-harmonic term, and `+kappa_sym/2` is the Sym2
bookkeeping term. H2 recovers slope `-r` only after adding `(1/2)S_sym,W` and
subtracting `(1/2)M_good,W`.

## Exact Good-Prime Sym2 Finite-Part Dependency

Use exactly

```text
L_sym,E^good(s)
 = product_{p good}
   (1-u_p^2 p^(-s))^(-1)
   (1-p^(-s))^(-1)
   (1-v_p^2 p^(-s))^(-1),
u_pv_p=1,
u_p+v_p=lambda_p.
```

Then its first prime coefficient is exactly `chi_sym2(p)`. Let

```text
D_sym,E(s) = sum_{p good} chi_sym2(p)p^(-s).
```

If the exact good-prime Sym2 package supplies

```text
log L_sym,E^good(s)
 = kappa_sym log(s-1) + log L_sym,E^*(1) + o(1),
```

and the higher-prime-power correction is finite at `s=1`, then Mellin
inversion gives the central finite part

```text
S_sym,W(K)
 = -kappa_sym log log K
   + C_sym,E
   + Z_sym,E,W(K)
   + o(1).
```

Offcentral logarithmic singularities would contribute

```text
Z_sym,E,W(K)
 = -(1/log K) sum_{rho != 1}
     m_rho K^(rho-1) W_hat(rho-1)
   + lower terms.
```

A pointwise finite part follows if the weighted Sym2 zero/pole branch sum is
finite and no uncancelled singularity has `Re rho > 1`. This is not
source-closed in the exact good-prime normalization.

What the fresh sources support only adjacently:

```text
global adjoint/Sym2 objects exist and are the right objects;
the exact Agent 3 good-prime finite part still needs local-factor
reconciliation and Sym2 zero/pole summability in the same shifted strip.
```

Consequently:

```text
S_sym,W(K)=C+o(1)
```

is not promotable unless `kappa_sym=0` is source-verified for
`L_sym,E^good` or proved in-repo with all ramified/local corrections removed.

## Conditional H2 Endpoint Theorem

Assume the closed local algebra, closed weighted Mertens, closed tails/bad
primes, and the two open analytic packages:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W + o(1),

S_sym,W(K)
 = -kappa_sym log log K
   + C_sym,E + o(1).
```

Then

```text
log P_E,W(K)
 = -r log log K + B_H2(E,W) + o(1),
```

with

```text
B_H2(E,W)
 = C_1,E,W
   + (1/2)C_sym,E
   - (1/2)C_M,E^good
   + C_ge3,E
   + B_bad,E.
```

Coefficient check:

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

Equivalently,

```text
P_E,W(K) = exp(B_H2(E,W)) (log K)^(-r)(1+o(1)).
```

This is a conditional reduction, not an unconditional EC endpoint theorem.

If either S1 or Sym2 keeps an explicit branch profile, the honest statement is

```text
log P_E,W(K)
 = -r log log K + B_H2(E,W)
   + Z_1,E,W(log K)/log K
   + (1/2)Z_sym,E,W(log K)/log K
   + o(1).
```

Do not mix this pointwise mode with H1 reciprocal Perron. H2 branch damping
does not control H1 reciprocal residues.

## Source Checks

Fresh source run directory:

```text
/tmp/agent04-h2sym2-source-20260511
```

Commands used:

```text
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -layout SOURCE.pdf SOURCE.txt
shasum -a 256 *.pdf
```

SHA256:

```text
080fbff5d5f122678cddd78a1b0561a79952c5fe72b49cf2fbc6b014edc0e8dc  friedlander_iwaniec_opera_ch1.pdf
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_arxiv_2312.05236.pdf
5072c63324c329250f70c4ef4e2648a0e8ff465d6b9c241c3d3646d4c6759997  ils_math_9901141.pdf
031de26f73977602225ec96b2207f3070cfc7d6b3cfc2371faed52ee254fb632  hoffstein_lockhart_maass_siegel.pdf
```

Verified external anchors:

- Friedlander-Iwaniec chapter PDF, PDF p. 17, Theorem 1.2/equation (1.4.17).
  Quote: "Mertens' Prime Number Theorem". Used only for ordinary unweighted
  `sum_{p<=x}1/p = log log x + C + o(1)`.
- Sheth, arXiv:2312.05236, PDF p. 13, Theorem 3.1 and Corollary 3.2.
  Quotes: "number of zeros"; "converges". Used only for EC zero counting and
  the pure multiplicity reciprocal-square zero sum.
- Iwaniec-Luo-Sarnak, arXiv:math/9901141, PDF p. 11, equations (13)-(15).
  Quote: "Euler product of degree 3 is entire". Used as adjacent Sym2 context,
  not as the exact Agent 3 `S_sym,W` finite-part theorem.
- Hoffstein-Lockhart, Annals 140 (1994), PDF pp. 3-5, equations (0.6)-(0.8).
  Quote: "adjoint square lift". Used as adjacent adjoint context, not to set
  `kappa_sym=0` for `L_sym,E^good`.

No Kuo-Murty, Conrad, Koyama correspondence, email draft, or numerical
finite-window diagnostic is used as a load-bearing theorem here.

## Remaining Dependencies

1. Prove or source-check the S1 branch-only continuation of
   `A_E(z)=sum_{p good}a_p p^(-1-z)` in the endpoint Mellin strip.
2. Prove legal S1 infinite-cut contour shift, including horizontal and
   left-edge bounds.
3. Reconcile global adjoint/Sym2 local factors with
   `L_sym,E^good`, proving finite nonzero bad-local correction at `s=1`.
4. Prove or source-check the exact `S_sym,W` finite-part theorem for
   `chi_sym2(p)=a_p^2/p-1`.
5. Prove Sym2 zero/pole counting and weighted branch summability in the same
   shifted strip, or retain `Z_sym,E,W/log K`.
6. Prove `kappa_sym=0` only if the exact good-prime object is verified; H2
   slope does not require its numeric value, but `S_sym,W=C+o(1)` does.
7. Keep H1 reciprocal Perron separate. Do not import H2 branch damping into H1.

## Verification Notes

Read scope:

```text
start.md
token-economy.yaml
L0_rules.md
L1_index.md
primes-equispaced/L1_index.md
handoff-2026-05-11-all-in-wave/H2_SYM2_ENDPOINT_PACKET_2026-05-11.md
handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md
handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
handoff-2026-05-11-h1-residue-control-wave/H2_SYM2_SOURCE_CLOSURE.md
```

Commands included `./te doctor`, `rg --files`, `rg -n`, `wc -l`, `sed -n`,
`curl`, `pdftotext`, and `shasum -a 256`.

No broad archive sweep was performed. The two extra files read were direct
dependencies named by the H2 endpoint packet and relevant to the requested
zero/Sym2 closure.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT04_H2_SYM2_ENDPOINT_CLOSURE_2026-05-11.md
```
