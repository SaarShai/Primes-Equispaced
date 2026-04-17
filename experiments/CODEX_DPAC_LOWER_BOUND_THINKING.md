# CODEX THINKING: Uniform Lower Bound for |c_K(ρ)|
**Date:** 2026-04-12  
**Task:** Can we prove |c_K(ρ)| > f(K) > 0 for ALL nontrivial zeros ρ simultaneously?

## Bottom Line
**Uniform lower bound is NOT provable with current tools.**
Strongest reachable: for fixed ρ, |c_K(ρ)| ≍ log K / |ζ'(ρ)| (eventually nonzero). For density-one zeros up to height T: lower bound ≫ log K / (log T)^A under strong average hypotheses (not uniform).

## Correction
The asymptotic is c_K(ρ) ~ log(K)/ζ'(ρ), NOT log(K)/ζ(ρ) — ζ(ρ)=0 at zeros, so latter is undefined. Multiplicity m>1 zeros give polynomial in log K of degree m-1.

## Approach 1 — Perron + Error (MOST PROMISING)
- Clean residue formula: double pole at w=0 gives (log K)/ζ'(ρ)
- Error term: E(K,ρ) = Σ_{ρ'≠ρ} K^{ρ'-ρ} / ((ρ'-ρ)ζ'(ρ')) + O(K^{-1/2+ε})
- Cauchy-Schwarz: |E| ≤ (Σ 1/|ρ'-ρ|²)^{1/2} · (Σ 1/|ζ'(ρ')|²)^{1/2}
- First factor blows up at small gaps. Second = Gonek-Hejhal discrete moment.
- **Key missing lemma**: pointwise upper bound on |ζ'(ρ)| uniform in ρ + uniform control of off-diagonal zero sum. Moment conjectures don't give this.

## Approach 2 — Counting
- c_K has O(T log K) zeros in [0,T]; ζ has ~T log T /2π zeros.
- c_K zeros much sparser than ζ zeros — but no rigorous separation without joint zero-distribution theorem.
- **Missing**: independence principle / pair-correlation / equidistribution relating zeros of c_K to zeros of ζ.

## Approach 3 — Euler Product Structure
- c_K(s) ≠ Π_{p≤K}(1-p^{-s}). Sharp cutoff correction destroys multiplicativity.
- c_K(s) = Π_{p≤K}(1-p^{-s}) - Σ_{n>K, P+(n)≤K} μ(n)n^{-s}
- Correction is NOT a small perturbation on Re(s)=1/2.
- Essentially no lower bound from product structure.

## Approach 4 — Why the 1/ζ Tail Argument Fails
- Identity 1/ζ(s) = Σ μ(n)n^{-s} valid only for Re(s) > 1.
- CANNOT write c_K(ρ) = 1/ζ(ρ) - tail(ρ) — both sides meaningless at ρ.
- Perron gives the correct mechanism: double pole residue → log K / ζ'(ρ).

## Strongest Statements
1. Fixed zero ρ: c_K(ρ) ~ log(K)/ζ'(ρ) → eventually nonzero (Perron + contour justification)
2. Density-one: under GH moments + zero spacing → lower bound ≫ log K / (log T)^A (height-dependent, not uniform)
3. All zeros simultaneously for fixed K: NOT within reach

## For Paper C
- Tier 3 should be stated as "density-one" or "all but finitely many" (NOT uniform)
- The correct statement: "for each nontrivial zero ρ, |c_K(ρ)| → ∞ as K → ∞ (under simple zero hypothesis)"
- Uniform: impossible without breakthrough in zero-distribution theory
