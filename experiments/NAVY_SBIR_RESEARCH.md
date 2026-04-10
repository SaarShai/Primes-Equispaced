# Navy SBIR N251-060: Hypersonic CFD Solver Research

**Date:** 2026-03-28
**Status:** CLOSED (deadline was Feb 5, 2025) -- but follow-on opportunities exist

---

## 1. SOLICITATION OVERVIEW

**Topic Number:** N251-060
**Title:** Automated, Fast Computational Fluid Dynamics (CFD) Solver Technologies for Hypersonics
**Sponsoring Agency:** Office of Naval Research (ONR)
**Program:** Navy SBIR 25.1
**Official Page:** https://navysbir.us/n25_1/N251-060.htm

**Critical Technology Areas:**
- Advanced Computing and Software
- Hypersonics
- Trusted AI and Autonomy

---

## 2. WHAT THEY ARE ASKING FOR

### Objective
Develop automated and fast CFD solver technologies for accurately predicting laminar hypersonic base flows in thermo-chemical non-equilibrium, significantly reducing dependency on user expertise and computational costs during early design phases of hypersonic vehicles.

### Core Requirements
1. **10X Efficiency Improvement:** At minimum an order-of-magnitude improvement in solver efficiency and time-to-solution on heterogeneous computing platforms, with platform-independent performance gains
2. **Complex Configuration Simulation:** Simulate realistic hypersonic vehicle configurations along flight trajectories including surface roughness, thermo-chemical nonequilibrium, steps, gaps, wall temperature distribution
3. **Automated Integration:** Automated solver interface for BLT prediction tools and MDAO frameworks
4. **Pre/Post-Processing Automation:** Automated grid generation, solver parameter selection, and post-processing to minimize user intervention

### Technical Background
- Boundary Layer Transition (BLT) is critical for hypersonic weapon design
- Laminar flow heating is 4-7x lower than turbulent flow heating
- Early BLT assessment reduces Thermal Protection System (TPS) requirements
- Current barriers: grid generation time, convergence issues, method robustness, high computational cost

### Approaches They Explicitly Call Out
- **Adaptive Mesh Refinement (AMR)** -- focuses computational resources on critical areas
- High-order, low-dissipation numerical methods
- Implicit shock tracking for complex shock interactions
- GPU acceleration
- ML model training for reduced-order modeling

### Keywords (from solicitation)
Hypersonic Flows, Boundary Layer Transition (BLT), CFD Solver, Thermo-Chemical Nonequilibrium, **Automated Grid Generation, Adaptive Mesh Refinement (AMR)**, High-Performance Computing (HPC), Laminar Base Flows, Ablation, MDAO

---

## 3. DEADLINE AND TIMELINE

| Event | Date |
|-------|------|
| Pre-release | December 4, 2024 |
| TPOC direct contact window | Dec 4, 2024 - Jan 7, 2025 |
| Open for proposals | January 8, 2025 |
| Q&A deadline | January 22, 2025 (12:00 PM ET) |
| **CLOSED** | **February 5, 2025 (12:00 PM ET)** |

**STATUS: This specific solicitation is CLOSED. See Section 8 for next steps.**

---

## 4. FUNDING AMOUNTS

### Phase I (Feasibility - 6-12 months)
| Component | Amount |
|-----------|--------|
| Base | $140,000 |
| Option | $100,000 |
| **Total Phase I** | **$240,000** |
| TABA (additional) | $6,500 |

### Phase II (Development - up to 24 months)
| Component | Amount |
|-----------|--------|
| **Standard Phase II** | **up to $1,800,000** |
| Sequential Phase II | up to $1,970,000 additional |
| Phase II TABA | up to $50,000 |

### Phase III (Transition/Commercialization)
- No SBIR funding limit; funded by DoD procurement or commercial sales
- Collaboration with industry partners and DoD agencies

**Total potential SBIR funding per project: ~$4M+ across phases**

---

## 5. HOW TO APPLY

### Portal
All proposals MUST be submitted through **DSIP (Defense SBIR/STTR Innovation Portal)**:
https://www.dodsbirsttr.mil/submissions/

