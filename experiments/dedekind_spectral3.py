#!/usr/bin/env python3
"""
Third pass: Identify K̂_p(χ) exactly.

KEY FINDINGS SO FAR:
1. K̂_p(χ) >= 0 for ALL odd χ, = 0 for all even χ and χ_0
2. K̂_p(χ) is REAL for all χ
3. ΣE² = (p-1)(2p-1)/(6p) ~ p/3 (NO log p in the simple discrepancy)
4. The spectral formula computes something DIFFERENT from ΣE²

THEORETICAL ATTACK:
s(r,p) = (1/4p) Σ_{k=1}^{p-1} cot(πk/p) cot(πkr/p)

K̂_p(χ) = Σ_r s(r,p) χ(r)
        = (1/4p) Σ_k cot(πk/p) [Σ_r χ(r) cot(πkr/p)]

For χ odd primitive mod p:
  Σ_{r=1}^{p-1} χ(r) cot(πkr/p) = (2i/π) τ(χ) L(1,χ̄)... no

Let me use the EXACT formula:
  For χ odd primitive mod p, the Gauss-type cotangent sum is:
  Σ_{a=1}^{p-1} χ(a) cot(πa/p) = 2i·τ(χ)/p · Σ_{n=1}^{∞} χ̄(n)/n
                                  = 2i·τ(χ)·L(1,χ̄)/p

Wait, the standard result is:
  L(1,χ) = -π/(i·p·τ(χ̄)) · Σ_{a=1}^{p-1} a·χ(a)   for χ odd

And for cotangent:
  Σ_{a=1}^{p-1} χ(a)·cot(πak/p) = χ̄(k) · Σ_{a=1}^{p-1} χ(a)·cot(πa/p)

This is because cot(πakr/p) = cot(π(a')/p) where a' ≡ akr mod p.

So: K̂_p(χ) = (1/4p) [Σ_k cot(πk/p) · χ̄(k)] · [Σ_a χ(a) cot(πa/p)]
            = (1/4p) · |C(χ)|²

where C(χ) = Σ_{a=1}^{p-1} χ(a) cot(πa/p).

THIS explains positivity! K̂_p(χ) = |C(χ)|²/(4p) >= 0 always!

Now: C(χ) = Σ χ(a) cot(πa/p).
For χ odd: C(χ) is pure imaginary (since cot is "even-ish" and χ is odd).
Actually cot(π(p-a)/p) = -cot(πa/p), so for χ odd:
  C(χ) = Σ χ(a) cot(πa/p), with χ(p-a) = -χ(a) and cot(π(p-a)/p) = -cot(πa/p)
  So paired: χ(a)cot(πa/p) + χ(p-a)cot(π(p-a)/p) = χ(a)cot(πa/p) + χ(a)cot(πa/p) = 2χ(a)cot(πa/p)
  C(χ) = 2 Σ_{a=1}^{(p-1)/2} χ(a) cot(πa/p).  This is REAL for real χ.

Actually let me just verify: K̂ = |C|²/(4p)
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

primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

print("=" * 80)
print("  VERIFY: K̂_p(χ) = |C(χ)|² / (4p)")
print("  where C(χ) = Σ_{a=1}^{p-1} χ(a) cot(πa/p)")
print("=" * 80)

for p in [11, 13, 17, 23]:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)

    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    # Dedekind sums
    ded = {}
    for r in range(1, p):
        ded[r] = dedekind_sum(r, p)

    # K̂ from definition
    K_hat = []
    for j in range(N):
        s = 0.0
        for r in range(1, p):
            s += ded[r] * (omega ** (j * dlog[r])).real
        K_hat.append(s)

    # C(χ) = Σ χ(a) cot(πa/p)
    C_chi = []
    for j in range(N):
        c = 0.0 + 0j
        for a in range(1, p):
            c += omega ** (j * dlog[a]) * (1.0 / math.tan(math.pi * a / p))
        C_chi.append(c)

    # K̂_predicted = |C(χ_j)|² * |C(χ̄_j)|² / (4p) ... no
    # Actually: K̂(χ) = (1/4p) Σ_k cot(πk/p) χ̄(k) · Σ_r χ(r) cot(πr/p)
    # Wait, let me be more careful.
    #
    # K̂(χ_j) = (1/4p) Σ_k cot(πk/p) · [Σ_r χ_j(r) cot(πkr/p)]
    #
    # Now Σ_r χ_j(r) cot(πkr/p):
    # Let r' = kr mod p, so r = k^{-1}r' mod p
    # Σ_r χ_j(r) cot(πr'/p) = χ_j(k^{-1}) Σ_{r'} χ_j(r') cot(πr'/p)
    # = χ̄_j(k) · C(χ_j)
    #
    # So K̂(χ_j) = (1/4p) · C(χ_j) · Σ_k cot(πk/p) χ̄_j(k)
    #            = (1/4p) · C(χ_j) · C(χ̄_j)
    #            = (1/4p) · C(χ_j) · conj(C(χ_j))   [since C(χ̄) = conj(C(χ)) when entries are real]
    #
    # Wait: C(χ̄_j) = Σ χ̄_j(a) cot(πa/p) = conj(Σ χ_j(a) cot(πa/p)) = conj(C(χ_j))
    # So K̂(χ_j) = |C(χ_j)|² / (4p)

    print(f"\np = {p}:")
    print(f"  {'j':>3} {'K̂(direct)':>12} {'|C|²/4p':>12} {'match':>6} {'|C(χ)|':>10}")
    for j in range(N):
        predicted = abs(C_chi[j])**2 / (4 * p)
        match = abs(K_hat[j] - predicted) < 1e-8
        print(f"  {j:3d} {K_hat[j]:12.6f} {predicted:12.6f} {'YES' if match else 'NO':>6} {abs(C_chi[j]):10.6f}")

# CONFIRMED! K̂_p(χ) = |C(χ)|²/(4p) where C(χ) = Σ χ(a) cot(πa/p)
# This PROVES positivity.

print("\n" + "=" * 80)
print("  RELATING C(χ) TO L-FUNCTIONS")
print("=" * 80)

# For χ odd primitive mod p:
#   L(1,χ) = -π/(p·τ(χ̄)) · B_{1,χ}
# where B_{1,χ} = Σ_{a=1}^{p-1} χ(a)·a/p = (1/p)Σ χ(a)·a
#
# Also known: Σ_{a=1}^{p-1} χ(a) cot(πa/p) = (2i/π) · τ(χ) · L(1,χ̄)  for χ ODD
# (This is eq. 9.8 in Iwaniec-Kowalski or similar)
#
# So C(χ) = (2i/π) · τ(χ) · L(1,χ̄)  for χ odd
# |C(χ)|² = (4/π²) · |τ(χ)|² · |L(1,χ̄)|² = (4/π²) · p · |L(1,χ)|²
# (using |τ(χ)|² = p and |L(1,χ̄)| = |L(1,χ)|)
#
# Therefore: K̂_p(χ) = |C(χ)|²/(4p) = (4p·|L(1,χ)|²)/(4p·π²) = |L(1,χ)|²/π²
#
# THIS IS HUGE: K̂_p(χ) = |L(1,χ)|² / π²

# Let me verify this numerically!
print("\nVerifying K̂_p(χ) = |L(1,χ)|² / π² ...")

def L_function(chi_vals, p, terms=10000):
    """Compute L(1,χ) = Σ_{n=1}^∞ χ(n)/n approximately."""
    s = 0.0 + 0j
    for n in range(1, terms + 1):
        r = n % p
        if r == 0:
            continue
        s += chi_vals[r] / n
    return s

for p in [11, 13, 17, 23, 29, 37, 47]:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)

    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    # Compute K̂ directly
    ded = {}
    for r in range(1, p):
        ded[r] = dedekind_sum(r, p)

    print(f"\np = {p}:")
    print(f"  {'j':>3} {'K̂(direct)':>12} {'|L(1,χ)|²/π²':>14} {'ratio':>8}")

    for j in [1, 3, N//2]:  # sample odd characters
        if j % 2 == 0:
            continue
        if j >= N:
            continue

        # χ_j values
        chi = {}
        for a in range(1, p):
            chi[a] = omega ** (j * dlog[a])

        # K̂ direct
        Kj = sum(ded[r] * chi[r].real for r in range(1, p))

        # L(1, χ_j)
        L1 = L_function(chi, p, terms=50000)

        predicted = abs(L1)**2 / (np.pi**2)

        print(f"  {j:3d} {Kj:12.6f} {predicted:14.6f} {Kj/predicted if predicted > 1e-10 else 'inf':>8}")

# Now: The spectral formula becomes:
# Σ K̂(χ)|Λ(χ)|²/(p-1)
# = Σ_{χ odd} |L(1,χ)|²|Λ(χ)|² / (π²(p-1))
#
# The log p factor must come from:
# (a) max |L(1,χ)| ~ log log p (known)
# (b) Σ_{χ odd} |L(1,χ)|² ~ (p/2)·log p (this would be the source!)
#
# Let me verify: Σ_{χ odd} |L(1,χ)|²

print("\n" + "=" * 80)
print("  MEAN VALUE: Σ_{χ odd} |L(1,χ)|²")
print("=" * 80)

# Known: Σ_{χ mod p} |L(1,χ)|² = (p-1)·(π²/6)·(1 - 1/p²)/(1) ... approximately
# Actually the mean value theorem gives:
# (1/(p-1)) Σ_{χ≠χ_0} |L(1,χ)|² = π²/6 · Π_{q|p}(1-1/q²) · (1 + O(1/p))
# For p prime: = π²/6 · (1-1/p²) ≈ π²/6

# But splitting odd/even might matter

print(f"\n{'p':>4} {'Σ_odd |L|²':>14} {'(p-1)/2':>8} {'avg|L|²':>10} {'avg/π²*6':>10} {'Σ_odd |L|²/logp':>16}")
for p in primes:
    N = p - 1
    g = primitive_root(p)
    omega = np.exp(2j * np.pi / N)

    dlog = {}
    val = 1
    for k in range(N):
        dlog[val] = k
        val = (val * g) % p

    sum_L2_odd = 0.0
    n_odd = 0
    for j in range(N):
        if j % 2 == 0:
            continue
        chi = {}
        for a in range(1, p):
            chi[a] = omega ** (j * dlog[a])
        L1 = L_function(chi, p, terms=20000)
        sum_L2_odd += abs(L1)**2
        n_odd += 1

    logp = np.log(p)
    avg = sum_L2_odd / n_odd if n_odd > 0 else 0
    print(f"{p:4d} {sum_L2_odd:14.6f} {n_odd:8d} {avg:10.6f} {6*avg/np.pi**2:10.6f} {sum_L2_odd/logp:16.6f}")

# NOW the key: Σ K̂(χ) = Σ_{χ odd} |L(1,χ)|²/π²
# And: K̂_p(χ) = |L(1,χ)|²/π², so Σ K̂ = (1/π²) Σ |L(1,χ)|²
# By mean value: Σ_{χ odd} |L(1,χ)|² ~ (p/2) · (π²/6) · log p ... is there a log p?

# Actually for (p-1)/2 odd characters and average |L|² ≈ π²/6:
# Σ = (p-1)/2 · π²/6
# This gives K̂ sum ~ p/(12) -- no log p!
# But wait, the mean value theorem for L(1,χ) is:
# (1/φ(q)) Σ_{χ mod q} |L(1,χ)|² = Σ_{n≤q} φ(n)/n² + ... ≈ log q + const

# Let me check MORE carefully with the actual sum

print(f"\n{'p':>4} {'Σ_odd K̂':>12} {'(p-1)/12':>10} {'ratio':>8} {'Σ K̂/logp':>12} {'p·logp/12':>10}")
for p in primes:
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

    sum_K = 0.0
    for j in range(N):
        if j % 2 == 0:
            continue
        Kj = sum(ded[r] * (omega ** (j * dlog[r])).real for r in range(1, p))
        sum_K += Kj

    logp = np.log(p)
    print(f"{p:4d} {sum_K:12.4f} {(p-1)/12:10.4f} {sum_K/((p-1)/12):8.4f} {sum_K/logp:12.4f} {p*logp/12:10.4f}")

# Direct check: Σ_{j odd} K̂(χ_j) = Σ_{j odd} Σ_r s(r,p) χ_j(r)
# = Σ_r s(r,p) Σ_{j odd} χ_j(r)
# Σ_{j odd} χ_j(r) = Σ_{j odd} ω^{j·dlog(r)} = ...
# This picks out r with dlog(r) = (p-1)/2, i.e., r = g^{(p-1)/2} = -1 mod p
# No wait, it's more subtle.

# Σ_{j=0}^{N-1} ω^{jk} = N·δ_{k≡0}
# Σ_{j odd} ω^{jk} = Σ_{j=0}^{N-1} ω^{jk} · (1-(-1)^j)/2 ... hmm
# = (1/2)[Σ_j ω^{jk} - Σ_j (-ω)^{jk}]
# = (1/2)[N·δ_{k≡0} - Σ_j (-1)^j ω^{jk}]
# = (1/2)[N·δ_{k≡0} - Σ_j e^{iπj} ω^{jk}]
# = (1/2)[N·δ_{k≡0} - Σ_j (ωe^{iπ/N·N})^j ... this is messy

# The point: Σ K̂ = Σ_r s(r,p) · (sum of odd chars at r) relates to s evaluated
# at specific residues. Let me just use the numerical data.

print(f"\n{'='*80}")
print(f"  THE LOG P QUESTION: Where does it live?")
print(f"{'='*80}")

# With K̂(χ) = |L(1,χ)|²/π², the spectral formula becomes:
# (1/(π²(p-1))) Σ_{χ odd} |L(1,χ)|² · |Λ_p(χ)|²
#
# For the Farey discrepancy, we need ΔW² ~ log p / p
# The HYPERBOLIC sum Σ|λ|² contains the Mertens function values M(N/m)
# which carry the arithmetic information.
#
# Key: |Λ(χ)|² peaks at characters where λ_p correlates with χ
# The λ_p function encodes M(N/m) -- hyperbolic divisor structure
# The L-function kernel amplifies characters that "see" the primes
#
# CANDIDATE: The log p enters through Σ|λ|² ~ p·log p
# Let me check this more carefully

print(f"\n{'p':>4} {'Σ|λ|²':>8} {'p':>4} {'logp':>7} {'Σ|λ|²/p':>10} {'Σ|λ|²/(p logp)':>16}")
for p in primes:
    N = p - 1
    from dedekind_spectral2 import mertens_array
    M_arr = mertens_array(N)
    sum_lam2 = sum((M_arr[N // m] + (1 if m == 1 else 0))**2 for m in range(1, p))
    logp = np.log(p)
    print(f"{p:4d} {sum_lam2:8d} {p:4d} {logp:7.3f} {sum_lam2/p:10.4f} {sum_lam2/(p*logp):16.6f}")
