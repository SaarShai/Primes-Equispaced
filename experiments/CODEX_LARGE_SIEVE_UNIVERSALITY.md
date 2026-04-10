# Codex: Large Sieve Approaches to Universality
# 2026-04-09

## Verdict: Large sieve CANNOT prove universality alone.
Large sieve = upper bounds / averages. Universality needs pointwise LOWER bounds.

## Ranking of approaches:
1. Turán power sum — ONLY genuine lower-bound tool. Needs local resonance/non-cancellation.
2. Large sieve + explicit formula — sees primes and zeros, but cross-terms brutal.
3. Gallagher/mean-value — strongest average control, but average→pointwise gap unsolved.
4. Dual large sieve — same barrier as direct, in dual form.
5. Direct large sieve — pure upper bound, dead end.

## Key insight: Turán is the right tool
Turán's method forces large values from oscillatory sums.
Needs: local lower bound for zero-weighted coefficients in short window ~1/log γ_k.
If local non-cancellation can be proved → peaks at specific zeros.

## Note from Codex
"The explicit formula weight is 1/ζ'(ρ), not 1/(ρ·ζ'(ρ))"
CORRECTION: For M(x), the weight IS 1/(ρ·ζ'(ρ)). For Σ μ(n)/n^s, it's 1/ζ'(ρ).
Our spectroscope uses M(p)/p, so the relevant weight depends on the formulation.
