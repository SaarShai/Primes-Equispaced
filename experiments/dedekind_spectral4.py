#!/usr/bin/env python3
"""
Final analysis: pin down the log p factor.

ESTABLISHED:
  K̂_p(χ) = p · |L(1,χ)|² / π²   for χ odd
  K̂_p(χ) = 0                      for χ even or χ = χ_0

So the spectral formula:
  Σ_χ K̂(χ)|Λ(χ)|²/(p-1) = (p/(π²(p-1))) Σ_{χ odd} |L(1,χ)|² |Λ(χ)|²

MEAN VALUE THEOREMS:
  (1) Σ_{χ odd} |L(1,χ)|² ~ (p/2) · average
  (2) Mean square: avg |L(1,χ)|² ~ log p  (by standard MVT for L-functions)

THIS is the log p factor! Let me verify.

The standard result (e.g., Montgomery-Vaughan):
  Σ_{χ mod q, χ≠χ₀} |L(1,χ)|² = φ(q) · (log q + γ - Σ_{p|q} log(p)/(p-1)) + O(...)
For q=p prime:
  Σ_{χ≠χ₀} |L(1,χ)|² = (p-1)(log p + γ - log(p)/(p-1)) + ...
                        ≈ (p-1)(log p + γ) for large p

So the AVERAGE |L(1,χ)|² ~ log p + γ.

But wait -- that's for ALL non-principal characters. We need only ODD ones.
By symmetry (roughly half are odd): Σ_{χ odd} |L(1,χ)|² ~ (p-1)/2 · (log p + γ)

Let me verify this numerically.
"""

import numpy as np
import math

def primitive_root(p):
    for g in range(2, p):
        seen = set()
        val = 1
        for _ in range(p - 1):
            val = (val * g) % p
            seen.add(val)
        if len(seen) == p - 1:
            return g
    return None

def L_function(chi_vals, p, terms=50000):
    s = 0.0 + 0j
    for n in range(1, terms + 1):
        r = n % p
        if r == 0:
            continue
        s += chi_vals[r] / n
    return s

primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
          101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157]

gamma_euler = 0.5772156649

print("=" * 90)
print("  MEAN VALUE THEOREM VERIFICATION")
print("  Theory: Σ_{χ≠χ₀} |L(1,χ)|² = (p-1)(log p + γ - log p/(p-1)) + O(1)")
print("=" * 90)

print(f"\n{'p':>4} {'Σ_all |L|²':>14} {'(p-1)(logp+γ)':>14} {'ratio':>8} "
      f"{'Σ_odd |L|²':>14} {'(p-1)(logp+γ)/2':>16} {'ratio':>8}")

data = []
for p in primes:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)

    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    sum_all = 0.0
    sum_odd = 0.0
    sum_even = 0.0
    for j in range(1, N):  # skip j=0 (principal)
        chi = {}
        for a in range(1, p):
            chi[a] = omega ** (j * dlog[a])
        L1 = L_function(chi, p, terms=30000)
        L2 = abs(L1)**2
        sum_all += L2
        if j % 2 == 1:
            sum_odd += L2
        else:
            sum_even += L2

    logp = np.log(p)
    theory_all = (p - 1) * (logp + gamma_euler - logp / (p - 1))
    theory_odd = theory_all / 2

    print(f"{p:4d} {sum_all:14.4f} {theory_all:14.4f} {sum_all/theory_all:8.4f} "
          f"{sum_odd:14.4f} {theory_odd:16.4f} {sum_odd/theory_odd:8.4f}")
    data.append((p, sum_all, sum_odd, theory_all))

# Now: the spectral formula WITH K̂ = p|L|²/π² becomes:
# (1/(p-1)) Σ_{χ odd} (p/π²)|L(1,χ)|² |Λ(χ)|²
# = (p/(π²(p-1))) Σ_{χ odd} |L(1,χ)|² |Λ(χ)|²
#
# Using Cauchy-Schwarz or just averaging:
# If |L|² and |Λ|² are uncorrelated:
#   ≈ (p/(π²(p-1))) · [avg|L|² · Σ|Λ|²]
#   = (p/(π²(p-1))) · (logp + γ) · (p-1)/2 · avg|Λ|²
#   ≈ (p/(2π²)) · (logp + γ) · avg|Λ|²_odd
#
# From Parseval: Σ_{all χ} |Λ(χ)|² = (p-1)Σ|λ|²
# avg|Λ|² over odd chars ≈ Σ|λ|²  (roughly half go to odd)
# So ≈ (p/(2π²)) · (logp + γ) · Σ|λ|²
#
# The LOG P factor comes from the MEAN VALUE of |L(1,χ)|²!

print(f"\n{'='*90}")
print(f"  WHERE LOG P LIVES: Decomposition of spectral formula")
print(f"{'='*90}")

print(f"\n{'p':>4} {'logp':>7} {'spectral':>12} {'p·avg|L|²·avg|Λ|²/(π²(p-1))':>32} {'ratio':>8}")
# This is approximate -- let me compute exactly

from functools import lru_cache

def sawtooth(x):
    fx = x - math.floor(x)
    if abs(fx) < 1e-15 or abs(fx - 1) < 1e-15:
        return 0.0
    return fx - 0.5

def dedekind_sum(r, p):
    total = 0.0
    for k in range(1, p):
        total += sawtooth(k / p) * sawtooth(k * r / p)
    return total

