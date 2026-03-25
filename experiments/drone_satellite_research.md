# Farey Scheduling for Drone Swarms & Satellite Constellations

**Date:** 2026-03-25
**Purpose:** Honest assessment of whether Farey-based scheduling offers real engineering value

---

## PART 1: DRONE SWARMS -- What They Actually Use Today

### Current Protocols

**MAVLink** is the dominant open-source protocol for drone communication. It handles
telemetry and command/control between drones and ground stations. It was designed
for point-to-point links, not swarm coordination, so swarms layer additional
protocols on top.

**Mesh networking** is the trend for decentralized swarms. Recent systems include:
- Meshtastic + DroneBridge32: mesh networking for swarm coordination, geofencing,
  and emergency landing
- MAVLink over Reticulum: encrypted zero-trust mesh transport (Beechat, 2025)
- Blockchain-based formation control using smart contracts for registration,
  identity, and positional coordination

### The Real Coordination Challenges

1. **Collision avoidance** -- Drones share positions and planned trajectories via
   mesh network, then compute repulsion vectors. This is the #1 priority.

2. **MAC layer (who talks when)** -- When 20+ drones share a radio frequency,
   they need a protocol to avoid transmitting at the same time. This is where
   TDMA matters.

3. **Bandwidth sharing** -- Short-range, low-bandwidth neighbor-to-neighbor
   communication is sufficient. Drones only need to talk to nearby drones,
   not the whole swarm.

4. **Decentralized agreement** -- No central controller. Drones must self-organize
   time slots, routes, and formations using only local information.

### How Drones Currently Handle TDMA

Several research approaches exist:

- **DTSA (Dynamic Time Slot Allocation):** Quadcopters share channel access in a
  non-periodic, decentralized manner. Nodes build a local topology database and
  pick slots to avoid conflicts.

- **Coalition game-based allocation:** Distributed game theory where drones negotiate
  slot ownership.

- **CSMA/TDMA hybrid:** A CSMA (listen-before-talk) phase discovers neighbors,
  then a centralized phase assigns TDMA slots, then pure TDMA runs.

**Key problem with all of these:** They require communication rounds to agree on
who gets which slot. The more drones, the more coordination overhead. Fixed TDMA
avoids conflicts but wastes slots. Dynamic TDMA adapts but requires negotiation.

### Could Farey Scheduling Help Here?

**The Farey TDMA idea:** Each drone with index k in a swarm of p drones transmits
at times aligned to k/p. The injection principle guarantees that when a new drone
(the p-th, where p is prime) joins, its transmission times fall into gaps between
existing transmissions. No coordination needed -- the drone just needs to know
its index and the swarm size.

**What would actually need to happen for a firmware engineer to use this:**

1. Each drone gets a unique index k (1 to p-1) at boot or via a lightweight
   discovery protocol
2. The frame period T is divided so drone k transmits at time offsets
   proportional to k/p within each frame
3. When the swarm grows to the next prime size, new drones pick slots at k/p_new
4. The injection principle guarantees no collision with existing slots

**Specific advantages:**
- Zero negotiation overhead for slot assignment (just compute k/p)
- Deterministic -- no randomness, no retries, no collision resolution
- The minimum gap between any two slots is exactly 1/(p*(p-1)), which is
  predictable and worst-case bounded

**Specific limitations -- and these are serious:**

1. **Swarm size must be prime.** Real swarms have arbitrary sizes (4, 10, 37
   drones). You would need to round up to the next prime, wasting slots for
   non-existent drones. For a 10-drone swarm, you'd use p=11, wasting 1 slot.
   Not terrible, but awkward.

2. **The injection guarantee only works when growing to the NEXT prime.**
   If you go from 7 drones to 11 drones, the intermediate sizes (8, 9, 10)
   don't have the same mathematical guarantee. You'd need to treat 8-10 as
   "using some slots from the p=11 frame."

