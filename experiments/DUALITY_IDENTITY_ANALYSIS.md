# Duality Identity Analysis — Session 13

**Date:** 2026-04-13  
**Status:** Partially resolved (pending Codex + deepseek confirmation)

## The Setup

At simple zero ρ = 1/2 + iγ of ζ:

- **Additive**: c_K(ρ) = Σ_{k≤K} μ(k)k^{-ρ} [Perron/RH] → -log K/ζ'(ρ)
- **Multiplicative**: euler_inv_K = Π_{p≤K}(1-p^{-ρ})^{-1} [DRH(A)] → ζ'(ρ)/(e^{γ_E} log K)
- **Product**: Q_K = Π_{p≤K}(1-p^{-ρ}) = 1/euler_inv_K → e^{γ_E} log K/ζ'(ρ)^{-1}

Wait — careful sign: euler_inv ~ ζ'(ρ)/(e^{γ_E} log K) → 0. So Q_K = 1/euler_inv ~ e^{γ_E} log K/ζ'(ρ) → ∞? No:

**Corrected DRH(A) statement**: (log K) · Π_{p≤K}(1-p^{-ρ})^{-1} → ζ'(ρ)/e^{γ_E}

So euler_inv ~ ζ'(ρ)/(e^{γ_E} log K) ... wait, that would mean the INVERSE grows to ∞? Let me restate precisely.

### DRH(A) for ζ at simple zero ρ (m=1):

(log K) · Π_{p≤K}(1-p^{-ρ})^{-1} → ζ'(ρ)/e^{γ_E}

Therefore: |Π_{p≤K}(1-p^{-ρ})^{-1}| ~ |ζ'(ρ)|/(e^{γ_E} log K) → 0

So: |Q_K| = |Π_{p≤K}(1-p^{-ρ})| = 1/|euler_inv| ~ e^{γ_E} log K/|ζ'(ρ)| → ∞

Hmm, OR is it:

(log K) · euler_inv → C, meaning euler_inv ~ C/log K → 0, meaning Q_K ~ log K → ∞?

## The Consistent Picture

From the M1 numerical task:
- R1 = |euler_inv| · |ζ'(ρ)| / log K → e^{γ_E} = 1.78107
  ⟹ |euler_inv| ~ e^{γ_E} log K / |ζ'(ρ)| → ∞
  ⟹ Q_K = 1/euler_inv → |ζ'(ρ)|/(e^{γ_E} log K) → 0

- R2 = |c_K| · |ζ'(ρ)| / log K → 1
  ⟹ |c_K| ~ log K / |ζ'(ρ)| → ∞

- P_K = c_K · (1/euler_inv) = c_K · Q_K

|P_K| = |c_K| · |Q_K| = (log K/|ζ'|) · (|ζ'|/(e^{γ_E} log K)) = **1/e^{γ_E} = e^{-γ_E}** ✓

**So duality identity P_K → -e^{-γ_E} is CONSISTENT and EQUIVALENT to DRH(A) given Perron.**

## Revised DRH(A) Interpretation

DRH(A): euler_inv = Π_{p≤K}(1-p^{-ρ})^{-1} grows like e^{γ_E} log K / ζ'(ρ) → ∞  
Therefore: Q_K = Π_{p≤K}(1-p^{-ρ}) shrinks like ζ'(ρ)/(e^{γ_E} log K) → 0

This means Σ_{p≤K} p^{-ρ} must diverge like **log log K** (not K^{1/2}/log K).

Why? Because: log Q_K = Σ_p log(1-p^{-ρ}) = -Σ_{p≤K} p^{-ρ} - Σ_{p≤K} p^{-2ρ}/2 - ...
If Q_K ~ C/log K, then log Q_K ~ -log log K.
So Σ_{p≤K} p^{-ρ} ~ log log K (main term).

## Key Question: Why Not K^{1/2}/log K?

Naive partial summation: Σ_{p≤K} p^{-ρ} ~ ∫ x^{-ρ}/log x dx ~ K^{1/2-iγ}/(ρ log K), magnitude K^{1/2}/(|ρ| log K) → ∞ fast.

BUT: at s = ρ (a zero of ζ), the EXPLICIT FORMULA for π(x) creates a resonance. The contribution from ρ itself in the Riemann-von Mangoldt formula:

π(x) ⊃ -li(x^ρ) ≈ -x^ρ/(ρ log x)

When computing ∫_2^K x^{-ρ} d(π(x)) with the ρ-term from explicit formula:

∫_2^K x^{-ρ} · d(-li(x^ρ)) = -∫_2^K x^{-ρ} · x^{ρ-1}/(ρ log x) dx = -1/ρ ∫_2^K x^{-1}/log x dx = -log log K/ρ + O(1)

This cancels the dominant K^{1/2} term! The net result:

**Σ_{p≤K} p^{-ρ} ~ log log K/ρ + C(ρ) + O(oscillatory/cancelling terms)**

This is the KEY CANCELLATION: the zero ρ absorbs its own K^{1/2} growth from the prime sum. At a zero, the prime sum has only logarithmic (not power) divergence.

## Summary of the Chain

1. **[RH + simple zeros]** c_K(ρ) ~ -log K/ζ'(ρ) [Perron, proved]
2. **[Explicit formula + cancellation at zero]** Σ_{p≤K} p^{-ρ} ~ log log K/ρ
3. **[From 2]** Q_K ~ C(ρ)/log K → 0 (partial Euler product shrinks)
4. **[DRH(A)]** The constant in Q_K ~ C(ρ)/log K is C(ρ) = ζ'(ρ)e^{-γ_E} [unproved]
5. **[1 + 4]** P_K = c_K · Q_K → (-1/ζ'(ρ)) · ζ'(ρ)e^{-γ_E} = -e^{-γ_E} ✓

## Status

- Step 2 (cancellation): PLAUSIBLE from explicit formula argument. Needs rigorous proof [RH-conditional].
- Step 4 (constant identification): Equivalent to DRH(A). Cannot prove without DRH.
- Step 2 + 3 (Q_K ~ C/log K): May be provable from PNT + explicit formula WITHOUT DRH.
- Full duality identity: EQUIVALENT TO DRH(A) given Perron [under RH + simple zeros].

**Conclusion**: Proving P_K → -e^{-γ_E} would require either:
(a) Proving DRH(A) directly (open problem), or
(b) Identifying the constant in Q_K ~ C/log K from first principles (= proving DRH(A) for ζ).

The identity is elegant and correct assuming both results; it is a REFORMULATION not a simplification of DRH(A).

**New question**: Can we prove Q_K ~ C/log K (without identifying C) from PNT + explicit formula?
This would give P_K = c_K · Q_K ~ (log K) · C/log K = C [some finite constant], 
possibly provable unconditionally, though C = -e^{-γ_E} requires DRH.

