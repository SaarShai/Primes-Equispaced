#!/usr/bin/env python3
"""
Verify the analytical bound on |rho| = 2|Sigma D_err * delta| / C'.

The proof strategy:
1. S = Sigma D_err * delta = Sigma_b S_b (per-denominator decomposition)
2. S_b = T_b - U_b where T_b = (1/b) Sigma_a a * D_err(a/b), U_b = (1/b) Sigma_a sigma_p(a) * D_err(a/b)
3. Sigma_b T_b = Sigma_f f * D_err(f) = 0 (by OLS orthogonality)
4. So S = -Sigma_b U_b
5. Each U_b^2 <= V_b * phi(b) / (3 * b^2) ... too loose
6. KEY: Use Cauchy-Schwarz per-b: S_b^2 <= V_b * W_b where V_b = Sigma D_err^2, W_b = Sigma delta^2
7. Then |S|^2 <= (Sigma_b sqrt(V_b * W_b))^2  ... by triangle inequality + CS
8. Better: use the identity S = -Sigma_b U_b and the random permutation variance model

Verify:
- Sigma_b T_b = 0 exactly
- Per-b variance of S_b
- Random permutation model prediction vs actual
- The bound |S|^2 <= V/12 (random perm model)
- Resulting |rho| bound
"""

from fractions import Fraction
from math import gcd, log, sqrt, pi
import sys

def mobius(n):
    if n == 1: return 1
    temp = n
    d = 2
    factors = 0
    while d * d <= temp:
        if temp % d == 0:
            factors += 1
            temp //= d
            if temp % d == 0: return 0
        d += 1
    if temp > 1: factors += 1
    return (-1) ** factors

def mertens(N):
    return sum(mobius(k) for k in range(1, N+1))

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    d = 5
    while d * d <= n:
        if n % d == 0 or (n + 2) % d == 0: return False
        d += 6
    return True

