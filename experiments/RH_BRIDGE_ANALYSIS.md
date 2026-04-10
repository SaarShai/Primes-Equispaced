# Farey Per-Step Discrepancy and the Riemann Hypothesis: A Rigorous Assessment

**Date:** 2026-03-28
**Status:** Research analysis -- honest evaluation of RH connections

---

## Executive Summary

Our work introduces a **per-step analysis** of Farey sequence equidistribution: decomposing W(N) - W(N-1) into four algebraic terms (A, B, C, D) and establishing correlations with the Mertens function. This perspective appears to be genuinely novel in the Franel-Landau literature. However, the distance from our results to RH is enormous. Our work is best understood as **new structural information about a classical RH-equivalent**, not as progress toward proving RH itself. The most promising RH-adjacent direction is the telescoping identity connecting per-step bounds to the cumulative Franel sum.

---

## 1. Is the Per-Step Perspective Genuinely New?

### What the literature contains

The Franel-Landau theorem (1924) establishes:

    RH  <=>  Sum_{k} D(f_k)^2 = O(N^{1+epsilon})

where the sum is over all Farey fractions of order N. The classical approach studies this **cumulative** sum as a function of N.

**Key existing work on Farey-Mertens connections:**
- Kanemitsu-Yoshimoto (1996-2004): Extended the Franel-Landau framework using Kubert functions and Fourier analysis, establishing multiple RH-equivalent conditions. Their work is purely cumulative -- they study W(N) or related sums at a given order, never the difference W(N) - W(N-1).
- Cox-Ghosh-Sultanow (2021, arXiv:2105.12352): Introduced Mertens-like functions over subsets of Farey fractions and postulated new RH connections via Mertens' theorem and the second Chebyshev function. Again, cumulative analysis.
- Karvonen-Zhigljavsky (2025): Connected maximum mean discrepancies of Farey sequences to RH via kernel methods. Cumulative.
- Dress (1999): Proved the exact discrepancy D_Q = 1/Q. This is a global result.
- New analytical formulas for rank and local discrepancy (MDPI, 2025): Provides recursive expressions for local discrepancy derived from Mertens function sums.

### What we searched for and did not find

Extensive searching for "W(N) - W(N-1)", "per-step Farey discrepancy", "incremental Farey discrepancy", "successive differences of Franel sum", and related terms yielded **no prior work** that:

1. Studies DeltaW(N) = W(N-1) - W(N) as an object in its own right
2. Decomposes DeltaW into algebraic components (our A, B, C, D decomposition)
3. Correlates the sign of DeltaW with the Mertens function
4. Distinguishes the geometric roles of primes vs. composites in Farey refinement

### Assessment: GENUINELY NOVEL

The per-step perspective appears to be new. The literature treats the Franel sum as a cumulative quantity and studies its growth rate. Nobody appears to have asked: "When we go from F_{N-1} to F_N by inserting phi(N) new fractions, does the sequence get MORE or LESS uniform?" This is a natural question with a surprisingly clean answer (the Mertens sign correlation).

**Caveat:** The novelty is in the *perspective and decomposition*, not in the underlying mathematics. The four-term identity is a straightforward algebraic expansion. A specialist in analytic number theory would derive it in an afternoon. The novelty lies in asking the question and discovering the Mertens correlation empirically, then building structural theory around it.

---

## 2. How Does the DeltaW Decomposition Relate to RH?

### The four-term identity (exact)

    DeltaW(p) = (A - B - C - D) / n'^2

