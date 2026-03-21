#!/usr/bin/env python3
"""
Per-Prime Wobble Reduction Analysis
====================================

This experiment measures how each individual prime reduces the Farey discrepancy
(the "wobble" — deviation from uniform distribution on the circle).

WHAT WE'RE LOOKING FOR:
- When prime p is added to the Farey sequence F_p (going from F_{p-1} to F_p),
  how much does the wobble decrease?
- Is there a pattern in the per-prime wobble reduction?
- Does it correlate with known prime properties (gaps, twin primes, etc.)?
- Can we discover a new conjecture?

THE WOBBLE:
W(N) = Σ |f_j - j/|F_N||²  where f_j are Farey fractions in order.
This is the Franel-Landau discrepancy — the quantity that the Riemann Hypothesis controls.

THE PER-PRIME REDUCTION:
ΔW(p) = W(p-1) - W(p)  for each prime p.
This measures how much each prime "improves" the uniform distribution.
Nobody has systematically studied this decomposition.
"""

import numpy as np
from math import gcd
from fractions import Fraction
import json
import os

def euler_totient(n):
    """Compute φ(n)."""
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

def farey_sequence(N):
    """Generate Farey sequence F_N as sorted list of Fraction objects."""
    fracs = set()
    for q in range(1, N + 1):
        for p in range(0, q + 1):
            if gcd(p, q) == 1:
                fracs.add(Fraction(p, q))
    return sorted(fracs)

