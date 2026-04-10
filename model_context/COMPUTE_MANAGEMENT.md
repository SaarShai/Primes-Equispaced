# Compute Management — DEFINITIVE PROCEDURES
# Everything here is PERMANENT infrastructure. Nothing session-scoped.
# Last updated: 2026-04-09

---

## ARCHITECTURE OVERVIEW

```
PERMANENT (survives session death):
  System crontab → m1max_watchdog.sh (every 15 min)
                 → m5max_watchdog.sh (every 15 min, only when enabled)
  
  m1max_continuous.sh → reads M1MAX_QUEUE.txt → runs on M1 Max (192.168.1.218)
  m5max_continuous.sh → reads M5MAX_QUEUE.txt → runs on local ollama

SESSION-DEPENDENT (Claude provides intelligence):
  Claude session → reviews results → writes NEXT_TASKS → updates master table
  Claude session → invokes Codex, Aristotle, Q3.6 on demand
```

---

## TIER 1: M1 Max (192.168.1.218) — ALWAYS RUNNING

### Models
- **deepseek-r1:32b** — proofs, rigorous derivations
- **qwen3.5:35b** — research, analysis, paper drafts

### Infrastructure
| Component | File | Purpose |
|-----------|------|---------|
| Watchdog | ~/bin/m1max_watchdog.sh | Cron: check runner + queue every 15 min |
| Runner | ~/bin/m1max_continuous.sh | Process: read queue, run tasks, loop forever |
| Refill | ~/bin/m1max_refill_queue.sh | Load CURATED tasks from NEXT_TASKS into queue |
| Queue | ~/Desktop/Farey-Local/M1MAX_QUEUE.txt | Active task queue |
| Next tasks | ~/Desktop/Farey-Local/M1MAX_NEXT_TASKS.txt | Curated by Claude after review |
| Task runner | ~/bin/remote_ollama.sh | Send task to M1 Max (standard) |
| Deepseek runner | ~/bin/remote_ollama_deepseek.sh | Send task to M1 Max (streaming) |

### Queue Format
```
MODEL|TASK_NAME|PROMPT
```
Example:
```
qwen3.5:35b|VARIANCE_PROOF_V3|Prove that... at least 2000 words.
deepseek-r1:32b|DS_DIAGONAL_SUM|Compute rigorously...
```

### CRITICAL RULES
1. M1 Max is NEVER idle
2. When queue empties, watchdog loads from M1MAX_NEXT_TASKS.txt
3. If NEXT_TASKS is also empty, M1 Max waits for Claude session to review + curate
4. Tasks are NEVER auto-generated — always curated based on result review
5. Results go to ~/Desktop/Farey-Local/experiments/{TASK_NAME}.md

---

## TIER 2: M5 Max (local) — ON DEMAND / OVERNIGHT

### Models
- **deepseek-r1:32b** — proofs (same as M1 Max, but local)
- **qwen3.5:35b** — research, analysis
- **gemma4:26b** — literature, breadth, connections

### Infrastructure
| Component | File | Purpose |
|-----------|------|---------|
| Watchdog | ~/bin/m5max_watchdog.sh | Cron: check runner (only when enabled) |
| Runner | ~/bin/m5max_continuous.sh | Process: read queue, run local ollama |
| Queue | ~/Desktop/Farey-Local/M5MAX_QUEUE.txt | Active task queue |
| Next tasks | ~/Desktop/Farey-Local/M5MAX_NEXT_TASKS.txt | Curated by Claude |
| Enable flag | ~/Desktop/Farey-Local/M5MAX_ENABLED | File exists = enabled |

### Activation
```bash
~/bin/compute_control.sh start   # Enable overnight
~/bin/compute_control.sh stop    # PAUSE (not delete!) overnight
~/bin/compute_control.sh status  # Show all tiers
```

### CRITICAL RULES
1. Default: OFF. Only enabled by user ("start overnight")
2. PAUSE, never delete. Queue preserved across stop/start
3. Cannot run qwen3.5:35b and gemma4:26b simultaneously (RAM conflict)
4. Queue tasks should specify model — runner handles sequencing
5. gemma4 available HERE but NOT on M1 Max

