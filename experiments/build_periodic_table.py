#!/usr/bin/env python3
"""
Build a "Periodic Table" of Three-Body Orbits organized by Continued Fraction structure.

Rows = CF period length (binned)
Columns = geometric mean of CF partial quotients (binned)
Cells = orbit counts, avg nobility, representative orbit, etc.
"""

import json
import math
import numpy as np
from collections import defaultdict, Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

# =============================================================================
# Load data
# =============================================================================
with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_exact_data.json') as f:
    data = json.load(f)

all_results = data['results']
orbits = [r for r in all_results if not r.get('period_not_found', False)]
n_total = len(all_results)
n_with_period = len(orbits)

print(f"Total orbits: {n_total}, with CF period: {n_with_period}")

# =============================================================================
# Define binning
# =============================================================================
# Rows: CF period length bins
ROW_BINS = [
    (1, 1, "1"),
    (2, 5, "2-5"),
    (6, 15, "6-15"),
    (16, 30, "16-30"),
    (31, 50, "31-50"),
    (51, 80, "51-80"),
    (81, 120, "81-120"),
    (121, 180, "121-180"),
    (181, 300, "181-300"),
]

# Columns: geometric mean bins
COL_BINS = [
    (1.000, 1.050, "1.00-1.05"),
    (1.050, 1.100, "1.05-1.10"),
    (1.100, 1.150, "1.10-1.15"),
    (1.150, 1.200, "1.15-1.20"),
    (1.200, 1.250, "1.20-1.25"),
    (1.250, 1.300, "1.25-1.30"),
    (1.300, 1.350, "1.30-1.35"),
    (1.350, 1.450, "1.35-1.45"),
]

def get_row_bin(period_length):
    for lo, hi, label in ROW_BINS:
        if lo <= period_length <= hi:
            return label
    return None

def get_col_bin(gmean):
    for lo, hi, label in COL_BINS:
        if lo <= gmean < hi:
            return label
    # Handle edge case gmean == 1.45
    if gmean >= 1.45:
        return COL_BINS[-1][2]
    return None

# =============================================================================
# Assign orbits to cells
# =============================================================================
table = defaultdict(list)  # (row_label, col_label) -> list of orbits

for r in orbits:
    row = get_row_bin(r['cf_period_length'])
    col = get_col_bin(r['cf_period_gmean'])
    if row and col:
        table[(row, col)].append(r)
    else:
        print(f"  Unassigned: {r['id']} period_len={r['cf_period_length']} gmean={r['cf_period_gmean']:.4f}")

row_labels = [b[2] for b in ROW_BINS]
col_labels = [b[2] for b in COL_BINS]

# =============================================================================
# Compute cell statistics
# =============================================================================
cells = {}
for ri, rl in enumerate(row_labels):
    for ci, cl in enumerate(col_labels):
        orbs = table.get((rl, cl), [])
        n = len(orbs)
        if n == 0:
            cells[(rl, cl)] = {
                "count": 0,
                "avg_nobility": None,
                "avg_Tstar": None,
                "avg_gmean": None,
                "avg_period_length": None,
                "representative": None,
                "representative_word": None,
                "families": {},
                "noble_gas": None,
            }
        else:
            nobilities = [o['nobility'] for o in orbs]
            tstars = [o['Tstar'] for o in orbs if o['Tstar'] is not None]
            families = Counter(o['family'] for o in orbs)
            # Representative: shortest word
            rep = min(orbs, key=lambda o: o['word_length'])
            # Noble gas: highest nobility in this cell
            noble_gas = max(orbs, key=lambda o: o['nobility'])

            cells[(rl, cl)] = {
                "count": n,
                "avg_nobility": float(np.mean(nobilities)),
                "std_nobility": float(np.std(nobilities)),
                "min_nobility": float(min(nobilities)),
                "max_nobility": float(max(nobilities)),
                "avg_Tstar": float(np.mean(tstars)) if tstars else None,
                "avg_gmean": float(np.mean([o['cf_period_gmean'] for o in orbs])),
                "avg_period_length": float(np.mean([o['cf_period_length'] for o in orbs])),
                "representative": rep['id'],
                "representative_word": rep['word'][:40] + ("..." if len(rep['word']) > 40 else ""),
                "representative_word_length": rep['word_length'],
                "families": dict(families),
                "noble_gas": {
                    "id": noble_gas['id'],
                    "nobility": noble_gas['nobility'],
                    "word": noble_gas['word'][:40] + ("..." if len(noble_gas['word']) > 40 else ""),
                    "cf_period": noble_gas['cf_period'][:10],
                    "cf_period_length": noble_gas['cf_period_length'],
                },
            }

