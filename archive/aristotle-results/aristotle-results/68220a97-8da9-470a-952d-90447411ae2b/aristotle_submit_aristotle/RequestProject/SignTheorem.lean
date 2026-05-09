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

/-! ## Per-Denominator Decomposition of R(p)

Decompose R(p) = Σ D·δ / Σ δ² by grouping fractions by denominator b.
For each b in {1,...,p-1} with gcd(b,p)=1, define:
  R_b = (Σ_{a coprime b} D(a/b)·δ(a/b)) / (Σ_{a coprime b} δ(a/b)²)

Then R = Σ_b w_b · R_b where w_b = (Σ_a δ(a/b)²) / (Σ δ²) are positive weights
summing to 1 (for denominators with nonzero shift).

If R_b ≥ -1/2 for all b and R_b > -1/2 for at least one b with w_b > 0,
then R > -1/2 by strict convexity.

### Computational findings

**p = 13:** R_b ≥ -1/2 for ALL denominators b, with equality exactly at b = 5.
  Values: b=1: 0, b=5: -1/2, b=7: 1/10, b=8: 1/2, b=9: 0, b=10: 0, b=11: -1/10.
  Overall R(13) = 813/15872 ≈ 0.051.

**p = 19:** R_b ≥ -1/2 FAILS at b=16 (R₁₆ = -5/6) and b=17 (R₁₇ = -7/12).
  Overall R(19) = 2905619/18867622 ≈ 0.154 (still > -1/2).

**p = 31:** R_b ≥ -1/2 for all b. No violations.

**p = 43:** R_b < -1/2 at b=37 (-277/210), b=40 (-27/22), b=41 (-10/7).

**p = 47:** R_b < -1/2 at b=3 (-3/2), b=9 (-3/2), b=15 (-15/14),
  b=22 (-5/8), b=41 (-9/14), b=43 (-37/22), b=45 (-3).

**Conclusion:** The per-denominator bound R_b > -1/2 does NOT hold in general.
Large denominators b (close to p) can have very negative R_b values.
However, these denominators have small shift-squared weights, so the overall
weighted average R still exceeds -1/2. A proof would need to bound the
weighted sum rather than each term individually.
-/

/-- Per-denominator cross term: Σ_{a coprime b} D_{p-1}(a/b) · δ_p(a/b). -/
def crossTermDenom (p b : ℕ) : ℚ :=
  ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.2 = b),
    displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)

/-- Per-denominator shift-squared sum: Σ_{a coprime b} δ_p(a/b)². -/
def shiftSquaredDenom (p b : ℕ) : ℚ :=
  ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.2 = b),
    (shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2

/-- Per-denominator correlation ratio: R_b = crossTermDenom / shiftSquaredDenom. -/
def corrRatioDenom (p b : ℕ) : ℚ :=
  crossTermDenom p b / shiftSquaredDenom p b

/-! ### Computational verification for p = 13 -/

/-- For p = 13: R_b ≥ -1/2 for all denominators b with nonzero shift. -/
theorem corrRatioDenom_ge_neg_half_13 :
    ∀ b ∈ Finset.range 13,
      shiftSquaredDenom 13 (b + 1) > 0 →
        corrRatioDenom 13 (b + 1) ≥ -1 / 2 := by native_decide

/-- For p = 13, b = 5: R_5 = -1/2 exactly (boundary case). -/
theorem corrRatioDenom_13_5 : corrRatioDenom 13 5 = -1 / 2 := by native_decide

/-- For p = 13, b = 7: R_7 > -1/2 (strict). -/
theorem corrRatioDenom_13_7_strict : corrRatioDenom 13 7 > -1 / 2 := by native_decide

/-- Overall R(13) > -1/2, as the per-denominator approach predicts. -/
theorem corrRatio_13_gt_neg_half : corrRatio 13 > -1 / 2 := by native_decide

/-! ### Counterexample: per-denominator bound fails at p = 19 -/

/-- For p = 19, b = 16: R₁₆ = -5/6 < -1/2 (per-denominator bound fails). -/
theorem corrRatioDenom_19_16_violation :
    corrRatioDenom 19 16 < -1 / 2 := by native_decide

/-- For p = 19, b = 17: R₁₇ = -7/12 < -1/2 (per-denominator bound fails). -/
theorem corrRatioDenom_19_17_violation :
    corrRatioDenom 19 17 < -1 / 2 := by native_decide

/-- Despite per-denominator violations, overall R(19) > -1/2 still holds. -/
theorem corrRatio_19_gt_neg_half : corrRatio 19 > -1 / 2 := by native_decide
