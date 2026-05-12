---
schema_version: 1
title: "Agent 08 H2 S1 renormalized log-growth"
date: 2026-05-11
agent: "Top 10 Challenge Wave Agent 08"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
tags: [top10-challenge-wave, h2, s1, cut-plane, renormalized-log-growth, right-branch]
---

# Agent 08 H2 S1 Renormalized Log-Growth

## Status

`RIGOROUS_REDUCTION`.

No unconditional H2 theorem is promoted. The correct replacement target is a
renormalized cut-plane theorem with exact right-cut retention:

```text
S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c).
```

The old literal global-branch theorem at endpoint decay
`|W_hat| << |t|^-2` remains unsafe. Renormalization removes the artificial
`2 pi i N(t)` branch accumulation on the left edge. A stronger kernel

```text
|W_hat^(j)(sigma+it)| << (1+|t|)^(-2-epsilon),  j=0,1,
```

also kills that particular accumulation, but it does not remove right branches.

Main correction to the Wave 3 right-branch handoff: if `Re a>0`, retaining only
the first term

```text
c_a K^a W_hat(a) / log K
```

is not enough for a finite-part theorem. The next Watson remainders have size
`K^(Re a)/(log K)^2`, still divergent. Therefore the theorem must retain the
whole right cut-lip integral unless a no-right-branch theorem is assumed.

No Koyama correspondence or email draft was touched.

## Objects

Fix an elliptic curve `E/Q`, analytic rank only

```text
r = ord_{s=1} L(E,s).
```

Let

```text
u = log K,
A_E(z) = sum_{p good} a_p p^(-1-z)
```

initially in the convergence half-plane. Use the Wave 2 branch identity in
`Re z > -eta`, `0 < eta < 1/4`:

```text
A_E(z)
 = log L_good(E,1+z)
   - (1/2) log L_sym,E^good(1+2z)
   + (1/2) log zeta_good(1+2z)
   + Phi_E(z),
```

where `Phi_E` is holomorphic in the strip.

The endpoint kernel satisfies

```text
W_hat(z) = 1/z + O(1)
```

at `z=0`, and on `-eta <= sigma <= c`, away from the central pole,

```text
|W_hat^(j)(sigma+it)| <= C_W (1+|t|)^(-2),  j=0,1.
```

The stronger-kernel alternative replaces `-2` by `-2-epsilon`.

## Source Protocol

Run directory:

```text
/tmp/agent08-h2-s1-renorm-sources-20260511
```

Commands run:

```bash
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac.tar.gz
curl -L --fail -o sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236
curl -L --fail -o ils_math_9901141.pdf https://arxiv.org/pdf/math/9901141
curl -L --fail -o hoffstein_lockhart_maass_siegel.pdf https://www.math.columbia.edu/~goldfeld/CoeffMaassForms.pdf
curl -L --fail -o zeta_zero_count_arxiv_2107.06506.pdf https://arxiv.org/pdf/2107.06506
./xpdf-tools-mac-4.06/binARM/pdftotext -layout sheth_ec_arxiv_2312.05236.pdf sheth_ec_arxiv_2312.05236.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout ils_math_9901141.pdf ils_math_9901141.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout hoffstein_lockhart_maass_siegel.pdf hoffstein_lockhart_maass_siegel.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout zeta_zero_count_arxiv_2107.06506.pdf zeta_zero_count_arxiv_2107.06506.txt
```

SHA256:

```text
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_arxiv_2312.05236.pdf
5072c63324c329250f70c4ef4e2648a0e8ff465d6b9c241c3d3646d4c6759997  ils_math_9901141.pdf
031de26f73977602225ec96b2207f3070cfc7d6b3cfc2371faed52ee254fb632  hoffstein_lockhart_maass_siegel.pdf
3fc4c89f49249924e61cb0d289d81559faed53fcbb838628ea32dc7ec6f89fbf  zeta_zero_count_arxiv_2107.06506.pdf
c0a2992348c0407356cec39f2f4b2e73705fb77edc852a4e9196e222712451a8  xpdf-tools-mac.tar.gz
```

Checked anchors:

- Sheth, arXiv:2312.05236, PDF p. 13, Theorem 3.1: "number of zeros" for
  `L(E,s)` satisfies `N_E(t)=c_E t(log t+c)+O(log t)`. Same page,
  Corollary 3.2: the reciprocal-square zero sum "converges".
