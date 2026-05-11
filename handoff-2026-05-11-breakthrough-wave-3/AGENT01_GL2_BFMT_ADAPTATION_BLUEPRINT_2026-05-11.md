---
schema_version: 1
title: "Agent 01 GL2/EC BFMT adaptation blueprint"
date: 2026-05-11
agent: "Breakthrough Wave 3 Agent 01 -- GL2/EC BFMT Adaptation Blueprint"
type: adaptation-blueprint
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.78
tags: [breakthrough-wave-3, h1, gl2, elliptic-curve, bfmt, reciprocal-derivative]
---

# Agent 01 GL2/EC BFMT Adaptation Blueprint

## Verdict

BFMT does not directly transfer from `zeta` to one fixed elliptic curve/newform.
It gives a precise proof model for a separated-zero theorem:

```text
EC-BFMT-Separated(k=1/2):
sum_{gamma in F_E(T,c)} |L'_E(1+i gamma)|^(-1)
  <<_{E,c,delta} T^(1+delta).
```

This would be enough on the good separated set because `T^(1+delta)=o(T^2)` for
fixed `delta<1`. It does not close H1 by itself. The full rank-one target still
needs the separate complement budget

```text
sum_{T<|gamma|<=2T, gamma notin F_E(T,c), simple}
  |L'_E(1+i gamma)|^(-1) = o(T^2).
```

No pair-correlation, zero-density, ratios-conjecture, or simplicity-count input
replaces that reciprocal complement estimate. BFMT is therefore a rigorous
reduction blueprint, not a promoted theorem.

## Source-Checked External Packet

Only BFMT was source-checked here; no broad source hunt was run.

```bash
mkdir -p /tmp/agent01-gl2-bfmt-20260511
curl -L --fail -s -o bfmt_negative_zeta_derivative.pdf \
  https://arxiv.org/pdf/2310.03949
curl -L --fail -s -o xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac-4.06.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  bfmt_negative_zeta_derivative.pdf bfmt_negative_zeta_derivative.txt
./xpdf-tools-mac-4.06/binARM/pdfinfo bfmt_negative_zeta_derivative.pdf
shasum -a 256 bfmt_negative_zeta_derivative.pdf
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_negative_zeta_derivative.pdf
```

PDF metadata: 19 pages.

Checked anchors:

- BFMT p. 1, abstract: states the paper's conditional upper-bound purpose.
- BFMT p. 2, Theorem 1.1: quote "Assume the Riemann hypothesis"; equation
  `(1.2)` gives the separated-family bound.
- BFMT p. 3, full-family warning: quote "simplicity of zeros is not enough".
- BFMT p. 3, proof input: quote "Littlewood's classical estimate".
- BFMT p. 6, Lemma 2.3: quote "coefficients"; equations `(2.4)-(2.5)`
  give the prime-polynomial coefficient bounds.
- BFMT p. 4, overview: quote "Landau-Gonek explicit formula".
- BFMT p. 8, Theorem 3.1: quote "any sequence of complex numbers".
- BFMT p. 15, Section 5 parameter setup: quote "conditions above ensure";
  equations `(5.1)-(5.7)` and the displayed inequalities impose the
  `T^(1-o(1))` support range.

## Normalization For EC

Use the normalized central-line variable

```text
mathcal L_E(s) := L(E, s + 1/2).
```

Then BFMT's `zeta` zero `rho=1/2+i gamma` corresponds to

```text
mathcal L_E(1/2+i gamma)=L(E,1+i gamma)=0,
mathcal L'_E(1/2+i gamma)=L'_E(1+i gamma).
```

All BFMT shifts `rho+1/log T` become

```text
L(E, 1 + 1/log T + i gamma).
```

The analytic-rank-one central zero at `s=1` is not in dyadic shells
`T<|gamma|<=2T`. No BSD or algebraic-rank substitution is used.

## BFMT Skeleton At `k=1/2`

BFMT defines negative discrete moments over zeta zeros and proves, on RH, an
upper bound over the separated set

```text
F = {gamma in (T,2T] : |gamma-gamma'| >> 1/log T for every other zero ordinate}.
```

For `k=1/2`, BFMT Theorem 1.1, equation `(1.2)`, gives

```text
sum_{gamma in F} |zeta'(rho)|^(-1) << T^(1+delta).
```

The proof has three load-bearing steps.

1. Compare the derivative at a zero to a shifted value:

```text
log 1/|zeta'(rho)|
  = log 1/|zeta(rho+1/log T)| + controlled zero-spacing error.
```

BFMT proves this for separated zeta zeros using equation `(2.1)` and the
`S(t)` bound.

2. Upper-bound negative shifted moments of `zeta` using a prime-polynomial
lower bound for `log |zeta|` and exponential truncations.

3. Bound the resulting Dirichlet-polynomial moments over zeros using BFMT
Theorem 3.1, whose proof is powered by the Landau-Gonek explicit formula.

## Zeta-Specific Inputs And EC Replacements

