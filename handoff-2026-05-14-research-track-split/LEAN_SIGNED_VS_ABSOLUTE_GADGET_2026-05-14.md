---
schema_version: 2
title: "Research-track Lean note — SignedVsAbsoluteResidueGadget (Aristotle round-9)"
type: per-sorry-note
domain: project
tier: working
status: CLOSED
confidence: 0.75
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/formal-conjectures/SignedVsAbsoluteResidueGadget.lean
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md
supersedes: []
superseded-by:
tags: [lean, research-track, aristotle, halo-route, sorry, round-9]
---

# Per-sorry research-track note — SignedVsAbsoluteResidueGadget

A new module file has been added to `formal-conjectures/`. This note exists per the session-prompt directive: "If the inventory changes, write a fresh per-sorry note in the research-track folder and ping the draft session via a log.md entry." The authoritative draft-track inventory at `handoff-2026-05-12-paper-prep/recent/LEAN_SORRY_STATUS.md` is read-only for this track.

## What was added

| File | Lines | Sorries | Headline |
|---|---|---|---|
| `formal-conjectures/SignedVsAbsoluteResidueGadget.lean` | 110 | 2 | `HaloStructural.absoluteResidueSum_tendsto_atTop` + `HaloStructural.signedResidueSum_tendsto_derivative` |

Lakefile updated to include the new module in both the `FormalConjectures` aggregate and as its own `[[lean_lib]]` target. Aristotle round-9 dispatched.

## Aristotle dispatch

| Field | Value |
|---|---|
| Project ID | `61469dcd-30b5-4f73-a237-efe5316d1679` |
| Label | `SignedVsAbsoluteGadget_round9` |
| Dispatched | 2026-05-14 |
| Project tar | 580K (within 100MB limit, after excluding `.lake/`) |
| Build dependencies | Mathlib v4.28.0 |
| Status | **COMPLETE** (returned ~20 min wall-clock); both sorries closed, 0 axioms beyond standard trust triple |
| File (post-Aristotle) | 128 lines, 0 sorries, 0 axioms; proofs use `div_pos`, `Filter.Tendsto.inv_tendsto_nhdsGT_zero`, `HasDerivAt.tendsto_slope_zero` (standard Mathlib) |

## Why this is not an unconditional-push round

The session-prompt directive forbids re-launching unconditional-push rounds without a fresh angle. Round-9 satisfies the exception:

- **Fresh angle**: this is a brand-new module, not in any prior Aristotle lineage (DPAC, MertensSpectroscope, FareyBridge, SmoothedDwf, CorrectedBInfty, RamanujanSum). It captures a structural insight from today's Stage 0 audit of the halo unconditional plan.
- **Scope**: pure complex analysis (`Complex`, `Filter`, `deriv`, `DifferentiableAt`). No L-function, no zero-counting, no Mathlib analytic-NT machinery.
- **Modular**: the file is self-contained; downstream files do not yet depend on it.
- **Two small sorries**, both with explicit proof strategies provided in the dispatch prompt.

## What the lemmas say (math content)

For complex `f, h : ℂ → ℂ` and the meromorphic function

```
G_δ(z)  =  f(z) / ((z - a)(z - (a + δ)) · h(z)),
```

with simple poles at `a` and `a + δ`:

**Claim 1**: as `δ → 0` with `f a ≠ 0` and `h a ≠ 0`,

```
‖Res_{z=a} G_δ‖ + ‖Res_{z=a+δ} G_δ‖  →  ∞.
```

**Claim 2**: as `δ → 0` with `f, h` differentiable at `a`,

```
Res_{z=a} G_δ + Res_{z=a+δ} G_δ  →  (f / h)'(a)         (bounded limit).
```

The gap between Claim 1 and Claim 2 is the precise structural reason why the halo route bypasses the rooted Palm wall: the absolute-value series sees individual cluster-collapse blow-up, while the signed sum (= divided difference) stays bounded.

## Relation to today's halo work

| Audit | Uses signed-vs-absolute principle |
|---|---|
| `H1_RESIDUE_FIRST_AUDIT_2026-05-14.md` (Stage 0) | Yes — verdict GREEN rests on the signed form `(H-min-r)` being the H1 minimal requirement |
| `HALO_DOOR_B_ARC_UNIFORMITY_AUDIT_2026-05-14.md` | Yes — halo plan §2.2 calls this the "two-zero gadget", cited as motivation |
| `HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §2 | Direct statement of the gadget in analytic prose |

The Lean lemma is the formal capture of the prose argument.

## Acceptance criteria

When Aristotle returns:

1. Both sorries closed without `axiom` declarations.
2. File compiles under Lean 4.28.0 + Mathlib 4.28.0.
3. `_AxiomCheck.lean` updated to include the two new theorems and confirms only `propext`, `Classical.choice`, `Quot.sound` dependencies (i.e., joins the "standard trust triple" set).

## Downstream notes

- The `_AxiomCheck.lean` file (`handoff-2026-05-12-paper-prep/recent/...` track) is the authoritative axiom audit. Adding the round-9 lemma's headlines there is a draft-track action, not a research-track action. **Recommendation**: ping the draft track via `log.md` once round-9 returns and is verified locally.
- The `LEAN_SORRY_STATUS.md` (paper-prep track) is read-only here. The cumulative state would go from "10 files / 8 fully proved / 2 DPAC-headline sorries" to "11 files / 9 fully proved / 2 DPAC-headline sorries" once round-9 returns clean. **Recommendation**: defer the inventory update to the draft track.

## Cost

| Item | Estimate |
|---|---|
| Aristotle dispatch | ~$X (round-9 cost TBD; round-7 RamanujanSum took ~30 min wall-clock and similar cost) |
| Wall-clock time to result | ~1-3 hours (estimate from prior rounds) |

## Boundary

Allowed:

```
A new research-track Lean module has been dispatched to Aristotle.
The dispatch is a fresh-angle module on the halo-residue structural
principle, not an unconditional-push retry.
```

Not allowed:

```
The dispatch has succeeded.
The two sorries are closed.
The halo route is formalized.
The inventory has moved.
```
