#!/usr/bin/env python3
"""
Extended Periodic Table of Three-Body Orbits
============================================
Extends the equal-mass periodic table (691 orbits) with 1,349 unequal-mass orbits.
Investigates the m3=4 correlation reversal and discovers new orbit predictions.

Tasks:
1. Compute CF properties for all 1,349 unequal-mass orbits
2. Build extended 3D periodic table (period x gmean x mass_ratio)
3. Investigate m3=4 nobility-entropy correlation reversal
4. Identify empty cells filled by unequal-mass orbits
5. Mass-ratio scaling analysis for shared orbit types
"""

import re
import sys
import json
import numpy as np
from fractions import Fraction
from collections import Counter, defaultdict
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

OUTDIR = '/Users/saar/Desktop/Farey-Local/experiments'

# ============================================================
# PART 0: Core CF computation (from existing code)
# ============================================================

L = np.array([[1, 0], [2, 1]], dtype=np.int64)
R = np.array([[1, 2], [0, 1]], dtype=np.int64)
L_inv = np.array([[1, 0], [-2, 1]], dtype=np.int64)
R_inv = np.array([[1, -2], [0, 1]], dtype=np.int64)

GENERATOR_MAP = {'A': L, 'a': L_inv, 'B': R, 'b': R_inv}

def word_to_gamma2_matrix(word):
    M = np.eye(2, dtype=np.int64)
    for letter in word:
        M = M @ GENERATOR_MAP[letter]
    return M

def matrix_to_cf(M):
    a, b = abs(M[0, 0]), abs(M[0, 1])
    c, d = abs(M[1, 0]), abs(M[1, 1])
    if a == 0:
        return []
    cf = []
    num, den = c, a
    while den > 0:
        q, r = divmod(num, den)
        cf.append(int(q))
        num, den = den, r
    return cf

def cf_to_nobility(cf):
    if not cf:
        return 0.0
    return sum(1 for x in cf if x == 1) / len(cf)

def cf_gmean(cf):
    if not cf or len(cf) == 0:
        return 1.0
    cf_pos = [x for x in cf if x > 0]
    if not cf_pos:
        return 1.0
    return np.exp(np.mean(np.log(cf_pos)))

def braid_entropy_estimate(word):
    M = word_to_gamma2_matrix(word)
    trace = abs(M[0,0] + M[1,1])
    if trace <= 2:
        return 0.0
    sr = (trace + np.sqrt(float(trace)**2 - 4)) / 2
    return np.log(float(sr)) / len(word) if len(word) > 0 else 0.0


# ============================================================
# PART 1: Parse data
# ============================================================

