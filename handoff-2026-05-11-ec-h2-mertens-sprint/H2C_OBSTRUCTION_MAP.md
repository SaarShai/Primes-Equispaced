---
schema_version: 1
title: "H2-C obstruction map for smoothed EC Mertens product"
date: 2026-05-11
type: obstruction-map
tier: working
status: NO_GO
confidence: 0.72
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
  - handoff-2026-05-11-ec-smoothing-blockers/T2_STOCHASTIC_EULER_PRODUCT_MODEL.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py
  - koyama-shared/data/pari_authoritative_zeros.json
tags: [ec-ndc, h2, mertens, euler-product, obstruction]
---

# H2-C Obstruction Map

status: `NO_GO`

## Verdict

Do not promote the naive pointwise H2

```text
log P_E,W(K) = -rank(E) log log K + B_E,W + o(1)
```

for the exact Agent 3 product.

The coefficient `-rank(E)` is the expected central term only after a serious
GL(2) Mertens theorem. It is not forced by the local factors alone. For this
central-point EC product, noncentral zeros on `Re(s)=1` produce persistent
terms `K^(i gamma)` after smoothing. Smoothstep damps high `gamma`; it does not
make fixed low zeros decay in `K`. Thus the honest product-side theorem is
oscillatory unless one adds a zero-killing, zero-free, cancellation, or
log-averaging hypothesis.

The repaired shape is

```text
log P_E,W(K)
  = -r log log K + B_E,W + Z_E,W(log K) + o(1),
```

where `r=ord_{s=1} L(E,s)` and

```text
Z_E,W(u) = sum_{gamma != 0} c_E,W(gamma) exp(i gamma u)
```

is the noncentral-zero term. The naive H2 is the special case
`Z_E,W(log K)=o(1)`, which is not justified and is contradicted by the local
zero landscape unless all relevant coefficients vanish.

## Exact Product Under Audit

Agent 3 defines, for the same smoothstep weight used in T1/T2,

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)).
```

At good primes,

```text
A_p(1) = 1 - a_p/p + 1/p.
```

At bad primes,

```text
A_p(1) = 1 - a_p/p.
```

The script uses the real logarithm

```text
log P_E,W(K) = -sum_p W(p/K) log A_p(1).
```

For the three training curves the code records ranks

```text
37a1: 1, 11a1: 0, 389a1: 2.
```

Local zero data in `koyama-shared/data/pari_authoritative_zeros.json` lists
noncentral imaginary parts for `37a1`

```text
5.0031700140066587, 6.870391216954432, ...
```

and for `389a1`

```text
2.8760990712604652, 4.416896083665258, ...
```

So any pointwise H2 for these curves must explain why these zero frequencies
do not appear, not merely ignore them.

## Coefficient Audit

At a good prime write the Satake parameters as

```text
alpha_p + beta_p = a_p,     alpha_p beta_p = p.
```

Then

```text
-log(1 - a_p/p + 1/p)
  = a_p/p + (a_p^2 - 2p)/(2p^2) + R_p,
```

with

```text
sum_p W(p/K) R_p = C_tail,E,W + o(1)
```

under standard bounded-tail estimates, because the `m >= 3` local-log terms
are absolutely summable.

The quadratic term is not harmless:

```text
(a_p^2 - 2p)/(2p^2)
  = -1/(2p) + (a_p^2 - p)/(2p^2).
```

Thus the good-prime quadratic piece contains the universal drift

```text
-1/2 sum_p W(p/K)/p = -1/2 log log K + C_W + o(1),
```

plus a symmetric-square-type residual

```text
1/2 sum_p W(p/K) (a_p^2 - p)/p^2.
```

That residual must be proved to have a smoothed limit, or folded into an
explicit symmetric-square constant. It is part of `B_E,W`; it cannot be
dropped from the derivation.

Therefore the coefficient of `log log K` is not locally `-r`. It is

```text
coeff(sum_p W(p/K) a_p/p) - 1/2
```

after the symmetric-square residual is shown to be constant-scale. To get
`-r`, one needs the prime-linear Mertens input

```text
sum_p W(p/K) a_p/p
  = (1/2 - r) log log K + A_E,W + zero terms + o(1).
