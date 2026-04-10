import Mathlib
import PrimeCircle

open Finset BigOperators Nat

/-!
# Denominator Displacement Sum Identity

For any Farey sequence F_N with n = |F_N| elements, and any denominator b with 2 ≤ b ≤ N:

  Σ_{a coprime b, 0<a<b} D(a/b) = -φ(b)/2

where D(a/b) = rank(a/b, F_N) - n·(a/b) is the displacement, and φ is Euler's totient.

## Proof Strategy
1. The coprime residues mod b pair up via a ↔ b-a, with Σ a = b·φ(b)/2
2. In F_N, the symmetry f ↔ 1-f maps rank j to rank n-1-j
3. So rank(a/b) + rank((b-a)/b) = n-1 for each pair
4. Summing: Σ rank(a/b) = φ(b)·(n-1)/2
5. Therefore Σ D = φ(b)·(n-1)/2 - n·φ(b)/2 = -φ(b)/2
-/

/-! ## Definitions -/

/-- The coprime residues: {a : 0 < a < b, gcd(a,b) = 1}. -/
def coprimeResidues (b : ℕ) : Finset ℕ :=
  (Finset.Ico 1 b).filter (fun a => Nat.Coprime a b)

/-- The rank of fraction a/b in F_N: number of elements (c,d) ∈ fareySet N with c/d < a/b,
    computed via cross-multiplication c·b < a·d. -/
def fareyRank (N a b : ℕ) : ℕ :=
  ((fareySet N).filter (fun p => p.1 * b < a * p.2)).card

/-! ## Computational Verification

We verify the identity computationally for small cases using `native_decide`.
The integer-form identity is: 2 * Σ rank(a/b) = (n-1) * φ(b).
-/

-- Verify Farey set cardinalities
example : (fareySet 4).card = 7 := by native_decide
example : (fareySet 6).card = 13 := by native_decide

-- F_4, b=3: coprime residues {1, 2}, ranks 2 and 4
-- D(1/3) = 2 - 7/3 = -1/3, D(2/3) = 4 - 14/3 = -2/3, Sum = -1 = -φ(3)/2 ✓
example : coprimeResidues 3 = {1, 2} := by native_decide
example : fareyRank 4 1 3 = 2 := by native_decide
example : fareyRank 4 2 3 = 4 := by native_decide

-- Integer form: 2 * Σ rank = (n-1) * φ(b), verified for F_4, b=3
example : 2 * (∑ a ∈ coprimeResidues 3, fareyRank 4 a 3) =
    ((fareySet 4).card - 1) * Nat.totient 3 := by native_decide

-- Coprime sum: 2 * Σ a = b * φ(b), verified for b=3
example : 2 * (∑ a ∈ coprimeResidues 3, a) = 3 * Nat.totient 3 := by native_decide

-- F_6, b=5: φ(5) = 4, displacement sum should be -2
example : 2 * (∑ a ∈ coprimeResidues 5, fareyRank 6 a 5) =
    ((fareySet 6).card - 1) * Nat.totient 5 := by native_decide
example : 2 * (∑ a ∈ coprimeResidues 5, a) = 5 * Nat.totient 5 := by native_decide

-- Additional: F_5, b=4, φ(4)=2, fractions 1/4, 3/4
example : 2 * (∑ a ∈ coprimeResidues 4, fareyRank 5 a 4) =
    ((fareySet 5).card - 1) * Nat.totient 4 := by native_decide

/-! ## Coprime Residues Lemmas -/

/-
PROBLEM
Cardinality of coprime residues equals Euler's totient.

PROVIDED SOLUTION
coprimeResidues b = (Ico 1 b).filter (Coprime · b).
Nat.totient_eq_card_coprime says totient b = (range b).filter (Coprime b ·) |>.card.
Since Coprime is symmetric, (Coprime b a ↔ Coprime a b).
The difference between Ico 1 b and range b is just the element 0.
For b ≥ 2, Coprime 0 b means gcd 0 b = b = 1, which is false since b ≥ 2.
So (range b).filter (Coprime · b) = (Ico 1 b).filter (Coprime · b) ∪ (if Coprime 0 b then {0} else ∅).
Since Coprime 0 b is false for b ≥ 2, the sets are equal.
Use Finset.range_eq_Ico to relate range b = Ico 0 b, then Ico 0 b = {0} ∪ Ico 1 b, filter distributes, and filter on {0} is empty.
-/
lemma coprimeResidues_card (b : ℕ) (hb : 2 ≤ b) :
    (coprimeResidues b).card = Nat.totient b := by
  unfold coprimeResidues;
  congr 1 with x ; simp +decide [ Nat.coprime_comm ];
  exact fun _ _ => Nat.pos_of_ne_zero ( by aesop )

/-
PROBLEM
If a ∈ coprimeResidues b, then b - a ∈ coprimeResidues b (for b ≥ 2).

PROVIDED SOLUTION
a ∈ coprimeResidues b means: a ∈ Ico 1 b (i.e., 1 ≤ a < b) and Nat.Coprime a b.

