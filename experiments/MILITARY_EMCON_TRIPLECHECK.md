# Military EMCON Triple-Check: Does Farey Scheduling Provide REAL Value?

**Date:** 2026-03-29
**Purpose:** Rigorous, adversarial validation of Farey scheduling for military EMCON swarm operations
**Verdict:** MIXED -- there is a genuine niche, but it is far narrower than the technical report implies

---

## 1. How Military EMCON Actually Works Today

### EMCON Levels
Military EMCON is a spectrum, not binary on/off:
- **EMCON Alpha (Total Silence):** All emissions off. Even microwaves. Ships/subs are ghosts.
- **EMCON Selective/Restricted:** Tailored list of permitted emitters, frequencies, power levels, and timing windows. E.g., "encrypted burst SATCOM at scheduled windows only."
- **EMCON Reduced:** Most emissions off, specific mission-critical systems allowed at low power.

### What They Actually Use for Scheduling
**Link 16 / JTIDS / MIDS** is the NATO standard tactical data link:
- TDMA with 1,536 time slots per 12-second frame (128 slots/second)
- 98,304 slots per 12.8-minute epoch
- Slots pre-assigned to users or groups via Network Participation Groups (NPGs)
- Frequency-hopping across 51 frequencies for jam resistance
- Crypto-protected slot assignments
- Requires GPS synchronization via a Network Time Reference (NTR)

**HAVE QUICK / SATURN:** Frequency-hopping voice comms
- Pre-loaded Word of the Day (WOD) + GPS time + net ID
- Pseudorandom hopping pattern derived deterministically
- Already achieves "zero real-time coordination" for frequency selection
- SATURN replaced HAVE QUICK across NATO by 2022

### Key Finding: The military ALREADY uses deterministic, pre-computed scheduling
Link 16 slot assignments and HAVE QUICK frequency patterns are pre-loaded before missions. Agents compute their behavior from shared secrets + time. This is conceptually similar to what Farey scheduling proposes, except the military versions are battle-tested, encrypted, and integrated into existing doctrine.

---

## 2. Does the Military ACTUALLY Need This?

### When Forces Go EMCON
Real EMCON scenarios from doctrine and recent conflicts:

1. **Submarine patrols:** SSBNs maintain total radio silence for months. They coordinate via pre-planned OPLANs. They receive (but don't transmit) via ELF/VLF. They do NOT need to coordinate with each other in real-time -- they operate independently in assigned patrol areas.

2. **Special operations:** Teams go radio silent during infiltration. They use pre-planned timing (H-hour minus X) and hand signals. Coordination is pre-briefed, not computed on the fly.

3. **Surface ships approaching hostile territory:** EMCON during approach phase. Coordination via pre-briefed movement plans, not real-time scheduling.

4. **Drone swarms in contested EW environment:** THIS is the most relevant scenario. Ukraine has demonstrated massive EW capability disrupting drone comms. DARPA programs (OFFSET, CODE) address this.

### The Honest Answer About Coordination Need
In most EMCON scenarios, forces do NOT need to coordinate dynamically during radio silence. They:
- Pre-brief all coordination before going silent
- Use "mission command" -- subordinates execute commander's intent autonomously
- Rely on time-based schedules agreed before EMCON begins
- Break radio silence only with "justifiable cause"

The 2024 US Army doctrine explicitly states: leaders must learn to issue mission-type orders and feel comfortable receiving only periodic updates. The doctrine solution to EMCON is NOT better scheduling algorithms -- it is better pre-planning and more autonomous decision-making.

### Where Dynamic Coordination IS Needed
The one scenario where Farey scheduling could matter:
- **Large drone swarms (50-250 units) that lose communication mid-mission** due to enemy jamming
- They need to share a single channel (or time-divided resource) without collisions
- The swarm size may change (units destroyed, new units arriving)
- Pre-programmed TDMA breaks if units are lost (wasted slots) or added (no slots for newcomers)

This is a REAL problem. But how big is it compared to what exists?

---

## 3. Does Monotone Nesting ACTUALLY Survive Unit Loss?

### The Claim
F_N subset of F_{N+1}: adding unit N+1 doesn't change existing schedules.

### The Critical Problem (Identified in the Question)
**Removing a unit DOES leave a gap.** If you have 10 units operating on F_11 (slots k/11 for k=1..10) and unit #3 is destroyed:
- Unit #3's slot (3/11) goes unused
- The remaining 9 units keep their slots -- no disruption
- BUT: channel utilization drops from 10/11 to 9/11
- The remaining units are NOT equivalent to F_10. They are F_11 minus one element.

### Does This Actually Matter?
**For the "no disruption" claim: YES, it works.** The surviving units don't need to change anything. They just keep transmitting at their assigned times. The dead unit's slot becomes wasted but causes no collision.

**For the "100% utilization" claim: NO, it fails under attrition.** If 3 of 10 units die, utilization drops to 7/10. Pre-programmed TDMA has the exact same problem -- dead units leave empty slots.

**For unit addition: the nesting IS genuinely useful.** Moving from p=11 to p=13 (adding 2 new units) preserves all existing 10 slots and adds 2 new ones at positions that are guaranteed non-colliding. Traditional TDMA would need to either have pre-reserved spare slots or do a full reassignment.

### Honest Assessment of Nesting
- **Adding units: REAL advantage** over traditional pre-planned TDMA
- **Removing units: NO advantage** over traditional TDMA (both waste the dead unit's slot)
- **Reclaiming dead slots: IMPOSSIBLE without communication** in either Farey or traditional TDMA
- The claim "no communication needed" is correct for the schedule itself, but if you want to recover wasted capacity, you need to somehow communicate the new group composition -- which requires communication.

---

## 4. Comparison to What Military Already Uses

### Link 16 TDMA
| Property | Link 16 | Farey Scheduling |
|----------|---------|-----------------|
| Zero-communication | No (needs NTR sync) | Yes (if clocks are synced) |
| Pre-computed | Yes (slot tables loaded pre-mission) | Yes (just k and p) |
| Collision-free | Yes (deterministic TDMA) | Yes (injection theorem) |
| Dynamic scaling | Poor (needs new slot table) | Good (prime increment) |
| Handles unit loss | Wastes slots | Wastes slots (same) |
| Jam-resistant | Yes (freq hopping + crypto) | No (single channel) |
| Battle-tested | 40+ years operational use | Zero operational use |
| GPS required | Yes (for NTR sync) | Yes (for time sync) |
| Encrypted | Yes | No inherent encryption |

### HAVE QUICK / SATURN
Both HAVE QUICK and Farey scheduling derive behavior deterministically from pre-loaded parameters. HAVE QUICK uses (WOD, TOD, NetID) -> frequency pattern. Farey uses (k, p) -> time slot. The conceptual approach is identical. The difference: HAVE QUICK solves frequency selection, Farey solves time-slot selection.

### Critical Observation: GPS Dependency
Both Link 16 and Farey scheduling require precise time synchronization. Without GPS (or equivalent), neither works. The military is investing billions in GPS-denied timing (DARPA ROCkN, HORDE PNT, chip-scale atomic clocks). If GPS-denied timing is solved, it benefits both Link 16 AND Farey equally.

**If GPS is denied, Farey scheduling has the same vulnerability as existing TDMA systems.** The problem isn't the slot assignment algorithm -- it's the time synchronization.

---

## 5. Quantified Gain Assessment

### Scenario: 10 submarines, 30-day patrol, periodic burst coordination

**Reality check:** Submarines on deterrent patrol do NOT coordinate with each other. Each SSBN operates independently in its assigned patrol area. This scenario is fabricated -- it doesn't match real submarine operations.

### Scenario: 100-drone swarm, urban operations, enemy jamming

This is the realistic scenario. Let's compare:

**Pre-programmed TDMA (100 slots, pre-assigned):**
- Works perfectly if all 100 drones survive and no new drones join
- If 20 drones are destroyed: 20% wasted slots, but 80 remaining drones are fine
- If 10 new drones arrive: NO slots available unless pre-reserved spares exist
- Mitigation: reserve spare slots (e.g., 120 slots for 100 drones) -- wastes 20% upfront

**Farey scheduling (p=101, prime):**
- Each drone gets slot k/101
- If 20 drones destroyed: same 20% waste, remaining 80 are fine (identical to TDMA)
- If 10 new drones arrive: upgrade to p=113, all existing slots preserved, 12 new slots added
- No need for pre-reserved spares

**Pure ALOHA (the strawman):**
- Nobody in the military uses pure ALOHA for mission-critical tactical scheduling
- Slotted ALOHA is used for low-data-rate satellite and RFID -- not for time-critical swarm coordination
- Comparing to ALOHA's 18-37% efficiency is misleading because ALOHA is not the actual competitor

**The REAL competitor: Dynamic TDMA with spare slots:**
- Pre-assign 100 drones to 130 slots (reserve 30 spares)
- New arrivals take the next spare slot (requires only knowing "I am drone 101, take spare slot 1")
- Utilization: 100/130 = 77% initially, vs Farey's 100/101 = 99%
- Farey advantage: ~22% better utilization initially
- After 20 losses: 80/130 = 62% vs 80/101 = 79% -- Farey advantage: ~17%

### Honest Quantification
**Farey's real advantage over pre-planned TDMA with spares: approximately 15-25% better channel utilization in dynamic scenarios.** This is meaningful but not revolutionary.

**The advantage disappears entirely if:**
- The force composition is known and stable (most military operations)
- There are only a few spare slots needed (small uncertainty)
- The system already uses frequency-hopping across many channels (Link 16's 51 frequencies)

---

## 6. Patent Landscape

### Existing IP in Military Scheduling
The search found several relevant patents:
- **US 7,433,340:** Staggering forward/reverse channel time slot allocation (general TDMA)
- **US 2013/0100942:** Dynamic TDMA slot assignments for MANETs (Harris Corporation)
- **JP 2003-009223:** Slot allocation algorithm

### Number-Theoretic Scheduling
**No patent was found combining Farey sequences, Stern-Brocot trees, or number-theoretic methods with TDMA scheduling.** This is a genuine gap in the patent landscape.

However, the "Zero-Exposure Distributed TDMA" protocol (IEEE, 2012) achieves zero-communication slot assignment through a different mechanism, and "Distributed TDMA for Autonomous Aerial Swarms" (IEEE Access, 2024) addresses swarm scheduling with self-organizing protocols.

### ITAR Considerations
A general-purpose scheduling algorithm based on Farey sequences would likely qualify as "fundamental research" and be exempt from ITAR controls, since it is based on standard mathematical principles taught in universities. However, if it were specifically designed for and integrated into a weapons system, ITAR could apply.

---

## 7. Skeptical Questions Answered

### "If Farey scheduling is so good, why hasn't anyone adopted number-theoretic scheduling in 70 years?"

**Honest answer: because the problem it solves rarely arises in practice.**

- Most military operations pre-plan their schedules. The group composition is known before the mission.
- When communication is available, dynamic TDMA protocols handle changes.
- When communication is denied, forces default to pre-planned schedules and autonomous behavior.
- The specific niche of "we need a new schedule AND we can't communicate AND the group size changed" is very narrow.
- Also: the military is extremely conservative about adopting new scheduling schemes. Link 16 has been the standard for 40+ years. Changing it requires billions in new equipment and training.

### "Is there a fundamental reason militaries prefer centralized scheduling?"

**Yes:** Centralized scheduling allows for priority assignment, quality of service, and security compartmentation. A commander can give AWACS more slots than a fighter. Link 16's NPG system allows flexible prioritization. Farey scheduling assigns equal-sized slots to all agents -- there is no priority mechanism. This is a significant operational limitation.

### "Are ITAR/classification concerns blocking publication?"

The fundamental mathematics (Farey sequences, injection theorems) is public domain and ITAR-exempt. The specific application to military systems might face review if it contained classified operational details, but a pure algorithm paper would not.

---

## 8. OVERALL HONEST ASSESSMENT

### What IS Genuinely Novel and Useful

1. **The mathematical guarantee is real.** The injection theorem is proven and machine-verified. No existing zero-communication scheduling scheme has this level of mathematical certainty.

2. **The nesting property for unit addition is genuinely useful.** Going from p to the next prime and preserving all existing assignments is elegant and has no exact equivalent in existing TDMA systems.

3. **The IP landscape is open.** No existing patent covers number-theoretic TDMA scheduling based on Farey sequences.

4. **The concept maps cleanly to a real (if narrow) operational need.** Drone swarms losing communication mid-mission is a demonstrated real-world problem (Ukraine).

### What Is Overstated

1. **"100% channel utilization vs ALOHA's 37%"** -- This comparison is misleading. Nobody uses ALOHA for tactical TDMA scheduling. The real competitor is pre-programmed TDMA, which also achieves near-100% utilization when the group is stable. The honest comparison shows 15-25% improvement in dynamic scenarios.

2. **"Zero-communication scheduling"** -- True for the schedule itself, but the system still requires synchronized clocks (GPS or equivalent), a shared prime p, and knowledge of your index k. Setting up these parameters requires communication before EMCON. Traditional TDMA requires the same setup.

3. **"The military doesn't have a solution for the zero-bandwidth case"** -- They do: it's called "pre-planned schedules from the OPLAN." The existing solution is organizational, not algorithmic. Farey offers an algorithmic improvement, but the claim of filling an unmet need is overstated.

4. **"Monotone nesting means adding/removing units doesn't disrupt"** -- Adding: true. Removing: no advantage over standard TDMA (both waste the slot). The report should separate these cases clearly.

5. **No priority mechanism** -- Equal slot sizes for all agents is a feature for sensor coordination but a bug for tactical communications where AWACS needs 10x the bandwidth of a fighter.

### Realistic Market Position

**Farey scheduling is a mathematically elegant solution to a real but narrow problem.** Its best-fit scenario is:

- Medium-to-large autonomous swarms (50-500 units)
- Operating in GPS-available but RF-denied environments
- Where group composition changes during the mission
- And agents need collision-free access to a shared time resource
- And there is no command hierarchy requiring priority differentiation

This describes: drone swarms under enemy jamming. Not submarines (they don't coordinate in real-time). Not special forces (too few units, pre-brief everything). Not surface fleet EMCON (use Link 16 in degraded mode, or pre-planned schedules).

### Recommended Next Steps (if pursuing this)

1. **Stop comparing to ALOHA.** Compare to pre-planned TDMA with spare slots. Show the 15-25% utilization advantage honestly.
2. **Add a priority extension.** Assign higher-priority units to fractions with smaller denominators (they get larger gaps around their slot). This is mathematically natural with Farey sequences.
3. **Address the GPS dependency explicitly.** Partner with GPS-denied timing work (DARPA ROCkN).
4. **Focus the pitch on drone swarms specifically.** Drop the submarine/SSBN framing entirely -- it doesn't match operational reality.
5. **Acknowledge the "Zero-Exposure Distributed TDMA" (IEEE, 2012) work.** This is a direct competitor that achieves zero-communication slot assignment through a different mechanism. Differentiate clearly.
6. **Consider the civilian market.** IoT sensor networks, autonomous vehicle coordination, and satellite constellation scheduling may have better product-market fit than military EMCON.

### Classification (per Aletheia framework)
- **Autonomy: Level C** (Human-AI Collaboration -- math is known, application is novel framing)
- **Significance: Level 1** (Minor Novelty -- elegant application of known math to a narrow problem, insufficient depth for publication in a top venue without substantial additional results)
- **Verification Status: Step 1 partial** (math verified, operational claims NOT verified against real military ops)

---

## Sources

- [Radio Silence - Wikipedia](https://en.wikipedia.org/wiki/Radio_silence)
- [Understanding EMCONs - Its Released](https://itsreleased.com/emcons-electronic-emissions-control-modern-warfare/)
- [Adapting to Multi-Domain Battlefield: Developing EMCON SOPs - US Army](https://www.army.mil/article/284546/adapting_to_multi_domain_battlefield_developing_emissions_control_sop)
- [Mission Command Means Emissions Control - USNI Proceedings](https://www.usni.org/magazines/proceedings/2021/may/mission-command-means-emissions-control)
- [JTIDS - Wikipedia](https://en.wikipedia.org/wiki/Joint_Tactical_Information_Distribution_System)
- [Link 16 - Wikipedia](https://en.wikipedia.org/wiki/Link_16)
- [Have Quick - Wikipedia](https://en.wikipedia.org/wiki/Have_Quick)
- [Command and Control of Strategic Submarines - NSL Archive](https://archive.navalsubleague.org/1990/command-and-control-of-strategic-submarines)
- [When Radios are Jammed, Fight Like Ants - Modern War Institute at West Point](https://mwi.westpoint.edu/radios-jammed-fight-like-ants-swarms-soldiers-future-battlefield/)
- [Beyond GPS: HORDE PNT - Military Embedded Systems](https://militaryembedded.com/comms/gps/beyond-gps-horde-pnt-for-contested-environments)
- [ROCkN Enables GPS-Free Operations - DARPA](https://www.darpa.mil/news/2026/rockn-enables-gps-free-operations)
- [Zero-Exposure Distributed TDMA - IEEE](https://ieeexplore.ieee.org/document/6133512/)
- [Distributed TDMA for Autonomous Aerial Swarms - ResearchGate, 2024](https://www.researchgate.net/publication/379296705_Distributed_TDMA_Scheduling_for_Autonomous_Aerial_Swarms_A_Self-Organizing_Approach)
- [Adaptive Slot Assignment for TDMA Airborne Networks - Springer](https://link.springer.com/chapter/10.1007/978-3-319-78139-6_27)
- [Dynamic TDMA Slot Assignments for MANETs - US Patent 2013/0100942](https://patents.google.com/patent/US20130100942A1/en)
- [ITAR - Wikipedia](https://en.wikipedia.org/wiki/International_Traffic_in_Arms_Regulations)
- [Expanding EMCON Scope - Australian Army Cove](https://cove.army.gov.au/article/expanding-scope-emissions-control-enhance-command-and-control-node-survivability-within-3rd-combat-brigade)
