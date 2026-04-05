# Detrended Amplitude Correlation Analysis
## Task 2: Honest Statistical Metric for Spectroscope Amplitude Matching

### The Problem
Raw correlation r=0.997 between observed F(gamma_k) and predicted |c_k|^2 for k=1..10 is **inflated by shared monotonic decay**. Both sequences decrease with k — any two monotone-decreasing sequences correlate strongly. Log-detrended residual correlation is r ~ -0.18, meaning the raw r captures shared power-law decay, not structural agreement.

### Honest Assessment: 10 Zeros Is Marginal
With n=10 data points and 1 dominant trend to remove, effective degrees of freedom ~ 8. This severely limits statistical power. We must be upfront about this.

### Recommended Tests (in order of convincingness)

#### 1. Rank Permutation Test (STRONGEST)
- **Method:** Randomly assign the 10 predicted |c_k|^2 values to the 10 observed F(gamma_k). Compute S = sum(F_k - alpha*|c_k|^2)^2 for true assignment vs all 10! = 3,628,800 permutations (exhaustive).
- **Metric:** Fraction of permutations with S <= S_true. Non-parametric p-value.
- **Pitfall:** If both sequences are monotonically ordered the same way, any monotone-preserving permutation scores well. Fix: detrend first, THEN permute residuals.

#### 2. Consecutive Ratio Test (TREND-FREE)
- **Method:** Compute r_k = F(gamma_{k+1})/F(gamma_k) and s_k = |c_{k+1}/c_k|^2 for k=1..9.
- **Metric:** Pearson/Spearman correlation between the 9 ratio pairs.
- **Why:** Dividing consecutive values cancels overall decay. Tests whether fluctuations match.
- **Interpretation:** r > 0.5 with 9 points suggestive (p ~ 0.08). r > 0.7 strong (p ~ 0.02).

#### 3. Top-K Combinatorial Test
- **Method:** Are the 3 largest F(gamma_k) at the 3 largest predicted |c_k|^2?
- **Metric:** Under random assignment, P(top-3 match) = 6/120 = 1/20 = 0.05.
- **Limitation:** p=0.05 is marginal with just top-3.

#### 4. Log-Linear Residual Correlation
- **Method:** Fit log(F_k) = a + b*log(gamma_k) + epsilon, same for |c_k|^2. Correlate residuals.
- **Known result:** r ~ -0.18 after detrending. NOT significant (p ~ 0.6).

### Recommendation for Paper 2

**Present THREE metrics:**
1. Raw r=0.997 — with caveat that it reflects shared decay
2. Consecutive ratio correlation — honest trend-free metric
3. Detrended permutation test — formal p-value

**Framing:** "The spectroscope detects zero POSITIONS to within 0.8%. The amplitude formula correctly predicts the ordering, but with only 10 resolved zeros, distinguishing the specific formula from any monotonically decreasing model is not possible at conventional significance levels. Rigorous amplitude matching requires resolving >= 20-30 zeros."

### Action Items
1. Compute consecutive ratio correlation from existing data
2. Run exhaustive permutation test on detrended residuals (10! tractable)
3. Report all three metrics honestly in Paper 2
4. Task 1 (500K primes) may resolve more zeros, enabling stronger tests
