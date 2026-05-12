---
schema_version: 1
title: "Agent 06 - H1 Actual Dyadic Shell PV Direct Attack"
date: 2026-05-11
agent: "Top-10 Challenge Wave Agent 06"
type: theorem-attempt
tier: working
status: NO_GO
confidence: 0.88
sources:
  - ../start.md
  - L0_rules.md
  - L1_index.md
  - HANDOFF.md
  - handoff-2026-05-11-breakthrough-wave-3/AGENT06_ACTUAL_COEFFICIENT_H1_PV_THEOREM_2026-05-11.md
  - handoff-2026-05-11-breakthrough-wave-2/AGENT03_H1_ACTUAL_COEFFICIENT_MOVING_PV_2026-05-11.md
  - handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md
  - https://arxiv.org/abs/2310.03949
  - https://arxiv.org/abs/1306.0854
tags: [top10-challenge, agent06, h1, actual-coefficients, dyadic-shell-pv, dpmv, no-go]
---

# Agent 06 - H1 Actual Dyadic Shell PV Direct Attack

status: `NO_GO`

## Verdict

`H1-ActualDyadicShellPV(E,W,r,H)` is not proved.

DPMV source progress helps only as an absolute domination route. It does not
prove direct pointwise moving-window phase cancellation for the actual
coefficients

```text
a_gamma(E,W) = W_hat(i gamma) / L'(E,1+i gamma).
```

The live situation is:

```text
Direct actual PV:
  still uncontrolled.

DPMV/BFMT route:
  useful only if it yields a full reciprocal-derivative shell budget,
  including the non-separated bad set.

Weaker modes:
  log-Cesaro, Besicovitch/profile, and product-average are distinct theorem
  modes and must not be substituted for pointwise moving-window H1.
```

No EC stabilization theorem is promoted.

## Target

Use analytic rank only:

```text
r = ord_(s=1) L(E,s).
```

For simple offcentral H1 zeros

```text
rho = 1+i gamma,       gamma != 0,
```

aggregate same-ordinate residues first and set

```text
a_gamma(E,W) = W_hat(i gamma) / L'(E,1+i gamma).
```

The direct pointwise theorem is:

```text
H1-ActualDyadicShellPV(E,W,r,H):
  sum_(2^j <= H(2U))
    sup_(u in [U,2U])
      | sum_(2^j < |gamma| <= 2^(j+1))
          a_gamma(E,W) e^(i gamma u) |
  = o(U^r).
```

For rank one:

```text
sum_(2^j <= H(2U)) B_j(E,W;U) = o(U).
```

This is a pointwise moving-window statement. The supremum is inside the shell
sum and the height is the legal H1 moving contour height.

## Direct Attack

Define

```text
S_j(u)
  = sum_(2^j < |gamma| <= 2^(j+1))
      a_gamma e^(i gamma u),

B_j(U)
  = sup_(u in [U,2U]) |S_j(u)|,

A_j
  = sum_(2^j < |gamma| <= 2^(j+1)) |a_gamma|.
```

The deterministic inequality is only:

```text
B_j(U) <= A_j.
```

Thus direct pointwise PV can be proved in either of two genuinely different
ways:

```text
phase route:
  prove cancellation in B_j(U) for the actual a_gamma;

absolute route:
  prove sum_(2^j <= H(2U)) A_j = o(U^r).
```

Current packets prove neither for all simple offcentral H1 zeros.

Actual coefficient structure gives:

```text
real W => a_(-gamma) = conjugate(a_gamma),
Mellin decay => |W_hat(i gamma)| is small on high shells,
functional equation => residues are not arbitrary.
```

These are identities and size modifiers. They do not bound the moving
supremum. In particular, conjugation makes the profile real, not small; Mellin
decay needs reciprocal-derivative control; the functional equation does not
currently provide a lower-tail theorem for `|L'(E,1+i gamma)|`.

## Mode Split

| mode | object | what it can prove | pointwise H1? |
|---|---|---|---|
| pointwise moving-window | `sum B_j(U)=o(U^r)` | uniform H1 residue disappearance on `u in [U,2U]` | yes |
| absolute | `sum A_j=o(U^r)` | pointwise H1 by triangle inequality | yes, but not PV |
| log-Cesaro | averages of `S_j(u)` or `Z(u)` in `u` | oscillatory mean zero after tail control | no |
| Besicovitch/profile | `sum |a_gamma|^2` plus pair/tail control | almost-periodic/profile term in mean square | no |
| product-average | average of H1 profile times H2/product profile | retained diagonal correlations | no |

### Log-Cesaro

For a finite shell,

```text
(1/U) int_U^(2U) e^(i gamma u) du
  = O(1/(U |gamma|)).
```

Therefore log-Cesaro vanishing follows from a tail such as

```text
sum_gamma |a_gamma|/|gamma| < infinity.
```

This controls an average, not

```text
sup_(u in [U,2U]) |S_j(u)|.
```

It cannot replace `H1-ActualDyadicShellPV`.

### Besicovitch/Profile

A natural profile hypothesis is

```text
sum_gamma |a_gamma|^2 < infinity
```

plus close-pair control. This gives a `B^2` or mean-square object

```text
Z(u) = sum_gamma a_gamma e^(i gamma u).
```

It does not imply uniform convergence, dyadic shell sup bounds, or sparse-spike
control. For positive rank, an `O(1)` profile may be negligible in averaged
scale; that is not the pointwise moving-window theorem.

