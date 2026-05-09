import Mathlib
import InjectionPrinciple
import BridgeIdentity

/-!
# Sub-Gap Permutation and the Modular Inverse Map

For a prime p ≥ 3, define b_k = k⁻¹ mod p for k = 1, …, p−1.

## Main results

1. **Permutation**: The map k ↦ b_k is a permutation of {1, …, p−1}.
2. **Harmonic identity**: ∑_{k=1}^{p−1} 1/b_k = H(p−1) = ∑_{k=1}^{p−1} 1/k.
3. **Sub-gap formula**: When k/p sits in a Farey gap (a/b, c/d) of F_{p−1},
   the left sub-gap has width exactly 1/(p·b), where b = k⁻¹ mod p comes from
   the Farey neighbor relation k·b − p·a = 1.
-/

open Finset Nat BigOperators

/-! ## Section 1: Computational Verification for Small Primes -/

/-- Compute the modular inverse image of {1,...,p-1} as a sorted list. -/
def modInvImageSorted (p : ℕ) : List ℕ :=
  ((List.range (p - 1)).map (fun i =>
    ((((i + 1 : ℕ) : ZMod p)⁻¹).val))).mergeSort (· ≤ ·)

/-- Check that the modular-inverse map is a permutation of {1,...,p-1}. -/
def checkModInvPerm (p : ℕ) : Bool :=
  modInvImageSorted p == (List.range (p - 1)).map (· + 1)

/-- Check the sub-gap relation: for each k in {1,...,p-1}, k * (k⁻¹ mod p) ≡ 1 (mod p). -/
def checkSubGapRelation (p : ℕ) : Bool :=
  (List.range (p - 1)).all (fun i =>
    let k := i + 1
    let b := (((k : ZMod p)⁻¹).val)
    b ≥ 1 ∧ b ≤ p - 1 ∧ (k * b) % p == 1)

-- Computational verification for p = 3, 5, 7
example : checkModInvPerm 3 = true := by native_decide
example : checkModInvPerm 5 = true := by native_decide
example : checkModInvPerm 7 = true := by native_decide

example : checkSubGapRelation 3 = true := by native_decide
example : checkSubGapRelation 5 = true := by native_decide
example : checkSubGapRelation 7 = true := by native_decide

/-! ## Section 2: The Modular Inverse as a Permutation -/

/-- The unit-inverse map as a permutation of (ZMod p)ˣ. -/
noncomputable def modInvPerm (p : ℕ) [Fact (Nat.Prime p)] : Equiv.Perm (ZMod p)ˣ where
  toFun := fun u => u⁻¹
  invFun := fun u => u⁻¹
  left_inv := inv_inv
  right_inv := inv_inv

/-- The modular-inverse map k ↦ k⁻¹ is a bijection on (ZMod p)ˣ. -/
theorem modInv_bijective (p : ℕ) [Fact (Nat.Prime p)] :
    Function.Bijective (fun u : (ZMod p)ˣ => u⁻¹) :=
  (modInvPerm p).bijective

/-
PROBLEM
For prime p and 1 ≤ k ≤ p-1, (k : ZMod p) is a unit.

PROVIDED SOLUTION
k ∈ Icc 1 (p-1) means 1 ≤ k ≤ p-1 so k is not divisible by prime p. Hence (k : ZMod p) ≠ 0 and is a unit in the field ZMod p.
-/
lemma zmod_isUnit_of_mem_Icc {p : ℕ} (hp : Nat.Prime p) (k : ℕ)
    (hk : k ∈ Finset.Icc 1 (p - 1)) :
    IsUnit ((k : ZMod p)) := by
  haveI := Fact.mk hp; exact IsUnit.mk0 _ ( by rw [ Ne.eq_def, ZMod.natCast_eq_zero_iff ] ; exact Nat.not_dvd_of_pos_of_lt ( Finset.mem_Icc.mp hk |>.1 ) ( lt_of_le_of_lt ( Finset.mem_Icc.mp hk |>.2 ) ( Nat.pred_lt hp.ne_zero ) ) ) ;

/-
PROBLEM
For prime p, k⁻¹ mod p lies in {1, ..., p-1} when k ∈ {1, ..., p-1}.

