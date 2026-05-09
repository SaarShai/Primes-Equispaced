import Mathlib

/-!
# Farey Gap Upper Bound

For consecutive Farey neighbours a/b, c/d of order N (with bc − ad = 1,
b ≤ N, d ≤ N, and b + d > N), the gap satisfies c/d − a/b ≤ 1/N.

## Proof strategy

1. By the Farey gap formula: c/d − a/b = 1/(bd) (since bc − ad = 1).
2. We need 1/(bd) ≤ 1/N, i.e., N ≤ bd.
3. Since b, d ≥ 1: (b−1)(d−1) ≥ 0, so bd ≥ b + d − 1.
4. Since b + d > N: bd ≥ b + d − 1 ≥ N.
5. Therefore 1/(bd) ≤ 1/N.
-/

open scoped Classical

/-- **Farey gap formula.** If bc − ad = 1, then c/d − a/b = 1/(bd). -/
theorem farey_gap_formula (a b c d : ℤ)
    (hb : 0 < b) (hd : 0 < d)
    (hdet : b * c - a * d = 1) :
    (c : ℚ) / d - a / b = 1 / (b * d) := by
  have hb' : (b : ℚ) ≠ 0 := Int.cast_ne_zero.mpr (ne_of_gt hb)
  have hd' : (d : ℚ) ≠ 0 := Int.cast_ne_zero.mpr (ne_of_gt hd)
  rw [div_sub_div _ _ hd' hb', div_eq_div_iff (mul_ne_zero hd' hb') (mul_ne_zero hb' hd')]
  have : (b : ℚ) * c - a * d = 1 := by exact_mod_cast hdet
  linear_combination (↑d * ↑b : ℚ) * this

/-
PROBLEM
**Farey gap upper bound (with b + d > N).** For consecutive Farey neighbours
    of order N (where b + d > N, b ≤ N, d ≤ N), the gap c/d − a/b ≤ 1/N.

PROVIDED SOLUTION
Use farey_gap_formula to get gap = 1/(bd). We need 1/(bd) ≤ 1/N, i.e., N ≤ bd.
Since b, d ≥ 1: (b-1)(d-1) ≥ 0 gives bd ≥ b + d - 1. And b + d > N gives
b + d - 1 ≥ N, so bd ≥ N. Therefore 1/(bd) ≤ 1/N.

In Lean: rewrite via farey_gap_formula, then use div_le_div and nlinarith
with the key inequalities. Alternatively, clear denominators in ℚ and use
norm_cast + nlinarith on the integer inequality N ≤ b * d.
-/
theorem farey_gap_upper_bound_corrected (a b c d N : ℤ)
    (hb : 0 < b) (hd : 0 < d) (hN : 0 < N)
    (hbN : b ≤ N) (hdN : d ≤ N)
    (hsum : N < b + d)
    (hdet : b * c - a * d = 1) :
    (c : ℚ) / d - a / b ≤ 1 / N := by
  sorry
