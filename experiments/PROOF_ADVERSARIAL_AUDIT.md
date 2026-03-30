# ADVERSARIAL AUDIT: Sign Theorem Proof
## Date: 2026-03-29
## Role: Hostile Referee
## Verdict: PROOF HAS MULTIPLE FATAL GAPS

---

## Executive Summary

The claimed proof of "For every prime p >= 11 with M(p) <= -3: DeltaW(p) < 0 (unconditionally)" contains **at least 5 fatal flaws**, **3 serious gaps**, and **several overstatements**. The proof as stated is **NOT valid**. What exists is a plausible heuristic argument supported by extensive computation, not a rigorous proof.

The core problem: the authors repeatedly encounter circularity and impossibility of bounding the cross term B analytically, then paper over these gaps with empirical observations and hand-waving about "structural correlations." The honest summary is: DeltaW(p) <= 0 is verified computationally to p = 100,000 and there are promising analytical ingredients, but no complete analytical proof exists for the tail p > 100,000.

---

## FATAL FLAW 1: Step 2 (B >= 0) is PURELY EMPIRICAL --- Not Proved

**Severity: FATAL**

The claim states: "Bypass: B >= 0 for M(p) <= -3 (verified for 210 primes to p ~ 3000), so suffices C+D > A+1."

This is an empirical observation, NOT a proof. The project's own files confirm this repeatedly:

- UNCONDITIONAL_EXTENSION.md line 264: "B_raw >= 0 (verified for 17,984 primes but not proved)"
- COMPLETE_ANALYTICAL_PROOF.md line 515: "B >= 0 (which is conjectured but not proved)"
- B_geq_0_attack.py line 815: "A proof of B >= 0 remains open"
- FINAL_PROOF_ATTEMPT.md Section 1.8: B+C > 0 for all p requires "proving quasi-random sign cancellation in Kloosterman-type sums" which is OPEN

The proof outline presents this step as if it can be "bypassed" by showing C+D > A+1. But this bypass itself depends on analytical bounds for D/A and C/A that have their own fatal problems (see below). **Without B >= 0, the entire analytical argument for p > 100,000 collapses.**

The Cauchy-Schwarz lower bound B_raw >= -2 sqrt(old_D_sq * delta_sq) is acknowledged in the project files to give a bound of order -N^{5/2}, which GROWS faster than all the positive terms. This is explicitly stated in COMPLETE_ANALYTICAL_PROOF.md around line 690: "the middle term -0.234 N^{5/2} GROWS FASTER than N^2. This means the Cauchy-Schwarz bound on B is too loose!"

**Conclusion: Step 2 is a conjecture, not a proved result. Labeling the bypass "suffices C+D > A+1" disguises this gap.**

---

## FATAL FLAW 2: The |1 - D/A| <= K/p Bound is CIRCULAR and WRONG

**Severity: FATAL**

The proof claims (Step 4): "1-D/A = O(exp(-c sqrt(log p))) from Walfisz effective Mertens bound (El Marraki 1995)."

The project's OWN explicit_P0.py file (lines 18-25) explicitly refutes this:

> "Prior work claimed |1 - D/A| <= K/p with K = 12. THIS IS WRONG. The actual scaling is |1 - D/A| ~ C_M(p)/sqrt(p) where C_M depends on the Mertens function M(p)."
> "Since M(p) = O(sqrt(p)) unconditionally (trivially), |1 - D/A| = O(1) -- it doesn't even go to zero in the worst case!"

The correct scaling is |1 - D/A| ~ |M(p)| * const / p, which for the trivial unconditional bound M(p) = O(p/log(p)) gives |1 - D/A| = O(1/log(p)) at best. This is NOT the claimed O(exp(-c sqrt(log p))).

