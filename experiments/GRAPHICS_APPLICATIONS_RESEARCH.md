# Farey-Based Methods in Computer Graphics: Research Assessment

**Date:** 2026-03-29
**Status:** Research survey (no code, no experiments)
**Motivation:** Our 3DGS results showed Farey achieves 5.5x compactness advantage. Where else in graphics could Farey properties provide genuine gains?

## Farey Properties Relevant to Graphics

| Property | What it does | Graphics relevance |
|----------|-------------|-------------------|
| **Gap-filling (mediant)** | Inserts the simplest fraction between two neighbors | Adaptive refinement without cascading |
| **Injection principle** | At most 1 new point per gap when going from F_n to F_{n+1} | Controlled densification, no explosion |
| **Hierarchical (Stern-Brocot)** | Binary tree of all rationals via mediants | Natural LOD structure |
| **Equidistribution** | F_n covers [0,1] with discrepancy O(1/N) (conditional on RH) | Uniform coverage guarantees |

---

## 1. MESH GENERATION & PHYSICS SIMULATION

### 1a. Adaptive Mesh Refinement (AMR)

**Current SOTA:** Delaunay refinement (Ruppert, Chew algorithms) inserts circumcenters or off-centers of poor-quality triangles. The element quality is guaranteed (minimum angle bounds of 20.7-30 degrees). Recent work (2025-2026) includes PINNs-guided AMR that uses neural network residuals to identify where to refine, and global-aware voxelized density control for 3DGS scenes.

**What Farey could offer:**
- **Mediant insertion as refinement operator:** When a mesh edge spans two rational coordinates a/b and c/d, the mediant (a+c)/(b+d) is the simplest point between them. This is analogous to but different from circumcenter insertion.
- **Injection principle prevents cascading:** Standard Delaunay refinement can trigger cascading splits (inserting one point forces splitting of adjacent elements). Farey's guarantee of at most 1 new point per gap is structurally similar to what AMR practitioners want.
- **Stern-Brocot tree as LOD hierarchy:** The tree depth corresponds to denominator size, providing a natural multi-resolution structure.

**Honest assessment: MARGINAL ADVANTAGE.**
- Delaunay refinement already has strong theoretical guarantees (element quality bounds, grading, size-optimality).
- The mediant does not account for geometry -- it inserts at a number-theoretically optimal position, not a geometrically optimal one (circumcenter minimizes the circumradius-to-shortest-edge ratio).
- No prior work found connecting Farey/mediant insertion to mesh refinement in any published paper.
- **The gap-filling property is real but mismatched:** mesh refinement needs geometric quality (angles, aspect ratios), not number-theoretic simplicity.
- One genuine niche: structured meshes on rational grids where coordinates are inherently rational. Here mediant insertion preserves rationality and low denominators, which could matter for exact arithmetic in computational geometry.

**Verdict:** Not competitive with Delaunay refinement for general meshes. Possible niche in rational-coordinate structured grids.

### 1b. Collision Detection

**Current SOTA:** Broadphase uses spatial hashing (Teschner et al.) with hierarchical grids, BVH trees, or sweep-and-prune. The only number-theoretic connection found is that prime-sized hash tables reduce collisions.

**Honest assessment: NO REAL ADVANTAGE.**
- Collision detection is fundamentally about spatial proximity, not about number-theoretic properties of coordinates.
- Farey properties do not help here. The problem is geometric, not arithmetic.

**Verdict:** No application.

### 1c. Material Simulation (Cloth, Fluids, Deformables)

**What Farey could offer:**
- Adaptive remeshing during simulation could use mediant insertion for controlled refinement.
- The injection principle could prevent the mesh explosion that happens when cloth wrinkles or fluids develop thin features.

**Honest assessment: WEAK.**
- These simulations need adaptive refinement based on physical quantities (strain, vorticity), not number-theoretic gap size.
- Existing methods (e.g., edge-collapse / edge-split based on local error metrics) are well-tuned to physics.

**Verdict:** No clear advantage over existing physics-driven adaptive methods.

---

## 2. RAY TRACING SAMPLING

### 2a. Quasi-Random Sampling (Halton, Sobol, R2) vs Farey

