#!/usr/bin/env python3
"""
Sphere Equidistribution: Extending Farey Per-Step Discrepancy to S²

On S¹: Farey fractions equidistribute. We study ΔW(p) = change in discrepancy at prime steps.
On S²: Duke (1988) proved lattice points (a/√n, b/√n, c/√n) with a²+b²+c²=n equidistribute.

This script:
1. Computes r₃(n) for n=1..1000
2. For primes p, collects rational points on S² and computes spherical discrepancy
3. Tracks ΔW_sphere(p) = change in spherical discrepancy at prime steps
4. Computes spherical harmonic sums Σ Y_ℓ^m(pts) — the bridge identity analog
5. Plots everything

Author: Farey Research (Saar), March 2026
"""

import numpy as np
from collections import defaultdict
import json
import os
import sys
import time

# ============================================================
# PART 1: Compute r₃(n) — representations as sum of 3 squares
# ============================================================

def compute_r3(N_max):
    """Compute r₃(n) = #{(a,b,c) ∈ Z³ : a²+b²+c² = n} for n=0..N_max.
    Counts all signs and orderings."""
    r3 = np.zeros(N_max + 1, dtype=np.int64)
    bound = int(np.sqrt(N_max)) + 1
    for a in range(-bound, bound + 1):
        a2 = a * a
        if a2 > N_max:
            continue
        for b in range(-bound, bound + 1):
            ab2 = a2 + b * b
            if ab2 > N_max:
                continue
            for c in range(-bound, bound + 1):
                s = ab2 + c * c
                if 0 <= s <= N_max:
                    r3[s] += 1
    return r3

def get_lattice_points(n):
    """Return all (a,b,c) with a²+b²+c² = n."""
    pts = []
    bound = int(np.sqrt(n)) + 1
    for a in range(-bound, bound + 1):
        a2 = a * a
        if a2 > n:
            continue
        for b in range(-bound, bound + 1):
            ab2 = a2 + b * b
            if ab2 > n:
                continue
            rem = n - ab2
            c = int(np.sqrt(rem))
            for cc in [c, -c, c+1, -(c+1)]:
                if cc * cc == rem:
                    pts.append((a, b, cc))
    # Remove duplicates
    return list(set(pts))

