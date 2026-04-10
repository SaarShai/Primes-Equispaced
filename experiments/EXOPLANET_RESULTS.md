# Exoplanet Resonance Chains and Farey Ordering

## Overview

Analysis of 341 multi-planet systems (3+ planets with measured
orbital periods) from the NASA Exoplanet Archive. We test whether consecutive
period ratios P_{i+1}/P_i follow Farey sequence ordering.

Total period ratios analyzed: 702
Farey order used: F_{12}

## Test Results

| Test | Statistic | p-value | Effect Size |
|------|-----------|---------|-------------|
| T1: Farey proximity (KS) | KS | 2.13e-01 | d=-0.07 |
| T1: Farey proximity (MW, one-sided) | MW-U | 9.65e-01 | |
| T2: Mediant ordering (KS) | KS | 1.09e-31 | |
| T3: Farey level clustering (KS) | KS | 1.56e-17 | |
| T3: Farey level clustering (MW) | MW-U | 8.86e-28 | |
| T4: SB depth (KS) | KS | 2.49e-01 | d=0.07 |
| T4: SB depth (MW, one-sided) | MW-U | 3.56e-02 | |
| T5: Resonant chain perm (error) | Perm | 0.5130 | n=30 |
| T5: Resonant chain perm (depth) | Perm | 0.2120 | |

### Key Numbers

- Mean Farey error (real): 0.008891
- Mean Farey error (random): 0.008297
- Mean SB depth (real): 16.76
- Mean SB depth (random): 17.42

## Interpretation

- TEST 1 NOT SIGNIFICANT (p=9.65e-01): No strong evidence that all multi-planet ratios prefer Farey fractions.
- TEST 3 SIGNIFICANT (p=8.86e-28): Real systems cluster at lower Farey levels than random.
- TEST 4 SIGNIFICANT (p=3.56e-02): Real ratios sit shallower in the Stern-Brocot tree (d=0.07).
- TEST 5 NOT SIGNIFICANT (p=0.5130): Known resonant chains do not stand out from the general population in Farey error.

## Known Resonant Chain Details

| System | Ratio | Nearest Farey | Error | SB Depth |
|--------|-------|---------------|-------|----------|
| TRAPPIST-1 | 1.603055 | 8/5 | 0.003055 | 18 |
| TRAPPIST-1 | 1.671893 | 5/3 | 0.005226 | 25 |
| TRAPPIST-1 | 1.506714 | 3/2 | 0.006714 | 40 |
| TRAPPIST-1 | 1.509182 | 3/2 | 0.009182 | 30 |
| TRAPPIST-1 | 1.341558 | 4/3 | 0.008224 | 17 |
| TRAPPIST-1 | 1.519769 | 3/2 | 0.019769 | 15 |
| HD 110067 | 1.500349 | 3/2 | 0.000349 | 3 |
| HD 110067 | 1.500664 | 3/2 | 0.000664 | 3 |
| HD 110067 | 1.500666 | 3/2 | 0.000666 | 3 |
| HD 110067 | 1.333369 | 4/3 | 0.000035 | 4 |
| HD 110067 | 1.333947 | 4/3 | 0.000614 | 4 |
| Kepler-223 | 1.333286 | 4/3 | 0.000047 | 4 |
| Kepler-223 | 1.502055 | 3/2 | 0.002055 | 3 |
| Kepler-223 | 1.333835 | 4/3 | 0.000502 | 4 |
| TOI-178 | 1.691504 | 17/10 | 0.008496 | 15 |
| TOI-178 | 2.024887 | 2 | 0.024887 | 42 |
| TOI-178 | 1.519340 | 3/2 | 0.019340 | 17 |
| TOI-178 | 1.528965 | 17/11 | 0.016490 | 16 |
| TOI-178 | 1.359952 | 15/11 | 0.003684 | 9 |
| Kepler-80 | 3.113356 | 28/9 | 0.002245 | 18 |
| Kepler-80 | 1.511900 | 3/2 | 0.011900 | 25 |
| Kepler-80 | 1.518327 | 3/2 | 0.018327 | 16 |
| Kepler-80 | 1.350387 | 15/11 | 0.013249 | 14 |
| Kepler-80 | 1.537828 | 17/11 | 0.007627 | 16 |
| Kepler-60 | 1.250273 | 5/4 | 0.000273 | 5 |
| Kepler-60 | 1.334062 | 4/3 | 0.000729 | 4 |
| GJ 876 | 15.527098 | 7/2 | 12.027098 | 29 |
| GJ 876 | 2.031255 | 2 | 0.031255 | 34 |
| GJ 876 | 2.033163 | 2 | 0.033163 | 32 |
| HR 8799 | 1.864865 | 13/7 | 0.007722 | 12 |
| HR 8799 | 2.463768 | 27/11 | 0.009223 | 14 |

## Figures

- `exoplanet_test1_farey_proximity.png` - Farey error distributions
- `exoplanet_test3_farey_level.png` - Farey level clustering
- `exoplanet_test4_sb_depth.png` - Stern-Brocot depth distributions
- `exoplanet_resonant_chains.png` - Resonant chain ratios vs Farey fractions
- `exoplanet_ratio_scatter.png` - All ratios scatter plot

## Methodology

1. Downloaded all confirmed planets in systems with 3+ planets from NASA Exoplanet Archive
2. Computed consecutive period ratios (sorted by period within each system)
3. For each ratio, found the nearest fraction p/q with q <= 12
4. Compared real distributions against random uniform ratios in the same range
5. Used two-sample KS tests and one-sided Mann-Whitney U tests
6. Effect sizes reported as Cohen's d where applicable

## Notes

- The Farey order N=12 was chosen to capture common MMR ratios
  (3:2, 4:3, 5:3, 5:4, 2:1, 8:5) while avoiding overfitting with too many fractions
- Stern-Brocot depth computed as sum of continued fraction coefficients
- Random baseline uses uniform distribution in the observed ratio range
- Known resonant systems represent a small fraction of all multi-planet systems;
  the signal may be diluted in the full population
