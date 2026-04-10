# Codex: R₂ Positivity Analysis (MPR-58)
# 2026-04-09

## Key Finding
Every new fraction in F_N \ F_{N-1} IS the mediant of its two old neighbors, for ALL N (not just primes). The "composites create non-mediant insertions" premise is FALSE. Lean-verified in GeneralInjection.lean.

## Two Different R₂ Definitions

1. **Gap-splitting functional** (convex dependence on gap lengths): R₂ > 0 is PROVABLE for every N ≥ 2. For any gap g split into x and g-x, local squared-gap energy changes by g² - x² - (g-x)² = 2x(g-x) > 0. Always positive regardless of split ratio. Fisher-information-style functional is universally monotone.

2. **Wobble response term** (old-fraction response in ΔW decomposition): UNPROVED for all composites. This is a correlation term, not just a local split term.

## The Exact Obstruction
The wobble response is a CORRELATION: Σ_{old f} D_old(f) · δ_N(f), where δ_N(f) contains divisor-sieve corrections. For composite N, the count of new fractions below old f involves inclusion-exclusion: #{k ≤ Nf : gcd(k,N)=1} = Σ_{d|N} μ(d)⌊Nf/d⌋. For primes this collapses to a single sawtooth; for composites, divisor terms introduce oscillations.

## Attack Vectors
1. Derive explicit composite shift formula as divisor-weighted sawtooth sum
2. Use f ↔ 1-f symmetry to cancel odd parts
3. Reindex by denominator → Ramanujan/Dedekind pieces
4. Prove denominator-by-denominator lower bound: convex gap gain dominates divisor-correlation error
5. Clean theorem NOW: state for gap-energy functional (provable), use as surrogate lemma

## Status
- Gap-energy R₂ > 0: PROVABLE (for Paper A as Theorem)
- Wobble R₂ > 0: OPEN (obstruction identified — divisor-sieve correlations)
