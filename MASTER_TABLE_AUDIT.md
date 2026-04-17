# MASTER TABLE AUDIT REPORT
**Date:** 2026-04-04
**Audited by:** Opus sub-agent
**Sources:** MASTER_TABLE.md, SESSION9_HANDOFF.md, SESSION10_HANDOFF.md, conversation_user_msgs.txt (200+ messages), ~/.farey_research/results/ (196 files)

---

## 1. Missing Items (not in MASTER_TABLE)

### 1A. SESSION 10 DISCOVERIES (CRITICAL -- these are the headline results)

| # | Direction | Where Mentioned | Suggested Status | Notes |
|---|-----------|-----------------|------------------|-------|
| M1 | **Chebyshev Bias for Farey Discrepancy (full framework)** | SESSION10_HANDOFF lines 23-37, CHEBYSHEV_BIAS_FAREY.md | 🟩 STRONG, Phase 📊 | The central discovery of Session 10. Phase-lock to gamma_1 (R=0.77), density prediction 0.47 vs 0.462. Should be a top-level MPR item, not just a sub-note on MPR-35. |
| M2 | **B'/C' = alpha + rho algebraic identity** | SESSION10_HANDOFF line 69, ALPHA_RHO_IDENTITY_DERIVATION.md | 🟢 PROVED, Phase 📊 | Exact algebraic identity proved from first principles. Not tracked as its own item. |
| M3 | **Unconditional: both signs infinitely often (Ingham adaptation)** | SESSION10_HANDOFF lines 10, 42-43, UNCONDITIONAL_PHASE_LOCK.md | 🟩 STRONG (needs adversarial verify), Phase 🔬 | DeltaW(p) takes both signs infinitely often with positive logarithmic density. This is an unconditional theorem. Session 10 recommends adversarial verification. |
| M4 | **Perron integral: T(N)+M(N) = residues + sum over zeta zeros (GRH)** | SESSION10_HANDOFF line 52, PERRON_INTEGRAL_T.md | 🟩 STRONG (conditional GRH), Phase 📊 | Adversarially verified (1 minor error corrected). Not in MASTER_TABLE. |
| M5 | **L-function generalization (twisted Farey discrepancy)** | SESSION10_HANDOFF lines 33-34, 59, 108, TWISTED_FAREY_DISCREPANCY.md | 🟩 STRONG, Phase 🔬 | chi mod 4 locks at 6.02, chi mod 3 locks at 8.04. Cross-control anomaly (4.1x) still needs investigation. |
| M6 | **Multi-scale T(N) decomposition: M(N/2)+M(N/3)+M(N/5) explain 96%** | SESSION10_HANDOFF line 35, MULTISCALE_T_ANALYSIS.md | 🟩 STRONG (computational), Phase 🧪 | Major computational finding. Not tracked. |
| M7 | **GRH+LI: Limiting density of DeltaW < 0 is exactly 1/2** | SESSION10_HANDOFF line 55 | 🟩 STRONG (conditional GRH+LI), Phase 📊 | Full Rubinstein-Sarnak framework applies. Not tracked. |
| M8 | **5-zero joint phase structure** | SESSION10_HANDOFF line 62 | 🧪 (computational), Phase 🧪 | All 5 leading zeta zeros phase-lock independently (p < 10^{-18}). |
| M9 | **Stern-Brocot test: per-level discrepancy vs Gauss map eigenvalues** | SESSION10_HANDOFF line 104 | ⬜ UNEXPLORED, Phase 🔬 | Listed as short-term priority in Session 10 but never added to MASTER_TABLE. |
| M10 | **Quantum chaos direction: operator on PSL(2,Z)\H with trace T(N)** | SESSION10_HANDOFF line 109 | ⬜ UNEXPLORED, Phase 🔬 | Listed as medium-term priority in Session 10. Note: PHYS-5 covers cold atoms/quantum chaos but NOT this specific operator direction. MPR-31 mentions quantum chaos generically but has no content. |

### 1B. APPLICATION DIRECTIONS FROM CONVERSATION

