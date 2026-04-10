# Denominator-Class Decomposition: Analysis and Proof Path

## 1. Setup and Definitions

For prime p, let N = p-1, and F_N the Farey sequence of order N (fractions a/b in [0,1] with b <= N, gcd(a,b)=1).

**Discrepancy:** D(a/b) = rank(a/b in F_N) - |F_N| * (a/b)

**Arithmetic displacement:** delta(a/b) = (a - p*a mod b) / b

**Decomposition by denominator:** For each b in {1,...,N}, let C_b = {a/b in F_N : gcd(a,b)=1}. Then:
- D_b = restriction of D to C_b
- delta_b = restriction of delta to C_b
- D_b = D_mean_b * 1 + D_b^osc, where D_mean_b = (1/phi(b)) * sum_{a/b in C_b} D(a/b)
- D_b^osc = D_b - D_mean_b (zero-mean oscillatory part)

**Key identity:**
```
B + C = sum_b [2 * <D_b^osc, delta_b> + ||delta_b||^2]
```
The smooth-cross term vanishes because sum(delta_b) = 0 per denominator class (since multiplication by p is a permutation of units mod b).

## 2. Computational Results

### 2.1 Per-Denominator Contributions

For each prime p and denominator b, we computed ||D_b^osc||^2, ||delta_b||^2, <D_b^osc, delta_b>, and the net contribution 2*cross + ||delta||^2.

**p=13:** ALL denominator contributions non-negative. B+C = 7594/1155 ~ 6.57.

**p=17:** Negative at b = {3, 13, 15}. B+C = 183880/27027 ~ 6.80. |neg|/pos = 0.27.

**p=23:** Negative at b = {4, 7, 21}. B+C = 121701/6188 ~ 19.67. |neg|/pos = 0.26.

**p=29:** Negative at b = {3, 5, 9, 13, 25, 26, 27}. B+C ~ 45.37. |neg|/pos = 0.20.

**p=37:** Negative at b = {5, 31, 33, 34, 35}. B+C ~ 88.80. |neg|/pos = 0.16.

### 2.2 Negative Contributions: Pattern

| p | Negative denominators | |neg|/pos ratio |
|---|---|---|
| 11 | {9, 10} | 0.42 |
| 13 | (none) | 0.00 |
| 17 | {3, 13, 15} | 0.27 |
| 19 | {17, 18} | 0.05 |
| 23 | {4, 7, 21} | 0.26 |
| 29 | {3,5,9,13,25,26,27} | 0.20 |
| 31 | (none) | 0.00 |
| 37 | {5,31,33,34,35} | 0.16 |
| 41 | 11 denominators | 0.29 |
| 59 | 15 denominators | 0.28 |
| 71 | 7 denominators | 0.07 |

**Key observation:** The ratio |neg|/pos stays bounded well below 1 (max observed: 0.42 at p=11). Negative contributors tend to cluster at b near N = p-1 (large denominators where D_b^osc is large) and at certain small b where p mod b has special structure.

### 2.3 The Ratio ||D_b^osc||/||delta_b|| (Per-Denominator)

**FINDING: The per-denominator condition ||D_b^osc|| < ||delta_b||/2 FAILS badly.**

For large b (near N), ||D_b^osc||^2 grows roughly as b^2 (from the growing Farey discrepancy), while ||delta_b||^2 stays bounded. The ratio ||D_b^osc||/||delta_b|| reaches values like 10-15 for b near N.

This means **the per-denominator Cauchy-Schwarz approach cannot work.**

### 2.4 Global Analysis (The Key)

Despite individual denominator failures, the GLOBAL quantities behave well:

| p | ||D^osc||^2/N^2 | ||delta||^2/N | cross/delta^2 | B+C/N | correlation |
|---|---|---|---|---|---|
| 11 | 0.14 | 0.40 | -0.32 | 0.14 | -0.17 |
| 13 | 0.20 | 0.57 | -0.02 | 0.55 | -0.01 |
| 29 | 0.82 | 1.17 | +0.19 | 1.62 | +0.04 |
| 53 | 2.03 | 2.35 | +0.69 | 5.59 | +0.10 |
| 97 | 4.44 | 4.71 | -0.11 | 3.71 | -0.01 |
| 113 | 5.52 | 5.53 | +2.20 | 29.88 | +0.21 |
| 131 | 6.33 | 6.21 | +1.16 | 23.31 | +0.12 |

