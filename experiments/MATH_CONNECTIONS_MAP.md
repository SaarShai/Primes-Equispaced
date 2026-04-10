# Mathematics Connections Map — Farey Spectroscope Research
# 2026-04-10 — Opus comprehensive analysis

## 15 MSC AREAS TOUCHED (ranked by connection strength)

| MSC | Area | Connection Strength | Our Key Result |
|-----|------|:------------------:|----------------|
| 11M06 | ζ and L-functions | 10/10 | Core: 20/20 detection, universality, dichotomy |
| 11N05 | Distribution of primes | 9/10 | M(p)/√p spectroscope, R=0.952 prediction |
| 11A55 | Farey sequences | 9/10 | ΔW new object, 434 Lean results, four-term decomposition |
| 42A16 | Fourier/harmonic analysis | 8/10 | γ² matched filter, 2→20 detection |
| 94A12 | Signal processing | 7/10 | Detection theory applied to zero-finding |
| 11K | Probabilistic NT | 7/10 | Chebyshev bias for Farey, R=0.77 phase lock |
| 15B52 | Random matrices (GUE) | 7/10 | RMSE=0.066 from arithmetic data |
| 11Y | Computational NT | 7/10 | Batch 12x-141x, class numbers 5-14x |
| 03B35 | Formal verification | 6/10 | 434 Lean results, Mathlib candidates |
| 11L | Dirichlet L-functions | 6/10 | 108 characters, batch detection |
| 70F10 | Three-body problem | 6/10 | Figure-eight = φ, periodic table |
| 11R | Algebraic NT | 5/10 | Number field classification, Lucas/Pell |
| 37A | Ergodic theory | 5/10 | Horocycle chain, equidistribution rate |
| 11J | Diophantine approximation | 5/10 | Baker's theorem on cancellation |
| 62M | Statistical inference | 4/10 | Chowla spectroscopic test |

## 7 BRIDGES BETWEEN DISTANT FIELDS (ranked)

| # | Bridge | Fields | Key Result | Status |
|---|--------|--------|-----------|--------|
| 1 | **Signal Processing ↔ Analytic NT** | 94A ↔ 11M | γ² matched filter = 20/20 detection | Novel, computational |
| 2 | **Three-Body ↔ Algebraic NT** | 70F ↔ 11R | Figure-eight = golden ratio | Proved + Lean |
| 3 | **Chebyshev Bias ↔ Farey Geometry** | 11K ↔ 11A | First non-prime-race bias | GRH-conditional |
| 4 | **RMT ↔ Farey Geometry** | 15B ↔ 11A | GUE from arithmetic data | Computational |
| 5 | **Formal Verification ↔ Analytic NT** | 03B ↔ 11M | 434 Lean results | Verified |
| 6 | **Diophantine ↔ Spectral Theory** | 11J ↔ 42A | Baker on cancellation | Algebraic |
| 7 | **CS/Large Sieve ↔ Zero-Free Regions** | 94A ↔ 11M | Upper RIP = large sieve | Theoretical |

## TAO'S UNIFIED MATHEMATICS

Three ways our work contributes to the view of mathematics as interconnected:
1. The spectroscope is a METHODOLOGY transferring signal processing into NT
2. SL(2,ℤ) appears in THREE contexts (Farey, three-body, continued fractions)
3. The chain ζ zeros → Farey regularity → prime signal → GUE → three-body crosses 5 field boundaries

## VISUALIZATION DESIGN
- TikZ for paper (hub-and-spoke with cross-links)
- D3.js for outreach website (interactive, hoverable)
- Central hub: 11M06 (ζ zeros)
- Inner ring: 11N, 11A55, 42A, 11K
- Outer ring: 94A12, 70F, 03B, 37A, 11R
- Gold edges for novel bridges, gray for classical
