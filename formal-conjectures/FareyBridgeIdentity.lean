/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Farey Bridge Identity (Lemma 3.1 of Shai 2026)

## Source
Saar Shai, "Per-Step Farey Discrepancy" (2026), Lemma 3.1.
This file is part of the Saar–Koyama joint paper's `formal-conjectures/`
Lean inventory; see `handoff-2026-05-12-paper-prep/SECTION_DRAFT_2026-05-12.md`
of the joint manuscript for the broader context.

## Mathematical content

For every prime `p ≥ 2`, the exponential sum over the Farey sequence
`F_{p-1}` evaluated at frequency `p` equals the Mertens function plus 2:

    ∑_{a/b ∈ F_{p-1}} e^(2π i p a / b)  =  M(p) + 2 ,

where `F_{p-1}` is the Farey sequence of order `p-1` (irreducible
fractions `a/b ∈ [0, 1]` with `b ≤ p-1`) and `M(p) := ∑_{k ≤ p} μ(k)`
is the Mertens function.

The identity decomposes into Ramanujan sums: the contribution from
denominator `b` is `c_b(p)` (the Ramanujan sum), which equals
`μ(b)` when `gcd(p, b) = 1` (i.e., for `b < p` and `p` prime, every
`b` is coprime to `p`).  Summing `μ(b)` over `b ≤ p - 1` plus the two
boundary fractions `0/1` and `1/1` gives `M(p) + 2`.

## Status

The mathematical proof is at the textbook level (Ramanujan-sum
decomposition + Möbius summation).  The Lean formalisation needs a
*concrete definition of the Farey sequence in Mathlib*, which is not
upstream as of v4.28.0.  We define `FareySet` locally below as
`Finset (ℕ × ℕ)` of coprime pairs `(a, b)` with `b ≤ n`, and state
the identity against that definition.  The proof is research-open
at the Lean level pending: (a) a more polished `FareySet` definition
matching Mathlib conventions, (b) the Mathlib Ramanujan-sum library
which is partial at v4.28.0.

References:
* Hardy & Wright, "An Introduction to the Theory of Numbers" (6th ed.),
  Theorem 304 (Ramanujan sum at primes).
* Saar Shai, "Per-Step Farey Discrepancy" (2026), Lemma 3.1, GitHub
  archive at `archive/request-projects/RequestProject/BridgeIdentity.lean`
  (an earlier scaffolding effort in this project).
-/

namespace FareyBridgeIdentity

open Nat Finset Complex BigOperators ArithmeticFunction

/-- `FareySet n` is the set of coprime pairs `(a, b)` in `ℕ × ℕ` with
`b ≥ 1` and `b ≤ n` and `a ≤ b` (so `a/b ∈ [0, 1]`).  This is the
Farey sequence of order `n` represented as a `Finset` of pairs.

(Mathlib at v4.28.0 does not yet have a dedicated `FareySequence`
definition; we use the natural ad-hoc one.) -/
def FareySet (n : ℕ) : Finset (ℕ × ℕ) :=
  (Finset.range (n + 1)).biUnion (fun b =>
    if h : b = 0 then ∅
    else
      (Finset.range (b + 1)).filter
        (fun a => Nat.Coprime a b)
      |>.image (fun a => (a, b))
    )

/-- The Mertens function `M(n) := ∑_{k = 1}^{n} μ(k)`. -/
noncomputable def mertens (n : ℕ) : ℤ :=
  ∑ k ∈ Finset.range (n + 1), ArithmeticFunction.moebius k

/--
**Farey Bridge Identity (Lemma 3.1 of Shai 2026).**

For every prime `p ≥ 2`,

    ∑_{(a, b) ∈ FareySet (p - 1)} e^(2π i p · a / b)  =  (M(p) + 2 : ℂ) .

The proof decomposes the sum by denominator `b`, recognises the
inner sum over coprime `a` as the Ramanujan sum `c_b(p) = μ(b)`
(valid since `b < p` ⇒ `gcd(p, b) = 1` ⇒ `c_b(p) = μ(b)`), and
collects the boundary contributions from `(0, 1)` and `(1, 1)`.

Status: **research-open in Lean**.  Mathlib v4.28.0 provides
`Nat.Coprime`, `ArithmeticFunction.moebius`, `Complex.exp`,
`Finset.sum`, and the basic Möbius-sum identities but no direct
`RamanujanSum` API.  The proof requires:

* `Mathlib.NumberTheory.RamanujanSum` (or equivalent): the identity
  `c_q(n) = μ(q / gcd(q,n)) · φ(q) / φ(q / gcd(q,n))`, specialising
  at `gcd(p, q) = 1` to `c_q(p) = μ(q)`.

Pen-and-paper proof: see Saar Shai, "Per-Step Farey Discrepancy"
(2026), §3.1. -/

theorem farey_bridge_identity
    (p : ℕ) (hp : Nat.Prime p) :
    ∑ pair ∈ FareySet (p - 1),
        Complex.exp
          ((2 * Real.pi : ℂ) * Complex.I * (p : ℂ) *
           (pair.1 : ℂ) / (pair.2 : ℂ))
      = (mertens p : ℂ) + 2 := by
  -- MATHLIB-PREREQ: Ramanujan-sum identity `c_q(p) = μ(q)` at primes
  -- `p` coprime to `q`.  Mathlib v4.28.0 does not yet provide this.
  -- Pen-and-paper proof: Saar Shai 2026, Lemma 3.1.
  sorry

end FareyBridgeIdentity
