#!/usr/bin/env python3
"""
Part 2: Deeper investigation of the S_b sign structure and alternative bounds.

Key finding from Part 1: |S|/sqrt(V/12) GROWS, so the random permutation model fails.
The S_b values are coherently negative (not random-signed).

New approach: Since S = -Sigma U_b and Sigma T_b = 0, we have S = Sigma S_b = Sigma (T_b - U_b).
The issue is that S_b = T_b - U_b, and T_b values cancel (sum = 0) but U_b values also
roughly cancel, leaving S as the difference of two near-zero sums.

ALTERNATIVE BOUND: Instead of bounding |S| directly, bound |rho| = 2|S|/C' using
the identity rho = 2*corr(D_err, delta)*R where R = ||D_err||/||delta||.

But we already know this approach gives |rho| ~ 2 * |corr| * sqrt(N), which is bad
unless |corr| decays as 1/sqrt(N).

NEW IDEA: Bound |S| using Cauchy-Schwarz PER DENOMINATOR and then exploit the
STRUCTURE of V_b (how D_err^2 distributes across denominators).

|S| = |Sigma_b S_b| <= Sigma_b |S_b| <= Sigma_b sqrt(V_b * W_b)

By CS on the outer sum:
(Sigma sqrt(V_b * W_b))^2 <= (Sigma V_b) * (Sigma W_b) = V * C'

So |S| <= sqrt(V * C'), giving |rho| <= 2*sqrt(V*C')/C' = 2*sqrt(V/C') = 2*R.

This is the trivial Cauchy-Schwarz bound: |rho| <= 2*R ~ 2*sqrt(N).

To improve, we need to exploit that V_b and W_b are NOT independent -- they have
OPPOSITE scaling with b:
  - V_b ~ n*c/b (D_err variance per-denominator, LARGE for small b)
  - W_b ~ phi(b)/12 * (b^2/b^2) ... actually W_b = sum delta^2 for denom b

Let me check the actual scaling of V_b and W_b.

Also: try the WEIGHTED Cauchy-Schwarz with optimal weights.
"""

from fractions import Fraction
from math import gcd, log, sqrt, pi
import sys

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    d = 5
    while d * d <= n:
        if n % d == 0 or (n + 2) % d == 0: return False
        d += 6
    return True

def mobius(n):
    if n == 1: return 1
    temp = n; d = 2; factors = 0
    while d * d <= temp:
        if temp % d == 0:
            factors += 1; temp //= d
            if temp % d == 0: return 0
        d += 1
    if temp > 1: factors += 1
    return (-1) ** factors

def mertens(N):
    return sum(mobius(k) for k in range(1, N+1))

