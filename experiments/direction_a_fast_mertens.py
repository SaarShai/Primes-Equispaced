#!/usr/bin/env python3
"""
DIRECTION A: Can the universal formula yield a faster Mertens algorithm?

Universal formula: S(m,N) = Σ_{f∈F_N} e^{2πimf} = M(N)+1+Σ_{d|m,d≥2} d·M(⌊N/d⌋)

Key insight: S(1,N) = M(N)+1 (trivially, since e^{2πi·1·f} = e^{2πif}).

But S(p,N) for prime p > N gives S(p,N) = M(N)+1 (no divisors of p in [2,N]).
So M(N) = S(p,N) - 1 for any prime p > N.

QUESTION: Can we compute S(m,N) without generating F_N?

IDEA 1: Mobius inversion.
Define T(m,N) = Σ_{a=0}^{N} Σ_{b=1}^{N} e^{2πim·a/b}  (sum over ALL a/b, not just coprime)
Then S(m,N) = Σ_{d=1}^{N} μ(d) · T(m, ⌊N/d⌋)  (Mobius inversion removes non-coprime)

Wait — T(m,N) = Σ_{b=1}^{N} Σ_{a=0}^{b} e^{2πima/b}
     = Σ_{b=1}^{N} (Σ_{a=0}^{b} e^{2πima/b})

The inner sum Σ_{a=0}^{b} e^{2πima/b} is a geometric series.
If b | m: sum = b+1
If b ∤ m: sum = (1 - e^{2πim(b+1)/b})/(1 - e^{2πim/b})
               = (1 - e^{2πim/b})/(1 - e^{2πim/b})  [since e^{2πim} = 1]
Wait, more carefully:
Σ_{a=0}^{b} e^{2πima/b} = (1 - e^{2πim(b+1)/b})/(1 - e^{2πim/b})
                         = (1 - e^{2πim} · e^{2πim/b})/(1 - e^{2πim/b})
                         = (1 - e^{2πim/b})/(1 - e^{2πim/b})  [since e^{2πim}=1]
                         = 1  ← this is WRONG, let me redo

Actually Σ_{a=0}^{b} e^{2πima/b} ≠ standard root of unity sum.
Standard: Σ_{a=0}^{b-1} e^{2πima/b} = b if b|m, else 0.
We sum to b (not b-1), so: Σ_{a=0}^{b} = Σ_{a=0}^{b-1} + e^{2πim} = (b if b|m, else 0) + 1.

So T_raw(m,N) = Σ_{b=1}^{N} [b·[b|m] + 1] = σ(m,N) + N
where σ(m,N) = Σ_{b|m, b≤N} b  (the restricted divisor sum).

BUT WAIT: We sum a from 0 to b, but F_N has a from 0 to b with gcd(a,b)=1.
The "all pairs" sum includes non-coprime pairs.

Actually let me reconsider. The Farey sum is:
S(m,N) = Σ_{b=1}^{N} Σ_{a=0, gcd(a,b)=1}^{b} e^{2πima/b}

The standard Ramanujan sum approach:
S(m,N) = Σ_{b=1}^{N} c_b^*(m) where c_b^*(m) = Σ_{a=0, gcd(a,b)=1}^{b} e^{2πima/b}

c_b^*(m) includes a=0 and a=b (both coprime to b iff b=1).
For b≥2: a=0 gives gcd(0,b)=b≠1, so excluded. a=b gives gcd(b,b)=b≠1, excluded.
For b=1: a=0 gives gcd(0,1)=1 ✓, a=1 gives gcd(1,1)=1 ✓.

So for b≥2: c_b^*(m) = c_b(m) (standard Ramanujan sum)
For b=1: c_1^*(m) = e^0 + e^{2πim} = 1 + 1 = 2

Thus S(m,N) = 2 + Σ_{b=2}^{N} c_b(m)

And c_b(m) = Σ_{d|gcd(b,m)} μ(b/d)·d

So we want Σ_{b=2}^{N} c_b(m).

Now, Σ_{b=1}^{N} c_b(m) is known: it equals M(N) + Σ_{d|m, d≥2} d·M(⌊N/d⌋).
(This is exactly the universal formula minus 1.)

So S(m,N) = 2 + Σ_{b=2}^{N} c_b(m) = 2 + (Σ_{b=1}^{N} c_b(m)) - c_1(m)
         = 2 + (M(N) + Σ_{d|m,d≥2} d·M(⌊N/d⌋)) - 1
         = M(N) + 1 + Σ_{d|m,d≥2} d·M(⌊N/d⌋)  ✓

OK so the formula is self-consistent. The question is: can we compute
Σ_{b=1}^{N} c_b(m) WITHOUT computing M first?

IDEA 2: Tomography approach.
We know S(m,N) = M(N) + 1 + Σ_{d|m,d≥2} d·M(⌊N/d⌋).

For m = prime p > N: S(p,N) = M(N) + 1.
For m = prime p ≤ N: S(p,N) = M(N) + 1 + p·M(⌊N/p⌋).
For m = p·q (distinct primes): S(pq,N) = M(N)+1 + p·M(⌊N/p⌋) + q·M(⌊N/q⌋) + pq·M(⌊N/pq⌋).

So from S at different m values, we get LINEAR equations in M at different arguments.
Can we solve this system faster than computing M directly?

Let's count: M(N), M(⌊N/2⌋), ..., M(1) — there are O(√N) distinct values of ⌊N/d⌋.
We need O(√N) equations. Can we find O(√N) values of m for which S(m,N) is easy to compute?

IDEA 3: Direct computation of partial Ramanujan sums.
Σ_{b=1}^{N} c_b(m) = Σ_{b=1}^{N} Σ_{d|gcd(b,m)} μ(b/d)·d
                    = Σ_{d|m} d · Σ_{k=1}^{⌊N/d⌋} μ(k)
                    = Σ_{d|m} d · M(⌊N/d⌋)

This IS the universal formula. So the formula is equivalent to Ramanujan sum 
partial sums, which is equivalent to knowing M at divisor-scaled arguments.

CONCLUSION for Idea 1-3: The universal formula doesn't give a NEW way to compute M,
it IS the Ramanujan sum identity. Computing S(m,N) is equivalent to computing M.

IDEA 4: HYBRID approach. 
The Meissel-Lehmer method computes M(N) in O(N^{2/3}) time.
But it works by computing Σ μ(n) using the identity M(N) = 1 - Σ_{n=2}^{N} M(⌊N/n⌋).

What if we use a DIFFERENT identity? The universal formula gives:
S(m,N) = Σ_{d|m} d · M(⌊N/d⌋)  (where the d=1 term is M(N))

This is a convolution: S = (id · [·|m]) * M at argument N.
By Mobius inversion on the divisor lattice:
M(N) = Σ_{d|m} μ(m/d) · (1/d) · S(d, N)  ← Mobius inversion on divisors of m

Wait, that's not quite right. Let me think again.

If F(d) = d·M(⌊N/d⌋) for divisors of m, and S(m,N) = Σ_{d|m} F(d),
then by Mobius inversion: F(m) = Σ_{d|m} μ(m/d) · S(d, N).
So m·M(⌊N/m⌋) = Σ_{d|m} μ(m/d) · S(d,N).

For m=1: M(N) = S(1,N) = M(N)+1... wait, S(1,N) should be |F_N| since e^{2πi·1·f} ≠ 1 in general.

Hmm wait, e^{2πi·1·f} = e^{2πif} which equals 1 only when f is integer. 
So S(1,N) = Σ e^{2πif} ≠ |F_N|. The universal formula says S(1,N) = M(N)+1.
And indeed: Σ e^{2πif} over Farey fractions does NOT equal |F_N|.

Let me just VERIFY computationally:
"""

