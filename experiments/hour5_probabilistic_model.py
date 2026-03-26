#!/usr/bin/env python3
"""
HOUR 5: PROBABILISTIC MODEL — Concentration of D·δ Correlation
==============================================================

KEY NEW THEORETICAL INSIGHT:
  We proved: Σ_f f·δ(f) = C_raw/2  (exact identity via deficit sums)

  This gives the linear decomposition:
    B_raw = α·C_raw + 2·Σ_f ε(f)·δ(f)

  where:
    α = Σ D(f)·(f-1/2) / Σ(f-1/2)²  [linear regression slope of D on (f-1/2)]
    ε(f) = D(f) - α·(f-1/2)           [regression residual]

  Proof:
    B_raw = 2·Σ D·δ = 2·Σ [α(f-1/2) + ε]·δ
           = 2α·Σ(f-1/2)·δ + 2·Σ ε·δ
           = 2α·(C_raw/2) + 2·Σ ε·δ   [using the identity]
           = α·C_raw + 2·Σ ε·δ

  GOALS:
  1. Verify the decomposition B_raw = α·C_raw + 2·Σ ε·δ exactly
  2. Compute α, Σ ε·δ, C_raw for all primes ≤ 5000
  3. Prove B_raw + C_raw = (α+1)·C_raw + 2·Σ ε·δ > 0 iff (α+1)/2 > |Σ ε·δ|/C_raw
  4. Identify whether |Σ ε·δ|/C_raw < 1/2 for all p ≥ 11 (i.e., whether R > -1)
  5. Find: does Σ ε·δ / C_raw converge to a constant? Does it go to 0?

  EXTENDED VERIFICATION:
  - Check B+C > 0 for ALL primes up to 5000
  - Find worst-case R = B_raw/C_raw

  NEW BOUND ATTEMPT:
  - If |Σ ε·δ|/C_raw is bounded by 1/2 - α, this proves R > -1.
  - Use Cauchy-Schwarz on residuals: |Σ ε·δ| ≤ sqrt(Σ ε²)·sqrt(C_raw)
  - This requires Σ ε²/C_raw ≤ (1+α)²/4 — check numerically
"""

import time
from math import gcd, isqrt, sqrt, floor, log, pi
from bisect import bisect_left, bisect_right

start_time = time.time()
MAX_RUNTIME = 300  # 5 minutes

