---
schema_version: 1
title: "Koyama moonshot synthesis"
date: 2026-05-11
type: moonshot-synthesis
tier: claim-safe
scope: "GL(1) Perron, EC-NDC, Path B rank/conductor, DPAC phase bridge"
sources:
  - handoff-2026-05-09-followup/KOYAMA_NEXT_SPRINT_SYNTHESIS_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.csv
  - koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md
  - formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md
tags: [koyama, moonshot, synthesis, claim-safe, gl1, ec, path-b, dpac]
---

# Koyama moonshot synthesis

## Executive decision

No theorem was promoted.

The moonshot produced four useful updates:

1. GL(1): the Perron blocker is sharper. Target-zero simplicity is not enough;
   off-target multiple zeros can create additional oscillatory `log K`-scale
   residues. The exact missing theorem is now the shifted nonlocal remainder
   theorem for `K^w/(w L(rho+w,chi))`.
2. EC-NDC: the base sweep is no longer blocked at `K=100000`. It was extended
   through `K=1000000`; all tested principled normalizations still fail.
3. Path B: the current rank signal fails conductor-controlled acceptance gates
   on local data. B1/B2 conductor controls remain an external GP/PARI run, not
   a rank-survival claim.
4. DPAC: fixed-`K,beta` bad gamma sets are expected to be null by the finite
   exponential-polynomial argument once the non-identity lemma is supplied.
   This is a claim-safe analytic proof sketch, but it is not Lean-verified and
   does not imply avoidance at zeta-zero ordinates.

## Status table

| Lane | Status | Claim-safe result | Promotion decision |
|---|---|---|---|
| GL(1) Perron-leading | `DEFER` | Local residue is closed; off-target residue aggregate is the hard blocker. Multiple off-target zeros would contribute `log K`-scale terms. | Do not state `c_K = log K/L' + o(log K)` as proved. |
| EC-NDC normalization | `NUMERICAL` | Complete sharp-cutoff sweep through `K=1000000`; `D_zeta2/L2E_partial^rank`, raw `D_zeta2`, `D_mix_good`, and `D_2_good` all fail promotion. | No EC normalization promoted. |
| Path B rank/conductor | `DEFER` | Local row-bootstrap diagnostics fail after adding centered `log N`; `gp`/`pari-elldata` absent locally. | No rank-survival sentence before B1/B2 controls. |
| DPAC phase bridge | `CONDITIONAL` / `DEFER` | Almost-everywhere gamma avoidance is safe; zeta-zero ordinate avoidance remains external. | Deprecate `dpac_of_LI`; use explicit phase hypotheses. |

## GL(1) Perron-leading

The moonshot did not close

```text
c_K(chi,rho) = log K/L'(rho,chi) + o(log K).
```

It sharpened the no-go boundary. The local residue at `w=0` is still proved:

```text
Res_{w=0} K^w/(w L(rho+w,chi))
  = log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2).
```

The missing term is the nonlocal shifted Perron remainder. A direct rectangle
and an Inoue/Soundararajan transfer both leave the same off-target residue
aggregate. If an off-target zero has multiplicity `m >= 2`, its residue can
include

```text
K^(lambda-rho) (log K)^(m-1) / ((m-1)! (lambda-rho) a_m),
```

so DRH/EDRH plus "the target zero is simple" is not a closed dependency
package. A sufficient theorem must either control all higher-order residues or
separately assume simple off-target zeros and prove cancellation of the simple
off-target aggregate.

## EC-NDC extended sweep

The EC lane extended the base sweep through `K=1000000` using a complete
good-prime table through prime `999983`.

Promotion rule:

```text
cross-curve ratio < 1.42083
and
max within-curve CV < 0.08567129
```

Final `K=1000000` metrics:

| normalization | max within-K CV | cross-curve ratio | promoted |
|---|---:|---:|---:|
| `D_zeta2_over_L2E_rank` | `0.09669211205` | `1.423821385` | false |
| `D_zeta2` | `0.09670092958` | `5.853565279` | false |
| `D_2_good` | `0.09601279473` | `10.64951807` | false |
| `D_mix_good` | `0.09601227645` | `11.04841098` | false |

At `K=1000000`:

