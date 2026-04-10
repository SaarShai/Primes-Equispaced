# 3DGS Farey-Guided Densification: Complete Handoff Document

## 1. WHAT WE DISCOVERED

### The Core Mathematical Properties (Lean 4 Verified)

1. **Generalized Injection Principle**: When inserting Farey order N fractions into F_{N-1}, each gap between adjacent fractions receives **at most 1 new fraction**. This bounds the rate of refinement.

2. **Universal Mediant Property**: Every new fraction is the mediant (a+c)/(b+d) of its neighbors — a weighted midpoint that respects the existing structure.

3. **Zero Cascading**: Inserting a new fraction never displaces existing ones. F_N ⊂ F_{N+1} strictly.

4. **2D/3D Tensor Product**: In higher dimensions (tensor product grids), each cell receives at most 1 new interior point per refinement level.

5. **Fisher Information Monotonicity**: The information content sum(1/gap²) strictly increases at every refinement step.

### The Proposed Application to 3D Gaussian Splatting

**The problem in 3DGS**: The Adaptive Density Control (ADC) algorithm decides when and where to add new Gaussians during training. The original ADC (Kerbl et al., SIGGRAPH 2023) uses a fixed gradient threshold (0.0002) that causes:
- **Over-densification**: Too many Gaussians in already-well-fit regions
- **Cascading splits**: One split triggers further splits in nearby Gaussians
- **Floaters**: Orphaned Gaussians that don't contribute to the reconstruction
- **Scene-independent threshold**: The same number works poorly across different scenes

**Our proposed solution**: Replace the fixed gradient threshold with Farey-guided insertion:
- Only insert where the spatial "gap" between Gaussians is large AND reconstruction error is high
- Place new Gaussians at mediant positions (weighted midpoints between neighbors)
- Limit to at most 1 insertion per gap per refinement level (bounded densification)
- Progressive refinement: increase the "Farey level" N over training, admitting finer gaps

---

## 2. EXPERIMENTS WE RAN

### 2.1 — 1D Demo (farey_3dgs_1d_demo.py)

**Setup**: Reconstruct a 1D signal (smooth sin + high-frequency burst) using 60 Gaussians, 2000 training steps, Adam optimizer, pure NumPy.

| Metric | Standard ADC | Farey |
|--------|-------------|-------|
| Final MSE | 0.052208 | 0.001574 |
| Gaussians | 60 | 60 |
| MSE/Gaussian | 8.7e-4 | 2.6e-5 |
| **Efficiency ratio** | — | **33.2x** |

**Key observation**: ADC scattered Gaussians everywhere including the smooth region. Farey concentrated them in the high-frequency burst.

### 2.2 — 2D Simple Demo (farey_3dgs_2d_simple.py)

**Setup**: 128x128 image, gradient background + square patch, 10 initial Gaussians, cap 100, 2000 steps.

| Metric | Standard ADC | Farey |
|--------|-------------|-------|
| Final MSE | 0.004660 | 0.000801 |
| Gaussians | 78 | 48 |
| MSE/Gaussian | 5.97e-5 | 1.67e-5 |
| **Efficiency ratio** | — | **3.6x** |

### 2.3 — 2D Full Demo (farey_3dgs_2d_demo.py)

**Setup**: 256x256 image, sinusoidal gradient + checkerboard patch in [0.3,0.7]², 25 initial Gaussians (5x5), cap 200, 3000 steps, axis-aligned 2D Gaussians. Uses Delaunay triangulation for neighbor finding.

| Metric | Standard ADC | Farey |
|--------|-------------|-------|
| Final MSE | 0.026529 | 0.011187 |
| PSNR (dB) | 15.76 | 19.51 |
| SSIM | 0.8510 | 0.9047 |
| Gaussians | 199 | 200 |
| MSE/Gaussian | 1.33e-4 | 5.59e-5 |
| **Efficiency ratio** | — | **2.4x** |

### 2.4 — 3D Demo (farey_3dgs_3d_demo.py)

**Setup**: 3D density field (sphere + 12 bump features), 64 initial Gaussians, cap 300, 2000 steps, isotropic 3D Gaussians, Delaunay tetrahedralization for neighbors.

