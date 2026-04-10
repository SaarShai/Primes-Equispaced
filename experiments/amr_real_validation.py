#!/usr/bin/env python3
"""
AMR REAL-WORLD VALIDATION EXPERIMENTS
======================================

Validates the claimed 15-25% total cell count reduction of Farey AMR vs standard AMR
using realistic test functions (not toy sine waves).

Experiments:
  1. Realistic 2D flow fields (Lamb-Oseen vortex, Sod shock tube, KH instability)
  2. 3D extension (tensor product Farey^3)
  3. Comparison against p4est/AMReX-like refinement patterns
  4. Actual compute time measurement (heat equation solve)

Outputs:
  amr_validation_exp1.png  — Experiment 1 results
  amr_validation_exp2.png  — Experiment 2 results
  amr_validation_exp3.png  — Experiment 3 results
  amr_validation_exp4.png  — Experiment 4 results
  AMR_VALIDATION_RESULTS.md — Full report
"""

import os
import sys
import time
import json
import numpy as np
from fractions import Fraction
from math import gcd, pi
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# CORE: FAREY SEQUENCE TOOLS
# ============================================================

def farey_sequence(N):
    """Generate Farey sequence F_N."""
    fracs = set()
    for d in range(1, N + 1):
        for n in range(0, d + 1):
            if gcd(n, d) == 1:
                fracs.add(Fraction(n, d))
    return sorted(fracs)


def farey_refine_cell(left, right, current_N, target_N):
    """Refine a single cell [left, right] from level current_N to target_N."""
    new_nodes = []
    for d in range(current_N + 1, target_N + 1):
        for n in range(0, d + 1):
            if gcd(n, d) == 1:
                f = Fraction(n, d)
                if left < f < right:
                    new_nodes.append(f)
    return sorted(new_nodes)


# ============================================================
# REALISTIC TEST FUNCTIONS
# ============================================================

def lamb_oseen_vortex(x, y):
    """Lamb-Oseen vortex vorticity field. Smooth, radially symmetric."""
    nu, t, Gamma = 0.01, 1.0, 1.0
    r2 = (x - 0.5)**2 + (y - 0.5)**2 + 1e-12
    return (Gamma / (4 * pi * nu * t)) * np.exp(-r2 / (4 * nu * t))


def sod_shock_tube_2d(x, y):
    """Sod shock tube at t=0.2. Sharp discontinuities + smooth regions."""
    x_head, x_tail, x_contact, x_shock = 0.2634, 0.4858, 0.6854, 0.8504
    rho = np.where(x < x_head, 1.0,
          np.where(x < x_tail, 1.0 - 0.573 * (x - x_head) / (x_tail - x_head),
          np.where(x < x_contact, 0.427,
          np.where(x < x_shock, 0.265, 0.125))))
    return rho * (1.0 + 0.1 * np.sin(2 * pi * y))


def kelvin_helmholtz(x, y):
    """KH instability: shear layers + perturbation modes."""
    delta = 0.05
    u = 0.5 * (np.tanh((y - 0.25) / delta) - np.tanh((y - 0.75) / delta) - 1.0)
    pert = (0.01 * np.sin(2*pi*x) * np.exp(-((y-0.25)/delta)**2)
          + 0.01 * np.sin(4*pi*x) * np.exp(-((y-0.75)/delta)**2)
          + 0.003 * np.sin(6*pi*x) * np.exp(-((y-0.5)/(2*delta))**2))
    return u + pert * 2.0


def multi_scale_features(x, y):
    """Features at 3 different length scales — hardest for AMR."""
    large = np.exp(-5 * ((x-0.5)**2 + (y-0.5)**2))
    r = np.sqrt((x-0.5)**2 + (y-0.5)**2)
    medium = 0.5 * np.exp(-100 * (r-0.3)**2)
    small = (0.3 * np.exp(-500*((x-0.2)**2+(y-0.8)**2))
           + 0.3 * np.exp(-500*((x-0.8)**2+(y-0.2)**2))
           + 0.3 * np.exp(-500*((x-0.7)**2+(y-0.7)**2)))
    return large + medium + small


def spherical_blast_3d(x, y, z):
    """3D spherical blast wave."""
    r = np.sqrt((x-0.5)**2 + (y-0.5)**2 + (z-0.5)**2) + 1e-12
    r0, delta = 0.3, 0.02
    return np.where(r < r0-delta, 1.0,
           np.where(r < r0+delta, 0.5*(1+np.cos(pi*(r-r0)/delta)),
                    0.1/(r/r0)**2))


def vortex_ring_3d(x, y, z):
    """3D toroidal vortex ring."""
    rho = np.sqrt((x-0.5)**2 + (y-0.5)**2)
    dist = np.sqrt((rho - 0.3)**2 + (z-0.5)**2)
    return np.exp(-(dist/0.05)**2)


# ============================================================
# ERROR ESTIMATION
# ============================================================

def cell_error_2d(x0, x1, y0, y1, func, num_samples=8):
    """Bilinear interpolation error on a rectangle."""
    x0f, x1f, y0f, y1f = float(x0), float(x1), float(y0), float(y1)
    xc = np.array([x0f, x1f, x0f, x1f])
    yc = np.array([y0f, y0f, y1f, y1f])
    fc = func(xc, yc)
    f00, f10, f01, f11 = fc

    xs = np.linspace(x0f, x1f, num_samples+2)[1:-1]
    ys = np.linspace(y0f, y1f, num_samples+2)[1:-1]
    xx, yy = np.meshgrid(xs, ys)
    xf, yf = xx.ravel(), yy.ravel()
    f_true = func(xf, yf)
    tx = (xf - x0f) / (x1f - x0f + 1e-30)
    ty = (yf - y0f) / (y1f - y0f + 1e-30)
    f_interp = f00*(1-tx)*(1-ty) + f10*tx*(1-ty) + f01*(1-tx)*ty + f11*tx*ty
    return np.max(np.abs(f_true - f_interp)), np.sqrt(np.mean((f_true - f_interp)**2))


