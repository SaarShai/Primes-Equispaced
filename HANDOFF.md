---
schema_version: 2
title: "Fresh Farey Current Handoff"
type: handoff
domain: project
tier: working
confidence: 0.9
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - start.md
  - token-economy.yaml
  - projects/farey-research/README.md
  - L2_facts/farey-current-state.md
  - L2_facts/farey-claim-ledger.md
supersedes: []
superseded-by: 
tags: [handoff, farey, repo-local, startup]
---

# Fresh Farey Current Handoff

## Current Contract

This repo is Fresh Farey Research running on the Token Economy framework. Agents start from `start.md`, load `L0_rules.md` and `L1_index.md`, then retrieve Farey facts on demand from the repo-local markdown wiki.

## Keep In Context

- Repo root: `/Users/saar/Fresh Farey gpt5.5`
- Config: `token-economy.yaml`
- Farey entrypoint: [[projects/farey-research/README]]
- Current state: [[L2_facts/farey-current-state]]
- Claim ledger: [[L2_facts/farey-claim-ledger]]
- Koyama: [[projects/farey-research/koyama-correspondence]]
- Compute: [[projects/farey-research/compute-agents]]
- Queue: [[projects/farey-research/task-queue]]
- Archive manifest: `raw/farey-archive/MANIFEST.jsonl`

## Non-Negotiables

- Work inside the repo root containing `token-economy.yaml`.
- Use `./te wiki search`, then `./te wiki timeline <id>`, then `./te wiki fetch <id>`.
- Do not load `raw/farey-archive/` wholesale; it is provenance, not working memory.
- Do not import old cron jobs, scheduled agents, live queue state, credentials, or external wiki settings.
- Use `/pa` or `/btw` for context-light prompts.
- Checkpoint near 20% context.

## Current Farey Priorities

1. Koyama V4 correction with W2 prime framing.
2. W2 prime mechanism.
3. Delta limit proof or weakening.
4. Exact Dominance-of-minus-one definition from Koyama.
5. Verification queue cleanup before paper drafting.

## Commit / Publish Flow

Checkpoint-worthy repo updates are handled by the `farey-publisher` mini subagent.

- Trigger it when a meaningful bundle is ready, a checkpoint is due, or the user asks for repo sync.
- It uses `scripts/farey_publish.sh` to stage only relevant Farey / Token Economy sections.
- It commits locally first and pushes to `origin` when the remote is available.
- Remote target: `https://github.com/SaarShai/Primes-Equispaced.git`.

## Verification Baseline

```bash
./te doctor
./te wiki index
./te wiki lint --strict
./te context status
```
