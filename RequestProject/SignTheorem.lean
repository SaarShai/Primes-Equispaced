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

    NOTE: ΔW = W(p-1) - W(p), so ΔW < 0 means W(p) > W(p-1).

    **WARNING: This theorem is known to be FALSE in general.**
    A counterexample exists at p = 243799 (and potentially other large primes).
    The statement ΔW(p) < 0 for all primes with M(p) ≤ -3 is not universally true.
    The sorry below is intentional and cannot be replaced with a valid proof.
    The bounded-range version `sign_theorem_conj_bounded` (for p < 114) IS valid
    and verified by native_decide. -/
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

/- **Original Ratio Test Theorem (INCORRECT — commented out):**
    The original statement claimed that newDispSquaredSum + shiftSquaredSum ≥ dilution
    implies deltaWobble < 0. This is FALSE.

    **Counterexample: p = 7.**
    - Nat.Prime 7 and 5 ≤ 7: ✓
    - newDispSquaredSum 7 + shiftSquaredSum 7 ≥ dilution 7: ✓ (verified by native_decide)
    - deltaWobble 7 < 0: ✗ (deltaWobble 7 ≥ 0, verified by native_decide)

    The error is that the original statement omits the crossTerm B(p) and the
    boundary correction of -1 (from f = 1, where D_p(1) = D_{p-1}(1) + δ(1) - 1).

    The correct four-term decomposition gives:
      W'(p) - W(p-1) = crossTerm(p) + shiftSquaredSum(p) - 1 + newDispSquaredSum(p)
    And deltaWobble(p) < 0 ⟺ dilution(p) < W'(p) - W(p-1),
    so the correct sufficient condition requires including the crossTerm.

    See `ratio_test` below for the corrected version.
-/
/- Original (false) statement:
theorem ratio_test_ORIGINAL (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h : newDispSquaredSum p + shiftSquaredSum p ≥ dilution p) :
    deltaWobble p < 0 := by
  sorry
-/

-- Computational evidence that the original ratio_test is false at p = 7:
theorem ratio_test_counterexample_hyp : newDispSquaredSum 7 + shiftSquaredSum 7 ≥ dilution 7 := by
  native_decide

theorem ratio_test_counterexample_concl : ¬(deltaWobble 7 < 0) := by
  native_decide

/-! ## Corrected Ratio Test

The correct four-term decomposition identity is:
  wobbleNumerator(p) - wobbleNumerator(p-1) = newDispSquaredSum(p) + crossTerm(p) + shiftSquaredSum(p) - 1

And deltaWobble(p) < 0 ⟺ dilution(p) < wobbleNumerator(p) - wobbleNumerator(p-1).

So the correct sufficient condition is:
  newDispSquaredSum(p) + crossTerm(p) + shiftSquaredSum(p) > dilution(p) + 1
-/

/-- The four-term identity for the wobble numerator change.
    Verified computationally for small primes. -/
theorem four_term_identity_5 :
    wobbleNumerator 5 - wobbleNumerator 4 =
    newDispSquaredSum 5 + crossTerm 5 + shiftSquaredSum 5 - 1 := by native_decide

theorem four_term_identity_7 :
    wobbleNumerator 7 - wobbleNumerator 6 =
    newDispSquaredSum 7 + crossTerm 7 + shiftSquaredSum 7 - 1 := by native_decide

theorem four_term_identity_13 :
    wobbleNumerator 13 - wobbleNumerator 12 =
    newDispSquaredSum 13 + crossTerm 13 + shiftSquaredSum 13 - 1 := by native_decide

/-
The four-term identity: wobbleNumerator(p) decomposes as
    wobbleNumerator(p-1) + newDispSquaredSum + crossTerm + shiftSquaredSum - 1.

    This follows from:
    1. fareySet(p) = fareySet(p-1) ∪ fareyNew(p) (disjoint)
    2. For old fractions with a < b: D_p(f) = D_{p-1}(f) + δ(f)
    3. For f = 1: D_p(1) = D_{p-1}(1) = 0 and δ(1) = 1
    4. Algebraic expansion: (D+δ)² = D² + 2Dδ + δ²
