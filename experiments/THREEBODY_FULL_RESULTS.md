# Three-Body Orbit -> Stern-Brocot: Full Validation Results

**Date**: 2026-03-27
**Orbits analyzed**: 695
**Source**: Li & Liao catalog (sjtu-liao/three-body), equal-mass zero-angular-momentum

## Pipeline

```
Free-group word (e.g. BabA)
  -> Gamma(2) matrix: a->[[1,2],[0,1]], b->[[1,0],[2,1]]
  -> Hyperbolic Mobius transformation
  -> Attracting fixed point (quadratic irrational)
  -> Eventually-periodic continued fraction
  -> CF period length, nobility, geometric mean
```

---

## TEST 1: Full Catalog Correlations (N=695)

### Raw Correlations

| Test | rho | p-value | 95% CI | sig |
|---|---|---|---|---|
| BASELINE_log_trace_vs_log_disc | 1.0000 | 0.00e+00 |  | *** |
| BASELINE_wordlen_vs_Tstar | 0.9988 | 0.00e+00 |  | *** |
| BASELINE_wordlen_vs_log_trace | 0.9983 | 0.00e+00 |  | *** |
| PARTIAL_disc_vs_period | 0.9146 | 1.19e-274 |  | *** |
| PARTIAL_disc_vs_stability | 1.0000 | 0.00e+00 |  | *** |
| PARTIAL_gmean_vs_period | 0.5129 | 6.90e-48 |  | *** |
| PARTIAL_gmean_vs_stability | 0.5049 | 3.13e-46 |  | *** |
| PARTIAL_nobility_vs_period | -0.6000 | 3.47e-69 | [-0.668, -0.529] | *** |
| PARTIAL_nobility_vs_stability | -0.5379 | 2.26e-53 | [-0.606, -0.467] | *** |
| RAW_approx_quality_vs_log_trace | 0.0540 | 1.55e-01 |  |  |
| RAW_cf_gmean_vs_Tstar | 0.2815 | 4.00e-14 |  | *** |
| RAW_cf_gmean_vs_log_trace | 0.2860 | 1.49e-14 |  | *** |
| RAW_log_disc_vs_Tstar | 0.9998 | 0.00e+00 |  | *** |
| RAW_log_disc_vs_log_trace | 1.0000 | 0.00e+00 |  | *** |
| RAW_lyapunov_proxy_vs_cf_gmean | 0.5427 | 1.78e-54 |  | *** |
| RAW_lyapunov_proxy_vs_nobility | -0.5628 | 2.53e-59 | [-0.631, -0.493] | *** |
| RAW_nobility_vs_Tstar | -0.3004 | 5.80e-16 |  | *** |
| RAW_nobility_vs_log_trace | -0.3052 | 1.92e-16 | [-0.374, -0.238] | *** |
| RAW_nobility_vs_period_density | -0.5754 | 1.61e-62 |  | *** |
| RAW_period_density_vs_cf_gmean | 0.5602 | 1.13e-58 |  | *** |

### N=100 vs N=full Comparison

| Metric | N=100 | N=full | Change |
|---|---|---|---|
| partial_stability_rho | -0.4461 | -0.5379 | -0.0918 (STRONGER) |
| partial_period_rho | -0.4989 | -0.6000 | -0.1011 (STRONGER) |
| raw_stability_rho | -0.2857 | -0.3052 | -0.0195 (STRONGER) |
| lyapunov_rho | -0.5245 | -0.5628 | -0.0383 (STRONGER) |

---

## TEST 2: Blind Prediction

- Training set: 500 orbits
- Test set: 195 orbits
- Stability threshold (bottom 30% Lyapunov proxy): 0.7458

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|
| Word length only | 0.677 | 0.481 | 0.426 | 0.452 | 0.741 |
| Nobility only | 0.913 | 0.907 | 0.803 | 0.852 | 0.853 |
| Word length + nobility | 0.867 | 0.797 | 0.770 | 0.783 | 0.887 |
| Full CF features | 0.908 | 0.864 | 0.836 | 0.850 | 0.969 |

**AUC improvement from nobility**: +0.1459
**AUC improvement from full CF**: +0.2284
**Nobility adds predictive value**: True

---

## TEST 3: Gap Prediction (Stern-Brocot Injection)

Total inter-orbit gaps analyzed: 354

### Top 10 Predicted Undiscovered Orbits

