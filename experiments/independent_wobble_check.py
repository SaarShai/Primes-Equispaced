#!/usr/bin/env python3
"""
INDEPENDENT VERIFICATION of the Wobble Sign Theorem claim.

Claim: For every prime p >= 11 with M(p) <= -3, W(p) > W(p-1),
i.e., W(p-1) - W(p) < 0.

Where:
  F_N = Farey sequence of order N (fractions a/b with 0 <= a <= b <= N, gcd(a,b)=1)
  |F_N| = number of elements in F_N
  For f in F_N: rank(f) = position of f in F_N (0-indexed)
  D(f) = rank(f) - |F_N| * f
  W(N) = sum of D(f)^2 / |F_N|^2  over all f in F_N

This script uses exact Fraction arithmetic throughout.

Author: Independent verification agent (no access to research agent's code)
"""

from fractions import Fraction
from math import gcd
import sympy

# ============================================================
# PART 1: Build Farey sequence from scratch
# ============================================================

def farey_sequence(N):
    """Generate Farey sequence F_N using the mediant property.
    Returns list of Fraction objects in ascending order."""
    # Standard algorithm: start with 0/1, 1/N (if N>=1), ..., 1/1
    # Use the next-term formula for Farey sequences
    fracs = []
    a, b = 0, 1
    c, d = 1, N
    fracs.append(Fraction(a, b))
    while c <= N:
        fracs.append(Fraction(c, d))
        # Next term formula: if a/b, c/d are consecutive in F_N,
        # then next = (k*c - a)/(k*d - b) where k = floor((N+b)/d)
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
    return fracs

def compute_W(N):
    """Compute W(N) = sum D(f)^2 / |F_N|^2 using exact arithmetic.
    Returns (W_exact as Fraction, list of D values, |F_N|)"""
    F = farey_sequence(N)
    size = len(F)
    size_frac = Fraction(size)

    D_values = []
    sum_D_sq = Fraction(0)

    for rank, f in enumerate(F):
        D = Fraction(rank) - size_frac * f
        D_values.append(D)
        sum_D_sq += D * D

    W = sum_D_sq / (size_frac * size_frac)
    return W, D_values, size

# ============================================================
# PART 2: Mertens function
# ============================================================

def mertens_function(n):
    """Compute M(n) = sum_{k=1}^{n} mu(k) using sympy."""
    M = 0
    for k in range(1, n+1):
        M += sympy.mobius(k)
    return M

# ============================================================
# PART 3: Compute and verify for target primes
# ============================================================

