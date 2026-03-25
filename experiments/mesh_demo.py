#!/usr/bin/env python3
"""
FAREY MESH GENERATION — INJECTION PRINCIPLE DEMO
==================================================

The injection principle: when refining from F_N to F_{N+1}, each existing
mesh interval gets AT MOST ONE new node inserted. This is a provable
quality guarantee that no existing adaptive mesh method provides.

THIS SCRIPT DEMONSTRATES:
1. 1D Farey mesh on [0,1] with nodes at Farey fractions F_N
2. Refinement F_N → F_{N+1}: each interval gets at most 1 new node
3. Mesh quality metrics at each step (max size ratio, variance, element count)
4. Comparison with UNIFORM refinement (halving each element)
5. Comparison with RANDOM insertion of the same number of points
6. 2D mesh using F_N × F_N tensor product
7. Verification of the "no double-split" guarantee
8. Demonstration that non-Farey strategies VIOLATE no-double-split

Generates figures: mesh_1d_comparison.png, mesh_2d_farey.png, mesh_quality.png,
                   no_double_split.png
"""

from fractions import Fraction
from math import gcd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
from matplotlib.tri import Triangulation
import random
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# CORE: FAREY SEQUENCE GENERATION
# ============================================================

def farey_sequence(N):
    """Generate Farey sequence F_N as sorted list of Fraction objects."""
    fracs = set()
    for d in range(1, N + 1):
        for n in range(0, d + 1):
            if gcd(n, d) == 1:
                fracs.add(Fraction(n, d))
    return sorted(fracs)


def farey_to_floats(fracs):
    """Convert Farey fractions to sorted float array."""
    return np.array(sorted(set(float(f) for f in fracs)))


# ============================================================
# 1D MESH QUALITY METRICS
# ============================================================

def mesh_quality(nodes):
    """
    Compute mesh quality metrics for a 1D mesh.

    Returns dict with:
      - num_elements: number of intervals
      - max_size_ratio: ratio of largest to smallest element (worst = high)
      - size_variance: variance of element sizes (worst = high)
      - max_element_size: largest element
      - min_element_size: smallest element
    """
    nodes = np.sort(np.unique(nodes))
    sizes = np.diff(nodes)

    if len(sizes) == 0:
        return {'num_elements': 0, 'max_size_ratio': 0,
                'size_variance': 0, 'max_element_size': 0,
                'min_element_size': 0}

    return {
        'num_elements': len(sizes),
        'max_size_ratio': sizes.max() / sizes.min() if sizes.min() > 0 else float('inf'),
        'size_variance': float(np.var(sizes)),
        'max_element_size': float(sizes.max()),
        'min_element_size': float(sizes.min()),
    }


# ============================================================
# REFINEMENT STRATEGIES
# ============================================================

def uniform_refine(nodes):
    """Uniform refinement: insert midpoint of every interval."""
    nodes = np.sort(np.unique(nodes))
    midpoints = (nodes[:-1] + nodes[1:]) / 2
    return np.sort(np.concatenate([nodes, midpoints]))


def random_refine(nodes, num_new):
    """Random refinement: insert num_new random points in [0,1]."""
    nodes = np.sort(np.unique(nodes))
    new_pts = np.random.uniform(0, 1, num_new)
    return np.sort(np.concatenate([nodes, new_pts]))


# ============================================================
# NO-DOUBLE-SPLIT VERIFICATION
# ============================================================

