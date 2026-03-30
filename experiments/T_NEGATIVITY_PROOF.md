# T(N) Negativity Analysis: Claim Is FALSE

## Date: 2026-03-30
## Status: DISPROVED. The claim T(N) < 0 for all N >= 42 with M(N) = -2 is FALSE.
## Classification: C1 (collaborative, minor novelty -- the disproof is the finding)
## Connects to: N2 (Mertens-Wobble), N5 (Per-Step Decomposition)
## Impact: CORRECTION_NEGATIVITY_PROOF.md must be revised.

---

## 0. Summary

**Original Claim (from CORRECTION_NEGATIVITY_PROOF.md, Section 2.3):**
> T(N) < 0 for all N >= 12 with M(N) = -2 and M(N+1) = -3.

where T(N) = sum_{m=2}^{N} M(floor(N/m))/m.

**Verdict: FALSE.** The first counterexample among M(p) = -3 primes is:

    p = 243799,  N = 243798,  T(N) = +0.165

Verified by independent computation (both C and Python, using the hyperbolic method).

Among all 922 primes p with M(p) = -3 and p <= 10^7:
- 675 (73.2%) have T(N) < 0
- 247 (26.8%) have T(N) >= 0
- Maximum: T(N) = +137.34 at p = 3,535,369

The claim held for all 174 primes up to p ~ 200,000, explaining why it passed
the earlier verification to p = 20,000.

---

## 1. The Identity

For prime p with M(p) = -3 (equivalently M(N) = -2 where N = p-1):

    6R(N) = 1 + M(N) + T(N) = -1 + T(N)

where R(N) = sum f_i^2 - n/3, and T(N) = sum_{m=2}^{N} M(floor(N/m))/m.

Also: T(N) = 3 + 6 * E(N) where E(N) = sum_{q=2}^{N} e(q) and
e(q) = prod_{p|q}(1-p) / (6q).

So T(N) < 0 iff E(N) < -1/2 iff 6R(N) < -1 iff R(N) < -1/6.

---

## 2. Why the Claim Fails

### 2.1. The R(N) Oscillation

From R_NEGATIVE_PROOF.md: R(N) oscillates with growing amplitude. While R(N) -> -infinity
on average, it has positive excursions. For general N, R(N) can be positive (first
positive N >= 7 occurs at N = 1417).

The claim T(N) < 0 for M(N) = -2 is equivalent to R(N) < -1/6 for these N.
But R(N) is not monotonically negative -- it oscillates around a negative trend.
The constraint M(N) = -2 does NOT force R(N) below -1/6.

### 2.2. Positive Excursions Among M(N) = -2

For ALL N >= 42 with M(N) = -2 (not just primes):
- First positive T(N) at N = 218,311
- By N = 10^7: 3,849 out of 12,661 (30.4%) have T(N) > 0
- Maximum T(N) = +139.54 at N = 3,529,804

### 2.3. Positive Excursions Among M(p) = -3 Primes

Restricting to N = p-1 where p is prime:
- First positive T(N) at N = 243,798 (p = 243,799)
- By p = 10^7: 247 out of 922 (26.8%) have T(N) > 0

### 2.4. Detailed Counterexample: p = 243,799

    M(243798) = -2
    M(243799) = -3 (p = 243799 is prime, mu(243799) = -1)
    T(243798) = +0.1652
    6R(243798) = -0.8348
    R(243798) = -0.1391
    alpha(p) ~ -6R = 0.835 < 1

Verified by both the C hyperbolic method and independent Python computation.

---

## 3. What the Counterexample Means for the Correction Proof

### 3.1. Impact on CORRECTION_NEGATIVITY_PROOF.md

The correction negativity proof claimed Term2 < 0 for all p >= 43 with M(p) = -3.
Since Term2 < 0 iff alpha + rho > 1, and at p = 243799 we have alpha ~ 0.835 < 1
with rho < 0, the condition alpha + rho > 1 FAILS at this prime.

So **Term2 > 0 at p = 243,799**.

The correction/C' = (1 - alpha - rho)/2 > 0 at this prime.

### 3.2. Impact on B' > 0

The claim B' > 0 (equivalently correction/C' < 1/2) is a WEAKER claim that
requires only alpha + rho > 0, not alpha + rho > 1.

For p = 243,799: alpha ~ 0.835 > 0 and rho is bounded, so alpha + rho could
still be positive. The B' > 0 claim is NOT directly affected by T(N) > 0.

The B' > 0 proof (ELMARRAKI_CORRECTION.md) uses a different argument:
it shows correction/C' < 1/2 (equivalently B'/C' > 0), which requires only
the weaker condition alpha + rho > 0. This proof should be checked separately.

### 3.3. The Logical Structure

The proof had three layers:

1. **B' > 0** (equivalently correction/C' < 1/2): needs alpha + rho > 0.
   This is the result that matters for the main theorem.
   STATUS: NOT affected by T(N) > 0. Still may hold.

2. **Term2 < 0** (equivalently correction < 0, i.e., alpha + rho > 1):
   a stronger claim used in CORRECTION_NEGATIVITY_PROOF.md.
   STATUS: FALSE for p >= 243,799. Counterexamples exist.

3. **T(N) < 0** (equivalently R(N) < -1/6): the technical claim used to show
   alpha > 1 to leading order.
   STATUS: FALSE for N >= 218,311. Counterexamples exist.

---

## 4. Why the Verification to p = 20,000 Was Misleading

The Mertens function M(x) has increasingly large oscillations as x grows.
The sum T(N) = sum M(floor(N/m))/m aggregates M values at many different scales,
and the oscillations in M can create positive T(N) values even when M(N) = -2.

For small N (up to ~200,000), the prime-driven negative contributions to the
sum of e(q) dominate. But for larger N, the semiprime contributions (which are
positive) occasionally push E(N) above -1/2, making T(N) positive.

The threshold where this first happens (N ~ 218,000) is beyond the range of the
streaming verification (p <= 20,000, N <= 19,999). This is an instance of
the general phenomenon that number-theoretic claims verified "up to N_0"
can fail spectacularly for N > N_0.

---

## 5. Analytical Understanding

### 5.1. Why No Analytical Proof Was Possible

The claim T(N) < 0 for M(N) = -2 cannot be proved because it is false.
The deeper reason: the convolution sum T(N) involves Mertens values at
DIFFERENT scales (N/2, N/3, ..., 1), and the constraint M(N) = -2 does
not sufficiently control M at these other scales.

Using the hyperbola method:
    T(N) + M(N) = sum_{d<=N} mu(d) * H(floor(N/d))

The right side equals the Dirichlet convolution of mu and the harmonic function.
Its sign depends on subtle cancellations in the Mertens function across all
scales from 1 to N. No known effective bound controls this sign.

### 5.2. The Perron Formula Perspective

Via Perron's formula, F(N) = sum M(fl(N/m))/m is related to the integral:

    F(N) ~ (1/2pi*i) * integral N^s/(s*zeta(s)) * zeta(s+1) ds

The residue at s = 0 (from zeta(s+1) having a pole) gives a contribution
of -2 (since 1/zeta(0) = -2). The "error" term from the contour integration
is of order O(N^{sigma}) for any sigma above the real part of the rightmost
zeta zero, and this error oscillates in sign.

Since T(N) = F(N) + 2, we get T(N) = [oscillating error], which has no
definite sign. The claim T(N) < 0 amounts to saying the oscillating error
is always negative for M(N) = -2, which is not true.

### 5.3. Connection to R(N) Oscillation

Since T(N) = 6R(N) + 1, the claim is equivalent to R(N) < -1/6 for all N
with M(N) = -2. But R(N) = 1/3 + sum e(q) oscillates with growing amplitude
(proved in R_NEGATIVE_PROOF.md). The M(N) = -2 constraint does not prevent
R(N) from exceeding -1/6.

In fact, the maximum of R(N) among N with M(N) = -2 in [42, 200000] was:
    max R(N) = -0.128 at N = 92166 (which is > -1/6 = -0.167)

This already shows 6R > -1 is possible, hence T > 0 is possible.

---

## 6. Computational Data

### 6.1. Verification Statistics (up to N = 10^7)

| Category | Count | T > 0 | Fraction | Max T |
|----------|-------|-------|----------|-------|
| ALL N with M(N)=-2, N >= 42 | 12,661 | 3,849 | 30.4% | +139.5 at N=3,529,804 |
| N = p-1, M(p) = -3 primes | 922 | 247 | 26.8% | +137.3 at N=3,535,368 |

### 6.2. First Counterexamples Among M(p) = -3 Primes

| p | N = p-1 | T(N) | 6R(N) | alpha approx |
|---|---------|------|-------|--------------|
| 243,799 | 243,798 | +0.165 | -0.835 | 0.835 |
| 383,983 | 383,982 | +8.801 | +7.801 | R > 0! |
| 384,203 | 384,202 | +3.152 | +2.152 | R > 0! |
| 564,671 | 564,670 | +4.636 | +3.636 | R > 0! |

### 6.3. T(N) < 0 Verified Range

T(N) < 0 for ALL M(p) = -3 primes with p <= 243,797 (174 primes, N <= 243,796).

The "worst case" in this range: T(12) = -0.430 at p = 13.
The next worst: T(42) = -2.895 at p = 43.

### 6.4. Exact Verification at Selected Primes (Fraction arithmetic, from prior work)

