# Farey-Structured Densification for 3D Gaussian Splatting

## Paper Outline — Target: CVPR 2026 or SIGGRAPH 2026

---

## Title

**Farey-Structured Densification for 3D Gaussian Splatting**

Alternative: *Mediant Injection: Number-Theoretic Densification Control for Gaussian Splatting*

---

## Abstract (Draft)

3D Gaussian Splatting (3DGS) achieves real-time novel view synthesis by optimizing
a collection of 3D Gaussians, but its Adaptive Density Control (ADC) mechanism
relies on gradient magnitude thresholds that are scene-dependent, often producing
redundant Gaussians in smooth regions and under-sampling fine detail. We introduce
Farey-structured densification, a principled replacement for ADC that uses the
geometric structure of Farey sequences to control when and where new Gaussians are
created. Our method constructs a Delaunay triangulation (2D) or tetrahedralization
(3D) of existing Gaussian centers, identifies under-resolved spatial gaps via a
scale-normalized distance metric, and injects at most one new Gaussian per gap per
refinement level — the Farey injection principle. This structural guarantee prevents
exponential growth while ensuring progressive coverage from coarse to fine.

On simplified benchmarks, Farey-guided densification achieves 33x better efficiency
per Gaussian in 1D, 2.4x in 2D (with +3.75 dB PSNR improvement), and [TBD]x in
3D density reconstruction. We integrate our approach with Scaffold-GS and evaluate
on standard benchmarks (Mip-NeRF 360, Tanks and Temples), demonstrating [TBD]
reduction in Gaussian count at comparable or improved visual quality.

---

## 1. Introduction

- 3DGS is fast but wasteful: ADC grows Gaussians based on gradient thresholds,
  leading to over-densification in smooth regions
- Existing fixes (ControlGS, SteepGS, AD-GS) adjust thresholds or add regularizers
  but remain fundamentally gradient-based
- We propose a structural approach inspired by Farey sequences from number theory:
  - Farey sequences enumerate all fractions p/q with q <= N, ordered on [0,1]
  - The "mediant" (p1+p2)/(q1+q2) of adjacent fractions fills gaps progressively
  - This gives a mathematically principled rule for where to insert new elements
- Key insight: the Farey mediant insertion rule generalizes to any dimension via
  Delaunay triangulation, which provides the natural notion of "adjacent" elements

**Contributions:**
1. A new densification criterion based on scale-normalized gap analysis in the
   Delaunay graph of Gaussian centers
2. The Farey injection principle: at most one Gaussian per spatial gap per
   refinement level, with provable growth bounds
3. Validated in 1D (33x), 2D (2.4x), 3D (pending) simplified benchmarks
4. Integration with Scaffold-GS demonstrating [TBD] on real scenes

## 2. Related Work

### 2.1 3D Gaussian Splatting
- Kerbl et al. (2023): Original 3DGS with ADC
- Key limitation: gradient threshold is a global hyperparameter that doesn't adapt
  to local scene complexity

### 2.2 Improved Densification for 3DGS
- **ControlGS** (Zheng et al., 2024): Score-based growth with spatial control
- **SteepGS** (Han et al., 2024): Steepest descent direction for split/clone decisions
- **AD-GS** (Ye et al., 2024): Anchor-based densification with adaptive thresholds
- **Scaffold-GS** (Lu et al., 2024): Voxel anchor hierarchy with neural Gaussians
- **Mini-Splatting** (Fang & Wang, 2024): Densification-aware sampling
- **GaussianPro** (Cheng et al., 2024): Progressive propagation for under-reconstructed regions
- All above use gradient-based or heuristic triggers; ours uses structural gap analysis

### 2.3 Number Theory in Signal Processing
- Farey sequences and Ford circles in sampling theory
- Stern-Brocot trees and mediant operations
- Connection to continued fractions and best rational approximations
- Our contribution: first application of Farey structure to learned 3D representations

## 3. Method

### 3.1 Preliminaries: Farey Sequences and Mediant Insertion
- Definition of Farey sequence F_N
- The mediant property: between adjacent a/b, c/d in F_N, the mediant (a+c)/(b+d)
  is the unique fraction with smallest denominator that falls between them
- Progressive refinement: F_1 -> F_2 -> ... covers [0,1] with provable gap bounds

### 3.2 From 1D to 3D: The Delaunay Bridge
- In 1D: adjacent Gaussians are left/right neighbors (sorted order)
- In 2D: adjacent Gaussians form Delaunay triangulation edges
- In 3D: adjacent Gaussians form Delaunay tetrahedralization edges
- This is the natural generalization: Delaunay edges connect "spatially adjacent"
  elements in any dimension

### 3.3 Gap Metric and Farey Admissibility
- For Delaunay edge (i,j):
  - d_edge = ||p_i - p_j|| / (r_i + r_j) where r is the effective radius
  - This counts "how many radii fit in the gap"
- Farey level N admits gaps with 1 < d_edge <= N
- Progressive schedule: N increases each densification round

### 3.4 Mediant Injection Rule
- Position: sigma-weighted interpolation p_new = p_i + t*(p_j - p_i), t = r_i/(r_i+r_j)
- Scale: r_new = alpha * (r_i + r_j), alpha < 0.5
- Error gate: only inject where local reconstruction error exceeds threshold
- At most one injection per edge per round (structural guarantee)

