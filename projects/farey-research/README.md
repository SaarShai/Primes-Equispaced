---
schema_version: 2
title: Fresh Farey Research
type: project
domain: project
tier: semantic
confidence: 0.95
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - raw/farey-archive/handoff/complete_farey_handoff.md.txt
  - raw/farey-archive/state-docs/CLAIM_STATUS.md.txt
  - projects/farey-research/WORKING_MANIFEST.jsonl
supersedes: []
superseded-by: 
tags: [farey, c1, modular-forms, token-economy]
---

# Fresh Farey Research

Fresh local repo for Farey Research using Token Economy retrieval and documentation rules.

## Source Of Truth

- Current state: [[L2_facts/farey-current-state]]
- Claim ledger: [[L2_facts/farey-claim-ledger]]
- C1 spectroscope: [[projects/farey-research/c1-spectroscope]]
- W2 prime model: [[projects/farey-research/w2-prime]]
- Koyama correspondence: [[projects/farey-research/koyama-correspondence]]
- Compute agents: [[projects/farey-research/compute-agents]]
- Task queue: [[projects/farey-research/task-queue]]
- Active agent queue: [[projects/farey-research/active-agent-queue]]
- Recent results review: [[projects/farey-research/recent-results-review]]
- Context rot blacklist: [[L4_archive/farey-context-rot]]

## Repo Layout

- `projects/farey-research/data/`: verified working data copied from curated sources.
- `projects/farey-research/scripts/`: canonical reproduction scripts.
- `projects/farey-research/results/`: curated result narratives.
- `raw/farey-archive/`: full relevant evidence archive; fetch only for provenance.
- `raw/farey-archive/MANIFEST.jsonl`: archive hashes and source paths.

## Current Priorities

1. Correct Koyama follow-up: V3 overclaimed pure-rank/conductor behavior; V4 must use W2 prime framing.
2. Validate W2 prime: leave-one-out diagnostics, rank-0 high-conductor recomputes, fixed/narrow-conductor contrasts.
3. Explain W2 prime: why rank/control points and log-conductor both appear in C1 second moments.
4. Prove or weaken Delta target: `E[C1^2(Delta, rho)] -> 1`.
5. Ask Koyama for the exact "Dominance of -1" definition before computing.
6. Keep importing only verified claims; archive model outputs until reviewed.

## Routing At A Glance

- M1: long proof/writeup work.
- M1B: numerical/PARI scripts and recomputations.
- M2: local Ollama only after daemon check.
- Aristotle: Lean 4 formalization.
- Gemini, Mistral, Cohere, SambaNova, Groq, OpenRouter: external API routing for writeups, proofs, summaries, and quick checks depending on depth and quota.
- `farey-publisher`: repo checkpoint commits and pushes at sensible intervals.

## Publish Cadence

Meaningful checkpoints are published through the `farey-publisher` mini subagent at intervals, not by ad hoc manual pushes.

- Trigger: checkpoint-worthy work, repo-sync request, or review-ready change bundle.
- Handler: `projects/agents-triage/agents/farey-publisher.md`.
- Helper: `scripts/farey_publish.sh` stages only relevant Farey / Token Economy sections and can commit or push to `origin`.
- Target remote: `https://github.com/SaarShai/Primes-Equispaced.git`.
- Scope rule: prefer the smallest relevant section set, never the entire tree.

## Koyama Update Trigger

When Saar pastes a new Koyama reply together with the email Saar sent, spawn a `gpt-5.4-mini` record-updater subagent immediately. Its job is to:

- update `projects/farey-research/koyama-correspondence.md`
- update `people/shin-ya-koyama.md`
- update `L2_facts/farey-claim-ledger.md` if a claim changed
- append the sync note to `log.md`
- refresh `projects/farey-research/task-queue.md` if the next action changed

Keep that update lean: record the new correspondence state, the latest asks, and any claim or task changes, but do not re-import the full email thread.

## Retrieval Rule

Use:

```bash
./te wiki search "<topic>"
./te wiki timeline "<id>"
./te wiki fetch "<id>"
```

Do not load the archive or old wiki wholesale. Promote a raw file only after verification and a concise synthesis page update.
