# OpenAI Prism Platform Handoff
## Complete Project Context + Task Assignment

## Project: Per-Step Farey Discrepancy and the Sign Theorem

### What This Is
A research project proving that prime numbers systematically disrupt the uniformity of rational number distributions (Farey sequences). The main result — the Sign Theorem — is proved via a hybrid analytical + computational approach.

### Current State (as of 2026-03-30)
- **Paper:** paper/main_new.tex (1557 lines, 11 theorems, ready for review)
- **Lean formalization:** 19 files, ~260 results, 2 sorry remaining
- **GitHub:** github.com/SaarShai/Primes-Equispaced

### What's Proved
1. Sign Theorem: ΔW(p) < 0 for all M(p) ≤ -3 primes (hybrid proof)
2. D/A = 1 + O(1/logp) (analytical, also D'-A'=-1 in Lean)
3. Σδ² = N²/(2π²) + o(N²) (analytical, Dedekind reciprocity)
4. Triangular distribution for displacements (analytical)
5. Composites: non-healers have density zero (unconditional via PNT)
6. Spectral positivity K̂ = (p/π²)|L(1,χ)|² (analytical)
7. 20+ supporting lemmas and identities

### What's NOT Proved (the one remaining gap)
B ≥ 0 for all M(p) ≤ -3 primes ANALYTICALLY. Verified computationally to p=20,000. The proof structure is identified (El Marraki correction bound) but explicit effective constants haven't been computed.

### Key Files in This Handoff
- paper/main_new.tex — the paper
- experiments/SESSION8_COMPLETE_SUMMARY.md — overview of all results
- experiments/B_EXACT_AUDIT.md — ground truth for B computation
- experiments/ELMARRAKI_CORRECTION.md — the proof attempt
- experiments/ADVERSARIAL_ELMARRAKI.md — what's missing
- experiments/CANONICAL_PROOF_STATUS.md — honest status of everything
- DIRECTION_TRACKER.md — all 43 research directions tracked

### Tasks for Prism

#### Task 1: Independent Verification of the Sign Theorem Proof
Read the paper and the proof chain. Verify each step independently:
- Four-term decomposition
- Σδ² = N²/(2π²) + o(N²) via Dedekind reciprocity
- D/A → 1 (two proofs: aliasing + Lean)
- B ≥ 0 (computational to 20K)
- Does the hybrid proof actually close?

#### Task 2: Close B ≥ 0 Analytically
The specific calculation needed: compute explicit upper bound on ||D_err||² and explicit lower bound on α using El Marraki |M(k)| ≤ 0.6257k/logk, then show the ratio r(p) < 1 for p ≥ 43. This is a mechanical (but careful) calculation.

#### Task 3: Explore New Directions
Pick any from the DIRECTION_TRACKER.md (43 items). Most promising:
- Density theorem (Rubinstein-Sarnak framework for Farey healing bias)
- Goldbach Δr decomposition (per-step strategy for Goldbach)
- Spectral extension to L(1/2,χ) via Nyman-Beurling kernel

### AI Contribution Statement
This research was conducted primarily by Claude Opus 4.6 (Anthropic), with formal verification by Aristotle (harmonic.fun), review by GPT-5.4 Extra High (OpenAI), and potentially Prism (OpenAI). Human researcher: Saar Shai.

### How to Access
All files are in the handoff zip. The GitHub repo has the complete history.
