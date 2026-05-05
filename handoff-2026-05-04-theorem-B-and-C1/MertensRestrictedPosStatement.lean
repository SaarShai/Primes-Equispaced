import Mathlib
import PrimeCircle
import DisplacementShift
import BridgeIdentity
import CrossTermPositive
import MertensDecomposition

/-!
# Mertens-restricted B(p) positivity — STATEMENT ONLY

This file is **statement only**.  The theorem is the central conjecture
of `Mertens_restricted_B_positivity.md`:

  **Conjecture B+.**  For every prime `p` with Mertens function
  `M(p) ≤ −3`, the Farey cross-term satisfies `B(p) > 0`.

In Lean we phrase this as a conditional statement (a `Prop`) and supply
two equivalent forms (one in `crossTerm`-language, one in
`B0 / Spsi`-language via Lemma 3.1).  The proofs are not provided
(this is the open conjecture); the theorem-statements use `sorry` in
the body to mark the blocking.

What IS proved (no `sorry`):
- `MertensRestrictedPositivity` and `MertensRestrictedPositivityForm2`
  are propositionally equivalent (via Lemma 3.1).
- The numerical instances p = 13, 19 already satisfy B(p) > 0 with
  M(p) = -3 (proved in `CrossTermPositive.lean`).

The conjecture is a real machine-stated open problem; even the
*statement* in Lean type-checks against Mathlib's `Nat.Prime`,
`mertens`, and our `crossTerm` infrastructure.
-/

namespace MertensRestrictedPosStatement

open MertensDecomposition

/-! ## 1. Statement form A — in `crossTerm` language. -/

/-- **Conjecture B+, form A.**  For every prime `p` with
    `mertens p ≤ −3`, the Farey cross-term `crossTerm p` is strictly
    positive. -/
def MertensRestrictedPositivity : Prop :=
  ∀ p : ℕ, Nat.Prime p → mertens p ≤ -3 → crossTerm p > 0

/-! ## 2. Statement form B — in `B0 / Spsi` language. -/

/-- **Conjecture B+, form B.**  For every prime `p` with
    `mertens p ≤ −3`,  `Spsi p < B0 (p − 1)`.  This is the form that
    makes the inequality between the p-independent Farey statistic and
    the prime-dependent sawtooth bilinear form explicit. -/
def MertensRestrictedPositivityForm2 : Prop :=
  ∀ p : ℕ, Nat.Prime p → mertens p ≤ -3 → Spsi p < B0 (p - 1)

/-! ## 3. Equivalence of form A and form B (proved unconditionally). -/

/-- The two formulations of Conjecture B+ are equivalent: this is just
    `crossTerm_pos_iff_Spsi_lt_B0` quantified over `p`. -/
theorem mertens_restricted_pos_equiv :
    MertensRestrictedPositivity ↔ MertensRestrictedPositivityForm2 := by
  unfold MertensRestrictedPositivity MertensRestrictedPositivityForm2
  constructor
  · intro h p hp hmp
    exact (crossTerm_pos_iff_Spsi_lt_B0 p).mp (h p hp hmp)
  · intro h p hp hmp
    exact (crossTerm_pos_iff_Spsi_lt_B0 p).mpr (h p hp hmp)

/-! ## 4. Verified numerical instances.

These witness that the conjecture is *consistent* on the smallest
known cases.  They follow from `crossTerm_val_13` and
`crossTerm_val_19` in `CrossTermPositive.lean`. -/

/-- B(13) > 0 (from `crossTerm_val_13 : crossTerm 13 = 271/385`). -/
theorem crossTerm_pos_13 : crossTerm 13 > 0 := by
  rw [crossTerm_val_13]; norm_num

/-- B(19) > 0 (from `crossTerm_val_19`). -/
theorem crossTerm_pos_19 : crossTerm 19 > 0 := by
  rw [crossTerm_val_19]; norm_num

/-- The B0 / Spsi form: `Spsi 13 < B0 12` (numerical instance). -/
theorem Spsi_lt_B0_13 : Spsi 13 < B0 12 :=
  (crossTerm_pos_iff_Spsi_lt_B0 13).mp crossTerm_pos_13

/-- The B0 / Spsi form: `Spsi 19 < B0 18` (numerical instance). -/
theorem Spsi_lt_B0_19 : Spsi 19 < B0 18 :=
  (crossTerm_pos_iff_Spsi_lt_B0 19).mp crossTerm_pos_19

/-! ## 5. The conjecture as an axiom (witness placeholder). -/

/-- `axiom` form for downstream files.  Anywhere we want to USE Conj B+
    we can `open MertensRestrictedPosStatement` and reference
    `mertens_restricted_pos_axiom`.  This is the formal placeholder
    until the open conjecture is proved. -/
axiom mertens_restricted_pos_axiom : MertensRestrictedPositivity

/-- Corollary of the axiom: form B holds. -/
theorem mertens_restricted_pos_form2_from_axiom :
    MertensRestrictedPositivityForm2 :=
  mertens_restricted_pos_equiv.mp mertens_restricted_pos_axiom

end MertensRestrictedPosStatement
