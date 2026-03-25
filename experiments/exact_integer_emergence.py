#!/usr/bin/env python3
"""
EXACT INTEGER EMERGENCE FROM EXTREME SIGNAL-TO-NOISE
=====================================================

The bridge identity:
  Σ_{b=1}^{p} c_b(p) = M(p) + p

where c_b(p) = Σ_{a: gcd(a,b)=1} e^{2πi·a·p/b} is the Ramanujan sum.

This sums ~3p²/π² unit vectors (one for each coprime pair a/b with b<=p).
The b=p term contributes φ(p) = p-1 vectors summing to p-1.
The remaining b=1..p-1 terms contribute ~3p²/π² - (p-1) vectors
summing to M(p) + 1 = M(p-1) + μ(p) + 1 = M(p-1).

The REAL miracle is the b<p part:
  Σ_{b=1}^{p-1} c_b(p) = M(p-1) = M(p) + 1
  (using M(p) = M(p-1) + μ(p) = M(p-1) - 1 for prime p)

For p=97: ~2806 vectors → sum = M(96) = M(97)+1 = 2.
Signal = 2, noise floor = 2804. SNR ≈ -63 dB. EXACT INTEGER.

This script investigates:
1. PERTURBATION SENSITIVITY — move one Farey fraction by ε
2. ALGEBRAIC vs RANDOM CANCELLATION — compare structured vs random
3. ROLE OF MULTIPLICATIVITY — randomize μ(b) and see what breaks
4. WHICH DENOMINATORS CANCEL MOST — find largest φ(b) with |μ(b)|=1
5. VISUALIZATION — show all vectors for p=11 colored by denominator
"""

import numpy as np
from math import gcd, pi, sqrt, log2, log10
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# ================================================================
# CORE NUMBER THEORY
# ================================================================