import numpy as np
from math import gcd, floor
from collections import defaultdict
import time

def mobius_sieve(N):
    """Compute μ(n) for n=0..N using sieve."""
    mu = [0] * (N + 1)
    mu[1] = 1
    for i in range(1, N + 1):
        for j in range(2 * i, N + 1, i):
            mu[j] -= mu[i]
    return mu

def mertens_values(N, mu):
    """Compute M(n) for n=0..N."""
    M = [0] * (N + 1)
    for n in range(1, N + 1):
        M[n] = M[n - 1] + mu[n]
    return M

def farey_exp_sum(m, N):
    """Compute S(m,N) = Σ_{f∈F_N} e^{2πimf} directly."""
    s = 0j
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                s += np.exp(2j * np.pi * m * a / b)
    return s

def universal_formula(m, N, M_vals):
    """Compute S(m,N) via the universal formula."""
    result = M_vals[N] + 1
    for d in range(2, N + 1):
        if m % d == 0:
            result += d * M_vals[N // d]
    return result

# Verify the formula
print("=" * 70)
print("VERIFICATION: Universal formula vs direct computation")
print("=" * 70)

N_max = 30
mu = mobius_sieve(N_max)
M = mertens_values(N_max, mu)

for N in [5, 10, 15, 20]:
    for m in [1, 2, 3, 5, 7, 6, 10, 12]:
        direct = farey_exp_sum(m, N)
        formula = universal_formula(m, N, M)
        match = abs(direct.real - formula) < 1e-8 and abs(direct.imag) < 1e-8
        if not match:
            print(f"  MISMATCH: m={m}, N={N}: direct={direct:.6f}, formula={formula}")

print("All verified ✓")

# ============================================================
# IDEA 5: Fast computation via the TOMOGRAPHY system
# ============================================================
print("\n" + "=" * 70)
print("IDEA 5: Tomography — recovering M(⌊N/d⌋) from Farey sums")
print("=" * 70)

# For a given N, the values ⌊N/d⌋ for d=1..N take only O(√N) distinct values.
# Let V = {⌊N/d⌋ : d=1..N} — these are the "compressed" M arguments.
# The universal formula at frequency m reads:
#   S(m,N) = Σ_{d|m, d≤N} d · M(⌊N/d⌋)
# This is a weighted sum of M at DIVISOR-scaled arguments.

# KEY QUESTION: Is there a set of frequencies {m_1,...,m_k} such that
# the resulting linear system uniquely determines all M(v) for v ∈ V,
# AND the Farey sums S(m_i,N) are efficiently computable?

def distinct_floor_values(N):
    """Return sorted list of distinct ⌊N/d⌋ values for d=1..N."""
    vals = set()
    for d in range(1, N + 1):
        vals.add(N // d)
    return sorted(vals)

N = 100
V = distinct_floor_values(N)
print(f"N={N}: {len(V)} distinct ⌊N/d⌋ values (≈ 2√N = {2*int(N**0.5)})")
print(f"Values: {V[:20]}...")

# For each frequency m, the equation S(m,N) = Σ_{d|m} d·M(⌊N/d⌋)
# involves only M values at ⌊N/d⌋ where d|m AND d≤N.
# So divisors of m select WHICH M values appear.

# PROBLEM: Most frequencies m have few divisors of m that are ≤ N,
# so each equation involves few unknowns. We need many equations.

# But highly composite numbers have MANY divisors!
# m = 2^a · 3^b · 5^c ... can have arbitrarily many divisors.

# Let's see what happens with m = N! (or similar highly composite m):
# Then EVERY d ≤ N divides m, and the equation becomes:
# S(N!, N) = Σ_{d=1}^{N} d · M(⌊N/d⌋) = Σ_{v∈V} c(v) · M(v)
# where c(v) = Σ_{d: ⌊N/d⌋=v} d.

# This is just ONE equation with |V| unknowns. Not helpful.

# We need |V| INDEPENDENT equations. Each uses a different m.
# For m = p (prime ≤ N): S(p,N) = M(N) + p·M(⌊N/p⌋) + 1
# This gives a 2-term equation linking M(N) and M(⌊N/p⌋).

# INSIGHT: We can BUILD a triangular system!
# Step 1: Choose p > N (prime). Then S(p,N) = M(N)+1, so M(N) = S(p,N)-1.
# Step 2: For prime p ≤ N: M(⌊N/p⌋) = (S(p,N) - M(N) - 1) / p.
# Step 3: For m = p·q: get M(⌊N/pq⌋).
# etc.

# BUT: computing S(p,N) requires generating F_N → O(N²) time.
# Unless we can compute S(p,N) faster...

# CRITICAL REALIZATION:
# S(m,N) = Σ_{b=1}^{N} c_b(m) + 1  (Ramanujan sum + the b=1 adjustment)
# c_b(m) = Σ_{d|gcd(b,m)} μ(b/d)·d
# 
# For FIXED m, computing Σ_{b=1}^{N} c_b(m) is:
# = Σ_{d|m} d · M(⌊N/d⌋)
# which brings us back to needing M values!

# So there's a CIRCULARITY: computing S(m,N) via Ramanujan sums requires M,
# and computing M via the formula requires S.

print("\n" + "=" * 70)
print("IDEA 6: SUBLINEAR Mertens via divided Farey sums")
print("=" * 70)

# Standard Meissel-Lehmer for M(N): O(N^{2/3}) time, O(N^{1/3}) space.
# Uses: M(N) = 1 - Σ_{n=2}^{N} M(⌊N/n⌋)
# This is the SAME as: Σ_{n=1}^{N} M(⌊N/n⌋) = 1 (the Mobius sum identity).

# The universal formula for m with divisors d_1,...,d_k in [1,N]:
# S(m,N) = Σ_{i} d_i · M(⌊N/d_i⌋) + 1

# The Meissel-Lehmer identity is the SPECIAL CASE where m has ALL integers 
# 1..N as divisors (i.e., m = lcm(1,...,N) or similar):
# Σ_{d=1}^{N} M(⌊N/d⌋) = 1

# So the Meissel-Lehmer approach IS the universal formula at m = lcm(1,...,N),
# weighted differently! Specifically:
# Meissel: Σ_{d=1}^{N} 1 · M(⌊N/d⌋) = 1 (all coefficients = 1)
# Universal: Σ_{d|m, d≤N} d · M(⌊N/d⌋) = S(m,N)-1 (coefficients = d)

# NEW IDEA: Can we use MULTIPLE universal formula instances 
# (at different m) to get a BETTER recursion than Meissel-Lehmer?

# The Meissel-Lehmer recursion: M(N) = 1 - Σ_{n=2}^{N} M(⌊N/n⌋)
# Complexity comes from evaluating M at O(√N) distinct values.

# If we had an identity involving FEWER M values, it would be faster.
# The universal formula at prime p > √N:
# S(p,N) = M(N) + 1 + p·M(⌊N/p⌋)  [only 2 terms!]
# But we need to know S(p,N)...

# HOWEVER: What if we can relate S(p,N) for DIFFERENT p?
# If S(p1,N) ≈ S(p2,N) for primes p1,p2 > N, then both equal M(N)+1.
# No new info.

# For primes √N < p ≤ N:
# S(p,N) = M(N) + 1 + p·M(⌊N/p⌋)
# M(⌊N/p⌋) is known by recursion on smaller arguments.
# So S(p,N) is determined by the M values we already know.

# CONCLUSION: The universal formula does NOT give a fundamentally new 
# algorithm because it's EQUIVALENT to the Ramanujan sum partial sums,
# which reduce to the Meissel-Lehmer identity.

print("Standard Meissel-Lehmer: M(N) = 1 - Σ_{n=2}^{N} M(⌊N/n⌋)")
print("Universal formula: S(m,N) = Σ_{d|m} d·M(⌊N/d⌋) + 1")
print("These are different VIEWS of the same structure (Ramanujan sums).")
print("The universal formula doesn't yield a faster algorithm per se.")

# ============================================================
# IDEA 7: Fast Ramanujan-sum partial sum computation
# ============================================================
print("\n" + "=" * 70)
print("IDEA 7: Batch Ramanujan sum computation")
print("=" * 70)

# NOVEL ANGLE: Can we compute S(m,N) for MANY m simultaneously in sublinear time?
# This would be useful for spectral analysis of the Farey sequence.

# S(m,N) = M(N) + 1 + Σ_{d|m, d≥2} d·M(⌊N/d⌋)
# If we precompute M(v) for all v ∈ {⌊N/d⌋ : d=1..N}, that's O(√N) values.
# Then S(m,N) for ANY m can be computed in O(τ(m)) time (# divisors of m).

# So: O(N^{2/3}) preprocessing → then O(τ(m)) per query.
# For a batch of Q queries: O(N^{2/3} + Q·max_τ(m)).

# Compare to NAIVE: O(N² · Q) (generate F_N for each query).
# Or: O(N²) to generate F_N, then O(N²) per query (evaluate sum).

# So the universal formula gives a massive speedup for BATCH Farey sum queries!
# Preprocessing O(N^{2/3}), then O(d(m)) per query vs O(N²) per query.

# SPEEDUP FACTOR: N² / d(m) ≈ N² / log(m) for typical m.

# Let's demonstrate:

print("\nBatch Farey exponential sum computation:")
print("Method 1 (direct): O(N²) per query")
print("Method 2 (universal formula + precomputed M): O(N^{2/3}) + O(d(m)) per query")
print()

# Time comparison
N_test = 200
mu_test = mobius_sieve(N_test)
M_test = mertens_values(N_test, mu_test)

# Method 1: Direct computation for 50 queries
queries = list(range(1, 51))
t0 = time.time()
direct_results = {}
for m in queries:
    direct_results[m] = farey_exp_sum(m, N_test)
t_direct = time.time() - t0

# Method 2: Universal formula (M already precomputed, O(N) sieve here)
t0 = time.time()
formula_results = {}
for m in queries:
    formula_results[m] = universal_formula(m, N_test, M_test)
t_formula = time.time() - t0

print(f"N={N_test}, {len(queries)} queries:")
print(f"  Direct: {t_direct:.3f}s")
print(f"  Formula: {t_formula:.6f}s")
print(f"  Speedup: {t_direct/t_formula:.0f}x")

# Verify agreement
max_err = max(abs(direct_results[m].real - formula_results[m]) for m in queries)
print(f"  Max error: {max_err:.2e}")

# ============================================================
# IDEA 8: NEW — Farey sum DFT and spectral analysis
# ============================================================
print("\n" + "=" * 70)
print("IDEA 8: Spectral structure of Farey exponential sums")
print("=" * 70)

# The function m ↦ S(m,N) is the "Farey DFT" at frequency m.
# The universal formula gives: S(m,N) = Σ_{d|m} d·M(⌊N/d⌋) + δ_{corrections}
# This is a MULTIPLICATIVE function of m (up to the constant M(N)+1)!

# More precisely, let F(m) = S(m,N) - M(N) - 1 = Σ_{d|m, d≥2} d·M(⌊N/d⌋).
# Define g(d) = d·M(⌊N/d⌋). Then F = 1*g (Dirichlet convolution with constant 1).
# Wait no, F(m) = Σ_{d|m, d≥2} g(d) = (g * 1)(m) - g(1) 
# Actually F(m) = Σ_{d|m} g(d) - g(1) where g(1) = 1·M(N) = M(N).
# And Σ_{d|m} g(d) = S(m,N) - 1 = F(m) + M(N).

# So the Dirichlet series of S(m,N)-1 is:
# Σ_{m=1}^∞ (S(m,N)-1)/m^s = Σ_{m=1}^∞ (Σ_{d|m} g(d))/m^s
#                             = (Σ g(d)/d^s) · ζ(s)
#                             = ζ(s) · Σ_{d=1}^{N} M(⌊N/d⌋)/d^{s-1}

# NOVEL OBSERVATION: The Dirichlet series of the Farey exponential sums
# factorizes as ζ(s) times a "Mertens transform":
# G(s) = Σ_{d=1}^{N} M(⌊N/d⌋) / d^{s-1}

# What is G(s)? Using M(⌊N/d⌋) = Σ_{k≤N/d} μ(k):
# G(s) = Σ_{d=1}^{N} Σ_{k=1}^{⌊N/d⌋} μ(k) / d^{s-1}
#       = Σ_{n=1}^{N} μ(n) · Σ_{d: ⌊N/d⌋≥n} 1/d^{s-1}

# Hmm this is getting complicated. Let me just compute and visualize.

N = 50
mu = mobius_sieve(N)
M = mertens_values(N, mu)

print(f"\nSpectral data S(m,{N}) for m=1..100:")
S_values = []
for m in range(1, 101):
    S_values.append(universal_formula(m, N, M))
    
# Check: is this multiplicative?
print("Multiplicativity test (S(m,N)-M(N)-1 should be multiplicative):")
F_vals = [s - M[N] - 1 for s in S_values]  # F(m) = S(m,N) - M(N) - 1
for a in [2, 3, 5, 7]:
    for b in [3, 5, 7, 11]:
        if a != b and a*b <= 100:
            lhs = F_vals[a*b - 1]  # F(ab)
            rhs_sum = F_vals[a-1] + F_vals[b-1] + F_vals[a-1]*F_vals[b-1]/(M[N])
            # Actually for Dirichlet convolution, F(ab) ≠ F(a)·F(b) in general.
            # Let's check: is g multiplicative?
            pass

# Actually let me check something more concrete:
# g(d) = d·M(⌊N/d⌋), and F(m) = Σ_{d|m, d≥2} g(d).
# F is NOT multiplicative since it's a sum of g over divisors (convolution with 1).
# But f(m) = Σ_{d|m} g(d) IS a Dirichlet convolution, so if g is multiplicative, f is too.

# Is g multiplicative? g(d) = d·M(⌊N/d⌋). 
# g(6) = 6·M(⌊50/6⌋) = 6·M(8) = 6·(-2) = -12
# g(2)·g(3) = 2·M(25) · 3·M(16) = 2·(-1) · 3·(-1) = 6. 
# -12 ≠ 6. So g is NOT multiplicative.
print(f"g(6) = 6·M(⌊50/6⌋) = 6·M(8) = 6·{M[8]} = {6*M[8]}")
print(f"g(2)·g(3) = 2·M(25)·3·M(16) = 2·{M[25]}·3·{M[16]} = {2*M[25]*3*M[16]}")
print(f"g is NOT multiplicative → S(m,N) is not multiplicative in m.")

# But the VALUES S(m,N) have interesting structure.
print(f"\nS(m,50) values for m=1..30:")
for m in range(1, 31):
    print(f"  S({m:2d},50) = {S_values[m-1]:6d}  (M(50)={M[50]}, divisor correction = {S_values[m-1]-M[50]-1})")

# ============================================================
# IDEA 9: NEW ALGORITHM — Segmented Ramanujan sum sieve
# ============================================================
print("\n" + "=" * 70)
print("IDEA 9: Segmented Ramanujan sum sieve for S(m,N) over many N")
print("=" * 70)

# Here's a genuinely novel algorithmic application:
# 
# PROBLEM: Compute S(m, N) for FIXED m and ALL N in [1, X].
# NAIVE: O(X²) (generate each F_N).
# 
# BETTER: Use S(m,N) = S(m,N-1) + c_N(m) (add one Ramanujan sum at a time).
# c_N(m) = Σ_{d|gcd(N,m)} μ(N/d)·d
# Computing c_N(m) takes O(d(gcd(N,m))) ≈ O(d(m)) time.
# Total: O(X · d(m)) for all N up to X.
# For fixed m this is O(X) — LINEAR!
#
# Compare to standard: computing M(N) for all N ≤ X also takes O(X) via sieve.
# And S(m,N) = M(N) + 1 + divisor corrections, so same complexity.
# Not a win.
#
# BUT: What if we want S(m,N) for ALL m in [1,M] and ALL N in [1,X]?
# The full "Farey spectrogram" S(m,N)?
# Via Ramanujan: O(X·M·max_d(m)) ≈ O(X·M·log(M))
# Via universal formula + precomputed M: O(X + M·X^{1/2}·log(M))
# The formula approach precomputes M at all O(√X) points, then for each m
# evaluates the divisor sum.

print("For the 'Farey spectrogram' S(m,N) for m=1..M, N=1..X:")
print("  Naive: O(X³)  (generate F_N for each m)")  
print("  Ramanujan: O(X·M·log(M))")
print("  Universal formula: O(X) + O(M·√X·log(M))")
print("  Winner: Universal formula when M >> √X")

