TASK: Make `corrected_B_infty` in `formal-conjectures/CorrectedBInfty.lean` of the attached project **unconditional** in Lean 4 / Mathlib v4.28.0, by discharging the `h_convergence` hypothesis.

CURRENT STATE. The theorem is closed CONDITIONALLY on:

```lean
(h_convergence : Filter.Tendsto (T_K chi ρ) Filter.atTop
  (nhds ((1 / 2 : ℂ) * Complex.log (L_value psi (2 * ρ))
         + BPC_1 psi q f ρ
         + BPC_2 chi ρ
         + T_ge3 chi ρ)))
```

This asserts that the partial prime-power tail `T_K(χ, ρ)` converges
to the four-component right-hand side. Given the hypothesis, the
Lean proof is three lines (`Classical.epsilon_spec` +
`tendsto_nhds_unique`).

PAPER-LEVEL DERIVATION. The pen-and-paper proof of this convergence
is in Appendix A of the manuscript (file
`handoff-2026-05-12-paper-prep/recent/APPENDIX_A_BINFTY_PROOF.md`,
attached in the project dir). The four-component identity at the
limit is

  T_∞(χ, ρ) = (1/2) log L(2ρ, ψ) + BPC_1 + BPC_2 + T_{≥3}.

The argument decomposes into:

1. Re-index the partial sum by k first:
   T_K = (1/2) ∑_{p ≤ K} χ²(p)/p^{2ρ}  +  ∑_{k ≥ 3} (1/k) ∑_{p ≤ K} χ(p)^k/p^{kρ}.

2. The k ≥ 3 tail is absolutely convergent (geometric bound at the
   boundary line Re(2ρ) = 1, so |χ(p) p^{-ρ}|^3 ≤ p^{-3/2}, prime
   zeta function dominates). Lean-elementary.

3. The k = 1 prime sum ∑_p χ²(p)/p^{2ρ} on Re(s) = 1 is only
   conditionally convergent. Its limit Σ_2(χ, ρ) is supplied by
   **Akatsuka 2013, Acta Arith. 160(2), Lemma 2.1 / eq. (2.5)**:

      ∑_{p ≤ X} 1/p^{1+2it_0} = c(t_0) + O((log X)^{-1})  for t_0 ≠ 0,

   derived by partial summation against PNT with explicit error
   term. Mathlib v4.28.0 has `Nat.PrimeNumberTheorem` (qualitative).

4. The boundary identity Σ_2 = log L(2ρ, χ²) - BPC_2 is obtained by
   continuity from the log-Euler-product expansion at Re(s) > 1.

5. The imprimitive-induction Euler-factor identity
   L(s, χ²) = L(s, ψ) ∏_{p|q, p∤f} (1 − ψ(p)/p^s)
   then converts log L(2ρ, χ²) into (1/2) · 2 · log L(2ρ, ψ) plus
   the BPC_1 sum. Half of Σ_2 gives (1/2) log L(2ρ, ψ) + BPC_1.

6. Assembly yields T_∞ = (1/2) log L(2ρ, ψ) + BPC_1 + BPC_2 + T_{≥3}.

WHAT WE WANT.

(A) IDEAL — derive `h_convergence` from genuine Mathlib inputs +
    Akatsuka 2013 eq. (2.5) (or a sufficient substitute). Most
    likely path: formalize a weaker form of Akatsuka's partial-
    summation bound, even just under explicit assumptions like
    PNT-with-explicit-error.

(B) SECOND BEST — split `h_convergence` into its four canonical
    inputs as separate hypotheses and prove each independently
    where Mathlib supports it, leaving only the truly missing
    pieces as named conditional hypotheses. This is a structural
    refinement that exposes the analytic gap more precisely.

(C) THIRD BEST — write the precise Lean blueprint for (A) /
    document which Mathlib lemmas are needed and the level of
    formalisation effort each would require.

CONSTRAINTS:
- No new `sorry`s. No new `axiom` declarations.
- Standard axioms only: `propext`, `Classical.choice`, `Quot.sound`.
- Toolchain pinned at `leanprover/lean4:v4.28.0` + Mathlib commit
  `8f9d9cff6bd728b17a24e163c9402775d9e6a365`.
- Don't break the 10-file FormalConjectures roll-up.
- Preserve `corrected_B_infty` (the existing conditional theorem) as
  a companion if the unconditional version replaces it.

CONTEXT FOR REALISM. This is harder than round-6 (which closed the
conditional version) and harder than round-7 (which formalised a
classical identity). Akatsuka 2013 eq. (2.5) is genuinely analytic
NT — partial summation against PNT-with-explicit-error. Mathlib has
the qualitative PNT but not the explicit-error version. The
realistic outcome is (B) — splitting the single fat hypothesis into
named structural pieces — with (A) reserved for whichever pieces
Mathlib can actually supply.

This is a research-grade Lean target.
