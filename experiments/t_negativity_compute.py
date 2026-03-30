#!/usr/bin/env python3
"""
Compute T(N) = sum_{m=2}^{N} M(floor(N/m)) / m
for all N with M(N) = -2 (these give M(p) = -3 primes when N+1 = p is prime).

Also verify the identity: T(N) = sum_{k=1}^{N} mu(k) * H(floor(N/k)) - M(N)
                                = sum mu(k) H(floor(N/k)) + 2

And analyze the decomposition:
  T(N) = (log N + gamma) * M(N) - sum mu(k) log(k) + gamma*M(N) + error - M(N)
       = sum mu(k) H(floor(N/k)) + 2
"""

import sys
from math import log, gcd
from fractions import Fraction

def compute_mobius_sieve(limit):
    """Compute mu(n) for n = 0..limit using sieve."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    # Sieve of Eratosthenes variant
    is_prime = [True] * (limit + 1)
    primes = []
    for p in range(2, limit + 1):
        if is_prime[p]:
            primes.append(p)
            mu[p] = -1
        for j, q in enumerate(primes):
            if p * q > limit:
                break
            is_prime[p * q] = False
            if p % q == 0:
                mu[p * q] = 0
                break
            else:
                mu[p * q] = -mu[p]
    return mu

def compute_mertens(mu, limit):
    """Compute M(n) = sum_{k=1}^{n} mu(k) for n = 0..limit."""
    M = [0] * (limit + 1)
    for n in range(1, limit + 1):
        M[n] = M[n-1] + mu[n]
    return M

def harmonic(n):
    """Compute H(n) = sum_{k=1}^{n} 1/k as a float."""
    s = 0.0
    for k in range(1, n + 1):
        s += 1.0 / k
    return s

def main():
    LIMIT = 100000
    print(f"Computing mu and M up to {LIMIT}...")
    mu = compute_mobius_sieve(LIMIT)
    M = compute_mertens(mu, LIMIT)

    # Precompute harmonic numbers
    print("Precomputing harmonic numbers...")
    H = [0.0] * (LIMIT + 1)
    for n in range(1, LIMIT + 1):
        H[n] = H[n-1] + 1.0 / n

    # Find all N with M(N) = -2
    targets = []
    for N in range(2, LIMIT + 1):
        if M[N] == -2:
            targets.append(N)

    print(f"Found {len(targets)} values of N with M(N) = -2")

    # Among these, find which ones have N+1 prime (so M(N+1) = -3)
    is_prime = [False] * (LIMIT + 2)
    for p in range(2, LIMIT + 2):
        if p > LIMIT:
            break
        if all(p % d != 0 for d in range(2, int(p**0.5) + 1)):
            is_prime[p] = True

    # Compute T(N) for each target
    print("\n=== T(N) for M(N) = -2, where N+1 is prime (i.e., M(p) = -3 primes) ===")
    print(f"{'N':>8} {'p=N+1':>8} {'T(N)':>12} {'6R(N)':>12} {'T via muH':>12} {'max_T':>12}")

    max_T = -float('inf')
    count_positive = 0
    count_total = 0
    worst_N = None

    all_results = []

    for N in targets:
        # Method 1: T(N) = sum_{m=2}^{N} M(floor(N/m)) / m
        T1 = 0.0
        for m in range(2, N + 1):
            T1 += M[N // m] / m

        # Method 2: T(N) = sum_{k=1}^{N} mu(k) * H(floor(N/k)) - M(N)
        T2 = 0.0
        for k in range(1, N + 1):
            if mu[k] != 0:
                T2 += mu[k] * H[N // k]
        T2 -= M[N]  # = T2 + 2 since M(N) = -2

        sixR = -1.0 + T1  # 6R(N) = 1 + M(N) + T(N) = 1 - 2 + T(N) = -1 + T(N)

        is_p_prime = (N + 1 <= LIMIT and is_prime[N + 1])

        if is_p_prime:
            count_total += 1
            if T1 > max_T:
                max_T = T1
                worst_N = N
            if T1 >= 0:
                count_positive += 1
                print(f"*** POSITIVE T(N) at N={N}, p={N+1}: T={T1:.6f}")

            all_results.append((N, N+1, T1, sixR, T2))

            if count_total <= 30 or count_total % 50 == 0 or N <= 200:
                print(f"{N:>8} {N+1:>8} {T1:>12.6f} {sixR:>12.6f} {T2:>12.6f} {max_T:>12.6f}")

    print(f"\n=== Summary ===")
    print(f"Total M(p)=-3 primes checked: {count_total}")
    print(f"Positive T(N) count: {count_positive}")
    print(f"Worst (largest) T(N): {max_T:.6f} at N={worst_N}")

    # Also check ALL N with M(N) = -2 (not just where N+1 is prime)
    print(f"\n=== T(N) for ALL N with M(N) = -2 (not just prime N+1) ===")
    max_T_all = -float('inf')
    worst_N_all = None
    count_positive_all = 0
    count_total_all = 0

    for N in targets:
        T = 0.0
        for m in range(2, N + 1):
            T += M[N // m] / m

        count_total_all += 1
        if T > max_T_all:
            max_T_all = T
            worst_N_all = N
        if T >= 0:
            count_positive_all += 1
            if count_positive_all <= 20:
                print(f"  POSITIVE at N={N}: T={T:.6f}")

    print(f"Total N with M(N)=-2 checked: {count_total_all}")
    print(f"Positive T(N) count: {count_positive_all}")
    print(f"Worst T(N): {max_T_all:.8f} at N={worst_N_all}")

    # Detailed decomposition of T(N) for key cases
    print("\n=== Detailed decomposition for small N ===")
    for N in [12, 18, 42, 46, 52, 70, 106, 130, 172, 178]:
        if M[N] != -2:
            continue
        print(f"\nN = {N}, M(N) = {M[N]}")
        # Split at sqrt(N)
        sqrtN = int(N**0.5)
        T_low = 0.0  # m = 2..sqrtN
        T_high = 0.0  # m > sqrtN
        for m in range(2, sqrtN + 1):
            contrib = M[N // m] / m
            T_low += contrib
            print(f"  m={m}: M(floor({N}/{m})) = M({N//m}) = {M[N//m]}, contrib = {contrib:.6f}")
        for m in range(sqrtN + 1, N + 1):
            T_high += M[N // m] / m
        T_total = T_low + T_high
        print(f"  T_low (m<=sqrt(N)={sqrtN}): {T_low:.6f}")
        print(f"  T_high (m>sqrt(N)):  {T_high:.6f}")
        print(f"  T(N) total:          {T_total:.6f}")

    # Analyze the sum -sum mu(k) log(k)  (PNT-equivalent sum)
    print("\n=== PNT sum: -sum_{k=1}^{N} mu(k) log(k) ===")
    pnt_sum = [0.0] * (LIMIT + 1)
    for k in range(1, LIMIT + 1):
        pnt_sum[k] = pnt_sum[k-1] - mu[k] * log(k) if k > 0 else 0

    for N in [42, 100, 500, 1000, 5000, 10000, 50000, 100000]:
        if N <= LIMIT:
            ratio = pnt_sum[N] / N if N > 0 else 0
            print(f"  N={N:>6}: -sum mu(k)log(k) = {pnt_sum[N]:>12.4f}, ratio to N = {ratio:.6f}")

if __name__ == '__main__':
    main()
