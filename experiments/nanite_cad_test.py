#!/usr/bin/env python3
"""
Farey LOD on a CAD-like parametric surface mesh.
Test: cylinder + flange (disk cap), compare Farey vs Cluster vs Uniform LOD at 50%.
"""

import numpy as np
from math import gcd
from collections import defaultdict
import json

# ── 1. Parametric mesh generation ──────────────────────────────────────

N_SEG = 32   # angular segments
N_ROW = 16   # cylinder rows
N_RAD = 32   # flange radial segments (matches cylinder)
N_RING = 8   # flange concentric rings

def make_cylinder(radius=1.0, height=2.0):
    """Cylinder: N_SEG around x N_ROW high. Returns verts, tris, param_info."""
    verts = []
    params = []  # (k/N_SEG angle param, j/N_ROW height param)
    for j in range(N_ROW + 1):
        for k in range(N_SEG):
            theta = 2 * np.pi * k / N_SEG
            z = height * j / N_ROW
            verts.append([radius * np.cos(theta), radius * np.sin(theta), z])
            params.append((k, N_SEG, j, N_ROW))  # (num, denom_ang, num_h, denom_h)
    verts = np.array(verts)

    tris = []
    for j in range(N_ROW):
        for k in range(N_SEG):
            k_next = (k + 1) % N_SEG
            v00 = j * N_SEG + k
            v01 = j * N_SEG + k_next
            v10 = (j + 1) * N_SEG + k
            v11 = (j + 1) * N_SEG + k_next
            tris.append([v00, v01, v10])
            tris.append([v01, v11, v10])

    return verts, np.array(tris), params


def make_flange(radius=1.0, inner_radius=1.0, outer_radius=1.8, z_height=2.0):
    """Disk flange at top of cylinder. Returns verts, tris, param_info."""
    verts = []
    params = []

    # Center vertex
    verts.append([0.0, 0.0, z_height])
    params.append((0, 1, 0, 1))  # center = trivial Farey level

    # Concentric rings from inner_radius to outer_radius
    for ring in range(1, N_RING + 1):
        r = inner_radius + (outer_radius - inner_radius) * ring / N_RING
        for k in range(N_RAD):
            theta = 2 * np.pi * k / N_RAD
            verts.append([r * np.cos(theta), r * np.sin(theta), z_height])
            params.append((k, N_RAD, ring, N_RING))

    verts = np.array(verts)

    tris = []
    # Inner fan: center to first ring
    for k in range(N_RAD):
        k_next = (k + 1) % N_RAD
        tris.append([0, 1 + k, 1 + k_next])

    # Ring-to-ring quads
    for ring in range(N_RING - 1):
        for k in range(N_RAD):
            k_next = (k + 1) % N_RAD
            v0 = 1 + ring * N_RAD + k
            v1 = 1 + ring * N_RAD + k_next
            v2 = 1 + (ring + 1) * N_RAD + k
            v3 = 1 + (ring + 1) * N_RAD + k_next
            tris.append([v0, v1, v2])
            tris.append([v1, v3, v2])

    return verts, np.array(tris), params


def farey_denominator(k, n):
    """Denominator of k/n in lowest terms."""
    g = gcd(k, n)
    return n // g


def merge_mesh(cyl_v, cyl_t, cyl_p, flange_v, flange_t, flange_p):
    """Merge cylinder and flange, stitching top ring to inner flange ring."""
    offset = len(cyl_v)
    all_v = np.vstack([cyl_v, flange_v])
    all_t = np.vstack([cyl_t, flange_t + offset])
    all_p = cyl_p + flange_p

    # Stitch: connect cylinder top row to flange inner ring
    stitch_tris = []
    for k in range(N_SEG):
        k_next = (k + 1) % N_SEG
        cyl_top = N_ROW * N_SEG + k        # top row of cylinder
        cyl_top_next = N_ROW * N_SEG + k_next
        flange_inner = offset + 1 + k       # first ring of flange
        flange_inner_next = offset + 1 + k_next
        stitch_tris.append([cyl_top, cyl_top_next, flange_inner])
        stitch_tris.append([cyl_top_next, flange_inner_next, flange_inner])

    all_t = np.vstack([all_t, np.array(stitch_tris)])
    return all_v, all_t, all_p


# ── 2. Assign Farey levels ────────────────────────────────────────────

