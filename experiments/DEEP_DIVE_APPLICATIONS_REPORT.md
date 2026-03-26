# Farey-Prime Scheduling: Deep-Dive Application Assessment

**Research Date:** March 26, 2026
**Purpose:** Honest evaluation of practical application domains beyond what is covered in TR-2026-001

---

## Methodology

Web research across seven target domains plus a literature scan for recent (2024-2026) academic work on coordination-without-communication. Each domain is assessed on four criteria:

1. **Real Problem?** Is the communication-denied coordination gap documented and funded?
2. **Current Solutions?** What exists today and how well does it work?
3. **Farey Advantage?** Does our approach offer something genuinely new, or are existing solutions adequate?
4. **Contact Path?** Who would we talk to?

Honesty rating scale: STRONG FIT / MODERATE FIT / WEAK FIT / NOT A FIT

---

## 1. Underwater Autonomous Vehicles (AUVs)

### Real Problem: YES -- well-documented and heavily funded

Underwater communication is fundamentally constrained. RF signals attenuate within meters of the surface. Acoustic modems offer low bandwidth (typically <10 kbps), high latency (speed of sound in water ~1500 m/s), and severe multipath effects. Optical communication requires line-of-sight and short range. The AUV market is projected to grow by USD 3.83 billion at 21.7% CAGR from 2024-2029.

Key constraint: AUV swarms face "excessive communication energy demands and limited environmental perception capabilities" (Nature Communications Engineering, 2025). Lockheed Martin's Marlin AUVs tested with the U.S. Navy in 2024-2025 demonstrated resilience to communication dropouts but still require acoustic networking.

### Current Solutions

- **Digital twin-driven swarm control** (Nature Comms Eng, 2025): Predicts flow fields and reduces communication energy via parameter estimation. Still requires some communication.
- **Hybrid optical-acoustic systems**: Teledyne Marine and L3Harris investing in improved bandwidth. Does not eliminate the communication requirement.
- **Decentralized/distributed control**: Enables swarms to function during dropouts but assumes eventual reconnection.
- **Bio-inspired implicit coordination**: Fish-inspired robot swarms (Science Robotics) achieve collective behaviors using only blue light sensing of neighbors -- no explicit communication. Closest analog to our approach.

### Farey Advantage Assessment: MODERATE FIT

**Where it fits:** Pre-mission scheduling of sensor sweeps, surfacing windows, or acoustic ping slots among AUVs. If 7 AUVs need to share a single acoustic channel, Farey(7) gives each a unique time slot with zero negotiation. When a new AUV joins (scaling to prime 11), existing slots are preserved.

**Where it struggles:** Underwater operations are less about time-slot scheduling and more about spatial coordination in 3D with currents. The primary challenge is maintaining formation and avoiding collisions in dynamic environments, not sharing a communication channel. Most AUV coordination problems are spatial, not temporal.

**Honest assessment:** Farey scheduling could be a useful building block for acoustic channel TDMA but is not a primary solution for the core AUV swarm challenge. It would be one module inside a larger autonomy stack, not the headline capability.

### Contacts

- **ONR Code 321 (Ocean Battlespace Sensing)**: Program officers for underwater autonomous systems
- **Lockheed Martin Rotary and Mission Systems**: Marlin AUV team
- **Teledyne Marine**: Autonomous vehicle division
- **Prof. Radhika Nagpal (Princeton)**: Fish-inspired robot swarm research (Science Robotics)

---

## 2. Space Operations / Satellite Constellations

### Real Problem: YES -- NASA actively investing

NASA's Delay-Tolerant Networking (DTN) addresses store-and-forward data relay but does not solve the coordination problem when multiple spacecraft must act simultaneously during communication blackouts. Mars missions experience up to 2-week blackouts during superior conjunction. The 2004 Mars scenario (3 orbiters + 2 rovers + 1 lander) demonstrated the real coordination challenge.

NASA's PACE mission became the first Class-B mission to use DTN operationally in 2024, with 34+ million bundles transmitted at 100% success rate. High-Rate DTN (HDTN) at Glenn Research Center targets 100-200 Gbps for future missions.

