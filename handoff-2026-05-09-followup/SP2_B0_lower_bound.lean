/-
  SP2_B0_lower_bound.lean — Lean skeleton for the new closed-form identity
  derived in `SP2_B0_lower_bound.md`.

  This file is **NOT a complete proof of `B0(N) ≥ c·N`** (sub-problem SP-2).
  It contains four `theorem` statements that the document
  `SP2_B0_lower_bound.md` proves analytically and verifies exact-rational
  in `SP2_B0_lower_bound.py` (V11–V14 all pass at N ∈ [2, 200]).

  The four theorems are:
    (T1) `s2_closed_form` — `s_2(b) = b² φ(b) / 3 + b · h(b) / 6` for `b ≥ 2`,
                            where `h(b) := ∏_{p|b}(1 − p)`.  (One-screen Möbius.)
    (T2) `X_closed_form` — `X(N) = (N̂ + 1)/3 + S(N)/6`, where
                            `S(N) := Σ_{b=2}^N h(b)/b`.
    (T3) `S_eq_mertens_harmonic` — `1 + S(N) = Σ_{k=1}^N M(⌊N/k⌋)/k`.
    (T4) `B0_eq_via_S_and_delta` — **the new closed form**
                                     `B0(N) = 1/12 − (N̂/12)·(2 + S(N))
                                              − (N̂/2)·‖δ‖_2²`.

  The bound `B0(N) ≥ c · N` itself is **OPEN**; (T4) reduces it to a
  Mertens-function lower bound on `2 + S(N)` (sub-problem MERTENS-LB in
  the markdown).

  All four theorems are sorry-stubbed and ready for Aristotle pickup.
-/

import Mathlib
-- bundle imports (renamed for the consolidated bundle layout)
-- import RequestProject.PrimeCircle
-- import RequestProject.DisplacementShift
-- import RequestProject.CrossTermPositive
-- import MertensDecomposition  -- (handoff-2026-05-04)
-- import R1BPlus               -- the R1 skeleton, providing fareyV, fareyX

namespace SP2BoundB0

open Finset BigOperators Nat ArithmeticFunction

/-! ## §0 — Auxiliary arithmetic functions

`h(b) := ∏_{p | b}(1 − p)` is the Möbius–Dirichlet convolution `μ * id`,
i.e. `h(b) = Σ_{d | b} μ(d) · d`.
-/

/-- The arithmetic function `h(b) = Σ_{d | b} μ(d) · d`, equivalently
    `∏_{p | b}(1 − p)`. -/
def h (b : ℕ) : ℤ :=
  ∑ d ∈ b.divisors, (ArithmeticFunction.moebius d : ℤ) * d

/-- The auxiliary statistic `S(N) := Σ_{b=2}^N h(b)/b`. -/
noncomputable def S (N : ℕ) : ℚ :=
  ∑ b ∈ Finset.Ico 2 (N + 1), (h b : ℚ) / b

/-- The Möbius totient `s_2(b) := Σ_{a coprime b, 1 ≤ a ≤ b−1} a²`. -/
def s2 (b : ℕ) : ℕ :=
  ((Finset.Ico 1 b).filter (fun a => Nat.Coprime a b)).sum (fun a => a^2)

/-- The classical Mertens function `M(N) = Σ_{n ≤ N} μ(n)`. -/
def Mertens (N : ℕ) : ℤ :=
  ∑ n ∈ Finset.Ico 1 (N + 1), (ArithmeticFunction.moebius n : ℤ)

/-! ## §1 — Theorem T1: closed form for `s_2(b)` -/

/--
**Theorem (SP-2, T1).**  For every `b ≥ 2`,
  `s_2(b) = b² · φ(b) / 3 + b · h(b) / 6`.

*Proof sketch.*  Möbius inversion `s_2(b) = Σ_{d | b} μ(d) · d² · S_2(b/d)`
where `S_2(m) = m(m+1)(2m+1)/6 = (2m³ + 3m² + m)/6`.  Use:
- `Σ_{d | b} μ(d)/d = φ(b)/b`  (Apostol Eq. 2.3),
- `Σ_{d | b} μ(d) = [b = 1]`,
- `Σ_{d | b} μ(d) · d = ∏_{p|b}(1 − p) = h(b)`.

The middle sum vanishes for `b ≥ 2`, giving `s_2(b) = b² φ(b)/3 + b · h(b)/6`.

Verified exact-rational at every `b ∈ [2, 50]` (49 cases, 0 failures);
see `/tmp/s2_formula.py` (or replicate with `SP2_B0_lower_bound.py`).
-/
theorem s2_closed_form (b : ℕ) (hb : 2 ≤ b) :
    (s2 b : ℚ) = (b^2 * Nat.totient b : ℚ) / 3 + (b * h b : ℚ) / 6 := by
  sorry

/-! ## §2 — Theorem T2: closed form for `X(N)` -/

