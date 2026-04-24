# Log

## [2026-04-24] review | recent compute/API outputs

Reviewed the recent M1/API output bundle under `raw/farey-archive/recent-outputs/`. Promoted only roadmap-level consequences: W2 prime remains the main validation track; the log-conductor term stays live; simple Deligne/Gamma normalization does not explain C1; Paper C arithmetic-surrogate theorem language is blocked; pair-correlation work needs primary-source review and a fresh script. Marked stale-baseline, `CANNOT COMPUTE`, traceback, and placeholder-citation outputs as archive-only/context rot.

## [2026-04-24] sync | Koyama reply and routing refresh

Updated the Koyama correspondence record and claim ledger to reflect the latest reply: Koyama endorsed the bugfix-and-recompute update, highlighted the linear-in-rank observation as interesting, and introduced the "Dominance of -1" challenge with an explicit request for dynamic-range verification beyond the 13 trillion baseline. Also expanded the Farey routing docs so Groq, Cohere, SambaNova, Cerebras, OpenRouter, Mistral, Gemini, Aristotle, M1, M1B, M2, and farey-publisher are all represented in routing decisions.

## [2026-04-24] ingest | Fresh Farey Research

Reinitialized this folder as a local Fresh Farey repo, archived relevant old Farey evidence under `raw/farey-archive/` with `MANIFEST.jsonl`, copied canonical working data/scripts into `projects/farey-research/`, and synthesized lean Token Economy pages for current state, claim ledger, C1, W2 prime, Koyama correspondence, compute agents, task queue, and context rot.

## [2026-04-24] ship | universal agent framework v1

Added `start.md`, `token-economy.yaml`, the `te` CLI, lean agent adapters, L0/L1 memory files, wiki-search v1, context-refresh, delegate-router, and context-keeper v2 retrieval tools. Verified with `bash scripts/run_all_tests.sh`.

## [2026-04-24] ship | agent-ignition supplement

Added wiki schema v2 templates, model-agnostic skills/prompts, context meter + handoff lint, stricter delegation contracts, hooks/configs/extensions, install dry-run, profile support, framework smoke bench, and CI gate. Verified with `bash scripts/run_all_tests.sh`, `te wiki lint --strict --fail-on-error`, `te bench run --suite framework-smoke`, JSON config validation, and Python compile.

## [2026-04-24] ship | personal-assistant routing

Added `/pa` and `/btw` prompt bypass via `te pa`, hook routing, a personal-assistant skill, and router prompt. Purpose: route context-light prompts through a lightweight classifier/dispatcher with minimal context, escalating only when risk or complexity requires the main model.

## [2026-04-24] harden | repo-local startup review

Reviewed the framework, repo docs, and setup prompt for duplicated startup glue, stale global setup language, noisy hooks, and routing/context-meter gaps. Updated `HANDOFF.md`, startup docs, `L0_rules.md`, wiki schema defaults, docs audit scope, context meter model sizing, adapter overwrite detection, and prompt hook behavior. Verified with `bash scripts/run_all_tests.sh`, `./INSTALL.sh --dry-run`, `./te wiki lint --strict --fail-on-error`, `./te doctor`, `./te hooks doctor`, `./te bench run --suite framework-smoke`, Python compile, `git diff --check`, active-doc global-term scan, and token-budget checks.

## [2026-04-24] harden | fresh folder setup

Updated the setup prompt and onboarding docs to keep first-run setup simple: if the target folder lacks `token-economy.yaml`, the prompt explicitly permits clearing that current folder only, including hidden files and `.git`, then cloning the canonical repo fresh. Purpose: avoid false stops in non-empty setup folders while still forbidding deletion outside the target folder.

## 2026-04-17

