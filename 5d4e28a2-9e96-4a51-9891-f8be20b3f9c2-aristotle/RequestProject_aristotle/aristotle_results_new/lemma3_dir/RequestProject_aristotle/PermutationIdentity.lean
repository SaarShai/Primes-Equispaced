import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DisplacementShift
import RequestProject.StrictPositivity
import RequestProject.CrossTermPositive
import RequestProject.BridgeIdentity

/-!
# The Permutation Square-Sum Identity

## Statement
For prime p and N < p, summing over all fractions a/b in the Farey sequence F_N
with b > 1:
  Sigma (a/b) * delta(a/b) = (1/2) * Sigma delta(a/b)^2
where delta(a/b) = (a - (p*a mod b)) / b is the shift function.

## Proof outline

1. Write delta = x - {px} where x = a/b, {px} = (pa mod b)/b.
2. Then x * delta - delta^2 / 2 = (x^2 - {px}^2) / 2.
3. For each fixed b, the map a -> pa mod b is a permutation of coprime residues
   (since gcd(p,b) = 1).
4. Therefore Sigma_{gcd(a,b)=1} (a/b)^2 = Sigma_{gcd(a,b)=1} (pa mod b / b)^2.
5. Each per-denominator sum of (x^2 - {px}^2) vanishes, so
   Sigma(x * delta - delta^2 / 2) = 0, giving
   Sigma x * delta = (1/2) * Sigma delta^2.

## Relation to existing definitions
- The LHS 2 * Sigma f * delta(f) relates to crossTerm via displacement.
- The RHS is shiftSquaredSum / 2.
- This identity provides an alternative route to understanding B+C positivity.
-/

open Finset BigOperators

/-! ## The fractional-part-squared sum: Sigma (pa mod b / b)^2 -/

/-- The shifted-squared sum per denominator: for fixed b, sum (pa mod b / b)^2
    over coprime residues a with 0 <= a <= b. -/
def shiftedSquaredSumDenom (p b : ℕ) : ℚ :=
  ∑ a ∈ (Finset.range (b + 1)).filter (fun a => Nat.Coprime a b),
    ((a * p % b : ℕ) : ℚ) ^ 2 / (b : ℚ) ^ 2

/-- The original-squared sum per denominator: for fixed b, sum (a/b)^2
    over coprime residues a with 0 <= a <= b. -/
def originalSquaredSumDenom (b : ℕ) : ℚ :=
  ∑ a ∈ (Finset.range (b + 1)).filter (fun a => Nat.Coprime a b),
    ((a : ℕ) : ℚ) ^ 2 / (b : ℚ) ^ 2

/-! ## Key permutation lemma (extended to include 0 and b) -/

/-- For gcd(p, b) = 1 with b >= 1, the map a -> a*p % b is a permutation
    on coprime residues {a : 0 <= a < b, gcd(a,b) = 1}.

    This is exactly coprime_mul_perm from BridgeIdentity.lean. We use it
    to show that Sigma_{gcd(a,b)=1, a<b} f(a*p%b) = Sigma_{gcd(a,b)=1, a<b} f(a)
    for any function f. -/

/-- Permutation invariance of sum of squares for coprime residues mod b.
    Since a -> a*p % b permutes the coprime residues (by coprime_mul_perm),
    the sum of f(a*p%b) equals the sum of f(a) for any f. -/
lemma sum_perm_eq {b p : ℕ} (hb : 0 < b) (hcop : Nat.Coprime p b)
    (f : ℕ → ℚ) :
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b), f (a * p % b) =
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b), f a := by
  have hperm := coprime_mul_perm b p hb hcop
  -- The image of the map a -> a*p%b on the coprime residues equals the coprime residues
  rw [← hperm]
  rw [Finset.sum_image]
  -- Injectivity of a -> a*p%b on coprime residues mod b
  intro a₁ ha₁ a₂ ha₂ heq
  simp only [Finset.mem_filter, Finset.mem_range] at ha₁ ha₂
  have hmod : a₁ * p ≡ a₂ * p [MOD b] := by
    exact heq
  have : a₁ ≡ a₂ [MOD b] := by
    rwa [Nat.ModEq] at hmod ⊢
    rw [Nat.mul_mod, Nat.mul_mod] at hmod
    have hp_inv : Nat.Coprime p b := hcop
    sorry
  have ha₁_lt := ha₁.1
  have ha₂_lt := ha₂.1
  omega

