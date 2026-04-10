# Unconditional Bounds from Verified Zeros: NEGATIVE RESULT
# 2026-04-10

## VERDICT: Spectroscope verification does NOT give useful unconditional bounds.

## Key Finding
GRH bound (2(log p)²) only beats Burgess bound (p^{0.151}) at p > 10^25.
At ALL practical primes (p < 10^20), Burgess is already better.

Partial zero verification to height T=80 gives WORSE bounds than Burgess
because the tail from unverified zeros (using zero-free region constants)
produces astronomically large terms.

## The Math
- Burgess: n_χ(p) ≤ p^{0.151} — unconditional, good for small p
- GRH: n_χ(p) ≤ 2(log p)² — conditional, good for HUGE p
- Crossover: p ≈ 10^25
- Spectroscope verifies to T≈80: tail bound exp(C·(log p)²/T) overflows

## Conclusion
This is a DEAD END for practical applications.
The spectroscope doesn't help with unconditional bounds on quadratic nonresidues.
