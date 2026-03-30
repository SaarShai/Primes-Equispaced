# Adversarial Audit: B >= 0 Proof for M(p) <= -3 Primes

**Date:** 2026-03-30
**Role:** Hostile referee. Assume authors are wrong until proven otherwise.
**Files audited:**
- ALPHA_POSITIVE_PROOF.md
- DECORRELATION_PROOF.md
- B_VIA_MOBIUS.md

---

## Executive Summary

**VERDICT: The proof chain does NOT close. B >= 0 is NOT proved analytically.**

The claimed proof has three components. Here is the status of each:

| Component | Claimed Status | Actual Status |
|-----------|---------------|---------------|
| alpha > 0 for N >= 7 | "Proved" | **GAP: Proposition 4 (R < 0) is not proved for all N >= 7** |
| Decorrelation |corr(D_err, delta)| -> 0 | "Analytical proof" | **NOT PROVED unconditionally. Best unconditional bound is O(sqrt(log p)), which is USELESS** |
| Correction bound in Mobius approach | "Empirically bounded" | **NOT PROVED. Only verified to p = 500** |

The numerical verification for p = 13, 19, 31, 43, 53 CONFIRMS B >= 0 holds for these specific primes. But the analytical proof has fatal gaps.

---

## Detailed Findings

### 1. ALPHA_POSITIVE_PROOF.md

#### 1.1 What is rigorous

- **Proposition 1** (Cov identity): Cov(D,f) = 1/(12n) - sum(D^2)/(2n^2) - R/2.
  - VERIFIED EXACTLY with rational arithmetic for p = 13, 19, 31, 43, 53.
  - The algebra is straightforward and correct.

- **Proposition 2** (R decomposition): R = 1/3 + sum e(q).
  - Correct, standard computation.

- **Proposition 3** (Prime error): e(p) = -(p-1)/(6p).
  - Correct. Trivial calculation.

- **Identity sum(f) = n/2**: Correct by Farey symmetry f <-> 1-f.

#### 1.2 GAPS and ERRORS

**GAP 1 (CRITICAL): Proposition 4 claims R < 0 for all N >= 7, but the proof is incomplete.**

The proof says:
> "The composite contributions provide partial cancellation but cannot overcome the prime terms..."

This is hand-waving, not a proof. The argument claims composite e(q) are bounded and prime e(p) dominate, but:

- No rigorous bound is given for composite e(q).
- The claim "|e(q)| < 1/6 for all q >= 2" is stated without proof. For composite q, S_2(q)/q^2 depends on the prime factorization of q, and bounding e(q) requires careful analysis.
- The growth rate argument "~-pi(N)/6" is only asymptotic and does not cover small N.
- The actual proof is: "Verified computationally for N = 2 through 99." This is computation, not proof.

**For N >= 100, R < 0 is UNPROVED.** The asymptotic argument is plausible but not rigorous.

**SEVERITY: MEDIUM.** The gap could likely be closed with more careful analysis. For the B >= 0 application, we only need alpha > 0, and the data shows alpha grows rapidly with N. The gap matters in principle but probably not in practice.

**GAP 2 (MINOR): Proposition 5 claims sum(D^2)/(2n^2) -> 0 but does not prove it rigorously.**

The file correctly notes this follows from PNT via the Walfisz bound, but does not write out the steps. The claim "sum D^2/n^2 = O(exp(-c' sqrt(log N)))" requires translating the Mertens bound M(x) << x exp(-c sqrt(log x)) into a Farey discrepancy bound, which is standard (Franel-Landau theory) but not spelled out.

**SEVERITY: LOW.** This is a standard result and could be filled in with a textbook reference.

**GAP 3 (NOTATION): The table uses N = p, but B_VIA_MOBIUS uses N = p - 1.**

The alpha proof's table says n = 59 for p = 13, corresponding to F_13 (order 13). But B_VIA_MOBIUS defines N = p - 1, so it uses F_12 with n = 47. Since the theorem covers all N >= 7, this does not affect correctness, but the inconsistency is confusing and sloppy.

#### 1.3 What is actually proved

