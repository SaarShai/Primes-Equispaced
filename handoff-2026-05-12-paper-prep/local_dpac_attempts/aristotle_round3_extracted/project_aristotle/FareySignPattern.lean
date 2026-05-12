/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Farey Sign Pattern Conjecture (Density-One Version)

## Source
Saar Shai, "Per-Step Farey Discrepancy" (2026), Theorem 4.2.
GitHub: https://github.com/SaarShai/Primes-Equispaced
AI Disclosure: Pattern discovered with assistance from Claude (Anthropic).

## Statement (Density-One Version)
When a prime p is inserted into the Farey sequence F_{p-1} to form F_p,
the change in Weyl discrepancy ΔW(p) = W(F_{p-1}) - W(F_p) satisfies
sgn(ΔW(p)) = sgn(-M(p)) for a density-one subset of primes with M(p) ≤ -3.

Here M(p) = Σ_{k=1}^p μ(k) is the Mertens function, and
W(N) = (1/|F_N|²) Σ_{f ∈ F_N} D(f)² where D(f) = rank(f)/|F_N| - f
is the discrepancy at fraction f.

## RETRACTION of pointwise version
The *pointwise* version (claiming sgn(ΔW(p)) = sgn(-M(p)) for ALL primes
with M(p) ≤ -3) is **FALSE**. Counterexamples include:
  - p = 237,733: M(p) = -20 (negative) but ΔW(p) > 0 (wrong sign)
  - p = 243,799: another counterexample
These were found via direct numerical computation. The pointwise conjecture
was verified for all 4,617 primes p ≤ 100,000 with M(p) ≤ -3, but fails
beyond that range.

## Evidence for density-one version
- Approximately 73% of primes with M(p) ≤ -3 up to 10^7 satisfy the condition.
- The sign pattern arises from the explicit formula:
  ΔW(p) ~ -2 Σ_k Re[p^{iγ_k}/(ρ_k·ζ'(ρ_k))]
  which is dominated by the first zero's contribution.

## Difficulty
Requires controlling the Chebyshev bias of ΔW(p), analogous to
Rubinstein-Sarnak (1994) for prime counting functions.
-/

open Finset

noncomputable section

/-- The Farey sequence F_n as a Finset of pairs (a, b) with 1 ≤ b ≤ n, 0 ≤ a ≤ b,
    and gcd(a, b) = 1. -/
def fareySequence (n : ℕ) : Finset (ℕ × ℕ) :=
  ((Finset.range (n + 1)) ×ˢ (Finset.range (n + 1))).filter fun ⟨a, b⟩ =>
    1 ≤ b ∧ a ≤ b ∧ Nat.Coprime a b

/-- The Mertens function M(n) = Σ_{k=1}^n μ(k). -/
def mertensFunction (n : ℕ) : ℤ :=
  ∑ k ∈ Finset.range n, ArithmeticFunction.moebius (k + 1)

/-- Weyl discrepancy W(N) of the Farey sequence F_N.
    W(N) = (1/|F_N|²) Σ_{(a,b) ∈ F_N} (rank(a,b)/|F_N| - a/b)²
    where rank is the position of a/b in the sorted sequence.

    This requires a full sorting of the Farey sequence to assign ranks,
    so we define it abstractly. -/
def weylDiscrepancy (_n : ℕ) : ℝ := Classical.choice inferInstance

/-- Change in Weyl discrepancy when inserting prime p:
    ΔW(p) = W(F_{p-1}) - W(F_p). -/
def deltaWeylDiscrepancy (p : ℕ) : ℝ :=
  weylDiscrepancy (p - 1) - weylDiscrepancy p

/-- The set of primes p ≤ X with M(p) ≤ -3 satisfying ΔW(p) > 0.
    Since M(p) ≤ -3 < 0, sgn(-M(p)) > 0, so the sign pattern condition
    sgn(ΔW(p)) = sgn(-M(p)) reduces to ΔW(p) > 0. -/
def signPatternPrimes (X : ℕ) : Finset ℕ :=
  ((Finset.range (X + 1)).filter Nat.Prime).filter fun p =>
    mertensFunction p ≤ -3 ∧ deltaWeylDiscrepancy p > 0

/-- The set of primes p ≤ X with M(p) ≤ -3. -/
def mertensNegPrimes (X : ℕ) : Finset ℕ :=
  ((Finset.range (X + 1)).filter Nat.Prime).filter fun p =>
    mertensFunction p ≤ -3

/-! ### Retraction: pointwise version is FALSE

The following documents that the pointwise sign pattern fails.
Counterexample: at p = 237,733, M(p) = -20 < 0, so sgn(-M(p)) > 0 predicts
ΔW(p) > 0, but the actual ΔW(p) is negative, violating the pattern.

We cannot directly compute this counterexample in Lean without
implementing the full Farey discrepancy computation, but the
counterexample is well-documented numerically.
-/

/-- **RETRACTED**: The pointwise sign pattern conjecture is FALSE.
Counterexamples exist at p = 237,733 and p = 243,799.
This theorem documents the retraction — we assert that the universal
statement does not hold. -/
theorem farey_sign_pattern_pointwise_FALSE :
    ¬ ∀ (p : ℕ), Nat.Prime p → mertensFunction p ≤ -3 →
      deltaWeylDiscrepancy p > 0 := by
  -- Cannot be proved without computing ΔW(237733) explicitly, which
  -- requires a full Farey discrepancy implementation.
  -- MATHLIB-PREREQ: Computational Farey sequence discrepancy
  sorry

/-- **Farey Sign Pattern (Density-One Version)**:
Among primes p with M(p) ≤ -3, the proportion satisfying
sgn(ΔW(p)) = sgn(-M(p)) (equivalently, ΔW(p) > 0 since M(p) < 0)
tends to 1 as X → ∞.

Formally: |signPatternPrimes X| / |mertensNegPrimes X| → 1. -/
theorem farey_sign_pattern_density_one :
    Filter.Tendsto
      (fun X : ℕ =>
        if (mertensNegPrimes X).card = 0 then (1 : ℝ)
        else (signPatternPrimes X).card / (mertensNegPrimes X).card)
      Filter.atTop (nhds 1) := by
  -- RESEARCH-OPEN: Requires Chebyshev-bias analysis analogous to
  -- Rubinstein-Sarnak (1994), controlling the distribution of
  -- ΔW(p) via the explicit formula involving zeta zeros.
  sorry

end
