#!/usr/bin/env python3
"""Verify D_new computation approach at p=13."""
from fractions import Fraction
from math import gcd

def farey_sequence(N):
    fracs = set()
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a,b) == 1:
                fracs.add(Fraction(a,b))
    return sorted(fracs)

p = 13
N = p - 1
F_N = farey_sequence(N)
F_p = farey_sequence(p)
n = len(F_N)
n_prime = len(F_p)

print(f"p={p}, N={N}, n={n}, n'={n_prime}")

# Method 1: Direct computation
D_new_direct = Fraction(0)
for k in range(1, p):
    f = Fraction(k, p)
    rank = sum(1 for g in F_p if g <= f) - 1
    D = Fraction(rank) - n_prime * f
    D_new_direct += D**2
    print(f"  k={k}: rank={rank}, D={float(D):.4f}, D^2={float(D**2):.4f}")

print(f"\nD_new (direct) = {float(D_new_direct):.6f}")

# Method 2: Merge walk (simulating the C code)
D_new_merge = Fraction(0)
# Walk through F_N in order, processing new fractions between consecutive entries
next_k = 1
rank_old = 0  # 0-indexed rank of current Farey fraction in F_N

for i in range(len(F_N)):
    f = F_N[i]
    # Process new fractions k/p < f (if next_k/p < f)
    while next_k < p and Fraction(next_k, p) < f:
        kp = Fraction(next_k, p)
        # N_{p-1}(k/p) = number of F_N fracs <= k/p
        # = rank_old (because k/p < f = F_N[rank_old], so all fracs up to F_N[rank_old-1] are <= k/p)
        # Wait: rank_old = i at this point.
        # F_N[0], ..., F_N[i-1] are < f. Since k/p < f too, and k/p is not in F_N,
        # N_{p-1}(k/p) = i  (= number of F_N fracs with value <= k/p,
        # which includes F_N[0]..F_N[i-1] since they're all < f, and we need to check
        # if any of F_N[0..i-1] > k/p)

        # Actually: N_{p-1}(k/p) = #{j: F_N[j] <= k/p}.
        # Since F_N is sorted and we know k/p < F_N[i], we have
        # N_{p-1}(k/p) = #{j < i: F_N[j] <= k/p}.
        # But F_N[i-1] might be > k/p or <= k/p.
        # We need a more careful count.
        N_pm1 = sum(1 for g in F_N if g <= kp)

        rank_in_Fp = N_pm1 + next_k - 1  # 0-indexed rank in F_p
        D_fp = rank_in_Fp - n_prime * kp
        D_new_merge += D_fp**2

        # What the C code would compute:
        # The C code uses rank_old + 1 as N_pm1 (when between F_N[rank_old] and F_N[rank_old+1])
        # But here we're processing BEFORE F_N[i], so we've already seen F_N[0..i-1]
        # rank_old here should be i (after incrementing for F_N[i-1])
        # Hmm, this is tricky. Let me trace more carefully.

        print(f"  NEW k={next_k}: N_pm1={N_pm1}, rank_Fp={rank_in_Fp}, D={float(D_fp):.4f}")
        print(f"    (C code would use rank_old+1 = {i}, same={N_pm1 == i})")
        next_k += 1

    # Process F_N[i] = f (if k/p == f, this is handled above since k/p not in F_N for prime p)

    rank_old = i  # not really used correctly here

# Handle remaining new fractions after last F_N entry
while next_k < p:
    kp = Fraction(next_k, p)
    N_pm1 = sum(1 for g in F_N if g <= kp)
    rank_in_Fp = N_pm1 + next_k - 1
    D_fp = rank_in_Fp - n_prime * kp
    D_new_merge += D_fp**2
    print(f"  NEW k={next_k} (after): N_pm1={N_pm1}, rank_Fp={rank_in_Fp}, D={float(D_fp):.4f}")
    next_k += 1

print(f"\nD_new (merge) = {float(D_new_merge):.6f}")
print(f"Match: {D_new_direct == D_new_merge}")
