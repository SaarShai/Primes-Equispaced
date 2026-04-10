#!/usr/bin/env python3
"""
R CANCELLATION ANALYSIS
========================
Why is |R(p)| empirically < 0.26 when Cauchy-Schwarz allows up to ~6.6?

R(p) = 2 * Sum D(f)*delta(f) / Sum delta(f)^2

The CS bound gives |R| <= 2*sqrt(Sum D^2 / Sum delta^2) ~ 6.6 for small p.
But empirically |R| < 0.26 for ALL tested primes.

This script investigates the MASSIVE sign cancellation that causes this.

INVESTIGATIONS:
1. Per-denominator cancellation: within each b, do D*delta terms cancel?
2. Cross-denominator cancellation: do C_b contributions cancel across b?
3. Correlation structure: D(f) vs delta(f) scatter
4. Structural reasons: symmetry, multiplicative independence, equidistribution
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import gcd, isqrt, sqrt
from collections import defaultdict
from fractions import Fraction
import os

OUTPUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")
FIG_DIR = os.path.expanduser("~/Desktop/Farey-Local/figures")
os.makedirs(FIG_DIR, exist_ok=True)


# ============================================================
# UTILITIES
# ============================================================

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def mertens_sieve(limit):
    sp = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if sp[i] == 0:
            for j in range(i, limit + 1, i):
                if sp[j] == 0:
                    sp[j] = i
    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        r = n
        nf = 0
        sqfree = True
        while r > 1:
            p = sp[r]
            c = 0
            while r % p == 0:
                r //= p
                c += 1
            if c >= 2:
                sqfree = False
                break
            nf += 1
        if sqfree:
            mu[n] = (-1) ** nf
    M = [0] * (limit + 1)
    for i in range(1, limit + 1):
        M[i] = M[i-1] + mu[i]
    return mu, M


def farey_sequence(N):
    """Return sorted Farey sequence F_N as list of (a, b) tuples."""
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: x[0] / x[1])
    return fracs


def compute_D_delta(p, fracs):
    """
    For each f = a/b in F_{p-1}, compute:
      D(f) = rank(f) - n * f   (discrepancy from uniform)
      delta(f) = (a - p*a mod b) / b  (per-step wobble)
    Returns arrays of (a, b, D, delta, D*delta) grouped by denominator.
    """
    N = p - 1
    n = len(fracs)

    by_denom = defaultdict(list)
    all_data = []

    for j, (a, b) in enumerate(fracs):
        f_val = a / b
        D = j - n * f_val  # rank is j (0-indexed)

        if a == 0 or a == b:
            delta = 0.0
        else:
            pa_mod_b = (p * a) % b
            delta = (a - pa_mod_b) / b

        prod = D * delta
        by_denom[b].append({'a': a, 'D': D, 'delta': delta, 'prod': prod})
        all_data.append({'a': a, 'b': b, 'D': D, 'delta': delta, 'prod': prod, 'f': f_val})

    return by_denom, all_data, n


# ============================================================
# INVESTIGATION 1: Per-denominator cancellation
# ============================================================

def per_denom_cancellation(p, by_denom):
    """
    For each denominator b, compute:
    - C_b = Sum D(a/b)*delta(a/b)  (signed cross term)
    - |C_b| vs Sum |D*delta|  (cancellation ratio)
    - sign pattern of D*delta terms
    """
    results = {}
    for b in sorted(by_denom.keys()):
        entries = by_denom[b]
        phi_b = len(entries)

        prods = [e['prod'] for e in entries]
        C_b = sum(prods)
        abs_sum = sum(abs(x) for x in prods)

        n_pos = sum(1 for x in prods if x > 0)
        n_neg = sum(1 for x in prods if x < 0)
        n_zero = sum(1 for x in prods if x == 0)

        # Cancellation ratio: 1 = perfect cancellation, 0 = no cancellation
        cancel_ratio = 1 - abs(C_b) / abs_sum if abs_sum > 0 else 0

        # Also track the delta sum (should be ~0 for coprime permutation)
        delta_sum = sum(e['delta'] for e in entries)

        results[b] = {
            'phi_b': phi_b,
            'C_b': C_b,
            'abs_sum': abs_sum,
            'cancel_ratio': cancel_ratio,
            'n_pos': n_pos,
            'n_neg': n_neg,
            'n_zero': n_zero,
            'delta_sum': delta_sum,
        }

    return results


# ============================================================
# INVESTIGATION 2: Cross-denominator cancellation
# ============================================================

def cross_denom_cancellation(per_denom_results):
    """
    Are some denominators positive contributors and others negative?
    How much do C_b values cancel across b?
    """
    C_vals = {b: r['C_b'] for b, r in per_denom_results.items()}

    total = sum(C_vals.values())
    abs_total = sum(abs(v) for v in C_vals.values())

    pos_contrib = sum(v for v in C_vals.values() if v > 0)
    neg_contrib = sum(v for v in C_vals.values() if v < 0)

    cross_cancel = 1 - abs(total) / abs_total if abs_total > 0 else 0

    return {
        'total_cross': total,
        'abs_total': abs_total,
        'pos_contrib': pos_contrib,
        'neg_contrib': neg_contrib,
        'cross_cancel_ratio': cross_cancel,
        'C_by_denom': C_vals,
    }


# ============================================================
# INVESTIGATION 3: Correlation structure
# ============================================================

def correlation_analysis(all_data, n):
    """
    Analyze correlation between D and delta.
    """
    D_arr = np.array([d['D'] for d in all_data])
    delta_arr = np.array([d['delta'] for d in all_data])

    # Pearson correlation
    if np.std(D_arr) > 0 and np.std(delta_arr) > 0:
        corr = np.corrcoef(D_arr, delta_arr)[0, 1]
    else:
        corr = 0.0

    # Spearman rank correlation
    from scipy.stats import spearmanr
    spear_corr, spear_p = spearmanr(D_arr, delta_arr)

    # Cross moment
    cross_moment = np.sum(D_arr * delta_arr)

    # CS bound
    cs_bound = np.sqrt(np.sum(D_arr**2) * np.sum(delta_arr**2))
    cs_ratio = abs(cross_moment) / cs_bound if cs_bound > 0 else 0

    return {
        'pearson_corr': corr,
        'spearman_corr': spear_corr,
        'spearman_p': spear_p,
        'cross_moment': cross_moment,
        'cs_bound': cs_bound,
        'cs_ratio': cs_ratio,
        'D': D_arr,
        'delta': delta_arr,
    }


# ============================================================
# INVESTIGATION 4: Structural analysis
# ============================================================

def structural_analysis(p, by_denom, all_data, n):
    """
    Deeper structural investigation:
    - Symmetry: D(-f) vs D(f), delta(-f) vs delta(f)
    - Within each b: how does the permutation sigma_p scramble?
    - Multiplicative structure
    """
    N = p - 1

    # For each b, the map a -> pa mod b is a permutation of units mod b
    # delta(a/b) = (a - sigma_p(a))/b where sigma_p(a) = pa mod b
    # D(a/b) depends on the global rank

    # Check: within each b, is D essentially "smooth" while delta is "scrambled"?
    results = {}
    for b in sorted(by_denom.keys()):
        if b <= 1:
            continue
        entries = sorted(by_denom[b], key=lambda e: e['a'])

        D_vals = np.array([e['D'] for e in entries])
        delta_vals = np.array([e['delta'] for e in entries])

        # D variation: how much does D change across a for fixed b?
        D_range = np.max(D_vals) - np.min(D_vals)
        D_std = np.std(D_vals)

        # delta variation
        delta_range = np.max(delta_vals) - np.min(delta_vals)
        delta_std = np.std(delta_vals)

        # Within-b correlation
        if D_std > 0 and delta_std > 0:
            within_corr = np.corrcoef(D_vals, delta_vals)[0, 1]
        else:
            within_corr = 0.0

        results[b] = {
            'D_range': D_range,
            'D_std': D_std,
            'delta_range': delta_range,
            'delta_std': delta_std,
            'within_corr': within_corr,
        }

    return results


# ============================================================
# INVESTIGATION 5: Random permutation comparison
# ============================================================

def random_comparison(p, fracs, n, n_trials=200):
    """
    Compare actual |R| to what we'd get with random permutations.
    For each denominator b, replace sigma_p with a random permutation of units mod b.
    """
    N = p - 1
    rng = np.random.default_rng(42)

    # Compute D values (fixed regardless of permutation)
    D_vals = {}
    for j, (a, b) in enumerate(fracs):
        D_vals[(a, b)] = j - n * (a / b)

    # Group by denominator
    denom_groups = defaultdict(list)
    for a, b in fracs:
        if a > 0 and a < b:
            denom_groups[b].append(a)

    # Actual R
    sum_D_delta = 0.0
    sum_delta_sq = 0.0
    for (a, b), D in D_vals.items():
        if a == 0 or a == b:
            continue
        pa_mod_b = (p * a) % b
        delta = (a - pa_mod_b) / b
        sum_D_delta += D * delta
        sum_delta_sq += delta * delta

    R_actual = 2 * sum_D_delta / sum_delta_sq if sum_delta_sq > 0 else 0

    # Random trials
    R_random = []
    for _ in range(n_trials):
        sdd = 0.0
        sds = 0.0
        for b, a_list in denom_groups.items():
            perm = list(a_list)
            rng.shuffle(perm)
            for a, sigma_a in zip(a_list, perm):
                D = D_vals[(a, b)]
                delta = (a - sigma_a) / b
                sdd += D * delta
                sds += delta * delta
        if sds > 0:
            R_random.append(2 * sdd / sds)

    return R_actual, np.array(R_random)


# ============================================================
# PLOTTING
# ============================================================

def plot_scatter_D_vs_delta(p, all_data, corr_data, fig_dir):
    """Scatter plot of D(f) vs delta(f) colored by denominator."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    D = corr_data['D']
    delta = corr_data['delta']
    b_arr = np.array([d['b'] for d in all_data])

    # Color by denominator
    ax = axes[0]
    scatter = ax.scatter(delta, D, c=b_arr, cmap='viridis', s=8, alpha=0.6)
    plt.colorbar(scatter, ax=ax, label='denominator b')
    ax.set_xlabel('delta(f)')
    ax.set_ylabel('D(f)')
    ax.set_title(f'p={p}: D vs delta (Pearson r={corr_data["pearson_corr"]:.4f})')
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)

    # Product D*delta heatmap
    ax = axes[1]
    prods = D * delta
    colors = ['red' if x < 0 else 'blue' for x in prods]
    ax.scatter(delta, D, c=colors, s=np.abs(prods)*2 + 1, alpha=0.4)
    ax.set_xlabel('delta(f)')
    ax.set_ylabel('D(f)')
    ax.set_title(f'p={p}: D*delta sign (blue=+, red=-)')
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, f'fig_R_cancel_scatter_p{p}.png'), dpi=150)
    plt.close()