### RAM Conflict Management
- deepseek-r1:32b (19GB) + phi4:14b (9GB) = 28GB — OK
- qwen3.5:35b (23GB) alone — OK
- gemma4:26b (17GB) alone — OK
- qwen3.5:35b + gemma4:26b = 40GB — TOO MUCH, will swap
- Runner runs tasks SEQUENTIALLY, so model switching is fine

---

## TIER 3: API — ON DEMAND (Claude session invokes)

### Model Assignments
| Model | Use For | How to Invoke |
|-------|---------|---------------|
| **Codex (GPT-5.4)** | Deep thinking, adversarial review | Agent tool with subagent_type: "codex:codex-rescue" |
| **Aristotle** | Lean 4 formalization | API at ~/.aristotle_api_key |
| **Q3.6 Plus** | Strategic analysis (rare) | OpenRouter (frequently rate-limited) |

### CRITICAL RULES
1. Codex = THINKING ONLY. Cannot write files. Returns text to Claude.
2. Aristotle = submit all pending Lean formalizations proactively
3. Q3.6 = backup only, don't depend on it (rate limits)
4. These run during Claude sessions, not via cron

---

## MODEL ROUTING — DEFINITIVE

### By Task Type
| Task | Primary Model | Machine | Fallback |
|------|--------------|---------|----------|
| Proofs/rigorous math | deepseek-r1:32b | M1 Max or M5 Max | qwen3.5:35b |
| Research/analysis | qwen3.5:35b | M1 Max or M5 Max | gemma4:26b |
| Literature/breadth | gemma4:26b | M5 Max only | qwen3.5:35b |
| Quick verification | phi4:14b | M5 Max only | qwen3:8b |
| Deep thinking/adversarial | Codex | API | Claude |
| Lean formalization | Aristotle | API | — |
| Strategic (rare) | Q3.6 | API | Claude |
| Paper writing | Claude | Session | — |
| Synthesis/decisions | Claude | Session | — |

### By Machine
| Machine | Models | Use |
|---------|--------|-----|
| M1 Max (remote) | deepseek-r1:32b, qwen3.5:35b | ALWAYS: proofs + research |
| M5 Max (local) | deepseek-r1:32b, qwen3.5:35b, gemma4:26b | ON DEMAND: proofs + research + literature |
| API | Codex, Aristotle, Q3.6 | ON DEMAND: thinking + Lean + strategy |

### Parallel Strategy
- M1 Max runs INDEPENDENTLY of M5 Max — different machines, no conflict
- M5 Max models run SEQUENTIALLY (RAM sharing)
- API runs INDEPENDENTLY of both — cloud, no local resource cost
- All 3 tiers can run simultaneously!

---

## REVIEW + TASK CREATION CYCLE (Claude session responsibility)

### When Claude Session Starts
1. `~/bin/compute_control.sh status` — check all tiers
2. Read recent results: `ls -lt ~/Desktop/Farey-Local/experiments/*.md | head -20`
3. Review results (read files, evaluate quality)
4. Update wiki with findings
5. Update MASTER_TABLE_INDEX.md if priorities changed
6. Write NEW curated tasks to M1MAX_NEXT_TASKS.txt and/or M5MAX_NEXT_TASKS.txt
7. Invoke API tasks (Codex, Aristotle) as needed

### Reviewing Results — PROCEDURE
1. Read result file
2. Assess: is this substantial (>5KB) or thin (<2KB)?
3. If substantial: extract key findings, update wiki, check if it advances master table direction
4. If thin: note failure, don't re-send same task — reformulate or try different model
5. Cross-check rule: finding from Model A → verify on Model B
6. Based on findings: create NEW tasks that build on results
7. Write these to NEXT_TASKS.txt (format: MODEL|TASK_NAME|PROMPT)

