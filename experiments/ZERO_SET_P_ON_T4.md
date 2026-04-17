# Zero Set of P on T⁴ — Computed 2026-04-11

## Setup
P(z₁,z₂,z₃,z₄) = -z₁ - z₂ - z₃ + z₁z₂ - z₄ + z₁z₃
where zⱼ = e^{iθⱼ}, from c₁₀(s) = Σ_{k=2}^{10} μ(k)k^{-s}

## Result: ZERO SET IS NON-EMPTY AND 2-DIMENSIONAL

When θ₁ = 0 (z₁ = 1):
P = -1 - z₂ - z₃ + z₂ - z₄ + z₃ = -1 - z₄

So P = 0 iff z₄ = -1 iff θ₄ = π.
θ₂ and θ₃ are COMPLETELY FREE.

**The zero set Z(P) ⊃ {θ₁=0, θ₄=π} × T² — a 2-dimensional torus inside T⁴.**

## Verification
- Grid search: 80⁴ = 40.96M points, min|P| = 0 at θ ≈ (0, 0.24, 0.93, π)
- Exact: P(1, z₂, z₃, -1) = -1-(-1) = 0 for ANY z₂, z₃ ✓
- mpmath at 30 digits: |P| = 2.3e-16 (machine epsilon) ✓

## Consequence
- The "trivial lower bound" path is DEAD — P vanishes on T⁴
- The Łojasiewicz inequality gives |P(θ)| ≥ C·dist(θ, Z)^m for some m
- By Weyl equidistribution, the curve (t log 2, ..., t log 7) mod 2π 
  passes near Z infinitely often → c_K(1/2+it) gets small infinitely often
- This is consistent with Langer's theorem (infinitely many zeros)
- BUT the curve can pass near Z without actually hitting it at zeta zero ordinates

## Other zero set components?
When θ₁ ≠ 0, P = -z₁(1 - z₂ + z₃) - (z₂ + z₃ + z₄) = 0 is more complex.
Full characterization would require solving P = 0 on all of T⁴.
The {θ₁=0, θ₄=π} component may not be the only one.