def cell_error_3d(x0, x1, y0, y1, z0, z1, func, ns=4):
    """Trilinear interpolation error."""
    cx = np.array([float(x0), float(x1)] * 4)
    cy = np.array([float(y0), float(y0), float(y1), float(y1)] * 2)
    cz = np.array([float(z0)] * 4 + [float(z1)] * 4)
    fc = func(cx, cy, cz)
    xs = np.linspace(float(x0), float(x1), ns+2)[1:-1]
    ys = np.linspace(float(y0), float(y1), ns+2)[1:-1]
    zs = np.linspace(float(z0), float(z1), ns+2)[1:-1]
    xx, yy, zz = np.meshgrid(xs, ys, zs, indexing='ij')
    xf, yf, zf = xx.ravel(), yy.ravel(), zz.ravel()
    f_true = func(xf, yf, zf)
    tx = (xf-float(x0))/(float(x1)-float(x0)+1e-30)
    ty = (yf-float(y0))/(float(y1)-float(y0)+1e-30)
    tz = (zf-float(z0))/(float(z1)-float(z0)+1e-30)
    f_interp = (fc[0]*(1-tx)*(1-ty)*(1-tz) + fc[1]*tx*(1-ty)*(1-tz) +
                fc[2]*(1-tx)*ty*(1-tz) + fc[3]*tx*ty*(1-tz) +
                fc[4]*(1-tx)*(1-ty)*tz + fc[5]*tx*(1-ty)*tz +
                fc[6]*(1-tx)*ty*tz + fc[7]*tx*ty*tz)
    return np.max(np.abs(f_true - f_interp)), np.sqrt(np.mean((f_true - f_interp)**2))


# ============================================================
# 2D FAREY AMR
# ============================================================

def farey_amr_2d(initial_N, func, tolerance, max_level=30):
    """2D Farey AMR on tensor-product grid. Zero cascading by construction."""
    x_nodes = farey_sequence(initial_N)
    y_nodes = farey_sequence(initial_N)

    cells = []
    for i in range(len(x_nodes) - 1):
        for j in range(len(y_nodes) - 1):
            cells.append((x_nodes[i], x_nodes[i+1], y_nodes[j], y_nodes[j+1],
                          initial_N, initial_N))  # (x0, x1, y0, y1, xlev, ylev)

    total_ref = 0
    iterations = 0

    while iterations < 30:
        iterations += 1
        new_cells = []
        refined_any = False

        for x0, x1, y0, y1, xl, yl in cells:
            merr, _ = cell_error_2d(x0, x1, y0, y1, func)
            if merr > tolerance and (xl < max_level or yl < max_level):
                x_new = []
                for lev in range(xl+1, min(xl+5, max_level+1)):
                    x_new = farey_refine_cell(x0, x1, xl, lev)
                    if x_new: break
                y_new = []
                for lev in range(yl+1, min(yl+5, max_level+1)):
                    y_new = farey_refine_cell(y0, y1, yl, lev)
                    if y_new: break

                if not x_new and not y_new:
                    new_cells.append((x0, x1, y0, y1, xl, yl))
                    continue

                x_pts = [x0] + x_new + [x1]
                y_pts = [y0] + y_new + [y1]
                nxl = max(p.denominator for p in x_pts)
                nyl = max(p.denominator for p in y_pts)
                for xi in range(len(x_pts)-1):
                    for yi in range(len(y_pts)-1):
                        new_cells.append((x_pts[xi], x_pts[xi+1],
                                          y_pts[yi], y_pts[yi+1], nxl, nyl))
                total_ref += 1
                refined_any = True
            else:
                new_cells.append((x0, x1, y0, y1, xl, yl))

        cells = new_cells
        if not refined_any:
            break

    # Final errors
    max_err = 0; l2_sum = 0
    for x0, x1, y0, y1, _, _ in cells:
        me, le = cell_error_2d(x0, x1, y0, y1, func)
        max_err = max(max_err, me)
        l2_sum += le**2
    l2 = np.sqrt(l2_sum / max(len(cells), 1))

    return {
        'final_cells': len(cells), 'cascading': 0,
        'total_refinements': total_ref, 'iterations': iterations,
        'max_error': float(max_err), 'l2_error': float(l2),
    }


# ============================================================
# 2D QUADTREE AMR WITH SPATIAL HASH (FAST 2:1 BALANCE)
# ============================================================

def quadtree_amr_2d(num_initial, func, tolerance, max_depth=8):
    """Quadtree AMR with 2:1 balance using spatial hash for fast neighbor lookup."""
    # Each cell: (x0, x1, y0, y1, depth)
    cells = []
    for i in range(num_initial):
        for j in range(num_initial):
            cells.append((i/num_initial, (i+1)/num_initial,
                          j/num_initial, (j+1)/num_initial, 0))

    total_ref = 0
    cascading = 0
    iterations = 0

    while iterations < 15:
        iterations += 1

        # Build spatial hash: map cell center (rounded) -> index
        # For 2:1 balance, we need to find neighbors efficiently
        cell_map = {}
        for idx, (x0, x1, y0, y1, d) in enumerate(cells):
            # Hash by center coordinates at fine resolution
            cx = round((x0 + x1) / 2, 10)
            cy = round((y0 + y1) / 2, 10)
            cell_map[(cx, cy)] = idx

        # Mark cells exceeding tolerance
        to_refine = set()
        for idx, (x0, x1, y0, y1, d) in enumerate(cells):
            if d >= max_depth:
                continue
            merr, _ = cell_error_2d(x0, x1, y0, y1, func)
            if merr > tolerance:
                to_refine.add(idx)

        if not to_refine:
            break

        needed_count = len(to_refine)

        # Enforce 2:1 balance using spatial proximity
        # Build a grid of cells by their depth
        changed = True
        balance_rounds = 0
        while changed and balance_rounds < 20:
            changed = False
            balance_rounds += 1
            additions = set()

            for idx in to_refine:
                x0, x1, y0, y1, d = cells[idx]
                w = x1 - x0
                h = y1 - y0
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2

                # Check potential neighbors in 4 directions
                # A neighbor is a cell that shares a face
                for nidx, (nx0, nx1, ny0, ny1, nd) in enumerate(cells):
                    if nidx in to_refine or nidx in additions or nd >= max_depth:
                        continue
                    nw = nx1 - nx0
                    ncx = (nx0 + nx1) / 2
                    ncy = (ny0 + ny1) / 2

                    # Quick distance check to avoid slow comparisons
                    if abs(cx - ncx) > (w + nw) and abs(cy - ncy) > (h + nw):
                        continue

                    # Face sharing check
                    x_overlap = (x0 < nx1 - 1e-10 and nx0 < x1 - 1e-10) or abs(x0-nx0) < 1e-10
                    y_overlap = (y0 < ny1 - 1e-10 and ny0 < y1 - 1e-10) or abs(y0-ny0) < 1e-10

                    shares_x_face = (abs(x1 - nx0) < 1e-10 or abs(nx1 - x0) < 1e-10) and y_overlap
                    shares_y_face = (abs(y1 - ny0) < 1e-10 or abs(ny1 - y0) < 1e-10) and x_overlap

                    if (shares_x_face or shares_y_face) and d + 1 - nd > 1:
                        additions.add(nidx)
                        changed = True

            if additions:
                cascading += len(additions)
                to_refine |= additions

        total_ref += len(to_refine)

        # Perform quad-splits
        new_cells = []
        for idx, (x0, x1, y0, y1, d) in enumerate(cells):
            if idx in to_refine and d < max_depth:
                mx = (x0 + x1) / 2
                my = (y0 + y1) / 2
                nd = d + 1
                new_cells.extend([
                    (x0, mx, y0, my, nd), (mx, x1, y0, my, nd),
                    (x0, mx, my, y1, nd), (mx, x1, my, y1, nd),
                ])
            else:
                new_cells.append((x0, x1, y0, y1, d))

        cells = new_cells

    # Final errors
    max_err = 0; l2_sum = 0
    for x0, x1, y0, y1, d in cells:
        me, le = cell_error_2d(x0, x1, y0, y1, func)
        max_err = max(max_err, me)
        l2_sum += le**2
    l2 = np.sqrt(l2_sum / max(len(cells), 1))

    return {
        'final_cells': len(cells), 'cascading': cascading,
        'needed': needed_count, 'total_refinements': total_ref,
        'iterations': iterations, 'max_error': float(max_err), 'l2_error': float(l2),
    }


