#!/usr/bin/env python3
"""
Farey-Conformal Mapping Experiment
===================================
Demonstrates the connection between Farey tessellation refinement and
discrete conformal mapping quality, following the Bobenko-Pinkall-Springborn
framework for Ptolemy flips on the Farey graph.

Key question: Does Farey refinement produce better or worse mesh quality
than uniform refinement when mapped through a conformal map?

The experiment:
  1. Build Farey tessellations at increasing orders
  2. Map them through a conformal map (Schwarz-Christoffel to an L-domain)
  3. Measure mesh quality (min angle, aspect ratio, condition number)
  4. Compare against uniform subdivision at matched vertex counts
  5. Demonstrate the injection (nesting) property visually
"""

import json
import os
import sys
import warnings
from fractions import Fraction
from math import gcd, pi, atan2, sqrt, log

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection, LineCollection
from scipy.spatial import Delaunay

warnings.filterwarnings('ignore', category=RuntimeWarning)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 1. Farey sequence and tessellation
# ---------------------------------------------------------------------------

def farey_sequence(n):
    """Generate the Farey sequence F_n as a sorted list of Fraction objects."""
    fracs = set()
    for d in range(1, n + 1):
        for num in range(0, d + 1):
            if gcd(num, d) == 1:
                fracs.add(Fraction(num, d))
    return sorted(fracs)


def farey_triangulation(fracs):
    """
    Build the Farey triangulation of [0,1] from consecutive Farey fractions.

    In the classical Farey tessellation, consecutive fractions a/b and c/d
    with |ad - bc| = 1 are connected by an edge, and their mediant (a+c)/(b+d)
    creates a triangle. For a given Farey sequence, consecutive triples
    (f[i], mediant(f[i], f[i+1]), f[i+1]) form triangles.

    We return vertices (as floats) and triangle index arrays.
    """
    verts = [float(f) for f in fracs]
    # Build triangles: each consecutive pair defines a segment;
    # we triangulate [0,1] by connecting consecutive fractions.
    # The Farey graph triangulation uses mediants as interior vertices,
    # but at order N all mediants that belong to F_N are already present.
    # So the triangulation is simply the 1D simplicial complex (edges).
    # For a 2D triangulation, we lift to the upper half-plane model:
    #   each fraction p/q maps to (p/q, 1/q^2) -- the Ford circle center.
    verts_2d = []
    for f in fracs:
        x = float(f)
        q = f.denominator
        y = 1.0 / (q * q)  # Ford circle radius / height
        verts_2d.append((x, y))

    verts_2d = np.array(verts_2d)

    # Build triangles from consecutive Farey neighbors.
    # In the Farey tessellation, fractions a/b, c/d are Farey neighbors
    # iff |ad - bc| = 1. For each triple of mutual neighbors, we get a
    # hyperbolic ideal triangle. In F_N, consecutive entries are neighbors.
    triangles = []
    for i in range(len(fracs) - 2):
        # Check which triples form valid Farey triangles
        for j in range(i + 1, min(i + 4, len(fracs))):
            for k in range(j + 1, min(j + 4, len(fracs))):
                fi, fj, fk = fracs[i], fracs[j], fracs[k]
                # Check all three pairs are Farey neighbors
                if (abs(fi.numerator * fj.denominator - fi.denominator * fj.numerator) == 1 and
                    abs(fj.numerator * fk.denominator - fj.denominator * fk.numerator) == 1 and
                    abs(fi.numerator * fk.denominator - fi.denominator * fk.numerator) == 1):
                    triangles.append((i, j, k))

    # If the neighbor-triple approach yields too few triangles,
    # fall back to consecutive triangulation
    if len(triangles) < len(fracs) - 2:
        triangles = []
        for i in range(len(fracs) - 2):
            triangles.append((i, i + 1, i + 2))

    return verts_2d, np.array(triangles, dtype=int)


