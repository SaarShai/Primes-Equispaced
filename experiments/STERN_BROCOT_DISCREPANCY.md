# Stern-Brocot & Calkin-Wilf Per-Level Discrepancy

## Date: 2026-03-31
## Status: Computed to level 22 (~4M fractions). Fully analyzed.

---

## Setup

**Stern-Brocot tree** restricted to [0,1]: Start with {0/1, 1/1}. At each level, insert mediants between all consecutive fractions. Level n has 2^n new fractions; cumulative |S_n| = 2^n + 1.

**Calkin-Wilf tree** restricted to [0,1]: Root 1/1; left child of p/q is p/(p+q), right child is (p+q)/q. Keep only fractions in [0,1].

**Key fact verified**: The cumulative sets S_n are **identical** for SB and CW at every level (checked to level 11 with exact arithmetic, confirmed numerically to level 22). Both trees enumerate the same fractions at each cumulative depth.

**Discrepancy**: W(n) = (1/|S_n|^2) * Sum_{f in S_n} D(f)^2, where D(f) = rank(f) - |S_n|*f.

---

## Results

### 1. DeltaW_SB(n) does NOT oscillate

DeltaW_SB(n) is **monotonically positive** for n >= 4, growing geometrically:

| n | DeltaW_SB(n) | Ratio to previous |
|---|---|---|
| 1 | -0.1111 | -- |
| 2 | -0.0667 | 0.600 |
| 3 | -0.0180 | 0.269 |
| 4 | +0.0368 | -2.046 |
| 5 | +0.1135 | 3.087 |
| 6 | +0.2468 | 2.175 |
| 7 | +0.5027 | 2.037 |
| 8 | +1.009 | 2.007 |
| 10 | +4.038 | 2.000 |
| 15 | +129.2 | 2.000 |
| 20 | +4135 | 2.000 |
| 22 | +16540 | 2.000 |

**The ratio converges to exactly 2.** DeltaW_SB(n) ~ C * 2^n with C = 0.00394.

Sign pattern: `---+++++++++++++++++++` (1 sign change out of 21 possible).

### 2. No spectral structure

The periodogram of DeltaW_SB shows only the exponential growth mode. After normalizing out the 2^n factor:

DeltaW_SB(n) / 2^(n-1) converges to **0.00788677...**

The deviations from this limit decay smoothly (ratio ~0.4-0.5 per level), with no oscillatory component. **No connection to zeta zeros, Gauss map eigenvalues, or Selberg spectrum.**

### 3. The limiting constant is an integral of Minkowski's question mark function

W_SB(n) / |S_n| converges to:

**integral_0^1 (?(x) - x)^2 dx = 0.0078868...**

where ?(x) is Minkowski's question mark function. This was verified numerically to 7 digits.

**Explanation**: The SB tree samples [0,1] uniformly in ?-coordinates. Since rank(f)/N -> ?(f), we get D(f) ~ N*(?(f) - f), so W/N -> integral of (? - id)^2.

### 4. SB and CW are identical

Correlation between DeltaW_SB and DeltaW_CW: **1.000000 (exact identity)**

This follows because the cumulative sets S_n coincide: both trees produce the same set of rationals at each depth. The trees differ only in which fractions they assign to which level, but the cumulative union is identical.

### 5. Stark contrast with Farey

| Property | Stern-Brocot / Calkin-Wilf | Farey |
|---|---|---|
| DeltaW behavior | Monotone growth, ratio -> 2 | Oscillation with sign changes |
| Sign changes | 1 out of 21 | 44 out of 98 (N=2..100) |
| Spectral content | None (pure geometric) | Locked to zeta zeros |
| Growth | DeltaW ~ 2^n (exponential) | DeltaW ~ O(1/N) (bounded, decaying) |
| Governing function | Minkowski ?(x) | Riemann zeta / Mertens |
| Ordering principle | Tree depth (CF digit sum) | Arithmetic (denominator bound) |

---

## Interpretation

The absence of spectral structure in SB discrepancy **confirms that the zeta-zero oscillation in Farey DeltaW is a consequence of the arithmetic ordering**, not an intrinsic property of the rational numbers themselves. The same rationals, ordered by tree depth rather than denominator, produce qualitatively different discrepancy dynamics:

- **Farey (denominator ordering)**: The step-by-step inclusion of fractions with denominator exactly N introduces number-theoretic correlations (Euler totient, Mobius function) that encode zeta zeros in the oscillation of DeltaW.

- **Stern-Brocot (tree ordering)**: The mediant-based insertion has a purely geometric doubling structure. The discrepancy is governed by Minkowski's question mark function ?(x), which measures the distortion between the arithmetic and tree orderings. Since ?(x) is a singular function (derivative zero a.e.) with no connection to the zeta function, the SB discrepancy carries no spectral signature of zeta zeros.

**Bottom line**: The spectral content is in the ORDERING, not the FRACTIONS. This is strong evidence that our Farey per-step discrepancy probes genuinely arithmetic information.

---

## Connection to Project

This result strengthens the case for N1/N2 (Farey discrepancy <-> Mertens/zeta):
- It provides a **null test**: a control experiment where the same fractions, differently ordered, produce no spectral signal.
- It clarifies that the zeta connection is specifically about the arithmetic of denominators (Euler phi, Mobius), not about the geometric structure of rational approximation.

---

## Scripts
- `stern_brocot_discrepancy.py` — main computation (SB + CW to level 22)
- `stern_brocot_normalized.py` — normalization analysis, Farey comparison, constant identification
- `stern_brocot_data.json` — raw numerical data
