---
schema_version: 1
title: "Agent 05 H1 Local Minimum-Modulus Certificate"
date: 2026-05-11
agent: "Top-10 Challenge Wave Agent 05 -- H1 LocalMinMod(E)"
type: theorem-audit
tier: working
status: NO_GO
confidence: 0.91
dependencies:
  - HANDOFF.md
  - handoff-2026-05-11-breakthrough-wave-3/AGENT05_MINIMUM_MODULUS_LOCAL_FACTOR_2026-05-11.md
  - handoff-2026-05-11-breakthrough-wave-3/AGENT04_BAD_SET_COMPLEMENT_BUDGET_2026-05-11.md
  - handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md
tags: [top10-challenge, h1, local-minimum-modulus, reciprocal-derivative, no-go]
---

# Agent 05 H1 Local Minimum-Modulus Certificate

status: `NO_GO`

## Verdict

`H1-LocalMinMod(E)` should be permanently killed as a proof route from the
standard complex-analysis toolkit listed in the prompt.

Keep only the following as a named hypothesis:

```text
H1-LocalMinModCertificate(E):
For all simple zeros rho=1+i gamma in T<|gamma|<=2T outside B_T,
there is a zero-free circle |s-rho|=r_rho such that

  m_rho/r_rho >= T^(-alpha)(log T)^lambda,

with alpha<1, or alpha=1 and lambda>1, and

  sum_(rho in B_T) |L'(E,rho)|^(-1)=o(T^2).
```

This certificate is exactly sufficient, but none of Borel-Caratheodory,
Jensen, Cartan, Hadamard products, or GL2 growth/zero-count estimates produces
it. Each route either restates a lower bound for `L'(E,rho)`, supplies only
averages/good points/selected heights, or creates exceptional sets without the
required bad reciprocal budget.

## Exact Threshold

Let `rho=1+i gamma` be a simple zero and write

```text
L(E,s)=(s-rho)g_rho(s),       g_rho(rho)=L'(E,rho).
```

If `|s-rho|=r` is zero-free except for `rho` and

```text
min_(|s-rho|=r) |L(E,s)| >= m,
```

then `1/g_rho` is holomorphic in the disk, so the maximum principle gives

```text
|L'(E,rho)| = |g_rho(rho)| >= m/r.
```

If the shell certificate is

```text
m_T/r_T >= T^(-alpha)(log T)^lambda,
```

then

```text
|L'(E,rho)|^(-1) <= T^alpha(log T)^(-lambda).
```

Using `N_E(2T)-N_E(T) <<_E T log T`,

```text
sum_good |L'(E,rho)|^(-1)
  <<_E T^(1+alpha)(log T)^(1-lambda).
```

For rank-one H1, this is `o(T^2)` exactly when

```text
alpha < 1,
```

or

```text
alpha = 1 and lambda > 1.
```

At `alpha=1, lambda=1` the method gives only `O(T^2)`, not the needed little-o.

## Tool Audit

### Borel-Caratheodory

Source-checked theorem shape: Borel-Caratheodory bounds an interior maximum
`M(r,f)` using a boundary maximum of `Re f` and `f(0)`. It is an upper-bound
transfer, not a lower-bound generator.

Applied to `log g_rho` on a zero-free disk, it can move an already-known
upper bound for `log |1/g_rho|` or `log |g_rho|` inward. But an upper bound for
`log |1/g_rho|` is exactly a lower bound for `|g_rho|`; it is the missing
minimum-modulus input.

Decision:

```text
Borel-Caratheodory -> NO_GO for H1-LocalMinModCertificate(E).
```

It can support selected-height contour lemmas after an anchor lower bound and
Cartan/Jensen bookkeeping. It does not supply zero-centered boundary minima for
each zero.

### Jensen

For nonvanishing `g_rho` in the disk, `log |g_rho|` is harmonic and

```text
log |g_rho(rho)|
  = average_(|s-rho|=r) log |g_rho(s)|.
```

This is the local content behind Jensen/Poisson-Jensen after the zero at `rho`
has been removed. Therefore a lower bound for the boundary average is already
a lower bound for `|L'(E,rho)|`. A pointwise lower bound for the boundary
minimum is stronger still. Jensen does not create either one from zero counts.

Decision:

```text
Jensen -> NO_GO.
```

It can count zeros from growth and boundary averages. It cannot turn
`N_E(T,2T)<<T log T` into a lower bound for `g_rho(rho)`.

### Cartan

