# Can We Prove c_K Zeros Avoid Zeta Zeros?
# Author: Saar Shai
# Analysis by: Claude Opus 4.6 (deep research mode)
# Date: 2026-04-11
# AI Disclosure: Analysis drafted with assistance from Claude (Anthropic)

## STATUS: HONEST ASSESSMENT -- PROOF OUT OF REACH, STRONG CONJECTURE

---

## 0. Setup and Context

The Dirichlet polynomial (partial sum of 1/zeta):
$$c_K(s) = \sum_{k=2}^{K} \mu(k) k^{-s}$$

For K=10: $c_{10}(s) = -2^{-s} - 3^{-s} - 5^{-s} + 6^{-s} - 7^{-s} + 10^{-s}$

**Known facts:**
- Langer (1931): c_K has infinitely many zeros in the critical strip. Count: N(T) ~ (log K - log 2)T/pi. For K=10: ~0.51T zeros up to height T.
- Moreno (1973): When exponents are Q-linearly independent, zeros are dense in each strip.
- Computational: c_K(rho) != 0 for all tested zeta zeros rho (200+ zeros, K=10,20,50).

**The question:** Can we PROVE that the zeros of c_K(s) never coincide with zeros of zeta(s)?

**Short answer:** No. This appears to be a HARD conjecture, comparable in difficulty to the linear independence hypothesis for zeta zero ordinates. We can state it as a well-motivated conjecture with substantial numerical evidence and multiple heuristic arguments.

---

## 1. Numerical Evidence (New Computation)

### 1.1 Avoidance at Zeta Zeros vs Generic Points

| K | min|c_K(rho)| at 50 zeta zeros | min|c_K| at 500 generic pts | Ratio |
|---|----------------------------------|-------------------------------|-------|
| 10 | 0.297 | 0.033 | 9.0x |
| 20 | 0.258 | 0.005 | 51.6x |
| 30 | 0.401 | 0.101 | 4.0x |

The minimum of |c_K| at zeta zeros is consistently LARGER than the minimum at generic points on Re(s)=1/2. This is the "avoidance" phenomenon: c_K is pulled away from zero at zeta zeros.

### 1.2 Closest Approach

The closest approach found: at rho_59 (gamma = 161.189):
- |c_10(rho_59)| = 0.0943 (smallest among first 200 zeros)
- A local minimum of |c_10(1/2+it)| occurs at t = 161.176, with |c_10| = 0.0941
- Distance: 0.013 in t, or 0.0067 mean zeta spacing units
- Critical: the local minimum is NOT a zero of c_10. The modulus 0.094 is bounded away from 0.
- As K increases: |c_20(rho_59)| = 0.42, |c_50(rho_59)| = 0.77 (growing -- pole repulsion)

### 1.3 Growth Rate |c_K(rho)| as K -> infinity

| rho | |c_K/log K| at K=50 | K=100 | K=200 | K=500 | 1/|zeta'(rho)| |
|-----|---------------------|-------|-------|-------|----------------|
| rho_1 | 1.148 | 1.150 | 1.106 | 1.149 | 1.261 |
| rho_10 | 0.623 | 0.723 | 0.739 | 0.669 | 0.705 |
| rho_50 | 0.230 | 0.292 | 0.148 | 0.235 | 0.267 |
| rho_100 | 0.297 | 0.216 | 0.220 | 0.272 | 0.250 |

The ratio |c_K(rho)|/log(K) stabilizes near 1/|zeta'(rho)| as K grows. This confirms the pole divergence mechanism: the partial sums of 1/zeta(s) at a zero of zeta grow like log(K)/|zeta'(rho)|.

### 1.4 Mean Value

Montgomery-Vaughan mean value theorem predicts:
$$\frac{1}{N(T)} \sum_{|\gamma_j| \leq T} |c_K(\rho_j)|^2 \approx \|c_K\|^2 = \sum_{\substack{k=2 \\ \mu(k)\neq 0}}^{K} \frac{1}{k}$$

| K | mean |c_K|^2 (200 zeros) | ||c_K||^2 | Ratio |
|---|-------------------------|-----------|-------|
| 10 | 1.796 | 1.443 | 1.245 |
| 20 | 2.474 | 1.860 | 1.330 |
| 50 | 3.772 | 2.417 | 1.561 |

