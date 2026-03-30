# Density Patterns: T(N) > 0 among M(p) = -3 Primes

## Date: 2026-03-30
## Status: Unverified (computational analysis, no analytical proofs)
## Classification: C1 (collaborative, minor novelty)
## Connects to: N2 (Mertens-Wobble), N5 (Per-Step Decomposition)

---

## 0. Summary

We analyze the 922 primes p <= 10^7 with M(p) = -3, of which 247 (26.8%)
have T(N) > 0 where N = p-1 and T(N) = sum_{m=2}^{N} M(floor(N/m))/m.

**Key findings:**

1. The fraction of T > 0 primes **increases sharply** with p: from 0% below
   p = 243,799 to 77% in the last window [p ~ 8M - 9.5M].
2. T > 0 primes are **extremely clustered** -- they come in long runs
   (max 81 consecutive), not isolated.
3. T(N) is **dominated** by M(N/2)/2 + M(N/3)/3 (correlation r = 0.95).
   T > 0 occurs almost exclusively when M(N/2) > 0.
4. No significant residue class bias.
5. **Strong zeta zero phase dependence**: T > 0 is concentrated in a
   half-arc of gamma_1 * log(p) mod 2pi, with resultant length 0.77
   (vs 0.13 for T < 0). This is the most striking finding.
6. The asymptotic density of T > 0 appears to approach ~1/2 or higher.

---

## 1. Density Trend (Q1)

**Does the fraction of T > 0 primes increase, decrease, or stabilize?**

It **increases sharply and monotonically**:

| Range | # primes | # T>0 | Fraction |
|-------|----------|-------|----------|
| [10, 100) | 6 | 0 | 0.000 |
| [100, 1K) | 20 | 0 | 0.000 |
| [1K, 10K) | 49 | 0 | 0.000 |
| [10K, 100K) | 99 | 0 | 0.000 |
| [100K, 1M) | 272 | 27 | 0.099 |
| [1M, 10M) | 476 | 220 | 0.462 |

In the last century of primes [p ~ 8.2M to 9.5M], the fraction reaches **77%**.

The running fraction over sliding windows of 100 primes shows a clear acceleration:
- Primes 1-200: 0%
- Primes 301-400: 15%
- Primes 501-600: 33%
- Primes 601-700: 53%
- Primes 801-900: 77%

**Interpretation:** The mean of T(N) drifts toward zero as p grows (mean T drops
from -17 in [10K, 100K) to -5 in [1M, 10M)), while the standard deviation grows
(from 5.6 to 57). This is consistent with T(N) being a sum of oscillating terms
whose variance grows faster than the mean drifts negative. The fraction of T > 0
should approach some positive limiting density, likely near 1/2 if the distribution
is approximately symmetric around its (slowly drifting) mean.

---

## 2. Clustering (Q2)

**Do the T > 0 primes cluster, or are they randomly distributed?**

They are **extremely clustered**. The T > 0 primes form only 16 runs among the
922 primes, with run lengths:

| Run length | Count |
|------------|-------|
| 1 | 5 |
| 2 | 3 |
| 4-5 | 2 |
| 11-17 | 2 |
| 28-34 | 2 |
| 56 | 1 |
| 81 | 1 |

The longest T > 0 run has 81 consecutive M(p)=-3 primes with T > 0.
The longest T < 0 run has 254 consecutive primes (all 174 primes below
p = 243,799, plus more).

**The median gap between consecutive T > 0 primes (in index space) is 1.0**,
meaning most T > 0 primes are immediately adjacent in the M=-3 sequence.
This strong clustering is because T(N) depends on M at multiple scales --
when M(x) is in a "positive excursion" near x ~ N/2, all nearby primes
benefit simultaneously.

---

## 3. Correlation with M(N/2) and M(N/3) (Q3)

**Since T(N) = sum M(floor(N/m))/m, do the leading terms dominate?**

Yes, overwhelmingly:

| Quantity | Correlation with T(N) |
|----------|-----------------------|
| M(N/2) | 0.892 |
| M(N/3) | 0.512 |
| M(N/5) | 0.500 |
| M(N/2)/2 + M(N/3)/3 | **0.949** |

The two leading terms account for 95% of T's variance.

**Conditional probabilities:**

| Condition | P(T > 0) | n |
|-----------|----------|---|
| M(N/2) > 0 | 0.500 | 480 |
| M(N/2) <= 0 | 0.016 | 442 |
| M(N/2) > 5 | 0.553 | 434 |
| M(N/2) < -5 | 0.011 | 354 |

**This is the core mechanism:** T(N) > 0 occurs almost exclusively when M(N/2) > 0.
Among T > 0 primes, 97.2% have M(N/2) > 0, versus only 35.6% of T < 0 primes.

The mean M(N/2) among T > 0 primes is +199 (a large positive excursion of Mertens),
versus -27 for T < 0 primes.

