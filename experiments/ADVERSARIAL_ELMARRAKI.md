# ADVERSARIAL AUDIT: El Marraki-Based Proof of B >= 0 for M(p) <= -3

## Date: 2026-03-30
## Role: Hostile Referee
## Scope: ELMARRAKI_CORRECTION.md claims unconditional proof that correction/C' < 1/2 for all primes with M(p) <= -3.

---

## Executive Summary

**VERDICT: The proof has CRITICAL GAPS in Part II. Parts I and III are sound.**

| Part | Claim | Verdict |
|------|-------|---------|
| Part I (p=13, 19) | Exact arithmetic | VERIFIED |
| Part II (p >= 43, M(p) = -3) | Alpha-decorrelation with El Marraki | CRITICAL GAPS |
| Part III (M(p) <= -4) | Leading-term dominance | SOUND (with caveats) |

The proof is NOT unconditional as claimed. Part II relies on:
1. A monotonicity claim verified only numerically, not proved
2. Effective constants that are never explicitly computed
3. A decorrelation framework (DECORRELATION_PROOF.md) that itself relies on either BDH averaging or unproved quasi-independence

---

## 1. Part I Audit: Exact Arithmetic (p = 13, 19)

### 1.1. p = 13 Verification

**Claim:** correction/C' = 2984/6781, and 2*2984 = 5968 < 6781.

**Check:** 2 * 2984 = 5968. 6781 - 5968 = 813 > 0. CORRECT.

**Cross-check with B_EXACT_AUDIT.md:** That file reports correction/C' = 0.4401 at p=13. Check: 2984/6781 = 0.44010... MATCHES.

**Check the formula used:** The proof uses B' = (|M(N)| - 1) * C' - 2 * correction, which is the CORRECTED formula from B_EXACT_AUDIT.md (Section "The Correct Formula"). The earlier wrong formula B' = (|M(N)| - 2) * C' - 2 * correction has been fixed. CORRECT.

At p=13: M(N) = M(12) = -2, so B' = (2-1)*C' - 2*correction = C' - 2*correction. B' > 0 iff correction < C'/2 iff correction/C' < 1/2. This is consistent.

**Verify B' = 271/385:** From B' = C' - 2*correction = 6781/1155 - 2*2984/1155 = 6781/1155 - 5968/1155 = 813/1155 = 271/385. CHECK: 813/1155 = 271/385? 271*1155/385 = 271*3 = 813. YES, CORRECT.

**VERDICT: Part I for p=13 is VERIFIED.**

### 1.2. p = 19 Verification

**Claim:** B' = 2905619/680680, and 2*2923756 = 5847512 < 8753131.

**Check:** 2*2923756 = 5847512. 8753131 - 5847512 = 2905619 > 0. CORRECT.

**Cross-check:** B' = C' - 2*correction = 8753131/680680 - 2*2923756/680680 = (8753131 - 5847512)/680680 = 2905619/680680. MATCHES the claimed B'.

**Cross-check with B_EXACT_AUDIT.md:** That file reports correction/C' = 0.3340 at p=19. Check: 2923756/8753131 = 0.33403... MATCHES.

**VERDICT: Part I for p=19 is VERIFIED.**

---

## 2. Part II Audit: Alpha-Decorrelation for p >= 43, M(p) = -3

This is where the proof has SERIOUS PROBLEMS.

### 2.1. The Proof Strategy

The proof decomposes B' = alpha*(C'+1) + 2*sum D_err*delta, then shows the residual is smaller than the leading term by bounding the ratio:

    r(p) = 2*||D_err||*sqrt(C') / (alpha*(C'+1))

The claim is that r(p) < 1 for all p >= 43 with M(p) = -3.

### 2.2. FLAW 1: The Cauchy-Schwarz bound is NOT sharp enough