def wobble_squared(farey_fracs):
    """Compute the wobble W(N) = Σ |f_j - j/|F_N||²."""
    size = len(farey_fracs)
    if size == 0:
        return Fraction(0)
    total = Fraction(0)
    for j, f in enumerate(farey_fracs):
        ideal = Fraction(j, size)
        delta = f - ideal
        total += delta * delta
    return total

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def sieve_primes(limit):
    """Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def run_wobble_experiment(max_N=200, output_dir=None):
    """
    Compute wobble W(N) for N = 2..max_N and per-prime reduction ΔW(p).

    For each N, we compute the full Farey sequence and its wobble.
    For primes p, we compute ΔW(p) = W(p-1) - W(p).
    """
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"Computing Farey wobble for N = 2..{max_N}")
    print("=" * 60)

    primes = sieve_primes(max_N)

    # Compute wobble for each N
    wobbles = {}  # N -> W(N) as float
    wobbles_exact = {}  # N -> W(N) as Fraction

    # Build Farey sequences incrementally
    farey_set = {Fraction(0, 1), Fraction(1, 1)}  # F_1

    for N in range(1, max_N + 1):
        # Add new fractions with denominator exactly N
        for p in range(1, N):
            if gcd(p, N) == 1:
                farey_set.add(Fraction(p, N))

        farey_sorted = sorted(farey_set)
        w = wobble_squared(farey_sorted)
        wobbles_exact[N] = w
        wobbles[N] = float(w)

        if N <= 30 or N % 10 == 0 or is_prime(N):
            print(f"  N={N:4d}  |F_N|={len(farey_sorted):6d}  W(N)={float(w):.10f}"
                  f"  {'PRIME' if is_prime(N) else ''}")

    # Compute per-prime wobble reduction
    print("\n" + "=" * 60)
    print("Per-prime wobble reduction ΔW(p) = W(p-1) - W(p)")
    print("=" * 60)

    prime_data = []
    for i, p in enumerate(primes):
        if p > max_N:
            break
        dw = wobbles[p - 1] - wobbles[p]
        dw_exact = wobbles_exact[p - 1] - wobbles_exact[p]

        # Compute prime gap
        gap = primes[i] - primes[i - 1] if i > 0 else 0

        # Is this a twin prime?
        is_twin = (i > 0 and gap == 2) or (i < len(primes) - 1 and primes[i + 1] - p == 2)

        # Normalized reduction: ΔW(p) * |F_p|²  (removes the trivial scaling)
        farey_size = 1 + sum(euler_totient(k) for k in range(1, p + 1))
        normalized_dw = dw * farey_size * farey_size

        # φ(p) = p-1 for prime p.
        # The "naive" prediction: ΔW(p) ≈ (p-1) / |F_p|²
        naive_prediction = (p - 1) / (farey_size * farey_size) if farey_size > 0 else 0
        ratio_to_naive = dw / naive_prediction if naive_prediction > 0 else float('inf')

        entry = {
            'prime': p,
            'index': i,
            'gap_from_prev': gap,
            'is_twin': is_twin,
            'phi_p': p - 1,
            'farey_size': farey_size,
            'wobble_before': wobbles[p - 1],
            'wobble_after': wobbles[p],
            'delta_w': dw,
            'normalized_dw': normalized_dw,
            'naive_prediction': naive_prediction,
            'ratio_to_naive': ratio_to_naive,
        }
        prime_data.append(entry)

        if p <= 50 or p % 20 < 3:
            print(f"  p={p:4d}  ΔW={dw:+.10f}  normalized={normalized_dw:.6f}"
                  f"  ratio={ratio_to_naive:.4f}  gap={gap:2d}"
                  f"  {'TWIN' if is_twin else ''}")

    # Analysis
    print("\n" + "=" * 60)
    print("ANALYSIS")
    print("=" * 60)

    deltas = [d['delta_w'] for d in prime_data if d['delta_w'] != 0]
    normalized = [d['normalized_dw'] for d in prime_data]
    ratios = [d['ratio_to_naive'] for d in prime_data if d['ratio_to_naive'] != float('inf')]

    if deltas:
        print(f"\n  All ΔW(p) positive (wobble always decreases)? {all(d > 0 for d in deltas)}")
        print(f"  Mean ΔW(p): {np.mean(deltas):.10f}")
        print(f"  Std  ΔW(p): {np.std(deltas):.10f}")

    if normalized:
        print(f"\n  Mean normalized ΔW: {np.mean(normalized):.6f}")
        print(f"  Std  normalized ΔW: {np.std(normalized):.6f}")

    if ratios:
        print(f"\n  Mean ratio to naive prediction: {np.mean(ratios):.6f}")
        print(f"  Std  ratio to naive prediction: {np.std(ratios):.6f}")
        print(f"  Min  ratio: {np.min(ratios):.6f}")
        print(f"  Max  ratio: {np.max(ratios):.6f}")

    # Twin prime analysis
    twin_ratios = [d['ratio_to_naive'] for d in prime_data if d['is_twin'] and d['ratio_to_naive'] != float('inf')]
    non_twin_ratios = [d['ratio_to_naive'] for d in prime_data if not d['is_twin'] and d['ratio_to_naive'] != float('inf')]

    if twin_ratios and non_twin_ratios:
        print(f"\n  Twin prime mean ratio:     {np.mean(twin_ratios):.6f} (n={len(twin_ratios)})")
        print(f"  Non-twin prime mean ratio: {np.mean(non_twin_ratios):.6f} (n={len(non_twin_ratios)})")
        diff = np.mean(twin_ratios) - np.mean(non_twin_ratios)
        print(f"  Difference: {diff:+.6f}")

    # Correlation with prime gap
    if len(prime_data) > 5:
        gaps = [d['gap_from_prev'] for d in prime_data[1:]]  # skip first (no prev gap)
        delta_vals = [d['normalized_dw'] for d in prime_data[1:]]
        corr = np.corrcoef(gaps, delta_vals)[0, 1]
        print(f"\n  Correlation(gap, normalized ΔW): {corr:.6f}")

    # Look for power law: does ΔW(p) ~ p^α ?
    if len(prime_data) > 10:
        log_p = np.log([d['prime'] for d in prime_data[2:]])
        log_dw = np.log([abs(d['delta_w']) for d in prime_data[2:] if d['delta_w'] > 0])
        if len(log_p) == len(log_dw):
            coeffs = np.polyfit(log_p, log_dw, 1)
            print(f"\n  Power law fit: ΔW(p) ≈ C · p^{coeffs[0]:.4f}")
            print(f"  (RH predicts the total wobble ~ N^(-1+ε), suggesting individual ΔW ~ p^(-3+ε))")

    # Save data
    output_file = os.path.join(output_dir, "wobble_data.json")
    with open(output_file, 'w') as f:
        json.dump(prime_data, f, indent=2, default=str)
    print(f"\n  Data saved to {output_file}")

    return prime_data


def plot_wobble_results(prime_data, output_dir=None):
    """Generate plots of the wobble analysis."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    primes = [d['prime'] for d in prime_data]
    deltas = [d['delta_w'] for d in prime_data]
    normalized = [d['normalized_dw'] for d in prime_data]
    ratios = [d['ratio_to_naive'] for d in prime_data]
    gaps = [d['gap_from_prev'] for d in prime_data]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Per-Prime Wobble Reduction Analysis', fontsize=14, fontweight='bold')

    # Plot 1: Raw wobble reduction by prime
    ax = axes[0, 0]
    ax.semilogy(primes, deltas, 'b.', markersize=3, alpha=0.7)
    ax.set_xlabel('Prime p')
    ax.set_ylabel('ΔW(p)')
    ax.set_title('Wobble Reduction per Prime')
    ax.grid(True, alpha=0.3)

    # Plot 2: Normalized wobble reduction
    ax = axes[0, 1]
    ax.plot(primes, normalized, 'r.', markersize=3, alpha=0.7)
    ax.set_xlabel('Prime p')
    ax.set_ylabel('ΔW(p) · |F_p|²')
    ax.set_title('Normalized Wobble Reduction')
    ax.grid(True, alpha=0.3)

    # Plot 3: Ratio to naive prediction
    ax = axes[1, 0]
    twin_p = [d['prime'] for d in prime_data if d['is_twin']]
    twin_r = [d['ratio_to_naive'] for d in prime_data if d['is_twin']]
    nontwin_p = [d['prime'] for d in prime_data if not d['is_twin']]
    nontwin_r = [d['ratio_to_naive'] for d in prime_data if not d['is_twin']]
    ax.plot(nontwin_p, nontwin_r, 'b.', markersize=3, alpha=0.5, label='Non-twin')
    ax.plot(twin_p, twin_r, 'r.', markersize=5, alpha=0.8, label='Twin prime')
    ax.set_xlabel('Prime p')
    ax.set_ylabel('Ratio to naive prediction')
    ax.set_title('Actual / Predicted Wobble Reduction')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 4: Gap vs normalized wobble reduction
    ax = axes[1, 1]
    colors = ['red' if d['is_twin'] else 'blue' for d in prime_data[1:]]
    ax.scatter(gaps[1:], normalized[1:], c=colors, s=5, alpha=0.5)
    ax.set_xlabel('Gap from previous prime')
    ax.set_ylabel('Normalized ΔW(p)')
    ax.set_title('Prime Gap vs Wobble Reduction')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plot_file = os.path.join(output_dir, "wobble_analysis.png")
    plt.savefig(plot_file, dpi=150)
    print(f"  Plot saved to {plot_file}")
    plt.close()


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    data = run_wobble_experiment(max_N=200, output_dir=output_dir)
    plot_wobble_results(data, output_dir=output_dir)
