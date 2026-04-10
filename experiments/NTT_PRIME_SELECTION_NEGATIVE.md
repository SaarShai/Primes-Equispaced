# NTT Prime Selection Test: NEGATIVE RESULT
# 2026-04-10

## VERDICT: Spectroscope has NO predictive power for NTT prime selection.

## Results
- Only 4 primes p≡1 mod 256 in [2000,10000]: 3329, 7681, 7937, 9473
- 3329 wins on total twiddle-factor Hamming weight (1442 vs 1594 next-best)
- Corr(M(p), total_HW) = +0.09 — NO SIGNAL
- The dominant factor is simply prime SIZE (bits). Corr(p, total_HW) = +0.92

## Why 3329 is already optimal
- Smallest prime ≡1 mod 256 above ~2000
- 12 bits (all others need 13-16)
- p-1 = 2⁸·13 (highly 2-adic)
- Chosen for Kyber because of LWE noise requirements, not NT structure

## Honest conclusion
The efficiency is dominated by a trivial factor (prime size in bits).
Our spectroscope detects zeros, not bit-level properties of primes.
This is a DEAD END for practical crypto applications.