The proof applies Cauchy-Schwarz to get:

    |sum D_err * delta| <= ||D_err|| * sqrt(C')

Then the ratio r(p) is bounded. BUT: The Cauchy-Schwarz inequality |sum D_err*delta| <= ||D_err||*||delta|| = ||D_err||*sqrt(C') is an UPPER BOUND on the sum. The proof then shows this upper bound divided by alpha*(C'+1)/2 is < 1.

**The issue:** The proof's TABLE (Section 3.6) reports:

    p = 13: ratio = 0.934
    p = 107: ratio = 0.500

These ratios use the Cauchy-Schwarz UPPER BOUND, not the actual value. The column "|sum D_err*delta|" is actually ||D_err||*sqrt(C'), not the true inner product. Let me check:

At p=13: The actual B' = 271/385 = 0.7039. From B' = alpha*(C'+1) + 2*sum D_err*delta: 0.7039 = 1.812*(5.87+1) + 2*sum D_err*delta = 12.44 + 2*sum D_err*delta. So sum D_err*delta = (0.7039 - 12.44)/2 = -5.87.

But the table says |sum D_err*delta| = 4.967. This is NOT the Cauchy-Schwarz bound -- it seems to be the actual computed value. IF so, the ratio 0.934 means the actual residual is 93.4% of the leading term at p=13, which is dangerously close to 1.

**Wait** -- actually: B' = alpha*(C' - M(N) - 1) + 2*sum D_err*delta (from Identity E in Section 1.3). For M(N) = -2: B' = alpha*(C'+1) + 2*sum D_err*delta. So the ratio should be |2*sum D_err*delta| / (alpha*(C'+1)). The claim is this ratio < 1, meaning the residual does not overwhelm the leading term.

At p=13: ratio = 2*4.967/(1.812*6.87) = 9.934/12.45 = 0.798. But the table says 0.934. Let me re-check: alpha*(C'+1)/2 = 1.812*6.87/2 = 6.226. Ratio = 4.967/6.226 = 0.798. Does not match 0.934.

**FINDING: The table values are INCONSISTENT with the formula.** If ratio = |sum D_err*delta| / (alpha*(C'+1)/2), then at p=13 I get 0.798, not 0.934. This could mean:
- The table uses a different formula
- The "sum D_err*delta" column IS the Cauchy-Schwarz bound, not the actual value
- There is an arithmetic error

**This inconsistency is a RED FLAG.** The proof needs to clarify what exactly is being computed in the table.

### 2.3. FLAW 2: Monotonicity of r(p) is NOT proved

Section 3.7 claims the ratio is "monotonically decreasing." The proof says:

> "The monotonic decrease for all p >= 13 is verified by the computation above."

This is COMPUTATION, not PROOF. The table has only 6 data points. The claim "monotonically decreasing for all p >= 13" is an extrapolation from 6 points. While the asymptotic scaling O(sqrt(log N)/sqrt(N)) would eventually guarantee decrease, the proof needs to show monotonicity for ALL p >= 43, not just at 6 sample points.

**What could go wrong:** Between two tested primes (say p=107 and p=199), there could be a prime q with M(q) = -3 where the ratio spikes above 1. The tested points miss such a spike.

**Mitigation:** The proof says it was verified "for all M(p)=-3 primes to p=20000" by streaming computation. If true, this closes the gap empirically up to p=20000. But:
- This is computational verification, not analytical proof
- The claim "PROVED (unconditional, fully analytical)" in the header is OVERSTATED
- What about p > 20000?

### 2.4. FLAW 3: Effective constants are never pinned down

Section 3.5 establishes the scaling:

    ||D_err|| = O(N^{3/2}/sqrt(log N))
    sqrt(C') = O(N)
    alpha = O(N/log N)

Leading to r(p) = O(sqrt(log N)/sqrt(N)).

But the CONSTANTS in these big-O expressions are never computed explicitly. The proof says (Section 3.8):

> "For N = 42: sqrt(42 * log(42)) = sqrt(157) = 12.5. If A/B <= 12.5 * 0.65 = 8.1, then ratio < 0.65 for N >= 42."

This is BACKWARDS reasoning. You cannot conclude A/B <= 8.1 from the numerical observation that the ratio is 0.65 at p=43. The whole point of the analytical proof is to DERIVE bounds on A and B from first principles, then show the ratio is < 1. Instead, the proof:
1. Observes the ratio is 0.65 at p=43 numerically
2. Asserts "this is consistent with the effective constants"
3. Claims the proof is done

This is circular. The proof uses computation at p=43 to validate the analytical bound, but the analytical bound was supposed to REPLACE the computation.

### 2.5. FLAW 4: The El Marraki bound is used loosely

Section 3.8 claims:

    sum D^2 <= 2 * n * max_{1<=k<=N} |M(k)|

The "proof" (lines 277-297) is hand-wavy. It invokes "the Franel-Landau representation" but then says "Taking L^2 norms and using orthogonality..." without actually working out the details. The bound sum D^2 <= c * n * max|M(k)| is not a standard result -- the standard Franel-Landau connection is:

    sum_{i=1}^n (D_i/n)^2 = -1 + sum_{k=1}^n 1/k^2 + sum_{k=1}^N (M(k)/n)^2 + ...

This is much more subtle than "sum D^2 ~ n * max|M(k)|". The actual relationship between sum D^2 and the Mertens function involves the FULL summation of M(k)^2 over k, not just the maximum.

**The El Marraki bound enters by bounding max|M(k)|, but what's needed is control over sum M(k)^2.** These are fundamentally different: sum_{k<=N} M(k)^2 could be much larger than N * (max|M(k)|)^2 / N = max|M(k)|^2.

### 2.6. FLAW 5: Dependence on DECORRELATION_PROOF.md

The alpha-decorrelation framework references DECORRELATION_PROOF.md. Reading that file:

- Approach 1 (bilinear sums) gets the bound |corr| = O(log p / p), but the proof relies on a "quasi-independence" step (**) that requires either:
  - (a) The large sieve inequality (only sketched, "applying this with appropriate encoding")
  - (b) Barban-Davenport-Halberstam averaging (gives the bound for "most" primes, not ALL)

- The decorrelation proof itself says (line 209): "The bound is unconditional for a density-1 set of primes; for ALL primes it requires the quasi-independence step (**), which follows from BDH averaging."

**This means the decorrelation bound is NOT unconditional for all primes.** It holds for a density-1 set. There could be exceptional primes where the decorrelation fails. The El Marraki proof in ELMARRAKI_CORRECTION.md does not acknowledge this dependency.

However: ELMARRAKI_CORRECTION.md's Part II does NOT explicitly invoke the decorrelation bound from DECORRELATION_PROOF.md. It uses Cauchy-Schwarz directly (Section 3.4), bypassing the correlation bound. So the question is: does the Cauchy-Schwarz approach in Section 3.4 work independently?

**Answer: Partially.** The Cauchy-Schwarz bound |sum D_err*delta| <= ||D_err||*sqrt(C') is unconditional. The issue is whether this bound is TIGHT ENOUGH. The proof claims it is, based on the scaling analysis in Section 3.5, but the effective constants are never pinned down (Flaw 3 above).

---

## 3. Part III Audit: M(p) <= -4

### 3.1. The Argument

For |M(N)| >= 3 (i.e., M(p) <= -4 gives M(N) = M(p-1), which may or may not have |M(N)| >= 3):

    B' = (|M(N)| - 1)*C' - 2*correction

The leading term is at least 2*C'. The proof bounds |correction|/C' = O(log log N / N).

### 3.2. Check: Does M(p) <= -4 imply |M(N)| >= 3?

M(p) = M(p-1) + mu(p) = M(N) + mu(p). Since p is prime, mu(p) = -1. So M(p) = M(N) - 1.

If M(p) <= -4, then M(N) - 1 <= -4, so M(N) <= -3, hence |M(N)| >= 3. CORRECT.

### 3.3. Check: Leading term

|M(N)| >= 3 gives (|M(N)|-1)*C' >= 2*C'. For B' > 0, need 2*correction < 2*C', i.e., correction/C' < 1. The proof bounds |correction|/C' = O(log log N / N), which is certainly < 1 for N >= 3.

### 3.4. Check: The Abel summation bound (Section 4.1)

The bound on |Term2| uses:

    |inner sum at step k| <= c * C'^{1/2} * N / k

This is asserted but not derived. Where does the N/k come from? The inner sum at step k involves DeltaS_k(f)*delta(f) summed over f, where DeltaS_k counts fractions with denominators in a specific range. The number of such fractions is O(N/k^2) per the hyperbola method, not O(N/k). The C'^{1/2} factor comes from Cauchy-Schwarz against delta.

**Issue:** If the correct bound on the inner sum is O(C'^{1/2} * sqrt(N/k^2)) = O(C'^{1/2} * sqrt(N)/k), then:

    |Term2| <= c * C'^{1/2} * sqrt(N) * sum_{k=1}^N |M(k)|/k

Using El Marraki: sum_{k=33}^N |M(k)|/k <= sum 0.6257/log(k) ~ 0.6257*N/log(N) (by PNT-style partial summation... actually this diverges as N/log N).

Hmm, but the sum sum_{k=1}^N |M(k)|/k^2 converges, so if the inner bound is O(C'^{1/2}/k) instead of O(C'^{1/2}*N/k), the argument works. The details are muddled.

### 3.5. Verdict on Part III

The conclusion is almost certainly correct -- when M(p) <= -4 the leading term 2*C' dominates massively (as the table shows, B'/C' >= 1.5 for all tested cases). The analytical machinery to close this rigorously is standard (Abel summation + El Marraki), but the specific bounds in Section 4.1 have unclear intermediate steps. The argument is SOUND IN SPIRIT but SLOPPY IN EXECUTION.

The exact verification at p=31 (the smallest M(p)=-4 prime) provides a safety net.

---

## 4. Formula Consistency Check

### 4.1. The off-by-one issue

B_EXACT_AUDIT.md confirms the CORRECT formula is:

    B' = (|M(N)| - 1) * C' - 2 * correction

ELMARRAKI_CORRECTION.md uses this formula (Section 1.2, Identity D). CORRECT -- the off-by-one has been fixed.

### 4.2. Ground truth comparison

B_EXACT_AUDIT.md: correction/C' = 0.4401 at p=13.
ELMARRAKI_CORRECTION.md: correction/C' = 2984/6781 = 0.44009... at p=13. MATCHES.

B_EXACT_AUDIT.md: B'/C' = 0.1199 at p=13.
ELMARRAKI_CORRECTION.md: B' = 271/385, C' = 6781/1155. B'/C' = (271/385)/(6781/1155) = (271*1155)/(385*6781) = 312,905/2,610,685 = 0.1199. MATCHES.

**VERDICT: Formulas are consistent with the ground truth audit.**

---

## 5. Critical Assessment of the "Unconditional" Claim

The header says: "Status: PROVED (unconditional, fully analytical with finite verification for small cases)"

**This is OVERSTATED.** The actual status is:

| Component | Status |
|-----------|--------|
| Part I (p=13, 19) | Proved by exact computation |
| Part II: Cauchy-Schwarz bound | Unconditional (true inequality) |
| Part II: ||D_err|| scaling | Uses El Marraki, but constants not explicit |
| Part II: alpha lower bound | References ALPHA_POSITIVE_PROOF.md (appears sound) |
| Part II: r(43) < 1 | COMPUTED, not proved analytically |
| Part II: r(p) monotone decreasing | COMPUTED for p <= 20000, not proved |
| Part II: r(p) < 1 for ALL p >= 43 with M(p)=-3 | NOT PROVED -- gap between computation (p <= 20000) and asymptotics (p >> 1) |
| Part III (M(p) <= -4) | Sound in spirit, sloppy in execution |

### 5.1. The Gap in Part II

The proof establishes:
1. r(p) = O(sqrt(log N)/sqrt(N)) as p -> infinity (analytical, using El Marraki)
2. r(p) < 1 for all tested p <= 20000 (computational)

But it does NOT establish:
3. r(p) < 1 for ALL p >= 43 with M(p) = -3

To close this gap, one needs EITHER:
- Explicit effective constants in the O() bound (Flaw 3), showing r(p) < 1 for all N >= 42
- A proof that r(p) is monotonically decreasing for p >= 43 (Flaw 2)
- Computation extended to the explicit threshold N_0 where the asymptotic bound takes over

The proof waves at this issue (Section 3.8) but never closes it.

---

## 6. Summary of Flaws

### CRITICAL (proof-breaking):
1. **Part II effective constants never computed.** The analytical bound r(p) = O(sqrt(log N)/sqrt(N)) has unspecified constants. Without these, the proof cannot bridge the gap between p=20000 (computed) and p -> infinity (asymptotic).

2. **Part II monotonicity not proved.** The claim that r(p) decreases monotonically is supported only by computation at finitely many points. A non-monotone spike between tested points could invalidate the proof.

### MAJOR (weakens the proof significantly):
3. **Table in Section 3.6 has unclear entries.** The column "|sum D_err*delta|" may be the Cauchy-Schwarz upper bound rather than the actual inner product. The ratio 0.934 at p=13 vs my calculation of 0.798 suggests inconsistency.

4. **Section 3.8 lemma (sum D^2 <= 2n*max|M(k)|) is not a standard result** and is insufficiently proved. The Franel-Landau connection involves sum M(k)^2, not max|M(k)|.

5. **Abel summation bounds in Part III (Section 4.1) have unclear intermediate steps.** The bound on the inner sum at step k is asserted without derivation.

### MINOR:
6. The El Marraki constant is stated as both 0.6257 (Section 3.2) and 0.644 (the user's question mentions 0.644). El Marraki 1995 gives |M(x)| <= 0.6257*x/log(x) for x >= 33. The 0.644 figure appears elsewhere in the literature (possibly Dress-El Marraki 1993 with a different range). The proof uses 0.6257 consistently, which is fine.

7. Section 6.3 references "El Marraki Does NOT Do" -- this is honest and appropriate disclosure.

---

## 7. What Would Fix the Proof

To make Part II genuinely rigorous:

1. **Compute explicit constants.** From El Marraki: |M(k)| <= 0.6257*k/log(k) for k >= 33. Use this to get EXPLICIT upper bound on ||D_err||^2 and EXPLICIT lower bound on alpha, with all constants tracked. Then verify analytically that the resulting ratio is < 1 for N >= 42.

2. **Or: extend computation to the explicit threshold.** Determine N_0 such that the asymptotic bound (with explicit but possibly loose constants) gives r(p) < 1 for N >= N_0. Then compute r(p) for all M(p)=-3 primes up to N_0. This is a "finite verification + asymptotic tail" proof, which is legitimate if done carefully.

3. **Or: prove monotonicity analytically.** Show that r(p) is decreasing for p >= 43. This would require showing d/dp r(p) < 0, which is hard given the irregular distribution of M(p)=-3 primes.

---

## 8. Final Verdict

**The proof is a PLAUSIBLE ARGUMENT with SIGNIFICANT GAPS, not a complete proof.**

- Parts I and III are solid (exact computation and large leading-term dominance respectively).
- Part II is the heart of the proof and has unfilled gaps in the effective constants.
- The "unconditional" label is premature.
- The correct assessment: "B >= 0 for M(p) <= -3 is proved for p <= 20000 by computation and strongly supported asymptotically by the El Marraki-based scaling analysis. A complete proof requires either explicit effective constants or extending the computation to the provable asymptotic threshold."

**Recommended status: "Partially proved with computational verification to p=20000 and asymptotic support. Full analytical closure pending explicit constant calculation."**