### Current Solutions

- **DTN store-and-forward**: Handles data relay during intermittent connectivity. Does NOT coordinate simultaneous actions across multiple spacecraft.
- **Pre-planned mission timelines**: Spacecraft follow detailed command sequences uploaded before blackouts. Rigid, cannot adapt.
- **Autonomous onboard planners**: JPL's CASPER and ESA's RAMP allow spacecraft to replan locally but cannot coordinate with other spacecraft.

### Farey Advantage Assessment: MODERATE FIT

**Where it fits:** Multiple orbiters sharing a relay antenna, or scheduling downlink windows among a constellation during conjunction. If 5 Mars orbiters each need relay time with a surface asset, Farey(5) assigns non-conflicting windows. When a 6th orbiter arrives (scale to Farey(7)), no existing assignments change.

**Where it struggles:** Space missions are meticulously pre-planned. The number of spacecraft at any single target is small (currently <10 at Mars). The overhead of implementing a new scheduling scheme vs. simply pre-planning a fixed schedule for 5-10 assets is hard to justify. The "flexible scaling" advantage matters less when you know exactly how many spacecraft you have.

**Honest assessment:** Farey scheduling is elegant but solves a problem that space agencies currently handle adequately with pre-planned timelines for small constellations. The value proposition improves significantly for future scenarios with dozens of assets (e.g., Artemis-era lunar surface operations with many robotic assets).

### Contacts

- **NASA SCaN (Space Communications and Navigation)**: DTN program office
- **JPL Section 332 (Mission Planning and Execution)**: Autonomous planning group
- **NASA Glenn Research Center**: HDTN development team

---

## 3. Disaster Response

### Real Problem: YES -- repeatedly demonstrated in real events

Communication infrastructure destruction is the norm in major disasters. Hurricane Maria (2017) knocked out 88% of Puerto Rico's cell sites. Hurricane Helene (late 2024) caused widespread communication failures in Tennessee and North Carolina. First responders consistently cite communication breakdown as a top operational challenge.

### Current Solutions

- **goTenna mesh networks**: Peer-to-peer radio mesh, actively deployed by FEMA and state agencies. Works without infrastructure but requires powered devices and radio transmission.
- **FirstNet (First Responder Network Authority)**: Dedicated LTE band with priority/preemption. Depends on surviving cell infrastructure.
- **Satellite phones / BGAN terminals**: Expensive, limited bandwidth, high latency.
- **Galileo EWSS (launching 2025)**: Satellite-based emergency alert broadcast. One-way only.
- **FEMA Disaster Emergency Communications**: Deploys portable cell towers and satellite terminals.

### Farey Advantage Assessment: WEAK FIT

**Where it fits:** Theoretically, if multiple rescue teams need to share a single radio frequency without a coordinator, pre-loaded Farey schedules could assign time slots. Each team uses their assigned slot to broadcast status.

**Where it struggles:** Disaster response is fundamentally about restoring communication, not operating without it. First responders NEED to exchange variable-length messages, not just occupy time slots. The problem is bandwidth and infrastructure, not time-slot allocation. Mesh networks (goTenna) already solve the peer-to-peer coordination problem better because they enable actual data exchange. Additionally, the number of teams is unpredictable and dynamic -- the "pre-loaded prime" model does not fit well.

**Honest assessment:** This is not a strong application domain. The disaster response community is investing in resilient communication restoration (mesh, satellite, portable towers), not communication-free coordination. Farey scheduling does not address their actual pain point.

### Contacts

- Not recommended as a primary outreach domain.

---

## 4. Autonomous Vehicle Platooning

### Real Problem: YES -- active research area with documented V2V failures

V2V communication failures in platoons are well-documented: packet loss, signal blocking, hardware damage. Research shows that >20% packet loss destabilizes multi-predecessor coordination. Multiple 2024-2025 papers address this directly.

### Current Solutions

