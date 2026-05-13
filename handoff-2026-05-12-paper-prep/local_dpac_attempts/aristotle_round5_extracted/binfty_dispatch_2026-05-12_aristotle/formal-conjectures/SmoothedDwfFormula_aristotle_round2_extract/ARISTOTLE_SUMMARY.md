# Summary of changes for run 885c640c-55cd-48f4-9ce5-1168566619d6
## Summary

Both `sorry`s in `SmoothedDwfFormula.lean` were investigated and determined to be **unclosable against Mathlib v4.28.0**. They are left as `sorry` with detailed prerequisite comments, per protocol.

### sorry #1 — `mellin_decay` (line 214)

**Unclosable for two independent reasons:**

1. **Structural issue**: `AdmissibleWeight.M` is an unconstrained `ℂ → ℂ` with no decay hypothesis. The theorem claims superpolynomial decay for *any* such `M`, which is false for arbitrary functions. **Fix**: add a field `M_decay : ∀ σ A, ∃ C, 0 ≤ C ∧ ∀ t, ‖M ⟨σ, t⟩‖ ≤ C * (1 + |t|) ^ (-A)` to `AdmissibleWeight`, then the proof is `Wt.M_decay σ A`.

2. **Missing Mathlib infrastructure**: Even for the Gaussian specialization `M(s) = ½Γ(s/2)`, Mathlib v4.28.0 does not provide a uniform Stirling bound on vertical strips. Missing: `Complex.Gamma.uniform_stirling_strip_bound`.

### sorry #2 — `inv_zeta_polynomial_growth` (line 242)

**Unclosable — missing quantitative bound:**

Mathlib provides `riemannZeta_ne_zero_of_one_le_re` (non-vanishing on Re s ≥ 1) but NOT the quantitative polynomial bound `‖1/ζ(σ+it)‖ ≤ C·(1+|t|)^B`. This is Titchmarsh, *The Theory of the Riemann Zeta-Function*, Theorem 3.11. A proof route would require:
- For σ > 1: Euler product ⇒ |ζ(σ+it)| bounded below
- For σ = 1: non-vanishing + continuity + convexity bound  
- For σ < 1: functional equation `riemannZeta_one_sub` + Stirling + above

None of these quantitative steps are in Mathlib v4.28.0.

### What was done

- Updated TODO comments on both theorems with precise missing prerequisite names, proof routes, and Mathlib references
- Removed duplicate TODO comment block on `inv_zeta_polynomial_growth`
- Verified the file builds cleanly (`lake build SmoothedDwfFormula` succeeds)
- All other theorems in the file are preserved and compile without changes
- No `axiom` declarations were introduced