The alpha proof establishes:
- An exact algebraic identity for Cov(D, f) [RIGOROUS]
- R < 0 for N = 7 through 99 [COMPUTATION]
- R < 0 for N large enough [PLAUSIBLE but not rigorous]
- alpha > 0 for N = 7 through 99 [COMPUTATION]
- alpha > 0 for N sufficiently large [FOLLOWS from R < 0 asymptotically, but threshold not effective]

**Bottom line: alpha > 0 is PROVED for N = 7 to 99 (by exact computation) and is highly plausible for all N >= 7, but the proof for N >= 100 has a gap in Proposition 4.**

---

### 2. DECORRELATION_PROOF.md

This is the weakest link in the chain. The file is honest about the gaps (credit to the authors) but the claimed "ANALYTICAL PROOF" status in the header is misleading.

#### 2.1 Four approaches, none fully rigorous

**Approach 1 (Bilinear/Type I/II):**
- The initial bound (Section 2.2) is acknowledged as "too crude."
- The refined bound (Section 2.3) still loses to Cauchy-Schwarz.
- The key step (Section 2.4) invokes a "Random Sign Cancellation Lemma" whose proof sketch relies on BDH. The lemma as stated is NOT a standard result -- it is a heuristic dressed up as a lemma.
- **Conclusion: O(log(p)/p) bound is CONDITIONAL on BDH averaging, and even then the density-1 qualification (Section 2.8) means it does not hold for ALL primes.**

**Approach 2 (Spectral/Fourier):**
- Section 3.4 derives |corr| <= 1/n = O(1/p^2), then admits "this is the trivial Parseval bound."
- Section 3.5 tries to exploit the spectral gap but produces only |corr| <= sqrt(1 - rho^2(f, delta)).
- Section 3.6 then computes rho^2 ~ pi^2/(24 log N), which is SMALL, meaning ||delta_err|| is approximately ||delta||. The bound is useless: it gives |corr| <= 1 approximately.
- **The file acknowledges this at Section 6.2 line "this gives ||delta_err|| approximately ||delta||, which is too weak."**
- **Conclusion: Approach 2 gives NO meaningful decorrelation bound.**

**Approach 3 (BDH Averaging):**
- The average bound (Section 4.5) is a legitimate application of BDH. The RMS correlation O(sqrt(log p)/p) for most primes is plausible.
- The step from average to pointwise (Section 4.6) gives a density-1 result by Chebyshev's inequality.
- Section 4.7 claims the M(p) <= -3 condition helps, but the "proof sketch" is vague: "Mertens condition forces alpha > 0 and creates structural positive bias." This is not a proof.
- **Conclusion: O(sqrt(log p)/p) for density-1 set of primes [PLAUSIBLE]. Extension to ALL M(p) <= -3 primes is UNPROVED.**

**Approach 4 (Direct Permutation):**
- The identity sum_b T_b = 0 (Section 5.7) is RIGOROUS and important. Verified: sum f * D_err(f) = 0 by construction (D_err is orthogonal to linear functions).
- But the conclusion S = -sum_b U_b and |S| ~ sqrt(V/12) requires the quasi-independence of sigma_p mod b across different b, which is ASSUMED.
- **The file itself admits (Section 5.6 line 609): "without exploiting sign cancellation, the direct approach cannot beat the trivial bound."**
- **Conclusion: O(sqrt(log p)/p) under quasi-independence assumption, which is NOT PROVED.**

#### 2.2 The corrected theorem (Section 6.3)

The file commendably includes a "corrected" version that is honest about what is proved:

- (a) Unconditional: O(sqrt(log p)) -- this is WORSE than trivial and proves nothing
- (b) Spectral + orthogonality: |corr| <= 1 -- trivially true, proves nothing
- (c) Under BDH quasi-independence: O(sqrt(log p)/p) -- this WOULD prove decorrelation but requires an unproved assumption
- (d) For M(p) <= -3 specifically: empirical only

**Bottom line: There is NO unconditional proof of decorrelation. The best unconditional bound is O(sqrt(log p)), which GROWS and does not prove decorrelation at all.**

