---
schema_version: 1
title: "C1 holdout curve protocol for EC smoothing"
date: 2026-05-11
type: protocol
tier: working
status: COMPUTE_BLOCKED
confidence: 0.74
sources:
  - handoff-2026-05-11-ec-smoothing-blockers/DISPATCH_MANIFEST.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py
  - koyama-shared/data/PATH_B_20FORMS.csv
  - koyama-shared/data/RANK0_CLUSTER.json
  - koyama-shared/data/RANK3_5077A1.json
tags: [ec-ndc, smoothing, holdout, blockers]
---

# C1 Holdout Curve Protocol

status: `COMPUTE_BLOCKED`

## Verdict

Do not promote. The current smoothed proxy was trained/reproduced on only
`11a1`, `37a1`, and `389a1`. A promotion-quality holdout requires fresh curves
with predeclared ranks/conductor strata and no alpha/mode retuning. Local files
contain usable holdout labels, conductors, and ranks, but not the required
minimal Weierstrass `ainvs` or new `a_p` tables for those holdouts.

## Baseline Training Set

These are not holdouts.

| curve | ainvs | conductor | rank | local source |
|---|---|---:|---:|---|
| `11a1` | `(0,-1,1,-10,-20)` | `11` | `0` | `Koyama_EC_NDC_extended_sweep.py` |
| `37a1` | `(0,0,1,-1,0)` | `37` | `1` | `Koyama_EC_NDC_extended_sweep.py` |
| `389a1` | `(0,1,1,-2,0)` | `389` | `2` | `Koyama_EC_NDC_extended_sweep.py` |

Training result to beat, at `all, alpha=0.75`: cross-curve ratio
`1.3473754929960748`; max within-curve CV `0.063297427334436704`.

## Predeclared Holdout Curves

Use the following EC-only holdouts from `koyama-shared/data/PATH_B_20FORMS.csv`.
Exclude `Delta` because it is not an elliptic curve and exclude the three
training curves above.

| curve | ainvs | conductor | rank | stratum |
|---|---|---:|---:|---|
| `14a1` | `EXTERNAL_REQUIRED` | `14` | `0` | rank 0, low conductor |
| `15a1` | `EXTERNAL_REQUIRED` | `15` | `0` | rank 0, low conductor |
| `17a1` | `EXTERNAL_REQUIRED` | `17` | `0` | rank 0, low conductor |
| `19a1` | `EXTERNAL_REQUIRED` | `19` | `0` | rank 0, low conductor |
| `20a1` | `EXTERNAL_REQUIRED` | `20` | `0` | rank 0, low conductor |
| `21a1` | `EXTERNAL_REQUIRED` | `21` | `0` | rank 0, low conductor |
| `24a1` | `EXTERNAL_REQUIRED` | `24` | `0` | rank 0, low conductor |
| `43a1` | `EXTERNAL_REQUIRED` | `43` | `1` | rank 1, low conductor |
| `53a1` | `EXTERNAL_REQUIRED` | `53` | `1` | rank 1, low conductor |
| `57a1` | `EXTERNAL_REQUIRED` | `57` | `1` | rank 1, low conductor |
| `58a1` | `EXTERNAL_REQUIRED` | `58` | `1` | rank 1, low conductor |
| `61a1` | `EXTERNAL_REQUIRED` | `61` | `1` | rank 1, low conductor |
| `433a1` | `EXTERNAL_REQUIRED` | `433` | `2` | rank 2, mid conductor |
| `446d1` | `EXTERNAL_REQUIRED` | `446` | `2` | rank 2, mid conductor |
| `571b1` | `EXTERNAL_REQUIRED` | `571` | `2` | rank 2, mid conductor |
| `5077a1` | `EXTERNAL_REQUIRED` | `5077` | `3` | rank 3, high conductor |

Rank/conductor strata:

| stratum | curves | gate role |
|---|---|---|
| rank `0`, `N<=100` | `14a1,15a1,17a1,19a1,20a1,21a1,24a1` | primary within-rank holdout |
| rank `1`, `N<=100` | `43a1,53a1,57a1,58a1,61a1` | primary within-rank holdout |
| rank `2`, `100<N<=1000` | `433a1,446d1,571b1` | primary within-rank holdout |
| rank `3`, `N>1000` | `5077a1` | sentinel only; no ratio gate by itself |
| all EC holdouts | all 16 curves | global promotion gate |

## External Dependency

Exact dependency: a Cremona/LMFDB-compatible elliptic-curve metadata source
providing, for each holdout label, minimal integral `ainvs`, conductor, rank,
and `a_p` convention compatible with `ellap`.

Preferred source: SageMath with Cremona database or PARI/GP with `pari-elldata`,
then export:

```text
label,ainvs,conductor,rank
14a1,"(...)",14,0
...
```

Local blocker: `gp` is not installed in this environment, and no local holdout
`ainvs` table exists. Local scripts assume `gp` for arbitrary Cremona labels,
while `AGENT3_ec_smoothed_reproducer.py` and
`Koyama_EC_NDC_extended_sweep.py` hardcode only the three training curves.

Fallback if no external curve database is available: reduce the holdout to
`AUDIT_ONLY`. Do not substitute guessed `ainvs`. A weaker fallback may compute
point counts only for curves whose minimal `ainvs` are independently supplied in
a flat CSV committed by a later agent.

