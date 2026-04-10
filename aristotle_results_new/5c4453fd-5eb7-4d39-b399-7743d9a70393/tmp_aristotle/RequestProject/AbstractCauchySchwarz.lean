import Mathlib

open Finset BigOperators

/-!
# Abstract Cauchy-Schwarz Bound

If Σ_{i ∈ s} a_i = -|s|/2 then Σ_{i ∈ s} a_i² ≥ |s|/4.

This is the abstract form of the wobble numerator lower bound.
-/

/-- If the sum of values over a finite set equals -n/2,
    then the sum of squares is at least n/4.
    Follows from Cauchy-Schwarz: (Σ a_i)² ≤ |s| · Σ a_i². -/
theorem sum_sq_ge_quarter_of_sum_eq_neg_half
    {ι : Type*} [DecidableEq ι] (s : Finset ι) (a : ι → ℚ)
    (hs : 0 < s.card)
    (hsum : ∑ i ∈ s, a i = -((s.card : ℚ)) / 2) :
    ∑ i ∈ s, (a i) ^ 2 ≥ ((s.card : ℚ)) / 4 := by
  have cauchy_schwarz : (∑ i ∈ s, a i)^2 ≤ (s.card : ℚ) * ∑ i ∈ s, (a i)^2 :=
    sq_sum_le_card_mul_sum_sq
  nlinarith [(by norm_cast : (1 : ℚ) ≤ s.card)]
