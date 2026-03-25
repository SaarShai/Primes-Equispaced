# Farey Mesh Refinement: Deep Dive into Real-World Scenarios

**Date:** 2026-03-25
**Honesty standard:** Each scenario rated GENUINE, SPECULATIVE, or NOT APPLICABLE.

---

## What We Actually Have (Our Proven Tools)

Before evaluating scenarios, here is exactly what our Farey refinement provides,
with proof status:

1. **Injection Principle** (Lean 4 proved, 0 sorry): When going from F_{N-1} to
   F_N, each gap between consecutive fractions receives AT MOST ONE new fraction.
   This holds for ALL N >= 2, not just primes.

2. **Mediant Property** (proved): Every newly inserted fraction is the mediant
   (a+c)/(b+d) of its two Farey neighbors a/b and c/b.

3. **Sub-gap Formula** (proved): When a gap of width 1/(qs) is split, the two
   resulting sub-gaps have widths 1/(qN) and 1/(sN), where q+s >= N.

4. **No cascading splits**: Because injection guarantees max 1 split per gap per
   refinement step, there is ZERO propagation. No element needs to be "fixed up"
   because its neighbor was split.

5. **Exact node positions**: All nodes are rational numbers a/b with known
   denominators. No floating-point ambiguity.

6. **Hierarchical structure**: The refinement sequence F_1, F_2, F_3, ... is
   strictly nested. Every node added at level N stays forever.

**What we do NOT have:**
- Any 2D/3D mesh generation algorithm (only 1D)
- Any error estimator that tells us WHERE to refine
- Any solver-coupled demonstration
- Any benchmark against industry-standard tools (GMSH, Triangle, TetGen)

---

## Scenario 1: Finite Element Analysis (FEA)

### 1a. Structural Engineering — Stress in a Beam

**The problem:** Solve the elasticity equations on a beam with load. The mesh
must capture stress concentrations at supports and load points.

**How standard methods work:**
- Start with a coarse mesh (maybe 100 elements)
- Solve, compute error estimator (e.g., Zienkiewicz-Zhu or residual-based)
- Mark elements with high error for refinement
- Refine those elements (bisection, red-green, or newest vertex)
- The critical challenge: refinement must maintain CONFORMITY (no hanging nodes)
  and SHAPE QUALITY (no degenerate elements)

**What Farey refinement offers (1D only):**
- For a 1D beam problem (bar under axial load), Farey refinement gives a mesh on
  [0, L] with provably no double-splits
- The sub-gap formula gives exact element sizes after refinement
- No conformity issue in 1D (there are no hanging nodes in 1D)

**The honest assessment:**
- In 1D, Farey refinement is a legitimate alternative to uniform or bisection
  refinement. BUT: 1D FEA problems are trivial. Nobody struggles with 1D mesh
  quality. The hard problems are 2D and 3D.
- The injection principle prevents cascading refinement, which IS a real problem
  in 2D/3D. But we have no proven 2D/3D extension.