# =============================================================================
# Special elements
# =============================================================================
# "Hydrogen" = figure-eight
hydrogen = next(r for r in orbits if r['id'] == 'I.A-1')
# "Helium" = next simplest
simplest = sorted(orbits, key=lambda r: (r['word_length'], r['cf_period_gmean']))
helium = simplest[1]  # second simplest
# "Lithium" = third
lithium = simplest[2]

special_elements = {
    "H": {"analogy": "Hydrogen", "orbit": hydrogen['id'], "word": hydrogen['word'],
           "cf_period": hydrogen['cf_period'], "nobility": hydrogen['nobility'],
           "reason": "Simplest orbit, pure golden ratio CF [0; 1,1,1,...], maximum nobility=1.0"},
    "He": {"analogy": "Helium", "orbit": helium['id'], "word": helium['word'][:30],
            "cf_period": helium['cf_period'], "nobility": helium['nobility'],
            "reason": "Second simplest, word_length=8"},
    "Li": {"analogy": "Lithium", "orbit": lithium['id'], "word": lithium['word'][:30],
            "cf_period": lithium['cf_period'], "nobility": lithium['nobility'],
            "reason": "Third simplest, word_length=8"},
}

# Noble gases per row (highest nobility in each period-length row)
noble_gases = {}
for rl in row_labels:
    row_orbits = []
    for cl in col_labels:
        row_orbits.extend(table.get((rl, cl), []))
    if row_orbits:
        ng = max(row_orbits, key=lambda o: o['nobility'])
        noble_gases[rl] = {
            "id": ng['id'],
            "nobility": ng['nobility'],
            "cf_period": ng['cf_period'][:10],
            "cf_period_length": ng['cf_period_length'],
            "gmean": ng['cf_period_gmean'],
            "word_length": ng['word_length'],
        }

# =============================================================================
# Statistics
# =============================================================================
total_in_table = sum(c['count'] for c in cells.values())
print(f"\nOrbits in table: {total_in_table}/{n_with_period}")

# Row statistics
row_stats = {}
for rl in row_labels:
    count = sum(cells[(rl, cl)]['count'] for cl in col_labels)
    row_stats[rl] = {"count": count, "fraction": count / n_with_period}

# Column statistics
col_stats = {}
for cl in col_labels:
    count = sum(cells[(rl, cl)]['count'] for rl in row_labels)
    col_stats[cl] = {"count": count, "fraction": count / n_with_period}

# Empty cells (potential "undiscovered" orbit types)
empty_cells = []
for rl in row_labels:
    for cl in col_labels:
        if cells[(rl, cl)]['count'] == 0:
            empty_cells.append({"row": rl, "col": cl})

# Cross-reference with Li-Liao families
family_by_cell = defaultdict(lambda: Counter())
for r in orbits:
    row = get_row_bin(r['cf_period_length'])
    col = get_col_bin(r['cf_period_gmean'])
    if row and col:
        family_by_cell[(row, col)][r['family']] += 1

# Family mixing analysis: do Li-Liao families map cleanly to CF cells?
family_purity = {}
for key, fam_counts in family_by_cell.items():
    total = sum(fam_counts.values())
    dominant = max(fam_counts.values())
    family_purity[key] = dominant / total

avg_purity = np.mean(list(family_purity.values()))
print(f"\nFamily purity (1.0 = Li-Liao family perfectly predicts CF cell): avg = {avg_purity:.3f}")

# Are there cells with mixed families?
mixed_cells = [(k, v) for k, v in family_by_cell.items() if len(v) > 1]
print(f"Cells with mixed families: {len(mixed_cells)} / {len(family_by_cell)}")

# =============================================================================
# Fibonacci structure detection
# =============================================================================
fib_set = {1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144}
fib_orbits = []
for r in orbits:
    period = r['cf_period']
    if all(p in fib_set for p in period) and len(period) > 1:
        fib_orbits.append(r['id'])

print(f"\nOrbits with all-Fibonacci CF partial quotients: {len(fib_orbits)}")

