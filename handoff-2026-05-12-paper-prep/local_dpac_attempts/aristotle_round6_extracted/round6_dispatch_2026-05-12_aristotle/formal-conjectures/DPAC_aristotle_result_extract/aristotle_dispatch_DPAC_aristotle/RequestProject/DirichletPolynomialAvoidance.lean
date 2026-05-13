/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

This file is the verbatim Dirichlet Polynomial Avoidance Conjecture (DPAC)
Lean skeleton submitted to google-deepmind/formal-conjectures PR #3716
on 2026-04-11, repackaged for Aristotle dispatch under the
RequestProject/ namespace.  No mathematical content has been altered.

Note on attributes: Lean 4.28.0 does not support multiple `@[…]` blocks
on one declaration nor AMS-style codes (e.g. `11M26`) as attribute arguments.
The original attribute annotations `@[category research_open]` and
`@[AMS 11M26, 30D15]` are therefore represented as `@[category, AMS]` with
the original annotations preserved in this comment.  The docstring is moved
before the attribute block to comply with Lean 4 grammar.  The sum syntax
`∑ k in` is replaced with `∑ k ∈` per Mathlib v4.28.0 convention.
-/

import RequestProject.Attrs
import Mathlib

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

## Partial results
- Unconditional: c_K(ρ) ≠ 0 for all but a density-zero subset of nontrivial
  zeros (follows from Langer's zero count O(T) vs N(T) ~ (T/2π) log T).
- GRH-conditional: The Mertens spectroscope F(γ_k)/F_avg → ∞ for all zeros.

## Difficulty
Comparable to the Linear Independence hypothesis (LI) for zeta zeros.
The zeros of c_K are determined by small-prime arithmetic; the zeros of ζ
by all primes. Proving they never coincide requires understanding the
arithmetic independence between these structures.

## Proof strategy (this file)

We pursue reduction R3 (LI ⟹ DPAC):
1. Define the Linear Independence Hypothesis (LI) for zeta-zero ordinates.
2. Define the truncated Möbius–Dirichlet polynomial `moebiusDirichletPoly`.
3. State and prove a conditional theorem `dpac_of_LI` showing LI ⟹ DPAC.
   The core analytic step (that LI prevents vanishing of finite exponential
   sums at zeta-zero ordinates) requires Mathlib infrastructure that does
   not yet exist in v4.28.0 and is left as a sorry with a TODO comment.
4. The main theorem `dirichlet_polynomial_avoidance_conjecture` remains
   with sorry, noting that it follows from LI + the conditional result.

We also provide a density-one framework (R1) showing that, unconditionally,
the set of zeta zeros where c_K vanishes has natural density zero.
-/

noncomputable section

open Complex Finset BigOperators

/-! ## The truncated Möbius–Dirichlet polynomial -/

/-- The truncated Möbius–Dirichlet polynomial c_K(s) = Σ_{n=2}^{K} μ(n) · n^{-s}. -/
def moebiusDirichletPoly (K : ℕ) (s : ℂ) : ℂ :=
  ∑ k ∈ Finset.range (K - 1),
    (ArithmeticFunction.moebius (k + 2) : ℂ) * ((k + 2 : ℂ) ^ (-s))

/-! ## Reduction R3: Linear Independence Hypothesis ⟹ DPAC -/

/-- The Linear Independence Hypothesis (LI) for the imaginary parts of
nontrivial Riemann zeta zeros: the multiset of positive ordinates
{γ : ρ = β + iγ is a nontrivial zeta zero with γ > 0} is linearly
independent over ℚ.

We state this as: for any finite ℚ-linear combination of distinct
positive zeta-zero ordinates, the combination is nonzero unless all
coefficients are zero. -/
def LinearIndependenceHypothesis : Prop :=
  ∀ (n : ℕ) (γ : Fin n → ℝ) (a : Fin n → ℚ),
    (∀ i, ∃ ρ : ℂ, riemannZeta ρ = 0 ∧ 0 < ρ.re ∧ ρ.re < 1 ∧ ρ.im = γ i ∧ 0 < γ i) →
    Function.Injective γ →
    (∑ i, (a i : ℝ) * γ i = 0) →
    ∀ i, a i = 0

/-- **Key analytic bridge (R3)**: Under the Linear Independence Hypothesis,
the truncated Möbius–Dirichlet polynomial c_K(s) does not vanish at any
nontrivial zero of the Riemann zeta function.

**Proof sketch**: If c_K(ρ) = 0 for ρ = β + iγ with ζ(ρ) = 0 and
0 < β < 1, then Σ_{n=2}^{K} μ(n) n^{-β} exp(-iγ log n) = 0.
Separating real and imaginary parts gives two linear relations involving
{cos(γ log n), sin(γ log n)}_{n squarefree, 2 ≤ n ≤ K}. By Kronecker's
theorem on simultaneous Diophantine approximation, such a vanishing for a
non-trivial exponential sum with algebraically independent frequencies
{log 2, log 3, log 5, ...} implies a ℚ-linear dependence among the
ordinates {γ_j}, contradicting LI.

The formal proof of this bridge requires:
- Kronecker's theorem / Bohr's theory of almost-periodic functions
- The structure of exponential sums over squarefree integers
- The connection between ℚ-linear independence of {γ_j} and
  non-vanishing of Dirichlet polynomials

None of these are available in Mathlib v4.28.0. -/
theorem dpac_of_LI
    (hLI : LinearIndependenceHypothesis)
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  -- TODO(aristotle): Kronecker–Bohr almost-periodic nonvanishing under LI
  -- Requires: Bohr's theory of almost-periodic functions (not in Mathlib v4.28.0),
  -- Kronecker's theorem on simultaneous approximation (not in Mathlib v4.28.0),
  -- and the structure theory of exponential sums over squarefree integers.
  sorry

/-! ## Reduction R1: Density-one avoidance (unconditional)

### Framework

The density-one result follows from comparing zero counts:
- **Langer (1931)**: c_K has at most C·T zeros with imaginary part in [0,T],
  where C depends on K but not on T.
- **Classical**: ζ has N(T) ~ (T/2π) log T nontrivial zeros with
  imaginary part in [0,T].

Therefore the ratio |{j ≤ N : c_K(ρ_j) = 0}| / N → 0 as N → ∞.

We formalize the logical skeleton: given any two counting functions where
one grows as O(T) and the other as Θ(T log T), the former is o(the latter).
-/

/-
**Density-zero from growth rates**: If a sequence of real numbers is
enumerated so that the n-th term grows like n / log n (as for zeta-zero
ordinates ordered by height), and a subset S of indices satisfies
|{j ≤ N : j ∈ S}| ≤ C · (N-th ordinate) for some constant C, then the
natural density of S is zero.

This is the purely real-analytic backbone of the density-one argument.
The actual derivation requires Langer's zero-counting bound and the
classical N(T) formula, neither of which is in Mathlib v4.28.0.
-/
theorem density_zero_from_growth_comparison
    (f : ℕ → ℝ)  -- f(N) counts "bad" zeros up to the N-th zeta zero
    (g : ℕ → ℝ)  -- g(N) = N (counts all zeta zeros up to the N-th)
    (C : ℝ) (_hC : 0 < C)
    (hf_bound : ∀ N, f N ≤ C * (N / Real.log N))
    (hg_def : ∀ N, g N = N)
    (hf_nonneg : ∀ N, 0 ≤ f N) :
    Filter.Tendsto (fun N => f N / g N) Filter.atTop (nhds 0) := by
  -- We need to show that $f(N) / N \leq C / \log N$ for all $N \geq 2$.
  have h_bound : ∀ N ≥ 2, (f N / (g N : ℝ)) ≤ C / Real.log N := by
    intro N hN; rw [ hg_def, div_le_iff₀ ] <;> first | positivity | convert hf_bound N using 1 ; ring;
  exact squeeze_zero_norm' ( Filter.eventually_atTop.mpr ⟨ 2, fun N hN => by rw [ Real.norm_of_nonneg ( div_nonneg ( hf_nonneg N ) ( hg_def N ▸ Nat.cast_nonneg _ ) ) ] ; exact h_bound N hN ⟩ ) ( tendsto_const_nhds.div_atTop ( Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop ) )

/-! ## Main theorem -/

-- Original upstream attributes: @[category research_open] @[AMS 11M26, 30D15]
/-- For fixed K ≥ 2 and any nontrivial zero ρ of the Riemann zeta function,
the truncated Möbius Dirichlet polynomial c_K(ρ) = Σ_{k=2}^{K} μ(k) · k^{-ρ}
is nonzero. -/
@[category, AMS]
theorem dirichlet_polynomial_avoidance_conjecture
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    (∑ k ∈ Finset.range (K - 1), (ArithmeticFunction.moebius (k + 2) : ℂ) *
      ((k + 2 : ℂ) ^ (-ρ))) ≠ 0 := by
  -- This is the full DPAC, a research-open conjecture comparable in
  -- difficulty to the Linear Independence Hypothesis (LI) for zeta zeros.
  --
  -- Under LI, the result follows from `dpac_of_LI` above.
  -- Unconditionally, the density-one reduction (R1) shows that c_K(ρ) ≠ 0
  -- for all but a density-zero set of nontrivial zeros, but this does not
  -- yield the universal quantification required here.
  --
  -- TODO(aristotle): full unconditional proof of DPAC
  sorry

end