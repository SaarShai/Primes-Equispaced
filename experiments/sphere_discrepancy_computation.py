#!/usr/bin/env python3
"""
Spherical analog of Farey per-step discrepancy DeltaW(p).

On S^2, Duke's theorem says lattice points (a,b,c) with a^2+b^2+c^2=n
equidistribute as n -> infinity (through representable integers).
We compute a per-step spherical cap discrepancy and check if a Sign Theorem holds.
"""

import numpy as np
from scipy.special import sph_harm
from sympy import isprime
import json
import time
import sys

np.random.seed(42)

N_MAX = 500
N_CAPS = 100  # number of random spherical caps for discrepancy

def find_representations(n):
    """Find all integer solutions (a,b,c) to a^2 + b^2 + c^2 = n."""
    solutions = []
    if n < 0:
        return solutions
    bound = int(np.sqrt(n)) + 1
    for a in range(-bound, bound + 1):
        a2 = a * a
        if a2 > n:
            continue
        for b in range(-bound, bound + 1):
            b2 = b * b
            if a2 + b2 > n:
                continue
            rem = n - a2 - b2
            c = int(round(np.sqrt(rem)))
            if c * c == rem:
                if c > 0:
                    solutions.append((a, b, c))
                    solutions.append((a, b, -c))
                else:
                    solutions.append((a, b, 0))
    return solutions


def normalize_to_sphere(solutions, n):
    """Normalize solutions to unit sphere points."""
    if n == 0 or len(solutions) == 0:
        return np.array([]).reshape(0, 3)
    sqrt_n = np.sqrt(n)
    pts = np.array(solutions, dtype=float) / sqrt_n
    return pts


def cart_to_spherical(pts):
    """Convert (x,y,z) on unit sphere to (theta, phi).
    theta = polar angle [0, pi], phi = azimuthal [0, 2pi]."""
    if len(pts) == 0:
        return np.array([]), np.array([])
    x, y, z = pts[:, 0], pts[:, 1], pts[:, 2]
    r = np.sqrt(x**2 + y**2 + z**2)
    r = np.maximum(r, 1e-15)
    theta = np.arccos(np.clip(z / r, -1, 1))
    phi = np.arctan2(y, x) % (2 * np.pi)
    return theta, phi


def generate_random_caps(n_caps):
    """Generate random spherical cap centers and half-angles."""
    # Random centers uniformly on S^2
    u = np.random.uniform(0, 1, n_caps)
    v = np.random.uniform(0, 1, n_caps)
    theta_c = np.arccos(1 - 2 * u)  # uniform on sphere
    phi_c = 2 * np.pi * v

    # Cap half-angles: uniform in cos(alpha) from -1 to 1
    # This gives uniform cap areas
    cos_alpha = np.random.uniform(-0.5, 0.95, n_caps)  # avoid full sphere / empty
    alpha = np.arccos(cos_alpha)

    # Center directions as unit vectors
    cx = np.sin(theta_c) * np.cos(phi_c)
    cy = np.sin(theta_c) * np.sin(phi_c)
    cz = np.cos(theta_c)
    centers = np.column_stack([cx, cy, cz])

    return centers, cos_alpha, alpha


def spherical_cap_discrepancy(pts, centers, cos_alpha):
    """
    Compute mean squared spherical cap discrepancy.
    For each cap, compare fraction of points inside to expected area fraction.
    Cap area fraction = (1 - cos(alpha)) / 2.
    """
    if len(pts) == 0:
        return float('inf')

    n_pts = len(pts)
    n_caps = len(centers)

    # Dot products: pts (n_pts, 3) . centers.T (3, n_caps) -> (n_pts, n_caps)
    dots = pts @ centers.T  # shape (n_pts, n_caps)

    # Point is in cap if dot product >= cos(alpha)
    in_cap = dots >= cos_alpha[np.newaxis, :]  # broadcast

    fractions = in_cap.sum(axis=0) / n_pts  # fraction in each cap
    expected = (1 - cos_alpha) / 2  # area fraction

    deviations = fractions - expected
    msd = np.mean(deviations**2)
    return msd


def compute_spherical_harmonics_sum(pts, theta, phi, ell_max=3):
    """
    For each (ell, m), compute sum of Y_ell^m over the lattice points.
    Returns dict of (ell, m) -> complex value.
    """
    results = {}
    if len(pts) == 0:
        for ell in range(1, ell_max + 1):
            for m in range(-ell, ell + 1):
                results[f"({ell},{m})"] = {"real": 0.0, "imag": 0.0, "abs": 0.0}
        return results

    for ell in range(1, ell_max + 1):
        for m in range(-ell, ell + 1):
            # scipy sph_harm uses (m, ell, phi, theta) convention
            # and m must be >= 0 for direct call; handle negative m
            if m >= 0:
                Y = sph_harm(m, ell, phi, theta)
            else:
                # Y_ell^{-m} = (-1)^m conj(Y_ell^m)
                Y = ((-1)**m) * np.conj(sph_harm(-m, ell, phi, theta))
            total = np.sum(Y)
            results[f"({ell},{m})"] = {
                "real": float(total.real),
                "imag": float(total.imag),
                "abs": float(abs(total))
            }
    return results


