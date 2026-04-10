import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DisplacementShift
import RequestProject.BridgeIdentity

/-!
# Strict Positivity of the Shift-Squared Sum

For any prime p ≥ 5, the sum Σ_{f ∈ F_{p-1}} δ(f)² > 0, where
δ(f) = f - {pf} is the shift function from `DisplacementShift.lean`.

## Proof Strategy (Rearrangement Inequality)

1. For denominator b with gcd(b,p)=1, define the twisted sum
   T_b = Σ_{a coprime b} a · (pa mod b).

2. Multiplication by p permutes the coprime residues mod b
   (`coprime_mul_perm` from `BridgeIdentity.lean`).

3. By the rearrangement inequality: Σ xᵢ · x_{σ(i)} ≤ Σ xᵢ²
   with equality iff σ is the identity on sorted elements.

4. Σ δ² = 2 · Σ_{b=2}^{p-1} (Σa² - T_b)/b² ≥ 0.

5. For p ≥ 5 prime, at least one b gives T_b < Σa², yielding strict positivity.

## Computational Verification

We verify the result for p = 5, 7, 11, 13 using `native_decide`.
-/

open Finset BigOperators

/-! ## The shift-squared sum -/

/-- The shift-squared sum: Σ_{(a,b) ∈ fareySet(p-1)} (shiftFun p (a/b))². -/
def shiftSquaredSum (p : ℕ) : ℚ :=
  ∑ ab ∈ fareySet (p - 1), (shiftFun p ((ab.1 : ℚ) / ab.2)) ^ 2

/-- The twisted product sum T_b = Σ_{a coprime to b, 0 ≤ a < b} a · (a * p % b). -/
def twistedSum (b p : ℕ) : ℕ :=
  ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b), a * (a * p % b)

/-- The sum of squares of coprime residues mod b: Σ_{a coprime to b, 0 ≤ a < b} a². -/
def coprimeSquareSum (b : ℕ) : ℕ :=
  ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b), a ^ 2

/-! ## Computational verification for small primes -/

/-- Strict positivity of the shift-squared sum for p = 5. -/
theorem shiftSquaredSum_pos_5 : shiftSquaredSum 5 > 0 := by native_decide

/-- Strict positivity of the shift-squared sum for p = 7. -/
theorem shiftSquaredSum_pos_7 : shiftSquaredSum 7 > 0 := by native_decide

/-- Strict positivity of the shift-squared sum for p = 11. -/
theorem shiftSquaredSum_pos_11 : shiftSquaredSum 11 > 0 := by native_decide

/-- Strict positivity of the shift-squared sum for p = 13. -/
theorem shiftSquaredSum_pos_13 : shiftSquaredSum 13 > 0 := by native_decide

/-! ## Rearrangement inequality components -/

/-- The twisted sum T_b uses a permutation of coprime residues (from `coprime_mul_perm`).
    When p is coprime to b, multiplication by p permutes {a : gcd(a,b) = 1, a < b}. -/
lemma twistedSum_uses_perm (b p : ℕ) (hb : 0 < b) (hcop : Nat.Coprime p b) :
    (Finset.filter (fun a => Nat.Coprime a b) (Finset.range b)).image
      (fun a => a * p % b) =
    Finset.filter (fun a => Nat.Coprime a b) (Finset.range b) :=
  coprime_mul_perm b p hb hcop

/-
PROBLEM
The twisted sum T_b ≤ Σ a² (sum of squares of coprime residues).
    Follows from Σ(a - σ(a))² ≥ 0 and the permutation property.

PROVIDED SOLUTION
Use Σ(a - σ(a))² ≥ 0 where σ(a) = a*p%b. Expand: Σ(a-σ(a))² = Σa² - 2·Σ a·σ(a) + Σσ(a)². Since σ is a permutation of the set (by coprime_mul_perm), Σσ(a)² = Σa². So Σ(a-σ(a))² = 2·Σa² - 2·T_b ≥ 0, giving T_b ≤ Σa².

