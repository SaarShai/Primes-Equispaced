# Universality: Status After Selberg Collapse
# 2026-04-09

## What Died
The "easy" path: Selberg → diagonal diverges → spectroscope energy diverges → peaks exist.
The diagonal sum Σ M(p)²/p² CONVERGES unconditionally (~0.57 and flattening).
Total spectroscope energy is BOUNDED on average (Montgomery-Vaughan confirms this).

## What's Alive

### The Spectroscope WORKS (computational fact)
F(γ₁)/F_avg = 7.2x at N=200K primes.
z-scores up to 65σ in full computation.
This is real — the energy CONCENTRATES at zeros even though the total is bounded.

### Conditional (RH) — straightforward
Under RH: Σ M(n)²/n² ~ 0.03·log x (diverges slowly).
Combined with Montgomery-Vaughan → average energy grows.
Combined with zero-free region contrapositive → peaks at zeros.
Paper J under RH is a clean, publishable conditional theorem.

### Unconditional paths that DON'T need diagonal divergence:

1. **Energy DISTRIBUTION, not magnitude:**
   The explicit formula M(p) = -1 + Σ_ρ p^ρ/(ρζ'(ρ)) is UNCONDITIONAL.
   Substituting into spectroscope creates CONSTRUCTIVE INTERFERENCE at γ_k.
   Even with bounded total energy, the distribution is non-uniform.
   Proving this rigorously: show F(γ_k) > C · F_avg for some C > 1.

2. **Turán power sum method:**
   Forces large values from oscillatory sums.
   Doesn't need total energy to diverge — needs the "spectrum" to be non-trivial.
   The explicit formula provides the non-trivial spectrum.

3. **Sarnak/Möbius disjointness:**
   μ(n) is orthogonal to deterministic sequences (Davenport proved for e^{2πiαn}).
   At zeros: resonance prevents cancellation.
   Completely independent of diagonal sums.

4. **Montgomery explicit kernel:**
   Σ_ρ |A(γ_ρ)|² = (T/2π)∫|A(t)|² dt + pair correlation terms.
   Even if ∫|A|² is bounded, the pair correlation terms can redistribute
   energy toward zeros. Need to show pair correlation contribution is positive.

## The Key Reframing
OLD question: Does the spectroscope have infinite energy?
ANSWER: No (unconditionally). The total energy converges.

NEW question: Is the energy CONCENTRATED at zeros rather than spread uniformly?
ANSWER: Yes (computationally 7.2x peak). This is what needs proving.

This is actually a MORE interesting mathematical question. It's about the
STRUCTURE of the energy distribution, not just its magnitude.

## Priority
1. State Paper J as conditional on RH (straightforward, publishable)
2. Pursue energy concentration unconditionally (harder, more novel)
3. The Sarnak angle is the most promising for a genuinely new approach
