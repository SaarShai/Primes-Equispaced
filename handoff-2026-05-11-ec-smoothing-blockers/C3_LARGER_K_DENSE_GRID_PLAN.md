---
schema_version: 1
title: "C3 larger/denser K grid plan"
date: 2026-05-11
type: plan
tier: working
status: COMPUTE_BLOCKED
confidence: 0.74
sources:
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_NDC_BEYOND_BAD_PRIMES.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md
tags: [ec-ndc, smoothing, blockers, larger-k, dense-grid]
---

# C3 Larger/Denser K Grid Plan

status: `COMPUTE_BLOCKED`

## Verdict

Do not promote. The `K<=1000000` smoothed proxy is reproducible, but the
existing seven-point grid is too sparse to rule out endpoint damping. At
`alpha=0.75`, `mode=all`, the last observed step `300000 -> 1000000` is still
large for `389a1`: `1.71095327841 -> 1.51321181870`, a relative move of
`-11.5574%`. The same numbers are effectively identical for `cP_only`, so the
`L2^rank` factor is still not load-bearing.

## Current Tail Facts From Existing CSV

For `alpha=0.75`, `mode=all`, using only the existing `K=100000,300000,1000000`
tail points:

| curve | X(100000) | X(300000) | X(1000000) | last-step drift | tail CV |
|---|---:|---:|---:|---:|---:|
| `37a1` | `1.56385329031` | `1.67816787391` | `1.65787946139` | `-1.2090%` | `3.0490%` |
| `11a1` | `1.16229935588` | `1.16894068117` | `1.16269999004` | `-0.5339%` | `0.2611%` |
| `389a1` | `1.57572723609` | `1.71095327841` | `1.51321181870` | `-11.5574%` | `5.1580%` |

The blocker is not "more rows" in the old mean/CV gate. The blocker is proving
that the tail has settled rather than being shaped by smooth cutoff position.

## Complexity Estimate

The exact `a_p` extension bottleneck is `ap_all_curves_for_prime(p)` in
`handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py`: for each missing
prime it allocates arrays of length `p` and evaluates all residues mod `p`.
Cost is therefore proportional to `sum p` over missing primes.

Measured prior exact extension:

| extension | missing primes | sum missing primes | observed time |
|---|---:|---:|---:|
| `100000 -> 1000000` | `68906` | `37096005486` | `267.953s` to `338.108s` |

Read-only sieve counts for the next ranges:

| extension | missing primes | sum missing primes | weight ratio vs `100000 -> 1000000` | time estimate |
|---|---:|---:|---:|---:|
| `1000000 -> 3000000` | `138318` | `274920670242` | `7.4111x` | `33-42 min` |
| `1000000 -> 10000000` | `586081` | `3165774592333` | `85.3400x` | `6.35-8.02 h`, likely worse under memory pressure |

`K=3000000` is feasible as a scheduled exact run. `K=10000000` is feasible only
as an overnight run with conservative worker count or after improving `a_p`.
CSV size is not the limiter: the `K=1000000` `a_p` table is `2.7M`; a `K=1e7`
table should still be tens of MB. CPU and per-worker array memory are the
limiters.

## Dense Grid Protocol

Use a predeclared log grid, not hand-picked endpoints.

Primary grid:

- `12` points per decade from `10^3` to `Kmax`, rounded to distinct integers.
- Force anchors: `1000,3000,10000,30000,100000,300000,1000000,3000000,10000000`.
- For `Kmax=3000000`, this gives enough points to see whether the current
  `300000 -> 1000000` drop continues, reverses, or damps.

Tail stress grid:

- `24` points per decade on `[100000,Kmax]`.
- Run only after the primary grid, and only for `modes=all,cP_only,P_only,PL2_only,sharp`.
- Predeclare alphas `0.65,0.70,0.75,0.80,0.85`; keep old alphas only for
  compatibility tables.

## Tail Metrics To Add To The Report

These can be computed from raw CSV without changing the reproducer.

- `tail_cv_decade`: per-curve CV using `K >= Kmax/10`.
- `tail_cv_half_decade`: per-curve CV using `K >= Kmax/sqrt(10)`.
- `last_step_rel`: `(X(Kmax)-X(Kprev))/X(Kprev)` for the final log-grid step.
- `max_abs_log_slope_tail`: max of `abs(diff(log X)/diff(log K))` over the top
  decade.
- `tail_range_rel`: `(max_tail-min_tail)/median_tail`.
- `endpoint_leverage`: old gate metrics recomputed after removing the largest
  `K`; promote only if the decision is unchanged.
- `pointwise_cross_ratio_tail`: max and median over tail `K` of
  `max_curve X(K)/min_curve X(K)`, not just ratio of curve means.
- `ablation_delta_tail`: max over tail of
  `abs(log X_all - log X_cP_only)` and `abs(log X_all - log X_P_only)`.

Interpretation rule: if `all` and `cP_only` remain numerically indistinguishable
on the dense tail, the larger-`K` result is evidence for endpoint smoothing, not
for the proposed `L2^rank` denominator.

