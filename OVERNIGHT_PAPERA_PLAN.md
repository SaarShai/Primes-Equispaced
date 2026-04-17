# Overnight Plan — Paper A Review
Date: 2026-04-15
Status: STAGED (not running yet)

## Goal
Comprehensive overnight review of Paper A ("Per-Step Analysis of Farey Sequence Uniformity")
before submission to Experimental Mathematics. Focus: adversarial proof checking, independent
reviews by multiple models, literature novelty confirmation, and comparison with successful papers.

## INFRASTRUCTURE FIXED (2026-04-15)
- Watchdogs were MISSING from crontab (explains M1 DEAD). Added:
  - `*/15 * * * * ~/bin/m1max_watchdog.sh` (restarts M1 runner if dead)
  - `*/15 * * * * ~/bin/m5max_watchdog.sh` (monitors M5)
  - `0 */2 * * * ~/bin/overnight_monitor_papera.sh` (overnight progress)
- M1 runner will auto-restart within 15 minutes of watchdog firing.

## What to do before running

1. Fix M1 runner (currently DEAD):
   ```bash
   nohup ~/bin/m1max_continuous.sh &
   ```
   Or wait for watchdog (runs every 15 min — next fire will restart it).

2. Clear existing queues (NDC tasks currently there — save if needed):
   ```bash
   cp ~/Desktop/Farey-Local/M1MAX_QUEUE.txt ~/Desktop/Farey-Local/M1MAX_QUEUE_NDC_BACKUP.txt
   cp ~/Desktop/Farey-Local/M5MAX_QUEUE.txt ~/Desktop/Farey-Local/M5MAX_QUEUE_NDC_BACKUP.txt
   > ~/Desktop/Farey-Local/M1MAX_QUEUE.txt
   > ~/Desktop/Farey-Local/M5MAX_QUEUE.txt
   ```

3. Move Paper A tasks from NEXT_TASKS to QUEUE:
   ```bash
   cat ~/Desktop/Farey-Local/M1MAX_NEXT_TASKS.txt >> ~/Desktop/Farey-Local/M1MAX_QUEUE.txt
   cat ~/Desktop/Farey-Local/M5MAX_NEXT_TASKS.txt >> ~/Desktop/Farey-Local/M5MAX_QUEUE.txt
   ```

4. Start/verify M5 runner:
   ```bash
   ~/bin/compute_control.sh start
   ```

5. Verify both running:
   ```bash
   ~/bin/compute_control.sh status
   ```

## Schedule (~8 hours, 23:00–07:00)

```
M1 Max: 10 tasks × ~45 min = ~7.5 hours
  T1  M1_PA_ADV_BRIDGE         (deepseek) adversarial Bridge Identity
  T2  M1_PA_ADV_DISPCOSINE     (deepseek) adversarial Displacement-Cosine
  T3  M1_PA_ADV_FOURTERM       (deepseek) adversarial four-term decomp
  T4  M1_PA_REVIEW_IDENTITIES  (qwen)     independent identities review
  T5  M1_PA_LIT_NOVELTY        (qwen)     literature novelty search
  T6  M1_PA_SIGN_ANALYSIS      (deepseek) sign theorem + counterexample
  T7  M1_PA_SPECTROSCOPE       (qwen)     spectroscope claim review
  T8  M1_PA_EXPMATH_COMPARE    (qwen)     compare to successful papers
  T9  M1_PA_REFEREE_SIM        (qwen)     referee simulation
  T10 M1_PA_ABSTRACT_INTRO     (qwen)     abstract + intro critique

M5 Max: 10 tasks × ~45 min = ~7.5 hours
  T11 M5_PA_LIT_FAREY          (gemma4)   literature: Farey discrepancy
  T12 M5_PA_LIT_MERTENS        (gemma4)   literature: Mertens + Farey
  T13 M5_PA_PROOFREAD_1        (qwen)     proofread sections 1-3
  T14 M5_PA_PROOFREAD_2        (deepseek) proofread sections 4-7
  T15 M5_PA_EXPMATH_PAPERS     (gemma4)   Experimental Mathematics examples
  T16 M5_PA_REFEREE_SIM2       (qwen)     second referee (different angle)
  T17 M5_PA_OPEN_QUESTIONS     (qwen)     open questions assessment
  T18 M5_PA_LEAN_REVIEW        (deepseek) Lean section claims review
  T19 M5_PA_FRAMING            (gemma4)   framing improvement suggestions
  T20 M5_PA_NOVELTY_FRAMEWORK  (qwen)     is per-step perspective truly new?
```

## Monitoring

- Check every 2 hours: `ls -lt ~/Desktop/Farey-Local/experiments/M1_PA_*.md ~/Desktop/Farey-Local/experiments/M5_PA_*.md 2>/dev/null`
- Check file sizes: `wc -c ~/Desktop/Farey-Local/experiments/M*_PA_*.md 2>/dev/null`
- Check runner logs: `tail -20 ~/Desktop/Farey-Local/experiments/M1MAX_CONTINUOUS_LOG.md`
- Morning review: read each result, update wiki, write revision tasks

## Success criteria
By morning:
- [ ] Bridge Identity adversarial: no gaps found, or specific gap identified
- [ ] Displacement-Cosine adversarial: proof verified or fixed
- [ ] Four-term adversarial: decomposition confirmed exact
- [ ] 2+ referee simulations with concrete revision suggestions
- [ ] Literature search: ΔW object confirmed novel, all cited papers verified real
- [ ] Spectroscope claims: honest assessment of what is/isn't proved
- [ ] Comparison with successful Experimental Mathematics papers: actionable lessons
- [ ] Proofreading: specific list of errors/ambiguities to fix

## NEXT STEPS (morning)
1. Read all 20 result files
2. Assess: substantial (>5KB good) vs thin (<2KB = reformulate)
3. Prioritize: what requires immediate Paper A revision?
4. Update wiki/log.md
5. Write targeted revision tasks for M1/M5 next cycle