def main():
    print("=" * 80)
    print("INDEPENDENT VERIFICATION OF WOBBLE SIGN THEOREM")
    print("=" * 80)

    # Target primes with expected M(p) <= -3
    target_primes = [11, 13, 17, 19, 23, 29, 31, 37]

    # First, compute M(p) independently
    print("\n--- TASK 0: Verify Mertens values ---")
    mertens_cache = {}
    for p in target_primes + [1399]:
        M = mertens_function(p)
        mertens_cache[p] = M
        print(f"  M({p}) = {M}")

    # Check which primes actually have M(p) <= -3
    print("\n  Primes with M(p) <= -3:")
    mp_le_neg3 = [p for p in target_primes if mertens_cache[p] <= -3]
    print(f"  {mp_le_neg3}")
    mp_gt_neg3 = [p for p in target_primes if mertens_cache[p] > -3]
    if mp_gt_neg3:
        print(f"  Primes with M(p) > -3: {mp_gt_neg3}")

    # ============================================================
    print("\n--- TASK 1: Compute W(p-1) - W(p) for each prime ---")
    # ============================================================

    results = {}
    for p in target_primes:
        W_p, D_p, size_p = compute_W(p)
        W_pm1, D_pm1, size_pm1 = compute_W(p - 1)
        diff = W_pm1 - W_p  # W(p-1) - W(p)

        results[p] = {
            'W_p': W_p,
            'W_pm1': W_pm1,
            'diff': diff,
            'M_p': mertens_cache[p],
            'size_p': size_p,
            'size_pm1': size_pm1,
            'D_p': D_p,
            'D_pm1': D_pm1,
        }

        sign_str = "NEGATIVE (W(p)>W(p-1))" if diff < 0 else "POSITIVE (W(p)<W(p-1))" if diff > 0 else "ZERO"
        claim_holds = (diff < 0) if mertens_cache[p] <= -3 else "N/A (M(p) > -3)"

        print(f"\n  p={p}, M(p)={mertens_cache[p]}")
        print(f"    |F_{p}| = {size_p}, |F_{p-1}| = {size_pm1}")
        print(f"    W({p}) = {float(W_p):.10f}")
        print(f"    W({p-1}) = {float(W_pm1):.10f}")
        print(f"    W({p-1}) - W({p}) = {float(diff):.10f}  [{sign_str}]")
        print(f"    Claim holds: {claim_holds}")

    # Summary
    print("\n  === TASK 1 SUMMARY ===")
    all_pass = True
    for p in target_primes:
        r = results[p]
        if r['M_p'] <= -3:
            ok = r['diff'] < 0
            if not ok:
                all_pass = False
            print(f"  p={p}: M(p)={r['M_p']}, diff={float(r['diff']):.10f}, claim {'HOLDS' if ok else '*** FAILS ***'}")
        else:
            print(f"  p={p}: M(p)={r['M_p']} > -3 (not in scope)")

    print(f"\n  Overall TASK 1: {'ALL PASS' if all_pass else '*** FAILURES FOUND ***'}")

    # ============================================================
    print("\n--- TASK 2: Compute delta-squared sums ---")
    # ============================================================
    # delta(f) for f in F_p \ F_{p-1}: these are the NEW fractions added at order p
    # For a prime p, the new fractions are a/p for a = 1, 2, ..., p-1 with gcd(a,p)=1
    # Since p is prime, ALL a/p for a=1,...,p-1 are new.

    # But wait - what exactly is delta? Need to understand the decomposition.
    # Let me think about this from first principles.
    #
    # When going from F_{p-1} to F_p (p prime), we INSERT p-1 new fractions: a/p for a=1,...,p-1
    # Each insertion shifts ranks of subsequent elements.
    #
    # The "delta" for a new fraction a/p inserted at position j in F_p:
    # delta(a/p) = D_p(a/p) where D_p(f) = rank_p(f) - |F_p| * f
    # This is just the discrepancy of the new fraction in the new sequence.

    # Actually, let me compute delta^2 sum directly as sum of D^2 for NEW fractions only.

    print("\n  Computing sum of D^2 for NEW fractions (a/p) in F_p:")
    for p in target_primes:
        r = results[p]
        F_p = farey_sequence(p)
        size_p = len(F_p)

        # Find D values for new fractions a/p
        delta_sq_sum = Fraction(0)
        new_count = 0
        for rank, f in enumerate(F_p):
            if f.denominator == p:
                D = Fraction(rank) - Fraction(size_p) * f
                delta_sq_sum += D * D
                new_count += 1

        threshold = Fraction(35, 1000) * p * p  # 0.035 * p^2
        ratio = float(delta_sq_sum) / (p * p) if p > 0 else 0

        print(f"  p={p}: sum(delta^2) = {float(delta_sq_sum):.4f}, "
              f"0.035*p^2 = {float(threshold):.4f}, "
              f"ratio = {ratio:.6f}, "
              f"bound holds: {delta_sq_sum >= threshold}, "
              f"new_fracs: {new_count}")

    # ============================================================
    print("\n--- TASK 4: Check p=1399, M(p)=+8 ---")
    # ============================================================
    # This should be a case where the claim does NOT apply (M(p) > -3)
    # and potentially W(p-1) - W(p) > 0 (i.e., W decreases)

    p = 1399
    print(f"  M({p}) = {mertens_cache[p]}")
    if mertens_cache[p] > -3:
        print(f"  Confirmed: M({p}) > -3, so claim does not apply.")

    # Computing W for p=1399 takes a while, let's do it
    print(f"  Computing W({p}) and W({p-1})... (this may take a minute)")
    W_1399, _, size_1399 = compute_W(1399)
    W_1398, _, size_1398 = compute_W(1398)
    diff_1399 = W_1398 - W_1399
    print(f"  |F_1399| = {size_1399}, |F_1398| = {size_1398}")
    print(f"  W(1399) = {float(W_1399):.10f}")
    print(f"  W(1398) = {float(W_1398):.10f}")
    print(f"  W(1398) - W(1399) = {float(diff_1399):.10f}")
    if diff_1399 > 0:
        print(f"  CONFIRMED: W(1398) > W(1399), i.e. wobble DECREASES at p=1399")
        print(f"  This means the Sign Theorem correctly excludes this case (M(p)={mertens_cache[p]} > -3)")
    elif diff_1399 < 0:
        print(f"  W(1398) < W(1399), wobble INCREASES even though M(p) > -3")
        print(f"  This doesn't contradict the claim (claim is only about M(p)<=-3)")
    else:
        print(f"  W(1398) = W(1399) exactly")

    return results, mertens_cache

if __name__ == "__main__":
    results, mertens_cache = main()