| # | Direction | Where Mentioned | Suggested Status | Notes |
|---|-----------|-----------------|------------------|-------|
| M11 | **Conformal mapping + Farey triangulation** | User msg [5], [38], [49], CONFORMAL_MAPPING_ASSESSMENT.md, CONFORMAL_PAPER_OUTLINE.md | 🟨 MODERATE, Phase 🔬 | User explicitly requested exploration. Agent found nesting confirmed but quality worse than uniform. Paper outline exists. Currently tracked as MESH-1 but with stale description ("BPS framework"). Should reflect conformal mapping angle. |
| M12 | **Cognitive radio / blind rendezvous** | User msg [7], agent completed "Research cognitive radio application" | 🟨 MODERATE, Phase 📝 | Report written. IOT-2 exists but says "Simplest blind rendezvous (k*t mod p)". Status should note the report is done. |
| M13 | **MIMO pilot contamination** | User msg [6], agent completed "Research MIMO pilot contamination" | ⬜ or 🟨, Phase 📊 | Research done, deep value analysis completed. Conclusion: crowded field, incremental. IOT-3 exists but status is stale ("Reframed for satellite"). |
| M14 | **3D gaming pipeline / mesh shaders** | User msg [17] item 5, [19] (deep dive), [21] item 2 | ⬛ DEAD (partially), Phase 📊 | User asked to explore. Agent found Nanite shipped fix (UE 5.4). Mesh shader trend confirmed real but Farey advantage minimal. MESH-5 covers Nanite as DEAD but the mesh shader trend investigation is not tracked. |
| M15 | **AI/ML upscaling (cutting-edge 3D graphics)** | User msg [21] item 4, [22] agent completed | 📊 assessed, Phase 📊 | GRAPHICS_APPLICATION_REPORT.md written. Two strong areas found: 3DGS densification (already tracked) and neural LOD (not tracked). |
| M16 | **Progressive geometry compression** | User msg [30], agent "Verify progressive compression claim" | ⬛ DEAD | Agent verdict: "OVERSTATED". 1D-only guarantee. Listed in DEAD-3 but only as a one-liner. |
| M17 | **IoT breakthrough patent investigation** | User msg [26] item 2, [34] agent "Verify IoT breakthrough + patent" | ⬛ NOT BREAKTHROUGH | TS-LoRa prior art (2019) already does modulo-based autonomous scheduling. The "99.8% delivery" claim is prior art. IOT-1 status updated but patent angle is not tracked or killed. |
| M18 | **Terrain LOD patent investigation** | User msg [26] item 3, [35] agent "Verify terrain LOD breakthrough + patent" | ⬛ DEAD | Agent verdict: "OVERSTATED". Power-of-2 also nested, skirts solve cracks. MESH-4 and DEAD-4 cover this. |
| M19 | **Defense outreach submission guide** | User msg [54], agent "Research defense submission processes" | 📝, Phase ⏳ | A detailed submission guide was created. Not tracked in MASTER_TABLE. The SUB section exists but doesn't capture the guide document itself. |
| M20 | **3DGS real codebase integration (gsplat-mps on M5 Max)** | User msgs [78]-[158], extensive 3DGS experiment series 1-7 | 🧪 IN PROGRESS, Phase 🧪 | Major effort across the conversation. Series 1-7 run locally. Results: Farey shows 0.02-0.11 dB advantage at tight budgets, hyperparameter robustness, but not a breakthrough. NOT in MASTER_TABLE at all. |
| M21 | **3DGS paper for SIGGRAPH/workshop** | User msgs [128]-[137], FAREY_3DGS_PAPER_OUTLINE.md | ⏳ pending results, Phase 📝 | Depends on 3DGS experiments. 3DGS-8 exists but has not been updated to reflect real experiment results. |
| M22 | **RH equivalent via Farey discrepancy** | results/rh_equivalent_20260403_062918.md | 🔬 explored, Phase 🔬 | Agent explored whether DeltaW properties could give an RH equivalent. File exists in results. Not tracked. |

### 1C. PROOF APPROACHES FROM CONVERSATION (Session 10+)

| # | Direction | Where Mentioned | Suggested Status | Notes |
|---|-----------|-----------------|------------------|-------|
| M23 | **Kernel negativity via Abel-step kernels K_m(p)** | SESSION9_HANDOFF line 57 | ⬛ likely DEAD (T(N)<0 disproved) | Was live route in Session 9. T(N)<0 being FALSE at p=243,799 (Session 10) likely kills this. Not tracked as dead. |
| M24 | **Direct coprime positivity (bypass Mobius)** | SESSION9_HANDOFF line 58 | 🔬 status unclear | Was Wave 2 item in Session 9. Results in DIRECT_B_POSITIVITY.md. Not separately tracked in MASTER_TABLE. |
| M25 | **Dirichlet series for alpha: zeta(s+1)/(6*zeta(s))** | SESSION9_HANDOFF line 59 | 🔬 status unclear | Was live route. Not tracked. |
| M26 | **Signed Mobius cancellation lemma** | SESSION9_HANDOFF line 60 | 🔬 status unclear | Was live route. Not tracked. |
| M27 | **Sum multiple blocks (Sigma_m B_{p,m} > 0)** | SESSION9_HANDOFF line 61 | 🔬 status unclear | Was live route. Not tracked. |
| M28 | **Fourier k=1 dominance approach** | results/fourier_k1_dominance_20260404_153156.md | 🔬 active (Apr 4) | Recent result file (15:31 today). Not tracked. |
| M29 | **R ~ sqrt(p) conjecture** | results/r_sqrt_p_conjecture_20260404_153510.md | 🔬 active (Apr 4) | Recent result file. Not tracked. |
| M30 | **Gamma_2 contribution analysis** | results/gamma2_contribution_retry_20260404_154529.md | 🔬 active (Apr 4) | Recent result file. Not tracked. |
| M31 | **Phase constant analysis** | results/phase_constant_20260404_154835.md | 🔬 active (Apr 4) | Recent result file. Not tracked. |

