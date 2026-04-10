# Codex: Unconditional Energy Concentration Analysis
# 2026-04-09 — Deep thinking on proof paths after Selberg collapse

## VERDICT: Full universal statement NOT provable with current tools.
The core obstruction is PHASE CONTROL, not energy magnitude.
Σ 1/p = ∞ gives mass but does not force prime phases to align with a specific γ_k.

## Approach Assessment

| Approach | Feasibility | Obstacle |
|----------|------------|----------|
| A. Explicit formula interference | HARD_BUT_POSSIBLE (smoothed) | Need uniform interchange + nonresonant tail cancellation |
| B. Sarnak/Möbius disjointness | BLOCKED | No disjointness theorem for multiplicative twists on primes |
| C. Entropy | IMPOSSIBLE | No theorem connecting entropy to pointwise frequency localization |
| D. Turán power sum | HARD_BUT_POSSIBLE (existence) | Forces large values SOMEWHERE, not at prescribed γ_k |
| E. Off-diagonal / Goldston-Gonek | HARD_BUT_POSSIBLE (L² version) | Missing: arithmetic correlation theory of M(p) over primes |
| F. Compressed sensing / adelic | BLOCKED | Needs RIP/incoherence for {log p}, no such theorem |

## Most Promising Strategy: SMOOTHED RESONANCE THEOREM
1. Smooth windows in log p and γ
2. Insert Landau/Gonek explicit formula
3. Split zeros into local window + distant tail
4. Zero-free region + density estimates bound the tail
5. Montgomery-Vaughan / Goldston-Gonek for prime sum control
6. Deduce lower bound from local zero window when S has enough mass

THE GAP: Need Re Σ_{p∈S∩[X,2X]} M(p)/p · e^{-iγ_k log p} >> Σ p^{-1/2}
along infinitely many X. Nothing like this is known.

## New Approaches Proposed by Codex

G. INVERSE THEOREM: Prove that if a divergent prime subset gives large resonance
   at a zero, it must have strong block structure. Structural theorem about subsets.

H. HYBRID LARGE SIEVE + BLOCK OPTIMIZATION: Discretize γ near zeros,
   block primes dyadically, optimize quadratic form. Realistic for smoothed theorem.

I. PRETENTIOUS MODEL: Model M(p) by pretentious Euler product surrogate.
   Heuristic for finding the right smoothing/localization.

## What Would the Experts Try?
- Tao: First test if statement is FALSE as stated. Then energy-increment argument.
- Maynard: Blockwise amplifier using sieve ideas to force primes into right windows.
- Soundararajan: Smoothed logarithmic-scale resonance + large-values framework.

## Strongest Provable Unconditional Theorem
Smoothed spectral decomposition: zeros appear as frequencies in the spectroscope,
Montgomery-Vaughan / Goldston-Gonek give exact diagonal + controlled off-diagonal.
The zeros SHOW UP in the Fourier picture. What's MISSING: pointwise lower bound at γ_k.

## Three Ingredients That Would Close the Gap (any one suffices)
1. Quantitative resonant block lower bound over every divergent prime subset
2. Phase coherence theorem from Σ 1/p = ∞ alone
3. Strong pointwise control of 1/ζ'(ρ) on positive-density zeros + off-resonance cancellation

## Sources
Ingham 1942, Goldston & Gonek 1998, Davenport 1937, Tao 2010, Inoue 2021,
Ford 2024, Mossinghoff-Trudgian-Yang 2024
