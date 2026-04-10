# Adversarial Audit: R(p; B) = O(log B / B) Proof Sketch

**Auditor role:** Hostile referee. Assume the authors are wrong until proven otherwise.

**Date:** 2026-03-29

**Verdict: The proof has AT LEAST THREE FATAL GAPS and several serious weaknesses. It cannot be accepted in its current form.**

---

## FATAL FLAW 1: The Rademacher bound |s(p,k)| = O(log k) is WRONG as stated

**This is the most serious error in the entire proof.**

The proof claims in Step 2(a) / Step 3: "Dedekind sum bound (Rademacher): For gcd(h,k)=1, |s(h,k)| = O(log k)."

This is **false as a pointwise bound** in the sense needed here.

### What Rademacher actually proved:

Rademacher's bound (1932) states that if h/k has continued fraction expansion [a_0; a_1, ..., a_n], then:

    12 |s(h,k)| <= ln 2 + (n+1)(ln(a_1 + 1) + ... ) ...

More precisely, the classical bound is:

    |s(h,k)| <= (1/8) d(k) log k

where d(k) is the number of divisors of k (Rademacher-Grosswald). Alternatively, the elementary bound from the three-term relation gives:

    |s(h,k)| <= (1/12)(h/k + k/h + 1/(hk))

**For FIXED h = p and VARYING k:** When k < p, this gives |s(p,k)| <= (1/12)(p/k + k/p + 1/pk) = O(p/k), which is UNBOUNDED as k -> 0. When k > p, this gives |s(p,k)| = O(k/p), which GROWS LINEARLY in k.

The bound |s(p,k)| = O(log k) holds:
1. On AVERAGE over h (Vardi 1993, Bettin-Drappeau): the second moment is Sigma_h |s(h,k)|^2 ~ k (log k)^2
2. For "most" values of h mod k, but NOT uniformly over all h

**For our setting (h = p fixed, k varying):** Via Dedekind reciprocity:

    s(p,k) = [(p/k + k/p + 1/(pk))/12 - 1/4] - s(k,p)

Since s(k,p) = s(k mod p, p) is bounded by O(p) for fixed p, we get:

    s(p,k) = k/(12p) + O(p/k) + O(p)

**This means s(p,k) ~ k/(12p) for large k.** It grows LINEARLY, not logarithmically!

### Impact on the proof:

With the correct bound |s(p,k)| = O(k/p) for k >> p, the numerator bound in Step 3 becomes:

    Sigma_k |s(p,k)| * |M_p(B/k; k)| >= Sigma_{k>p} (k/(12p)) * |M_p(B/k; k)|

Even with |M_p(B/k; k)| = O(B/(k log(B/k))), the sum becomes:

    ~ Sigma_{k=1}^{B} (k/p) * B/(k log(B/k)) = (B/p) Sigma_k 1/log(B/k)

This sum diverges like B/log B, giving a total of O(B^2 / (p log B)), NOT O(B log B).

**The numerator is O(B^2 / (p log B)), and the denominator is O(B^2). The ratio is O(1/(p log B)), which STILL goes to zero** -- but the proof as stated, using |s(p,k)| = O(log k), contains a fatal error in the intermediate step. The conclusion MAY still hold, but the argument as written is incorrect.

### The authors' own data contradicts them:

The proof document reports max |s(p,b)|/log(b) ratios of 0.44 to 3.10 for b <= 300. But this is misleading because b <= 300 is SMALL. For b = 300 and p = 13, s(13, 300) should be approximately 300/156 ~ 1.92, while log(300) ~ 5.7. So the ratio is ~ 0.34. But for b = 10000, s(13, 10000) ~ 10000/156 ~ 64, while log(10000) ~ 9.2, giving ratio ~ 7.0. **The ratio grows without bound.**

**Severity: FATAL.** The claimed bound is wrong. The proof must be restructured to use the correct asymptotic s(p,k) ~ k/(12p).

---

