/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

This file is the verbatim Dirichlet Polynomial Avoidance Conjecture (DPAC)
Lean skeleton submitted to google-deepmind/formal-conjectures PR #3716
on 2026-04-11, repackaged for Aristotle dispatch under the
RequestProject/ namespace.  No mathematical content has been altered:
the single `theorem dirichlet_polynomial_avoidance_conjecture` carries
the same `:= by sorry` placeholder, and the docstrings, attributes
(`@[category research_open]`, `@[AMS 11M26, 30D15]`), Mathlib imports,
and Möbius–Dirichlet polynomial definition are bit-for-bit identical
to the upstream PR.  The only edit is administrative: the namespace
adjustment from `FormalConjectures.Paper` (DeepMind layout) to the
flat `RequestProject` layout used by the Aristotle dispatcher.

See `RequestProject/DPAC.lean` for the expanded formalization with
conditional bridges, the density-one comparison skeleton, and the
proved algebraic identity `moebiusDirichletPoly_eq_gammaExponentialPoly`.
-/

import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.NumberTheory.ArithmeticFunction
import Mathlib.NumberTheory.LSeries.RiemannZeta

/-!
# Dirichlet Polynomial Avoidance Conjecture

## Source
Saar Shai, "Prime Spectroscopy of Riemann Zeros" (2026), Section 3.
GitHub: https://github.com/SaarShai/Primes-Equispaced
AI Disclosure: Conjecture formulated with assistance from Claude (Anthropic).

## Statement
For fixed K ≥ 2, the truncated Möbius Dirichlet polynomial
  c_K(s) = Σ_{k=2}^{K} μ(k) · k^{-s}
is nonzero at every nontrivial zero of the Riemann zeta function.

## Evidence
- Verified via interval arithmetic (100-digit precision) for K ∈ {10, 20, 50}
  at the first 100 nontrivial zeta zeros: all 300 cases certified nonzero.
- The polynomial c_K has infinitely many zeros in the critical strip
  (Langer 1931, ~0.51T zeros up to height T for K=10), but these zeros
  appear to systematically avoid zeta zero ordinates.
- Statistical anomaly: min|c_K(ρ)| at zeta zeros exceeds min|c_K| at generic
  points on Re(s)=1/2 by a factor of 9x (K=10) to 52x (K=20).
- Under RH, |c_K(ρ)| → ∞ as K → ∞ for each fixed zero ρ, consistent with
  the pole of 1/ζ(s) at zeros.

## Difficulty
Comparable to the Linear Independence hypothesis (LI) for zeta zeros.
The zeros of c_K are determined by small-prime arithmetic; the zeros of ζ
by all primes. Proving they never coincide requires understanding the
arithmetic independence between these structures.
-/

/-- For fixed K ≥ 2 and any nontrivial zero ρ of the Riemann zeta function,
the truncated Möbius Dirichlet polynomial c_K(ρ) = Σ_{k=2}^{K} μ(k) · k^{-ρ}
is nonzero. -/
theorem dirichlet_polynomial_avoidance_conjecture
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    (∑ k ∈ Finset.range (K - 1), (ArithmeticFunction.moebius (k + 2) : ℂ) *
      ((k + 2 : ℂ) ^ (-ρ))) ≠ 0 := by
  sorry
