# Session 11 Handoff — 2026-04-10

## PAPER STATUS: "Prime Spectroscopy of Riemann Zeros"
Three theorems designed, proofs written (Opus 35KB), 5 gaps identified.
Paper scope locked: Dichotomy + Universality + Stability. No figure-eight/Chowla/Lean.

## WHAT'S PROVED (verified)
- Dichotomy: unconditional (needs gap fixes C,D,E)
- Universality: GRH-conditional (needs gap fix F)
- Stability: unconditional via large sieve (needs gap fix I — role swap)
- Phase φ_k for k=1..20 (mpmath, 0.003 rad match)
- 20-term model R=0.944
- Batch L-function: 20x faster at q=10000 (crossover q≥400)
- Error sum < 0.10 (100 zeros, convergent tail)
- ΔW novelty confirmed (Codex, NOT Franel-Landau)
- 434 Lean results (figure-eight 8 + prime power sum 3 + Farey cardinality 1)

## WHAT'S BROKEN (don't rebuild on these)
- Selberg input Σ M(n)²/n² = (6/π²)log x — FALSE
- Density-one unconditional — BROKEN (off-line pollution)
- Prime matrix for practical CS — NOT competitive (δ⁺ ~ 250)

## PROOF GAPS (from Codex adversarial, attacks C,D,E,F,I)
- C: No uniform gap β*-β_j for nearby zeros in Dichotomy
- D: T=N² gives too many zeros for error sum convergence
- E: c>0 in lower bound needs resonant dominance proof
- F: |ζ'(ρ)| lower bound — HARDEST, no unconditional bound
- I: Large sieve role swap in Theorem 3

## EASY WINS REMAINING
- Progression decomposition (p≡1 vs 3 mod 4) — on M1 Max
- Out-of-sample split test
- Sanity check vs Odlyzko tables — on M1 Max
- Benchmark batch with wall-clock timing
- Related work paragraph — on M1 Max

## FILES
- Proofs: experiments/OPUS_THREE_THEOREMS_FULL_PROOFS.jsonl
- Significance: experiments/OPUS_SIGNIFICANCE_AND_IMPACT.md
- Easy wins: experiments/EASY_WINS_RESULTS.md + OPUS_EASY_WINS_RANKED.md + CODEX_EASY_WINS_LIST.md
- Outreach: OUTREACH_TARGETS.md
- All Opus analyses: experiments/OPUS_*.md
- All Codex analyses: experiments/CODEX_*.md
- Phase data: experiments/PHASE_AMPLITUDES_K1_TO_10.md
- Corrections: experiments/SELBERG_INPUT_DISPROVED.md, DENSITY_ONE_UNCONDITIONAL_BROKEN.md

## INFRASTRUCTURE
- M1 Max: ALIVE, scheduled agent every 2h, 3 tasks running
- M5 Max: PAUSED
- System crontab: watchdogs every 15 min
- Kaggle project: ~/Documents/Benchmarks Kaggle/ (separate session)
