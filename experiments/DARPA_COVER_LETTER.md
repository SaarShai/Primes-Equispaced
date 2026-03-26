# Cover Letter: Farey-Prime Scheduling Executive Summary

**From:** Saar Shai, Independent Researcher
**To:** DARPA Tactical Technology Office, BAA HR001125S0011
**Date:** March 2026
**Subject:** Executive Summary -- Farey-Prime Scheduling for Zero-Overhead Multi-Agent Time Coordination

---

Dear Program Manager,

When autonomous agents lose their communication link, they lose the ability to coordinate. Today there is no proven method for a group of drones, submarines, or ground vehicles to guarantee collision-free timing without first exchanging scheduling messages. The attached executive summary describes a solution: Farey-Prime Scheduling, a mathematically proven coordination method where each agent computes its unique time slot from a single formula — with zero communication overhead and a machine-verified guarantee of zero collisions.

**The problem:** When autonomous agents operating under EMCON or DDIL conditions must share a time resource -- a transmission channel, a sensor window, a movement corridor -- current methods require either runtime communication to negotiate the schedule, or rigid pre-planned assignments that cannot accommodate new agents.

**The solution:** Farey-Prime Scheduling allows each agent to compute its unique, collision-free time slot from just two pre-loaded integers (an index and a prime). No runtime communication, channel sensing, or observation of other agents is needed to determine the schedule. The collision-freedom guarantee has been formally verified in the Lean 4 proof assistant with 24 machine-checked theorems and zero unproven steps -- a level of formal assurance that is, to our knowledge, unprecedented for a scheduling protocol.

**What is genuinely novel:** The hierarchical injection property. When a group scales from prime p to the next prime q, all existing slot assignments are preserved and new agents slot into gaps without any reassignment. No prior work in the TDMA or topology-transparent scheduling literature provides this specific property in a zero-overhead context. We have conducted an honest competitive analysis against CRT-based topology-transparent scheduling, DESYNC, STDMA, and probabilistic methods; the comparison is detailed in the attached summary.

**What this is not:** Farey scheduling is not a replacement for communication. Agents still transmit data during their assigned slots. The value is eliminating the scheduling negotiation itself -- zero bandwidth, zero time, and zero emissions consumed on meta-coordination.

This work is directly relevant to the coordination challenges addressed by DARPA FLUID (the zero-bandwidth floor of the DDIL degradation curve) and the legacy of OFFSET and CODE (swarm coordination under communication denial). I am seeking Phase 1 funding for scalable simulation, formal verification extension, and peer-reviewed publication, with a path toward software integration and hardware demonstration in subsequent phases.

I welcome the opportunity to discuss this work with the appropriate program manager. The full technical report, Lean 4 proof suite, and simulation code are available upon request.

Respectfully,

Saar Shai
Independent Researcher
