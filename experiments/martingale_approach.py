#!/usr/bin/env python3
"""
MARTINGALE / SUBMARTINGALE ANALYSIS OF THE FAREY WOBBLE
========================================================

W(N) = Σ(f_j - j/n)² is the Farey wobble for F_N.

QUESTION: Is some transformation of W(N) a supermartingale or submartingale
with respect to the Farey sequence filtration?

TRANSFORMATIONS STUDIED:
  Z(N) = N · W(N)            — normalized wobble
  Y(N) = log W(N)            — log wobble
  P(N) = Π(1 + ΔW(k)/W(k-1)) — multiplicative wobble (telescope to W(N)/W(1))

EMPIRICAL FACTS:
  - At composites: W typically DECREASES (~96% of the time)
  - At primes with M(p) ≤ -3: W typically INCREASES (~100% of the time)
  - ΔW(p) ≈ -c·M(p)/n for some constant c

ANALYSIS:
  1. Compute Z(N) = N·W(N) for N = 2..500 and check monotonicity
  2. Check submartingale property: E[Z(N+1) | Z(N)] ≥ Z(N)
  3. Doob decomposition: Z = M + A where M is martingale, A is predictable increasing
  4. Log wobble Y(N) = log W(N) — check supermartingale
  5. Multiplicative product and bounds via Azuma-Hoeffding
"""

import numpy as np
from math import gcd, isqrt, log, sqrt
from fractions import Fraction
import time
import sys

start_time = time.time()


# ─────────────────────────────────────────────────────────────
# SECTION 0: Utility functions
# ─────────────────────────────────────────────────────────────

def sieve_primes(limit):
    """Return boolean sieve and list of primes up to limit."""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return sieve


def euler_totient_sieve(limit):
    """Compute φ(n) for all n up to limit."""
    phi = np.arange(limit + 1, dtype=np.int64)
    for p in range(2, limit + 1):
        if phi[p] == p:  # p is prime
            phi[p::p] -= phi[p::p] // p
    return phi


def compute_wobble(sorted_fracs):
    """Compute W = Σ (f_j - j/n)² vectorized."""
    n = len(sorted_fracs)
    if n == 0:
        return 0.0
    ideal = np.arange(n, dtype=np.float64) / n
    deltas = sorted_fracs - ideal
    return np.dot(deltas, deltas)


def mertens_function(limit):
    """Compute M(n) = Σ_{k=1}^n μ(k) via sieve of Moebius function."""
    mu = np.zeros(limit + 1, dtype=np.int64)
    mu[1] = 1
    # Sieve for Moebius
    is_prime = sieve_primes(limit)
    primes = np.where(is_prime)[0]

    # Initialize mu
    mu_arr = np.ones(limit + 1, dtype=np.int64)
    min_factor = np.zeros(limit + 1, dtype=np.int64)

    for p in primes:
        # Mark all multiples of p
        mu_arr[p::p] *= -1
        # Mark multiples of p^2 as 0
        p2 = p * p
        if p2 <= limit:
            mu_arr[p2::p2] = 0

    mu_arr[0] = 0
    # Compute cumulative Mertens
    M = np.cumsum(mu_arr)
    return mu_arr, M


# ─────────────────────────────────────────────────────────────
# SECTION 1: Build Farey sequences and compute W(N) for all N
# ─────────────────────────────────────────────────────────────

MAX_N = 500  # Range of analysis

print("=" * 70)
print("MARTINGALE ANALYSIS OF FAREY WOBBLE")
print("=" * 70)
print(f"\nComputing W(N) for N = 1..{MAX_N}")

is_prime = sieve_primes(MAX_N)
phi = euler_totient_sieve(MAX_N)

# Build Farey fractions incrementally
frac_set = {0.0, 1.0}
wobbles = np.zeros(MAX_N + 1)
farey_sizes = np.zeros(MAX_N + 1, dtype=int)
wobbles[1] = 0.25  # W(F_1) for {0, 1}: (0 - 0)^2 + (1 - 0.5)^2 = 0.25
farey_sizes[1] = 2

t0 = time.time()