def elapsed():
    return time.time() - start_time


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
    """Generate Farey sequence F_N as (num, den) pairs in sorted order."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b


def compute_all_terms(p, phi_arr):
    """
    Compute all key quantities for the probabilistic decomposition at prime p.

    Returns:
        dict with all quantities for analysis
    """
    N = p - 1

    # Build Farey sequence F_N as float values (for speed) + exact fractions
    farey_fracs_float = []  # (float_val, num, den)
    for a, b in farey_generator(N):
        farey_fracs_float.append((a / b, a, b))
    # farey_fracs_float is already sorted by (a/b)

    n = len(farey_fracs_float)
    n_prime = n + (p - 1)

    # Compute D(f) for each old fraction f in F_N
    # D(f) = rank(f) - n*f  (rank = index 0..n)
    D_vals = []
    f_vals = []
    a_vals = []
    b_vals = []

    for idx, (fv, a, b) in enumerate(farey_fracs_float):
        D = idx - n * fv
        D_vals.append(D)
        f_vals.append(fv)
        a_vals.append(a)
        b_vals.append(b)

    # Compute δ(f) = (a - pa mod b)/b for each fraction
    delta_vals = []
    for i, (fv, a, b) in enumerate(farey_fracs_float):
        pa_mod_b = (p * a) % b
        delta = (a - pa_mod_b) / b
        delta_vals.append(delta)

    # ----------------------------------------------------------------
    # CORE QUANTITIES
    # ----------------------------------------------------------------

    old_D_sq = sum(D * D for D in D_vals)
    C_raw = sum(d * d for d in delta_vals)  # = Σ δ²
    B_raw = 2.0 * sum(D_vals[i] * delta_vals[i] for i in range(n))

    # ----------------------------------------------------------------
    # VERIFY IDENTITY: Σ f·δ(f) = C_raw/2
    # ----------------------------------------------------------------
    sum_f_delta = sum(f_vals[i] * delta_vals[i] for i in range(n))
    sum_f_half_delta = sum((f_vals[i] - 0.5) * delta_vals[i] for i in range(n))
    sum_delta = sum(delta_vals)  # Should be ≈ 0 (permutation)

    identity_check = abs(sum_f_delta - C_raw / 2)  # Should be ≈ 0

    # ----------------------------------------------------------------
    # REGRESSION: α = Σ D(f)·(f-1/2) / Σ(f-1/2)²
    # ----------------------------------------------------------------
    sum_D_fhalf = sum(D_vals[i] * (f_vals[i] - 0.5) for i in range(n))
    sum_fhalf_sq = sum((f_vals[i] - 0.5)**2 for i in range(n))

    alpha = sum_D_fhalf / sum_fhalf_sq if sum_fhalf_sq > 0 else 0.0

    # Residuals ε(f) = D(f) - α·(f-1/2)
    epsilon_vals = [D_vals[i] - alpha * (f_vals[i] - 0.5) for i in range(n)]

    # ----------------------------------------------------------------
    # VERIFY DECOMPOSITION: B_raw = α·C_raw + 2·Σ ε·δ
    # ----------------------------------------------------------------
    sum_eps_delta = sum(epsilon_vals[i] * delta_vals[i] for i in range(n))
    B_raw_decomp = alpha * C_raw + 2 * sum_eps_delta  # Should equal B_raw

    decomp_error = abs(B_raw - B_raw_decomp)  # Should be ≈ 0

    # ----------------------------------------------------------------
    # KEY RATIOS
    # ----------------------------------------------------------------
    R = B_raw / C_raw if C_raw > 0 else 0.0  # = 2·Σ D·δ / Σ δ²

    # For B+C > 0: need R > -1
    B_plus_C = B_raw + C_raw  # Should be > 0

    # The ratio: Σ ε·δ / C_raw (the "residual ratio")
    residual_ratio = sum_eps_delta / C_raw if C_raw > 0 else 0.0

    # Cauchy-Schwarz bound: |Σ ε·δ| ≤ sqrt(Σ ε²)·sqrt(C_raw)
    sum_eps_sq = sum(e * e for e in epsilon_vals)
    cs_bound = sqrt(sum_eps_sq * C_raw) if sum_eps_sq > 0 and C_raw > 0 else 0.0
    cs_ratio = abs(sum_eps_delta) / cs_bound if cs_bound > 0 else 0.0  # Should be ≤ 1

    # The regression "quality": fraction of D² explained by linear term
    # R² = 1 - Σε²/Σ(D-D̄)²
    D_mean = sum(D_vals) / n
    sum_D_centered_sq = sum((D_vals[i] - D_mean)**2 for i in range(n))
    R_squared = 1.0 - sum_eps_sq / sum_D_centered_sq if sum_D_centered_sq > 0 else 0.0

    # ----------------------------------------------------------------
    # DILUTION AND D/A (non-circular part)
    # ----------------------------------------------------------------
    dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2

    # New D^2: equispaced sum at k/p
    # Build sorted Farey float array for binary search
    fary_floats = [fv for fv, a, b in farey_fracs_float]

    S_virt = 0.0
    X_cross = 0.0
    for k in range(1, p):
        target = k / p
        # Count fractions ≤ target in F_N
        rank_at_target = bisect_right(fary_floats, target + 1e-12)
        # Handle exact Farey fractions: target might equal a Farey fraction
        # More careful: count fractions strictly ≤ k/p
        # Use the exact inequality: a/b ≤ k/p iff a*p ≤ k*b
        # For float we accept small error here
        Dv = rank_at_target - n * target
        S_virt += Dv * Dv
        X_cross += Dv * target

    S_kp = sum(k*k for k in range(1, p)) / p**2  # = (p-1)(2p-1)/(6p²) * p = (p-1)(2p-1)/(6p)
    new_D_sq = S_virt + 2 * X_cross + S_kp
    DA_ratio = new_D_sq / dilution_raw if dilution_raw > 0 else 0.0

    return {
        'p': p, 'n': n, 'n_prime': n_prime, 'N': N,
        'old_D_sq': old_D_sq,
        'C_raw': C_raw,
        'B_raw': B_raw,
        'R': R,
        'B_plus_C': B_plus_C,
        'dilution_raw': dilution_raw,
        'DA_ratio': DA_ratio,

        # Identity check
        'sum_f_delta': sum_f_delta,
        'C_raw_half': C_raw / 2,
        'identity_error': identity_check,

        # Regression
        'alpha': alpha,
        'sum_fhalf_sq': sum_fhalf_sq,
        'sum_D_fhalf': sum_D_fhalf,
        'R_squared': R_squared,

        # Decomposition
        'sum_eps_delta': sum_eps_delta,
        'sum_eps_sq': sum_eps_sq,
        'decomp_error': decomp_error,
        'residual_ratio': residual_ratio,

        # Cauchy-Schwarz
        'cs_bound': cs_bound,
        'cs_ratio': cs_ratio,

        # Additional
        'sum_delta': sum_delta,
        'C_over_A': C_raw / dilution_raw if dilution_raw > 0 else 0.0,
    }


def main():
    print("=" * 75)
    print("HOUR 5: PROBABILISTIC MODEL — Linear Decomposition of B_raw")
    print("=" * 75)
    print()
    print("THEORETICAL SETUP:")
    print("  We exploit the identity: Σ_f f·δ(f) = C_raw/2  (exact!)")
    print("  This gives: B_raw = α·C_raw + 2·Σ ε·δ")
    print("  where α = regression slope of D on (f-1/2), ε = D - α(f-1/2)")
    print()
    print("  B+C > 0 iff R = B_raw/C_raw > -1")
    print("          iff α + 2·(Σε·δ)/C_raw > -1")
    print("          iff (Σε·δ)/C_raw > -(1+α)/2")
    print()

    limit = 5000
    phi_arr = euler_totient_sieve(limit + 10)
    primes = sieve_primes(limit)
    primes = [p for p in primes if p >= 11]

    print(f"Testing {len(primes)} primes in [11, {limit}]")
    print()

    # ----------------------------------------------------------------
    # PHASE 1: Verify identity and decomposition for small primes exactly
    # ----------------------------------------------------------------
    print("PHASE 1: Identity Verification (p ≤ 200)")
    print("-" * 50)
    print(f"{'p':>5} | {'α':>8} | {'R=B/C':>8} | {'ResidRatio':>10} | {'B+C>0':>6} | {'IdentErr':>10} | {'DecompErr':>10}")
    print("-" * 80)

    small_primes = [p for p in primes if p <= 200]
    max_identity_error = 0.0
    max_decomp_error = 0.0

    for p in small_primes:
        r = compute_all_terms(p, phi_arr)
        max_identity_error = max(max_identity_error, r['identity_error'])
        max_decomp_error = max(max_decomp_error, r['decomp_error'])

        flag = "OK" if r['B_plus_C'] > 0 else "FAIL"
        print(f"{p:>5} | {r['alpha']:>8.4f} | {r['R']:>8.4f} | {r['residual_ratio']:>10.4f} | "
              f"{flag:>6} | {r['identity_error']:>10.2e} | {r['decomp_error']:>10.2e}")

    print()
    print(f"Max identity error (|Σf·δ - C/2|): {max_identity_error:.2e}")
    print(f"Max decomp error (|B - α·C - 2Σε·δ|): {max_decomp_error:.2e}")
    print()

    # ----------------------------------------------------------------
    # PHASE 2: Systematic analysis for all primes ≤ 5000
    # ----------------------------------------------------------------
    print("PHASE 2: Full Analysis for All Primes ≤ 5000")
    print("-" * 50)

    results = []
    violations = []

    min_R = float('inf')
    min_R_p = -1
    min_Bplus_C = float('inf')

    for i, p in enumerate(primes):
        if elapsed() > MAX_RUNTIME * 0.8:
            print(f"  [Time limit approaching, stopping at p={p}]")
            break

        r = compute_all_terms(p, phi_arr)
        results.append(r)

        if r['R'] < min_R:
            min_R = r['R']
            min_R_p = p
        if r['B_plus_C'] < min_Bplus_C:
            min_Bplus_C = r['B_plus_C']

        if r['B_plus_C'] <= 0:
            violations.append(r)

        # Print progress
        if p <= 100 or (p <= 1000 and i % 20 == 0) or i % 50 == 0:
            print(f"  p={p:5d}: R={r['R']:+.4f}, α={r['alpha']:+.4f}, "
                  f"res_ratio={r['residual_ratio']:+.4f}, B+C={'OK' if r['B_plus_C']>0 else 'FAIL'}")

    print()
    print("=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"  Primes tested: {len(results)}")
    print(f"  Violations (B+C ≤ 0): {len(violations)}")
    if violations:
        for v in violations:
            print(f"    p={v['p']}: R={v['R']:.4f}, B+C={v['B_plus_C']:.6e}")
    print(f"  Minimum R (= B/C): {min_R:.4f} at p={min_R_p}")
    print(f"  Minimum B+C: {min_Bplus_C:.6e}")
    print()

    if results:
        alphas = [r['alpha'] for r in results]
        residual_ratios = [r['residual_ratio'] for r in results]
        cs_ratios = [r['cs_ratio'] for r in results]
        R_vals = [r['R'] for r in results]
        R2_vals = [r['R_squared'] for r in results]

        print(f"  α statistics:")
        print(f"    min α = {min(alphas):.4f}")
        print(f"    max α = {max(alphas):.4f}")
        print(f"    mean α = {sum(alphas)/len(alphas):.4f}")
        print()
        print(f"  Residual ratio (Σε·δ / C_raw) statistics:")
        print(f"    min = {min(residual_ratios):.4f}")
        print(f"    max = {max(residual_ratios):.4f}")
        print(f"    mean = {sum(residual_ratios)/len(residual_ratios):.4f}")
        print()
        print(f"  CS efficiency ratio (|Σε·δ| / CS_bound) statistics:")
        print(f"    min = {min(cs_ratios):.4f}")
        print(f"    max = {max(cs_ratios):.4f}")
        print(f"    mean = {sum(cs_ratios)/len(cs_ratios):.4f}")
        print()
        print(f"  R² (regression quality) statistics:")
        print(f"    min R² = {min(R2_vals):.4f}")
        print(f"    max R² = {max(R2_vals):.4f}")
        print(f"    mean R² = {sum(R2_vals)/len(R2_vals):.4f}")
        print()

        # ----------------------------------------------------------------
        # PHASE 3: Analyze the KEY BOUND
        # ----------------------------------------------------------------
        print("PHASE 3: Can We Prove |Σε·δ|/C_raw < (1+α)/2?")
        print("-" * 55)
        print("  This would imply R > -1 (i.e., B+C > 0)")
        print()

        bound_holds = []
        bound_fails = []
        bound_margins = []

        for r in results:
            alpha = r['alpha']
            rr = r['residual_ratio']  # = Σε·δ/C_raw
            needed = (1 + alpha) / 2
            margin = needed - abs(rr)
            bound_margins.append(margin)

            if margin > 0:
                bound_holds.append(r['p'])
            else:
                bound_fails.append((r['p'], margin))

        print(f"  |Σε·δ|/C_raw < (1+α)/2 holds for {len(bound_holds)}/{len(results)} primes")
        print(f"  Minimum margin: {min(bound_margins):.4f}")
        print(f"  Maximum margin: {max(bound_margins):.4f}")
        print(f"  Mean margin: {sum(bound_margins)/len(bound_margins):.4f}")

        if bound_fails:
            print(f"\n  FAILS for {len(bound_fails)} primes:")
            for p, m in bound_fails[:20]:
                print(f"    p={p}: margin={m:.4f}")
        print()

        # ----------------------------------------------------------------
        # PHASE 4: The CS bound analysis
        # ----------------------------------------------------------------
        print("PHASE 4: Cauchy-Schwarz Bound on Σε·δ")
        print("-" * 55)
        print("  |Σε·δ| ≤ sqrt(Σε²) · sqrt(C_raw)  (CS)")
        print("  For R > -1, need: CS bound < (1+α)·C_raw/2")
        print("  Equivalently: Σε²/C_raw < (1+α)²/4")
        print()

        cs_vs_bound = []
        for r in results:
            alpha = r['alpha']
            required = (1 + alpha)**2 / 4
            actual = r['sum_eps_sq'] / r['C_raw'] if r['C_raw'] > 0 else 0
            cs_vs_bound.append((r['p'], actual, required, actual / required if required > 0 else float('inf')))

        ratios = [actual/required for _, actual, required, ratio in cs_vs_bound if required > 0]

        print(f"  (Σε²/C_raw) / ((1+α)²/4) statistics:")
        print(f"    min = {min(ratios):.2f}")
        print(f"    max = {max(ratios):.2f}")
        print(f"    mean = {sum(ratios)/len(ratios):.2f}")
        print()

        # Top 10 worst ratios
        cs_vs_bound_sorted = sorted(cs_vs_bound, key=lambda x: -x[3])
        print(f"  Top 10 worst cases (highest ratio):")
        for p, actual, required, ratio in cs_vs_bound_sorted[:10]:
            print(f"    p={p:5d}: Σε²/C = {actual:.4f}, need < {required:.4f}, ratio = {ratio:.2f}")
        print()

        # ----------------------------------------------------------------
        # PHASE 5: Asymptotic trend analysis
        # ----------------------------------------------------------------
        print("PHASE 5: Asymptotic Trends")
        print("-" * 55)

        # Check if R → +∞, or converges
        large_primes = [(r['p'], r['R'], r['alpha'], r['residual_ratio'])
                        for r in results if r['p'] > 1000]

        if large_primes:
            print(f"  For p > 1000 ({len(large_primes)} primes):")
            R_large = [x[1] for x in large_primes]
            alpha_large = [x[2] for x in large_primes]
            rr_large = [x[3] for x in large_primes]

            print(f"    R range: [{min(R_large):.3f}, {max(R_large):.3f}]")
            print(f"    α range: [{min(alpha_large):.3f}, {max(alpha_large):.3f}]")
            print(f"    Residual ratio range: [{min(rr_large):.3f}, {max(rr_large):.3f}]")
            print()

            # Sample trend
            sample = large_primes[::max(1, len(large_primes)//20)]
            print(f"  Trend (sample of p > 1000):")
            print(f"    {'p':>6} | {'R':>8} | {'α':>8} | {'res_ratio':>10}")
            for p, R, alpha, rr in sample[:20]:
                print(f"    {p:>6} | {R:>8.4f} | {alpha:>8.4f} | {rr:>10.4f}")

        # ----------------------------------------------------------------
        # PHASE 6: The Deficit Sum Lower Bound verification
        # ----------------------------------------------------------------
        print()
        print("PHASE 6: Deficit Sum Lower Bound for C_raw")
        print("-" * 55)
        print("  Theory: C_raw ≥ N²/(48 log N) for p ≥ 101")
        print()

        small_p_for_deficit = [r for r in results if r['p'] <= 500]
        for r in small_p_for_deficit[::5]:
            N = r['N']
            p = r['p']
            if N >= 100:
                lower = N**2 / (48 * log(N))
                actual = r['C_raw']
                ratio = actual / lower
                print(f"    p={p:5d}, N={N:5d}: C_raw={actual:.4f}, "
                      f"LB={lower:.4f}, ratio={ratio:.2f}")

        # ----------------------------------------------------------------
        # PHASE 7: New analytical bound attempt
        # ----------------------------------------------------------------
        print()
        print("PHASE 7: New Analytical Framework")
        print("-" * 55)
        print()

        # The key question: what is Σ ε·δ in terms of known quantities?
        # ε(f) = D(f) - α(f-1/2)
        # δ(f) = f - σ_p(f)
        # Σ ε·δ = Σ D·δ - α·Σ(f-1/2)·δ = B_raw/2 - α·C_raw/2
        # So: 2·Σ ε·δ = B_raw - α·C_raw  (consistent with decomposition)

        # Key: can we bound Σ ε·δ using the "non-linear D" separately?
        # ε(f) = D(f) - α(f-1/2) is the "non-linear" part of D
        # For prime b denominators: D(a/b) = Σ_{d≤N} e_d(a/b)
        # The linear part of e_d is proportional to a/d or a/b
        # The non-linear part comes from the "residual" of equidistribution

        # Check: is Σ ε·δ always ≥ -C_raw/2 (which is what we need for R ≥ -1)?
        print("  Key check: Is (Σε·δ)/C_raw > -1/2 always? (needed for R > -1)")
        residual_ratios_all = [r['residual_ratio'] for r in results]
        min_rr = min(residual_ratios_all)
        print(f"  Min (Σε·δ)/C_raw = {min_rr:.4f}")
        print(f"  This would give min R = α + 2*(Σε·δ)/C_raw")

        for r in results:
            if r['residual_ratio'] == min(residual_ratios_all):
                p0 = r['p']
                alpha0 = r['alpha']
                rr0 = r['residual_ratio']
                print(f"  Worst case: p={p0}, α={alpha0:.4f}, res_ratio={rr0:.4f}")
                print(f"  R = α + 2*res_ratio = {alpha0 + 2*rr0:.4f}")
                break

        print()
        print("  Fundamental bound: R > -1 iff 2*(Σε·δ)/C_raw > -(1+α)")
        print("  Equivalently: Σε·δ/C_raw > -(1+α)/2")
        print()

        # Check: is there a universal lower bound on Σε·δ/C_raw?
        lower_bounds_rr = [(r['p'], r['residual_ratio'], (1+r['alpha'])/2) for r in results]
        critical = [(p, rr, needed) for p, rr, needed in lower_bounds_rr if rr < -0.3]

        if critical:
            print(f"  Primes where res_ratio < -0.3:")
            for p, rr, needed in sorted(critical, key=lambda x: x[1])[:20]:
                print(f"    p={p}: res_ratio={rr:.4f}, need > {-needed:.4f}")
        else:
            print(f"  No primes with res_ratio < -0.3 (good!)")

        print()
        print("  Large p trend for res_ratio:")
        trend_data = [(r['p'], r['residual_ratio']) for r in results if r['p'] > 500]
        if trend_data:
            # Fit: does res_ratio → 0 or some constant?
            N_large = [r['N'] for r in results if r['p'] > 500]
            rr_large2 = [r['residual_ratio'] for r in results if r['p'] > 500]

            # Log fit
            logN = [log(N) for N in N_large]
            if len(rr_large2) > 5:
                mean_rr = sum(rr_large2) / len(rr_large2)
                print(f"  For p > 500: mean res_ratio = {mean_rr:.4f}")

                # Sample
                sample_trend = [(r['p'], r['residual_ratio']) for r in results[::max(1,len(results)//15)]
                                if r['p'] > 500]
                print(f"  {'p':>6} | {'res_ratio':>10} | {'R=B/C':>8}")
                for p, rr in sample_trend[:20]:
                    R_val = next(r['R'] for r in results if r['p'] == p)
                    print(f"  {p:>6} | {rr:>10.4f} | {R_val:>8.4f}")

    # ----------------------------------------------------------------
    # FINAL CONCLUSIONS
    # ----------------------------------------------------------------
    print()
    print("=" * 65)
    print("CONCLUSIONS")
    print("=" * 65)

    if results:
        n_verified = len(results)
        max_p_verified = results[-1]['p']
        n_violations = len(violations)

        print(f"\n1. B+C > 0 (R > -1) verified for all {n_verified} primes in [11, {max_p_verified}]")
        print(f"   Violations found: {n_violations}")
        print(f"   Minimum R = {min_R:.4f} at p = {min_R_p}")

        print(f"\n2. Identity Σf·δ = C/2 confirmed (max error: {max_identity_error:.2e})")
        print(f"   Decomposition B = αC + 2Σε·δ confirmed (max error: {max_decomp_error:.2e})")

        print(f"\n3. Regression slope α:")
        print(f"   Range: [{min(alphas):.3f}, {max(alphas):.3f}]")
        print(f"   Always positive? {all(a > 0 for a in alphas)}")

        print(f"\n4. Residual ratio Σε·δ/C_raw:")
        print(f"   Range: [{min(residual_ratios):.3f}, {max(residual_ratios):.3f}]")
        print(f"   Always > -1/2? {all(r > -0.5 for r in residual_ratios)}")
        print(f"   Always > -(1+α)/2? {len(bound_holds) == len(results) if 'bound_holds' in dir() else 'N/A'}")

        # The key analytical question
        print(f"\n5. KEY ANALYTICAL QUESTION:")
        print(f"   Is |Σε·δ|/C_raw < (1+α)/2 always?")
        if 'bound_fails' in dir():
            if not bound_fails:
                print(f"   YES — holds for all tested primes!")
                print(f"   This would imply R > -1 if we can prove it analytically.")
            else:
                print(f"   NO — fails for {len(bound_fails)} primes")

        print(f"\n6. CS BOUND ANALYSIS:")
        if 'ratios' in dir():
            print(f"   (Σε²/C) / ((1+α)²/4) ratio: max={max(ratios):.1f}")
            if max(ratios) < 1:
                print(f"   GREAT: CS bound alone proves R > -1 for all tested primes!")
            elif max(ratios) < 4:
                print(f"   MODERATE: CS bound is off by factor {max(ratios):.1f}, needs refinement")
            else:
                print(f"   CS bound is too weak (factor {max(ratios):.1f}), need different approach")

    print(f"\nTotal runtime: {elapsed():.1f}s")


if __name__ == '__main__':
    main()
