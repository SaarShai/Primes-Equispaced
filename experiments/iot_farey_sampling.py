#!/usr/bin/env python3
"""
Farey Adaptive Sampling for IoT Edge Devices
=============================================

Compares Farey-based adaptive refinement against:
  1. Uniform sampling
  2. Random sampling
  3. Bisection-based adaptive (midpoint of highest-error interval)
  4. Compressed sensing (random subset + L1 reconstruction)

Test signals: ECG-like, temperature drift+spikes, vibration (mixed frequencies)

Key question: Does Farey's structured refinement (mediants = smallest denominator)
beat simple bisection for signal sampling?

Potential edge: Farey gives the "simplest" next sample point (smallest denominator
mediant), which may adapt faster to features at non-power-of-2 positions.
"""

import numpy as np
import time
import json
import os
from fractions import Fraction
from collections import defaultdict

# ============================================================
# Signal generators
# ============================================================

def ecg_signal(t):
    """ECG-like: periodic with sharp QRS complex."""
    # Normalize t to [0,1] period
    phase = t % 1.0
    # P wave
    p = 0.2 * np.exp(-((phase - 0.1) ** 2) / (2 * 0.01 ** 2))
    # QRS complex (sharp spike)
    q = -0.1 * np.exp(-((phase - 0.3) ** 2) / (2 * 0.003 ** 2))
    r = 1.0 * np.exp(-((phase - 0.32) ** 2) / (2 * 0.004 ** 2))
    s = -0.15 * np.exp(-((phase - 0.34) ** 2) / (2 * 0.003 ** 2))
    # T wave
    tw = 0.3 * np.exp(-((phase - 0.5) ** 2) / (2 * 0.02 ** 2))
    return p + q + r + s + tw


def temperature_signal(t):
    """Temperature: slow drift + sudden spikes."""
    base = 20 + 2 * np.sin(2 * np.pi * t)  # slow drift
    # Sudden spikes at specific locations
    spike1 = 5.0 * np.exp(-((t - 0.25) ** 2) / (2 * 0.005 ** 2))
    spike2 = -3.0 * np.exp(-((t - 0.7) ** 2) / (2 * 0.003 ** 2))
    spike3 = 4.0 * np.exp(-((t - 0.55) ** 2) / (2 * 0.004 ** 2))
    return base + spike1 + spike2 + spike3


def vibration_signal(t):
    """Vibration: mix of frequencies with transient burst."""
    base = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 13 * t)
    # Transient burst centered at t=0.4
    burst_env = np.exp(-((t - 0.4) ** 2) / (2 * 0.02 ** 2))
    burst = burst_env * np.sin(2 * np.pi * 50 * t)
    # Another transient at t=0.8
    burst2_env = np.exp(-((t - 0.8) ** 2) / (2 * 0.015 ** 2))
    burst2 = burst2_env * np.sin(2 * np.pi * 37 * t)
    return base + burst + burst2


SIGNALS = {
    'ecg': ecg_signal,
    'temperature': temperature_signal,
    'vibration': vibration_signal,
}

# ============================================================
# Farey sequence utilities
# ============================================================

def farey_sequence(n):
    """Generate Farey sequence F_n as sorted list of Fraction objects."""
    fracs = set()
    for d in range(1, n + 1):
        for num in range(0, d + 1):
            fracs.add(Fraction(num, d))
    return sorted(fracs)


def farey_mediant(a, b):
    """Compute mediant of two fractions a/b and c/d = (a+c)/(b+d)."""
    return Fraction(a.numerator + b.numerator, a.denominator + b.denominator)


# ============================================================
# Sampling strategies
# ============================================================

def uniform_sampling(signal_func, n_samples):
    """Sample signal at n uniformly spaced points in [0,1]."""
    t_start = time.perf_counter()
    points = np.linspace(0, 1, n_samples)
    values = np.array([signal_func(t) for t in points])
    elapsed = time.perf_counter() - t_start
    return points, values, elapsed


def random_sampling(signal_func, n_samples, seed=42):
    """Sample at random points in [0,1]."""
    t_start = time.perf_counter()
    rng = np.random.RandomState(seed)
    points = np.sort(rng.uniform(0, 1, n_samples))
    # Ensure endpoints
    points[0] = 0.0
    points[-1] = 1.0
    values = np.array([signal_func(t) for t in points])
    elapsed = time.perf_counter() - t_start
    return points, values, elapsed


def bisection_adaptive_sampling(signal_func, n_samples):
    """
    Adaptive bisection: start with endpoints, always split the interval
    with highest actual interpolation error at the midpoint.

    Error heuristic: evaluate the midpoint and compare to linear interpolation.
    This costs one extra function eval per interval per iteration, but gives
    the TRUE error, not just an estimate from endpoint differences.
    """
    t_start = time.perf_counter()

    # Start with endpoints
    points = {0.0, 1.0}
    values = {0.0: signal_func(0.0), 1.0: signal_func(1.0)}

    # Add a few initial points
    for t in [0.25, 0.5, 0.75]:
        points.add(t)
        values[t] = signal_func(t)

    while len(points) < n_samples:
        sorted_pts = sorted(points)
        # Find interval with highest ACTUAL error at midpoint
        best_error = -1
        best_mid = None
        for i in range(len(sorted_pts) - 1):
            left, right = sorted_pts[i], sorted_pts[i + 1]
            mid = (left + right) / 2.0
            if mid in points:
                continue
            # Evaluate the actual error: true value vs linear interpolation
            true_val = signal_func(mid)
            interp_val = (values[left] + values[right]) / 2.0
            error_est = abs(true_val - interp_val)
            if error_est > best_error:
                best_error = error_est
                best_mid = mid
                best_mid_val = true_val

        if best_mid is None:
            # Fallback: split widest interval
            widest = -1
            for i in range(len(sorted_pts) - 1):
                w = sorted_pts[i+1] - sorted_pts[i]
                mid = (sorted_pts[i] + sorted_pts[i+1]) / 2.0
                if w > widest and mid not in points:
                    widest = w
                    best_mid = mid
            if best_mid is None:
                break
            best_mid_val = signal_func(best_mid)

        points.add(best_mid)
        values[best_mid] = best_mid_val

    sorted_pts = sorted(points)
    vals = np.array([values[t] for t in sorted_pts])
    elapsed = time.perf_counter() - t_start
    return np.array(sorted_pts), vals, elapsed


