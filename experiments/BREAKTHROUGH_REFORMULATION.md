# BREAKTHROUGH: Two Exact Identities and B+C Reformulation
## Date: 2026-03-29
## Status: 🔬 Unverified — computationally confirmed, independent verification running

---

## Identity 1: Permutation Square-Sum
**Σ (a/b)·δ(a/b) = (1/2)·Σ δ(a/b)²** i.e., **Σ x·δ = C/2**

Proof: δ = x - {px}, so x·δ - δ²/2 = (x² - {px}²)/2. Since a→pa mod b is a permutation, Σ(a/b)² = Σ(pa mod b/b)² per denominator, so the sum vanishes. □

## Identity 2: T(p) = -C/2 (trivial corollary)
Define T(m) = Σ_{a/b ∈ F_N, b>1} {am/b}·δ(a/b). Then:
- **T(1) = C/2** (Identity 1)
- **T(p) = -C/2** (since δ = x-{px}, T(p) = Σ(x-δ)·δ = T(1) - C = -C/2)

## Main Reformulation
From D(x) = -x - R(x) where R(x) = Σ_{d≤N} μ(d)·Σ_{m≤N/d} {xm}:

**B + C = -2·Σ R(x)·δ(x)**

Expanding R as a Möbius sum:

**B + C = -2·Σ_{d≤N} μ(d)·Σ_{m=1}^{⌊N/d⌋} T(m)**

where T(m) = Σ (σ_m(a)/b)·δ(a/b) and σ_m(a) = ma mod b.

## Kloosterman Connection
For fixed b with gcd(m,b)=1:
Σ_{gcd(a,b)=1} (ma mod b)·(a - pa mod b) = K(1,m;b) - K(m,p;b)

where K(a,b;c) = Σ_{x coprime to c} ax · bx^{-1} (mod c) is the Kloosterman sum.

**Weil's bound**: |K(a,b;c)| ≤ d(c)·√c where d(c) = number of divisors.

## Proof Strategy (NEW)
1. Bound |T(m)| ≤ Σ_b d(b)·√b / b² ~ (constant) using Kloosterman/Weil bounds
2. The Möbius sum Σ_d μ(d)·Σ_{m≤N/d} T(m) involves Mertens-type cancellation
3. Sign analysis: d=1 term (positive) vs Möbius corrections (negative → makes total negative)
4. Need: |Möbius corrections| > d=1 term, which is what makes B+C > 0

## Empirical Data
Σ R·δ < 0 for ALL primes tested (5, 7, 11, 13, 17, 23, 29, 37, 53).

d=1 contribution is always POSITIVE. Möbius corrections from d=prime (μ=-1) make total negative. The Sign Theorem is equivalent to: the Möbius cancellation overwhelms the base sum — exactly the regime where M(p) being negative helps!

## Connection to N2 (Mertens-Discrepancy)
B+C > 0 ⟺ Σ R·δ < 0 ⟺ Möbius cancellation in fractional part sums × δ is net negative.
This is precisely the M(p) ↔ ΔW(p) connection (N2) made algebraically precise!
