#!/usr/bin/env python3
"""
Compute alpha, Cov(D,f), R, and related quantities for Farey sequences F_N
for N = 1400 to 2000, using exact rational arithmetic.

Goal: Check if alpha > 0 even when R > 0 (which happens around N=1417).
Also compute sum(D*f) and check the bound sum(D*f) > -n/4.
"""

from fractions import Fraction
from math import gcd
import sys

def farey_sequence(N):
    """Generate Farey sequence F_N as list of Fraction objects, sorted."""
    fracs = set()
    for q in range(1, N+1):
        for a in range(0, q+1):
            if gcd(a, q) == 1:
                fracs.add(Fraction(a, q))
    return sorted(fracs)

def compute_alpha_data(N):
    """Compute all quantities for F_N using exact rational arithmetic."""
    F = farey_sequence(N)
    n = len(F)

    # Compute sums
    sum_f = sum(F)
    sum_f2 = sum(f*f for f in F)

    # R = sum f^2 - n/3
    R = sum_f2 - Fraction(n, 3)

    # Displacements D_i = i - n*f_i (using 0-indexed: D_i = (i+1) - n*f_i...
    # Actually standard: i goes from 1 to n, so D(f_i) = i - n*f_i
    sum_D = Fraction(0)
    sum_D2 = Fraction(0)
    sum_Df = Fraction(0)
    sum_i2 = Fraction(0)

    for idx, f in enumerate(F):
        i = idx + 1  # 1-indexed rank
        D = i - n * f
        sum_D += D
        sum_D2 += D * D
        sum_Df += D * f
        sum_i2 += Fraction(i*i, 1)

    # Cov(D, f) = (1/n) * sum(D*f) - E[D]*E[f]
    E_D = sum_D / n
    E_f = sum_f / n
    Cov_Df = sum_Df / n - E_D * E_f

    # Var(f)
    Var_f = sum_f2 / n - E_f * E_f

    # alpha = Cov(D,f) / Var(f)
    alpha = Cov_Df / Var_f if Var_f != 0 else None

    # Verify identity: Cov = 1/(12n) - sum_D2/(2n^2) - R/2
    term1 = Fraction(1, 12*n)
    term2 = -sum_D2 / (2 * n * n)
    term3 = -R / 2
    identity_cov = term1 + term2 + term3

    # Check: sum(D*f) > -n/4 ?
    threshold = Fraction(-n, 4)
    Df_above_threshold = sum_Df > threshold

    return {
        'N': N,
        'n': n,
        'R': R,
        'R_float': float(R),
        'sum_D2_over_2n2': float(sum_D2 / (2*n*n)),
        'term1': float(term1),
        'term2': float(term2),
        'term3': float(term3),
        'Cov': float(Cov_Df),
        'identity_cov': float(identity_cov),
        'alpha': float(alpha) if alpha is not None else None,
        'sum_Df': float(sum_Df),
        'neg_n_over_4': float(threshold),
        'Df_above_threshold': Df_above_threshold,
        'identity_check': abs(float(Cov_Df) - float(identity_cov)) < 1e-20,
    }

# First, scan around 1417 to find where R changes sign
print("=" * 100)
print("PHASE 1: Find where R changes sign (scan N = 1410 to 1425)")
print("=" * 100)
print(f"{'N':>6} {'n':>8} {'R':>14} {'Cov':>14} {'alpha':>10} {'sum_Df':>14} {'-n/4':>14} {'Df>-n/4':>8}")
print("-" * 100)

for N in range(1410, 1426):
    d = compute_alpha_data(N)
    print(f"{d['N']:>6} {d['n']:>8} {d['R_float']:>14.8f} {d['Cov']:>14.8f} {d['alpha']:>10.4f} {d['sum_Df']:>14.4f} {d['neg_n_over_4']:>14.4f} {'YES' if d['Df_above_threshold'] else 'NO':>8}")
    sys.stdout.flush()

