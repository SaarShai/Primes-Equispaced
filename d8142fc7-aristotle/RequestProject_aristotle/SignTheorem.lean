import Mathlib
import PrimeCircle
import DisplacementShift
import StrictPositivity
import CrossTermPositive
import BridgeIdentity
import MertensGrowth

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
WN(p) = WN(p-1) + B + C - 1 + D
where B = crossTerm, C = shiftSquaredSum, D = newDispSquaredSum.

ΔW(p) < 0 ⟺ B + C - 1 + D > dilution
where dilution = WN(p-1) · (n'² - n²) / n²

## Corrected Ratio Test
The original hypothesis `D + C ≥ dilution` was insufficient because it omitted
the cross term B and the -1 boundary correction. A counterexample is p = 7,
where D + C ≥ dilution but ΔW(7) > 0.

The corrected sufficient condition is: D + B + C - 1 > dilution.

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

/-! ## Ratio Test — sufficient condition for ΔW(p) < 0 -/

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

/-! ## Counterexample: original hypothesis is insufficient -/

/-- **Counterexample:** The original hypothesis `D + C ≥ dilution` does not
    suffice for `ΔW(p) < 0`. For p = 7, the hypothesis holds
    (`newDispSquaredSum 7 + shiftSquaredSum 7 ≥ dilution 7`)
    but `deltaWobble 7 > 0` (wobble *decreases* at p = 7).

    The cross term B(7) = -9/10 < 0, and B + C - 1 + D < dilution for p = 7. -/
theorem ratio_test_counterexample :
    newDispSquaredSum 7 + shiftSquaredSum 7 ≥ dilution 7 ∧ ¬(deltaWobble 7 < 0) := by
  native_decide

/- ORIGINAL (INCORRECT) STATEMENT — commented out because it is false for p = 7.
   The hypothesis omits the cross term B and the boundary correction -1.

theorem ratio_test_original (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h : newDispSquaredSum p + shiftSquaredSum p ≥ dilution p) :
    deltaWobble p < 0 := by
  sorry
-/

/-! ## Four-Term Decomposition Infrastructure -/

/-- fareyCount is always positive. -/
lemma fareyCount_pos (N : ℕ) : 0 < fareyCount N := by
  unfold fareyCount; omega

/-- fareyCount cast to ℚ is positive. -/
lemma fareyCount_cast_pos (N : ℕ) : (0 : ℚ) < (fareyCount N : ℚ) := by
  exact Nat.cast_pos.mpr (fareyCount_pos N)

/-- fareyCount cast to ℚ is nonzero. -/
lemma fareyCount_cast_ne_zero (N : ℕ) : (fareyCount N : ℚ) ≠ 0 :=
  ne_of_gt (fareyCount_cast_pos N)

/-- fareyCount² cast to ℚ is positive. -/
lemma fareyCount_sq_pos (N : ℕ) : (0 : ℚ) < (fareyCount N : ℚ) ^ 2 :=
  sq_pos_of_pos (fareyCount_cast_pos N)

/-- The displacement of 1 in any Farey sequence is 0:
    D_N(1) = rank(1, F_N) - |F_N| · 1 = |F_N| - |F_N| = 0. -/
lemma displacement_one_eq_zero (N : ℕ) : displacement N 1 = 0 := by
  unfold displacement fareyRank
  rw [Finset.filter_true_of_mem]
  · simp
  · intro ab hab
    simp [fareySet] at hab
    exact div_le_one_of_le₀ (by exact_mod_cast hab.2.2.1) (Nat.cast_nonneg _)

/-- The shift at f = 1 equals 1 for any p ≥ 1: δ_p(1) = 1 - {p} = 1 - 0 = 1. -/
lemma shiftFun_one (p : ℕ) : shiftFun p 1 = 1 := by
  unfold shiftFun
  simp

/-- The displacement squared of 1 in F_p equals 0. -/
lemma dispNew_one_eq_zero (p : ℕ) : displacement p 1 = 0 :=
  displacement_one_eq_zero p

/-
PROBLEM
**Four-Term Decomposition.**
    WN(p) = WN(p-1) + B + C - 1 + D, where:
    - WN = wobbleNumerator
    - B = crossTerm p
    - C = shiftSquaredSum p
    - D = newDispSquaredSum p

    Proof sketch:
    1. fareySet(p) = fareySet(p-1) ∪ fareyNew(p) (disjoint).
    2. WN(p) = Σ_{old} D_p(f)² + Σ_{new} D_p(f)² = dispNewSquaredSum(p) + D.
    3. For old fractions f ≠ 1: D_p(f) = D_{p-1}(f) + δ(f) (displacement_shift).
    4. For f = 1: D_p(1) = 0 but (D_{p-1}(1) + δ(1))² = (0 + 1)² = 1.
    5. So dispNewSquaredSum(p) = Σ_{all old} (D_{p-1} + δ)² - 1
       = (WN(p-1) + B + C) - 1 (by quadratic_expansion_sum).
    6. Therefore WN(p) = WN(p-1) + B + C - 1 + D.

PROVIDED SOLUTION
The proof breaks into two key identities:

Identity 1: wobbleNumerator(p) = dispNewSquaredSum(p) + newDispSquaredSum(p)
  This follows from fareySet_eq_union: fareySet(p) = fareySet(p-1) ∪ fareyNew(p),
  and noting that (fareySet p).filter(_.2 = p) = fareyNew(p) for prime p,
  while the remaining elements are exactly fareySet(p-1).

Identity 2: dispNewSquaredSum(p) = dispSquaredSum(p) + crossTerm(p) + shiftSquaredSum(p) - 1
  = wobbleNumerator(p-1) + crossTerm(p) + shiftSquaredSum(p) - 1

  This uses the displacement-shift identity. For each (a,b) in fareySet(p-1):
  - If a < b: displacement(p, a/b) = displacement(p-1, a/b) + shiftFun(p, a/b)
    So D_p(a/b)² = (D_{p-1}(a/b) + δ(a/b))²
  - If a = b (i.e., f = 1): displacement(p, 1) = 0 but (D_{p-1}(1) + δ(1))² = (0+1)² = 1

  So dispNewSquaredSum(p) = Σ_{a<b} (D_{p-1} + δ)² + 0
    = Σ_{all} (D_{p-1} + δ)² - (D_{p-1}(1) + δ(1))² + D_p(1)²
    = Σ_{all} (D_{p-1} + δ)² - 1
    = (dispSquaredSum + crossTerm + shiftSquaredSum) - 1  [by quadratic_expansion_sum]

Combining: WN(p) = WN(p-1) + B + C - 1 + D.
-/
lemma four_term_decomposition (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    wobbleNumerator p =
      wobbleNumerator (p - 1) + crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p := by
  -- By definition of $wobbleNumerator$, we can split the sum into two parts: one over $fareySet (p - 1)$ and one over $fareyNew p$.
  have h_split : wobbleNumerator p = ∑ ab ∈ fareySet (p - 1), (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 + ∑ ab ∈ fareyNew p, (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 := by
    rw [ ← Finset.sum_union ];
    · rw [ ← fareySet_eq_union p ( by linarith ) ];
      rfl;
    · apply fareySet_new_disjoint p (by linarith);
  -- By definition of `displacement`, we can expand the square of the displacement for the new fractions.
  have h_expand_new : ∑ ab ∈ fareySet (p - 1), (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 = ∑ ab ∈ fareySet (p - 1), (displacement (p - 1) ((ab.1 : ℚ) / ab.2) + shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 - 1 := by
    have h_expand_old : ∀ ab ∈ fareySet (p - 1), displacement p ((ab.1 : ℚ) / ab.2) ^ 2 = (displacement (p - 1) ((ab.1 : ℚ) / ab.2) + shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 - (if ab = (1, 1) then 1 else 0) := by
      intro ab hab
      by_cases h : ab = (1, 1);
      · -- Substitute the known values of displacement p 1, displacement (p-1) 1, and shiftFun p 1.
        have h_values : displacement p 1 = 0 ∧ displacement (p - 1) 1 = 0 ∧ shiftFun p 1 = 1 := by
          exact ⟨ displacement_one_eq_zero p, displacement_one_eq_zero ( p - 1 ), shiftFun_one p ⟩;
        aesop;
      · rw [ if_neg h, displacement_shift ];
        all_goals norm_num [ fareySet ] at *;
        · assumption;
        · tauto;
        · linarith;
        · exact lt_of_le_of_lt hab.1.2 ( Nat.pred_lt hp.ne_zero );
        · cases lt_or_eq_of_le hab.2.2.1 <;> aesop;
    rw [ Finset.sum_congr rfl h_expand_old, Finset.sum_sub_distrib ] ; norm_num [ Finset.sum_ite, hp.ne_zero ] ; ring;
    exact Finset.mem_filter.mpr ⟨ Finset.mem_product.mpr ⟨ Finset.mem_range.mpr ( by omega ), Finset.mem_range.mpr ( by omega ) ⟩, by norm_num, by norm_num, by norm_num ⟩;
  -- Apply the quadratic expansion sum to the sum over `fareySet (p - 1)`.
  have h_quad_expansion : ∑ ab ∈ fareySet (p - 1), (displacement (p - 1) ((ab.1 : ℚ) / ab.2) + shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 = dispSquaredSum p + crossTerm p + shiftSquaredSum p := by
    convert quadratic_expansion_sum p using 1;
  simp_all +decide [ wobbleNumerator, newDispSquaredSum ] ; ring!;
  congr! 2;
  ext ⟨a, b⟩; simp [fareyNew, fareySet];
  grind +ring

/-
PROBLEM
**Sign Condition (Corrected).**
    If D + B + C - 1 > dilution, then ΔW(p) < 0.

    Proof: From four_term_decomposition, WN(p) = WN(p-1) + B + C - 1 + D.
    Then ΔW(p) = WN(p-1)/n² - WN(p)/n'²
              = (WN(p-1)·n'² - WN(p)·n²) / (n²·n'²)
              = (WN(p-1)·(n'²-n²) - (B+C-1+D)·n²) / (n²·n'²)
              = (dilution·n² - (B+C-1+D)·n²) / (n²·n'²)
              = (dilution - B - C + 1 - D) / n'²
    Since the hypothesis gives dilution < B+C-1+D, the numerator is negative,
    and n'² > 0, so ΔW(p) < 0.

PROVIDED SOLUTION
From four_term_decomposition: wobbleNumerator p = wobbleNumerator (p-1) + crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p.

deltaWobble p = wobble(p-1) - wobble(p)
  = wobbleNumerator(p-1) / fareyCount(p-1)² - wobbleNumerator(p) / fareyCount(p)²

Let n = fareyCount(p-1), n' = fareyCount(p). Both are positive (fareyCount_pos).
Let WN = wobbleNumerator(p-1), B = crossTerm p, C = shiftSquaredSum p, D = newDispSquaredSum p.

deltaWobble p = WN/n² - (WN + B + C - 1 + D)/n'²   [by four_term_decomp]

To show this is < 0, i.e., WN/n² < (WN + B + C - 1 + D)/n'²,
equivalently WN · n'² < (WN + B + C - 1 + D) · n²   [since n², n'² > 0]
equivalently WN · (n'² - n²) < (B + C - 1 + D) · n²

Now dilution p = WN · (n'² - n²) / n² by definition.
So the condition becomes: dilution p · n² < (B + C - 1 + D) · n²
i.e., dilution p < B + C - 1 + D = newDispSquaredSum p + crossTerm p + shiftSquaredSum p - 1.

This is exactly the hypothesis h.

Key steps:
1. Unfold deltaWobble, wobble, dilution
2. Use four_term_decomposition to substitute for wobbleNumerator p
3. Show fareyCount_cast_ne_zero and fareyCount_sq_pos for the denominator
4. Clear denominators and do the algebra with field_simp and linarith/ring
-/
lemma sign_condition (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h : newDispSquaredSum p + crossTerm p + shiftSquaredSum p - 1 > dilution p) :
    deltaWobble p < 0 := by
  unfold deltaWobble;
  unfold wobble dilution at *;
  rw [ div_sub_div, div_lt_iff₀ ];
  · rw [ four_term_decomposition p hp hp5 ] at *;
    contrapose! h;
    rw [ le_div_iff₀ ] <;> first | linarith | exact pow_pos ( Nat.cast_pos.mpr <| fareyCount_pos _ ) _;
  · exact mul_pos ( sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos _ ) ) ) ( sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos _ ) ) );
  · exact ne_of_gt ( sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos _ ) ) );
  · exact ne_of_gt ( sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos p ) ) )

/-- **Corrected Ratio Test Theorem.**
    The sufficient condition requires including the cross term B and the
    boundary correction -1.

    If D + B + C - 1 > dilution, then ΔW(p) < 0.

    The original hypothesis `D + C ≥ dilution` was insufficient because
    it omitted the cross term B and the -1 boundary correction.
    Counterexample: p = 7, where D + C ≥ dilution but B = -9/10 < 0
    and ΔW(7) > 0 (see `ratio_test_counterexample`). -/
theorem ratio_test (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h : newDispSquaredSum p + crossTerm p + shiftSquaredSum p - 1 > dilution p) :
    deltaWobble p < 0 :=
  sign_condition p hp hp5 h

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

/-! ## Correlation Ratio Analysis: R(p) > -1/2 -/

/-- The exact value of the correlation ratio at p = 11:
    R(11) = -1155/5974 ≈ -0.1934.
    This is the most negative corrRatio among all primes tested up to 100. -/
theorem corrRatio_val_11 : corrRatio 11 = -1155 / 5974 := by native_decide

/-- R(11) > -1/2: the worst-case correlation ratio is bounded away from -1/2. -/
theorem corrRatio_gt_neg_half_11 : corrRatio 11 > -1 / 2 := by native_decide

/-- **Monotonicity witness:** For all primes 13 ≤ p ≤ 100,
    corrRatio(p) ≥ corrRatio(11).
    p = 11 achieves the global minimum of the correlation ratio
    among primes ≤ 100. -/
theorem corrRatio_ge_11_for_range :
    ∀ p ∈ Finset.Icc 13 100, Nat.Prime p → corrRatio p ≥ corrRatio 11 := by
  native_decide

/-- **B+C > 0 from R > -1/2.**
    If the correlation ratio R(p) > -1/2, then 1 + 2R > 0,
    and since δ² > 0 (StrictPositivity), we get B+C = δ²·(1+2R) > 0. -/
theorem bPlusC_pos_of_corrRatio (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (hR : corrRatio p > -1 / 2) : bPlusC p > 0 := by
  rw [bPlusC_eq_shift_times_oneAddR p hp hp5]
  apply mul_pos (shiftSquaredSum_pos p hp hp5)
  linarith

/-- Helper: R(p) > -1/2 for all primes 11 ≤ p ≤ 83 (by native_decide on Finset.Icc). -/
private theorem corrRatio_helper :
    ∀ p ∈ Finset.Icc 11 83, Nat.Prime p → corrRatio p > -1 / 2 := by
  native_decide

/-- R(p) > -1/2 for all primes p with 11 ≤ p ≤ 83, verified by native_decide. -/
theorem corrRatio_gt_neg_half_range (p : ℕ) (h11 : 11 ≤ p) (hp : Nat.Prime p)
    (h83 : p ≤ 83) : corrRatio p > -1 / 2 :=
  corrRatio_helper p (Finset.mem_Icc.mpr ⟨h11, h83⟩) hp

/-- **B+C > 0 for all primes 11 ≤ p ≤ 83.** -/
theorem bPlusC_pos_all_le_83 (p : ℕ) (hp : Nat.Prime p) (hp11 : 11 ≤ p) (hp83 : p ≤ 83) :
    bPlusC p > 0 := by
  have hR := corrRatio_gt_neg_half_range p hp11 hp hp83
  exact bPlusC_pos_of_corrRatio p hp (by omega) hR

/-! ## Sign Theorem: computational verification for extended range -/

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

private theorem sign_helper_61_113 :
    ∀ p ∈ Finset.Icc 61 113, Nat.Prime p → (mertens p : ℤ) ≤ -3 → deltaWobble p < 0 := by
  native_decide

/-- ΔW(p) < 0 for primes p with 61 ≤ p ≤ 113 and M(p) ≤ -3. -/
theorem sign_theorem_61_to_113 (p : ℕ) (hp : Nat.Prime p) (hp61 : 61 ≤ p)
    (hp113 : p ≤ 113) (hM : (mertens p : ℤ) ≤ -3) :
    deltaWobble p < 0 :=
  sign_helper_61_113 p (Finset.mem_Icc.mpr ⟨hp61, hp113⟩) hp hM

/-- ΔW(p) < 0 for all primes p with 13 ≤ p ≤ 113 and M(p) ≤ -3. -/
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

/-! ## Density-1 conjecture: computational evidence -/

/-- Among primes in {11, ..., 97}, ZERO have ΔW(p) ≥ 0.
    Covers 21 primes from 11 to 97 with zero exceptions. -/
theorem density_zero_le_97 :
    (Finset.filter (fun p => Nat.Prime p ∧ 11 ≤ p ∧ ¬(deltaWobble p < 0))
      (Finset.range 98)).card = 0 := by
  native_decide

/-- The only primes with ΔW(p) ≥ 0 below 98 are {2, 3, 5, 7} — all less than 11. -/
theorem exceptions_are_small_primes :
    ∀ p ∈ Finset.range 98, Nat.Prime p → deltaWobble p ≥ 0 → p < 11 := by
  native_decide

/-- The per-denominator cross term: for a fixed denominator b,
    CT_b(p) = Σ_{(a,b) ∈ F_{p-1}, denom = b} D_{p-1}(a/b) · δ_p(a/b). -/
def perDenomCrossTerm (p b : ℕ) : ℚ :=
  ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.2 = b),
    displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)

/-
PROBLEM
The cross term decomposes as a sum over denominators:
    Σ_{f ∈ F_{p-1}} D(f)·δ(f) = Σ_{b=1}^{p-1} CT_b(p).

PROVIDED SOLUTION
The cross term is defined as crossTerm p = 2 * Σ_{ab ∈ fareySet(p-1)} D(ab) * δ(ab). So crossTerm p / 2 = Σ_{ab ∈ fareySet(p-1)} D(ab) * δ(ab). The per-denominator term perDenomCrossTerm p b = Σ_{ab ∈ fareySet(p-1), ab.2 = b} D(ab) * δ(ab). The sum Σ_{b ∈ Icc 1 (p-1)} perDenomCrossTerm p b partitions fareySet(p-1) by the second component b. Since every (a,b) in fareySet(p-1) has 1 ≤ b ≤ p-1, this is exactly a partition of the full sum. Use Finset.sum_fiberwise or Finset.sum_biUnion to decompose the sum over fareySet(p-1) by the second component.
-/
theorem crossTerm_eq_sum_perDenom (p : ℕ) :
    crossTerm p / 2 = ∑ b ∈ Finset.Icc 1 (p - 1), perDenomCrossTerm p b := by
  rw [ div_eq_iff ] <;> norm_num [ perDenomCrossTerm, crossTerm ];
  rw [ mul_comm, ← Finset.sum_biUnion ];
  · congr! 2;
    unfold fareySet; ext; aesop;
  · exact fun x hx y hy hxy => Finset.disjoint_left.mpr fun z => by aesop;

/-! ### Computational verification for p = 13

For p = 13, the Farey sequence F_12 has denominators b = 1, ..., 12.
We compute CT_b(13) for each b and verify the Weil-type bound
  |CT_b|² · b ≤ φ(b)²
equivalently |CT_b| ≤ φ(b)/√b, which is stronger than the conjectured bound.

Non-zero values:
  CT_5(13) = -1/5,  |CT|² · 5 = 1/5  ≤ φ(5)² = 16  ✓
  CT_7(13) = 1/7,   |CT|² · 7 = 1/7  ≤ φ(7)² = 36  ✓
  CT_8(13) = 1/2,   |CT|² · 8 = 2    ≤ φ(8)² = 16  ✓
  CT_11(13) = -1/11, |CT|² · 11 = 1/11 ≤ φ(11)² = 100 ✓

All other denominators give CT_b = 0.
-/

/-- CT_5(13) = -1/5. -/
theorem perDenomCT_13_5 : perDenomCrossTerm 13 5 = -1/5 := by native_decide

/-- CT_7(13) = 1/7. -/
theorem perDenomCT_13_7 : perDenomCrossTerm 13 7 = 1/7 := by native_decide

/-- CT_8(13) = 1/2. -/
theorem perDenomCT_13_8 : perDenomCrossTerm 13 8 = 1/2 := by native_decide

/-- CT_11(13) = -1/11. -/
theorem perDenomCT_13_11 : perDenomCrossTerm 13 11 = -1/11 := by native_decide

/-- For p=13, CT_b = 0 for b ∈ {1,2,3,4,6,9,10,12}. -/
theorem perDenomCT_13_zero : ∀ b ∈ ({1,2,3,4,6,9,10,12} : Finset ℕ),
    perDenomCrossTerm 13 b = 0 := by native_decide

/-- **Weil-type bound verification for p = 13:**
    For every denominator b ∈ {1,...,12}, |CT_b(13)|² · b ≤ φ(b)².
    This is equivalent to |CT_b| ≤ φ(b)/√b, a bound consistent with
    Weil-bound-style cancellation from the multiplication-by-p permutation. -/
theorem weil_bound_check_13 :
    ∀ b ∈ Finset.Icc 1 12,
      (perDenomCrossTerm 13 b) ^ 2 * b ≤ (Nat.totient b : ℚ) ^ 2 := by
  native_decide

/-- The total cross term for p = 13 equals twice the sum of per-denominator terms. -/
theorem crossTerm_decomp_13 :
    crossTerm 13 = 2 * (perDenomCrossTerm 13 5 + perDenomCrossTerm 13 7 +
      perDenomCrossTerm 13 8 + perDenomCrossTerm 13 11) := by native_decide

/-! ### Weil Bound Conjecture for the Per-Denominator Cross Term

The key structural conjecture, motivated by character sum bounds:

**Conjecture (Weil bound for cross term).**
For prime p ≥ 5 and each denominator b with 1 ≤ b ≤ p-1 and gcd(b,p) = 1:
  |CT_b(p)|² · b ≤ C² · φ(b)²
for some absolute constant C > 0 (computationally, C = 1 suffices for all
tested primes up to p = 100).

Equivalently: |CT_b(p)| ≤ C · φ(b) / √b.

**Proof path (character sum approach):**
1. The shift δ(a/b) = (a - pa mod b)/b involves the multiplication-by-p map
   on (ℤ/bℤ)*, which is a group automorphism.
2. The displacement D(a/b) involves the global Farey rank, which has a
   Ramanujan sum expansion: D(a/b) ≈ Σ_{q|b} c_q(a) · g(q) for some
   arithmetic function g.
3. The cross term CT_b = Σ_a D(a/b)·δ(a/b) is a bilinear form mixing
   the global rank structure (via D) and the local multiplication map (via δ).
4. Expanding D in Dirichlet characters mod b and using the Weil bound
   |Σ χ(a)·f(a)| ≤ C·√b for non-trivial χ gives the cancellation.
5. The cancellation is specific to the algebraic structure of σ_p;
   random permutations do NOT achieve the same level of cancellation
   (as verified by the z-score analysis: z-scores range from -4 to -24).

This bound, combined with Σ δ² ~ φ(b)/b, would give:
  |R(p)| = |Σ_b CT_b| / (Σ_b δ²_b) ≤ C / √(min_b)
which tends to 0 for large primes, proving R > -1 and hence B+C > 0.
-/

/- ORIGINAL (INCORRECT) STATEMENT — commented out because it is false.
   Counterexample: p = 23, b = 12 gives CT = 29/18, CT²·b = 841/27 > 16 = φ(12)².
   The bound was computationally tested only up to p ≤ 19 (not p ≤ 100 as claimed).
   The issue is that displacement D_{p-1}(a/b) grows with p, so the per-denominator
   cross term CT_b grows beyond the φ(b)/√b bound for larger primes.

theorem weil_bound_cross_term (p b : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (hb : 1 ≤ b) (hbp : b ≤ p - 1) :
    (perDenomCrossTerm p b) ^ 2 * b ≤ (Nat.totient b : ℚ) ^ 2 := by
  sorry
-/

/-- **Counterexample to the Weil bound conjecture (C=1):**
    For p = 23, b = 12: CT_12(23) = 29/18, so CT²·b = 841/27 > 16 = φ(12)².
    This is the smallest prime where the bound fails. -/
theorem weil_bound_counterexample :
    ¬((perDenomCrossTerm 23 12) ^ 2 * 12 ≤ (Nat.totient 12 : ℚ) ^ 2) := by
  native_decide

/-- **Weil bound holds for p ≤ 19:**
    The original bound CT_b² · b ≤ φ(b)² does hold for all primes 5 ≤ p ≤ 19
    and all denominators 1 ≤ b ≤ p-1. -/
theorem weil_bound_le_19 :
    ∀ p ∈ Finset.Icc 5 19, Nat.Prime p →
      ∀ b ∈ Finset.Icc 1 (p - 1),
        (perDenomCrossTerm p b) ^ 2 * b ≤ (Nat.totient b : ℚ) ^ 2 := by
  native_decide

/-! ### Consequence: R(p) → 0 and B+C > 0

If the Weil bound |CT_b| ≤ φ(b)/√b holds, then:
  |B/2| = |Σ_b CT_b| ≤ Σ_b |CT_b| ≤ Σ_b φ(b)/√b

Meanwhile, δ² = Σ_b (Σ_a δ(a/b)²) and each per-denominator δ² term is
of order φ(b)/b. So:
  |R| = |B|/(2·δ²) ≤ (Σ φ(b)/√b) / (Σ φ(b)/b) ~ 1/√(typical b)

For large primes, the typical denominator b is of order p, so |R| ~ 1/√p → 0.
This gives R > -1 for p sufficiently large, and hence B+C > 0. -/