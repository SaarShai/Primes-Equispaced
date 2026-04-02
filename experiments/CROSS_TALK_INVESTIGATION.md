# Cross-Talk Investigation: Why the Zeta Zero Appears in T_chi7 for All Primes

**Date:** 2026-03-31
**Status:** Analysis complete, mechanism identified
**Verification Status:** 🔬 Unverified — results require independent replication
**Classification:** C1 (collaborative, minor novelty) — the finding is a diagnostic clarification, not a new discovery

---

## The Problem

T_chi7_quad (Farey discrepancy twisted by the quadratic character mod 7) shows **19.4x sigma** phase-lock at the **zeta zero** gamma_1 = 14.13 when computed over ALL primes p <= 50,000. This is deeply anomalous — T_chi7 should only phase-lock at zeros of L(s, chi_7), not at zeros of zeta(s).

With the M(p) = -3 restriction (145 primes), the signal drops to 3.3x — borderline, and previously interpreted as noise. Why does fixing M(p) suppress the cross-talk?

## Summary of Findings

**The cross-talk is mediated by the strong anticorrelation between T_chi7 and T_plain.** Since sgn(T_chi7) = -sgn(T_plain) for 77% of primes, the zeta-zero signal in T_plain is inherited by T_chi7 with flipped sign. Regressing out T_plain reduces the zeta-zero sigma from 19.4 to 5.3, while the chi7-zero sigma INCREASES from 12.5 to 21.3. The M(p)=-3 restriction works because it fixes a variable that both T_plain and T_chi7 strongly depend on, partially breaking their coupling.

---

## Phase 1 Results: Correlations and Strata

### Test A: Pairwise Correlations (all primes <= 50,000, n=5133)

| Pair | Correlation | Fisher z | Interpretation |
|------|------------|----------|----------------|
| T_chi7 vs M(p) | **+0.581** | 47.5 | T_chi7 grows with M(p) |
| T_plain vs M(p) | **-0.915** | -111.6 | T_plain is nearly a function of M(p) |
| T_chi7 vs T_plain | **-0.620** | -52.0 | Strong anticorrelation |

The -0.92 correlation between T_plain and M(p) is expected: T_plain(N) = 1 - alpha(N) where alpha is the Farey discrepancy, and M(N) = N*(1 - 2*alpha(N)), so T_plain is a linear function of M(p)/p plus lower-order terms.

The -0.62 correlation between T_chi7 and T_plain arises because both involve sums of mu(k)/m over the same divisors of N = p-1. The mu(k) values dominate the sum structure, and both T_plain and T_chi7 share the same mu(k) — they differ only in the chi(k) weighting.

### Test B: Phase-Lock at Zeta Zero by M(p) Stratum

| Sample | n | frac(T_chi7 > 0) | max sigma at zeta zero |
|--------|---|-------------------|----------------------|
| All primes | 5133 | 0.738 | **19.4x** |
| M(p) = -3 | 145 | 0.717 | 3.3x |
| M(p) = -2 | 136 | 0.794 | 3.1x |
| M(p) = -1 | 131 | 0.824 | 3.9x |
| M(p) = 0 | 120 | 0.867 | 2.9x |
| Random subsample (n=145) | 145 | ~0.77 | 3.4 +/- 0.5 |

**Critical observation:** Individual M(p) strata show 2.9-3.9x sigma — still above the 1x random expectation. The M(p)=-3 restriction does NOT fully remove cross-talk. The reduction from 19.4x to 3.3x is primarily a **sample size effect** (5133 vs 145 primes), since random subsamples of size 145 also give ~3.4x.

### Test E: Partial Correlation with Zeta Signal

| Measure | Value |
|---------|-------|
| corr(T_chi7, cos(gamma_zeta * log p)) | -0.009 (essentially zero) |
| Partial corr, conditioning linearly on M(p) | 0.080 |
| Within-stratum corr (weighted average) | -0.025 |

The LINEAR correlation between T_chi7 and the zeta oscillation is near zero. The phase-lock operates through the SIGN structure, not through linear dependence. The within-stratum correlations are small and sign-varying, confirming the cross-talk is not a simple confound through M(p).

---

## Phase 2 Results: Mechanistic Tests

### Test 1: Shuffle Test

Permuting T_chi7 values among primes (destroying the assignment of T_chi7(p) to prime p, while preserving the marginal distribution):

