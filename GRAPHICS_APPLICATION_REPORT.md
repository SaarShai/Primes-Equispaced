# Farey Properties in Cutting-Edge 3D Graphics (2024-2026)
## Research Report: Where Do Our Properties Have Value?

**Date:** 2026-03-26
**Our Properties Under Evaluation:**
- Generalized Injection: each gap gets at most 1 new point per refinement level (Lean verified)
- Universal Mediant: every new point is the mediant of its neighbors
- No Cascading: zero propagation per refinement step
- Canonical Invertible Hierarchy (Stern-Brocot tree)
- 2D/3D Tensor Product: bounded injection in higher dimensions
- Fisher Information Monotonicity: information content strictly increases

---

## 1. AI/ML Upscaling (DLSS, FSR, XeSS)

### State of the Art (2025-2026)
- **DLSS 4** (CES 2025): Multi Frame Generation generates up to 3 additional frames per rendered frame. Moved from CNNs to **vision transformers** with self-attention across entire frames and across multiple frames. 40% faster, 30% less VRAM than prior gen.
- **DLSS 4.5** (CES 2026): 2nd-generation transformer model with 5x compute of original transformer, trained on expanded high-fidelity dataset. Performance Mode now matches native quality.
- **DLSS 5** (announced GTC March 2026): Full neural rendering -- AI enhances lighting and materials at up to 4K. Received backlash for altering developer art direction.

### Architecture
These systems take a low-resolution rendered frame + motion vectors + depth buffers and reconstruct a high-resolution frame. The transformer architecture evaluates relative importance of each pixel across the full frame and across temporal frames. This is fundamentally a **pixel-space** problem operating on dense regular grids.

### Farey Connection Assessment
Farey sequences operate on **rational number hierarchies** with discrete refinement. DLSS operates on **dense 2D pixel grids** with learned neural interpolation. The problems are structurally different:
- DLSS does not need a hierarchy of refinement -- it does a single-shot upscale
- There is no "mediant" analog in pixel interpolation -- the neural network learns arbitrary nonlinear mappings
- The transformer attention mechanism already handles multi-scale importance weighting
- No mesh or geometric structure is involved

**Rating: NO CONNECTION**

The only remote possibility would be using Farey-structured sampling patterns for the low-res input, but current systems take whatever the game engine renders. This is not a gap anyone is trying to fill.

---

## 2. Neural Radiance Fields (NeRF) and 3D Gaussian Splatting

### State of the Art (2025-2026)
3D Gaussian Splatting (3DGS) has largely overtaken NeRF for real-time applications. The LOD problem is now central:

- **CLoD-GS** (OpenReview 2025): Continuous Level-of-Detail within a single unified 3DGS model, eliminating discrete LOD popping artifacts.
- **LODGE** (NeurIPS 2025 Spotlight): Hierarchical LOD for large-scale scenes, depth-aware smoothing filter + importance-based pruning, chunk-based spatial partitioning for mobile.
- **CLOD-3DGS** (Facebook/Eurographics 2025): Learns to order splats by importance; budget-based and foveated rendering. Open source Vulkan renderer.
- **LOD-GS** (CVPR 2025): Triangle-based MLP organizing Gaussian clusters. Most memory-efficient approach.

### Open Problem: Adaptive Densification is Broken
The original 3DGS densification strategy is a **major bottleneck** (multiple 2025 papers):
- Fixed gradient threshold (0.0002) causes under-densification early, overfitting late
- Splitting creates "floater" artifacts -- erroneous Gaussians that detach from surfaces
- Once floaters form, photometric loss cannot remove them
- Background regions get over-densified, foreground gets overfitted

2025 solutions (AD-GS at SIGGRAPH Asia, GeoTexDensifier, PixelGS) all try to make densification smarter, but they are heuristic fixes.

### Farey Connection Assessment
**This is the strongest connection.** The Gaussian densification problem maps directly onto our refinement properties:

1. **Bounded Injection**: Each region should get at most a controlled number of new Gaussians per refinement step. Currently 3DGS has no such guarantee -- splitting can cascade wildly, creating clusters of redundant Gaussians. Farey's "at most 1 new point per gap per level" could provide a principled bound.

2. **No Cascading**: The zero propagation property means refining one region does not force refinement in adjacent regions. Current 3DGS densification has exactly this problem -- gradient-based splitting in one area can cause chain reactions.

3. **Universal Mediant**: New Gaussians should be placed at the "mediant" position between existing ones. Current splitting just clones a Gaussian and applies noise. A mediant-based placement could be more geometrically principled.

