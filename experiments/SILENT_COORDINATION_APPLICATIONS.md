# Silent Coordination Applications: Honest Assessment

**Date:** 2026-03-29
**Status:** Unverified -- needs adversarial review
**Connection:** Novel Discovery N1 (Farey injection), N2 (M(p) correlation)

---

## 1. The Claimed Unique Advantage

Farey-Prime Scheduling allows N agents to independently compute compatible,
non-colliding time slots from just (agent_id k, group_size p) with:
- **Zero communication** -- no message exchange at any point
- **Deterministic** -- every agent computes the same schedule independently
- **Non-colliding** -- mathematically guaranteed, formally verified in Lean 4
- **Monotone scaling** -- F_N is a subset of F_{N+1}, so adding agents never
  disrupts existing assignments

The question: **where does this combination actually beat existing solutions?**

---

## 2. Competitive Landscape (Honest Assessment)

### 2.1 DESYNC / Firefly-Inspired Protocols
- **What they do:** Nodes broadcast periodic "firing" messages and self-organize
  into evenly-spaced TDMA slots. Converges in ~8 rounds for small networks.
- **Strengths:** Self-adjusting, no global clock, >90% bandwidth utilization,
  adapts to node arrivals/departures automatically.
- **Weakness vs Farey:** Requires multiple communication rounds to converge.
  Each node must hear neighbors' firing messages. NOT zero-communication.
  Convergence takes O(log N) rounds minimum.
- **Farey advantage:** Genuine. DESYNC needs communication; Farey needs none.
  In strict EMCON or acoustic-limited environments, DESYNC cannot operate.

### 2.2 SOTDMA / STDMA (Self-Organized TDMA)
- **What they do:** Each node broadcasts its next slot reservation as part of
  its current transmission. Used in AIS (marine vessel tracking) and aviation
  VDL Mode 4.
- **Strengths:** Proven in real-world maritime/aviation systems. Standardized.
- **Weakness vs Farey:** Requires GPS for time synchronization. Each node must
  transmit to announce its slot reservation -- NOT zero-communication. Adding
  a new node requires it to listen to existing traffic first.
- **Farey advantage:** Genuine. SOTDMA requires both GPS and at least one
  communication round. Farey requires neither.

### 2.3 CRT-Based Topology-Transparent Scheduling (TTS)
- **What they do:** Use Chinese Remainder Theorem to assign transmission slots
  that guarantee collision-free communication regardless of network topology.
  Each node needs only its ID and a global parameter (N or max degree).
- **Strengths:** No topology knowledge needed. Mathematically guaranteed.
  Well-studied (Su 2015, GCRT extensions 2016).
- **THIS IS THE CLOSEST COMPETITOR.** CRT-TTS is also deterministic, requires
  only local computation from (node_id, N), and guarantees collision-freedom.
- **Key differences from Farey:**
  - CRT-TTS addresses multi-hop collision avoidance (distance-2 coloring),
    while Farey addresses single-channel TDMA
  - CRT-TTS frame length grows as O(N^2) or worse; Farey slots are O(1/N)
    within a fixed [0,1) interval
  - CRT-TTS does NOT have the monotone scaling property -- changing N
    requires recomputing all schedules
  - CRT-TTS requires knowledge of max degree (original) or total N (later
    variants)
- **Farey advantage:** The MONOTONE NESTING property (F_p subset of F_q for
  p < q) is genuinely absent from CRT-TTS. This is the real differentiator.

### 2.4 Pre-Programmed TDMA
- **What they do:** Assign fixed time slots before deployment. Standard military
  approach for EMCON operations.
- **Strengths:** Zero-communication during operation. Deterministic. Proven.
- **Weakness vs Farey:** Completely rigid. Adding agent #101 to a 100-agent
  plan requires new orders distributed to ALL agents. Cannot adapt in the field.
- **Farey advantage:** Genuine. Farey allows scaling without redistribution of
  the entire schedule.

### 2.5 Randomized ALOHA / Slotted ALOHA
- **What they do:** Nodes transmit at random times. Accept collisions, retransmit.
- **Strengths:** Zero coordination needed. Works with any number of nodes.
- **Weakness:** Maximum throughput ~37% (slotted ALOHA). Collisions are inherent.
- **Farey advantage:** Genuine. 100% utilization vs 37%. But ALOHA is far
  simpler and more robust to node failures.

### 2.6 Consistent Hashing (for data center / load balancing)
- **What they do:** Map nodes and resources onto a hash ring. Adding/removing
  nodes only affects neighboring segments.
- **Strengths:** Monotone property for key assignment. Proven at scale (Dynamo,
  Cassandra, memcached).
- **Why it's NOT a competitor:** Consistent hashing solves a different problem
  (key-to-node mapping), not time-slot scheduling. The monotone property is
  analogous but the domains don't overlap. However, it demonstrates that the
  "monotone scaling" idea is well-known in distributed systems, just not for
  TDMA scheduling specifically.

