#!/usr/bin/env python3
"""
R(11) BYPASS CHECK: Can the proof reduce to a single computation?
=================================================================

R(p) = crossTerm(p) / (2 * shiftSquaredSum(p))

where:
  crossTerm(p) = 2 * Σ_{f in F_{p-1}} D_{p-1}(f) * δ_p(f)   [= B(p)]
  shiftSquaredSum(p) = Σ_{f in F_{p-1}} (δ_p(f))^2            [= C(p)]

So R(p) = B(p) / (2 * C(p)).

The sign theorem needs B + C > 0, i.e. 2*R*C + C > 0, i.e. C*(1 + 2R) > 0.
Since C > 0 always, we need 1 + 2R > 0, i.e. R > -1/2.

KEY QUESTION: Is R(11) the minimum of R(p) over all primes p >= 11?
If so, the proof reduces to verifying R(11) > -1/2 (a single computation).

Known: R(11) = -1155/5974 ≈ -0.1934 (from Lean native_decide).
"""

import time
import csv
from fractions import Fraction
from math import gcd, isqrt

start_time = time.time()


def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def farey_sequence(N):
    """Generate Farey sequence F_N as list of (a, b) with a/b in [0, 1]."""
    fracs = []
    a0, b0, c0, d0 = 0, 1, 1, N
    fracs.append((0, 1))
    while c0 <= N:
        fracs.append((c0, d0))
        k = (N + b0) // d0
        a0, b0, c0, d0 = c0, d0, k * c0 - a0, k * d0 - b0
    return fracs


def compute_R_exact(p):
    """Compute R(p) = crossTerm(p) / (2 * shiftSquaredSum(p)) using exact Fraction arithmetic."""
    N = p - 1
    fracs = farey_sequence(N)
    n = len(fracs)

    cross_sum = Fraction(0)  # Σ D(f) * δ(f)  [using Lean's 1-based rank]
    shift_sq_sum = Fraction(0)  # Σ δ(f)^2

    for j, (a, b) in enumerate(fracs):
        # Lean rank = j + 1 (1-based: counts elements <= f)
        # D_lean(f) = rank(f) - |F_N| * f = (j+1) - n * (a/b)
        D = Fraction(j + 1) - Fraction(n * a, b)

        # Lean: shiftFun p f = f - Int.fract(p * f)
        # For f = a/b: fract(p*a/b) = (p*a mod b) / b
        # So shiftFun = a/b - (p*a mod b)/b = (a - p*a mod b) / b
        sigma = (p * a) % b
        delta = Fraction(a - sigma, b)

        cross_sum += D * delta
        shift_sq_sum += delta * delta

    # crossTerm(p) = 2 * cross_sum  (Lean definition: 2 * Σ D*δ)
    # shiftSquaredSum(p) = shift_sq_sum
    # corrRatio(p) = crossTerm / (2 * shiftSquaredSum) = cross_sum / shift_sq_sum

    if shift_sq_sum == 0:
        return None, Fraction(0), Fraction(0)

    R = cross_sum / shift_sq_sum  # = crossTerm / (2 * shiftSquaredSum)
    return R, 2 * cross_sum, shift_sq_sum


def compute_R_float(p):
    """Fast float version for larger primes."""
    N = p - 1
    fracs = farey_sequence(N)
    n = len(fracs)

    cross_sum = 0.0
    shift_sq_sum = 0.0

    for j, (a, b) in enumerate(fracs):
        # Lean rank: 1-based (j+1)
        D = (j + 1) - n * a / b
        sigma = (p * a) % b
        delta = (a - sigma) / b

        cross_sum += D * delta
        shift_sq_sum += delta * delta

    if shift_sq_sum == 0:
        return None

    return cross_sum / shift_sq_sum


def mobius_sieve(limit):
    """Compute Mobius function."""
    sp = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if sp[i] == 0:
            for j in range(i, limit + 1, i):
                if sp[j] == 0:
                    sp[j] = i
    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        p = sp[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]
    return mu


def mertens_at(n, mu):
    """M(n) = Σ_{k=1}^{n} μ(k)."""
    return sum(mu[1:n+1])


