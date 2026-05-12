---
schema_version: 1
title: "H1 shell moment synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: COMPLETE
verdict: RIGOROUS_REDUCTION
confidence: 0.82
sources:
  - handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md
  - handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_ANALYTIC_ATTEMPT.md
  - handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_RMT_HEURISTIC.md
  - handoff-2026-05-11-h1-shell-moment-wave/FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md
  - handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md
  - handoff-2026-05-11-h1-shell-moment-wave/TC_HEIGHT_EXPONENT_AUDIT.md
  - handoff-2026-05-11-h1-shell-moment-wave/RANK_ZERO_FALLBACK_PAPER_SKELETON.md
tags: [ec-ndc, h1, shell-moment, synthesis]
---

# H1 Shell Moment Synthesis

Status: `RIGOROUS_REDUCTION`.

Decision: no EC smoothing theorem promotion. The wave closes bookkeeping, not
the fixed H1 theorem. The right live objects are named hypotheses:

```text
H1-shell-moment(E,delta):
  J_E,2(T) <= C_E T^(3-delta)
```

for simple offcentral zeros, with multiple zeros handled by the existing
Laurent exceptional-term package; and

```text
H-height(A<q), with q=2 for the current smoothstep-scale kernel.
```

`H-left` is closed only after choosing the shifted contour
`Re z=-eta` with `eta>1/2`.

Confidence aggregation rule: use the minimum live confidence among the
decision-driving packets after dropping the model-only RMT heuristic as proof
evidence. This keeps the overall decision at `0.82`: strong enough to update
the roadmap, not strong enough to promote the theorem.

## Decision Targets

1. Is the fixed-curve shell moment

```text
J_E,2(T) <= C_E T^(3-delta)
```

source-closed, proof-candidate, or a named open hypothesis?

2. Can the fixed H1 reciprocal-residue aggregate be controlled by a direct
principal-value theorem without absolute convergence?

3. Are `H-height` and `H-left` source-closed or named open contour hypotheses?

4. If these remain open, is the fallback paper path ready as a rank-zero
profile plus arithmetic product-average package?

## Result Table

| Slot | File | Status | Decision |
|---|---|---|---|
| Source audit | `SHELL_MOMENT_SOURCE_AUDIT.md` | `AUDIT_ONLY` | Close-but-insufficient. No checked fixed-curve EC/GL2 source proves `J_E,2(T)<=C_E T^(3-delta)`, and no source proves the direct fixed H1 weight upper bound. |
| Analytic attempt | `SHELL_MOMENT_ANALYTIC_ATTEMPT.md` | `RIGOROUS_REDUCTION` | Shell moment follows from explicit anti-small-derivative inputs: pointwise derivative lower bounds, small-derivative tail bounds, zero repulsion plus minimum modulus, or positive mollifier majorants. GRH, simplicity, spacing, and lower negative moments alone do not imply it. |
| RMT heuristic | `SHELL_MOMENT_RMT_HEURISTIC.md` | `AUDIT_ONLY` | Model predicts `J_E,2(T) ~ T polylog(T)`, so `T^(3-delta)` is plausibly weak for any `delta<2`; heuristic only, not proof. |
| Principal value | `FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md` | `RIGOROUS_REDUCTION` | A direct fixed-weight PV theorem can close positive-rank H1 only with uniform cancellation giving `Z_PV(u)=o(u^r)` in the needed windows. Spacing plus square moments gives averaged/profile modes, not pointwise H1. |
| Reciprocal strip | `RECIPROCAL_STRIP_BOUNDS.md` | `RIGOROUS_REDUCTION` | `H-left` closes for `eta>1/2` by functional equation plus absolute reciprocal Euler product. `H-height(A<2)` remains open. |
| TC height exponent | `TC_HEIGHT_EXPONENT_AUDIT.md` | `NO_GO` | Generic Cartan/Jensen bookkeeping does not close `A_TC<2`; with only local zero count it naturally loses `T^(O(loglogT))`, so a real EC/GL2 minimum-modulus theorem with explicit exponent or a stronger kernel/theorem mode is needed. |
| Fallback paper | `RANK_ZERO_FALLBACK_PAPER_SKELETON.md` | `RIGOROUS_REDUCTION` | Rank-zero fallback is paper-ready as a conditional oscillatory H1 profile plus separate arithmetic product-average diagonal theorem. It is not a pointwise constant theorem and does not close EC smoothing. |

## Decisions

### 1. Shell Moment

Current state:

```text
named open hypothesis / conditional theorem input
```

No checked source or local proof closes the fixed-curve shell bound

```text
J_E,2(T)
 = sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-2)
 <= C_E T^(3-delta).
```

