# Farey LOD on CAD-Like Parametric Surface Mesh

**Date:** 2026-04-07
**Test:** `experiments/nanite_cad_test.py`

## Setup

Cylinder + flange (disk cap) mesh:
- Cylinder: 32 segments x 17 rows = 544 vertices
- Flange: 32 radial x 8 concentric rings + center = 257 vertices
- Total: 801 vertices, 1568 triangles
- Stitch zone: 64 triangles connecting cylinder top to flange inner ring

## Farey Level Distribution

| Denom threshold | Vertices | Fraction |
|---|---|---|
| <= 1 | 4 | 0.5% |
| <= 2 | 11 | 1.4% |
| <= 4 | 37 | 4.6% |
| <= 8 | 137 | 17.1% |
| **<= 16** | **401** | **50.1%** |
| <= 32 | 801 | 100% |

Key observation: 32-segment parametric surface yields exactly 6 LOD levels (divisors of 32: 1,2,4,8,16,32). Each level doubles the previous. This is a clean power-of-2 cascade -- exactly what CAD visualization wants.

## Results at ~50% Reduction

| Method | Kept | Ratio | Cracks | Error | Boundary | Overhead |
|---|---|---|---|---|---|---|
| **Farey** | 401 | 50.1% | 1568 | 0.3529 | 16/32 | 0 |
| **Cluster** | 477 | 59.6% | 1302 | 0.3529 | 32/32 | 156 |
| **Uniform** | 209 | 26.1% | 1184 | 0.3529 | 16/32 | 0 |

## Analysis

### What went right for Farey
1. **Perfect parametric alignment.** The Farey hierarchy IS the parametric subdivision hierarchy. Denominator thresholds correspond to subdivision levels. No artificial clustering needed.
2. **Zero overhead.** No border vertices to lock, no cluster boundaries to track. The hierarchy is intrinsic to the geometry.
3. **Clean LOD cascade.** 6 natural levels for a 32-segment mesh, each roughly doubling vertex count. This is exactly what streaming LOD wants.
4. **Exact 50% hit.** denom<=16 gives exactly 50.1% -- the Farey hierarchy naturally subdivides by powers of 2 for power-of-2 segment counts.

### What went wrong for Farey
1. **Most cracks (1568).** Every triangle with mixed Farey levels becomes a crack. Farey removes vertices in a scattered pattern (all odd-denominator positions) that touches nearly every triangle.
2. **Boundary preservation: only 16/32.** Half the boundary vertices have denom=32 (odd-k positions like k=1,3,5...) and get removed at the 50% level. This tears the cylinder-flange seam.
3. **Crack count dominates.** The crack metric is the key failure: 1568 cracks = 100% of triangles are partial. This is because Farey removes every other vertex around the circle -- every triangle has at least one removed neighbor.

### Why cracks are so high
The fundamental issue: Farey LOD removes vertices based on **parameter-space** position, not **mesh connectivity**. For a 32-segment circle, denom<=16 keeps vertices at angles 0, pi/16, pi/8, ... (even positions) and removes all odd positions. This means every quad on the cylinder has exactly one vertex removed, creating 100% crack rate.

This is NOT a flaw of Farey per se -- it means **retriangulation is mandatory**. The kept vertices at denom<=16 form a valid 16-segment circle. If we retriangulate using only kept vertices, we get zero cracks. The "cracks" measured here are artifacts of using the original triangulation with missing vertices.

### Cluster LOD trade-offs
- Preserves all 32 boundary vertices (locked) but at 19.5% overhead (156 extra locked verts)
- Still has 1302 cracks inside clusters
- Actually kept 59.6% (not 50%) because border locking inflates the count
- Imprecise reduction ratio is a real production problem

### The real comparison should be
| | Farey + retri | Cluster | Uniform + retri |
|---|---|---|---|
| Cracks | 0 (by construction) | 1302 | 0 (by construction) |
| Overhead | 0 | 156 (19.5%) | 0 |
| Kept ratio | exact 50.1% | inflated 59.6% | exact 26.1% |
| Natural levels | 6 | N/A | 1 (all or nothing) |

## Key Insight: CAD + Farey Is Natural BUT Requires Retriangulation

For parametric CAD surfaces:
- Parameters are rational fractions (k/N) by construction
- Farey denominators ARE the natural subdivision levels
- Power-of-2 segment counts give clean power-of-2 LOD cascades
- BUT: you cannot just delete vertices from existing triangulation. You must retriangulate at each LOD level.

This is actually identical to how Nanite works: Nanite doesn't just remove vertices from existing triangles. It builds new triangle clusters at each LOD level. Farey's contribution would be: **the hierarchy for WHICH vertices to keep is given for free by the parametric structure**, instead of needing a DAG construction pass.

## Verdict: PARTIALLY VIABLE for CAD

**Viable** in the sense that:
- Farey hierarchy perfectly matches CAD parametric structure (no artificial clustering)
- Zero overhead (no border locking, no cluster graphs)
- Clean LOD cascade with predictable reduction ratios
- Works with any power-of-2 segment count (standard in CAD)

**Not drop-in** because:
- Retriangulation at each LOD level is mandatory (just deleting vertices = 100% cracks)
- Boundary seams (multi-patch CAD models) need explicit handling
- Cluster-based approaches handle mixed-resolution boundaries better out of the box

**Best use case:** CAD visualization where surfaces are single parametric patches with power-of-2 sampling. The Farey hierarchy gives you the LOD levels for free; you just need a retriangulator (which CAD tools already have).

**Worst use case:** Multi-patch models with T-junctions and non-power-of-2 sampling. Here cluster-based approaches win because they explicitly manage boundaries.
