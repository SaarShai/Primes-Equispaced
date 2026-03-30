# Adversarial Audit: CORRECTION_NEGATIVITY_PROOF.md

## Date: 2026-03-30
## Role: Hostile Referee (Step 3 of Verification Protocol)
## Claim Under Review: "For every prime p >= 43 with M(p) = -3, the Abel correction Term2 < 0."
## Verdict: CLAIM IS NOT PROVED. Multiple fatal and serious gaps identified.

---

## Executive Summary

The document presents a three-part argument: (A) alpha grows like log(N), (B) |rho| = O(sqrt(log N)), (C) combining gives alpha + rho > 1 for p >= 43. The argument has the correct *structure* of a proof, but Part B is fundamentally broken and Part C relies on empirical constants that are not rigorously established. The finite verification to p = 20,000 uses floating-point arithmetic, not exact arithmetic. The claim should be downgraded from "PROVED" to "SUPPORTED BY STRONG COMPUTATIONAL EVIDENCE WITH A PARTIAL ANALYTICAL FRAMEWORK."

---

## FLAW 1 (FATAL): The Decorrelation Bound |rho| = O(sqrt(log N)) Is NOT Proved

### What the proof claims:
Section 3 states: "|rho| = O(sqrt(log N))" and cites DECORRELATION_PROOF.md.

### What DECORRELATION_PROOF.md actually says:

The decorrelation proof document is remarkably honest in its Section 6.3 ("Corrected Main Theorem"), where it **retracts its own earlier claims**:

> **(a) Unconditional (trivial): |corr(D_err, delta)| = O(sqrt(log p)), giving no decorrelation.**

This is a bound on the CORRELATION, not on rho itself. The relationship between correlation and rho is:

    rho = 2 * sum(D_err * delta) / C' = 2 * corr(D_err, delta) * ||D_err|| * ||delta|| / C'

Since ||D_err|| ~ sqrt(V) ~ N * sqrt(log N) and ||delta|| ~ N / sqrt(log N) and C' ~ N^2 / log(N), a correlation bound of O(sqrt(log p)) gives:

    |rho| ~ corr * ||D_err|| * ||delta|| / C' * 2

This does NOT obviously give |rho| = O(sqrt(log N)). The proof conflates two different quantities.

### The actual situation from DECORRELATION_PROOF.md:

- **Unconditional:** |corr(D_err, delta)| = O(sqrt(log p)). This is the TRIVIAL Cauchy-Schwarz bound and proves NOTHING about decorrelation.
- **Under BDH quasi-independence (conditional):** |corr| = O(sqrt(log p)/p). This WOULD give decorrelation, but it requires the quasi-independence of multiplicative permutations sigma_p mod b across different b, which is NOT proved for all primes. It holds only for a density-1 set.
- **For M(p) <= -3 specifically:** The document states this "only strengthens the bound" but provides no rigorous proof of this claim.

The decorrelation document itself says in Section 8.2:
> "Quasi-independence for ALL p with M(p) <= -3: The BDH bound gives density-1 but not ALL."

And in Section 9:
> "Verification Status: Unverified"

**Conclusion:** The decorrelation bound, which is the entire foundation of Part B, is either trivial (unconditional) or unproved for all M(p) = -3 primes (conditional on BDH quasi-independence). The correction negativity proof cites this as an established result when it is not.

### Severity: FATAL. Without Part B, the analytical argument for p > 179 collapses entirely.

---

## FLAW 2 (FATAL): The Identity B'/C' = alpha + rho Is Verified, Not Proved

### What the proof says:
Section 1: "Identity (verified exactly at 10 primes via Fraction arithmetic)."

### The problem:
The document calls this an "identity" but only provides computational verification at 10 specific primes. An identity must hold for ALL primes by algebraic manipulation. The document never provides a derivation -- it just verifies at a few points.

To be fair, this identity likely IS algebraic (it follows from decomposing the bilinear sum sum(D * delta) into its linear and nonlinear components). But the proof document does not PROVE it. It should either:
1. Provide the algebraic derivation, or
2. Clearly label this as a conjecture verified at 10 points.

### Severity: FATAL as written, likely FIXABLE. The algebraic derivation should be straightforward but is simply missing from the document.

---

## FLAW 3 (SERIOUS): The Constants c_1 = 1.03, c_2 = 1.15, c_3 = 1.40 Are Empirical Fit Parameters

### What the proof claims:
Section 2.5 states: "alpha(p) >= 1.03 log(p-1) - 1.15 (empirical lower bound, R^2 > 0.99)"

