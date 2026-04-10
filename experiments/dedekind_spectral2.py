#!/usr/bin/env python3
"""
Second pass: Fix formula, find logp, deeper analysis.

KEY OBSERVATIONS from first run:
1. K̂_p(χ) >= 0 for ALL characters, ALL primes tested (HUGE!)
2. K̂ is REAL for all characters (Dedekind sums are odd-ish)
3. K̂(χ_0) = 0 (principal char gives zero -- sum of Dedekind sums vanishes)
4. K̂ vanishes on EVEN characters (j even), nonzero only on ODD characters
5. The spectral formula gives different value from direct ΣE² -- need to check formula

Let me re-derive and check what the formula ACTUALLY computes.
Also: identify K̂_p(χ) in terms of L-functions.
"""

import numpy as np
import math

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
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for pp in primes:
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

# ============================================================
# KNOWN IDENTITY: For p prime, the Dedekind sum satisfies
#   s(r,p) = (1/(4p)) * Σ_{k=1}^{p-1} cot(πk/p) cot(πkr/p)
#
# And for the character transform:
#   K̂_p(χ) = Σ_{r=1}^{p-1} s(r,p) χ(r)
#           = (1/(4p)) Σ_k cot(πk/p) Σ_r χ(r) cot(πkr/p)
#
# The inner sum Σ_r χ(r) cot(πkr/p) is a Gauss-type sum.
# For χ odd (χ(-1) = -1): relates to L(1,χ) via
#   L(1,χ) = -(π/(p·τ(χ̄))) Σ_{a=1}^{p-1} χ̄(a) a ... (Hurwitz)
# ============================================================

# Focus: What does K̂ look like in terms of p?
# Hypothesis: K̂_p(χ) ~ (p-1)/(2π²) · L(2,χ) for some normalization

primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

print("=" * 80)
print("  DEDEKIND KERNEL: IDENTIFYING K̂_p(χ) STRUCTURE")
print("=" * 80)

# For each prime, compute K̂ for the "generator" odd character
# and relate to known L-function values

for p in primes:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)

    # Discrete log
    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    # Dedekind sums
    ded = [0.0] * p
    for r in range(1, p):
        ded[r] = dedekind_sum(r, p)

    # K̂ for all chars
    K_hat = []
    for j in range(N):
        s = 0.0 + 0j
        for r in range(1, p):
            s += ded[r] * omega ** (j * dlog[r])
        K_hat.append(s.real)  # They're all real

    # Identify which K̂ are nonzero
    nonzero_K = [(j, K_hat[j]) for j in range(N) if abs(K_hat[j]) > 1e-10]

    # Theoretical: s(r,p) is an ODD function mod p: s(p-r,p) = -s(r,p)
    # So K̂_p(χ) = Σ s(r,p) χ(r) vanishes unless χ is ODD (χ(-1)=-1)
    # Check: j is odd character iff χ_j(-1) = -1
    # χ_j(-1) = ω^{j·dlog(p-1)} = ω^{j·(N/2)} = e^{iπj} = (-1)^j
    # So χ_j is odd iff j is odd!

    # For odd j: K̂_p(χ_j) > 0 -- this is the positivity result

    # max K̂
    max_K = max(K_hat)

    # Known: for the Legendre symbol χ_L (quadratic character, j=N/2),
    # s(r,p) relates to class number via Dedekind reciprocity

    # Key: K̂_p(χ_j) for j=1 (primitive generator character)
    K1 = K_hat[1] if len(K_hat) > 1 else 0

    # Cotangent formula: s(r,p) = (1/4p) Σ_{k=1}^{p-1} cot(πk/p) cot(πkr/p)
    # So K̂(χ_j) = (1/4p) Σ_k cot(πk/p) · [Σ_r χ_j(r) cot(πkr/p)]

    # The bracket is: Σ_r χ_j(r) cot(πkr/p)
    # For χ_j primitive: this equals χ_j(k^{-1}) · (-iπ/τ(χ_j)) · (something)
    # Actually: Σ_r χ(r) cot(πkr/p) = -(2/τ(χ̄)) · χ̄(k) · Σ_{n=1}^∞ χ(n)/n ... no

    # Let's just compute the ratio K̂_p(χ_1) / (p/12) and K̂ / log(p)
    print(f"\np={p:3d}: K̂(χ_1)={K1:8.4f}, max K̂={max_K:8.4f}, p/12={p/12:.4f}, "
          f"K̂₁/(p/12)={K1/(p/12):.4f}, max_K/p={max_K/p:.5f}, "
          f"max_K/(p*logp/(12))={12*max_K/(p*np.log(p)):.5f}")

