#!/usr/bin/env python3
"""
Mertens Function & Farey Wobble: Deep Connection Analysis
==========================================================

KEY FORMULA (Landau, ~1924):
  M(N) = -1 + Σ_{a ∈ F_N} e^{2πia}

where M(N) = Σ_{k=1}^N μ(k) is the Mertens function
and F_N is the Farey sequence of order N.

This script:
1. Verifies the formula numerically for small N
2. Analyzes M(N) oscillations near the spike zone (N=3000-4000)
3. Correlates per-step ΔW(N) with μ(N) (Möbius function)
4. Investigates the role of Riemann zeta zeros in the burst behavior
5. Reads C output CSV if available for large-N analysis
"""

import numpy as np
from math import gcd, log, pi, cos, sin, sqrt
import cmath
import json
import os
import sys
import csv

# ──────────────────────────────────────────────
# 1. SIEVES
# ──────────────────────────────────────────────

def compute_mobius_sieve(limit):
    """Compute μ(n) for all n ≤ limit using a linear sieve."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime = [True] * (limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1  # squarefree with 1 prime factor
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0  # p² | ip
                break
            else:
                mu[i * p] = -mu[i]
    return mu, is_prime


def mertens_series(mu, N):
    """Return M(k) = Σ_{j=1}^k μ(j) for k=0..N as an array."""
    M = [0] * (N + 1)
    for k in range(1, N + 1):
        M[k] = M[k-1] + mu[k]
    return M


# ──────────────────────────────────────────────
# 2. FAREY GENERATOR
# ──────────────────────────────────────────────

def farey_generator(N):
    """Yield (a, b) for each fraction a/b in F_N in order."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b


def farey_character_sum(N):
    """Compute Σ_{a/b ∈ F_N} exp(2πi · a/b)."""
    total = complex(0)
    for (a, b) in farey_generator(N):
        total += cmath.exp(2j * pi * a / b)
    return total


# ──────────────────────────────────────────────
# 3. VERIFY LANDAU FORMULA: M(N) = -1 + Σ exp(2πia)
# ──────────────────────────────────────────────

def verify_landau_formula(max_N=50):
    print("=" * 65)
    print("VERIFICATION: Landau's formula M(N) = -1 + Σ_{a∈F_N} e^{2πia}")
    print("=" * 65)
    mu, _ = compute_mobius_sieve(max_N)
    M = mertens_series(mu, max_N)

    print(f"\n{'N':>4}  {'M(N)':>6}  {'Re(charsum)-1':>14}  {'|error|':>10}  {'match?':>6}")
    all_ok = True
    for N in range(1, max_N + 1):
        cs = farey_character_sum(N)
        predicted = cs.real - 1
        error = abs(predicted - M[N])
        ok = error < 1e-8
        if not ok:
            all_ok = False
        if N <= 20 or N % 10 == 0:
            print(f"  {N:3d}  {M[N]:6d}  {predicted:14.8f}  {error:10.2e}  {'✓' if ok else '✗':>6}")

    print(f"\n  Formula verified for N=1..{max_N}: {'ALL CORRECT' if all_ok else 'ERRORS FOUND'}")
    return M


# ──────────────────────────────────────────────
# 4. MERTENS OSCILLATION NEAR SPIKE ZONE
# ──────────────────────────────────────────────