# ============================================================
# OPTIMIZED 2D QUADTREE: DEPTH-ARRAY APPROACH
# ============================================================

def quadtree_amr_2d_fast(num_initial, func, tolerance, max_depth=8):
    """
    Fast quadtree AMR using numpy arrays.
    Uses a flat array representation and vectorized neighbor checks.
    """
    # Start with a list of cells as numpy arrays for speed
    # cell = [x0, x1, y0, y1, depth]
    n = num_initial
    cell_list = []
    for i in range(n):
        for j in range(n):
            cell_list.append([i/n, (i+1)/n, j/n, (j+1)/n, 0])
    cells = np.array(cell_list)

    total_ref = 0
    cascading = 0
    iterations = 0

    while iterations < 12:
        iterations += 1
        nc = len(cells)

        # Compute errors for all cells
        errors = np.zeros(nc)
        for idx in range(nc):
            errors[idx], _ = cell_error_2d(cells[idx, 0], cells[idx, 1],
                                            cells[idx, 2], cells[idx, 3], func)

        to_refine = set(np.where((errors > tolerance) & (cells[:, 4] < max_depth))[0])
        if not to_refine:
            break

        needed_count = len(to_refine)

        # 2:1 balance enforcement
        # For each cell to refine, check all other cells for face adjacency
        # Use bounding box pre-filter for speed
        changed = True
        rounds = 0
        while changed and rounds < 15:
            changed = False
            rounds += 1
            additions = set()

            refine_list = list(to_refine)
            for idx in refine_list:
                x0, x1, y0, y1, d = cells[idx]
                w = x1 - x0

                # Pre-filter: only check cells within 2*w distance
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2
                dx = np.abs((cells[:, 0] + cells[:, 1]) / 2 - cx)
                dy = np.abs((cells[:, 2] + cells[:, 3]) / 2 - cy)
                near = np.where((dx < 2*w) & (dy < 2*w))[0]

                for nidx in near:
                    if nidx in to_refine or nidx in additions:
                        continue
                    nd = cells[nidx, 4]
                    if nd >= max_depth:
                        continue
                    if d + 1 - nd <= 1:
                        continue

                    nx0, nx1, ny0, ny1 = cells[nidx, :4]

                    # Face adjacency
                    x_overlap = (x0 < nx1 - 1e-10 and nx0 < x1 - 1e-10)
                    y_overlap = (y0 < ny1 - 1e-10 and ny0 < y1 - 1e-10)
                    x_face = (abs(x1-nx0) < 1e-10 or abs(nx1-x0) < 1e-10) and y_overlap
                    y_face = (abs(y1-ny0) < 1e-10 or abs(ny1-y0) < 1e-10) and x_overlap

                    if x_face or y_face:
                        additions.add(int(nidx))
                        changed = True

            if additions:
                cascading += len(additions)
                to_refine |= additions

        total_ref += len(to_refine)

        # Quad-split
        new_cells = []
        for idx in range(nc):
            if idx in to_refine:
                x0, x1, y0, y1, d = cells[idx]
                mx, my = (x0+x1)/2, (y0+y1)/2
                nd = d + 1
                new_cells.extend([
                    [x0, mx, y0, my, nd], [mx, x1, y0, my, nd],
                    [x0, mx, my, y1, nd], [mx, x1, my, y1, nd],
                ])
            else:
                new_cells.append(list(cells[idx]))
        cells = np.array(new_cells)

    # Final errors
    nc = len(cells)
    max_err = 0; l2_sum = 0
    for idx in range(nc):
        me, le = cell_error_2d(cells[idx,0], cells[idx,1], cells[idx,2], cells[idx,3], func)
        max_err = max(max_err, me)
        l2_sum += le**2
    l2 = np.sqrt(l2_sum / max(nc, 1))

    return {
        'final_cells': nc, 'cascading': cascading,
        'needed': needed_count if 'needed_count' in dir() else 0,
        'total_refinements': total_ref, 'iterations': iterations,
        'max_error': float(max_err), 'l2_error': float(l2),
    }


# ============================================================
# 3D FAREY AMR
# ============================================================

