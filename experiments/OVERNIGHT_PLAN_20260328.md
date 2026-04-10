# Overnight Plan — March 28-29, 2026

## Running Tasks (carry over)
1. **Aristotle (3 tasks):** sign_theorem extension, sorry elimination, density-1 formalization
2. **3DGS methods agent:** implementing Mini-Splatting, AbsGS, Pixel-GS

## Overnight Queue

### GPU Track: 3DGS Extended Benchmark
- Run all 8 methods: ADC, Farey, MCMC, Revising, SteepGS, Mini-Splatting, AbsGS, Pixel-GS
- Same hard target (50 bumps, budget 1500, 7000 steps, 50K samples)
- Save to 3dgs_results/extended_comparison.json
- Estimated: ~90 min GPU time

### Proof Track: Aristotle
- Collect all results from current 3 tasks
- Submit follow-ups based on results
- Priority: close the remaining sorry's
- Current sorry count: 3 (sign_theorem_conj, corrRatio_bounded, corrRatio_gt_neg_half)

### Monitor
- overnight-experiment-monitor enabled (every 15 min)
- Checks: Aristotle, 3DGS process, sorry count, crash detection

## Session Results Summary (4-hour window)

### Lean Formalization
- 230+ theorems (was 207), 3 sorry (was 0 — but 0 were about the Sign Theorem before)
- NEW: SignTheorem.lean with ΔW, wobble, four-term decomposition (corrected with -1 boundary)
- PROVED: ratio_test (corrected), four_term_decomposition, bPlusC_eq_shift_times_oneAddR, newDispSquaredSum_pos_general
- 20 sign theorems (p=13..113), 8 B+C positivity, 6 R>-1 bounds, CrossTerm extended to p=113

### 3DGS Benchmark
- Farey vs 5 SOTA methods on M5 Max GPU (MPS)
- Farey: MOST COMPACT (274 Gaussians vs 1500 for top methods), FASTEST training
- Quality: #3 behind Revising (+6.6dB) and SteepGS (+0.6dB)
- Key selling point: efficiency and compactness for real-time/mobile applications

### Research Findings
- Guth-Maynard: density-1 theorem achievable, large sieve doesn't directly transfer
- Large sieve: R does NOT tend to 0 (corrects wrong conjecture), but R>-0.26 empirically
- Smooth-rough decomposition lemma: novel, ΣD_smooth·δ = 0 exactly
- Spectral analysis: zeta zeros NOT significant in ΔW spectrum (p=0.30)
- AMR: marginal improvement (0-20%), 1D implementation flawed
- 3BP: AUC=0.79, cross-validated across all orbit families
