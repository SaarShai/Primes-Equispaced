# Phase and Amplitude Data for First 10 Zeta Zeros
# Computed with mpmath at 30-digit precision, 2026-04-09

## Explicit formula: ΔW(p) ~ Σ_k A_k · cos(γ_k log p + φ_k)
## where A_k = |1/(ρ_k · ζ'(ρ_k))| and φ_k = arg(1/(ρ_k · ζ'(ρ_k)))

| k | γ_k | ζ'(ρ_k) | φ_k (rad) | |c_k| | A_k/A_1 |
|---|-----|---------|-----------|-------|---------|
| 1 | 14.1347 | +0.7833+0.1247i | -1.6933 | 0.089142 | 1.000 |
| 2 | 21.0220 | +1.1093-0.2487i | -1.3264 | 0.041831 | 0.469 |
| 3 | 25.0109 | +1.2958+0.4500i | -1.8851 | 0.029142 | 0.327 |
| 4 | 30.4249 | +1.1201-0.6675i | -1.0169 | 0.025203 | 0.283 |
| 5 | 32.9351 | +1.1606+0.7506i | -2.1297 | 0.021966 | 0.246 |
| 6 | 37.5862 | +1.8535-0.5610i | -1.2636 | 0.013738 | 0.154 |
| 7 | 40.9187 | +1.4595-0.3029i | -1.3540 | 0.016394 | 0.184 |
| 8 | 43.3271 | +1.4641+1.1037i | -2.2052 | 0.012587 | 0.141 |
| 9 | 48.0052 | +1.0339-1.1789i | -0.7096 | 0.013284 | 0.149 |
| 10 | 49.7738 | +1.2609+0.6508i | -2.0372 | 0.014158 | 0.159 |

## Key Observations

1. Amplitude decays roughly as 1/(γ_k · |ζ'(ρ_k)|)
2. γ₂ contributes 47% of γ₁ — significant
3. By k=6, amplitudes drop to ~15% — noise floor territory
4. The 5-term model (k=1..5) captures amplitudes down to 25% of A₁
5. Phases are NOT uniformly distributed: cluster near -1.5 ± 0.5 rad

## Prediction for Paper B
- 1-term model: R = 0.77 (empirical, matches)
- 2-term: should improve by ~(0.469)² ≈ 22% of remaining variance → R ≈ 0.85
- 5-term: captures ~(1 + 0.47² + 0.33² + 0.28² + 0.25²) normalized → R ≈ 0.93-0.96
- NEED: computational verification by running actual regression

## Corrections to Prior Work
- qwen fabricated ζ'(ρ₁) = -0.174 + 0.251i — COMPLETELY WRONG
- Actual: ζ'(ρ₁) = +0.783 + 0.125i
- qwen fabricated phases φ₁=2.54, φ₂=0.35, φ₃=-1.05, φ₄=-0.88, φ₅=1.42 — ALL WRONG
- Actual: φ₁=-1.69, φ₂=-1.33, φ₃=-1.89, φ₄=-1.02, φ₅=-2.13
