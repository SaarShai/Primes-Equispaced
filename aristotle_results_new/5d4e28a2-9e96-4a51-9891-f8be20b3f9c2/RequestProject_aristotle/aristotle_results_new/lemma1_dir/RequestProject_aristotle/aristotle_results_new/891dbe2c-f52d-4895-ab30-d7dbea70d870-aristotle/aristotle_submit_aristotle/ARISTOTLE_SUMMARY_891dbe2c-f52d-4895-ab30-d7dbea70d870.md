# Summary of changes
Added two new theorems to `RequestProject/SignTheorem.lean`:

1. **`sign_theorem_density_one`** (sorry'd statement): The density-1 Sign Theorem stating that ΔW(p) < 0 for all primes p ≥ 11 except a set of density zero. This is left as a `sorry` since it requires deep analytic number theory (Franel-Landau criterion + zero density estimates).

2. **`sign_theorem_all_le_113`** (fully proved): The bounded verification theorem showing ΔW(p) < 0 for ALL primes p with 11 ≤ p ≤ 113. This is proved computationally using `native_decide` via a helper lemma `sign_theorem_all_le_113_aux` that checks the property over `Finset.Icc 11 113`. The proof uses only standard axioms (`propext`, `Classical.choice`, `Lean.ofReduceBool`, `Lean.trustCompiler`, `Quot.sound`).

**Implementation notes:** The user's suggested `interval_cases p <;> simp_all <;> native_decide` approach timed out during `lake build` because `interval_cases` generates 103 subgoals and `simp_all` cannot evaluate `Nat.Prime` for composite numbers. Instead, I used a more efficient approach: a single `native_decide` proof over `∀ p ∈ Finset.Icc 11 113, Nat.Prime p → deltaWobble p < 0`, then applied it with the membership proof. The file builds successfully (verified with `lean_build`).