4. **Canonical Invertible Hierarchy**: The LOD problem (CLoD-GS, LODGE) needs a hierarchy that can be traversed up and down. The Stern-Brocot tree provides exactly this -- a canonical ordering of all refinement levels with invertible operations.

5. **Fisher Information Monotonicity**: As you add Gaussians, the information content should strictly increase. Currently, floaters DECREASE information quality. This property could serve as a theoretical criterion for when densification is beneficial.

However, the **practical gap** is significant: Farey operates on 1D rational intervals, while Gaussians live in 3D space with anisotropic covariances. The 2D/3D tensor product property partially addresses this, but the mapping from "bounded injection on rationals" to "bounded densification of oriented 3D ellipsoids" requires substantial theoretical work.

**Rating: STRONG CONNECTION (theoretical) / WEAK-to-MODERATE (practical, needs bridging work)**

---

## 3. Neural Mesh Generation / AI Mesh Tools

### State of the Art (2025-2026)
- **MeshGPT**: Autoregressive triangle mesh generation using learned vocabulary of latent embeddings + transformer prediction. Produces compact artist-like meshes.
- **VertexRegen** (ICCV 2025): Generates meshes from scratch with continuous LOD, progressively adding detail via autoregressive sequence generation.
- **RL-based Delaunay** (CAD 2025): Reinforcement learning trains a graph neural network for mesh point placement, matching Triangle/DistMesh quality.
- **Industry reality** (2026): AI generators (Meshy, Tripo) still produce decimated meshes resembling photogrammetry, not clean quad topology needed for animation.

### Open Problem
The unsolved challenge is generating **clean topology** (edge loops, quads, animation-ready). AI produces dense triangle soups. Progressive/hierarchical generation with controlled topology is an open problem.

### Farey Connection Assessment
The VertexRegen progressive generation and the topology problem connect to Farey properties:

- **Canonical hierarchy**: If mesh vertices were generated in Farey order, each LOD level would be a well-defined subset with guaranteed properties. Current autoregressive models have no such structural guarantee.
- **Bounded injection**: Each refinement level adds a bounded number of vertices, preventing topology explosions.
- **Invertibility**: You could coarsen (remove the highest-level vertices) and get a valid lower-LOD mesh, by construction.

The weakness: real meshes have irregular connectivity, and Farey's structure is inherently tied to rational arithmetic on intervals. Mapping this to arbitrary surface topology is non-trivial.

**Rating: WEAK CONNECTION**

The ideas are appealing conceptually but the gap between 1D rational refinement and 3D mesh topology is large. The RL-based Delaunay work is closer to what Farey could contribute to, but even there the connection requires significant adaptation.

---

## 4. Mesh Shader Tessellation Trend

### State of the Art (2025-2026)
- **Microsoft's stated intent**: Amplification shaders are designed to "eventually replace hardware tessellators" (DirectX specs).
- **Nanite Tessellation** shipped in UE 5.4 (2024): Software-driven tessellation for displacement mapping, dynamic snow/lava. Brian Karis (Epic) emphasizes this complements simplification, not replaces it.
- **GPU mesh shader procedural resurfacing** (CGF 2025): Competitive with traditional tessellation, lower memory/power, supports dynamic visuals.
- **Adoption reality**: Only Epic has pulled off a full Nanite system. Most studios still use legacy pipelines. Mesh shaders are "too much work for hardly any gain" for many devs.

### How Strong Is This Trend?
It is **happening now** but slowly. Nanite Tessellation is production-ready. The industry direction is clear (software tessellation via mesh/amplification shaders), but broad adoption is 3-5 years out for non-Unreal engines. Hardware tessellators will not disappear from GPUs soon but are increasingly bypassed.

### Farey Connection Assessment
This is the connection explored in the original Farey tessellation work. The question is whether it still matters:

- **Software tessellation needs smart subdivision**: With amplification shaders, developers choose their own subdivision scheme. Farey's bounded injection, no-cascading, and mediant properties are directly applicable as a subdivision strategy.
- **But Nanite uses a different paradigm**: Nanite works by simplification from dense meshes, not by tessellation/subdivision of coarse meshes. The tessellation component (displacement mapping) uses standard subdivision surfaces.
- **Procedural generation**: AMD's work graph + mesh shader procedural generation is a natural fit for Farey-structured subdivision.

The honest assessment: the **market for novel tessellation schemes is shrinking** as the industry moves toward Nanite-style simplification. The remaining niche (procedural displacement in amplification shaders) is real but small.

**Rating: WEAK CONNECTION (shrinking market)**

This was the original motivation for Farey tessellation, but the industry has moved toward simplification-first rather than subdivision-first approaches. The connection is mathematically sound but the commercial relevance has diminished.