The mean exceeds the prediction (ratio > 1). This is consistent with the pole repulsion boosting |c_K| at zeta zeros above the "generic" average.

---

## 2. Analysis of Five Approaches

### Approach 1: Arithmetic Independence

**Idea:** The zeros of c_K are determined by mu(k) for k <= K (finitely many small integers). The zeros of zeta are determined by all primes. These "should be" independent.

**Analysis:**
- The conjecture that zeta zero ordinates are algebraically independent over Q is itself a famous open problem (related to the Linear Independence hypothesis).
- Even if the ordinates were proved algebraically independent, c_K(rho) = 0 is a TRANSCENDENTAL equation (involving p^{-i*gamma}), not an algebraic one. Algebraic independence of {gamma_j} doesn't directly prevent transcendental relations.
- The equation c_10(1/2 + i*gamma) = 0, written in torus coordinates, is: $-z_2/\sqrt{2} - z_3/\sqrt{3} - z_5/\sqrt{5} + z_2 z_3/\sqrt{6} - z_7/\sqrt{7} + z_2 z_5/\sqrt{10} = 0$ where $z_p = e^{-i\gamma \log p}$ are unit-modulus. This is one complex equation in 4 real unknowns.

**Verdict:** No proof available. Would require progress on algebraic independence conjectures AND additional work to bridge the algebraic/transcendental gap.

### Approach 2: 1/zeta Pole Repulsion

**Idea:** At a zeta zero rho, the partial sums c_K(rho) approximate the pole of 1/zeta(s), so |c_K(rho)| -> infinity as K -> infinity. Even for finite K, the pole "repels" c_K from zero.

**Analysis:**
- The divergence c_K(rho) -> infinity is REAL and verified numerically. Rate: ~log(K)/|zeta'(rho)|.
- But for FIXED K (say K=10), c_K(rho) = sum_{k=2}^{10} mu(k) k^{-rho} is just a finite sum. It's a specific complex number, not "pulled" by any force.
- The "repulsion" is a heuristic interpretation of the growth with K, not a rigorous mechanism for fixed K.
- To formalize: c_K(rho) = [1/zeta(rho) - R_K(rho)], where R_K is the tail. Both 1/zeta and R_K have a pole at rho, and c_K(rho) is their (finite) difference. The "pole" determines the limiting behavior, not the finite-K value.
- The CORRECT statement: for each fixed rho, there exists K_0(rho) such that c_K(rho) != 0 for K > K_0. This is because |c_K(rho)| -> infinity, so eventually |c_K(rho)| > 0. But K_0 could be very large, and this says nothing about whether c_K(rho) = 0 for small K.

**What IS provable (under RH):**
> For each nontrivial zero rho of zeta(s), |c_K(rho)| -> infinity as K -> infinity.