def analyze_mertens_near_spike(max_N=5500):
    """
    Analyze M(N)/√N near the spike zone (N=3000-4000).
    Investigate if the spike corresponds to M(N) reaching local extrema.
    Also compute the contribution of the first few zeta zeros.
    """
    print("\n" + "=" * 65)
    print("MERTENS FUNCTION ANALYSIS NEAR SPIKE ZONE (N=3000-4500)")
    print("=" * 65)

    mu, is_prime = compute_mobius_sieve(max_N)
    M = mertens_series(mu, max_N)

    # Spike zone: violations at 3163, 3251-3359, 3433-3511
    spike_start = 3000
    spike_end = 4000

    # Find local extrema of M(N)/sqrt(N)
    normalized = [M[N] / sqrt(N) if N > 0 else 0 for N in range(max_N + 1)]

    print(f"\n  M(N) and M(N)/√N trajectory through spike zone:")
    print(f"  {'N':>5}  {'M(N)':>8}  {'M(N)/√N':>10}  {'μ(N)':>6}  {'prime?':>6}")

    # Print at key points: just before, during, and after spike
    key_points = (
        list(range(2950, 2970)) +
        [3163] +
        list(range(3245, 3270)) +
        list(range(3295, 3310)) +
        [3359, 3360] +
        list(range(3430, 3445)) +
        [3511, 3512] +
        list(range(3590, 3600))
    )

    for N in key_points:
        if N > max_N:
            break
        note = ""
        if N in [1399,1409,1423,1427,1429, 2633,2647,2657,2659,2663,
                 3163, 3251,3253,3257,3259,3271,3299,3301,3307,3313,
                 3319,3323,3329,3331,3343,3359,3433,3449,3457,3461,
                 3463,3467,3511]:
            note = " ← VIOLATION"
        p_str = "prime" if is_prime[N] else ""
        print(f"  {N:5d}  {M[N]:8d}  {normalized[N]:10.6f}  {mu[N]:6d}  {p_str:6s}{note}")

    # Find actual extrema of M(N)/√N in the range
    print(f"\n  Extrema of M(N)/√N in [{spike_start}, {spike_end+500}]:")
    local_max_val = max(normalized[spike_start:spike_end+500])
    local_min_val = min(normalized[spike_start:spike_end+500])
    local_max_idx = normalized.index(local_max_val)
    local_min_idx = normalized.index(local_min_val)
    print(f"    Maximum: M({local_max_idx})/√{local_max_idx} = {local_max_val:.6f}")
    print(f"    Minimum: M({local_min_idx})/√{local_min_idx} = {local_min_val:.6f}")

    # Overall extrema up to max_N
    global_max = max(normalized[2:])
    global_min = min(normalized[2:])
    gmax_idx = normalized.index(global_max)
    gmin_idx = normalized.index(global_min)
    print(f"\n  Global extrema of M(N)/√N up to N={max_N}:")
    print(f"    Maximum: M({gmax_idx})/√{gmax_idx} = {global_max:.6f}")
    print(f"    Minimum: M({gmin_idx})/√{gmin_idx} = {global_min:.6f}")

    return mu, M, normalized, is_prime


# ──────────────────────────────────────────────
# 5. ZETA ZEROS ANALYSIS
# ──────────────────────────────────────────────

# First 20 non-trivial zeros of ζ(s) on the critical line s = 1/2 + iγ
ZETA_ZEROS_IMAGINARY = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
]

def zeta_zero_phase(N, gamma):
    """Phase of N^{iγ} = exp(iγ log N)."""
    return gamma * log(N)

def mertens_explicit_approx(N, num_zeros=20):
    """
    Approximate M(N) using the explicit formula (leading zeros only):
      M(N) ≈ Σ_ρ N^ρ / (ρ ζ'(ρ))
    We use just the phase information N^{iγ}/|ρ| ≈ N^{1/2} cos(γ log N + φ_k) / γ_k
    ignoring ζ'(ρ) (unknown) but capturing the oscillation structure.
    """
    # Rough approximation: each zero contributes ~ ±2 * N^{1/2} / γ_k * cos(γ_k * log(N))
    # The factor 2 comes from pairing ρ with ρ̄
    approx = 0.0
    for gamma in ZETA_ZEROS_IMAGINARY[:num_zeros]:
        phase = gamma * log(N)
        approx += cos(phase) / gamma  # rough, ignoring ζ'(ρ) scaling
    return -2 * sqrt(N) * approx  # sign and scale are approximate

