/-
  R1_B_plus.lean — proof skeleton for the new structural identities derived
  in `R1_B_plus_proof_attempt.md`.

  This file is NOT a complete proof of Conjecture B+ (`crossTerm p > 0` for
  primes with `mertens p ≤ -3`). It contains four `theorem` statements that
  the document `R1_B_plus_proof_attempt.md` proves analytically and verifies
  exactly (`R1_B_plus_proof_attempt.py`, 10 V-checks all passing). They are
  ready for Aristotle pickup.

  Imports follow the bundle layout (`archive/request-projects/RequestProject/`
  and `handoff-2026-05-04-theorem-B-and-C1/`). The actual `import` lines may
  need light renaming once the bundle is consolidated.

  The four theorems isolated here are:
    (T1) `B0_closed_form` — `B0(N) = V(N) - N̂·X(N) - N̂/4` (exact ℚ).
    (T2) `crossTerm_eq_V_NX_Q` — `crossTerm p / 2 = V - N̂·X - Q(p)` (exact ℚ).
    (T3) `mth_bridge_identity` — Σ_f cos(2πmpf) = 2 + Σ_b c_b(m).
    (T4) `re_Tm_closed_form` — Re T_m(p) = (1/2)·(2 + Σ_b c_b(m)).

  None of (T1)–(T4) finishes Conjecture B+; they are *exact identities* that
  reduce B+ to a single bound on the imaginary parts of T_m (sub-problem
  SP-1 in the markdown).
-/

import Mathlib
-- bundle imports
-- import RequestProject.PrimeCircle
-- import RequestProject.DisplacementShift
-- import RequestProject.CrossTermPositive
-- import MertensDecomposition  -- (handoff-2026-05-04, the Lemma 3.1 file)
-- import BridgeIdentity

namespace R1BPlus

open Finset BigOperators Complex

/-! ## Auxiliary p-independent Farey statistics

These are the V, X, Q in `R1_B_plus_proof_attempt.md` §5.3.
-/