**Current SOTA:** The field is mature and competitive.
- **Halton sequence:** O(1/N) convergence, best in dimensions <= 6, degrades in higher dimensions.
- **Sobol sequence:** O(1/N) convergence, best for higher dimensions, benefits enormously from Owen scrambling (approaches O(N^{-3/2}) convergence).
- **R2 sequence (Roberts 2018):** Based on generalized golden ratio, provably optimal among Weyl sequences, single line of code to compute, consistently best normalized distance.
- **Blue noise:** Spatiotemporal blue noise (NVIDIA) distributes Monte Carlo error as blue noise in screen space, critical for real-time ray tracing.
- **Koksma-Hlawka bound:** Error <= D_N * V(f), where D_N is the star discrepancy and V(f) is the Hardy-Krause variation.

**Farey sequence discrepancy:**
- F_n has approximately 3n^2/pi^2 elements.
- The star discrepancy of F_n satisfies D_N = O(1/N) if and only if the Riemann Hypothesis holds.
- Under RH, the discrepancy is O(N^{-1} * (log N)^{2+epsilon}).
- Without RH, we only know D_N = O(N^{-1/2+epsilon}).

**Critical comparison at same N:**
- For N points, Halton and Sobol achieve D_N = O(N^{-1} * (log N)^d) unconditionally.
- Farey achieves similar D_N only conditionally (on RH) and only in 1D.
- Farey sequences are inherently 1D -- they live on [0,1]. Extending to 2D or higher requires product constructions that lose the clean theoretical properties.
- Halton, Sobol, and R2 are natively multi-dimensional.

**Honest assessment: NO ADVANTAGE for ray tracing sampling.**
- The existing sequences (Sobol + Owen scrambling, R2, blue noise) are extremely well-optimized for graphics.
- Farey's theoretical discrepancy bound is conditional on RH and only matches (does not beat) existing sequences.
- Farey is 1D-native; graphics needs 2D+ sampling (pixel position, lens, time, wavelength, BRDF direction = 5D+).
- No prior work found using Farey sequences for graphics sampling.
- The R2 sequence already exploits the number-theoretic insight (golden ratio = worst rational approximation = best equidistribution) that connects to Farey/continued fraction theory, but in a more practically useful form.

**Verdict:** Existing quasi-random methods already incorporate the relevant number theory. Farey adds nothing.

### 2b. Importance Sampling

**Current SOTA:** Multiple importance sampling (MIS), next event estimation (NEE), path guiding with octree/kd-tree structures, Russian roulette.

**What Farey could offer:** Nothing. Importance sampling is about matching the sampling distribution to the integrand, not about uniform coverage.

**Verdict:** No application.

---

## 3. 3D GAUSSIAN SPLATTING AND RELATED

### 3a. 3DGS Adaptive Density Control (ADC)

**Current SOTA and its problems:**
Standard 3DGS ADC uses gradient-based heuristics: if a Gaussian has high view-space gradient, it is split (if large) or cloned (if small). This has known failure modes:
1. **Local Enclosure Bias:** Gradient signals are local; no global reference for where densification is actually needed.
2. **Density-dependent Bias:** Densification rate couples to initial point density, not geometric demand.
3. **Cascading densification:** Splitting can trigger further splits in neighbors.
4. **Floaters and artifacts:** Over-densification in foreground, under-densification in background.

**2025 research directions:**
- Global-aware voxelized ADC (frequency-domain analysis to resolve gradient ambiguity)
- Alternating densification phases (AD-GS, SIGGRAPH Asia 2025)
- One-shot dense initialization (NexusGS, RGS-SLAM)
- Localized points management with error source zone identification (CVPR 2025)

**What Farey offers (and why it already worked in our benchmark):**
- **Injection principle maps directly to ADC:** "At most 1 new Gaussian per under-sampled gap" prevents the cascading densification that plagues standard ADC.
- **Mediant placement is geometrically motivated in 1D:** For Gaussians along a ray or on a surface parameterized by a single coordinate, the mediant finds the optimal insertion point.
- **Stern-Brocot hierarchy gives natural LOD:** Gaussians at depth k in the tree have denominators <= 2^k, providing a built-in level-of-detail structure.

**Honest assessment: THIS IS OUR STRONGEST APPLICATION.**
- Our 5.5x compactness advantage is real and directly attributable to the injection principle preventing Gaussian bloat.
- The gap-filling property addresses the exact failure mode (Local Enclosure Bias) that the 2026 global-aware voxelized ADC paper identifies.
- However, our current results are only on a synthetic 1D benchmark. The key question is whether mediant-based insertion generalizes to 3D scenes with complex geometry.
- **Limitation:** In 3D, "gaps" between Gaussians are not as cleanly defined as in 1D. We need a principled way to identify gaps in 3D Gaussian distributions and define mediants in that context.

**Verdict: STRONG -- pursue this. But must solve the 1D-to-3D generalization problem.**

