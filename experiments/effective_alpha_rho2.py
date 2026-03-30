#!/usr/bin/env python3
"""
EFFECTIVE ALPHA-RHO ANALYSIS - Part 2

Direct approach: bound |rho| = |2*sum(D_err*delta)/C'| by analyzing
the per-denominator structure.

Key insight: rho = 2*sum_b S_b^{err} / C' where S_b^{err} = sum_{a coprime b} D_err(a/b) * delta(a/b)

If the S_b^{err} terms cancel across denominators, we get a bound on |rho|.

NEW IDEA: Instead of bounding rho, bound B'/C' - alpha DIRECTLY.
B'/C' - alpha = rho = 2*sum(D_err*delta)/C'

The D_err is orthogonal to linear functions of f. So the only part of delta
that contributes is the "nonlinear" part delta_err = delta - beta*(f - mean_f) - gamma.

Thus: rho = 2*sum(D_err * delta_err) / C'  (exact, since D_err perp linear functions)

And: |rho| <= 2 * ||D_err|| * ||delta_err|| / C'  (Cauchy-Schwarz)

Now: ||delta_err||^2 / C' = 1 - (linear explained variance of delta by f)
     = 1 - Cov(delta, f)^2 / (Var(delta) * Var(f))

If the linear part of delta explains a fraction eta^2 of Var(delta), then:
  ||delta_err||^2 = C' * (1 - eta^2)   ... wait this isn't right for sums vs variances.

Let me be precise.

delta_err(f) = delta(f) - beta*(f - mean_f) - mean(delta)
where beta = Cov(delta, f) / Var(f)

||delta_err||^2 = sum(delta_err^2) = sum(delta^2) - n*mean(delta)^2 - beta^2 * sum((f-mean_f)^2)
               = C_raw - n*mean(delta)^2 - beta^2 * n * Var(f)

For primes: mean(delta) = 0 (sum_delta = 0), so:
||delta_err||^2 = C_raw - beta^2 * n * Var(f)

And rho = 2*sum(D_err * delta_err) / C_raw

By Cauchy-Schwarz:
|rho| <= 2 * ||D_err|| * ||delta_err|| / C_raw
       = 2 * sqrt(||D_err||^2 * ||delta_err||^2) / C_raw
       = 2 * sqrt(||D_err||^2 / C_raw * ||delta_err||^2 / C_raw)

Let R_D^2 = ||D_err||^2 / C_raw and R_delta^2 = ||delta_err||^2 / C_raw.

Then |rho| <= 2 * sqrt(R_D^2 * R_delta^2) = 2 * R_D * R_delta.

We already know R_D = ||D_err|| / ||delta|| ~ sqrt(N).

What about R_delta? R_delta = ||delta_err|| / ||delta||.
If R_delta < 1 (i.e., delta has significant linear component),
that helps reduce the bound.

From the decorrelation proof: rho^2(f, delta) = Cov(f,delta)^2 / (Var(f)*Var(delta)) ~ pi^2/(24 log N).
So 1 - rho^2 ~ 1 - pi^2/(24 log N), meaning R_delta ~ 1 - pi^2/(48 log N).

This doesn't help: R_delta ~ 1 for large N.

ALTERNATIVE: Don't use Cauchy-Schwarz at all. Instead, use the identity
  sum(D_err * delta) = sum_b S_b^err
and bound each S_b^err individually.

For a fixed denominator b, with phi(b) coprime residues:
  S_b^err = sum_{a coprime b} D_err(a/b) * (a - sigma_p(a))/b

D_err(a/b) = D(a/b) - mean_D - alpha*(a/b - mean_f)

The variance of D_err within denominator b is Var_b(D_err).
The variance of delta within denominator b is Var_b(delta).

Key question: what is the per-denominator correlation between D_err and delta?
"""

from fractions import Fraction
from math import gcd, log, sqrt
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

def farey_sequence(N):
    fracs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: Fraction(x[0], x[1]))
    return fracs

