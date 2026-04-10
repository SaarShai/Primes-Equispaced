# MASTER TABLE AUDIT
## Exhaustive scan of all project sources vs MASTER_TABLE.md
**Date:** 2026-03-28

---

## METHODOLOGY

Scanned all of the following sources against the 57-item master table:
1. Master table (~/Desktop/Farey-Local/MASTER_TABLE.md) -- 57 items
2. All 86 experiment .md files in ~/Desktop/Farey-Local/experiments/
3. TODO_LIST.md (GDrive)
4. DISCOVERY_DATABASE.md (GDrive)
5. .claude/ memory files
6. GDrive-only experiment files (FAREY_PHYSICS_CONNECTIONS.md, etc.)
7. paper/main.tex (theorems, applications sections)
8. Lean formalization files (12 .lean files)
9. GRAPHICS_APPLICATION_REPORT.md, TERRAIN_LOD_ENGINEERING_ASSESSMENT.md (GDrive root)

---

## FINDINGS: ITEMS MISSING FROM MASTER TABLE

### Category 1: PROVED THEOREMS not in table

| # | Item | Source | Category | Strength | Should Add? |
|---|------|--------|----------|----------|-------------|
| 1 | **Voronoi Entropy Monotonicity**: H(F_{N+1}) > H(F_N) for all N >= 2 (proved, elementary, appears novel) | voronoi_entropy_findings.md | MPR | STRONG | **YES** -- new theorem with elementary proof, possibly publishable standalone |
| 2 | **I_k family universally monotone**: sum (bd)^k strictly increasing for all k > 0 (proved via AM-GM) | monotone_functionals_findings.md, psl2z_identities_findings.md | MPR | STRONG | **YES** -- complete characterization of monotone Farey functionals |
| 3 | **Log-Sum monotonicity**: L(N) = sum log(bd) strictly increasing (proved, delta = 2 log(b+d)) | monotone_functionals_findings.md | MPR | STRONG | **YES** -- simple but new |
| 4 | **J_k sign theorem**: J_k = sum g^k increasing for 0<k<1, constant at k=1, decreasing for k>1 (proved via convexity) | monotone_functionals_findings.md | MPR | STRONG | **YES** -- complete picture of gap-power functionals |
| 5 | **Farey antisymmetry identity**: sum f(a/b) = 0 for any antisymmetric f over F_N (proved) | psl2z_identities_findings.md | MPR | MODERATE | **YES** -- clean structural identity |
| 6 | **Grand identity for weighted Farey sums**: sum f(b) * exp(2pi i a/b) = f(1) + sum f(b)*mu(b) for ANY arithmetic f | compression_findings.md | MPR | STRONG | **YES** -- generalizes bridge identity to arbitrary weights |
| 7 | **Liouville-weighted Farey sum = Q(N) + 1**: sum lambda(b)*exp(...) = squarefree count + 1 | compression_findings.md | MPR | MODERATE | **YES** -- novel identity connecting Liouville function to Farey geometry |

### Category 2: EMPIRICAL FINDINGS not in table

| # | Item | Source | Category | Strength | Should Add? |
|---|------|--------|----------|----------|-------------|
| 8 | **Twin prime geometric entanglement**: twin primes show identical sign(DeltaW) 100% of time, r=0.808 | information_paradox_findings.md | MPR | MODERATE | **YES** -- potentially novel connection |
| 9 | **Mertens-Healing Theorem for 2p semiprimes**: M(2p) > 0 implies 2p is non-healing (100% to N=1500) | MERTENS_HEALING_THEOREM.md, NONHEALING_FINAL_FINDINGS.md | MPR | STRONG | **YES** -- clean empirical law, not in table |
| 10 | **Prime squares non-heal iff p >= 11**: exact threshold for p^2 non-healing | NONHEALING_FINAL_FINDINGS.md | MPR | STRONG | **YES** -- clean result |
| 11 | **Wobble-entropy duality**: DeltaW ~ -DeltaH with r=-0.914 | entropy_findings.md | MPR | STRONG | **YES** -- deep structural connection |
| 12 | **Farey gaps 97.4% of max entropy**: near-maximal entropy at all scales | entropy_findings.md | MPR | MODERATE | Maybe -- supporting observation |
| 13 | **M(p) explains only 18% as discrete MI but 93.4% as variance**: information-theoretic characterization | entropy_findings.md | MPR | MODERATE | Maybe -- clarifies information paradox |
| 14 | **Primorials are local minima of W**: W(30), W(210) verified as local minima | primorials_optimal_refinement.md | MPR | MODERATE | **YES** -- connects to QMC/optimal refinement |
| 15 | **phi(N)/N < 0.87 threshold**: cleanly separates W-increasing from W-decreasing steps | primorials_optimal_refinement.md | MPR | MODERATE | **YES** -- useful empirical law |
| 16 | **C/A is INCREASING with p** (~ p^0.016), not decreasing as analytical bound suggests | MARATHON_FINDINGS_2026_03_26.md | MPR | STRONG | **YES** -- critical for proof strategy |
| 17 | **Full decomposition D/A + C/A >= 1.09** for all tested primes (min at p=2857) | MARATHON_FINDINGS_2026_03_26.md | MPR | STRONG | **YES** -- key computational fact for proof |
| 18 | **Three compression mechanisms identified**: Mobius, Weil (algebraic-geometric), Equidistribution | compression_findings.md | MPR | MODERATE | **YES** -- novel classification |
| 19 | **Beatty sequences show strong compression** (ratio ~ N^{-0.94} for golden ratio) | compression_findings.md | MPR | MODERATE | Maybe -- tangential finding |

