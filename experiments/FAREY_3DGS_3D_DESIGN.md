# Farey-Structured Densification for 3D Gaussian Splatting: Architecture Design

## 1. Overview

This document describes how Farey-guided densification integrates with 3D Gaussian
Splatting (3DGS), specifically targeting the Scaffold-GS architecture. We generalize
the validated 1D and 2D approaches:

| Dimension | Neighbor structure          | Gap metric                        | Result               |
|-----------|----------------------------|-----------------------------------|----------------------|
| 1D        | Sorted order (left/right)   | gap / (sigma_L + sigma_R)         | 33x efficiency gain  |
| 2D        | Delaunay triangulation edges| dist / (r_i + r_j), r=sqrt(sx*sy) | 2.4x, +3.75 dB PSNR |
| **3D**    | **3D Delaunay tetrahedralization edges** | **dist / (r_i + r_j), r=cbrt(sx*sy*sz)** | **pending** |

The core principle is dimension-invariant: Delaunay triangulation provides the natural
notion of "spatial neighbors" in any dimension, and the Farey mediant injection rule
(at most one new primitive per gap per refinement level) controls growth.

## 2. Scaffold-GS Background

Scaffold-GS (Lu et al., 2024) introduces a two-level hierarchy:

```
Scaffold-GS Architecture:
  Voxel Grid -> Anchors (coarse) -> Neural Gaussians (fine)

  Each anchor a_v at voxel v:
    - Position: p_v (voxel center)
    - Feature vector: f_v
    - Scaling factor: s_v
    - Offset MLP: f_v -> {delta_k, sigma_k, alpha_k, color_k} for k=1..K

  Growing rule (standard):
    For each anchor a_v, accumulate view-space gradient magnitudes.
    If avg_gradient > tau_g AND the voxel has unoccupied neighbors:
      Spawn new anchor in the unoccupied neighbor voxel.
```

**Key insight:** Scaffold-GS already discretizes space into a voxel grid. Its growing
rule is a 3D analog of ADC — it uses gradient thresholds to decide *when* to grow,
but the *where* is constrained to adjacent empty voxels. This is exactly where Farey
injection can improve: instead of gradient thresholds, we use structural gap analysis
to determine which empty voxels most need filling.

## 3. Farey Integration Architecture

### 3.1 The Farey-Scaffold Bridge

```
Standard Scaffold-GS pipeline:
  [Train] -> [Accumulate gradients] -> [Grow if grad > threshold] -> [Train]

Farey-Scaffold pipeline:
  [Train] -> [Build Delaunay on anchors] -> [Compute gap metrics]
  -> [Farey-admit gaps at level N] -> [Error-gate] -> [Inject mediants] -> [Train]
```

The replacement is surgical: we swap the gradient-threshold growing criterion with
Farey gap analysis, while keeping everything else (the anchor-to-Gaussian MLP,
the rendering pipeline, the pruning logic) unchanged.

### 3.2 Gap Definition in 3D

Given a set of anchors with positions {p_i} and effective radii {r_i}:

**Effective radius** (isotropic equivalent):
```
r_i = (sx_i * sy_i * sz_i)^(1/3)    [geometric mean of scales]
```

For anisotropic Gaussians with a full covariance, use:
```
r_i = det(Sigma_i)^(1/6)            [sixth root of determinant]
```

**3D Delaunay tetrahedralization:**
```python
from scipy.spatial import Delaunay
points = np.array([[x1,y1,z1], [x2,y2,z2], ...])  # anchor positions
tri = Delaunay(points)
# tri.simplices gives tetrahedra; extract unique edges
```

**Gap metric for edge (i, j):**
```
d_edge(i,j) = ||p_i - p_j|| / (r_i + r_j)
```

This is the "Farey denominator" analog: it counts how many effective radii fit in
the gap between two Delaunay-adjacent anchors. A large d_edge means the gap is
under-resolved.

### 3.3 Farey Level and Refinement Schedule

**Farey level N** controls which gaps are eligible for injection at each refinement
round. The schedule mirrors the 1D/2D approach:

```
Round 1: N=2  (only inject into very large gaps, d_edge <= 2)
Round 2: N=3  (admit slightly smaller gaps)
Round 3: N=4
...
Round k: N=k+1
```

**Admissibility rule:** Edge (i,j) is admissible at level N if:
```
1 < d_edge(i,j) <= N
```

The lower bound d_edge > 1 avoids injecting between already-overlapping Gaussians.
The upper bound d_edge <= N implements the progressive refinement: coarse gaps first,
fine gaps later.

**Farey injection principle (3D):** At most ONE new anchor per Delaunay edge per
refinement round. This is the structural guarantee that prevents exponential growth.

### 3.4 Mediant Position and Initialization

For an admissible edge (i, j), the new anchor is placed at:

