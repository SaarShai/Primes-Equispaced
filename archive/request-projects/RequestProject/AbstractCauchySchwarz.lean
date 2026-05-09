import Mathlib

open Finset BigOperators

/-!
# Abstract Cauchy-Schwarz Bound

If Σ_{i ∈ s} a_i = -|s|/2 then Σ_{i ∈ s} a_i² ≥ |s|/4.

This is the abstract form of the wobble numerator lower bound.
-/

/-
PROBLEM
If the sum of values over a finite set equals -n/2,
    then the sum of squares is at least n/4.
    Follows from Cauchy-Schwarz: (Σ a_i)² ≤ |s| · Σ a_i².

PROVIDED SOLUTION
By Cauchy-Schwarz inequality: (Σ a_i)² ≤ |s| · Σ a_i². We have Σ a_i = -|s|/2, so (|s|/2)² = |s|²/4 ≤ |s| · Σ a_i². Dividing by |s| (which is positive): Σ a_i² ≥ |s|/4. In Lean, use Finset.inner_mul_le_norm_mul_sq or derive it directly: have (Σ a_i)² ≤ |s| · Σ a_i² from the Cauchy-Schwarz inequality for finite sums (each with weight 1). Then substitute hsum and simplify.
-/
theorem sum_sq_ge_quarter_of_sum_eq_neg_half
    {ι : Type*} [DecidableEq ι] (s : Finset ι) (a : ι → ℚ)
    (hs : 0 < s.card)
    (hsum : ∑ i ∈ s, a i = -((s.card : ℚ)) / 2) :
    ∑ i ∈ s, (a i) ^ 2 ≥ ((s.card : ℚ)) / 4 := by
  have := Finset.sum_nonneg fun i ( hi : i ∈ s ) ↦ sq_nonneg ( a i - -1 / 2 );
  simp_all +decide [ add_sq, Finset.sum_add_distrib, sub_sq ];
  norm_num [ ← Finset.mul_sum _ _ _, ← Finset.sum_mul, hsum ] at this; linarith;