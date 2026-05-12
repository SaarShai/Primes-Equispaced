---
schema_version: 1
title: "Agent 04 EC-BFMT Bad-Set Inverse-Gap Budget"
date: 2026-05-11
agent: "Top-10 Challenge Wave Agent 04"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.88
tags: [top10-challenge, h1, ec-bfmt, bad-set, inverse-gap, pair-correlation, reciprocal-derivative]
---

# Agent 04 EC-BFMT Bad-Set Inverse-Gap Budget

status: `RIGOROUS_REDUCTION`

## Verdict

`EC-BFMT-BadSetBudget(E,c)` is not implied by any count-only spacing, pair-correlation,
local-statistics, zero-density, or simplicity route.

The clean theorem is:

```text
local cluster minimum modulus
+ inverse-product-distance layer cake
=> EC-BFMT-BadSetBudget(E,c).
```

For pair clusters, a GUE-strength close-pair law with exponent `beta>1` would
control the inverse-gap sum, but it still does not control
`|L'(E,rho)|^(-1)` without a local minimum-modulus lower bound. Known
pair-correlation/local-statistics theorems are zero-location theorems; they do
not include reciprocal derivative caps.

No EC theorem is promoted.

## Setup

Fix an elliptic curve `E/Q`. In the project normalization, offcentral critical
zeros are written

```text
rho = 1 + i gamma.
```

For a dyadic shell, set

```text
S_E(T) = {simple zeros rho=1+i gamma : T<|gamma|<=2T},
X_rho  = |L'(E,rho)|^(-1).
```

Use complex zero distance unless GRH is explicitly assumed. Define the separated
BFMT good set

```text
F_E(T,c) = {rho in S_E(T) :
            dist(rho, Z_E\{rho}) >= c/log T}.
```

The BFMT bad set is

```text
B_E(T,c) = S_E(T) \ F_E(T,c).
```

The target is

```text
EC-BFMT-BadSetBudget(E,c):
  sum_(rho in B_E(T,c)) X_rho = o(T^2).
```

Actual multiple zeros are not in `S_E(T)`. They remain under the separate H1
Laurent/effective-degree rules.

## Source-Checked Anchors

Source workspace:

```bash
/tmp/agent04-ec-bfmt-badset-sources-20260511
```

Extractor:

```bash
curl -L --fail -s -o xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac-4.06.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -v
```

`pdftotext version 4.06`.

Fetches:

```bash
curl -L --fail -s -o bfmt.pdf https://arxiv.org/pdf/2310.03949
curl -L --fail -s -o rudnick_sarnak2.pdf \
  https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf
curl -L --fail -s -o montgomery_paircor.pdf \
  https://public.websites.umich.edu/~hlm/paircor1.pdf
curl -L --fail -s -o sheth_ec_zero_count.pdf https://arxiv.org/pdf/2312.05236
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt.pdf
393cd6ad3a61036070ed7b86113de5dd1bb033b47eec8998fb9597bb091c13c7  rudnick_sarnak2.pdf
78f0e34113c331ab8e52fdf6f2fdc5c7a57bc5c59de68c01d1843339dc352b5b  montgomery_paircor.pdf
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_zero_count.pdf
```

Checked anchors:

1. BFMT, arXiv:2310.03949, PDF p. 1 abstract and p. 2 Theorem 1.1. Quote
   anchor: "conditional upper bounds for negative discrete moments". Use:
   zeta has a separated-zero negative derivative moment theorem; the excluded
   bad-set count is only motivated by pair correlation.

2. BFMT, PDF p. 2, lines around the separated family `F`. Use: Montgomery pair
   correlation is invoked to estimate excluded-zero counts, not derivative
   sizes.

3. Rudnick-Sarnak, PDF p. 4-5, Theorems 1.1-1.2. Quote anchor:
   "n-level correlations of the zeros are GUE". Use: fixed primitive
   L-functions have local correlation theorems under stated restrictions, but
   these are correlation sums over zero locations.

4. Montgomery, PDF p. 4. Quote anchor: "pair correlation function of the zeros".
   Use: zeta pair-correlation/simplicity context is count/statistical, not a
   reciprocal derivative theorem.