-/
lemma four_term_identity (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    wobbleNumerator p = wobbleNumerator (p - 1) + newDispSquaredSum p
      + crossTerm p + shiftSquaredSum p - 1 := by
  -- Apply the displacement-shift identity to each term in the sum.
  have h_displacement_shift : ∀ ab ∈ fareySet (p - 1), ab.1 < ab.2 → (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 = (displacement (p - 1) ((ab.1 : ℚ) / ab.2)) ^ 2 + 2 * displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2) + (shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 := by
    intro ab hab hlt
    have h_displacement : displacement p ((ab.1 : ℚ) / ab.2) = displacement (p - 1) ((ab.1 : ℚ) / ab.2) + shiftFun p ((ab.1 : ℚ) / ab.2) := by
      have := @displacement_shift;
      apply this p ab.1 ab.2 hp;
      · unfold fareySet at hab; aesop;
      · bv_omega;
      · rcases p with ( _ | _ | p ) <;> simp_all +decide [ fareySet ];
      · assumption
    rw [h_displacement]
    ring;
  have h_displacement_shift_one : (displacement p 1) ^ 2 = (displacement (p - 1) 1) ^ 2 + 2 * displacement (p - 1) 1 * shiftFun p 1 + (shiftFun p 1) ^ 2 - 1 := by
    unfold displacement shiftFun;
    unfold fareyRank; norm_num; ring;
    rw [ show ( Finset.filter ( fun p : ℕ × ℕ => ( p.1 : ℚ ) * ( p.2 : ℚ ) ⁻¹ ≤ 1 ) ( fareySet p ) ) = fareySet p from Finset.filter_true_of_mem fun x hx => by rw [ ← div_eq_mul_inv ] ; exact div_le_one_of_le₀ ( mod_cast by linarith [ Finset.mem_filter.mp hx ] ) ( mod_cast by linarith [ Finset.mem_filter.mp hx ] ) ] ; rw [ show ( Finset.filter ( fun p : ℕ × ℕ => ( p.1 : ℚ ) * ( p.2 : ℚ ) ⁻¹ ≤ 1 ) ( fareySet ( p - 1 ) ) ) = fareySet ( p - 1 ) from Finset.filter_true_of_mem fun x hx => by rw [ ← div_eq_mul_inv ] ; exact div_le_one_of_le₀ ( mod_cast by linarith [ Finset.mem_filter.mp hx ] ) ( mod_cast by linarith [ Finset.mem_filter.mp hx ] ) ] ; ring;
  have h_sum_displacement_shift : ∑ ab ∈ fareySet (p - 1), (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 = ∑ ab ∈ fareySet (p - 1), (displacement (p - 1) ((ab.1 : ℚ) / ab.2)) ^ 2 + 2 * ∑ ab ∈ fareySet (p - 1), displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2) + ∑ ab ∈ fareySet (p - 1), (shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 - 1 := by
    have h_sum_displacement_shift : ∀ ab ∈ fareySet (p - 1), (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 = (displacement (p - 1) ((ab.1 : ℚ) / ab.2)) ^ 2 + 2 * displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2) + (shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 - (if ab = (1, 1) then 1 else 0) := by
      intro ab hab; split_ifs <;> simp_all +decide ;
      by_cases h : ab.1 < ab.2 <;> simp_all +decide [ fareySet ];
      · exact h_displacement_shift _ _ hab.1.1 hab.1.2 hab.2.1 hab.2.2.1 hab.2.2.2 h;
      · grind;
    rw [ Finset.sum_congr rfl h_sum_displacement_shift ];
    simp +decide [ Finset.sum_add_distrib, Finset.mul_sum _ _ _, mul_assoc ];
    exact Finset.mem_filter.mpr ⟨ Finset.mem_product.mpr ⟨ Finset.mem_range.mpr ( by omega ), Finset.mem_range.mpr ( by omega ) ⟩, by norm_num, by norm_num, by norm_num ⟩;
  have h_sum_displacement_shift : ∑ ab ∈ fareySet p, (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 = ∑ ab ∈ fareySet (p - 1), (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 + ∑ ab ∈ fareyNew p, (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 := by
    rw [ ← Finset.sum_union ];
    · rw [ fareySet_eq_union p ( by linarith ) ];
    · exact fareySet_new_disjoint p ( by linarith );
  unfold wobbleNumerator newDispSquaredSum crossTerm shiftSquaredSum;
  rw [ show fareyNew p = ( fareySet p |> Finset.filter fun x => x.2 = p ) from ?_ ] at *;
  · grind;
  · ext ⟨a, b⟩; simp [fareyNew, fareySet];
    grind

/-- Helper: fareyCount is always positive. -/
lemma fareyCount_pos (N : ℕ) : 0 < fareyCount N := by
  unfold fareyCount; omega

/-
Algebraic step: given the four-term identity and the hypothesis on the
    four-term sum vs dilution, conclude deltaWobble < 0.
-/
lemma ratio_test_of_four_term (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h_id : wobbleNumerator p = wobbleNumerator (p - 1) + newDispSquaredSum p
      + crossTerm p + shiftSquaredSum p - 1)
    (h : newDispSquaredSum p + crossTerm p + shiftSquaredSum p > dilution p + 1) :
    deltaWobble p < 0 := by
  -- Let's simplify the expression using the definitions of `wobble`, `deltaWobble`, and `dilution`.
  unfold deltaWobble wobble dilution at *;
  rw [ sub_neg, div_lt_div_iff₀ ];
  · rw [ div_add_one, gt_iff_lt, div_lt_iff₀ ] at h <;> nlinarith [ show ( 0 : ℚ ) < fareyCount ( p - 1 ) from mod_cast fareyCount_pos _ ];
  · exact sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos _ ) );
  · exact sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos p ) )

/-- **Corrected Ratio Test Theorem:**
    If newDispSquaredSum + crossTerm + shiftSquaredSum > dilution + 1,
    then ΔW(p) < 0.

    This corrects the original `ratio_test` by including the crossTerm B(p)
    and the boundary correction of +1 on the right-hand side. -/
theorem ratio_test (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h : newDispSquaredSum p + crossTerm p + shiftSquaredSum p > dilution p + 1) :
    deltaWobble p < 0 :=
  ratio_test_of_four_term p hp hp5 (four_term_identity p hp hp5) h

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

/-! ## B+C positivity via correlation ratio -/

/-- If R(p) > -1/2, then B+C > 0.
    Proof: B+C = δ²(1 + 2R). Since δ² > 0 and 1 + 2R > 0, the product is positive. -/
theorem bPlusC_pos_of_corrRatio (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (hR : corrRatio p > -1/2) :
    bPlusC p > 0 := by
  rw [bPlusC_eq_shift_times_oneAddR p hp hp5]
  apply mul_pos (shiftSquaredSum_pos p hp hp5)
  linarith

private theorem corrRatio_helper :
    ∀ p ∈ Finset.Icc 11 83, Nat.Prime p → corrRatio p > -1/2 := by
  native_decide

/-- R(p) > -1/2 for all primes p with 11 ≤ p ≤ 83, verified by native_decide. -/
theorem corrRatio_gt_neg_half_range (p : ℕ) (h11 : 11 ≤ p) (hp : Nat.Prime p)
    (h83 : p ≤ 83) : corrRatio p > -1/2 :=
  corrRatio_helper p (Finset.mem_Icc.mpr ⟨h11, h83⟩) hp

/-- B+C > 0 for all primes p with 11 ≤ p ≤ 83. -/
theorem bPlusC_pos_all_le_83 (p : ℕ) (hp : Nat.Prime p) (hp11 : 11 ≤ p) (hp83 : p ≤ 83) :
    bPlusC p > 0 := by
  have hR := corrRatio_gt_neg_half_range p hp11 hp hp83
  exact bPlusC_pos_of_corrRatio p hp (by omega) hR

/-! ## Computational verification: ΔW(p) < 0 for all primes 13..113 with M(p) ≤ -3 -/

private theorem sign_helper_le_60 :
    ∀ p ∈ Finset.Icc 13 60, Nat.Prime p → (mertens p : ℤ) ≤ -3 → deltaWobble p < 0 := by
  native_decide

/-- ΔW(p) < 0 for primes p with 13 ≤ p ≤ 60 and M(p) ≤ -3. -/
theorem sign_theorem_le_60 (p : ℕ) (hp : Nat.Prime p) (hp13 : 13 ≤ p)
    (hp60 : p ≤ 60) (hM : (mertens p : ℤ) ≤ -3) :
    deltaWobble p < 0 :=
  sign_helper_le_60 p (Finset.mem_Icc.mpr ⟨hp13, hp60⟩) hp hM

-- Individual verifications for primes 61..113 with M(p) ≤ -3
theorem sign_theorem_71 : deltaWobble 71 < 0 := by native_decide
theorem sign_theorem_73 : deltaWobble 73 < 0 := by native_decide
theorem sign_theorem_79 : deltaWobble 79 < 0 := by native_decide
theorem sign_theorem_83 : deltaWobble 83 < 0 := by native_decide
theorem sign_theorem_107 : deltaWobble 107 < 0 := by native_decide
theorem sign_theorem_109 : deltaWobble 109 < 0 := by native_decide
theorem sign_theorem_113 : deltaWobble 113 < 0 := by native_decide

/-- Helper: ΔW(p) < 0 for all p ∈ [61, 113] with Nat.Prime p and M(p) ≤ -3. -/
private theorem sign_helper_61_113 :
    ∀ p ∈ Finset.Icc 61 113, Nat.Prime p → (mertens p : ℤ) ≤ -3 → deltaWobble p < 0 := by
  native_decide

/-- ΔW(p) < 0 for primes p with 61 ≤ p ≤ 113 and M(p) ≤ -3. -/
theorem sign_theorem_61_to_113 (p : ℕ) (hp : Nat.Prime p) (hp61 : 61 ≤ p)
    (hp113 : p ≤ 113) (hM : (mertens p : ℤ) ≤ -3) :
    deltaWobble p < 0 :=
  sign_helper_61_113 p (Finset.mem_Icc.mpr ⟨hp61, hp113⟩) hp hM

/-- ΔW(p) < 0 for all primes p with 13 ≤ p ≤ 113 and M(p) ≤ -3.
    Verified by interval_cases + native_decide. -/
theorem sign_theorem_all_le_113 (p : ℕ) (hp : Nat.Prime p) (hp13 : 13 ≤ p)
    (hp113 : p ≤ 113) (hM : (mertens p : ℤ) ≤ -3) :
    deltaWobble p < 0 := by
  by_cases h60 : p ≤ 60
  · exact sign_theorem_le_60 p hp hp13 h60 hM
  · exact sign_theorem_61_to_113 p hp (by omega) hp113 hM

/-- **Sign Theorem for bounded range:**
    For prime p with 13 ≤ p < 114 and M(p) ≤ -3, ΔW(p) < 0. -/
theorem sign_theorem_conj_bounded (p : ℕ) (hp : Nat.Prime p) (hp13 : 13 ≤ p)
    (hp114 : p < 114) (hM : (mertens p : ℤ) ≤ -3) :
    deltaWobble p < 0 :=
  sign_theorem_all_le_113 p hp hp13 (by omega) hM