| BFMT input | Zeta-specific content | EC/newform replacement needed | verdict |
|---|---|---|---|
| RH | BFMT Theorem 1.1 assumes RH, p. 2. | Fixed-curve GRH for `L(E,s)` in normalized form, plus zeros counted on the central line. | Required hypothesis; not H1 closure. |
| Separated family `F` | Separation at scale `1/log T`; pair correlation only motivates density. | Define `F_E(T,c)` by nearest-neighbor spacing at least `c/log T`, excluding multiple zeros automatically. | Good-set theorem candidate. |
| Full zero family | BFMT explicitly warns that RH plus simplicity does not suffice, p. 3. | Need a reciprocal derivative budget on `F_E^c`; zero count is insufficient. | Main H1 blocker. |
| Derivative-shift comparison | Kirila/BFMT formula `(2.1)` relates `log |zeta'(rho)|` to `log |zeta(rho+1/log T)|` and nearby zeros. | `GL2-ShiftDerivativeComparison(E,c)`: for `gamma in F_E(T,c)`, prove `|L'_E(1+i gamma)|^(-1) <= exp(C_E logT/loglogT)|L_E(1+1/logT+i gamma)|^(-1)`. | Plausible named input. |
| `S(t)` bound | BFMT uses Littlewood's RH bound for the zeta argument, p. 3. | Need an argument-function bound for fixed `L(E,s)` strong enough to control local zero sums in the shifted derivative formula. | Named input; not supplied by BFMT. |
| Approximate functional equation | BFMT does not use a standard AFE as the main engine. It uses a lower bound for shifted `zeta` via prime polynomials, Lemma 2.3. | A GL2 AFE alone is not enough for reciprocal moments; need a GL2 lower-bound/Harper-Soundararajan analogue for `log |L_E|`. | AFE route alone is no-go. |
| Prime-polynomial lower bound | BFMT Lemma 2.3 uses prime coefficients `b(p;Delta)` and deterministic error terms, p. 6. | Replace prime weights by normalized newform coefficients and prove the same one-sided lower bound with prime-square, conductor, gamma, and bad-prime terms controlled. | Major source gap. |
| Mollifier length | BFMT's Dirichlet polynomials have effective support below `T^(1-o(1))`; see Propositions 2.5-2.7 and constraints before `(5.1)`. | Need the same length range for GL2 zero averages. Fixed conductor should not change the exponent target, but this must be proved in the GL2 mean-value input. | Named input. |
| Ratios conjecture | Not used in BFMT's proof of Theorem 1.1. It appears in the background literature only. | GL2 ratios conjectures may predict constants, but they do not give a rigorous H1 bound here. | Not a proof input. |
| Zero-density | Not a BFMT substitute; BFMT assumes RH. | Zero-density cannot replace GRH in the derivative-shift step and does not bound reciprocal derivatives on clustered zeros. | No-go for H1. |
| Pair correlation | BFMT uses Montgomery pair correlation only to motivate that `F` should have full density, p. 2. | Fixed-curve pair correlation would still only estimate excluded-zero counts. It gives no cap on `|L'_E|^(-1)` on `F_E^c`. | No-go for complement. |
| Gonek-type sums | BFMT Theorem 3.1 and Lemma 3.2 evaluate zero averages of Dirichlet polynomials using Landau-Gonek. | Need `GL2-LandauGonek-DPMV(E,theta)`: a zero-discrete mean-value theorem for fixed `L(E,s)` Dirichlet polynomials of length `T^(theta)`, `theta<1`. | Central missing theorem. |
| Arithmetic diagonal | Zeta diagonal is `N(T) sum |a_n|^2/n`; off-diagonal terms appear only when `m/n` is an integer prime power. | GL2 diagonal must use normalized coefficients and Rankin-Selberg-sized prime sums; off-diagonal must carry fixed-form von Mangoldt coefficients. | Doable only inside DPMV. |
| Bad primes/conductor | Zeta has no ramified Euler factors and conductor `1`. | Fixed `E` introduces finitely many bad primes and gamma/conductor constants. These should be lower-order but must be explicit. | Bookkeeping input. |
| Multiple zeros | BFMT's `F` excludes repeated ordinates; `J_-k` is only defined for simple zeros. | H1 simple-zero sum can ignore nonsimple zeros only if multiple-zero residues are separately retained or killed by the finite-box theorem. | Outside BFMT good set. |

## Required EC-BFMT Hypothesis Package

The separated-good-set theorem follows from the following named package. None
is promoted here.

### `GL2-ShiftDerivativeComparison(E,c)`

For all simple zeros `rho_E=1/2+i gamma` of `mathcal L_E` with
`gamma in F_E(T,c)`,

```text
log |mathcal L'_E(rho_E)|^(-1)
  <= log |mathcal L_E(rho_E+1/log T)|^(-1)
     + O_E,c(log T/log log T).
```

This is the fixed-curve analogue of BFMT Lemma 2.1. It must be proved from a
Hadamard/Kirila formula plus a fixed-curve argument-function estimate. It is
local and only handles separated zeros.

### `GL2-LogLowerBound(E,k,theta)`

For `sigma=1/2+1/log T`, prove a one-sided lower bound for
`log |mathcal L_E(sigma+i gamma)|` by short prime polynomials with normalized
coefficients, suitable for the BFMT exponential-truncation decomposition.

