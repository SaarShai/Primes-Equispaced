#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run35b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/OVERNIGHT_NANITE_MATHLIB_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/OVERNIGHT_NANITE_MATHLIB_LOG.md"
}

rung4() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/OVERNIGHT_NANITE_MATHLIB_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"gemma4:26b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/OVERNIGHT_NANITE_MATHLIB_LOG.md"
}

echo "=== Overnight Nanite+Mathlib started $(date) ===" > "$OUT/OVERNIGHT_NANITE_MATHLIB_LOG.md"

# ===== NANITE LOD TRACK (35b) =====

# 1. 3D mesh parameterization — the gap between our 2D result and production
run35b "NANITE_3D_PARAMETERIZATION" "Our Farey LOD eliminates 126% boundary overhead in 2D by using denominator-based vertex levels. To apply this to 3D game meshes (Nanite/UE5), we need to parameterize arbitrary 3D mesh onto a Farey domain. Options: (1) Conformal map: map mesh surface to [0,1]^2 via conformal parameterization, then apply Farey grid. Problem: distortion at singularities. (2) Barycentric coordinates: assign each vertex a Farey-based barycentric coordinate within its triangle. (3) Edge-based: assign each edge a Farey level based on its length ratio to neighbors. (4) Spectral: use mesh Laplacian eigenvectors to define a natural hierarchy. Which approach is most feasible for a proof-of-concept? What would a minimal demo look like? Design the simplest possible 3D Farey LOD that works on a triangle mesh of ~1000 vertices."

# 2. Compare with Nanite's actual algorithm
run35b "NANITE_COMPARISON_DETAILED" "Nanite (UE5) uses: (1) cluster meshes into groups of ~128 triangles, (2) simplify each cluster independently using quadric error metrics, (3) border vertices between clusters CANNOT be simplified (causes cracks), (4) build a DAG of cluster groups at multiple LOD levels. Our Farey approach: each vertex has a unique denominator level. LOD k = keep vertices with denominator <= k. No clusters needed, no border problem. Compare: (a) Memory overhead: Nanite stores DAG + cluster metadata. Farey stores one integer per vertex. (b) Runtime: Nanite does per-cluster LOD selection via screen-space error. Farey does per-vertex threshold check. (c) Quality: Nanite preserves topology within clusters but not across. Farey preserves global hierarchy. Write a detailed comparison table. What would convince Epic Games this is worth investigating?"

# 3. Tech report draft for Nanite team
run35b "NANITE_TECH_REPORT_DRAFT" "Draft a 2-page technical report titled 'Farey-Based LOD: Eliminating Cluster Boundary Artifacts in Mesh Simplification.' Target audience: graphics engineers at Epic Games. Structure: (1) Problem: Nanite's cluster boundary vertices can't be simplified, wasting 126% vertices in 2D. (2) Solution: assign each vertex a Farey denominator level via mesh parameterization. LOD k = keep denominator <= k. Zero boundary artifacts by construction. (3) Results: 2D proof-of-concept shows 0% structural overhead vs 126% for cluster-based. (4) Limitations: 3D parameterization not yet implemented. (5) Next steps: minimal 3D demo on Stanford bunny. Write in technical but accessible style. Include pseudocode for the LOD selection algorithm."

# 4. Who to contact at Epic + meshoptimizer
run35b "NANITE_CONTACT_STRATEGY" "Strategy for approaching the graphics community with our Farey LOD work. Key people: (1) Brian Karis (Epic Games, Nanite technical director). (2) Arseny Kapoulkine (meshoptimizer author, independent consultant). (3) Morgan McGuire (formerly NVIDIA, now independent). (4) Hugues Hoppe (Microsoft Research, mesh simplification pioneer). For each: how to reach them, what angle to use, what would interest them. Also: relevant conferences (SIGGRAPH, Eurographics), relevant GitHub repos to contribute to (meshoptimizer has 6K stars). What is the minimum demo that would get their attention?"

# ===== MATHLIB CONTRIBUTION TRACK (35b) =====

