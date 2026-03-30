import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DisplacementShift
import RequestProject.SignTheorem
import RequestProject.AbstractCauchySchwarz
import RequestProject.CauchySchwarzBound

/-!
# The C_W ≥ 1/4 Bound

## Statement
For N ≥ 1, the wobble constant satisfies:
  C_W = wobbleNumerator(N) / fareyCount(N)² ≥ 1 / (4 · fareyCount(N))

## Proof outline
1. **Displacement sum (Step 1):** Σ_{f ∈ F_N} D(f) = |F_N|/2
   (fareyRank is 1-indexed, and by Farey symmetry Σ f = n/2)

2. **Cauchy-Schwarz (Step 2):** (Σ D)² ≤ |F_N| · Σ D²
   Substituting Σ D = n/2 gives n²/4 ≤ n · Σ D², hence Σ D² ≥ n/4.

3. **C_W bound (Step 3):** wobbleNumerator = Σ D² ≥ n/4, so
   C_W = Σ D² / n² ≥ (n/4) / n² = 1/(4n).
-/

open Finset BigOperators

/-! ## Auxiliary lemmas about fareyCount cast to ℚ -/

/-- fareyCount N cast to ℚ is positive (for any N, since fareyCount = 1 + Σ). -/
lemma fareyCount_cast_pos (N : ℕ) : (0 : ℚ) < (fareyCount N : ℚ) := by
  apply Nat.cast_pos.mpr
  unfold fareyCount
  exact add_pos_of_pos_of_nonneg zero_lt_one (Finset.sum_nonneg fun _ _ => Nat.zero_le _)

/-- fareyCount N cast to ℚ is nonzero. -/
lemma fareyCount_cast_ne_zero (N : ℕ) : (fareyCount N : ℚ) ≠ 0 :=
  ne_of_gt (fareyCount_cast_pos N)

/-- (fareyCount N)² is positive as a rational. -/
lemma fareyCount_sq_pos (N : ℕ) : (0 : ℚ) < (fareyCount N : ℚ) ^ 2 :=
  sq_pos_of_pos (fareyCount_cast_pos N)

/-! ## fareySet card positive -/

/-- fareySet N has positive cardinality when N ≥ 1. -/
lemma fareySet_card_pos (N : ℕ) (hN : N ≥ 1) : 0 < (fareySet N).card := by
  rw [← fareyCount_eq_card N hN]
  exact fareyCount_pos N hN

/-! ## Variant of abstract Cauchy-Schwarz for positive sum -/

/-- If the sum of values over a finite set equals n/2,
    then the sum of squares is at least n/4.
    Follows from Cauchy-Schwarz: (Σ a_i)² ≤ |s| · Σ a_i². -/
theorem sum_sq_ge_quarter_of_sum_eq_pos_half
    {ι : Type*} [DecidableEq ι] (s : Finset ι) (a : ι → ℚ)
    (hs : 0 < s.card)
    (hsum : ∑ i ∈ s, a i = ((s.card : ℚ)) / 2) :
    ∑ i ∈ s, (a i) ^ 2 ≥ ((s.card : ℚ)) / 4 := by
  have h_cauchy_schwarz : (∑ i ∈ s, a i)^2 ≤ (∑ i ∈ s, (a i)^2) * (∑ i ∈ s, (1 : ℚ)^2) := by
    have h_cauchy_schwarz : ∀ (u v : ι → ℝ), (∑ i ∈ s, u i * v i)^2 ≤ (∑ i ∈ s, u i^2) * (∑ i ∈ s, v i^2) := by
      exact fun u v => sum_mul_sq_le_sq_mul_sq s u v
    convert h_cauchy_schwarz ( fun i => a i |> Rat.cast ) ( fun i => 1 ) using 1 ; norm_num [ ← @Rat.cast_inj ℝ ];
    norm_cast;
  norm_num [ hsum ] at h_cauchy_schwarz; nlinarith [ ( by norm_cast : ( 1 : ℚ ) ≤ Finset.card s ) ] ;

/-! ## The wobble numerator lower bound -/

/-- wobbleNumerator(N) ≥ fareyCount(N) / 4, derived from Cauchy-Schwarz. -/
theorem wobbleNumerator_ge_fareyCount_div_four (N : ℕ) (hN : N ≥ 1) :
    wobbleNumerator N ≥ (fareyCount N : ℚ) / 4 := by
  exact le_trans ( by rw [ fareyCount_eq_card N hN ] ) ( wobbleNumerator_ge_card_div_four N hN )

/-! ## The main C_W bound -/

/-- **C_W ≥ 1/(4n) bound:**
    wobbleNumerator(N) / fareyCount(N)² ≥ 1 / (4 · fareyCount(N)).

    This follows from wobbleNumerator(N) ≥ fareyCount(N) / 4
    (the Cauchy-Schwarz lower bound), by dividing both sides by fareyCount(N)². -/
theorem cw_ge_quarter_inv (N : ℕ) (hN : N ≥ 1) :
    wobbleNumerator N / (fareyCount N : ℚ) ^ 2 ≥ 1 / (4 * fareyCount N) := by
  have h_pos : (0 : ℚ) < (fareyCount N : ℚ) := fareyCount_cast_pos N
  have h_bound : wobbleNumerator N ≥ (fareyCount N : ℚ) / 4 :=
    wobbleNumerator_ge_fareyCount_div_four N hN
  rw [ge_iff_le, div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith

/-! ## Computational verification for small N -/

theorem cw_ge_quarter_inv_1 :
    wobbleNumerator 1 / (fareyCount 1 : ℚ) ^ 2 ≥ 1 / (4 * fareyCount 1) := by native_decide

theorem cw_ge_quarter_inv_2 :
    wobbleNumerator 2 / (fareyCount 2 : ℚ) ^ 2 ≥ 1 / (4 * fareyCount 2) := by native_decide

theorem cw_ge_quarter_inv_3 :
    wobbleNumerator 3 / (fareyCount 3 : ℚ) ^ 2 ≥ 1 / (4 * fareyCount 3) := by native_decide