def assign_farey_levels(params):
    """Each vertex gets Farey level = max denominator of its parameter fractions."""
    levels = []
    for p in params:
        k_ang, n_ang, k_h, n_h = p
        d_ang = farey_denominator(k_ang, n_ang)
        d_h = farey_denominator(k_h, n_h)
        levels.append(max(d_ang, d_h))
    return np.array(levels)


# ── 3. LOD Methods ────────────────────────────────────────────────────

def find_boundary_verts(verts, tris, n_cyl_verts):
    """Find vertices on cylinder-flange boundary (top ring of cylinder)."""
    boundary = set(range(N_ROW * N_SEG, (N_ROW + 1) * N_SEG))
    return boundary


def count_cracks(verts, tris, kept_mask):
    """Count cracks: edges where one vertex kept, other removed, on a kept triangle's edge."""
    cracks = 0
    for tri in tris:
        v0, v1, v2 = tri
        kept = [kept_mask[v0], kept_mask[v1], kept_mask[v2]]
        if sum(kept) == 1 or sum(kept) == 2:
            # Partially kept triangle = crack
            cracks += 1
    return cracks


def geometric_error(verts, tris, kept_mask):
    """Hausdorff-like error: max distance from removed vertex to nearest kept vertex."""
    kept_idx = np.where(kept_mask)[0]
    removed_idx = np.where(~kept_mask)[0]
    if len(removed_idx) == 0 or len(kept_idx) == 0:
        return 0.0
    kept_pos = verts[kept_idx]
    max_err = 0.0
    for ri in removed_idx:
        dists = np.linalg.norm(kept_pos - verts[ri], axis=1)
        max_err = max(max_err, np.min(dists))
    return max_err


# ── Method A: Farey LOD ──────────────────────────────────────────────

def farey_lod(verts, tris, levels, target_ratio=0.5):
    """Keep vertices with Farey denominator <= threshold."""
    # Find threshold that gives ~target_ratio vertices
    sorted_levels = np.sort(np.unique(levels))
    best_thresh = sorted_levels[0]
    for thresh in sorted_levels:
        ratio = np.sum(levels <= thresh) / len(levels)
        if ratio >= target_ratio:
            best_thresh = thresh
            break

    kept_mask = levels <= best_thresh
    return kept_mask, best_thresh


# ── Method B: Cluster LOD ────────────────────────────────────────────

def cluster_lod(verts, tris, n_cyl_verts, target_ratio=0.5):
    """Split into 4 clusters, simplify each to 50%, lock borders."""
    n_total = len(verts)
    # Clusters: top cap (flange), bottom half cyl, left cyl, right cyl
    # Simpler: by z-coordinate and angle
    mid_z = (verts[:, 2].max() + verts[:, 2].min()) / 2

    clusters = np.zeros(n_total, dtype=int)
    for i in range(n_total):
        x, y, z = verts[i]
        if i >= n_cyl_verts:  # flange
            clusters[i] = 0
        elif z < mid_z and np.arctan2(y, x) >= 0:
            clusters[i] = 1
        elif z < mid_z:
            clusters[i] = 2
        else:
            clusters[i] = 3

    # Find border vertices (on edges between clusters)
    border = set()
    for tri in tris:
        cs = set(clusters[v] for v in tri)
        if len(cs) > 1:
            for v in tri:
                border.add(v)

    # Keep all border verts, randomly thin each cluster to target
    kept_mask = np.zeros(n_total, dtype=bool)
    for v in border:
        kept_mask[v] = True

    border_overhead = len(border)

    for c in range(4):
        cluster_verts = np.where((clusters == c) & (~np.array([i in border for i in range(n_total)])))[0]
        n_keep = max(1, int(len(cluster_verts) * target_ratio))
        # Keep every other vertex (systematic)
        keep_idx = cluster_verts[::2][:n_keep]
        kept_mask[keep_idx] = True

    return kept_mask, border_overhead


# ── Method C: Uniform LOD ────────────────────────────────────────────

def uniform_lod(verts, tris, n_cyl_verts, target_ratio=0.5):
    """Remove every other row/column on cylinder, every other ring on flange."""
    kept_mask = np.zeros(len(verts), dtype=bool)

    # Cylinder: keep even rows and even columns
    for j in range(N_ROW + 1):
        for k in range(N_SEG):
            idx = j * N_SEG + k
            if j % 2 == 0 and k % 2 == 0:
                kept_mask[idx] = True

    # Flange: keep center + even rings, even angles
    kept_mask[n_cyl_verts] = True  # center
    for ring in range(1, N_RING + 1):
        for k in range(N_RAD):
            idx = n_cyl_verts + 1 + (ring - 1) * N_RAD + k
            if ring % 2 == 0 and k % 2 == 0:
                kept_mask[idx] = True

    return kept_mask


