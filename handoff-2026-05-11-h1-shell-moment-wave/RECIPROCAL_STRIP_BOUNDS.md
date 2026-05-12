---
schema_version: 1
title: "Reciprocal strip bounds for H1 contour tails"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.76
dependencies:
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_ANALYTIC_ATTEMPT.md
tags: [ec-ndc, h1, contour-tail, reciprocal-strip, height-avoidance]
---

# Reciprocal Strip Bounds For H1 Contour Tails

Status: `RIGOROUS_REDUCTION`.

Confidence: `0.76`.

Confidence aggregation rule: take the minimum of the source-backed left-line
closure, the proof-candidate height lemma, and the unresolved `A<q` promotion
gap.

Dependencies:
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md`
- `handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md`
- `handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_ANALYTIC_ATTEMPT.md`

## Do Not Promote Unless

- `eta>1/2` is allowed by the kernel strip. This closes `H-left` by reflection
  to the absolute Euler-product side. For `eta<=1/2`, `H-left` remains a
  reciprocal lower-bound hypothesis.
- The horizontal height lemma is either fully written as a Cartan/Jensen proof
  for this fixed EC L-function or cited from a GL2 source by the project
  source protocol.
- The resulting polynomial height exponent `A_TC` is proved to satisfy
  `A_TC<q`. The argument below gives some finite `A_TC`; it does not prove
  `A_TC<2` for the repository smoothstep-scale `q=2`.
- Moving-box use checks the same `T(u)` against
  `e^(sigma u) T(u)^(A_TC-q)=o(u^r)`. Fixed-`u` tail closure is weaker.
- Offcentral reciprocal residues and multiple-zero Laurent terms remain
  separate H1 blockers. Strip bounds do not bound `1/L'(rho)`.
- Every external theorem used in a final paper has the required source packet:
  `curl + pdftotext + short quote + page/equation`.

## Verdict

`H-left` can be removed as a new assumption if the contour is shifted to

```text
Re z = -eta,       eta>1/2.
```

Then `s=1-eta+it` reflects under the elliptic-curve functional equation to
`2-s=1+eta-it`, where `1+eta>3/2` is in the absolute reciprocal Euler-product
half-plane. This gives

```text
|1/L(E,1-eta+it)| <= C_E,eta (1+|t|)^(-2 eta),
```

so

```text
int_R |W_hat(-eta+it)/L(E,1-eta+it)| dt < infinity
```

whenever `|W_hat(-eta+it)| << (1+|t|)^(-q)` and `q+2 eta>1`. For
`eta>1/2`, this is automatic for every positive Mellin-decay exponent `q`.

`H-height` reduces to a Titchmarsh-Cartan minimum-modulus lemma. The lemma
should give legal heights `T_n` with

```text
sup_{-eta<=x<=sigma} |1/L(E,1+x+iT_n)| <= C T_n^(A_TC)
```

for some finite fixed exponent `A_TC=A_TC(E,eta,sigma)`. This is enough only
for kernels with `q>A_TC`. It does not close the stated smoothstep target
`A<q` when `q=2`.

Thus the contour-tail assumption becomes:

```text
eta>1/2
+ Titchmarsh-Cartan EC height lemma with exponent A_TC
+ kernel decay q>A_TC.
```

For the current fixed smoothstep-scale `q=2`, the honest state is still:

```text
H-left: closed by eta>1/2.
H-height(A<2): not source-closed.
```

## H-left Proof

Use the EC convention from Sheth:

```text
Lambda(E,s)=N_E^(s/2)(2 pi)^(-s) Gamma(s)L(E,s),
Lambda(E,s)=w_E Lambda(E,2-s).
```

For `s=1-eta+it` with `eta>1/2`, rearrange:

```text
1/L(E,s)
 = w_E^(-1) N_E^(s-1) (2 pi)^(2-2s)
   Gamma(s)/Gamma(2-s) * 1/L(E,2-s).
```

Here `2-s=1+eta-it`, and `1+eta>3/2`. The reciprocal Euler product converges
absolutely and uniformly on this line, so

```text
|1/L(E,1+eta-it)| <= C_E,eta.
```

Stirling's gamma-ratio estimate gives

```text
|Gamma(1-eta+it)/Gamma(1+eta-it)| <<_eta (1+|t|)^(-2 eta).
```

Therefore

```text
|1/L(E,1-eta+it)| <<_E,eta (1+|t|)^(-2 eta).
```

Consequently

```text
|W_hat(-eta+it)/L(E,1-eta+it)|
 << (1+|t|)^(-q-2 eta),
```

which is integrable if `q+2 eta>1`.

This also rules out zeros on the shifted line for `eta>1/2`, since a zero at
`1-eta+it` would reflect to a zero at `1+eta-it`, contradicting the nonzero
absolute Euler product.

## Why eta<=1/2 Does Not Close

If `eta<=1/2`, reflection lands at

```text
Re(2-s)=1+eta<=3/2.
```

The reciprocal Euler product is no longer absolutely controlled. GRH would
remove zeros on `Re s=1-eta`, but it still would not give a polynomial bound
for `1/L(E,1-eta+it)` or absolute integrability after multiplication by a
fixed polynomial-decay Mellin kernel. This is a genuine reciprocal
minimum-modulus input, not a zero-location input.

## H-height Reduction

Let

```text
a = 1-eta,       b = 1+sigma,
K_T = {s=x+iT: a<=x<=b}.
```

A sufficient fixed-curve lemma is:

```text
TC-height(E,a,b):
there exist legal T_n -> infinity and A_TC<infinity such that
  sup_{s in K_Tn} |1/L(E,s)| <= C T_n^(A_TC).
```

