---
schema_version: 1
title: "Agent 02 Fixed-Curve Reciprocal Derivative Source Hunt"
date: 2026-05-11
agent: "Breakthrough Wave 3 Agent 02"
type: source-hunt
tier: working
status: NO_GO
confidence: 0.88
tags: [breakthrough-wave-3, h1, fixed-curve, reciprocal-derivative, source-hunt, gl2]
---

# Agent 02 Fixed-Curve Reciprocal Derivative Source Hunt

status: `NO_GO`

## Verdict

No source-checked theorem was found that proves, for one fixed elliptic curve/newform,

```text
sum_{T < |gamma| <= 2T, simple} |L'(E, 1+i gamma)|^(-1) = o(T^2),
```

or an upper negative first moment / small-derivative tail strong enough to imply it.

The only fixed-`L` GL2-capable source found is Li-Zaharescu. It is direct but
wrong-direction for H1: it gives a lower bound for a second negative moment,
existence of small `L'(rho)`, and signed mollified reciprocal sums, not an
absolute reciprocal upper bound.

Best source-shaped reduction remains:

```text
Fixed-curve GL2/EC negative first moment theorem:
  sum_{T < |gamma| <= 2T, simple} |L'(E,1+i gamma)|^(-1) = o(T^2),

or

Separated-zero theorem plus explicit bad-set reciprocal budget.
```

No theorem is promoted.

## Context Read

- `start.md`
- `token-economy.yaml`
- `L0_rules.md`
- `L1_index.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-3-plan.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT01_H1_DERIVATIVE_SOURCE_CLOSURE_2026-05-11.md`

No broad wiki/raw archives were loaded. No H2 branch damping was used as H1
reciprocal-pole damping. Analytic-rank H1 only. No Koyama correspondence or email
drafts touched.

## Search Scope

Searches were restricted to derivative-at-zero reciprocal objects and immediate
near misses. Representative queries:

```text
GL(2) L-functions L'(rho) negative moments zeros derivative reciprocal
elliptic curve L-function derivative at zeros reciprocal L'(rho)
newform L'(rho) zeros negative moment derivative
"negative discrete moments" "L'(rho)" "L-functions"
"sum" "1/|L'(rho)|" "cusp form"
"reciprocal of L'(rho)" "L-functions"
```

Candidates were source-registered only after PDF download and `pdftotext`
extraction.

## Source Protocol

Run directory:

```bash
/tmp/wave3-agent02-sources
```

Text extraction setup:

```bash
cd /tmp/wave3-agent02-sources
curl -L --fail -s -o xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac-4.06.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -v
```

`pdftotext` reported:

```text
pdftotext version 4.06 [www.xpdfreader.com]
```

Fetched/extracted sources:

```bash
curl -L --fail -s -o li_zaharescu_Lprime_rho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  li_zaharescu_Lprime_rho.pdf li_zaharescu_Lprime_rho.txt

curl -L --fail -s -o bfmt_negative_zeta_derivative.pdf \
  'https://arxiv.org/pdf/2310.03949'
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  bfmt_negative_zeta_derivative.pdf bfmt_negative_zeta_derivative.txt

curl -L --fail -s -o defaveri_simple_gl2.pdf \
  'https://ems.press/content/serial-article-files/48859'
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  defaveri_simple_gl2.pdf defaveri_simple_gl2.txt

curl -L --fail -s -o hko_random_matrix_zeta_derivative.pdf \
  'https://maths.ucd.ie/~noconnell/pubs/hko00.pdf'
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  hko_random_matrix_zeta_derivative.pdf hko_random_matrix_zeta_derivative.txt
```

SHA256:

```text
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011  li_zaharescu_Lprime_rho.pdf
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_negative_zeta_derivative.pdf
92f7bca8f11a5e521b7e9ed38ce8cc37dd36f054b8d8e55a5a768847158caee3  defaveri_simple_gl2.pdf
d73c088120f1b12c78ae21f403ff30d47e2a09f9e5df6184584edf35ec83b086  hko_random_matrix_zeta_derivative.pdf
```

## Exact Fixed-Curve / Fixed-`L` Results

### Li-Zaharescu, `Value Distribution of L'(rho)`

Classification: `FIXED_L_DIRECT_BUT_WRONG_DIRECTION`.

Scope anchor:

- PDF p. 1 abstract. Quote: "automorphic L-function".
- PDF p. 2 introduction. Quote: "holomorphic cusp forms".
- PDF p. 2 introduction. Quote: "automorphic L-functions of GL(m)".

Theorems checked:

- PDF p. 2, Theorem 1.1, equation (5). Under RH/no zeros to the
  right and Selberg normality, it proves a lower bound:

```text
sum_{T <= Im rho <= 2T} 1/|L'(rho)|^2 >> T (log T)^(kappa-1).
```

Short quote: "lower bound for the negative moment".

- PDF p. 2, Theorem 1.2, equation (6). Under the same right-half-plane
  zero condition and normality variant, it proves infinitely many small
  derivative values:

```text
min_{T <= Im rho <= 2T} |L'(rho)|
  << exp(-(sqrt(kappa)+o(1)) log T / log log T).
```

Short quote: "there are infinitely many zeros".

- PDF p. 4, equations (9)-(13), defines mollified sums including
  reciprocal derivatives. Equation (10) is the key signed object:

```text
S1 = sum_{L(rho)=0, T1<Im rho<T2} L'(rho)^(-1) X(rho)Y(1-rho).
```

Short quote: "Dirichlet polynomials".

- PDF p. 7, Theorem 4.1, gives an asymptotic formula for `S1` when
  `M=T^theta`, `theta<1`, under RH and almost-all simplicity.

Short quote: "almost all zeros".

Decision:

```text
Not load-bearing for H1.
```

Reasons:

- Theorem 1.1 is a lower bound for `sum |L'(rho)|^(-2)`, not an upper
  bound for `sum |L'(rho)|^(-1)`.
- Theorem 1.2 proves existence of small derivative values; it is not a
  small-derivative upper tail.
- The signed mollified sum `S1` is not an absolute moment and does not
  control the H1 coefficients
  `W_hat(i gamma) exp(i gamma u) / L'(E,1+i gamma)`.
- The theorem is fixed-`L` and GL2-capable, but it does not prove the
  fixed-curve reciprocal budget.

## Families

No source-checked theorem was found in a GL2/newform/elliptic-curve family
that directly controls

```text
sum |L_f'(rho_f)|^(-1),
negative moments of L_f'(rho_f) at zeros,
or small-L_f'(rho_f) tails at zeros.
```

Family papers surfaced by search were about central values, central derivatives,
function-field `L`-values with small shifts, or zero statistics. Those are not
the derivative-at-zero reciprocal object and were not used as theorem inputs.

Decision:

```text
No family source supplies a fixed-curve theorem by specialization.
```

## Zeta-Only Analogues

### Bui-Florea-Milinovich, negative discrete moments of `zeta'(rho)`

Classification: `ZETA_ONLY_MODEL_THEOREM`.

Theorems checked:

- PDF p. 1, equation (1.1), defines

```text
J_{-k}(T) = sum_{T < gamma <= 2T} |zeta'(rho)|^(-2k).
```

Short quote: "negative discrete moments".

- PDF pp. 2-3, Theorem 1.1, equation (1.2). Under RH, for the separated
  subfamily

```text
F = { gamma in (T,2T] : |gamma-gamma'| >> 1/log T
      for every other ordinate gamma' },
```

it proves

```text
sum_{gamma in F} |zeta'(rho)|^(-2k)
  << T^(1+delta),       if 2k(1+epsilon) <= 1,
  << T^(k+1/2+delta),   if 2k(1+epsilon) > 1.
```

For `k=1/2`, this gives the desired first reciprocal moment shape on `F`,
but only for zeta and only on a separated subfamily.

Short quote: "two different subfamilies".

- PDF p. 3, section 1.2. The paper explicitly warns that full-family
  negative moments require more than RH plus simplicity:

Short quote: "simplicity of zeros is not enough".

- PDF p. 4, equations (1.5)-(1.6). Under the Weak Mertens Conjecture,
  the paper records full-family zeta bounds:

```text
J_{-k}(T) = o(T^(k+1)(log T)^(1-k)),  0<k<1,
J_{-k}(T) = o(T^(2k)),                k>=1.
```

Decision:

```text
Useful proof model only.
```

Limits:

- It is zeta-only.
- The main theorem is not over all zeros; it requires a separated subfamily.
- The full-family statement uses WMC and is still zeta-only.
- It cannot be cited for fixed elliptic curves/newforms without a new GL2
  analogue and a bad-set reciprocal budget.

