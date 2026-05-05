import Mathlib
import CageHalfWidth

/-!
# Cage rescaled algebra

Extends `CageHalfWidth.lean` with explicit root statements for the
quadratic `x² − 34 x + 144 = 0`, which has roots `Y± = 17 ± √145`.

Together with the `(12π)`-rescaling these give the cage edges
`c± = (17 ± √145)/(12 π)`.

Also provides the Vieta-form identities:
- `Y+ + Y−  = 34`
- `Y+ · Y−  = 144`
- discriminant `34² − 4 · 144 = 580 = 4 · 145` (so `√disc = 2 √145`).

Pure algebra; no analytic machinery beyond `Real.sqrt`.
-/

namespace CageRescaledAlgebra

open Real CageHalfWidth

/-! ## 1. The un-halved roots `Y± = 17 ± √145`. -/

noncomputable def Yplus  : ℝ := 17 + Real.sqrt 145
noncomputable def Yminus : ℝ := 17 - Real.sqrt 145

/-- Vieta sum: `Y+ + Y− = 34`. -/
theorem Y_sum : Yplus + Yminus = 34 := by
  unfold Yplus Yminus; ring

/-- Vieta product: `Y+ · Y− = 144`. -/
theorem Y_product : Yplus * Yminus = 144 := by
  unfold Yplus Yminus
  have hsq : Real.sqrt 145 * Real.sqrt 145 = 145 := sqrt_145_mul_self
  nlinarith [hsq]

/-- `Y+` is a root of `x² − 34 x + 144`. -/
theorem Yplus_root_quadratic :
    Yplus ^ 2 - 34 * Yplus + 144 = 0 := by
  unfold Yplus
  have hsq : Real.sqrt 145 * Real.sqrt 145 = 145 := sqrt_145_mul_self
  nlinarith [hsq]

/-- `Y−` is a root of `x² − 34 x + 144`. -/
theorem Yminus_root_quadratic :
    Yminus ^ 2 - 34 * Yminus + 144 = 0 := by
  unfold Yminus
  have hsq : Real.sqrt 145 * Real.sqrt 145 = 145 := sqrt_145_mul_self
  nlinarith [hsq]

/-- Discriminant of `x² − 34 x + 144`: `34² − 4·144 = 580`. -/
theorem disc_34_144 : (34 : ℚ) ^ 2 - 4 * 144 = 580 := by norm_num

/-- And `580 = 4 · 145`. -/
theorem disc_eq_four_145 : (580 : ℚ) = 4 * 145 := by norm_num

/-- So the *square root* of the discriminant is `2 √145`. -/
theorem sqrt_disc_eq_two_sqrt_145 :
    Real.sqrt 580 = 2 * Real.sqrt 145 := by
  rw [show (580 : ℝ) = 4 * 145 by norm_num,
      show (4 : ℝ) = 2 ^ 2 by norm_num]
  rw [Real.sqrt_mul (by positivity), Real.sqrt_sq (by norm_num : (2:ℝ) ≥ 0)]

/-! ## 2. The (12π) rescaling. -/

/-- The cage edges, in `(12π)` rescaled form. -/
noncomputable def cPlus  : ℝ := Yplus  / (12 * Real.pi)
noncomputable def cMinus : ℝ := Yminus / (12 * Real.pi)

/-- The rescaled-cage edges agree with `CageHalfWidth.cPlus` / `cMinus`. -/
theorem cPlus_eq : cPlus = CageHalfWidth.cPlus := by
  unfold cPlus Yplus CageHalfWidth.cPlus
  rfl

theorem cMinus_eq : cMinus = CageHalfWidth.cMinus := by
  unfold cMinus Yminus CageHalfWidth.cMinus
  rfl

/-- Center of the rescaled cage: `(c+ + c−)/2 = 17/(12π)`. -/
theorem c_center :
    (cPlus + cMinus) / 2 = 17 / (12 * Real.pi) := by
  unfold cPlus cMinus Yplus Yminus
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

/-- Half-width of the rescaled cage: `(c+ − c−)/2 = √145/(12π)`. -/
theorem c_half_width :
    (cPlus - cMinus) / 2 = Real.sqrt 145 / (12 * Real.pi) := by
  unfold cPlus cMinus Yplus Yminus
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

/-- Product (after rationalisation): `c+ · c− · (12π)² = 144`. -/
theorem c_product_rationalized :
    cPlus * cMinus * (12 * Real.pi) ^ 2 = 144 := by
  unfold cPlus cMinus
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hsq : Real.sqrt 145 * Real.sqrt 145 = 145 := sqrt_145_mul_self
  have hY : Yplus * Yminus = 144 := Y_product
  field_simp
  nlinarith [hY, sq_nonneg Real.pi]

/-- The rescaled cage half-width is positive. -/
theorem c_half_width_pos : 0 < Real.sqrt 145 / (12 * Real.pi) :=
  CageHalfWidth.cage_half_width_pos

end CageRescaledAlgebra