- **Switched controllers (CACC to ACC fallback)**: When V2V fails, vehicles degrade from Cooperative ACC to standard ACC using only onboard sensors. Well-studied, already implemented in commercial systems.
- **DMPC with state estimation**: Distributed Model Predictive Control that estimates missing information probabilistically.
- **PIDM (Platoon Intelligent Driver Model, 2025)**: Analytical framework integrating dynamic communication topologies with vehicle dynamics.
- **Adaptive Kalman Filtering**: Dynamic weight adjustment based on communication topology state.

### Farey Advantage Assessment: WEAK FIT

**Where it fits:** If platoon vehicles need to sequence actions (lane changes, exit maneuvers) and V2V drops, a pre-loaded schedule could assign time windows for each vehicle's maneuver.

**Where it struggles:** Platooning is a continuous-control problem, not a discrete-scheduling problem. Vehicles need to maintain spacing at millisecond timescales, not take turns. The fallback from CACC to ACC (using radar/lidar only) is well-understood and already deployed. The time-slot paradigm does not match the physical problem of maintaining safe following distances at highway speeds.

**Honest assessment:** This is not a natural fit. The platooning community has sophisticated fallback strategies that operate in the continuous domain. Farey scheduling solves a discrete time-slot problem that is not the actual bottleneck.

### Contacts

- Not recommended as a primary outreach domain.

---

## 5. Underground Mining Operations

### Real Problem: YES -- GPS-denied, communication-constrained

Underground mines are inherently GPS-denied with severe communication constraints. Rock walls, dust, and moisture degrade all wireless signals. Mine tunnels are typically 2m x 2m cross-sections. A 2025 systematic review highlights Wi-Fi, LTE, and 5G as prevailing technologies but notes significant gaps in handling communication outages.

Multi-robot underground systems must operate fully autonomously using only onboard sensors. Coordination of heterogeneous fleets (drilling, hauling, exploration robots) without centralized control is an active research challenge.

### Current Solutions

- **Leaky feeder cables**: Radiating coaxial cables along tunnels. Fixed infrastructure, breaks when tunnel collapses.
- **Mesh networks (Kinetic Mesh / Rajant)**: Autonomous industrial wireless mesh. Adapts to conditions but still requires radio.
- **5G private networks**: Being tested but feasibility in active mines unproven.
- **Pre-planned traffic management**: Mining trucks follow rigid schedules through narrow tunnels. Very similar to our use case.

### Farey Advantage Assessment: MODERATE FIT

**Where it fits:** Mining vehicles sharing single-lane tunnels must sequence their passage through intersections and narrow segments. This is literally the chokepoint scheduling problem. If communication infrastructure fails (tunnel collapse, equipment failure), pre-loaded Farey schedules could maintain safe sequencing. The scaling property matters: when a new vehicle enters the mine, it gets a unique slot without disrupting existing vehicles.

**Where it struggles:** Mining operations are highly centralized and controlled. Dispatch systems track every vehicle. The scenarios where ALL communication fails simultaneously are rare (they have redundant systems). The fleet sizes are modest (typically 10-30 vehicles).

**Honest assessment:** This is a legitimate secondary application, particularly for emergency/degraded operations when communication infrastructure is damaged. The tunnel chokepoint problem is a genuine fit for temporal scheduling. However, it is a niche safety-net application, not a headline capability. The mining industry moves slowly on adopting new technology.

### Contacts

- **CSIRO Mining Technology Group** (Australia): Leading mining autonomy research
- **Sandvik Mining and Rock Technology**: Autonomous mining fleet systems
- **Epiroc**: Underground mining automation division
- **NIOSH (National Institute for Occupational Safety and Health)**: Mining safety research

---

## 6. Nuclear Facility Operations

### Real Problem: UNCLEAR -- highly regulated, conservative domain

The search found no documented scenarios combining EMP events, communication failures at nuclear facilities, and autonomous system coordination. Nuclear facilities operate under extremely conservative safety philosophies with multiple redundant communication systems and manual override capabilities.

### Current Solutions

