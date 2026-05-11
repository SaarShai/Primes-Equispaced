---
schema_version: 1
title: "Agent 03 separated-zero reciprocal derivative budget"
date: 2026-05-11
agent: "Breakthrough Wave 3 Agent 03 -- Separated-Zero Theorem Candidate"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.87
tags: [breakthrough-wave-3, h1, separated-zeros, reciprocal-derivative, fixed-curve-gl2]
---

# Agent 03 Separated-Zero Reciprocal Budget

status: `RIGOROUS_REDUCTION`

## Verdict

No fixed-curve separated-zero theorem is promoted.

For a fixed elliptic curve `E/Q`, write the critical line in the project
normalization as `s=1+i gamma`, and set

```text
X_rho = |L'(E,rho)|^(-1),       rho=1+i gamma.
```

The separated good-set target is

```text
S_F(T;c) =
  sum_(rho in F_T(c)) X_rho
  = o(T^2),
```

where `F_T(c)` is a dyadic set of simple zeros with nearest-neighbor spacing at
least `c/log T`. For rank-one H1 this is useful only with the complement budget

```text
sum_(rho notin F_T(c), simple, T<|gamma|<=2T) X_rho = o(T^2).
```

What is proved here:

```text
separation + local boundary minimum modulus
  => S_F(T;c) = o(T^2).
```

What is not proved:

```text
separation alone => any H1-sized reciprocal derivative budget.
```

The exact live theorem is a fixed-curve GL2/EC BFMT-style separated negative
first moment, or an equivalent local minimum-modulus theorem.

## Definitions

Let `Z_E(T,2T)` be the noncentral zeros `rho=1+i gamma` with
`T<|gamma|<=2T`. Under RH/GRH, nearest-neighbor spacing can be read as ordinate
spacing. Unconditionally, ordinate spacing is insufficient; the local argument
below needs complex zero separation:

```text
dist(rho, Z_E\{rho}) >= c/log T.
```

Define

```text
F_T(c) = {rho in Z_E(T,2T):
          rho simple and dist(rho,Z_E\{rho}) >= c/log T}.
```

The rank-one H1 size target is `o(T^2)`, not merely pointwise finiteness.

## Source-Checked Inputs

Source workspace:

```bash
/tmp/agent03-separated-zero-sources-20260511
```

Extractor:

```bash
curl -L --fail -s -o xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac-4.06.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 ...
```

`pdftotext` reported version `4.06`.

Fetches:

```bash
curl -L --fail -s -o bfmt.pdf https://arxiv.org/pdf/2310.03949
curl -L --fail -s -o li_zaharescu.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
curl -L --fail -s -o sheth.pdf https://arxiv.org/pdf/2312.05236
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt.pdf
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011  li_zaharescu.pdf
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth.pdf
```

Used anchors:

1. Sheth, arXiv:2312.05236v4, PDF p. 13, Theorem 3.1. Quote anchor:
   "number of zeros". Display:

   ```text
   N_E(t) = alpha_E t(log t+c)/pi + O(log t).
   ```

   Consequence used here:

   ```text
   #Z_E(T,2T) <<_E T log T.
   ```

2. Bui-Florea-Milinovich, arXiv:2310.03949, PDF p. 1 abstract, quote anchor:
   "conditional upper bounds"; PDF p. 2, Theorem 1.1, equation (1.2). For zeta,
   RH plus their separated family gives

   ```text
   sum_(gamma in F) |zeta'(rho)|^(-2k) << T^(1+delta)
   ```

   in the `2k(1+epsilon)<=1` case and the stated second branch otherwise.
   With `k=1/2`, equation (1.2) gives `<< T^(1+delta)` on the separated
   zeta subfamily. This is model material only for EC.

3. BFMT, PDF p. 2, pair-correlation motivation before Theorem 1.1. Quote
   anchor: "Montgomery's Pair Correlation Conjecture". It is cited only as a
   zeta-model explanation that pair correlation counts excluded close pairs.

4. BFMT, PDF p. 1, equation (1.1), quote anchor: "random matrix theory model".
   For zeta, the RMT prediction for `J_-k` is

   ```text
   J_-k(T) asymp T (log T)^((k-1)^2).
   ```

   With `k=1/2`, this predicts `T(log T)^(1/4)` for the first reciprocal
   derivative moment. This is RMT-only, not a theorem for EC.

