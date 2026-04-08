## Summary
Fix prediction failure & redundant metrics.
Adopt hybrid dynamical-statistical framework.

## Analysis
| Issue | Solution | Rationale |
| :--- | :--- | :--- |
| 0/4199 empty-cell predictions | ML (C) | Boost specificity |
| Hristov test failure | Lyapunov (B) | Capture chaos regimes |
| rho=0.994 redundancy | Orthogonal features (C) | Reduce multicollinearity |
| Predictive power uncertainty | Figure-eight (D) | Anchor phi-conjecture |

## Verdict/Next Steps
1. Integrate Lyapunov exponents (B)
2. Train ML on Figure-eight data (C, D)
3. Verify stability via Lean 4
4. Exclude Li-Liao extension (A)