Terminology: **ComCom** = our compound-compression project (disambiguate from Claude Code's "CC").
- Wiki created. Folder: repo-local `Token Economy/` markdown wiki.
- Ingested research brief → `raw/2026-04-17-research-brief.md`.
- Setup confirmed: caveman plugin active, superpowers skill loaded, wiki initialized.
- Next: flesh out concept pages, pick first project (likely compound-compression-pipeline or wiki-query-shortcircuit).
- Built [[projects/compound-compression-pipeline]] (aka **ComCom**). Measured 70-73% on prose, 59% on mixed technical at gentler rate. Code/paths/URLs preserved via placeholder protection.
- Ingested [[raw/2026-04-17-semantic-diff-survey]]. Novelty 4/5. Created [[concepts/semantic-diff-edits]]. Added [[ROADMAP]] as live tracker.
- Ran quality eval on Ollama (phi4:14b, 3 tasks). Result: 55.7% token savings @ 100% quality retention at rate=0.5. Placeholder format fixed (`XPROTECT{n}XEND` survives BERT tokenization). Compressed prompts also faster (1.4s vs 9.8s observed).
- Built eval-v2: SQuAD v2 + gemma4:31b judge + bootstrap CIs + failure-mode classification. Running in background.
- Built [[projects/semdiff]] (AST-node diff). Measured 95.5% savings after 2 method edits on argparse.py (2575 lines, 19,280 → 859 tokens); 99.5% on stable re-read. Tree-sitter for py/js/ts/rust.
- Kaggle auth set up (user: saarshai).
- Built [[projects/context-keeper]]. Skill + PreCompact hook. Regex extractor + optional local-LLM pass. Current framework writes memory under repo-local `.token-economy/` paths.
- **Eval-v2 completed** (SQuAD v2, n=8, 2 runs, phi4:14b + qwen3:8b judge). Token savings **44.5% CI [41.5-47.4]**. Δscore **−0.25 CI [−0.62, 0.00]**. Failure modes on comp: 8 NONE, 6 MISSING, 2 SWAP. **v1's "55.7% @ 100%" overstated**; principled measurement shows small, non-significant quality hit. N too small to resolve CI. Judge swap (gemma4:31b → qwen3:8b) fixed 129s latency thrash.
- Built ComCom v2 (pipeline_v2.py) with question-aware + critical-zone protection; eval-v3 in progress (4 conditions: full, v1, v2, adaptive-escalation). Early data shows v2 over-compresses (critical-protect + rate=0.5 on remainder = total too low). Fix planned: scale rate by (1 - protected_fraction).
- **semdiff MCP server built**. Python 3.11 + mcp SDK. 3 tools exposed (read_file_smart, snapshot_clear, snapshot_status). Protocol roundtrip tested (initialize, tools/list, tools/call all pass). CC plugin wrapper at `plugin/.mcp.json`. Install docs at [[projects/semdiff/INSTALL]].
- **bench/ built**. Kaggle API wired via registry.yaml. 7 datasets registered (2 downloaded so far). Adapters emit uniform {id, context, question, answer, type, meta} schema. CoQA multi-turn items designed for growing-context stress. Kaggle Notebook template drafted for free-T4-GPU evals (30h/wk, 10× local throughput). See [[bench/README]].
- **Eval-v3 complete (ComCom upgrade)**. D_adaptive (self-verify escalation) delivers 44.9% savings at Δscore −0.12 [−0.38, 0.00] — quality effectively preserved. Zero REFUSE failures. C_v2 (question-aware + critical-zone) confirmed broken by over-compression; fix deprioritized since D_adaptive bypasses the issue. Shipped config: `pipeline_v2.compress` + `verify.escalate_gen`.

## [2026-04-20] download-status | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=in-progress (authenticated curl running, ETA ~12h)
## [2026-04-20 22:36 BST] download-complete | Qwen3.6-35B-A3B-5bit | M1B all 5 shards verified (24.73 GB) via LAN HTTP server; shard1 required fresh download after dual-curl corruption; see /tmp/resume_qwen36_report.md
## [2026-04-20] download-finish | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=complete (LAN transfer from M1:8888, all 5 shards verified, ~23GB, completed ~14:36 PDT)
## [2026-04-21] download-finish | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=complete
## [2026-04-24] dispatch | Active Farey agent queue

- Created [[projects/farey-research/active-agent-queue]] after Saar approved the 30-task campaign.
- Scope: Koyama reply, Dominance-of-minus-one compute design, W2 prime validation, C1/Delta normalization, and theory/paper pipeline.
- Routing excludes M2 and Codex API for this campaign; dispatcher should use M1, M1B, Gemini, Aristotle, Groq, Cohere, SambaNova, Cerebras, OpenRouter, and Mistral.

## [2026-04-24] dispatch | First wave results

- Completed K01, K04, D01, W01, C01, and T01 for the active Farey campaign.
- T01 first blocked on M1 because Ollama was down, then completed via Mistral.
- Created heartbeat automation `farey-agent-queue-monitor` for 15-minute queue checks.

## [2026-04-24] dispatch | Long-haul queue extension

- Added a long-haul batch to [[projects/farey-research/active-agent-queue]] so M1B and M1 have several hours of follow-on work.
- Long-haul work is mostly M1B numerical/comparison tasks, with M1 theory/writeup tasks carrying explicit fallback routes so the queue can keep moving if the M1 daemon stays down.

## [2026-04-24] rule | subagent queue discipline

- Recorded the durable rule to close only completed idle subagents so thread slots clear cleanly.
- Recorded the monitor-subagent rule: once spawned, let the monitor keep dispatching until the queue is complete or Saar stops it, and do not intervene or review early.
## [2026-04-24 13:39 BST] dispatch-update | First wave results
- K01 done on Gemini; K04 done on Cohere; D01 done on M1B; W01 done on M1B; C01 done on M1B.
- T01 blocked on M1 because `curl: (7) Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server`.
- W01 used `projects/farey-research/data/W2_PRIME_FIT.json` and matched stored coefficients to within `3.764e-14`.
