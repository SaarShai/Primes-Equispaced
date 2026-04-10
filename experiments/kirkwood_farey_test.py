#!/usr/bin/env python3
"""
Kirkwood Gap / Farey Sequence Correlation Analysis
===================================================
Tests whether Kirkwood gap depths in the asteroid belt correlate with
Farey sequence properties (denominator q, gap width 1/q^2, discrepancy).

Data source: NASA JPL Small-Body Database API
Fallback: synthetic distribution matching known gap positions/depths.

Author: Farey Project (automated analysis)
Date: 2026-03-27
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy import stats
from scipy.signal import savgol_filter
from fractions import Fraction
import json
import os
import time
import sys

# ─── Configuration ───────────────────────────────────────────────────
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
JUPITER_A = 5.2044  # AU
A_MIN, A_MAX = 2.0, 3.5  # main belt range in AU
HIST_BINS = 500  # fine-grained histogram
FAREY_ORDER = 10  # F_10 for analysis
GAP_WINDOW_AU = 0.02  # half-width for gap depth measurement in AU

# Known Kirkwood gaps for validation
KNOWN_GAPS = {
    '4:1': {'a': 2.058, 'ratio': Fraction(1, 4)},
    '3:1': {'a': 2.500, 'ratio': Fraction(1, 3)},
    '5:2': {'a': 2.824, 'ratio': Fraction(2, 5)},
    '7:3': {'a': 2.957, 'ratio': Fraction(3, 7)},
    '2:1': {'a': 3.276, 'ratio': Fraction(1, 2)},
    '9:4': {'a': 3.030, 'ratio': Fraction(4, 9)},
    '5:3': {'a': 3.075, 'ratio': Fraction(3, 5)},  # weaker gap
    '7:4': {'a': 3.175, 'ratio': Fraction(4, 7)},  # Hilda region boundary
}


def fetch_jpl_data():
    """Fetch asteroid semi-major axes from JPL Small-Body Database API."""
    import urllib.request
    import urllib.parse

    print("Fetching asteroid data from JPL SSD API...")
    # Query: numbered asteroids, main belt, return semi-major axis
    # The API supports field selection and constraints
    base_url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
    params = {
        'fields': 'a',
        'sb-kind': 'a',       # asteroids only
        'sb-class': 'MBA',    # main belt asteroids
    }
    query_str = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_str}"

    print(f"  URL: {url}")
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'FareyProject/1.0 (research)')

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
            data = json.loads(raw)

        # Parse the response
        fields = data.get('fields', [])
        rows = data.get('data', [])
        print(f"  Received {len(rows)} asteroids, fields: {fields}")

        # Find the 'a' column index
        a_idx = fields.index('a')
        semi_major_axes = np.empty(len(rows), dtype=np.float64)
        count = 0
        for row in rows:
            try:
                a_val = float(row[a_idx])
                if A_MIN <= a_val <= A_MAX:
                    semi_major_axes[count] = a_val
                    count += 1
            except (ValueError, TypeError):
                continue

        a_array = semi_major_axes[:count].copy()
        print(f"  {len(a_array)} asteroids in range [{A_MIN}, {A_MAX}] AU")
        return a_array

    except Exception as e:
        print(f"  JPL API failed: {e}")
        return None


def fetch_mpc_data():
    """Try Minor Planet Center data as backup."""
    import urllib.request

    print("Trying MPC orbital elements (MPCORB)...")
    # MPC provides a compact format; try their JSON API
    url = "https://minorplanetcenter.net/Extended_Files/mpcorb_extended.json.gz"
    # This is huge; let's try the API instead
    # Actually, let's try the simpler approach: astquery
    # For speed, we can use the astorb database format

    # Alternative: use the SSD close-approach or sbdb APIs with pagination
    # Let's try a different JPL endpoint that's more reliable
    base_url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"

    # Try fetching in batches by spkid range
    all_axes = []
    # Main belt numbered asteroids are roughly spkid 2000001 to 2700000+
    # Let's try a simpler constraint
    import urllib.parse
    params = {
        'fields': 'a',
        'sb-kind': 'a',
        'sb-ns': 'n',   # numbered only
        'sb-class': 'MBA',
        'limit': '0',
    }
    query_str = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_str}"
    print(f"  Trying numbered MBA query: {url}")

    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'FareyProject/1.0 (research)')

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read()
            data = json.loads(raw)
        fields = data.get('fields', [])
        rows = data.get('data', [])
        print(f"  Received {len(rows)} numbered MBAs")
        a_idx = fields.index('a')
        axes = []
        for row in rows:
            try:
                a_val = float(row[a_idx])
                if A_MIN <= a_val <= A_MAX:
                    axes.append(a_val)
            except (ValueError, TypeError):
                continue
        if len(axes) > 1000:
            return np.array(axes)
    except Exception as e:
        print(f"  MPC backup also failed: {e}")

    return None


def generate_synthetic_data(n=500000):
    """
    Generate synthetic asteroid distribution matching known Kirkwood gap
    positions and depths. Uses empirical knowledge from asteroid surveys.
    """
    print("Generating synthetic asteroid distribution (fallback)...")
    print("  (Based on empirical Kirkwood gap positions and depths)")

    # Background: roughly proportional to a^2 (volume of annulus), with
    # enhanced density in certain families
    rng = np.random.default_rng(42)

    # Base distribution: mixture of broad Gaussians for asteroid families
    # plus a smooth background
    a_vals = []

    # Smooth background
    n_bg = int(n * 0.4)
    a_bg = rng.uniform(A_MIN, A_MAX, n_bg)
    a_vals.append(a_bg)

    # Major concentrations (Flora, Nysa, Koronis, Eos, Themis, etc.)
    families = [
        (2.20, 0.08, 0.10),  # Flora family
        (2.42, 0.05, 0.06),  # Nysa-Polana
        (2.62, 0.06, 0.05),  # near 5:2
        (2.87, 0.04, 0.08),  # Koronis
        (3.02, 0.04, 0.06),  # Eos
        (3.15, 0.05, 0.10),  # Themis
        (2.36, 0.03, 0.05),  # Vesta family
    ]
    for center, sigma, frac in families:
        n_fam = int(n * frac)
        a_fam = rng.normal(center, sigma, n_fam)
        a_fam = a_fam[(a_fam >= A_MIN) & (a_fam <= A_MAX)]
        a_vals.append(a_fam)

    a_all = np.concatenate(a_vals)

    # Now carve out the Kirkwood gaps with realistic depths
    # Gap parameters: (center_au, half_width_au, depletion_fraction)
    gap_params = [
        (2.058, 0.015, 0.95),  # 4:1 - very deep
        (2.500, 0.025, 0.92),  # 3:1 - very deep, wider
        (2.824, 0.020, 0.85),  # 5:2 - deep
        (2.957, 0.012, 0.70),  # 7:3 - moderate
        (3.276, 0.030, 0.90),  # 2:1 - very deep, wide
        (3.030, 0.008, 0.40),  # 9:4 - weak
        (3.075, 0.006, 0.25),  # 5:3 - very weak
        (3.175, 0.005, 0.20),  # 7:4 - very weak
    ]

    for center, hw, depletion in gap_params:
        mask = np.abs(a_all - center) < hw
        # Remove fraction of asteroids in gap
        remove = rng.random(mask.sum()) < depletion
        indices_in_gap = np.where(mask)[0]
        indices_to_remove = indices_in_gap[remove]
        a_all = np.delete(a_all, indices_to_remove)

    print(f"  Generated {len(a_all)} synthetic asteroids")
    return a_all


def compute_period_ratios(a_array):
    """Convert semi-major axes to period ratios with Jupiter."""
    # Kepler's third law: T ~ a^(3/2)
    # Period ratio = T_asteroid / T_Jupiter = (a/a_J)^(3/2)
    return (a_array / JUPITER_A) ** 1.5


def farey_sequence(n):
    """Generate Farey sequence F_n as list of Fraction objects."""
    fracs = set()
    for q in range(1, n + 1):
        for p in range(0, q + 1):
            fracs.add(Fraction(p, q))
    return sorted(fracs)


def farey_in_range(order, lo, hi):
    """Get Farey fractions in [lo, hi] range."""
    seq = farey_sequence(order)
    return [f for f in seq if lo <= float(f) <= hi]


def farey_discrepancy(p, q, order):
    """
    Compute the Farey discrepancy D(p/q) for p/q in F_order.
    D(p/q) = index(p/q in F_n) - n*(n+1)/2 * (p/q) - 1/2
    This measures deviation from uniform spacing.
    """
    # Generate full Farey sequence and find index
    seq = farey_sequence(order)
    frac = Fraction(p, q)
    try:
        idx = seq.index(frac)
    except ValueError:
        return None
    N = len(seq) - 1  # number of intervals
    expected = N * float(frac)
    return idx - expected


def farey_neighbors(frac, order):
    """Find left and right Farey neighbors of frac in F_order."""
    seq = farey_sequence(order)
    try:
        idx = seq.index(frac)
    except ValueError:
        return None, None
    left = seq[idx - 1] if idx > 0 else None
    right = seq[idx + 1] if idx < len(seq) - 1 else None
    return left, right


def farey_gap_width(frac, order):
    """
    Width of the Farey interval containing frac in F_order.
    For p/q, theoretical width ~ 1/q^2 for large q.
    Actual: distance to left neighbor + distance to right neighbor.
    """
    left, right = farey_neighbors(frac, order)
    width = 0
    if left is not None:
        width += float(frac) - float(left)
    if right is not None:
        width += float(right) - float(frac)
    return width


def measure_gap_depth(a_array, center_au, window=GAP_WINDOW_AU, background_mult=3.0):
    """
    Measure gap depth at a given semi-major axis position.
    Returns depth as fractional depletion: 1 - (count_in_gap / expected_count).

    Method: compare asteroid count in narrow window around center to
    average of flanking regions.
    """
    in_gap = np.sum(np.abs(a_array - center_au) < window)

    # Background: flanking regions, same width
    left_center = center_au - window * background_mult
    right_center = center_au + window * background_mult
    in_left = np.sum(np.abs(a_array - left_center) < window)
    in_right = np.sum(np.abs(a_array - right_center) < window)
    background = (in_left + in_right) / 2.0

    if background == 0:
        return 0.0
    depth = 1.0 - (in_gap / background)
    return max(depth, 0.0)  # clamp negative (no gap)


def measure_gap_depth_histogram(hist_counts, bin_centers, center_ratio,
                                  window_ratio=0.005, bg_mult=3.0):
    """Measure gap depth from histogram data in period-ratio space."""
    gap_mask = np.abs(bin_centers - center_ratio) < window_ratio
    gap_count = hist_counts[gap_mask].mean() if gap_mask.any() else 0

    left_center = center_ratio - window_ratio * bg_mult
    right_center = center_ratio + window_ratio * bg_mult
    left_mask = np.abs(bin_centers - left_center) < window_ratio
    right_mask = np.abs(bin_centers - right_center) < window_ratio

    bg_left = hist_counts[left_mask].mean() if left_mask.any() else 0
    bg_right = hist_counts[right_mask].mean() if right_mask.any() else 0
    background = (bg_left + bg_right) / 2.0

    if background <= 0:
        return 0.0
    depth = 1.0 - (gap_count / background)
    return max(depth, 0.0)


def au_to_ratio(a):
    """Convert AU to period ratio with Jupiter."""
    return (a / JUPITER_A) ** 1.5


def ratio_to_au(r):
    """Convert period ratio to AU."""
    return JUPITER_A * r ** (2.0 / 3.0)


def run_analysis():
    """Main analysis pipeline."""
    print("=" * 70)
    print("KIRKWOOD GAP / FAREY SEQUENCE CORRELATION ANALYSIS")
    print("=" * 70)

    # ─── Step 1: Get asteroid data ───────────────────────────────────
    print("\n--- Step 1: Acquiring asteroid semi-major axis data ---")
    data_source = "unknown"
    a_data = fetch_jpl_data()
    if a_data is not None and len(a_data) > 10000:
        data_source = "JPL Small-Body Database API"
        print(f"  SUCCESS: {len(a_data)} asteroids from JPL")
    else:
        a_data = fetch_mpc_data()
        if a_data is not None and len(a_data) > 10000:
            data_source = "JPL (numbered MBA query)"
            print(f"  SUCCESS: {len(a_data)} asteroids from JPL (backup)")
        else:
            a_data = generate_synthetic_data()
            data_source = "Synthetic (empirical gap model)"
            print(f"  FALLBACK: Using synthetic data ({len(a_data)} asteroids)")

    # ─── Step 2: Compute period ratios ───────────────────────────────
    print("\n--- Step 2: Computing period ratios ---")
    ratios = compute_period_ratios(a_data)
    print(f"  Period ratio range: [{ratios.min():.4f}, {ratios.max():.4f}]")
    print(f"  (Corresponding to a = [{A_MIN}, {A_MAX}] AU)")

    # ─── Step 3: Build histogram ─────────────────────────────────────
    print("\n--- Step 3: Building asteroid histogram ---")
    # Histogram in AU space
    hist_a, bin_edges_a = np.histogram(a_data, bins=HIST_BINS, range=(A_MIN, A_MAX))
    bin_centers_a = 0.5 * (bin_edges_a[:-1] + bin_edges_a[1:])

    # Histogram in ratio space
    ratio_min, ratio_max = au_to_ratio(A_MIN), au_to_ratio(A_MAX)
    hist_r, bin_edges_r = np.histogram(ratios, bins=HIST_BINS,
                                        range=(ratio_min, ratio_max))
    bin_centers_r = 0.5 * (bin_edges_r[:-1] + bin_edges_r[1:])

    # Smooth for gap detection
    if len(hist_a) > 51:
        hist_smooth = savgol_filter(hist_a.astype(float), 31, 3)
    else:
        hist_smooth = hist_a.astype(float)

    # ─── Step 4: Farey sequence analysis ─────────────────────────────
    print(f"\n--- Step 4: Farey sequence F_{FAREY_ORDER} analysis ---")
    farey_fracs = farey_in_range(FAREY_ORDER, ratio_min, ratio_max)
    print(f"  {len(farey_fracs)} Farey fractions in range "
          f"[{ratio_min:.4f}, {ratio_max:.4f}]")

    # For each Farey fraction, measure gap depth and Farey properties
    results = []
    for frac in farey_fracs:
        p, q = frac.numerator, frac.denominator
        if q <= 1:
            continue  # skip trivial fractions

        r = float(frac)
        a_center = ratio_to_au(r)

        # Measure gap depth in AU space
        depth_au = measure_gap_depth(a_data, a_center,
                                      window=GAP_WINDOW_AU)

        # Measure gap depth in ratio space
        ratio_window = 0.005
        depth_ratio = measure_gap_depth_histogram(
            hist_r, bin_centers_r, r, window_ratio=ratio_window)

        # Farey properties
        disc = farey_discrepancy(p, q, FAREY_ORDER)
        gw = farey_gap_width(frac, FAREY_ORDER)
        inv_q2 = 1.0 / (q * q)

        # Check if this is a known gap
        known_name = None
        for name, info in KNOWN_GAPS.items():
            if info['ratio'] == frac:
                known_name = name

        results.append({
            'p': p, 'q': q, 'fraction': str(frac),
            'ratio': r, 'a_au': a_center,
            'depth_au': depth_au, 'depth_ratio': depth_ratio,
            'denominator': q, 'inv_q2': inv_q2,
            'discrepancy': disc, 'gap_width': gw,
            'known_gap': known_name,
        })

    # Sort by denominator for display
    results.sort(key=lambda x: (x['q'], x['p']))

    print(f"\n  {'Fraction':<10} {'a (AU)':<8} {'Depth(AU)':<10} "
          f"{'Depth(R)':<10} {'q':<4} {'1/q^2':<10} {'Known':<8}")
    print("  " + "-" * 68)
    for r in results:
        known_str = r['known_gap'] if r['known_gap'] else ''
        print(f"  {r['fraction']:<10} {r['a_au']:<8.3f} {r['depth_au']:<10.4f} "
              f"{r['depth_ratio']:<10.4f} {r['q']:<4} {r['inv_q2']:<10.6f} "
              f"{known_str:<8}")

    # ─── Step 5: Statistical tests ───────────────────────────────────
    print("\n--- Step 5: Statistical correlation tests ---")

    # Filter to fractions with nonzero gap depth (detectable gaps only)
    sig_results = [r for r in results if r['depth_au'] > 0.05]
    all_results = results

    # Arrays for correlation
    depths_au = np.array([r['depth_au'] for r in all_results])
    depths_ratio = np.array([r['depth_ratio'] for r in all_results])
    denoms = np.array([r['q'] for r in all_results])
    inv_q2 = np.array([r['inv_q2'] for r in all_results])
    gap_widths = np.array([r['gap_width'] for r in all_results])
    discrepancies = np.array([r['discrepancy'] for r in all_results])

    # Test 1: depth vs 1/q^2 (our main prediction)
    corr1, p1 = stats.spearmanr(inv_q2, depths_au)
    corr1_p, p1_p = stats.pearsonr(inv_q2, depths_au)
    print(f"\n  Test 1: Gap depth (AU) vs 1/q^2")
    print(f"    Spearman r = {corr1:.4f}, p = {p1:.2e}")
    print(f"    Pearson  r = {corr1_p:.4f}, p = {p1_p:.2e}")

    # Test 2: depth vs denominator q (expect negative: bigger q = shallower)
    corr2, p2 = stats.spearmanr(denoms, depths_au)
    corr2_p, p2_p = stats.pearsonr(denoms, depths_au)
    print(f"\n  Test 2: Gap depth (AU) vs denominator q")
    print(f"    Spearman r = {corr2:.4f}, p = {p2:.2e}")
    print(f"    Pearson  r = {corr2_p:.4f}, p = {p2_p:.2e}")

    # Test 3: depth vs Farey gap width
    corr3, p3 = stats.spearmanr(gap_widths, depths_au)
    corr3_p, p3_p = stats.pearsonr(gap_widths, depths_au)
    print(f"\n  Test 3: Gap depth (AU) vs Farey gap width")
    print(f"    Spearman r = {corr3:.4f}, p = {p3:.2e}")
    print(f"    Pearson  r = {corr3_p:.4f}, p = {p3_p:.2e}")

    # Test 4: depth vs |discrepancy|
    abs_disc = np.abs(discrepancies)
    corr4, p4 = stats.spearmanr(abs_disc, depths_au)
    print(f"\n  Test 4: Gap depth (AU) vs |discrepancy|")
    print(f"    Spearman r = {corr4:.4f}, p = {p4:.2e}")

    # Test 5: For significant gaps only (depth > 0.05)
    if len(sig_results) >= 5:
        sig_depths = np.array([r['depth_au'] for r in sig_results])
        sig_inv_q2 = np.array([r['inv_q2'] for r in sig_results])
        sig_denoms = np.array([r['q'] for r in sig_results])
        sig_gw = np.array([r['gap_width'] for r in sig_results])

        corr5, p5 = stats.spearmanr(sig_inv_q2, sig_depths)
        print(f"\n  Test 5: Significant gaps only (depth > 0.05, n={len(sig_results)})")
        print(f"    depth vs 1/q^2: Spearman r = {corr5:.4f}, p = {p5:.2e}")

        corr5b, p5b = stats.spearmanr(sig_denoms, sig_depths)
        print(f"    depth vs q:     Spearman r = {corr5b:.4f}, p = {p5b:.2e}")

        corr5c, p5c = stats.spearmanr(sig_gw, sig_depths)
        print(f"    depth vs gw:    Spearman r = {corr5c:.4f}, p = {p5c:.2e}")

    # Test 6: Power law fit depth ~ q^alpha
    # Use log-log regression on significant gaps
    if len(sig_results) >= 5:
        log_q = np.log(sig_denoms)
        log_d = np.log(sig_depths + 1e-10)
        slope, intercept, r_val, p_val, se = stats.linregress(log_q, log_d)
        print(f"\n  Test 6: Power law fit depth ~ q^alpha (significant gaps)")
        print(f"    alpha = {slope:.3f} +/- {se:.3f}")
        print(f"    R^2 = {r_val**2:.4f}, p = {p_val:.2e}")
        print(f"    (Prediction: alpha ~ -2 if depth ~ 1/q^2)")

    # ─── Step 6: Plots ───────────────────────────────────────────────
    print("\n--- Step 6: Generating plots ---")

    # Plot (a): Asteroid histogram with Farey fractions marked
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(bin_centers_a, hist_a, width=(A_MAX - A_MIN) / HIST_BINS,
           color='steelblue', alpha=0.7, label='Asteroid count')
    if len(hist_smooth) == len(bin_centers_a):
        ax.plot(bin_centers_a, hist_smooth, 'k-', lw=1.5, alpha=0.5,
                label='Smoothed')

    # Mark known Kirkwood gaps
    colors = {'4:1': 'red', '3:1': 'red', '5:2': 'orange', '7:3': 'green',
              '2:1': 'red', '9:4': 'purple', '5:3': 'brown', '7:4': 'pink'}
    for name, info in KNOWN_GAPS.items():
        a_val = info['a']
        q_val = info['ratio'].denominator
        c = colors.get(name, 'gray')
        ax.axvline(a_val, color=c, linestyle='--', alpha=0.8, lw=1.5)
        ax.text(a_val, ax.get_ylim()[1] * 0.95 if ax.get_ylim()[1] > 0 else 100,
                f'{name}\n(q={q_val})', ha='center', va='top', fontsize=8,
                color=c, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    ax.set_xlabel('Semi-major axis (AU)', fontsize=12)
    ax.set_ylabel('Asteroid count', fontsize=12)
    ax.set_title(f'Main Belt Asteroid Distribution with Kirkwood Gaps\n'
                 f'(Data: {data_source}, n={len(a_data):,})', fontsize=13)
    ax.legend(loc='upper left')
    ax.set_xlim(A_MIN, A_MAX)
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'kirkwood_histogram.png'), dpi=150)
    print(f"  Saved kirkwood_histogram.png")
    plt.close()

    # Plot (b): Gap depth vs denominator
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    # Panel 1: depth vs denominator q
    ax1 = axes[0]
    for r in all_results:
        marker = '*' if r['known_gap'] else 'o'
        size = 120 if r['known_gap'] else 40
        color = 'red' if r['known_gap'] else 'steelblue'
        ax1.scatter(r['q'], r['depth_au'], s=size, c=color, marker=marker,
                    alpha=0.7, edgecolors='black', linewidth=0.5, zorder=5)
        if r['known_gap']:
            ax1.annotate(r['known_gap'], (r['q'], r['depth_au']),
                         textcoords="offset points", xytext=(5, 5), fontsize=7)

    ax1.set_xlabel('Denominator q', fontsize=11)
    ax1.set_ylabel('Gap Depth (fractional depletion)', fontsize=11)
    ax1.set_title(f'Gap Depth vs Denominator\n'
                  f'Spearman r={corr2:.3f}, p={p2:.2e}', fontsize=11)
    ax1.axhline(0, color='gray', linestyle='-', alpha=0.3)

    # Panel 2: depth vs 1/q^2
    ax2 = axes[1]
    for r in all_results:
        marker = '*' if r['known_gap'] else 'o'
        size = 120 if r['known_gap'] else 40
        color = 'red' if r['known_gap'] else 'steelblue'
        ax2.scatter(r['inv_q2'], r['depth_au'], s=size, c=color, marker=marker,
                    alpha=0.7, edgecolors='black', linewidth=0.5, zorder=5)
        if r['known_gap']:
            ax2.annotate(r['known_gap'], (r['inv_q2'], r['depth_au']),
                         textcoords="offset points", xytext=(5, 5), fontsize=7)

    # Add regression line
    mask_pos = depths_au > 0
    if mask_pos.sum() > 2:
        slope_fit, int_fit, _, _, _ = stats.linregress(inv_q2[mask_pos], depths_au[mask_pos])
        x_fit = np.linspace(0, inv_q2.max(), 100)
        ax2.plot(x_fit, slope_fit * x_fit + int_fit, 'r--', alpha=0.5,
                 label=f'Linear fit (slope={slope_fit:.2f})')
        ax2.legend(fontsize=9)

    ax2.set_xlabel('1/q^2 (Farey gap width proxy)', fontsize=11)
    ax2.set_ylabel('Gap Depth (fractional depletion)', fontsize=11)
    ax2.set_title(f'Gap Depth vs 1/q^2\n'
                  f'Spearman r={corr1:.3f}, p={p1:.2e}', fontsize=11)

    # Panel 3: depth vs Farey gap width
    ax3 = axes[2]
    for r in all_results:
        marker = '*' if r['known_gap'] else 'o'
        size = 120 if r['known_gap'] else 40
        color = 'red' if r['known_gap'] else 'steelblue'
        ax3.scatter(r['gap_width'], r['depth_au'], s=size, c=color, marker=marker,
                    alpha=0.7, edgecolors='black', linewidth=0.5, zorder=5)
        if r['known_gap']:
            ax3.annotate(r['known_gap'], (r['gap_width'], r['depth_au']),
                         textcoords="offset points", xytext=(5, 5), fontsize=7)

    ax3.set_xlabel(f'Farey gap width (in F_{FAREY_ORDER})', fontsize=11)
    ax3.set_ylabel('Gap Depth (fractional depletion)', fontsize=11)
    ax3.set_title(f'Gap Depth vs Farey Gap Width\n'
                  f'Spearman r={corr3:.3f}, p={p3:.2e}', fontsize=11)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'kirkwood_correlations.png'), dpi=150)
    print(f"  Saved kirkwood_correlations.png")
    plt.close()

    # Plot (c): Log-log plot for power law
    if len(sig_results) >= 5:
        fig, ax = plt.subplots(figsize=(8, 6))
        sig_q_arr = np.array([r['q'] for r in sig_results])
        sig_d_arr = np.array([r['depth_au'] for r in sig_results])

        for r in sig_results:
            marker = '*' if r['known_gap'] else 'o'
            size = 150 if r['known_gap'] else 60
            color = 'red' if r['known_gap'] else 'steelblue'
            ax.scatter(r['q'], r['depth_au'], s=size, c=color, marker=marker,
                       alpha=0.8, edgecolors='black', linewidth=0.5, zorder=5)
            if r['known_gap']:
                ax.annotate(r['known_gap'], (r['q'], r['depth_au']),
                            textcoords="offset points", xytext=(8, 3), fontsize=9)

        # Power law fit line
        q_range = np.linspace(1.5, sig_q_arr.max() * 1.2, 100)
        ax.plot(q_range, np.exp(intercept) * q_range ** slope, 'r--', lw=2,
                alpha=0.6, label=f'Fit: depth ~ q^{{{slope:.2f}}}')

        # Reference line: 1/q^2
        ref_scale = sig_d_arr[np.argmin(sig_q_arr)] * sig_q_arr.min() ** 2
        ax.plot(q_range, ref_scale / q_range ** 2, 'g:', lw=2, alpha=0.6,
                label='Reference: 1/q^2')

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Denominator q', fontsize=12)
        ax.set_ylabel('Gap Depth', fontsize=12)
        ax.set_title(f'Power Law: Gap Depth vs Denominator\n'
                     f'Fit: depth ~ q^{{{slope:.2f} +/- {se:.2f}}}, '
                     f'R^2={r_val**2:.3f}', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, which='both')
        plt.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, 'kirkwood_powerlaw.png'), dpi=150)
        print(f"  Saved kirkwood_powerlaw.png")
        plt.close()

    # ─── Step 7: Write results report ────────────────────────────────
    print("\n--- Step 7: Writing results report ---")
    report = generate_report(data_source, a_data, results, sig_results,
                             corr1, p1, corr1_p, p1_p,
                             corr2, p2, corr2_p, p2_p,
                             corr3, p3, corr3_p, p3_p,
                             corr4, p4,
                             locals())
    report_path = os.path.join(OUTPUT_DIR, 'KIRKWOOD_RESULTS.md')
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"  Saved KIRKWOOD_RESULTS.md")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    return results


def generate_report(data_source, a_data, results, sig_results,
                    corr1, p1, corr1_p, p1_p,
                    corr2, p2, corr2_p, p2_p,
                    corr3, p3, corr3_p, p3_p,
                    corr4, p4, local_vars):
    """Generate the markdown results report."""

    # Extract power law results if available
    alpha = local_vars.get('slope', None)
    alpha_se = local_vars.get('se', None)
    alpha_r2 = local_vars.get('r_val', None)

    n_asteroids = len(a_data)
    n_farey = len(results)
    n_sig = len(sig_results)

    known_gap_results = [r for r in results if r['known_gap']]
    known_gap_results.sort(key=lambda x: x['q'])

    report = f"""# Kirkwood Gap / Farey Sequence Correlation Analysis

