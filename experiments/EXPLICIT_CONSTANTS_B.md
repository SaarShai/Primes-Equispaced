# Explicit Constants for B ≥ 0: Status Report
## Date: 2026-03-30

## What IS Verified (exact Fraction arithmetic)

For the CORRECTED formula B' = (|M(N)|-1)·C' - 2·correction:

### M(p) = -3 primes (48 tested to p ≈ 5000):
| Range | correction/C' | B' > 0? |
|-------|--------------|---------|
| p = 13 | +0.4401 | YES (margin 0.06 from 0.5 threshold) |
| p = 19 | +0.3340 | YES (margin 0.17) |
| p ≥ 43 | ALL NEGATIVE | YES (correction reinforces B > 0) |

### Key observation
Correction/C' is monotonically decreasing for p ≥ 43 with M(p) = -3:
- p=43: -0.177
- p=107: -0.944
- p=431: -1.412

It becomes MORE negative with p, never returning to positive.

### M(p) ≤ -4 primes
Leading term ≥ 2C'. Correction/C' never exceeds 0.22. Massive margin.

## What IS NOT Proved (the gap)
An analytical proof that correction < 0 for ALL p ≥ 43 with M(p) = -3.

The structural reason: as p grows, the Möbius cancellation in the Abel remainder
becomes stronger (more terms, more cancellation). The correction involves
Σ_{k=1}^{N-1} [M(k)+2] · (delta-weighted partial sum), and the [M(k)+2] terms
have both signs, with increasing cancellation as N grows.

## Recommended approach for closure
1. Prove correction < 0 for p ≥ P₀ using El Marraki |M(k)| ≤ 0.6257k/logk
2. Verify p=43 to P₀ by exact computation
3. Combined: correction < C'/2 for ALL M(p)=-3 primes