for N in range(2, MAX_N + 1):
    # Add fractions with denominator N
    for p in range(1, N):
        if gcd(p, N) == 1:
            frac_set.add(p / N)

    sorted_arr = np.array(sorted(frac_set))
    w = compute_wobble(sorted_arr)
    wobbles[N] = w
    farey_sizes[N] = len(sorted_arr)

    if N % 100 == 0:
        elapsed = time.time() - t0
        print(f"  N = {N}: W = {w:.8f}, |F_N| = {len(sorted_arr)}, time = {elapsed:.1f}s")

print(f"  Done in {time.time() - t0:.1f}s\n")

# Compute Mertens
mu_arr, mertens = mertens_function(MAX_N)


# ─────────────────────────────────────────────────────────────
# SECTION 2: Z(N) = N · W(N) — normalized wobble
# ─────────────────────────────────────────────────────────────

print("=" * 70)
print("SECTION 2: Z(N) = N · W(N) — Normalized Wobble")
print("=" * 70)

Z = np.zeros(MAX_N + 1)
for N in range(1, MAX_N + 1):
    Z[N] = N * wobbles[N]

# Print Z values at key points
print(f"\n{'N':>5} {'W(N)':>12} {'Z(N)=N·W(N)':>14} {'ΔZ':>10} {'Type':>8} {'M(N)':>6}")
print("-" * 60)

delta_Z = np.zeros(MAX_N + 1)
for N in range(2, min(MAX_N + 1, 51)):  # Show first 50
    delta_Z[N] = Z[N] - Z[N-1]
    ntype = "PRIME" if is_prime[N] else "comp"
    print(f"{N:5d} {wobbles[N]:12.8f} {Z[N]:14.8f} {delta_Z[N]:+10.6f} {ntype:>8} {mertens[N]:6d}")

# Compute delta_Z for all N
for N in range(2, MAX_N + 1):
    delta_Z[N] = Z[N] - Z[N-1]

# Monotonicity check
print(f"\n--- Z(N) monotonicity analysis (N = 2..{MAX_N}) ---")
z_increases = np.sum(delta_Z[2:MAX_N+1] > 0)
z_decreases = np.sum(delta_Z[2:MAX_N+1] < 0)
print(f"  Z increases: {z_increases} times ({100*z_increases/(MAX_N-1):.1f}%)")
print(f"  Z decreases: {z_decreases} times ({100*z_decreases/(MAX_N-1):.1f}%)")

# Split by prime vs composite
prime_dz = [delta_Z[N] for N in range(2, MAX_N + 1) if is_prime[N]]
comp_dz = [delta_Z[N] for N in range(2, MAX_N + 1) if not is_prime[N]]

print(f"\n  At PRIMES ({len(prime_dz)} total):")
print(f"    ΔZ > 0 (increase): {sum(1 for d in prime_dz if d > 0)} ({100*sum(1 for d in prime_dz if d > 0)/len(prime_dz):.1f}%)")
print(f"    ΔZ < 0 (decrease): {sum(1 for d in prime_dz if d < 0)} ({100*sum(1 for d in prime_dz if d < 0)/len(prime_dz):.1f}%)")
print(f"    Mean ΔZ at primes: {np.mean(prime_dz):+.6f}")
print(f"    Median ΔZ at primes: {np.median(prime_dz):+.6f}")

print(f"\n  At COMPOSITES ({len(comp_dz)} total):")
print(f"    ΔZ > 0 (increase): {sum(1 for d in comp_dz if d > 0)} ({100*sum(1 for d in comp_dz if d > 0)/len(comp_dz):.1f}%)")
print(f"    ΔZ < 0 (decrease): {sum(1 for d in comp_dz if d < 0)} ({100*sum(1 for d in comp_dz if d < 0)/len(comp_dz):.1f}%)")
print(f"    Mean ΔZ at composites: {np.mean(comp_dz):+.6f}")
print(f"    Median ΔZ at composites: {np.median(comp_dz):+.6f}")

# Z range
print(f"\n  Z range: [{np.min(Z[2:MAX_N+1]):.6f}, {np.max(Z[2:MAX_N+1]):.6f}]")
print(f"  Z mean: {np.mean(Z[2:MAX_N+1]):.6f}")
print(f"  Z std: {np.std(Z[2:MAX_N+1]):.6f}")