Concretely: cast to ℤ. Show 2 * twistedSum b p ≤ 2 * coprimeSquareSum b. This is 2·Σ a·(a*p%b) ≤ Σa² + Σ(a*p%b)². The latter equals 2·Σa² by the permutation. And 2·a·σ(a) ≤ a² + σ(a)² by AM-GM (i.e., (a-σ(a))² ≥ 0).
-/
lemma twistedSum_le_squareSum (b p : ℕ) (hb : 0 < b) (hcop : Nat.Coprime p b) :
    twistedSum b p ≤ coprimeSquareSum b := by
      -- By the permutation property, we have that $\sum_{a \in \text{coprime}(b)} a \cdot \sigma(a) \leq \frac{1}{2} \sum_{a \in \text{coprime}(b)} a^2 + \frac{1}{2} \sum_{a \in \text{coprime}(b)} \sigma(a)^2$.
      have h_perm : ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), a * (a * p % b) ≤ (∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), a^2 + ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), (a * p % b)^2) / 2 := by
        rw [ ← Finset.sum_add_distrib, Nat.le_div_iff_mul_le ] <;> norm_num [ Finset.sum_mul _ _ _ ];
        exact Finset.sum_le_sum fun x hx => by linarith [ sq_nonneg ( x - ( x * p % b ) : ℤ ) ] ;
      -- Since σ(a) is a permutation of the set, we have $\sum_{a \in \text{coprime}(b)} \sigma(a)^2 = \sum_{a \in \text{coprime}(b)} a^2$.
      have h_perm_sq : ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), (a * p % b)^2 = ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), a^2 := by
        have h_perm_sq : Finset.image (fun a => a * p % b) (Finset.filter (fun a => Nat.Coprime a b) (Finset.range b)) = Finset.filter (fun a => Nat.Coprime a b) (Finset.range b) := by
          exact?;
        conv_rhs => rw [ ← h_perm_sq, Finset.sum_image ( Finset.card_image_iff.mp <| by aesop ) ] ;
      convert h_perm using 1 ; ring;
      exact Eq.symm ( Nat.div_eq_of_eq_mul_left zero_lt_two ( by linarith! [ show coprimeSquareSum b = ∑ x ∈ Finset.filter ( fun x => Nat.Coprime x b ) ( Finset.range b ), x ^ 2 from rfl ] ) )

/-
PROBLEM
When the permutation a ↦ a*p % b moves at least one element,
    we get strict inequality: T_b < Σa². This follows from
    Σ(a - σ(a))² = 2(Σa² - T_b) > 0.

PROVIDED SOLUTION
Similar to twistedSum_le_squareSum but strict. We have Σ(a - σ(a))² = 2(Σa² - T_b). The term (a₀ - σ(a₀))² > 0 since a₀ ≠ σ(a₀), and all other terms ≥ 0. So Σ(a - σ(a))² > 0, giving 2(Σa² - T_b) > 0, i.e., T_b < Σa².

Cast everything to ℤ. Show:
1. Σ_{a∈S} (a - a*p%b)² > 0 because the a₀ term is positive.
2. Σ_{a∈S} (a - a*p%b)² = 2·Σa² - 2·T_b (using Σ(a*p%b)² = Σa² by permutation).
3. Conclude 2·T_b < 2·Σa² and divide by 2.