# 5. Audit Lean files for Mathlib readiness
run35b "MATHLIB_READINESS_AUDIT" "We have 15 Lean 4 files with 422 results (266 theorems, 93 lemmas, 63 definitions) about Farey sequences. To contribute to Mathlib, each file needs: (1) Consistent style (Mathlib naming conventions: snake_case, no abbreviations). (2) Proper imports (use Mathlib API, not ad hoc definitions). (3) Documentation (docstrings for every public declaration). (4) No sorry, no native_decide for non-trivial results (Mathlib prefers tactic proofs). (5) Logical organization (one concept per file, clear dependency graph). Assess: how much work is needed to bring our files to Mathlib standard? List the 10 most valuable results that Mathlib currently LACKS about Farey sequences. Which files are closest to ready? Which need the most work?"

# 6. What does Mathlib currently have on Farey?
run35b "MATHLIB_FAREY_GAP_ANALYSIS" "What does Mathlib (the Lean 4 math library) currently contain about Farey sequences? Check your knowledge: (1) Is there a Farey sequence definition in Mathlib? (2) Are Ramanujan sums defined? (3) Is the Mertens function defined? (4) Are Dedekind sums in Mathlib? (5) Is the Mobius function and Mobius inversion available? (6) Are there any results about equidistribution of Farey fractions? For each: if it exists, give the Mathlib module name. If not, this is a gap our contribution would fill. Identify the TOP 5 most impactful contributions we could make."

# ===== GEMMA4 TRACK =====

# 7. Nanite literature review
rung4 "NANITE_LITERATURE_DEEP" "Survey the mesh LOD literature for approaches that address cluster boundary artifacts. Key papers: (1) Nanite original (Karis, SIGGRAPH 2021 talk). (2) meshoptimizer (Kapoulkine). (3) 'Recreating Nanite' blog series. (4) Hoppe's progressive meshes (1996). (5) Garland-Heckbert quadric error metrics (1997). What solutions have been proposed for the border vertex problem specifically? Has anyone used number-theoretic or denominator-based hierarchies for mesh LOD? What is the state of the art as of 2025?"

# 8. Mathlib contribution process
rung4 "MATHLIB_CONTRIBUTION_GUIDE" "How does one contribute to Mathlib (the Lean 4 math library)? Describe: (1) The PR process. (2) Style requirements (naming, documentation). (3) Review process and timeline. (4) What kinds of contributions are most valued. (5) Recent examples of new theory areas being added. (6) How to structure a contribution that adds a new theory (Farey sequences). (7) Who maintains the number theory section. (8) Is there a RFC process for new theories?"

# 9. Progressive data transmission — the BUILD recommendation
rung4 "PROGRESSIVE_TRANSMISSION_DESIGN" "Design a progressive 1D data transmission protocol using Farey ordering. The key insight: send data points in order of increasing Farey denominator. Each point maximally reduces the receiver's uncertainty about the full signal. Properties: (1) Any prefix of the transmission gives the best possible spatial coverage for that number of points. (2) The receiver can reconstruct an approximation at any interruption point. (3) Deterministic — both sender and receiver know the order without coordination. Compare to: (a) progressive JPEG (frequency-domain, not spatial). (b) Van der Corput sequence (similar but less structured). (c) Random ordering (no optimality). Design a concrete protocol for transmitting a 1D temperature profile from a satellite sensor. What is the error bound after receiving k out of N points?"

# 10. Nanite demo specification
rung4 "NANITE_DEMO_SPEC" "Specify a minimal Farey LOD demo that would impress graphics engineers. Requirements: (1) Input: triangle mesh in OBJ format (~1000 triangles). (2) Process: assign each vertex a Farey level via edge-length-based parameterization. (3) Output: mesh at multiple LOD levels, with ZERO cracks between adjacent levels. (4) Visualization: show the mesh at LOD 1, 2, 3, ... with smooth transitions. (5) Comparison: same mesh with standard cluster-based LOD showing boundary artifacts. Implementation: Python + trimesh library (fast prototyping). What is the simplest parameterization that assigns meaningful denominator levels to 3D mesh vertices?"

echo "=== Overnight complete $(date) ===" >> "$OUT/OVERNIGHT_NANITE_MATHLIB_LOG.md"
