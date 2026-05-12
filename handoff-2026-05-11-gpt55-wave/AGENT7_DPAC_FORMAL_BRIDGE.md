---
title: "Agent 7 - DPAC Formal Bridge"
date: 2026-05-11
agent: "GPT-5.5 xhigh Agent 7"
status: RIGOROUS_REDUCTION
confidence: 0.78
scope: "Lean/Aristotle-ready DPAC phase-avoidance packets; no unsafe LI bridge"
dependencies:
  - "Lean 4.28.0 / Mathlib syntax check on current patched file"
  - "positive-real complex-power expansion for `moebiusDirichletPoly_eq_gammaExponentialPoly`"
  - "certified zeta-zero boxes plus interval nonvanishing for finite-sample claims"
  - "external all-zero finite phase avoidance, if anyone wants full DPAC from the bridge"
---

# Agent 7 - DPAC Formal Bridge

Compile/proof state: local `lean` and `lake` are absent (`command -v` returned nonzero), so nothing below is locally compiled. Current `formal-conjectures/DPAC_full.lean` has active `sorry` at `moebiusDirichletPoly_eq_gammaExponentialPoly` and `dirichlet_polynomial_avoidance_conjecture`. No active `dpac_of_LI` theorem is present; `dpac_of_LI` appears only in the tombstone/comment trail.

No external theorem is used as a proved input in this packet. Names such as Langer/Riemann-von Mangoldt are dependency labels only until primary-source quote/page/equation data are embedded.

## Read Sources

- `HANDOFF.md`
- `handoff-2026-05-09-followup/KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md`
- `formal-conjectures/DPAC_full.lean`
- `formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md`
- `formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md`
- `handoff-2026-05-09-followup/KOYAMA_CLAIM_AUDIT_2026-05-11.md`
- Additional dispatch context: `formal-conjectures/DPAC_HYGIENE_STATUS_2026-05-10.md`, `formal-conjectures/DPAC_dispatch_receipt.md`, `formal-conjectures/DPAC_aristotle_result_extract/.../ARISTOTLE_SUMMARY.md`

## Current Lean Surface

Observed names in `DPAC_full.lean`:

```lean
def moebiusDirichletPoly (K : ℕ) (s : ℂ) : ℂ
def LinearIndependenceHypothesis : Prop
def gammaExponentialPoly (K : ℕ) (β γ : ℝ) : ℂ
def badGammaSet (K : ℕ) (β : ℝ) : Set ℝ
def LogPrimePhaseAvoidance (K : ℕ) (ρ : ℂ) : Prop
def FiniteLogPrimePhaseIndependence (K : ℕ) (ρ : ℂ) : Prop
def ExternalZetaZeroPhaseAvoidance : Prop
```

Compile/proof state: signatures are uncompiled locally. `LinearIndependenceHypothesis` is background only; it must not be a bridge hypothesis.

## Packet A - Complex-Power Normalization

Compile/proof state: declared in `DPAC_full.lean`, uncompiled locally, proof currently `sorry`.

```lean
theorem moebiusDirichletPoly_eq_gammaExponentialPoly
    (K : ℕ) (ρ : ℂ) :
    moebiusDirichletPoly K ρ =
      gammaExponentialPoly K ρ.re ρ.im := by
  -- TODO: positive-real complex-power convention
  sorry
```

Dispatch dependency: prove the positive-base identity for every integer base `n = k + 2 > 0`:

```text
(n : ℂ) ^ (-(β + γ * I)) =
  (Real.rpow (n : ℝ) (-β) : ℂ) * exp (-(I) * (γ : ℂ) * log ((n : ℝ) : ℂ))
```

Do not promote any phase bridge that rewrites `moebiusDirichletPoly` through `gammaExponentialPoly` until this packet is compiled and sorry-free.

## Packet B - Pointwise Phase Bridge

Compile/proof state: declared in `DPAC_full.lean`, uncompiled locally. Proof is only as good as Packet A.

