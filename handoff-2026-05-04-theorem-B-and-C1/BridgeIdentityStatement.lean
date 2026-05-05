import Mathlib
import PrimeCircle
import BridgeIdentity

/-!
# Bridge Identity — clean restatement

Re-exports the result of `BridgeIdentity.lean` in a clean form usable
elsewhere in the project, and provides extra simp-style lemmas for
specific small primes.

The Bridge Identity is

  Σ_{f ∈ F_{p−1}} e^{2 π i p f}  =  M(p) + 2

for every prime p ≥ 2.  This is `BridgeIdentity.bridge_identity`.

Below we provide:
1. A clean `bridge_id_clean` restatement (just the imported theorem).
2. Numerical sanity-check `bridge_rhs_*` reuses (already in BridgeIdentity).
3. A "real-part" projection identity, in case downstream files only
   need the real component.
-/

namespace BridgeIdentityStatement

open Complex BigOperators

/-! ## 1. Re-export of the main identity. -/

/-- **Bridge Identity (clean restatement).**  For every prime `p`,
    `Σ_{f ∈ F_{p−1}} e^{2 π i p f} = M(p) + 2`. -/
theorem bridge_id_clean (p : ℕ) (hp : Nat.Prime p) :
    fareyExpSumBridge (p - 1) p = ↑(mertens p) + 2 :=
  bridge_identity p hp

/-! ## 2. Statement-level corollaries (no proof needed beyond reuse). -/

/-- The Bridge sum at p = 2 equals 2. -/
theorem bridge_p2 :
    fareyExpSumBridge 1 2 = ↑(mertens 2) + 2 :=
  bridge_id_clean 2 (by decide)

/-- The Bridge sum at p = 3 equals M(3) + 2 = 1. -/
theorem bridge_p3 :
    fareyExpSumBridge 2 3 = ↑(mertens 3) + 2 :=
  bridge_id_clean 3 (by decide)

/-- The Bridge sum at p = 13 equals M(13) + 2 = -1. -/
theorem bridge_p13 :
    fareyExpSumBridge 12 13 = ↑(mertens 13) + 2 :=
  bridge_id_clean 13 (by decide)

/-! ## 3. The Bridge Identity has integer real part.

    Since `M(p) + 2` is real, the LHS must be real.  This is a
    structural fact that downstream files (e.g. for B0 inequalities)
    can use. -/

/-- The Bridge sum at a prime is a real number (its imaginary part is
    zero), as a consequence of the identity. -/
theorem bridge_im_zero (p : ℕ) (hp : Nat.Prime p) :
    (fareyExpSumBridge (p - 1) p).im = 0 := by
  rw [bridge_id_clean p hp]
  simp

/-- The real part of the Bridge sum at prime `p` is exactly
    `mertens p + 2` (cast to ℝ). -/
theorem bridge_re_eq (p : ℕ) (hp : Nat.Prime p) :
    (fareyExpSumBridge (p - 1) p).re = (mertens p : ℝ) + 2 := by
  rw [bridge_id_clean p hp]
  simp

/-! ## 4. The bridge sum is bounded by `|M(p)| + 2`. -/

/-- `‖Σ e^{2πi p f}‖ ≤ |M(p)| + 2` follows directly from the identity,
    using the (real-valued) RHS. -/
theorem bridge_norm_bound (p : ℕ) (hp : Nat.Prime p) :
    ‖fareyExpSumBridge (p - 1) p‖ ≤ |(mertens p : ℝ)| + 2 := by
  rw [bridge_id_clean p hp]
  -- ‖(M(p) : ℂ) + 2‖ ≤ ‖(M(p) : ℂ)‖ + ‖(2 : ℂ)‖ = |M(p)| + 2
  have htri : ‖((mertens p : ℂ)) + 2‖ ≤ ‖((mertens p : ℂ))‖ + ‖(2 : ℂ)‖ :=
    norm_add_le _ _
  have h2 : ‖((mertens p : ℂ))‖ = |(mertens p : ℝ)| := by
    rw [show ((mertens p : ℂ)) = ((mertens p : ℝ) : ℂ) by push_cast; rfl]
    exact Complex.norm_real _
  have h3 : ‖(2 : ℂ)‖ = 2 := by norm_num
  linarith

end BridgeIdentityStatement
