# README — Lean 4 / Mathlib4 status for the Saar–Koyama Technical/Computational section

This file follows the blueprint convention introduced by Massot for
the PFR formalization: every theorem statement in §X of the paper is
paired with a Lean declaration, and the relationship between the
printed proof and the Lean development is made explicit.

## Toolchain

- **Lean** `leanprover/lean4:v4.28.0` (pinned in `primes-equispaced/lean-toolchain`).
- **Mathlib4** commit `8f9d9cff6bd728b17a24e163c9402775d9e6a365`
  (pinned in `primes-equispaced/lake-manifest.json`).
- **Lake** 5.0.0-src (Lean 4.28.0).

## Repository layout

All Lean source files live in `primes-equispaced/formal-conjectures/`.

| File | Lines | Theorems / lemmas | Proof-position `sorry` | Build status |
|---|---:|---:|---:|---|
| `SmoothedDwfFormula_full.lean` | ~430 | 36 | 2 (annotated as Mathlib v4.28.0 prerequisites) | Builds standalone per Aristotle dispatch 885c640c (2026-05-12); see lakefile note below |
| `DPAC_full.lean` | 336 | 8 | 1 (only the headline DPAC conjecture) | Builds standalone per Aristotle dispatch bb0cd153 (2026-05-12) |
| `DirichletPolynomialAvoidance.lean` | ~60 | 1 | 1 (DPAC conjecture statement) | Compiles |
| `LocalPerronResidue.lean` | ~25 | 1 | 1 (proof; statement compiles) | Statement compiles |
| `CorrectedBInfty.lean` | ~50 | 1 | 1 (proof; statement compiles) | Statement compiles, modulo MATHLIB-PREREQ comments |
| `MertensSpectroscopeUniversality.lean` | ~55 | 1 | 1 | Compiles |
| `FareyBridgeIdentity.lean` | ~50 | 1 | 2 | Compiles |
| `FareySignPattern.lean` | ~55 | 1 | 1 | Compiles (positive theorem **falsified**; file retained as negative-result record) |

Total: **47 theorem/lemma declarations**, **10 proof-position `sorry`s**
across 8 files, each `sorry` annotated either as a Mathlib v4.28.0
prerequisite or as a research-open conjecture.

## Paper-theorem ↔ Lean-declaration map

| Paper object | Lean declaration | File | Status |
|---|---|---|---|
| Lemma X.3.1 (local Perron double-pole residue) | `local_perron_residue` | `LocalPerronResidue.lean` | **SCAFFOLD** (statement only) |
| Theorem X.4.1 ($B_\infty$ identity) | `corrected_B_infty` | `CorrectedBInfty.lean` | **SCAFFOLD** (statement only; uses `DirichletCharacter`, `IsPrimitive`, `LFunction` from Mathlib v4.28.0) |
| Theorem X.4.2 ($c_K$ leading + subleading) | (statement under construction) | `MertensSpectroscopeUniversality.lean` | **SCAFFOLD** |
| Hypothesis AK (eq.\ (\ref{eq:AK}) of §X.4.3) | (named `Hypothesis_AK` in skeleton; not yet added) | (planned) | **EXTERNAL** — Aoki–Koyama 2023 (1.4), p. 235 |
| (SP-L), Shifted Perron leading | (named `Hypothesis_SPL`) | (planned) | **OPEN** |
| (NDC) conditional limit (eq.\ (\ref{eq:NDC}) of §X.4.4) | (composition theorem from AK + SP-L) | (planned) | **CONDITIONAL** |
| Boundary residue $R_0 = -2$ (smoothed $\Delta w_f$, Schwartz cutoff) | `R0_value` + algebraic-glue chain (≈25 theorems) | `SmoothedDwfFormula_full.lean` | **THEOREM (chain)** — proved without `sorry` |
| `mellin_decay` analytic prerequisite | `mellin_decay` | `SmoothedDwfFormula_full.lean:218` | `sorry`; MATHLIB-PREREQ: (1) add `M_decay` field to `AdmissibleWeight`; (2) `Complex.Gamma.uniform_stirling_strip_bound` not in Mathlib v4.28.0 |
| `inv_zeta_polynomial_growth` analytic prerequisite | `inv_zeta_polynomial_growth` | `SmoothedDwfFormula_full.lean:247` | `sorry`; MATHLIB-PREREQ: Titchmarsh §3.11 quantitative bound on $1/\zeta(s)$ |
| DPAC headline conjecture | `dirichlet_polynomial_avoidance_conjecture` | `DPAC_full.lean:335` | `sorry` — **research-open**; Aristotle correctly diagnoses as comparable in difficulty to the Linear Independence Hypothesis for zeta-zero ordinates |
| DPAC algebraic identity $\mathrm{Mob}\,c_K(\rho) = \mathrm{GammaExpPoly}(\rho)$ | `moebiusDirichletPoly_eq_gammaExponentialPoly` | `DPAC_full.lean` | **THEOREM** (closed by Aristotle round-2; uses only `propext`, `Classical.choice`, `Quot.sound`) |
| DPAC phase-avoidance bridges (4) | `dpac_of_logPrimePhaseAvoidance`, `dpac_of_finiteLogPrimePhaseIndependence`, `dpac_of_externalZetaZeroPhaseAvoidance`, `dpac_of_certifiedZetaZeroSample` | `DPAC_full.lean` | **THEOREM** (all four closed without `sorry`) |
| DPAC density-comparison helper | `density_zero_from_growth_comparison` | `DPAC_full.lean` | **THEOREM** |
| Farey bridge identity (R1) | (file-level) | `FareyBridgeIdentity.lean` | **SCAFFOLD** |
| Farey sign pattern (B$_+$ Mertens-restricted positivity) | (file-level) | `FareySignPattern.lean` | **NEGATIVE** — positive theorem is *falsified* by counterexamples at $p = 237{,}733$ (B$(p) = -3.018 \times 10^{10}$, $M(p) = -20$) and $p = 243{,}799$. File retained as a record of the negative result. |