**Position (sigma-weighted mediant):**
```
p_new = p_i + t * (p_j - p_i)
where t = r_i / (r_i + r_j)
```

This places the new anchor closer to the larger Gaussian (which "reaches" further
into the gap), matching the classical Farey mediant property.

**Scale initialization:**
```
r_new = alpha * (r_i + r_j) / 2,   alpha = 0.35
```

The factor alpha < 0.5 ensures the new anchor is smaller than its parents, enabling
progressive refinement.

**Weight/opacity initialization:**
```
w_new = 0.5 * (w_i + w_j)
```

**Feature vector (for Scaffold-GS):**
```
f_new = 0.5 * (f_i + f_j)   [linear interpolation of anchor features]
```

### 3.5 Error Gating

Not every admissible gap needs filling. We add an error gate:

1. Compute current rendering at the midpoint region
2. Compare against ground truth (if available) or use the accumulated gradient
   magnitude as a proxy for reconstruction quality
3. Only inject if the local error exceeds threshold tau_e

For the simplified demo, we directly evaluate density error at sample points
near the gap midpoint. For full Scaffold-GS integration, we use the existing
per-anchor gradient accumulation as the error proxy.

### 3.6 Pruning

Farey injection is paired with pruning to remove low-contribution anchors:

```
Prune anchor i if:
  - opacity alpha_i < tau_alpha (too transparent)
  - OR max(scale_i) > scene_extent * tau_scale (too large, "floater")
  - OR contribution to rendered pixels < tau_contrib over last M frames
```

This is unchanged from standard Scaffold-GS / 3DGS pruning.

## 4. Full Algorithm Pseudocode

```python
def farey_3dgs_training(scene, config):
    """Complete Farey-guided 3DGS training loop."""

    # Initialize anchors from SfM point cloud or random
    anchors = initialize_anchors(scene.sfm_points)
    optimizer = Adam(anchors.parameters(), lr=config.lr)
    farey_level = 1

    for iteration in range(config.max_iterations):
        # ── Forward pass ──────────────────────────────────────────
        viewpoint = sample_camera(scene)
        rendered = render_gaussians(anchors, viewpoint)
        loss = l1_loss(rendered, viewpoint.gt_image) + \
               config.lambda_ssim * (1 - ssim(rendered, viewpoint.gt_image))

        # ── Backward pass ─────────────────────────────────────────
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # ── Farey densification (every D iterations) ──────────────
        if iteration % config.densify_interval == 0 \
           and iteration < config.densify_until:

            farey_level += 1

            # Step 1: Build 3D Delaunay on anchor positions
            positions = anchors.get_positions()  # (N, 3)
            radii = anchors.get_effective_radii()  # (N,)

            tri = Delaunay(positions.numpy())
            edges = extract_unique_edges(tri.simplices)

            # Step 2: Score each edge
            candidates = []
            for (i, j) in edges:
                dist = np.linalg.norm(positions[i] - positions[j])
                d_edge = dist / (radii[i] + radii[j] + 1e-8)

                # Farey admissibility
                if d_edge <= 1.0 or d_edge > farey_level:
                    continue

                # Error gate (use accumulated gradient as proxy)
                edge_error = max(anchors.grad_accum[i], anchors.grad_accum[j])
                if edge_error < config.error_threshold:
                    continue

                # Compute mediant position
                t = radii[i] / (radii[i] + radii[j] + 1e-8)
                p_new = positions[i] + t * (positions[j] - positions[i])
                r_new = 0.35 * (radii[i] + radii[j])

                candidates.append((edge_error, p_new, r_new, i, j))

            # Step 3: Inject (budget-limited, sorted by error)
            candidates.sort(key=lambda c: -c[0])
            budget = config.max_anchors - len(anchors)

            for err, p_new, r_new, i, j in candidates[:budget]:
                new_anchor = create_anchor(
                    position=p_new,
                    scale=r_new,
                    features=0.5 * (anchors.features[i] + anchors.features[j]),
                    opacity=0.5 * (anchors.opacity[i] + anchors.opacity[j])
                )
                anchors.add(new_anchor)
                optimizer.extend(new_anchor.parameters())

            # Step 4: Reset gradient accumulators
            anchors.reset_grad_accum()

        # ── Pruning (every P iterations) ──────────────────────────
        if iteration % config.prune_interval == 0:
            prune_mask = (anchors.opacity < config.min_opacity) | \
                         (anchors.max_scale > config.max_scale_ratio * scene.extent)
            anchors.remove(prune_mask)
            optimizer.remove(prune_mask)

    return anchors
```

## 5. Complexity Analysis

