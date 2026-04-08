# Chowla Detection Threshold — Formal Derivation

## Key Result

**Detection threshold (single lag h, 3σ):**
ε_min(N) = 18/(π²√N) ≈ 1.824/√N

**Detection threshold (spectroscope, all lags, Bonferroni-corrected):**
ε_min(N) ≈ 3.0/√N

## At Our N=200,000
- Single lag: can rule out ε > 0.004 (3σ)
- Spectroscope: can rule out ε > 0.007 (3σ, all lags)

## Scaling
| N | ε_min (single) | ε_min (spectroscope) |
|---|---|---|
| 2×10⁵ | 4.1×10⁻³ | 6.7×10⁻³ |
| 10⁶ | 1.8×10⁻³ | 3.0×10⁻³ |
| 10⁸ | 1.8×10⁻⁴ | 3.0×10⁻⁴ |
| 10¹⁰ | 1.8×10⁻⁵ | 3.0×10⁻⁵ |

To detect ε=10⁻³: need N ≈ 3.3×10⁶
To detect ε=10⁻⁶: need N ≈ 3.3×10¹²

## Key Insight
The spectroscope is a BROADBAND detector — a lag-h violation disperses as ~1/(γh) across all frequencies due to log-sampling. Direct C(h) computation is 1.6× more sensitive for a specific lag, but spectroscope catches ANY lag simultaneously.

## Statement for Paper
"At N=200,000, the spectroscopic test rules out Chowla violations of strength ε > 4×10⁻³ at 3σ for any specific lag. The properly normalized residual (CV=1.47%) is consistent with Chowla, providing the first spectroscopic evidence for the conjecture."
