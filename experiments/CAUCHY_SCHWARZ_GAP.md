# Cauchy-Schwarz Gap Analysis for R(p=997)

**Date:** 2026-04-05 10:48
**Prime:** p = 997, N = p-1 = 996
**Farey order:** F_{996}, |F_{996}| = 301,651

## Definitions

For f = a/b in F_N with gcd(a,b) = 1:
- **D(f)** = rank(f, F_N) - |F_N| · f  (rank deviation)
- **δ(f)** = f - {pf} = a/b - (pa mod b)/b  (insertion deviation)
- **R** = Σ D·δ / Σ δ²  (correlation ratio)
- **CS bound** = √(Σ D²) / √(Σ δ²)  (Cauchy-Schwarz upper bound on |R|)

## Global Results

| Quantity | Value |
|:---------|------:|
| Σ(D·δ) | 102,036.937773 |
| Σ(δ²) | 49,782.644465 |
| Σ(D²) | 57,738,407.89 |
| **R** | **2.0496488057** |
| **CS bound** | **34.0559830305** |
| **Tightness** |R|/CS | **0.0601846907** |
| **Looseness** CS/|R| | **16.6155×** |

## Cancellation Decomposition

The gap between |R| and the CS bound arises from two sources:

1. **Within-denominator cancellation**: D·δ products with different signs
   for fractions sharing the same denominator b.
2. **Cross-denominator cancellation**: per-denominator sums Σ_b(D·δ) with
   different signs across different b values.

| Stage | Raw | Retained | Cancelled |
|:------|----:|---------:|----------:|
| Pointwise → per-denom | 540,560.5191 | 135,678.0556 | 74.90% |
| Per-denom → global | 135,678.0556 | 102,036.9378 | 24.79% |

**Key finding:** ~75% of the raw |D·δ| mass cancels within
fixed denominators. Only ~25% additional cancellation occurs
when summing across denominators. The within-denominator oscillation of D and δ
is the dominant source of the Cauchy-Schwarz gap.

## Denominator Sign Distribution

| Category | Count |
|:---------|------:|
| Active denominators | 996 |
| Positive R_b | 832 |
| Negative R_b | 152 |
| Zero R_b | 12 |

## Contribution by Denominator Size Band

| Band | Σ weighted R_b | # denoms | # pos | # neg |
|:-----|---------------:|---------:|------:|------:|
| 2–49 | -0.0005579013 | 48 | 17 | 26 |
| 50–99 | +0.0103410367 | 50 | 36 | 13 |
| 100–199 | +0.0443979594 | 100 | 83 | 16 |
| 200–399 | +0.3362934689 | 200 | 181 | 17 |
| 400–699 | +1.1068856085 | 300 | 285 | 14 |
| 700–996 | +0.5522886336 | 297 | 230 | 66 |

## Top 30 Denominators by |Weighted Contribution|

