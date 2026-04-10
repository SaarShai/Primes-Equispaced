# Series 9-11 Experiment Plan

## Series 9: Stability Test (Variance Measurement)

**Question:** How much does PSNR vary across random seeds for each method?

**Setup:**
- Same scene (medium complexity, our standard)
- Same config (6000 steps, interval=200, max_new=30)
- 20 random seeds per method (B and C)
- Measure: mean PSNR, std PSNR, min PSNR, max PSNR, coefficient of variation

**What we expect:**
- Farey: low variance (stable ~28-29 dB regardless of seed)
- ADC: high variance (swings 27-32 dB depending on seed)

**Metrics for paper:**
- Box plot of PSNR distributions
- Coefficient of variation (CV = std/mean)
- "Worst-case guarantee" — minimum PSNR across 20 seeds

**Runtime:** 40 runs × ~10 min = ~7 hours

**Additional sub-experiments:**
- 9a: Variance at max_new=10 (tight budget)
- 9b: Variance at max_new=30 (medium budget)
- 9c: Variance at max_new=100 (generous budget)
- 9d: Variance at max_new=unlimited

This directly supports the paper section "Farey Provides Hyperparameter Robustness."

---

## Series 10: Comparison vs State-of-the-Art Densification

**Question:** How does Farey compare to the best published densification methods?

**Baselines to implement:**
1. **Vanilla ADC** (Kerbl et al. SIGGRAPH 2023) — gradient threshold, split+clone
2. **Error-gated ADC** (our fair baseline) — error-guided insertion
3. **SteepGS-style** (CVPR 2025) — split along least eigenvalue of splitting matrix, 2 offspring
4. **Mini-Splatting-style** (ECCV 2024) — blur-based split criterion + importance sampling
5. **Farey-guided** (ours)

**What we measure:**
- PSNR at fixed Gaussian budget (500, 1000, 2000)
- Gaussian count at fixed PSNR target (25, 27, 29 dB)
- Training time to reach target quality
- PSNR variance across 5 seeds

**Implementation notes:**
- SteepGS: approximate by splitting along the axis of maximum scale (simplified eigenvalue)
- Mini-Splatting: approximate by computing per-Gaussian blur contribution and splitting high-blur Gaussians

**Scenes:** Medium + Hard (from Series 4)

**Runtime:** 5 methods × 2 scenes × 5 seeds = 50 runs × ~10 min = ~8 hours

---

## Series 11: Stability Comparison vs Most Stable Methods

**Question:** Is Farey MORE stable than methods specifically designed for consistent quality?

**Methods known for stability:**
1. **Scaffold-GS** (CVPR 2024) — anchor-based, structured grid provides inherent stability
2. **ControlGS** (2025) — uniform octree splitting, no heuristic thresholds
3. **Mini-Splatting** (ECCV 2024) — importance-based, theoretically more principled
4. **Farey-guided** (ours)

**Test protocol:**
- Same scene, 20 seeds per method, 3 budget levels (10, 30, 100)
- Measure CV (coefficient of variation) of PSNR across seeds
- Measure min-max PSNR range across seeds
- Measure sensitivity to budget parameter (CV of PSNR across budget levels)

**Metrics for paper:**
- "Budget sensitivity" = range of PSNR across different max_new values
  - ADC: 4.83 dB range (from Series 3)
  - Farey: 0.00 dB range (from Series 3) ← this is the killer number
  - Scaffold-GS: TBD
  - ControlGS: TBD

**Implementation notes:**
- Scaffold-GS: anchor grid with neural Gaussians — complex, may need simplified version
- ControlGS: uniform 8-way split + opacity pruning — simpler to implement

**Runtime:** 4 methods × 3 budgets × 20 seeds = 240 runs × ~10 min = ~40 hours

---

## Priority Order

1. **Series 9** (7 hours) — proves the stability claim with statistical rigor
2. **Series 10** (8 hours) — compares against published methods
3. **Series 11** (40 hours) — comprehensive stability comparison

Total: ~55 hours (~2.5 days of continuous computation)

## Queue Order After Current Work

After Series 4+5 complete:
→ Series 6-8 (real 3D, ~5-6 days)
→ Series 9 (stability proof, ~7 hours)
→ Series 10 (SOTA comparison, ~8 hours)
→ Series 11 (stability comparison, ~40 hours)
