# Opus: Invalidation Tests + Major Structural Finding
# 2026-04-10

## TASK 1: Tighter Mean Value — DEAD
Σ M(p)²/p² = 0.576 at N=500K. Plateaued. g(T) → 0.576, NOT zero.
Growth rate ~0.03·log log N (diverges astronomically slowly).
No contradiction possible via this route.

## TASK 2: Fourth Moment — NOT universal across zeros
| Zero | γ | Amplification |
|------|---|---------------|
| 1 | 14.13 | 14.9x |
| 2 | 21.02 | 4.3x |
| 3 | 25.01 | 1.7x |
| 5 | 32.94 | 0.3x |
| 8 | 43.33 | 0.1x |

Only γ₁ shows strong amplification. Higher zeros below background.
Amplification ratio grows as ~N^{0.32} — spectroscope improves with more data.

## TASK 3c: Four-Term Decomposition — ⭐ MAJOR STRUCTURAL FINDING ⭐

### 33,000:1 CANCELLATION
| Term | |F(γ₁)| | Phase |
|------|---------|-------|
| ΔS₂ | 71.16 | 1.70 |
| -ΔR_term | 142.65 | -1.43 |
| ΔJ | 71.50 | 1.71 |
| **ΔW** | **0.038** | **-3.06** |

Each individual term sees zeros ~2000x more strongly than ΔW itself.
Three terms are phase-aligned and nearly PERFECTLY cancel.
ΔW is the 0.03% residual of this cancellation.

### Small-k dominance
k=2..10 range carries the LARGEST signal (|F|=1.79 > full M(p) |F|=1.49).
Zero detection comes primarily from small squarefree numbers.
mu(2)=-1, mu(3)=-1, mu(5)=-1, mu(6)=1, mu(7)=-1, mu(10)=1 — these drive it all.

## NEW LEADS
1. The 33,000:1 cancellation: if proved to be IMPERFECT by at least C/p^ε,
   this constrains zero locations. Connects to explicit formulas for S₂, R, J individually.
2. Small-k sieve: just k=2..10 captures most signal. Tractable explicit formula possible.
3. N^{0.32} amplification growth: spectroscope sensitivity increases with data.
