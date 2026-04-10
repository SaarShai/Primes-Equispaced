# Farey Scheduling for Data Centers: Honest Assessment

**Date:** 2026-03-29
**Verdict:** Marginal gain over existing solutions. The problem is largely already solved.

## Executive Summary

Farey-based "silent coordination" for data center scheduling provides **zero-collision deterministic scheduling with zero cascading on node changes**. However, this combination is NOT unique to Farey sequences. Consistent hashing already provides zero-disruption node addition/removal, and simple midpoint bisection provides both zero cascading AND better spacing than Farey mediants. The specific Farey/Stern-Brocot mediant insertion actually produces WORSE spacing quality than trivial alternatives. The claimed benefits are real but overstated: the problem of distributed coordination without communication is well-studied, and existing solutions (jitter, consistent hashing, TDMA) handle it adequately in practice. There may be a narrow niche for the formal guarantees, but it does not justify "zero communication overhead with guaranteed non-collision" as a novel contribution.

## Problem Statement

N nodes in a data center need to access a shared resource (or perform periodic tasks) without colliding with each other, ideally without a central coordinator, and with minimal disruption when nodes are added or removed.

## Current Solutions and Their Limitations

### 1. Random Jitter (Industry Standard)
- **How it works:** Each node adds a random delay (jitter) to its scheduled time.
- **Collision rate:** Birthday problem applies. With N=1000 nodes and T=10000 time slots, P(collision) approaches 1.0. With wider jitter windows (T=100*N), collision rate drops to negligible levels.
- **In practice:** YouTube, PayPal, Facebook all use jitter. The 10% jitter technique (e.g., 3600 +/- 300 seconds for hourly tasks) converts 10,000 simultaneous requests into approximately 14 per second, which is entirely manageable.
- **Disruption on node change:** Zero -- new nodes just pick a random offset.
- **Weakness:** Probabilistic, not deterministic. Collisions are rare but possible.

### 2. TDMA / Round-Robin (Equal Spacing)
- **How it works:** Assign node i to time slot i/N.
- **Collision rate:** Zero by construction.
- **Spacing quality:** Perfect (max/min gap ratio = 1.0).
- **Disruption on node change:** Catastrophic -- adding 1 node to N requires ALL N nodes to shift from i/N to i/(N+1). In our simulation, 99%+ of nodes must change their schedule.
- **Weakness:** Cannot handle dynamic membership without global reconfiguration.

### 3. Consistent Hashing (Distributed Systems Standard)
- **How it works:** Hash each node to positions on a ring [0,1). Each node owns the arc clockwise to the next node. With virtual nodes (150+ per physical node), load is approximately balanced.
- **Collision rate:** Depends on application -- nodes own different arcs, so if used for time-slot assignment, no collisions.
- **Disruption on node change:** Only ~1/N of keys (time slots) are remapped. Existing node positions do NOT change.
- **Spacing quality:** Poor -- max/min gap ratio of 792:1 at N=100 (our measurement). Virtual nodes help but don't eliminate the variance.
- **Weakness:** Uneven spacing; requires virtual nodes for decent balance.

### 4. Centralized Coordinators (Paxos, Raft)
- **How it works:** A leader assigns schedules. Replicas ensure availability via consensus.
- **Examples:** Google Cron Service (Paxos-based), Dkron (Raft-based), Kubernetes CronJobs.
- **Collision rate:** Zero -- the coordinator prevents them.
- **Disruption on node change:** Zero -- the coordinator reassigns.
- **Weakness:** Requires communication. Leader election takes time. Adds latency and a dependency. Google notes that Paxos communication must be synchronous, adding overhead to every cron launch.

### 5. Fastpass / pFabric (Network-Level TDMA)
- **How it works:** Centralized arbiter assigns time slots for packet transmission. Achieved 240x reduction in queue lengths at Facebook.
- **Weakness:** Requires centralized arbiter. pFabric requires specialized hardware.

## Farey Scheduling: How It Works

Assign node i a position in [0,1) using Stern-Brocot mediant insertion:
1. Start with boundaries 0/1 and 1/1.
2. First node gets position 1/2 (mediant of 0/1 and 1/1).
3. Second node gets 1/3 or 2/3 (mediant into largest gap).
4. Continue: each new node inserts at the mediant of the two fractions bounding the largest gap.

**Key property claimed:** Adding node N+1 does not change the positions of nodes 1..N (zero cascading).

## What's Novel (Honest Assessment)

| Claim | Verdict | Explanation |
|-------|---------|-------------|
| Zero collision by construction | NOT NOVEL | TDMA, any deterministic scheme achieves this |
| Equidistribution of positions | NOT NOVEL | Classical result (Franel 1924). And Farey mediants are WORSE than TDMA |
| Zero cascading on node add/remove | PARTIALLY NOVEL as application | Zero cascading follows from Stern-Brocot tree structure (1858). But applying it to distributed scheduling may be a new framing |
| Zero cascading + good spacing | THE ACTUAL CLAIM | This is the combination no single existing method provides. But "good" spacing is debatable (see below) |
| Monotonically improving quality | NEEDS PROOF | If the Sign Theorem proves quality never degrades on node addition, this may be genuinely novel |