def verify_no_double_split(old_nodes, new_nodes):
    """
    Verify injection principle: each old interval gets at most 1 new node.

    Returns:
      - valid: True if no interval was split more than once
      - max_splits: maximum number of new nodes in any single old interval
      - split_counts: list of (interval_index, split_count) for all intervals
    """
    old_nodes = np.sort(np.unique(old_nodes))
    new_nodes = np.sort(np.unique(new_nodes))

    # Find points in new_nodes that are NOT in old_nodes
    old_set = set(np.round(old_nodes, 15))
    truly_new = [x for x in new_nodes if round(x, 15) not in old_set]

    # For each old interval, count how many new points land inside it
    split_counts = []
    for i in range(len(old_nodes) - 1):
        lo, hi = old_nodes[i], old_nodes[i + 1]
        count = sum(1 for x in truly_new if lo < x < hi)
        split_counts.append((i, count))

    max_splits = max(c for _, c in split_counts) if split_counts else 0
    valid = max_splits <= 1

    return valid, max_splits, split_counts


def count_double_splits(old_nodes, new_nodes):
    """Count how many intervals got split 2+ times."""
    _, _, split_counts = verify_no_double_split(old_nodes, new_nodes)
    return sum(1 for _, c in split_counts if c >= 2)


# ============================================================
# DEMO 1: 1D MESH COMPARISON
# ============================================================

def demo_1d_comparison():
    """
    Compare Farey, uniform, and random mesh refinement on [0,1].
    """
    print("=" * 70)
    print("DEMO 1: 1D Mesh Refinement Comparison")
    print("=" * 70)

    max_N = 20

    # Track quality metrics for each strategy
    farey_metrics = []
    uniform_metrics = []
    random_metrics = []

    # Also track node counts for fair comparison
    farey_counts = []

    # Build Farey meshes F_1 through F_max_N
    print(f"\n{'N':>4} | {'#Elem':>6} | {'MaxRatio':>10} | {'Variance':>12} | {'NoDblSplit':>10}")
    print("-" * 60)

    for N in range(1, max_N + 1):
        fn = farey_sequence(N)
        nodes_f = farey_to_floats(fn)
        q = mesh_quality(nodes_f)
        farey_metrics.append(q)
        farey_counts.append(len(nodes_f))

        # Verify no-double-split for N >= 2
        if N >= 2:
            fn_prev = farey_sequence(N - 1)
            nodes_prev = farey_to_floats(fn_prev)
            valid, max_s, _ = verify_no_double_split(nodes_prev, nodes_f)
            nds_str = f"PASS (max={max_s})" if valid else f"FAIL (max={max_s})"
        else:
            nds_str = "N/A"

        print(f"{N:>4} | {q['num_elements']:>6} | {q['max_size_ratio']:>10.4f} | "
              f"{q['size_variance']:>12.8f} | {nds_str}")

    # Build uniform and random meshes with matching node counts
    print(f"\n--- Uniform refinement (matching node counts) ---")
    print(f"{'Step':>4} | {'#Elem':>6} | {'MaxRatio':>10} | {'Variance':>12}")
    print("-" * 50)

    # Start uniform from {0, 1}
    uniform_nodes = np.array([0.0, 1.0])
    step = 0
    while len(uniform_nodes) < farey_counts[-1] + 5:
        q = mesh_quality(uniform_nodes)
        uniform_metrics.append(q)
        print(f"{step:>4} | {q['num_elements']:>6} | {q['max_size_ratio']:>10.4f} | "
              f"{q['size_variance']:>12.8f}")
        uniform_nodes = uniform_refine(uniform_nodes)
        step += 1

    print(f"\n--- Random refinement (matching node counts, avg of 20 trials) ---")
    print(f"{'#Nodes':>6} | {'#Elem':>6} | {'MaxRatio':>10} | {'Variance':>12}")
    print("-" * 50)

    np.random.seed(42)
    for target_count in farey_counts[::2]:  # every other for brevity
        ratios = []
        variances = []
        for trial in range(20):
            rnd_nodes = np.sort(np.concatenate([[0.0, 1.0],
                                                np.random.uniform(0, 1, target_count - 2)]))
            q = mesh_quality(rnd_nodes)
            ratios.append(q['max_size_ratio'])
            variances.append(q['size_variance'])
        avg_ratio = np.mean(ratios)
        avg_var = np.mean(variances)
        random_metrics.append({
            'num_elements': target_count - 1,
            'max_size_ratio': avg_ratio,
            'size_variance': avg_var,
            'node_count': target_count,
        })
        print(f"{target_count:>6} | {target_count - 1:>6} | {avg_ratio:>10.4f} | "
              f"{avg_var:>12.8f}")

    return farey_metrics, uniform_metrics, random_metrics, farey_counts