Need to show b - a ∈ coprimeResidues b:
1. b - a ∈ Ico 1 b: since 1 ≤ a < b, we have 1 ≤ b - a < b. The lower bound: b - a ≥ 1 since a < b means a ≤ b - 1. The upper bound: b - a < b since a ≥ 1.
2. Nat.Coprime (b - a) b: gcd(b - a, b) = gcd(b - a, b). Since b = (b - a) + a, gcd(b-a, b) = gcd(b-a, a) = gcd(a, b-a). And gcd(a, b-a) divides gcd(a, b) = 1 since b = a + (b-a). Actually: use Nat.Coprime.sub_self or the fact that gcd(b-a, b) = gcd(a, b). The key identity is Nat.coprime_sub_self or Nat.Coprime.symm with sub. We can use that gcd(n-a, n) = gcd(a, n) for a ≤ n. This follows from gcd(n-a, n) = gcd(n-a, n - (n-a)) = gcd(n-a, a) = gcd(a, n-a) and gcd(a, n) = gcd(a, n - a) by the Euclidean step.
-/
lemma complement_mem_coprimeResidues (b a : ℕ) (hb : 2 ≤ b) (ha : a ∈ coprimeResidues b) :
    b - a ∈ coprimeResidues b := by
  -- Since $a \in \text{coprimeResidues } b$, we have $1 \leq a < b$ and $\gcd(a, b) = 1$.
  obtain ⟨ha1, ha2⟩ : 1 ≤ a ∧ a < b ∧ Nat.Coprime a b := by
    unfold coprimeResidues at ha; aesop;
  exact Finset.mem_filter.mpr ⟨ Finset.mem_Ico.mpr ⟨ Nat.sub_pos_of_lt ha2.1, Nat.sub_lt ( by linarith ) ( by linarith ) ⟩, by simpa [ ha2.1.le ] using ha2.2 ⟩

/-
PROBLEM
The complement map a ↦ b - a is an involution on coprimeResidues b.

PROVIDED SOLUTION
Since a ∈ coprimeResidues b, we have a ∈ Ico 1 b, so 1 ≤ a and a < b. Therefore a ≤ b, so b - a ≤ b, and since a < b we get b - a ≥ 1 > 0, so b - a ≤ b - 1 < b. Hence b - (b - a) = a by Nat.sub_sub_self (since a ≤ b, actually a < b so a ≤ b).
-/
lemma complement_invol (b : ℕ) (hb : 2 ≤ b) (a : ℕ) (ha : a ∈ coprimeResidues b) :
    b - (b - a) = a := by
  rw [ Nat.sub_sub_self ( by linarith [ Finset.mem_Ico.mp ( Finset.mem_filter.mp ha |>.1 ) ] ) ]

/-
PROBLEM
Sum identity: 2 * Σ_{a ∈ coprimeResidues b} a = b * φ(b) (over ℕ).

PROVIDED SOLUTION
The involution a ↦ b - a on coprimeResidues b pairs elements such that a + (b-a) = b.

Step 1: Σ_{a ∈ coprimeResidues b} (a + (b - a)) = Σ_{a ∈ coprimeResidues b} b = b * card(coprimeResidues b).

Step 2: By the involution (complement_mem_coprimeResidues, complement_invol), Σ (b - a) = Σ a.
Use Finset.sum_involution or Finset.sum_bij with the map a ↦ b - a to show Σ (b-a) = Σ a.
Or simply: Σ (a + (b-a)) = Σ a + Σ (b-a) and Σ (b-a) = Σ a by reindexing via the bijection.

Step 3: So 2 * Σ a = b * card = b * totient b (using coprimeResidues_card).
-/
lemma coprime_residues_sum_nat (b : ℕ) (hb : 2 ≤ b) :
    2 * ∑ a ∈ coprimeResidues b, a = b * Nat.totient b := by
  -- By definition of coprime residues, we can pair each element with its complement to b.
  have h_pair : ∑ a ∈ coprimeResidues b, a = ∑ a ∈ coprimeResidues b, (b - a) := by
    apply Finset.sum_bij (fun a ha => b - a);
    · exact fun a ha => complement_mem_coprimeResidues b a hb ha;
    · exact fun a₁ ha₁ a₂ ha₂ h => by rw [ tsub_right_inj ] at h <;> linarith [ Finset.mem_Ico.mp ( Finset.mem_filter.mp ha₁ |>.1 ), Finset.mem_Ico.mp ( Finset.mem_filter.mp ha₂ |>.1 ) ] ;
    · exact fun x hx => ⟨ b - x, complement_mem_coprimeResidues b x hb hx, Nat.sub_sub_self ( le_of_lt ( Finset.mem_Ico.mp ( Finset.mem_filter.mp hx |>.1 ) |>.2 ) ) ⟩;
    · exact fun a ha => by rw [ Nat.sub_sub_self ( le_of_lt ( Finset.mem_Ico.mp ( Finset.mem_filter.mp ha |>.1 ) |>.2 ) ) ] ;
  -- By combining the results from the pairing and the sum of the complements, we get:
  have h_combined : ∑ a ∈ coprimeResidues b, a + ∑ a ∈ coprimeResidues b, (b - a) = b * (coprimeResidues b).card := by
    rw [ ← Finset.sum_add_distrib, Finset.sum_congr rfl fun x hx => add_tsub_cancel_of_le <| by linarith [ Finset.mem_Ico.mp <| Finset.mem_filter.mp hx |>.1 ] ] ; simp +decide [ mul_comm ];
  rw [ two_mul, coprimeResidues_card b hb ] at * ; linarith

