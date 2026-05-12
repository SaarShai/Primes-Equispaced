---
schema_version: 1
title: "EC C2-prime diagnostic protocol"
date: 2026-05-11
type: protocol
tier: working
status: PREDECLARATION_FOR_FUTURE_DIAGNOSTICS_ONLY
confidence: 0.76
sources:
  - handoff-2026-05-11-all-in-wave/EC_G3_FAILURE_DIAGNOSTIC_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_REPORT_2026-05-11.md
  - handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md
tags: [ec-ndc, smoothing, c2-prime, diagnostic-protocol]
---

# EC C2-prime Diagnostic Protocol

status: `PREDECLARATION_FOR_FUTURE_DIAGNOSTICS_ONLY`

## Purpose

C2-prime is not a rescue of failed G3. It is a clean diagnostic protocol for
future EC numerics after the full G3 empirical-p failure.

The old G3 result remains:

```text
G3_FAIL
0/512 iid old/primary passes
0/128 shared old/primary passes
iid p_ratio failure
shared p_score failure
```

Any C2-prime pass is exploratory finite evidence only. It cannot promote an EC
theorem without the H1/H2 theory gaps.

## Why C2-prime Exists

The full G3 diagnostic showed:

```text
st_iid:    31/512 nulls beat real ratio; 0/512 beat real CV; 0/512 pass old/primary.
st_shared: 20/128 nulls beat real ratio; 5/128 beat real additive score; 0/128 beat real CV; 0/128 pass old/primary.
```

So the additive score and ratio-only p-tests are not equivalent to the
conjunctive old gate. Low ratio can compensate for a CV miss. C2-prime replaces
that with Pareto and CV-specific diagnostics.

## Non-Retroactivity Rule

Do not use C2-prime to reclassify the existing `512/128` G3 run as a pass.
Those data were already seen. C2-prime can be checked on them only as an
explanatory diagnostic.

For any future pass/fail claim, freeze the exact protocol before generating:

- fresh stochastic seeds;
- holdout curves;
- denser/larger `K`;
- new kernels or match modes.

## Fixed Primary Group

Keep the current primary group fixed unless a separate protocol supersedes it:

```text
kernel = smoothstep
mode = all
alpha = 0.75
match = none
K grid = 1000, 3000, 10000, 30000, 100000, 300000, 1000000
curves = 37a1, 11a1, 389a1
real ratio = 1.3473754929960748
real max CV = 0.063297427334436704
old ratio cutoff = 1.42083
old CV cutoff = 0.08567129
```

No relaxation of the old CV cutoff is allowed. The G3 diagnostic showed the
first shared null near-pass appears if the CV cutoff is relaxed to `0.10`.

## Diagnostic Metrics

For each null family, compute:

```text
old_pass = ratio < old_ratio_cutoff and max_cv < old_cv_cutoff
primary_pass = old_pass and old primary score clause
cv_better = max_cv <= real_max_cv
ratio_better = ratio <= real_ratio
pareto_better = ratio <= real_ratio and max_cv <= real_max_cv
old_pareto = ratio < old_ratio_cutoff and max_cv < old_cv_cutoff
```

Add-one empirical p-values:

```text
p_cv = (1 + count(cv_better))/(n + 1)
p_pareto = (1 + count(pareto_better))/(n + 1)
p_old_pareto = (1 + count(old_pareto))/(n + 1)
```

Optional ranking score for reporting only:

```text
pareto_score = max(log(ratio)/log(real_ratio), max_cv/real_max_cv)
```

The real anchor has `pareto_score = 1`. A null can score below `1` only if it
beats the real point in both ratio and max CV. This avoids allowing ratio to
buy a CV miss.

## Fresh-Seed C2-prime Gate

Use a fresh seed block, not seeds already used in G3:

```text
st_iid:    seeds 512..1023
st_shared: seeds 128..255
```

Predeclared finite diagnostic pass requires:

```text
st_iid old_pass_rate <= 0.01
st_iid primary_pass_rate <= 0.005
st_iid p_cv <= 0.01
st_iid p_pareto <= 0.01

st_shared old_pass_rate <= 0.02
st_shared p_cv <= 0.02
st_shared p_pareto <= 0.02
```

Report `p_ratio` and additive `p_score`, but do not use them as pass/fail
clauses unless a new protocol justifies their weights before the run.

## Holdout/Larger-K Discipline

Holdout curves and denser/larger `K` are not promotion gates unless the
predeclared stochastic diagnostic is already passed on fresh seeds.

Order:

1. Freeze C2-prime implementation and seed blocks.
2. Run fresh stochastic C2-prime.
3. If it fails, stop EC numerical promotion work.
4. If it passes, run holdout curves as exploration.
5. If holdouts pass, run denser/larger `K` as exploration.
6. Still require H1/H2 theory before theorem language.

## Existing-G3 Diagnostic Values

These are post hoc explanatory values, not pass/fail reclassification:

| family | cv_better | pareto_better | old_pass | primary_pass |
|---|---:|---:|---:|---:|
| `st_iid` | `0/512` | `0/512` | `0/512` | `0/512` |
| `st_shared` | `0/128` | `0/128` | `0/128` | `0/128` |

Interpretation: real CV and Pareto position are strong on the seen stochastic
data, but the already-run G3 remains a fail because the predeclared empirical
ratio/score clauses failed.

## Research Decision

EC numerics are now a secondary diagnostic lane. The main research lane should
move to:

- `H1-weighted-l1(E,W,epsilon)`;
- fixed-weight H1 PV;
- H2 S1/Sym2 endpoint theorem packaging.
