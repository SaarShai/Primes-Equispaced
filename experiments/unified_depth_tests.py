#!/usr/bin/env python3
"""Unified tests: zeta detection, sign prediction, sparse approximation.
Uses REAL data from bc_verify_100000_c.csv."""

import numpy as np
import csv, math, os

DATA = os.path.expanduser("~/Desktop/Farey-Local/experiments/bc_verify_100000_c.csv")

# Load data
primes, R_vals, bpc_vals = [], [], []
with open(DATA) as f:
    reader = csv.DictReader(f)
    for row in reader:
        primes.append(int(row['p']))
        R_vals.append(float(row['R']))
        bpc_vals.append(float(row['B_plus_C']))

primes = np.array(primes, dtype=float)
R_vals = np.array(R_vals)
bpc_vals = np.array(bpc_vals)

# ΔW sign: B+C > 0 means ΔW < 0 (for qualifying primes where A > D roughly)
# Actually R > 0 correlates with ΔW < 0. Use R as the sign proxy.
dw_sign = -np.sign(R_vals)  # ΔW < 0 when R > 0

print(f"Loaded {len(primes)} qualifying primes, p_max = {primes[-1]:.0f}")
print(f"R > 0: {np.sum(R_vals > 0)} / {len(R_vals)} ({100*np.mean(R_vals > 0):.1f}%)")
print()

# ===== TEST 1: ZETA ZERO DETECTION FROM FAREY DATA =====
print("=" * 60)
print("TEST 1: BLIND ZETA ZERO DETECTION")
print("=" * 60)

gamma_grid = np.linspace(5, 50, 9001)  # resolution 0.005
log_p = np.log(primes)

# Farey spectral function: F(γ) = |Σ R(p) · p^{-1/2-iγ}|²
F_gamma = np.zeros(len(gamma_grid))
for i, gamma in enumerate(gamma_grid):
    terms = R_vals * primes**(-0.5) * np.exp(-1j * gamma * log_p)
    F_gamma[i] = np.abs(np.sum(terms))**2

# Find peaks (local maxima above threshold)
threshold = np.percentile(F_gamma, 95)
peaks = []
for i in range(1, len(F_gamma) - 1):
    if F_gamma[i] > F_gamma[i-1] and F_gamma[i] > F_gamma[i+1] and F_gamma[i] > threshold:
        peaks.append((gamma_grid[i], F_gamma[i]))

peaks.sort(key=lambda x: -x[1])
top_peaks = peaks[:10]

known_zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052]

print(f"Top 10 detected peaks:")
for g, h in top_peaks:
    # Check proximity to known zeros
    closest = min(known_zeros, key=lambda z: abs(z - g))
    match = "✓ MATCH" if abs(closest - g) < 0.5 else ""
    print(f"  γ = {g:.3f}  (height = {h:.1f})  nearest known zero: {closest:.3f} {match}")

matched = sum(1 for g, h in top_peaks[:5] if any(abs(g - z) < 0.5 for z in known_zeros))
print(f"\nTop 5 peaks matching known zeros (within ±0.5): {matched}/5")
print()

# ===== TEST 2: SIGN PREDICTION =====
print("=" * 60)
print("TEST 2: ΔW SIGN PREDICTION via γ₁ phase formula")
print("=" * 60)

gamma1 = 14.1347
# Test multiple phase values
for phi in [4.590, 5.28, 4.0, 5.0]:
    pred = -np.sign(np.cos(gamma1 * log_p + phi))
    # Use sign of -R as proxy for ΔW sign (R > 0 → ΔW < 0)
    actual = np.sign(R_vals)  # positive R → ΔW negative → we predict negative
    # Since almost all R > 0, predict "negative ΔW" = predict R > 0
    # The phase formula predicts sgn(ΔW) = -sgn(cos(γ₁·log(p) + φ))
    # ΔW < 0 iff R > 0 (for our data). So actual_dw_sign = -1 when R > 0.
    actual_dw = np.where(R_vals > 0, -1, 1)
    pred_dw = -np.sign(np.cos(gamma1 * log_p + phi))
    accuracy = np.mean(actual_dw == pred_dw)
    print(f"  φ = {phi:.3f}: accuracy = {accuracy:.1%}")

# By p-range
best_phi = 5.28
pred_dw = -np.sign(np.cos(gamma1 * log_p + best_phi))
actual_dw = np.where(R_vals > 0, -1, 1)
for lo, hi in [(0, 1000), (1000, 10000), (10000, 50000), (50000, 100000)]:
    mask = (primes >= lo) & (primes < hi)
    if mask.sum() > 0:
        acc = np.mean(actual_dw[mask] == pred_dw[mask])
        print(f"  p ∈ [{lo}, {hi}): accuracy = {acc:.1%} (n={mask.sum()})")
print()

# ===== TEST 3: SPARSE APPROXIMATION (using R values) =====
print("=" * 60)
print("TEST 3: Do primes with extreme R dominate the spectral signal?")
print("=" * 60)

# Sort primes by |R| (proxy for "depth contribution")
order = np.argsort(-np.abs(R_vals))

for pct in [10, 20, 30, 50, 100]:
    n_use = max(1, int(len(primes) * pct / 100))
    idx = order[:n_use]

    # Spectral function using only top pct% primes
    F_sub = np.zeros(len(gamma_grid))
    for i, gamma in enumerate(gamma_grid):
        terms = R_vals[idx] * primes[idx]**(-0.5) * np.exp(-1j * gamma * log_p[idx])
        F_sub[i] = np.abs(np.sum(terms))**2

    # Find γ₁ peak
    g1_region = (gamma_grid > 13) & (gamma_grid < 16)
    peak_height = np.max(F_sub[g1_region])
    peak_loc = gamma_grid[g1_region][np.argmax(F_sub[g1_region])]

    # γ₂ peak for comparison
    g2_region = (gamma_grid > 20) & (gamma_grid < 22)
    g2_height = np.max(F_sub[g2_region])

    ratio = peak_height / (g2_height + 1e-10)
    print(f"  Top {pct:3d}% primes ({n_use:4d}): γ₁ peak at {peak_loc:.2f}, "
          f"γ₁/γ₂ ratio = {ratio:.1f}")

print("\nIf γ₁/γ₂ ratio INCREASES with fewer primes, depth-filtering amplifies γ₁.")
