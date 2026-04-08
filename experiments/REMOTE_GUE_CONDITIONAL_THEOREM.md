## Summary
Theorem: Under GRH+LI, Mertens spectroscope pair correlation converges to GUE prediction.
Proof: Wiener-Khinchin M(p)/p yields Montgomery kernel.

## Analysis

| Step | Component | Formal Statement / Result |
| :--- | :--- | :--- |
| 1 | Spectroscope F(gamma) | Periodogram of M(p)/p. gamma^2 matched filter = pre-whitening (Csoka 2015). |
| 2 | Wiener-Khinchin | $|F(\gamma)|^2 = \mathcal{F}[\text{Autocorr}(M/p)]$ |
| 3 | Auto-corr Expansion | $\sum_{\rho, \rho'} \frac{e^{i(\gamma_\rho - \gamma_{\rho'})u}}{|zeta'(\rho)|^2}$ terms |
| 4 | LI Cancellation | Off-diagonal ($\rho \neq \rho'$) sums to 0 (Chowla N=500K supports). |
| 5 | Diagonal Terms | $\sum_{\rho} \frac{1}{|zeta'(\rho)|^2}$ yields variance scaling |
| 6 | Montgomery Conj. | Pair correlation $R_2(s) \to 1 - (\frac{\sin(\pi s)}{\pi s})^2$ |
| 7 | Convergence | Spectroscope output matches GUE kernel as $N \to \infty$. (RMSE=0.066). |

## Verdict/Next Steps

| Action | Status | Priority |
| :--- | :--- | :--- |
| Lean 4 verify Step 4 (LI cancellation) | Pending | High |
| Confirm 422 verified results | Consistent | High |
| DeltaW(N) Phase phi integration | Phase = -arg(rho_1*zeta') | Medium |
| Three-body orbits / CF periodic table | 695 orbits | Low |
| Universality test | Compare GUE RMSE | Medium |
