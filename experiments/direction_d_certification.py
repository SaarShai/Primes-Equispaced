#!/usr/bin/env python3
"""
DIRECTION D: Interval arithmetic certification of p=92173 counterexample

The claim: At p=92173 with M(p)=-2, ΔW(p) > 0 (positive despite M<0).
This is the ONLY counterexample among 9,588 primes up to 100K.
ΔW = +3.56×10⁻¹¹.

We want to CERTIFY this with exact or interval arithmetic.

APPROACH 1: Use the exact decomposition with Python's Fraction class.
The Farey generator runs in O(N) time/space and gives exact fractions.
We need to compute ΔW(92173) = W(92172) - W(92173).

PROBLEM: |F_{92172}| ≈ 3·92172²/π² ≈ 2.58 billion. Way too large for exact.

APPROACH 2: Use the closed-form decomposition.
ΔW(p) involves specific sums over F_{p-1} that we computed exactly.
The key quantities:
  S2 = Σ f², ΔS2 = (p-1)(2p-1)/(6p)
  R = Σ j·f (rank-weighted sum)  
  J(n) = (n-1)(2n-1)/(6n)

ΔW = ΔS2 - (2/n')·R_{new} + J(n) - J(n')

But R_new requires iterating over ALL Farey fractions.

APPROACH 3: Use the WOBBLE DECOMPOSITION identity.
ΔW(p) can be expressed in terms of sums that the Farey generator can compute.
The generator is O(n) where n = |F_{p-1}| ≈ 2.58 billion for p=92173.
This takes a very long time but IS doable.

APPROACH 4: Use the CROSS-TERM formula.
We showed ΔW(p) depends on Σ D·δ (the cross term).
If we can evaluate this cross term with interval arithmetic, we're done.

APPROACH 5: Smaller counterexample search.
Before certifying p=92173, check if there's a SMALLER counterexample 
with M(p)=-2 (or -1) and ΔW(p) > 0.

Actually, let me first check: for which primes is M(p) = -2?
And compute ΔW using the C program that already exists.
"""

from math import gcd
import mpmath
from mpmath import mpf, mp
import time

# Set high precision
mp.dps = 50  # 50 decimal places

def mobius_sieve(N):
    mu = [0] * (N + 1)
    mu[1] = 1
    for i in range(1, N + 1):
        for j in range(2 * i, N + 1, i):
            mu[j] -= mu[i]
    return mu

def sieve_primes(N):
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(N**0.5) + 1):
        if is_prime[p]:
            for j in range(p*p, N + 1, p):
                is_prime[j] = False
    return is_prime

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

# ============================================================
# FIND COUNTEREXAMPLE CANDIDATES
# ============================================================
print("=" * 70)
print("Finding primes with M(p) = -2 (counterexample candidates)")
print("=" * 70)

N_MAX = 10000  # Start small to understand the pattern
mu = mobius_sieve(N_MAX)
is_prime = sieve_primes(N_MAX)

M_val = 0
candidates = []
for n in range(1, N_MAX + 1):
    M_val += mu[n]
    if is_prime[n] and M_val == -2 and n >= 11:
        candidates.append(n)

print(f"Primes p ≤ {N_MAX} with M(p) = -2: {len(candidates)} total")
print(f"First 30: {candidates[:30]}")

# ============================================================
# EXACT ΔW COMPUTATION FOR SMALL CANDIDATES
# ============================================================
print("\n" + "=" * 70)
print("Exact ΔW computation for small candidates with M(p) = -2")
print("=" * 70)

from fractions import Fraction

