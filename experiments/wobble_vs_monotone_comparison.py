#!/usr/bin/env python3
"""
CONNECTING MONOTONE FUNCTIONALS TO WOBBLE ANALYSIS
====================================================
Can I_k or L bound the wobble W or ΔW?

Key question: Is there an inequality W(N) <= f(I_k(N), ...) that helps?

Also: compute the growth rates of I_k and L to understand their utility.
"""

from fractions import Fraction
from math import gcd, log, sqrt
import numpy as np
import time

def farey_sequence(N):
    sequence = []
    a, b, c, d = 0, 1, 1, N
    sequence.append((a, b))
    while (c, d) != (1, 1) or not sequence:
        sequence.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
    sequence.append((1, 1))
    return sequence

def farey_bd_pairs(N):
    seq = farey_sequence(N)
    return [(seq[i][1], seq[i+1][1]) for i in range(len(seq)-1)]

def compute_wobble(N):
    seq = farey_sequence(N)
    n = len(seq)
    ideal = np.linspace(0, 1, n)
    fracs = np.array([p/q for p, q in seq])
    return float(np.sum((fracs - ideal)**2))

def compute_I2(N):
    return sum((b*d)**2 for b, d in farey_bd_pairs(N))

def compute_L(N):
    return sum(log(b*d) for b, d in farey_bd_pairs(N))