# =============================================================================
# Save JSON
# =============================================================================
table_json = {
    "metadata": {
        "title": "Periodic Table of Three-Body Orbits (CF-Organized)",
        "description": "691 equal-mass zero-angular-momentum three-body periodic orbits organized by continued fraction structure",
        "source": "Li-Liao catalog (695 orbits), CF analysis via exact quadratic surd method",
        "n_total": n_total,
        "n_in_table": total_in_table,
        "n_period_not_found": n_total - n_with_period,
        "row_variable": "CF period length (binned)",
        "col_variable": "Geometric mean of CF partial quotients (binned)",
        "row_bins": [{"lo": b[0], "hi": b[1], "label": b[2]} for b in ROW_BINS],
        "col_bins": [{"lo": b[0], "hi": b[1], "label": b[2]} for b in COL_BINS],
    },
    "cells": {},
    "row_stats": row_stats,
    "col_stats": col_stats,
    "empty_cells": empty_cells,
    "special_elements": special_elements,
    "noble_gases": noble_gases,
    "family_analysis": {
        "avg_purity": avg_purity,
        "n_mixed_cells": len(mixed_cells),
        "mixed_cells_detail": [
            {"cell": f"{k[0]} x {k[1]}", "families": dict(v)}
            for k, v in mixed_cells
        ],
    },
    "fibonacci_orbits": fib_orbits[:20],
}

# Serialize cells
for rl in row_labels:
    for cl in col_labels:
        key = f"{rl}|{cl}"
        table_json["cells"][key] = cells[(rl, cl)]

with open('/Users/saar/Desktop/Farey-Local/experiments/threebody_periodic_table.json', 'w') as f:
    json.dump(table_json, f, indent=2)
print("\nSaved: threebody_periodic_table.json")

# =============================================================================
# Generate matplotlib figure
# =============================================================================
fig, ax = plt.subplots(1, 1, figsize=(16, 10))

nrows = len(row_labels)
ncols = len(col_labels)

# Build data matrices
count_matrix = np.zeros((nrows, ncols))
nobility_matrix = np.full((nrows, ncols), np.nan)
tstar_matrix = np.full((nrows, ncols), np.nan)

for ri, rl in enumerate(row_labels):
    for ci, cl in enumerate(col_labels):
        c = cells[(rl, cl)]
        count_matrix[ri, ci] = c['count']
        if c['avg_nobility'] is not None:
            nobility_matrix[ri, ci] = c['avg_nobility']
        if c['avg_Tstar'] is not None:
            tstar_matrix[ri, ci] = c['avg_Tstar']

# Color by nobility (green=high/noble, red=low/less noble)
cmap = plt.cm.RdYlGn  # Red-Yellow-Green
norm = mcolors.Normalize(vmin=0.60, vmax=0.95)

