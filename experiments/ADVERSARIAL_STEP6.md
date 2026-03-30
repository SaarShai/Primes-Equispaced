# Adversarial Audit: Step 6 — Signed Fluctuation S(p) = O(p log p) Claim

## Date: 2026-03-29
## Status: FATAL GAP — claimed bound NOT proved
## Verification level: Step 3 (adversarial audit)

---

## Executive Summary

**The proof claims S(p) = O(p log p) in the theorem statement but only establishes S(p) = O(p^2 / log p) in the actual argument.** The gap is a factor of p / log^2(p), which diverges to infinity. The stated theorem is NOT proved. The weaker bound O(p^2 / log p) IS validly proved and still suffices to show S(p)/p^2 = o(1), but the rate of decay is O(1/log p), not O(log p / p) as claimed.

---

## Detailed Findings

### 1. Lemma 1 (Dedekind sum identity): CORRECT

T_h^full(k) = k^2 * [s(h,k) + (k-1)/4]

**Verification:** The algebra on lines 73-85 is correct. The expansion of the sawtooth function is standard. I verified numerically for (h,k) = (3,7), (5,11), (7,13), (2,17), (11,23) — all match exactly (Fraction arithmetic, zero error).

**One minor note:** The proof writes "sigma_h permutes {1,...,k-1}" on line 82. This is only true when gcd(h,k) = 1, which is assumed. The statement could be more explicit, but the math is correct.

### 2. Lemma 2 (Mobius inversion): CORRECT

T_b(p) = sum_{d|b} mu(d) * d^2 * T_p^full(b/d)

