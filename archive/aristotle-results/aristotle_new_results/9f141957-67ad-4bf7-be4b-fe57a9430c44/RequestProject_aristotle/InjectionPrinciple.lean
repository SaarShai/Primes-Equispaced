import Mathlib
import PrimeCircle

/-!
# The Injection Principle for Farey Sequences

For any prime p ≥ 3, each gap between adjacent fractions in the Farey sequence F_{p-1}
contains at most one fraction k/p.

## Proof outline

The proof uses three key facts about adjacent fractions a/b, c/d in F_{p-1}:

1. **Mediant argument**: Adjacent fractions satisfy bc − ad = 1 and b + d ≥ p.
   If b + d ≤ p − 1, the mediant (a+c)/(b+d) would be a coprime fraction with
   denominator ≤ p − 1 lying strictly between a/b and c/d, contradicting adjacency.

2. **Product bound**: From b + d ≥ p with b, d ≥ 1, we get bd ≥ p − 1
   (since (b−1)(d−1) ≥ 0 gives bd + 1 ≥ b + d ≥ p).

3. **Counting argument**: Any valid k satisfies a·p·d < k·b·d < a·p·d + p
   (an interval of width p in ℕ), while consecutive valid k-values are spaced
   b·d ≥ p − 1 apart. A squeeze argument shows at most one k fits.
-/

open Finset Nat

/-! ## Section 1: Computational Verification for Small Primes -/

/-- Boolean check of the injection principle for a specific prime p.
    Verifies that for every pair (a/b, c/d) with bc = ad + 1, b + d ≥ p,
    b,d ∈ [1, p-1], gcd conditions, at most one k ∈ [1, p-1] satisfies
    a·p < k·b and k·d < c·p. -/
def injectionCheckBool (p : ℕ) : Bool :=
  (List.finRange p).all fun b =>
    (List.finRange p).all fun d =>
      (List.finRange p).all fun a =>
        (List.finRange p).all fun c =>
          if Nat.ble 1 b.val && Nat.ble 1 d.val &&
             Nat.beq (Nat.gcd a.val b.val) 1 &&
             Nat.beq (Nat.gcd c.val d.val) 1 &&
             Nat.beq (b.val * c.val) (a.val * d.val + 1) &&
             Nat.ble p (b.val + d.val)
          then
            (List.finRange p).all fun k₁ =>
              (List.finRange p).all fun k₂ =>
                !(Nat.ble 1 k₁.val &&
                  Nat.blt (a.val * p) (k₁.val * b.val) &&
                  Nat.blt (k₁.val * d.val) (c.val * p) &&
                  Nat.ble 1 k₂.val &&
                  Nat.blt (a.val * p) (k₂.val * b.val) &&
                  Nat.blt (k₂.val * d.val) (c.val * p)) ||
                Nat.beq k₁.val k₂.val
          else true

/-- Computational verification of the injection principle for p = 3. -/
theorem injection_check_3 : injectionCheckBool 3 = true := by native_decide

/-- Computational verification of the injection principle for p = 5. -/
theorem injection_check_5 : injectionCheckBool 5 = true := by native_decide

/-- Computational verification of the injection principle for p = 7. -/
theorem injection_check_7 : injectionCheckBool 7 = true := by native_decide

/-! ## Section 2: The Mediant Lemma -/

/-- The mediant (a+c)/(b+d) lies strictly between a/b and c/d when bc = ad + 1
    (expressed via cross-multiplication to avoid fractions).
    Both inequalities follow from the identity bc − ad = 1 applied to
    the cross-multiplied differences. -/
theorem mediant_strictly_between {a b c d : ℕ} (hb : 0 < b) (hd : 0 < d)
    (hdet : b * c = a * d + 1) :
    a * (b + d) < (a + c) * b ∧ (a + c) * d < c * (b + d) := by
  constructor <;> nlinarith

/-- If bc = ad + 1, then gcd(a+c, b+d) = 1, i.e., the mediant is in lowest terms.
    Any common factor g of (a+c) and (b+d) must divide b(a+c) − a(b+d) = bc − ad = 1. -/
theorem mediant_coprime {a b c d : ℕ} (hdet : b * c = a * d + 1) :
    Nat.Coprime (a + c) (b + d) := by
  by_contra h_not_coprime
  obtain ⟨p, hp_prime, hp_div_ac, hp_div_bd⟩ :
      ∃ p, Nat.Prime p ∧ p ∣ a + c ∧ p ∣ b + d :=
    Nat.Prime.not_coprime_iff_dvd.mp h_not_coprime
  obtain ⟨k₁, hk₁⟩ := hp_div_ac
  obtain ⟨k₂, hk₂⟩ := hp_div_bd
  simp_all +decide [Nat.prime_mul_iff]
  exact hp_prime.not_dvd_one <| by
    exact ⟨k₁ * b - k₂ * a, by
      rw [mul_tsub]
      exact eq_tsub_of_add_eq <| by nlinarith⟩

