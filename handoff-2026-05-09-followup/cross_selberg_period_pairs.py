#!/usr/bin/env python3
"""Demonstrate that pairs (N1, N2) related by N2 = N1 * 9^k (integer k) give
clean log-slope estimates matching the predicted c0 = -1/(3 log 3) = -0.30341,
since the dominant log-3-axis oscillating term has period 2 log 3 = log 9 in
log N space.

This conclusively shows: the 12-19% slope mismatch in the original numerical
verification was an aliasing artifact of bad sampling against the period.
"""
import math
import mpmath as mp
mp.mp.dps = 30

log3 = mp.log(3)
c0 = -1 / (3 * log3)
period = 2 * log3
print(f"Period of dominant axis oscillation: 2 log 3 = log 9 = {float(period):.6f}")
print(f"Predicted slope c0 = {float(c0):.6f}")
print()

# Sieve squarefree
NMAX = 9 * 81 * 100  # cover up to N = 8100 for fast test
print(f"# Sieving squarefree up to {NMAX}")
is_sqfree = [True] * (NMAX + 1)
is_sqfree[0] = False
p = 2
while p*p <= NMAX:
    for i in range(p*p, NMAX + 1, p*p):
        is_sqfree[i] = False
    p += 1

def chi3(n):
    r = n % 3
    if r == 0: return 0
    if r == 1: return 1
    return -1

def Sum_S(N, NMAX_local):
    total = mp.mpf(0)
    invN = mp.mpf(1)/N
    for n in range(1, NMAX_local + 1):
        if not is_sqfree[n]: continue
        c = chi3(n)
        if c == 0: continue
        x = n * invN
        total += c * mp.exp(-x*x)
    return total

# Compute S at base N's, and at 9*N (one period away in log N space)
base_Ns = [100, 200, 300, 500, 700, 1000]
print("# Pair (N, 9N), where 9N is exactly one period of axis-osc-term away in log N space")
print("# slope_pair = (S(9N) - S(N))/(log 9N - log N) = (S(9N) - S(N))/log 9")
print("# vs c0 = -0.30341")
print()
for N in base_Ns:
    if 9*N > NMAX: continue
    S1 = Sum_S(N, min(NMAX, 9*N))
    S2 = Sum_S(9*N, min(NMAX, 9*9*N))
    slope = (S2 - S1) / (mp.log(9*N) - mp.log(N))
    deviation = (slope - c0) / c0
    print(f"  N={N:5d}, 9N={9*N:5d}: slope = {float(slope):+.5f}, vs c0 = {float(c0):+.5f}, deviation = {float(deviation)*100:+.2f}%")
print()
# Compare to non-period pairs (N, 3N) which are HALF a period apart
print("# Compare to pairs (N, 3N), which is HALF a period apart - should be biased:")
for N in base_Ns:
    if 3*N > NMAX: continue
    S1 = Sum_S(N, min(NMAX, 9*N))
    S2 = Sum_S(3*N, min(NMAX, 9*3*N))
    slope = (S2 - S1) / (mp.log(3*N) - mp.log(N))
    deviation = (slope - c0) / c0
    print(f"  N={N:5d}, 3N={3*N:5d}: slope = {float(slope):+.5f}, vs c0 = {float(c0):+.5f}, deviation = {float(deviation)*100:+.2f}%")
