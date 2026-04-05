# Composite Healing Characterization

## Theorem (Computational)
For N ≤ 500:
- ΔW(n) > 0 for ALL composite n with ω(n) ≥ 2 (2+ distinct prime factors)
- ΔW(p^k) can be negative (prime powers behave like primes)
- The non-healing set is EXACTLY the prime powers

## Interpretation
The number-theoretic boundary between damage and healing is:
- ω(n) = 1 (primes and prime powers): can damage regularity (ΔW ≤ 0)
- ω(n) ≥ 2 (composites with 2+ factors): ALWAYS heal regularity (ΔW > 0)

## Why prime powers behave like primes
For n = p^k: φ(p^k)/p^k = 1 - 1/p (same density ratio as prime p itself).
The new fractions a/p^k with gcd(a,p^k)=1 have the SAME density structure
as fractions a/p, just at a higher denominator. The "damage" mechanism
is identical — only the scale changes.

## For composites with ω ≥ 2
For n = p₁^{a₁}·p₂^{a₂}·...·: φ(n)/n = Π(1 - 1/pᵢ) is SMALLER than any 1 - 1/pᵢ.
Fewer new fractions (as a proportion) → less disruption → healing dominates.
The multiple prime factors create INTERFERENCE that cancels the damage.
