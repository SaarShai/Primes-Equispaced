---
schema_version: 2
title: Active Agent Queue
type: project
domain: project
tier: working
confidence: 0.9
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - projects/farey-research/task-queue.md
  - projects/farey-research/compute-agents.md
  - projects/farey-research/koyama-correspondence.md
  - projects/farey-research/w2-prime.md
  - L2_facts/farey-claim-ledger.md
supersedes: []
superseded-by:
tags: [farey, agents, queue, koyama, w2-prime]
---

# Active Agent Queue

## Scope

Fresh 30-task campaign approved on 2026-04-24. Goal: make progress on the top Farey research directions, with immediate emphasis on a careful Koyama reply. This queue is active only through the new dispatcher; do not revive old cron jobs, hourly routines, or stale `NEXT_TASKS` files.

## Routing Rules

- Use: M1, M1B, Gemini, Aristotle, Groq, Cohere, SambaNova, Cerebras, OpenRouter, Mistral.
- Do not use: M2 for this campaign, Codex API, old scheduled agents.
- No email is sent without Saar's explicit approval.
- API keys and credentials must not be written to repo files or logs.
- Results are evidence only after review; raw model outputs stay archived or summarized.
- Commit/push meaningful checkpoints through `farey-publisher`.

## Top Directions

1. Koyama reply package: CV/grant positioning, W2 update, Dominance-of-minus-one feasibility, exact questions.
2. Dominance-of-minus-one compute design: define target, estimate feasibility, build dynamic prime-counting plan.
3. W2 prime validation: stress-test regression, conductor/rank separation, reproducibility.
4. C1/Delta normalization and asymptotics: verify arithmetic conventions, bad primes, kernel dependence, K sweeps.
5. Theory/paper pipeline: W2 mechanism, safe Sym2/Rankin-Selberg framing, Paper C repairs, pair-correlation only after primary-source verification.

## Dispatcher Contract

The dispatcher should maintain a minimal status board from this queue:

- `queued`: not sent
- `sent`: dispatched to an agent
- `running`: agent acknowledged or output file is actively changing
- `blocked`: needs user/main-agent decision
- `done`: compact result packet received
- `reviewed`: main agent reviewed and promoted/rejected

Every 15 minutes while active, check whether M1 or M1B is idle and whether API tasks have returned. If an agent is idle, send the highest-priority queued task that matches its route.

## Tasks

| id | direction | route | deliverable | status |
|---|---|---|---|---|
| K01 | Koyama reply | Gemini | factual CV/grant bullet block | done |
| K02 | Koyama reply | Gemini | structured email outline, no send | queued |
| K03 | Koyama reply | Mistral or OpenRouter | unsafe-claim/adversarial review of draft claims | queued |
| K04 | Koyama reply | Cohere | exact Dominance-of-minus-one clarification questions | done |
| K05 | Koyama reply | Gemini | cautious W2 prime paragraph for Koyama | queued |
| K06 | Koyama reply | Cohere | bugfix and raw Sym2 falsification paragraph | queued |
| D01 | Dominance | M1B | feasibility estimate for hundreds-of-trillions dynamic prime-bias verification | done |
| D02 | Dominance | M1B | segmented counting/data schema for dynamic `x` curves | queued |
| D03 | Dominance | Gemini | algorithms/tools memo for `pi(x;q,a)` scale work | queued |
| D04 | Dominance | M1B | M1/M1B runtime and storage estimate | queued |
| D05 | Dominance | M1B | minimal pilot below `13e12` | queued |
| D06 | Dominance | Gemini | email paragraph on feasibility and prerequisites | queued |
| W01 | W2 prime | M1B | reproducible W2 regression from canonical data | done |
| W02 | W2 prime | M1B | leave-one-out and bootstrap diagnostics | queued |
| W03 | W2 prime | Gemini | rank-0 high-conductor control curve list | queued |
| W04 | W2 prime | M1B | fixed/narrow-conductor rank-contrast experiment plan | queued |
| W05 | W2 prime | M1B | 37a/37b sanity report | queued |
| W06 | W2 prime | Cerebras or OpenRouter | adversarial statistical critique of W2 prime | queued |
| C01 | C1/Delta | M1B | audit `mu_f(p^2)` convention in scripts/data | done |
| C02 | C1/Delta | M1B | bad-prime local-factor convention note | queued |
| C03 | C1/Delta | M1B | Delta K-sweep plan for approach-to-1 test | queued |
| C04 | C1/Delta | M1B | kernel/smoothing-dependence experiment matrix | queued |
| C05 | C1/Delta | Aristotle | exactness notes for C1 formula/formalization candidates | queued |
| C06 | C1/Delta | Cohere | safe Delta-only conjecture wording | queued |
| T01 | Theory/papers | M1, rerouted to Mistral | W2 mechanism derivation attempt via Rankin-Selberg/explicit formula | done |
| T02 | Theory/papers | Mistral | Sym2/Deligne normalization possibilities memo | queued |
| T03 | Theory/papers | Aristotle | Paper C arithmetic-surrogate failure/formal risk note | queued |
| T04 | Theory/papers | M1 | density/proportion/mollifier replacement theorem plan | queued |
| T05 | Theory/papers | Gemini | primary-source pair-correlation citation memo | queued |
| T06 | Theory/papers | Gemini | integrated draft Koyama response from reviewed packets, no send | queued |

## Dispatch State

- Done: K01, K04, D01, W01, C01, T01.
- T01 first blocked on M1. Exact M1 Ollama error: `curl: (7) Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server`.
- T01 was rerouted to Mistral and completed at `raw/farey-archive/recent-outputs/library-experiments/T01_MISTRAL_W2_MECHANISM.md.txt`.
- M1B stayed single-queue, so W01 and C01 ran after D01.

## First Wave

Start with K01, K04, D01, W01, C01, and T01. This gives the Koyama reply immediate substance while numerical and theory lanes begin in parallel.