## Summary

This analysis tests whether the depths of Kirkwood gaps in the asteroid belt
correlate with properties of the corresponding Farey fractions. The central
prediction: **gap depth should scale as 1/q^2** (where q is the denominator
of the resonance ratio p/q), because the Farey gap width around p/q is
approximately 1/q^2.

**Data source:** {data_source}
**Asteroids analyzed:** {n_asteroids:,}
**Semi-major axis range:** {A_MIN} - {A_MAX} AU
**Farey order:** F_{FAREY_ORDER}
**Farey fractions in range:** {n_farey}
**Fractions with detectable gaps (depth > 0.05):** {n_sig}

## Known Kirkwood Gaps

| Resonance | a (AU) | Period Ratio | q | 1/q^2 | Measured Depth |
|-----------|--------|-------------|---|-------|----------------|
"""
    for r in known_gap_results:
        report += (f"| {r['known_gap']} | {r['a_au']:.3f} | {r['fraction']} | "
                   f"{r['q']} | {r['inv_q2']:.4f} | {r['depth_au']:.4f} |\n")

    report += f"""
## Correlation Results

### Test 1: Gap Depth vs 1/q^2 (PRIMARY PREDICTION)

| Metric | Value |
|--------|-------|
| Spearman r | {corr1:.4f} |
| Spearman p-value | {p1:.2e} |
| Pearson r | {corr1_p:.4f} |
| Pearson p-value | {p1_p:.2e} |

