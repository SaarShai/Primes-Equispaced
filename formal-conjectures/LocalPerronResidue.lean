-- File 1: LocalPerronResidue.lean
import Mathlib

namespace LocalPerronResidue

open Complex

/-- Local Perron double-pole residue at a simple zero.
For analytic L near 0 with L(0) = 0 and L'(0) ≠ 0, the residue at w = 0 of
K^w / (w · L(w)) equals log K / L'(0) - L''(0) / (2 · L'(0)^2). -/
theorem local_perron_residue
    (K : ℝ) (hK : (1 : ℝ) < K)
    (L : ℂ → ℂ) (hL : AnalyticAt ℂ L 0)
    (hL0 : L 0 = 0) (hL'0 : deriv L 0 ≠ 0) :
    -- MATHLIB-PREREQ: `Residue.residue` for meromorphic functions
    -- MATHLIB-PREREQ: `AnalyticAt.hasFPowerSeriesAt` for Laurent expansion
    -- MATHLIB-PREREQ: `deriv_iterate` or `iteratedDeriv` for higher derivatives
    residue (fun w => (↑K : ℂ) ^ w / (w * L w)) 0 =
      (↑(Real.log K) / deriv L 0 - deriv (deriv L) 0 / (2 * (deriv L 0) ^ 2) : ℂ) := by
  sorry

end LocalPerronResidue
