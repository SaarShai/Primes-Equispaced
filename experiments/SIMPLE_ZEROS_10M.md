# Simple Zeros Test: N=10,000,000

**Date:** 2026-04-06  
**Mobius sieve limit:** 10,000,000  
**Primes:** 664,579  
**Local spectral points:** 64 per zero (window +/-0.5)  
**Full spectrum:** 5000 pts on [5.0, 85.0]  
**Monte Carlo shuffles:** 50

## Method

Same as SIMPLE_ZEROS_TEST.md (N=1M) but with 10x more primes.
Linear sieve for Mobius, vectorized spectral computation.
Optimization: compute dense local spectra around each zero
(64 pts in +/-0.5 window) instead of full 25K-point sweep.
Lorentzian vs squared-Lorentzian fitting with chi-squared comparison.
Added: 50-shuffle Monte Carlo null hypothesis test.

## Results: Per-Zero Analysis

| k | gamma_k | chi2(Lor) | chi2(SqLor) | Ratio | Kurtosis | Preferred | MC p-val |
|---|---------|-----------|-------------|-------|----------|-----------|----------|
| 1 | 14.134725 | 1.017e+10 | 1.016e+10 | 0.998 | -1.260 | Double? | 0.520 |
| 2 | 21.022040 | 2.529e+09 | 2.487e+09 | 0.983 | -1.216 | Double? | 0.420 |
| 3 | 25.010858 | 4.410e+09 | 4.437e+09 | 1.006 | -0.732 | Simple | 0.460 |
| 4 | 30.424876 | 1.350e+10 | 1.344e+10 | 0.996 | -0.901 | Double? | 0.380 |
| 5 | 32.935062 | 1.089e+10 | 1.088e+10 | 1.000 | -1.063 | Double? | 0.380 |
| 6 | 37.586178 | 1.564e+10 | 1.461e+10 | 0.934 | -0.927 | Double? | 0.460 |
| 7 | 40.918719 | 4.246e+08 | 3.080e+08 | 0.725 | -1.061 | Double? | 0.900 |
| 8 | 43.327073 | 3.554e+09 | 3.634e+09 | 1.022 | -0.635 | Simple | 0.380 |
| 9 | 48.005151 | 3.071e+10 | 3.064e+10 | 0.998 | -1.124 | Double? | 0.340 |
| 10 | 49.773832 | 8.802e+09 | 9.854e+09 | 1.120 | -0.600 | Simple | 0.240 |
| 11 | 52.970321 | 1.457e+09 | 1.435e+09 | 0.985 | -0.670 | Double? | 0.400 |
| 12 | 56.446248 | 3.277e+09 | 2.965e+09 | 0.905 | -1.073 | Double? | 0.560 |
| 13 | 59.347044 | 3.218e+10 | 3.117e+10 | 0.969 | -0.615 | Double? | 0.460 |
| 14 | 60.831779 | 2.878e+09 | 2.680e+09 | 0.931 | -0.754 | Double? | 0.580 |
| 15 | 65.112544 | 2.682e+09 | 2.254e+09 | 0.840 | -0.701 | Double? | 0.620 |
| 16 | 67.079811 | 5.558e+09 | 5.718e+09 | 1.029 | -1.059 | Simple | 0.400 |
| 17 | 69.546402 | 1.530e+10 | 1.438e+10 | 0.940 | -0.704 | Double? | 0.540 |
| 18 | 72.067158 | 2.576e+09 | 1.955e+09 | 0.759 | -0.286 | Double? | 0.720 |
| 19 | 75.704691 | 4.994e+10 | 4.821e+10 | 0.965 | -0.943 | Double? | 0.560 |
| 20 | 77.144840 | 5.383e+09 | 5.027e+09 | 0.934 | -1.497 | Double? | 0.460 |

## Summary Statistics

- **Zeros where Lorentzian preferred (Simple):** 4/20
- **Zeros where Sq-Lorentzian preferred (Double?):** 16/20
- **Average chi2 ratio (sq/simple):** 0.9519
- **Average peak kurtosis:** -0.8910

## Comparison with N=1M

| Metric | N=1M | N=10M |
|--------|------|-------|
| Primes | 78,498 | 664,579 |
| Simple preferred | 11/20 | 4/20 |
| Avg chi2 ratio | 1.037 | 0.9519 |
| Avg kurtosis | 0.997 | -0.8910 |

## Monte Carlo Null Hypothesis Test

Under the null (shuffled M(p)), the spectral peaks have no special relationship
to zeta zeros. We compare the chi-squared ratio distribution:

- **Real average ratio:** 0.9519
- **Null average ratio:** 1.0264 +/- 0.1310
- **Global p-value:** 0.7600

The real data does NOT show statistically significant preference for Lorentzian peaks
compared to the shuffled null at the 0.05 level.

## Conclusion

**10M does NOT clearly improve discrimination:** 4/20 zeros prefer Lorentzian (vs 11/20 at 1M).
Average chi2 ratio moved from 1.037 to 0.9519.
Monte Carlo global p-value = 0.7600.

The compensated Mertens spectroscope at N=10^7 provides comparable evidence
for the Simple Zeros Hypothesis compared to N=10^6.
