---
schema_version: 1
title: "EC S1 smoothed explicit formula sprint dispatch manifest"
date: 2026-05-11
type: manifest
tier: working
status: COMPLETE
confidence: 0.8
sources:
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
  - handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
tags: [ec-ndc, h2, s1, explicit-formula, dispatch]
---

# EC S1 Smoothed Explicit Formula Sprint

Goal: resolve the H2 fork for

```text
S_1,W(K) = sum_p W(p/K) a_p/p.
```

The previous sprint left a precise discrepancy:

- optimistic route: noncentral zeros contribute lower-order terms such as
  `K^(i gamma) W_hat(i gamma) / log K`;
- obstruction route: noncentral zeros persist as an almost-periodic
  `Z_E,W(log K)`;
- fallback route: only a logarithmically averaged theorem is claim-safe.

## Required Agent Status Values

Each agent output must use exactly one:

`PROOF_CANDIDATE`, `RIGOROUS_REDUCTION`, `NO_GO`, `COMPUTE_BLOCKED`,
`LITERATURE_BLOCKED`, or `AUDIT_ONLY`.

## Agents

| Agent | Model | Target | Output |
|---|---|---|---|
| S1-A | `gpt-5.5`, xhigh | Derive smoothed explicit formula for `S_1,W` from `L'/L`/log `L`; decide pointwise zero-term scale | `S1A_EXPLICIT_FORMULA_DERIVATION.md` |
| S1-B | `gpt-5.5`, xhigh | Source audit for explicit formulas/prime sums with GL(2) coefficients and smoothing | `S1B_SOURCE_AUDIT.md` |
| S1-C | `gpt-5.5`, xhigh | Zero-term branch analysis: `K^{i gamma}/log K` vs persistent `K^{i gamma}` | `S1C_ZERO_TERM_ANALYSIS.md` |
| S1-D | `gpt-5.5`, xhigh | Averaged fallback theorem and how it composes with H1 | `S1D_AVERAGED_FALLBACK.md` |
| S1-E | `gpt-5.5`, xhigh | Numerical residual/zero-frequency diagnostics using existing data | `S1E_NUMERICAL_ZERO_DIAGNOSTICS.md` plus optional script/CSV |
| S1-F | `gpt-5.5`, xhigh | Symmetric-square/quadratic companion term needed by H2 | `S1F_SYM2_COMPANION_TERM.md` |

## Outputs

| Output | Status | Decision |
|---|---|---|
| `S1A_EXPLICIT_FORMULA_DERIVATION.md` | `RIGOROUS_REDUCTION` | Main theorem skeleton; offcentral branch terms lower order by `1/log K`. |
| `S1B_SOURCE_AUDIT.md` | `LITERATURE_BLOCKED` | No audited source closes the exact endpoint-smoothed S1 theorem. |
| `S1C_ZERO_TERM_ANALYSIS.md` | `RIGOROUS_REDUCTION` | Resolves local zero-scale fork for S1. |
| `S1D_AVERAGED_FALLBACK.md` | `RIGOROUS_REDUCTION` | Averaged fallback meaningful but too weak for original pointwise goal. |
| `S1E_NUMERICAL_ZERO_DIAGNOSTICS.md` | `AUDIT_ONLY` | Seven-point data too sparse to decide frequency behavior. |
| `S1F_SYM2_COMPANION_TERM.md` | `RIGOROUS_REDUCTION` | Companion term required for final H2 coefficient. |
| `S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md` | `RIGOROUS_REDUCTION` | Current sprint synthesis. |

## Do Not Promote Unless

- the derivation starts from the exact Agent 3 local factor normalization;
- the central coefficient is stated in analytic-rank language first;
- the noncentral zero contribution is explicitly derived, not guessed;
- source claims follow `curl + pdftotext + verbatim quote + page/eq`;
- the final theorem mode is explicit: pointwise, oscillatory, averaged, or
  conditional on a zero-term suppression hypothesis;
- composition with H1 uses the same theorem mode.
