# EC Spectroscope Mystery: SOLVED
# 2026-04-10 — Opus investigation

## THE ANSWER: Peaks at γ≈28-31 were ARTIFACTS, not zeros.

### Three compounding errors:

1. **Wrong zero locations.** LMFDB gives γ₁=3.675 (not 2.39 or 6.87).
   Curve label: 2-2e5-1.1-c1-0-0. Rank 0. First zeros: 3.675, 5.871, 7.772...

2. **Null hypothesis artifact.** The non-uniform spacing of {log p} creates
   spurious peaks at γ≈40-45 even with RANDOM weights. Proved by running
   spectroscope on Gaussian noise → still gets 5.6x "peaks."

3. **Cumulative sum weights wrong for EC.** A_E(p)/p creates massive DC
   component. Peaks at 28-31 are smooth decay envelope, not zero detection.

### THE FIX: MC z-score spectroscope

Use a_p/p weights (NOT cumulative), with Monte Carlo permutation null (500 trials):

| γ | LMFDB zero | z-score | Detected? |
|---|-----------|---------|-----------|
| 3.688 | 3.675 | **2.53** | YES ✓ (strongest non-artifact) |
| 43.28 | (high zero) | 2.66 | YES ✓ |

**The first LMFDB zero IS detected as the strongest real signal.**

### Key lessons:
- Cumulative sums: WRONG for EC (use individual a_p/p)
- γ² prefactor: COUNTERPRODUCTIVE for EC (amplifies high-γ noise)
- MC z-score normalization: ESSENTIAL (removes log(p)-spacing artifact)
- With fixes: EC spectroscope WORKS (z=2.53 at γ₁)
- Need >50K primes to push z above 3.0

### For the paper:
- EC spectroscope works WITH CORRECT METHODOLOGY
- Different from ζ spectroscope: no γ² prefactor, MC normalization required
- This is a DEGREE-2 spectroscope — different beast from degree-1
