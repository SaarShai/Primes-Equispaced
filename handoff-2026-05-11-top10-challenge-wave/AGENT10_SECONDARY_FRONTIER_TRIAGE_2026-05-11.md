---
schema_version: 1
title: "Agent 10 - Secondary Frontier Triage"
date: 2026-05-11
agent: "Top-10 Challenge Wave Agent 10"
type: frontier-triage
tier: execution-packet
status: RIGOROUS_REDUCTION
confidence: 0.89
scope: "Compare B+ sign-cluster bridge, DPAC finite phase bridge, and Delta ramified axis-pole registry work"
sources:
  - start.md
  - primes-equispaced/HANDOFF.md
  - primes-equispaced/index.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/L2_facts/farey-claim-ledger.md
  - primes-equispaced/handoff-2026-05-11-top10-challenge-wave/TOP10_CHALLENGE_WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_COMPUTE_SPEC_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT09_DPAC_LEAN_BRIDGE_PATCH_PLAN_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT10_DELTA_THEOREM_B_SENTINEL_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT8_THEOREM_B_DELTA_SCOUT.md
  - primes-equispaced/paper/Delta_machine_paper_theorem_registry.md
  - primes-equispaced/paper/Delta_machine_paper_compositio_draft.md
tags: [top10-challenge-wave, secondary-frontier, b-plus, dpac, delta-machine, theorem-registry]
---

# Agent 10 - Secondary Frontier Triage

Status: `RIGOROUS_REDUCTION`.

No theorem is promoted.  The single highest-leverage secondary task is:

```text
Delta-2.5b registry execution:
promote the local ramified correction divisor / axis-pole multiplicity
proposition into the Delta theorem registry and draft patch queue,
with an explicit no-Theorem-B-impact boundary.
```

This packet is triage plus an execution packet.  It does not edit the Delta
paper, theorem registry, Lean files, or Koyama correspondence/email drafts.

## Decision

Pick Delta.

Reason: it is the only candidate among the three that is simultaneously
theorem-shaped, source-safe without new external theorem claims, low-cost, and
needed to repair stale public-facing paper/registry language.  The local
proposition is finite complex algebra after the ramified correction
polynomials `P_p` are known.  It converts the resolved `zeta x L(s, chi_3)`
axis-pole diagnosis into a durable theorem-registry entry while preserving the
Theorem B no-impact boundary.

Do not mark `THEOREM_PROMOTED` in this packet: the registry/draft patch has not
been applied here, and broad higher-rank Cross-Selberg/global-continuation
claims remain separate conditional material.

## Comparison

| candidate | current state | next action | leverage | reason not picked now |
|---|---|---|---|---|
| B+ sign-cluster bridge | Execution-ready compute spec for dense MR bridge `237733 <= p <= 243799`; expected `468` rows and about `9.94` core-hours. | Implement/run `AGENT08_BPLUS_BRIDGE_COMPUTE.c`, merge rows, certify clusters. | Medium. Produces a finite classification theorem/table, not a proof route. | Already fully specified; compute-only; no source-risk reduction; does not change any theorem registry or external claim boundary. |
| DPAC finite phase bridge | Exact Lean signatures exist for finite phase avoidance and normalization; active proof blockers remain. | Prove `moebiusDirichletPoly_eq_gammaExponentialPoly` and raw phase bridge sorry-free; do not resurrect `dpac_of_LI`. | Low-to-medium. Good formal hygiene, but still conditional and not a zeta-zero phase theorem. | Blocked by Lean proof work plus absent zeta-zero phase input. Current output would still be bridge hygiene, not DPAC progress. |
| Delta ramified axis-pole registry | Local proposition and patch plan exist; paper/registry still contain stale `N=10^6` / slope-mismatch language. | Apply Proposition 2.5b to registry/draft and replace stale Open 7.2 / 10.2 text. | High. Small edit, theorem-shaped, removes stale claims, no new external dependency. | Picked. |

## Selected Task

### Delta-2.5b Registry Execution

Target files for the next worker:

```text
paper/Delta_machine_paper_theorem_registry.md
paper/Delta_machine_paper_compositio_draft.md
```

Required source packet:

```text
handoff-2026-05-11-breakthrough-wave-2/AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md
```

