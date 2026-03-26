# Executive Summary: Farey-Prime Scheduling for Zero-Overhead Multi-Agent Time Coordination

**Submitted to:** DARPA Tactical Technology Office, BAA HR001125S0011
**Date:** March 2026
**Distribution Statement A:** Approved for Public Release; Distribution Unlimited
**Point of Contact:** Saar Shai, Independent Researcher

---

## Problem Statement

When a swarm of drones loses its communication link — whether from enemy jamming, an EMP event, or operating deep underground — every second of coordination is lost. Today, there is no way for autonomous agents to guarantee collision-free timing without first talking to each other. We propose a solution: a simple mathematical formula that lets each agent independently compute its unique time slot, with a machine-verified proof of zero collisions — no communication required.

Specifically, multi-agent autonomous systems operating under Emissions Control (EMCON) or in Degraded, Disrupted, Intermittent, and Limited (DDIL) communication environments face a scheduling problem: how do agents coordinate their use of shared time slots -- for transmission windows, sensor sweeps, or movement through chokepoints -- without dedicating any communication bandwidth to scheduling negotiation? Current fallback modes reduce to rigid pre-planned schedules (no flexibility to add agents), convergent protocols such as DESYNC and STDMA (require multiple rounds of beacon exchange before the schedule stabilizes), or probabilistic random access (no collision guarantee). No existing method simultaneously provides zero scheduling overhead, flexible scaling, observation-free operation, and mathematically guaranteed collision-free time assignment.

**Clarification on scope:** Farey-Prime Scheduling eliminates the need for meta-communication about who transmits when. Agents still use their assigned time slots to transmit data. The value is zero *scheduling overhead* -- no bandwidth, time, or emissions are consumed negotiating the schedule itself.

## Proposed Innovation

Farey-Prime Scheduling is a deterministic TDMA scheme derived from the injection properties of Farey sequences at prime orders. Each agent is pre-loaded with two integers: its index k and the group prime p. During operation, agent k occupies time slot k/p of each frame period. No runtime communication, channel sensing, or observation of other agents is required to determine the schedule. The schedule is fully determined at load time, freeing all available bandwidth for mission data.

The key structural property is **hierarchical non-disruption**: when a group scales from prime p to a larger prime q, all existing slot assignments at order p are preserved. New agents at order q slot into gaps without reassignment. This enables graceful growth -- reinforcements join a coordinated group by loading the next prime, without any schedule renegotiation or reassignment of existing agents. To our knowledge, no prior work in the TDMA or topology-transparent scheduling literature provides this specific hierarchical injection property in a zero-overhead context.

## Key Technical Result

The collision-freedom guarantee rests on the Farey Injection Theorem: each gap between consecutive fractions in Farey sequence F_{N-1} receives at most one new fraction in F_N. This theorem has been formally verified in the Lean 4 proof assistant using the Mathlib library, comprising 24 machine-checked theorems among 207 total declarations with no unproven steps. Supporting results include verified proofs of the Farey involution, displacement antisymmetry, and insertion orthogonality.

Computational verification extends through all primes up to 49,999 (5,133 primes tested, zero exceptions). Simulation of a 50-agent denied-environment scenario confirms 0.0% collision rate and 100% slot utilization under complete communication denial, compared to 36.4% collision rate for DESYNC (which fails entirely when its beacon exchange is jammed) and 22.3% for pure ALOHA.

This level of formal verification -- machine-checked proofs of correctness for a scheduling protocol -- is, to our knowledge, without precedent in the TDMA literature.

## Competitive Advantage

The table below summarizes the gap Farey-Prime Scheduling fills:

| Method | Zero Scheduling Overhead | Flexible Scaling | No Observation | Collision-Free Guarantee |
|--------|--------------------------|-----------------|----------------|--------------------------|
| **Farey-Prime** | **Yes** | **Yes (hierarchical)** | **Yes** | **Yes (formally verified)** |
| DESYNC | No (beacon rounds) | Yes | Yes | Yes (after convergence) |
| STDMA (AIS) | No (listening phase) | Yes | No | Yes (after convergence) |
| CRT-TTS | Yes* | Yes | Yes | Yes |
| Birthday/ALOHA | Yes | Yes | Yes | No (probabilistic) |
| Pre-planned rigid | Yes | No | Yes | Yes |

*CRT-based Topology-Transparent Scheduling also requires no runtime communication for schedule computation. However, it requires pre-agreement on global network parameters (maximum node count N or maximum degree bound D), and it addresses multi-hop interference avoidance rather than single-channel TDMA. Its schedule lengths grow as O(D^2), leading to lower slot utilization for large networks. Critically, CRT-TTS does not provide the hierarchical injection property -- the ability to add agents at the next prime without disturbing any existing assignments. Both approaches are formally correct; the distinction is in the problem domain (multi-hop vs. single-channel) and the scaling model (parameter-dependent vs. hierarchical prime growth).