/-- Adjacent fractions in F_N must have b + d > N. If b + d ≤ N, the coprime mediant
    (a+c)/(b+d) would lie in F_N between them, contradicting adjacency.
    Here adjacency is expressed as: no fraction e/f with f ≤ N lies strictly between. -/
theorem farey_adjacent_sum_gt {N a b c d : ℕ} (hb : 0 < b) (hd : 0 < d)
    (hbN : b ≤ N) (hdN : d ≤ N)
    (hdet : b * c = a * d + 1)
    (hadj : ∀ e f : ℕ, 0 < f → f ≤ N → Nat.Coprime e f →
      ¬(a * f < e * b ∧ e * d < c * f)) :
    N < b + d := by
  exact not_le.mp fun contra =>
    hadj (a + c) (b + d) (by linarith) (by linarith) (mediant_coprime hdet)
      ⟨by nlinarith, by nlinarith⟩

/-! ## Section 3: Auxiliary Arithmetic Lemma -/

/-- Product bound: if b + d ≥ p and b, d ≥ 1, then bd + 1 ≥ p.
    Follows from (b−1)(d−1) ≥ 0, i.e., bd ≥ b + d − 1 ≥ p − 1. -/
theorem prod_ge_sum_pred {b d p : ℕ} (hb : 1 ≤ b) (hd : 1 ≤ d) (hsum : p ≤ b + d) :
    p ≤ b * d + 1 := by
  nlinarith [Nat.sub_add_cancel (by linarith : 1 ≤ b),
             Nat.sub_add_cancel (by linarith : 1 ≤ d)]

/-! ## Section 4: The Injection Principle -/

/-- Core arithmetic lemma: given bc = ad + 1 and b + d ≥ p with b, d ≥ 1,
    there is at most one natural number k satisfying a·p < k·b and k·d < c·p.

    **Proof**: From bc = ad + 1, multiplying by p gives c·p·b = a·p·d + p.
    For any valid k, multiplying a·p < k·b by d and k·d < c·p by b shows
    a·p·d < k·b·d < a·p·d + p. If two values k₁ ≠ k₂ existed, the spacing
    |k₂ − k₁|·b·d ≥ b·d ≥ p − 1 within an interval of width p yields
    a·p·d < k·(p−1) < a·p·d + 1, which is impossible for natural numbers. -/
theorem at_most_one_in_gap (p a b c d : ℕ) (hb : 1 ≤ b) (hd : 1 ≤ d)
    (hdet : b * c = a * d + 1) (hsum : p ≤ b + d) :
    ∀ k₁ k₂ : ℕ,
      a * p < k₁ * b → k₁ * d < c * p →
      a * p < k₂ * b → k₂ * d < c * p →
      k₁ = k₂ := by
  intro k₁ k₂ hk₁ hk₂ hk₃ hk₄
  have := prod_ge_sum_pred hb hd hsum
  nlinarith

/-- **The Injection Principle.** For any prime p ≥ 3, let a/b and c/d be adjacent
    fractions in the Farey sequence F_{p-1} (so bc − ad = 1, b,d ≤ p−1, and
    b + d ≥ p by the mediant property). Then at most one fraction k/p with
    1 ≤ k ≤ p − 1 lies strictly between a/b and c/d.

    This follows directly from `at_most_one_in_gap` since the condition
    a·p < k·b ∧ k·d < c·p is the cross-multiplied form of a/b < k/p < c/d. -/
theorem injection_principle (p : ℕ) (hp : Nat.Prime p) (hp3 : 3 ≤ p)
    (a b c d : ℕ) (hb : 1 ≤ b) (hd : 1 ≤ d)
    (hbN : b ≤ p - 1) (hdN : d ≤ p - 1)
    (hab : Nat.Coprime a b) (hcd : Nat.Coprime c d)
    (hdet : b * c = a * d + 1)
    (hsum : p ≤ b + d) :
    ∀ k₁ k₂ : ℕ, 1 ≤ k₁ → k₁ ≤ p - 1 → 1 ≤ k₂ → k₂ ≤ p - 1 →
      a * p < k₁ * b → k₁ * d < c * p →
      a * p < k₂ * b → k₂ * d < c * p →
      k₁ = k₂ :=
  fun k₁ k₂ _ _ _ _ h1 h2 h3 h4 =>
    at_most_one_in_gap p a b c d hb hd hdet hsum k₁ k₂ h1 h2 h3 h4
