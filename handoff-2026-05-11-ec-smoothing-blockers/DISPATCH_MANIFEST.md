---
schema_version: 1
title: "EC smoothing blocker sprint dispatch manifest"
date: 2026-05-11
type: manifest
tier: working
status: COMPLETE
confidence: 0.8
sources:
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv
tags: [ec-ndc, smoothing, blockers, dispatch]
---

# EC Smoothing Blocker Sprint

Goal: turn the reproduced EC smoothing finite pattern into either a theorem-grade
route, an explicit no-go, or a sharper experimental falsification plan.

## Priority Order

1. Theorem explaining why smoothing the coefficient sum and Euler product should
   stabilize an asymptotic object.
2. Independent probabilistic/model explanation for the ablation pattern.
3. Predeclared holdout curves.
4. Larger and denser `K` grid.
5. Kernel-family and null-control falsification.

## Agents

| Agent | Model | Target | Output |
|---|---|---|---|
| T1 | `gpt-5.5`, xhigh | Smoothed Perron/Mellin theorem candidate | `T1_SMOOTHED_PERRON_THEOREM.md` |
| T2 | `gpt-5.5`, xhigh | Sato-Tate/random Euler product model and ablation explanation | `T2_STOCHASTIC_EULER_PRODUCT_MODEL.md` |
| C1 | `gpt-5.5`, xhigh | Holdout curve protocol | `C1_HOLDOUT_CURVE_PROTOCOL.md` |
| C2 | `gpt-5.5`, xhigh | Kernel and null-control tests | `C2_KERNEL_NULL_CONTROL_PLAN.md` |
| C3 | `gpt-5.5`, xhigh | Larger/denser `K` plan | `C3_LARGER_K_DENSE_GRID_PLAN.md` |

## Outputs

| Output | Status | Decision |
|---|---|---|
| `T1_SMOOTHED_PERRON_THEOREM.md` | `RIGOROUS_REDUCTION` | Conditional theorem target; no promotion until `H1`/`H2` close. |
| `T2_STOCHASTIC_EULER_PRODUCT_MODEL.md` | `RIGOROUS_REDUCTION` | Finite variance/covariance explanation for the ablation pattern. |
| `C1_HOLDOUT_CURVE_PROTOCOL.md` | `COMPUTE_BLOCKED` | Needs external `ainvs`/curve metadata and convention checks. |
| `C2_KERNEL_NULL_CONTROL_PLAN.md` | `RIGOROUS_REDUCTION` | Exact falsification protocol; execution pending. |
| `C3_LARGER_K_DENSE_GRID_PLAN.md` | `COMPUTE_BLOCKED` | `K=3e6` feasible; `K=1e7` needs faster point counting or overnight run. |
| `EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md` | `RIGOROUS_REDUCTION` | Current sprint synthesis. |

## Current Baseline

Saved reproduction through `K<=1000000`:

- `all, alpha=0.75`: cross-curve ratio `1.3473754929960748`, max CV `0.063297427334436704`.
- `cP_only, alpha=0.75`: cross-curve ratio `1.3474536199105895`, max CV `0.063319173311522384`.
- Full smoothing passes old gates for all 7 tested alphas.
- 22 mode/alpha combinations pass old gates.

Claim state: `NUMERICAL_LEAD_ONLY`. The pattern is reproducible, but the proposed
`L2^rank` denominator is not load-bearing yet.

## Promotion Gate

Do not promote any EC smoothing claim unless:

- a theorem/reduction explains the smoothed coefficient sum/Euler product
  mechanism under explicit hypotheses;
- `alpha=0.75` or another predeclared alpha survives holdout curves;
- larger/denser `K` does not reveal endpoint damping masquerading as
  convergence;
- kernel-family and null controls do not reproduce the same signal trivially;
- component ablations identify the load-bearing normalization.