print("\n" + "=" * 80)
print("  SCALING TABLE: max K̂ and the p/12 normalization")
print("=" * 80)

print(f"\n{'p':>4} {'logp':>7} {'maxK̂':>10} {'maxK̂·12/p':>12} {'maxK̂/(p·logp/12)':>18} {'K̂(χ₁)':>10} {'K̂₁·12/p':>10}")
scaling_data = []
for p in primes:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)
    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    ded = [0.0] * p
    for r in range(1, p):
        ded[r] = dedekind_sum(r, p)

    K_hat = []
    for j in range(N):
        s = 0.0 + 0j
        for r in range(1, p):
            s += ded[r] * omega ** (j * dlog[r])
        K_hat.append(s.real)

    max_K = max(K_hat)
    K1 = K_hat[1]

    logp = np.log(p)
    print(f"{p:4d} {logp:7.3f} {max_K:10.4f} {12*max_K/p:12.4f} {12*max_K/(p*logp):18.5f} {K1:10.4f} {12*K1/p:10.4f}")
    scaling_data.append((p, logp, max_K, K1))

# Now check: does maxK̂ ~ p/(2π²)·log(p)?
print(f"\n{'p':>4} {'maxK̂':>10} {'p·logp/(2π²)':>14} {'ratio':>8}")
for p, logp, max_K, K1 in scaling_data:
    theory = p * logp / (2 * np.pi**2)
    print(f"{p:4d} {max_K:10.4f} {theory:14.4f} {max_K/theory:8.4f}")

# Check: maxK̂ ~ p·logp/12 ?
print(f"\n{'p':>4} {'maxK̂':>10} {'p·logp/12':>12} {'ratio':>8}  | {'(p-1)/(2π²)·logp':>18} {'ratio':>8}")
for p, logp, max_K, K1 in scaling_data:
    t1 = p * logp / 12
    t2 = (p-1) / (2 * np.pi**2) * logp
    print(f"{p:4d} {max_K:10.4f} {t1:12.4f} {max_K/t1:8.4f}  | {t2:18.4f} {max_K/t2:8.4f}")

# KEY QUESTION: Where does logp appear in the SPECTRAL FORMULA?
# Σ E(k)² = (1/(p-1)) Σ_χ K̂(χ) |Λ(χ)|²
# If K̂(χ) ~ C·p for odd χ (with some χ-dependent constant)
# and |Λ(χ)|² ~ p on average (Parseval gives (p-1) Σ|λ|²)
# then Σ K̂|Λ|² ~ C·p · p · (p-1)/2 characters
# giving ΣE² ~ C·p²/2
# But we expect ΣE² ~ C'·log(p)
# So something must cancel...

# Let me check: what is Σ|λ(a)|² as a function of p?
print(f"\n{'='*80}")
print(f"  Σ|λ(a)|² and hyperbolic-sum structure")
print(f"{'='*80}")

