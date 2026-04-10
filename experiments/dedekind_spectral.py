#!/usr/bin/env python3
"""
Dedekind-kernel spectral attack on Σ E(k)².

Formula from Codex:
  Σ E(k)² = (1/(p-1)) Σ_χ K̂_p(χ) |Λ_p(χ)|²

where:
  K̂_p(χ) = Σ_{r=1}^{p-1} s(r,p) · χ(r)     (Dedekind kernel transform)
  Λ_p(χ) = Σ_{a=1}^{p-1} λ_p(a) · χ(a)       (Mertens-type transform)
  λ_p(m) = M(⌊N/m⌋) + 1_{m=1}                 where N = p-1
  s(r,p) = Dedekind sum s(r,p) = Σ_{k=1}^{p-1} ((k/p))((kr/p))
  ((x)) = x - floor(x) - 1/2 if x not integer, 0 if integer (sawtooth)
"""

import numpy as np
from fractions import Fraction
import json

def sawtooth(x):
    """((x)) = x - floor(x) - 1/2 if x not integer, 0 if integer."""
    fx = x - int(x) if x >= 0 else x - int(x)
    # Handle negative properly
    import math
    fx = x - math.floor(x)
    if abs(fx) < 1e-15 or abs(fx - 1) < 1e-15:
        return 0.0
    return fx - 0.5

def dedekind_sum(r, p):
    """Compute Dedekind sum s(r,p) = Σ_{k=1}^{p-1} ((k/p))((kr/p))."""
    total = 0.0
    for k in range(1, p):
        total += sawtooth(k / p) * sawtooth(k * r / p)
    return total

def mertens(n):
    """Compute Mertens function M(n) = Σ_{k=1}^n μ(k)."""
    if n <= 0:
        return 0
    # Sieve for mu
    mu = [0] * (n + 1)
    mu[1] = 1
    is_prime = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (n + 1)
    M[0] = 0
    for i in range(1, n + 1):
        M[i] = M[i - 1] + mu[i]
    return M[n]

def mertens_array(n):
    """Return full array M[0..n]."""
    if n <= 0:
        return [0]
    mu = [0] * (n + 1)
    mu[1] = 1
    is_prime = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (n + 1)
    for i in range(1, n + 1):
        M[i] = M[i - 1] + mu[i]
    return M

def primitive_root(p):
    """Find a primitive root mod p."""
    for g in range(2, p):
        seen = set()
        val = 1
        for _ in range(p - 1):
            val = (val * g) % p
            seen.add(val)
        if len(seen) == p - 1:
            return g
    return None

def all_characters(p):
    """
    Return all (p-1) Dirichlet characters mod p.
    χ_j(g^k) = ω^{jk} where g = primitive root, ω = e^{2πi/(p-1)}.
    Returns dict: j -> {a: χ_j(a) for a in 1..p-1}
    """
    g = primitive_root(p)
    n = p - 1
    omega = np.exp(2j * np.pi / n)

    # Build discrete log table: a -> k where g^k ≡ a mod p
    dlog = {}
    val = 1
    for k in range(n):
        dlog[val] = k
        val = (val * g) % p

    chars = {}
    for j in range(n):
        chi = {}
        for a in range(1, p):
            chi[a] = omega ** (j * dlog[a])
        chars[j] = chi
    return chars