## Fixed Experiment

Primary target:

```text
mode = all
alpha = 0.75
K grid = 1000,3000,10000,30000,100000,300000,1000000
proxy = zeta(2) * c_alpha(K) * P_alpha(K) / L2_alpha(K)^rank
```

Secondary robustness, reported but not tunable:

```text
alphas = 0.65,0.75,0.85
modes = sharp,c_only,P_only,L2_only,cP_only,cL2_only,PL2_only,all
tail grid = 100000,150000,200000,300000,500000,700000,1000000
```

No holdout result may change the primary alpha, mode, curve list, or gates.
If `0.65` or `0.85` wins after seeing holdouts, that is a new experiment, not a
promotion of this one.

## Acceptance Gates

All gates below are conjunctive.

1. Primary all-holdout gate at `all, alpha=0.75`:
   - cross-curve ratio of per-curve means `< 1.42083`;
   - max within-curve CV over the seven-point K grid `< 0.08567129`;
   - no individual curve mean outside `[0.80, 1.80]`.

2. Rank-stratified gate:
   - rank `0`, rank `1`, and rank `2` strata each have cross-curve ratio
     `< 1.42083`;
   - each curve in those strata has within-curve CV `< 0.08567129`;
   - `5077a1` has within-curve CV `< 0.10` as a high-rank sentinel.

3. Conductor-stratified gate:
   - low-conductor EC holdouts `N<=100` have cross-curve ratio `< 1.42083`;
   - mid-conductor EC holdouts `100<N<=1000` have cross-curve ratio
     `< 1.42083`;
   - `5077a1` must not be an outlier by more than factor `1.80` from the
     all-holdout median.

4. Tail-drift gate:
   - over the tail grid, each curve has CV `< 0.060`;
   - for each curve, `abs(X(1000000)/mean_tail - 1) < 0.08`;
   - no monotone last-three-point drift with relative span `> 0.10`.

5. Ablation/load-bearing gate:
   - `all, alpha=0.75` passes every gate above;
   - no proper ablation mode passes both the all-holdout cross-ratio gate and
     max-CV gate;
   - if `cP_only` is within `1%` of `all` on both cross-ratio and max-CV, the
     `L2^rank` denominator is not load-bearing and status remains `NO_GO` for
     promotion.

6. Reproducibility gate:
   - every row has `product_complete=True`;
   - output records script SHA256, metadata SHA256, AP-cache SHA256, Python/NumPy
     versions, K grid, alpha grid, modes, and wall time;
   - generated `a_p` values for the three training curves match the existing
     `AGENT3_EC_AP_TABLE_1000000.csv` prefix exactly before any holdout result
     is trusted.

## Failure Modes

- `MISSING_METADATA`: any holdout lacks exact `ainvs`, conductor, or rank.
- `CONVENTION_MISMATCH`: bad-prime `a_p` or local inverse factors differ from
  the existing AGENT3 convention.
- `ALPHA_OVERFIT`: a non-primary alpha is selected after holdout inspection.
- `GLOBAL_FAIL`: all-holdout cross-ratio or max-CV gate fails.
- `STRATUM_FAIL`: rank or conductor stratum fails despite a global pass.
- `TAIL_FAIL`: endpoint smoothing hides tail drift.
- `ABLATION_FAIL`: `cP_only`, `P_only`, or another proper ablation passes with
  comparable metrics.
- `HIGH_RANK_OUTLIER`: `5077a1` breaks the sentinel factor/CV bound.
- `CACHE_FAIL`: AP cache incomplete, non-reproducible, or not hash-recorded.

Any failure mode blocks promotion. `MISSING_METADATA` or `CACHE_FAIL` is
`COMPUTE_BLOCKED`; `ABLATION_FAIL` is `NO_GO`; a clean numerical pass without a
theorem is still only `PROOF_CANDIDATE`.

## Fastest Feasible Implementation Route

1. Produce a small external metadata CSV for the 16 holdouts from SageMath or
   PARI/GP `pari-elldata`. This is the only missing input.
2. Fork, do not mutate, `AGENT3_ec_smoothed_reproducer.py` into a later
   holdout-specific script that loads curve metadata from CSV instead of
   hardcoded `CURVES`.
3. Generalize the existing vectorized point-count routine over an arbitrary
   curve list. For `p=2`, retain exhaustive long-model counting.
4. Write a holdout AP cache through `K=1000000`, then compute the fixed primary
   and secondary grids above.
5. Emit raw CSV, metrics CSV, and a markdown report with hashes and explicit
   pass/fail labels for every gate.

Expected compute scale: direct point counting to `K=1000000` for 16 holdouts is
roughly five to six times the current three-curve AGENT3 workload. Native
Sage/PARI `ellap` could be faster but must first be convention-checked against
the existing three-curve AP cache.

## do not promote unless

- exact holdout `ainvs`, conductors, and ranks are sourced and hash-recorded;
- `all, alpha=0.75` passes the global, rank-stratified, conductor-stratified,
  tail-drift, ablation, and reproducibility gates above;
- proper ablations do not reproduce the same pass;
- the result is reported as a finite smoothed proxy unless a separate theorem
  supplies the Euler/Perron mechanism.
