import Mathlib
import RequestProject.PrimeCircle

/-!
# The Displacement-Shift Identity

When adding a prime p to the Farey sequence F_{p-1} to get F_p, the displacement
of each old fraction f ≠ 1 changes by exactly the shift function δ(f) = f - {pf}:

  D_p(f) = D_{p-1}(f) + δ(f)

where D_N(f) = rank(f, F_N) - |F_N| · f.

## Proof outline

1. |F_p| = |F_{p-1}| + (p-1), since φ(p) = p-1 for prime p.
2. rank(f, F_p) = rank(f, F_{p-1}) + ⌊pf⌋, because exactly ⌊pf⌋ of the new
   fractions k/p (k = 1, ..., p-1) satisfy k/p ≤ f when f < 1.
3. Algebra: D_p(f) = D_{p-1}(f) + (⌊pf⌋ - (p-1)f) = D_{p-1}(f) + (f - {pf}).
-/

open Finset

/-! ## Core definitions -/

/-- Rank of f in the Farey sequence of order N: the number of Farey fractions ≤ f. -/
def fareyRank (N : ℕ) (f : ℚ) : ℕ :=
  ((fareySet N).filter (fun p => (p.1 : ℚ) / p.2 ≤ f)).card

/-- Displacement of f in the Farey sequence of order N: rank(f) - |F_N| · f. -/
def displacement (N : ℕ) (f : ℚ) : ℚ :=
  (fareyRank N f : ℚ) - (fareySet N).card * f

/-- Shift function δ_p(f) = f - {pf}, where {·} is the fractional part. -/
def shiftFun (p : ℕ) (f : ℚ) : ℚ :=
  f - Int.fract ((p : ℚ) * f)

/-! ## Computational verification for p = 2, 3, 5 -/

/-- The identity holds for all f ≠ 1 in F₁ when p = 2. -/
theorem displacement_shift_p2 :
    ∀ ab ∈ fareySet 1, ab.1 < ab.2 →
      displacement 2 ((ab.1 : ℚ) / ab.2) =
        displacement 1 ((ab.1 : ℚ) / ab.2) + shiftFun 2 ((ab.1 : ℚ) / ab.2) := by
  native_decide

/-- The identity holds for all f ≠ 1 in F₂ when p = 3. -/
theorem displacement_shift_p3 :
    ∀ ab ∈ fareySet 2, ab.1 < ab.2 →
      displacement 3 ((ab.1 : ℚ) / ab.2) =
        displacement 2 ((ab.1 : ℚ) / ab.2) + shiftFun 3 ((ab.1 : ℚ) / ab.2) := by
  native_decide

/-- The identity holds for all f ≠ 1 in F₄ when p = 5. -/
theorem displacement_shift_p5 :
    ∀ ab ∈ fareySet 4, ab.1 < ab.2 →
      displacement 5 ((ab.1 : ℚ) / ab.2) =
        displacement 4 ((ab.1 : ℚ) / ab.2) + shiftFun 5 ((ab.1 : ℚ) / ab.2) := by
  native_decide

/-! ## Algebraic identity -/

/-- The shift function equals ⌊pf⌋ - (p-1)f: this is the key algebraic rearrangement. -/
lemma shiftFun_eq_floor_sub (p : ℕ) (f : ℚ) :
    shiftFun p f = (⌊(p : ℚ) * f⌋ : ℚ) - ((p : ℚ) - 1) * f := by
  simp only [shiftFun, Int.fract]
  ring

/-! ## Structural lemmas about Farey sets -/

/-- For N ≥ 2, the Farey set decomposes as F_N = F_{N-1} ∪ newFractions(N). -/
lemma fareySet_eq_union (N : ℕ) (hN : 2 ≤ N) :
    fareySet N = fareySet (N - 1) ∪ fareyNew N := by
  ext ⟨a, b⟩; simp [fareySet, fareyNew]
  grind +ring

