---
schema_version: 1
title: "Agent 07 - EC G3/C2-prime numerical diagnosis"
date: 2026-05-11
agent: "Agent 07"
type: diagnostic
tier: claim-safe
status: DIAGNOSTIC_ONLY
confidence: 0.83
scope: "G3 empirical-p failure diagnosis and next predeclared C2-prime, holdout, and dense-K diagnostic gates"
sources:
  - start.md
  - L1_index.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/EC_G3_FAILURE_DIAGNOSTIC_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/EC_C2_PRIME_DIAGNOSTIC_PROTOCOL_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_REPORT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUMMARY_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py
  - primes-equispaced/handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py
  - primes-equispaced/handoff-2026-05-11-ec-smoothing-blockers/C1_HOLDOUT_CURVE_PROTOCOL.md
  - primes-equispaced/handoff-2026-05-11-ec-smoothing-blockers/C3_LARGER_K_DENSE_GRID_PLAN.md
tags: [ec-ndc, smoothing, g3, c2-prime, null-controls, holdout, dense-k]
---

# Agent 07 - EC G3/C2-prime Numerical Diagnosis

Status enum: `DIAGNOSTIC_ONLY`.

## Verdict

G3 remains a real predeclared failure. Do not reclassify it.

Observed G3 facts:

| family | trials | old pass | primary pass | failed clause |
|---|---:|---:|---:|---|
| `st_iid` | `512` | `0` | `0` | `p_ratio=0.062378167641325533 > 0.01` |
| `st_shared` | `128` | `0` | `0` | `p_score=0.046511627906976744 > 0.02` |

The failure is not "stochastic nulls pass the old gate." They do not. The
failure is score/gate non-equivalence: ratio-only and additive-score empirical
p-values are weaker than the conjunctive old gate.

Decision:

```text
G3 result: G3_FAIL, unchanged.
C2-prime: future-only diagnostic, not a rescue.
Holdout/dense-K: run only after a fresh C2-prime diagnostic pass.
Theorem promotion: forbidden without H1/H2 theorem closure.
```

## Failure Diagnosis

### 1. Score Design

The old gate is conjunctive:

```text
ratio < 1.42083
max_cv < 0.08567129
```

The primary score used by the scripts is additive:

```text
score = log(ratio) + max_cv
real_score = 0.3614560483477629
primary slack = 0.005
```

This lets low ratio buy a CV miss. That is the core design flaw.

Best shared-score null:

```text
seed = 113
ratio = 1.1608386545795315
max_cv = 0.09678231388824925
score = 0.24592503586956727
```

It beats the real additive score but fails the old CV cutoff. It is the warning
row: only about `13%` above the old CV cutoff and far better on ratio than the
real point.

Best iid-score null:

```text
seed = 398
ratio = 1.0955148176893732
max_cv = 0.27236448141701425
score = 0.36358888733909978
```

This is not a near old-gate pass. Its max CV is more than `4x` the real max CV.
It demonstrates the same score-design problem in a more extreme form.

Conclusion: do not use `p_ratio` or additive `p_score` as promotion gates unless
their weights are frozen before the run and made non-compensatory for CV.

### 2. CV/Pareto Tests

The seen G3 data are strong on CV and Pareto position, but only post hoc:

| family | cv_better | pareto_better | add-one `p_cv` | add-one `p_pareto` |
|---|---:|---:|---:|---:|
| `st_iid` | `0/512` | `0/512` | `1/513 = 0.001949317738791423` | `1/513 = 0.001949317738791423` |
| `st_shared` | `0/128` | `0/128` | `1/129 = 0.007751937984496124` | `1/129 = 0.007751937984496124` |

These numbers explain why the real point looked special, but they cannot rescue
G3 because the C2-prime clauses were not the predeclared G3 clauses.

C2-prime should make the CV/Pareto questions first-class:

```text
cv_better     = max_cv <= real_max_cv
ratio_better  = ratio <= real_ratio
pareto_better = ratio <= real_ratio and max_cv <= real_max_cv
old_pareto    = ratio < old_ratio_cutoff and max_cv < old_cv_cutoff
```

Use add-one p-values:

```text
p_cv         = (1 + count(cv_better))/(n + 1)
p_pareto     = (1 + count(pareto_better))/(n + 1)
p_old_pareto = (1 + count(old_pareto))/(n + 1)
```

Optional reporting score only:

```text
pareto_score = max(log(ratio)/log(real_ratio), max_cv/real_max_cv)
```

This score cannot rank a null below real unless it beats real on both ratio and
max CV.

### 3. Finite-Grid Artifact Risk