def analyze_zeta_zero_phases(spike_zone_start=3163, spike_zone_end=3511):
    print("\n" + "=" * 65)
    print("ZETA ZERO PHASE ANALYSIS AT SPIKE ZONE")
    print("=" * 65)

    print(f"\n  Phase γ·log(N) (mod 2π) at key violation primes:")
    violation_primes = [3163, 3251, 3253, 3257, 3259, 3271, 3299, 3301,
                        3307, 3313, 3319, 3323, 3329, 3331, 3343, 3359,
                        3433, 3449, 3457, 3461, 3463, 3467, 3511]

    # For each of the first 5 zeros, show phase at spike zone
    print(f"\n  {'N':>5}", end="")
    for gamma in ZETA_ZEROS_IMAGINARY[:5]:
        print(f"  γ={gamma:.2f}→φ", end="")
    print()

    for N in [2600, 2663, 3000, 3163] + violation_primes[:8] + [3511, 3600, 4000, 4861]:
        print(f"  {N:5d}", end="")
        for gamma in ZETA_ZEROS_IMAGINARY[:5]:
            phase = (gamma * log(N)) % (2 * pi)
            print(f"  {phase:9.4f}", end="")
        print()

    # Key question: Is cos(γ_1 * log(N)) unusually large at the spike zone?
    print("\n  cos(γ₁·log N) across the range (γ₁ = 14.1347...):")
    gamma1 = ZETA_ZEROS_IMAGINARY[0]
    print(f"  {'N':>6}  {'cos(γ₁·logN)':>14}  {'note':}")
    for N in range(3000, 3600, 10):
        c = cos(gamma1 * log(N))
        note = ""
        if N in violation_primes:
            note = "← violation prime"
        if abs(c) > 0.9:
            note += " [NEAR EXTREMUM]"
        if note:
            print(f"  {N:6d}  {c:14.8f}  {note}")

    # Compare phase structure at non-spike vs spike zones
    print(f"\n  Mean |cos(γ₁·log p)| by range (should be higher near spike if zeros responsible):")
    mu_arr, is_prime = compute_mobius_sieve(6000)
    for lo, hi in [(1000,2000), (2000,3000), (3000,4000), (4000,5000), (5000,6000)]:
        primes_in_range = [N for N in range(lo, hi) if is_prime[N] and N >= 11]
        mean_cos = np.mean([abs(cos(gamma1 * log(p))) for p in primes_in_range])
        print(f"    [{lo:5d},{hi:5d}): {len(primes_in_range):3d} primes, mean|cos(γ₁·log p)|={mean_cos:.6f}")


# ──────────────────────────────────────────────
# 6. DELTA W vs MU CORRELATION
# ──────────────────────────────────────────────

