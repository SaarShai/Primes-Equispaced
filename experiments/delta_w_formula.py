#!/usr/bin/env python3
"""
Deriving an Exact Formula for ΔW(p) — Breakthrough C
=====================================================

Goal: Express ΔW(p) = W(p-1) - W(p) analytically.

SETUP:
  W(N) = Σ_{j=0}^{|F_N|-1} (f_j - j/|F_N|)²
       = Σ f_j² - (2/|F_N|) Σ j·f_j + (1/|F_N|²) Σ j²

Let n = |F_{p-1}|, m = φ(p) = p-1 (new fractions from prime p).
So |F_p| = n + m = n + p - 1.

The new fractions are: k/p for k = 1, 2, ..., p-1 (all coprime to p since p is prime).
These get inserted at various positions in the sorted Farey sequence.

KEY DECOMPOSITION:
  W(N) = S2(N) - S1(N)²/|F_N| + Var_correction

where S2 = Σ f_j², S1 = Σ f_j = |F_N|/2 (by Farey symmetry).

Actually, let's use:
  W(N) = Σ (f_j - j/n)² = Σ f_j² - (2/n)Σ j·f_j + (1/n²)Σ j²

where n = |F_N| and the sums are over j = 0, ..., n-1.

We know:
  Σ j² = n(n-1)(2n-1)/6
  Σ f_j = n/2  (Farey symmetry)

So W(N) = Σ f_j² - (2/n)·R(N) + (n-1)(2n-1)/(6n)

where R(N) = Σ_{j=0}^{n-1} j·f_j is the "rank-weighted sum".

The question: how do Σ f_j² and R(N) change when we go from F_{p-1} to F_p?

Let's compute this EXACTLY for small primes and look for patterns.
"""

from fractions import Fraction
from math import gcd, sqrt
import csv
import os

