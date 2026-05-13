# Aristotle dispatch: close the two remaining `sorry`s in SmoothedDwfFormula_full.lean

This file (`SmoothedDwfFormula.lean`) contains the smoothed Δw_f explicit
formula proof skeleton against Mathlib v4.28.0. There are two remaining
`sorry`s. Please close them or report the exact Mathlib prerequisite if
they cannot be closed against Mathlib v4.28.0.

## sorry #1 — `mellin_decay` (line 211)

Statement:
```
theorem mellin_decay
    (Wt : AdmissibleWeight) (σ : ℝ) (A : ℝ) :
    ∃ C : ℝ, 0 ≤ C ∧
      ∀ t : ℝ, ‖Wt.M ⟨σ, t⟩‖ ≤ C * (1 + |t|) ^ (-A) := by
  sorry
```

The needed analytic fact: for the canonical Gaussian Mellin transform
`M_W(s) = ½ Γ(s/2)`, the Stirling bound on vertical strips gives
`|M_W(σ + it)| ≤ C(σ) · (1+|t|)^{σ/2 − ½} · exp(−π|t|/4)`.
This is superpolynomial decay, which implies the polynomial bound.

Strategy options:
  (a) Use `Complex.Gamma_abs_le` or `Complex.norm_Gamma` from Mathlib (if
      it exists) plus the exponential factor of Stirling.
  (b) Add a decay axiom to `AdmissibleWeight` and prove the lemma for it.
  (c) If Mathlib v4.28.0 lacks the uniform Stirling bound on strips,
      report this as the prerequisite and leave a TODO.

## sorry #2 — `inv_zeta_polynomial_growth` (line 237)

Statement:
```
theorem inv_zeta_polynomial_growth
    (σ : ℝ) (_hσ : σ ≠ 1) :
    ∃ (B C : ℝ), 0 ≤ C ∧
      ∀ t : ℝ, riemannZeta ⟨σ, t⟩ ≠ 0 →
        ‖1 / riemannZeta ⟨σ, t⟩‖ ≤ C * (1 + |t|) ^ B := by
  sorry
```

The needed analytic fact: polynomial bound on `1/ζ(s)` on vertical lines
off `Re s = 1`. Titchmarsh Theorem 3.11. Mathlib has individual
non-vanishing on `Re s ≥ 1` but not the polynomial bound.

Strategy options:
  (a) Search Mathlib v4.28.0 for any `riemannZeta_*polynomial*` lemma.
  (b) Route through the functional equation `Complex.riemannZeta_one_sub`
      and a polynomial bound on the completed zeta function.
  (c) If unclosable, report as prerequisite.

## Protocol

- NO `axiom`. If unclosable in v4.28.0, leave as `sorry` with a comment
  naming the missing Mathlib lemma.
- Each closed theorem must `lake build` cleanly.
- Preserve every other theorem in the file. Only edit the two `sorry`
  bodies and (if necessary) add Mathlib `open` directives at the top.
