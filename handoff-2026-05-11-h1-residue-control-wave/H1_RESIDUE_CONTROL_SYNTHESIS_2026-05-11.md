---
schema_version: 1
title: "H1 residue-control synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.87
sources:
  - handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_PRODUCT_AVERAGE_THEOREM.md
  - handoff-2026-05-11-h1-residue-control-wave/H2_SYM2_SOURCE_CLOSURE.md
  - handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
  - handoff-2026-05-11-h1-residue-control-wave/RESIDUE_CONTROL_ADVERSARIAL_REFEREE.md
tags: [ec-ndc, h1, residue-control, smoothing, synthesis]
---

# H1 Residue-Control Synthesis

No EC smoothing theorem was promoted.

The wave did produce theorem-grade scaffolding. The H1 side is now reduced to
an exact finite-box reciprocal-Perron identity plus explicit residue-control
conditions. Positive analytic rank has a clean conditional closure criterion;
rank zero has an honest oscillatory profile; and product-level averaging has a
precise diagonal-constant formulation. The remaining obstruction is not
bookkeeping. It is the fixed-curve reciprocal derivative/Laurent problem at
offcentral zeros.

## Result Table

| Slot | File | Status | Decision |
|---|---|---|---|
| Source hunt | `H1_RECIP_DERIVATIVE_SOURCE_HUNT.md` | `LITERATURE_BLOCKED` | Checked sources do not close fixed-curve `1/L'(rho)` or Laurent control. |
| Contour shift | `H1_CONTOUR_SHIFT_THEOREM.md` | `RIGOROUS_REDUCTION` | Finite-box identity and residue formulas are explicit; tails remain assumptions. |
| Positive rank | `H1_POSITIVE_RANK_CLOSURE.md` | `RIGOROUS_REDUCTION` | `Z_c(u)+I(u)=o(u^r)` is exact; bounded simple residues suffice for `r>=1`. |
| Rank zero | `H1_RANK_ZERO_OSCILLATORY_PROFILE.md` | `RIGOROUS_REDUCTION` | Claim-safe target is `Q_0+Z_c(u)+o(1)`, not a constant. |
| Product average | `H1_PRODUCT_AVERAGE_THEOREM.md` | `RIGOROUS_REDUCTION` | Arithmetic log-Cesaro average of the product has a conditional diagonal constant. |
| H2/Sym2 closure | `H2_SYM2_SOURCE_CLOSURE.md` | `RIGOROUS_REDUCTION` | Local H2 algebra is closed; S1 branch and Sym2 finite part remain proof/source blocked. |
| Kernel filtering | `KERNEL_ZERO_FILTERING.md` | `RIGOROUS_REDUCTION` | Finite signed filtering is diagnostic; it does not prove asymptotic stabilization. |
| Referee | `RESIDUE_CONTROL_ADVERSARIAL_REFEREE.md` | `NO_GO` | Do not promote the combined H1/H2 theorem. |

## What Actually Advanced

The finite-box H1 identity is now the canonical scaffold:

```text
c_E,W(e^u)
 = Q_E,W(u)
   + sum_{rho != 1, |Im(rho)|<T} R_rho(u)
   + vertical/horizontal/truncation errors.
```

The central polynomial is closed locally:

```text
Q_E,W(u)=Res_{z=0} e^(uz) W_hat(z)/L(E,1+z),
Q_E,W(u)=w_-1 u^r/L^(r)(E,1)+O(u^(r-1)).
```

For normalized kernels, `w_-1=1`.

For a simple offcentral zero `rho=1+i gamma`,

```text
R_rho(u)=e^(i gamma u) W_hat(i gamma)/L'(E,1+i gamma).
```

For a zero of multiplicity `m`, the residue is

```text
e^(i gamma u) times a polynomial in u of degree at most m-1,
```

lowered by kernel zeros or coefficient cancellations.

## Positive Rank

For analytic rank `r>=1`, the exact H1 requirement is:

```text
Z_c(u)+I(u)=o(u^r),
```

where `Z_c` is the offcentral reciprocal-residue aggregate and `I` is the
post-residue contour remainder.

A clean sufficient condition is:

```text
all effective offcentral residue degrees are < r,
all lower-degree coefficient aggregates are bounded or absolutely convergent,
and the contour tail is o(u^r).
```

In the all-simple-zero case, this reduces to:

```text
sum_{gamma != 0} |W_hat(i gamma)/L'(E,1+i gamma)| < infinity.
```

That condition would imply the needed positive-rank H1 pointwise input, but it
is not sourced or proved.

