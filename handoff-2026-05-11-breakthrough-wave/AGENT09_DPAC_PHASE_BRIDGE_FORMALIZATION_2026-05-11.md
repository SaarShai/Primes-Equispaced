---
title: "Agent 09 - DPAC / Phase Bridge Formalization"
date: 2026-05-11
agent: "Agent 09"
status: RIGOROUS_REDUCTION
scope: "Separate finite phase-avoidance facts from zeta-zero ordinate claims"
output_owner: "primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT09_DPAC_PHASE_BRIDGE_FORMALIZATION_2026-05-11.md"
---

# Agent 09 - DPAC / Phase Bridge Formalization

## Verdict

Status: `RIGOROUS_REDUCTION`.

No theorem is promoted here.  The safe DPAC bridge is only:

```text
finite log-prime phase avoidance at the same target zero
  + positive-real complex-power normalization
  -> moebiusDirichletPoly K rho != 0.
```

Finite phase facts over real `gamma` are not zeta-zero ordinate facts.  They
can show that bad ordinates form a thin/null subset of `R` for fixed `K,beta`;
they do not show that the deterministic zeta-zero ordinates avoid that set.

The old `dpac_of_LI` pattern stays dead.  LI among zeta-zero ordinates does
not imply nonvanishing of

```text
sum_{2 <= n <= K} mu(n) n^(-beta) exp(-i gamma log n).
```

## Read Context

- `start.md`
- root `L1_index.md`
- `primes-equispaced/L1_index.md`
- `primes-equispaced/formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md`
- `primes-equispaced/formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md`
- `primes-equispaced/formal-conjectures/DPAC_full.lean`
- adjacent read-only context: old extracted Aristotle DPAC file and Agent 7 formal-bridge packet, used only to identify the deprecated bridge shape.

## Current Lean Surface

Observed in current `DPAC_full.lean`:

```lean
def moebiusDirichletPoly (K : ℕ) (s : ℂ) : ℂ
def LinearIndependenceHypothesis : Prop
def gammaExponentialPoly (K : ℕ) (β γ : ℝ) : ℂ
def badGammaSet (K : ℕ) (β : ℝ) : Set ℝ
def LogPrimePhaseAvoidance (K : ℕ) (ρ : ℂ) : Prop
def FiniteLogPrimePhaseIndependence (K : ℕ) (ρ : ℂ) : Prop
def ExternalZetaZeroPhaseAvoidance : Prop
```

Current `FiniteLogPrimePhaseIndependence` is an alias:

```lean
def FiniteLogPrimePhaseIndependence (K : ℕ) (ρ : ℂ) : Prop :=
  LogPrimePhaseAvoidance K ρ
```

Treat it as a naming wrapper, not an independence theorem.

`dpac_of_LI` is not an active theorem in current `DPAC_full.lean`; it appears
only in the tombstone/comment trail.  The old extracted Aristotle file still
contains the unsafe `dpac_of_LI` scaffold and must not be used as the source
for new dispatches.

## Non-Vacuous Bridge Statements

Use statements whose hypotheses contain the actual finite phase fact, a real
finite certificate, or an explicit external all-zero phase theorem.  Do not
use existential "witness" wrappers that merely package the desired conclusion.

### 1. Normalization Is a Separate Obligation

This theorem is required before the current phase bridge can be promoted:

```lean
theorem moebiusDirichletPoly_eq_gammaExponentialPoly
    (K : ℕ) (ρ : ℂ) :
    moebiusDirichletPoly K ρ =
      gammaExponentialPoly K ρ.re ρ.im := by
  -- positive-real complex-power convention
  sorry
```

Until it is proved sorry-free, the bridge should be dispatched in this
explicit-hypothesis form:

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
  rw [hnorm]
  exact hphase
```

This avoids hiding the normalization proof behind a `sorry`.

### 2. Pointwise Phase Avoidance Bridge

After normalization is closed:

```lean
def LogPrimePhaseAvoidance (K : ℕ) (ρ : ℂ) : Prop :=
  gammaExponentialPoly K ρ.re ρ.im ≠ 0

theorem dpac_of_logPrimePhaseAvoidance
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : LogPrimePhaseAvoidance K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  rw [moebiusDirichletPoly_eq_gammaExponentialPoly K ρ]
  exact hphase