**Interpretation:** {"Strong positive correlation supports the Farey gap width prediction." if corr1 > 0.3 and p1 < 0.05 else "Weak or non-significant correlation." if corr1 > 0 else "Negative correlation contradicts prediction."}

### Test 2: Gap Depth vs Denominator q

| Metric | Value |
|--------|-------|
| Spearman r | {corr2:.4f} |
| Spearman p-value | {p2:.2e} |
| Pearson r | {corr2_p:.4f} |
| Pearson p-value | {p2_p:.2e} |

**Interpretation:** {"Negative correlation confirms larger denominators produce shallower gaps." if corr2 < -0.3 and p2 < 0.05 else "Weak correlation."}

### Test 3: Gap Depth vs Farey Gap Width

| Metric | Value |
|--------|-------|
| Spearman r | {corr3:.4f} |
| Spearman p-value | {p3:.2e} |
| Pearson r | {corr3_p:.4f} |
| Pearson p-value | {p3_p:.2e} |

### Test 4: Gap Depth vs |Farey Discrepancy|

| Metric | Value |
|--------|-------|
| Spearman r | {corr4:.4f} |
| Spearman p-value | {p4:.2e} |

"""
    if alpha is not None:
        alpha_r2_val = alpha_r2 ** 2 if alpha_r2 else 0
        report += f"""### Test 6: Power Law Fit (significant gaps only)