---

## 5. Procedural Generation + AI

### State of the Art (2025-2026)
- **AMD GPUOpen**: Work graphs + mesh shaders for procedural terrain with LOD. Heightmap terrain with Perlin noise, mesh shader replacing tessellation.
- **Neural style transfer for terrain** (arXiv 2024): Combining procedural noise with neural style transfer from real-world DEM data.
- **GAN-based terrain**: Conditional GANs generate photorealistic terrain from rough PoI sketches.
- **Neural mesh density prediction**: Neural networks predict local mesh size fields from a-posteriori error estimators, enabling feature-aligned adaptivity.

### Farey Connection Assessment
Procedural terrain generation with LOD is inherently hierarchical and uses mediant-like subdivision:

- **Quadtree terrain LOD** is structurally similar to Farey refinement in 2D (the tensor product property applies).
- **Bounded injection** prevents over-refinement: each LOD transition adds a bounded number of vertices.
- **No cascading** is critical for terrain: refining a mountain peak should not force refinement in a distant flat plain. Current quadtree LOD systems approximately have this property, but Farey provides a rigorous guarantee.

However, the existing quadtree/CDLOD approaches already work well enough. The incremental value of Farey's theoretical guarantees over established terrain LOD systems is marginal.

**Rating: WEAK CONNECTION**

Terrain LOD is a solved-enough problem. Farey adds rigor but not performance or quality improvements over existing quadtree approaches.

---

## 6. Geometry Compression / Streaming

### State of the Art (2025-2026)
- **Hierarchical Neural Surfaces** (Dec 2025): Spherical parameterization + INR encoding displacement fields. State-of-the-art compression.
- **NeCGS** (ICCV 2025): Compresses 1000s of meshes up to 900x using TSDF-Def + quantization-aware auto-decoder. Exploits local geometric similarity within and across shapes.
- **Neural Progressive Meshes** (SIGGRAPH 2023, heavily cited 2025): Subdivision-based encoder-decoder. Shared learned generative space for geometric details. Progressive residual transmission between subdivision levels.
- **Quantized Neural Displacement Fields** (CGF 2025): Small neural network encodes displacement field. 4x to 380x compression.
- **Progressive Compression with Diffusion** (ICLR 2025): Single model produces lossy-to-lossless reconstructions from partial bitstreams.

### Open Problem
Progressive mesh streaming requires a canonical hierarchy for transmission: send coarse first, then refinement data. Current approaches learn this hierarchy from data. The question is whether a mathematically principled hierarchy (like Stern-Brocot) could improve compression ratios or streaming efficiency.

### Farey Connection Assessment
**This is the second-strongest connection.**

1. **Neural Progressive Meshes explicitly use subdivision-based hierarchy**: The encoder-decoder operates on subdivision levels. Farey refinement IS a subdivision scheme with provably optimal properties (bounded injection, canonical ordering, invertibility).

2. **Canonical hierarchy for progressive streaming**: The Stern-Brocot tree provides a canonical ordering of all possible refinement points. This maps to a natural bit-allocation strategy: higher in the tree = more important = transmitted first.

3. **Fisher Information Monotonicity**: Each transmitted refinement level strictly increases information content. This is exactly what a progressive codec needs -- guaranteed quality improvement with each additional bit of data.

4. **Invertibility**: The decoder can exactly reconstruct any intermediate LOD level by walking the tree. No need for separate encode/decode models per level.

5. **Compression ratio**: Farey's bounded injection means the number of new points per level is tightly controlled, which could yield better entropy coding bounds.

The gap: Neural Progressive Meshes operate on Loop subdivision of triangle meshes, not on rational number refinement. The mapping from Farey to Loop subdivision is not obvious. However, the structural parallels (hierarchical, progressive, bounded refinement) are strong.

**Rating: STRONG CONNECTION**

This is where the Farey properties most naturally apply. A paper titled "Farey-Structured Progressive Mesh Compression" comparing against Neural Progressive Meshes on compression ratio and streaming quality would be a credible contribution.

---

## 7. Differentiable Rendering

### State of the Art (2025-2026)
- **Gaussian Mesh Renderer (GMR)** (Feb 2026): Derives Gaussian primitives analytically from mesh triangles, enabling gradient flow. Smoother gradients than traditional mesh renderers.
- **Topology-aware optimization** (2025-2026): Persistent homology priors regularize optimization. Penalizes topological defects during gradient descent.
- **MIT thesis** (2025): First differentiable mesh rendering scaling to unbounded real-world scenes.
- **Hybrid volumetric-mesh pipelines**: Gradients flow from soft pseudo-volumetric layers to mesh vertex positions.
- **Key problem**: Vanishing gradients near occluded regions, self-intersecting structures, and the over-smoothing vs. gradient-flow tradeoff in soft rasterization.

