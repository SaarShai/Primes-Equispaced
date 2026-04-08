## Summary
W-K application invalid for singular distributions without regularization. LI guarantees independence but not pair-correlation convergence rates.

## Analysis

| Query | Gap | Status |
|---|---|---|
| W-K Applicability | Signal is distribution, not $L^2$ | **Fail** |
| Diagonal/Off-diagonal | LI insufficient for pair-exponential cancellation | **Partial** |
| Convergence Uniformity | Pointwise proven, uniformity unverified | **Unknown** |

## Verdict/Next Steps
Proof requires explicit distributional Wiener-Khinchin derivation. Add spectral gap constraints to pair-correlation sums. Verify test function decay in Lean 4. Formalize 6.4KB proof steps for distributional limits.
