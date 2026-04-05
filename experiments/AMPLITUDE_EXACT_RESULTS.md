# Exact Amplitude Matching: Mertens Spectroscope

**Date:** 2026-04-05 19:29
**Method:** mpmath ζ'(ρ_k) at 50-digit precision (NOT Stirling approximation)
**Möbius sieve:** N = 500,000
**Primes used:** 41,538
**Spectral grid:** 20,000 points on [5, 85]

## Correlation Metrics

| Metric | Value | p-value |
|--------|-------|---------|
| Pearson r (|c_k|² vs peak) | -0.438596 | 5.3053e-02 |
| Spearman ρ (rank) | -0.178947 | 4.5033e-01 |
| Consecutive ratio r | -0.584938 | 8.5220e-03 |
| Log-space Pearson r | -0.276748 | 2.3752e-01 |

**Previous result (Stirling approx):** Pearson r = -0.035

## Per-Zero Table

| k | γ_k | |ζ'(ρ_k)| | |c_k|² | Observed Peak | Pred/Obs Ratio |
|---:|---:|---:|---:|---:|---:|
| 1 | 14.1347 | 0.793157156657 | 7.946305e-03 | 245729.96 | 3.233755e-08 |
| 2 | 21.0220 | 1.136843863889 | 1.749866e-03 | 315330.99 | 5.549298e-09 |
| 3 | 25.0109 | 1.371736373300 | 8.492323e-04 | 322961.35 | 2.629517e-09 |
| 4 | 30.4249 | 1.303926784661 | 6.352110e-04 | 341165.77 | 1.861884e-09 |
| 5 | 32.9351 | 1.382147869445 | 4.824729e-04 | 339186.59 | 1.422441e-09 |
| 6 | 37.5862 | 1.936499521611 | 1.887259e-04 | 348916.39 | 5.408915e-10 |
| 7 | 40.9187 | 1.490617269508 | 2.687566e-04 | 338168.25 | 7.947424e-10 |
| 8 | 43.3271 | 1.833540095892 | 1.584317e-04 | 400137.58 | 3.959431e-10 |
| 9 | 48.0052 | 1.567962229480 | 1.764839e-04 | 391838.29 | 4.503999e-10 |
| 10 | 49.7738 | 1.418902296841 | 2.004701e-04 | 309346.09 | 6.480447e-10 |
| 11 | 52.9703 | 2.426568754460 | 6.052172e-05 | 340714.65 | 1.776317e-10 |
| 12 | 56.4462 | 2.367964500443 | 5.596882e-05 | 373693.16 | 1.497721e-10 |
| 13 | 59.3470 | 1.391850939176 | 1.465501e-04 | 322538.80 | 4.543643e-10 |
| 14 | 60.8318 | 1.654191679482 | 9.875013e-05 | 315768.44 | 3.127296e-10 |
| 15 | 65.1125 | 2.287855786885 | 4.505971e-05 | 333927.81 | 1.349385e-10 |
| 16 | 67.0798 | 1.783575838629 | 6.985688e-05 | 230027.06 | 3.036898e-10 |
| 17 | 69.5464 | 2.186310303280 | 4.325185e-05 | 266678.08 | 1.621875e-10 |
| 18 | 72.0672 | 2.964577984859 | 2.190675e-05 | 381078.41 | 5.748621e-11 |
| 19 | 75.7047 | 1.779535934170 | 5.509623e-05 | 374848.96 | 1.469825e-10 |
| 20 | 77.1448 | 1.457506850541 | 7.909467e-05 | 296701.68 | 2.665798e-10 |

## Interpretation

The exact |ζ'(ρ_k)| values replace the Stirling approximation that gave
r = -0.035. The predicted amplitudes |c_k|² = 1/|ρ_k·ζ'(ρ_k)|² should track
the observed spectral peaks F_comp(γ_k) = γ²|Σ M(p)/p · e^{-iγ log p}|².

Key observations:
- Both |c_k|² and observed peaks decrease with k (larger γ_k), but at different rates
- The log-space correlation removes the dominant 1/γ² scaling trend
- Consecutive ratios test whether zero-to-zero fluctuations match
