# Shared Context for Local Models
Updated: 2026-04-09

## Project: Farey Research
Independent researcher (Saar Shai) studying per-step Farey discrepancy and its connection to Riemann zeta zeros.

## Paper Constellation (12 papers)
See ~/Desktop/Farey-Local/PAPER_CONSTELLATION.md for full list.
Key papers: A (ΔW foundation), B (Chebyshev phase), C (spectroscope method), D (universality).

## Key Objects
- ΔW(N) = W(F_{N-1}) - W(F_N): per-step Farey discrepancy (NOVEL object)
- F_comp(γ) = γ²·|Σ M(p)/p · e^{-iγ log p}|²: compensated Mertens spectroscope
- R(p) = ΣD·δ/Σδ²: Farey insertion-deviation correlation ratio

## Key Results (verified)
- Spectroscope detects 20/20 zeta zeros (local z-score, up to 65σ)
- γ² matched filter: NOVEL application (pre-whitening is classical, this application is new)
- Universality: any 2750 primes encode all 20 zeros (NOVEL, no prior literature)
- Phase φ = -arg(ρ₁·ζ'(ρ₁)) = -1.6933 rad — CONFIRMED to 0.003 rad
- GUE pair correlation: RMSE=0.066 from arithmetic data (190 pairs)
- Chowla detection threshold: ε = 1.824/√N
- Siegel zero: 465M sigma sensitivity for q≤13
- 422 Lean 4 verified results (+ 1 from Aristotle = 423)

## VERIFIED NUMERICAL CONSTANTS (use these, do NOT fabricate)
- ρ₁ = 0.5 + 14.134725141734693i
- ζ'(ρ₁) = 0.783296511867031 + 0.124699829748171i  ← COMPUTED WITH MPMATH
- |ζ'(ρ₁)| = 0.793160433356506
- arg(ζ'(ρ₁)) = 0.15787 rad
- φ₁ = -arg(ρ₁·ζ'(ρ₁)) = -1.6933 rad
- φ₂ = -1.3264, φ₃ = -1.8851, φ₄ = -1.0169, φ₅ = -2.1297 rad
- A₁ = 0.0891, A₂/A₁ = 0.469, A₃/A₁ = 0.327, A₄/A₁ = 0.283, A₅/A₁ = 0.246

## EXPLICIT FORMULA (RESOLVED — correct form)
The explicit formula for M(x) uses:
  M(x) ~ Σ_ρ x^ρ / (ρ · ζ'(ρ))
The coefficient is 1/(ρ·ζ'(ρ)), NOT 1/((ρ-1)·ζ'(ρ)).
The (ρ-1) form is WRONG for ΔW. This was verified numerically: the ρ form gives
arg = -1.6933 matching empirical -1.69 to 0.003 rad; the (ρ-1) form gives -1.764, off by 0.074 rad.

## CRITICAL WARNING — DATA INTEGRITY PROTOCOL
DO NOT fabricate numerical values of ζ'(ρ), arg(ζ'(ρ)), or any special function evaluation.
If a task requires numerical computation, say "NEEDS MPMATH VERIFICATION" and proceed with symbolic/theoretical analysis only.
The values above are GROUND TRUTH computed at 30-digit precision.

## REFERENCE DATA PROTOCOL (added after 3 wrong-data incidents)
Before comparing computed values to "known" reference values:
1. STATE THE EXACT SOURCE (paper title + page, LMFDB URL, or mpmath computation)
2. VERIFY THE OBJECT MATCHES — e.g., confirm WHICH curve, WHICH character, WHICH normalization
3. COMPUTE A SANITY CHECK — e.g., if a_5(E) should be -2, compute #E(F_5) directly and check
4. If source is "from memory" or "approximately" → TREAT AS UNVERIFIED, do NOT build on it
5. If two sources disagree → STOP and resolve before proceeding

PAST ERRORS FROM IGNORING THIS:
- Selberg: confused μ(n)² with M(n)² → 5 hours wasted on false premise
- ζ'(ρ₁): qwen fabricated -0.174+0.251i (real: 0.783+0.125i) → wrong coefficient conclusion
- Elliptic curve: compared a_p to values from WRONG CURVE → false "mismatch" diagnosis

## CRITICAL: Novelty
Fourier duality primes↔zeros is CLASSICAL (cite Csoka 2015, Planat et al, Van der Pol 1947).
Our novel contributions: γ² filter, local z, Farey R(p) connection, universality, pair correlation, ΔW(N) object, four-term decomposition, 423 Lean results.

## Key Open Problems
1. Unconditional universality proof — the diagonal sum Σ M(p)²/p² CONVERGES unconditionally (VERIFIED), so the variance approach is dead. Need alternative: Montgomery kernel, Sarnak/Möbius disjointness, or off-diagonal structure.
2. R₂ > 0 for wobble decomposition (gap-energy version proved, wobble version open)
3. GUE regularization (Wiener-Khinchin gap for distributions)
4. Paper J must be CONDITIONAL on RH (under RH: Σ M(n)²/n² ~ 0.03·log x, diverges slowly)

## KILLED DIRECTION (DO NOT REVISIT)
- "Selberg gives Σ M(n)²/n² = (6/π²)log x" — FALSE. Confuses μ(n)² with M(n)².
  Σ μ(n)²/n = (6/π²)log x ✓ (squarefree counting)
  Σ M(n)²/n² ≈ 2.26 at N=500K, nearly constant ✗

## File Locations
- Experiments: ~/Desktop/Farey-Local/experiments/
- Wiki: ~/Documents/Spark Obsidian Beast/Farey Research/wiki/
- Master table: ~/Desktop/Farey-Local/MASTER_TABLE_INDEX.md

## Output Convention
- Write results to ~/Desktop/Farey-Local/experiments/YOUR_TASK_NAME.md
- Include: date, method, key findings, limitations, next steps
- Be honest about what is proved vs computational vs speculative
- If you need a numerical value you don't have: SAY SO. Do not make one up.
