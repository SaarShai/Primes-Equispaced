# Radio-Silent Coordination: The Real-World Problem and How Farey/Prime Scheduling Helps

**Date:** 2026-03-25
**Purpose:** Document real, published problems where autonomous agents must coordinate
WITHOUT communication, and honestly assess how our Farey injection principle addresses them.

---

## Executive Summary

The problem of coordinating autonomous agents without communication is not theoretical.
It is an active, funded, unsolved problem across military, automotive, space, and
disaster-response domains. Billions of dollars flow into programs that all hit the
same wall: **when you can't talk, how do you avoid stepping on each other?**

Our contribution -- the Farey injection principle -- provides a mathematically proven,
deterministic answer for one critical sub-problem: **collision-free time-slot assignment
with zero communication**. Each agent needs only to know two numbers (its index k and
the group size p, a prime) to compute its transmission/action slot k/p. The injection
principle guarantees no collisions with any agent operating at lower Farey orders.

This document surveys the real-world demand across six domains.

---

## 1. DARPA Programs

### 1.1 DARPA OFFSET (OFFensive Swarm-Enabled Tactics)

**Source:** [DARPA OFFSET Program Page](https://www.darpa.mil/research/programs/offensive-swarm-enabled-tactics)
**Source:** [DARPA OFFSET Vision Paper (IEEE)](https://ieeexplore.ieee.org/document/10876037/)

**THE PROBLEM:** OFFSET envisions swarms of 250+ small unmanned aircraft and ground
systems operating in dense urban environments -- buildings, tunnels, tight corridors.
These environments severely constrain communications: vertical structures block signals,
indoor operations lose GPS and radio contact, and the sheer number of agents creates
bandwidth contention.

The program ran six "swarm sprints" with themes including swarm autonomy, human-swarm
teaming, and maintaining communications indoors. The core challenge: how do 250 robots
share a radio channel when buildings block their signals and enemy jamming degrades
what remains?

**CURRENT SOLUTIONS:**
- Behavior-based swarm tactics where agents follow local rules (separation, alignment,
  cohesion) to produce emergent coordinated behavior
- Game-theoretic approaches where agents run the same algorithm independently
- Mesh networking with adaptive routing to work around blocked paths
- Pre-planned "plays" (like football plays) loaded before mission start

**THE GAP:** All current approaches either require some communication to coordinate,
or fall back to pre-scripted behavior when communication fails. There is no principled
mathematical framework for guaranteeing collision-free channel access when radio contact
is lost entirely.

**HOW FAREY SCHEDULING HELPS (honest assessment):**
- In EMCON (total radio silence), each drone could compute its transmission window
  as k/p of the frame period using only its pre-assigned index. Zero coordination
  overhead, zero radio emissions during slot assignment.
- When a new drone joins (if the swarm grows to the next prime count), the injection
  principle guarantees it slots in without disrupting existing schedules.
- **Limitation:** OFFSET swarms have arbitrary sizes (not prime). You'd round up to
  the next prime, wasting a few slots. For 250 drones, the next prime is 251 -- only
  1 wasted slot. This is practical.
- **Limitation:** Spatial reuse (two distant drones transmitting simultaneously) is
  not addressed. Farey scheduling is a single-channel model.

---

### 1.2 DARPA CODE (Collaborative Operations in Denied Environment)

**Source:** [DARPA CODE Program Page](https://www.darpa.mil/research/programs/collaborative-operations-in-denied-environment)
**Source:** [CODE Phase 2 Announcement](https://www.darpa.mil/news/2016/code-unmanned-air-system)

**THE PROBLEM:** CODE develops algorithms for groups of unmanned aircraft to collaborate
under a single human supervisor in "anti-access/area-denial" (A2AD) environments --
where adversaries actively jam communications and deny GPS. The program explicitly
targets scenarios where bandwidth is severely limited or intermittently denied.

CODE demonstrated UAS that could "efficiently share information, cooperatively plan
and allocate mission objectives, make coordinated tactical decisions, and collaboratively
react to a dynamic, high-threat environment with minimal communication."

**CURRENT SOLUTIONS:**
- Modular software architecture designed to be "resilient to bandwidth limitations
  and communications disruptions"
- Raytheon's Phase 3 implementation focuses on graceful degradation: full autonomy
  when disconnected, collaborative planning when connected
- The key insight: each UAS must be able to operate independently but also merge
  plans when communication is briefly restored

**THE GAP:** When communication drops entirely, current CODE systems revert to
individual autonomous behavior -- each UAS pursues its last known mission objective
independently. There is no mechanism for coordinated timing of actions (like
simultaneous sensor sweeps or coordinated strikes) during blackout periods.

**HOW FAREY SCHEDULING HELPS:**
- During communication blackouts, UAS could maintain coordinated timing using
  pre-agreed Farey slots. Each aircraft knows its index; the schedule is implicit.
- When communication resumes, the Farey structure means no re-negotiation of
  time slots is needed -- the schedule was deterministic all along.
- **This is the strongest use case:** a pre-loaded Farey schedule acts as a
  mathematical "fallback mode" that guarantees coordination during comm loss.

---

### 1.3 DARPA FLUID (Flexible Logistics for Uncertain and Intermittent Data)

**Source:** [DARPA FLUID Program Page](https://www.darpa.mil/research/programs/fluid)

**THE PROBLEM:** FLUID explicitly targets DDIL (Denied, Disrupted, Intermittent,
Limited) network conditions. The program seeks to enable C5ISRT systems to function
"without sacrificing application or network utility, under network capacities that
range from 1Mbps to 1Kbps."

This is DARPA acknowledging that near-peer adversaries (Russia, China) can and will
degrade US military communications to near-zero bandwidth.

**CURRENT SOLUTIONS:**
- Intelligent message compression and prioritization
- Dynamic adaptation of data and control plane messages
- The goal is to "reduce load while not impacting system utility"

**THE GAP:** FLUID focuses on making existing systems work at low bandwidth. It does
NOT address the zero-bandwidth case -- what happens when there is NO communication
at all, not even 1Kbps.

**HOW FAREY SCHEDULING HELPS:**
- Farey scheduling operates at ZERO bandwidth. No bytes need to be exchanged.
- It could serve as the "below 1Kbps" fallback that FLUID does not cover.
- Agents pre-loaded with Farey schedules maintain coordination even when FLUID's
  compression can't help because the channel is dead.

---

### 1.4 DARPA STOIC and ROCkN (Timing Without GPS)

**Source:** [DARPA STOIC Program](https://www.darpa.mil/research/programs/spatial-temporal-orientation-information-contested-environments)
**Source:** [ROCkN Enables GPS-Free Operations](https://www.darpa.mil/news/2026/rockn-enables-gps-free-operations)

**THE PROBLEM:** GPS provides not just positioning but also precise timing for
military operations. When GPS is jammed or spoofed, systems lose both location
AND time synchronization. STOIC and ROCkN develop backup timing sources using
optical clocks and quantum sensors.

**CURRENT SOLUTIONS:**
- Ultra-stable tactical clocks (atomic clocks small enough for field deployment)
- Optical time synchronization that is harder to jam than GPS
- Quantum navigation systems (DARPA RoQS program)

**HOW FAREY SCHEDULING HELPS:**
- Farey-based TDMA requires only that agents agree on a shared time reference
  and know their index. It does NOT require GPS.
- Combined with ROCkN's precise clocks, Farey scheduling provides a complete
  coordination solution: ROCkN gives you accurate time, Farey gives you
  collision-free slot assignment, and neither requires GPS or radio communication.
- This is a natural pairing: ROCkN solves "when is it?" and Farey solves
  "whose turn is it?"

---

## 2. Military Operations

### 2.1 EMCON (Emissions Control)

**Source:** [Mission Command Means Emissions Control, US Naval Institute Proceedings, May 2021](https://www.usni.org/magazines/proceedings/2021/may/mission-command-means-emissions-control)
**Source:** [Adapting to Multi-Domain Battlefield: Developing EMCON SOP, US Army, 2024](https://www.army.mil/article/284546/adapting_to_multi_domain_battlefield_developing_emissions_control_sop)
**Source:** [Drill Emission Control as a Main Battery, US Naval Institute Proceedings, June 2023](https://www.usni.org/magazines/proceedings/2023/june/drill-emission-control-main-battery)
**Source:** [EMCON for Ground Forces, CRFS](https://www.crfs.com/blog/emissions-control-emcon-for-ground-forces)

**THE PROBLEM:** EMCON is the military practice of controlling electromagnetic
emissions to avoid detection by enemy sensors. Modern adversaries (particularly
Russia and China) field mobile electronic warfare platforms capable of RF direction
finding, SIGINT collection, jamming, and spoofing. Any radio transmission reveals
your position. The US military is re-learning that "unplugged" operations are
essential for survival.

EMCON has graded levels, from no restrictions to total radio silence. At the
strictest level, all electromagnetic emissions cease -- no radar, no radio, no
data links. Units must coordinate using only pre-planned orders and "mission
command" (commander's intent).

**CURRENT SOLUTIONS:**
- "Mission-type orders" -- commanders issue intent-based orders before EMCON
  begins, trusting subordinates to adapt
- Pre-planned movement schedules and phase lines
- Visual signals, runners, wire communication
- The fundamental approach is human judgment guided by pre-briefed plans

**THE GAP:** Pre-planned schedules are rigid. If the situation changes during
EMCON, units cannot adapt their coordination. There is no mathematical framework
for guaranteeing that independently-acting units don't interfere with each other's
actions (transmissions, sensor sweeps, movements through choke points).

**HOW FAREY SCHEDULING HELPS:**
- Units could be pre-assigned Farey indices before EMCON begins. During radio
  silence, each unit computes its action windows from k/p.
- If a unit needs to briefly break EMCON to transmit critical data, it knows
  exactly when to transmit to avoid collision with any other unit's emergency
  transmission window.
- The schedule is deterministic and pre-computable: units can verify the full
  collision-free schedule before radio silence begins.
- **This is compelling because it replaces rigid human pre-planning with a
  mathematical guarantee that works for any number of units (up to the next prime).**

---

### 2.2 Submarine Coordination

**Source:** [Communication with Submarines, Wikipedia](https://en.wikipedia.org/wiki/Communication_with_submarines)
**Source:** [Communicating with the Silent Service, US Naval Institute Proceedings, December 1981](https://www.usni.org/magazines/proceedings/1981/december/communicating-silent-service)
**Source:** [Submarine Communications, GlobalSecurity.org](https://www.globalsecurity.org/military/systems/ship/sub-comm.htm)

**THE PROBLEM:** Submarines are the ultimate radio-silent platforms. Radio waves
do not penetrate salt water at normal frequencies. Submerged submarines receive
one-way VLF/ELF broadcasts (which can penetrate to operational depths) but
CANNOT transmit without surfacing or trailing an antenna near the surface --
which compromises their position and survival.

Nuclear ballistic missile submarines (SSBNs) operate for months with essentially
zero outbound communication. Attack submarines (SSNs) operating in contested
waters must minimize all emissions. Coordinating multiple submarines in a
battle group requires that they avoid each other's patrol areas and sensor
footprints without being able to talk.

**CURRENT SOLUTIONS:**
- Pre-planned patrol zones ("waterspace management")
- Time-phased movement corridors where only one submarine occupies a sector
  at a time
- One-way VLF/ELF broadcasts from shore to submarines (receive only)
- Acoustic communication for short-range, low-bandwidth coordination
  (but acoustic emissions can also reveal position)
- The fundamental approach: before deployment, agree on who goes where and when

**THE GAP:** Pre-planned patrol schedules are inflexible. If tactical conditions
change (an enemy submarine is detected in an unexpected location), submarines
cannot dynamically re-coordinate without breaking radio silence. The current
solution is conservative spacing -- submarines stay far apart so coordination
isn't needed, at the cost of reduced sensor coverage.

**HOW FAREY SCHEDULING HELPS:**
- Time windows for brief antenna exposure (to receive updates or transmit
  intelligence bursts) could follow a Farey schedule, ensuring no two submarines
  in a group surface simultaneously or use the same acoustic channel at the
  same time.
- The schedule adapts to group size: a task force of 3, 5, or 7 submarines
  (all primes) maps directly. Non-prime sizes round up.
- **Key advantage:** No negotiation, no signal exchange, no detectable emissions
  needed to maintain the coordination schedule.

---

### 2.3 JTRS (Joint Tactical Radio System) and Anti-Jamming

**Source:** [Joint Tactical Radio System, Wikipedia](https://en.wikipedia.org/wiki/Joint_Tactical_Radio_System)
**Source:** [JTRS, GlobalSecurity.org](https://www.globalsecurity.org/military/systems/ground/jtrs.htm)

**THE PROBLEM:** JTRS was the US military's (ultimately cancelled, over-budget)
attempt to build a universal software-defined radio. It supported anti-jam
capabilities through spread-spectrum modulation. But when jamming overwhelms
even spread-spectrum defenses, radios go silent.

**CURRENT SOLUTIONS:**
- Spread-spectrum and frequency hopping to resist jamming
- Adaptive routing to route around jammed nodes
- Low-probability-of-intercept waveforms
- When all else fails: revert to wire communication or runners

**THE GAP:** There is no standardized "what to do when the radio is completely
jammed" protocol beyond reverting to non-electronic methods.

**HOW FAREY SCHEDULING HELPS:**
- Farey scheduling could serve as the "below jam threshold" fallback. When
  frequency hopping fails because the entire band is jammed, units fall back
  to a pre-loaded Farey time schedule for coordinating actions.
- No radio needed. The schedule was computed before deployment.
- **Limitation:** This only coordinates TIMING, not the content of coordination.
  Units still need to know what to do -- Farey tells them when.

---

## 3. Self-Driving Cars and V2X Communication

### 3.1 V2X Communication Failure at Intersections

**Source:** [V2X in Autonomous Vehicles Domain, ScienceDirect (2023)](https://www.sciencedirect.com/science/article/pii/S2590198223002270)
**Source:** [Autonomous Intersection Management, UT Austin](https://www.cs.utexas.edu/~aim/)
**Source:** [V2X Communication Survey, Springer (2024)](https://link.springer.com/article/10.1007/s42154-024-00310-2)

**THE PROBLEM:** Vehicle-to-Everything (V2X) communication promises cooperative
driving where cars share positions, speeds, and intentions. But V2X has serious
failure modes:
- Signal fading in urban canyons (buildings block signals)
- Packet loss under heavy traffic (too many cars transmitting)
- Latency spikes that make real-time coordination unreliable
- Cybersecurity attacks (spoofing, denial of service)
- Mixed fleet: for decades, most cars on the road won't have V2X

The intersection is the critical scenario. Autonomous Intersection Management (AIM)
systems assume V2V communication to negotiate right-of-way. When communication
fails, the system must fall back to... what? Currently, conservative stopping
(which causes gridlock) or human takeover (which defeats the purpose).

**CURRENT SOLUTIONS:**
- Infrastructure-based (V2I): roadside units manage intersection scheduling
- Vehicle-based (V2V): cars negotiate directly
- Hybrid: combine onboard sensors with V2X data
- When V2X fails: fall back to onboard sensors only (camera, LiDAR, radar)
  and conservative behavior (slow down, increase following distance)

**THE GAP:** There is no mathematical framework for guaranteeing collision-free
intersection traversal when V2X is completely unavailable. Onboard sensors alone
cannot see around corners or through occlusions. The current fallback is
"be cautious" -- which works for safety but kills throughput.

**HOW FAREY SCHEDULING HELPS:**
- If vehicles approaching an intersection have agreed on a Farey schedule (even
  from a simple numbering: direction 1, 2, 3, 4 for N/S/E/W), each vehicle
  knows its time window to enter the intersection without needing V2X.
- The schedule could be based on lane number, approach direction, or arrival
  order (using local sensing only to determine sequence).
- **Limitation:** The hard part of intersection management is dynamic: cars
  arrive at unpredictable times. A static Farey schedule doesn't adapt to
  real-time traffic. It would work better for regular, predictable flows
  (like highway on-ramp merging) than chaotic intersections.
- **Honest assessment:** This is the weakest application domain. V2X failure
  modes are best addressed by better sensors and conservative driving, not
  by pre-computed schedules.

---

### 3.2 NHTSA Research on V2X Reliability

**Source:** [NHTSA Vehicle-to-Vehicle Communications Readiness Report (2014)](https://www.nhtsa.gov/sites/nhtsa.gov/files/readiness-of-v2v-technology-for-application-812014.pdf)
**Source:** [NHTSA V2X Communications RFC](https://www.nhtsa.gov/press-releases/us-department-transportation-releases-request-comment-rfc-vehicle-everything-v2x)

**THE PROBLEM:** NHTSA's research acknowledges that V2X reliability is not
guaranteed. The 2014 readiness report identified signal degradation, interference,
and scalability as open challenges. The FCC's decision to share the 5.9 GHz
band with unlicensed devices (WiFi 6E) created further interference risks.

**STATUS:** V2X deployment remains incomplete. Mixed fleets (V2X-equipped and
non-equipped vehicles) will coexist for decades. Any V2X-dependent coordination
system must have a fallback for when communication is unavailable.

---

## 4. Disaster Response

### 4.1 Post-Hurricane Communication Collapse

**Source:** [Hurricane Katrina Lessons Learned, White House Report (2006)](https://georgewbush-whitehouse.archives.gov/reports/katrina-lessons-learned/chapter5.html)
**Source:** [Solutions for Resilient Communication in Disaster Relief, arXiv (2024)](https://arxiv.org/html/2410.13977v1)
**Source:** [Hurricane Otis Disaster Response, Sepura](https://sepura.com/case-studies/hurricane-otis-disaster-response/)
**Source:** [FEMA Disaster Emergency Communications](https://www.fema.gov/about/offices/response/disaster-emergency-communications)

**THE PROBLEM:** When a major hurricane or earthquake strikes, communication
infrastructure is often destroyed entirely. Cell towers go down. Fiber is cut.
Power fails. First responders arrive to find they cannot coordinate because
there is no network.

Hurricane Katrina (2005) was the landmark failure: state and local authorities
"understood the devastation was serious but lacked the ability to communicate
with each other and coordinate a response." Hurricane Otis (2023) destroyed
Acapulco's entire communication infrastructure.

**CURRENT SOLUTIONS:**
- FirstNet: a dedicated nationwide broadband network for first responders, built
  on AT&T infrastructure, with priority/preemption and deployable cell sites
- Mobile cell-on-wheels (COW) and cell-on-light-truck (COLT) units
- Satellite phones (Iridium, Starlink)
- Mesh networking devices (Meshtastic, goTenna)
- Device-to-Device (D2D) communication as decentralized fallback
- Drones as temporary communication relays

**THE GAP:** All fallback systems still require SOME communication infrastructure --
even mesh networks need initial neighbor discovery. In the first hours after a
catastrophic event, when nothing works, responders must self-organize with no
communication at all. They rely on pre-planned meeting points and schedules.

**HOW FAREY SCHEDULING HELPS:**
- Rescue teams pre-assigned Farey indices could coordinate search sectors using
  time-phased schedules. Team k searches sector k/p at the corresponding time
  fraction of the operational period.
- When teams must share a limited radio channel (a single surviving repeater),
  Farey scheduling determines who transmits when -- no negotiation needed.
- **Key advantage for disaster response:** simplicity. A Farey schedule requires
  NO technology beyond a watch. Each team knows its index and the total team
  count. The schedule is deterministic.
- **Limitation:** Dynamic situations (teams discovering new survivors, areas
  becoming inaccessible) require adaptive coordination that a static schedule
  doesn't provide.

---

### 4.2 FirstNet Vulnerabilities

**Source:** [FirstNet Authority Update on Network Outage Task Force](https://firstnet.gov/newsroom/blog/firstnet-authority-update-network-outage-task-force)
**Source:** [FirstNet Outage Concern, ABC News (2024)](https://abcnews.go.com/Politics/fistnet-outage-concern-law-enforcement-leaders/story?id=107599252)

**THE PROBLEM:** FirstNet, the dedicated first-responder network, runs on AT&T
infrastructure. On February 22, 2024, an AT&T software update caused a widespread
outage that affected FirstNet subscribers. Law enforcement leaders expressed
serious concern that the backup system itself had a single point of failure.

**STATUS:** This is a real, documented vulnerability. The US first-responder
network has gone down, and there is no agreed-upon "below FirstNet" coordination
protocol.

---

## 5. Space Operations

### 5.1 Deep Space Communication Blackouts

**Source:** [NASA Delay/Disruption Tolerant Networking](https://www.nasa.gov/communicating-with-missions/delay-disruption-tolerant-networking/)
**Source:** [DTN Overview, NASA](https://www.nasa.gov/reference/delay-disruption-tolerant-networking-overview/)
**Source:** [Communication Delays, Disruptions, and Blackouts for Crewed Mars Missions, NASA (2022)](https://ntrs.nasa.gov/api/citations/20220013418/downloads/ASCEND-Communication%20Delays,%20Disruptions,%20and%20Blackouts%20for%20Crewed%20Mars%20Missions.pdf)

**THE PROBLEM:** Deep space missions face inherent communication challenges:
- **Mars communication delay:** 5-24 minutes one-way, making real-time control
  impossible
- **Solar conjunction blackouts:** When Mars passes behind the Sun (relative to
  Earth), communication is completely blocked for ~2 weeks every 26 months
- **Entry/descent/landing blackouts:** Plasma heating during atmospheric entry
  blocks all radio communication for several minutes -- exactly when the mission
  is most critical
- **Lunar far side:** No direct Earth communication is possible from the far side
  of the Moon

**CURRENT SOLUTIONS:**
- **DTN (Delay/Disruption Tolerant Networking):** Store-and-forward approach where
  each network node stores data until the next node is available
- **Autonomous schedulers:** NASA's Perseverance rover has an onboard scheduler
  that independently adapts activities when communication is delayed or unavailable
- **Relay satellites:** China's Queqiao satellite at Earth-Moon L2 relays signals
  from the lunar far side
- **Pre-planned command sequences:** Rovers receive days of commands in advance
  and execute them autonomously during blackouts

**THE GAP:** Multi-spacecraft coordination during blackouts is largely unaddressed.
When multiple rovers, orbiters, and landers operate around Mars during solar
conjunction, each must independently avoid interference (radio frequency conflicts,
simultaneous relay requests) without any Earth-based coordination.

**HOW FAREY SCHEDULING HELPS:**
- Multiple Mars spacecraft could use pre-computed Farey schedules for relay access.
  During solar conjunction (no Earth contact for ~2 weeks), each spacecraft knows
  its transmission window for the Mars relay orbiter based on its Farey index.
- **Lunar far side operations:** As more nations land missions on the lunar far
  side, relay satellite access will need scheduling. Farey-based scheduling provides
  a coordination protocol that works even without Earth contact.
- **Key advantage:** The schedule is pre-computable and verifiable before the
  mission. No in-flight negotiation needed.
- **This is genuinely useful** because space missions are pre-planned, the number
  of spacecraft is small and known, and the communication blackout periods are
  predictable.

---

### 5.2 Multi-Satellite Constellation Coordination

**Source:** [Localization of Ad-Hoc Lunar Constellations in Communication Failure Modes, NASA (2024)](https://ntrs.nasa.gov/citations/20240012984)
**Source:** [Satellite Constellation Design for Lunar Navigation, ION (2023)](https://navi.ion.org/content/70/4/navi.613)

**THE PROBLEM:** NASA's 2024 paper explicitly addresses "communication failure
modes" in ad-hoc lunar constellations. Distributed lunar constellations must
schedule communication activities, and current approaches use mixed-integer
linear programming (MILP) -- which requires centralized computation.

**HOW FAREY SCHEDULING HELPS:**
- A decentralized Farey schedule could replace centralized MILP scheduling
  for communication slot assignment in lunar constellations.
- Each satellite computes its own slot from its index. No ground station needed.
- As new satellites join the constellation, the injection principle means existing
  schedules are undisturbed.

---

## 6. Patents and Prior Art

### 6.1 Self-Organizing TDMA (STDMA)

**Source:** [In-depth Analysis of Self-Organizing TDMA, ResearchGate (2015)](https://www.researchgate.net/publication/271554066_In-depth_analysis_and_evaluation_of_Self-organizing_TDMA)
**Source:** [Distributed TDMA for Autonomous Aerial Swarms, IEEE (2024)](https://ieeexplore.ieee.org/document/10479053/)

Self-organizing TDMA (STDMA) is an existing approach where nodes claim time slots
without central coordination. The AIS (Automatic Identification System) for
maritime vessel tracking uses STDMA.

**How STDMA works:** Each node listens to the channel, identifies unused slots,
and claims one. Conflicts are resolved through a reservation/collision protocol.

**Key difference from Farey scheduling:** STDMA requires an initial listening
phase (nodes must hear each other's slot claims). Farey scheduling requires
NO listening -- each node computes its slot independently.

---

### 6.2 DESYNC Protocol (Firefly-Inspired Desynchronization)

**Source:** [DESYNC: Self-Organizing Desynchronization and TDMA, IEEE (2007)](https://ieeexplore.ieee.org/document/4379660/)

**How DESYNC works:** Inspired by fireflies that naturally desynchronize their
flashing, nodes adjust their firing times to space evenly among their neighbors.
Over several rounds, nodes converge to a collision-free TDMA schedule.

**Key properties:**
- Does NOT require a global clock
- Automatically adjusts to the number of nodes
- Reduces message loss from ~58% to <1%
- Self-maintaining and adaptive

**Key difference from Farey scheduling:** DESYNC requires multiple rounds of
communication to converge. Nodes must hear each other's "fires" to adjust.
Farey scheduling computes the final schedule immediately with zero communication.

**DESYNC is the closest existing work to our approach.** Both achieve self-organizing
TDMA without central coordination. The critical difference: DESYNC needs several
rounds of beacon exchange to converge; Farey scheduling needs zero.

---

### 6.3 US Patent US8112176B2 -- Self-Organizing Mobile Robotic Collectives

**Source:** [US8112176B2, Google Patents](https://patents.google.com/patent/US8112176/en)

This patent (inventor: Solomon Neal) covers a system of self-organizing mobile
robotic agents using hybrid AI and behavior-based control for collective operations
including mapping, coordinating missions, and forming coalitions.

**Key difference from Farey scheduling:** This patent addresses high-level task
allocation and coalition formation. Farey scheduling addresses low-level timing
coordination. They are complementary, not competitive.

---

### 6.4 TDMA Slot Allocation Patents

**Source:** [US5748624A - Time-slot Allocation in TDMA](https://patents.google.com/patent/US5748624A/en)
**Source:** [US20070133592A1 - Tree-based Spatial TDMA Scheduling](https://patents.google.com/patent/US20070133592)

Multiple patents cover TDMA slot allocation, but all require either:
- A central scheduler (base station assigns slots), or
- A distributed negotiation protocol (nodes exchange slot requests)

**No existing patent uses Farey sequences or prime-number-based mathematical
guarantees for zero-communication slot assignment.** This appears to be a
genuinely novel approach.

---

### 6.5 Chinese Remainder Theorem in Frequency Hopping

**Source:** [CRT-based Frequency Hopping Sequences, Springer (2012)](https://link.springer.com/article/10.1007/s10623-012-9774-3)
**Source:** [Frequency-Hopping Spread Spectrum, Wikipedia](https://en.wikipedia.org/wiki/Frequency-hopping_spread_spectrum)

The Chinese Remainder Theorem (CRT) has been used to construct frequency-hopping
sequences with optimal collision properties. CRT constructions require P and Q
to be coprime, and produce hopping patterns where collisions between users are
minimized.

**Connection to our work:** CRT and Farey sequences are both rooted in the
same number theory -- coprimality, modular arithmetic, the Euler totient function.
CRT addresses frequency-domain separation; Farey injection addresses time-domain
separation. They could be combined: Farey for time slots, CRT for frequency
hopping within each slot.

---

## 7. Academic Foundations

### 7.1 Schelling Focal Points (Game Theory of Coordination Without Communication)

**Source:** [Focal Point (Game Theory), Wikipedia](https://en.wikipedia.org/wiki/Focal_point_(game_theory))
**Source:** Thomas Schelling, *The Strategy of Conflict* (1960)

Thomas Schelling's Nobel Prize-winning insight: people CAN coordinate without
communication by converging on "focal points" -- solutions that are prominent
or obvious to all parties.

Classic example: asked to meet a stranger in New York City with no prior
communication, most people choose "noon at Grand Central Terminal." There is
nothing optimal about this choice; it's just the most culturally prominent one.

**Connection to Farey scheduling:** Our approach replaces cultural prominence
with mathematical certainty. Instead of hoping agents converge on the same
focal point (which requires shared cultural context), Farey scheduling provides
a universal, culture-independent focal point: the mathematically unique
collision-free schedule determined by the Farey sequence.

**Farey scheduling is a "mathematical Schelling point"** -- the provably unique,
maximally fair, collision-free time division that any agent can independently compute.

---

### 7.2 Communication-Free Multi-Robot Coordination

**Source:** [Towards Communication-Free Coordination for Multi-Robot Exploration, INRIA (2011)](https://inria.hal.science/inria-00599605v1/document)
**Source:** [Learning to Coordinate without Communication under Incomplete Information, arXiv (2024)](https://arxiv.org/html/2409.12397)
**Source:** [Task Allocation without Communication Based on Incomplete Information Game Theory, Springer (2018)](https://link.springer.com/content/pdf/10.1007/s10846-018-0783-y.pdf)

**THE PROBLEM:** Active research area. Multiple papers address how robots can
coordinate without explicit communication:

1. **Game-theoretic approaches:** Agents use Nash equilibria and regret minimization
   to select non-conflicting actions. Each agent independently computes a strategy
   that is optimal given the strategies of others.

2. **Observation-based implicit coordination:** Agents observe each other's actions
   (positions, movements) and infer intentions. This requires line-of-sight.

3. **Frontier-based exploration:** Robots choose exploration directions based on
   their position relative to other robots, counting how many robots are closer
   to each frontier. No communication needed -- just position awareness.

4. **Epistemic inference:** Recent work (2024) uses probabilistic models where
   agents build beliefs about others' plans and coordinate implicitly through
   shared probabilistic understanding.

**Key difference from all of these:** All existing communication-free methods
require either (a) observation of other agents (line of sight), or (b) learning/
convergence over multiple rounds. Farey scheduling requires NEITHER. It works
with no observation and no learning -- just two numbers (k and p).

---

## 8. Summary: The Landscape of Need

| Domain | Scale of Need | Funding Level | Status Quo When Comms Fail | Farey Fit |
|--------|--------------|---------------|---------------------------|-----------|
| DARPA Swarms (OFFSET/CODE) | 250+ drones | $100M+ programs | Revert to individual autonomy | STRONG |
| DDIL Military Ops (FLUID) | Battalion-scale | $B+ across DoD | Mission-type orders (human judgment) | STRONG |
| EMCON Naval Operations | Task force (3-20 ships) | Core doctrine | Pre-planned schedules, rigid | STRONG |
| Submarine Operations | 2-7 submarines | National security priority | Waterspace management, conservative | MODERATE |
| V2X Autonomous Vehicles | Millions of vehicles | $B+ industry | Conservative driving, slow down | WEAK |
| Disaster Response | 10-100 teams | FirstNet ($B+) | Pre-planned meeting points | MODERATE |
| Deep Space (Mars, Moon) | 3-10 spacecraft | $B+ per mission | Pre-planned sequences | STRONG |
| Satellite Constellations | 66-7000 satellites | Commercial | Centralized MILP scheduling | MODERATE |

---

## 9. What Makes Farey Scheduling Genuinely Novel

Existing approaches to coordination without communication fall into three categories:

1. **Pre-planned rigid schedules** (military EMCON, submarine waterspace management):
   Work but are inflexible and don't scale.

2. **Self-organizing convergent protocols** (DESYNC, STDMA):
   Achieve flexible schedules but require multiple rounds of communication to converge.

3. **Observation-based implicit coordination** (game theory, frontier exploration):
   Require line-of-sight observation of other agents.

**Farey scheduling occupies an empty niche:** it is simultaneously:
- **Zero-communication** (unlike DESYNC, STDMA)
- **Flexible/scalable** (unlike rigid pre-planned schedules)
- **No observation needed** (unlike game-theoretic/implicit approaches)
- **Mathematically guaranteed** collision-free (unlike probabilistic methods)
- **Instant** -- no convergence time, no learning, no negotiation

The injection principle is the mathematical foundation: when agents operate at
Farey order p (a prime), their slots provably interleave with all lower-order
agents without collision. This is not a heuristic or an approximation -- it is
a theorem.

---

## 10. Honest Limitations

We must be clear about what Farey scheduling does NOT solve:

1. **Content of coordination, not just timing.** Farey scheduling tells agents
   WHEN to act. It does not tell them WHAT to do. It must be combined with
   mission-type orders, pre-planned objectives, or autonomous decision-making.

2. **Static group composition.** The injection principle works cleanly when
   growing from F_{p-1} to F_p (adding a prime layer). Dynamic join/leave of
   individual agents requires mapping to the nearest prime frame, which is
   workable but adds complexity.

3. **Single channel only.** Farey scheduling is a 1D time-division model.
   It does not address spatial reuse (multiple agents transmitting simultaneously
   on non-interfering channels) or frequency allocation (which channels to use).

4. **Requires shared time reference.** All agents must agree on a common clock.
   This is non-trivial in some settings (though DARPA's ROCkN and STOIC programs
   are building exactly this capability).

5. **Prime constraint.** Group sizes must be rounded up to the nearest prime.
   For small groups (5, 7, 11 agents), this is negligible. For large groups
   (250 drones), the nearest prime is typically within 1-2 of the actual count.

---

## 11. Recommended Next Steps

1. **Write a short applications paper** targeting IEEE Communications Letters or
   IEEE Signal Processing Letters, demonstrating Farey TDMA with simulation
   results showing zero-collision performance vs. DESYNC convergence time.

2. **Contact DARPA program managers** for OFFSET (completed), CODE, and FLUID
   to present the approach as a "zero-bandwidth fallback" for DDIL environments.

3. **Build a simulation** showing 250 agents using Farey scheduling vs. STDMA
   vs. DESYNC, measuring: time to first collision-free schedule, bandwidth
   consumed during setup, and recovery time after agent failure.

4. **Investigate combination with CRT frequency hopping** -- Farey for time
   slots, CRT for frequency channels -- to create a full 2D (time-frequency)
   coordination scheme with zero communication.

5. **Patent consideration:** The specific combination of Farey injection +
   prime-order TDMA for zero-communication scheduling appears to have no
   prior art. A provisional patent application could protect the concept while
   the academic paper is in review.
