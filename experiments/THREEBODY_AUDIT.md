# CRITICAL AUDIT: Three-Body Orbit -> Stern-Brocot Mapping Results

**Date**: 2026-03-27
**Auditor**: Claude (adversarial review mode)
**Files reviewed**: `THREEBODY_FULL_RESULTS.md`, `threebody_full_test.py`, `threebody_full_data.json`

---

## EXECUTIVE SUMMARY

The core mathematical pipeline (word -> matrix -> fixed point -> CF) is correctly implemented for orbits where the CF period is successfully detected. The figure-eight -> golden ratio result is an exact algebraic identity, not a numerical coincidence. The correlations between CF properties and orbital properties are real and survive permutation testing.

**However, the analysis has several serious methodological flaws that undermine the reported numbers, and the novelty claims are substantially overstated.** The findings are not wrong, but they are less impressive than presented.

**Overall verdict: PARTIALLY VALID. Solid kernel of truth wrapped in overstatement.**

---

## 1. MATRIX MAPPING CORRECTNESS

### Generators: CORRECT

- `a = [[1,2],[0,1]]` and `b = [[1,0],[2,1]]` are valid generators of Gamma(2).
- Both satisfy the Gamma(2) membership conditions (a,d odd; b,c even; det=1).
- Gamma(2) is free on these two generators (classical result).
- Inverses `A = [[1,-2],[0,1]]`, `B = [[1,0],[-2,1]]` are correctly computed.

### Figure-eight word BabA: CORRECT

Hand computation verified:
```
B*a*b*A = [[5, -8], [-8, 13]]
Trace = 18, Det = 1
```
Fixed point equation: -8z^2 + 8z + 8 = 0, simplifies to z^2 - z - 1 = 0.
Roots: phi and -1/phi. Attracting FP = -1/phi. |FP| = 1/phi EXACTLY.

### Word parsing: CORRECT

Uppercase = inverse convention is consistently applied. Left-to-right multiplication matches the standard convention for composing group elements along a path.

### ISSUE: Word-to-orbit assignment comes from external catalog

The mapping from orbit ID to free-group word comes from the Li & Liao catalog (sjtu-liao/three-body). We trust this catalog but have not independently verified the word assignments. If any word assignments are wrong, all downstream analysis for those orbits is corrupted.

---

## 2. FIXED POINT COMPUTATION

### Formula: CORRECT

For Mobius transform z -> (az+b)/(cz+d), fixed points satisfy cz^2 + (d-a)z - b = 0, giving z = (a-d +/- sqrt((d-a)^2 + 4bc)) / (2c). This matches the script.

### Attracting FP selection: CORRECT

The script selects the root with larger |cz+d|, corresponding to |f'(z)| = 1/|cz+d|^2 < 1. This is the correct criterion for the attracting fixed point.

### c=0 case: NOT AN ISSUE

All 695 orbits are hyperbolic (|trace| > 2) with c != 0. No parabolic or elliptic cases exist in the catalog.

### All FPs are negative: NOTED

All 695 attracting fixed points lie in (-1, 0). The script takes abs() before computing the CF. Since ALL are negative, this is a consistent convention, but it loses sign information. Since the Stern-Brocot tree only covers positive reals, this is an unavoidable choice, but it should be explicitly acknowledged.

---

## 3. CONTINUED FRACTION COMPUTATION: **SERIOUS FLAW**

### The Problem: Floating-Point CF Degradation

The script computes CFs using `math.sqrt(float(D))` and standard float64 arithmetic. For orbits with large discriminants (D ~ 10^84 for long words), the fixed point has only ~15 significant digits. After ~20 CF steps, accumulated floating-point error produces **spurious large partial quotients** that are pure numerical artifacts.

**Evidence**: Orbit I.A-101 has a clear pattern [0; 1,1,1,2,1,1,1,2,...] for the first ~20 terms, then degrades to produce partial quotients as large as 1427. The true CF (being a quadratic irrational) is eventually periodic with a short period, but the float64 computation cannot detect this.

### Impact: 123 Orbits (17.7%) Have Corrupted CF Data

- 123 orbits have `cf_period_length = 0` (period detection failed).
- These orbits have mean nobility = 0.482, vs 0.766 for detected orbits.
- The low nobility is an ARTIFACT of corrupted CF tails diluting the fraction of 1s.
- These corrupted values systematically bias the full-catalog correlations downward.

### Verification: Detected-Only Correlations Are Much Stronger

| Metric | All 695 | Detected 572 only |
|--------|---------|-------------------|
| Partial nobility vs stability | -0.538 | -0.876 |
| Partial nobility vs period | -0.600 | -0.946 |
| Lyapunov proxy vs nobility | -0.563 | -0.957 |

The corrupted orbits are adding noise, not signal. The correlations would be stronger with correct CF computation.

### Fix Required

Use exact quadratic surd arithmetic for CF computation. Since all fixed points are quadratic irrationals, their CFs can be computed exactly using the standard algorithm that tracks (P + sqrt(D))/Q with integer P, D, Q. This would eliminate all floating-point issues.

