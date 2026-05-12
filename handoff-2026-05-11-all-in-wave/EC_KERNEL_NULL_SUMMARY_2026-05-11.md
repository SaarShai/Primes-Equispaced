---
schema_version: 1
title: "EC kernel/rank/curve-label null suite"
date: 2026-05-11
type: report
tier: working
status: STOCHASTIC_NULLS_NOT_RUN
confidence: 0.76
sources:
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md
tags: [ec-ndc, smoothing, kernels, null-controls, falsification]
---

# EC Kernel/Null Suite

status: `STOCHASTIC_NULLS_NOT_RUN`

## Verdict

Do not promote. The primary smoothstep result reproduces exactly and the deterministic C2 gates run here pass, including kernel robustness, rank permutations, curve-label permutations, and tail stability. Stochastic Sato-Tate nulls and larger/denser holdouts remain unrun.

## Exact Run

- Command: `handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py --force`
- Python: `3.9.6`
- NumPy: `2.0.2`
- Script SHA256: `6d775385d361e4df5995810db398b522cb46dcf58089c778799baabc8c6fab30`
- AP cache: `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT3_EC_AP_TABLE_1000000.csv`
- AP cache SHA256: `830c19a1bd5d134e83e662f65bfb2b3fce252fef1ed5d74234234bec14920132`
- K grid: `1000,3000,10000,30000,100000,300000,1000000`
- Alpha grid: `0.5,0.65,0.75,0.85,0.92`
- Modes: `all,cP_only,P_only,PL2_only`
- Elapsed seconds: `12.032`

## Gate Table

| gate | status | detail |
|---|---:|---|
| `G0_reproducibility` | `PASS` | finite_positive=True; anchor_ratio=1.3473754929960748; anchor_max_cv=0.063297427334436704 |
| `G1_primary_survival` | `PASS` | old=True; loo_k=7/7; leave_one_curve=True,True,True |
| `G2_none` | `PASS` | smoothstep(none):True; hann(none):True; riesz(2):True; exponential(3):True; gaussian(0.50):True |
| `G2_continuous` | `PASS` | smoothstep(none):True; hann(none):True; riesz(2):True; exponential(3):True; gaussian(0.50):True |
| `G2_discrete_both` | `PASS` | smoothstep(none):True; hann(none):True; riesz(2):True; exponential(3):True; gaussian(0.50):True |
| `G4_rank_specificity` | `PASS` | nonidentity_pass=0/5; identity_score=0.3614560483477629; best_nonidentity=0_1_2 score=1.3345275042237115 |
| `G4_curve_label_specificity` | `PASS` | nonidentity_pass=0/5; identity_score=0.3614560483477629; best_nonidentity=11a1_37a1_389a1 score=1.3345275042237115 |
| `G5_tail_stability` | `PASS` | tail_ratio=1.4023997514636641; tail_max_cv=0.05158036084512034; max_abs_slope=0.024791742743129768 |

## Primary Anchor

| ratio | max CV | score | tail ratio | tail max CV |
|---:|---:|---:|---:|---:|
| 1.3473754929960748 | 0.063297427334436704 | 0.3614560483477629 | 1.4023997514636641 | 0.05158036084512034 |

## Kernel Representatives

| match | kernel | param | pass | ratio | max CV |
|---|---|---:|---:|---:|---:|
| `none` | `smoothstep` | `none` | `True` | 1.3473754929960748 | 0.063297427334436704 |
| `none` | `hann` | `none` | `True` | 1.3471654079502935 | 0.06347917224624941 |
| `none` | `riesz` | `2` | `True` | 1.3564586812299859 | 0.064167367478000864 |
| `none` | `exponential` | `3` | `True` | 1.3643478380141667 | 0.067119268548343269 |
| `none` | `gaussian` | `0.50` | `True` | 1.3501844890221315 | 0.063421209137502918 |
| `continuous` | `smoothstep` | `none` | `True` | 1.3473754929960748 | 0.063297427334436704 |
| `continuous` | `hann` | `none` | `True` | 1.3471654079502935 | 0.06347917224624941 |
| `continuous` | `riesz` | `2` | `True` | 1.3466762605953893 | 0.065160715818036896 |
| `continuous` | `exponential` | `3` | `True` | 1.3433646465437687 | 0.072814118544054326 |
| `continuous` | `gaussian` | `0.50` | `True` | 1.3502914442881035 | 0.063421465774932684 |
| `discrete_both` | `smoothstep` | `none` | `True` | 1.3473754929960666 | 0.063297427334436843 |
| `discrete_both` | `hann` | `none` | `True` | 1.3471534484463787 | 0.063477470165776803 |
| `discrete_both` | `riesz` | `2` | `True` | 1.3464890309243982 | 0.065091281420660202 |
| `discrete_both` | `exponential` | `3` | `True` | 1.343655150182075 | 0.073502872575141528 |
| `discrete_both` | `gaussian` | `0.50` | `True` | 1.3503102734328718 | 0.063402637839905102 |

## Rank Permutations

Nonidentity old-gate passes: `0/5`.

| seed | pass | ratio | max CV | score |
|---|---:|---:|---:|---:|
| `identity` | `True` | 1.3473754929960748 | 0.063297427334436704 | 0.3614560483477629 |
| `0_1_2` | `False` | 3.5652353798472096 | 0.063297427334436704 | 1.3345275042237115 |
| `0_2_1` | `False` | 6.9123568686422683 | 0.063324047692216931 | 1.9966347081624274 |
| `2_0_1` | `False` | 7.2709491632090542 | 0.063324047692216931 | 2.0472108896164061 |
| `1_2_0` | `False` | 19.195187247721073 | 0.063350747123075798 | 3.0180103305541004 |
| `2_1_0` | `False` | 20.190975857974269 | 0.063350747123075798 | 3.0685865120080793 |

## Curve-Label Permutations

Nonidentity old-gate passes: `0/5`.

| seed | pass | ratio | max CV | score |
|---|---:|---:|---:|---:|
| `identity` | `True` | 1.3473754929960748 | 0.063297427334436704 | 0.3614560483477629 |
| `11a1_37a1_389a1` | `False` | 3.5652353798472096 | 0.063297427334436704 | 1.3345275042237115 |
| `389a1_37a1_11a1` | `False` | 6.9123568686422683 | 0.063324047692216931 | 1.9966347081624274 |
| `389a1_11a1_37a1` | `False` | 7.2709491632090542 | 0.063324047692216931 | 2.0472108896164061 |
| `37a1_389a1_11a1` | `False` | 19.195187247721073 | 0.063350747123075798 | 3.0180103305541004 |
| `11a1_389a1_37a1` | `False` | 20.190975857974269 | 0.063350747123075798 | 3.0685865120080793 |

## Files

- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_RAW_2026-05-11.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_METRICS_2026-05-11.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_CONTROL_SUMMARY_2026-05-11.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUMMARY_2026-05-11.md`

## Remaining Controls

Stochastic Sato-Tate nulls and larger/denser K holdouts are still separate gates. This run is enough to keep the EC smoothed proxy unpromoted if any permutation specificity gate fails.
