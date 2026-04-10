import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DisplacementShift
import RequestProject.StrictPositivity
import RequestProject.CrossTermPositive
import RequestProject.BridgeIdentity
import RequestProject.MertensGrowth

/-!
# The Sign Theorem: ΔW(p) < 0 for primes

## Statement (original)
For prime p ≥ 13 with Mertens function M(p) ≤ -3, the Farey discrepancy
strictly increases: W(F_p) > W(F_{p-1}), equivalently ΔW(p) < 0.

## Stronger Conjecture
Computational evidence shows ΔW(p) < 0 for ALL primes p ≥ 11,
regardless of the Mertens value M(p). This is verified by `native_decide`
for all primes p ∈ [11, 113].

**Note:** ΔW(p) > 0 for p ∈ {2, 3, 5, 7}, so the conjecture cannot be
extended below p = 11. This is because for very small primes, the "dilution"
effect (adding many fractions relative to the Farey set size) outweighs the
displacement growth.

## Key Definitions
- W(N) = (1/|F_N|²) · Σ_{f ∈ F_N} D(f)² — the Farey wobble
- ΔW(p) = W(F_{p-1}) - W(F_p) — discrepancy change at prime step
- B(p) = 2 · Σ D·δ — cross term
- C(p) = Σ δ² — shift-squared sum
- D(p) = Σ D_p(k/p)² — new displacement squared sum

## Four-Term Decomposition (PROVED COMPUTATIONALLY)
WN(p) = WN(p-1) + B + C - 1 + D

where:
- WN = wobbleNumerator (sum of squared displacements)
- B = crossTerm = 2 Σ D_{p-1}(f) · δ(f)
- C = shiftSquaredSum = Σ δ(f)²
- D = newDispSquaredSum = Σ D_p(k/p)²
- The -1 is the boundary correction at f = 1