The present primary grid has only seven K values:

```text
1000,3000,10000,30000,100000,300000,1000000
```

That is too sparse to rule out a finite-grid or endpoint-damping artifact.
Current deterministic controls show useful robustness, but not asymptotic
stability. The C3 blocker already records the visible tail risk:

```text
389a1: X(300000) = 1.71095327841
389a1: X(1000000) = 1.51321181870
last-step drift = -11.5574%
```

The seven-point max CV can miss oscillation between grid points and cannot
distinguish settled tail behavior from a smooth cutoff window.

### 4. Null-Family Weakness

The two Sato-Tate families are useful bracket controls, not faithful EC
universe models.

`st_iid` weakness:

- replaces good-prime traces independently by curve;
- destroys cross-curve arithmetic correlation;
- flags that ratio alone is easy to beat by chance.

`st_shared` weakness:

- gives all curves the same stochastic trace at each good prime;
- over-correlates the curves;
- is the sharper warning family because `5/128` nulls beat the additive score
  and seed `113` nearly reaches the old CV cutoff.

Both families omit conductor/rank conditioning, central-zero structure,
bad-prime model uncertainty, and any conditioning on reciprocal-derivative or
Perron residue behavior. A stochastic pass is diagnostic evidence only, not a
theorem input.

## C2-prime Predeclared Diagnostic

Run C2-prime only on fresh seeds:

```text
st_iid:    seeds 512..1023
st_shared: seeds 128..255
```

Freeze the primary group:

```text
kernel = smoothstep
mode = all
alpha = 0.75
match = none
K grid = 1000,3000,10000,30000,100000,300000,1000000
curves = 37a1,11a1,389a1
real_ratio = 1.3473754929960748
real_max_cv = 0.063297427334436704
old_ratio_cutoff = 1.42083
old_cv_cutoff = 0.08567129
```

No relaxation of `old_cv_cutoff` is allowed. The first shared null near-pass
appears already if the CV cutoff is relaxed to `0.10`.

Pass clauses:

```text
st_iid old_pass_rate <= 0.01
st_iid primary_pass_rate <= 0.005
st_iid p_cv <= 0.01
st_iid p_pareto <= 0.01

st_shared old_pass_rate <= 0.02
st_shared p_cv <= 0.02
st_shared p_pareto <= 0.02
```

Report but do not gate on:

```text
p_ratio
additive p_score
best ratio row
best additive score row
pareto_score quantiles
```

C2-prime outcome labels:

| outcome | meaning |
|---|---|
| `C2P_FAIL` | stop EC numerical promotion lane; report diagnostic only |
| `C2P_PASS_DIAGNOSTIC` | unlock holdout curves as exploration only |
| `C2P_COMPUTE_BLOCKED` | script/cache/seed/provenance failure; no numerical inference |

No C2-prime outcome promotes an EC theorem.

## Holdout-Curve Gate Spec

Run only after `C2P_PASS_DIAGNOSTIC`.

Use the C1 predeclared holdout set. The three training curves are not holdouts:

```text
training = 11a1,37a1,389a1
```

Holdout curves:

```text
rank 0: 14a1,15a1,17a1,19a1,20a1,21a1,24a1
rank 1: 43a1,53a1,57a1,58a1,61a1
rank 2: 433a1,446d1,571b1
rank 3 sentinel: 5077a1
```

Hard prerequisites:

```text
exact ainvs, conductor, rank for every holdout
AP convention checked against the existing three-curve cache
script SHA256, metadata SHA256, AP-cache SHA256 recorded
product_complete=True for every raw row
no alpha/mode/kernel retuning after seeing holdouts
```

Primary fixed experiment:

```text
kernel = smoothstep
mode = all
alpha = 0.75
K grid = 1000,3000,10000,30000,100000,300000,1000000
proxy = zeta(2) * c_alpha(K) * P_alpha(K) / L2_alpha(K)^rank
```

Conjunctive diagnostic gates:

| gate | pass condition |
|---|---|
| `H0_repro` | training curves reproduce the existing AP-cache prefix and primary anchor before holdout metrics are trusted |
| `H1_global` | all-holdout cross-curve ratio `< 1.42083`, max within-curve CV `< 0.08567129`, and no curve mean outside `[0.80,1.80]` |
| `H2_rank` | rank 0, rank 1, and rank 2 strata each have ratio `< 1.42083`; every curve in those strata has CV `< 0.08567129` |
| `H3_conductor` | `N<=100` and `100<N<=1000` strata each have ratio `< 1.42083`; `5077a1` is not farther than factor `1.80` from the all-holdout median |
| `H4_tail` | tail grid `100000,150000,200000,300000,500000,700000,1000000`: each curve tail CV `< 0.060`, `abs(X(1000000)/mean_tail - 1) < 0.08`, and no last-three relative span `> 0.10` |
| `H5_load_bearing` | no proper ablation mode passes both the all-holdout ratio and max-CV gates; if `cP_only` is within `1%` of `all` on both ratio and max CV, label `ABLATION_FAIL` |

