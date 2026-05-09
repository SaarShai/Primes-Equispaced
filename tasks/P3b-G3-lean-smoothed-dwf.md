# P3b / G3 — Aristotle Lean Extension: `SmoothedDwfFormula.lean` Stub → Full Theorem

**Target:** Aristotle (harmonic.fun). API key required — currently **MISSING** on this machine; needs `~/.farey_api_keys` or `ARISTOTLE_API_KEY` env var.
**Repo root context:** `/Users/za/Documents/Farey NOW/primes-equispaced/` (this repo).
**Deliverable:** `formal-conjectures/SmoothedDwfFormula_full.lean` (or extension in place of the bundle's stub) compiling in Mathlib 4.28.0 via `lake build`, with no `sorry`.

---

## Goal (single sentence)

Extend the existing 114-LOC stub at [`handoff-2026-05-04-theorem-B-and-C1/SmoothedDwfFormula.lean`](../handoff-2026-05-04-theorem-B-and-C1/SmoothedDwfFormula.lean) into a fully-proved ~600 LOC Lean 4 theorem in Mathlib 4.28.0 stating the **Smoothed Δw_f explicit formula** with `R₀ = −2`, including the lemmas `R0_eq_neg_two` (already `:= rfl`), `mellin_transform_decay`, `contour_shift_to_critical_line`, and the residue calculus combining them.

If the full theorem cannot be Lean-proved (e.g. Mathlib is missing a prerequisite), report the missing prerequisite with exact statement and the gap analysis.

---

## Context: why this is Aristotle, not Opus

- Lean formalization is the Aristotle (harmonic.fun) agent's primary specialty.
- ~600 LOC is at the upper end of what Aristotle handles autonomously in 4–8 weeks wall-clock.
- The R₀ = −2 anchor is already proven by `rfl` in the stub — the work is the Mellin contour shift and residue calculus extension.
- If Aristotle fails, the fallback is Opus 4.7 extra-high writing the proofs in markdown and a separate Lean-savvy reviewer porting them — but Aristotle should be tried first.

---

## API key requirement

**Before dispatch, confirm:**
- `~/.farey_api_keys` contains `ARISTOTLE_API_KEY=...` line, OR
- `ARISTOTLE_API_KEY` env var is set, OR
- harmonic.fun key is in `~/Documents/Spark Obsidian Beast/Design Claude/wiki/AI-Setup/API Keys & Credentials.md`

User has been notified that all three are currently missing on this machine and is sharing the key.

Once key is wired, dispatch via the Aristotle CLI / API per harmonic.fun documentation. Per [`delta-machine-roadmap.md`](../handoff-2026-05-04-theorem-B-and-C1/delta-machine-roadmap.md): "PRIORITIZE — Lean formalization."

---

## Mandatory protocol (read before starting; embedded in deliverable)

1. **NO `sorry`** — every lemma must be proved or marked `axiom` with explicit justification (e.g., "this is Mathlib's `MellinTransform.zero_of_decay` — pending Mathlib upgrade").
2. **No fabrication** — every Mathlib lemma cited must exist in Mathlib 4.28.0 (`Mathlib.Analysis.MellinTransform`, `Mathlib.NumberTheory.LSeries`, etc.). If a needed lemma is not in Mathlib, state so explicitly and either prove it or downgrade to `axiom`.
3. **Single confidence aggregation rule** — for Lean: `lake build` either compiles or doesn't. Confidence is binary at the build level. State "compiles in Mathlib 4.28.0 commit `<sha>`" or "fails because [...]".
4. **Cross-reference prior Lean attempts**:
   - [`Aristotle_Lean_formalization_REPORT.md`](../handoff-2026-05-04-theorem-B-and-C1/Aristotle_Lean_formalization_REPORT.md)
   - [`Aristotle_Lean_extended_REPORT.md`](../handoff-2026-05-04-theorem-B-and-C1/Aristotle_Lean_extended_REPORT.md)
   - [`T2_Lean_SmoothedDwf_REPORT.md`](../handoff-2026-05-04-theorem-B-and-C1/T2_Lean_SmoothedDwf_REPORT.md) — direct prior on this exact task
   - [`T3_Lean_DeltaMachineMaster_REPORT.md`](../handoff-2026-05-04-theorem-B-and-C1/T3_Lean_DeltaMachineMaster_REPORT.md) — the master theorem Lean status
5. **Don't switch theorem.** Stay on `Smoothed Δw_f explicit formula` exactly:
   ```
   ∑_n W(n/N) · Δw_f(n) = R₀ + ∑_{ρ: ζ(ρ)=0} N^ρ · M_W(ρ) / ζ'(ρ) + E_A(N)
   ```
   where `R₀ = -2`, `E_A(N) = O(N^{-A})` for any `A > 0` (Schwartz decay), `W` is a Schwartz test function, `M_W(s) = (1/2)·Γ(s/2)`.

---

## Inputs and references

### Lean stub to extend

[`handoff-2026-05-04-theorem-B-and-C1/SmoothedDwfFormula.lean`](../handoff-2026-05-04-theorem-B-and-C1/SmoothedDwfFormula.lean) — 114 LOC. Quote it verbatim at top of the deliverable. Contains:
- `R0_value : R0 = -2 := rfl`
- existence axiom for the full formula

### Companion Lean already in the bundle

- [`DeltaMachineMaster.lean`](../handoff-2026-05-04-theorem-B-and-C1/DeltaMachineMaster.lean) — master theorem algebraic backbone
- [`BridgeIdentityStatement.lean`](../handoff-2026-05-04-theorem-B-and-C1/BridgeIdentityStatement.lean) — Bridge identity
- [`CageHalfWidth.lean`](../handoff-2026-05-04-theorem-B-and-C1/CageHalfWidth.lean) — algebra of `√145/(12π)`
- [`CFKRSFactorSixteen.lean`](../handoff-2026-05-04-theorem-B-and-C1/CFKRSFactorSixteen.lean)
- [`CageRescaledAlgebra.lean`](../handoff-2026-05-04-theorem-B-and-C1/CageRescaledAlgebra.lean)
- [`GL2RiemannVonMangoldt.lean`](../handoff-2026-05-04-theorem-B-and-C1/GL2RiemannVonMangoldt.lean)
- [`MertensDecomposition.lean`](../handoff-2026-05-04-theorem-B-and-C1/MertensDecomposition.lean)
- [`MertensRestrictedPosStatement.lean`](../handoff-2026-05-04-theorem-B-and-C1/MertensRestrictedPosStatement.lean)
- [`ReverseEngineerDecomp.lean`](../handoff-2026-05-04-theorem-B-and-C1/ReverseEngineerDecomp.lean)

### Mathematical reference

- [`Smoothed_Dwf_explicit_formula_VERIFIED.md`](../handoff-2026-05-04-theorem-B-and-C1/Smoothed_Dwf_explicit_formula_VERIFIED.md) — clean derivation of `R₀ = -2` via `1/ζ(0) = -2` and `M_W(0)` residue
- [`Smoothed_Dwf_publishable.md`](../handoff-2026-05-04-theorem-B-and-C1/Smoothed_Dwf_publishable.md) — 604-line manuscript section, this is the math you are formalizing
- [`Smoothed_Dwf_numerical.gp`](../handoff-2026-05-04-theorem-B-and-C1/Smoothed_Dwf_numerical.gp), `.out` — 8-digit numerical at N=10⁵, the empirical anchor

### Mathlib 4.28.0 prerequisites (verify each exists)

- `Mathlib.Analysis.MellinTransform` — Mellin transform definitions, decay lemmas
- `Mathlib.NumberTheory.LSeries.Basic` — ζ definition
- `Mathlib.NumberTheory.Mobius` — μ
- `Mathlib.Analysis.Complex.Contour` — contour integrals (if exists; otherwise needs supplementary)
- `Mathlib.Analysis.SchwartzSpace` — Schwartz test functions

---

## Plan (step-by-step)

### Step 1 — read T2 prior report

Open [`T2_Lean_SmoothedDwf_REPORT.md`](../handoff-2026-05-04-theorem-B-and-C1/T2_Lean_SmoothedDwf_REPORT.md). Report:
- What lemmas Aristotle previously attempted
- What succeeded, what failed
- Why a fresh attempt is warranted (e.g., new Mathlib release, different proof strategy)

### Step 2 — establish the namespace and imports

```lean
import Mathlib.Analysis.MellinTransform
import Mathlib.NumberTheory.LSeries.Basic
import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.Mobius
import Mathlib.Analysis.SchwartzSpace
import Mathlib.Analysis.Complex.Contour  -- or supplement

namespace SmoothedDwf
```

### Step 3 — port the existing stub

Copy `SmoothedDwfFormula.lean` (114 LOC) verbatim. Confirm `R0_value : R0 = -2 := rfl` still compiles.

### Step 4 — prove `mellin_transform_decay`

Statement:
```lean
lemma mellin_transform_decay (W : SchwartzMap ℝ ℝ) (s : ℂ) :
  (mellin W s).abs ≤ C(s) * (1 + |s|.re)^{-A}  -- for any A > 0
```
Pull from `Mathlib.Analysis.MellinTransform`; if needed, supplement.

### Step 5 — prove `contour_shift_to_critical_line`

The contour-shift lemma: shift the Mellin contour from `Re(s) > σ_0` (right of the critical line) to `Re(s) = 1/2 - δ` for small `δ > 0`, picking up residues at zeros of `ζ` and at `s = 0`.

Statement (sketch):
```lean
lemma contour_shift_to_critical_line (W : SchwartzMap ℝ ℝ) (N : ℝ) (σ₀ : ℝ) (h : σ₀ > 1) :
  ∫ (s : ℂ) in vertical_line σ₀, N^s · M_W(s) / ζ(s)
    = R₀ + ∑ ρ in zerosOf ζ ∩ critical_strip, N^ρ · M_W(ρ) / ζ'(ρ)
      + ∫ (s : ℂ) in vertical_line (1/2 - δ), N^s · M_W(s) / ζ(s)
```

This is the load-bearing lemma. ~200 LOC. Use Mathlib's `Complex.integral_contour_shift` if exists; otherwise prove it (likely needs `Mathlib.Analysis.Complex.Contour` extension).

### Step 6 — prove `tail_decay`

Statement:
```lean
lemma tail_decay (W : SchwartzMap ℝ ℝ) (N : ℝ) (A : ℝ) (hA : A > 0) :
  |∫ (s : ℂ) in vertical_line (1/2 - δ), N^s · M_W(s) / ζ(s)| ≤ C · N^{-A}
```

This is the Schwartz-decay tail bound. ~100 LOC.

### Step 7 — combine into the main theorem

```lean
theorem SmoothedDwfFormula_full (W : SchwartzMap ℝ ℝ) (N : ℝ) (hN : N ≥ 1) :
  ∑' n, W (n/N) * Δw n = R₀ + ∑' ρ in zerosOf ζ ∩ critical_strip, N^ρ * M_W(ρ) / ζ'(ρ)
    + E_A N
  where E_A N has the Schwartz-decay bound.
```

Combine Steps 4, 5, 6 via Perron's formula (which expresses `Σ W(n/N)·Δw(n)` as the original Mellin contour integral at `Re(s) = σ₀ > 1`).

### Step 8 — verify `lake build` returns 0

Run:
```bash
lake build SmoothedDwfFormula
```

Should succeed with no errors and no `sorry`.

If a Mathlib upgrade is needed, document the missing lemma and the upgrade path. Do NOT use `sorry` to ship.

### Step 9 — sanity check against numerical

The 8-digit numerical match at N=10⁵ from `Smoothed_Dwf_numerical.gp` is the empirical anchor. If the Lean theorem statement (when specialized to W = explicit Schwartz cutoff and N = 10⁵) does not match the numerical to 8+ digits (via `Mathlib.Tactic.NormNum.Decide` or external numerical evaluation), there is a bug somewhere — report it.

### Step 10 — handle the double-pole correction at trivial zeros

Per `Smoothed_Dwf_explicit_formula_VERIFIED.md`: "At `s = -2k`, both `M_W` and `1/ζ` have simple poles → double pole of the integrand. Original `R_triv = ∑ N^{-2k} · G_f(-2k) · M_W(-2k) / ζ'(-2k)` formula was invalid. Corrected formula gives `N^{-2k} · [c_1(k) · log N + c_0(k)]`."

Formalize this correction. Verify numerically at `s = -2` to 18 digits per the prior numerical. The double-pole contribution is `O(N^{-2} · log N)`, comfortably absorbed in the tail `E_A(N)`.

---

## Deliverable specification

### Lean file

`formal-conjectures/SmoothedDwfFormula_full.lean` (or wherever the project is configured to put it; check `lakefile.toml` for the source dir).

Must include:
- All imports listed in Step 2
- Full proofs (no `sorry`)
- Theorem statement matching exactly the math from `Smoothed_Dwf_publishable.md`
- Companion lemmas: `mellin_transform_decay`, `contour_shift_to_critical_line`, `tail_decay`, `double_pole_correction`

### Companion Markdown report

`formal-conjectures/SmoothedDwfFormula_full_REPORT.md` with:

1. **Build status** — `lake build SmoothedDwfFormula_full` output (success or specific error)
2. **Mathlib version** — exact commit used
3. **LOC count** — total LOC, breakdown by lemma
4. **What was new** vs T2 prior report
5. **Any `axiom` declarations** — listed with explicit justification (Mathlib gap, prior result not yet ported, etc.)
6. **Numerical sanity check** — 8-digit match against `Smoothed_Dwf_numerical.gp` at N=10⁵
7. **Known gaps** — anything that fell short, with reproducible failure mode

---

## Done when

- `formal-conjectures/SmoothedDwfFormula_full.lean` exists and `lake build` returns 0
- No `sorry` anywhere
- Companion report exists with all 7 sections
- LOC count ≥ 500 (target ~600 per roadmap; ≥500 acceptable if the proof is tight)
- Numerical sanity check matches `Smoothed_Dwf_numerical.gp` to ≥8 digits
- Any `axiom` declarations are justified

## Stop and report immediately if

- Mathlib 4.28.0 is missing a prerequisite (e.g., contour-integral framework not yet in Mathlib) — report exactly which lemma and propose either a supplement file or downgrade to `axiom`
- The contour shift step requires a residue-calculus framework that doesn't exist in Mathlib — propose either porting from `Mathlib.Analysis.Complex.Contour` or using `IsHomotopic` machinery
- `Δw` definition in any companion `.lean` file disagrees with the math in `Smoothed_Dwf_publishable.md` — flag and stop
- Aristotle returns successive failure traces on the same lemma — escalate to user to consider Opus extra-high markdown drafting + manual port

Do **not** ship a Lean file with `sorry` and call it "complete."
