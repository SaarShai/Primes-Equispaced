#!/usr/bin/env python3
"""
Extended sweep: N = 2000 to 5000 (sampled) to find more alpha <= 0 cases.
Also deeper analysis of the N=1417,1418 cases.
"""

from math import gcd
import sys
import time

def farey_next(a1, b1, a2, b2, N):
    k = (N + b1) // b2
    return k * a2 - a1, k * b2 - b1

def compute_alpha_data(N):
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

    term1 = 1.0 / (12 * n)
    term2 = -sum_D2 / (2.0 * n * n)
    term3 = -R / 2.0

    return {
        'N': N, 'n': n, 'R': R, 'Cov': Cov, 'alpha': alpha,
        'sum_Df': sum_Df, 'sum_D2': sum_D2,
        'term1': term1, 'term2': term2, 'term3': term3,
    }

# Part 1: Detailed analysis of N=1417, 1418
print("=" * 100)
print("DETAILED ANALYSIS of N=1417, 1418")
print("=" * 100)
for N in [1416, 1417, 1418, 1419]:
    d = compute_alpha_data(N)
    print(f"\nN = {d['N']}, n = {d['n']}")
    print(f"  R = {d['R']:.10f}")
    print(f"  1/(12n)    = {d['term1']:.10f}")
    print(f"  -D2/(2n^2) = {d['term2']:.10f}")
    print(f"  -R/2       = {d['term3']:.10f}")
    print(f"  Cov(D,f)   = {d['Cov']:.10f}")
    print(f"  alpha      = {d['alpha']:.10f}")
    print(f"  sum(D*f)   = {d['sum_Df']:.4f}")
    print(f"  -n/4       = {-d['n']/4:.4f}")
    print(f"  sum(D*f) + n/4 = {d['sum_Df'] + d['n']/4:.4f}")
sys.stdout.flush()

# Part 2: What's special about N=1417?
# Is 1417 prime? What primes are near it?
def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

print("\n" + "=" * 100)
print("PRIMALITY near 1417:")
for N in range(1410, 1425):
    p = "PRIME" if is_prime(N) else ""
    print(f"  {N}: {p}")

# Part 3: Extended sweep N=2001 to 5000 (every 10th)
print("\n" + "=" * 100)
print("EXTENDED SWEEP: N = 2001 to 5000 (every 10th)")
print("=" * 100)

alpha_neg_ext = []
R_pos_ext = []
t0 = time.time()

for N in range(2001, 5001, 10):
    d = compute_alpha_data(N)

    if d['R'] > 0:
        R_pos_ext.append((N, d['n'], d['R'], d['alpha']))

    if d['alpha'] is not None and d['alpha'] <= 0:
        alpha_neg_ext.append((N, d['n'], d['R'], d['Cov'], d['alpha']))

    if N % 500 == 1:
        elapsed = time.time() - t0
        print(f"  Progress: N={N}, elapsed={elapsed:.1f}s", file=sys.stderr)
        sys.stderr.flush()

if alpha_neg_ext:
    print(f"\nalpha <= 0 cases found ({len(alpha_neg_ext)}):")
    for N, n, R, Cov, alpha in alpha_neg_ext:
        print(f"  N={N}: n={n}, R={R:.8f}, Cov={Cov:.8f}, alpha={alpha:.6f}")
else:
    print("\nNo alpha <= 0 cases found in [2001, 5000] (sampled every 10)")

if R_pos_ext:
    print(f"\nR > 0 cases found ({len(R_pos_ext)}):")
    for N, n, R, alpha in R_pos_ext[:30]:
        print(f"  N={N}: n={n}, R={R:.8f}, alpha={alpha:.6f}")
    if len(R_pos_ext) > 30:
        print(f"  ... and {len(R_pos_ext)-30} more")
else:
    print("\nNo R > 0 cases found in [2001, 5000] (sampled every 10)")

# Part 4: Analyze the e(q) contributions near 1417
print("\n" + "=" * 100)
print("DENOMINATOR CONTRIBUTION e(q) near q=1417")
print("=" * 100)

def euler_phi(n):
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
    s = 0
    for a in range(1, q):
        if gcd(a, q) == 1:
            s += a * a
    return s

# Compute cumulative R as function of N
print(f"{'N':>6} {'R(N)':>14} {'e(N)':>14} {'phi(N)':>8} {'prime?':>7}")
print("-" * 55)
R_cum = 1.0/3.0
for q in range(2, 1425):
    s2 = S2_coprime(q)
    ph = euler_phi(q)
    e_q = s2 / (q*q) - ph / 3.0
    R_cum += e_q
    if q >= 1410:
        p = "PRIME" if is_prime(q) else ""
        print(f"{q:>6} {R_cum:>14.8f} {e_q:>14.8f} {ph:>8} {p:>7}")
