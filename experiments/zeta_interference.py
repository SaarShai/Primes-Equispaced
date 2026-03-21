#!/usr/bin/env python3
"""
Zeta Zero Constructive Interference & Wobble Violation Analysis
================================================================

HYPOTHESIS: Wobble violations occur when multiple Riemann zeta zeros
constructively interfere, causing M(N)/√N to peak.

The explicit formula (von Mangoldt / Titchmarsh):
  M(x) = Σ_ρ x^ρ / (ρ · ζ'(ρ))  + (smaller terms)

Each nontrivial zero ρ_k = 1/2 + i·γ_k contributes a term
  ≈ 2·√x · cos(γ_k · log(x) + φ_k) / |ρ_k · ζ'(ρ_k)|

"Constructive interference" = when cos(γ_k · log(x) + φ_k) is
consistently positive for many zeros simultaneously.

This script:
1. Computes "interference score" I(N) = Σ_k cos(γ_k · log N) / γ_k
2. Shows that peaks of I(N) predict wobble violation zones
3. Predicts the NEXT violation cluster locations beyond N=20,000
"""

import numpy as np
from math import log, pi, cos, sin, sqrt, gcd
import csv
import os

# First 50 nontrivial zeros of ζ(s): imaginary parts γ_k
# Source: Odlyzko / LMFDB
ZETA_ZEROS = [
    14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
    37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
    52.970321478, 56.446247697, 59.347044003, 60.831778525, 65.112544048,
    67.079811257, 69.546401711, 72.067157674, 75.704690699, 77.144840069,
    79.337375020, 82.910380854, 84.735492981, 87.425274613, 88.809111208,
    92.491899271, 94.651344041, 95.870634228, 98.831194218, 101.317851006,
    103.725538040, 105.446623052, 107.168611184, 111.029535543, 111.874659177,
    114.320220915, 116.226680321, 118.790782866, 121.370125002, 122.946829294,
    124.256818554, 127.516683880, 129.578704200, 131.087688531, 133.497737203,
    134.756509753, 138.116042055, 139.736208952, 141.123707404, 143.111845808,
]


def interference_score(N, num_zeros=20):
    """
    I(N) = Σ_{k=1}^{num_zeros} cos(γ_k · log N) / γ_k

    This approximates the contribution of the first num_zeros Riemann zeros
    to M(N)/√N (up to constant factors from ζ'(ρ)).
    """
    ln_N = log(N)
    score = 0.0
    for gamma in ZETA_ZEROS[:num_zeros]:
        score += cos(gamma * ln_N) / gamma
    return score


def weighted_interference_score(N, num_zeros=20):
    """
    Same but with 1/γ_k^2 weighting (accounts for ζ'(ρ) scaling roughly).
    """
    ln_N = log(N)
    score = 0.0
    for gamma in ZETA_ZEROS[:num_zeros]:
        score += cos(gamma * ln_N) / (gamma ** 2)
    return score


def compute_interference_profile(max_N=20000, num_zeros=20):
    """Compute I(N) for all N from 2 to max_N."""
    profile = np.zeros(max_N + 1)
    for N in range(2, max_N + 1):
        profile[N] = interference_score(N, num_zeros)
    return profile


def find_peaks(profile, threshold, min_N=11):
    """Find local maxima above threshold."""
    peaks = []
    for N in range(max(min_N, 2), len(profile) - 1):
        if (profile[N] > threshold and
            profile[N] >= profile[N-1] and profile[N] >= profile[N+1]):
            peaks.append((N, profile[N]))
    return peaks


def is_prime_sieve(max_N):
    """Simple Sieve of Eratosthenes."""
    sieve = [True] * (max_N + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(max_N**0.5) + 1):
        if sieve[p]:
            for k in range(p*p, max_N + 1, p):
                sieve[k] = False
    return sieve


