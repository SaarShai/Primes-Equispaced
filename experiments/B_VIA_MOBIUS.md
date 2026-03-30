# B >= 0 via Mobius Reformulation

## Setup

For prime p with N = p-1, the four-term decomposition gives:
- B = 2 * sum_F D(x) * delta(x), where D(x) = rank(x) - n*x
- C = sum_F delta(x)^2
- R(x) = -D(x) - x, so D = -R - x

The Mobius reformulation:
    R(x) = sum_{d <= N} mu(d) * S(x, floor(N/d))
where S(x, M) = sum_{m=1}^M {xm} (sum of fractional parts).

## Key Identities (all verified numerically)

1. **B + C = -2 * sum R*delta** (definition of R = -D - x)
2. **sum x*delta = C/2** (permutation identity)
3. **B = -C - 2*sum(R*delta)**
4. **B >= 0 iff sum(R*delta) <= -C/2**

## Abel Summation Decomposition

Apply Abel summation to R(x) = sum_{d=1}^N mu(d) * S(x, floor(N/d)):

    R(x) = M(N) * {x} + sum_{k=1}^{N-1} M(k) * Delta_S_k(x)

where:
- M(k) = sum_{d=1}^k mu(d) is the Mertens function
- Delta_S_k(x) = S(x, floor(N/k)) - S(x, floor(N/(k+1))) >= 0
- M(N) = M(p-1) = M(p) + 1 (since p is prime, mu(p) = -1)

Summing against delta over the Farey sequence:

    sum R*delta = M(p-1) * sum(x * delta) + sum_{k<N} M(k) * sum_x Delta_S_k * delta

## The Leading Term (EXACT)

    Term1 = M(p-1) * sum(x*delta) = M(p-1) * C/2

This uses the exact identity sum x*delta = C/2 (permutation identity).

Dividing by -C/2:

    Term1 / (-C/2) = -M(p-1) = |M(p)| - 1

**For M(p) <= -3: the leading term alone gives |sum R*delta| >= 2 * (C/2) = C > C/2.**

## Proof Structure

**Theorem (conditional on correction bound):** If M(p) <= -3, then B >= 0.

**Proof sketch:**

Write sum(R*delta) = M(p-1) * C/2 + Term2, where Term2 is the Abel correction.

B >= 0 iff sum(R*delta) <= -C/2, i.e.:

    M(p-1) * C/2 + Term2 <= -C/2
    Term2 <= -(1 + M(p-1)) * C/2 = -M(p) * C/2 = |M(p)| * C/2

Since M(p-1) = M(p) + 1 <= -2, the leading term already gives:

    M(p-1) * C/2 <= -2 * C/2 = -C

So we need the correction Term2 to satisfy:

    Term2 <= |M(p)| * C/2

Equivalently, defining correction = Term2 / (-C/2):

    correction >= -(|M(p)| - 2)

For |M(p)| >= 4, this means correction >= -2 or less (easily satisfied).
For M(p) = -3 (|M(p)| = 3), this means **correction > -1**.

## Numerical Verification (45 primes, p <= 500)

| p | M(p) | Leading | Correction | Ratio | B >= 0? |
|---|------|---------|------------|-------|---------|
| 13 | -3 | 2 | -0.8801 | 1.12 | YES |
| 19 | -3 | 2 | -0.6680 | 1.33 | YES |
| 31 | -4 | 3 | -0.4440 | 2.56 | YES |
| 43 | -3 | 2 | +0.3535 | 2.35 | YES |
| 73 | -4 | 3 | +0.7982 | 3.80 | YES |
| 113 | -5 | 4 | +1.4153 | 5.42 | YES |
| 199 | -8 | 7 | +0.8948 | 7.89 | YES |
| 293 | -8 | 7 | +1.1564 | 8.16 | YES |
| 443 | -9 | 8 | +0.4629 | 8.46 | YES |

**All 45 primes with M(p) <= -3 up to p = 500 satisfy B >= 0.**

Average correction by M(p):
- M(p) = -3: avg = +1.74, min = -0.88 (p=13), always > -1
- M(p) = -4: avg = +1.96, min = -0.44 (p=31), always > -1
- M(p) = -5: avg = +2.27, min = +0.88 (p=191), always > 0
- M(p) <= -6: all corrections positive

## Why the Correction is Bounded

The correction Term2 = sum_{k=1}^{N-1} M(k) * sum_x Delta_S_k(x) * delta(x).

**Key observations:**

1. **Cancellation structure:** The inner sum sum_x Delta_S_k * delta involves correlation
   between fractional part sums and the delta function. For most k, this oscillates
   and cancels heavily (visible in the d-by-d decomposition where individual d-terms
   have magnitude ~C but alternate signs).

2. **The d=1 term opposes the leading term:** When decomposed by Mobius contributions
   rather than Abel, the d=1 term (S(x,N) alone) gives POSITIVE sum*delta, while the
   Mobius corrections (d >= 2) collectively dominate and make the total negative.

3. **Growth with p:** For large p, the correction grows positively (empirically ~log(p)),
   which means the ratio sum(R*delta)/(-C/2) grows beyond |M(p)|-1. The leading term
   is the MINIMUM contribution.

## The Gap to a Full Proof

What remains to prove analytically:

1. **For M(p) = -3:** Show that correction > -1. This is the tightest case.
   - Worst observed: p=13 with correction = -0.88
   - For p >= 43 with M(p)=-3, correction is always positive
   - Need: explicit bound on |Term2| / (C/2) for small primes, or direct verification for p = 13, 19

2. **For M(p) <= -4:** The margin is large (leading >= 3, correction > -1 always).
   Any reasonable bound on Term2 suffices.

3. **Bounding Term2 in general:** Term2 involves the weighted Mertens function
   sum M(k) * f(k) where f(k) = sum_x Delta_S_k * delta. The function f has
   zero mean (by Mobius inversion) and oscillates, so the sum is controlled
   by the oscillation of M(k), not its size.

## Possible Analytical Approaches

### Approach A: Direct computation for small primes + asymptotic bound
- For p in {13, 19}: compute B exactly (done, both B > 0)
- For p >= 23 with M(p) <= -3: use the fact that correction grows with p
- Need: monotonicity or lower bound for correction as function of p

### Approach B: Variance bound on Term2
- Term2 = sum M(k) * c_k where c_k = sum_x Delta_S_k * delta
- By Cauchy-Schwarz: |Term2|^2 <= (sum M(k)^2) * (sum c_k^2)
- The c_k are "correlation coefficients" of Delta_S functions with delta
- If sum c_k^2 = o(sum M(k)^2), then Term2 = o(||M||_2) which is sublinear in the leading term

### Approach C: Reformulate as Dedekind sum identity
- S(a/b, M) involves Dedekind-sum-type expressions
- The Mobius transform of Dedekind sums may have known closed forms
- Connection to Rademacher-type reciprocity?

## Summary

The Mobius reformulation reduces B >= 0 to:

    sum R(x) * delta(x) <= -C/2

Abel summation extracts the EXACT leading term:

    M(p-1) * C/2 = -(|M(p)| - 1) * C/2

For M(p) <= -3, this leading term already gives |(leading)| >= 2 * C/2 > C/2.
The correction is empirically bounded by max |-0.88| < 1, so the sum exceeds C/2
in absolute value for ALL tested primes.

**The proof reduces to bounding the Abel correction, which is the correlation of
a Mobius-weighted fractional-part-sum oscillation with the delta function.**

---
Date: 2026-03-30
Status: Partial analytical proof. Leading term exact, correction empirically bounded.
Verification: 45 primes up to p=500, all B >= 0 confirmed.
