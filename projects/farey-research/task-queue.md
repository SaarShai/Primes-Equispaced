---
schema_version: 2
title: Farey Fresh Task Queue
type: project
domain: project
tier: working
confidence: 0.8
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - raw/farey-archive/handoff/complete_farey_handoff.md.txt
  - raw/farey-archive/state-docs/VERIFICATION_QUEUE.md.txt
  - raw/farey-archive/state-docs/DEFERRED_TASKS.txt
  - projects/farey-research/compute-agents.md
supersedes: []
superseded-by: 
tags: [farey, tasks, queue, priorities]
---

# Farey Fresh Task Queue

No old routine was imported. This is the seed queue for designing new work.

## P0

1. Draft Koyama V4 correction: W2 prime, raw Sym2 falsification, Delta anchor, precise Dominance-of-minus-one questions, and no rank-only overclaim.
2. Validate W2 prime with actual computations: leave-one-out diagnostics, rank-0 high-conductor labels, fixed/narrow-conductor contrasts, and 37b/37a sanity checks.
3. Run verification gate on C1 normalization: denominator, bad primes, coefficient convention, smoothing kernel.
4. Refill compute queues from this page, not from old `NEXT_TASKS` files.
5. Publish the current checkpoint through `farey-publisher` once the bundle is clean.
6. When a fresh Koyama reply + Saar reply pair arrives, spawn a `gpt-5.4-mini` record-updater subagent first, then apply the lean record refresh before any broader research work.
7. Active approved campaign: [[projects/farey-research/active-agent-queue]].

## P1

1. W2 prime mechanism: turn the conductor-bias and Samba mechanism notes into a precise Sym2/Rankin-Selberg derivation attempt.
2. Delta proof strategy: test or prove `E[C1^2(Delta,rho)] -> 1`; avoid overclaiming.
3. Deligne-completed Sym2 correction: blocked until a concrete formula improves on the failed simple Gamma/Deligne normalization checks.
4. Dominance of -1: wait for exact definition from Koyama, then design AP prime-counting tool.

## P2

1. Pair correlation off-central zeros for modular L-functions: rebuild from primary sources and a small verified script; do not cite the recent broad survey directly.
2. Paper C arithmetic surrogate: reformulate away from the likely false `K log K`-type theorem; explore density/proportion/mollifier statements instead.
3. Rework paper drafts only after claim ledger is clean; do not use `PAPER_C_INTRODUCTION_DRAFT.md.txt` as claim-bearing prose.

## Publish Trigger

If a bundle changes the claim ledger, current state, Koyama correspondence, or active task queue, route it through the publish helper instead of leaving it uncommitted.

## Verification Queue

Imported risk checks:

- normalization completeness
- denominator formula
- finite-`K` correction
- sample semantics
- EC bug multiply sourced
- self-calibration artifact
- local factor ambiguity
- smoothing-kernel match
- window/count mismatch
- publication hierarchy

Use [[projects/farey-research/compute-agents]] to route work by cost and capability.
