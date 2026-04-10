import Mathlib

/-!
# Deficit Minimality: D_q(2) = q(q²-1)/24 and D_q(r) ≥ D_q(2)

## Definitions
For prime q ≥ 3 and 1 ≤ r ≤ q-1 with gcd(r,q) = 1:

  D_q(r) := Σ_{a=1}^{q-1} a² - Σ_{a=1}^{q-1} a·(r·a mod q)

This measures the "deficit" of the permutation a ↦ ra mod q from the identity.

## Main Results

**Theorem 1 (Explicit evaluation):** D_q(2) = q(q²-1)/24.

**Theorem 2 (Minimality):** For all r with 1 < r < q and gcd(r,q) = 1,
  D_q(r) ≥ D_q(2).

## Connection to Farey research
The deficit D_q(r) appears in the analysis of how Farey fractions rearrange
under multiplication by r mod q. The minimality at r=2 explains why the
"simplest nontrivial" permutation produces the smallest rearrangement cost.
-/

open Finset BigOperators

/-! ## Core Definitions -/

/-- The sum Σ_{a=1}^{q-1} a², computed over ℚ for exact arithmetic. -/
def sumOfSquares (q : ℕ) : ℚ :=
  ∑ a ∈ Finset.Icc 1 (q - 1), (a : ℚ) ^ 2

/-- The modular cross sum: Σ_{a=1}^{q-1} a · (r·a mod q), computed over ℚ. -/
def modCrossSum (q r : ℕ) : ℚ :=
  ∑ a ∈ Finset.Icc 1 (q - 1), (a : ℚ) * ((r * a % q : ℕ) : ℚ)

/-- The deficit: D_q(r) = Σ a² - Σ a·(ra mod q). -/
def deficit (q r : ℕ) : ℚ :=
  sumOfSquares q - modCrossSum q r

/-! ## The Dedekind sum (classical definition) -/

/-- The sawtooth function ((x)) = x - ⌊x⌋ - 1/2 if x ∉ ℤ, else 0. -/
def sawtooth (x : ℚ) : ℚ :=
  if (x.den : ℤ) = 1 then 0 else x - ⌊x⌋ - 1/2

/-- The Dedekind sum s(h,k). -/
def dedekindSum (h k : ℕ) : ℚ :=
  ∑ a ∈ Finset.Icc 1 (k - 1),
    sawtooth ((a : ℚ) / k) * sawtooth ((h * a : ℚ) / k)

/-! ## Computational Verification: D_q(2) = q(q²-1)/24 for small primes -/

/-- D_3(2) = 1. Note: 3·(9-1)/24 = 1. -/
theorem deficit_3_2 : deficit 3 2 = 1 := by native_decide

/-- D_5(2) = 5. Note: 5·24/24 = 5. -/
theorem deficit_5_2 : deficit 5 2 = 5 := by native_decide

/-- D_7(2) = 14. Note: 7·48/24 = 14. -/
theorem deficit_7_2 : deficit 7 2 = 14 := by native_decide

/-- D_11(2) = 55. Note: 11·120/24 = 55. -/
theorem deficit_11_2 : deficit 11 2 = 55 := by native_decide

/-- D_13(2) = 91. Note: 13·168/24 = 91. -/
theorem deficit_13_2 : deficit 13 2 = 91 := by native_decide

/-- Verify the formula: D_q(2) = q(q²-1)/24 for q = 3. -/
theorem deficit_formula_3 : deficit 3 2 = 3 * (3 ^ 2 - 1) / 24 := by native_decide

/-- Verify the formula for q = 5. -/
theorem deficit_formula_5 : deficit 5 2 = 5 * (5 ^ 2 - 1) / 24 := by native_decide

/-- Verify the formula for q = 7. -/
theorem deficit_formula_7 : deficit 7 2 = 7 * (7 ^ 2 - 1) / 24 := by native_decide

/-- Verify the formula for q = 11. -/
theorem deficit_formula_11 : deficit 11 2 = 11 * (11 ^ 2 - 1) / 24 := by native_decide

/-- Verify the formula for q = 13. -/
theorem deficit_formula_13 : deficit 13 2 = 13 * (13 ^ 2 - 1) / 24 := by native_decide

/-- Verify the formula for q = 17. -/
theorem deficit_formula_17 : deficit 17 2 = 17 * (17 ^ 2 - 1) / 24 := by native_decide

/-- Verify the formula for q = 19. -/
theorem deficit_formula_19 : deficit 19 2 = 19 * (19 ^ 2 - 1) / 24 := by native_decide

/-- Verify the formula for q = 23. -/
theorem deficit_formula_23 : deficit 23 2 = 23 * (23 ^ 2 - 1) / 24 := by native_decide