For step 2, use coprime_mul_perm to show the image equals the original set, then sum_image with injectivity to show Σ(a*p%b)² = Σa².
-/
lemma twistedSum_lt_of_moved (b p : ℕ) (hb : 0 < b) (hcop : Nat.Coprime p b)
    (a₀ : ℕ) (ha₀_mem : a₀ ∈ (Finset.range b).filter (fun a => Nat.Coprime a b))
    (ha₀_moved : a₀ * p % b ≠ a₀) :
    twistedSum b p < coprimeSquareSum b := by
      -- Let's rewrite the sum $\sum_{a \in S} (a - a * p \% b)^2$ using the identity $a^2 + b^2 - 2ab = (a - b)^2$.
      have h_sum_sq_rewrite : ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), (a - (a * p % b) : ℤ) ^ 2 = 2 * (∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), a ^ 2 : ℤ) - 2 * (∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), a * (a * p % b) : ℤ) := by
        have h_sum_sq_rewrite : ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), (a * p % b : ℤ) ^ 2 = ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), a ^ 2 := by
          have h_sum_sq_rewrite : Finset.image (fun a => a * p % b) (Finset.filter (fun a => Nat.Coprime a b) (Finset.range b)) = Finset.filter (fun a => Nat.Coprime a b) (Finset.range b) := by
            apply coprime_mul_perm b p hb hcop;
          conv_rhs => rw [ ← h_sum_sq_rewrite, Finset.sum_image ( Finset.card_image_iff.mp <| by aesop ) ] ; norm_cast;
          norm_num;
        simp_all +decide [ sub_sq, Finset.sum_add_distrib, Finset.mul_sum _ _ _ ] ; ring;
        simp +decide only [mul_comm, mul_assoc];
        rw [ Finset.mul_sum _ _ _ ];
      -- Since there's at least one term where $a \neq a * p \% b$, we have $\sum_{a \in S} (a - a * p \% b)^2 > 0$.
      have h_sum_sq_pos : ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), (a - (a * p % b) : ℤ) ^ 2 > 0 := by
        rw [ Finset.sum_eq_add_sum_diff_singleton ha₀_mem ];
        exact add_pos_of_pos_of_nonneg ( sq_pos_of_ne_zero ( sub_ne_zero_of_ne <| mod_cast Ne.symm ha₀_moved ) ) ( Finset.sum_nonneg fun _ _ => sq_nonneg _ );
      linarith! [ show ∑ a ∈ Finset.filter ( fun a => Nat.Coprime a b ) ( Finset.range b ), ( a : ℤ ) * ( a * p % b ) = twistedSum b p from mod_cast rfl, show ∑ a ∈ Finset.filter ( fun a => Nat.Coprime a b ) ( Finset.range b ), ( a : ℤ ) ^ 2 = coprimeSquareSum b from mod_cast rfl ] ;

/-- For p ≥ 5 prime, b = p-2 gives a non-identity permutation since
    1 * p % (p-2) = 2 ≠ 1 (when p-2 ≥ 3). -/