# ─────────────────────────────────────────────────────────────
# SECTION 3: Submartingale test for Z(N)
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SECTION 3: Submartingale Test for Z(N)")
print("=" * 70)
print("\nA submartingale satisfies E[Z(N+1) | Z(N)] ≥ Z(N), i.e., ΔZ ≥ 0 on average.")
print("We estimate conditional expectation using sliding windows.\n")

# Method 1: Running average of ΔZ
window_sizes = [10, 20, 50, 100]
for w in window_sizes:
    if w >= MAX_N - 1:
        continue
    running_avg = np.convolve(delta_Z[2:MAX_N+1], np.ones(w)/w, mode='valid')
    positive_avg = np.sum(running_avg > 0)
    total = len(running_avg)
    print(f"  Window {w:3d}: {positive_avg}/{total} running averages > 0 ({100*positive_avg/total:.1f}%)")

# Method 2: Conditional on prime vs composite
# At step N+1, if N+1 is prime, Z tends to increase; if composite, Z tends to decrease
# Overall average ΔZ:
mean_dz = np.mean(delta_Z[2:MAX_N+1])
print(f"\n  Overall mean ΔZ = {mean_dz:+.8f}")
print(f"  If > 0: Z is a submartingale (on average increases)")
print(f"  If < 0: Z is a supermartingale (on average decreases)")

# Method 3: Check submartingale property in bins of Z
print(f"\n  Conditional E[ΔZ | Z in bin]:")
z_vals = Z[2:MAX_N]
dz_vals = delta_Z[3:MAX_N+1]  # ΔZ(N+1) paired with Z(N)
n_bins = 8
z_min, z_max = np.min(z_vals), np.max(z_vals)
bin_edges = np.linspace(z_min, z_max, n_bins + 1)

print(f"  {'Z bin':>20} {'E[ΔZ|Z]':>12} {'Count':>6} {'Sub?':>5}")
print(f"  {'-'*48}")
for i in range(n_bins):
    mask = (z_vals >= bin_edges[i]) & (z_vals < bin_edges[i+1])
    if i == n_bins - 1:  # include right edge for last bin
        mask = (z_vals >= bin_edges[i]) & (z_vals <= bin_edges[i+1])
    if np.sum(mask) > 0:
        cond_mean = np.mean(dz_vals[mask])
        count = np.sum(mask)
        is_sub = "YES" if cond_mean >= 0 else "no"
        print(f"  [{bin_edges[i]:.4f}, {bin_edges[i+1]:.4f}] {cond_mean:+12.6f} {count:6d} {is_sub:>5}")


# ─────────────────────────────────────────────────────────────
# SECTION 4: Y(N) = log W(N) — Log wobble supermartingale test
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SECTION 4: Y(N) = log W(N) — Log Wobble")
print("=" * 70)
print("\nIf Y is a supermartingale, then E[log W(N+1) | log W(N)] ≤ log W(N),")
print("meaning W decreases geometrically on average.\n")

Y = np.zeros(MAX_N + 1)
for N in range(1, MAX_N + 1):
    if wobbles[N] > 0:
        Y[N] = log(wobbles[N])

delta_Y = np.zeros(MAX_N + 1)
for N in range(2, MAX_N + 1):
    delta_Y[N] = Y[N] - Y[N-1]

# Show first values
print(f"{'N':>5} {'W(N)':>12} {'Y=log W':>12} {'ΔY':>12} {'≈ΔW/W':>12} {'Type':>6}")
print("-" * 65)
for N in range(2, min(MAX_N+1, 31)):
    ntype = "PRIME" if is_prime[N] else "comp"
    ratio = delta_Y[N]
    dw_over_w = (wobbles[N] - wobbles[N-1]) / wobbles[N-1] if wobbles[N-1] > 0 else 0
    print(f"{N:5d} {wobbles[N]:12.8f} {Y[N]:12.6f} {delta_Y[N]:+12.6f} {dw_over_w:+12.6f} {ntype:>6}")

# Statistics
mean_dy = np.mean(delta_Y[2:MAX_N+1])
print(f"\n  Overall mean ΔY = {mean_dy:+.8f}")
print(f"  If < 0: Y is a supermartingale => W decreases geometrically on average")