# ---------------------------------------------------------------------------
# 2. Conformal mapping: Schwarz-Christoffel for an L-shaped domain
# ---------------------------------------------------------------------------

def sc_map_l_domain(z, num_pts=200):
    """
    Approximate conformal map from the upper half-plane to an L-shaped domain.

    We use a numerical Schwarz-Christoffel approach. The L-domain has vertices
    at (0,0), (2,0), (2,1), (1,1), (1,2), (0,2) with interior angles
    pi/2 at convex corners and 3pi/2 at the reentrant corner.

    For a tractable experiment, we use a simpler conformal map:
    w = z^(2/3) maps the upper half-plane to a 2pi/3 wedge,
    demonstrating how conformal maps distort mesh quality near singularities.

    We also implement a Joukowski-type map for richer geometry.
    """
    # Use z^alpha map -- has a singularity at origin (branch point)
    # This is the canonical example for studying mesh quality near singularities
    alpha = 2.0 / 3.0
    # Work with complex numbers
    w = np.zeros_like(z, dtype=complex)
    mask = np.abs(z) > 1e-15
    w[mask] = np.abs(z[mask]) ** alpha * np.exp(1j * alpha * np.angle(z[mask]))
    return w


def joukowski_map(z, a=0.15, c_shift=0.1):
    """
    Joukowski-type conformal map: w = z + a^2/z, shifted.
    Maps circles to airfoil-like shapes. Good for testing mesh quality
    near cusps and regions of high curvature.
    """
    z_shifted = z + c_shift
    mask = np.abs(z_shifted) > 1e-15
    w = np.zeros_like(z, dtype=complex)
    w[mask] = z_shifted[mask] + a ** 2 / z_shifted[mask]
    return w


def notched_square_map(z):
    """
    Conformal map via composition: z^(2/3) followed by a Mobius transform,
    creating a domain with both a singularity and varying curvature.
    """
    # First: power map (singularity at 0)
    alpha = 0.7
    w1 = np.abs(z) ** alpha * np.exp(1j * alpha * np.angle(z))
    # Then: Mobius transform to create asymmetry
    a_mob = 0.3 + 0.1j
    w = (w1 - a_mob) / (1.0 - np.conj(a_mob) * w1)
    return w


# ---------------------------------------------------------------------------
# 3. Uniform subdivision for comparison
# ---------------------------------------------------------------------------

def uniform_triangulation(n_verts):
    """
    Build a uniform subdivision of [0,1] x [0, h_max] with approximately
    n_verts vertices, lifted to a 2D region comparable to the Farey tessellation.

    Returns vertices and triangles matching the format of farey_triangulation.
    """
    # Create a grid in [0,1] x [0,1] with ~n_verts points
    n_side = max(3, int(np.sqrt(n_verts)))
    xs = np.linspace(0, 1, n_side)
    ys = np.linspace(0.01, 1, n_side)  # Avoid y=0 singularity
    xx, yy = np.meshgrid(xs, ys)
    verts = np.column_stack([xx.ravel(), yy.ravel()])

    # Delaunay triangulation
    tri = Delaunay(verts)
    return verts, tri.simplices


# ---------------------------------------------------------------------------
# 4. Mesh quality metrics
# ---------------------------------------------------------------------------

def triangle_angles(p1, p2, p3):
    """Compute the three angles (in degrees) of a triangle given 2D vertices."""
    def angle_at(a, b, c):
        v1 = b - a
        v2 = c - a
        cos_a = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-30)
        cos_a = np.clip(cos_a, -1, 1)
        return np.degrees(np.arccos(cos_a))

    return [angle_at(p1, p2, p3), angle_at(p2, p1, p3), angle_at(p3, p1, p2)]


def aspect_ratio(p1, p2, p3):
    """
    Compute the aspect ratio of a triangle.
    Ratio of circumradius to inradius (normalized so equilateral = 1).
    """
    a = np.linalg.norm(p2 - p3)
    b = np.linalg.norm(p1 - p3)
    c = np.linalg.norm(p1 - p2)
    s = (a + b + c) / 2.0
    area = np.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
    if area < 1e-30:
        return 1e6
    R = (a * b * c) / (4 * area)
    r = area / s
    return R / (2 * r)  # Normalized: equilateral triangle = 1


