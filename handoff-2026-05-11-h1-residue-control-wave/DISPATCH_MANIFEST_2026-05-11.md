---
schema_version: 1
title: "H1 residue-control wave dispatch manifest"
date: 2026-05-11
type: dispatch-manifest
tier: working
status: COMPLETE
confidence: 0.9
tags: [ec-ndc, h1, residue-control, gpt55-wave]
---

# H1 Residue-Control Wave Dispatch Manifest

Goal: make the shortest meaningful progress on the EC smoothing blocker after
the H1 reciprocal-Perron wave. Target: close, reduce, or refute fixed-curve
reciprocal-residue control for H1, while preserving honest rank-zero and
averaged fallback formulations.

All spawned agents used `model=gpt-5.5` with `reasoning_effort=xhigh`.

| slot | agent id | nickname | task | output | state |
|---|---|---|---|---|---|
| 1 | `019e15fb-36ad-74e0-b945-09dd8a996df7` | Aristotle | H1 reciprocal derivative source/proof hunt | `H1_RECIP_DERIVATIVE_SOURCE_HUNT.md` | complete |
| 2 | `019e15fb-3729-79b2-858c-dc7cdc13a32f` | Curie | H1 contour-shift theorem candidate | `H1_CONTOUR_SHIFT_THEOREM.md` | complete |
| 3 | `019e15fb-378d-7ca3-9df9-b5299ae39c0e` | Rawls | Positive-rank closure conditions | `H1_POSITIVE_RANK_CLOSURE.md` | complete |
| 4 | `019e15fb-37ec-7363-81a1-ec541afcdfbd` | Boyle | Rank-zero oscillatory profile | `H1_RANK_ZERO_OSCILLATORY_PROFILE.md` | complete |
| 5 | `019e15fb-385e-7241-8222-78d1d2460242` | Poincare | Product-level averaged theorem | `H1_PRODUCT_AVERAGE_THEOREM.md` | complete |
| 6 | `019e15fb-3a9c-77e3-a4c5-905413e0b574` | Gauss | H2/Sym2 source closure | `H2_SYM2_SOURCE_CLOSURE.md` | complete |
| 7 | host thread limit | local | Kernel zero-filtering reduction | `KERNEL_ZERO_FILTERING.md` | complete |
| 8 | `019e1600-97e7-76e1-8b51-3230f89682bc` | Euclid | Adversarial referee | `RESIDUE_CONTROL_ADVERSARIAL_REFEREE.md` | complete |

## Shared Contract

Each deliverable must use one exact status:

```text
PROOF_CANDIDATE
RIGOROUS_REDUCTION
NO_GO
COMPUTE_BLOCKED
LITERATURE_BLOCKED
AUDIT_ONLY
```

Each must include confidence, dependencies, and a `Do Not Promote Unless`
section. External theorem citations require the mandatory
`curl + pdftotext + short quote + page/eq` protocol.

## Synthesis Rule

Promote nothing unless both proof and citation dependencies are closed. If the
best result is conditional, record it as a theorem scaffold or rigorous
reduction, not as an EC smoothing theorem.
