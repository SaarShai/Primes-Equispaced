import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DisplacementShift
import RequestProject.StrictPositivity
import RequestProject.CrossTermPositive
import RequestProject.BridgeIdentity

/-!
# The Permutation Square-Sum Identity

## Statement
For prime p and N = p - 1, summing over all proper fractions a/b in the Farey
sequence F_N (i.e., with a < b):
  Sigma_{a<b} (a/b) * delta(a/b) = (1/2) * Sigma_{a<b} delta(a/b)^2
where delta(a/b) = shiftFun p (a/b) = a/b - {p * a/b}.

Over the full Farey set (including f = 0 and f = 1), the identity becomes:
  Sigma f * delta(f) = (1/2) * Sigma delta(f)^2 + 1/2
because at f = 1: f * delta(1) = 1 * 1 = 1 but delta(1)^2/2 = 1/2.

## Proof outline
1. Write delta = x - {px} where x = a/b, {px} = (pa mod b)/b.
2. Then x * delta - delta^2 / 2 = (x^2 - {px}^2) / 2  (algebraic identity).
3. For each fixed b, the map a -> pa mod b is a permutation of coprime
   residues (since gcd(p,b) = 1), by coprime_mul_perm from BridgeIdentity.lean.
4. Therefore Sigma_{gcd(a,b)=1} (a/b)^2 = Sigma_{gcd(a,b)=1} (pa mod b / b)^2.
5. Each per-denominator sum of (x^2 - {px}^2) vanishes, so
   Sigma(x * delta - delta^2 / 2) = 0, giving the identity.

## Connection to existing results
- The shift-squared sum shiftSquaredSum is defined in StrictPositivity.lean.
- The permutation coprime_mul_perm is proved in BridgeIdentity.lean.
- The cross term crossTerm = 2 Sigma D * delta is defined in CrossTermPositive.lean.
- This identity provides a structural constraint on Sigma f * delta(f).
-/

open Finset BigOperators

/-! ## Definitions -/

/-- The value-times-shift sum over proper fractions (a < b) in F_{p-1}:
    Sigma_{(a,b) in fareySet(p-1), a<b} (a/b) * shiftFun(p, a/b). -/
def valueTimesShiftProper (p : ℕ) : ℚ :=
  ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2),
    ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)

/-- The shift-squared sum over proper fractions (a < b) in F_{p-1}. -/
def shiftSquaredSumProper (p : ℕ) : ℚ :=
  ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2),
    (shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2

/-- The value-times-shift sum over the full Farey set F_{p-1}:
    Sigma_{(a,b) in fareySet(p-1)} (a/b) * shiftFun(p, a/b). -/
def valueTimesShift (p : ℕ) : ℚ :=
  ∑ ab ∈ fareySet (p - 1),
    ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)

/-! ## Computational verification -/

/-- The identity holds for p = 5 (proper fractions). -/
theorem perm_identity_proper_5 :
    valueTimesShiftProper 5 = shiftSquaredSumProper 5 / 2 := by native_decide

/-- The identity holds for p = 7 (proper fractions). -/
theorem perm_identity_proper_7 :
    valueTimesShiftProper 7 = shiftSquaredSumProper 7 / 2 := by native_decide

/-- The identity holds for p = 11 (proper fractions). -/
theorem perm_identity_proper_11 :
    valueTimesShiftProper 11 = shiftSquaredSumProper 11 / 2 := by native_decide

/-- The identity holds for p = 13 (proper fractions). -/
theorem perm_identity_proper_13 :
    valueTimesShiftProper 13 = shiftSquaredSumProper 13 / 2 := by native_decide

/-- The identity holds for p = 19 (proper fractions). -/
theorem perm_identity_proper_19 :
    valueTimesShiftProper 19 = shiftSquaredSumProper 19 / 2 := by native_decide

/-- The identity holds for p = 23 (proper fractions). -/
theorem perm_identity_proper_23 :
    valueTimesShiftProper 23 = shiftSquaredSumProper 23 / 2 := by native_decide

/-- The corrected full-sum identity for p = 5:
    Sigma f * delta(f) = Sigma delta(f)^2 / 2 + 1/2. -/