---

## 3. Application Domains: Where Is Zero-Communication Actually Needed?

### 3.1 Underwater Acoustic Sensor Networks -- STRONG FIT

**The problem:** Acoustic communication underwater is slow (1500 m/s), expensive
(high power), and bandwidth-limited (~10 kbps). Round-trip times of seconds to
minutes. Communication rounds for DESYNC-style convergence are prohibitively slow.

**Current SOTA:**
- UD-TDMA: Distributed but requires 2-hop neighbor information exchange
- ECS: Continuous-time scheduling but requires topology maintenance
- RL-based slot learning (2024): Autonomous but needs training episodes
- DL-MAC: Distributed clustering with TDMA, but needs cluster formation phase

**Farey advantage:** Genuine and significant. With Farey scheduling:
- Deploy sensors with just (sensor_id, fleet_size) pre-loaded
- Zero acoustic messages needed for schedule coordination
- Adding a new sensor (at next prime fleet size) never disrupts existing sensors
- Bandwidth saved: all coordination overhead eliminated

**Quantified benefit:**
- For N=100 sensors with 10-second cycle time:
  - Each sensor gets 100ms slot (= 10s / 100)
  - DESYNC convergence: ~8 rounds x 10s = 80 seconds of setup time with
    100 acoustic messages
  - Farey: instant operation, zero messages
- For N=97 (prime): each sensor gets slot at k/97 in [0,1), mapped to
  time offset (k/97) * T_cycle

**Honest caveat:** Underwater sensors often need to adapt to varying channel
conditions, which Farey's fixed schedule cannot do. Also, sensors may not know
the exact fleet size if some fail silently.

**Verdict: REAL OPPORTUNITY. Publication-worthy for underwater networking venues.**

### 3.2 Satellite Constellations -- MODERATE FIT

**The problem:** LEO mega-constellations (Starlink: 6000+ sats) need inter-satellite
coordination. Communication delays range from milliseconds (LEO-LEO) to seconds
(GEO relay). DARPA's ROCkN program addresses GPS-denied timing with optical clocks.

**Current SOTA:**
- MDMA-CCM: Multi-agent collaboration model for satellite scheduling
- Ground-station-based centralized planning (traditional)
- Autonomous on-board scheduling with periodic ground updates

**Farey advantage:** Limited. Satellites typically have:
- Reliable inter-satellite links (laser/RF)
- Ground station contact windows for schedule updates
- On-board atomic clocks for precise timing
- The communication constraint is not severe enough to justify zero-comm

**Where Farey could help:** A specific scenario: contested space environment
where adversary is jamming inter-satellite links and ground stations are denied.
Satellites fall back to autonomous operation. Pre-loaded Farey schedule provides
collision-free downlink windows without any coordination.

**Honest caveat:** This is a niche scenario. Most satellite operations have
adequate communication for more flexible scheduling.

**Verdict: NICHE. Interesting for contested-space papers but not primary market.**

### 3.3 Military Swarm Operations (EMCON) -- STRONG FIT

**The problem:** Under EMCON conditions, all RF emissions cease. Drone swarms,
autonomous vehicles, and dismounted troops must coordinate without any radio
transmission. Current approach: rigid pre-planned schedules distributed before
mission start.

**Current SOTA:**
- Pre-planned TDMA schedules (rigid, no field adaptation)
- DARPA OFFSET program: swarm tactics, but assumes communication available
- DARPA CODE program: collaborative operations in denied environments
- Chip-scale atomic clocks for timing holdover during GPS denial

**Farey advantage:** Genuine. The specific gap Farey fills:
- Pre-planned schedules cannot adapt (what if 3 of 20 drones are destroyed?)
- Farey's monotone nesting means the SURVIVING drones' slots remain valid
  even as fleet size effectively decreases
- New drones joining mid-mission can compute compatible slots from just
  knowing the NEW fleet size (next prime above current)
- No RF emission at any point

**Quantified benefit:**
- Pre-planned TDMA for 20 drones, 3 destroyed: remaining 17 drones still
  have their original slots, but 3 slots are now wasted (15% waste)
