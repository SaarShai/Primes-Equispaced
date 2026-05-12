---
schema_version: 1
title: "EC G3 stochastic null failure diagnostic"
date: 2026-05-11
type: diagnostic
tier: working
status: G3_FAIL_DIAGNOSED_NO_PROMOTION
confidence: 0.78
sources:
  - handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py
  - handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_REPORT_2026-05-11.md
  - handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_METRICS_2026-05-11.csv
  - handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_RAW_2026-05-11.csv
  - handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_RAW_2026-05-11.csv
  - handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md
tags: [ec-ndc, smoothing, g3, null-controls, diagnostic]
---

# EC G3 Failure Diagnostic

status: `G3_FAIL_DIAGNOSED_NO_PROMOTION`

## Verdict

Full G3 failed the predeclared empirical-p gates. Do not promote the EC
smoothed finite pattern.

The failure is more specific than "Sato-Tate nulls pass the old gate":

- no stochastic seed passes the old gate;
- no stochastic seed passes the primary gate;
- no stochastic seed has max CV below the old CV cutoff;
- no stochastic seed has max CV below the real max CV;
- but many stochastic seeds beat the real ratio alone, and a few shared seeds
  beat the additive score.

So the current G3 failure is a metric-specific empirical specificity failure:
the ratio-only and additive-score p-tests are not cleared, even though the
literal two-component old/primary pass tests are cleared.

## Fixed Real Anchor

```text
real ratio  = 1.3473754929960748
real max CV = 0.063297427334436704
real score  = 0.3614560483477629
old ratio cutoff = 1.42083
old CV cutoff    = 0.08567129
primary score cutoff = real score + 0.005
```

## G3 Summary

| family | seeds | old pass | primary pass | p_ratio | p_score | status |
|---|---:|---:|---:|---:|---:|---|
| `st_iid` | `512/512` | `0` | `0` | `0.062378167641325533` | `0.0019493177387914229` | `FAIL` |
| `st_shared` | `128/128` | `0` | `0` | `0.16279069767441862` | `0.046511627906976744` | `FAIL` |

Predeclared thresholds:

```text
iid:    p_ratio <= 0.01 and p_score <= 0.01
shared: p_score <= 0.02
```

Failing clauses:

```text
st_iid:    p_ratio = 0.062378167641325533 > 0.01
st_shared: p_score = 0.046511627906976744 > 0.02
```

## Failure Mode Counts

| family | ratio <= real | score <= real | CV < old cutoff | CV <= real CV | old pass | primary pass |
|---|---:|---:|---:|---:|---:|---:|
| `st_iid` | `31/512` | `0/512` | `0/512` | `0/512` | `0/512` | `0/512` |
| `st_shared` | `20/128` | `5/128` | `0/128` | `0/128` | `0/128` | `0/128` |

This is the main diagnostic split:

- `ratio` alone is not specific enough;
- `max CV` is highly specific;
- the additive score can be beaten by nulls with much better ratio but worse CV.

## Quantiles

| family | metric | min | q01 | q05 | median | q95 |
|---|---|---:|---:|---:|---:|---:|
| `st_iid` | ratio | `1.0454966645724264` | `1.1019731461791635` | `1.2697014495049983` | `2.6033032660910753` | `9.82679540063852` |
| `st_iid` | max CV | `0.1863103952371311` | `0.2110780198978008` | `0.26573762889956165` | `0.6331796328908827` | `12.21852465383352` |
| `st_iid` | score | `0.3635888873390998` | `0.4898502462961392` | `0.7740542027262431` | `1.7030627412717598` | `8.469177915475896` |
| `st_shared` | ratio | `1.0305984856846804` | `1.0417202830938432` | `1.1151079033993918` | `1.9174021320005434` | `5.223699830082381` |
| `st_shared` | max CV | `0.09678231388824925` | `0.10586873482377705` | `0.14219571271762793` | `0.33506273178387413` | `3.972042872361214` |
| `st_shared` | score | `0.24592503586956727` | `0.26255343255293867` | `0.4109276387275393` | `1.0970435581251494` | `4.498492605783533` |

## Closest Nulls

### Best iid score

Seed `398`:

```text
ratio = 1.0955148176893732
max CV = 0.27236448141701425
score = 0.36358888733909978
```

Per-curve profiles:

| curve | mean | CV | K-profile |
|---|---:|---:|---|
| `37a1` | `1.2472254572135308` | `0.16469047519503452` | `1.16333, 1.16728, 1.54893, 1.55115, 1.1915, 0.952002, 1.15638` |
| `11a1` | `1.1525159085318015` | `0.2625137791357746` | `1.10037, 0.943731, 0.884057, 0.916443, 1.10453, 1.30087, 1.8176` |
| `389a1` | `1.138483420830529` | `0.27236448141701425` | `1.18113, 0.781429, 0.693707, 1.06112, 1.3375, 1.6776, 1.2369` |

Interpretation: ratio is much better than real, but CV is more than `4x` the
real max CV and more than `3x` the old CV cutoff. It is not an old-gate near
pass.

### Best shared score

Seed `113`:

```text
ratio = 1.1608386545795315
max CV = 0.096782313888249247
score = 0.24592503586956727
```

Per-curve profiles:

| curve | mean | CV | K-profile |
|---|---:|---:|---|
| `37a1` | `1.2303081698827456` | `0.07722426398842097` | `1.22806, 1.07199, 1.24552, 1.40687, 1.28489, 1.19271, 1.18212` |
| `11a1` | `1.1457886302346338` | `0.09678231388824925` | `1.14279, 1.08745, 1.09096, 1.2971, 1.32759, 1.04683, 1.0278` |
| `389a1` | `1.3300757319540968` | `0.09153487018597035` | `1.26133, 1.1378, 1.30343, 1.57214, 1.38229, 1.32878, 1.32475` |

Interpretation: this is the real warning row. It misses the old CV cutoff
(`0.09678 > 0.08567`) but only by about `13%`, and its ratio is much better
than the real ratio. The additive score ranks it better than real.

## Sensitivity

Counts for hypothetical CV cutoffs while keeping the old ratio cutoff:

| family | CV cutoff | ratio < old count | ratio <= real count |
|---|---:|---:|---:|
| `st_iid` | `0.08567129` | `0` | `0` |
| `st_iid` | `0.20` | `0` | `0` |
| `st_iid` | `0.30` | `1` | `1` |
| `st_iid` | `0.35` | `9` | `8` |
| `st_shared` | `0.08567129` | `0` | `0` |
| `st_shared` | `0.10` | `1` | `1` |
| `st_shared` | `0.12` | `2` | `1` |
| `st_shared` | `0.20` | `6` | `3` |
| `st_shared` | `0.35` | `18` | `10` |

The old CV cutoff is load-bearing. Relaxing it even slightly in the shared
family admits the first null near-pass.

Counts for additive score slack:

| family | slack over real score | count |
|---|---:|---:|
| `st_iid` | `0` | `0` |
| `st_iid` | `0.005` | `1` |
| `st_iid` | `0.20` | `10` |
| `st_shared` | `0` | `5` |
| `st_shared` | `0.005` | `5` |
| `st_shared` | `0.20` | `16` |

The additive score is not equivalent to the old gate. Low ratio can compensate
for CV failure.

## Decision Boundary

Claim-safe interpretation:

1. The full G3 result is a genuine `G3_FAIL` under the predeclared gate.
2. It is not evidence that random nulls literally pass the old/primary gate.
3. It is evidence that the current empirical score/ratio specificity tests are
   too weakly separated from Sato-Tate nulls on this finite grid.
4. This blocks EC smoothing promotion before holdout curves or denser/larger
   `K`.

## Next EC Move

Do not silently replace G3 after seeing the result. If EC numerics continue,
the next honest step is a new predeclared diagnostic gate `C2-prime`, not a
promotion gate:

- keep old/primary pass rates;
- add Pareto empirical tests such as `ratio <= real_ratio` and
  `max_cv <= real_max_cv`;
- add CV-only empirical p-values;
- replace the additive score or normalize it so CV cannot be bought by ratio;
- only then run holdout curves and denser/larger `K` as exploration.

The research-priority route after this diagnostic is theory-first:
`H1-weighted-l1(E,W,epsilon)` / fixed-weight PV, plus H2 endpoint packaging.