## FATAL FLAW 2: The Mertens function bound M_p(x;k) = O(x/log x) is unjustified

Step 3(b) claims that the "restricted Mertens function" M_p(x; k) = Sigma_{d <= x, gcd(p, dk) = 1} mu(d) satisfies |M_p(x;k)| = O(x / log x).

### Problems:

1. **The coprimality condition gcd(p, dk) = 1 is not standard.** This means d must be coprime to p AND k must be coprime to p. The second condition is a CONSTRAINT ON k, not on d. So M_p(x; k) is either the full Mertens function restricted to d coprime to p (when gcd(k,p) = 1), or it is identically zero (when gcd(k,p) > 1, but since p is prime and we're summing over b coprime to p, this case doesn't arise).

2. **For d coprime to p:** M_p(x; k) = Sigma_{d <= x, gcd(d, p) = 1, gcd(d, k) = 1} mu(d). This requires d coprime to BOTH p and k. The restriction to d coprime to p only removes d = p, 2p, 3p, ... and changes the bound by a factor of (1 - 1/p), which is fine. But the restriction gcd(d, k) = 1 is more problematic.

3. **Dependence on k:** When we need |M_p(x; k)| = O(x/log x), the implicit constant depends on k. For k with many small prime factors, the restriction gcd(d,k) = 1 removes a significant fraction of integers, and the Mertens-type cancellation may be weaker. The standard result for Sigma_{d <= x, gcd(d,q) = 1} mu(d) is:

       Sigma_{d <= x, gcd(d,q) = 1} mu(d) = (mu * 1_{gcd(.,q)=1})(x)

   This has generating Dirichlet series (Product_{p | q} (1 - p^{-s})^{-1}) / zeta(s), and the Mertens-type bound is:

       |Sigma| <= C(q) * x / log x

   where C(q) depends on q. For our purposes, C(k) could grow with k, and we're summing over k.