Slot overhead is negligible: for practical group sizes (5--500 agents), at most 3 slots are wasted due to the prime gap, representing less than 1% overhead. The required clock synchronization (within one slot duration) is achievable with current tactical timing sources including GPS-disciplined oscillators and emerging optical clocks (DARPA ROCkN/STOIC programs).

## Relevance to DARPA Programs

Farey-Prime Scheduling addresses the zero-bandwidth fallback layer for programs that encounter DDIL coordination challenges:

- **DARPA FLUID (FLexible networking Using Intelligent Dialecting):** Active program seeking C5ISRT operation under DDIL conditions. Farey scheduling provides the deterministic coordination layer for the extreme case where network bandwidth drops to zero -- the floor beneath FLUID's degradation curve.

- **DARPA OFFSET (concluded) / DARPA CODE (concluded, transitioned to NAVAIR):** These programs demonstrated the operational need for swarm coordination under communication denial. OFFSET fielded 250+ agent swarms; CODE demonstrated collaborative UAS autonomy under active jamming. Successor programs and the Replicator initiative inherit the same coordination challenges that Farey scheduling addresses.

## Demonstration Readiness

The following artifacts exist and are available for review:

- **Lean 4 formal proofs:** 207 declarations, 24 key theorems, zero unproven steps. Complete machine-checked verification of the injection property and supporting identities.
- **Computational verification suite:** Python simulation confirming injection for all primes through 49,999.
- **Denied-environment simulation:** 50-agent scenario with comparative benchmarks against DESYNC, pure ALOHA, and slotted ALOHA under communication denial.
- **Technical report (TR-2026-001):** Full mathematical exposition, competitive analysis, and operational parameter tables.

## Proposed Work

**Phase 1 (Months 1--12, simulation and analysis):** Scalable simulation comparing Farey-Prime Scheduling against DESYNC, STDMA, CRT-TTS, and random access for scenarios up to 250 agents across varied operational conditions (partial jamming, agent attrition, timing drift up to 10% of slot duration). Extend formal verification to the 2D tensor-product case for combined spatial-temporal scheduling. Deliver peer-reviewed publication to IEEE Communications Letters or IEEE MILCOM. Investigate combined Farey time-slot / CRT frequency-hopping scheme for full time-frequency coordination.

**Phase 2 (Months 9--24, software integration and testing):** Develop a reference implementation of the Farey scheduling layer as a lightweight middleware component. Integrate with an open-source autonomous systems framework (e.g., ROS 2, MACE) to demonstrate activation as a fallback coordination mode upon communication loss detection. Validate on a small-scale multi-robot testbed (5--15 units). Measure time-to-coordinated-operation versus baseline degraded-mode behaviors. Engage with a hardware partner (drone swarm vendor or tactical radio manufacturer) for Phase 3 planning.

**Phase 3 (Months 18--36, hardware demonstration):** Demonstration on a multi-agent platform (ground robots or commercial drone swarm, 10--50 units) under simulated EMCON conditions. Develop transition documentation for integration into autonomous system coordination stacks. The computational requirement is minimal -- one integer division per agent per frame -- enabling implementation on the simplest embedded processors.

## Team

**Saar Shai** -- Independent Researcher. Developer of the Farey-Prime Scheduling theory, author of the Lean 4 formal verification suite, and principal investigator on all simulation and analysis work to date. Background in mathematics and computational research with focus on number-theoretic structures and their applications.

*The investigator seeks collaboration with a university research group or defense laboratory for Phase 2--3 hardware integration and testing.*

## Known Limitations

1. **Timing only, not content.** Farey scheduling determines WHEN agents act, not WHAT they do. It must be combined with mission planning to achieve meaningful coordination.
2. **Single channel.** The current formulation addresses one-dimensional time-division only. Multi-channel extension via combined Farey/CRT construction is proposed for Phase 1 investigation.
3. **Shared time reference required.** All agents must agree on a common clock to within one slot duration. For a 251-agent system with 1-second frames, this means synchronization to approximately 1 ms -- achievable with current tactical timing sources.
4. **Static group composition.** The injection property handles graceful growth (adding agents at the next prime) but does not natively handle arbitrary join/leave dynamics. Departed agents leave unused slots (acceptable but wasteful).

---

*This summary references formally verified results (Lean 4 proof assistant, Mathlib library). All collision-freedom guarantees cited are machine-checked. Computational verification extends through p = 49,999. Full technical report and simulation data available upon request.*

*Contact: HR001125S0011@darpa.mil (BAA Coordinator) | Executive Summary deadline: April 17, 2026*
