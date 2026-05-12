---
schema_version: 1
title: "EC H2 smoothed Mertens sprint dispatch manifest"
date: 2026-05-11
type: manifest
tier: working
status: COMPLETE
confidence: 0.8
sources:
  - handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
  - handoff-2026-05-11-ec-smoothing-blockers/T2_STOCHASTIC_EULER_PRODUCT_MODEL.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
tags: [ec-ndc, smoothing, h2, mertens, dispatch]
---

# EC H2 Smoothed Mertens Sprint

Goal: attack the theorem input

```text
H2: log P_E,W(K) = -rank(E) log log K + B_E,W + o(1)
```

for the smoothed EC Euler product at `s=1`, where `P_E,W(K)` uses the local
inverse factors from the Agent 3 reproducer.

## Priority

1. Determine whether a citation-closed theorem already implies H2.
2. If not, prove a conditional H2 with exact hypotheses.
3. If impossible, isolate the obstruction precisely enough to redirect the EC
   smoothing route.
4. Check the current numerical data against the claimed `-rank loglogK` slope.

## Agents

| Agent | Model | Target | Output |
|---|---|---|---|
| H2-A | `gpt-5.5`, xhigh | Literature/source audit for GL(2)/EC Mertens products | `H2A_LITERATURE_AUDIT.md` |
| H2-B | `gpt-5.5`, xhigh | Analytic proof attempt via explicit formula/PNT for EC coefficients | `H2B_ANALYTIC_PROOF_ATTEMPT.md` |
| H2-C | `gpt-5.5`, xhigh | Obstruction/no-go and exact hypothesis map | `H2C_OBSTRUCTION_MAP.md` |
| H2-D | `gpt-5.5`, xhigh | Numerical slope diagnostics from existing reproduction data | `H2D_NUMERICAL_DIAGNOSTICS.md` plus optional script/CSV |
| H2-E | `gpt-5.5`, xhigh | Final theorem packaging: weakest useful H2 statement | `H2E_THEOREM_PACKAGING.md` |

## Outputs

| Output | Status | Decision |
|---|---|---|
| `H2A_LITERATURE_AUDIT.md` | `RIGOROUS_REDUCTION` | No audited theorem proves pointwise H2; sharp BSD-Mertens plus smoothing transfer would imply it. |
| `H2B_ANALYTIC_PROOF_ATTEMPT.md` | `RIGOROUS_REDUCTION` | Exact local decomposition and conditional proof target. |
| `H2C_OBSTRUCTION_MAP.md` | `NO_GO` | Naive pointwise `B+o(1)` H2 unsafe without treating offcentral zero terms. |
| `H2D_NUMERICAL_DIAGNOSTICS.md` | `AUDIT_ONLY` | Seven-point slopes are compatible with `-rank`, tail not settled. |
| `H2E_THEOREM_PACKAGING.md` | `RIGOROUS_REDUCTION` | Weakest useful theorem template. |
| `H2_SPRINT_SYNTHESIS_2026-05-11.md` | `RIGOROUS_REDUCTION` | Current claim-safe synthesis. |

## Status Rule

Every agent output must use exactly one status:

`PROOF_CANDIDATE`, `RIGOROUS_REDUCTION`, `NO_GO`, `COMPUTE_BLOCKED`,
`LITERATURE_BLOCKED`, or `AUDIT_ONLY`.

## Do Not Promote Unless

- the coefficient `-rank(E)` is derived for the exact local factors and smoothed
  kernel;
- zero/pole contributions of `L(E,s)` and any symmetric-square or bad-prime
  terms are explicitly accounted for;
- source claims have `curl + pdftotext + verbatim quote + page/eq`;
- the statement separates rank-zero behavior from positive-rank behavior;
- numerical diagnostics do not contradict the proposed slope.
