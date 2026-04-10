#!/usr/bin/env python3
"""
Sweep ALL N from 7 to 2000 to find every N where alpha <= 0.
Also track where R > 0.
"""

from math import gcd
import sys
import time

def farey_next(a1, b1, a2, b2, N):
    k = (N + b1) // b2
    return k * a2 - a1, k * b2 - b1

def compute_alpha_fast(N):
    fracs = []
    a1, b1 = 0, 1
    a2, b2 = 1, N
    fracs.append((a1, b1))
    fracs.append((a2, b2))
    while not (a2 == 1 and b2 == 1):
        a3, b3 = farey_next(a1, b1, a2, b2, N)
        fracs.append((a3, b3))
        a1, b1 = a2, b2
        a2, b2 = a3, b3

    n = len(fracs)
    sum_f = 0.0
    sum_f2 = 0.0
    sum_Df = 0.0
    sum_D2 = 0.0

    for idx, (a, b) in enumerate(fracs):
        i = idx + 1
        f = a / b
        D = i - n * f
        sum_f += f
        sum_f2 += f * f
        sum_Df += D * f
        sum_D2 += D * D

    R = sum_f2 - n / 3.0
    E_f = sum_f / n
    sum_D = n * (n + 1) / 2.0 - n * sum_f
    E_D = sum_D / n
    Cov = sum_Df / n - E_D * E_f
    Var_f = sum_f2 / n - E_f * E_f
    alpha = Cov / Var_f if Var_f > 0 else None

    return N, n, R, Cov, alpha

# Sweep N = 7 to 2000
alpha_neg = []
R_pos = []

t0 = time.time()
for N in range(7, 2001):
    _, n, R, Cov, alpha = compute_alpha_fast(N)

    if R > 0:
        R_pos.append((N, n, R))

    if alpha is not None and alpha <= 0:
        alpha_neg.append((N, n, R, Cov, alpha))

    if N % 200 == 0:
        elapsed = time.time() - t0
        print(f"  Progress: N={N}, elapsed={elapsed:.1f}s", file=sys.stderr)
        sys.stderr.flush()

print("=" * 100)
print(f"ALL N in [7, 2000] where alpha <= 0:")
print("=" * 100)
print(f"{'N':>6} {'n':>8} {'R':>14} {'Cov':>14} {'alpha':>10}")
print("-" * 60)
for N, n, R, Cov, alpha in alpha_neg:
    print(f"{N:>6} {n:>8} {R:>14.8f} {Cov:>14.8f} {alpha:>10.6f}")

print(f"\nTotal: {len(alpha_neg)} values of N with alpha <= 0")

print("\n" + "=" * 100)
print(f"ALL N in [7, 2000] where R > 0:")
print("=" * 100)
print(f"{'N':>6} {'n':>8} {'R':>14}")
print("-" * 40)
for N, n, R in R_pos:
    print(f"{N:>6} {n:>8} {R:>14.8f}")

print(f"\nTotal: {len(R_pos)} values of N with R > 0")

# Check correlation: does alpha < 0 only when R > 0?
R_pos_set = set(x[0] for x in R_pos)
alpha_neg_set = set(x[0] for x in alpha_neg)
print(f"\nalpha <= 0 AND R > 0: {alpha_neg_set & R_pos_set}")
print(f"alpha <= 0 AND R <= 0: {alpha_neg_set - R_pos_set}")
print(f"R > 0 AND alpha > 0: {R_pos_set - alpha_neg_set}")