def parse_unequal_mass_words(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
    rows = re.findall(r'<tr>\s*<th>(.*?)</th>\s*<td>(.*?)</td>\s*</tr>', html, re.DOTALL)
    results = []
    for class_info, word in rows:
        if 'Free group' in word or 'Class' in class_info:
            continue
        word = word.strip()
        if not word or not re.match(r'^[AaBb]+$', word):
            continue
        clean_class = re.sub(r'<[^>]+>', '', class_info).replace('&nbsp;', ' ').strip()
        mass_match = re.search(r'\(([\d.]+)\)', clean_class)
        m3 = float(mass_match.group(1)) if mass_match else None
        class_type_match = re.match(r'([IVX]+\.[A-Z])', clean_class)
        class_type = class_type_match.group(1) if class_type_match else clean_class.split()[0]
        num_match = re.search(r'(\d+)', clean_class)
        orbit_num = int(num_match.group(1)) if num_match else 0
        results.append({
            'class': class_type, 'number': orbit_num, 'm3': m3,
            'word': word, 'word_len': len(word), 'raw_class': clean_class
        })
    return results

def parse_equal_mass_words(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
    rows = re.findall(r'<tr>\s*<th>(.*?)</th>\s*<td>(.*?)</td>\s*</tr>', html, re.DOTALL)
    results = []
    for class_info, word in rows:
        if 'Free group' in word or 'Class' in class_info:
            continue
        word = word.strip()
        if not word or not re.match(r'^[AaBb]+$', word):
            continue
        clean_class = re.sub(r'<[^>]+>', '', class_info).replace('&nbsp;', ' ').strip()
        class_type_match = re.match(r'([IVX]+\.[A-Z])', clean_class)
        class_type = class_type_match.group(1) if class_type_match else clean_class.split()[0]
        num_match = re.search(r'(\d+)', clean_class)
        orbit_num = int(num_match.group(1)) if num_match else 0
        results.append({
            'class': class_type, 'number': orbit_num, 'm3': 1.0,
            'word': word, 'word_len': len(word), 'raw_class': clean_class
        })
    return results


def compute_cf_properties(orbits):
    """Compute CF properties for all orbits."""
    for o in orbits:
        word = o['word']
        M = word_to_gamma2_matrix(word)
        o['trace'] = abs(int(M[0,0] + M[1,1]))
        cf = matrix_to_cf(M)
        o['cf'] = cf
        o['cf_period'] = len(cf)
        o['nobility'] = cf_to_nobility(cf)
        o['gmean'] = cf_gmean(cf)
        o['entropy'] = braid_entropy_estimate(word)
        # Check identity
        o['is_identity'] = np.array_equal(M, np.eye(2, dtype=np.int64)) or \
                           np.array_equal(M, -np.eye(2, dtype=np.int64))
        # Orbit type key (class + number)
        o['orbit_type'] = f"{o['class']}-{o['number']}"
    return orbits


# ============================================================
# PART 2: Periodic table bins
# ============================================================

ROW_BINS = [
    (1, 1, "1"), (2, 5, "2-5"), (6, 15, "6-15"), (16, 30, "16-30"),
    (31, 50, "31-50"), (51, 80, "51-80"), (81, 120, "81-120"),
    (121, 180, "121-180"), (181, 300, "181-300")
]

COL_BINS = [
    (1.0, 1.05, "1.00-1.05"), (1.05, 1.1, "1.05-1.10"),
    (1.1, 1.15, "1.10-1.15"), (1.15, 1.2, "1.15-1.20"),
    (1.2, 1.25, "1.20-1.25"), (1.25, 1.3, "1.25-1.30"),
    (1.3, 1.35, "1.30-1.35"), (1.35, 1.45, "1.35-1.45")
]

def get_cell(cf_period, gmean):
    row_label = None
    for lo, hi, label in ROW_BINS:
        if lo <= cf_period <= hi:
            row_label = label
            break
    if row_label is None:
        if cf_period > 300:
            row_label = "181-300"  # overflow
        else:
            return None

    col_label = None
    for lo, hi, label in COL_BINS:
        if lo <= gmean < hi:
            col_label = label
            break
    if col_label is None:
        if gmean >= 1.45:
            col_label = "1.35-1.45"  # overflow
        elif gmean < 1.0:
            col_label = "1.00-1.05"  # underflow
        else:
            return None

    return f"{row_label}|{col_label}"


# ============================================================
# PART 3: Main analysis
# ============================================================

def main():
    print("=" * 70)
    print("  EXTENDED PERIODIC TABLE OF THREE-BODY ORBITS")
    print("  Equal + Unequal mass analysis")
    print("=" * 70)

    # --- Parse data ---
    print("\n[1] Parsing orbit data...")
    equal_orbits = parse_equal_mass_words('/tmp/three_body_equal_words.md')
    unequal_orbits = parse_unequal_mass_words('/tmp/three_body_unequal_words.md')
    print(f"    Equal-mass: {len(equal_orbits)} orbits")
    print(f"    Unequal-mass: {len(unequal_orbits)} orbits")

    # --- Compute CF properties ---
    print("\n[2] Computing CF properties...")
    equal_orbits = compute_cf_properties(equal_orbits)
    unequal_orbits = compute_cf_properties(unequal_orbits)
    all_orbits = equal_orbits + unequal_orbits
    print(f"    Total: {len(all_orbits)} orbits with CF properties")

    # Mass breakdown
    mass_counts = Counter(o['m3'] for o in all_orbits)
    for m3 in sorted(mass_counts):
        print(f"    m3={m3}: {mass_counts[m3]} orbits")

    # --- Load existing periodic table for reference ---
    with open(f'{OUTDIR}/threebody_periodic_table.json') as f:
        orig_table = json.load(f)
    orig_cells = orig_table['cells']

    # ================================================================
    # TASK 1: Extended periodic table
    # ================================================================
    print("\n" + "=" * 70)
    print("  TASK 1: EXTENDED PERIODIC TABLE")
    print("=" * 70)

    # Build cell assignments for all orbits
    eq_cells = defaultdict(list)
    uneq_cells = defaultdict(list)
    uneq_cells_by_mass = defaultdict(lambda: defaultdict(list))

    for o in equal_orbits:
        cell = get_cell(o['cf_period'], o['gmean'])
        if cell:
            eq_cells[cell].append(o)

    for o in unequal_orbits:
        cell = get_cell(o['cf_period'], o['gmean'])
        if cell:
            uneq_cells[cell].append(o)
            uneq_cells_by_mass[o['m3']][cell].append(o)

    # All possible cells
    all_cell_keys = set()
    for rb in ROW_BINS:
        for cb in COL_BINS:
            all_cell_keys.add(f"{rb[2]}|{cb[2]}")

    # Identify newly filled cells
    empty_in_equal = [k for k in all_cell_keys if len(eq_cells.get(k, [])) == 0]
    newly_filled = [k for k in empty_in_equal if len(uneq_cells.get(k, [])) > 0]

    print(f"\nEqual-mass filled cells: {sum(1 for k in all_cell_keys if len(eq_cells.get(k,[])) > 0)}")
    print(f"Empty in equal-mass: {len(empty_in_equal)}")
    print(f"Newly filled by unequal-mass: {len(newly_filled)}")

    if newly_filled:
        print("\nNewly filled cells:")
        for cell in sorted(newly_filled):
            orbs = uneq_cells[cell]
            masses = sorted(set(o['m3'] for o in orbs))
            nobs = [o['nobility'] for o in orbs]
            print(f"  {cell:25s}: {len(orbs)} orbits, masses={masses}, "
                  f"avg_nob={np.mean(nobs):.3f}")

    # Print extended table
    print("\nEXTENDED PERIODIC TABLE (count: equal + unequal):")
    row_labels = [rb[2] for rb in ROW_BINS]
    col_labels = [cb[2] for cb in COL_BINS]

    header = f"{'CF Period':>12}"
    for cl in col_labels:
        header += f" {cl:>12}"
    print(header)
    print("-" * len(header))

    for rl in row_labels:
        row_str = f"{rl:>12}"
        for cl in col_labels:
            key = f"{rl}|{cl}"
            eq_n = len(eq_cells.get(key, []))
            uneq_n = len(uneq_cells.get(key, []))
            if eq_n == 0 and uneq_n == 0:
                row_str += f" {'---':>12}"
            elif eq_n > 0 and uneq_n > 0:
                row_str += f" {f'{eq_n}+{uneq_n}':>12}"
            elif eq_n > 0:
                row_str += f" {f'{eq_n}eq':>12}"
            else:
                row_str += f" {f'{uneq_n}NEW':>12}"
        print(row_str)

    # ================================================================
    # TASK 2: m3=4 correlation reversal investigation
    # ================================================================
    print("\n" + "=" * 70)
    print("  TASK 2: m3=4 CORRELATION REVERSAL INVESTIGATION")
    print("=" * 70)

    mass_values = sorted(set(o['m3'] for o in all_orbits))
    corr_results = {}

    print(f"\nNobility-Entropy correlation by mass ratio:")
    print(f"{'m3':>6} {'N':>6} {'rho':>8} {'p-value':>12} {'mean_nob':>10} {'mean_ent':>10}")
    print("-" * 60)

    for m3 in mass_values:
        orbs = [o for o in all_orbits if o['m3'] == m3 and o['entropy'] > 0]
        if len(orbs) < 10:
            nobs = [o['nobility'] for o in orbs]
            ents = [o['entropy'] for o in orbs]
            print(f"{m3:6.2f} {len(orbs):6d} {'(too few)':>8} {'---':>12} "
                  f"{np.mean(nobs):.4f} {np.mean(ents):.4f}" if orbs else f"{m3:6.2f} {len(orbs):6d} (too few)")
            corr_results[m3] = {'n': len(orbs), 'rho': None, 'p': None}
            continue
        nobs = np.array([o['nobility'] for o in orbs])
        ents = np.array([o['entropy'] for o in orbs])
        rho, p = stats.spearmanr(nobs, ents)
        corr_results[m3] = {'n': len(orbs), 'rho': rho, 'p': p,
                            'mean_nob': float(np.mean(nobs)),
                            'mean_ent': float(np.mean(ents))}
        print(f"{m3:6.2f} {len(orbs):6d} {rho:8.4f} {p:12.2e} "
              f"{np.mean(nobs):10.4f} {np.mean(ents):10.4f}")

    # Investigate the reversal in detail
    print("\n--- Detailed m3=4 investigation ---")

    # Per-family breakdown at each mass
    print(f"\nPer-family nobility-entropy correlation at each mass:")
    print(f"{'m3':>6} {'Family':>8} {'N':>5} {'rho':>8} {'p':>10}")
    print("-" * 45)

    family_mass_corrs = defaultdict(dict)
    for m3 in mass_values:
        families_at_mass = defaultdict(list)
        for o in all_orbits:
            if o['m3'] == m3 and o['entropy'] > 0:
                families_at_mass[o['class']].append(o)
        for fam in sorted(families_at_mass.keys()):
            orbs = families_at_mass[fam]
            if len(orbs) < 5:
                continue
            nobs = [o['nobility'] for o in orbs]
            ents = [o['entropy'] for o in orbs]
            rho, p = stats.spearmanr(nobs, ents)
            family_mass_corrs[fam][m3] = rho
            print(f"{m3:6.2f} {fam:>8} {len(orbs):5d} {rho:8.4f} {p:10.2e}")

    # Check: is the reversal gradual or sudden?
    print("\n--- Reversal pattern analysis ---")
    print("Tracking correlation sign across mass ratios:")
    for m3 in mass_values:
        r = corr_results.get(m3, {})
        rho = r.get('rho')
        if rho is not None:
            sign = "+" if rho > 0 else "-"
            bar = "#" * int(abs(rho) * 40)
            direction = "POSITIVE" if rho > 0 else "NEGATIVE"
            print(f"  m3={m3:5.2f}: rho={rho:+.4f} [{sign}{bar:40s}] {direction}")

    # Word length and CF period distributions at m3=4
    print("\n--- Property distributions at high mass ratios ---")
    for m3 in [1.0, 2.0, 4.0, 5.0]:
        orbs = [o for o in all_orbits if o['m3'] == m3]
        if not orbs:
            continue
        wlens = [o['word_len'] for o in orbs]
        periods = [o['cf_period'] for o in orbs]
        nobs = [o['nobility'] for o in orbs]
        ents = [o['entropy'] for o in orbs if o['entropy'] > 0]
        print(f"\n  m3={m3}:  N={len(orbs)}")
        print(f"    word_len: mean={np.mean(wlens):.1f}, std={np.std(wlens):.1f}")
        print(f"    cf_period: mean={np.mean(periods):.1f}, std={np.std(periods):.1f}")
        print(f"    nobility: mean={np.mean(nobs):.4f}, std={np.std(nobs):.4f}")
        if ents:
            print(f"    entropy: mean={np.mean(ents):.4f}, std={np.std(ents):.4f}")

    # ================================================================
    # TASK 3: Empty cell filling and orbit predictions
    # ================================================================
    print("\n" + "=" * 70)
    print("  TASK 3: EMPTY CELL ANALYSIS AND ORBIT PREDICTIONS")
    print("=" * 70)

    print(f"\nAll 21 originally empty cells in equal-mass table:")
    print(f"{'Cell':>30} {'EQ':>4} {'UEQ':>5} {'Status':>12} {'Masses':>20}")
    print("-" * 80)

    predictions = []
    for cell in sorted(empty_in_equal):
        eq_n = len(eq_cells.get(cell, []))
        uneq_n = len(uneq_cells.get(cell, []))
        if uneq_n > 0:
            masses = sorted(set(o['m3'] for o in uneq_cells[cell]))
            status = "FILLED"
            # This is a prediction: these orbits exist at specific mass ratios
            for o in uneq_cells[cell]:
                predictions.append({
                    'cell': cell,
                    'orbit_type': o['orbit_type'],
                    'm3': o['m3'],
                    'nobility': o['nobility'],
                    'cf_period': o['cf_period'],
                    'gmean': o['gmean'],
                    'word': o['word'][:30]
                })
        else:
            masses = []
            status = "EMPTY"
        print(f"{cell:>30} {eq_n:>4} {uneq_n:>5} {status:>12} {str(masses):>20}")

    if predictions:
        print(f"\nORBIT PREDICTIONS from newly filled cells:")
        print(f"{'Cell':>25} {'Type':>10} {'m3':>5} {'Nob':>6} {'Period':>7} {'Gmean':>7}")
        print("-" * 70)
        for p in predictions[:30]:
            print(f"{p['cell']:>25} {p['orbit_type']:>10} {p['m3']:5.2f} "
                  f"{p['nobility']:6.3f} {p['cf_period']:7d} {p['gmean']:7.3f}")

    # What CF properties would fill remaining empty cells?
    print("\nPREDICTED PROPERTIES for still-empty cells:")
    still_empty = [k for k in empty_in_equal if len(uneq_cells.get(k, [])) == 0]
    for cell in sorted(still_empty):
        parts = cell.split('|')
        row_label = parts[0]
        col_label = parts[1]
        # Find the row/col bin ranges
        for lo, hi, label in ROW_BINS:
            if label == row_label:
                per_lo, per_hi = lo, hi
                break
        for lo, hi, label in COL_BINS:
            if label == col_label:
                gm_lo, gm_hi = lo, hi
                break
        mid_per = (per_lo + per_hi) / 2
        mid_gm = (gm_lo + gm_hi) / 2
        # Estimate nobility from gmean (using the known inverse relationship)
        est_nob = max(0, min(1, 1.0 - 2.5 * (mid_gm - 1.0)))
        print(f"  {cell:>30}: need CF period ~{mid_per:.0f}, gmean ~{mid_gm:.3f}, "
              f"est. nobility ~{est_nob:.2f}")

    # ================================================================
    # TASK 4: Mass-ratio scaling for shared orbit types
    # ================================================================
    print("\n" + "=" * 70)
    print("  TASK 4: MASS-RATIO SCALING FOR SHARED ORBIT TYPES")
    print("=" * 70)

    # Group by orbit type across masses
    orbit_type_mass = defaultdict(list)
    for o in all_orbits:
        orbit_type_mass[o['orbit_type']].append(o)

    # Find orbit types present at multiple masses
    shared_types = {k: v for k, v in orbit_type_mass.items()
                    if len(set(o['m3'] for o in v)) >= 3}

    print(f"\nOrbit types present at 3+ mass ratios: {len(shared_types)}")

    # Analyze scaling
    scaling_results = []
    print(f"\n{'Type':>12} {'N_masses':>8} {'Masses':>30} {'Nob_slope':>10} {'Ent_slope':>10} {'Per_slope':>10}")
    print("-" * 90)

    for otype in sorted(shared_types.keys()):
        orbs = shared_types[otype]
        mass_vals = sorted(set(o['m3'] for o in orbs))
        n_masses = len(mass_vals)

        # Get mean properties at each mass
        mass_nob = []
        mass_ent = []
        mass_per = []
        mass_list = []
        for m3 in mass_vals:
            morbs = [o for o in orbs if o['m3'] == m3]
            mass_list.append(m3)
            mass_nob.append(np.mean([o['nobility'] for o in morbs]))
            mass_ent.append(np.mean([o['entropy'] for o in morbs]))
            mass_per.append(np.mean([o['cf_period'] for o in morbs]))

        # Fit linear trend
        if len(mass_list) >= 3:
            nob_slope = stats.linregress(mass_list, mass_nob).slope
            ent_slope = stats.linregress(mass_list, mass_ent).slope
            per_slope = stats.linregress(mass_list, mass_per).slope
        else:
            nob_slope = ent_slope = per_slope = float('nan')

        scaling_results.append({
            'type': otype,
            'n_masses': n_masses,
            'masses': mass_vals,
            'nob_slope': nob_slope,
            'ent_slope': ent_slope,
            'per_slope': per_slope,
            'mass_nob': list(zip(mass_list, mass_nob)),
            'mass_ent': list(zip(mass_list, mass_ent)),
            'mass_per': list(zip(mass_list, mass_per))
        })

        if n_masses >= 3:
            print(f"{otype:>12} {n_masses:>8} {str(mass_vals):>30} "
                  f"{nob_slope:>10.4f} {ent_slope:>10.6f} {per_slope:>10.2f}")

    # Universal scaling law check
    print("\n--- Universal scaling law analysis ---")
    nob_slopes = [r['nob_slope'] for r in scaling_results if not np.isnan(r['nob_slope'])]
    ent_slopes = [r['ent_slope'] for r in scaling_results if not np.isnan(r['ent_slope'])]
    per_slopes = [r['per_slope'] for r in scaling_results if not np.isnan(r['per_slope'])]

    if nob_slopes:
        print(f"Nobility slope distribution: mean={np.mean(nob_slopes):.4f}, "
              f"std={np.std(nob_slopes):.4f}, median={np.median(nob_slopes):.4f}")
        pos_nob = sum(1 for s in nob_slopes if s > 0)
        neg_nob = sum(1 for s in nob_slopes if s < 0)
        print(f"  Positive slopes: {pos_nob}, Negative slopes: {neg_nob}")

    if ent_slopes:
        print(f"Entropy slope distribution: mean={np.mean(ent_slopes):.6f}, "
              f"std={np.std(ent_slopes):.6f}, median={np.median(ent_slopes):.6f}")

    if per_slopes:
        print(f"Period slope distribution: mean={np.mean(per_slopes):.2f}, "
              f"std={np.std(per_slopes):.2f}, median={np.median(per_slopes):.2f}")

    # ================================================================
    # VISUALIZATIONS
    # ================================================================
    print("\n" + "=" * 70)
    print("  GENERATING VISUALIZATIONS")
    print("=" * 70)

    # --- Figure 1: Extended periodic table heatmap ---
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    row_labels = [rb[2] for rb in ROW_BINS]
    col_labels = [cb[2] for cb in COL_BINS]

    # Equal-mass table
    eq_grid = np.zeros((len(row_labels), len(col_labels)))
    for i, rl in enumerate(row_labels):
        for j, cl in enumerate(col_labels):
            key = f"{rl}|{cl}"
            eq_grid[i, j] = len(eq_cells.get(key, []))

    im1 = axes[0].imshow(eq_grid, cmap='YlOrRd', aspect='auto', interpolation='nearest')
    axes[0].set_xticks(range(len(col_labels)))
    axes[0].set_xticklabels(col_labels, rotation=45, ha='right', fontsize=8)
    axes[0].set_yticks(range(len(row_labels)))
    axes[0].set_yticklabels(row_labels, fontsize=8)
    axes[0].set_xlabel('CF Geometric Mean')
    axes[0].set_ylabel('CF Period Length')
    axes[0].set_title(f'Equal-Mass Table (N={len(equal_orbits)})')
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            v = int(eq_grid[i, j])
            if v > 0:
                axes[0].text(j, i, str(v), ha='center', va='center', fontsize=7,
                           color='white' if v > 20 else 'black')
    plt.colorbar(im1, ax=axes[0], label='Count')

    # Extended table (equal + unequal)
    ext_grid = np.zeros((len(row_labels), len(col_labels)))
    new_grid = np.zeros((len(row_labels), len(col_labels)))
    for i, rl in enumerate(row_labels):
        for j, cl in enumerate(col_labels):
            key = f"{rl}|{cl}"
            eq_n = len(eq_cells.get(key, []))
            uneq_n = len(uneq_cells.get(key, []))
            ext_grid[i, j] = eq_n + uneq_n
            if eq_n == 0 and uneq_n > 0:
                new_grid[i, j] = 1  # Mark newly filled

    im2 = axes[1].imshow(ext_grid, cmap='YlOrRd', aspect='auto', interpolation='nearest')
    axes[1].set_xticks(range(len(col_labels)))
    axes[1].set_xticklabels(col_labels, rotation=45, ha='right', fontsize=8)
    axes[1].set_yticks(range(len(row_labels)))
    axes[1].set_yticklabels(row_labels, fontsize=8)
    axes[1].set_xlabel('CF Geometric Mean')
    axes[1].set_ylabel('CF Period Length')
    axes[1].set_title(f'Extended Table (N={len(all_orbits)})')
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            v = int(ext_grid[i, j])
            if v > 0:
                color = 'white' if v > 20 else 'black'
                label = str(v)
                if new_grid[i, j] > 0:
                    label = f"*{v}"
                    color = 'lime'
                axes[1].text(j, i, label, ha='center', va='center', fontsize=7,
                           color=color, fontweight='bold' if new_grid[i,j] > 0 else 'normal')
    plt.colorbar(im2, ax=axes[1], label='Count')

    plt.suptitle('Three-Body Orbit Periodic Table: Equal vs Extended', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{OUTDIR}/threebody_extended_table_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: threebody_extended_table_heatmap.png")

    # --- Figure 2: m3=4 correlation reversal ---
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))

    plot_masses = [0.5, 0.75, 1.0, 2.0, 4.0, 5.0, 8.0, 10.0]
    for idx, m3 in enumerate(plot_masses):
        ax = axes[idx // 4][idx % 4]
        orbs = [o for o in all_orbits if o['m3'] == m3 and o['entropy'] > 0]
        if not orbs:
            ax.text(0.5, 0.5, f'm3={m3}\nNo data', ha='center', va='center',
                   transform=ax.transAxes)
            ax.set_title(f'm3={m3}')
            continue

        nobs = [o['nobility'] for o in orbs]
        ents = [o['entropy'] for o in orbs]

        # Color by family
        families = list(set(o['class'] for o in orbs))
        colors = plt.cm.tab10(np.linspace(0, 1, max(len(families), 1)))
        fam_color = {f: colors[i] for i, f in enumerate(families)}

        for o in orbs:
            ax.scatter(o['nobility'], o['entropy'], c=[fam_color[o['class']]],
                      s=15, alpha=0.6)

        # Compute and show correlation
        if len(orbs) >= 10:
            rho, p = stats.spearmanr(nobs, ents)
            color = 'red' if rho < 0 else 'blue'
            ax.set_title(f'm3={m3} (N={len(orbs)})\nrho={rho:.3f}, p={p:.1e}',
                        fontsize=9, color=color)
            # Add trend line
            z = np.polyfit(nobs, ents, 1)
            x_line = np.linspace(min(nobs), max(nobs), 50)
            ax.plot(x_line, np.polyval(z, x_line), '--', color=color, alpha=0.7, linewidth=2)
        else:
            ax.set_title(f'm3={m3} (N={len(orbs)})', fontsize=9)

        ax.set_xlabel('Nobility', fontsize=8)
        ax.set_ylabel('Braid Entropy', fontsize=8)
        ax.tick_params(labelsize=7)

    plt.suptitle('Nobility vs Braid Entropy by Mass Ratio\n(Red title = negative correlation, Blue = positive)',
                fontsize=13)
    plt.tight_layout()
    plt.savefig(f'{OUTDIR}/threebody_m3_correlation_reversal.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: threebody_m3_correlation_reversal.png")

    # --- Figure 3: Correlation evolution with mass ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel A: Overall correlation vs m3
    valid_masses = [m3 for m3 in mass_values if corr_results[m3].get('rho') is not None]
    rhos = [corr_results[m3]['rho'] for m3 in valid_masses]
    ns = [corr_results[m3]['n'] for m3 in valid_masses]

    axes[0].bar(range(len(valid_masses)), rhos,
               color=['blue' if r > 0 else 'red' for r in rhos],
               alpha=0.7)
    axes[0].set_xticks(range(len(valid_masses)))
    axes[0].set_xticklabels([f'{m:.1f}' for m in valid_masses], rotation=45)
    axes[0].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    axes[0].set_xlabel('Mass ratio m3')
    axes[0].set_ylabel('Spearman rho (nobility vs entropy)')
    axes[0].set_title('Correlation Reversal with Mass')
    for i, (m, r, n) in enumerate(zip(valid_masses, rhos, ns)):
        axes[0].text(i, r + 0.02 * np.sign(r), f'N={n}', ha='center', fontsize=7)

    # Panel B: Per-family correlation evolution
    for fam in sorted(family_mass_corrs.keys()):
        fam_masses = sorted(family_mass_corrs[fam].keys())
        fam_rhos = [family_mass_corrs[fam][m] for m in fam_masses]
        axes[1].plot(fam_masses, fam_rhos, 'o-', label=fam, markersize=5)
    axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    axes[1].set_xlabel('Mass ratio m3')
    axes[1].set_ylabel('Spearman rho')
    axes[1].set_title('Per-Family Correlation Evolution')
    axes[1].legend(fontsize=8)

    # Panel C: Mean nobility and entropy vs mass
    mean_nobs = []
    mean_ents = []
    plot_m = []
    for m3 in mass_values:
        orbs = [o for o in all_orbits if o['m3'] == m3]
        if orbs:
            plot_m.append(m3)
            mean_nobs.append(np.mean([o['nobility'] for o in orbs]))
            mean_ents.append(np.mean([o['entropy'] for o in orbs if o['entropy'] > 0] or [0]))

    ax2 = axes[2].twinx()
    l1, = axes[2].plot(plot_m, mean_nobs, 'bo-', label='Nobility', markersize=6)
    l2, = ax2.plot(plot_m, mean_ents, 'rs-', label='Entropy', markersize=6)
    axes[2].set_xlabel('Mass ratio m3')
    axes[2].set_ylabel('Mean Nobility', color='blue')
    ax2.set_ylabel('Mean Entropy', color='red')
    axes[2].set_title('Mean Properties vs Mass Ratio')
    axes[2].legend(handles=[l1, l2], loc='center right', fontsize=8)

    plt.suptitle('m3=4 Anomaly Investigation', fontsize=13)
    plt.tight_layout()
    plt.savefig(f'{OUTDIR}/threebody_m3_anomaly_investigation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: threebody_m3_anomaly_investigation.png")

    # --- Figure 4: Mass-ratio scaling for shared types ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Select top shared orbit types for visualization
    top_shared = sorted(scaling_results, key=lambda r: r['n_masses'], reverse=True)[:15]

    for sr in top_shared:
        if not sr['mass_nob']:
            continue
        m_vals = [x[0] for x in sr['mass_nob']]
        nob_vals = [x[1] for x in sr['mass_nob']]
        ent_vals = [x[1] for x in sr['mass_ent']]
        per_vals = [x[1] for x in sr['mass_per']]

        axes[0].plot(m_vals, nob_vals, 'o-', label=sr['type'], markersize=4, alpha=0.7)
        axes[1].plot(m_vals, ent_vals, 'o-', label=sr['type'], markersize=4, alpha=0.7)
        axes[2].plot(m_vals, per_vals, 'o-', label=sr['type'], markersize=4, alpha=0.7)

    axes[0].set_xlabel('Mass ratio m3')
    axes[0].set_ylabel('Nobility')
    axes[0].set_title('Nobility vs Mass')
    axes[0].legend(fontsize=6, ncol=2)

    axes[1].set_xlabel('Mass ratio m3')
    axes[1].set_ylabel('Braid Entropy')
    axes[1].set_title('Entropy vs Mass')

    axes[2].set_xlabel('Mass ratio m3')
    axes[2].set_ylabel('CF Period')
    axes[2].set_title('CF Period vs Mass')

    plt.suptitle('Mass-Ratio Scaling for Shared Orbit Types', fontsize=13)
    plt.tight_layout()
    plt.savefig(f'{OUTDIR}/threebody_mass_ratio_scaling.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: threebody_mass_ratio_scaling.png")

    # --- Figure 5: 3D periodic table (mass as third dimension) ---
    fig = plt.figure(figsize=(16, 10))

    # One subplot per mass ratio
    mass_list_plot = [0.5, 0.75, 1.0, 2.0, 4.0]
    for idx, m3 in enumerate(mass_list_plot):
        ax = fig.add_subplot(2, 3, idx + 1)
        grid = np.zeros((len(row_labels), len(col_labels)))
        orbs = [o for o in all_orbits if o['m3'] == m3]
        for o in orbs:
            cell = get_cell(o['cf_period'], o['gmean'])
            if cell:
                parts = cell.split('|')
                ri = row_labels.index(parts[0])
                ci = col_labels.index(parts[1])
                grid[ri, ci] += 1

        im = ax.imshow(grid, cmap='YlOrRd', aspect='auto', interpolation='nearest')
        ax.set_xticks(range(len(col_labels)))
        ax.set_xticklabels(col_labels, rotation=45, ha='right', fontsize=6)
        ax.set_yticks(range(len(row_labels)))
        ax.set_yticklabels(row_labels, fontsize=6)
        ax.set_title(f'm3={m3} (N={len(orbs)})', fontsize=10)
        for i in range(len(row_labels)):
            for j in range(len(col_labels)):
                v = int(grid[i, j])
                if v > 0:
                    ax.text(j, i, str(v), ha='center', va='center', fontsize=6,
                           color='white' if v > 15 else 'black')
        plt.colorbar(im, ax=ax, shrink=0.8)

    # Summary panel
    ax = fig.add_subplot(2, 3, 6)
    # Show which cells each mass fills
    mass_fill_counts = []
    for m3 in mass_values:
        cells_filled = set()
        for o in all_orbits:
            if o['m3'] == m3:
                cell = get_cell(o['cf_period'], o['gmean'])
                if cell:
                    cells_filled.add(cell)
        mass_fill_counts.append((m3, len(cells_filled)))

    m_vals = [x[0] for x in mass_fill_counts]
    c_vals = [x[1] for x in mass_fill_counts]
    ax.bar(range(len(m_vals)), c_vals, color='steelblue')
    ax.set_xticks(range(len(m_vals)))
    ax.set_xticklabels([f'{m:.1f}' for m in m_vals], rotation=45)
    ax.set_xlabel('Mass ratio m3')
    ax.set_ylabel('Distinct cells filled')
    ax.set_title('Cell Coverage by Mass')

    plt.suptitle('3D Periodic Table: Mass Ratio as Third Dimension', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{OUTDIR}/threebody_3d_periodic_table.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: threebody_3d_periodic_table.png")

    # ================================================================
    # SAVE RESULTS
    # ================================================================
    print("\n" + "=" * 70)
    print("  SAVING RESULTS")
    print("=" * 70)

    results = {
        'metadata': {
            'title': 'Extended Periodic Table of Three-Body Orbits',
            'n_equal': len(equal_orbits),
            'n_unequal': len(unequal_orbits),
            'n_total': len(all_orbits),
            'mass_values': sorted(mass_counts.keys()),
        },
        'extended_table': {},
        'newly_filled_cells': [],
        'still_empty_cells': [],
        'correlation_reversal': corr_results,
        'scaling_results': [],
        'predictions': predictions[:50],
    }

    # Extended table data
    for key in all_cell_keys:
        eq_n = len(eq_cells.get(key, []))
        uneq_n = len(uneq_cells.get(key, []))
        total = eq_n + uneq_n
        avg_nob = np.mean([o['nobility'] for o in eq_cells.get(key, []) + uneq_cells.get(key, [])]) if total > 0 else None
        results['extended_table'][key] = {
            'equal_count': eq_n,
            'unequal_count': uneq_n,
            'total': total,
            'avg_nobility': float(avg_nob) if avg_nob is not None else None,
        }

    for cell in newly_filled:
        orbs = uneq_cells[cell]
        results['newly_filled_cells'].append({
            'cell': cell,
            'count': len(orbs),
            'masses': sorted(set(o['m3'] for o in orbs)),
            'avg_nobility': float(np.mean([o['nobility'] for o in orbs])),
        })

    results['still_empty_cells'] = sorted(still_empty)

    # Convert corr_results for JSON serialization
    for m3 in results['correlation_reversal']:
        r = results['correlation_reversal'][m3]
        for k, v in r.items():
            if isinstance(v, (np.floating, np.integer)):
                r[k] = float(v)

    # Scaling results (top 30)
    for sr in scaling_results[:30]:
        results['scaling_results'].append({
            'type': sr['type'],
            'n_masses': sr['n_masses'],
            'nob_slope': float(sr['nob_slope']) if not np.isnan(sr['nob_slope']) else None,
            'ent_slope': float(sr['ent_slope']) if not np.isnan(sr['ent_slope']) else None,
            'per_slope': float(sr['per_slope']) if not np.isnan(sr['per_slope']) else None,
        })

    with open(f'{OUTDIR}/threebody_extended_table_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print("  Saved: threebody_extended_table_results.json")

    # ================================================================
    # SUMMARY
    # ================================================================
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"\n  Total orbits analyzed: {len(all_orbits)}")
    print(f"  Equal-mass: {len(equal_orbits)}, Unequal-mass: {len(unequal_orbits)}")
    print(f"  Mass ratios: {sorted(mass_counts.keys())}")
    print(f"\n  Periodic table: 9x8 = 72 cells")
    print(f"  Equal-mass filled: {sum(1 for k in all_cell_keys if len(eq_cells.get(k,[])) > 0)}")
    print(f"  Newly filled by unequal: {len(newly_filled)}")
    print(f"  Still empty: {len(still_empty)}")
    print(f"\n  Correlation reversal:")
    for m3 in valid_masses:
        r = corr_results[m3]
        rho = r.get('rho')
        if rho is not None:
            sign = "POSITIVE" if rho > 0 else "NEGATIVE"
            print(f"    m3={m3}: rho={rho:+.4f} ({sign})")
    print(f"\n  Shared orbit types (3+ masses): {len(shared_types)}")
    if nob_slopes:
        print(f"  Nobility scaling: {sum(1 for s in nob_slopes if s > 0)} positive, "
              f"{sum(1 for s in nob_slopes if s < 0)} negative slopes")
    print(f"\n  Orbit predictions: {len(predictions)} from newly filled cells")

    return results


if __name__ == '__main__':
    results = main()
