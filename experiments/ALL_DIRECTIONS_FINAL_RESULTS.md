# All Directions: Final Test Results
# 2026-04-10

## DETECTS ZEROS (confirmed)
| Input | Peak/Avg | Notes |
|-------|----------|-------|
| M(p)/p (Mertens) | 8.4-17.3x | Main spectroscope, 20/20 zeros |
| Twisted Mertens M_χ | 2.8-3.8x | Dirichlet L-functions verified |
| Prime gaps g(p)/p | 3.8x | **NOVEL** — gaps encode zeros |
| Squarefree residual | 3.0x | Extends beyond Mertens |
| Smooth numbers (B=100) | 2.9x | Extends to smooth numbers |
| Fourth moment |F|⁴ | 96x | Massive amplification of signal |
| Finite field (ground truth) | 15x, 0.005 rad | Validated on known zeros |

## DOES NOT DETECT ZEROS
| Input | Peak/Avg | Notes |
|-------|----------|-------|
| Semiprimes (ω=2) | 0.89x | Two prime factors insufficient |
| Möbius correlation h=1 | 0.32x | Chowla correlations orthogonal |
| Möbius correlation h=2 | 0.91x | Same |
| Möbius correlation h=6 | 0.07x | Same |

## PREDICTIVE MODEL
| Test | R | Notes |
|------|---|-------|
| Train (p≤50K) | 0.938 | 20-term explicit formula |
| **Test (p>50K)** | **0.952** | **BETTER out-of-sample! Genuinely predictive.** |

## PRACTICAL APPLICATIONS
| Application | Result | Status |
|------------|--------|--------|
| Batch L-function | 12x-141x speedup | **CONFIRMED — killer app** |
| NTT prime selection | No correlation | DEAD END |
| Unconditional bounds | Burgess beats GRH for p<10²⁵ | DEAD END |
| Prime counting | Explicit formula oscillates | DEAD END |
| Costas sequences | All Welch perfect | DEAD END |
| QS smoothness | ~1-3% (designed, not run) | MARGINAL |

## EC SPECTROSCOPE: UNDER INVESTIGATION
Peaks at γ≈28-31 (7.8x) instead of expected γ₁≈2.39.
Mean a_p ≈ 0.04 (nearly zero, mean subtraction doesn't help).
Opus investigating possible explanations.