#### 2.3 Does decorrelation even matter for B >= 0?

The decorrelation is used in the chain: B_raw = alpha * C_raw + 2 * sum(D_err * delta). If |sum D_err * delta| << alpha * C_raw, then B_raw > 0.

But the numerical data tells a different story. At p = 13:
- alpha * C_raw = 8.394
- 2 * sum(D_err * delta) = -7.690
- B_raw = 0.704

The "residual" term is 92% of the "leading" term. This is NOT a small correction. The decorrelation framework suggests the residual should be negligible, but at p = 13, it nearly cancels the leading term. The proof would need to show B_raw > 0 with only 8% margin, which the decorrelation bound cannot provide even if it were proved.

At larger primes the margin grows (by p = 53, residual is 66% of leading), but the convergence is slow. The decorrelation approach cannot handle small primes where the margin is tight.

---

### 3. B_VIA_MOBIUS.md

#### 3.1 What is rigorous

- **Identity B + C = -2 sum(R * delta)**: Correct by definition.
- **Identity sum(x * delta) = C/2**: VERIFIED EXACTLY for all 5 test primes. This is the permutation identity and is rigorous.
- **Abel summation decomposition**: The formal manipulation is correct.
- **Leading term M(p-1) * C/2**: EXACT, follows from the Abel decomposition + the permutation identity. VERIFIED.

#### 3.2 GAPS and ERRORS

**GAP 4 (FATAL): The correction bound |correction/(-C/2)| < 1 for M(p) = -3 is NOT PROVED.**

This is the critical gap. The entire proof reduces to showing that the Abel correction Term2 satisfies correction_ratio > -1 for M(p) = -3 primes. The file states:

> "What remains to prove analytically: For M(p) = -3: Show that correction > -1."

And the approaches listed (A, B, C) are all sketches, not proofs:
- Approach A requires monotonicity of correction as a function of p, which is NOT established (the data shows correction goes from -0.88 at p=13 to -0.67 at p=19 to -0.44 at p=31 to +0.35 at p=43 -- not monotone until after p=31).
- Approach B (variance bound via Cauchy-Schwarz) is stated as a possibility but not carried out.
- Approach C (Dedekind sums) is pure speculation.

**The correction is verified only for 45 primes up to p = 500.** There is no analytical guarantee that the correction stays above -1 for all M(p) = -3 primes.

**SEVERITY: FATAL. This is the single point of failure for the entire proof.**

**GAP 5 (MODERATE): The Abel summation step needs careful justification.**

The decomposition R(x) = M(N) * {x} + sum M(k) * Delta_S_k(x) is stated without complete proof. The Abel summation itself is standard, but the specific form of Delta_S_k and its non-negativity need verification.

Delta_S_k(x) = S(x, floor(N/k)) - S(x, floor(N/(k+1))), where S(x, M) = sum_{m=1}^M {xm}.

Since floor(N/k) >= floor(N/(k+1)), we have S(x, floor(N/k)) >= S(x, floor(N/(k+1))) because we are adding non-negative terms {xm}. So Delta_S_k >= 0 is correct.

However, the step from sum_d mu(d) * S(x, floor(N/d)) to the Abel form requires careful handling of the sum over d. This is standard Abel summation but should be written out.

**GAP 6 (MINOR): The definition R(x) = -D(x) - x conflicts with standard notation.**

In Farey theory, the "discrepancy" D(f) = rank(f) - n*f is standard. Writing R(x) = -D(x) - x introduces a non-standard quantity that can cause confusion, especially since R is also used for the quantity sum(f^2) - n/3 in the alpha proof. Two different quantities both called R.

---

### 4. Does the Chain Close?

The intended proof chain:

1. alpha > 0 (from ALPHA_POSITIVE_PROOF.md)
2. |corr(D_err, delta)| -> 0 (from DECORRELATION_PROOF.md)
3. Therefore B_raw = alpha * C_raw + 2 * sum(D_err * delta) > 0 for large enough p
4. For small p, verify directly

**DOES NOT CLOSE because:**

