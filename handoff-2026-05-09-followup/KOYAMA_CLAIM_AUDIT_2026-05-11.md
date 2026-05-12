# Koyama claim/citation audit

Date: 2026-05-11
Agent: E
Scope: independent audit of the 2026-05-11 Koyama moonshot packets plus `HANDOFF.md` and `L2_facts/farey-claim-ledger.md`.
Write policy: audited files not edited.

## Verdict

No P0 theorem-promotion failure found. The current packet set consistently keeps GL(1) Perron-leading at `DEFER`, EC-NDC at `NUMERICAL/no promotion`, Path B at `external controls required`, and DPAC as no zeta-zero bridge.

Main remaining risks: theorem-grade wording around the DPAC finite phase layer, non-embedded external citations, finite-product naming, inconsistent status labels, and stale handoff counts.

## Findings

### P1 - DPAC theorem language outruns verification status

Refs:
- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md:35`
- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md:147`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:19`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:21`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:39`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:132`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:205`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:212`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:219`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:251`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:406`

Issue: the synthesis says the DPAC layer is a "real safe theorem layer" and "proves almost-everywhere gamma avoidance". The DPAC packet itself says "Claim-safe documentation only", no Lean build was run, and the theorem candidates remain `sorry`. The analytic claim is plausible and elementary, but this packet is not a formal theorem artifact.

Safe replacement wording:

> DPAC: for fixed `K,beta`, the finite exponential-polynomial argument gives a claim-safe analytic proof sketch: assuming the non-identity lemma for the Mobius polynomial, the bad real-gamma set is measure zero. This packet is not Lean-verified and does not imply pointwise avoidance at zeta-zero ordinates.

### P1 - External literature references are not citation-closed

Refs:
- `handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md:124`
- `handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md:169`
- `handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md:185`
- `handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md:208`
- `handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md:268`
- `handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md:284`
- `HANDOFF.md:54`
- `HANDOFF.md:82`
- `HANDOFF.md:121`

Issue: the Perron packet names Inoue/Soundararajan-style formulas and bounds without exact bibliographic entries, page/equation numbers, or embedded quotes. `HANDOFF.md` also names Aoki-Koyama 2023, eq. (1.4), p.235, while the handoff protocol requires PDF retrieval, verbatim quote, and embedded quote before using cited theorem claims. This is safe for internal planning only if treated as inherited/unverified here.

Safe replacement wording:

> For internal planning: an Inoue/Soundararajan-style explicit-formula or partial-sum route appears to transfer the off-target residue problem rather than close it. This reference is not citation-closed in the moonshot packet. Before paper/correspondence use, attach exact bibliographic data, page/equation numbers, and short verified quotes. For AK, write "conditional AK constant, per the previously verified AK note" unless the quote is embedded in the deliverable.

### P1 - `L2E^rank` wording can be misread as a completed/global L-value normalization

Refs:
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md:47`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md:49`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md:53`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md:57`
- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md:92`
- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md:107`
- `HANDOFF.md:57`
- `L2_facts/farey-claim-ledger.md:58`

Issue: the CSV schema uses `L2E_partial`, but the prose/tables abbreviate to `L2E^rank`. That can sound like the completed or infinite `L(E,2)` value, while the computation is a finite sharp-cutoff good-prime Euler-product proxy.

Safe replacement wording:

> `D_zeta2_over_L2E_rank` is a finite sharp-cutoff good-prime Euler-product proxy using `L2E_partial^rank` through the reported prime bound (`p_max=999983` at `K=1000000`), not a completed/global `L(E,2)` normalization.

### P2 - Path B "falsification" is too strong

Refs:
- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md:8`
- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md:16`
- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md:20`
- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md:27`
- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md:29`
- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md:84`
- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md:189`
- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md:114`

Issue: line 16 calls the local NumPy output "falsification/diagnostic", but the same packet says B1/B2 are not decision-complete locally because conductor-matched controls are absent. Current evidence fails local conductor-controlled acceptance gates; it does not falsify every possible rank-survival formulation.

Safe replacement wording:

> Local NumPy-only failure-to-promote diagnostic from stored rows. Current Path B remains conductor-confounded or undecided until external B1/B2 controls are computed; no rank-survival sentence is supported.

### P2 - Machine-readable status labels are inconsistent

Refs:
- `handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md:7`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md:7`
- `koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md:8`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:1`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:19`
- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md:39`

Issue: Perron has frontmatter `status: DEFER`; EC and Path B only have body status lines; DPAC has frontmatter but no `status`; synthesis has a table but no overall status key. This makes stale promotion easier for future agents/tools.

Safe replacement wording:

> Mirror explicit status labels in future edits: synthesis `status: NO_THEOREM_PROMOTED`; EC `status: NUMERICAL_NO_PROMOTION`; Path B `status: EXTERNAL_BLOCKED_LOCAL_FAIL`; DPAC `status: PROOF_SKETCH_NOT_LEAN_VERIFIED_DEFER_ZETA_BRIDGE`.

### P2 - Handoff misattribution count is stale/inconsistent

Refs:
- `HANDOFF.md:60`
- `HANDOFF.md:89`

Issue: one line says 16 misattributions caught, with 12+4; another says 15, with 12+3. This undermines the citation-audit story even though it does not affect the Koyama math.

Safe replacement wording:

> At least 15 citation/misattribution failures were caught; exact count needs reconciliation before external use.

### P2 - DPAC finite-sample certificate claim needs inline provenance

Refs:
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:164`
- `formal-conjectures/DPAC_PHASE_BRIDGE_MOONSHOT_2026-05-11.md:390`
- `formal-conjectures/DPAC_aristotle_result_extract/aristotle_dispatch_DPAC_aristotle/DPAC_context.md:106`
- `formal-conjectures/DPAC_dispatch_receipt.md:121`