/-
PROBLEM
Sum identity over ℚ: 2 * Σ (a : ℚ) = (b : ℚ) * φ(b).

PROVIDED SOLUTION
Cast coprime_residues_sum_nat to ℚ: from 2 * Σ a = b * totient b over ℕ, cast both sides to ℚ using Nat.cast.
-/
lemma coprime_residues_sum_rat (b : ℕ) (hb : 2 ≤ b) :
    2 * ∑ a ∈ coprimeResidues b, (a : ℚ) = (b : ℚ) * (Nat.totient b : ℚ) := by
  rw [ ← Nat.cast_sum, ← Nat.cast_mul ] ; exact mod_cast coprime_residues_sum_nat b hb

/-! ## Farey Symmetry Lemmas -/

/-
PROBLEM
The complement (q-a, q) of a Farey fraction (a, q) is also in fareySet N.

PROVIDED SOLUTION
Given (a, q) ∈ fareySet N, from the definition we have: q ∈ range (N+1), a ∈ range (N+1), 1 ≤ q, a ≤ q, Coprime a q.
Need (q - a, q) ∈ fareySet N:
- q - a ∈ range (N+1): q - a ≤ q ≤ N, so q - a < N + 1. ✓
- q ∈ range (N+1): same as before. ✓
- 1 ≤ q: same. ✓
- q - a ≤ q: obvious (Nat.sub_le). ✓
- Coprime (q - a) q: gcd(q - a, q) = gcd(a, q) = 1 since gcd(n - k, n) = gcd(k, n) for k ≤ n. Use the fact that coprimality is preserved under subtraction from the modulus.
-/
lemma complement_mem_fareySet' (N a q : ℕ) (h : (a, q) ∈ fareySet N) :
    (q - a, q) ∈ fareySet N := by
  unfold fareySet at *;
  simp +zetaDelta at *;
  exact ⟨ ⟨ by linarith, by linarith ⟩, by linarith, by simpa [ h.2.2.1 ] using h.2.2.2 ⟩

/-
PROBLEM
For coprime a, b with a ≤ b, if a * d = c * b then a = c and b = d.