def farey_amr_3d(initial_N, func, tolerance, max_level=15):
    """3D Farey AMR on tensor-product grid F_N^3."""
    nodes = farey_sequence(initial_N)
    cells = []
    for i in range(len(nodes)-1):
        for j in range(len(nodes)-1):
            for k in range(len(nodes)-1):
                cells.append((nodes[i], nodes[i+1], nodes[j], nodes[j+1],
                              nodes[k], nodes[k+1], initial_N))

    total_ref = 0
    iterations = 0

    while iterations < 15:
        iterations += 1
        new_cells = []
        refined_any = False

        for cell in cells:
            x0, x1, y0, y1, z0, z1, lev = cell
            merr, _ = cell_error_3d(x0, x1, y0, y1, z0, z1, func)
            if merr > tolerance and lev < max_level:
                axes_new = {}
                for axis, (lo, hi) in [('x',(x0,x1)), ('y',(y0,y1)), ('z',(z0,z1))]:
                    for tl in range(lev+1, min(lev+5, max_level+1)):
                        new = farey_refine_cell(lo, hi, lev, tl)
                        if new:
                            axes_new[axis] = new
                            break
                    if axis not in axes_new:
                        axes_new[axis] = []

                if not any(axes_new.values()):
                    new_cells.append(cell)
                    continue

                x_pts = [x0] + axes_new['x'] + [x1]
                y_pts = [y0] + axes_new['y'] + [y1]
                z_pts = [z0] + axes_new['z'] + [z1]
                nl = max(max(p.denominator for p in x_pts),
                         max(p.denominator for p in y_pts),
                         max(p.denominator for p in z_pts))
                for xi in range(len(x_pts)-1):
                    for yi in range(len(y_pts)-1):
                        for zi in range(len(z_pts)-1):
                            new_cells.append((x_pts[xi], x_pts[xi+1],
                                              y_pts[yi], y_pts[yi+1],
                                              z_pts[zi], z_pts[zi+1], nl))
                total_ref += 1
                refined_any = True
            else:
                new_cells.append(cell)

        cells = new_cells
        if not refined_any:
            break

    max_err = 0; l2_sum = 0
    for x0, x1, y0, y1, z0, z1, _ in cells:
        me, le = cell_error_3d(x0, x1, y0, y1, z0, z1, func)
        max_err = max(max_err, me)
        l2_sum += le**2
    l2 = np.sqrt(l2_sum / max(len(cells), 1))

    return {
        'final_cells': len(cells), 'cascading': 0,
        'total_refinements': total_ref, 'iterations': iterations,
        'max_error': float(max_err), 'l2_error': float(l2),
    }


# ============================================================
# 3D OCTREE AMR (FAST)
# ============================================================

def octree_amr_3d_fast(num_initial, func, tolerance, max_depth=4):
    """Octree AMR with 2:1 balance. Uses simple approach, depth-limited."""
    cells = []
    n = num_initial
    for i in range(n):
        for j in range(n):
            for k in range(n):
                cells.append([i/n, (i+1)/n, j/n, (j+1)/n, k/n, (k+1)/n, 0])

    total_ref = 0
    cascading = 0
    iterations = 0

    while iterations < 8:
        iterations += 1
        nc = len(cells)

        # Mark cells
        to_refine = set()
        for idx in range(nc):
            c = cells[idx]
            if c[6] >= max_depth:
                continue
            merr, _ = cell_error_3d(c[0], c[1], c[2], c[3], c[4], c[5], func)
            if merr > tolerance:
                to_refine.add(idx)

        if not to_refine:
            break

        needed_count = len(to_refine)

        # 2:1 balance (simplified: one pass, check all pairs)
        # For 3D, limit balance passes to keep runtime sane
        for _ in range(3):
            additions = set()
            for idx in to_refine:
                c = cells[idx]
                w = c[1] - c[0]
                cx = (c[0]+c[1])/2; cy = (c[2]+c[3])/2; cz = (c[4]+c[5])/2
                d = c[6]

                for nidx in range(nc):
                    if nidx in to_refine or nidx in additions:
                        continue
                    nc2 = cells[nidx]
                    if nc2[6] >= max_depth or d + 1 - nc2[6] <= 1:
                        continue
                    nw = nc2[1] - nc2[0]
                    ncx = (nc2[0]+nc2[1])/2; ncy = (nc2[2]+nc2[3])/2; ncz = (nc2[4]+nc2[5])/2

                    # Quick distance filter
                    if (abs(cx-ncx) > w+nw or abs(cy-ncy) > w+nw or abs(cz-ncz) > w+nw):
                        continue

                    # Check face adjacency (simplified)
                    x_adj = abs(c[1]-nc2[0]) < 1e-10 or abs(nc2[1]-c[0]) < 1e-10
                    y_adj = abs(c[3]-nc2[2]) < 1e-10 or abs(nc2[3]-c[2]) < 1e-10
                    z_adj = abs(c[5]-nc2[4]) < 1e-10 or abs(nc2[5]-c[4]) < 1e-10

                    if x_adj or y_adj or z_adj:
                        additions.add(nidx)

            if not additions:
                break
            cascading += len(additions)
            to_refine |= additions

        total_ref += len(to_refine)

        # Oct-split
        new_cells = []
        for idx in range(nc):
            if idx in to_refine:
                c = cells[idx]
                mx = (c[0]+c[1])/2; my = (c[2]+c[3])/2; mz = (c[4]+c[5])/2
                nd = c[6] + 1
                for xl, xr in [(c[0],mx),(mx,c[1])]:
                    for yl, yr in [(c[2],my),(my,c[3])]:
                        for zl, zr in [(c[4],mz),(mz,c[5])]:
                            new_cells.append([xl,xr,yl,yr,zl,zr,nd])
            else:
                new_cells.append(cells[idx])
        cells = new_cells

    max_err = 0; l2_sum = 0
    for c in cells:
        me, le = cell_error_3d(c[0], c[1], c[2], c[3], c[4], c[5], func)
        max_err = max(max_err, me)
        l2_sum += le**2
    l2 = np.sqrt(l2_sum / max(len(cells), 1))

    return {
        'final_cells': len(cells), 'cascading': cascading,
        'needed': needed_count if 'needed_count' in dir() else 0,
        'total_refinements': total_ref, 'iterations': iterations,
        'max_error': float(max_err), 'l2_error': float(l2),
    }