/-- The old and new Farey fractions are disjoint. -/
lemma fareySet_new_disjoint (N : ℕ) (hN : 2 ≤ N) :
    Disjoint (fareySet (N - 1)) (fareyNew N) := by
  unfold fareySet fareyNew; simp +decide [Finset.disjoint_left]
  intros; omega

/-- For prime p, |F_p| = |F_{p-1}| + (p - 1). -/
lemma fareySet_prime_card (p : ℕ) (hp : Nat.Prime p) :
    (fareySet p).card = (fareySet (p - 1)).card + (p - 1) := by
  rw [farey_new_fractions_count p hp.two_le, Nat.totient_prime hp]

/-! ## Counting new fractions -/

/-- The floor of p·a/b is non-negative for natural numbers p, a, b with b > 0. -/
lemma floor_pa_div_b_nonneg (p a b : ℕ) (hb : 0 < b) :
    0 ≤ ⌊(p : ℚ) * a / b⌋ := by
  positivity

/-- The number of new fractions k/p (for k = 1, ..., p-1) satisfying k/p ≤ a/b
    equals ⌊pa/b⌋, when 0 ≤ a < b < p and p is prime. -/
lemma new_fractions_count (p a b : ℕ) (hp : Nat.Prime p)
    (hb : 0 < b) (hbp : b < p) (hab : a < b) :
    ((fareyNew p).filter (fun x => (x.1 : ℚ) / x.2 ≤ (a : ℚ) / b)).card =
      (⌊(p : ℚ) * a / b⌋).toNat := by
  convert Finset.card_eq_sum_ones
    (Finset.Icc 1 (⌊(p : ℚ) * (a : ℚ) / (b : ℚ)⌋.toNat)) using 1
  · have h_set_eq : {x ∈ fareyNew p | (x.1 : ℚ) / (x.2 : ℚ) ≤ (a : ℚ) / (b : ℚ)} =
        Finset.image (fun k => (k, p))
          (Finset.Icc 1 (⌊(p : ℚ) * (a : ℚ) / (b : ℚ)⌋.toNat)) := by
      ext ⟨x, y⟩; simp [fareyNew]
      constructor <;> intro h <;> simp_all +decide [div_le_div_iff₀, Nat.cast_pos]
      · rw [div_le_div_iff₀] at h <;> norm_cast at * <;> try linarith
        exact ⟨Nat.pos_of_ne_zero (by aesop_cat),
          by rw [Nat.le_div_iff_mul_le hb]; linarith⟩
      · have h_x_lt_p : x < p := by
          refine lt_of_le_of_lt h.1.2 ?_
          rw [← Int.ofNat_lt,
            Int.toNat_of_nonneg (Int.floor_nonneg.mpr <| by positivity)]
          exact Int.floor_lt.mpr <| by
            rw [div_lt_iff₀ <| by positivity]; norm_cast; nlinarith
        field_simp
        exact ⟨⟨by linarith,
          Nat.Coprime.symm <| hp.coprime_iff_not_dvd.mpr <|
            Nat.not_dvd_of_pos_of_lt h.1.1 <| by linarith⟩,
          by rw [div_le_iff₀ <| Nat.cast_pos.mpr hp.pos]
             have := Nat.floor_le (show 0 ≤ (p : ℚ) * a / b by positivity)
             rw [le_div_iff₀ <| Nat.cast_pos.mpr hb] at this
             norm_cast at *; nlinarith⟩
    rw [h_set_eq, Finset.card_image_of_injective]; aesop_cat
  · norm_num

/-! ## Rank step -/

/-- The rank of f in F_p equals the rank in F_{p-1} plus ⌊pf⌋, for f < 1
    with denominator < p (the ⌊pf⌋ new fractions k/p lie below f). -/
