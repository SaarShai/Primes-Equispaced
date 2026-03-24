# Exploration Summary — Day 2

## Certified Results

1. **Counterexample p=92,173 CERTIFIED** with 256-bit MPFR interval arithmetic
   - ΔW = +3.5614 × 10⁻¹¹ (positive despite M=-2)
   - Interval widths: S2 ~ 10⁻⁶⁰, R ~ 10⁻⁵⁰ (39+ orders of magnitude below |ΔW|)
   - Total computation: 28 minutes (842s + 843s)

## New Lean Formalizations (Aristotle)

2. **CharacterBridge.lean** — 11 results, 0 sorry
   - Character-weighted bridge: Σ χ(denom)·e^{2πimf} = 1 + Σ(χ·μ)(b)
   - Extends framework to all Dirichlet L-functions and GRH

3. **InjectionPrinciple.lean** — 11 results, 0 sorry
   - Each Farey gap gets at most one k/p fraction
   - Complete proof: adjacency → b+d≥p → bd≥p-1 → interval<2 → ≤1 integer

4. **Formalization totals**: 6 files, 90 results, 1 sorry (MertensGrowth only)

## New Identities (Proved)

5. **Σ D(a/b) = -φ(b)/2** for each denominator b
   - The total displacement of fractions with fixed denominator b is exactly -φ(b)/2
   - Universal (holds for any Farey order N ≥ b)
   - Proof: Farey symmetry f↔1-f pairs ranks summing to n-1

6. **δ vanishes at b | (p-1)**: When p ≡ 1 (mod b), multiplication by p is identity, so δ(a/b) = 0
   - Cross term contributions come only from b where p ≢ 1 (mod b)

7. **Involution formula**: For p ≡ -1 (mod b): C_b = (2/b)Σa·D(a/b) + φ(b)/2

## Structural Insights

8. **Cross term is pure covariance**: Σ δ = 0 per denominator (from coprime permutation), so Σ D·δ measures correlation, not means

9. **Multiplicative order controls cycle structure**: Higher ord_b(p) → more complex permutation → larger |C_b|

10. **Connection to Kloosterman sums**: The twisted sum Σ a·σ_p(a) has Kloosterman structure, but the D-weighting brings in global Farey structure that resists standard bounds

## Algorithmic Results

11. **Batch Farey Sum Algorithm**: 1,373× speedup for computing S(m,N) at many frequencies

12. **Large-scale Mertens statistics** up to N=500,000:
    - max M = 244 at N=463,139 (M/√N = 0.36)
    - min M = -258 at N=355,733 (M/√N = -0.43)
    - 41,534 primes analyzed; 52% have M>0, 47% have M<0

## Negative Results (Honest)

13. **No faster Mertens**: Universal formula doesn't improve on O(N^{2/3}) Meissel-Lehmer

14. **Partial anticorrelation fails**: C_b can be positive even for small b (e.g., C_3 > 0 at p=53), so per-denominator bounds don't close the problem

15. **First moment has no universal formula**: Σ a·D(a/b) depends on global Farey structure, unlike the zeroth moment which is always -φ(b)/2

## Open Directions

- Kloosterman/Weil bounds on the twisted cross term (most promising for anticorrelation)
- Three-distance theorem connection to gap structure (agent exploring)
- Sawtooth decomposition δ = ((f)) - ((pf)) → Dedekind sum connection
- Character Mertens correlation with prime races (0.46 correlation)

## Late Session Discoveries

16. **Modular inverse neighbor theorem** (from three-distance agent):
    Left neighbor of k/p has denominator b = k⁻¹ mod p.
    Sub-gaps: 1/(pb) left, 1/(pd) right, with b+d=p.

17. **New-fraction displacement formula** (verified exactly):
    D_new(k/p) = k/p - n/(pb) + D_old(a/b)  where b = k⁻¹ mod p
    The entire new-fraction wobble is a sum over modular inverses!

18. **Injection = invertibility**: The Injection Principle is equivalent
    to multiplication being invertible in (Z/pZ)* (one-line algebraic proof).

19. **Multiplicity-two property**: Among gaps adjacent to new k/p fractions,
    each width 1/(pj) appears exactly twice.
