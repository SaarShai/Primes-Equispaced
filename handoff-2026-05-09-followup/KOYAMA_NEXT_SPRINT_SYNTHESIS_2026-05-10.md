---
schema_version: 1
title: "Koyama next sprint synthesis"
date: 2026-05-10
type: sprint-synthesis
tier: claim-safe
scope: "GL(1) Perron gap, EC residual diagnostics, Path B controls, DPAC hygiene"
sources:
  - handoff-2026-05-09-followup/KOYAMA_RESEARCH_DECISION_MEMO_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_2026-05-10.md
  - koyama-shared/results/PATH_B_CONTROL_QUEUE_2026-05-10.md
  - formal-conjectures/DPAC_NEXT_STEPS_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_GL1_claimsafe_note_outline_2026-05-10.md
tags: [koyama, sprint, synthesis, claim-safe, gl1, ec, dpac, path-b]
---

# Koyama next sprint synthesis

## Executive decision

No theorem was promoted in this sprint.

The biggest win is claim safety. The Perron-leading gap is now sharply
isolated; the EC mixed residual candidate has a concrete script and a negative
truncated diagnostic; Path B has a decision-complete conductor-control queue;
and DPAC has exact safe replacement hypotheses for the unsafe LI bridge.

## Sprint status table

| Workstream | Output | Status | Coordinator decision |
|---|---|---|---|
| GL(1) Perron-leading audit | `Koyama_Perron_leading_gap_audit_2026-05-10.md` | `DEFER` | Do not promote `c_K = log K/L' + o(log K)`. Local residue is `PROVED`; global nonlocal Perron remainder is still missing. |
| EC mixed residual | `Koyama_EC_NDC_mixed_residual.py`, `Koyama_EC_NDC_mixed_residual_2026-05-10.md` | `NUMERICAL` / `DEFER` | No normalization promoted. Both tested truncated diagnostics are much worse than the current best cross-curve ratio `1.42083`. |
| Path B conductor controls | `PATH_B_CONTROL_QUEUE_2026-05-10.md` | `DEFER` | Run B1 and B2 conductor-matched controls before any rank-isolated sentence. Rank-4 remains a candidate-only queue. |
| DPAC hygiene | `DPAC_NEXT_STEPS_2026-05-10.md` | `CONDITIONAL` / `DEFER` | Replace the unsafe LI bridge with explicit finite log-prime phase-avoidance hypotheses or a cited external phase theorem. |
| Claim-safe GL(1) note | `Koyama_GL1_claimsafe_note_outline_2026-05-10.md` | `CONDITIONAL` | Short note can safely state AK under DRH/EDRH, local Perron residue, corrected `B_infty`, and negative EC/simple-constant results. |

## GL(1): Perron-leading gap

Status: `DEFER`.

Agent A found no dependency-closed path from the current notes to

```text
c_K(chi,rho) = log K/L'(rho,chi) + o(log K).
```

What is `PROVED`: the local double-pole residue for

```text
K^w / (w L(w+rho,chi))
```

at `w=0`:

```text
log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2).
```

What remains missing: a shifted Perron nonlocal remainder lemma proving that,
after extracting the `w=0` residue, all other zero residues, shifted contour
pieces, horizontal sides, and truncation tails contribute `o(log K)` for the
exact shifted kernel.

Consequence: the corrected GL(1) NDC limit remains `CONDITIONAL` on AK's
DRH/EDRH Euler-product asymptotic plus the still-deferred Perron-leading
lemma.

## EC residual diagnostic

Status: `NUMERICAL`, with promotion status `DEFER`.

Agent B implemented the requested mixed residual script using the inverse
convention `mu_E(p^2)=p` and avoiding the older `a_p^2-p` normalization.

Coordinator rerun:

```bash
python3 handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual.py --max-k 100000 --write-report handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_2026-05-10.md
python3 handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual.py --max-k 100000 --emit-csv
python3 -m py_compile handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual.py
```

Result:

| normalization | cross-curve ratio | max within-curve CV | promoted |
|---|---:|---:|---:|
| `D_mix_good_truncated` | `11.380239` | `0.16197044` | false |
| `D_2_good_truncated` | `10.973293` | `0.16197044` | false |