Required theorem guard:

```text
handoff-2026-05-11-breakthrough-wave/AGENT10_DELTA_THEOREM_B_SENTINEL_2026-05-11.md
```

### Proposition To Insert

Use this statement, adapting only notation/style.

```text
Proposition 2.5b (Ramified correction divisor and axis-pole multiplicities).

Let S_ram be a finite set of primes. For each p in S_ram, let

  P_p(z) = c_p prod_alpha (z - alpha)^(m_{p,alpha}),
  P_p(0) != 0.

Set

  E_ram(s) = prod_{p in S_ram} P_p(p^{-s})^{-1}

and let

  I(s) = A(s) M_W(s) E_ram(s),

where A(s) is the remaining global/unramified meromorphic factor and M_W(s)
is the Mellin-transform factor.

For alpha = r exp(i theta), every local solution of p^{-s} = alpha is

  s_{p,alpha,k}
    = -log r / log p - i(theta + 2*pi*k) / log p,
    k in Z.

The local contribution lies on the imaginary axis if and only if |alpha| = 1.
With divisor-order convention ord_{s0}(zero)>0 and ord_{s0}(pole)<0,

  ord_{s0} I
    = ord_{s0}(A M_W)
      - sum_{p,alpha,k: s_{p,alpha,k}=s0} m_{p,alpha}.

Thus the actual pole multiplicity at s0 is max(0, -ord_{s0} I).
Zeros of A(s)M_W(s) may cancel local ramified poles.  In the no-cancellation
case, local root multiplicities and collision multiplicities add.
```

Proof paragraph:

```text
Since P_p(0) != 0, every root alpha is nonzero.  The map s -> p^{-s} has
derivative -log(p)p^{-s}, nonzero at each preimage of alpha.  Therefore a root
of order m of P_p pulls back to a zero of order m of P_p(p^{-s}), hence to a
pole of order m of P_p(p^{-s})^{-1}.  Divisor orders add under products,
including the orders of A(s) and M_W(s).  The axis criterion follows from
Re(s_{p,alpha,k}) = -log|alpha|/log p.
```

### Required Regression

Include the `zeta x L(s, chi_3)` check:

```text
E_ram(s) = (1 - 3^{-2s})^{-1}
P_3(z) = 1 - z^2
alpha = +1, -1
s = i*pi*k/log 3
```

State that this is the local axis-pole lattice used to resolve the old
12-19 percent slope mismatch in Section 5.6.  Do not turn this into a broad
higher-rank global-continuation claim.

## Exact Execution Steps

1. Read:

```text
handoff-2026-05-11-breakthrough-wave-2/AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md
handoff-2026-05-11-breakthrough-wave/AGENT10_DELTA_THEOREM_B_SENTINEL_2026-05-11.md
paper/Delta_machine_paper_theorem_registry.md
paper/Delta_machine_paper_compositio_draft.md
```

2. Apply only the Delta patch-plan edits:

```text
registry:
  - replace stale Proposition 2.5 slope-mismatch comment;
  - insert Proposition 2.5b after Proposition 2.5;
  - replace Open 10.2 with higher-rank ramified correction data;
  - update summary table.

draft:
  - repair Proposition 2.5 mismatch paragraph;
  - insert Proposition 2.5b before the functoriality section;
  - connect Section 5.6 to Proposition 2.5b via P_3(z)=1-z^2;
  - replace stale Open 7.2 with Open 7.2';
  - update section/table/open-problem summaries that still describe the old
    N=10^6 slope-check as open.
```

3. Run stale-language checks:

```bash
rg -n "Open 7\\.2|Open 10\\.2|12% mismatch|19% mismatch|N = 10\\^6|10\\^6|slope mismatch" \
  paper/Delta_machine_paper_theorem_registry.md \
  paper/Delta_machine_paper_compositio_draft.md

rg -n "Proposition 2\\.5b|Ramified correction divisor|axis-pole|P_3\\(z\\)=1-z\\^2" \
  paper/Delta_machine_paper_theorem_registry.md \
  paper/Delta_machine_paper_compositio_draft.md
```

Expected result: no stale `N=10^6` / old mismatch-open language remains except
in explicitly historical sentences that say it is resolved.  `Proposition 2.5b`
appears in the registry, draft theorem body, and summary tables.

