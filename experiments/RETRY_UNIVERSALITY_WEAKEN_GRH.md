## Summary
Zero-density estimates insufficient alone; exceptional zeros near $\sigma=1$ dominate on-resonance sums. Universality conditional on zero-free region excluding Siegel zeros, not just density.

## Analysis

| Regime | Re($\rho$) | Contribution Magnitude | Bound Mechanism |
| :--- | :--- | :--- | :--- |
| On-resonance | $1/2$ | $O(N^{-1/2})$ | $p^{-1/2}$ |
| Off-resonance | $1/2 < \beta < 1$ | $O(N^{\beta-1})$ | $p^{\beta-1}$ |
| Siegel Exceptional | $\beta \to 1$ | $O(N^{-\epsilon})$ | $p^{-\epsilon}$ |
| ZDE Bulk | $\sigma \in [1/2, 1)$ | $\sum T^{A(1-\sigma)}$ | Ingham $N(\sigma, T)$ |

Off-resonance sum $\sum_{\rho} N^{\beta-1}$. ZDE bounds count $N(\sigma, T)$. Integral $\int_{1/2}^1 N^{\sigma-1} dN(\sigma)$. Ingham estimate suppresses high $\sigma$ bulk, but single $\beta \approx 1$ escapes density constraint. $N^{\beta-1}$ vs $N^{-1/2}$. If $\beta > 3/4$, off-resonance dominates $N^{-1/2}$. ZDE allows $\beta$ arbitrarily close to 1 for finitely many zeros.

## Verdict/Next Steps
- Condition: Zero-free region near $\sigma=1$ (no Siegel zeros).
- Proof: Replace GRH hypothesis with effective zero-free region.
- Lean: Update 422 verified lemmas; add $1-\sigma$ bound check.
- Experiment: Check Farey discrepancy for $N > 500K$ against Siegel zero models.