4. **The authors never state what M_p(x;k) means precisely.** Looking at the proof document, the definition is M_p(x; k) = Sigma_{d <= x, gcd(p, dk) = 1} mu(d). The condition gcd(p, dk) = 1 means gcd(p,d) = 1 AND gcd(p,k) = 1. Since p is prime, this just means p does not divide d and p does not divide k. So M_p(x;k) = M^{(p)}(x) * 1_{p nmid k}, where M^{(p)}(x) = Sigma_{d <= x, p nmid d} mu(d). **Wait -- that's not right either**, because the constraint on k is separate from the sum over d. Let me re-read...

   Actually, looking again: the sum over b coprime to p gives us Sigma_{b=2}^{B} (with gcd(b,p)=1), and substituting b = dk, we need gcd(dk, p) = 1, which is gcd(d,p)=1 AND gcd(k,p)=1. So for each k with gcd(k,p)=1, we sum mu(d) over d <= B/k with gcd(d,p) = 1. This is just the ordinary Mertens function minus the terms where p | d.

   **Clarification:** M_p(x; k) = Sigma_{d<=x, p nmid d} mu(d) when gcd(k,p)=1, and is 0 otherwise. The restriction to p nmid d only removes terms at d = p, 2p, ... This is:

       M_p(x) = M(x) - mu(p) * M(x/p) * [correction for gcd]

   Actually more precisely: Sigma_{d<=x, gcd(d,p)=1} mu(d) = Sigma_{d<=x} mu(d) - Sigma_{d<=x, p|d} mu(d) = M(x) - Sigma_{e<=x/p} mu(pe). Since mu(pe) = -mu(e) when gcd(e,p)=1 and 0 when p|e, this gets complicated but the bound |M_p(x)| = O(x/log x) is reasonable by standard sieve methods.

   **However**, I now realize the definition in the proof document also seems to require gcd(d, k) = 1 (from the condition that b = dk is coprime to... wait, no. The outer sum is over b coprime to p, and b = dk. We need gcd(b,p) = 1, which is gcd(dk,p) = 1. There is NO requirement that gcd(d,k) = 1! The d in the Mobius inversion is a divisor of b, and k = b/d. So d and k are NOT necessarily coprime.

5. **But wait -- there IS a deeper issue.** The Mobius inversion C(p,b) = Sigma_{d|b} mu(d) s(p, b/d) sums over divisors d of b. When we exchange summation order from Sigma_b Sigma_{d|b} to Sigma_k Sigma_d, we need b = dk with d | b. That means d and k can share factors. The M_p function should be:

       M_p(B/k; k) = Sigma_{d <= B/k, k | dk (automatic), gcd(dk,p) = 1} mu(d)

   The condition gcd(dk,p)=1 means p does not divide dk, i.e., p nmid d and p nmid k. So the constraint on d is simply p nmid d, for those k with p nmid k.

   **There is NO constraint gcd(d,k) = 1.** The M_p function is genuinely just the Mertens function with the multiples of p removed. This is OK -- the bound O(x/log x) transfers.

### Revised assessment:

After careful analysis, the M_p bound is probably correct but **inadequately justified**. The proof document waves its hands at "PNT-based bound" without specifying which version and whether the error term depends on p. For a rigorous proof, one needs to cite the explicit result for Sigma_{d<=x, gcd(d,q)=1} mu(d) and verify the constant.

**Severity: SERIOUS GAP (not necessarily fatal, but requires substantial additional argument).**

---

## FATAL FLAW 3: The summation exchange in Step 2 is sloppy and hides the real structure

The proof claims:

    Sigma_{b=2}^{B} C(p,b) = Sigma_{b=2}^{B} Sigma_{d|b} mu(d) s(p, b/d)
                             = Sigma_{k=1}^{B} s(p,k) * M_p(B/k; k)

Wait -- let me check this carefully. If b ranges over [2, B] with gcd(b,p)=1, and we set k = b/d for d | b, then k ranges over divisors of b divided into b. For a fixed k, d ranges over multiples... no.

Let's be precise. Set k = b/d. Then for b from 2 to B with d | b, we have d from 1 to B/k for each k from 1 to B. But:

- The original sum is over b coprime to p, b from 2 to B
- b = dk, and d | b means d and k are not independent: they satisfy dk = b
- For fixed k, d ranges over {d : dk <= B, gcd(dk, p) = 1}
- But we also need b >= 2, so dk >= 2

This exchange is standard (it's just rearranging a double sum), so the mechanics are fine. **However:**

The critical issue is that the sum Sigma_b runs over b coprime to p, and b = dk. We need gcd(dk, p) = 1. Since p is prime, this is p nmid d AND p nmid k. So the sum becomes:

    Sigma_{k=1, p nmid k}^{B} s(p,k) * (Sigma_{d: 1<=d<=B/k, p nmid d} mu(d))

But wait: k also starts at 1 (when d = b), and s(p, 1) = 0 (empty sum). And k = 1 gives d = b, so the d sum runs over b from 2 to B with p nmid b. OK, this is consistent.

**The real problem:** The exchange is valid, but the subsequent BOUND is wrong because of Fatal Flaw 1. After substitution:

    |Sigma_b C(p,b)| <= Sigma_k |s(p,k)| * |Sigma_d mu(d)|

With s(p,k) ~ k/(12p) for large k, the bound becomes:

    ~ Sigma_{k=1}^{B} (k/p) * (B/k) / log(B/k) [using M(x) = O(x/log x)]
    = (B/p) * Sigma_{k=1}^{B} 1/log(B/k)

For k = 1 to B-1, set m = B - k, then 1/log(m+1) ~ 1/log B for most terms. The sum is approximately B/log B. So the total is B^2 / (p log B).

But this uses the UPPER BOUND on |M|. In reality, there is massive cancellation in the Sigma_k s(p,k) M_p(B/k) sum because s(p,k) changes sign. **The proof never exploits this cancellation**, which means the bound O(B^2/(p log B)) for the numerator is likely a vast overestimate.

**Severity: FATAL in combination with Flaw 1.** The O(B log B) bound is wrong. The correct bound appears to be O(B^2 / (p log B)), which still gives R -> 0 but with a DIFFERENT rate and a p-dependent constant.

---

## SERIOUS FLAW 4: The denominator bound Sigma V(b) ~ 0.024 B^2 lacks proof

The proof claims Sigma_{b=2}^{B} V(b) ~ 0.024 * B^2 based on numerical evidence. The analytical argument is incomplete.

### Issues:

1. **V(b) is defined as Sigma_{gcd(a,b)=1} ((a/b))^2.** The proof document gives:

       V(b) = Sigma_{d|b} mu(d) * (b/d - 1)(b/d - 2) / (12 * b/d)

   This is from Mobius inversion applied to Sigma_{a=1}^{k-1} ((a/k))^2 = (k-1)(k-2)/(12k). **But this Mobius inversion is WRONG.**

   The identity Sigma_{a=1}^{k-1} ((a/k))^2 = (k-1)(k-2)/(12k) sums over ALL a from 1 to k-1. The coprime-restricted version is:

       V(b) = Sigma_{gcd(a,b)=1, 1<=a<b} ((a/b))^2

   Using Mobius inversion to extract the coprime condition:

       V(b) = Sigma_{d|b} mu(d) * Sigma_{a'=1}^{b/d - 1} ((a'/( b/d)))^2
            = Sigma_{d|b} mu(d) * (b/d - 1)(b/d - 2) / (12 * b/d)

   Wait -- this IS correct, because if gcd(a,b) = d, then a = d*a' with gcd(a', b/d) = 1, and ((a/b)) = ((da'/(db'))) = ((a'/b')). So the sum over a with gcd(a,b) = d gives the sum of ((a'/b'))^2 over a' coprime to b' = b/d... **NO!** That's the sum over a' from 1 to b'-1 with gcd(a', b') = 1, which is V(b/d), not the unrestricted sum.

   So we have: Sigma_{a=1}^{b-1} ((a/b))^2 = Sigma_{d|b} V(b/d), and by Mobius inversion:

       V(b) = Sigma_{d|b} mu(d) * F(b/d)

   where F(k) = Sigma_{a=1}^{k-1} ((a/k))^2 = (k-1)(k-2)/(12k). This is actually correct as stated. Good.