/-! ## Computational Verification: D_q(r) ≥ D_q(2) (minimality) -/

/-- For q = 5: D_5(r) ≥ D_5(2) for all r in {2,3,4}. -/
theorem deficit_min_5 : ∀ r ∈ ({2, 3, 4} : Finset ℕ),
    deficit 5 r ≥ deficit 5 2 := by native_decide

/-- For q = 7: D_7(r) ≥ D_7(2) for all r in {2,3,4,5,6}. -/
theorem deficit_min_7 : ∀ r ∈ ({2, 3, 4, 5, 6} : Finset ℕ),
    deficit 7 r ≥ deficit 7 2 := by native_decide

/-- For q = 11: D_11(r) ≥ D_11(2) for all valid r. -/
theorem deficit_min_11 : ∀ r ∈ ({2, 3, 4, 5, 6, 7, 8, 9, 10} : Finset ℕ),
    deficit 11 r ≥ deficit 11 2 := by native_decide

/-- For q = 13: D_13(r) ≥ D_13(2) for all valid r. -/
theorem deficit_min_13 : ∀ r ∈ ({2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12} : Finset ℕ),
    deficit 13 r ≥ deficit 13 2 := by native_decide

/-! ## Helper lemmas for the general theorems -/

/-
PROBLEM
Sum of squares formula: ∑_{a=1}^{n} a² = n(n+1)(2n+1)/6.

PROVIDED SOLUTION
Prove by induction on n. Base case n=0: both sides are 0 (Icc 1 0 is empty). Inductive step: use Finset.sum_Icc_succ_top or equivalent to peel off the n+1 term: ∑_{a=1}^{n+1} a² = ∑_{a=1}^{n} a² + (n+1)². Apply IH and verify algebra with field_simp; ring. May need to convert between Icc sums and the induction. Key idea: Nat.Icc_insert_right or show Finset.Icc 1 (n+1) = insert (n+1) (Finset.Icc 1 n) when n ≥ 1, or handle n=0 separately.
-/
private lemma sum_sq_Icc (n : ℕ) :
    ∑ a ∈ Finset.Icc 1 n, (a : ℚ) ^ 2 = ↑n * (↑n + 1) * (2 * ↑n + 1) / 6 := by
  exact Eq.symm ( Nat.recOn n ( by norm_num ) fun n ih => by norm_num [ Finset.sum_Ioc_succ_top, (Nat.succ_eq_succ ▸ Finset.Icc_succ_left_eq_Ioc) ] at * ; linarith )

/-
PROBLEM
Sum formula: ∑_{a=1}^{n} a = n(n+1)/2.

PROVIDED SOLUTION
Prove by induction on n. Base case n=0: Icc 1 0 is empty, both sides 0. Inductive step: peel off the last element n+1 from Icc 1 (n+1). Apply IH and check algebra with field_simp; ring.
-/
private lemma sum_Icc_nat (n : ℕ) :
    ∑ a ∈ Finset.Icc 1 n, (a : ℚ) = ↑n * (↑n + 1) / 2 := by
  exact Nat.recOn n ( by norm_num ) fun n ih => by norm_num [ Finset.sum_Ioc_succ_top, (Nat.succ_eq_succ ▸ Finset.Icc_succ_left_eq_Ioc) ] at * ; linarith;

/-- sumOfSquares(2k+1) = k(2k+1)(4k+1)/3. -/
private lemma sumOfSquares_closed (k : ℕ) :
    sumOfSquares (2 * k + 1) = (k : ℚ) * (2 * ↑k + 1) * (4 * ↑k + 1) / 3 := by
  unfold sumOfSquares
  have h : 2 * k + 1 - 1 = 2 * k := by omega
  rw [h, sum_sq_Icc]
  push_cast; ring

/-
PROBLEM
Splitting an Icc sum: ∑_{k+1}^{2k} = ∑_{1}^{2k} - ∑_{1}^{k}.

