#!/usr/bin/env python3
"""
fig_damage_response.py — Damage/Response figure for the Farey paper.

Visualizes the three-term decomposition of DeltaW = W(F_p) - W(F_{p-1}):

    DeltaW = calD + C + B'

where:
    calD = (1/n'^2) sum_{new} D_{F_p}(k/p)^2   (new-fraction damage, > 0)
    C    = (1/n'^2) sum_{old} delta(f)^2         (shift-squared, > 0)
    B'   = (2/(n*n')) sum_{old} D_{prev}*delta    (cross-term, < 0 for good primes)

Two-panel figure:
    Panel A (left):  Horizontal bar chart — damage (calD + C) vs response (|B'|)
    Panel B (right): D(1/p)^2 share of calD
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fractions import Fraction
from math import gcd
import os

plt.rcParams.update({
    "text.usetex": False,
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.size": 10,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
})

# ---------------------------------------------------------------------------
# Computation
# ---------------------------------------------------------------------------

def farey_sequence(N):
    """Generate Farey sequence F_N as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def mobius_sieve(n):
    """Return list mu[0..n] with Mobius function values."""
    mu = [0] * (n + 1)
    mu[1] = 1
    is_prime = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for pr in primes:
            if i * pr > n:
                break
            is_prime[i * pr] = False
            if i % pr == 0:
                mu[i * pr] = 0
                break
            else:
                mu[i * pr] = -mu[i]
    return mu


def mertens(p):
    """Compute Mertens function M(p) = sum_{k=1}^{p} mu(k)."""
    mu = mobius_sieve(p)
    return sum(mu[1 : p + 1])


def compute_decomposition(p):
    """
    Compute the exact three-term decomposition of DeltaW for prime p.
    Verified to machine precision.
    """
    F_prev = farey_sequence(p - 1)
    F_curr = farey_sequence(p)

    n = len(F_prev)
    n_prime = len(F_curr)

    D_prev = {}
    for j, f in enumerate(F_prev):
        D_prev[f] = j - n * float(f)

    D_curr = {}
    for j, f in enumerate(F_curr):
        D_curr[f] = j - n_prime * float(f)

    new_fracs = [f for f in F_curr if f.denominator == p]

    calD = (1.0 / n_prime**2) * sum(D_curr[f] ** 2 for f in new_fracs)

    deltas = {}
    for f in F_prev:
        deltas[f] = D_curr[f] - (n_prime / n) * D_prev[f]

    B_cross = (2.0 / (n * n_prime)) * sum(D_prev[f] * deltas[f] for f in F_prev)

    C = (1.0 / n_prime**2) * sum(deltas[f] ** 2 for f in F_prev)

    # Verification
    DeltaW_decomp = calD + C + B_cross
    W_prev = sum(D_prev[f] ** 2 for f in F_prev) / n**2
    W_curr = sum(D_curr[f] ** 2 for f in F_curr) / n_prime**2
    DeltaW_actual = W_curr - W_prev
    assert abs(DeltaW_decomp - DeltaW_actual) < 1e-10

    frac_1p = Fraction(1, p)
    D_1p_sq = D_curr[frac_1p] ** 2 / n_prime**2
    D_1p_pct = D_1p_sq / calD if calD > 0 else 0.0

    damage_total = calD + C
    compensation = abs(B_cross) / damage_total if damage_total > 0 else 0.0

    return {
        "p": p, "n": n, "n_prime": n_prime,
        "calD": float(calD), "C": float(C), "B_cross": float(B_cross),
        "DeltaW": float(DeltaW_actual),
        "D_1p_sq": float(D_1p_sq), "D_1p_pct": float(D_1p_pct),
        "compensation": float(compensation), "M_p": mertens(p),
    }


# ---------------------------------------------------------------------------
# Select primes
# ---------------------------------------------------------------------------

candidate_primes = [
    11, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71, 79, 83, 89, 97,
    101, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
    167, 173, 179, 181, 191, 193, 197, 199,
]

print("Computing three-term decomposition...")
print(f"{'p':>5s} {'M(p)':>5s} {'calD':>10s} {'C':>10s} {'B_cross':>10s} "
      f"{'DeltaW':>10s} {'|B|/(D+C)':>10s} {'1/p share':>10s}")
print("-" * 75)

all_results = []
for p in candidate_primes:
    r = compute_decomposition(p)
    tag = " ***" if r["M_p"] <= -3 else ""
    print(
        f"  {r['p']:>3d}  {r['M_p']:>4d}  "
        f"{r['calD']:>10.6f} {r['C']:>10.6f} {r['B_cross']:>10.6f} "
        f"{r['DeltaW']:>10.6f} {r['compensation']:>9.1%} "
        f"{r['D_1p_pct']:>9.1%}{tag}"
    )
    if r["M_p"] <= -3:
        all_results.append(r)

target_primes = {43, 53, 71, 83, 107, 131, 173, 193}
selected = [r for r in all_results if r["p"] in target_primes]
if len(selected) < 8:
    for r in all_results:
        if r["p"] not in target_primes and len(selected) < 8:
            selected.append(r)
    selected.sort(key=lambda r: r["p"])

print(f"\nSelected {len(selected)} primes for figure:")
for r in selected:
    print(f"  p={r['p']:>3d}, M(p)={r['M_p']:>3d}, "
          f"compensation={r['compensation']:.1%}, 1/p share={r['D_1p_pct']:.1%}")

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(13.5, 5.8), gridspec_kw={"width_ratios": [2.5, 1]}
)
fig.subplots_adjust(wspace=0.28, left=0.10, right=0.96, top=0.87, bottom=0.10)

