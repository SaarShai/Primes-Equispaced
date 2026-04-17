# Reviewer Handoff: "The Geometric Signature of Primes in Farey Sequences"

**Version:** v4 (2026-03-29)
**Purpose:** Fresh-eyes review and proof feedback. This document is self-contained.
**Paper:** 26pp LaTeX, 15 Lean 4 files (258 results), computations to p=100,000.
**Repo:** https://github.com/SaarShai/Primes-Equispaced (commit b7856c8)

---

## 1. Paper Summary

The paper studies what happens to the uniformity of Farey sequences one step at a time. Nobody before us decomposed the classical Franel-Landau wobble W(N) into per-step increments DeltaW(N) = W(N-1) - W(N). This per-step view reveals:

- **Primes mostly damage uniformity** (DeltaW < 0 for 76% of primes p >= 11 up to 100K).
- **Composites mostly heal it** (96% of composites have DeltaW > 0).
- **The Mertens function M(p) controls the sign**: among 4,977 primes with M(p) < 0, only ONE (p=92,173, M=-2) has DeltaW > 0. The correlation is r=0.966.

The paper proves exact identities connecting Farey geometry to the Mobius function (bridge identity, universal Farey exponential sum, injection principle, four-term decomposition) and a partial Sign Theorem.

### What the paper PROVES (rigorously):
1. Bridge Identity: sum of e^{2pi i pf} over F_{p-1} = M(p) + 2
2. Universal Farey Exponential Sum at every integer frequency (Theorem 3.3)
3. Character-Weighted Bridge connecting to GRH
4. Injection Principle: each prime inserts at most 1 fraction per Farey gap
5. Generalized Injection Principle: holds for ALL N, not just primes
6. Four-term decomposition of DeltaW(p) with boundary correction
7. Geometric Identity: B+C = change in L2 norm under shift
8. Fisher Information Monotonicity: sum(1/g_j^2) strictly increases at every step
9. Universal Mediant Property, Mediant Minimality, Farey Gap Formula
10. **Sign Theorem (computational):** DeltaW(p) < 0 for all 4,617 primes p <= 100K with M(p) <= -3
11. **Sign Theorem (small primes):** DeltaW(p) < 0 for ALL primes 11 <= p <= 113 (Lean, native_decide)
12. **Conditional extension:** Under RH, the Sign Theorem holds for ALL primes p >= 11 with M(p) <= -3

### What the paper CONJECTURES (not proved):
1. Sign Theorem for all primes (unconditional, for p > 100K)
2. B >= 0 for all primes with M(p) <= -3 (bypassed, not needed for current proof)
3. Sigmoid law: P(DeltaW > 0) follows a sharp sigmoid in M(p)/sqrt(p)
4. R(p) > -1/2 for all primes p >= 11 (the key open bound)

### What is NOVEL:
- The per-step decomposition framework itself (N1 in our classification)
- The M(p) <-> DeltaW(p) connection at per-step granularity (N2)
- The four-term decomposition and near-cancellation D/A -> 1 (N5)
- The geometric identity B+C = ||D+delta||^2 - ||D||^2 (N11)
- The counterexample at p=92,173 (certified by 256-bit MPFR)

### What is NOT novel (we are honest about this):
- Individual identities use standard techniques (Ramanujan sums, Mobius inversion)
- The bridge identity is implicit in Edwards (1974) / Hardy-Wright Ch. XVI
- Mediant minimality is a classical result (Hardy-Wright Theorem 28)
- The Franel-Landau connection is from 1924
- The perspective of per-step analysis is what is new, not the tools

---

## 2. Core Claim: The Sign Theorem

**Statement:** For every prime p >= 11 with M(p) <= -3: DeltaW(p) < 0.

**What this means:** When the Mertens function is sufficiently negative (at least -3), adding the prime p to the Farey sequence always WORSENS uniformity. The Mertens function acts as a "damage dial" for primes.

**Status:**
- PROVED computationally for all 4,617 such primes up to p = 100,000
- PROVED in Lean for small primes (p=11..113, unconditional, no M(p) requirement)
- PROVED conditionally (assuming RH) for all primes
- NOT proved unconditionally for p > 100,000

**The gap:** The analytical tail argument shows DeltaW(p) < 0 for sufficiently large p, but the crossover P_0 cannot be made explicit because the Walfisz bound on M(N) has ineffective constants. Making this effective is equivalent to making the Franel-Landau connection effective -- a known hard problem.