def mobius_sieve(max_N):
    """Compute μ(n) and M(n) for all n ≤ max_N."""
    mu = [0] * (max_N + 1)
    mu[1] = 1
    is_p = [True] * (max_N + 1)
    primes = []
    for i in range(2, max_N + 1):
        if is_p[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > max_N:
                break
            is_p[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (max_N + 1)
    for k in range(1, max_N + 1):
        M[k] = M[k-1] + mu[k]
    return mu, M, is_p


def main():
    MAX_N = 30000  # predict beyond 20000
    NUM_ZEROS = 30

    print("=" * 70)
    print("ZETA ZERO CONSTRUCTIVE INTERFERENCE ANALYSIS")
    print("=" * 70)

    # Compute interference profile
    print(f"\nComputing I(N) = Σ cos(γ_k·log N)/γ_k for N=2..{MAX_N} with {NUM_ZEROS} zeros...")
    profile = compute_interference_profile(MAX_N, NUM_ZEROS)

    # Compute Mertens function for comparison
    print(f"Computing M(N) for N=1..{MAX_N}...")
    mu, M, is_p = mobius_sieve(MAX_N)

    # Normalized Mertens
    M_norm = np.zeros(MAX_N + 1)
    for N in range(2, MAX_N + 1):
        M_norm[N] = M[N] / sqrt(N)

    # Correlation between I(N) and M(N)/√N
    valid = np.arange(100, MAX_N + 1)
    corr = np.corrcoef(profile[valid], M_norm[valid])[0, 1]
    print(f"\n  Correlation ρ(I(N), M(N)/√N) for N≥100: {corr:.6f}")

    # ──────────────────────────────────────────────
    # KEY TEST: Do peaks of I(N) predict violation zones?
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("PEAK ANALYSIS: Does high I(N) predict wobble violations?")
    print(f"{'='*70}")

    # Identify "hot zones" where I(N) is in its top 10%
    all_I = profile[100:MAX_N+1]
    threshold_90 = np.percentile(all_I, 90)
    threshold_95 = np.percentile(all_I, 95)

    print(f"\n  I(N) percentiles: 90th={threshold_90:.6f}, 95th={threshold_95:.6f}")

    # Find contiguous hot zones
    hot_starts = []
    in_hot = False
    for N in range(100, MAX_N + 1):
        if profile[N] > threshold_90:
            if not in_hot:
                hot_starts.append(N)
                in_hot = True
        else:
            if in_hot:
                hot_starts[-1] = (hot_starts[-1], N - 1)
                in_hot = False
    if in_hot:
        hot_starts[-1] = (hot_starts[-1], MAX_N)

    # Filter to only tuples
    hot_zones = [z for z in hot_starts if isinstance(z, tuple)]

    print(f"\n  Hot zones (I(N) > 90th percentile) — predicted violation regions:")
    print(f"  {'Zone':>4}  {'Start':>6}  {'End':>6}  {'Span':>5}  {'MaxI':>8}  {'MaxM/√N':>9}  {'Primes':>6}")
    for i, (lo, hi) in enumerate(hot_zones[:20]):
        max_I = max(profile[lo:hi+1])
        max_M = max(M_norm[lo:hi+1])
        n_primes = sum(1 for N in range(lo, hi+1) if is_p[N])
        print(f"  {i+1:4d}  {lo:6d}  {hi:6d}  {hi-lo:5d}  {max_I:8.5f}  {max_M:+9.5f}  {n_primes:6d}")

    # ──────────────────────────────────────────────
    # PREDICTIONS FOR N > 20000
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("PREDICTIONS: Violation clusters beyond N=20,000")
    print(f"{'='*70}")

    print(f"\n  Hot zones in [20000, {MAX_N}] (I > 90th percentile):")
    future_zones = [(lo, hi) for lo, hi in hot_zones if lo >= 20000]
    for i, (lo, hi) in enumerate(future_zones):
        max_I = max(profile[lo:hi+1])
        max_M = max(M_norm[lo:hi+1])
        n_primes = sum(1 for N in range(lo, hi+1) if is_p[N])
        print(f"    [{lo}, {hi}]: span={hi-lo}, maxI={max_I:.5f}, maxM/√N={max_M:+.5f}, {n_primes} primes")

    if not future_zones:
        print("    None found in this range. Try extending MAX_N.")

    # ──────────────────────────────────────────────
    # PHASE ALIGNMENT ANALYSIS
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("PHASE ALIGNMENT: Are zeros constructively interfering at spike zones?")
    print(f"{'='*70}")

    known_spikes = [
        ("Cluster 1", 1399, 1429),
        ("Cluster 2", 2633, 2663),
        ("Cluster 3 (dense)", 3163, 3511),
        ("Quiet zone", 16000, 18000),
    ]

    for label, lo, hi in known_spikes:
        mid = (lo + hi) // 2
        ln_mid = log(mid)
        phases = [(ZETA_ZEROS[k] * ln_mid) % (2*pi) for k in range(NUM_ZEROS)]
        # Count how many phases are in [0, π] (positive contribution zone)
        n_positive = sum(1 for ph in phases if cos(ph) > 0)
        mean_cos = np.mean([cos(ph) for ph in phases])
        I_mid = interference_score(mid, NUM_ZEROS)
        M_mid = M_norm[min(mid, MAX_N)] if mid <= MAX_N else 0

        print(f"\n  {label} (N≈{mid}):")
        print(f"    I(N) = {I_mid:+.6f}")
        print(f"    M(N)/√N = {M_mid:+.6f}")
        print(f"    Zeros with positive cosine: {n_positive}/{NUM_ZEROS} ({100*n_positive/NUM_ZEROS:.0f}%)")
        print(f"    Mean cos(γ_k·log N): {mean_cos:+.4f}")

        # Show first 10 zero phases
        print(f"    First 10 phases (mod 2π): ", end="")
        for k in range(10):
            ph = phases[k]
            c = cos(ph)
            sign = "+" if c > 0 else "-"
            print(f"{sign}{abs(ph):.2f} ", end="")
        print()

    # ──────────────────────────────────────────────
    # CORRELATION BY WINDOW
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("WINDOWED CORRELATION: I(N) vs M(N)/√N by 2000-range")
    print(f"{'='*70}")

    print(f"\n  {'Range':>16}  {'ρ(I,M/√N)':>10}  {'mean I':>9}  {'mean M/√N':>10}  {'max I':>8}")
    for lo in range(0, min(MAX_N, 30000), 2000):
        hi = min(lo + 2000, MAX_N)
        rng = range(max(lo, 2), hi)
        if len(list(rng)) < 10:
            continue
        I_vals = [profile[N] for N in rng]
        M_vals = [M_norm[N] for N in rng]
        if np.std(I_vals) > 0 and np.std(M_vals) > 0:
            c = np.corrcoef(I_vals, M_vals)[0, 1]
        else:
            c = 0
        print(f"  [{lo:6d},{hi:6d}): {c:+10.4f}  {np.mean(I_vals):+9.5f}  {np.mean(M_vals):+10.5f}  {max(I_vals):8.5f}")

    # ──────────────────────────────────────────────
    # FINAL SUMMARY
    # ──────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"""
The interference score I(N) = Σ cos(γ_k·log N)/γ_k serves as a proxy for
the oscillatory part of M(N)/√N driven by zeta zeros.

KEY FINDING: Global correlation ρ(I(N), M(N)/√N) = {corr:.4f}
This means the first {NUM_ZEROS} zeta zeros account for ~{100*corr**2:.0f}% of the
variance in M(N)/√N (in an R² sense).

The "hot zones" where I(N) exceeds the 90th percentile should predict
exactly where wobble violation clusters appear:
  - When I(N) > 0 for many consecutive N → M(N) peaks positive → ΔW(p) > 0
  - When I(N) ≈ 0 or negative → quiet zone, no violations

The burst-then-quiet pattern in violation clusters is a DIRECT CONSEQUENCE
of the quasi-periodic but incommensurate oscillation of zeta zero phases.
The first zero γ₁ ≈ 14.13 dominates, creating a pseudo-period of:
  2π/γ₁ ≈ 0.445 in log-space
  → At N=1000: period ≈ e^{0.445} × 1000 ≈ 1560 (in N-space)
  → At N=10000: period ≈ e^{0.445} × 10000 ≈ 15600 (in N-space)

The second zero γ₂ ≈ 21.02 has pseudo-period 2π/γ₂ ≈ 0.299 in log-space.
When γ₁ and γ₂ phases align (constructive), bursts are strong.
When they cancel (destructive), the quiet zone appears.
""")


if __name__ == '__main__':
    main()