Section 4.1 then uses this in a quadratic inequality to establish the threshold P_0 = 179.

### The problems:

1. **c_1 = 1.03 is a regression coefficient, not a proved lower bound.** An R^2 > 0.99 means the linear fit explains 99% of variance, but it says NOTHING about whether the fit is a lower bound. The actual alpha values could dip below the regression line at some untested prime. The proof needs alpha >= c_1 log(p) - c_2 as a LOWER BOUND, not as a best-fit line.

2. **The fit is based on only 10 data points** (the exactly computed primes up to p = 179). Extrapolating a linear regression from 10 points to all p > 179 is not a proof.

3. **c_3 = 1.40 is claimed as an "empirical upper bound" on |rho|/sqrt(log N).** Looking at the data in Section 3.2, the ratios are: 0.831, 1.159, 1.315, 1.239, 1.360, 1.328, 1.336, 1.380, 1.383, 1.382. The values are STILL INCREASING at p = 179. The claim c_3 = 1.40 is a guess that the ratio will not exceed 1.40, but there is zero analytical justification. The ratio goes from 0.83 to 1.38 over the range -- who says it stops at 1.40?

4. **Even if the constants were exact**, the argument only covers p > 179. The finite verification must cover [43, 179] exactly. This part IS done with exact Fraction arithmetic (8 primes), which is fine.

### Severity: SERIOUS. The analytical argument for p > 179 rests on unproved empirical constants. The argument is heuristic, not rigorous.

---

## FLAW 4 (SERIOUS): The Streaming Computation for 179 < p <= 20,000 Uses Floating-Point Arithmetic

### What the proof claims:
Section 4.1, Case 3: "For all 81 remaining M(p) = -3 primes in (179, 20000], the streaming computation confirms correction/C' < 0 < 1/2."

### What the code actually does:
Reading `correction_m3.c`, the computation uses `double` throughout:
```c
double B_raw = 0.0;
double C_raw = 0.0;
...
double D = (double)rank - (double)n * f;
...
B_raw += 2.0 * D * delta;
C_raw += delta * delta;
```

This is IEEE 754 double-precision floating point. For p near 20,000, the Farey sequence has n ~ 3N^2/pi^2 ~ 120 million elements. Each iteration accumulates a floating-point sum. After 120 million additions of terms of varying magnitude, the accumulated rounding error is potentially significant.

### Specific concerns:

1. **Catastrophic cancellation in B_raw:** B_raw = 2 * sum(D * delta) involves terms of alternating sign. For large p, individual terms |D * delta| can be large while B_raw is the difference of large positive and negative contributions. This is the classic scenario for catastrophic cancellation in floating-point.

2. **The rank computation:** `rank` is computed as a running integer counter (exact), but `D = rank - n * f` involves multiplying `n` (a large integer, ~120M) by `f` (a double). For n = 120,000,000 and f near 1/2, the product n*f = 60,000,000, and the difference rank - 60,000,000 could lose 8 decimal digits of precision. Since double has ~15.7 decimal digits, D has at most ~8 significant digits.

3. **No error analysis is provided.** The proof does not bound the accumulated floating-point error or argue that it is negligible relative to the margin.

4. **The margin for correctness is unclear.** For the claim Term2 < 0 (equivalently correction/C < 0), the margin is |correction/C|. For p = 43, correction/C = -0.177, but for what primes is the margin smallest? If any prime near p = 179 has correction/C close to 0, floating-point errors could invalidate the verification.

### Partial mitigation:
The exact Fraction arithmetic verification covers the 8 primes in [43, 179], and the correction/C values there range from -0.177 to -1.224. These are large margins where floating-point would not be an issue. But for 179 < p <= 20,000, we rely on `double` arithmetic.

Looking at the data (Section 4.1): at p = 179, correction/C = -1.224, and the values become more negative for larger p (reaching -8.45 at p = 12413). If the correction/C is always deeply negative in this range, floating-point error (likely in the range 10^{-6} to 10^{-3} relative error) would not flip the sign.

### Severity: SERIOUS but likely not fatal. The margins appear large enough that floating-point error would not flip signs. However, without a rigorous error analysis, this is a gap in the proof.

---

## FLAW 5 (SERIOUS): T(N) < 0 Is Verified Only Computationally

### What the proof claims:
Section 2.3: "Claim. T(N) < 0 for all N >= 12 with M(N) = -2 and M(N+1) = -3."