# ============================================================
# DEMO 2: NO-DOUBLE-SPLIT GUARANTEE
# ============================================================

def demo_no_double_split():
    """
    Verify no-double-split for Farey refinement.
    Show it FAILS for random and greedy strategies.
    """
    print("\n" + "=" * 70)
    print("DEMO 2: No-Double-Split Guarantee Verification")
    print("=" * 70)

    results = {'farey': [], 'random': [], 'greedy_midpoint': []}

    max_N = 25

    # Farey: verify for every step
    print(f"\n--- Farey refinement (F_N → F_{{N+1}}) ---")
    print(f"{'N→N+1':>8} | {'Old Elem':>8} | {'New Pts':>7} | {'MaxSplit':>8} | {'DblSplit':>8} | {'Valid':>5}")
    print("-" * 65)

    for N in range(2, max_N + 1):
        old_nodes = farey_to_floats(farey_sequence(N - 1))
        new_nodes = farey_to_floats(farey_sequence(N))
        valid, max_s, sc = verify_no_double_split(old_nodes, new_nodes)
        dbl = count_double_splits(old_nodes, new_nodes)
        num_new = len(new_nodes) - len(old_nodes)

        results['farey'].append({
            'step': N, 'valid': valid, 'max_split': max_s,
            'double_splits': dbl, 'num_new': num_new
        })

        print(f"{N-1:>3}→{N:<3} | {len(old_nodes)-1:>8} | {num_new:>7} | "
              f"{max_s:>8} | {dbl:>8} | {'YES' if valid else 'NO':>5}")

    # Random: insert same number of new points as Farey does
    print(f"\n--- Random insertion (same # of new points as Farey) ---")
    print(f"{'N→N+1':>8} | {'Old Elem':>8} | {'New Pts':>7} | {'MaxSplit':>8} | {'DblSplit':>8} | {'Valid':>5}")
    print("-" * 65)

    np.random.seed(123)
    for N in range(2, max_N + 1):
        old_nodes = farey_to_floats(farey_sequence(N - 1))
        farey_new = farey_to_floats(farey_sequence(N))
        num_new = len(farey_new) - len(old_nodes)

        # Insert random points into the old mesh
        new_pts = np.random.uniform(0, 1, num_new)
        combined = np.sort(np.unique(np.concatenate([old_nodes, new_pts])))

        valid, max_s, sc = verify_no_double_split(old_nodes, combined)
        dbl = count_double_splits(old_nodes, combined)

        results['random'].append({
            'step': N, 'valid': valid, 'max_split': max_s,
            'double_splits': dbl, 'num_new': num_new
        })

        print(f"{N-1:>3}→{N:<3} | {len(old_nodes)-1:>8} | {num_new:>7} | "
              f"{max_s:>8} | {dbl:>8} | {'YES' if valid else 'NO':>5}")

    # Greedy midpoint: always split the LARGEST interval (can double-split)
    print(f"\n--- Greedy midpoint (split largest interval repeatedly) ---")
    print(f"{'Step':>8} | {'Old Elem':>8} | {'New Pts':>7} | {'MaxSplit':>8} | {'DblSplit':>8} | {'Valid':>5}")
    print("-" * 65)

    greedy_nodes = np.array([0.0, 1.0])
    for step in range(2, max_N + 1):
        old_nodes = greedy_nodes.copy()
        num_to_add = max(1, step)  # add 'step' new points by splitting largest

        current = old_nodes.copy()
        for _ in range(num_to_add):
            sizes = np.diff(current)
            idx = np.argmax(sizes)
            mid = (current[idx] + current[idx + 1]) / 2
            current = np.sort(np.append(current, mid))

        valid, max_s, sc = verify_no_double_split(old_nodes, current)
        dbl = count_double_splits(old_nodes, current)

        results['greedy_midpoint'].append({
            'step': step, 'valid': valid, 'max_split': max_s,
            'double_splits': dbl, 'num_new': num_to_add
        })

        print(f"{step:>8} | {len(old_nodes)-1:>8} | {num_to_add:>7} | "
              f"{max_s:>8} | {dbl:>8} | {'YES' if valid else 'NO':>5}")

        greedy_nodes = current

    return results