5. Sheth, arXiv:2312.05236, PDF p. 13, Theorem 3.1. Quote anchor:
   "number of zeros". Use:

   ```text
   N_E(t) = alpha_E t(log t+c)/pi + O(log t),
   ```

   hence `#S_E(T) <<_E T log T`.

## Main Conditional Theorem

### Cluster Product-MinMod Theorem

For each `rho in B_E(T,c)`, suppose there is a radius

```text
0 < R_rho <= A/log T
```

and a finite cluster

```text
C_rho = {rho=rho_0, rho_1, ..., rho_(k_rho-1)}
       = Z_E cap {|s-rho| < R_rho}
```

such that `|s-rho|=R_rho` contains no zero and

```text
m_rho := min_(|s-rho|=R_rho) |L(E,s)| > 0.
```

Define

```text
D_rho = product_(a=1)^(k_rho-1) |rho-rho_a|,
```

with `D_rho=1` if `k_rho=1`.

If

```text
sum_(rho in B_E(T,c))
  R_rho (2R_rho)^(k_rho-1) / (m_rho D_rho)
  = o(T^2),
```

then

```text
EC-BFMT-BadSetBudget(E,c)
```

holds.

Proof. In the disk,

```text
L(E,s) = product_(a=0)^(k_rho-1) (s-rho_a) h_rho(s),
```

where `h_rho` is holomorphic and nonvanishing. On `|s-rho|=R_rho`,

```text
product_(a=0)^(k_rho-1) |s-rho_a|
  <= R_rho (2R_rho)^(k_rho-1).
```

Therefore

```text
|h_rho(s)| >= m_rho / (R_rho (2R_rho)^(k_rho-1))
```

on the boundary. The maximum principle applied to `1/h_rho` gives the same
lower bound at the center. Since

```text
L'(E,rho) = D_rho h_rho(rho),
```

we get

```text
X_rho <= R_rho (2R_rho)^(k_rho-1)/(m_rho D_rho).
```

Summing proves the theorem.

## Pair Layer Cake

For pair clusters (`k_rho=2`), write

```text
d_rho = min_(rho' != rho) |rho-rho'|.
```

Assume a uniform local certificate

```text
R_rho <= A/log T,
m_rho >= h(T)/T,        h(T)->infinity.
```

Then

```text
X_rho <= 2A^2 T / (h(T)(log T)^2 d_rho).
```

Let

```text
P_T(delta) = #{rho in B_E(T,c) : d_rho <= delta}.
```

Because `d_rho <= c/log T` on the bad set,

```text
sum_(rho in B_E(T,c)) 1/d_rho
 <= (log T/c) P_T(c/log T)
    + int_(log T/c)^infinity P_T(1/u) du.
```

Thus the pair-cluster bad budget follows from the exact inverse-gap condition

```text
(T/(h(T)(log T)^2))
  [ (log T/c) P_T(c/log T)
    + int_(log T/c)^infinity P_T(1/u) du ]
  = o(T^2).
```

Equivalently,

```text
sum_(rho in B_E(T,c)) 1/d_rho
  = o(h(T) T (log T)^2).
```

### GUE-Strength Count Corollary

If, uniformly for `0<delta<=c/log T`,

```text
P_T(delta) <<_E T log T (delta log T)^beta
```

with `beta>1`, then

```text
sum_(rho in B_E(T,c)) 1/d_rho <<_E T (log T)^2.
```

Together with `m_rho >= h(T)/T`, this gives

```text
sum_(rho in B_E(T,c)) X_rho <<_E T^2/h(T)=o(T^2).
```

This is the sharp way pair-correlation-style input can help: it supplies an
inverse-gap count, and the local minimum modulus supplies the reciprocal cap.
The count input alone does not touch `X_rho`.

## Higher Cluster Product Layers

For clusters of size `k>=3`, set

```text
Y_rho = 1 / D_rho,
M_k(T;V) = #{rho in B_E(T,c) : k_rho=k, Y_rho>V}.
```

The exact product-distance layer cake is

```text
sum_(rho:k_rho=k) Y_rho
  = int_0^infinity M_k(T;V) dV.
```

Under the uniform certificate `R_rho<=A/logT`, `m_rho>=h(T)/T`, the `k`-cluster
contribution is bounded by

```text
A(2A)^(k-1) T / (h(T)(log T)^k)
  * int_0^infinity M_k(T;V) dV.
```

So the sufficient and essentially exact condition is