def main():
    print("=" * 80)
    print("R(11) BYPASS CHECK: Is R(11) the global minimum of R(p)?")
    print("=" * 80)
    print()

    # Phase 1: Exact computation for small primes
    EXACT_LIMIT = 200
    print(f"PHASE 1: EXACT Fraction arithmetic for primes p in [5, {EXACT_LIMIT}]")
    print("-" * 80)

    primes = sieve_primes(EXACT_LIMIT)
    primes_ge5 = [p for p in primes if p >= 5]

    mu = mobius_sieve(EXACT_LIMIT)

    results = []
    min_R = Fraction(1000)
    min_R_p = 0
    violations = []

    print(f"{'p':>5} {'M(p)':>5} {'R(p) exact':>25} {'R(p) float':>12} {'R > -1/2?':>10}")
    print("-" * 65)

    for p in primes_ge5:
        R_exact, crossTerm_val, shiftSqSum_val = compute_R_exact(p)
        if R_exact is None:
            continue

        M_p = mertens_at(p, mu)
        R_float = float(R_exact)
        is_gt_neg_half = R_exact > Fraction(-1, 2)

        results.append({
            'p': p, 'M_p': M_p,
            'R_exact': R_exact, 'R_float': R_float,
            'crossTerm': crossTerm_val, 'shiftSqSum': shiftSqSum_val,
            'gt_neg_half': is_gt_neg_half,
        })

        if R_exact < min_R:
            min_R = R_exact
            min_R_p = p

        if not is_gt_neg_half:
            violations.append(p)

        # Print for notable primes
        should_print = (p <= 50 or p == min_R_p or not is_gt_neg_half or
                        R_float < -0.15 or p in [97, 101, 127, 131, 149, 151, 191, 193, 197, 199])
        if should_print:
            print(f"{p:5d} {M_p:5d} {str(R_exact):>25s} {R_float:12.8f} {'YES' if is_gt_neg_half else '*** NO ***':>10}")

    elapsed1 = time.time() - start_time
    print()
    print(f"EXACT RESULTS (up to p={EXACT_LIMIT}, {elapsed1:.1f}s):")
    print(f"  Primes tested: {len(results)}")
    print(f"  min R(p) = {float(min_R):.10f} at p = {min_R_p}")
    print(f"  min R exact = {min_R}")
    print(f"  R(11) exact = {results[2]['R_exact'] if len(results) > 2 else 'N/A'}")
    print(f"  R > -1/2 violations: {len(violations)}")
    if violations:
        print(f"  Violation primes: {violations}")

    # Check: is min_R = R(11)?
    R_11 = None
    for r in results:
        if r['p'] == 11:
            R_11 = r['R_exact']
            break

    if R_11 is not None:
        print()
        if min_R_p == 11:
            print(f"  *** R(11) = {float(R_11):.10f} IS the minimum over all primes up to {EXACT_LIMIT} ***")
            print(f"  *** Proof would reduce to: verify R(11) = {R_11} > -1/2 ***")
            print(f"  *** Check: R(11) + 1/2 = {R_11 + Fraction(1,2)} = {float(R_11 + Fraction(1,2)):.10f} > 0? {'YES' if R_11 > Fraction(-1,2) else 'NO'} ***")
        else:
            print(f"  R(11) = {float(R_11):.10f} is NOT the minimum!")
            print(f"  min R(p) = {float(min_R):.10f} at p = {min_R_p}")
            print(f"  Difference: R({min_R_p}) - R(11) = {float(min_R - R_11):.10f}")

    # Phase 2: Float computation for larger primes
    print()
    print("=" * 80)
    FLOAT_LIMIT = 1000
    print(f"PHASE 2: Float arithmetic for primes p in [5, {FLOAT_LIMIT}]")
    print("-" * 80)

    primes_ext = sieve_primes(FLOAT_LIMIT)
    primes_ext_ge5 = [p for p in primes_ext if p >= 5]
    mu_ext = mobius_sieve(FLOAT_LIMIT)

    float_results = []
    min_R_float = float('inf')
    min_R_float_p = 0
    max_R_float = float('-inf')
    max_R_float_p = 0
    neg_R_count = 0
    violations_float = []

    for p in primes_ext_ge5:
        R = compute_R_float(p)
        if R is None:
            continue
        M_p = mertens_at(p, mu_ext)
        float_results.append({'p': p, 'R': R, 'M_p': M_p})

        if R < min_R_float:
            min_R_float = R
            min_R_float_p = p
        if R > max_R_float:
            max_R_float = R
            max_R_float_p = p
        if R < 0:
            neg_R_count += 1
        if R <= -0.5:
            violations_float.append((p, R))

    elapsed2 = time.time() - start_time

    print(f"  Primes tested: {len(float_results)}")
    print(f"  min R(p) = {min_R_float:.10f} at p = {min_R_float_p}")
    print(f"  max R(p) = {max_R_float:.10f} at p = {max_R_float_p}")
    print(f"  Negative R count: {neg_R_count} / {len(float_results)}")
    print(f"  R <= -1/2 violations: {len(violations_float)}")
    if violations_float:
        for pp, rr in violations_float[:10]:
            print(f"    p={pp}: R={rr:.10f}")

    # Phase 3: Trend analysis
    print()
    print("=" * 80)
    print("PHASE 3: TREND ANALYSIS — Does min R(p) decrease, stabilize, or oscillate?")
    print("-" * 80)

    # Track running minimum
    running_min = float('inf')
    running_min_p = 0
    milestones = [50, 100, 200, 300, 500, 750, 1000]
    milestone_idx = 0

    print(f"{'Range':>10} {'min R':>14} {'at p':>8} {'# neg R':>10}")
    print("-" * 50)

    neg_count = 0
    for r in float_results:
        if r['R'] < running_min:
            running_min = r['R']
            running_min_p = r['p']
        if r['R'] < 0:
            neg_count += 1

        if milestone_idx < len(milestones) and r['p'] >= milestones[milestone_idx]:
            print(f"  p<={milestones[milestone_idx]:5d} {running_min:14.10f}  p={running_min_p:5d}  {neg_count:8d}")
            milestone_idx += 1

    # Bottom 10 R values
    print()
    print("BOTTOM 10 R(p) values (most negative):")
    sorted_results = sorted(float_results, key=lambda x: x['R'])
    for r in sorted_results[:10]:
        print(f"  p={r['p']:5d}  M(p)={r['M_p']:4d}  R={r['R']:.10f}  1+2R={1+2*r['R']:.10f}")

    # Top 10 R values
    print()
    print("TOP 10 R(p) values (most positive):")
    sorted_desc = sorted(float_results, key=lambda x: -x['R'])
    for r in sorted_desc[:10]:
        print(f"  p={r['p']:5d}  M(p)={r['M_p']:4d}  R={r['R']:.10f}")

    # Phase 4: Correlation of R with M(p)
    print()
    print("=" * 80)
    print("PHASE 4: R(p) vs M(p) CORRELATION")
    print("-" * 80)

    # Group by M(p)
    from collections import defaultdict
    by_mertens = defaultdict(list)
    for r in float_results:
        by_mertens[r['M_p']].append(r['R'])

    print(f"{'M(p)':>5} {'count':>6} {'min R':>12} {'max R':>12} {'mean R':>12} {'all > -1/2?':>12}")
    print("-" * 70)
    for m in sorted(by_mertens.keys()):
        vals = by_mertens[m]
        mn = min(vals)
        mx = max(vals)
        mean = sum(vals) / len(vals)
        all_ok = all(v > -0.5 for v in vals)
        print(f"{m:5d} {len(vals):6d} {mn:12.8f} {mx:12.8f} {mean:12.8f} {'YES' if all_ok else 'NO':>12}")

    elapsed_total = time.time() - start_time

    # Phase 5: Try to go higher with float
    print()
    print("=" * 80)
    EXTENDED_LIMIT = 2000
    print(f"PHASE 5: Extended float to p = {EXTENDED_LIMIT}")
    print("-" * 80)

    primes_big = sieve_primes(EXTENDED_LIMIT)
    primes_big_ge5 = [p for p in primes_big if p > FLOAT_LIMIT]

    ext_min_R = min_R_float
    ext_min_R_p = min_R_float_p

    for i, p in enumerate(primes_big_ge5):
        R = compute_R_float(p)
        if R is not None and R < ext_min_R:
            ext_min_R = R
            ext_min_R_p = p
            print(f"  NEW MINIMUM: p={p}, R={R:.10f}")

        if (i + 1) % 50 == 0:
            elapsed = time.time() - start_time
            print(f"  [{elapsed:.1f}s] p={p}, running min R = {ext_min_R:.10f} at p={ext_min_R_p}")

    elapsed_final = time.time() - start_time
    print(f"\n  Extended range min R = {ext_min_R:.10f} at p = {ext_min_R_p}")
    print(f"  Total time: {elapsed_final:.1f}s")

    # ================================================================
    # FINAL SUMMARY
    # ================================================================
    print()
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print()
    print(f"  R(11) exact = {R_11}  = {float(R_11):.10f}")
    print(f"  R(11) + 1/2 = {R_11 + Fraction(1,2)}  > 0: {'YES' if R_11 > Fraction(-1,2) else 'NO'}")
    print()
    print(f"  Global min R(p) over p in [5, {EXTENDED_LIMIT}]:")
    print(f"    min R = {ext_min_R:.10f} at p = {ext_min_R_p}")
    print(f"    Is this R(11)? {'YES' if ext_min_R_p == 11 else 'NO'}")
    print()
    if ext_min_R_p == 11:
        print("  CONCLUSION: R(11) appears to be the global minimum.")
        print("  The proof WOULD reduce to a single verified computation:")
        print(f"    R(11) = {R_11} > -1/2")
        print(f"    Since {R_11} + 1/2 = {R_11 + Fraction(1,2)} > 0, QED.")
    else:
        print(f"  CONCLUSION: R({ext_min_R_p}) = {ext_min_R:.10f} < R(11) = {float(R_11):.10f}")
        print(f"  The R(11) bypass does NOT work as stated.")
        print(f"  But R > -1/2 still holds if {ext_min_R:.10f} > -0.5: {'YES' if ext_min_R > -0.5 else 'NO'}")
    print()
    print(f"  R > -1/2 violations in [5, {EXTENDED_LIMIT}]: {len(violations_float)}")
    print(f"  Total time: {elapsed_final:.1f}s")

    # Phase 6: Deep dive on violations
    print()
    print("=" * 80)
    print("PHASE 6: DETAILED VIOLATION ANALYSIS")
    print("-" * 80)

    # Recheck violations with exact arithmetic
    violation_primes = [5, 7, 11, 1399, 1409, 1423, 1427, 1429]
    mu_2k = mobius_sieve(2000)
    print("Exact check of problematic primes (exact for small, float for large):")
    for p in violation_primes:
        M_p = mertens_at(p, mu_2k)
        if p <= 200:
            R_ex, ct, ss = compute_R_exact(p)
            print(f"  p={p}: R = {R_ex} = {float(R_ex):.12f}, 1+2R = {float(1 + 2*R_ex):.12f}, M(p) = {M_p}")
        else:
            R_fl = compute_R_float(p)
            print(f"  p={p}: R = {R_fl:.12f} (float), 1+2R = {1+2*R_fl:.12f}, M(p) = {M_p}")

    # All primes with R < -0.3 in range
    print()
    print("All primes p <= 2000 with R(p) < -0.3:")
    all_big = sieve_primes(2000)
    all_big_ge5 = [p for p in all_big if p >= 5]
    mu_big = mobius_sieve(2000)
    neg_vals = []
    for p in all_big_ge5:
        R = compute_R_float(p)
        if R is not None and R < -0.3:
            M_p = mertens_at(p, mu_big)
            neg_vals.append((p, R, M_p))
            print(f"  p={p:5d}  M(p)={M_p:4d}  R={R:.10f}  1+2R={1+2*R:.10f}")

    # Save results
    return results, float_results, R_11, ext_min_R, ext_min_R_p


if __name__ == '__main__':
    results, float_results, R_11, ext_min_R, ext_min_R_p = main()
