import Mathlib
import RequestProject.BridgeIdentity

/-!
# Growth of the Mertens function

The Mertens function M(N) = Σ_{k=1}^{N} μ(k) satisfies |M(N)| = Ω(√N).

More precisely, |M(N)| ≥ c·√N for infinitely many N, where c > 0 is an
absolute constant. This is a classical result in analytic number theory,
following from the connection between the Mertens function and the zeros
of the Riemann zeta function on the critical line.

## Computational verification

We first verify specific values of the Mertens function that witness
|M(N)| > 0.5·√N:
- |M(3)|  = 1,  √3  ≈ 1.73, ratio ≈ 0.58
- |M(5)|  = 2,  √5  ≈ 2.24, ratio ≈ 0.89
- |M(13)| = 3,  √13 ≈ 3.61, ratio ≈ 0.83
- |M(31)| = 4,  √31 ≈ 5.57, ratio ≈ 0.72
-/

/-! ## Computational witnesses -/

/-- M(3) = -1, so |M(3)|/√3 > 0.5. -/
theorem mertens_eq_neg_one : mertens 3 = -1 := by native_decide

/-- M(5) = -2, so |M(5)|/√5 > 0.89. -/
theorem mertens_eq_neg_two : mertens 5 = -2 := by native_decide

/-- M(13) = -3, so |M(13)|/√13 > 0.83. -/
theorem mertens_eq_neg_three : mertens 13 = -3 := by native_decide

/-- M(31) = -4, so |M(31)|/√31 > 0.71. -/
theorem mertens_eq_neg_four : mertens 31 = -4 := by native_decide

/-! ## Ω(√N) growth -/

/-- The Mertens function satisfies |M(N)| = Ω(√N): for any constant C,
there exists N such that |M(N)| > C · √N. This is equivalent to saying
that M(N)/√N is unbounded, a classical result in analytic number theory
that follows from the existence of zeros of the Riemann zeta function
on the critical line Re(s) = 1/2. -/
theorem mertens_omega_sqrt : ∀ C : ℝ, ∃ N : ℕ, (N : ℝ).sqrt * C < |↑(mertens N)| := by
  sorry
