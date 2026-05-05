import Mathlib

/-!
# Cage Half-Width Algebra (Theorem B / Sequel-1)

The Milinovich–Ng (2014) cage for the M-N statistic `u_f` has edges
  `c± = (17 ± √145) / (12π)`.

This file formalizes the **purely algebraic** content:
1. The discriminant identity `17² − 4·36 = 145` (rational, `norm_num`).
2. `c±` are real numbers and `(c⁺ − c⁻)/2 = √145 / (12π)` (cage half-width).
3. `c⁺ · c⁻ · (12π)² = 144`, equivalently the rationalized product identity.

No analytic machinery: only `Real.sqrt`, `Real.pi_ne_zero`, basic field/ring.
-/

namespace CageHalfWidth

open Real

/-! ## Pure ℚ discriminant. -/

/-- Discriminant of the cage quadratic `Y² − 17·Y + 36`: `17² − 4·36 = 145`. -/
theorem cage_discriminant : (17 : ℚ)^2 - 4 * 36 = 145 := by norm_num

/-- Equivalent rationalized form: `(17 + √145)·(17 − √145) = 17² − 145 = 144`. -/
theorem cage_root_product_rat : (17 : ℚ)^2 - 145 = 144 := by norm_num

/-! ## Real algebra: cage edges and half-width. -/

/-- `(√145)^2 = 145`. -/
lemma sqrt_145_sq : Real.sqrt 145 ^ 2 = 145 := by
  rw [sq_sqrt]; norm_num

/-- `√145 * √145 = 145` (multiplicative form, more useful for `nlinarith`). -/
lemma sqrt_145_mul_self : Real.sqrt 145 * Real.sqrt 145 = 145 := by
  rw [← sq]; exact sqrt_145_sq

/-- The cage edges in original coordinates `c± = (17 ± √145)/(12π)`. -/
noncomputable def cPlus : ℝ := (17 + Real.sqrt 145) / (12 * Real.pi)

/-- The cage edges in original coordinates `c± = (17 ± √145)/(12π)`. -/
noncomputable def cMinus : ℝ := (17 - Real.sqrt 145) / (12 * Real.pi)

/-- Cage center: `(c⁺ + c⁻)/2 = 17/(12π)`. -/
theorem c_center : (cPlus + cMinus) / 2 = 17 / (12 * Real.pi) := by
  unfold cPlus cMinus
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

/-- **Cage half-width.** `(c⁺ − c⁻)/2 = √145 / (12π)`. -/
theorem cage_half_width :
    (cPlus - cMinus) / 2 = Real.sqrt 145 / (12 * Real.pi) := by
  unfold cPlus cMinus
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

/-- The half-width is positive. -/
theorem cage_half_width_pos : 0 < Real.sqrt 145 / (12 * Real.pi) := by
  apply div_pos
  · exact Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 145)
  · positivity

/-- Product identity: `c⁺ · c⁻ · (12π)² = 144`. The `(12π)²` factor lets us
    keep this in the form of a polynomial identity (no division by `π`). -/
theorem c_product_rationalized :
    cPlus * cMinus * (12 * Real.pi) ^ 2 = 144 := by
  unfold cPlus cMinus
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hsq : Real.sqrt 145 * Real.sqrt 145 = 145 := sqrt_145_mul_self
  have hne : (12 * Real.pi) ≠ 0 := by positivity
  field_simp
  -- Goal: (17 + √145) * (17 - √145) * (12π)² = 144 * (12π)²    (after field_simp)
  -- (17 + √145)(17 - √145) = 289 - 145 = 144.
  nlinarith [hsq, sq_nonneg (Real.pi)]

/-- The "Y-form" cage edges (without the `1/(12π)` factor) are roots of
    `Y² − 34·Y + 144 = 0` (note: 34 = 2·17, since the un-halved roots have
    sum `34`). Equivalently, the half-shifted roots `(17 ± √145)/2` are
    roots of `Z² − 17·Z + 36 = 0`. We state the un-halved version, which
    matches the discriminant `cage_discriminant` after halving. -/
theorem Yplus_root :
    (17 + Real.sqrt 145) ^ 2 - 34 * (17 + Real.sqrt 145) + 144 = 0 := by
  have hsq : Real.sqrt 145 * Real.sqrt 145 = 145 := sqrt_145_mul_self
  nlinarith [hsq]

theorem Yminus_root :
    (17 - Real.sqrt 145) ^ 2 - 34 * (17 - Real.sqrt 145) + 144 = 0 := by
  have hsq : Real.sqrt 145 * Real.sqrt 145 = 145 := sqrt_145_mul_self
  nlinarith [hsq]

end CageHalfWidth