- **Hardened communication systems**: Nuclear facilities use EMP-hardened, physically separated communication channels (fiber optic, hardwired).
- **Manual procedures**: Operators follow paper-based emergency procedures. Nuclear safety philosophy emphasizes human-in-the-loop, not autonomous coordination.
- **Multi-robot systems for inspection**: Some research on autonomous robots for nuclear environment inspection (IET Cyber-Systems and Robotics, 2023), but these use digital twin interfaces with human-on-the-loop.
- **IAEA autonomy levels**: NRC recognizes autonomy levels 1-4 but current nuclear applications are levels 1-2 (human-assisted by AI).

### Farey Advantage Assessment: NOT A FIT

**Where it fits:** Theoretically, autonomous inspection robots in a contaminated zone could schedule their movements through corridors. But this is hypothetical and not a real current need.

**Where it struggles:** Nuclear facilities are the most conservative technology adopters. They have redundant hardened communication. The regulatory environment (NRC, IAEA) makes adoption of novel scheduling schemes for safety-critical operations essentially impossible in the near term. There is no documented demand for communication-free coordination in this domain.

**Honest assessment:** Do not pursue. The nuclear domain has different problems (radiation-hardened electronics, decontamination, regulatory compliance) that Farey scheduling does not address.

### Contacts

- Not recommended.

---

## 7. Open DARPA/ONR/AFRL Solicitations (2025-2026)

### Direct Matches: NONE currently named

The most directly relevant historical programs (DARPA CODE and DARPA OFFSET) have both concluded. No current named program specifically targets "communication-denied autonomous swarm coordination."

### Best Entry Points (Office-Wide BAAs with Rolling Deadlines)

| Solicitation | Office | Deadline | Relevance |
|---|---|---|---|
| **DARPA TTO BAA (HR001125S0011)** | Tactical Technology Office | Exec Summary: Apr 17, 2026; Proposal: Jun 22, 2026 | STRONGEST. TTO housed both OFFSET and CODE. Focus on "low-cost autonomous systems that can use mass to overwhelm." |
| **DARPA STO BAA** | Strategic Technology Office | Rolling through 2026 | STRONG. Seeks "autonomy and control algorithms, distributed autonomy and teaming, communications and networking." |
| **DARPA I2O BAA (HR001126S0001)** | Information Innovation Office | Abstract: Nov 1, 2026; Proposal: Nov 30, 2026 | MODERATE. Broadest AI entry point. Our approach is more math than AI but could fit under "resilient systems." |
| **DARPA DSO BAA** | Defense Sciences Office | Rolling through Jun 2, 2026 | MODERATE. Mathematical foundations angle could fit here. |
| **ONR Long-Range BAA** | Office of Naval Research | Rolling | MODERATE. Submarine and UUV coordination angle. |

### Related Active Programs

- **DARPA AIR (Artificial Intelligence Reinforcements)**: Successor to ACE. Multi-ship autonomous air combat. Communication resilience is a secondary concern but relevant.
- **DARPA RACER**: Demonstrated autonomous ground vehicles in GPS-denied environments. Now open-sourcing the RACER software stack (announced 2026).
- **Pentagon Replicator Initiative**: Deploying thousands of cheap autonomous drones by 2026. Communication-denied operation is implicit in the mass-deployment concept.
- **Shield AI Hivemind**: Commercial autonomous swarm AI for GPS-denied environments.
- **L3Harris AMORPHOUS (Feb 2025)**: Command-and-control system where any drone in a swarm can assume coordination duties if another is lost.

### Recommendation

Submit a 2-page executive summary to the **DARPA TTO BAA** by April 2026. Frame it as: "Mathematically verified scheduling primitive for OFFSET/CODE-class problems. Formal verification in Lean 4. Zero communication overhead. Hierarchical scaling. Complements existing autonomy stacks."

---

## 8. Recent Academic Literature (2024-2026) for Citation/Engagement

### Must-Cite Papers

