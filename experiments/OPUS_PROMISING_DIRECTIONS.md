# Strategic Research Directions — Opus Analysis
# Date: 2026-04-11
# Context: Full review of TOP_DISCOVERIES, MASTER_TABLE, Strategic_Priorities, Lessons_Learned, 
#          Paper C outline, Session 11 handoff, recent M1 Max results, K=5 attempt

---

## QUESTION 1: MOST PROMISING DIRECTIONS

### Direction 1: DPAC Conjecture Paper (Avoidance Phenomenon)

**(a) What specifically to do:**
Write a standalone paper for Experimental Mathematics stating the DPAC conjecture precisely, presenting:
- The 800 interval certificates (K=10,20,50,100 at zeros j=1..200)
- The 4.4-16.1x avoidance ratio with statistical analysis
- The double obstruction mechanism (modulus+phase, r=0.063)
- The density-zero Theorem A' (unconditional, via Langer count)
- K<=4 unconditional theorem as warm-up
- Extend certificates to K=200 (pure computation, no new theory needed)

This is NOT Paper C. This is a focused conjecture paper: "here is a new phenomenon, here is overwhelming evidence, here is partial structural explanation, here are unconditional results for small K."

**(b) Probability of success:** 85% for acceptance at Experimental Mathematics. The journal exists for exactly this: computationally-supported conjectures with rigorous backing evidence. The novelty is undeniable (nobody has stated DPAC). Risk: referee says "not enough theory" -- mitigated by Theorem A', double obstruction, and the K<=4 proof.

**(c) What it would mean:** Establishes the avoidance phenomenon in the literature. Creates a named conjecture others can attack. Opens a research direction at the intersection of Dirichlet polynomial zero theory and zeta zero statistics. Gets cited by anyone working on non-vanishing of truncated Euler products.

**(d) Estimated effort:** 40-60 hours. Content exists in experiment files. Main work: assembly, figures, polishing the density-zero proof, extending certificates to K=200 (overnight computation).

---

### Direction 2: K=5 Non-Vanishing (Pushing the Unconditional Frontier)

**(a) What specifically to do:**
The deepseek K=5 attempt FAILED -- the argument is hand-waving at the critical step. The problem: for K=5, c_5(s) = -(2^{-s} + 3^{-s} + 5^{-s}), and we need |c_5(rho)| > 0 for all zeta zeros. The K<=4 proof works because |1/sqrt(2) - 1/sqrt(3)| > 0 (reverse triangle inequality with TWO terms). For THREE terms, we need the zero set of the map (theta_1, theta_2, theta_3) -> A*e^{i*theta_1} + B*e^{i*theta_2} + C*e^{i*theta_3} = 0 (with A=1/sqrt(2), B=1/sqrt(3), C=1/sqrt(5)) to be avoidable.

Specific attack plan:
1. COMPUTE: For which (theta_2, theta_3, theta_5) does the sum vanish? This is a 1-dimensional curve in T^3 (solve for theta_2 given theta_3, theta_5 satisfying |sum|=0). Map it explicitly.
2. CHECK: Does the Kronecker flow (t*log2, t*log3, t*log5) mod 2pi ever hit this curve? The flow is equidistributed on T^3 (Weyl), so it comes arbitrarily close. The question is: does it HIT? For a 1D curve in T^3, the flow is a 1D curve too -- generically they don't intersect in T^3 (dimension count: 1+1 < 3).
3. PROVE: The zero set of |c_5(1/2+it)| is a countable set of t-values (isolated zeros of a real-analytic function on R). Show this set has measure zero and intersects {gamma_k} in at most finitely many points. This might follow from the Q-linear independence of {log 2, log 3, log 5, gamma_k} -- but this is a hard transcendence problem.

Alternative: Instead of proving c_5(rho) != 0 for ALL zeros, prove it for all but finitely many. The Langer/Moreno framework (exponential polynomials with rationally independent exponents have only finitely many common zeros with any fixed exponential polynomial) might apply here if properly formulated.