### Category 3: APPLICATION DOMAINS explored but not in table

| # | Item | Source | Category | Strength | Should Add? |
|---|------|--------|----------|----------|-------------|
| 20 | **AUV (underwater autonomous vehicles)**: MODERATE FIT for acoustic channel TDMA | DEEP_DIVE_APPLICATIONS_REPORT.md | DEF | MODERATE | **YES** -- new defense application angle |
| 21 | **Financial applications**: exhaustively assessed, NOT PRACTICAL (4 scenarios killed) | financial_applications.md | NEW (FIN) | DEAD | **YES** -- important to record as dead end |
| 22 | **Drone swarm TDMA**: MARGINAL, niche in radio-silent scenarios only | drone_satellite_research.md | DEF | WEAK | Maybe -- overlaps with radio-silent (DEF-4) |
| 23 | **Satellite constellation scheduling**: NOT PRACTICAL (routing is bottleneck, not timing) | drone_satellite_research.md | IOT | DEAD | **YES** -- record as dead end |
| 24 | **AI upscaling (DLSS/FSR)**: NO CONNECTION | GRAPHICS_APPLICATION_REPORT.md | NEW | DEAD | Maybe -- record dead end |
| 25 | **QMC parameter selection**: 1373x batch speedup (Application A4 in DISCOVERY_DATABASE) | new_applications.md, DISCOVERY_DATABASE | ML | MODERATE | **YES** -- in discovery DB but not master table |
| 26 | **Compressed sensing**: divisor-weighted L1 gives 2.6x (marginal, Application A5) | DISCOVERY_DATABASE | ML | WEAK | Maybe -- marginal result |
| 27 | **Geometric hashing**: order-preserving for rationals (niche, Application A6) | DISCOVERY_DATABASE | ML | WEAK | No -- too niche |
| 28 | **Signal processing**: O(1) Farey DFT via bridge identity | compression_applications_findings.md | ML | MODERATE | Maybe -- neat but narrow |

### Category 4: PROOF APPROACHES / RESEARCH TOOLS not in table