### Creating Tasks — RULES
1. Every task must advance a specific MASTER_TABLE direction
2. Include master table ID in task name when possible (e.g., UNI_3_MINIMUM_SUBSET)
3. Tasks must request SPECIFIC output: "prove X", "derive Y", "compute Z"
4. Always include "at least 2000 words" for qwen3.5 (prevents thin output)
5. For deepseek: ask for RIGOROUS step-by-step (it gives boxed answers otherwise)
6. NEVER re-send a task that already produced thin results without reformulation
7. NEVER auto-generate tasks — always based on reviewed findings

### Updating Master Table — WHEN
- Result confirms a direction → update status
- Result disproves a direction → mark DEAD, move to MASTER_TABLE_DEAD.md
- Result opens new direction → add with priority
- Result changes understanding → update all affected entries

---

## WHAT HAPPENS BETWEEN SESSIONS (NO Claude)

1. System crontab runs watchdogs every 15 minutes
2. M1 Max: processes queue, loads NEXT_TASKS when empty, idles when both empty
3. M5 Max: same pattern, but only if ENABLED
4. Results accumulate in experiments/
5. No auto-generated tasks — machines wait for Claude session to review + curate
6. This is BY DESIGN: we don't want blind task loops

---

## SYSTEM CRONTAB (PERMANENT)
```
*/15 * * * * ~/bin/m1max_watchdog.sh >> /tmp/m1max_watchdog_cron.log 2>&1
*/15 * * * * ~/bin/m5max_watchdog.sh >> /tmp/m5max_watchdog_cron.log 2>&1
```

---

## FILES REFERENCE

### Scripts (~/bin/)
| Script | Purpose |
|--------|---------|
| m1max_watchdog.sh | Cron: check M1 Max runner + queue |
| m1max_continuous.sh | M1 Max task runner (loops forever) |
| m1max_refill_queue.sh | Load curated NEXT_TASKS into queue |
| m5max_watchdog.sh | Cron: check M5 Max runner + queue |
| m5max_continuous.sh | M5 Max task runner (loops forever, local) |
| compute_control.sh | Start/stop/status for all tiers |
| remote_ollama.sh | Send single task to M1 Max |
| remote_ollama_deepseek.sh | Send deepseek task to M1 Max (streaming) |

### Data Files (~/Desktop/Farey-Local/)
| File | Purpose |
|------|---------|
| M1MAX_QUEUE.txt | Active M1 Max task queue |
| M1MAX_NEXT_TASKS.txt | Curated tasks, loaded by refill when queue empty |
| M5MAX_QUEUE.txt | Active M5 Max task queue |
| M5MAX_NEXT_TASKS.txt | Curated tasks for M5 Max |
| M5MAX_ENABLED | Flag file: exists = M5 Max enabled |
| MASTER_TABLE_INDEX.md | All research directions + priorities |
| PAPER_CONSTELLATION.md | 12 papers + survey |

### Results (~/Desktop/Farey-Local/experiments/)
| Pattern | Source |
|---------|--------|
| M1_*.md | M1 Max results |
| M5_*.md | M5 Max results |
| AUTO_*.md | M1 Max auto-generated (LEGACY — no longer used) |
| Q36_*.md | Q3.6 API results |
| ARISTOTLE_*.md | Aristotle API results |
| CODEX_*.md | Codex results |

---

## TROUBLESHOOTING

### M1 Max idle
```bash
crontab -l                                    # watchdog entry exists?
cat /tmp/m1max_continuous.lock                 # PID?
kill -0 $(cat /tmp/m1max_continuous.lock)      # alive?
wc -l ~/Desktop/Farey-Local/M1MAX_QUEUE.txt   # tasks?
~/bin/m1max_watchdog.sh                        # manual trigger
```

### M5 Max not running
```bash
ls ~/Desktop/Farey-Local/M5MAX_ENABLED         # enabled?
~/bin/compute_control.sh start                  # enable
~/bin/m5max_watchdog.sh                         # manual trigger
```

### Model returns empty/thin
1. Check if another model is loaded (RAM conflict)
2. Restart ollama: `ollama stop <model>` then retry
3. Reformulate task — don't re-send verbatim
