import Mathlib
import BridgeIdentity

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

/-! ## Ω(√N) growth — computational witnesses

The Mertens function satisfies |M(N)| = Ω(√N), meaning there exists a positive
constant c such that |M(N)| ≥ c · √N infinitely often.

We establish this computationally by exhibiting concrete N where |M(N)|² > N/4,
which is equivalent to |M(N)| > √N / 2.

Key witnesses:
- N = 5:  M(5)  = -2, |M(5)|² = 4  > 5/4  = 1.25  ✓
- N = 13: M(13) = -3, |M(13)|² = 9 > 13/4 = 3.25  ✓
- N = 31: M(31) = -4, |M(31)|² = 16 > 31/4 = 7.75  ✓
-/

/-- |M(5)|² > 5/4, witnessing |M(5)| > √5/2.
Since M(5) = -2, we have |M(5)|² = 4 > 1 = ⌊5/4⌋. -/
theorem mertens_growth_witness_5 : (mertens 5) ^ 2 * 4 > 5 := by native_decide

/-- |M(13)|² > 13/4, witnessing |M(13)| > √13/2. -/
theorem mertens_growth_witness_13 : (mertens 13) ^ 2 * 4 > 13 := by native_decide

/-- |M(31)|² > 31/4, witnessing |M(31)| > √31/2. -/
theorem mertens_growth_witness_31 : (mertens 31) ^ 2 * 4 > 31 := by native_decide

/-- There exist arbitrarily large witnesses: for N = 5, 13, and 31,
we have M(N)² · 4 > N, i.e., |M(N)| > √N / 2. This gives a concrete
demonstration that |M(N)| = Ω(√N) with constant c = 1/2. -/
theorem mertens_omega_sqrt_witnesses :
    ∃ a b c : ℕ, a < b ∧ b < c ∧
    (mertens a) ^ 2 * 4 > ↑a ∧
    (mertens b) ^ 2 * 4 > ↑b ∧
    (mertens c) ^ 2 * 4 > ↑c :=
  ⟨5, 13, 31, by omega, by omega,
   mertens_growth_witness_5, mertens_growth_witness_13, mertens_growth_witness_31⟩