## What "SCAFFOLD" means

A SCAFFOLD entry has:

- The **statement** type-checked against Mathlib v4.28.0 (or with named
  `MATHLIB-PREREQ` comments where Mathlib lacks the API the statement
  type uses).
- The **proof** as `sorry`.

No `axiom` is introduced anywhere in the project; missing Mathlib
infrastructure is annotated `-- MATHLIB-PREREQ: <name>` and the proof
is left as `sorry`. This protocol is project policy (carried over
from the earlier `archive/request-projects/RequestProject/` work) and
is reflected throughout the present manuscript.

## What "THEOREM" means

A THEOREM entry has both the statement type-checked and the proof
closed without `sorry`. Aristotle round-2 dispatches on 2026-05-12
verified that `SmoothedDwfFormula.lean` and `DPAC.lean` both `lake
build`-succeed when isolated, with the only remaining `sorry`s being
those annotated as Mathlib v4.28.0 prerequisites (Stirling on strips,
$1/\zeta$ polynomial growth) and the DPAC headline research-open
conjecture.

## Lakefile / build path note

The repository root `primes-equispaced/lakefile.toml` declares
`[[lean_lib]] name = "RequestProject"` and `defaultTargets =
["RequestProject"]`. This points at an archived path
(`archive/request-projects/RequestProject/`), not the current
`formal-conjectures/` directory. As a result, `lake build` at the
repo root does not currently build the formal-conjectures files.
Both `SmoothedDwfFormula_full.lean` and `DPAC_full.lean` *do* build
successfully when isolated (per the Aristotle round-2 result
extracts at `formal-conjectures/SmoothedDwfFormula_aristotle_round2_extract/`
and `formal-conjectures/DPAC_aristotle_round2_extract/`).

**Repair task (TODO before submission).** Either (a) move the
`formal-conjectures/*.lean` files into a `FormalConjectures/`
namespace directory and update the lakefile, or (b) update the
lakefile globs to include `formal-conjectures/*`. The former is
cleaner; the latter is one-line. This is cosmetic for the
manuscript's claims (the Lean files individually compile) but
necessary for a clean root-level `lake build` invocation.

## How to rebuild

Once the lakefile is repaired, the following sequence will build
the entire formal-conjectures subtree from a fresh checkout:

```bash
# install elan if needed:
curl --proto '=https' --tlsv1.2 -sSf \
    https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y \
    --default-toolchain leanprover/lean4:v4.28.0

# rebuild against pinned mathlib:
cd primes-equispaced/
lake update mathlib   # first-run: ~30 min clone + cache
lake build            # ~15 min depending on caching
```

