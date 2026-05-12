---
schema_version: 1
title: "H1 breakthrough proof wave synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.88
sources:
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/H2_SYM2_PROOF_ATTEMPT_2.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/KERNEL_FILTER_DIAGNOSTIC_IMPLEMENTATION.md
  - handoff-2026-05-11-h1-breakthrough-proof-wave/BREAKTHROUGH_WAVE_REFEREE.md
tags: [ec-ndc, h1, reciprocal-residues, smoothing, synthesis]
---

# H1 Breakthrough Proof Wave Synthesis

No EC smoothing theorem was promoted.

The wave closed a useful negative loop: the direct Li-Zaharescu/mollifier route
does not give the fixed-kernel H1 upper bound. But it also produced sharper
quantitative targets for any future proof:

```text
reciprocal derivative shell moment,
reciprocal strip bounds for contour tails,
explicit multiple-zero exceptional terms,
and matched H2 branch/Sym2 closure.
```

## Result Table

| Slot | File | Status | Decision |
|---|---|---|---|
| LZ dyadic upper bound | `H1_LZ_DYADIC_UPPER_BOUND.md` | `NO_GO` | Existing Li-Zaharescu input does not supply fixed H1 upper bounds; extracted exact shell criterion. |
| Fixed-weight transfer | `H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md` | `NO_GO` | Dirichlet-polynomial mollifier weights cannot uniformly represent the fixed H1 weight without a new upper-bound theorem. |
| Multiple zeros | `H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md` | `RIGOROUS_REDUCTION` | H1 theorem must retain explicit polynomial-exponential exceptional terms unless killed/controlled. |
| Contour tails | `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md` | `RIGOROUS_REDUCTION` | Finite-box identity and legal heights are clean; horizontal/left tails reduce to `H-height` and `H-left`. |
| Rank-zero/product average | `RANK_ZERO_PRODUCT_AVERAGE_PACKAGE.md` | `RIGOROUS_REDUCTION` | Paper-ready fallback package: pointwise profile and arithmetic product average kept separate. |
| H2/Sym2 | `H2_SYM2_PROOF_ATTEMPT_2.md` | `RIGOROUS_REDUCTION` | Local H2 algebra coherent; exact endpoint S1 and good-prime Sym2 remain conditional. |
| Kernel filter | `KERNEL_FILTER_DIAGNOSTIC_IMPLEMENTATION.md`; `kernel_filter_moments.py` | `RIGOROUS_REDUCTION` | Finite signed log-kernel filtering is implementation-ready diagnostic, not theorem evidence. |
| Referee | `BREAKTHROUGH_WAVE_REFEREE.md` | `NO_GO` | Do not promote; wave is a guarded reduction packet. |

## Main Negative Result

The direct route

```text
Li-Zaharescu reciprocal-derivative/mollifier machinery
  => fixed-kernel H1 reciprocal-residue bound
```

is blocked.

The fixed H1 weight is

```text
W_hat(i gamma) e^(i gamma u).
```

Li-Zaharescu-style weights live in a length-`M=T^theta`
log-ratio Dirichlet-polynomial class. Uniformly approximating the phase
`e^(i gamma u)` forces available frequencies near `u`, hence a length barrier
roughly

```text
u <= log M = theta log T.
```

This leaves the low and medium shells

```text
T < exp(u/theta)
```

uncontrolled. Estimating the approximation residual already needs the
reciprocal-derivative upper bound we were trying to prove. Thus the transfer is
circular without a new theorem.

## Sharp Positive-Rank Target

The wave extracted the clean shell target.

Let

```text
|W_hat(i t)| <= C (1+|t|)^(-q).
```

For simple zeros, a sufficient dyadic input is:

```text
J_E,2(T) :=
  sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-2)
  <= C_E T^theta (log T)^B
```

with

```text
theta < 2q - 1.
```

Then Cauchy-Schwarz gives absolute uniform convergence of

```text
sum_gamma W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma),
```

so the simple-zero H1 offcentral aggregate is `O(1)` uniformly in `u`, enough
for positive analytic rank `r>=1` once the H1 contour tail is `o(u^r)`.

For the current smoothstep-scale decay `q=2`, the target is:

```text
J_E,2(T) <= C_E T^(3-delta)
```

for some `delta>0`.

This is not sourced or proved; it is the next exact theorem target.

## Contour Tail Target

The H1 finite-box identity is valid under ordinary meromorphic contour
calculus. The start-line truncation is also clean once the Mellin/Perron start
line is placed in an absolute-convergence region.

The hard contour assumptions are:

```text
H-height:
  legal heights T_n with
  sup_{-eta<=x<=sigma} |1/L(E,1+x+iT_n)| <= C T_n^A
  with A<q;

H-left:
  int_R |W_hat(-eta+it)/L(E,1-eta+it)| dt < infinity,
```

or a compatible polynomial substitute on the shifted line.

Zero counting supplies legal heights and separation from ordinates, but it
does not supply reciprocal bounds for `1/L(E,s)` near zeros. This is the same
reciprocal-control obstruction in contour form.

## Multiple-Zero Handling

The multiple-zero package removes an ambiguity. If `rho=1+i gamma` has
multiplicity `m`, the H1 contribution is:

```text
e^(i gamma u) P_rho(u),
deg P_rho <= m-1,
```

with coefficients from the Laurent expansion of `1/L(E,s)` and derivatives of
`W_hat`.

For positive rank `r`, central closure requires every surviving effective
critical-line degree to be `< r`, unless the term is kernel-killed,
coefficient-cancelled, retained, or averaged. For rank zero, any nonzero
degree `>=1` term grows, and even simple residues remain main-scale
oscillation.

Thus many-simple-zero results are not enough. The theorem must explicitly
retain or control the exceptional set.

## Rank-Zero Fallback

The rank-zero object is now paper-package ready as a conditional fallback:

```text
c_E,W(e^u) = 1/L(E,1) + Z_c(u) + o(1),
```

with a declared convergence mode for `Z_c`.

The product-average fallback is a separate arithmetic average:

```text
A_U[c_E,W(e^u)P_E,W(e^u)].
```

If

```text
H_c(u)=q_0 + sum_gamma a_gamma e^(i gamma u),
G(u)=sum_eta d_eta e^(i eta u),
```

then the conditional diagonal constant is:

```text
e^(B_H2)(q_0 d_0 + sum_gamma a_gamma d_(-gamma)).
```

This is not an averaged-log or geometric-mean statement.

## H2 State

The H2/Sym2 second attempt confirms:

```text
log P_E,W(K)
 = S_1,W + (1/2)S_sym,W - (1/2)M_good,W + R_ge3,W + B_bad,E,W.
```

Local algebra is coherent and the `kappa_sym` coefficient cancels correctly.
But exact endpoint-smoothed S1 branch continuation and exact good-prime Sym2
finite part are still proof/source dependencies. H2 remains conditional and
does not control H1 reciprocal poles.

## Kernel Diagnostic

`kernel_filter_moments.py` constructs a signed log-Gaussian diagnostic kernel
with finite constraints

```text
W_hat(0)=1,
W_hat(i gamma_j)=0.
```

Smoke test:

```text
gamma = 1.5, 3.25, 5.75
max residual about 1.4e-16
```

The referee correctly notes a caveat: this diagnostic uses a log-Gaussian
Schwartz moment normalization, not the endpoint kernel pole
`W_hat(z)=1/z+O(1)` used for the H1 central polynomial. It is useful for
finite low-zero experiments, not for theorem promotion.

## Claim-Safe State

Allowed:

```text
The breakthrough wave makes the H1 obstruction quantitatively sharper.
Positive-rank pointwise H1 would follow from a reciprocal-derivative shell
moment with theta<2q-1, plus contour assumptions H-height/H-left and
multiple-zero effective-degree control. Rank zero is best handled as an
oscillatory profile or arithmetic product average.
```

Forbidden:

```text
Existing Li-Zaharescu/mollifier results prove fixed H1.
Mollifier weights transfer uniformly to the fixed H1 weight.
Kernel filtering proves fixed-kernel asymptotics.
Rank-zero smoothing gives a constant pointwise limit.
H2 branch damping controls H1 reciprocal poles.
```

## Best Next Move

The next proof target is now exact:

```text
Prove or disprove the fixed-curve shell moment

  J_E,2(T) = sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-2)
             <= C_E T^(3-delta)

for the fixed GL(2)/EC L-function, or replace it by a direct principal-value
bound for the fixed H1 weight.
```

If that target stays out of reach, the most honest paper path is:

```text
rank-zero oscillatory profile
+ product-average diagonal theorem
+ finite kernel-filter diagnostics as evidence for low-zero dominance.
```

## Do Not Promote Unless

- The fixed H1 shell moment/direct bound is proved or sourced.
- `H-height` and `H-left` are proved or the contour theorem is explicitly
  conditional on them.
- Multiple-zero exceptional terms are retained or controlled.
- H2 endpoint S1/Sym2 closure is proved in the same theorem mode.
- Kernel diagnostics stay diagnostic.
- Every external theorem used in a final paper has the required source packet.