**(b) Probability of success:** 30% for "all zeros," 65% for "all but finitely many." The dimension-counting argument is heuristic but the Langer approach for the weaker statement is plausible. The hard case: maybe there exists one specific gamma_k where the phases conspire. Computation can check the first 10,000 zeros trivially.

**(c) What it would mean:** K=5 is the first case where more than 2 primes contribute. Going from K=4 to K=5 crosses a structural barrier (two vectors -> three vectors). If proved, the induction to K=6,7,... becomes plausible (each additional prime adds a dimension to the flow but only a codimension-1 constraint). This could eventually yield c_K(rho) != 0 for all K, which combined with |c_K(rho)| -> infinity would give a new proof of zeta zero detection.

**(d) Estimated effort:** 20-30 hours for computational exploration + dimension counting heuristic. 60+ hours for rigorous proof. Delegate: deepseek for the Langer reformulation, Python for the zero-set computation, mpmath for checking first 10K zeros at K=5.

---

### Direction 3: Double Obstruction -> Structural Density-Zero Proof

**(a) What specifically to do:**
Currently Theorem A' says "all but O(T) zeros have c_K(rho) != 0" via the Langer count of exponential polynomial zeros. This is clean but says nothing about WHY the avoidance happens. The double obstruction (modulus condition AND phase condition, with r=0.063 correlation) suggests a STRUCTURAL reason.

Specific program:
1. FORMALIZE: Define the modulus barrier M(K,gamma) = min over phase assignments of |c_K(1/2+igamma)|. This is a deterministic function of gamma.
2. COMPUTE: M(K,gamma) for K=10,20,50,100 at gamma=gamma_1,...,gamma_200 and at 10,000 generic gamma values. Compare distributions.
3. PROVE: Under GRH, M(K,gamma_j) >= f(K) for some explicit f(K) > 0, using the arithmetic structure of the primes at the zero (i.e., the phases t*log(p) mod 2pi at t=gamma_j have specific statistical properties due to being a zeta zero).
4. Key insight to exploit: AT a zeta zero, sum mu(k)k^{-rho} is trying to approximate 1/zeta(rho) = 0 from below. But the truncation c_K stops early, and the MISMATCH between the truncated and infinite product creates a guaranteed gap. Can we quantify this gap?

**(b) Probability of success:** 45%. The mismatch idea is promising but quantifying it rigorously requires control over the tail of the Euler product at rho, which is exactly what nobody has. The empirical double obstruction is very clean (r=0.063 means the two conditions are nearly independent), which suggests a proof should decompose into two independent steps.

**(c) What it would mean:** A density-zero result with STRUCTURAL content (not just counting) would be genuinely new in analytic number theory. It would explain the avoidance phenomenon theoretically, not just observe it. This is the highest-value theory goal after K=5.

**(d) Estimated effort:** 40-80 hours. Heavy theory. Delegate: deepseek for the Euler product tail analysis, Codex for the structural argument, computation for the modulus barrier data.

---

### Direction 4: Batch Spectroscope for Automorphic L-Functions

**(a) What specifically to do:**
Currently batch spectroscope handles Dirichlet characters (18s for 10K at conductor q). Extend to:
1. Weight-2 modular forms (elliptic curves): a_p coefficients from LMFDB. Run the spectroscope on all curves of conductor <= 1000. Detect their L-function zeros.
2. Maass forms: eigenvalues from LMFDB. Test whether the spectroscope detects Maass form L-function zeros.
3. Symmetric power L-functions: L(s, sym^2 f) for modular forms f. These have Euler products of degree 3, so the spectroscope should still work but with modified coefficients.

The C implementation already handles the core Fourier transform. The extension is: (a) compute the right coefficients a_p for each L-function type, (b) feed them to the existing spectroscope, (c) check detection.

**(b) Probability of success:** 75% for elliptic curves (we already have partial EC results at 3.0x). 50% for Maass forms (different analytic behavior). 35% for symmetric powers (degree 3 Euler products may need longer sums).