### 5.1 Per-Refinement Cost

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Delaunay tetrahedralization | O(N^2) worst, O(N log N) expected | N = number of anchors |
| Edge extraction | O(T) | T = number of tetrahedra, O(N) expected |
| Gap scoring | O(E) | E = number of edges, O(N) expected |
| Sorting candidates | O(E log E) | |
| Injection | O(B) | B = budget |
| **Total per round** | **O(N log N)** expected | |

For typical 3DGS scenes with N ~ 10^5-10^6 anchors, the Delaunay computation is the
bottleneck. Mitigation strategies:

1. **Spatial hashing**: Only rebuild Delaunay in regions with high gradient, not globally
2. **Incremental Delaunay**: Use incremental insertion rather than full rebuild
3. **Approximate neighbors**: Use k-NN (via KDTree) as a faster proxy for Delaunay edges

### 5.2 Growth Rate Bound

**Theorem (Farey growth bound, 3D):** Under Farey-guided injection with level schedule
N(k) = k+1 at round k, with at most one injection per Delaunay edge per round:

```
|anchors(k+1)| <= |anchors(k)| + |edges(k)|
```

Since the expected number of Delaunay edges in 3D is O(N), this gives at most O(N)
new anchors per round. Combined with error gating (which typically admits a small
fraction of edges), the actual growth is sublinear.

Compare with standard ADC which can split every Gaussian with grad > threshold,
leading to potentially exponential growth without careful budget management.

## 6. Integration Points with Scaffold-GS

### 6.1 Minimal Changes Required

```
File: scaffold_gs/model.py
  - Add: effective_radius() method to Anchor class
  - Add: farey_densify() method alongside existing densify_and_prune()

File: scaffold_gs/train.py
  - Replace: densify_and_prune() call with farey_densify()
  - Add: farey_level tracking variable

File: scaffold_gs/utils.py (new)
  - Add: delaunay_edges() helper
  - Add: farey_gap_score() helper
  - Add: mediant_position() helper
```

### 6.2 Configuration

```yaml
# farey_config.yaml
farey:
  enabled: true
  initial_level: 1
  level_increment: 1          # +1 per densification round
  gap_lower_bound: 1.0        # d_edge > 1 (skip overlapping)
  scale_factor: 0.35          # new anchor scale relative to parents
  error_threshold: 0.0005     # local error gate
  max_injections_per_round: 1000
  use_approximate_neighbors: false  # true for large scenes
  neighbor_k: 20              # k for approximate kNN neighbors
```

## 7. Expected Behavior and Hypotheses

### 7.1 Density-Adaptive Refinement

The Farey approach should:
- Place MORE anchors in geometrically complex regions (thin structures, edges, fine detail)
- Place FEWER anchors in smooth regions (walls, floors, sky)
- Achieve this WITHOUT per-region hyperparameter tuning

This is because:
- Complex regions have diverse anchor scales -> larger d_edge values -> admitted earlier
- Smooth regions have similar, large-scale anchors -> small d_edge -> admitted later (or never)

### 7.2 Efficiency Predictions

Based on 1D (33x) and 2D (2.4x) results, we hypothesize:

| Metric | Prediction | Rationale |
|--------|-----------|-----------|
| Gaussian count reduction | 1.5-3x fewer | Gap-aware placement avoids redundancy |
| PSNR at equal count | +1-3 dB | Better spatial distribution |
| Training convergence | 1.2-2x faster | Fewer wasted Gaussians to optimize |
| Memory reduction | 1.5-3x | Fewer Gaussians = less VRAM |

The efficiency gain may be smaller in 3D because:
- 3DGS already has pruning and opacity-based densification
- View-dependent effects add complexity not present in 1D/2D
- Scaffold-GS's voxel grid already provides some spatial structure

### 7.3 Scene-Dependent Effects

| Scene type | Expected Farey advantage |
|-----------|-------------------------|
| Indoor (Mip-NeRF 360) | High - many flat surfaces waste Gaussians under ADC |
| Object-centric (NeRF Synthetic) | Medium - more uniform complexity |
| Large outdoor (Mega-NeRF) | Very high - huge scale variation |
| Thin structures (hair, foliage) | Very high - ADC over-splits in empty space |

## 8. Roadmap

### Phase 1: Simplified 3D Demo (this session)
- Isotropic Gaussians in numpy
- 3D density field reconstruction (no rendering)
- Validate principle extends to 3D

### Phase 2: Integration with gsplat
- Use gsplat (open-source 3DGS) as the rendering backend
- Implement Farey densification as a drop-in replacement for ADC
- Benchmark on NeRF Synthetic dataset (Blender scenes)

### Phase 3: Scaffold-GS Integration
- Fork Scaffold-GS codebase
- Implement the anchor-level Farey injection
- Benchmark on Mip-NeRF 360 and Tanks and Temples

### Phase 4: Paper Submission
- Target: CVPR 2026 or SIGGRAPH 2026
- Ablation studies, comparisons, analysis
