## Summary
Liouville z-scores differ from Mertens via $\zeta(2s)$ weighting and full variance vs squarefree normalization. Liouville spectroscope yields statistically stronger zeta zero peaks, scaling scores by $|\zeta(2\rho)|\sqrt{\pi^2/6}$ with Csoka 2015 matched filter.

## Analysis
| Metric | Mertens ($M(n)$) | Liouville ($L(n)$) |
| :--- | :--- | :--- |
| Dirichlet Series | $1/\zeta(s)$ | $\zeta(2s)/\zeta(s)$ |
| Amplitude Factor | $1/\zeta'(\rho)$ | $\zeta(2\rho)/\zeta'(\rho)$ |
| Phase Shift | $-\arg(\zeta'(\rho))$ | $-\arg(\zeta(2\rho)\zeta'(\rho))$ |
| Term Density | $6/\pi^2 \approx 0.61$ | $1.00$ |
| Variance $\sigma^2$ | $x \cdot 6/\pi^2$ | $x$ |
| Chowla Test | $\sum \mu(n)\mu(n+h)$ | $\sum \lambda(n)\lambda(n+h)$ |
| Peak Strength | Baseline | Higher by $|\zeta(2\rho)|\sqrt{\pi^2/6}$ |
| GUE Match | RMSE=0.066 | Expected ~0.066 |

## Verdict/Next Steps
*   Liouville z-scores distinct and stronger than Mertens.
*   Liouville phase differs by $\arg(\zeta(2\rho))$.
*   Liouville Chowla correlations more robust due to full support.
*   Run Liouville GUE regression (target 422 Lean 4 verified threshold).
*   Update Csoka 2015 filter with $\lambda$ variance normalization.
