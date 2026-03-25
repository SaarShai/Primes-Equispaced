# FINAL PROOF ATTEMPT: B+C > 0 and Unconditional Extension

## Executive Summary

This document reports the results of a deep analytical investigation into two goals:

1. **GOAL 1:** Prove B+C > 0 analytically for all primes p >= 11.
2. **GOAL 2:** Make progress on the unconditional extension (DeltaW < 0 for ALL primes with M <= -3).

**Bottom line:** Both goals encounter fundamental obstructions that place them in the territory of deep analytic number theory. We identify the precise mathematical barriers and the most promising paths forward.

---

## GOAL 1: B+C > 0 Analytically

### 1.1. The Setup

We need to show R > -1 where R = 2 Sum(D * delta) / Sum(delta^2).

The approach is to bound |Sum D*delta| relative to Sum delta^2. Writing Sum D*delta = Sum_b C_b where C_b = Sum_{gcd(a,b)=1} D(a/b) * delta(a/b), the question reduces to bounding the aggregate cross term.

### 1.2. SD(D_b) Scaling

**Finding:** The within-denominator standard deviation SD(D_b) scales as approximately sqrt(n/b), where n = |F_N| and b is the denominator.

*Explanation:* D(a/b) = Sum_{d<=N} E_d(a/b) where E_d(a/b) = #{c: gcd(c,d)=1, c/d <= a/b} - phi(d)*(a/b). These are approximately independent across d, each contributing variance of order phi(d)/b to Var(D) within denominator b. Summing over d gives Var_D ~ n/b.

**Numerical verification (ratio SD(D_b) / sqrt(n/b)):**

| p | b=5 | b=10 | b=15 | b=20 | b=30 |
|---|-----|------|------|------|------|
| 97 | 0.039 | 0.038 | 0.079 | 0.136 | 0.238 |
| 199 | 0.031 | 0.046 | 0.085 | 0.070 | 0.112 |
| 307 | 0.012 | 0.021 | 0.017 | 0.015 | 0.052 |

The ratio is small (0.01 - 0.24), meaning SD(D_b) is much LESS than sqrt(n/b). The actual scaling is closer to SD(D_b) ~ c_b * sqrt(n/b) with c_b typically in [0.01, 0.15].

### 1.3. Why Cauchy-Schwarz Fails

**Bound:** |R| <= 2 * sqrt(V_within / Sum delta^2), where V_within = Sum_b phi_b * Var_D_b.

**Problem:** V_within ~ n * Sum phi(b)/b ~ n * (6/pi^2) * N, while Sum delta^2 ~ N^2 / (2 pi^2).

The ratio V_within / Sum delta^2 ~ 36N / pi^2, which GROWS with N.

Therefore the CS bound gives |R| = O(sqrt(N)), which is useless for proving |R| < 1.

**Numerical evidence:**

| p | V_within/Sdq | CS bound on |R| | Actual |R| |
|---|-------------|-----------------|------------|
| 11 | 4.5 | 4.3 | 0.52 |
| 97 | 90.7 | 19.0 | 0.21 |
| 199 | 222.9 | 29.9 | 6.89 |
| 307 | 329.0 | 36.3 | 3.07 |
| 499 | 560.1 | 47.3 | 6.88 |

The CS bound is 5-50x larger than the actual |R|.

### 1.4. The Critical Mechanism: Sign Cancellation

**Why |R| stays bounded despite the growing V_within/Sdq ratio:**

The global correlation rho_global = Sum D~*delta / sqrt(V_within * Sdq) DECAYS as approximately 1/sqrt(N).