- Hasanalizade-Shen-Wong, arXiv:2107.06506, PDF p. 1: `N(T)` counts
  "non-trivial zeros" of zeta; PDF p. 2, Corollary 1.2 gives an explicit
  Riemann-von Mangoldt error bound.
- Iwaniec-Luo-Sarnak, arXiv:math/9901141, PDF p. 11, equations (13)-(15):
  the symmetric-square "Euler product of degree 3 is entire" and satisfies a
  functional equation.
- Hoffstein-Lockhart, Annals 140 (1994), PDF p. 3, equations (0.6)-(0.8):
  the GL(3) object is the "adjoint square lift"; `L(s,F)` is "known to be
  entire", with `L(1,F)` nonzero.

Use limits:

- EC and zeta zero ledgers are source-supported.
- Sym2/adjoining-square analytic continuation is source-backed as a global
  finite-degree object, but the exact good-prime S1/Sym2 finite-part contour is
  still an in-repo theorem package. This packet imports Wave 2 Agent 06 for the
  exact good-prime reconciliation and does not independently promote it.
- No external source is cited as proving the endpoint-smoothed fixed-curve
  S1 theorem.

## Branch Ledger

In the cut strip `-eta <= Re z <= c`, write every logarithmic branch point
`a` using

```text
A_E(z) = c_a log(1/(z-a)) + holomorphic.
```

For a noncolliding branch point,

```text
c_a =
  - ord_{s=1+a} L_good(E,s)
  + (1/2) ord_{s=1+2a} L_sym,E^good(s)
  - (1/2) ord_{s=1+2a} zeta_good(s).
```

Collisions add these coefficients. At `a=0`,

```text
c_0 = 1/2 + kappa_sym/2 - r,
```

where

```text
kappa_sym = ord_{s=1} L_sym,E^good(s).
```

Under the Wave 2 Agent 06 standard good-prime adjoint/Sym2 reconciliation,
`kappa_sym=0`, hence `c_0=1/2-r`.

Define the noncentral branch set

```text
B = {a != 0 : -eta < Re a <= c}.
```

Split it as

```text
B^- = {a in B : Re a <= 0},
B^+ = {a in B : Re a > 0}.
```

For `a=beta+i gamma`, put

```text
M_a = sup_{0 <= v <= beta+eta}
  ( |W_hat(a-v)| + |W_hat'(a-v)| ).
```

The branch summability input needed for endpoint decay `q=2` is

```text
sum_{a in B} |c_a| M_a < infinity
```

for any branch family whose cut lips are to be summed. It follows from
`N(T+1)-N(T)=O(log T)` plus `|W_hat|+|W_hat'|<<|t|^-2` for EC and zeta
ledgers, and from the same finite-degree local zero-count input for Sym2.

Agent 09 classification remains valid for the S1 right ledger: in `Re a>0`,
the Sym2 and zeta good-prime factors are evaluated at `Re(1+2a)>1`, so their
Euler products are absolutely convergent and locally nonvanishing. Thus the
standard right branches are exactly shifted right-of-central zeros of
`L_good(E,s)`:

```text
a = rho-1,  Re rho > 1,
c_a = -ord_{s=rho} L_good(E,s).
```

No-right-branch is therefore a GRH/RH-type input and is not proved here.

## Exact Retained Cut-Lip Terms

For each branch `a=beta+i gamma` with `beta>-eta`, whose chosen cut does not
hit the kernel pole at `z=0`, the exact left-going lip contribution is

```text
I_a(K)
 = c_a K^a int_0^(beta+eta) e^(-uv) W_hat(a-v) dv,
u = log K.
```

If an exceptional real cut would pass through `z=0` or another kernel pole,
route that cut around the pole and retain the resulting finite local term
explicitly. None of the conclusions below may hide such a term in the error.

For nonright branches `beta <= 0`, Watson expansion and the summed derivative
bound give

```text
sum_{a in B^-} I_a(K)
 = (1/u) sum_{a in B^-} c_a K^a W_hat(a)
   + O_E,W(u^-2)
   + O_E,W(K^-eta).
```

For right branches `beta>0`, the exact retained term is

```text
R_S1^+(K;E,W,eta,c)
 = sum_{a in B^+} c_a K^a
     int_0^(beta+eta) e^(-uv) W_hat(a-v) dv.
```

This is the safe retained object. Its first Watson term is

```text
B_S1^+(K;E,W,c)
 = (1/u) sum_{a in B^+} c_a K^a W_hat(a),
```

which specializes to Agent 09's formula