| curve | `D*zeta2` | `D*zeta2/L2E_partial^rank` | `D_mix_good` | `D_2_good` |
|---|---:|---:|---:|---:|
| `37a1` | `0.64436487481` | `1.68869590178` | `0.295574402072` | `0.347071221404` |
| `11a1` | `1.10536976744` | `1.10536976744` | `0.789991412357` | `0.953983875518` |
| `389a1` | `0.196892734571` | `1.51845034256` | `0.0745156770652` | `0.0933570189209` |

Decision: the finite good-prime `L2E_partial^rank` proxy remains the best
numerical proxy, but it now misses both the ratio and within-curve stability
thresholds at `K=1000000`. The mixed residual candidates are decisively worse
cross-curve. No promoted bad-prime-adjusted variant was derived.

## Path B rank/conductor

Local Path B status is negative for rank isolation and incomplete for external
controls.

The stored data have strong rank/conductor lock:

```text
corr(rank, logN) = 0.9721071164173819
```

Bootstrap gates on local rows:

| model | rank beta | bootstrap 95% CI | `P(beta <= 0)` | LOO beta range | max leverage | verdict |
|---|---:|---:|---:|---:|---:|---|
| `y ~ 1 + rank` | `0.585860` | `[0.238656, 0.845991]` | `0.00005` | `[0.358825, 0.621127]` | `0.333333` | confounded screen only |
| `y ~ 1 + rank + logNc` | `-0.677256` | `[-1.221404, 0.091164]` | `0.95515` | `[-0.786934, -0.253343]` | `0.533428` | fail |
| `y ~ 1 + rank + logNc + rank:logNc` | `0.001435` | `[-0.687660, 0.737488]` | `0.60730` | `[-0.317877, 0.194992]` | `0.870262` | fail |

Decision: current Path B is either conductor-confounded or undecided pending
external B1/B2 controls. It is not a rank-isolated theorem.

## DPAC phase bridge

The DPAC lane found a positive, safe analytic layer:

```text
C_{K,beta}(gamma)
  = sum_{2 <= n <= K} mu(n) n^(-beta) exp(-i gamma log n)
```

has a bad real gamma set of measure zero unless the associated entire finite
exponential polynomial is identically zero. For the Mobius polynomial with
`K >= 2`, it is not identically zero.

This gives a claim-safe analytic proof sketch for almost-everywhere gamma
avoidance for fixed `K,beta`, assuming the non-identity lemma for the Mobius
polynomial. It is not Lean-verified and does not prove pointwise avoidance for
zeta-zero ordinates. Safe theorem layers are:

```text
dpac_of_logPrimePhaseAvoidance
ae_logPrimePhaseAvoidance_fixed_beta
dpac_of_certifiedZetaZeroSample
dpac_of_externalZetaZeroPhaseAvoidance
```

Decision: deprecate `dpac_of_LI` loudly; do not silently rename it.

## Verification

Coordinator checks run after resuming the failed session:

```bash
python3 -m py_compile \
  handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py \
  handoff-2026-05-09-followup/Koyama_EC_NDC_build_ap_table.py \
  handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual.py \
  koyama-shared/scripts/path_b_20forms.py \
  koyama-shared/scripts/rank4_5_extension.py
```

EC CSV readback:

```text
rows = 21
max K = 1000000
all product_complete = true
max prime = 999983
```

Worker packet recovery:

- Perron packet landed in `Koyama_Perron_moonshot_2026-05-11.md`.
- EC packet landed in the EC worker log and matches the on-disk report.
- Path B packet landed in `PATH_B_MOONSHOT_DECISION_2026-05-11.md`.
- DPAC packet landed in `DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md`.

## Next actions

1. GL(1): prove or cite the shifted Perron nonlocal remainder theorem,
   explicitly handling off-target multiple zeros or excluding them.
2. EC-NDC: stop trying the four tested sharp-cutoff normalizations as
   promotion candidates. Next useful work is a theoretical no-go/obstruction
   for this normalization class, a derived bad-prime finite factor, or a
   different smoothed/complex-zero diagnostic.
3. Path B: run the B1/B2 GP/PARI conductor-control queue externally.
4. DPAC: patch `DPAC_full.lean` with `LogPrimePhaseAvoidance` layers and a
   deprecation tombstone for `dpac_of_LI`.
5. Draft only claim-safe Koyama notes: local Perron residue, corrected
   `B_infty`, AK under stated hypotheses, EC negative evidence, and no
   unqualified `D_K -> e^{-gamma}`.