---

## 4. NOBILITY DEFINITION: **AD HOC AND NON-STANDARD**

### What the script computes

`nobility = fraction of partial quotients in the CF period (or truncated CF) that equal 1`

This is a continuous relaxation of the standard noble number definition. A **noble number** in the mathematical literature has CF that is eventually ALL 1s. The script's "nobility" allows arbitrary non-1 terms and just counts the fraction of 1s.

### This is not standard terminology

No published paper uses "nobility" as a continuous measure in this way. The standard measures in KAM theory are:
- Irrationality measure / Diophantine exponent
- Brjuno sum
- Whether the frequency ratio is a noble number (binary: yes/no)

### Nobility is redundant with CF geometric mean

Spearman correlation between nobility and geometric mean: rho = -0.994. They carry essentially the same information. The geometric mean is a more standard and interpretable quantity.

### This matters for novelty claims

Using a non-standard measure and calling it "nobility" gives a false impression of connection to the KAM nobility concept. The actual measure is just "what fraction of CF partial quotients are 1."

---

## 5. STATISTICAL CONCERNS

### Partial correlations: CORRECTLY IMPLEMENTED

The script residualizes both X and Y against word length using OLS, then computes Spearman rho on the residuals. This is a valid approach to computing partial rank correlations.

### Permutation test: CORRECTLY IMPLEMENTED

The permutation shuffles nobilities (breaking the word-to-physics mapping) while keeping word lengths fixed, and re-residualizes each permutation. This correctly tests whether the word-specific CF information (beyond word length) correlates with physical properties.

### "14-16 sigma" z-scores: MISLEADING

These z-scores are computed as (observed_rho - null_mean) / null_std. While the permutation test is valid, reporting z-scores this way implies Gaussian statistics. The actual permutation p-value is the floor of the test: p = 1/10001 ~ 0.0001. The honest statement is "p < 0.0001" not "14 sigma."

### Confound: Orbit family

The Kruskal-Wallis test shows families differ in nobility (H=16.36, p=0.0026). However, within-family correlations are still strong (rho ~ -0.85 for I.A, I.B, II.C), so family membership does not explain the nobility-stability relationship. This is a positive result.

### Lyapunov proxy: MISLEADING NAME

`log_trace / word_length` is the braid entropy, not the dynamical Lyapunov exponent. The correlation between word length and log(trace) is rho = 0.998, so the "Lyapunov proxy" has coefficient of variation of only 3.9%. Calling this a "Lyapunov proxy" overstates the physical content. It is the deviation of log(trace) from its word-length expectation.

### Prediction AUC: MODEST

- Random baseline: AUC = 0.500
- Word length only: AUC = 0.741
- Nobility only: AUC = 0.853
- Nobility improvement over word length: +0.112

The AUC of 0.853 sounds impressive, but the "stability" being predicted is itself defined from the braid matrix trace (log_trace / word_length), not from actual numerical integration of orbit stability. So the prediction is: CF properties of a matrix predict the trace of that matrix. This is much less surprising than predicting actual dynamical stability.

---

## 6. GAP PREDICTIONS: **ESSENTIALLY MEANINGLESS**

The 354 "gap predictions" are produced by:
1. Sorting orbits by |fixed point|
2. Finding gaps between adjacent FP values
3. Linearly interpolating initial conditions

**Problems**:
- There is no physical reason adjacent FP values should correspond to adjacent orbits.
- The largest "gap" spans 58% of the entire FP range -- it is just two orbits that happen to be far apart in FP space.
- Linear interpolation of (v1, v2, T) in the three-body problem has no theoretical basis.
- These cannot be called "predictions" unless someone integrates the proposed initial conditions and finds periodic orbits there.
- The Stern-Brocot tree is dense in the positive reals, so there are always "gaps" to fill. This is a tautology, not a prediction.

---

## 7. NOVELTY ASSESSMENT: **SUBSTANTIALLY OVERSTATED**

### What is actually new

The specific computation of CF properties of Gamma(2) fixed points for the Li & Liao catalog of 695 three-body orbits, and the correlation of these properties with catalog parameters (T*, trace).

### What is NOT new

1. **Gamma(2) ~ F_2 ~ braid topology of three-body orbits**: This is classical (Moore 1993, Montgomery 1998). The identification of three-body braids with free group elements in Gamma(2) is well established.

2. **Noble numbers are stable in KAM theory**: This dates to the 1960s-70s (Kolmogorov, Arnold, Moser). The idea that tori with noble frequency ratios are the last to break is standard textbook material.

3. **Kin, Nakamura, Ogawa (2021) already did the key work**: Their paper "Lissajous 3-braids" explicitly:
   - Classifies 3-braids via the Stern-Brocot tree
   - Computes pseudo-Anosov dilatations (= eigenvalues of the braid matrix)
   - Shows dilatation increases as the slope descends in the Stern-Brocot tree
   - Discusses continued fractions of quadratic surds for these braids
   - Studies the Farey tessellation cutting sequences

   This is essentially the same framework applied to Lissajous orbits rather than Li-Liao orbits.