def compute_per_denom(p):
    """Compute per-denominator contributions to rho."""
    N = p - 1
    fracs = farey_sequence(N)
    n = len(fracs)
    interior = [(a, b) for (a, b) in fracs if b >= 2]
    n_int = len(interior)

    # Compute delta and D for interior fractions
    deltas = {}
    for (a, b) in interior:
        sigma = (p * a) % b
        deltas[(a, b)] = Fraction(a - sigma, b)

    rank_map = {}
    for j, (a, b) in enumerate(fracs):
        rank_map[(a, b)] = j

    D_map = {}
    for (a, b) in fracs:
        D_map[(a, b)] = Fraction(rank_map[(a, b)]) - n * Fraction(a, b)

    # Compute alpha (regression slope)
    sum_f = sum(Fraction(a, b) for (a, b) in interior)
    sum_D = sum(D_map[(a, b)] for (a, b) in interior)
    sum_f2 = sum(Fraction(a, b)**2 for (a, b) in interior)
    sum_Df = sum(D_map[(a, b)] * Fraction(a, b) for (a, b) in interior)

    mean_f = sum_f / n_int
    mean_D = sum_D / n_int
    cov_Df = sum_Df / n_int - mean_D * mean_f
    var_f = sum_f2 / n_int - mean_f**2
    alpha = cov_Df / var_f

    # Compute D_err for each interior fraction
    D_err = {}
    for (a, b) in interior:
        D_err[(a, b)] = D_map[(a, b)] - mean_D - alpha * (Fraction(a, b) - mean_f)

    # Per-denominator analysis
    denoms = sorted(set(b for (a, b) in interior))

    C_prime = sum(deltas[(a, b)]**2 for (a, b) in interior)
    B_prime = sum(2 * D_map[(a, b)] * deltas[(a, b)] for (a, b) in interior)

    sum_Derr_delta = sum(D_err[(a, b)] * deltas[(a, b)] for (a, b) in interior)
    rho = 2 * sum_Derr_delta / C_prime

    print(f"\n=== p = {p}, N = {N}, n = {n}, n_int = {n_int} ===")
    print(f"alpha = {float(alpha):.6f}")
    print(f"rho = {float(rho):.6f}")
    print(f"alpha + rho = {float(alpha + rho):.6f}")
    print(f"B'/C' = {float(B_prime/C_prime):.6f}")
    print(f"C' = {float(C_prime):.4f}")

    # Per-denominator S_b^err
    print(f"\n  b  phi(b)  S_b_err     |S_b_err|  C_b        S_b_err/C_b")
    total_S_err = Fraction(0)
    total_C_b = Fraction(0)

    per_denom_data = []
    for b in denoms:
        fracs_b = [(a, b) for (a, bb) in interior if bb == b]
        S_b_err = sum(D_err[(a, b)] * deltas[(a, b)] for (a, _) in fracs_b)
        C_b = sum(deltas[(a, b)]**2 for (a, _) in fracs_b)
        total_S_err += S_b_err
        total_C_b += C_b
        phi_b = len(fracs_b)
        per_denom_data.append((b, phi_b, float(S_b_err), float(C_b)))
        if phi_b >= 2:
            print(f"  {b:3d}  {phi_b:3d}  {float(S_b_err):10.4f}  {abs(float(S_b_err)):10.4f}  "
                  f"{float(C_b):10.4f}  {float(S_b_err/C_b) if C_b != 0 else 0:10.4f}")

    # Verify sum
    print(f"\n  Total S_err = {float(total_S_err):.6f}, should equal sum_Derr_delta = {float(sum_Derr_delta):.6f}")
    print(f"  Total C_b = {float(total_C_b):.4f}, should equal C' = {float(C_prime):.4f}")

    # Key: what fraction of |S_err| comes from small vs large denominators?
    cumsum_S_small = Fraction(0)
    cumsum_S_large = Fraction(0)
    threshold = int(sqrt(N))
    for b, phi_b, s_err, c_b in per_denom_data:
        if b <= threshold:
            cumsum_S_small += Fraction(s_err).limit_denominator(10**15)
        else:
            cumsum_S_large += Fraction(s_err).limit_denominator(10**15)

    print(f"\n  Small denom (b <= {threshold}): sum S_err ~ {float(cumsum_S_small):.4f}")
    print(f"  Large denom (b > {threshold}): sum S_err ~ {float(cumsum_S_large):.4f}")

    # Compute ||D_err||^2 and ||delta_err||^2
    beta = sum(deltas[(a, b)] * (Fraction(a, b) - mean_f) for (a, b) in interior)
    beta = beta / (n_int * var_f)
    # Actually beta = Cov(delta, f) / Var(f)
    sum_d = sum(deltas[(a, b)] for (a, b) in interior)
    sum_df = sum(deltas[(a, b)] * Fraction(a, b) for (a, b) in interior)
    mean_delta = sum_d / n_int
    cov_delta_f = sum_df / n_int - mean_delta * mean_f
    beta_correct = cov_delta_f / var_f

    norm_Derr2 = sum(D_err[(a, b)]**2 for (a, b) in interior)

    # delta_err = delta - mean_delta - beta*(f - mean_f)
    norm_delta_err2 = Fraction(0)
    for (a, b) in interior:
        d_err = deltas[(a, b)] - mean_delta - beta_correct * (Fraction(a, b) - mean_f)
        norm_delta_err2 += d_err**2

    # Cauchy-Schwarz bound on |rho|
    cs_bound = 2 * (float(norm_Derr2) * float(norm_delta_err2))**0.5 / float(C_prime)

    print(f"\n  ||D_err||^2 = {float(norm_Derr2):.4f}")
    print(f"  ||delta||^2 = C' = {float(C_prime):.4f}")
    print(f"  ||delta_err||^2 = {float(norm_delta_err2):.4f}")
    print(f"  ||delta_err||/||delta|| = {(float(norm_delta_err2)/float(C_prime))**0.5:.6f}")
    print(f"  R = ||D_err||/||delta|| = {(float(norm_Derr2)/float(C_prime))**0.5:.6f}")
    print(f"  Cauchy-Schwarz bound on |rho|: {cs_bound:.4f}")
    print(f"  Actual |rho| = {abs(float(rho)):.4f}")
    print(f"  Ratio actual/CS = {abs(float(rho))/cs_bound:.4f}")

    return {
        'p': p,
        'alpha': float(alpha),
        'rho': float(rho),
        'R': (float(norm_Derr2)/float(C_prime))**0.5,
        'delta_err_ratio': (float(norm_delta_err2)/float(C_prime))**0.5,
        'cs_bound': cs_bound,
        'actual_rho': abs(float(rho)),
    }