def correlate_delta_w_with_mu(json_file=None, csv_file=None):
    """
    Correlate ΔW(N) = W(N-1) - W(N) with μ(N) across all N.
    """
    print("\n" + "=" * 65)
    print("CORRELATION: ΔW(N) vs μ(N) (Möbius function)")
    print("=" * 65)

    # Try to load CSV data (from C program output)
    data_by_N = {}
    if csv_file and os.path.exists(csv_file):
        print(f"\n  Loading C CSV data from {csv_file}...")
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                N = int(row['N'])
                data_by_N[N] = {
                    'wobble': float(row['wobble']),
                    'farey_size': int(row['farey_size']),
                    'is_prime': int(row['is_prime']),
                    'delta_w': float(row['delta_w']),
                    'mertens': int(row['mertens']),
                    'mu': int(row['mu']),
                }
        print(f"  Loaded {len(data_by_N)} rows.")
    elif json_file and os.path.exists(json_file):
        print(f"\n  Loading JSON data from {json_file}...")
        with open(json_file) as f:
            jdata = json.load(f)
        # Only has prime_results, but let's use those
        for r in jdata.get('prime_results', []):
            data_by_N[r['p']] = {
                'delta_w': r['delta'],
                'is_prime': 1,
            }
        print(f"  Loaded {len(data_by_N)} prime records from JSON.")
    else:
        print("  No data file found. Run the C program first.")
        return

    if not data_by_N:
        return

    max_N = max(data_by_N.keys())
    mu_sieve, is_prime_sieve = compute_mobius_sieve(max_N)

    # For CSV data: full correlation
    if csv_file and os.path.exists(csv_file):
        all_N = sorted(data_by_N.keys())
        delta_w = np.array([data_by_N[N]['delta_w'] for N in all_N])
        mu_vals = np.array([data_by_N[N]['mu'] for N in all_N])
        mertens_vals = np.array([data_by_N[N]['mertens'] for N in all_N])

        # Correlation between ΔW and μ
        # Only valid from N=2 (delta for N=1 is 0 by convention)
        valid = [i for i, N in enumerate(all_N) if N >= 2]
        dw = delta_w[valid]
        mu = mu_vals[valid]

        corr = np.corrcoef(dw, mu)[0, 1]
        print(f"\n  Pearson correlation: ρ(ΔW(N), μ(N)) = {corr:.6f}")

        # Breakdown by mu value
        print(f"\n  Mean ΔW(N) by μ(N) value:")
        for mv in [-1, 0, 1]:
            idx = [i for i in valid if mu_vals[i] == mv]
            if idx:
                mean_dw = np.mean(delta_w[idx])
                std_dw = np.std(delta_w[idx])
                n_neg = sum(1 for i in idx if delta_w[i] < 0)
                print(f"    μ(N)={mv:+d}: n={len(idx):5d}, mean ΔW={mean_dw:+.8f}, "
                      f"std={std_dw:.8f}, {100*n_neg/len(idx):.1f}% wobble increased")

        # Correlation between M(N) and W(N) (level comparison)
        w_vals = np.array([data_by_N[N]['wobble'] for N in all_N])
        fs_vals = np.array([data_by_N[N]['farey_size'] for N in all_N])
        N_vals = np.array(all_N, dtype=float)

        # Theoretical: W(N) ~ C/N under RH, M(N) ~ O(N^{0.5+ε})
        # Test: is M(N)^2 correlated with N * W(N)?
        MN2 = mertens_vals ** 2
        NW = N_vals * w_vals
        corr2 = np.corrcoef(MN2[1:], NW[1:])[0, 1]
        print(f"\n  Pearson correlation: ρ(M(N)², N·W(N)) = {corr2:.6f}")
        print(f"  (Both should be O(N^ε) under RH — strong correlation expected)")

        # Plot the spike zone in detail
        print(f"\n  Wobble increase rate and M(N) around spike zone:")
        print(f"  {'N':>5}  {'ΔW(N)':>14}  {'μ(N)':>5}  {'M(N)':>7}  {'M/√N':>8}  note")
        for N in range(3155, 3520, 2):
            if N not in data_by_N:
                continue
            d = data_by_N[N]
            mn = d['mertens']
            dw = d['delta_w']
            is_p = d['is_prime']
            note = ""
            if N in [3163, 3251,3253,3257,3259,3271,3299,3301,3307,3313,
                     3319,3323,3329,3331,3343,3359,3433,3449,3457,3461,
                     3463,3467,3511]:
                note = " ← VIOLATION"
            p_str = "p" if is_p else " "
            print(f"  {N:5d}  {dw:14.8f}  {mu_sieve[N]:5d}  {mn:7d}  "
                  f"{mn/sqrt(N):8.5f}  {p_str}{note}")

    # JSON data: only primes
    elif json_file:
        prime_Ns = sorted(data_by_N.keys())
        for N in prime_Ns[:30]:
            d = data_by_N[N]
            mu_v = mu_sieve[N]
            print(f"  p={N:6d}  ΔW={d['delta_w']:+.8f}  μ(p)={mu_v:+d}")


# ──────────────────────────────────────────────
# 7. LOAD AND ANALYZE C OUTPUT
# ──────────────────────────────────────────────

