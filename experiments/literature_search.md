# Literature Search: Unconditional Bounds for the Sign Theorem

**Date:** 2026-03-25
**Goal:** Find any result in the mathematical literature that could help prove the
unconditional Sign Theorem: DeltaW(p) <= 0 when M(p) <= -3.

**Recall the obstruction (from UNCONDITIONAL_EXTENSION.md):** We need ONE of:
- (A) An effective Riemann sum bound: Sum D(k/p)^2 ~ (p-1)/n * integral D(x)^2 dx
- (B) B_raw = 2 Sum D(f) delta(f) >= 0 (positive correlation of D and delta)
- (A') An unconditional bound on W(p-1) better than O(log N)
- Any other route to DeltaW(p) < 0

---

## 1. Farey Discrepancy: Best Known Unconditional Bounds

### 1.1. Dress 1999 -- Absolute Discrepancy Equals 1/Q Exactly

**Paper:** F. Dress, "Discrepance des suites de Farey," J. Theorie Nombres Bordeaux 11(2), 345-367, 1999.
**URL:** https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.255/

**Result:** The absolute (L-infinity) discrepancy of the Farey sequence F_Q equals 1/Q
exactly, for every Q >= 1. That is, sup_x |D(x)/N| = 1/Q where N = |F_Q|.

**Status:** UNCONDITIONAL.
**Applicability:** This gives us the sup-norm of D(x)/N. Since N ~ 3Q^2/pi^2, this
means max|D(x)| ~ 3Q/pi^2. This is the TRIVIAL bound on max|D| and does NOT
help with the Riemann sum problem (A), which needs control on the total variation
of D(x)^2, not just the sup-norm.

### 1.2. Niederreiter 1973 -- Order of Magnitude of Discrepancy

**Paper:** H. Niederreiter, "The distribution of Farey points," Math. Ann. 201, 341-345, 1973.

**Result:** The discrepancy D_N* of the Farey sequence F_Q has order of magnitude 1/Q.
This was the first proof that the discrepancy is Theta(1/Q).

**Status:** UNCONDITIONAL.
**Applicability:** Same as Dress -- gives the sup-norm behavior but not L2 or
total variation bounds.

### 1.3. Huxley 1971 -- Distribution of Farey Points

**Paper:** M.N. Huxley, "The distribution of Farey points, I," Acta Arith. 18, 281-287, 1971.

**Result:** Generalized Franel's theorem to zeros of Dirichlet L-functions. Proved the
discrepancy has order 1/Q. Also obtained results on sums of the discrepancy function.

**Status:** UNCONDITIONAL for the order-of-magnitude result.
**Applicability:** The generalization to L-functions is interesting but does not directly
help with our specific Riemann sum problem.

---

## 2. Franel-Landau Sums and L2 Discrepancy

### 2.1. The Franel-Landau Theorem (1924)

**Classical result:** The Riemann Hypothesis is EQUIVALENT to:
   Sum_{r=1}^{N} (a_r - r/N)^2 = O(Q^{-1+epsilon})
where a_r are the Farey fractions of order Q and N = |F_Q|.

Equivalently: Sum d_r^2 = O(N * Q^{-1+epsilon}) = O(Q^{1+epsilon}).

**Status:** CONDITIONAL (equivalent to RH). The L2 norm of the discrepancy being
small at a specific rate IS the Riemann Hypothesis.

**Applicability:** This is the CORE obstacle. Our problem (A) requires showing that
the Riemann sum of D(x)^2 at equispaced points approximates the integral well.
The integral itself is Sum d_r^2 (the Franel sum). Any polynomial-rate bound on
the Franel sum is equivalent to RH.

### 2.2. Codeca-Perelli 1988 -- Lp Spaces

**Paper:** P. Codeca, A. Perelli, "On the Uniform Distribution (mod 1) of the Farey
Fractions and lP Spaces," Math. Ann. 279, 413-422, 1988.

**Result:** Studied the Lp norms of the discrepancy of Farey fractions. Established
connections between Lp discrepancy bounds and the Riemann Hypothesis for various p.

**Status:** CONDITIONAL results (tied to RH for the sharp bounds).
**Applicability:** The L2 case (p=2) is directly our Franel sum. No unconditional
improvement over trivial bounds.

### 2.3. Kanemitsu-Yoshimoto 1996 -- Farey Series and RH

**Paper:** S. Kanemitsu, M. Yoshimoto, "Farey series and the Riemann hypothesis,"
Acta Arith. 75(4), 351-374, 1996. (Plus parts II, III, IV in subsequent papers.)

**Result:** Established multiple equivalences between sums of squared Farey discrepancies
and the Riemann Hypothesis. Extended the Franel-Landau framework.

**Status:** CONDITIONAL (all sharp bounds are RH-equivalent).
**Applicability:** Confirms that ANY approach through L2 Farey discrepancy bounds
at polynomial rates leads to RH-equivalence.

---

## 3. Karvonen-Zhigljavsky 2024 -- Maximum Mean Discrepancy

**Paper:** T. Karvonen, A. Zhigljavsky, "Maximum mean discrepancies of Farey sequences,"
arXiv:2407.10214, published in Acta Math. Hungar. 2025.
**URL:** https://arxiv.org/abs/2407.10214

**Main Result (Theorem 2.1):** For a large class of positive-semidefinite kernels
(including all Matern kernels of order >= 1/2), the polynomial rate
MMD(F_n) = O(n^{-3/2+epsilon}) = O(N^{-3/4+epsilon}) is EQUIVALENT to RH.

**Key Insight:** For the kernel K(x,y) = 1 + min{x,y}, the MMD equals the
discretized L2 discrepancy (Lemma 4.1). So the L2 Farey discrepancy having
any polynomial convergence rate is an RH-equivalent statement.

**Unconditional Results:** NONE. The paper works exclusively with conditional
(RH-dependent) results. All convergence rates require RH.

**Applicability to our problem:** NEGATIVE. This paper confirms that our approach
(A) -- bounding the Riemann sum of D(x)^2 -- is fundamentally an RH-equivalent
problem when stated in terms of polynomial convergence rates.

HOWEVER: Our problem is WEAKER than the full RH. We do not need
Sum D(k/p)^2 = O(Q^{1+epsilon}). We only need:
   Sum D(k/p)^2 >= (1 - epsilon) * (p-1)/n * Sum d_r^2
That is, we need the Riemann sum to be CLOSE to the integral, NOT that the
integral itself is small. This is a different (potentially easier) question.

---

## 4. Mertens Function: Explicit Unconditional Bounds

### 4.1. Walfisz 1963 -- Classical Unconditional Bound

**Reference:** A. Walfisz, "Weylsche Exponentialsummen in der neueren Zahlentheorie,"
VEB Deutscher Verlag der Wissenschaften, Berlin, 1963.

**Result:** M(x) = O(x * exp(-c * (log x)^{3/5} * (log log x)^{-1/5}))
for some constant c > 0.

**Status:** UNCONDITIONAL but INEFFECTIVE (the constant c is not computed).
**Applicability:** This is the best known unconditional bound on M(x) and
therefore on the Farey discrepancy max|D(x)|. But the ineffective constant
makes it useless for explicit computations. We CANNOT use it to bound the
total variation of D(x)^2.

### 4.2. Ramare 2012 -- Explicit Unconditional Bound

**Reference:** O. Ramare, explicit bounds on M(x).

**Result:** For D >= 100,000: |M(D)|/D <= 0.013/log(D).

**Status:** UNCONDITIONAL and EXPLICIT.
**Applicability:** This gives |M(D)| <= 0.013 * D / log(D). Since
the Farey discrepancy D(x) involves sums of mu, and max|D(x)| is related
to M(N), this bound is relevant. However, we need max|D(x)| not just M(N).

The discrepancy D(x) = Sum_{k<=N, k/N<=x} 1 - N*x involves ALL partial sums
of the Mobius function, not just M(N). The bound on individual D(f) involves
M evaluated at various points. So the Ramare bound gives:
   max|D(x)| <= sum of |M(N/k)| terms
which is O(N / log N) at best -- essentially the trivial bound.

### 4.3. Lee-Leong 2024 -- New Explicit Mertens Bounds

**Paper:** E.S. Lee, N. Leong, "New explicit bounds for Mertens function and the
reciprocal of the Riemann zeta-function," arXiv:2208.06141v4, 2024.
**URL:** https://arxiv.org/abs/2208.06141

**Results:**
1. M(x) << x * exp(-eta_1 * sqrt(log x)) -- explicit version, first of its kind
2. M(x) << x * exp(-eta_2 * (log x)^{3/5} * (log log x)^{-1/5}) -- first explicit
   version of the Walfisz-type bound
3. 1/zeta(sigma + it) << (log t)^{2/3} * (log log t)^{1/4} -- explicit

**Status:** UNCONDITIONAL and EXPLICIT (with computable constants eta_1, eta_2).
**Applicability:** THIS IS THE MOST PROMISING RESULT for our problem.

If eta_1 and eta_2 are computable, we can bound:
- max|D(x)| = O(N * exp(-c * sqrt(log N))) with an explicit c
- Total variation of D(x)^2 = O(N^2 * max|D(x)|)
- Riemann sum error for D(x)^2 at equispaced points k/p

The Riemann sum error is bounded by V(D^2) / p where V is total variation.
This gives: |Riemann sum - integral| / integral <= O(N * exp(-c sqrt(log N)) / p).
Since p ~ N, this is O(exp(-c sqrt(log N))) which DOES go to zero.

**KEY QUESTION:** Are the constants eta_1, eta_2 actually computed in the paper?
If so, we can determine for which N the Riemann sum error is < 1, which is
what we need.

**VERDICT:** Need to read the full paper to extract the explicit constants.

---

## 5. New Unconditional Local Discrepancy Estimates (2025)

**Paper:** (Author not fully identified), "New Analytical Formulas for the Rank of
Farey Fractions and Estimates of the Local Discrepancy," Mathematics 13(1), 140, 2025.
**URL:** https://www.mdpi.com/2227-7390/13/1/140

**Results:**
1. New recursive formula for the rank of any Farey fraction
2. New unconditional estimate of LOCAL discrepancy that DECREASES with the order
   of the Farey sequence (improves previously known estimates)
3. Second unconditional estimate derived from a sum of the Mertens function

**Status:** UNCONDITIONAL.
**Applicability:** POTENTIALLY USEFUL. If the local discrepancy estimates give
pointwise bounds on |D(a/b)| that are better than the trivial O(N/Q) bound,
this could help bound the total variation of D(x)^2, which is the key
ingredient for the Riemann sum approach (A).

**VERDICT:** Need to read the full paper to see the exact estimates and whether
they give effective, computable bounds.

---

## 6. Other Relevant References

### 6.1. Cox et al. 2021 -- Farey Sequence and Mertens Function

**Paper:** D. Cox et al., "The Farey Sequence and the Mertens Function,"
arXiv:2105.12352, 2021.
**URL:** https://arxiv.org/abs/2105.12352

**Result:** Functions of subsets of Farey fractions analogous to the Mertens function,
with results analogous to Mikolas's theorem.

**Applicability:** Provides structural insight into the Farey-Mertens connection
but no new unconditional bounds.

### 6.2. Weber 2019 -- Quadratic Farey and Riemann Sums

**Paper:** M. Weber, "On the Uniform Distribution (mod 1) of the Farey Sequence,
quadratic Farey and Riemann sums," arXiv:1906.07628, 2019.

**Result:** Sharp estimates of Farey sums for 1-periodic functions with Dini-type
regularity. Also results for quadratic Riemann sums related to local integrals
of the zeta function.

**Applicability:** The "Riemann sums" in this paper are sums over Farey points
(not equispaced points), so the setting is different from our problem.

### 6.3. Cobeli-Zaharescu 2003 -- Survey

**Paper:** C. Cobeli, A. Zaharescu, "The Haros-Farey sequence at two hundred years.
A survey," Acta Univ. Apulensis 5, 1-38, 2003.
**URL:** https://eudml.org/doc/126412

**Applicability:** Comprehensive survey of Farey fraction distribution. Useful
background but no new bounds.

### 6.4. Alkan-Goral -- Sums over Mobius Function and Discrepancy

**Paper:** E. Alkan, H. Goral, "On sums over the Mobius function and discrepancy
of Farey sequences," J. Number Theory, 2013.
**URL:** https://www.sciencedirect.com/science/article/pii/S0022314X13000218

**Result:** Upper bounds on absolute discrepancy of modified Farey sequences.

**Applicability:** May provide bounds on individual D(f) values that could help
with total variation estimates.

### 6.5. Hall-Shiu 2003 -- Index of a Farey Sequence

**Paper:** R.R. Hall, P. Shiu, "The index of a Farey sequence," Michigan Math. J.
51(1), 2003.
**URL:** https://projecteuclid.org/journals/michigan-mathematical-journal/volume-51/issue-1/The-index-of-a-Farey-sequence/10.1307/mmj/1049832901.pdf

**Result:** Studies the "index" of Farey sequences (a quantity related to the sum
of discrepancies).

**Applicability:** The index is related to the L1 norm of the discrepancy.
Different from our L2 problem.

---

## 7. Assessment and Recommendations

### 7.1. What the Literature Says

The literature makes clear that:

1. **Any polynomial-rate L2 bound on Farey discrepancy is RH-equivalent.**
   (Franel-Landau, Kanemitsu-Yoshimoto, Karvonen-Zhigljavsky all confirm this.)

2. **The best unconditional bound on M(x) is Walfisz-type**, now with explicit
   constants thanks to Lee-Leong 2024.

3. **The sup-norm discrepancy is exactly 1/Q** (Dress 1999), which is the trivial
   bound and not sufficient.

4. **New unconditional local discrepancy estimates exist** (MDPI 2025 paper) that
   improve over previous bounds, but it is unclear if they are effective enough.

### 7.2. Most Promising Path: Lee-Leong Explicit Mertens Bounds

The Lee-Leong 2024 paper is the most promising for our problem because:

- It gives EXPLICIT unconditional bounds on M(x) with computable constants
- These bounds can be translated to bounds on max|D(x)| and total variation of D^2
- The Riemann sum error for D(x)^2 at equispaced points can then be bounded
- The error goes to zero (at a sub-polynomial rate), so there exists N_0 beyond
  which the Riemann sum approximation is good enough

**The key question is whether N_0 is small enough** that the gap between N_0 and
our computational verification range (p <= 200,000, so N ~ 450) can be bridged.

If eta_1 in Lee-Leong is, say, 0.01, then exp(-0.01 * sqrt(log N)) < 0.5
requires log(N) > 4800, i.e., N > e^4800 -- FAR too large. Even with the
stronger Walfisz-type bound, N_0 would be astronomically large.

**ASSESSMENT: The Lee-Leong bounds, while explicit, are almost certainly too weak
to close the gap. The Walfisz-type saving exp(-(log x)^{3/5-epsilon}) is tiny
for any computationally accessible N.**

### 7.3. Alternative: Approach (B) -- B_raw >= 0

No paper in the literature directly addresses the correlation between D(f) and
delta(f) = f - {pf}. This is because:
- D(f) comes from additive number theory (counting fractions)
- delta(f) comes from multiplicative structure (multiplication by p mod 1)
- Their correlation mixes these two worlds

The closest results are from equidistribution theory (Weyl sums, exponential sums),
but none address this specific cross-term.

### 7.4. Alternative: Direct W(p-1) Bounds

No paper gives an unconditional bound on W(p-1) = Sum |d_r|^2 that is better
than the trivial O(N log N) coming from the prime number theorem. Any improvement
in the exponent would be RH-equivalent.

### 7.5. Conclusion

**The literature search indicates that proving the unconditional Sign Theorem
analytically for all primes requires either:**

1. **A breakthrough in explicit Mertens bounds** (constants many orders of magnitude
   better than current best), OR

2. **A new technique** that does not go through the Farey discrepancy bounds at all,
   possibly exploiting the specific structure of DeltaW(p) rather than bounding
   its components individually, OR

3. **Extended computation** to cover a larger range, combined with the existing
   sub-polynomial analytical bound that kicks in for sufficiently large p
   (even though N_0 is currently unknown/astronomical).

**No existing result in the literature directly solves our problem.** The most
relevant new result is Lee-Leong 2024, which gives the first explicit Walfisz-type
Mertens bounds, but the constants are almost certainly insufficient for our needs.

The MDPI 2025 paper on local Farey discrepancy deserves closer reading -- if its
bounds are effective enough to improve the total variation estimate for D(x)^2,
it could help tighten the Riemann sum approximation.

---

## Sources

- [Dress 1999 - Discrepance des suites de Farey](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.255/)
- [Karvonen-Zhigljavsky 2024 - MMD of Farey sequences](https://arxiv.org/abs/2407.10214)
- [Lee-Leong 2024 - Explicit Mertens bounds](https://arxiv.org/abs/2208.06141)
- [MDPI 2025 - Local discrepancy of Farey fractions](https://www.mdpi.com/2227-7390/13/1/140)
- [Cox et al. 2021 - Farey and Mertens](https://arxiv.org/abs/2105.12352)
- [Weber 2019 - Quadratic Farey sums](https://arxiv.org/abs/1906.07628)
- [Cobeli-Zaharescu 2003 - Survey](https://eudml.org/doc/126412)
- [Kanemitsu-Yoshimoto 1996 - Farey series and RH (Acta Arith. 75(4))](https://link.springer.com/article/10.1023/A:1006543108881)
- [Alkan-Goral 2013 - Sums over Mobius and discrepancy](https://www.sciencedirect.com/science/article/pii/S0022314X13000218)
- [Hall-Shiu 2003 - Index of Farey sequence](https://projecteuclid.org/journals/michigan-mathematical-journal/volume-51/issue-1/The-index-of-a-Farey-sequence/10.1307/mmj/1049832901.pdf)
- [Karvonen-Zhigljavsky (Acta Math. Hungar. 2025)](https://link.springer.com/article/10.1007/s10474-025-01577-5)
- [Huxley-Zhigljavsky - Farey fractions and hyperbolic lattice points](https://ssa.cf.ac.uk/zhigljavsky/pdfs/number%20theory/Huxley_Zh.pdf)
- [Codeca-Perelli 1988 - Farey fractions and Lp spaces](https://link.springer.com/article/10.1007/BF01456278)
