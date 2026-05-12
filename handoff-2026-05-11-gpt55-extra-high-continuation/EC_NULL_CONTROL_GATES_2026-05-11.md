---
schema_version: 1
title: "EC null-control gates for AGENT3 smoothed proxy"
date: 2026-05-11
type: report
tier: working
status: NO_GO
confidence: 0.76
sources:
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_2026-05-11.csv
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_METRICS_2026-05-11.csv
  - handoff-2026-05-11-gpt55-extra-high-continuation/EC_NULL_CONTROL_GATES_2026-05-11.py
tags: [ec-ndc, smoothing, null-controls, ablation, no-promotion]
---

# EC Null-Control Gates

status: `NO_GO`
first failing gate: `G2_primary_alpha_null_rejection`

## Scope

This audit is read-only over the saved `smoothstep` AGENT3 CSVs. It does not implement new kernel families or stochastic null simulations.
Primary case is predeclared as `all, alpha=0.75`.
Predeclared null modes are `cP_only, P_only, PL2_only`.

## Exact Command

- Command: `handoff-2026-05-11-gpt55-extra-high-continuation/EC_NULL_CONTROL_GATES_2026-05-11.py --force`
- Python: `3.9.6`
- Script SHA256: `ddbf4220eea5227f19cc878cf5274688830eebe93df7910f2cb230afea121c7c`
- Raw CSV SHA256: `3e0d3d504d78f6d0f807ba0677dc1e225d4075ec98b03b27d49b1a62bd6ddb9d`
- Metrics CSV SHA256: `719de44ab103119e2fe53e3e31f0193404fd199107a5260b47eb4a8f03904448`
- Summary CSV: `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/EC_NULL_CONTROL_ABLATION_SUMMARY_2026-05-11.csv`

## Gate Results

| gate | status | detail |
|---|---:|---|
| `G0_primary_anchor` | `PASS` | `all, alpha=0.75` ratio `1.3473754929960748`, max CV `0.063297427334436704`; anchor tolerance `5e-13` |
| `G1_primary_survival` | `PASS` | primary old gate `True`, leave-one-K `7/7`, leave-one-curve `3/3` |
| `G2_primary_alpha_null_rejection` | `FAIL` | passing primary-alpha nulls: `cP_only`, `PL2_only`, `P_only` |
| `G3_alpha_sweep_null_rejection` | `FAIL` | passing null mode/alpha rows `15` across modes `cP_only, P_only, PL2_only` |
| `G4_best_null_margin` | `FAIL` | best null `cP_only, alpha=0.75` score delta `7.9728811071266836e-05` versus required `0.01` |
| `G5_L2_smoothing_load_bearing` | `FAIL` | `all` vs `cP_only` at alpha `0.75` score delta `7.9728811071266836e-05` versus required `0.01` |

## Load-Bearing Ablation Summary

Primary score `log(ratio)+max_cv`: `0.3614560483477629`.
Best predeclared null: `cP_only, alpha=0.75`, score `0.36153577715883417`.
Best-null score delta versus primary: `7.9728811071266836e-05`.
Material margin required for load-bearing promotion: `0.01`.

| class | mode | alpha | old gate | ratio | max CV | score | score delta vs primary |
|---|---|---:|---:|---:|---:|---:|---:|
| `primary` | `all` | 0 | True | 1.4067934832480298 | 0.066157193795105734 | 0.40747018307908545 | 0.046014134731322542 |
| `primary` | `all` | 0.25 | True | 1.3786042051313698 | 0.061019865232229339 | 0.38209140698813471 | 0.020635358640371804 |
| `primary` | `all` | 0.5 | True | 1.359825674272148 | 0.063993107979051472 | 0.37134961882892226 | 0.0098935704811593528 |
| `primary` | `all` | 0.65 | True | 1.3592276762583548 | 0.066193602570005644 | 0.37311025590599722 | 0.01165420755823432 |
| `primary` | `all` | 0.75 | True | 1.3473754929960748 | 0.063297427334436704 | 0.3614560483477629 | 0 |
| `primary` | `all` | 0.85 | True | 1.3676209623121751 | 0.059774312812809476 | 0.37284701928777797 | 0.011390970940015066 |
| `primary` | `all` | 0.92 | True | 1.3927481408096773 | 0.066713363080442512 | 0.39799223809234568 | 0.036536189744582781 |
| `predeclared_null` | `cP_only` | 0.75 | True | 1.3474536199105895 | 0.063319173311522384 | 0.36153577715883417 | 7.9728811071266836e-05 |
| `predeclared_null` | `P_only` | 0.75 | True | 1.3690514798829585 | 0.065162093522829645 | 0.37928024312721154 | 0.017824194779448632 |
| `predeclared_null` | `PL2_only` | 0.75 | True | 1.3689713655053704 | 0.0651323248451188 | 0.37919195457429511 | 0.017735906226532205 |

Passing predeclared null rows:

