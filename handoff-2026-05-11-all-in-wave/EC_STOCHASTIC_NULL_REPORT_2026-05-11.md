---
schema_version: 1
title: "EC stochastic Sato-Tate null controls"
date: 2026-05-11
type: report
tier: working
status: G3_FAIL
confidence: 0.70
sources:
  - handoff-2026-05-11-ec-smoothing-blockers/C2_KERNEL_NULL_CONTROL_PLAN.md
  - handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py
tags: [ec-ndc, smoothing, sato-tate, null-controls]
---

# EC Stochastic Sato-Tate Null Controls

status: `G3_FAIL`

## Verdict

Do not promote from this run. Full G3 was run at the predeclared size and gives `0` old-gate and `0` primary-gate passes in both null families, but the empirical p gates fail: iid `p_ratio=0.062378167641325533 > 0.01`, and shared `p_score=0.046511627906976744 > 0.02`.

## Exact Run

- Command: `handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py --iid-seeds 512 --shared-seeds 128 --force`
- Python: `3.9.6`
- NumPy: `2.0.2`
- Script SHA256: `fc203d8b434f99f37c9a5fd09fba367b1079c204830427ab0f814265860451df`
- AP cache: `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT3_EC_AP_TABLE_1000000.csv`
- AP cache SHA256: `830c19a1bd5d134e83e662f65bfb2b3fce252fef1ed5d74234234bec14920132`
- K grid: `1000,3000,10000,30000,100000,300000,1000000`
- iid seeds: `0..511`
- shared seeds: `0..127`
- Elapsed seconds: `1723.058`

## Summary

| family | trials | old pass | primary pass | best ratio | best score | p_ratio | p_score | status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `st_iid` | 512/512 | 0 (0) | 0 (0) | 1.0454966645724264 | 0.36358888733909978 | 0.062378167641325533 | 0.0019493177387914229 | `FAIL` |
| `st_shared` | 128/128 | 0 (0) | 0 (0) | 1.0305984856846804 | 0.24592503586956727 | 0.16279069767441862 | 0.046511627906976744 | `FAIL` |

## Best Null Rows

| family | seed | pass old | pass primary | ratio | max CV | score | means (37a1, 11a1, 389a1) |
|---|---:|---:|---:|---:|---:|---:|---|
| `st_iid` | 398 | `False` | `False` | 1.0955148176893732 | 0.27236448141701425 | 0.36358888733909978 | 1.2472254572135308, 1.1525159085318015, 1.138483420830529 |
| `st_iid` | 417 | `False` | `False` | 1.061267038525225 | 0.31031678868123774 | 0.36978030234321929 | 1.0850891479924669, 1.1408180940947721, 1.151569346625825 |
| `st_iid` | 510 | `False` | `False` | 1.0901499758211637 | 0.33952879369363292 | 0.42584407296618637 | 0.98085719039435104, 1.0692814423924164, 1.0619179591472849 |
| `st_iid` | 27 | `False` | `False` | 1.0747305293804807 | 0.39449706642656562 | 0.46656702623939095 | 1.4262269637910379, 1.3270554104508172, 1.3579329085710712 |
| `st_iid` | 387 | `False` | `False` | 1.1186549642011367 | 0.35894042950061317 | 0.47106746829913732 | 1.1220848676625299, 1.25118202745735, 1.1184700086240216 |
| `st_iid` | 474 | `False` | `False` | 1.1566239317221603 | 0.34434488832592669 | 0.48985024629613921 | 1.216122426559711, 1.0514415214882855, 1.1793438374424026 |
| `st_iid` | 198 | `False` | `False` | 1.1980733314365515 | 0.32733446879991335 | 0.50804917816952955 | 1.4953609581303451, 1.5273689771521146, 1.791552084807376 |
| `st_iid` | 34 | `False` | `False` | 1.2241597744600095 | 0.32413745688122764 | 0.52639216714200088 | 1.1390107548703112, 1.3092614477142397, 1.0695184362611241 |
| `st_shared` | 113 | `False` | `False` | 1.1608386545795315 | 0.096782313888249247 | 0.24592503586956727 | 1.2303081698827456, 1.1457886302346338, 1.3300757319540968 |
| `st_shared` | 15 | `False` | `False` | 1.1122509670375784 | 0.15616757240666065 | 0.26255343255293867 | 0.66711243815724852, 0.65409534380152246, 0.72751817867802071 |
| `st_shared` | 90 | `False` | `False` | 1.0595314615674554 | 0.21309488335102558 | 0.27092167636732556 | 1.1407552487083488, 1.1702111805996989, 1.2086660759547028 |
| `st_shared` | 1 | `False` | `False` | 1.1603922504072572 | 0.14073941163583784 | 0.28949750649814016 | 0.95376760319239984, 1.010667001711913, 0.87097014079265367 |
| `st_shared` | 48 | `False` | `False` | 1.1621918101654758 | 0.20751868914574176 | 0.35782640294229656 | 0.81536481843928776, 0.71834616785343652, 0.83485603314301815 |
| `st_shared` | 66 | `False` | `False` | 1.0305984856846804 | 0.34043459577751245 | 0.37057428333530545 | 0.94650131834463891, 0.92669741865970023, 0.95505295635858933 |
| `st_shared` | 99 | `False` | `False` | 1.3567049158684092 | 0.10586873482377705 | 0.41092763872753929 | 1.1050994406665713, 0.94712886013253361, 1.2849743805026514 |
| `st_shared` | 49 | `False` | `False` | 1.2344516268894781 | 0.22551971278622904 | 0.43614655744693515 | 0.64006319809187062, 0.75007554668407472, 0.60761841966548757 |

## Decision

Full G3 is `G3_FAIL`. The finite EC smoothing pattern remains non-theorem evidence; any EC continuation should first explain or revise the empirical-p failure before treating holdout curves or larger/denser `K` as promotion gates.

## Files

- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_RAW_2026-05-11.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_METRICS_2026-05-11.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_SUMMARY_2026-05-11.csv`
- `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_REPORT_2026-05-11.md`