/-- The sum of squares of coprime residues is invariant under the permutation
    a -> a*p % b when gcd(p, b) = 1.

    That is: Sigma_{gcd(a,b)=1, a<b} (a*p%b)^2 = Sigma_{gcd(a,b)=1, a<b} a^2. -/
lemma coprime_square_sum_perm_invariant (b p : ℕ) (hb : 0 < b) (hcop : Nat.Coprime p b) :
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b), ((a * p % b : ℕ) : ℚ) ^ 2 =
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b), ((a : ℕ) : ℚ) ^ 2 := by
  have hperm := coprime_mul_perm b p hb hcop
  rw [← hperm]
  rw [Finset.sum_image]
  intro a₁ ha₁ a₂ ha₂ heq
  simp only [Finset.mem_filter, Finset.mem_range] at ha₁ ha₂
  -- If a₁ * p % b = a₂ * p % b then a₁ * p ≡ a₂ * p (mod b)
  -- Since gcd(p, b) = 1, we can cancel p to get a₁ ≡ a₂ (mod b)
  -- Since a₁, a₂ < b, we get a₁ = a₂
  have hmod : a₁ * p % b = a₂ * p % b := heq
  have hcong : a₁ * p ≡ a₂ * p [MOD b] := hmod
  have := (Nat.Coprime.mul_mod_cancel_right_iff hcop a₁ a₂ b).mp
  sorry

/-! ## Computational verification of the identity for small primes -/

/-- The value-times-shift sum: Sigma_{(a,b) in fareySet(N)} (a/b) * shiftFun(p, a/b). -/
def valueTimesShift (p : ℕ) : ℚ :=
  ∑ ab ∈ fareySet (p - 1),
    ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)

/-- Computational verification: the identity holds for p = 5. -/
theorem perm_identity_5 : valueTimesShift 5 = shiftSquaredSum 5 / 2 := by native_decide

/-- Computational verification: the identity holds for p = 7. -/
theorem perm_identity_7 : valueTimesShift 7 = shiftSquaredSum 7 / 2 := by native_decide

/-- Computational verification: the identity holds for p = 11. -/
theorem perm_identity_11 : valueTimesShift 11 = shiftSquaredSum 11 / 2 := by native_decide

/-- Computational verification: the identity holds for p = 13. -/
theorem perm_identity_13 : valueTimesShift 13 = shiftSquaredSum 13 / 2 := by native_decide

/-- Computational verification: the identity holds for p = 19. -/
theorem perm_identity_19 : valueTimesShift 19 = shiftSquaredSum 19 / 2 := by native_decide

/-- Computational verification: the identity holds for p = 23. -/
theorem perm_identity_23 : valueTimesShift 23 = shiftSquaredSum 23 / 2 := by native_decide

/-! ## The algebraic identity: x * delta - delta^2/2 = (x^2 - {px}^2) / 2 -/

/-- For a fraction x = a/b with b > 0, and delta = x - {px},
    we have x * delta - delta^2 / 2 = (x^2 - {px}^2) / 2.

    Proof: delta = x - y where y = {px} = (pa mod b)/b.
    x * delta = x * (x - y) = x^2 - xy.
    delta^2 = (x - y)^2 = x^2 - 2xy + y^2.
    x * delta - delta^2/2 = x^2 - xy - (x^2 - 2xy + y^2)/2
                           = x^2 - xy - x^2/2 + xy - y^2/2
                           = x^2/2 - y^2/2 = (x^2 - y^2)/2. -/
lemma algebraic_identity (x y : ℚ) :
    x * (x - y) - (x - y) ^ 2 / 2 = (x ^ 2 - y ^ 2) / 2 := by
  ring

/-! ## Per-denominator cancellation -/

/-- For each fixed denominator b with gcd(p, b) = 1, the sum
    Sigma_{gcd(a,b)=1, 0<a<b} ((a/b)^2 - ((pa mod b)/b)^2) = 0.

    This follows because a -> pa mod b permutes the coprime residues,
    so Sigma (a/b)^2 = Sigma ((pa mod b)/b)^2. -/
