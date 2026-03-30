# NEW DISCOVERY: Permutation Square-Sum Identity

## Date: 2026-03-29
## Status: 🔬 Unverified — computationally confirmed, needs independent verification

## The Identity

For prime p and N = p-1, summing over all a/b ∈ F_N with b > 1:

**Σ (a/b)·δ(a/b) = (1/2)·Σ δ(a/b)²**

where δ(a/b) = (a - pa mod b)/b.

Equivalently: **Σ x·δ(x) = C/2** where C = ||δ||².

## Proof (7 lines)

1. Write δ = x - {px} where x = a/b, so x·δ = x² - x·{px} and δ² = x² - 2x·{px} + {px}².
2. Then x·δ - δ²/2 = x²/2 - {px}²/2 = (x² - {px}²)/2.
3. Sum over all coprime a with fixed b: Σ_a [(a/b)² - (pa mod b)²/b²].
4. Since a → pa mod b is a **permutation** of coprime residues mod b (as gcd(p,b)=1):
   Σ (a/b)² = Σ (pa mod b)²/b², so each inner sum vanishes.
5. Total: Σ(x·δ - δ²/2) = 0, hence **Σ x·δ = C/2**. □

## Consequence

Combined with D(x) = -x - R(x) (from Möbius inversion of Farey rank):

- B/2 = Σ D·δ = -Σ x·δ - Σ R·δ = -C/2 - Σ R·δ
- **B + C = -2·Σ R(x)·δ(x)**

where R(x) = Σ_{d≤N} μ(d) · Σ_{m=1}^{⌊N/d⌋} {x·m}

## Significance

The Sign Theorem (B+C > 0) now reduces to:

**Σ R(x)·δ(x) < 0**

i.e., the Möbius-weighted fractional-part function R is negatively correlated with δ.

This is a **massive simplification** — from a quadratic identity involving D (rank displacement) to a LINEAR condition on R (Möbius fractional parts) × δ (multiplicative displacement).

## Verification

Confirmed with **exact Fraction arithmetic** for all primes p = 5, 7, 11, 13, ..., 101, 103.

## Classification

Autonomy: A (discovered by AI autonomously during proof exploration)
Significance: Pending — need to check if this identity is known
