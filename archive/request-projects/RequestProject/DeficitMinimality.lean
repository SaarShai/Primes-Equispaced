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

/-! ## The general theorems (targets for Aristotle) -/

/-
PROBLEM
**Theorem 1 (D_q(2) formula):**
    For odd prime q ≥ 3, D_q(2) = q(q²-1)/24.

PROVIDED SOLUTION
For odd prime q ≥ 3, compute modCrossSum q 2 = ∑_{a=1}^{q-1} a*(2a mod q).

Split into two ranges:
- For a = 1 to (q-1)/2: 2a < q, so 2a mod q = 2a. Contribution: ∑ a*2a = 2∑a² = 2*(q-1)/2*((q-1)/2+1)*(2*(q-1)/2+1)/6
- For a = (q+1)/2 to q-1: 2a ≥ q, so 2a mod q = 2a - q. Contribution: ∑ a*(2a-q)

Then sumOfSquares q = q(q-1)(2q-1)/6 (standard sum of squares formula).

deficit q 2 = sumOfSquares q - modCrossSum q 2.

After algebraic simplification, this equals q(q²-1)/24.

The computation involves splitting the sum at q/2 and using standard sum formulas ∑k = n(n+1)/2 and ∑k² = n(n+1)(2n+1)/6.
-/
theorem deficit_two_formula (q : ℕ) (hq : Nat.Prime q) (hq3 : 3 ≤ q) :
    deficit q 2 = (q : ℚ) * ((q : ℚ) ^ 2 - 1) / 24 := by
  -- Split the sum into two parts: one for $a < q/2$ and one for $a \geq q/2$.
  have h_split : ∑ a ∈ Finset.Icc 1 (q - 1), (a : ℚ) * ((2 * a % q : ℕ) : ℚ) = ∑ a ∈ Finset.Icc 1 ((q - 1) / 2), (a : ℚ) * (2 * a : ℚ) + ∑ a ∈ Finset.Icc ((q + 1) / 2) (q - 1), (a : ℚ) * (2 * a - q : ℚ) := by
    have h_split : Finset.Icc 1 (q - 1) = Finset.Icc 1 ((q - 1) / 2) ∪ Finset.Icc ((q + 1) / 2) (q - 1) := by
      grind +revert;
    rw [ h_split, Finset.sum_union ];
    · refine' congrArg₂ ( · + · ) ( Finset.sum_congr rfl fun x hx => _ ) ( Finset.sum_congr rfl fun x hx => _ ) <;> norm_num at *;
      · exact Or.inl <| mod_cast Nat.mod_eq_of_lt <| by omega;
      · rw [ Nat.mod_eq_sub_mod ];
        · rw [ Nat.mod_eq_of_lt ];
          · exact Or.inl ( by rw [ Nat.cast_sub ] <;> norm_num ; omega );
          · omega;
        · omega;
    · exact Finset.disjoint_left.mpr fun x hx₁ hx₂ => by linarith [ Finset.mem_Icc.mp hx₁, Finset.mem_Icc.mp hx₂, Nat.div_mul_le_self ( q - 1 ) 2, Nat.div_add_mod ( q + 1 ) 2, Nat.mod_lt ( q + 1 ) two_pos, Nat.sub_add_cancel hq.pos ] ;
  rcases Nat.even_or_odd' q with ⟨ c, rfl | rfl ⟩ <;> norm_num at *;
  · simp_all +decide [ Nat.prime_mul_iff ];
  · unfold deficit sumOfSquares modCrossSum; norm_num [ h_split ] ; ring;
    erw [ Finset.sum_Ico_eq_sub _ _, Finset.sum_Ico_eq_sub _ _, Finset.sum_Ico_eq_sub _ _ ] <;> norm_num [ Finset.sum_range_succ' ] ; ring;
    · norm_num [ Finset.sum_add_distrib, Finset.mul_sum _ _ _, Finset.sum_mul ] ; ring;
      norm_num [ ← Finset.mul_sum _ _ _, ← Finset.sum_mul ] ; ring;
      -- Evaluate the sums of squares and linear terms using known formulas.
      have h_sums : ∀ n : ℕ, (∑ i ∈ Finset.range n, (i : ℚ)) = n * (n - 1) / 2 ∧ (∑ i ∈ Finset.range n, (i ^ 2 : ℚ)) = n * (n - 1) * (2 * n - 1) / 6 := by
        exact fun n => ⟨ by induction n <;> simpa [ Finset.sum_range_succ ] using by linarith, by induction n <;> simpa [ Finset.sum_range_succ ] using by linarith ⟩;
      norm_num [ h_sums ] ; ring;
    · grind

/-! ## Helper lemmas for deficit minimality -/

/-
PROBLEM
Multiplication by r mod q maps Icc 1 (q-1) to itself when q is prime and 0 < r < q.

PROVIDED SOLUTION
Show the image is a subset of Icc 1 (q-1) (since ra mod q ∈ {1,...,q-1} when q is prime and both r,a ∈ {1,...,q-1}: ra mod q ≠ 0 because q prime doesn't divide r*a as 0 < r,a < q; and ra mod q < q). Then use injectivity (mul_mod_injOn) and card equality to conclude they're equal. Use Finset.eq_of_subset_of_card_le or Finset.image_eq_of_injOn.
-/
lemma mul_mod_image_Icc (q r : ℕ) (hq : Nat.Prime q) (hr : 0 < r) (hrq : r < q) :
    (Finset.Icc 1 (q - 1)).image (fun a => r * a % q) = Finset.Icc 1 (q - 1) := by
  refine Finset.eq_of_subset_of_card_le ( Finset.image_subset_iff.mpr ?_ ) ?_;
  · exact fun x hx => Finset.mem_Icc.mpr ⟨ Nat.pos_of_ne_zero fun con => by have := Nat.dvd_of_mod_eq_zero con; exact absurd ( hq.dvd_mul.mp this ) ( by rintro ( h | h ) <;> have := Nat.le_of_dvd ( by linarith [ Finset.mem_Icc.mp hx ] ) h <;> linarith [ Finset.mem_Icc.mp hx, Nat.sub_add_cancel hq.pos ] ), Nat.le_sub_one_of_lt <| Nat.mod_lt _ <| pos_of_gt hrq ⟩;
  · rw [ Finset.card_image_of_injOn ];
    intro a ha b hb hab;
    haveI := Fact.mk hq; simp_all +decide [ ← ZMod.natCast_eq_natCast_iff' ] ;
    exact Nat.mod_eq_of_lt ( show a < q from lt_of_le_of_lt ha.2 ( Nat.pred_lt hq.ne_zero ) ) ▸ Nat.mod_eq_of_lt ( show b < q from lt_of_le_of_lt hb.2 ( Nat.pred_lt hq.ne_zero ) ) ▸ by simpa [ ← ZMod.natCast_eq_natCast_iff' ] using hab.resolve_right ( by rw [ ZMod.natCast_eq_zero_iff ] ; exact Nat.not_dvd_of_pos_of_lt hr hrq ) ;

/-
PROBLEM
The map a ↦ r * a % q is injective on Icc 1 (q-1) when q is prime and 0 < r < q.

PROVIDED SOLUTION
If r*a ≡ r*b mod q then q | r*(a-b). Since q is prime and 0 < r < q, gcd(r,q)=1, so q | (a-b). But a, b ∈ {1,...,q-1} so |a-b| < q, hence a = b.

Use ZMod or Nat.Prime.dvd_mul to handle the divisibility argument.
-/
lemma mul_mod_injOn (q r : ℕ) (hq : Nat.Prime q) (hr : 0 < r) (hrq : r < q) :
    Set.InjOn (fun a => r * a % q) (Finset.Icc 1 (q - 1) : Set ℕ) := by
  intros a ha b hb hab; haveI := Fact.mk hq; simp_all +decide [ ← ZMod.natCast_eq_natCast_iff' ] ;
  exact Nat.mod_eq_of_lt ( show a < q from lt_of_le_of_lt ha.2 ( Nat.pred_lt hq.ne_zero ) ) ▸ Nat.mod_eq_of_lt ( show b < q from lt_of_le_of_lt hb.2 ( Nat.pred_lt hq.ne_zero ) ) ▸ by simpa [ ← ZMod.natCast_eq_natCast_iff' ] using hab.resolve_right ( by rw [ ZMod.natCast_eq_zero_iff ] ; exact Nat.not_dvd_of_pos_of_lt hr hrq ) ;

/-
PROBLEM
The sum of f over the image of Icc 1 (q-1) under multiplication by r mod q
    equals the sum over Icc 1 (q-1).

PROVIDED SOLUTION
Use Finset.sum_nbij (or sum_bij) with the bijection a ↦ r*a % q on Finset.Icc 1 (q-1). The key facts are:
1. mul_mod_image_Icc shows the image is Icc 1 (q-1)
2. mul_mod_injOn shows injectivity

More concretely: rewrite the LHS as ∑ over the image using Finset.sum_image with injectivity from mul_mod_injOn. Then use mul_mod_image_Icc to rewrite the image set back to Icc 1 (q-1).
-/
lemma sum_image_mul_mod (q r : ℕ) (hq : Nat.Prime q) (hr : 0 < r) (hrq : r < q)
    (f : ℕ → ℚ) :
    ∑ a ∈ Finset.Icc 1 (q - 1), f (r * a % q) =
    ∑ a ∈ Finset.Icc 1 (q - 1), f a := by
  -- Apply the fact that multiplication by r is a permutation on the nonzero elements modulo q.
  have h_perm : Finset.image (fun a => r * a % q) (Finset.Icc 1 (q - 1)) = Finset.Icc 1 (q - 1) := by
    exact?;
  conv_rhs => rw [ ← h_perm, Finset.sum_image ( Finset.card_image_iff.mp <| by aesop ) ] ;

/-
PROBLEM
The deficit equals half the sum of displacement squared.

PROVIDED SOLUTION
Expand (a - b)² = a² - 2ab + b². So:
∑ (a - ra%q)² = ∑ a² - 2∑ a*(ra%q) + ∑ (ra%q)²

By sum_image_mul_mod with f(x) = x², we have ∑ (ra%q)² = ∑ a² = sumOfSquares q.

So ∑ (a - ra%q)² = 2*sumOfSquares q - 2*modCrossSum q r.

And (1/2) * ∑ (a-ra%q)² = sumOfSquares q - modCrossSum q r = deficit q r.

The proof unfolds deficit, sumOfSquares, modCrossSum and uses algebraic identities over ℚ, along with sum_image_mul_mod for the key permutation step.
-/
lemma deficit_eq_half_disp_sq (q r : ℕ) (hq : Nat.Prime q) (hr : 0 < r) (hrq : r < q) :
    deficit q r = (1/2 : ℚ) *
      ∑ a ∈ Finset.Icc 1 (q - 1), ((a : ℚ) - ((r * a % q : ℕ) : ℚ))^2 := by
  unfold deficit;
  -- Expand the square and split the sum into three parts.
  have h_expand : ∑ a ∈ Finset.Icc 1 (q - 1), (a - (r * a % q : ℕ) : ℚ) ^ 2 = ∑ a ∈ Finset.Icc 1 (q - 1), (a : ℚ) ^ 2 - 2 * ∑ a ∈ Finset.Icc 1 (q - 1), (a : ℚ) * ((r * a % q : ℕ) : ℚ) + ∑ a ∈ Finset.Icc 1 (q - 1), ((r * a % q : ℕ) : ℚ) ^ 2 := by
    simp +decide [ sub_sq, Finset.sum_add_distrib, Finset.mul_sum _ _ _, mul_assoc ];
  -- By sum_image_mul_mod, we have ∑ (ra%q)² = ∑ a² = sumOfSquares q.
  have h_sum_image : ∑ a ∈ Finset.Icc 1 (q - 1), ((r * a % q : ℕ) : ℚ) ^ 2 = ∑ a ∈ Finset.Icc 1 (q - 1), (a : ℚ) ^ 2 := by
    convert sum_image_mul_mod q r hq hr hrq ( fun x => x ^ 2 ) using 1;
  unfold sumOfSquares modCrossSum; linarith;

/-
PROBLEM
For r=2 and prime q ≥ 3, the displacement squared equals min(a, q-a)².

PROVIDED SOLUTION
Case split on whether a ≤ (q-1)/2 or a > (q-1)/2.

Case 1 (a ≤ (q-1)/2): Since q is odd (prime ≥ 3), 2*a ≤ q-1 < q, so 2*a % q = 2*a. Then (a - 2a)² = a² = (-a)². Also min(a, q-a) = a since a ≤ (q-1)/2 < q-a. So both sides are a².

Case 2 (a > (q-1)/2): Since a ≤ q-1, we have (q+1)/2 ≤ a ≤ q-1. Then 2a ≥ q+1 > q, and 2a ≤ 2(q-1) < 2q. So 2*a % q = 2*a - q. Then (a - (2a - q))² = (q - a)². Also min(a, q-a) = q - a since a > (q-1)/2 means q - a < a. So both sides are (q-a)².

Use omega for the arithmetic, Nat.mod_eq_of_lt and Nat.mod_eq_sub_mod for the mod computations.
-/
lemma disp_sq_two (q : ℕ) (hq : Nat.Prime q) (hq3 : 3 ≤ q) (a : ℕ)
    (ha : a ∈ Finset.Icc 1 (q - 1)) :
    ((a : ℚ) - ((2 * a % q : ℕ) : ℚ))^2 = ((min a (q - a) : ℕ) : ℚ)^2 := by
  cases le_total a ( q - a ) <;> simp_all +decide [ Nat.mod_eq_of_lt ];
  · rw [ Nat.mod_eq_of_lt ];
    · push_cast; ring;
    · cases Nat.Prime.eq_two_or_odd hq <;> omega;
  · rw [ Nat.cast_sub ];
    · rw [ show ( 2 * a % q : ℕ ) = 2 * a - q from ?_ ];
      · rw [ Nat.cast_sub ] <;> push_cast <;> linarith [ Nat.sub_add_cancel ( by linarith : 1 ≤ q ) ];
      · rw [ Nat.mod_eq_sub_mod ( by linarith ) ];
        rw [ Nat.mod_eq_of_lt ( by omega ) ];
    · omega

/-
PROBLEM
For any r with 1 < r < q and q prime, each displacement squared is ≥ min(c, q-c)²
    where c = a * (q + 1 - r) % q. This is because a - ra mod q ≡ a(1-r) mod q,
    so the displacement is either c or c - q, giving square c² or (q-c)² ≥ min(c,q-c)².

PROVIDED SOLUTION
Let c = a * (q + 1 - r) % q. We know 1 ≤ a ≤ q-1 and 1 < r < q.

Key congruence: a - r*a ≡ a*(1-r) ≡ a*(q+1-r) ≡ c (mod q).
So a - (r*a % q) ≡ c (mod q) as integers.

Since a ∈ {1,...,q-1} and r*a % q ∈ {1,...,q-1}, we have a - (r*a % q) ∈ {-(q-2),...,q-2}.
And c ∈ {1,...,q-1} (since q prime, a*(q+1-r) not divisible by q).

So a - (r*a % q) is either c or c - q (the two representatives of c mod q in the range).

Case 1: a - (r*a%q) = c. Then the LHS = c², and min(c, q-c)² ≤ c². ✓
Case 2: a - (r*a%q) = c - q. Then the LHS = (c-q)² = (q-c)², and min(c, q-c)² ≤ (q-c)². ✓

Both cases follow from min(c, q-c)² ≤ max(c², (q-c)²), which equals whichever the displacement squared is.

The key step is establishing that a - (r*a%q) ≡ c mod q. Work with cast to ℤ:
(a : ℤ) - (r*a%q : ℤ) ≡ a - r*a ≡ a*(1-r) mod q.
And c = a*(q+1-r) % q, so (c : ℤ) ≡ a*(q+1-r) ≡ a*(1-r) mod q (since q+1-r ≡ 1-r mod q).
So a - (r*a%q) ≡ c mod q.

Then since |a - (r*a%q)| ≤ q-2 < q, and c ∈ {1,...,q-1}, we get a - (r*a%q) = c or c-q.
-/
lemma disp_sq_ge_min (q r a : ℕ) (hq : Nat.Prime q) (hq3 : 3 ≤ q)
    (hr1 : 1 < r) (hrq : r < q)
    (ha : a ∈ Finset.Icc 1 (q - 1)) :
    ((a : ℚ) - ((r * a % q : ℕ) : ℚ))^2 ≥
    ((min (a * (q + 1 - r) % q) (q - a * (q + 1 - r) % q) : ℕ) : ℚ)^2 := by
  -- Let $c = a * (q + 1 - r) % q$. Then $a - (r * a % q) ≡ c \ (\text{mod} \ q)$.
  set c := a * (q + 1 - r) % q
  have h_congr : (a : ℤ) - (r * a % q : ℤ) ≡ c [ZMOD q] := by
    simp +zetaDelta at *;
    rw [ Nat.cast_sub ( by linarith ) ] ; push_cast ; ring;
    norm_num [ ← ZMod.intCast_eq_intCast_iff ];
  -- Since $a - (r * a % q) ≡ c \ (\text{mod} \ q)$, we have $a - (r * a % q) = c$ or $a - (r * a % q) = c - q$.
  have h_cases : (a : ℤ) - (r * a % q : ℤ) = c ∨ (a : ℤ) - (r * a % q : ℤ) = c - q := by
    obtain ⟨ k, hk ⟩ := h_congr.symm.dvd;
    -- Since $|a - (r * a % q)| \leq q - 2$ and $c \in \{1, \ldots, q - 1\}$, we have $k = 0$ or $k = -1$.
    have hk_bounds : -1 ≤ k ∧ k ≤ 0 := by
      constructor <;> nlinarith [ show ( a : ℤ ) ≤ q - 1 by exact le_tsub_of_add_le_right ( by linarith [ Finset.mem_Icc.mp ha, Nat.sub_add_cancel hq.pos ] ), show ( r * a % q : ℤ ) ≥ 0 by exact Int.emod_nonneg _ ( by linarith ), show ( r * a % q : ℤ ) < q by exact Int.emod_lt_of_pos _ ( by linarith ), show ( c : ℤ ) ≥ 0 by exact mod_cast Nat.zero_le _, show ( c : ℤ ) < q by exact mod_cast Nat.mod_lt _ ( by linarith ) ];
    cases hk_bounds ; interval_cases k <;> norm_num at hk ⊢ <;> first | left; linarith | right; linarith;
  cases' h_cases with h h <;> norm_cast at * <;> simp_all +decide [ Nat.mod_eq_of_lt ];
  · exact pow_le_pow_left₀ ( by positivity ) ( mod_cast min_le_left _ _ ) _;
  · rw [ Int.subNatNat_eq_coe ];
    rw [ min_def ] ; split_ifs <;> nlinarith [ Nat.sub_add_cancel ( show c ≤ q from Nat.le_of_lt <| Nat.mod_lt _ hq.pos ) ] ;

/-
PROBLEM
The sum of min(c, q-c)² over the permuted indices equals the sum of min(a, q-a)².

PROVIDED SOLUTION
Use sum_image_mul_mod with r' = q+1-r and f(x) = (min x (q-x) : ℕ)² cast to ℚ.

Since 1 < r < q, we have q+1-r ∈ {2,...,q-1}, so 0 < q+1-r < q. This gives:
∑ f(a*(q+1-r) % q) = ∑ f(a).

That is exactly the statement we need, since f(a) = ((min a (q-a) : ℕ) : ℚ)^2.

Note: f(a*(q+1-r) % q) = ((min (a*(q+1-r)%q) (q - a*(q+1-r)%q) : ℕ) : ℚ)^2 which is exactly the LHS summand.
-/
lemma sum_min_sq_perm (q r : ℕ) (hq : Nat.Prime q) (hq3 : 3 ≤ q)
    (hr1 : 1 < r) (hrq : r < q) :
    ∑ a ∈ Finset.Icc 1 (q - 1),
      ((min (a * (q + 1 - r) % q) (q - a * (q + 1 - r) % q) : ℕ) : ℚ)^2 =
    ∑ a ∈ Finset.Icc 1 (q - 1), ((min a (q - a) : ℕ) : ℚ)^2 := by
  convert sum_image_mul_mod q ( q + 1 - r ) hq ( by omega ) ( by omega ) _ using 1;
  ac_rfl

/-
PROBLEM
**Theorem 2 (Deficit minimality):**
    For prime q ≥ 3 and 1 < r < q, D_q(r) ≥ D_q(2).

    Proof: deficit q r = (1/2) ∑ (a - ra mod q)².
    Each term (a - ra mod q)² ≥ min(c, q-c)² where c = a(1-r) mod q.
    Since a ↦ c is a permutation, ∑ min(c,q-c)² = ∑ min(a,q-a)².
    For r=2, each (a - 2a mod q)² = min(a, q-a)² exactly.
    So deficit q r ≥ (1/2) ∑ min(a,q-a)² = deficit q 2.

PROVIDED SOLUTION
1. Rewrite deficit q r using deficit_eq_half_disp_sq (with hr = by linarith for 0 < r).
2. Rewrite deficit q 2 using deficit_eq_half_disp_sq (with 0 < 2 and 2 < q since q ≥ 3).
3. Replace each (a - 2a%q)² with min(a,q-a)² using disp_sq_two and Finset.sum_congr.
4. Apply GE.ge, mul_le_mul_of_nonneg_left with (1/2 ≥ 0).
5. Apply Finset.sum_le_sum using disp_sq_ge_min for the pointwise bound ≥ min(c,q-c)².
6. Apply sum_min_sq_perm to equate ∑ min(c,q-c)² = ∑ min(a,q-a)².

So: deficit q r = (1/2)∑(a-ra%q)² ≥ (1/2)∑ min(c,q-c)² = (1/2)∑ min(a,q-a)² = deficit q 2.

Key: use `calc` or `have` statements chaining these steps. Use `le_refl` or `Finset.sum_le_sum` for the sum inequality, combined with the permutation identity sum_min_sq_perm.
-/
theorem deficit_minimality (q r : ℕ) (hq : Nat.Prime q) (hq3 : 3 ≤ q)
    (hr1 : 1 < r) (hrq : r < q) :
    deficit q r ≥ deficit q 2 := by
  rw [ deficit_eq_half_disp_sq q 2 hq ( by norm_num ) ( by linarith ), deficit_eq_half_disp_sq q r hq ( by linarith ) hrq ];
  -- Apply the inequality term by term to the sums.
  have h_sum_ineq : ∀ a ∈ Finset.Icc 1 (q - 1), ((a : ℚ) - ((r * a % q : ℕ) : ℚ))^2 ≥ ((min (a * (q + 1 - r) % q) (q - a * (q + 1 - r) % q) : ℕ) : ℚ)^2 := by
    exact?;
  refine' mul_le_mul_of_nonneg_left ( le_trans _ ( Finset.sum_le_sum h_sum_ineq ) ) ( by norm_num );
  rw [ sum_min_sq_perm ];
  · exact Finset.sum_le_sum fun x hx => by rw [ disp_sq_two q hq hq3 x hx ] ;
  · assumption;
  · linarith;
  · grind;
  · grind +splitImp

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