| Paper | Venue | Relevance |
|---|---|---|
| **"Implicit coordination for 3D underwater collective behaviors in a fish-inspired robot swarm"** | Science Robotics | Foundational work on coordination without explicit communication. Demonstrates that complex collective behaviors emerge from local sensing only. |
| **"CoDe: Communication Delay-Tolerant Multi-Agent Collaboration via Dual Alignment"** | arXiv, Jan 2025 | Directly addresses communication delay/denial. Proposes intent-based messaging. Our work is complementary (we eliminate communication entirely). |
| **"Harnessing Stubborn AUVs for Decentralized Decision Strategies in Communication-Limited Environments"** | EUMAS 2025 (Frenkel) | AUV-specific communication-limited coordination. Direct comparison opportunity. |
| **"Successful Misunderstandings: Learning to Coordinate Without Being Understood"** | EUMAS 2025 | Novel framing of coordination without mutual comprehension. Theoretical complement to our approach. |
| **"New Collision-Free Balanced Frequency Hopping Sequence Sets"** | arXiv:2408.12149, Aug 2024 | Uses GF(p) constructions for collision-free frequency hopping. CLOSEST mathematical relative -- uses finite field number theory for collision avoidance. Key comparison point. |
| **"Multi-Agent Coordination across Diverse Applications: A Survey"** | arXiv, Feb 2025 | Comprehensive survey covering sparse/learned communication protocols. Position our work within this taxonomy. |
| **CRT-based protocol sequences for collision channels without feedback** | IEEE Trans. Info. Theory | Uses Chinese Remainder Theorem for deterministic multiple access. Direct mathematical competitor using different number-theoretic tool. |
| **Coprime cycle-length rendezvous algorithms for cognitive radio** | Various | Uses coprime property for guaranteed channel rendezvous. Same mathematical family as our work. |

### Key Venues for Submission/Engagement

- **EUMAS 2025/2026**: European conference on multi-agent systems. Active work on communication-limited coordination.
- **AAMAS 2025 (Detroit) / 2026 (Cyprus)**: Premier multi-agent systems venue. Has a workshop on "Autonomous Agents and Multi-Agent Systems for Space Applications."
- **IEEE MILCOM**: Military communications. Natural venue for the defense application.
- **IEEE Trans. Information Theory**: For the pure mathematical contribution (collision-free sequences).

---

## 9. Synthesis: Honest Priority Ranking

| Domain | Fit Rating | Rationale | Action |
|---|---|---|---|
| **Military swarms (DARPA/DoD)** | STRONG | Core problem matches exactly. Funded. Programs existed and successors are forming. | Submit TTO BAA exec summary by Apr 2026 |
| **Underground mining** | MODERATE | Tunnel chokepoint scheduling is a genuine fit. Niche but real. | Explore through CSIRO or Sandvik |
| **AUV swarms** | MODERATE | Acoustic channel TDMA is real but is one component of a larger challenge. | Position as building block, not headline |
| **Space operations** | MODERATE | Elegant fit but small constellations reduce urgency. Better for future lunar/Mars scenarios. | Write white paper for NASA SCaN |
| **Vehicle platooning** | WEAK | Continuous control problem, not discrete scheduling. Good fallbacks exist. | Do not prioritize |
| **Disaster response** | WEAK | Community wants communication restoration, not communication avoidance. | Do not prioritize |
| **Nuclear facilities** | NOT A FIT | No documented need. Extremely conservative domain. | Do not pursue |

---

## 10. Key Insight from This Research

The most important finding is the **collision-free frequency hopping / protocol sequence** literature. Papers on CRT-based sequences, coprime rendezvous algorithms, and GF(p) collision-free hopping sets are using closely related number-theoretic machinery for closely related problems. The 2024 paper on Collision-Free Balanced FHS (arXiv:2408.12149) is essentially a sibling approach using Galois fields instead of Farey sequences.

**Strategic implication:** Our Farey-Prime scheduling should be explicitly positioned against the CRT-sequence and GF(p)-FHS literature, not just against DESYNC/STDMA. The unique selling point remains the hierarchical injection property (new agents join without reassigning existing slots), which neither CRT nor GF(p) approaches provide naturally. But we must acknowledge and cite this related work to be credible.