lemma exists_strict_ineq (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    ∃ b, 2 ≤ b ∧ b ≤ p - 1 ∧ Nat.Coprime p b ∧ twistedSum b p < coprimeSquareSum b := by
  refine ⟨p - 2, by omega, by omega, ?_, ?_⟩
  · exact (hp.coprime_iff_not_dvd).mpr (fun h => by have := Nat.le_of_dvd (by omega) h; omega)
  · refine twistedSum_lt_of_moved _ _ (by omega) ?_ 1 ?_ ?_
    · exact (hp.coprime_iff_not_dvd).mpr (fun h => by have := Nat.le_of_dvd (by omega) h; omega)
    · simp [Finset.mem_filter, Finset.mem_range]; omega
    · simp only [one_mul]
      rw [Nat.mod_eq_sub_mod (show p - 2 ≤ p by omega)]
      rw [show p - (p - 2) = 2 from by omega]
      rw [Nat.mod_eq_of_lt (show 2 < p - 2 by omega)]
      omega

/-! ## Main theorem: general strict positivity -/

/-- **Strict Positivity Theorem.** For any prime p ≥ 5, the shift-squared sum is
    strictly positive: Σ_{f ∈ F_{p-1}} δ(f)² > 0.

    Proof: the Farey fraction 1/(p-2) contributes δ = -1/(p-2) ≠ 0,
    so its square 1/(p-2)² > 0 is a positive term in a sum of nonneg terms. -/
theorem shiftSquaredSum_pos (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    shiftSquaredSum p > 0 := by
  refine lt_of_lt_of_le ?_ (Finset.single_le_sum
    (fun ab _ => sq_nonneg (shiftFun p ((ab.1 : ℚ) / ab.2)))
    (show (1, p - 2) ∈ fareySet (p - 1) from ?_))
  · -- Show (shiftFun p (1/(p-2)))² > 0
    unfold shiftFun; rcases p with (_ | _ | _ | p) <;> norm_num at *
    rw [Int.fract]; ring_nf; norm_num
    rcases p with (_ | _ | p) <;> norm_num at *
    field_simp
    rw [show ⌊((p : ℚ) + 1 + 1 + 3) / (1 + (p + 1 + 1))⌋ = 1 by
      exact Int.floor_eq_iff.mpr ⟨by norm_num; rw [le_div_iff₀] <;> linarith,
                                    by norm_num; rw [div_lt_iff₀] <;> linarith⟩]
    norm_num; nlinarith
  · -- Show (1, p-2) ∈ fareySet(p-1)
    rcases p with (_ | _ | _ | _ | p) <;> simp_all +arith +decide [fareySet]

/-! ## Nonnegativity (easier direction) -/

/-- Each term δ(f)² is nonneg, so the sum is nonneg. -/
lemma shiftSquaredSum_nonneg (p : ℕ) : shiftSquaredSum p ≥ 0 := by
  unfold shiftSquaredSum
  apply Finset.sum_nonneg
  intros
  positivity

/-! ## Auxiliary: the shift-squared sum decomposes by denominator -/

/-- The shift-squared sum decomposes as a sum over denominators b from 1 to p-1. -/
lemma shiftSquaredSum_by_denom (p : ℕ) (_hp : Nat.Prime p) :
    shiftSquaredSum p =
    ∑ b ∈ Finset.Icc 1 (p - 1),
      ∑ a ∈ (Finset.range (b + 1)).filter (fun a => Nat.Coprime a b),
        (shiftFun p ((a : ℚ) / b)) ^ 2 := by
  have fareySet_decomp : fareySet (p - 1) = Finset.biUnion (Finset.Icc 1 (p - 1))
      (fun b => Finset.image (fun a => (a, b))
        ((Finset.range (b + 1)).filter (fun a => Nat.Coprime a b))) := by
    ext ⟨a, b⟩; simp [fareySet]; grind
  unfold shiftSquaredSum; rw [fareySet_decomp]; erw [Finset.sum_biUnion]; aesop
  exact fun a ha b hb hab =>
    Finset.disjoint_left.mpr fun x hx₁ hx₂ => hab <| by aesop

/-! ## Key identity relating δ² to twisted sums

For each denominator b ≥ 2, the contribution to the shift-squared sum
from fractions with denominator b is:

  Σ_{a coprime b, 0 < a < b} (a/b - {pa/b})²
  = (1/b²) · Σ_{a coprime b} (a - (pa mod b))²
  = (1/b²) · (2·Σa² - 2·T_b)
  = (2/b²) · (coprimeSquareSum b - twistedSum b p)
-/

/-
PROBLEM
The shift function at a/b equals (a - (a*p mod b))/b for 0 ≤ a < b.

PROVIDED SOLUTION
shiftFun p (a/b) = a/b - Int.fract(p * a/b). We need Int.fract(p * (a:ℚ)/b) = (p*a % b : ℕ)/b. Use Int.fract_eq_iff or show directly that ⌊p*(a:ℚ)/b⌋ = (p*a/b : ℕ) (Euclidean division). Then Int.fract = p*a/b - ⌊p*a/b⌋ = p*a/b - (p*a÷b) = (p*a % b)/b. The key identity: p*a = b*(p*a÷b) + (p*a%b), so (p*a:ℚ)/b = (p*a÷b) + (p*a%b)/b, and the floor is p*a÷b. Then shiftFun = a/b - (p*a%b)/b = (a - p*a%b)/b. Note a*p%b = p*a%b by commutativity of multiplication.
-/
lemma shiftFun_rational (p a b : ℕ) (hb : 0 < b) (_hab : a < b) :
    shiftFun p ((a : ℚ) / b) = ((a : ℤ) - (a * p % b : ℕ)) / (b : ℚ) := by
      have h_frac : Int.fract ((p : ℚ) * (a : ℚ) / (b : ℚ)) = ((a * p) % b : ℕ) / (b : ℚ) := by
        rw [ Int.fract_eq_iff ];
        field_simp;
        norm_cast;
        exact ⟨ by norm_num, Nat.mod_lt _ hb, ⟨ a * p / b, by rw [ Int.subNatNat_eq_coe ] ; push_cast; linarith [ Nat.mod_add_div ( a * p ) b ] ⟩ ⟩;
      convert congr_arg ( fun x : ℚ => ( a : ℚ ) / b - x ) h_frac using 1 ; ring;
      · unfold shiftFun; ring;
      · norm_num [ sub_div ]