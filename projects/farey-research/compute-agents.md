---
schema_version: 2
title: Farey Compute Agents
type: procedure
domain: project
tier: procedural
confidence: 0.85
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - raw/farey-archive/state-docs/COMPUTE_ROUTING.md.txt
  - raw/farey-archive/state-docs/API_QUOTA_POLICY.md.txt
  - raw/farey-archive/handoff/complete_farey_handoff.md.txt
supersedes: []
superseded-by: 
tags: [farey, compute, agents, queues]
---

# Farey Compute Agents

This page records capabilities and queue formats only. Old cron jobs, hourly routines, scheduled agents, and live queue state were not imported as active machinery.

## Local / LAN Compute

| agent | endpoint | capability | queue format |
|---|---|---|---|
| M1 Ollama | `new@192.168.1.218` | `deepseek-r1:32b`, `qwen3.5:35b`; long proof/writeup tasks | `MODEL|TASK_NAME|PROMPT` |
| M1B Python | `za@192.168.1.64` | CPU Python 3.9 + PARI/mpmath; numerical scripts | `SCRIPT_PATH|TASK_NAME` |
| M2 local | `localhost:11434` | local Ollama; use only after daemon check | `MODEL|TASK_NAME|PROMPT` |

Drain/skip flags live externally in `/Users/saar/Library/FareyState/*.flag`; check them before any new routine design.

Permanent/known-disabled resources:

- M5B: permanently off.
- EXO: skipped until corrupt model/download issue is intentionally repaired.
- M2: verify `curl -s http://localhost:11434/api/tags` before use.

## APIs

| provider | best use | notes |
|---|---|---|
| Codex high effort | proof construction, adversarial review | available, but avoid for routine use unless explicitly needed |
| Gemini Pro OAuth | deep thinking, long review | OAuth may need interactive login |
| Mistral | proof/reasoning and code tasks | use exact endpoint/key conventions |
| OpenRouter | broad deep writeups | paid/credit-aware |
| Cohere | synthesis and RAG-style summaries | cheap/default tier |
| SambaNova | deep analysis | use exact `DeepSeek-V3.1`; curl subprocess |
| Groq | quick checks and fast summaries | cheap/default tier |
| Cerebras | bursty large-model calls | model names change; verify current access first |
| Aristotle | Lean 4 formalization | use only for Lean submission tasks |

Credentials are not stored in this repo. Paths only: `~/.farey_api_keys`, `~/.aristotle_api_key`, `~/.ssh/id_ed25519`.

## New Routine Design Rule

Build new routines from this capability map and [[projects/farey-research/task-queue]]. Do not copy old cron files or scheduled-agent definitions.

## Routing At A Glance

- Deep proof review: Gemini Pro OAuth, Mistral large, or Codex high effort if the user explicitly wants Codex.
- Lean 4 formalization: Aristotle first.
- Medium writeups and synthesis: Gemini Flash/Pro, Mistral small/medium, Cohere, OpenRouter, or SambaNova depending on latency and quota.
- Quick summaries / fact lookups: Groq or Gemini Flash-lite.
- Numerical/PARI work: M1B first, then M2 if the daemon is healthy.
- Large local proof/writing: M1.
- Repo checkpoint commits and pushes: `farey-publisher` on `gpt-5.4-mini`.
