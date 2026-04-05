# Optimal Weighting — Verified Results

## The 3.2x SNR claim is a NORMALIZATION ARTIFACT

The original optimal_weighting.py used peak/median as SNR. This metric is
misleading because smaller weights shrink the median faster than the peak.
Unit weight (w=1) achieves SNR=55.3, higher than M(p)/sqrt(p) at 43.9 —
which is clearly absurd (w=1 carries no information about Mertens function).

## Fair Metrics

| Weight | z-score | Peak fraction | Error % |
|--------|---------|---------------|---------|
| R(p) | 5.4 | 27.6% | 0.295% |
| M(p)/sqrt(p) | 9.0 (1.7x over R) | 37.3% | 0.214% |
| M(p) | 5.2 | 26.4% | 0.267% |
| Unit (w=1) | 7.8 | 44.2% | 0.101% |

## True Findings

1. M(p)/sqrt(p) IS modestly better than R(p) by z-score (1.7x, not 3.2x)
2. Unit weight works surprisingly well on the pre-filtered dataset
3. The M(p)<=-3 FILTER does the heavy lifting, not the weight function
4. R(p) weighting adds noise from variable magnitudes
5. For Paper 2: the interesting question is whether M(p)/sqrt(p) or unit
   weight remains better when using ALL primes (no M(p) filter)

## Impact on Paper 1
None — the R(p) spectroscope is correctly described. The M(p)/sqrt(p)
comparison is a Paper 2 topic that requires the full prime set to be fair.
