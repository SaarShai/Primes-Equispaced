# Queue Submission: C/A Lower Bound + RH Conditional
Date: 2026-04-13

## Status: QUEUED

Both tasks appended to ~/Desktop/Farey-Local/M1MAX_NEXT_TASKS.txt.

---

## Task 1: M1_CA_LOWER_BOUND_QWEN
- Model: qwen3.5:35b
- Goal: Lower bound C/A >= c/log^2(p), using Bertrand primes b in [p/2,p-1], variance of non-identity permutations, PNT summation
- Key objects: C = (1/n'^2) Sum delta(f)^2, A = Sum D(f)^2 * (1/n^2 - 1/n'^2)
- Expected output: >= 2000 words, rigorous vs heuristic clearly separated

## Task 2: M1_DELTAW_RATIO_RH_CONDITIONAL
- Model: deepseek-r1:32b
- Goal: Use RH to analyze C/A ratio; determine if RH gives lower bound on Sum delta^2
- Key question: does RH imply C/A -> infinity or stay bounded?
- Expected output: step-by-step, each step labeled RH vs unconditional

---

## Verification
- grep confirms both task names appear exactly once in M1MAX_NEXT_TASKS.txt
- Format: MODEL|TASK_NAME|PROMPT (single line, pipe-separated) — matches existing format
