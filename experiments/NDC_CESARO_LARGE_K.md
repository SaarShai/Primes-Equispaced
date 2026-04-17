# NDC Cesaro Mean — Large K Verification

ρ₁ = 0.5 + 14.13472514173469i  
ζ(2) = π²/6 ≈ 1.6449340668482264  
mp.dps = 25 (mpmath)  
DRH reference: -e^{-γ_E} ≈ -0.5614594836 (Akatsuka 2013, limit for |D_K| at ζ zeros)

## K | |D_K*z2| | Cesaro(|D_K*z2|) | Re(Cesaro(D_K*z2))

| K   | \|D_K·ζ(2)\|   | Cesàro(\|D_K·ζ(2)\|) | Re(Cesàro(D_K·ζ(2))) |
|-----|----------------|----------------------|----------------------|
| 100 | 1.18891990     | 1.08681430           | 1.08085760           |
| 150 | 1.17047490     | 1.05706300           | 1.05228550           |
| 200 | 0.98929009     | 1.03174270           | 1.02505400           |
| 250 | 1.14756320     | 1.05592930           | 1.04838900           |
| 300 | 0.84100114     | 1.03247340           | 1.02386070           |
| 400 | 1.01710930     | 1.05222390           | 1.04238300           |
| 500 | 0.99500689     | 1.01653460           | 1.00535950           |

## Notes

- Cesàro(|D_K·ζ(2)|) = (1/K) Σ_{j=1}^K |D_j(ρ)·ζ(2)|
- Re(Cesàro) = (1/K) Σ_{j=1}^K Re(D_j(ρ)·ζ(2))
- DRH conjecture: |D_K| → e^{-γ_E} ≈ 0.5615 at ζ zeros (Akatsuka 2013)
- The quantity above is D_K·ζ(2), so DRH would predict |D_K·ζ(2)| → 0.5615 × 1.6449 ≈ 0.9234

## Conclusion

The Cesàro mean of |D_K·ζ(2)| is **slowly decreasing from 1.087 (K=100) toward ~1.017 (K=500)** but is NOT converging to 1.0 at this rate. The trend is:

- K=100: 1.0868
- K=200: 1.0317
- K=300: 1.0325
- K=400: 1.0522  (oscillation — non-monotone)
- K=500: 1.0165

The convergence is **slow and non-monotone** (oscillates). Re(Cesàro) tracks |Cesàro| closely (imaginary part ≈ 0 as expected since the sum is over real-valued |·|).

Comparing to Akatsuka DRH prediction: at K=500, |D_K·ζ(2)| ≈ 0.995, which is close to the DRH-predicted value of ~0.923. The individual |D_K·ζ(2)| values are oscillating around ~1.0 but NOT the Cesàro mean converging to 1.0. The conjecture that Cesàro mean → 1 remains **unverified at K=500** — more work needed (K >> 500).

Computed: 2026-04-16, mpmath dps=25.
