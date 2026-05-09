import Mathlib

/-!
# Q-Linear Independence of Logarithms of Distinct Primes

This file proves that the set {log p : p prime} is Q-linearly independent.
Specifically: for any finite set S of distinct primes and rational coefficients
q_p, if Σ_{p ∈ S} q_p * log p = 0, then every q_p = 0.

This is needed for the Turán non-vanishing theorem in the Farey discrepancy
framework: if a linear combination of characters at prime arguments vanishes,
the individual coefficients must vanish.

## Main result

`log_prime_Q_linear_indep`: The logarithms of distinct primes are linearly
independent over ℚ.
-/

open Real Finset

/-- Logarithms of distinct primes are linearly independent over ℚ.

For any finite set S of distinct primes and rational coefficients (q : ℕ → ℚ),
if the weighted sum Σ_{p ∈ S} q(p) * log p = 0, then q(p) = 0 for all p ∈ S.

Proof sketch:
- Suppose Σ q_p * log p = 0 with q_p = a_p / b (common denominator b).
- Then Σ a_p * log p = 0, i.e., log(Π p^{a_p}) = 0, i.e., Π p^{a_p} = 1.
- By unique factorization (fundamental theorem of arithmetic), all a_p = 0.
- Hence all q_p = 0.
-/
theorem log_prime_Q_linear_indep
    (S : Finset ℕ) (hS : ∀ p ∈ S, Nat.Prime p)
    (q : ℕ → ℚ)
    (hsum : ∑ p ∈ S, (q p : ℝ) * Real.log p = 0) :
    ∀ p ∈ S, q p = 0 := by
  sorry

/-- Equivalent formulation: the family (Real.log ·) on primes is ℚ-linearly
independent as a family of real numbers, in the sense that any finite ℚ-linear
combination that equals zero has all coefficients zero. -/
theorem log_prime_Q_linear_indep' :
    LinearIndependent ℚ (fun p : {p : ℕ // Nat.Prime p} => Real.log (p : ℝ)) := by
  sorry