prime_dy = [delta_Y[N] for N in range(2, MAX_N+1) if is_prime[N]]
comp_dy = [delta_Y[N] for N in range(2, MAX_N+1) if not is_prime[N]]
print(f"  Mean ΔY at primes: {np.mean(prime_dy):+.8f}")
print(f"  Mean ΔY at composites: {np.mean(comp_dy):+.8f}")

# Effective decay rate
# If Y is supermartingale with drift -c, then W(N) ~ W(1) * exp(-c*N)
# Better: since W ~ 1/(12N), log W ~ -log(12N), so ΔY ~ -1/N
print(f"\n  Theoretical ΔY ≈ -1/N for W ~ 1/(12N):")
for N in [10, 50, 100, 200, 500]:
    if N <= MAX_N:
        actual = np.mean(delta_Y[max(2, N-5):N+1])
        theory = -1.0 / N
        print(f"    N ≈ {N}: actual mean ΔY ≈ {actual:+.6f}, -1/N = {theory:+.6f}")


# ─────────────────────────────────────────────────────────────
# SECTION 5: Doob Decomposition Z = M + A
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SECTION 5: Doob Decomposition Z(N) = M(N) + A(N)")
print("=" * 70)
print("\nDoob's decomposition: any submartingale Z = M + A where:")
print("  M is a martingale (E[ΔM | past] = 0)")
print("  A is predictable and increasing (A(0) = 0, A non-decreasing)")
print("\nWe estimate A(N) = Σ_{k=2}^{N} E[ΔZ(k) | F_{k-1}]")
print("Using empirical conditional means as estimates.\n")

# Estimate E[ΔZ(N) | F_{N-1}] using the type of N (prime vs composite)
# This is a simple filtration-based estimate

A = np.zeros(MAX_N + 1)  # Predictable increasing process
M_doob = np.zeros(MAX_N + 1)  # Martingale part

# Better estimate: condition on whether N is prime
# E[ΔZ(N) | N is prime] = mean_prime_dz
# E[ΔZ(N) | N is composite] = mean_comp_dz
# These are predictable (we know if N is prime before seeing Z(N))

mean_prime_dz_val = np.mean(prime_dz)
mean_comp_dz_val = np.mean(comp_dz)

for N in range(2, MAX_N + 1):
    if is_prime[N]:
        conditional_mean = mean_prime_dz_val
    else:
        conditional_mean = mean_comp_dz_val
    A[N] = A[N-1] + conditional_mean
    M_doob[N] = Z[N] - A[N]

# Check M is roughly a martingale
delta_M = np.diff(M_doob[1:MAX_N+1])  # ΔM(N) for N = 2..MAX_N
print(f"  Predictable process A:")
print(f"    A(50) = {A[50]:.6f}")
print(f"    A(100) = {A[100]:.6f}")
print(f"    A(200) = {A[200]:.6f}")
print(f"    A({MAX_N}) = {A[MAX_N]:.6f}")
print(f"    A is {'increasing' if np.all(np.diff(A[1:MAX_N+1]) >= -1e-10) else 'NOT always increasing'}")

print(f"\n  Martingale part M:")
print(f"    Mean ΔM = {np.mean(delta_M):+.8f} (should be ≈ 0)")
print(f"    Std ΔM = {np.std(delta_M):.8f}")

# Refined Doob: condition on (prime/composite AND Mertens value)
print(f"\n  Refined conditioning on (prime/composite, M(N) sign):")
categories = {
    'prime, M>0': lambda N: is_prime[N] and mertens[N] > 0,
    'prime, M=0': lambda N: is_prime[N] and mertens[N] == 0,
    'prime, M<0': lambda N: is_prime[N] and mertens[N] < 0,
    'prime, M≤-3': lambda N: is_prime[N] and mertens[N] <= -3,
    'comp, M>0': lambda N: not is_prime[N] and mertens[N] > 0,
    'comp, M≤0': lambda N: not is_prime[N] and mertens[N] <= 0,
}