- Standard bisection methods (Rivara's longest-edge bisection) already guarantee
  that all angles stay >= half the smallest initial angle. This is a STRONGER
  guarantee than anything we have for 2D.

**Verdict: GENUINE for 1D, SPECULATIVE for 2D/3D.**
The 1D benefit is real but trivial. The 2D/3D extension is where the value would
be, but it does not exist yet.

### 1b. CFD Mesh Around an Airfoil

**The problem:** Solve Navier-Stokes equations around an airfoil. Need extremely
fine mesh in the boundary layer (thin region near the surface) and coarse mesh
far away. The mesh must transition smoothly from fine to coarse.

**What standard methods provide:**
- Structured boundary-layer meshes with controlled growth ratios
- Unstructured triangular/tetrahedral meshes in the far field
- Delaunay refinement (Ruppert/Chew algorithms) guarantees minimum angles of
  ~26-30 degrees in the unstructured region
- Quadtree/octree methods handle the transition with 2:1 balancing rules

**What Farey refinement could offer:**
- In the structured direction (normal to the airfoil surface), a 1D Farey mesh
  could control growth ratios. Each refinement step adds at most one layer in
  each existing interval.
- The rational node positions might help with exact layer thickness specification

**The honest assessment:**
- CFD boundary layer meshing is inherently a 1D problem in the wall-normal
  direction, so Farey refinement IS applicable to that slice
- BUT: boundary layer meshes use GEOMETRIC growth ratios (each layer is r times
  thicker than the previous), not Farey-style number-theoretic spacing
- The Farey spacing (widths 1/(qs)) does not match the exponential growth that
  CFD solvers need near walls
- The real bottleneck in CFD meshing is the 2D/3D unstructured region, where
  we have nothing to offer

**Verdict: NOT APPLICABLE in practice.**
The spacing pattern of Farey fractions does not match what CFD solvers actually
need. Geometric growth ratios are fundamentally different from mediant-based
rational spacing.

### 1c. Thermal Analysis of a Heatsink

**The problem:** Solve the heat equation on a heatsink geometry. Need fine mesh
near fins and heat sources, coarse mesh in bulk material.

**Assessment:** Same as 1b. The geometry is 3D, the real challenge is meshing
complex fin geometries, and Farey refinement addresses none of these challenges.

**Verdict: NOT APPLICABLE.**

### 1d. How Mesh Quality Affects Solution Accuracy

**Key facts from the literature:**
- Condition number of the stiffness matrix scales as O(h^{-2}) where h is the
  mesh size parameter. Poorly shaped elements make this worse.
- In 1D, ALL elements are intervals -- there is no "shape quality" concern.
  The only metric is the size ratio between the largest and smallest elements.
- Farey meshes have a max size ratio that grows with N (the largest gap in F_N
  is ~1/N while the smallest is ~1/N^2), giving a ratio of ~N.
- Uniform meshes have ratio = 1 (perfect).
- So for 1D: uniform mesh BEATS Farey mesh on element quality.

**The Farey advantage in 1D is not element quality -- it is REFINEMENT quality.**
The guarantee is about the PROCESS of refining, not the final mesh shape.

**Verdict: GENUINE distinction, but the advantage is narrow.**

---

## Scenario 2: Adaptive Mesh Refinement (AMR)

### 2a. Current Methods and Their Cascading Problem

**h-refinement** (making elements smaller):
- Bisection: split one element into two. In 2D/3D, this creates hanging nodes
  that must be resolved by splitting neighbors. This is "cascading refinement."
- Red-green refinement: "Red" splits create 4 sub-triangles. Neighbors that
  share a split edge need "green" closure (2 sub-triangles). Green elements have
  worse quality. If green elements are later marked for refinement, they must be
  "ungreened" first.
- Newest vertex bisection: avoids some cascading by choosing the split edge
  consistently, but still requires closure operations.

**The cascading problem in detail:**
When you split element A, its neighbor B now has a hanging node on their shared
edge. So B must be split too. But splitting B might create a hanging node on B's
other neighbor C. And so on. In the worst case, a single marked element triggers
O(log n) cascading splits.

**What Farey refinement guarantees:**
- In 1D: ZERO cascading. Each gap gets at most 1 new node. Period.
- This is because the Farey property q+s >= N for consecutive denominators q, s
  in F_{N-1} ensures that the gap width 1/(qs) is too small to fit two new
  fractions with denominator N.

**The honest comparison:**
- Newest vertex bisection in 2D also has bounded cascading: at most O(1)
  additional splits per marked element (amortized). The constant depends on the
  initial mesh but is typically small.
- The Farey guarantee of EXACTLY ZERO cascading is stronger than existing 2D
  bounds, but it only applies in 1D.
- In 2D, a tensor-product Farey mesh (F_N x F_N grid) would have zero cascading
  per axis, but this only works on rectangular domains.

**Verdict: GENUINE advantage in 1D. Would be a genuine advantage in 2D/3D IF
the extension existed and worked on non-rectangular domains.**

### 2b. WHERE to Refine and HOW MUCH

**Current error estimators:**
- Residual-based: compute the PDE residual on each element
- Recovery-based (Zienkiewicz-Zhu): compare the computed gradient to a smoothed
  gradient
- Goal-oriented: estimate error in a specific output quantity
- All of these tell you WHICH elements to refine

**What Farey refinement says about WHERE:**
- Nothing. The injection principle does not tell you where to refine.
- Farey refinement is a GLOBAL operation: going from F_{N-1} to F_N adds phi(N)
  new nodes everywhere. You cannot selectively refine only one region.
- This is a FUNDAMENTAL limitation for adaptive methods.

**Possible workaround:** Use Farey-style local refinement by inserting mediants
only in marked gaps. This preserves the no-double-split property locally. But
this is just "insert the mediant of neighbors" -- which is essentially what
newest vertex bisection already does in 1D.

**Verdict: NOT APPLICABLE for adaptive refinement in its current form.**
The global nature of F_N -> F_{N+1} makes it useless for local adaptivity.
A local mediant-insertion variant might work but is not novel.

### 2c. Compare: Quadtree/Octree vs Farey

**Quadtree/octree refinement:**
- Recursive subdivision of squares/cubes into 4/8 children
- 2:1 balancing rule: neighbors can differ by at most one refinement level
- Handles complex geometry via cut-cells at boundaries
- Highly parallelizable (p4est library scales to millions of cores)
- Elements are axis-aligned rectangles/cubes -- not ideal for curved boundaries

**Farey refinement (1D):**
- Adds nodes at specific rational positions
- No balancing rule needed (injection handles it automatically)
- Cannot handle geometry at all (only works on intervals)

**The comparison is not meaningful.** Quadtree/octree is a 2D/3D spatial
subdivision method. Farey refinement is a 1D interval subdivision. They solve
different problems at different scales. Comparing them would be like comparing
a bicycle to a cargo ship.

**Verdict: NOT APPLICABLE. Different categories entirely.**

---

## Scenario 3: 3D Extension

### 3a. Tensor Product Extension to 2D/3D

**The idea:** Take a Farey mesh F_N on [0,1] and form the tensor product
F_N x F_N on [0,1]^2. This gives a rectangular grid where each axis has
Farey-spaced nodes.

**What this provides:**
- Refinement from (F_N x F_N) to (F_{N+1} x F_{N+1}) has a controlled
  splitting pattern: each rectangle can gain at most 1 new node in each
  direction, so it splits into at most 4 sub-rectangles.
- Actually, the tensor product of "at most 1 split per axis" means each
  rectangle can be split into 1, 2, or 4 sub-rectangles -- never more.
- All node positions are exact rationals (a/b, c/d).

**Limitations:**
- ONLY works on rectangular domains [0,1]^2 or [0,1]^3
- Cannot handle L-shaped domains, circular domains, or any non-rectangular
  geometry without coordinate transformation
- Produces rectangular elements only. Triangular/tetrahedral elements (which are
  needed for complex geometry) are not addressed.
- The mesh is uniform in structure even though the spacing varies -- no local
  adaptivity.

**Verdict: GENUINE but extremely limited.**
Works on rectangular domains. Useless for real-world geometry.

### 3b. Delaunay vs Farey in 2D Triangulation

**Delaunay triangulation guarantees:**
- Maximizes the minimum angle among all possible triangulations of the same
  point set (the "max-min angle" property)
- Ruppert's algorithm: guaranteed minimum angle of ~26.5 degrees
- Chew's second algorithm: guaranteed minimum angle of ~30 degrees
- Both produce size-graded meshes that are near-optimal in element count

**Farey in 2D:**
- We have no 2D Farey triangulation algorithm
- If we placed Farey nodes (a/b, c/d) in 2D and then ran Delaunay triangulation
  on them, we would get a Delaunay mesh -- but the node placement is from Farey,
  not from an error estimator
- The node distribution would be denser near (0,0) and (1,1) due to the
  concentration of Farey fractions with small denominators near 0 and 1

**Verdict: SPECULATIVE.**
No 2D Farey triangulation exists. Using Farey nodes with Delaunay connectivity
is possible but offers no clear advantage over standard Delaunay refinement.

### 3c. Tetrahedral Meshes in 3D

**Existing quality guarantees:**
- TetGen uses Delaunay-based algorithms with radius-edge ratio bounds
- CGAL provides Delaunay refinement with user-specified quality criteria
- The theoretical guarantees are weaker than in 2D (no equivalent of the 30-degree
  angle bound in general)

**Farey contribution:** None. We have no 3D algorithm.

**Verdict: NOT APPLICABLE.**

---

## Scenario 4: Specific Test Problem Comparisons

### 4a. L-shaped Domain

**The problem:** Solve -Laplacian(u) = f on an L-shaped domain. The solution has
a singularity at the re-entrant corner (the inside corner of the L). The mesh
must be extremely fine near this corner and can be coarse elsewhere.

**Why Farey refinement fails here:**
- The L-shaped domain is not rectangular, so tensor-product Farey meshes do not
  apply directly
- The singularity requires LOCAL refinement near one point. Farey refinement is
  GLOBAL.
- Standard graded meshes use geometric refinement toward the corner, with element
  sizes proportional to r^alpha where r is the distance from the corner. Farey
  spacing (rationals with bounded denominators) does not produce this geometric
  grading.

**Verdict: NOT APPLICABLE.**

### 4b. Crack Tip

**The problem:** Model stress intensity at a crack tip in fracture mechanics.
Similar to the L-shaped domain: singularity at the crack tip requires intense
local refinement.

**Same issues as 4a.** The crack tip is a point singularity requiring geometric
grading. Farey refinement produces number-theoretic spacing, not geometric
grading.

**Verdict: NOT APPLICABLE.**

### 4c. Where a Fair 1D Comparison WOULD Work

**A good test case:** 1D Poisson equation -u'' = f on [0,1] with a solution
that has multiple scales (e.g., f(x) = sin(100*pi*x) + 10*sin(2*pi*x)).

**What we could compare:**
- Mesh A: Farey nodes F_N for various N
- Mesh B: Same number of uniformly spaced nodes
- Mesh C: Same number of nodes placed at Chebyshev points
- Mesh D: Adaptive bisection guided by an error estimator

**Expected results (honest prediction):**
- For smooth f: uniform and Chebyshev will likely beat Farey, because Farey
  concentrates nodes near 0 and 1 (small-denominator fractions cluster there)
  while the error is distributed across the domain
- For f with rational-frequency structure: Farey MIGHT have an advantage because
  its nodes align with the function's natural frequencies
- Adaptive bisection will beat everything because it puts nodes where the error
  actually is

**The Farey advantage would appear in:**
- Measuring refinement COST (how many elements are affected per refinement step)
- Measuring refinement PREDICTABILITY (exact sub-element sizes are known a priori)
- NOT in final solution accuracy for a given node count

**Verdict: GENUINE comparison possible in 1D, but Farey likely loses on accuracy
and wins only on refinement-process properties.**

---

## Scenario 5: Game Development / Real-Time Graphics

### 5a. Level-of-Detail (LOD) Mesh Generation

**How LOD works in practice:**
- Pre-generate multiple mesh resolutions of a 3D model (e.g., 10K, 5K, 1K, 200
  triangles)
- Switch between them based on camera distance
- The hard problem: avoiding "popping" (visible transitions)
- Solutions: cross-fading, geomorphing, continuous LOD (CLOD)

**What Farey refinement could offer:**
- A nested sequence of 1D meshes (F_1 subset F_2 subset F_3 ...)
- Perfect nesting means transitions are smooth: going from LOD level N to N+1
  only ADDS nodes, never moves existing ones
- The injection guarantee means the visual change per LOD step is bounded

**The honest assessment:**
- LOD is fundamentally a 3D surface problem. Our 1D tool does not apply directly.
- The nested property IS valuable for LOD, but uniform subdivision (catmull-clark,
  loop subdivision) already provides perfect nesting in 3D.
- Modern GPU-driven LOD (Nanite in Unreal Engine 5) uses cluster-based LOD that
  is fundamentally different from node-based refinement.
- For terrain heightmaps (which ARE a 1D-parameter family over a 2D grid), Farey
  refinement along each axis might provide controlled LOD. But terrain LOD
  already works well with quadtree-based methods (CDLOD, geoclipmaps).

**Verdict: SPECULATIVE.**
The nesting property is genuinely useful for LOD, but existing methods already
achieve it in 3D. No practical advantage demonstrated.

### 5b. Terrain Rendering

**How terrain LOD works:**
- Terrain is a heightmap: a 2D grid where each cell has a height value
- LOD is achieved by using coarser grids for distant terrain
- The hard problem: stitching different LOD levels together without cracks
- Standard solution: T-junction removal, skirt geometry, or continuous morph

**What Farey refinement could offer:**
- A 2D tensor-product Farey grid for the terrain
- Transitions between LOD levels that provably introduce at most 1 new vertex
  per existing edge (no multi-splits)
- Exact rational vertex positions that eliminate floating-point stitching errors

**The honest assessment:**
- Terrain LOD is already a well-solved problem. Quadtree-based methods (CDLOD,
  geoclipmaps) handle it efficiently with GPU instancing.
- The "at most 1 split per edge" property would prevent T-junctions, which IS
  genuinely useful -- but the standard "restricted quadtree" already achieves
  this with the 2:1 balancing rule.
- The exact rational positions are a theoretical nicety but not practically
  important because terrain data (heightmaps) is already discretized.

**Verdict: MARGINAL.**
The no-multi-split property is genuinely relevant to terrain stitching, but
existing methods (2:1 balanced quadtrees) already solve this. Farey refinement
does not offer enough improvement to justify changing established pipelines.

### 5c. Could Farey Give Smoother LOD Transitions?

**The argument for:**
- Farey refinement inserts mediants, which are the "most natural" midpoints
  between two fractions (in the sense of the Stern-Brocot tree)
- The mediant a+c)/(b+d) is the simplest fraction between a/b and c/d
- This might produce visually smoother transitions than arbitrary midpoint
  insertion

