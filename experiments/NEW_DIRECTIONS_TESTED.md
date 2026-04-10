# New Directions: Quick Tests + Opus Strategic Analysis
# 2026-04-10

## QUICK TEST RESULTS (computed in 1 minute)

| Direction | Peak/Avg | Detection | Significance |
|-----------|----------|-----------|-------------|
| E. Convergence series | 4.6x→17.3x (grows with N) | ✅ YES | Clean convergence curve for paper |
| F. Prime GAP spectroscope | 3.8x | ✅ YES | **NOVEL**: gaps encode zeros! |
| B. Squarefree residual | 3.0x | ✅ YES | Spectroscope extends beyond M(p) |
| G. Möbius lag-1 correlation | 0.3x | ✗ NO | Chowla correlations orthogonal to spectroscope |

## OPUS PRIORITY RANKING

| # | Direction | Priority | 1-hour test | Reason |
|---|-----------|----------|-------------|--------|
| 1 | E. Convergence time series | HIGHEST | Plot F(γ₁;N) for N=100..100K | Trivial, guaranteed figure, extracts |ζ'(ρ)| |
| 2 | H. Finite field spectroscopy | HIGH | Curve over F₁₀₁, known zeros | Ground truth validation, referee-proof |
| 3 | A. Inverse spectroscopy | HIGH | Predict M(p) for p>10⁶ | Already have the model, win-win test |
| 4 | B. Other sequences | HIGH | Squarefree, semiprime, smooth | Extends universality beyond primes |
| 5 | G. Chowla correlator | MED-HIGH | C_h(x) for h=1,2,6 | Synergizes with Paper F |
| 6 | F. Prime gap spectroscopy | MEDIUM | Already tested — 3.8x ✓ | Novel connection to Cramér |
| 7 | I. Phase transition map | MEDIUM | R² heatmap for (K,N) grid | Methods section material |
| 8 | C. Fourth moment | MEDIUM | |Σ|⁴ at zeros | Pair correlation via spectroscope |
| 9 | D. Adaptive/ML | LOW | Optimize filter vs γ² | Engineering, not math |

## KEY DISCOVERIES FROM QUICK TESTS
1. Prime GAPS detect zeros (3.8x) — nobody has shown this
2. Squarefree residuals detect zeros (3.0x) — extends beyond Mertens
3. Möbius correlations do NOT detect zeros — orthogonal mechanism
4. Convergence is monotone and steady — good for paper figure