Holdout outcomes:

```text
HOLDOUT_PASS_DIAGNOSTIC
HOLDOUT_FAIL
HOLDOUT_COMPUTE_BLOCKED
```

Even `HOLDOUT_PASS_DIAGNOSTIC` only unlocks dense/larger `K` exploration.

## Denser/Larger-K Gate Spec

Run only after `C2P_PASS_DIAGNOSTIC` and `HOLDOUT_PASS_DIAGNOSTIC`.

Stage order:

```text
1. cache-only dense replay through Kmax=1000000
2. exact extension to Kmax=3000000
3. optional Kmax=10000000 confirmation only if Kmax=3000000 passes
```

Dense primary grid:

```text
12 points per decade from 10^3 to Kmax, rounded to distinct integers
force anchors = 1000,3000,10000,30000,100000,300000,1000000,3000000,10000000
```

Tail stress grid:

```text
24 points per decade on [100000,Kmax]
modes = all,cP_only,P_only,PL2_only,sharp
alphas = 0.65,0.70,0.75,0.80,0.85
headline remains smoothstep/all/alpha=0.75
```

Add required tail metrics:

```text
tail_cv_decade
tail_cv_half_decade
last_step_rel
max_abs_log_slope_tail
tail_range_rel
endpoint_leverage
pointwise_cross_ratio_tail
ablation_delta_tail
```

Conjunctive diagnostic gates:

| gate | pass condition |
|---|---|
| `K0_repro` | seven-point anchor reproduces before dense metrics are trusted |
| `K1_dense_old_gate` | smoothstep/all/alpha=0.75 passes old ratio and old CV on the full dense grid |
| `K2_tail_old_gate` | top decade and top half-decade each pass old ratio and old CV |
| `K3_slope` | `max_abs_log_slope_tail <= 0.03` for every curve |
| `K4_last_step` | `abs(last_step_rel) <= 0.08` for every curve at the final dense-grid step |
| `K5_endpoint_leverage` | removing the largest K leaves old-gate status unchanged and changes ratio and max CV by at most `0.02` absolute |
| `K6_pointwise_tail` | tail pointwise cross-ratio median `< 1.42083` and max `< 1.80` |
| `K7_load_bearing_tail` | `all` is not numerically indistinguishable from `cP_only`, `P_only`, or `PL2_only`; if ratio/CV deltas are both within `1%`, label `ABLATION_FAIL` |
| `K8_3e6_confirmation` | `Kmax=3000000` passes `K1` through `K7`; do not run `Kmax=10000000` unless this passes |

Dense-K outcomes:

```text
DENSE_K_PASS_DIAGNOSTIC
DENSE_K_FAIL
DENSE_K_COMPUTE_BLOCKED
```

Any `DENSE_K_PASS_DIAGNOSTIC` remains finite numerical evidence only.

## Decision Boundary

Promotion is blocked at three independent levels:

```text
1. G3 has already failed its predeclared empirical-p gates.
2. C2-prime, holdout, and dense-K gates are diagnostics only.
3. EC smoothing still needs H1/H2 theorem closure before theorem language.
```

Recommended next move if EC numerics continue:

```text
freeze C2-prime implementation and fresh seed blocks;
run C2-prime once;
if it fails, stop numerical promotion work;
if it passes, run holdouts;
if holdouts pass, run dense/larger K;
in all cases, keep theorem work on H1/H2 as the main lane.
```

## Verification Notes

Verified inputs:

- `./te doctor` returned `ok: true`.
- Loaded `start.md`, root `L1_index.md`, and `primes-equispaced/L1_index.md`.
- Loaded the requested G3/C2-prime/stochastic/kernel reports.
- Inspected stochastic CSV headers and script metric definitions.
- Inspected deterministic kernel-suite holdout/tail gate definitions.
- Loaded C1/C3 blocker protocols to preserve existing holdout and dense-K
  gate design.

No long compute was run. No stochastic seeds were regenerated. No theorem was
promoted. No Koyama correspondence or email draft was edited.

## Changed Files

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT07_EC_G3_C2_PRIME_DIAGNOSIS_2026-05-11.md`
