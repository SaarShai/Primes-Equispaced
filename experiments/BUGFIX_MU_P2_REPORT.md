# Bug Report: μ_f(p²) Wrong in C₁ Ensemble Scripts

**Date:** 2026-04-20  
**Found by:** Codex review of koyama-shared/  
**Severity:** HIGH — affects all ensemble E[C₁²] results  
**Status:** Scripts FIXED. Results need recomputation.

---

## The Bug

### Correct formula

For a cusp form f of weight k with Hecke eigenvalues a_p, the Dirichlet series for 1/L(s,f) has multiplicative coefficients μ_f(n) satisfying:

- μ_f(p) = −a_p  
- **μ_f(p²) = a_p² − a_{p²}** (from the convolution inverse formula)
- μ_f(p^k) = 0 for k ≥ 3 (when the Euler factor is degree 2)

By the Hecke recursion:
- EC (weight 2): a_{p²} = a_p² − p → **μ_E(p²) = p**  
- Δ (weight 12): a_{p²} = τ(p)² − p^11 → **μ_Δ(p²) = p^11**

These follow from the Euler factor (1 − a_p x + p^{k−1} x²) for 1/L(s,f) at good prime p.

### What the code computed (WRONG)

```python
# 37a1 and 389a1 scripts (OLD — WRONG):
v = a*a-p if kpow==2    # = a_{p²}, NOT μ_E(p²) = p

# Delta script (OLD — WRONG):
v = tp*tp - p**11 if kpow==2    # = τ(p²), NOT μ_Δ(p²) = p^11
```

The code uses the Hecke eigenvalue a_{p²} where it should use the INVERSE coefficient μ_f(p²).

### Fixed code (in koyama-shared/scripts/, as of 2026-04-20):

```python
# 37a1 and 389a1 scripts (NEW — CORRECT):
v = p if kpow==2    # μ_E(p²) = p

# Delta script (NEW — CORRECT):
v = p**11 if kpow==2    # μ_Δ(p²) = p^11
```

---

## Impact on Results — NUMERICALLY VERIFIED

**PARI-verified a_p data at K=3000 (scripts: BUGFIX_FINAL_COMPARE.py):**

| Curve | C₁_wrong (K=3000) | C₁_correct (K=3000) | ratio | C₁² scale |
|-------|-------------------|---------------------|-------|------------|
| 37a1  | 0.0890            | 0.0842              | 0.946 | 0.895×     |
| Δ     | 0.4978            | 0.8906              | **1.789** | **3.20×** |

**Ratio trend (|c_K(correct)| / |c_K(wrong)|) for Δ:**
- K=500: 1.701, K=1000: 1.736, K=2000: 1.769, K=3000: 1.789 → still increasing toward K→∞

**Impact on claimed E[C₁²] values:**

| Claim | Pre-bugfix value | Estimated post-fix | Valid? |
|-------|-----------------|-------------------|--------|
| E[C₁²](37a1) at N=500 zeros | 2.561 | ~2.3 | Minor change |
| E[C₁²](Δ) at N=500 zeros | 2.473 | ~7.9 | **COMPLETELY WRONG** |
| E[C₁²](389a1) at N=500 zeros | 5.660 | Unknown | Need recompute |
| C₁(Δ,γ₁)=0.4964 at K=10⁵ | 0.4964 | ~0.9+ | **WRONG** |
| "4% match between 37a1 and Δ" | 4% | **factor ~3.4×** | **INVALIDATED** |

### Why Δ is so much more affected

For Δ: wrong μ_Δ(4) = τ(2)²−2^{11} = 576−2048 = −1472 (NEGATIVE)  
vs correct μ_Δ(4) = 2^{11} = 2048 (POSITIVE)

The ratio wrong/correct = −1472/2048 ≈ −0.72, with opposite sign. This one term at n=4 alone causes a factor ~1.7 error in |c_K| because it points in the WRONG direction. Subsequent p²-terms (n=9,25,...) compound this.

