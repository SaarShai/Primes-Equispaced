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
ΔW(p) < 0 ⟺ B + C + D > dilution + 1
where B = crossTerm, C = shiftSquaredSum, D = newDispSquaredSum,
and dilution = WN(p-1) · (n'² - n²) / n².

## Computational evidence
- Verified for ALL 4,617 primes with M(p) ≤ -3 up to p = 99,991
- Zero violations found
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

/-- **Sign Theorem (computational verification):**
    For all primes p with 13 ≤ p < 114 and M(p) ≤ -3, ΔW(p) < 0 (wobble increases).

    This covers all 13 primes in this range satisfying the Mertens condition:
    p ∈ {13, 19, 31, 43, 47, 53, 71, 73, 79, 83, 107, 109, 113}.

    NOTE: ΔW = W(p-1) - W(p), so ΔW < 0 means W(p) > W(p-1).

    The general conjecture (for ALL primes p ≥ 13 with M(p) ≤ -3) has been
    verified computationally for all 4,617 such primes up to p = 99,991 with
    zero violations. The full algebraic proof remains open, pending formalization
    of growth bounds for B + C + D vs dilution + 1. -/
theorem sign_theorem_conj :
    ∀ p ∈ Finset.filter (fun p => Nat.Prime p ∧ 13 ≤ p ∧ mertens p ≤ -3) (Finset.range 114),
    deltaWobble p < 0 := by native_decide

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

/-! ## Four-Term Decomposition -/

/-- **Four-Term Decomposition:**
    WN(p) = WN(p-1) + B + C - 1 + D
    where B = crossTerm(p), C = shiftSquaredSum(p), D = newDispSquaredSum(p). -/
theorem four_term_decomposition (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    wobbleNumerator p = wobbleNumerator (p - 1) + crossTerm p + shiftSquaredSum p - 1 +
      newDispSquaredSum p := by
  unfold wobbleNumerator crossTerm shiftSquaredSum newDispSquaredSum
  rw [show fareySet p = fareySet (p - 1) ∪ fareyNew p from ?_, Finset.sum_union]
  · have h_displacement_shift : ∀ ab ∈ fareySet (p - 1),
        displacement p (ab.1 / ab.2 : ℚ) ^ 2 =
          displacement (p - 1) (ab.1 / ab.2 : ℚ) ^ 2 +
          2 * displacement (p - 1) (ab.1 / ab.2 : ℚ) * shiftFun p (ab.1 / ab.2 : ℚ) +
          shiftFun p (ab.1 / ab.2 : ℚ) ^ 2 -
          (if ab.1 = ab.2 then 1 else 0) := by
      intro ab hab
      by_cases h : ab.1 < ab.2
      · rw [if_neg h.ne, displacement_shift]
        all_goals norm_num [fareySet] at *
        exacts [by ring, hp, hab.2.2.2, hab.2.1, by omega, h]
      · split_ifs <;> simp_all +decide [fareySet]
        · rw [displacement_shift_boundary]; ring
          · unfold displacement shiftFun; norm_num; ring
            rw [show fareyRank (p - 1) 1 = (fareySet (p - 1)).card from ?_]; ring
            refine' congr_arg Finset.card (Finset.filter_true_of_mem fun x hx => _)
            exact div_le_one_of_le₀ (mod_cast by linarith [Finset.mem_filter.mp hx])
              (Nat.cast_nonneg _)
          · assumption
        · omega
    rw [Finset.sum_congr rfl h_displacement_shift]
    norm_num [Finset.sum_add_distrib, Finset.mul_sum _ _ _, Finset.sum_mul]; ring
    rw [show (fareySet (p - 1) ∪ fareyNew p |> Finset.filter fun x => x.2 = p) =
        fareyNew p from ?_]
    norm_num [Finset.sum_add_distrib, Finset.mul_sum _ _ _, Finset.sum_mul _ _ _,
      Finset.sum_sub_distrib, Finset.sum_const_zero, zero_add, add_assoc,
      add_left_comm, add_comm]; ring
    · rw [show (fareySet (p - 1) |> Finset.filter fun x => x.1 = x.2) = {(1, 1)} from ?_]
      norm_num; ring
      ext ⟨a, b⟩; simp [fareySet]; grind
    · ext ⟨a, b⟩; simp [fareySet, fareyNew]; grind +ring
  · apply fareySet_new_disjoint p (by linarith)
  · exact fareySet_eq_union p (by linarith)

/-! ## fareyCount and fareySet cardinality -/

/-
PROBLEM
fareyCount(N) equals the cardinality of fareySet(N).

PROVIDED SOLUTION
Induction on N starting from N=1. Base case N=1: fareyCount 1 = 1 + φ(1) = 2. fareySet 1 = {(0,1), (1,1)} which has card 2. Verify by native_decide.

Inductive step: For N ≥ 2, use farey_new_fractions_count to get |fareySet(N)| = |fareySet(N-1)| + φ(N), and show fareyCount(N) = fareyCount(N-1) + φ(N) from the definition (by splitting the sum). Then apply the inductive hypothesis.

For the recurrence of fareyCount: fareyCount(N) = 1 + Σ_{k=0}^{N-1} φ(k+1) = (1 + Σ_{k=0}^{N-2} φ(k+1)) + φ(N) = fareyCount(N-1) + φ(N). This uses Finset.sum_range_succ.
-/
lemma fareyCount_eq_card (N : ℕ) (hN : 1 ≤ N) : fareyCount N = (fareySet N).card := by
  induction' hN with N hN ih;
  · native_decide +revert;
  · convert congr_arg ( fun x : ℕ => x + Nat.totient N.succ ) ih using 1;
    · unfold fareyCount; simp +arith +decide [ Finset.sum_range_succ ] ;
    · convert farey_new_fractions_count N.succ _ using 1 ; aesop

/-
PROBLEM
fareyCount is positive for N ≥ 1.

PROVIDED SOLUTION
fareyCount N = 1 + Σ ... ≥ 1 > 0.
-/
lemma fareyCount_pos (N : ℕ) (hN : 1 ≤ N) : 0 < fareyCount N := by
  exact add_pos_of_pos_of_nonneg zero_lt_one <| Finset.sum_nonneg fun _ _ => Nat.zero_le _

/-- wobbleNumerator is nonneg. -/
lemma wobbleNumerator_nonneg (N : ℕ) : 0 ≤ wobbleNumerator N := by
  unfold wobbleNumerator
  exact Finset.sum_nonneg (fun _ _ => sq_nonneg _)

/-! ## Ratio test: algebraic criterion for ΔW(p) < 0 -/

/-
PROBLEM
**Ratio Test (corrected):**
    If B + C + D > dilution + 1, then ΔW(p) < 0.

PROVIDED SOLUTION
Use four_term_decomposition to substitute wobbleNumerator(p) in the definition of deltaWobble.

deltaWobble p = wobble(p-1) - wobble(p) = WN(p-1)/n² - WN(p)/n'² where n = fareyCount(p-1), n' = fareyCount(p).

By four_term_decomposition: WN(p) = WN(p-1) + B + C - 1 + D.

So deltaWobble = WN(p-1)/n² - (WN(p-1) + B + C - 1 + D)/n'².

For this to be < 0, we need WN(p-1)/n² < (WN(p-1) + B + C - 1 + D)/n'²,
i.e., WN(p-1) * n'² < (WN(p-1) + B + C - 1 + D) * n²,
i.e., WN(p-1) * (n'² - n²) < (B + C - 1 + D) * n².

Dividing by n²: dilution < B + C - 1 + D, i.e., B + C + D > dilution + 1.

The hypothesis gives exactly this: B + C + D > dilution + 1.

Key steps:
1. Unfold deltaWobble, wobble
2. Use four_term_decomposition to rewrite WN(p)
3. Show n > 0 and n' > 0 (use fareyCount_pos)
4. Clear denominators and use the hypothesis

Actually, be careful with the division. Since we're working in ℚ, we need:
deltaWobble p = WN(p-1) / n² - WN(p) / n'²
= [WN(p-1) * n'² - WN(p) * n²] / (n² * n'²)
= [WN(p-1) * n'² - (WN(p-1) + B + C - 1 + D) * n²] / (n² * n'²)
= [WN(p-1) * (n'² - n²) - (B + C - 1 + D) * n²] / (n² * n'²)

The denominator n² * n'² > 0. So deltaWobble < 0 iff numerator < 0, iff
WN(p-1) * (n'² - n²) < (B + C - 1 + D) * n², iff
WN(p-1) * (n'² - n²) / n² < B + C - 1 + D, iff
dilution < B + C - 1 + D, iff
B + C + D > dilution + 1.

Use div_lt_iff, sub_neg, etc. to manipulate the inequality.
-/
theorem ratio_test_corrected (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h : crossTerm p + shiftSquaredSum p + newDispSquaredSum p > dilution p + 1) :
    deltaWobble p < 0 := by
  -- Apply the four-term decomposition to rewrite the wobbleNumerator.
  have h_decomp : wobbleNumerator p = wobbleNumerator (p - 1) + crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p := by
    exact four_term_decomposition p hp hp5;
  -- Substitute the decomposition into the expression for deltaWobble.
  have h_deltaWobble : deltaWobble p = (wobbleNumerator (p - 1) * (fareyCount p ^ 2 - fareyCount (p - 1) ^ 2) - (crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p) * fareyCount (p - 1) ^ 2) / (fareyCount p ^ 2 * fareyCount (p - 1) ^ 2) := by
    unfold deltaWobble;
    unfold wobble; rw [ div_sub_div ] ; ring;
    · rw [ h_decomp ] ; ring;
    · exact ne_of_gt ( sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos _ ( Nat.sub_pos_of_lt hp.one_lt ) ) ) );
    · exact ne_of_gt ( sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos p ( by linarith ) ) ) );
  rw [ h_deltaWobble, div_lt_iff₀ ];
  · unfold dilution at h;
    rw [ div_add_one, gt_iff_lt, div_lt_iff₀ ] at h <;> norm_num at *;
    · linarith;
    · exact sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos _ ( Nat.sub_pos_of_lt hp.one_lt ) ) );
    · exact ne_of_gt ( fareyCount_pos _ ( Nat.sub_pos_of_lt hp.one_lt ) );
  · exact mul_pos ( sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos p ( by linarith ) ) ) ) ( sq_pos_of_pos ( Nat.cast_pos.mpr ( fareyCount_pos ( p - 1 ) ( Nat.sub_pos_of_lt hp.one_lt ) ) ) )

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