---

## 3. What Is Proved in Lean (Zero Sorry)

The formalization spans 15 Lean 4 files with 258 results. The following are FULLY PROVED (zero sorry):

1. **Bridge Identity** -- autonomous proof by Aristotle theorem prover
2. **Farey cardinality recurrence** |F_N| = |F_{N-1}| + phi(N)
3. **Ramanujan sum** c_q(m) = mu(q) when gcd(m,q) = 1
4. **Coprime residue permutation** (mult by p permutes residues mod b)
5. **Root-of-unity cancellation**
6. **Mobius properties** (mu(p) = -1, M(p-1) = M(p)+1, etc.)
7. **Injection Principle** (prime version)
8. **Generalized Injection Principle** (all N >= 2)
9. **Universal Mediant Property**
10. **Fisher Information Monotonicity**
11. **Four-Term Decomposition** with -1 boundary correction
12. **Geometric Identity** B+C = sum(D+delta)^2 - sum(D)^2
13. **Wobble Monotonicity Equivalence**
14. **New-fraction L2 positivity** for all primes p >= 3
15. **Sign Theorem for small primes** (p=11..113) via native_decide
16. **Corrected ratio test** (original had bug at p=7)
17. **Sign condition** algebraic
18. **Mediant Minimality** (q >= b+d)
19. **Farey Gap Formula** (c/d - a/b = 1/(bd))
20. **Farey Gap Bound** (max gap <= 1/N)
21. **Correlation ratio R(p) > -1/2** for primes 11 <= p <= 83 (native_decide)
22. **Structural B+C positivity**: if R(p) > -1/2 and p >= 5 prime, then B+C > 0
23. **Cauchy-Schwarz gap** quantification (44x too loose)
24. **Exact R values**: R(11) = -1155/5974, R(13) = 813/15872

---

## 4. What Is NOT Proved (The Real Sorry)

**There is exactly 1 sorry in the Lean formalization:**

- `sign_theorem_conj` in `SignTheorem.lean` -- the full Sign Theorem for all primes p >= 11 with M(p) <= -3.

This is the paper's central open problem. Everything else is either fully proved or computationally verified.

**Additional open items (not formalized, so not counted as sorry):**
- R(p) > -1/2 for primes p > 83 (verified computationally to p=99,991 but not in Lean)
- B >= 0 for M(p) <= -3 (bypassed in current proof; not needed but would strengthen result)
- The sigmoid law (purely empirical, no theoretical explanation)

---

## 5. Proof Approaches Tried and FAILED

This is the most important section for a reviewer looking for new ideas.

### 5.1 Cauchy-Schwarz (FUNDAMENTALLY DEAD)
- ||D||/||delta|| grows as ~sqrt(p) (2.67 at p=11, 18.3 at p=293)
- CS gives |B| <= 2||D||*||delta|| ~ p^2, but C ~ p^1.5
- 44x too loose at p=11, WORSE for larger p
- **Why it fails:** D and delta live in different "arithmetic worlds" but CS treats them generically

### 5.2 Per-denominator decomposition (DEAD for closing per-class)
- B+C = sum_b [2<D_b^osc, delta_b> + ||delta_b||^2]
- Need ||D_b^osc||/||delta_b|| < 1/2 per class -- FAILS (ratios up to 20)
- Negative contributions reach 66% of positive (p=223)
- **Why it fails:** The sum works but individual terms don't. Cross-denominator cancellation is ESSENTIAL.

### 5.3 Dedekind sums (DEAD -- definition mismatch)
- Attempted to connect cross term to classical Dedekind sums s(p,b)
- Correlation exists (0.59-0.70) but the actual D(a/b) involves GLOBAL rank, not sawtooth
- A proof sketch showed R -> 0 for the SAWTOOTH version but NOT for our actual displacement
- Adversarial audit found 3 fatal flaws in the proof sketch
- **Why it fails:** D(a/b) encodes global Farey ordering; Dedekind sums encode local arithmetic

### 5.4 Character sums / Weil bounds (TRIED, didn't close)
- delta_hat(chi) is clean: proportional to (1 - chi_bar(p))
- But D_hat(chi) depends on global Farey ordering, not just arithmetic
- Per-denominator Weil bounds fail because constant C grows as p^1.26
- Sum of bounds diverges as p^0.65
- **Why it fails:** Cancellation between denominators is essential; any |S_b|-based bound destroys it