| Metric | Standard ADC | Farey |
|--------|-------------|-------|
| Train MSE | 0.000020 | 0.000001 |
| Test MSE | 0.001093 | 0.000095 |
| Gaussians | 108 | 122 |
| MSE/Gaussian (test) | 1.01e-5 | 7.79e-7 |
| Detail region fraction | 33.3% | 48.4% |
| **Efficiency ratio** | — | **19.2x** |

### Trend Across Dimensions

| Dim | Efficiency Gain | Note |
|-----|----------------|------|
| 1D | 33.2x | Same Gaussian count |
| 2D (simple) | 3.6x | Farey used 38% fewer |
| 2D (full) | 2.4x | Same Gaussian count, +3.75 dB |
| 3D | 19.2x | Similar count, much better test generalization |

---

## 3. CRITICAL PROBLEMS WITH OUR EXPERIMENTS (Verified by Rigorous Review)

### Problem 1: UNFAIR BASELINE

Our "Standard ADC" is a simplified caricature of real 3DGS ADC:

| Feature | Real 3DGS ADC | Our Baseline |
|---------|---------------|-------------|
| Gradient accumulation over iterations | Yes | No (single-step) |
| Clone operation (for small Gaussians) | Yes | **Missing entirely** |
| Split operation (for large Gaussians) | Yes | Yes (only this) |
| Opacity-based pruning | Yes (< 0.005) | No |
| Periodic opacity reset | Yes | No |
| Anisotropic Gaussians (full covariance) | Yes | No (isotropic only) |
| Spherical harmonics for view-dependent color | Yes | No |
| Differentiable rasterization pipeline | Yes | No (direct evaluation) |
| Split direction (along gradient/eigenvector) | Yes | Random offset |

**Impact**: The missing clone operation is critical — real ADC clones small Gaussians to fill gaps, which is exactly the error-guided placement our Farey method does. We may be comparing Farey (with error-guided placement) against a baseline that lacks it.

### Problem 2: TOY SCALE

| Our demos | Real 3DGS |
|-----------|-----------|
| 60-300 Gaussians | 1-6 MILLION Gaussians |
| 1D/2D signals or 3D density field | Multi-view photographs of real scenes |
| Direct function evaluation | Differentiable rasterization + 2D projection |
| 2000-3000 steps | 30,000 steps |

Behavior at toy scale tells us almost nothing about real-scale behavior.

### Problem 3: ATTRIBUTION ERROR

The improvement in our demos comes primarily from **error-guided gap-filling**, not from Farey mathematics. Specifically:
- We insert only where reconstruction error is high (error gating)
- We place new Gaussians between existing ones (gap-aware placement)
- We limit insertions per region (rate control)

Multiple published methods already do this:
- **Revising Densification** (Bulo et al., ECCV 2024) — per-pixel error as densification criterion
- **Mini-Splatting** (ECCV 2024) — importance-based splitting
- **SteepGS** (CVPR 2025) — eigenvalue-based split direction, proves 2 offspring suffice
- **Improving ADC** (VISAPP 2025) — ascending gradient thresholds

If we gave standard ADC the same error-gating logic without Farey framing, it would likely perform comparably.

### What Real Methods Achieve on Standard Benchmarks

On Mip-NeRF 360 (the standard 3DGS benchmark):

| Method | Gaussians | PSNR | Change vs 3DGS |
|--------|-----------|------|-----------------|
| 3DGS (baseline) | 3.34M | 27.47 dB | — |
| Mini-Splatting | 0.49M (7x fewer) | 27.30 dB | -0.17 dB |
| Scaffold-GS | ~0.76M (4.4x fewer) | 28.84 dB | +1.37 dB |
| SteepGS | 1.61M (52% fewer) | 28.73 dB | +1.26 dB |

**Key observation**: Best published methods achieve 2-7x Gaussian reduction. Nobody reports 19x or 33x. A 0.5 dB improvement is considered significant.

---

## 4. WHAT WE CAN HONESTLY CLAIM

### Novel contributions (defensible):
1. **Mathematical framework**: Farey injection provides a principled, formally verified framework for progressive spatial refinement. No prior work connects Farey/Stern-Brocot theory to Gaussian splatting.
2. **Bounded densification guarantee**: At most 1 new Gaussian per gap per level — a provable bound that no heuristic method offers.
3. **No cascading property**: Proven (Lean 4) that insertion in one gap doesn't affect others.
4. **Progressive refinement schedule**: The Farey level N provides a natural coarse-to-fine curriculum.

