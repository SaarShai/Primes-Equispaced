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

- Use: M1, M1B, M2 Ollama, Gemini, Aristotle, Groq, Cohere, SambaNova, Cerebras, OpenRouter, Mistral.
- Prefer M2 `qwen3.6:latest` for local theory/drafting/review tasks when it is available; use M2 `gemma4:31b` for literature/novelty brainstorming.
- Do not use: Codex API, old scheduled agents.
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
| K02 | Koyama reply | Gemini | structured email outline, no send | reviewed |
| K03 | Koyama reply | Mistral or OpenRouter | unsafe-claim/adversarial review of draft claims | reviewed |
| K04 | Koyama reply | Cohere | exact Dominance-of-minus-one clarification questions | done |
| K05 | Koyama reply | Gemini | cautious W2 prime paragraph for Koyama | reviewed |
| K06 | Koyama reply | Cohere | bugfix and raw Sym2 falsification paragraph | reviewed |
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
- K02, K03, K05, and K06 were reviewed in [[projects/farey-research/incoming-results-review-2026-04-24]].
- K02 is meta-outline only; K03 is incomplete and too hesitant about the narrow raw Sym2 falsification; K05 is useful only with softer wording.
- K06 must not be used as written; it wrongly describes the `mu_f(p^2)` bug as Farey-sequence-related.

## First Wave

Start with K01, K04, D01, W01, C01, and T01. This gives the Koyama reply immediate substance while numerical and theory lanes begin in parallel.

## Long-Haul Batch

These tasks are meant to keep M1B busy for hours and give M1/M2 enough theory/writeup work to stay fed if local daemons are healthy. If M1 is unavailable, prefer M2 `qwen3.6:latest` for local theory/drafting tasks before paid API fallback unless the task explicitly needs an external API.

| id | direction | route | deliverable | status |
|---|---|---|---|---|
| H01 | Dominance | M1B | segmented dynamic `pi(x;q,a)` pilot plan for a bounded modulus set | queued |
| H02 | Dominance | M1B | storage and checkpoint budget for several-hour prime sweeps | queued |
| H03 | W2 prime | M1B | leave-one-out residual table with a one-page interpretation | queued |
| H04 | W2 prime | M1B | rank-0 high-conductor comparison table from canonical data | queued |
| H05 | W2 prime | M1B | 37a1 vs 389a1 vs 5077a1 standardized comparison note | queued |
| H06 | C1/Delta | M1B | Delta per-zero K-convergence cross-check using canonical scripts/data | queued |
| H07 | C1/Delta | M1B | kernel/smoothing sensitivity note with recommended default | queued |
| H08 | C1/Delta | M1B | reproducibility manifest for current C1 and W2 scripts | queued |
| H09 | Koyama reply | M1 or M2 `qwen3.6:latest` | cautious grant/CV reply outline, with `Mistral` fallback if local models are down | queued |
| H10 | Koyama reply | M1 or M2 `qwen3.6:latest` | Dominance-of-minus-one question framing memo, with `OpenRouter` fallback if local models are down | queued |
| H11 | Theory/papers | M1 or M2 `qwen3.6:latest` | Rankin-Selberg / explicit-formula mechanism note for W2 prime, with `Mistral` fallback if local models are down | queued |
| H12 | Theory/papers | M1 or M2 `qwen3.6:latest` | Paper C replacement theorem sketch using density/proportion/mollifier language, with `Mistral` fallback if local models are down | queued |
| H13 | Theory/papers | M1 or M2 `gemma4:31b` | primary-source pair-correlation bibliography and citation-safe summary, with `Gemini` fallback if local models are down | queued |
| H14 | Theory/papers | M1 or M2 `qwen3.6:latest` | claim-safe paragraph set for an eventual Koyama email, with `OpenRouter` fallback if local models are down | queued |
| H15 | W2 prime | M1B | narrow-conductor contrast experiment design for the next compute window | queued |
| H16 | Dominance | M1B | minimal pilot definition below `13e12` that still answers Koyama's dynamic-x request | queued |

## Breakthrough Queue