The theorem must explicitly handle:

```text
prime terms,
prime-square terms,
fixed bad-prime Euler factors,
gamma/conductor constants,
all deterministic error terms.
```

This replaces BFMT Lemmas 2.3-2.4.

### `GL2-LandauGonek-DPMV(E,theta)`

For every Dirichlet polynomial `A(s)=sum_{n<=x} a_n n^{-s}` with
`x<=T^(theta)` and `theta<1` in the BFMT range, prove a zero-discrete
mean-value formula of the schematic form

```text
sum_{0<gamma_E<=T} |A(rho_E)|^2
  = N_E(T) sum_{n<=x} |a_n|^2/n
    + explicit fixed-form off-diagonal
    + O_E(x (log xT)^A sum_{n<=x} |a_n|^2/n).
```

The off-diagonal must be strong enough to reproduce BFMT Propositions 2.5,
2.6, and 2.7 with GL2 coefficients. This is the central missing theorem.

### `GL2-ArithmeticDiagonal(E)`

The BFMT propositions need prime-sum evaluations matching the zeta powers of
`log log T`. For fixed `E`, the replacement must prove the exact diagonal sizes
for normalized coefficients on all BFMT prime blocks, with bad primes removed
or absorbed into constants.

This is not just cosmetic: wrong diagonal normalization changes the exponent in
the final `T^(1+delta)` estimate.

## Conditional Separated-Zero Theorem

Under the four hypotheses above, the BFMT proof adapts to fixed `E` as follows.

Let

```text
F_E(T,c) = {gamma in (T,2T] :
  L(E,1+i gamma)=0 is simple and
  |gamma-gamma'| >= c/log T for every other zero ordinate gamma'}.
```

Then for every `delta>0`,

```text
sum_{gamma in F_E(T,c)} |L'_E(1+i gamma)|^(-1)
  <<_{E,c,delta} T^(1+delta).
```

Proof transfer:

1. Apply `GL2-ShiftDerivativeComparison(E,c)` to replace each reciprocal
   derivative by the reciprocal shifted value times `exp(O(logT/loglogT))`.
2. Use `GL2-LogLowerBound(E,k,theta)` with `k=1/2` to dominate reciprocal
   shifted values by BFMT-style truncated exponentials.
3. Expand the truncated exponentials into Dirichlet polynomials with total
   support below `T^(1-o(1))`.
4. Apply `GL2-LandauGonek-DPMV(E,theta)` and `GL2-ArithmeticDiagonal(E)` to
   reproduce BFMT's Propositions 2.5-2.7.
5. Use BFMT's parameter choices from Section 5. At `k=1/2`, the final exponent
   is `T^(1+delta)`.

This is a theorem candidate only after the named GL2 inputs are proved and
source-checked.

## Why This Does Not Close H1

H1 rank one needs

```text
R_E,1(T) =
sum_{T<|gamma|<=2T, simple} |L'_E(1+i gamma)|^(-1)
= o(T^2).
```

The separated theorem only gives

```text
sum_{gamma in F_E(T,c)} |L'_E(1+i gamma)|^(-1)=o(T^2).
```

The missing term is

```text
B_E(T,c)=
sum_{gamma notin F_E(T,c), simple} |L'_E(1+i gamma)|^(-1).
```

BFMT gives no mechanism for `B_E(T,c)`. A conjectural pair-correlation count
for `F_E^c` would still not control `B_E(T,c)`, because rare clustered zeros
are exactly where `|L'_E|` can be very small. This is the same obstruction
identified in Wave 2: spacing/count information is not a reciprocal tail bound.

## No-Go Boundaries

- `Ratios conjecture`: prediction only here; not a rigorous substitute for
  `GL2-LandauGonek-DPMV` or the complement budget.
- `Pair correlation`: can motivate density of `F_E`, but cannot bound
  reciprocal derivatives on `F_E^c`.
- `Zero density`: cannot replace GRH in the BFMT derivative-shift comparison
  and cannot cap small derivatives.
- `Simplicity`: simple zeros may still have arbitrarily small derivatives.
- `Approximate functional equation`: useful for values, not enough for a
  negative shifted moment upper bound without one-sided log control.
- `H2 branch damping`: irrelevant to H1 reciprocal poles and not used.

## Next Exact Target

Do not search broadly. Prove or source-kill this named theorem:

```text
GL2-LandauGonek-DPMV(E,theta)
```

with the exact coefficient ranges needed for BFMT Propositions 2.5-2.7. If it
fails, the BFMT adaptation is dead even on separated zeros. If it succeeds, the
next target is the independent bad-set theorem:

```text
EC-BFMT-BadSetBudget(E,c):
B_E(T,c)=o(T^2).
```

Only the pair of separated theorem plus bad-set budget can close rank-one H1.

## Verification Notes

- Top-level status is `RIGOROUS_REDUCTION`.
- No theorem is promoted.
- External theorem claims are restricted to the BFMT source packet above.
- Analytic rank only.
- No Koyama correspondence or email draft touched.
- No H2 branch damping used as H1 reciprocal-pole damping.