def mertens(N):
    """Compute M(N) = sum_{k=1}^N mu(k) via sieve."""
    mu = [0] * (N + 1)
    mu[1] = 1
    is_composite = [False] * (N + 1)
    primes = []
    for i in range(2, N + 1):
        if not is_composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N:
                break
            is_composite[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = 0
    result = []
    for k in range(1, N+1):
        M += mu[k]
        result.append(M)
    return result

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

MAX_N = 300

print("=" * 70)
print("GROWTH RATES OF MONOTONE FUNCTIONALS vs WOBBLE")
print("=" * 70)
print()

t0 = time.time()
M_vals = mertens(MAX_N)

print(f"{'N':>5}  {'W(N)':>14}  {'I_2(N)':>14}  {'L(N)':>10}  {'M(N)':>6}  dW")
print("-" * 70)

wobbles = []
I2_vals = []
L_vals = []
primes_with_violations = []

prev_W = None
for N in range(2, MAX_N+1):
    W = compute_wobble(N)
    I2 = compute_I2(N)
    L = compute_L(N)
    M = M_vals[N-1]
    
    wobbles.append(W)
    I2_vals.append(I2)
    L_vals.append(L)
    
    if N <= 30 or (is_prime(N) and N <= 100):
        dW = (W - prev_W) if prev_W is not None else 0
        marker = " <PRIME" if is_prime(N) else ""
        if is_prime(N) and prev_W is not None and W > prev_W:
            marker += " [VIOLATION]"
        print(f"{N:>5}  {W:>14.8f}  {I2:>14.1f}  {L:>10.4f}  {M:>6}  {dW:>+10.6f}{marker}")
    
    prev_W = W

print()
print("=" * 70)
print("QUESTION: Does I_2(N) / n^3 converge? (theoretical: ~N^3/3 asymptotically)")
print("=" * 70)
print()

for N in [50, 100, 150, 200, 250, 300]:
    seq = farey_sequence(N)
    n = len(seq)
    I2 = I2_vals[N-2]
    L = L_vals[N-2]
    W = wobbles[N-2]
    
    # I_2 = sum (bd)^2. For large N, sum_{b<=N} sum_{d: next to b} (bd)^2 ~ ?
    # Each b appears ~phi(b)/b times as a denominator. Average bd ~ N^2/2.
    # So I_2 ~ |F_N| * (N^2/4) ~ (3N^2/pi^2) * N^2/4 = 3N^4/(4pi^2)
    predicted_I2 = 3 * N**4 / (4 * np.pi**2)
    
    # L = sum log(bd). Average log(bd) ~ 2*log(N/2). |F_N| ~ 3N^2/pi^2.
    # So L ~ 3N^2/pi^2 * 2*log(N) = 6N^2*log(N)/pi^2
    predicted_L = 6 * N**2 * log(N) / np.pi**2
    
    # W: known asymptotics W(N) ~ N^2/(6*pi^2 * ...) -- not clear
    print(f"  N={N:3d}: I2={I2:.0f}  pred={predicted_I2:.0f}  ratio={I2/predicted_I2:.4f}  "
          f"L={L:.2f}  pred_L={predicted_L:.2f}  ratio_L={L/predicted_L:.4f}  "
          f"W={W:.6f}")

print()
print("=" * 70)
print("PROPOSED INEQUALITY: W(N) <= C * n * I_2(N)^{-1/2}")
print("=" * 70)
print()
print("Motivation: Cauchy-Schwarz gives")
print("  sum (f_j - ideal_j)^2 <= (sum 1/g_j^2)^{-1} * (sum displacement^2 * g_j^2 * ...)")
print()
print("Actually the Cauchy-Schwarz approach: is there a clean bound?")
print("  W(N) = sum delta_j^2 where delta_j = f_j - j/(n-1)")
print("  I_2 = sum (1/g_j)^2")
print("  Candidate: W(N) * I_2(N) >= (sum |delta_j| / g_j)^2  [C-S]")
print()

print("Computing W * I_2 and n^2 / 3 to look for a ratio:")
for N in [20, 50, 100, 200]:
    W = wobbles[N-2]
    I2 = I2_vals[N-2]
    n = len(farey_sequence(N))
    ratio = W * I2 / n**2
    print(f"  N={N}: W={W:.4e}  I2={I2:.2e}  W*I2={W*I2:.4e}  n={n}  W*I2/n^2={ratio:.6f}")

print()
print("=" * 70)
print("BOUNDING DeltaW(prime) IN TERMS OF MONOTONE FUNCTIONALS")
print("=" * 70)
print()
print("Key question: For prime p, can I_k(p) - I_k(p-1) serve as a proxy for DeltaW(p)?")
print()
print("If DeltaI_2(p) = sum_new_gaps (bd)^2 - old_gap^2 > 0 always, and")
print("DeltaW(p) = positive sometimes / negative other times,")
print("then the two are UNCORRELATED by any simple inequality.")
print()
print("But: DeltaI_2(p) depends on WHICH gaps split.")
print("  At prime p: all gaps involving b+d=p are split.")
print("  The fraction of all gaps that split ~ phi(p)/|F_{p-1}| ~ p/(3(p-1)^2/pi^2)")
print("  = pi^2/(3(p-1)) -> 0 as p -> infinity.")
print()
print("So at large prime p, only O(p) out of O(p^2) gaps are split,")
print("and the ones that split are exactly those with b+d=p.")

print()
print("Examining gap splits AT prime p:")
prev_pairs = set()
for p in [11, 13, 17, 19, 23, 29, 31, 37]:
    seq_p = farey_sequence(p)
    seq_p1 = farey_sequence(p-1)
    pairs_p = set(farey_bd_pairs(p))
    pairs_p1 = set(farey_bd_pairs(p-1))
    
    # New gaps in F_p that didn't exist in F_{p-1}
    new_gaps = pairs_p - pairs_p1
    split_gaps = []
    for (b1, d1) in new_gaps:
        # Find the parent gap
        if b1 + d1 == p:  # one of the children has b+d=p
            pass
    
    n_new = len(new_gaps)
    total_in_p1 = len(pairs_p1)
    total_in_p = len(pairs_p)
    
    W_p = compute_wobble(p)
    W_p1 = compute_wobble(p-1)
    dW = W_p - W_p1
    
    print(f"  p={p}: phi(p)={p-1}, gaps in F_{{p-1}}={total_in_p1}, "
          f"new_gaps_in_F_p={n_new}, DeltaW={dW:+.4e}  {'VIOLATION' if dW > 0 else ''}")

print()
print("=" * 70)
print("SUMMARY OF NEW THEOREMS")
print("=" * 70)
print()
print("THEOREM 1 (I_k Family). For ALL k > 0 and ALL N >= 2:")
print("  I_k(N) = sum_{consecutive Farey pairs a/b < c/d} (bd)^k")
print("is strictly increasing.")
print()
print("PROOF: Each step N->N+1 inserts mediants at pairs (b,d) with b+d=N+1,")
print("  replacing gap (bd)^k with (b(b+d))^k + (d(b+d))^k = (b+d)^k(b^k+d^k).")
print("  Delta = (b+d)^k(b^k+d^k) - (bd)^k >= 2^(k+1)*(bd)^k - (bd)^k > 0.")
print("  phi(N+1) >= 1 ensures at least one split.  QED.")
print()
print("THEOREM 2 (Log-Sum). L(N) = sum log(bd) is strictly increasing.")
print("PROOF: Delta L = 2*log(b+d) >= 2*log(2) > 0.  QED.")
print()
print("THEOREM 3 (J_k family). J_k(N) = sum (1/(bd))^k = sum g^k is")
print("  - strictly increasing for 0 < k < 1")
print("  - constant (=1) for k=1")
print("  - strictly decreasing for k > 1.")
print("PROOF: delta = g1^k+g2^k - (g1+g2)^k, sign determined by convexity of x^k.  QED.")
print()
print("CONTRAST WITH WOBBLE:")
print("  W(N) = sum (f_j - j/(n-1))^2 is NOT universally monotone.")
print("  W fails at primes p with M(p)/sqrt(p) > ~0.12 (empirical threshold).")
print("  No gap-functional analog exists for W because W measures GLOBAL alignment,")
print("  not LOCAL gap properties.")
print()
print(f"Time: {time.time()-t0:.1f}s")
