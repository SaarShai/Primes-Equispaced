import Mathlib

theorem mul_p_perm (p b : ℕ) (hp : Nat.Coprime p b) (a : ℕ) (ha : Nat.Coprime a b) :
    Nat.Coprime (p * a % b) b := by
  rw [← Nat.mod_add_div (p * a) b] at *
  simp_all +decide [Nat.Coprime]
  exact Nat.Coprime.mul_left hp ha
