# Model Routing — DEFINITIVE
# Updated: 2026-04-09

## Model Assignments by Task Type

| Task Type | Model | Machine | Notes |
|-----------|-------|---------|-------|
| Proofs/rigorous math | deepseek-r1:32b | M1 Max or M5 Max | Best for step-by-step rigor |
| Research/analysis | qwen3.5:35b | M1 Max or M5 Max | Deep reasoning, 17KB outputs |
| Literature/breadth | gemma4:26b | M5 Max ONLY | Broad knowledge, connections |
| Quick verification | phi4:14b | M5 Max ONLY | Fast, lightweight |
| Deep thinking/adversarial | Codex (GPT-5.4) | API | THINKING only, no file writes |
| Lean 4 formalization | Aristotle | API | Submit proactively |
| Strategic (rare) | Q3.6 Plus | API (OpenRouter) | Rate-limited, backup only |
| Paper writing | Claude | Session | Quality matters |
| Synthesis/decisions | Claude | Session | Human-in-the-loop |

## Model Assignments by Machine

### M1 Max (remote, 192.168.1.218, 32GB RAM)
- deepseek-r1:32b (19GB) — proofs
- qwen3.5:35b (23GB) — research
- Run sequentially (one model at a time)
- ALWAYS running via permanent watchdog

### M5 Max (local, 128GB RAM)
- deepseek-r1:32b (19GB) — proofs
- qwen3.5:35b (23GB) — research
- gemma4:26b (17GB) — literature/breadth
- phi4:14b (9GB) — quick checks
- Run sequentially (RAM conflict between large models)
- ON DEMAND — enabled by user

### API (cloud, no local resources)
- Codex — deep thinking, adversarial review
- Aristotle — Lean 4 proofs
- Q3.6 — strategic analysis (rare, rate-limited)
- Invoked by Claude session, not automated

## Anti-Patterns (DO NOT)
- DON'T use Codex for file writes (sandboxed)
- DON'T use gemma4 for deep math proofs (too shallow)
- DON'T use qwen3:8b for anything requiring reasoning
- DON'T use Q3.6 for batch tasks (rate limit kills throughput)
- DON'T run 35b and gemma4 simultaneously on M5 Max (RAM conflict)
- DON'T send to 8b/gemma4 while 35b is loaded (empty response)
- DON'T use 35b for code generation (bugs). Use general agents.
- DON'T re-send failed tasks verbatim — reformulate first
- DON'T auto-generate tasks — always curate based on result review

## DEEPSEEK FABRICATION GUARD (added 2026-04-13 — MANDATORY)
Deepseek-r1:32b FABRICATES when asked to "derive" algebraic identities from scratch.
CONFIRMED FABRICATIONS:
  - "ΔW(p) = (p-1)/2·M(p)" — produced TWICE unprompted. FALSE at all tested primes.
  - "R₂ ≥ 0 manifestly" — FALSE. R₂(197) = -2.831e-06 < 0 (locally verified).
ROOT CAUSE: deepseek pattern-matches to "plausible" boxed formula when asked to derive.
FIX: anti-fabrication rules now injected via remote_ollama_deepseek.sh system prompt.
USAGE RULE: DON'T ask deepseek to "derive" ΔW = f(M(p)). DO ask it to VERIFY numerically.
USAGE RULE: DON'T ask deepseek to "prove R₂ ≥ 0". DO ask it to compute R₂(p) for p≤300.
USAGE RULE: Always give deepseek the counterexample IN THE PROMPT when known.

## Codex Special Rules
- codex:codex-rescue = THINKING ONLY
- Cannot write to ~/Desktop/Farey-Local/ (sandbox)
- Returns text → Claude saves to disk
- For code/file tasks: use Agent (no subagent_type)

## Task Prompting Best Practices
- qwen3.5:35b: always say "at least 2000 words" (prevents thin output)
- deepseek-r1:32b: say "give rigorous step-by-step proof" (prevents boxed-answer-only)
- gemma4:26b: good for "survey X, list connections, brainstorm approaches"
- phi4:14b: good for "verify this calculation", "check this formula"
