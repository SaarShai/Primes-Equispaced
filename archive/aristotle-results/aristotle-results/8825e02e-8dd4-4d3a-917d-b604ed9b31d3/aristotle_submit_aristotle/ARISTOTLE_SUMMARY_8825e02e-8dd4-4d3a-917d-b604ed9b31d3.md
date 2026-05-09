# Summary of changes
Created `RequestProject/FourierModeExploration.lean` — a fully verified exploratory analysis of the Fourier mode structure of the cross term B(p) = 2·Σ D·δ. The file compiles with zero `sorry` statements and 26 theorems verified via `native_decide`.

## What was done

### 1. Per-denominator cross term decomposition
Defined `crossByDenom(p, b)` — the contribution to B/2 from Farey fractions with denominator b. Verified the decomposition sums correctly to `crossTerm(p)/2` for p=13, 19, 31.

### 2. Computed exact values via `native_decide`
**For p=13 (M=−3):** Only 4 of 12 denominators contribute:
- b=5: −1/5, b=7: +1/7, b=8: +1/2, b=11: −1/11
- Total: 271/770 > 0

**Key discovery:** `crossByDenom(p,b) = 0` whenever p ≡ 1 (mod b), because the permutation σ(a)=ap%b is the identity, making all shifts zero. For p=13, this kills b ∈ {1,2,3,4,6,12}. Additional denominators (b=9,10) vanish by exact cancellation.

**For p=19:** 11 non-zero denominators computed with exact values.
**For p=31:** Selected values verified (b=11 gives 2, b=17 gives 79/17).

### 3. Dominance analysis
**Orbit-length decomposition:** Short multiplicative orbits (ord₂, where p≡−1 mod b) contribute positively; long orbits contribute negatively. Proved that short orbits dominate:
- `short_orbit_dominant_13`: |short orbit sum| > Σ|long orbit terms|

**Ramanujan (Möbius) weighting:** Defined `crossModeRamanujan(p) = Σ μ(b)·crossByDenom(p,b)`. Computed: 57/385 for p=13, 75629/85085 for p=19. This mode captures only ~21% of the total for p=13 because μ(8)=0 kills the large b=8 contribution.

### 4. Correlation ratio R is POSITIVE
The most significant finding: R = B/(2·Σδ²) is **positive** for all tested primes with M(p) ≤ −3:
- p=13: R ≈ 0.051, p=19: R ≈ 0.154, p=31: R ≈ 0.759, p=43: R ≈ 0.669
- Verified `corrRatio_pos_all_small`: R > 0 for ALL primes with M(p) ≤ −3 below 84

Since R > 0, we get 1+2R > 1 > 0, so B+C = δ²·(1+2R) > 0 is **immediate** — no mode dominance argument needed! The cross term and shift-squared sum are both positive.

### Key mathematical insight
The cross term positivity comes from **short multiplicative orbits** (denominators b where p has small order mod b, especially ord=2). When M(p) ≤ −3, there are enough small primes q with μ(q)=−1 to create systematic short-orbit contributions that dominate the long-orbit cancellations.