# Character Sum Approach to Bounding R(p)

## Status: NEGATIVE RESULT -- naive character sum bounds are insufficient

**Date:** 2026-03-29
**Verification level:** Unverified (computational findings, no proof)

---

## Setup

For prime p with N = p-1:
- Farey sequence F_N, with |F_N| = n
- D(a/b) = rank(a/b) - n * (a/b) (Farey discrepancy)
- delta(a/b) = (a - pa mod b) / b (multiplication-by-p shift)
- R(p) = 2 * Sum D(f) * delta(f) / Sum delta(f)^2

**Goal:** Prove R(p) > -1/2 for all primes p >= 13.

**Why this matters:** B+C = Sum delta^2 * (1 + R) > 0 iff R > -1.
The stronger bound R > -1/2 gives margin.

## Empirical Findings

### 1. R(p) values for small primes

| p | R(p) | M(p) | Notes |
|---|------|------|-------|
| 5 | -1.000 | -2 | Borderline (B+C = 0) |
| 7 | -1.000 | -2 | Borderline |
| 11 | -0.518 | -2 | Below -1/2 |
| 13 | 0.120 | -3 | First prime with R > -1/2 |
| 17 | -0.277 | -2 | |
| 97 | -0.211 | 1 | |
| 199 | 6.895 | -8 | Large positive |
| 293 | 7.156 | -8 | |

**Key empirical fact:** For ALL primes p >= 13 tested (up to p = 300),
R(p) > -0.28. The bound R > -1/2 holds with significant margin.

### 2. R(p) is strongly correlated with M(p) (Mertens function)

When M(p) is very negative, R(p) is large and positive.
When M(p) is positive (e.g., p = 97, M = 1), R(p) is mildly negative.
The most negative R values occur for small p where M(p) = -2.

### 3. Per-denominator decomposition: S_b = Sum_{gcd(a,b)=1} D(a/b) * delta(a/b)

The cross-term R is a sum over denominators: Sum D*delta = Sum_b S_b.
Both positive and negative S_b values occur. The CANCELLATION between
them is essential.

## Why Character Sum Bounds Fail

### The naive approach

For each b, expand D(a/b) in Dirichlet characters mod b:
  D(a/b) = Sum_chi d_hat(chi) * chi(a)

Then S_b = Sum_chi d_hat(chi) * T_chi(b) where
  T_chi(b) = Sum_{gcd(a,b)=1} chi(a) * delta(a/b)

The Weil bound gives |T_chi(b)| <= C * sqrt(b) for non-trivial chi.

### Three fatal problems

**Problem 1: The constant C grows with p.**
The empirical best constant C such that |S_b| <= C * phi(b) * sqrt(b) / b
grows as C ~ 0.02 * p^1.26. This means the individual S_b bounds get
WORSE with p, not better.

**Problem 2: The sum of bounds diverges.**
Even with the tightest per-denominator bound:
  Sum_b |S_b|_bound / [(1/2) * Sum delta^2]
grows as ~ 0.6 * p^0.65. This ratio exceeds 1 already at p = 13.

**Problem 3: Cancellation between denominators is essential.**
For p = 97: the negative S_b contributions total -312.6, while
the threshold is -112.8. The positive S_b contributions (total +265.1)
are essential for keeping R > -1/2. Any approach that bounds |S_b|
individually and then sums will lose this cancellation.

The cancellation factor (Sum |S_b| / |Sum S_b|) grows with p:
  p=13: 2.7x
  p=97: 12.1x
  p=199: 1.0x (accidentally small)

### The "weil_tight" bound sqrt(phi(b) * b)

This tighter bound |S_b| <= C' * sqrt(phi(b) * b) does hold for all
tested cases with C' < 0.6, but:
- Summing it still gives a ratio > 1
- It doesn't capture the signed structure

## What Would Work

### Approach A: Mertens function connection

Since R(p) correlates strongly with M(p), and M(p) >= -2 for p >= 13
(actually the minimum of M up to 200 is M(113) = -5, M(197) = -7, etc.),
the connection R(p) ~ f(M(p)) might give a route. But M(p) can be
arbitrarily negative for large p, so this correlation might not persist.

Actually, R(p) is POSITIVELY correlated with -M(p): when M is very negative
(e.g., M(199) = -8), R is very positive (R ~ 6.9). This means the Mertens
function HELPS -- the more negative M(p), the more R is pushed positive.
The dangerous regime is M(p) positive or close to 0.

### Approach B: Structural cancellation proof

Prove that the positive S_b and negative S_b contributions cancel to give
Sum D*delta > -(1/4) * Sum delta^2.

This requires understanding WHY positive S_b terms outweigh the
negative deficit. The structure of D(a/b) (which involves counting
Farey fractions) and delta(a/b) (which involves multiplication by p)
have correlated arithmetic structure.

### Approach C: Direct asymptotic analysis

Sum D(f)*delta(f) can be related to sums involving the Mobius function:
  Sum D(a/b) * delta(a/b) ~ Sum involving mu(b) and M(p-1)

If this connection can be made explicit, the asymptotic behavior of
M(N) provides the bound. Known bounds: |M(N)| = O(N / log N) (unconditional),
|M(N)| = O(N^{1/2+eps}) (assuming RH).

### Approach D: Proved for p >= p_0, check small cases

Since the character sum analysis shows |S_b| / sqrt(phi(b)*b) < 0.57
for all tested b and p, and this ratio might decrease for large p:
- Prove |S_b| <= C * sqrt(phi(b)*b) with C < 1 for all b
- Show the sum converges for large p
- Computer-check all primes p < p_0

## Conclusion

**The naive per-denominator Weil bound approach CANNOT prove R(p) > -1/2.**
The bounds are too loose by a factor that grows as p^0.65.

The fundamental obstacle is that positive and negative S_b contributions
nearly cancel, and any absolute-value-based bound destroys this cancellation.

**Recommended next steps:**
1. Investigate the M(p) <-> R(p) connection analytically
2. Try the large sieve on the full sum (not per-denominator)
3. Look for a direct evaluation of Sum D*delta in terms of arithmetic functions
4. Approach D: prove for p >= p_0 with asymptotic argument, check small p

## Files

- `character_sum_proof.py` -- full computational analysis
- `r_cancellation_analysis.py` -- earlier cancellation study
- `large_sieve_R_bound.py` -- large sieve approach