Fit: depth ~ q^alpha

| Parameter | Value |
|-----------|-------|
| alpha | {alpha:.3f} +/- {alpha_se:.3f} |
| R^2 | {alpha_r2_val:.4f} |
| Predicted alpha | -2.0 (from 1/q^2) |

**Interpretation:** {"Close to predicted -2 exponent!" if abs(alpha + 2) < 1 else "Exponent differs from predicted -2."}

"""

    report += f"""## All Measured Fractions

| Fraction | a (AU) | q | Depth | 1/q^2 | Gap Width | Known |
|----------|--------|---|-------|-------|-----------|-------|
"""
    for r in sorted(results, key=lambda x: -x['depth_au']):
        known = r['known_gap'] or ''
        report += (f"| {r['fraction']} | {r['a_au']:.3f} | {r['q']} | "
                   f"{r['depth_au']:.4f} | {r['inv_q2']:.6f} | "
                   f"{r['gap_width']:.6f} | {known} |\n")

    report += f"""
## Figures

- `kirkwood_histogram.png` - Asteroid distribution with Kirkwood gaps marked
- `kirkwood_correlations.png` - Three-panel correlation plots
- `kirkwood_powerlaw.png` - Log-log power law analysis

## Method Notes

1. **Gap depth** measured as fractional depletion: 1 - (count_in_gap / background_count),
   where background is the average of flanking regions at 3x the gap half-width.
2. **Farey properties** computed from F_{FAREY_ORDER}.
3. **Period ratios** via Kepler's third law: T_ratio = (a/a_Jupiter)^(3/2).
4. Statistical tests use both Spearman (rank) and Pearson (linear) correlations.

## Physical Interpretation

The Kirkwood gaps arise from orbital resonances with Jupiter. At a mean-motion
resonance p:q, repeated gravitational perturbations at the same orbital phase
destabilize asteroids. The **strength** of this resonance depends on q (the
order): lower-order resonances (small q) are stronger, producing deeper gaps.

The Farey sequence connection: in F_n, the "territory" around p/q has width
approximately 1/q^2. This is the **mediant interval** width. Our analysis
tests whether the physical gap depth scales similarly with 1/q^2, which would
indicate that Farey sequence geometry directly predicts the resonance structure.
"""
    return report


if __name__ == '__main__':
    run_analysis()
