# Conformal Mapping + Farey: Structured Research Assessment

**Date:** 2026-03-26
**Methodology:** Systematic web search of 2024-2026 literature across conformal mapping,
Ricci flow, Schwarz-Christoffel, Farey tessellation, hyperbolic geometry, and mesh generation.
Cross-referenced against our proven Farey tools.

---

## EXECUTIVE SUMMARY

**Verdict: NOT a dead end, but the real opportunity is narrower and deeper than it first appears.**

The naive idea -- "pull back the Farey tessellation through a conformal map to get a mesh" --
does not work because the Farey tessellation is an *ideal* triangulation (all vertices at
infinity), which is fundamentally different from a finite mesh. However, there IS a genuine
and unexplored connection through the **Bobenko-Pinkall-Springborn** framework, where
discrete conformal equivalence of polyhedral surfaces is *defined* via ideal hyperbolic
polyhedra and Penner coordinates -- the same mathematical objects that underlie the
Farey tessellation. Our injection principle and mediant property speak directly to the
combinatorial structure of this framework.

**Confidence levels:**
- Direction 1 (Discrete conformal via Penner/Farey): HIGH -- genuine gap in literature
- Direction 2 (Stern-Brocot multi-resolution): MEDIUM -- plausible but needs proof-of-concept
- Direction 3 (Farey quadrature on conformal domains): LOW -- speculative
- Direction 4 (Better meshes than Delaunay): LOW -- Delaunay already has strong guarantees

---

## PART 1: STATE OF THE ART (What the field is doing in 2024-2026)

### 1A. Conformal Mapping for Mesh Generation