print(f"  {'Category':>16} {'E[ΔZ]':>12} {'E[ΔY]':>12} {'Count':>6}")
print(f"  {'-'*50}")
for label, cond in categories.items():
    idxs = [N for N in range(2, MAX_N+1) if cond(N)]
    if len(idxs) > 0:
        dz_cat = [delta_Z[N] for N in idxs]
        dy_cat = [delta_Y[N] for N in idxs]
        print(f"  {label:>16} {np.mean(dz_cat):+12.6f} {np.mean(dy_cat):+12.6f} {len(idxs):6d}")


# ─────────────────────────────────────────────────────────────
# SECTION 6: Multiplicative Martingale — Product Analysis
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SECTION 6: Multiplicative Product Analysis")
print("=" * 70)
print("\nDefine R(N) = W(N)/W(1) = Π_{k=2}^{N} (1 + ΔW(k)/W(k-1))")
print("If log R(N) is a supermartingale, then W decreases geometrically.\n")

log_ratios = np.zeros(MAX_N + 1)  # log(W(N)/W(N-1))
cum_log_ratio = np.zeros(MAX_N + 1)  # Σ log(W(k)/W(k-1)) = log(W(N)/W(1))

for N in range(2, MAX_N + 1):
    if wobbles[N] > 0 and wobbles[N-1] > 0:
        log_ratios[N] = log(wobbles[N] / wobbles[N-1])
        cum_log_ratio[N] = cum_log_ratio[N-1] + log_ratios[N]

print(f"  log(W(N)/W(1)) at key points:")
for N in [10, 20, 50, 100, 200, 500]:
    if N <= MAX_N:
        print(f"    N = {N:4d}: log(W(N)/W(1)) = {cum_log_ratio[N]:+.6f}, W(N)/W(1) = {wobbles[N]/wobbles[1]:.6f}")

# Variance of log-increments (for Azuma-Hoeffding)
prime_log_ratios = [log_ratios[N] for N in range(2, MAX_N+1) if is_prime[N]]
comp_log_ratios = [log_ratios[N] for N in range(2, MAX_N+1) if not is_prime[N]]

print(f"\n  Log-ratio statistics:")
print(f"    Overall: mean = {np.mean(log_ratios[2:MAX_N+1]):+.8f}, std = {np.std(log_ratios[2:MAX_N+1]):.8f}")
print(f"    Primes:  mean = {np.mean(prime_log_ratios):+.8f}, std = {np.std(prime_log_ratios):.8f}")
print(f"    Comps:   mean = {np.mean(comp_log_ratios):+.8f}, std = {np.std(comp_log_ratios):.8f}")

# Bounded differences for Azuma-Hoeffding
max_abs_log_ratio = np.max(np.abs(log_ratios[2:MAX_N+1]))
print(f"\n  Max |log(W(N)/W(N-1))| = {max_abs_log_ratio:.6f}")
print(f"  This is the bound 'c' for Azuma-Hoeffding.")
print(f"  Azuma bound: P(|Σ ΔM_k| > t) ≤ 2·exp(-t²/(2·n·c²))")
print(f"  For n = {MAX_N}, c = {max_abs_log_ratio:.4f}:")
for t_mult in [1, 2, 3]:
    t = t_mult * sqrt(MAX_N) * max_abs_log_ratio
    bound = 2 * np.exp(-t**2 / (2 * MAX_N * max_abs_log_ratio**2))
    print(f"    t = {t_mult}·√n·c = {t:.4f}: P(deviation > t) ≤ {bound:.6f}")


# ─────────────────────────────────────────────────────────────
# SECTION 7: Z(p) - Z(p-1) at primes with M(p) ≤ -3
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SECTION 7: ΔZ at Primes with M(p) ≤ -3")
print("=" * 70)
print("\nIf Z(p) - Z(p-1) > 0 for primes with M(p) ≤ -3, then")
print("W(p) > W(p-1)·(p-1)/p, meaning W decreases slower than 1/p.\n")

print(f"{'p':>5} {'M(p)':>6} {'W(p-1)':>12} {'W(p)':>12} {'ΔW':>12} {'Z(p-1)':>10} {'Z(p)':>10} {'ΔZ':>10}")
print("-" * 82)