# Draw cells
for ri in range(nrows):
    for ci in range(ncols):
        count = int(count_matrix[ri, ci])
        nob = nobility_matrix[ri, ci]

        if count == 0:
            # Empty cell - gray with question mark
            rect = plt.Rectangle((ci, nrows - 1 - ri), 1, 1,
                                  facecolor='#f0f0f0', edgecolor='#cccccc', linewidth=0.5)
            ax.add_patch(rect)
            ax.text(ci + 0.5, nrows - 1 - ri + 0.5, '?',
                    ha='center', va='center', fontsize=14, color='#aaaaaa', fontweight='bold')
        else:
            # Colored cell
            color = cmap(norm(nob))
            rect = plt.Rectangle((ci, nrows - 1 - ri), 1, 1,
                                  facecolor=color, edgecolor='white', linewidth=1.5)
            ax.add_patch(rect)

            # Count (large)
            size = min(20, max(8, 6 + count // 10))
            ax.text(ci + 0.5, nrows - 1 - ri + 0.65, str(count),
                    ha='center', va='center', fontsize=size, fontweight='bold',
                    color='black' if nob > 0.75 else 'white',
                    path_effects=[pe.withStroke(linewidth=1, foreground='white')])

            # Nobility (small)
            ax.text(ci + 0.5, nrows - 1 - ri + 0.35, f'n={nob:.2f}',
                    ha='center', va='center', fontsize=7,
                    color='#333333' if nob > 0.75 else '#eeeeee')

            # Representative orbit ID (tiny)
            rep = cells[(row_labels[ri], col_labels[ci])].get('representative', '')
            if rep:
                ax.text(ci + 0.5, nrows - 1 - ri + 0.12, rep,
                        ha='center', va='center', fontsize=5.5,
                        color='#555555' if nob > 0.75 else '#dddddd')

# Mark special elements
# Figure-eight
h_row = 0  # period 1 -> row 0
h_col = 0  # gmean 1.0 -> col 0
rect = plt.Rectangle((h_col, nrows - 1 - h_row), 1, 1,
                      facecolor='none', edgecolor='gold', linewidth=3)
ax.add_patch(rect)
ax.text(h_col + 0.95, nrows - 1 - h_row + 0.92, 'H', ha='right', va='top',
        fontsize=8, fontweight='bold', color='goldenrod',
        path_effects=[pe.withStroke(linewidth=2, foreground='white')])

# Axes
ax.set_xlim(0, ncols)
ax.set_ylim(0, nrows)
ax.set_xticks([i + 0.5 for i in range(ncols)])
ax.set_xticklabels(col_labels, fontsize=9, rotation=30, ha='right')
ax.set_yticks([nrows - 1 - i + 0.5 for i in range(nrows)])
ax.set_yticklabels(row_labels, fontsize=9)
ax.set_xlabel('Geometric Mean of CF Partial Quotients (nobility proxy)', fontsize=12, fontweight='bold')
ax.set_ylabel('CF Period Length (algebraic complexity)', fontsize=12, fontweight='bold')
ax.set_title('Periodic Table of Three-Body Orbits\nOrganized by Continued Fraction Structure (691 orbits)',
             fontsize=14, fontweight='bold', pad=15)

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.7, pad=0.02)
cbar.set_label('Average Nobility (green=stable, red=less stable)', fontsize=10)

# Annotations
ax.text(ncols + 0.5, nrows - 0.3, 'Cell = count of orbits', fontsize=8, color='#666666',
        transform=ax.transData)
ax.text(ncols + 0.5, nrows - 0.7, 'n = avg nobility', fontsize=8, color='#666666',
        transform=ax.transData)
ax.text(ncols + 0.5, nrows - 1.1, '? = empty (predicted)', fontsize=8, color='#aaaaaa',
        transform=ax.transData)
ax.text(ncols + 0.5, nrows - 1.5, 'Gold border = "Hydrogen"', fontsize=8, color='goldenrod',
        transform=ax.transData)

plt.tight_layout()
plt.savefig('/Users/saar/Desktop/Farey-Local/experiments/threebody_periodic_table.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("Saved: threebody_periodic_table.png")

# =============================================================================
# Print summary for markdown
# =============================================================================
print("\n" + "="*80)
print("PERIODIC TABLE SUMMARY")
print("="*80)

print(f"\nTotal orbits in table: {total_in_table}")
print(f"Empty cells: {len(empty_cells)} out of {nrows * ncols}")

print(f"\n--- Row statistics (CF period length) ---")
for rl in row_labels:
    s = row_stats[rl]
    print(f"  {rl:>10s}: {s['count']:4d} orbits ({s['fraction']*100:5.1f}%)")

print(f"\n--- Column statistics (gmean) ---")
for cl in col_labels:
    s = col_stats[cl]
    print(f"  {cl:>10s}: {s['count']:4d} orbits ({s['fraction']*100:5.1f}%)")

print(f"\n--- Noble Gases (highest nobility per row) ---")
for rl in row_labels:
    if rl in noble_gases:
        ng = noble_gases[rl]
        print(f"  {rl:>10s}: {ng['id']:12s} nobility={ng['nobility']:.4f} gmean={ng['gmean']:.4f} cf_len={ng['cf_period_length']}")

print(f"\n--- Special Elements ---")
for sym, info in special_elements.items():
    print(f"  {sym} ({info['analogy']}): {info['orbit']} - {info['reason']}")

print(f"\n--- Family Analysis ---")
print(f"  Average purity: {avg_purity:.3f}")
print(f"  Mixed cells: {len(mixed_cells)}")
for k, v in sorted(mixed_cells, key=lambda x: -sum(x[1].values()))[:10]:
    print(f"    {k[0]:>10s} x {k[1]:>10s}: {dict(v)}")

print(f"\n--- Empty Cells (predicted undiscovered orbit types) ---")
for ec in empty_cells:
    print(f"  Period {ec['row']}, gmean {ec['col']}")

PYEOF
