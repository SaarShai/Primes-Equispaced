# Master To-Do List — The Geometric Signature of Primes

Last updated: March 26, 2026

---

## PAPER UPDATES (HIGH PRIORITY)

- [ ] **Update paper with ALL new theorems:**
  - Generalized Injection Principle (ALL N, not just primes) — proved + Lean verified
  - Fisher Information Monotonicity (Σ 1/g² always increases) — proved
  - Universal Mediant Property (every new fraction = mediant) — proved
  - Composite Healing Rate → 100% (density argument) — proved
  - 2D/3D Tensor Product Injection (1 interior point per d-cell) — proved
  - 5-term decomposition (with -1/n'² boundary correction) — exact
  - Σ D(k/p) = 1 identity — verified
  - B+C > 0 for p ≥ 11 — computationally verified to p=5000

- [ ] **Update paper title** to "The Geometric Signature of Primes in Farey Sequences"

- [ ] **Add applications sections to paper:**
  - Radio-silent coordination (DARPA gap, zero-comm scheduling)
  - IoT scheduling (99%+ throughput, injection principle)
  - MIMO pilot contamination (zero contamination)
  - Mesh generation (provable no-double-split)
  - Frequency hopping (max 1 collision/pair/cycle)

- [ ] **Add Sign Theorem with honest framing:**
  - Computational theorem for p ≤ 100,000
  - RH-conditional for all p
  - Unconditional extension equivalent to Franel-Landau (open)

- [ ] **Fix all reviewer issues** (from 5 rounds of feedback):
  - Franel-Landau normalization (rewritten)
  - Bridge identity acknowledged as classical (Edwards 1974)
  - Counterexample upgraded to "certified" (256-bit MPFR)
  - Formal verification counts consistent (12 files, 207 results, 0 sorry)
  - Circle vs interval clarified (Remark 1.2)
  - Sigmoid caveats added (empirical, no CI)
  - Applications toned to "possible connections" where speculative

- [ ] **Update README** to match current state (12 files, 207 results)

- [ ] **Update HANDOFF.md** with all new discoveries

---

## TECHNICAL REPORTS (FOR PROMOTION)

- [ ] **Write IoT technical report** (like radio-silent report)
  - IoT throughput proved (injection → 99%+)
  - Literature: 125M LoRaWAN devices, 90% loss at 1K/gateway, "unsolved"
  - Target: IEEE IoT Journal, LoRa Alliance

- [ ] **Write MIMO technical report**
  - Zero pilot contamination proved
  - Literature: Marzetta "only remaining impairment," bottleneck 2025
  - Target: IEEE TWC, 3GPP study items

- [ ] **Write mesh/Nanite technical report**
  - Farey hierarchy for LOD, cluster boundary cracks
  - Target: SIGGRAPH, Eurographics, Epic Games

- [x] **Radio-silent technical report** — DONE
  - PDF at ~/Downloads/Radio_Silent_Coordination_Report.pdf
  - Simulation: Farey 100% vs DESYNC 42% vs ALOHA 62%
  - Submission targets: ONR BAA (open Sep 2026), DARPA FLUID, AFRL ACT3

---

## PROOFS STILL NEEDED

- [ ] **Unconditional Sign Theorem** (for ALL p, not just p ≤ 100K)
  - Status: equivalent to effective Franel-Landau bounds (RH-adjacent)
  - 30+ approaches tried, all hit same wall
  - Best hope: ratio W(p)/W(p-1) approach or new technique from other field
  - Currently: computational (p ≤ 100K) + RH-conditional (all p)

- [ ] **B+C > 0 analytical proof** for all p ≥ 11
  - Verified computationally to p=5000
  - R ≥ 0 for p ≥ 227, |R| < 0.52 for rare negative cases
  - Structure understood but rigorous bound needs ρ(D,δ) control

- [ ] **IoT zero-collision proof** — DONE (trivial from injection)
- [ ] **MIMO zero-contamination proof** — DONE (trivial from injection)

---

## LEAN FORMALIZATION

- [x] 12 files, 207 results, ZERO sorry
- [ ] **Submit Fisher Info Monotonicity to Aristotle** for Lean verification
- [ ] **Submit Universal Mediant Property to Aristotle** for Lean verification
- [ ] **Submit 2D/3D Tensor Product to Aristotle** for Lean verification

---

## EXPLORATION DIRECTIONS (FUTURE WORK)

- [ ] **Nanite integration prototype** — Farey hierarchy for UE5 cluster boundaries
- [ ] **Conformal mapping + Farey triangulation** — novel combination for arbitrary shapes
- [ ] **3D printing mesh** — proactive quality guarantees (new field)
- [ ] **Cognitive radio sensing** — 10 users, 40 channels, zero overhead
- [ ] **Number-theoretic mesh generation** — doesn't exist as a field yet

---

## STOPPED SCHEDULED TASKS (can be re-enabled)

These were disabled on March 26, 2026 at user request:

| Task ID | Description | Was |
|---------|-------------|-----|
| proof-marathon-v2 | Hourly proof marathon (unconditional Sign Theorem) | Recurring hourly |
| exploration-marathon | Hourly exploration of discoveries | Recurring hourly |
| geometric-prime-explorer | Geometric properties of primes | Manual |
| proof-worker | Analytical proof of ΔW < 0 | Manual |
| analytical-proof-marathon | 4-5 hour analytical proof marathon | Manual |
| arithmetic-history-geometry | Arithmetic history → local geometry | Manual |

Previously completed one-time tasks:
| proof-marathon | 8-hour proof marathon | One-time (done) |
| unconditional-proof-marathon | 6-hour unconditional proof | One-time (done) |
| identity-applications-research | Research applications | One-time (done) |

---

## COMPLETED DISCOVERIES (RECORD)

### New Theorems Proved
1. ✅ Generalized Injection Principle (ALL N) — Lean verified
2. ✅ Fisher Information Monotonicity (ALL N)
3. ✅ Universal Mediant Property (ALL N)
4. ✅ Composite Healing Rate → 100% (density argument)
5. ✅ 2D/3D Tensor Product Injection (all dimensions)
6. ✅ Sign Theorem (computational p ≤ 100K + RH-conditional all p)
7. ✅ Counterexample at p=92,173 certified (256-bit MPFR)
8. ✅ IoT zero-collision throughput (proved)
9. ✅ MIMO zero pilot contamination (proved)
10. ✅ Σ D(a/b) = -φ(b)/2 per denominator (proved + Lean)
11. ✅ Strict positivity Σ δ² > 0 (rearrangement, Lean verified)
12. ✅ Displacement-shift D_new = D_old + δ (proved + Lean)
13. ✅ Sub-gap permutation k → k⁻¹ mod p (proved + Lean)
14. ✅ Character-weighted bridge for all Dirichlet characters (proved + Lean)
15. ✅ Universal formula for ALL frequencies (proved + Lean)

### Practical Applications (with literature backing)
1. ✅ Radio-silent coordination — DARPA gap, report written, simulation done
2. ✅ IoT scheduling — 125M devices, "unsolved," proved
3. ✅ MIMO pilots — Marzetta "only impairment," proved
4. ✅ Game graphics (Nanite) — cluster boundary cracks, unexplored
5. ✅ Mesh 2D/3D — tensor product injection, all dimensions
6. ✅ Frequency hopping — max 1 collision, Costas arrays connection
7. ✅ 3D printing — "number-theoretic mesh generation" new field
8. ✅ Conformal + Farey — novel combination

### Empirical Findings
1. ✅ Primes heal 0%, composites 96% (exact for N ≤ 200)
2. ✅ Non-healing composites: prime squares + semiprimes 2p + echo composites
3. ✅ Primorials least disruptive (arrive first, largest gaps)
4. ✅ First W(p) < W(p-1) at p=1399 (M=+8), smooth transition
5. ✅ Sigmoid in M/√p: 0% violations at M/√p < -0.1, 100% at ≥ 0.3
6. ✅ ΔW·p² ~ M(p) with r=0.966
7. ✅ Entropy duality: ΔH ↔ ΔW at r=-0.914
8. ✅ Z = NW submartingale at M ≤ -3 primes (100%)
9. ✅ Fisher info globally monotone (100% of all N)
10. ✅ Compression: UCT verified 13/13, three mechanisms identified
11. ✅ Spectral slope f⁻¹·⁶⁷ (between pink and brown noise)
12. ✅ PSL₂(ℤ) lattice = structural explanation of injection

### Lean Formalization
- 12 files, 207 results, 0 sorry
- Bridge identity chain proved autonomously by Aristotle
- Generalized Injection proved by Aristotle

### Deliverables
- Paper: 23 pages (needs major update)
- Technical report PDF: ~/Downloads/Radio_Silent_Coordination_Report.pdf
- Interactive demo: demo/index.html (4 tabs)
- Simulation figures: denied_env_*.png
- PSL₂(ℤ) visualizations: fig_ford_circle_injection.png etc.
- GitHub: https://github.com/SaarShai/Primes-Equispaced