3. **Drones join and leave dynamically.** The Farey model assumes you add a
   whole new prime layer at once. A single drone joining mid-mission doesn't
   map cleanly to "adding all fractions with denominator p."

4. **Existing TDMA solutions already work.** DTSA and similar protocols handle
   dynamic join/leave with 1-2 communication rounds. The overhead of those
   rounds is small (milliseconds). Farey scheduling saves you those milliseconds
   but adds the constraint of prime-sized frames.

5. **Spatial reuse is the real win.** In multi-hop swarms, two drones far apart
   can transmit simultaneously because their signals don't interfere. Farey
   scheduling doesn't address spatial reuse at all -- it's a single-channel model.

---

## PART 2: SATELLITE CONSTELLATIONS -- What They Actually Use Today

### Current Architecture

**Starlink:**
- ~7,000+ satellites in LEO with laser inter-satellite links (ISLs)
- Ku-band downlink to users: frames divided into 302 time-division intervals
  of 4.4 microseconds each, 750 frames/second
- Beamforming + TDMA for managing concurrent ground users
- ISL routing is a major research problem: end-to-end latency is dominated
  by propagation delay and is proportional to network diameter

**Iridium:**
- 66 satellites with Ka-band inter-satellite links
- Each satellite maintains 4 quasi-permanent ISLs (2 intra-plane, 2 inter-plane)
- Originally designed with static scheduling, later switched to dynamic routing
  and channel selection
- Unique in relaying data satellite-to-satellite (most competitors route
  everything through ground stations)

**OneWeb:**
- Currently has NO inter-satellite links -- all traffic goes ground-station
  to satellite to ground-station. This makes handoff between satellites
  the dominant challenge.

### The Real Bottlenecks

1. **Handoff complexity:** LEO satellites move fast. A ground user's connection
   must switch between satellites every few minutes. The handoff decision is
   NP-hard to optimize globally. Current systems make local decisions at each
   handoff event.

2. **ISL link scheduling:** Which satellite talks to which neighbor in which
   time slot. This is MF-TDMA (multi-frequency TDMA) and is computationally
   expensive -- the scheduling problem is NP-hard.

3. **Beam scheduling latency:** Each satellite serves multiple ground beams.
   Scheduling which beam gets which time slot creates fronthaul latency
   proportional to user count.

4. **Topology dynamics:** ISL links break and reform as orbital geometry changes.
   Routing must adapt continuously.

### Could Farey Scheduling Help Here?

**The idea:** Assign satellite communication slots based on Farey fractions.
Satellite i in a constellation of p satellites transmits on ISL at time i/p.
When new satellites are added (to the next prime count), they slot in without
conflicting with existing assignments.

**Where it MIGHT have value:**

- **Reducing handoff coordination:** If beam time slots follow a Farey pattern,
  a user being handed from satellite A to satellite B could predict its new
  slot position without a signaling exchange. The slot assignment is implicit
  in the satellite's index.

- **Constellation growth:** Starlink adds satellites regularly. If existing slot
  assignments are based on F_p and new satellites are at the next prime, the
  injection principle means no existing satellite's schedule changes. This is
  a real advantage over schemes that require global re-scheduling when the
  constellation grows.

**Where it DOESN'T help (and these dominate):**

1. **The bottleneck is routing, not slot assignment.** The hard problem in satellite
   networks is choosing WHICH satellites to route through, not WHEN each satellite
   transmits. Farey scheduling addresses timing, not routing. The routing problem
   is what consumes engineering effort and compute cycles.

2. **MF-TDMA is already mature.** Existing satellite systems use sophisticated
   MF-TDMA with interference-aware scheduling that accounts for beam patterns,
   frequency reuse, and geographic coverage. Farey scheduling is a 1D timing
   model that ignores all of these dimensions.

3. **Constellation sizes aren't prime.** Starlink has ~7,000 satellites. Iridium
   has 66. Neither is prime. You'd need to embed these into the nearest prime,
   wasting capacity. For Iridium (66 -> 67, which is prime), the waste is tiny.
   For Starlink at arbitrary counts, it's manageable but adds complexity for
   no clear gain over existing methods.