def compute_spectral(p):
    """Compute all spectral quantities for prime p."""
    N = p - 1
    print(f"\n{'='*70}")
    print(f"  PRIME p = {p},  N = p-1 = {N}")
    print(f"{'='*70}")

    # 1. Dedekind sums s(r, p) for r = 1..p-1
    ded_sums = {}
    for r in range(1, p):
        ded_sums[r] = dedekind_sum(r, p)

    print(f"\nDedekind sums s(r,{p}):")
    for r in sorted(ded_sums.keys()):
        if abs(ded_sums[r]) > 1e-12:
            print(f"  s({r},{p}) = {ded_sums[r]:.10f}")

    # Dedekind sum reciprocity: s(r,p) + s(p,r) = (r/p + p/r + 1/(rp))/12 - 1/4
    # For p prime: s(r,p) = (1/4p) Σ_{k=1}^{p-1} cot(πk/p) cot(πkr/p)

    # 2. All Dirichlet characters
    chars = all_characters(p)

    # 3. Compute K̂_p(χ) = Σ_{r=1}^{p-1} s(r,p) · χ(r)
    K_hat = {}
    for j in range(N):
        val = 0.0 + 0j
        for r in range(1, p):
            val += ded_sums[r] * chars[j][r]
        K_hat[j] = val

    print(f"\nK̂_p(χ_j) for all characters:")
    for j in range(N):
        re, im = K_hat[j].real, K_hat[j].imag
        print(f"  j={j:2d}: K̂ = {re:+12.8f} {im:+12.8f}i  |K̂| = {abs(K_hat[j]):.8f}")

    # 4. Check positivity of Re(K̂_p(χ))
    all_nonneg = all(K_hat[j].real >= -1e-10 for j in range(N))
    print(f"\nPositivity check: All Re(K̂_p(χ)) ≥ 0?  {'YES' if all_nonneg else 'NO'}")
    if not all_nonneg:
        neg_chars = [(j, K_hat[j].real) for j in range(N) if K_hat[j].real < -1e-10]
        print(f"  Negative values: {neg_chars}")

    # 5. Compute λ_p(m) = M(⌊N/m⌋) + 1_{m=1}
    M_arr = mertens_array(N)

    lambda_p = {}
    for m in range(1, p):
        lambda_p[m] = M_arr[N // m] + (1 if m == 1 else 0)

    print(f"\nλ_p(m) for m = 1..{min(20, p-1)}:")
    for m in range(1, min(21, p)):
        print(f"  λ({m}) = {lambda_p[m]}  [M(⌊{N}/{m}⌋) = {M_arr[N // m]}, indicator = {1 if m == 1 else 0}]")

    # 6. Compute Λ_p(χ) = Σ_{a=1}^{p-1} λ_p(a) · χ(a)
    Lambda = {}
    for j in range(N):
        val = 0.0 + 0j
        for a in range(1, p):
            val += lambda_p[a] * chars[j][a]
        Lambda[j] = val

    print(f"\nΛ_p(χ_j) for all characters:")
    for j in range(N):
        re, im = Lambda[j].real, Lambda[j].imag
        mag2 = abs(Lambda[j])**2
        print(f"  j={j:2d}: Λ = {re:+12.6f} {im:+12.6f}i  |Λ|² = {mag2:.6f}")

    # 7. Spectral formula: Σ E(k)² = (1/(p-1)) Σ_χ K̂_p(χ) |Λ_p(χ)|²
    spectral_sum = 0.0 + 0j
    for j in range(N):
        spectral_sum += K_hat[j] * abs(Lambda[j])**2
    spectral_sum /= (p - 1)

    print(f"\nSpectral formula result:")
    print(f"  (1/(p-1)) Σ K̂·|Λ|² = {spectral_sum.real:.10f} + {spectral_sum.imag:.10f}i")

    # 8. Direct computation of Σ E(k)² for comparison
    # E(k) = Σ_{m≤k, gcd(m,p)=1} 1  -  k·φ(p)/p
    # For prime p: E(k) = #{1≤m≤k : p∤m} - k·(p-1)/p
    direct_sum_E2 = 0.0
    for k in range(1, p):
        count = sum(1 for m in range(1, k + 1) if m % p != 0)
        E_k = count - k * (p - 1) / p
        direct_sum_E2 += E_k**2

    print(f"  Direct Σ E(k)² = {direct_sum_E2:.10f}")
    print(f"  Ratio spectral/direct = {spectral_sum.real / direct_sum_E2 if direct_sum_E2 > 0 else 'N/A':.10f}")

    # 9. Parseval check: Σ_χ |Λ_p(χ)|² = (p-1) · Σ |λ_p(a)|²
    parseval_lhs = sum(abs(Lambda[j])**2 for j in range(N))
    parseval_rhs = (p - 1) * sum(lambda_p[a]**2 for a in range(1, p))

    print(f"\nParseval check:")
    print(f"  Σ |Λ(χ)|² = {parseval_lhs:.6f}")
    print(f"  (p-1)·Σ|λ(a)|² = {parseval_rhs:.6f}")
    print(f"  Match: {abs(parseval_lhs - parseval_rhs) < 1e-6}")
    print(f"  Σ|λ(a)|² = {sum(lambda_p[a]**2 for a in range(1, p)):.6f}")

    # 10. Which characters dominate |Λ|²?
    sorted_chars = sorted(range(N), key=lambda j: abs(Lambda[j])**2, reverse=True)
    print(f"\nTop characters by |Λ(χ)|²:")
    for rank, j in enumerate(sorted_chars[:min(10, N)]):
        pct = abs(Lambda[j])**2 / parseval_lhs * 100
        print(f"  #{rank+1}: j={j}, |Λ|² = {abs(Lambda[j])**2:.6f} ({pct:.1f}% of total)")

    # 11. Look at K̂ for principal character (j=0)
    print(f"\nPrincipal character (j=0):")
    print(f"  K̂_p(χ_0) = {K_hat[0].real:.10f}")
    print(f"  This = Σ s(r,p) = {sum(ded_sums[r] for r in range(1, p)):.10f}")
    # Known: Σ_{r=1}^{p-1} s(r,p) = -(p-1)(p-2)/(12p)... let's check
    theory = -(p-1)*(p-2)/(12*p)
    print(f"  Theory -(p-1)(p-2)/(12p) = {theory:.10f}")

    # 12. Analyze K̂ structure — is there a log p factor?
    print(f"\n--- LOG P ANALYSIS ---")
    print(f"  log(p) = {np.log(p):.6f}")
    print(f"  K̂(χ_0) = {K_hat[0].real:.6f}")
    print(f"  K̂(χ_0) / log(p) = {K_hat[0].real / np.log(p):.6f}")
    print(f"  max |K̂(χ)| = {max(abs(K_hat[j]) for j in range(N)):.6f}")
    print(f"  max |K̂| / log(p) = {max(abs(K_hat[j]) for j in range(N)) / np.log(p):.6f}")

    # Average |K̂| over non-principal
    if N > 1:
        avg_Khat = np.mean([abs(K_hat[j]) for j in range(1, N)])
        print(f"  avg |K̂(χ)| (non-principal) = {avg_Khat:.6f}")
        print(f"  avg / log(p) = {avg_Khat / np.log(p):.6f}")

    return {
        'p': p,
        'K_hat': {j: (K_hat[j].real, K_hat[j].imag) for j in range(N)},
        'Lambda': {j: (Lambda[j].real, Lambda[j].imag) for j in range(N)},
        'Lambda_sq': {j: abs(Lambda[j])**2 for j in range(N)},
        'spectral_sum': spectral_sum.real,
        'direct_sum': direct_sum_E2,
        'parseval_lhs': parseval_lhs,
        'parseval_rhs': parseval_rhs,
        'logp': np.log(p),
    }

# Run for target primes
results = {}
for p in [11, 13, 17]:
    results[p] = compute_spectral(p)

# Cross-prime analysis
print(f"\n{'='*70}")
print(f"  CROSS-PRIME ANALYSIS")
print(f"{'='*70}")

print(f"\n{'p':>4} {'log p':>8} {'ΣE²':>12} {'ΣE²/logp':>12} {'K̂(χ₀)':>12} {'K̂₀/logp':>12} {'max|K̂|':>10} {'Σ|λ|²':>10}")
for p in [11, 13, 17]:
    r = results[p]
    K0 = r['K_hat'][0][0]
    max_K = max(np.sqrt(v[0]**2 + v[1]**2) for v in r['K_hat'].values())
    sum_lam2 = r['parseval_rhs'] / (p - 1)
    print(f"{p:4d} {r['logp']:8.4f} {r['direct_sum']:12.6f} {r['direct_sum']/r['logp']:12.6f} {K0:12.6f} {K0/r['logp']:12.6f} {max_K:10.6f} {sum_lam2:10.1f}")

# Deeper analysis: decompose spectral sum by character
print(f"\n--- SPECTRAL DECOMPOSITION ---")
for p in [11, 13, 17]:
    r = results[p]
    N = p - 1
    print(f"\np = {p}:")
    total = 0.0
    for j in range(N):
        K_re = r['K_hat'][j][0]
        K_im = r['K_hat'][j][1]
        L2 = r['Lambda_sq'][j]
        contrib = (K_re * L2) / N  # real part of contribution
        total += contrib
        if abs(contrib) > 0.001:
            print(f"  j={j:2d}: K̂={K_re:+.6f}{K_im:+.6f}i, |Λ|²={L2:.4f}, contrib={contrib:.6f}")
    print(f"  Total = {total:.6f}")

# Run larger primes to see scaling
print(f"\n{'='*70}")
print(f"  SCALING ANALYSIS (more primes)")
print(f"{'='*70}")

large_primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
print(f"\n{'p':>4} {'logp':>7} {'ΣE²':>10} {'ΣE²/logp':>10} {'Σ|λ|²':>8} {'K̂(χ₀)':>10} {'|K̂₀|/p':>8}")
for p in large_primes:
    r = compute_spectral(p)
    K0 = r['K_hat'][0][0]
    sum_lam2 = r['parseval_rhs'] / (p - 1)
    print(f"{p:4d} {r['logp']:7.3f} {r['direct_sum']:10.4f} {r['direct_sum']/r['logp']:10.4f} {sum_lam2:8.1f} {K0:10.6f} {abs(K0)/p:8.5f}")

# Final: check if K̂(non-principal) ~ constant or ~ logp
print(f"\n--- NON-PRINCIPAL K̂ SCALING ---")
print(f"{'p':>4} {'logp':>7} {'avg|K̂_np|':>12} {'avg/logp':>10} {'avg*p':>10} {'max|K̂_np|':>12} {'max/logp':>10}")
for p in large_primes:
    if p < 5:
        continue
    r = compute_spectral(p)
    N = p - 1
    np_vals = [np.sqrt(r['K_hat'][j][0]**2 + r['K_hat'][j][1]**2) for j in range(1, N)]
    if np_vals:
        avg_np = np.mean(np_vals)
        max_np = max(np_vals)
        print(f"{p:4d} {r['logp']:7.3f} {avg_np:12.6f} {avg_np/r['logp']:10.6f} {avg_np*p:10.4f} {max_np:12.6f} {max_np/r['logp']:10.6f}")