For 37a1: wrong μ_E(4) = a_2²−2 = 4−2 = 2 vs correct = 2. **These are identical for p=2!**  
For p=3: wrong = (-3)²−3 = 6 vs correct = 3. Different sign direction but smaller relative impact.

The Δ correction is catastrophic because the first correction term n=4 has the WRONG SIGN.

### Results that are PRE-BUGFIX (need recomputation):

| File | Status |
|------|--------|
| koyama-shared/results/C1_500_ZEROS.md | **INVALIDATED** — E[C₁²](Δ) wrong by 3× |
| koyama-shared/results/C1_K50K_37A1_HEAVY.md | Needs recompute (~10% shift) |
| koyama-shared/results/C1_K50K_DELTA_HEAVY.md | **INVALIDATED** — wrong by ~2× |
| koyama-shared/results/C1_K50K_389A1_HEAVY.md | Needs recompute |
| koyama-shared/results/DELTA_0500_IDENTITY_HUNT.md | **INVALIDATED** — C₁=0.4964 is WRONG |
| experiments/C1_500_ZEROS.md | **INVALIDATED** |

### Results NOT affected:

| Item | Reason |
|------|--------|
| Zeta zeros spectroscope (c_K for ζ) | Uses ordinary μ(n) which IS correct (squarefree) |
| Dirichlet character χ computations | Need to check — same issue if using wrong p² formula |
| Zero locations (lfunzeros) | PARI-computed, unaffected |
| a_p verification | Cross-checks a_p values, unaffected |

---

## Codex Audit Additional Findings

**Codex flagged these — ASSESSED:**

1. **"Using ordinary μ for general L-functions"** — PARTIALLY CORRECT. We DO use form-specific coefficients. The issue is specifically at p² (using Hecke eigenvalue instead of inverse coefficient).

2. **"B_∞ diverges on Re(s)=1/2"** — INCORRECT (Codex error). At k=2: sum is Σ_p χ(p)²p^{-2ρ} with 2ρ=1+2iγ. For non-principal χ², L(1+2iγ,χ²) converges conditionally. For k≥3: Re(kρ)=k/2>1 → absolute convergence. B_∞ conjecture is fine.

3. **"Rank-2 zeros are ill-defined"** — INCORRECT for imaginary zeros. L'(ρ,E)≠0 at ρ=1/2+iγ for complex zeros of rank-2 curves (only the BSD zero at s=1 is double).

4. **"γ_E additive offset not analytically justified"** — VALID CONCERN. The (log K + γ_E) normalization is a convention. Full justification requires explicit residue computation.

5. **"Universality falsified is dimensionally wrong"** — CORRECT (original universality claim was ill-posed; we already knew and reported this).

---

## Action Required

1. ✅ Fix scripts (done — 4 files corrected)
2. ✅ Verified bug impact numerically (BUGFIX_FINAL_COMPARE.py)
3. ⏳ Recompute E[C₁²] at K=50K, N=500 zeros for 37a1, Δ, 389a1 with correct μ
4. ⏳ Recompute C₁(Δ,γ₁) at K=10^5 with correct μ — expect ~0.89, not 0.496
5. 🚫 **DO NOT SEND REPLY9 TO KOYAMA** — the quoted E[C₁²] values are wrong by factor 3×

---

## Note on Scientific Significance

Even with the bug, the STRUCTURE of the computation is sound:
- The "mu" array correctly handles the k=1 (squarefree) terms: μ_f(p) = −a_p ✓
- The k≥3 terms are set to zero ✓ (correct for degree-2 Euler factors)
- Only k=2 terms are wrong (using Hecke eigenvalue a_{p²} vs correct p^{k-1})

The C₁ statistic is STILL measuring a meaningful partial Dirichlet sum. The question is whether the corrected computation:
(a) Preserves the universality pattern (E[C₁²] matches for 37a1 vs Δ)
(b) Changes the E[C₁²] for rank-2 curves relative to rank-1
(c) Changes the C₁(Δ,γ₁)=0.4964 value significantly

These are empirical questions that require recomputation.