# ============================================================
# AMReX-LIKE AMR
# ============================================================

def amrex_like_amr_2d(num_initial, func, tolerance, blocking_factor=4, max_depth=8):
    """AMReX-like: quadtree + 2:1 balance + blocking factor."""
    n = num_initial
    cells = np.array([[i/n, (i+1)/n, j/n, (j+1)/n, 0]
                       for i in range(n) for j in range(n)])

    total_ref = 0
    cascading = 0
    iterations = 0

    while iterations < 10:
        iterations += 1
        nc = len(cells)

        errors = np.zeros(nc)
        for idx in range(nc):
            errors[idx], _ = cell_error_2d(cells[idx,0], cells[idx,1],
                                            cells[idx,2], cells[idx,3], func)

        to_refine = set(np.where((errors > tolerance) & (cells[:,4] < max_depth))[0])
        if not to_refine:
            break

        needed_count = len(to_refine)

        # Blocking factor: if any cell in a BF-sized block needs refinement, all do
        min_w = np.min(cells[:, 1] - cells[:, 0])
        bf_size = min_w * blocking_factor

        blocks_hit = set()
        for idx in to_refine:
            bx = int(cells[idx, 0] / bf_size + 0.001)
            by = int(cells[idx, 2] / bf_size + 0.001)
            blocks_hit.add((bx, by))

        for idx in range(nc):
            if idx not in to_refine:
                bx = int(cells[idx, 0] / bf_size + 0.001)
                by = int(cells[idx, 2] / bf_size + 0.001)
                if (bx, by) in blocks_hit and cells[idx, 4] < max_depth:
                    to_refine.add(idx)
                    cascading += 1

        # Simple 2:1 balance (one pass)
        additions = set()
        for idx in list(to_refine):
            x0, x1, y0, y1, d = cells[idx]
            w = x1 - x0
            for nidx in range(nc):
                if nidx in to_refine or nidx in additions:
                    continue
                nd = cells[nidx, 4]
                if nd >= max_depth or d + 1 - nd <= 1:
                    continue
                nx0, nx1, ny0, ny1 = cells[nidx, :4]
                nw = nx1 - nx0
                if abs((x0+x1)/2 - (nx0+nx1)/2) > w + nw:
                    continue
                if abs((y0+y1)/2 - (ny0+ny1)/2) > w + nw:
                    continue
                # Adjacency
                x_face = (abs(x1-nx0)<1e-10 or abs(nx1-x0)<1e-10)
                y_face = (abs(y1-ny0)<1e-10 or abs(ny1-y0)<1e-10)
                if x_face or y_face:
                    additions.add(int(nidx))
        cascading += len(additions)
        to_refine |= additions

        total_ref += len(to_refine)

        new_cells = []
        for idx in range(nc):
            if idx in to_refine:
                x0, x1, y0, y1, d = cells[idx]
                mx, my = (x0+x1)/2, (y0+y1)/2
                nd = d + 1
                new_cells.extend([
                    [x0,mx,y0,my,nd], [mx,x1,y0,my,nd],
                    [x0,mx,my,y1,nd], [mx,x1,my,y1,nd],
                ])
            else:
                new_cells.append(list(cells[idx]))
        cells = np.array(new_cells)

    nc = len(cells)
    max_err = 0; l2_sum = 0
    for idx in range(nc):
        me, le = cell_error_2d(cells[idx,0], cells[idx,1], cells[idx,2], cells[idx,3], func)
        max_err = max(max_err, me)
        l2_sum += le**2
    l2 = np.sqrt(l2_sum / max(nc, 1))

    return {
        'final_cells': nc, 'cascading': cascading,
        'total_refinements': total_ref, 'iterations': iterations,
        'max_error': float(max_err), 'l2_error': float(l2),
    }


# ============================================================
# EXPERIMENT 1: Realistic 2D Flow Fields
# ============================================================

def run_experiment_1():
    print("\n" + "="*70)
    print("EXPERIMENT 1: Realistic 2D Flow Fields")
    print("="*70)

    functions = {
        'Lamb-Oseen': lamb_oseen_vortex,
        'Sod Shock': sod_shock_tube_2d,
        'Kelvin-Helmholtz': kelvin_helmholtz,
        'Multi-Scale': multi_scale_features,
    }

    tolerances = [0.1, 0.05, 0.02, 0.01, 0.005]
    results = {}

    for fname, func in functions.items():
        print(f"\n--- {fname} ---")
        results[fname] = {'farey': [], 'quadtree': []}

        for tol in tolerances:
            print(f"  tol={tol}...", end=" ", flush=True)

            t0 = time.time()
            f_stats = farey_amr_2d(4, func, tol, max_level=25)
            f_stats['time'] = time.time() - t0
            f_stats['tolerance'] = tol
            results[fname]['farey'].append(f_stats)

            t0 = time.time()
            q_stats = quadtree_amr_2d_fast(6, func, tol, max_depth=7)
            q_stats['time'] = time.time() - t0
            q_stats['tolerance'] = tol
            results[fname]['quadtree'].append(q_stats)

            ratio = f_stats['final_cells'] / max(q_stats['final_cells'], 1)
            print(f"F={f_stats['final_cells']}, Q={q_stats['final_cells']}, "
                  f"ratio={ratio:.2f}, casc={q_stats['cascading']}")

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Experiment 1: Farey AMR vs Quadtree on Realistic 2D Functions',
                 fontsize=14, fontweight='bold')

    for idx, (fname, data) in enumerate(results.items()):
        ax = axes[idx // 2][idx % 2]
        f_cells = [s['final_cells'] for s in data['farey']]
        q_cells = [s['final_cells'] for s in data['quadtree']]
        q_casc = [s['cascading'] for s in data['quadtree']]

        x = range(len(tolerances))
        w = 0.35
        bars1 = ax.bar([i-w/2 for i in x], f_cells, w, label='Farey AMR', color='#2196F3', alpha=0.8)
        q_needed = [max(q-c, 0) for q, c in zip(q_cells, q_casc)]
        ax.bar([i+w/2 for i in x], q_needed, w, label='Quadtree (needed)', color='#FF5722', alpha=0.8)
        ax.bar([i+w/2 for i in x], q_casc, w, bottom=q_needed,
               color='#FFB74D', alpha=0.8, label='Cascading overhead')

        ax.set_title(fname)
        ax.set_xticks(x)
        ax.set_xticklabels([str(t) for t in tolerances], fontsize=8)
        ax.set_xlabel('Tolerance')
        ax.set_ylabel('Cell count')
        ax.legend(fontsize=7)
        ax.set_yscale('log')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'amr_validation_exp1.png'), dpi=150)
    plt.close()
    print("  -> Saved amr_validation_exp1.png")
    return results