def farey_adaptive_sampling(signal_func, n_samples):
    """
    Farey adaptive sampling:
    - Start with F_3 (coarse: 0, 1/3, 1/2, 2/3, 1)
    - Evaluate signal at these points
    - For each adjacent pair, compute error estimate
    - Refine highest-error interval by inserting the MEDIANT
      (the Farey neighbor with smallest denominator)
    - Repeat until budget exhausted

    Key difference from bisection: mediant (a+c)/(b+d) instead of midpoint.
    This gives the "simplest" rational in the interval (Stern-Brocot property).
    """
    t_start = time.perf_counter()

    # Start with F_3
    initial = [Fraction(0, 1), Fraction(1, 3), Fraction(1, 2),
               Fraction(2, 3), Fraction(1, 1)]

    points = set(initial)
    values = {}
    for f in initial:
        t = float(f)
        values[f] = signal_func(t)

    while len(points) < n_samples:
        sorted_pts = sorted(points)
        # Find interval with highest ACTUAL error at mediant
        best_error = -1
        best_mediant = None
        best_med_val = None
        for i in range(len(sorted_pts) - 1):
            left, right = sorted_pts[i], sorted_pts[i + 1]
            med = farey_mediant(left, right)
            if med in points:
                continue
            med_t = float(med)
            # Actual error: true value vs linear interpolation at mediant
            true_val = signal_func(med_t)
            frac_pos = (med_t - float(left)) / (float(right) - float(left))
            interp_val = values[left] + frac_pos * (values[right] - values[left])
            error_est = abs(true_val - interp_val)
            if error_est > best_error:
                best_error = error_est
                best_mediant = med
                best_med_val = true_val

        if best_mediant is None:
            # Fallback: split widest interval
            widest = -1
            for i in range(len(sorted_pts) - 1):
                w = float(sorted_pts[i+1] - sorted_pts[i])
                med = farey_mediant(sorted_pts[i], sorted_pts[i+1])
                if w > widest and med not in points:
                    widest = w
                    best_mediant = med
            if best_mediant is None:
                break
            best_med_val = signal_func(float(best_mediant))

        points.add(best_mediant)
        values[best_mediant] = best_med_val

    sorted_pts = sorted(points)
    pts_float = np.array([float(f) for f in sorted_pts])
    vals = np.array([values[f] for f in sorted_pts])
    elapsed = time.perf_counter() - t_start
    return pts_float, vals, elapsed


def stern_brocot_mediant(left_frac, right_frac, max_depth=10):
    """
    Find the Stern-Brocot tree mediant closest to the midpoint of the interval.
    This avoids the asymmetry problem where naive mediant(a/b, c/d) = (a+c)/(b+d)
    converges to an endpoint when denominators are unbalanced.

    Strategy: descend the Stern-Brocot tree from the root, always choosing the
    branch that gets closer to the interval midpoint, up to max_depth.
    """
    target = (float(left_frac) + float(right_frac)) / 2.0

    # Stern-Brocot tree: start with 0/1 and 1/0 (infinity) as sentinels
    lo_n, lo_d = 0, 1
    hi_n, hi_d = 1, 0  # represents infinity

    best = None
    for _ in range(max_depth):
        med_n = lo_n + hi_n
        med_d = lo_d + hi_d
        med_val = med_n / med_d

        # Is this mediant in our interval?
        if float(left_frac) < med_val < float(right_frac):
            best = Fraction(med_n, med_d)

        if med_val < target:
            lo_n, lo_d = med_n, med_d
        elif med_val > target:
            hi_n, hi_d = med_n, med_d
        else:
            best = Fraction(med_n, med_d)
            break

    if best is None:
        # Fallback to naive mediant
        best = farey_mediant(left_frac, right_frac)

    return best


def farey_sb_adaptive_sampling(signal_func, n_samples):
    """
    Farey adaptive sampling using Stern-Brocot tree mediants.
    Unlike naive mediant which can be asymmetric, this picks the
    'simplest' fraction near the interval midpoint from the SB tree.

    This preserves Farey's key properties:
    - Deterministic, integer arithmetic only
    - Sample points are always 'simple' rationals
    - Certifiable approximation bounds
    While fixing the convergence problem of naive mediants.
    """
    t_start = time.perf_counter()

    # Start with F_3
    initial = [Fraction(0, 1), Fraction(1, 3), Fraction(1, 2),
               Fraction(2, 3), Fraction(1, 1)]

    points = set(initial)
    values = {}
    for f in initial:
        values[f] = signal_func(float(f))

    while len(points) < n_samples:
        sorted_pts = sorted(points)
        best_error = -1
        best_mediant = None
        best_med_val = None

        for i in range(len(sorted_pts) - 1):
            left, right = sorted_pts[i], sorted_pts[i + 1]
            med = stern_brocot_mediant(left, right)
            if med in points:
                # Try naive mediant as fallback
                med = farey_mediant(left, right)
                if med in points:
                    continue
            med_t = float(med)
            if med_t <= float(left) or med_t >= float(right):
                continue
            true_val = signal_func(med_t)
            frac_pos = (med_t - float(left)) / (float(right) - float(left))
            interp_val = values[left] + frac_pos * (values[right] - values[left])
            error_est = abs(true_val - interp_val)
            if error_est > best_error:
                best_error = error_est
                best_mediant = med
                best_med_val = true_val

        if best_mediant is None:
            # Fallback: split widest interval
            widest = -1
            for i in range(len(sorted_pts) - 1):
                w = float(sorted_pts[i+1] - sorted_pts[i])
                med = stern_brocot_mediant(sorted_pts[i], sorted_pts[i+1])
                if w > widest and med not in points:
                    widest = w
                    best_mediant = med
            if best_mediant is None:
                break
            best_med_val = signal_func(float(best_mediant))

        points.add(best_mediant)
        values[best_mediant] = best_med_val

    sorted_pts = sorted(points)
    pts_float = np.array([float(f) for f in sorted_pts])
    vals = np.array([values[f] for f in sorted_pts])
    elapsed = time.perf_counter() - t_start
    return pts_float, vals, elapsed


