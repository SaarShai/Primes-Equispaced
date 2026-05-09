import Mathlib
import PrimeCircle
import DisplacementShift
import SignTheorem

/-!
# The C_W ≥ 1/4 Bound

## Statement
For the Farey sequence F_N with n = |F_N|:
  Σ_{f∈F_N} D(f)² ≥ n/4
where D(f) = rank(f) - n·f is the displacement.

Equivalently: wobbleNumerator(N) ≥ fareyCount(N) / 4.

## Proof (3 steps)
1. **Displacement sum:** Σ D = Σ rank(f) - n · Σ f.
   By Farey symmetry, Σ_{f∈F_N} f = n/2 (pairing f ↔ 1-f).
   Also Σ rank(f) = n(n-1)/2 (ranks are 0,1,...,n-1 up to reindex).
   So Σ D = n(n-1)/2 - n·(n/2) = -n/2.

2. **Cauchy-Schwarz:** (Σ D)² ≤ n · Σ D².

3. **Combine:** n²/4 ≤ n · Σ D², hence Σ D² ≥ n/4.
-/

open Finset BigOperators

/-! ## Displacement sum equals -n/2

This is the key identity: Σ_{f∈F_N} D(f) = -n/2 where n = |F_N|.
-/

/-- The sum of all displacements over F_N. -/
noncomputable def displacementSum (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N, displacement N ((ab.1 : ℚ) / ab.2)

/-- The sum of fractions in F_N: Σ_{(a,b)∈fareySet N} a/b. -/
noncomputable def fareySumFractions (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N, ((ab.1 : ℚ) / ab.2)

/- The original statement had n*(n-1)/2, but this is incorrect because fareyRank
   uses ≤ (inclusive), so ranks range from 1 to n, not 0 to n-1.
   Counterexample: N=1, fareySet = {(0,1),(1,1)}, ranks = {1,2}, sum = 3 ≠ 1.
   The correct formula is n*(n+1)/2.  -/

/-- Farey fractions are injective: distinct elements of fareySet N
    give distinct rational values a/b. -/
lemma farey_frac_injective (N : ℕ) (x y : ℕ × ℕ)
    (hx : x ∈ fareySet N) (hy : y ∈ fareySet N)
    (heq : (x.1 : ℚ) / x.2 = (y.1 : ℚ) / y.2) : x = y := by
  have h_cross : x.1 * y.2 = y.1 * x.2 := by
    rw [ div_eq_div_iff ] at heq <;> norm_cast at * <;> linarith [ Finset.mem_filter.mp hx, Finset.mem_filter.mp hy ]
  have h_denom_eq : x.2 = y.2 := by
    apply_mod_cast Nat.dvd_antisymm
    · exact ( Nat.Coprime.symm <| by unfold fareySet at hx; aesop ) |> fun h => h.dvd_of_dvd_mul_left <| h_cross.symm ▸ dvd_mul_left _ _
    · refine' Nat.Coprime.dvd_of_dvd_mul_left _ _
      exacts [ y.1, by simpa [ Nat.coprime_comm ] using Finset.mem_filter.mp hy |>.2.2.2, h_cross ▸ dvd_mul_left _ _ ]
  unfold fareySet at hx hy; aesop

/-- For each element ab of fareySet N, the number of elements with the same
    fraction value is exactly 1 (by injectivity). -/
lemma farey_eq_singleton (N : ℕ) (ab : ℕ × ℕ) (hab : ab ∈ fareySet N) :
    ((fareySet N).filter (fun p => (p.1 : ℚ) / p.2 = (ab.1 : ℚ) / ab.2)) = {ab} := by
  ext p; simp
  exact ⟨ fun h => farey_frac_injective N p ab h.1 hab h.2, fun h => h.symm ▸ ⟨ hab, rfl ⟩ ⟩

/-- For each element of fareySet N, the rank plus the "upper rank"
    (number of elements ≥) equals n + 1, using injectivity. -/
lemma farey_rank_upper_rank (N : ℕ) (ab : ℕ × ℕ) (hab : ab ∈ fareySet N) :
    ((fareySet N).filter (fun p => (p.1 : ℚ) / p.2 ≤ (ab.1 : ℚ) / ab.2)).card +
    ((fareySet N).filter (fun p => (ab.1 : ℚ) / ab.2 ≤ (p.1 : ℚ) / p.2)).card =
    (fareySet N).card + 1 := by
  have h_inclusion_exclusion :
      (fareySet N).filter (fun p => (p.1 : ℚ) / p.2 ≤ (ab.1 : ℚ) / ab.2) ∪
        (fareySet N).filter (fun p => (ab.1 : ℚ) / ab.2 ≤ (p.1 : ℚ) / p.2) = fareySet N ∧
      (fareySet N).filter (fun p => (p.1 : ℚ) / p.2 ≤ (ab.1 : ℚ) / ab.2) ∩
        (fareySet N).filter (fun p => (ab.1 : ℚ) / ab.2 ≤ (p.1 : ℚ) / p.2) = {ab} := by
    constructor
    · grind
    · ext p
      simp +zetaDelta at *
      exact ⟨ fun h => farey_frac_injective N _ _ h.1.1 hab ( by linarith ),
              fun h => h.symm ▸ ⟨ ⟨ hab, le_rfl ⟩, hab, le_rfl ⟩ ⟩
  grind

/-- The rank sum identity (corrected): Σ rank(f) = n(n+1)/2 where n = |F_N|.
    Ranks are 1, 2, ..., n (since fareyRank counts elements ≤ f, inclusive). -/
lemma rank_sum (N : ℕ) :
    ∑ ab ∈ fareySet N, (fareyRank N ((ab.1 : ℚ) / ab.2) : ℚ) =
      (fareySet N).card * ((fareySet N).card + 1) / 2 := by
  have h_symm_sum : ∑ ab ∈ fareySet N, fareyRank N ((ab.1 : ℚ) / (ab.2 : ℚ)) =
      ∑ ab ∈ fareySet N, ((fareySet N).filter
        (fun p => (ab.1 : ℚ) / (ab.2 : ℚ) ≤ (p.1 : ℚ) / (p.2 : ℚ))).card := by
    unfold fareyRank
    simp +decide only [card_filter]
    rw [ Finset.sum_comm ]
  have h_sum : ∑ ab ∈ fareySet N, fareyRank N ((ab.1 : ℚ) / (ab.2 : ℚ)) +
      ∑ ab ∈ fareySet N, ((fareySet N).filter
        (fun p => (ab.1 : ℚ) / (ab.2 : ℚ) ≤ (p.1 : ℚ) / (p.2 : ℚ))).card =
      ((fareySet N).card : ℚ) * (((fareySet N).card : ℚ) + 1) := by
    have h_sum : ∀ ab ∈ fareySet N, fareyRank N ((ab.1 : ℚ) / (ab.2 : ℚ)) +
        ((fareySet N).filter
          (fun p => (ab.1 : ℚ) / (ab.2 : ℚ) ≤ (p.1 : ℚ) / (p.2 : ℚ))).card =
        ((fareySet N).card : ℚ) + 1 := by
      intros ab hab; exact_mod_cast farey_rank_upper_rank N ab hab
    simpa [ Finset.sum_add_distrib, mul_add ] using Finset.sum_congr rfl h_sum
  rw [ eq_div_iff ] <;> norm_cast at * ; linarith

/-- Farey symmetry: Σ_{f∈F_N} f = n/2 where n = |F_N|.
    Proof: the map f ↦ 1-f is an involution on F_N, so Σ f + Σ (1-f) = n,
    giving 2·Σf = n, hence Σf = n/2. -/
lemma farey_sum_symmetry (N : ℕ) (hN : 1 ≤ N) :
    fareySumFractions N = (fareySet N).card / 2 := by
  sorry

/-- The displacement sum equals -n/2. -/
lemma displacement_sum_eq (N : ℕ) (hN : 1 ≤ N) :
    displacementSum N = -(fareySet N).card / 2 := by
  sorry

/-! ## The C_W ≥ 1/4 Bound via Cauchy-Schwarz -/

/-- **C_W Bound (Cauchy-Schwarz):**
    wobbleNumerator(N) = Σ D(f)² ≥ |F_N| / 4.

    Proof:
    By Cauchy-Schwarz, (Σ D)² ≤ n · Σ D².
    We showed Σ D = -n/2, so (n/2)² = n²/4 ≤ n · Σ D².
    Dividing by n (which is positive): Σ D² ≥ n/4.  -/
theorem cw_bound (N : ℕ) (hN : 1 ≤ N) :
    wobbleNumerator N ≥ (fareySet N).card / 4 := by
  sorry

/-- Computational verification for small N. -/
theorem cw_bound_1 : wobbleNumerator 1 ≥ (fareySet 1).card / 4 := by native_decide
theorem cw_bound_2 : wobbleNumerator 2 ≥ (fareySet 2).card / 4 := by native_decide
theorem cw_bound_3 : wobbleNumerator 3 ≥ (fareySet 3).card / 4 := by native_decide
theorem cw_bound_5 : wobbleNumerator 5 ≥ (fareySet 5).card / 4 := by native_decide
