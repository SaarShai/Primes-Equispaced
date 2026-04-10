import Mathlib
import PrimeCircle

open Finset BigOperators

/-- The sum of fractions in F_N: Σ_{(a,b)∈fareySet N} a/b. -/
noncomputable def fareySumFractions' (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N, ((ab.1 : ℚ) / ab.2)

/-- The Farey involution: (a, b) ↦ (b - a, b). -/
def fareyInvol (ab : ℕ × ℕ) : ℕ × ℕ := (ab.2 - ab.1, ab.2)

/-- Membership in fareySet unpacked. -/
lemma mem_fareySet_iff {N : ℕ} {ab : ℕ × ℕ} :
    ab ∈ fareySet N ↔ ab.1 ≤ N ∧ ab.2 ≤ N ∧ 1 ≤ ab.2 ∧ ab.1 ≤ ab.2 ∧ Nat.Coprime ab.1 ab.2 := by
  simp [fareySet, Finset.mem_filter, Finset.mem_product, Finset.mem_range]
  omega

/-
PROBLEM
gcd(b - a, b) = gcd(a, b) when a ≤ b.

PROVIDED SOLUTION
gcd(b-a, b) = gcd(b-a, b - (b-a)) = gcd(b-a, a) = gcd(a, b-a). But also gcd(a, b) = gcd(a, b-a) when a ≤ b. Use Nat.Coprime.sub_self or Nat.coprime_sub_self_left or similar Mathlib lemma. Alternatively, use that gcd(b-a, b) divides gcd(a, b) since any divisor of b-a and b also divides a = b - (b-a).
-/
lemma coprime_sub {a b : ℕ} (hab : a ≤ b) (hc : Nat.Coprime a b) :
    Nat.Coprime (b - a) b := by
  simpa [ hab ] using hc

/-
PROBLEM
The Farey involution maps fareySet N to itself.

PROVIDED SOLUTION
From h, using mem_fareySet_iff we get a ≤ N, b ≤ N, 1 ≤ b, a ≤ b, Coprime a b. Need to show (b-a, b) ∈ fareySet N, i.e., b-a ≤ N, b ≤ N, 1 ≤ b, b-a ≤ b, Coprime (b-a) b. All follow from the hypotheses. b-a ≤ b is Nat.sub_le. b-a ≤ N follows from b-a ≤ b ≤ N. Coprimality from coprime_sub.
-/
lemma fareyInvol_mem {N : ℕ} {ab : ℕ × ℕ} (h : ab ∈ fareySet N) :
    fareyInvol ab ∈ fareySet N := by
  rw [ fareyInvol ];
  rw [ mem_fareySet_iff ] at *;
  exact ⟨ Nat.sub_le_of_le_add <| by linarith, by linarith, by linarith, Nat.sub_le _ _, by simpa [ h.2.2.2.1 ] using h.2.2.2.2 ⟩

/-
PROBLEM
The Farey involution is an involution.

PROVIDED SOLUTION
fareyInvol (fareyInvol (a,b)) = fareyInvol (b-a, b) = (b-(b-a), b) = (a, b). Use Nat.sub_sub_self (from fareySet membership, a ≤ b). Get a ≤ b from mem_fareySet_iff.
-/
lemma fareyInvol_invol {N : ℕ} {ab : ℕ × ℕ} (h : ab ∈ fareySet N) :
    fareyInvol (fareyInvol ab) = ab := by
  -- By definition of fareyInvol, we have fareyInvol (fareyInvol ab) = (ab.2 - (ab.2 - ab.1), ab.2).
  simp [fareyInvol];
  rw [ Nat.sub_sub_self ( by linarith [ mem_fareySet_iff.mp h ] ) ]

/-
PROBLEM
The shifted fractions sum to zero under the involution.

