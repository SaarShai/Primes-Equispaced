#!/usr/bin/env python3
"""
Sphere Equidistribution v2: Breaking the octahedral symmetry

The v1 script found that ALL Y_l^m sums vanish exactly. This is because:
- If (a,b,c) is a rep, so are all 48 images under octahedral group Oh
- Oh acts on S² and Y_l^m transforms as irreps of Oh
- The sum over a FULL orbit always vanishes for l >= 1

Fix: Use PRIMITIVE representations:
  Method A: Take one point per orbit (a >= b >= c >= 0)
  Method B: Use "genus theory" points — weight by 1/|stabilizer|
  Method C: Use the DIRECTION points only — (a,b,c) with gcd(a,b,c)=1

Also: The right analog of the Farey exponential sum is NOT Y_l^m
but rather the THETA SERIES itself. The bridge identity on S² relates
to Fourier coefficients of the theta function, which are r_3(n,P) —
the weighted representation numbers.

For the Sign Theorem analog, we should look at:
- Whether cumulative cap discrepancy of ORBIT REPRESENTATIVES decreases at primes
- The theta coefficients r_3(p,P) for specific harmonic polynomials P

Key insight: r_3(n, Y_2^0) = Σ_{a²+b²+c²=n} (2c² - a² - b²)
This does NOT vanish because the polynomial P(a,b,c) = 2c²-a²-b²
is evaluated at INTEGER points, not unit sphere points.
"""

import numpy as np
from collections import defaultdict
import json
import os
import time