print(f"\n{'p':>4} {'logp':>7} {'Σ|λ|²':>10} {'Σ|λ|²/p':>10} {'Σ|λ|²/logp':>12} {'Σ|λ|²/(p·logp)':>16}")
for p in primes:
    N = p - 1
    M_arr = mertens_array(N)
    sum_lam2 = 0
    for m in range(1, p):
        lam = M_arr[N // m] + (1 if m == 1 else 0)
        sum_lam2 += lam * lam
    logp = np.log(p)
    print(f"{p:4d} {logp:7.3f} {sum_lam2:10d} {sum_lam2/p:10.4f} {sum_lam2/logp:12.4f} {sum_lam2/(p*logp):16.6f}")

# Σ|λ(a)|² = Σ_{m=1}^{N} [M(⌊N/m⌋) + δ_{m,1}]²
# The dominant term is Σ_{m=1}^N M(⌊N/m⌋)²
# This is a HYPERBOLIC SUM of Mertens function squared.
# By standard results: Σ_{m≤N} M(⌊N/m⌋)² relates to Σ_{n≤N} 1/n ~ log N

print(f"\n{'='*80}")
print(f"  DIRECT ΣE² scaling")
print(f"{'='*80}")

# Direct computation of ΣE² for many primes
print(f"\n{'p':>4} {'logp':>7} {'ΣE²':>12} {'ΣE²/logp':>12} {'12·ΣE²/logp':>14} {'ΣE²·p':>12}")
for p in primes:
    N = p - 1
    sum_E2 = 0.0
    for k in range(1, p):
        count = k - k // p  # #{1<=m<=k : p∤m} -- for k<p, this is just k
        E_k = count - k * (p - 1) / p
        sum_E2 += E_k ** 2
    logp = np.log(p)
    print(f"{p:4d} {logp:7.3f} {sum_E2:12.6f} {sum_E2/logp:12.6f} {12*sum_E2/logp:14.6f} {sum_E2*p:12.4f}")

# Wait -- for k < p, count = k (nothing divisible by p in 1..k when k<p)
# So E(k) = k - k(p-1)/p = k/p
# Therefore ΣE² = Σ_{k=1}^{p-1} (k/p)² = (1/p²) Σ k² = (p-1)p(2p-1)/(6p²)
# = (p-1)(2p-1)/(6p)

print(f"\n{'='*80}")
print(f"  EXACT: ΣE² = (p-1)(2p-1)/(6p) for prime p")
print(f"{'='*80}")
print(f"\n{'p':>4} {'ΣE²':>12} {'(p-1)(2p-1)/6p':>16} {'match':>6}")
for p in primes:
    sum_E2 = 0.0
    for k in range(1, p):
        E_k = k / p
        sum_E2 += E_k ** 2
    theory = (p - 1) * (2 * p - 1) / (6 * p)
    print(f"{p:4d} {sum_E2:12.6f} {theory:16.6f} {'YES' if abs(sum_E2-theory)<1e-8 else 'NO':>6}")

# So ΣE² = (p-1)(2p-1)/(6p) ~ p/3 for large p
# There is NO logp factor in ΣE² for the Farey-level discrepancy!
# The logp lives elsewhere -- in the PER-STEP discrepancy variance.

# NOW: The spectral formula mismatch.
# Our formula gives (1/(p-1)) Σ K̂|Λ|² which is NOT equal to ΣE².
# This means the codex formula is either:
# (a) for a DIFFERENT quantity (not the simple discrepancy E(k) = k/p)
# (b) has different normalization
# (c) is for the Farey discrepancy, not the mod-p discrepancy

# Let me check: what does the spectral formula ACTUALLY equal?
print(f"\n{'='*80}")
print(f"  WHAT DOES THE SPECTRAL FORMULA COMPUTE?")
print(f"{'='*80}")

print(f"\n{'p':>4} {'spectral':>12} {'ΣE²':>12} {'ratio':>8} {'Σ|λ|²':>8} {'spec/(Σ|λ|²)':>14}")
for p in primes:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)
    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    ded = [0.0] * p
    for r in range(1, p):
        ded[r] = dedekind_sum(r, p)

    M_arr = mertens_array(N)
    lambda_p = {}
    for m in range(1, p):
        lambda_p[m] = M_arr[N // m] + (1 if m == 1 else 0)

    K_hat = []
    Lambda = []
    for j in range(N):
        sk = 0.0 + 0j
        sl = 0.0 + 0j
        for r in range(1, p):
            chi_r = omega ** (j * dlog[r])
            sk += ded[r] * chi_r
            sl += lambda_p[r] * chi_r
        K_hat.append(sk.real)
        Lambda.append(sl)

    spectral = sum(K_hat[j] * abs(Lambda[j])**2 for j in range(N)) / N
    sum_E2 = (p - 1) * (2 * p - 1) / (6 * p)
    sum_lam2 = sum(lambda_p[m]**2 for m in range(1, p))

    print(f"{p:4d} {spectral:12.4f} {sum_E2:12.4f} {spectral/sum_E2 if sum_E2>0 else 0:8.4f} {sum_lam2:8.1f} {spectral/sum_lam2:14.6f}")

# What if the spectral formula computes Σ_{k} (Σ_{m≤k} λ(m))² in real space?
# i.e., convolution of Dedekind kernel with λ?
print(f"\n{'='*80}")
print(f"  CONVOLUTION CHECK")
print(f"{'='*80}")

for p in [11, 13, 17]:
    N = p - 1
    M_arr = mertens_array(N)

    # Compute Σ_{a,b} s(ab^{-1}, p) λ(a) λ(b) where ab^{-1} is mod p
    conv = 0.0
    ded = {}
    for r in range(1, p):
        ded[r] = dedekind_sum(r, p)

    for a in range(1, p):
        for b in range(1, p):
            # ab^{-1} mod p
            ab_inv = (a * pow(b, p-2, p)) % p
            lam_a = M_arr[N // a] + (1 if a == 1 else 0)
            lam_b = M_arr[N // b] + (1 if b == 1 else 0)
            conv += ded[ab_inv] * lam_a * lam_b
    conv /= (p - 1)

    # Compare to spectral
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)
    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    K_hat = []
    Lambda = []
    for j in range(N):
        sk = 0.0 + 0j
        sl = 0.0 + 0j
        for r in range(1, p):
            chi_r = omega ** (j * dlog[r])
            sk += ded[r] * chi_r
            sl += (M_arr[N // r] + (1 if r == 1 else 0)) * chi_r
        K_hat.append(sk.real)
        Lambda.append(sl)

    spectral = sum(K_hat[j] * abs(Lambda[j])**2 for j in range(N)) / N

    print(f"p={p}: convolution = {conv:.6f}, spectral = {spectral:.6f}, match = {abs(conv-spectral)<1e-6}")

# The spectral formula computes the Dedekind-weighted L2 norm.
# Now the KEY question: where is log p?

# K̂_p(χ) for odd primitive χ: known to relate to L(2,sym²χ) or similar
# Let me test: K̂_p(χ_j) vs L-function values

print(f"\n{'='*80}")
print(f"  K̂ vs COTANGENT SUMS (exact)")
print(f"{'='*80}")

# K̂(χ_j) = Σ_r s(r,p) χ_j(r)
# s(r,p) = (1/4p) Σ_k cot(πk/p) cot(πkr/p)  [standard]
# So K̂(χ_j) = (1/4p) Σ_k cot(πk/p) · C_j(k)
# where C_j(k) = Σ_r χ_j(r) cot(πkr/p)
#
# For ODD primitive χ_j:
#   Σ_{r=1}^{p-1} χ_j(r) cot(πkr/p) = -(2i/τ(χ_j)) · χ_j(-k) · L(1,χ_j)
# Hmm, not quite. Let me use the formula directly.
#
# Actually: Σ_{a=1}^{p-1} χ(a) ((a/p)) = -(1/(2πi)) · τ(χ) · L(1,χ̄) for χ primitive
# And cot(πa/p) = 2((a/p)) / (something)... no.
#
# Better: For χ odd primitive mod p:
#   Σ_{a=1}^{p-1} χ(a) · a = τ(χ) · p / (2πi) · L(1,χ̄)  ... no
#
# The cleanest formula: for p prime, χ odd primitive mod p:
#   L(1,χ) = -π/(τ(χ̄)·p) · Σ_{a=1}^{p-1} χ̄(a)·a·(p - 2⌊ap/p⌋ -1)... complicated
#
# Let me just check numerically: K̂_p(χ_j) / (p/12)

for p in [11, 13, 17, 19, 23]:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)
    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    ded = {}
    for r in range(1, p):
        ded[r] = dedekind_sum(r, p)

    # Reciprocity: s(1,p) = (p² + p + 1 - 3p) / (12p) = (p-1)(p-2)/(12p) ... wait
    # s(1,p) = (p-1)(p-2)/(12p) by direct computation
    s1_theory = (p-1)*(p-2)/(12*p)

    print(f"\np={p}: s(1,p) = {ded[1]:.8f}, theory (p-1)(p-2)/12p = {s1_theory:.8f}")

    # K̂ values (odd j only)
    for j in range(N):
        if j % 2 == 1:  # odd characters
            sk = sum(ded[r] * (omega ** (j * dlog[r])).real for r in range(1, p))
            # Normalize by p/12
            print(f"  j={j}: K̂ = {sk:.6f}, K̂·12/p = {12*sk/p:.6f}, K̂·12/(p-1) = {12*sk/(p-1):.6f}")
