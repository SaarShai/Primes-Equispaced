---
schema_version: 1
title: "Koyama GPT-5.5 deep gap synthesis"
date: 2026-05-11
type: deep-gap-synthesis
tier: claim-safe
status: NO_THEOREM_PROMOTED
scope: "Five GPT-5.5 xhigh lanes on Koyama hard blockers"
sources:
  - handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_EC_NDC_normalization_no_go_2026-05-11.md
  - koyama-shared/results/PATH_B_CONTROL_RUNNER_2026-05-11.md
  - formal-conjectures/DPAC_PHASE_BRIDGE_PATCH_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_CLAIM_AUDIT_2026-05-11.md
tags: [koyama, gpt-5.5, deep-gap, synthesis, claim-safe]
---

# Koyama GPT-5.5 deep gap synthesis

## Executive decision

No theorem was promoted.

The five GPT-5.5 xhigh lanes produced one concrete no-go result, one useful
formal hygiene patch, one executable unblocker, one citation-backed Perron
obstruction packet, and one adversarial claim audit.

## Result table

| Lane | Status | Result | Decision |
|---|---|---|---|
| GL(1) shifted Perron | `DEFER` | Inoue/Soundararajan-style explicit formulas transfer the off-target residue problem; they do not close it. Off-target multiple zeros remain a dependency blocker. | Do not promote Perron-leading. Missing theorem: `Z_simple(K,T_K)=o(log K)` plus rectangle/truncation bounds, or stronger all-residue control. |
| EC-NDC normalization | `NO-GO` for finite bad-prime factors | Any per-curve finite bad-prime factor leaves within-curve CV invariant. The tested sharp-cutoff class already misses the strict CV gate through `K=1000000`. | Stop pursuing finite bad-prime corrections for the tested sharp-cutoff class. |
| Path B controls | `EXTERNAL_BLOCKED_LOCAL_FAIL` | Added `path_b_control_queue_runner.py` to emit GP packets, ingest controls, and run bootstrap gates. Current data still fail conductor-controlled gates. | Run the runner on a future `gp`/`pari-elldata` machine; no rank-survival claim. |
| DPAC phase bridge | `SCAFFOLD_PATCHED` | `DPAC_full.lean` tombstones `dpac_of_LI` and introduces explicit phase-avoidance bridge names. | Treat as claim-safe scaffold only; no Lean build, no DPAC proof. |
| Claim audit | `NO_P0` | No theorem-promotion failure found; P1/P2 wording risks identified. | Apply wording downgrades before external use. |

## GL(1) Perron

Status: `DEFER`.

The theorem hunt checked primary sources:

- Shota Inoue, JTNB 33 (2021), Theorem 1 `(1.4)`, Theorem 2 `(2.1)`,
  Theorem 3 proof.
- Soundararajan, *Partial sums of the Mobius function*, Theorem 1.

Result: these sources do not imply the exact shifted statement for

```text
F_K(w) = K^w/(w L(rho+w,chi)).
```

They leave the same nonlocal zero residue aggregate. The local double-pole
residue at `w=0` is still `PROVED`, but the global leading theorem requires
one of:

```text
all off-target residues, including higher-order residues, sum to o(log K),
```

or the cleaner sufficient package:

```text
all crossed off-target zeros are simple,
Z_simple(K,T_K)=o(log K),
and the shifted rectangle/truncation terms are o(log K).
```

This is not a counterexample to Dirichlet L-functions. It is a dependency
no-go for the current theorem package.

## EC-NDC

Status: `NO-GO` for finite/bad-prime local-factor corrections in the tested
sharp-cutoff `rho=1` class.

Reason: all bad primes for the three test curves are below the first grid
point `K=1000`, so any finite bad-prime factor is a curve constant over the
whole grid. For any candidate

```text
X_E(K) = base_E(K)/B_E,
```

the within-curve coefficient of variation is unchanged. The strict promotion
rule requires max within-curve CV `< 0.08567129`, while the best tested base
candidate remains:

```text
max within-CV = 0.09601227645.
```

Bad-prime residuals are also numerically too small:

| curve | bad-prime residual |
|---|---:|
| `37a1` | `1.00035884431` |
| `11a1` | `1.00441078791` |
| `389a1` | `1.00000330991` |

Applying the derived residuals still fails:

| candidate | max within-CV | cross-curve ratio |
|---|---:|---:|
| `D_mix_good / R_bad` | `0.09601227645` | `10.9999291948` |
| `D_2_good / C_2_bad` | `0.09601279473` | `10.6056376407` |

Decision: the next EC move is not another finite bad-prime factor. It must be
a different diagnostic: smoothing, complex-zero/Gamma conventions,
conductor/Tamagawa/period theory, or a proof-level no-go for a broader class.

## Path B

Status: `EXTERNAL_BLOCKED_LOCAL_FAIL`.

Added:

```text
koyama-shared/scripts/path_b_control_queue_runner.py
koyama-shared/results/PATH_B_CONTROL_RUNNER_2026-05-11.md
```

The runner:

- checks for `gp` and standard `pari-elldata` paths;
- emits exact GP packets for B1/B2 discovery;
- emits per-curve GP computation packets;
- ingests selected-control CSV rows when present;
- runs NumPy-only bootstrap/LOO/leverage acceptance gates with seed
  `20260510`.

Current local status remains:

```text
gp = absent
pari-elldata = absent
B1 = incomplete
B2 = incomplete
```

Current-data diagnostics reproduce the earlier decision:

| model | rank beta | bootstrap 95% CI | verdict |
|---|---:|---:|---|
| rank only | `0.585860` | `[0.238656, 0.845991]` | confounded screen only |
| rank + logN | `-0.677256` | `[-1.221404, 0.091164]` | fail |
| interaction | `0.001435` | `[-0.687660, 0.737488]` | fail |

Decision: Path B is now operationally unblocked for the next environment, but
mathematically it remains undecided/failing locally.

## DPAC

Status: `SCAFFOLD_PATCHED`, not Lean-verified.

`formal-conjectures/DPAC_full.lean` now tombstones the unsafe LI bridge:

```text
DPAC_LI_BRIDGE_DEPRECATED, 2026-05-11
```

The old theorem declaration `dpac_of_LI` no longer appears as a theorem. Safe
bridge names now exist in the scaffold:

```text
LogPrimePhaseAvoidance
FiniteLogPrimePhaseIndependence
ExternalZetaZeroPhaseAvoidance
dpac_of_logPrimePhaseAvoidance
dpac_of_finiteLogPrimePhaseIndependence
dpac_of_externalZetaZeroPhaseAvoidance
dpac_of_certifiedZetaZeroSample
```

This patch intentionally leaves proof obligations as `sorry`, especially the
complex-power equality between `moebiusDirichletPoly` and the explicit
`gammaExponentialPoly`. Local `lean` and `lake` are absent, so syntax was not
build-verified.

Decision: the file is safer for downstream agents because unsafe LI use should
now fail loudly.

## Audit Actions

The audit found no P0 theorem-promotion failure. It did flag wording risks
that should guide future edits:

- DPAC finite phase should be described as a claim-safe analytic proof sketch,
  not a Lean-verified theorem.
- The old `L2E` rank-power shorthand should be written as the finite
  `L2E_partial^rank` good-prime
  proxy when precision matters.
- Path B local output is a failure-to-promote diagnostic, not a total
  falsification of all possible rank formulations.
- The global misattribution count in `HANDOFF.md` needs reconciliation before
  external use.

## Coordinator Decision

Current top blockers after GPT-5.5:

1. **GL(1)**: prove/cite the shifted residue cancellation theorem
   `Z_simple(K,T_K)=o(log K)` or a stronger all-residue theorem.
2. **EC-NDC**: abandon finite bad-prime corrections for the tested sharp-cutoff
   class; pursue a different diagnostic or broader no-go theorem.
3. **Path B**: run the new runner in a GP/PARI environment and compute B1/B2
   selected controls.
4. **DPAC**: run Lean/Lake elsewhere, repair syntax if needed, then prove the
   scaffolded phase bridge statements or dispatch them to Aristotle.
5. **Claims**: use the audit wording before correspondence or publication.
