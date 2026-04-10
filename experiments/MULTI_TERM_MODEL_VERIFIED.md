# Multi-Term Explicit Formula Model — Computationally Verified
# 2026-04-09 — Direct computation with mpmath + Möbius sieve

## Setup
- M(p)/√p correlated against Σ_{k=1}^{K} 2·A_k·cos(γ_k·log p + φ_k)
- Phases and amplitudes from mpmath at 30-digit precision
- 9,591 primes up to 100,000
- Möbius sieve computed from scratch

## Results

| K (terms) | R | R² | Sign agreement |
|-----------|------|------|---------------|
| 1 | 0.687 | 0.472 | 73.6% |
| 2 | 0.789 | 0.623 | 75.7% |
| 3 | 0.834 | 0.696 | 81.7% |
| 5 | 0.876 | 0.767 | 80.5% |

## Key findings
1. Each additional zero MEASURABLY improves the fit
2. γ₂ alone adds 15% variance explained (0.47 → 0.62)
3. 5 zeros explain 77% of variance — substantial
4. Sign agreement peaks at 3 terms (81.7%) then dips slightly (80.5%)
   — the 4th and 5th terms add amplitude precision but don't flip many signs
5. The 1-term R=0.687 (not 0.77 as previously claimed — need to check normalization)

## Correction
The previously reported R=0.77 may have used:
(a) a different observable (R(p) instead of M(p)/√p)
(b) a different normalization
(c) a restricted prime range
Need to reconcile.

## For Paper B
This table is PUBLISHABLE. Direct computational verification that the explicit formula
predicts M(p) oscillations with increasing accuracy as more zeros are included.
The phases φ_k are EXACT (mpmath), not fitted — this is a PREDICTION, not a fit.