4. **Physical constraints dominate.** ISL link distance, line-of-sight, orbital
   mechanics, and hardware limits (how many laser links per satellite) are the
   real constraints. Time slot assignment is a solved sub-problem within these
   constraints.

5. **Latency optimization needs topology-awareness.** Recent research focuses on
   minimizing network diameter through ISL topology design. This is a graph
   theory problem about which links to establish, not about when to use them.

---

## PART 3: HONEST ASSESSMENT

### Drone Swarms

| Aspect | Assessment |
|--------|-----------|
| **Mathematical elegance** | Genuine. The zero-coordination, zero-collision guarantee from the injection principle is mathematically clean. |
| **Practical advantage over DTSA** | Marginal. Saves 1-2 ms of negotiation per join event. Not a bottleneck in practice. |
| **Implementation complexity** | Low -- just compute k/p. But the prime-size constraint adds awkwardness. |
| **What engineers actually need** | Spatial reuse, dynamic join/leave, variable-rate slots, priority classes. Farey scheduling provides none of these. |
| **Would an engineer use this?** | Unlikely as a primary protocol. Possibly as a fallback for initial slot assignment before negotiation completes -- a "day zero" schedule that works immediately. |

**Honest verdict:** It's a neat mathematical property (zero-coordination collision freedom)
that solves a sub-problem that isn't the main bottleneck. Drone engineers spend their
time on collision avoidance algorithms, mesh routing, and mission planning -- not on
MAC-layer slot negotiation.

**One genuinely useful niche:** GPS-denied or radio-silent scenarios where drones
CANNOT communicate to negotiate slots. If drones must maintain radio silence but still
need to take turns transmitting (e.g., military scenarios), a pre-agreed Farey schedule
lets them coordinate without any transmissions. This is a real, if narrow, use case.

### Satellite Constellations

| Aspect | Assessment |
|--------|-----------|
| **Mathematical elegance** | Same as drones -- the injection principle is real math. |
| **Practical advantage over MF-TDMA** | Minimal. MF-TDMA already handles slot assignment well. The hard problems are elsewhere. |
| **Constellation growth benefit** | This is the strongest point. Adding satellites without re-scheduling existing ones is valuable. But existing systems handle this with reserved capacity pools. |
| **What engineers actually need** | Better routing algorithms, topology optimization, handoff prediction, interference management. |
| **Would an engineer use this?** | No. The problem Farey scheduling solves (1D time slot assignment) is not what satellite engineers are struggling with. |

**Honest verdict:** Satellite communication scheduling is a multi-dimensional problem
(time, frequency, beam direction, spatial reuse, routing topology). Farey scheduling
addresses one dimension (time) in a way that's mathematically elegant but practically
redundant -- existing TDMA implementations already handle time slot assignment, and
the real engineering challenges are in the other dimensions.

### Overall: Mathematical Curiosity or Engineering Tool?

**Mostly a mathematical curiosity for these specific domains.** Here's why:

1. The injection principle gives a CLEAN THEORETICAL PROPERTY (coordination-free
   collision avoidance) that's intellectually satisfying.

2. But the engineering problems in both drones and satellites are dominated by
   challenges that Farey scheduling doesn't address: routing, spatial reuse,
   interference management, dynamic topology, and multi-dimensional resource
   allocation.

3. The prime-number constraint is a persistent practical annoyance with no
   engineering benefit.

4. Existing protocols (DTSA, MF-TDMA) solve the slot assignment sub-problem
   adequately, and they handle the additional dimensions (frequency, space)
   that Farey scheduling ignores.

**Where Farey scheduling IS genuinely interesting (outside drones/satellites):**

- **Frequency-hopping spread spectrum:** FHSS already uses number-theoretic
  constructions for hop sequences. Coprime-based one-coincidence sequences
  (which are related to Farey structure) are used in practice. This is the
  closest real-world relative.