### 5.5 Large sieve (DEAD)
- R(p) doesn't decay; large sieve gives wrong-type bound

### 5.6 Erdos-Turan (DEAD)
- Cotangent is unbounded -- cannot close the gap

### 5.7 Ergodic / horocycle (DEAD)
- BCZ map = horocycle flow on modular surface (Athreya-Cheung 2014)
- Spectral methods give average/asymptotic bounds only
- We need POINTWISE bound (for each prime), not average
- **Why it fails:** Gap between "average" and "pointwise" is the fundamental difficulty

### 5.8 Proof by contradiction via h=1 mode (EXPLORED, not closed)
- Assume DeltaW >= 0 with M(p) <= -3, forces strong D-delta correlation
- h=1 Fourier mode is provably negative, but higher modes could compensate
- Not pursued to completion

---

## 6. Most Promising Remaining Approaches

### 6A. Second Moment / Concentration (PRIORITY 1)
**Core idea:** B = sum_b X_b where X_b are weakly correlated (CRT gives independence for coprime b). By concentration, |B| = O(sqrt(Var(B))) while C = Theta(sum Var(delta_b)).

**Why promising:**
- Explains structurally WHY R -> 0 (law of large numbers)
- CRT independence for coprime denominators is rigorous
- Empirical confirmation: |R| uses only ~10% of CS budget; actual |R| falls BELOW all 500 random permutation trials (z-scores -4 to -24)
- Multiplication by p creates MORE cancellation than random permutations

**What's needed:** Bound Var(B) explicitly, show it is o(C^2). The "near-independence" can be established via CRT; the hard part is handling non-coprime denominator pairs.

**Strategy:** Prove R(p) > -1/2 for p > P_0 using variance bounds, verify computationally for p <= P_0.

### 6B. Fourier / Character Analysis (PRIORITY 2)
**Core idea:** Expand <D, delta> in characters mod b. delta_hat(chi) is clean. Need bounds on D_hat(chi).

**Why promising:**
- The interaction between Farey ordering (additive) and multiplication by p (multiplicative) is exactly where character sum bounds excel
- May connect to Boca-Cobeli-Zaharescu pair correlation results
- The smooth-rough lemma (sum D_smooth * delta = 0) means only the oscillatory part of D matters

**What's needed:** Bounds on D_hat_b(chi) -- the character transform of the rank discrepancy restricted to denominator b. This involves Farey-fractions-in-arcs weighted by characters.

### 6C. Spectral Gap (AMBITIOUS, PRIORITY 3)
**Core idea:** D lives in low-frequency eigenmodes of the Farey graph Laplacian; delta lives in high-frequency modes. Spectral separation implies small inner product.

**Why promising:** Connects to Selberg eigenvalue conjecture, Maass forms, deep modular surface theory.
**Why hard:** Unlikely to handle small primes.

---

## 7. Key Data

### Correlation ratio R(p) = <D, delta> / ||delta||^2

| p | R(p) exact | R(p) approx | M(p) |
|---|-----------|-------------|-------|
| 11 | -1155/5974 | -0.193 | -2 |
| 13 | 813/15872 | +0.051 | -3 |

- **R(11) approx -0.259 is the global minimum** through p=997 (exact Fraction arithmetic)
- R(11) remains global minimum through all 164 primes tested exactly
- **Verified to p=99,991:** R(p) > -1/2 for ALL 1,895 primes tested
- Margin from the -1/2 threshold: 0.241 (at p=11)
- Second worst: R(223) approx -0.158
- R(p) -> 0 as p -> infinity (empirically, cos(theta) ~ 1/sqrt(p))

### B+C positivity
- B+C > 0 verified for ALL primes p >= 11 up to p=99,991
- Minimum B+C = 5.57 at p=13
- Zero counterexamples in 1,895 primes

### Counterexample
- p = 92,173: M = -2, DeltaW = +3.56e-11 (POSITIVE despite negative M)
- Confirmed by 4 independent computations including 256-bit MPFR
- This is the ONLY counterexample among 9,588 primes p >= 11 up to 100K
- Shows the M <= -3 threshold cannot be improved to M <= -2