### 3.5 Integration with Scaffold-GS
- Replace gradient-threshold growing with Farey gap analysis
- Anchor features initialized by interpolation
- Pruning unchanged from baseline

### 3.6 Growth Bound Analysis
- Theorem: under Farey injection, |G(k+1)| <= |G(k)| + |E(k)| where E(k) is the
  number of admissible Delaunay edges
- Expected growth is sublinear due to error gating
- Compare with ADC: potentially exponential without budget capping

## 4. Experiments

### 4.1 Simplified Benchmarks (Proof of Concept)

#### 4.1.1 1D Signal Reconstruction
- Target: smooth + high-frequency burst signal
- Result: 33x efficiency gain (MSE per Gaussian)
- Farey uses fewer Gaussians, concentrates them in the high-frequency region

#### 4.1.2 2D Image Reconstruction
- Target: 256x256 image with smooth gradient + checkerboard patch
- Result: 2.4x efficiency gain, +3.75 dB PSNR
- Farey places Gaussians adaptively via Delaunay edges

#### 4.1.3 3D Density Reconstruction
- Target: sphere with high-detail patch (density field)
- Result: [TBD]x efficiency gain
- Validates that Delaunay-based gap analysis works in 3D

### 4.2 Full 3DGS Benchmarks

#### 4.2.1 Datasets
- Mip-NeRF 360 (9 scenes: indoor + outdoor)
- Tanks and Temples (2 scenes)
- NeRF Synthetic / Blender (8 objects)

#### 4.2.2 Baselines
- 3DGS (Kerbl et al., 2023) — original ADC
- Scaffold-GS (Lu et al., 2024) — voxel anchor hierarchy
- ControlGS (Zheng et al., 2024) — score-based growth
- Mini-Splatting (Fang & Wang, 2024) — densification-aware

#### 4.2.3 Metrics
- PSNR, SSIM, LPIPS (visual quality)
- Gaussian count (compactness)
- MSE per Gaussian (efficiency)
- Training time, peak VRAM (resource usage)
- FPS at inference (rendering speed)

### 4.3 Ablation Studies
- Effect of Farey level schedule (linear vs logarithmic vs adaptive)
- Effect of error threshold
- Effect of scale factor alpha for new Gaussians
- Delaunay vs k-NN approximation for neighbor graph
- With/without error gating

### 4.4 Analysis
- Gaussian spatial distribution visualization (ours vs ADC)
- Scale distribution by scene region
- Growth curves over training
- Per-scene breakdown

## 5. Discussion

- Why does Farey injection work? Connection to optimal quantization theory
- Limitations: Delaunay cost for very large scenes (mitigated by spatial hashing)
- The approach is orthogonal to other improvements (compression, anti-aliasing)
  and can be combined with them
- Broader impact: the Farey injection principle may apply to other learned
  representations (NeRF, point clouds, mesh refinement)

## 6. Conclusion

- Farey-structured densification provides a principled, number-theory-inspired
  replacement for gradient-threshold-based ADC in 3DGS
- Validated across 1D, 2D, 3D with consistent efficiency gains
- The Delaunay-mediant framework is dimension-agnostic and architecture-agnostic
- Achieves comparable or better visual quality with significantly fewer Gaussians

---

## Supplementary Material

### A. Proofs
- A.1 Farey growth bound (Theorem 1)
- A.2 Gap coverage guarantee (every gap eventually filled)
- A.3 Connection to Ford circles and optimal packing

### B. Implementation Details
- B.1 Efficient Delaunay computation for large point sets
- B.2 Spatial hashing for local Delaunay updates
- B.3 Hyperparameter sensitivity analysis

### C. Additional Results
- C.1 Per-scene breakdowns for all datasets
- C.2 Failure cases and limitations
- C.3 Video comparisons (supplementary website)

---

## Key Figures Plan

1. **Teaser figure** (page 1): Side-by-side of ADC vs Farey Gaussian placement on a
   representative scene. ADC scatters Gaussians uniformly; Farey concentrates on detail.

2. **Method overview** (page 3): Diagram showing Delaunay triangulation of Gaussians,
   gap identification, mediant injection, and the progressive refinement schedule.

3. **1D/2D/3D progression** (page 5): Three-panel showing the Farey approach working
   consistently across dimensions, with the Delaunay structure highlighted.

4. **Quantitative results table** (page 6): PSNR/SSIM/LPIPS vs Gaussian count for all
   baselines on Mip-NeRF 360.

5. **Spatial distribution** (page 7): Histogram of Gaussians by scene region, showing
   Farey's adaptive concentration.

6. **Growth curves** (page 7): Gaussian count over training iterations for ADC vs Farey.

---

## Timeline

| Phase | Target Date | Deliverable |
|-------|-----------|-------------|
| Simplified demos (1D, 2D, 3D) | Done / March 2026 | Proof of concept |
| gsplat integration | April 2026 | Working prototype |
| Scaffold-GS integration | May 2026 | Full pipeline |
| Mip-NeRF 360 benchmarks | June 2026 | Quantitative results |
| Paper writing | July 2026 | Draft |
| Submission | July-Aug 2026 | SIGGRAPH Asia / CVPR 2026 |
