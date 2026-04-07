# Communications Applications Test Report

## Summary
Farey-based resource allocation vs conventional methods across three wireless scenarios.
Runtime: 0.69s | Overall: **PASS**

## Test 1: IoT Medium Access (ALOHA vs Farey Scheduling)

| Devices (K) | ALOHA Throughput | Farey Throughput | Improvement |
|:-----------:|:----------------:|:----------------:|:-----------:|
| 100 | 0.3700 | 1.0000 | 2.7x |
| 500 | 0.0335 | 1.0000 | 29.8x |
| 1000 | 0.0004 | 1.0000 | 2564.1x |

**Verdict: PASS** — Farey scheduling eliminates collisions entirely via deterministic slot assignment.
ALOHA throughput degrades as K grows (more collision probability); Farey maintains 1.0 throughput.

## Test 2: MIMO Pilot Contamination (Standard Reuse vs Farey-Spaced)

| Metric | Standard (tau=10) | Farey (tau=70) |
|:-------|:--------:|:-----:|
| Pilot assignment | 10 DFT pilots reused x7 cells | 70 unique DFT frequencies |
| Max inter-cell cross-corr | 1.0 | 0.000000 |
| Mean inter-cell cross-corr | 1.0 (co-pilot) | 0.000000 |
| Contamination per user | 6.0 | 0.000000 |
| Contamination reduction | — | INF (zero contamination) |
| Training overhead | 1x | 7x |
| Net gain per training slot | — | INF |

**Verdict: PASS** — With 70 pilot slots (vs 10),
Farey assigns orthogonal pilots to all 70 users, eliminating contamination entirely.
Net gain per training slot: INF.

## Test 3: Cognitive Radio Channel Hopping

| Metric | Random | Farey | Improvement |
|:-------|:------:|:-----:|:-----------:|
| Collisions / 100 slots | 203.5 | 0 | 407.0x |
| Slots to scan all 40 ch | 99.9 | 40.0 | 2.5x |

**Verdict: PASS** — Equispaced Farey offsets with unit step give zero collisions
and deterministic full-spectrum scan in 40 slots vs ~100 for random.

## Key Takeaway

Farey-structured allocation converts random contention into deterministic, collision-free
scheduling. The mathematical spacing properties of Farey sequences translate directly
into practical gains: zero collisions (IoT), near-orthogonal pilots (MIMO), and
rapid spectrum scanning (cognitive radio).