theorem perm_identity_full_5 :
    valueTimesShift 5 = shiftSquaredSum 5 / 2 + 1 / 2 := by native_decide

/-- The corrected full-sum identity for p = 7. -/
theorem perm_identity_full_7 :
    valueTimesShift 7 = shiftSquaredSum 7 / 2 + 1 / 2 := by native_decide

/-- The corrected full-sum identity for p = 13. -/
theorem perm_identity_full_13 :
    valueTimesShift 13 = shiftSquaredSum 13 / 2 + 1 / 2 := by native_decide

/-- Batch verification: the proper-fractions identity holds for all primes
    5 <= p <= 29. -/
theorem perm_identity_proper_le_29 :
    ∀ p ∈ Finset.filter Nat.Prime (Finset.Icc 5 29),
      valueTimesShiftProper p = shiftSquaredSumProper p / 2 := by
  native_decide

/-- Batch verification: the corrected full-sum identity holds for all primes
    5 <= p <= 29. -/
theorem perm_identity_full_le_29 :
    ∀ p ∈ Finset.filter Nat.Prime (Finset.Icc 5 29),
      valueTimesShift p = shiftSquaredSum p / 2 + 1 / 2 := by
  native_decide

/-! ## The algebraic identity: x * delta - delta^2/2 = (x^2 - y^2)/2 -/

/-- For any rationals x, y with delta = x - y:
    x * (x - y) - (x - y)^2 / 2 = (x^2 - y^2) / 2.

    This is the pointwise identity underlying the permutation square-sum identity.
    Setting x = a/b and y = (pa mod b)/b = {p * a/b}, we get
    x * delta - delta^2/2 = (x^2 - {px}^2)/2. -/
lemma algebraic_identity (x y : ℚ) :
    x * (x - y) - (x - y) ^ 2 / 2 = (x ^ 2 - y ^ 2) / 2 := by
  ring

/-! ## Permutation invariance of squared sums -/

/-- Permutation invariance of sums: for any function f,
    Sigma_{gcd(a,b)=1, a<b} f(a*p%b) = Sigma_{gcd(a,b)=1, a<b} f(a)
    when gcd(p, b) = 1. This follows from coprime_mul_perm. -/
lemma sum_coprime_perm_eq (b p : ℕ) (hb : 0 < b) (hcop : Nat.Coprime p b)
    (f : ℕ → ℚ) :
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b), f (a * p % b) =
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b), f a := by
  have hperm := coprime_mul_perm b p hb hcop
  conv_lhs =>
    arg 2; ext a; rw [show a * p % b = (fun a => a * p % b) a from rfl]
  rw [← Finset.sum_image (f := f) (s := (Finset.range b).filter (fun a => Nat.Coprime a b))
    (g := fun a => a * p % b)]
  · rw [hperm]
  · -- Injectivity of a -> a*p%b on coprime residues
    intro a₁ ha₁ a₂ ha₂ heq
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at ha₁ ha₂
    have ha₁r := ha₁.1
    have ha₂r := ha₂.1
    -- a₁ * p % b = a₂ * p % b implies a₁ * p ≡ a₂ * p (mod b)
    -- Since gcd(p, b) = 1, cancel p to get a₁ ≡ a₂ (mod b)
    -- Since a₁, a₂ < b, we get a₁ = a₂
    have hmod : a₁ * p ≡ a₂ * p [MOD b] := heq
    have hcong : a₁ ≡ a₂ [MOD b] := by
      rw [Nat.modEq_iff_dvd] at hmod ⊢
      have hsub : (b : ℤ) ∣ ((a₂ : ℤ) - a₁) * p := by
        convert hmod using 1; push_cast; ring
      exact (hcop.symm.cast (R := ℤ)).dvd_of_dvd_mul_right hsub
    -- Since a₁, a₂ < b and a₁ ≡ a₂ (mod b), we get a₁ = a₂
    rw [Nat.ModEq] at hcong
    simp only [Nat.mod_eq_of_lt ha₁r, Nat.mod_eq_of_lt ha₂r] at hcong
    exact hcong