```

This is the real H2 theorem. It is equivalent to extracting the central zero
of `L(E,s)` while simultaneously controlling the quadratic/symmetric-square
piece. The Agent 3 local factor convention does not prove it.

## Zero-Term Obstruction

For GL(1) products at `s=1`, offcritical zeros give decaying terms after
partial summation. Here the central point is `s=1` and the noncentral EC zeros
are also on `Re(s)=1` in the local data/conjectural picture.

A simple zero

```text
rho = 1 + i gamma,   gamma != 0,
```

contributes to the prime-linear product side a term of the form

```text
c_E,W(gamma) K^(i gamma),
```

where `c_E,W(gamma)` is a Mellin/partial-summation coefficient depending on
the smoothing kernel and the residue of the logarithmic derivative. Its exact
normalization belongs in H2-A/H2-B, but its size is constant in `K` whenever
the coefficient is nonzero.

Smoothstep helps only by making `c_E,W(gamma)` decay as `|gamma|` grows. It
does not shrink the first few fixed zero frequencies. A higher smoothness
kernel would improve convergence of the zero sum, not remove the low-zero
oscillation.

Consequences:

- For `r >= 1`, subtracting `-r log log K` still leaves bounded oscillations,
  so a constant `B_E,W + o(1)` is not the right pointwise target.
- For `r = 0`, the central term is already constant-scale; any noncentral zero
  oscillation is the same size as the proposed limit. Rank zero is therefore
  harder, not automatic.
- Multiplicity of a product-side zero changes the logarithmic-derivative
  residue by the multiplicity. Unlike the reciprocal Perron side in T1, it
  does not by itself create `(log K)^(m-1)` terms in `log P`; the obstruction
  here is persistent oscillation.

## Constants That Must Be Present

Even after the `-r log log K` coefficient is proved, `B_E,W` is not a free
universal constant. It must absorb at least:

```text
log lambda_E,      lambda_E = L^(r)(E,1)/r!
```

from the central Taylor expansion;

```text
C_W
```

from the smoothed Mertens kernel;

```text
C_sym2,E,W
```

from the good-prime quadratic/symmetric-square residual;

```text
C_tail,E,W
```

from the absolutely convergent `m >= 3` local-log tail;

```text
C_bad,E = -sum_{p | N_E} log(1 - a_p/p)
```

once `K` is larger than all bad primes.

The finite bad-prime part is a curve constant. It cannot repair within-curve
drift on the current grid once all bad primes are already below the first
checkpoint, matching the earlier finite bad-prime no-go.

## Sign And Branch Check

For the Agent 3 finite product there is no numerical branch ambiguity:

- at good primes, `1 - a_p/p + 1/p = #E(F_p)/p > 0`;
- at bad primes in the script convention, `1 - a_p/p > 0`;
- the script computes `log_P = -sum log(inv_p1) * weight`, hence the central
  zero of order `r` predicts decay of the product and the sign `-r`.

Analytically, a proof must not take a global logarithm through zeros without a
branch convention. Use the real branch from `s=1+sigma`, `sigma>0`, or work
with `-L'/L` and integrate back. If one switches from inverse local factors to
local factors, the sign of the coefficient flips.

## Exact Repair Hypotheses

The naive H2 can be repaired in three honest ways.

### Repair A: oscillatory H2

Replace H2 by:

```text
log P_E,W(K)
  = -r log log K + B_E,W + Z_E,W(log K)
    + O((log K)^(-eta)).
```

Required hypotheses:

1. `L(E,s)` has central order `r` and a positive right-hand Taylor coefficient
   `lambda_E`.
2. The smoothed prime-linear explicit formula holds at `s=1`, with all
   noncentral zeros on `Re(s)=1` contributing the explicit Fourier series
   `Z_E,W`.
3. The coefficients `c_E,W(gamma)` are summable enough for the stated kernel;
   smoothstep plausibly gives high-zero damping, but this still needs proof.
4. The quadratic residual
   `1/2 sum W(p/K)(a_p^2-p)/p^2` has a limit with error
   `O((log K)^(-eta))`.
5. The `m >= 3` good-prime local-log tail and finite bad-prime factors have
   limits with compatible errors.

This is the best pointwise theorem target.

### Repair B: averaged H2

State H2 only after averaging in `u=log K`, for example

```text
1/T integral_T^(2T)
  (log P_E,W(exp u) + r log u) du
  -> B_E,W.
```

Required hypotheses:

1. The oscillatory expansion in Repair A holds.
2. The zero frequencies have no zero-frequency leakage other than the central
   zero already represented by `-r log log K`.
3. The zero series may be integrated termwise or controlled in mean square.

This kills `exp(i gamma u)` terms by averaging, but it is not the pointwise H2
used in T1.

### Repair C: zero-killed pointwise H2

Keep the original pointwise shape only under the explicit suppression
hypothesis

```text
Z_E,W(log K) = o(1).
```

This requires at least one of:

- no noncentral zeros of `L(E,s)` on `Re(s)=1`;
- `c_E,W(gamma)=0` for every noncentral zero frequency;
- a proved cancellation theorem for the full noncentral zero aggregate.

This is too strong for the present EC data. The local zero file already gives
noncentral frequencies for `37a1` and `389a1`; the smoothstep kernel was not
designed to vanish at them.

## Decision For The Sprint

Use `NO_GO` for naive H2 as written.

The coefficient `-rank(E)` may be the correct central coefficient for the
exact Agent 3 product, but only inside an explicit formula that also contains
the noncentral zero Fourier term and the symmetric-square/good-prime
constants. The theorem package should not state `B_E,W + o(1)` pointwise
unless it adds Repair B or Repair C. For fixed-curve stabilization of
`c_E,W(K) P_E,W(K)`, T1 must either include matching zero terms on both sides
and prove cancellation, or weaken the conclusion to an averaged statement.
