import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DenominatorSum

open Finset BigOperators

/-!
# New Fraction Discrepancy Sum for Prime p

## Main Result
For any prime p ≥ 3:
  Σ_{k=1}^{p-1} D₁_{F_p}(k/p) = (p-1)/2

where D₁(f) = rank₁(f) - |F_p| · f uses the 1-indexed rank
  rank₁(k/p) := #{f ∈ F_p | f < k/p} + 1  =  fareyRank p k p + 1.

## Proof strategy
1. Reflection lemma: fareyRank N a b + fareyRank N (b-a) b = |F_N| - 1
   (for (a,b) ∈ fareySet N, 1 ≤ a < b)
2. Discrepancy reflection (1-indexed): D₁(k/p) + D₁((p-k)/p) = 1
3. Sum over (p-1)/2 disjoint pairs → total = (p-1)/2

## Note on rank convention
`fareyRank N a b` = #{(c,d) ∈ fareySet N | c*b < a*d} is STRICT (0-indexed).
The problem statement uses 1-indexed rank: rank₁ = fareyRank + 1.
`newFracDisc1` below implements the 1-indexed version.
-/

/-! ## Definitions -/

/-- 1-indexed rank of k/b in F_N: #{f ∈ F_N | f < k/b} + 1. -/
noncomputable def fareyRank1 (N k b : ℕ) : ℕ := fareyRank N k b + 1

/-- 1-indexed displacement of k/p in F_p: rank₁(k/p) - |F_p| * (k/p). -/
noncomputable def newFracDisc1 (p k : ℕ) : ℚ :=
  (fareyRank1 p k p : ℚ) - (fareySet p).card * ((k : ℚ) / p)

/-- New fractions with denominator p: {k : 1 ≤ k < p, gcd(k,p)=1}. -/
def newFracs (p : ℕ) : Finset ℕ :=
  (Finset.Ico 1 p).filter (fun k => Nat.Coprime k p)

/-! ## Computational Verification -/

-- Verify Farey sizes
example : (fareySet 5).card = 11 := by native_decide

-- Verify strict ranks for p=5
-- F_5 = {0/1, 1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, 1/1}
-- #{f < 1/5} = 1 (just 0/1), so fareyRank 5 1 5 = 1
example : fareyRank 5 1 5 = 1 := by native_decide
example : fareyRank 5 4 5 = 9 := by native_decide
example : fareyRank 5 2 5 = 4 := by native_decide
example : fareyRank 5 3 5 = 6 := by native_decide

-- Reflection: fareyRank(k/p) + fareyRank((p-k)/p) = |F_p| - 1 = n - 1
example : fareyRank 5 1 5 + fareyRank 5 4 5 = (fareySet 5).card - 1 := by native_decide
example : fareyRank 5 2 5 + fareyRank 5 3 5 = (fareySet 5).card - 1 := by native_decide
example : fareyRank 7 1 7 + fareyRank 7 6 7 = (fareySet 7).card - 1 := by native_decide
example : fareyRank 7 2 7 + fareyRank 7 5 7 = (fareySet 7).card - 1 := by native_decide
example : fareyRank 7 3 7 + fareyRank 7 4 7 = (fareySet 7).card - 1 := by native_decide

-- Main identity for small primes
example : (∑ k ∈ newFracs 3, newFracDisc1 3 k) = 1 := by native_decide
example : (∑ k ∈ newFracs 5, newFracDisc1 5 k) = 2 := by native_decide
example : (∑ k ∈ newFracs 7, newFracDisc1 7 k) = 3 := by native_decide
example : (∑ k ∈ newFracs 11, newFracDisc1 11 k) = 5 := by native_decide
example : (∑ k ∈ newFracs 13, newFracDisc1 13 k) = 6 := by native_decide

/-! ## Helper Lemmas -/

/-- For prime p and 1 ≤ k < p, gcd(k, p) = 1. -/
lemma prime_coprime_lt (p k : ℕ) (hp : Nat.Prime p) (hk1 : 1 ≤ k) (hkp : k < p) :
    Nat.Coprime k p :=
  Nat.Coprime.symm ((Nat.Prime.coprime_iff_not_dvd hp).mpr
    (Nat.not_dvd_of_pos_of_lt (by omega) hkp))

/-- For prime p, newFracs p = Ico 1 p (filter is trivial). -/
lemma newFracs_eq_Ico (p : ℕ) (hp : Nat.Prime p) :
    newFracs p = Finset.Ico 1 p := by
  unfold newFracs
  ext k
  simp only [Finset.mem_filter, Finset.mem_Ico]
  exact ⟨And.left, fun ⟨h1, h2⟩ => ⟨⟨h1, h2⟩, prime_coprime_lt p k hp h1 h2⟩⟩