5. Li-Zaharescu, PDF p. 1 abstract, quote anchor: "lower bound for the second
   negative moment"; PDF p. 2, Theorem 1.1 equation (5), and Theorem 1.2
   equation (6). Use: adjacent/no-go. It gives lower negative-moment and
   extreme-small-value information, not an upper reciprocal budget.

## Proven Conditional Lemma

### Sep-MinMod Lemma

Assume:

1. `rho in F_T(c)` is simple.
2. For each `rho`, there is a radius

   ```text
   0 < r_rho <= c/(2 log T)
   ```

   such that `L(E,s)` has no zero in `0<|s-rho|<=r_rho`.
3. There is `h(T)->infinity` such that

   ```text
   min_(|s-rho|=r_rho) |L(E,s)|
     >= r_rho h(T) log T / T.
   ```

Then

```text
S_F(T;c) <<_E T^2 / h(T) = o(T^2).
```

Proof. Write

```text
L(E,s)=(s-rho)g_rho(s),       g_rho(rho)=L'(E,rho).
```

The zero-free punctured disk makes `g_rho` nonvanishing in `|s-rho|<=r_rho`.
On the boundary,

```text
|g_rho(s)| = |L(E,s)|/r_rho >= h(T) log T / T.
```

Apply the maximum principle to `1/g_rho`. Then

```text
|L'(E,rho)| = |g_rho(rho)| >= h(T) log T / T,
X_rho <= T/(h(T)log T).
```

By the zero-count input,

```text
#F_T(c) <= #Z_E(T,2T) <<_E T log T.
```

Therefore

```text
S_F(T;c) <= #F_T(c) T/(h(T)log T)
          <<_E T^2/h(T)
          = o(T^2).
```

This is a valid conditional implication, not a promoted EC theorem: the missing
input is the boundary minimum-modulus lower bound at each separated zero.

## Equivalent Tail Form

For

```text
M_F(T;V) = #{rho in F_T(c): X_rho > V},
```

the exact separated reciprocal budget is

```text
S_F(T;c)
  = int_0^infinity M_F(T;V) dV.
```

Since `M_F(T;V) <= #F_T(c) <<_E T log T`, the interval `0<V<=1`
contributes only `O_E(T log T)`. Thus

```text
S_F(T;c)=o(T^2)
```

is equivalent to

```text
int_1^infinity M_F(T;V) dV = o(T^2).
```

A source-closable theorem may therefore be stated either as Sep-MinMod or as
this layer-cake tail bound.

## Mode Split

### 1. Unconditional Mode

Result: reduction only.

Unconditional ordinate spacing among critical-line zeros does not imply a
zero-free complex disk; zeros off the line could lie inside the local circle.
Even full complex separation only supplies the disk. It does not lower-bound
the nonzero factor `g_rho(rho)`.

Abstract obstruction:

```text
zeros + spacing do not determine derivative sizes.
```

Multiplying a local analytic model by a tiny nonvanishing factor leaves the
zero set and separation unchanged while making all derivatives tiny. For a
fixed normalized L-function the multiplier is not free, but this shows exactly
which data spacing lacks: a lower bound for the nonzero local factor.

Unconditional sufficient theorem:

```text
EC-Sep-MinMod(E,c,h):
  every rho in F_T(c) has the Sep-MinMod certificate with h(T)->infinity.
```

Then `S_F(T;c)=o(T^2)` by the lemma.

Unconditional no-go:

```text
nearest-neighbor spacing alone => no H1 reciprocal budget.
```

### 2. RH/GRH Mode

Result: zeta model exists; fixed-curve EC theorem not source-closed.

Under RH/GRH, ordinate spacing `|gamma-gamma'|>=c/log T` does give a
zero-free disk of radius `<c/(2logT)` around `rho`, because all nontrivial zeros
lie on the critical line. This removes the geometric blocker but not the
minimum-modulus blocker.

The exact fixed-curve theorem needed is:

```text
EC-Sep-BFMT-1/2(E,c):
  For every delta>0,
  sum_(rho in F_T(c)) |L'(E,rho)|^(-1)
    <<_(E,c,delta) T^(1+delta).
```

This would be far stronger than H1 needs, since `T^(1+delta)=o(T^2)` for
fixed `delta<1`.

BFMT proves the analogous separated theorem for `zeta'(rho)` under RH, but the
checked source is zeta-only. Importing it to one fixed elliptic curve would
require a new GL2/newform proof: approximate functional equation, mollifier,
zero-repulsion bookkeeping, and arithmetic diagonal all have to be rebuilt.

RH/GRH alone is not enough in this packet.