PROVIDED SOLUTION
Use Finset.sum_sdiff or Finset.sum_union. First show Finset.Icc 1 k ⊆ Finset.Icc 1 (2*k) (since k ≤ 2*k). Then Finset.Icc 1 (2*k) \ Finset.Icc 1 k = Finset.Icc (k+1) (2*k) (ext + omega). Then by Finset.sum_sdiff: ∑_{(k+1)..2k} + ∑_{1..k} = ∑_{1..2k}, rearrange to get the result. Alternative: show Finset.Icc 1 (2*k) = Finset.Icc 1 k ∪ Finset.Icc (k+1) (2*k) (disjoint since all elements of first ≤ k and all of second ≥ k+1), then use Finset.sum_union.
-/
private lemma sum_Icc_upper_half (k : ℕ) (hk : 1 ≤ k) :
    ∑ a ∈ Finset.Icc (k + 1) (2 * k), (a : ℚ) =
    ∑ a ∈ Finset.Icc 1 (2 * k), (a : ℚ) - ∑ a ∈ Finset.Icc 1 k, (a : ℚ) := by
  erw [ eq_sub_iff_add_eq', Finset.sum_Ico_consecutive ] <;> linarith!

/-
PROBLEM
The key decomposition: modCrossSum(2k+1, 2) = 2·sumOfSquares(2k+1) - (2k+1)·∑_{k+1}^{2k} a.

    Proof: Split [1, 2k] into [1, k] ∪ [k+1, 2k].
    For a ≤ k: 2a < 2k+1 so 2a mod (2k+1) = 2a, giving term a·(2a) = 2a².
    For a ≥ k+1: 2k+1 ≤ 2a < 2(2k+1) so 2a mod (2k+1) = 2a-(2k+1), giving term a·(2a-(2k+1)) = 2a² - (2k+1)a.
    Summing: 2·∑a² - (2k+1)·∑_{k+1}^{2k} a.

PROVIDED SOLUTION
Unfold modCrossSum and sumOfSquares. Show 2*k+1-1 = 2*k.

Split Finset.Icc 1 (2*k) into Finset.Icc 1 k ∪ Finset.Icc (k+1) (2*k) (disjoint). Use Finset.sum_union.

For the low half (a ∈ Icc 1 k): use Finset.sum_congr to show each term a * ((2*a % (2*k+1) : ℕ) : ℚ) = a * (2*a : ℚ) = 2*a². Key fact: 2*a % (2*k+1) = 2*a by Nat.mod_eq_of_lt (since 2*a ≤ 2*k < 2*k+1, so omega).

For the high half (a ∈ Icc (k+1) (2*k)): use Finset.sum_congr to show each term a * ((2*a % (2*k+1) : ℕ) : ℚ) = a * (2*a - (2*k+1) : ℚ) = 2*a² - (2*k+1)*a. Key facts: 2*k+1 ≤ 2*a (by omega since a ≥ k+1), 2*a < 2*(2*k+1) (by omega since a ≤ 2*k). So 2*a % (2*k+1) = 2*a - (2*k+1), proved by rw [Nat.mod_eq_sub_mod (by omega)]; exact Nat.mod_eq_of_lt (by omega). Cast to ℚ using Nat.cast_sub.

After rewriting both halves:
Low half sum = 2 * ∑_{a=1}^{k} a² (factor out, use Finset.mul_sum or sum_congr)
High half sum = 2 * ∑_{a=k+1}^{2k} a² - (2k+1) * ∑_{a=k+1}^{2k} a (use Finset.sum_sub_distrib and Finset.mul_sum)

Total = 2*(∑_{1}^{k} a² + ∑_{k+1}^{2k} a²) - (2k+1)*∑_{k+1}^{2k} a = 2*∑_{1}^{2k} a² - (2k+1)*∑_{k+1}^{2k} a = 2*sumOfSquares(2k+1) - (2k+1)*∑_{k+1}^{2k} a.

The algebra involves rearranging with push_cast and ring. Be very careful with ℕ→ℚ casts.
-/
private lemma modCrossSum_two_decomp (k : ℕ) (hk : 1 ≤ k) :
    modCrossSum (2 * k + 1) 2 =
    2 * sumOfSquares (2 * k + 1) -
    ↑(2 * k + 1) * (∑ a ∈ Finset.Icc (k + 1) (2 * k), (a : ℚ)) := by
  unfold modCrossSum sumOfSquares;
  -- Split the sum into two parts: one over $[1, k]$ and one over $[k+1, 2k]$.
  have h_split : ∑ a ∈ Finset.Icc 1 (2 * k), (a : ℚ) * ((2 * a % (2 * k + 1) : ℕ) : ℚ) =
    ∑ a ∈ Finset.Icc 1 k, (a : ℚ) * (2 * a : ℚ) + ∑ a ∈ Finset.Icc (k + 1) (2 * k), (a : ℚ) * ((2 * a - (2 * k + 1) : ℚ)) := by
      have h_split : Finset.Icc 1 (2 * k) = Finset.Icc 1 k ∪ Finset.Icc (k + 1) (2 * k) := by
        exact Eq.symm ( Finset.Ico_union_Ico_eq_Ico ( by linarith ) ( by linarith ) );
      rw [ h_split, Finset.sum_union ];
      · refine' congrArg₂ ( · + · ) ( Finset.sum_congr rfl fun x hx => _ ) ( Finset.sum_congr rfl fun x hx => _ ) <;> norm_num [ Nat.mod_eq_of_lt ] at *;
        · exact Or.inl ( by rw [ Nat.mod_eq_of_lt ] <;> norm_cast ; linarith );
        · rw [ Nat.mod_eq_sub_mod ] <;> norm_num [ Nat.add_mod, Nat.mul_mod ];
          · rw [ Nat.mod_eq_of_lt ] <;> norm_num [ Nat.cast_sub ( by linarith : 2 * k + 1 ≤ 2 * x ) ] ; omega;
          · linarith;
      · exact Finset.disjoint_left.mpr fun x hx₁ hx₂ => by linarith [ Finset.mem_Icc.mp hx₁, Finset.mem_Icc.mp hx₂ ] ;
  simp_all +decide [ mul_sub, mul_assoc, Finset.mul_sum _ _ _, Finset.sum_add_distrib, pow_two ] ; ring!;
  rw [ show ( Finset.Icc 1 ( k * 2 ) ) = Finset.Icc 1 k ∪ Finset.Icc ( k + 1 ) ( k * 2 ) from ?_, Finset.sum_union ] <;> norm_num [ add_comm, add_left_comm, add_assoc, mul_comm, mul_assoc, mul_left_comm, Finset.sum_add_distrib ] ; ring;
  · exact Finset.disjoint_left.mpr fun x hx₁ hx₂ => by linarith [ Finset.mem_Icc.mp hx₁, Finset.mem_Icc.mp hx₂ ] ;
  · exact Eq.symm ( Finset.Ico_union_Ico_eq_Ico ( by linarith ) ( by linarith ) )

/-! ## The general theorems (targets for Aristotle) -/

/-- **Theorem 1 (D_q(2) formula):**
    For odd prime q ≥ 3, D_q(2) = q(q²-1)/24. -/
theorem deficit_two_formula (q : ℕ) (hq : Nat.Prime q) (hq3 : 3 ≤ q) :
    deficit q 2 = (q : ℚ) * ((q : ℚ) ^ 2 - 1) / 24 := by
  have hodd : q % 2 = 1 := hq.eq_two_or_odd.resolve_left (by omega)
  obtain ⟨k, rfl⟩ : ∃ k, q = 2 * k + 1 := ⟨q / 2, by omega⟩
  have hk : 1 ≤ k := by omega
  unfold deficit
  rw [modCrossSum_two_decomp k hk, sumOfSquares_closed k,
      sum_Icc_upper_half k hk, sum_Icc_nat, sum_Icc_nat]
  push_cast; ring

/-- **Theorem 2 (Deficit minimality):**
    For prime q ≥ 3 and 1 < r < q, D_q(r) ≥ D_q(2). -/
theorem deficit_minimality (q r : ℕ) (hq : Nat.Prime q) (hq3 : 3 ≤ q)
    (hr1 : 1 < r) (hrq : r < q) :
    deficit q r ≥ deficit q 2 := by
  sorry

/-- **Combined (Deficit lower bound):**
    For prime q ≥ 3 and 1 < r < q, D_q(r) ≥ q(q²-1)/24. -/
theorem deficit_lower_bound (q r : ℕ) (hq : Nat.Prime q) (hq3 : 3 ≤ q)
    (hr1 : 1 < r) (hrq : r < q) :
    deficit q r ≥ (q : ℚ) * ((q : ℚ) ^ 2 - 1) / 24 := by
  calc deficit q r ≥ deficit q 2 := deficit_minimality q r hq hq3 hr1 hrq
    _ = (q : ℚ) * ((q : ℚ) ^ 2 - 1) / 24 := deficit_two_formula q hq hq3

/-! ## Batch verification of the formula for primes up to 30 -/

/-- The formula D_q(2) = q(q²-1)/24 holds for all primes 3 ≤ q < 30. -/
theorem deficit_formula_batch_30 :
    ∀ q ∈ (Finset.range 30).filter (fun q => Nat.Prime q ∧ 3 ≤ q),
    deficit q 2 = (q : ℚ) * ((q : ℚ) ^ 2 - 1) / 24 := by native_decide

/-- The minimality D_q(r) ≥ D_q(2) holds for all primes 3 ≤ q ≤ 13,
    all 2 ≤ r ≤ q-1. -/
theorem deficit_minimality_batch_13 :
    ∀ q ∈ (Finset.range 14).filter (fun q => Nat.Prime q ∧ 3 ≤ q),
    ∀ r ∈ Finset.range q, 2 ≤ r → deficit q r ≥ deficit q 2 := by native_decide