```lean
theorem dpac_of_logPrimePhaseAvoidance
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : LogPrimePhaseAvoidance K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  rw [moebiusDirichletPoly_eq_gammaExponentialPoly K ρ]
  exact hphase

theorem dpac_of_finiteLogPrimePhaseIndependence
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : FiniteLogPrimePhaseIndependence K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  exact dpac_of_logPrimePhaseAvoidance K hK ρ hρ hρ_nontrivial hphase
```

Interpretation: this is a conditional reduction from exact finite log-prime phase avoidance to nonvanishing of the truncated Mobius polynomial at the same zero. It is not an LI theorem and not full DPAC.

## Packet C - External All-Zero Phase Bridge

Compile/proof state: declared in `DPAC_full.lean`, uncompiled locally. This is a bridge from an explicit external input, not a proof of that input.

```lean
def ExternalZetaZeroPhaseAvoidance : Prop :=
  ∀ (K : ℕ) (ρ : ℂ),
    K ≥ 2 →
    riemannZeta ρ = 0 →
    0 < ρ.re ∧ ρ.re < 1 →
    LogPrimePhaseAvoidance K ρ

theorem dpac_of_externalZetaZeroPhaseAvoidance
    (hbridge : ExternalZetaZeroPhaseAvoidance)
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  exact dpac_of_logPrimePhaseAvoidance K hK ρ hρ hρ_nontrivial
    (hbridge K ρ hK hρ hρ_nontrivial)
```

Aristotle should leave `ExternalZetaZeroPhaseAvoidance` as a hypothesis unless it proves a real all-zero phase theorem. Do not turn it into an `axiom`.

## Packet D - Certified Finite Sample Bridge

Compile/proof state: declared in `DPAC_full.lean`, uncompiled locally. Proof is term-level and should be Aristotle-low-risk.

```lean
theorem dpac_of_certifiedZetaZeroSample
    (K : ℕ) (hK : K ≥ 2)
    (T : ℝ) (sample : Finset ℂ)
    (box : ℂ → Set ℂ)
    (hcover :
      ∀ ρ : ℂ,
        riemannZeta ρ = 0 →
        0 < ρ.re ∧ ρ.re < 1 →
        0 < ρ.im ∧ ρ.im ≤ T →
        ∃ z ∈ sample, ρ ∈ box z)
    (havoid :
      ∀ z ∈ sample, ∀ s ∈ box z,
        moebiusDirichletPoly K s ≠ 0) :
    ∀ ρ : ℂ,
      riemannZeta ρ = 0 →
      0 < ρ.re ∧ ρ.re < 1 →
      0 < ρ.im ∧ ρ.im ≤ T →
      moebiusDirichletPoly K ρ ≠ 0 := by
  intro ρ hρ hstrip hheight
  rcases hcover ρ hρ hstrip hheight with ⟨z, hzsample, hρbox⟩
  exact havoid z hzsample ρ hρbox
```

Promotion limit: this certifies only the supplied finite boxes/range. Project context reports `300/300` nonvanishing cases, but this packet did not rerun them; cite only as finite empirical certificate evidence with provenance.

## Packet E - Fixed-`K,beta` Almost-Everywhere Layer

Compile/proof state: statement plan only; not declared in current `DPAC_full.lean`; not Lean-verified. This layer is not a zeta-zero bridge.

```lean
def HasNoFiniteAccumulation (S : Set ℝ) : Prop :=
  ∀ x : ℝ, ∃ ε > 0, (S ∩ Metric.ball x ε).Finite

theorem badGammaSet_discrete_or_identically_zero
    (K : ℕ) (β : ℝ) :
    (∀ γ : ℝ, gammaExponentialPoly K β γ = 0) ∨
    HasNoFiniteAccumulation (badGammaSet K β) := by
  sorry

theorem gammaExponentialPoly_not_identically_zero
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    ¬ (∀ γ : ℝ, gammaExponentialPoly K β γ = 0) := by
  sorry

theorem ae_logPrimePhaseAvoidance_fixed_beta
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    ∀ᵐ γ ∂MeasureTheory.volume, gammaExponentialPoly K β γ ≠ 0 := by
  sorry
```