This queue implements the incoming-results review. Do not treat generated outputs as promoted evidence until Saar asks for a review.

### Koyama Email Package

| id | route | task | output | status |
|---|---|---|---|---|
| K07 | main/Gemini | draft full Koyama email from reviewed parts only | user-review draft, no send | queued |
| K08 | Mistral/OpenRouter | adversarial review of K07 for overclaiming | unsafe-claim report | queued |
| K09 | main | replace K06 with corrected bugfix paragraph | email-ready paragraph | queued |
| K10 | Gemini | produce concise CV/grant block with factual blanks marked | CV insert | queued |
| K11 | Cohere | refine Dominance questions into compact email form | 6-8 questions | queued |
| K12 | main | assemble final Koyama email packet | draft plus notes | queued |

### Dominance Of `-1`

| id | route | task | output | status |
|---|---|---|---|---|
| D02 | M1B | design segmented residue-tally schema | data schema plus checkpoint plan | queued |
| D03 | Gemini + M2 `qwen3.6:latest` or `gemma4:31b` | literature map: prime races, Chebyshev bias, dynamic `x` | source list plus novelty memo | queued |
| D04 | M1B | runtime/storage estimates for `1e13`, `1e14`, `3e14` | budget table | queued |
| D05 | M1B | define pilot below `13e12` once Koyama gives modulus | pilot spec | blocked |
| D06 | M1B | prototype dynamic-grid API contract | pseudocode plus CLI contract | queued |
| D07 | Cerebras/OpenRouter | adversarial feasibility review | bottleneck/risk memo | queued |

### W2 Prime Validation

| id | route | task | output | status |
|---|---|---|---|---|
| W02 | M1B | leave-one-out diagnostics on 22-point fit | residual/LOO table | queued |
| W03 | M1B | bootstrap coefficient stability | CI and leverage report | queued |
| W04 | Gemini | pick rank-0 high-conductor EC controls | label list | queued |
| W05 | M1B | compute or plan rank-0 high-conductor controls | comparison table | queued |
| W06 | M1B | fixed/narrow-conductor rank contrasts | design plus first results | queued |
| W07 | OpenRouter/Cerebras | statistical critique of W2 prime | overfit/model-risk memo | queued |
| W08 | M1B | separate 200-zero vs 500-zero anchors in all tables | clean evidence table | queued |
| W09 | main | update roadmap after W02-W08 review | promoted/rejected findings | blocked |

### C1 / Delta / Normalization

| id | route | task | output | status |
|---|---|---|---|---|
| C02 | M1B | bad-prime local-factor audit | convention note | queued |
| C03 | M1B | Delta `K`-sweep plan and cost estimate | run matrix | queued |
| C04 | M1B | kernel/smoothing sensitivity experiment design | matrix plus default | queued |
| C05 | Aristotle | formalize exact `mu_f(p^2)` convention target | Lean feasibility note | queued |
| C06 | Cohere | safe Delta-only conjecture wording | paper/email text | queued |
| C07 | M1B | verify no active script uses old `a_{p^2}` convention | scan report | queued |
| C08 | main | promote C1 normalization gate result after review | claim-ledger update plan | blocked |

### Theory / Novelty / Papers

| id | route | task | output | status |
|---|---|---|---|---|
| T02 | Mistral | Sym2/Deligne normalization possibilities, source-aware | math memo | queued |
| T03 | Aristotle | Paper C arithmetic-surrogate failure/formal risk | proof-risk note | queued |
| T04 | M1 or M2 `qwen3.6:latest`, Mistral fallback | density/proportion/mollifier replacement theorem | theorem plan | queued |
| T05 | Gemini + M2 `gemma4:31b` | primary-source pair-correlation bibliography | citation-safe memo | queued |
| T06 | M1 or M2 `qwen3.6:latest`, OpenRouter fallback | explicit-formula mechanism for `log(N)` term | derivation attempt | queued |
| T07 | main | identify breakthrough criteria vs artifact criteria | decision memo | queued |
| T08 | main | build paper triage for C1/W2, Delta, Dominance, Paper C | paper roadmap | queued |