PROVIDED SOLUTION
Since k ∈ Icc 1 (p-1), (k : ZMod p) is a unit (by zmod_isUnit_of_mem_Icc). Its inverse is also a unit, so (k : ZMod p)⁻¹ ≠ 0, which means its val ≥ 1. Also val < p so val ≤ p - 1. Hence val ∈ Icc 1 (p-1).
-/
lemma modInv_mem_Icc {p k : ℕ} (hp : Nat.Prime p) (hp3 : 3 ≤ p)
    (hk : k ∈ Finset.Icc 1 (p - 1)) :
    ((k : ZMod p)⁻¹).val ∈ Finset.Icc 1 (p - 1) := by
  haveI := Fact.mk hp; norm_num at hk ⊢;
  have h_inv_range : (k : ZMod p)⁻¹ ≠ 0 := by
    exact inv_ne_zero <| by rw [ Ne.eq_def, ZMod.natCast_eq_zero_iff ] ; exact Nat.not_dvd_of_pos_of_lt hk.1 <| lt_of_le_of_lt hk.2 <| Nat.pred_lt hp.ne_zero;
  exact ⟨ Nat.pos_of_ne_zero ( by simpa [ ZMod.val_eq_zero ] using h_inv_range ), Nat.le_pred_of_lt ( ZMod.val_lt _ ) ⟩

/-
PROBLEM
The modular-inverse map on {1,...,p-1} is injective.

