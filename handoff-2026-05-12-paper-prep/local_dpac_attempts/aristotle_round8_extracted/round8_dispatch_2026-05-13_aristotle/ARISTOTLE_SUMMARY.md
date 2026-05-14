# Summary of changes for run a25797bf-bbe0-4a56-84d6-49a2c4b2487f
## Outcome: Option (C) — Blueprint with provable infrastructure

The `h_explicit_formula` hypothesis in `mertens_spectroscope_universality` **cannot be discharged** with Mathlib v4.28.0. The hypothesis packages the RH-conditional explicit formula for M(x) and the resonance argument at zeta-zero ordinates — analytic number theory that is entirely absent from Mathlib (no Perron formula, no explicit formula for M(x) or ψ(x), no oscillatory integral estimates for Dirichlet series over primes).

### What was delivered

The file `formal-conjectures/MertensSpectroscopeUniversality.lean` was enhanced with:

1. **Detailed 5-step blueprint** (in the module docstring) tracing the precise chain from Soundararajan 2009 Theorem 1 to `h_explicit_formula`, identifying exactly what Mathlib is missing at each step:
   - Step 1: Explicit formula for M(x) via Perron inversion (Mathlib gap: TOTAL)
   - Step 2: Soundararajan's quantitative bound under RH (Mathlib gap: TOTAL)
   - Step 3: Partial summation for complex-exponential sums (Mathlib gap: PARTIAL — `Finset.sum_by_parts` exists but oscillatory estimates do not)
   - Step 4: Resonance at γ = γ_ρ₀ — the key mathematical step where ∑ p^{-1/2} diverges
   - Step 5: Concrete enumeration of 4 missing Mathlib components (~2000+ lines of new formalization needed)

2. **Two proven infrastructure lemmas** (no sorry, standard axioms only):
   - `spectroscope_nonneg`: F_{P,N}(γ) ≥ 0 for all P, N, γ
   - `reciprocal_sqrt_not_summable`: if ∑_{p∈P} 1/p diverges, then ∑_{p∈P} 1/√p diverges — this is Step 4(c) of the blueprint, the only part of the argument currently formalizable with Mathlib

3. **Enriched obstruction comments** on the `h_explicit_formula` parameter itself, listing the 4 specific missing ingredients.

### Verification

- Zero sorry statements in the file
- All axioms are standard: `propext`, `Classical.choice`, `Quot.sound`
- The 10-file `FormalConjectures` roll-up target builds successfully
- `MertensSpectroscopeUniversality` module builds in ~10s

### Why Options (A) and (B) were not achievable

- **Option (A)** (fully unconditional): Requires formalizing the Perron inversion formula, the explicit formula for M(x), and oscillatory integral estimates — a multi-week project requiring ~2000+ lines of new Mathlib infrastructure.
- **Option (B)** (weaker hypothesis from existing Mathlib PNT): Mathlib's PNT-level result (`riemannZeta_ne_zero_of_one_le_re`) does not provide M(x) = o(x) or any quantitative Mertens bound. Even if it did, deriving spectroscope divergence still requires the explicit formula machinery (Steps 1–3 of the blueprint).