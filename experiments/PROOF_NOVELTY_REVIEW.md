# Proof Novelty Review: Brutally Honest Classification

**Date:** 2026-03-28
**Scope:** All theorems, identities, lemmas, and proofs from the paper, Lean formalization, discovery database, and experiment reports.

---

## Summary Statistics

| Classification | Count | Percentage |
|---------------|-------|------------|
| BOILERPLATE   | 10    | 33%        |
| SOLID         | 8     | 27%        |
| INSIGHTFUL    | 7     | 23%        |
| NOVEL         | 5     | 17%        |

---

## PART 1: The Identities (Section 3 of the Paper)

### 1. Bridge Identity
**Statement:** Sum_{f in F_{p-1}} e^{2pi i p f} = M(p) + 2

**Classification: BOILERPLATE**

**Why:** The paper itself acknowledges this is implicit in Edwards (1974) and Hardy-Wright Ch. XVI. The Ramanujan sum decomposition (c_q(p) = mu(q) when gcd(p,q)=1) is a standard exercise in analytic number theory. Summing mu over [2, p-1] to get M(p-1) - 1 is mechanical. Any graduate student who knows Ramanujan sums could derive this in an hour.

What WE added: Explicitly stating it in the per-step context and giving it a name. That framing is useful but the mathematics is not new.

---

### 2. Generalized Bridge Identity
**Statement:** Sum_{f in F_N} e^{2pi i m f} = M(N) + 1 for any prime m > N

**Classification: BOILERPLATE**

**Why:** Identical proof to #1, replacing p-1 with N and noting gcd(m,b)=1 for all b <= N < m. The observation that all primes m > N give the same sum is mildly interesting but follows immediately.

---

### 3. Universal Farey Exponential Sum Formula
**Statement:** Sum_{f in F_N} e^{2pi i m f} = M(N) + 1 + Sum_{d|m, d>=2} d * M(floor(N/d))

**Classification: SOLID**

**Why:** This is the complete evaluation at all integer frequencies, not just coprime ones. The exchange of summation order over Ramanujan sums c_b(m) = Sum_{d|gcd(b,m)} d*mu(b/d) is a standard technique, but carrying it through cleanly for all m and N, and recognizing the result as a "divisor-scaled Mertens" function, requires care. It is more than an exercise but the methods (Ramanujan sum + Mobius inversion) are entirely standard.

**What's good:** The formula itself appears to be new in the literature in this explicit closed form. Verified on a 40x30 grid. The "Mertens tomography" reading (inverting to recover M at multiple scales from a single F_N) is a nice conceptual contribution.

---

### 4. Master Involution Principle (MIP)
**Statement:** Sum_{f in F_N} D(f)*g(f) = -(1/2)*Sum g(f) for symmetric g

**Classification: BOILERPLATE**

**Why:** This is the observation that D(1-f) = -D(f) - 1, then pairing terms under the symmetry f <-> 1-f. The proof is three lines. The symmetry of Farey sequences under f <-> 1-f is classical (it is the reason the Stern-Brocot tree is symmetric). Applying it to get sum formulas for symmetric test functions is routine.

---

### 5. Displacement-Cosine Identity
**Statement:** Sum D(f)*cos(2pi p f) = -1 - M(p)/2

**Classification: SOLID**