/-- The sum of squares of coprime residues is invariant under the
    permutation a -> a*p % b when gcd(p, b) = 1.

    Sigma_{gcd(a,b)=1, a<b} (a*p%b)^2 = Sigma_{gcd(a,b)=1, a<b} a^2. -/
lemma coprime_square_sum_perm_invariant (b p : ℕ) (hb : 0 < b)
    (hcop : Nat.Coprime p b) :
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b),
      ((a * p % b : ℕ) : ℚ) ^ 2 =
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b),
      ((a : ℕ) : ℚ) ^ 2 :=
  sum_coprime_perm_eq b p hb hcop (fun a => (a : ℚ) ^ 2)

/-! ## Per-denominator cancellation -/

/-- For each fixed denominator b >= 2 with gcd(p, b) = 1, the sum
    Sigma_{gcd(a,b)=1, 0<=a<b} ((a/b)^2 - ((pa mod b)/b)^2) = 0.

    This follows because a -> pa mod b permutes the coprime residues,
    so Sigma (a/b)^2 = Sigma ((pa mod b)/b)^2. -/
lemma per_denom_cancel (p b : ℕ) (hb : 1 < b) (hcop : Nat.Coprime p b) :
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b),
      (((a : ℚ) / b) ^ 2 - (((a * p % b : ℕ) : ℚ) / b) ^ 2) = 0 := by
  have hb_pos : (0 : ℚ) < (b : ℚ) := by positivity
  have hb_ne : (b : ℚ) ≠ 0 := ne_of_gt hb_pos
  have hb2_ne : (b : ℚ) ^ 2 ≠ 0 := pow_ne_zero 2 hb_ne
  -- Reduce to: Sigma a^2 = Sigma (a*p%b)^2
  have hsq := coprime_square_sum_perm_invariant b p (by omega) hcop
  -- Each term is (a^2 - (a*p%b)^2) / b^2, and the numerator sums to 0
  have : ∀ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b),
      ((a : ℚ) / b) ^ 2 - (((a * p % b : ℕ) : ℚ) / b) ^ 2 =
      ((a : ℚ) ^ 2 - ((a * p % b : ℕ) : ℚ) ^ 2) / (b : ℚ) ^ 2 := by
    intro a _
    rw [div_pow, div_pow]
    ring
  rw [Finset.sum_congr rfl this, ← Finset.sum_div, Finset.sum_sub_distrib]
  simp only [hsq, sub_self, zero_div]

/-! ## Main theorems -/

/-- **Permutation Square-Sum Identity (proper fractions, computational, p <= 29).**
    For all primes p in {5, ..., 29}:
      Sigma_{a<b, (a,b) in F_{p-1}} (a/b) * delta(a/b)
        = (1/2) * Sigma_{a<b} delta(a/b)^2. -/
theorem perm_identity_proper_le_29' :
    ∀ p ∈ Finset.filter Nat.Prime (Finset.Icc 5 29),
      valueTimesShiftProper p = shiftSquaredSumProper p / 2 := by
  native_decide

/-! ## Helper lemmas for the main identity -/

lemma shiftFun_as_sub (p a b : ℕ) (hb : 0 < b) (hab : a < b) :
    shiftFun p ((a : ℚ) / b) = (a : ℚ) / b - (a * p % b : ℕ) / (b : ℚ) := by
  rw [shiftFun];
  field_simp;
  norm_num [ Int.fract_eq_iff ];
  rw [ Int.fract ];
  rw [ mul_sub, mul_div_cancel₀ _ ( by positivity ) ];
  rw [ sub_eq_iff_eq_add' ] ; norm_cast ; norm_num [ Nat.mod_add_div ];
  exact mod_cast by rw [ Nat.div_add_mod ] ;

lemma summand_eq (p a b : ℕ) (hb : 0 < b) (hab : a < b) :
    ((a : ℚ) / b) * shiftFun p ((a : ℚ) / b) -
      (shiftFun p ((a : ℚ) / b)) ^ 2 / 2 =
    (((a : ℚ) / b) ^ 2 - (((a * p % b : ℕ) : ℚ) / b) ^ 2) / 2 := by
  rw [ show shiftFun p ( a / b : ℚ ) = a / b - ( a * p % b : ℕ ) / b from ?_ ] ; ring;
  convert shiftFun_as_sub p a b hb hab using 1

lemma farey_perm_mem (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (ab : ℕ × ℕ) (hab : ab ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2)) :
    (ab.1 * p % ab.2, ab.2) ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2) := by
  unfold fareySet at *;
  norm_num +zetaDelta at *;
  refine' ⟨ ⟨ ⟨ _, _ ⟩, _, _, _ ⟩, _ ⟩;
  any_goals linarith [ Nat.mod_lt ( ab.1 * p ) ( by linarith : 0 < ab.2 ) ];
  exact Nat.Coprime.mul_left hab.1.2.2.2 ( hp.coprime_iff_not_dvd.mpr <| Nat.not_dvd_of_pos_of_lt hab.1.2.1 <| by omega )

