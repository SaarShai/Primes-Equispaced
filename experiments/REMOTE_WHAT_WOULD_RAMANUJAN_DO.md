## Summary
Current analysis isolates Farey discrepancy and Möbius fluctuations. Liouville, Ramanujan tau, Jordan totient, elliptic coefficients, lattice point counts constitute priority targets.

## Analysis

| Function | $L$-function Link | Spectroscopic Hypothesis |
| :--- | :--- | :--- |
| Liouville $\lambda(n)$ | $\zeta(s)$ | GUE universality parallel to $\mu(n)$ |
| Ramanujan $\tau(n)$ | Modular $\Delta$ | Lehmer conjecture, zero statistics |
| Jordan $J_k(n)$ | $\zeta(s-k)$ | Lattice density oscillations |
| Elliptic $a_p(E)$ | Hasse L-series | Sato-Tate distribution (GUE) |
| Sums of Squares $r_2(n)$ | Theta series $\theta^2$ | Gaussian integer lattice zeros |

## Verdict/Next Steps
- Compute Liouville spectrum (Priority 1).
- Verify $\lambda(n)$ in Lean 4 (align with 422 results).
- Apply $\gamma^2$ matched filter per Csoka 2015.
- Target $N=500K$ for statistical convergence.
- Compare RMSE against GUE baseline ($0.066$).
- Phase $\phi$ calculation for $\tau(n)$ follow Chowla protocol.