def farey_sequence(N):
    """Return F_N as a sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def compute_wobble_exact(fracs):
    """Compute W(N) exactly using Fraction arithmetic."""
    n = len(fracs)
    if n == 0:
        return Fraction(0)
    w = Fraction(0)
    for j, f in enumerate(fracs):
        delta = f - Fraction(j, n)
        w += delta * delta
    return w

def compute_components(fracs):
    """Compute S2, R, and other components exactly."""
    n = len(fracs)
    S2 = sum(f * f for f in fracs)  # Σ f_j²
    S1 = sum(fracs)                  # Σ f_j = n/2
    R = sum(Fraction(j) * f for j, f in enumerate(fracs))  # Σ j·f_j
    sum_j2 = Fraction(n * (n-1) * (2*n-1), 6)  # Σ j²
    W = S2 - Fraction(2, n) * R + Fraction(1, n*n) * sum_j2
    return {
        'n': n, 'S1': S1, 'S2': S2, 'R': R, 'sum_j2': sum_j2, 'W': W
    }

def analyze_delta_w(max_p=100):
    """Analyze ΔW(p) decomposition for small primes."""
    print("=" * 80)
    print("EXACT FORMULA DERIVATION FOR ΔW(p)")
    print("=" * 80)

    # Precompute Farey sequences
    farey = {}
    for N in range(1, max_p + 1):
        farey[N] = farey_sequence(N)

    print(f"\nComputed F_N for N=1..{max_p}")

    # For each prime p, compute the exact decomposition of ΔW(p)
    primes = [p for p in range(11, max_p + 1)
              if p > 1 and all(p % d != 0 for d in range(2, int(p**0.5) + 1))]

    print(f"\n{'p':>4} {'n':>6} {'m':>4} {'ΔS2':>20} {'ΔR':>20} {'ΔW':>20} {'ΔW>0':>5}")

    results = []
    for p in primes:
        comp_p = compute_components(farey[p])
        comp_pm1 = compute_components(farey[p - 1])

        n = comp_pm1['n']  # |F_{p-1}|
        m = p - 1            # φ(p) for prime p
        n_new = n + m        # |F_p|

        delta_S2 = comp_p['S2'] - comp_pm1['S2']
        delta_R = comp_p['R'] - comp_pm1['R']
        delta_W = comp_pm1['W'] - comp_p['W']  # positive = violation

        # The new fractions k/p contribute to S2:
        new_frac_S2 = sum(Fraction(k, p) ** 2 for k in range(1, p))
        # Simplify: Σ_{k=1}^{p-1} k²/p² = (p-1)(2p-1)/(6p)
        new_frac_S2_formula = Fraction((p-1) * (2*p - 1), 6 * p)

        is_viol = "YES" if delta_W > 0 else "no"

        results.append({
            'p': p, 'n': n, 'm': m, 'n_new': n_new,
            'delta_S2': delta_S2, 'delta_R': delta_R, 'delta_W': delta_W,
            'new_frac_S2': new_frac_S2, 'new_frac_S2_formula': new_frac_S2_formula,
            'W_p': comp_p['W'], 'W_pm1': comp_pm1['W'],
            'S2_p': comp_p['S2'], 'S2_pm1': comp_pm1['S2'],
            'R_p': comp_p['R'], 'R_pm1': comp_pm1['R'],
        })

        print(f"{p:4d} {n:6d} {m:4d} {float(delta_S2):20.12f} "
              f"{float(delta_R):20.6f} {float(delta_W):20.15f} {is_viol:>5}")

    # Now look for patterns in ΔW
    print(f"\n{'='*80}")
    print("DECOMPOSITION ANALYSIS")
    print(f"{'='*80}")

    print(f"\nKey identity: W(N) = S2 - (2/n)R + (n-1)(2n-1)/(6n)")
    print(f"So ΔW = [S2_old - (2/n)R_old + ...] - [S2_new - (2/n')R_new + ...]")
    print(f"where n = |F_{{p-1}}|, n' = n + p - 1")

    print(f"\n{'p':>4} {'W(p-1)':>18} {'W(p)':>18} {'ΔW':>18} {'n·ΔW':>18}")
    for r in results:
        print(f"{r['p']:4d} {float(r['W_pm1']):18.12f} {float(r['W_p']):18.12f} "
              f"{float(r['delta_W']):18.15f} {float(r['n_new'] * r['delta_W']):18.12f}")

    # Key insight: what is the contribution of the NEW fractions vs the RESHUFFLING?
    print(f"\n{'='*80}")
    print("NEW FRACTIONS vs RESHUFFLING CONTRIBUTIONS")
    print(f"{'='*80}")

    print(f"\nWhen p fractions k/p are inserted into F_{{p-1}}:")
    print(f"  1. NEW: The p-1 new fractions k/p add to S2 by Σ(k/p)² = (p-1)(2p-1)/(6p)")
    print(f"  2. REINDEX: All |F_p| fractions get new ideal positions j/|F_p|")
    print(f"  3. The net ΔW depends on WHERE the new fractions land relative to ideal positions")

    print(f"\n{'p':>4} {'ΔS2(new)':>18} {'ΔS2(total)':>18} {'ratio':>8}")
    for r in results:
        ratio = float(r['new_frac_S2'] / r['delta_S2']) if r['delta_S2'] != 0 else 0
        print(f"{r['p']:4d} {float(r['new_frac_S2']):18.12f} {float(r['delta_S2']):18.12f} "
              f"{ratio:8.4f}")

    # Look at the RANK POSITIONS of new fractions
    print(f"\n{'='*80}")
    print("RANK POSITIONS OF NEW FRACTIONS (small primes)")
    print(f"{'='*80}")

    for p in primes[:5]:  # Just first 5 primes
        new_fracs = [Fraction(k, p) for k in range(1, p)]
        new_fracs_sorted = sorted(new_fracs)

        # Find their positions in F_p
        f_p = farey[p]
        positions = []
        for nf in new_fracs_sorted:
            pos = f_p.index(nf)
            positions.append(pos)

        n_new = len(f_p)
        ideal_positions = [Fraction(pos, n_new) for pos in positions]
        actual_values = new_fracs_sorted
        deviations = [float(av - ip) for av, ip in zip(actual_values, ideal_positions)]

        mean_dev = sum(deviations) / len(deviations) if deviations else 0

        print(f"\n  Prime p={p}: {p-1} new fractions, mean deviation = {mean_dev:.8f}")
        if p <= 19:
            for nf, pos in zip(new_fracs_sorted, positions):
                ideal = Fraction(pos, n_new)
                dev = float(nf - ideal)
                print(f"    {nf} at rank {pos}/{n_new}, "
                      f"ideal={float(ideal):.6f}, dev={dev:+.6f}")

    # Final: can we express ΔW(p) in terms of M(p)?
    print(f"\n{'='*80}")
    print("CONNECTING ΔW(p) TO M(p)")
    print(f"{'='*80}")

    # Compute Mertens function
    max_N = max_p
    mu = [0] * (max_N + 1)
    mu[1] = 1
    is_prime_arr = [True] * (max_N + 1)
    is_prime_arr[0] = is_prime_arr[1] = False
    primes_list = []
    for i in range(2, max_N + 1):
        if is_prime_arr[i]:
            primes_list.append(i)
            mu[i] = -1
        for q in primes_list:
            if i * q > max_N: break
            is_prime_arr[i * q] = False
            if i % q == 0: mu[i * q] = 0; break
            else: mu[i * q] = -mu[i]
    M = [0] * (max_N + 1)
    for k in range(1, max_N + 1):
        M[k] = M[k-1] + mu[k]

    print(f"\n{'p':>4} {'ΔW':>18} {'M(p)':>6} {'M/√p':>10} {'n²·ΔW':>18} {'n²·ΔW/M':>12}")
    for r in results:
        p = r['p']
        m_val = M[p]
        m_norm = m_val / sqrt(p)
        n2_dw = float(r['n_new']**2 * r['delta_W'])
        ratio = n2_dw / m_val if m_val != 0 else float('inf')
        print(f"{p:4d} {float(r['delta_W']):18.15f} {m_val:6d} {m_norm:10.5f} "
              f"{n2_dw:18.8f} {ratio:12.6f}")

    print(f"\n  Looking for: ΔW(p) ≈ f(M(p), p, |F_p|)")
    print(f"  If n²·ΔW/M(p) is approximately constant, then ΔW ≈ C·M(p)/n²")

    # Check if n²·ΔW / M(p) converges
    ratios = []
    for r in results:
        p = r['p']
        m_val = M[p]
        if m_val != 0 and r['delta_W'] != 0:
            n2_dw = float(r['n_new']**2 * r['delta_W'])
            ratios.append(n2_dw / m_val)

    if ratios:
        import numpy as np
        print(f"\n  n²·ΔW/M(p) statistics:")
        print(f"    Mean: {np.mean(ratios):.6f}")
        print(f"    Std:  {np.std(ratios):.6f}")
        print(f"    CV:   {np.std(ratios)/abs(np.mean(ratios)):.4f}")
        print(f"    Min:  {np.min(ratios):.6f}")
        print(f"    Max:  {np.max(ratios):.6f}")

        if np.std(ratios) / abs(np.mean(ratios)) < 0.3:
            print(f"\n  *** POSSIBLE RELATIONSHIP: ΔW(p) ≈ {np.mean(ratios):.4f} · M(p) / |F_p|² ***")
        else:
            print(f"\n  Ratio is NOT approximately constant (CV={np.std(ratios)/abs(np.mean(ratios)):.2f})")
            print(f"  Need a more sophisticated model.")


if __name__ == '__main__':
    analyze_delta_w(max_p=80)