lemma farey_perm_injective (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    ∀ a₁ ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2),
    ∀ a₂ ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2),
    (a₁.1 * p % a₁.2, a₁.2) = (a₂.1 * p % a₂.2, a₂.2) → a₁ = a₂ := by
  simp +zetaDelta at *;
  intros a b ha hb c d hc hd h_mod hb_eq
  have h_congr : a * p ≡ c * p [MOD b] := by
    aesop
  have h_cancel : a ≡ c [MOD b] := by
    rw [ Nat.modEq_iff_dvd ] at *;
    have h_coprime : Nat.Coprime p b := by
      exact hp.coprime_iff_not_dvd.mpr fun h => by have := Nat.le_of_dvd ( Nat.pos_of_ne_zero ( by aesop_cat ) ) h; linarith [ Finset.mem_filter.mp ha, Nat.sub_add_cancel hp.pos, Finset.mem_range.mp ( Finset.mem_product.mp ( Finset.mem_filter.mp ha |>.1 ) |>.2 ) ] ;
    exact Int.dvd_of_dvd_mul_left_of_gcd_one ( by simpa [ sub_mul ] using h_congr ) ( by simpa [ Int.gcd_natCast_natCast ] using h_coprime.symm )
  have h_eq : a = c := by
    rw [ Nat.ModEq, Nat.mod_eq_of_lt, Nat.mod_eq_of_lt ] at h_cancel <;> aesop
  exact ⟨h_eq, hb_eq⟩

lemma sq_sum_perm_invariant (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2),
      (((ab.1 * p % ab.2 : ℕ) : ℚ) / ab.2) ^ 2 =
    ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2),
      ((ab.1 : ℚ) / ab.2) ^ 2 := by
  have h_perm : Finset.filter (fun ab => ab.1 < ab.2) (fareySet (p - 1)) = Finset.image (fun ab => (ab.1 * p % ab.2, ab.2)) (Finset.filter (fun ab => ab.1 < ab.2) (fareySet (p - 1))) := by
    have h_perm : Finset.card (Finset.filter (fun ab => ab.1 < ab.2) (fareySet (p - 1))) = Finset.card (Finset.image (fun ab => (ab.1 * p % ab.2, ab.2)) (Finset.filter (fun ab => ab.1 < ab.2) (fareySet (p - 1)))) := by
      rw [ Finset.card_image_of_injOn ];
      intros ab₁ hab₁ ab₂ hab₂ h_eq; have := farey_perm_injective p hp hp5 ab₁ hab₁ ab₂ hab₂; aesop;
    rw [ Finset.eq_of_subset_of_card_le ( Finset.image_subset_iff.mpr fun x hx => show ( x.1 * p % x.2, x.2 ) ∈ { ab ∈ fareySet ( p - 1 ) | ab.1 < ab.2 } from ?_ ) ] ; aesop;
    convert farey_perm_mem p hp hp5 x hx using 1;
  conv_rhs => rw [ h_perm, Finset.sum_image ( fun x hx y hy hxy => farey_perm_injective p hp hp5 x hx y hy hxy ) ] ;