### Critical Finding: Mediant Insertion Has POOR Spacing

Our simulation reveals that Stern-Brocot mediant insertion produces **dramatically worse** spacing than alternatives:

| Method | Max/Min Gap Ratio (N=100) |
|--------|--------------------------|
| TDMA | 1.00 (perfect) |
| Midpoint bisection | 2.00 |
| Consistent hashing | 792 |
| **Farey mediant** | **69.0** |
| Random | 1925 |

Farey mediant insertion is 69x worse than TDMA and 34.5x worse than simple midpoint bisection. This is because mediants like (a+c)/(b+d) are NOT midpoints -- they cluster toward simpler fractions, producing uneven spacing.

**Simple midpoint bisection** (insert at the exact center of the largest gap) ALSO has zero cascading AND achieves a max/min ratio of only 2.0. This means the "Farey" part of Farey scheduling actually makes the spacing WORSE compared to trivial bisection.

### What Actually Matters: The Comparison Matrix

| Property | TDMA | Consistent Hash | Midpoint Bisection | Farey Mediant | Random+Jitter |
|----------|------|----------------|-------------------|---------------|---------------|
| Zero collisions | Yes | Yes* | Yes | Yes | No (rare) |
| Good spacing | Perfect | Poor | Very Good | Poor | Fair |
| Zero cascading | No (100% disruption) | Yes | Yes | Yes | Yes |
| No coordinator | Yes | Yes | Yes | Yes | Yes |
| Formal guarantees | Yes | Probabilistic | Yes | Yes | No |
| Number-theoretic elegance | No | No | No | Yes | No |

*Consistent hashing achieves zero collisions if nodes own exclusive time arcs.

**Midpoint bisection dominates Farey mediant on every practical metric** while also having zero cascading. The only advantage of Farey is number-theoretic structure (rational positions, connection to Stern-Brocot tree, potential for formal proofs about asymptotic behavior).

## Quantitative Results (Simulation)

### Collision Counts (1000 cycles, time resolution = 1/(2N))

| N | Random | TDMA | Consistent Hash | Farey |
|---|--------|------|----------------|-------|
| 10 | 2000 | 0 | 2000 | 1000 |
| 50 | 9000 | 0 | 9000 | 10000 |
| 100 | 22000 | 0 | 25000 | 25000 |
| 500 | 100000 | 0 | 108000 | 179000 |
| 1000 | 210000 | 0 | 214000 | 399000 |

**Farey has MORE collisions than random at high N** because its uneven spacing causes multiple nodes to land in the same time bucket. This is a direct consequence of the poor spacing quality.

### Disruption on Node Addition (1 node added)

| N | Farey | TDMA | Consistent Hash |
|---|-------|------|----------------|
| 10 | 0% | 90% | 0% |
| 50 | 0% | 98% | 0% |
| 100 | 0% | 99% | 0% |
| 500 | 0% | 99.8% | 0% |

Farey and consistent hashing BOTH achieve 0% disruption. This is not a differentiator.

## Use Case Analysis

### a) Distributed Cron (N machines, hourly tasks)
- **Current solution:** Random jitter (industry standard). Google uses Paxos-based cron.
- **Farey advantage:** Deterministic zero collision.
- **Honest assessment:** Jitter works. With 10% jitter on a 1-hour window, 1000 machines spread across 12 minutes = 1.4 tasks/second. No real-world system is bottlenecked by this. Farey solves a problem that doesn't really exist in practice.

### b) Cross-DC Replication Timing
- **Current solution:** CRDTs, vector clocks, configurable sync intervals.
- **Farey advantage:** Deterministic sync windows.
- **Honest assessment:** With 3-5 data centers, you can trivially schedule them manually. The coordination overhead of CRDTs is in conflict RESOLUTION, not collision AVOIDANCE. Farey addresses the wrong problem -- it prevents simultaneous sync, but the real cost is state divergence and reconciliation.

### c) Log/Metrics Aggregation (1000 agents, shared TSDB)
- **Current solution:** Random flush intervals, or agent-side buffering.
- **Farey advantage:** Zero write contention.
- **Honest assessment:** Modern time-series databases (InfluxDB, Prometheus, ClickHouse) handle concurrent writes at massive scale. Write contention is not the bottleneck -- it's disk I/O and compaction. Spreading writes evenly might help marginally with burst load, but TSDBs are already designed for this.

### d) Health Check / Monitoring (N probes, M services)
- **Current solution:** Randomized intervals + exponential backoff.
- **Farey advantage:** Predictable, even load distribution.
- **Honest assessment:** This is probably the STRONGEST use case. Thundering herd on health checks can cause false-positive outage alerts. But even here, simple randomized intervals with a spread window work well enough.

