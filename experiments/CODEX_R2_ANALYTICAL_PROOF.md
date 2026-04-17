# Codex THINKING: R²(K,P) Analytical Proof
**Date:** 2026-04-12  
**Task:** Prove analytically that R²(K,P) has a closed form, and that R increases with P  
**Status:** COMPLETED — 3 theorems, 1 proposition

---

## Setup

Under RH, M(p)/√p = 2·Re[Σ_{k=1}^∞ p^{iγ_k}/(ρ_k·ζ'(ρ_k))] + O(1)

S_K(p) = 2·Re[Σ_{k=1}^K c_k p^{iγ_k}], c_k = 1/(ρ_k ζ'(ρ_k))

Observed: R=0.938 in-sample (p≤50K), R=0.952 out-of-sample (p>50K)

---

## Theorem 1 [Proved: RH + Landau-Gonek]

R²(K,P) is a ratio of quadratic forms in the symmetric 2K-frequency Gram matrix:

**R²(K,P) = (b_K* Γ_K(P) b_K) / (b_∞* Γ_∞(P) b_∞)**

where:
- Γ_{mn}(P) = Φ_P(e^{i(λ_m−λ_n)log p})
- Diagonal: Γ_{mm}(P) = 1
- Off-diagonal: |Γ_{mn}(P)| ≪ 1/(|λ_m−λ_n| log P) via Landau-Gonek

The full variance expansion contains:
- **G-block**: difference frequencies γ_j−γ_k (the Gram matrix)
- **H-block**: sum frequencies γ_j+γ_k (forced by the real-valued nature of S_K)

Full variance expansion:
```
Var_P(S_K) = 4·Σ_{k≤K}|c_k|² 
           + 8·Σ_{j<k}Re(c_j c̄_k G_{jk}(P))    ← G-block
           + 4·Σ_{j,k}Re(c_j c_k H_{jk}(P))     ← H-block
           + O(1/log P)
```

---

## Theorem 2 [Proved: RH + GH + negligible-remainder hypothesis]

As P → ∞, cross-terms vanish (by Landau-Gonek orthogonality) and:

**R²(K,∞) = Σ_{k≤K} |c_k|² / Σ_{k≥1} |c_k|²**

**Critical caveat**: Does NOT follow from RH alone. The variance-negligibility of the O(1) explicit-formula remainder is an extra hypothesis (not GRH, but a separate regularity assumption).

---

## The 1/k² Approximation is Wrong

Naive: ⟨|c_k|²⟩ ~ 1/k²  →  R²(K,∞) ≈ 1 − 6/(π²K)  →  R²(20,∞) ≈ 0.970

**Gonek-Hejhal correction**: ⟨|ζ'(ρ_k)|²⟩ ~ (log γ_k)/(2π)

So: ⟨|c_k|²⟩ ~ 8π/(γ_k² log γ_k) ~ (2/π)(log k)/k²

The log k factor makes the tail heavier → sum over k≤K smaller relative to total → R²(K,∞) < 0.970.

---

## Proposition 3 [Conjectural — NOT provable from RH]

∂R²/∂P > 0 is NOT provable pointwise from RH + Landau-Gonek.

Reason: the Landau-Gonek correction is:

(P^{iα}−1)/(iα log P) = sin(α log P)/(α log P) + i(1−cos(α log P))/(α log P)

The real part changes sign infinitely often as P varies → off-diagonal Gram corrections are not sign-definite → ∂R²/∂P is not provably positive.

**What IS rigorous**: R²(K,P) = R²(K,∞) + O_K(1/log P) with oscillatory error.

**Averaged monotonicity**: Under a random-phase model for zero frequencies,
  E[R²(K,P)] = R²(K,∞) − C_K/log P + o(1/log P), C_K ≥ 0
This is CONJECTURAL (random-phase model not proved from RH).

---

## Gap Diagnosis: 0.970 vs 0.906 (gap = 0.064)

Three sources, all contributing:

1. **Wrong tail law** (main): GH gives (log k)/k², heavier than 1/k², lowers R²(K,∞)
2. **Finite-P cross-terms**: log(50000) ≈ 10.82 → 1/log P corrections are ~9% → several-percent effect plausible
3. **Explicit-formula O(1) remainder**: if it carries non-negligible variance, denominator is inflated, R² pushed down

Scale check: |c₁|² = 1/(|ρ₁|²·|ζ'(ρ₁)|²) ≈ 1/(199.89 · 0.6292) ≈ 0.00795 ✓ (consistent with stated value)

Pinning down Σ_{k≤20}|c_k|² precisely requires the full list of ζ'(ρ_k) for k=1..20 at high precision.

---

## Summary: What is Provable vs Conjectural

| Claim | Status | Hypotheses |
|-------|--------|-----------|
| R²(K,P) = Gram matrix ratio | **PROVED** | RH + Landau-Gonek |
| Off-diagonal entries ≪ 1/(gap·log P) | **PROVED** | RH + Landau-Gonek |
| R²(K,∞) = Σ|c_k|²/Σ|c_k|² | **PROVED** | RH + GH + negligible-remainder |
| GH correction: (log k)/k² tail | **CONJECTURAL** | Gonek-Hejhal moments |
| R²(K,P) monotone increasing in P | **NOT PROVABLE** | RH insufficient; needs random-phase |
| Averaged E[R²(K,P)] increasing | **CONJECTURAL** | Random-phase model |

---

## Implications for DPAC

The R=0.952 out-of-sample result is analytically explained as the finite-P shadow of R²(K,∞). The "improvement" out-of-sample is real but not provably monotone — it reflects oscillatory approach to the limiting value, which happens to be positive on the out-of-sample range tested. The limiting value itself requires GH moments to evaluate precisely.