**The argument against:**
- "Visually smooth" for LOD is about vertex positions in 3D space, not about
  rational number properties of parameter coordinates
- The visual quality depends on surface normal continuity, which Farey refinement
  says nothing about
- Subdivision surfaces (Catmull-Clark, Loop) are specifically designed for
  smooth visual quality and have rigorous smoothness guarantees (C1 or C2
  continuity at regular vertices)

**Verdict: SPECULATIVE.**
No evidence that Farey mediants produce visually smoother results than standard
midpoint insertion or subdivision.

---

## Summary Table

| Scenario | Genuine? | Our Advantage | Existing Competition |
|----------|----------|---------------|---------------------|
| 1D FEA | GENUINE but trivial | Zero cascading refinement | Bisection (also trivial in 1D) |
| CFD airfoil | NOT APPLICABLE | None | Boundary layer meshing, Delaunay |
| Thermal heatsink | NOT APPLICABLE | None | 3D tetrahedral meshing |
| AMR cascading | GENUINE (1D only) | Provably zero propagation | Newest vertex bisection (O(1) amortized) |
| AMR adaptivity | NOT APPLICABLE | Nothing (global refinement) | Error estimators + local refinement |
| Quadtree comparison | NOT APPLICABLE | Different categories | Quadtree/octree (2D/3D) |
| 2D tensor product | GENUINE but limited | Bounded splits per rectangle | Works only on rectangles |
| 2D Delaunay vs Farey | SPECULATIVE | No 2D algorithm exists | Ruppert/Chew (30-degree guarantee) |
| 3D tetrahedra | NOT APPLICABLE | Nothing | TetGen, CGAL |
| L-shaped domain | NOT APPLICABLE | Wrong spacing pattern | Graded meshes |
| Crack tip | NOT APPLICABLE | Wrong spacing pattern | Geometric grading |
| Game LOD | SPECULATIVE | Nesting property | Subdivision surfaces, Nanite |
| Terrain rendering | MARGINAL | No multi-split | 2:1 balanced quadtrees |
| Smooth LOD transitions | SPECULATIVE | No evidence | Catmull-Clark, Loop subdivision |

