---
schema_version: 1
title: "S1 smoothed explicit formula sprint synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.82
sources:
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1A_EXPLICIT_FORMULA_DERIVATION.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1B_SOURCE_AUDIT.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1C_ZERO_TERM_ANALYSIS.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1D_AVERAGED_FALLBACK.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1E_NUMERICAL_ZERO_DIAGNOSTICS.md
  - handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1F_SYM2_COMPANION_TERM.md
tags: [ec-ndc, s1, explicit-formula, h2, synthesis]
---

# S1 Smoothed Explicit Formula Sprint Synthesis

No theorem was promoted. The sprint made real progress on the H2 fork.

## Executive Verdict

For the smoothed prime-linear trace

```text
S_1,W(K) = sum_p W(p/K) a_p/p,
```

offcentral zeros of `L(E,s)` should be lower order, not persistent, provided
the relevant Dirichlet series has logarithmic branch singularities and the
weighted zero sum is controllable.

The local contribution of a zero `rho=1+i gamma` is

```text
-m_rho K^(i gamma) W_hat(i gamma) / log K
```

up to sign/branch conventions and smaller `1/(log K)^2` terms. Persistent
`K^(i gamma)` terms belong to logarithmic-derivative or log-prime-weighted
formulas before integrating away the `log p` weight.

This resolves the main H2-B/H2-C discrepancy in favor of a pointwise theorem
route, conditional on branch-only continuation, zero-summability, contour
control, and the symmetric-square companion term.

## Result Table

| Agent | Status | Result | Decision |
|---|---|---|---|
| S1-A | `RIGOROUS_REDUCTION` | Derives the smoothed Mellin formula and `K^(rho-1)W_hat(rho-1)/log K` offcentral scale. | Use as main theorem skeleton. |
| S1-B | `LITERATURE_BLOCKED` | Audited sources support adjacent GL(2)/EC explicit-formula structure but not the exact fixed-curve endpoint-smoothed S1 theorem. | New in-repo proof needed. |
| S1-C | `RIGOROUS_REDUCTION` | Local branch analysis confirms noncentral zero term is lower order for S1, not persistent. | Resolves the zero-scale fork locally. |
| S1-D | `RIGOROUS_REDUCTION` | Log-`K` averaged fallback is meaningful but too weak for original pointwise goal. | Keep as fallback only. |
| S1-E | `AUDIT_ONLY` | Seven-point data are too sparse; `37a1` has weak zero-frequency hint, `389a1` not stable. | Numerics neither prove nor disprove. |
| S1-F | `RIGOROUS_REDUCTION` | H2 also needs symmetric-square and prime-harmonic finite parts; same branch logic should make offcentral sym2 terms lower order. | Include in final H2 theorem. |

## Repaired Pointwise Target

Let

```text
r = ord_{s=1} L(E,s)
```

and let `kappa_sym` be the central order of the companion symmetric-square or
adjoint object in the H2 convention. Under exact Agent 3 local normalization,
an admissible kernel `W`, branch-only continuation, and zero-summability:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + Z_1,E,W(log K)/log K
   + O((log K)^(-2)) + lower contour errors.
```

For zeros on `Re(s)=1`, `Z_1,E,W` is bounded if

```text
sum_gamma |m_gamma W_hat(i gamma)| < infinity.
```

Thus `Z_1,E,W(log K)/log K = o(1)`.

H2 then requires the companion terms:

```text
S_sym,W(K)  = -kappa_sym log log K + C_sym,E,W + o(1),
M_good,W(K) =  log log K + C_M,E,W + o(1),
```

plus finite `R_ge3` and bad-prime constants. The product coefficient becomes

```text
(1/2 + kappa_sym/2 - r) - kappa_sym/2 - 1/2 = -r.
```

## What Is Still Missing

The local zero-scale calculation is not yet a complete theorem. The missing
proof obligations are:

- derive the continuation and local branch expansion of
  `A_E(z)=sum_p a_p p^(-1-z)` in the required strip;
- prove the weighted zero-summability and contour-shift bounds for the chosen
  smoothstep or admissible kernel;
- prove the same finite-part theorem for `S_sym,W`;
- source-verify or prove the ordinary weighted prime-Mertens finite part for
  `M_good,W`;
- keep analytic rank first, using algebraic rank only under BSD/rank equality;
- verify the exact Agent 3 bad-prime convention is absorbed only into constants.

## Literature State

The source audit is `LITERATURE_BLOCKED`. Audited sources do not prove the exact
fixed-curve, endpoint-smoothed S1 theorem. They support adjacent explicit
formula structures and show why the prime-square/symmetric-square term cannot
be dropped, but they do not close this sprint's theorem.

## Numerical State

The numerical diagnostics are `AUDIT_ONLY`. The saved seven-point grid cannot
distinguish `K^(i gamma)/log K` from persistent `K^(i gamma)`. It gives a weak
`37a1` hint and no stable `389a1` confirmation. Dense log-`K` data would be
needed for a serious frequency test.

## Decision

This is the strongest EC smoothing theorem route so far:

```text
Pointwise H2-limit is plausible under explicit branch/zero-summability
hypotheses.
```

It is not literature-closed and not proof-closed. The next sprint should
produce a formal theorem statement and proof skeleton for the branch-expansion
and zero-summability hypotheses, or implement the C3 dense log-grid to test
the predicted `1/log K` residual damping.

## Do Not Promote Unless

- the exact Agent 3 local factors remain in the statement;
- `S_1,W` uses analytic rank and includes `kappa_sym`;
- `S_sym,W` and `M_good,W` are included before claiming product coefficient
  `-r`;
- all offcentral contributions are derived as logarithmic branch terms or
  explicitly retained;
- the zero sum and contour errors are proved or stated as hypotheses;
- no audited source is cited beyond what it actually proves;
- H1 composition uses the same pointwise theorem mode.