def farey_generator(N):
    """Generate Farey sequence F_N in order."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def compute_wobble_generator(N):
    """Compute W(N) using Farey generator (exact rational arithmetic)."""
    n = 0
    fracs = []
    for (a, b) in farey_generator(N):
        fracs.append(Fraction(a, b))
        n += 1
    
    W = Fraction(0)
    for j in range(n):
        diff = fracs[j] - Fraction(j, n)
        W += diff * diff
    return W, n

# Test with small M(p)=-2 primes
test_primes = [p for p in candidates if p <= 200]
print(f"Testing primes with M(p)=-2 up to 200: {test_primes}")

for p in test_primes[:10]:
    t0 = time.time()
    W_prev, n_prev = compute_wobble_generator(p - 1)
    W_curr, n_curr = compute_wobble_generator(p)
    dW = W_prev - W_curr
    elapsed = time.time() - t0
    
    sign_str = "POSITIVE (counterexample!)" if dW > 0 else "negative"
    print(f"  p={p:5d}: ΔW = {float(dW):.6e}  [{sign_str}]  ({elapsed:.2f}s)")

# ============================================================  
# APPROACH FOR p=92173: Use the factored formula
# ============================================================
print("\n" + "=" * 70)
print("FACTORED FORMULA for ΔW certification")
print("=" * 70)

# For prime p, going from F_{p-1} to F_p:
# New fractions: k/p for k=1,...,p-1 (exactly p-1 new fractions)
# 
# Using the exact decomposition:
# W(N) = (1/n)·Σ(j - n·f_j)² / n²... wait, let me use the standard form:
# W(N) = Σ_{j=0}^{n-1} (f_j - j/n)² where n = |F_N|.
#
# Actually computing W directly via generator requires O(n) memory to store all fracs.
# For p=92173, n ≈ 2.58 billion. That's ~20GB of Fraction objects. Not feasible.
#
# ALTERNATIVE: compute ΔW without computing W itself.
# The key identity: 
# ΔW(p) = W(p-1) - W(p)
# 
# We can decompose this into parts that don't require storing all fractions.
# 
# BUT: W(p) involves (f_j - j/n')² where the f_j and ranks are in F_p,
# and W(p-1) involves (f_j - j/n) where the f_j and ranks are in F_{p-1}.
# These are DIFFERENT lists with different denominators.
#
# The DIRECT approach: compute both W(p-1) and W(p) incrementally.
# For F_{p-1}, use the generator. For F_p, insert the new fractions.
#
# A STREAMING approach for W:
# S2 = Σ f_j² and R = Σ j·f_j, then W = S2 - 2R/n + J(n)
# where J(n) = Σ (j/n)² = (n-1)(2n-1)/(6n).
#
# S2 can be accumulated: just sum f² as generator runs. No storage needed.
# R requires knowing ranks, which the generator gives in order.
# So we can compute S2 and R in a SINGLE PASS through the generator.

# Let me test this streaming approach:
def compute_S2_R_streaming(N):
    """Compute S2 and R for F_N in a streaming fashion."""
    S2 = Fraction(0)
    R = Fraction(0)
    n = 0
    for (a, b) in farey_generator(N):
        f = Fraction(a, b)
        S2 += f * f
        R += n * f  # rank is n (0-indexed: 0, 1, 2, ...)
        n += 1
    return S2, R, n

# Verify on small cases
for N in [5, 10, 20]:
    S2, R, n = compute_S2_R_streaming(N)
    J = Fraction((n-1)*(2*n-1), 6*n)
    W_streaming = S2 - 2*R/n + J
    
    # Compare to direct
    W_direct, n_direct = compute_wobble_generator(N)
    
    assert n == n_direct
    assert W_streaming == W_direct, f"Mismatch at N={N}: {W_streaming} vs {W_direct}"

print("Streaming S2, R computation verified ✓")

# Now: for the CERTIFICATION, we need to compute ΔW(p) = W(p-1) - W(p).
# Both W(p-1) and W(p) can be computed via the streaming approach.
# W(p-1) needs one pass through F_{p-1}.
# W(p) needs one pass through F_p = F_{p-1} ∪ {k/p : k=1,...,p-1}.
#
# F_p can be generated by the same generator. Two passes total.
# For p=92173: each pass scans ~2.58 billion fractions.
# With Python's Fraction, that's ~1 μs per fraction → ~2.58 million seconds.
# WAY too slow.
#
# WITH mpmath mpf at 50 digits: maybe 10x faster but still too slow.
#
# WITH C code and GMP: ~100ns per fraction → ~258 seconds per pass. FEASIBLE.

# ============================================================
# MEDIUM-SCALE EXACT CERTIFICATION
# ============================================================
print("\n" + "=" * 70)
print("MEDIUM-SCALE CERTIFICATION: primes up to p=2000 with M(p)=-2")
print("=" * 70)

# Find all primes up to 2000 with M(p) = -2
mu2000 = mobius_sieve(2000)
M_val = 0
candidates_2000 = []
for n in range(1, 2001):
    M_val += mu2000[n]
    if is_prime[n] and M_val == -2 and n >= 11:
        candidates_2000.append(n)
    
print(f"Primes with M(p)=-2, p ≤ 2000: {candidates_2000}")

# Compute ΔW for each using streaming approach with Fraction
for p in candidates_2000:
    t0 = time.time()
    S2_prev, R_prev, n_prev = compute_S2_R_streaming(p - 1)
    J_prev = Fraction((n_prev - 1) * (2 * n_prev - 1), 6 * n_prev)
    W_prev = S2_prev - 2 * R_prev / n_prev + J_prev
    
    S2_curr, R_curr, n_curr = compute_S2_R_streaming(p)
    J_curr = Fraction((n_curr - 1) * (2 * n_curr - 1), 6 * n_curr)
    W_curr = S2_curr - 2 * R_curr / n_curr + J_curr
    
    dW = W_prev - W_curr
    elapsed = time.time() - t0
    
    sign = "+" if dW > 0 else "-"
    print(f"  p={p:5d}: ΔW = {sign}{abs(float(dW)):.6e}  "
          f"(n_prev={n_prev}, n_curr={n_curr}, {elapsed:.1f}s)")
    
    if dW > 0:
        print(f"    *** COUNTEREXAMPLE FOUND: p={p}, M(p)=-2, ΔW > 0 ***")
        print(f"    Exact ΔW = {dW}")

# ============================================================
# C CODE FOR LARGE-SCALE CERTIFICATION
# ============================================================
print("\n" + "=" * 70)
print("Generating C code for p=92173 certification")
print("=" * 70)

# The C code would use the Farey generator with 128-bit integers or GMP
# for exact rational arithmetic. Let me write it.
# For now, let me compute what |F_{92172}| is:

phi = euler_totient_sieve(100000)
farey_size_92172 = 1 + sum(phi[k] for k in range(1, 92173))
print(f"|F_{{92172}}| = {farey_size_92172}")
print(f"|F_{{92173}}| = {farey_size_92172 + 92172}")
print(f"Ratio |F|/p² = {farey_size_92172 / 92172**2:.6f} (should be ~3/π² = {3/3.14159265**2:.6f})")

# ============================================================
# ALTERNATIVE: ΔW via the EXACT cross-term formula
# ============================================================
print("\n" + "=" * 70)
print("ΔW via cross-term formula (avoids computing W directly)")
print("=" * 70)

# The exact formula for ΔW(p) at prime p:
# Let n = |F_{p-1}|, m = p-1 = φ(p), n' = n + m.
# 
# ΔW(p) = W(p-1) - W(p) can be decomposed as:
# (using W = S2 - 2R/n + J(n) and R = Σ j·f_j)
#
# The exact decomposition is complex but the key is:
# all the terms except the CROSS TERM Σ D·δ can be computed in closed form
# from n, m, and a few simple sums over the Farey sequence.
#
# The cross term Σ D·δ is the hard part and requires streaming through F_{p-1}.
#
# For the certification: we need to compute Σ D·δ with enough precision
# to determine its sign and magnitude, then plug into the closed-form rest.

# Let me first verify this decomposition for small primes:
print("\nVerifying cross-term ΔW decomposition:")
for p in [11, 13, 17, 19, 23]:
    # Exact ΔW
    S2_prev, R_prev, n_prev = compute_S2_R_streaming(p - 1)
    J_prev = Fraction((n_prev - 1) * (2 * n_prev - 1), 6 * n_prev)
    W_prev = S2_prev - 2 * R_prev / n_prev + J_prev
    
    S2_curr, R_curr, n_curr = compute_S2_R_streaming(p)
    J_curr = Fraction((n_curr - 1) * (2 * n_curr - 1), 6 * n_curr)
    W_curr = S2_curr - 2 * R_curr / n_curr + J_curr
    
    dW_exact = W_prev - W_curr
    
    # Cross term Σ D(f)·δ(f)
    cross = Fraction(0)
    rank = 0
    for (a, b) in farey_generator(p - 1):
        f = Fraction(a, b)
        D = rank - n_prev * f
        pa_mod_b = (p * a) % b
        delta = f - Fraction(pa_mod_b, b)
        cross += D * delta
        rank += 1
    
    m = p - 1  # number of new fractions
    n = n_prev
    n_prime = n + m
    
    # The ΔW decomposition:
    # ΔW = (closed form terms) + (function of cross term)
    # Let me just report the values
    print(f"  p={p}: ΔW_exact={float(dW_exact):.6e}, cross={float(cross):.6e}, "
          f"n={n}, m={m}")

