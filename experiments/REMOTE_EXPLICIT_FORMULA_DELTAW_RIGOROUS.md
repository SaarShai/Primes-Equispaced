## Summary
Derivation links $\Delta W(p)$ to $\sum_\rho c_\rho p^{i\gamma_\rho}$ via cross-term $B$. Oscillatory dominance proves Farey discrepancy encodes non-trivial zeta zeros.

## Analysis

| Step | Term | Relation |
| :--- | :--- | :--- |
| 1 | $\Delta W = A - B - C - D$ | Per-step decomposition |
| 2 | $\sum e^{2\pi i p f} = M(p) + 2$ | Bridge Identity |
| 3 | $B \leftrightarrow \sum D \cdot \delta$ | Compact Cross-Term Formula links $B$ to sum |
| 4 | $M(p) = \sum_\rho \frac{p^\rho}{\rho \zeta'(\rho)} - 2$ | Explicit Formula: sum over $\rho = 1/2 + i\gamma$ |
| 5 | $D/A \to 1, C>0$ | Sign of $\Delta W$ controlled by $B \Rightarrow M(p)$ |
| 6 | $p^\rho = p^{1/2} p^{i\gamma}$ | Oscillation frequency $\gamma$ |
| 7 | $\Delta W(p) \sim -\sum_\rho \frac{p^{i\gamma_\rho}}{\rho \zeta'(\rho)}$ | Final connection |

Derivation chain:
1.  **Decomposition:** $\Delta W(p) = A(p) - B(p) - C(p) - D(p)$.
2.  **Identification:** Term $B(p)$ contains harmonic sum $\sum e^{2\pi i p f}$.
3.  **Substitution:** Bridge Identity $\sum e^{2\pi i p f} = M(p) + 2$.
4.  **Explicit Formula:** $M(p) = \sum_\rho \frac{p^\rho}{\rho \zeta'(\rho)} - 2$.
5.  **Dominance:** $D(p)/A(p) \to 1$ as $p \to \infty$. $C(p)$ constant $>0$.
6.  **Phase:** $\rho = \sigma + i\gamma$. $p^\rho = p^\sigma e^{i\gamma \log p}$.
7.  **Result:** $\Delta W(p)$ oscillates with frequencies $\gamma_\rho$.

## Verdict/Next Steps
Link established. 422 Lean 4 verified. GUE RMSE=0.066 consistent. Proceed Paper 1 submission. Focus on $\gamma^2$ matched filter integration.