def main():
    print(f"Spherical discrepancy computation: n = 1..{N_MAX}")
    print(f"Using {N_CAPS} random spherical caps")
    sys.stdout.flush()

    # Pre-generate caps (fixed for all n)
    centers, cos_alpha, alpha = generate_random_caps(N_CAPS)

    # Storage
    r3_values = {}  # n -> r3(n)
    W_sphere = {}   # n -> discrepancy
    all_sh_sums = {}  # n -> spherical harmonic sums (for primes only)

    primes = [p for p in range(2, N_MAX + 1) if isprime(p)]
    prime_set = set(primes)

    t0 = time.time()

    for n in range(1, N_MAX + 1):
        sols = find_representations(n)
        r3_n = len(sols)
        r3_values[n] = r3_n

        if r3_n == 0:
            W_sphere[n] = None  # not representable
            continue

        pts = normalize_to_sphere(sols, n)
        W_sphere[n] = float(spherical_cap_discrepancy(pts, centers, cos_alpha))

        # Spherical harmonics for primes
        if n in prime_set:
            theta, phi = cart_to_spherical(pts)
            sh = compute_spherical_harmonics_sum(pts, theta, phi, ell_max=3)
            all_sh_sums[n] = sh

        if n % 100 == 0:
            elapsed = time.time() - t0
            print(f"  n={n}, elapsed={elapsed:.1f}s")
            sys.stdout.flush()

    # Compute DeltaW_sphere
    delta_W_all = {}
    delta_W_primes = {}
    delta_W_primes_1mod4 = {}
    delta_W_primes_3mod4 = {}

    for n in range(2, N_MAX + 1):
        if W_sphere.get(n) is not None and W_sphere.get(n-1) is not None:
            dw = W_sphere[n-1] - W_sphere[n]
            delta_W_all[n] = dw

            if n in prime_set:
                delta_W_primes[n] = dw
                if n % 4 == 1:
                    delta_W_primes_1mod4[n] = dw
                elif n % 4 == 3:
                    delta_W_primes_3mod4[n] = dw

    # Analysis
    print("\n=== RESULTS ===\n")

    # Overall stats
    all_dw_vals = list(delta_W_all.values())
    print(f"All integers: {len(all_dw_vals)} values")
    print(f"  Mean DeltaW: {np.mean(all_dw_vals):.6e}")
    print(f"  Median DeltaW: {np.median(all_dw_vals):.6e}")
    print(f"  Fraction DeltaW < 0: {sum(1 for v in all_dw_vals if v < 0) / len(all_dw_vals):.4f}")

    # Prime stats
    prime_dw_vals = list(delta_W_primes.values())
    prime_dw_keys = list(delta_W_primes.keys())
    print(f"\nPrimes: {len(prime_dw_vals)} values")
    if prime_dw_vals:
        print(f"  Mean DeltaW: {np.mean(prime_dw_vals):.6e}")
        print(f"  Median DeltaW: {np.median(prime_dw_vals):.6e}")
        neg_count = sum(1 for v in prime_dw_vals if v < 0)
        print(f"  Fraction DeltaW < 0: {neg_count / len(prime_dw_vals):.4f} ({neg_count}/{len(prime_dw_vals)})")

        # Which primes have DeltaW >= 0?
        pos_primes = [p for p, v in delta_W_primes.items() if v >= 0]
        if pos_primes:
            print(f"  Primes with DeltaW >= 0: {pos_primes[:20]}{'...' if len(pos_primes) > 20 else ''}")

    # 1 mod 4 vs 3 mod 4
    vals_1mod4 = list(delta_W_primes_1mod4.values())
    vals_3mod4 = list(delta_W_primes_3mod4.values())

    if vals_1mod4:
        print(f"\nPrimes p=1 (mod 4): {len(vals_1mod4)} values")
        print(f"  Mean DeltaW: {np.mean(vals_1mod4):.6e}")
        neg_1 = sum(1 for v in vals_1mod4 if v < 0)
        print(f"  Fraction DeltaW < 0: {neg_1 / len(vals_1mod4):.4f} ({neg_1}/{len(vals_1mod4)})")

    if vals_3mod4:
        print(f"\nPrimes p=3 (mod 4): {len(vals_3mod4)} values")
        print(f"  Mean DeltaW: {np.mean(vals_3mod4):.6e}")
        neg_3 = sum(1 for v in vals_3mod4 if v < 0)
        print(f"  Fraction DeltaW < 0: {neg_3 / len(vals_3mod4):.4f} ({neg_3}/{len(vals_3mod4)})")

    # r3 connection
    print(f"\n=== r3 and Discrepancy Connection ===")
    print(f"{'n':>6} {'r3(n)':>8} {'W_sphere':>14} {'DeltaW':>14}")
    for p in primes[:30]:
        w = W_sphere.get(p)
        dw = delta_W_primes.get(p)
        w_str = f"{w:.6e}" if w is not None else "N/A"
        dw_str = f"{dw:.6e}" if dw is not None else "N/A"
        print(f"{p:>6} {r3_values[p]:>8} {w_str:>14} {dw_str:>14}")

    # Spherical harmonics analysis
    print(f"\n=== Spherical Harmonics Sums (first 15 primes) ===")
    for p in primes[:15]:
        if p in all_sh_sums:
            sh = all_sh_sums[p]
            # Print |sum Y_1^0|, |sum Y_2^0|, |sum Y_3^0| (zonal harmonics)
            y10 = sh.get("(1,0)", {}).get("abs", 0)
            y20 = sh.get("(2,0)", {}).get("abs", 0)
            y30 = sh.get("(3,0)", {}).get("abs", 0)
            print(f"  p={p:>5}: |Y_1^0 sum|={y10:.4f}, |Y_2^0 sum|={y20:.4f}, |Y_3^0 sum|={y30:.4f}, r3={r3_values[p]}")

    # Check if |sum Y_ell^m| / r3(p) shows any pattern
    print(f"\n=== Normalized |sum Y_ell^m| / r3(p) for zonal harmonics ===")
    normalized_y10 = []
    normalized_y20 = []
    for p in primes:
        if p in all_sh_sums and r3_values[p] > 0:
            sh = all_sh_sums[p]
            y10 = sh.get("(1,0)", {}).get("abs", 0)
            y20 = sh.get("(2,0)", {}).get("abs", 0)
            normalized_y10.append(y10 / r3_values[p])
            normalized_y20.append(y20 / r3_values[p])
    if normalized_y10:
        print(f"  |Y_1^0|/r3: mean={np.mean(normalized_y10):.6f}, std={np.std(normalized_y10):.6f}")
    if normalized_y20:
        print(f"  |Y_2^0|/r3: mean={np.mean(normalized_y20):.6f}, std={np.std(normalized_y20):.6f}")

    # Correlation between DeltaW and r3
    common_primes = [p for p in primes if p in delta_W_primes and r3_values[p] > 0]
    if len(common_primes) > 5:
        dw_arr = np.array([delta_W_primes[p] for p in common_primes])
        r3_arr = np.array([r3_values[p] for p in common_primes])
        corr = np.corrcoef(dw_arr, r3_arr)[0, 1]
        print(f"\n  Correlation(DeltaW, r3) over primes: {corr:.4f}")

        log_r3 = np.log(r3_arr)
        corr2 = np.corrcoef(dw_arr, log_r3)[0, 1]
        print(f"  Correlation(DeltaW, log r3) over primes: {corr2:.4f}")

    # Save results
    results = {
        "parameters": {"N_MAX": N_MAX, "N_CAPS": N_CAPS},
        "r3": {str(k): v for k, v in r3_values.items()},
        "W_sphere": {str(k): v for k, v in W_sphere.items() if v is not None},
        "delta_W_all": {str(k): v for k, v in delta_W_all.items()},
        "delta_W_primes": {str(k): v for k, v in delta_W_primes.items()},
        "delta_W_primes_1mod4": {str(k): v for k, v in delta_W_primes_1mod4.items()},
        "delta_W_primes_3mod4": {str(k): v for k, v in delta_W_primes_3mod4.items()},
        "spherical_harmonics_primes": {str(k): v for k, v in all_sh_sums.items()},
        "summary": {
            "all_integers": {
                "count": len(all_dw_vals),
                "mean_delta_W": float(np.mean(all_dw_vals)) if all_dw_vals else None,
                "median_delta_W": float(np.median(all_dw_vals)) if all_dw_vals else None,
                "frac_negative": float(sum(1 for v in all_dw_vals if v < 0) / len(all_dw_vals)) if all_dw_vals else None,
            },
            "primes": {
                "count": len(prime_dw_vals),
                "mean_delta_W": float(np.mean(prime_dw_vals)) if prime_dw_vals else None,
                "median_delta_W": float(np.median(prime_dw_vals)) if prime_dw_vals else None,
                "frac_negative": float(neg_count / len(prime_dw_vals)) if prime_dw_vals else None,
                "positive_primes": pos_primes if pos_primes else [],
            },
            "primes_1mod4": {
                "count": len(vals_1mod4),
                "mean_delta_W": float(np.mean(vals_1mod4)) if vals_1mod4 else None,
                "frac_negative": float(neg_1 / len(vals_1mod4)) if vals_1mod4 else None,
            },
            "primes_3mod4": {
                "count": len(vals_3mod4),
                "mean_delta_W": float(np.mean(vals_3mod4)) if vals_3mod4 else None,
                "frac_negative": float(neg_3 / len(vals_3mod4)) if vals_3mod4 else None,
            },
            "correlation_deltaW_r3": float(corr) if len(common_primes) > 5 else None,
            "correlation_deltaW_log_r3": float(corr2) if len(common_primes) > 5 else None,
        }
    }

    outpath = "/Users/saar/Desktop/Farey-Local/experiments/sphere_discrepancy_results.json"
    with open(outpath, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {outpath}")

    elapsed = time.time() - t0
    print(f"Total time: {elapsed:.1f}s")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