/-- |newFracs p| = p - 1 for prime p. -/
lemma newFracs_card (p : ℕ) (hp : Nat.Prime p) :
    (newFracs p).card = p - 1 := by
  rw [newFracs_eq_Ico p hp, Finset.Ico_card]
  simp

/-- Complement closure: k ∈ newFracs p → p - k ∈ newFracs p. -/
lemma newFracs_complement (p : ℕ) (hp : Nat.Prime p) (k : ℕ) (hk : k ∈ newFracs p) :
    p - k ∈ newFracs p := by
  rw [newFracs_eq_Ico p hp] at hk ⊢
  simp only [Finset.mem_Ico] at hk ⊢
  omega

/-- No fixed points: for odd prime p ≥ 3 and k ∈ newFracs p, k ≠ p - k. -/
lemma newFracs_no_fixpoint (p k : ℕ) (hp : Nat.Prime p) (hp3 : 3 ≤ p)
    (hk : k ∈ newFracs p) : k ≠ p - k := by
  rw [newFracs_eq_Ico p hp] at hk
  simp only [Finset.mem_Ico] at hk
  -- k = p - k ↔ 2k = p; impossible for odd prime p
  have hodd : p % 2 = 1 := by
    have h2 : Nat.Prime 2 := by decide
    have : ¬ (2 : ℕ) ∣ p := by
      intro hdvd
      have := (Nat.Prime.dvd_iff_eq h2 hp.ne_one).mp hdvd
      omega
    omega
  omega

/-! ## Key Reflection Lemmas -/

/-
PROBLEM
For (a, b) ∈ fareySet N with 1 ≤ a < b (and a/b ≠ 1/2, which holds for prime b),
  fareyRank N a b + fareyRank N (b - a) b = (fareySet N).card - 1.

PROVIDED SOLUTION
Let f = a/b and g = (b-a)/b = 1 - f. Note f + g = 1, f ≠ g (since a ≠ b/2).

The Farey involution φ: (c,d) ↦ (d-c, d) maps fareySet N to itself bijectively
(proved in FareySymmetry.lean as fareyInvol_mem and fareyInvol_invol).
Under φ: c/d < f ↔ (d-c)/d > g ↔ φ(c,d) > g.

So φ bijects {elements strictly < f} with {elements strictly > g}.

Total count:
  #{< f} + #{= f} + #{between f and g} + #{= g} + #{> g} = n
Note f < g (since a < b/2 when a < b and a + (b-a) = b; actually f < 1/2 < g or f > 1/2 > g).
When f < 1/2 < g (which holds for k/p with k < p/2):
  #{< f} + 1 + #{f < x < g} + 1 + #{> g} = n
  fareyRank(f) + #{strictly between} + #{> g} + 1 = n - 1.

Actually simpler: since φ bijects {< f} with {> g},
  #{< f} = #{> g}.
Also a/b is distinct from (b-a)/b (f ≠ g).
Count: #{< f} + 1_{f ∈ F} + #{f < x < g} + 1_{g ∈ F} + #{> g} = n.
Both f=(a,b) and g=(b-a,b) are in fareySet N (by hmem and fareyInvol_mem).
So: #{< f} + #{< g} + [count between] + 2 = n... this is getting complicated.