**(c) What it would mean:** Demonstrating that the spectroscope works across the Langlands program would be a significant computational achievement. It would validate the universality theorem in practice (not just for Dirichlet characters) and position the batch tool as genuinely useful for L-function computation. The LMFDB team would care -- they compute zeros by other methods and could use ours for cross-validation.

**(d) Estimated effort:** 30-50 hours. Mostly computational. Download LMFDB data, modify coefficient computation, run experiments. The C infrastructure exists.

---

### Direction 5: Unconditional Detection Without GRH

**(a) What specifically to do:**
Currently: Theorem B (GRH detection) is conditional. The dichotomy theorem is unconditional but says "detects the rightmost zero" (wherever it is). Can we get unconditional detection of SPECIFIC zeros?

Approach: The 800 interval certificates are already unconditional -- they prove c_K(rho_j) != 0 at specific zeros using interval arithmetic. The spectroscope detection at those zeros follows unconditionally from c_K(rho_j) != 0 + explicit formula (which is unconditional for the truncated version). 

So the argument would be: for each certified zero rho_j, the spectroscope peak at gamma_j exceeds the noise floor for N sufficiently large, with an EXPLICIT N_0(gamma_j). This is a finite computation for each zero. The result: "The Mertens spectroscope unconditionally detects the first 200 (or 800) zeta zeros."

This is weaker than the GRH theorem (which gets ALL zeros) but has the enormous advantage of being unconditional. And 800 zeros is far more than any referee would dismiss.

**(b) Probability of success:** 80%. The main subtlety: making the "sufficiently large N" explicit. The truncated explicit formula has effective error bounds (Goldston, Gonek, et al.), and combining with the interval certificates should close the argument.

**(c) What it would mean:** First unconditional spectroscope detection theorem for specific zeros. Bridges the gap between K<=4 (unconditional but says nothing about detection) and Theorem B (complete detection but conditional). Would be a strong addition to Paper C.

**(d) Estimated effort:** 20-30 hours. Delegate: deepseek for the effective error bound, Python for computing explicit N_0 for each of the 800 zeros.

---

### Direction 6: Connect Avoidance to LI / GUE

**(a) What specifically to do:**
The Linear Independence conjecture (LI) says the positive imaginary parts of zeta zeros are linearly independent over Q. The GUE hypothesis says local zero statistics match random matrix theory. Both are about the DISTRIBUTION of zeros.

DPAC says c_K zeros AVOID zeta zeros. Is there a logical relationship?

Test 1: If LI holds, does DPAC follow? The phases t*log(p) at t=gamma_j would be "generic" on the torus (by LI + Kronecker), making it unlikely that c_K(rho_j)=0 (which requires specific phase alignment). This would give: LI implies DPAC (for fixed K, all but finitely many zeros).

Test 2: Does GUE pair correlation predict the avoidance ratio? The 4.4-16.1x gap between min|c_K| at zeta zeros vs generic points should have a GUE-theoretic explanation if the avoidance is a consequence of local repulsion statistics.

Test 3: Does Montgomery's pair correlation function predict the spacing between c_K zeros and zeta zeros? Compute the pair correlation of the combined set {zeta zeros} union {c_K zeros} and compare to GUE.

**(b) Probability of success:** 50% for the LI implication (this is plausible and would be a nice theorem). 30% for the GUE connection (less clear theoretically). 60% for the pair correlation computation (pure numerics).

**(c) What it would mean:** Connecting DPAC to LI would embed the avoidance phenomenon in the mainstream conjecture landscape. Connecting to GUE would link it to random matrix theory. Either would dramatically increase the paper's appeal.

**(d) Estimated effort:** 30-40 hours. The LI implication is a theory question (delegate to deepseek/Codex). The GUE/pair correlation tests are computational.

---

### PRIORITY RANKING (Directions for Q1):