---

## 2. Wrongly-Labeled Items

| ID | Current Status | Should Be | Evidence |
|----|---------------|-----------|----------|
| **MPR-4** (Unconditional Sign Theorem) | 🟢 (VERY STRONG) | **Needs major revision** -- the Sign Theorem as originally formulated is DISPROVED. B+C < 0 at p=243,799 (Session 10). The theorem now holds only as a Chebyshev bias statement (both signs infinitely often). | SESSION10_HANDOFF: "B+C < 0 at same prime (Sign Theorem fails)". The MASTER_TABLE still describes it with Session 8 progress as if the original Sign Theorem goal is intact. |
| **MPR-1** (B+C computation to p=100K) | 🟩 "2,722 primes verified (p<=50K), 0 violations" | **Update data: 4,617 primes verified to p=100K, and ALSO note B+C < 0 at p=243,799 for M(p)=-3**. The "0 violations" claim is outdated -- B+C > 0 for all qualifying primes to 100K was the Session 9 state, but Session 10 found the first counterexample at 243,799. | SESSION10_HANDOFF line 48; SESSION9_HANDOFF line 45; conversation agent "Extend B+C to 50K" and "Extend B+C to 100K" |
| **MPR-2** (B+C analytical proof) | 🟩 STRONG "Path C: delta^2 >= N^2/(12 log N) closes proof" | Should be **⬛ DEAD or major pivot** -- B+C > 0 for ALL primes is FALSE. The analytical proof target must be revised to B+C > 0 for p >= 11 with M(p) <= -3, or a density statement. | SESSION10_HANDOFF: B+C>0 is FALSE at p=243,799 |
| **MPR-3** (B+C ratio test approach) | 🟩 STRONG | Should be **⬛ DEAD or major pivot** -- same reason as MPR-2. B+C > 0 for all primes is the wrong target. | Same evidence |
| **MPR-13** (Rayleigh quotient approach) | 🟩 STRONG "Ranked #1 most promising proof approach" | Should be **🟨 or ⬛** -- this was for proving B+C > 0 universally. With B+C < 0 at 243,799, the target has changed. | Session 10 disproof |
| **MPR-14** (Schur convexity/majorization) | 🟨 MODERATE | Should be **⬛ DEAD** -- was alternative for proving B+C > 0 universally. | Session 10 disproof |
| **MPR-22** (two entries) | Both labeled MPR-22 | **DUPLICATE ID.** One is "B+C = -2*Sigma*R*delta Reformulation" (Section A line 44) and the other is "Geometric identity B+C = Sigma(D+delta)^2 - Sigma*D^2" (Section A line 62). One needs a new ID. |
| **MPR-23** (two entries) | Both labeled MPR-23 | **DUPLICATE ID.** One is "Extend spectral formula to L(1/2,chi)" (NEW DIRECTIONS line 19) and the other is "Wobble monotonicity equiv (BCZ horocycle)" (Section A line 63). One needs a new ID. |
| **MPR-24** (two entries) | Both labeled MPR-24 | **DUPLICATE ID.** One is "Prove composites heal (DeltaW > 0)" (NEW DIRECTIONS line 10) and the other is "newDispSquaredSum_pos_general (p>=13)" (Section A line 64). One needs a new ID. |
| **MPR-25** (two entries) | Both labeled MPR-25 | **DUPLICATE ID.** One is "Farey telescope / pair correlation" (NEW DIRECTIONS line 13) and the other is "Smooth-rough orthogonality lemma" (Section A line 65). One needs a new ID. |
| **MPR-26** (two entries) | Both labeled MPR-26 | **DUPLICATE ID.** One is "Higher moments L^4, L^6" (NEW DIRECTIONS line 20) and the other is "Guth-Maynard density-1 path" (Section A line 66). One needs a new ID. |
| **MPR-27** (two entries) | Both labeled MPR-27 | **DUPLICATE ID.** One is "Explicit formula: zeros <-> DeltaW(p)" (NEW DIRECTIONS line 12) and the other is "S^2 extension (higher-dim Sign Thm)" (Section A line 67). One needs a new ID. |
| **MPR-28** (two entries) | Both labeled MPR-28 | **DUPLICATE ID.** One is "Remove M(p) <= -3 restriction" (NEW DIRECTIONS line 18, status SETTLED) and the other is "Large sieve R->0 approach" (Section A line 68, status DEAD). One needs a new ID. |
| **MPR-29** (two entries) | Both labeled MPR-29 | **DUPLICATE ID.** One is "'Studying increments' in other problems" (NEW DIRECTIONS line 21) and the other is "Displacement-guided 3DGS" (Section A line 69, status DEAD). One needs a new ID. |
| **IOT-4** (two entries) | Both labeled IOT-4 | **DUPLICATE.** Appears in both Section E (DEF) line 123 and Section F (IOT) line 132 with slightly different descriptions. |
| **DEF-1 through DEF-4** | All ⬛ DEAD | **Partially incorrect** -- DEF-4 (Radio-silent report) says "DEAD" but the conversation shows the report was fact-checked, improved, and is being used for DARPA/ONR submissions. The scheduling-based defense direction is dead, but the report itself and the DARPA executive summary are active submission items (SUB-2). The status should distinguish between "silent scheduling is dead" vs "the report/executive summary submission is alive". |
| **PUB-5** (Radio-silent report) | "Done" targeting "DARPA / IEEE MILCOM" | Should note that DEF direction is dead but report is being repurposed for "zero-overhead coordination" framing. DARPA exec summary exists. |
| **3DGS-12** (Colab definitive test) | 🧪🟨 "Running definitive test on Colab" | Should be **⬛ or updated** -- the conversation pivoted to local M5 Max testing (gsplat-mps). No mention of Colab test completing. |
| **MPR-35** (Density theorem: DeltaW < 0 for almost all primes) | 🟨 MODERATE | Should be **🟩 STRONG** -- Session 10 established the full Rubinstein-Sarnak framework, unconditional both-signs result via Ingham, GRH+LI gives density exactly 1/2. This is now a core result, not moderate/parked. |
| **MPR-39** (Extend R computation to 10^7) | 🟨 | Session 10 says "Extend computation to 10^8" as immediate priority (line 103). Status should reflect whether any progress was made. |
| **MASTER_TABLE header** | "Last updated: 2026-03-30 (session 8 FINAL)" | **Stale**. The body has been updated (DEAD-15 through DEAD-23 dated 2026-04-04) but the header still says Session 8. Should say Session 10+. |