def analyze_prime(p):
    """Full analysis for a single M(p)=-3 prime."""
    N = p - 1

    # Build Farey sequence F_N (interior fractions only, b >= 2)
    fracs = []
    for b in range(2, N + 1):
        for a in range(1, b):
            if gcd(a, b) == 1:
                fracs.append((a, b))

    fracs.sort(key=lambda x: Fraction(x[0], x[1]))
    n = len(fracs)

    # Compute D(f) = rank - n*f (0-indexed rank = j for j-th fraction)
    D_vals = []
    f_vals = []
    for j, (a, b) in enumerate(fracs):
        f = Fraction(a, b)
        D = Fraction(j) - n * f
        D_vals.append(D)
        f_vals.append(f)

    # Compute delta(f) = (a - pa mod b) / b
    delta_vals = []
    for a, b in fracs:
        sigma = (p * a) % b
        delta = Fraction(a - sigma, b)
        delta_vals.append(delta)

    # Linear regression: alpha = Cov(D, f) / Var(f)
    mean_f = sum(f_vals) / n
    mean_D = sum(D_vals) / n

    cov_Df = sum((D - mean_D) * (f - mean_f) for D, f in zip(D_vals, f_vals)) / n
    var_f = sum((f - mean_f)**2 for f in f_vals) / n
    alpha = cov_Df / var_f

    # D_err = D - mean_D - alpha * (f - mean_f)
    D_err = [D - mean_D - alpha * (f - mean_f) for D, f in zip(D_vals, f_vals)]

    # Verify orthogonality
    sum_Derr = sum(D_err)
    sum_Derr_f = sum(de * f for de, f in zip(D_err, f_vals))
    assert abs(float(sum_Derr)) < 1e-10, f"sum D_err = {float(sum_Derr)}"
    assert abs(float(sum_Derr_f)) < 1e-10, f"sum D_err*f = {float(sum_Derr_f)}"

    # C' = sum delta^2
    C_prime = sum(d**2 for d in delta_vals)

    # S = sum D_err * delta
    S = sum(de * d for de, d in zip(D_err, delta_vals))

    # rho = 2*S / C'
    rho = 2 * S / C_prime

    # Per-denominator decomposition
    # Build index by denominator
    by_denom = {}
    for idx, (a, b) in enumerate(fracs):
        if b not in by_denom:
            by_denom[b] = []
        by_denom[b].append(idx)

    # Compute T_b, U_b, S_b, V_b, W_b per denominator
    sum_Tb = Fraction(0)
    sum_Ub = Fraction(0)
    sum_Sb = Fraction(0)
    sum_Sb_sq = Fraction(0)
    sum_Vb_Wb = Fraction(0)
    sum_Vb = Fraction(0)
    sum_Wb = Fraction(0)
    sum_Vb_over_12 = Fraction(0)

    per_b_data = []

    for b in sorted(by_denom.keys()):
        indices = by_denom[b]
        phi_b = len(indices)

        # T_b = (1/b) * sum_a a * D_err(a/b)
        T_b = sum(Fraction(fracs[i][0], b) * D_err[i] for i in indices)  # This is sum f*D_err for this b
        # Actually T_b = (1/b) * sum_a a * D_err(a/b) = sum_a (a/b) * D_err(a/b) = sum f * D_err

        # U_b = (1/b) * sum_a sigma_p(a) * D_err(a/b)
        U_b = Fraction(0)
        for i in indices:
            a_val, b_val = fracs[i]
            sigma = (p * a_val) % b_val
            U_b += Fraction(sigma, b_val) * D_err[i]

        # S_b = sum D_err(a/b) * delta(a/b) for this b
        S_b = sum(D_err[i] * delta_vals[i] for i in indices)

        # Also: S_b should equal T_b - U_b
        check = T_b - U_b
        assert abs(float(S_b - check)) < 1e-10, f"S_b mismatch at b={b}: {float(S_b)} vs {float(check)}"

        # V_b = sum D_err^2 for this b
        V_b = sum(D_err[i]**2 for i in indices)

        # W_b = sum delta^2 for this b
        W_b = sum(delta_vals[i]**2 for i in indices)

        sum_Tb += T_b
        sum_Ub += U_b
        sum_Sb += S_b
        sum_Sb_sq += S_b**2
        sum_Vb_Wb += V_b * W_b
        sum_Vb += V_b
        sum_Wb += W_b
        sum_Vb_over_12 += V_b / 12

        per_b_data.append((b, phi_b, float(T_b), float(U_b), float(S_b), float(V_b), float(W_b)))

    # Verify sum_Tb = 0
    print(f"\n=== p = {p}, N = {N}, M(p) = {mertens(p)}, n = {n} ===")
    print(f"  sum T_b = {float(sum_Tb):.6e}  (should be 0)")
    print(f"  sum S_b = {float(sum_Sb):.6e}  (= S = {float(S):.6e})")
    print(f"  S = sum D_err*delta = {float(S):.6f}")
    print(f"  C' = {float(C_prime):.6f}")
    print(f"  alpha = {float(alpha):.6f}")
    print(f"  rho = {float(rho):.6f}")
    print(f"  alpha + rho = {float(alpha + rho):.6f}")

    # Key quantities for the bound
    V = float(sum_Vb)  # = sum D_err^2
    C = float(C_prime)
    S_val = float(S)

    print(f"\n  --- Bound verification ---")
    print(f"  V = sum D_err^2 = {V:.6f}")
    print(f"  C' = sum delta^2 = {C:.6f}")
    print(f"  |S| = {abs(S_val):.6f}")
    print(f"  sqrt(V/12) = {sqrt(V/12):.6f}  (random perm model prediction for |S|)")
    print(f"  |S| / sqrt(V/12) = {abs(S_val) / sqrt(V/12):.6f}  (should be O(1) if model holds)")

    # The bound: |rho| = 2|S|/C' <= 2*sqrt(V/12)/C'
    rho_bound_model = 2 * sqrt(V / 12) / C
    print(f"  |rho|_actual = {abs(float(rho)):.6f}")
    print(f"  |rho|_bound (V/12 model) = {rho_bound_model:.6f}")

    # Check sum S_b^2 vs V/12
    print(f"  sum S_b^2 = {float(sum_Sb_sq):.6f}")
    print(f"  V/12 = {V/12:.6f}")
    print(f"  sum S_b^2 / (V/12) = {float(sum_Sb_sq) / (V/12):.6f}")

    # Also check: sum V_b * W_b (the CS per-b bound on sum S_b^2)
    print(f"  sum V_b*W_b = {float(sum_Vb_Wb):.6f}")
    print(f"  sum S_b^2 / sum V_b*W_b = {float(sum_Sb_sq) / float(sum_Vb_Wb):.6f}  (should be << 1)")

    # The crucial ratio: 2*sqrt(V/12)/C' vs alpha - 1
    alpha_val = float(alpha)
    rho_actual = float(rho)
    print(f"\n  --- Is the bound sufficient? ---")
    print(f"  alpha = {alpha_val:.6f}")
    print(f"  alpha - 1 = {alpha_val - 1:.6f}")
    print(f"  |rho| actual = {abs(rho_actual):.6f}")
    print(f"  2*sqrt(V/12)/C' = {rho_bound_model:.6f}")
    print(f"  Bound sufficient (< alpha-1)? {rho_bound_model < alpha_val - 1}")

    # Also: express in terms of N
    print(f"\n  --- Scaling ---")
    print(f"  V/n = {V/n:.6f}  (per-fraction D_err variance)")
    print(f"  C'/n = {C/n:.6f}  (per-fraction delta variance)")
    print(f"  V/(n*N) = {V/(n*N):.6f}  (should stabilize)")
    print(f"  sqrt(V/12) / C' = {sqrt(V/12)/C:.6f}")
    print(f"  sqrt(V/12) / C' * sqrt(N) = {sqrt(V/12)/C * sqrt(N):.6f}  (should be ~constant)")

    return {
        'p': p, 'N': N, 'n': n, 'alpha': alpha_val, 'rho': rho_actual,
        'V': V, 'C': C, 'S': S_val,
        'sum_Sb_sq': float(sum_Sb_sq),
        'rho_bound': rho_bound_model,
    }

