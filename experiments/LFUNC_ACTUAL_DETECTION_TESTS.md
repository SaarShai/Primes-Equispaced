# L-Function Spectroscope: ACTUAL Zero Detection Tests
# 2026-04-10 — Real computation, not estimates

## RESULTS

| L-function | Correct weights | Peak/Avg | Detected? |
|-----------|----------------|----------|-----------|
| ζ(s) | M(p)/p | **8.4x** | **YES ✓** |
| L(s,χ₄) | M_χ₄(p)/p where M_χ₄ = Σ μ(n)χ₄(n) | **2.8x** | **YES ✓** |
| L(s,E) y²=x³-x | a_p(E)/√p | 0.9x | **NO ✗** |
| L(s,χ₋₂₀) | M_χ₋₂₀(p)/p | 0.1x | **NO ✗** |

## WHAT WORKS
- ζ(s): strong detection (8.4x peak/average)
- Dirichlet L(s,χ₄): works with TWISTED Mertens M_χ(p) (2.8x)
- Key: must use M_χ(p) = Σ_{n≤p} μ(n)·χ(n), NOT χ(p)·M(p)

## WHAT DOESN'T WORK (yet)
- Elliptic curve: using a_p/√p gives flat spectroscope (0.9x). 
  Likely needs cumulative A_E(p) with γ² pre-whitening tuned to degree-2 L-function.
  The critical line is at Re(s)=1, not 1/2 — normalization may need adjustment.
- L(s,χ₋₂₀): zero locations may be wrong (approximate values used).
  Or needs more primes (N=50K may be insufficient for this conductor).

## FIRST ERROR: WRONG WEIGHTS
Initial test used χ(p)·M(p) — WRONG. Must use twisted Mertens M_χ(p).
After correction: Dirichlet detection works.

## IMPLICATIONS FOR THE PAPER
- Dirichlet batch speedup: CONFIRMED (detection works)
- Elliptic curve batch speedup: NOT YET CONFIRMED (detection fails)
- The batch speedup table should mark elliptic curve and higher as "speedup estimated, detection pending verification"
- Cannot claim batch advantage for functions where detection itself isn't verified