### 3b. NeRF Point Sampling Along Rays

**Current SOTA:**
- Original NeRF: stratified uniform sampling + hierarchical volume sampling (coarse-to-fine).
- ProNeRF (2024): projection-aware sampling with learned sampler networks.
- View-consistent sampling (ICCV 2025): pre-computed view-consistency distribution for importance sampling.
- End-to-end sampling point optimization (2024): MLP-Mixer learns optimal sample positions.
- Probability-guided sampling (ECCV 2024): PDF in projection space focuses rays on regions of interest.

**What Farey could offer:**
- **Ray sampling is inherently 1D** (parameterized by distance along the ray). This is exactly where Farey excels.
- **Mediant insertion along rays:** Start with coarse samples, insert mediants in gaps with highest error. The injection principle ensures controlled densification.
- **Stern-Brocot hierarchy for coarse-to-fine:** This directly parallels NeRF's existing hierarchical sampling, but with a principled number-theoretic structure instead of learned heuristics.

**Honest assessment: MODERATE POTENTIAL.**
- NeRF ray sampling IS a 1D problem, which is Farey's sweet spot.
- However, the field is moving away from NeRF toward 3DGS (which does not sample along rays).
- Existing learned samplers (ProNeRF, view-consistent) already achieve excellent results by learning scene-specific distributions.
- Farey would provide a scene-agnostic baseline that does not require training, which could be useful for initialization or for very sparse settings.
- **Key question:** Does Farey's equidistribution property actually help when the density along a ray is highly non-uniform (empty space, then a thin surface, then more empty space)?

**Verdict: Moderate -- could work as initialization or regularizer for NeRF ray sampling, but the field is moving away from NeRF.**

### 3c. 4DGS (Dynamic Scenes)

**What it is:** Extends 3DGS to time-varying scenes. Uses deformation fields (HexPlane) or per-frame Gaussian parameters.

**What Farey could offer:**
- Temporal densification: when a scene changes between frames, use mediant-based insertion in the temporal dimension to add Gaussians only where motion creates new gaps.
- The injection principle prevents temporal Gaussian bloat.

**Honest assessment: SPECULATIVE but interesting.**
- The temporal dimension is again 1D (time), so Farey's properties apply cleanly.
- No existing work uses number-theoretic methods for temporal densification.
- Worth exploring but needs concrete experiments.

**Verdict: Speculative -- interesting direction, no evidence yet.**

### 3d. Text-to-3D (Score Distillation Sampling)

**Current SOTA (2025):**
- SDS and its variants (VSD, UDS, CFD, SemanticSDS, L2-VSD, Dive3D) optimize a 3D representation by distilling a 2D diffusion model.
- Key problems: mode-seeking behavior (over-smoothing), Janus artifacts (multi-face problem), lack of diversity.
- 2025 fixes: multi-view consistent noise, reward-guided gradients, flow-based distillation.

**What Farey could offer:**
- SDS involves sampling noise levels and camera viewpoints. Farey-based sampling of viewpoints could ensure more uniform angular coverage.
- However, the core SDS problem is about gradient quality from the diffusion model, not about sampling uniformity.

**Honest assessment: NO REAL ADVANTAGE.**
- The bottleneck in text-to-3D is the quality of the distillation gradient, not the sampling distribution.
- Camera viewpoints are already sampled uniformly or with importance weighting.
- Farey adds nothing to the core SDS optimization.

**Verdict:** No application.

### 3e. SLAM with Gaussian Splatting

**Current SOTA (2025):**
- Multiple Gaussian SLAM systems: SplaTAM, MDGS-SLAM, RGS-SLAM, FeatureSLAM, OGS-SLAM, SplatMAP.
- Key challenge: where to add new Gaussians as the camera moves through the scene.
- Approaches: residual-driven densification, one-shot correspondence-based initialization, multi-view densification, SLAM-informed adaptive densification.

**What Farey could offer:**
- As the camera moves, new scene regions are observed. Farey-based insertion could add Gaussians only in genuine gaps in the map.
- The injection principle prevents the "floater" problem (spurious Gaussians in already-covered regions).
- Stern-Brocot hierarchy could provide LOD for the Gaussian map (coarse map far from camera, fine near).

**Honest assessment: MODERATE POTENTIAL.**
- SLAM densification faces exactly the problem Farey solves: controlled insertion in under-covered regions without cascading.
- However, SLAM operates in 3D, and Farey's clean properties are 1D.
- The one-shot initialization approach (RGS-SLAM) already largely solves the densification problem by starting with a dense map.