# ============================================================
# EXPERIMENT 2: 3D Extension
# ============================================================

def run_experiment_2():
    print("\n" + "="*70)
    print("EXPERIMENT 2: 3D Extension")
    print("="*70)

    functions = {
        'Spherical Blast': spherical_blast_3d,
        'Vortex Ring': vortex_ring_3d,
    }
    tolerances = [0.2, 0.1, 0.05]
    results = {}

    for fname, func in functions.items():
        print(f"\n--- {fname} ---")
        results[fname] = {'farey': [], 'octree': []}

        for tol in tolerances:
            print(f"  tol={tol}...", end=" ", flush=True)

            t0 = time.time()
            f_stats = farey_amr_3d(3, func, tol, max_level=12)
            f_stats['time'] = time.time() - t0
            f_stats['tolerance'] = tol
            results[fname]['farey'].append(f_stats)

            t0 = time.time()
            o_stats = octree_amr_3d_fast(3, func, tol, max_depth=3)
            o_stats['time'] = time.time() - t0
            o_stats['tolerance'] = tol
            results[fname]['octree'].append(o_stats)

            ratio = f_stats['final_cells'] / max(o_stats['final_cells'], 1)
            print(f"F={f_stats['final_cells']}, O={o_stats['final_cells']}, "
                  f"ratio={ratio:.2f}, casc={o_stats['cascading']}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Experiment 2: Farey AMR vs Octree in 3D', fontsize=14, fontweight='bold')

    for idx, (fname, data) in enumerate(results.items()):
        ax = axes[idx]
        f_cells = [s['final_cells'] for s in data['farey']]
        o_cells = [s['final_cells'] for s in data['octree']]
        o_casc = [s['cascading'] for s in data['octree']]

        x = range(len(tolerances))
        w = 0.35
        ax.bar([i-w/2 for i in x], f_cells, w, label='Farey AMR', color='#2196F3', alpha=0.8)
        o_needed = [max(o-c, 0) for o, c in zip(o_cells, o_casc)]
        ax.bar([i+w/2 for i in x], o_needed, w, label='Octree (needed)', color='#FF5722', alpha=0.8)
        ax.bar([i+w/2 for i in x], o_casc, w, bottom=o_needed,
               color='#FFB74D', alpha=0.8, label='Cascading overhead')

        ax.set_title(fname)
        ax.set_xticks(x)
        ax.set_xticklabels([str(t) for t in tolerances])
        ax.set_xlabel('Tolerance')
        ax.set_ylabel('Cell count')
        ax.legend(fontsize=8)
        ax.set_yscale('log')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'amr_validation_exp2.png'), dpi=150)
    plt.close()
    print("  -> Saved amr_validation_exp2.png")
    return results


# ============================================================
# EXPERIMENT 3: p4est/AMReX-like Refinement Patterns
# ============================================================

def run_experiment_3():
    print("\n" + "="*70)
    print("EXPERIMENT 3: p4est/AMReX-like Refinement Patterns")
    print("="*70)

    func = multi_scale_features
    tolerances = [0.1, 0.05, 0.02, 0.01, 0.005]
    results = {'farey': [], 'quadtree': [], 'amrex': []}

    for tol in tolerances:
        print(f"  tol={tol}...", end=" ", flush=True)

        f_stats = farey_amr_2d(4, func, tol, max_level=25)
        f_stats['tolerance'] = tol
        results['farey'].append(f_stats)

        q_stats = quadtree_amr_2d_fast(6, func, tol, max_depth=7)
        q_stats['tolerance'] = tol
        results['quadtree'].append(q_stats)

        a_stats = amrex_like_amr_2d(6, func, tol, blocking_factor=4, max_depth=7)
        a_stats['tolerance'] = tol
        results['amrex'].append(a_stats)

        print(f"F={f_stats['final_cells']}, Q={q_stats['final_cells']}, "
              f"A={a_stats['final_cells']}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Experiment 3: Farey vs p4est-like vs AMReX-like', fontsize=14, fontweight='bold')

    fc = [s['final_cells'] for s in results['farey']]
    qc = [s['final_cells'] for s in results['quadtree']]
    ac = [s['final_cells'] for s in results['amrex']]

    ax1.plot(tolerances, fc, 'o-', label='Farey AMR', color='#2196F3', lw=2)
    ax1.plot(tolerances, qc, 's-', label='p4est-like (quad+balance)', color='#FF5722', lw=2)
    ax1.plot(tolerances, ac, '^-', label='AMReX-like (BF=4)', color='#4CAF50', lw=2)
    ax1.set_xlabel('Tolerance'); ax1.set_ylabel('Cell count')
    ax1.set_title('Cell Count vs Tolerance')
    ax1.legend(); ax1.set_xscale('log'); ax1.set_yscale('log'); ax1.invert_xaxis()

    qo = [s['cascading']/max(s['final_cells'],1)*100 for s in results['quadtree']]
    ao = [s['cascading']/max(s['final_cells'],1)*100 for s in results['amrex']]
    ax2.plot(tolerances, [0]*len(tolerances), 'o-', label='Farey (0%)', color='#2196F3', lw=2)
    ax2.plot(tolerances, qo, 's-', label='p4est-like', color='#FF5722', lw=2)
    ax2.plot(tolerances, ao, '^-', label='AMReX-like', color='#4CAF50', lw=2)
    ax2.set_xlabel('Tolerance'); ax2.set_ylabel('Cascading overhead (%)')
    ax2.set_title('Cascading Overhead %')
    ax2.legend(); ax2.set_xscale('log'); ax2.invert_xaxis()

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'amr_validation_exp3.png'), dpi=150)
    plt.close()
    print("  -> Saved amr_validation_exp3.png")
    return results