2. **But the asymptotic Sigma V(b) ~ const * B^2 needs proof.** Using V(b) ~ phi(b)(phi(b) - 1)/(12 * phi(b)) ... no. For large b:

       V(b) = Sigma_{d|b} mu(d) (b/d - 1)(b/d - 2)/(12 b/d)
            ~ Sigma_{d|b} mu(d) * b/(12d)    [keeping leading term]
            = (b/12) * Sigma_{d|b} mu(d)/d
            = (b/12) * phi(b)/b
            = phi(b)/12

   So V(b) ~ phi(b)/12 for large b. Then:

       Sigma_{b=2}^{B} V(b) ~ (1/12) Sigma_{b=2}^{B} phi(b) ~ (1/12) * (3/pi^2) * B^2

   since Sigma_{b=1}^{B} phi(b) ~ 3B^2/pi^2. This gives:

       Sigma V(b) ~ B^2 / (4 pi^2) ~ 0.02533 * B^2

   which matches the claimed 0.024 reasonably well.

   **But the outer sum is over b coprime to p**, not all b! The restriction gcd(b,p) = 1 removes about 1/p of the terms:

       Sigma_{b<=B, gcd(b,p)=1} phi(b) ~ (3/pi^2) * B^2 * (1 - 1/p^2) / (1) ...

   Actually, Sigma_{b<=B, gcd(b,p)=1} phi(b) is harder to evaluate. The density factor for the coprimality restriction on b and the interaction with phi(b) requires careful handling. The constant 0.024 may be approximately correct but the proof document does not derive it rigorously.