Dependencies: identity theorem or finite-exponential-polynomial zero discreteness; non-identity of the Mobius exponential polynomial for `K ≥ 2`; local-finite/countable/null bridge on `ℝ`. Even if proved, this says almost every real ordinate avoids the finite zero locus, not that zeta-zero ordinates do.

## Packet F - Density Comparison Skeleton

Compile/proof state: declared in `DPAC_full.lean`, no local build. Older Aristotle summary says the previous version compiled, but the current patched file must be rebuilt before promotion.

```lean
theorem density_zero_from_growth_comparison
    (f : ℕ → ℝ) (g : ℕ → ℝ)
    (C : ℝ) (_hC : 0 < C)
    (hf_bound : ∀ N, f N ≤ C * (N / Real.log N))
    (hg_def : ∀ N, g N = N)
    (hf_nonneg : ∀ N, 0 ≤ f N) :
    Filter.Tendsto (fun N => f N / g N) Filter.atTop (nhds 0)
```

This is pure real-analysis scaffolding. It does not contain Langer, Riemann-von Mangoldt, zero multiplicity conventions, or an intersection bound; those require citation-closed external inputs before any number-theoretic statement.

## Aristotle Dispatch Spec

Use a fresh Aristotle project; do not mutate the existing `59d181d5-b207-4882-a5ba-0786ec51d361` result.

Payload:

```text
lakefile.toml                         # package RequestProject, Mathlib v4.28.0
lean-toolchain                        # leanprover/lean4:v4.28.0
RequestProject/Attrs.lean             # no-op category/AMS tag attrs
RequestProject/DirichletPolynomialAvoidance.lean
DPAC_PHASE_BRIDGE_CONTEXT.md          # this packet plus source list
```

`RequestProject/DirichletPolynomialAvoidance.lean` should be the current patched `formal-conjectures/DPAC_full.lean`, not the older extracted result containing `dpac_of_LI`.

Build target:

```text
lake build RequestProject.DirichletPolynomialAvoidance
```

Aristotle objectives, in order:

1. Repair syntax/import issues only enough to build under Lean 4.28.0.
2. Prove/confirm `dpac_of_certifiedZetaZeroSample` sorry-free and `#print axioms` it.
3. Prove/confirm `density_zero_from_growth_comparison` sorry-free and `#print axioms` it.
4. Close `moebiusDirichletPoly_eq_gammaExponentialPoly`, or isolate the exact Mathlib lemma names blocking it.
5. Once Packet A is closed, confirm the phase bridge packets are sorry-free modulo their explicit hypotheses.
6. Leave `dirichlet_polynomial_avoidance_conjecture` research-open unless a full proof exists with no external phase axiom.

Reject output if it reintroduces `dpac_of_LI`, states LI implies DPAC, adds `axiom`/`admit`/`unsafe`, treats density-one as pointwise DPAC, or promotes almost-everywhere gamma avoidance to zeta-zero avoidance.

Expected acceptable terminal state: `COMPLETE_WITH_ERRORS` is fine if the only remaining errors/sorries are explicitly named open research targets. A true promotion requires build success plus `#print axioms` with no `sorryAx` for the promoted auxiliary lemmas.

## Do Not Promote Unless

- `lake build RequestProject.DirichletPolynomialAvoidance` returns 0 on the current patched file.
- `rg "theorem dpac_of_LI|def dpac_of_LI"` returns no hit; comment-only tombstone hits are acceptable.
- `rg "axiom|admit|unsafe"` has no active proof-surface hits.
- Every promoted auxiliary theorem has `#print axioms` output with no `sorryAx`.
- Any phase bridge promotion includes a closed `moebiusDirichletPoly_eq_gammaExponentialPoly`.
- Any finite-sample claim names the exact sample, box cover, interval arithmetic evaluator, precision, and independent readback provenance.
- Any external theorem claim includes primary-source quote/page/equation embedded in the deliverable.
- Full DPAC is not promoted while `dirichlet_polynomial_avoidance_conjecture` ends in `sorry` or depends on `ExternalZetaZeroPhaseAvoidance` as an unproved assumption.

Verdict: the safe formal bridge is explicit phase/certificate/external-input reduction; the old LI bridge stays dead.