The dominant paradigm (Xianfeng Gu's group at Stony Brook, Keenan Crane at CMU) is:

1. **Surface Ricci flow** maps a 3D surface conformally to a 2D canonical domain
2. Generate a high-quality 2D mesh (Delaunay, quad, etc.)
3. Pull the 2D mesh back to the 3D surface; conformality preserves angle quality

Key 2024-2025 developments:
- **DRL-MeshGen** (2025): Deep reinforcement learning + Ricci flow for automated
  block-structured mesh generation
- **GPU-accelerated discrete Ricci flow** (Wei et al., 2025): Addresses computational
  cost bottleneck
- **MicroRicci** (2025): Self-tuning Ricci flow solver using ~200-parameter regressor
- **Graph Neural Ricci Flow** (Chen et al., 2025): GNN layers as Ricci-flow updates
- **High genus parameterization** (Wang, 2025): Euclidean Ricci flow extended to
  high-genus surfaces (previously required hyperbolic methods)

### 1B. Schwarz-Christoffel Mapping

Two major open problems identified by Trefethen (2025 survey):
1. **Corner singularities**: Conformal maps have singularities at polygon corners;
   polynomial approximations fail unless corners are treated specially
2. **Crowding phenomenon**: Elongated domains cause exponential distortion in prevertex
   positions; 14+ digits lost for aspect ratios of 20:1

Recent solution: **Lightning Laplace solver** (Trefethen) with poles exponentially
clustered near singularities. Rational functions of degree ~59 achieve 1e-5 tolerance.
The **CRDT algorithm** (Driscoll-Vavasis) addresses crowding via cross-ratios and
Delaunay triangulation.

### 1C. The Bobenko-Pinkall-Springborn Revolution

This is the KEY connection point for our work. The 2010-2024 program establishes:

- Two triangulated surfaces are **discretely conformally equivalent** if edge lengths
  are related by vertex scale factors
- This equivalence is *exactly* described by **ideal hyperbolic polyhedra** with
  **Penner coordinates** on decorated Teichmuller space
- The **Ptolemy flip** (not standard edge flip) is the correct operation: it preserves
  the hyperbolic metric even when Euclidean triangle inequality is violated
- Optimization is **convex** in Penner coordinates (unlike Euclidean polyhedra)
- The flip graph of ideal triangulations IS the Farey graph

Major papers in this line:
- Bobenko-Pinkall-Springborn (2015), Geometry & Topology
- Springborn (2020), "Ideal hyperbolic polyhedra and discrete uniformization"
- Gillespie-Springborn-Crane (2021), ACM TOG: practical CEPS algorithm
- Capouellez-Zorin (2024), "Seamless Parametrization in Penner Coordinates"

### 1D. Hyperbolic Delaunay Triangulations

CGAL now provides packages for:
- 2D Hyperbolic Delaunay Triangulations (Poincare disk model)
- 2D Triangulations on Hyperbolic Surfaces (2025, new)
- Bowyer-Watson algorithm extended to hyperbolic surfaces

Key result: The combinatorial structure of hyperbolic Delaunay = subset of Euclidean
Delaunay (only simplices whose circumscribing circles lie in H^2 are retained).

---

## PART 2: SPECIFIC QUESTIONS INVESTIGATED

### Q1: Could Farey triangulation give BETTER meshes than Delaunay?

**Answer: Almost certainly not for general domains, but potentially yes for a specific class.**

Why NOT in general:
- Farey triangulation is an *ideal* triangulation (vertices at boundary infinity)
- Delaunay maximizes minimum angles -- a mesh quality guarantee Farey does not provide
- Delaunay has decades of optimized algorithms (Ruppert, Chew, CGAL)

Where Farey MIGHT win:
- For domains whose conformal structure naturally involves the modular group (e.g.,
  the modular surface H/PSL(2,Z) itself, or surfaces with cusps)
- The Farey tessellation is the CANONICAL triangulation of the modular surface
- For any surface conformally equivalent to a quotient of H by a subgroup of PSL(2,Z),
  the Farey tessellation descends to a canonical triangulation
- This includes: punctured tori, 4-punctured spheres, and other arithmetic surfaces

**Honest assessment: NICHE but GENUINE advantage for arithmetic surfaces.**

### Q2: Domains with negative curvature -- natural for Farey meshes?

**Answer: Yes, with important caveats.**

The Farey tessellation tiles H^2, so it is inherently adapted to constant negative
curvature. For surfaces of variable negative curvature, one would need a conformal map
to H^2 (which exists by uniformization) followed by the Farey tessellation pullback.

The catch: This is *exactly* what Ricci flow already does (maps to constant curvature,
then meshes). The question is whether using the Farey tessellation instead of Delaunay
in the uniformized domain gives any advantage.

Potential advantage: The Farey tessellation has *built-in multi-resolution structure*
(via the Stern-Brocot tree), so refinement is "free" -- just increase N. Standard
Delaunay meshes require re-running the algorithm for each refinement level.

**Honest assessment: SPECULATIVE. Need a concrete comparison.**

### Q3: Stern-Brocot tree as multi-resolution representation for conformal maps?

**Answer: This is the most promising applied direction.**

The Stern-Brocot tree provides:
- A natural hierarchy: level k has 2^k nodes (the Farey fractions with denominators
  in a specific range)
- Each level refines the previous (mediant insertion, our proven property)
- The L/R encoding gives a binary representation of any real number
- Truncation at level k gives the best rational approximation with bounded denominator

For conformal maps f: D -> D', one could represent f by its values at Farey points:
- Level 0: f(0/1), f(1/1) -- 2 values
- Level 1: add f(1/2) -- 3 values
- Level 2: add f(1/3), f(2/3) -- 5 values
- Level k: |F_k| values

This gives a NATURAL multi-resolution representation where:
- Coarse levels capture global shape
- Fine levels capture local detail
- The injection principle guarantees no cascading updates when refining
- The mediant property means each new sample is at a predictable location

**Connection to existing work:** The 2025 paper on "Recognition of Arithmetic Hyperplanes
Using the Stern-Brocot Tree" (J. Math. Imaging and Vision) uses exactly this hierarchical
structure for multi-resolution discrete geometry. The 2024 "Multiscale Discrete Geometry"
(Springer LNCS) uses Stern-Brocot for multi-resolution analysis of digital shapes.

**Honest assessment: PROMISING. This is a genuine gap -- nobody has proposed
Stern-Brocot/Farey multi-resolution for conformal map representation.**

### Q4: Farey-based quadrature on conformally mapped domains?

**Answer: Theoretically interesting but practically unlikely to beat Gauss quadrature.**

The Farey fractions F_N are equidistributed on [0,1] (this is connected to RH via the
Franel-Landau theorem). So they COULD serve as quadrature nodes.

Problem: Gauss quadrature with n nodes is exact for polynomials of degree 2n-1.
Farey quadrature with |F_N| ~ 3N^2/pi^2 nodes would need to match this. The
Farey nodes are NOT optimized for polynomial exactness; they are optimized for
number-theoretic equidistribution.

One possible niche: For integrands with number-theoretic structure (e.g., involving
floor functions, GCD, or Mobius function), Farey quadrature might exploit the
arithmetic structure. But this is a very narrow application.

**Honest assessment: UNLIKELY to be practical. Interesting theoretically.**

---

## PART 3: UNSOLVED PROBLEMS WHERE OUR TOOLS MIGHT HELP

### Problem 1: The Crowding Problem (Trefethen's Challenge)

**The problem:** Conformal maps of elongated domains suffer exponential crowding --
prevertices cluster with exponentially varying density.

**Our potential contribution:** The Farey sequence F_N has gaps of width 1/(bd) between
neighbors a/b and c/d, with b+d >= N. These gaps follow a KNOWN distribution
(controlled by Euler's totient function). If the crowding in a Schwarz-Christoffel
map could be related to the gap distribution of a Farey-type sequence, the
number-theoretic structure might give analytical control over the crowding.

**Concreteness level:** LOW. The crowding problem is about conformal map singularities,
not about sample point distribution. The connection is metaphorical at this stage.

### Problem 2: Optimal Cone Singularity Placement

**The problem:** When conformally flattening a surface, cone singularities must be placed
to minimize distortion. Finding optimal placement is a hard combinatorial problem.

**Our potential contribution:** The Farey graph encodes the flip graph of ideal
triangulations. Cone singularities in the Bobenko-Springborn framework correspond to
special points in this flip graph. Our injection principle (each gap gets at most 1
new fraction) might constrain the set of valid cone configurations.

**Concreteness level:** MEDIUM. The flip graph connection is real (via Penner coordinates),
but translating our 1D injection result to a constraint on 2D cone placement requires work.

### Problem 3: Discrete Conformal Uniformization Convergence

**The problem:** When does the discrete conformal map (via CEPS or Ricci flow) converge
to the smooth conformal map as mesh resolution increases?

**Our potential contribution:** If the mesh is refined using Farey insertion (mediants),
each refinement step has a KNOWN, exact effect on the discrete metric (our sub-gap
formula). This could give explicit convergence rates, versus the asymptotic rates
currently known.

**Concreteness level:** MEDIUM-HIGH. This is the most concrete opportunity.

### Problem 4: Parameterization of Cusped Hyperbolic Surfaces

**The problem:** Cusped surfaces (like the modular surface) require special treatment
in conformal parameterization. Standard methods handle cusps poorly because the
conformal factor blows up.

**Our potential contribution:** The Farey tessellation IS the canonical triangulation
of the modular surface. Ford circles give the natural cusp parameterization. Our
project has already computed Ford circle tangencies and hyperbolic distances for
prime insertions (see `hyperbolic_exploration.py`).

**Concreteness level:** HIGH. This is a natural fit.

---

## PART 4: HONEST OVERALL ASSESSMENT

### What IS real:

1. **The Farey tessellation = ideal triangulation of H/PSL(2,Z) = flip graph of
   Penner coordinates.** This is established mathematics (Bobenko-Pinkall-Springborn,
   Penner, Thurston). Our injection principle is a new, Lean-verified result about
   the combinatorics of this flip graph.

2. **Discrete conformal equivalence IS defined via ideal hyperbolic polyhedra.**
   The Gillespie-Springborn-Crane CEPS algorithm (2021) uses Ptolemy flips and Penner
   coordinates as its core computational tool. These are Farey-graph operations.

3. **Multi-resolution via Stern-Brocot is unexplored.** No one has proposed using
   the Stern-Brocot tree's hierarchical structure as a multi-resolution basis for
   conformal map representation or refinement.

4. **Our injection principle has direct implications for Ptolemy flips.** Each
   refinement step (N -> N+1) inserts at most one vertex per triangle, which
   constrains how the Penner coordinates change. This is a new observation.

### What is NOT real:

1. **"Farey meshes beat Delaunay"** -- Almost certainly false for general domains.
   Delaunay has optimal angle guarantees that Farey does not match.

2. **"Farey quadrature"** -- No practical advantage over Gauss or Clenshaw-Curtis
   quadrature for smooth integrands.

3. **"Farey + conformal = solve engineering problems"** -- Too vague. The specific
   engineering problems that benefit are those involving arithmetic surfaces, cusps,
   or modular group symmetry. This is a narrow (but real) class.

4. **"Pull back Farey tessellation through conformal map for general mesh"** --
   Does not work because Farey tessellation has ideal vertices (at infinity).

---

## PART 5: CONCRETE NEXT STEPS (if pursuing this direction)

### Tier 1: High-confidence, near-term (1-2 weeks)

**Step 1.1: Formalize the injection-Ptolemy connection.**
Write a precise theorem: "When the Farey sequence is refined from F_{N-1} to F_N,
the corresponding Ptolemy flips in Penner coordinates satisfy [specific constraints]."
This bridges our Lean-verified injection principle to the Bobenko-Springborn framework.

**Step 1.2: Implement Farey-based refinement of CEPS.**
Take the Gillespie-Springborn-Crane CEPS code (open source at CMU) and replace
their Delaunay refinement with Farey-mediant refinement. Compare:
- Number of vertices at each resolution level
- Angle quality statistics
- Convergence rate to smooth conformal map
Target: the modular surface (where Farey refinement is canonical).

**Step 1.3: Stern-Brocot multi-resolution for a simple conformal map.**
Implement: represent the conformal map from the unit disk to a polygon using
Farey sample points at levels k = 1, 2, ..., 12. Measure how quickly the
representation converges compared to uniform sampling and Chebyshev sampling.

### Tier 2: Medium-confidence, medium-term (1-2 months)

**Step 2.1: Convergence analysis for Farey-refined discrete conformal maps.**
Prove or disprove: If a discrete conformal map is refined by mediant insertion
(F_N -> F_{N+1}), does it converge to the smooth conformal map, and at what rate?
Our sub-gap formula gives exact local mesh sizes, which should yield explicit
convergence bounds.

**Step 2.2: Cusped surface parameterization benchmark.**
Take 3-4 cusped hyperbolic surfaces (modular surface, once-punctured torus,
figure-eight knot complement boundary). Compare Farey-based parameterization
against Ricci flow parameterization (Gu's code) for:
- Accuracy near cusps
- Computational cost
- Mesh quality

**Step 2.3: Connect to the crowding problem.**
Investigate whether the Farey gap distribution (widths 1/(bd) with specific statistics)
can model or predict the crowding in Schwarz-Christoffel maps of elongated polygons.

### Tier 3: Speculative, long-term (3+ months)

**Step 3.1: Farey-Penner coordinates for surface remeshing.**
Develop an algorithm that uses the Stern-Brocot tree structure to provide
adaptive, hierarchical remeshing of surfaces via Penner coordinate refinement.

**Step 3.2: Number-theoretic quadrature on modular domains.**
Develop quadrature rules for integrals over the fundamental domain of PSL(2,Z)
using Farey points as nodes. This is natural because Farey points ARE the
lattice points of this domain.

**Step 3.3: Lean formalization of Ptolemy flip properties.**
Extend the Lean 4 proof of injection to prove properties about Ptolemy flips
and Penner coordinate updates during Farey refinement.

---

## PART 6: KEY REFERENCES

### Foundational (Farey-hyperbolic connection)
- Bobenko, Pinkall, Springborn. "Discrete conformal maps and ideal hyperbolic polyhedra." Geom. & Top. 2015.
- Springborn. "Ideal hyperbolic polyhedra and discrete uniformization." arXiv:1707.06848.
- Penner. "The decorated Teichmuller space of punctured surfaces." Comm. Math. Phys. 1987.

### Computational (state of the art)
- Gillespie, Springborn, Crane. "Discrete Conformal Equivalence of Polyhedral Surfaces." ACM TOG 2021.
- Capouellez, Zorin. "Seamless Parametrization in Penner Coordinates." ACM TOG 2024.
- Trefethen. "Numerical Conformal Mapping." arXiv:2507.14872, 2025.

### Mesh generation
- Gu (Stanford CTR). "Computational Conformal Geometry for High-Quality Mesh Generation." 2024-2025.
- Wei et al. "GPU-Accelerated Optimization of Discrete Ricci Flow." IET Image Processing, 2025.
- MicroRicci. arXiv:2506.15571, 2025.

### Hyperbolic Delaunay
- CGAL. "2D Hyperbolic Triangulations" and "2D Triangulations on Hyperbolic Surfaces." 2019/2025.
- Ebbens. "Delaunay triangulations on hyperbolic surfaces." Master thesis, Groningen, 2017.

### Multi-resolution / Stern-Brocot
- "Recognition of Arithmetic Hyperplanes Using the Stern-Brocot Tree." J. Math. Imaging & Vision, 2025.
- "Multiscale Discrete Geometry." Springer LNCS (uses Stern-Brocot for multi-resolution).

### Farey tessellation
- Series. "Continued Fractions and Hyperbolic Geometry." Warwick lecture notes.
- Karpenkov, Pratoussevitch. "Farey Bryophylla." arXiv:2409.01621, 2024.
- Seignourel. "The Farey Tessellation." U. Chicago REU, 2023.

---

## BOTTOM LINE

The combination "conformal mapping + Farey" is NOT merely a nice-sounding pair.
There is a genuine, deep mathematical connection through the Bobenko-Springborn
framework where Farey graph operations (Ptolemy flips in Penner coordinates) are
the ACTUAL computational primitives of discrete conformal mapping. Our injection
principle is a new result about these primitives.

However, the practical application is NARROW:
- It applies to arithmetic/cusped surfaces, not general engineering meshes
- It offers multi-resolution structure, not better mesh quality
- It connects to unsolved problems in convergence analysis, not in solver performance

The honest recommendation: Pursue Steps 1.1-1.3 as a focused investigation.
If the injection-Ptolemy connection yields a clean theorem and the CEPS comparison
shows measurable benefits for cusped surfaces, there is a solid paper here.
If not, pivot to the Stern-Brocot multi-resolution representation, which has
independent value regardless of the conformal mapping connection.
