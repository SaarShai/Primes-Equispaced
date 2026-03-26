# Paper Outline: Farey Injection and Discrete Conformal Geometry

**Working title:** *Farey Injection Constraints on Ptolemy Flips in the Bobenko-Springborn Framework*

**Alternative titles:**
- *Nested Farey Refinement and Penner Coordinate Stability for Discrete Conformal Maps*
- *How Farey Mediant Insertion Constrains Discrete Conformal Equivalence*

**Target venues:** Discrete & Computational Geometry (primary), Computer Aided Geometric Design (secondary), or Computational Geometry: Theory and Applications

**Status:** Research outline, not a draft. Based on Lean 4-verified injection principle and numerical experiments (March 2026).

---

## 1. Introduction (1.5--2 pages)

### 1.1 Context: The BPS Framework

Discrete conformal equivalence of polyhedral surfaces, as formulated by Bobenko-Pinkall-Springborn (2015) and refined by Springborn (2020), is defined via ideal hyperbolic polyhedra with Penner coordinates on decorated Teichmuller space. The key computational primitive is the **Ptolemy flip**: an edge operation that preserves the hyperbolic metric even when the Euclidean triangle inequality is violated. The practical implementation (CEPS algorithm, Gillespie-Springborn-Crane 2021; Penner coordinates for seamless parametrization, Capouellez-Zorin 2024) relies on sequences of these flips.

**Critical observation:** The flip graph of ideal triangulations of a punctured surface is the **Farey graph**. Ptolemy flips are operations on this graph. Yet the combinatorial constraints that Farey structure imposes on flip sequences have not been studied.

### 1.2 Our Contribution

We bring a formally verified result from number theory -- the **Farey injection principle** -- to bear on the BPS framework. The injection principle (verified in Lean 4) states:

> When refining the Farey sequence from F_{N-1} to F_N, each open interval (a/b, c/d) of consecutive Farey neighbors receives **at most one** new mediant (a+c)/(b+d), and this occurs if and only if b + d = N.

**Main claim:** This injection property constrains how Ptolemy flips can occur during mesh refinement in Penner coordinates. Specifically:

1. Each refinement step introduces at most one new vertex per triangle (no cascading splits).
2. The nesting property (F_N subset of F_{N+1}) guarantees that existing Penner coordinates are preserved under refinement.
3. The mediant formula gives an **explicit** expression for the new Penner coordinate in terms of its neighbors.

**Honest positioning:** This is a **structural/theoretical** contribution. Farey refinement does not produce better mesh quality than uniform refinement in the Euclidean metric. The value is compatibility with the discrete conformal framework and the explicit, non-cascading nature of the refinement.

### 1.3 Paper Organization

Brief roadmap of remaining sections.

---

## 2. Preliminaries (2--3 pages)

### 2.1 Farey Sequences and the Stern-Brocot Tree

- Definition of F_N; mediant operation; Stern-Brocot tree as the union of all Farey insertions
- Key properties: neighbors a/b, c/d satisfy |bc - ad| = 1; mediant (a+c)/(b+d) has denominator b+d
- The injection principle (state precisely, cite Lean proof)
- The sub-gap formula: when mediant m is inserted into interval (a/b, c/d), the new sub-intervals have widths 1/(b(b+d)) and 1/((b+d)d)

### 2.2 The Farey Graph and Ideal Triangulations

- Farey graph: vertices are Q union {1/0}; edges connect Farey neighbors
- Equivalence with ideal triangulation of the hyperbolic plane H^2
- Each ideal triangle has vertices p/q, r/s, (p+r)/(q+s) with the mediant as the "child"
- PSL(2,Z) acts by Mobius transformations, preserving the Farey graph

### 2.3 Discrete Conformal Equivalence (BPS Theory)