def analyze_c_output(csv_file):
    if not os.path.exists(csv_file):
        print(f"\n  C output file not found: {csv_file}")
        print("  Run: ./wobble_largescale 20000")
        return

    print("\n" + "=" * 65)
    print("C OUTPUT ANALYSIS (LARGE N)")
    print("=" * 65)

    data = []
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'N': int(row['N']),
                'wobble': float(row['wobble']),
                'farey_size': int(row['farey_size']),
                'is_prime': int(row['is_prime']),
                'delta_w': float(row['delta_w']),
                'mertens': int(row['mertens']),
                'mu': int(row['mu']),
            })

    max_N = data[-1]['N']
    print(f"\n  Data range: N=1 to N={max_N}")

    # Violation analysis
    violations = [d['N'] for d in data
                  if d['is_prime'] and d['N'] >= 11 and d['delta_w'] > 0]
    primes_ge11 = [d['N'] for d in data if d['is_prime'] and d['N'] >= 11]
    print(f"  Primes ≥ 11: {len(primes_ge11)}")
    print(f"  Violations: {len(violations)} ({100*len(violations)/len(primes_ge11):.1f}%)")

    # Violation rate by 1000s
    print(f"\n  Violation rate by range:")
    for lo in range(0, max_N, 2000):
        hi = lo + 2000
        pr = [d['N'] for d in data if d['is_prime'] and d['N'] >= 11 and lo <= d['N'] < hi]
        vl = [d['N'] for d in data if d['is_prime'] and d['N'] >= 11
              and lo <= d['N'] < hi and d['delta_w'] > 0]
        if pr:
            print(f"    [{lo:6d},{hi:6d}): {len(pr):4d} primes, "
                  f"{len(vl):3d} violations ({100*len(vl)/len(pr):.1f}%)")

    # Cluster analysis with gap > 100
    print(f"\n  Violation clusters (gap > 100 = new cluster):")
    if violations:
        clusters = [[violations[0]]]
        for p in violations[1:]:
            if p - clusters[-1][-1] <= 100:
                clusters[-1].append(p)
            else:
                clusters.append([p])
        for i, cl in enumerate(clusters):
            print(f"    Cluster {i+1}: first={cl[0]}, last={cl[-1]}, "
                  f"size={len(cl)}, span={cl[-1]-cl[0]}")

    # Power law for non-violation primes
    ps = np.array([d['N'] for d in data
                   if d['is_prime'] and d['N'] >= 11 and d['delta_w'] < 0])
    dws = np.array([-d['delta_w'] for d in data
                    if d['is_prime'] and d['N'] >= 11 and d['delta_w'] < 0])
    if len(ps) > 20:
        coeffs = np.polyfit(np.log(ps), np.log(dws), 1)
        print(f"\n  Power law: |ΔW(p)| ~ p^{coeffs[0]:.4f}")

    # M(N) statistics near violations
    print(f"\n  Mean M(N) at violation vs non-violation primes (≥11):")
    viol_M = [d['mertens'] for d in data
              if d['is_prime'] and d['N'] >= 11 and d['delta_w'] > 0]
    nonviol_M = [d['mertens'] for d in data
                 if d['is_prime'] and d['N'] >= 11 and d['delta_w'] < 0]
    if viol_M and nonviol_M:
        print(f"    Violations:     mean M={np.mean(viol_M):.2f}, median M={np.median(viol_M):.2f}")
        print(f"    Non-violations: mean M={np.mean(nonviol_M):.2f}, median M={np.median(nonviol_M):.2f}")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file  = os.path.join(script_dir, 'wobble_ultra_data.json')
    csv_file   = os.path.join(script_dir, 'wobble_c_data_20000.csv')

    print("MERTENS FUNCTION & FAREY WOBBLE: DEEP CONNECTION ANALYSIS")
    print("=" * 65)

    # 1. Verify the Landau formula
    verify_landau_formula(max_N=60)

    # 2. Mertens oscillation near spike zone
    mu_arr, M_arr, normalized, is_prime_arr = analyze_mertens_near_spike(max_N=5500)

    # 3. Zeta zero phase analysis
    analyze_zeta_zero_phases()

    # 4. ΔW vs μ correlation (JSON if available, CSV preferred)
    if os.path.exists(csv_file):
        correlate_delta_w_with_mu(csv_file=csv_file)
    elif os.path.exists(json_file):
        correlate_delta_w_with_mu(json_file=json_file)

    # 5. Full C output analysis
    if os.path.exists(csv_file):
        analyze_c_output(csv_file)

    print("\n" + "=" * 65)
    print("SUMMARY OF CONNECTIONS")
    print("=" * 65)
    print("""
FORMULA 1 (Landau):  M(N) = -1 + Σ_{a ∈ F_N} e^{2πia}

FORMULA 2 (Franel-Landau equivalence):
  RH ⟺ Σ |f_j - j/|F_N|| = O(N^{1/2+ε})

FORMULA 3 (Our wobble):
  W(N) = Σ (f_j - j/|F_N|)² — the L²-squared version

FORMULA 4 (New per-step decomposition):
  ΔW(N) = W(N-1) - W(N)  [SIGN: negative = prime disrupts uniformity]

CONJECTURE (refined from data):
  For primes p ≥ 11, ΔW(p) < 0 holds in ~93% of cases.
  Violations cluster in bursts, possibly connected to oscillations of M(N)/√N
  or constructive interference of Riemann zeta zero contributions.

OPEN QUESTION:
  Does the violation rate converge to a constant, or does it → 0 as N → ∞?
  If → 0: consistent with RH
  If → positive constant: potentially problematic for RH
  The burst at N≈3163-3511 with 19% violation rate needs more data.
""")