## Heuristics

### Hughes-Keating-O'Connell random-matrix model

Classification: `HEURISTIC_ZETA_ONLY`.

Anchors:

- PDF p. 1, abstract. Quote: "Random matrix theory is used".
- PDF p. 1, equation (1.1), defines normalized zeta derivative moments
  at zeros.
- PDF p. 3, Conjecture 1.3, equation (1.16), predicts `J_k(T)`.
- PDF p. 6, Conjecture 2.3, equation (2.22), gives the `k=-1/2`
  first reciprocal derivative prediction.
- PDF p. 7, discussion after equation (2.25), explains the large negative
  moment obstruction from near-collisions. Short quote: "two zeros lie
  very close together".

Decision:

```text
Diagnostic only; no theorem input.
```

Limits:

- It is zeta-only random-matrix heuristics.
- It predicts the shape of negative moments but does not prove an upper
  bound.
- It reinforces the same bad-set problem: close zeros dominate large
  reciprocal derivative moments.

## Adjacent Non-Load-Bearing Sources

### de Faveri, simple zeros of GL(2) L-functions

Classification: `ADJACENT_ONLY`.

Anchors:

- PDF p. 1 abstract. Quote: "first power bound".
- PDF p. 2, Theorem 1.1. For a primitive holomorphic modular form of
  arbitrary weight, level, and nebentypus, it gives a power lower bound
  for the count of simple zeros of the completed `L`-function.

The extracted text renders the exponent badly, but the theorem statement is
the source anchor:

```text
N_f^s(T) = Omega(T^delta) for any delta < 2/27.
```

Decision:

```text
Not load-bearing for H1.
```

Reason:

Simple-zero counts do not upper-bound reciprocal derivatives. They do not
control

```text
sum |L'(rho)|^(-1)
```

even over the zeros known to be simple, and they do not bound the complement.

## H1 Implication Test

For analytic rank one, H1 needs

```text
R_E,1(T) = sum_{T < |gamma| <= 2T, simple}
           |L'(E,1+i gamma)|^(-1) = o(T^2).
```

Checked sources fail as follows:

| source class | source | result shape | H1 status |
|---|---|---|---|
| fixed-`L` GL2-capable | Li-Zaharescu | lower `sum |L'|^-2`; small-value existence; signed mollified sums | wrong direction / not absolute |
| family | searched candidates | central values, central derivatives, or zero statistics | not the object |
| zeta theorem | Bui-Florea-Milinovich | upper negative moments for zeta on separated subfamilies; WMC full-family zeta observation | model only |
| heuristic | Hughes-Keating-O'Connell | RMT prediction for zeta derivative moments | no theorem |
| adjacent GL2 | de Faveri | power-many simple zeros | no reciprocal cap |

## Exact Missing Theorem

The source hunt reduces H1 to the following still-missing theorem.

```text
FixedCurve-GL2-RecipDeriv-Budget(E).

Let E/Q be fixed and let L(E,s) be normalized so H1 zeros are
rho = 1+i gamma. For dyadic T,

  sum_{T < |gamma| <= 2T, simple} |L'(E,rho)|^(-1) = o(T^2).

Equivalently, prove a layer-cake tail

  integral_1^infty #{T<|gamma|<=2T :
      |L'(E,1+i gamma)|^(-1) >= V} dV = o(T^2),

or prove a separated-zero theorem plus

  sum_{gamma in bad set} |L'(E,1+i gamma)|^(-1) = o(T^2).
```

The BFMT zeta theorem identifies the plausible proof shape. Li-Zaharescu shows
the fixed-`L` reciprocal-derivative machinery exists, but not in the absolute
upper-tail direction required here.

## Acceptance Check

- Top-level status is one of the allowed statuses: `NO_GO`.
- No theorem promoted.
- Every external theorem claim above has `curl + pdftotext` provenance,
  short quote, and page/equation anchor.
- Exact fixed-curve/fixed-`L`, families, zeta-only analogues, heuristics,
  and adjacent sources are separated.
- Analytic-rank H1 only.
- H2 branch damping not used for H1 reciprocal-pole damping.
- No Koyama correspondence/email drafts.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT02_FIXED_CURVE_RECIP_DERIV_SOURCE_HUNT_2026-05-11.md
```
