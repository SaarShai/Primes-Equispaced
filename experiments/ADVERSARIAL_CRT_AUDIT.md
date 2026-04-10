# Adversarial Audit: CRT Deficit Composites Proof

**Date:** 2026-03-29
**Role:** Hostile referee (Step 3 of verification protocol)
**Document audited:** CRT_DEFICIT_COMPOSITES.md
**Claim:** Sum_{b=2}^{N} delta_b^2 = N^2/(2pi^2) + O(N log N), unconditionally.

**VERDICT: THE MAIN THEOREM IS NOT PROVED. Step 6 is an unresolved gap.**

---

## Item-by-Item Audit

### 1. E[deficit_b] = S_2(b) - b^2*phi(b)/4 (Step 4)

**STATUS: CORRECT.**

The random-permutation expected value is correctly derived:
- For a uniform random permutation pi of a set {x_1,...,x_n}: E[Sum x_i * pi(x_i)] = (Sum x_i)^2 / n. This is a standard combinatorial identity.
- Applied to (Z/bZ)*: Sum_{gcd(a,b)=1} a = b*phi(b)/2 (correct), so E[T_b] = (b*phi(b)/2)^2 / phi(b) = b^2*phi(b)/4. Verified numerically for b = 6, 10, 12, 15, 20, 30 -- exact match.
- Therefore E[deficit_b] = S_2(b) - b^2*phi(b)/4. Correct.

### 2. Sum E[deficit_b]/b^2 = N^2/(4pi^2) (Step 5)

**STATUS: CORRECT, but the derivation of A(N) in Step 3 is sloppy.**

The computation proceeds as:
- Sum E[deficit_b]/b^2 = Sum S_2(b)/b^2 - (1/4)*Sum phi(b) = A(N) - (1/4)*Sum phi(b).
- A(N) = N^2/pi^2 + O(N log N): TRUE. The key asymptotic is S_2(b) ~ b^2*phi(b)/3 (verified numerically: ratio = 1.0005 at b=100), so A(N) = Sum S_2(b)/b^2 ~ (1/3)*Sum phi(b) = N^2/pi^2. Numerical verification confirms convergence.
- Sum_{b<=N} phi(b) = 3N^2/pi^2 + O(N log N): Standard result (Mertens).

So the conclusion N^2/(4pi^2) is correct.

**HOWEVER: The Step 3 derivation in the document is embarrassingly messy.** The author abandons their first attempt mid-sentence ("Hmm, this isn't clean. Let me redo."), then the "cleaner approach" appeals to "we know empirically" before waving hands at "standard Tauberian analysis." A published proof needs to either:
(a) Write out the Mobius inversion cleanly: S_2(b) = Sum_{d|b} mu(d)*d^2 * (b/d - 1)(b/d)(2b/d - 1)/6, leading term b^2*phi(b)/3, then sum using Sum phi(b) ~ 3N^2/pi^2, or
(b) Cite a specific reference for the Dirichlet series approach.

The result is correct but the exposition is not proof-grade.

### 3. The Kloosterman Claim (Step 6) -- THE FATAL GAP

**STATUS: NOT PROVED. The claimed bound is numerically FALSE.**

The document's "Proof Roadmap" (end of Step 6) proposes three approaches to show:

> Sum_{b<=N} [T_b(p) - E[T_b]] / b^2 = o(N^2).

The preferred approach states:

> "Direct Kloosterman: |T_b - E[T_b]| <= C * b^{3/2+epsilon}, then Sum b^{3/2+epsilon}/b^2 converges."

**This is FALSE.** Numerical computation for p = 397 reveals:

| b   | |T_b - E[T_b]| / b^{3/2} |
|-----|--------------------------|
| 50  | 5.66                     |
| 199 | 16.33 (at b^2 scale)     |
| 395 | 261.64                   |

The ratio |T_b - E[T_b]| / b^{3/2} is UNBOUNDED -- it reaches 261 at b = 395. The pointwise bound |T_b - E[T_b]| <= C * b^{3/2+epsilon} does not hold with any reasonable constant. The actual growth is closer to b^{5/2}.

**Moreover, T_b is NOT a Kloosterman sum.** T_b = Sum_{gcd(a,b)=1} a * (pa mod b) involves floor functions, not exponentials. The connection to Kloosterman sums is indirect at best -- for prime b, the deficit relates to Dedekind sums s(p,b) via deficit_b = b(b-1)(b-2)/12 - b^2 * s(p,b) (verified exactly for p=97, all primes q <= 23). Dedekind sum bounds (Rademacher: |s(p,q)| = O(q log q)) are WEAKER than what the document assumes.

**Critical growth-rate data for Sum |T_b - E[T_b]|/b^2:**

| p   | N   | Sum \|fluct\|/b^2 | Sum/N   | Sum/N^{1/2} |
|-----|-----|-------------------|---------|-------------|
| 29  | 28  | 8.53              | 0.30    | 1.61        |
| 53  | 52  | 22.13             | 0.43    | 3.07        |
| 97  | 96  | 54.30             | 0.57    | 5.54        |
| 199 | 198 | 158.47            | 0.80    | 11.26       |
| 397 | 396 | 394.56            | 1.00    | 19.83       |

