---
schema_version: 1
title: "Breakthrough wave 2 dispatch manifest"
date: 2026-05-11
type: dispatch-manifest
tier: working
status: COMPLETE
confidence: 0.90
tags: [breakthrough-wave-2, h1, h2, gl1, b-plus, dpac, delta]
---

# Breakthrough Wave 2 Dispatch Manifest

status: `COMPLETE`

## Coordinator Rules

- No theorem is promoted unless proof and source protocol close.
- Allowed statuses: `THEOREM_PROMOTED`, `RIGOROUS_REDUCTION`, `NO_GO`,
  `DIAGNOSTIC_ONLY`.
- External theorem claims require `curl + pdftotext`, short quote, and
  page/equation.
- Use analytic rank only.
- H2 branch damping must not be used as H1 reciprocal-pole damping.
- Numerical EC work remains diagnostic until H1/H2 close.
- Do not edit Koyama correspondence/email drafts.

## Agents

| agent | topic | output | result |
|---|---|---|---|
| 01 | H1 anti-small-derivative source closure | `AGENT01_H1_DERIVATIVE_SOURCE_CLOSURE_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 02 | H1 near-multiple-zero mechanism | `AGENT02_H1_NEAR_MULTIPLE_ZERO_BUDGET_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 03 | H1 actual-coefficient moving PV | `AGENT03_H1_ACTUAL_COEFFICIENT_MOVING_PV_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 04 | H1 finite-box theorem assembly | `AGENT04_H1_FINITE_BOX_THEOREM_ASSEMBLY_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 05 | H2 S1 branch-contour legality | `AGENT05_H2_S1_BRANCH_CONTOUR_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 06 | H2 exact good-prime Sym2 closure | `AGENT06_H2_GOOD_PRIME_SYM2_CLOSURE_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 07 | GL1 moving off-target PV | `AGENT07_GL1_MOVING_OFFTARGET_PV_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 08 | B+ bridge compute implementation spec | `AGENT08_BPLUS_BRIDGE_COMPUTE_SPEC_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 09 | DPAC Lean bridge patch plan | `AGENT09_DPAC_LEAN_BRIDGE_PATCH_PLAN_2026-05-11.md` | `RIGOROUS_REDUCTION` |
| 10 | Delta registry patch plan | `AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md` | `RIGOROUS_REDUCTION` |

## Integration Target

Integrated in:

```text
BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
```

Project pointers and the claim ledger were updated only for durable verified
changes.