### What is actually proved:
The analytical argument in Section 2.3 is explicitly abandoned mid-way:
> "This direct asymptotic approach is imprecise for explicit constants. Instead, we proceed computationally for the finite range and analytically for the asymptotic."

But the "analytical for the asymptotic" part is never completed. Section 5.3 gives heuristic reasoning about why T(N) should be negative (involving the derivative of 1/zeta(s) at s=1), but this is not made rigorous.

### The real question:
Could there exist a very large prime p with M(p) = -3 where T(N) > 0? The M(p) = -3 condition constrains M(p-1) = -2, but it does NOT prevent wild oscillations in the sum T(N) = sum_{m=2}^{N} M(floor(N/m))/m. The Mertens function M(x) oscillates wildly (unconditionally, |M(x)| grows at least as fast as x^{1/2} infinitely often). For a sufficiently pathological N, the partial sums in T(N) could in principle conspire to be positive.

### What would be needed:
A rigorous bound showing that for M(N) = -2, the sum T(N) = sum_{m>=2} M(floor(N/m))/m is bounded above by some explicit negative constant. The prime number theorem gives the asymptotic, but making it effective (with explicit constants and error terms) is nontrivial.

### Severity: SERIOUS. This is a genuine gap in the analytical framework. The computation to p = 20,000 is reassuring but does not constitute a proof for all primes.

---

## FLAW 6 (MODERATE): Potential Circularity Check -- PASSED

### The concern:
Does the decorrelation bound use B >= 0 in its proof?

### Finding:
After careful reading of DECORRELATION_PROOF.md, the decorrelation bound does NOT assume B >= 0. The bound is derived from:
- The Barban-Davenport-Halberstam theorem (standard result in analytic number theory)
- Cauchy-Schwarz inequality
- The algebraic identity sum_b T_b = 0
- Properties of multiplicative permutations

None of these ingredients use B >= 0. The proof is NOT circular in this specific sense.

However, there is a subtler issue: the M(p) <= -3 condition is used in DECORRELATION_PROOF.md Section 4.7 ("Making it Unconditional for M(p) <= -3") where it states that "The M(p) <= -3 condition means mu(k) = -1 for at least 3 more primes k <= p than mu(k) = +1." This characterization of M(p) <= -3 is incorrect -- the Mertens function counts ALL mu(k) for k <= p, not just primes. The constraint M(p) = -3 involves the cumulative sum of mu over all integers, including composite numbers with even or odd numbers of prime factors.

### Severity: MODERATE. No circularity, but the auxiliary claim about what M(p) <= -3 "means" is wrong (though not load-bearing for the argument).

---

## FLAW 7 (MODERATE): The Claim "|rho|/(alpha-1) Remains Below 1 for All p > 20,000" Is NOT Proved

### What the proof claims:
Section 4.2 and Section 12 ("Honest Assessment") item 8: "The claim that the ratio |rho|/(alpha-1) remains below 1 for all p > 20000 (follows from items 6 and 7)."

### The problem:
This claim "follows from items 6 and 7" -- i.e., from alpha ~ c log(N) and |rho| = O(sqrt(log N)). But as established in FLAW 1, the |rho| bound is not proved. Even assuming it were proved with effective constant c_3, the claim requires:

    c_3 * sqrt(log p) < c_1 * log(p) - c_2 - 1

for all p > 20,000 with M(p) = -3. This is an asymptotic statement that is true for sufficiently large p (since log grows faster than sqrt(log)), but "sufficiently large" depends on the constants, which are empirical.

### Severity: MODERATE. The asymptotic argument is correct in principle, but without rigorous constants it is not a proof.

---

## FLAW 8 (MINOR): The "alpha ~ -6R(N)" Relationship Error Term

### What the proof claims:
Section 2.4: "alpha = -6R(N) + O(1/N)"

More precisely: "alpha = [-6R(N) + 1/n - 6 C_W(N)/N] / [1 + 12R(N)/n]"

### The issue:
The denominator [1 + 12R(N)/n] involves R(N)/n. Since R(N) ~ -log(N)/6 and n ~ 3N^2/pi^2, the ratio R(N)/n ~ -pi^2 log(N)/(18 N^2) which is indeed O(log(N)/N^2), as claimed. So for large N:

    alpha = -6R(N) * (1 - 12R(N)/n + ...) + O(1/N) = -6R(N) + O(log(N)^2/N^2) + O(1/N)

The dominant correction is O(1/N), not O(log(N)/N) or larger. The error term is correctly characterized.