- Two triangulated surfaces (T, l) and (T, l') are discretely conformally equivalent if l'_e = exp(u_i/2 + u_j/2) * l_e for vertex scale factors u
- This is **exactly** the geometry of ideal hyperbolic polyhedra (Springborn 2020)
- Penner coordinates lambda_e = l_e * exp(h_i + h_j) where h_i are horocyclic decoration lengths
- Ptolemy relation: when flipping edge e in quadrilateral (i,j,k,l), the new length satisfies lambda_e * lambda_e' = lambda_{ik} * lambda_{jl} + lambda_{il} * lambda_{jk}
- Convexity of the energy functional in Penner coordinates

### 2.4 The CEPS Algorithm

- Brief summary of Gillespie-Springborn-Crane (2021): intrinsic Delaunay triangulation + Penner coordinate optimization + layout
- Role of Ptolemy flips in maintaining intrinsic Delaunay property
- Recent extension: Capouellez-Zorin (2024) for seamless parametrization

---

## 3. Main Result: Injection Constrains Ptolemy Flips (2--3 pages)

### 3.1 Farey Refinement as a Sequence of Ptolemy Flips

**Proposition 3.1.** The transition from the ideal triangulation corresponding to F_N to that of F_{N+1} can be realized as a sequence of Ptolemy flips, where:
- Each flip inserts exactly one new ideal vertex (the mediant).
- No two flips share an edge (they are independent and can be performed in any order).
- The number of flips equals |F_{N+1}| - |F_N| = phi(N+1), Euler's totient.

*Proof sketch:* The new fractions in F_{N+1} \ F_N are exactly those p/q with q = N+1 and gcd(p, N+1) = 1. Each such fraction is the mediant of exactly one pair of F_N-neighbors (by the injection principle). The corresponding Ptolemy flip subdivides exactly one ideal triangle. Since distinct mediants lie in distinct intervals, no two flips interact.

### 3.2 Penner Coordinate Stability Under Farey Refinement

**Theorem 3.2 (Main result).** Let T_N be the ideal triangulation corresponding to F_N with Penner coordinates {lambda_e}. After Farey refinement to T_{N+1}:

(a) All edges of T_N that are not flipped retain their Penner coordinates exactly.

(b) For each flipped edge, the new Penner coordinates are determined explicitly by the Ptolemy relation applied to the enclosing quadrilateral.

(c) The total number of Penner coordinates that change is exactly 3 * phi(N+1) (three new edges per inserted vertex, minus the one removed edge, plus two modified boundary edges -- net: 3 * phi(N+1) new coordinates).

*Consequence:* Farey refinement is a **local, non-cascading** update to Penner coordinates. This contrasts with arbitrary refinement strategies where inserting a vertex may trigger a cascade of Delaunay flips that propagates across the mesh.

### 3.3 Explicit Coordinate Formulas

For the mediant (a+c)/(b+d) inserted between neighbors a/b and c/d in F_N:

- The three new edges connect (a+c)/(b+d) to a/b, c/d, and the opposite vertex of the enclosing ideal quadrilateral.
- Using the sub-gap formula, the new edge lengths in the Farey metric are 1/(b(b+d)), 1/((b+d)d), and a formula involving the quadrilateral geometry.
- These translate to explicit Penner coordinates via the decoration structure.

**Remark:** The formulas simplify dramatically when the decoration is the standard horocyclic one (Ford circles), giving Penner coordinates proportional to 1/(q_i * q_j) for an edge connecting p_i/q_i to p_j/q_j.

---

## 4. Experimental Validation (2 pages)

### 4.1 Setup

- Farey tessellations at orders N = 3, 5, 7, 11, 13, 17, 19, 23
- Two conformal test maps: z^{2/3} (corner singularity) and Joukowski transform (cusp geometry)
- Mesh quality metrics: minimum angle, maximum aspect ratio, mean condition number
- Comparison: Farey refinement vs. uniform angular subdivision at matched vertex counts
- Convergence metric: maximum pointwise error of interpolated conformal map

### 4.2 Result 1: Mesh Quality (Farey Loses)

**Farey refinement produces significantly worse mesh quality than uniform refinement.** This is expected and must be stated honestly.

| Metric | Farey (N=23) | Uniform (matched) | Factor |
|--------|-------------|-------------------|--------|
| Min angle (z^{2/3}) | 0.09 deg | 38.6 deg | ~400x worse |
| Max aspect ratio (z^{2/3}) | 171,494 | 1.46 | ~117,000x worse |
| Mean condition (z^{2/3}) | 96.0 | 1.73 | ~55x worse |

**Explanation:** Farey fractions cluster near rationals with small denominators. Under conformal maps with singularities, this clustering produces extremely elongated triangles. Uniform subdivision avoids this by construction.

### 4.3 Result 2: Nesting Property (Farey Wins)

**The injection/nesting property is perfectly confirmed:** F_N is a strict subset of F_{N+1}, so all vertices at resolution N persist at resolution N+1. No vertex is displaced, and no re-triangulation is needed for the existing portion of the mesh.

Uniform refinement does NOT have this property in general: changing from k to k+1 uniform points may shift all existing vertices.

### 4.4 Result 3: Convergence Behavior

Both methods converge as vertex count increases, but uniform refinement converges faster in the L-infinity norm. Farey convergence is monotonically improving but slower (Farey wins 0/8 tests for z^{2/3}, 2/8 for Joukowski at low orders only).

### 4.5 Interpretation

The experimental results confirm the theoretical positioning: Farey refinement's value is **structural** (nesting, explicit formulas, compatibility with Penner coordinates), not **metric** (angle quality, aspect ratio). For applications where the BPS framework is used and refinement stability matters, the structural advantages outweigh the metric disadvantages.

---

## 5. Discussion and Applications (1.5--2 pages)

### 5.1 Where This Matters

**Cusped hyperbolic surfaces.** The Farey tessellation is the canonical triangulation of the modular surface H^2/PSL(2,Z). For cusped surfaces that are quotients of H^2 by arithmetic subgroups of PSL(2,Z), Farey refinement is geometrically natural. The mesh quality "defect" is actually a feature: the elongated triangles near cusps reflect the genuine geometry of the cusp, where the conformal factor diverges. Forcing equilateral triangles near a cusp introduces artificial distortion.

**Convergence analysis for discrete conformal maps.** The explicit, non-cascading nature of Farey refinement (Theorem 3.2) may enable sharper convergence proofs for discrete-to-smooth limits. Current convergence results (Luo 2004, Bobenko-Lutz-Springborn 2022) use asymptotic arguments. Farey refinement gives exact local mesh sizes (via the sub-gap formula), potentially yielding explicit convergence rates.

**Multi-resolution conformal map representation.** The Stern-Brocot tree provides a natural hierarchy: level k of the tree corresponds to Farey order k, and each level strictly refines the previous. A conformal map sampled at Farey points inherits this hierarchy, enabling progressive transmission and level-of-detail rendering without recomputation.

### 5.2 Limitations

1. **Not a mesh quality improvement.** Farey refinement is categorically worse than Delaunay or uniform refinement for metric quality. We do not claim otherwise.
2. **Ideal vs. finite vertices.** The Farey tessellation has all vertices on the ideal boundary (real line / circle at infinity). Applying our results to finite triangulations requires the decorated/truncated ideal polyhedra framework (Springborn 2020), which adds technical overhead.
3. **Generality.** The direct connection to Farey sequences applies to surfaces with PSL(2,Z) symmetry. Extension to general surfaces requires embedding the local flip structure into a Farey-like graph, which is possible but non-trivial.
4. **No implementation of CEPS integration.** We have not yet modified the CEPS algorithm to use Farey refinement. The experimental validation uses standalone mesh quality metrics, not end-to-end conformal parametrization quality.

### 5.3 Open Questions

1. Does Farey refinement yield better convergence *rates* (not quality per step, but quality per degree of freedom in the limit) for discrete conformal maps on arithmetic surfaces?
2. Can the injection principle constrain optimal cone singularity placement? Each refinement inserts at most one vertex per triangle, limiting where cones can appear.
3. Is there a quantitative version of Theorem 3.2 that bounds the Penner coordinate perturbation at each step in terms of the Farey order N?

---

## 6. Conclusion (0.5 page)

We have identified and formalized a structural connection between the Farey injection principle -- a number-theoretic result verified in Lean 4 -- and the Bobenko-Pinkall-Springborn framework for discrete conformal geometry. The main result (Theorem 3.2) shows that Farey refinement produces non-cascading, explicitly computable updates to Penner coordinates, with the number of modified coordinates per step given exactly by Euler's totient function. While this does not improve mesh quality in the Euclidean metric, it provides a rigid combinatorial scaffold for refinement in discrete conformal geometry, with potential applications to cusped surface parametrization and convergence analysis.

---

## References (key citations)

### BPS Framework
1. Bobenko, Pinkall, Springborn. "Discrete conformal maps and ideal hyperbolic polyhedra." *Geometry & Topology* 19 (2015), 2155--2215.
2. Springborn. "Ideal hyperbolic polyhedra and discrete uniformization." arXiv:1707.06848 (2020).
3. Gillespie, Springborn, Crane. "Discrete Conformal Equivalence of Polyhedral Surfaces." *ACM Trans. Graphics* 40(4), 2021.
4. Capouellez, Zorin. "Seamless Parametrization in Penner Coordinates." *ACM Trans. Graphics* 43(4), 2024.

### Farey / Number Theory
5. Hardy, Wright. *An Introduction to the Theory of Numbers.* Chapter 3 (Farey sequences).
6. Graham, Knuth, Patashnik. *Concrete Mathematics.* Chapter 4 (Stern-Brocot tree).
7. [Our Lean 4 formalization of the injection principle -- cite repository.]

### Decorated Teichmuller Theory
8. Penner. "The decorated Teichmuller space of punctured surfaces." *Comm. Math. Phys.* 113 (1987), 299--339.
9. Penner. *Decorated Teichmuller Theory.* European Mathematical Society, 2012.

### Convergence
10. Luo. "Combinatorial Yamabe flow on surfaces." *Comm. Contemp. Math.* 6 (2004), 765--780.
11. Bobenko, Lutz, Springborn. "Convergence of discrete uniformization." In preparation / arXiv.

### Computational Conformal Geometry
12. Gu, Yau. *Computational Conformal Geometry.* International Press, 2008.
13. Trefethen. "Numerical Conformal Mapping with Rational Functions." *Comput. Methods Funct. Theory* 20 (2020), 369--387.

---

## Appendix A: Experimental Details

- Full mesh quality tables for all Farey orders and both test maps
- Visualization of Farey nesting at orders 5, 11, 23
- Code availability: Python experiment code + Lean 4 proof repository

## Appendix B: Lean 4 Proof Summary

- Statement of the injection theorem in Lean 4 syntax
- Proof structure overview (no full listing; cite repository)
- Verified properties used in Section 3

---

## Estimated Length

- Main text: 10--12 pages (DCG format)
- Appendices: 2--3 pages
- Total: 12--15 pages

## Writing Plan

1. **First priority:** Make Proposition 3.1 and Theorem 3.2 precise. Currently stated as claims; need rigorous proofs connecting Farey combinatorics to Penner coordinate updates.
2. **Second priority:** Implement Farey refinement within CEPS (or a simplified version) to get end-to-end conformal map quality data, not just mesh quality.
3. **Third priority:** Write the cusped surface example (Section 5.1) with concrete computations on the modular surface.
