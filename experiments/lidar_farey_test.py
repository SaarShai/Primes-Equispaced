#!/usr/bin/env python3
"""
Quick validation: Farey mediant insertion vs. linear interpolation for LiDAR scan-line densification.

Synthetic 1D "scan line": angular samples of a scene with objects at various depths.
We simulate a sparse LiDAR return (depth as function of angle), then densify.
"""

import numpy as np
import time

np.random.seed(42)

# === Scene: depth as function of angle ===
# Simulate objects: a wall, a car (box), a pedestrian (narrow spike), background
def scene_depth(angles):
    """Ground truth depth at each angle. Units: meters."""
    depth = np.full_like(angles, 50.0)  # far background at 50m

    # Wall segment: angles 0.3-0.8 rad, at 10m
    mask_wall = (angles >= 0.3) & (angles <= 0.8)
    depth[mask_wall] = 10.0

    # Car: angles 1.2-1.6 rad, at 15m, with slight curvature
    mask_car = (angles >= 1.2) & (angles <= 1.6)
    depth[mask_car] = 15.0 + 2.0 * np.sin(5 * (angles[mask_car] - 1.2))

    # Pedestrian: narrow object at angle ~2.0, at 8m
    mask_ped = (angles >= 1.95) & (angles <= 2.05)
    depth[mask_ped] = 8.0

    # Smooth transitions at edges (realistic: partial returns)
    for edge in [0.3, 0.8, 1.2, 1.6, 1.95, 2.05]:
        near = np.abs(angles - edge) < 0.03
        if np.any(near):
            depth[near] = depth[near] + 5.0 * np.exp(-((angles[near] - edge) / 0.01) ** 2)

    return depth


# === Sparse sampling (simulating low-resolution LiDAR) ===
N_sparse = 64  # typical for a 16-beam LiDAR scan line
N_dense_gt = 2048  # ground truth resolution

angles_sparse = np.linspace(0, np.pi, N_sparse)
angles_dense = np.linspace(0, np.pi, N_dense_gt)

depth_sparse = scene_depth(angles_sparse)
depth_gt = scene_depth(angles_dense)


# === Densification methods ===

def densify_linear(angles_sp, depth_sp, n_target):
    """Linear interpolation between sparse points."""
    angles_out = np.linspace(angles_sp[0], angles_sp[-1], n_target)
    depth_out = np.interp(angles_out, angles_sp, depth_sp)
    return angles_out, depth_out


def densify_farey_mediant(angles_sp, depth_sp, n_rounds):
    """
    Farey mediant insertion: between consecutive points (a_i, d_i) and (a_{i+1}, d_{i+1}),
    insert the mediant. For angles, this is just the midpoint. For depths, we use
    the Farey mediant: (p1+p2)/(q1+q2) if we express depths as rationals,
    or more practically, a weighted combination.

    Key question: what does "mediant" mean for depth values?
    Option A: mediant of rational approximations of depth
    Option B: just midpoint (which makes this identical to linear interp)
    Option C: harmonic mean (reciprocal averaging, natural for distances)

    We test Option A (rational approx) and Option C (harmonic).
    """
    # Option A: Farey rational approximation
    from fractions import Fraction

    angles_list = list(angles_sp)
    depth_list = list(depth_sp)

    for _ in range(n_rounds):
        new_angles = []
        new_depths = []
        for i in range(len(angles_list) - 1):
            new_angles.append(angles_list[i])
            new_depths.append(depth_list[i])

            # Midpoint angle
            mid_angle = (angles_list[i] + angles_list[i + 1]) / 2.0

            # Farey mediant of depths: approximate as p/q, then mediant
            f1 = Fraction(depth_list[i]).limit_denominator(1000)
            f2 = Fraction(depth_list[i + 1]).limit_denominator(1000)
            mediant = Fraction(f1.numerator + f2.numerator, f1.denominator + f2.denominator)

            new_angles.append(mid_angle)
            new_depths.append(float(mediant))

        new_angles.append(angles_list[-1])
        new_depths.append(depth_list[-1])

        angles_list = new_angles
        depth_list = new_depths

    return np.array(angles_list), np.array(depth_list)


def densify_harmonic(angles_sp, depth_sp, n_rounds):
    """Harmonic mean insertion: natural for distance/depth values."""
    angles_list = list(angles_sp)
    depth_list = list(depth_sp)

    for _ in range(n_rounds):
        new_angles = []
        new_depths = []
        for i in range(len(angles_list) - 1):
            new_angles.append(angles_list[i])
            new_depths.append(depth_list[i])

            mid_angle = (angles_list[i] + angles_list[i + 1]) / 2.0
            # Harmonic mean
            d1, d2 = depth_list[i], depth_list[i + 1]
            if d1 > 0 and d2 > 0:
                harm = 2.0 * d1 * d2 / (d1 + d2)
            else:
                harm = (d1 + d2) / 2.0

            new_angles.append(mid_angle)
            new_depths.append(harm)

        new_angles.append(angles_list[-1])
        new_depths.append(depth_list[-1])

        angles_list = new_angles
        depth_list = new_depths

    return np.array(angles_list), np.array(depth_list)


