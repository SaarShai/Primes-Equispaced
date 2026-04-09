# Liouville Spectroscope: Computation Result

**Date:** 2026-04-09  
**Script:** `~/Desktop/Farey-Local/experiments/liouville_spectroscope.py`  
**Figure:** `~/Desktop/Farey-Local/figures/liouville_spectroscope.png`

## Parameters
- N = 500,000 (sieve limit)
- 41,538 primes used
- gamma range: [5, 85], 20,000 points
- Local z-score window: half-width 1.5
- First 20 nontrivial zeta zeros tested

## Spectroscope Definitions
- **Mertens:** F_M(gamma) = gamma^2 |sum_{p prime} M(p)/p * exp(-i*gamma*log(p))|^2
- **Liouville:** F_L(gamma) = gamma^2 |sum_{p prime} L(p)/p * exp(-i*gamma*log(p))|^2

## Z-Score Comparison Table

| Zero | gamma     | z_Mertens | z_Liouville | Ratio L/M |
|------|-----------|-----------|-------------|-----------|
| 1    | 14.1347   | 2.058     | 2.144       | 1.042     |
| 2    | 21.0220   | 2.209     | 2.512       | 1.137     |
| 3    | 25.0109   | 1.138     | -0.109      | -0.096    |
| 4    | 30.4249   | 1.835     | 1.789       | 0.975     |
| 5    | 32.9351   | 1.159     | -0.215      | -0.185    |
| 6    | 37.5862   | 2.398     | -1.433      | -0.597    |
| 7    | 40.9187   | 2.005     | 1.745       | 0.871     |
| 8    | 43.3271   | 0.493     | -0.600      | -1.217    |
| 9    | 48.0052   | 1.764     | -0.164      | -0.093    |
| 10   | 49.7738   | 0.642     | 1.128       | 1.756     |
| 11   | 52.9703   | 1.019     | 2.665       | 2.616     |
| 12   | 56.4462   | 1.000     | 2.566       | 2.565     |
| 13   | 59.3470   | -0.008    | 0.937       | --        |
| 14   | 60.8318   | 0.490     | -1.299      | -2.653    |
| 15   | 65.1125   | 2.458     | 3.151       | 1.282     |
| 16   | 67.0798   | 1.418     | 0.831       | 0.586     |
| 17   | 69.5464   | 0.991     | -0.872      | -0.880    |
| 18   | 72.0672   | -0.360    | 1.751       | --        |
| 19   | 75.7047   | 0.998     | -0.769      | -0.770    |
| 20   | 77.1448   | 1.084     | 1.195       | 1.102     |

## Summary Statistics

| Metric                       | Value    |
|------------------------------|----------|
| Mean z_Mertens               | 1.240    |
| Mean z_Liouville             | 0.848    |
| Zeros with z > 2 (Mertens)  | 5 / 20   |
| Zeros with z > 2 (Liouville)| 5 / 20   |
| Mean ratio L/M               | 0.413    |
| Median ratio L/M             | 0.728    |
| Std ratio L/M                | 1.313    |

## Verdict

**Liouville is NOT 2.6x better than Mertens.** The mean ratio is 0.41, and median 0.73 -- Mertens actually outperforms on average.

Key observations:
1. **High variance in ratios**: L/M ranges from -2.65 to +2.62, indicating the relative strength is zero-dependent.
2. **Mertens more consistent**: 5/20 zeros exceed z=2 for both, but Mertens has fewer negative z-scores (2 vs 8 for Liouville).
3. **Liouville shines at specific zeros**: zeros 11, 12, 15 show L/M > 1.2, consistent with |zeta(2*rho)| being large there. But this is sporadic.
4. **Theory says ratio ~ |zeta(2*rho)| * sqrt(pi^2/6) ~ 1.28 * |zeta(2*rho)|**. The observed mean of 0.41 suggests |zeta(2*rho)| < 1 on average at these zeros, or interference effects dominate.

## Why the Theory Overpredicted

The theoretical ratio assumes asymptotic regime (N -> infinity) and ignores:
- Finite-N interference patterns
- Phase misalignment between zeta(2*rho) and zeta'(rho)
- The cumulative sum L(p) has larger magnitude fluctuations that create both stronger peaks AND stronger noise
- Liouville includes all n (not just squarefree), so the noise floor is higher

## Status
- **Claim "Liouville 2.6x better"**: DISPROVED computationally at N=500K
- **Mertens spectroscope remains the better choice** for zeta zero detection at moderate N
- Liouville may improve at much larger N where asymptotics kick in -- worth testing at N=10M
