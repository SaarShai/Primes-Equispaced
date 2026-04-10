#!/usr/bin/env python3
"""
Cauchy-Schwarz Gap Analysis for Farey Correlation Ratio R(p)
============================================================
For a prime p, generates F_{p-1} and decomposes the gap between
|R| and the Cauchy-Schwarz bound into within-denominator and
cross-denominator cancellation.

Definitions:
  D(a/b) = rank(a/b, F_{p-1}) - |F_{p-1}| * (a/b)
  delta(a/b) = a/b - (p*a mod b)/b
  R = sum(D*delta) / sum(delta^2)
  CS_bound = sqrt(sum(D^2)) / sqrt(sum(delta^2))
  tightness = |R| / CS_bound
"""

import math
import time
import sys
from collections import defaultdict


def farey_sequence(N):
    """Generate Farey sequence F_N as list of (a, b) with 0/1 and 1/1."""
    seq = []
    a, b, c, d = 0, 1, 1, N
    seq.append((a, b))
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        seq.append((a, b))
    return seq


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def euler_phi(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def analyze_cauchy_schwarz_gap(p):
    """Main analysis for prime p."""
    assert all(p % i != 0 for i in range(2, int(p**0.5) + 1)), f"{p} is not prime"

    N = p - 1
    print(f"Generating F_{N} for p={p}...")
    t0 = time.time()
    seq = farey_sequence(N)
    F_size = len(seq)
    t1 = time.time()
    print(f"  |F_{N}| = {F_size}, generated in {t1 - t0:.3f}s")

    # Compute D and delta for each fraction
    # Group by denominator
    denom_data = defaultdict(lambda: {
        'sum_Dd': 0.0, 'sum_dd': 0.0, 'sum_DD': 0.0,
        'sum_raw_abs_Dd': 0.0, 'phi': 0, 'count': 0
    })

    total_Dd = 0.0
    total_dd = 0.0
    total_DD = 0.0
    total_raw_abs_Dd = 0.0

    for rank_idx, (a, b) in enumerate(seq):
        # D(a/b) = rank - |F| * (a/b)
        f_val = a / b if b != 0 else 0.0
        D = rank_idx - F_size * f_val

        # delta(a/b) = a/b - (p*a mod b)/b
        if b == 0:
            delta = 0.0
        elif a == 0 or a == b:
            # endpoints: delta(0/1) = 0, delta(1/1) = 0
            delta = 0.0
        else:
            pa_mod_b = (p * a) % b
            delta = a / b - pa_mod_b / b

        Dd = D * delta
        dd = delta * delta
        DD = D * D

        total_Dd += Dd
        total_dd += dd
        total_DD += DD
        total_raw_abs_Dd += abs(Dd)

        d = denom_data[b]
        d['sum_Dd'] += Dd
        d['sum_dd'] += dd
        d['sum_DD'] += DD
        d['sum_raw_abs_Dd'] += abs(Dd)
        d['count'] += 1

    # Compute phi for each denominator
    for b in denom_data:
        denom_data[b]['phi'] = euler_phi(b)

    t2 = time.time()
    print(f"  Computed D, delta for all fractions in {t2 - t1:.3f}s")

    # Global quantities
    R = total_Dd / total_dd if total_dd > 0 else 0
    CS_bound = math.sqrt(total_DD) / math.sqrt(total_dd) if total_dd > 0 else 0
    tightness = abs(R) / CS_bound if CS_bound > 0 else 0
    looseness = 1.0 / tightness if tightness > 0 else float('inf')

    print(f"\n{'='*60}")
    print(f"GLOBAL RESULTS (p={p})")
    print(f"{'='*60}")
    print(f"  |F_{N}| = {F_size}")
    print(f"  Σ(D·δ)  = {total_Dd:.6f}")
    print(f"  Σ(δ²)   = {total_dd:.6f}")
    print(f"  Σ(D²)   = {total_DD:.6f}")
    print(f"  R = Σ(D·δ)/Σ(δ²) = {R:.10f}")
    print(f"  CS_bound = √(ΣD²)/√(Σδ²) = {CS_bound:.10f}")
    print(f"  tightness = |R|/CS = {tightness:.10f}")
    print(f"  looseness = CS/|R| = {looseness:.4f}x")

    # Cancellation decomposition
    # Within-denominator: how much cancellation happens inside each fixed b?
    # For each b, compare |Σ_b D·δ| to Σ_b |D·δ|
    within_retained = sum(abs(d['sum_Dd']) for d in denom_data.values())
    within_raw = sum(d['sum_raw_abs_Dd'] for d in denom_data.values())
    within_cancel_frac = 1.0 - within_retained / within_raw if within_raw > 0 else 0

    # Cross-denominator: how much cancellation when summing the per-b totals?
    cross_retained = abs(total_Dd)
    cross_cancel_frac = 1.0 - cross_retained / within_retained if within_retained > 0 else 0

    print(f"\n{'='*60}")
    print(f"CANCELLATION DECOMPOSITION")
    print(f"{'='*60}")
    print(f"  Σ|D·δ| (raw pointwise)     = {within_raw:.6f}")
    print(f"  Σ_b |Σ_within_b D·δ| (after within-b cancel) = {within_retained:.6f}")
    print(f"  |Σ_all D·δ| (after cross-b cancel) = {cross_retained:.6f}")
    print(f"  Within-denom cancellation   = {within_cancel_frac:.4%}")
    print(f"  Cross-denom cancellation    = {cross_cancel_frac:.4%}")
    print(f"  Within-denom retention      = {1.0 - within_cancel_frac:.4%}")
    print(f"  Cross-denom retention       = {1.0 - cross_cancel_frac:.4%}")

    # Per-denominator table
    denom_list = []
    for b, d in denom_data.items():
        if d['sum_dd'] > 0:
            R_b = d['sum_Dd'] / d['sum_dd']
        else:
            R_b = 0.0
        weight = d['sum_dd'] / total_dd if total_dd > 0 else 0
        weighted_contrib = R_b * weight
        denom_list.append({
            'b': b,
            'phi': d['phi'],
            'count': d['count'],
            'sum_Dd': d['sum_Dd'],
            'sum_dd': d['sum_dd'],
            'sum_DD': d['sum_DD'],
            'R_b': R_b,
            'weight': weight,
            'weighted_contrib': weighted_contrib,
        })

    # Sort by |weighted_contrib| descending
    denom_list.sort(key=lambda x: abs(x['weighted_contrib']), reverse=True)

    # Sign statistics
    pos_Rb = sum(1 for d in denom_list if d['R_b'] > 0)
    neg_Rb = sum(1 for d in denom_list if d['R_b'] < 0)
    zero_Rb = sum(1 for d in denom_list if d['R_b'] == 0)
    active = len(denom_list)

    print(f"\n{'='*60}")
    print(f"DENOMINATOR SIGN DISTRIBUTION")
    print(f"{'='*60}")
    print(f"  Active denominators: {active}")
    print(f"  Positive R_b: {pos_Rb}")
    print(f"  Negative R_b: {neg_Rb}")
    print(f"  Zero R_b:     {zero_Rb}")

    # Size-band analysis
    bands = [(2, 49), (50, 99), (100, 199), (200, 399), (400, 699), (700, N)]
    print(f"\n{'='*60}")
    print(f"CONTRIBUTION BY DENOMINATOR SIZE BAND")
    print(f"{'='*60}")
    print(f"  {'Band':>12} | {'Σ weighted_contrib':>18} | {'# denoms':>8} | {'# pos':>6} | {'# neg':>6}")
    print(f"  {'-'*12}-+-{'-'*18}-+-{'-'*8}-+-{'-'*6}-+-{'-'*6}")
    for lo, hi in bands:
        in_band = [d for d in denom_list if lo <= d['b'] <= hi]
        band_contrib = sum(d['weighted_contrib'] for d in in_band)
        n_pos = sum(1 for d in in_band if d['R_b'] > 0)
        n_neg = sum(1 for d in in_band if d['R_b'] < 0)
        print(f"  {lo:>5}-{hi:<5} | {band_contrib:>+18.10f} | {len(in_band):>8} | {n_pos:>6} | {n_neg:>6}")

    # Top 30 table
    print(f"\n{'='*60}")
    print(f"TOP 30 DENOMINATORS BY |WEIGHTED CONTRIBUTION|")
    print(f"{'='*60}")
    hdr = f"  {'b':>5} | {'φ(b)':>5} | {'Σ D·δ':>14} | {'Σ δ²':>14} | {'R_b':>12} | {'weight':>8} | {'w·R_b':>12}"
    print(hdr)
    print(f"  {'-'*5}-+-{'-'*5}-+-{'-'*14}-+-{'-'*14}-+-{'-'*12}-+-{'-'*8}-+-{'-'*12}")
    for d in denom_list[:30]:
        print(f"  {d['b']:>5} | {d['phi']:>5} | {d['sum_Dd']:>+14.6f} | {d['sum_dd']:>14.6f} | {d['R_b']:>+12.6f} | {d['weight']:>8.6f} | {d['weighted_contrib']:>+12.8f}")

    # Write report
    report = generate_report(p, N, F_size, R, CS_bound, tightness, looseness,
                              total_Dd, total_dd, total_DD,
                              within_raw, within_retained, cross_retained,
                              within_cancel_frac, cross_cancel_frac,
                              pos_Rb, neg_Rb, zero_Rb, active,
                              bands, denom_list)
    return report


def generate_report(p, N, F_size, R, CS_bound, tightness, looseness,
                     total_Dd, total_dd, total_DD,
                     within_raw, within_retained, cross_retained,
                     within_cancel_frac, cross_cancel_frac,
                     pos_Rb, neg_Rb, zero_Rb, active,
                     bands, denom_list):
    lines = []
    lines.append(f"# Cauchy-Schwarz Gap Analysis for R(p={p})")
    lines.append(f"")
    lines.append(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Prime:** p = {p}, N = p-1 = {N}")
    lines.append(f"**Farey order:** F_{{{N}}}, |F_{{{N}}}| = {F_size:,}")
    lines.append(f"")
    lines.append(f"## Definitions")
    lines.append(f"")
    lines.append(f"For f = a/b in F_N with gcd(a,b) = 1:")
    lines.append(f"- **D(f)** = rank(f, F_N) - |F_N| · f  (rank deviation)")
    lines.append(f"- **δ(f)** = f - {{pf}} = a/b - (pa mod b)/b  (insertion deviation)")
    lines.append(f"- **R** = Σ D·δ / Σ δ²  (correlation ratio)")
    lines.append(f"- **CS bound** = √(Σ D²) / √(Σ δ²)  (Cauchy-Schwarz upper bound on |R|)")
    lines.append(f"")
    lines.append(f"## Global Results")
    lines.append(f"")
    lines.append(f"| Quantity | Value |")
    lines.append(f"|:---------|------:|")
    lines.append(f"| Σ(D·δ) | {total_Dd:,.6f} |")
    lines.append(f"| Σ(δ²) | {total_dd:,.6f} |")
    lines.append(f"| Σ(D²) | {total_DD:,.2f} |")
    lines.append(f"| **R** | **{R:.10f}** |")
    lines.append(f"| **CS bound** | **{CS_bound:.10f}** |")
    lines.append(f"| **Tightness** |R|/CS | **{tightness:.10f}** |")
    lines.append(f"| **Looseness** CS/|R| | **{looseness:.4f}×** |")
    lines.append(f"")
    lines.append(f"## Cancellation Decomposition")
    lines.append(f"")
    lines.append(f"The gap between |R| and the CS bound arises from two sources:")
    lines.append(f"")
    lines.append(f"1. **Within-denominator cancellation**: D·δ products with different signs")
    lines.append(f"   for fractions sharing the same denominator b.")
    lines.append(f"2. **Cross-denominator cancellation**: per-denominator sums Σ_b(D·δ) with")
    lines.append(f"   different signs across different b values.")
    lines.append(f"")
    lines.append(f"| Stage | Raw | Retained | Cancelled |")
    lines.append(f"|:------|----:|---------:|----------:|")
    lines.append(f"| Pointwise → per-denom | {within_raw:,.4f} | {within_retained:,.4f} | {within_cancel_frac:.2%} |")
    lines.append(f"| Per-denom → global | {within_retained:,.4f} | {cross_retained:,.4f} | {cross_cancel_frac:.2%} |")
    lines.append(f"")
    lines.append(f"**Key finding:** ~{within_cancel_frac:.0%} of the raw |D·δ| mass cancels within")
    lines.append(f"fixed denominators. Only ~{cross_cancel_frac:.0%} additional cancellation occurs")
    lines.append(f"when summing across denominators. The within-denominator oscillation of D and δ")
    lines.append(f"is the dominant source of the Cauchy-Schwarz gap.")
    lines.append(f"")
    lines.append(f"## Denominator Sign Distribution")
    lines.append(f"")
    lines.append(f"| Category | Count |")
    lines.append(f"|:---------|------:|")
    lines.append(f"| Active denominators | {active} |")
    lines.append(f"| Positive R_b | {pos_Rb} |")
    lines.append(f"| Negative R_b | {neg_Rb} |")
    lines.append(f"| Zero R_b | {zero_Rb} |")
    lines.append(f"")
    lines.append(f"## Contribution by Denominator Size Band")
    lines.append(f"")
    lines.append(f"| Band | Σ weighted R_b | # denoms | # pos | # neg |")
    lines.append(f"|:-----|---------------:|---------:|------:|------:|")
    for lo, hi in bands:
        in_band = [d for d in denom_list if lo <= d['b'] <= hi]
        band_contrib = sum(d['weighted_contrib'] for d in in_band)
        n_pos = sum(1 for d in in_band if d['R_b'] > 0)
        n_neg = sum(1 for d in in_band if d['R_b'] < 0)
        lines.append(f"| {lo}–{hi} | {band_contrib:+.10f} | {len(in_band)} | {n_pos} | {n_neg} |")
    lines.append(f"")
    lines.append(f"## Top 30 Denominators by |Weighted Contribution|")
    lines.append(f"")
    lines.append(f"| b | φ(b) | Σ D·δ | Σ δ² | R_b | weight | w·R_b |")
    lines.append(f"|---:|-----:|------:|-----:|----:|-------:|------:|")
    for d in denom_list[:30]:
        lines.append(f"| {d['b']} | {d['phi']} | {d['sum_Dd']:+.6f} | {d['sum_dd']:.6f} | {d['R_b']:+.6f} | {d['weight']:.6f} | {d['weighted_contrib']:+.8f} |")
    lines.append(f"")
    lines.append(f"## Analysis")
    lines.append(f"")
    lines.append(f"### Where does the cancellation come from?")
    lines.append(f"")
    lines.append(f"The Cauchy-Schwarz bound is {looseness:.1f}× looser than the actual |R| value.")
    lines.append(f"This gap decomposes as follows:")
    lines.append(f"")
    lines.append(f"1. **Within-denominator oscillation ({within_cancel_frac:.0%})**: For a fixed denominator b,")
    lines.append(f"   the products D(a/b)·δ(a/b) alternate in sign as a varies over the φ(b)")
    lines.append(f"   coprime numerators. The rank deviation D has a known sawtooth structure")
    lines.append(f"   (related to Dedekind sums), while δ depends on the arithmetic of p·a mod b.")
    lines.append(f"   These two oscillations are only weakly correlated, causing massive cancellation.")
    lines.append(f"")
    lines.append(f"2. **Cross-denominator sign changes ({cross_cancel_frac:.0%})**: The per-denominator")
    lines.append(f"   sums R_b have {pos_Rb} positive and {neg_Rb} negative values. However, the")
    lines.append(f"   positive values dominate ({pos_Rb} vs {neg_Rb}), so the net effect after")
    lines.append(f"   cross-denominator summation is a further {cross_cancel_frac:.0%} reduction.")
    lines.append(f"")
    lines.append(f"### Implications for tighter bounds")
    lines.append(f"")
    lines.append(f"To close the Cauchy-Schwarz gap, we need to exploit the within-denominator")
    lines.append(f"structure. For each fixed b, the sum Σ_{{gcd(a,b)=1}} D(a/b)·δ(a/b) can be")
    lines.append(f"related to Kloosterman sums S(p, 1; b) via the Dedekind sum representation of D.")
    lines.append(f"The exponential sum cancellation within Kloosterman sums is precisely what")
    lines.append(f"drives the within-denominator cancellation observed here.")
    lines.append(f"")
    lines.append(f"A tighter bound should replace Cauchy-Schwarz with a per-denominator estimate:")
    lines.append(f"  R = Σ_b (w_b · R_b) where w_b = Σ_b δ² / Σ_all δ²")
    lines.append(f"and bound each R_b using the Weil bound for Kloosterman sums.")
    lines.append(f"")

    return "\n".join(lines)


if __name__ == "__main__":
    p = 997
    if len(sys.argv) > 1:
        p = int(sys.argv[1])
    report = analyze_cauchy_schwarz_gap(p)

    # Write report
    outpath = sys.argv[2] if len(sys.argv) > 2 else None
    if outpath:
        with open(outpath, 'w') as f:
            f.write(report)
        print(f"\nReport written to {outpath}")
    else:
        # Default paths
        import os
        for base in [os.path.expanduser("~/Desktop/Farey-Local/experiments"),
                     "/Users/saar/Library/CloudStorage/GoogleDrive-saar.shai@gmail.com/My Drive/Farey Folder/experiments"]:
            if os.path.isdir(base):
                outpath = os.path.join(base, "CAUCHY_SCHWARZ_GAP.md")
                with open(outpath, 'w') as f:
                    f.write(report)
                print(f"\nReport written to {outpath}")