**Severity: MODERATE.** The quadratic growth is real (it follows from standard estimates), but the precise constant is not proven. For the O(log B / B) conclusion, only the order of growth matters, so this is not fatal. But for explicit bounds (needed for the R > -1/2 claim at finite B), the constant matters.

---

## SERIOUS FLAW 5: Uniformity in p is completely unaddressed

The proof claims R(p; B) = O(log B / B) for each fixed prime p. But:

1. **The implicit constant depends on p.** Using the corrected analysis (Fatal Flaw 1), the numerator is O(B^2 / (p log B)) and the denominator is O(B^2 * (1 - 1/p)), so:

       |R(p; B)| <= C(p) / log B

   where C(p) involves the constant from the Mertens bound and the Dedekind sum growth rate. The dependence on p is through the 1/(12p) coefficient in s(p,k) ~ k/(12p).

2. **For the claim R > -1/2 "for all sufficiently large B":** The threshold B_0(p) depends on p. Could B_0(p) grow with p? If B_0(p) = O(p), then for any fixed B, there exist primes p > B for which the result says nothing.

3. **The proof document acknowledges this as an open question** (Section 7, Question 2) but still states the theorem without a uniformity caveat. This is an overstatement.

**Severity: SERIOUS.** The theorem as stated is non-uniform in p and should say so explicitly.

---

## SERIOUS FLAW 6: Computational verification is woefully inadequate

The proof is verified numerically only for:
- p in {13, 31, 97} (three primes)
- B up to 100 (or 300 for Dedekind sum statistics)

### Problems:

1. **Three primes is not "all primes."** The proof claims to work for all primes, but has been tested on essentially zero percent of primes. At minimum, one should test p = 2, 3, 5, 7 (small primes where edge cases occur), p ~ 1000 (moderate), and p ~ 10^6 (large).

2. **B = 100 is tiny.** The asymptotic claim R = O(log B / B) should be tested to B = 10^4 or 10^5 at least. At B = 100, log B / B ~ 0.046, and the observed |R| values are 0.05 or less -- this is CONSISTENT but not COMPELLING. The data could equally well fit |R| = O(1/sqrt(B)) or other rates.

3. **The Mobius inversion was verified to b = 40.** This is an identity that should hold for all b. Verifying to b = 40 is reasonable for an identity check, but the BOUNDS need testing at much larger scales.

4. **No verification of the key bound |Sigma C| = O(B log B).** The proof document reports that |Sigma C(p,b)| is "O(B) or slower" but does not verify the claimed O(B log B). What is the actual growth rate? Is it O(B), O(B log B), O(B^{3/2}), or something else? Without this, the proof's central claim is unverified.

**Severity: SERIOUS.** The empirical foundation is too thin to support the claimed generality.

---

## MODERATE FLAW 7: The Mobius inversion requires gcd(p,b) = 1, which is not always discussed

The identity s(p,b) = Sigma_{d|b} C(p, b/d) assumes that the Dedekind sum s(p,b) decomposes into coprime-restricted pieces. This works when gcd(p,b) = 1, because:

- For gcd(a,b) = d, we write a = da', b = db', and ((pa/b)) = ((pa'/b'))
- This requires that the map a -> pa mod b descends correctly to the quotient