- Step 2 is not proved unconditionally. The best unconditional bound is trivial.
- Even if step 2 were proved, the rate of decorrelation (at best O(sqrt(log p)/p) under BDH) combined with the rate of alpha growth (alpha ~ log p by the data) would give B_raw/C_raw >= c/log(p) - O(log(p)^{3/2}/p). This is positive for p > p_0 where p_0 depends on the implicit constants, which are NOT computed. So p_0 is not effective.
- For p <= p_0, direct verification would be needed, but p_0 is unknown.

**Alternative chain via Mobius (B_VIA_MOBIUS.md):**

1. sum(R * delta) = M(p-1) * C/2 + correction [EXACT]
2. For M(p) <= -3: M(p-1) <= -2, so leading term <= -C [EXACT]
3. B >= 0 iff correction_ratio > -(|M(p)| - 2) [EXACT]
4. For M(p) = -3: need correction_ratio > -1 [NOT PROVED]
5. For M(p) <= -4: need correction_ratio > -2 [HIGHLY PLAUSIBLE but NOT PROVED]

**This chain ALSO does not close because step 4 is unproved.**

---

### 5. Numerical Verification Results

For the 5 requested primes, ALL identities check out exactly:

| p | M(p) | n | alpha | |corr(D_err,delta)| | B_raw | correction_ratio | B>=0 |
|---|------|---|-------|---------------------|-------|------------------|------|
| 13 | -3 | 47 | 1.430 | 0.279 | 0.704 | -0.880 | YES |
| 19 | -3 | 103 | 2.302 | 0.319 | 4.269 | -0.668 | YES |
| 31 | -4 | 279 | 3.698 | 0.272 | 62.006 | -0.444 | YES |
| 43 | -3 | 543 | 3.896 | 0.250 | 112.062 | +0.354 | YES |
| 53 | -3 | 831 | 4.102 | 0.221 | 169.612 | +0.400 | YES |

**Note on n values:** My computation uses N = p - 1 (consistent with B_VIA_MOBIUS.md), giving n = 47 for p = 13. The ALPHA_POSITIVE_PROOF.md table claims n = 59 for p = 13, which corresponds to N = p = 13 (F_13 not F_12). This notation inconsistency does not affect the theorem (which covers all N >= 7) but is sloppy.

Verified EXACTLY (rational arithmetic):
- Cov(D,f) = 1/(12n) - sum(D^2)/(2n^2) - R/2 : **EXACT for all 5 primes**
- sum(x * delta) = C/2 : **EXACT for all 5 primes**
- B_raw = alpha * C_raw + 2 * sum(D_err * delta) : **EXACT for all 5 primes**
- sum(R * delta) = -(B + C)/2 : **EXACT for all 5 primes**

The decorrelation |corr(D_err, delta)| ranges from 0.22 to 0.32 for these primes. This is NOT small. It is decreasing with p but slowly (NOT the O(p^{-0.475}) claimed in the decorrelation file for these small primes).

---

### 6. Specific Answers to Audit Questions

**Q: Is alpha > 0 proof rigorous?**
A: The Cov identity is rigorous. The conclusion alpha > 0 for all N >= 7 has a gap: R < 0 for N >= 100 is not proved (only verified to N = 99). The gap is fillable but not currently filled.

**Q: Is the decorrelation O(sqrt(log p)/p) proved or heuristic?**
A: HEURISTIC. None of the 4 approaches produces an unconditional proof. The best unconditional bound (Approach 2) is O(sqrt(log p)), which is trivially useless. The O(sqrt(log p)/p) bound (Approaches 1, 3, 4) all require either BDH averaging (giving density-1 only) or quasi-independence assumptions (unproved). The file itself admits this in the corrected Section 6.3.

**Q: Which of the 4 approaches is rigorous?**
A: None are fully rigorous. Approach 2 gives an unconditional but useless bound. Approaches 1, 3, 4 give useful bounds but are conditional. The most promising is Approach 3 (BDH averaging) which at least gives a density-1 result.