## Patent Landscape

No patents were found using Farey sequences, Stern-Brocot trees, or mediants for scheduling or resource allocation. The patent space appears open. However:

1. The lack of prior patents may indicate lack of commercial interest rather than untapped opportunity.
2. A patent on "mediant insertion for distributed scheduling" would be narrow and easily designed around (use midpoint bisection instead, which is better anyway).
3. Consistent hashing patents (Akamai, 1998) already cover the zero-disruption scheduling space.

## Limitations and Honest Caveats

### The Hard Truth

1. **The problem is already well-solved.** Random jitter, consistent hashing, and centralized coordinators handle every realistic data center scenario. No operator is suffering from the specific combination of problems Farey scheduling addresses.

2. **Farey mediant insertion produces poor spacing.** The max/min gap ratio of 69:1 at N=100 means some nodes are crammed together while others have huge gaps. This is WORSE than random (with more nodes in the same bucket). Simple midpoint bisection beats Farey on every metric except number-theoretic elegance.

3. **"Zero communication" is misleading.** Every method except TDMA achieves zero communication for node addition. The comparison should be "Farey vs. consistent hashing" (both have zero disruption), not "Farey vs. centralized coordinator."

4. **The Sign Theorem / monotonic improvement claim needs scrutiny.** If this is truly about Farey mediants, the worsening max/min ratio (from 6:1 at N=5 to 267:1 at N=500) contradicts "quality improves monotonically" in the spacing sense. It may hold in some other sense (e.g., asymptotic equidistribution), but that's a classical result.

5. **No real-world validation.** All claims are theoretical or simulated. No production system uses Farey scheduling, and no benchmark shows it outperforming existing solutions on real workloads.

### Where Farey MIGHT Have Value (Narrow Niches)

1. **Formal verification scenarios:** If you need a PROVABLY correct schedule with guaranteed bounds (e.g., safety-critical systems), the number-theoretic structure of Farey sequences enables formal proofs that random jitter cannot provide.

2. **Embedded systems without randomness:** Systems with no random number generator (some microcontrollers) could use Farey positions computed from node IDs via rational arithmetic.

3. **Mathematical framework for analysis:** Even if Farey scheduling isn't practically superior, it provides a clean framework for ANALYZING distributed scheduling quality, connecting to deep results in number theory.

## Comparison Table: Farey vs. SOTA

| Metric | Random+Jitter | TDMA | Consistent Hash | Farey Mediant | Midpoint Bisection |
|--------|--------------|------|----------------|---------------|-------------------|
| Collisions | Rare | Zero | Zero* | Zero** | Zero |
| Spacing quality | Fair | Perfect | Poor | Poor | Very Good |
| Disruption on add | 0% | ~100% | 0% | 0% | 0% |
| Communication needed | None | None | None | None | None |
| Implementation complexity | Trivial | Trivial | Moderate | Moderate | Trivial |
| Formal guarantees | None | Full | Probabilistic | Full | Full |
| Production deployment | Everywhere | Common | Everywhere | None | Rare |
| Handles heterogeneous nodes | Yes (weight jitter) | Yes (multi-slot) | Yes (virtual nodes) | Unclear | Unclear |

*With exclusive time arcs. **Only at exact rational positions; poor spacing causes bucket collisions in discrete time.

## Recommended Next Steps

1. **Do NOT pursue Farey scheduling for data centers as a standalone contribution.** The gain over existing solutions is marginal to nonexistent, and the spacing quality issue undermines the core value proposition.

2. **If pursuing this, pivot to midpoint bisection** as the practical algorithm, with Farey/Stern-Brocot theory providing the analytical framework. Midpoint bisection has strictly better spacing while retaining zero cascading.

3. **The strongest publishable angle** is not the application but the THEORY: formally proving bounds on spacing quality under dynamic node insertion using Stern-Brocot structure. This is a math contribution, not a systems contribution.

4. **For patent purposes:** The patent space is open but the claim would be narrow. A patent on "hierarchical bisection scheduling with number-theoretic analysis" might have more substance than raw "Farey scheduling."

5. **If pursuing application papers:** Target formal-methods or safety-critical-systems venues where provable guarantees matter more than raw performance. General systems venues (SOSP, OSDI, NSDI) will reject this because the baselines (jitter, consistent hashing) already work.

## Classification (Aletheia Framework)

- **Autonomy:** Level A (AI-generated analysis)
- **Significance:** Level 0-1 (the application framing is not sufficiently novel for publication; the problem is already solved by existing methods)
- **Verification status:** Simulation-verified, but the negative finding (Farey spacing is poor) is the main result

## Bottom Line

The "silent coordination" claim is technically correct but practically irrelevant. The data center scheduling problem is already well-solved by simpler methods. Farey mediant insertion specifically has a spacing quality problem that makes it worse than trivial alternatives (midpoint bisection) that share all its other desirable properties. The research value lies in the mathematical framework, not the application.