---

## Where the GENUINE Value Lives

After this deep dive, here is an honest assessment of where Farey-based mesh
refinement has real, demonstrable value:

### The One Genuine Niche: Provably Bounded Refinement in 1D

**The claim we CAN make:**
When refining a 1D mesh by going from Farey order N-1 to N, EVERY existing
element receives at most one new node. This is proven in Lean 4 with zero sorry.
No existing 1D refinement method makes this exact guarantee as a theorem
(though bisection in 1D trivially satisfies it too -- you only split one element
at a time).

**Why it matters (slightly):**
- For time-stepping methods where the mesh evolves over time, knowing that each
  step introduces at most one split per element means the CFL condition (which
  constrains the time step based on the smallest element) degrades predictably
- The exact sub-gap formula gives CLOSED-FORM element sizes after refinement,
  which no other method provides
- For pedagogical purposes, Farey refinement is a beautiful illustration of how
  number theory connects to numerical methods

### The Potential Value That Does Not Yet Exist: 2D/3D Extension

If someone could extend the injection principle to 2D triangulations or 3D
tetrahedralizations, THAT would be genuinely valuable:
- Zero-cascading refinement in 2D/3D would eliminate the need for closure
  algorithms (red-green, newest vertex bisection)
- Closed-form element quality bounds after refinement would simplify error
  estimation
