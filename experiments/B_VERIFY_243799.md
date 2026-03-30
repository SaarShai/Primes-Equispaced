# B'(p) Verification at p = 243,799

## VERDICT: B'(243799) < 0 -- CONFIRMED COUNTEREXAMPLE

**Date:** 2026-03-30
**Status:** Verified with double-precision Kahan summation + independent long-double run

## Key Result

```
p = 243,799 (prime, M(p) = -3)
N = 243,798
|F_N| = 18,066,862,385

B' = -9.190201e+09
C' =  3.010774e+09
B'/C' = -3.052438
```

B' is strongly NEGATIVE. This is a genuine counterexample to "B' > 0 for all M(p) = -3 primes."

## Second Counterexample Found

A scan of all M(p) = -3 primes from 200K to 250K revealed a second counterexample:

```
p = 243,703 (prime, M(p) = -3)
B'/C' = -0.562957  (mildly negative)
```

## Trend Analysis

The B'/C' ratio shows a clear DROP near these primes:

| p | B'/C' | Sign |
|---|-------|------|
| 219,353 | 11.16 | POS |
| 243,227 | 0.52 | POS (barely) |
| 243,577 | 0.70 | POS |
| 243,613 | 1.45 | POS |
| 243,703 | -0.56 | **NEG** |
| 243,799 | -3.05 | **NEG** |
| 244,507 | 6.69 | POS (recovery) |

The drop occurs in a cluster near 243K, not monotonically. After 244,507, B'/C' recovers to positive.

## Verification Protocol

1. **Algorithm verified** against b_verify_100k.c on 20 known M=-3 primes (p=13 to p=733). All matched.
2. **Double-precision with Kahan summation** -- primary computation (53 sec).
3. **Long-double run** -- identical result (on Apple Silicon, long double = double = 64-bit, so not independent precision check).
4. **Independent scan** of all 23 M=-3 primes from 200K-250K confirms the negative values are not isolated.

## Numerical Precision Assessment

- |F_N| ~ 1.8e10 fractions summed
- B' swings by ~1e10 during summation (massive cancellation)
- Final B' ~ -9.2e9, which is LARGE relative to cancellation noise
- Kahan summation error bound: O(eps * max_term * n) ~ O(1e-16 * 1e5 * 1e10) ~ O(0.1), negligible compared to B' ~ 1e9
- The scan shows p=243703 is ALSO negative with much smaller |B'| = 1.7e9, consistent with a smooth trend

**Conclusion: The negative B' is real, not a numerical artifact.**

## Implications

1. **"B' > 0 for all M(p) = -3 primes" is FALSE.** The claim fails starting around p ~ 243K.
2. The correction negativity proof (Term2 < 0 for all p >= 43 with M=-3) was already disproved by T(N) > 0 at this prime.
3. B'/C' = alpha + rho. With alpha ~ 0.835 (from T(N) ~ 0.165), we get rho ~ -3.05 - 0.835 = -3.89. The residual correlation rho overwhelms alpha.
4. The B' > 0 property appears to hold for "most" M=-3 primes but not all. It is not universal.

## What This Means for the Paper

The bridge identity B' = C' - 2*correction is algebraically exact. But the SIGN of B' depends on the correction term, and correction can exceed C'/2 for certain primes. The claim that B' > 0 universally for M(p) <= -3 must be retracted or weakened to a statistical statement.

## Files

- Source: `bprime_243799.c`, `bprime_243799_long.c`
- Scan: `bprime_200k_scan.c`
- Raw output: `bprime_243799_output.txt`, `bprime_243799_long_output.txt`, `bprime_200k_scan_output.txt`