---

## 3. DARPA/DEF Direction Status

### What was pursued:
1. **Radio-silent coordination** (Farey-prime scheduling for zero-communication multi-agent timing). A full technical report was written (RADIO_SILENT_TECHNICAL_REPORT.md).
2. **DARPA TTO BAA HR001125S0011** -- An executive summary and cover letter were drafted (DARPA_EXECUTIVE_SUMMARY.md). The framing was corrected from "zero-communication" to "zero-overhead coordination" after the fact-check agent found that agents still need communication -- Farey only coordinates timing.
3. **ONR Code 311** -- Contact identified (Dr. Kamgar-Parsi). White paper path mapped.
4. **AFRL Tech Connect** -- Portal identified.
5. **A patent draft** was created (PATENT_DRAFT_SILENT_COORDINATION.md).
6. **Kill test (Session 7)**: Clock drift analysis showed Farey slots as close as 0.011ms at order 18 for 97 drones vs 1.03ms TDMA. Off-by-one in fleet size causes collisions, requiring communication, defeating the silent premise. This is structural and unfixable.

### What happened:
- **DEAD-15** killed all defense applications based on clock drift being fatal for the core scheduling premise.
- However, the **AUV/underwater direction** (IOT-4) was flagged as "POTENTIALLY SALVAGEABLE" because acoustic timescale is seconds, not milliseconds, making clock drift tolerance much more forgiving.
- The **DARPA executive summary** and **submission guide** were completed and are tracked in SUB-2, SUB-7, SUB-9, SUB-10.