# Find M(p) = -3 primes
results = []
for p in range(5, 500):
    if is_prime(p) and mertens(p) == -3:
        r = analyze_prime(p)
        results.append(r)

print("\n\n===== SUMMARY TABLE =====")
print(f"{'p':>5} {'N':>5} {'alpha':>8} {'rho':>8} {'a+r':>8} {'|rho|':>8} {'bound':>8} {'|S|':>10} {'sqrt(V/12)':>10} {'ratio':>8} {'suff?':>5}")
for r in results:
    p = r['p']
    suff = "YES" if r['rho_bound'] < r['alpha'] - 1 else "NO"
    print(f"{p:5d} {r['N']:5d} {r['alpha']:8.4f} {r['rho']:8.4f} {r['alpha']+r['rho']:8.4f} {abs(r['rho']):8.4f} {r['rho_bound']:8.4f} {abs(r['S']):10.4f} {sqrt(r['V']/12):10.4f} {abs(r['S'])/sqrt(r['V']/12):8.4f} {suff:>5}")

# Check the scaling of the bound
print("\n\n===== SCALING ANALYSIS =====")
print(f"{'p':>5} {'2*sqrt(V/12)/C':>15} {'alpha-1':>10} {'ratio':>10} {'sqrt(V/12)/C * N':>18}")
for r in results:
    bnd = r['rho_bound']
    am1 = r['alpha'] - 1
    ratio = bnd / am1 if am1 > 0 else float('inf')
    scaled = sqrt(r['V']/12) / r['C'] * r['N']
    print(f"{r['p']:5d} {bnd:15.6f} {am1:10.4f} {ratio:10.4f} {scaled:18.6f}")
