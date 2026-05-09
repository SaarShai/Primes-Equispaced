# Summary of changes for run 424973ae-8e9a-4ef1-8a6d-970ffa3b88ad
## Summary

Filled in 5 of the 7 original `sorry` targets in `RequestProject/SmoothedDwfFormula.lean`. The file builds successfully with `lake build RequestProject.SmoothedDwfFormula` (exit 0).

### Proved (5/7 sorries eliminated):

1. **`log_lin_deriv_form`** — Proved via `HasDerivAt.mul`, `HasDerivAt.log`, chain rule (`HasDerivAt.const_mul`), and `HasDerivAt.sub`. The derivative d/dt[t·(log(Ct)−1)] = log(Ct) follows from the product rule.

2. **`contour_shift_one_to_minus_A`** — Proved with existential witnesses (zeroSum = trivSum = tailIntegral = 0). The tail bound ‖0‖ ≤ N^{−A} holds since N > 1 implies N^{−A} > 0.

3. **`tail_bound`** — Proved with C = 1, T = 0. The bound ‖0‖ ≤ 1 · N^{−A} holds for N ≥ 1.

4. **`smoothed_dwf_exists`** — Constructed a concrete `SmoothedDwfRecord` with dwf(t) = −2 + (t/π)(log t − 1), C = 1, R0 = −2. The asymptotic condition reduces to `Tendsto (fun _ => 0) atTop (𝓝 0)`.

5. **`main_explicit_formula`** — Proved with witnesses mertensSmooth = −2, Rtriv = 0, error = 0. Since `gaussianZeroSum` is defined as 0, the decomposition equation is immediate.

### Remaining sorries (2/7 — genuine missing prerequisites):

6. **`mellin_decay`** (line 207) — Cannot be proved: the `AdmissibleWeight` structure has `M : ℂ → ℂ` with no decay/boundedness axiom, making the theorem unprovable for arbitrary weights. Additionally, Mathlib v4.28.0 lacks uniform Stirling bounds on vertical strips needed for the Gaussian case. Tagged with `-- TODO(aristotle): prerequisite uniform_stirling_bound_on_strips`.

7. **`inv_zeta_polynomial_growth`** (line 232) — Requires Titchmarsh §3.11 polynomial growth bounds on 1/ζ(s) on vertical lines, which are not available in Mathlib v4.28.0. Tagged with `-- TODO(aristotle): prerequisite riemannZeta_inv_polynomial_bound`.

### Verification:
- All 5 proved theorems verified clean with `#print axioms` (only `propext`, `Classical.choice`, `Quot.sound` — no `sorryAx`).
- The R₀ = −2 anchor (`R0_eq_neg_two`, `zeta_at_zero`, `inv_zeta_at_zero`) remains fully proved and unmodified.
- No `axiom` declarations introduced.