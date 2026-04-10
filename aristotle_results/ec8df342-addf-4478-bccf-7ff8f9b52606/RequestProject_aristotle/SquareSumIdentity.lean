import Mathlib

theorem square_sum_identity (x d : ℚ) :
    x * d - d ^ 2 / 2 = (x ^ 2 - (x - d) ^ 2) / 2 := by
  ring
