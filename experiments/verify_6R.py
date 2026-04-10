#!/usr/bin/env python3
"""
Verify 6R(N) = 1 + sum_{m=1}^{N} M(floor(N/m))/m
at specific problematic N values.

Also verify that alpha ~ -6R(N) using an independent method.
"""

import sys

def compute_mobius_sieve(limit):
    """Compute mu and Mertens to limit."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    # smallest prime factor
    spf = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if spf[i] == 0:
            for j in range(i, limit + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    for n in range(2, limit + 1):
        p = spf[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]

    M = [0] * (limit + 1)
    s = 0
    for i in range(1, limit + 1):
        s += mu[i]
        M[i] = s
    return mu, M

def compute_6R(N, M):
    """Compute 6R(N) = 1 + sum_{m=1}^{N} M(floor(N/m))/m."""
    total = 0.0
    for m in range(1, N + 1):
        total += M[N // m] / m
    return 1.0 + total

# Check a few specific values
# First, verify at small N where we know the answer
N_check = 12  # p = 13
limit = max(570000, N_check)
print(f"Sieving to {limit}...")
mu, M = compute_mobius_sieve(limit)

print(f"\nVerification at N={N_check} (p=13):")
val = compute_6R(N_check, M)
print(f"  6R({N_check}) = {val:.6f}")
print(f"  alpha = {-val:.6f}")
print(f"  M({N_check}) = {M[N_check]}")

for N_check in [42, 70, 106, 178]:
    val = compute_6R(N_check, M)
    print(f"\nN={N_check} (p={N_check+1}): 6R = {val:.6f}, alpha = {-val:.6f}, M(N) = {M[N_check]}")

# Now check the problematic value N = 383982 (p = 383983)
# This is too large for Python direct sum in reasonable time
# But let's check N = 243798 (alpha claimed = 0.83)
N_check = 243798
print(f"\nComputing 6R({N_check})... (will take a while)")
val = compute_6R(N_check, M)
print(f"  6R({N_check}) = {val:.6f}")
print(f"  alpha = {-val:.6f}")
print(f"  M({N_check}) = {M[N_check]}")

# Check N = 383982 if within sieve limit
if 383982 <= limit:
    N_check = 383982
    print(f"\nComputing 6R({N_check})...")
    val = compute_6R(N_check, M)
    print(f"  6R({N_check}) = {val:.6f}")
    print(f"  alpha = {-val:.6f}")
    print(f"  M({N_check}) = {M[N_check]}")

# More importantly: check M(N) at these primes
for p in [243799, 383983, 384203, 565549, 567937]:
    if p - 1 <= limit:
        print(f"\np = {p}: M(p) = {M[p]}, M(p-1) = {M[p-1]}")