| | Sigma at zeta zero |
|--|---------------------|
| Original T_chi7 | **19.4** |
| Shuffled (100 trials) | mean 3.4, std 0.3, max 4.5 |

The original is **53.9 standard deviations** above the shuffled mean. **The cross-talk is prime-specific** — it requires the actual T_chi7(p) value to be associated with the correct prime p. This rules out any explanation based purely on the distribution of T_chi7 values.

### Test 2: Sign Coupling in Phase Space

The sign of T_chi7 depends strongly on the zeta phase gamma_zeta * log(p) mod 2pi:

| Phase sector | frac(T_chi7 > 0) | frac(T_plain > 0) |
|-------------|-------------------|-------------------|
| [0, pi/4) | 0.788 | 0.019 |
| [pi/4, pi/2) | **0.975** | 0.000 |
| [pi/2, 3pi/4) | **0.991** | 0.000 |
| [3pi/4, pi) | 0.948 | 0.003 |
| [pi, 5pi/4) | 0.583 | 0.003 |
| [5pi/4, 3pi/2) | 0.452 | 0.231 |
| [3pi/2, 7pi/4) | 0.518 | 0.063 |
| [7pi/4, 2pi) | 0.588 | 0.231 |

**Interpretation:** T_plain is almost always negative (frac > 0 is 0-23%). When T_plain IS positive (sectors 5-7), T_chi7 drops to ~50% positive. When T_plain is always negative (sectors 1-4), T_chi7 is 79-99% positive. **The signs are anticorrelated, and this anticorrelation is coherent with the zeta phase.**

### Test 3: Frequency Scan

The frequency scan reveals a fundamental problem with the test statistic:

| Gamma | T_chi7 sigma | T_plain sigma | Note |
|-------|-------------|---------------|------|
| 1.0 | 37.5 | 45.1 | Artifact (monotone trend) |
| 4.97 | 12.5 | 11.1 | chi7 zero |
| 10.0 | 20.9 | 11.6 | No known zero |
| 14.13 | 19.4 | 13.0 | Zeta zero |
| 17.0 | 7.8 | 4.6 | No known zero |

**The background sigma is extremely high** (mean 12.9 for T_chi7). The huge sigmas at low gamma are artifacts of the 74% positive bias in T_chi7: with 74% of phases in the "positive" class, R_positive is dominated by the mean of e^{i*gamma*log(p)} over most primes, which is large at low frequencies where cos(gamma*log(p)) is slowly varying.

The 19.4x at gamma=14.13 is NOT dramatically above the background mean of 12.9x. The test is confounded by the sign imbalance.

### Test 4: The Smoking Gun — Residualization

**This is the definitive test.** We regress T_chi7 linearly on T_plain and examine the residual:

T_chi7 = -0.623 * T_plain - 2.183 + residual

| Statistic | Original T_chi7 | Residualized T_chi7 |
|-----------|-----------------|---------------------|
| Sigma at zeta zero (14.13) | 19.4 | **5.3** |
| Sigma at chi7 zero (4.97) | 12.5 | **21.3** |
| corr with T_plain | -0.620 | 0.000 |

**The zeta-zero signal drops by 73%** (from 19.4 to 5.3) after removing the T_plain component. Simultaneously, **the chi7-zero signal nearly doubles** (from 12.5 to 21.3), becoming the dominant spectral peak in the residual.

After residualization, the frequency scan top-10 peaks are all at low gamma (artifact region), with the chi7 zero at 21.3x being the only physically meaningful peak.

---

## The Mechanism: Complete Explanation

### Why cross-talk appears with all primes

1. **T_chi7 and T_plain share arithmetic structure.** Both are computed as T(N) = sum_{m=2}^{N} M(N/m)/m, where M is either the plain or chi-twisted Mertens function. Since both use the same primes p and the same value N = p-1, and since mu(k) appears in both sums, the values are correlated.

2. **The correlation is strong and negative** (r = -0.62). Specifically, sgn(T_chi7) = -sgn(T_plain) for 77% of primes. Since T_plain is almost always negative (93% of primes have T_plain < 0), T_chi7 is almost always positive (74%).

3. **T_plain genuinely phase-locks at the zeta zero** (by the Perron integral mechanism: poles of 1/zeta(s)). This creates a phase-dependent sign pattern in T_plain.

4. **T_chi7 inherits this pattern with flipped sign.** Because sgn(T_chi7) ~ -sgn(T_plain), the phase-lock test on T_chi7 at the zeta zero detects the NEGATIVE image of the T_plain signal. In fact, -T_chi7 gives exactly the same 19.4x sigma at the zeta zero.