**Verification:** The key step on line 104-106 is:
- For a = d*a', we have (p * d * a') mod (d * m) = d * ((p*a') mod m) where m = b/d.
- This identity holds because d factors out of both the numerand and the modulus.
- Verified numerically for (p,b) = (5,6), (7,12), (11,15), (13,10) — all match.

**Corollary (line 126):** [T_b(p) - E[T_b]] / b^2 = sum_{d|b} mu(d) * s(p, b/d)

This follows correctly from Lemma 1 and Lemma 2. Verified numerically for all test cases.

### 3. The KEY step: S(p) = O(p log p) — **NOT PROVED**

This is the **central failure** of the proof. Here is the chain of logic:

**Step 1 (lines 134-148):** Correctly decomposes S(p) via Mobius inversion into:
S(p) = sum_d mu(d) * S_0(floor((p-1)/d))

**Step 2 (lines 149-226):** Uses Dedekind reciprocity to split S_0(M) = D(M) - R(M).
- D(M) = (p/12)*log(M) + O(M) — correct
- R(M) = sum s(h,p) — bounded pointwise by M*(p-1)/12 — correct

**Step 3 (lines 246-304):** Attempts to bound S(p) via the Mobius sum. **FAILS.**

The proof itself admits on line 304: "This gives |S(p)| = O(p^2 * log(p)), which is WORSE than what we claimed." It then says "We need the SIGNED cancellation in the Mobius sum" but does NOT provide it. Instead, it pivots to Step 4.

**Step 4 (lines 309-371):** Abandons the Mobius approach. Decomposes S = S_prime + S_comp.

- S_comp: Bounded by O(log^2 p) using tau(b) * Rademacher. This is CORRECT and verified numerically (|S_comp|/log^2(p) stays bounded around 0.1-1.2).

- S_prime: Bounded by pi(p-1) * (p-1)/12 = O(p^2/log p) using ONLY the trivial Rademacher pointwise bound |s(p,q)| <= (q-1)/12. This bound is VALID but gives O(p^2/log p), NOT O(p log p).

**Step 5 (lines 375-390):** Claims S(p) = O(p^2/log p). Note this is the correct conclusion from Step 4, but it **contradicts the theorem statement** S(p) = O(p log p) on line 21.

**The gap:** O(p^2/log p) vs O(p log p) differs by a factor of p/log^2(p). For p = 10^6, this is a factor of ~55,000.

### 4. Rademacher bound usage: SUFFICIENT for what's proved, NOT for what's claimed

The Rademacher bound |s(h,k)| <= (k-1)/12 is used correctly throughout. It IS sufficient to establish O(p^2/log p). It is NOT sufficient to establish O(p log p) — that would require CANCELLATION of s(p,q) across different primes q, which is never proved.

The proof gestures at this cancellation in the "Sharper Bound" section (lines 397-440) via equidistribution/large sieve arguments, but explicitly labels these as "heuristic" (line 411: "By a law-of-large-numbers heuristic") and says they "can be made rigorous" (line 418) without actually doing so.

### 5. The large sieve / equidistribution claim: STATED but NOT PROVED

Lines 216-226 invoke a "large sieve inequality" or "Polya-Vinogradov-style bound":

max_{M<=p} |sum_{h=1}^M s(h,p)|^2 <= p * sum_{h=1}^{p-1} s(h,p)^2

This inequality IS numerically valid (verified for p = 11, 13, 17, 23, 29; ratio stays below 0.11). However:

1. The proof never actually uses this bound in the final argument (Step 3 is abandoned).
2. The cited reference "Montgomery-Vaughan, Ch. 12" is vague — no theorem number given.
3. The standard large sieve applies to exponential sums, not directly to Dedekind sums. Applying it to Dedekind sums via the cotangent representation (lines 229-241) requires additional justification that is not provided.

### 6. Second moment formula: WRONG

The proof cites (line 208-209):

sum_{h=1}^{k-1} s(h,k)^2 = (k-1)(k-2)(2k^2+1)/(720k) ~ k^3/360

**This formula is INCORRECT.** Numerical verification for prime k:

| k  | Actual sum s(h,k)^2 | Claimed formula | Ratio |
|----|---------------------|-----------------|-------|
| 7  | 0.2755              | 0.5893          | 0.468 |
| 11 | 1.2107              | 2.7614          | 0.438 |
| 13 | 1.8343              | 4.7808          | 0.384 |
| 17 | 4.0138              | 11.353          | 0.354 |
| 23 | 9.1371              | 29.545          | 0.309 |
| 29 | 15.864              | 60.936          | 0.260 |

The ratio is NOT constant and DECREASES with k, so this is not a simple constant-factor error. The actual second moment grows as ~k^2/2, not ~k^3/360. The correct asymptotic appears to be closer to k^2 * C for some constant C, not k^3/360.

**Impact:** This error goes in the SAFE direction — the proof overstates the second moment, which means the large sieve bound on partial sums is pessimistic. Since the large sieve bound is not used in the final argument anyway (Step 3 is abandoned), this error does not affect the proved O(p^2/log p) bound. But it does mean the "Sharper Bound" section is built on a false premise.

### 7. Numerical verification of S(p)/p^2

| p   | S(p)     | S(p)/p    | S(p)/p^2    | S(p)/(p log p) |
|-----|----------|-----------|-------------|-----------------|
| 11  | 0.660    | 0.0600    | 0.00545     | 0.0250          |
| 29  | 3.475    | 0.1198    | 0.00413     | 0.0356          |
| 53  | 7.478    | 0.1411    | 0.00266     | 0.0355          |
| 97  | 7.357    | 0.0758    | 0.00078     | 0.0166          |
| 199 | 46.663   | 0.2345    | 0.00118     | 0.0443          |
| 397 | -17.259  | -0.0435   | -0.00011    | -0.0073         |

S(p)/p^2 does converge to 0. The ratio |S(p)|/(p log p) stays bounded (< 0.05), suggesting O(p log p) may be true empirically. But the proof does not establish it.

The proof's own table (lines 452-461) is numerically correct (verified to within rounding for p = 23, 53, 97, 199, 307, 401).

### Additional finding: Prime vs Composite decomposition

The decomposition S = S_prime + S_comp is correct, but reveals that COMPOSITE denominators dominate:

| p   | S_prime  | S_comp   | |S_comp|/|S_prime| |
|-----|----------|----------|-------------------|
| 53  | 1.16     | 6.31     | 5.4x              |
| 97  | 1.84     | 5.51     | 3.0x              |
| 199 | 13.19    | 33.48    | 2.5x              |

The proof bounds S_comp = O(log^2 p), but numerically S_comp is growing faster than log^2(p) and is actually LARGER than S_prime. This suggests the O(log^2 p) bound on S_comp may be too optimistic, or the growth rate has not yet settled for these small primes.

Wait — rechecking: |S_comp|/log^2(p) ratios are 0.40 (p=53), 0.26 (p=97), 1.19 (p=199), 0.31 (p=397). These DO stay bounded, so O(log^2 p) may be correct. The dominance of S_comp over S_prime at small p is not inconsistent with S_comp = O(log^2 p) and S_prime = O(p^2/log p) because for small p these are comparable.

---

## Verdict

### What IS proved:
1. Lemma 1 (Dedekind sum identity) -- CORRECT
2. Lemma 2 (Mobius inversion) -- CORRECT
3. The identity [T_b(p) - E[T_b]]/b^2 = sum_{d|b} mu(d) s(p, b/d) -- CORRECT
4. S_comp(p) = O(log^2 p) -- CORRECT (but second moment formula is wrong, irrelevant)
5. S_prime(p) = O(p^2/log p) -- CORRECT (trivial Rademacher bound)
6. **S(p) = O(p^2/log p)** -- CORRECT
7. **S(p)/p^2 = O(1/log p) = o(1)** -- CORRECT

### What is NOT proved:
1. **S(p) = O(p log p)** -- the theorem statement, UNPROVED
2. **S(p)/p^2 = O(log p / p)** -- the corollary on line 25, UNPROVED
3. The "sharper" bound S(p) = O(p^{3/2}/sqrt(log p)) -- labeled heuristic, UNPROVED
4. The second moment formula is wrong (safe direction, does not affect proved results)

### Impact on the wobble proof:
The connection to the wobble proof (lines 468-484) only requires S(p)/p^2 = o(1), which IS proved. The rate o(1) = O(1/log p) is slower than the claimed O(log p / p), but the qualitative conclusion "C = E[C] * (1 + o(1))" still holds.

**HOWEVER:** If the wobble proof needs C >= (c/2)*p^2 for ALL sufficiently large p (not just asymptotically), then the O(1/log p) rate matters. With O(1/log p), we need p large enough that c - C'/log(p) > c/2, i.e., log(p) > 2C'/c. This gives an explicit (but possibly large) threshold. The O(log p / p) rate would have given a much smaller threshold.

### Recommendation:
1. **Fix the theorem statement** to say O(p^2/log p), which is what the proof establishes.
2. **Mark the sharper bound as a conjecture**, not a heuristic that "can be made rigorous."
3. **Fix the second moment formula** or remove it (it's not used in the valid part of the proof).
4. **Verify that O(1/log p) rate suffices** for the downstream wobble proof applications.

---

## Classification

**Autonomy:** Level A (autonomous audit)
**Finding severity:** MAJOR — theorem statement does not match proof content