Simpler direct proof:
fareyRank N a b = #{x ∈ F_N | x < f}
fareyRank N (b-a) b = #{x ∈ F_N | x < g} = #{x ∈ F_N | x < 1-f} = #{x ∈ F_N | 1-x > f}
  = #{φ(x) ∈ F_N | φ(x) > f} = #{y ∈ F_N | y > f} (since φ is a bijection)
  = n - fareyRank N a b - 1  (subtracting the n-#{<f} total minus the f element itself).

Wait: #{x < f} + #{x = f} + #{x > f} = n.
So #{x > f} = n - fareyRank N a b - 1.
And fareyRank N (b-a) b = #{x > f} = n - fareyRank N a b - 1.
Therefore: fareyRank N a b + fareyRank N (b-a) b = n - 1.

Key step: fareyRank N (b-a) b = #{x ∈ F_N | x > f}.
Proof: x < (b-a)/b ↔ x < 1-f ↔ 1-x > f (since 1-x = (d-c)/d for x=c/d,
and the involution maps x ↦ 1-x within F_N when x ≠ 1).
But we need to handle x = 1/1: 1-1 = 0 = 0/1 which IS in F_N.
φ(1,1) = (0,1) ∈ F_N. So φ bijects ALL of F_N to F_N.
x < g = (b-a)/b biject with φ(x) > 1-g = f via the bijection φ.
So #{x < g} = #{φ(x) > f} = #{y > f} (letting y = φ(x)).

For the bijection to work on the full F_N:
#{x ∈ F_N | x < g} = #{y ∈ F_N | y > f}   (using φ: x ↦ 1-x)
  [because: x < (b-a)/b ↔ x < 1-f ↔ 1-x > f ↔ φ(x) > f]
And #{y ∈ F_N | y > f} = n - #{x < f} - 1 = n - fareyRank(f) - 1.
So fareyRank(f) + fareyRank(g) = fareyRank(f) + n - fareyRank(f) - 1 = n - 1. QED.

Implementation: Use Finset.card_compl or a direct bijection argument.
The bijection φ = fareyInvol from FareySymmetry.lean works here.
-/
lemma farey_reflection_rank (N a b : ℕ) (hN : 1 ≤ N) (hmem : (a, b) ∈ fareySet N)
    (ha : 1 ≤ a) (hab : a < b) :
    fareyRank N a b + fareyRank N (b - a) b = (fareySet N).card - 1 := by
  -- fareyRank N (b-a) b = #{x ∈ F_N | x > a/b}
  -- because x < (b-a)/b ↔ φ(x) = (d-c)/d < (b-a)/b is wrong...
  -- Actually: x < (b-a)/b ↔ the reflected element 1-x > a/b.
  -- Use the bijection fareyInvol from FareySymmetry.
  unfold fareyRank
  -- LHS = #{p | p.1*b < a*p.2} + #{p | p.1*b < (b-a)*p.2}
  -- We want to show this equals |fareySet N| - 1.
  -- Key: #{p | p.1*b < (b-a)*p.2} = #{p | a*p.2 < p.1*b}... no wait.
  -- p.1*b < (b-a)*p.2 ↔ p.1*b < b*p.2 - a*p.2 ↔ p.1*b - b*p.2 < -a*p.2
  -- ↔ b*(p.1 - p.2) < -a*p.2 ↔ b*(p.2 - p.1) > a*p.2 (when p.1 ≤ p.2)
  -- ↔ (p.2-p.1)/p.2 > a/b ↔ the reflected element is > a/b ↔ a*p.2 < p.1*b is FALSE.
  -- Careful: p.1*b < (b-a)*p.2 ↔ p.1/p.2 < (b-a)/b ↔ p.1/p.2 < 1 - a/b
  --   ↔ 1 - p.1/p.2 > a/b ↔ (p.2 - p.1)/p.2 > a/b ↔ a*p.2 < (p.2-p.1)*b.
  -- So #{p | p.1*b < (b-a)*p.2} = #{p | a*p.2 < (p.2-p.1)*b}
  --   = #{q | a*q.2 < q.1*b} where q = fareyInvol p = (p.2-p.1, p.2)
  --   = #{q ∈ fareySet N | a*q.2 < q.1*b} (since fareyInvol is a bijection of fareySet N)
  -- And #{p | p.1*b < a*p.2} = #{p ∈ fareySet N | p.1*b < a*p.2}.
  -- Sum = #{p | p.1*b < a*p.2} + #{q | a*q.2 < q.1*b}
  --     = #{elements strictly less than a/b} + #{elements strictly greater than a/b}
  --     = |fareySet N| - 1  (subtracting the unique element equal to a/b).
  sorry

/-- For (a, b) ∈ fareySet N with 1 ≤ a < b,
    D₁(a/b) + D₁((b-a)/b) = 1  (using 1-indexed rank). -/
lemma disc1_reflection (N a b : ℕ) (hN : 1 ≤ N) (hmem : (a, b) ∈ fareySet N)
    (ha : 1 ≤ a) (hab : a < b) :
    let n := (fareySet N).card
    let disc1 := fun x y : ℕ => (fareyRank N x y : ℚ) + 1 - n * ((x : ℚ) / y)
    disc1 a b + disc1 (b - a) b = 1 := by
  simp only
  have hb : (0 : ℚ) < b := by
    have := (mem_fareySet_iff.mp hmem).2.1
    exact_mod_cast Nat.pos_of_ne_zero (by omega)
  have hN_pos : 1 ≤ (fareySet N).card := by
    have : (0, 1) ∈ fareySet N := by
      rw [mem_fareySet_iff]; simp; omega
    exact Nat.one_le_iff_ne_zero.mpr (Finset.card_ne_zero.mpr ⟨_, this⟩)
  have hfrac : (a : ℚ) / b + ((b - a : ℕ) : ℚ) / b = 1 := by
    rw [Nat.cast_sub (Nat.le_of_lt_succ (Nat.lt_succ_of_lt hab))]
    field_simp; ring
  have hrank := farey_reflection_rank N a b hN hmem ha hab
  have hcard_pos : 1 ≤ (fareySet N).card := hN_pos
  push_cast
  have : (fareyRank N a b : ℚ) + (fareyRank N (b - a) b : ℚ) =
      (fareySet N).card - 1 := by exact_mod_cast hrank
  linarith [show (fareySet N).card * ((a : ℚ) / ↑b) +
    (fareySet N).card * ((↑(b - a) : ℚ) / ↑b) = (fareySet N).card by
      rw [← hfrac]; ring]

/-! ## Main Theorem -/

/-- Key membership: for prime p and k ∈ newFracs p, (k, p) ∈ fareySet p. -/
lemma newFracs_mem_fareySet (p k : ℕ) (hp : Nat.Prime p) (hk : k ∈ newFracs p) :
    (k, p) ∈ fareySet p := by
  rw [newFracs_eq_Ico p hp] at hk
  simp only [Finset.mem_Ico] at hk
  rw [mem_fareySet_iff]
  exact ⟨by omega, le_refl p, by omega, Nat.le_of_lt_succ (Nat.lt_succ_of_lt hk.2),
         prime_coprime_lt p k hp hk.1 hk.2⟩

/-- The involution p - k preserves bounds (k < p means p - k < p). -/
lemma newFracs_complement_lt (p k : ℕ) (hk_mem : k ∈ Finset.Ico 1 p) :
    1 ≤ p - k ∧ p - k < p := by
  simp only [Finset.mem_Ico] at hk_mem; omega

/-- Main theorem: Σ_{k=1}^{p-1} D₁(k/p) = (p-1)/2 for prime p ≥ 3. -/
theorem new_fraction_disc1_sum (p : ℕ) (hp : Nat.Prime p) (hp3 : 3 ≤ p) :
    ∑ k ∈ newFracs p, newFracDisc1 p k = ((p : ℚ) - 1) / 2 := by
  -- Step 1: rewrite as shifted sum
  -- D₁(k/p) - 1/2 + D₁((p-k)/p) - 1/2 = 0 for each pair
  have hpair : ∀ k ∈ newFracs p,
      newFracDisc1 p k - 1/2 + (newFracDisc1 p (p - k) - 1/2) = 0 := by
    intro k hk
    unfold newFracDisc1 fareyRank1
    -- Apply disc1_reflection with N=p, a=k, b=p
    rw [newFracs_eq_Ico p hp] at hk
    simp only [Finset.mem_Ico] at hk
    have hmem := newFracs_mem_fareySet p k hp (by rwa [newFracs_eq_Ico p hp,
      Finset.mem_Ico])
    have hrefl := disc1_reflection p k p (Nat.Prime.one_le hp) hmem hk.1 hk.2
    simp only at hrefl
    -- hrefl : (fareyRank p k p + 1 - |F_p| * (k/p)) + (fareyRank p (p-k) p + 1 - |F_p|*((p-k)/p)) = 1
    -- Goal: (fareyRank p k p + 1 - |F_p| * (k/p)) - 1/2 +
    --        ((fareyRank p (p-k) p + 1) - |F_p| * ((p-k)/p) - 1/2) = 0
    linarith
  -- Step 2: sum the shifted discrepancies using involution
  have hsum_shifted : ∑ k ∈ newFracs p, (newFracDisc1 p k - 1/2) = 0 := by
    apply Finset.sum_involution (fun k _ => p - k)
    · -- cancellation
      intro k hk
      linarith [hpair k hk]
    · -- no fixed points
      intro k hk _
      exact newFracs_no_fixpoint p k hp hp3 hk
    · -- closure
      exact fun k hk _ => newFracs_complement p hp k hk
    · -- involutive: p - (p - k) = k
      intro k hk
      rw [newFracs_eq_Ico p hp] at hk
      simp only [Finset.mem_Ico] at hk
      omega
  -- Step 3: extract the main sum
  have hcard : (newFracs p).card = p - 1 := newFracs_card p hp
  rw [Finset.sum_sub_distrib] at hsum_shifted
  simp only [Finset.sum_const, nsmul_eq_mul] at hsum_shifted
  linarith [show ((newFracs p).card : ℚ) * (1 / 2) = ((p : ℚ) - 1) / 2 by
    push_cast [hcard]
    have hp1 : 1 ≤ p := Nat.Prime.one_le hp
    push_cast [Nat.sub_one_eq_pred, show p - 1 + 1 = p from by omega]
    ring]
