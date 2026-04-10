#!/usr/bin/env python3
"""
Fast computation of alpha for Farey sequences F_N, N=1400..2000.

Key insight: R = sum f^2 - n/3 can be computed by denominator:
  R = 1/3 + sum_{q=2}^{N} e(q)
where e(q) = S_2(q)/q^2 - phi(q)/3 and S_2(q) = sum_{gcd(a,q)=1, 1<=a<=q-1} a^2.

For sum(D*f) and Cov(D,f), we need the actual Farey sequence ordering.
We use the mediant-based generation which is O(n) and very fast.

But with n~600K, even float arithmetic on all fractions is feasible.
"""

from math import gcd, sqrt
import sys
import time

def euler_phi(n):
    """Euler's totient function."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def S2_coprime(q):
    """Sum of a^2 for a in [1, q-1] with gcd(a, q) = 1."""
    s = 0
    for a in range(1, q):
        if gcd(a, q) == 1:
            s += a * a
    return s

def compute_R_by_denominator(N):
    """Compute R = sum f^2 - n/3 using denominator decomposition. Returns exact rational as float."""
    # R = 1/3 + sum_{q=2}^{N} [S_2(q)/q^2 - phi(q)/3]
    # Compute with high precision using floats (sufficient for our needs)
    R = 1.0/3.0
    for q in range(2, N+1):
        s2 = S2_coprime(q)
        ph = euler_phi(q)
        e_q = s2 / (q * q) - ph / 3.0
        R += e_q
    return R

def farey_next(a1, b1, a2, b2, N):
    """Given consecutive Farey fractions a1/b1 < a2/b2, find next fraction."""
    k = (N + b1) // b2
    return k * a2 - a1, k * b2 - b1

def compute_alpha_fast(N):
    """Compute alpha and related quantities using the mediant algorithm for Farey generation."""
    # Generate Farey sequence F_N using the standard algorithm
    # Start: 0/1, 1/N
    fracs = []  # list of (a, b) = a/b

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

    # Compute all needed sums using float arithmetic
    sum_f = 0.0
    sum_f2 = 0.0
    sum_Df = 0.0
    sum_D2 = 0.0

    for idx, (a, b) in enumerate(fracs):
        i = idx + 1  # 1-indexed rank
        f = a / b
        D = i - n * f
        sum_f += f
        sum_f2 += f * f
        sum_Df += D * f
        sum_D2 += D * D

    R = sum_f2 - n / 3.0
    E_D = (n + 1) / 2.0 - n * sum_f / n  # = (n+1)/2 - sum_f ... but sum_D = n(n+1)/2 - n*sum_f
    # Actually E_D = sum_D / n = [n(n+1)/2 - n*sum_f] / n = (n+1)/2 - sum_f
    # And E_f = sum_f / n = 1/2 (by symmetry)

    E_f = sum_f / n
    Cov_Df = sum_Df / n - ((n + 1) / 2.0 - sum_f) * E_f

    # Actually simpler: E[D] = sum_D/n, E[f] = 1/2
    sum_D = n * (n + 1) / 2.0 - n * sum_f
    E_D_val = sum_D / n
    Cov_Df2 = sum_Df / n - E_D_val * E_f

    Var_f = sum_f2 / n - E_f * E_f
    alpha = Cov_Df2 / Var_f if Var_f > 0 else None

    # Identity check terms
    term1 = 1.0 / (12 * n)
    term2 = -sum_D2 / (2.0 * n * n)
    term3 = -R / 2.0
    identity_cov = term1 + term2 + term3

    threshold = -n / 4.0

    return {
        'N': N,
        'n': n,
        'R': R,
        'sum_D2_over_2n2': sum_D2 / (2.0 * n * n),
        'term1': term1,
        'term2': term2,
        'term3': term3,
        'Cov': Cov_Df2,
        'identity_cov': identity_cov,
        'alpha': alpha,
        'sum_Df': sum_Df,
        'neg_n_over_4': threshold,
        'Df_above_threshold': sum_Df > threshold,
        'Var_f': Var_f,
        'sum_D': sum_D,
        'sum_D2': sum_D2,
    }

# First verify against known small values
print("VERIFICATION against exact values from proof document:")
print(f"{'N':>6} {'n':>8} {'R':>14} {'Cov':>14} {'alpha':>10}")
for N in [7, 13, 29, 53, 97]:
    d = compute_alpha_fast(N)
    print(f"{d['N']:>6} {d['n']:>8} {d['R']:>14.6f} {d['Cov']:>14.6f} {d['alpha']:>10.4f}")
sys.stdout.flush()

# Phase 1: Scan around N=1417
print("\n" + "=" * 110)
print("PHASE 1: R sign change scan (N = 1400 to 1430)")
print("=" * 110)
print(f"{'N':>6} {'n':>8} {'R':>14} {'-R/2':>14} {'-D2/2n2':>14} {'1/12n':>14} {'Cov':>14} {'alpha':>10} {'sum_Df':>14}")
print("-" * 110)

for N in range(1400, 1431):
    t0 = time.time()
    d = compute_alpha_fast(N)
    dt = time.time() - t0
    marker = " <-- R>0" if d['R'] > 0 else ""
    print(f"{d['N']:>6} {d['n']:>8} {d['R']:>14.8f} {d['term3']:>14.8f} {d['term2']:>14.8f} {d['term1']:>14.8f} {d['Cov']:>14.8f} {d['alpha']:>10.4f} {d['sum_Df']:>14.4f}{marker}  [{dt:.1f}s]")
    sys.stdout.flush()

# Phase 2: N = 1417 to 2000 (sample every 5th to keep runtime manageable)
print("\n" + "=" * 110)
print("PHASE 2: Alpha for N = 1417 to 2000 (every 5th N + all R>0 cases)")
print("=" * 110)
print(f"{'N':>6} {'n':>8} {'R':>14} {'Cov':>14} {'alpha':>10} {'sum_Df':>14} {'-n/4':>14} {'Df>-n/4':>7}")
print("-" * 110)

min_alpha = float('inf')
min_alpha_N = None
alpha_negative = []
R_positive_Ns = []
results_sampled = []

for N in range(1417, 2001):
    # Sample: every 5th, or near boundaries
    if N % 5 != 0 and N != 1417 and N != 2000:
        continue

    d = compute_alpha_fast(N)
    results_sampled.append(d)

    if d['alpha'] is not None and d['alpha'] < min_alpha:
        min_alpha = d['alpha']
        min_alpha_N = N

    if d['alpha'] is not None and d['alpha'] <= 0:
        alpha_negative.append(N)

    if d['R'] > 0:
        R_positive_Ns.append(N)

    marker = " <-- R>0" if d['R'] > 0 else ""
    print(f"{d['N']:>6} {d['n']:>8} {d['R']:>14.8f} {d['Cov']:>14.8f} {d['alpha']:>10.4f} {d['sum_Df']:>14.4f} {d['neg_n_over_4']:>14.4f} {'YES' if d['Df_above_threshold'] else 'NO':>7}{marker}")
    sys.stdout.flush()

print("\n" + "=" * 110)
print("SUMMARY")
print("=" * 110)
print(f"Range: N = 1417 to 2000 (sampled {len(results_sampled)} values)")
print(f"R positive at sampled N: {R_positive_Ns[:20]}...")
print(f"Alpha negative at sampled N: {alpha_negative}")
print(f"Minimum alpha: {min_alpha:.6f} at N = {min_alpha_N}")
print(f"sum(D*f) > -n/4 for ALL sampled: {all(d['Df_above_threshold'] for d in results_sampled)}")

# Phase 3: Detailed R > 0 analysis
if R_positive_Ns:
    print("\n" + "=" * 110)
    print(f"PHASE 3: R > 0 cases ({len(R_positive_Ns)} found)")
    print("=" * 110)
    print(f"{'N':>6} {'R':>14} {'|R|/2':>14} {'D2/(2n2)':>14} {'1/(12n)':>14} {'Cov':>14} {'Cov check':>14}")
    print("-" * 110)
    for d in results_sampled:
        if d['R'] > 0:
            print(f"{d['N']:>6} {d['R']:>14.10f} {abs(d['R'])/2:>14.10f} {d['sum_D2_over_2n2']:>14.10f} {d['term1']:>14.10f} {d['Cov']:>14.10f} {d['identity_cov']:>14.10f}")

# Phase 4: The alternative bound
print("\n" + "=" * 110)
print("PHASE 4: Alternative bound analysis")
print("=" * 110)
print("alpha > 0 iff Cov(D,f) > 0 iff sum(D*f)/n > E[D]*E[f] = (1/2)(1/2) = 1/4")
print("Actually: alpha > 0 iff sum(D*f) > n * E[D] * E[f]")
print()
print(f"{'N':>6} {'sum(D*f)':>14} {'n*ED*Ef':>14} {'margin':>14} {'margin/n':>14}")
print("-" * 70)
for d in results_sampled:
    if d['N'] % 50 == 0 or d['N'] == 1417 or d['R'] > 0:
        nEDEf = d['sum_D'] / d['n'] * (1.0/2.0) * d['n']  # = sum_D * 0.5
        # Actually n*E[D]*E[f] = n * (sum_D/n) * (1/2) = sum_D/2
        nEDEf = d['sum_D'] * 0.5
        margin = d['sum_Df'] - nEDEf
        print(f"{d['N']:>6} {d['sum_Df']:>14.4f} {nEDEf:>14.4f} {margin:>14.4f} {margin/d['n']:>14.8f}")