Then the H1 horizontal edges satisfy

```text
|H_+(T_n,u)|+|H_-(T_n,u)|
 << e^(sigma u) T_n^(A_TC-q).
```

So fixed-`u` horizontal decay follows if `q>A_TC`, and moving-box decay needs

```text
e^(sigma u) T_n(u)^(A_TC-q)=o(u^r).
```

### Proof Skeleton For TC-height

The following proof is plausible and standard, but the final EC writeup should
either include all details or replace it with a PDF-verified GL2 citation.

1. Polynomial upper bound. In any fixed vertical strip containing `[a,b]`,
   functional equation plus absolute convergence on `Re s>3/2`, then
   Phragmen-Lindelof, give

   ```text
   |L(E,s)| <= C (1+|t|)^B.
   ```

2. Anchor lower bound. Choose `kappa>max(b,3/2)`. The absolute Euler product
   gives

   ```text
   |L(E,kappa+it)| >= c_E,kappa > 0.
   ```

3. Local zero count. Sheth's zero count gives

   ```text
   #{rho: |Im rho-T|<=C_0, a-C_0<=Re rho<=b+C_0} <<_E log T.
   ```

4. Jensen/Borel-Caratheodory. Apply Jensen in fixed disks centered near
   `kappa+iT`, using the anchor lower bound and polynomial upper bound. Divide
   by the local zero factors. The zero-free part has logarithm bounded by
   `O(log T)` in a slightly smaller rectangle.

5. Cartan avoidance. Cartan's lemma covers the points where the zero-factor
   product is smaller than `T^(-C)` by disks with total radii `<1/10`. The
   projections of those disks to the ordinate axis have total length `<1/5`,
   so some `T_* in [T,T+1]` avoids all of them.

6. On the horizontal segment `K_T*`, both the zero-factor part and the
   zero-free part are bounded below by `T^(-C)`. Hence

   ```text
   sup_{a<=x<=b} |1/L(E,x+iT_*)| <= T^(A_TC).
   ```

This proves only a finite exponent. It gives no useful numerical inequality
against `q=2`.

## What Is Source-closed

- EC analytic continuation and functional equation: source-backed.
- EC Euler product in `Re s>3/2` and Hasse-size local roots: source-backed.
- EC zero count `N_E(t)=c_E t log t+O(log t)`: source-backed.
- Zeta analogue of height-minimum theorem: source-backed as a model only.
- `H-left` for `eta>1/2`: proved from the source-backed EC facts plus the
  elementary gamma-ratio estimate.

## What Remains New

- A fully written EC/GL2 Titchmarsh-Cartan minimum-modulus proof for
  `TC-height(E,a,b)`, or a PDF-verified citation for it.
- Any bound showing the resulting exponent satisfies `A_TC<q`, especially
  `A_TC<2` for the current smoothstep-scale contour.
- `H-left` for `eta<=1/2`.
- Moving-box compatibility between `T(u)`, horizontal tails, original-line
  tails, and offcentral residue aggregation.

## Source Packet

Run directory:

```bash
/tmp/h1-shell-moment-agent5
```

Tool:

```bash
/tmp/h1-contour-tail-20260511/xpdf-tools-mac-4.06/binARM/pdftotext
```

Fetched/extracted:

```bash
curl -L --fail -o /tmp/h1-shell-moment-agent5/sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236
/tmp/h1-contour-tail-20260511/xpdf-tools-mac-4.06/binARM/pdftotext -layout /tmp/h1-shell-moment-agent5/sheth_ec_arxiv_2312.05236.pdf /tmp/h1-shell-moment-agent5/sheth_ec_arxiv_2312.05236.txt

curl -L --fail -o /tmp/h1-shell-moment-agent5/titchmarsh_zeta.pdf https://sites.math.rutgers.edu/~zeilberg/EM18/TitchmarshZeta.pdf
/tmp/h1-contour-tail-20260511/xpdf-tools-mac-4.06/binARM/pdftotext -layout /tmp/h1-shell-moment-agent5/titchmarsh_zeta.pdf /tmp/h1-shell-moment-agent5/titchmarsh_zeta.txt
```

SHA256:

```text
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_arxiv_2312.05236.pdf
ee495ba7e6b7af4722317baa79087881c16f648cb8af72843eb869c7497a03d0  titchmarsh_zeta.pdf
```

Verified anchors:

- Sheth, `Euler product asymptotics for L-functions of elliptic curves`,
  arXiv:2312.05236. PDF p. 1: "functional equation asserts". Use: EC
  functional equation.
- Sheth, PDF p. 1: "defined for Re(s) > 3/2". Use: absolute Euler-product
  side.
- Sheth, PDF p. 5, equation (2.1): "Riemann Hypothesis for elliptic curves".
  Use: Hasse-size local roots and reciprocal Euler-product convergence for
  `Re s>3/2`.
- Sheth, PDF p. 13, Theorem 3.1: "number of zeros". Use: local
  `O_E(log T)` zero count.
- Titchmarsh, `The Theory of the Riemann Zeta-function`, PDF p. 114,
  Theorem 9.7: "There is a constant A". Use: GL1 model for the height
  minimum-modulus theorem only. It does not prove the EC/GL2 height lemma.

## Bottom Line

The reciprocal strip package should be rewritten as:

```text
Choose eta>1/2.
Then H-left is closed.
Assume/prove TC-height(E,1-eta,1+sigma) with exponent A_TC.
Require q>A_TC for horizontal decay.
```

This is a real reduction of the H1 contour tails, but it is not a promotion of
the fixed smoothstep `q=2` theorem.

## Changed Paths

- `handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md`