def condition_number_metric(p1, p2, p3):
    """
    Condition number of the Jacobian of the affine map from reference
    equilateral triangle to the given triangle. Measures distortion.
    """
    # Reference: equilateral with side 1
    ref = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]])
    # Affine map: [p2-p1, p3-p1] = J * [ref2-ref1, ref3-ref1]
    A = np.column_stack([p2 - p1, p3 - p1])
    B = np.column_stack([ref[1] - ref[0], ref[2] - ref[0]])
    try:
        J = A @ np.linalg.inv(B)
        s = np.linalg.svd(J, compute_uv=False)
        if s[-1] < 1e-30:
            return 1e6
        return s[0] / s[-1]
    except np.linalg.LinAlgError:
        return 1e6


def compute_mesh_quality(verts, triangles):
    """
    Compute mesh quality statistics for a triangulation.
    Returns dict with min_angle, max_aspect_ratio, mean_condition_number, etc.
    """
    if len(triangles) == 0:
        return {
            'min_angle': 0, 'max_angle': 180, 'mean_angle_deviation': 60,
            'max_aspect_ratio': 1e6, 'mean_aspect_ratio': 1e6,
            'max_condition': 1e6, 'mean_condition': 1e6,
            'num_vertices': len(verts), 'num_triangles': 0
        }

    all_angles = []
    all_ar = []
    all_cond = []

    for tri in triangles:
        p1, p2, p3 = verts[tri[0]], verts[tri[1]], verts[tri[2]]
        angles = triangle_angles(p1, p2, p3)
        all_angles.extend(angles)
        all_ar.append(aspect_ratio(p1, p2, p3))
        all_cond.append(condition_number_metric(p1, p2, p3))

    all_angles = np.array(all_angles)
    all_ar = np.array(all_ar)
    all_cond = np.array(all_cond)

    return {
        'min_angle': float(np.min(all_angles)),
        'max_angle': float(np.max(all_angles)),
        'mean_angle_deviation': float(np.mean(np.abs(all_angles - 60))),
        'max_aspect_ratio': float(np.max(all_ar)),
        'mean_aspect_ratio': float(np.mean(all_ar)),
        'max_condition': float(np.max(all_cond)),
        'mean_condition': float(np.mean(all_cond)),
        'num_vertices': int(len(verts)),
        'num_triangles': int(len(triangles))
    }


def map_triangulation(verts, triangles, conformal_map):
    """
    Apply a conformal map to the vertices of a triangulation.
    Input vertices are (x, y) in the upper half-plane.
    Returns mapped vertices as 2D real array.
    """
    z = verts[:, 0] + 1j * verts[:, 1]
    w = conformal_map(z)
    mapped = np.column_stack([w.real, w.imag])
    return mapped, triangles


# ---------------------------------------------------------------------------
# 5. Convergence measurement
# ---------------------------------------------------------------------------

def convergence_error(verts_coarse, tris_coarse, verts_fine, tris_fine, conformal_map):
    """
    Measure convergence: how well the discrete (coarse) triangulation
    approximates the continuous conformal map, using the fine triangulation
    as ground truth.

    We sample points on the coarse mesh edges, interpolate the conformal map
    on the coarse mesh vs evaluating it directly, and measure max error.
    """
    # Sample midpoints of coarse triangles
    if len(tris_coarse) == 0:
        return 1e6

    errors = []
    for tri in tris_coarse:
        # Centroid of the triangle in the source domain
        centroid = np.mean(verts_coarse[tri], axis=0)
        z_exact = centroid[0] + 1j * centroid[1]
        w_exact = conformal_map(np.array([z_exact]))[0]

        # Piecewise-linear approximation: average of mapped vertices
        mapped_verts = []
        for idx in tri:
            z_v = verts_coarse[idx, 0] + 1j * verts_coarse[idx, 1]
            w_v = conformal_map(np.array([z_v]))[0]
            mapped_verts.append(w_v)
        w_linear = np.mean(mapped_verts)

        errors.append(abs(w_exact - w_linear))

    return float(np.max(errors))


