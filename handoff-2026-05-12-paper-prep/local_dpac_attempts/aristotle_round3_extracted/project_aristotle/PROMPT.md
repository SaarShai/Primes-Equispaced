# Aristotle dispatch: 5 Lean files, attempt honest sorry-closure

Project context: the joint Saar-Koyama paper's `formal-conjectures/`
directory has 8 Lean files. Aristotle round-2 already handled
SmoothedDwfFormula_full.lean (2 sorries diagnosed as unclosable in
Mathlib v4.28.0) and DPAC_full.lean (1 sorry closed, 1 left as the
research-open conjecture itself). The DirichletPolynomialAvoidance.lean
statement is also research-open.

This dispatch covers the remaining 5 files. For each, please attempt
to close the sorry by giving the actual mathematical statement (not
`True`) using Mathlib v4.28.0's available API where possible, and:

- If a real statement type-checks and is provable: close the sorry.
- If a real statement type-checks but the proof is research-open:
  leave `sorry` with `-- RESEARCH-OPEN: <one-line rationale>` comment.
- If the statement requires Mathlib API not present at v4.28.0:
  leave the statement as a `True := by sorry` placeholder BUT add a
  `-- MATHLIB-PREREQ: <named missing API>` comment listing exactly
  which Mathlib API is needed.
- DO NOT introduce `axiom`.
- DO NOT fake-close by trivializing the theorem type to `True` if
  the actual content is non-trivial.

## File 1: FareyBridgeIdentity.lean

Current statement: `theorem farey_bridge_identity : True := by sorry`.
Docstring says: "For prime p ≥ 2, Σ_{(a,b) ∈ F_{p-1}} exp(2πi p a/b) = M(p) + 2."

The Farey sequence F_n is the set of irreducible fractions a/b ∈ [0,1]
with b ≤ n. The Mertens function M(p) = Σ_{k=1}^p μ(k).

If Mathlib v4.28.0 has `ArithmeticFunction.moebius` (it does) and
supports finite-set sums over rationals, attempt to define the
Farey-set sum and state the identity. If Mathlib does not have a
Farey-sequence definition, define it locally as a `Finset (ℕ × ℕ)`
with the coprimality condition.

## File 2: MertensSpectroscopeUniversality.lean

Current statement is `True := by sorry`. Docstring says: "Under GRH,
any prime subset P with Σ 1/p divergent detects all nontrivial zeta
zeros via the Mertens spectroscope."

Convert to a real statement that says: under a hypothesis
`hGRH : ∀ ρ, riemannZeta ρ = 0 → ρ.re = 1/2 ∨ ρ.im = 0`,
and assuming Σ_{p∈P} 1/p diverges,
the spectroscope F_P(γ) is unbounded as N→∞ at γ = Im ρ.

If the divergence statement is too hard to formalize, keep the
type but make sure it's at least non-vacuous. The proof can be
research-open `sorry`.

## File 3: FareySignPattern.lean

**Important**: the *pointwise* version of this theorem is
FALSIFIED by counterexamples at p = 237,733 (with M(p) = -20,
ΔW(p) > 0 — wrong sign) and p = 243,799. So the file's
"positive" theorem must be RETRACTED.

The remaining plausible version is the *density-one* version:
"the proportion of primes p ≤ X with M(p) ≤ -3 satisfying
sgn(ΔW(p)) = sgn(-M(p)) tends to 1 as X → ∞."

Please:
1. Rename the theorem to make the density-one nature explicit.
2. Add a Lean `theorem` recording the falsification of the pointwise
   version as a concrete `example : ΔW(237733) > 0 ∧ M(237733) < 0`
   (if you have time / API; otherwise documentation only).
3. Leave the density-one statement as `sorry` with research-open
   comment.

## File 4: LocalPerronResidue.lean

Statement uses `residue` for the meromorphic residue functional, but
Mathlib v4.28.0's `Residue.residue` API is partial. If the statement
won't type-check, downgrade to a statement that uses ONLY the Laurent
coefficient `iteratedDeriv` API, or use a local definition of
"residue at simple zero" as `(iteratedDeriv 0 (fun w => K^w / w / L(w+ρ)))^{-1}` ... no wait,
let me restate.

Concretely, the residue of `K^w / (w · L(w + ρ))` at `w = 0`, given
that `L` has a simple zero at `ρ`, equals
`log K / L'(ρ) - L''(ρ) / (2 · L'(ρ)²)`.

This is a one-page Laurent expansion. Attempt to state and (if
Mathlib API allows) prove it. If not, leave as research-open
`sorry` with MATHLIB-PREREQ annotation.

## File 5: CorrectedBInfty.lean

Statement uses `DirichletCharacter.IsPrimitive`, `LFunction`, etc.
If those compile in Mathlib v4.28.0, attempt the statement. Otherwise
downgrade to a statement using ONLY raw `ArithmeticFunction` /
explicit prime sums.

The mathematical content is the closed-form B_∞ identity
T_∞ = (1/2) log L(2ρ, ψ) + BPC_1 + BPC_2 + T_{≥3}
with the four components defined in the existing scaffold.

Leave proof as `sorry` (research-open at the analytic-continuation
boundary-line step that requires Akatsuka 2013); make sure the
statement is non-vacuous.

## Protocol

- Build each file standalone with `lake build` against Mathlib v4.28.0.
- If a file does not build, fix imports / scaffolding until it does.
- Track which sorries close, which remain, and document each remaining
  one's nature (RESEARCH-OPEN, MATHLIB-PREREQ, or VACUOUS-STATEMENT).
- Return a clear ARISTOTLE_SUMMARY.md with the per-file outcome.