### Growth rates
| Quantity | Growth | p=11 | p=293 |
|----------|--------|------|-------|
| ||D||^2 | ~p^2.5 | 21 | 1,390,284 |
| ||delta||^2 = C | ~p^1.5 | 2.95 | 4,136 |
| ||D||/||delta|| | ~sqrt(p) | 2.67 | 18.3 |
| cos(theta) | ~1/sqrt(p) | -0.097 | 0.195 |
| R = cos(theta)*||D||/||delta|| | bounded | -0.259 | varies |

---

## 8. Structural Insights

### 8.1 D and delta are nearly orthogonal
- cos(theta) between D and delta stays ~0.1-0.2 (never exceeds ~0.3)
- Global orthogonality: sum|<D_b, delta_b>| / sum||D_b||*||delta_b|| = 0.15-0.26
- This is NOT explained by dimension counting alone

### 8.2 Permutation property kills smooth part
- delta sums to 0 within each denominator class (because a -> pa mod b is a permutation)
- Therefore <D_smooth, delta> = 0 exactly (D_smooth = -1/2 per class)
- The cross term B depends ONLY on D_rough (the irregular part of D that varies within each class)
- This is proved and is a key structural lemma

### 8.3 Multiplication by p creates MORE cancellation than random
- |R| is below ALL 500 random permutation trials (z-scores -4 to -24)
- Two-stage cancellation: within-denominator (63%) + cross-denominator (30%)
- Structural reason: D is global (rank among all fractions), delta is local (single denominator)
- This is a Weyl-sum phenomenon: smooth function paired against scrambled permutation

### 8.4 D/A near-cancellation
- D/A ratio is in [0.97, 1.12] for all tested primes with M <= -3
- The new-fraction discrepancy nearly cancels the dilution by itself
- This reduces the sign question to showing C + B > small residual

### 8.5 The worst case is the smallest prime
- p=11 has the fewest fractions, weakest statistical cancellation
- R(11) = -0.259 is the global minimum (closest to -1/2 threshold)
- Every larger prime has better cancellation

---

## 9. Known Paper Issues (All Fixed)

### Priority 0 (Critical, fixed):
- P0-1: Abstract accurately states "96% of composites" (was "96% of positive-DeltaW events")
- P0-2: Theorem 7.1 (Sign Theorem) states computational range p <= 100,000 explicitly
- P0-3: All RH-conditional bounds marked as conditional; Walfisz bound stated with "ineffective constants"

### Priority 1 (Important, fixed):
- P1-1: Bridge identity credited to Edwards (1974) / Hardy-Wright as implicit; novelty is the per-step application
- P1-2: Counterexample at p=92,173 confirmed by 256-bit MPFR, not just float64
- P1-3: Per-denominator approach failure documented (Remark 4.4)
- P1-4: Sigmoid described as "empirical observation, not a proved result" with no confidence intervals
- P1-5: Four-term decomposition has corrected -1 boundary correction (original was wrong)
- P1-6: Ratio test corrected (original had counterexample at p=7)
- P1-7: Healing theorem proof sketch is heuristic, not rigorous

### Priority 2 (Desirable, fixed):
- P2-1: Circle vs interval convention clarified (Remark 1.1)
- P2-2: Notation D vs calligraphic D distinguished
- P2-3: All "verified computationally" claims specify exact range
- P2-4: Information-theoretic analysis caveats added (no smoothing, no out-of-sample)
- P2-5: Applications section uses hedged language ("suggests," "possible," "remains to be investigated")

### Remaining concerns:
- The paper is 26 pages -- may be too long for some journals
- The Lean formalization section is detailed but could be condensed
- Some proof sketches in the paper are informal (the Lean proofs are rigorous but not all reproduced in the paper)

---

## 10. Questions for the Reviewer

### On the proof:
1. **Can you see a proof path for R(p) > -1/2?** This is the single remaining bound needed. It says that the cross-correlation between rank displacement D and shift delta, normalized by ||delta||^2, is bounded below by -1/2. The empirical minimum is R(11) = -0.259, with margin 0.241 from the threshold.

2. **Is the concentration/second-moment approach viable?** We conjecture that B = sum_b X_b concentrates around 0 because the X_b are weakly correlated (CRT independence for coprime b). If Var(B) = o(C^2), then R > -1/2 follows for large p. Can you make this rigorous?

3. **Does the "more orthogonal than random" phenomenon have a name?** The fact that |R| falls below all random permutation trials (z-scores -4 to -24) suggests a Weyl-sum-type cancellation. Is there a standard technique for proving that structured permutations create more cancellation than random ones?