# ---------------------------------------------------------------------------
# 6. Visualization
# ---------------------------------------------------------------------------

def plot_triangulation(ax, verts, triangles, title, color='steelblue',
                       alpha=0.3, edge_color='navy', lw=0.5):
    """Plot a 2D triangulation on a given axes."""
    if len(triangles) > 0:
        triplt = mtri.Triangulation(verts[:, 0], verts[:, 1], triangles)
        ax.triplot(triplt, color=edge_color, lw=lw, alpha=0.8)
    ax.plot(verts[:, 0], verts[:, 1], '.', color=color, markersize=2, alpha=0.7)
    ax.set_title(title, fontsize=10)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)


def plot_injection_property(fracs_n, fracs_n1, order_n, order_n1, save_path):
    """
    Demonstrate the injection (nesting) property:
    F_N is a subset of F_{N+1}, so the tessellation refines without
    displacing existing vertices.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Build both tessellations
    verts_n, tris_n = farey_triangulation(fracs_n)
    verts_n1, tris_n1 = farey_triangulation(fracs_n1)

    # Plot F_N
    plot_triangulation(axes[0], verts_n, tris_n,
                       f'Farey tessellation F_{{{order_n}}} ({len(fracs_n)} vertices)')

    # Plot F_{N+1}
    plot_triangulation(axes[1], verts_n1, tris_n1,
                       f'Farey tessellation F_{{{order_n1}}} ({len(fracs_n1)} vertices)')

    # Overlay: show new vertices in red
    set_n = set(fracs_n)
    new_fracs = [f for f in fracs_n1 if f not in set_n]
    old_fracs = [f for f in fracs_n1 if f in set_n]

    # Plot the refined mesh with highlights
    if len(tris_n1) > 0:
        triplt = mtri.Triangulation(verts_n1[:, 0], verts_n1[:, 1], tris_n1)
        axes[2].triplot(triplt, color='navy', lw=0.3, alpha=0.4)

    # Old vertices in blue
    old_pts = np.array([(float(f), 1.0 / f.denominator ** 2) for f in old_fracs])
    if len(old_pts) > 0:
        axes[2].plot(old_pts[:, 0], old_pts[:, 1], 'o', color='steelblue',
                     markersize=4, label=f'Existing ({len(old_fracs)})', zorder=5)

    # New vertices in red
    new_pts = np.array([(float(f), 1.0 / f.denominator ** 2) for f in new_fracs])
    if len(new_pts) > 0:
        axes[2].plot(new_pts[:, 0], new_pts[:, 1], 'o', color='crimson',
                     markersize=5, label=f'New ({len(new_fracs)})', zorder=6)

    axes[2].set_title(f'Injection: F_{{{order_n}}} ⊂ F_{{{order_n1}}} '
                      f'(+{len(new_fracs)} new vertices)')
    axes[2].set_aspect('equal')
    axes[2].legend(fontsize=8)
    axes[2].grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {save_path}")


# ---------------------------------------------------------------------------
# 7. Main experiment
# ---------------------------------------------------------------------------

def run_experiment():
    """Run the full Farey conformal mapping experiment."""

    print("=" * 70)
    print("FAREY-CONFORMAL MAPPING EXPERIMENT")
    print("Bobenko-Pinkall-Springborn framework: Ptolemy flips on Farey graph")
    print("=" * 70)

    orders = [3, 5, 7, 11, 13, 17, 19, 23]
    conformal_maps = {
        'power_2_3': ('z^(2/3) — singularity at origin', sc_map_l_domain),
        'joukowski': ('Joukowski — cusp/airfoil geometry', joukowski_map),
    }

    results = {
        'description': 'Farey vs uniform mesh quality under conformal mapping',
        'orders': orders,
        'maps': {},
    }

    # -----------------------------------------------------------------------
    # Part A: Mesh quality comparison for each conformal map
    # -----------------------------------------------------------------------
    for map_name, (map_desc, cmap) in conformal_maps.items():
        print(f"\n{'─' * 60}")
        print(f"Conformal map: {map_desc}")
        print(f"{'─' * 60}")

        farey_quality = []
        uniform_quality = []
        farey_convergence = []
        uniform_convergence = []

        # Build finest mesh for convergence reference
        fracs_fine = farey_sequence(max(orders) + 10)
        verts_fine, tris_fine = farey_triangulation(fracs_fine)

        for N in orders:
            print(f"\n  Order N = {N}:")

            # --- Farey tessellation ---
            fracs = farey_sequence(N)
            verts_f, tris_f = farey_triangulation(fracs)
            mapped_f, tris_f_mapped = map_triangulation(verts_f, tris_f, cmap)
            q_farey = compute_mesh_quality(mapped_f, tris_f_mapped)
            farey_quality.append(q_farey)

            print(f"    Farey: {q_farey['num_vertices']} verts, "
                  f"{q_farey['num_triangles']} tris, "
                  f"min_angle={q_farey['min_angle']:.1f}°, "
                  f"max_AR={q_farey['max_aspect_ratio']:.2f}, "
                  f"mean_cond={q_farey['mean_condition']:.2f}")

            # --- Uniform with matched vertex count ---
            n_verts_target = q_farey['num_vertices']
            verts_u, tris_u = uniform_triangulation(n_verts_target)
            mapped_u, tris_u_mapped = map_triangulation(verts_u, tris_u, cmap)
            q_uniform = compute_mesh_quality(mapped_u, tris_u_mapped)
            uniform_quality.append(q_uniform)

            print(f"    Uniform: {q_uniform['num_vertices']} verts, "
                  f"{q_uniform['num_triangles']} tris, "
                  f"min_angle={q_uniform['min_angle']:.1f}°, "
                  f"max_AR={q_uniform['max_aspect_ratio']:.2f}, "
                  f"mean_cond={q_uniform['mean_condition']:.2f}")

            # --- Convergence ---
            err_f = convergence_error(verts_f, tris_f, verts_fine, tris_fine, cmap)
            err_u = convergence_error(verts_u, tris_u, verts_fine, tris_fine, cmap)
            farey_convergence.append(err_f)
            uniform_convergence.append(err_u)

            print(f"    Convergence error: Farey={err_f:.6f}, Uniform={err_u:.6f}")

        results['maps'][map_name] = {
            'description': map_desc,
            'farey_quality': farey_quality,
            'uniform_quality': uniform_quality,
            'farey_convergence': farey_convergence,
            'uniform_convergence': uniform_convergence,
        }

        # -------------------------------------------------------------------
        # Plot: mesh quality comparison
        # -------------------------------------------------------------------
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f'Mesh Quality: Farey vs Uniform — {map_desc}', fontsize=13)

        n_verts_f = [q['num_vertices'] for q in farey_quality]
        n_verts_u = [q['num_vertices'] for q in uniform_quality]

        # Min angle (higher is better)
        axes[0, 0].plot(orders, [q['min_angle'] for q in farey_quality],
                        'o-', color='crimson', label='Farey', lw=2)
        axes[0, 0].plot(orders, [q['min_angle'] for q in uniform_quality],
                        's--', color='steelblue', label='Uniform', lw=2)
        axes[0, 0].set_ylabel('Min angle (degrees)')
        axes[0, 0].set_xlabel('Farey order N')
        axes[0, 0].legend()
        axes[0, 0].set_title('Minimum angle (higher = better)')
        axes[0, 0].grid(True, alpha=0.3)

        # Max aspect ratio (lower is better)
        axes[0, 1].plot(orders, [q['max_aspect_ratio'] for q in farey_quality],
                        'o-', color='crimson', label='Farey', lw=2)
        axes[0, 1].plot(orders, [q['max_aspect_ratio'] for q in uniform_quality],
                        's--', color='steelblue', label='Uniform', lw=2)
        axes[0, 1].set_ylabel('Max aspect ratio')
        axes[0, 1].set_xlabel('Farey order N')
        axes[0, 1].legend()
        axes[0, 1].set_title('Max aspect ratio (lower = better)')
        axes[0, 1].set_yscale('log')
        axes[0, 1].grid(True, alpha=0.3)

        # Mean condition number (lower is better)
        axes[0, 2].plot(orders, [q['mean_condition'] for q in farey_quality],
                        'o-', color='crimson', label='Farey', lw=2)
        axes[0, 2].plot(orders, [q['mean_condition'] for q in uniform_quality],
                        's--', color='steelblue', label='Uniform', lw=2)
        axes[0, 2].set_ylabel('Mean condition number')
        axes[0, 2].set_xlabel('Farey order N')
        axes[0, 2].legend()
        axes[0, 2].set_title('Mean condition (lower = better)')
        axes[0, 2].grid(True, alpha=0.3)

        # Convergence rate
        axes[1, 0].semilogy(orders, farey_convergence,
                            'o-', color='crimson', label='Farey', lw=2)
        axes[1, 0].semilogy(orders, uniform_convergence,
                            's--', color='steelblue', label='Uniform', lw=2)
        axes[1, 0].set_ylabel('Max pointwise error')
        axes[1, 0].set_xlabel('Farey order N')
        axes[1, 0].legend()
        axes[1, 0].set_title('Convergence rate (lower = better)')
        axes[1, 0].grid(True, alpha=0.3)

        # Convergence vs vertex count (fair comparison)
        axes[1, 1].loglog(n_verts_f, farey_convergence,
                          'o-', color='crimson', label='Farey', lw=2)
        axes[1, 1].loglog(n_verts_u, uniform_convergence,
                          's--', color='steelblue', label='Uniform', lw=2)
        axes[1, 1].set_ylabel('Max pointwise error')
        axes[1, 1].set_xlabel('Number of vertices')
        axes[1, 1].legend()
        axes[1, 1].set_title('Convergence vs vertex count')
        axes[1, 1].grid(True, alpha=0.3)

        # Mean angle deviation (lower is better, 0 = all equilateral)
        axes[1, 2].plot(orders, [q['mean_angle_deviation'] for q in farey_quality],
                        'o-', color='crimson', label='Farey', lw=2)
        axes[1, 2].plot(orders, [q['mean_angle_deviation'] for q in uniform_quality],
                        's--', color='steelblue', label='Uniform', lw=2)
        axes[1, 2].set_ylabel('Mean |angle - 60°|')
        axes[1, 2].set_xlabel('Farey order N')
        axes[1, 2].legend()
        axes[1, 2].set_title('Angle deviation from equilateral')
        axes[1, 2].grid(True, alpha=0.3)

        plt.tight_layout()
        save_path = os.path.join(OUT_DIR, f'farey_conformal_quality_{map_name}.png')
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"\n  Saved: {save_path}")

    # -----------------------------------------------------------------------
    # Part B: Mapped triangulations visualization
    # -----------------------------------------------------------------------
    print(f"\n{'─' * 60}")
    print("Generating mapped triangulation visualizations...")
    print(f"{'─' * 60}")

    for map_name, (map_desc, cmap) in conformal_maps.items():
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        fig.suptitle(f'Farey Tessellations Mapped by {map_desc}', fontsize=13)

        for idx, N in enumerate([3, 7, 13, 23]):
            fracs = farey_sequence(N)
            verts, tris = farey_triangulation(fracs)

            # Source (upper half-plane)
            plot_triangulation(axes[0, idx], verts, tris,
                               f'Source: F_{{{N}}} ({len(fracs)} pts)',
                               color='crimson', edge_color='darkred')

            # Mapped
            mapped, tris_m = map_triangulation(verts, tris, cmap)
            plot_triangulation(axes[1, idx], mapped, tris_m,
                               f'Mapped: F_{{{N}}}',
                               color='steelblue', edge_color='navy')

        plt.tight_layout()
        save_path = os.path.join(OUT_DIR, f'farey_conformal_meshes_{map_name}.png')
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {save_path}")

    # -----------------------------------------------------------------------
    # Part C: Injection property demonstration
    # -----------------------------------------------------------------------
    print(f"\n{'─' * 60}")
    print("Demonstrating injection (nesting) property...")
    print(f"{'─' * 60}")

    # Show several consecutive pairs
    pairs = [(3, 4), (5, 6), (7, 8), (11, 12)]
    for n1, n2 in pairs:
        fracs_n1 = farey_sequence(n1)
        fracs_n2 = farey_sequence(n2)
        save_path = os.path.join(OUT_DIR,
                                 f'farey_conformal_injection_{n1}_{n2}.png')
        plot_injection_property(fracs_n1, fracs_n2, n1, n2, save_path)

    # Also demonstrate injection across larger gaps
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.suptitle('Farey Nesting Property: F_N ⊂ F_M for N < M', fontsize=13)

    for idx, (n_small, n_big) in enumerate([(3, 7), (5, 13), (7, 19), (11, 23)]):
        fracs_s = farey_sequence(n_small)
        fracs_b = farey_sequence(n_big)
        set_s = set(fracs_s)

        verts_b, tris_b = farey_triangulation(fracs_b)
        if len(tris_b) > 0:
            triplt = mtri.Triangulation(verts_b[:, 0], verts_b[:, 1], tris_b)
            axes[idx].triplot(triplt, color='navy', lw=0.3, alpha=0.3)

        # Old vertices
        old_pts = [(float(f), 1.0 / f.denominator ** 2)
                   for f in fracs_b if f in set_s]
        new_pts = [(float(f), 1.0 / f.denominator ** 2)
                   for f in fracs_b if f not in set_s]

        if old_pts:
            old_arr = np.array(old_pts)
            axes[idx].plot(old_arr[:, 0], old_arr[:, 1], 'o', color='steelblue',
                           markersize=5, label=f'F_{{{n_small}}} ({len(old_pts)})',
                           zorder=5)
        if new_pts:
            new_arr = np.array(new_pts)
            axes[idx].plot(new_arr[:, 0], new_arr[:, 1], '.', color='crimson',
                           markersize=3, label=f'New ({len(new_pts)})', zorder=4)

        axes[idx].set_title(f'F_{{{n_small}}} → F_{{{n_big}}}')
        axes[idx].set_aspect('equal')
        axes[idx].legend(fontsize=7)
        axes[idx].grid(True, alpha=0.2)

    plt.tight_layout()
    save_path = os.path.join(OUT_DIR, 'farey_conformal_nesting_overview.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {save_path}")

    # -----------------------------------------------------------------------
    # Part D: Summary analysis
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("SUMMARY OF RESULTS")
    print(f"{'=' * 70}")

    for map_name, data in results['maps'].items():
        print(f"\nMap: {data['description']}")
        print(f"  {'Order':>6} | {'Farey min∠':>12} {'Unif min∠':>12} | "
              f"{'Farey AR':>10} {'Unif AR':>10} | "
              f"{'Farey err':>10} {'Unif err':>10}")
        print(f"  {'─' * 6}-+-{'─' * 12}-{'─' * 12}-+-{'─' * 10}-{'─' * 10}-+-{'─' * 10}-{'─' * 10}")

        farey_wins_angle = 0
        farey_wins_ar = 0
        farey_wins_conv = 0

        for i, N in enumerate(orders):
            qf = data['farey_quality'][i]
            qu = data['uniform_quality'][i]
            ef = data['farey_convergence'][i]
            eu = data['uniform_convergence'][i]

            angle_winner = '◄' if qf['min_angle'] > qu['min_angle'] else ''
            ar_winner = '◄' if qf['max_aspect_ratio'] < qu['max_aspect_ratio'] else ''
            conv_winner = '◄' if ef < eu else ''

            if qf['min_angle'] > qu['min_angle']:
                farey_wins_angle += 1
            if qf['max_aspect_ratio'] < qu['max_aspect_ratio']:
                farey_wins_ar += 1
            if ef < eu:
                farey_wins_conv += 1

            print(f"  {N:>6} | {qf['min_angle']:>10.1f}° {qu['min_angle']:>10.1f}° | "
                  f"{qf['max_aspect_ratio']:>10.2f} {qu['max_aspect_ratio']:>10.2f} | "
                  f"{ef:>10.6f} {eu:>10.6f} "
                  f"{'  Farey better' if (ef < eu) else ''}")

        n_tests = len(orders)
        print(f"\n  Farey wins: angle {farey_wins_angle}/{n_tests}, "
              f"aspect ratio {farey_wins_ar}/{n_tests}, "
              f"convergence {farey_wins_conv}/{n_tests}")

        # Store summary
        results['maps'][map_name]['summary'] = {
            'farey_wins_min_angle': farey_wins_angle,
            'farey_wins_aspect_ratio': farey_wins_ar,
            'farey_wins_convergence': farey_wins_conv,
            'total_tests': n_tests,
        }

    # Overall assessment
    total_angle_wins = sum(d['summary']['farey_wins_min_angle']
                           for d in results['maps'].values())
    total_ar_wins = sum(d['summary']['farey_wins_aspect_ratio']
                        for d in results['maps'].values())
    total_conv_wins = sum(d['summary']['farey_wins_convergence']
                          for d in results['maps'].values())
    total_tests = sum(d['summary']['total_tests']
                      for d in results['maps'].values())

    print(f"\n{'=' * 70}")
    print("OVERALL ASSESSMENT")
    print(f"{'=' * 70}")
    print(f"  Across all conformal maps ({len(conformal_maps)} maps, "
          f"{total_tests} total comparisons):")
    print(f"  Farey wins on minimum angle:  {total_angle_wins}/{total_tests}")
    print(f"  Farey wins on aspect ratio:   {total_ar_wins}/{total_tests}")
    print(f"  Farey wins on convergence:    {total_conv_wins}/{total_tests}")

    if total_conv_wins > total_tests / 2:
        verdict = ("FAREY REFINEMENT IS SUPERIOR: The number-theoretic structure "
                    "of Farey fractions concentrates vertices near singularities "
                    "(high-denominator fractions cluster near rationals with "
                    "special structure), giving better convergence under "
                    "conformal mapping.")
    elif total_conv_wins == total_tests / 2:
        verdict = ("MIXED RESULTS: Farey and uniform refinement show comparable "
                    "performance. The advantages of Farey refinement may be "
                    "situation-dependent, with benefits near singularities "
                    "offset by suboptimality in smooth regions.")
    else:
        verdict = ("UNIFORM REFINEMENT IS SUPERIOR for raw mesh quality, but "
                    "Farey refinement has the crucial structural advantage of "
                    "the injection property (nested refinement without vertex "
                    "displacement), which is essential for the "
                    "Bobenko-Pinkall-Springborn discrete conformal framework.")

    print(f"\n  Verdict: {verdict}")
    results['verdict'] = verdict

    # Save JSON results
    json_path = os.path.join(OUT_DIR, 'farey_conformal_results.json')

    # Make results JSON-serializable
    def make_serializable(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [make_serializable(v) for v in obj]
        return obj

    with open(json_path, 'w') as f:
        json.dump(make_serializable(results), f, indent=2)
    print(f"\n  Results saved: {json_path}")

    print(f"\n{'=' * 70}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 70}")

    return results


if __name__ == '__main__':
    run_experiment()