def sieve_primes(N):
    """Sieve of Eratosthenes up to N."""
    is_prime = [False, False] + [True] * (N - 1)
    for i in range(2, int(N**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, N + 1, i):
                is_prime[j] = False
    return [p for p in range(2, N + 1) if is_prime[p]]


# ============================================================
# PART 2: Spherical Discrepancy (L2 cap discrepancy)
# ============================================================

def spherical_cap_area(cos_theta):
    """Normalized area of spherical cap with polar angle theta.
    Cap = {x on S² : x·pole >= cos_theta}.
    Area = (1 - cos_theta)/2 (normalized to [0,1])."""
    return (1.0 - cos_theta) / 2.0

def l2_cap_discrepancy(points_on_sphere):
    """Compute L2 cap discrepancy of points on S².

    For a set of N points on S², the L2 cap discrepancy is:
    D_L2² = ∫_{S²} [F_N(cap(x,θ)) - A(cap(x,θ))]² d(x,θ)

    We use the closed-form Stolarsky invariant principle:
    D_L2² = C - (1/N²) Σᵢ Σⱼ ||xᵢ - xⱼ||
    where C is a known constant for S².

    Actually, we use the simpler spherical cap discrepancy w.r.t. pole direction.
    For computational efficiency, we use multiple random poles and average.
    """
    if len(points_on_sphere) == 0:
        return float('inf')

    N = len(points_on_sphere)
    pts = np.array(points_on_sphere)

    # Stolarsky invariant principle for S²:
    # The L2 discrepancy satisfies:
    # D²_L2 = 1/3 - (1/N²) Σᵢ<ⱼ ||xᵢ - xⱼ|| / (2π)
    # Actually the generalized form uses:
    # D²_L2 = ∫∫ K(x,y) dμ(x)dμ(y) - (2/N)Σᵢ ∫ K(xᵢ,y)dμ(y) + (1/N²)ΣᵢΣⱼ K(xᵢ,xⱼ)

    # Use spherical harmonic expansion approach instead.
    # The L2 discrepancy decomposes as:
    # D²_L2 = Σ_{ℓ≥1} (1/(2ℓ+1)) |Σⱼ Pℓ(xⱼ·pole)/N - δ_{ℓ,0}|²
    # averaged over poles.

    # Simpler: compute cap discrepancy w.r.t. z-axis at 50 thresholds
    cos_thetas = np.linspace(-0.99, 0.99, 100)
    z_vals = pts[:, 2] if pts.ndim == 2 else np.array([p[2] for p in points_on_sphere])

    disc_sq_sum = 0.0
    for ct in cos_thetas:
        empirical = np.sum(z_vals >= ct) / N
        theoretical = spherical_cap_area(ct)
        disc_sq_sum += (empirical - theoretical) ** 2

    # Average over multiple random poles for isotropy
    np.random.seed(42)
    n_poles = 20
    for _ in range(n_poles):
        # Random pole direction
        pole = np.random.randn(3)
        pole /= np.linalg.norm(pole)
        dots = pts @ pole
        for ct in cos_thetas:
            empirical = np.sum(dots >= ct) / N
            theoretical = spherical_cap_area(ct)
            disc_sq_sum += (empirical - theoretical) ** 2

    return np.sqrt(disc_sq_sum / (len(cos_thetas) * (1 + n_poles)))


def energy_discrepancy(points_on_sphere):
    """Alternative discrepancy: generalized energy / Riesz s-energy.
    Uses the fact that for uniform distribution on S²,
    the average pairwise distance is 4/3.
    Discrepancy ~ |avg_distance - 4/3|.
    Also compute the Coulomb energy deviation."""
    if len(points_on_sphere) < 2:
        return 0.0, 0.0

    pts = np.array(points_on_sphere)
    N = len(pts)

    # Pairwise distances
    total_dist = 0.0
    count = 0
    for i in range(min(N, 500)):  # cap for speed
        for j in range(i + 1, min(N, 500)):
            d = np.linalg.norm(pts[i] - pts[j])
            total_dist += d
            count += 1

    avg_dist = total_dist / count if count > 0 else 0
    distance_discrepancy = abs(avg_dist - 4.0/3.0)

    return avg_dist, distance_discrepancy


# ============================================================
# PART 3: Spherical Harmonics
# ============================================================

def real_spherical_harmonic(l, m, x, y, z):
    """Compute real spherical harmonics Y_l^m evaluated at point (x,y,z) on S².
    Uses Cartesian form for low l values (0,1,2,3).
    Points assumed to be on unit sphere: x²+y²+z² = 1."""

    if l == 0 and m == 0:
        return 1.0 / np.sqrt(4 * np.pi)

    if l == 1:
        if m == -1:
            return np.sqrt(3/(4*np.pi)) * y
        elif m == 0:
            return np.sqrt(3/(4*np.pi)) * z
        elif m == 1:
            return np.sqrt(3/(4*np.pi)) * x

    if l == 2:
        if m == -2:
            return np.sqrt(15/(4*np.pi)) * x * y
        elif m == -1:
            return np.sqrt(15/(4*np.pi)) * y * z
        elif m == 0:
            return np.sqrt(5/(16*np.pi)) * (2*z*z - x*x - y*y)
        elif m == 1:
            return np.sqrt(15/(4*np.pi)) * x * z
        elif m == 2:
            return np.sqrt(15/(16*np.pi)) * (x*x - y*y)

    if l == 3:
        if m == -3:
            return np.sqrt(35/(32*np.pi)) * y * (3*x*x - y*y)
        elif m == -2:
            return np.sqrt(105/(4*np.pi)) * x * y * z
        elif m == -1:
            return np.sqrt(21/(32*np.pi)) * y * (4*z*z - x*x - y*y)
        elif m == 0:
            return np.sqrt(7/(16*np.pi)) * z * (2*z*z - 3*x*x - 3*y*y)
        elif m == 1:
            return np.sqrt(21/(32*np.pi)) * x * (4*z*z - x*x - y*y)
        elif m == 2:
            return np.sqrt(105/(16*np.pi)) * z * (x*x - y*y)
        elif m == 3:
            return np.sqrt(35/(32*np.pi)) * x * (x*x - 3*y*y)

    # For higher l, use scipy
    try:
        from scipy.special import sph_harm
        r = np.sqrt(x*x + y*y + z*z)
        if r < 1e-15:
            return 0.0
        theta = np.arccos(np.clip(z/r, -1, 1))
        phi = np.arctan2(y, x)
        if m >= 0:
            return np.real(sph_harm(m, l, phi, theta)) * np.sqrt(2) if m > 0 else np.real(sph_harm(0, l, phi, theta))
        else:
            return np.imag(sph_harm(-m, l, phi, theta)) * np.sqrt(2)
    except ImportError:
        return 0.0


def compute_harmonic_sums(pts_on_sphere, l_max=4):
    """For points on S², compute Σ Y_l^m(pt) for all l=0..l_max, m=-l..l.
    Returns dict: (l,m) -> sum."""
    results = {}
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            s = 0.0
            for pt in pts_on_sphere:
                s += real_spherical_harmonic(l, m, pt[0], pt[1], pt[2])
            results[(l, m)] = s
    return results


# ============================================================
# PART 4: Bridge Identity Check
# ============================================================

def mertens_function(n):
    """Compute M(n) = Σ_{k=1}^{n} μ(k)."""
    # Sieve for Mobius function
    mu = np.ones(n + 1, dtype=np.int64)
    mu[0] = 0
    is_prime = [True] * (n + 1)
    for p in range(2, n + 1):
        if is_prime[p]:
            for j in range(p, n + 1, p):
                if j > p:
                    is_prime[j] = False
                mu[j] *= -1
            p2 = p * p
            for j in range(p2, n + 1, p2):
                mu[j] = 0
    return np.cumsum(mu)

def circular_bridge_identity(p, farey_pts=None):
    """On S¹: Σ_{f in F_p} e^{2πi p f} = M(p) + 2.
    Verify this for reference."""
    # Farey fractions of order p
    from fractions import Fraction
    fracs = set()
    for q in range(1, p + 1):
        for a in range(0, q + 1):
            fracs.add(Fraction(a, q))
    fracs = sorted(fracs)

    total = sum(np.exp(2j * np.pi * float(f) * p) for f in fracs)
    return total


# ============================================================
# MAIN COMPUTATION
# ============================================================

def main():
    print("=" * 70)
    print("SPHERE EQUIDISTRIBUTION: Extending Farey ΔW to S²")
    print("=" * 70)
    print()

    N_MAX = 1000

    # Step 1: Compute r₃(n)
    print("[1/5] Computing r₃(n) for n=0..{} ...".format(N_MAX))
    t0 = time.time()
    r3 = compute_r3(N_MAX)
    print(f"  Done in {time.time()-t0:.1f}s")

    # Verify: r₃(0)=1, r₃(1)=6, r₃(2)=12, r₃(3)=8
    print(f"  r₃(0)={r3[0]}, r₃(1)={r3[1]}, r₃(2)={r3[2]}, r₃(3)={r3[3]}")
    print(f"  r₃(4)={r3[4]}, r₃(5)={r3[5]}, r₃(7)={r3[7]}")
    # Legendre: r₃(n)=0 iff n=4^a(8b+7)
    zeros = [n for n in range(1, 100) if r3[n] == 0]
    print(f"  Zeros of r₃ in [1,100]: {zeros}")
    print(f"  (Should be 4^a(8b+7): 7,15,23,28,31,39,47,55,56,60,...)")

    # Step 2: Get primes and their lattice points
    primes = sieve_primes(N_MAX)
    # Filter: primes p must have r₃(p) > 0, i.e., p ≠ 7 mod 8
    # Actually p=4^a(8b+7) means p≡7(mod 8) for prime p
    primes_with_reps = [(p, r3[p]) for p in primes if r3[p] > 0]
    print(f"\n[2/5] Primes with r₃(p)>0: {len(primes_with_reps)} out of {len(primes)}")
    print(f"  Primes p≡7(mod 8) with r₃=0: {[p for p in primes if r3[p]==0][:20]}")

    # Step 3: Compute spherical discrepancy for each prime
    print(f"\n[3/5] Computing spherical discrepancy for each prime...")

    results = []
    prev_disc = None
    cumulative_pts = []  # accumulate all points seen so far

    for idx, (p, r3p) in enumerate(primes_with_reps):
        # Get lattice points for this prime
        pts = get_lattice_points(p)

        if len(pts) != r3p:
            # Possible duplicates or missing — use r3p as ground truth
            pass

        if len(pts) == 0:
            continue

        # Normalize to unit sphere
        sqrt_p = np.sqrt(p)
        sphere_pts = [(a/sqrt_p, b/sqrt_p, c/sqrt_p) for (a,b,c) in pts]

        # Method A: discrepancy of just this prime's points
        disc_p = l2_cap_discrepancy(sphere_pts) if len(sphere_pts) >= 3 else float('inf')

        # Method B: cumulative discrepancy (like Farey — add points as we go through primes)
        cumulative_pts.extend(sphere_pts)
        disc_cum = l2_cap_discrepancy(cumulative_pts) if len(cumulative_pts) >= 3 else float('inf')

        # ΔW_sphere
        if prev_disc is not None:
            delta_w = disc_cum - prev_disc
        else:
            delta_w = 0.0

        # Average pairwise distance (quick quality check)
        avg_d, d_disc = energy_discrepancy(sphere_pts)

        results.append({
            'p': p,
            'r3': r3p,
            'r3_actual': len(pts),
            'disc_single': disc_p,
            'disc_cumulative': disc_cum,
            'delta_w': delta_w,
            'avg_dist': avg_d,
            'dist_disc': d_disc,
            'n_cumulative': len(cumulative_pts),
        })

        prev_disc = disc_cum

        if idx < 10 or idx % 20 == 0:
            print(f"  p={p:4d}  r₃(p)={r3p:4d}  D_single={disc_p:.6f}  "
                  f"D_cum={disc_cum:.6f}  ΔW={delta_w:+.6f}")

    # Step 4: Spherical harmonic sums (Bridge Identity analog)
    print(f"\n[4/5] Computing spherical harmonic sums for primes...")
    print(f"  On S¹: Σ e^{{2πipf}} = M(p)+2")
    print(f"  On S²: Σ_{{a²+b²+c²=p}} Y_l^m(a/√p, b/√p, c/√p) = ???")

    # Also compute Mertens for comparison
    M = mertens_function(N_MAX)

    harmonic_results = []
    test_primes = [p for p, r in primes_with_reps if p <= 200]

    for p in test_primes:
        pts = get_lattice_points(p)
        if len(pts) == 0:
            continue
        sqrt_p = np.sqrt(p)
        sphere_pts = [(a/sqrt_p, b/sqrt_p, c/sqrt_p) for (a,b,c) in pts]

        h_sums = compute_harmonic_sums(sphere_pts, l_max=3)

        entry = {
            'p': p,
            'r3': len(pts),
            'M_p': int(M[p]),
            'harmonic_sums': {f"({l},{m})": float(h_sums[(l,m)]) for l in range(4) for m in range(-l, l+1)},
        }

        # Key check: Y_0^0 sum should be r₃(p)/√(4π) since Y_0^0 = 1/√(4π)
        y00_sum = h_sums[(0, 0)]
        expected_y00 = len(pts) / np.sqrt(4 * np.pi)

        # Normalized sums (divide by r₃(p) to get "average")
        entry['y00_sum'] = float(y00_sum)
        entry['y00_expected'] = float(expected_y00)

        # Check l=1 sums: should these vanish by symmetry?
        # If (a,b,c) is a rep, so is (-a,b,c), etc. So Y_1^m sums should be 0!
        l1_sums = [h_sums[(1, m)] for m in [-1, 0, 1]]
        entry['l1_sum_norm'] = float(np.sqrt(sum(s**2 for s in l1_sums)))

        # l=2 sums — these are the first non-trivial ones
        l2_sums = [h_sums[(2, m)] for m in range(-2, 3)]
        entry['l2_sums'] = [float(s) for s in l2_sums]
        entry['l2_sum_norm'] = float(np.sqrt(sum(s**2 for s in l2_sums)))

        # Normalized l=2 sum (per representation)
        entry['l2_per_rep'] = float(np.sqrt(sum(s**2 for s in l2_sums)) / len(pts)) if len(pts) > 0 else 0

        harmonic_results.append(entry)

        if p <= 50 or p in [97, 101, 197, 199]:
            print(f"  p={p:4d}: r₃={len(pts):3d}, M(p)={int(M[p]):+3d}, "
                  f"Y₀₀_sum={y00_sum:.3f} (exp={expected_y00:.3f}), "
                  f"|Y₁|={entry['l1_sum_norm']:.6f}, "
                  f"|Y₂|={entry['l2_sum_norm']:.3f}")

    # Step 5: Analysis and plots
    print(f"\n[5/5] Analysis and plotting...")

    # Extract data for plotting
    p_vals = [r['p'] for r in results]
    delta_w_vals = [r['delta_w'] for r in results]
    disc_cum_vals = [r['disc_cumulative'] for r in results]
    r3_vals = [r['r3'] for r in results]

    # Key question: Is ΔW_sphere always negative (like our Sign Theorem on S¹)?
    positive_dw = [(r['p'], r['delta_w']) for r in results[1:] if r['delta_w'] > 0]
    negative_dw = [(r['p'], r['delta_w']) for r in results[1:] if r['delta_w'] < 0]

    print(f"\n  === SIGN THEOREM ANALOG ON S² ===")
    print(f"  ΔW > 0 (discrepancy INCREASED): {len(positive_dw)} primes")
    print(f"  ΔW < 0 (discrepancy DECREASED): {len(negative_dw)} primes")
    print(f"  ΔW = 0: {len(results) - 1 - len(positive_dw) - len(negative_dw)} primes")

    if len(positive_dw) > 0:
        print(f"  SIGN THEOREM FAILS on S²! Positive ΔW at: {[p for p,_ in positive_dw[:20]]}")
    else:
        print(f"  SIGN THEOREM HOLDS on S²! ΔW ≤ 0 for all primes tested.")

    # Correlation between ΔW_sphere and M(p)
    dw_arr = np.array([r['delta_w'] for r in results[1:]])
    mp_arr = np.array([int(M[r['p']]) for r in results[1:]])
    if len(dw_arr) > 5:
        corr = np.corrcoef(dw_arr, mp_arr)[0, 1]
        print(f"\n  Correlation(ΔW_sphere, M(p)): {corr:.4f}")
        print(f"  (On S¹, ΔW correlates strongly with M(p) — does it on S²?)")

    # Spherical harmonic analysis summary
    print(f"\n  === SPHERICAL HARMONIC BRIDGE IDENTITY ===")
    print(f"  l=1 sums (should vanish by sign symmetry):")
    for hr in harmonic_results[:5]:
        print(f"    p={hr['p']}: |Y₁_sum| = {hr['l1_sum_norm']:.2e}")

    print(f"\n  l=2 sums (first non-trivial — analog of exponential sum):")
    # Check if l=2 sum relates to M(p) or some arithmetic function
    l2_norms = [(hr['p'], hr['l2_sum_norm'], hr['M_p']) for hr in harmonic_results if hr['r3'] > 0]
    for p, l2n, mp in l2_norms[:10]:
        print(f"    p={p:4d}: |Y₂_sum|={l2n:8.3f}, r₃(p)={r3[p]:4d}, M(p)={mp:+3d}")

    # Check: is |Y₂_sum| / r₃(p) bounded? Decaying?
    if l2_norms:
        ratios = [(p, l2n / r3[p]) for p, l2n, mp in l2_norms if r3[p] > 0]
        print(f"\n  |Y₂_sum|/r₃(p) ratios:")
        for p, ratio in ratios[:10]:
            print(f"    p={p}: {ratio:.6f}")
        ratio_vals = [r for _, r in ratios]
        print(f"    Mean ratio: {np.mean(ratio_vals):.6f}")
        print(f"    Max ratio:  {np.max(ratio_vals):.6f}")
        print(f"    → Duke's theorem says this → 0 as p → ∞")

    # Y_2^0 specifically: relates to z² - 1/3, the simplest non-trivial test function
    print(f"\n  Y₂⁰ sum specifically (the 'z²-1/3' test):")
    for hr in harmonic_results[:10]:
        y20 = hr['harmonic_sums'].get('(2,0)', 0)
        print(f"    p={hr['p']:4d}: Y₂⁰_sum = {y20:+10.4f}, normalized = {y20/hr['r3']:+.6f}")

    # Save results
    output = {
        'r3_values': {str(n): int(r3[n]) for n in range(min(200, N_MAX+1))},
        'discrepancy_results': results,
        'harmonic_results': harmonic_results,
        'sign_theorem': {
            'positive_count': len(positive_dw),
            'negative_count': len(negative_dw),
            'holds': len(positive_dw) == 0,
        },
    }

    outpath = os.path.expanduser('~/Desktop/Farey-Local/experiments/sphere_equidistribution_results.json')
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Results saved to {outpath}")

    # Plotting
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Sphere Equidistribution: Extending Farey ΔW to S²', fontsize=14)

        # Plot 1: r₃(n) for all n
        ax = axes[0, 0]
        ns = range(1, min(200, N_MAX+1))
        ax.scatter(ns, [r3[n] for n in ns], s=3, alpha=0.5)
        prime_ns = [p for p in primes if p < 200]
        ax.scatter(prime_ns, [r3[p] for p in prime_ns], s=10, c='red', label='primes', zorder=5)
        ax.set_xlabel('n')
        ax.set_ylabel('r₃(n)')
        ax.set_title('r₃(n) = representations as sum of 3 squares')
        ax.legend()

        # Plot 2: Cumulative discrepancy
        ax = axes[0, 1]
        ax.plot(p_vals[1:], disc_cum_vals[1:], 'b-', lw=0.8)
        ax.set_xlabel('Prime p')
        ax.set_ylabel('Cumulative L2 cap discrepancy')
        ax.set_title('Spherical discrepancy (cumulative)')

        # Plot 3: ΔW_sphere(p) — THE KEY PLOT
        ax = axes[0, 2]
        colors = ['red' if dw > 0 else 'blue' for dw in delta_w_vals[1:]]
        ax.bar(p_vals[1:], delta_w_vals[1:], color=colors, width=2, alpha=0.7)
        ax.axhline(y=0, color='black', lw=0.5)
        ax.set_xlabel('Prime p')
        ax.set_ylabel('ΔW_sphere(p)')
        ax.set_title('Per-step spherical discrepancy change (Sign Theorem test)')

        # Plot 4: ΔW_sphere vs M(p)
        ax = axes[1, 0]
        mp_for_plot = [int(M[r['p']]) for r in results[1:]]
        ax.scatter(mp_for_plot, delta_w_vals[1:], s=10, alpha=0.5)
        ax.set_xlabel('M(p) (Mertens function)')
        ax.set_ylabel('ΔW_sphere(p)')
        ax.set_title(f'ΔW_sphere vs M(p) (corr={corr:.3f})' if len(dw_arr) > 5 else 'ΔW_sphere vs M(p)')
        ax.axhline(y=0, color='black', lw=0.5)
        ax.axvline(x=0, color='black', lw=0.5)

        # Plot 5: |Y₂| sum vs p
        ax = axes[1, 1]
        hp = [hr['p'] for hr in harmonic_results]
        hl2 = [hr['l2_sum_norm'] for hr in harmonic_results]
        hr3 = [hr['r3'] for hr in harmonic_results]
        ax.scatter(hp, hl2, s=15, c='green', label='|Y₂ sum|')
        ax.scatter(hp, [r3[p] for p in hp], s=15, c='gray', alpha=0.3, label='r₃(p)')
        ax.set_xlabel('Prime p')
        ax.set_ylabel('|Y₂ sum|')
        ax.set_title('Spherical harmonic l=2 sum')
        ax.legend()

        # Plot 6: Normalized Y₂ sum (bridge identity test)
        ax = axes[1, 2]
        normalized_l2 = [hr['l2_per_rep'] for hr in harmonic_results]
        ax.scatter(hp, normalized_l2, s=15, c='purple')
        ax.set_xlabel('Prime p')
        ax.set_ylabel('|Y₂ sum| / r₃(p)')
        ax.set_title('Normalized Y₂ sum → 0? (Duke\'s theorem)')
        # Add power-law fit
        if len(hp) > 5:
            from numpy.polynomial import polynomial as P
            log_p = np.log(np.array(hp))
            log_r = np.log(np.array(normalized_l2) + 1e-15)
            mask = np.isfinite(log_r) & (np.array(normalized_l2) > 1e-10)
            if np.sum(mask) > 3:
                coeffs = np.polyfit(log_p[mask], log_r[mask], 1)
                ax.plot(hp, np.exp(coeffs[1]) * np.array(hp)**coeffs[0],
                       'r--', label=f'slope={coeffs[0]:.3f}')
                ax.legend()
                print(f"\n  Power-law fit: |Y₂|/r₃ ~ p^{{{coeffs[0]:.3f}}}")
                print(f"  Duke's theorem predicts decay ~ p^{{-1/28}} = p^{{-0.036}}")

        plt.tight_layout()
        plotpath = os.path.expanduser('~/Desktop/Farey-Local/experiments/sphere_equidistribution.png')
        plt.savefig(plotpath, dpi=150, bbox_inches='tight')
        print(f"  Plot saved to {plotpath}")

    except ImportError as e:
        print(f"  Matplotlib not available: {e}")

    print("\n" + "=" * 70)
    print("COMPUTATION COMPLETE")
    print("=" * 70)

    return results, harmonic_results


if __name__ == '__main__':
    results, harmonic_results = main()