The correct carry-forward formulation is:

```text
H1-shell-moment(E,delta):
  there exist C_E,T0,delta>0 such that for T>=T0,
  J_E,2(T) <= C_E T^(3-delta),
```

where the sum is over simple zeros and all multiple-zero Laurent terms are
retained, killed, or explicitly assumed absent in a separate package.

Sufficient proof routes now have exact names:

1. pointwise lower bound `|L'(E,1+i gamma)| >= T^(-1+eta) polylog(T)^(-1)`;
2. small-derivative anti-concentration for `N_E(T;V)`;
3. zero repulsion plus a boundary minimum-modulus bound with exponent
   `mu-kappa<1`;
4. a positive mollifier majorant or relative reciprocal approximation whose
   square norm is `O(T^(3-delta))`.

Invalid routes are now closed: GRH, all-simple zeros, spacing, almost-all
simplicity, EC zero counting, Li-Zaharescu lower bounds, signed mollified
first moments, or zeta negative-moment analogues do not give this upper bound.

### 2. Principal Value

A direct fixed-weight PV theorem is viable only as its own named hypothesis:

```text
H1-fixed-weight-PV(E,W,r):
  legal-height sums
    sum W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)
  converge to Z_PV(u), and Z_PV(u)=o(u^r)
  in the required u-windows.
```

For `r>=1`, that would close positive-rank H1 after the same contour tails and
multiple-zero effective-degree checks. Without uniform PV cancellation, the
safe outputs are Besicovitch/profile, dyadic log-Cesaro, or product-average
theorems.

For `r=0`, even a convergent PV profile is main scale:

```text
c_E,W(e^u)=Q_0+Z_PV(u)+o(1).
```

It is not a pointwise constant limit unless a separate coefficient-death
theorem proves `Z_PV(u)->0`.

### 3. Strip Bounds

`H-left` is no longer an independent blocker if the contour shift may use

```text
Re z=-eta,   eta>1/2.
```

Then the functional equation reflects to `Re(2-s)=1+eta>3/2`, where the
reciprocal Euler product is absolutely controlled, and the gamma ratio gives
polynomial decay.

`H-height` remains a named hypothesis for the current kernel:

```text
TC-height(E,1-eta,1+sigma; A_TC):
  legal heights T_n exist with
  sup_{1-eta<=x<=1+sigma}|1/L(E,x+iT_n)| <= C T_n^(A_TC).
```

The generic Cartan/Jensen route does not prove `A_TC<2`. The follow-up audit
shows that with only local zero count `O(log T)` the natural zero-factor loss is

```text
T^(O(loglogT)),
```

so even a fixed finite exponent is not automatic from that argument. A real
fixed EC/GL2 minimum-modulus theorem with explicit exponent below `2`, or a
stronger kernel with `q>A_TC`, is needed.

### 4. Fallback Paper

The fallback path is viable and should be the claim-safe paper route if shell
moment/PV/height remain open:

```text
rank zero:
  c_E,W(e^u)=Q_0+Z_c(u)+o(1)
```

with the zero series in a declared convergence mode, plus a separate
arithmetic dyadic product average

```text
Avg_u c_E,W(e^u) P_E,W(e^u)
  = e^(B_H2)(q_0 d_0 + sum_gamma a_gamma d_(-gamma))
```

under the H2/profile hypotheses. This theorem mode must not be rewritten as
an averaged-log statement or as pointwise EC smoothing.

## Roadmap Change

Replace the previous "prove the shell moment or direct PV" move with this
decision tree:

1. Try to prove `H1-shell-moment(E,delta)` through one of the named
   anti-small-derivative routes.
2. If a direct theorem is desired, prove `H1-fixed-weight-PV(E,W,r)` with
   uniform cancellation, not only spacing/moment inputs.
3. For contour tails, set `eta>1/2`, record `H-left` as closed, and do not
   reuse generic Cartan/Jensen as a proof of `A_TC<2`; find a real EC/GL2
   minimum-modulus theorem with explicit exponent, or change kernel/theorem
   mode.
4. If these remain open, write the rank-zero/profile/product-average fallback.

## Promotion Guard

Do not promote an EC smoothing theorem unless all of these are explicitly
closed or assumed in theorem language:

- `H1-shell-moment(E,delta)` or `H1-fixed-weight-PV(E,W,r)`;
- multiple-zero Laurent exceptional terms;
- `TC-height` with `A_TC<q` and moving-box compatibility;
- H2/Sym2 endpoint-smoothed source/proof inputs;
- rank-zero oscillatory/profile or product-average mode.

RMT remains heuristic support only. Source audit remains negative for the
fixed-curve EC/GL2 upper bound.