- **Distributed sensor networks with no communication:** Sensors that must
  wake up in non-colliding patterns without being able to talk to each other.
  Same niche as the radio-silent drone scenario.

- **As a theoretical benchmark:** The Farey schedule provides a provably
  optimal (in a specific sense) collision-free assignment that other
  heuristic protocols can be compared against.

---

## Summary for the Project

**Do not oversell Farey scheduling for drones or satellites.** The math is real,
but the engineering value is marginal because:
- It solves a sub-problem (1D time slot assignment) that isn't the bottleneck
- It ignores the dimensions that matter most (space, frequency, routing)
- Existing protocols handle this sub-problem adequately
- The prime-number constraint adds friction with no compensating benefit

**The honest framing:** Farey scheduling is a coordination-free TDMA scheme with
a provable collision-avoidance guarantee. It is most interesting as a theoretical
contribution to distributed scheduling, and has a narrow practical niche in
scenarios where zero communication is available for coordination (radio-silent
operations, pre-agreed schedules). It should not be positioned as a replacement
for existing drone or satellite communication protocols.

---

## Sources

### Drone Swarm Protocols
- [Decentralized Swarm Management via MAVLink (IEEE)](https://ieeexplore.ieee.org/document/7781964/)
- [MAVLink over Reticulum -- Zero Trust Drone C2 (Beechat, 2025)](https://beechat.network/2025/10/24/beechat-network-systems-unveils-mavlink-over-reticulum-toward-zero-trust-drone-command-control/)
- [Collision Avoidance for Drone Swarms (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11858889/)
- [Distributed TDMA for Autonomous Aerial Swarms](https://napier-repository.worktribe.com/OutputFile/3595881)
- [TDMA Slot Allocation for UAV Formations (Canterbury)](https://ir.canterbury.ac.nz/bitstreams/049b7dc1-192b-4d42-8def-2b426840dad1/download)
- [Dynamic Time Slot Allocation for UAV Formation (Nature)](https://www.nature.com/articles/s41598-025-30533-0)
- [Slot Allocation via Coalition Games (MDPI)](https://www.mdpi.com/1099-4300/27/3/256)
- [Decentralized UAV Swarm Control Design (Springer)](https://link.springer.com/article/10.1007/s42452-024-06408-w)

### Satellite Communication
- [Starlink Latency Improvements (SpaceX)](https://starlink.com/public-files/StarlinkLatency.pdf)
- [Inter-Satellite Link Configuration for LEO (arXiv)](https://arxiv.org/html/2511.15861v1)
- [Time-varying Bottleneck Links in LEO Networks (NDSS)](https://www.ndss-symposium.org/wp-content/uploads/2025-109-paper.pdf)
- [MF-TDMA Scheduling for Multi-Spot Beam Satellites (ResearchGate)](https://www.researchgate.net/publication/329820278_MF-TDMA_Scheduling_Algorithm_for_Multi_Spot_Beam_Satellite_Systems_Based_on_Co-Channel_Interference_Evaluation)
- [Enhancing LEO Constellations with ISLs (arXiv)](https://arxiv.org/html/2406.05078v1)
- [Iridium Satellite Constellation (Wikipedia)](https://en.wikipedia.org/wiki/Iridium_satellite_constellation)
- [Optimal Handover in LEO Networks (arXiv)](https://arxiv.org/html/2512.02449v1)
- [Dynamic Routing in Satellite Networks (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9231381/)

### Number Theory and Scheduling
- [Coprime FH Sequence Construction (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11592906/)
- [Combinatorial Algorithm for TDMA Scheduling (Springer)](https://link.springer.com/article/10.1007/s10589-007-9143-8)
- [TDMA Scheduling for Wireless Sensor Networks (Berkeley)](https://people.eecs.berkeley.edu/~varaiya/papers_ps.dir/tdmaschedule.pdf)
