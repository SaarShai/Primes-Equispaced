# EDRH Divergence Theory — Codex Analysis
**Date:** 2026-04-16  
**Source:** Codex deep thinking agent

---

## Q1: Rate of |E_K(ρ)| at zeta zeros

NOT O(log K). The sum S_K(ρ) = Σ_{p≤K} p^{-1/2-iγ} has main term from Li(K^{1-ρ}):

log|E_K(ρ)| = Re(Li(K^{1-ρ})) + O(1)

|E_K(ρ)| oscillates with envelope **exp(Θ(√K / log K))**.

This is much stronger than O(log K). The analogy with |ζ(1+it)| ~ (log t)^O(1) breaks down entirely — at the critical line the Li term changes the asymptotic scale.

## Q2: Rate of |c_K(ρ)| at zeta zeros

Under RH: M(t) ≪ t^{1/2+ε}. Partial summation gives:

|c_K(ρ)| ≪ K^ε   (under RH)

So c_K = O(K^ε) — no genuine power growth. The cancellation between c_K and E_K is extraordinary: E_K grows as exp(Θ(√K/log K)), c_K grows as K^ε, yet D_K = c_K·E_K → -e^{-γ}. This means c_K must oscillate at the reciprocal rate to E_K.

## Q3: Exponent m and constant C

**Sheth [2025, Cambridge Math. Proc.] — VERIFY CITATION before using.**

If correct: For primitive Dirichlet χ, simple zero ρ_χ (m=1 universally):
- E_K^χ(ρ_χ) · log K → √2^{ν(χ)} · |L'(ρ_χ,χ)| / e^γ
- ν(χ) = -ord_{s=1} L(s,χ²) = 1 if χ² principal, 0 if χ² nonprincipal
- χ_{-4} (χ² principal): √2 factor. C = √2·|L'(ρ,χ_{-4})|/e^γ
- χ_5, χ_11 (χ² nonprincipal): no √2. C = |L'(ρ,χ)|/e^γ

**C correction**: denominator is e^γ ≈ 1.781, not ζ(2) ≈ 1.645. Ratio e^γ/ζ(2) ≈ 1.083 — would improve our 88-93% fits.

m=1 for ALL simple zeros regardless of character order. ν(χ) affects the CONSTANT, not the exponent.

## Q4: Proved vs Conjectured

| Statement | Status | Citation |
|-----------|--------|----------|
| D_K(ρ) → -e^{-γ} for ζ zeros | PROVED | Akatsuka 2017, Kodai Math. J. 40:79 |
| E_K^χ(ρ_χ)·log K → C for primitive Dirichlet χ | PROVED (conditional GRH+RP) | Sheth 2025 — VERIFY |
| D_K^χ(ρ_χ) → specific constant at non-central zeros | OPEN | Not in literature |

## Q5: Paper G Paragraph (verbatim from Codex)

Akatsuka [Ak17] proved that for any nontrivial zero ρ of the Riemann zeta function, D_K(ρ) → -e^{-γ}. For primitive Dirichlet L-functions, the central-point behavior was established by Sheth [She25] under GRH + Ramanujan–Petersson: if m = ord_{s=1/2} L(s,π), then (log x)^m Π_{p≤x}(1-α_{j,p}p^{-1/2})^{-1} converges to (√2^{ν(π)}/e^{mγ} m!) L^{(m)}(1/2,π), where ν(π) = -ord_{s=1} L(s,π²) in the degree-one case. For simple zeros, m=1 universally, with constant proportional to L'(ρ_χ,χ)/e^γ; quadratic characters (χ² principal) pick up an additional √2 factor. By contrast, the behavior of D_K^χ(ρ_χ) at an arbitrary non-central zero of a primitive Dirichlet L-function remains **unproved**; numerical evidence suggests (log K)^{-1} decay for E_K^χ, consistent with simplicity, but a rigorous limit theorem is open.

## CRITICAL FLAGS

1. **VERIFY SHETH 2025**: Search "Sheth Cambridge Math Proc 2025 Euler product" before citing. Could be fabricated.
2. **Akatsuka 2017 Kodai Math J 40:79**: More specific than previous "Akatsuka 2013" — verify which year/journal.
3. **C formula**: e^γ vs ζ(2) — need numerical test to distinguish (factor of 1.08).
4. **E_K divergence exp(Θ(√K/log K))**: Much stronger than O(log K). Verify by computing |E_K(ρ_1)| for K=100,1000,10000.
