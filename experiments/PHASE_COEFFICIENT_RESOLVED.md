# RESOLVED: Phase Coefficient for ΔW explicit formula
# 2026-04-09 — Computed with mpmath at 30-digit precision

## Result
The correct coefficient is **1/(ρ·ζ'(ρ))**, NOT 1/((ρ-1)·ζ'(ρ)).

## Computation
ρ₁ = 0.5 + 14.1347251417346937904572519836i
ζ'(ρ₁) = 0.783296511867030928649657209239 + 0.124699829748171089409928491509i
|ζ'(ρ₁)| = 0.793160433356506116013897565274

### Candidate A: c = 1/(ρ·ζ'(ρ))
arg(c) = -1.6933 rad
Match to φ_empirical = -1.69: **Δ = 0.003 rad** ← PERFECT

### Candidate B: c = 1/((ρ-1)·ζ'(ρ))
arg(c) = -1.7640 rad
Match to φ_empirical = -1.69: Δ = 0.074 rad ← worse

## Conclusion
The explicit formula for ΔW(p) uses the STANDARD Mertens function coefficient:
ΔW(p) ~ Σ_ρ p^ρ / (ρ·ζ'(ρ))

The (ρ-1) form proposed in task_110 was INCORRECT.
The 0.003 rad residual in Candidate A is likely due to:
- Higher-order zeros (γ₂, γ₃, ...) contributing small phase shifts
- Finite N effects in the empirical measurement

## Impact
- MPR-27: RESOLVED. Coefficient is 1/(ρ·ζ'(ρ)).
- MPR-40: Phase reconciliation DONE. No ρ vs ρ-1 ambiguity.
- Paper B: Phase formula φ = -arg(ρ₁·ζ'(ρ₁)) = -1.6933 rad is CORRECT as originally stated.
- The qwen-fabricated ζ'(ρ₁) ≈ -0.174 + 0.251i was COMPLETELY WRONG.
  Actual value: 0.783 + 0.125i.

## Note on ζ'(ρ₁)
The LMFDB-compatible value ζ'(ρ₁) = 0.7833 + 0.1247i should be used in all future work.