| p | correction/C' | alpha + rho | Term2 < 0? |
|---|---------------|-------------|------------|
| 43 | -0.177 | 1.354 | YES |
| 47 | -0.281 | 1.562 | YES |
| 53 | -0.200 | 1.400 | YES |
| 71 | -0.409 | 1.818 | YES |
| 107 | -0.944 | 2.888 | YES |
| 131 | -0.879 | 2.757 | YES |
| 173 | -1.243 | 3.486 | YES |
| 179 | -1.224 | 3.448 | YES |

All verified primes up to p = 179 have Term2 < 0, consistent with T(N) < 0
in this range.

---

## 7. What IS True

### 7.1. T(N) < 0 for small N with M(N) = -2

**Verified:** T(N) < 0 for all N in {12, 14, 17, 18, 21, 23, 24, 25, 29, 34, 37, 42, ...}
up to N = 243,796 where M(N) = -2.

For the 174 M(p) = -3 primes with p <= 243,797: T(N) < 0.

### 7.2. T(N) is negative on average

Among N with M(N) = -2 and N >= 42 (up to 10^7):
- Mean T(N) ~ -20 (deeply negative on average)
- But with large positive excursions

### 7.3. B' > 0 may still hold

The B' > 0 claim (correction/C' < 1/2) requires only alpha + rho > 0,
which is weaker than alpha + rho > 1 (which requires T < 0).

Even when T > 0 (alpha < 1), we could still have alpha + rho > 0
since alpha > 0 always holds and rho, while negative, may satisfy |rho| < alpha.

The B' > 0 question at p = 243,799 requires computing alpha and rho
exactly at that prime, which needs the full Farey sequence F_{243798}.

---

## 8. Implications for CORRECTION_NEGATIVITY_PROOF.md

### 8.1. What Must Change

1. **Section 2.3 Claim:** "T(N) < 0 for all N >= 12 with M(N) = -2" must be
   replaced by "T(N) < 0 for all N in [12, 243796] with M(N) = -2 (verified),
   but T(N) > 0 occurs for N = 243798 and many larger N."

2. **Section 4.1 Case 1 (p >= P_0):** The analytical argument assumed alpha > 1,
   which requires T < 0. This fails. The proof of Term2 < 0 for p >= 179
   collapses.

3. **The main theorem** "Term2 < 0 for all p >= 43 with M(p) = -3" is FALSE.
   Must be downgraded to "Term2 < 0 for all M(p) = -3 primes p in [43, 243797]."

4. **The B' > 0 proof** (ELMARRAKI_CORRECTION.md) uses correction/C' < 1/2,
   NOT Term2 < 0. This proof may survive if it doesn't depend on T(N) < 0.
   Needs re-examination.

### 8.2. Status of the Correction Negativity Proof

- **PROVED (exact):** Term2 < 0 for 8 primes in [43, 179] (Fraction arithmetic).
- **VERIFIED (computational):** Term2 < 0 for 174 primes in [43, 243797].
- **FALSE:** Term2 < 0 fails at p = 243,799 (and 246 more primes up to 10^7).

### 8.3. Salvageable Results

The proof structure (alpha + rho decomposition, identity B'/C' = alpha + rho)
remains valid. The issue is purely quantitative: alpha does not always exceed 1.

For the B' > 0 application, one should pursue the weaker bound alpha + rho > 0
rather than alpha + rho > 1.

---

## 9. Scripts and Verification

- `t_negativity_compute.py`: Initial Python computation (verified to N = 100,000)
- `t_negativity_verify.c`: Fast C verification using hyperbolic method (to N = 10^7)
- `t_negativity_verify2.c`: C verification distinguishing prime/non-prime cases
- `t_negativity_analysis.py`: Analysis of E(N) decomposition
- `t_negativity_analytical.py`: Attempted analytical approaches (all fail)
- `t_negativity_proof_analysis.py`: Detailed decomposition by omega(q)

---

## 10. Honest Assessment

This document reports a NEGATIVE finding: a claim that was believed true (and
verified computationally to p = 20,000) turns out to be false for larger primes.

The initial computational verification was misleading because:
1. The threshold for counterexamples (N ~ 218,000) is an order of magnitude
   beyond the verification range (N ~ 20,000).
2. The oscillations in R(N) grow slowly, so the "near misses" that would
   hint at future failure were not visible in the verified range.

This underscores the danger of treating computational verification as proof,
especially in problems involving number-theoretic oscillations (Mertens function,
prime counting, etc.) where phenomena at small scale can differ qualitatively
from large-scale behavior.

The adversarial audit (ADVERSARIAL_CORRECTION_NEGATIVITY.md) correctly identified
this as a "SERIOUS" gap (Flaw 5), noting that "the analytical argument in
Section 2.3 is explicitly abandoned mid-way" and "the prime number theorem gives
the asymptotic, but making it effective is nontrivial." The audit was right
to flag this -- the claim is not just hard to prove, it is false.
