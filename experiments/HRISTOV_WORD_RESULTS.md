# Hristov Three-Body Orbits: Free-Group Word Analysis

## Method

1. **All 4860 Hristov syzygies are palindromes** (time-reversal symmetric Euler-configuration orbits).
2. The full-period braid word freely reduces to the identity (w * w^{-1} = e) for every orbit.
3. **Solution:** Use the **half-period word** (first half of syzygy) as the topologically meaningful free-group element.
4. Map half-period words to Gamma(2) matrices via the standard embedding a -> [[1,2],[0,1]], b -> [[1,0],[2,1]].

## Transition Mapping

| Transition | Generator | Interpretation |
|:----------:|:---------:|:---------------|
| 1 -> 2 | a | sigma_1 (forward) |
| 2 -> 1 | A = a^{-1} | sigma_1^{-1} (backward) |
| 2 -> 3 | b | sigma_2 (forward) |
| 3 -> 2 | B = b^{-1} | sigma_2^{-1} (backward) |
| 1 -> 3 | B | skip backward |
| 3 -> 1 | b | skip forward |

## Key Findings

- **Orbits processed:** 4860
- **Palindromic:** 4860/4860 (100.0%)
- **Nontrivial half-words:** 4552/4860
- **Hyperbolic (|trace| > 2):** 4552/4860 (93.7%)
- **Trivial half-words:** 308/4860

## Correlations with Lyapunov Exponents

### Hyperbolic orbits (n=4552)

| Quantity | Pearson r | p-value |
|:---------|:---------:|:-------:|
| log(spectral_radius) | -0.0961 | 8.28e-11 |
| half_word_length | -0.0950 | 1.35e-10 |
| log(|trace|) | -0.0962 | 7.66e-11 |
| log(rho)/word_len | -0.0331 | 2.55e-02 |

### All orbits (n=4860)

| Quantity | Pearson r | p-value |
|:---------|:---------:|:-------:|
| half_reduced_len | -0.1342 | 5.74e-21 |
| half_raw_len | +0.1096 | 1.86e-14 |
| syzygy_length | +0.1816 | 2.66e-37 |
| raw_word_entropy | -0.1494 | 1.13e-25 |
| |abel_a| + |abel_b| | -0.1342 | 5.74e-21 |

## By Topological Class

| Class | n | Avg half-word len | Avg |trace| | Hyperbolic | Avg Lyapunov |
|:-----:|:---:|:---------:|:----------:|:---------:|:----------:|
| 1 | 1422 | 11.4 | 2339710799.2 | 1422 | 32.70 |
| 2 | 1672 | 10.8 | 19575712116.7 | 1672 | 32.36 |
| 3 | 1766 | 9.9 | 2789519245.3 | 1458 | 35.64 |

## Sample Half-Period Free-Group Words (first 30)

| # | Class | Half-word | Len | |Trace| | log(rho) | Lyapunov |
|:-:|:-----:|:----------|:---:|:------:|:--------:|:--------:|
| 1 | 1 | BABB | 4 | 14 | 2.634 | 15.43 |
| 2 | 1 | BABB | 4 | 14 | 2.634 | 18.55 |
| 3 | 2 | babb | 4 | 14 | 2.634 | 18.01 |
| 4 | 3 |  | 0 | 2 | 0.000 | 30.16 |
| 5 | 1 | BABB | 4 | 14 | 2.634 | 20.22 |
| 6 | 2 | babb | 4 | 14 | 2.634 | 19.41 |
| 7 | 3 | BABBABBABBAB | 12 | 9602 | 9.170 | 35.87 |
| 8 | 1 | BABB | 4 | 14 | 2.634 | 21.34 |
| 9 | 2 | babb | 4 | 14 | 2.634 | 20.38 |
| 10 | 3 |  | 0 | 2 | 0.000 | 29.44 |
| 11 | 3 |  | 0 | 2 | 0.000 | 34.62 |
| 12 | 3 | BABBABBABBAB | 12 | 9602 | 9.170 | 46.28 |
| 13 | 1 | BABBABBABB | 10 | 1366 | 7.220 | 25.68 |
| 14 | 2 | BA | 2 | 6 | 1.763 | 25.75 |
| 15 | 2 | BA | 2 | 6 | 1.763 | 12.20 |
| 16 | 2 | BABBABBABBABBA | 14 | 56246 | 10.937 | 12.16 |
| 17 | 3 | BABBABBABBAB | 12 | 9602 | 9.170 | 36.92 |
| 18 | 1 | BABB | 4 | 14 | 2.634 | 22.19 |
| 19 | 2 | babb | 4 | 14 | 2.634 | 21.12 |
| 20 | 3 |  | 0 | 2 | 0.000 | 39.18 |
| 21 | 3 |  | 0 | 2 | 0.000 | 41.31 |
| 22 | 2 | BA | 2 | 6 | 1.763 | 39.72 |
| 23 | 2 | BABBABBABBABBA | 14 | 56246 | 10.937 | 39.39 |
| 24 | 3 | BABBABBABBAB | 12 | 9602 | 9.170 | 17.60 |
| 25 | 3 | babbab | 6 | 98 | 4.585 | 16.64 |
| 26 | 1 | BABBABBABBABBABB | 16 | 133854 | 11.805 | 24.08 |
| 27 | 3 | babbabbabbab | 12 | 9602 | 9.170 | 41.59 |
| 28 | 1 | BABB | 4 | 14 | 2.634 | 8.13 |
| 29 | 1 | BABB | 4 | 14 | 2.634 | 29.15 |
| 30 | 2 | babb | 4 | 14 | 2.634 | 29.20 |

## Data Files

- Full results: `hristov_freegroup_results.csv`
- This report: `HRISTOV_WORD_RESULTS.md`