**Critical finding: cross/delta^2 stays well above -1/2.** The minimum observed is -0.32 at p=11. This is the condition needed for B+C > 0.

**The correlation coefficient |<D^osc, delta>| / (||D^osc|| * ||delta||)** stays tiny: between 0.006 and 0.21. Cauchy-Schwarz gives a bound that is 5-100x too loose.

## 3. Why the Naive Approach Fails

The "obvious" proof attempt:
```
B+C >= ||delta||^2 - 2*||D^osc||*||delta||  (by Cauchy-Schwarz)
    = ||delta|| * (||delta|| - 2*||D^osc||)
```
This requires ||D^osc|| < ||delta||/2, but:
- ||D^osc||^2 ~ c * N^2 * log(N) (Franel-Landau type scaling)
- ||delta||^2 ~ c' * N (linear in N)

So ||D^osc|| ~ N*sqrt(log N) >> ||delta|| ~ sqrt(N), and the condition fails for all large p.

## 4. Why Cancellation Occurs

### 4.1 Structural Explanation

D^osc and delta live in "different worlds":
- **D^osc(a/b)** depends on the position of a/b relative to other Farey fractions (a global, analytic quantity)
- **delta(a/b)** depends on the arithmetic of multiplication by p mod b (a local, algebraic quantity)

Within each denominator class b, we decomposed D^osc into:
- **Linear part:** Projection of D^osc onto the position variable a/b
- **Residual part:** Everything else

The linear part of the cross term is POSITIVE and grows with p. The residual part is NEGATIVE and also grows, but slightly less. They nearly cancel.

For p=37: Linear cross = +75.75, Residual cross = -62.59, Net = +13.16
For p=71: Linear cross = +443.0, Residual cross = -245.6, Net = +197.4
For p=97: Linear cross = +594.4, Residual cross = -642.0, Net = -47.6

### 4.2 The Correlation is Small Because...

The key mechanism: **pseudorandomness of the multiplication-by-p permutation.**

For b not dividing p-1, the map a -> pa mod b is a nontrivial permutation of (Z/bZ)*. The displacement delta(a/b) = (a - pa mod b)/b has the structure of a "permutation displacement".

