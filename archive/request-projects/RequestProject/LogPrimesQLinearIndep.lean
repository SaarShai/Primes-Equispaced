import Mathlib

/-!
# Q-linear independence of log 2, log 3, log 5

The logarithms of distinct primes are Q-linearly independent.
This is a consequence of the Fundamental Theorem of Arithmetic (unique factorization).

Here we prove the key special case for {log 2, log 3, log 5}: if
  2^a * 3^b * 5^c = 1  (with a, b, c : ℤ)
then a = 0, b = 0, c = 0.

This is the key lemma for the K = 5 phase analysis in the DPAC project:
it shows that the triple {γ log 2 / 2π, γ log 3 / 2π, γ log 5 / 2π} is
equidistributed (by Kronecker), so the non-vanishing of c_5(ρ) cannot be
proved purely by magnitude bounds — it requires specific properties of
Riemann zeros.
-/

/-- Integer powers of 2 and 3 are never equal (log 2 / log 3 is irrational). -/
theorem two_pow_ne_three_pow (a b : ℕ) (ha : 0 < a) : 2 ^ a ≠ 3 ^ b := by
  intro h
  have h2 : Nat.Prime 2 := by norm_num
  have h3 : Nat.Prime 3 := by norm_num
  have : 2 ∣ 3 ^ b := h ▸ dvd_pow_self 2 (by omega)
  have : 2 ∣ 3 := (Nat.Prime.dvd_of_dvd_pow h2 this)
  norm_num at this

/-- No product 2^a * 3^b * 5^c = 1 in ℕ unless a = b = c = 0.
    This is the natural number version (positive integer exponents). -/
theorem prime_product_eq_one_nat (a b c : ℕ) :
    2 ^ a * 3 ^ b * 5 ^ c = 1 → a = 0 ∧ b = 0 ∧ c = 0 := by
  intro h
  constructor
  · by_contra ha
    have ha' : 0 < a := Nat.pos_of_ne_zero ha
    have : 2 ∣ 2 ^ a * 3 ^ b * 5 ^ c := dvd_mul_of_dvd_left (dvd_mul_of_dvd_left (dvd_pow_self 2 (by omega)) _) _
    rw [h] at this
    exact absurd this (by norm_num)
  constructor
  · by_contra hb
    have hb' : 0 < b := Nat.pos_of_ne_zero hb
    have : 3 ∣ 2 ^ a * 3 ^ b * 5 ^ c := dvd_mul_of_dvd_left (dvd_mul_of_dvd_right (dvd_pow_self 3 (by omega)) _) _
    rw [h] at this
    exact absurd this (by norm_num)
  · by_contra hc
    have hc' : 0 < c := Nat.pos_of_ne_zero hc
    have : 5 ∣ 2 ^ a * 3 ^ b * 5 ^ c := dvd_mul_of_dvd_right (dvd_pow_self 5 (by omega)) _
    rw [h] at this
    exact absurd this (by norm_num)

/-
The integer exponent version: 2^a * 3^b * 5^c = 1 in ℝ implies a = b = c = 0.
    Proof: move negative exponents to the other side, apply unique factorization in ℕ.
-/
theorem log_primes_Q_linear_independent (a b c : ℤ) :
    (2 : ℝ) ^ a * (3 : ℝ) ^ b * (5 : ℝ) ^ c = 1 → a = 0 ∧ b = 0 ∧ c = 0 := by
  intro h
  -- Key: 2^a * 3^b * 5^c = 1 means the product equals 1
  -- Equivalently: 2^{a+} * 3^{b+} * 5^{c+} = 2^{a-} * 3^{b-} * 5^{c-}
  -- where x+ = max(x,0) and x- = max(-x, 0).
  -- By unique factorization in ℕ, all exponents match, so a+ = a-, etc., giving a = 0.
  rcases a with ( _ | a ) <;> rcases b with ( _ | b ) <;> rcases c with ( _ | c ) <;> norm_num [ zpow_add₀, zpow_neg ] at *;
  all_goals field_simp at h;
  all_goals norm_cast at *; have := congr_arg Even h; norm_num [ parity_simps ] at this;
  · aesop;
  · apply_fun fun x => x.factorization 5 at h ; simp_all +decide;
  · apply_fun fun x => x.factorization 3 at h ; simp_all +decide;
  · grind

/-
Equivalent formulation: {log 2, log 3, log 5} are Q-linearly independent.
    That is, q₁ log 2 + q₂ log 3 + q₃ log 5 = 0 with q₁,q₂,q₃ ∈ ℚ implies all zero.
-/
theorem log_primes_rat_linear_independent (q₁ q₂ q₃ : ℚ) :
    q₁ * Real.log 2 + q₂ * Real.log 3 + q₃ * Real.log 5 = 0 →
    q₁ = 0 ∧ q₂ = 0 ∧ q₃ = 0 := by
  -- Clear denominators: write qᵢ = aᵢ/d. Then a₁ log 2 + a₂ log 3 + a₃ log 5 = 0
  -- i.e., log(2^a₁ * 3^a₂ * 5^a₃) = 0, i.e., 2^a₁ * 3^a₂ * 5^a₃ = 1 in ℝ.
  -- By log_primes_Q_linear_independent, all aᵢ = 0, so all qᵢ = 0.
  intro h
  have h_eq : (2 : ℝ) ^ (q₁.num * q₂.den * q₃.den) * (3 : ℝ) ^ (q₂.num * q₁.den * q₃.den) * (5 : ℝ) ^ (q₃.num * q₁.den * q₂.den) = 1 := by
    have h_exp : Real.log (2 ^ (q₁.num * q₂.den * q₃.den) * 3 ^ (q₂.num * q₁.den * q₃.den) * 5 ^ (q₃.num * q₁.den * q₂.den)) = 0 := by
      rw [ Real.log_mul, Real.log_mul, Real.log_zpow, Real.log_zpow, Real.log_zpow ] <;> norm_num;
      · rw [ ← @Rat.num_div_den q₁, ← @Rat.num_div_den q₂, ← @Rat.num_div_den q₃ ] at h ; simp_all +decide [ mul_assoc, mul_comm, mul_left_comm, div_eq_mul_inv ];
        field_simp at h;
        linarith;
      · positivity;
      · positivity;
      · exact ⟨ by positivity, by positivity ⟩;
      · positivity;
    rw [ ← Real.exp_log ( by positivity : 0 < ( 2 : ℝ ) ^ ( q₁.num * q₂.den * q₃.den ) * 3 ^ ( q₂.num * q₁.den * q₃.den ) * 5 ^ ( q₃.num * q₁.den * q₂.den ) ), h_exp, Real.exp_zero ];
  have := log_primes_Q_linear_independent ( q₁.num * q₂.den * q₃.den ) ( q₂.num * q₁.den * q₃.den ) ( q₃.num * q₁.den * q₂.den ) ?_ <;> simp_all +decide [ ← mul_assoc, Rat.cast_def ]