def sieve_primes(N):
    is_prime = [False, False] + [True] * (N - 1)
    for i in range(2, int(N**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, N + 1, i):
                is_prime[j] = False
    return [p for p in range(2, N + 1) if is_prime[p]]

def get_lattice_points(n):
    """Return all (a,b,c) with a²+b²+c² = n."""
    pts = set()
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
            if rem < 0:
                continue
            c = int(np.sqrt(rem) + 0.5)
            if c * c == rem:
                pts.add((a, b, c))
                pts.add((a, b, -c))
            # Also check c-1 for rounding
            c2 = int(np.sqrt(rem))
            if c2 * c2 == rem:
                pts.add((a, b, c2))
                pts.add((a, b, -c2))
    return list(pts)

def get_primitive_reps(n):
    """Get one representative per orbit under octahedral group Oh.
    Take points with a >= b >= c >= 0."""
    all_pts = get_lattice_points(n)
    primitive = set()
    for (a, b, c) in all_pts:
        # Canonical form: sorted absolute values, descending
        vals = sorted([abs(a), abs(b), abs(c)], reverse=True)
        primitive.add(tuple(vals))
    return list(primitive)

def get_positive_octant_reps(n):
    """Get points with a > 0 (first coordinate positive).
    This breaks half the sign symmetry while keeping some structure."""
    all_pts = get_lattice_points(n)
    return [(a, b, c) for (a, b, c) in all_pts if a > 0]

def mertens_function(n):
    mu = np.ones(n + 1, dtype=np.int64)
    mu[0] = 0
    is_prime_arr = [True] * (n + 1)
    for p in range(2, n + 1):
        if is_prime_arr[p]:
            for j in range(p, n + 1, p):
                if j > p:
                    is_prime_arr[j] = False
                mu[j] *= -1
            p2 = p * p
            for j in range(p2, n + 1, p2):
                mu[j] = 0
    return np.cumsum(mu)


# ============================================================
# WEIGHTED REPRESENTATION NUMBERS r_3(n, P)
# These are the actual Fourier coefficients of theta_P(z)
# ============================================================

def r3_weighted(n, harmonic='Y20'):
    """Compute r₃(n, P) = Σ_{a²+b²+c²=n} P(a,b,c)
    where P is a harmonic polynomial (NOT evaluated on unit sphere).

    Key formulas:
    P = 2c²-a²-b² corresponds to Y_2^0 direction
    P = a²-b² corresponds to Y_2^2 direction
    P = ab corresponds to Y_2^{-2} direction
    """
    pts = get_lattice_points(n)
    if len(pts) == 0:
        return 0.0

    total = 0.0
    for (a, b, c) in pts:
        if harmonic == 'Y20':
            # P = 2c² - a² - b² (proportional to Y_2^0)
            total += 2*c*c - a*a - b*b
        elif harmonic == 'Y22':
            # P = a² - b²
            total += a*a - b*b
        elif harmonic == 'Y2m2':
            # P = ab
            total += a * b
        elif harmonic == 'Y21':
            # P = ac
            total += a * c
        elif harmonic == 'Y2m1':
            # P = bc
            total += b * c
        elif harmonic == 'Y30':
            # P = c(2c² - 3a² - 3b²)
            total += c * (2*c*c - 3*a*a - 3*b*b)
        elif harmonic == 'cubic':
            # P = a*b*c — not a spherical harmonic but tests l=3 sector
            total += a * b * c
    return total


def l2_cap_discrepancy_directed(points_on_sphere, n_poles=30, n_thresholds=80):
    """Compute rotationally-averaged L2 cap discrepancy."""
    if len(points_on_sphere) < 2:
        return float('inf')

    N = len(points_on_sphere)
    pts = np.array(points_on_sphere)
    cos_thetas = np.linspace(-0.95, 0.95, n_thresholds)

    np.random.seed(42)
    disc_sq_sum = 0.0
    total_tests = 0

    for _ in range(n_poles):
        pole = np.random.randn(3)
        pole /= np.linalg.norm(pole)
        dots = pts @ pole

        for ct in cos_thetas:
            empirical = np.sum(dots >= ct) / N
            theoretical = (1.0 - ct) / 2.0
            disc_sq_sum += (empirical - theoretical) ** 2
            total_tests += 1

    return np.sqrt(disc_sq_sum / total_tests)


def main():
    print("=" * 70)
    print("SPHERE EQUIDISTRIBUTION v2: Breaking Symmetry + Theta Coefficients")
    print("=" * 70)

    N_MAX = 500
    primes = sieve_primes(N_MAX)
    M = mertens_function(N_MAX)

    # ============================================================
    # PART A: Weighted representation numbers r_3(n, P)
    # These are the ACTUAL Fourier coefficients — the bridge identity analog
    # ============================================================
    print("\n[A] WEIGHTED REPRESENTATION NUMBERS r₃(n, P)")
    print("   These are Fourier coefficients of theta_P(z), weight 3/2 + deg(P)")
    print("   On S¹: the analog is Σ e^{2πipf} = M(p)+2")
    print("   On S²: r₃(p, Y₂⁰) = Σ_{a²+b²+c²=p} (2c²-a²-b²)")
    print()

    r3_y20_data = []
    r3_y22_data = []
    r3_y30_data = []
    r3_plain_data = []

    for p in primes:
        pts = get_lattice_points(p)
        r3p = len(pts)
        if r3p == 0:
            continue

        y20 = r3_weighted(p, 'Y20')
        y22 = r3_weighted(p, 'Y22')
        y30 = r3_weighted(p, 'Y30')

        r3_y20_data.append({'p': p, 'r3': r3p, 'r3_Y20': y20, 'M': int(M[p])})
        r3_y22_data.append({'p': p, 'r3': r3p, 'r3_Y22': y22})
        r3_y30_data.append({'p': p, 'r3': r3p, 'r3_Y30': y30})
        r3_plain_data.append({'p': p, 'r3': r3p})

        if p <= 50 or p in [97, 101, 197, 199]:
            print(f"  p={p:4d}: r₃={r3p:4d}, r₃(Y₂⁰)={y20:+8.0f}, "
                  f"r₃(Y₂²)={y22:+8.0f}, r₃(Y₃⁰)={y30:+8.0f}, M(p)={int(M[p]):+3d}")

    # KEY ANALYSIS: Do these vanish by symmetry too?
    print(f"\n  Analysis of r₃(p, Y₂⁰):")
    y20_vals = [d['r3_Y20'] for d in r3_y20_data]
    nonzero_y20 = [d for d in r3_y20_data if abs(d['r3_Y20']) > 0.5]
    print(f"    Non-zero count: {len(nonzero_y20)} / {len(r3_y20_data)}")

    if len(nonzero_y20) == 0:
        print(f"    ALL ZERO — the cubic symmetry kills Y₂⁰ at integer level too!")
        print(f"    Reason: (a,b,c) → (b,c,a) permutation symmetry makes")
        print(f"    Σ(2c²-a²-b²) = Σ(2a²-b²-c²) = Σ(2b²-c²-a²)")
        print(f"    Adding: 3·Σ(2c²-a²-b²) = 0 → Σ(2c²-a²-b²) = 0")
        print(f"\n    This means: the FULL octahedral sum kills ALL degree-2 harmonics")
        print(f"    for a²+b²+c²=n (any n), because the form is isotropic under S₃.")
    else:
        print(f"    Found non-zero values!")
        for d in nonzero_y20[:10]:
            print(f"      p={d['p']}: r₃(Y₂⁰)={d['r3_Y20']}")

    print(f"\n  Analysis of r₃(p, Y₃⁰):")
    nonzero_y30 = [d for d in r3_y30_data if abs(d['r3_Y30']) > 0.5]
    print(f"    Non-zero count: {len(nonzero_y30)} / {len(r3_y30_data)}")

    # ============================================================
    # PART B: USE ANISOTROPIC FORMS — Break the S₃ permutation symmetry
    # Instead of a²+b²+c² = n, use a²+b²+2c² = n or similar
    # ============================================================
    print(f"\n{'='*70}")
    print("[B] ANISOTROPIC FORM: a² + b² + 2c² = p")
    print("   This breaks S₃ permutation symmetry → Y₂⁰ should NOT vanish")
    print()

    def get_aniso_points(n):
        """Return (a,b,c) with a² + b² + 2c² = n."""
        pts = set()
        bound = int(np.sqrt(n)) + 1
        for c in range(-bound, bound + 1):
            rem = n - 2 * c * c
            if rem < 0:
                continue
            for b in range(-bound, bound + 1):
                rem2 = rem - b * b
                if rem2 < 0:
                    continue
                a = int(np.sqrt(rem2) + 0.5)
                if a * a == rem2:
                    pts.add((a, b, c))
                    pts.add((-a, b, c))
                a2 = int(np.sqrt(rem2))
                if a2 * a2 == rem2:
                    pts.add((a2, b, c))
                    pts.add((-a2, b, c))
        return list(pts)

    def aniso_weighted(n, harmonic='Y20'):
        pts = get_aniso_points(n)
        total = 0.0
        for (a, b, c) in pts:
            if harmonic == 'Y20':
                total += 2*c*c - a*a - b*b
            elif harmonic == 'Z20':
                # Adapted: weight by the natural metric of the form
                # On the ellipsoid a²+b²+2c² = n, use (a/√n, b/√n, c√2/√n)
                total += 2*(2*c*c) - a*a - b*b  # enhanced c-weight
        return total, len(pts)

    aniso_results = []
    for p in primes[:80]:
        w, npts = aniso_weighted(p, 'Y20')
        if npts > 0:
            aniso_results.append({'p': p, 'npts': npts, 'w_Y20': w, 'M': int(M[p])})
            if p <= 50 or len(aniso_results) % 15 == 0:
                print(f"  p={p:4d}: npts={npts:4d}, Σ(2c²-a²-b²)={w:+8.0f}, M(p)={int(M[p]):+3d}")

    nonzero_aniso = [d for d in aniso_results if abs(d['w_Y20']) > 0.5]
    print(f"\n  Non-zero r₃(p, Y₂⁰) for anisotropic form: {len(nonzero_aniso)} / {len(aniso_results)}")

    if len(nonzero_aniso) > 0:
        print(f"  SUCCESS: Anisotropic form breaks the symmetry!")
        # Check correlation with M(p)
        w_vals = np.array([d['w_Y20'] for d in aniso_results if abs(d['w_Y20']) > 0.1])
        m_vals = np.array([d['M'] for d in aniso_results if abs(d['w_Y20']) > 0.1])
        if len(w_vals) > 5:
            corr = np.corrcoef(w_vals, m_vals)[0, 1]
            print(f"  Correlation(r₃(p,Y₂⁰), M(p)) = {corr:.4f}")

    # ============================================================
    # PART C: Correct approach — PRIMITIVE orbit representatives
    # Take one point per Oh-orbit and compute cap discrepancy
    # ============================================================
    print(f"\n{'='*70}")
    print("[C] DISCREPANCY OF ORBIT REPRESENTATIVES ON S²")
    print("   One point per octahedral orbit, normalized to S²")
    print()

    disc_results = []
    prev_disc = None
    cumulative_pts = []

    for p in primes:
        prim = get_primitive_reps(p)
        if len(prim) == 0:
            continue

        sqrt_p = np.sqrt(p)
        # These are (a >= b >= c >= 0), normalize to sphere
        sphere_pts = [(a/sqrt_p, b/sqrt_p, c/sqrt_p) for (a, b, c) in prim]
        cumulative_pts.extend(sphere_pts)

        if len(cumulative_pts) >= 3:
            disc = l2_cap_discrepancy_directed(cumulative_pts)
            delta_w = disc - prev_disc if prev_disc is not None else 0.0
            disc_results.append({
                'p': p, 'n_orbits': len(prim),
                'disc': disc, 'delta_w': delta_w,
                'n_cum': len(cumulative_pts), 'M': int(M[p])
            })
            prev_disc = disc

            if p <= 30 or len(disc_results) % 15 == 0:
                print(f"  p={p:4d}: orbits={len(prim):3d}, D={disc:.6f}, "
                      f"ΔW={delta_w:+.6f}, n_cum={len(cumulative_pts)}")

    # Sign theorem test
    pos_dw = [d for d in disc_results[1:] if d['delta_w'] > 0]
    neg_dw = [d for d in disc_results[1:] if d['delta_w'] < 0]
    print(f"\n  === SIGN THEOREM (orbit representatives) ===")
    print(f"  ΔW > 0: {len(pos_dw)} primes")
    print(f"  ΔW < 0: {len(neg_dw)} primes")
    if len(pos_dw) > 0:
        print(f"  Sign theorem FAILS for orbit reps on S²")
        print(f"  Ratio positive: {len(pos_dw)/(len(pos_dw)+len(neg_dw)):.2%}")
    else:
        print(f"  Sign theorem HOLDS for orbit reps on S²!")

    # ΔW vs M(p) correlation
    if len(disc_results) > 5:
        dw = np.array([d['delta_w'] for d in disc_results[1:]])
        mp = np.array([d['M'] for d in disc_results[1:]])
        corr = np.corrcoef(dw, mp)[0, 1]
        print(f"  Correlation(ΔW_orbit, M(p)): {corr:.4f}")

    # ============================================================
    # PART D: The CORRECT bridge identity analog
    # On S¹: Σ_{k≤N, gcd(k,N)=1} e^{2πi k/N} = μ(N) (Ramanujan sum)
    # On S²: Use the theta series with CHARACTER
    # θ_χ(z) = Σ_n r₃(n,χ) q^n where χ is a Dirichlet character
    # ============================================================
    print(f"\n{'='*70}")
    print("[D] THETA SERIES WITH CHARACTERS — True Bridge Identity")
    print("   θ(z,χ) = Σ χ(a)χ(b)χ(c) q^{a²+b²+c²}")
    print("   Fourier coefficients: r₃(n,χ) = Σ_{a²+b²+c²=n} χ(a)χ(b)χ(c)")
    print()

    def r3_character(n, q_mod):
        """Compute r₃(n, χ) = Σ_{a²+b²+c²=n} χ(a)χ(b)χ(c)
        where χ is the Legendre symbol mod q_mod (must be odd prime)."""
        pts = get_lattice_points(n)
        if len(pts) == 0:
            return 0

        def legendre(a, p):
            if a % p == 0:
                return 0
            return pow(a, (p-1)//2, p) if pow(a, (p-1)//2, p) <= 1 else -1

        total = 0
        for (a, b, c) in pts:
            chi_a = legendre(a, q_mod)
            chi_b = legendre(b, q_mod)
            chi_c = legendre(c, q_mod)
            total += chi_a * chi_b * chi_c
        return total

    # Test with χ = Legendre symbol mod 3
    print("  Using χ = Legendre symbol mod 3:")
    char_results_3 = []
    for p in primes[:60]:
        pts = get_lattice_points(p)
        if len(pts) == 0:
            continue
        r3c = r3_character(p, 3)
        char_results_3.append({'p': p, 'r3': len(pts), 'r3_chi3': r3c, 'M': int(M[p])})
        if p <= 30 or len(char_results_3) % 10 == 0:
            print(f"    p={p:4d}: r₃={len(pts):4d}, r₃(χ₃)={r3c:+6d}, M(p)={int(M[p]):+3d}")

    nonzero_chi3 = [d for d in char_results_3 if abs(d['r3_chi3']) > 0]
    print(f"\n  Non-zero r₃(p, χ₃): {len(nonzero_chi3)} / {len(char_results_3)}")

    if len(nonzero_chi3) > 3:
        # Correlation with M(p)
        vals_c = np.array([d['r3_chi3'] for d in char_results_3])
        vals_m = np.array([d['M'] for d in char_results_3])
        if np.std(vals_c) > 0:
            corr = np.corrcoef(vals_c, vals_m)[0, 1]
            print(f"  Correlation(r₃(χ₃), M(p)) = {corr:.4f}")

    # Test with χ = Legendre symbol mod 5
    print("\n  Using χ = Legendre symbol mod 5:")
    char_results_5 = []
    for p in primes[:60]:
        pts = get_lattice_points(p)
        if len(pts) == 0:
            continue
        r3c = r3_character(p, 5)
        char_results_5.append({'p': p, 'r3': len(pts), 'r3_chi5': r3c, 'M': int(M[p])})
        if p <= 30 or len(char_results_5) % 10 == 0:
            print(f"    p={p:4d}: r₃={len(pts):4d}, r₃(χ₅)={r3c:+6d}, M(p)={int(M[p]):+3d}")

    # ============================================================
    # PART E: The fundamental question — is there a NATURAL ΔW on S²?
    # ============================================================
    print(f"\n{'='*70}")
    print("[E] FUNDAMENTAL COMPARISON: S¹ vs S²")
    print()

    # On S¹, the Farey sequence F_N adds fractions a/q with q=N.
    # The "per-step" is adding all fractions with denominator exactly N.
    # On S², the analog is: at "level n", add all integer points on sphere of radius √n.
    # The per-step change uses PRIME levels only.

    # Compute the L2 discrepancy using ALL integers (not just primes)
    print("  Computing cumulative discrepancy at ALL integers (not just primes):")
    all_cum_pts = []
    all_disc_data = []
    prev_d = None

    for n in range(1, 201):
        pts = get_lattice_points(n)
        if len(pts) == 0:
            continue

        sqrt_n = np.sqrt(n)
        sphere_pts = [(a/sqrt_n, b/sqrt_n, c/sqrt_n) for (a, b, c) in pts]
        all_cum_pts.extend(sphere_pts)

        if len(all_cum_pts) >= 5 and n % 5 == 0:
            d = l2_cap_discrepancy_directed(all_cum_pts)
            delta = d - prev_d if prev_d is not None else 0
            is_p = n in primes
            all_disc_data.append({'n': n, 'disc': d, 'delta': delta,
                                  'is_prime': is_p, 'n_pts': len(all_cum_pts)})
            prev_d = d

    # At primes vs composites
    prime_deltas = [d['delta'] for d in all_disc_data if d['is_prime'] and d['n'] > 5]
    comp_deltas = [d['delta'] for d in all_disc_data if not d['is_prime'] and d['n'] > 5]

    if prime_deltas:
        print(f"  Mean ΔW at primes:     {np.mean(prime_deltas):+.6f}")
    if comp_deltas:
        print(f"  Mean ΔW at composites: {np.mean(comp_deltas):+.6f}")
    print(f"  (On S¹: primes ALWAYS decrease discrepancy)")

    # ============================================================
    # SAVE AND PLOT
    # ============================================================
    output = {
        'r3_weighted_Y20': r3_y20_data,
        'anisotropic_results': aniso_results,
        'orbit_discrepancy': disc_results,
        'character_results_mod3': char_results_3,
        'character_results_mod5': char_results_5,
    }

    outpath = os.path.expanduser('~/Desktop/Farey-Local/experiments/sphere_equidist_v2_results.json')
    with open(outpath, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    # Plotting
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Sphere Equidistribution v2: Breaking Symmetry', fontsize=14)

        # Plot 1: r₃(p, Y₂⁰) = 0 proof
        ax = axes[0, 0]
        ps = [d['p'] for d in r3_y20_data[:80]]
        y20s = [d['r3_Y20'] for d in r3_y20_data[:80]]
        ax.scatter(ps, y20s, s=15, c='blue')
        ax.axhline(y=0, color='red', lw=1)
        ax.set_xlabel('Prime p')
        ax.set_ylabel('r₃(p, Y₂⁰)')
        ax.set_title('r₃(p, Y₂⁰) = 0 (S₃ symmetry kills it)')

        # Plot 2: Anisotropic form
        ax = axes[0, 1]
        if aniso_results:
            ps_a = [d['p'] for d in aniso_results]
            ws = [d['w_Y20'] for d in aniso_results]
            colors_a = ['red' if d['w_Y20'] > 0 else 'blue' for d in aniso_results]
            ax.bar(ps_a, ws, color=colors_a, width=2)
            ax.set_xlabel('Prime p')
            ax.set_ylabel('r₃(p, Y₂⁰) [anisotropic]')
            ax.set_title('Anisotropic: a²+b²+2c²=p')

        # Plot 3: Character-twisted theta coefficients
        ax = axes[0, 2]
        if char_results_3:
            ps_c = [d['p'] for d in char_results_3]
            cs = [d['r3_chi3'] for d in char_results_3]
            ax.bar(ps_c, cs, color='green', width=2, alpha=0.7)
            ax.set_xlabel('Prime p')
            ax.set_ylabel('r₃(p, χ₃)')
            ax.set_title('Character-twisted: Σ χ₃(a)χ₃(b)χ₃(c)')

        # Plot 4: Orbit-representative discrepancy
        ax = axes[1, 0]
        if disc_results:
            ps_d = [d['p'] for d in disc_results[1:]]
            dws = [d['delta_w'] for d in disc_results[1:]]
            colors_d = ['red' if dw > 0 else 'blue' for dw in dws]
            ax.bar(ps_d, dws, color=colors_d, width=2, alpha=0.7)
            ax.axhline(y=0, color='black', lw=0.5)
            ax.set_xlabel('Prime p')
            ax.set_ylabel('ΔW (orbit reps)')
            ax.set_title('ΔW on S² (orbit representatives)')

        # Plot 5: ΔW_orbit vs M(p)
        ax = axes[1, 1]
        if disc_results:
            dws_arr = [d['delta_w'] for d in disc_results[1:]]
            mps = [d['M'] for d in disc_results[1:]]
            ax.scatter(mps, dws_arr, s=10, alpha=0.5, c='purple')
            ax.set_xlabel('M(p)')
            ax.set_ylabel('ΔW_orbit')
            ax.set_title('ΔW_orbit vs M(p)')
            ax.axhline(y=0, color='black', lw=0.5)
            ax.axvline(x=0, color='black', lw=0.5)

        # Plot 6: Cumulative discrepancy
        ax = axes[1, 2]
        if disc_results:
            ax.plot([d['p'] for d in disc_results], [d['disc'] for d in disc_results], 'b-', lw=0.8)
            ax.set_xlabel('Prime p')
            ax.set_ylabel('Cumulative discrepancy')
            ax.set_title('Cumulative discrepancy (orbit reps, S²)')

        plt.tight_layout()
        plotpath = os.path.expanduser('~/Desktop/Farey-Local/experiments/sphere_equidist_v2.png')
        plt.savefig(plotpath, dpi=150, bbox_inches='tight')
        print(f"\n  Plots saved to {plotpath}")

    except ImportError as e:
        print(f"  Matplotlib not available: {e}")

    print(f"\n  Results saved to {outpath}")
    print("\n" + "=" * 70)
    print("v2 COMPUTATION COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
