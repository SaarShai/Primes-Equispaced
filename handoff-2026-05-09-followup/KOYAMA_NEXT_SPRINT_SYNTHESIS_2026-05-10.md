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
  - handoff-2026-05-09-followup/Koyama_EC_NDC_build_ap_table.py
  - handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table_100000.csv
  - handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_complete_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_L2E_complete_check_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md
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
| EC mixed residual | `Koyama_EC_NDC_mixed_residual.py`, `Koyama_EC_NDC_mixed_residual_complete_2026-05-11.md` | `NUMERICAL` / `DEFER` | No normalization promoted. Complete good-prime products through `K=100000` still have cross-curve ratios about `11`, far worse than the benchmark `1.42083`. |
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

Initial coordinator rerun used the bundled 100-prime table and was correctly
marked truncated. The 2026-05-11 continuation removed that limitation by
building a complete `a_p` table through `K=100000`. The later 2026-05-11
moonshot then extended the base EC-NDC sweep itself through `K=1000000`.

Complete-data commands:

```bash
python3 handoff-2026-05-09-followup/Koyama_EC_NDC_build_ap_table.py --max-k 100000 --out handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table_100000.csv
python3 handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual.py --max-k 100000 --ap-table handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table_100000.csv --write-report handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_complete_2026-05-11.md
python3 -m py_compile handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual.py
```

Complete `K=100000` result:

| normalization | cross-curve ratio | max within-curve CV | promoted |
|---|---:|---:|---:|
| `D_mix_good` | `11.365809` | `0.084975752` | false |
| `D_2_good` | `10.955575` | `0.084965682` | false |

The current best benchmark remains cross-curve ratio `1.42083`. The complete
good-prime products improve within-curve stability enough to hit the old CV
scale, but cross-curve collapse fails by almost an order of magnitude.

Key `K=100000` values:

| curve | D_mix | D_2 | complete |
|---|---:|---:|---:|
| `37a1` | `0.2834173726` | `0.3327962619` | true |
| `11a1` | `0.8464364855` | `1.022145728` | true |
| `389a1` | `0.0728996818` | `0.09133237325` | true |

Moonshot extended-sweep result through `K=1000000`:

| normalization | cross-curve ratio | max within-curve CV | promoted |
|---|---:|---:|---:|
| `D_zeta2_over_L2E_rank` | `1.423821385` | `0.09669211205` | false |
| `D_zeta2` | `5.853565279` | `0.09670092958` | false |
| `D_2_good` | `10.64951807` | `0.09601279473` | false |
| `D_mix_good` | `11.04841098` | `0.09601227645` | false |

This supersedes the earlier `K=300000` blocker note. The base sweep is now
available through `K=1000000`; no tested sharp-cutoff normalization is
promoted.

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
2. If pursuing EC residuals further, stop treating the four tested sharp-cutoff
   normalizations as promotion candidates. Next useful work is a derived
   bad-prime factor, a no-go theorem for this normalization class, or a
   genuinely different smoothed/complex-zero diagnostic.
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
- EC CSV emit: pass; 15 complete rows after the 2026-05-11 `a_p` table
  extension.
- EC extended sweep: pass; 21 complete rows through `K=1000000`, max prime
  `999983`, all `product_complete=True`.
- EC baseline parse: reproduced the existing `D_K*zeta(2)` values at
  `K=100000` for `37a1`, `11a1`, and `389a1`.
- Path B regression refit: pass using stdlib CSV plus NumPy, no pandas,
  statsmodels, or sklearn.

Final repo hygiene checks are recorded in the coordinator closeout response.