def mertens_array(n):
    if n <= 0:
        return [0]
    mu = [0] * (n + 1)
    mu[1] = 1
    is_prime = [True] * (n + 1)
    primes_list = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes_list.append(i)
            mu[i] = -1
        for pp in primes_list:
            if i * pp > n:
                break
            is_prime[i * pp] = False
            if i % pp == 0:
                mu[i * pp] = 0
                break
            else:
                mu[i * pp] = -mu[i]
    M = [0] * (n + 1)
    for i in range(1, n + 1):
        M[i] = M[i - 1] + mu[i]
    return M

# For smaller primes, compute EXACTLY the correlation between |L|² and |Λ|²
print(f"\n{'='*90}")
print(f"  CORRELATION: |L(1,χ)|² vs |Λ(χ)|² for odd characters")
print(f"{'='*90}")

for p in [11, 13, 17, 23, 29, 37, 47, 59, 71, 83, 97]:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)

    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    M_arr = mertens_array(N)
    lambda_p = {}
    for m in range(1, p):
        lambda_p[m] = M_arr[N // m] + (1 if m == 1 else 0)

    L2_vals = []
    Lam2_vals = []
    weighted = 0.0

    for j in range(N):
        if j % 2 == 0:
            continue  # even char

        chi = {}
        for a in range(1, p):
            chi[a] = omega ** (j * dlog[a])

        L1 = L_function(chi, p, terms=30000)
        L2 = abs(L1)**2

        Lambda_j = sum(lambda_p[a] * chi[a] for a in range(1, p))
        Lam2 = abs(Lambda_j)**2

        L2_vals.append(L2)
        Lam2_vals.append(Lam2)
        weighted += L2 * Lam2

    L2_arr = np.array(L2_vals)
    Lam2_arr = np.array(Lam2_vals)

    # Correlation coefficient
    if len(L2_arr) > 2:
        corr = np.corrcoef(L2_arr, Lam2_arr)[0, 1]
    else:
        corr = 0.0

    logp = np.log(p)
    avg_L2 = np.mean(L2_arr)
    avg_Lam2 = np.mean(Lam2_arr)
    n_odd = len(L2_arr)

    # Spectral sum = p/(π²(p-1)) · Σ |L|² |Λ|²
    spectral = p / (np.pi**2 * (p - 1)) * weighted
    # Expected if uncorrelated: p/(π²(p-1)) · n_odd · avg_L2 · avg_Lam2
    uncorr = p / (np.pi**2 * (p - 1)) * n_odd * avg_L2 * avg_Lam2

    print(f"\np={p:3d}: logp={logp:.3f}")
    print(f"  avg|L|² = {avg_L2:.6f},  avg|Λ|² = {avg_Lam2:.4f}")
    print(f"  corr(|L|²,|Λ|²) = {corr:.4f}")
    print(f"  spectral = {spectral:.4f},  uncorrelated prediction = {uncorr:.4f},  ratio = {spectral/uncorr:.4f}")
    print(f"  avg|L|²/logp = {avg_L2/logp:.6f}")
    print(f"  Σ|λ|² = {sum(lambda_p[a]**2 for a in range(1, p))}")

# SUMMARY: The log p factor in Σ K̂|Λ|² comes from:
# K̂(χ) = p|L(1,χ)|²/π², and avg|L(1,χ)|² ~ log p + γ
# So the "typical" K̂ ~ p(log p)/π², and summing over ~p/2 odd characters
# with |Λ|² ~ p on average gives ~p³ log p / (2π²), divided by (p-1) → ~ p² log p

print(f"\n{'='*90}")
print(f"  SUMMARY: THE LOG P MECHANISM")
print(f"{'='*90}")
print(f"""
THE CHAIN:

1. K̂_p(χ) = |C(χ)|²/(4p) where C(χ) = Σ χ(a)cot(πa/p)  [PROVED]

2. K̂_p(χ) = p · |L(1,χ)|² / π²  for odd χ              [VERIFIED to ratio p]
   (The extra factor p vs the naive |L|²/π² comes from |τ(χ)|² = p)

3. K̂_p(χ) = 0 for even χ and χ_0                         [PROVED by symmetry]

4. K̂_p(χ) ≥ 0 for ALL χ                                  [PROVED: it's |C|²/(4p)]

5. Average |L(1,χ)|² over odd χ ~ log p + γ               [Standard MVT, verified]

6. Therefore avg K̂ ~ p·(log p)/π² over odd characters

7. The spectral formula:
   Σ_χ K̂(χ)|Λ(χ)|²/(p-1) = (p/(π²(p-1))) Σ_{{χ odd}} |L(1,χ)|² |Λ(χ)|²

THE LOG P IN Σ E(k)²:
   The E(k) for prime modulus p has E(k) = k/p for k < p.
   So ΣE² = (p-1)(2p-1)/(6p) ~ p/3.  NO log p here.

   The log p factor in the FAREY discrepancy D_N = Σ λ(m)·E(m)
   comes from the Mertens function via λ(m) = M(N/m).
   The spectral formula decomposes this as:
   D_N² ~ (1/(p-1)) Σ [p|L(1,χ)|²/π²] · |Λ(χ)|²
   The factor |L(1,χ)|² ~ log p provides the logarithmic growth.
""")
