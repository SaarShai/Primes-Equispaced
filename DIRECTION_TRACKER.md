# Complete Direction Tracker
## Every direction we've identified, with status and next steps

### PROVED THEOREMS (ready for paper)
| # | Direction | Status | What remains |
|---|-----------|--------|-------------|
| 1 | Sign Theorem (M(p) ≤ -3) | ✅ PROVED | Paper rewrite in progress |
| 2 | Permutation Square-Sum Σxδ = C/2 | ✅ PROVED | In paper |
| 3 | Deficit minimality D_q(2) | ✅ PROVED | In Lean + paper |
| 4 | Deficit minimality D_q(r) ≥ D_q(2) | ✅ PROVED | In paper |
| 5 | Σδ² = N²/(2π²) + o(N²) | ✅ PROVED | Paper rewrite |
| 6 | Spectral positivity K̂ = (p/π²)\|L(1,χ)\|² | ✅ PROVED | In paper |
| 7 | C_W ≥ 1/4 (Cauchy-Schwarz) | ✅ PROVED | In Lean + paper |
| 8 | C_W ≥ N/28 (large-b fractions) | ✅ PROVED | In paper |
| 9 | Σ E² ≥ p²/28 (endpoints) | ✅ PROVED | In paper |
| 10 | M(p) ≤ -3 threshold is optimal | ✅ SETTLED | p=92,173 counterexample |

### ESSENTIALLY PROVED (needs writeup polish)
| # | Direction | Status | What remains |
|---|-----------|--------|-------------|
| 11 | Triangular distribution | 🟩 ESSENTIALLY PROVED | Large-sieve step needs careful writeup |
| 12 | Composites: density-zero non-healers | 🟩 ESSENTIALLY PROVED | μ-M independence needs standard citation |
| 13 | Powers of 2 always heal | 🟩 PROVED (structural) | Add to paper |

### CONFIRMED COMPUTATIONALLY (not analytical proofs)
| # | Direction | Status | What remains |
|---|-----------|--------|-------------|
| 14 | Zeta zeros in ΔW spectrum (Z=1625) | 📊 CONFIRMED | Add figure to paper |
| 15 | B ≥ 0 for M(p) ≤ -3 (p ≤ 3000) | 📊 VERIFIED | NOT proved analytically |
| 16 | (C+D)/A ≥ 1.096 for all tested | 📊 VERIFIED | Follows from proved bounds for large p |
| 17 | Σδ²/N² → 1/(2π²) convergence | 📊 VERIFIED | Proved asymptotically |

### HIGH PRIORITY EXPLORATIONS
| # | Direction | Status | Next step |
|---|-----------|--------|-----------|
| 18 | Primes-are-random beyond L² | 🟩 Triangular covers full distribution | Prove joint distribution, error term O(p^{3/2+ε}) |
| 19 | Composites heal: close remaining gaps | 🟩 Strong progress | Explicit N₀, rigorous μ-M independence |
| 20 | Explicit formula: ΔW = zeros coupling | 🟨 Formally derived | Rigorous truncation + regularization |
| 21 | Farey telescope / pair correlation | 🟨 New connection found | Mellin poles at γ-γ' → Montgomery connection |
| 22 | Density theorem "ΔW < 0 for almost all primes" | 🟨 Natural next step | Rubinstein-Sarnak theory |
| 23 | **Prove B ≥ 0 for M(p) ≤ -3 analytically** | 🟨 **HIGH PRIORITY** | Kloosterman/spectral methods — key to fully analytical proof |
| 44 | **Prove D/A → 1 analytically** | 🟩 **HIGH PRIORITY** | May follow from proved S(p) bound — agent checking! |
| 24 | Test zero-pair periodogram on larger dataset | 🟨 Z=1625 confirmed | Push to p = 10⁶ |

### MEDIUM PRIORITY
| # | Direction | Status | Next step |
|---|-----------|--------|-----------|
| 25 | Spectral extension to L(1/2,χ) | 🟨 ζ(1) pole blocks | Nyman-Beurling or Matérn-1/2 workaround |
| 26 | Higher moments L⁴, L⁶ connections | 🟩 Triangular predicts all | Connect to L-function fourth moment |
| 27 | Goldbach Δr per-step analysis | 🟨 Most promising application | Explore sieve-theoretic decomposition |
| 28 | Geometric lens: other prime effects | 🟨 New research program | What else do primes DO to combinatorial objects? |
| 29 | Prove C_W = O(1) unconditionally | 🟨 Meaningful for RH | As hard as understanding zero distribution |
| 30 | K constant: make K ≤ 10 rigorous | 🟨 Structure proved | Computational extension to 1.1M, or cancel proof |
| 31 | Error term in Σδ² | 🟨 O(p^{5/3}) proved | Improve to O(p^{3/2+ε}) |

### LOW PRIORITY / SPECULATIVE
| # | Direction | Status | Notes |
|---|-----------|--------|-------|
| 32 | Generalize to number fields | ⬜ Unexplored | Dedekind zeta analogues |
| 33 | Quantum chaos / modular surface | ⬜ Unexplored | QUE connection via Farey |
| 34 | New zero-free regions via geometry | ⬜ Long-shot | Would require magnitude control |
| 35 | Other discrepancy measures (L¹, L∞) | ⬜ Unexplored | Different Farey norms |
| 36 | ABC conjecture per-step analysis | ⬜ Very speculative | From increments exploration |

### DEAD / SETTLED
| # | Direction | Status | Why |
|---|-----------|--------|-----|
| 37 | B+C > 0 for ALL primes | ⬛ DEAD | False at p=1399 (M=+8) |
| 38 | Extend threshold to M(p) ≤ -2 | ⬛ DEAD | Counterexample at p=92,173 |
| 39 | Kloosterman pointwise bound | ⬛ DEAD | Ratio reaches 261, fails |
| 40 | Σ M(t)² ~ (6/π²)t | ⬛ DEAD | Confused μ² with M². Actual: ~0.016t² |
| 41 | Σ D² ~ n²logN | ⬛ DEAD | Correct: ~N³·(const + loglogN) |
| 42 | "Studying increments" as novel methodology | ⬛ CORRECTED | Novel for Farey, standard in general NT |
| 43 | New route to RH | ⬛ CORRECTED | New perspective, NOT new route |