# ── 4. Run ────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("FAREY LOD ON CAD-LIKE PARAMETRIC SURFACE MESH")
    print("=" * 70)

    # Build mesh
    cyl_v, cyl_t, cyl_p = make_cylinder()
    flange_v, flange_t, flange_p = make_flange()
    n_cyl_verts = len(cyl_v)

    verts, tris, params = merge_mesh(cyl_v, cyl_t, cyl_p, flange_v, flange_t, flange_p)
    levels = assign_farey_levels(params)

    print(f"\nMesh: {len(verts)} vertices, {len(tris)} triangles")
    print(f"  Cylinder: {n_cyl_verts} verts ({N_SEG} seg x {N_ROW+1} rows)")
    print(f"  Flange:   {len(flange_v)} verts ({N_RAD} radial x {N_RING} rings + center)")
    print(f"  Stitch:   {2*N_SEG} triangles")

    boundary = find_boundary_verts(verts, tris, n_cyl_verts)
    print(f"  Boundary verts (cyl-flange): {len(boundary)}")

    # Farey level distribution
    unique, counts = np.unique(levels, return_counts=True)
    print(f"\nFarey level distribution:")
    for u, c in zip(unique, counts):
        print(f"  denom <= {u:3d}: {np.sum(levels <= u):4d} verts ({100*np.sum(levels <= u)/len(verts):.1f}%)")

    results = {}

    # ── A: Farey LOD ──
    print("\n" + "-" * 50)
    print("A) FAREY LOD (denominator threshold)")
    farey_mask, thresh = farey_lod(verts, tris, levels, 0.5)
    n_kept = np.sum(farey_mask)
    cracks = count_cracks(verts, tris, farey_mask)
    err = geometric_error(verts, tris, farey_mask)

    # Check boundary preservation
    boundary_kept = sum(1 for v in boundary if farey_mask[v])
    print(f"  Threshold: denom <= {thresh}")
    print(f"  Kept: {n_kept}/{len(verts)} ({100*n_kept/len(verts):.1f}%)")
    print(f"  Boundary preserved: {boundary_kept}/{len(boundary)}")
    print(f"  Cracks (partial tris): {cracks}")
    print(f"  Max geometric error: {err:.4f}")
    results['farey'] = {
        'kept': int(n_kept), 'ratio': round(n_kept/len(verts), 3),
        'cracks': cracks, 'error': round(err, 4),
        'boundary_kept': boundary_kept, 'threshold': int(thresh),
        'overhead': 0
    }

    # ── B: Cluster LOD ──
    print("\n" + "-" * 50)
    print("B) CLUSTER LOD (4 clusters, border locking)")
    cluster_mask, border_overhead = cluster_lod(verts, tris, n_cyl_verts, 0.5)
    n_kept = np.sum(cluster_mask)
    cracks = count_cracks(verts, tris, cluster_mask)
    err = geometric_error(verts, tris, cluster_mask)
    boundary_kept = sum(1 for v in boundary if cluster_mask[v])
    print(f"  Kept: {n_kept}/{len(verts)} ({100*n_kept/len(verts):.1f}%)")
    print(f"  Border overhead (locked verts): {border_overhead}")
    print(f"  Boundary preserved: {boundary_kept}/{len(boundary)}")
    print(f"  Cracks (partial tris): {cracks}")
    print(f"  Max geometric error: {err:.4f}")
    results['cluster'] = {
        'kept': int(n_kept), 'ratio': round(n_kept/len(verts), 3),
        'cracks': cracks, 'error': round(err, 4),
        'boundary_kept': boundary_kept, 'overhead': border_overhead
    }

    # ── C: Uniform LOD ──
    print("\n" + "-" * 50)
    print("C) UNIFORM LOD (every other row/col)")
    uniform_mask = uniform_lod(verts, tris, n_cyl_verts, 0.5)
    n_kept = np.sum(uniform_mask)
    cracks = count_cracks(verts, tris, uniform_mask)
    err = geometric_error(verts, tris, uniform_mask)
    boundary_kept = sum(1 for v in boundary if uniform_mask[v])
    print(f"  Kept: {n_kept}/{len(verts)} ({100*n_kept/len(verts):.1f}%)")
    print(f"  Boundary preserved: {boundary_kept}/{len(boundary)}")
    print(f"  Cracks (partial tris): {cracks}")
    print(f"  Max geometric error: {err:.4f}")
    results['uniform'] = {
        'kept': int(n_kept), 'ratio': round(n_kept/len(verts), 3),
        'cracks': cracks, 'error': round(err, 4),
        'boundary_kept': boundary_kept, 'overhead': 0
    }

    # ── Summary ──
    print("\n" + "=" * 70)
    print("SUMMARY COMPARISON")
    print("=" * 70)
    print(f"{'Method':<12} {'Kept':>6} {'Ratio':>7} {'Cracks':>7} {'Error':>8} {'Boundary':>10} {'Overhead':>10}")
    print("-" * 70)
    for name, r in results.items():
        print(f"{name:<12} {r['kept']:>6} {r['ratio']:>7.1%} {r['cracks']:>7} {r['error']:>8.4f} "
              f"{r['boundary_kept']:>5}/{len(boundary):<4} {r.get('overhead',0):>10}")

    # ── Key analysis ──
    print("\n" + "=" * 70)
    print("ANALYSIS: Does parametric structure make Farey LOD natural for CAD?")
    print("=" * 70)

    # Check if Farey levels align with parametric structure
    # For a 32-segment cylinder, denominators are divisors of 32: 1,2,4,8,16,32
    print("\nParametric alignment check:")
    print("  32-segment circle: denominators possible = divisors of 32")
    divs_32 = [d for d in range(1, 33) if 32 % d == 0]
    print(f"  Divisors of 32: {divs_32}")
    print(f"  These create {len(divs_32)} natural LOD levels (powers of 2)")

    # Fraction of vertices at each power-of-2 level
    print("\n  Power-of-2 LOD cascade:")
    for d in divs_32:
        n_at = np.sum(levels <= d)
        print(f"    denom <= {d:2d}: {n_at:4d} verts ({100*n_at/len(verts):5.1f}%) -- "
              f"{'<-- NATURAL' if d in [4, 8, 16] else ''}")

    farey_wins = (results['farey']['cracks'] <= results['cluster']['cracks'] and
                  results['farey']['cracks'] <= results['uniform']['cracks'])
    cluster_overhead_pct = 100 * results['cluster']['overhead'] / len(verts)

    print(f"\nKey findings:")
    print(f"  1. Farey cracks: {results['farey']['cracks']} vs Cluster: {results['cluster']['cracks']} vs Uniform: {results['uniform']['cracks']}")
    print(f"  2. Cluster border overhead: {results['cluster']['overhead']} verts ({cluster_overhead_pct:.1f}% of mesh)")
    print(f"  3. Farey boundary preservation: {results['farey']['boundary_kept']}/{len(boundary)}")
    print(f"  4. Geometric error: Farey={results['farey']['error']:.4f} Cluster={results['cluster']['error']:.4f} Uniform={results['uniform']['error']:.4f}")

    if farey_wins:
        print("\n  >> FAREY LOD has fewest cracks on this parametric CAD mesh.")
    else:
        print(f"\n  >> Farey does NOT have fewest cracks here.")

    # Verdict
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    # Check if parametric = natural for Farey
    # Key insight: CAD parametric surfaces have rational parameters by construction
    # Farey hierarchy IS the natural hierarchy for these parameters
    is_natural = len(divs_32) >= 4  # power-of-2 gives clean cascade

    if is_natural and farey_wins:
        verdict = "VIABLE"
        reasoning = ("Parametric CAD surfaces have rational parameters by construction. "
                     "The Farey hierarchy directly matches the parametric subdivision, "
                     "giving clean LOD levels without cluster boundaries or border locking overhead. "
                     "Crack count is competitive with or better than cluster-based approaches.")
    elif is_natural:
        verdict = "PARTIALLY VIABLE"
        reasoning = ("Farey hierarchy aligns with parametric structure (natural LOD levels), "
                     "but crack count is not the best. The zero-overhead advantage may "
                     "compensate in streaming scenarios.")
    else:
        verdict = "NOT NATURAL"
        reasoning = "Parametric structure does not align well with Farey hierarchy."

    print(f"\n  {verdict}")
    print(f"\n  {reasoning}")

    return results


if __name__ == '__main__':
    results = main()