# ============================================================
# EXPERIMENT 4: Compute Time (Heat Equation)
# ============================================================

def run_experiment_4():
    print("\n" + "="*70)
    print("EXPERIMENT 4: Compute Time (Heat Equation)")
    print("="*70)

    alpha = 0.01
    t_final = 0.05

    def exact_solution(x, y, t):
        sigma2 = 0.01 + 2*alpha*t
        return (0.01/sigma2) * np.exp(-((x-0.5)**2 + (y-0.5)**2) / (2*sigma2))

    def initial_condition(x, y):
        return exact_solution(x, y, 0)

    resolutions = [8, 16, 32, 64]
    results = {'uniform': [], 'farey': []}

    for N in resolutions:
        print(f"\n  N={N}...", flush=True)

        # UNIFORM
        t0 = time.time()
        h = 1.0 / N
        dt = 0.2 * h**2 / alpha
        n_steps = max(int(t_final / dt), 1)
        dt = t_final / n_steps

        xs = np.linspace(0, 1, N+1)
        xx, yy = np.meshgrid(xs, xs, indexing='ij')
        u = initial_condition(xx, yy)

        # Vectorized FD
        for _ in range(n_steps):
            u_new = u.copy()
            u_new[1:-1, 1:-1] = u[1:-1, 1:-1] + alpha * dt * (
                (u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1]) / h**2 +
                (u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2]) / h**2
            )
            u = u_new

        err_u = np.sqrt(np.mean((u - exact_solution(xx, yy, t_final))**2))
        time_u = time.time() - t0
        results['uniform'].append({'N': N, 'cells': N*N, 'time': time_u,
                                   'l2_error': float(err_u), 'n_steps': n_steps})
        print(f"    Uniform: {N*N} cells, {time_u:.4f}s, L2={err_u:.2e}")

        # FAREY (match approximate cell count)
        N_farey = max(3, int(np.sqrt(N * 3.3)))
        t0 = time.time()
        fnodes = farey_sequence(N_farey)
        nf = len(fnodes)
        fx = np.array([float(f) for f in fnodes])

        u_f = np.zeros((nf, nf))
        for i in range(nf):
            for j in range(nf):
                u_f[i, j] = initial_condition(fx[i], fx[j])

        dx = np.diff(fx)
        h_min = np.min(dx)
        dt_f = 0.2 * h_min**2 / alpha
        n_steps_f = max(int(t_final / dt_f), 1)
        dt_f = t_final / n_steps_f

        for _ in range(n_steps_f):
            u_new = u_f.copy()
            for i in range(1, nf-1):
                dxl = fx[i] - fx[i-1]
                dxr = fx[i+1] - fx[i]
                for j in range(1, nf-1):
                    dyl = fx[j] - fx[j-1]
                    dyr = fx[j+1] - fx[j]
                    uxx = 2.0/(dxl+dxr) * (u_f[i+1,j]/dxr - u_f[i,j]*(1/dxr+1/dxl) + u_f[i-1,j]/dxl)
                    uyy = 2.0/(dyl+dyr) * (u_f[i,j+1]/dyr - u_f[i,j]*(1/dyr+1/dyl) + u_f[i,j-1]/dyl)
                    u_new[i,j] = u_f[i,j] + alpha*dt_f*(uxx + uyy)
            u_f = u_new

        # Error at Farey nodes
        u_exact_f = np.zeros((nf, nf))
        for i in range(nf):
            for j in range(nf):
                u_exact_f[i,j] = exact_solution(fx[i], fx[j], t_final)
        err_f = np.sqrt(np.mean((u_f - u_exact_f)**2))
        time_f = time.time() - t0
        n_cells_f = (nf-1)**2

        results['farey'].append({'N': N, 'N_farey': N_farey, 'cells': n_cells_f,
                                 'time': time_f, 'l2_error': float(err_f),
                                 'n_steps': n_steps_f})
        print(f"    Farey:   {n_cells_f} cells (F_{N_farey}), {time_f:.4f}s, "
              f"L2={err_f:.2e}, steps={n_steps_f}")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Experiment 4: Heat Equation — Uniform vs Farey Grid', fontsize=14, fontweight='bold')

    uc = [r['cells'] for r in results['uniform']]
    ut = [r['time'] for r in results['uniform']]
    ue = [r['l2_error'] for r in results['uniform']]
    fc = [r['cells'] for r in results['farey']]
    ft = [r['time'] for r in results['farey']]
    fe = [r['l2_error'] for r in results['farey']]

    ax1.loglog(uc, ut, 'o-', label='Uniform', color='#FF5722', lw=2)
    ax1.loglog(fc, ft, 's-', label='Farey', color='#2196F3', lw=2)
    ax1.set_xlabel('Cell count'); ax1.set_ylabel('Time (s)'); ax1.set_title('Time vs Cells'); ax1.legend()

    ax2.loglog(uc, ue, 'o-', label='Uniform', color='#FF5722', lw=2)
    ax2.loglog(fc, fe, 's-', label='Farey', color='#2196F3', lw=2)
    ax2.set_xlabel('Cell count'); ax2.set_ylabel('L2 error'); ax2.set_title('Error vs Cells'); ax2.legend()

    ax3.loglog(ut, ue, 'o-', label='Uniform', color='#FF5722', lw=2)
    ax3.loglog(ft, fe, 's-', label='Farey', color='#2196F3', lw=2)
    ax3.set_xlabel('Time (s)'); ax3.set_ylabel('L2 error')
    ax3.set_title('Efficiency (lower-left = better)'); ax3.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'amr_validation_exp4.png'), dpi=150)
    plt.close()
    print("  -> Saved amr_validation_exp4.png")
    return results


# ============================================================
# HONESTY CHECKS
# ============================================================