| mode | alpha | ratio | max CV | score |
|---|---:|---:|---:|---:|
| `cP_only` | 0 | 1.4073013023288647 | 0.066797792922392754 | 0.40847169335190309 |
| `cP_only` | 0.25 | 1.3788260745364742 | 0.061327234264609572 | 0.38255970078239859 |
| `cP_only` | 0.5 | 1.359780745442883 | 0.064154232089411178 | 0.37147770225446564 |
| `cP_only` | 0.65 | 1.3593274654739098 | 0.066235566505953275 | 0.37322563326223412 |
| `cP_only` | 0.75 | 1.3474536199105895 | 0.063319173311522384 | 0.36153577715883417 |
| `cP_only` | 0.85 | 1.367605626319518 | 0.05978060629123727 | 0.37284209907537591 |
| `cP_only` | 0.92 | 1.3927526296315482 | 0.066717844123676165 | 0.39799994212651763 |
| `P_only` | 0.65 | 1.4008896786386076 | 0.070275780316219172 | 0.40738329984437022 |
| `P_only` | 0.75 | 1.3690514798829585 | 0.065162093522829645 | 0.37928024312721154 |
| `P_only` | 0.85 | 1.366515830251503 | 0.060251761567118804 | 0.37251607240960705 |
| `P_only` | 0.92 | 1.4003233218860602 | 0.074967291470311989 | 0.411670445632346 |
| `PL2_only` | 0.65 | 1.4007854162221256 | 0.070220777271914295 | 0.407253868172191 |
| `PL2_only` | 0.75 | 1.3689713655053704 | 0.0651323248451188 | 0.37919195457429511 |
| `PL2_only` | 0.85 | 1.3665311924986026 | 0.060240037574336124 | 0.37251559026299225 |
| `PL2_only` | 0.92 | 1.4003187470373801 | 0.074962683151305803 | 0.41166257031343945 |

## Leave-One-K Diagnostics

Pass count: `7/7`.
Ratio range: `1.331450602331709` to `1.3705117170902625`.
Max-CV range: `0.051639475223074015` to `0.068090710814448313`.

| held-out K | old gate | ratio | max CV |
|---:|---:|---:|---:|
| 1000 | True | 1.3416286318694279 | 0.067515330265573714 |
| 3000 | True | 1.3659859494650461 | 0.05648338649978768 |
| 10000 | True | 1.3705117170902625 | 0.051639475223074015 |
| 30000 | True | 1.3588243514729232 | 0.066393109801078792 |
| 100000 | True | 1.3462820640463853 | 0.068090710814448313 |
| 300000 | True | 1.331450602331709 | 0.06074606690560657 |
| 1000000 | True | 1.3548824394358756 | 0.06421203509125957 |

## Leave-One-Curve Diagnostics

| held-out curve | old gate | holdout ratio | holdout CV |
|---|---:|---:|---:|
| `37a1` | True | 1.1597262732614431 | 0.040314798205058552 |
| `11a1` | True | 1.3467724722662582 | 0.015589562672353854 |
| `389a1` | True | 1.1612847818639083 | 0.063297427334436704 |

## Clean Rerun Command

Writes to a fresh rerun directory under this handoff folder and leaves original AGENT3 outputs untouched.

```bash
mkdir -p '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun'
python3 '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py' --workers 8 --ap-cache '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT3_EC_AP_TABLE_1000000.csv' --ap-cache-out '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun/AGENT3_EC_AP_TABLE_1000000.csv' --raw-csv '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun/AGENT3_EC_SMOOTHED_PROXY.csv' --metrics-csv '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun/AGENT3_EC_SMOOTHED_PROXY_METRICS.csv' --report '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun/AGENT3_EC_SMOOTHED_PROXY_SUMMARY.md'
python3 '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/EC_NULL_CONTROL_GATES_2026-05-11.py' --raw-csv '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun/AGENT3_EC_SMOOTHED_PROXY.csv' --metrics-csv '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun/AGENT3_EC_SMOOTHED_PROXY_METRICS.csv' --summary-csv '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun/EC_NULL_CONTROL_ABLATION_SUMMARY.csv' --report '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/ec-null-control-rerun/EC_NULL_CONTROL_GATES.md'
```

## Do Not Promote Unless

- A predeclared alpha, preferably `0.75`, survives holdout curves across ranks/conductors.
- The signal survives a denser K grid and larger K, with tail-only drift controlled.
- Component ablation shows the proposed normalization is load-bearing, not merely endpoint smoothing.
- A theorem explains the smoothing kernel and normalization from an explicit Euler/Perron transform.

## Next Controls

- Implement the C2 primary kernel suite: smoothstep, hann, riesz, exponential, gaussian.
- Run stochastic nulls: Sato-Tate iid/shared, prime-order permutation, sign-randomization.
- Add rank and curve-label permutation controls for the `L2^rank` denominator.
- Extend to holdout curves and a denser/larger K grid before any promotion.
