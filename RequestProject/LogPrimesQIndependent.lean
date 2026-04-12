import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Rat.Basic

/-!
# Q-linear independence of logarithms of distinct primes

Key lemma for the Turán non-vanishing theorem (Theorem A2 in Paper C).
If Σ qⱼ · log pⱼ = 0 for rationals qⱼ and distinct primes pⱼ,
then all qⱼ = 0.

This follows from the Fundamental Theorem of Arithmetic:
if Σ qⱼ log pⱼ = 0, clearing denominators gives Σ mⱼ log pⱼ = 0
with integers mⱼ, hence Π pⱼ^mⱼ = 1, hence mⱼ = 0 for all j
by unique prime factorization.
-/

/-- The logarithms of distinct primes are Q-linearly independent. -/
theorem log_primes_Q_independent
    (ps : List ℕ) (qs : List ℚ)
    (hprimes : ∀ p ∈ ps, Nat.Prime p)
    (hnodup : ps.Nodup)
    (hlen : ps.length = qs.length)
    (hsum : (List.zipWith (fun p q => q * Real.log (p : ℝ)) ps qs).sum = 0) :
    ∀ q ∈ qs, q = 0 := by
  sorry