- Farey approach: same 15% waste (Farey doesn't solve this either -- the
  destroyed drones' slots are also wasted)
- BUT: adding 5 reinforcement drones with pre-planned TDMA requires
  distributing a new schedule to ALL 17+5=22 drones (requires communication)
- Farey: reinforcement drones compute slots at p=23 (next prime), and
  these are guaranteed non-colliding with the original p=19 slots

**Honest caveat:** The reinforcement scenario assumes the original drones
don't need to know about the new drones' slots. If bidirectional communication
is needed, Farey only solves one direction (new drones avoid old drones, but
old drones don't know when to listen for new drones). This is a real limitation.

**Verdict: REAL OPPORTUNITY. The reinforcement/scaling scenario is genuine.**

### 3.4 Emergency / Post-Disaster Networks -- WEAK FIT

**The problem:** After infrastructure destruction (earthquake, hurricane), ad-hoc
mesh networks must self-organize. Meshtastic and similar systems handle this.

**Current SOTA:**
- Meshtastic: open-source mesh networking, LoRa-based, self-organizing
- Project OWL DuckLinks: solar-powered mesh for disaster response
- ALOHA-based protocols (accept collisions, prioritize simplicity)

**Farey advantage:** Minimal. Emergency networks:
- Can tolerate collisions (human safety > bandwidth efficiency)
- Need maximum simplicity (Farey requires agents to know fleet size)
- Typically have some communication ability (that's the whole point)
- Bandwidth efficiency (100% vs 37%) matters less than reliability

**Honest caveat:** Emergency responders would never adopt a system that requires
knowing the exact fleet size over a system that "just works" with collisions.

**Verdict: NOT A GOOD FIT. Simplicity and robustness beat efficiency here.**

### 3.5 IoT Sensor Networks (Remote/Low-Power) -- MODERATE FIT

**The problem:** Dense sensor deployments (agriculture, environmental monitoring)
where minimizing radio-on time saves battery. Each sensor wakes briefly to
transmit, then sleeps.

**Current SOTA:**
- LoRaWAN: ALOHA-based, accepts collisions, server-managed
- Zigbee: Beacon-based TDMA with coordinator
- BLE Mesh: Flood-based, no scheduling
- WirelessHART: Centralized TDMA with network manager

**Farey advantage:** Moderate. For dense deployments where a coordinator is
impractical:
- Each sensor pre-loaded with (id, N) computes its wake-up time
- Zero coordination overhead saves energy
- Adding sensors at next prime order doesn't disrupt existing sensors
- No coordinator/gateway needed for scheduling

**Honest caveat:** LoRaWAN works fine for most IoT deployments despite
collisions. The energy savings from zero-coordination may be marginal compared
to the complexity of requiring exact fleet size knowledge. Also, sensor
deployments change slowly (unlike military scenarios), so occasional
reconfiguration via a coordinator is acceptable.

**Verdict: MODERATE. Energy-constrained dense deployments are a real niche.**

### 3.6 Cognitive Radio Spectrum Access -- WEAK FIT

**The problem:** Secondary users must access spectrum without interfering with
primary users or each other. Autonomous channel selection without coordination.

**Current SOTA:**
- Dynamic Jump-Stay (DJS): Distributed channel hopping, no CCC needed
- Autonomous sensing order selection: Converges to collision-free orders
- RL/AI-based spectrum access: Adaptive, learning-based

**Farey advantage:** Limited. Cognitive radio is fundamentally about SENSING
(what channels are free?), not about SCHEDULING (when to transmit). Farey
solves the scheduling problem but CR users need to adapt to dynamic spectrum
availability, which a fixed Farey schedule cannot do.

**Verdict: NOT A GOOD FIT. Dynamic spectrum requires adaptivity, not fixed scheduling.**

---

## 4. The Real Differentiator: Monotone Nesting

After honest analysis, the genuinely unique property is:

**F_p is a subset of F_q for all primes p < q.**

This means: slots assigned to an N-agent fleet are AUTOMATICALLY valid in any
larger fleet. No existing TDMA protocol has this mathematical guarantee.

Comparison:
| Property | Pre-planned | DESYNC | SOTDMA | CRT-TTS | ALOHA | **Farey** |
|---|---|---|---|---|---|---|
| Zero communication | Yes | No | No | Yes | Yes | **Yes** |
| Deterministic | Yes | No | Partly | Yes | No | **Yes** |
| Collision-free | Yes | Yes* | Yes* | Yes | No | **Yes** |
| Monotone scaling | No | Yes** | No | No | N/A | **Yes** |
| No GPS required | Yes | Yes | No | Yes | Yes | **Yes** |
| Adaptive density | No | Yes | Yes | No | N/A | **Yes*** |
| Formally verified | No | No | No | No | No | **Yes** |

*After convergence / **Self-adjusting but requires comm / ***Requires knowing new N

The column where Farey is UNIQUELY "Yes" across all rows is the combination of:
zero-communication + deterministic + collision-free + monotone scaling.

No other protocol achieves all four simultaneously.

---

## 5. Strongest Application Cases (Ranked)

### Tier 1: Genuine Advantage
1. **Underwater acoustic sensor networks** -- Communication is the bottleneck.
   Eliminating coordination messages saves significant energy and time.
   Publication target: IEEE Journal of Oceanic Engineering, ACM WUWNet.

2. **Military EMCON swarm operations** -- Zero-emission requirement is absolute.
   Monotone scaling handles fleet attrition and reinforcement.
   Publication target: IEEE MILCOM, military venues.

### Tier 2: Niche Advantage
3. **Dense IoT sensor networks** -- Energy savings from zero-coordination.
   Requires specific conditions (no coordinator, fixed deployment size).

4. **Contested space operations** -- Satellite scheduling when inter-satellite
   links are jammed. Very specific scenario.

### Tier 3: Farey Doesn't Win
5. **Emergency networks** -- Simplicity beats efficiency.
6. **Cognitive radio** -- Adaptivity beats fixed scheduling.
7. **Data center scheduling** -- Consistent hashing already solves this.

---

## 6. Key Weaknesses to Acknowledge

### 6.1 Fleet Size Must Be Known
Every agent must know p (fleet size, ideally prime). If agents don't know the
current fleet size (e.g., some failed silently), the schedule breaks down.
Pre-planned TDMA has the same weakness. DESYNC and ALOHA do not.

### 6.2 Prime Constraint
The strongest guarantees require p to be prime. In practice, this means
rounding up to the next prime (e.g., 100 agents use p=101). The ~1% overhead
is negligible, but explaining "why prime?" adds complexity.

### 6.3 No Adaptivity
Farey schedules are fixed. If channel conditions vary (fading, interference),
there's no mechanism to adapt. DESYNC and RL-based protocols handle this.

### 6.4 Single-Channel Only
Farey scheduling as described works for a single shared channel. Multi-channel
or multi-hop scenarios require extensions not yet developed.

### 6.5 The Monotone Scaling Requires Coordination About N
To scale from p agents to q agents, SOMEONE must decide q and communicate it.
The schedule computation is zero-comm, but the decision to scale is not.
This is often glossed over but it's a real operational gap.

---

## 7. Patentability Assessment

### Prior Art Search Results
- No patents found combining Farey/Stern-Brocot with TDMA scheduling
- CRT-TTS patents exist (Su 2015) but are mathematically distinct
- SOTDMA/STDMA patents exist (Hakan Lans) but require communication
- Number-theoretic scheduling is a known concept, but Farey-specific
  monotone nesting for TDMA appears to be novel

### Patentability
- The specific method (assign slot k/p for agent k in fleet of p, where p
  is prime) combined with the monotone nesting property appears patentable
- The formal verification in Lean 4 adds value but isn't itself patentable
- Strongest claim: "A method for autonomous time-slot assignment in
  multi-agent systems using Farey sequence injection properties, wherein
  adding agents at a higher prime order produces slots guaranteed
  non-colliding with all existing assignments without communication"

### Recommendation
File a provisional patent application covering the scheduling method before
publishing. The underwater sensor network application provides the strongest
use case for the patent specification.

---

## 8. Publication Strategy

### Primary Paper: Underwater Sensor Networks
- **Title:** "Farey-Prime Scheduling: Zero-Communication TDMA for Underwater
  Acoustic Sensor Networks"
- **Venue:** IEEE Journal of Oceanic Engineering or ACM WUWNet
- **Angle:** Eliminate coordination overhead in bandwidth-starved underwater
  networks. Compare against UD-TDMA, DESYNC, ALOHA.
- **Strength:** Quantifiable advantage (zero acoustic messages vs O(N log N))

### Secondary Paper: Military/EMCON
- **Title:** "Formally Verified Autonomous Scheduling for EMCON Operations"
- **Venue:** IEEE MILCOM or DARPA-adjacent venues
- **Angle:** The only formally verified zero-communication scheduling protocol.
  Lean 4 proofs provide mathematical guarantees unavailable in any competitor.

### Theory Paper: The Monotone Nesting Property
- **Title:** "Monotone TDMA: Scale-Free Scheduling via Farey Injection"
- **Venue:** IEEE/ACM Transactions on Networking or theoretical CS venue
- **Angle:** Pure contribution -- the mathematical property and its implications
  for distributed scheduling theory.

---

## 9. Bottom Line

**Is this a real opportunity?** YES, but narrower than initially hoped.

The zero-communication + monotone scaling combination is genuinely novel for
TDMA scheduling. No existing protocol provides both simultaneously. However:

- The advantage is strongest in environments where communication is
  PHYSICALLY expensive or OPERATIONALLY forbidden (underwater, EMCON)
- In environments where communication is merely inconvenient (IoT, mesh),
  existing protocols like DESYNC work well enough
- The fleet-size-must-be-known requirement is a real limitation that
  competitors like DESYNC and ALOHA don't have

**Estimated significance:** C1-C2 (collaborative, minor-to-publication grade).
The theoretical property is clean and novel. The application advantage is
real but domain-specific. Not a breakthrough, but a solid publishable
contribution for the right venue.