```text
-(1/log K) sum_{rho in Z_S1^+(E;c)}
  m_rho K^(rho-1) W_hat(rho-1).
```

But `B_S1^+` alone is not enough when any `Re a>0` branch exists:

```text
I_a(K) - c_a K^a W_hat(a)/u
 = O_a,W(K^(Re a) u^-2),
```

and `K^(Re a)u^-2` is not `o(1)`. Therefore a pointwise H2 theorem must either
assume `B^+=empty`, prove cancellation of the full right-lip aggregate, or
subtract `R_S1^+`, not merely `B_S1^+`.

## Renormalized Log-Growth Input

For finite height `T`, remove branch cuts and define the regularized boundary
value by subtracting the local logarithmic jumps:

```text
A_E^reg,T(z)
 = A_E(z) - c_0 log(1/z)
   - sum_{a in B, |Im a| <= T+1} c_a log(1/(z-a)),
```

with the same left-going cuts and local branch choices as the contour.

The exact input still needed is:

```text
RegularLogLeftEdge(E,W,eta;c):
```

there exists a truncation sequence `T_n -> infinity`, avoiding branch ordinates,
such that:

1. Horizontal edges:

   ```text
   |A_E^reg,T_n(sigma +/- iT_n)| << (log T_n)^B
   ```

   uniformly for `-eta <= sigma <= c`, after the local branch disks/cuts are
   removed.

2. Left edge:

   ```text
   int_{-T_n}^{T_n}
     |W_hat(-eta+it) A_E^reg,T_n(-eta+it)| dt = O_E,W(1)
   ```

   in the finite cut-plane sense, with convergence as `n -> infinity`.

3. Branch lips:

   ```text
   sum_{a in B} |c_a| M_a < infinity
   ```

   for all lips being summed, with `B^+` retained exactly.

4. The ordinary holomorphic correction `Phi_E` and finite bad-prime factors
   obey the same boundary estimates; finite factors only alter constants and
   finite branch ledgers.

This is the precise renormalized replacement for the literal global-branch
left-edge assertion. It is plausible from finite-degree polynomial growth,
local zero counts `N(T+1)-N(T)=O(log T)`, and Cartan/Jensen local
factorization, but this packet does not promote it as a sourced external
theorem for the exact S1 object.

## Conditional Theorem

Theorem `S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c)`.

Assume:

1. the Wave 2 branch identity for `A_E(z)` in `Re z > -eta`;
2. the exact good-prime Sym2 normalization of Wave 2 Agent 06, if
   `kappa_sym=0` is used;
3. all singularities in the strip are logarithmic branches plus explicitly
   listed finite ramified factors;
4. the EC, zeta, and Sym2 branch ledgers satisfy the weighted summability
   above;
5. `RegularLogLeftEdge(E,W,eta;c)`;
6. no right branch is silently dropped: `B^+` is empty, canceled by a separate
   theorem, or retained as `R_S1^+`.

Then, for `u=log K`,

```text
S_1,W^good(K)
 = c_0 log u
   + C_1,E,W,c
   + (1/u) sum_{a in B^-} c_a K^a W_hat(a)
   + R_S1^+(K;E,W,eta,c)
   + O_E,W(u^-2)
   + O_E,W(K^-eta).
```

Equivalently,

```text
S_1,W^good(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W,c
   + (1/log K) sum_{a in B^-} c_a K^a W_hat(a)
   + R_S1^+(K;E,W,eta,c)
   + O_E,W((log K)^-2)
   + O_E,W(K^-eta).
```

If `B^+=empty`, or if `R_S1^+` is subtracted, and all nonright branches satisfy
`Re a<=0`, the noncentral aggregate is `O_E,W(1/log K)`. With
`kappa_sym=0`, this gives the S1 finite-part form

```text
S_1,W^good(K)
 = (1/2-r) log log K + C_1,E,W + o(1)
```

in the no-right-branch mode.

Proof sketch.

Start from Mellin inversion on `Re z=c`. Apply Cauchy's theorem in finite
cut rectangles using the local branch choices. The central branch at `0`
contributes

```text
c_0 log u + constant
```

because `W_hat(z)=1/z+O(1)` and
`A_E(z)=c_0 log(1/z)+holomorphic`. Each noncentral branch lip gives the exact
integral `I_a(K)`. The summed Watson expansion is legal for `B^-` by
`sum |c_a|M_a<infinity`; `B^+` is retained exactly. Horizontal edges vanish
along `T_n` by `T_n^-2 polylog(T_n)->0`. The renormalized left edge is
`O(K^-eta)` by the weighted integrability clause. Letting `T_n->infinity`
proves the formula.