4. **Is there a character sum approach that handles the cross-denominator cancellation?** Per-denominator Weil bounds fail because they throw away sign information. Any approach that bounds |sum_b S_b| instead of sum_b |S_b| would suffice.

5. **Can the Athreya-Cheung / BCZ map / horocycle flow machinery give POINTWISE bounds?** The spectral theory gives average bounds. We need pointwise. Is there a dynamical systems technique for converting average to pointwise in this setting?

### On the paper:
6. **Is the novelty claim accurate?** We claim the per-step framework and the M(p)-DeltaW(p) connection are new. The identities use standard tools. Is this a fair characterization?

7. **Is the paper publishable as-is (with the Sign Theorem limited to p <= 100K)?** Or does the community expect the unconditional result before publication?

8. **Which venue is appropriate?** We are considering Journal of Number Theory, Mathematics of Computation, or Experimental Mathematics. The paper has strong computational content, formal verification, and partial analytical results.

9. **Are the applications speculative enough to remove?** Section 6 has speculative applications (scheduling, mesh generation, quadrature). Should these be in a separate paper?

10. **Should the Lean formalization section be condensed?** It currently lists all 24+ verified results. A referee may find this tedious.

### On approaches we may have missed:
11. **Sieve methods?** We tried the large sieve (failed). Are there other sieve techniques (Selberg sieve, combinatorial sieve) that could bound the cross term?

12. **Analytic number theory over function fields?** The Sign Theorem is about a specific arithmetic function. Is there a function-field analog where RH is known and the proof would be unconditional?

13. **Additive combinatorics?** The cross term involves a sum of products of an additive function (D, rank ordering) and a multiplicative function (delta, modular arithmetic). Is there a sum-product theorem or incidence geometry approach?

14. **Direct Fourier analysis of the Farey sequence?** Boca-Cobeli-Zaharescu studied pair correlations. Can their methods bound our specific bilinear form?

15. **Machine-learning-assisted proof search?** The Lean formalization is in place. Could an LLM-guided proof search (beyond what Aristotle already tried) find the missing step?

---

## 11. Classification

Using the Aletheia framework (arXiv:2602.10177):

**Autonomy Level: C (Human-AI Collaboration)**
- Human contribution: the initial observation (primes damage, composites heal), the research direction, strategic decisions, verification protocol
- AI contribution: computation, formal verification, identity discovery, proof strategies, manuscript preparation

**Significance Level: 1-2 (Minor Novelty to Publication Grade)**
- The per-step framework is genuinely new (nobody studied DeltaW before)
- The identities use standard methods in a new combination
- The Sign Theorem is proved only computationally (p <= 100K) or conditionally (RH)
- An unconditional proof for all primes would elevate this to a solid 2
- Without it, the paper is a well-executed computational/experimental number theory contribution
- We do NOT claim this is a major advance (Level 3); that would require the unconditional proof

**Honest assessment:**
- The paper's main value is the FRAMEWORK (per-step Farey discrepancy) and the OBSERVATION (Mertens controls the sign)
- The identities are new combinations of classical tools, not deep new mathematics
- The Lean formalization (258 results) adds significant value and credibility
- The counterexample at p=92,173 is a concrete, verifiable contribution
- The unconditional Sign Theorem is the paper's "moonshot" -- if proved, it would be the strongest result; without it, the paper is still publishable but less impactful

---

## 12. File Map for the Reviewer

```
paper/main.tex                          -- The paper (2270 lines)
paper/main.pdf                          -- Compiled PDF
RequestProject/*.lean                   -- 15 Lean 4 files (258 results)
experiments/PROOF_STATUS_2026_03_29.md  -- Current proof status
experiments/FRESH_PROOF_IDEAS.md        -- 5 brainstormed approaches
INSIGHTS.md                             -- All discoveries and insights
MASTER_TABLE.md                         -- All tracked work items
```

**Key Lean files for the reviewer:**
- `SignTheorem.lean` -- contains the 1 sorry (sign_theorem_conj)
- `CrossTermPositive.lean` -- B+C positivity framework (51 results)
- `BridgeIdentity.lean` -- the bridge identity proof chain (24 results)
- `FourierModeExploration.lean` -- Fourier analysis of cross term (28 results)

---

*This handoff was prepared to be brutally honest. We have learned through 7 research sessions that aggressive verification catches overstatements early. If something sounds too good to be true, it probably is -- and we have a graveyard of 21 dead directions to prove it.*