PROVIDED SOLUTION
Since a * d = c * b and gcd(a,b) = 1, we have b | d (since b | a*d = c*b... wait that's trivially true). Let me think again.

a * d = c * b with gcd(a,b) = 1 and gcd(c,d) = 1.

From a * d = c * b and gcd(a,b) = 1: b divides a*d, and since gcd(a,b) = 1, b divides d.
From a * d = c * b and gcd(c,d) = 1: d divides c*b, and since gcd(c,d) = 1, d divides b.
So b | d and d | b, hence b = d (both positive).
Then a * b = c * b, so a = c.

Use Nat.Coprime.dvd_of_dvd_mul_right or similar Mathlib lemmas.
-/
lemma reduced_fraction_unique (a b c d : ℕ)
    (hb : 0 < b) (hd : 0 < d)
    (hab : Nat.Coprime a b) (hcd : Nat.Coprime c d)
    (h : a * d = c * b) : a = c ∧ b = d := by
  -- Since $a$ and $b$ are coprime and $a * d = c * b$, it follows that $b$ divides $d$ and $d$ divides $b$, hence $b = d$.
  have h_bd : b ∣ d ∧ d ∣ b := by
    exact ⟨ hab.symm.dvd_of_dvd_mul_left <| h.symm ▸ dvd_mul_left _ _, hcd.symm.dvd_of_dvd_mul_left <| h ▸ dvd_mul_left _ _ ⟩;
  have := Nat.dvd_antisymm h_bd.1 h_bd.2; aesop;

/-
PROBLEM
Element (a,b) is in fareySet N when a ∈ coprimeResidues b and b ≤ N.

PROVIDED SOLUTION
a ∈ coprimeResidues b means 1 ≤ a, a < b, and Nat.Coprime a b.
fareySet N = filter (fun p => 1 ≤ p.2 ∧ p.1 ≤ p.2 ∧ Nat.Coprime p.1 p.2) from (range (N+1) ×ˢ range (N+1)).
So (a, b) ∈ fareySet N iff:
- a ∈ range (N+1): a < N+1. Since a < b ≤ N, a < N+1. ✓
- b ∈ range (N+1): b < N+1. Since b ≤ N. ✓
- 1 ≤ b: since a ≥ 1 and a < b, b ≥ 2 ≥ 1. ✓
- a ≤ b: since a < b. ✓
- Nat.Coprime a b: given. ✓
-/
lemma mem_fareySet_of_coprimeResidues (N a b : ℕ) (hbN : b ≤ N)
    (ha : a ∈ coprimeResidues b) : (a, b) ∈ fareySet N := by
  -- By definition of coprimeResidues, we know that a is in the range 1 to b-1 and gcd(a, b) = 1.
  have ha_range : 1 ≤ a ∧ a < b ∧ Nat.Coprime a b := by
    unfold coprimeResidues at ha; aesop;
  exact Finset.mem_filter.mpr ⟨ Finset.mem_product.mpr ⟨ Finset.mem_range.mpr ( by linarith ), Finset.mem_range.mpr ( by linarith ) ⟩, by linarith, by linarith, ha_range.2.2 ⟩

/-
PROBLEM
Complement reverses cross-multiplication order: c*b < a*d ↔ (b-a)*d < (d-c)*b,
    when c ≤ d and a < b and d > 0.

PROVIDED SOLUTION
With natural subtraction, since a < b and c ≤ d and d > 0:
c * b < a * d ↔ (b - a) * d < (d - c) * b.

We can verify: (d - c) * b - (b - a) * d = db - cb - bd + ad = ad - cb.
And a * d - c * b = ad - cb.

So c * b < a * d ↔ ad - cb > 0 ↔ (d-c)*b - (b-a)*d > 0 ↔ (b-a)*d < (d-c)*b.

More carefully with natural subtraction:
Since a < b we have b - a > 0 and b - a + a = b.
Since c ≤ d we have d - c ≥ 0 and d - c + c = d.

Forward: Assume c*b < a*d, i.e., ad > cb.
(d-c)*b = db - cb and (b-a)*d = bd - ad = db - ad.
So (d-c)*b - (b-a)*d = (db - cb) - (db - ad) = ad - cb > 0.
Hence (b-a)*d < (d-c)*b.

Backward: analogous.

Use omega or work with integers (cast to ℤ and use omega).
-/
lemma complement_reverses_order (a b c d : ℕ) (hab : a < b) (hcd : c ≤ d) (hd : 0 < d) :
    c * b < a * d ↔ (b - a) * d < (d - c) * b := by
  constructor <;> intro h <;> nlinarith [ Nat.sub_add_cancel hab.le, Nat.sub_add_cancel hcd ] ;

/-
PROBLEM
The number of elements in fareySet N equal to a/b (via cross-multiplication)
    is exactly 1, when a ∈ coprimeResidues b and b ≤ N.

PROVIDED SOLUTION
We need to show there's exactly one element (c,d) in fareySet N with c*b = a*d.

First, (a,b) is in the filtered set: (a,b) ∈ fareySet N by mem_fareySet_of_coprimeResidues, and a*b = a*b trivially.

Second, uniqueness: if (c,d) ∈ fareySet N and c*b = a*d, then since (c,d) ∈ fareySet implies Coprime c d, and ha implies Coprime a b, by reduced_fraction_unique we get c = a and d = b.

So the filtered set is exactly {(a,b)}, which has card 1. Use Finset.card_eq_one.mpr with a witness.
-/
lemma fareySet_eq_singleton (N a b : ℕ) (hb : 2 ≤ b) (hbN : b ≤ N)
    (ha : a ∈ coprimeResidues b) :
    ((fareySet N).filter (fun p => p.1 * b = a * p.2)).card = 1 := by
  -- Since (a, b) is in the set and any other element (c, d) in the set must satisfy c = a and d = b, the set is a singleton.
  have h_singleton : ∀ p ∈ fareySet N, p.1 * b = a * p.2 → p = (a, b) := by
    intro p hp h_eq
    obtain ⟨c, d, hc, hd⟩ : ∃ c d, p = (c, d) ∧ 1 ≤ d ∧ c ≤ d ∧ Nat.Coprime c d ∧ c * b = a * d := by
      unfold fareySet at hp; aesop;
    have h_unique : c = a ∧ d = b := by
      apply reduced_fraction_unique;
      · linarith;
      · linarith;
      · exact hd.2.2.1;
      · exact Finset.mem_filter.mp ha |>.2;
      · grind;
    aesop;
  exact Finset.card_eq_one.mpr ⟨ ( a, b ), Finset.eq_singleton_iff_unique_mem.mpr ⟨ Finset.mem_filter.mpr ⟨ mem_fareySet_of_coprimeResidues N a b hbN ha, by ring ⟩, fun p hp => h_singleton p ( Finset.filter_subset _ _ hp ) ( Finset.mem_filter.mp hp |>.2 ) ⟩ ⟩

/-
PROBLEM
Rank symmetry: rank(a/b) + rank((b-a)/b) = |F_N| - 1.
    Proved by showing the complement map on fareySet reverses the ordering,
    and the unique element with c/d = a/b is (a,b) itself.

PROVIDED SOLUTION
We show rank(a/b) + rank((b-a)/b) = n - 1 where n = |fareySet N|.

Define three disjoint parts of fareySet N:
- A = {(c,d) : c*b < a*d}     (rank(a/b) = |A|)
- B = {(c,d) : c*b = a*d}     (|B| = 1 by fareySet_eq_singleton)
- C = {(c,d) : c*b > a*d}     (the rest)

|A| + |B| + |C| = n, so |A| + |C| = n - 1.

Now rank((b-a)/b) = |{(c,d) ∈ fareySet N : c*b < (b-a)*d}|.

The complement map φ: (c,d) ↦ (d-c, d) is a bijection on fareySet N (by complement_mem_fareySet', and it's an involution since (d-(d-c), d) = (c, d) when c ≤ d).

For (c,d) ∈ C (i.e., c*b > a*d, equivalently a*d < c*b):
The complement (d-c, d) satisfies: (d-c)*b < (b-a)*d ↔ c*b > a*d (by complement_reverses_order with roles swapped). Actually, complement_reverses_order says: c*b < a*d ↔ (b-a)*d < (d-c)*b. Taking the contrapositive/negation and using strict inequality: a*d < c*b ↔ (d-c)*b < (b-a)*d.

Wait, let me be more precise. complement_reverses_order says c*b < a*d ↔ (b-a)*d < (d-c)*b. So ¬(c*b < a*d) ↔ ¬((b-a)*d < (d-c)*b), i.e., a*d ≤ c*b ↔ (d-c)*b ≤ (b-a)*d.

For elements in C: c*b > a*d. By complement_reverses_order applied with swapped roles... Actually, let's just directly verify:
(d-c)*b < (b-a)*d ↔ db - cb < bd - ad ↔ ad < cb ↔ a*d < c*b, which is exactly what C means.

So φ maps C bijectively to {(c',d) ∈ fareySet N : c'*b < (b-a)*d} = the set counted by rank((b-a)/b).

Therefore rank((b-a)/b) = |C|, and rank(a/b) + rank((b-a)/b) = |A| + |C| = n - 1.

IMPLEMENTATION APPROACH: Rather than constructing the bijection explicitly, use a counting argument.

Partition fareySet N into three sets by the trichotomy of c*b vs a*d:
- filter (c*b < a*d) has card = fareyRank N a b
- filter (c*b = a*d) has card = 1 (by fareySet_eq_singleton)
- filter (c*b > a*d), call it C

Similarly partition by c*b vs (b-a)*d:
- filter (c*b < (b-a)*d) has card = fareyRank N (b-a) b

Show filter(c*b < (b-a)*d) = filter(c*b > a*d) by showing the conditions are equivalent for elements of fareySet:
For (c,d) ∈ fareySet N: c ≤ d and d ≥ 1, and ha gives a < b.
c*b < (b-a)*d ↔ cb < bd - ad ↔ cb + ad < bd ↔ ...
Actually, c*b < (b-a)*d = b*d - a*d. So c*b < b*d - a*d ↔ c*b + a*d < b*d ↔ a*d < b*d - c*b = (d-c)*b ↔ a*d < (d-c)*b.
And c*b > a*d ↔ a*d < c*b. That's not the same as a*d < (d-c)*b.

Hmm, I made an error. Let me reconsider.

c*b > a*d means c/d > a/b.
c*b < (b-a)*d means c/d < (b-a)/b = 1 - a/b, i.e., c/d + a/b < 1, i.e., (cb + ad)/bd < 1, i.e., cb + ad < bd.

These are NOT the same condition! Let me reconsider the argument.

Actually, the argument uses the complement MAP. We don't show the conditions are the same for the same element. We show that φ sends C to the set for rank((b-a)/b).

For (c,d) ∈ C: c*b > a*d. Apply φ to get (d-c, d).
Check (d-c)*b < (b-a)*d: (d-c)*b = db - cb, (b-a)*d = bd - ad = db - ad.
So (d-c)*b < (b-a)*d ↔ db - cb < db - ad ↔ ad < cb ↔ a*d < c*b. ✓ (This is the C condition.)

So φ maps C into {(c',d') : c'*b < (b-a)*d'}. Since φ is an involution on fareySet, and φ maps {c'*b < (b-a)*d'} back to C (by the same calculation), φ is a bijection between C and {c'*b < (b-a)*d'}.

Therefore fareyRank N (b-a) b = |C|.

And fareyRank N a b + fareyRank N (b-a) b = |A| + |C| = n - 1.

So the key equality is:
(fareySet N).card = |A| + |B| + |C| where
|A| = fareyRank N a b, |B| = 1, |C| = fareyRank N (b-a) b.

Approach: Show fareySet N = A ∪ B ∪ C (disjoint), so card = |A| + |B| + |C|.
Then |A| + |C| = card - |B| = card - 1.

Use Finset.filter_card_add_filter_neg_card_eq_card or a three-way partition via the trichotomy lt/eq/gt of c*b vs a*d.

Actually, the simplest approach:
fareySet = (filter (c*b < a*d)) ∪ (filter (c*b ≥ a*d))
|filter (c*b ≥ a*d)| = |filter (c*b = a*d)| + |filter (c*b > a*d)|

But showing this requires some work with Finset partitioning.

Alternative simpler approach:
n = |filter (< )| + |filter (= )| + |filter (> )|
  = fareyRank N a b + 1 + fareyRank N (b-a) b

For the last equality, show |filter (> )| = fareyRank N (b-a) b.

filter(c*b > a*d) on fareySet = filter((d-c)*b < (b-a)*d) on image of complement... this is complex in Lean.

Actually, maybe the cleanest approach is:
1. Show filter(c*b > a*d) has same card as filter(c'*b < (b-a)*d') by constructing a bijection.
2. The bijection is the complement map restricted to these filters.

Use Finset.card_bij or Finset.card_eq_of_equiv.

Key helper: for (c,d) ∈ fareySet N with c*b > a*d:
- (d-c, d) ∈ fareySet N (by complement_mem_fareySet')
- (d-c)*b < (b-a)*d (shown above)

And conversely for (c',d') ∈ fareySet N with c'*b < (b-a)*d':
- (d'-c', d') ∈ fareySet N
- (d'-c')*b > a*d'... wait, need to check. For (c', d') with c'*b < (b-a)*d':
  Apply complement to get (d'-c', d'). Check (d'-c')*b > a*d':
  (d'-c')*b vs a*d'. We have c'*b < (b-a)*d' = bd' - ad'. So c'b + ad' < bd'.
  (d'-c')*b = d'b - c'b. Since c'b < bd' - ad', we get d'b - c'b > ad'. ✓

So the complement is a bijection between filter(c*b > a*d) and filter(c'*b < (b-a)*d').

This gives |filter(c*b > a*d)| = |filter(c'*b < (b-a)*d')| = fareyRank N (b-a) b.

Then: n = fareyRank N a b + 1 + fareyRank N (b-a) b.
So: fareyRank N a b + fareyRank N (b-a) b = n - 1.

The proof has three parts:

Part 1: Partition fareySet N into three disjoint sets by trichotomy of c*b vs a*d:
  A = filter (c*b < a*d)  — card = fareyRank N a b
  B = filter (c*b = a*d)  — card = 1 (by fareySet_eq_singleton)
  C = filter (c*b > a*d)  — remaining

So |A| + |B| + |C| = n, hence |A| + |C| = n - 1.

Part 2: Show fareyRank N (b-a) b = |C|.

The complement map φ: (c,d) ↦ (d-c, d) maps C bijectively to the set {(c',d') ∈ fareySet : c'*b < (b-a)*d'}.

For any (c,d) ∈ fareySet with c*b > a*d (i.e., (c,d) ∈ C):
- φ(c,d) = (d-c, d) ∈ fareySet N (by complement_mem_fareySet')
- (d-c)*b < (b-a)*d, because: (d-c)*b = db - cb, (b-a)*d = db - ad, and cb > ad implies db - cb < db - ad. With natural subtraction: use nlinarith with Nat.sub_add_cancel for c ≤ d and a < b (from ha ∈ coprimeResidues).

For injectivity: if φ(c₁,d₁) = φ(c₂,d₂) then (d₁-c₁, d₁) = (d₂-c₂, d₂), so d₁=d₂ and c₁=c₂.

For surjectivity: given (c',d') with c'*b < (b-a)*d', the preimage is (d'-c', d'). Check:
- (d'-c', d') ∈ fareySet (by complement_mem_fareySet' applied to (c',d'))
- (d'-c')*b > a*d': because c'*b < (b-a)*d' implies (d'-c')*b > a*d' by the same arithmetic.

So |C| = |{(c',d') : c'*b < (b-a)*d'}| = fareyRank N (b-a) b.

Part 3: Combine: fareyRank N a b + fareyRank N (b-a) b = |A| + |C| = n - 1.

IMPORTANT IMPLEMENTATION NOTE: Use Finset.card_bij for the bijection. The key arithmetic facts needed are:
- For (c,d) ∈ fareySet: c ≤ d and d ≥ 1
- For a ∈ coprimeResidues b: 1 ≤ a and a < b, so a ≤ b
- Natural subtraction: (d-c)*b = d*b - c*b when c ≤ d, and (b-a)*d = b*d - a*d when a ≤ b
- Use these with nlinarith after Nat.sub_add_cancel

For the three-way partition, use a direct counting argument:
  card(fareySet) = card(filter lt) + card(filter eq) + card(filter gt)
This can be shown by showing every element falls into exactly one of the three categories (by trichotomy of natural number multiplication).
-/
set_option maxHeartbeats 400000 in
lemma rank_symmetry (N a b : ℕ) (hb : 2 ≤ b) (hbN : b ≤ N)
    (ha : a ∈ coprimeResidues b) :
    fareyRank N a b + fareyRank N (b - a) b = (fareySet N).card - 1 := by
  -- By definition of fareySet, we can partition it into three disjoint subsets based on the inequality $c*b < a*d$, $c*b = a*d$, and $c*b > a*d$.
  set A := ((fareySet N).filter (fun p => p.1 * b < a * p.2))
  set B := ((fareySet N).filter (fun p => p.1 * b = a * p.2))
  set C := ((fareySet N).filter (fun p => p.1 * b > a * p.2));
  -- By definition of fareySet, we know that fareySet N is partitioned into A, B, and C.
  have h_partition : fareySet N = A ∪ B ∪ C := by
    grind +ring;
  -- By definition of fareySet, we know that fareySet N is partitioned into A, B, and C, and |B| = 1.
  have h_card_B : B.card = 1 := by
    convert fareySet_eq_singleton N a b hb hbN ha using 1;
  -- By definition of fareySet, we know that fareySet N is partitioned into A, B, and C, and |C| = fareyRank N (b - a) b.
  have h_card_C : C.card = fareyRank N (b - a) b := by
    refine' Finset.card_bij ( fun p hp => ( p.2 - p.1, p.2 ) ) _ _ _ <;> simp +decide [ C ] at *;
    · intro x y hx hy; refine' ⟨ _, _ ⟩ <;> norm_num [ fareySet ] at *;
      · exact ⟨ ⟨ by linarith, by linarith ⟩, by linarith, by simpa [ hx.2.2.1 ] using hx.2.2.2 ⟩;
      · nlinarith only [ hy, hx, Nat.sub_add_cancel ( show x ≤ y from hx.2.2.1 ), Nat.sub_add_cancel ( show a ≤ b from by linarith [ Finset.mem_Ico.mp ( Finset.mem_filter.mp ha |>.1 ) ] ) ];
    · intro a₁ b₁ h₁ h₂ a₂ b₂ h₃ h₄ h₅ h₆; rw [ tsub_eq_iff_eq_add_of_le ] at h₅ <;> norm_num at * ;
      · constructor <;> nlinarith [ Nat.sub_add_cancel ( show a₂ ≤ b₂ from by { unfold fareySet at h₃; norm_num at h₃; linarith } ) ];
      · unfold fareySet at h₁; norm_num at h₁; linarith;
    · unfold coprimeResidues at ha; norm_num at ha;
      intro x y hx hy; use y - x; refine' ⟨ ⟨ _, _ ⟩, _ ⟩ <;> norm_num [ fareySet ] at *;
      · exact ⟨ ⟨ by linarith, by linarith ⟩, by linarith, by simpa [ hx.2.2.1 ] using hx.2.2.2 ⟩;
      · nlinarith only [ Nat.sub_add_cancel ( show x ≤ y from hx.2.2.1 ), Nat.sub_add_cancel ( show a ≤ b from ha.1.2.le ), hy ];
      · rw [ Nat.sub_sub_self hx.2.2.1 ];
  rw [ h_partition, Finset.card_union_of_disjoint, Finset.card_union_of_disjoint ] <;> norm_num [ h_card_B, h_card_C ];
  · simp only [A]; unfold fareyRank; omega;
  · exact Finset.disjoint_filter.mpr fun _ _ _ _ => by linarith;
  · exact ⟨ Finset.disjoint_filter.mpr fun _ _ _ _ => by linarith, Finset.disjoint_filter.mpr fun _ _ _ _ => by linarith ⟩

/-
PROBLEM
Sum of ranks: 2 * Σ rank(a/b) = (|F_N| - 1) * φ(b).
    Follows from rank_symmetry and the involution a ↦ b-a on coprimeResidues.

PROVIDED SOLUTION
2 * Σ_{a} fareyRank N a b
= Σ_{a} fareyRank N a b + Σ_{a} fareyRank N (b-a) b   [reindex second sum via involution a ↦ b-a]
= Σ_{a} (fareyRank N a b + fareyRank N (b-a) b)
= Σ_{a} ((fareySet N).card - 1)                        [by rank_symmetry]
= (coprimeResidues b).card * ((fareySet N).card - 1)
= totient b * ((fareySet N).card - 1)

For the reindexing, use Finset.sum_nbij with the bijection a ↦ b - a on coprimeResidues b.
Properties: complement_mem_coprimeResidues gives it maps into coprimeResidues, complement_invol gives it's an involution (hence bijective and surjective).
-/
lemma rank_sum_nat (N b : ℕ) (hb : 2 ≤ b) (hbN : b ≤ N) :
    2 * ∑ a ∈ coprimeResidues b, fareyRank N a b =
    ((fareySet N).card - 1) * Nat.totient b := by
  -- By the symmetry property of fareyRank, we can pair each element with its complement.
  have h_pair : ∑ a ∈ coprimeResidues b, fareyRank N a b = ∑ a ∈ coprimeResidues b, fareyRank N (b - a) b := by
    apply Finset.sum_bij (fun a ha => b - a);
    · exact fun a ha => complement_mem_coprimeResidues b a hb ha;
    · exact fun a₁ ha₁ a₂ ha₂ h => by rw [ tsub_right_inj ] at h <;> linarith [ Finset.mem_Ico.mp ( Finset.mem_filter.mp ha₁ |>.1 ), Finset.mem_Ico.mp ( Finset.mem_filter.mp ha₂ |>.1 ) ] ;
    · exact fun a ha => ⟨ b - a, complement_mem_coprimeResidues _ _ hb ha, Nat.sub_sub_self <| Finset.mem_Ico.mp ( Finset.mem_filter.mp ha |>.1 ) |>.2.le ⟩;
    · exact fun a ha => by rw [ Nat.sub_sub_self ( show a ≤ b from le_of_lt ( Finset.mem_Ico.mp ( Finset.mem_filter.mp ha |>.1 ) |>.2 ) ) ] ;
  -- Using the symmetry property of fareyRank, we can pair each element with its complement.
  have h_symm : ∑ a ∈ coprimeResidues b, (fareyRank N a b + fareyRank N (b - a) b) = (coprimeResidues b).card * ((fareySet N).card - 1) := by
    rw [ Finset.sum_congr rfl fun x hx => rank_symmetry N x b hb hbN hx ] ; norm_num;
  simp_all +decide [ Finset.sum_add_distrib, mul_comm ];
  rw [ coprimeResidues_card ] at * ; linarith!;
  linarith

/-! ## Main Theorem -/

/-
PROBLEM
**Denominator Displacement Sum Identity.**
    For the Farey sequence F_N with n = |F_N| elements, and denominator b with 2 ≤ b ≤ N:
      Σ_{a coprime b, 0<a<b} (rank(a/b) - n·(a/b)) = -φ(b)/2.

    The proof combines the rank-sum identity (from Farey symmetry) with the
    coprime residue sum identity (from the a ↔ b-a pairing).

PROVIDED SOLUTION
From rank_sum_nat: 2 * Σ fareyRank N a b = ((fareySet N).card - 1) * totient b.
From coprime_residues_sum_rat: 2 * Σ (a : ℚ) = b * totient b.

Let n = (fareySet N).card, φ = totient b, S_rank = Σ fareyRank, S_a = Σ a (over ℚ).

Over ℚ:
S_rank = (n - 1) * φ / 2  (from rank_sum_nat cast to ℚ)
S_a = b * φ / 2            (from coprime_residues_sum_rat)

The sum we want is:
Σ (fareyRank N a b - n * a / b) = S_rank - n/b * S_a
= (n-1)*φ/2 - n/b * b*φ/2
= (n-1)*φ/2 - n*φ/2
= -φ/2

Use field_simp and ring after establishing the cast identities. Note b ≠ 0 since b ≥ 2.

Key steps:
1. Push the sum through: Σ (rank - n*a/b) = (Σ rank) - n/b * (Σ a)
   Use Finset.sum_sub_distrib and factor out n/b from the second sum.
2. Substitute the two identities.
3. Simplify algebraically.

For step 1: Σ_a (rank(a) - n * a / b) = Σ rank(a) - Σ (n * a / b) = Σ rank(a) - (n/b) * Σ a.
Use Finset.sum_sub_distrib for the first split, then Finset.mul_sum to factor n/b.
-/
theorem denom_displacement_sum (N b : ℕ) (hb : 2 ≤ b) (hbN : b ≤ N) :
    ∑ a ∈ coprimeResidues b,
      ((fareyRank N a b : ℚ) - (fareySet N).card * (a : ℚ) / (b : ℚ)) =
    -(Nat.totient b : ℚ) / 2 := by
  have h_coprime_residues_sum : ∑ a ∈ coprimeResidues b, ((fareyRank N a b : ℚ)) = (((fareySet N).card : ℚ) - 1) * (Nat.totient b : ℚ) / 2 := by
    have := rank_sum_nat N b hb hbN;
    rw [ eq_div_iff ] <;> norm_cast;
    rw [ Int.subNatNat_of_le ] <;> norm_cast ; linarith [ Nat.sub_add_cancel ( show 1 ≤ Finset.card ( fareySet N ) from Finset.card_pos.mpr ⟨ ( 1, 1 ), by exact Finset.mem_filter.mpr ⟨ Finset.mem_product.mpr ⟨ Finset.mem_range.mpr <| by linarith, Finset.mem_range.mpr <| by linarith ⟩, by norm_num, by linarith, by norm_num ⟩ ⟩ ) ];
    exact Finset.card_pos.mpr ⟨ ( 1, 1 ), by exact Finset.mem_filter.mpr ⟨ Finset.mem_product.mpr ⟨ Finset.mem_range.mpr <| by linarith, Finset.mem_range.mpr <| by linarith ⟩, by norm_num, by linarith, by norm_num ⟩ ⟩;
  have h_coprime_sum : ∑ a ∈ coprimeResidues b, (a : ℚ) = (b : ℚ) * (Nat.totient b : ℚ) / 2 := by
    have := @coprime_residues_sum_rat b hb; norm_num [ mul_comm ] at *; linarith;
  simp_all +decide [ mul_div_assoc ];
  norm_num [ ← Finset.mul_sum _ _ _, ← Finset.sum_div, h_coprime_sum ] ; ring_nf;
  norm_num [ show b ≠ 0 by linarith ]