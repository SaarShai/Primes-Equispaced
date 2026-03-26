# Outreach & Submission Plan — Farey-Prime Scheduling

**Last updated:** March 26, 2026
**Status:** Working through this list together

---

## 1. DARPA TTO BAA HR001125S0011 — URGENT (Deadline: April 17, 2026)

**What:** Executive summary for Tactical Technology Office, office-wide BAA
**Why:** Best fit — DDIL coordination is exactly what FLUID and OFFSET successor programs need
**Documents ready:** DARPA_EXECUTIVE_SUMMARY.md + DARPA_COVER_LETTER.md

### Steps:
- [ ] **Saar:** Register at https://baa-registration.darpa.mil/ (takes 2-3 business days — do ASAP)
- [ ] **Saar:** Download full BAA + Attachment A (executive summary template) from https://sam.gov/opp/109aceb76198452b91f8ecce72b4890b/view
- [ ] **Claude:** Reformat executive summary to match Attachment A template (once downloaded)
- [ ] **Saar:** Review and approve final executive summary
- [ ] **Saar:** Package as .zip and upload through https://baa.darpa.mil/ before April 17, 4:00 PM ET
- [ ] **Saar:** Send cover letter email to HR001125S0011@darpa.mil referencing the submission

**Contacts:**
- BAA Coordinator: HR001125S0011@darpa.mil
- BAAT tech support: BAAT_Support@darpa.mil (Mon-Fri 9am-5pm ET)

---

## 2. ONR Code 311 — Long Range BAA N0001425SB001 (Rolling, by Sep 30, 2026)

**What:** 5-page white paper to Office of Naval Research, Division 311 (Machine Learning, Reasoning and Intelligence)
**Why:** Code 311 explicitly funds "decentralized collaborating teams of autonomous agents" — near-perfect match. Submarine EMCON is a primary use case.

### Steps:
- [ ] **Claude:** Draft email to Dr. Kamgar-Parsi introducing the work and asking if it fits Code 311
- [ ] **Saar:** Send email to behzad.kamgarparsi.civ@us.navy.mil
- [ ] **Saar:** Download BAA PDF from https://www.onr.navy.mil/assets/2024-10/N0001425SB001.pdf
- [ ] **Saar:** Download white paper cover page template from ONR website
- [ ] **Claude:** Write 5-page white paper (cover page + technical concept + naval relevance + cost estimate)
- [ ] **Saar:** Review and approve white paper
- [ ] **Saar:** Submit via https://submissions.nre.navy.mil

**Contacts:**
- Program Officer: Dr. Behzad Kamgar-Parsi
- Email: behzad.kamgarparsi.civ@us.navy.mil
- Code 31 contacts page: https://www.onr.navy.mil/organization/departments/code-31/code-31-contacts

---

## 3. DARPA I2O BAA HR001126S0001 (Abstract by Nov 1, 2026)

**What:** Abstract to Information Innovation Office, office-wide BAA FY2026
**Why:** I2O covers transformative AI and autonomy. Multi-agent coordination with formal guarantees fits their "trustworthy AI" thrust.

### Steps:
- [ ] **Wait** for DARPA TTO response first (~45 days after April submission)
- [ ] **Claude:** Draft 3-5 page abstract tailored to I2O thrust areas
- [ ] **Saar:** Review and approve
- [ ] **Saar:** Submit through https://baa.darpa.mil/ (same BAAT portal, same registration)

**Contacts:**
- BAA email (likely): HR001126S0001@darpa.mil (verify in BAA document)
- Download BAA: https://www.darpa.mil/work-with-us/opportunities/hr001126s0001

---

## 4. AFRL Tech Connect — Unsolicited Idea (No deadline)

**What:** Submit technology idea through Air Force's official intake portal
**Why:** Gets our work in front of AFRL subject matter experts. Low effort, potential high return.

### Steps:
- [ ] **Claude:** Draft a 1-page technology summary tailored for AFRL (autonomous UAS coordination focus)
- [ ] **Saar:** Review and approve
- [ ] **Saar:** Submit at https://airforcetechconnect.org/ (look for "lightbulb" submit icon)
- [ ] **Saar:** Also submit at contact form: https://contact.usaftechconnect.com/