**Q: Is sum(R*delta) = M(p-1)*C/2 + correction an EXACT identity or approximate?**
A: The Abel decomposition is EXACT. sum(R*delta) = M(p-1) * C/2 + Term2 where Term2 = sum_{k<N} M(k) * sum_x Delta_S_k * delta. This is verified exactly. The LEADING TERM extraction is rigorous.

**Q: Is the correction bound |correction| < 1 for M(p) = -3 proved or just verified?**
A: JUST VERIFIED to p = 500 (45 primes). NOT PROVED analytically. This is the fatal gap.

**Q: Does the chain actually close?**
A: NO. Neither the decorrelation chain nor the Mobius chain produces a complete analytical proof. Both reduce to bounding a quantity that is only controlled empirically.

---

### 7. Summary of All Gaps

| # | Gap | Severity | Location |
|---|-----|----------|----------|
| 1 | R < 0 for N >= 100 not proved | MEDIUM | ALPHA_POSITIVE_PROOF Prop 4 |
| 2 | sum(D^2)/(2n^2) -> 0 not spelled out | LOW | ALPHA_POSITIVE_PROOF Prop 5 |
| 3 | N = p vs N = p-1 notation conflict | LOW | Between files |
| 4 | Correction ratio > -1 for M(p)=-3 not proved | FATAL | B_VIA_MOBIUS |
| 5 | Abel summation details incomplete | LOW | B_VIA_MOBIUS |
| 6 | R notation overloaded | LOW | Between files |
| 7 | No unconditional decorrelation proof | FATAL | DECORRELATION_PROOF |
| 8 | "Analytical proof" header is misleading | MODERATE | DECORRELATION_PROOF header |

---

### 8. What IS Established

Despite the gaps, the following IS firmly established:

1. **Exact algebraic identities** connecting Cov(D,f), R, D^2, alpha, B_raw, C_raw, and the Mobius function. These are verified with exact rational arithmetic and are not in doubt.

2. **B >= 0 for all M(p) <= -3 primes up to p = 500** (45 primes), by direct computation.

3. **The Mobius leading term** M(p-1) * C/2 is exact and provides the correct "reason" why B >= 0: the Mertens function being sufficiently negative forces the Farey discrepancy sum to have the right sign.

4. **The correction is empirically well-behaved**: worst case is -0.88 at p = 13, and it trends positive for larger primes. A proof that the correction is bounded is plausible but absent.

5. **The alpha > 0 result is highly robust**: alpha grows monotonically for p >= 13 and is verified exactly through N = 99. A complete proof is within reach.

---

### 9. Recommendations

1. **Drop the word "proof" from the decorrelation file header.** Replace "ANALYTICAL PROOF" with "ANALYTICAL FRAMEWORK (conditional)."

2. **Close Gap 1** by proving R < 0 for all N >= 7 rigorously. This likely requires bounding sum |e(q)| for composite q and showing the prime contributions dominate. The asymptotic argument in Proposition 4 can be made effective with work.

3. **Close Gap 4** by either:
   - (a) Proving an explicit upper bound on |Term2|/C that is less than 1. The variance approach (Approach B in B_VIA_MOBIUS) seems most promising.
   - (b) Extending the computational verification to cover all M(p) = -3 primes up to some effective threshold where an asymptotic argument takes over.
   - (c) Finding a direct proof that does not go through the correction bound (e.g., a monotonicity argument for B_raw/C_raw as a function of p).

4. **Be honest about the status.** The current state is: strong empirical evidence + exact identities + conditional analytical bounds. This is interesting and publishable as a CONJECTURE with supporting evidence, not as a theorem.

---

**Classification:** This audit rates the overall B >= 0 claim as:
- **Verification status: 🔬 Unverified** (Step 1 partially passed for the identities; the proof chain itself fails Step 1)
- **Autonomy: C** (collaborative)
- **Significance: Level 1** (interesting conjecture with strong evidence, not a proved theorem)

---

*Auditor's note: The identities are beautiful and the Mobius reformulation is genuinely insightful. The leading term extraction via Abel summation is the right approach. But a proof is a proof, and what is presented here is not one. The gap between "verified for 45 primes" and "proved for all primes" is not small -- it is the entire content of the theorem.*