5. **The sigma statistic amplifies this through sample size.** With n=5133 primes and a 74/26 sign split, even a modest phase-coherence in the majority class gives high sigma (R * sqrt(n)). At n=145, the same R gives only ~3.3x.

### Why cross-talk disappears with M(p) = -3

It doesn't fully disappear — it drops from 19.4x to 3.3x. This drop has **two causes**:

1. **Sample size reduction** (primary): 5133 -> 145 primes. Random subsamples of 145 primes also give ~3.4x mean sigma, confirming this is the dominant effect.

2. **Partial decorrelation** (secondary): Fixing M(p) partially breaks the T_chi7 ~ T_plain coupling, because both depend on M(p). Within the M(p)=-3 stratum, the residual variation in T_chi7 and T_plain is less correlated. However, the within-stratum phase-lock at the zeta zero is still 2.9-3.9x, so the decorrelation is incomplete.

### The Perron integral perspective

From the Perron integral:

T_chi(N) + M_chi(N) = (1/2pi*i) integral N^s * F(s, chi) ds

where F(s, chi) has poles at zeros of L(s, chi). The cross-talk arises because **T_chi is not just the Perron integral** — it also contains M_chi(N), which is correlated with M(N) = M_plain(N) through shared mu values. The "contamination" enters through the arithmetic overlap in the partial sums, not through the analytic structure of L-functions.

---

## Implications

### For the phase-lock selectivity claim

The original claim — that T_chi selectively phase-locks at zeros of L(s,chi) and NOT at zeros of other L-functions — is **partially correct but requires qualification:**

- **After residualization against T_plain, the selectivity IS clean.** Residualized T_chi7 shows 21.3x at its own zero and only 5.3x at the zeta zero (which may itself be reducible further by residualizing against higher zeta harmonics).

- **The raw T_chi7 signal is contaminated by T_plain cross-talk.** This is an arithmetic artifact, not a failure of the Perron mechanism.

- **The M(p)=-3 restriction is primarily a sample-size reducer,** not a magic decorrelation filter. The original interpretation (that fixing M(p) breaks the coupling) is partially right but overstated — the dominant effect is simply having fewer primes.

### For publication

1. The phase-lock selectivity claim should be stated as: "After removing the zeta component (by regressing T_chi against T_plain), the residual T_chi selectively phase-locks at zeros of L(s,chi)."

2. The raw cross-talk should be disclosed and explained as arising from the arithmetic overlap between T_chi and T_plain.

3. The frequency scan background issue (high sigma at low gamma due to sign imbalance) should be addressed by using a better test statistic that normalizes for sign imbalance, or by always comparing to a proper null distribution.

---

## Suggested Fixes for Future Analysis

1. **Always residualize** T_chi against T_plain before testing at non-chi frequencies.
2. **Use a sign-balanced test statistic**: instead of splitting by T > 0 vs T < 0, use |R_all| = |mean(e^{i*gamma*log(p)} * sgn(T(p)))|, which naturally accounts for sign imbalance.
3. **Compare to permutation null**, not 1/sqrt(n). The permutation null (shuffling T values among primes) gives a proper background of ~3.4x at n=145, ~3.4x at n=5133. Any signal above this is real.
4. **The chi7 zero at 21.3x after residualization (vs background ~10x) is a genuine 2x above background.** More primes (p to 200K) would help establish this more clearly.

---

## Code

- Phase 1: `~/Desktop/Farey-Local/experiments/cross_talk_investigation.py`
- Phase 2: `~/Desktop/Farey-Local/experiments/cross_talk_phase2.py`
- Logs: `~/Desktop/Farey-Local/experiments/cross_talk_investigation.log`
- Original deep exploration: `~/Desktop/Farey-Local/experiments/l_function_deep_test.py`

---

## Action Items

1. **Run residualized frequency scan with p to 200K** to confirm chi7 zero is the dominant peak after T_plain removal.
2. **Implement proper permutation null** for all future phase-lock tests.
3. **Update L_FUNCTION_DEEP_EXPLORATION.md** section on control failures with this explanation.
4. **Consider whether the -0.62 anticorrelation has its own theoretical explanation** — why should T_chi7 and T_plain be negatively correlated? This likely follows from the identity relating their generating functions (both involve 1/L(s,*) factors, and the Euler product coupling creates arithmetic correlations).
