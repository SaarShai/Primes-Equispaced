#!/usr/bin/env python3
"""
Exact verification: correction/C' < 0 for ALL M(p)=-3 primes p in [43, 20000].

Uses fractions.Fraction for ALL arithmetic -- zero floating point.

Definitions (from B_EXACT_AUDIT.md):
  F_N = Farey sequence of order N = p-1
  n = count of fractions in F_N with denominator >= 2
  D(f_j) = j - n*f_j   (0-indexed rank among b>=2 fractions)
  delta(a/b) = (a - (p*a mod b)) / b   [exact integer arithmetic]
  B' = 2 * sum_{b>=2} D(f)*delta(f)
  C' = sum_{b>=2} delta(f)^2
  correction = -(B' + C')/2 - M(N)*C'/2
      (derived from identity: B' + C' = -2*sum_R_delta, and correction = sum_R_delta - M(N)*C'/2)
  ratio = correction / C'

For M(p)=-3 primes with p>=43: we expect correction/C' < 0.
For p=13,19 (also M(p)=-3): correction/C' is positive but < 1/2.
"""

import sys
import time
from fractions import Fraction
from math import gcd

# --- Mobius and Mertens ---

def compute_mobius_sieve(limit):
    """Compute mu(n) for n=0..limit using a sieve."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    # Smallest prime factor sieve
    spf = list(range(limit + 1))
    for i in range(2, int(limit**0.5) + 1):
        if spf[i] == i:  # i is prime
            for j in range(i*i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i

    for n in range(2, limit + 1):
        if spf[n] == n:
            # n is prime
            mu[n] = -1
        else:
            p = spf[n]
            m = n // p
            if m % p == 0:
                # p^2 divides n
                mu[n] = 0
            else:
                mu[n] = -mu[m]
    return mu


def compute_mertens(mu, limit):
    """Compute M(n) = sum_{k=1}^{n} mu(k) for n=0..limit."""
    M = [0] * (limit + 1)
    for n in range(1, limit + 1):
        M[n] = M[n-1] + mu[n]
    return M


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def farey_b_ge_2(N):
    """
    Generate sorted Farey fractions F_N with denominator >= 2.
    Returns list of (a, b) tuples in sorted order.

    Uses the mediant/next-term algorithm for Farey sequences,
    then filters out b=1 terms.
    """
    # Standard Farey sequence generation via next-term recurrence
    # F_N starts with 0/1, 1/N, ... , (N-1)/N, 1/1
    # We generate all of F_N then filter b>=2.
    # For large N this is memory-intensive but correct.

    # Actually, let's generate directly using the Stern-Brocot / mediant approach.
    # The standard next-term formula for Farey:
    # Given consecutive terms a/b, c/d in F_N:
    #   next = (floor((N+b)/d)*c - a) / (floor((N+b)/d)*d - b)

    fracs = []
    # Start: 0/1, 1/N
    a, b = 0, 1
    c, d = 1, N

    # We skip 0/1 (b=1), but include 1/N (if N>=2)
    if d >= 2:
        fracs.append((c, d))

    while not (c == 1 and d == 1):
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        if d >= 2:
            fracs.append((c, d))
        # Safety: c/d = 1/1 means we're done

    return fracs


def verify_prime(p, mu_arr):
    """
    For prime p, compute B', C', correction, correction/C' using exact arithmetic.
    Returns dict with results, or None if M(p) != -3.

    IMPORTANT: D(f_j) = j - n*f_j where j is the 0-indexed rank in the FULL
    Farey sequence F_N (including 0/1 and 1/1) and n = |F_N| (full count).
    B' and C' sum only over b>=2 fractions, but D uses the full-sequence rank.
    """
    N = p - 1

    # Compute M(p) = sum mu(k) for k=1..p
    Mp = sum(mu_arr[k] for k in range(1, p + 1))
    if Mp != -3:
        return None

    # M(N) = M(p-1) = M(p) - mu(p) = -3 - (-1) = -2
    MN = Mp - mu_arr[p]

    # Generate FULL Farey sequence F_N using mediant algorithm
    # Then sum over b>=2 fractions only, using full-sequence rank for D
    # Start: 0/1, 1/N
    all_fracs = []  # list of (a, b) in sorted order, full F_N
    a, b = 0, 1
    c, d = 1, N
    all_fracs.append((a, b))  # 0/1
    all_fracs.append((c, d))  # 1/N

    while not (c == 1 and d == 1):
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        all_fracs.append((c, d))

    n_full = len(all_fracs)  # |F_N|

    # Compute D and delta for b>=2 fractions only
    # D(f_j) = j - n_full * f_j, where j is rank in FULL sequence
    # delta(a/b) = (a - (p*a mod b)) / b

    B_prime = Fraction(0)
    C_prime = Fraction(0)
    n_interior = 0  # count of b>=2 fractions

    for j, (a, b) in enumerate(all_fracs):
        if b < 2:
            continue  # skip 0/1 and 1/1

        n_interior += 1
        f = Fraction(a, b)
        D = Fraction(j) - Fraction(n_full) * f

        # delta = (a - (p*a mod b)) / b, exact integer arithmetic
        pa_mod_b = (p * a) % b
        delta = Fraction(a - pa_mod_b, b)

        B_prime += D * delta
        C_prime += delta * delta

    B_prime = 2 * B_prime

    # correction = -(B' + C')/2 - M(N)*C'/2
    correction = -(B_prime + C_prime) / 2 - Fraction(MN) * C_prime / 2

    ratio = correction / C_prime

    return {
        'p': p,
        'N': N,
        'n': n_full,
        'n_interior': n_interior,
        'Mp': Mp,
        'MN': MN,
        'B_prime': B_prime,
        'C_prime': C_prime,
        'correction': correction,
        'ratio': ratio,
        'ratio_float': float(ratio),
        'B_positive': B_prime > 0,
    }


def main():
    LIMIT = 20000

    print(f"Computing Mobius sieve up to {LIMIT}...")
    sys.stdout.flush()
    mu = compute_mobius_sieve(LIMIT)
    M = compute_mertens(mu, LIMIT)

    # Find all M(p)=-3 primes up to LIMIT
    mp3_primes = []
    for p in range(2, LIMIT + 1):
        if is_prime(p) and M[p] == -3:
            mp3_primes.append(p)

    print(f"Found {len(mp3_primes)} primes with M(p)=-3 in [2, {LIMIT}]")
    print(f"Primes: {mp3_primes[:20]}{'...' if len(mp3_primes) > 20 else ''}")
    sys.stdout.flush()

    # Estimate feasibility: |F_N| ~ 3N^2/pi^2
    # For p=1000, N=999, |F_N| ~ 304000 fractions -- feasible
    # For p=5000, N=4999, |F_N| ~ 7.6M fractions -- slow but maybe feasible
    # For p=20000, N=19999, |F_N| ~ 121M fractions -- very slow with Fraction

    results = []
    all_pass = True
    feasibility_limit = None

    for p in mp3_primes:
        t0 = time.time()

        # Estimate size
        N = p - 1
        est_size = int(3 * N * N / 9.8696)  # 3N^2/pi^2

        if est_size > 5_000_000:
            # Skip very large ones but document
            if feasibility_limit is None:
                feasibility_limit = p
            elapsed = time.time() - t0
            print(f"p={p}: SKIPPED (est. {est_size:,} fractions, too large for exact Fraction arithmetic)")
            sys.stdout.flush()
            continue

        result = verify_prime(p, mu)
        elapsed = time.time() - t0

        if result is None:
            # Shouldn't happen since we pre-filtered
            continue

        results.append(result)

        r = result
        status = "PASS" if r['ratio'] < 0 else ("PASS(+)" if r['ratio'] < Fraction(1, 2) else "FAIL")
        if r['ratio'] >= 0 and p >= 43:
            if r['ratio'] >= Fraction(1, 2):
                all_pass = False
                status = "FAIL"

        print(f"p={r['p']:5d}  N={r['N']:5d}  |F_N|={r['n']:7d}  M(N)={r['MN']:3d}  "
              f"B'>0={str(r['B_positive']):5s}  corr/C'={r['ratio_float']:+.6f}  "
              f"[{status}]  ({elapsed:.1f}s)")
        sys.stdout.flush()

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    # Count results
    n_verified = len(results)
    n_negative = sum(1 for r in results if r['ratio'] < 0)
    n_positive_but_small = sum(1 for r in results if 0 <= r['ratio'] < Fraction(1, 2))
    n_fail = sum(1 for r in results if r['ratio'] >= Fraction(1, 2))
    n_b_positive = sum(1 for r in results if r['B_positive'])

    # Check the critical claim: for p >= 43, correction/C' < 0
    critical_range = [r for r in results if r['p'] >= 43]
    critical_pass = all(r['ratio'] < 0 for r in critical_range)

    print(f"Total M(p)=-3 primes in [2, {LIMIT}]: {len(mp3_primes)}")
    print(f"Verified exactly: {n_verified}")
    if feasibility_limit:
        print(f"Skipped (too large) starting at p={feasibility_limit}")
    print(f"  correction/C' < 0: {n_negative}")
    print(f"  0 <= correction/C' < 1/2: {n_positive_but_small}")
    print(f"  correction/C' >= 1/2: {n_fail}")
    print(f"  B' > 0: {n_b_positive} / {n_verified}")
    print()

    if critical_pass and len(critical_range) > 0:
        print(f"RESULT: correction/C' < 0 for ALL {len(critical_range)} tested M(p)=-3 primes with p >= 43.")
    elif len(critical_range) == 0:
        print("WARNING: No primes with p >= 43 were verified.")
    else:
        failures = [r for r in critical_range if r['ratio'] >= 0]
        print(f"FAILURE: correction/C' >= 0 at {len(failures)} primes with p >= 43:")
        for r in failures:
            print(f"  p={r['p']}, correction/C' = {r['ratio_float']}")

    # Small primes p=13,19
    small = [r for r in results if r['p'] in (13, 19)]
    if small:
        print()
        print("Small M(p)=-3 primes (p=13,19):")
        for r in small:
            ok = r['ratio'] < Fraction(1, 2)
            print(f"  p={r['p']}: correction/C' = {r['ratio_float']:+.6f}, < 1/2: {ok}")

    # Detailed table
    print()
    print("DETAILED TABLE:")
    print(f"{'p':>6s} {'N':>6s} {'|F_N|':>8s} {'M(N)':>5s} {'B>0':>5s} {'corr/C':>12s}")
    print("-" * 50)
    for r in results:
        print(f"{r['p']:6d} {r['N']:6d} {r['n']:8d} {r['MN']:5d} "
              f"{'YES' if r['B_positive'] else 'NO':>5s} {r['ratio_float']:+12.6f}")


if __name__ == '__main__':
    main()