# Colours
COL_calD   = "#c44e52"
COL_D1p    = "#922b21"
COL_C      = "#dd8452"
COL_B      = "#4c72b0"
COL_net    = "#55a868"
COL_pct_1p = "#922b21"

n_bars = len(selected)
y_pos = np.arange(n_bars)
bar_h = 0.58

ytick_labels = ["p = %d  (M = %d)" % (r["p"], r["M_p"]) for r in selected]

# ===== Panel A ==============================================================
ax1.set_title(
    r"(a)  $\Delta W = \mathcal{D} + C + B$: damage vs. response",
    fontsize=12, fontweight="bold", pad=10, loc="left",
)

for i, r in enumerate(selected):
    calD_val = r["calD"]
    C_val    = r["C"]
    B_val    = r["B_cross"]
    DW       = r["DeltaW"]
    D_1p     = r["D_1p_sq"]

    # RIGHT: damage stack
    ax1.barh(i, calD_val, height=bar_h, color=COL_calD, edgecolor="white",
             linewidth=0.4, zorder=2,
             label=r"$\mathcal{D}$ (new-fraction damage)" if i == 0 else "")
    ax1.barh(i, C_val, left=calD_val, height=bar_h, color=COL_C,
             edgecolor="white", linewidth=0.4, zorder=2,
             label=r"$C$ (shift$^2$)" if i == 0 else "")

    # 1/p highlight
    ax1.barh(i, D_1p, height=bar_h, color=COL_D1p, edgecolor="none",
             zorder=2, alpha=0.7,
             label=r"$D(1/p)^2/n'^{\,2}$ portion" if i == 0 else "")

    # LEFT: response B
    ax1.barh(i, B_val, height=bar_h, color=COL_B, edgecolor="white",
             linewidth=0.4, zorder=2,
             label=r"$B$ (cross-term response)" if i == 0 else "")

    # Net DeltaW diamond
    ax1.plot(DW, i, marker="D", color=COL_net, markersize=6, zorder=4,
             markeredgecolor="white", markeredgewidth=0.6,
             label=r"net $\Delta W$" if i == 0 else "")

ax1.axvline(0, color="black", linewidth=0.7, zorder=3)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(ytick_labels, fontsize=9.5)
ax1.invert_yaxis()
ax1.set_xlabel(r"Contribution to $\Delta W = W(\mathcal{F}_p) - W(\mathcal{F}_{p-1})$",
               fontsize=10.5)

# Column headers
ax1.text(0.72, 1.02, "damage", transform=ax1.transAxes,
         fontsize=10, fontweight="bold", color=COL_calD, ha="center", va="bottom")
ax1.text(0.18, 1.02, "response", transform=ax1.transAxes,
         fontsize=10, fontweight="bold", color=COL_B, ha="center", va="bottom")

# Legend below chart
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(
    handles, labels,
    loc="upper left", bbox_to_anchor=(0.0, -0.08),
    fontsize=8.5, framealpha=0.95, edgecolor="#cccccc",
    borderpad=0.5, ncol=3, columnspacing=1.2,
)

ax1.grid(axis="x", alpha=0.2, linewidth=0.4)

# ===== Panel B ==============================================================
ax2.set_title(
    r"(b)  $D(1/p)^2$ share of $\mathcal{D}$",
    fontsize=12, fontweight="bold", pad=10, loc="left",
)

pcts = [r["D_1p_pct"] * 100 for r in selected]

ax2.barh(y_pos, [100] * n_bars, height=bar_h, color="#f2f2f2",
         edgecolor="#e0e0e0", linewidth=0.3)
bars = ax2.barh(y_pos, pcts, height=bar_h, color=COL_pct_1p,
                edgecolor="white", linewidth=0.4, alpha=0.85)

for i, pct in enumerate(pcts):
    ax2.text(pct + 1.2, i, f"{pct:.0f}%", va="center", fontsize=9.5,
             fontweight="bold", color=COL_D1p)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(["p = %d" % r["p"] for r in selected], fontsize=9.5)
ax2.invert_yaxis()
ax2.set_xlabel(r"Share of $\mathcal{D}$ (%)", fontsize=10.5)
ax2.set_xlim(0, 48)

mean_pct = np.mean(pcts)
ax2.axvline(mean_pct, color="#999999", linestyle="--", linewidth=0.9, alpha=0.7)
ax2.text(mean_pct + 0.8, n_bars - 0.3,
         "mean\n" + f"{mean_pct:.0f}%",
         fontsize=8.5, color="#888888", va="top", ha="left")

ax2.text(
    0.96, 0.06,
    ("A single fraction " + r"$1/p$" + "\n"
     "accounts for ~29% of\n"
     "total new-fraction damage"),
    transform=ax2.transAxes, fontsize=8, ha="right", va="bottom",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff5f5",
              edgecolor=COL_calD, alpha=0.85, linewidth=0.6),
)

ax2.grid(axis="x", alpha=0.2, linewidth=0.4)

# Formatting
for ax in (ax1, ax2):
    ax.tick_params(axis="both", which="major", labelsize=9.5)

fig.suptitle(
    "Damage/Response Mechanism in Farey Prime Insertions",
    fontsize=14, fontweight="bold", y=0.96,
)

# Save
out_dir = os.path.expanduser("~/Desktop/Farey-Local/figures")
os.makedirs(out_dir, exist_ok=True)

png_path = os.path.join(out_dir, "fig_damage_response.png")
pdf_path = os.path.join(out_dir, "fig_damage_response.pdf")

fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(pdf_path, bbox_inches="tight")
print(f"\nSaved: {png_path}")
print(f"Saved: {pdf_path}")

plt.close(fig)
print("Done.")
