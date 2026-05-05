import Mathlib

/-!
# Reverse-engineering of the M-N constant 2/(3π)

The Milinovich-Ng (2014) leading constant for the GL(2) weight-aspect
4-derivative average is `2/(3π)`.  Cross-referenced to the CFKRS recipe
and the GUE/Barnes-G arithmetic, this constant decomposes as

  `2/(3π) = (1/(2π)) · (1/12) · 16`

where:
- `1/(2π)`  is the standard zero-density factor (RvM 2π denominator),
- `1/12 = G(3)² / G(5)`  is the Barnes-G factor for k=2 (Hughes thesis,
  Mezzadri 2003),
- `16 = 2^4`  is the conductor-shift derivative factor for degree-2
  L-functions (CFKRS, see `CFKRSFactorSixteen.lean` and
  `CFKRS_symbolic_verification.md`).

The identity is a pure rational algebraic statement once `π` is treated
as a unit.  This file machine-verifies it. -/

namespace ReverseEngineerDecomp

open Real

/-! ## 1. Pure ℚ identity (factoring out `π`). -/

/-- The rational fingerprint: `2/3 = (1/2) · (1/12) · 16`. -/
theorem mn_constant_rational :
    (2 : ℚ) / 3 = (1 / 2) * (1 / 12) * 16 := by norm_num

/-- Equivalently: `(1/2) · (1/12) · 16 = 16 / 24 = 2/3`. -/
theorem mn_factor_check : (1 / 2 : ℚ) * (1 / 12) * 16 = 16 / 24 := by norm_num

/-- And `16/24 = 2/3` as rationals. -/
theorem mn_sixteen_24 : (16 : ℚ) / 24 = 2 / 3 := by norm_num

/-! ## 2. Real form (with the `π` denominator restored). -/

/-- The reverse-engineering identity over ℝ:
      `2 / (3 π)  =  (1 / (2 π)) · (1 / 12) · 16`. -/
theorem mn_constant_decomposition :
    2 / (3 * Real.pi) = (1 / (2 * Real.pi)) * (1 / 12) * 16 := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

/-- Symbolic factor labels: `RvM = 1/(2π)`, `Barnes = 1/12`, `Conductor = 16`. -/
noncomputable def rvmFactor : ℝ := 1 / (2 * Real.pi)

noncomputable def barnesFactor : ℝ := 1 / 12

noncomputable def conductorFactor : ℝ := 16

/-- The MN constant as a labelled product of the three structural pieces. -/
theorem mn_constant_named :
    rvmFactor * barnesFactor * conductorFactor = 2 / (3 * Real.pi) := by
  unfold rvmFactor barnesFactor conductorFactor
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

/-- Each labelled factor is positive. -/
theorem rvmFactor_pos : 0 < rvmFactor := by
  unfold rvmFactor
  apply div_pos one_pos
  positivity

theorem barnesFactor_pos : 0 < barnesFactor := by
  unfold barnesFactor; norm_num

theorem conductorFactor_pos : 0 < conductorFactor := by
  unfold conductorFactor; norm_num

/-- Therefore the M-N constant `2/(3π)` is positive. -/
theorem mn_constant_pos : 0 < 2 / (3 * Real.pi) := by
  rw [← mn_constant_named]
  exact mul_pos (mul_pos rvmFactor_pos barnesFactor_pos) conductorFactor_pos

end ReverseEngineerDecomp