lemma per_denom_cancel (p b : ℕ) (hb : 1 < b) (hcop : Nat.Coprime p b) :
    ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b),
      (((a : ℚ) / b) ^ 2 - (((a * p % b : ℕ) : ℚ) / b) ^ 2) = 0 := by
  have hb_pos : (0 : ℚ) < (b : ℚ) := by positivity
  have hb_ne : (b : ℚ) ≠ 0 := ne_of_gt hb_pos
  -- Factor out 1/b^2
  simp only [div_pow, ← sub_div]
  rw [Finset.sum_div]
  suffices h : ∑ a ∈ (Finset.range b).filter (fun a => Nat.Coprime a b),
      (((a : ℕ) : ℚ) ^ 2 - ((a * p % b : ℕ) : ℚ) ^ 2) = 0 by
    rw [h]; simp
  -- This is Sigma a^2 - Sigma (a*p%b)^2, and both sums are equal by permutation
  rw [Finset.sum_sub_distrib]
  have := coprime_square_sum_perm_invariant b p (by omega) hcop
  linarith

/-! ## The main identity -/

/-- **Permutation Square-Sum Identity (computational, p < 30).**
    For all primes p in {5, 7, 11, 13, 17, 19, 23, 29}:
      Sigma_{f in F_{p-1}} f * delta(f) = (1/2) * Sigma delta(f)^2.

    Equivalently: valueTimesShift p = shiftSquaredSum p / 2. -/
theorem perm_identity_le_30 :
    ∀ p ∈ Finset.filter Nat.Prime (Finset.Icc 5 29),
      valueTimesShift p = shiftSquaredSum p / 2 := by
  native_decide

/-- **Permutation Square-Sum Identity (general statement).**
    For prime p >= 5:
      Sigma_{f in F_{p-1}} f * shiftFun(p, f) = shiftSquaredSum(p) / 2.

    Proof: By the algebraic identity, each term f * delta(f) - delta(f)^2/2
    equals (f^2 - {pf}^2)/2. Summing over all f in F_{p-1} and grouping by
    denominator b, each group vanishes because a -> pa mod b is a permutation
    (coprime_mul_perm). Therefore Sigma f*delta = Sigma delta^2/2. -/
theorem perm_square_sum_identity (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    valueTimesShift p = shiftSquaredSum p / 2 := by
  -- The proof proceeds by showing that the difference
  -- Sigma f * delta(f) - Sigma delta(f)^2 / 2 = 0.
  -- By the algebraic identity, this difference equals
  -- Sigma_{f} (f^2 - {pf}^2) / 2, which vanishes per-denominator.
  unfold valueTimesShift shiftSquaredSum
  -- We need: Sigma f * shift(f) = (1/2) * Sigma shift(f)^2
  -- i.e., Sigma (f * shift(f) - shift(f)^2 / 2) = 0
  -- i.e., Sigma (f^2 - {pf}^2) / 2 = 0
  sorry

/-! ## Consequences for B+C analysis -/

/-- The cross-shift-value sum: 2 * Sigma f * delta(f).
    By the permutation identity, this equals shiftSquaredSum. -/
def crossShiftValue (p : ℕ) : ℚ :=
  2 * valueTimesShift p

/-- By the permutation identity, 2 * Sigma f * delta(f) = shiftSquaredSum. -/
theorem crossShiftValue_eq (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p) :
    crossShiftValue p = shiftSquaredSum p := by
  unfold crossShiftValue
  rw [perm_square_sum_identity p hp hp5]
  ring

/-- **Connection to the cross term B.**
    The cross term B = 2 * Sigma D * delta decomposes as:
      B = 2 * Sigma (D - f) * delta + 2 * Sigma f * delta
        = 2 * Sigma (D - f) * delta + shiftSquaredSum

    Since D(f) = rank(f) - |F_N| * f, the term (D - f) involves the
    centered displacement. The permutation identity gives us the
    second term exactly. -/

/-- Computational verification of the connection: for p = 13,
    crossTerm = 2 * Sigma (D - f) * delta + shiftSquaredSum. -/
theorem cross_connection_13 :
    crossTerm 13 = 2 * (∑ ab ∈ fareySet 12,
      (displacement 12 ((ab.1 : ℚ) / ab.2) - (ab.1 : ℚ) / ab.2) *
      shiftFun 13 ((ab.1 : ℚ) / ab.2)) + shiftSquaredSum 13 := by
  native_decide

/-! ## Computational range check -/

/-- The identity holds for all primes 5 <= p <= 43. -/
theorem perm_identity_le_43 :
    ∀ p ∈ Finset.filter Nat.Prime (Finset.Icc 5 43),
      valueTimesShift p = shiftSquaredSum p / 2 := by
  native_decide
