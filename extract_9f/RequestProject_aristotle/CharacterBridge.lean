import Mathlib
import PrimeCircle
import BridgeIdentity

/-!
# Character-Weighted Bridge Identity

For any function `chi : ℕ → ℂ` satisfying `chi 1 = 1`, and any prime `m > N`,

  Σ_{(a,b) ∈ F_N} chi(b) · e^{2πi m a/b} = 1 + Σ_{b=1}^{N} chi(b) · μ(b)

This generalizes the bridge identity from `BridgeIdentity.lean` (which is the
special case `chi = 1`).

## Proof strategy

1. Decompose the Farey sum by denominator b ∈ [1, N].
2. For b = 1: the coprime pairs are (0,1) and (1,1), contributing
   chi(1) · (e^0 + e^{2πim}) = 1 · 2 = 2.
3. For b ≥ 2: since m is prime and m > N ≥ b, we have gcd(m,b) = 1.
   The inner sum over a coprime to b in {0,...,b} equals c_b(m) = μ(b).
   So the contribution is chi(b) · μ(b).
4. Total = 2 + Σ_{b=2}^{N} chi(b) · μ(b)
         = 2 + (Σ_{b=1}^{N} chi(b) · μ(b) - chi(1) · μ(1))
         = 2 + Σ_{b=1}^{N} chi(b) · μ(b) - 1
         = 1 + Σ_{b=1}^{N} chi(b) · μ(b).  QED
-/

open Finset BigOperators Complex

/-! ## Character-weighted Farey exponential sum -/

/-- The character-weighted Farey exponential sum:
    Σ_{(a,b) ∈ F_N} chi(b) · e^{2πi m a/b} -/
noncomputable def charFareyExpSum (chi : ℕ → ℂ) (N m : ℕ) : ℂ :=
  ∑ ab ∈ fareySet N,
    chi ab.2 * exp (2 * ↑Real.pi * I * (↑m : ℂ) * (↑ab.1 : ℂ) / (↑ab.2 : ℂ))

/-! ## Computational verification for small cases

We verify the Möbius side values using `native_decide`. -/

/-- M(1) = 1, so 1 + M(1) = 2. -/
theorem char_bridge_rhs_N1 : 1 + mertens 1 = (2 : ℤ) := by native_decide

/-- M(2) = 0, so 1 + M(2) = 1. -/
theorem char_bridge_rhs_N2 : 1 + mertens 2 = (1 : ℤ) := by native_decide

/-- M(4) = -1, so 1 + M(4) = 0. -/
theorem char_bridge_rhs_N4 : 1 + mertens 4 = (0 : ℤ) := by native_decide

/-- M(6) = -1, so 1 + M(6) = 0. -/
theorem char_bridge_rhs_N6 : 1 + mertens 6 = (0 : ℤ) := by native_decide

/-- M(10) = -1, so 1 + M(10) = 0. -/
theorem char_bridge_rhs_N10 : 1 + mertens 10 = (0 : ℤ) := by native_decide

/-- M(12) = -2, so 1 + M(12) = -1. -/
theorem char_bridge_rhs_N12 : 1 + mertens 12 = (-1 : ℤ) := by native_decide

/-! ## Decomposition lemmas -/

/-
PROBLEM
The character-weighted Farey sum decomposes by denominator and factors out chi.

PROVIDED SOLUTION
Unfold charFareyExpSum. The fareySet N can be decomposed as a biUnion over b ∈ Icc 1 N, where for each b the fiber is {(a,b) : a ∈ range(b+1), Coprime a b}. This is exactly the same decomposition used in fareyExpSum_eq_sum_by_denom from BridgeIdentity.lean, but with the extra chi(b) factor. Since chi(b) is constant within each fiber (b is fixed), we can factor it out using Finset.mul_sum. The biUnion decomposition follows from fareySet's definition as a filter on range(N+1) ×ˢ range(N+1) with conditions 1 ≤ b, a ≤ b, Coprime a b.
-/
lemma charFareyExpSum_factor (chi : ℕ → ℂ) (N m : ℕ) :
    charFareyExpSum chi N m =
    ∑ b ∈ Finset.Icc 1 N,
      chi b * ∑ a ∈ (Finset.range (b + 1)).filter (fun a => Nat.Coprime a b),
        exp (2 * ↑Real.pi * I * (↑m : ℂ) * (↑a : ℂ) / (↑b : ℂ)) := by
  -- We can rewrite the sum over the Farey set as a sum over the divisors of $N$.
  have h_farey_divisors : fareySet N = Finset.biUnion (Finset.Icc 1 N) (fun b => Finset.image (fun a => (a, b)) ((Finset.range (b + 1)).filter (fun a => Nat.Coprime a b))) := by
    ext ⟨a, b⟩; simp [fareySet];
    grind;
  unfold charFareyExpSum;
  rw [ h_farey_divisors, Finset.sum_biUnion ];
  · simp +decide [ Finset.mul_sum _ _ _ ];
  · exact fun a ha b hb hab => Finset.disjoint_left.mpr fun x hx₁ hx₂ => hab <| by aesop;