**No formal page limits — this is an idea intake portal.**

---

## 5. AFRL ACT3 — Autonomy Capability Team (Watch for solicitations)

**What:** Direct outreach to AFRL's AI special operations group
**Why:** ACT3 runs the Autonomous Air Combat Operations portfolio. Swarm coordination under comms denial is directly relevant.

### Steps:
- [ ] **Claude:** Draft introductory email for ACT3 Autonomy Industry Day contact
- [ ] **Saar:** Send email to afrl.rq.autonomyindustryday@us.af.mil
- [ ] **Watch** for new solicitations at https://www.afrl.af.mil/ACT3/ and SAM.gov

---

## 6. AFRL Munitions Directorate BAA FA865125S0001 (Open through Oct 31, 2029)

**What:** Long-running BAA for Air Dominance technologies, $750M ceiling
**Why:** Could fit if framed for autonomous munitions coordination. Lower priority — pursue only if other AFRL channels show interest.

### Steps:
- [ ] **Defer** until after AFRL Tech Connect and ACT3 responses
- [ ] If interest shown, check for specific topic calls within this BAA on SAM.gov

---

## Draft Emails (Claude to prepare, Saar to send)

### Email 1: ONR Dr. Kamgar-Parsi

**To:** behzad.kamgarparsi.civ@us.navy.mil
**Subject:** White Paper Inquiry — Zero-Overhead Multi-Agent Coordination for EMCON Operations

Dear Dr. Kamgar-Parsi,

I am an independent researcher working on a formally verified method for multi-agent time coordination that requires zero scheduling overhead — no beacons, no channel sensing, no coordination messages. Each agent computes its unique collision-free time slot from a single mathematical formula, pre-loaded before deployment.

The method is based on the injection properties of Farey sequences and has been formally verified in Lean 4 (207 machine-checked declarations, zero unproven steps). Computational verification extends through 50,000 primes with zero exceptions.

I believe this work is directly relevant to ONR Code 311's research on decentralized collaborating teams of autonomous agents, particularly for submarine EMCON operations and undersea autonomous vehicle coordination where electromagnetic emissions must be minimized.

I would welcome the opportunity to discuss whether a white paper submission under BAA N0001425SB001 would be appropriate for your program. A technical report and formal proof suite are available upon request.

Respectfully,
Saar Shai
Independent Researcher
saar.shai@gmail.com

---

### Email 2: AFRL ACT3

**To:** afrl.rq.autonomyindustryday@us.af.mil
**Subject:** Inquiry — Formally Verified Coordination for Autonomous Systems Under Comms Denial

Dear ACT3 Team,

I am writing to inquire about potential interest in a formally verified method for autonomous agent coordination that operates with zero communication overhead. The method allows any number of agents to independently compute collision-free time slots using a single pre-loaded formula — with a machine-verified mathematical guarantee of zero collisions.

This addresses a specific gap in DDIL/EMCON scenarios: when a swarm of autonomous platforms loses its communication link, how do they maintain coordinated timing? Our approach requires no runtime messages, no channel sensing, and no observation of other agents.

The mathematical foundation has been formally verified in Lean 4 with 207 machine-checked results. I would welcome any guidance on relevant upcoming solicitations or the best way to engage with ACT3 on this topic.

Respectfully,
Saar Shai
Independent Researcher
saar.shai@gmail.com

---

## Timeline

| Week | Action |
|------|--------|
| **This week (Mar 26-28)** | Register on DARPA BAAT; download Attachment A; send ONR email |
| **Next week (Mar 31-Apr 4)** | Reformat exec summary to template; send AFRL emails |
| **Week of Apr 7** | Final review of DARPA submission |
| **Apr 14-17** | Submit DARPA TTO executive summary |
| **May** | Submit ONR white paper; submit AFRL Tech Connect idea |
| **June-July** | Await DARPA response (~45 days); prepare I2O abstract if TTO is encouraging |
| **Sep** | ONR full proposal if white paper is encouraged |