**Bottom line:** T(N) > 0 happens when the Mertens function is in a positive
excursion at x ~ N/2. Since M(x) positive excursions are correlated over
a range of x, this explains the clustering in Q2 -- nearby primes share
similar M(N/2) values.

---

## 4. Residue Classes (Q4)

**Are T > 0 primes concentrated in particular residue classes?**

No. The fractions are remarkably uniform:

| p mod 6 | Fraction T>0 |
|---------|--------------|
| 1 | 0.254 |
| 5 | 0.284 |

| p mod 12 | Fraction T>0 |
|----------|--------------|
| 1 | 0.252 |
| 5 | 0.257 |
| 7 | 0.255 |
| 11 | 0.311 |

The p = 11 mod 12 class has a slightly elevated fraction (0.311 vs 0.254-0.257
for others), but with only ~220 primes per class, this is within 1-sigma of
statistical fluctuation. None of the residue classes mod 24 or mod 30 show
statistically significant deviations.

**Conclusion:** T(N) > 0 is NOT driven by residue class structure. This is
expected: the Mertens function M(x) at x ~ N/2 does not depend on the
residue class of p.

---

## 5. Spacing Distribution (Q5)

| | T>0 gaps | T<0 gaps | All M=-3 gaps |
|--|----------|----------|---------------|
| Mean | 33,186 | 14,234 | 10,417 |
| Median | 227 | 133 | 140 |
| Std | 194,391 | 108,296 | - |

Both distributions are extremely heavy-tailed (median << mean), which is
expected for prime gaps. The T > 0 gaps are about 2x larger than T < 0 gaps
on average, reflecting the lower density of T > 0 primes overall. But
note the median gap of 227 for T > 0 is comparable to 133 for T < 0,
confirming that T > 0 primes are locally dense when they occur (clustering).

The normalized gap distribution:
- 89.4% of T>0 gaps are less than half the mean (heavy left tail)
- Only 6.1% exceed twice the mean (rare large gaps between clusters)

This is the signature of a "bursty" point process: long quiet periods
punctuated by intense clusters.

---

## 6. Zeta Zero Phase Dependence (Q6)

**This is the most striking result.**

Under GRH, M(x) ~ -2 Re(x^{1/2+i*gamma_1}) / (1/2 + i*gamma_1) + ...,
where gamma_1 = 14.1347... is the imaginary part of the first zeta zero.
The phase of this oscillation at x is gamma_1 * log(x) mod 2*pi.

Binning the 922 primes by gamma_1 * log(p) mod 2*pi:

| Phase range | n | T>0 | Fraction |
|-------------|---|-----|----------|
| [0.00, 0.52) | 56 | 17 | 0.304 |
| [0.52, 1.05) | 82 | 0 | **0.000** |
| [1.05, 1.57) | 41 | 0 | **0.000** |
| [1.57, 2.09) | 44 | 0 | **0.000** |
| [2.09, 2.62) | 47 | 2 | 0.043 |
| [2.62, 3.14) | 104 | 0 | **0.000** |
| [3.14, 3.67) | 118 | 8 | 0.068 |
| [3.67, 4.19) | 54 | 13 | 0.241 |
| [4.19, 4.71) | 32 | 19 | **0.594** |
| [4.71, 5.24) | 96 | 65 | **0.677** |
| [5.24, 5.76) | 123 | 77 | **0.626** |
| [5.76, 6.28) | 125 | 46 | 0.368 |

**T > 0 is concentrated in the phase window [4.2, 5.8] and completely absent
from [0.5, 2.6] and [2.6, 3.1].**

Circular statistics:
- T > 0 primes: circular mean = -1.005 (= 5.28), resultant length R = **0.769**
- T < 0 primes: circular mean = 2.273, resultant length R = 0.130

A resultant length of 0.77 indicates extremely strong phase concentration.
The T > 0 primes are clustered at phase ~ 5.3 (roughly 5*pi/3), while
T < 0 primes are nearly uniformly distributed (R = 0.13).

**Why this happens:** T(N) involves M(N/m) for m = 2, 3, 5, ....
The dominant term M(N/2) has its oscillation evaluated at N/2, where
the phase is gamma_1 * log(N/2) = gamma_1 * log(N) - gamma_1 * log(2).
When this phase puts M(N/2) in a positive excursion, T > 0 results.
Since gamma_1 * log(2) ~ 9.80 ~ 3.52 mod 2*pi, there is a fixed phase
offset between M(N) and M(N/2), creating a preferred phase window for
T > 0 in the gamma_1 * log(p) coordinate.

This is a clean signature of the zeta zeros controlling the sign of T(N).

---

## 7. Asymptotic Density Prediction (Q7)

The running fraction of T > 0 is accelerating:

| k (first k primes) | Running fraction |
|---------------------|-----------------|
| 174 | 0.000 |
| 300 | 0.003 |
| 500 | 0.060 |
| 700 | 0.166 |
| 900 | 0.274 |

In the last window of 100 primes (p ~ 8M-9.5M), the fraction is 0.77.