Moreover, the "K = 12" constant used in COMPLETE_ANALYTICAL_PROOF.md is fitted empirically from data for p <= 6000 with a "50% safety margin." This is NOT a proved bound. The authors' own analysis shows p * |1-D/A| is NOT bounded -- it grows. The sqrt(p) * |1-D/A| quantity appears more stable, suggesting |1 - D/A| ~ C/sqrt(p), but even this is not proved.

**The circularity problem**: The identity D/A = 1 - (B + C + n'^2 DeltaW)/dilution_raw involves DeltaW itself. So bounding D/A requires knowing DeltaW, which is what we are trying to prove is negative. The COMPLETE_ANALYTICAL_PROOF.md acknowledges this circularity explicitly at multiple points (lines 120, 475, 522, 702, 759) and never resolves it.

**The El Marraki/Walfisz connection claimed in Step 4 is not substantiated anywhere in the proof files.** The Walfisz bound |M(N)| <= N * exp(-c * sqrt(log N)) is an unconditional bound on the Mertens function, but the proof never shows HOW this translates to a bound on 1 - D/A. The claimed "1 - D/A = O(exp(-c sqrt(log p)))" appears to be fabricated -- it does not follow from any derivation in the project files.

**Conclusion: The D/A bound is either circular (uses DeltaW <= 0 to prove DeltaW <= 0) or empirically fitted without rigorous justification. The connection to the Walfisz/El Marraki bound is asserted without proof.**

---

## FATAL FLAW 3: Step 3 (C/A >= c/log^2(p)) Depends on Unproved Lemma

**Severity: FATAL**

The C/A lower bound chain has the following structure:

1. delta_sq = Sum delta(f)^2 >= Sum over prime b of (b^2-1)/(12b)
2. The restriction to prime b uses: deficit_m(b) >= deficit_2(b) = (b^3-b)/24 (Lemma 2, "minimality of multiplication by 2")
3. Lemma 2 is stated as: "Verified by exact computation for all primes b <= 37"

**Lemma 2 is NOT proved for b >= 41.** It is verified computationally for small primes only. The "spectral" explanation given is heuristic: "chi(2) has the largest Re chi(m) among nontrivial characters" is a claim about character sums that is neither proved nor referenced.

The STEP2_PROOF.md acknowledges this at line 274: "The minimality of multiplication by 2 (Lemma 2, computational for b <= 37)."

For b >= 41, the proof falls back to weaker bounds. The COMPLETE_ANALYTICAL_PROOF.md at line 355 states: "For b >= 41: the lemma can be avoided by using a weaker bound. Since deficit_m(b) >= 1 for any m != 1 (mod b)." But deficit_m(b) >= 1 is vastly weaker than deficit_m(b) >= (b^3-b)/24, and it is not clear that the weaker bound suffices for the quantitative claim C/A >= pi^2/(432 log^2 N).

Actually, re-reading the proof more carefully: the PNT-based lower bound on delta_sq (Theorem 2 in STEP2_PROOF.md, giving delta_sq >= N^2/(48 log N)) does NOT actually require Lemma 2 for all b. It only needs deficit_b >= (b^3-b)/24 for prime b where p != 1 mod b. For such b, since p is a prime different from b, we have p mod b is some m != 0, 1. So we need deficit_m(b) >= (b^3-b)/24 for ALL such m.

But wait -- the proof ONLY claims this when m = p mod b, and uses Lemma 2 which says the minimum over all m != 1 is achieved at m = 2. If Lemma 2 fails for some large prime b, then there could exist m with deficit_m(b) < (b^3-b)/24, invalidating the sum bound.

**The claim deficit_2 is minimal is plausible but unproved.** Without it, one needs a different lower bound on the per-denominator contributions, and the factor of (b^3-b)/24 may need to be replaced by something smaller, potentially changing the final constant.

**Mitigation**: Even if Lemma 2 fails, the bound deficit_b >= 1 for m != 1 gives delta_sq >= O(N/log N) (sum of 1/(12b^2) over primes with b-1 contribution). This is much weaker: delta_sq >= cN/log N instead of N^2/(48 log N). The ratio C/A would then be O(1/(N log N)) instead of O(1/log^2 N), which would NOT suffice for the crossover argument.

**Conclusion: The quantitative C/A bound requires Lemma 2 (minimality of 2-deficit) which is verified only for b <= 37 and not proved in general.**

---

## FATAL FLAW 4: Step 5 -- "For Large p" Has No Proved Explicit P_0

**Severity: FATAL**

The claim "Since 1/log^2(p) >> exp(-c sqrt(log p)), C/A > 1-D/A for large p" requires:

(a) Both sides to be proved bounds (they are not -- see Flaws 2 and 3)
(b) An explicit P_0 such that the inequality holds for all p > P_0
(c) The computational base (Step 6) to cover all p <= P_0

The COMPLETE_ANALYTICAL_PROOF.md computes P_0 ~ 65,500 using K = 12. But K = 12 is an EMPIRICAL constant, not a proved one (see Flaw 2). The entire crossover calculation is therefore built on sand.

Even if we accept K = 12 and C/A >= pi^2/(432 log^2 N), the crossover equation p > 525.2 log^2(p) gives P_0 ~ 65,500. The computational base covers p <= 100,000, which does overlap. BUT:

- The computational base verifies DeltaW <= 0, not the specific analytical conditions (D/A + C/A >= 1 or B/A + C/A + D/A >= 1).
- The analytical argument for p > P_0 requires B >= 0 (which is not proved) OR requires D/A + C/A > 1 (which uses the circular/unproved D/A bound).

So even with overlap, the analytical regime is not self-supporting.

**Conclusion: There is no proved P_0 because the analytical bounds feeding into its calculation are not proved.**

---

## FATAL FLAW 5: The "Proof" is Actually a Computation + Heuristic Argument

**Severity: FATAL (structural)**

The proof as presented in the project files acknowledges its own incompleteness at every turn. The FINAL_PROOF_ATTEMPT.md summary table (line 227-237) explicitly lists:

| Question | Status |
|---|---|
| B+C > 0 for all p | OPEN |
| |R| < 1 for all p | OPEN |
| DeltaW <= 0 for all p | OPEN |
| D/A ~ 1 with effective error | OPEN |

The COMPLETE_ANALYTICAL_PROOF.md itself goes through MULTIPLE failed attempts:
- Section 6.2: "THE RESOLUTION" -- then discovers the CS bound on B is too loose (line 690)
- Section 7.1: Acknowledges "beta bound is too loose" (line 929)
- Section 7.3: Falls back to "definitive version" that REQUIRES B >= 0 from computation

The final "clean proof" (Theorem 6, starting line 789) splits into:
- Regime 1 (p <= 100,000): computation -- FINE
- Regime 2 (p > 100,000): claims to use "self-consistent inequality" but ultimately requires B >= 0 which is not proved

**Conclusion: There is no complete proof. There is a verified computation for p <= 100,000 and a heuristic analytical argument for p > 100,000 with at least one unproved ingredient (B >= 0 or the non-circular D/A bound).**

---

## SERIOUS GAP 1: The Four-Term Decomposition "Lean-Verified" Claim

**Severity: SERIOUS**

Step 1 claims: "Four-term decomposition (Lean-verified): DeltaW = A - B - C + 1 - D - 1/n'^2"

The Lean files contain `sorry` in the key theorems:
- SignTheorem.lean line 81: `sign_theorem_conj` uses `sorry`
- SignTheorem.lean line 118: `ratio_test` uses `sorry`
- BridgeIdentity.lean: contains 1 `sorry`

The `native_decide` verifications only cover specific small primes (13, 19, 31, 43, 47, 53, 59, 61). The general four-term decomposition identity and the ratio test are NOT Lean-verified -- they have `sorry` placeholders.

Moreover, the formula in the claim "DeltaW = A - B - C + 1 - D - 1/n'^2" does not match the formula in the proof files. The standard decomposition is:

    DeltaW = (A - B - C - D) / n'^2

where A = dilution_raw, B = B_raw = 2 Sum D*delta, C = delta_sq, D = new_D_sq (all divided by n'^2). The "+1" and "-1/n'^2" terms in the claimed formula are suspicious and may indicate sign/normalization confusion.

**Conclusion: The Lean formalization is incomplete. The `sorry`-free theorems only cover small-prime verifications via `native_decide`, not the general algebraic identities.**

---

## SERIOUS GAP 2: The "Deficit-Dedekind" Connection

**Severity: SERIOUS**

Step 3 references a "deficit-Dedekind lemma" that provides C/A >= c/log^2(p). The files reference a connection between deficits and Dedekind sums (BC_positive_proof.py mentions "The deficit approach via Dedekind sums" as approach 10). However:

1. The Dedekind sum connection is mentioned but never proved. The deficit identity (deficit_b = half sum of (a - sigma(a))^2) is proved, but calling this a "Dedekind connection" is misleading -- it is a simple algebraic identity about permutations.

2. The key step "min deficit per prime q is D_q(2) = q(q^2-1)/24" is Lemma 1 (exact formula for multiplication by 2), which IS proved. But the claim that this is the MINIMUM over all multipliers (Lemma 2, minimality) is only verified for q <= 37.

3. The "summing over primes gives delta^2 >= N^2/(24 log N)" -- the actual proved bound is delta_sq >= N^2/(48 log N) (with a factor of 48, not 24), and this uses the PNT in a standard way. The factor discrepancy between the claim (24) and the proof (48) suggests sloppiness.

**Conclusion: The deficit identity is correct. The Dedekind connection is nominal. The minimality of the 2-deficit is unproved in general.**

---

## SERIOUS GAP 3: Restriction to M(p) <= -3

**Severity: SERIOUS**

The theorem is stated for primes with M(p) <= -3 only. This is a significant restriction. The proof files show that:

- B+C = 0 exactly for p = 5 and p = 7 (PROOF_BREAKTHROUGH.md, Section 4)
- The M(p) <= -3 condition is used to ensure B >= 0 empirically (from the "B >= 0 for M(p) <= -3" claim verified for 210 primes)

But this raises the question: what happens for primes with M(p) > -3? Are there primes where DeltaW > 0? The computational data shows DeltaW <= 0 for ALL primes up to 100,000, not just those with M(p) <= -3. So why restrict?

The restriction appears to be an artifact of the proof strategy (needing B >= 0 which is easier to verify/believe when M(p) is sufficiently negative). This suggests the theorem as stated is weaker than the data supports, and the M(p) <= -3 condition is a crutch for the unproved B >= 0 step.

---

## OVERSTATEMENTS AND MINOR ISSUES

### 1. "Unconditionally" -- Misuse of Term

The claim says "unconditionally" but the proof:
- Uses K = 12 fitted from data (not proved unconditionally)
- Uses Lemma 2 verified only for b <= 37
- Uses B >= 0 verified only computationally
- Has unresolved circularity in the D/A bound

Nothing about this proof is unconditional. The only unconditional results are the algebraic identities and the rearrangement inequality.

### 2. Effective Mertens Bound Misapplication

The claim references "El Marraki 1995: |M(x)| <= 0.644x/log(x)." This is a valid result, but nowhere in the proof files is it shown how this translates to 1 - D/A = O(exp(-c sqrt(log p))). The Walfisz bound gives |M(N)| <= N exp(-c sqrt(log N)), and El Marraki gives |M(x)| <= 0.644x/log(x). These are different bounds with different ranges of usefulness. The proof does not specify which is being used or how.

### 3. Computational Base Issues

The claim says "verified for all 4,617 M(p) <= -3 primes to p = 100,000." But the proof strategy requires the analytical argument to take over before the computational base ends. The analytical crossover at P_0 ~ 65,500 is computed using unproved constants. If the true P_0 is larger than 100,000, there is a gap.

### 4. Sign Convention Confusion

The claimed decomposition "DeltaW = A - B - C + 1 - D - 1/n'^2" does not match the standard form in the project files, which is DeltaW = (A - B - C - D)/n'^2 where A, B, C, D are specific sums. The "+1" and "-1/n'^2" terms appear nowhere in the derivations and may indicate the claim was written from memory rather than from the actual proof.

---

## WHAT ACTUALLY EXISTS (Honest Assessment)

1. **Proved (unconditional)**:
   - The four-term decomposition identity (algebraic, verified in Python and partially in Lean)
   - deficit_b >= 0 via rearrangement inequality, with equality iff p = 1 mod b
   - deficit_2(b) = (b^3-b)/24 for odd prime b (Lemma 1)
   - delta_sq > 0 for all p >= 5
   - delta_sq >= N^2/(48 log N) for N >= 100 (using PNT + Lemma 2 for b <= 37 + weaker universal bounds for larger b -- though the exact constant needs checking)
   - C/A >= pi^2/(432 log^2(N)) -- depends on Lemma 2

2. **Proved (computational)**:
   - DeltaW(p) <= 0 for all primes p in [11, 100,000] -- zero violations
   - B+C > 0 for all primes in [11, 1000]
   - B >= 0 for all primes with M(p) <= -3 up to p ~ 200,000
   - D/A + C/A > 1 for all primes in [11, 2000]

3. **NOT proved (open)**:
   - B >= 0 for all primes (or even for all M(p) <= -3 primes)
   - |1 - D/A| <= K/p with explicit K (circular or empirical)
   - Lemma 2 (minimality of 2-deficit) for b >= 41
   - The crossover: that analytical bounds cover p > P_0 for some P_0 <= 100,000
   - The Sign Theorem itself for p > 100,000

---

## VERDICT

**The claimed proof is INVALID as presented.** It contains:

- 5 fatal flaws (empirical steps presented as proved, circularity, unproved lemmas, no explicit P_0, incomplete structure)
- 3 serious gaps (Lean sorry's, Dedekind connection unclear, artificial M(p) restriction)
- Multiple overstatements ("unconditionally", misapplied Mertens bounds)

**What can be honestly claimed:**

> "DeltaW(p) <= 0 for all primes p in [11, 100,000] (verified by exact computation, zero violations among 9,592 primes). For larger p, we have promising but incomplete analytical ingredients: a lower bound C/A >= pi^2/(432 log^2 N) from the rearrangement inequality and PNT (modulo the minimality of the 2-deficit for large primes), and strong empirical evidence that B >= 0 and D/A ~ 1. A complete analytical proof for the tail remains open, with the key obstruction being the non-negativity of the cross term B."

This is a strong computational result with interesting analytical partial progress. It is NOT a proof.

---

## RECOMMENDATIONS

1. **Stop claiming this is proved.** Be explicit about what is computational vs. analytical.
2. **Close Lemma 2** rigorously for all primes, or replace it with a universal lower bound.
3. **Resolve the D/A circularity.** Either find a non-circular bound on D/A or abandon the four-term approach for the analytical tail.
4. **Prove B >= 0** or find a proof strategy that does not require it. The Kloosterman sum approach mentioned in FINAL_PROOF_ATTEMPT.md is the right direction but appears to be genuinely hard.
5. **Close the Lean sorry's** in SignTheorem.lean and BridgeIdentity.lean.
6. **Fix the sign convention** in the claim statement to match the actual decomposition.
7. **Extend the computational base** to p = 10^6 or beyond to provide a larger safety margin while the analytical gaps are worked on.

---

*Audit conducted by an independent adversarial reviewer with access to all project files. Every finding is supported by specific file references and line numbers.*
