#!/usr/bin/env python3
"""
Farey LOD on Point Cloud Data — Does hierarchical ordering help?

Compares three progressive orderings for streaming 3D point clouds:
1. FAREY: Sort by max denominator of best rational approximation per coordinate
2. RANDOM: Random permutation
3. OCTREE: Standard octree traversal (coarse cells first)

Measures at cutoffs k = 100, 500, 1000, 2000, 5000, 10000:
- Max gap (largest nearest-neighbor distance = proxy for empty sphere)
- Coverage uniformity (std dev of local densities)
- Reconstruction error (Hausdorff-like distance from k-subset to full cloud)
"""

import numpy as np
from scipy.spatial import cKDTree
from fractions import Fraction
import time
import json
import os

np.random.seed(42)

# ── 1. Generate realistic point cloud: sphere with bumps ──

def generate_bumpy_sphere(n_points=10000):
    """Sphere with Gaussian bumps, mapped to [0,1]^3."""
    theta = np.random.uniform(0, 2 * np.pi, n_points)
    phi = np.arccos(np.random.uniform(-1, 1, n_points))

    # Base radius with bumps
    r = 1.0
    # Add 5 Gaussian bumps at random locations
    bump_centers = np.random.RandomState(0).uniform(0, np.pi, (5, 2))  # (theta, phi)
    for tc, pc in bump_centers:
        angular_dist = np.arccos(
            np.clip(np.sin(phi) * np.sin(pc) * np.cos(theta - tc) +
                    np.cos(phi) * np.cos(pc), -1, 1)
        )
        r = r + 0.15 * np.exp(-angular_dist**2 / 0.1)

    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    # Map to [0,1]^3
    pts = np.column_stack([x, y, z])
    for i in range(3):
        mn, mx = pts[:, i].min(), pts[:, i].max()
        pts[:, i] = (pts[:, i] - mn) / (mx - mn + 1e-12)

    return pts


# ── 2. Farey complexity: best rational approximation denominator ──

def farey_denominator(x, max_denom=1000):
    """Denominator of best rational approximation of x with denom <= max_denom."""
    f = Fraction(x).limit_denominator(max_denom)
    return f.denominator

def farey_complexity(point, max_denom=1000):
    """Max denominator across coordinates — higher = more complex."""
    return max(farey_denominator(c, max_denom) for c in point)


# ── 3. Octree ordering ──

def octree_order(points, max_depth=10):
    """
    Assign octree traversal order: points in coarser cells come first.
    Morton code approach — interleave bits of quantized coordinates.
    """
    n = len(points)
    # Quantize to grid
    grid_size = 2**max_depth
    quantized = np.clip((points * grid_size).astype(int), 0, grid_size - 1)

    # Morton code (Z-order curve) — interleave bits
    def morton3d(x, y, z):
        code = 0
        for i in range(max_depth):
            code |= ((x >> i) & 1) << (3 * i)
            code |= ((y >> i) & 1) << (3 * i + 1)
            code |= ((z >> i) & 1) << (3 * i + 2)
        return code

    codes = np.array([morton3d(q[0], q[1], q[2]) for q in quantized])
    return np.argsort(codes)


# ── 4. Metrics ──

def max_gap(points_subset):
    """Max nearest-neighbor distance among subset points (proxy for largest hole)."""
    if len(points_subset) < 2:
        return float('inf')
    tree = cKDTree(points_subset)
    dists, _ = tree.query(points_subset, k=2)
    return float(np.max(dists[:, 1]))

def coverage_uniformity(points_subset, n_bins=5):
    """
    Divide [0,1]^3 into n_bins^3 voxels, count points per voxel.
    Return coefficient of variation (std/mean) — lower = more uniform.
    """
    if len(points_subset) < 2:
        return float('inf')
    bins = np.linspace(0, 1.0001, n_bins + 1)
    counts = np.zeros(n_bins**3)
    ix = np.digitize(points_subset[:, 0], bins) - 1
    iy = np.digitize(points_subset[:, 1], bins) - 1
    iz = np.digitize(points_subset[:, 2], bins) - 1
    ix = np.clip(ix, 0, n_bins - 1)
    iy = np.clip(iy, 0, n_bins - 1)
    iz = np.clip(iz, 0, n_bins - 1)
    idx = ix * n_bins**2 + iy * n_bins + iz
    for i in idx:
        counts[i] += 1
    mean_c = counts.mean()
    if mean_c == 0:
        return float('inf')
    return float(counts.std() / mean_c)

def reconstruction_error(points_subset, full_points):
    """
    One-sided Hausdorff: for each point in full cloud, distance to nearest
    in subset. Return mean and max.
    """
    if len(points_subset) < 1:
        return float('inf'), float('inf')
    tree = cKDTree(points_subset)
    dists, _ = tree.query(full_points, k=1)
    return float(np.mean(dists)), float(np.max(dists))