Issue: the DPAC packet reports 100-digit interval arithmetic and `300/300` certified nonvanishing cases. It lists the context files under "Additional context checked", but not in frontmatter `sources`, and the certificate statement is not line-cited where it appears.

Safe replacement wording:

> Existing project context reports 100-digit interval arithmetic with `300/300` nonvanishing cases for `K in {10,20,50}` at the first 100 zeta zeros; this audit did not independently rerun the certificates. Treat as finite empirical certificate evidence, not an all-zero theorem.

### P3 - "Breakthroughs" is rhetorical overclaim

Refs:
- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md:22`
- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md:24`

Issue: "No theorem was promoted" is correct. Calling the four outputs "breakthroughs" is rhetorically stronger than the content: two are negative diagnostics, one is a sharpened obstruction, and one is a proof-sketch layer without zeta-zero bridge.

Safe replacement wording:

> The moonshot produced four useful updates.

### P3 - "Formally closed" in `HANDOFF.md` should stay scoped to prior audits

Refs:
- `HANDOFF.md:41`
- `HANDOFF.md:93`

Issue: "all formally closed" is broad. It may be correct as project state, but the Koyama audit did not recheck those Theorem B routes. Avoid letting this phrase inherit fresh authority from the Koyama moonshot.

Safe replacement wording:

> Current handoff records these five near-term Theorem B-exact routes as closed under prior audits; the 2026-05-11 Koyama moonshot did not reopen or reverify them.

## Safe global packet

Use this as the claim-safe summary:

> No Koyama theorem was promoted on 2026-05-11. GL(1) Perron-leading remains `DEFER`: the local double-pole residue is local algebra, but the shifted nonlocal off-target zero aggregate, including possible higher-order residues, is not citation-closed. EC-NDC remains numerical negative evidence through `K=1000000` for the four tested finite sharp-cutoff normalizations; `L2E_partial^rank` is only a finite good-prime proxy. Path B remains conductor-confounded or externally blocked pending B1/B2 controls. DPAC has a claim-safe fixed-`K,beta` almost-everywhere phase-avoidance proof sketch, not a Lean-verified theorem and not a zeta-zero ordinate bridge.