### Farey Connection Assessment
The connection here is subtle but potentially interesting:

- **Mediant-based vertex placement**: If mesh vertices are placed at Farey mediants, the refinement structure could provide **smoother gradient landscapes** for optimization. The mediant is the "balanced" point between neighbors, which could reduce gradient discontinuities.
- **Hierarchical optimization**: Start optimizing at coarse Farey level, progressively refine. This coarse-to-fine strategy is already used (e.g., DiffTetVR), but Farey provides a canonical schedule with guaranteed properties.
- **Fisher Information Monotonicity**: Guarantees that each refinement step adds information, which could serve as a principled early-stopping criterion for mesh optimization.

However, differentiable rendering's gradient problems are fundamentally about **visibility discontinuities** and **rasterization softness**, not about refinement structure. Farey properties address refinement order, not the rendering equation.

**Rating: WEAK CONNECTION**

Farey could improve the coarse-to-fine optimization schedule, but the core problems in differentiable rendering (visibility gradients, soft rasterization tradeoffs) are orthogonal to refinement hierarchies.

---

## Summary Table

| Area | State of Art | Farey Connection | Rating | Practical Path |
|------|-------------|------------------|--------|---------------|
| AI Upscaling (DLSS/FSR) | Transformer-based, pixel-space | None | **NO CONNECTION** | N/A |
| 3D Gaussian Splatting | LOD + densification are hot open problems | Bounded injection, no cascading directly address densification bugs | **STRONG** (theory) | Paper: "Farey-Structured Gaussian Densification" |
| Neural Mesh Generation | Autoregressive, topology unsolved | Canonical hierarchy appealing but 1D-to-3D gap large | **WEAK** | Too speculative |
| Mesh Shader Tessellation | Happening but Nanite uses simplification-first | Original motivation, but market shrinking | **WEAK** (shrinking) | Niche: procedural displacement |
| Procedural Generation | Quadtree LOD + neural already works | Farey adds rigor but not perf/quality | **WEAK** | Marginal improvement |
| Geometry Compression | Neural progressive meshes, 900x compression | Canonical hierarchy maps to progressive streaming | **STRONG** | Paper: "Farey-Structured Progressive Compression" |
| Differentiable Rendering | Soft rasterization, topology-aware | Coarse-to-fine schedule improvement | **WEAK** | Secondary benefit only |

---

## Brutally Honest Bottom Line

**Two areas have genuine potential:**

1. **3D Gaussian Splatting densification** -- The open problem (adaptive densification creates floaters, cascades, and over-refinement) maps almost perfectly to Farey's bounded injection and no-cascading properties. The catch: you need to bridge from 1D rational intervals to 3D anisotropic Gaussians. The 2D/3D tensor product property is the starting point, but substantial theoretical work is needed. The field is actively publishing on this exact problem (SIGGRAPH Asia 2025, multiple arXiv papers), so timing is good.

2. **Progressive geometry compression/streaming** -- Neural Progressive Meshes already use subdivision hierarchies. Farey provides a mathematically canonical alternative with provably optimal properties. The Fisher Information Monotonicity result directly guarantees quality improvement per transmitted level. This is the most natural application.

**Everything else is a stretch.** The AI upscaling world (DLSS etc.) has zero need for Farey. Mesh shader tessellation was the original pitch but the industry is moving away from subdivision-first approaches. Procedural generation and differentiable rendering have existing solutions that work well enough.

**The honest risk:** Even in the two strong areas, you face the "1D-to-3D bridge" problem. Farey properties are proven for rational intervals. Extending them to 3D Gaussian fields or triangle mesh subdivision requires non-trivial theoretical work that may not preserve the elegant properties. The 2D/3D tensor product result helps, but it is the beginning of the bridge, not the whole bridge.

---

## Recommended Next Steps

1. **For 3DGS densification**: Implement a toy 2D version where Gaussians on a line segment are refined using Farey-structured densification. Compare against standard 3DGS splitting on a 1D reconstruction task. If it eliminates floaters and cascading, write it up.

2. **For progressive compression**: Take the Neural Progressive Meshes architecture and replace Loop subdivision with Farey-structured refinement on a simple test case (e.g., height-field mesh). Measure compression ratio and reconstruction quality vs. the baseline.

3. **For both**: The Fisher Information Monotonicity result is the most unique property. No existing work in either area has a comparable theoretical guarantee. Lead with this in any paper pitch.
