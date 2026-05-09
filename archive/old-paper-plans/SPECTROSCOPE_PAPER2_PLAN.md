# Farey Spectroscope — Paper 2 Research Plan
Created: 2026-04-05

## Overview
The spectroscope detects zeta zeros from Farey data with 0.8% accuracy using ~3,800 primes. To make a strong second paper, we need: rigorous theory, scaling, honest metrics, L-function breadth, and bulletproof null controls.

## 7 Tasks (Phase 1: all parallelizable)

### Task 1: Scale R(p) to 500K primes [CRITICAL]
- **Do:** Run `R_bound_1M` binary with max_p=500000 (~15,000 qualifying primes)
- **Then:** Rerun spectroscope on expanded data, measure gamma_1..gamma_9 detection
- **Resource:** Local machine, background process (6-12 hours)
- **Deliverable:** Convergence rate figure (error vs N_primes), gamma_4+ detection
- **Paper role:** Figure 2 — the "money figure" showing the method works at scale

### Task 2: Detrended Amplitude Correlation [CRITICAL]
- **Do:** The r=0.997 is inflated by shared monotonic decay. Compute honest metrics:
  - Log-detrend both F(gamma_k) and |c_k|^2, correlate residuals
  - Spearman rank correlation on consecutive ratios
  - Permutation test (1000 shuffles) for p-value
- **Resource:** Qwen 3.6 Plus (design metric) + Python (compute)
- **Deliverable:** Honest correlation value + p-value. If weak, pivot paper claims.
- **Paper role:** Credibility. Reviewers will spot the inflation instantly.

### Task 3: Convergence Rate Theory [CRITICAL]
- **Do:** Derive (under GRH) how fast error in gamma_k decreases with N primes
  - Signal: |a_j|^2 (N/log N)^2
  - Noise: cross-sums O(sqrt(N) log N) under GRH+LI
  - Peak width: ~2pi/log(p_max) (Rayleigh resolution limit)
  - Expected rate: O(1/log p_max) — verify against Task 1 data
- **Resource:** qwen3.5:35b (deep math reasoning, sequential)
- **Deliverable:** Conditional theorem or conjecture + fit with computational data
- **Paper role:** The theoretical backbone. Without it, the spectroscope is just a picture.

### Task 4: L-function Survey (chi mod q, q <= 20) [HIGH]
- **Do:** Compute F_chi(gamma) for all primitive characters mod q <= 20
  - Compare peaks against known L(s,chi) zeros (via mpmath)
  - Record: detection accuracy, SNR, number of zeros found per character
  - Identify failure modes (chi_5 failed previously — why?)
- **Resource:** Codex (code gen) + local Python
- **Deliverable:** Master table + heatmap figure (modulus x gamma x power)
- **Paper role:** Proves the spectroscope is a general tool, not a one-off trick

### Task 5: Montgomery Pair Correlation [HIGH]
- **Do:** Extend autocorrelation analysis to full pair statistics:
  - Compute A(tau) = integral F(gamma) F(gamma+tau) dgamma
  - Compare peak positions against all gamma_j - gamma_k differences
  - Overlay Montgomery's 1 - (sin(pi alpha)/(pi alpha))^2 kernel
  - Null control: pair correlation from shuffled data
- **Resource:** Codex (implementation) + qwen3:8b (lit check on normalization)
- **Deliverable:** Pair correlation figure: Farey-derived vs GUE prediction
- **Paper role:** Bridge to random matrix theory — major citation magnet

### Task 6: Null Hypothesis Battery [CRITICAL]
- **Do:** 6 null tests, 1000 trials each:
  1. Shuffled R(p) values among same primes
  2. i.i.d. Gaussian R(p) with same variance
  3. Consecutive integers instead of primes
  4. Composite orders instead of prime orders
  5. F(gamma + delta) for delta = 0.5, 1.0, 2.0 (shifted zeros check)
  6. False discovery rate among 1000 shuffled spectra
- **Resource:** Codex (code gen) + local machine (~30 min total)
- **Deliverable:** p-values for each test + 95% confidence envelope figure
- **Paper role:** Makes the paper referee-proof against "artifact" objection

### Task 7: Optimal Weighting & Raw DeltaW Spectroscope [MEDIUM]
- **Do:** Test:
  - Different M(p) thresholds: <= -1, -2, -3, -4, -5, and no filter
  - Soft weighting: w(p) = max(0, -M(p)-2)^alpha for alpha = 0, 0.5, 1, 2
  - Raw DeltaW spectroscope: G(gamma) = |sum DeltaW(p) p^{-1/2-igamma}|^2
  - Informativeness ranking: which primes contribute most to gamma_1?
- **Resource:** gemma4:26b (brainstorm) + Python
- **Deliverable:** Filter optimization table + assessment of raw DeltaW variant
- **Paper role:** Principled justification for method choices

## Resource Assignment

| Task | Primary | Wall Time |
|------|---------|-----------|
| 1. Scale R(p) | Local C binary (background) | 6-12h |
| 2. Detrended amp | Qwen 3.6 + Python | 2h |
| 3. Convergence theory | qwen3.5:35b | 4-8h |
| 4. L-function survey | Codex + Python | 3h |
| 5. Pair correlation | Codex + Python | 3h |
| 6. Null battery | Codex + Python | 2h |
| 7. Optimal weighting | gemma4:26b + Python | 2h |

## Dependency Graph
Tasks 1-5: fully parallel. Tasks 6-7: can start on current data, rerun with Task 1 output.

## Success Criteria (paper-ready when)
1. gamma_1-gamma_5 detected to <1% error with convergence rate measured
2. Honest amplitude metric with permutation p-value
3. Convergence theorem (conditional) or conjecture + fit
4. At least 5 L-functions with successful zero detection
5. All null controls passed
6. Pair correlation figure (at least qualitative match with Montgomery)

## Paper 2 Structure
1. Introduction + spectroscope definition
2. Position detection + convergence (Tasks 1, 3)
3. Amplitude matching — honest analysis (Task 2)
4. L-function generalization (Task 4)
5. Pair correlation + random matrix connection (Task 5)
6. Statistical controls (Task 6)
7. Optimal design + DeltaW variant (Task 7)
8. Theory under GRH (Task 3 extended)

## Key Files
- `experiments/R_bound_1M` — compiled C binary for R(p) computation
- `experiments/R_bound_200K_output.csv` — current best data (6,248 primes to p=143K)
- `experiments/farey_spectroscope.py` — main spectroscope script
- `experiments/spectral_amplitudes.py` — amplitude matching
- `paper/section_spectroscope_draft.tex` — draft section (140 lines)
