#!/usr/bin/env python3
"""
PSL₂(ℤ) / Ford Circle interpretation of the Injection Principle.

Generates four publication-quality figures:
  1. Ford Circles for F_6 → F_7
  2. Ideal Triangle Splitting via mediant insertion
  3. The Modular Surface / Fundamental Domain of PSL₂(ℤ)
  4. Euler Characteristic Preservation under Farey insertion
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as MplCircle, Arc, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as pe
from math import gcd
from fractions import Fraction

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
FIG_DIR = os.path.join(ROOT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

DPI = 200

# Color palette
BLUE = '#457B9D'
DARK_BLUE = '#1D3557'
RED = '#E63946'
GOLD = '#F4A261'
TEAL = '#2A9D8F'
CREAM = '#F1FAEE'
DARK = '#264653'
LIGHT_GRAY = '#E8E8E8'
MEDIUM_GRAY = '#B0B0B0'

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except Exception:
    try:
        plt.style.use('seaborn-whitegrid')
    except Exception:
        pass

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'figure.facecolor': 'white',
})


# ---------------------------------------------------------------------------
# Farey sequence utilities
# ---------------------------------------------------------------------------
def farey_sequence(n):
    """Generate the Farey sequence F_n as list of Fraction objects."""
    fracs = set()
    for b in range(1, n + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def ford_circle_params(frac):
    """Return (cx, cy, r) for the Ford circle at fraction a/b."""
    a, b = frac.numerator, frac.denominator
    r = 1.0 / (2.0 * b * b)
    cx = float(frac)
    cy = r
    return cx, cy, r


def are_tangent(f1, f2):
    """Check if Ford circles at f1 and f2 are tangent (Farey neighbors)."""
    a, b = f1.numerator, f1.denominator
    c, d = f2.numerator, f2.denominator
    return abs(a * d - b * c) == 1


def hyperbolic_geodesic(x1, x2, npts=200):
    """
    Return arrays (xs, ys) tracing the hyperbolic geodesic (semicircle)
    connecting points x1 and x2 on the real line in the upper half-plane.
    """
    center = (x1 + x2) / 2.0
    radius = abs(x2 - x1) / 2.0
    theta = np.linspace(0, np.pi, npts)
    xs = center + radius * np.cos(theta)
    ys = radius * np.sin(theta)
    return xs, ys


# =========================================================================
# FIGURE 1: Ford Circles for F_6 → F_7
# =========================================================================
def figure1_ford_circles():
    print("Generating Figure 1: Ford Circles F_6 → F_7 ...")
    f6 = farey_sequence(6)
    f7 = farey_sequence(7)
    new_fracs = [f for f in f7 if f not in f6]

    fig, ax = plt.subplots(figsize=(14, 3.8))
    ax.set_facecolor('#FAFAFA')

    # Draw tangency lines between Farey neighbors in F_7
    for i in range(len(f7) - 1):
        if are_tangent(f7[i], f7[i + 1]):
            cx1, cy1, r1 = ford_circle_params(f7[i])
            cx2, cy2, r2 = ford_circle_params(f7[i + 1])
            ax.plot([cx1, cx2], [cy1, cy2], color=MEDIUM_GRAY, lw=0.5,
                    alpha=0.5, zorder=1)

    # Draw existing circles (F_6) in blue
    for frac in f6:
        cx, cy, r = ford_circle_params(frac)
        circle = MplCircle((cx, cy), r, fill=True, facecolor=BLUE,
                           edgecolor=DARK_BLUE, linewidth=0.8, alpha=0.7,
                           zorder=3, clip_on=True)
        ax.add_patch(circle)
        # Label fractions with denominator <= 6 (large enough to read)
        if frac.denominator <= 6:
            label = f"{frac.numerator}/{frac.denominator}" if frac.denominator > 1 else str(frac.numerator)
            y_off = max(0.006, r + 0.004)
            ax.text(cx, cy + y_off, label, ha='center', va='bottom',
                    fontsize=8, color=DARK_BLUE, fontweight='bold')

    # Draw new circles (denom 7) in red
    for frac in new_fracs:
        cx, cy, r = ford_circle_params(frac)
        circle = MplCircle((cx, cy), r, fill=True, facecolor=RED,
                           edgecolor='#A4161A', linewidth=1.0, alpha=0.85,
                           zorder=4, clip_on=True)
        ax.add_patch(circle)
        label = f"{frac.numerator}/{frac.denominator}"
        ax.text(cx, cy + r + 0.004, label, ha='center', va='bottom',
                fontsize=8, color=RED, fontweight='bold')

    # Draw the real line
    ax.axhline(y=0, color=DARK, lw=1.5, zorder=2)

    # Legend (positioned via bbox_to_anchor outside the plot area)
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=BLUE,
               markeredgecolor=DARK_BLUE, markersize=12, label='$\\mathcal{F}_6$ (existing)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=RED,
               markeredgecolor='#A4161A', markersize=12, label='Denominator 7 (new)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10,
              framealpha=0.9, bbox_to_anchor=(0.0, 1.0))

    ax.set_title("The Injection Principle as Ford Circle Packing",
                 fontsize=15, fontweight='bold', pad=12)
    ax.set_xlabel("$a/b$", fontsize=12)
    ax.set_ylabel("Height in $\\mathbb{H}$", fontsize=12)

    # Annotation explaining the injection
    ax.annotate(
        "Each new $a/7$ fits\nuniquely between a\ntangent pair from $\\mathcal{F}_6$",
        xy=(0.42, 0.012), xytext=(0.78, 0.10),
        fontsize=9, color=DARK,
        arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
        bbox=dict(boxstyle='round,pad=0.3', facecolor=CREAM, edgecolor=GOLD,
                  alpha=0.9)
    )

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.005, 0.16)
    ax.set_aspect('equal')

    ax.tick_params(axis='y', labelsize=8)
    ax.tick_params(axis='x', labelsize=8)

    # Position axes manually; avoid bbox_inches='tight' which would expand
    # the bounding box to include the full extent of clipped circles.
    fig.subplots_adjust(left=0.05, right=0.98, bottom=0.15, top=0.82)
    path = os.path.join(FIG_DIR, "fig_ford_circle_injection.png")
    fig.savefig(path, dpi=DPI, facecolor='white')
    plt.close(fig)
    print(f"  Saved: {path}")


# =========================================================================
# FIGURE 2: Ideal Triangle Splitting
# =========================================================================
def figure2_ideal_triangle():
    print("Generating Figure 2: Ideal Triangle Splitting ...")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for idx, ax in enumerate(axes):
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.02, 0.65)
        ax.set_aspect('equal')
        ax.set_facecolor('#FAFAFA')
        ax.axhline(y=0, color=DARK, lw=1.5, zorder=1)

    # The triangle: 0/1 — 1/2 — 1/1 (a classic Farey triangle)
    # Mediant of 0/1 and 1/2 is 1/3
    # Or use: 1/3, 1/2, 2/5 with mediant 3/7
    # Let's use the cleaner example: 0/1, 1/2, 1/1
    # Mediant of 0/1 and 1/2 = 1/3; of 1/2 and 1/1 = 2/3
    # Use: vertices at 1/3, 1/2, 2/5. Mediant of 1/3 and 2/5 = 3/8.
    # Actually let's use the simplest: 0/1, 1/1 with mediant 1/2 splitting
    # into 0/1—1/2—1/1.

    # Panel A: Before insertion — single ideal triangle 0/1, 1/2, 1/1
    # with the triangle having geodesics 0↔1/2, 1/2↔1, and 0↔1
    ax = axes[0]
    ax.set_title("Before: One Ideal Triangle", fontsize=13, fontweight='bold')

    # Draw the three geodesic edges of the triangle
    pairs = [(0.0, 0.5), (0.5, 1.0), (0.0, 1.0)]
    colors_edges = [BLUE, BLUE, BLUE]
    for (x1, x2), col in zip(pairs, colors_edges):
        xs, ys = hyperbolic_geodesic(x1, x2)
        ax.plot(xs, ys, color=col, lw=2.5, zorder=3, alpha=0.85)

    # Shade the triangle interior
    # Approximate by sampling the region
    theta1 = np.linspace(0, np.pi, 200)
    # outer arc: 0 to 1
    xo = 0.5 + 0.5 * np.cos(theta1)
    yo = 0.5 * np.sin(theta1)
    # left inner arc: 0 to 1/2
    xl = 0.25 + 0.25 * np.cos(theta1)
    yl = 0.25 * np.sin(theta1)
    # right inner arc: 1/2 to 1
    xr = 0.75 + 0.25 * np.cos(theta1)
    yr = 0.25 * np.sin(theta1)

    # Fill the triangle: between outer arc and inner arcs
    # Upper boundary: outer arc from 0 to 1
    # Lower boundary: left arc (0 to 0.5) then right arc (0.5 to 1)
    lower_x = np.concatenate([xl, xr[::-1]])
    lower_y = np.concatenate([yl, yr[::-1]])
    ax.fill_between(xo, yo, np.interp(xo, lower_x, lower_y),
                    alpha=0.15, color=GOLD, zorder=2)

    # Label vertices
    for val, label in [(0, "0/1"), (0.5, "1/2"), (1, "1/1")]:
        ax.plot(val, 0, 'o', color=DARK, markersize=6, zorder=5)
        ax.text(val, -0.015, label, ha='center', va='top', fontsize=11,
                fontweight='bold', color=DARK)

    # Area annotation
    ax.text(0.5, 0.30, "Area = $\\pi$", ha='center', va='center',
            fontsize=14, color=DARK, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=CREAM,
                      edgecolor=GOLD, alpha=0.9))

    # Panel B: After insertion — mediant 1/3 splits triangle
    ax = axes[1]
    ax.set_title("After: Mediant $1/3$ Splits the Triangle", fontsize=13,
                 fontweight='bold')

    # New edges: 0↔1/3, 1/3↔1/2, 0↔1/2, 1/2↔1, 0↔1
    # The mediant of 0/1 and 1/2 is 1/3
    # This splits triangle (0/1, 1/2, 1/1) into (0/1, 1/3, 1/2) ∪ — wait,
    # the mediant of 0/1 and 1/2 is 1/3, which creates a new edge 1/3↔∞
    # In the finite picture: splits 0/1—1/2 edge, creating two triangles:
    # (0/1, 1/3, 1/2) sharing the outer arc with (0/1, 1/2, 1/1)

    # Draw original outer arc
    xs, ys = hyperbolic_geodesic(0, 1)
    ax.plot(xs, ys, color=BLUE, lw=2.5, zorder=3, alpha=0.85)
    xs, ys = hyperbolic_geodesic(0.5, 1)
    ax.plot(xs, ys, color=BLUE, lw=2.5, zorder=3, alpha=0.85)

    # Original edge now split: 0↔1/2 becomes 0↔1/3 and 1/3↔1/2
    xs, ys = hyperbolic_geodesic(0, 1.0 / 3)
    ax.plot(xs, ys, color=BLUE, lw=2.5, zorder=3, alpha=0.85)
    xs, ys = hyperbolic_geodesic(1.0 / 3, 0.5)
    ax.plot(xs, ys, color=BLUE, lw=2.5, zorder=3, alpha=0.85)

    # New edge: 1/3 ↔ 1 (the splitting geodesic)
    xs, ys = hyperbolic_geodesic(1.0 / 3, 1.0)
    ax.plot(xs, ys, color=RED, lw=3, zorder=4, alpha=0.9,
            linestyle='--')

    # Shade left sub-triangle (0/1, 1/3, 1/2) — but really we need
    # the triangle (0/1, 1/3, 1/1) left and (1/3, 1/2, 1/1) right
    # Actually the new geodesic from 1/3 to ∞ (vertical line) isn't finite.
    # The proper picture: inserting 1/3 between 0/1 and 1/2 as Farey neighbors,
    # new edge 1/3 connects to all vertices of the old triangle.
    # The old triangle (0, 1/2, 1) splits into (0, 1/3, 1) ∪ (1/3, 1/2, 1)
    # via new edge 1/3↔1.

    # Shade left triangle: between arc(0,1) above, arc(0,1/3) and arc(1/3,1) below
    theta_fine = np.linspace(0, np.pi, 500)

    # Left sub-triangle (0, 1/3, 1): outer arc 0↔1, inner arcs 0↔1/3, 1/3↔1
    ax.fill_between(
        *hyperbolic_geodesic(0, 1.0 / 3, 300),
        0, alpha=0.12, color=TEAL, zorder=2
    )

    # Actually let's do a simpler shading approach: just shade each sub-triangle
    # with distinct colors
    # Left: vertices 0, 1/3, 1
    # Right: vertices 1/3, 1/2, 1

    # For the left triangle, use fill_between on the outer arc minus inner arcs
    xo2, yo2 = hyperbolic_geodesic(0, 1, 500)
    x_left, y_left = hyperbolic_geodesic(0, 1.0 / 3, 500)
    x_split, y_split = hyperbolic_geodesic(1.0 / 3, 1.0, 500)

    # Left triangle region: above arcs 0↔1/3 and 1/3↔1, below arc 0↔1
    lower_left_x = np.concatenate([x_left, x_split[::-1]])
    lower_left_y = np.concatenate([y_left, y_split[::-1]])
    # Sort by x for interpolation
    sort_idx = np.argsort(lower_left_x)
    lower_left_x = lower_left_x[sort_idx]
    lower_left_y = lower_left_y[sort_idx]

    # Interpolate lower boundary at the outer arc x-values
    mask = (xo2 >= 0) & (xo2 <= 1)
    lower_interp = np.interp(xo2[mask], lower_left_x, lower_left_y)
    ax.fill_between(xo2[mask], yo2[mask], lower_interp,
                    alpha=0.12, color=TEAL, zorder=2)

    # Now shade the right sub-triangle differently
    # Right sub-triangle: 1/3, 1/2, 1
    # Outer: arc 1/3↔1 (the splitting geodesic)
    # Inner: arcs 1/3↔1/2 and 1/2↔1
    x_r1, y_r1 = hyperbolic_geodesic(1.0 / 3, 0.5, 300)
    x_r2, y_r2 = hyperbolic_geodesic(0.5, 1.0, 300)
    lower_right_x = np.concatenate([x_r1, x_r2[::-1]])
    lower_right_y = np.concatenate([y_r1, y_r2[::-1]])
    sort_idx = np.argsort(lower_right_x)
    lower_right_x = lower_right_x[sort_idx]
    lower_right_y = lower_right_y[sort_idx]

    mask2 = (x_split >= 1.0 / 3) & (x_split <= 1.0)
    lower_interp2 = np.interp(x_split[mask2], lower_right_x, lower_right_y)
    ax.fill_between(x_split[mask2], y_split[mask2], lower_interp2,
                    alpha=0.12, color=GOLD, zorder=2)

    # Label vertices
    for val, label in [(0, "0/1"), (1.0 / 3, "1/3"), (0.5, "1/2"), (1, "1/1")]:
        ax.plot(val, 0, 'o', color=DARK if val != 1.0 / 3 else RED,
                markersize=6 if val != 1.0 / 3 else 8, zorder=5)
        offset = -0.015
        ax.text(val, offset, label, ha='center', va='top', fontsize=11,
                fontweight='bold', color=DARK if val != 1.0 / 3 else RED)

    # Area annotations for sub-triangles
    ax.text(0.38, 0.33, "$\\pi$", ha='center', va='center',
            fontsize=13, color=TEAL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=TEAL, alpha=0.8))
    ax.text(0.62, 0.18, "$\\pi$", ha='center', va='center',
            fontsize=13, color='#C77800', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=GOLD, alpha=0.8))

    # New edge label
    ax.annotate("New geodesic\n$1/3 \\leftrightarrow 1/1$",
                xy=(0.55, 0.28), xytext=(0.82, 0.50),
                fontsize=10, color=RED,
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor=CREAM,
                          edgecolor=RED, alpha=0.9))

    fig.suptitle("Every Farey Insertion Splits an Ideal Triangle",
                 fontsize=16, fontweight='bold', y=1.02)

    # Legend
    legend_elements = [
        Line2D([0], [0], color=BLUE, lw=2.5, label='Existing geodesics'),
        Line2D([0], [0], color=RED, lw=3, linestyle='--', label='New splitting geodesic'),
    ]
    axes[1].legend(handles=legend_elements, loc='upper right', fontsize=9,
                   framealpha=0.9)

    fig.tight_layout()
    path = os.path.join(FIG_DIR, "fig_ideal_triangle_splitting.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {path}")


# =========================================================================
# FIGURE 3: The Modular Surface / Fundamental Domain of PSL₂(ℤ)
# =========================================================================
def figure3_fundamental_domain():
    print("Generating Figure 3: Fundamental Domain of PSL₂(ℤ) ...")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.05, 2.2)
    ax.set_aspect('equal')
    ax.set_facecolor('#FAFAFA')

    # --- Draw the fundamental domain ---
    # Boundaries: |z| = 1 (circular arc), Re(z) = -1/2, Re(z) = 1/2
    # The domain is |z| >= 1 and |Re(z)| <= 1/2

    # Circular arc from -1/2 + i*sqrt(3)/2 to 1/2 + i*sqrt(3)/2
    theta = np.linspace(np.pi / 3, 2 * np.pi / 3, 300)
    arc_x = np.cos(theta)
    arc_y = np.sin(theta)

    # Vertical lines from the arc endpoints up to y_max
    y_top = 2.1
    left_x = -0.5
    right_x = 0.5
    left_y_bottom = np.sqrt(3) / 2
    right_y_bottom = np.sqrt(3) / 2

    # Fill the fundamental domain
    # Build the boundary: left vertical line (top to bottom), arc (left to right),
    # right vertical line (bottom to top), top edge (right to left)
    boundary_x = np.concatenate([
        [left_x, left_x],           # left edge top to bottom
        arc_x,                       # arc left to right
        [right_x, right_x],         # right edge bottom to top
        [right_x, left_x],          # top edge right to left
    ])
    boundary_y = np.concatenate([
        [y_top, left_y_bottom],
        arc_y,
        [right_y_bottom, y_top],
        [y_top, y_top],
    ])
    ax.fill(boundary_x, boundary_y, alpha=0.15, color=BLUE, zorder=2)

    # Draw boundaries
    ax.plot(arc_x, arc_y, color=DARK_BLUE, lw=2.5, zorder=3)
    ax.plot([left_x, left_x], [left_y_bottom, y_top], color=DARK_BLUE,
            lw=2.5, zorder=3)
    ax.plot([right_x, right_x], [right_y_bottom, y_top], color=DARK_BLUE,
            lw=2.5, zorder=3)

    # Dashed continuation upward
    ax.plot([left_x, left_x], [y_top - 0.05, y_top + 0.05], color=DARK_BLUE,
            lw=2.5, linestyle=':', zorder=3)
    ax.plot([right_x, right_x], [y_top - 0.05, y_top + 0.05], color=DARK_BLUE,
            lw=2.5, linestyle=':', zorder=3)

    # Arrow indicating cusp at infinity
    ax.annotate("", xy=(0, 2.15), xytext=(0, 2.0),
                arrowprops=dict(arrowstyle='->', color=DARK_BLUE, lw=2))
    ax.text(0, 2.18, "cusp at $i\\infty$", ha='center', va='bottom',
            fontsize=12, fontweight='bold', color=DARK_BLUE)

    # Label the domain
    ax.text(0, 1.3, "$\\mathcal{F}$", ha='center', va='center',
            fontsize=28, color=DARK_BLUE, fontweight='bold', alpha=0.6)

    # Mark special points
    # rho = e^{i pi/3} = 1/2 + i sqrt(3)/2
    rho_x, rho_y = 0.5, np.sqrt(3) / 2
    ax.plot(rho_x, rho_y, 'o', color=RED, markersize=8, zorder=5)
    ax.text(rho_x + 0.08, rho_y - 0.05, "$\\rho = e^{i\\pi/3}$",
            fontsize=11, color=RED, fontweight='bold')

    # rho-bar
    ax.plot(-rho_x, rho_y, 'o', color=RED, markersize=8, zorder=5)
    ax.text(-rho_x - 0.08, rho_y - 0.05, "$\\bar{\\rho} = e^{2i\\pi/3}$",
            fontsize=11, color=RED, fontweight='bold', ha='right')

    # i
    ax.plot(0, 1, 'o', color=TEAL, markersize=8, zorder=5)
    ax.text(0.08, 1.0, "$i$", fontsize=13, color=TEAL, fontweight='bold')

    # --- Farey tessellation overlay ---
    # Draw some Farey geodesics in the strip near the real axis
    # Farey fractions as cusps: show geodesics between Farey neighbors
    farey = farey_sequence(5)
    # Only draw geodesics within our view
    for i in range(len(farey) - 1):
        f1, f2 = farey[i], farey[i + 1]
        x1, x2 = float(f1), float(f2)
        if x1 >= -0.6 and x2 <= 1.2:
            xs, ys = hyperbolic_geodesic(x1, x2, 200)
            # Clip to our view
            mask = (xs >= -1.2) & (xs <= 1.2) & (ys <= 2.2)
            ax.plot(xs[mask], ys[mask], color=GOLD, lw=1.0, alpha=0.5,
                    zorder=1)

    # Mark Farey fractions on real line that are in view
    ax.axhline(y=0, color=DARK, lw=1.5, zorder=2)
    for f in farey:
        x = float(f)
        if -1.2 <= x <= 1.2:
            ax.plot(x, 0, '|', color=DARK, markersize=8, zorder=5)
            if f.denominator <= 4:
                label = f"{f.numerator}/{f.denominator}" if f.denominator > 1 else str(f.numerator)
                ax.text(x, -0.03, label, ha='center', va='top', fontsize=8,
                        color=DARK)

    # Draw the full unit circle lightly
    theta_full = np.linspace(0, np.pi, 300)
    ax.plot(np.cos(theta_full), np.sin(theta_full), color=MEDIUM_GRAY,
            lw=1, linestyle=':', alpha=0.5, zorder=1)

    # Boundary labels
    ax.text(-0.5, 0.45, "$\\mathrm{Re}(z) = -\\frac{1}{2}$",
            fontsize=10, color=DARK_BLUE, rotation=90, va='bottom', ha='right')
    ax.text(0.5, 0.45, "$\\mathrm{Re}(z) = \\frac{1}{2}$",
            fontsize=10, color=DARK_BLUE, rotation=90, va='bottom', ha='left')
    ax.text(0.35, 0.75, "$|z| = 1$", fontsize=10, color=DARK_BLUE,
            rotation=-30)

    # Annotation about cusps
    ax.annotate(
        "Farey fractions\ncorrespond to cusps\nof the modular surface",
        xy=(0.8, 0.0), xytext=(0.85, 0.5),
        fontsize=10, color=DARK,
        arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5),
        bbox=dict(boxstyle='round,pad=0.4', facecolor=CREAM,
                  edgecolor=GOLD, alpha=0.9)
    )

    ax.set_title("Fundamental Domain of $\\mathrm{PSL}_2(\\mathbb{Z})$\nwith Farey Tessellation",
                 fontsize=15, fontweight='bold', pad=12)
    ax.set_xlabel("$\\mathrm{Re}(z)$", fontsize=12)
    ax.set_ylabel("$\\mathrm{Im}(z)$", fontsize=12)

    fig.tight_layout()
    path = os.path.join(FIG_DIR, "fig_modular_surface.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {path}")


# =========================================================================
# FIGURE 4: Euler Characteristic Preservation
# =========================================================================
def figure4_euler_characteristic():
    print("Generating Figure 4: Euler Characteristic Preservation ...")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    def draw_farey_graph(ax, fracs, title, highlight_new=None):
        """Draw the Farey graph with vertices, edges, faces."""
        ax.set_xlim(-0.15, 1.15)
        ax.set_ylim(-0.08, 0.65)
        ax.set_aspect('equal')
        ax.set_facecolor('#FAFAFA')
        ax.axhline(y=0, color=DARK, lw=1.5, zorder=1)

        edges = []
        for i in range(len(fracs)):
            for j in range(i + 1, len(fracs)):
                if are_tangent(fracs[i], fracs[j]):
                    edges.append((fracs[i], fracs[j]))

        # Draw edges
        for f1, f2 in edges:
            x1, x2 = float(f1), float(f2)
            xs, ys = hyperbolic_geodesic(x1, x2, 200)
            is_new_edge = False
            if highlight_new is not None:
                if f1 in highlight_new or f2 in highlight_new:
                    is_new_edge = True
            color = RED if is_new_edge else BLUE
            lw = 2.5 if is_new_edge else 2.0
            alpha = 0.9 if is_new_edge else 0.7
            ax.plot(xs, ys, color=color, lw=lw, alpha=alpha, zorder=3)

        # Draw vertices
        for f in fracs:
            x = float(f)
            is_new = highlight_new is not None and f in highlight_new
            color = RED if is_new else DARK_BLUE
            size = 10 if is_new else 7
            ax.plot(x, 0, 'o', color=color, markersize=size, zorder=5)
            label = f"{f.numerator}/{f.denominator}" if f.denominator > 1 else str(f.numerator)
            ax.text(x, -0.025, label, ha='center', va='top', fontsize=10,
                    fontweight='bold', color=color)

        ax.set_title(title, fontsize=13, fontweight='bold')

        return len(fracs), len(edges)

    # Before: F_3 = {0/1, 1/3, 1/2, 2/3, 1/1}
    f3 = farey_sequence(3)
    V1, E1 = draw_farey_graph(axes[0], f3, "Before: $\\mathcal{F}_3$")

    # After: insert 2/5 (mediant of 1/3 and 1/2)
    # F_3 with 2/5 added
    f3_plus = sorted(f3 + [Fraction(2, 5)])
    new_fracs = {Fraction(2, 5)}
    V2, E2 = draw_farey_graph(axes[1], f3_plus, "After: Insert $2/5$",
                               highlight_new=new_fracs)

    # Count faces (triangles in Farey graph)
    # For a planar graph with the half-plane as outer face:
    # F = E - V + 2 (Euler's formula for connected planar graph)
    F1 = E1 - V1 + 2
    F2 = E2 - V2 + 2
    chi1 = V1 - E1 + F1
    chi2 = V2 - E2 + F2

    # Add count boxes
    box_style = dict(boxstyle='round,pad=0.5', facecolor=CREAM,
                     edgecolor=DARK, alpha=0.95)

    axes[0].text(0.98, 0.62, f"$V = {V1}$\n$E = {E1}$\n$F = {F1}$\n"
                 f"$\\chi = V - E + F = {chi1}$",
                 transform=axes[0].transAxes, ha='right', va='top',
                 fontsize=11, bbox=box_style, color=DARK,
                 fontfamily='serif')

    axes[1].text(0.98, 0.62, f"$V = {V2}$\n$E = {E2}$\n$F = {F2}$\n"
                 f"$\\chi = V - E + F = {chi2}$",
                 transform=axes[1].transAxes, ha='right', va='top',
                 fontsize=11, bbox=box_style, color=DARK,
                 fontfamily='serif')

    # Delta box between panels
    dV = V2 - V1
    dE = E2 - E1
    dF = F2 - F1
    dchi = chi2 - chi1

    fig.text(0.5, -0.02,
             f"$\\Delta V = +{dV}$,  $\\Delta E = +{dE}$,  "
             f"$\\Delta F = +{dF}$,  "
             f"$\\Delta\\chi = {dV} - {dE} + {dF} = {dchi}$",
             ha='center', va='top', fontsize=14, fontweight='bold',
             color=DARK,
             bbox=dict(boxstyle='round,pad=0.5', facecolor=GOLD,
                       edgecolor=DARK, alpha=0.3))

    # Arrow annotation showing the change
    fig.text(0.5, -0.07,
             "Each Farey insertion: $+1$ vertex, $+2$ edges, $+1$ face  "
             "$\\Longrightarrow$  $\\chi$ invariant",
             ha='center', va='top', fontsize=12, color=DARK,
             style='italic')

    fig.suptitle("Euler Characteristic Preservation Under Farey Insertion",
                 fontsize=15, fontweight='bold', y=1.02)

    # Legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=DARK_BLUE,
               markersize=8, label='Existing vertex'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=RED,
               markersize=10, label='New vertex ($2/5$)'),
        Line2D([0], [0], color=BLUE, lw=2, label='Existing edge'),
        Line2D([0], [0], color=RED, lw=2.5, label='New edge'),
    ]
    axes[1].legend(handles=legend_elements, loc='upper left', fontsize=9,
                   framealpha=0.9)

    fig.tight_layout()
    path = os.path.join(FIG_DIR, "fig_euler_characteristic.png")
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {path}")


# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("PSL₂(ℤ) / Ford Circle Visualization Suite")
    print("=" * 60)
    figure1_ford_circles()
    figure2_ideal_triangle()
    figure3_fundamental_domain()
    figure4_euler_characteristic()
    print("=" * 60)
    print("All figures generated successfully.")
    print(f"Output directory: {FIG_DIR}")
