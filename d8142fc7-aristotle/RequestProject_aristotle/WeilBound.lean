import Mathlib
import PrimeCircle
import DisplacementShift
import StrictPositivity
import CrossTermPositive
import BridgeIdentity
import MertensGrowth

open Finset BigOperators

/-- The per-denominator cross term: for a fixed denominator b,
    CT_b(p) = Σ_{(a,b) ∈ F_{p-1}, denom = b} D_{p-1}(a/b) · δ_p(a/b). -/
def perDenomCrossTerm' (p b : ℕ) : ℚ :=
  ∑ ab ∈ (fareySet (p - 1)).filter (fun ab => ab.2 = b),
    displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)

/-! ## Counterexample to the Weil Bound Conjecture (C=1)

The original conjecture stated: for prime p ≥ 5 and 1 ≤ b ≤ p-1,
  (perDenomCrossTerm p b)² · b ≤ φ(b)²

This is FALSE. The smallest counterexample is p = 23, b = 12:
  CT_12(23) = 29/18
  CT² · b = (29/18)² · 12 = 841/27 ≈ 31.1
  φ(12)² = 4² = 16

The bound holds for all primes p ≤ 19 but fails starting at p = 23.
The issue is that the displacement D_{p-1}(a/b) grows with p (since
|F_{p-1}| ~ 3p²/π² grows), so the per-denominator cross term can
exceed the φ(b)/√b bound for larger primes.
-/

/-- Counterexample: the Weil bound CT²·b ≤ φ(b)² fails at p=23, b=12. -/
theorem weil_bound_counterexample' :
    ¬((perDenomCrossTerm' 23 12) ^ 2 * 12 ≤ (Nat.totient 12 : ℚ) ^ 2) := by
  native_decide

/-- The Weil bound holds for p = 13 (the case verified in SignTheorem.lean). -/
theorem weil_bound_holds_13 :
    ∀ b ∈ Finset.Icc 1 12,
      (perDenomCrossTerm' 13 b) ^ 2 * b ≤ (Nat.totient b : ℚ) ^ 2 := by
  native_decide