### What MASTER_TABLE should say:
- **DEF-1, DEF-2, DEF-3**: Correct as ⬛ DEAD. The scheduling-for-drones premise is killed.
- **DEF-4**: Should be split. The radio-silent report as a DEFENSE SCHEDULING tool is dead. But the executive summary and the "zero-overhead coordination" framing are alive as submission items. Currently DEF-4 says "DEAD" which is misleading -- SUB-2 still targets DARPA TTO with the exec summary.
- **IOT-4 (AUV)**: Correctly marked as salvageable. Should note that this is the ONLY surviving defense-adjacent direction.
- **SUB-2 (DARPA TTO BAA)**: Still listed as active with "Register BAAT + submit by Apr 17". This should either be killed (if the scheduling premise is truly dead for all contexts) or updated to reflect the reframed "zero-overhead" angle. Currently inconsistent with DEF-1 being DEAD.

---

## 4. Structural Issues

### 4A. Duplicate IDs (CRITICAL)
The "NEW DIRECTIONS" section (added in Session 8) reuses MPR-22 through MPR-29, which already existed in Section A. This creates 8 pairs of duplicate IDs. The NEW DIRECTIONS items should be renumbered starting from MPR-40 or higher.

### 4B. Stale Header
Header says "Last updated: 2026-03-30 (session 8 FINAL)" but body has items from 2026-04-04.

### 4C. Session 10 Not Integrated
The Chebyshev bias discovery (Session 10) fundamentally changed the project. The Sign Theorem was disproved, B+C > 0 is false, and the framing shifted to spectral decomposition / Chebyshev bias. The MASTER_TABLE still reflects the Session 8 worldview where the Sign Theorem was the goal and B+C > 0 was expected to hold universally.

### 4D. 3DGS Real Experiments Not Tracked
An extensive multi-day experiment campaign (Series 1-7+) was run on the M5 Max with gsplat-mps. Results, learnings, and plans for Series 8-11 are not captured in any MASTER_TABLE item.

---

## 5. Recommendations

### Top 3 items to add IMMEDIATELY:

**1. Chebyshev Bias Framework (new top-level item)**
- **Suggested ID:** MPR-40
- **Description:** "Chebyshev Bias for Farey Discrepancy: spectral decomposition indexed by Dirichlet characters, oscillations at L-function zeros"
- **Status:** 🟩 STRONG
- **Phase:** 📊 (core results proved, paper integration needed)
- **Rationale:** This IS the project now. It subsumes the old Sign Theorem, the density theorem, the L-function generalization, and the Ingham unconditional result. Without this as a top-level item, the MASTER_TABLE does not reflect the current state of the project.

**2. Fix MPR-4 and MPR-1/2/3 status to reflect Sign Theorem disproof**
- MPR-4 should note that the unconditional sign theorem in its ORIGINAL form is disproved (B+C < 0 at p=243,799). The new theorem is: both signs occur infinitely often with positive logarithmic density (Ingham).
- MPR-1 should note B+C verified to 100K but counterexample found at 243,799.
- MPR-2 and MPR-3 should be pivoted or killed -- the proof target (B+C > 0 for all primes) is FALSE.
- **Rationale:** Currently the MASTER_TABLE implies B+C > 0 is an open theorem to prove. It is not -- it is false. This is the single most misleading aspect of the current table.

**3. Renumber duplicate IDs (MPR-22 through MPR-29)**
- The NEW DIRECTIONS section duplicates 8 IDs from Section A.
- Suggested: Renumber NEW DIRECTIONS items as MPR-40 through MPR-49 (after the Chebyshev item gets MPR-40, start from MPR-41).
- **Rationale:** Duplicate IDs make it impossible to reference items unambiguously. Any agent or person reading the table will be confused.

### Additional high-priority additions:
4. Add 3DGS real experiment tracking item (gsplat-mps Series 1-7+ results)
5. Add Stern-Brocot test / Gauss map eigenvalues (Session 10 priority)
6. Add L-function generalization as its own tracked item
7. Resolve SUB-2 vs DEF-1 inconsistency (is the DARPA submission alive or dead?)

---

## Appendix: Items Confirmed Present and Correct

The following items were checked and are correctly represented in the MASTER_TABLE:
- DEAD-1 through DEAD-14 (all verified as genuinely dead)
- DEAD-15 (silent coordination killed by clock drift -- correct)
- DEAD-16 through DEAD-23 (proof paths killed -- correct)
- 3BP-1 through 3BP-10 (three-body items -- correct)
- AMR-1 through AMR-7 (adaptive mesh -- correct)
- PHYS-1 through PHYS-17 (physics explorations -- correct)
- ML-1 through ML-5 (machine learning -- correct)
- PUB-1 through PUB-7 (publications -- correct, though PUB-1 target should note Chebyshev framing)
- SUB-1 through SUB-14 (submissions -- correct but SUB-2 is inconsistent with DEF-1)