### Product-Average

If an H2/product profile has

```text
P(u) = d_0 + sum_lambda d_lambda e^(i lambda u),
```

then product averaging gives diagonal terms of the form

```text
sum_gamma a_gamma d_(-gamma)
```

whenever the tails and interchange are justified. Product averaging changes the
constant; it does not erase H1 residues and it does not imply pointwise
stabilization.

## DPMV Source Check

External claims were checked against primary arXiv sources and the already
downloaded PDF text packet in `/tmp/farey-dpmv-continuation-20260511`.

PDF hashes:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_2310_03949.pdf
7429a8705e1d7e790a925bd7a410338a52e24ab060e890bdb13f9b8780810f10  milinovich_ng_1306_0854.pdf
```

Primary source pages:

```text
BFMT: arXiv:2310.03949, "Negative discrete moments of the derivative of the Riemann zeta-function"
Milinovich-Ng: arXiv:1306.0854, "Simple zeros of modular L-functions"
```

Checked anchors:

```text
BFMT Theorem 1.1:
  zeta negative derivative moments over separated zero family F;
  under RH, at k=1/2 gives T^(1+delta)-scale upper bound.

BFMT Theorem 3.1:
  zeta zero-discrete mean value theorem with "any sequence of complex numbers";
  relies on Landau-Gonek.

Milinovich-Ng Lemma 3.3:
  GL2/newform Landau-Gonek analogue for zeros of L(s,f).

Milinovich-Ng Proposition 4.1:
  GL2 zero-discrete mean value theorem for A(s)=sum a(n)n^(-s);
  requires coefficient conditions (39), (40);
  includes Lambda_f * a convolution error.

Milinovich-Ng Proposition 4.3:
  prime-supported high moments only under x^m <= T^(2/3).
```

Source decision:

```text
LG-Explicit-GL2(f):
  source-closed adjacent input.

DPMV-GL2-GeneralA(f,eta):
  source-backed but coefficient-conditional.

DPMV-GL2-PrimePowerHighMoment(f,2/3):
  source-backed only below the 2/3 support wall.

BFMT-CoefficientErrorCheck(E):
  still live.
```

## Does DPMV Help This Target?

Yes, but only indirectly.

If a GL2/BFMT adaptation proves a separated-zero bound

```text
sum_(gamma in F_E(T,c))
  |L'(E,1+i gamma)|^(-1)
  << T^(1+delta),
```

and if the complementary bad set satisfies

```text
sum_(gamma notin F_E(T,c), simple)
  |L'(E,1+i gamma)|^(-1)
  = o(T^2),
```

then the absolute route can dominate the actual shells. With

```text
|W_hat(i gamma)| <= C_W |gamma|^(-q),
```

one gets

```text
A_j <= C_W 2^(-qj) R_E,1(2^j),

R_E,1(T)
  = sum_(T < |gamma| <= 2T, simple)
      |L'(E,1+i gamma)|^(-1).
```

For the current rank-one `q=2` packets, the clean sufficient target remains

```text
R_E,1(T) = o(T^2).
```

Then

```text
sum_(2^j <= H(2U)) A_j = o(U),
```

and `H1-ActualDyadicShellPV(E,W,1,H)` follows by triangle inequality.

But this is not a direct PV theorem. It uses no phase cancellation in
`e^(i gamma u)`. It proves pointwise H1 only after absolute reciprocal
coefficients are controlled.

## Remaining Blocker

DPMV progress does not currently control all actual reciprocal coefficients.

The unresolved pieces are exactly:

```text
1. BFMT-CoefficientErrorCheck(E):
   verify that the BFMT k=1/2 coefficient families satisfy the
   Milinovich-Ng Proposition 4.1/4.3 hypotheses and absorb Lambda_f*a errors.

2. EC-BFMT-BadSetBudget(E,c):
   prove the non-separated complement contributes o(T^2) to R_E,1(T).

3. Direct phase theorem:
   independently prove sum B_j(U)=o(U^r) for the actual coefficients.
```

Without 1 and 2, DPMV does not give the absolute route. Without 3, there is no
direct actual moving-window PV theorem.

## Final Boundary

Do not promote:

```text
spacing + l2/profile => pointwise PV
log-Cesaro => pointwise PV
product-average => pointwise constant
DPMV separated progress => full H1 actual shell PV
```

Promotable future statements are:

```text
H1-ActualDyadicShellPV(E,W,r,H)
  as a new fixed-curve moving-window exponential-sum theorem;

or

Full reciprocal-derivative domination:
  sum_(2^j <= H(2U)) 2^(-qj) R_E,1(2^j) = o(U^r).
```

Current status:

```text
direct pointwise moving-window: NO_GO
log-Cesaro: weaker averaged mode
Besicovitch/profile: weaker profile mode
product-average: retained-correlation mode
DPMV source progress: useful but insufficient; actual reciprocal coefficients remain uncontrolled
```

## Protocol Check

Commands/checks used:

```text
../te doctor
sed reads of HANDOFF.md, Wave 2 Agent 03, Wave 3 Agent 06, DPMV split
curl of arXiv TeX sources for 1306.0854 and 2310.03949
rg/sed checks of downloaded PDF text in /tmp/farey-dpmv-continuation-20260511
git status --short on assigned output path and named source files
```

No correspondence or email drafts were used or edited.

Changed file:

```text
primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT06_H1_ACTUAL_DYADIC_SHELL_PV_2026-05-11.md
```
