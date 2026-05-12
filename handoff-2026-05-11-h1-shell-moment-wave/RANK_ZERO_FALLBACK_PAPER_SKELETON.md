---
schema_version: 1
title: "Rank-zero fallback paper skeleton"
date: 2026-05-11
type: paper-skeleton
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.82
dependencies:
  - handoff-2026-05-11-h1-breakthrough-proof-wave/RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/KERNEL_FILTER_DIAGNOSTIC_IMPLEMENTATION.md
tags: [ec-ndc, h1, rank-zero, product-average, fallback]
---

# Rank-Zero Fallback Paper Skeleton

Status: RIGOROUS_REDUCTION.

Confidence: 0.82.

Dependencies:

- `handoff-2026-05-11-h1-breakthrough-proof-wave/RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/KERNEL_FILTER_DIAGNOSTIC_IMPLEMENTATION.md`
- downstream local dependencies named inside `RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md`.

External theorem citations: none. This skeleton uses local reduction packets
only. Any future external theorem citation must include the repository source
packet: `curl + pdftotext + short verbatim quote + page/equation`.

## Do Not Promote Unless

- The section is explicitly framed as a fallback if the shell moment bound
  and reciprocal strip bounds remain open.
- Rank-zero H1 is stated as an oscillatory profile
  `Q_0 + Z_c(u) + o(1)`, not as a pointwise constant limit.
- Pointwise H1 profile mode and arithmetic product-average mode remain
  separate theorem modes.
- Every H1 contour shift, height-avoidance, indentation, and tail estimate is
  proved for the exact same fixed kernel and Mellin normalization.
- The reciprocal-zero profile has a declared convergence mode: uniform
  convergence of symmetric truncations, absolute tail control, or an explicit
  average-compatible replacement.
- Every offcentral multiple zero is ruled out, killed, retained as an explicit
  polynomial-exponential term, or moved to a renormalized theorem. In rank
  zero, any surviving positive-degree term blocks a bounded profile.
- Product averaging is the arithmetic dyadic log average of
  `c_E,W(e^u) P_E,W(e^u)`, not an averaged log, logarithmic derivative, or
  geometric mean statement.
- The product-average constant includes the H1/H2 diagonal terms
  `q_0 d_0 + sum_gamma a_gamma d_(-gamma)`, not only the central term.
- Kernel filtering is described only as a finite signed-kernel diagnostic
  unless tail residues and kernel admissibility are proved separately.
- No EC smoothing theorem, positive-rank theorem, or fixed-kernel H1 bound is
  claimed from this section.

## Purpose

This section is the claim-safe fallback for the H1 shell-moment wave. If the
fixed-kernel shell moment

```text
J_E,2(T)=sum_{T<|gamma|<=2T}|L'(E,1+i gamma)|^(-2)
```

and the reciprocal strip hypotheses `H-height/H-left` remain open, the paper
can still state a rank-zero conditional section with two guarded outputs:

```text
pointwise mode:
  rank-zero H1 = central term + offcentral oscillatory profile + error;

product-average mode:
  arithmetic dyadic average of H1 times H2 = diagonal constant.
```

This does not close the EC smoothing theorem. It records the exact safe
fallback theorem architecture.

## Paper Section Placement

Suggested title:

```text
Rank-Zero Residues and Product Averages
```

Place after the H1 reciprocal Perron/contour setup and before any attempted
H1/H2 composition theorem.

Subsections:

1. Fixed-kernel H1 normalization.
2. Rank-zero central residue.
3. Offcentral reciprocal residues and the oscillatory profile.
4. No pointwise constant without coefficient death.
5. Dyadic product averaging.
6. H2 product-form input and finite-part bookkeeping.
7. Diagonal extraction theorem.
8. Diagnostics and non-promotion rules.

## Normalization Block

Fix an elliptic curve `E/Q`, an admissible smoothing kernel `W`, and

```text
u = log K.
```

Use the H1 normalization

```text
c_E,W(K)
 = (1/(2 pi i)) int_(Re z=sigma)
     K^z W_hat(z) / L(E,1+z) dz.
```

Rank-zero assumptions:

```text
ord_(s=1) L(E,s) = 0,
L(E,1) != 0,
W_hat(z) = w_(-1)/z + holomorphic at z=0.
```

Repository-normalized kernels have `w_(-1)=1`.

Central residue:

```text
Q_0
 = Res_(z=0) e^(uz) W_hat(z)/L(E,1+z)
 = w_(-1)/L(E,1).
```

## Theorem A: Rank-Zero Oscillatory H1 Profile

Working theorem statement for the paper:

```text
Theorem A.
Let E/Q have analytic rank zero. Fix an admissible W in the H1 Mellin
normalization above. Assume:

(A1) finite-height H1 contour shift:
     c_E,W(e^u)=Q_0+Z_T(u)+I_T(u)
     along legal truncation heights T;

(A2) offcentral zero accounting:
     every offcentral reciprocal pole is simple and included in Z_T,
     or else is killed, cancelled, or retained separately as an explicit
     polynomial-exponential term;

(A3) reciprocal-zero profile convergence:
     the symmetric truncations of the simple-zero sum converge uniformly,
     or a stronger explicit tail bound is available;

(A4) contour/profile tail:
     there are legal T(u)->infinity with |I_T(u)| plus the reciprocal-zero
     tail tending to 0.

Then

c_E,W(e^u)
 = w_(-1)/L(E,1)
   + sum_(gamma != 0)
       W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)
   + o(1),

with the sum interpreted in the declared convergence mode.
```

For normalized kernels:

```text
c_E,W(e^u) = 1/L(E,1) + Z_c(u) + o(1).
```

Required paper wording:

```text
This is a pointwise oscillatory profile theorem. It is not a pointwise
constant-limit theorem.
```

## Multiple-Zero Variant

If an offcentral zero

```text
rho = 1+i gamma
```

has multiplicity `m`, the residue contributes

```text
e^(i gamma u) P_rho(u),     deg P_rho <= m-1.
```

Rank-zero rule:

```text
deg P_rho >= 1 and P_rho != 0
  => unbounded oscillatory-polynomial term;
  => no bounded unrenormalized H1 profile.
```

Therefore the paper theorem must either assume these terms absent/killed, or
state a broader retained-profile theorem:

```text
c_E,W(e^u)
 = Q_0
   + sum_gamma e^(i gamma u)P_rho(u)
   + o(1).
```

Do not hide a polynomial-exponential term in `o(1)`.

## Lemma B: No Constant Limit Without Coefficient Death

Working lemma statement:

```text
Lemma B.
Let

Z_c(u)=sum_(gamma != 0) a_gamma e^(i gamma u)

converge uniformly in symmetric truncations. If

Q_0 + Z_c(u)

has a pointwise limit as u->infinity, then every retained nonzero-frequency
coefficient a_gamma is zero.
```

Proof skeleton:

```text
a_lambda
 = lim_(U->infinity) (1/U) int_0^U Z_c(u)e^(-i lambda u) du.
```

If `Z_c(u)` converges to `0`, the right side is `0`. Thus any nonzero residue
coefficient forces persistent main-scale oscillation.

Paper use:

```text
This lemma is the guardrail preventing the sentence
"rank-zero smoothing tends to 1/L(E,1)" unless all nonzero frequencies are
proved dead by a separate mechanism.
```

## Product-Average Setup

Use dyadic logarithmic arithmetic averaging:

```text
A_U(F) = (1/U) int_U^(2U) F(u) du
       = (1/U) int_exp(U)^exp(2U) F(log K) dK/K.
```

Target:

```text
A_U(c_E,W(e^u) P_E,W(e^u)).
```

Not the target:

```text
exp(A_U(log(c_E,W(e^u)P_E,W(e^u)))).
```

H1 mean-scale notation:

```text
H_c(u)=q_0 + sum_(gamma != 0) a_gamma e^(i gamma u),
q_0 = w_(-1)/L(E,1),
a_gamma = W_hat(i gamma)/L'(E,1+i gamma)
```

in the simple-zero profile case.

H2 input, imported as bookkeeping:

```text
P_E,W(e^u)=exp(B_H2(E,W)) G(u)(1+eps_P(u)),
G(u)=exp(Z_P(u)).
```

Mean coefficients are coefficients of `G`, not of `Z_P`:

```text
d_eta = Mean_dyadic(G(u)e^(-i eta u)).
```

## Theorem C: Rank-Zero Product Arithmetic Average

Working theorem statement for the paper:

```text
Theorem C.
Assume Theorem A in average-compatible form. Assume further:

(C1) H2 product form:
     P_E,W(e^u)=exp(B_H2(E,W))G(u)(1+eps_P(u));

(C2) H2 mean coefficients:
     G has dyadic mean coefficients d_eta;

(C3) joint-tail extraction:
     finite exponential truncations of H_c and G approximate the product
     in dyadic mean strongly enough to pass zero-frequency extraction to
     the infinite profile;

(C4) product errors:
     H1 contour/profile errors and eps_P are small after multiplication
     by the corresponding product factors in dyadic mean;

(C5) no growing H1 term:
     no unrenormalized positive-degree offcentral multiple-zero term survives.

Then

A_U(c_E,W(e^u)P_E,W(e^u))
 -> C_E,W^prod,

where

C_E,W^prod
 = exp(B_H2(E,W))
   (q_0 d_0 + sum_(gamma != 0) a_gamma d_(-gamma)).
```

Equivalent form:

```text
C_E,W^prod
 = exp(B_H2(E,W)) Mean_dyadic(H_c(u)G(u)).
```