The verification at 6 primes shows ratios within 0.8% of 1. For p = 19, the ratio is 1.0077, giving an error of 0.77%. For p = 13, the ratio is 0.9998, a 0.02% error. These are consistent with an O(1/N) correction.

### Severity: MINOR. The error term analysis is adequate. No issue here.

---

## FLAW 9 (OBSERVATION): The Proof's Honest Assessment Is More Honest Than the Proof Itself

Section 12 ("Honest Assessment") correctly identifies most of the gaps I found:
- Item 6: "the effective constant is not fully explicit"
- Item 7: "from the PNT-type estimate" (i.e., not fully effective)
- Item 8: "follows from items 6 and 7" (i.e., conditional on unproved bounds)

But Section 0 labels the status as "PROVED (three-part analytical proof + finite verification)" and Section 4.1 ends with "QED." This is misleading. A document that says "QED" in the proof body but then admits in the appendix that key steps are not rigorous is poorly structured. The QED should be removed or replaced with "QED (conditional on the decorrelation bound and effective constants)."

### Severity: OBSERVATION (editorial, not mathematical).

---

## Summary of Findings

| Flaw | Description | Severity | Fixable? |
|------|-------------|----------|----------|
| 1 | Decorrelation bound |rho| = O(sqrt(log N)) is NOT proved | FATAL | Requires new mathematics (proving quasi-independence for M(p)=-3 primes) |
| 2 | Identity B'/C' = alpha + rho verified but not derived | FATAL | FIXABLE (algebraic derivation should be routine) |
| 3 | Constants c_1, c_2, c_3 are empirical, not proved bounds | SERIOUS | Partially fixable with effective PNT bounds |
| 4 | Streaming computation uses floating-point | SERIOUS | FIXABLE (use GMP/exact arithmetic, or do error analysis) |
| 5 | T(N) < 0 only verified computationally | SERIOUS | Hard to fix analytically |
| 6 | Circularity check | PASSED | N/A |
| 7 | |rho|/(alpha-1) < 1 for p > 20000 not proved | MODERATE | Follows from fixing Flaws 1 and 3 |
| 8 | Error term in alpha ~ -6R(N) | MINOR/OK | No issue |
| 9 | "PROVED" label inconsistent with "Honest Assessment" | Editorial | Relabel as conditional/partial |

---

## Overall Verdict

**The claim "Term2 < 0 for all primes p >= 43 with M(p) = -3" is NOT proved.**

What IS established:
1. Term2 < 0 for the 8 M(p) = -3 primes in [43, 179], verified by exact rational arithmetic. (Rigorous.)
2. Term2 < 0 for the 81 M(p) = -3 primes in (179, 20000], verified by floating-point streaming computation. (Strong numerical evidence, not rigorous.)
3. An analytical framework showing WHY Term2 should be negative: alpha grows like log(N) while |rho| grows slower. (Correct in spirit, not made rigorous.)

The proof should be relabeled as:
- **Rigorous for p in [43, 179]:** 8 primes, exact arithmetic.
- **Strong numerical evidence for p in [43, 20000]:** 89 primes, floating-point.
- **Heuristic analytical argument for all p:** structure is sound but key bounds are not effective.

### Recommended status: "PARTIALLY PROVED (exact verification to p=179) + STRONG NUMERICAL EVIDENCE (to p=20000) + CONDITIONAL ANALYTICAL ARGUMENT"

---

## Recommendations for the Authors

1. **Derive the identity B'/C' = alpha + rho algebraically.** This should be straightforward from the definition of alpha as the regression coefficient. Just expand the definitions.

2. **Either prove the decorrelation bound rigorously or state the theorem as conditional.** The BDH quasi-independence for ALL M(p) = -3 primes appears to be an open problem in analytic number theory. Be honest about this.

3. **Re-run the streaming computation with exact arithmetic** (Python Fraction or GMP integers). For p up to 20,000, the Farey sequence has ~120M elements, and exact Fraction arithmetic would be slow but feasible over a few hours.

4. **Prove T(N) < 0 analytically** using effective versions of PNT or Mertens' theorem. This may require importing results from the literature on explicit bounds for sum mu(k) log(k).

5. **Extend the exact verification range.** If exact verification can be pushed to p = 50,000 or 100,000, the gap between verification and asymptotics becomes smaller, and the empirical constants become more trustworthy.

6. **Remove the "QED" and "PROVED" labels** until the gaps are closed. Replace with "CONDITIONALLY PROVED" or "PROVED MODULO EFFECTIVE DECORRELATION."
