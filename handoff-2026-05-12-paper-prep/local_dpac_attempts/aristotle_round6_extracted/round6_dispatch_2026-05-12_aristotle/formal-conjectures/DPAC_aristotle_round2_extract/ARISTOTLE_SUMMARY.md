# Summary of changes for run bb0cd153-0364-48e2-85fd-564fd8ce4679
# DPAC Dispatch Summary

## Sorry #1 — `moebiusDirichletPoly_eq_gammaExponentialPoly` (was line ~164): **CLOSED ✓**

This was the algebraic identity showing that the complex-power Dirichlet polynomial `(k+2)^(-ρ)` equals the explicit fixed-line exponential form `(k+2)^(-β) * exp(-iγ log(k+2))`. The proof:
- Reduces to per-summand equality via `Finset.sum_congr`
- Uses `Complex.cpow_def_of_ne_zero` to unfold complex powers
- Applies `Real.rpow_def_of_pos` for the real-power component
- Handles the exponential-log manipulation with `norm_num` and `ring`

The proof uses only standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

## Sorry #2 — `dirichlet_polynomial_avoidance_conjecture` (main theorem): **RESEARCH-OPEN, left as `sorry`**

This is the full DPAC conjecture: for every K ≥ 2 and every nontrivial zeta zero ρ, the truncated Möbius polynomial c_K(ρ) ≠ 0. This is comparable in difficulty to the Linear Independence Hypothesis for zeta-zero ordinates — no unconditional proof exists in the literature.

Missing Mathlib prerequisites for even partial progress:
- Zero-counting for finite exponential polynomials (Langer 1931): no `N_{c_K}(T) = O(T)` in Mathlib
- Riemann–von Mangoldt formula `N(T) ~ (T/2π) log T`: not in Mathlib
- Joint distribution / independence of zeros of ζ and c_K: open mathematical problem

The sorry is annotated with these explanations. The conditional bridge theorems (`dpac_of_logPrimePhaseAvoidance`, `dpac_of_externalZetaZeroPhaseAvoidance`, `dpac_of_certifiedZetaZeroSample`) are all fully proved and reduce DPAC to explicit phase-avoidance or interval-arithmetic inputs.

## Project structure

- `RequestProject/DPAC.lean` — main expanded formalization (1 sorry remaining: the research-open conjecture)
- `RequestProject/DirichletPolynomialAvoidance.lean` — original upstream skeleton (fixed import from `Mathlib.NumberTheory.ZetaFunction` → `Mathlib.NumberTheory.LSeries.RiemannZeta`, and `∑ k in` → `∑ k ∈`)
- `RequestProject/Attrs.lean` — stub attributes for `@[category]` and `@[AMS]`

Both files compile successfully under Lean 4.28.0 / Mathlib v4.28.0.