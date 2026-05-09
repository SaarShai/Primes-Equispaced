import Mathlib
import RequestProject.PrimeCircle
import RequestProject.DisplacementShift
import RequestProject.StrictPositivity
import RequestProject.CrossTermPositive
import RequestProject.BridgeIdentity
import RequestProject.MertensGrowth

open Finset BigOperators

/-! ## Definitions matching SignTheorem.lean -/

def fareyCount' (N : ℕ) : ℕ :=
  1 + ∑ k ∈ Finset.range N, Nat.totient (k + 1)

def wobbleNumerator' (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N, (displacement N ((ab.1 : ℚ) / ab.2)) ^ 2

def wobble' (N : ℕ) : ℚ :=
  wobbleNumerator' N / (fareyCount' N : ℚ) ^ 2

def deltaWobble' (p : ℕ) : ℚ :=
  wobble' (p - 1) - wobble' p

/-! ## Extended computational verification: p ∈ [114, 140]

These primes with M(p) ≤ -3 in this range are: 131, 139.
Both satisfy ΔW(p) < 0, extending the verified range from p ≤ 113
(in SignTheorem.lean) to p ≤ 140. -/

private theorem sign_helper_114_140 :
    ∀ p ∈ Finset.Icc 114 140, Nat.Prime p → (mertens p : ℤ) ≤ -3 →
      deltaWobble' p < 0 := by
  native_decide

/-- ΔW(p) < 0 for primes p with 114 ≤ p ≤ 140 and M(p) ≤ -3. -/
theorem sign_theorem_114_to_140 (p : ℕ) (hp : Nat.Prime p) (hp114 : 114 ≤ p)
    (hp140 : p ≤ 140) (hM : (mertens p : ℤ) ≤ -3) :
    deltaWobble' p < 0 :=
  sign_helper_114_140 p (Finset.mem_Icc.mpr ⟨hp114, hp140⟩) hp hM

/-! ## Main conjecture (still open)

**Sign Theorem (main conjecture):**
For prime p ≥ 13 with M(p) ≤ -3, ΔW(p) < 0 (wobble increases).

STATUS: Open conjecture. Verified computationally for all qualifying
primes p ≤ 140:
- sign_theorem_all_le_113 in SignTheorem.lean covers p ≤ 113
- sign_theorem_114_to_140 above covers 114 ≤ p ≤ 140

The previously proposed proof path via the Weil bound |CT_b|² · b ≤ φ(b)²
is INVALID — that bound was disproved with counterexample p=23, b=12
(see weil_bound_counterexample in WeilBound.lean and SignTheorem.lean).

A valid proof would require either:
(a) A corrected per-denominator bound with the right dependence on p, or
(b) A direct analysis of the four-term decomposition showing
    D + B + C - 1 > dilution when M(p) ≤ -3, or
(c) A fundamentally different approach.
-/
/-- DISPROVED at p = 243,799.  Retained as documentation.
    The bounded version sign_theorem_114_to_140 above is proved. -/
-- theorem sign_theorem_conj' (p : ℕ) (hp : Nat.Prime p) (hp13 : 13 ≤ p)
--     (hM : (mertens p : ℤ) ≤ -3) :
--     deltaWobble' p < 0 := by sorry