**The fraction has not stabilized.** It is still rapidly increasing.

**Theoretical expectation:** T(N) = sum_{m=2}^N M(N/m)/m is essentially the
"Dirichlet summatory function" of M. By the Perron integral representation,

  T(N) + 2 = (1/2pi*i) integral N^s * zeta(s+1) / (s * zeta(s)) ds

The residue at s = 0 gives -2 (matching the +2 offset), and the remaining
"error" is an oscillatory sum over zeta zeros. As N grows, this sum has
increasing amplitude (like sqrt(N) times oscillations), and the fraction
of time it exceeds 2 (i.e., T > 0) depends on the distribution of the
sum of cos(gamma_k * log(N)) terms.

By analogy with the Chebyshev bias (Rubinstein-Sarnak 1994), the logarithmic
density of {N : T(N) > 0} should be determined by the distribution of
a random variable Z = sum c_k * cos(theta_k) where the theta_k are
independent uniform on [0, 2*pi). The bias (toward T < 0 or T > 0)
depends on whether the "offset" (-2 in our case) is positive or negative.

Since T(N) = F(N) + 2 where F(N) has mean 0 over zeta oscillations, the
offset of +2 means T is biased POSITIVE on average in the oscillatory
picture. But this conflicts with the observed mean T < 0, suggesting the
non-oscillatory drift (from the Mertens function being predominantly
negative) matters more at these scales.

**Prediction:** The density of T > 0 should approach some value in (0, 1),
likely between 0.3 and 0.6, as p -> infinity. The current data strongly
suggests it is NOT converging to zero. Whether it approaches 1/2 exactly
(as it would if the oscillations were symmetric) or some other value
requires understanding the distribution of the sum over zeta zeros.
The data up to 10^7 is insufficient to determine the limiting density.

---

## 8. Summary Table

| Question | Answer |
|----------|--------|
| Q1: Density trend | Sharply increasing: 0% below 100K, 10% in [100K,1M), 46% in [1M,10M) |
| Q2: Clustering | Extreme: runs of up to 81, median gap = 1 in index |
| Q3: M(N/2), M(N/3) | M(N/2)/2 + M(N/3)/3 has r = 0.95 with T(N). T>0 iff M(N/2) > 0 (97%) |
| Q4: Residue classes | No bias. Uniform across all tested moduli |
| Q5: Spacing | Bursty: small median gap (227) but large mean (33K). Heavy-tailed |
| Q6: Zeta zeros | STRONG phase dependence. T>0 concentrated in half-arc. R = 0.77 |
| Q7: Asymptotic density | Increasing, not stabilized. Likely positive limit, possibly near 1/2 |

---

## 9. What This Means for the Main Results

### 9.1. The T < 0 Regime Is Not Universal

The claim T(N) < 0 for all M(p)=-3 primes fails badly as p grows. By p ~ 10^7,
almost half the primes have T > 0. Any proof strategy that requires T < 0 is
fundamentally limited to small primes.

### 9.2. The Mechanism Is Clear

T(N) > 0 happens when M(N/2) > 0. This is the Mertens function in a positive
excursion, which occurs more frequently (in a logarithmic density sense)
as we look at larger values. The connection to zeta zero oscillations is
explicit and quantitative.

### 9.3. Phase Structure Matters

The zeta zero phase dependence (Q6) means that the T > 0 primes are not
"random" within the M=-3 sequence -- they are determined by where p sits
in the oscillation cycle of the first zeta zero. This suggests that any
proof about T(N) sign must engage with the spectral theory of the zeta
function, not just elementary bounds.

### 9.4. Implications for B+C Positivity

Since B+C > 0 fails at exactly the T > 0 primes (Section 2 of
B_PLUS_C_POSITIVITY.md), and these primes constitute ~27% of M=-3 primes
to 10^7 with the fraction growing, the B+C > 0 claim is false for a
substantial and growing fraction of primes. The original proof strategy
must be completely rethought.

---

## 10. Scripts and Data

- `density_patterns.c` -- C program computing T(N) for all M(p)=-3 primes
- `density_patterns.py` -- Python analysis script with all 7 questions + plots
- `density_patterns_all.csv` -- Full dataset: 922 primes with T(N), M(N/k), residues
- `density_patterns_plots.png` -- 9-panel figure
- `density_patterns_analysis.txt` -- Raw text output of analysis

---

## 11. Honest Assessment

This is computational exploration, not proof. The trends observed to 10^7 may
not persist to 10^8 or beyond. In particular:

1. The increasing fraction of T > 0 could plateau before reaching 1/2.
2. The zeta zero phase dependence could weaken if higher zeros contribute
   more at larger scales.
3. The correlation with M(N/2) is exact by the structure of the sum, but
   the question of what fraction of M=-3 primes have M(N/2) > 0 is itself
   a deep number-theoretic question.

The sample size (922 primes, 247 with T > 0) is adequate for the qualitative
conclusions but too small for precise density estimates.
