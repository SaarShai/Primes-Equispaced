/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

# Local Perron double-pole residue (Lemma X.3.1 of the Saar–Koyama paper)

The shifted Perron integrand `F(w) = K^w / (w * L(w + ρ))`, where `L`
is analytic at `ρ` with a simple zero there, has a double pole at
`w = 0`. The Laurent coefficient of `w^{-1}` (the "residue") is

    log K / L'(ρ) - L''(ρ) / (2 * L'(ρ)^2).

This is the algebraic content of Lemma X.3.1 of the joint manuscript
and the load-bearing identity for Theorem X.4.2. No deep mathematics
(no RH, no DRH) is used; it is pure Laurent algebra.

This file states the identity as a limit relation, avoiding
dependence on Mathlib's partial meromorphic-residue API. The proof
is the routine Taylor expansion of `1/L` at a simple zero combined
with the expansion of `K^w/w`. Whether the formal Lean proof goes
through against Mathlib v4.28.0 depends on the availability of
second-order Taylor-coefficient extraction; until that is verified
the proof is left as `sorry` with a research-open comment. The
mathematical proof is fully written out in Appendix B §B.2 of the
joint manuscript.

References:
* Saar Shai – Shin-ya Koyama, joint manuscript, §X.3 of the
  Technical/Computational section.
* Full pen-and-paper proof: Appendix B (`APPENDIX_B_CK_SUBLEADING_PROOF.md`)
  §B.2.
-/

import Mathlib

namespace LocalPerronResidue

open Complex Filter

/-- The "subleading constant"
`C₁(L, ρ) := - L''(ρ) / (2 · L'(ρ)²)`.
This is the constant appearing in the second term of the
Laurent expansion of `1/L(w + ρ)` at `w = 0`. -/
noncomputable def C₁ (L : ℂ → ℂ) (ρ : ℂ) : ℂ :=
  - (iteratedDeriv 2 L ρ) / (2 * (deriv L ρ) ^ 2)

/-- The "double-pole residue coefficient" of `F(w) := K^w / (w · L(w + ρ))`
at `w = 0`, when `L` has a simple zero at `ρ`. -/
noncomputable def perronResidue (K : ℝ) (L : ℂ → ℂ) (ρ : ℂ) : ℂ :=
  (Real.log K : ℂ) / deriv L ρ + C₁ L ρ

/-- The double-pole leading coefficient of `F(w)` (coefficient of `w^{-2}`). -/
noncomputable def perronDoublePole (L : ℂ → ℂ) (ρ : ℂ) : ℂ :=
  1 / deriv L ρ

/--
**Lemma X.3.1 (Local Perron double-pole residue).**

Let `K > 1` be real, and let `L : ℂ → ℂ` be analytic at `ρ ∈ ℂ` with
a simple zero at `ρ` (`L ρ = 0`, `deriv L ρ ≠ 0`).  Then the function
`F(w) := K^w / (w · L(w + ρ))` admits the Laurent expansion at
`w = 0`

    F(w) = perronDoublePole L ρ / w²
         + perronResidue K L ρ / w
         + holomorphic_at_0(w),

equivalently expressed as

    lim_{w → 0, w ≠ 0}
        ( F(w) - perronDoublePole L ρ / w² - perronResidue K L ρ / w )
      = 0.

The proof is the routine Laurent expansion: `1/L(w+ρ) = 1/(L'(ρ)·w)
- L''(ρ)/(2·L'(ρ)²) + O(w)` (Taylor inversion at a simple zero), and
`K^w/w = 1/w + log K + O(w)`; their product gives the stated
coefficients.

The proof against Mathlib v4.28.0 requires extracting the Taylor
coefficients of `L` at `ρ` to second order, which is closable via
`AnalyticAt.hasFPowerSeriesAt` and explicit coefficient
manipulation. Until the precise Mathlib API for the Taylor-inversion
step is verified, the proof is `sorry` with the *research-open*
status for the Lean formalization; the mathematical proof is fully
written out in Appendix B §B.2 of the joint manuscript.
-/
@[category research_open]
theorem local_perron_residue
    (K : ℝ) (hK : (1 : ℝ) < K)
    (L : ℂ → ℂ) (ρ : ℂ)
    (h_L_analytic : AnalyticAt ℂ L ρ)
    (h_L_zero : L ρ = 0)
    (h_Lp : deriv L ρ ≠ 0) :
    -- The Laurent-coefficient identity, stated as a limit.
    Tendsto
      (fun w : ℂ =>
        ((K : ℂ) ^ w / (w * L (w + ρ)))
          - perronDoublePole L ρ / w ^ 2
          - perronResidue K L ρ / w)
      (nhdsWithin 0 ({0} : Set ℂ)ᶜ) (nhds 0) := by
  -- MATHLIB-PREREQ: `AnalyticAt.hasFPowerSeriesAt` extraction of the
  -- second-order Taylor coefficient of `L` at `ρ`; combined with the
  -- Taylor expansion of `K^w` (entire) the result is mechanical.
  -- Pen-and-paper proof in Appendix B §B.2 of the joint manuscript.
  sorry

/-- The defining equality between `perronResidue` and the
explicit-coefficient form
`log K / L'(ρ) - L''(ρ) / (2 · L'(ρ)²)`.  This is the algebraic
identity used in Theorem X.4.2; the proof is `rfl` modulo
definitional unfolding. -/
theorem perronResidue_eq
    (K : ℝ) (L : ℂ → ℂ) (ρ : ℂ) :
    perronResidue K L ρ
      = (Real.log K : ℂ) / deriv L ρ
        - iteratedDeriv 2 L ρ / (2 * (deriv L ρ) ^ 2) := by
  unfold perronResidue C₁
  ring

end LocalPerronResidue
