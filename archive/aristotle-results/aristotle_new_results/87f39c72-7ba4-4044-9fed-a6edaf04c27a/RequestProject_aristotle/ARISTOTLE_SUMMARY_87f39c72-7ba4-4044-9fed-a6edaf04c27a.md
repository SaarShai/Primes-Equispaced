# Summary of changes
I proved the standalone Cauchy-Schwarz-based bound in `AbstractCauchySchwarz.lean`. The theorem `sum_sq_ge_quarter_of_sum_eq_neg_half` states:

Given a finset `s` of type `ι`, a function `a : ι → ℚ`, the hypothesis that `0 < s.card`, and `∑ i ∈ s, a i = -(s.card : ℚ) / 2`, then `∑ i ∈ s, (a i) ^ 2 ≥ (s.card : ℚ) / 4`.

The proof uses Mathlib's `sq_sum_le_card_mul_sum_sq` (the Cauchy-Schwarz / Chebyshev inequality: `(∑ f)² ≤ |s| · ∑ f²`) and then `nlinarith` to finish the algebraic reasoning — substituting the sum hypothesis and dividing by the cardinality.

I also added a copy of the proved lemma (as `sum_sq_ge_quarter_of_sum_eq_neg_half'`) to `CWBound.lean` as a helper before the main `cw_bound` theorem, so it can be used there directly.

Both files build successfully with no `sorry` and only standard axioms (`propext`, `Classical.choice`, `Quot.sound`).