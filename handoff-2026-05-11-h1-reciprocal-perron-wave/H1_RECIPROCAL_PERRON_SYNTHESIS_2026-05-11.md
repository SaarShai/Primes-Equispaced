---
schema_version: 1
title: "H1 reciprocal Perron synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.86
sources:
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md
tags: [ec-ndc, h1, reciprocal-perron, smoothing, synthesis]
---

# H1 Reciprocal Perron Synthesis

No theorem was promoted.

The H1 wave closed the central local algebra and sharply mapped the obstruction.
The exact pointwise H1 input remains literature-blocked because the offcentral
reciprocal-residue aggregate needs bounds on `1/L'(rho)` or higher Laurent
coefficients at zeros of `L(E,s)`.

## Result Table

| Slot | File | Status | Decision |
|---|---|---|---|
| Central polynomial | `H1_CENTRAL_POLYNOMIAL.md` | `RIGOROUS_REDUCTION` | Central residue algebra closed once Perron representation is granted. |
| Offcentral aggregate | `H1_OFFCENTRAL_RESIDUE_AGGREGATE.md` | `RIGOROUS_REDUCTION` | Bounded simple residues suffice for positive rank, not rank zero. |
| Multiple-zero/rank-zero | `H1_MULTIPLE_ZERO_RANK0_NOGO.md` | `NO_GO` | Rank zero and `m>=r+1` multiple zeros block pointwise constant limits. |
| Fallback modes | `H1_AVERAGED_OSCILLATORY_FALLBACK.md` | `RIGOROUS_REDUCTION` | Honest alternatives are oscillatory profile or product-level averaging. |
| Source audit | `H1_SOURCE_AUDIT.md` | `LITERATURE_BLOCKED` | No checked source closes fixed-curve H1 reciprocal Perron. |
| Referee | `H1_ADVERSARIAL_REFEREE.md` | `NO_GO` | No H1/EC smoothing promotion. |

## What Actually Closed

For

```text
c_E,W(K) = (1/(2 pi i)) int K^z W_hat(z)/L(E,1+z) dz,
u = log K,
r = ord_{s=1}L(E,s),
```

the central residue polynomial is

```text
Q_r(u) = Res_{z=0} e^(uz) W_hat(z)/L(E,1+z).
```

If `W_hat(z)=w_(-1)/z+O(1)`, then the leading coefficient is

```text
w_(-1) / L^(r)(E,1).
```

For the normalized kernels used in the EC smoothing work, `w_(-1)=1`, so the
leading term is

```text
u^r / L^(r)(E,1).
```

The apparent `r!/L^(r)(E,1)` is the Laurent coefficient of `1/L(E,1+z)`;
the coefficient of `u^r` in the Perron residue gains the cancelling `1/r!`
from `e^(uz)`.

## Main Obstruction

For a simple offcentral zero `rho=1+i gamma`,

```text
Res_{z=i gamma} e^(uz) W_hat(z)/L(E,1+z)
 = e^(i gamma u) W_hat(i gamma)/L'(rho).
```

There is no H2-style `1/u` loss. Smooth `W` damps high `|gamma|`, but it does
not control fixed low zeros or the reciprocal derivative.

For positive analytic rank `r>=1`, pointwise fixed-curve composition only needs

```text
Z_c(u)+E_c(u)=o(u^r),
```

so a bounded simple-zero aggregate is enough. For rank zero, bounded
offcentral residues remain main-scale almost-periodic terms; pointwise
constant stabilization fails unless they vanish, cancel, are retained
explicitly, or are averaged in a declared product-level theorem.

For an offcentral zero of multiplicity `m`, H1 can produce

```text
e^(i gamma u) u^(m-1)
```

times a nonzero coefficient. After multiplying by the H2 normalization
`u^(-r)`, any effective degree `m-1>=r` is constant-scale or worse.

## Source State

The source audit found adjacent inputs but no closure:

- Perron/Mellin background exists, but not the exact fixed-kernel H1 contour
  shift.
- EC zero counting supports pure multiplicity-weight sums, not
  `1/L'(rho)` sums.
- Checked sources do not prove all offcentral zeros are simple or bounded
  multiplicity for a fixed EC/GL(2) L-function.
- Checked sources do not provide the needed fixed-curve reciprocal-derivative
  bounds or moments.

Thus the exact H1 theorem is `LITERATURE_BLOCKED`, not false.

## Claim-Safe Next Targets

Pointwise positive-rank target:

```text
c_E,W(e^u) = Q_r(u) + o(u^r),     r>=1,
```

after proving the H1 contour shift, reciprocal-residue control, and tails.

Rank-zero target:

```text
c_E,W(e^u) = Q_0 + Z_c(u) + o(1),
```

with `Z_c` retained, killed by a kernel/cancellation theorem, or averaged.

Product-level averaged target:

```text
A_U [c_E,W(e^u) P_E,W(e^u)] -> C_E,W
```

where the averaging is proved for the product itself. Averaged `log P` alone
does not imply pointwise or arithmetic-average stabilization of `c_E,W P_E,W`.

## Do Not Promote Unless

- H1 has its own reciprocal-pole theorem; do not import H2 branch damping.
- Reciprocal derivative/Laurent coefficient control is proved or sourced.
- Rank zero is separated.
- Multiple offcentral zeros are ruled out, controlled, retained, or averaged.
- H1 and H2 use the same pointwise, oscillatory, or averaged mode.
- Exact Agent-3 local factors and analytic rank conventions remain in force.
- No cross-curve universality, BSD evidence, or closed EC smoothing claim is made.