| Rank | Left | Right | Midpoint FP | Gap | Pred v1 | Pred v2 | Pred T |
|---|---|---|---|---|---|---|---|
| 1 | II.C-222 | II.C-104 | 0.499651 | 0.235128 | 0.40177 | 0.39111 | 208.84 |
| 2 | II.C-39 | II.C-2 | 0.678300 | 0.090614 | 0.49589 | 0.43858 | 96.71 |
| 3 | II.C-5 | I.A-3 | 0.752193 | 0.057166 | 0.58316 | 0.53655 | 31.86 |
| 4 | I.A-90 | I.A-148 | 0.625188 | 0.010012 | 0.27126 | 0.42580 | 202.54 |
| 5 | I.A-3 | II.C-61 | 0.782117 | 0.002681 | 0.64236 | 0.50445 | 24.11 |
| 6 | II.C-206 | I.B-21 | 0.631527 | 0.002609 | 0.25528 | 0.39938 | 139.37 |
| 7 | II.C-69 | I.A-51 | 0.381145 | 0.001884 | 0.26119 | 0.23747 | 132.98 |
| 8 | II.A-4 | I.A-28 | 0.619347 | 0.001670 | 0.03763 | 0.64047 | 94.59 |
| 9 | II.C-197 | II.C-64 | 0.378949 | 0.001655 | 0.09193 | 0.16663 | 87.04 |
| 10 | II.C-109 | I.A-97 | 0.617565 | 0.000699 | 0.32397 | 0.50130 | 259.83 |

*These initial conditions can be fed into an N-body integrator to verify.*

---

## TEST 4: Randomization Control (10,000 Permutations)

| Test | Observed rho | Permutation p | z-score |
|---|---|---|---|
| Partial: nobility vs stability | -0.5379 | 0.0001 | -14.19 *** |
| Partial: nobility vs period | -0.6000 | 0.0001 | -15.60 *** |
| Raw: nobility vs stability | -0.3052 | 0.0001 | -8.07 *** |
| Lyapunov proxy vs nobility | -0.5628 | 0.0001 | -14.79 *** |

Null distribution stats:
- Partial stability: mean=-0.0003, std=0.0379
- Partial period: mean=-0.0002, std=0.0385

---

## CF Period Distribution

| Period length | Count | Percentage |
|---|---|---|
| 0 | 123 | 17.7% |
| 1 | 72 | 10.4% |
| 3 | 1 | 0.1% |
| 4 | 105 | 15.1% |
| 5 | 86 | 12.4% |
| 7 | 15 | 2.2% |
| 9 | 61 | 8.8% |
| 10 | 9 | 1.3% |
| 11 | 26 | 3.7% |
| 13 | 52 | 7.5% |
| 14 | 82 | 11.8% |
| 15 | 8 | 1.2% |
| 16 | 18 | 2.6% |
| 17 | 25 | 3.6% |
| 18 | 1 | 0.1% |
| 19 | 7 | 1.0% |
| 20 | 4 | 0.6% |

### Family CF Profiles

| Family | N | Mean Nobility | Mean CF gmean | Period Mode |
|---|---|---|---|---|
| I.A | 190 | 0.713 | 1.358 | 14 |
| I.B | 191 | 0.686 | 1.391 | 5 |
| II.A | 4 | 0.921 | 1.066 | 1 |
| II.B | 10 | 0.755 | 1.368 | 1 |
| II.C | 300 | 0.732 | 1.406 | 0 |

**Kruskal-Wallis test** (families differ in nobility): H=16.36, p=2.57e-03

---

## Figure-Eight Analysis

- Word: `BabA`  (length 4)
- Trace = 18, Det = 1
- Discriminant = 320
- Attracting FP = -0.618033988749895
- |FP| = 0.618033988749895
- 1/phi = 0.618033988749895
- |FP - 1/phi| = 1.11e-16
- **CONFIRMED**: Figure-eight maps to 1/phi (golden ratio)
- CF = [0, 1]
- CF period = [1]
- Nobility = 1.000

---

## OVERALL VERDICT

### Test-by-test assessment:

1. **Full catalog**: Partial nobility-stability rho=-0.5379 (p=2.26e-53), partial nobility-period rho=-0.6000 (p=3.47e-69)
2. **Blind prediction**: AUC improvement from nobility = +0.1459
3. **Gap prediction**: 354 gaps identified, top 10 predictions listed
4. **Randomization**: Permutation p-values: stability=0.0001, period=0.0001

### Overall Assessment: **STRONG POSITIVE**

Both key partial correlations survive permutation testing AND nobility adds blind-predictive value beyond word length. The SB mapping captures genuine physical structure not visible from topology alone.

### Figure-Eight -> Golden Ratio: CONFIRMED

Regardless of the statistical results, the figure-eight -> 1/phi mapping is a genuine algebraic identity: Gamma(2) matrix of word 'aB' has golden-ratio fixed point. This is an exact result, not a statistical one.