- But this extension is a major open problem, not something we have

### What We Should NOT Claim

- That Farey refinement produces better meshes than existing methods (it does
  not, in any demonstrated scenario)
- That the injection principle solves the cascading problem in 2D/3D (it only
  works in 1D)
- That tensor-product Farey meshes are useful for real geometry (they only work
  on rectangles)
- That Farey refinement helps with LOD or game graphics (existing methods are
  far ahead)

---

## Recommended Next Steps (If Pursuing This Direction)

1. **Build a real 1D FEM comparison:** Solve -u'' = f on [0,1] with Farey nodes
   vs uniform vs Chebyshev vs adaptive. Measure L2 error, H1 error, condition
   number. Publish the actual numbers.

2. **Investigate local Farey refinement:** Instead of going F_N -> F_{N+1}
   globally, insert mediants only in marked elements. Does the injection
   principle still hold locally? (It should, since the mediant property is local.)

3. **Study the 2D extension seriously:** Can the injection principle be proved
   for 2D Farey-type triangulations? The Farey graph (where vertices are Farey
   fractions and edges connect neighbors) IS a triangulation of the hyperbolic
   plane. Can this be projected to a planar triangulation with quality guarantees?

4. **Find the right function class:** Our QMC work suggests Farey nodes are good
   for functions with multiplicative/rational-frequency structure. Identify what
   PDE solutions have this structure and benchmark there.

---

## Sources

- Rivara, M.C. "Algorithms for refining triangular grids suitable for adaptive
  and multigrid techniques." Int. J. Numer. Methods Eng. (1984)
- Ruppert, J. "A Delaunay refinement algorithm for quality 2-dimensional mesh
  generation." J. Algorithms (1995)
- Shewchuk, J.R. "Delaunay refinement algorithms for triangular mesh generation."
  Computational Geometry (2002)
- Long Chen. "Adaptive Finite Element Methods." (UCI lecture notes)
- Burstedde, C. et al. "p4est: Scalable algorithms for parallel adaptive mesh
  refinement on forests of octrees." SIAM J. Sci. Comput. (2011)
- COMSOL documentation on mesh refinement techniques
- Unity documentation on LOD mesh transitions