The "coordination without communication" field is growing rapidly (EUMAS, AAMAS, NeurIPS all had relevant papers in 2024-2025), but most work focuses on learned implicit coordination (reinforcement learning, emergent communication). Our deterministic, formally verified approach occupies a distinct niche: guaranteed performance rather than expected performance. This is the angle to emphasize for defense and safety-critical applications.

---

## Sources

- [Digital twin-driven swarm of AUVs (Nature Comms Eng, 2025)](https://www.nature.com/articles/s44172-025-00571-7)
- [AUV Swarm Coordination Systems 2025-2030](https://www.macnifico.pt/news-en/auv-swarm-coordination-systems-2025-2030-revolutionizing-underwater-autonomy-mission-efficiency/86566/)
- [NASA Delay/Disruption Tolerant Networking](https://www.nasa.gov/communicating-with-missions/delay-disruption-tolerant-networking/)
- [NASA High-Rate DTN](https://www.nasa.gov/glenn/glenn-expertise-space-exploration/scan/high-rate-delay-tolerant-networking/)
- [NASA DTN Overview](https://www.nasa.gov/technology/space-comms/dtn-overview-benefits-successstories-learningresources/)
- [Sustainable Communication Infrastructure in Disaster Relief (arXiv, 2024)](https://arxiv.org/html/2410.13977v1)
- [goTenna Mesh Networks for Disaster Response](https://gotenna.com/blogs/newsroom/mobile-mesh-networks-can-ensure-communication-in-disaster)
- [FirstNet Emergency Management](https://firstnet.gov/public-safety/firstnet-for/emergency-management)
- [CAV Platoon Maintenance under Communication Failures](https://www.sciencedirect.com/science/article/abs/pii/S2214209622000146)
- [PIDM: V2V Communication Limitations in Platoons (PLOS One, 2025)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0328555)
- [Platoon Stability under Communication Disruption (2024)](https://www.researchgate.net/publication/383477004)
- [Underground Multi-robot Systems (arXiv, 2025)](https://arxiv.org/html/2509.16267v1)
- [Autonomous Mining through Cooperative Driving (Nature Comms Eng, 2024)](https://www.nature.com/articles/s44172-024-00220-5)
- [Wireless Communication in Underground Mining (IEEE Access, 2025)](https://ieeexplore.ieee.org/iel8/6287639/10820123/10971933.pdf)
- [DARPA OFFSET Program](https://www.darpa.mil/work-with-us/offensive-swarm-enabled-tactics)
- [DARPA AIR Program](https://www.darpa.mil/research/programs/artificial-intelligence-reinforcements)
- [DARPA TTO BAA](https://www.darpa.mil/research/opportunities/baa)
- [Every DARPA AI Program 2026](https://grantedai.com/blog/every-darpa-ai-program-2026)
- [Collision-Free Balanced FHS (arXiv:2408.12149, 2024)](https://arxiv.org/abs/2408.12149)
- [CRT Protocol Sequences (arXiv:1611.03012)](https://arxiv.org/abs/1611.03012)
- [Implicit Coordination in Fish-Inspired Robot Swarms (Science Robotics)](https://www.science.org/doi/full/10.1126/scirobotics.abd8668)
- [CoDe: Communication Delay-Tolerant Collaboration (arXiv, 2025)](https://arxiv.org/html/2501.05207v1)
- [Multi-Agent Coordination Survey (arXiv, Feb 2025)](https://arxiv.org/html/2502.14743v2)
- [Comprehensive Survey on Multi-Agent Cooperative Decision-Making (arXiv, Mar 2025)](https://arxiv.org/html/2503.13415v1)
- [South Korea-US Underwater Drone Swarms](https://www.armyrecognition.com/news/navy-news/2025/south-korea-and-the-u-s-to-build-navy-underwater-drone-swarms-to-counter-china-in-indo-pacific)
- [DARPA RACER Finish Line (2026)](https://www.darpa.mil/news/2026/racer-finish-line)
- [Battle Swarms 2025](https://www.factorem.co/knowledge-hub/battle-swarms-2025-ai-defense-bots-storm-the-frontline)