# Find M=-3 primes
primes_m3 = [p for p in range(2, 200) if is_prime(p) and mertens(p) == -3]
print(f"M=-3 primes up to 200: {primes_m3}")

results = []
for p in primes_m3:
    print(f"\nComputing p = {p}...", file=sys.stderr)
    r = compute_per_denom(p)
    results.append(r)

print("\n\n" + "="*80)
print("SUMMARY TABLE")
print("="*80)
print(f"{'p':>5} {'alpha':>8} {'|rho|':>8} {'a+r':>8} {'R':>8} {'d_err_r':>8} {'CS_bnd':>8} {'|rho|/CS':>10}")
for r in results:
    print(f"{r['p']:5d} {r['alpha']:8.4f} {r['actual_rho']:8.4f} "
          f"{r['alpha']+r['rho']:8.4f} {r['R']:8.4f} {r['delta_err_ratio']:8.4f} "
          f"{r['cs_bound']:8.4f} {r['actual_rho']/r['cs_bound']:10.4f}")

print()
print("KEY FINDING:")
print("CS_bnd = 2 * ||D_err|| * ||delta_err|| / C'")
print("This is the tightest Cauchy-Schwarz bound using orthogonality.")
print("If CS_bnd < alpha - 1 for all p >= 43, then alpha + rho > 1 unconditionally.")
print()
for r in results:
    alpha_m1 = r['alpha'] - 1
    cs = r['cs_bound']
    status = "OK" if cs < alpha_m1 else "FAIL"
    print(f"  p={r['p']:3d}: CS_bnd={cs:.4f}, alpha-1={alpha_m1:.4f}, "
          f"ratio={cs/alpha_m1:.4f} [{status}]")