lemma diff_sq_sum_eq_zero (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2),
      (((ab.1 : ℚ) / ab.2) ^ 2 - (((ab.1 * p % ab.2 : ℕ) : ℚ) / ab.2) ^ 2) = 0 := by
  have := sq_sum_perm_invariant p hp hp5;
  simp_all +decide [ sub_eq_zero ]

/-- **Permutation Square-Sum Identity (proper fractions, general statement).**
    For prime p >= 5:
      Sigma_{(a,b) in fareySet(p-1), a<b} (a/b) * shiftFun(p, a/b)
        = shiftSquaredSumProper(p) / 2.

    Proof sketch:
    1. By algebraic_identity, each summand f * delta(f) - delta(f)^2 / 2
       equals (f^2 - {pf}^2) / 2.
    2. Grouping by denominator b, each group sums to 0 by per_denom_cancel.
    3. Therefore Sigma (f * delta) = Sigma delta^2 / 2. -/
theorem perm_square_sum_identity_proper (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    valueTimesShiftProper p = shiftSquaredSumProper p / 2 := by
  suffices h : valueTimesShiftProper p - shiftSquaredSumProper p / 2 = 0 by linarith
  unfold valueTimesShiftProper shiftSquaredSumProper
  rw [Finset.sum_div, ← Finset.sum_sub_distrib]
  have hcongr : ∀ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.1 < ab.2),
      ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2) -
        (shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2 / 2 =
      (((ab.1 : ℚ) / ab.2) ^ 2 - (((ab.1 * p % ab.2 : ℕ) : ℚ) / ab.2) ^ 2) / 2 := by
    intro ab hab
    simp only [Finset.mem_filter] at hab
    exact summand_eq p ab.1 ab.2 (by simp [fareySet] at hab; omega) hab.2
  rw [Finset.sum_congr rfl hcongr, ← Finset.sum_div, diff_sq_sum_eq_zero p hp hp5, zero_div]

/-- **Corrected full-sum identity (general statement).**
    For prime p >= 5:
      Sigma_{(a,b) in fareySet(p-1)} (a/b) * shiftFun(p, a/b)
        = shiftSquaredSum(p) / 2 + 1/2.

    The correction term 1/2 comes from f = 1: shiftFun(p, 1) = 1,
    so f * delta(1) = 1 but delta(1)^2/2 = 1/2, contributing an extra 1/2. -/
theorem perm_square_sum_identity_full (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    valueTimesShift p = shiftSquaredSum p / 2 + 1 / 2 := by
  have h1 : valueTimesShiftProper p = shiftSquaredSumProper p / 2 :=
    perm_square_sum_identity_proper p hp hp5
  rw [ show valueTimesShift p = valueTimesShiftProper p + shiftFun p 1 from ?_, h1 ];
  · unfold shiftSquaredSumProper;
    unfold shiftSquaredSum; unfold shiftFun; norm_num;
    rw [ show ( fareySet ( p - 1 ) ) = ( fareySet ( p - 1 ) |> Finset.filter fun ab => ab.1 < ab.2 ) ∪ { ( 1, 1 ) } from ?_, Finset.sum_union ] <;> norm_num ; ring;
    · simp +decide [ mul_assoc, mul_comm, mul_left_comm ];
      congr! 1;
      grind;
    · ext ⟨a, b⟩; simp [fareySet];
      grind +ring;
  · unfold valueTimesShift valueTimesShiftProper shiftFun;
    rw [ Finset.sum_eq_sum_diff_singleton_add ( show ( 1, 1 ) ∈ fareySet ( p - 1 ) from ?_ ) ];
    · rw [ Finset.sdiff_singleton_eq_erase ];
      rw [ show ( fareySet ( p - 1 ) ).erase ( 1, 1 ) = ( fareySet ( p - 1 ) |> Finset.filter fun ab => ab.1 < ab.2 ) from ?_ ] ; norm_num;
      ext ⟨a, b⟩; simp [fareySet];
      grind +ring;
    · exact Finset.mem_filter.mpr ⟨ Finset.mem_product.mpr ⟨ Finset.mem_range.mpr ( by omega ), Finset.mem_range.mpr ( by omega ) ⟩, by norm_num, by norm_num, by norm_num ⟩

/-! ## Relationship to ShiftSquaredSum -/

/-- The proper-fractions shift-squared sum differs from shiftSquaredSum by
    the f=0 and f=1 terms. Since shiftFun(p, 0) = 0 and shiftFun(p, 1) = 1:
    shiftSquaredSum(p) = shiftSquaredSumProper(p) + 1.

    (The (0,1) term contributes 0^2 = 0, and the (1,1) term contributes 1^2 = 1.) -/
theorem shiftSquaredSum_eq_proper_plus_one (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    shiftSquaredSum p = shiftSquaredSumProper p + 1 := by
  unfold shiftSquaredSum shiftSquaredSumProper shiftFun;
  rw [ show ( fareySet ( p - 1 ) ) = ( fareySet ( p - 1 ) |> Finset.filter fun x ↦ x.1 < x.2 ) ∪ { ( 1, 1 ) } from ?_, Finset.sum_union ] <;> norm_num;
  · rw [ Finset.sum_filter, Finset.sum_filter ];
    rw [ Finset.sum_insert, Finset.sum_filter ] ; aesop;
    grind;
  · ext ⟨a, b⟩; simp [fareySet];
    grind

/-- Computational check: shiftSquaredSum = shiftSquaredSumProper + 1 for p = 5. -/
theorem shiftSquaredSum_proper_5 :
    shiftSquaredSum 5 = shiftSquaredSumProper 5 + 1 := by native_decide

/-- Computational check: shiftSquaredSum = shiftSquaredSumProper + 1 for p = 7. -/
theorem shiftSquaredSum_proper_7 :
    shiftSquaredSum 7 = shiftSquaredSumProper 7 + 1 := by native_decide

/-- Computational check: shiftSquaredSum = shiftSquaredSumProper + 1 for p = 13. -/
theorem shiftSquaredSum_proper_13 :
    shiftSquaredSum 13 = shiftSquaredSumProper 13 + 1 := by native_decide

/-- Batch verification: shiftSquaredSum = shiftSquaredSumProper + 1 for primes
    5 <= p <= 29. -/
theorem shiftSquaredSum_proper_le_29 :
    ∀ p ∈ Finset.filter Nat.Prime (Finset.Icc 5 29),
      shiftSquaredSum p = shiftSquaredSumProper p + 1 := by
  native_decide

/-! ## Extended computational verification -/

/-- Batch verification: the proper-fractions identity holds for all primes
    5 <= p <= 43. -/
theorem perm_identity_proper_le_43 :
    ∀ p ∈ Finset.filter Nat.Prime (Finset.Icc 5 43),
      valueTimesShiftProper p = shiftSquaredSumProper p / 2 := by
  native_decide

/-- Batch verification: the corrected full-sum identity holds for all primes
    5 <= p <= 43. -/
theorem perm_identity_full_le_43 :
    ∀ p ∈ Finset.filter Nat.Prime (Finset.Icc 5 43),
      valueTimesShift p = shiftSquaredSum p / 2 + 1 / 2 := by
  native_decide

/-! ## Connection to the cross term B

The cross term B = 2 * Sigma D * delta. The displacement D(f) can be decomposed
as D(f) = (rank - |F_N|*f), so:
  B = 2 * Sigma D * delta
    = 2 * Sigma (D - f) * delta + 2 * Sigma f * delta  [adding and subtracting]

Wait -- this is not right since D already involves f. Instead, note that:
  B = 2 * Sigma D * delta
and the permutation identity gives us:
  2 * Sigma f * delta = shiftSquaredSum + 1  (over the full Farey set)

The quantity Sigma f * delta is NOT the same as B (which uses D, not f).
However, the identity constrains the "value-weighted" shift sum, which is
a useful structural fact about the shift function. -/

/-- The permutation identity implies: over proper fractions,
    2 * valueTimesShiftProper = shiftSquaredSumProper. -/
theorem double_valueTimesShift_eq (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    2 * valueTimesShiftProper p = shiftSquaredSumProper p := by
  have h := perm_square_sum_identity_proper p hp hp5
  linarith
