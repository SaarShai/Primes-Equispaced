# Paper Restructure Plan
# From 14 sections (2,522 lines) to 8 focused sections (~15 pages)

## Strategy: MERGE + TRIM + ADD, not rewrite from scratch

The current paper is comprehensive but sprawling. The restructure:
1. KEEP: all proved theorems, key identities, computational evidence
2. MERGE: consolidate overlapping sections
3. TRIM: remove redundant subsections, over-long proofs of minor results
4. ADD: 6 missing results + 8 new figures

## Section Mapping: Current → New

### NEW §1: Introduction (current §1, trimmed)
- Keep: abstract, opening, ΔW definition
- Update abstract: add spectroscope result and damage/response
- Add: forward reference to spectroscope Figure 1
- Trim: remove subsection on "observation that started it all" (fold into narrative)
- Lines: ~100 → ~80

### NEW §2: Definitions and Four-Term Decomposition (current §2 + §4.1-4.3)
- Keep: all definitions, four-term decomposition
- ADD: D(1/p) = 1 - |F_{p-1}|/p proposition (NEW, proved)
- ADD: Two δ definitions clarified (Def 1 = Farey gap, Def 2 = insertion deviation)
- ADD: D(1/p) dominance table (65% of |Σ D·δ|)
- Move: relevant parts of "Wobble-Mertens Phenomenon" §4 here
- Lines: ~170

### NEW §3: The Sign Pattern and Chebyshev Bias (current §10, enhanced)
- Keep: Computational Sign Observation, p=243,799 counterexample, R>0 conjecture
- ADD: Damage/Response decomposition (R₁ vs R₂) — NEW RESULT
- ADD: Response mechanism: sign alignment 56-59% + magnitude effect
- ADD: Phase-lock: sgn(ΔW) ~ -sgn(cos(γ₁·log(p)+φ))
- ADD: GRH-conditional density → 1/2
- ADD: Composites characterization: ω(n)≥2 always heals
- Figures: phase_lock_visualization, fig_delta_w_signs (updated)
- Lines: ~200

### NEW §4: A Different Computational Path to the Zeta Zeros (ENTIRELY NEW)
- ADD: Farey spectral function F(γ) definition
- ADD: Proposition (GRH): F(γ_k) ∝ |1/(ρ_k·ζ'(ρ_k))|² — tested at r=0.953
- ADD: γ₁ detection result (14.05, 0.6% error)
- ADD: Convergence comparison with Riemann-Siegel
- ADD: Multi-character extension (L-function zeros via twisting)
- ADD: Pair correlation detection (autocorrelation, γ₂-γ₁ found)
- Figures: farey_spectroscope, farey_vs_classical, convergence,
          zero_contributions, multi_character, amplitude_matching
- Lines: ~200

### NEW §5: Algebraic Identities and Proofs (current §3, trimmed)
- Keep best 6-7 identities: Bridge, Geometric B+C, Permutation Σfδ=C/2,
  Displacement-Cosine, Injection Principle, Universal δ-symmetric
- TRIM: remove 3-4 minor subsections (Compact Cross-Term, Smooth-Rough,
  Fractional Parts — these can go to appendix if needed)
- Keep: Mertens tomography (important for mechanism)
- Lines: ~300 (down from ~450)

### NEW §6: Computational Evidence (current §5+§6+§9+§11, merged)
- Merge: "Why Primes Are Special" + "Computational Methods" +
  "Lower Bounds" + "Compression"
- Keep: key computational results, lower bound theorems
- ADD: GK concentration (20%→94% figure)
- ADD: Composites ω(n)≥2 characterization
- Trim: remove speculative applications, over-detailed compression analysis
- Lines: ~250

### NEW §7: Formal Verification (current §6, unchanged)
- Keep as-is, update Lean sorry count (now 1, intentional)
- Update: add Aristotle entropy monotonicity + gap bound proofs
- Lines: ~100

### NEW §8: Open Questions and Future Directions (current §12+§7.7+§7.8)
- Merge: Open Questions + Speculative Future + Applications
- ADD: Gaussian Farey / Ford spheres
- ADD: Goldbach Δr per-step
- ADD: R₂ > 0 as open problem
- Trim: remove dead-end applications
- Lines: ~100

## Total: ~1,400 lines (down from 2,522) = ~15 pages

## Sections to DELETE entirely:
- Current §7 "Computational Methods" → fold into §6
- Current §8 "Applications and Connections" → best parts to §8, rest cut
- Current §11 "Compression Phenomenon" → 1 paragraph in §6

## Key additions for final draft:
1. Farey Spectroscope section (§4) — ~200 lines of NEW content
2. Damage/Response in §3 — ~50 lines NEW
3. D(1/p) proposition in §2 — ~20 lines NEW
4. Composites in §3/§6 — ~30 lines NEW
5. GK concentration in §6 — ~20 lines NEW
6. 8 new figures integrated throughout
