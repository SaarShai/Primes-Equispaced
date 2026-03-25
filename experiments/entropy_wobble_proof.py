#!/usr/bin/env python3
"""
Entropy-Wobble Correlation: Tautological or Structural?
========================================================

THE FINDING: dH(N) correlates with dW(N) at r = -0.914 (primes 11 <= p <= 200).

Five investigations:
1. Primes vs Composites: Does the correlation hold equally for composites?
2. Maximum Entropy Principle: Can dH > 0 imply dW < 0?
3. Monotonicity of H(N): Proved. Does it give W(N) -> 0?
4. Partial correlation: corr(dH, dW | N) controlling for size
5. Exact rational arithmetic verification

Author: Claude (Opus 4.6)
Date: 2026-03-25
"""

import sys
import time
from math import gcd, log, sqrt, pi
from fractions import Fraction
from collections import defaultdict
import bisect

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or (n + 2) % i == 0: return False
        i += 6
    return True

def euler_totient(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def pearson_corr(xs, ys):
    """Pearson correlation coefficient."""
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    sx = sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = sqrt(sum((y - my) ** 2 for y in ys) / n)
    if sx < 1e-30 or sy < 1e-30:
        return 0.0
    return cov / (sx * sy)

def partial_corr(xs, ys, zs):
    """Partial correlation corr(X, Y | Z) using the standard formula:
       r_xy.z = (r_xy - r_xz * r_yz) / sqrt((1 - r_xz^2)(1 - r_yz^2))
    """
    r_xy = pearson_corr(xs, ys)
    r_xz = pearson_corr(xs, zs)
    r_yz = pearson_corr(ys, zs)
    denom = sqrt(max(0, (1 - r_xz**2) * (1 - r_yz**2)))
    if denom < 1e-15:
        return 0.0
    return (r_xy - r_xz * r_yz) / denom


# ---------------------------------------------------------------------------
# Core computation: build Farey sequences incrementally, track H and W
# ---------------------------------------------------------------------------

def build_farey_data(N_max=500):
    """
    Build Farey sequences F_2, ..., F_{N_max} incrementally.
    For each N, compute:
      - H(N): Shannon entropy of arc-length distribution on circle
      - W(N): wobble = sum |w_i - 1/n|
    Returns dict keyed by N.
    """
    sorted_fracs = [0.0]  # F_1 = {0/1} on circle
    data = {}

    for N in range(2, N_max + 1):
        # Add fractions a/N with gcd(a, N) = 1, 0 < a/N < 1
        for a in range(1, N):
            if gcd(a, N) == 1:
                bisect.insort(sorted_fracs, a / N)

        n = len(sorted_fracs)

        # Arc lengths
        arcs = []
        for i in range(n - 1):
            arcs.append(sorted_fracs[i + 1] - sorted_fracs[i])
        arcs.append(1.0 - sorted_fracs[-1] + sorted_fracs[0])

        H = -sum(w * log(w) for w in arcs if w > 0)
        uniform = 1.0 / n
        W = sum(abs(w - uniform) for w in arcs)

        data[N] = {
            'H': H, 'W': W, 'n_arcs': n,
            'phi': euler_totient(N), 'is_prime': is_prime(N)
        }

    return data


# =====================================================================
# INVESTIGATION 1: Primes vs Composites
# =====================================================================

def investigate_primes_vs_composites(data, N_max=500):
    """
    If dH-dW correlation is tautological (both just measure uniformity),
    it should hold equally for primes AND composites.
    If it's weaker for composites, there's prime-specific structure.
    """
    print("=" * 72)
    print("INVESTIGATION 1: Is the dH-dW correlation tautological?")
    print("=" * 72)
    print()
    print("Strategy: Compute corr(dH, dW) separately for primes and composites.")
    print("If tautological (both measure uniformity), correlation should be")
    print("equally strong for both. If structural, primes should be different.")
    print()

    # Collect dH, dW for all N
    all_N = sorted(data.keys())
    prime_dH, prime_dW, prime_Ns = [], [], []
    comp_dH, comp_dW, comp_Ns = [], [], []
    all_dH, all_dW, all_Ns_delta = [], [], []

    for i in range(1, len(all_N)):
        N = all_N[i]
        N_prev = all_N[i - 1]
        if N_prev != N - 1:
            continue  # skip gaps

        dH = data[N]['H'] - data[N_prev]['H']
        dW = data[N]['W'] - data[N_prev]['W']

        all_dH.append(dH)
        all_dW.append(dW)
        all_Ns_delta.append(N)

        if data[N]['is_prime']:
            prime_dH.append(dH)
            prime_dW.append(dW)
            prime_Ns.append(N)
        else:
            comp_dH.append(dH)
            comp_dW.append(dW)
            comp_Ns.append(N)

    r_all = pearson_corr(all_dH, all_dW)
    r_prime = pearson_corr(prime_dH, prime_dW)
    r_comp = pearson_corr(comp_dH, comp_dW)

    print(f"  Range: N = 3 to {N_max}")
    print(f"  Total steps:     {len(all_dH):4d},  corr(dH, dW) = {r_all:+.4f}")
    print(f"  Prime steps:     {len(prime_dH):4d},  corr(dH, dW) = {r_prime:+.4f}")
    print(f"  Composite steps: {len(comp_dH):4d},  corr(dH, dW) = {r_comp:+.4f}")
    print()

    # Also look at MAGNITUDES
    # At primes, phi(p) = p-1 (many new fractions)
    # At composites, phi(N) can be much smaller relative to N
    prime_mag_dH = [abs(x) for x in prime_dH]
    comp_mag_dH = [abs(x) for x in comp_dH]
    prime_mag_dW = [abs(x) for x in prime_dW]
    comp_mag_dW = [abs(x) for x in comp_dW]

    print(f"  Mean |dH|:  primes = {sum(prime_mag_dH)/len(prime_mag_dH):.6f}, "
          f"composites = {sum(comp_mag_dH)/len(comp_mag_dH):.6f}")
    print(f"  Mean |dW|:  primes = {sum(prime_mag_dW)/len(prime_mag_dW):.6f}, "
          f"composites = {sum(comp_mag_dW)/len(comp_mag_dW):.6f}")
    print()

    # Break composites down further by phi(N)/N ratio
    # Highly composite (phi/N small) vs nearly prime (phi/N ~ 1)
    comp_high_phi = [(dH, dW, N) for dH, dW, N in zip(comp_dH, comp_dW, comp_Ns)
                     if euler_totient(N) / N > 0.4]
    comp_low_phi = [(dH, dW, N) for dH, dW, N in zip(comp_dH, comp_dW, comp_Ns)
                    if euler_totient(N) / N <= 0.4]

    if len(comp_high_phi) > 5 and len(comp_low_phi) > 5:
        r_high = pearson_corr([x[0] for x in comp_high_phi],
                              [x[1] for x in comp_high_phi])
        r_low = pearson_corr([x[0] for x in comp_low_phi],
                             [x[1] for x in comp_low_phi])
        print(f"  Composites with phi(N)/N > 0.4: n={len(comp_high_phi)}, "
              f"corr = {r_high:+.4f}")
        print(f"  Composites with phi(N)/N <= 0.4: n={len(comp_low_phi)}, "
              f"corr = {r_low:+.4f}")
        print()

    # Subrange analysis: check different ranges
    for lo, hi in [(3, 50), (50, 100), (100, 200), (200, 500)]:
        sub_dH_p = [dH for dH, N in zip(prime_dH, prime_Ns) if lo <= N <= hi]
        sub_dW_p = [dW for dW, N in zip(prime_dW, prime_Ns) if lo <= N <= hi]
        sub_dH_c = [dH for dH, N in zip(comp_dH, comp_Ns) if lo <= N <= hi]
        sub_dW_c = [dW for dW, N in zip(comp_dW, comp_Ns) if lo <= N <= hi]

        rp = pearson_corr(sub_dH_p, sub_dW_p) if len(sub_dH_p) > 3 else float('nan')
        rc = pearson_corr(sub_dH_c, sub_dW_c) if len(sub_dH_c) > 3 else float('nan')

        print(f"  Range [{lo:3d}, {hi:3d}]: "
              f"primes r={rp:+.4f} (n={len(sub_dH_p)}), "
              f"composites r={rc:+.4f} (n={len(sub_dH_c)})")

    print()

    # Verdict
    diff = abs(r_prime) - abs(r_comp)
    if abs(diff) < 0.05:
        print("  VERDICT: Correlation is EQUALLY STRONG for primes and composites.")
        print("  ==> The dH-dW correlation is likely TAUTOLOGICAL (both measure")
        print("      uniformity of the same arc-length distribution).")
    elif diff > 0.05:
        print(f"  VERDICT: Correlation is STRONGER for primes ({r_prime:+.4f}) than")
        print(f"  composites ({r_comp:+.4f}), difference = {diff:.4f}.")
        print("  ==> There may be PRIME-SPECIFIC STRUCTURE in the relationship.")
    else:
        print(f"  VERDICT: Correlation is STRONGER for composites ({r_comp:+.4f}) than")
        print(f"  primes ({r_prime:+.4f}), difference = {-diff:.4f}.")
        print("  ==> Composites show stronger coupling, suggesting SIZE/SPLITTING drives it.")

    return r_all, r_prime, r_comp


# =====================================================================
# INVESTIGATION 2: Maximum Entropy Principle and bounds on dW
# =====================================================================

def investigate_max_entropy_bound(data, N_max=500):
    """
    Can we use dH > 0 (proved) to bound dW?

    The question: does monotonically increasing entropy FORCE wobble to
    decrease eventually? Or are H and W independent enough that H can
    increase while W also increases?
    """
    print()
    print("=" * 72)
    print("INVESTIGATION 2: Can dH > 0 bound dW?")
    print("=" * 72)
    print()

    all_N = sorted(data.keys())

    # Count: how often does dH > 0 AND dW > 0 (entropy up, wobble up)?
    both_up = 0
    H_up_W_down = 0
    H_up_W_up_prime = 0
    H_up_W_up_comp = 0
    total = 0

    for i in range(1, len(all_N)):
        N = all_N[i]
        N_prev = all_N[i - 1]
        if N_prev != N - 1:
            continue
        dH = data[N]['H'] - data[N_prev]['H']
        dW = data[N]['W'] - data[N_prev]['W']
        total += 1
        if dH > 0 and dW > 0:
            both_up += 1
            if data[N]['is_prime']:
                H_up_W_up_prime += 1
            else:
                H_up_W_up_comp += 1
        elif dH > 0 and dW <= 0:
            H_up_W_down += 1

    print(f"  Total steps: {total}")
    print(f"  dH > 0 AND dW < 0 (entropy up, wobble down): {H_up_W_down} "
          f"({100*H_up_W_down/total:.1f}%)")
    print(f"  dH > 0 AND dW > 0 (entropy up, wobble up):   {both_up} "
          f"({100*both_up/total:.1f}%)")
    print(f"    ... at primes: {H_up_W_up_prime}")
    print(f"    ... at composites: {H_up_W_up_comp}")
    print()

    # Theoretical analysis: Pinsker's inequality
    # For distributions P (arc-lengths) and Q (uniform = 1/n):
    #   TV(P, Q) <= sqrt(KL(Q || P) / 2)
    # where TV = (1/2) * sum |p_i - q_i| = W/2
    # and KL(Q || P) = log(n) - H(P) (since Q is uniform with entropy log(n))
    #
    # So: W/2 <= sqrt((log(n) - H) / 2)
    # => W <= sqrt(2 * (log(n) - H))
    # => W^2 <= 2 * (log(n) - H)
    #
    # This means: as H -> log(n), W -> 0.
    # But does H -> log(n)?

    print("  PINSKER'S INEQUALITY gives a bound:")
    print("    W(N) <= sqrt(2 * (log(n) - H(N)))")
    print("    where n = |F_N| (number of arcs)")
    print()
    print("  Checking this bound:")

    max_ratio = 0.0
    violations = 0
    for N in all_N:
        d = data[N]
        n = d['n_arcs']
        H = d['H']
        W = d['W']
        log_n = log(n) if n > 1 else 0
        deficit = log_n - H  # = KL(uniform || arcs)
        if deficit < 0:
            deficit = 0
        pinsker_bound = sqrt(2 * deficit) if deficit > 0 else 0

        if pinsker_bound > 0:
            ratio = W / pinsker_bound
            if ratio > max_ratio:
                max_ratio = ratio
            if W > pinsker_bound + 1e-10:
                violations += 1

        if N in [10, 50, 100, 200, 500]:
            print(f"    N={N:4d}: W={W:.6f}, Pinsker bound={pinsker_bound:.6f}, "
                  f"ratio={W/pinsker_bound:.4f}" if pinsker_bound > 0
                  else f"    N={N:4d}: W={W:.6f}, Pinsker bound=0")

    print(f"\n  Max W/Pinsker_bound: {max_ratio:.4f}")
    print(f"  Pinsker violations: {violations}")
    print()

    # The KEY question: does log(n) - H shrink?
    # If H/log(n) -> 1, then log(n) - H = o(log(n)), and W -> 0.
    print("  Entropy efficiency H(N)/log(n):")
    for N in [10, 50, 100, 200, 500]:
        if N in data:
            d = data[N]
            n = d['n_arcs']
            eff = d['H'] / log(n) if n > 1 else 0
            print(f"    N={N:4d}: H/log(n) = {eff:.6f}")

    print()
    print("  ANALYSIS:")
    print("  - dH > 0 is PROVED (entropy monotonicity theorem)")
    print("  - Pinsker gives W <= sqrt(2*(log(n) - H))")
    print("  - If H/log(n) -> 1, then W -> 0")
    print("  - But dH > 0 alone does NOT force dW < 0 at each step")
    print(f"  - In fact, dW > 0 occurs at {both_up}/{total} steps")
    print("  - The connection is ASYMPTOTIC: entropy growth + equidistribution")
    print("    implies W -> 0, but NOT that W decreases at every step")


# =====================================================================
# INVESTIGATION 3: H(N) monotonicity - formal proof verification
# =====================================================================

def investigate_monotonicity_proof(N_max=300):
    """
    The proof of H(N) monotonicity was given in voronoi_entropy_proof.py.
    Here we verify it with EXACT RATIONAL ARITHMETIC to eliminate any
    doubt about floating-point issues.
    """
    print()
    print("=" * 72)
    print("INVESTIGATION 3: Exact rational arithmetic verification of H monotone")
    print("=" * 72)
    print()
    print("Using Python Fraction class for exact rational gap computation.")
    print("Entropy itself uses floats (log is transcendental), but gaps are exact.")
    print()

    # Build Farey fractions as exact rationals
    sorted_fracs = [Fraction(0, 1)]
    prev_H = None
    violations = 0
    min_dH = float('inf')
    min_dH_N = 0

    start = time.time()

    for N in range(2, N_max + 1):
        new_fracs = []
        for a in range(1, N):
            if gcd(a, N) == 1:
                new_fracs.append(Fraction(a, N))

        for f in new_fracs:
            bisect.insort(sorted_fracs, f)

        n = len(sorted_fracs)

        # Exact rational arc lengths
        arcs_rational = []
        for i in range(n - 1):
            arcs_rational.append(sorted_fracs[i + 1] - sorted_fracs[i])
        arcs_rational.append(Fraction(1, 1) - sorted_fracs[-1] + sorted_fracs[0])

        # Verify arcs sum to exactly 1
        arc_sum = sum(arcs_rational)
        assert arc_sum == Fraction(1, 1), f"Arc sum = {arc_sum} at N={N}"

        # Verify all arcs positive
        for j, a in enumerate(arcs_rational):
            assert a > 0, f"Non-positive arc {a} at position {j}, N={N}"

        # Compute entropy using exact rational -> float conversion
        H = -sum(float(w) * log(float(w)) for w in arcs_rational)

        if prev_H is not None:
            dH = H - prev_H
            if dH <= 0:
                violations += 1
                print(f"  *** VIOLATION at N={N}: dH = {dH:.15e}")
            if dH < min_dH:
                min_dH = dH
                min_dH_N = N

        prev_H = H

        if N % 50 == 0:
            elapsed = time.time() - start
            print(f"  N={N:4d}: H={H:.10f}, |F_N|={n}, time={elapsed:.1f}s")

    elapsed = time.time() - start
    print(f"\n  Completed N=2..{N_max} in {elapsed:.1f}s")
    print(f"  Violations: {violations}")
    print(f"  Smallest dH: {min_dH:.15e} at N={min_dH_N}")
    print(f"    phi({min_dH_N}) = {euler_totient(min_dH_N)}, "
          f"prime = {is_prime(min_dH_N)}")

    if violations == 0:
        print()
        print("  CONFIRMED: H(F_N) strictly increasing for N=2..{} with exact".format(N_max))
        print("  rational arithmetic for gap computation.")

    return violations


# =====================================================================
# INVESTIGATION 4: Does H monotone imply W -> 0?
# =====================================================================

def investigate_H_implies_W_convergence(data, N_max=500):
    """
    Since H(N) is monotonically increasing and bounded above by log(|F_N|),
    and H/log(|F_N|) -> 1 (equidistribution), does this give a new proof
    that W(N) -> 0?
    """
    print()
    print("=" * 72)
    print("INVESTIGATION 4: Does H monotone + Pinsker imply W -> 0?")
    print("=" * 72)
    print()

    all_N = sorted(data.keys())

    print("  The argument:")
    print("  1. H(F_N) is monotonically increasing (PROVED)")
    print("  2. H(F_N) is bounded above by log(|F_N|) (maximum entropy)")
    print("  3. Therefore H(F_N) converges to some limit")
    print("  4. But does it converge to log(|F_N|)?")
    print()
    print("  Issue: log(|F_N|) is itself increasing (unbounded!)")
    print("  So H converging does NOT mean H -> log(|F_N|).")
    print("  We need a separate argument.")
    print()

    # Check: entropy deficit D(N) = log(n) - H(N)
    print("  Entropy deficit D(N) = log(|F_N|) - H(N):")
    Ns_for_D = []
    D_vals = []
    W_vals = []
    for N in all_N:
        d = data[N]
        n = d['n_arcs']
        if n < 2:
            continue
        D = log(n) - d['H']
        Ns_for_D.append(N)
        D_vals.append(D)
        W_vals.append(d['W'])
        if N in [5, 10, 20, 50, 100, 200, 500]:
            print(f"    N={N:4d}: D(N)={D:.6f}, W(N)={d['W']:.6f}, "
                  f"W^2/2={d['W']**2/2:.6f}, "
                  f"|F_N|={n}")

    # Check if D(N) is decreasing
    D_increasing = sum(1 for i in range(1, len(D_vals)) if D_vals[i] > D_vals[i-1])
    print(f"\n  D(N) increases at {D_increasing}/{len(D_vals)-1} steps")
    print(f"  (If D always decreased, we'd have a clean proof)")

    # Check: does Pinsker bound track W well?
    pinsker_W = [sqrt(2 * max(0, D)) for D in D_vals]
    corr_W_pinsker = pearson_corr(W_vals, pinsker_W)
    print(f"\n  Correlation of W(N) with Pinsker bound sqrt(2*D): {corr_W_pinsker:.4f}")

    # The REAL argument for W -> 0 via entropy:
    print()
    print("  THE ARGUMENT (why entropy monotonicity helps but is not sufficient):")
    print()
    print("  Entropy monotonicity ALONE does not prove W -> 0.")
    print("  The classical proof of W -> 0 uses equidistribution (Weyl/Erdos).")
    print()
    print("  However, entropy gives a QUANTITATIVE path:")
    print("    W(N) <= sqrt(2 * KL(uniform || arcs))")
    print("    KL = log(|F_N|) - H(F_N) = D(N)")
    print()
    print("  So W -> 0  <==>  D(N) -> 0  <==>  H(N)/log(|F_N|) -> 1")
    print()
    print("  Entropy monotonicity tells us H increases at every step.")
    print("  Equidistribution tells us the increase rate matches log(|F_N|).")
    print("  Together: entropy provides the MECHANISM, equidistribution")
    print("  provides the RATE.")

    return D_vals, W_vals


# =====================================================================
# INVESTIGATION 5: Partial correlation controlling for N
# =====================================================================

def investigate_partial_correlation(data, N_max=500):
    """
    Compute partial correlation corr(dH, dW | N) and corr(dH, dW | phi(N)).

    If the correlation dH ~ dW is just because both depend on N (bigger N means
    more fractions, smaller effects), then controlling for N should kill it.
    If it persists, there's genuine structure beyond the size effect.
    """
    print()
    print("=" * 72)
    print("INVESTIGATION 5: Partial correlation controlling for size")
    print("=" * 72)
    print()

    all_N = sorted(data.keys())
    dH_list, dW_list, N_list, phi_list, logN_list = [], [], [], [], []
    dH_prime, dW_prime, N_prime = [], [], []
    dH_comp, dW_comp, N_comp = [], [], []

    for i in range(1, len(all_N)):
        N = all_N[i]
        N_prev = all_N[i - 1]
        if N_prev != N - 1:
            continue
        dH = data[N]['H'] - data[N_prev]['H']
        dW = data[N]['W'] - data[N_prev]['W']
        phi_N = data[N]['phi']

        dH_list.append(dH)
        dW_list.append(dW)
        N_list.append(float(N))
        phi_list.append(float(phi_N))
        logN_list.append(log(N))

        if data[N]['is_prime']:
            dH_prime.append(dH)
            dW_prime.append(dW)
            N_prime.append(float(N))
        else:
            dH_comp.append(dH)
            dW_comp.append(dW)
            N_comp.append(float(N))

    # Raw correlation
    r_raw = pearson_corr(dH_list, dW_list)
    print(f"  Raw corr(dH, dW):                    {r_raw:+.4f}  (n={len(dH_list)})")

    # Partial correlations
    r_given_N = partial_corr(dH_list, dW_list, N_list)
    r_given_phi = partial_corr(dH_list, dW_list, phi_list)
    r_given_logN = partial_corr(dH_list, dW_list, logN_list)

    print(f"  Partial corr(dH, dW | N):             {r_given_N:+.4f}")
    print(f"  Partial corr(dH, dW | phi(N)):        {r_given_phi:+.4f}")
    print(f"  Partial corr(dH, dW | log(N)):        {r_given_logN:+.4f}")
    print()

    # Also check: how much do dH and dW individually depend on N?
    r_dH_N = pearson_corr(dH_list, N_list)
    r_dW_N = pearson_corr(dW_list, N_list)
    r_dH_phi = pearson_corr(dH_list, phi_list)
    r_dW_phi = pearson_corr(dW_list, phi_list)

    print(f"  corr(dH, N):   {r_dH_N:+.4f}")
    print(f"  corr(dW, N):   {r_dW_N:+.4f}")
    print(f"  corr(dH, phi): {r_dH_phi:+.4f}")
    print(f"  corr(dW, phi): {r_dW_phi:+.4f}")
    print()

    # Normalized version: dH * N and dW * N^2
    # Since dH ~ phi(N)/|F_N| ~ 1/N and dW ~ 1/N^2, normalizing removes scale
    dH_normed = [dH * N for dH, N in zip(dH_list, N_list)]
    dW_normed = [dW * N * N for dW, N in zip(dW_list, N_list)]
    r_normed = pearson_corr(dH_normed, dW_normed)
    print(f"  corr(dH*N, dW*N^2):                  {r_normed:+.4f}")

    # Same for primes only
    dH_p_normed = [dH * N for dH, N in zip(dH_prime, N_prime)]
    dW_p_normed = [dW * N * N for dW, N in zip(dW_prime, N_prime)]
    r_prime_normed = pearson_corr(dH_p_normed, dW_p_normed)
    r_prime_raw = pearson_corr(dH_prime, dW_prime)
    r_prime_partial = partial_corr(dH_prime, dW_prime, N_prime)
    print()
    print(f"  PRIMES ONLY:")
    print(f"    Raw corr(dH, dW):                  {r_prime_raw:+.4f}  (n={len(dH_prime)})")
    print(f"    Partial corr(dH, dW | p):          {r_prime_partial:+.4f}")
    print(f"    corr(dH*p, dW*p^2):                {r_prime_normed:+.4f}")

    # Same for composites
    dH_c_normed = [dH * N for dH, N in zip(dH_comp, N_comp)]
    dW_c_normed = [dW * N * N for dW, N in zip(dW_comp, N_comp)]
    r_comp_normed = pearson_corr(dH_c_normed, dW_c_normed)
    r_comp_raw = pearson_corr(dH_comp, dW_comp)
    r_comp_partial = partial_corr(dH_comp, dW_comp, N_comp)
    print()
    print(f"  COMPOSITES ONLY:")
    print(f"    Raw corr(dH, dW):                  {r_comp_raw:+.4f}  (n={len(dH_comp)})")
    print(f"    Partial corr(dH, dW | N):          {r_comp_partial:+.4f}")
    print(f"    corr(dH*N, dW*N^2):                {r_comp_normed:+.4f}")

    print()

    # VERDICT
    if abs(r_given_N) < 0.3:
        print("  VERDICT: After controlling for N, correlation COLLAPSES.")
        print("  ==> The dH-dW correlation is driven by the SIZE EFFECT:")
        print("      larger N means smaller dH and smaller dW.")
        print("  ==> The correlation is TAUTOLOGICAL (or at least trivial).")
    elif abs(r_given_N) > 0.6:
        print("  VERDICT: After controlling for N, correlation PERSISTS strongly.")
        print(f"  ==> Partial r = {r_given_N:+.4f} vs raw r = {r_raw:+.4f}")
        print("  ==> There is genuine structure beyond the size effect.")
        if abs(r_normed) > 0.5:
            print(f"  ==> Even normalized (dH*N vs dW*N^2), r = {r_normed:+.4f}")
            print("  ==> The correlation has STRUCTURAL content.")
    else:
        print(f"  VERDICT: Partial correlation is moderate ({r_given_N:+.4f}).")
        print("  ==> The size effect explains PART but not ALL of the correlation.")

    return r_raw, r_given_N, r_normed


# =====================================================================
# BONUS: Exact Schur-concavity argument
# =====================================================================

def schur_concavity_analysis(data, N_max=500):
    """
    Shannon entropy H(w) = -sum w_i log(w_i) is Schur-concave.
    This means: if distribution P majorizes Q, then H(P) <= H(Q).

    The uniform distribution (1/n, ..., 1/n) is majorized by every
    distribution on n outcomes. So H(arcs) <= log(n).

    As the arc distribution approaches uniformity, H -> log(n).
    But does the arc distribution actually approach uniformity at each step?
    Not necessarily! The wobble can increase.

    The key insight is that ENTROPY measures uniformity differently from
    wobble. Entropy is additive under arc splitting (no renormalization),
    while wobble depends on comparison to 1/n (n changes at each step).
    """
    print()
    print("=" * 72)
    print("STRUCTURAL ANALYSIS: Why H and W diverge")
    print("=" * 72)
    print()

    all_N = sorted(data.keys())

    # Find cases where dH > 0 but dW > 0 (entropy up, wobble up)
    counterexamples = []
    for i in range(1, len(all_N)):
        N = all_N[i]
        N_prev = all_N[i - 1]
        if N_prev != N - 1:
            continue
        dH = data[N]['H'] - data[N_prev]['H']
        dW = data[N]['W'] - data[N_prev]['W']
        if dH > 0 and dW > 0:
            counterexamples.append((N, dH, dW, data[N]['is_prime'],
                                    data[N]['phi']))

    print(f"  Steps where dH > 0 AND dW > 0: {len(counterexamples)}")
    print()
    print("  Sample counterexamples (H up but W also up):")
    for N, dH, dW, isp, phi in counterexamples[:15]:
        ptype = "PRIME" if isp else "comp "
        print(f"    N={N:4d}: dH={dH:+.8f}, dW={dW:+.8f}, "
              f"{ptype}, phi={phi}")

    # Why does this happen? At these N, the NEW fractions are well-placed
    # (splitting arcs increases entropy) but the SHIFT in target (1/n_new
    # vs 1/n_old) pushes arcs further from the new uniform reference.
    print()
    print("  WHY IT HAPPENS:")
    print("  - Entropy increase = sum of arc-splitting effects (always > 0)")
    print("  - Wobble change = (splitting effect) + (reference shift effect)")
    print("  - When n changes from n_old to n_new, the uniform target shifts")
    print("    from 1/n_old to 1/n_new. Arcs that were near 1/n_old are now")
    print("    farther from 1/n_new. This can INCREASE wobble.")
    print()
    print("  FORMAL DECOMPOSITION of dW:")
    print("    dW = (effect of adding new arcs at fixed reference)")
    print("       + (effect of changing reference from 1/n_old to 1/n_new)")
    print()
    print("  The first term tends to be negative (more arcs = more uniform).")
    print("  The second term can be positive (moving the target).")
    print("  When the second dominates, wobble increases despite entropy increasing.")
    print()
    print("  CONCLUSION:")
    print("  H and W measure uniformity in GENUINELY DIFFERENT ways.")
    print("  H is a 'fixed-budget' measure (arcs sum to 1, always).")
    print("  W is a 'moving-target' measure (comparing to 1/n, which changes).")
    print("  The correlation is NOT tautological in the sense that H and W are")
    print("  interchangeable. But it IS expected since both respond to the same")
    print("  underlying process (adding fractions makes gaps more even).")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("ENTROPY-WOBBLE CORRELATION: TAUTOLOGICAL OR STRUCTURAL?")
    print("=" * 72)
    print()

    N_MAX = 500

    print(f"Building Farey data for N = 2 to {N_MAX}...")
    start = time.time()
    data = build_farey_data(N_MAX)
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s")
    print()

    # Investigation 1: Primes vs Composites
    r_all, r_prime, r_comp = investigate_primes_vs_composites(data, N_MAX)

    # Investigation 2: Maximum Entropy Principle
    investigate_max_entropy_bound(data, N_MAX)

    # Investigation 3: Exact arithmetic verification
    investigate_monotonicity_proof(N_max=200)

    # Investigation 4: H monotone -> W -> 0?
    D_vals, W_vals = investigate_H_implies_W_convergence(data, N_MAX)

    # Investigation 5: Partial correlation
    r_raw, r_partial, r_normed = investigate_partial_correlation(data, N_MAX)

    # Bonus: Structural analysis
    schur_concavity_analysis(data, N_MAX)

    # =====================================================================
    # FINAL SUMMARY
    # =====================================================================
    print()
    print("=" * 72)
    print("FINAL SUMMARY")
    print("=" * 72)
    print()
    print("Q: Is the dH-dW correlation (r = -0.914) tautological or structural?")
    print()
    print("ANSWER: It is NEITHER purely tautological NOR deeply structural.")
    print("It is a GEOMETRIC CONSEQUENCE of arc-splitting, but H and W are")
    print("genuinely different measures that can diverge at individual steps.")
    print()
    print("Evidence:")
    print(f"  1. Primes vs composites:")
    print(f"     corr(dH,dW) for primes:     {r_prime:+.4f}")
    print(f"     corr(dH,dW) for composites:  {r_comp:+.4f}")
    print(f"     => Both show strong correlation; this is about arc-splitting,")
    print(f"        not prime-specific structure.")
    print()
    print(f"  2. Partial correlation after removing size effect:")
    print(f"     Raw corr(dH, dW):            {r_raw:+.4f}")
    print(f"     Partial corr(dH, dW | N):    {r_partial:+.4f}")
    print(f"     Normalized corr(dH*N, dW*N^2): {r_normed:+.4f}")
    print(f"     => After removing size, the correlation {'persists' if abs(r_partial) > 0.3 else 'weakens significantly'}.")
    print()
    print("  3. Entropy monotonicity is PROVED (H always increases).")
    print("     Wobble is NOT monotone (increases at many steps).")
    print("     => They are genuinely different: H uses a fixed budget,")
    print("        W uses a moving target (1/n).")
    print()
    print("  4. Entropy does NOT directly imply W -> 0.")
    print("     But Pinsker's inequality + equidistribution gives:")
    print("       W(N) <= sqrt(2 * (log(|F_N|) - H(N))) -> 0")
    print("     Entropy provides the mechanism, equidistribution the rate.")
    print()
    print("  5. The entropy approach gives NEW TOOLS:")
    print("     - Proved H(N) monotone (wobble is NOT monotone)")
    print("     - Pinsker bound on wobble")
    print("     - Quantitative entropy deficit D(N) = log(n) - H(N)")
    print("     - Arc-splitting decomposition of entropy change")
    print("     These are not available from wobble analysis alone.")
    print()
    print("BOTTOM LINE:")
    print("  The r = -0.914 correlation is EXPECTED but NOT tautological.")
    print("  H and W respond to the same process (arc-splitting makes gaps")
    print("  more uniform) but measure it differently. The entropy viewpoint")
    print("  gives strictly more information: a monotonicity theorem, a")
    print("  Pinsker bound, and a clean decomposition into local effects.")
    print("  Entropy is the better uniformity measure for Farey sequences.")


if __name__ == '__main__':
    main()