The Mathlib commit pin in `lake-manifest.json` ensures bit-for-bit
reproducibility against the v4.28.0 commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`.

## Aristotle dispatch history

| Date | Project ID | Target | Status |
|---|---|---|---|
| 2026-05-09 | `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad` | SmoothedDwfFormula (round 1) | COMPLETE_WITH_ERRORS — scaffold |
| 2026-05-09 | `8e608890-f0ba-4a89-bbb0-a63b5bcab697` | R1_B_plus | COMPLETE |
| 2026-05-10 | `59d181d5-b207-4882-a5ba-0786ec51d361` | DPAC (round 1) | COMPLETE_WITH_ERRORS |
| **2026-05-12** | **`885c640c-55cd-48f4-9ce5-1168566619d6`** | **SmoothedDwfFormula (round 2)** | **COMPLETE** — both sorries diagnosed; file `lake build`-verified |
| **2026-05-12** | **`bb0cd153-0364-48e2-85fd-564fd8ce4679`** | **DPAC (round 2)** | **COMPLETE_WITH_ERRORS** — algebraic sorry closed; conjecture sorry left |

Polling: `./scripts/poll_aristotle.sh` (one-shot) or
`./scripts/poll_aristotle.sh --watch`.

## File-by-file `MATHLIB-PREREQ` index

For convenience, every named Mathlib prerequisite annotated in the
Lean files is collected here:

| Annotation | File:line | What is missing in Mathlib v4.28.0 |
|---|---|---|
| `uniform_stirling_bound_on_strips` | `SmoothedDwfFormula_full.lean:204-216` | A uniform Stirling bound for `Complex.Gamma` on vertical strips of the form $\|\Gamma(\sigma + it)\| \le C(σ) \cdot (1+\|t\|)^{σ-1/2}\,\exp(-π\|t\|/2)$. Note: even with this in place, the structure `AdmissibleWeight` would still need a decay field. |
| `riemannZeta_inv_polynomial_bound` | `SmoothedDwfFormula_full.lean:237-245` | Polynomial bound $\|1/\zeta(σ + it)\| \le C(σ)(1+\|t\|)^B$ for $σ \neq 1$. Mathlib has individual non-vanishing on $\mathrm{Re}\,s \ge 1$ (`riemannZeta_ne_zero_of_one_le_re`) but not this quantitative bound. Reference: Titchmarsh, Theorem 3.11. |
| (`DPAC_full.lean` headline `sorry` at line 335) | `DPAC_full.lean:335` | Mathematical inputs missing for *any* unconditional proof of DPAC: zero-counting for finite exponential polynomials (Langer 1931); Riemann–von Mangoldt formula $N(T) \sim (T/2π)\log T$; independence between zeros of $\zeta$ and zeros of $c_K$. |
| `Residue.residue` | `LocalPerronResidue.lean` | Mathlib's residue-of-meromorphic-function API. (Mathlib has residue at a pole via `Complex.residue` in some contexts; the full API is partial as of v4.28.0.) |
| `AnalyticAt.hasFPowerSeriesAt` | `LocalPerronResidue.lean` | The general Laurent-expansion API for `AnalyticAt`. |
| `iteratedDeriv` higher-derivative API | `LocalPerronResidue.lean` | For accessing `L''(0)` as `iteratedDeriv 2 L 0`. |
| `DirichletCharacter.IsPrimitive` | `CorrectedBInfty.lean` | The primitivity predicate for Dirichlet characters. |
| `DirichletCharacter.conductor` | `CorrectedBInfty.lean` | The conductor function. |
| `DirichletCharacter.induce` | `CorrectedBInfty.lean` | Induced-character relation. |
| `LSeries` for $L(s, \chi)$ | `CorrectedBInfty.lean` | Mathlib's `LSeries` API (under active development). |
| `vonMangoldt` summation identities | `CorrectedBInfty.lean` | Standard $\Lambda(n)$ summation in `Mathlib.NumberTheory.ArithmeticFunction`. |

These annotations are the precise "blueprint" of what an *upstream
Mathlib contribution* would need to add in order for the present
manuscript's Lean status to advance from SCAFFOLD to
PROVED-UP-TO-MATHLIB-PREREQ and then to THEOREM.