| Rank | Direction | Prob | Impact | Effort | ROI |
|------|-----------|------|--------|--------|-----|
| 1 | DPAC paper (Experimental Mathematics) | 85% | HIGH | 40-60h | BEST |
| 2 | Unconditional detection of 800 zeros | 80% | HIGH | 20-30h | EXCELLENT |
| 3 | K=5 non-vanishing ("all but finitely many") | 65% | VERY HIGH | 30-60h | GOOD |
| 4 | LI implies DPAC | 50% | VERY HIGH | 30-40h | GOOD |
| 5 | Batch for automorphic L-functions | 75% | MEDIUM | 30-50h | GOOD |
| 6 | Double obstruction structural proof | 45% | VERY HIGH | 40-80h | MODERATE |

---

## QUESTION 2: EASY WINS

### Easy Win 1: K<=4 Note for American Mathematical Monthly

**(a) What to do:** Write a 4-6 page expository note. The result: |c_K(rho)| >= |1/sqrt(2) - 1/sqrt(3)| > 0 for all zeta zeros, all K<=4. The proof is one line (reverse triangle inequality + mu(k) values). Frame it as: "A simple observation about truncated reciprocals of zeta at its zeros." Include: the definition, the proof, numerical illustrations, connection to the detection problem, open question (does this extend to K=5?).

**(b) Effort:** 8-12 hours. The proof is done. Just needs clean writing and context.

**(c) Deliverable:** Accepted AMM note. Door-opener publication. Shows community you can prove clean theorems.

---

### Easy Win 2: Extend Certificates to K=500 Zeros

**(a) What to do:** The interval arithmetic certification pipeline is 100% reliable (800/800 success rate). Run it for K=10,20,50,100 at zeros j=1..500. This is pure computation -- no new theory, no risk of failure.

**(b) Effort:** 4-8 hours (mostly waiting for computation). The code exists.

**(c) Deliverable:** "2000 rigorous interval certificates" instead of "800." Strengthens every paper that cites the certificates. Stronger evidence for DPAC (500 zeros instead of 200).

---

### Easy Win 3: Spectroscope on Primes in Arithmetic Progressions

**(a) What to do:** Run the existing spectroscope on primes p = a mod q for various (a,q). The universality theorem predicts detection for any subset with divergent reciprocal sum. Verify: (1) primes = 1 mod 4 detect zeta zeros, (2) primes = 3 mod 4 detect zeta zeros, (3) primes = 1 mod 3 detect Dirichlet L(s, chi_3) zeros. Tabulate detection ratios. Compare to full prime set.

**(b) Effort:** 6-10 hours. The spectroscope code exists. Just need to filter the input primes and run.

**(c) Deliverable:** Table for Paper C showing universality in action. Specific numbers for the referee: "primes = 1 mod 4 give 2.8x detection, primes = 3 mod 4 give 3.1x" (or whatever the data shows). Makes universality theorem concrete, not abstract.

---

### Easy Win 4: pip-installable Spectroscope Package

**(a) What to do:** Package the Python spectroscope (not the C batch version) as a pip-installable tool. Include: (1) mertens_spectroscope(primes, gamma_range), (2) detection_zscores(primes, known_zeros), (3) interval_certificate(K, zero_index), (4) avoidance_ratio(K, n_zeros). Write a 1-page README with examples.

**(b) Effort:** 10-15 hours. The code exists in scattered scripts. Main work: refactor into package structure, add docstrings, write setup.py, test.

**(c) Deliverable:** pip install farey-spectroscope. Lowers barrier for anyone to reproduce results. Credibility artifact. Link in every paper.

---

### Easy Win 5: Blog Post / Expository Article

**(a) What to do:** Write a 2000-word blog post: "How to Hear Riemann Zeros in Prime Numbers." Cover: what the spectroscope does (with a figure), the K<=4 theorem (accessible proof), the avoidance mystery (with data), and the universality result (philosophical implications). Target: mathematical audience but not experts. Post on a personal site or arXiv expository section.