## Existing-Script Command Plan

Do not launch these casually. They are command plans for the compute window.

Cache-only dense replay through `K=1000000` first:

```bash
KGRID=$(python3 - <<'PY'
import math
vals={1000,3000,10000,30000,100000,300000,1000000}
for j in range(0, 37):
    vals.add(int(round(10 ** (3 + j / 12))))
print(",".join(map(str, sorted(v for v in vals if v <= 1000000))))
PY
)
python3 handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py \
  --max-k 1000000 \
  --k-grid "$KGRID" \
  --alphas 0.65,0.70,0.75,0.80,0.85 \
  --modes all,cP_only,P_only,PL2_only,sharp \
  --workers 6 \
  --ap-cache handoff-2026-05-11-gpt55-wave/AGENT3_EC_AP_TABLE_1000000.csv \
  --ap-cache-out handoff-2026-05-11-ec-smoothing-blockers/C3_EC_AP_TABLE_1000000_DENSE.csv \
  --raw-csv handoff-2026-05-11-ec-smoothing-blockers/C3_EC_SMOOTHED_PROXY_DENSE_1000000.csv \
  --metrics-csv handoff-2026-05-11-ec-smoothing-blockers/C3_EC_SMOOTHED_PROXY_DENSE_METRICS_1000000.csv \
  --report handoff-2026-05-11-ec-smoothing-blockers/C3_EC_SMOOTHED_PROXY_DENSE_1000000.md
```

Then exact extension to `K=3000000`:

```bash
KGRID=$(python3 - <<'PY'
import math
anchors={1000,3000,10000,30000,100000,300000,1000000,3000000}
vals=set(anchors)
top=math.log10(3000000)
j=0
while 3 + j / 12 <= top + 1e-12:
    vals.add(int(round(10 ** (3 + j / 12))))
    j += 1
print(",".join(map(str, sorted(v for v in vals if v <= 3000000))))
PY
)
python3 handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py \
  --max-k 3000000 \
  --k-grid "$KGRID" \
  --alphas 0.65,0.70,0.75,0.80,0.85 \
  --modes all,cP_only,P_only,PL2_only,sharp \
  --workers 6 \
  --ap-cache handoff-2026-05-11-gpt55-wave/AGENT3_EC_AP_TABLE_1000000.csv \
  --ap-cache-out handoff-2026-05-11-ec-smoothing-blockers/C3_EC_AP_TABLE_3000000.csv \
  --raw-csv handoff-2026-05-11-ec-smoothing-blockers/C3_EC_SMOOTHED_PROXY_DENSE_3000000.csv \
  --metrics-csv handoff-2026-05-11-ec-smoothing-blockers/C3_EC_SMOOTHED_PROXY_DENSE_METRICS_3000000.csv \
  --report handoff-2026-05-11-ec-smoothing-blockers/C3_EC_SMOOTHED_PROXY_DENSE_3000000.md
```

Do not attempt `K=10000000` until the `K=3000000` dense tail passes the new
tail metrics. If attempted with the current exact point counter, use `--workers
2` or `--workers 3` first to avoid per-prime array memory spikes.

## Algorithmic Improvements Before `K=10000000`

1. Replace exact `a_p` point counting. Current vectorized residue enumeration is
   simple and auditable, but it is `O(sum_{p<=K} p)`. A PARI/Sage/eclib/SEA path
   for fixed elliptic curves should make `K=10000000` routine instead of
   overnight.
2. Convert `spf` from a Python list of Python ints to a compact `uint32` array.
   This matters at `K=10000000`, where `list(range(K+1))` has large object
   overhead before any EC work begins.
3. Compute smoothed sums by prefix moments. The smoothstep kernel is polynomial
   on the transition interval, so `c`, `log P`, and `log L2` can be evaluated
   from prefix sums of `value`, `value*x`, `value*x^2`, and `value*x^3` instead
   of fresh dot products for every `(K,alpha,curve)`. This would make dense
   grids cheap once `a_p` is cached.
4. Build `mu` multiplicatively by sieve recurrence rather than refactoring every
   `n` separately for each curve. This is not the current blocker at `K=1e6`,
   but it becomes visible after `a_p` is fixed.
5. Split run stages: exact `a_p` cache generation, raw dense-grid evaluation,
   and tail-metric summarization. This prevents a failed report pass from
   wasting a completed expensive `a_p` extension.

## Do Not Promote Unless

Literal gate: do not promote unless all of the following hold.

- `alpha=0.75` or another predeclared alpha survives the dense primary grid and
  the tail stress grid.
- `tail_cv_decade`, `last_step_rel`, `max_abs_log_slope_tail`, and
  `endpoint_leverage` show the tail is stabilizing.
- `all` separates from `cP_only`, `P_only`, and `PL2_only` on the dense tail in a
  way that makes `L2^rank` load-bearing.
- `K=3000000` does not reproduce the current `389a1` endpoint swing, and any
  later `K=10000000` run confirms rather than reverses the `K=3000000` tail.
- Kernel-family and null-control tests fail to reproduce the same gate pass.