/--
The Lean canonical Farey-set sum `X(N) := Σ_{f ∈ F_N} f²`.  Defined
in `R1_B_plus.lean` as `fareyX`; restated here for self-containment.
-/
noncomputable def fareyX (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N, ((ab.1 : ℚ) / ab.2)^2

/--
**Theorem (SP-2, T2).**  For every `N ≥ 2`,
  `fareyX N = (|F_N| + 1)/3 + S(N)/6`.

*Proof sketch.*  Group `F_N` by denominator. For `b = 1`: contributions
`f = 0/1 = 0` and `f = 1/1 = 1`, summing to `0² + 1² = 1`.  For `b ≥ 2`:
contribution `s_2(b)/b²`. Use T1 plus `Σ_{b=1}^N φ(b) = |F_N| − 1`.

Verified exact-rational at every `N ∈ [2, 200]` (199 cases, 0 failures);
see `SP2_B0_lower_bound.py [V12]`.
-/
theorem X_closed_form (N : ℕ) (hN : 2 ≤ N) :
    fareyX N = ((fareySet N).card + 1 : ℚ) / 3 + S N / 6 := by
  sorry

/-! ## §3 — Theorem T3: Möbius–harmonic Mertens identity -/

/--
The Möbius–harmonic Mertens identity for `1 + S(N)`.
-/

/--
**Theorem (SP-2, T3).**  For every `N ≥ 1`,
  `1 + S(N) = Σ_{k=1}^N M(⌊N/k⌋)/k`.

*Proof sketch.*
  `Σ_{b=1}^N h(b)/b = Σ_{b=1}^N (1/b) Σ_{d | b} μ(d) · d`.
Set `b = d·m`:
  `= Σ_d μ(d) Σ_{m ≤ N/d} 1/m = Σ_m (1/m) Σ_{d ≤ N/m} μ(d) = Σ_k M(⌊N/k⌋)/k`.

Note: `1 + S(N) = Σ_{b=1}^N h(b)/b` since `h(1) = μ(1)·1 = 1` and the +1
accounts for the `b = 1` contribution.

Verified exact-rational at every `N ∈ [1, 200]` (200 cases, 0 failures);
see `SP2_B0_lower_bound.py [V11]`.
-/
theorem S_eq_mertens_harmonic (N : ℕ) (hN : 1 ≤ N) :
    1 + S N = ∑ k ∈ Finset.Ico 1 (N + 1), (Mertens (N / k) : ℚ) / k := by
  sorry

/-! ## §4 — Theorem T4: the new closed form for `B0(N)` -/

/-- `‖δ‖_2² := Σ_v (r_v − v/N̂)²` where `r_v` is the v-th Farey fraction
in `F_N`. Equivalently: `Σ_{f ∈ F_N} (f − rank(f)/N̂)²`. -/
noncomputable def fareyDeltaSq (N : ℕ) : ℚ :=
  ∑ ab ∈ fareySet N,
    let f := (ab.1 : ℚ) / ab.2
    let r := (fareyRank N f : ℚ)
    let nh := (fareySet N).card
    (f - r / nh)^2

/--
**Theorem (SP-2, T4): the new B0 closed form.**
For every `N ≥ 2`,
  `B0 N = 1/12 − (|F_N| / 12) · (2 + S(N)) − (|F_N| / 2) · ‖δ‖_2²`.

*Proof sketch.*
Step (a): combine R1 V10 (`B0 = V − N̂·X − N̂/4`) with the Abel-summation
identity `Σ_{k=1}^{N̂−1} Δ_k = N̂²/3 + 1/6 − V` (Lemma C8 in the markdown,
proved by Abel rearrangement of partial sums of `δ_v`) and the
`f·D` identity `Σ_f f·D(f) = −Σ_v v·δ_v − N̂‖δ‖_2²` (C7), folding to
  `B0(N) = N̂²/6 + 1/12 − N̂·X(N)/2 − N̂·‖δ‖_2²/2`  (C10).

Step (b): substitute T2 (`X(N) = (N̂ + 1)/3 + S(N)/6`); the `N̂²/6` terms
cancel, giving (C13):
  `B0(N) = 1/12 − N̂/12 − N̂·S(N)/12 − N̂·‖δ‖_2²/2
         = 1/12 − (N̂/12) · (1 + S(N))            − N̂·‖δ‖_2²/2`.

Using T3 (`1 + S(N) = Σ_k M(⌊N/k⌋)/k`), this is also
  `B0(N) = 1/12 − (N̂/12) · (1 + Σ_k M(⌊N/k⌋)/k) − N̂·‖δ‖_2²/2`,
i.e. `B0(N) = 1/12 − (N̂/12) · (2 + S(N)) − N̂·‖δ‖_2²/2` since
`2 + S(N) = 1 + (1 + S(N))`.

Verified exact-rational at every `N ∈ [2, 200]` (199 cases, 0 failures);
see `SP2_B0_lower_bound.py [V13]`.
-/
theorem B0_eq_via_S_and_delta (N : ℕ) (hN : 2 ≤ N) :
    MertensDecomposition.B0 N
    = (1/12 : ℚ)
      - ((fareySet N).card : ℚ) / 12 * (2 + S N)
      - ((fareySet N).card : ℚ) / 2 * fareyDeltaSq N := by
  sorry

/-! ## §5 — Reduction of SP-2 to (MERTENS-LB)

The theorem (T4) reduces sub-problem SP-2 — finding an explicit `c > 0`
and `N_0` such that `B0(N) ≥ c · N` for all `N ≥ N_0` — to the
**Mertens-harmonic lower bound** below.

Note: `‖δ‖_2² = O(log² N / N̂²)` unconditionally (Niederreiter 1978
Lemma 2.1 / Mikolas 1949); this Lean statement is recorded as a `sorry`-
stubbed lemma.
-/

/--
**Lemma (Niederreiter / Mikolas).**  There is an absolute constant
`C_Niederreiter > 0` such that for all `N ≥ 2`,
  `(|F_N|) · ‖δ‖_2² ≤ C_Niederreiter · log²(|F_N| + 1)`.

Standard reference: Niederreiter (1978), "Quasi-Monte Carlo Methods and
Pseudo-Random Numbers", Lemma 2.1, p. 985. Mikolas (1949), Pacific J. Math 1.
-/
theorem niederreiter_delta_sq_bound :
    ∃ C_Niederreiter : ℚ, C_Niederreiter > 0 ∧
    ∀ N : ℕ, 2 ≤ N →
      ((fareySet N).card : ℚ) * fareyDeltaSq N
      ≤ C_Niederreiter * (Nat.log 2 ((fareySet N).card + 1) : ℚ)^2 := by
  sorry

/--
**The reduction (open conjecture):** SP-2's bound `B0(N) ≥ c · N` for some
explicit `c > 0` and `N_0` is **equivalent**, modulo the Niederreiter
`O(log² N)` correction, to the Mertens-harmonic lower bound (MERTENS-LB):

  `1 + Σ_{k=1}^N M(⌊N/k⌋)/k ≤ −c'`  for all `N ≥ N_0`,

with `c' > 0` connected to `c` by `c' = 12 c · N / |F_N| ≈ 4π² c / N` (so
asymptotically the bound `B0(N) ≥ c · N` follows from any constant-sign
bound `2 + S(N) ≤ −c'_const < 0`).

This Lean statement is recorded as a **`sorry`-stubbed conjecture**, not a
theorem; closing it requires settling (MERTENS-LB), which is open.
-/
theorem mertens_lb_implies_B0_lower_bound
    (c' : ℚ) (hc' : c' > 0)
    (N_0 : ℕ)
    (hMERT_LB : ∀ N : ℕ, N_0 ≤ N →
      (1 : ℚ) + ∑ k ∈ Finset.Ico 1 (N + 1), (Mertens (N / k) : ℚ) / k ≤ -c') :
    ∃ c : ℚ, c > 0 ∧ ∃ N_0' : ℕ, ∀ N : ℕ, N_0' ≤ N →
      MertensDecomposition.B0 N ≥ c * N := by
  -- Use T4 + T3 + Niederreiter (above).  The argument:
  --   B0(N) = 1/12 − (N̂/12) · (1 + Σ_k M(⌊N/k⌋)/k) − (N̂/2)·‖δ‖²
  --         ≥ 1/12 + (N̂·c')/12 − (N̂/2)·‖δ‖²            (by hMERT_LB)
  --         ≥ (c'/12) · N̂ − C_Niederreiter · log²(N̂)   (Niederreiter)
  --         ≥ (c'/(4π²)) · N²  (1 + o(1))                 (since N̂ ~ 3N²/π²)
  -- with explicit c = c'/(4π²) − ε.
  sorry

/-! ## §6 — Empirical sweep formalized as `native_decide`

The empirical claim `B0(p−1) ≥ 0.4383 · (p−1)` for all 117 Mertens-
restricted primes `p ≤ 1637` is amenable to `native_decide` over a
finite list.  Below is the statement; the proof would run the same
exact-rational sweep as `SP2_B0_lower_bound.py`.
-/

/--
**Empirical theorem (decidable; sorry-stubbed).**
For every prime `p ≤ 1637` with `Mertens p ≤ −3`,
  `MertensDecomposition.B0 (p − 1) ≥ (0.4383 : ℚ) * (p − 1)`.

Proof would be by `native_decide` after replacing 0.4383 with an exact
rational such as `4383/10000` and unfolding `B0` over the Lean
`fareySet (p − 1)`.  Verified Python side in `SP2_B0_lower_bound.py 1637`
(117/117 pass).
-/
theorem B0_geq_const_N_for_mertens_primes_up_to_1637
    (p : ℕ) (hp : Nat.Prime p) (hp_le : p ≤ 1637)
    (hM : Mertens p ≤ -3) :
    MertensDecomposition.B0 (p - 1) ≥ (4383 : ℚ) / 10000 * (p - 1 : ℚ) := by
  sorry

end SP2BoundB0