## Sign Condition
ΔW(p) < 0 ⟺ B + C - 1 + D > dilution
where dilution = WN(p-1) · (n'² - n²) / n²

## Computational evidence
- Verified for ALL 4,617 primes with M(p) ≤ -3 up to p = 99,991
- ΔW(p) < 0 verified by native_decide for ALL primes p ∈ [11, 113]
  (including primes with M(p) > -3, e.g., p = 11, 17, 23, 29, 37, 41)
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

/-! ## Four-Term Decomposition Identity -/

/-- **Four-Term Decomposition (computational verification for p = 7):**
    WN(p) = WN(p-1) + B + C - 1 + D. -/
theorem four_term_decomposition_7 :
    wobbleNumerator 7 =
      wobbleNumerator 6 + crossTerm 7 + shiftSquaredSum 7 - 1 + newDispSquaredSum 7 := by
  native_decide

/-- **Four-Term Decomposition (computational verification for p = 11):**
    WN(p) = WN(p-1) + B + C - 1 + D. -/
theorem four_term_decomposition_11 :
    wobbleNumerator 11 =
      wobbleNumerator 10 + crossTerm 11 + shiftSquaredSum 11 - 1 + newDispSquaredSum 11 := by
  native_decide

/-- **Four-Term Decomposition (computational verification for p = 13):**
    WN(p) = WN(p-1) + B + C - 1 + D. -/
theorem four_term_decomposition_13 :
    wobbleNumerator 13 =
      wobbleNumerator 12 + crossTerm 13 + shiftSquaredSum 13 - 1 + newDispSquaredSum 13 := by
  native_decide

/-
PROBLEM
**Four-Term Decomposition (general statement):**
    For prime p ≥ 5, WN(p) = WN(p-1) + crossTerm(p) + shiftSquaredSum(p) - 1 + newDispSquaredSum(p).

    The -1 is the boundary correction at f = 1, where
    D_p(1) = D_{p-1}(1) + δ(1) - 1 (not D_{p-1}(1) + δ(1)).

PROVIDED SOLUTION
The four-term decomposition WN(p) = WN(p-1) + B + C - 1 + D follows from:

1. fareySet(p) = fareySet(p-1) ∪ fareyNew(p) (disjoint union for prime p)
   This gives: WN(p) = Σ_{f ∈ F_{p-1}} D_p(f)² + Σ_{f ∈ new} D_p(f)²
   = (Σ_{f ∈ F_{p-1}} D_p(f)²) + newDispSquaredSum(p)

2. For old fractions f < 1: D_p(f) = D_{p-1}(f) + δ(f) (displacement_shift)
   For f = 1: D_p(1) = D_{p-1}(1) + δ(1) - 1 (displacement_shift_boundary)
   And D_{p-1}(1) = 0, δ(1) = 1, so D_p(1) = 0.

3. Σ_{f ∈ F_{p-1}} D_p(f)²
   = Σ_{f < 1} (D_{p-1}(f) + δ(f))² + D_p(1)²
   = Σ_{f ∈ F_{p-1}} (D_{p-1}(f) + δ(f))² - (D_{p-1}(1) + δ(1))² + D_p(1)²
   = Σ_{f ∈ F_{p-1}} (D_{p-1}(f) + δ(f))² - 1 + 0
   = WN(p-1) + B + C - 1
   (using the quadratic expansion: Σ(D+δ)² = ΣD² + 2ΣDδ + Σδ² = WN(p-1) + B + C)

4. So WN(p) = WN(p-1) + B + C - 1 + D.

This proof requires a lot of machinery. It might be very hard for the subagent to prove in full generality. The key lemmas used are:
- fareySet_eq_union, fareySet_new_disjoint (from DisplacementShift)
- displacement_shift (for f < 1)
- displacement_shift_boundary (for f = 1)
- quadratic_expansion_sum (from CrossTermPositive)
-/
theorem four_term_decomposition (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    wobbleNumerator p =
      wobbleNumerator (p - 1) + crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p := by
  have h_decomp : ∑ ab ∈ fareySet p, (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 = ∑ ab ∈ fareySet (p - 1), (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 + ∑ ab ∈ fareyNew p, (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 := by
    rw [ ← Finset.sum_union ];
    · rw [ fareySet_eq_union p ( by linarith ) ];
    · apply fareySet_new_disjoint; linarith [Nat.sub_add_cancel hp.pos];
  have h_decomp : ∑ ab ∈ fareySet (p - 1), (displacement p ((ab.1 : ℚ) / ab.2)) ^ 2 = ∑ ab ∈ fareySet (p - 1), (displacement (p - 1) ((ab.1 : ℚ) / ab.2) + shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 - 1 := by
    have h_decomp : ∀ ab ∈ fareySet (p - 1), displacement p ((ab.1 : ℚ) / ab.2) ^ 2 = (displacement (p - 1) ((ab.1 : ℚ) / ab.2) + shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 - (if ab = (1, 1) then 1 else 0) := by
      intros ab hab
      by_cases h : ab = (1, 1);
      · unfold displacement shiftFun; norm_num [ h ] ;
        unfold fareyRank;
        rw [ show ( fareySet p |>.filter fun p : ℕ × ℕ => ( p.1 : ℚ ) / p.2 ≤ 1 ) = fareySet p from ?_, show ( fareySet ( p - 1 ) |>.filter fun p : ℕ × ℕ => ( p.1 : ℚ ) / p.2 ≤ 1 ) = fareySet ( p - 1 ) from ?_ ] <;> norm_num [ Finset.filter_true_of_mem ];
        · intro a b hab; rw [ div_le_iff₀ ] <;> norm_cast <;> linarith [ Finset.mem_filter.mp hab, Finset.mem_product.mp ( Finset.mem_filter.mp hab |>.1 ) ] ;
        · intro a b hab; rw [ div_le_iff₀ ] <;> norm_cast <;> linarith [ Finset.mem_filter.mp hab |>.2 ] ;
      · rw [ if_neg h, displacement_shift ];
        all_goals norm_num [ fareySet ] at hab ⊢;
        · assumption;
        · tauto;
        · linarith;
        · exact lt_of_le_of_lt hab.1.2 ( Nat.pred_lt hp.ne_zero );
        · grind;
    rw [ Finset.sum_congr rfl h_decomp, Finset.sum_sub_distrib ] ; norm_num;
    unfold fareySet; norm_num; omega;
  unfold wobbleNumerator crossTerm shiftSquaredSum newDispSquaredSum;
  simp_all +decide [ Finset.sum_add_distrib, add_sq, Finset.mul_sum _ _ _, Finset.sum_mul ] ; ring!;
  rw [ show fareyNew p = ( fareySet p |> Finset.filter fun x => x.2 = p ) from ?_ ];
  ext ⟨a, b⟩; simp [fareyNew, fareySet];
  grind

/-! ## The Sign Theorem -/

/-- **Sign Theorem (original conjecture, Mertens condition):**
    For prime p ≥ 13 with M(p) ≤ -3, ΔW(p) < 0 (wobble increases).

    NOTE: ΔW = W(p-1) - W(p), so ΔW < 0 means W(p) > W(p-1). -/
theorem sign_theorem_conj (p : ℕ) (hp : Nat.Prime p) (hp13 : 13 ≤ p)
    (hM : (mertens p : ℤ) ≤ -3) :
    deltaWobble p < 0 := by
  sorry

/-! ## Stronger Conjecture: ΔW(p) < 0 for ALL primes p ≥ 11

The Mertens condition M(p) ≤ -3 is NOT needed. Computational verification shows
ΔW(p) < 0 for EVERY prime p ≥ 11, including those with M(p) = -2, -1, 0, etc.

Counterexamples below p = 11:
- ΔW(2) = 1/9 > 0
- ΔW(3) = 1/15 > 0
- ΔW(5) = 1/77 > 0
- ΔW(7) = 71/25935 > 0

These small primes have ΔW > 0 because the dilution effect dominates:
adding φ(p) = p-1 new fractions to a small Farey set F_{p-1} causes
a proportionally larger normalization change than the displacement growth.
-/

/-- **Stronger Sign Theorem (conjecture):**
    For ALL primes p ≥ 11, ΔW(p) < 0 (wobble increases),
    regardless of the Mertens value M(p).

    This is strictly stronger than `sign_theorem_conj` since it drops the
    Mertens condition M(p) ≤ -3. -/
theorem sign_theorem_all_primes (p : ℕ) (hp : Nat.Prime p) (hp11 : 11 ≤ p) :
    deltaWobble p < 0 := by
  sorry

/-! ## Computational counterexamples: ΔW(p) > 0 for p ∈ {2, 3, 5, 7}

These show the conjecture is sharp: p ≥ 11 is the correct threshold. -/

/-- ΔW(2) = 1/9 > 0: wobble DECREASED at p = 2. -/
theorem deltaWobble_pos_2 : deltaWobble 2 > 0 := by native_decide

/-- ΔW(3) = 1/15 > 0: wobble DECREASED at p = 3. -/
theorem deltaWobble_pos_3 : deltaWobble 3 > 0 := by native_decide

/-- ΔW(5) = 1/77 > 0: wobble DECREASED at p = 5. -/
theorem deltaWobble_pos_5 : deltaWobble 5 > 0 := by native_decide

/-- ΔW(7) = 71/25935 > 0: wobble DECREASED at p = 7. -/
theorem deltaWobble_pos_7 : deltaWobble 7 > 0 := by native_decide

/-! ## Computational verification: ΔW(p) < 0 for individual primes -/

/-- ΔW(11) < 0. M(11) = -2 (no Mertens condition needed!). -/
theorem sign_theorem_11 : deltaWobble 11 < 0 := by native_decide

/-- ΔW(13) < 0. M(13) = -3. -/
theorem sign_theorem_13 : deltaWobble 13 < 0 := by native_decide

/-- ΔW(19) < 0. M(19) = -3. -/
theorem sign_theorem_19 : deltaWobble 19 < 0 := by native_decide

/-- ΔW(31) < 0. M(31) = -4. -/
theorem sign_theorem_31 : deltaWobble 31 < 0 := by native_decide

/-! ## Batch verification: ALL primes in [11, 113]

Split into manageable ranges to avoid native_decide timeouts. -/

/-- ΔW(p) < 0 for every prime p with 11 ≤ p < 50.
    Covers 13 primes: 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47. -/
theorem sign_theorem_11_to_50 :
    ∀ p ∈ Finset.filter (fun p => Nat.Prime p ∧ 11 ≤ p) (Finset.range 50),
    deltaWobble p < 0 := by native_decide

/-- ΔW(p) < 0 for every prime p with 50 ≤ p < 80.
    Covers 7 primes: 53, 59, 61, 67, 71, 73, 79. -/
theorem sign_theorem_50_to_80 :
    ∀ p ∈ Finset.filter (fun p => Nat.Prime p ∧ 50 ≤ p) (Finset.range 80),
    deltaWobble p < 0 := by native_decide

/-- ΔW(p) < 0 for every prime p with 80 ≤ p < 100.
    Covers 4 primes: 83, 89, 97. -/
theorem sign_theorem_80_to_100 :
    ∀ p ∈ Finset.filter (fun p => Nat.Prime p ∧ 80 ≤ p) (Finset.range 100),
    deltaWobble p < 0 := by native_decide

/-- ΔW(p) < 0 for every prime p with 100 ≤ p < 114.
    Covers 5 primes: 101, 103, 107, 109, 113. -/
theorem sign_theorem_100_to_114 :
    ∀ p ∈ Finset.filter (fun p => Nat.Prime p ∧ 100 ≤ p) (Finset.range 114),
    deltaWobble p < 0 := by native_decide

/-! ## Sign condition from the four-term decomposition

The correct condition for ΔW(p) < 0 is:
  B + C - 1 + D > dilution(p)

where B = crossTerm, C = shiftSquaredSum, D = newDispSquaredSum.

NOTE: An earlier version stated a "ratio test" with D + C ≥ dilution (ignoring B
and the boundary correction). That version was FALSE: counterexample at p = 7
where D + C > dilution but ΔW(7) > 0 because B = -9/10 is very negative.
-/

/-
PROBLEM
**Sign Condition (correct version):**
    If crossTerm(p) + shiftSquaredSum(p) - 1 + newDispSquaredSum(p) > dilution(p),
    then ΔW(p) < 0.

    This follows directly from the four-term decomposition
    WN(p) = WN(p-1) + B + C - 1 + D and the definition of dilution.

PROVIDED SOLUTION
We need to show that if WN(p) = WN(p-1) + B + C - 1 + D and B + C - 1 + D > dilution(p), then deltaWobble p < 0.

deltaWobble p = wobble(p-1) - wobble(p)
= WN(p-1)/n² - WN(p)/n'²
where n = fareyCount(p-1) and n' = fareyCount(p).

For this to be < 0 we need WN(p)/n'² > WN(p-1)/n², i.e., WN(p) · n² > WN(p-1) · n'².

From h_decomp: WN(p) = WN(p-1) + (B + C - 1 + D).
So WN(p) · n² = WN(p-1) · n² + (B + C - 1 + D) · n².
We need this > WN(p-1) · n'², i.e., (B + C - 1 + D) · n² > WN(p-1) · (n'² - n²).

dilution(p) = WN(p-1) · (n'² - n²) / n².
So the condition h says: B + C - 1 + D > WN(p-1) · (n'² - n²) / n².
Multiplying by n² > 0: (B + C - 1 + D) · n² > WN(p-1) · (n'² - n²).

Key facts needed:
1. fareyCount is always positive (it's 1 + sum of positive terms), so n > 0 and n² > 0.
2. fareyCount(p) > fareyCount(p-1) for prime p ≥ 5, so n' > n > 0 and n'² > n² > 0.
3. wobble = WN / fareyCount², so deltaWobble = WN(p-1)/n² - WN(p)/n'².
4. fareyCount equals (fareySet N).card... actually we need to verify this.

Actually wait - wobble uses fareyCount but wobbleNumerator sums over fareySet. And fareyCount(N) = 1 + Σ_{k=1}^N φ(k) while (fareySet N).card might be different. Let me check.

Actually fareyCount(N) = (fareySet N).card. Both count the Farey fractions of order N.

The proof is algebraic: unfold deltaWobble, wobble, dilution. Show that WN(p)/n'² > WN(p-1)/n² using the decomposition and the condition h. The key step is multiplying the inequality h by n² (which is positive) and comparing with the cross-multiplied form.

We need to show deltaWobble p < 0, which by definition is wobble(p-1) - wobble(p) < 0, i.e., wobble(p) > wobble(p-1).

Unfolding definitions:
- wobble N = wobbleNumerator N / (fareyCount N)²
- deltaWobble p = wobbleNumerator(p-1) / (fareyCount(p-1))² - wobbleNumerator(p) / (fareyCount(p))²
- dilution p = wobbleNumerator(p-1) * ((fareyCount p)² - (fareyCount(p-1))²) / (fareyCount(p-1))²

Let WN₀ = wobbleNumerator(p-1), WNp = wobbleNumerator(p), n = (fareyCount(p-1) : ℚ), n' = (fareyCount(p) : ℚ).

From h_decomp: WNp = WN₀ + excess where excess = crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p.
From h: excess > dilution p = WN₀ * (n'² - n²) / n².

deltaWobble p = WN₀/n² - WNp/n'² = WN₀/n² - (WN₀ + excess)/n'²
= (WN₀ · n'² - (WN₀ + excess) · n²) / (n² · n'²)
= (WN₀ · (n'² - n²) - excess · n²) / (n² · n'²)

Since h says excess > WN₀ · (n'² - n²) / n², multiplying by n² > 0:
excess · n² > WN₀ · (n'² - n²)
So WN₀ · (n'² - n²) - excess · n² < 0.
And n² · n'² > 0, so the fraction is negative.

Key facts:
1. n = (fareyCount(p-1) : ℚ) ≥ 1 > 0 (fareyCount N = 1 + Σ φ(k) ≥ 1)
2. n' = (fareyCount(p) : ℚ) ≥ 1 > 0
3. So n² > 0, n'² > 0, n² · n'² > 0

Use `sub_div` to combine the fractions and then `div_neg_of_neg_of_pos` or similar.
-/
theorem sign_condition (p : ℕ) (_hp : Nat.Prime p) (_hp5 : 5 ≤ p)
    (h_decomp : wobbleNumerator p =
      wobbleNumerator (p - 1) + crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p)
    (h : crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p > dilution p) :
    deltaWobble p < 0 := by
  rw [ show deltaWobble p = wobbleNumerator ( p - 1 ) / ( fareyCount ( p - 1 ) : ℚ ) ^ 2 - wobbleNumerator p / ( fareyCount p : ℚ ) ^ 2 from rfl ];
  rw [ sub_neg, div_lt_div_iff₀ ];
  · unfold dilution at h;
    rw [ gt_iff_lt, div_lt_iff₀ ] at h;
    · rw [ h_decomp ] ; linarith;
    · exact sq_pos_of_pos <| Nat.cast_pos.mpr <| Nat.pos_of_ne_zero <| by unfold fareyCount; aesop;
  · exact sq_pos_of_pos <| Nat.cast_pos.mpr <| Nat.pos_of_ne_zero <| by unfold fareyCount; aesop;
  · exact sq_pos_of_pos <| Nat.cast_pos.mpr <| by unfold fareyCount; exact add_pos_of_pos_of_nonneg zero_lt_one <| Finset.sum_nonneg fun _ _ => Nat.zero_le _;

/-! ## The B+C sum and ratio test components -/

/-- The B+C sum: crossTerm(p) + shiftSquaredSum(p).
    B+C > 0 implies ΔW < 0 when combined with D ≥ dilution + 1. -/
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

/-- **Ratio Test (CORRECTED version, statement only):**
    The original ratio test `D + C ≥ dilution → ΔW < 0` was FALSE
    (counterexample: p = 7 has D + C > dilution but ΔW(7) > 0).

    The correct sufficient condition includes B:
    If newDispSquaredSum + crossTerm + shiftSquaredSum > dilution + 1,
    then ΔW(p) < 0. -/
theorem ratio_test_corrected (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h_decomp : wobbleNumerator p =
      wobbleNumerator (p - 1) + crossTerm p + shiftSquaredSum p - 1 + newDispSquaredSum p)
    (h : newDispSquaredSum p + crossTerm p + shiftSquaredSum p > dilution p + 1) :
    deltaWobble p < 0 :=
  sign_condition p hp hp5 h_decomp (by linarith)

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