4. Acceptance boundary:

```text
PASS only if the patch says Proposition 2.5b is local finite algebra after
P_p is known and explicitly says it does not imply Theorem B, BCL transfer,
support-4 fixed-level density, at-zeros second moments of L', or broad
higher-rank Selberg-class continuation.
```

## Source-Safety Rules

No new external theorem claims are needed for the selected task.  The proof
uses only local finite complex algebra.  Existing external dependencies for
the broader Cross-Selberg proposition remain existing dependencies; do not
upgrade them or cite them as fresh support for Proposition 2.5b.

Do not add:

```text
Theorem B-exact consequence
BCL transfer consequence
support-4 density consequence
unconditional higher-rank plus-tensor continuation
claim that all Cross-Selberg pairs have the needed global continuation
```

Do not edit:

```text
correspondence/
projects/farey-research/koyama-correspondence.md
raw/farey-archive/correspondence/
```

## Wait States

### B+ Wait State

The next B+ task is real but should wait for a compute slot:

```text
Run tier1B_bridge_237733_243799 from
handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_COMPUTE_SPEC_2026-05-11.md.
```

Minimum valid output:

```text
BPLUS_BRIDGE_ROWS_237733_243799.tsv
BPLUS_BRIDGE_CHUNKS_237733_243799.tsv
BPLUS_BRIDGE_CLUSTERS_237733_243799.tsv
BPLUS_BRIDGE_BOUNDARIES_237733_243799.tsv
BPLUS_BRIDGE_SUMMARY_237733_243799.md
BPLUS_BRIDGE_MERGED_MANIFEST_237733_243799.json
```

Allowed claim: certified finite MR-order `B(p)` sign clusters across the
bridge.  Forbidden claim: any revival of B+ positivity or any use of `T(p-1)`
as a sign proxy.

### DPAC Wait State

The next DPAC task is formal hygiene, not a theorem push:

```text
Prove the positive-real complex-power normalization and raw phase bridge
sorry-free in formal-conjectures/DPAC_full.lean.
```

Acceptance conditions:

```text
no active theorem dpac_of_LI
no axiom/admit/unsafe
moebiusDirichletPoly_eq_gammaExponentialPoly closed
dpac_of_logPrimePhaseAvoidance depends only on same-K same-rho finite phase
dirichlet_polynomial_avoidance_conjecture remains research-open unless fully proved
```

Do not describe ambient real-gamma measure-zero phase facts as pointwise DPAC at
zeta zeros.

## Verification Notes

Read-only checks performed for this packet:

```text
HANDOFF.md, index.md, L1_index.md, L2_facts/farey-claim-ledger.md
TOP10_CHALLENGE_WAVE_SYNTHESIS_2026-05-11.md
BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
AGENT08_BPLUS_BRIDGE_COMPUTE_SPEC_2026-05-11.md
AGENT09_DPAC_LEAN_BRIDGE_PATCH_PLAN_2026-05-11.md
AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md
AGENT10_DELTA_THEOREM_B_SENTINEL_2026-05-11.md
AGENT8_THEOREM_B_DELTA_SCOUT.md
targeted rg against Delta registry/draft for stale Open 7.2 / Open 10.2 text
```

Observed:

```text
paper/Delta_machine_paper_theorem_registry.md still has stale Open 10.2
N=10^6 slope-check language.

paper/Delta_machine_paper_compositio_draft.md already has Section 5.6.1
resolved-language, but still has stale Proposition 2.5, Section 7.2,
summary, and red-flag text describing the old slope mismatch as open.

handoff-2026-05-11-breakthrough-wave-2/AGENT10_DELTA_REGISTRY_PATCH_PLAN_2026-05-11.md
already gives exact patch text; this packet promotes that as the single
highest-leverage secondary-frontier task.
```

External theorem source-check:

```text
No new external theorem claim is introduced here.
The selected Delta proposition is local finite algebra.
Inherited external-source claims in older Delta/BCL context are not reused as
new theorem input in this packet.
```

## Changed Files

Created only:

```text
handoff-2026-05-11-top10-challenge-wave/AGENT10_SECONDARY_FRONTIER_TRIAGE_2026-05-11.md
```
