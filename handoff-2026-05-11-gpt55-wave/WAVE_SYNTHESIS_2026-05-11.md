---
schema_version: 1
title: "GPT-5.5 xhigh research wave synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: NO_THEOREM_PROMOTED
confidence: 0.9
sources:
  - handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md
  - handoff-2026-05-11-gpt55-wave/AGENT2_PERRON_CITATION_AUDIT.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_NDC_BEYOND_BAD_PRIMES.md
  - handoff-2026-05-11-gpt55-wave/AGENT4_MERTENS_SMALLK_TAIL.md
  - handoff-2026-05-11-gpt55-wave/AGENT5_BPLUS_CLUSTER_PROGRAM.md
  - handoff-2026-05-11-gpt55-wave/AGENT6_PATH_B_CONTROLS.md
  - handoff-2026-05-11-gpt55-wave/AGENT7_DPAC_FORMAL_BRIDGE.md
  - handoff-2026-05-11-gpt55-wave/AGENT8_THEOREM_B_DELTA_SCOUT.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
tags: [gpt-5.5, xhigh, synthesis, claim-safe]
---

# GPT-5.5 xhigh research wave synthesis

## Executive decision

No theorem was promoted.

The wave produced one promising numerical proof candidate, three useful
rigorous reductions, three no-go/blocker results, and one citation-closed audit.
The EC candidate has now been reproduced from saved code/data, but component
ablations downgrade it from "normalization candidate" to "finite smoothing
mechanism lead."

## Result table

| Slot | Status | Result | Decision |
|---:|---|---|---|
| 1 | `NO_GO` | Target-zero simplicity cannot close shifted Perron-leading; off-target higher-order zeros can contribute log-scale or larger residues. | Keep GL(1) NDC conditional on a real off-target residue theorem. |
| 2 | `AUDIT_ONLY` | AK source supports an `e^gamma` denominator in its stated DRH formula; checked sources do not close shifted Perron or `1/zeta(2)` promotion. | Use only citation-closed negative/correction language in Koyama email. |
| 3 | `PROOF_CANDIDATE` downgraded to `NUMERICAL_LEAD_ONLY` | Saved reproducer confirms Agent 3's all-component smoothstep numbers through `K<=1000000`; `all, alpha=0.75` has ratio `1.347375492996` and max CV `0.063297427334`. But 22 mode/alpha ablations pass the old gate, including `cP_only` and `P_only`, so `L2^rank` is not load-bearing yet. | Treat as a reproducible finite smoothing lead. Next gate: predeclared holdout curves, larger/denser K, and kernel/ablation null tests. |
| 4 | `NO_GO` | Global fixed `K0<=100` negative-tail envelopes are falsified on the log grid through `1e9`; finite `R_10<0` holds densely through `1e6`; `K0=200` is sample-survived only. | Use MERTENS tail work as finite-window mechanism plus `K0=200` test gate. |
| 5 | `RIGOROUS_REDUCTION` | The old B+ sign theorem remains dead; exact next program is dense MR-prime sign clusters split by `B`, `T`, `B0`, and `Spsi`. | Route to Paper B negative/identity program. |
| 6 | `COMPUTE_BLOCKED` | Path B controls are executable but blocked without `gp`, `pari-elldata`, and 12 selected control rows. | Run on external GP/PARI machine before any rank-survival claim. |
| 7 | `RIGOROUS_REDUCTION` | DPAC reduced to explicit phase/certificate/external-input bridges; no unsafe LI bridge. | Dispatch fresh Aristotle build; no DPAC promotion before Lean closure. |
| 8 | `RIGOROUS_REDUCTION` | BCL transfer stays closed for Theorem B-exact unconditional; viable Delta extension is local ramified axis-pole multiplicity. | Add Delta Open 7.2' as theorem target; no Theorem B impact. |

## Main progress

The strongest new lead is still EC-NDC, but its shape changed. Smoothing the
finite coefficient sum and Euler product is reproducibly powerful; the saved
run confirms Agent 3's all-component values exactly on the three-curve grid.
However, ablations show the old gate is not specific to the proposed
`L2E_partial^rank` denominator. Treat this as a concrete smoothing mechanism
lead, not as BSD/`L(E,2)` evidence and not as a theorem.

The Perron side became more closed in the negative direction.  Agent 1 proves
the local obstruction from off-target multiple zeros; Agent 2 confirms that the
current source set does not supply the missing noncentral shifted theorem.
That preserves the Koyama paper posture: corrected constants plus obstruction.

Paper B should now lean into negative structure: the old B+ sign claim is false, and
the meaningful project is sign-cluster classification via the decomposition
`B(p)/2 = B0(p-1) - Spsi(p)`.

## Next actions

1. **EC smoothing holdout.** Use the persisted `AGENT3_ec_smoothed_reproducer.py`
   and full `a_p` cache to test predeclared holdout curves, larger/denser `K`,
   kernel families, and null controls. The current three-curve result is
   reproducible but not promotable.
2. **Koyama email source pass.** Use Agent 2's wording; do not say AK proves the
   arbitrary noncentral Dirichlet statement unless that source is retrieved.
3. **MERTENS `K0=200` gate.** Dense scan beyond `1e6` or targeted windows from
   the `1e9` log-grid positives.
4. **B+ cluster rows.** Implement the tier-1 dense MR-prime row/cluster TSVs.
5. **DPAC Aristotle dispatch.** Fresh project using the current patched
   `DPAC_full.lean`; reject any output that revives `dpac_of_LI`.
6. **Delta Open 7.2'.** Add the ramified axis-pole multiplicity proposition to
   the Delta paper theorem queue.

## Do not promote unless

- EC smoothing survives a predeclared larger curve sample, larger/denser `K`,
  kernel/null controls, and a load-bearing ablation test.
- GL(1) Perron-leading gets an actual off-target residue theorem.
- DPAC has Lean/Lake build success and `#print axioms` without `sorryAx` for
  any promoted lemma.
- Path B has the external B1/B2 control rows and passes all gates.
- BCL is never used as an unconditional Theorem B-exact transfer.