## H2 Consequence With Correct Retention

Using the Wave 2 local H2 identity and the source-closed Sym2 finite part in
the standard convention `kappa_sym=0`, the right-retained H2 mode is:

```text
log P_E,W^good(K)
 + r log log K
 - R_S1^+(K;E,W,eta,c)
 = C_H2,E,W,c
   + O_E,W(1/log K)
   + O_E,W(K^-eta),
```

provided the ordinary good-prime Mertens term and `m>=3`/bad-prime corrections
are handled in the existing H2 bookkeeping.

The weaker subtraction

```text
log P_E,W^good(K) + r log log K - B_S1^+(K;E,W,c)
```

does not have a finite limit if a right branch with `Re a>0` is present,
unless a further full-lip cancellation theorem is supplied.

Thus the pointwise finite-part theorem

```text
log P_E,W^good(K) + r log log K = C_H2,E,W + o(1)
```

requires one of:

```text
B^+ = empty,
R_S1^+(K;E,W,eta,c) = o(1),
or exact subtraction of R_S1^+.
```

Current sources prove none of the first two unconditionally.

## Stronger-Kernel Alternative

If the endpoint kernel is strengthened to

```text
|W_hat^(j)(sigma+it)| << (1+|t|)^(-2-epsilon),  j=0,1,
```

then the literal accumulated global branch constant is absolutely integrable.
Indeed, zero counting gives cumulative branch size at most

```text
N(t) = O_E(t log t)
```

for EC and zeta ledgers, and the finite-degree Sym2 input gives the same
order. Hence

```text
int_2^infinity N(t) t^(-2-epsilon) dt
 << int_2^infinity (log t) t^(-1-epsilon) dt
 < infinity.
```

This stronger kernel can replace the renormalized left-edge device for the
specific `2 pi i N(t)` obstruction. It still does not justify deleting right
branches, and it still needs the exact good-prime branch identity and Sym2
normalization.

For the current smoothstep-scale `q=2` kernel, the same calculation is

```text
int_2^infinity (t log t) t^-2 dt
 = int_2^infinity (log t)/t dt
 = infinity.
```

Therefore literal global-branch `S1-CutPlane-LogGrowth(E,W,eta)` should remain
`NO_GO` at `q=2`; only the renormalized theorem is viable.

## What Remains To Promote

To upgrade this packet from `RIGOROUS_REDUCTION` to `THEOREM_PROMOTED`, close
the following exact inputs:

```text
RegularLogLeftEdge(E,W,eta;c)
Sym2-ZeroLedger-RegularLog(E,W,eta;c)
ExactGoodPrime-Sym2-Normalization(E) in the same local convention
RightBranchAbsentOrFullLipCancellation(E,W,eta;c), if no retained term is allowed
```

The first two are the live source/proof obligations. The third is imported
from Wave 2 Agent 06 for the standard convention. The fourth is GRH-type or a
new cancellation theorem; absent it, H2 must retain `R_S1^+`.

## Obstruction Boundary

Killed:

```text
literal global branch + q=2 + absolute left-edge integrability.
```

The divergence is exactly the branch-count accumulation:

```text
2 pi i N(t) * t^-2.
```

Reduced:

```text
S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c)
```

to regular-log left-edge control, weighted branch summability, exact Sym2
normalization, and exact right-lip retention.

Not transferred:

```text
H2 branch damping -> H1 reciprocal-pole control.
```

This packet gives no estimate for `1/L'(E,1+i gamma)` and no H1 shell/PV
input.

## Verification Notes

Local reads:

```text
HANDOFF.md
handoff-2026-05-11-breakthrough-wave-3/AGENT08_S1_CUTPLANE_LOG_GROWTH_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-3/AGENT09_S1_RIGHT_BRANCH_CLASSIFICATION_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-2/AGENT05_H2_S1_BRANCH_CONTOUR_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-2/AGENT06_H2_GOOD_PRIME_SYM2_CLOSURE_2026-05-11.md
handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
```

`./te doctor` could not be run because `./te` is absent in
`/Users/za/Documents/Farey NOW/primes-equispaced`; `L0_rules.md` and
`L1_index.md` were read directly.

Changed file:

```text
primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT08_H2_S1_RENORMALIZED_LOG_GROWTH_2026-05-11.md
```