| # | Item | Source | Category | Strength | Should Add? |
|---|------|--------|----------|----------|-------------|
| 29 | **Rayleigh quotient approach** to W(p)/W(p-1) ratio bound (ranked #1 most promising) | cross_field_research.md | MPR | MODERATE | **YES** -- active proof approach |
| 30 | **Schur convexity / majorization approach** (ranked #2, conceptually cleanest) | cross_field_research.md | MPR | MODERATE | **YES** -- active proof approach |
| 31 | **Ergodic theory / Gauss map approach** to unconditional theorem | ergodic_approach.md | MPR | WEAK | Maybe -- not yet productive |
| 32 | **Explicit formula approach**: M(p) ~ sum p^rho/rho gives |1-D/A| = O(p^{-0.4}) | MARATHON_FINDINGS_2026_03_26.md | MPR | MODERATE | **YES** -- viable proof path |

### Category 5: PHYSICS CONNECTIONS not fully captured

| # | Item | Source | Category | Strength | Should Add? |
|---|------|--------|----------|----------|-------------|
| 33 | **Arnold tongues / Devil's staircase**: Farey ordering of mode-locked regions (well-established) | FAREY_PHYSICS_CONNECTIONS.md | PHYS | STRONG | **YES** -- stronger than current PHYS entries |
| 34 | **Atomic physics: doubly-excited Rydberg, pendular-planet states (2025)** | FAREY_QUANTUM_CONNECTIONS.md | PHYS | MODERATE | Already PHYS-7, but more detail available |
| 35 | **Josephson junctions / charge-density waves**: Farey structure in condensed matter | FAREY_PHYSICS_CONNECTIONS.md | PHYS | MODERATE | Maybe -- expands PHYS context |

### Category 6: ITEMS IN TODO_LIST.md not captured in master table

| # | Item | Source | Category | Strength | Should Add? |
|---|------|--------|----------|----------|-------------|
| 36 | **Update paper with 8 new theorems** (Generalized Injection, Fisher, Mediant, Healing, Tensor, etc.) | TODO_LIST.md | PUB | STRONG | Already in MPR-5/PUB-1 implicitly, but paper update task not explicit |
| 37 | **Write MIMO technical report** (zero pilot contamination proved) | TODO_LIST.md | IOT | STRONG | **YES** -- separate deliverable, not just IOT-1 |
| 38 | **Write mesh/Nanite technical report** | TODO_LIST.md | MESH | MODERATE | Already MESH-1 area, but deliverable not tracked |

### Category 7: DISCOVERY_DATABASE items not in master table

| # | Item | Source | Category | Strength | Should Add? |
|---|------|--------|----------|----------|-------------|
| 39 | **Theorem #20: Zero-Sum identity sum D(k/p) = 1** (verified, needs proof) | DISCOVERY_DATABASE | MPR | MODERATE | **YES** -- tracked as Open Problem O5 but not in master table |
| 40 | **Empirical E7: |DeltaW| ~ p^{-1.77} scaling law** | DISCOVERY_DATABASE | MPR | MODERATE | **YES** -- quantitative finding not captured |
| 41 | **Empirical E8: 97.3% sign persistence between consecutive primes** | DISCOVERY_DATABASE | MPR | MODERATE | Maybe -- supporting statistic |
| 42 | **Structural S5: 19,000:1 compression phenomenon** | DISCOVERY_DATABASE, information_paradox_findings.md | MPR | STRONG | **YES** -- major structural insight |
| 43 | **Structural S6: Euler chi=2 preserved (DeltaV=+1, DeltaE=+2, DeltaF=+1)** | DISCOVERY_DATABASE | MPR | MODERATE | **YES** -- topological result |
| 44 | **Open Problem O5: Prove sum D(k/p) = 1** | DISCOVERY_DATABASE | MPR | MODERATE | **YES** -- open problem not tracked |

### Category 8: LEAN FORMALIZATION gaps

| # | Item | Source | Category | Strength | Should Add? |
|---|------|--------|----------|----------|-------------|
| 45 | **Lean files exist for 12 theorems but only 3 Aristotle submissions tracked** (Fisher, Mediant, Tensor) | TODO_LIST.md, Lean files | MPR | STRONG | MPR-5 covers this but doesn't list all 12 files |

---

## SUMMARY

### MUST ADD (high-value items clearly missing):

1. **MPR-9**: Voronoi Entropy Monotonicity theorem (proved, possibly novel)
2. **MPR-10**: I_k/J_k/L monotone functional family (proved, 3 theorems)
3. **MPR-11**: Grand identity for weighted Farey sums (generalizes bridge identity)
4. **MPR-12**: Twin prime geometric entanglement (r=0.808, novel connection)
5. **MPR-13**: Mertens-Healing Theorem for composites (clean empirical law)
6. **MPR-14**: Primorials as optimal refinement / local W-minima
7. **MPR-15**: C/A increasing trend + full decomposition data (critical for proof)
8. **MPR-16**: Zero-Sum identity sum D(k/p) = 1 (open problem)
9. **MPR-17**: |DeltaW| ~ p^{-1.77} scaling law
10. **MPR-18**: Three compression mechanisms (Mobius, Weil, Equidistribution)
11. **MPR-19**: 19,000:1 compression / information paradox resolution
12. **MPR-20**: Euler chi=2 topological invariance
13. **ML-5**: QMC parameter selection (1373x speedup, from DISCOVERY_DATABASE A4)
14. **DEF-5**: AUV underwater scheduling (moderate fit)
15. **FIN-1**: Financial applications (DEAD -- 4 scenarios killed)
16. **SAT-1**: Satellite constellation scheduling (DEAD)
17. **PHYS-10**: Arnold tongues / Devil's staircase (strong established connection)

### SHOULD ADD (moderate value):

18. Farey antisymmetry identity (sum f = 0 for antisymmetric f)
19. Liouville-weighted Farey sum = Q(N)+1
20. Wobble-entropy duality (DeltaW ~ -DeltaH)
21. phi(N)/N < 0.87 threshold for W direction
22. Rayleigh quotient + Schur convexity proof approaches
23. MIMO technical report as separate deliverable
24. Explicit formula proof path for B+C+D >= A

### ALREADY CAPTURED (no action needed):

- All 3BP items (1-10) are well-covered
- All 3DGS items (1-9) are well-covered
- All AMR items (1-7) are well-covered
- All DEF items (1-4) are well-covered
- Mesh items (1-5) are covered including dead ends
- Most physics items (1-9) are covered
- ML items (1-4) are covered
- All publication items (1-7) are covered

### DEAD ENDS properly killed but not recorded:

- Financial trading applications (all 4 scenarios)
- Satellite constellation scheduling
- AI upscaling (DLSS/FSR/XeSS) -- no connection
- Drone TDMA (marginal, niche only)
- Erdos-Turan bound (already MPR-8 DEAD)
- Terrain LOD / Nanite (already MESH-4/5 DEAD)

---

## STATISTICS UPDATE (if all MUST-ADD items are added)

- **Total items:** 57 + 17 = 74
- **New STRONG items:** 7
- **New MODERATE items:** 6
- **New DEAD items:** 3
- **New open problems explicitly tracked:** 2
- **Papers in pipeline:** 7 (unchanged, but MIMO report could be PUB-8)
