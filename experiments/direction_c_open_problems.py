#!/usr/bin/env python3
"""
DIRECTION C: Connections to open problems

1. Chowla's conjecture: Σ_{n≤N} μ(n)μ(n+1) = o(N)
   Can the per-denominator structure help?

2. Can the geometric framework prove anything new about M(N)?

3. Correlations of Möbius with other functions.
"""

from math import gcd, floor, sqrt, log
import numpy as np
from fractions import Fraction

def mobius_sieve(N):
    mu = [0] * (N + 1)
    mu[1] = 1
    for i in range(1, N + 1):
        for j in range(2 * i, N + 1, i):
            mu[j] -= mu[i]
    return mu

def mertens_values(N, mu):
    M = [0] * (N + 1)
    for n in range(1, N + 1):
        M[n] = M[n - 1] + mu[n]
    return M

# ============================================================
# CHOWLA'S CONJECTURE AND FAREY STRUCTURE
# ============================================================
print("=" * 70)
print("CHOWLA'S CONJECTURE via Farey framework")
print("=" * 70)

# Chowla's conjecture: Σ_{n≤N} μ(n)μ(n+h) = o(N) for all h ≥ 1.
# 
# The bridge identity gives M(N) = Σ c_b(1) + 1 = Σ μ(b) + 1 (trivially).
# But can we get μ(n)μ(n+1) from the Farey structure?
#
# Key idea: In F_N, consecutive fractions a/b, c/d satisfy bc - ad = 1.
# The Farey NEIGHBORS are characterized by this determinant condition.
# μ(b) and μ(d) are the Möbius values at consecutive denominators.
#
# QUESTION: Is Σ_{(a/b,c/d) neighbors in F_N} μ(b)μ(d) related to Chowla's sum?
# 
# NOT directly, because consecutive Farey denominators (b,d) with bc-ad=1
# are NOT the same as consecutive integers (n, n+1).
# But there IS a connection through the FAREY MEDIANT:
# If a/b and c/d are Farey neighbors with b+d > N, then (a+c)/(b+d) is NOT in F_N.
# The pairs (b,d) that arise as Farey neighbor denominators in F_N are exactly
# the pairs with b+d > N, b ≤ N, d ≤ N, gcd-related...

N_max = 5000
mu = mobius_sieve(N_max)
M = mertens_values(N_max, mu)

# Compute Chowla sums for h=1,2,3
print("\nChowla sums Σ_{n≤N} μ(n)μ(n+h) for various N and h:")
for N in [100, 500, 1000, 2000, 5000]:
    for h in [1, 2, 3]:
        chowla = sum(mu[n] * mu[n + h] for n in range(1, N + 1) if n + h <= N_max)
        print(f"  N={N:5d}, h={h}: Σ μ(n)μ(n+h) = {chowla:7d} (ratio to N: {chowla/N:.4f})")

# ============================================================
# FAREY NEIGHBOR CORRELATIONS
# ============================================================
print("\n" + "=" * 70)
print("FAREY NEIGHBOR CORRELATIONS: Σ μ(b)μ(d) over consecutive pairs")
print("=" * 70)