## Rank Zero

For analytic rank zero, simple offcentral residues are main-scale terms. The
honest target is:

```text
c_E,W(e^u)
 = 1/L(E,1)
   + sum_{gamma != 0}
       W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)
   + o(1),
```

with a declared convergence mode, such as uniform convergence of symmetric
truncations after an explicit tail bound.

A pointwise constant limit is forbidden unless those nonzero-frequency
residues vanish, cancel, are filtered with tail control, or are replaced by an
averaged/product theorem.

## Product-Average Fallback

The claim-safe averaged fallback averages the product itself:

```text
A_U[c_E,W(e^u) P_E,W(e^u)]
 = (1/U) int_U^(2U) c_E,W(e^u) P_E,W(e^u) du.
```

If H1 has mean-scale coefficients

```text
H_c(u)=q_r + sum_gamma h_gamma e^(i gamma u),
```

and H2 has

```text
P_E,W(e^u)=e^(B_H2) u^(-r) G(u)(1+o_mean(1)),
G(u)=sum_eta d_eta e^(i eta u),
```

then the conditional diagonal constant is:

```text
C_E,W^prod
 = e^(B_H2) (q_r d_0 + sum_gamma h_gamma d_(-gamma)).
```

This is a different theorem mode. It cannot be derived from averaged `log P`
alone and cannot be mixed with a pointwise H1 statement.

## Source State

The source hunt checked adjacent fixed-curve GL2/simple-zero and
reciprocal-derivative material. It found:

- many-simple-zero results, not all-simple-zero or bounded multiplicity;
- negative-moment and mollified templates, not upper bounds for the fixed H1
  residue aggregate;
- no theorem controlling higher Laurent coefficients at multiple zeros;
- no theorem proving the direct fixed-weight sum
  `sum W_hat(i gamma)e^(i gamma u)/L'(1+i gamma)`.

Thus positive-rank pointwise closure remains `LITERATURE_BLOCKED`.

## H2 Pairing

The H2 side is coherent only as a matched conditional package. The exact local
expansion must retain:

```text
S_1,W, S_sym,W, M_good,W, R_ge3,W, B_bad,E,W.
```

The local algebra gives the intended `-r log log K` coefficient only when the
S1 and Sym2 conventions are paired correctly. But the exact endpoint-smoothed
S1 branch theorem and good-prime Sym2 finite-part theorem remain unclosed.

## Kernel Filtering

Finite signed kernel filtering can kill finitely many named low zeros by
imposing

```text
W_hat(i gamma_j)=0.
```

This is useful diagnostically. It does not prove fixed-kernel asymptotic
stabilization because the unfiltered reciprocal-residue tail remains
uncontrolled. Positive kernels and infinite filtering require separate
feasibility and entire-function arguments.

## Claim-Safe Statement

Allowed:

```text
The EC smoothing route has been reduced to matched H1 and H2 conditional
packages. H1 has an exact finite-box residue scaffold, positive-rank closure
criteria, a rank-zero oscillatory profile, and a product-average fallback.
The decisive unresolved analytic input is fixed-curve reciprocal
derivative/Laurent control at offcentral zeros.
```

Forbidden:

```text
The EC smoothing theorem is proved.
Smoothing alone stabilizes H1.
Rank-zero pointwise constants follow from smoothing.
H2 branch damping transfers to H1 reciprocal poles.
Many simple zeros means all offcentral zeros are simple.
```

## Best Next Move

The next high-leverage task is not more local algebra. It is a new proof
attempt for an H1 reciprocal-residue estimate, modelled on the
Li-Zaharescu-style mollified contour method but converted into an upper-bound
theorem for the fixed H1 weight:

```text
W_hat(i gamma) e^(i gamma u).
```

The theorem must be uniform in `u`, dyadically summable against Mellin decay,
and explicit about exceptional multiple zeros. If that fails, the most honest
paper path is the rank-zero oscillatory profile plus product-level averaged
fallback.

## Do Not Promote Unless

- The exact H1 contour shift and tails are proved for the same fixed kernel.
- `1/L'(rho)` and higher Laurent coefficients are controlled, or the theorem
  retains/averages all surviving terms.
- Rank zero is stated as profile/filter/average, not as constant stabilization.
- H2/Sym2 branch and finite-part inputs are closed in the same theorem mode.
- Product averaging, if used, averages `c_E,W P_E,W` directly and proves
  diagonal/offdiagonal tail extraction.
- Every external theorem used to discharge a blocker has the required
  source packet.