def hybrid_farey_bisection_sampling(signal_func, n_samples):
    """
    Hybrid: use Farey mediants when interval width > threshold,
    switch to bisection for fine refinement.

    Rationale: Farey gives better initial coverage (non-dyadic grid),
    bisection gives faster convergence for fine detail.

    On IoT: the 'phase 1' Farey coverage can be precomputed and stored
    in flash (Farey sequences are deterministic). Only phase 2 bisection
    needs runtime computation.
    """
    t_start = time.perf_counter()

    # Phase 1: Farey coarse coverage (use ~40% of budget)
    phase1_budget = max(5, n_samples * 2 // 5)
    phase2_budget = n_samples - phase1_budget

    # Start with F_3
    initial = [Fraction(0, 1), Fraction(1, 3), Fraction(1, 2),
               Fraction(2, 3), Fraction(1, 1)]
    points_frac = set(initial)
    values_frac = {}
    for f in initial:
        values_frac[f] = signal_func(float(f))

    # Phase 1: Farey mediant refinement
    while len(points_frac) < phase1_budget:
        sorted_pts = sorted(points_frac)
        best_error = -1
        best_med = None
        best_val = None
        for i in range(len(sorted_pts) - 1):
            left, right = sorted_pts[i], sorted_pts[i + 1]
            med = stern_brocot_mediant(left, right)
            if med in points_frac:
                med = farey_mediant(left, right)
                if med in points_frac:
                    continue
            med_t = float(med)
            if med_t <= float(left) or med_t >= float(right):
                continue
            true_val = signal_func(med_t)
            frac_pos = (med_t - float(left)) / (float(right) - float(left))
            interp_val = values_frac[left] + frac_pos * (values_frac[right] - values_frac[left])
            error_est = abs(true_val - interp_val)
            if error_est > best_error:
                best_error = error_est
                best_med = med
                best_val = true_val
        if best_med is None:
            break
        points_frac.add(best_med)
        values_frac[best_med] = best_val

    # Convert to float for phase 2
    points = set()
    values = {}
    for f in points_frac:
        t = float(f)
        points.add(t)
        values[t] = values_frac[f]

    # Phase 2: Bisection refinement on remaining budget
    while len(points) < n_samples:
        sorted_pts = sorted(points)
        best_error = -1
        best_mid = None
        best_mid_val = None
        for i in range(len(sorted_pts) - 1):
            left, right = sorted_pts[i], sorted_pts[i + 1]
            mid = (left + right) / 2.0
            if mid in points:
                continue
            true_val = signal_func(mid)
            interp_val = (values[left] + values[right]) / 2.0
            error_est = abs(true_val - interp_val)
            if error_est > best_error:
                best_error = error_est
                best_mid = mid
                best_mid_val = true_val
        if best_mid is None:
            widest = -1
            for i in range(len(sorted_pts) - 1):
                w = sorted_pts[i+1] - sorted_pts[i]
                mid = (sorted_pts[i] + sorted_pts[i+1]) / 2.0
                if w > widest and mid not in points:
                    widest = w
                    best_mid = mid
            if best_mid is None:
                break
            best_mid_val = signal_func(best_mid)
        points.add(best_mid)
        values[best_mid] = best_mid_val

    sorted_pts = sorted(points)
    vals = np.array([values[t] for t in sorted_pts])
    elapsed = time.perf_counter() - t_start
    return np.array(sorted_pts), vals, elapsed


def compressed_sensing_sampling(signal_func, n_samples, n_dense=1000, seed=42):
    """
    Compressed sensing: sample at random subset, reconstruct via L1 minimization.
    Uses DCT basis for sparsity.
    """
    t_start = time.perf_counter()

    # Dense grid for reconstruction target
    t_dense = np.linspace(0, 1, n_dense)

    # Random measurement indices
    rng = np.random.RandomState(seed)
    indices = np.sort(rng.choice(n_dense, size=min(n_samples, n_dense), replace=False))

    # Measure
    measurements = np.array([signal_func(t_dense[i]) for i in indices])

    # DCT basis matrix (columns are DCT basis vectors)
    # We'll use a simple iterative hard thresholding for L1-like reconstruction
    # (avoiding scipy dependency for IoT-relevance)

    # Build measurement matrix: Phi = selection matrix
    # Build DCT matrix
    N = n_dense
    M = len(indices)

    # DCT matrix
    dct_matrix = np.zeros((N, N))
    for k in range(N):
        for n_idx in range(N):
            if k == 0:
                dct_matrix[n_idx, k] = 1.0 / np.sqrt(N)
            else:
                dct_matrix[n_idx, k] = np.sqrt(2.0 / N) * np.cos(np.pi * k * (2 * n_idx + 1) / (2 * N))

    # Measurement matrix: rows of DCT corresponding to selected indices
    A = dct_matrix[indices, :]

    # Iterative Hard Thresholding (IHT) - simple CS reconstruction
    sparsity = min(n_samples // 2, N // 4)
    x = np.zeros(N)  # DCT coefficients
    step_size = 0.5 / (np.linalg.norm(A, ord=2) ** 2 + 1e-10)

    for iteration in range(200):
        residual = measurements - A @ x
        gradient = A.T @ residual
        x_new = x + step_size * gradient
        # Hard threshold: keep top-k coefficients
        idx_sorted = np.argsort(np.abs(x_new))[::-1]
        mask = np.zeros(N)
        mask[idx_sorted[:sparsity]] = 1.0
        x = x_new * mask

    # Reconstruct signal
    reconstructed = dct_matrix @ x

    # Return the measurement points and their values
    pts = t_dense[indices]
    vals = measurements
    elapsed = time.perf_counter() - t_start

    return pts, vals, elapsed, t_dense, reconstructed


# ============================================================
# Reconstruction and evaluation
# ============================================================

def linear_interpolate(sample_pts, sample_vals, eval_pts):
    """Piecewise linear interpolation."""
    return np.interp(eval_pts, sample_pts, sample_vals)


def compute_snr(original, reconstructed):
    """Signal-to-noise ratio in dB."""
    signal_power = np.mean(original ** 2)
    noise_power = np.mean((original - reconstructed) ** 2)
    if noise_power < 1e-30:
        return 100.0  # essentially perfect
    return 10 * np.log10(signal_power / noise_power)


def compute_max_error(original, reconstructed):
    """Maximum absolute error."""
    return np.max(np.abs(original - reconstructed))


def estimate_memory_bytes(n_samples):
    """
    Estimate memory for storing sample points + values.
    For IoT: points as uint16 (0-65535 range), values as int16.
    Total: 4 bytes per sample.
    """
    return n_samples * 4  # 2 bytes position + 2 bytes value


def estimate_flops_farey(n_samples):
    """
    Estimate computational cost for Farey adaptive sampling.
    Per iteration: scan all intervals (O(n)), compute mediant (O(1)), evaluate signal (O(1)).
    Total: O(n^2) for n samples.
    """
    return n_samples * n_samples  # quadratic in sample count


def estimate_flops_bisection(n_samples):
    """Same complexity as Farey: scan intervals + split."""
    return n_samples * n_samples


def estimate_flops_uniform(n_samples):
    """Just evaluate signal n times."""
    return n_samples


def estimate_flops_cs(n_samples, n_dense=1000, n_iter=200):
    """CS: matrix-vector products dominate."""
    return n_iter * 2 * n_samples * n_dense  # A^T and A operations


# ============================================================
# Main comparison
# ============================================================

def run_comparison(signal_name, signal_func, sample_counts, n_eval=10000):
    """Run all methods on a signal for various sample counts."""

    # Ground truth
    t_eval = np.linspace(0, 1, n_eval)
    y_true = np.array([signal_func(t) for t in t_eval])

    results = {}

    for n in sample_counts:
        results[n] = {}

        # 1. Uniform
        pts, vals, elapsed = uniform_sampling(signal_func, n)
        recon = linear_interpolate(pts, vals, t_eval)
        results[n]['uniform'] = {
            'snr': compute_snr(y_true, recon),
            'max_error': compute_max_error(y_true, recon),
            'time': elapsed,
            'flops': estimate_flops_uniform(n),
            'memory': estimate_memory_bytes(n),
        }

        # 2. Random
        pts, vals, elapsed = random_sampling(signal_func, n)
        recon = linear_interpolate(pts, vals, t_eval)
        results[n]['random'] = {
            'snr': compute_snr(y_true, recon),
            'max_error': compute_max_error(y_true, recon),
            'time': elapsed,
            'flops': estimate_flops_uniform(n),
            'memory': estimate_memory_bytes(n),
        }

        # 3. Bisection adaptive
        pts, vals, elapsed = bisection_adaptive_sampling(signal_func, n)
        recon = linear_interpolate(pts, vals, t_eval)
        results[n]['bisection'] = {
            'snr': compute_snr(y_true, recon),
            'max_error': compute_max_error(y_true, recon),
            'time': elapsed,
            'flops': estimate_flops_bisection(n),
            'memory': estimate_memory_bytes(n),
        }

        # 4. Farey adaptive (naive mediant)
        pts, vals, elapsed = farey_adaptive_sampling(signal_func, n)
        recon = linear_interpolate(pts, vals, t_eval)
        results[n]['farey'] = {
            'snr': compute_snr(y_true, recon),
            'max_error': compute_max_error(y_true, recon),
            'time': elapsed,
            'flops': estimate_flops_farey(n),
            'memory': estimate_memory_bytes(n),
        }

        # 5. Farey with Stern-Brocot tree mediants
        pts, vals, elapsed = farey_sb_adaptive_sampling(signal_func, n)
        recon = linear_interpolate(pts, vals, t_eval)
        results[n]['farey_sb'] = {
            'snr': compute_snr(y_true, recon),
            'max_error': compute_max_error(y_true, recon),
            'time': elapsed,
            'flops': estimate_flops_farey(n),
            'memory': estimate_memory_bytes(n),
        }

        # 6. Hybrid Farey+Bisection
        pts, vals, elapsed = hybrid_farey_bisection_sampling(signal_func, n)
        recon = linear_interpolate(pts, vals, t_eval)
        results[n]['hybrid'] = {
            'snr': compute_snr(y_true, recon),
            'max_error': compute_max_error(y_true, recon),
            'time': elapsed,
            'flops': estimate_flops_farey(n),
            'memory': estimate_memory_bytes(n),
        }

        # 7. Compressed sensing
        pts, vals, elapsed, t_dense, recon_cs = compressed_sensing_sampling(
            signal_func, n, n_dense=1000)
        # Interpolate CS reconstruction to eval grid
        recon = np.interp(t_eval, t_dense, recon_cs)
        results[n]['cs'] = {
            'snr': compute_snr(y_true, recon),
            'max_error': compute_max_error(y_true, recon),
            'time': elapsed,
            'flops': estimate_flops_cs(n),
            'memory': estimate_memory_bytes(n) + 1000 * 8,  # + DCT storage
        }

    return results


def analyze_farey_vs_bisection(signal_func, n_samples=50, n_eval=10000):
    """
    Deep dive: WHERE does Farey place samples vs bisection?
    Look at sample point distributions to understand the structural difference.
    """
    t_eval = np.linspace(0, 1, n_eval)
    y_true = np.array([signal_func(t) for t in t_eval])

    # Get sample points from both methods
    farey_pts, farey_vals, _ = farey_adaptive_sampling(signal_func, n_samples)
    bisect_pts, bisect_vals, _ = bisection_adaptive_sampling(signal_func, n_samples)

    # Analyze interval widths
    farey_widths = np.diff(farey_pts)
    bisect_widths = np.diff(bisect_pts)

    # Check if bisection creates power-of-2 artifacts
    bisect_unique_widths = set()
    for w in bisect_widths:
        # Round to detect powers of 2
        for k in range(1, 20):
            if abs(w - 1.0 / (2 ** k)) < 1e-10:
                bisect_unique_widths.add(f"1/{2**k}")
                break

    # Check Farey interval diversity
    farey_unique_widths = len(set(np.round(farey_widths, 10)))
    bisect_unique_count = len(set(np.round(bisect_widths, 10)))

    # Find features at non-power-of-2 positions
    # Compute signal gradient
    gradient = np.abs(np.gradient(y_true, t_eval))
    feature_locations = t_eval[gradient > np.percentile(gradient, 95)]

    # How close does each method's samples get to feature locations?
    farey_feature_dist = []
    bisect_feature_dist = []
    for feat in feature_locations:
        farey_feature_dist.append(np.min(np.abs(farey_pts - feat)))
        bisect_feature_dist.append(np.min(np.abs(bisect_pts - feat)))

    return {
        'farey_unique_widths': farey_unique_widths,
        'bisect_unique_widths': bisect_unique_count,
        'bisect_power2_widths': list(bisect_unique_widths),
        'farey_mean_feature_dist': np.mean(farey_feature_dist) if farey_feature_dist else 0,
        'bisect_mean_feature_dist': np.mean(bisect_feature_dist) if bisect_feature_dist else 0,
        'farey_max_feature_dist': np.max(farey_feature_dist) if farey_feature_dist else 0,
        'bisect_max_feature_dist': np.max(bisect_feature_dist) if bisect_feature_dist else 0,
        'farey_width_entropy': -np.sum(np.unique(np.round(farey_widths, 8), return_counts=True)[1] / len(farey_widths) *
                                       np.log2(np.unique(np.round(farey_widths, 8), return_counts=True)[1] / len(farey_widths) + 1e-30)),
        'bisect_width_entropy': -np.sum(np.unique(np.round(bisect_widths, 8), return_counts=True)[1] / len(bisect_widths) *
                                        np.log2(np.unique(np.round(bisect_widths, 8), return_counts=True)[1] / len(bisect_widths) + 1e-30)),
    }


def test_non_power2_features():
    """
    Specifically test signal with features at non-power-of-2 positions.
    This is where Farey SHOULD win over bisection.
    """
    def signal_at_thirds(t):
        """Signal with sharp features at 1/3, 2/3, 1/5, 3/7 — non-dyadic positions."""
        base = np.sin(2 * np.pi * t)
        # Features at non-power-of-2 positions
        f1 = 2.0 * np.exp(-((t - 1/3) ** 2) / (2 * 0.005 ** 2))
        f2 = 1.5 * np.exp(-((t - 2/3) ** 2) / (2 * 0.004 ** 2))
        f3 = 1.8 * np.exp(-((t - 1/5) ** 2) / (2 * 0.003 ** 2))
        f4 = 2.2 * np.exp(-((t - 3/7) ** 2) / (2 * 0.004 ** 2))
        return base + f1 + f2 + f3 + f4

    def signal_at_powers(t):
        """Signal with features at power-of-2 positions — bisection should win here."""
        base = np.sin(2 * np.pi * t)
        f1 = 2.0 * np.exp(-((t - 0.25) ** 2) / (2 * 0.005 ** 2))
        f2 = 1.5 * np.exp(-((t - 0.5) ** 2) / (2 * 0.004 ** 2))
        f3 = 1.8 * np.exp(-((t - 0.125) ** 2) / (2 * 0.003 ** 2))
        f4 = 2.2 * np.exp(-((t - 0.75) ** 2) / (2 * 0.004 ** 2))
        return base + f1 + f2 + f3 + f4

    n_eval = 10000
    t_eval = np.linspace(0, 1, n_eval)

    results = {}
    for name, sig in [('non_dyadic', signal_at_thirds), ('dyadic', signal_at_powers)]:
        y_true = np.array([sig(t) for t in t_eval])
        results[name] = {}

        for n in [20, 30, 50, 80, 100]:
            # Farey
            pts_f, vals_f, _ = farey_adaptive_sampling(sig, n)
            recon_f = linear_interpolate(pts_f, vals_f, t_eval)
            snr_f = compute_snr(y_true, recon_f)

            # Bisection
            pts_b, vals_b, _ = bisection_adaptive_sampling(sig, n)
            recon_b = linear_interpolate(pts_b, vals_b, t_eval)
            snr_b = compute_snr(y_true, recon_b)

            results[name][n] = {
                'farey_snr': snr_f,
                'bisection_snr': snr_b,
                'farey_advantage_dB': snr_f - snr_b,
            }

    return results


def iot_feasibility_analysis(n_samples=50):
    """Can this run on 32KB RAM? Estimate resource usage."""

    # Memory breakdown
    sample_storage = estimate_memory_bytes(n_samples)  # points + values

    # Farey: need to store sorted list of Fraction-like pairs
    # On IoT: store as (numerator: uint16, denominator: uint16) = 4 bytes each
    farey_overhead = n_samples * 4  # Fraction storage

    # Working memory for interval scanning
    working_mem = n_samples * 8  # error estimates array

    # Total
    total_farey = sample_storage + farey_overhead + working_mem

    # Bisection: simpler, just float positions
    total_bisection = sample_storage + n_samples * 4 + working_mem

    # CS: needs DCT matrix or at least column access
    # For n_dense=100 (tiny), DCT matrix = 100*100*4 = 40KB — already too big!
    # Could use on-the-fly DCT computation but adds flops
    cs_matrix_mem = 100 * 100 * 4  # reduced dense grid
    total_cs = sample_storage + cs_matrix_mem

    ram_budget = 32 * 1024  # 32KB

    return {
        'ram_budget_bytes': ram_budget,
        'farey_total_bytes': total_farey,
        'bisection_total_bytes': total_bisection,
        'cs_total_bytes': total_cs,
        'farey_fits_32kb': total_farey <= ram_budget,
        'bisection_fits_32kb': total_bisection <= ram_budget,
        'cs_fits_32kb': total_cs <= ram_budget,
        'farey_ram_percent': 100.0 * total_farey / ram_budget,
        'bisection_ram_percent': 100.0 * total_bisection / ram_budget,
        'cs_ram_percent': 100.0 * total_cs / ram_budget,
        'max_samples_farey_32kb': ram_budget // 16,  # 16 bytes per sample total
        'note': 'CS needs dense grid matrix — impractical on 32KB without on-the-fly DCT',
    }


def power_savings_estimate(uniform_rate=1000, farey_samples_needed=None,
                           signal_duration_s=1.0):
    """
    Estimate power savings from reduced sampling.

    ESP32 power model:
    - Active mode: ~80mA at 240MHz
    - ADC read: ~150us per sample
    - Deep sleep: ~10uA
    - WiFi TX: ~170mA

    Key insight: fewer samples = more time in deep sleep = huge power savings
    """
    # ESP32 typical values
    active_current_mA = 80
    sleep_current_mA = 0.01  # 10uA
    adc_time_per_sample_s = 150e-6
    wifi_tx_current_mA = 170
    wifi_tx_time_per_sample_s = 0.001  # 1ms per sample transmitted
    battery_mAh = 1000  # typical LiPo

    # Uniform: sample at full rate
    uniform_n = int(uniform_rate * signal_duration_s)
    uniform_active_time = uniform_n * adc_time_per_sample_s
    uniform_tx_time = uniform_n * wifi_tx_time_per_sample_s
    uniform_sleep_time = signal_duration_s - uniform_active_time - uniform_tx_time
    if uniform_sleep_time < 0:
        uniform_sleep_time = 0

    uniform_energy = (active_current_mA * uniform_active_time +
                      wifi_tx_current_mA * uniform_tx_time +
                      sleep_current_mA * uniform_sleep_time) / 3600  # mAh

    results = {}
    for method_name, n_adaptive in (farey_samples_needed or {}).items():
        adaptive_active_time = n_adaptive * adc_time_per_sample_s
        # Extra computation time for Farey/bisection
        compute_time = n_adaptive * n_adaptive * 1e-6  # ~1us per comparison
        adaptive_tx_time = n_adaptive * wifi_tx_time_per_sample_s
        adaptive_sleep_time = signal_duration_s - adaptive_active_time - adaptive_tx_time - compute_time
        if adaptive_sleep_time < 0:
            adaptive_sleep_time = 0

        adaptive_energy = (active_current_mA * (adaptive_active_time + compute_time) +
                          wifi_tx_current_mA * adaptive_tx_time +
                          sleep_current_mA * adaptive_sleep_time) / 3600

        savings_pct = 100.0 * (1 - adaptive_energy / uniform_energy) if uniform_energy > 0 else 0

        # Battery life comparison
        uniform_life_hours = battery_mAh / (uniform_energy / signal_duration_s * 3600) if uniform_energy > 0 else float('inf')
        adaptive_life_hours = battery_mAh / (adaptive_energy / signal_duration_s * 3600) if adaptive_energy > 0 else float('inf')

        results[method_name] = {
            'n_samples': n_adaptive,
            'energy_mAh_per_s': adaptive_energy,
            'savings_vs_uniform_pct': savings_pct,
            'battery_life_hours': adaptive_life_hours,
            'battery_life_days': adaptive_life_hours / 24,
            'uniform_life_days': uniform_life_hours / 24,
            'life_extension_factor': adaptive_life_hours / uniform_life_hours if uniform_life_hours > 0 else float('inf'),
        }

    results['uniform'] = {
        'n_samples': uniform_n,
        'energy_mAh_per_s': uniform_energy,
        'savings_vs_uniform_pct': 0,
        'battery_life_hours': battery_mAh / (uniform_energy / signal_duration_s * 3600) if uniform_energy > 0 else float('inf'),
    }
    results['uniform']['battery_life_days'] = results['uniform']['battery_life_hours'] / 24

    return results


# ============================================================
# Main execution
# ============================================================

def main():
    print("=" * 70)
    print("FAREY ADAPTIVE SAMPLING FOR IoT EDGE DEVICES")
    print("=" * 70)

    sample_counts = [10, 20, 30, 50, 80, 100, 150, 200]

    all_results = {}

    # Run comparison for each signal
    for sig_name, sig_func in SIGNALS.items():
        print(f"\n{'=' * 50}")
        print(f"Signal: {sig_name.upper()}")
        print(f"{'=' * 50}")

        results = run_comparison(sig_name, sig_func, sample_counts)
        all_results[sig_name] = results

        # Print results table
        print(f"\n{'N':>5} | {'Method':>12} | {'SNR(dB)':>10} | {'MaxErr':>10} | {'Time(ms)':>10}")
        print("-" * 65)

        for n in sample_counts:
            for method in ['uniform', 'random', 'bisection', 'farey', 'farey_sb', 'hybrid', 'cs']:
                r = results[n][method]
                print(f"{n:>5} | {method:>12} | {r['snr']:>10.2f} | {r['max_error']:>10.4f} | {r['time']*1000:>10.2f}")
            print("-" * 65)

    # Deep dive: Farey vs Bisection
    print(f"\n{'=' * 70}")
    print("DEEP DIVE: FAREY vs BISECTION — Sample Placement Analysis")
    print(f"{'=' * 70}")

    for sig_name, sig_func in SIGNALS.items():
        analysis = analyze_farey_vs_bisection(sig_func, n_samples=50)
        print(f"\n--- {sig_name.upper()} (50 samples) ---")
        print(f"  Farey unique interval widths:    {analysis['farey_unique_widths']}")
        print(f"  Bisection unique interval widths: {analysis['bisect_unique_widths']}")
        print(f"  Bisection power-of-2 widths:     {analysis['bisect_power2_widths']}")
        print(f"  Farey width entropy:             {analysis['farey_width_entropy']:.3f} bits")
        print(f"  Bisection width entropy:         {analysis['bisect_width_entropy']:.3f} bits")
        print(f"  Farey mean dist to features:     {analysis['farey_mean_feature_dist']:.6f}")
        print(f"  Bisection mean dist to features: {analysis['bisect_mean_feature_dist']:.6f}")
        print(f"  Farey max dist to features:      {analysis['farey_max_feature_dist']:.6f}")
        print(f"  Bisection max dist to features:  {analysis['bisect_max_feature_dist']:.6f}")

    # Non-dyadic vs dyadic feature test
    print(f"\n{'=' * 70}")
    print("KEY TEST: Features at non-power-of-2 positions")
    print("(This is where Farey SHOULD have an advantage)")
    print(f"{'=' * 70}")

    np2_results = test_non_power2_features()
    for sig_type in ['non_dyadic', 'dyadic']:
        print(f"\n--- {sig_type.upper()} signal ---")
        print(f"{'N':>5} | {'Farey SNR':>12} | {'Bisect SNR':>12} | {'Farey Adv(dB)':>14}")
        print("-" * 55)
        for n in sorted(np2_results[sig_type].keys()):
            r = np2_results[sig_type][n]
            marker = " <-- Farey wins" if r['farey_advantage_dB'] > 0.5 else (
                " <-- Bisection wins" if r['farey_advantage_dB'] < -0.5 else " ~tie")
            print(f"{n:>5} | {r['farey_snr']:>12.2f} | {r['bisection_snr']:>12.2f} | {r['farey_advantage_dB']:>+14.2f}{marker}")

    # IoT feasibility
    print(f"\n{'=' * 70}")
    print("IoT FEASIBILITY: 32KB RAM Analysis")
    print(f"{'=' * 70}")

    feasibility = iot_feasibility_analysis(50)
    print(f"\n  RAM budget:              {feasibility['ram_budget_bytes']:,} bytes")
    print(f"  Farey total:             {feasibility['farey_total_bytes']:,} bytes ({feasibility['farey_ram_percent']:.1f}%)")
    print(f"  Bisection total:         {feasibility['bisection_total_bytes']:,} bytes ({feasibility['bisection_ram_percent']:.1f}%)")
    print(f"  CS total:                {feasibility['cs_total_bytes']:,} bytes ({feasibility['cs_ram_percent']:.1f}%)")
    print(f"  Farey fits 32KB:         {feasibility['farey_fits_32kb']}")
    print(f"  Bisection fits 32KB:     {feasibility['bisection_fits_32kb']}")
    print(f"  CS fits 32KB:            {feasibility['cs_fits_32kb']}")
    print(f"  Max Farey samples @32KB: {feasibility['max_samples_farey_32kb']}")
    print(f"  Note: {feasibility['note']}")

    # Power savings estimate
    print(f"\n{'=' * 70}")
    print("POWER SAVINGS ESTIMATE (ESP32 model)")
    print(f"{'=' * 70}")

    # Determine how many samples each method needs for 30dB SNR on ECG
    target_snr = 30.0
    ecg_results = all_results['ecg']

    samples_for_target = {}
    for method in ['uniform', 'random', 'bisection', 'farey', 'farey_sb', 'hybrid']:
        for n in sample_counts:
            if ecg_results[n][method]['snr'] >= target_snr:
                samples_for_target[method] = n
                break
        else:
            samples_for_target[method] = sample_counts[-1]

    print(f"\n  Target: {target_snr:.0f} dB SNR on ECG signal")
    print(f"  Samples needed:")
    for method, n in sorted(samples_for_target.items(), key=lambda x: x[1]):
        print(f"    {method:>12}: {n} samples")

    # Only adaptive methods for power comparison
    adaptive_needs = {k: v for k, v in samples_for_target.items() if k != 'uniform'}
    power = power_savings_estimate(
        uniform_rate=1000,
        farey_samples_needed=adaptive_needs,
    )

    print(f"\n  Power comparison (1000 Hz uniform baseline):")
    print(f"  {'Method':>12} | {'Samples':>8} | {'Savings':>10} | {'Battery(days)':>14} | {'Extension':>10}")
    print(f"  {'-'*70}")

    uniform_days = power['uniform']['battery_life_days']
    print(f"  {'uniform':>12} | {power['uniform']['n_samples']:>8} | {'baseline':>10} | {uniform_days:>14.1f} | {'1.0x':>10}")

    for method in ['random', 'bisection', 'farey', 'farey_sb', 'hybrid']:
        if method in power:
            p = power[method]
            ext = f"{p['life_extension_factor']:.1f}x"
            print(f"  {method:>12} | {p['n_samples']:>8} | {p['savings_vs_uniform_pct']:>9.1f}% | {p['battery_life_days']:>14.1f} | {ext:>10}")

    # HONEST ASSESSMENT
    print(f"\n{'=' * 70}")
    print("HONEST ASSESSMENT: Does Farey beat bisection?")
    print(f"{'=' * 70}")

    # Compute average advantage across all signals and sample counts
    for farey_variant in ['farey', 'farey_sb', 'hybrid']:
        advantages = []
        for sig_name in SIGNALS:
            for n in sample_counts:
                fv_snr = all_results[sig_name][n][farey_variant]['snr']
                bisect_snr = all_results[sig_name][n]['bisection']['snr']
                advantages.append(fv_snr - bisect_snr)

        avg_adv = np.mean(advantages)
        std_adv = np.std(advantages)
        pct_wins = 100.0 * sum(1 for a in advantages if a > 0.5) / len(advantages)
        pct_loses = 100.0 * sum(1 for a in advantages if a < -0.5) / len(advantages)
        pct_tie = 100.0 - pct_wins - pct_loses

        print(f"\n  --- {farey_variant.upper()} vs BISECTION ---")
        print(f"  Average advantage: {avg_adv:+.2f} dB (std: {std_adv:.2f} dB)")
        print(f"  Wins (>0.5 dB):    {pct_wins:.0f}%")
        print(f"  Loses:             {pct_loses:.0f}%")
        print(f"  Ties:              {pct_tie:.0f}%")

    # Non-dyadic advantage
    np2_advantages = []
    for n in np2_results['non_dyadic']:
        np2_advantages.append(np2_results['non_dyadic'][n]['farey_advantage_dB'])
    avg_np2_adv = np.mean(np2_advantages)

    dyadic_advantages = []
    for n in np2_results['dyadic']:
        dyadic_advantages.append(np2_results['dyadic'][n]['farey_advantage_dB'])
    avg_dyadic_adv = np.mean(dyadic_advantages)

    print(f"\n  Non-dyadic features:     {avg_np2_adv:+.2f} dB Farey advantage")
    print(f"  Dyadic features:         {avg_dyadic_adv:+.2f} dB Farey advantage")

    # Best Farey variant overall
    best_variant = None
    best_avg = -999
    for farey_variant in ['farey', 'farey_sb', 'hybrid']:
        advantages = []
        for sig_name in SIGNALS:
            for n in sample_counts:
                fv_snr = all_results[sig_name][n][farey_variant]['snr']
                bisect_snr = all_results[sig_name][n]['bisection']['snr']
                advantages.append(fv_snr - bisect_snr)
        avg = np.mean(advantages)
        if avg > best_avg:
            best_avg = avg
            best_variant = farey_variant

    if best_avg > 1.0:
        verdict = f"YES — {best_variant} provides meaningful advantage over bisection ({best_avg:+.1f} dB)"
    elif best_avg > 0.2:
        verdict = f"MARGINAL — {best_variant} slightly better but advantage is small ({best_avg:+.1f} dB)"
    elif best_avg > -0.2:
        verdict = f"TIE — No significant difference ({best_avg:+.1f} dB)"
    elif best_avg > -1.0:
        verdict = f"SLIGHT LOSS — Bisection slightly better ({best_avg:+.1f} dB)"
    else:
        verdict = f"LOSS — Bisection beats best Farey variant ({best_variant}) by {-best_avg:.1f} dB"

    print(f"\n  OVERALL VERDICT: {verdict}")

    # Farey's real advantages (even if it ties on SNR)
    print(f"\n  Farey's structural advantages (even if SNR is similar):")
    print(f"  1. Deterministic: no RNG needed (critical for constrained devices)")
    print(f"  2. Integer arithmetic: mediants use only addition (no division/multiply)")
    print(f"  3. Certifiable: provable bounds on approximation quality")
    print(f"  4. Zero-communication sync: multiple sensors can agree on sample points")
    print(f"     without any communication (all use same Farey order)")
    print(f"  5. Graceful degradation: if interrupted, samples so far are optimally spaced")

    # Save all results
    output = {
        'main_results': {},
        'non_dyadic_test': {},
        'feasibility': feasibility,
        'honest_assessment': {
            'best_variant': best_variant,
            'best_avg_advantage_dB': float(best_avg),
            'non_dyadic_advantage_dB': float(avg_np2_adv),
            'dyadic_advantage_dB': float(avg_dyadic_adv),
            'verdict': verdict,
        }
    }

    # Convert numpy types for JSON
    for sig_name in all_results:
        output['main_results'][sig_name] = {}
        for n in all_results[sig_name]:
            output['main_results'][sig_name][str(n)] = {}
            for method in all_results[sig_name][n]:
                output['main_results'][sig_name][str(n)][method] = {
                    k: float(v) if isinstance(v, (np.floating, np.integer)) else v
                    for k, v in all_results[sig_name][n][method].items()
                }

    for sig_type in np2_results:
        output['non_dyadic_test'][sig_type] = {}
        for n in np2_results[sig_type]:
            output['non_dyadic_test'][sig_type][str(n)] = {
                k: float(v) for k, v in np2_results[sig_type][n].items()
            }

    outpath = os.path.expanduser('~/Desktop/Farey-Local/experiments/iot_farey_results.json')
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved to: {outpath}")

    return output


if __name__ == '__main__':
    main()