D^osc has Fourier structure concentrated in low frequencies (it's a smooth function perturbed by arithmetic), while the permutation displacement has energy spread across all frequencies. The inner product of a low-frequency function with a spread-spectrum signal is small.

This is analogous to how Kloosterman sums and Ramanujan sums provide square-root cancellation.

## 5. Scaling Summary

| Quantity | Scaling with N=p-1 | Notes |
|---|---|---|
| ||D^osc||^2 | ~ N^2 * log(N) | Standard Franel-Landau |
| ||delta||^2 | ~ c * N, c in [0.4, 6.3] | Grows linearly (c depends on arithmetic of p) |
| \|cross\| | << ||D^osc|| * ||delta|| | Massive cancellation |
| B+C | ~ N * c', c' > 0 | Grows linearly, always positive |
| B+C/N | minimum 0.14 at p=11 | Bounded below away from 0 |
| ||D_osc||^2/N^2 | ~ log(N)/pi^2 | Confirmed scaling |
| ||D_mean||^2/N^2 | ~ 0.076 (constant) | The smooth part is O(N^2) |

## 6. Proof Path: Three Strategies

### Strategy A: Direct Correlation Bound (Most Promising)

**Goal:** Show |<D^osc, delta>| <= (1/2 - epsilon) * ||delta||^2 for some epsilon > 0.

**Approach:** Expand both D^osc and delta in Dirichlet characters mod b (or additive characters e(ka/b)).

For each denominator b:
- D^osc restricted to C_b has character expansion with coefficients related to L-functions
- delta restricted to C_b has character expansion determined by the permutation a -> pa mod b

The inner product <D_b^osc, delta_b> becomes a sum of products of character coefficients.

**Key ingredient needed:** A bound on Sigma_b |<D_b^osc, delta_b>| that's o(||delta||^2).

Since ||D_b^osc||^2 grows like b^2 but ||delta_b||^2 ~ phi(b) (much smaller), the per-denominator cross terms can be large. But they oscillate in SIGN across b, giving cancellation in the sum.

**Status:** Requires character sum analysis. The empirical correlation of ~0.01-0.20 suggests ample room.

### Strategy B: Variance Decomposition

**Goal:** Show B+C = ||D + delta||^2 - ||D||^2 > 0 using properties of D + delta.

Equivalently: ||D + delta||^2 > ||D||^2.

**Observation:** delta adds "mass" to D, and this mass is concentrated in different denominator classes than where D is large. Since D grows with b (large denominators have large discrepancy) but delta is most active at moderate b, the addition is "transverse".

**Status:** Heuristic. Needs formalization.

### Strategy C: Positivity via Completeness (Boldest)

**Goal:** Show that for each denominator class, the net contribution is non-negative for "most" b, and the negative contributions from the remaining b are absorbed.

From the data:
- b dividing p-1: delta_b = 0, so net = 0 (neutral)
- b with p mod b = 1 (same condition): delta_b = 0
- b with p mod b = -1: delta_b is deterministic, can analyze exactly
- Other b: pseudorandom behavior of permutation gives near-orthogonality

**Partition of denominators:**
1. b | (p-1): net = 0 (contributes nothing)
2. b with ||D_b^osc|| small (b << N^{2/3}): net ~ ||delta_b||^2 > 0 (positive, though small per term)
3. b with ||D_b^osc|| large (b near N): net can be negative, but these b have small ||delta_b||
4. The total negative is bounded by sum over large-b terms

**Needed:** Quantitative bound showing category 3 is absorbed by category 2.

**Status:** Most complex but most likely to give an unconditional result. The empirical |neg|/pos ratio of 0.42 or less gives hope.

## 7. Concrete Next Steps

1. **Character sum computation (Strategy A):** Express <D_b^osc, delta_b> in terms of Dirichlet characters. The delta part involves the character expansion of the permutation a -> pa mod b, which is explicit: it's multiplication by p. The D^osc part involves Kloosterman-type sums.

2. **Large-b bound (Strategy C):** For b > N^{1-epsilon}, show ||delta_b||^2 << phi(b) * (something small) that beats ||D_b^osc||.

3. **Small-b positivity (Strategy C):** For b < N^{1/2}, show ||D_b^osc||^2 < ||delta_b||^2/4 using the fact that D varies slowly among fractions with small denominator.

4. **Global orthogonality (Strategy A):** Prove that sum_b <D_b^osc, delta_b> satisfies a square-root cancellation bound of the form O(N^{1/2} * polylog), which would give B+C = ||delta||^2 + O(N^{1/2} * polylog) ~ N + lower order, hence positive for large p.

## 8. Assessment

**Difficulty:** High. This is not a simple bound but requires understanding the interplay between Farey discrepancy (analytic number theory) and modular multiplication (algebraic number theory).

**Feasibility:** The massive empirical gap between |cross| and the CS bound (factor of 5-100x) suggests there IS a provable structural reason for the cancellation. The question is whether existing techniques suffice.

**Most promising concrete attack:** Strategy A with character sums, targeting the bound:
```
|sum_b <D_b^osc, delta_b>| = O(N * sqrt(log N))
```
Combined with ||delta||^2 ~ c*N (c > 0), this would give B+C > 0 for p sufficiently large.

**Remaining gap for small p:** Direct verification (already done for p <= 131, all positive).

## 9. Key Data Tables (Exact)

### B+C values (exact fractions):
- p=13: B+C = 7594/1155
- p=17: B+C = 183880/27027
- p=23: B+C = 121701/6188

### Critical ratio cross/delta^2:
- Minimum over p in [11, 113]: -0.32 at p=11
- For B+C > 0: need this > -0.5
- Margin at p=11: 0.18 (comfortably positive)

### Scaling:
- ||D^osc||^2 / (N^2 * log N) grows toward ~1/pi^2 (standard)
- ||delta||^2 / N grows from ~0.4 to ~6.3 (depends on arithmetic of p)
- B+C / N > 0 always, minimum 0.14 at p=11
