---
schema_version: 2
title: Recent Compute Results Review
type: project
domain: project
tier: working
confidence: 0.8
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - raw/farey-archive/recent-outputs/desktop-experiments/
  - raw/farey-archive/recent-outputs/library-experiments/
  - projects/farey-research/task-queue.md
supersedes: []
superseded-by:
tags: [farey, compute-results, review, roadmap]
---

# Recent Compute Results Review

Reviewed the recent M1/API output bundle under `raw/farey-archive/recent-outputs/`. This page records only roadmap-level consequences; raw outputs remain archive evidence, not active context.

## High-Level Verdict

- The W2 prime direction is strengthened as the main active research thread, but several recent outputs are theory-only and cannot be promoted as evidence.
- The `log(N)` term should stay in the working model. The conductor-bias simulation argues rank/conductor collinearity alone is probably too small to explain the observed `0.47 * log(N)` coefficient.
- Simple raw Sym2/Petersson and simple Deligne/Gamma-normalized variants do not currently explain `E[C1^2]`; keep them as negative/blocked.
- Paper C arithmetic-surrogate theorem language is not ready. Recent analysis says the proposed `K log K`-type surrogate is likely the wrong asymptotic for cuspidal forms.
- Pair-correlation work remains useful but must be rebuilt from primary literature and fresh code. The recent survey has citation/formula risk and should not be cited directly.
- Several M1 outputs used stale values such as `1.087` and `1.175`, or ended in `CANNOT COMPUTE`; these are not active evidence.

## Reviewed Outputs

### Promote As Roadmap Signals

- `CONDUCTOR_BIAS_SIMULATION.md.txt`: argues omitted rank/conductor correlation probably explains only part of the log-conductor coefficient. Treat as heuristic support for W2 prime, not proof.
- `SAMBA_W2PRIME_LOGN_MECHANISM.md.txt`: gives a plausible route through Rankin-Selberg second moments and Sym2-family averages. Useful as a theory-search prompt; not a theorem.
- `OR_DELIGNE_NORMALIZATION_COMPLETE.md.txt`: negative result for simple Gamma/Deligne collapse. Promote as a blocker for correspondence claims.
- `OR_ARITHMETIC_SURROGATE_EC_WEIGHT2.md.txt` and `ARITHMETIC_SURROGATE_THEOREM_PREVIEW.md.txt`: warn that the Paper C surrogate asymptotic is likely mis-stated for cuspidal forms. Treat as a stop sign for paper drafting.
- `TURAN_A2_VIABLE_ALTERNATIVES.md.txt`: useful non-vanishing strategy map; supports weakening Paper C to density/proportion/mollified statements.

### Keep Archived / Do Not Promote

- `W2PRIME_22PT_REGRESSION_ANALYSIS.md.txt`, `W2PRIME_MECHANISM_CONDUCTOR_REVIEW.md.txt`, `W2PRIME_RANK_LOGN_THEORY.md.txt`: failed with connection-refused tracebacks.
- `M1_PHASE1_*`, `M1_PHASE2_*`, `WAVE5_37A1_VS_389A1_GAP.md.txt`: many use stale `1.087/1.175` style baselines or say `CANNOT COMPUTE`. Use only as prompt history, not evidence.
- `GROQ_RANK0_37B1_PREDICTION.md.txt`: incomplete thought trace, no usable verdict.
- `PATH_H_TURAN_REPAIR_STATEMENT.md.txt`: contains placeholder citations like `[Author] (Year)`; not usable.
- `PAPER_C_INTRODUCTION_DRAFT.md.txt`: draft prose only and currently overstates W2 prime as a law.
- `WAVE5_PAIR_CORR_LITERATURE.md.txt`: citation/formula risk; use only as a reminder to do a primary-source review.
- `WEIGHT12_L_PRIME_ZERO_SCALING.md.txt`: short heuristic only; no roadmap change.

## Roadmap Consequences

1. W2 prime becomes a validation-and-mechanism project: run leave-one-out diagnostics, actual rank-0 high-conductor recomputes, fixed/narrow-conductor contrasts, and a clean Sym2-family-theory derivation attempt.
2. Koyama correspondence should present W2 prime cautiously: `log(N)` appears real in current data; rank-only W2 is superseded; exact mechanism is open.
3. Deligne-completed Sym2 is demoted from promising to blocked until a concrete formula beats the simple normalization failures.
4. Delta remains a separate clean anchor. None of the recent outputs changed the verified `0.950231842` status.
5. Paper C should not be drafted as theorem language. Reframe as non-vanishing/density/mollifier alternatives only after proof review.
6. Pair correlation remains P2. Next step is a small verified script plus primary-source bibliography, not another broad model survey.
