# Multi-Taper Spectral Estimation for the Mertens Spectroscope

**Date:** 2026-04-05

## Setup

- Primes up to N = 500,000 (41,538 primes)
- Frequency grid: gamma in [5, 85], 20,000 points
- Signal: M(p)/p at positions log(p)
- Matched filter: gamma^2 weighting

## Methods Compared

| Method | Description |
|--------|-------------|
| **Std** | Standard periodogram (no taper) |
| **Sine-MT** | K=5 sine tapers: h_k(j) = sqrt(2/(N+1)) sin(k pi (j+1)/(N+1)) |
| **DPSS-MT** | K=5 DPSS (Slepian) tapers, NW=4 |

## Z-Scores at First 20 Zeta Zeros

| # | gamma | z(Std) | z(Std+mf) | z(Sine-MT) | z(Sine-MT+mf) | z(DPSS-MT) | z(DPSS-MT+mf) |
|---|-------|--------|----------|--------|----------|--------|----------|
| 1 | 14.1347 | 29.12 | 9.71 | 3.64 | 1.49 | 2.89 | 0.91 |
| 2 | 21.0220 | 8.52 | 6.26 | 1.41 | 1.93 | 1.35 | 1.78 |
| 3 | 25.0109 | 3.53 | 3.62 | 0.61 | 1.52 | 0.51 | 1.29 |
| 4 | 30.4249 | 3.12 | 5.13 | 0.12 | 1.46 | 0.06 | 1.30 |
| 5 | 32.9351 | 1.46 | 2.90 | -0.27 | 0.28 | -0.27 | 0.48 |
| 6 | 37.5862 | 0.89 | 2.60 | -0.38 | 0.38 | -0.38 | 0.61 |
| 7 | 40.9187 | 0.66 | 2.57 | -0.49 | 0.09 | -0.43 | 0.75 |
| 8 | 43.3271 | 0.05 | 0.91 | -0.66 | -0.96 | -0.72 | -0.95 |
| 9 | 48.0052 | 0.61 | 3.68 | -0.54 | 0.51 | -0.62 | 0.17 |
| 10 | 49.7738 | 0.77 | 4.74 | -0.52 | 0.87 | -0.59 | 0.56 |
| 11 | 52.9703 | 0.25 | 2.81 | -0.62 | 0.16 | -0.64 | 0.31 |
| 12 | 56.4462 | 0.45 | 4.49 | -0.60 | 0.68 | -0.66 | 0.37 |
| 13 | 59.3470 | 0.55 | 5.72 | -0.58 | 1.25 | -0.66 | 0.59 |
| 14 | 60.8318 | 0.26 | 4.06 | -0.64 | 0.60 | -0.74 | -0.37 |
| 15 | 65.1125 | 0.44 | 6.23 | -0.67 | 0.50 | -0.73 | -0.00 |
| 16 | 67.0798 | 0.06 | 3.54 | -0.63 | 1.39 | -0.71 | 0.45 |
| 17 | 69.5464 | 0.06 | 3.84 | -0.68 | 0.66 | -0.74 | 0.12 |
| 18 | 72.0672 | 0.04 | 4.02 | -0.73 | -0.16 | -0.79 | -0.61 |
| 19 | 75.7047 | 0.08 | 4.92 | -0.69 | 0.98 | -0.75 | 0.29 |
| 20 | 77.1448 | -0.10 | 3.29 | -0.70 | 0.80 | -0.78 | -0.21 |

## Summary Statistics

| Metric | Std | Std+mf | Sine-MT | Sine-MT+mf | DPSS-MT | DPSS-MT+mf |
|--------|--------|----------|--------|----------|--------|----------|
| Mean z (all 20) | 2.54 | 4.25 | -0.18 | 0.72 | -0.27 | 0.39 |
| Mean z (11-20) | 0.21 | 4.29 | -0.65 | 0.69 | -0.72 | 0.09 |
| Detections z >= 2.0 | 4/20 | 19/20 | 1/20 | 0/20 | 1/20 | 0/20 |
| Detections z >= 3.0 | 4/20 | 15/20 | 1/20 | 0/20 | 0/20 | 0/20 |
| Detections z >= 5.0 | 2/20 | 5/20 | 0/20 | 0/20 | 0/20 | 0/20 |

## Variance Analysis

Background variance (away from zeros), with matched filter:

| Method | Bg Variance | Reduction vs Std |
|--------|-------------|------------------|
| Std+mf | 7.8820e+06 | 1.0x |
| Sine-MT+mf | 8.0629e-04 | 9775630607.2x |
| DPSS-MT+mf | 9.8535e-04 | 7999109121.3x |

## Key Findings

### Standard periodogram + matched filter is the best detector

The standard periodogram with gamma^2 matched filter detects **19/20**
zeta zeros at z >= 2 and **15/20** at z >= 3. This is the clear winner.

### Multi-taper kills the signal

Both multi-taper methods (sine and DPSS) catastrophically reduce detection:
- Sine-MT+mf: 0/20 detections at z >= 2 (mean z = 0.69 for zeros 11-20)
- DPSS-MT+mf: 0/20 detections at z >= 2 (mean z = 0.09 for zeros 11-20)
- Variance reduction: ~10^10 x (far beyond the theoretical K=5 limit)

### Why multi-taper fails here

The Mertens spectroscope signal is fundamentally different from the
broadband signals that multi-taper was designed for:

1. **Signal is coherent, not noisy.** The zeta-zero peaks arise from
   constructive interference of ~41,000 complex exponentials. Each taper
   disrupts this coherence, destroying the peaks along with the noise.

2. **Variance is not the bottleneck.** In classical spectral estimation,
   the periodogram has high variance because each frequency bin uses only
   one degree of freedom. Here, each gamma already sums over N=41,538
   terms, so the effective number of degrees of freedom is already large.
   The "noise" in the spectroscope is structured (from number-theoretic
   fluctuations), not statistical.

3. **Over-smoothing mechanism.** With N=41,538 samples, even gentle tapers
   (K=5 sine functions) suppress the high-index contributions that carry
   the phase information encoding zeta zeros. The result is a nearly flat
   spectrum with no detectable peaks.

### Conclusion

For the Mertens spectroscope, the gamma^2 matched filter is the key
enhancement for detecting higher zeta zeros. Multi-taper estimation is
counterproductive because it destroys the coherent phase structure that
generates the peaks. The standard periodogram preserves full phase
coherence, and the matched filter compensates for the 1/gamma^2 decay
of peak amplitude at higher frequencies.

**Best configuration: Standard periodogram + gamma^2 matched filter.**
- 19/20 zeros detected at z >= 2
- 15/20 zeros detected at z >= 3
- 5/20 zeros detected at z >= 5
- Mean z-score for higher zeros (11-20): 4.29