The sum grows as ~N, NOT as N^{1/2+epsilon}. The document's claim "Sum |T_b - E[T_b]|/b^2 = O(N^{1/2+epsilon})" is off by a factor of N^{1/2}.

**However:** The SIGNED sum does cancel better:

| p   | N   | signed sum / N^2 |
|-----|-----|-----------------|
| 29  | 28  | 0.00443         |
| 53  | 52  | 0.00277         |
| 97  | 96  | 0.00080         |
| 199 | 198 | 0.00119         |
| 397 | 396 | -0.00011        |

The signed sum / N^2 does appear to tend to 0, which is all that's needed for the theorem. But proving signed cancellation over a sum of non-standard arithmetic functions indexed by ALL integers b <= N (not just primes) is a substantially harder problem than individual pointwise bounds. This would require either:

1. A large-sieve type inequality summing over all moduli b simultaneously, or
2. Equidistribution of {pa mod b / b} in a form uniform over both a and b, or
3. A Barban-Davenport-Halberstam type theorem for these specific sums.

None of these are "elementary" and none are proved or even precisely stated in the document.

### 4. Numerical Verification of Sum delta^2 / N^2

**STATUS: DOCUMENT VALUES CONFIRMED (with minor discrepancies at p=199).**

My independent computation:

| p   | My Sum_d2/N^2 | Document's value | Match? |
|-----|---------------|-----------------|--------|
| 11  | 0.02951       | 0.0295          | YES    |
| 29  | 0.04048       | (not listed)    | --     |
| 53  | 0.04481       | (not listed)    | --     |
| 97  | 0.04895       | 0.0490          | YES    |
| 199 | 0.04833       | 0.0483          | YES    |
| 397 | 0.05091       | 0.0509          | YES    |

Convergence to 1/(2pi^2) = 0.05066 is genuine but slow and non-monotonic (p=199 dips below p=97). The claim of "monotonic for p >= 47" in the document is contradicted by p=199 < p=97 in the ratio.

---

## Internal Contradictions in the Document

1. **Summary says "No Kloosterman bounds needed"** but Step 6 explicitly invokes "Direct Kloosterman: |T_b - E[T_b]| <= C * b^{3/2+epsilon}."

2. **Status says "Analytically proved (unconditional)"** but the Proof Roadmap section admits: "Step 6 is the remaining analytical challenge." These contradict each other.

3. **Step 3 derivation is abandoned mid-calculation** ("Hmm, this isn't clean. Let me redo.") and never completed rigorously. The "cleaner approach" appeals to empirical data and unspecified "standard Tauberian analysis."

4. **The "Proof Sketch" in Step 6(e)** says "the fluctuations cancel by the large sieve / equidistribution" without stating which large sieve inequality, for which sums, with what parameters. This is a claim, not a proof.

---

## Additional Issues

- **Lemma 1 (Step 1):** Correct and well-proved. The identity deficit_b = (1/2) Sum (a - pa mod b)^2 is elementary.

- **Corollary (deficit_b = 0 iff p = 1 mod b):** Correct. sigma_b = identity iff pa = a mod b for all coprime a, iff p = 1 mod b.

- **Composite contribution analysis:** The observation that composites dominate is correct and interesting, but the CRT decomposition claim "deficit_b = q2^2 * deficit_{q1} + q1^2 * deficit_{q2} + cross_term" is stated without proof.

- **Dedekind sum connection:** Verified exactly for p=97 and primes q = 5, 7, 11, 13, 17, 19, 23. This is correct and potentially useful, but the document does not exploit it to close Step 6.

---

## Verdict

### What IS proved:
1. deficit_b >= 0 for all b (elementary, correct).
2. deficit_b = 0 iff p = 1 mod b (elementary, correct).
3. A(N) = N^2/pi^2 + O(N log N) (standard, correct, but sloppily presented).
4. E_random[deficit_b] = S_2(b) - b^2*phi(b)/4 (correct).
5. Sum E_random[deficit_b]/b^2 = N^2/(4pi^2) + O(N log N) (correct).
6. Numerically, Sum delta_b^2 / N^2 converges to 1/(2pi^2) for primes up to 397 (verified independently).

### What is NOT proved:
6. **The fluctuation cancellation step.** The document's Kloosterman approach fails numerically (the pointwise bound is false). The signed cancellation is empirically true but unproved. No rigorous argument is given for Sum [T_b - E[T_b]]/b^2 = o(N^2).

### Classification:
- **The theorem is a CONJECTURE, not a theorem.** Supported by strong numerical evidence but with an analytical gap.
- **Overstatement level: HIGH.** The document says "Analytically proved (unconditional)" and "Classification: C2 (publication grade)" when the central step is unproved.
- **Correct status should be:** "Steps 1-5 proved. Step 6 (fluctuation cancellation) is an open problem. The constant 1/(2pi^2) is conjectural."

### Recommendations:
1. Downgrade status from "proved" to "conjectured with strong numerical support."
2. Explicitly acknowledge the gap in Step 6.
3. Clean up the Step 3 derivation.
4. Investigate whether Barban-Davenport-Halberstam or a mean-value theorem for Dedekind sums can close the gap.
5. Remove the self-contradictions (summary vs. roadmap).

---

**Audit performed:** Independent numerical recomputation of all key quantities. All code written from scratch without access to the CRT agent's code.