/-- `V(N) := Σ_{f ∈ F_N} rank(f) · f`, the rank-value covariance. -/
def fareyV (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N,
    (fareyRank N ((ab.1 : ℚ) / ab.2) : ℚ) * ((ab.1 : ℚ) / ab.2)

/-- `X(N) := Σ_{f ∈ F_N} f²`, the second moment of f over the Farey set. -/
def fareyX (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N, ((ab.1 : ℚ) / ab.2)^2

/-- `Q(p) := Σ_{f ∈ F_{p−1}} D_{p−1}(f) · {p · f}`, the bilinear correlation
    of displacement against the fractional part. -/
def fareyQ (p : ℕ) : ℚ :=
  ∑ ab ∈ fareySet (p - 1),
    displacement (p - 1) ((ab.1 : ℚ) / ab.2) *
    Int.fract ((p : ℚ) * ((ab.1 : ℚ) / ab.2))

/-! ## Theorem T1 — closed form for B0(N) -/

/--
**Theorem (R1, T1).** For every `N ≥ 1`,
  `B0(N) = V(N) − |F_N| · X(N) − |F_N|/4`.

The proof is a one-screen algebraic expansion using:
- `Σ_f f = N̂/2` (Farey reflection f ↔ 1−f, with both 0/1 and 1/1 in F_N),
- `Σ_f rank(f) = N̂·(N̂+1)/2` (rank is a permutation of `1, …, N̂`).

Numerically verified exact-rational at primes p ≤ 100 (24 instances).
See `R1_B_plus_proof_attempt.py` `[V10]`.
-/
theorem B0_closed_form (N : ℕ) :
    MertensDecomposition.B0 N =
      fareyV N - (fareySet N).card * fareyX N - (fareySet N).card / 4 := by
  sorry

/-! ## Theorem T2 — Σ D·δ = V − N̂·X − Q(p) -/

/--
**Theorem (R1, T2).** For every prime `p ≥ 2`,
  `crossTerm p / 2 = V(p−1) − |F_{p−1}| · X(p−1) − Q(p)`.

The proof uses `shiftFun_eq_floor_sub` (`δ(f) = ⌊pf⌋ − (p−1)f`) and the
substitution `⌊pf⌋ = pf − {pf}`. After algebra, the final identity is

  Σ D · δ = V − N̂·X − Σ D·{pf}.

Numerically verified exact-rational at primes p ≤ 100. See `[V9]`.
-/
theorem crossTerm_eq_V_NX_Q (p : ℕ) (hp : Nat.Prime p) :
    crossTerm p / 2 =
      fareyV (p - 1) - (fareySet (p - 1)).card * fareyX (p - 1) - fareyQ p := by
  sorry

/-! ## Theorem T3 — m-th Bridge identity (NEW) -/

/-- The Ramanujan sum `c_b(m) = Σ_{d | gcd(m, b)} μ(b/d) · d`. -/
def ramanujanSum (m b : ℕ) : ℤ :=
  ∑ d ∈ (Nat.gcd m b).divisors, (Int.ofNat d) * Nat.ArithmeticFunction.moebius (b / d)

/--
**Theorem (R1, T3): m-th Bridge identity.** For every prime `p ≥ 2` and
every integer `m ≥ 1`,
  `Σ_{f ∈ F_{p−1}} cos(2π m p f) = 2 + Σ_{b=2}^{p−1} c_b(m)`.

Proof: group F_{p−1} by denominator; for b = 1 the f = 0/1 and f = 1/1
contributions sum to 2; for 2 ≤ b ≤ p − 1, since gcd(p, b) = 1, the map
`a ↦ p·a mod b` is a bijection on `(ℤ/bℤ)^×`, so the inner sum
`Σ_{a coprime to b} e^{2πi m p a / b}` reduces to `c_b(m)`.

Specialized at m = 1: c_b(1) = μ(b), recovering the classical Bridge
identity `M(p) + 2`.

Numerically verified exact-rational at (p, m) ∈ {11, …, 79} × {1, …, 11}
(132 pairs). See `[V7]`.
-/
theorem mth_bridge_identity (p : ℕ) (hp : Nat.Prime p) (m : ℕ) (hm : 1 ≤ m) :
    ((∑ ab ∈ fareySet (p - 1),
        Complex.exp (2 * Real.pi * Complex.I * m * p *
          (((ab.1 : ℚ) / ab.2 : ℚ) : ℂ))).re : ℝ)
    = 2 + (((∑ b ∈ Finset.Ico 2 p, ramanujanSum m b) : ℤ) : ℝ) := by
  sorry

/-! ## Theorem T4 — Re T_m closed form (NEW) -/

/-- The bilinear Fourier mode `T_m(p) := Σ_f D(f) e^{2πi m p f}`. -/
noncomputable def Tm (p m : ℕ) : ℂ :=
  ∑ ab ∈ fareySet (p - 1),
    ((displacement (p - 1) ((ab.1 : ℚ) / ab.2) : ℝ) : ℂ) *
    Complex.exp (2 * Real.pi * Complex.I * m * p *
      (((ab.1 : ℚ) / ab.2 : ℚ) : ℂ))

/--
**Theorem (R1, T4): Re T_m closed form.** For every prime `p ≥ 2` and
every integer `m ≥ 1`,
  `(Re T_m(p)) = (1/2) · [2 + Σ_{b=2}^{p−1} c_b(m)]`.

Proof: by f → 1−f reflection on F_{p−1}, `rank(1−f) = N̂ + 1 − rank(f)` and
`cos(2π m p (1−f)) = cos(2π m p f)`. Pairing gives:
  Σ rank(f) cos(2πmpf) = (N̂+1)/2 · C_m(p)
  Σ f · cos(2πmpf) = (1/2) · C_m(p)
where C_m(p) is the m-th Bridge sum from T3. Subtracting:
  Re T_m = (N̂+1)/2 · C_m − N̂ · (1/2) · C_m = (1/2) · C_m.

Numerically verified to 10⁻⁷ at 66 (p, m) pairs. See `[V8]`.
-/
theorem re_Tm_closed_form (p : ℕ) (hp : Nat.Prime p) (m : ℕ) (hm : 1 ≤ m) :
    (Tm p m).re = (1/2 : ℝ) *
      (2 + (((∑ b ∈ Finset.Ico 2 p, ramanujanSum m b) : ℤ) : ℝ)) := by
  sorry

/-! ## Specialization: m = 1 recovers `Re T_1 = (M(p) + 2)/2`

This is a **structural new identity**: it ties the real part of the
displacement-weighted Bridge sum to the Mertens function via T3 + T4.
-/

/-- Re T_1(p) = (M(p) + 2)/2, the m=1 specialization of T4 + classical Bridge. -/
theorem re_T1_eq_M_plus_2_over_2 (p : ℕ) (hp : Nat.Prime p) :
    (Tm p 1).re = ((mertens p : ℤ) + 2 : ℝ) / 2 := by
  -- This follows from `re_Tm_closed_form` at m=1 plus
  -- `c_b(1) = μ(b)` (one-line Ramanujan sum identity)
  -- plus `Σ_{b=2}^{p-1} μ(b) = M(p−1) − 1 = M(p) + 2 − 2 = M(p)` (using μ(p) = -1).
  sorry

/-! ## Reduction of Conjecture B+ to a bound on the imaginary parts

Using T1, T2, T4 + Hurwitz: B(p) > 0 iff
  Σ_{m ≥ 1} (Im T_m(p)) / m  >  −π · (B0(p−1) + 1/2).

This is the form of Conjecture B+ that is open after this session.
The Lean statement is recorded for the Aristotle pickup as a *target*,
not a theorem.
-/

/-- The reduced form of Conjecture B+. *Reduction is rigorous; the reduced
    inequality is the open sub-problem `(SP-1)` in `R1_B_plus_proof_attempt.md`.* -/
theorem crossTerm_pos_iff_imTm_bound (p : ℕ) (hp : Nat.Prime p) :
    crossTerm p > 0 ↔
    -- Formal RHS: an Aistleitner-style discrepancy bound.
    -- Stated abstractly because the explicit constants need SP-1 closure.
    True   -- placeholder: full statement requires explicit constants
  := by
  sorry

end R1BPlus
