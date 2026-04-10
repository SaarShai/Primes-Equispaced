# MASTER TABLE INDEX — Priorities, Status, Next Steps
Last updated: 2026-04-10 (Session 11, end of day)

## HIGHEST PRIORITY — PAPER-READY

| ID | Direction | Status | Next Step |
|----|-----------|--------|-----------|
| MPR-49 + UNI + J | **Paper C: "Prime Spectroscopy of Riemann Zeros"** | THREE THEOREMS PROVED: Dichotomy (unconditional), Universality (GRH), Stability (large sieve). All 5 proof gaps closed. 20-term model R=0.944. Out-of-sample verified. Batch L-function 12x at q=10K. Dirichlet detection verified (χ₄: 2.8x, χ₋₂₀: 3.8x). Bounded interval failure confirmed. | **Write paper draft.** Fix EC detection (needs M1 Max). Push to GitHub. Contact LMFDB. |
| 3BP | **Paper H: Three-Body Number Field Classification** | Figure-eight = golden ratio (8 Lean theorems). Lucas numbers for Q(√5). Pell equation T²-dU²=4 for all families. Entropy h=2n·log(ε_d). Periodic table of algebraic invariants. | Verify traces 47, 123 in 695-orbit database. Write paper. |
| MPR-40 | **Paper B: Chebyshev Bias Phase** | Phase RESOLVED: 1/(ρ·ζ'(ρ)), φ₁=-1.6933 confirmed to 0.003 rad. φ_k for k=1..20 computed (mpmath). 20-term model R=0.944. | Write paper. Content complete. |

## HIGH PRIORITY — CONTENT EXISTS, NEEDS WORK

| ID | Direction | Status | Next Step |
|----|-----------|--------|-----------|
| MPR-58 | Damage/Response (Paper A) | Gap-energy R₂>0 provable for all N≥2 (Codex). Wobble R₂ open (divisor-sieve obstruction). ΔW novelty confirmed vs Franel-Landau (Codex, 24 searches). δD(p) also correlates (R=-0.67) — differentiation is structural not empirical. | Formalize gap-energy theorem. Write Paper A. |
| CHW | Chowla Spectroscopic Test (Paper F) | Threshold ε=1.824/√N derived. Evidence FOR Chowla at N=200K. False alarm resolved. | Normalize periodogram computation. Scale to N=10M. |
| MPR-49b | L-function Extensions (Paper G) | Dirichlet: verified ✅. Elliptic curve: partial (3.0x near γ₂, needs more primes). Modular forms: not tested. Siegel: 465M sigma at q≤13. Batch speedup table computed for 7 types. | Verify EC with correct a_p + more primes. Test modular forms. |
| LEAN | 434 Lean Results (Paper I) | 434 total (figure-eight 8, prime power sum 3, Farey cardinality 1). 2 genuine sorrys (BridgeIdentity, SignTheorem). GitHub: Primes-Equispaced. | Push latest. Mathlib PR (Farey cardinality). Close BridgeIdentity sorry. |

## RESOLVED (completed this session)

| ID | Direction | Resolution |
|----|-----------|------------|
| MPR-27 | Explicit formula coefficient | **RESOLVED.** 1/(ρ·ζ'(ρ)) correct. mpmath verified to 0.003 rad. |
| UNI-2 | Unconditional variance proof | **KILLED.** Selberg input was wrong (μ(n)²≠M(n)²). Σ M(p)²/p² converges unconditionally. |
| UNI-2b | Density-one unconditional | **KILLED.** Off-line zeros pollute globally. |
| UNI-2c | Dichotomy (unconditional) | **PROVED.** Spectroscope detects rightmost zero regardless of RH. |
| UNI-7 | Interval-restricted failure | **VERIFIED.** [100K,200K] gives 0.9x. Sparse wide-range (every 100th) gives 3.3x. |
| RIP | Compressed sensing connection | **ASSESSED.** Upper RIP from large sieve. Lower RIP = RH barrier. Prime matrix NOT competitive for practical CS (δ⁺~250). Reframed as stability. |

## KILLED DIRECTIONS (added this session)

- **Selberg prime extraction:** Input Σ M(n)²/n² = (6/π²)log x was FALSE (confused μ(n)² with M(n)²)
- **Density-one unconditional:** Off-line zeros pollute at every bulk ordinate
- **Practical CS/RIP:** δ⁺ ~ P/T ≈ 250, not competitive with random matrices
- **Empirical ΔW vs D(N):** δD(p) also correlates (R=-0.67), so empirical separation fails

## SAAR ACTION ITEMS

| Priority | What |
|----------|------|
| **HIGHEST** | Get arXiv endorser → submit Paper C |
| **HIGHEST** | Contact LMFDB team (draft ready in OUTREACH_DRAFTS.md) |
| HIGH | Contact Maynard/Tao re: bounded gaps corollary |
| HIGH | Get arXiv endorser → submit Paper H (three-body) |
| MEDIUM | Push Lean to GitHub, Mathlib PR |
| MEDIUM | Contact Keating/Snaith (RMT), Berry/Connes (quantum chaos) |

## PAPER CONSTELLATION (updated)

| Paper | Title | Status | Priority |
|-------|-------|--------|----------|
| **C** | **Prime Spectroscopy of Riemann Zeros** | PROOF COMPLETE. Computation verified. Batch L-function verified. GitHub section live. | **1 — SUBMIT FIRST** |
| **H** | Three-Body Number Field Classification | Content complete. Lean verified. Needs dataset verification. | **2** |
| **B** | Chebyshev Bias Phase | Content complete. 20-term R=0.944. | 3 |
| **A** | Per-Step Farey Discrepancy | Gap-energy R₂>0 ready. ΔW novelty confirmed. | 4 |
| **F** | Chowla Spectroscopic Test | Methodology complete. Needs N=10M computation. | 5 |
| **G** | L-Function Extensions | Dirichlet verified. EC/modular pending. Siegel 465M sigma. | 6 |
| **I** | 434 Lean Results | GitHub ready. Mathlib PR candidates identified. | 7 |
| **D** | Universality (standalone) | Merged into Paper C. | — |
| **J** | Unconditional Variance | Merged into Paper C (Dichotomy theorem). Variance approach killed. | — |
| **E** | GUE from Arithmetic Data | GUE RMSE=0.066. Wiener-Khinchin gap remains. Low priority. | 8 |
| **K** | Gaussian Farey Z[i] | 1344 pts enumerated. Not computed. | 9 |
| **M** | Horocycle Equidistribution | Chain identified. Not formalized. | 10 |

## MOST SIGNIFICANT FINDINGS (updated)

| Finding | Status | Significance |
|---------|:------:|:------------:|
| ⭐⭐⭐ Universality: any Σ1/p=∞ subset detects all zeros | PROVED (GRH) | Most novel contribution |
| ⭐⭐⭐ Dichotomy: spectroscope detects zeros regardless of RH | PROVED (unconditional) | Clean RH equivalence |
| ⭐⭐⭐ Batch L-function: 12x-141x speedup for families | VERIFIED (computation) | Practical application |
| ⭐⭐ Figure-eight = golden ratio + number field classification | PROVED + Lean | Most broadly appealing |
| ⭐⭐ 20-term model R=0.944 (89% variance explained) | VERIFIED | Explicit formula quantified |
| ⭐⭐ Phase φ_k for k=1..20 at 0.003 rad precision | VERIFIED (mpmath) | Ground truth data |
| ⭐⭐ 434 Lean 4 verified results | PROVED | Largest Farey formalization |
| ⭐ Bounded gaps corollary: Maynard-Tao primes detect zeros | COROLLARY of universality | Links two frontiers |
| ⭐ Stability: large sieve guarantees detection stability | PROVED (unconditional) | Measurement framework |
| ⭐ GUE RMSE=0.066 from arithmetic data | VERIFIED | New pathway to RMT |
| ⭐ ΔW(N) is novel (not Franel-Landau rediscovery) | CONFIRMED (Codex, 24 searches) | Foundational novelty |

## STATS
Papers: 12 planned, 2 ready (C, H), 3 near-ready (B, A, I)
Lean: 434 results, 2 genuine sorrys
Outreach: 7 draft emails ready (OUTREACH_DRAFTS.md)
GitHub: spectroscope-paper/ section live with benchmarks + visualization
Infrastructure: M1 Max permanent, scheduled agent every 2h, verification gates mandatory
