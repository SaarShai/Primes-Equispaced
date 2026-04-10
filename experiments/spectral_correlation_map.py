#!/usr/bin/env python3
"""
Spectral Correlation Mapping:
Compute |L(1,χ)|² and |Λ_p(χ)|² for all Dirichlet characters χ mod p,
for a range of primes. Analyze correlations and where the log p factor lives.
"""

import numpy as np
from math import gcd, floor, log, pi, sqrt
from itertools import product as iterproduct
import sys

# ─── Mertens function ───
def mertens(n):
    """Compute M(n) = Σ_{k=1}^n μ(k)"""
    if n <= 0:
        return 0
    # Sieve μ
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
    M = 0
    for k in range(1, n + 1):
        M += mu[k]
    return M

# Precompute Mertens values up to max needed
def precompute_mertens(N):
    """Return array M[0..N] where M[n] = Σ_{k=1}^n μ(k)"""
    mu = [0] * (N + 1)
    mu[1] = 1
    is_prime = [True] * (N + 1)
    primes = []
    for i in range(2, N + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (N + 1)
    for k in range(1, N + 1):
        M[k] = M[k - 1] + mu[k]
    return M

# ─── Dirichlet characters mod p (p prime) ───
def primitive_root(p):
    """Find a primitive root mod p."""
    if p == 2:
        return 1
    # Factor p-1
    phi = p - 1
    factors = set()
    n = phi
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    # Find generator
    for g in range(2, p):
        ok = True
        for f in factors:
            if pow(g, phi // f, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None

def build_characters(p):
    """
    Build all Dirichlet characters mod p (p prime).
    Returns list of dicts: chi[a] for a in 0..p-1.
    chi[0] = 0 always (for a ≡ 0 mod p).
    Character index k=0 is the principal character.
    """
    g = primitive_root(p)
    # Build discrete log table
    dlog = [0] * p  # dlog[g^j mod p] = j
    val = 1
    for j in range(p - 1):
        dlog[val] = j
        val = (val * g) % p

    omega = np.exp(2j * pi / (p - 1))
    characters = []
    for k in range(p - 1):  # k = 0, 1, ..., p-2
        chi = np.zeros(p, dtype=complex)
        for a in range(1, p):
            chi[a] = omega ** (k * dlog[a])
        characters.append(chi)
    return characters

def is_even_character(chi, p):
    """χ is even if χ(-1) = 1, odd if χ(-1) = -1."""
    val = chi[p - 1]  # -1 mod p = p-1
    return abs(val - 1.0) < 1e-6

# ─── L(1, χ) computation ───
def compute_L1(chi, p, num_terms=1000):
    """Compute L(1,χ) = Σ_{n=1}^{num_terms} χ(n)/n."""
    s = 0.0 + 0.0j
    for n in range(1, num_terms + 1):
        s += chi[n % p] / n
    return s

# ─── Lambda_p and E(k) ───
def compute_lambda_p(p, M_arr):
    """
    λ_p(a) = M(⌊(p-1)/a⌋) + 1_{a=1}
    Returns array lambda_p[a] for a = 0, 1, ..., p-1.
    """
    lam = np.zeros(p)
    for a in range(1, p):
        lam[a] = M_arr[floor((p - 1) / a)] + (1 if a == 1 else 0)
    return lam

def compute_E_values(p, M_arr):
    """
    E(k) = Σ_{a: ⌊(p-1)/a⌋=k} 1  (i.e., count of a in [1,p-1] mapping to k)
    Actually, let me compute the Farey discrepancy sums.
    E(k) = λ_p(a) for the per-step errors.

    More precisely, E(k) for k=1,...,p-1 are the per-step discrepancies.
    But let me just compute Σ E(k)² = Σ_{a=1}^{p-1} λ_p(a)².
    """
    lam = compute_lambda_p(p, M_arr)
    return np.sum(lam[1:] ** 2)

def compute_Lambda_transform(chi, p, M_arr):
    """
    Λ_p(χ) = Σ_{a=1}^{p-1} λ_p(a)·χ(a)
    """
    lam = compute_lambda_p(p, M_arr)
    s = 0.0 + 0.0j
    for a in range(1, p):
        s += lam[a] * chi[a]
    return s

# ─── Main computation ───
primes = [11, 13, 17, 23, 29, 37, 43, 53, 67, 79, 97]

# Precompute Mertens up to max prime
max_p = max(primes)
M_arr = precompute_mertens(max_p)

results = {}

for p in primes:
    print(f"\n{'='*60}")
    print(f"Processing p = {p}")
    print(f"{'='*60}")

    chars = build_characters(p)
    num_chars = len(chars)  # = p-1

    data = []

    for k in range(num_chars):
        chi = chars[k]
        even = is_even_character(chi, p)
        parity = "even" if even else "odd"

        # L(1, χ)
        L1 = compute_L1(chi, p, num_terms=1000)
        L1_sq = abs(L1) ** 2

        # Λ_p(χ)
        Lam = compute_Lambda_transform(chi, p, M_arr)
        Lam_sq = abs(Lam) ** 2

        # K̂_p(χ)
        if even:
            Khat = 0.0
        else:
            Khat = (p / pi**2) * L1_sq

        # Product
        product = Khat * Lam_sq

        data.append({
            'k': k,
            'parity': parity,
            'L1': L1,
            'L1_sq': L1_sq,
            'Lam': Lam,
            'Lam_sq': Lam_sq,
            'Khat': Khat,
            'product': product,
        })

        if k == 0:
            label = "principal"
        else:
            label = f"χ_{k}"
        print(f"  {label:12s} ({parity:4s}): |L(1,χ)|²={L1_sq:10.4f}, |Λ|²={Lam_sq:10.4f}, K̂·|Λ|²={product:10.4f}")

    # Sums over odd characters
    odd_data = [d for d in data if d['parity'] == 'odd']
    even_data = [d for d in data if d['parity'] == 'even']

    sum_Khat_Lam = sum(d['product'] for d in odd_data)

    # Σ E(k)² = Σ λ_p(a)²
    sum_E_sq = compute_E_values(p, M_arr)

    # (p-1) · Σ E(k)² -- but actually by Parseval, Σ_χ |Λ_p(χ)|² = (p-1)·Σ λ_p(a)²
    parseval_check = sum(d['Lam_sq'] for d in data)
    parseval_expected = (p - 1) * sum_E_sq

    # Correlation analysis over odd characters
    if len(odd_data) > 2:
        log_L1_sq = [log(d['L1_sq']) for d in odd_data if d['L1_sq'] > 0]
        log_Lam_sq = [log(d['Lam_sq']) for d in odd_data if d['Lam_sq'] > 0]

        # Need to align - only include where both are positive
        pairs = [(log(d['L1_sq']), log(d['Lam_sq'])) for d in odd_data
                 if d['L1_sq'] > 1e-15 and d['Lam_sq'] > 1e-15]

        if len(pairs) > 2:
            x = np.array([p[0] for p in pairs])
            y = np.array([p[1] for p in pairs])
            corr = np.corrcoef(x, y)[0, 1]
        else:
            corr = float('nan')
    else:
        corr = float('nan')

    # Average |L(1,χ)|² over odd chars
    avg_L1_sq_odd = np.mean([d['L1_sq'] for d in odd_data]) if odd_data else 0
    avg_Lam_sq_odd = np.mean([d['Lam_sq'] for d in odd_data]) if odd_data else 0
    avg_Lam_sq_even = np.mean([d['Lam_sq'] for d in even_data]) if even_data else 0
    avg_Lam_sq_all = np.mean([d['Lam_sq'] for d in data])

    # Where does log p live?
    # Compare: sum_Khat_Lam / p² and log(p)
    ratio_sum_over_p2 = sum_Khat_Lam / p**2

    results[p] = {
        'data': data,
        'odd_data': odd_data,
        'even_data': even_data,
        'sum_Khat_Lam': sum_Khat_Lam,
        'sum_E_sq': sum_E_sq,
        'parseval_check': parseval_check,
        'parseval_expected': parseval_expected,
        'corr': corr,
        'avg_L1_sq_odd': avg_L1_sq_odd,
        'avg_Lam_sq_odd': avg_Lam_sq_odd,
        'avg_Lam_sq_even': avg_Lam_sq_even,
        'avg_Lam_sq_all': avg_Lam_sq_all,
        'ratio_sum_over_p2': ratio_sum_over_p2,
    }

    print(f"\n  SUMMARY for p={p}:")
    print(f"    # odd chars: {len(odd_data)}, # even chars: {len(even_data)}")
    print(f"    Σ_{{odd}} K̂·|Λ|² = {sum_Khat_Lam:.6f}")
    print(f"    Σ λ_p(a)²     = {sum_E_sq:.6f}")
    print(f"    (p-1)·Σλ²     = {parseval_expected:.6f}")
    print(f"    Σ_{{all}} |Λ|² = {parseval_check:.6f} (Parseval check)")
    print(f"    Avg |L(1,χ)|² (odd) = {avg_L1_sq_odd:.6f}")
    print(f"    Avg |Λ|² (odd)      = {avg_Lam_sq_odd:.6f}")
    print(f"    Avg |Λ|² (even)     = {avg_Lam_sq_even:.6f}")
    print(f"    Corr(log|L|², log|Λ|²) over odd = {corr:.6f}")
    print(f"    Σ K̂·|Λ|² / p² = {ratio_sum_over_p2:.6f}")
    print(f"    log(p) = {log(p):.6f}")

# ─── Cross-prime analysis ───
print("\n\n" + "="*80)
print("CROSS-PRIME ANALYSIS")
print("="*80)

print(f"\n{'p':>4} | {'#odd':>4} | {'ΣK̂|Λ|²':>12} | {'Σλ²':>10} | {'(p-1)Σλ²':>12} | {'Parseval':>12} | {'Avg|L|²odd':>11} | {'Avg|Λ|²odd':>11} | {'corr':>8} | {'ΣK̂|Λ|²/p²':>11} | {'logp':>8}")
print("-"*140)

for p in primes:
    r = results[p]
    print(f"{p:4d} | {len(r['odd_data']):4d} | {r['sum_Khat_Lam']:12.4f} | {r['sum_E_sq']:10.4f} | {r['parseval_expected']:12.4f} | {r['parseval_check']:12.4f} | {r['avg_L1_sq_odd']:11.6f} | {r['avg_Lam_sq_odd']:11.4f} | {r['corr']:8.4f} | {r['ratio_sum_over_p2']:11.6f} | {log(p):8.4f}")

# ─── Where does log p live? ───
print("\n\nWHERE DOES log(p) LIVE?")
print("="*60)
print(f"{'p':>4} | {'Avg|L|²_odd':>12} | {'Avg|L|²/logp':>12} | {'Avg|Λ|²_odd':>12} | {'Avg|Λ|²/p':>11} | {'ΣK̂|Λ|²/p²':>11} | {'ratio/logp':>10}")
print("-"*90)

for p in primes:
    r = results[p]
    lp = log(p)
    print(f"{p:4d} | {r['avg_L1_sq_odd']:12.6f} | {r['avg_L1_sq_odd']/lp:12.6f} | {r['avg_Lam_sq_odd']:12.4f} | {r['avg_Lam_sq_odd']/p:11.4f} | {r['ratio_sum_over_p2']:11.6f} | {r['ratio_sum_over_p2']/lp:10.6f}")

# ─── Which characters carry the most weight? ───
print("\n\nTOP CHARACTERS BY K̂·|Λ|² PRODUCT (for each p)")
print("="*60)

for p in primes:
    r = results[p]
    odd_sorted = sorted(r['odd_data'], key=lambda d: d['product'], reverse=True)
    total = r['sum_Khat_Lam']
    print(f"\np = {p}: total Σ K̂·|Λ|² = {total:.4f}")
    for i, d in enumerate(odd_sorted[:5]):
        frac = d['product'] / total * 100 if total > 0 else 0
        print(f"  χ_{d['k']:2d}: K̂·|Λ|² = {d['product']:10.4f} ({frac:5.1f}%), |L|²={d['L1_sq']:.4f}, |Λ|²={d['Lam_sq']:.4f}")

# ─── Ratio analysis: does Σ K̂·|Λ|² / p² grow as log p? ───
print("\n\nGROWTH ANALYSIS: Σ K̂·|Λ|² / p²  vs  log(p)")
print("="*60)

x_logp = np.array([log(p) for p in primes])
y_ratio = np.array([results[p]['ratio_sum_over_p2'] for p in primes])

# Fit linear: y = a·x + b
if len(primes) > 2:
    A = np.vstack([x_logp, np.ones(len(x_logp))]).T
    slope, intercept = np.linalg.lstsq(A, y_ratio, rcond=None)[0]
    print(f"  Linear fit: Σ K̂·|Λ|² / p² ≈ {slope:.6f} · log(p) + {intercept:.6f}")

    # Also try: y = a · (log p)^b
    log_y = np.log(np.abs(y_ratio) + 1e-15)
    log_x = np.log(x_logp)
    A2 = np.vstack([log_x, np.ones(len(log_x))]).T
    b_exp, log_a = np.linalg.lstsq(A2, log_y, rcond=None)[0]
    print(f"  Power fit:  Σ K̂·|Λ|² / p² ≈ {np.exp(log_a):.6f} · (log p)^{b_exp:.4f}")

# ─── Also check: Σ K̂·|Λ|² vs (p-1)·Σλ² ───
print("\n\nPARSEVAL-WEIGHTED COMPARISON")
print("="*60)
print(f"{'p':>4} | {'Σ_odd K̂|Λ|²':>14} | {'Σ_all |Λ|²':>14} | {'(p-1)Σλ²':>14} | {'K̂-weighted/all':>14}")
print("-"*70)

for p in primes:
    r = results[p]
    ratio = r['sum_Khat_Lam'] / r['parseval_check'] if r['parseval_check'] > 0 else 0
    print(f"{p:4d} | {r['sum_Khat_Lam']:14.4f} | {r['parseval_check']:14.4f} | {r['parseval_expected']:14.4f} | {ratio:14.6f}")

# ─── Decompose: avg K̂ over odd chars, avg |Λ|² over odd chars ───
print("\n\nDECOMPOSITION: Σ K̂·|Λ|² = (#odd) · Avg(K̂) · Avg(|Λ|²) · (1 + cov_term)")
print("="*70)
print(f"{'p':>4} | {'#odd':>4} | {'Avg K̂':>10} | {'Avg|Λ|²':>10} | {'naive product':>14} | {'actual sum':>12} | {'cov factor':>10}")
print("-"*80)

for p in primes:
    r = results[p]
    n_odd = len(r['odd_data'])
    avg_Khat = np.mean([d['Khat'] for d in r['odd_data']]) if n_odd > 0 else 0
    avg_Lam = r['avg_Lam_sq_odd']
    naive = n_odd * avg_Khat * avg_Lam
    actual = r['sum_Khat_Lam']
    cov_factor = actual / naive if naive > 0 else float('nan')
    print(f"{p:4d} | {n_odd:4d} | {avg_Khat:10.4f} | {avg_Lam:10.4f} | {naive:14.4f} | {actual:12.4f} | {cov_factor:10.6f}")

# ─── Track scaling of components ───
print("\n\nSCALING OF COMPONENTS WITH p")
print("="*60)
print(f"{'p':>4} | {'Avg K̂ odd':>10} | {'K̂/p':>8} | {'K̂/(p·logp)':>11} | {'Avg|Λ|²odd':>11} | {'|Λ|²/logp':>9} | {'#odd·AvgK̂·Avg|Λ|²/p²':>22}")
print("-"*95)

for p in primes:
    r = results[p]
    n_odd = len(r['odd_data'])
    avg_Khat = np.mean([d['Khat'] for d in r['odd_data']]) if n_odd > 0 else 0
    avg_Lam = r['avg_Lam_sq_odd']
    lp = log(p)
    normalized = n_odd * avg_Khat * avg_Lam / p**2
    print(f"{p:4d} | {avg_Khat:10.4f} | {avg_Khat/p:8.4f} | {avg_Khat/(p*lp):11.6f} | {avg_Lam:11.4f} | {avg_Lam/lp:9.4f} | {normalized:22.6f}")

print("\n\nDone.")