```text
int_0^infinity M_k(T;V) dV
  = o(h(T) T (log T)^k).
```

Plain `k`-tuple or local-density counts are weaker. They bound how many
clusters exist, not how small the product of internal distances can be.

## Count-Only No-Go

Any theorem whose hypotheses mention only zero locations, counts, spacing,
pair correlation, n-level correlations, density, or simplicity cannot imply
`EC-BFMT-BadSetBudget(E,c)`.

Reason: those hypotheses are invariant under multiplying a local analytic model
by a nonzero scalar. The zero set and all local statistics stay fixed, while
every `L'(rho)` is scaled by that scalar and every `X_rho` by its inverse. Thus
the reciprocal sum can be made larger than `T^2` without changing any
count-only datum.

For the actual normalized elliptic-curve `L`-function the scalar is fixed, but
the logical obstruction remains: a proof cannot extract derivative lower
bounds from zero-location statistics alone. It must use at least one of:

```text
local boundary minimum modulus,
direct reciprocal-derivative tail,
weighted derivative moment upper bound,
arithmetic BFMT-style negative moment theorem on the bad set.
```

Known local-statistics results therefore do not imply `o(T^2)` by themselves.
Rudnick-Sarnak/Montgomery-type inputs can at most help prove the `P_T` or
`M_k` count side of the layer cakes. BFMT itself uses pair correlation only to
motivate density of the separated zeta family; it does not provide the EC
cluster reciprocal cap.

## Decision Table

| route | result | reason |
|---|---:|---|
| Close-pair count `P_T(delta)` only | `NO_GO` | No cap for `X_rho`. |
| Pair correlation / GUE local stats only | `NO_GO` | Location statistics, not derivative statistics. |
| Rudnick-Sarnak n-level correlations only | `NO_GO` | Correlation sums over zeros; no reciprocal derivative weights. |
| Simplicity proportion only | `NO_GO` | Simple zeros can still have tiny derivatives. |
| Pair count with `beta>1` plus `m_rho>=h/T` | sufficient | Gives inverse-gap sum and local reciprocal cap. |
| `k`-cluster count only | `NO_GO` | Product of internal distances may be arbitrarily small. |
| Product-distance layer cake plus min modulus | sufficient | Directly dominates `sum X_rho`. |
| Direct bad-set tail `int #{X>V}dV=o(T^2)` | sufficient | Equivalent to the desired budget. |

## Carry-Forward Input

The theorem input to carry forward is:

```text
EC-BFMT-ClusterProductBudget(E,c):
  For B_E(T,c), each clustered simple zero has a zero-centered local
  minimum-modulus certificate, and the resulting inverse-product-distance
  sum

    sum_(rho in B_E(T,c))
      R_rho (2R_rho)^(k_rho-1) / (m_rho D_rho)

  is o(T^2).
```

This implies `EC-BFMT-BadSetBudget(E,c)`.

If the separated BFMT adaptation is eventually closed, this remains the exact
independent complement input. Without it, the BFMT route stops at the separated
set.

## Verification Notes

Read requested context:

```text
HANDOFF.md
handoff-2026-05-11-breakthrough-wave-3/BREAKTHROUGH_WAVE_3_SYNTHESIS_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-3/AGENT03_SEPARATED_ZERO_RECIP_BUDGET_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-3/AGENT04_BAD_SET_COMPLEMENT_BUDGET_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-2/AGENT02_H1_NEAR_MULTIPLE_ZERO_BUDGET_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-3/AGENT01_GL2_BFMT_ADAPTATION_BLUEPRINT_2026-05-11.md
handoff-2026-05-11-breakthrough-wave-3/AGENT05_MINIMUM_MODULUS_LOCAL_FACTOR_2026-05-11.md
```

Checks:

```text
Allowed status used: RIGOROUS_REDUCTION.
External theorem claims source-checked with curl + pdftotext.
No theorem promoted.
Analytic rank only.
No H2 branch damping used as H1 reciprocal-pole damping.
No Koyama correspondence/email drafts touched.
Project-local ./te was absent; ../te doctor returned ok:false because this
folder lacks its own Token Economy config/start file.
```

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-top10-challenge-wave/AGENT04_EC_BFMT_BADSET_INVERSEGAP_BUDGET_2026-05-11.md
```
