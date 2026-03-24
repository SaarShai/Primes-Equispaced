# Research Directions: Farey-Mertens Identities

**Date:** March 2026
**Project:** "New Identities Connecting Farey Sequences to the Mertens Function via Per-Step Discrepancy"
**Authors of original paper:** Saar Shai and Claude Opus 4.6 (Anthropic)

This document maps out how the Farey-Mertens identities discovered in this project can advance other areas of mathematics, how the identities themselves can be developed further, and concrete next steps for the paper and future work.

---

## PART A: CONNECTIONS TO OTHER AREAS OF MATHEMATICS

### A1. Discrepancy Theory and the Riemann Hypothesis

**The 2025 Karvonen-Zhigljavsky paper is directly relevant.** Karvonen and Zhigljavsky ("Maximum mean discrepancies of Farey sequences," *Acta Mathematica Hungarica*, 2025) proved that the maximum mean discrepancy (MMD) of Farey sequences under Matern kernels converges at polynomial rate if and only if the Riemann Hypothesis holds. Their work characterizes RH through kernel discrepancy of Farey sequences -- a framework that is structurally close to what this project does with L2 discrepancy.

**Concrete connection:** The universal formula (Theorem 3.3) evaluates the Fourier coefficients of the Farey empirical measure exactly. Since kernel MMD is determined by Fourier coefficients (via Mercer's theorem), the universal formula should give *exact* MMD values for any frequency-computable kernel, not just asymptotic bounds. This would strengthen the Karvonen-Zhigljavsky results from asymptotic equivalence to exact evaluation.

**Open problem:** Can the universal formula be used to compute the kernel MMD of F_N in closed form for the Matern-1/2 kernel (exponential kernel)? If so, the RH equivalence becomes: RH if and only if a specific explicit sum involving M(floor(N/d)) is O(N^{1/2+epsilon}).

**References to cite:**
- Karvonen, T. and Zhigljavsky, A. "Maximum mean discrepancies of Farey sequences." *Acta Math. Hungar.* (2025). https://doi.org/10.1007/s10474-025-01577-5
- Dress, F. "Discrepance des suites de Farey." *J. Theor. Nombres Bordeaux* 11 (1999), 345-367.

### A2. Dirichlet L-functions and Twisted Mertens Functions

The universal formula Sigma_{f in F_N} e^{2pi i m f} = M(N) + 1 + Sigma_{d|m, d>=2} d * M(floor(N/d)) naturally generalizes to *twisted* Farey sums.

**Key idea:** Replace the Mobius function mu(n) with a Dirichlet character chi(n) * mu(n). Define the twisted Mertens function M_chi(N) = Sigma_{k<=N} chi(k) * mu(k). By the same Ramanujan sum decomposition, one should obtain:

  Sigma_{f in F_N} chi(denom(f)) * e^{2pi i m f} = M_chi(N) + correction terms

This would connect Farey geometry to Dirichlet L-functions L(s, chi), since M_chi controls the partial sums of 1/L(s, chi).

**What this enables:**
- A Farey-geometric reformulation of the Generalized Riemann Hypothesis (for each chi)
- Per-step wobble analysis with character twists, potentially revealing how primes in arithmetic progressions affect Farey uniformity differently
- Connection to Chebyshev bias: the Rubinstein-Sarnak density function (1994) quantifies the logarithmic density of x where pi(x;q,a) > pi(x;q,b). A twisted per-step analysis could give a *geometric* interpretation of Chebyshev bias through Farey discrepancy in arithmetic progressions.

**References:**
- Rubinstein, M. and Sarnak, P. "Chebyshev's bias." *Experiment. Math.* 3 (1994), 173-197.
- Dickinson, H. "Zeros of Dirichlet L-functions near the critical line." *Mathematika* 70 (2024).
- Lu, G. and Ma, J. "Exponential sums with the Dirichlet coefficients of Rankin-Selberg L-functions." *Monatsh. Math.* (2024).

### A3. Random Matrix Theory and the GUE Conjecture

The Montgomery-Odlyzko law says that the pair correlation of nontrivial zeta zeros matches the GUE (Gaussian Unitary Ensemble) eigenvalue statistics. The universal formula provides a new handle on this.

**Observation:** The Farey exponential sum at frequency m encodes M at divisor-scaled arguments: M(N), M(N/2), M(N/3), etc. These are exactly the quantities that appear in explicit formulas connecting zeta zeros to arithmetic. If one studies the *covariance structure* of the Farey exponential sums at different frequencies m1, m2, the off-diagonal terms involve joint distributions of M(N/d1) and M(N/d2), which under RMT assumptions should exhibit universal correlations.

**Concrete direction:** Compute the correlation matrix Corr(S(m1, N), S(m2, N)) where S(m,N) = Sigma_{f in F_N} e^{2pi i m f}, for large N and many frequency pairs. Compare to GUE predictions. The universal formula makes this computation tractable since it reduces to correlations of Mertens function values.

**Open question:** Does the per-step wobble Delta W(p) at primes exhibit GUE-type nearest-neighbor spacing statistics? The sigmoid relationship suggests the distribution is controlled by M(p)/sqrt(p), which under RMT should have a specific limiting distribution.

**References:**
- Keating, J. P. and Snaith, N. C. "Random matrix theory and zeta(1/2+it)." *Comm. Math. Phys.* 214 (2000), 57-89.
- Hughes, C. P. "Random matrix theory and the distribution of the zeros of..." *Lecture notes*, University of Manchester.

### A4. Sieve Methods and Additive Combinatorics

**Large sieve connection:** The classical large sieve inequality bounds Sigma_{q<=Q} Sigma_{a (mod q), gcd(a,q)=1} |Sigma_{n<=N} a_n e^{2pi i n a/q}|^2. The inner exponential sums are exactly what the universal formula evaluates when the a_n are indicator functions of the Farey sequence. This means the universal formula gives *exact* values where the large sieve gives *bounds*.

**Potential application:** Use the exact Farey exponential sums to:
1. Test the tightness of large sieve bounds in specific cases
2. Construct improved Selberg sieve weights using Farey geometry
3. Understand the "sieve parity barrier" through the lens of prime/composite asymmetry in Delta W

**Higher uniformity connection:** Matomaki, Radziwill, Shao, Tao, and Teravinen ("Higher uniformity of arithmetic functions in short intervals II," arXiv:2411.05770, 2024) prove that the Mobius function has small Gowers norms in short intervals. The per-step perspective in this project is complementary: it studies how Mobius cancellation manifests geometrically at each integer, rather than in intervals.

**Open problem:** Can the per-step Delta W analysis detect the "Siegel zero" phenomenon? If a Sirichlet character chi had a real zero very close to s=1, the twisted Mertens function M_chi would have anomalous growth, which should appear as anomalous behavior in twisted Farey wobble.

**References:**
- Matomaki, K. et al. "Higher uniformity of arithmetic functions in short intervals II." arXiv:2411.05770 (2024).
- The large sieve for square moduli, revisited. arXiv:2503.18009 (2025).

### A5. The Selberg Class and Universality

The Selberg class S consists of L-functions satisfying axioms (Dirichlet series, analytic continuation, functional equation, Ramanujan conjecture, Euler product). For any F in S, the partial sums of 1/F(s) generalize the Mertens function.

**Key question:** Can the bridge identity be formulated for general Selberg class elements? The proof uses:
1. Decomposition by denominator (Farey structure)
2. Ramanujan sums c_q(n) = mu(q) when gcd(n,q)=1 (Mobius property)
3. Summation exchange

Step 2 is specific to the Riemann zeta function (mu = coefficients of 1/zeta). For a general F in S with coefficients a_F(n), one would replace mu(n) with the Dirichlet series coefficients of 1/F(s). The question is whether the Farey decomposition still yields clean closed-form results.

**Universality theorem angle:** Voronin's universality theorem says zeta(s) can approximate any nonvanishing holomorphic function in the critical strip. The universal formula links Farey exponential sums to Mertens function values. Can this be combined to show that Farey exponential sums (as functions of N, at fixed m) have a universality property?

**References:**
- Steuding, J. "Universality for L-functions in the Selberg class." *Lith. Math. J.* 50 (2010).
- arXiv:2302.09709 "Universality for the iterated integrals of logarithms of L-functions in the Selberg class" (2023).

### A6. The Erdos Discrepancy Problem

Tao (2015) proved that for any sequence f: N -> {-1,+1}, the discrepancy sup_{n,d} |Sigma_{k=1}^{n} f(kd)| is unbounded. The proof reduces to completely multiplicative functions via Fourier analysis, then uses the Elliott conjecture.

**The bridge identity connection:** For f = mu (the Mobius function, restricted to {-1,0,+1}), the partial sums Sigma_{k<=n} mu(kd) involve the Mertens function at scaled arguments, exactly as in the universal formula. Specifically:

  Sigma_{k<=n} mu(k) = M(n) (the d=1 case, which the bridge evaluates geometrically)

For d > 1, Sigma_{k<=n} mu(kd) involves M(n) values that appear in the universal formula's divisor sum.

**Open direction:** The paper notes that composites produce 96% of positive Delta W (uniformity improvement) while primes produce 99% of negative Delta W (degradation). This prime/composite asymmetry in Farey uniformity may be relevant to understanding why the Erdos discrepancy problem is "hard" for multiplicative functions -- the signed cancellations in mu create a delicate balance that manifests geometrically as the near-zero wobble changes.

**References:**
- Tao, T. "The Erdos discrepancy problem." *Discrete Analysis* (2016), Paper No. 1.
- "Good weights for the Erdos discrepancy problem." *Discrete Analysis* (2024).

### A7. Zero-Free Regions and Explicit Bounds

The Korobov-Vinogradov zero-free region for zeta(s) has been recently improved (Ford, 2024-2025, improving the constant to c = 48.0718; Yang, 2024, in *Research in Number Theory*). These improvements feed directly into bounds on M(N).

**The per-step perspective adds information:** Standard bounds on M(N) come from integrating information about zeta zeros. The per-step decomposition W(N) = W(1) - Sigma Delta W(k) gives a *different* structural decomposition: it separates prime contributions (controlled by M) from composite contributions (controlled by totient/divisor structure). If one could prove that the composite contributions are always positive (the 96% observation suggests this is nearly true), then bounds on W(N) would reduce to bounds on the sum of prime contributions only.

**Concrete next step:** Determine whether the composite positivity rate (96%) can be proved to hold for all N, or at least for N beyond some explicit threshold. If so, this gives a new route to Mertens-type bounds: W(N) = O(N^{-1+epsilon}) + (composite correction), where the composite correction is provably positive.

**References:**
- Yang, A. "Explicit zero-free regions for the Riemann zeta-function." *Res. Number Theory* 9 (2023).
- Ford, K. "Zero-free regions for the Riemann zeta function." arXiv:1910.08205, updated February 2025.

---

## PART B: DEVELOPING THE IDENTITIES FURTHER

### B1. Inverting the Universal Formula

The universal formula expresses the Farey exponential sum S(m, N) in terms of M(N/d) for d | m. This is a system of equations:

  S(m, N) = M(N) + 1 + Sigma_{d|m, d>=2} d * M(floor(N/d))

**Question:** Can this be inverted? Given the exponential sums S(m, N) for m = 1, 2, ..., K, can we recover M(N), M(N/2), M(N/3), ...?

**Answer: Yes, via Mobius inversion on the divisor structure.** The formula has the shape of a Dirichlet convolution evaluated at integer points. Specifically, define g(m) = S(m, N) - 1 and h(d) = d * M(floor(N/d)) with h(1) = M(N). Then g = h * 1 (Dirichlet convolution with the constant function 1). By Mobius inversion: h(m) = Sigma_{d|m} mu(d) * g(m/d).

This means:

  m * M(floor(N/m)) = Sigma_{d|m} mu(d) * [S(m/d, N) - 1]

**Practical implication:** One can compute M(N/m) for any m by measuring Farey exponential sums at divisors of m. This is a *geometric* method of computing the Mertens function.

**Computational test:** Verify this inversion for N = 30, m = 1, ..., 40 using the existing computational data.

### B2. Higher-Order Statistics of Delta W

The paper studies the *sign* of Delta W(p). Much more information is available in the higher moments.

**Variance of Delta W over primes:** Define Var_P(N) = (1/pi(N)) * Sigma_{p<=N} Delta W(p)^2. How does this grow? The sigmoid suggests that for most primes, Delta W(p) ~ C * M(p) / p^2 for some constant C. If so:

  Var_P(N) ~ C^2 / N^4 * Sigma_{p<=N} M(p)^2

Under RH, M(p)^2 = O(p^{1+epsilon}), so Var_P(N) ~ O(N^{-3+epsilon}).

**Correlations between consecutive primes:** Does Delta W(p_n) correlate with Delta W(p_{n+1})? The Mertens function satisfies M(p_{n+1}) = M(p_n) - 1 (since mu(p) = -1 for all primes), so consecutive prime Mertens values are *perfectly correlated with offset -1*. But the wobble involves more than just M -- the cross-term Sigma D * delta introduces additional structure.

**Distribution of Delta W(p):** For primes with M(p) = k (fixed), what is the distribution of Delta W(p)? The sigmoid suggests it depends primarily on M(p)/sqrt(p). Map out the conditional distribution Delta W(p) | M(p) = k for various k values.

**Experiment to run:** From the existing wobble_primes_100000.csv data:
1. Compute Var(Delta W(p)) in sliding windows of 500 primes
2. Compute autocorrelation of the Delta W(p) sequence
3. For each k in {-5, -4, ..., 3, 4}, plot the histogram of Delta W(p) for primes with M(p) = k

### B3. Connecting the Sigmoid to Rubinstein-Sarnak

The sigmoid relationship (violation probability as a function of M(p)/sqrt(p)) bears a striking resemblance to the Rubinstein-Sarnak density function for Chebyshev bias.

**The Rubinstein-Sarnak framework:** Under GRH and the Linear Independence hypothesis (LI) for zeta zeros, Rubinstein and Sarnak showed that the logarithmic density delta(q; a, b) of the set {x : pi(x;q,a) > pi(x;q,b)} exists and can be computed from the distribution of a specific random variable involving zeta zeros.

**The analog here:** The "violation" event {Delta W(p) > 0 and M(p) < 0} plays the role of {pi(x;4,1) > pi(x;4,3)} in Chebyshev bias. The sigmoid transition at M(p)/sqrt(p) ~ 0 plays the role of the bias density.

**Rigorous connection would require:**
1. Express Delta W(p) in terms of the bridge identity plus cross-term corrections
2. Show that the cross-term Sigma D * delta has a distribution controlled by an explicit function of M(p)/sqrt(p)
3. Derive the sigmoid shape from the distribution of M(p)/sqrt(p) (which under RH is approximately Gaussian with mean ~ -sqrt(p) * C and variance ~ p * D for known constants C, D)

**Key obstacle:** Step 2 requires bounding Sigma D * delta, which is the anticorrelation lemma -- the main open problem of the paper. However, one could bypass the full proof and instead establish a *distributional* version: show that for "generic" primes (all but o(pi(N)) of them), the sigmoid relationship holds.

**References:**
- Rubinstein, M. and Sarnak, P. "Chebyshev's bias." *Experiment. Math.* 3 (1994), 173-197.
- Fiorilli, D. and Martin, G. "Inequities in the Shanks-Renyi prime number race: an asymptotic formula for the densities." *J. reine angew. Math.* 676 (2013).

### B4. Generating Function for Delta W(p) Over Primes

**Question:** Is there a Dirichlet series or other generating function for Delta W(p)?

The per-step wobble change can be decomposed as:

  Delta W(p) = (positive composite-like terms) + (terms involving M(p))

If one could write Delta W(p) ~ f(M(p), p) for an explicit function f, then:

  Sigma_{p} Delta W(p) * p^{-s} = Sigma_{p} f(M(p), p) * p^{-s}

This would relate the generating function for Delta W over primes to the Dirichlet series Sigma_p M(p) p^{-s}, which in turn relates to zeta and its derivatives.

**A more tractable object:** Instead of Delta W(p) itself, consider just the bridge term:

  Sigma_{f in F_{p-1}} cos(2pi p f) = M(p) + 2

The generating function for this over primes is:

  Sigma_p (M(p) + 2) p^{-s} = 2 * P(s) + Sigma_p M(p) p^{-s}

where P(s) = Sigma_p p^{-s} is the prime zeta function. The second term Sigma_p M(p) p^{-s} can be expressed via partial summation in terms of 1/zeta(s) and the prime counting function, connecting it to the deepest objects in analytic number theory.

### B5. Certifying the p = 92,173 Counterexample

The counterexample at p = 92,173 (M(p) = -2, Delta W > 0) is confirmed by three floating-point methods but not by exact arithmetic. This should be certified.

**Recommended approach: Ball arithmetic with the Arb library.**

Arb (by Fredrik Johansson) is a C library for arbitrary-precision interval (ball) arithmetic. Unlike naive floating-point, Arb tracks error bounds rigorously, so a certified computation would prove that Delta W(92173) lies in a specific interval that is provably positive.

**Implementation plan:**
1. Use Python's `python-flint` package (Python bindings to Arb/FLINT)
2. Compute all Farey fractions f in F_{92172} using exact rational arithmetic (this is feasible -- |F_{92172}| ~ 2.6 billion, but one can compute Delta W incrementally)
3. Alternatively: compute Delta W(p) using the decomposition Delta W = (sum of squared new displacements) - 2*(cross term) + (reindexing correction), where each piece can be computed in ball arithmetic with controlled precision.

**Alternative: Use mpmath's arbitrary-precision floats** with sufficient precision (e.g., 100 decimal digits) to ensure the result is reliable, though this would not give a formal certificate.

**Alternative: Exact rational arithmetic.** Since all Farey fractions are rationals and all operations are additions and multiplications, Delta W(p) is exactly rational. The computation is O(p^2) with rational arithmetic, which for p = 92,173 means ~8.5 billion rational operations. This is feasible with optimized GMP arithmetic in C.

**Libraries:**
- Arb: https://github.com/fredrik-johansson/arb (C, rigorous ball arithmetic)
- python-flint: Python bindings for FLINT/Arb
- mpmath: https://mpmath.org/ (Python, arbitrary precision, not rigorous intervals)
- SageMath: includes Arb as a standard package with high-level Python interface

### B6. The Anticorrelation Lemma: New Approaches

The main proof gap is showing Sigma D(f) * delta(f) < 0 for primes p >= 19 with M(p) <= 0. Fourteen approaches have been tried. Here are directions not yet explored:

**Approach 15: Probabilistic model.** Model the Farey fractions as a point process and show that D and delta are negatively correlated in expectation. The GUE/Poisson transition in spacing statistics of Farey sequences (known to be related to the pair correlation of zeta zeros) could provide the necessary probabilistic structure.

**Approach 16: Ergodic theory.** The Farey map T: [0,1] -> [0,1] defined by T(x) = {1/x} preserves the Gauss measure. The rank discrepancy D and shift delta can be viewed as observables on this dynamical system. Ergodic mixing properties might yield the required correlation estimate.

**Approach 17: Modular forms.** The Farey sequence parametrizes cusps of the modular group. The bridge identity has the form of a period integral of an Eisenstein series. The cross-term Sigma D * delta might be expressible as a Petersson inner product, where positivity/negativity results from spectral theory of automorphic forms are available.

**Approach 18: Computational verification to higher bounds.** Extend the computation from p <= 100,000 to p <= 10,000,000 or beyond. The C code already exists and is O(p^2) per prime; parallelizing across a cluster could reach p ~ 10^7 in days. Finding a second counterexample (or extending the zero-counterexample range for M <= -3) would guide the theoretical approach.

---

## PART C: PRACTICAL NEXT STEPS

### C1. What Is Classical vs. New

**Classical (known before this paper):**
- The evaluation Sigma_{f in F_N} e^{2pi i f} = M(N) + 1 is implicit in Edwards (1974), *Riemann's Zeta Function*, Section 12.2 ("The Riemann Hypothesis and Farey Series"). Edwards derives this as part of the Franel-Landau framework. The key step is the same: decompose by denominator, use c_q(1) = mu(q).
- The Franel-Landau theorem itself: RH iff Sigma |f_j - j/n| = O(N^{1/2+epsilon}).
- Ramanujan sums c_q(n) = mu(q) when gcd(n,q) = 1 (Ramanujan, 1918).
- The Farey involution sigma(f) = 1-f and its properties.

**New in this paper (to our knowledge):**
- The per-step decomposition Delta W(N) = W(N-1) - W(N) and its study.
- The per-frequency generalization: Sigma_{f in F_N} e^{2pi i m f} = M(N) + 1 + Sigma_{d|m, d>=2} d * M(floor(N/d)) for *all* m, N. The m=1 case is classical; the general case appears new.
- The prime/composite asymmetry in Delta W (96% composites improve, primes cause 99% of damage).
- The sigmoid relationship between violation probability and M(p)/sqrt(p).
- The displacement-cosine, delta-symmetric, and cross-term identities (Theorems 3.4-3.8).
- The formal verification in Lean 4 of the bridge identity chain.
- The applications to exact quadrature errors, iCZT spectral leakage, and slope quantization bias.

**The Edwards reference should be cited more precisely.** The paper currently cites Edwards (1974) but should specify Section 12.2 and note that Edwards presents the m=1 case as part of the Franel-Landau proof, not as an independent identity. The per-frequency generalization and divisor-sum formula are the main new contributions.

### C2. Prior Work on Per-Step Farey Discrepancy

**No prior work found.** Extensive searching found no papers that study how W(N) changes at individual steps. The Farey discrepancy literature focuses on:
- Cumulative discrepancy W(N) or D_N (Franel 1924, Landau 1924, Niederreiter 1973)
- Discrepancy in subintervals (Dress 1999, Haynes-Pollington-Velani 2018)
- Discrepancy for restricted denominator sets (Cobeli-Zaharescu 2003)
- Maximum mean discrepancy (Karvonen-Zhigljavsky 2025)

The per-step Delta W(N) perspective appears genuinely novel. This should be stated clearly in the paper.

### C3. Additional References the Paper Should Cite

The paper currently has 8 references. Here are 5 additional references that would strengthen it:

1. **Karvonen, T. and Zhigljavsky, A.** "Maximum mean discrepancies of Farey sequences." *Acta Math. Hungar.* (2025). -- *Directly relevant: RH equivalent via Farey kernel discrepancy. The universal formula may improve their results.*

2. **Cox, D., Ghosh, S., and Sultanow, E.** "The Farey Sequence and the Mertens Function." arXiv:2105.12352 (2021). -- *Studies Farey-Mertens connections from a different angle; introduces "companion functions" analogous to M(N). Should be compared to the universal formula.*

3. **Matomaki, K., Radziwill, M., Shao, X., Tao, T., and Teravinen, J.** "Higher uniformity of arithmetic functions in short intervals II." arXiv:2411.05770 (2024). -- *State-of-the-art on Mobius cancellation in short intervals; the per-step perspective is complementary.*

4. **Dress, F.** "Discrepance des suites de Farey." *J. Theor. Nombres Bordeaux* 11 (1999), 345-367. -- *Best known unconditional bounds on cumulative Farey discrepancy.*

5. **Kanemitsu, S., Sita Rama Chandra Rao, R., and Siva Rama Sarma, A.** "Some sums involving Farey fractions I." *J. Math. Soc. Japan* 34 (1982), 125-171. -- *Extensive study of sums over Farey fractions; some of the per-step identities may be implicit in their framework.*

**Bonus references (if extending the discussion):**

6. **Haynes, A., Pollington, A., and Velani, S.** "The Duffin-Schaeffer conjecture with extra divergence." *Math. Ann.* 353 (2012), 259-273. -- *For connections between Farey sequences and metric Diophantine approximation.*

7. **Balazard, M. and de Roton, A.** "Notes de lecture de l'article 'Disproof of the Mertens conjecture'." *J. reine angew. Math.* 649 (2010). -- *For context on Mertens function oscillations and the disproof of |M(x)| < sqrt(x).*

### C4. Experimental Mathematics Submission

**Journal fit:** *Experimental Mathematics* (Taylor & Francis) is an excellent target. The paper combines:
- Formal results inspired by experimentation (the sigmoid discovery)
- Conjectures suggested by experiments (the M <= -3 conjecture)
- Algorithms for mathematical exploration (per-step wobble computation)
- Computational verification alongside formal proofs

**Submission requirements (from the journal website):**
- Papers must present formal results inspired by experimentation, or conjectures supported by experiments
- Computer results should be presented in human-graspable form (not raw output)
- All peer review is single-anonymized
- Submission is online via the Taylor & Francis Submission Portal
- LaTeX is the preferred format

**What to do before submitting:**
1. Certify the p = 92,173 counterexample (see B5 above) -- the journal will want this
2. Add the 5 additional references from C3
3. Clarify the classical/new boundary (see C1) more precisely in Section 3
4. Consider splitting: the 8 theorems + applications + computational findings may be better as two papers: (a) the identities and their proofs, (b) the computational investigation and conjectures

**Alternative journals:**
- *Mathematics of Computation* (AMS): good for the formal verification angle
- *Journal of Number Theory* (Elsevier): if the paper is split, the pure identity paper could go here
- *Research in Number Theory* (Springer): newer journal, fast turnaround, good for computational number theory
- *The Ramanujan Journal* (Springer): given the Ramanujan sum connection, this is thematically appropriate

### C5. Immediate Computational Experiments

These can be run with the existing codebase:

1. **Extend computations to N = 1,000,000:** The C code is O(N^2) per prime, so primes near 10^6 take ~10^12 operations each. This is feasible on a modern workstation (days of compute time). Focus on primes with M(p) = -2 (the counterexample class) to find more violations or extend the gap.

2. **Compute the inversion formula (B1):** Verify that Mobius inversion of the universal formula correctly recovers M(N/d) from the exponential sums, for N = 30, m = 1,...,40.

3. **Higher-order Delta W statistics (B2):** From the existing CSV data, compute variance, autocorrelation, and conditional distributions.

4. **Exact rational computation for p = 92,173:** Write a C program using GMP rationals to compute Delta W(92173) exactly. This gives a certified result without needing interval arithmetic.

5. **Test twisted Farey sums (A2):** For small chi (characters mod 3, mod 4, mod 5), compute the twisted Farey exponential sums and verify they match the predicted M_chi formula.

---

## SUMMARY OF HIGHEST-IMPACT DIRECTIONS

Ranked by potential impact and feasibility:

| Priority | Direction | Impact | Feasibility | Section |
|----------|-----------|--------|-------------|---------|
| 1 | Certify p=92,173 counterexample | High (publishability) | High (days of work) | B5 |
| 2 | Clarify classical vs. new + add references | High (credibility) | High (editorial) | C1, C3 |
| 3 | Inversion of universal formula | High (new tool) | High (straightforward) | B1 |
| 4 | Twisted Farey sums / L-functions | Very high (new theory) | Medium (research) | A2 |
| 5 | Connection to Karvonen-Zhigljavsky MMD | High (timely) | Medium (analysis) | A1 |
| 6 | Higher-order Delta W statistics | Medium (insights) | High (computation) | B2 |
| 7 | Rubinstein-Sarnak sigmoid connection | Very high (deep) | Low (requires anticorrelation) | B3 |
| 8 | Selberg class generalization | Very high (broad) | Low (substantial research) | A5 |
| 9 | Random matrix theory correlations | High (fashionable) | Medium (computation + theory) | A3 |
| 10 | Submit to Experimental Mathematics | High (career) | High (editorial work) | C4 |

---

## APPENDIX: KEY FORMULAS FOR REFERENCE

**Universal Formula (Theorem 3.3):**
Sigma_{f in F_N} e^{2 pi i m f} = M(N) + 1 + Sigma_{d|m, d>=2} d * M(floor(N/d))

**Bridge Identity (Theorem 3.1):**
Sigma_{f in F_{p-1}} e^{2 pi i p f} = M(p) + 2

**Displacement-Cosine (Theorem 3.5):**
Sigma_{f in F_{p-1}} D(f) * cos(2 pi p f) = -1 - M(p)/2

**Per-step decomposition:**
Delta W(N) = W(N-1) - W(N), where W(N) = Sigma_{j} (f_j - j/n)^2

**Sigmoid observation:**
P(Delta W(p) > 0 | M(p)/sqrt(p) in [a,b]) transitions sharply from 0 to 1 around M(p)/sqrt(p) = 0