The current best benchmark remains cross-curve ratio `1.42083` with better
within-curve stability. Therefore neither residual wins even as a truncated
diagnostic.

Limitation: the available `Koyama_EC_NDC_ap_table.csv` stops at `p=541`, so
the script correctly labels every `K=100000` row as incomplete. The
`K=300000` run was not attempted because the complete `K=100000` product
precondition was not met.

## Path B conductor-control queue

Status: `DEFER`.

Coordinator refit of `PATH_B_20FORMS.csv` using only `csv` and NumPy confirms
the deconfounding problem:

```text
rows = 19 EC rows
corr(rank, logN) = 0.972107
rank-only beta = 0.585860
rank + centered logN rank beta = -0.677256
rank + centered logN + interaction rank beta = 0.001435
```

The next useful run is not more high-rank examples alone. It is a crossed
conductor/rank matrix:

- B1: conductors `350-650`; add at least 3 rank-0 and 3 rank-1 controls
  against existing rank-2 rows.
- B2: conductors `4500-5600`; add at least 2 each of rank 0, 1, and 2
  against `5077a1`.
- B3-B5: rank-4 candidate bands around `19747`, `214850`, and `234446`, with
  rank-0 first and rank-1 next if available.

Acceptance gate: bootstrap `B=20000`, seed `20260510`, row resampling,
empirical 95% CI, `P(beta <= 0) <= 0.025`, every LOO beta positive, and no
accepted model leverage `>= 0.50`.

No local PARI/GP run was possible.

## DPAC hygiene

Status: `CONDITIONAL` / `DEFER`.

Agent D gives three safe replacement forms:

```text
LogPrimePhaseAvoidance(K, rho)
FiniteLogPrimePhaseIndependence(K, rho)
LogPrimePhaseTheorem
```

The exact safe theorem names are:

```text
dpac_of_logPrimePhaseAvoidance
dpac_of_finiteLogPrimePhaseIndependence
dpac_of_logPrimePhaseTheorem
```

Density-one packaging should remain an abstract conditional counting lemma:
fixed `K`, assumed bad-count bound, assumed zeta-count asymptotic, conclusion
that bad coincidences have density zero. This does not prove pointwise DPAC.

No Lean build was attempted; local `lean` and `lake` are unavailable.

## Claim-safe note path

Status: `CONDITIONAL`.

The short-note skeleton is safe if it keeps this hierarchy:

1. Theorem A: Aoki-Koyama constant specialization under DRH/EDRH.
2. Lemma B: local Perron double-pole residue.
3. Theorem C: corrected `B_infty` identity with `psi`, `BPC1`, `BPC2`,
   and `T_{>=3}`.
4. Conditional Corollary D: under Perron-leading, the corrected GL(1) NDC
   limit follows.
5. Remark E: old simple constants and the EC simple universality claim are
   negative results, not promoted theorems.

## Next work queue

1. Prove or cite the shifted Perron nonlocal remainder lemma. This is the only
   path to promoting the GL(1) NDC statement.
2. Extend `Koyama_EC_NDC_ap_table.csv` to the actual requested `K=100000`
   products, then rerun the mixed residual script.
3. On a PARI/GP machine with `pari-elldata`, execute B1 and B2 Path B conductor
   controls before drafting any rank-isolated claim.
4. Patch `DPAC_full.lean` documentation and theorem names around finite
   log-prime phase avoidance before using the formal file in a dispatch brief.
5. Draft the GL(1) note only from the claim-safe skeleton and the decision
   memo; do not silently upgrade conditional statements.

## Coordinator verification

Completed in this sprint:

- EC script compile: pass.
- EC report rerun at `--max-k 100000`: pass.
- EC CSV emit: pass; 15 rows, all incomplete because `p_table_max=541`.
- EC baseline parse: reproduced the existing `D_K*zeta(2)` values at
  `K=100000` for `37a1`, `11a1`, and `389a1`.
- Path B regression refit: pass using stdlib CSV plus NumPy, no pandas,
  statsmodels, or sklearn.

Final repo hygiene checks are recorded in the coordinator closeout response.