# Phase 2: Compute for all N from 1417 to 2000 where R might be positive
# To keep runtime manageable, sample every 10th N plus key points
print("\n" + "=" * 100)
print("PHASE 2: Alpha for N = 1417 to 2000 (every N)")
print("=" * 100)
print(f"{'N':>6} {'n':>8} {'R':>14} {'-R/2':>14} {'-D2/2n2':>14} {'Cov':>14} {'alpha':>10} {'sum_Df':>14} {'-n/4':>14} {'OK':>4}")
print("-" * 100)

min_alpha = float('inf')
min_alpha_N = None
alpha_negative_count = 0
R_positive_count = 0
alpha_positive_when_R_positive = 0

results = []

for N in range(1417, 2001):
    d = compute_alpha_data(N)
    results.append(d)

    if d['alpha'] is not None and d['alpha'] < min_alpha:
        min_alpha = d['alpha']
        min_alpha_N = N

    if d['alpha'] is not None and d['alpha'] <= 0:
        alpha_negative_count += 1

    R_pos = d['R_float'] > 0
    if R_pos:
        R_positive_count += 1
        if d['alpha'] is not None and d['alpha'] > 0:
            alpha_positive_when_R_positive += 1

    # Print every 10th or when R changes sign or alpha is small
    if N % 25 == 0 or N <= 1425 or R_pos or (d['alpha'] is not None and d['alpha'] < 1.0):
        print(f"{d['N']:>6} {d['n']:>8} {d['R_float']:>14.8f} {d['term3']:>14.8f} {d['term2']:>14.8f} {d['Cov']:>14.8f} {d['alpha']:>10.4f} {d['sum_Df']:>14.4f} {d['neg_n_over_4']:>14.4f} {'OK' if d['Df_above_threshold'] else 'FAIL':>4}")
        sys.stdout.flush()

print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"Range: N = 1417 to 2000 ({len(results)} values)")
print(f"R positive count: {R_positive_count}")
print(f"Alpha negative count: {alpha_negative_count}")
print(f"Alpha positive when R > 0: {alpha_positive_when_R_positive} out of {R_positive_count}")
print(f"Minimum alpha: {min_alpha:.6f} at N = {min_alpha_N}")

# Phase 3: For the R > 0 cases, check what saves alpha
print("\n" + "=" * 100)
print("PHASE 3: Detailed analysis of R > 0 cases")
print("=" * 100)
print(f"{'N':>6} {'n':>8} {'R':>14} {'1/(12n)':>14} {'-D2/(2n2)':>14} {'-R/2':>14} {'Cov':>14} {'alpha':>10}")
print("-" * 100)

for d in results:
    if d['R_float'] > 0:
        print(f"{d['N']:>6} {d['n']:>8} {d['R_float']:>14.10f} {d['term1']:>14.10f} {d['term2']:>14.10f} {d['term3']:>14.10f} {d['Cov']:>14.10f} {d['alpha']:>10.6f}")

# Phase 4: Check the alternative criterion sum(D*f) > -n/4
print("\n" + "=" * 100)
print("PHASE 4: Alternative bound sum(D*f) > -n/4")
print("=" * 100)
all_Df_ok = all(d['Df_above_threshold'] for d in results)
print(f"sum(D*f) > -n/4 for ALL N in [1417,2000]: {all_Df_ok}")

# Find the ratio sum(D*f) / (-n/4) -- how far from the boundary
print(f"\n{'N':>6} {'sum(D*f)':>14} {'-n/4':>14} {'ratio':>10} {'margin':>14}")
print("-" * 70)
for d in results:
    if d['N'] % 50 == 0 or d['N'] == 1417:
        ratio = d['sum_Df'] / d['neg_n_over_4'] if d['neg_n_over_4'] != 0 else float('inf')
        margin = d['sum_Df'] - d['neg_n_over_4']
        print(f"{d['N']:>6} {d['sum_Df']:>14.4f} {d['neg_n_over_4']:>14.4f} {ratio:>10.4f} {margin:>14.4f}")
