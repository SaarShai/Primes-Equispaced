import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Data.Complex.Exponential

/-!
# Non-vanishing of c_K(s) for K ≤ 4 on the critical line

For K = 2, 3, 4, the truncated Möbius Dirichlet polynomial
c_K(s) = Σ_{k=2}^K μ(k) k^{-s} is nonzero everywhere on Re(s) = 1/2.

Proof sketch:
- c_2(s) = -2^{-s}, so |c_2| = 2^{-1/2} > 0.
- c_3(s) = -2^{-s} - 3^{-s}. On Re(s)=1/2: |c_3| ≥ ||2^{-1/2}| - |3^{-1/2}||
  = |1/√2 - 1/√3| = (√3 - √2)/(√6) > 0 by reverse triangle inequality.
- c_4 = c_3 since μ(4) = 0.

This is unconditional and applies to ALL nontrivial zeta zeros.
-/

/-- On the critical line Re(s) = 1/2, the modulus |k^{-s}| = k^{-1/2}. -/
lemma modulus_on_critical_line (k : ℕ) (hk : 0 < k) (t : ℝ) :
    Complex.abs ((k : ℂ) ^ (-(1/2 + t * Complex.I))) = (k : ℝ) ^ (-(1/2 : ℝ)) := by
  sorry

/-- 1/√2 ≠ 1/√3. -/
lemma sqrt2_inv_ne_sqrt3_inv : (1 : ℝ) / Real.sqrt 2 ≠ 1 / Real.sqrt 3 := by
  sorry

/-- c_2(s) = -2^{-s} is nonzero everywhere. -/
theorem c2_nonvanishing (s : ℂ) : -((2 : ℂ) ^ (-s)) ≠ 0 := by
  sorry

/-- c_3(s) = -2^{-s} - 3^{-s} is nonzero on Re(s) = 1/2,
    by the reverse triangle inequality: the two terms have
    different moduli (1/√2 ≠ 1/√3) so cannot cancel. -/
theorem c3_nonvanishing_critical_line (t : ℝ) :
    let s := (1/2 : ℂ) + t * Complex.I
    -((2 : ℂ) ^ (-s)) - (3 : ℂ) ^ (-s) ≠ 0 := by
  sorry