lemma fareyRank_step (p a b : ℕ) (hp : Nat.Prime p)
    (hb : 0 < b) (hbp : b < p) (hab : a < b) :
    fareyRank p ((a : ℚ) / b) =
      fareyRank (p - 1) ((a : ℚ) / b) + (⌊(p : ℚ) * a / b⌋).toNat := by
  have h_union := fareySet_eq_union p hp.two_le
  have h_disjoint := fareySet_new_disjoint p hp.two_le
  have h_filter : (fareySet p).filter (fun p => (p.1 : ℚ) / p.2 ≤ (a : ℚ) / b) =
      (fareySet (p - 1)).filter (fun p => (p.1 : ℚ) / p.2 ≤ (a : ℚ) / b) ∪
      (fareyNew p).filter (fun p => (p.1 : ℚ) / p.2 ≤ (a : ℚ) / b) := by
    rw [h_union, Finset.filter_union]
  have h_card : ((fareySet p).filter (fun p => (p.1 : ℚ) / p.2 ≤ (a : ℚ) / b)).card =
      ((fareySet (p - 1)).filter (fun p => (p.1 : ℚ) / p.2 ≤ (a : ℚ) / b)).card +
      ((fareyNew p).filter (fun p => (p.1 : ℚ) / p.2 ≤ (a : ℚ) / b)).card := by
    rw [h_filter, Finset.card_union_of_disjoint]
    exact Disjoint.mono (Finset.filter_subset _ _) (Finset.filter_subset _ _) h_disjoint
  have h_new : ((fareyNew p).filter (fun p => (p.1 : ℚ) / p.2 ≤ (a : ℚ) / b)).card =
      (⌊(p : ℚ) * a / b⌋).toNat :=
    new_fractions_count p a b hp hb hbp hab
  convert h_card.trans (congr_arg₂ _ rfl h_new) using 1

/-! ## Main theorem -/

/-- **Displacement-Shift Identity.** For prime p and f = a/b with gcd(a,b) = 1,
    b < p, and f < 1, the displacement shifts by exactly δ_p(f) = f - {pf}:
    D_p(f) = D_{p-1}(f) + δ_p(f). -/
theorem displacement_shift (p a b : ℕ) (hp : Nat.Prime p)
    (_hcop : Nat.Coprime a b) (hb : 0 < b) (hbp : b < p) (hlt : a < b) :
    displacement p ((a : ℚ) / b) =
      displacement (p - 1) ((a : ℚ) / b) + shiftFun p ((a : ℚ) / b) := by
  unfold displacement
  rw [fareyRank_step, fareySet_prime_card]
  all_goals norm_num [shiftFun_eq_floor_sub]
  any_goals assumption
  rw [Nat.cast_sub hp.pos]; ring
  rw [← Int.toNat_of_nonneg (Int.floor_nonneg.mpr (by positivity))]; norm_cast

/-- **Boundary case.** For f = 1, D_p(1) = D_{p-1}(1) + δ_p(1) - 1.
    The correction of -1 arises because ⌊p · 1⌋ = p but only p-1 new fractions
    k/p are strictly less than 1. -/
theorem displacement_shift_boundary (p : ℕ) (_hp : Nat.Prime p) :
    displacement p 1 = displacement (p - 1) 1 + shiftFun p 1 - 1 := by
  have h_rank : fareyRank p 1 = (fareySet p).card ∧
      fareyRank (p - 1) 1 = (fareySet (p - 1)).card := by
    constructor <;> rw [fareyRank]
    · rw [Finset.filter_true_of_mem]
      exact fun x hx =>
        div_le_one_of_le₀ (mod_cast (Finset.mem_filter.mp hx) |>.2.2.1) (Nat.cast_nonneg _)
    · refine congr_arg Finset.card (Finset.filter_true_of_mem
        fun x hx => div_le_one_of_le₀ ?_ (Nat.cast_nonneg _))
      unfold fareySet at hx; aesop
  unfold displacement shiftFun; aesop
