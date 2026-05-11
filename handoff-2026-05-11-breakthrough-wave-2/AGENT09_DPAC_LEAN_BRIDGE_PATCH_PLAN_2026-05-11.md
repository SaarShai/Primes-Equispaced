---
schema_version: 1
title: "Agent 09 - DPAC Lean Bridge Patch Plan"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 09"
status: RIGOROUS_REDUCTION
confidence: 0.87
scope: "Exact Lean signatures for claim-safe DPAC phase bridges; no Lean edits"
output_owner: "primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT09_DPAC_LEAN_BRIDGE_PATCH_PLAN_2026-05-11.md"
sources:
  - start.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT09_DPAC_PHASE_BRIDGE_FORMALIZATION_2026-05-11.md
  - primes-equispaced/formal-conjectures/DPAC_full.lean
  - primes-equispaced/formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md
  - primes-equispaced/formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md
tags: [breakthrough-wave-2, dpac, lean, phase-bridge, claim-safe]
---

# Agent 09 - DPAC Lean Bridge Patch Plan

status: `RIGOROUS_REDUCTION`

## Verdict

No theorem is promoted.

Do not resurrect `dpac_of_LI`.  The Lean patch should expose only:

1. positive-real complex-power normalization;
2. DPAC from the exact finite phase nonvanishing at the same `K, rho`;
3. optional ambient real-`gamma` finite phase facts that explicitly do not
   imply zeta-zero avoidance.

Koyama correspondence/email drafts: not read, not edited.

## Current Lean Surface

Current `primes-equispaced/formal-conjectures/DPAC_full.lean` already has:

```lean
def moebiusDirichletPoly (K : ℕ) (s : ℂ) : ℂ
def LinearIndependenceHypothesis : Prop
def gammaExponentialPoly (K : ℕ) (β γ : ℝ) : ℂ
def badGammaSet (K : ℕ) (β : ℝ) : Set ℝ
def LogPrimePhaseAvoidance (K : ℕ) (ρ : ℂ) : Prop
def FiniteLogPrimePhaseIndependence (K : ℕ) (ρ : ℂ) : Prop
def ExternalZetaZeroPhaseAvoidance : Prop
```

`FiniteLogPrimePhaseIndependence` is currently only:

```lean
def FiniteLogPrimePhaseIndependence (K : ℕ) (ρ : ℂ) : Prop :=
  LogPrimePhaseAvoidance K ρ
```

Treat this as a naming wrapper, not an independence theorem.

Known active `sorry` sites:

```lean
moebiusDirichletPoly_eq_gammaExponentialPoly
dirichlet_polynomial_avoidance_conjecture
```

## Patch Order

### 1. Complex-Power Normalization

Primary theorem signature to prove sorry-free:

```lean
theorem moebiusDirichletPoly_eq_gammaExponentialPoly
    (K : ℕ) (ρ : ℂ) :
    moebiusDirichletPoly K ρ =
      gammaExponentialPoly K ρ.re ρ.im := by
  -- proof obligation: positive-real complex-power convention
  -- ((n : ℂ) ^ (-ρ)) =
  --   (Real.rpow (n : ℝ) (-ρ.re) : ℂ) *
  --   Complex.exp (-(Complex.I) * (ρ.im : ℂ) *
  --     Complex.log ((n : ℝ) : ℂ))
  sorry
```

Recommended helper signature:

```lean
lemma nat_cpow_neg_eq_rpow_mul_exp
    (n : ℕ) (hn : 0 < n) (ρ : ℂ) :
    ((n : ℂ) ^ (-ρ)) =
      ((Real.rpow (n : ℝ) (-ρ.re) : ℝ) : ℂ) *
        Complex.exp (-(Complex.I) * (ρ.im : ℂ) *
          Complex.log ((n : ℝ) : ℂ)) := by
  sorry
```

Expected statement: for each positive natural base, Lean's complex power
matches the explicit fixed-line exponential factor used by
`gammaExponentialPoly`; then sum termwise over `k + 2`.

### 2. Non-Vacuous Raw Phase Bridge

Add this bridge first so downstream users can avoid relying on the
normalization `sorry` while it is being proved:

```lean
theorem dpac_of_gammaExponentialPoly_ne_zero_with_normalization
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hnorm :
      moebiusDirichletPoly K ρ =
        gammaExponentialPoly K ρ.re ρ.im)
    (hphase : gammaExponentialPoly K ρ.re ρ.im ≠ 0) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  rw [hnorm]
  exact hphase
```

Non-vacuous assumption: `hphase` is exactly finite phase nonvanishing at the
same target `K, rho`.  `hK`, `hρ`, and `hρ_nontrivial` preserve the DPAC
interface but are not proof-relevant to this bridge.

### 3. Named Phase Bridge With Explicit Normalization

Preferred theorem name while normalization remains a separate proof obligation:

```lean
theorem dpac_of_logPrimePhaseAvoidance_with_normalization
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hnorm :
      moebiusDirichletPoly K ρ =
        gammaExponentialPoly K ρ.re ρ.im)
    (hphase : LogPrimePhaseAvoidance K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  exact
    dpac_of_gammaExponentialPoly_ne_zero_with_normalization
      K hK ρ hρ hρ_nontrivial hnorm hphase
```

Expected statement: finite log-prime phase avoidance plus explicit
normalization implies DPAC at the same zero.

### 4. Named Phase Bridge After Normalization Closes

Current theorem shape is correct, but proof promotion is blocked until
`moebiusDirichletPoly_eq_gammaExponentialPoly` is sorry-free:

```lean
theorem dpac_of_logPrimePhaseAvoidance
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : LogPrimePhaseAvoidance K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  rw [moebiusDirichletPoly_eq_gammaExponentialPoly K ρ]
  exact hphase
```

Expected statement: claim-safe conditional DPAC.  It proves no zeta-zero phase
theorem.

### 5. Structural Phase Name

Keep only as a wrapper until a real finite prime-torus zero-locus definition
exists:

```lean
theorem dpac_of_finiteLogPrimePhaseIndependence
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : FiniteLogPrimePhaseIndependence K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  exact dpac_of_logPrimePhaseAvoidance K hK ρ hρ hρ_nontrivial hphase
```

Non-vacuous only because the current definition unfolds to
`gammaExponentialPoly K ρ.re ρ.im ≠ 0`.  Do not describe this as LI.

### 6. External All-Zero Phase Bridge

Current global bridge shape is acceptable only with the external theorem
passed as a hypothesis:

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

Do not turn `ExternalZetaZeroPhaseAvoidance` into an `axiom`.

## Ambient Finite Phase Facts

These are useful Lean targets, but they do not imply pointwise DPAC.

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

theorem badGammaSet_measureZero_of_not_identically_zero
    (K : ℕ) (β : ℝ)
    (hnot : ¬ (∀ γ : ℝ, gammaExponentialPoly K β γ = 0)) :
    MeasureTheory.volume (badGammaSet K β) = 0 := by
  sorry

theorem badGammaSet_measureZero_moebius
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    MeasureTheory.volume (badGammaSet K β) = 0 := by
  exact badGammaSet_measureZero_of_not_identically_zero K β
    (gammaExponentialPoly_not_identically_zero K hK β)

theorem ae_logPrimePhaseAvoidance_fixed_beta
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    ∀ᵐ γ ∂MeasureTheory.volume,
      gammaExponentialPoly K β γ ≠ 0 := by
  -- expected from badGammaSet_measureZero_moebius
  sorry
```

Non-vacuous assumption: `hK : 2 ≤ K` guarantees the `n = 2` Mobius term is
present.  Promotion limit: these are ambient real-line statements, not
zeta-zero ordinate statements.

## Certified Finite-Sample Bridge

Existing theorem shape is correct for finite verified ranges:

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

Non-vacuous assumptions: `sample`, `box`, `hcover`, and `havoid` must come
from actual interval/box certificates.  This theorem proves only the finite
height range in `hcover`.

## Forbidden Signatures

Do not add:

```lean
theorem dpac_of_LI
    (hLI : LinearIndependenceHypothesis)
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  sorry
```

Do not add existential wrappers where the witness is just the desired phase
fact:

```lean
theorem dpac_of_exists_phase_witness
    (K : ℕ) (ρ : ℂ)
    (h : ∃ _w : Unit, LogPrimePhaseAvoidance K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  sorry
```

Do not add active `axiom`, `admit`, or `unsafe` declarations.

## Proof Blockers

1. `moebiusDirichletPoly_eq_gammaExponentialPoly`: needs Lean proof of
   positive-real complex power, `Complex.log` on positive real bases, `rpow`,
   exponent splitting, and termwise finite-sum rewriting.
2. `nat_cpow_neg_eq_rpow_mul_exp`: exact Mathlib lemma names for complex
   `cpow`, positive real `log`, and real-to-complex casts must be confirmed in
   the target Lean/Mathlib version.
3. `gammaExponentialPoly_not_identically_zero`: needs uniqueness/nontriviality
   for finite exponential polynomials with distinct frequencies `log n`; the
   `n = 2` Mobius coefficient must be isolated without allowing cancellation.
4. `badGammaSet_discrete_or_identically_zero`: needs analytic zero-set support
   for finite exponential polynomials, or a custom proof via complex
   analytic continuation.
5. `badGammaSet_measureZero_*`: needs countability/local finiteness to
   measure-zero conversion in `ℝ`.
6. Zeta-zero phase theorem remains absent: no theorem sends zeta-zero
   ordinates into the complement of `badGammaSet K ρ.re`.
7. Certified finite sample route needs concrete zero boxes, cover proof,
   interval evaluator, precision protocol, and certificate readback.
8. `density_zero_from_growth_comparison` remains a counting skeleton and does
   not imply pointwise DPAC.

## Verification Notes

Read-only commands run:

```text
./te doctor
sed -n '1,220p' start.md
sed -n '1,220p' primes-equispaced/L1_index.md
sed -n '1,240p' primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
sed -n '1,380p' primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT09_DPAC_PHASE_BRIDGE_FORMALIZATION_2026-05-11.md
sed -n '1,380p' primes-equispaced/formal-conjectures/DPAC_full.lean
sed -n '1,180p' primes-equispaced/formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md
sed -n '1,260p' primes-equispaced/formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md
rg -n "dpac_of_LI|LogPrimePhaseAvoidance|FiniteLogPrimePhaseIndependence|ExternalZetaZeroPhaseAvoidance|moebiusDirichletPoly_eq_gammaExponentialPoly|gammaExponentialPoly|badGammaSet|sorry|axiom|admit|unsafe" primes-equispaced/formal-conjectures/DPAC_full.lean
command -v lean
command -v lake
git status --short
```

Results:

- `./te doctor` returned `"ok": true`.
- `DPAC_full.lean` has no active `theorem dpac_of_LI`; only tombstone/comment
  hits remain.
- `DPAC_full.lean` has no active `axiom`, `admit`, or `unsafe` hits by the
  targeted grep.
- `command -v lean` and `command -v lake` produced no path, so no Lean build
  was run.
- No Lean file edits were made.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT09_DPAC_LEAN_BRIDGE_PATCH_PLAN_2026-05-11.md
```