def plot_per_denom_anatomy(p, per_denom_results, cross_results, fig_dir):
    """Bar chart of C_b by denominator, showing cancellation."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    denoms = sorted(per_denom_results.keys())
    denoms = [b for b in denoms if b > 1]  # skip b=1

    C_vals = [per_denom_results[b]['C_b'] for b in denoms]
    abs_sums = [per_denom_results[b]['abs_sum'] for b in denoms]
    cancel_ratios = [per_denom_results[b]['cancel_ratio'] for b in denoms]
    phi_vals = [per_denom_results[b]['phi_b'] for b in denoms]

    # C_b values
    ax = axes[0, 0]
    colors = ['blue' if c >= 0 else 'red' for c in C_vals]
    ax.bar(range(len(denoms)), C_vals, color=colors, alpha=0.7)
    ax.set_xticks(range(len(denoms)))
    ax.set_xticklabels(denoms, fontsize=6, rotation=45)
    ax.set_xlabel('denominator b')
    ax.set_ylabel('C_b = Sum D*delta')
    ax.set_title(f'p={p}: Per-denom cross terms C_b')
    ax.axhline(0, color='gray', lw=0.5)

    # Cancellation ratio within each b
    ax = axes[0, 1]
    ax.bar(range(len(denoms)), cancel_ratios, color='green', alpha=0.7)
    ax.set_xticks(range(len(denoms)))
    ax.set_xticklabels(denoms, fontsize=6, rotation=45)
    ax.set_xlabel('denominator b')
    ax.set_ylabel('Cancellation ratio')
    ax.set_title(f'p={p}: Within-denom cancellation (1=perfect)')

    # Cumulative C_b (running sum reveals cross-denom cancellation)
    ax = axes[1, 0]
    cum_C = np.cumsum(C_vals)
    ax.plot(range(len(denoms)), cum_C, 'b-o', markersize=3)
    ax.set_xticks(range(len(denoms)))
    ax.set_xticklabels(denoms, fontsize=6, rotation=45)
    ax.set_xlabel('denominator b')
    ax.set_ylabel('Cumulative Sum C_b')
    ax.set_title(f'p={p}: Running sum of C_b (shows cross-denom cancel)')
    ax.axhline(0, color='gray', lw=0.5)

    # |C_b| vs phi(b)
    ax = axes[1, 1]
    ax.scatter(phi_vals, [abs(c) for c in C_vals], alpha=0.6)
    ax.set_xlabel('phi(b)')
    ax.set_ylabel('|C_b|')
    ax.set_title(f'p={p}: |C_b| vs phi(b)')

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, f'fig_R_cancel_anatomy_p{p}.png'), dpi=150)
    plt.close()


def plot_random_comparison(p, R_actual, R_random, fig_dir):
    """Histogram of R from random permutations vs actual R."""
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(R_random, bins=40, alpha=0.7, density=True, color='gray', label='Random perm')
    ax.axvline(R_actual, color='red', lw=2, label=f'Actual R={R_actual:.4f}')
    ax.axvline(0, color='black', lw=0.5, ls='--')

    mean_rand = np.mean(R_random)
    std_rand = np.std(R_random)
    ax.axvline(mean_rand, color='blue', lw=1, ls='--', label=f'Random mean={mean_rand:.4f}')

    ax.set_xlabel('R value')
    ax.set_ylabel('Density')
    ax.set_title(f'p={p}: Actual R vs random permutation R (std={std_rand:.4f})')
    ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, f'fig_R_cancel_random_p{p}.png'), dpi=150)
    plt.close()

    return mean_rand, std_rand


def plot_within_denom_correlation(p, structural_results, fig_dir):
    """Heatmap-like plot of within-denominator correlations."""
    denoms = sorted(b for b in structural_results.keys() if structural_results[b]['D_std'] > 0)
    corrs = [structural_results[b]['within_corr'] for b in denoms]

    fig, ax = plt.subplots(figsize=(12, 4))
    colors = ['blue' if c >= 0 else 'red' for c in corrs]
    ax.bar(range(len(denoms)), corrs, color=colors, alpha=0.7)
    ax.set_xticks(range(len(denoms)))
    ax.set_xticklabels(denoms, fontsize=5, rotation=45)
    ax.set_xlabel('denominator b')
    ax.set_ylabel('Within-b correlation(D, delta)')
    ax.set_title(f'p={p}: Within-denominator correlation between D and delta')
    ax.axhline(0, color='gray', lw=0.5)
    ax.set_ylim(-1.1, 1.1)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, f'fig_R_cancel_within_corr_p{p}.png'), dpi=150)
    plt.close()

    return corrs


# ============================================================
# MULTI-PRIME SUMMARY
# ============================================================

def plot_summary(prime_data, fig_dir):
    """Summary plots across all primes."""
    primes = [d['p'] for d in prime_data]
    R_vals = [d['R_actual'] for d in prime_data]
    cs_ratios = [d['cs_ratio'] for d in prime_data]
    pearson = [d['pearson'] for d in prime_data]
    within_cancel = [d['within_cancel_avg'] for d in prime_data]
    cross_cancel = [d['cross_cancel'] for d in prime_data]

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # |R| vs p
    ax = axes[0, 0]
    ax.scatter(primes, [abs(r) for r in R_vals], s=10, alpha=0.7)
    ax.set_xlabel('p')
    ax.set_ylabel('|R(p)|')
    ax.set_title('|R(p)| vs prime p')
    ax.axhline(0.26, color='red', ls='--', label='0.26 barrier')
    ax.legend()

    # CS usage ratio
    ax = axes[0, 1]
    ax.scatter(primes, cs_ratios, s=10, alpha=0.7, color='green')
    ax.set_xlabel('p')
    ax.set_ylabel('|Sum D*delta| / sqrt(Sum D^2 * Sum delta^2)')
    ax.set_title('CS tightness ratio (how much of CS bound is used)')

    # Pearson correlation
    ax = axes[0, 2]
    ax.scatter(primes, pearson, s=10, alpha=0.7, color='purple')
    ax.set_xlabel('p')
    ax.set_ylabel('Pearson corr(D, delta)')
    ax.set_title('Global correlation D vs delta')
    ax.axhline(0, color='gray', lw=0.5)

    # Within-denom cancellation
    ax = axes[1, 0]
    ax.scatter(primes, within_cancel, s=10, alpha=0.7, color='orange')
    ax.set_xlabel('p')
    ax.set_ylabel('Avg within-denom cancellation ratio')
    ax.set_title('Within-denominator cancellation (1=perfect)')

    # Cross-denom cancellation
    ax = axes[1, 1]
    ax.scatter(primes, cross_cancel, s=10, alpha=0.7, color='brown')
    ax.set_xlabel('p')
    ax.set_ylabel('Cross-denom cancellation ratio')
    ax.set_title('Cross-denominator cancellation (1=perfect)')

    # Both cancellation types
    ax = axes[1, 2]
    ax.scatter(within_cancel, cross_cancel, c=primes, cmap='viridis', s=15, alpha=0.7)
    plt.colorbar(ax.collections[0], ax=ax, label='prime p')
    ax.set_xlabel('Within-denom cancellation')
    ax.set_ylabel('Cross-denom cancellation')
    ax.set_title('Within vs Cross cancellation')

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig_R_cancel_summary.png'), dpi=150)
    plt.close()


def plot_cancellation_decomposition(prime_data, fig_dir):
    """Stacked bar: within-denom vs cross-denom cancellation contribution."""
    primes = [d['p'] for d in prime_data if d['p'] <= 200]

    fig, ax = plt.subplots(figsize=(14, 6))

    # For each prime, show:
    # - Total |Sum D*delta| before cancellation (sum of |individual terms|)
    # - After within-denom cancellation (sum of |C_b|)
    # - After cross-denom cancellation (|Sum C_b|)

    total_abs = []
    after_within = []
    after_cross = []

    for d in prime_data:
        if d['p'] > 200:
            continue
        total_abs.append(d['total_abs_terms'])
        after_within.append(d['sum_abs_Cb'])
        after_cross.append(d['abs_total_cross'])

    x = range(len(primes))
    ax.bar(x, total_abs, alpha=0.3, color='gray', label='Sum |D*delta| (no cancellation)')
    ax.bar(x, after_within, alpha=0.5, color='blue', label='Sum |C_b| (after within-b cancel)')
    ax.bar(x, after_cross, alpha=0.8, color='red', label='|Sum C_b| (after cross-b cancel)')

    ax.set_xticks(x)
    ax.set_xticklabels(primes, fontsize=6, rotation=45)
    ax.set_xlabel('prime p')
    ax.set_ylabel('Magnitude')
    ax.set_title('Cancellation decomposition: total -> within-denom -> cross-denom')
    ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'fig_R_cancel_decomposition.png'), dpi=150)
    plt.close()


# ============================================================
# MAIN ANALYSIS
# ============================================================

if __name__ == '__main__':
    from scipy.stats import spearmanr
    import time

    mu, M = mertens_sieve(2000)
    primes = sieve_primes(800)
    test_primes = [p for p in primes if p >= 11]

    print("=" * 80)
    print("R CANCELLATION ANALYSIS")
    print("Why |R(p)| << CS bound for all primes")
    print("=" * 80)

    # -------------------------------------------------------
    # Phase 1: Detailed analysis for selected primes
    # -------------------------------------------------------
    detail_primes = [11, 13, 23, 37, 53, 97, 199, 307, 503]
    detail_primes = [p for p in detail_primes if p in test_primes]

    print("\n" + "=" * 60)
    print("PHASE 1: DETAILED PER-PRIME ANALYSIS")
    print("=" * 60)

    for p in detail_primes:
        t0 = time.time()
        N = p - 1
        fracs = farey_sequence(N)
        by_denom, all_data, n = compute_D_delta(p, fracs)

        # Investigation 1: per-denom cancellation
        pd_results = per_denom_cancellation(p, by_denom)

        # Investigation 2: cross-denom cancellation
        cross_results = cross_denom_cancellation(pd_results)

        # Investigation 3: correlation
        corr_data = correlation_analysis(all_data, n)

        # Investigation 4: structural
        struct_data = structural_analysis(p, by_denom, all_data, n)

        # Compute R
        sum_D_delta = sum(d['prod'] for d in all_data)
        sum_delta_sq = sum(d['delta']**2 for d in all_data)
        R = 2 * sum_D_delta / sum_delta_sq if sum_delta_sq > 0 else 0

        elapsed = time.time() - t0

        print(f"\n--- p = {p} (M(p)={M[p]}, N={N}, |F_N|={n}) [{elapsed:.2f}s] ---")
        print(f"  R(p) = {R:.6f}")
        print(f"  |Sum D*delta| = {abs(sum_D_delta):.4f}")
        print(f"  Sum delta^2 = {sum_delta_sq:.4f}")
        print(f"  CS bound: |R| <= {2*corr_data['cs_bound']/sum_delta_sq:.4f}")
        print(f"  CS usage: {corr_data['cs_ratio']:.6f} ({corr_data['cs_ratio']*100:.2f}%)")
        print(f"  Pearson corr(D, delta) = {corr_data['pearson_corr']:.6f}")
        print(f"  Spearman corr(D, delta) = {corr_data['spearman_corr']:.6f} (p={corr_data['spearman_p']:.4f})")

        # Within-denom cancellation summary
        cancel_ratios = [pd_results[b]['cancel_ratio'] for b in pd_results if b > 1 and pd_results[b]['abs_sum'] > 0]
        avg_within = np.mean(cancel_ratios) if cancel_ratios else 0
        print(f"  Within-denom cancellation: avg={avg_within:.4f}")

        # Cross-denom cancellation
        print(f"  Cross-denom cancellation: {cross_results['cross_cancel_ratio']:.4f}")
        print(f"    Positive C_b contrib: {cross_results['pos_contrib']:+.4f}")
        print(f"    Negative C_b contrib: {cross_results['neg_contrib']:+.4f}")

        # Per-denom detail (top contributing)
        top_denoms = sorted(pd_results.items(), key=lambda x: abs(x[1]['C_b']), reverse=True)[:8]
        print(f"  Top contributing denominators:")
        print(f"    {'b':>4} {'phi(b)':>6} {'C_b':>12} {'|C_b|/Sum|':>12} {'within_cancel':>14}")
        for b, r in top_denoms:
            if b <= 1:
                continue
            print(f"    {b:4d} {r['phi_b']:6d} {r['C_b']:+12.4f} {abs(r['C_b'])/r['abs_sum'] if r['abs_sum']>0 else 0:12.4f} {r['cancel_ratio']:14.4f}")

        # Within-denom correlation detail
        corr_list = [(b, struct_data[b]['within_corr']) for b in struct_data if struct_data[b]['D_std'] > 0 and struct_data[b]['delta_std'] > 0]
        if corr_list:
            pos_corrs = [c for _, c in corr_list if c > 0.1]
            neg_corrs = [c for _, c in corr_list if c < -0.1]
            zero_corrs = [c for _, c in corr_list if -0.1 <= c <= 0.1]
            print(f"  Within-b correlations: {len(pos_corrs)} positive, {len(neg_corrs)} negative, {len(zero_corrs)} near-zero")

        # Plots for detailed primes
        plot_scatter_D_vs_delta(p, all_data, corr_data, FIG_DIR)
        plot_per_denom_anatomy(p, pd_results, cross_results, FIG_DIR)
        plot_within_denom_correlation(p, struct_data, FIG_DIR)

    # -------------------------------------------------------
    # Phase 2: Random comparison for selected primes
    # -------------------------------------------------------
    print("\n" + "=" * 60)
    print("PHASE 2: ACTUAL vs RANDOM PERMUTATION COMPARISON")
    print("=" * 60)

    random_primes = [13, 37, 97, 199, 307]
    random_primes = [p for p in random_primes if p in test_primes]

    for p in random_primes:
        t0 = time.time()
        fracs = farey_sequence(p - 1)
        by_denom, all_data, n = compute_D_delta(p, fracs)

        R_actual, R_random = random_comparison(p, fracs, n, n_trials=500)
        mean_rand, std_rand = plot_random_comparison(p, R_actual, R_random, FIG_DIR)

        elapsed = time.time() - t0
        z_score = (R_actual - mean_rand) / std_rand if std_rand > 0 else 0

        print(f"p={p:4d}: R_actual={R_actual:+.6f}, random mean={mean_rand:+.6f}, "
              f"std={std_rand:.6f}, z-score={z_score:+.2f} [{elapsed:.1f}s]")
        print(f"        |R_actual|={abs(R_actual):.6f} vs random |R| mean={np.mean(np.abs(R_random)):.6f}")

        # Is actual R unusually small?
        frac_smaller = np.mean(np.abs(R_random) < abs(R_actual))
        frac_larger = np.mean(np.abs(R_random) > abs(R_actual))
        print(f"        Fraction of random |R| < actual |R|: {frac_smaller:.3f}")
        print(f"        Fraction of random |R| > actual |R|: {frac_larger:.3f}")

    # -------------------------------------------------------
    # Phase 3: Summary across all primes
    # -------------------------------------------------------
    print("\n" + "=" * 60)
    print("PHASE 3: SUMMARY ACROSS ALL PRIMES up to 500")
    print("=" * 60)

    summary_primes = [p for p in test_primes if p <= 500]
    prime_data = []

    for p in summary_primes:
        N = p - 1
        fracs = farey_sequence(N)
        by_denom, all_data, n = compute_D_delta(p, fracs)

        pd_results = per_denom_cancellation(p, by_denom)
        cross_results = cross_denom_cancellation(pd_results)
        corr_data = correlation_analysis(all_data, n)

        sum_D_delta = sum(d['prod'] for d in all_data)
        sum_delta_sq = sum(d['delta']**2 for d in all_data)
        R = 2 * sum_D_delta / sum_delta_sq if sum_delta_sq > 0 else 0

        total_abs_terms = sum(abs(d['prod']) for d in all_data)
        sum_abs_Cb = sum(abs(pd_results[b]['C_b']) for b in pd_results)

        cancel_ratios = [pd_results[b]['cancel_ratio'] for b in pd_results if b > 1 and pd_results[b]['abs_sum'] > 0]
        avg_within = np.mean(cancel_ratios) if cancel_ratios else 0

        prime_data.append({
            'p': p,
            'M_p': M[p],
            'R_actual': R,
            'cs_ratio': corr_data['cs_ratio'],
            'pearson': corr_data['pearson_corr'],
            'within_cancel_avg': avg_within,
            'cross_cancel': cross_results['cross_cancel_ratio'],
            'total_abs_terms': total_abs_terms,
            'sum_abs_Cb': sum_abs_Cb,
            'abs_total_cross': abs(cross_results['total_cross']),
        })

    # Print summary table
    print(f"\n{'p':>5} {'M(p)':>5} {'R(p)':>10} {'CS%':>8} {'Pearson':>9} {'W-cancel':>9} {'X-cancel':>9}")
    print("-" * 65)
    for d in prime_data:
        print(f"{d['p']:5d} {d['M_p']:5d} {d['R_actual']:+10.6f} {d['cs_ratio']*100:7.3f}% "
              f"{d['pearson']:+9.6f} {d['within_cancel_avg']:9.4f} {d['cross_cancel']:9.4f}")

    # Summary statistics
    R_abs = [abs(d['R_actual']) for d in prime_data]
    cs_ratios = [d['cs_ratio'] for d in prime_data]

    print(f"\nSummary statistics:")
    print(f"  max |R| = {max(R_abs):.6f} at p={prime_data[np.argmax(R_abs)]['p']}")
    print(f"  mean |R| = {np.mean(R_abs):.6f}")
    print(f"  mean CS usage = {np.mean(cs_ratios)*100:.3f}%")
    print(f"  mean within-denom cancellation = {np.mean([d['within_cancel_avg'] for d in prime_data]):.4f}")
    print(f"  mean cross-denom cancellation = {np.mean([d['cross_cancel'] for d in prime_data]):.4f}")

    # Identify dominant cancellation mechanism
    within_savings = [1 - d['sum_abs_Cb'] / d['total_abs_terms'] if d['total_abs_terms'] > 0 else 0 for d in prime_data]
    cross_savings = [1 - d['abs_total_cross'] / d['sum_abs_Cb'] if d['sum_abs_Cb'] > 0 else 0 for d in prime_data]

    print(f"\n  CANCELLATION DECOMPOSITION:")
    print(f"  Within-denom reduces magnitude by: {np.mean(within_savings)*100:.1f}% on average")
    print(f"  Cross-denom reduces magnitude by: {np.mean(cross_savings)*100:.1f}% on average")
    print(f"  Combined reduction: {np.mean([1 - d['abs_total_cross']/d['total_abs_terms'] if d['total_abs_terms']>0 else 0 for d in prime_data])*100:.1f}%")

    # Summary plots
    plot_summary(prime_data, FIG_DIR)
    plot_cancellation_decomposition(prime_data, FIG_DIR)

    # -------------------------------------------------------
    # Phase 4: KEY MATHEMATICAL INSIGHT
    # -------------------------------------------------------
    print("\n" + "=" * 60)
    print("PHASE 4: STRUCTURAL EXPLANATION")
    print("=" * 60)

    # For p=13, do detailed term-by-term analysis
    p = 13
    fracs = farey_sequence(p - 1)
    by_denom, all_data, n = compute_D_delta(p, fracs)

    print(f"\nTerm-by-term for p={p}:")
    print(f"{'f':>8} {'b':>3} {'D(f)':>10} {'delta(f)':>10} {'D*delta':>10} {'sign':>5}")
    print("-" * 50)

    for d in all_data:
        if d['delta'] == 0:
            continue
        sign = '+' if d['prod'] > 0 else '-'
        print(f"{d['a']}/{d['b']:3d} {d['b']:3d} {d['D']:10.4f} {d['delta']:10.4f} {d['prod']:10.4f} {sign:>5}")

    # Check: does D depend mostly on b (not a) while delta depends on a mod structure?
    print(f"\nD(f) depends on GLOBAL position (rank - n*f)")
    print(f"delta(f) depends on LOCAL structure (a - pa mod b)/b")
    print(f"These are structurally independent: D sees all denominators, delta sees only one.")

    # Check the mean D per denominator
    print(f"\nMean D(f) per denominator for p={p}:")
    for b in sorted(by_denom.keys()):
        if b <= 1:
            continue
        entries = by_denom[b]
        D_mean = np.mean([e['D'] for e in entries])
        D_std = np.std([e['D'] for e in entries])
        delta_mean = np.mean([e['delta'] for e in entries])
        delta_std = np.std([e['delta'] for e in entries])
        print(f"  b={b:3d}: mean(D)={D_mean:+.4f}, std(D)={D_std:.4f}, "
              f"mean(delta)={delta_mean:+.6f}, std(delta)={delta_std:.4f}")

    # Key insight: delta sums to ~0 per denominator AND D is nearly constant per denom
    # So C_b = Sum_a D(a/b)*delta(a/b) ~ mean(D|b) * Sum_a delta(a/b) ~ 0
    print(f"\nKEY INSIGHT:")
    print(f"  delta(a/b) sums to ~0 for each denominator b (coprime permutation property)")
    print(f"  D(a/b) varies slowly with a for fixed b (smooth step function)")
    print(f"  Therefore C_b = Sum_a D(a/b)*delta(a/b) ~ mean_D(b) * Sum_a delta(a/b) ~ 0")
    print(f"  The residual |C_b| comes from the covariance of D's a-variation with delta")
    print(f"  This covariance is small because D's variation within a denom is ~O(phi(b))")
    print(f"  while delta's fluctuations are ~O(1/b), giving |C_b| ~ O(phi(b)/b)")

    # Quantify: for each b, how much of C_b is explained by mean(D)*sum(delta)?
    print(f"\nDecomposition: C_b = mean(D|b)*sum(delta|b) + cov_term")
    for b in sorted(by_denom.keys()):
        if b <= 1:
            continue
        entries = by_denom[b]
        D_mean = np.mean([e['D'] for e in entries])
        delta_sum = sum(e['delta'] for e in entries)
        C_b = sum(e['prod'] for e in entries)
        mean_term = D_mean * delta_sum
        cov_term = C_b - mean_term
        print(f"  b={b:3d}: C_b={C_b:+.6f}, mean*sum={mean_term:+.6f}, cov_term={cov_term:+.6f}")

    print(f"\nDone. Figures saved to {FIG_DIR}")
    print(f"Total time: {time.time() - time.time():.1f}s")