| b | φ(b) | Σ D·δ | Σ δ² | R_b | weight | w·R_b |
|---:|-----:|------:|-----:|----:|-------:|------:|
| 985 | 784 | -737.382741 | 121.551269 | -6.066434 | 0.002442 | -0.01481204 |
| 503 | 502 | +692.288270 | 93.188867 | +7.428873 | 0.001872 | +0.01390622 |
| 991 | 990 | -655.550959 | 138.193744 | -4.743709 | 0.002776 | -0.01316826 |
| 961 | 930 | -625.315297 | 151.371488 | -4.130998 | 0.003041 | -0.01256091 |
| 973 | 828 | -601.804728 | 133.623844 | -4.503723 | 0.002684 | -0.01208865 |
| 925 | 720 | -592.841081 | 118.516757 | -5.002171 | 0.002381 | -0.01190859 |
| 839 | 838 | +578.056019 | 138.271752 | +4.180579 | 0.002778 | +0.01161160 |
| 937 | 936 | -564.146211 | 153.859125 | -3.666641 | 0.003091 | -0.01133219 |
| 509 | 508 | +562.184676 | 88.039293 | +6.385611 | 0.001768 | +0.01129278 |
| 671 | 600 | +554.622951 | 103.308495 | +5.368609 | 0.002075 | +0.01114089 |
| 719 | 718 | +541.303199 | 120.453408 | +4.493880 | 0.002420 | +0.01087333 |
| 791 | 672 | +530.761062 | 109.522124 | +4.846154 | 0.002200 | +0.01066157 |
| 599 | 598 | +498.245409 | 107.015025 | +4.655845 | 0.002150 | +0.01000842 |
| 899 | 840 | +496.460512 | 140.191324 | +3.541307 | 0.002816 | +0.00997256 |
| 779 | 720 | +492.785623 | 120.010270 | +4.106195 | 0.002411 | +0.00989874 |
| 501 | 332 | +475.293413 | 66.395210 | +7.158550 | 0.001334 | +0.00954737 |
| 987 | 552 | -473.489362 | 81.155015 | -5.834382 | 0.001630 | -0.00951113 |
| 955 | 760 | -472.848168 | 122.659686 | -3.854960 | 0.002464 | -0.00949825 |
| 611 | 552 | +471.158756 | 90.749591 | +5.191855 | 0.001823 | +0.00946432 |
| 995 | 792 | -466.592965 | 65.933668 | -7.076703 | 0.001324 | -0.00937260 |
| 863 | 862 | +458.858633 | 142.838934 | +3.212420 | 0.002869 | +0.00921724 |
| 749 | 636 | +449.423231 | 112.870494 | +3.981760 | 0.002267 | +0.00902771 |
| 695 | 552 | +445.064748 | 94.048921 | +4.732269 | 0.001889 | +0.00894016 |
| 755 | 600 | +443.947020 | 101.880795 | +4.357514 | 0.002047 | +0.00891771 |
| 977 | 976 | -437.853634 | 153.938588 | -2.844340 | 0.003092 | -0.00879531 |
| 499 | 498 | +436.090180 | 165.334669 | +2.637621 | 0.003321 | +0.00875988 |
| 519 | 344 | +436.046243 | 60.947977 | +7.154401 | 0.001224 | +0.00875900 |
| 527 | 480 | +428.652751 | 82.573055 | +5.191194 | 0.001659 | +0.00861049 |
| 993 | 660 | -428.610272 | 83.250755 | -5.148425 | 0.001672 | -0.00860963 |
| 551 | 504 | +423.393829 | 87.513612 | +4.838034 | 0.001758 | +0.00850485 |

## Analysis

### Where does the cancellation come from?

The Cauchy-Schwarz bound is 16.6× looser than the actual |R| value.
This gap decomposes as follows:

1. **Within-denominator oscillation (75%)**: For a fixed denominator b,
   the products D(a/b)·δ(a/b) alternate in sign as a varies over the φ(b)
   coprime numerators. The rank deviation D has a known sawtooth structure
   (related to Dedekind sums), while δ depends on the arithmetic of p·a mod b.
   These two oscillations are only weakly correlated, causing massive cancellation.

2. **Cross-denominator sign changes (25%)**: The per-denominator
   sums R_b have 832 positive and 152 negative values. However, the
   positive values dominate (832 vs 152), so the net effect after
   cross-denominator summation is a further 25% reduction.

### Implications for tighter bounds

To close the Cauchy-Schwarz gap, we need to exploit the within-denominator
structure. For each fixed b, the sum Σ_{gcd(a,b)=1} D(a/b)·δ(a/b) can be
related to Kloosterman sums S(p, 1; b) via the Dedekind sum representation of D.
The exponential sum cancellation within Kloosterman sums is precisely what
drives the within-denominator cancellation observed here.

A tighter bound should replace Cauchy-Schwarz with a per-denominator estimate:
  R = Σ_b (w_b · R_b) where w_b = Σ_b δ² / Σ_all δ²
and bound each R_b using the Weil bound for Kloosterman sums.