count_positive_dz = 0
count_total = 0
for p in range(2, MAX_N + 1):
    if is_prime[p] and mertens[p] <= -3:
        dw = wobbles[p] - wobbles[p-1]
        dz = Z[p] - Z[p-1]
        count_total += 1
        if dz > 0:
            count_positive_dz += 1
        if p <= 200 or (p <= MAX_N and count_total <= 50):
            print(f"{p:5d} {mertens[p]:6d} {wobbles[p-1]:12.8f} {wobbles[p]:12.8f} {dw:+12.8f} "
                  f"{Z[p-1]:10.6f} {Z[p]:10.6f} {dz:+10.6f}")

print(f"\nPrimes with M(p) ≤ -3: {count_total} total")
print(f"  ΔZ > 0: {count_positive_dz} ({100*count_positive_dz/max(1,count_total):.1f}%)")
print(f"  ΔZ ≤ 0: {count_total - count_positive_dz} ({100*(count_total - count_positive_dz)/max(1,count_total):.1f}%)")


# ─────────────────────────────────────────────────────────────
# SECTION 8: Quadratic variation and BDG inequality
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SECTION 8: Quadratic Variation and BDG Inequality")
print("=" * 70)
print("\nBurkholder-Davis-Gundy: E[max |M_k|^p] ~ E[[M]_N^{p/2}]")
print("where [M]_N = Σ (ΔM_k)² is the quadratic variation.\n")

# Quadratic variation of Z
QV_Z = np.cumsum(delta_Z[2:MAX_N+1]**2)
print(f"  Quadratic variation [Z]_N:")
for N in [10, 50, 100, 200, 500]:
    if N - 1 <= len(QV_Z):
        print(f"    [Z]_{N} = {QV_Z[N-2]:.6f}")

# Quadratic variation of the martingale part
QV_M = np.cumsum(delta_M**2)
print(f"\n  Quadratic variation [M]_N (martingale part):")
for N in [10, 50, 100, 200, 500]:
    if N - 2 < len(QV_M):
        print(f"    [M]_{N} = {QV_M[N-2]:.6f}")

# Growth rate of QV
print(f"\n  [Z]_N / N (should stabilize if increments are stationary):")
for N in [10, 50, 100, 200, 500]:
    if N - 1 <= len(QV_Z):
        print(f"    [Z]_{N} / {N} = {QV_Z[N-2]/N:.6f}")

# BDG constant estimate
print(f"\n  For BDG with p=2: E[max|M|²] ≤ C · E[[M]_N]")
print(f"  [M]_{MAX_N} = {QV_M[-1]:.6f}")
print(f"  max|M| up to {MAX_N} = {np.max(np.abs(M_doob[2:MAX_N+1])):.6f}")


# ─────────────────────────────────────────────────────────────
# SECTION 9: Alternative transformation — W(N) · N^α
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SECTION 9: Optimal Exponent — W(N) · N^α")
print("=" * 70)
print("\nFind α such that T(N) = W(N) · N^α is closest to a martingale.")
print("If W(N) ~ c/N^β, then T(N) = c·N^{α-β}, which is martingale iff α = β.\n")

# Estimate β from W(N) ≈ c / N^β
# log W(N) ≈ log c - β log N
# Linear regression: Y = a + b·X where Y = log W, X = log N
valid = np.arange(10, MAX_N + 1)
log_W = np.log(wobbles[valid])
log_N = np.log(valid.astype(float))

# Linear regression
X = np.column_stack([np.ones(len(valid)), log_N])
coeffs = np.linalg.lstsq(X, log_W, rcond=None)[0]
log_c_est = coeffs[0]
beta_est = -coeffs[1]

print(f"  Regression: log W ≈ {coeffs[0]:.4f} + ({coeffs[1]:.4f}) · log N")
print(f"  => W(N) ≈ {np.exp(log_c_est):.6f} / N^{beta_est:.4f}")
print(f"  (Expected: W ~ 1/(12N) => β = 1, c = 1/12 ≈ {1/12:.6f})")

# Try several α values
print(f"\n  {'α':>6} {'Mean Δ(W·N^α)':>16} {'Std Δ(W·N^α)':>16} {'Sub?':>5}")
print(f"  {'-'*48}")
best_alpha = None
best_mean_abs = float('inf')