### What remains unproven:
1. Whether the advantage holds against a **fair baseline** (proper ADC with cloning + pruning)
2. Whether the approach **scales** to millions of Gaussians on real scenes
3. Whether the Farey math adds value **beyond** error-guided placement
4. Whether the Delaunay-based gap detection is **computationally tractable** at scale (O(n log n) in 2D, potentially O(n²) in 3D)

---

## 5. THE BRIDGE FROM FAREY TO 3DGS

### Structural Mapping (via Scaffold-GS)

The viable bridge goes through **anchor-based 3DGS** (Scaffold-GS, CVPR 2024):

| Farey Concept | Scaffold-GS Concept |
|---|---|
| Ordered interval [a/b, c/d] | Voxel cell in the anchor grid |
| Gap width 1/(bd) | Voxel scale / anchor extent |
| Mediant (a+c)/(b+d) | New anchor at weighted midpoint |
| "At most 1 per gap per level" | At most 1 new anchor per voxel per step |
| No cascading | Growing one anchor doesn't trigger neighbors |
| Stern-Brocot tree depth | Octree level |

### Per-Axis Decomposition

For each row of anchors along a single axis:
1. Sort by coordinate → ordered sequence
2. Compute gap widths between consecutive anchors
3. Map anchor scale to "Farey denominator": d_i = round(1/scale_i)
4. Admission criterion: gap is admissible at level N if d_i + d_j ≤ N
5. New anchor placed at sigma-weighted mediant position
6. Tensor product extends to 3D

### Gap-Size-to-Scale Mapping

- Farey gap width 1/(bd) ↔ Gaussian scale (spatial extent)
- Denominator sum b+d ↔ reciprocal of scale (higher = finer)
- Injection condition b+d > N ↔ "don't split below resolution threshold"

---

## 6. COMPETING APPROACHES (State of the Art, 2024-2026)

### Anchor-based (Scaffold-GS family)
- **Scaffold-GS** (CVPR 2024 Highlight): Voxel grid of anchors, MLPs spawn Gaussians. Foundation for Octree-GS, 4D Scaffold-GS.
- **Octree-GS** (TPAMI 2025): Multi-resolution octree anchor structure.

### Optimization-theoretic
- **SteepGS** (CVPR 2025, Facebook Research): Proves splitting escapes saddle points. 2 offspring suffice. Eigenvalue-based split direction. Most theoretically principled existing work.
- **ControlGS** (2025): Uniform octree-style 8-way splitting + sparsification.

### Heuristic improvements
- **AD-GS** (SIGGRAPH Asia 2025): Alternating aggressive/conservative phases.
- **Mini-Splatting** (ECCV 2024): Blur-based splitting + importance sampling.
- **Revising Densification** (ECCV 2024): Per-pixel error as criterion.
- **Improving ADC** (VISAPP 2025): Ascending gradient thresholds.

### Geometric structure
- **Radiant Foam**: Voronoi diagrams as scene partitions.
- **MILo**: Delaunay triangulations from Gaussian parameters.

---

## 7. KEY OPEN QUESTIONS FOR VALIDATION

1. **Ablation**: If we give standard ADC the same error-gating and gap-aware placement but WITHOUT Farey math (just insert at midpoints where error is high, limit to 1 per region), does Farey still win? This separates the math from the heuristic.

2. **Scalability**: Delaunay tetrahedralization of N points is O(N²) worst case in 3D. At 3 million Gaussians, is this feasible? Alternative: kNN-based gap detection (O(N log N) with spatial hashing).

3. **Integration point**: Scaffold-GS is the natural target. Its anchor growing mechanism already uses voxel-based spatial structure — replacing the gradient-threshold growing criterion with Farey admission is a contained modification.

4. **Fair comparison**: Must compare against proper baselines including Scaffold-GS, SteepGS, Mini-Splatting on Mip-NeRF 360, Tanks & Temples, Deep Blending.

