# Universality Test: M(p)/p Weighting

**Date:** 2026-04-06

## Setup

- Sieved Mobius/Mertens to N = 1,000,000
- Primes: 78,498
- Weighting: **M(p)/p** (Mertens function at p, divided by p)
- Spectral function: F(γ) = γ² |Σ (M(p)/p) exp(-iγ log p)|²
- γ range: [10.0, 50.0], 10000 points
- Target: γ₁ = 14.134725
- Z-score: peak vs background ±8.0, excluding ±1.5 around known zeros
- Trials per configuration: 50

## Random Subset Results

| N_sub | Mean z | Std z | Detection rate (z>3) |
|------:|-------:|------:|--------------------:|
| 200 | 15.12 | 7.28 | 94% |
| 500 | 19.38 | 11.40 | 92% |
| 1,000 | 23.01 | 13.33 | 94% |
| 2,000 | 31.90 | 19.58 | 88% |
| 5,000 | 37.11 | 17.62 | 100% |
| 10,000 | 32.30 | 15.19 | 100% |
| 20,000 | 40.74 | 11.98 | 100% |
| 50,000 | 54.73 | 6.22 | 100% |

**Minimum N for ≥95% detection: ~2750**

## Structured Subsets (N = 5,000)

| Subset | N used | Mean z | Std z | Detection rate |
|--------|-------:|-------:|------:|---------------:|
| p ≡ 1 mod 4 | 5,000 | 36.20 | 16.24 | 100% |
| Twin primes | 5,000 | 9.17 | 3.37 | 100% |
| p ∈ [500K,1M] | 5,000 | 0.78 | 0.08 | 0% |
| Every 5th prime | 5,000 | 38.68 | 12.91 | 100% |
| Random (baseline) | 5,000 | 37.11 | 17.62 | 100% |

## Key Findings

1. **Minimum subset size for 95% detection:** ~2750 primes (3.5% of all primes to 10^6)
2. **Even N=200 random primes give mean z=15.1** with 94% detection -- remarkably strong signal even at tiny subsets
3. **Partial universality:** Detection works for p equiv 1 mod 4, twin primes, every-5th-prime (all 100%). But **p in [500K,1M] gives 0% detection** (mean z=0.78)
4. **Large-prime failure is expected:** M(p)/p ~ O(1/sqrt(p)) for large p, so high primes contribute negligible weight. The signal lives in small primes where |M(p)/p| is large
5. **Twin primes show weaker z-scores** (mean 9.17 vs 37 for random) despite 100% detection -- consistent with their sparser log-spacing

## Critical Observation: Small Primes Dominate

The M(p)/p weighting heavily favors small primes:
- M(2)/2 = -0.5, M(3)/3 = -0.67, M(5)/5 = -0.4
- M(500000)/500000 ~ O(10^{-3})

This means the zero-detection signal is concentrated in the first few thousand primes. The [500K,1M] subset fails completely because those primes have weights ~1000x smaller than small primes.

**Implication:** M(p)/p is NOT a universality-compatible weighting. It strongly biases toward small primes. Compare with log(p)/sqrt(p) which gives more uniform contributions across the prime range.

## Comparison with log(p)/sqrt(p) weighting

| Property | M(p)/p | log(p)/sqrt(p) |
|----------|--------|----------------|
| Small prime weight | Very large | Moderate |
| Large prime weight | ~0 | Still significant |
| [500K,1M] detection | 0% | (to be tested) |
| Minimum N for 95% | ~2750 | (to be tested) |
| Theoretical basis | Mertens function | Von Mangoldt / explicit formula |

## Interpretation

The M(p)/p weight assigns each prime a contribution proportional to the cumulative Mobius function normalized by magnitude. From the explicit formula M(x)/x ~ Sum x^{rho-1}/rho, this is natural but **concentrates information in small primes** where |M(p)| ~ O(sqrt(p)) makes M(p)/p ~ O(1/sqrt(p)). For large p, the weight vanishes and those primes contribute nothing.

This is fundamentally different from Fourier-analytic weightings like log(p)/sqrt(p) which maintain comparable contributions across the prime range. The M(p)/p weighting detects zeros efficiently (only ~2750 primes needed) precisely because it automatically focuses on the information-dense small primes.

![Universality figure](universality_mertens_weight.png)