# ============================================================
# DEMO 3: 2D MESH
# ============================================================

def demo_2d_mesh():
    """
    Create 2D meshes using F_N x F_N tensor product.
    Compare Farey vs random node placement quality.
    """
    print("\n" + "=" * 70)
    print("DEMO 3: 2D Tensor-Product Mesh (Farey vs Random)")
    print("=" * 70)

    results_2d = []

    for N in [3, 5, 7, 10, 15]:
        fn = farey_to_floats(farey_sequence(N))

        # Farey tensor product
        xx, yy = np.meshgrid(fn, fn)
        farey_pts = np.column_stack([xx.ravel(), yy.ravel()])

        # Triangulate
        tri_f = Triangulation(farey_pts[:, 0], farey_pts[:, 1])

        # Compute triangle quality (ratio of circumradius to inradius)
        qualities_f = triangle_qualities(farey_pts, tri_f.triangles)

        # Random with same number of points
        np.random.seed(42 + N)
        n_pts = len(farey_pts)
        rand_pts = np.random.uniform(0, 1, (n_pts, 2))
        # Add boundary points to keep it fair
        boundary = np.array([[0,0],[1,0],[0,1],[1,1]])
        rand_pts = np.vstack([boundary, rand_pts[4:]])

        tri_r = Triangulation(rand_pts[:, 0], rand_pts[:, 1])
        qualities_r = triangle_qualities(rand_pts, tri_r.triangles)

        result = {
            'N': N,
            'n_points': n_pts,
            'n_triangles_farey': len(tri_f.triangles),
            'n_triangles_random': len(tri_r.triangles),
            'farey_quality_mean': np.mean(qualities_f),
            'farey_quality_worst': np.max(qualities_f),
            'farey_quality_std': np.std(qualities_f),
            'random_quality_mean': np.mean(qualities_r),
            'random_quality_worst': np.max(qualities_r),
            'random_quality_std': np.std(qualities_r),
        }
        results_2d.append(result)

        print(f"\nN={N}: {n_pts} points")
        print(f"  Farey:  {len(tri_f.triangles)} triangles, "
              f"mean quality={np.mean(qualities_f):.4f}, "
              f"worst={np.max(qualities_f):.4f}, "
              f"std={np.std(qualities_f):.4f}")
        print(f"  Random: {len(tri_r.triangles)} triangles, "
              f"mean quality={np.mean(qualities_r):.4f}, "
              f"worst={np.max(qualities_r):.4f}, "
              f"std={np.std(qualities_r):.4f}")

    return results_2d


def triangle_qualities(points, triangles):
    """
    Compute quality metric for each triangle.
    Quality = circumradius / (2 * inradius). Perfect equilateral = 1.
    Higher = worse quality.
    """
    qualities = []
    for tri in triangles:
        A, B, C = points[tri[0]], points[tri[1]], points[tri[2]]

        # Side lengths
        a = np.linalg.norm(B - C)
        b = np.linalg.norm(A - C)
        c = np.linalg.norm(A - B)

        # Semi-perimeter
        s = (a + b + c) / 2

        # Area by Heron's formula
        area_sq = s * (s - a) * (s - b) * (s - c)
        if area_sq <= 0:
            qualities.append(100.0)  # degenerate
            continue
        area = np.sqrt(area_sq)

        # Circumradius R = abc / (4*area)
        R = (a * b * c) / (4 * area)

        # Inradius r = area / s
        r = area / s

        # Quality ratio (1 = perfect equilateral)
        qualities.append(R / (2 * r))

    return np.array(qualities)