PROVIDED SOLUTION
From h we get a ≤ b and 1 ≤ b. Cast to ℚ: (a : ℚ)/b - 1/2 + ((b - a : ℕ) : ℚ)/b - 1/2. Note (b - a : ℕ) cast to ℚ equals (b : ℚ) - (a : ℚ) since a ≤ b. So the sum is a/b + (b-a)/b - 1 = a/b + 1 - a/b - 1 = 0. Use Nat.cast_sub, field_simp.
-/
lemma fareyInvol_cancel {ab : ℕ × ℕ} (h : ab ∈ fareySet N) :
    ((ab.1 : ℚ) / ab.2 - 1/2) + (((ab.2 - ab.1 : ℕ) : ℚ) / ab.2 - 1/2) = 0 := by
  rw [ Nat.cast_sub ( by linarith [ mem_fareySet_iff.mp h ] ) ] ; ring;
  rw [ mul_inv_cancel₀ ( Nat.cast_ne_zero.mpr ( by linarith [ mem_fareySet_iff.mp h ] ) ), neg_add_eq_zero ]

/-
PROBLEM
At fixed points of the involution, a/b - 1/2 = 0.

PROVIDED SOLUTION
If fareyInvol (a,b) = (a,b) then (b-a, b) = (a, b), so b-a = a, meaning b = 2a (from a ≤ b). Then a/b = a/(2a) = 1/2. So a/b - 1/2 = 0. Get a ≤ b from mem_fareySet_iff.
-/
lemma fareyInvol_fixed_zero {ab : ℕ × ℕ} (h : ab ∈ fareySet N)
    (hfixed : fareyInvol ab = ab) :
    (ab.1 : ℚ) / ab.2 - 1/2 = 0 := by
  unfold fareyInvol at hfixed;
  grind +suggestions

/-
PROBLEM
Farey symmetry: Σ_{f∈F_N} f = n/2 where n = |F_N|.

PROVIDED SOLUTION
Rewrite fareySumFractions' as ∑ ab ∈ fareySet N, (ab.1 : ℚ)/ab.2. We want this equals card/2, equivalently ∑ ab, (ab.1/ab.2 - 1/2) = 0. Use Finset.sum_sub_distrib to split: fareySumFractions' N - ∑ ab, 1/2 = 0. The second sum is card * (1/2) = card/2. So fareySumFractions' N = card/2.

Actually, more directly: use Finset.sum_involution with g = fareyInvol (as a dependent function on membership), f(ab) = ab.1/ab.2 - 1/2. The conditions are:
1. f(a) + f(g(a)) = 0: this is fareyInvol_cancel
2. f(a) ≠ 0 → g(a) ≠ a: this is the contrapositive of fareyInvol_fixed_zero
3. g(a) ∈ s: this is fareyInvol_mem
4. g(g(a)) = a: this is fareyInvol_invol

This gives ∑ ab, (ab.1/ab.2 - 1/2) = 0. Then use Finset.sum_sub_distrib to rewrite as fareySumFractions' N - card/2 = 0, hence fareySumFractions' N = card/2.
-/
lemma farey_sum_symmetry' (N : ℕ) (hN : 1 ≤ N) :
    fareySumFractions' N = (fareySet N).card / 2 := by
  unfold fareySumFractions' fareySet; ring; norm_num;
  -- By pairing each fraction with its complement, we can show that the sum of the fractions in F_N is equal to the sum of their complements.
  have h_pair : ∑ x ∈ Finset.filter (fun p => 1 ≤ p.2 ∧ p.1 ≤ p.2 ∧ Nat.Coprime p.1 p.2) (Finset.product (Finset.range (1 + N)) (Finset.range (1 + N))), (x.1 : ℚ) / x.2 = ∑ x ∈ Finset.filter (fun p => 1 ≤ p.2 ∧ p.1 ≤ p.2 ∧ Nat.Coprime p.1 p.2) (Finset.product (Finset.range (1 + N)) (Finset.range (1 + N))), (1 - (x.1 : ℚ) / x.2) := by
    apply Finset.sum_bij (fun x hx => (x.2 - x.1, x.2)) _ _ _ _ <;> simp_all +decide [ add_comm, Finset.mem_filter, Finset.mem_product ];
    · grind +extAll;
    · intros; omega;
    · exact fun a b ha hb hb' hab h => ⟨ b - a, ⟨ by omega, by omega, by simpa [ hab ] using h ⟩, by omega ⟩;
    · intro a b _ _ _ _ _; rw [ one_sub_div ( by positivity ) ] ; ring;
  norm_num [ Finset.sum_add_distrib ] at * ; linarith!;