**Verdict: Moderate -- similar to 3DGS ADC. The 1D-to-3D generalization is the bottleneck.**

---

## 4. MEDICAL IMAGING: CT/MRI RECONSTRUCTION

**Current SOTA:**
- Compressed sensing (Candes, Donoho, Tao) enables reconstruction from fewer samples than Nyquist requires, given sparsity in some transform domain.
- Deep learning + compressed sensing integration is the dominant 2025 trend.
- Sampling patterns: random undersampling of k-space (Fourier domain), Poisson disc, variable density random.

**What Farey could offer:**
- k-space sampling is inherently structured (Cartesian grid, radial, spiral). Farey-based sampling along radial lines could provide better angular coverage.
- The equidistribution property could give provable coverage guarantees for sampling patterns.

**Honest assessment: WEAK.**
- Compressed sensing theory requires incoherent measurements. Random sampling provides this naturally; Farey's deterministic structure may actually hurt incoherence.
- Deep learning methods are rapidly making hand-crafted sampling patterns obsolete by learning to reconstruct from whatever pattern is given.
- No prior work found combining Farey/number-theoretic methods with medical image reconstruction.

**Verdict:** Unlikely to beat existing methods. The incoherence requirement works against Farey's structured nature.

---

## 5. LiDAR POINT CLOUD DENSIFICATION

**Current SOTA (2025):**
- Image-guided pseudo-LiDAR generation (ImagePG)
- Spherical coordinate interpolation (DenseSphere)
- VAE/diffusion-based densification
- Sparse transformer fusion (FlatFusion)

**What Farey could offer:**
- LiDAR produces points on radial rays from the sensor. Along each ray, the spacing increases with distance (inverse square).
- Farey-based insertion along each ray could add synthetic points in the largest gaps, with the injection principle preventing over-densification near the sensor.

**Honest assessment: WEAK TO MODERATE.**
- The 1D-along-a-ray aspect is promising (same argument as NeRF ray sampling).
- However, the real information needed for densification comes from other modalities (cameras, learned priors), not from geometric gap-filling.
- Simply inserting points in geometric gaps without knowing what is there creates hallucinated geometry.

**Verdict:** Gap-filling alone is insufficient. Would need to be combined with learned priors to have value.

---

## 6. CUTTING-EDGE AREAS

### 6a. Neural Implicit Representations (DeepSDF, Occupancy Networks)

**What Farey could offer:** Sample query points along rays or in 3D space using Farey-based spacing. Same argument as NeRF ray sampling.

**Honest assessment: WEAK.** The field is moving toward analytical intersection methods (AlphaSurf, 2025) that avoid Monte Carlo sampling entirely.

### 6b. Differentiable Rendering

**Current SOTA (2025):** Advanced Monte Carlo with warped-area sampling, octree/kd-tree path guiding, Owen-scrambled Sobol. A comprehensive 2025 survey covers the full landscape.

**What Farey could offer:** Nothing beyond what existing quasi-random sequences already provide. The 1D limitation is fatal for multi-dimensional path space integration.

**Verdict:** No advantage.

### 6c. Light Field Rendering

**Honest assessment:** Light fields are 4D (2D position + 2D direction). Farey's 1D nature makes it unsuitable.

### 6d. Volumetric Video Compression

**Current SOTA (2025):** MPEG V-PCC and G-PCC standards, learned compression, adaptive tiling, quality-aware point cloud sampling, DASH streaming frameworks. Active area with multiple 2025 publications.

**What Farey could offer:**
- Progressive transmission using Stern-Brocot hierarchy: send coarse level first, then refinements.
- This is analogous to progressive mesh transmission, which is well-established.

**Honest assessment: MODERATE NICHE.**
- The progressive/hierarchical transmission idea is sound but not novel -- progressive meshes (Hoppe 1996) and LOD streaming are standard.
- Farey's specific contribution would be the guarantee that each refinement level adds exactly 1 point per gap, giving predictable bandwidth.
- The 2025 work on adaptive 3DGS video streaming (saliency-driven tiling) is a better fit for our 3DGS results than Farey-based compression.

**Verdict:** Minor niche. The hierarchical property is real but not differentiated enough from existing progressive representations.

### 6e. Photon Mapping / Path Tracing

**Current SOTA:** Differentiable photon mapping with generalized path gradients (2025), blue noise photon relaxation, importance-driven path tracing using photon maps (Jensen).

**What Farey could offer:** Farey-based photon placement could provide more uniform caustic patterns. But photon mapping already uses sophisticated importance sampling and blue noise relaxation.