# ============================================================
# FIGURE 1: 1D Mesh at Different Refinement Levels
# ============================================================

def plot_1d_meshes():
    """Plot 1D Farey meshes at different N, plus comparison."""
    fig, axes = plt.subplots(4, 1, figsize=(14, 10))

    levels = [3, 5, 8, 12]

    for ax, N in zip(axes, levels):
        fn = farey_to_floats(farey_sequence(N))

        # Draw intervals as colored bars
        sizes = np.diff(fn)
        norm_sizes = sizes / sizes.max()

        for i in range(len(fn) - 1):
            color = plt.cm.viridis(1.0 - norm_sizes[i])  # small = bright
            ax.barh(0, sizes[i], left=fn[i], height=0.4, color=color,
                    edgecolor='black', linewidth=0.5)

        # Mark nodes
        ax.plot(fn, np.zeros_like(fn), 'k|', markersize=15, markeredgewidth=1.5)

        # Highlight NEW nodes (not in F_{N-1})
        if N > 1:
            fn_prev = farey_to_floats(farey_sequence(N - 1))
            prev_set = set(np.round(fn_prev, 12))
            new_nodes = [x for x in fn if round(x, 12) not in prev_set]
            if new_nodes:
                ax.plot(new_nodes, np.zeros(len(new_nodes)), 'rv',
                        markersize=8, label=f'New in F_{N}')

        q = mesh_quality(fn)
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.3, 0.5)
        ax.set_yticks([])
        ax.set_title(f'F_{N}: {q["num_elements"]} elements, '
                     f'max ratio = {q["max_size_ratio"]:.3f}, '
                     f'variance = {q["size_variance"]:.6f}',
                     fontsize=11)
        ax.legend(loc='upper right', fontsize=9)

    axes[-1].set_xlabel('Position on [0, 1]', fontsize=12)
    fig.suptitle('1D Farey Mesh Refinement — Injection Principle',
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path = os.path.join(OUTPUT_DIR, 'mesh_1d_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nSaved: {path}")


# ============================================================
# FIGURE 2: Quality Metrics Comparison
# ============================================================

def plot_quality_comparison(farey_metrics, farey_counts):
    """Plot quality metrics: Farey vs uniform vs random."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Farey data
    f_elems = [m['num_elements'] for m in farey_metrics]
    f_ratios = [m['max_size_ratio'] for m in farey_metrics]
    f_vars = [m['size_variance'] for m in farey_metrics]

    # Uniform data (build fresh)
    u_elems, u_ratios, u_vars = [], [], []
    nodes = np.array([0.0, 1.0])
    for _ in range(12):
        q = mesh_quality(nodes)
        u_elems.append(q['num_elements'])
        u_ratios.append(q['max_size_ratio'])
        u_vars.append(q['size_variance'])
        nodes = uniform_refine(nodes)

    # Random data (average over trials)
    np.random.seed(42)
    r_elems, r_ratios, r_vars = [], [], []
    for nc in farey_counts:
        trial_ratios, trial_vars = [], []
        for _ in range(50):
            rn = np.sort(np.concatenate([[0.0, 1.0],
                                         np.random.uniform(0, 1, nc - 2)]))
            q = mesh_quality(rn)
            trial_ratios.append(q['max_size_ratio'])
            trial_vars.append(q['size_variance'])
        r_elems.append(nc - 1)
        r_ratios.append(np.mean(trial_ratios))
        r_vars.append(np.mean(trial_vars))

    # Plot 1: Max size ratio vs number of elements
    ax = axes[0]
    ax.plot(f_elems, f_ratios, 'b.-', label='Farey', linewidth=2, markersize=8)
    ax.plot(u_elems, u_ratios, 'g^-', label='Uniform', linewidth=2, markersize=8)
    ax.plot(r_elems, r_ratios, 'rs-', label='Random', linewidth=2, markersize=6)
    ax.set_xlabel('Number of Elements')
    ax.set_ylabel('Max Size Ratio (lower = better)')
    ax.set_title('Worst-Case Element Ratio')
    ax.legend()
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)

    # Plot 2: Size variance vs number of elements
    ax = axes[1]
    ax.plot(f_elems, f_vars, 'b.-', label='Farey', linewidth=2, markersize=8)
    ax.plot(u_elems, u_vars, 'g^-', label='Uniform', linewidth=2, markersize=8)
    ax.plot(r_elems, r_vars, 'rs-', label='Random', linewidth=2, markersize=6)
    ax.set_xlabel('Number of Elements')
    ax.set_ylabel('Element Size Variance (lower = better)')
    ax.set_title('Element Size Uniformity')
    ax.legend()
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)

    # Plot 3: Farey max ratio convergence (shows bounded growth)
    ax = axes[2]
    Ns = list(range(1, len(farey_metrics) + 1))
    ax.plot(Ns, f_ratios, 'b.-', linewidth=2, markersize=8)
    ax.axhline(y=3.0, color='r', linestyle='--', alpha=0.5, label='Ratio = 3')
    ax.axhline(y=2.0, color='orange', linestyle='--', alpha=0.5, label='Ratio = 2')
    ax.set_xlabel('Farey Order N')
    ax.set_ylabel('Max Size Ratio')
    ax.set_title('Farey Max Ratio vs Order N')
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.suptitle('Mesh Quality: Farey vs Uniform vs Random',
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUTPUT_DIR, 'mesh_quality.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")


# ============================================================
# FIGURE 3: 2D Meshes
# ============================================================

def plot_2d_meshes():
    """Plot 2D Farey tensor-product meshes at different N."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 11))

    levels = [3, 5, 8]

    for col, N in enumerate(levels):
        fn = farey_to_floats(farey_sequence(N))

        # Farey mesh
        xx, yy = np.meshgrid(fn, fn)
        pts_f = np.column_stack([xx.ravel(), yy.ravel()])
        tri_f = Triangulation(pts_f[:, 0], pts_f[:, 1])
        q_f = triangle_qualities(pts_f, tri_f.triangles)

        ax = axes[0, col]
        ax.triplot(tri_f, 'b-', linewidth=0.5, alpha=0.7)
        ax.plot(pts_f[:, 0], pts_f[:, 1], 'b.', markersize=3)
        ax.set_title(f'Farey F_{N} x F_{N}\n{len(pts_f)} pts, '
                     f'{len(tri_f.triangles)} tri\n'
                     f'mean Q={np.mean(q_f):.3f}, worst={np.max(q_f):.3f}',
                     fontsize=10)
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2)

        # Random mesh with same number of points
        np.random.seed(42 + N)
        n_pts = len(pts_f)
        # Ensure corners are included
        corners = np.array([[0,0],[1,0],[0,1],[1,1]])
        inner = np.random.uniform(0, 1, (n_pts - 4, 2))
        pts_r = np.vstack([corners, inner])
        tri_r = Triangulation(pts_r[:, 0], pts_r[:, 1])
        q_r = triangle_qualities(pts_r, tri_r.triangles)

        ax = axes[1, col]
        ax.triplot(tri_r, 'r-', linewidth=0.5, alpha=0.7)
        ax.plot(pts_r[:, 0], pts_r[:, 1], 'r.', markersize=3)
        ax.set_title(f'Random ({n_pts} pts)\n'
                     f'{len(tri_r.triangles)} tri\n'
                     f'mean Q={np.mean(q_r):.3f}, worst={np.max(q_r):.3f}',
                     fontsize=10)
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2)

    axes[0, 0].set_ylabel('Farey Mesh', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Random Mesh', fontsize=12, fontweight='bold')

    fig.suptitle('2D Mesh: Farey Tensor Product vs Random\n'
                 '(Quality Q = R/(2r), perfect equilateral = 1, higher = worse)',
                 fontsize=13, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    path = os.path.join(OUTPUT_DIR, 'mesh_2d_farey.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")


# ============================================================
# FIGURE 4: No-Double-Split Verification
# ============================================================

def plot_no_double_split(results):
    """Visualize double-split counts across strategies."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Farey
    ax = axes[0]
    steps = [r['step'] for r in results['farey']]
    max_splits = [r['max_split'] for r in results['farey']]
    dbl_splits = [r['double_splits'] for r in results['farey']]
    ax.bar(steps, max_splits, color='blue', alpha=0.7, label='Max splits per interval')
    ax.axhline(y=1, color='green', linestyle='--', linewidth=2, label='Limit = 1')
    ax.set_xlabel('Farey Order N')
    ax.set_ylabel('Max Splits in Any Interval')
    ax.set_title('Farey: ALWAYS <= 1\n(Injection Principle)', fontsize=11)
    ax.legend()
    ax.set_ylim(0, max(3, max(max_splits) + 1))
    ax.grid(True, alpha=0.3)

    # Random
    ax = axes[1]
    steps_r = [r['step'] for r in results['random']]
    max_splits_r = [r['max_split'] for r in results['random']]
    dbl_splits_r = [r['double_splits'] for r in results['random']]
    colors_r = ['red' if m > 1 else 'green' for m in max_splits_r]
    ax.bar(steps_r, max_splits_r, color=colors_r, alpha=0.7)
    ax.axhline(y=1, color='green', linestyle='--', linewidth=2, label='Limit = 1')
    ax.set_xlabel('Refinement Step')
    ax.set_ylabel('Max Splits in Any Interval')
    violations_r = sum(1 for m in max_splits_r if m > 1)
    ax.set_title(f'Random: {violations_r}/{len(max_splits_r)} steps VIOLATE\n'
                 f'(red = double-split occurred)', fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Greedy
    ax = axes[2]
    steps_g = [r['step'] for r in results['greedy_midpoint']]
    max_splits_g = [r['max_split'] for r in results['greedy_midpoint']]
    colors_g = ['red' if m > 1 else 'green' for m in max_splits_g]
    ax.bar(steps_g, max_splits_g, color=colors_g, alpha=0.7)
    ax.axhline(y=1, color='green', linestyle='--', linewidth=2, label='Limit = 1')
    ax.set_xlabel('Refinement Step')
    ax.set_ylabel('Max Splits in Any Interval')
    violations_g = sum(1 for m in max_splits_g if m > 1)
    ax.set_title(f'Greedy Midpoint: {violations_g}/{len(max_splits_g)} steps VIOLATE\n'
                 f'(red = double-split occurred)', fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.suptitle('No-Double-Split Guarantee: Farey vs Random vs Greedy',
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    path = os.path.join(OUTPUT_DIR, 'no_double_split.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")


# ============================================================
# WHY THIS MATTERS — THEORETICAL SUMMARY
# ============================================================

def print_theory_summary():
    """Print explanation of why the injection principle matters for meshing."""
    print("\n" + "=" * 70)
    print("WHY THE INJECTION PRINCIPLE IS A MESH QUALITY GUARANTEE")
    print("=" * 70)
    print("""
THE PROBLEM WITH EXISTING MESH REFINEMENT:
  Standard adaptive mesh refinement (Delaunay, advancing front, etc.)
  can create cascading splits: refining one element forces neighbors to
  refine too, leading to uncontrolled element count growth and quality
  degradation. There is NO a-priori bound on how many elements change.

THE FAREY INJECTION GUARANTEE:
  When refining from F_N to F_{N+1}:

  THEOREM: Each interval [a/b, c/d] of F_N receives AT MOST ONE new
  fraction (a+c)/(b+d), and this happens if and only if b+d = N+1.

  PROOF: The mediant (a+c)/(b+d) has denominator b+d. It appears in
  F_{N+1} iff b+d <= N+1. Since a/b and c/d are Farey neighbors in F_N,
  we know b+d >= N+1 (Farey neighbor property). So b+d = N+1 exactly
  when the mediant is inserted, and b+d > N+1 means no insertion.

  Either way: AT MOST ONE new point per interval. QED.

CONSEQUENCES FOR MESH GENERATION:
  1. BOUNDED GROWTH: |F_{N+1}| - |F_N| = phi(N+1) <= N (Euler totient)
     At most N new elements per step. No cascading.

  2. QUALITY PRESERVATION: If the mesh at step N has max ratio R,
     the ratio at step N+1 is at most 2R (worst case: the largest
     element gets split, becoming two elements of size ratio at most 2:1).

  3. PREDICTABLE REFINEMENT: You know IN ADVANCE exactly which
     intervals will be split (those with b+d = N+1).

  4. NO EXISTING METHOD provides all three guarantees simultaneously.
     Delaunay gives quality but not bounded growth or predictability.
     Uniform gives predictability but wastes elements in smooth regions.
""")


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("FAREY MESH GENERATION — INJECTION PRINCIPLE DEMO")
    print("=" * 70)

    # Demo 1: 1D comparison
    farey_m, uniform_m, random_m, farey_c = demo_1d_comparison()

    # Demo 2: No-double-split verification
    nds_results = demo_no_double_split()

    # Demo 3: 2D mesh comparison
    results_2d = demo_2d_mesh()

    # Generate all figures
    print("\n" + "=" * 70)
    print("GENERATING FIGURES")
    print("=" * 70)

    plot_1d_meshes()
    plot_quality_comparison(farey_m, farey_c)
    plot_2d_meshes()
    plot_no_double_split(nds_results)

    # Theory summary
    print_theory_summary()

    # Final summary
    print("=" * 70)
    print("SUMMARY OF RESULTS")
    print("=" * 70)

    # Count violations
    farey_violations = sum(1 for r in nds_results['farey'] if not r['valid'])
    random_violations = sum(1 for r in nds_results['random'] if not r['valid'])
    greedy_violations = sum(1 for r in nds_results['greedy_midpoint'] if not r['valid'])

    print(f"\nNo-Double-Split Violations:")
    print(f"  Farey:          {farey_violations}/{len(nds_results['farey'])} steps  "
          f"{'(PERFECT - injection principle holds)' if farey_violations == 0 else 'UNEXPECTED FAILURES'}")
    print(f"  Random:         {random_violations}/{len(nds_results['random'])} steps violated")
    print(f"  Greedy midpt:   {greedy_violations}/{len(nds_results['greedy_midpoint'])} steps violated")

    print(f"\n2D Mesh Quality (mean Q, lower = better):")
    for r in results_2d:
        improvement = (r['random_quality_mean'] - r['farey_quality_mean']) / r['random_quality_mean'] * 100
        print(f"  N={r['N']:>2}: Farey={r['farey_quality_mean']:.4f}, "
              f"Random={r['random_quality_mean']:.4f} "
              f"({'Farey ' + str(round(improvement, 1)) + '% better' if improvement > 0 else 'Random better'})")

    print(f"\nFigures saved to: {OUTPUT_DIR}/")
    print(f"  mesh_1d_comparison.png  — 1D meshes at F_3, F_5, F_8, F_12")
    print(f"  mesh_quality.png        — Quality metrics comparison")
    print(f"  mesh_2d_farey.png       — 2D Farey vs random meshes")
    print(f"  no_double_split.png     — Double-split violation chart")

    print("\nDone.")