# ── 5. Run experiment ──

def run_experiment():
    print("Generating bumpy sphere point cloud (10,000 points)...")
    points = generate_bumpy_sphere(10000)
    n = len(points)
    print(f"  Shape: {points.shape}, range: [{points.min():.3f}, {points.max():.3f}]")

    # Compute orderings
    print("\nComputing FAREY ordering...")
    t0 = time.time()
    complexities = np.array([farey_complexity(p) for p in points])
    farey_order = np.argsort(complexities)
    t_farey = time.time() - t0
    print(f"  Done in {t_farey:.1f}s. Complexity range: [{complexities.min()}, {complexities.max()}]")

    print("Computing RANDOM ordering...")
    random_order = np.random.permutation(n)

    print("Computing OCTREE ordering...")
    t0 = time.time()
    oct_order = octree_order(points)
    t_octree = time.time() - t0
    print(f"  Done in {t_octree:.1f}s")

    cutoffs = [100, 500, 1000, 2000, 5000, 10000]
    orderings = {
        'farey': farey_order,
        'random': random_order,
        'octree': oct_order,
    }

    results = {}
    for name, order in orderings.items():
        print(f"\nEvaluating {name.upper()} ordering...")
        results[name] = {}
        for k in cutoffs:
            subset = points[order[:k]]
            mg = max_gap(subset)
            cu = coverage_uniformity(subset)
            re_mean, re_max = reconstruction_error(subset, points)
            results[name][k] = {
                'max_gap': mg,
                'coverage_cv': cu,
                'recon_mean': re_mean,
                'recon_max': re_max,
            }
            print(f"  k={k:>5}: max_gap={mg:.4f}  coverage_cv={cu:.3f}  "
                  f"recon_mean={re_mean:.4f}  recon_max={re_max:.4f}")

    # ── 6. Summary comparison ──
    print("\n" + "=" * 80)
    print("SUMMARY: Farey vs Random vs Octree")
    print("=" * 80)

    # For each metric, who wins at each cutoff?
    metrics = ['max_gap', 'coverage_cv', 'recon_mean', 'recon_max']
    metric_labels = ['Max Gap', 'Coverage CV', 'Recon Mean', 'Recon Max']

    wins = {name: 0 for name in orderings}
    total_comparisons = 0

    for metric, label in zip(metrics, metric_labels):
        print(f"\n{label} (lower is better):")
        print(f"  {'k':>6}  {'Farey':>10}  {'Random':>10}  {'Octree':>10}  {'Winner':>10}")
        for k in cutoffs:
            vals = {name: results[name][k][metric] for name in orderings}
            winner = min(vals, key=vals.get)
            wins[winner] += 1
            total_comparisons += 1
            marker = {name: ' *' if name == winner else '  ' for name in orderings}
            print(f"  {k:>6}  {vals['farey']:>10.4f}{marker['farey']}  "
                  f"{vals['random']:>10.4f}{marker['random']}  "
                  f"{vals['octree']:>10.4f}{marker['octree']}  "
                  f"{winner:>10}")

    print(f"\nTotal wins across all metrics and cutoffs ({total_comparisons} comparisons):")
    for name in orderings:
        pct = 100 * wins[name] / total_comparisons
        print(f"  {name.upper():>8}: {wins[name]:>2}/{total_comparisons} ({pct:.0f}%)")

    # Farey advantage ratio at each cutoff
    print(f"\nFarey / Random ratio (recon_mean, <1 means Farey better):")
    for k in cutoffs:
        ratio = results['farey'][k]['recon_mean'] / max(results['random'][k]['recon_mean'], 1e-12)
        print(f"  k={k:>5}: {ratio:.3f}")

    print(f"\nFarey / Octree ratio (recon_mean, <1 means Farey better):")
    for k in cutoffs:
        ratio = results['farey'][k]['recon_mean'] / max(results['octree'][k]['recon_mean'], 1e-12)
        print(f"  k={k:>5}: {ratio:.3f}")

    return results, wins, total_comparisons


if __name__ == '__main__':
    results, wins, total = run_experiment()

    # Save raw results as JSON
    out_path = os.path.expanduser('~/Desktop/Farey-Local/experiments/nanite_pointcloud_results.json')
    # Convert int keys to strings for JSON
    json_results = {}
    for name in results:
        json_results[name] = {str(k): v for k, v in results[name].items()}
    with open(out_path, 'w') as f:
        json.dump(json_results, f, indent=2)
    print(f"\nRaw results saved to {out_path}")