def mobius_sieve(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def euler_totient(n):
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

def mertens(n, mu):
    return sum(mu[1:n+1])

def ramanujan_sum(b, n):
    """Compute c_b(n) numerically."""
    total = 0.0 + 0.0j
    for a in range(1, b + 1):
        if gcd(a, b) == 1:
            total += np.exp(2j * pi * a * n / b)
    return total

def bridge_vectors_grouped(p):
    """Return all unit vectors grouped by denominator b.
    Returns dict: b -> list of (a, complex_value)."""
    groups = defaultdict(list)
    for b in range(1, p + 1):
        for a in range(1, b + 1):
            if gcd(a, b) == 1:
                v = np.exp(2j * pi * a * p / b)
                groups[b].append((a, v))
    return groups

# ================================================================
# INVESTIGATION 1: PERTURBATION SENSITIVITY
# ================================================================

def investigate_perturbation():
    print("=" * 70)
    print("INVESTIGATION 1: PERTURBATION SENSITIVITY")
    print("=" * 70)

    mu = mobius_sieve(200)
    results = {}

    for p in [7, 11, 23, 53, 97]:
        groups = bridge_vectors_grouped(p)
        all_vecs = [(b, a, v) for b in groups for a, v in groups[b]]
        n = len(all_vecs)
        exact_sum = sum(v for _, _, v in all_vecs)
        M_val = mertens(p, mu)

        # Exclude b=p to isolate the "miraculous" part
        vecs_no_p = [(b, a, v) for b, a, v in all_vecs if b != p]
        n_no_p = len(vecs_no_p)
        sum_no_p = sum(v for _, _, v in vecs_no_p)

        # Per-vector sensitivity: perturb one phase by ε
        # |d/dε e^{2πi(θ+ε)}| = 2π, so each vector contributes exactly 2π sensitivity
        eps = 1e-6
        max_change = 0
        for idx in range(min(n_no_p, 300)):
            b, a, v_orig = vecs_no_p[idx]
            v_pert = np.exp(2j * pi * (a * p / b + eps))
            change = abs(v_pert - v_orig)
            if change > max_change:
                max_change = change

        # Aggregate sensitivity: if ALL fractions shift by ε simultaneously
        agg_sensitivity = 2 * pi * n_no_p

        results[p] = {
            'n_total': n,
            'n_miraculous': n_no_p,
            'sum_total': float(exact_sum.real),
            'sum_miraculous': float(sum_no_p.real),
            'expected_total': M_val + p,
            'expected_miraculous': M_val + 1,  # M(p-1) for prime p
            'per_vector_sensitivity': 2 * pi,
            'aggregate_sensitivity': agg_sensitivity,
        }

        print(f"\np = {p}:")
        print(f"  Total: {n} vectors → sum = {exact_sum.real:.1f} (expect M({p})+{p} = {M_val + p})")
        print(f"  b<p:   {n_no_p} vectors → sum = {sum_no_p.real:.1f} (expect M({p})+1 = {M_val + 1})")
        print(f"  Per-vector sensitivity: 2π ≈ {2*pi:.4f}")
        print(f"  Aggregate sensitivity (all b<p shifted): 2π·{n_no_p} = {agg_sensitivity:.0f}")
        print(f"  SNR of miraculous part: {20*log10(max(abs(M_val+1), 0.5)/n_no_p):.1f} dB")

    print(f"\n{'─'*70}")
    print("INSIGHT: Each vector has sensitivity 2π. The aggregate sensitivity")
    print("2π·n is huge (~18000 for p=97). Yet the sum is an exact integer.")
    print("A random perturbation of ALL fractions by ε would destroy the")
    print("integer by ~2π·√n·ε (random walk of n perturbations of size 2πε).")
    print("This means the integer structure is FRAGILE to random noise")
    print("but PERFECTLY MAINTAINED by the algebraic relationships.")

    return results

# ================================================================
# INVESTIGATION 2: ALGEBRAIC vs RANDOM CANCELLATION
# ================================================================

def investigate_algebraic_vs_random():
    print("\n" + "=" * 70)
    print("INVESTIGATION 2: ALGEBRAIC vs RANDOM CANCELLATION")
    print("=" * 70)

    np.random.seed(42)
    n_trials = 10000
    mu = mobius_sieve(200)
    results = {}

    primes = [7, 11, 13, 23, 37, 53, 67, 97]

    for p in primes:
        groups = bridge_vectors_grouped(p)
        # Focus on the b<p part (the miraculous cancellation)
        vecs_no_p = []
        for b in groups:
            if b != p:
                for a, v in groups[b]:
                    vecs_no_p.append(v)
        n = len(vecs_no_p)
        alg_sum = sum(vecs_no_p)
        alg_mag = abs(alg_sum)
        M_val = mertens(p, mu)
        expected = M_val + 1  # = M(p-1) for prime p

        # Random: n uniform random unit vectors
        random_mags = []
        for _ in range(n_trials):
            phases = np.random.uniform(0, 2*pi, n)
            s = abs(np.sum(np.exp(1j * phases)))
            random_mags.append(s)
        random_mags = np.array(random_mags)

        # Rayleigh stats
        rayleigh_mean = sqrt(pi * n / 2)
        rayleigh_std = sqrt(n * (4 - pi) / 2)

        snr_alg = 20 * log10(max(alg_mag, 0.1) / n)
        snr_rand = 20 * log10(rayleigh_mean / n)

        # How often does random beat algebraic?
        frac_below = np.mean(random_mags <= alg_mag) if alg_mag > 0 else 0

        results[p] = {
            'n': n,
            'alg_mag': float(alg_mag),
            'alg_value': float(alg_sum.real),
            'expected': expected,
            'random_mean': float(np.mean(random_mags)),
            'random_std': float(np.std(random_mags)),
            'sqrt_n': float(sqrt(n)),
            'snr_alg_dB': float(snr_alg),
            'snr_rand_dB': float(snr_rand),
            'snr_gap_dB': float(snr_alg - snr_rand),
            'percentile': float(100 * frac_below),
        }

        print(f"\np = {p}: n = {n} vectors (b < p only)")
        print(f"  Algebraic |sum| = {alg_mag:.4f} (value = {alg_sum.real:.1f}, expected {expected})")
        print(f"  Random E[|sum|] = {np.mean(random_mags):.2f} ± {np.std(random_mags):.2f}")
        print(f"  √n = {sqrt(n):.2f}")
        print(f"  SNR algebraic: {snr_alg:.1f} dB")
        print(f"  SNR random:    {snr_rand:.1f} dB")
        print(f"  Gap:           {snr_alg - snr_rand:.1f} dB")
        print(f"  Algebraic at {100*frac_below:.2f}th percentile of random")

    return results


# ================================================================
# INVESTIGATION 3: ROLE OF MULTIPLICATIVITY
# ================================================================

def investigate_multiplicativity():
    print("\n" + "=" * 70)
    print("INVESTIGATION 3: ROLE OF MULTIPLICATIVITY")
    print("=" * 70)

    np.random.seed(42)
    mu = mobius_sieve(200)
    results = {}

    for p in [7, 11, 23, 53, 97]:
        M_val = mertens(p, mu)
        true_sum_no_p = M_val + 1  # M(p-1)

        # The sum over b=1..p-1 of c_b(p):
        # For prime p, gcd(b,p)=1 for all b<p, so c_b(p) = μ(b).
        # Thus the sum = Σ_{b=1}^{p-1} μ(b) = M(p-1) = M(p) + 1.
        #
        # With random μ: Σ random_μ(b) for squarefree b, 0 for others
        # = Σ_{b squarefree, b<p} (±1 random)

        squarefree_b = [b for b in range(1, p) if mu[b] != 0]
        n_sqfree = len(squarefree_b)

        n_trials = 50000
        random_sums = []
        for _ in range(n_trials):
            s = sum(np.random.choice([-1, 1]) for _ in squarefree_b)
            random_sums.append(s)
        random_sums = np.array(random_sums)

        results[p] = {
            'true_sum': true_sum_no_p,
            'n_squarefree': n_sqfree,
            'random_mean': float(np.mean(random_sums)),
            'random_std': float(np.std(random_sums)),
            'all_integers': True,  # always true: sum of ±1
            'z_score': float((true_sum_no_p - np.mean(random_sums)) / np.std(random_sums)),
        }

        percentile = 100 * np.mean(random_sums <= true_sum_no_p)
        print(f"\np = {p}: M(p-1) = {true_sum_no_p}")
        print(f"  Squarefree b < p: {n_sqfree}")
        print(f"  Random μ sums: mean={np.mean(random_sums):.2f}, std={np.std(random_sums):.2f}")
        print(f"  True value at z = {results[p]['z_score']:.2f}")
        print(f"  100% are integers (sum of ±1 is always integer)")
        print(f"  KEY: Integrality is STRUCTURAL. Smallness of M(p) requires REAL μ.")

    print(f"\n{'─'*70}")
    print("INSIGHT: Two separate phenomena:")
    print("  1) INTEGRALITY: Guaranteed by Ramanujan sum structure (c_b always integer)")
    print("  2) SMALLNESS: M(p) ~ O(√p) requires the specific multiplicative")
    print("     correlations of μ. Random ±1 gives |sum| ~ √n_sqfree ~ √(6p/π²).")

    return results


# ================================================================
# INVESTIGATION 4: WHICH DENOMINATORS CANCEL MOST
# ================================================================

def investigate_denominators():
    print("\n" + "=" * 70)
    print("INVESTIGATION 4: DENOMINATOR CANCELLATION ANALYSIS")
    print("=" * 70)

    mu = mobius_sieve(200)
    results = {}

    for p in [23, 53, 97]:
        data = []
        for b in range(1, p):  # b < p only
            phi_b = euler_totient(b)
            cb = round(ramanujan_sum(b, p).real)  # = μ(b) for prime p
            data.append({
                'b': b,
                'phi_b': phi_b,
                'mu_b': mu[b],
                'c_b': cb,
                'cancel_ratio': phi_b / max(abs(cb), 1),
            })

        data.sort(key=lambda x: x['cancel_ratio'], reverse=True)
        results[p] = data

        print(f"\np = {p}: Top cancellers (b < p, sorted by φ(b)/|c_b|)")
        print(f"  {'b':>4} {'φ(b)':>6} {'μ(b)':>5} {'c_b':>5} {'φ(b)/|c_b|':>10}")
        for d in data[:12]:
            print(f"  {d['b']:>4} {d['phi_b']:>6} {d['mu_b']:>5} {d['c_b']:>5} {d['cancel_ratio']:>10.1f}")

        # b with μ(b)=0 give c_b=0: perfect cancellation of φ(b) vectors
        perfect = [d for d in data if d['c_b'] == 0 and d['phi_b'] > 0]
        near_perfect = [d for d in data if abs(d['c_b']) == 1 and d['phi_b'] >= 10]

        total_vecs = sum(d['phi_b'] for d in data)
        perfect_cancelled = sum(d['phi_b'] for d in perfect)
        near_perfect_vecs = sum(d['phi_b'] for d in near_perfect)

        print(f"\n  Total vectors (b<p): {total_vecs}")
        print(f"  Perfect cancellation (μ(b)=0): {perfect_cancelled} vectors from {len(perfect)} denominators")
        print(f"  Near-perfect (|c_b|=1, φ(b)>=10): {near_perfect_vecs} vectors from {len(near_perfect)} denominators")
        print(f"  Most impressive: b={data[0]['b']}, φ(b)={data[0]['phi_b']} vectors → c_b={data[0]['c_b']}")

    return results


# ================================================================
# INVESTIGATION 5: VISUALIZATIONS
# ================================================================

def vis_p11_anatomy():
    """Detailed anatomy of cancellation for p=11."""
    print("\n" + "=" * 70)
    print("INVESTIGATION 5: VISUALIZATION FOR p=11")
    print("=" * 70)

    p = 11
    mu = mobius_sieve(20)
    M_val = mertens(p, mu)
    groups = bridge_vectors_grouped(p)

    total_sum = sum(v for b in groups for _, v in groups[b])
    sum_no_p = sum(v for b in groups if b != p for _, v in groups[b])
    n_total = sum(len(vs) for vs in groups.values())
    n_no_p = sum(len(vs) for b, vs in groups.items() if b != p)

    print(f"p = {p}, M({p}) = {M_val}")
    print(f"Full sum: {total_sum.real:.6f} (expect M+p = {M_val + p})")
    print(f"b<p sum:  {sum_no_p.real:.6f} (expect M+1 = {M_val + 1})")
    print(f"Vectors: {n_total} total, {n_no_p} with b<p")

    print(f"\nPer-denominator:")
    print(f"  {'b':>3} {'φ(b)':>5} {'μ(b)':>5} {'c_b':>6} {'phases':>40}")
    for b in sorted(groups.keys()):
        vs = groups[b]
        group_sum = sum(v for _, v in vs)
        phases_str = ', '.join(f'{a}/{b}' for a, _ in vs)
        print(f"  {b:>3} {len(vs):>5} {mu[b] if b <= len(mu)-1 else '?':>5} "
              f"{group_sum.real:>6.1f}   {phases_str}")

    # ── FIGURE: Three-panel anatomy ──
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    cmap = plt.cm.tab20
    all_b = sorted(groups.keys())
    colors = {b: cmap(i / max(len(all_b), 1)) for i, b in enumerate(all_b)}

    # Panel 1: All vectors on unit circle, colored by b
    ax = axes[0]
    theta = np.linspace(0, 2*pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.2, lw=0.5)
    ax.axhline(0, color='k', alpha=0.1); ax.axvline(0, color='k', alpha=0.1)

    for b in all_b:
        if b == p:
            continue  # skip b=p for clarity
        xs = [v.real for _, v in groups[b]]
        ys = [v.imag for _, v in groups[b]]
        ax.scatter(xs, ys, c=[colors[b]], s=40, label=f'b={b} (c={round(sum(v for _,v in groups[b]).real)})',
                   zorder=3, edgecolors='k', linewidth=0.3)

    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_title(f'{n_no_p} vectors (b<{p}) on unit circle', fontsize=11)
    ax.legend(fontsize=6, loc='upper left', ncol=2)

    # Panel 2: Ramanujan sums as arrows from origin
    ax = axes[1]
    ax.axhline(0, color='k', alpha=0.2); ax.axvline(0, color='k', alpha=0.2)

    for b in all_b:
        gs = sum(v for _, v in groups[b])
        phi_b = len(groups[b])
        ax.annotate('', xy=(gs.real, gs.imag), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color=colors[b], lw=2.5))
        offset_y = 0.2 if gs.imag >= 0 else -0.4
        ax.text(gs.real, gs.imag + offset_y, f'b={b}\nc={round(gs.real)}\nφ={phi_b}',
                fontsize=6, ha='center', color=colors[b], fontweight='bold')

    ax.set_xlim(-2, 11); ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_title(f'Ramanujan sums c_b({p})', fontsize=11)

    # Panel 3: Cumulative sum walk (b<p only)
    ax = axes[2]
    ax.axhline(0, color='k', alpha=0.2); ax.axvline(0, color='k', alpha=0.2)

    cum = 0.0 + 0.0j
    for b in all_b:
        if b == p:
            continue
        gs = sum(v for _, v in groups[b])
        prev = cum
        cum += gs
        ax.annotate('', xy=(cum.real, cum.imag), xytext=(prev.real, prev.imag),
                     arrowprops=dict(arrowstyle='->', color=colors[b], lw=2))
        mid = (prev + cum) / 2
        ax.text(mid.real, mid.imag + 0.15, f'b={b}', fontsize=6, ha='center', color=colors[b])

    ax.plot(0, 0, 'ko', ms=8, zorder=5, label='Start')
    ax.plot(cum.real, cum.imag, 'r*', ms=15, zorder=5,
            label=f'End = {cum.real:.1f} = M({p-1})')
    ax.legend(fontsize=9)
    ax.set_aspect('equal')
    ax.set_title(f'Cumulative walk (b<{p}): {n_no_p} vecs → {cum.real:.1f}', fontsize=11)

    plt.suptitle(f'Anatomy of cancellation for p={p}: '
                 f'{n_no_p} vectors (b<p) sum to M({p-1}) = {M_val+1}',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig_cancellation_p11_anatomy.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")


def vis_snr_comparison():
    """SNR: algebraic vs random across primes."""
    print("\n── SNR comparison figure ──")

    np.random.seed(42)
    mu = mobius_sieve(200)
    primes = [5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

    p_list, snr_alg, snr_rand, n_list, alg_mag_list = [], [], [], [], []

    for p in primes:
        groups = bridge_vectors_grouped(p)
        n = sum(len(vs) for b, vs in groups.items() if b != p)
        alg = abs(sum(v for b in groups if b != p for _, v in groups[b]))
        M_val = mertens(p, mu)
        rayleigh = sqrt(pi * n / 2)

        p_list.append(p)
        n_list.append(n)
        alg_mag_list.append(alg)
        snr_alg.append(20*log10(max(alg, 0.1)/n))
        snr_rand.append(20*log10(rayleigh/n))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax = axes[0]
    ax.plot(p_list, snr_alg, 'ro-', ms=5, lw=1.5, label='Algebraic |M(p-1)|')
    ax.plot(p_list, snr_rand, 'b^--', ms=5, lw=1.5, label='Random E[|sum|]')
    ax.fill_between(p_list, snr_alg, snr_rand, alpha=0.15, color='green')
    ax.set_xlabel('Prime p'); ax.set_ylabel('SNR (dB)')
    ax.set_title('SNR: Algebraic vs Random (b<p part)', fontsize=12)
    ax.legend(); ax.grid(True, alpha=0.3)

    mid = len(p_list)//2
    gap = snr_rand[mid] - snr_alg[mid]
    ax.annotate(f'Gap ~ {gap:.0f} dB\n= multiplicative\nstructure',
                xy=(p_list[mid], (snr_alg[mid]+snr_rand[mid])/2),
                fontsize=9, ha='center', color='green', fontweight='bold')

    ax = axes[1]
    ax.semilogy(p_list, n_list, 'ks--', ms=4, lw=1, alpha=0.5, label='n (vectors)')
    rands = [sqrt(pi*n/2) for n in n_list]
    ax.semilogy(p_list, rands, 'b^--', ms=5, lw=1.5, label='Random √(πn/2)')
    ax.semilogy(p_list, [max(m, 0.5) for m in alg_mag_list], 'ro-', ms=5, lw=1.5,
                label='Algebraic |M(p-1)|')
    ax.set_xlabel('Prime p'); ax.set_ylabel('Magnitude')
    ax.set_title('Magnitudes: n vectors, random expectation, algebraic result', fontsize=12)
    ax.legend(); ax.grid(True, alpha=0.3)

    plt.suptitle('The -60 dB miracle: algebraic cancellation far exceeds random',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig_cancellation_snr_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")


def vis_denominator_heatmap():
    """Bar chart of φ(b) vs c_b for several primes."""
    print("── Denominator cancellation figure ──")

    mu = mobius_sieve(200)
    primes_to_show = [11, 23, 37, 53, 67, 97]

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    for idx, p in enumerate(primes_to_show):
        ax = axes[idx//3][idx%3]
        bs = list(range(1, p))  # b < p
        phis = [euler_totient(b) for b in bs]
        cbs = [round(ramanujan_sum(b, p).real) for b in bs]
        mus = [mu[b] for b in bs]

        bar_colors = []
        for i in range(len(bs)):
            if mus[i] == 0:
                bar_colors.append('green')     # c_b=0: perfect cancel
            elif mus[i] == -1:
                bar_colors.append('steelblue')  # c_b=-1
            else:
                bar_colors.append('coral')      # c_b=+1

        ax.bar(bs, phis, color=bar_colors, alpha=0.7, width=0.8)
        ax.bar(bs, [abs(c) for c in cbs], color='black', alpha=0.5, width=0.3)

        total_v = sum(phis)
        final = sum(cbs)
        ax.set_xlabel('Denominator b')
        ax.set_ylabel('Vectors / Result')
        ax.set_title(f'p={p}: {total_v} vectors → {final} = M({p-1})', fontsize=10)

        if idx == 0:
            from matplotlib.patches import Patch
            legend = [
                Patch(facecolor='steelblue', alpha=0.7, label='μ(b)=-1, c_b=-1'),
                Patch(facecolor='coral', alpha=0.7, label='μ(b)=+1, c_b=+1'),
                Patch(facecolor='green', alpha=0.7, label='μ(b)=0, c_b=0'),
                Patch(facecolor='black', alpha=0.5, label='|c_b(p)| result'),
            ]
            ax.legend(handles=legend, fontsize=6)

    plt.suptitle('φ(b) vectors (tall bars) collapse to |c_b|=0 or 1 (tiny black bars)',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig_cancellation_denominator_heatmap.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")


def vis_random_histogram():
    """Histograms: random |sum| vs algebraic."""
    print("── Random vs algebraic histogram ──")

    np.random.seed(42)
    mu = mobius_sieve(200)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for idx, p in enumerate([11, 53, 97]):
        ax = axes[idx]
        groups = bridge_vectors_grouped(p)
        n = sum(len(vs) for b, vs in groups.items() if b != p)
        alg_sum = sum(v for b in groups if b != p for _, v in groups[b])
        alg_mag = abs(alg_sum)
        M_val = mertens(p, mu)

        mags = []
        for _ in range(20000):
            s = abs(np.sum(np.exp(1j * np.random.uniform(0, 2*pi, n))))
            mags.append(s)
        mags = np.array(mags)

        ax.hist(mags, bins=80, density=True, alpha=0.7, color='steelblue', label=f'Random (n={n})')
        ax.axvline(alg_mag, color='red', lw=3, label=f'Algebraic = {alg_mag:.1f}')
        ax.axvline(sqrt(n), color='orange', lw=2, ls='--', label=f'sqrt(n)={sqrt(n):.1f}')

        pctl = 100 * np.mean(mags <= alg_mag)
        ax.set_xlabel('|sum|'); ax.set_ylabel('Density')
        ax.set_title(f'p={p}: n={n}, M({p-1})={M_val+1}', fontsize=11)
        ax.legend(fontsize=8)

        if alg_mag < mags.min():
            ax.annotate(f'Algebraic\noff-chart\nleft!', xy=(mags.min(), 0),
                        fontsize=8, color='red', ha='left')
        else:
            ax.annotate(f'{pctl:.1f}th pctl', xy=(alg_mag, 0), fontsize=8,
                        color='red', ha='right')

    plt.suptitle('Random walk distribution vs algebraic result (b<p vectors)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig_cancellation_random_vs_algebraic.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")


def vis_multiplicativity_scramble():
    """What happens when μ is randomized?"""
    print("── Multiplicativity scramble figure ──")

    np.random.seed(42)
    mu = mobius_sieve(200)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for idx, p in enumerate([11, 53, 97]):
        ax = axes[idx]
        M_val = mertens(p, mu)
        true_val = M_val + 1  # M(p-1)

        sqfree = [b for b in range(1, p) if mu[b] != 0]
        n_sq = len(sqfree)

        sums = np.array([sum(np.random.choice([-1,1]) for _ in sqfree) for _ in range(50000)])

        lo, hi = int(sums.min())-1, int(sums.max())+2
        ax.hist(sums, bins=range(lo, hi), density=True, alpha=0.7, color='steelblue',
                label=f'Random μ (n_sq={n_sq})')
        ax.axvline(true_val, color='red', lw=3, label=f'True M({p-1})={true_val}')

        z = (true_val - np.mean(sums)) / np.std(sums)
        ax.set_xlabel('Σ random_μ(b)'); ax.set_ylabel('Density')
        ax.set_title(f'p={p}: z-score = {z:.2f}', fontsize=11)
        ax.legend(fontsize=8)

    plt.suptitle('Randomizing μ: sums stay integer, but M(p) requires the real Mobius function',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig_cancellation_multiplicativity_scramble.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")


# ================================================================
# MAIN
# ================================================================

if __name__ == '__main__':
    print("EXACT INTEGER EMERGENCE FROM EXTREME SNR")
    print("=" * 70)

    r1 = investigate_perturbation()
    r2 = investigate_algebraic_vs_random()
    r3 = investigate_multiplicativity()
    r4 = investigate_denominators()

    vis_p11_anatomy()
    vis_snr_comparison()
    vis_denominator_heatmap()
    vis_random_histogram()
    vis_multiplicativity_scramble()

    print("\n" + "=" * 70)
    print("GRAND SUMMARY: WHY EXACT INTEGERS EMERGE")
    print("=" * 70)
    print("""
CORRECTED IDENTITY:
  Σ_{b=1}^{p} c_b(p) = M(p) + p

Decomposition:
  b = p:   contributes φ(p) = p-1 vectors summing to p-1 (trivial)
  b < p:   contributes ~3p²/π² - (p-1) vectors summing to M(p-1) = M(p)+1

THE MIRACLE is in the b<p part:
  ~3p²/π² vectors cancel down to M(p)+1, which is O(√p) under RH.

THREE LAYERS OF STRUCTURE:

1. RAMANUJAN SUM STRUCTURE → INTEGRALITY
   c_b(n) is always an integer (Ramanujan's theorem).
   For prime p with b<p: c_b(p) = μ(b) ∈ {-1, 0, +1}.
   This is WHY the sum is an exact integer.

2. MULTIPLICATIVE CORRELATIONS → SMALLNESS
   M(p) = Σ μ(k) is small because μ is multiplicative.
   The prime factorization structure forces global cancellation.
   Random ±1 on squarefree b would give |sum| ~ √(6p/π²).
   The real μ gives |M(p)| ~ O(√p log p), same order but SPECIFIC.

3. PER-DENOMINATOR CANCELLATION → THE -60 dB
   Within denominator b, φ(b) unit vectors sum to μ(b) ∈ {-1,0,+1}.
   For b=89 (prime), 88 unit vectors sum to -1: a 88:1 cancellation!
   For b=90 (non-squarefree), 24 vectors sum to exactly 0.
   This is possible because the vectors are primitive roots of unity,
   not random phases.

The "noise" is not noise — it is algebraically determined structure
that cancels PERFECTLY, not statistically.
""")

    print("Figures saved to figures/fig_cancellation_*.png")
    print("Done!")