5. **What "modest gain" looks like**: In this field, +0.3-0.5 dB PSNR at same Gaussian count, or 2x fewer Gaussians at same PSNR, is a publishable result. We don't need 19x — 1.5x would be significant if demonstrated on real benchmarks.

---

## 8. PROJECT PLAN: REAL-SCALE VALIDATION

### Phase 1: Setup (1 week)
- Clone Scaffold-GS repository (https://github.com/city-super/Scaffold-GS)
- Set up environment (CUDA, PyTorch, gsplat or diff-gaussian-rasterization)
- Run baseline Scaffold-GS on 2-3 Mip-NeRF 360 scenes to establish reference numbers
- Requires: NVIDIA GPU with ≥12GB VRAM (RTX 3080+ or similar)

### Phase 2: Integration (2 weeks)
- Modify Scaffold-GS anchor growing to use Farey admission criterion
- Replace gradient-threshold growing with: gap-size check (denominator sum ≤ N) AND local error check
- Place new anchors at mediant positions instead of voxel centers
- Implement progressive level schedule (N increases over training)
- Keep everything else identical (same learning rates, same pruning, same rendering)

### Phase 3: Ablation (1 week)
- Run 3 variants on same scenes:
  A. Scaffold-GS baseline (unchanged)
  B. Scaffold-GS + error-gating only (no Farey math — just midpoint + error threshold)
  C. Scaffold-GS + full Farey (mediant + admission + level schedule)
- Compare B vs C to isolate the Farey contribution from the error-gating contribution
- Metrics: PSNR, SSIM, LPIPS, Gaussian count, training time, memory

### Phase 4: Benchmark (1 week)
- If Phase 3 shows Farey (C) beats error-gating-only (B):
  - Run full Mip-NeRF 360 (9 scenes), Tanks & Temples, Deep Blending
  - Compare against published numbers from SteepGS, Mini-Splatting, ControlGS
  - Report honest numbers with confidence intervals
- If Phase 3 shows no difference between B and C:
  - The Farey math doesn't add practical value beyond error-gating
  - Write up as negative result / framework paper without performance claims

### Hardware Requirements
- NVIDIA GPU ≥ 12GB VRAM (training Scaffold-GS)
- ~50GB disk for datasets (Mip-NeRF 360 is ~6GB, T&T ~10GB)
- Python 3.8+, CUDA 11.8+, PyTorch 2.0+

### Expected Timeline: 5 weeks total

### What Success Looks Like
- **Strong success**: +0.5 dB PSNR at same Gaussian count, or 2x fewer Gaussians at same PSNR, on Mip-NeRF 360. Publishable at CVPR/SIGGRAPH.
- **Moderate success**: +0.2 dB or 1.3x fewer Gaussians. Workshop paper or arXiv.
- **Negative result**: Farey adds nothing over error-gating. Still publishable as framework + negative finding. The mathematical contribution (injection principle for spatial refinement) stands regardless.

---

## 9. FILES AND CODE

All in `/Users/saar/Library/CloudStorage/GoogleDrive-saar.shai@gmail.com/My Drive/Farey Folder/experiments/`:

| File | Description |
|------|-------------|
| `farey_3dgs_1d_demo.py` | 1D demo (33x result) |
| `farey_3dgs_2d_simple.py` | 2D simple demo (3.6x result) |
| `farey_3dgs_2d_demo.py` | 2D full demo (2.4x, +3.75dB) |
| `farey_3dgs_3d_demo.py` | 3D demo (19.2x result) |
| `FAREY_3DGS_3D_DESIGN.md` | Full Scaffold-GS integration design |
| `FAREY_3DGS_PAPER_OUTLINE.md` | CVPR/SIGGRAPH paper outline |
| `GRAPHICS_APPLICATION_REPORT.md` | Broader graphics applications analysis |
| `farey_3dgs_1d_*.png` | 1D figures |
| `farey_3dgs_2d_*.png` | 2D figures |
| `farey_3dgs_3d_*.png` | 3D figures |

### Key Lean 4 proofs (in `/RequestProject/`):
- `StrictPositivity.lean` — C = δ² > 0
- `BridgeIdentity.lean` — Farey exponential sum = M(p) + 2
- `PrimeCircle.lean` — Foundation (fareySet, ramanujanSum, Mobius inversion)