PROVIDED SOLUTION
If ((a : ZMod p)⁻¹).val = ((b : ZMod p)⁻¹).val then (a : ZMod p)⁻¹ = (b : ZMod p)⁻¹ (by ZMod.val_injective). Then inverting both sides gives (a : ZMod p) = (b : ZMod p). Since a, b ∈ Icc 1 (p-1), both are < p, so ZMod.val_natCast gives a = b.
-/
lemma modInv_injective_on_Icc {p : ℕ} (hp : Nat.Prime p) (hp3 : 3 ≤ p) :
    Set.InjOn (fun k : ℕ => ((k : ZMod p)⁻¹).val) (Finset.Icc 1 (p - 1) : Set ℕ) := by
  intros a ha b hb hab
  have h_inv_eq : (a : ZMod p)⁻¹ = (b : ZMod p)⁻¹ := by
    haveI := Fact.mk hp; exact ZMod.val_injective p hab;
  have h_a_eq_b : (a : ZMod p) = (b : ZMod p) := by
    haveI := Fact.mk hp; aesop;
  have h_a_eq_b_nat : a = b := by
    exact Nat.mod_eq_of_lt ( show a < p from lt_of_le_of_lt ( Finset.mem_Icc.mp ha |>.2 ) ( Nat.pred_lt hp.ne_zero ) ) ▸ Nat.mod_eq_of_lt ( show b < p from lt_of_le_of_lt ( Finset.mem_Icc.mp hb |>.2 ) ( Nat.pred_lt hp.ne_zero ) ) ▸ by simpa [ ← ZMod.natCast_eq_natCast_iff' ] using h_a_eq_b;
  exact h_a_eq_b_nat

/-
PROBLEM
**Theorem 1 (Permutation)**: The map k ↦ k⁻¹ mod p is a permutation of {1,...,p-1}.
    This follows because modular inversion is a bijection on (ℤ/pℤ)*.

PROVIDED SOLUTION
Use modInv_injective_on_Icc and modInv_mem_Icc. The function maps Icc 1 (p-1) into itself (by modInv_mem_Icc) and is injective on it (by modInv_injective_on_Icc). Since Icc 1 (p-1) is finite, an injective self-map is a bijection. Use Finset.exists_equiv_of_injOn or construct the Equiv.Perm directly using Equiv.ofBijective or Set.InjOn.bijOn_image then extend to a perm.
-/
theorem modInv_perm_of_Icc (p : ℕ) (hp : Nat.Prime p) (hp3 : 3 ≤ p) :
    ∃ σ : Equiv.Perm (Finset.Icc 1 (p - 1)),
      ∀ x : Finset.Icc 1 (p - 1),
        ((↑(σ x) : ℕ) : ZMod p) = ((↑x : ℕ) : ZMod p)⁻¹ := by
  haveI := Fact.mk hp; simp_all +decide [ ← ZMod.val_natCast ] ;
  obtain ⟨σ, hσ⟩ : ∃ σ : (Finset.Icc 1 (p - 1) : Set ℕ) → Finset.Icc 1 (p - 1), ∀ a : Finset.Icc 1 (p - 1), ((σ a).val : ℕ) = (((a.val : ℕ)⁻¹ : ZMod p).val) := by
    haveI := Fact.mk hp; use fun a => ⟨ ( ( a.val : ZMod p ) ⁻¹ |> ZMod.val ), by
      convert modInv_mem_Icc hp hp3 _ ; aesop ⟩ ; aesop;
  have hσ_bij : Function.Bijective σ := by
    have hσ_inj : Function.Injective σ := by
      intros a b hab; have := hσ a; have := hσ b; simp_all +decide [ ZMod.val_natCast ] ;
      haveI := Fact.mk hp; simp_all +decide [ ZMod.val_injective _ |>.eq_iff ] ;
      exact Subtype.ext <| Nat.mod_eq_of_lt ( show ( a : ℕ ) < p from lt_of_le_of_lt ( Finset.mem_Icc.mp a.2 |>.2 ) ( Nat.pred_lt hp.ne_zero ) ) ▸ Nat.mod_eq_of_lt ( show ( b : ℕ ) < p from lt_of_le_of_lt ( Finset.mem_Icc.mp b.2 |>.2 ) ( Nat.pred_lt hp.ne_zero ) ) ▸ by simpa [ ← ZMod.natCast_eq_natCast_iff' ] using ‹ ( b : ZMod p ) = a ›.symm;
    generalize_proofs at *; exact ⟨hσ_inj, Finite.injective_iff_surjective.mp hσ_inj⟩;
  obtain ⟨σ', hσ'⟩ : ∃ σ' : Equiv.Perm (Finset.Icc 1 (p - 1) : Set ℕ), ∀ a : Finset.Icc 1 (p - 1), σ' a = σ a := by
    exact ⟨ Equiv.ofBijective σ hσ_bij, fun a => rfl ⟩;
  use σ';
  intro a ha hb; haveI := Fact.mk hp; simp_all +decide ;

/-! ## Section 3: Harmonic Identity -/

/-
PROBLEM
**Theorem 2 (Harmonic identity)**: Since the modular inverse is a permutation
    of {1,...,p-1}, summing 1/b_k over k = 1,...,p-1 yields H(p-1).
    ∑_{k=1}^{p-1} 1/(k⁻¹ mod p) = ∑_{k=1}^{p-1} 1/k

PROVIDED SOLUTION
The function k ↦ ((k : ZMod p)⁻¹).val maps Icc 1 (p-1) into itself (modInv_mem_Icc) and is injective (modInv_injective_on_Icc). Since the domain is finite and the function is an injective self-map, the image is the whole set. Use Finset.sum_nbij or Finset.sum_bij with this bijection to reindex the sum. The function g(k) = 1/k is applied to the image which is a permutation, so the sums are equal.
-/
theorem harmonic_identity_sum (p : ℕ) (hp : Nat.Prime p) (hp3 : 3 ≤ p) :
    ∑ k ∈ Finset.Icc 1 (p - 1), (1 : ℚ) / ((((k : ZMod p)⁻¹).val : ℕ) : ℚ) =
    ∑ k ∈ Finset.Icc 1 (p - 1), (1 : ℚ) / (k : ℚ) := by
  -- The function k ↦ ((k : ZMod p)⁻¹).val is a bijection on the finite set {1, ..., p-1}, so summing over it is the same as summing over the original set.
  have h_bij : Finset.image (fun k : ℕ => ((k : ZMod p)⁻¹).val) (Finset.Icc 1 (p - 1)) = Finset.Icc 1 (p - 1) := by
    refine Finset.eq_of_subset_of_card_le ( Finset.image_subset_iff.mpr fun x hx => ?_ ) ?_;
    · exact?;
    · rw [ Finset.card_image_of_injOn ];
      exact?;
  conv_rhs => rw [ ← h_bij, Finset.sum_image ( Finset.card_image_iff.mp <| by aesop ) ] ;

/-! ## Section 4: Sub-Gap Formula -/

/-
PROBLEM
The Farey neighbor relation: if k*b = p*a + 1, then k/p - a/b = 1/(p*b).

PROVIDED SOLUTION
From k*b = p*a + 1, we get k*b - p*a = 1. So k/p - a/b = (k*b - p*a)/(p*b) = 1/(p*b). Use field_simp to clear denominators, then use the hypothesis to finish with ring/omega.
-/
lemma farey_subgap_width (a b k p : ℕ) (hb : 0 < b) (hp : 0 < p)
    (hneighbor : k * b = p * a + 1) :
    (k : ℚ) / p - (a : ℚ) / b = 1 / (p * b) := by
  -- Combine the fractions on the left-hand side.
  field_simp [hneighbor];
  exact sub_eq_of_eq_add <| mod_cast hneighbor ▸ by ring;

/-
PROBLEM
The modular inverse relation: for prime p, k in {1,...,p-1},
    k * (k⁻¹ mod p) ≡ 1 (mod p).

PROVIDED SOLUTION
k ∈ Icc 1 (p-1) so (k : ZMod p) ≠ 0, hence IsUnit. Then k * k⁻¹ = 1 in ZMod p. Transfer to the val representation: ZMod.val_natCast_of_lt and ZMod.val_mul etc. Key: use ZMod.val_inv_mul or show that (↑k * (↑k)⁻¹ : ZMod p) = 1, then take .val of both sides and use that ZMod.val 1 = 1 (since p ≥ 3 > 1). Use ZMod.mul_inv_of_unit or IsUnit.mul_val_inv.
-/
lemma modInv_mul_mod_eq_one (p k : ℕ) (hp : Nat.Prime p) (hk : k ∈ Finset.Icc 1 (p - 1)) :
    (k * ((k : ZMod p)⁻¹).val) % p = 1 := by
  -- Since $k$ and $p$ are coprime, $k$ has a multiplicative inverse modulo $p$, denoted by $k^{-1}$.
  have h_inv : (k : ZMod p) * ((k : ZMod p)⁻¹) = 1 := by
    haveI := Fact.mk hp; exact mul_inv_cancel₀ ( by rw [ Ne.eq_def, ZMod.natCast_eq_zero_iff ] ; exact Nat.not_dvd_of_pos_of_lt ( Finset.mem_Icc.mp hk |>.1 ) ( lt_of_le_of_lt ( Finset.mem_Icc.mp hk |>.2 ) ( Nat.pred_lt hp.ne_zero ) ) ) ;
  haveI := Fact.mk hp; simp_all +decide [ ← ZMod.val_natCast ] ;
  rcases p with ( _ | _ | p ) <;> norm_cast at *

/-
PROBLEM
**Theorem 3 (Sub-gap formula)**: When k·b − p·a = 1 (Farey neighbor condition)
    and b = k⁻¹ mod p, the left sub-gap width is 1/(p·b).

    From k·b ≡ 1 (mod p), we get k·b = p·a + 1 for some a,
    hence k/p − a/b = 1/(p·b).

PROVIDED SOLUTION
Let b = ((k : ZMod p)⁻¹).val. By modInv_mul_mod_eq_one, (k * b) % p = 1. So k * b = p * (k * b / p) + 1 (since the remainder is 1). Let a = k * b / p. Then k * b = p * a + 1 and by farey_subgap_width we get the formula. For b > 0, use modInv_mem_Icc to get b ≥ 1. For p > 0, use hp.pos.
-/
theorem subgap_formula (p k : ℕ) (hp : Nat.Prime p) (hp3 : 3 ≤ p)
    (hk : k ∈ Finset.Icc 1 (p - 1)) :
    let b := ((k : ZMod p)⁻¹).val
    ∃ a : ℕ, k * b = p * a + 1 ∧
      (k : ℚ) / p - (a : ℚ) / b = 1 / (p * b) := by
  -- By definition of $b$, we know that $k * b ≡ 1 \pmod{p}$.
  have h_mod : k * ((k : ZMod p)⁻¹).val ≡ 1 [MOD p] := by
    simp +zetaDelta at *;
    haveI := Fact.mk hp; simp +decide [ ← ZMod.natCast_eq_natCast_iff ] ;
    rw [ mul_inv_cancel₀ ( by rw [ Ne.eq_def, ZMod.natCast_eq_zero_iff ] ; exact Nat.not_dvd_of_pos_of_lt hk.1 ( lt_of_le_of_lt hk.2 ( Nat.pred_lt hp.ne_zero ) ) ) ];
  obtain ⟨a, ha⟩ : ∃ a : ℕ, k * ((k : ZMod p)⁻¹).val = p * a + 1 := by
    exact ⟨ k * ( k : ZMod p ) ⁻¹.val / p, by linarith [ Nat.mod_add_div ( k * ( k : ZMod p ) ⁻¹.val ) p, h_mod.symm ▸ Nat.mod_eq_of_lt hp.two_le ] ⟩;
  use a
  simp [ha];
  rw [ div_sub_div, div_eq_mul_inv ] <;> norm_cast <;> aesop;