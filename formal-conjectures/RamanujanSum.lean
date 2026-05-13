/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Ramanujan sum at primes (project-local formalisation)

A minimal Lean 4 / Mathlib v4.28.0 formalisation of the
**Ramanujan-sum-at-primes identity** sufficient to discharge the
`h_ramanujan_decomp` hypothesis in `FareyBridgeIdentity.lean`.

We use the Möbius-inversion form
`c_q(n) := ∑_{d ∣ gcd(q, n)} d * μ(q / d)` (Hardy & Wright,
*An Introduction to the Theory of Numbers*, 6th ed., Theorem 271);
this is integer-valued and avoids any complex-roots-of-unity setup.

Main result: `ramanujan_sum_prime_coprime` — for any `q ≥ 1` and
prime `p` with `gcd(p, q) = 1`, `c_q(p) = μ(q)`. This is Hardy &
Wright Theorem 304.
-/

namespace RamanujanSum

open Nat ArithmeticFunction

/-- Ramanujan sum in its Möbius-inversion form. -/
noncomputable def ramanujanSum (q n : ℕ) : ℤ :=
  ∑ d ∈ (Nat.gcd q n).divisors, (d : ℤ) * ArithmeticFunction.moebius (q / d)

/-- **Hardy & Wright, Theorem 304.** For any `q ≥ 1` and a prime
`p` coprime to `q`, the Ramanujan sum `c_q(p)` equals `μ(q)`. -/
theorem ramanujan_sum_prime_coprime
    (q p : ℕ) (_hq : 1 ≤ q) (_hp : Nat.Prime p)
    (h_coprime : Nat.Coprime p q) :
    ramanujanSum q p = ArithmeticFunction.moebius q := by
  -- Strategy: gcd(q, p) = 1 by coprimality, so the divisor set of
  -- gcd(q, p) is just {1}. The sum reduces to its d = 1 term:
  -- (1 : ℤ) * μ(q / 1) = μ(q).
  unfold ramanujanSum
  have h_gcd : Nat.gcd q p = 1 := by
    rw [Nat.gcd_comm]
    exact h_coprime
  rw [h_gcd, Nat.divisors_one, Finset.sum_singleton, Nat.div_one]
  simp

end RamanujanSum