4. **The figure-eight -> golden ratio connection**: While presented as a discovery, this follows immediately from the matrix [[5,-8],[-8,13]] having characteristic polynomial z^2 - z - 1 = 0. Anyone who writes down the matrix for the simplest braid word would find this.

### What a referee would say

- **Dynamical systems referee**: "The correlation between CF properties and braid entropy is expected from KAM theory. The Gamma(2) representation is standard. What new dynamical insight does this provide beyond 'numbers that are hard to approximate by rationals correspond to more stable orbits'?"

- **Number theory referee**: "The mapping from free group words to Gamma(2) matrices to fixed points is the standard correspondence. The 'nobility' measure is non-standard and redundant with the geometric mean of partial quotients. What is the number-theoretic contribution?"

- **Astrophysics referee**: "The 'stability' measure is defined from the braid matrix trace, not from actual orbital integration. Are these orbits actually more stable in the dynamical sense? Without numerical integration, the predictive claims are untestable."

---

## 8. OVERSTATEMENT INVENTORY

| Claim | Assessment |
|-------|------------|
| "14-16 sigma" significance | MISLEADING. Permutation p < 0.0001 is all that can be said. |
| "Figure-eight = golden ratio" | CORRECT but trivial. It follows from a 2-line algebra computation. |
| "354 gap predictions" | MEANINGLESS. Linear interpolation in FP space is not a physical prediction. |
| "AUC = 0.853" | INFLATED. Predicting braid entropy from CF properties of the same matrix is near-tautological. |
| "Genuine physical structure not visible from topology alone" | PARTIALLY TRUE. CF properties do add information beyond word length, but the "physical structure" claim requires actual dynamical integration to validate. |
| "Nobility adds blind-predictive value" | TRUE but modest (+0.112 AUC) and the "stability" label is misleading. |
| N=695 catalog "full validation" | COMPROMISED. 123 orbits (17.7%) have corrupted CF data from floating-point errors. |

---

## 9. WHAT SURVIVES SCRUTINY

1. **Figure-eight = 1/phi**: Exact algebraic identity. Survives completely.

2. **CF properties correlate with braid entropy beyond word length**: On the 572 orbits with correct CF computation, the partial correlations are very strong (rho ~ -0.88 to -0.95). This is real.

3. **The mapping from three-body braid words to CF properties via Gamma(2) is computationally tractable**: The pipeline works and could be applied to newly discovered orbits.

4. **Permutation tests confirm the correlations are not an artifact of word length**: The methodology is sound.

---

## 10. RECOMMENDATIONS

### Must fix before publication

1. **Replace float64 CF computation with exact quadratic surd arithmetic.** This eliminates the 123 corrupted orbits and produces correct period detection for all 695 orbits.

2. **Drop or heavily qualify the "gap predictions" section.** These are not predictions. At best they are "numerically motivated suggestions for future numerical integration."

3. **Rename "nobility" to something like "CF-ones-fraction" or use the standard geometric mean.** The current name falsely implies connection to KAM noble numbers.

4. **Replace "Lyapunov proxy" with "braid entropy" or "normalized log-trace".** The current name falsely implies connection to the dynamical Lyapunov exponent.

5. **Acknowledge Kin-Nakamura-Ogawa (2021) as strong prior art.** Their framework is essentially the same, applied to a different orbit family.

### Should fix

6. Report permutation p-values, not z-scores. "p < 0.0001" is honest; "14 sigma" is misleading.

7. Validate "stability" claims with actual numerical orbit integration, not just braid entropy.

8. Discuss the non-standard "nobility" definition explicitly and compare with standard Diophantine measures.

### Nice to have

9. Include within-family correlations to demonstrate the result is not a family-clustering artifact (they are strong and support the finding).

10. Repeat the prediction experiment using only detected orbits with correct CF computation.

---

## FINAL ASSESSMENT

**The work contains a real signal: CF properties of the Gamma(2) braid matrix encode information about orbital complexity beyond what word length alone provides.** This is demonstrated by the strong partial correlations on the 572 correctly-computed orbits and confirmed by permutation testing.

**However, the presentation substantially overstates the novelty and significance:**
- The Gamma(2)-to-CF mapping is a straightforward application of classical number theory.
- The KAM connection (noble = stable) is decades old.
- Kin-Nakamura-Ogawa (2021) already built the key bridge between braids, Stern-Brocot, and three-body orbits.
- 17.7% of the data is corrupted by floating-point errors.
- The "stability" being predicted is a braid-theoretic quantity, not a dynamical one.
- The gap predictions are not scientifically meaningful.

**If the float issue is fixed and the claims are appropriately qualified, this could be a useful computational contribution showing the CF-stability correlation on the full Li-Liao catalog. It is NOT a fundamental discovery.**