# === Run densification ===
print("=" * 60)
print("LiDAR Scan-Line Densification Test")
print("=" * 60)
print(f"Sparse points: {N_sparse}, Ground truth: {N_dense_gt}")
print()

# Linear interpolation
t0 = time.time()
ang_lin, dep_lin = densify_linear(angles_sparse, depth_sparse, N_dense_gt)
t_lin = time.time() - t0

# Farey mediant (5 rounds: 64 -> 128 -> 256 -> 512 -> 1024 -> 2048ish)
n_rounds = 5
t0 = time.time()
ang_far, dep_far = densify_farey_mediant(angles_sparse, depth_sparse, n_rounds)
t_far = time.time() - t0

# Harmonic mean
t0 = time.time()
ang_harm, dep_harm = densify_harmonic(angles_sparse, depth_sparse, n_rounds)
t_harm = time.time() - t0


# === Evaluate: interpolate all onto the ground truth grid and compute MSE ===
dep_lin_eval = np.interp(angles_dense, ang_lin, dep_lin)
dep_far_eval = np.interp(angles_dense, ang_far, dep_far)
dep_harm_eval = np.interp(angles_dense, ang_harm, dep_harm)

mse_lin = np.mean((dep_lin_eval - depth_gt) ** 2)
mse_far = np.mean((dep_far_eval - depth_gt) ** 2)
mse_harm = np.mean((dep_harm_eval - depth_gt) ** 2)

mae_lin = np.mean(np.abs(dep_lin_eval - depth_gt))
mae_far = np.mean(np.abs(dep_far_eval - depth_gt))
mae_harm = np.mean(np.abs(dep_harm_eval - depth_gt))

print(f"{'Method':<25} {'MSE (m^2)':<15} {'MAE (m)':<12} {'Time (ms)':<12} {'Points'}")
print("-" * 75)
print(f"{'Linear interp':<25} {mse_lin:<15.4f} {mae_lin:<12.4f} {t_lin*1000:<12.2f} {len(dep_lin)}")
print(f"{'Farey mediant':<25} {mse_far:<15.4f} {mae_far:<12.4f} {t_far*1000:<12.2f} {len(dep_far)}")
print(f"{'Harmonic mean':<25} {mse_harm:<15.4f} {mae_harm:<12.4f} {t_harm*1000:<12.2f} {len(dep_harm)}")
print()

# === Key diagnostic: where do they differ? ===
diff_far_lin = dep_far_eval - dep_lin_eval
max_diff = np.max(np.abs(diff_far_lin))
print(f"Max absolute difference (Farey vs Linear): {max_diff:.6f} m")
print(f"Mean absolute difference (Farey vs Linear): {np.mean(np.abs(diff_far_lin)):.6f} m")
print()

# Check at depth discontinuities (where objects begin/end)
edges = [0.3, 0.8, 1.2, 1.6, 1.95, 2.05]
print("Errors near depth discontinuities (within 0.05 rad of edge):")
print(f"{'Edge (rad)':<15} {'MAE Linear':<15} {'MAE Farey':<15} {'MAE Harmonic':<15} {'Winner'}")
print("-" * 75)
for edge in edges:
    mask = np.abs(angles_dense - edge) < 0.05
    if np.any(mask):
        e_lin = np.mean(np.abs(dep_lin_eval[mask] - depth_gt[mask]))
        e_far = np.mean(np.abs(dep_far_eval[mask] - depth_gt[mask]))
        e_harm = np.mean(np.abs(dep_harm_eval[mask] - depth_gt[mask]))
        winner = min([("Linear", e_lin), ("Farey", e_far), ("Harmonic", e_harm)], key=lambda x: x[1])[0]
        print(f"{edge:<15.2f} {e_lin:<15.4f} {e_far:<15.4f} {e_harm:<15.4f} {winner}")

print()
print("=" * 60)
print("ANALYSIS")
print("=" * 60)
print("""
The Farey mediant of two rationals p1/q1 and p2/q2 is (p1+p2)/(q1+q2).
For depth values expressed as rationals, this is NOT the arithmetic mean.
However, for typical depth values (8m, 10m, 15m, 50m), the mediant of
their rational approximations is very close to the arithmetic mean.

Example: mediant of 10/1 and 50/1 = 60/2 = 30 (= arithmetic mean exactly).
Example: mediant of 8/1 and 50/1 = 58/2 = 29 (= arithmetic mean exactly).

The mediant ONLY differs from the arithmetic mean when the denominators
of the rational approximations differ. For integer-valued depths,
denominators are always 1, so mediant = arithmetic mean = midpoint.

CONCLUSION: For LiDAR depth values, Farey mediant insertion is
essentially identical to linear interpolation. The Farey structure
is irrelevant because LiDAR returns are at PHYSICAL positions,
not at rational fractions with meaningful numerator/denominator structure.
""")