**(b) Effort:** 6-10 hours.

**(c) Deliverable:** Public-facing explanation that generates interest before the formal papers appear. Shareable link for email outreach to Rudnick, Keating, Maynard, etc.

---

### Easy Win 6: Lean Mathlib PR for Farey Cardinality

**(a) What to do:** Extract the Farey cardinality lemma (|F_N| = 1 + sum_{k=1}^{N} phi(k)) from the 434 Lean results. Format it for Mathlib contribution standards. Submit PR.

**(b) Effort:** 8-12 hours (mostly reformatting to Mathlib style, which is strict).

**(c) Deliverable:** Accepted Mathlib contribution. Direct connection to Buzzard/Kontorovich community. Credibility for the full Lean library.

---

### EASY WIN RANKING:

| Rank | Win | Effort | Impact |
|------|-----|--------|--------|
| 1 | AMM note (K<=4) | 8-12h | Publication |
| 2 | Extend to 500 zeros | 4-8h | Strengthens all papers |
| 3 | Primes in progressions | 6-10h | Paper C table |
| 4 | Lean Mathlib PR | 8-12h | Community credibility |
| 5 | pip package | 10-15h | Reproducibility |
| 6 | Blog post | 6-10h | Outreach |

---

## QUESTION 3: CROSS-DOMAIN APPLICATIONS

### Application 1: Universality + Sieve Theory (Maynard-Tao)

**(a) Tool:** Universality theorem (any sum 1/p = infinity subset detects all zeros).

**(b) Area:** Bounded gaps between primes (Maynard-Tao weights).

**(c) Specific experiment:** The Maynard-Tao theorem produces infinitely many primes in intervals [x, x+C*log(x)] for some effective C. These primes form a subset P_MT with sum 1/p = infinity (since there are >> x/log^2(x) such primes up to x). By universality, P_MT detects all zeta zeros. 

Run the spectroscope on:
1. Primes that are first elements of twin-prime pairs (p where p+2 is also prime)
2. Primes in clusters of 3+ (p, p+2, p+6 or similar admissible tuples)
3. Primes that are NOT part of any close pair (isolated primes, gaps > 2*log(p))

Compare detection ratios. If twin primes give BETTER detection than isolated primes, this reveals that "clustered" primes carry MORE zero information per prime -- a new quantitative refinement of universality.