def analyze_deep(p):
    """Deep per-denominator analysis."""
    N = p - 1

    # Build Farey sequence
    fracs = []
    for b in range(2, N + 1):
        for a in range(1, b):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: Fraction(x[0], x[1]))
    n = len(fracs)

    # Compute D, delta
    D_vals = []
    f_vals = []
    for j, (a, b) in enumerate(fracs):
        f = Fraction(a, b)
        D = Fraction(j) - n * f
        D_vals.append(D)
        f_vals.append(f)

    delta_vals = []
    for a, b in fracs:
        sigma = (p * a) % b
        delta_vals.append(Fraction(a - sigma, b))

    # OLS
    mean_f = sum(f_vals) / n
    mean_D = sum(D_vals) / n
    cov_Df = sum((D - mean_D) * (f - mean_f) for D, f in zip(D_vals, f_vals)) / n
    var_f = sum((f - mean_f)**2 for f in f_vals) / n
    alpha = cov_Df / var_f
    D_err = [D - mean_D - alpha * (f - mean_f) for D, f in zip(D_vals, f_vals)]

    C_prime = sum(d**2 for d in delta_vals)
    S = sum(de * d for de, d in zip(D_err, delta_vals))
    rho = 2 * S / C_prime

    # Per-denominator
    by_denom = {}
    for idx, (a, b) in enumerate(fracs):
        if b not in by_denom:
            by_denom[b] = []
        by_denom[b].append(idx)

    # Collect V_b, W_b, S_b data
    b_list = sorted(by_denom.keys())
    V_b_list = []
    W_b_list = []
    S_b_list = []
    phi_b_list = []

    for b in b_list:
        indices = by_denom[b]
        phi_b = len(indices)
        V_b = float(sum(D_err[i]**2 for i in indices))
        W_b = float(sum(delta_vals[i]**2 for i in indices))
        S_b = float(sum(D_err[i] * delta_vals[i] for i in indices))
        V_b_list.append(V_b)
        W_b_list.append(W_b)
        S_b_list.append(S_b)
        phi_b_list.append(phi_b)

    # How many S_b are positive vs negative?
    n_pos = sum(1 for s in S_b_list if s > 0)
    n_neg = sum(1 for s in S_b_list if s < 0)
    n_zero = sum(1 for s in S_b_list if s == 0)
    sum_pos = sum(s for s in S_b_list if s > 0)
    sum_neg = sum(s for s in S_b_list if s < 0)

    print(f"\np={p}: S_b signs: {n_pos} pos, {n_neg} neg, {n_zero} zero")
    print(f"  sum(pos S_b) = {sum_pos:.2f}, sum(neg S_b) = {sum_neg:.2f}")
    print(f"  net S = {sum_pos + sum_neg:.2f}, cancellation ratio = {abs(sum_pos + sum_neg)/(sum_pos - sum_neg):.4f}")

    # V_b/phi_b scaling with b
    print(f"\n  Scaling of V_b/phi_b and W_b/phi_b with b:")
    # Group by b ranges
    small_b = [i for i, b in enumerate(b_list) if b <= N//4]
    mid_b = [i for i, b in enumerate(b_list) if N//4 < b <= 3*N//4]
    large_b = [i for i, b in enumerate(b_list) if b > 3*N//4]

    for label, group in [("small", small_b), ("mid", mid_b), ("large", large_b)]:
        if not group:
            continue
        avg_Vphi = sum(V_b_list[i]/phi_b_list[i] for i in group) / len(group)
        avg_Wphi = sum(W_b_list[i]/phi_b_list[i] for i in group) / len(group) if any(phi_b_list[i] > 0 for i in group) else 0
        avg_Sphi = sum(S_b_list[i]/phi_b_list[i] for i in group) / len(group)
        total_V = sum(V_b_list[i] for i in group)
        total_W = sum(W_b_list[i] for i in group)
        total_S = sum(S_b_list[i] for i in group)
        print(f"    {label:6s} b: avg V_b/phi = {avg_Vphi:.4f}, avg W_b/phi = {avg_Wphi:.6f}, avg S_b/phi = {avg_Sphi:.4f}, total S = {total_S:.2f}")

    # Key test: what fraction of S comes from each b-range?
    V = sum(V_b_list)
    W = sum(W_b_list)

    # The bound we actually need: |S| < (alpha - 1) * C' / 2
    needed = (float(alpha) - 1) * float(C_prime) / 2
    print(f"\n  |S| = {abs(float(S)):.2f}, needed |S| < {needed:.2f} for alpha+rho > 1")
    print(f"  Margin: {needed / abs(float(S)):.4f}x")

    # Check: what if we bound |S| <= c * sqrt(V * log(N)) for some c?
    # Then |rho| = 2*c*sqrt(V*log N)/C'
    # We need 2*c*sqrt(V*log N)/C' < alpha - 1
    # i.e., c < (alpha-1)*C' / (2*sqrt(V*log N))
    c_needed = (float(alpha) - 1) * float(C_prime) / (2 * sqrt(V * log(N)))
    c_actual = abs(float(S)) / sqrt(V * log(N))
    print(f"  |S|/sqrt(V*log N) = {c_actual:.4f}, need < {c_needed:.4f}")

    # Check: |S|/sqrt(V) scaling
    print(f"  |S|/sqrt(V) = {abs(float(S))/sqrt(V):.4f}")
    print(f"  |S|/(V/sqrt(C')) = {abs(float(S)) * sqrt(float(C_prime))/V:.6f}")

    return {'p': p, 'alpha': float(alpha), 'rho': float(rho),
            'S': float(S), 'V': V, 'C': float(C_prime),
            'c_actual': c_actual, 'c_needed': c_needed,
            'S_over_sqrtV': abs(float(S))/sqrt(V)}

results = []
for p in range(5, 500):
    if is_prime(p) and mertens(p) == -3:
        r = analyze_deep(p)
        results.append(r)

print("\n\n===== CRITICAL SCALING TABLE =====")
print(f"{'p':>5} {'|S|/sqrt(V*logN)':>16} {'c_needed':>10} {'|S|/sqrt(V)':>12} {'|S|/V*sqrtC':>12} {'margin':>8}")
for r in results:
    N = r['p'] - 1
    margin = r['c_needed'] / r['c_actual'] if r['c_actual'] > 0 else float('inf')
    s_over_v_sqrtc = abs(r['S']) * sqrt(r['C']) / r['V']
    print(f"{r['p']:5d} {r['c_actual']:16.4f} {r['c_needed']:10.4f} {r['S_over_sqrtV']:12.4f} {s_over_v_sqrtc:12.6f} {margin:8.2f}x")