**Why:** This is a direct combination of the MIP (#4) with the Bridge Identity (#1). Apply MIP with g = cos(2pi p f) (which is symmetric), get -(1/2)*(M(p)+2) = -1 - M(p)/2. The derivation is mechanical. However, the INTERPRETATION -- that the Fourier coefficient of the rank discrepancy at frequency p is a linear function of M(p) -- is genuinely illuminating. It makes concrete the connection between geometric positioning and Mobius cancellation.

**What's good:** The statement itself, while derivable, creates a clean bridge between discrepancy geometry and the Mertens function that I have not seen stated this way in the literature.

---

### 6. Fractional Parts Sum
**Statement:** Sum_{f in F_{p-1}} {pf} = (n-2)/2

**Classification: BOILERPLATE**

**Why:** Multiplication by p permutes coprime residues mod b (standard), so Sum {pa/b} over coprime a = phi(b)/2 for each b >= 2. Sum over b, add boundary terms. Completely routine.

---

### 7. Universal delta-Symmetric Identity
**Statement:** Sum delta(f)*g(f) = g(1) for symmetric g

**Classification: BOILERPLATE**

**Why:** delta(1-f) = -delta(f) for interior points (antisymmetry), so interior terms cancel pairwise when g is symmetric. Boundary contributes delta(1)*g(1) = g(1). Three-line proof, standard.

---

### 8. Cross-Term Formula
**Statement:** Sum D(f)*delta(f)^2 = -(1/2)*Sum delta(f)^2 - 1/2

**Classification: BOILERPLATE**

**Why:** delta(f)^2 is symmetric for interior points (squaring kills the sign), so apply MIP on the interior, then add the boundary correction. The boundary correction (the "-1/2") requires a small calculation but nothing non-obvious.

---

### 9. Character-Weighted Bridge
**Statement:** Sum chi(denom(f))*e^{2pi i m f} = 1 + Sum_{b=1}^{N} (chi*mu)(b) for prime m > N

**Classification: SOLID**

**Why:** Same Ramanujan-sum decomposition as the bridge, but weighting by a Dirichlet character. The connection to GRH (via 1/L(s,chi) = Sum (chi*mu)(n)*n^{-s}) is classical and well-known. However, stating the Farey exponential sum formulation of GRH explicitly for all characters, and recognizing it as a generalization of the Franel-Landau RH equivalence, is a clean synthesis worth publishing.

---

### 10. Displacement-Shift Identity
**Statement:** D_{F_p}(f) = D_{F_{p-1}}(f) + delta(f) for old fractions f != 1

**Classification: SOLID**

**Why:** The new rank = old rank + floor(pf), so D_new = D_old + floor(pf) - (p-1)f = D_old + (f - {pf}) = D_old + delta(f). This is a counting argument, entirely elementary. But it is the KEY STRUCTURAL IDENTITY that makes the entire four-term decomposition work. Without it, you cannot decompose DeltaW into interpretable terms. The fact that nobody bothered to write this down before (because nobody studied per-step wobble) is more a reflection of the per-step perspective being new than the identity being hard.

---

## PART 2: The Structural Results

### 11. Injection Principle (Prime)
**Statement:** Each gap in F_{p-1} contains at most one fraction k/p

**Classification: SOLID**

**Why:** The proof uses b+d >= p (standard Farey neighbor property), then bd >= p-1 (from (b-1)(d-1) >= 0), then the gap has width p/(bd) <= p/(p-1) < 2, so at most one integer fits. This is clean but entirely elementary -- it is a three-step counting/bounding argument using only the mediant property and AM-GM.

**What's good:** The result itself, while not deep, is useful and appears not to have been explicitly stated in this form. The Lean formalization is clean.

---

### 12. Generalized Injection Principle (All N)
**Statement:** Each gap in F_{N-1} receives at most one new fraction when forming F_N

**Classification: INSIGHTFUL**

**Why:** For primes, this is the result above. For general N, the proof requires a case analysis on q*s vs N (Cases 1-3 in the Lean file), with Case 3 (q*s = N-1) requiring the observation that (q-1)(s-1) = 0 forces a boundary denominator. The four-case structure and the critical product analysis are non-trivial. More importantly, the CONCEPTUAL STEP of recognizing that injection is a universal Farey property (not just for primes) is valuable. The standard viewpoint is that new fractions are mediants -- the injection perspective is dual to this but emphasizes different structure.

**Key non-obvious step:** Case 3 -- recognizing that q*s = N-1 forces q=1 or s=1, turning what looks like a potential failure case into a boundary case that is easy to handle.

---

### 13. Universal Mediant Property
**Statement:** Every new fraction in F_N \ F_{N-1} is the mediant of its neighbors

**Classification: BOILERPLATE**

**Why:** This is a well-known property of Farey sequences, essentially the definition of the Stern-Brocot tree. It appears in Hardy-Wright, Concrete Mathematics (Graham-Knuth-Patashnik), and every textbook treatment of Farey sequences.

---

### 14. Fisher Information Monotonicity
**Statement:** Sum 1/g_j^2 strictly increases at every step N -> N+1

**Classification: INSIGHTFUL**

**Why:** The proof that 1/g1^2 + 1/g2^2 > 1/g^2 when a gap g is split into g1 and g2 by the mediant uses the identity b^2*N^2 + d^2*N^2 > b^2*d^2 (which holds since b+d = N). The inequality itself is elementary, but the CONNECTION to Fisher information from statistics is non-obvious and genuinely interesting. The fact that Fisher information monotonically increases at EVERY step (no exceptions, unlike the wobble) makes this a cleaner invariant than the wobble itself.

**Key non-obvious step:** Recognizing that Sum 1/g_j^2 is the Fisher information of the gap distribution, and that its monotonicity is a natural complement to the wobble analysis. The contrast with the wobble (which has counterexamples) makes this particularly interesting.

---

### 15. Modular Inverse Neighbor
**Statement:** Left Farey neighbor of k/p has denominator b = k^{-1} mod p

**Classification: SOLID**

**Why:** From the adjacency condition kb - pa = 1, read mod p: kb = 1 (mod p), so b = k^{-1} mod p. This is a one-line observation. But it connects the injection geometry to modular arithmetic in a concrete way that makes the Injection Principle transparent: injectivity of gap placement is equivalent to invertibility of multiplication in (Z/pZ)*.

---

### 16. Denominator Sum
**Statement:** Sum D(a/b) over coprime a = -phi(b)/2

**Classification: BOILERPLATE**

**Why:** Sum of (j - n*a/b) over coprime a, using the pairing a <-> b-a. Standard symmetry argument.

---

### 17. Strict Positivity of Sum delta^2
**Statement:** Sum delta(f)^2 > 0 for all primes p >= 5

**Classification: SOLID**

**Why:** By the rearrangement inequality, Sum a*sigma_p(a) <= Sum a^2 with equality iff sigma_p = identity (i.e., p = 1 mod b). For p >= 5, b = p-2 gives p = 2 mod (p-2) != 1, so at least one denominator contributes strictly. Clean application of a well-known inequality.

---

## PART 3: The Per-Step Framework and Decomposition

### 18. The Per-Step Perspective on Farey Discrepancy
**Statement:** Define DeltaW(N) = W(N-1) - W(N) and study its sign prime-by-prime

**Classification: NOVEL**

**Why:** This is the foundational conceptual contribution of the paper. The Franel-Landau theorem connects W(N) to the Riemann Hypothesis, but the PER-STEP behavior -- how W changes at each integer -- has not been studied. The observation that primes and composites play fundamentally different roles (primes damage, composites heal) is empirically striking and was previously unknown. The telescoping W(N) = W(1) - Sum DeltaW(k) reframes Farey convergence as a competition between prime damage and composite healing.

**Key non-obvious insight:** That the sign of DeltaW(p) correlates with M(p), creating a direct bridge between per-step Farey geometry and the Mobius function at a level of granularity that was not known.

---

### 19. The Four-Term DeltaW = A - B - C - D Decomposition
**Statement:** DeltaW(p) decomposes into dilution (A), cross-term (B), shift-squared (C), and new-fraction discrepancy (D)

**Classification: INSIGHTFUL**

**Why:** Given the displacement-shift identity D_new = D_old + delta, the algebraic expansion of Sum D_new^2 - Sum D_old^2 is straightforward. What makes this INSIGHTFUL rather than BOILERPLATE is:

1. The discovery that D/A -> 1 (the new-fraction discrepancy nearly cancels the dilution), reducing the sign question to a thin residual.
2. The recognition that the near-cancellation D/A ~ 1 is WHY the problem is hard -- the sign depends on a 0.1% residual in a sum of O(p^2) terms.
3. The identification of B >= 0 (empirical) as the critical open problem, and the subsequent BYPASS discovery that C + D > A suffices.

**Key non-obvious step:** The near-cancellation D/A -> 1. This is not algebraically obvious; it required computation to discover and then the "factor-of-2 Riemann sum identity" to explain.

---

### 20. The D/A -> 1 Near-Cancellation (Factor-of-2 Identity)
**Statement:** Sum_{k=1}^{p-1} D_old(k/p)^2 ~ 2*(p-1)*integral D_old(x)^2 dx, making D/A -> 1

**Classification: INSIGHTFUL**

**Why:** The equally-spaced Riemann sum at points k/p of D_old(x)^2 is approximately TWICE the integral, not equal to it. This is surprising because for smooth functions the Riemann sum converges to the integral. The factor of 2 arises because D_old(x) has jumps at every Farey fraction, and the prime-spaced evaluation points k/p hit these jumps in a systematic way. This is a genuinely non-obvious numerical discovery that required computational exploration to find. It explains why D/A -> 1 and quantifies the convergence rate.

---

### 21. The Bypass Theorem (C + D > A without needing B >= 0)
**Statement:** For M(p) <= -3, C + D > A regardless of B's sign

**Classification: INSIGHTFUL**

**Why:** The original approach tried to prove B >= 0, which is IMPOSSIBLE (B < 0 at p = 13). The bypass -- recognizing that C grows as p^2 while A grows as p*log(p), so C alone eventually dominates -- is a genuine insight. The proof combines:
- Rearrangement inequality lower bound on C (Sum delta^2 >= N^2/(48 log N))
- Franel-Landau upper bound on A (dilution ~ p * log(p))
- Quadratic vs. quasi-linear growth comparison

The "C > A for large p" argument is not deep, but the DISCOVERY that this bypass exists -- that you do not need B >= 0 at all -- saved the proof program from a dead end.

---

## PART 4: The Quantitative Bounds

### 22. Deficit Identity: deficit_2(b) = (b^3 - b)/24
**Statement:** The displacement deficit for multiplication by 2 mod prime b has a closed form

**Classification: SOLID**

**Why:** Direct computation by splitting a into two ranges ([1, (b-1)/2] and [(b+1)/2, b-1]). The sum of squares formula finishes it. Elementary but the result is clean.

---

### 23. C/A Lower Bound: C/A >= pi^2/(432 log^2 N)
**Statement:** The shift-squared to dilution ratio has an explicit positive lower bound

**Classification: SOLID**

**Why:** Chains together: rearrangement inequality -> deficit lower bound -> PNT sum over primes -> Franel-Landau dilution upper bound. Each step uses a standard tool. The constant 432 is conservative by a factor of ~73 compared to empirical values. The chain is competent but uses no new technique.

---

### 24. R_1 >= 1 - eps(p) Bound (Step 1)
**Statement:** The main D_old sampling term approaches 1 with rate O(1/sqrt(log p))

**Classification: SOLID**

**Why:** Uses Cauchy-Schwarz on the cross term R_2, the exact formula for R_3, and a quadratic completion. Standard optimization techniques, no surprises.

---

## PART 5: The Empirical Discoveries

### 25. Sigmoid Relationship: P(DeltaW > 0) as function of M(p)/sqrt(p)
**Statement:** The probability of uniformity improvement follows a sharp sigmoid in M(p)/sqrt(p)

**Classification: NOVEL**

**Why:** This is a purely empirical discovery with no theoretical explanation. The sharpness of the transition (0% to 100% over a narrow band) and its dependence on the normalized Mertens function is striking. The connection to Rubinstein-Sarnak bias theory is suggestive but unproved. No one has studied this relationship before.

---

### 26. The p = 92,173 Counterexample (Certified)
**Statement:** M(92173) = -2 but DeltaW > 0, certified by 256-bit MPFR

**Classification: NOVEL**

**Why:** This disproves the natural conjecture (M < 0 => DeltaW <= 0 for p >= 11) and establishes M = -3 as the exact threshold. The certification methodology (four independent computations including rigorous interval arithmetic) is thorough. Finding this required systematic computation through 100,000 primes. The counterexample is a concrete, verified mathematical fact.

---

### 27. Primes Damage / Composites Heal Asymmetry
**Statement:** 99% of negative DeltaW mass comes from primes; 96% of composites heal

**Classification: NOVEL**

**Why:** This asymmetry in the per-step behavior of Farey sequences was unknown. It gives a new perspective on Farey convergence: the approach to uniformity is not monotone but is a competition between prime-driven damage and composite-driven healing. This is the central empirical finding that motivates the entire paper.

---

### 28. Sign Theorem (Hybrid Proof)
**Statement:** For all primes 11 <= p <= 100,000 with M(p) <= -3: DeltaW(p) < 0

**Classification: INSIGHTFUL**

**Why:** The proof is a hybrid of computation (finite base to 100K) and analysis (C/A = Omega(1/log^2 p) exceeds the gap 1 - D/A = O(1/sqrt(p))). The key insight is recognizing that these two rates cross: 1/log^2 p >> 1/sqrt(p) for large p. The proof structure (computational base + analytical tail with overlap) is a known technique, but applying it here required assembling all the preceding identities and bounds into a coherent argument. The conditional extension under RH is a nice bonus.

---

## PART 6: The PSL2Z and Secondary Results

### 29. Sum s(a,b) = 0 over Farey sequence (Dedekind sum identity)
**Statement:** Sum of Dedekind sums over all Farey fractions is exactly 0 for all N

**Classification: BOILERPLATE**

**Why:** Immediate from the reflection symmetry f <-> 1-f and the antisymmetry s(b-a,b) = -s(a,b). The proof is given explicitly in the PSL2Z report and takes three lines.

---

### 30. Euler Characteristic Preservation (DeltaV=+1, DeltaE=+2, DeltaF=+1)
**Statement:** Each Farey insertion preserves chi = V - E + F = 2

**Classification: BOILERPLATE**

**Why:** Topological invariance of Euler characteristic under cell subdivision. Standard result in algebraic topology applied to a specific triangulation.

---

### 31. B+C as Energy Change Identity
**Statement:** B + C = Sum D_{F_p}(f)^2 - Sum D_{F_{p-1}}(f)^2 over old fractions

**Classification: SOLID**

**Why:** Algebraic identity from (D+delta)^2 - D^2 = 2D*delta + delta^2 = B + C. Simple but the INTERPRETATION is useful: B+C > 0 iff prime insertion increases the total squared displacement of old fractions.

---

### 32. Compression Phenomenon (19,000:1)
**Statement:** The bridge identity compresses |F_N| ~ 3N^2/pi^2 fractions into one integer M(N)

**Classification: NOVEL (as a conceptual observation)

**Why:** While the mathematics is just the bridge identity, the observation that this represents extreme information compression (and the quantification of the compression ratio) is a fresh way to view the Farey-Mertens connection. The UCT (Universal Compression Test) finding that compressible sequences are exactly the Mobius-definable ones (13/13 matches) is an intriguing empirical pattern that could lead to interesting theory.

---

## PART 7: The Lean Formalization

### 33. Lean Formalization (12 files, 207 results, 0 sorry)
**Statement:** All core identities formally verified in Lean 4

**Classification:** Not a mathematical contribution, but a significant ENGINEERING contribution. The autonomous proof construction by Aristotle (especially the bridge identity chain: coprime permutation -> Ramanujan sum -> bridge identity) is noteworthy for AI-assisted mathematics. The permutation lemma (coprime_mul_perm) is the most technically involved Lean proof.

---

## OVERALL ASSESSMENT

### What is genuinely new (the 5 NOVEL items):
1. **The per-step perspective itself** -- studying DeltaW(N) prime-by-prime
2. **The primes-damage/composites-heal asymmetry** -- the central empirical finding
3. **The sigmoid relationship** with M(p)/sqrt(p) -- a sharp empirical law
4. **The p=92,173 counterexample** -- a concrete certified mathematical fact
5. **The compression phenomenon** framing -- a new conceptual lens

### What shows real mathematical thinking (the 7 INSIGHTFUL items):
1. The generalized injection principle (case analysis, boundary structure)
2. Fisher information monotonicity (connection to statistics)
3. The four-term decomposition (near-cancellation discovery)
4. The D/A -> 1 factor-of-2 identity (non-obvious numerical discovery)
5. The bypass theorem (escaping the B >= 0 dead end)
6. The Sign Theorem proof structure (computational base + analytical tail)
7. The generalized injection's conceptual shift (injection vs. mediant duality)

### What is competent but standard (the 8 SOLID items):
The universal formula, character bridge, displacement-shift, injection principle (prime), modular inverse neighbor, strict positivity, deficit formula, C/A bound, R_1 bound, B+C energy identity

### What any competent mathematician would derive (the 10 BOILERPLATE items):
The bridge identity, generalized bridge, MIP, fractional parts sum, delta-symmetric identity, cross-term formula, universal mediant, denominator sum, Dedekind sum identity, Euler characteristic

### Honest bottom line:

The mathematical TECHNIQUES are largely standard -- Ramanujan sums, Mobius inversion, rearrangement inequality, Cauchy-Schwarz, symmetry arguments. There is no single proof that would make an expert say "how did they think of that?" The most technically demanding work is the quantitative bounds (STEP1, STEP2, C/A lower bound), which chain together known tools competently but without novelty.

The genuine intellectual contributions are:
1. **The perspective** -- nobody studied DeltaW(p) before. This is the big idea.
2. **The empirical discoveries** -- the sigmoid, the damage/heal asymmetry, the counterexample, the near-cancellation D/A ~ 1.
3. **The synthesis** -- connecting Farey geometry to Mertens function at a per-step level, assembling a hybrid proof of the Sign Theorem.
4. **The bypass insight** -- recognizing that C + D > A sidesteps the B >= 0 problem.

About 30% of the content is boilerplate, 27% is solid, and the remaining 40% contains the real value. The paper's strength is NOT in deep new proofs but in a fresh viewpoint that connects known objects in a new way. That is a legitimate and publishable contribution, but one should not oversell the technical depth of the individual results.

### What to emphasize vs. de-emphasize in the paper:

**Emphasize:** The per-step perspective, the empirical discoveries (sigmoid, damage/heal, counterexample), the Sign Theorem, the four-term decomposition's near-cancellation, Fisher information monotonicity, the compression phenomenon.

**De-emphasize:** The bridge identity (acknowledge as classical more clearly), the boilerplate symmetry identities (they are tools, not contributions), the detailed quantitative bounds (relegate to appendix).

**Do NOT claim:** That the bridge identity is "new" -- it is a new framing of a classical result. That the injection principle is "deep" -- it is elementary. That the Lean formalization proves anything mathematically new -- it verifies known results.
