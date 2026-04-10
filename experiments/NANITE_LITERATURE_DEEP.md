The problem of "cluster boundary artifacts"—commonly manifesting as cracks, T-junctions, or "popping" at the seams of different Level of Detail (LOD) transitions—is a fundamental challenge in geometry processing. As rendering shifts from discrete LOD (swapping whole meshes) to continuous, cluster-based streaming (Nanite-style), the complexity of this problem has increased.

Here is a survey of the literature and the approaches used to solve the border vertex problem.

---

### 1. Solutions to the Border Vertex Problem

The "border vertex problem" occurs when the vertices of a high-detail cluster do not align with the vertices of a low-detail neighbor, creating gaps (cracks) or overlapping geometry.

#### A. Constraint-Based Simplification (The Classical Approach)
*   **Garland-Heckbert (1997) & Hoppe (1996):** In the context of Quadric Error Metrics (QEM), the standard solution is **Boundary Preservation Constraints**. When performing edge collapses, the algorithm identifies "boundary edges" (edges belonging to only one face). To prevent cracks, these edges are assigned a high-weight penalty (or "virtual" quadrics) that prevents them from moving or collapsing in a way that deviates from the original boundary.
*   **Attribute-Aware Constraints (Meshoptimizer):** Kapoulkine’s work emphasizes that boundaries aren''t just geometric; they are topological (UV seams, material boundaries). The solution here is to treat any edge with a discontinuity in attributes as a "hard" boundary, preventing any collapse that would merge two different attribute values, thus maintaining the "watertightness" of the seam.

#### B. The Stitching/Degenerate Triangle Approach (The Nanite Approach)
*   **Nanite (Karis, 2021) & "Recreating Nanite":** Nanite does not attempt to prevent the mismatch between cluster levels; instead, it **manages the mismatch through geometry injection**. 
*   When a cluster is subdivided, the boundaries of the new children may not match the parent. Nanite handles this using **"Stitching Triangles" or "Degenerate Triangles."** As the hierarchy is traversed, the renderer can inject zero-area or highly elongated triangles that bridge the gap between a high-resolution child and a low-resolution neighbor. 
*   Furthermore, Nanite uses a **visibility-buffer (V-Buffer) approach** where the error metric is calculated in screen space. By ensuring the error (deviation from the original mesh) is bounded by a sub-pixel threshold, the "cracks" become smaller than a pixel, making them visually imperceptible.

#### C. The Transvoxel/Voxel Approach
*   In terrain LOD (often associated with the *Transvoxel Algorithm* by Eric Lengyel), the solution is the creation of **transition layers**. This involves generating a specific set of intermediate geometry (transition meshes) that topologically connects a high-resolution voxel grid to a lower-resolution one, effectively "shaving" the edges of the high-res cells to meet the low-res ones.

---

### 2. Number-Theoretic and Denominator-Based Hierarchies

Your intuition regarding "denominator-based" hierarchies is highly relevant to how modern spatial data structures function.

While "number-theoretic" is a rare term in standard mesh literature, the concept of **Dyadic Decompositions** (using denominators of $2^n$) is the backbone of all modern hierarchical LOD.

*   **Dyadic/Quadtree/Octree Structures:** All the papers mentioned (Nanite, Meshoptimizer) rely on a hierarchy where each level of detail represents a scale of $1/2^n$ of the original mesh. This is a "denominator-based" approach where the precision of the vertex position is defined by the depth of the tree.

*   **Morton Encoding (Z-order curves):** This is the closest link to number theory. By using bit-interleaving (an integer-based approach), meshes are mapped to a 1D space that preserves spatial locality. This allows the "clustering" to be done using simple integer arithmetic rather than expensive floating-point spatial searches. 
*   **The "Denominator" logic:** In Nanite, the cluster hierarchy is essentially a **Spatial DAG (Directed Acyclic Graph)**. The "denominator" is implicit in the refinement level: a cluster at level $k$ represents a geometric area with a precision error proportional to $1/2^k$. The "border problem" is solved by ensuring that the error metric $\epsilon$ is consistent across the boundary, effectively treating the boundary as a shared "denominator" across adjacent clusters.

---

### 3. State of the Art (as of 2025)

As of 2025, the industry has moved away from "LOD" as a discrete concept and toward **"Continuous Geometry Streaming."**

**Key SOTA Characteristics:**

1.  **Micro-polygon Micro-streaming:** We are no longer "swapping meshes." The SOTA (exemplified by Unreal Engine 5's evolution and beyond) involves a **Visibility Buffer (V-Buffer)** architecture. The geometry is stored in a highly compressed, hierarchical format (like Nanite) where the "LOD" is a real-time, per-pixel decision made during the rasterization of clusters.
2.  **Neural Geometry Integration:** The frontier involves **Neural Radiance Fields (NeRFs) and 3D Gaussian Splatting (3DGS)** being integrated with traditional polygonal meshes. The SOTA approach is "Hybrid Rendering": using Nanite-style clusters for opaque, large-scale structural geometry and Gaussian Splatting for complex, volumetric, or thin-surface details (like hair or foliage) that are too difficult to "stitch" using triangles.
3.  **Attribute-Agnostic Error Metrics:** Recent research focuses on error metrics that are not just distance-based (QEM) but **perceptual-based**. Using machine learning, the error metric now accounts for how the human eye perceives "cracks" under specific lighting conditions, allowing for even more aggressive simplification of boundaries.
4.  **Hardware-Accelerated Topology:** Modern GPUs are being designed with primitives that allow for more efficient handling of the "degenerate triangles" used in stitching, reducing the overhead that previously made the Nanite-style stitching approach expensive.

**Summary Table**

| Approach | Core Strategy | Primary Limitation |
| :--- | :--- | :--- |
| **Classical (QEM)** | Constraint/Penalty on edges | High computational cost for real-time updates |
| **Nanite-style** | Degenerate stitching/Sub-pixel error | Requires massive bandwidth/V-Buffer architecture |
| **Transvoxel** | Transition geometry layers | Complexity in managing "triple" intersections |
| **SOTA (2025)** | Hybrid Mesh/Gaussian/Neural | Extremely complex memory/streaming management |