```

This is claim-safe because `hphase` is exactly the finite nonvanishing needed
at the same `K,rho`.  It proves no zeta-zero phase theorem.

### 3. Structural Phase Name

Current safe wrapper:

```lean
theorem dpac_of_finiteLogPrimePhaseIndependence
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : FiniteLogPrimePhaseIndependence K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  exact dpac_of_logPrimePhaseAvoidance K hK ρ hρ hρ_nontrivial hphase
```

Promotion limit: this is not stronger than `LogPrimePhaseAvoidance` until a
real prime-torus zero-locus definition replaces the alias.

### 4. Certified Finite Sample Bridge

This is the right shape for finite computations because the theorem quantifies
over concrete `sample`, `box`, `hcover`, and `havoid` data:

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

This proves only the finite height/sample range supplied by `hcover`.

### 5. External All-Zero Phase Bridge

This is the only global bridge shape that may imply full DPAC, and only with
the external theorem supplied as a hypothesis:

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

## Finite Phase Facts, Not Zeta Claims

These are acceptable future finite/exponential-polynomial statements because
they contain no `riemannZeta` hypothesis and make no claim about zeta-zero
ordinates:

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

theorem badGammaSet_measureZero_moebius
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    MeasureTheory.volume (badGammaSet K β) = 0 := by
  sorry

theorem ae_logPrimePhaseAvoidance_fixed_beta
    (K : ℕ) (hK : 2 ≤ K) (β : ℝ) :
    ∀ᵐ γ ∂MeasureTheory.volume,
      gammaExponentialPoly K β γ ≠ 0 := by
  sorry
```

Promotion limit: even if all four are proved, they establish almost-everywhere
avoidance in ambient `ℝ`, not avoidance at zeta-zero ordinates.

## Forbidden/Vacuous Patterns

Reject theorem shapes like:

```lean
theorem dpac_of_LI
    (hLI : LinearIndependenceHypothesis)
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  sorry
```

Reject existential certificate wrappers that create a witness without carrying
verifiable data:

```lean
-- Bad shape: existential witness is just the desired phase fact.
theorem dpac_of_exists_phase_witness
    (K : ℕ) (ρ : ℂ)
    (h : ∃ _w : Unit, LogPrimePhaseAvoidance K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  sorry
```

Reject any route that:

- promotes ambient measure-zero gamma avoidance to zeta-zero avoidance;
- describes `density_zero_from_growth_comparison` as pointwise DPAC;
- states "LI implies DPAC" without an explicit theorem from zeta ordinates to
  the finite log-prime phase zero locus;
- adds active `axiom`, `admit`, or `unsafe` declarations;
- calls `ExternalZetaZeroPhaseAvoidance` proved when it is only a hypothesis.

## Blocked Assumptions

1. Complex-power normalization:
   `moebiusDirichletPoly_eq_gammaExponentialPoly` still has `sorry` in current
   `DPAC_full.lean`.
2. Fixed-`K,beta` exponential-polynomial layer:
   discreteness/nullity/non-identity lemmas are only reserved/planned, not
   declared and proved in current Lean.
3. Zeta-zero phase theorem:
   no proved theorem sends zeta-zero ordinates into the complement of the
   finite log-prime phase zero locus.
4. Certified finite sample:
   a Lean theorem shape exists, but any concrete claim needs exact sample,
   zero boxes, cover proof, interval evaluator, precision, and readback.
5. Density-one route:
   current comparison skeleton omits formal zeta zero counts, Langer-type
   counts for `c_K`, multiplicity conventions, and the intersection bound.
6. Build verification:
   local `lean` and `lake` were unavailable, so no build or `#print axioms`
   check was run.

## Verification Notes

Read-only checks run:

```text
./te doctor
sed -n '1,220p' start.md
sed -n '1,260p' L1_index.md
sed -n '1,260p' primes-equispaced/L1_index.md
sed -n '1,260p' primes-equispaced/formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md
sed -n '1,260p' primes-equispaced/formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md
sed -n '1,560p' primes-equispaced/formal-conjectures/DPAC_full.lean
rg -n "theorem dpac_of_LI|def dpac_of_LI|DPAC_LI_BRIDGE_DEPRECATED|LogPrimePhaseAvoidance|FiniteLogPrimePhaseIndependence|ExternalZetaZeroPhaseAvoidance|dpac_of_certifiedZetaZeroSample|moebiusDirichletPoly_eq_gammaExponentialPoly|sorry|axiom|admit|unsafe" primes-equispaced/formal-conjectures/DPAC_full.lean
command -v lean
command -v lake
git status --short
```

Results:

- `./te doctor` returned `"ok": true`.
- Current `DPAC_full.lean` has no active `theorem dpac_of_LI` or
  `def dpac_of_LI`; only tombstone/comment hits remain.
- Current `DPAC_full.lean` has known `sorry` sites at
  `moebiusDirichletPoly_eq_gammaExponentialPoly` and
  `dirichlet_polynomial_avoidance_conjecture`.
- `rg` found no active `axiom`, `admit`, or `unsafe` hits in current
  `DPAC_full.lean`.
- `command -v lean` and `command -v lake` returned nonzero.
- No Lean files were edited.

## Changed Files

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT09_DPAC_PHASE_BRIDGE_FORMALIZATION_2026-05-11.md`