**Honest assessment: NO ADVANTAGE.** The existing methods are well-optimized and address the actual bottleneck (variance reduction in caustics), not uniform placement.

---

## SUMMARY: RANKED OPPORTUNITIES

| Rank | Application | Farey advantage | Key property | Honest rating |
|------|------------|----------------|--------------|---------------|
| 1 | **3DGS Adaptive Density Control** | Injection principle prevents cascading; mediant fills gaps optimally | Injection + gap-filling | STRONG |
| 2 | **Gaussian SLAM densification** | Controlled map growth, no floaters | Injection + hierarchy | MODERATE |
| 3 | **NeRF ray sampling** | 1D problem where Farey excels; scene-agnostic initialization | Gap-filling + hierarchy | MODERATE |
| 4 | **4DGS temporal densification** | Temporal dimension is 1D | Injection in time | SPECULATIVE |
| 5 | **LiDAR ray densification** | Per-ray 1D gap filling | Gap-filling | WEAK-MODERATE |
| 6 | **Volumetric video progressive streaming** | Stern-Brocot gives predictable refinement | Hierarchy | WEAK |
| 7 | **Structured mesh refinement** | Rational coordinate preservation | Mediant | NICHE |
| -- | Ray tracing QMC sampling | Existing methods already optimal | -- | NO ADVANTAGE |
| -- | Collision detection | Irrelevant | -- | NO ADVANTAGE |
| -- | Text-to-3D / SDS | Bottleneck is elsewhere | -- | NO ADVANTAGE |
| -- | Medical imaging (CT/MRI) | Incoherence requirement conflicts | -- | NO ADVANTAGE |
| -- | Differentiable rendering | Multi-dimensional; 1D limitation fatal | -- | NO ADVANTAGE |

---

## KEY INSIGHT: THE 1D BOTTLENECK

The pattern across all applications is clear: **Farey properties are powerful in 1D and weak or irrelevant in higher dimensions.**

Applications where the problem can be decomposed into 1D sub-problems (rays in NeRF, time in 4DGS, radial lines in LiDAR) retain some Farey advantage. Applications that are inherently multi-dimensional (path tracing integration, mesh quality, collision detection) do not.

**The critical research question is:** Can we define a meaningful multi-dimensional generalization of Farey gap-filling? Possible approaches:
1. **Per-axis decomposition:** Apply Farey independently along each axis (like Halton uses different primes per dimension). But this loses the inter-dimensional correlations that make Sobol/Owen scrambling effective.
2. **Geodesic Farey on manifolds:** Define mediants along geodesic paths on surfaces. This would extend the 1D property to curved surfaces.
3. **Voronoi-guided Farey:** Use Voronoi cells to identify gaps in 3D, then insert mediants along the line connecting the two most distant Gaussians. This preserves the injection principle in a localized 1D sense.

Option 3 (Voronoi-guided Farey) is the most promising path for generalizing our 3DGS results to 3D.

---

## PRIOR WORK CHECK

**Number-theoretic methods in graphics:**
- Golden ratio sequences for sampling (Schretter & Kobbelt) -- uses continued fraction theory related to Farey
- R2 sequence (Roberts 2018) -- exploits golden ratio as worst-approximable irrational, connected to Farey/Stern-Brocot theory
- Low-discrepancy blue noise (Ahmed et al., SIGGRAPH Asia 2016) -- uses van der Corput sequences
- Farey sequence discrepancy and RH connection (classical number theory)

**No prior work found using Farey sequences directly for:**
- Mesh refinement
- 3DGS densification
- NeRF sampling
- Point cloud densification
- Any graphics application

**This confirms our work is novel but also means the burden of proof is on us to demonstrate genuine advantage over existing methods.**

---

## RECOMMENDED NEXT STEPS

1. **3DGS in 3D (Priority 1):** Design and test Voronoi-guided Farey densification for real 3D Gaussian scenes. This is the make-or-break experiment.
2. **NeRF ray sampling (Priority 2):** Implement Farey-based hierarchical sampling along NeRF rays and compare against stratified + hierarchical volume sampling on standard benchmarks (NeRF-Synthetic, LLFF).
3. **Do NOT pursue:** Ray tracing QMC, collision detection, medical imaging, or differentiable rendering. The existing methods are better suited and our properties do not transfer.
4. **Write up 3DGS results:** Even if limited to 1D, the 5.5x compactness result with clean theoretical motivation (injection principle) is publishable as a position paper or workshop paper, with the 3D generalization as future work.
