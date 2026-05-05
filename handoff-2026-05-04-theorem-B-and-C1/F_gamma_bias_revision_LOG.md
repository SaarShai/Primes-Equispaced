---
title: "F(γ) Bias-Claim Revision Audit Log"
date: 2026-05-03
revision_tag: "[REV: F(γ) bias 2026-05-03]"
authority: F_gamma_uniform_T_VERIFIED.md (conf 0.88)
---

# F(γ) Bias-Claim Revision — Audit & Diff Summary

## Correction Summary

**Stale claim (all files before revision):**
> |γ̂_ρ^{(X)} − γ_ρ| ≤ C₁/log X  uniformly in T

**Corrected claim (all files after revision):**
> - For **well-isolated** zeros (e.g. zero #1): bias envelope is O(1/log X) with monotone decay.
> - For **non-isolated** zeros in general: bias oscillates within that envelope due to X^{iγ_ρ}-phase factor; general bound is O(X^{−1/2} · log T).
> - Empirically: bias uniformly bounded by C(W) ≈ 0.1 (Gaussian W); |bias|·log X cycles in [0.03, 0.55] across 45 tested (k, X) pairs.

**Authority:** `F_gamma_uniform_T_VERIFIED.md` (conf 0.88), §3.1 numerical tables and §5 item 6.

---

## Files Audited

### 1. F_gamma_uniform_T_closure.md (conf 0.83)
**Status: EDITED**

Three locations revised:

**A. Bottom-line section (U) — lines ~21-26:**
- Old: "Bias |γ̂_ρ^{(X)} − γ_ρ| ≤ C/log X uniformly in T."
- New: Replaced with two-case statement (isolated vs non-isolated), O(X^{−1/2}·log T) general bound, C(W) ≈ 0.1 empirical cap, [REV] tag.

**B. Theorem 3.3(b) — line ~173:**
- Old: "|γ̂_ρ^{(X)} − γ_ρ| ≤ C₁/log X uniformly;"
- New: Multi-line corrected statement with envelope / oscillation distinction, empirical [0.03, 0.55] range, general O(X^{−1/2}·log T) bound, [REV] tag.

**C. §7 Paper B summary paragraph:**
- Old: "bias O(1/log X)"
- New: "bias bounded uniformly by C(W) ≈ 0.1 (envelope O(1/log X) for well-isolated zeros; O(X^{−1/2}·log T) generally due to X^{iγ_ρ} phase cycling)", [REV] tag.

---

### 2. Farey_F_gamma_local_z_monotonicity.md (conf 0.78)
**Status: EDITED**

Four locations revised:

**A. Bottom-line (B) statement:**
- Old: "finite-X bias |γ̂_ρ^{(X)} − γ_ρ| = O(1/log X)"
- New: "bias bounded uniformly by C(W) ≈ 0.1; envelope O(1/log X) for well-isolated zeros; oscillates within envelope due to X^{iγ_ρ}-phase interference; general O(X^{−1/2}·log T)"; [REV] tag.

**B. Step 2 finite-X argmax bias (§4), equation (9) prose:**
- Old: "consistent with the 1/log X scaling" (implying clean monotone scaling universally)
- New: Added [REV] block distinguishing the isolated-zero envelope from the oscillatory non-isolated case; explicit reference to `F_gamma_uniform_T_VERIFIED.md` 45-case verification; |bias|·log X ∈ [0.03, 0.55] range added.

**C. §7 Proven list:**
- Old: "Local strict monotonicity of F² around finite-X argmax γ̂_ρ^{(X)} with explicit bias O(1/log X)."
- New: "bias bounded uniformly by C(W) ≈ 0.1; envelope O(1/log X) for isolated zeros, O(X^{−1/2}·log T) generally"; [REV] tag.

**D. §8 Paper B section structure:**
- Old: "§X.4 Local argmax bias O(1/log X) — numerically sharp."
- New: Two-tier bias statement with [REV] tag.

---

### 3. F_gamma_uniform_T_VERIFIED.md (conf 0.88)
**Status: NO EDIT — this is the source-of-truth for the correction**

Already contains the corrected bias claim in §3.1 (the CORRECTED bias claim block) and §5 item 6. Not modified.

---

### 4. Smoothed_Dwf_publishable.md (conf 0.93)
**Status: NO EDIT — no F(γ) bias claim present**

This file covers the Δw_f explicit formula lemma (Theorem X.3.1). No reference to F(γ) argmax bias. Unaffected.

---

### 5. PAPER_DRAFT_TheoremB_WeightAspect.md
**Status: NO EDIT — no F(γ) bias claim present**

This file covers the L'(ρ_f, f) second moment (Theorems B-cage and B-exact). No F(γ) Spectroscope bias claim. Unaffected.

---

### 6. wiki/Research/Farey-Spectroscope-Unification-Open.md
**Status: NO EDIT — no F(γ) bias claim present**

This file covers the broader spectroscope unification questions (10-question checklist). No specific F(γ) bias bound stated. Unaffected.

---

## Mathematical Sanity Check

The correction is consistent with first principles:

- The dominant term near zero ρ₀ is X · |K_W(γ_ρ₀ − γ)|² · |1/ζ'(ρ₀)|² (magnitude X).
- The cross-zero interference near ρ₀ is O(X^{1/2} · log^{3/2} T) (from §3.2 of closure.md).
- The argmax shift is set by the ratio: cross / (X · |K_W''(0)|) = O(X^{−1/2} · log^{3/2} T / log X).
- For X = T^{1+ε}: this is O(T^{−(1+ε)/2} · log^{3/2} T / log T) → 0, confirming the bound decays.
- The oscillatory behavior arises because the cross-zero sum has phases e^{iγ_ρ log X} that are not summed over γ — they appear as a γ-independent complex number that rotates the argmax, so as X varies the argmax oscillates rather than monotonically converging.
- For zero #1 (most isolated, Δ ≈ 6.89), the cross term is exponentially small in Δ ≈ 6.89, so the envelope IS the monotone 1/log X term. This is unique to zero #1's exceptional isolation.

---

## Files Changed

| File | Locations edited | Summary |
|---|---|---|
| F_gamma_uniform_T_closure.md | 3 | Bottom-line (U), Theorem 3.3(b), §7 summary |
| Farey_F_gamma_local_z_monotonicity.md | 4 | Bottom-line (B), §4 Step 2, §7 proven list, §8 section structure |

Total: 7 edits across 2 files. All edits tagged [REV: F(γ) bias 2026-05-03].
