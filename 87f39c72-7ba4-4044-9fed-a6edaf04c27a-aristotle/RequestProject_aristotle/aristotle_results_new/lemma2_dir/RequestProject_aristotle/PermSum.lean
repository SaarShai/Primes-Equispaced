import Mathlib

open Finset BigOperators

theorem perm_preserves_sum_of_sq (s : Finset ℕ) (sigma : Equiv.Perm ℕ)
    (hs : ∀ x ∈ s, sigma x ∈ s) (f : ℕ → ℚ) :
    ∑ x ∈ s, f x = ∑ x ∈ s, f (sigma x) := by
  have h_bij : s.image sigma = s :=
    Finset.eq_of_subset_of_card_le (Finset.image_subset_iff.mpr hs)
      (by rw [Finset.card_image_of_injective _ sigma.injective])
  conv_lhs => rw [← h_bij, Finset.sum_image (by simp +decide)]