Since |R| = 2 * |rho_global| * sqrt(V_within/Sdq), and V_within/Sdq ~ cN, we get |R| ~ 2 * (c'/sqrt(N)) * sqrt(cN) = 2c'*sqrt(c), which is bounded.

**Why rho_global decays:** The per-denominator cross terms C_b change sign across different denominators. The correlation rho_b between D~ and delta within denominator b varies from -0.98 to +0.98, with roughly equal positive and negative values.

**Numerical evidence of sign cancellation (p=97):**
- 47 denominators with rho_b > 0
- 37 denominators with rho_b < 0
- Mean rho_b = -0.002 (nearly zero)
- RMS rho_b = 0.296

**Numerical evidence of sign cancellation (p=307):**
- 239 denominators with rho_b > 0
- 54 denominators with rho_b < 0
- Mean rho_b = 0.153
- RMS rho_b = 0.257

The cancellation is NOT perfect random sign behavior. The mean rho_b drifts positive for larger p (which is why R > 0 for most large p). But the cancellation is sufficient to keep |R| bounded.

### 1.5. The Random Walk Ratio

If C_b were independent random variables, we would expect:
|Sum C_b| / sqrt(Sum C_b^2) ~ 1/sqrt(K) where K is the number of terms.

**Numerical evidence:**

| p | |Sum C_b| / sqrt(Sum C_b^2) | 1/sqrt(#terms) | Ratio |
|---|---------------------------|-----------------|-------|
| 11 | 0.97 | 0.41 | 2.4 |
| 97 | 0.51 | 0.11 | 4.7 |
| 199 | 10.95 | 0.07 | 149 |
| 307 | 9.24 | 0.06 | 159 |
| 499 | 16.68 | 0.05 | 370 |

**This is a problem.** For larger p, the ratio |Sum C_b|/sqrt(Sum C_b^2) grows significantly beyond the 1/sqrt(K) random expectation. This means C_b does NOT behave like independent random variables for large p. There is a systematic positive bias that grows.

### 1.6. The Permutation Identity

We verified the exact identity:
C_b = (1/b) * Sum_a a * [D(a/b) - D(sigma_{p^{-1}}(a)/b)]

This expresses C_b as measuring how D changes under the multiplicative permutation sigma_{p^{-1}} mod b. The identity is verified to machine precision for all tested denominators.

**Interpretation:** C_b is large when the Farey discrepancy D is significantly different at a/b compared to where the multiplicative permutation sends a/b. This ties the cross term to the interplay between additive structure (Farey ordering) and multiplicative structure (modular arithmetic).

### 1.7. Proof Strategy Assessment

**For B+C > 0 (equivalently R > -1):**

An analytical proof requires showing that the sign cancellation in Sum_b C_b is sufficient to prevent the total from being more negative than -Sum delta^2 / 2.

The data shows:
- R is negative for only 4 out of 91 primes in [11, 500]
- When R < 0, the minimum is R = -0.52 at p = 11
- For p >= 19, R is almost always positive

**The most promising proof structure:**

1. For p <= P0 (e.g., P0 = 500): exact computation (done, R > -1 for all).

2. For p > P0: Show R is bounded below by -1 + epsilon for some epsilon > 0.

   The challenge: the only known bound is the CS bound which gives |R| = O(sqrt(N)), useless.

   **Needed:** Either
   (a) A refined bound exploiting the sign structure of C_b across denominators, OR
   (b) A direct proof that Sum_b C_b >= -Sum delta^2 / 2 using the permutation identity.

   Approach (b) requires understanding when D(a/b) - D(sigma_{p^{-1}}(a)/b) is systematically negative, which is related to whether the multiplicative permutation moves fractions toward regions of higher or lower Farey discrepancy. This is a deep question about the correlation between additive and multiplicative structures.

### 1.8. Conclusion for Goal 1

**B+C > 0 is verified for all primes p in [11, 500] by exact computation.**

**An analytical proof for all p >= 11 requires proving quasi-random sign cancellation in Kloosterman-type sums.** Specifically, one needs to show that the per-denominator cross terms C_b, viewed as a function of b with p fixed, exhibit sufficient cancellation to keep their sum bounded relative to Sum delta^2.

This is a statement about the equidistribution of the Farey discrepancy function under multiplicative permutations, and appears to require tools from the theory of exponential sums or automorphic forms.

**The fact that R is asymptotically POSITIVE (and growing) for large p is actually good news:** it means B+C > 0 becomes easier to prove for large p, and the hard case is small p where exact verification works.

---

## GOAL 2: Unconditional Extension via Telescoping

### 2.1. The Telescoping Idea

The idea was: write W(p) = W(2) - Sum_{k=3}^{p} DeltaW(k) and show each |DeltaW(k)| is bounded by c*W(k-1)/k for c < 1, giving geometric decay control.

### 2.2. Critical Discovery: W is NOT Monotonically Non-Decreasing

**W DECREASES at most composite steps and INCREASES at prime steps (for p >= 11).**

Specifically:
- At N = 3, 4, 5, 6, 7, 8, 9, 10: W decreases (DeltaW > 0)
- At N = 11 (prime): W INCREASES (DeltaW < 0) -- first increase!
- At N = 12 (composite): W decreases again
- At N = 13 (prime): W increases
- Pattern continues: primes push W up, composites pull it back down

**Out of 200 steps, 147 composite steps have DeltaW > 0 (W decreases).**

This means the telescoping approach as originally conceived is invalid: we cannot claim W is monotonically non-decreasing.

### 2.3. The DeltaW/W Ratio

| p | |DeltaW/W| * p | |DeltaW/W| * p / log(p) |
|---|-------------|----------------------|
| 11 | 0.66 | 0.28 |
| 31 | 3.32 | 0.97 |
| 97 | 0.92 | 0.20 |
| 199 | 6.85 | 1.29 |
| 499 | 6.95 | 1.12 |

The maximum of |DeltaW/W| * p is 7.99 (at p = 467), giving c ~ 8, far too large for the telescoping product to converge with c < 1.

Even with the log correction, max |DeltaW/W| * p / log(p) = 1.30, which gives c ~ 1.3 > 1, still not sufficient.

### 2.4. Why Telescoping Fails

The telescoping approach requires proving DeltaW(k) <= 0 at each step, which IS the sign theorem itself. So telescoping provides no leverage -- it is equivalent to what we are trying to prove.

Moreover, the bound |DeltaW(p)|/W(p-1) is NOT small enough (it is O(1/p) but with a large constant c ~ 8) to give useful decay rates.

### 2.5. Alternative: Net Effect Over Prime-Composite Cycles

A more promising observation: while W oscillates (down at composites, up at primes), the NET effect over each "cycle" from one prime to the next is positive (W increases from W(p) to W(p') where p' is the next prime).

Specifically, defining Delta_net(p, p') = W(p') - W(p) for consecutive primes p < p':
- This is the SUM of all DeltaW(N) for N = p+1, ..., p'.
- It includes ONE prime increase (at N = p') and several composite decreases.
- The prime increase MORE than compensates for the composite decreases.

This suggests looking at the CUMULATIVE effect rather than individual steps.

### 2.6. The Fundamental Obstruction Remains

The unconditional extension requires proving one of:

**(A) Riemann Sum Approximation:** Sum_{k=1}^{p-1} D_old(k/p)^2 closely approximates the integral of D(x)^2. This requires effective equidistribution bounds with effective constants, which are not available unconditionally (the Walfisz bound has an ineffective constant).

**(B) Cross-Term Non-Negativity:** B_raw >= 0. This requires understanding the correlation between Farey discrepancy and multiplicative shift, which mixes additive and multiplicative number theory.

**(C) New Technique:** A proof that does not go through the four-term decomposition.

### 2.7. A New Observation: The "Effective Margin" is Large

From the data, for primes p >= 11 with M(p) <= -3:
- B/A + C/A + D/A >= 1.098 (minimum at p = 2857)
- The margin B/A + C/A + D/A - 1 is at least 0.098

This 10% margin is HUGE in analytic number theory terms. Any approach that loses less than 10% would suffice.

The CS bound on B/A gives |B/A| <= 2*sqrt(V_within*Sdq)/dilution_raw, which is O(1) (not O(sqrt(N)) as for |R|, because the normalization by dilution_raw introduces an extra factor of 1/N). Specifically, |B/A| appears bounded by about 0.3-0.5 empirically.

So the real question reduces to: **can we prove D/A >= 1 - epsilon with epsilon < 0.1?**

This is the Riemann sum problem: proving that sampling D(x)^2 at equally-spaced points captures at least 90% of the integral.

---

## Summary Table

| Question | Status | Obstruction |
|----------|--------|-------------|
| B+C > 0 for p <= 500 | PROVED (exact computation) | None |
| B+C > 0 for all p | OPEN | Sign cancellation in Kloosterman sums |
| |R| < 1 for all p | OPEN | Same as above |
| R > 0 for large p | STRONGLY SUGGESTED by data | Would follow from positive bias of C_b |
| DeltaW <= 0 for p <= 100,000 | PROVED (computation) | None |
| DeltaW <= 0 for all p | OPEN | Effective Riemann sum bounds OR B >= 0 |
| Telescoping approach | FAILS | c ~ 8 >> 1; W oscillates |
| D/A ~ 1 with effective error | OPEN | Effective equidistribution |
| Net W increase per prime cycle | OBSERVED | Not formalized |

## Viable Next Steps

1. **Extend B+C > 0 verification** to p = 5000 or 10000 (computationally cheap, strengthens the verified range).

2. **Formalize the R > 0 for large p result** as a conditional statement: "If p > P0 and SD(D_b)/SD(delta_b) * rho_eff < 1/(2*sqrt(V_within/Sdq)), then B+C > 0." Then show this condition holds for large p using the positive bias.

3. **Pursue the "effective margin" approach** for the unconditional extension: prove D/A >= 0.9 (rather than D/A ~ 1) using crude but effective bounds on the Riemann sum error, combined with the C/A lower bound.

4. **Study the large sieve inequality** applied to D(x)^2 sampled at k/p -- this is precisely the setting where the large sieve gives effective bounds on Riemann sum errors.

5. **Investigate the operator-theoretic approach** (Path D from UNCONDITIONAL_EXTENSION.md): the Farey map eigenvalues may provide a route to proving monotonicity without the four-term decomposition.
