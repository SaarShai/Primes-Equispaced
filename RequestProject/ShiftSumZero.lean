import Mathlib
import RequestProject.PrimeCircle
import RequestProject.BridgeIdentity

/-!
# Per-Denominator Shift Sum Vanishes

## Statement
For prime p and any b with 2 ≤ b ≤ p-1, the sum of shift residuals over
coprime residues vanishes:
  Σ_{a: gcd(a,b)=1, 0≤a<b} (a - pa mod b) = 0

This follows because a → pa mod b is a permutation of the coprime residues
mod b (since gcd(p,b) = 1 for b < p). So Σ(pa mod b) = Σa.

## Connection
This is the key per-denominator cancellation underlying the Permutation
Square-Sum Identity (PermutationIdentity.lean) and the Bridge Identity.
-/

open Finset BigOperators

/-! ## The linear shift sum vanishes -/

/-- For b ≥ 1 with gcd(p, b) = 1, the sum of (a - a*p % b) over coprime
    residues mod b equals zero.

    Proof: Since a → a*p % b is a permutation of coprime residues (coprime_mul_perm),
    Σ(a*p % b) = Σa, so Σ(a - a*p % b) = 0. -/
theorem shift_sum_zero (p b : ℕ) (hb : 0 < b) (hcop : Nat.Coprime p b) :
    ∑ a in (Finset.range b).filter (fun a => Nat.Coprime a b),
      ((a : ℤ) - (a * p % b : ℤ)) = 0 := by
  have hperm := coprime_mul_perm b p hb hcop
  suffices h : ∑ a in (Finset.range b).filter (fun a => Nat.Coprime a b), (a * p % b : ℤ) =
    ∑ a in (Finset.range b).filter (fun a => Nat.Coprime a b), (a : ℤ) by
    simp [Finset.sum_sub_distrib, h]
  -- The map a → a * p % b is a permutation of the coprime residues
  conv_lhs =>
    arg 2; ext a; rw [show (a * p % b : ℤ) = ((fun a => a * p % b) a : ℤ) from by push_cast; rfl]
  rw [← Finset.sum_image (f := fun a => (a : ℤ))
    (s := (Finset.range b).filter (fun a => Nat.Coprime a b))
    (g := fun a => a * p % b)]
  · rw [hperm]
  · -- Injectivity
    intro a₁ ha₁ a₂ ha₂ heq
    simp only [Finset.mem_filter, Finset.mem_range] at ha₁ ha₂
    have ha₁r := ha₁.1
    have ha₂r := ha₂.1
    have hmod : a₁ * p ≡ a₂ * p [MOD b] := heq
    have hcong : a₁ ≡ a₂ [MOD b] := by
      rw [Nat.modEq_iff_dvd] at hmod ⊢
      have hsub : (b : ℤ) ∣ ((a₂ : ℤ) - a₁) * p := by
        convert hmod using 1; push_cast; ring
      exact (hcop.symm.cast (R := ℤ)).dvd_of_dvd_mul_right hsub
    rw [Nat.ModEq] at hcong
    simp only [Nat.mod_eq_of_lt ha₁r, Nat.mod_eq_of_lt ha₂r] at hcong
    exact hcong

/-- Variant with rational division by b: the per-denominator shift sum
    Σ_{gcd(a,b)=1} (a/b - (a*p%b)/b) = 0. -/
theorem shift_sum_zero_rat (p b : ℕ) (hb : 0 < b) (hcop : Nat.Coprime p b) :
    ∑ a in (Finset.range b).filter (fun a => Nat.Coprime a b),
      ((a : ℚ) / b - ((a * p % b : ℕ) : ℚ) / b) = 0 := by
  have hb_ne : (b : ℚ) ≠ 0 := by positivity
  simp_rw [← sub_div]
  rw [Finset.sum_div]
  rw [div_eq_zero_iff]
  left
  have h := shift_sum_zero p b hb hcop
  push_cast at h ⊢
  exact_mod_cast h

/-- The shift sum formulated for the shiftFun from DisplacementShift.lean:
    Σ_{gcd(a,b)=1, a<b} shiftFun(p, a/b) depends only on the coprime class structure.

    Note: This is NOT zero in general because shiftFun(p, a/b) = a/b - {p*a/b}
    and {p*a/b} = (pa mod b)/b only when a < b. The sum of shiftFun values
    equals the sum of (a - pa mod b)/b over coprime residues, which IS zero. -/
theorem shift_fun_sum_zero (p b : ℕ) (hb : 1 < b) (hcop : Nat.Coprime p b) :
    ∑ a in (Finset.range b).filter (fun a => Nat.Coprime a b),
      ((a : ℚ) / b - ((a * p % b : ℕ) : ℚ) / b) = 0 := by
  have hb_pos : 0 < b := by omega
  have hb_ne : (b : ℚ) ≠ 0 := by positivity
  simp_rw [← sub_div]
  rw [Finset.sum_div]
  have : (∑ a in (Finset.range b).filter (fun a => Nat.Coprime a b),
    ((a : ℚ) - ((a * p % b : ℕ) : ℚ))) / (b : ℚ) = 0 := by
    rw [div_eq_zero_iff]
    left
    have h := shift_sum_zero p b hb_pos hcop
    push_cast at h ⊢
    exact_mod_cast h
  exact this
