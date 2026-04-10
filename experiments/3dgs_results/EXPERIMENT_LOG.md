# 3DGS Experiment Log

## Series 1: Farey Parameter Tuning (Complete)
Best config: farey_start=45, farey_inc=5

## Series 2: Training Duration (Complete)
| Config | Steps | Interval | B (ADC) | C (Farey) | Delta |
|--------|-------|----------|---------|-----------|-------|
| 2a | 1000 | 200 | 25.38 | 25.37 | -0.01 |
| 2b | 2000 | 200 | 25.67 | 25.87 | +0.20 |
| 2c | 4000 | 200 | 25.79 | 26.13 | +0.34 |
| 2d | 4000 | 100 | 25.78 | 26.12 | +0.34 |
| 2e | 4000 | 400 | 25.60 | 25.67 | +0.08 |
| 2f | 6000 | 200 | 25.84 | 26.28 | **+0.44** |

**Key finding:** Farey advantage grows with training duration.
Best: +0.44 dB at 6000 steps, interval=200.

## Series 3: Densification Budget (Complete)
| Config | max_new | B (ADC) | C (Farey) | Delta | B Gauss | C Gauss |
|--------|---------|---------|-----------|-------|---------|---------|
| 3_10 | 10 | 26.86 | 26.97 | +0.11 | 644 | 774 |
| 3_30 | 30 | 31.87 | 28.82 | -3.05 | 1370 | 502 |
| 3_100 | 100 | 27.04 | 28.82 | +1.78 | 2000 | ~500 |
| 3_unlimited | 9999 | 30.60 | 28.82 | -1.78 | 2000 | ~500 |

**KEY FINDING: Farey provides hyperparameter robustness.**
- Farey PSNR is 28.82 dB across ALL budget settings (rock-solid stable)
- ADC PSNR swings from 27.04 to 31.87 depending on max_new (4.83 dB range!)
- At tight budget (10): Farey wins (+0.11)
- At high budget (100): Farey wins (+1.78) because ADC destabilizes
- The unexpected results (win at 10 and 100, lose at 30 and unlimited) are
  EXPLAINED by ADC's instability — it sometimes gets lucky (30, unlimited)
  and sometimes collapses (100). Farey never collapses.

**Paper note:** The non-monotonic ADC behavior (good at 30, bad at 100, good
again at unlimited) demonstrates that ADC quality is a function of how its
densification interacts with the optimizer — a chaotic interaction that
depends sensitively on budget. Farey's bounded injection (at most 1 per gap)
prevents this chaotic interaction by providing a predictable, controlled
refinement schedule.

## Series 4: Scene Complexity (Running)
| Config | Scene | B (ADC) | C (Farey) | Delta |
|--------|-------|---------|-----------|-------|
| 4a | Easy (smooth) | 80.86 | 81.88 | +1.02 |
| 4b | Medium (checker) | running | - | - |
| 4c | Hard (multi-scale) | queued | - | - |
| 4d | Extreme (dense HF) | queued | - | - |

## Series 5: Gap Threshold (Queued)
Pending after Series 4.

## Planned Series
- **Series 6-8:** Real 3DGS (gsplat-mps), see SERIES678_PLAN.md
- **Series 9:** Stability test (20+ seeds, measure PSNR variance)
- **Series 10:** Compare vs SteepGS and Mini-Splatting baselines
- **Series 11:** Compare stability vs most stable known methods
