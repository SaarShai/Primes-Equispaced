#!/usr/bin/env python3
"""
INDEPENDENT VERIFICATION - Part 2
Four-term decomposition and broad scan of M(p) <= -3 primes.
"""

from fractions import Fraction
from math import gcd
import sympy

def farey_sequence(N):
    """Generate Farey sequence F_N."""
    fracs = []
    a, b = 0, 1
    c, d = 1, N
    fracs.append(Fraction(a, b))
    while c <= N:
        fracs.append(Fraction(c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
    return fracs

def compute_W_and_details(N):
    """Compute W(N) and return detailed information."""
    F = farey_sequence(N)
    size = len(F)
    sum_D_sq = Fraction(0)
    D_map = {}  # fraction -> D value
    for rank, f in enumerate(F):
        D = Fraction(rank) - Fraction(size) * f
        D_map[f] = D
        sum_D_sq += D * D
    W = sum_D_sq / (Fraction(size) ** 2)
    return W, D_map, size, set(F)

def mertens_sieve(limit):
    """Compute Mertens function values up to limit using a sieve for mu."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    # Sieve of Eratosthenes variant for Mobius function
    is_prime = [True] * (limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1  # prime => mu = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]

    # Compute running sum M(n) = sum mu(k) for k=1..n
    M = [0] * (limit + 1)
    running = 0
    for n in range(1, limit + 1):
        running += mu[n]
        M[n] = running
    return M

# ============================================================
# PART 3: Four-term decomposition verification
# ============================================================

def verify_decomposition(p):
    """
    Verify the four-term decomposition for prime p.

    When going from F_{p-1} to F_p, new fractions a/p (a=1,...,p-1) are inserted.
    Let's derive what W(p-1) - W(p) equals in terms of the changes.

    W(N) = (1/|F_N|^2) * sum_{f in F_N} D_N(f)^2
    where D_N(f) = rank_N(f) - |F_N| * f

    For the old fractions (those in both F_{p-1} and F_p):
    - Their rank in F_p increases by the number of new fractions inserted before them
    - The normalization |F_p| != |F_{p-1}|

    Let's just compute each term directly and check if a decomposition makes sense.
    """
    W_p, D_p_map, size_p, set_p = compute_W_and_details(p)
    W_pm1, D_pm1_map, size_pm1, set_pm1 = compute_W_and_details(p - 1)

    # New fractions: those in F_p but not in F_{p-1}
    new_fracs = set_p - set_pm1
    old_fracs = set_p & set_pm1  # should equal set_pm1

    assert old_fracs == set_pm1, "Old fractions should be exactly F_{p-1}"
    assert len(new_fracs) == p - 1, f"Expected {p-1} new fractions, got {len(new_fracs)}"

    # Decompose sum D_p^2 into contributions from old and new fractions
    sum_D_sq_old_in_p = Fraction(0)
    sum_D_sq_new_in_p = Fraction(0)

    for f in old_fracs:
        sum_D_sq_old_in_p += D_p_map[f] ** 2
    for f in new_fracs:
        sum_D_sq_new_in_p += D_p_map[f] ** 2

    total_D_sq_p = sum_D_sq_old_in_p + sum_D_sq_new_in_p

    # Also compute sum D_{p-1}^2
    sum_D_sq_pm1 = Fraction(0)
    for f in set_pm1:
        sum_D_sq_pm1 += D_pm1_map[f] ** 2

    # W(p-1) - W(p) = sum_D_sq_pm1 / size_pm1^2 - total_D_sq_p / size_p^2
    diff_exact = sum_D_sq_pm1 / Fraction(size_pm1**2) - total_D_sq_p / Fraction(size_p**2)

    # Now let's try to understand the "A, B, C, D" decomposition.
    # A natural decomposition:
    #
    # W(p-1) - W(p) = [sum D_{p-1}(f)^2 / |F_{p-1}|^2] - [sum D_p(f)^2 / |F_p|^2]
    #
    # = (1/|F_{p-1}|^2) sum_{old} D_{p-1}(f)^2
    #   - (1/|F_p|^2) [sum_{old} D_p(f)^2 + sum_{new} D_p(f)^2]
    #
    # Let's define:
    #   C' = (1/|F_p|^2) * sum_{new} D_p(f)^2   (contribution of new fractions, always >= 0)
    #
    # Then W(p-1) - W(p) = [sum_{old} D_{p-1}^2 / |F_{p-1}|^2 - sum_{old} D_p^2 / |F_p|^2] - C'
    #
    # The first bracket is the "old fraction" contribution.

    C_prime = sum_D_sq_new_in_p / Fraction(size_p**2)

    old_contribution = sum_D_sq_pm1 / Fraction(size_pm1**2) - sum_D_sq_old_in_p / Fraction(size_p**2)

    # Verify: W(p-1) - W(p) = old_contribution - C_prime
    check = old_contribution - C_prime
    assert check == diff_exact, f"Decomposition check failed: {float(check)} != {float(diff_exact)}"

    # For the claim to hold (diff < 0), we need C_prime > old_contribution
    # i.e., the new fractions' contribution must overwhelm the old fraction changes.

    # The "delta^2" sum from Task 2 is sum_D_sq_new_in_p (unnormalized)
    delta_sq_sum = sum_D_sq_new_in_p
    threshold = Fraction(35, 1000) * p * p

    return {
        'p': p,
        'diff': diff_exact,
        'C_prime': C_prime,
        'C_prime_unnorm': delta_sq_sum,
        'old_contribution': old_contribution,
        'size_p': size_p,
        'size_pm1': size_pm1,
        'delta_sq_sum': delta_sq_sum,
        'threshold_0035': threshold,
        'delta_sq_ge_threshold': delta_sq_sum >= threshold,
    }


def main():
    print("=" * 80)
    print("PART 2: FOUR-TERM DECOMPOSITION & BROAD SCAN")
    print("=" * 80)

    # ============================================================
    print("\n--- TASK 3: Verify decomposition for small primes ---")
    # ============================================================

    target_primes = [13, 19, 31]  # The M(p) <= -3 primes from our list

    for p in target_primes:
        r = verify_decomposition(p)
        print(f"\n  p={p}:")
        print(f"    W(p-1) - W(p) = {float(r['diff']):.12f}")
        print(f"    C' (new frac contribution, normalized) = {float(r['C_prime']):.12f}")
        print(f"    old_contribution = {float(r['old_contribution']):.12f}")
        print(f"    Check: old_contrib - C' = {float(r['old_contribution'] - r['C_prime']):.12f} == diff? {r['old_contribution'] - r['C_prime'] == r['diff']}")
        print(f"    For claim: need C' > old_contrib: {r['C_prime'] > r['old_contribution']}")
        print(f"    delta_sq_sum = {float(r['delta_sq_sum']):.4f}, threshold 0.035*p^2 = {float(r['threshold_0035']):.4f}, holds: {r['delta_sq_ge_threshold']}")

    # Also check non-M(p)<=-3 primes to see the pattern
    print("\n  --- Also checking primes with M(p) > -3: ---")
    for p in [11, 17, 23, 29, 37]:
        r = verify_decomposition(p)
        M_p = sum(sympy.mobius(k) for k in range(1, p+1))
        print(f"  p={p}, M(p)={M_p}: diff={float(r['diff']):.12f}, C'={float(r['C_prime']):.12f}, old={float(r['old_contribution']):.12f}")

    # ============================================================
    print("\n--- TASK 5: Broad scan of M(p) <= -3 primes ---")
    # ============================================================

    LIMIT = 3000
    print(f"  Scanning all primes up to {LIMIT}...")
    M_vals = mertens_sieve(LIMIT)

    # Find all primes with M(p) <= -3
    primes_mp_le_neg3 = []
    for n in range(2, LIMIT + 1):
        if sympy.isprime(n) and M_vals[n] <= -3:
            primes_mp_le_neg3.append(n)

    print(f"  Found {len(primes_mp_le_neg3)} primes with M(p) <= -3 up to {LIMIT}")
    print(f"  First 20: {primes_mp_le_neg3[:20]}")

    # Check every one
    failures = []
    all_checked = 0
    for p in primes_mp_le_neg3:
        W_p_fracs = farey_sequence(p)
        W_pm1_fracs = farey_sequence(p - 1)

        size_p = len(W_p_fracs)
        size_pm1 = len(W_pm1_fracs)

        sum_Dsq_p = Fraction(0)
        for rank, f in enumerate(W_p_fracs):
            D = Fraction(rank) - Fraction(size_p) * f
            sum_Dsq_p += D * D

        sum_Dsq_pm1 = Fraction(0)
        for rank, f in enumerate(W_pm1_fracs):
            D = Fraction(rank) - Fraction(size_pm1) * f
            sum_Dsq_pm1 += D * D

        W_p = sum_Dsq_p / Fraction(size_p ** 2)
        W_pm1 = sum_Dsq_pm1 / Fraction(size_pm1 ** 2)
        diff = W_pm1 - W_p

        all_checked += 1
        if diff >= 0:
            failures.append((p, M_vals[p], float(diff)))
            print(f"  *** FAILURE at p={p}, M(p)={M_vals[p]}, diff={float(diff):.12e} ***")

        if all_checked % 20 == 0:
            print(f"  ... checked {all_checked}/{len(primes_mp_le_neg3)} primes so far, {len(failures)} failures")

    print(f"\n  === TASK 5 RESULTS ===")
    print(f"  Checked {all_checked} primes with M(p) <= -3 up to {LIMIT}")
    print(f"  Failures: {len(failures)}")
    if failures:
        print(f"  Failed primes: {failures}")
    else:
        print(f"  ALL PASSED - claim holds for every M(p) <= -3 prime up to {LIMIT}")

    # ============================================================
    print("\n--- TASK 5b: Check if claim fails for some M(p) > -3 primes ---")
    # ============================================================
    # This tells us whether M(p) <= -3 is the RIGHT threshold

    primes_mp_gt_neg3 = []
    for n in range(11, min(500, LIMIT + 1)):
        if sympy.isprime(n) and M_vals[n] > -3:
            primes_mp_gt_neg3.append(n)

    wobble_increases_despite_mp_gt_neg3 = []
    wobble_decreases = []

    for p in primes_mp_gt_neg3:
        W_p_fracs = farey_sequence(p)
        W_pm1_fracs = farey_sequence(p - 1)
        size_p = len(W_p_fracs)
        size_pm1 = len(W_pm1_fracs)

        sum_Dsq_p = Fraction(0)
        for rank, f in enumerate(W_p_fracs):
            D = Fraction(rank) - Fraction(size_p) * f
            sum_Dsq_p += D * D

        sum_Dsq_pm1 = Fraction(0)
        for rank, f in enumerate(W_pm1_fracs):
            D = Fraction(rank) - Fraction(size_pm1) * f
            sum_Dsq_pm1 += D * D

        W_p = sum_Dsq_p / Fraction(size_p ** 2)
        W_pm1 = sum_Dsq_pm1 / Fraction(size_pm1 ** 2)
        diff = W_pm1 - W_p

        if diff < 0:
            wobble_increases_despite_mp_gt_neg3.append((p, M_vals[p], float(diff)))
        else:
            wobble_decreases.append((p, M_vals[p], float(diff)))

    print(f"  Checked {len(primes_mp_gt_neg3)} primes with M(p) > -3 in [11, 500)")
    print(f"  Wobble still INCREASES (diff < 0): {len(wobble_increases_despite_mp_gt_neg3)}")
    print(f"  Wobble DECREASES (diff >= 0): {len(wobble_decreases)}")
    if wobble_decreases:
        print(f"  First 10 where wobble decreases:")
        for p, mp, d in wobble_decreases[:10]:
            print(f"    p={p}, M(p)={mp}, diff={d:.12e}")
    if wobble_increases_despite_mp_gt_neg3:
        print(f"  Note: wobble increases for M(p)>-3 too, e.g.:")
        for p, mp, d in wobble_increases_despite_mp_gt_neg3[:10]:
            print(f"    p={p}, M(p)={mp}, diff={d:.12e}")

    return failures, wobble_decreases


if __name__ == "__main__":
    failures, decreases = main()