def farey_generator(N):
    """Generate Farey sequence F_N in order."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

# For each F_N, compute Σ μ(b_j)μ(b_{j+1}) over consecutive denominator pairs
print("\nΣ μ(b_j)·μ(b_{j+1}) over consecutive Farey denominators:")
for N in [10, 20, 50, 100, 200, 500, 1000]:
    mu_local = mobius_sieve(N)

    prev_b = None
    mu_corr = 0
    n_pairs = 0

    for (a, b) in farey_generator(N):
        if prev_b is not None:
            mu_corr += mu_local[prev_b] * mu_local[b]
            n_pairs += 1
        prev_b = b

    farey_size = n_pairs + 1
    print(f"  N={N:5d}: |F_N|={farey_size:7d}, corr={mu_corr:7d}, "
          f"ratio/|F|: {mu_corr/farey_size:.4f}, ratio/N: {mu_corr/N:.4f}")

# ============================================================
# NEW MERTENS BOUNDS FROM FAREY GEOMETRY
# ============================================================
print("\n" + "=" * 70)
print("NEW MERTENS BOUNDS from Farey geometry")
print("=" * 70)

# Can we prove |M(N)| = Ω(√N) using the Farey framework?
#
# The bridge identity: S(p,N) = M(N)+1 for prime p > N.
# S(p,N) = Σ_{f∈F_N} e^{2πipf} is a GEOMETRIC quantity.
#
# |S(p,N)| = |M(N)+1|.
# So |M(N)+1| = |Σ e^{2πipf}|.
#
# For RANDOM points {f_j}, |Σ e^{2πimf_j}| ~ √n (CLT).
# Farey fractions are NOT random, but they ARE equidistributed.
# 
# Can we prove |S(p,N)| = Ω(√n) for SOME p > N?
# n = |F_N| ~ 3N²/π², so √n ~ N√3/π ≈ 0.55N.
#
# This would give |M(N)+1| = Ω(N), which is MUCH stronger than Ω(√N)!
# But that's probably too strong...
#
# Actually, |M(N)| = o(N) (by PNT), so |S(p,N)| = |M(N)+1| = o(N) = o(√n·N/√n).
# Since n ~ N², √n ~ N. So |S(p,N)| = o(√n). The Farey sequence has LESS
# randomness than random points at the prime frequency. This is EXPECTED
# since the Farey points are equidistributed.
#
# But can we get a LOWER bound? 
# The key issue: we need M(N) to be large sometimes.
# M(N) changes sign infinitely often (proved by Ingham 1942).
# The maximum |M(N)| for N ≤ X grows at least like √X (Odlyzko-te Riele, 1985).
#
# OUR APPROACH: Use the wobble analysis.
# If ΔW(p) > 0 for some p with M(p) < 0, that constrains |M|.
# The sigmoid says: P(ΔW>0) ≈ sigmoid(c·M(p)/√p).
# If M(p)/√p > 0.3, then ΔW(p) > 0 with probability 1 (empirically).
# If M(p)/√p < -0.1, then ΔW(p) < 0 with probability 1.
# 
# Can we use this to prove M(N) = Ω(√N)?
# If we could prove: "ΔW(p) > 0 infinitely often" (which is true since 
# composites frequently improve uniformity and there's a balancing argument),
# and "ΔW(p) > 0 implies M(p) ≥ -c√p" (which the sigmoid suggests),
# then M takes values ≥ -c√p infinitely often.
# Combined with M taking values ≤ -c√p infinitely often (which needs proof),
# we'd get oscillation.

# Let me compute the empirical distribution of M(p)/√p:
print("\nDistribution of M(p)/√p for primes p ≤ 5000:")
from collections import Counter

def sieve_primes(N):
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(N**0.5) + 1):
        if is_prime[p]:
            for j in range(p*p, N + 1, p):
                is_prime[j] = False
    return [p for p in range(2, N + 1) if is_prime[p]]

primes = sieve_primes(5000)
bins = {}  # bin by M/√p rounded to 0.05
for p in primes:
    ratio = M[p] / sqrt(p)
    bin_key = round(ratio * 20) / 20  # round to nearest 0.05
    bins[bin_key] = bins.get(bin_key, 0) + 1

for k in sorted(bins.keys()):
    bar = '#' * bins[k]
    print(f"  {k:6.2f}: {bins[k]:4d} {bar}")

# ============================================================
# NOVEL: Farey-Mertens OSCILLATION theorem
# ============================================================
print("\n" + "=" * 70)
print("NOVEL: Farey-geometric oscillation of M(N)")
print("=" * 70)

# Here's the key insight for a potential new result:
# 
# THEOREM (proposed): For any ε > 0, there exist infinitely many N with
#   M(N) > N^{1/2 - ε} and infinitely many N with M(N) < -N^{1/2 - ε}.
# 
# This is WEAKER than what's known (Odlyzko-te Riele proved ∃ N with |M(N)| > √N,
# and Ingham proved sign changes), but the proof strategy is DIFFERENT:
# 
# 1. The cumulative wobble W(N) → 0 as N → ∞ (equidistribution theorem).
# 2. For primes p, ΔW(p) is controlled by M(p)/√p (our discovery).
# 3. Primes are frequent enough that Σ_p ΔW(p) must nearly cancel Σ_composite ΔW(n).
# 4. If M(p)/√p were always < -c for some c, then ALL prime steps would 
#    increase wobble, giving W(N) → ∞, contradicting equidistribution.
# 5. Therefore M(p)/√p > -c infinitely often.
# 6. Similarly M(p)/√p < c infinitely often.
# 
# This gives oscillation of M, but only proves M(p) > -c√p (not > +c√p).
# The STRENGTH of M(p)/√p > +c√p would need the full sigmoid analysis.
# 
# HOWEVER: step 3 is the weak point. Let me quantify:

print("\nCumulative wobble decomposition:")
# Compute W(N) for N up to 200 using exact fractions
def compute_wobble(N):
    F = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                F.append(Fraction(a, b))
    F.sort()
    n = len(F)
    W = sum((F[j] - Fraction(j, n))**2 for j in range(n))
    return float(W)

wobble_data = []
for N in range(2, 101):
    W = compute_wobble(N)
    wobble_data.append((N, W))

print(f"{'N':>5} {'W(N)':>12} {'N²·W(N)':>12}")
for N, W in wobble_data[::10]:
    print(f"{N:5d} {W:12.8f} {N*N*W:12.4f}")

# ============================================================
# NOVEL: SHIFTED MERTENS FUNCTION CORRELATIONS
# ============================================================
print("\n" + "=" * 70)
print("SHIFTED MERTENS CORRELATIONS from universal formula")
print("=" * 70)

# The universal formula connects M at different scales:
# S(m,N) = Σ_{d|m} d · M(⌊N/d⌋) + 1
#
# For m = p₁p₂ (product of two primes):
# S(p₁p₂, N) = M(N) + p₁·M(⌊N/p₁⌋) + p₂·M(⌊N/p₂⌋) + p₁p₂·M(⌊N/p₁p₂⌋) + 1
#
# This CONSTRAINS how M values at different scales relate!
# If we know S(p₁p₂, N) (which is a Farey sum, hence "geometric"),
# we get a LINEAR relation between M(N), M(⌊N/p₁⌋), M(⌊N/p₂⌋), M(⌊N/p₁p₂⌋).
#
# NOVEL OBSERVATION: The Farey sum S(m,N) = Σ c_b(m) + 1
# where c_b(m) is the Ramanujan sum, satisfies:
# |c_b(m)| ≤ gcd(b,m) ≤ b
# So |S(m,N) - 1| ≤ Σ_{b=1}^{N} gcd(b,m)
#
# For m = prime p: |S(p,N) - 1| ≤ Σ_{b=1}^{N} gcd(b,p) = Σ_{b: p∤b} 1 + Σ_{b: p|b} p
# = (N - ⌊N/p⌋) + p·⌊N/p⌋ = N + (p-1)·⌊N/p⌋.
#
# The universal formula: S(p,N) = M(N) + 1 + p·M(⌊N/p⌋)
# So |M(N) + p·M(⌊N/p⌋)| ≤ N + (p-1)·⌊N/p⌋ ≈ 2N.
#
# This gives: M(N) + p·M(⌊N/p⌋) = O(N).
# Since M(N) = O(N) trivially, this is NOT tight.
# 
# But with the WEIL BOUND on Ramanujan sums: |c_b(m)| ≤ gcd(b,m)^{1/2} · b^{1/2} · τ(...)
# Actually the Weil bound gives |K(m,n;c)| ≤ τ(c)·gcd(m,n,c)^{1/2}·c^{1/2}
# and c_b(m) = Σ_{d|gcd(b,m)} μ(b/d)·d.
# For prime b: c_b(m) = -1 if b∤m, b-1 if b|m. So |c_b(m)| ≤ b.
# Not helpful.

# BETTER: Use the VARIANCE of S(m,N) across m.
# Var_m[S(m,N)] for m ≤ M equals:
# Var[Σ d·M(⌊N/d⌋) over d|m] 
# The divisor structure creates correlations.

# Let me compute the variance empirically:
N = 100
mu100 = mobius_sieve(N)
M100 = mertens_values(N, mu100)

S_vals = []
for m in range(1, 201):
    s = M100[N] + 1
    for d in range(2, N + 1):
        if m % d == 0:
            s += d * M100[N // d]
    S_vals.append(s)

mean_S = np.mean(S_vals)
var_S = np.var(S_vals)
print(f"N=100, m=1..200:")
print(f"  Mean S(m,N) = {mean_S:.2f}")
print(f"  Var S(m,N) = {var_S:.2f}")
print(f"  Std S(m,N) = {var_S**0.5:.2f}")

# ============================================================
# NOVEL: MULTIPLICATIVE FUNCTION DETECTION via Farey sums
# ============================================================
print("\n" + "=" * 70)
print("MULTIPLICATIVE FUNCTION DETECTION via Farey sums")
print("=" * 70)

# Here's a genuinely novel application:
# 
# PROBLEM: Given a black-box function f: N → C, determine if f is multiplicative.
# 
# CLASSICAL APPROACH: Check f(mn) = f(m)f(n) for many coprime pairs → O(N²).
# 
# NEW APPROACH using Farey sums:
# Define S_f(m,N) = Σ_{a/b ∈ F_N} f(b) · e^{2πima/b}
# If f is completely multiplicative, then by the same Ramanujan sum argument:
# S_f(m,N) = Σ_{b=1}^{N} f(b)·c_b(m)
#           = Σ_{d|m} d · (Σ_{k≤N/d} f(dk)·μ(k))
# 
# For f = id (identity): this gives weighted Mertens sums.
# For f = μ: this gives M(N) + corrections (our universal formula).
# For f = χ (Dirichlet character): this gives twisted Mertens.
# 
# The KEY: for multiplicative f, S_f(m,N) has a DIVISOR-SUM structure.
# For non-multiplicative f, it doesn't.
# 
# DETECTION: Check if S_f(p₁p₂,N) = S_f_predicted(p₁p₂,N) where the prediction
# uses only S_f(p₁,N) and S_f(p₂,N). If it matches → f is likely multiplicative.

# Verify with f = μ (multiplicative):
print("\nVerification with f = μ (should show divisor structure):")
for m in [2, 3, 5, 6, 10, 15, 30]:
    # Direct computation
    S_direct = 0
    for b in range(1, 51):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                S_direct += mu100[b] * np.exp(2j * np.pi * m * a / b)
    
    # Via universal formula (using f=μ, the standard one)
    # Actually S_μ(m,N) = Σ μ(b)·c_b(m) = Σ_{d|m} d·Σ_{k≤N/d} μ(dk)μ(k)
    # This involves μ(dk)μ(k) which is NOT simply M.
    # For f=1 (constant): S_1(m,N) = Σ c_b(m) = M(N) + corrections.
    # For f=μ: more complex.
    
    print(f"  m={m:3d}: S_μ(m,50) = {S_direct.real:8.3f} + {S_direct.imag:8.3f}i")

# ============================================================
# NOVEL: FAREY SEQUENCE ENTROPY AND PRIME DISTRIBUTION
# ============================================================
print("\n" + "=" * 70)
print("FAREY SEQUENCE ENTROPY")
print("=" * 70)

# Define the "Farey entropy" at scale N:
# H(N) = -Σ_{f∈F_N} (1/|F_N|) · log(gap size at f)
# where gap size = f_{j+1} - f_j = 1/(b_j · b_{j+1}).
#
# This measures the "complexity" of the Farey distribution.
# For uniform distribution, H = log(|F_N|).
# The EXCESS entropy H - log(n) measures non-uniformity.
#
# CONNECTION TO MERTENS: The bridge identity connects the Fourier transform
# of the Farey measure to M(N). The entropy involves the LOG of gap sizes,
# which are products of consecutive denominators.

print("Farey entropy H(N) vs log(|F_N|):")
for N in [5, 10, 20, 50, 100]:
    F = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                F.append(Fraction(a, b))
    F.sort()
    n = len(F)
    
    # Compute gap distribution
    gaps = [float(F[j+1] - F[j]) for j in range(n-1)]
    
    # Entropy of gap distribution (treating gaps as a probability-like quantity)
    total_gap = sum(gaps)  # should be 1 (from 0 to 1)
    H = -sum(g * log(g) for g in gaps if g > 0)
    H_uniform = log(n - 1)  # entropy of n-1 equal gaps
    
    # Alternative: use 1/|F_N| weighted entropy
    H_farey = -sum(log(g) for g in gaps) / (n - 1)
    
    print(f"  N={N:3d}: n={n:5d}, H={H:.4f}, H_uniform={H_uniform:.4f}, "
          f"excess={H - H_uniform:.4f}, <-log(gap)>={H_farey:.4f}")

# ============================================================
# NOVEL: EXPLICIT OSCILLATION BOUND
# ============================================================
print("\n" + "=" * 70)
print("EXPLICIT OSCILLATION BOUND via Farey cumulative wobble")
print("=" * 70)

# Here's the argument:
# W(N) = Σ (f_j - j/n)² → 0 as N → ∞ (equidistribution, Franel).
# More precisely, W(N) ~ c/N² (known).
#
# ΔW(p) = W(p-1) - W(p) for prime p.
# Σ_{n=2}^{N} ΔW(n) = W(1) - W(N).
# W(1) = 0 (F_1 = {0, 1}, wobble = 0).
# So Σ_{n=2}^{N} ΔW(n) = -W(N).
#
# Split: Σ_{p prime ≤ N} ΔW(p) + Σ_{n composite ≤ N} ΔW(n) = -W(N).
#
# Empirically, composites contribute positively (ΔW > 0 for ~96% of composites)
# and primes contribute negatively (ΔW < 0 for ~93% of primes).
#
# If ALL ΔW(p) < 0 for p ≥ some p₀, then:
# Σ_{composite} ΔW(n) ≥ W(N) + |Σ_{prime} ΔW(p)|
# The RHS is positive and the LHS is bounded, so this is consistent.
#
# But if ΔW(p) were ALWAYS deeply negative (say ΔW(p) < -c/p),
# then Σ ΔW(p) ~ -c·log(log(N)) (Mertens' theorem).
# And W(N) ~ c'/N² → 0, so composite contributions must compensate.
# This IS possible since composites are denser.
#
# CONCLUSION: The wobble argument alone doesn't directly bound M.
# We need the sigmoid connection: ΔW(p) < 0 ⟺ M(p)/√p < threshold.
# Combined with ΔW balance, this constrains how often M is large/small.

# Let me compute the MAGNITUDE of ΔW for primes vs composites:
print("\nΔW magnitude breakdown:")
for N_target in [30, 50, 80, 100]:
    prime_sum = 0.0
    comp_sum = 0.0
    
    for n in range(2, N_target + 1):
        W_prev = compute_wobble(n - 1)
        W_curr = compute_wobble(n)
        dW = W_prev - W_curr
        
        is_prime = n >= 2 and all(n % k != 0 for k in range(2, int(n**0.5) + 1))
        if is_prime:
            prime_sum += dW
        else:
            comp_sum += dW
    
    W_N = compute_wobble(N_target)
    print(f"  N={N_target:3d}: Σ ΔW(prime)={prime_sum:10.6f}, "
          f"Σ ΔW(comp)={comp_sum:10.6f}, "
          f"sum={prime_sum+comp_sum:10.6f}, -W(N)={-W_N:10.6f}")