def run_honesty_checks(exp1, exp2):
    print("\n" + "="*70)
    print("CRITICAL HONESTY CHECKS")
    print("="*70)

    report = []

    # Check 1: Cell count ratio (Farey / Quadtree) — is Farey REALLY better?
    print("\n[CHECK 1] Farey cell count vs Quadtree total (ratio < 1 = Farey wins)")
    report.append("\n## Check 1: Farey vs Quadtree Total Cell Count")
    report.append("| Function | Tolerance | Farey | Quadtree | Ratio (F/Q) | Quad Cascading |")
    report.append("|----------|-----------|-------|----------|-------------|----------------|")

    all_ratios = []
    for fname, data in exp1.items():
        for f, q in zip(data['farey'], data['quadtree']):
            ratio = f['final_cells'] / max(q['final_cells'], 1)
            all_ratios.append(ratio)
            line = f"| {fname} | {f['tolerance']} | {f['final_cells']} | {q['final_cells']} | {ratio:.3f} | {q['cascading']} |"
            report.append(line)
            print(f"  {fname} tol={f['tolerance']}: ratio={ratio:.3f}")

    mean_ratio = np.mean(all_ratios)
    wins = sum(1 for r in all_ratios if r < 1.0)
    total = len(all_ratios)
    print(f"\n  MEAN ratio: {mean_ratio:.3f}")
    print(f"  Farey wins: {wins}/{total} comparisons")
    report.append(f"\n**Mean ratio (Farey/Quadtree): {mean_ratio:.3f}**")
    report.append(f"**Farey wins {wins}/{total} comparisons**")

    # Check 2: Farey vs Quadtree EXCLUDING cascading
    print("\n[CHECK 2] Farey vs Quadtree (needed cells only, no cascading)")
    report.append("\n## Check 2: Farey vs Quadtree Needed Cells Only")
    report.append("| Function | Tol | Farey | Quad Needed | Ratio |")
    report.append("|----------|-----|-------|-------------|-------|")
    needed_ratios = []
    for fname, data in exp1.items():
        for f, q in zip(data['farey'], data['quadtree']):
            needed = max(q['final_cells'] - q['cascading'], 1)
            ratio = f['final_cells'] / needed
            needed_ratios.append(ratio)
            report.append(f"| {fname} | {f['tolerance']} | {f['final_cells']} | {needed} | {ratio:.3f} |")
            print(f"  {fname} tol={f['tolerance']}: Farey/needed = {ratio:.3f}")

    print(f"\n  MEAN ratio vs needed: {np.mean(needed_ratios):.3f}")
    report.append(f"\n**Mean ratio vs needed cells: {np.mean(needed_ratios):.3f}**")

    # Check 3: Error comparison at same tolerance
    print("\n[CHECK 3] Max error achieved (both methods at same tolerance)")
    report.append("\n## Check 3: Error Comparison at Same Tolerance")
    report.append("| Function | Tol | Farey MaxErr | Quad MaxErr | Farey L2 | Quad L2 |")
    report.append("|----------|-----|-------------|-------------|----------|---------|")
    for fname, data in exp1.items():
        for f, q in zip(data['farey'], data['quadtree']):
            report.append(f"| {fname} | {f['tolerance']} | {f['max_error']:.4f} | {q['max_error']:.4f} | {f['l2_error']:.2e} | {q['l2_error']:.2e} |")

    # Check 4: 3D cascading
    if exp2:
        print("\n[CHECK 4] 3D cascading overhead")
        report.append("\n## Check 4: 3D Cascading Overhead")
        report.append("| Function | Tol | Farey 3D | Octree 3D | Octree Cascading | Overhead % |")
        report.append("|----------|-----|----------|-----------|-----------------|------------|")
        for fname, data in exp2.items():
            for f, o in zip(data['farey'], data['octree']):
                overhead = o['cascading'] / max(o['final_cells'], 1) * 100
                report.append(f"| {fname} | {f['tolerance']} | {f['final_cells']} | {o['final_cells']} | {o['cascading']} | {overhead:.1f}% |")
                print(f"  {fname} tol={f['tolerance']}: octree cascade={o['cascading']}/{o['final_cells']} ({overhead:.1f}%)")

    # Check 5: Is the advantage function-dependent?
    print("\n[CHECK 5] Function-dependence of advantage")
    report.append("\n## Check 5: Function Dependence")
    for fname, data in exp1.items():
        ratios = [f['final_cells']/max(q['final_cells'],1) for f, q in zip(data['farey'], data['quadtree'])]
        print(f"  {fname}: mean ratio = {np.mean(ratios):.3f} (range {np.min(ratios):.3f}-{np.max(ratios):.3f})")
        report.append(f"- **{fname}**: mean ratio = {np.mean(ratios):.3f} (range {np.min(ratios):.3f}-{np.max(ratios):.3f})")

    return report, {
        'mean_ratio': float(mean_ratio),
        'mean_needed_ratio': float(np.mean(needed_ratios)),
        'wins': wins, 'total': total,
    }


# ============================================================
# MAIN
# ============================================================

def main():
    print("="*70)
    print("AMR REAL-WORLD VALIDATION EXPERIMENTS")
    print("Testing Farey AMR claims on realistic data")
    print("="*70)

    t_start = time.time()

    exp1 = run_experiment_1()
    exp2 = run_experiment_2()
    exp3 = run_experiment_3()
    exp4 = run_experiment_4()
    honesty_report, honesty_stats = run_honesty_checks(exp1, exp2)

    total_time = time.time() - t_start
    print(f"\nTotal runtime: {total_time:.1f}s")

    # Save JSON
    def to_json(obj):
        if isinstance(obj, (np.integer,)): return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return str(obj)

    all_data = {'exp1': exp1, 'exp2': exp2, 'exp3': exp3, 'exp4': exp4,
                'honesty': honesty_stats, 'total_time': total_time}
    with open(os.path.join(OUTPUT_DIR, 'amr_validation_results.json'), 'w') as f:
        json.dump(all_data, f, indent=2, default=to_json)

    # Print summary for report generation
    print("\n" + "="*70)
    print("SUMMARY FOR REPORT")
    print("="*70)
    print(f"Mean Farey/Quadtree ratio (2D): {honesty_stats['mean_ratio']:.3f}")
    print(f"Mean Farey/Needed ratio (2D): {honesty_stats['mean_needed_ratio']:.3f}")
    print(f"Farey wins {honesty_stats['wins']}/{honesty_stats['total']} comparisons")

    # Return everything for report writing
    return {
        'exp1': exp1, 'exp2': exp2, 'exp3': exp3, 'exp4': exp4,
        'honesty_report': honesty_report, 'honesty_stats': honesty_stats,
    }


if __name__ == '__main__':
    results = main()
