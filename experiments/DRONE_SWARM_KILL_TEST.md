# DRONE SWARM KILL TEST: Farey Silent Coordination

**Date:** 2026-03-29
**Verdict: DIRECTION IS DEAD (4/5 kill tests triggered)**
**Simulation:** `drone_swarm_kill_test.py`

---

## Executive Summary

The Farey silent coordination concept for drone swarms fails 4 of 5 kill tests. The fundamental problem is that Farey scheduling requires **global agreement on fleet size N**, which itself requires communication -- defeating the core premise of "silent" coordination. Additionally, Farey slot spacing is **97x more drift-sensitive** than TDMA, and the utilization advantage over pre-planned TDMA is only 5.2% (not the claimed 15-25%).

**Only Test 5 survived**, and even that was conditional: Farey's deterministic zero-collision guarantee IS genuinely better than hash-based protocols like ZE-DTDMA, but only matters if the N-agreement problem is solved (which requires communication).

---

## Test Results

### Test 1: Utilization vs Pre-planned TDMA -- KILLED

| Method | Utilization |
|--------|------------|
| Pre-planned TDMA (100 fixed slots) | 90.0% |
| Farey scheduling | 95.2% |
| Adaptive TDMA (oracle) | 100.0% |

**Farey advantage: 5.2%** (below 10% kill threshold, far below claimed 15-25%)

The scenario tested dynamic fleet changes (80 -> 90 -> 85 -> 100 drones over 1000 time slots). Farey wastes slots because `|F_n|` rarely equals N exactly:
- 85 drones need F_17 (96 slots) = 11.5% wasted
- 90 drones need F_17 (96 slots) = 6.2% wasted
- 80 drones need F_16 (80 slots) = 0% wasted (lucky case)

**Why the original 15-25% claim was wrong:** It compared Farey to a worst-case TDMA that pre-allocates for peak fleet size and never adapts. But any real TDMA system would resize periodically. The fair comparison (Farey vs simple pre-planned TDMA) gives only ~5%.

### Test 2: Prime Constraint Overhead -- KILLED

If we require the Farey ORDER to be prime (for better equidistribution properties):
- **Max overhead: 61.7%** at fleet=60 (must use prime order 17 giving 97 slots)
- Even at moderate fleet sizes, prime-order overhead ranges 15-25%

General (non-prime) Farey order has max overhead of 16% at fleet=50. Still significant, but the prime constraint is devastating.

### Test 3: Off-by-One Fleet Size Disagreement -- KILLED

**The fatal flaw:** When drones disagree on N by just 1, and this causes the computed Farey ORDER to differ, collisions occur.

- At N=200: order changes from 25 to 26. Half-fleet disagreement caused **6 slot collisions**.
- Order boundaries occur at **6.2% of fleet sizes** in the 50-500 range (28 out of 450).
- When the Farey order is the same for N and N+1 (93.8% of cases), there are zero collisions.

**Why this kills the concept:** The whole point of "silent coordination" is no communication. But Farey scheduling REQUIRES every drone to agree on the exact same N. If one drone counts wrong (lost a beacon, joined late, etc.), schedules diverge at order boundaries and packets collide. You need a consensus protocol for N, which means you need communication -- defeating the purpose.

### Test 4: Clock Drift Sensitivity -- KILLED (most devastating)

| Metric | TDMA | Farey |
|--------|------|-------|
| Min gap between slots | 1.031 ms | 0.011 ms |
| Max tolerable drift | 0.516 ms | 0.005 ms |
| Drift tolerance ratio | 100% | **1.0%** |

Farey slots at order 18 (for 97 drones in 100ms frame) have a minimum gap of just 0.011ms -- nearly **100x smaller** than TDMA's uniform 1.03ms gap. This means:

- At 0.01ms drift: TDMA has 0% collisions, Farey has **100%** collisions
- At 0.1ms drift: TDMA still has 0% collisions, Farey has **100%** collisions
- Farey only matches TDMA when drift is so large (0.5ms+) that both systems fail

**This is a fundamental structural problem.** Farey fractions are NOT uniformly spaced. The three-distance theorem guarantees at most 3 distinct gap sizes for irrational rotations, but Farey sequences have 96 distinct gap sizes for order 18. The smallest gaps are catastrophically small.

**Real-world implication:** GPS-disciplined clocks achieve ~20ns accuracy, but cheaper oscillators drift by microseconds to milliseconds. Any practical drone swarm would need sub-microsecond synchronization to use Farey scheduling, which is far more demanding than TDMA requires.

### Test 5: ZE-DTDMA Comparison -- SURVIVED (CONDITIONAL)

Farey DOES have a genuine advantage over hash-based distributed TDMA:

| Property | Farey | ZE-DTDMA |
|----------|-------|----------|
| Zero communication | YES | YES |
| Deterministic (no collisions) | YES | NO |
| Dynamic membership | PARTIAL (needs N) | YES |
| Works without knowing N | NO | YES |
| Crypto security | NO | YES |
| Utilization (97 drones) | 95.1% | 53.3% |

ZE-DTDMA suffers heavy birthday-paradox collisions (~29 per frame with 97 drones and 128 slots). Farey's mathematical guarantee of zero collisions is real and valuable.

**But this advantage is conditional:** It only matters if the N-agreement problem (Test 3) can be solved without communication. If solving N-agreement requires a broadcast, you might as well use adaptive TDMA.

---

## Honest Assessment

### What Farey scheduling genuinely offers:
1. **Mathematically guaranteed zero collisions** (no other distributed protocol has this)
2. **Provably equidistributed slot positions** (from number theory)
3. **No hash function or crypto overhead**
4. **Higher utilization than hash-based protocols** (95% vs 53% for ZE-DTDMA)

### What kills it in practice:
1. **N-agreement is the Achilles heel.** Silent coordination that requires fleet-size consensus isn't truly silent.
2. **Clock drift sensitivity is 100x worse than TDMA.** The non-uniform gaps in Farey sequences create tiny gaps that are catastrophically sensitive to timing errors.
3. **Utilization advantage over TDMA is only 5%**, not 15-25% as originally claimed.
4. **Prime-order overhead** is impractical (up to 62% wasted slots).

### Could the concept be salvaged?
Partially, with significant modifications:
- Use Farey fractions only for the **equidistribution** property, not the scheduling structure
- Combine with a lightweight beacon-count protocol for N-agreement
- Add guard intervals between Farey slots to handle drift (but this reduces the utilization advantage)
- Use a FIXED Farey order (e.g., always F_41 with 530 slots) to avoid the N-agreement problem -- but then you're just using a precomputed lookup table, not "Farey scheduling"

### Bottom line:
The direction has **genuine mathematical elegance** but **fatal engineering flaws**. The N-agreement problem and clock drift sensitivity are not minor issues -- they are fundamental to the concept's viability. A paper claiming "silent coordination via Farey sequences" would be immediately challenged on these points by any wireless systems reviewer.

**Recommendation: Do not pursue this direction further.** The mathematical properties of Farey sequences are real, but they do not map well to the drone swarm scheduling problem. The constraints of real-world wireless (clock drift, fleet uncertainty, adversarial environments) are incompatible with Farey's requirements (exact N, exact timing, public slot assignments).

---

## Classification (Aletheia Framework)

- **Autonomy:** Level A (autonomous analysis)
- **Significance:** Level 0 (the approach doesn't work; knowing it doesn't work is useful but not publishable)
- **Verification status:** Fully validated (kill tests are conclusive)
