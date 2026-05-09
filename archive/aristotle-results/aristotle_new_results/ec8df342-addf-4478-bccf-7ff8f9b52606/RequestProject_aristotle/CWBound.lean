import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DisplacementShift
import RequestProject.SignTheorem

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

/-- The rank sum identity: Σ rank(f) = n(n-1)/2 where n = |F_N|.
    This holds because the ranks are a permutation of {0, 1, ..., n-1}. -/
lemma rank_sum (N : ℕ) :
    ∑ ab ∈ fareySet N, (fareyRank N ((ab.1 : ℚ) / ab.2) : ℚ) =
      (fareySet N).card * ((fareySet N).card - 1) / 2 := by
  sorry

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