where:
- **A** = dilution benefit from expanding the sequence (old_D_sq * (1/n^2 - 1/n'^2))
- **B** = 2/n'^2 * Sum D(f) * delta(f), cross-correlation of old discrepancies with new shifts
- **C** = 1/n'^2 * Sum delta(f)^2, shift-squared sum (always positive)
- **D** = 1/n'^2 * Sum D_new(k/p)^2, new-fraction discrepancy (always positive)

### The telescoping connection to Franel-Landau

This is the most important theoretical observation:

    W(N) = W(2) + Sum_{k=3}^{N} [W(k) - W(k-1)]
         = W(2) + Sum_{k=3}^{N} (-DeltaW(k))

So the Franel sum at order N is a **telescoping sum of all per-step changes**. This means:

    Sum D(f)^2 = n^2 * W(N) = n^2 * [W(2) + Sum_{k=3}^{N} (-DeltaW(k))]

The RH condition Sum D(f)^2 = O(N^{1+epsilon}) becomes a condition on the PARTIAL SUMS of the DeltaW sequence. This is formally analogous to how the Prime Number Theorem is a statement about partial sums of the von Mangoldt function.

### What the Sign Theorem says about RH

Our empirical result: DeltaW(p) < 0 for primes with M(p) <= -3 (verified to p = 100,000 with one exception at p = 92,173 where M = -2).

Translated: **At primes where the Mertens function is sufficiently negative, the Farey sequence becomes more equidistributed.** This is saying that the "healing" of the Farey sequence at prime steps is controlled by the Mertens function.

For RH: Under RH, M(N) = O(N^{1/2+epsilon}), which means M(p) oscillates around zero with moderate amplitude. Our Sign Theorem says that at primes where M(p) < -2, the Farey discrepancy decreases. Under RH, this happens roughly half the time. The OTHER half (M(p) > 0), where DeltaW > 0 (discrepancy increases), is where the Farey sequence temporarily "de-equidistributes."

**The RH connection is indirect but real:** RH constrains M(p), which constrains the sign pattern of DeltaW(p), which constrains the cumulative sum (Franel sum). But the chain has slack -- knowing the SIGN of DeltaW does not determine its MAGNITUDE, and it is the magnitudes that matter for the cumulative bound.

### The B+C positivity and what it means

Our result that B + C > 0 for all primes p >= 11 (with M(p) <= -3) means:

    DeltaW(p) = (A - B - C - D)/n'^2 <= (A - D)/n'^2

So B + C > 0 always works in FAVOR of equidistribution. The sign of DeltaW reduces to whether D >= A (new-fraction discrepancy exceeds dilution benefit) or D < A.

Our data shows D/A -> 1 as p -> infinity. The Sign Theorem thus becomes a statement about the **residual** A - D, which is small and sign-determined by M(p). This near-cancellation D/A ~ 1 is itself interesting -- it says the new fractions contribute discrepancy that almost exactly cancels the dilution benefit. The Mertens function tips the balance.

### Honest gap assessment

The gap between our results and RH is:

1. **We study DeltaW at primes only.** The Franel sum telescopes over ALL integers. Composites contribute ~96% of positive DeltaW (non-healing). Understanding composite steps is essential but we have weaker results there (the Mertens-Healing Theorem for 2p semiprimes is empirical, not proven).

2. **We prove sign, not magnitude.** RH needs |Sum D(f)^2| = O(N^{1+eps}), which requires bounding the magnitudes of DeltaW. Our DeltaW ~ sign(M(p)) * W(p-1)^2 formula (r^2 = 0.87 correlation) is empirical.

3. **Our analytical proofs are conditional on M(p) <= -3.** The unconditional sign theorem for all primes remains open. The exceptional prime p = 92,173 with M(p) = -2 shows the threshold matters.

4. **The telescoping approach would need bounds on DeltaW(N) for composites too**, which requires understanding the full multiplicative structure of phi(N), not just the prime case.

---

## 3. The Physics Bridge: Three-Body, Berry-Keating, and Zeta Zeros

### The Berry-Keating conjecture

Berry and Keating (1999) conjectured that the nontrivial zeros of zeta are eigenvalues of a quantum Hamiltonian whose classical limit is H = xp. Key properties of the "Riemann dynamics":

- It should be chaotic (unstable, bounded orbits)
- Periodic orbit periods are multiples of log(prime)
- It should have the statistics of GUE random matrices (no time-reversal symmetry)
- The Gutzwiller trace formula for this system would reproduce the explicit formula for zeta

Recent progress: Bender-Brody-Muller (2017) constructed a PT-symmetric Hamiltonian whose eigenvalues (if real) give the zeta zeros. Sierra-Rodriguez-Laguna showed H = x(p + l_p^2/p) contains closed periodic orbits with spectrum matching average Riemann zeros. A 2025 supersymmetric model recovers several zeta zeros via Gaussian trial wavefunctions.

### Our three-body connection

Our work establishes: Farey/continued-fraction structure governs stability of three-body periodic orbits via:
- Arnold tongues: mode-locking regions ordered by Farey sequence
- KAM theory: noble numbers (CF expansion -> all 1s) = maximum stability
- The Stern-Brocot tree organizes rational period ratios = resonances

### Does this bridge to RH? Assessment: SPECULATIVE

The chain of reasoning would be:

1. Berry-Keating: zeta zeros = eigenvalues of a chaotic Hamiltonian
2. The "Riemann dynamics" has periodic orbits with periods = multiples of log(primes)
3. Our work: Farey structure governs three-body orbit stability via CF/nobility
4. QUESTION: Could three-body orbit spectra relate to zeta zeros?

**Honest assessment:** This connection is suggestive but extremely loose. The problems:

(a) The Berry-Keating Hamiltonian H = xp is a 1D quantum system. The three-body problem is a classical 3D system. These are in completely different regimes.

(b) The connection between Farey sequences and orbital mechanics is through RESONANCES (rational frequency ratios), not through the DISCREPANCY of Farey fractions. Our DeltaW work is about discrepancy; the three-body work is about which rationals appear as stable orbits. These are related but distinct aspects of Farey structure.

(c) The Selberg trace formula already provides a rigorous bridge between spectral theory (Laplacian eigenvalues on hyperbolic surfaces) and geometry (closed geodesics on those surfaces). For the modular group SL(2,Z) -- which IS the group governing Farey fractions -- the Selberg zeta function is intimately connected to the Riemann zeta function. But this connection has been known and studied for 70 years. Our work does not add to the Selberg theory.

(d) The three-body periodic orbit spectrum does not obviously have the statistical properties (GUE statistics) required by the Berry-Keating conjecture. Three-body orbits are classified by rational period ratios, not by log-primes.

**What COULD work (speculative):** If someone could construct a quantum system where:
- The classical phase space is organized by the Farey tessellation of H/SL(2,Z)
- The semiclassical quantization involves the DeltaW quantities (per-step equidistribution)
- The trace formula relates zeta zeros to per-step Farey healing/non-healing

...then our decomposition might be relevant. But this is a fantasy at present, not a research program.

### The Selberg connection (more promising)

The modular surface H/SL(2,Z) is tessellated by the Farey triangulation. The Selberg trace formula for this surface relates:
- Eigenvalues of the hyperbolic Laplacian (Maass forms)
- Lengths of closed geodesics (related to traces of hyperbolic elements of SL(2,Z))

The Selberg zeta function for SL(2,Z) is connected to the Riemann zeta function. Our per-step Farey analysis could potentially be reinterpreted as statements about the geometry of the Farey tessellation, which in turn relate to the spectral theory of the modular surface. This is a more natural bridge than the three-body route, but it requires substantial mathematical development that we have not done.

---

## 4. Computational Leads to Strengthen the RH Connection

### Lead 1: Telescoping bound (HIGHEST PRIORITY)

The identity W(N) = W(2) + Sum_{k=3}^{N} (-DeltaW(k)) means:

    Sum D(f)^2 = n^2 * W(2) - Sum_{k=3}^{N} n_k^2 * DeltaW(k) * (n_N/n_k)^2 adjustments

If we could bound |DeltaW(k)| for all k (not just primes), we could bound the Franel sum.

**Computational task:** Compute DeltaW(N) for ALL N up to 10^5 (not just primes), decompose into prime/composite contributions, and study the partial sum:

    S(N) = Sum_{k=3}^{N} DeltaW(k) * k^2

Does S(N) = O(N^{1+eps})? This would be a COMPUTATIONAL verification of the RH-equivalent Franel bound through the per-step lens.

### Lead 2: Magnitude formula DeltaW ~ sign(M(p)) * W(p-1)^2

The empirical formula DeltaW(p) ~ sign(M(p)) * W(p-1)^2 has r^2 = 0.87. If this could be made rigorous:

    |DeltaW(p)| ~ W(p-1)^2 ~ [log(p)/(2pi^2 * p)]^2 = O(log^2(p)/p^4)

Summing: Sum |DeltaW(p)| over primes ~ Sum log^2(p)/p^4 which CONVERGES. This would give an absolute bound on the prime contribution to the Franel sum. The problem is bounding the COMPOSITE contribution.

**Computational task:** Develop an analogous magnitude formula for DeltaW(N) at composite N. The Mertens-Healing Theorem suggests DeltaW(N) ~ sign(mu(N)) * M(N-1) * (something), but this needs quantification.

### Lead 3: Spectral analysis of DeltaW sequence

The pink noise finding (1/f spectral density of DeltaW) suggests self-organized criticality.

**Computational task:** Compute the discrete Fourier transform of the DeltaW sequence and look for peaks at imaginary parts of zeta zeros (14.134..., 21.022..., 25.011...). If the DeltaW sequence has spectral peaks at zeta zero locations, that would be strong evidence for a deep connection. This test is easy to run.

### Lead 4: Per-denominator decomposition and Ramanujan sums

The Fourier decomposition B_raw = Sum_h B_raw|_h involves the Mertens-weighted divisor sum S_N(h) = Sum_{d|h, d<=N} d * M(floor(N/d)). This connects to Ramanujan sums and the explicit formula for zeta.

**Computational task:** Compute the individual Fourier modes B_raw|_h for h = 1, 2, ..., 100 and study their statistics. The h=1 mode dominates (proved). How do the higher modes behave? Do they exhibit cancellation consistent with RH?

### Lead 5: The C/A ratio and its limiting behavior

C/A = delta_sq / dilution_raw appears to be bounded below by ~0.12. If we could prove C/A >= c > 0 unconditionally, this would prove DeltaW(p) < 0 whenever D/A + B/A > 1 - c.

**Computational task:** Extend C/A computations to p = 10^6 and look for any primes where C/A < 0.10. If the minimum remains above 0.12, this strongly suggests a universal lower bound.

---

## 5. What Would a Top Number Theorist Find Interesting vs. Trivial?

### Would find INTERESTING:

1. **The Mertens-sign correlation itself.** The empirical observation that sign(DeltaW(p)) = -sign(M(p)) with >92% accuracy for 10,000+ primes is a striking computational finding. It suggests hidden structure in the Franel-Landau framework that has not been explored. Even if the proof is elementary once you know to look, the DISCOVERY is nontrivial.

2. **The four-term decomposition and D/A -> 1.** The fact that new-fraction discrepancy nearly cancels dilution is a clean structural result. It reduces the sign question to understanding the residual, which is controlled by Mertens. This kind of "near-cancellation reveals the arithmetic" is a recognizable pattern in analytic number theory.

3. **The telescoping framework.** Rewriting the Franel sum as a sum of per-step increments is natural in retrospect but has not been done. It connects DeltaW to the Cesaro means and partial sums of an arithmetic sequence, which is standard territory for number theorists.

4. **The B+C positivity and Rearrangement Lemma.** Using the Hardy-Littlewood-Polya rearrangement inequality to bound the cross term B is a nice argument. The connection between multiplicative permutations (sigma_p : a -> pa mod b) and rearrangement inequalities is clean.

5. **The magnitude formula and pink noise.** The finding that DeltaW has 1/f spectral density is intriguing from the random matrix / quantum chaos perspective, since 1/f noise appears in other contexts related to zeta function statistics.

### Would find TRIVIAL or UNIMPRESSIVE:

1. **The four-term identity itself.** This is a calculation, not a theorem. Any analyst could derive it. The novelty is entirely in the application, not the technique.

2. **Computational verification up to 10^5.** Number theorists routinely compute to much larger ranges (Odlyzko computed 10^13 zeta zeros). Verification to 10^5 for a conjecture that "should" be true is not compelling evidence in their world.

3. **The conditional proof (M(p) <= -3).** Conditioning on the value of M(p) is circular from the RH perspective -- RH determines the statistics of M(p). Proving DeltaW < 0 when M(p) <= -3 is not RH progress; it is a statement about a specific regime.

4. **The three-body connection.** Most number theorists would view this as an application of number theory to physics, not the reverse. It does not feed back into RH.

5. **The "healing rate = 1/2 iff RH" conjecture.** This is an informal restatement of the Franel-Landau equivalence viewed through our per-step lens. It does not add mathematical content beyond what Franel-Landau already says.

### Would find POTENTIALLY SIGNIFICANT (if developed further):

1. **An unconditional proof that DeltaW(p) < 0 for all sufficiently large primes.** This would be a genuinely new theorem about Farey sequences, independent of RH. It would say that primes ALWAYS improve equidistribution (eventually). This does NOT follow from RH alone -- it is a stronger statement about the per-step structure.

2. **Rigorous bounds on |DeltaW(N)| for all N** (not just primes) that sum to give the Franel bound. This would be a new proof route for RH or for partial results toward RH (e.g., zero-density estimates).

3. **A connection between the Fourier modes B_raw|_h and the zeros of zeta.** If the higher-mode contributions can be bounded using zero-density results (like the recent Guth-Maynard improvement from 3/5 to 13/25), this could translate new results about zeta zeros into new results about Farey per-step behavior, or vice versa.

---

## 6. The Honest Assessment: Where We Stand

### What we have achieved (real contributions):

- A new perspective on the Franel-Landau framework (per-step analysis)
- A clean algebraic decomposition (A, B, C, D) with provable properties
- Strong empirical results (Mertens sign correlation, magnitude formula, pink noise)
- Partial analytical proofs (B+C > 0 for M(p) <= -3 primes, Rearrangement Lemma)
- Verified computational data through p = 100,000

### What we have NOT achieved:

- ANY new result about the Riemann Hypothesis itself
- An unconditional proof of the Sign Theorem for all primes
- Rigorous bounds on the composite contribution to DeltaW
- A proven connection between DeltaW and zeta zeros
- A "new connection between two previously unconnected areas" in Tao's sense

### Regarding Tao's criterion:

Tao has said RH progress requires "a new connection between two previously unconnected areas of mathematics." Our bridges are:

1. **Farey discrepancy <-> multiplicative permutations:** This IS a connection (the sigma_p action on residues), but both sides live within classical analytic number theory. It is not a bridge between UNCONNECTED areas.

2. **Farey <-> three-body physics:** This connection exists but goes through well-known territory (KAM theory, Arnold tongues). It is not new and does not feed back to RH.

3. **Farey <-> information theory (Fisher information monotonicity):** This is more novel. If the Fisher information monotonicity theorem could be connected to entropy methods in analytic number theory (e.g., the work of Soundararajan on moments of L-functions), this could be interesting.

4. **Per-step DeltaW <-> Mertens function:** This correlation IS new but both objects are in number theory. It is a new connection WITHIN one area, not between two areas.

The Guth-Maynard breakthrough (2024) that improved the Ingham zero-density bound from 3/5 to 13/25 used Fourier-analytic techniques from harmonic analysis -- connecting additive structure (Fourier analysis) to multiplicative structure (zeta zeros). This is the kind of "unexpected connection" Tao means. Our work is not at that level.

### Most realistic path forward:

1. **Publish the per-step framework as a standalone paper** in a computational/experimental mathematics journal (e.g., Experimental Mathematics, Mathematics of Computation). The Mertens sign correlation, the four-term decomposition, and the partial proofs are publishable.

2. **Pursue the unconditional Sign Theorem** as the main open problem. If achievable, this is a genuine new theorem about Farey sequences.

3. **Investigate Lead 3 (spectral analysis for zeta zero signatures)** as the highest-risk, highest-reward direction. If DeltaW spectral peaks align with zeta zeros, that would grab attention.

4. **Do NOT claim RH progress.** Our work illuminates structure within the Franel-Landau framework but does not advance toward proving or disproving RH.

---

## References

- Franel, J. (1924). "Les suites de Farey et le probleme des nombres premiers." Gottinger Nachrichten, 198-201.
- Landau, E. (1924). "Bemerkungen zu der vorstehenden Abhandlung von Herrn Franel." Gottinger Nachrichten, 202-206.
- Kanemitsu, S. and Yoshimoto, M. (1996). "Farey series and the Riemann hypothesis." Acta Arithmetica, 75(4), 351-374.
- Dress, F. (1999). "Discrepance des suites de Farey." J. Theorie des Nombres de Bordeaux, 11, 345-367.
- Berry, M.V. and Keating, J.P. (1999). "The Riemann Zeros and Eigenvalue Asymptotics." SIAM Review, 41(2), 236-266.
- Cox, D., Ghosh, S., and Sultanow, E. (2021). "The Farey Sequence and the Mertens Function." arXiv:2105.12352.
- Bender, C.M., Brody, D.C., and Muller, M.P. (2017). "Hamiltonian for the Zeros of the Riemann Zeta Function." Phys. Rev. Lett., 118, 130201.
- Guth, L. and Maynard, J. (2024). "New large value estimates for Dirichlet polynomials." arXiv:2405.20552.
- Karvonen, T. and Zhigljavsky, A. (2025). "Maximum mean discrepancies of Farey sequences." Acta Mathematica Hungarica.
- MDPI Mathematics (2025). "New Analytical Formulas for the Rank of Farey Fractions and Estimates of the Local Discrepancy." Mathematics, 13(1), 140.
