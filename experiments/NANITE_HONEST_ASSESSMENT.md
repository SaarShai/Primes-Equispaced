# Honest Assessment: Farey LOD vs Real-World Mesh LOD

**Date:** 2026-04-07
**Script:** `experiments/nanite_honest_assessment.py`
**Status:** COMPLETE — verdict is unfavorable for Farey LOD

---

## Setup

- **Terrain:** 64x64 grid heightmap (4225 vertices, 8192 triangles)
- **Height function:** 5-octave sin-based pseudo-terrain on [0,1]^2
- **Target:** 50% vertex reduction (~2112 vertices)
- **Also tested:** 60x60 (non-power-of-2) and 30x30 (highly composite)

## Results: 64x64 Grid (Standard Game Terrain Tile)

| Metric | Uniform | Cluster (Nanite) | Farey <=32 | Farey <=64 |
|---|---|---|---|---|
| Vertices kept | 2241 | 2689 | 1089 | 4225 |
| % of original | 53.0% | 63.6% | 25.8% | 100.0% |
| Overhead vs 50% | 6.1% | 27.3% | -48.4% | +100.0% |
| T-junctions | 3968 | 3072 | 2112 | 0 |
| Max geo error | 0.120 | 0.120 | 0.908 | 0.000 |
| High-curv kept | 49.6% | 60.3% | 24.1% | 100% |

**Farey CANNOT hit 50% on a 64x64 grid.** The denominator levels are {1, 2, 4, 8, 16, 32, 64}. Level 32 gives 25.8%. Level 64 gives 100%. There is a 74.2% gap with no intermediate option.

## Results: 60x60 Grid (Farey-Friendly)

| Metric | Uniform | Cluster | Farey <=20 | Farey <=30 |
|---|---|---|---|---|
| Vertices kept | 1981 | 2194 | 1369 | 2025 |
| % of original | 53.2% | 59.0% | 36.8% | 54.4% |
| Overhead vs 50% | 6.5% | 18.0% | -26.4% | +8.9% |
| T-junctions | 3480 | 2352 | 888 | 1440 |
| Max geo error | 0.144 | 0.719 | 0.806 | 0.806 |

Better granularity on non-power-of-2 grids. Farey <=30 hits 54.4% with only 8.9% overhead. But: **1440 T-junctions** and **5x worse geometric error** than uniform.

## Results: 30x30 Grid (Best Case for Farey: 30 = 2*3*5)

| Metric | Uniform | Cluster | Farey <=10 | Farey <=15 |
|---|---|---|---|---|
| Vertices kept | 541 | 470 | 225 | 529 |
| % of original | 56.3% | 48.9% | 23.4% | 55.0% |
| Overhead vs 50% | 12.7% | -2.1% | -53.1% | +10.2% |
| T-junctions | 840 | 432 | 120 | 368 |

Even on a highly-composite grid, Farey levels are too coarse (23.4% or 55.0%).

---

## Five Fundamental Problems

### 1. Granularity Problem
On power-of-2 grids (the industry standard), Farey levels are powers of 2. You get {1, 2, 4, 8, 16, 32, 64} — that's 7 LOD levels, but the jumps between them are enormous. Level 32 has 25.8% of vertices; level 64 has 100%. There is no way to get 50%, 40%, 60%, 70%, or 80%. On non-power-of-2 grids you get more levels, but still coarse.

### 2. Geometry-Blind
Farey selects vertices by denominator (a number-theoretic property), not by terrain curvature. On the 64x64 grid at level <=32, Farey keeps only 24.1% of high-curvature vertices — worse than the 49.6% that random checkerboard achieves. Farey preferentially keeps vertices where fractions simplify, regardless of terrain shape.

### 3. 2D Crack-Free is Broken
The Stern-Brocot mediant property guarantees crack-free 1D nesting. In 2D, Farey levels produce T-junctions at every tested level on every tested grid size. The 2D nesting structure is not simply the product of two 1D Stern-Brocot trees.

### 4. Cluster Overhead is NOT 126%
On the real 64x64 grid with 8x8 clusters, overhead is 27.3% — not 126%. The earlier 126% figure came from a contrived 2D segment test with unfavorable border-to-interior ratio. Real grids share border vertices between adjacent clusters, dramatically reducing overhead.

### 5. Farey is the Wrong Optimization Target
Real LOD systems (Nanite, ROAM, progressive meshes) use geometric error to decide what to remove. Farey uses arithmetic. A vertex at coordinates (1/3, 1/5) has denominator 5 and is kept early; a vertex at (17/64, 33/64) has denominator 64 and is dropped — regardless of whether it's on a cliff or a flat plain.

---

## The 126% Revisited

The earlier test used a 1D chain of clusters where every cluster border was unique. On a 2D grid, border vertices are shared between 2 or 4 clusters. This sharing reduces effective overhead from 126% to 27%. Our earlier result was technically correct but practically misleading.

## What Farey LOD IS Good For

1. **Theoretical interest**: The nested hierarchy has beautiful number-theoretic structure
2. **1D parametric curves**: The Stern-Brocot crack-free property works in 1D
3. **Visualization of number theory**: Showing Farey sequences on meshes
4. **Possible hybrid**: Farey nesting as scaffold + geometry-weighted selection within each level (unexplored, might rescue the idea)

## What It Is NOT Good For

1. Terrain LOD (geometry-blind, coarse levels)
2. Game mesh LOD (power-of-2 grids are catastrophic)
3. Replacing Nanite/cluster-based approaches (which are geometry-aware)
4. Any application where visual quality matters more than arithmetic elegance

---

## Verdict

**Were we fooling ourselves?** Partially yes.

- The 126% cluster overhead was real on the toy test but misleading for real grids (actual: 27%)
- Farey LOD has a fatal granularity problem on power-of-2 grids
- Farey LOD is geometry-blind — it keeps the wrong vertices for terrain
- Farey LOD produces T-junctions in 2D (the crack-free property is 1D only)
- The mathematical elegance is real; the practical utility is not

**Score card:**
- Nanite (cluster): **B+** — real, shipped, works, moderate overhead
- Uniform decimation: **C** — simple but cracks everywhere
- Farey LOD: **D** — elegant math, wrong tool for mesh LOD

**Recommendation:** Do not pursue Farey LOD as a mesh decimation method. If anything, explore a hybrid where Farey provides the nesting structure but vertex selection within each level is weighted by geometric error. Even then, the granularity problem on power-of-2 grids may be fatal.