When gcd(p,b) > 1 (i.e., p | b), the Dedekind sum s(p,b) is defined but the decomposition may differ because ((pa/b)) = ((pa'/b')) requires gcd(p, b') = 1 at each level. Since the outer sum already restricts to b coprime to p, this is handled -- but the proof should state this constraint explicitly at every step.

**Severity: MINOR.** The restriction gcd(b,p) = 1 is present in the definition of R(p;B) and carries through. But the proof is sloppy about tracking it.

---

## MODERATE FLAW 8: Section 4 (Reciprocity analysis) contradicts Section 3

In Section 4 of the proof document, the authors use Dedekind reciprocity to write:

    s(p,b) = [(p/b + b/p + 1/(pb))/12 - 1/4] - s(b,p)

They then note that s(b,p) depends only on b mod p and that the sum over a full period vanishes. This gives:

    Sigma_b s(p,b) ~ Sigma_b b/(12p) + O(B) = B^2/(24p) + O(B)

This shows **Sigma s(p,b) grows like B^2**, not like B log B! Since C(p,b) = Sigma_{d|b} mu(d) s(p, b/d), and the Sigma C is a Mobius-weighted version of Sigma s, there is massive cancellation. But the proof in Section 3 BOUNDS |Sigma C| by bounding each term individually (triangle inequality), which destroys this cancellation.

**This confirms Fatal Flaw 1:** The individual term bound |s(p,k)| = O(log k) is wrong, and the proof needs to exploit the cancellation structure rather than using the triangle inequality.

**Severity: Confirms FATAL status of Flaw 1. The authors' own reciprocity analysis in Section 4 shows that s(p,k) ~ k/(12p), not O(log k).**

---

## SUMMARY OF FLAWS

| # | Flaw | Severity | Status |
|---|------|----------|--------|
| 1 | |s(p,k)| = O(log k) is FALSE for fixed p, varying k. Correct bound is O(k/p). | **FATAL** | Proof must be restructured |
| 2 | M_p(x;k) = O(x/log x) inadequately justified | SERIOUS GAP | Likely fixable |
| 3 | Triangle inequality bound gives O(B^2/p), not O(B log B) | **FATAL** | Follows from Flaw 1 |
| 4 | Denominator constant not rigorously derived | MODERATE | Likely fixable |
| 5 | No uniformity in p | SERIOUS | Theorem must state dependence |
| 6 | Computational verification insufficient | SERIOUS | Easily fixable |
| 7 | gcd(p,b) = 1 not tracked carefully | MINOR | Easily fixable |
| 8 | Section 4 contradicts Section 3 | Confirms FATAL | See Flaw 1 |

---

## CAN THE PROOF BE SALVAGED?

**Possibly yes**, but it requires a fundamentally different argument for the numerator bound.

### The corrected argument (sketch):

Using s(p,k) = k/(12p) - 1/4 + O(p/k) - s(k,p), we have:

    Sigma_b C(p,b) = Sigma_k [k/(12p) - 1/4 + O(p/k) - s(k,p)] * M_p(B/k)

The leading term k/(12p) gives:

    (1/(12p)) Sigma_k k * M_p(B/k)

By partial summation / Dirichlet hyperbola, Sigma_{k<=B} k * M(B/k) involves the partial sums of the Mertens function weighted by k, which should be O(B^2 / log B) by PNT. So the leading contribution is O(B^2 / (p log B)).

With denominator ~ B^2 / (4 pi^2), we get:

    |R| <= O(1 / (p log B)) -> 0

This is actually a BETTER rate than claimed (O(1/(p log B)) vs O(log B / B)), but requires a completely different proof! The current proof's Step 3 is irreparably broken.

### What's needed for a correct proof:

1. Replace the Rademacher bound with Dedekind reciprocity: s(p,k) = k/(12p) + periodic term + O(p/k)
2. Show that the main term k/(12p) produces a contribution to Sigma C that is bounded by O(B^2 / (p log B)) using PNT for Sigma k * M(B/k)
3. Show that the periodic term s(k,p) produces a bounded contribution O(B) using the vanishing period sum
4. Conclude |R| = O(1/(p log B))

This would be a genuine proof, but it is NOT what the current document contains.

---

## VERDICT

**REJECT.** The proof contains a fundamental error in its main step (the Dedekind sum bound), and the correct bound, while likely still yielding R -> 0, requires a substantially different argument. The computational verification is inadequate, the uniformity in p is not addressed, and Section 4 of the authors' own document contradicts Section 3. The proof cannot be accepted in its current form but may be salvageable with significant revision.
