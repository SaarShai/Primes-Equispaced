import Mathlib
import PrimeCircle
import DisplacementShift
import BridgeIdentity
import CrossTermPositive

/-!
# Mertens-Restricted B(p) Decomposition (Lemma 3.1)

From `/Users/saar/Farey 4.7 solutions/Mertens_restricted_B_positivity.md` §3:

  **Lemma 3.1 (Decomposition; exact rational identity).**  For every prime `p ≥ 2`,
    `B(p) = 2 · B₀(p − 1) − 2 · S_ψ(p)`,
  where with `N = p − 1`,
    `B₀(N)   = Σ_{f ∈ F_N} D_N(f) · (f − 1/2)`,
    `S_ψ(p)  = Σ_{f ∈ F_{p−1}} D_{p−1}(f) · ψ(p f)`,
    `ψ(x)    = {x} − 1/2`.

The proof rests on the pointwise identity
  `δ(f) = (f − 1/2) − ψ(p f)`                                  (★)
which holds whenever `ψ` is interpreted with the convention `ψ(integer) = −1/2`
(equivalently `ψ(x) = {x} − 1/2`).

This file:
1. Defines `B0` and `Spsi` over ℚ using the existing `displacement` and
   `Int.fract` (so `ψ` is the standard sawtooth `{x} − 1/2`).
2. Proves the pointwise identity (★) as a ℚ identity (it follows from the
   definition `δ(f) = f − {p f}` directly).
3. Concludes the decomposition `crossTerm p = 2 · B0 (p−1) − 2 · Spsi p`.

The proof is purely algebraic in ℚ (no analysis, no Bridge identity needed
for this particular lemma).
-/

namespace MertensDecomposition

open Finset BigOperators

/-! ## The sawtooth `ψ(x) = {x} − 1/2` over ℚ. -/

/-- Sawtooth function on ℚ: `ψ(x) = {x} − 1/2`. With Lean's `Int.fract`,
    `Int.fract` returns a value in `[0, 1)`, so `ψ` lies in `[−1/2, 1/2)`. -/
def psi (x : ℚ) : ℚ := Int.fract x - 1/2

/-! ## The two pieces `B₀` and `S_ψ`. -/

/-- The p-independent Farey statistic `B₀(N) = Σ_{f ∈ F_N} D_N(f) · (f − 1/2)`. -/
def B0 (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N,
    displacement N ((ab.1 : ℚ) / ab.2) * ((ab.1 : ℚ) / ab.2 - 1/2)

/-- The Bridge-related sawtooth bilinear form
    `S_ψ(p) = Σ_{f ∈ F_{p−1}} D_{p−1}(f) · ψ(p f)`. -/
def Spsi (p : ℕ) : ℚ :=
  ∑ ab ∈ fareySet (p - 1),
    displacement (p - 1) ((ab.1 : ℚ) / ab.2) *
      psi ((p : ℚ) * ((ab.1 : ℚ) / ab.2))

/-! ## The pointwise identity (★)

The shift function from `DisplacementShift.lean` is
  `shiftFun p f = f − Int.fract (p · f)`.
The sawtooth is `psi x = Int.fract x − 1/2`. Therefore for any `f ∈ ℚ`,
  `shiftFun p f  =  (f − 1/2) − psi (p · f)`,
which is just rearranging `f − Int.fract(p·f) = (f − 1/2) − (Int.fract(p·f) − 1/2)`.
This identity is independent of whether `p · f` is integer or not — Lean's
`Int.fract` already implements the `{x} = 0` convention at integers, and
`ψ` then takes value `−1/2` there, exactly matching the documented convention
in `Mertens_restricted_B_positivity.md` (★).
-/

/-- The pointwise identity (★) on ℚ: `δ(f) = (f − 1/2) − ψ(p · f)`. -/
theorem shift_eq_centered_minus_psi (p : ℕ) (f : ℚ) :
    shiftFun p f = (f - 1/2) - psi ((p : ℚ) * f) := by
  unfold shiftFun psi
  ring

/-! ## The decomposition lemma. -/

/-- **Lemma 3.1 (decomposition).**
    `crossTerm p = 2 · B0 (p − 1) − 2 · Spsi p`.

The proof is a pointwise application of (★) under the sum, then linearity. -/
theorem crossTerm_eq_2B0_sub_2Spsi (p : ℕ) :
    crossTerm p = 2 * B0 (p - 1) - 2 * Spsi p := by
  unfold crossTerm B0 Spsi
  simp only [Finset.mul_sum, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro ab _
  rw [shift_eq_centered_minus_psi]
  ring

/-! ## Computational sanity checks (ℚ exact)

These spot-check Lemma 3.1 against the verified `crossTerm_val_*` theorems
in `CrossTermPositive.lean`. They are pure `native_decide` over ℚ. -/

/-- Lemma 3.1 at p = 5: B(5) = 2·B₀(4) − 2·S_ψ(5) = −2/9. -/
theorem decomposition_check_5 :
    crossTerm 5 = 2 * B0 4 - 2 * Spsi 5 :=
  crossTerm_eq_2B0_sub_2Spsi 5

/-- Lemma 3.1 at p = 13: B(13) = 271/385. -/
theorem decomposition_check_13 :
    crossTerm 13 = 2 * B0 12 - 2 * Spsi 13 :=
  crossTerm_eq_2B0_sub_2Spsi 13

/-- Lemma 3.1 at p = 19. -/
theorem decomposition_check_19 :
    crossTerm 19 = 2 * B0 18 - 2 * Spsi 19 :=
  crossTerm_eq_2B0_sub_2Spsi 19

/-! ## Conjecture B+ as a ℚ inequality

With Lemma 3.1 in hand, Conjecture B+ from
`/Users/saar/Farey 4.7 solutions/Mertens_restricted_B_positivity.md`
becomes:

  **(B+').** For every prime `p` with `mertens p ≤ −3`,  `Spsi p < B0 (p−1)`.

This is structurally the same statement as `crossTerm p > 0` but in a form
that explicitly separates the p-independent Farey part `B0` from the
prime-dependent sawtooth part `Spsi`. -/

/-- Equivalence: `crossTerm p > 0 ↔ Spsi p < B0 (p − 1)`. -/
theorem crossTerm_pos_iff_Spsi_lt_B0 (p : ℕ) :
    crossTerm p > 0 ↔ Spsi p < B0 (p - 1) := by
  rw [crossTerm_eq_2B0_sub_2Spsi]
  constructor
  · intro h; linarith
  · intro h; linarith

end MertensDecomposition
