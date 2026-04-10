## Summary
Visualization suite maps Farey discrepancies & Mertens bias to Zeta zero spectra. Interactive layers demonstrate GUE universality & prime denominator bursts.

## Analysis

| Feature | Farey Circle | Explicit Formula | Mertens Walk |
| :--- | :--- | :--- | :--- |
| **Visual Core** | Circle; mediant insertion | Curve $M(x)$ + zero modes | Random walk; prime bias |
| **Interaction** | Denom increment; color level | Slider: # Zeros | Toggle Prime/Composite |
| **Metric** | $\Delta W(N)$ burst | RMSE $0.066$ (GUE) | Spectroscope freq |
| **Context** | Prime denom spikes | $\sum \cos(\gamma \log x)/\gamma$ | Matches $\zeta$ zeros |
| **Verified** | 422 Lean 4 results | Chowla (N=500K) | $\phi = \text{-arg}$ |
| **Filter** | Gap distribution | Pre-whitening | Csoka 2015 ($\gamma^2$) |

## Verdict/Next Steps
*   Integrate Csoka 2015 gamma^2 matched filter (pre-whitening) into Mertens Walk.
*   Implement Phase $\phi$ solver in Explicit Formula tooltips.
*   Ensure GUE RMSE $0.066$ displayed on convergence plot.
*   Verify prime burst animation against Chowla N=500K evidence.
*   Prioritize 422 Lean 4 verified results for visual confirmation.