for alpha in np.arange(0.5, 1.6, 0.05):
    T = wobbles[2:MAX_N+1] * (np.arange(2, MAX_N+1, dtype=float) ** alpha)
    dT = np.diff(T)
    mean_dT = np.mean(dT)
    std_dT = np.std(dT)
    is_sub = "YES" if mean_dT > 0 else "no"
    if abs(mean_dT) < best_mean_abs:
        best_mean_abs = abs(mean_dT)
        best_alpha = alpha
    if abs(alpha - round(alpha, 1)) < 0.001 or abs(alpha - beta_est) < 0.03:
        print(f"  {alpha:6.2f} {mean_dT:+16.8f} {std_dT:16.8f} {is_sub:>5}")

print(f"\n  Best α for martingale (mean ΔT ≈ 0): α ≈ {best_alpha:.2f}")
print(f"  This means W(N) · N^{best_alpha:.2f} is closest to a martingale.")
print(f"  Interpretation: W(N) decays like 1/N^{best_alpha:.2f} on average.")

# For the best alpha, check submartingale property more carefully
T_best = wobbles[2:MAX_N+1] * (np.arange(2, MAX_N+1, dtype=float) ** best_alpha)
dT_best = np.diff(T_best)
print(f"\n  For α = {best_alpha:.2f}:")
print(f"    ΔT > 0: {np.sum(dT_best > 0)} ({100*np.sum(dT_best > 0)/len(dT_best):.1f}%)")
print(f"    ΔT < 0: {np.sum(dT_best < 0)} ({100*np.sum(dT_best < 0)/len(dT_best):.1f}%)")


# ─────────────────────────────────────────────────────────────
# SECTION 10: Summary and Conclusions
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SECTION 10: SUMMARY AND CONCLUSIONS")
print("=" * 70)

print(f"""
FINDINGS (N = 2..{MAX_N}):

1. Z(N) = N · W(N):
   - Range: [{np.min(Z[2:MAX_N+1]):.4f}, {np.max(Z[2:MAX_N+1]):.4f}]
   - Mean ΔZ = {np.mean(delta_Z[2:MAX_N+1]):+.6f}
   - Z is {'a SUBMARTINGALE (increases on avg)' if np.mean(delta_Z[2:MAX_N+1]) > 0 else 'a SUPERMARTINGALE (decreases on avg)' if np.mean(delta_Z[2:MAX_N+1]) < 0 else 'approximately a MARTINGALE'}

2. Y(N) = log W(N):
   - Mean ΔY = {np.mean(delta_Y[2:MAX_N+1]):+.6f}
   - Y is {'a SUPERMARTINGALE => W decreases geometrically' if np.mean(delta_Y[2:MAX_N+1]) < 0 else 'NOT a supermartingale'}

3. Doob Decomposition Z = M + A:
   - Predictable part A({MAX_N}) = {A[MAX_N]:.4f}
   - A is {'monotone increasing' if np.all(np.diff(A[1:MAX_N+1]) >= -1e-10) else 'not always increasing'}
   - Martingale part: mean ΔM = {np.mean(delta_M):+.8f}, std = {np.std(delta_M):.6f}

4. Primes with M(p) ≤ -3:
   - ΔZ > 0 in {count_positive_dz}/{count_total} cases ({100*count_positive_dz/max(1,count_total):.1f}%)
   - These primes push Z upward (W decays slower than 1/N)

5. Optimal exponent:
   - W(N) ~ c/N^β with β ≈ {beta_est:.4f}
   - W(N)·N^{best_alpha:.2f} is closest to martingale

6. Multiplicative analysis:
   - Max |log(W(N)/W(N-1))| = {max_abs_log_ratio:.4f} (Azuma bound)
   - log(W({MAX_N})/W(1)) = {cum_log_ratio[MAX_N]:+.4f}

PROBABILISTIC IMPLICATIONS:
   - If Z is a submartingale bounded in L², Doob's convergence theorem
     implies Z(N) → Z(∞) a.s. (with respect to a suitable probability).
   - The bounded quadratic variation [Z]_N / N → σ² suggests
     CLT-type concentration of Z around its drift.
   - Azuma-Hoeffding with c = {max_abs_log_ratio:.4f} gives exponential
     concentration bounds for deviations of log W from its expected path.
""")

elapsed = time.time() - start_time
print(f"Total runtime: {elapsed:.1f}s")