### Required Registrations (START THESE NOW -- they take weeks)
1. **SAM.gov** -- Get Unique Entity ID (UEI) and CAGE code
   - https://sam.gov
2. **SBA Company Registry** -- Get SBC Control ID
   - https://www.sbir.gov
3. **DSIP Account** -- Uses Login.gov authentication
   - https://www.dodsbirsttr.mil/submissions/

**CRITICAL:** Legal name and address must match EXACTLY across SAM.gov, SBIR.gov, and DSIP.

### Proposal Format
- Submitted as multiple volumes through DSIP
- Volume 7 requires "Disclosures of Foreign Affiliations or Relationships to Foreign Countries" webform
- Phase I is Firm Fixed Price contract
- Phase II is typically Cost Plus Fixed Fee

### Reference Documents
- Navy Phase I Instructions: Navy_SBIR_251_v3.pdf (at navysbir.com)
- DoD SBIR Program Solicitation preface at dodsbirsttr.mil

---

## 6. ELIGIBILITY REQUIREMENTS

### Must Be:
- **For-profit US small business** (Small Business Concern / SBC)
- **500 or fewer employees** (including affiliates)
- **51%+ US-owned** (by US citizens or permanent resident aliens)
- **Located in the United States** with primary operations in US
- **R&D performed in the US**

### Principal Investigator:
- Must be "primarily employed" by the small business during award
- Cannot be full-time employed elsewhere

### Legal Structure:
- Individual proprietorship, partnership, LLC, corporation, joint venture, association, trust, or cooperative
- Joint ventures: less than 50% foreign participation

### Export Controls (IMPORTANT):
- Topic is subject to **ITAR** (22 CFR Parts 120-130) and **EAR** (15 CFR Parts 730-774)
- Must disclose all foreign nationals, visa status, and assigned tasks

---

## 7. FIT ANALYSIS: FAREY AMR vs. N251-060 REQUIREMENTS

### Direct Match Points

| N251-060 Requirement | Farey AMR Capability | Fit |
|----------------------|---------------------|-----|
| 10X solver efficiency improvement | **7-15x demonstrated on shocks** | STRONG MATCH |
| Adaptive Mesh Refinement | **Core technology -- Farey-mediant based AMR** | EXACT MATCH |
| Automated grid generation | **Mathematically automated via Farey sequences** | STRONG MATCH |
| Reduce user expertise dependency | **Number-theoretic rules eliminate manual tuning** | STRONG MATCH |
| Platform-independent gains | **Algorithmic improvement, not hardware-dependent** | STRONG MATCH |
| GPU acceleration | Needs development | GAP |
| Thermo-chemical nonequilibrium | Needs domain-specific implementation | GAP |
| Complex 3D vehicle geometries | Needs extension from current 1D/2D work | GAP |
| BLT prediction integration | Needs coupling with stability analysis tools | GAP |

### Key Selling Points
1. **AMR is explicitly listed as a keyword and promising approach** in the solicitation
2. Our 7-15x speedup on shock problems is in the right ballpark for their 10x requirement
3. The mathematical foundation (Farey mediants) provides provably optimal mesh refinement -- no user tuning needed
4. Approach is fundamentally algorithmic, so it compounds with GPU acceleration (could exceed 10x)

### Gaps to Address
1. Need to extend to 3D hypersonic-relevant test cases
2. Need thermo-chemical nonequilibrium solver coupling
3. Need GPU implementation for Phase II
4. Need domain expertise partner (hypersonics lab or existing CFD company)

### Competitive Landscape
- At least one Phase I award was made under N251-060 to a firm proposing "high-order U-MUSCL scheme and automated mesh generation and adaptive refinement capability" for the Kestrel CFD suite (~$139,733)
- CFD Research Corporation (Huntsville, AL) is a major player in SBIR hypersonic CFD
- Spectral Sciences, Inc. has related Army STTR work on hypersonic modeling

---

## 8. NEXT STEPS AND ALTERNATIVE OPPORTUNITIES

### N251-060 is CLOSED, but:

#### A. Navy 25.2 SBIR -- N252-100 (OPEN NOW)
**Title:** Efficient Multiphysics Modeling Framework for Rain-Induced Damage and Aerodynamic Effects on Hypersonic Vehicles
- **Sponsor:** ONR
- **Opens:** April 23, 2025
- **Closes:** May 21, 2025
- **Explicitly requires AMR** for tracking flow features
- **Requires GPU acceleration**
- **URL:** https://www.navysbir.com/n25_2/N252-100.htm

#### B. Navy 25.B STTR -- N25B-T033
**Title:** Hypersonic CFD Heat Flux Sub-Models Development
- **Closed:** May 21, 2025
- NAVAIR sponsored, targets Kestrel CFD solver improvements

#### C. Navy 25.2 SBIR -- N252-120
**Title:** Plasma Modeling and Simulation for Hypersonics
- Strategic Systems Programs (SSP)
- Related computational hypersonics work

#### D. Upcoming 26.x Solicitations
- SBIR program was reauthorized March 17, 2026 (after Oct 2025 lapse)
- DoD 26.1 solicitations expected March-April 2026
- **Hypersonics remains a top DoD SBIR priority area**
- Monitor: https://www.dodsbirsttr.mil/topics-app/

### Recommended Strategy
1. **IMMEDIATE:** Start SAM.gov and SBA registrations NOW (takes 2-4 weeks)
2. **IMMEDIATE:** Register on DSIP portal
3. **SHORT-TERM:** Prepare for 26.1 solicitation cycle (expected any day now)
4. **SHORT-TERM:** Develop 3D hypersonic benchmark results with Farey AMR
5. **MEDIUM-TERM:** Identify a hypersonics domain partner (university lab or existing CFD firm)
6. **MEDIUM-TERM:** GPU implementation of Farey AMR algorithm

---

## 9. KEY CONTACTS AND RESOURCES

| Resource | URL |
|----------|-----|
| Navy SBIR Home | https://www.navysbir.com/ |
| DoD DSIP Portal (submissions) | https://www.dodsbirsttr.mil/submissions/ |
| DoD Topic Search | https://www.dodsbirsttr.mil/topics-app/ |
| SBIR.gov (registration) | https://www.sbir.gov |
| SAM.gov (entity registration) | https://sam.gov |
| DoD SBIR Help Desk | DoDSBIRSupport@reisystems.com |
| N251-060 Topic Page | https://navysbir.us/n25_1/N251-060.htm |
| N252-100 Topic Page | https://www.navysbir.com/n25_2/N252-100.htm |

---

## 10. REFERENCES FROM SOLICITATION

Key papers cited in N251-060 (for literature review):
1. Schneider (2004) -- Hypersonic laminar-turbulent transition on circular cones and scramjet forebodies
2. Hader & Fasel (2018) -- Natural transition via random inflow disturbances
3. Paredes et al. (2011) -- Planar PSE methodology
4. Nichols & Candler (2019) -- Input-output analysis for hypersonic boundary layers
5. Kamal et al. (2020) -- One-Way Navier-Stokes equations
6. Browne et al. (2019) -- Efficient wavepacket tracking for stability prediction
7. Peck et al. (2024) -- Boundary-layer instability on swept fin
8. Johnston & Candler (2023) -- BoLT-2 hypersonic boundary layer transition
9. Dong et al. (2024) -- Hypersonic turbulent boundary layer over lifting body

---

## BOTTOM LINE

**The N251-060 solicitation is a near-perfect match for Farey AMR technology.** AMR is explicitly called out as a key approach, the 10x efficiency target aligns with our 7-15x demonstrated improvement, and automated grid generation is a core requirement that maps directly to our number-theoretic approach.

**The specific 25.1 window is closed**, but the Navy continues to solicit hypersonic CFD improvements across multiple cycles. The critical action items are:
1. Get registered (SAM.gov, SBA, DSIP) immediately
2. Watch for 26.1 topics (imminent)
3. Build 3D hypersonic benchmarks to strengthen proposal
4. Find a domain partner with hypersonics expertise