/-- For b ≥ 2 with m prime and b < m, the inner exponential sum equals μ(b). -/
lemma inner_exp_sum_eq_moebius (b m : ℕ) (hb : 2 ≤ b) (hm : Nat.Prime m) (hbm : b < m) :
    ∑ a ∈ (Finset.range (b + 1)).filter (fun a => Nat.Coprime a b),
      exp (2 * ↑Real.pi * I * (↑m : ℂ) * (↑a : ℂ) / (↑b : ℂ)) =
    ↑(ArithmeticFunction.moebius b : ℤ) := by
  rw [farey_denom_ge2_eq_ramanujan b m hb]
  exact ramanujanSumGen_coprime_eq_moebius b m (by omega)
    (hm.coprime_iff_not_dvd.mpr (fun h => absurd (Nat.le_of_dvd (by omega) h) (by omega)))

/-! ## The Character Bridge Identity -/

/-
PROBLEM
**The Character Bridge Identity**: For any `chi : ℕ → ℂ` with `chi 1 = 1`
    and any prime `m > N`,

      Σ_{(a,b) ∈ F_N} chi(b) · e^{2πi m a/b} = 1 + Σ_{b=1}^{N} chi(b) · μ(b)

PROVIDED SOLUTION
Step 1: Use charFareyExpSum_factor to decompose the LHS into Σ_{b∈Icc 1 N} chi(b) * (inner sum over a).

Step 2: Split Icc 1 N = {1} ∪ Icc 2 N using Finset.Icc_insert_left or similar (since 1 ≤ N). Rewrite as sum over {1} plus sum over Icc 2 N.

Step 3: For b=1: the inner sum with b=1 has range(1+1) = range 2. Use farey_denom_one_sum m to show this inner sum = 2. So the b=1 term = chi(1) * 2 = 1 * 2 = 2 (using hchi).

Step 4: For b ∈ Icc 2 N: each b satisfies 2 ≤ b and b ≤ N < m, so b < m. Use inner_exp_sum_eq_moebius to replace each inner sum with (μ(b) : ℂ). So the Icc 2 N sum becomes Σ_{b∈Icc 2 N} chi(b) * μ(b).

Step 5: So LHS = 2 + Σ_{b∈Icc 2 N} chi(b) * μ(b).

Step 6: For the RHS, split Σ_{b∈Icc 1 N} chi(b)*μ(b) = chi(1)*μ(1) + Σ_{b∈Icc 2 N} chi(b)*μ(b) = 1*1 + Σ_{b∈Icc 2 N} chi(b)*μ(b) (using hchi, moebius_one). So RHS = 1 + 1 + Σ_{b∈Icc 2 N} chi(b)*μ(b) = 2 + Σ_{b∈Icc 2 N} chi(b)*μ(b) = LHS.
-/
theorem character_bridge_identity (chi : ℕ → ℂ) (hchi : chi 1 = 1)
    (N m : ℕ) (hN : 1 ≤ N) (hm : Nat.Prime m) (hmN : N < m) :
    charFareyExpSum chi N m =
    1 + ∑ b ∈ Finset.Icc 1 N, chi b * ↑(ArithmeticFunction.moebius b : ℤ) := by
  rw [ charFareyExpSum_factor chi N m ];
  rw [ Finset.sum_eq_add_sum_diff_singleton ( show 1 ∈ Finset.Icc 1 N from Finset.mem_Icc.mpr ⟨ by linarith, by linarith ⟩ ) ];
  rw [ Finset.sum_eq_add_sum_diff_singleton ( show 1 ∈ Icc 1 N from Finset.mem_Icc.mpr ⟨ by linarith, by linarith ⟩ ) ] ; norm_num [ hchi ];
  rw [ Finset.sum_eq_add ( 0 : ℕ ) ( 1 : ℕ ) ] <;> norm_num [ hchi, Complex.exp_ne_zero ];
  · rw [ Complex.exp_eq_one_iff.mpr ⟨ m, by push_cast; ring ⟩ ] ; ring;
    refine' congr rfl ( Finset.sum_congr rfl fun x hx => _ );
    convert congr_arg _ ( inner_exp_sum_eq_moebius x m ( by linarith [ Finset.mem_Icc.mp ( Finset.mem_sdiff.mp hx |>.1 ), show x > 1 from lt_of_le_of_ne ( Finset.mem_Icc.mp ( Finset.mem_sdiff.mp hx |>.1 ) |>.1 ) ( Ne.symm <| by aesop ) ] ) hm ( by linarith [ Finset.mem_Icc.mp ( Finset.mem_sdiff.mp hx |>.1 ) ] ) ) using 2 ; ring;
  · native_decide +revert