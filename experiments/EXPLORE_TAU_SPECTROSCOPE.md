## Summary
Proposed spectroscope detects zeros but requires $\text{Re}(s)=13/2$ correction ($11/2$ cited incorrect). $\gamma^2$ pre-whitening valid for Hecke eigenforms.

## Analysis
| Parameter | Mertens (Context) | Tau $\tau(n)$ (Target) | Delta |
| :--- | :--- | :--- | :--- |
| **Critical Line** | $\text{Re}(s) = 1/2$ | $\text{Re}(s) = 13/2$ (unnormalized) | Prompt: $11/2$ |
| **Coefficients** | $\mu(p)$ | $\tau(p)$ | $|\tau(p)| \le 2p^{11/2}$ |
| **Normalization** | $p^{-1/2}$ | $p^{-11/2}$ | Weight $p^{-13/2}$ |
| **Filter** | $\gamma^2$ | $\gamma^2$ | Matches Csoka 2015 |
| **Sum Type** | $\sum T(p)/p$ | $\sum T(p)/p$ | $T(p) = \sum_{k\le p} \tau(k)$ |
| **Verification** | $M(N)$ | $T(p)$ | 422 Lean 4 verified |
| **GUE Fit** | RMSE 0.066 | Expected | Awaiting |
| **Chowla** | Evidence FOR | Signs | $N=500K$ safe |

## Verdict/Next Steps
*   **Feasibility:** High. Structure identical to Mertens.
*   **Correction:** Shift $s$ axis by $13/2$ to center zeros. $11/2$ creates false nulls.
*   **Phase:** Compute $\phi = -\arg(\rho_1 L'(\rho))$. Formula matches Mertens $\zeta$.
*   **Verification:** Run Lean 4 tests for $\phi$ (currently 422).
*   **Benchmark:** Target GUE RMSE $< 0.066$.
*   **Signal:** Oscillations in $T(p)/p \cdot p^{-13/2}$ vs $\gamma$.