Cartan-type lemmas produce good points outside disks around zeros, or selected
horizontal heights. This is valuable for contour avoidance, but H1 residues need
one of:

```text
full circle:  min_(|s-rho|=r_rho) |L(E,s)| >= m_rho,
bad budget:   sum_bad |L'(E,rho)|^(-1)=o(T^2).
```

Cartan exceptional disks can intersect the zero-centered circle at its minimum.
Small total radius or small bad arc length is not enough, because a single
uncontrolled arc can drive the boundary minimum to zero. If bad zeros are
declared whenever their circles meet exceptional disks, the remaining problem
is exactly the bad reciprocal budget.

Decision:

```text
Cartan -> NO_GO without an added bad reciprocal budget.
```

### Hadamard Products

Hadamard factorization expresses an entire finite-order function as an
exponential factor times a canonical product over zeros. For a completed EC
`L`-function this can rewrite `L'(E,rho)` in terms of:

```text
exponential/gamma/trivial-zero factors,
product of distances to all other nontrivial zeros,
normalizing constants.
```

This is bookkeeping. To lower-bound the product one must already control close
neighbors, moderately close zero clusters, the far-zero exponential balance,
and the nonzero factor. A close neighbor gives an explicit small factor; many
moderately close zeros can also depress the product. Zero count bounds do not
give the needed product-distance lower bound.

Decision:

```text
Hadamard product -> NO_GO unless supplemented by small-gap/product-distance
reciprocal budgets equivalent to the H1 obstruction.
```

### GL2 Growth And Zero Counts

The source-checked EC zero count gives

```text
N_E(t)=alpha_E t(log t+c)/pi + O(log t),
```

hence local shell count `<<_E T log T` and unit-window count `<<_E log T`.
This is only cardinality control.

Li-Zaharescu selected-height minimum modulus gives, for Selberg-class objects
including holomorphic cusp-form `L`-functions, a height in each `[T,T+1]` with

```text
|L(sigma+it)| >= exp(-A log t/log log t)
```

in the fixed normalized strip. This is strong enough for horizontal contour
avoidance after EC normalization, but it is not a boundary circle around every
zero. It supplies `H-height`, not `1/L'(rho)` control.

Milinovich-Ng supplies GL2 zero mean-value machinery under RH and coefficient
hypotheses. The DPMV split already isolates that as the live BFMT coefficient
audit route. It is not a generic growth/zero-count implication and does not
produce local boundary minima by itself.

Decision:

```text
GL2 growth/zero-count estimates -> NO_GO for H1-LocalMinModCertificate(E).
```

They can feed `GL2-LandauGonek-DPMV` or selected-height contour work. They do
not revive LocalMinMod.

## Failure Model

All listed routes fail the same structural test. They control one of:

```text
average log |L|,
maximum of |L| or Re log L,
zero count,
good points outside exceptional disks,
selected horizontal heights,
formal products over zeros.
```

H1 needs:

```text
minimum over a full zero-centered boundary circle,
or a reciprocal-derivative tail budget for the zeros where the circle fails.
```

The gap is not cosmetic. If `L(E,s)=(s-rho)g_rho(s)`, then the desired
certificate is just

```text
|g_rho(rho)| >= T^(-alpha)(log T)^lambda.
```

Jensen makes this a boundary-average statement. Borel-Caratheodory can move
the statement inside after it is known on a larger boundary. Cartan can delete
bad arcs or points. Hadamard can rewrite it as a product. GL2 zero count can
bound how many factors appear at a given scale. None supplies the lower bound
with the required exponent.

## Permanent Kill Rule

Do not spend another wave on:

```text
Borel-Caratheodory + Jensen + Cartan + zero count
```

as a standalone derivation of `H1-LocalMinMod(E)`.

The only admissible future revival must enter as one of:

```text
1. a new source-checked theorem directly proving the certificate above;
2. a direct reciprocal-derivative tail theorem;
3. a BFMT/DPMV separated-zero theorem plus EC-BFMT-BadSetBudget(E,c);
4. a fixed-weight PV theorem strong enough to bypass reciprocal absolute sums.
```

Anything else is a reformulation of the killed route.

## Source Checks

Run directory:

```text
/tmp/agent05-top10-minmod-20260511
```

Extractor:

```text
/tmp/agent05-minmod-sources/xpdf-tools-mac-4.06/binARM/pdftotext
pdftotext version 4.06
```

Fetched/extracted PDFs:

```text
curl -L --fail -s -o huusko_selected_topics_complex_analysis.pdf \
  https://integraali.com/huusko/tiedostoja/3318213/2013.pdf
curl -L --fail -s -o dupuy_hadamard.pdf \
  https://tdupu.github.io/complexspring2017/hadamard.pdf
curl -L --fail -s -o titchmarsh_zeta.pdf \
  https://sites.math.rutgers.edu/~zeilberg/EM18/TitchmarshZeta.pdf
curl -L --fail -s -o sheth_2312_05236.pdf \
  https://arxiv.org/pdf/2312.05236
curl -L --fail -s -o li_zaharescu_Lprime_rho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
curl -L --fail -s -o milinovich_ng_1306_0854.pdf \
  https://arxiv.org/pdf/1306.0854
```

SHA256:

```text
72e14aab70396d502e606def6ec0ad76b68c75c171b5fa952843d6f78bc5ae2a  huusko_selected_topics_complex_analysis.pdf
1ce50fcd4ab8a2dd64cc080c4402eae8d44b3927bb509ca4820045f8711fc0c6  dupuy_hadamard.pdf
ee495ba7e6b7af4722317baa79087881c16f648cb8af72843eb869c7497a03d0  titchmarsh_zeta.pdf
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_2312_05236.pdf
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011  li_zaharescu_Lprime_rho.pdf
7429a8705e1d7e790a925bd7a410338a52e24ab060e890bdb13f9b8780810f10  milinovich_ng_1306_0854.pdf
```

Verified anchors:

- Huusko, `Selected Topics in Complex Analysis`, PDF p. 5, Proposition 2.2:
  "Borel-Caratheodory inequality"; theorem bounds `M(r,f)` by `A(R,f)` and
  `|f(0)|`.
- Huusko, PDF p. 13, Theorem 6.1: "Jensen's formula"; theorem equates the
  boundary average of `log |f|` with `log |f(0)|` plus zero factors.
- Dupuy, `Hadamard's Theorem and Entire Functions of Finite Order`, PDF p. 2,
  Theorem 1.4: "Hadamard"; finite-order entire functions factor into an
  exponential, zero at the origin, and canonical products over zeros.
- Titchmarsh, `The Theory of the Riemann Zeta-Function`, book p. 219,
  Theorem 9.7: "each interval [T,T+1) contains"; zeta model selected-height
  minimum modulus and exceptional-measure form, not a zero-centered local
  circle theorem.
- Sheth, `Euler Product Asymptotics for L-functions of Elliptic Curves`,
  arXiv:2312.05236, PDF p. 13, Theorem 3.1: "number of zeros"; gives
  `N_E(t)=alpha_E t(log t+c)/pi+O(log t)`.
- Li-Zaharescu, `Value Distribution of L'(rho)`, PDF p. 2: class includes
  "holomorphic cusp forms"; PDF p. 4, Proposition 3.1: "Each interval
  [T,T+1] contains" a height with the displayed lower bound.
- Milinovich-Ng, `Simple zeros of modular L-functions`, arXiv:1306.0854,
  PDF p. 19, Proposition 4.1: zero-discrete Dirichlet-polynomial mean square
  under RH and coefficient hypotheses; not a boundary minimum-modulus theorem.

No source above states the required zero-centered boundary certificate with
`alpha<1` or `alpha=1, lambda>1`, and no source supplies the bad reciprocal
budget for exceptions.

## Final Decision Table

| route | output available | H1 certificate? | status |
|---|---|---:|---|
| Borel-Caratheodory | interior upper bounds from real-part bounds | no | `NO_GO` |
| Jensen / Poisson-Jensen | boundary average and zero-factor identities | no | `NO_GO` |
| Cartan | good points/selected heights outside exceptional disks | no without reciprocal bad budget | `NO_GO` |
| Hadamard product | product expression over zeros | no without product-distance budget | `NO_GO` |
| GL2 growth/zero count | polynomial/selected-height/count inputs | no | `NO_GO` |
| local boundary certificate plus bad reciprocal budget | exact sufficient hypothesis | yes | hypothesis only |

## Verification Notes

- Read `start.md`, project `HANDOFF.md`, Wave 3 Agent 05 minimum-modulus
  packet, Agent 04 bad-set budget, and the DPMV split.
- Used only analytic-rank H1 language.
- Did not use H2 branch damping as H1 reciprocal-pole damping.
- No Koyama correspondence or email drafts touched.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT05_H1_LOCAL_MINMOD_CERTIFICATE_2026-05-11.md
```
