---
schema_version: 1
title: "H1 shell moment wave dispatch manifest"
date: 2026-05-11
type: dispatch-manifest
tier: working
status: COMPLETE
confidence: 0.9
tags: [ec-ndc, h1, shell-moment, reciprocal-strip]
---

# H1 Shell Moment Wave Dispatch Manifest

Goal: make progress on the exact post-breakthrough blockers:

```text
J_E,2(T)=sum_{T<|gamma|<=2T}|L'(E,1+i gamma)|^(-2)
         <= C_E T^(3-delta)
```

for smoothstep-scale `q=2`, or a direct fixed-weight principal-value theorem;
and reciprocal strip bounds `H-height/H-left` for H1 contour tails.

Requested engine from user: "opus 5.5 extra high." Available session
equivalent used: `gpt-5.5` with `reasoning_effort=xhigh`.

| slot | agent id | task | output | state |
|---|---|---|---|---|
| 1 | completed | Shell moment source audit | `SHELL_MOMENT_SOURCE_AUDIT.md` | `AUDIT_ONLY`; close-but-insufficient |
| 2 | completed | Shell moment analytic proof attempt | `SHELL_MOMENT_ANALYTIC_ATTEMPT.md` | `RIGOROUS_REDUCTION`; anti-small-derivative reductions |
| 3 | completed | Shell moment/RMT heuristic and sharpness | `SHELL_MOMENT_RMT_HEURISTIC.md` | `AUDIT_ONLY`; heuristic support only |
| 4 | completed | Direct fixed-weight principal-value route | `FIXED_WEIGHT_PRINCIPAL_VALUE_ROUTE.md` | `RIGOROUS_REDUCTION`; needs uniform PV cancellation |
| 5 | completed | Reciprocal strip `H-height/H-left` proof/source hunt | `RECIPROCAL_STRIP_BOUNDS.md` | `RIGOROUS_REDUCTION`; `H-left` closed for `eta>1/2`, `H-height(A<2)` open |
| 6 | completed | Rank-zero fallback paper skeleton | `RANK_ZERO_FALLBACK_PAPER_SKELETON.md` | `RIGOROUS_REDUCTION`; profile/product-average fallback |
| 7 | local | Synthesis and acceptance | `H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md` | complete |
| 8 | local follow-up | TC-height exponent audit | `TC_HEIGHT_EXPONENT_AUDIT.md` | `NO_GO`; generic Cartan/Jensen does not close `A_TC<2` |

## Shared Contract

Each agent deliverable must use one exact status:

```text
PROOF_CANDIDATE
RIGOROUS_REDUCTION
NO_GO
COMPUTE_BLOCKED
LITERATURE_BLOCKED
AUDIT_ONLY
```

Each must include confidence, dependencies, and a `Do Not Promote Unless`
section. External theorem citations require `curl + pdftotext + short quote +
page/eq`.

## Promotion Rule

No EC smoothing theorem promotion. The best possible success is either a
source/proof candidate for the shell moment/strip bounds or a clear decision
to elevate them as named open hypotheses.

## Final Dispatch Decision

The wave elevates the shell moment, fixed-weight PV cancellation, and
quantitative height bound as named open hypotheses/conditional inputs.

Closed locally:

- `H-left` if the contour can shift to `Re z=-eta` with `eta>1/2`.
- The exact anti-small-derivative reductions that would imply
  `J_E,2(T)<=C_E T^(3-delta)`.
- Rank-zero fallback packaging as an oscillatory profile plus separate
  arithmetic product average.

Still open:

- fixed-curve EC/GL2 upper bound for `J_E,2(T)`;
- direct fixed-weight H1 principal-value cancellation;
- `TC-height` with exponent `A_TC<2` for the current `q=2` kernel; generic
  Cartan/Jensen is not enough, so this needs an explicit EC/GL2
  minimum-modulus theorem or a stronger kernel/theorem mode.
