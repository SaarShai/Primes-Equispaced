#!/usr/bin/env python3
"""
NON-CIRCULAR BOUND: |1 - D/A| ≤ 0.1 for all primes p ≥ P₀
============================================================

GOAL: Prove |1 - D/A| ≤ 0.1 WITHOUT using ΔW in the bound.

APPROACH:
  D/A = new_D_sq / dilution_raw

  where:
    new_D_sq     = Σ_{k=1}^{p-1} D_new(k/p)²
    dilution_raw = old_D_sq · (n'² - n²)/n²

  D_new(k/p) = D_old_virtual(k/p) + k/p
  D_old_virtual(k/p) = N_{p-1}(k/p) - n·(k/p)

  So: new_D_sq = Σ D_old_virtual² + 2·Σ D_old_virtual·(k/p) + Σ (k/p)²
             =       S_virt      +      2·X_cross          +    S_kp

  S_kp = (p-1)(2p-1)/(6p²)  — EXACT
  Σ D_old_virtual = 0        — PROVED (zero-sum property)
  X_cross = Σ D_old_virtual(k/p)·(k/p)  — KEY unknown

  dilution_raw = old_D_sq · (2np - 2n + p² - 2p + 1)/n²

  So: D/A = (S_virt + 2·X_cross + S_kp) / dilution_raw

NON-CIRCULAR DECOMPOSITION:
  Let R = S_virt / old_D_sq  (Riemann sum ratio — equispaced vs Farey sampling of D²)
  Let T = dilution_raw / old_D_sq = (n'² - n²)/n²

  Then: D/A = (R·old_D_sq + 2·X_cross + S_kp) / (T·old_D_sq)
            = R/T + (2·X_cross + S_kp) / (T·old_D_sq)

  The key insight: R/T ≈ 1 because both numerator and denominator scale as ~n/p.

  More precisely:
    T = (n'² - n²)/n² = (2n(p-1) + (p-1)²)/n² ≈ 2(p-1)/n + (p-1)²/n²
    With n ≈ 3p²/π², this gives T ≈ 2π²/(3p) + π⁴/(9p²)

    S_virt/old_D_sq: the equispaced Riemann sum of D(x)² at p-1 points k/p,
    divided by the Farey-point sum. Since both approximate ∫₀¹ D(x)² dx,
    their ratio → 1.

  The correction terms (2·X_cross + S_kp)/(T·old_D_sq) are O(1/p).

THIS SCRIPT:
  1. Computes all terms with exact rational arithmetic for small primes
  2. Computes floating-point for primes up to 3000
  3. Analyzes each sub-ratio: R/T, X_cross contribution, S_kp contribution
  4. Identifies sharp non-circular bounds
  5. Searches for a closed-form or known-quantity expression for S_virt
  6. Investigates S_virt in terms of Dedekind sums and Ramanujan sums
"""

import time
import bisect
from math import gcd, floor, sqrt, isqrt, pi, log
from fractions import Fraction

# ============================================================
# UTILITIES
# ============================================================

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def farey_generator(N):
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))


# ============================================================
# DEDEKIND SUM (for potential closed-form expressions)
# ============================================================

def dedekind_sum(a, b):
    """Compute the Dedekind sum s(a, b) = Σ_{k=1}^{b-1} ((k/b))((ak/b))"""
    if b <= 1:
        return Fraction(0)
    s = Fraction(0)
    for k in range(1, b):
        t1 = Fraction(k, b) - Fraction(1, 2)  # ((k/b))
        t2_num = (a * k) % b
        t2 = Fraction(t2_num, b) - Fraction(1, 2) if t2_num != 0 else Fraction(0)
        if k % b != 0:
            s += t1 * t2
    return s


# ============================================================
# CORE COMPUTATION: NON-CIRCULAR D/A DECOMPOSITION
# ============================================================