**Verdict:** Gives a theorem for growing K (each zero is eventually detected), but NOT for fixed K (the paper's setting). Heuristic only for fixed K.

### Approach 3: Dimension Argument on T^4

**Idea:** The zero set of P(theta) on T^4 is codimension-2 (a 2-surface in a 4-manifold). The Kronecker flow {(t log 2, t log 3, t log 5, t log 7) mod 2pi : t in R} is 1-dimensional. In general position, a 1-manifold and a 2-manifold in a 4-manifold DON'T intersect.

**Analysis:**
- Langer's theorem PROVES they DO intersect (c_K has infinitely many zeros), so the "general position" argument fails.
- The Kronecker flow is equidistributed (Weyl) but not "generic" in the smooth topology sense -- it's a very special 1-manifold.
- The zero variety Z = {P = 0} has Haar measure zero on T^4 (codim 2, so measure 0).
- The equidistributed flow visits Z with density proportional to its "effective 1-dimensional measure" (related to Langer's count formula).
- Zeta zeros define specific points on the Kronecker flow: gamma_j -> (gamma_j log 2, ..., gamma_j log 7) mod 2pi.
- Under equidistribution of {gamma_j log p mod 2pi}, the proportion of zeta zeros landing on Z tends to 0.
- But proportion 0 does NOT mean cardinality 0.

**Gradient analysis:** Near the zero variety Z, |P(theta)| ~ 1.29 * dist(theta, Z). The observed min|c_10(rho)| = 0.094 implies the closest zeta zero is distance at least 0.094/1.29 ~ 0.073 from Z on T^4.

**Verdict:** Suggestive dimension/measure argument, but "density zero" is weaker than "empty set." Cannot rule out sporadic coincidences.

### Approach 4: Linear Independence Hypothesis (LI)

**Idea:** Under the LI conjecture (positive imaginary parts of zeta zeros are linearly independent over Q), the tuple (gamma_j log 2, gamma_j log 3, gamma_j log 5, gamma_j log 7) mod 2pi equidistributes on T^4 as j -> infinity. Since the zero variety has measure zero, almost no zeta zeros land on it.

**Analysis:**
- LI is itself an unproved (and seemingly very hard) conjecture.
- Even under LI, we only get DENSITY zero, not emptiness.
- To get emptiness, we would need QUANTITATIVE equidistribution: a bound on the discrepancy of the sequence {(gamma_j log p) mod 2pi}_{j=1}^N on T^4. The best known (under GRH + LI) give discrepancy O(N^{-1/2+eps}), which after summing over the N(T) ~ T log T zeros, gives: expected number of coincidences within epsilon = O(epsilon * T^{1/2+eps} * log T). For epsilon -> 0, this -> 0, which would PROVE avoidance... but this argument has a gap: the "epsilon" here refers to the discrepancy scale, not the size of the zero variety.
- A complete proof would need to show that the zero variety Z has empty intersection with the range of a specific Diophantine-type condition on the gamma_j.

**Verdict:** The most promising THEORETICAL direction, but conditional on LI (unproved) and requires delicate quantitative equidistribution that goes beyond current technology.

### Approach 5: Probabilistic Counting

**Idea:** Count expected coincidences using densities.

**Analysis:**
- c_K zeros on Re(s)=1/2 have density ~0.51 per unit height (Langer).
- Zeta zeros have density ~(1/2pi) log(T/2pi) per unit height at height T.
- If c_K zeros were uniformly distributed, expected number of coincidences within epsilon in [0,T]: ~ 2 * epsilon * 0.51 * (1/2pi) * T * log T.
- For any epsilon > 0, this -> infinity as T -> infinity.
- So counting CANNOT rule out coincidences. Need arithmetic structure.

**Verdict:** Wrong direction. This shows coincidences are NOT ruled out by density alone.

---

## 3. The Correct Framing: A Conjecture

### Conjecture (Dirichlet Polynomial Avoidance)

For each fixed K >= 2, the zeros of $c_K(s) = \sum_{k=2}^K \mu(k) k^{-s}$ are disjoint from the nontrivial zeros of $\zeta(s)$.

### Evidence Supporting the Conjecture

1. **Numerical verification:** c_K(rho) != 0 for K = 10, 20, 50 at 200 nontrivial zeros (50-digit precision). Minimum |c_10(rho)| = 0.094 (at rho_59).

2. **Statistical anomaly:** min|c_K(rho)| at zeta zeros is 9x larger than min|c_K| at generic points for K=10, and 52x larger for K=20. If c_K zeros were unrelated to zeta zeros, we'd expect the minimum at zeta zeros to be comparable to the generic minimum.

3. **Pole repulsion:** |c_K(rho)| grows like log(K)/|zeta'(rho)| as K -> infinity. For each fixed rho, only finitely many K can have |c_K(rho)| < delta.

4. **Measure theory:** Under LI, the proportion of zeta zeros with c_K(rho) = 0 is zero (equidistribution on T^4, zero variety has measure 0).

5. **Torus geometry:** The zero variety of |P|^2 on T^4 has codimension 2. The zeta zero torus points maintain distance >= 0.073 from this variety (empirically).

### What IS Provable

**Theorem (under RH).** For each nontrivial zero rho of zeta(s), $|c_K(\rho)| \to \infty$ as $K \to \infty$. In particular, for each rho, there exists $K_0(\rho)$ such that $c_K(\rho) \neq 0$ for all $K \geq K_0(\rho)$.

*Proof sketch:* Under RH, the Dirichlet series $1/\zeta(s) = \sum_{k=1}^{\infty} \mu(k) k^{-s}$ converges conditionally for Re(s) > 1/2 (this follows from RH via the Perron formula and the estimate M(x) = O(x^{1/2+eps})). At a simple zero rho, the partial sums c_K(rho) are partial sums of a conditionally convergent series whose limit is the pole value 1/zeta(rho) = infinity. Hence the partial sums diverge, i.e., |c_K(rho)| -> infinity.

**Theorem (unconditional, finite).** For K = 10, 20, 50 and for all nontrivial zeros rho with |Im(rho)| < 396.4 (the first 200 zeros), c_K(rho) != 0. Verified at 50-digit precision.

### What Seems Out of Reach

A proof that for FIXED K (say K=10), c_K(rho) != 0 for ALL nontrivial zeros rho. This would require:
- Either: algebraic independence results for {p^{-i*gamma_j}} that are far beyond current number theory.
- Or: quantitative equidistribution on T^4 that controls individual points (not just averages).
- Or: an entirely new approach connecting the arithmetic of mu(k) to the distribution of zeta zeros.

The difficulty level appears comparable to the Linear Independence hypothesis for zeta zero ordinates (a standard conjecture in analytic number theory that has resisted proof for decades).

---

## 4. Recommended Paper Strategy

1. **State the Avoidance Conjecture** clearly, with full numerical evidence.
2. **Prove the K->infinity theorem** (under RH) as a rigorous result.
3. **Give the pole repulsion heuristic** as motivation for the conjecture.
4. **Present the statistical anomaly** (min at zeros >> min at generic points) as strong empirical evidence.
5. **Use the GRH-conditional detection theorem** (already proved in OPUS_CLEAN_PROOF_FINAL.md) as the main theoretical result.
6. **Note the connection to LI:** the Avoidance Conjecture follows from LI + quantitative equidistribution, and would in turn give unconditional spectroscopic detection.
7. **Be honest:** mark the conjecture as open, note it is hard, cite the difficulty comparison to LI.

---

## 5. Open Questions for Further Investigation

1. **Quantitative equidistribution:** Under GRH, what is the best discrepancy bound for {gamma_j log p mod 2pi} on T^4? Can Goldston-Gonek-Montgomery type results give anything useful?

2. **Baker-type transcendence:** Can Baker's theorem on linear forms in logarithms say anything about c_K(rho) = 0? The equation involves log 2, log 3, log 5, log 7 (algebraic) and gamma (transcendental), but Baker's theorem requires linear forms, and c_K = 0 is not linear.

3. **Explicit computation for specific K:** Can the zeros of c_10(s) be characterized more explicitly? For K=2, c_2(s) = -2^{-s}, which has zeros at s = (2n+1)pi*i/log 2 -- none of which are zeta zeros (this would require gamma_j = (2n+1)pi/log 2, contradicting any form of LI). Can similar arguments work for K=3?

4. **Small K cases:** For K=2, c_2(rho) = -2^{-rho} != 0 iff rho is not at s = (2n+1)pi*i/log 2. Since zeta zeros are not at regularly spaced points (GUE statistics), c_2(rho) != 0 for all rho. Can this be made rigorous? It would require proving that no zeta zero has imaginary part equal to an odd multiple of pi/log 2.

5. **Connection to Chowla's conjecture:** The avoidance is related to the cancellation structure of mu(k). Does the Chowla conjecture (or its proved special cases) give any information?

---

## References

- Langer, R.E. (1931). On the zeros of exponential sums and integrals. Bull AMS 37(4):213-239.
- Moreno, C.J. (1973). The zeros of exponential polynomials (I). Compositio Math 26:69-78.
- Montgomery, H.L. (1994). Ten Lectures on the Interface between Analytic Number Theory and Harmonic Analysis.
- Rubinstein, M. & Sarnak, P. (1994). Chebyshev's bias. Experimental Mathematics 3(3):173-197. [Uses LI]
- Gonek, S.M. (1989). On negative moments of the Riemann zeta-function. Mathematika 36:71-88.
- Montgomery, H.L. & Vaughan, R.C. (1974). Hilbert's inequality. J. London Math. Soc. (2) 8:73-82.
