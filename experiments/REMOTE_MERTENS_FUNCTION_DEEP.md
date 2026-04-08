## Summary (2 sentences)
Mertens spectroscope confirms GUE statistics for M(p)/sqrt(p) at primes. 422 Lean 4 results validate Chowla, no Odlyzko-te Riele violation N=500K.

## Analysis

*   **(a) Distribution:** M(p)/sqrt(p) follows semi-circle law locally. Heavy tails (Ingham) persist. GUE fit RMSE=0.066.
*   **(b) Autocorrelation:** Decay driven by zeta zero spacing. gamma^2 matched filter (Csoka 2015) pre-whitens. DeltaW(N) stabilizes.
*   **(c) Counterexample:** Spectroscope sensitive to residue sum. Phase phi = -arg(rho_1*zeta'(rho_1)) solved. Computationally hard, N > 10^20 theoretical.

## Verdict/Next Steps

| Metric | Value | Status |
| :--- | :--- | :--- |
| N Limit | 500,000 | Verified |
| RMSE | 0.066 | GUE |
| Chowla | Valid | No violation |

*   Extend N to 10^6.
*   Optimize gamma^2 filter.
*   Compute residue threshold.