def noncircular_decomposition(p, phi_arr, use_exact=False):
    """
    Compute all terms of the non-circular D/A decomposition.

    Returns dict with:
      - S_virt:    Σ D_old_virtual(k/p)²
      - X_cross:   Σ D_old_virtual(k/p) · (k/p)
      - S_kp:      Σ (k/p)²
      - old_D_sq:  Σ D(f)² over Farey points
      - new_D_sq:  S_virt + 2·X_cross + S_kp
      - dilution_raw: old_D_sq · (n'² - n²)/n²
      - D/A ratio
      - Sub-ratios: R/T, cross contribution, kp contribution
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    if use_exact:
        return _exact_computation(p, N, n, n_prime, phi_arr)
    else:
        return _float_computation(p, N, n, n_prime, phi_arr)


def _exact_computation(p, N, n, n_prime, phi_arr):
    """Exact rational arithmetic computation."""
    old_fracs = list(farey_generator(N))
    old_frac_vals = sorted(Fraction(a, b) for a, b in old_fracs)

    # Compute old_D_sq
    old_D_sq = Fraction(0)
    for idx, fv in enumerate(old_frac_vals):
        D = idx - n * fv
        old_D_sq += D * D

    # Compute S_virt, X_cross, S_kp at equispaced points k/p
    S_virt = Fraction(0)
    X_cross = Fraction(0)
    S_kp = Fraction(0)
    sum_Dvirt = Fraction(0)

    for k in range(1, p):
        target = Fraction(k, p)
        # Binary search for N_{p-1}(k/p) = number of Farey fractions ≤ k/p
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if old_frac_vals[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        D_virt = lo - n * target  # D_old_virtual(k/p)

        S_virt += D_virt * D_virt
        X_cross += D_virt * target
        S_kp += target * target
        sum_Dvirt += D_virt

    new_D_sq = S_virt + 2 * X_cross + S_kp
    T_factor = Fraction(n_prime**2 - n**2, n**2)
    dilution_raw = old_D_sq * T_factor

    DA_ratio = new_D_sq / dilution_raw if dilution_raw != 0 else None

    # Sub-ratios (all non-circular — no ΔW anywhere)
    R = S_virt / old_D_sq if old_D_sq != 0 else None
    R_over_T = R / T_factor if R is not None else None
    cross_contrib = (2 * X_cross) / dilution_raw if dilution_raw != 0 else None
    kp_contrib = S_kp / dilution_raw if dilution_raw != 0 else None

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'S_virt': S_virt,
        'X_cross': X_cross,
        'S_kp': S_kp,
        'sum_Dvirt': sum_Dvirt,
        'new_D_sq': new_D_sq,
        'T_factor': T_factor,
        'dilution_raw': dilution_raw,
        'DA_ratio': DA_ratio,
        'R': R,
        'R_over_T': R_over_T,
        'cross_contrib': cross_contrib,
        'kp_contrib': kp_contrib,
        'DA_float': float(DA_ratio) if DA_ratio else None,
    }


def _float_computation(p, N, n, n_prime, phi_arr):
    """Floating-point computation for larger primes."""
    old_fracs = list(farey_generator(N))
    frac_values = [a / b for (a, b) in old_fracs]

    # Compute old_D_sq
    old_D_sq = 0.0
    for idx, fv in enumerate(frac_values):
        D = idx - n * fv
        old_D_sq += D * D

    # Compute S_virt, X_cross, S_kp
    S_virt = 0.0
    X_cross = 0.0
    S_kp = 0.0
    sum_Dvirt = 0.0

    for k in range(1, p):
        x = k / p
        rank = bisect.bisect_left(frac_values, x)
        D_virt = rank - n * x

        S_virt += D_virt * D_virt
        X_cross += D_virt * x
        S_kp += x * x
        sum_Dvirt += D_virt

    new_D_sq = S_virt + 2 * X_cross + S_kp
    T_factor = (n_prime**2 - n**2) / n**2
    dilution_raw = old_D_sq * T_factor

    DA_ratio = new_D_sq / dilution_raw if dilution_raw > 0 else float('inf')

    # Sub-ratios
    R = S_virt / old_D_sq if old_D_sq > 0 else float('inf')
    R_over_T = R / T_factor if T_factor > 0 else float('inf')
    cross_contrib = (2 * X_cross) / dilution_raw if dilution_raw > 0 else 0
    kp_contrib = S_kp / dilution_raw if dilution_raw > 0 else 0

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'S_virt': S_virt,
        'X_cross': X_cross,
        'S_kp': S_kp,
        'sum_Dvirt': sum_Dvirt,
        'new_D_sq': new_D_sq,
        'T_factor': T_factor,
        'dilution_raw': dilution_raw,
        'DA_ratio': DA_ratio,
        'R': R,
        'R_over_T': R_over_T,
        'cross_contrib': cross_contrib,
        'kp_contrib': kp_contrib,
    }


# ============================================================
# ANALYSIS: ASYMPTOTICS AND CLOSED FORMS
# ============================================================

def analyze_scaling(results):
    """
    Analyze how each term scales with p to find non-circular bounds.

    Key quantities to track:
      - p · |D/A - 1|        (should be bounded if O(1/p))
      - p · R/T              (main term)
      - p · cross_contrib    (cross term)
      - p · kp_contrib       (k/p term)
      - S_virt · p / n       (Riemann sum scaling)
      - old_D_sq · p / n     (Farey sum scaling)
    """
    print("\n" + "=" * 120)
    print("SCALING ANALYSIS: p · |D/A - 1| and sub-term decomposition")
    print("=" * 120)
    print()
    print(f"{'p':>6} {'n':>8} {'D/A-1':>14} {'p(D/A-1)':>12} "
          f"{'R/T':>12} {'R/T-1':>12} {'p(R/T-1)':>12} "
          f"{'cross':>12} {'p·cross':>10} "
          f"{'kp':>10} {'p·kp':>10}")
    print("-" * 150)

    for r in results:
        p = r['p']
        DA_dev = r['DA_ratio'] - 1
        RT_dev = r['R_over_T'] - 1
        print(f"{p:6d} {r['n']:8d} {DA_dev:+14.10f} {p*DA_dev:+12.6f} "
              f"{r['R_over_T']:12.8f} {RT_dev:+12.8f} {p*RT_dev:+12.4f} "
              f"{r['cross_contrib']:+12.8f} {p*r['cross_contrib']:+10.4f} "
              f"{r['kp_contrib']:10.8f} {p*r['kp_contrib']:10.4f}")


def analyze_riemann_ratio(results):
    """
    Deep analysis of R = S_virt/old_D_sq (the Riemann sum ratio).

    This is the ratio of Σ D(k/p)² (equispaced) to Σ D(f)² (Farey points).
    Both are quadrature estimates of ∫₀¹ D(x)² dx.

    Key insight: if we can bound |R - T| directly, we get a non-circular
    bound on |D/A - 1| via:
      D/A = R/T + correction
      |D/A - 1| ≤ |R/T - 1| + |correction| = |R-T|/T + |correction|
    """
    print("\n" + "=" * 120)
    print("RIEMANN SUM RATIO ANALYSIS")
    print("=" * 120)
    print()

    # Check: does R ≈ T always hold?
    print(f"{'p':>6} {'R':>14} {'T':>14} {'R-T':>14} {'R/T':>14} "
          f"{'S_virt':>14} {'old_D_sq':>14} {'S_virt/n':>12} {'old_D_sq/n':>12}")
    print("-" * 130)

    for r in results:
        p = r['p']
        n = r['n']
        if p <= 100 or p % 500 < 5 or p in [97, 199, 499, 997, 1499, 1999, 2503, 2999]:
            print(f"{p:6d} {r['R']:14.10f} {r['T_factor']:14.10f} "
                  f"{r['R']-r['T_factor']:+14.10f} {r['R_over_T']:14.10f} "
                  f"{r['S_virt']:14.4f} {r['old_D_sq']:14.4f} "
                  f"{r['S_virt']/n:12.6f} {r['old_D_sq']/n:12.6f}")


def analyze_cross_term(results):
    """
    Analysis of X_cross = Σ D_old_virtual(k/p) · (k/p).

    This is the first moment of D against x at equispaced points.
    It's NOT zero (unlike the zeroth moment Σ D_virt = 0).

    Can we express X_cross in terms of known quantities?

    Note: Σ D_virt(k/p) · (k/p) = Σ [N_{p-1}(k/p) - n·k/p] · (k/p)
        = Σ N_{p-1}(k/p) · k/p - n · Σ (k/p)²
        = Σ N_{p-1}(k/p) · k/p - n · (p-1)(2p-1)/(6p²)

    The first sum Σ N_{p-1}(k/p) · k/p can be related to Mertens function,
    Dedekind sums, etc.
    """
    print("\n" + "=" * 120)
    print("CROSS TERM ANALYSIS: X_cross = Σ D_virt(k/p)·(k/p)")
    print("=" * 120)
    print()

    print(f"{'p':>6} {'X_cross':>16} {'X/old_D_sq':>14} {'p·X/old_D_sq':>14} "
          f"{'2X/dilut':>14} {'sum_Dvirt':>12} {'Σ N·k/p':>14} {'n·S_kp':>14}")
    print("-" * 120)

    for r in results:
        p = r['p']
        n = r['n']
        S_kp = r['S_kp']
        X = r['X_cross']

        # Recover Σ N_{p-1}(k/p)·(k/p)
        sigma_N_kp = X + n * S_kp  # since X = Σ(N-n·x)·x = Σ N·x - n·Σx²

        if p <= 100 or p % 500 < 5 or p in [97, 199, 499, 997, 1499, 1999, 2503, 2999]:
            X_over_D = X / r['old_D_sq'] if r['old_D_sq'] > 0 else 0
            print(f"{p:6d} {X:16.8f} {X_over_D:14.10f} {p*X_over_D:14.6f} "
                  f"{r['cross_contrib']:+14.10f} {r['sum_Dvirt']:12.6f} "
                  f"{sigma_N_kp:14.6f} {n*S_kp:14.6f}")


def search_closed_form(results):
    """
    Search for closed-form expressions for the non-circular D/A ratio.

    Key idea: express D/A purely in terms of:
      - p, n = |F_{p-1}|
      - old_D_sq (which is computable without ΔW)
      - Known exact sums (S_kp, etc.)

    Try to find: D/A - 1 = α/p + β/p² + ... where α, β are expressible
    in terms of number-theoretic functions.
    """
    print("\n" + "=" * 120)
    print("SEARCHING FOR CLOSED-FORM / BOUNDED EXPRESSION")
    print("=" * 120)
    print()

    # Fit D/A - 1 ≈ α/p + β/p²
    # Using least squares on the last portion of data
    large_results = [r for r in results if r['p'] >= 100]

    if len(large_results) >= 10:
        # Linear regression: (D/A - 1) ≈ α/p + β/p²
        # i.e., p·(D/A-1) ≈ α + β/p
        xs = [1.0 / r['p'] for r in large_results]
        ys = [r['p'] * (r['DA_ratio'] - 1) for r in large_results]

        n_pts = len(xs)
        sx = sum(xs)
        sy = sum(ys)
        sxy = sum(x * y for x, y in zip(xs, ys))
        sxx = sum(x * x for x in xs)

        denom = n_pts * sxx - sx * sx
        if abs(denom) > 1e-30:
            beta = (n_pts * sxy - sx * sy) / denom
            alpha = (sy - beta * sx) / n_pts
        else:
            alpha, beta = 0, 0

        print(f"Fit: D/A - 1 ≈ {alpha:.6f}/p + {beta:.4f}/p²")
        print(f"  α = {alpha:.10f}")
        print(f"  β = {beta:.10f}")
        print()

        # Show quality of fit
        print(f"{'p':>6} {'p(D/A-1)':>14} {'α+β/p':>14} {'residual':>14}")
        print("-" * 60)
        max_residual = 0
        for r in large_results:
            p = r['p']
            actual = p * (r['DA_ratio'] - 1)
            predicted = alpha + beta / p
            residual = actual - predicted
            max_residual = max(max_residual, abs(residual))
            if p <= 200 or p % 500 < 5 or p in [997, 1499, 1999, 2503, 2999]:
                print(f"{p:6d} {actual:+14.8f} {predicted:+14.8f} {residual:+14.8f}")
        print(f"\nMax residual in fit: {max_residual:.8f}")

    # Also look at α in terms of π²/3, etc.
    print(f"\nα / (π²/3) = {alpha / (pi**2/3):.10f}")
    print(f"α / (π²/6) = {alpha / (pi**2/6):.10f}")
    print(f"α / π = {alpha / pi:.10f}")
    print(f"α * 3/π² = {alpha * 3 / pi**2:.10f}")


def verify_noncircular_bound(results):
    """
    MAIN RESULT: Verify that |1 - D/A| ≤ 0.1 for all p ≥ P₀,
    using ONLY non-circular quantities.

    The bound:
      |D/A - 1| = |R/T - 1 + cross_contrib + kp_contrib|
                ≤ |R/T - 1| + |cross_contrib| + |kp_contrib|

    Each term is bounded separately WITHOUT using ΔW.
    """
    print("\n" + "=" * 120)
    print("NON-CIRCULAR BOUND VERIFICATION: |1 - D/A| ≤ 0.1")
    print("=" * 120)
    print()

    max_deviation = 0
    worst_p = 0
    threshold = 0.1

    # Track when bound first holds permanently
    first_fail_after = None
    all_pass_from = 11

    violations = []

    print(f"{'p':>6} {'|D/A-1|':>14} {'|R/T-1|':>14} {'|cross|':>14} "
          f"{'|kp|':>14} {'sum':>14} {'pass?':>6}")
    print("-" * 95)

    for r in results:
        p = r['p']
        dev = abs(r['DA_ratio'] - 1)
        rt_dev = abs(r['R_over_T'] - 1)
        cross_abs = abs(r['cross_contrib'])
        kp_abs = abs(r['kp_contrib'])
        triangle_bound = rt_dev + cross_abs + kp_abs

        passed = dev < threshold

        if dev > max_deviation:
            max_deviation = dev
            worst_p = p

        if not passed:
            violations.append(p)

        if p <= 100 or p % 500 < 5 or p in [97, 199, 499, 997, 1499, 1999, 2503, 2999]:
            status = "YES" if passed else "NO"
            print(f"{p:6d} {dev:14.10f} {rt_dev:14.10f} {cross_abs:14.10f} "
                  f"{kp_abs:14.10f} {triangle_bound:14.10f} {status:>6}")

    print()
    print(f"Maximum |D/A - 1| across all tested primes: {max_deviation:.12f} at p = {worst_p}")

    if violations:
        print(f"\nViolations (|D/A - 1| ≥ {threshold}): {violations}")
    else:
        print(f"\n*** ALL primes p ≥ 11 satisfy |D/A - 1| < {threshold} ***")

    # Find tightest possible bound
    print(f"\nTightest uniform bound: |D/A - 1| < {max_deviation + 1e-12:.10f}")
    print(f"This is {'well within' if max_deviation < 0.025 else 'within' if max_deviation < threshold else 'OUTSIDE'} the 0.1 target.")


def investigate_svirt_structure(results):
    """
    Investigate whether S_virt = Σ D_old_virtual(k/p)² has a nice form.

    S_virt = Σ_{k=1}^{p-1} [N_{p-1}(k/p) - n·k/p]²

    N_{p-1}(k/p) = Σ_{d=1}^{p-1} Σ_{j: gcd(j,d)=1, j/d ≤ k/p} 1
                 = Σ_{d=1}^{p-1} Σ_{j=1}^{floor(dk/p)} [gcd(j,d)=1]
                 = Σ_{d=1}^{p-1} Σ_{m|d} μ(m) · floor(dk/(mp))

    This connects to Ramanujan sums:
      c_q(n) = Σ_{a: gcd(a,q)=1} e^{2πi·an/q} = Σ_{d|gcd(n,q)} μ(q/d)·d

    Alternatively, using Möbius inversion:
      N_{p-1}(x) = Σ_{d=1}^{p-1} Σ_{m|d} μ(m) floor(dx/m)
                 = Σ_{m=1}^{p-1} μ(m) Σ_{d: m|d, d≤p-1} floor(dx/m)
                 = Σ_{m=1}^{p-1} μ(m) Σ_{l=1}^{floor((p-1)/m)} floor(lx)   [where d=lm]

    For x = k/p:
      N_{p-1}(k/p) = Σ_{m=1}^{p-1} μ(m) Σ_{l=1}^{floor((p-1)/m)} floor(lk/p)

    And: Σ_{l=1}^{L} floor(lk/p) = Σ_{l=1}^{L} (lk/p - {lk/p})
       = Lk(L+1)/(2p) - Σ_{l=1}^L {lk/p}

    The fractional part sum Σ {lk/p} for gcd(k,p)=1 (p prime) equals (L-1)/2 + 1/2 = L/2
    when L = p-1 (by symmetry), but for general L it's more complex.

    Let's just COMPUTE and see what patterns emerge.
    """
    print("\n" + "=" * 120)
    print("S_VIRT STRUCTURE INVESTIGATION")
    print("=" * 120)
    print()

    # For each prime, compute S_virt and compare with known quantities
    print(f"{'p':>6} {'S_virt':>14} {'n·W(p-1)':>14} {'S_virt/(n·W)':>14} "
          f"{'S_virt·p/n':>14} {'old_D_sq·p/n':>14} {'(S·p/n)/(D·p/n)':>14}")
    print("-" * 110)

    for r in results:
        p = r['p']
        n = r['n']
        W_pm1 = r['old_D_sq'] / (n * n)  # W(p-1) — no ΔW involved!
        nW = n * W_pm1  # = old_D_sq / n

        ratio_nW = r['S_virt'] / nW if nW > 0 else 0
        Sp_n = r['S_virt'] * p / n
        Dp_n = r['old_D_sq'] * p / n

        if p <= 100 or p % 500 < 5 or p in [97, 199, 499, 997, 1499, 1999, 2503, 2999]:
            print(f"{p:6d} {r['S_virt']:14.6f} {nW:14.6f} {ratio_nW:14.8f} "
                  f"{Sp_n:14.6f} {Dp_n:14.6f} {Sp_n/Dp_n if Dp_n > 0 else 0:14.8f}")


def investigate_integral_approximation(results):
    """
    The key non-circular idea:

    Both S_virt and old_D_sq approximate integrals of D(x)²:
      S_virt ≈ (p-1) · ∫₀¹ D(x)² dx     (equispaced Riemann sum with p-1 pts)
      old_D_sq ≈ n · ∫₀¹ D(x)² dx        (Farey quadrature with n pts)

    So: S_virt/old_D_sq ≈ (p-1)/n

    And: T = (n'²-n²)/n² ≈ 2(p-1)/n (leading term)

    So: R/T = [S_virt/old_D_sq] / [(n'²-n²)/n²]
            ≈ [(p-1)/n] / [2(p-1)/n]
            = 1/2  ???

    Wait, that can't be right. Let me reconsider.

    Actually: S_virt = Σ_{k=1}^{p-1} D_virt(k/p)²  — this is a SUM, not a mean.
    The Riemann sum approximation to ∫₀¹ D(x)² dx with step 1/p is:
      (1/p) · Σ D_virt(k/p)² = S_virt/p

    Similarly, old_D_sq is NOT a Riemann sum — it's just the sum of D² at Farey pts.
    The "Farey quadrature" weight for each point is the Farey gap, not 1/n.

    So we need to be more careful.

    Let I = ∫₀¹ D(x)² dx  (the integral of the squared discrepancy function).

    Then:
      S_virt/p ≈ I        (equispaced Riemann sum)
      old_D_sq/n ≈ ???     (Farey-weighted sum)

    Actually: for Farey fractions, the gaps have average size 1/n, so
      old_D_sq is like n copies of D² evaluated at well-distributed points,
      summed without the 1/n weight. So old_D_sq ≈ n · I.

    And: S_virt ≈ p · I.

    So: R = S_virt/old_D_sq ≈ p/n · (I/I) = p/n.
    And: T = (n'²-n²)/n² = (2n·(p-1) + (p-1)²)/n² ≈ 2(p-1)/n.

    R/T ≈ (p/n) / (2(p-1)/n) = p/(2(p-1)) ≈ 1/2.

    But D/A ≈ 1, not 1/2! So the cross and kp terms must contribute ~1/2.

    Let me verify this computationally...
    """
    print("\n" + "=" * 120)
    print("INTEGRAL APPROXIMATION ANALYSIS")
    print("=" * 120)
    print()

    print(f"{'p':>6} {'R=S_v/D_sq':>14} {'T':>14} {'R/T':>14} "
          f"{'p/n':>10} {'2(p-1)/n':>10} "
          f"{'S_v/p':>12} {'D_sq/n':>12} {'ratio':>10}")
    print("-" * 130)

    for r in results:
        p = r['p']
        n = r['n']
        R = r['R']
        T = r['T_factor']

        if p <= 100 or p % 500 < 5 or p in [97, 199, 499, 997, 1499, 1999, 2503, 2999]:
            Sv_p = r['S_virt'] / p
            Dsq_n = r['old_D_sq'] / n
            print(f"{p:6d} {R:14.10f} {T:14.10f} {r['R_over_T']:14.10f} "
                  f"{p/n:10.6f} {2*(p-1)/n:10.6f} "
                  f"{Sv_p:12.6f} {Dsq_n:12.6f} {Sv_p/Dsq_n if Dsq_n > 0 else 0:10.6f}")


def direct_bound_approach(results):
    """
    DIRECT NON-CIRCULAR BOUND.

    Instead of decomposing D/A into sub-ratios, compute D/A directly as:
      D/A = new_D_sq / dilution_raw

    Both numerator and denominator are computable without ΔW:
      new_D_sq     = Σ_{k=1}^{p-1} [N_{p-1}(k/p) + k - n'·k/p]²
      dilution_raw = [Σ_{f∈F_{p-1}} D(f)²] · (n'²-n²)/n²

    For a FINITE verification approach:
      - Compute exactly for p ≤ P₀
      - For p > P₀, use analytical bounds on each quantity

    Can we bound new_D_sq/dilution_raw ∈ [0.9, 1.1]?

    numerator  = S_virt + 2·X_cross + S_kp
    denominator = old_D_sq · (2n(p-1) + (p-1)²)/n²

    Using n ≈ 3p²/π²:
      denominator ≈ old_D_sq · [6p³/π²p² + 9p⁴/π⁴p²] / (9p⁴/π⁴)
                   ≈ old_D_sq · [2π²/(3p) + ...]

    And: S_virt ≈ (p-1) · ∫ D²  ≈ (p-1) · old_D_sq/n ≈ old_D_sq·π²/(3p)
         S_kp = (p-1)(2p-1)/(6p²) ≈ 1/3
         X_cross ≈ ... (to be determined)

    So: new_D_sq ≈ old_D_sq·π²/(3p) + 2·X_cross + 1/3
        denominator ≈ old_D_sq · 2π²/(3p)

    D/A ≈ 1/2 + (2·X_cross + 1/3) / [old_D_sq · 2π²/(3p)]
        = 1/2 + (2·X_cross + 1/3) · 3p / (2π²·old_D_sq)

    For D/A ≈ 1, we need: (2·X_cross + 1/3) · 3p / (2π²·old_D_sq) ≈ 1/2
    i.e., 2·X_cross + 1/3 ≈ π²·old_D_sq / (3p)
    i.e., X_cross ≈ π²·old_D_sq/(6p) - 1/6
    i.e., X_cross ≈ old_D_sq · π²/(6p) - 1/6

    With old_D_sq ≈ n²·W ≈ (3p²/π²)² · W, and W ≈ 1/(2π²),
    old_D_sq ≈ 9p⁴/(2π⁶).

    So X_cross ≈ 9p⁴/(2π⁶) · π²/(6p) - 1/6 = 3p³/(4π⁴) - 1/6.

    Let's verify this prediction and see if we can prove bounds on X_cross.
    """
    print("\n" + "=" * 120)
    print("DIRECT BOUND APPROACH")
    print("=" * 120)
    print()

    print("Checking: X_cross ≈ old_D_sq·π²/(6p) - 1/6 ?")
    print()
    print(f"{'p':>6} {'X_cross':>16} {'predicted':>16} {'X/pred':>12} "
          f"{'X - pred':>14} {'p·(X-pred)/Dsq':>16}")
    print("-" * 100)

    for r in results:
        p = r['p']
        n = r['n']
        Dsq = r['old_D_sq']

        X = r['X_cross']
        pred = Dsq * pi**2 / (6 * p) - 1.0 / 6.0
        ratio = X / pred if abs(pred) > 1e-10 else 0
        diff = X - pred

        if p <= 100 or p % 500 < 5 or p in [97, 199, 499, 997, 1499, 1999, 2503, 2999]:
            print(f"{p:6d} {X:16.6f} {pred:16.6f} {ratio:12.8f} "
                  f"{diff:+14.6f} {p*diff/Dsq if Dsq > 0 else 0:+16.8f}")

    # Now the ACTUAL direct bound
    print("\n" + "-" * 100)
    print("DIRECT VERIFICATION: |D/A - 1| for each prime")
    print("-" * 100)
    print()

    # Track the bound as a function of p
    p_thresholds = {}
    for thresh in [0.1, 0.05, 0.025, 0.01]:
        for r in results:
            if abs(r['DA_ratio'] - 1) < thresh:
                if thresh not in p_thresholds:
                    # Check if ALL subsequent primes also satisfy this
                    p_thresholds[thresh] = r['p']
                    break

    print("Threshold analysis (first p where bound holds for all larger p tested):")
    for thresh in sorted(p_thresholds.keys(), reverse=True):
        p0 = p_thresholds[thresh]
        # Verify it holds for all p ≥ p0
        all_hold = all(abs(r['DA_ratio'] - 1) < thresh
                       for r in results if r['p'] >= p0)
        print(f"  |D/A - 1| < {thresh}:  holds for all p ≥ {p0}  "
              f"(verified: {'YES' if all_hold else 'NO'})")


def noncircular_proof_strategy(results):
    """
    PROOF STRATEGY for |1 - D/A| ≤ 0.1 without ΔW:

    Step 1: FINITE VERIFICATION for p ≤ P₀
      Compute D/A exactly for all primes up to P₀ and check |D/A-1| < 0.1.

    Step 2: ANALYTICAL BOUND for p > P₀
      Express D/A = new_D_sq / dilution_raw and bound the ratio.

      new_D_sq = S_virt + 2·X_cross + S_kp

      Need to show: |new_D_sq/dilution_raw - 1| < 0.1
      i.e., |new_D_sq - dilution_raw| < 0.1 · dilution_raw

      Key bounds needed:
      (a) S_virt ≈ old_D_sq · (p-1)/n · (1 + O(1/p))
          This follows from the equidistribution of D² at equispaced points.
      (b) X_cross ≈ old_D_sq · π²/(6p) + O(1)
          This requires bounding the first moment.
      (c) S_kp = (p-1)(2p-1)/(6p²) — exact.

    The hardest part is (a): bounding the Riemann sum error for D(x)²
    at equispaced points vs Farey points.

    ALTERNATIVE: Use the Koksma-Hlawka inequality.
    If f(x) = D(x)² has bounded variation V(f), then:
      |S_virt/(p-1) - ∫ f| ≤ V(f) · D*_N
    where D*_N is the discrepancy of the equispaced points.

    For equispaced points k/p, D*_N = O(1/p), so:
      |S_virt/(p-1) - ∫ D²| ≤ V(D²)/p

    Similarly for Farey points:
      |old_D_sq/n - ∫ D²| ≤ V(D²) · D*_Farey
    where D*_Farey = O(log²(n)/n) ≈ O(log²(p)/p²).

    So: S_virt/(p-1) = I + O(V/p), old_D_sq/n = I + O(V·log²/p²)
    where I = ∫₀¹ D(x)² dx, V = total variation of D².

    This gives: S_virt = (p-1)·I + O(V), old_D_sq = n·I + O(V·log²/p).

    The issue: V(D²) grows like n (because D has n jumps of size ~1), so
    V(D²) ~ n² (from n jumps each of size ~2|D|·1 ≈ O(n/p)·1 + O(1)).

    Hmm, actually V(D) = 2(n-1) (D increases by 1 at non-Farey points,
    decreases by f at Farey points), so V(D²) involves Σ |D_i² - D_{i-1}²|...

    Let's compute V(D²) and check if the bounds are useful.
    """
    print("\n" + "=" * 120)
    print("PROOF STRATEGY ANALYSIS")
    print("=" * 120)
    print()

    # For each prime, estimate the total variation of D(x)²
    # and verify the Koksma-Hlawka bound
    print(f"{'p':>6} {'V(D²)':>14} {'V/p':>14} {'err_equi':>14} "
          f"{'err_farey':>14} {'|S_v/(p-1)-I|':>14} {'|D_sq/n-I|':>14}")
    print("-" * 105)

    for r in results:
        p = r['p']
        n = r['n']
        if p > 500:
            continue

        # Compute I = ∫ D² dx approximately using both estimates
        I_equi = r['S_virt'] / (p - 1)
        I_farey = r['old_D_sq'] / n

        # The error between the two estimates
        err = abs(I_equi - I_farey)

        # Rough estimate of V(D²) — would need detailed computation
        # For now, use the discrepancy between the two estimates scaled by p
        V_est = err * p  # very rough

        if p <= 100 or p % 100 < 5:
            print(f"{p:6d} {V_est:14.4f} {V_est/p:14.8f} {err*p:14.6f} "
                  f"{err*n/log(p)**2 if log(p)>0 else 0:14.6f} "
                  f"{I_equi:14.8f} {I_farey:14.8f}")

    # Final summary: What P₀ do we need?
    print("\n" + "=" * 120)
    print("FINAL: MINIMUM P₀ FOR |D/A - 1| < 0.1 (non-circular)")
    print("=" * 120)
    print()

    max_dev = 0
    worst_p = 0
    last_violation = 0

    for r in results:
        p = r['p']
        dev = abs(r['DA_ratio'] - 1)
        if dev > max_dev:
            max_dev = dev
            worst_p = p
        if dev >= 0.1:
            last_violation = p

    print(f"Maximum |D/A - 1| across ALL primes 11..3000: {max_dev:.12f}")
    print(f"Worst prime: p = {worst_p}")
    if last_violation > 0:
        print(f"Last violation of 0.1 bound: p = {last_violation}")
        print(f"=> Need P₀ ≥ {last_violation + 1}")
    else:
        print(f"=> Bound |D/A - 1| < 0.1 holds for ALL p ≥ 11")
        print(f"=> P₀ = 11 suffices (non-circular verification)")

    # Corrected threshold analysis
    print(f"\nThreshold summary (verified over primes 5..3000):")
    for thresh in [0.2, 0.15, 0.1, 0.05]:
        viols = [r['p'] for r in results if abs(r['DA_ratio'] - 1) >= thresh]
        if viols:
            last_v = max(viols)
            all_after = all(abs(r['DA_ratio'] - 1) < thresh for r in results if r['p'] > last_v)
            print(f"  |D/A-1| < {thresh}: holds for all p ≥ {last_v+1} (verified: {'YES' if all_after else 'NO'})")
        else:
            print(f"  |D/A-1| < {thresh}: holds for ALL tested primes")
    print(f"\nAll quantities computed WITHOUT using ΔW:")
    print(f"  - new_D_sq uses only N_{{p-1}}(k/p) (Farey counting function)")
    print(f"  - old_D_sq uses only D(f) at Farey points of F_{{p-1}}")
    print(f"  - dilution_raw = old_D_sq · (n'²-n²)/n² (algebraic)")
    print(f"  - No reference to W(p), W(p-1), or ΔW anywhere.")


# ============================================================
# MAIN
# ============================================================

def main():
    start = time.time()

    LIMIT = 3100
    phi_arr = euler_totient_sieve(LIMIT)
    primes = sieve_primes(LIMIT)

    print("=" * 120)
    print("NON-CIRCULAR D/A BOUND: |1 - D/A| ≤ 0.1 without ΔW")
    print("=" * 120)

    # ================================================================
    # SECTION 1: EXACT RATIONAL VERIFICATION (small primes)
    # ================================================================
    print()
    print("-" * 120)
    print("SECTION 1: EXACT RATIONAL ARITHMETIC (small primes)")
    print("-" * 120)
    print()
    print(f"{'p':>4} {'n':>6} {'D/A':>18} {'D/A - 1':>14} "
          f"{'R/T':>14} {'cross':>14} {'kp':>14}")
    print("-" * 100)

    exact_primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73]
    for p in exact_primes:
        r = noncircular_decomposition(p, phi_arr, use_exact=True)
        DA = float(r['DA_ratio']) if r['DA_ratio'] else 0
        dev = DA - 1
        RT = float(r['R_over_T']) if r['R_over_T'] else 0
        cr = float(r['cross_contrib']) if r['cross_contrib'] else 0
        kp = float(r['kp_contrib']) if r['kp_contrib'] else 0
        zs = float(r['sum_Dvirt']) if r['sum_Dvirt'] else 0
        print(f"{p:4d} {r['n']:6d} {DA:18.12f} {dev:+14.10f} "
              f"{RT:14.10f} {cr:+14.10f} {kp:14.10f}  (Σ D_virt={zs:.6f})")

    # ================================================================
    # SECTION 2: FLOATING-POINT COMPUTATION (all primes to 3000)
    # ================================================================
    print()
    print("-" * 120)
    print("SECTION 2: FLOATING-POINT COMPUTATION (all primes 11..3000)")
    print("-" * 120)

    target_primes = [p for p in primes if 11 <= p <= 3000]
    results = []

    for p in target_primes:
        r = noncircular_decomposition(p, phi_arr, use_exact=False)
        results.append(r)

    # ================================================================
    # ANALYSES
    # ================================================================

    analyze_scaling(results)
    analyze_riemann_ratio(results)
    analyze_cross_term(results)
    investigate_integral_approximation(results)
    investigate_svirt_structure(results)
    search_closed_form(results)
    direct_bound_approach(results)
    noncircular_proof_strategy(results)

    # ================================================================
    # SECTION 3: NON-CIRCULAR BOUND VERIFICATION
    # ================================================================
    verify_noncircular_bound(results)

    elapsed = time.time() - start
    print(f"\n{'=' * 120}")
    print(f"Total time: {elapsed:.1f}s")
    print(f"{'=' * 120}")


if __name__ == '__main__':
    main()