Special nonoscillatory H2 case:

```text
G(u)=1
  => d_0=1 and d_eta=0 for eta != 0
  => C_E,W^prod = exp(B_H2(E,W)) w_(-1)/L(E,1).
```

For normalized kernels:

```text
C_E,W^prod = exp(B_H2(E,W))/L(E,1).
```

Required paper wording:

```text
This is an arithmetic product-average constant. It is not a pointwise
constant limit for c_E,W(e^u), and it is not determined by averaging log P.
```

## Proof Dependency Checklist

H1 profile:

- Fixed `W` and fixed Mellin convention.
- Meromorphic H1 contour identity in a finite box.
- Legal height sequence avoiding zeros.
- Central residue computation at `z=0`.
- Offcentral residue computation at `z=i gamma`.
- Multiple-zero Laurent expansion or explicit exclusion.
- Reciprocal-zero tail convergence mode.
- Horizontal and shifted-line contour tail estimates.

Product average:

- Theorem A in average-compatible form.
- Exact H2 local factor decomposition.
- Finite part `B_H2(E,W)`.
- Mean coefficients of `G=exp(Z_P)`.
- Product-error smallness for `eps_P`.
- Joint H1/H2 infinite-frequency tail passage.
- Diagonal extraction for finite exponential sums:

```text
A_U(e^(i(alpha)u)) -> 1 if alpha=0,
A_U(e^(i(alpha)u)) -> 0 if alpha!=0.
```

Still-open blockers not solved by this skeleton:

- shell moment bound for fixed H1 residues;
- reciprocal strip bounds `H-height/H-left`;
- source-closed H2 endpoint finite parts if not already supplied;
- curve-specific zero data for diagnostics;
- theorem-grade kernel filtering with tail control.

## Examples and Diagnostics

Example 1: one simple conjugate pair.

If only one conjugate pair is retained, then

```text
c_E,W(e^u)
 = q_0 + a_gamma e^(i gamma u)
       + conjugate(a_gamma)e^(-i gamma u)
       + o(1)
 = q_0 + 2 Re(a_gamma e^(i gamma u)) + o(1).
```

If `a_gamma != 0`, the H1 term does not have a pointwise constant limit.

Example 2: product diagonal.

If

```text
H_c(u)=q_0+a_gamma e^(i gamma u)+a_(-gamma)e^(-i gamma u),
G(u)=d_0+d_gamma e^(i gamma u)+d_(-gamma)e^(-i gamma u),
```

then the product average keeps exactly the zero-frequency diagonals:

```text
Mean(H_cG)
 = q_0 d_0 + a_gamma d_(-gamma) + a_(-gamma)d_gamma.
```

Example 3: finite signed filtering diagnostic.

The diagnostic script

```bash
python3 handoff-2026-05-11-h1-breakthrough-proof-wave/kernel_filter_moments.py \
  --gammas gamma1,gamma2,gamma3
```

constructs a signed log-Gaussian moment kernel with

```text
W_hat(0)=1,
W_hat(i gamma_j)=0
```

for the supplied finite list. This can test whether low offcentral residues
explain observed stabilization. It does not prove smoothing stabilization,
tail control, positivity, or fixed endpoint-kernel admissibility.

## No-Promotion Language For Draft

Allowed paragraph:

```text
When the fixed-kernel reciprocal-residue bounds are not available, the
rank-zero H1 term is best treated as a central residue plus an explicit
offcentral oscillatory profile. Separately, under a product-mean extraction
hypothesis for the H1 profile and the H2 Euler-product factor, the dyadic
arithmetic average of the product has a diagonal constant.
```

Forbidden replacements:

```text
Rank-zero smoothing converges pointwise to 1/L(E,1).
The H2 factor damps the H1 reciprocal poles pointwise.
Finite kernel filtering proves the fixed-kernel theorem.
The product-average theorem is an averaged-log theorem.
The EC smoothing theorem follows from the rank-zero fallback.
```

Safe abstract wording:

```text
We isolate a conditional rank-zero fallback: a pointwise oscillatory H1
profile and a separate arithmetic product-average theorem. This section is a
reduction and bookkeeping device; the fixed-kernel shell moment and reciprocal
strip estimates remain independent analytic inputs.
```

## Source Map For Final Paper

Local source paths:

```text
rank-zero/product theorem skeleton:
  handoff-2026-05-11-h1-breakthrough-proof-wave/RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md

blocked shell/strip context:
  handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md

finite filtering diagnostic:
  handoff-2026-05-11-h1-breakthrough-proof-wave/KERNEL_FILTER_DIAGNOSTIC_IMPLEMENTATION.md
```

Citation rule:

```text
Do not cite an external theorem in the final paper from this skeleton unless
the cited PDF has been fetched, converted with pdftotext, and quoted with
page/equation data in the local source packet.
```