### 3. Pair-Correlation Mode

Result: count-only pair correlation does not bound reciprocal derivatives.

A Montgomery-type pair-correlation theorem for `L(E,s)` could imply that the
close-pair complement

```text
B_T(beta) = {rho: nearest neighbor distance <= beta/log T}
```

has small cardinality, e.g.

```text
#B_T(beta) << beta^3 T log T
```

in the zeta cubic-repulsion model cited by BFMT. This only helps the
complement count. It gives no upper bound for `X_rho`.

For all simple zeros, pair correlation becomes useful only with a cap or tail:

```text
#B_T(beta) * C(T) = o(T^2),
X_rho <= C(T) for rho in B_T(beta),
```

or equivalently

```text
int_1^infinity #{rho in B_T(beta): X_rho>V} dV = o(T^2).
```

Thus pair-correlation mode still needs one of:

```text
EC-Sep-BFMT-1/2(E,c) on F_T(c),
EC-Sep-MinMod(E,c,h) on F_T(c),
EC-Bad-Recip(E,c) on the complement.
```

Pair correlation alone is `NO_GO` for H1.

### 4. RMT-Only Mode

Result: diagnostic only.

By the zeta RMT model cited in BFMT, the first reciprocal derivative moment
corresponds to `k=1/2` and has predicted size

```text
T (log T)^(1/4)
```

for a typical/full-density family. The fixed-curve EC analogue would be
`T polylog(T)`, hence safely `o(T^2)`.

This is useful as a plausibility check only. It supplies no theorem, no bad-set
tail, and no admissible H1 proof input.

## Theorem Inputs To Carry Forward

### Input A: separated BFMT analogue

```text
EC-Sep-BFMT-1/2(E,c):
  For fixed E/Q and c>0, for every delta>0,
  sum_(rho in F_T(c)) |L'(E,rho)|^(-1)
    <<_(E,c,delta) T^(1+delta).
```

### Input B: separated local minimum modulus

```text
EC-Sep-MinMod(E,c,h):
  There exists h(T)->infinity such that every rho in F_T(c)
  has a zero-free radius r_rho<=c/(2logT) and

    min_(|s-rho|=r_rho) |L(E,s)|
      >= r_rho h(T)logT/T.
```

### Input C: complement reciprocal budget

```text
EC-Bad-Recip(E,c):
  sum_(rho notin F_T(c), simple, T<|gamma|<=2T)
    |L'(E,rho)|^(-1)
  = o(T^2).
```

Then either

```text
Input A + Input C
```

or

```text
Input B + Input C
```

implies the analytic-rank-one H1 simple-zero reciprocal target:

```text
R_E,1(T)=o(T^2).
```

Actual multiple offcentral zeros remain outside this reciprocal-simple-zero
sum and must be handled by the Laurent/effective-degree branch. They are not
absorbed here.

## Decision Table

| route | decision | reason |
|---|---:|---|
| Full complex separation only | no-go | gives a disk, not `g_rho(rho)` lower bound |
| RH/GRH plus ordinate separation | reduction | gives the disk; still needs min-modulus or BFMT analogue |
| Sep-MinMod certificate | sufficient | proves `S_F(T;c)<<T^2/h(T)` |
| EC-Sep-BFMT-1/2 | sufficient if proved | would give `T^(1+delta)` on `F_T(c)` |
| Pair correlation only | no-go | counts close pairs; no reciprocal cap |
| Pair correlation plus bad reciprocal tail | sufficient for complement | exact condition is layer-cake `o(T^2)` |
| RMT prediction | diagnostic only | predicts `T polylog(T)`, but no theorem |
| Li-Zaharescu negative moment/small values | adjacent only | lower/existence direction, not upper reciprocal budget |

## Verification Notes

Read targeted context first:

```text
start.md
token-economy.yaml
L0_rules.md
L1_index.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3-plan.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT01_H1_DERIVATIVE_SOURCE_CLOSURE_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT02_H1_NEAR_MULTIPLE_ZERO_BUDGET_2026-05-11.md
```

Checks:

```text
./te doctor returned ok:true.
External theorem claims above use curl + pdftotext, short quotes, and page/equation anchors.
Analytic rank only.
No H2 branch damping used as H1 reciprocal-pole damping.
No Koyama correspondence or email drafts touched.
No broad wiki/raw archives loaded.
No theorem promoted.
```

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT03_SEPARATED_ZERO_RECIP_BUDGET_2026-05-11.md
```
