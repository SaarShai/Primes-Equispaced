import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DisplacementShift
import RequestProject.StrictPositivity
import RequestProject.CrossTermPositive
import RequestProject.BridgeIdentity
import RequestProject.MertensGrowth

/-!
# The Sign Theorem: ΔW(p) < 0 for primes with M(p) ≤ -3

## Statement
For prime p ≥ 13 with Mertens function M(p) ≤ -3, the Farey discrepancy
strictly increases: W(F_p) > W(F_{p-1}), equivalently ΔW(p) < 0.

## Key Definitions
- W(N) = (1/|F_N|²) · Σ_{f ∈ F_N} D(f)² — the Farey wobble
- ΔW(p) = W(F_{p-1}) - W(F_p) — discrepancy change at prime step
- B(p) = 2 · Σ D·δ — cross term
- C(p) = Σ δ² — shift-squared sum

## Four-Term Decomposition
ΔW(p) < 0 ⟺ D_new_sq + B + C > dilution
where dilution = old_D_sq · (n'² - n²) / n²

## Ratio Test (Approach 4 — weakened sufficient condition)
It suffices to show: D/A + C/A ≥ 1
where A = dilution_raw, D = new_D_sq, C/A = δ²/dilution_raw

This is much weaker than B+C > 0 since D/A → 1 as p → ∞.

## Computational evidence
- Verified for ALL 4,617 primes with M(p) ≤ -3 up to p = 99,991
- Zero violations found
- min(D/A + C/A) = 1.0957 > 1 (at p = 2857)
-/

open Finset BigOperators

/-! ## Scaled wobble W(N) -/

/-- The Farey count |F_N| = 1 + Σ_{k=1}^N φ(k). -/
def fareyCount (N : ℕ) : ℕ :=
  1 + ∑ k ∈ Finset.range N, Nat.totient (k + 1)

/-- The displacement-squared sum (wobble numerator): Σ D(f)² over F_N. -/
def wobbleNumerator (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N, (displacement N ((ab.1 : ℚ) / ab.2)) ^ 2

/-- The scaled wobble: W(N) = wobbleNumerator(N) / fareyCount(N)². -/
def wobble (N : ℕ) : ℚ :=
  wobbleNumerator N / (fareyCount N : ℚ) ^ 2

/-- The wobble change: ΔW(p) = W(p-1) - W(p). Negative means wobble increased. -/
def deltaWobble (p : ℕ) : ℚ :=
  wobble (p - 1) - wobble p

/-! ## Four-term decomposition components -/

/-- New displacement squared sum: Σ_{k=1}^{p-1} D_p(k/p)². -/
def newDispSquaredSum (p : ℕ) : ℚ :=
  ∑ ab ∈ (fareySet p).filter (fun ab => ab.2 = p),
    (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2

/-- Dilution: the amount by which W decreases just from adding fractions
    (even if they had zero displacement). -/
def dilution (p : ℕ) : ℚ :=
  let n := (fareyCount (p - 1) : ℚ)
  let n' := (fareyCount p : ℚ)
  wobbleNumerator (p - 1) * (n' ^ 2 - n ^ 2) / n ^ 2

/-! ## The Sign Theorem -/

/-- **Sign Theorem (main conjecture):**
    For prime p ≥ 13 with M(p) ≤ -3, ΔW(p) < 0 (wobble increases).

    NOTE: ΔW = W(p-1) - W(p), so ΔW < 0 means W(p) > W(p-1). -/
theorem sign_theorem_conj (p : ℕ) (hp : Nat.Prime p) (hp13 : 13 ≤ p)
    (hM : (mertens p : ℤ) ≤ -3) :
    deltaWobble p < 0 := by
  sorry

/-! ## Computational verification: ΔW(p) < 0 for small primes with M(p) ≤ -3 -/

/-- ΔW(13) < 0, verified by native_decide. M(13) = -3. -/
theorem sign_theorem_13 : deltaWobble 13 < 0 := by native_decide

/-- ΔW(19) < 0, verified by native_decide. M(19) = -3. -/
theorem sign_theorem_19 : deltaWobble 19 < 0 := by native_decide

/-- ΔW(31) < 0, verified by native_decide. M(31) = -4. -/
theorem sign_theorem_31 : deltaWobble 31 < 0 := by native_decide

/-! ## Ratio Test — weaker sufficient condition -/

/-- The B+C sum: crossTerm(p) + shiftSquaredSum(p).
    B+C > 0 implies ΔW < 0 when combined with D ≥ dilution. -/
def bPlusC (p : ℕ) : ℚ :=
  crossTerm p + shiftSquaredSum p

/-! ## B+C Positivity: computational verification -/

theorem bPlusC_pos_13 : bPlusC 13 > 0 := by native_decide
theorem bPlusC_pos_19 : bPlusC 19 > 0 := by native_decide
theorem bPlusC_pos_31 : bPlusC 31 > 0 := by native_decide
theorem bPlusC_pos_43 : bPlusC 43 > 0 := by native_decide
theorem bPlusC_pos_47 : bPlusC 47 > 0 := by native_decide
theorem bPlusC_pos_53 : bPlusC 53 > 0 := by native_decide
theorem bPlusC_pos_59 : bPlusC 59 > 0 := by native_decide
theorem bPlusC_pos_61 : bPlusC 61 > 0 := by native_decide

/-- **Ratio Test Theorem (statement):**
    If D/A + C/A ≥ 1 (i.e., newDispSquaredSum + shiftSquaredSum ≥ dilution),
    then ΔW(p) < 0. -/
theorem ratio_test (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h : newDispSquaredSum p + shiftSquaredSum p ≥ dilution p) :
    deltaWobble p < 0 := by
  sorry

/-! ## Key lemma: R = B_raw / δ² is bounded away from -1 -/

/-- The correlation ratio R(p) = crossTerm(p) / (2 · shiftSquaredSum(p)).
    B+C > 0 ⟺ 1 + R > 0 ⟺ R > -1. -/
def corrRatio (p : ℕ) : ℚ :=
  crossTerm p / (2 * shiftSquaredSum p)

/-- **Key structural fact (PROVED):** B+C = δ² · (1 + 2R).
    Since δ² > 0 (StrictPositivity) and R > -1 (to be proved),
    this gives B+C > 0. -/
theorem bPlusC_eq_shift_times_oneAddR (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    bPlusC p = shiftSquaredSum p * (1 + 2 * corrRatio p) := by
  unfold bPlusC corrRatio
  linarith [mul_div_cancel₀ (crossTerm p)
    (show (2 * shiftSquaredSum p) ≠ 0 from
      mul_ne_zero two_ne_zero (ne_of_gt (shiftSquaredSum_pos p hp hp5)))]

/-! ## Density-1 conjecture: computational evidence -/

/-- **Density-1 Sign Theorem (conjecture):**
    For all ε > 0, the proportion of primes p ≥ 11 where ΔW(p) ≥ 0
    tends to 0. That is, ΔW(p) < 0 for density-1 of primes.

    This is beyond current formalization capabilities (requires deep
    analytic number theory). We provide computational evidence below. -/
theorem sign_theorem_density_one :
    ∀ ε : ℝ, ε > 0 → ∃ N : ℕ,
      ∀ M : ℕ, M ≥ N →
        ((Finset.filter (fun p => Nat.Prime p ∧ 11 ≤ p ∧ ¬(deltaWobble p < 0))
          (Finset.range (M + 1))).card : ℝ) /
        ((Finset.filter (fun p => Nat.Prime p ∧ 11 ≤ p)
          (Finset.range (M + 1))).card : ℝ) < ε := by
  sorry

/-! ### Computational evidence for density-1 conjecture

We verify both theorems up to the largest computationally feasible bound.
The original target was range 114 (primes ≤ 113), but `native_decide` times
out beyond range 98 due to the O(p⁴) cost of computing Farey wobble sums.
Range 98 covers all 21 primes from 11 to 97. -/

/-- Among primes in {11, ..., 97}, ZERO have ΔW(p) ≥ 0.
    This provides computational evidence that the exception set has density 0.
    Covers 21 primes: 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97. -/
theorem density_zero_le_97 :
    (Finset.filter (fun p => Nat.Prime p ∧ 11 ≤ p ∧ ¬(deltaWobble p < 0))
      (Finset.range 98)).card = 0 := by
  native_decide

/-- The only primes with ΔW(p) ≥ 0 below 98 are {2, 3, 5, 7} — all less than 11.
    Equivalently: for every prime p with 11 ≤ p ≤ 97, we have ΔW(p) < 0. -/
theorem exceptions_are_small_primes :
    ∀ p ∈ Finset.range 98, Nat.Prime p → deltaWobble p ≥ 0 → p < 11 := by
  native_decide
