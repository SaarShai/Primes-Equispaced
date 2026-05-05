import Mathlib

/-!
# CFKRS factor-16 algebraic identity

For the GL(2) modular form L-function the conductor is `q · t²`, so
`log𝔮 = log q + 2 log t`.  CFKRS recipe pulls down four shift-derivatives,
yielding a leading factor `(log q + 2 log t)^4`.  Comparing to the GL(1)
zeta baseline (which yields `log^4 t`) the ratio limits to `2^4 = 16` as
`t → ∞`.

This file formalises the **purely algebraic** content (the symbolic
expansion verified in `CFKRS_symbolic_verification.md`):

1. The expansion identity
   `(Q + 2 L)^4 = 16 L^4 + 32 L^3 Q + 24 L^2 Q^2 + 8 L Q^3 + Q^4`,
   over any commutative ring.
2. The polynomial-in-`Q/L` expression for the ratio
   `(Q + 2 L)^4 / L^4`, valid for `L ≠ 0`.
3. The asymptotic limit `(Q + 2 L)^4 / L^4 → 16` as `L → ∞`.
-/

namespace CFKRSFactorSixteen

open Real Filter Topology

/-! ## 1. Algebraic expansion of `(Q + 2 L)^4`. -/

/-- Symbolic expansion of `(Q + 2 L)^4`, verbatim from
    `CFKRS_symbolic_verification.md` (sympy `expand`). -/
theorem cfkrs_quartic_expansion (Q L : ℝ) :
    (Q + 2 * L) ^ 4 =
      16 * L ^ 4 + 32 * L ^ 3 * Q + 24 * L ^ 2 * Q ^ 2 +
        8 * L * Q ^ 3 + Q ^ 4 := by
  ring

/-- Pure rational fingerprint: `2^4 = 16`. -/
theorem two_pow_four_eq_sixteen : (2 : ℚ) ^ 4 = 16 := by norm_num

/-- Equivalent integer form: `2^4 = 16` over ℤ. -/
theorem two_pow_four_eq_sixteen_int : (2 : ℤ) ^ 4 = 16 := by norm_num

/-! ## 2. Polynomial ratio. -/

/-- The polynomial-in-`Q/L` form of the ratio:
    `(Q + 2 L)^4 / L^4 = 16 + 32 (Q/L) + 24 (Q/L)^2 + 8 (Q/L)^3 + (Q/L)^4`. -/
theorem cfkrs_ratio_polynomial (Q L : ℝ) (hL : L ≠ 0) :
    (Q + 2 * L) ^ 4 / L ^ 4 =
      16 + 32 * (Q / L) + 24 * (Q / L) ^ 2 +
        8 * (Q / L) ^ 3 + (Q / L) ^ 4 := by
  have hL4 : L ^ 4 ≠ 0 := pow_ne_zero 4 hL
  field_simp
  ring

/-- Subtracting 16 leaves only lower-order terms in `Q/L`. -/
theorem cfkrs_ratio_minus_sixteen (Q L : ℝ) (hL : L ≠ 0) :
    (Q + 2 * L) ^ 4 / L ^ 4 - 16 =
      32 * (Q / L) + 24 * (Q / L) ^ 2 +
        8 * (Q / L) ^ 3 + (Q / L) ^ 4 := by
  rw [cfkrs_ratio_polynomial Q L hL]
  ring

/-! ## 3. Asymptotic limit `(Q + 2 L)^4 / L^4 → 16` as `L → ∞`. -/

/-- `Q / L → 0` as `L → ∞` (real version). -/
lemma tendsto_div_atTop (Q : ℝ) :
    Tendsto (fun L : ℝ => Q / L) atTop (𝓝 0) := by
  -- `Q / L = Q * L⁻¹`. Use `Tendsto.const_mul` on `L⁻¹ → 0`.
  have hinv : Tendsto (fun L : ℝ => L⁻¹) atTop (𝓝 0) :=
    tendsto_inv_atTop_zero
  have h := hinv.const_mul Q
  simpa [div_eq_mul_inv, mul_zero] using h

/-- The asymptotic limit: as `L → ∞`, `(Q + 2 L)^4 / L^4 → 16`. -/
theorem cfkrs_ratio_tendsto_sixteen (Q : ℝ) :
    Tendsto (fun L : ℝ => (Q + 2 * L) ^ 4 / L ^ 4) atTop (𝓝 16) := by
  have hQL : Tendsto (fun L : ℝ => Q / L) atTop (𝓝 0) := tendsto_div_atTop Q
  -- Build the limit of the polynomial expression.
  have h0 : Tendsto (fun _ : ℝ => (16 : ℝ)) atTop (𝓝 16) := tendsto_const_nhds
  have h1 : Tendsto (fun L : ℝ => 32 * (Q / L)) atTop (𝓝 0) := by
    have := hQL.const_mul (32 : ℝ); simpa using this
  have h2 : Tendsto (fun L : ℝ => 24 * (Q / L) ^ 2) atTop (𝓝 0) := by
    have hp : Tendsto (fun L : ℝ => (Q / L) ^ 2) atTop (𝓝 0) := by
      have := hQL.pow 2; simpa using this
    have := hp.const_mul (24 : ℝ); simpa using this
  have h3 : Tendsto (fun L : ℝ => 8 * (Q / L) ^ 3) atTop (𝓝 0) := by
    have hp : Tendsto (fun L : ℝ => (Q / L) ^ 3) atTop (𝓝 0) := by
      have := hQL.pow 3; simpa using this
    have := hp.const_mul (8 : ℝ); simpa using this
  have h4 : Tendsto (fun L : ℝ => (Q / L) ^ 4) atTop (𝓝 0) := by
    have := hQL.pow 4; simpa using this
  have hsum : Tendsto
      (fun L : ℝ => 16 + 32 * (Q / L) + 24 * (Q / L) ^ 2 +
        8 * (Q / L) ^ 3 + (Q / L) ^ 4) atTop (𝓝 16) := by
    have step :=
      ((((h0.add h1).add h2).add h3).add h4)
    simpa using step
  -- Identify with the original function on `L > 0`.
  refine hsum.congr' ?_
  filter_upwards [eventually_gt_atTop (0 : ℝ)] with L hL
  have hLne : L ≠ 0 := ne_of_gt hL
  exact (cfkrs_ratio_polynomial Q L hLne).symm

end CFKRSFactorSixteen