**(d) What finding would mean:** If clustered primes give stronger detection: the spectroscope provides a new lens on the Maynard-Tao machinery. The sieve weights that select clustered primes are AMPLIFYING the zeta zero signal. This connects two of the biggest topics in modern analytic number theory (bounded gaps and zero detection) in a concrete, computational way. Maynard himself would likely be interested (he's at Oxford, computationally minded).

If detection is EQUAL regardless of clustering: universality is "flat" -- all primes contribute equally regardless of local gap structure. This is also interesting (it means the zero information is truly uniformly distributed).

---

### Application 2: Spectroscope as Black-Box Conjecture Tester

**(a) Tool:** The spectroscope framework (input: any arithmetic sequence a(n), output: does it detect zeta zeros?).

**(b) Area:** Classification of arithmetic functions by their "zero content."

**(c) Specific experiments:**
1. **Ramanujan tau function tau(n):** This is the Fourier coefficient of the weight-12 cusp form. Does sum tau(p)/p^s detect Ramanujan L-function zeros? (Should work -- tau is a Hecke eigenform.)
2. **Partition function p(n):** Already tested and FAILS (no oscillation). But what about p(n) mod 5? Ramanujan congruences say p(5n+4) = 0 mod 5. Does the sequence p(n) mod 5 (which oscillates!) detect anything? The M5 partition-mod-5 experiment exists -- check results.
3. **Sum-of-divisors sigma(n):** Known to NOT detect zeros (Session 11: sigma FAILS). But what about the ERROR TERM in the average of sigma(n)? Define E(x) = sum_{n<=x} sigma(n) - pi^2*x^2/12. Does E(x) detect zeta zeros?
4. **Liouville lambda(n):** The spectroscope already works (Session 11). But what about PRODUCTS lambda(n)*lambda(n+1)? This relates to Chowla's conjecture. If the product sequence detects zeros, it reveals the zero structure in consecutive correlations.
5. **Number of representations as sum of 2 squares r_2(n):** Already FAILS (Gauss circle). But what about r_2(n) restricted to prime arguments? r_2(p) = 8*(1+chi_{-4}(p)), so this reduces to the chi_{-4} spectroscope, which SHOULD work.

**(d) What finding would mean:** A systematic classification of "which arithmetic functions detect which L-function zeros" would be a new organizational principle. The meta-theorem (needs Euler insertion + explicit formula + oscillation) predicts the answer, but testing it across many functions either validates the meta-theorem or reveals exceptions. Any exception would be a discovery.

---

### Application 3: Avoidance Phenomenon for Other Dirichlet Polynomials

**(a) Tool:** DPAC conjecture framework + interval certification pipeline.

**(b) Area:** General non-vanishing theory for Dirichlet polynomials.

**(c) Specific experiments:**
1. Replace mu(k) with lambda(k) (Liouville function): Does c_K^{lambda}(rho) also avoid zero at zeta zeros? (It should -- lambda also relates to 1/zeta.)
2. Replace mu(k) with the von Mangoldt function Lambda(k): Does sum_{k<=K} Lambda(k)/k^s avoid zeros of zeta? (Different -- Lambda relates to -zeta'/zeta, not 1/zeta.)
3. Test with RANDOM coefficients: Take a_k iid +/-1. Does sum a_k k^{-s} show avoidance at zeta zeros? If YES: avoidance is a consequence of arithmetic structure. If NO: avoidance is a consequence of the SPECIFIC coefficients mu(k).
4. Test with Dirichlet characters: Does sum chi(k) k^{-s} (truncated L-function) show avoidance at L(s,chi) zeros? Run for chi mod 3, mod 4, mod 5.
5. Replace zeta zeros with L-function zeros: Does c_K(rho_chi) show avoidance at zeros of L(s,chi)?

**(d) What finding would mean:** If avoidance holds for ALL multiplicative-function-based Dirichlet polynomials: DPAC generalizes to a universal principle about truncated Euler products. If it holds ONLY for Mobius: the avoidance is specific to the structure of mu(k), pointing to deep properties of the Mobius function at zeta zeros. If random coefficients also show avoidance: the phenomenon is essentially geometric (about the distribution of {k^{-it}} on the unit circle) rather than arithmetic.

---

### Application 4: 33,000:1 Cancellation in Other Sequences

**(a) Tool:** Four-term decomposition (A-B-C-D) and cancellation ratio analysis.

**(b) Area:** Precision cancellation in arithmetic sums.

**(c) Specific experiments:**
1. Compute the four-term decomposition for the TWISTED Farey discrepancy (Farey sequence with character weights). Does the 33,000:1 ratio persist? Increase? Decrease?
2. Compute analogous decompositions for: (a) the Stern-Brocot tree level sums, (b) the continued fraction partial quotients, (c) the Minkowski ?(x) function values.
3. For each: measure the cancellation ratio (largest term / residual). If any sequence shows comparable or higher cancellation, it shares structural properties with Farey.

**(d) What finding would mean:** The 33,000:1 ratio is currently a standalone curiosity. Finding it in other sequences would reveal a FAMILY of arithmetic objects with extreme cancellation, potentially connected through the modular group SL(2,Z) (which underlies Farey, Stern-Brocot, and continued fractions). Finding that it's UNIQUE to Farey would confirm the special status of Farey discrepancy among arithmetic sequences.

---

### Application 5: Interval Certificates for Dirichlet L-Functions

**(a) Tool:** Interval arithmetic certification pipeline.

**(b) Area:** Non-vanishing of truncated L-functions at specific points.

**(c) Specific experiment:**
For Dirichlet characters chi mod q (q = 3, 4, 5, 7, 8):
1. Compute c_K^{chi}(rho) = sum_{k<=K} chi(k)*mu(k)*k^{-rho} at the first 100 zeros of L(s, chi).
2. Certify c_K^{chi}(rho) != 0 using interval arithmetic.
3. Tabulate: which (chi, K, zero_index) are certified?

This is a direct extension of the existing pipeline. The code for interval arithmetic exists. The only new input: the zeros of L(s, chi) (available from LMFDB or computable with mpmath).

**(d) What finding would mean:** If certificates succeed for Dirichlet L-functions: the avoidance phenomenon is not specific to zeta. DPAC generalizes. This would be strong evidence for a universal principle. If certificates FAIL for some L-functions: identifies which L-functions have weaker avoidance, suggesting a classification based on conductor or character type.

---

### Application 6: Gap Spectroscope + Goldston-Pintz-Yildirim

**(a) Tool:** Prime gap spectroscope (3.8x detection).

**(b) Area:** Small gaps between primes (GPY sieve).

**(c) Specific experiment:**
The GPY method shows that liminf (p_{n+1}-p_n)/log(p_n) = 0. The method uses sieve weights optimized for detecting small gaps. Run the spectroscope on:
1. The GPY sieve-weighted sum: sum w(p) * (gap_indicator) * p^{-it} where w(p) are the GPY weights
2. Compare to the unweighted gap spectroscope
3. The GPY weights should AMPLIFY the spectroscope signal because they concentrate on the primes most sensitive to zero locations

**(d) What finding would mean:** If GPY weights amplify detection: the sieve weights that produce bounded gaps are EXACTLY the weights that amplify zeta zero detection. This is a deep structural connection between bounded gaps and zero detection. It suggests that the bounded gaps phenomenon is a CONSEQUENCE of how primes encode zero information -- a philosophical reframing of Maynard-Tao.

---

### CROSS-DOMAIN RANKING:

| Rank | Application | Novelty | Feasibility | Expected Impact |
|------|------------|---------|-------------|-----------------|
| 1 | Black-box conjecture tester (tau, p(n) mod 5, etc.) | HIGH | HIGH | Classification principle |
| 2 | Avoidance for other Dirichlet polynomials | VERY HIGH | HIGH | Generalizes DPAC |
| 3 | Twin primes vs isolated primes (Maynard-Tao) | HIGH | HIGH | Connects two frontiers |
| 4 | Interval certificates for Dirichlet L-functions | MEDIUM | VERY HIGH | Extends pipeline |
| 5 | Gap spectroscope + GPY weights | HIGH | MEDIUM | Deep structural insight |
| 6 | 33,000:1 cancellation in other sequences | MEDIUM | MEDIUM | Structural classification |

---

## OVERALL STRATEGIC RECOMMENDATION

**Immediate (next 2 weeks):**
1. Write DPAC paper for Experimental Mathematics (Direction 1)
2. Write AMM note on K<=4 (Easy Win 1)
3. Extend certificates to 500 zeros (Easy Win 2)
4. Run spectroscope on primes in progressions (Easy Win 3)

**Short-term (next 1-2 months):**
5. Unconditional detection of 800 specific zeros (Direction 5)
6. K=5 non-vanishing attempt -- reformulated (Direction 2)
7. Avoidance for other Dirichlet polynomials (Application 2)
8. pip package (Easy Win 5)

**Medium-term (next 3-6 months):**
9. LI implies DPAC (Direction 6)
10. Batch spectroscope for automorphic L-functions (Direction 4)
11. Black-box conjecture tester systematic campaign (Application 1)
12. Double obstruction structural proof (Direction 3)

**The single highest-ROI action right now: Write the DPAC paper.** The content exists. The novelty is clear. The target journal (Experimental Mathematics) is ideal. Ship it.
