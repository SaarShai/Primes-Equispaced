# B_∞ Formula Theory — Codex Analysis
**Date:** 2026-04-16  
**Source:** Codex deep thinking agent  
**Status:** HIGH QUALITY — save to Paper G

---

## Main Result (Paper G Theorem)

**Theorem (conditional on GRH for input).** Let χ be a primitive Dirichlet character mod q, ρ_χ a simple zero of L(s,χ) with Re(ρ_χ)=1/2, and L(2ρ_χ,χ²)≠0. Define
$$B_K(\chi,\rho_\chi) := \Im\log\prod_{p\le K}(1-\chi^2(p)p^{-2\rho_\chi})^{-1}$$
along the continuous branch. Then
$$\lim_{K\to\infty} B_K(\chi,\rho_\chi) = \Im\log L(2\rho_\chi,\chi^2).$$

**For nonprincipal χ²: UNCONDITIONAL** (no GRH beyond Re(ρ_χ)=1/2). de la Vallée Poussin proves L(s,χ²)≠0 on Re=1 unconditionally. PNT for arithmetic progressions gives convergence.

**For principal χ² (χ_{-4}² = χ₀ mod 4, χ₀²=χ₀):** Titchmarsh §3.15 proves Euler product convergence on Re=1, t≠0.

**Failure excluded under GRH:** zeros ρ of L(s,χ) have Re=1/2 (by GRH), so 2ρ lies on Re=1 where L(s,χ²) has no zeros. Failure condition L(2ρ,χ²)=0 is automatically impossible.

---

## Convergence Rates (explains numerics)

| Character | χ²type | Rate | Numerics |
|-----------|--------|------|----------|
| χ₀, χ_{-4} | Principal | O(1/log K) — slow | ±0.015 at K=1000 |
| χ₅ | Nonprincipal | O(K^{-1/2} log² K) under GRH | ±0.0002 at K=500 |

**Why**: principal χ² has main term in Σ_p χ²(p)/p^{1+it} ~ π(K)/K^{1+it} → O(1/log K). Nonprincipal χ²: full cancellation via PNT in arithmetic progressions, A(x)=O(x^{1/2}log²x) under GRH → O(K^{-1/2}).

---

## B_K vs Im(log D_K) — Two DIFFERENT Objects

D_K(ρ) = Π_{p≤K}(1-χ(p)p^{-ρ})^{-1} evaluated at zero ρ of L(s,χ).
B_K = Im(log Π_{p≤K}(1-χ²(p)p^{-2ρ})^{-1}) = Euler product of χ² at 2ρ.

Two differences:
1. Local factors: χ(p) → χ²(p)
2. Evaluation point: ρ (zero of L(s,χ)) → 2ρ (on Re=1, NOT a zero of L(s,χ²))

For χ=χ₀: D_K(ρ) → -e^{-γ_E} (real), Im(log D_K) → ±π ≠ -0.170 = B_∞.
The squaring and doubling TOGETHER escape the zero: χ→χ² removes first-order zero structure, ρ→2ρ moves to nonzero boundary.

---

## Character Analysis

**χ_{-4}²**: χ_{-4}² = principal mod 4. L(s,χ_{-4}²) = ζ(s)·(1-2^{-s}).
arg L(s) = arg ζ(1+12.04i) + arctan(2^{-1}sin(t log 2)/(1-2^{-1}cos(t log 2))).
Principal character → O(1/log K) convergence.

**χ₅²**: Legendre symbol mod 5 (nonprincipal, order 2). L(s,χ₅²) entire.
Strongest cancellation among 3 examples → fastest convergence O(K^{-1/2} log² K).

---

## Connection to T_∞

T_∞ = (1/2)·Im(log L(2ρ,χ²)) = (1/2)·B_∞.
The 1/2 normalization: from the definition B_K = Im(log E_K^{χ²}(2ρ)).
The factor 2 in 2ρ and the squaring χ→χ² are the "second moment" structure that makes the formula stable.

---

## References
- Titchmarsh, *Theory of the Riemann Zeta-Function*, §3.15 (Euler product on σ=1)
- Conrad, *Partial Euler Products on the Critical Line*, Canadian J. Math.
- Kaneko, *Euler Product Asymptotics for Dirichlet L-Functions*, Bull. Australian Math. Soc.
- DLMF §27.4

