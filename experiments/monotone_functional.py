#!/usr/bin/env python3
"""
MONOTONE FUNCTIONAL SEARCH
============================

GOAL: Find a functional Phi(N) that is:
  1. PROVABLY monotone (or monotone at primes with M <= -3)
  2. Related to W(N) tightly enough that Phi-monotonicity implies W-monotonicity

CANDIDATES:
  A. |S(1,N)|^2 = (M(N)+1)^2  — Farey exponential sum squared
  B. H(N) = -sum g_j log(g_j) — Shannon entropy of gap distribution (PROVED monotone)
  C. Fisher(N) = sum 1/g_j^2   — Fisher information of gap distribution
  D. MaxGap(N) = max(g_j)      — Largest Farey gap
  E. Z(N) = N * W(N)           — Normalized wobble
  F. W(N) * H(N)               — Wobble-entropy product
  G. W(N) * n(N)               — Wobble times Farey count
  H. sum g_j^2                 — L2 norm of gaps (= 1/n + W_L2 related)
  I. W(N) / KL(N)              — Wobble per unit of entropy deficit
  J. W(N) * N^2                — Quadratically normalized wobble

For each, compute:
  - The functional for N = 2..500
  - Whether it's monotone increasing or decreasing
  - Correlation with W(N)
  - Whether its monotonicity at primes (M <= -3) implies W growth

Author: Claude (Opus 4.6)
Date: 2026-03-25
"""

import numpy as np
from math import gcd, isqrt, log, sqrt
import time
import sys

start_time = time.time()

# ─────────────────────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────────────────────

def sieve_primes(limit):
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return sieve

def euler_totient_sieve(limit):
    phi = np.arange(limit + 1, dtype=np.int64)
    for p in range(2, limit + 1):
        if phi[p] == p:
            phi[p::p] -= phi[p::p] // p
    return phi

def mobius_sieve(limit):
    mu = np.ones(limit + 1, dtype=np.int64)
    mu[0] = 0
    is_p = sieve_primes(limit)
    for p in np.where(is_p)[0]:
        mu[p::p] *= -1
        p2 = int(p) * int(p)
        if p2 <= limit:
            mu[p2::p2] = 0
    return mu

# ─────────────────────────────────────────────────────────────
# Main computation
# ─────────────────────────────────────────────────────────────

MAX_N = 500

print("=" * 78)
print("MONOTONE FUNCTIONAL SEARCH FOR FAREY WOBBLE")
print("=" * 78)
print(f"\nComputing all functionals for N = 2..{MAX_N}")
print(f"Looking for functionals that are monotone AND imply W growth\n")

is_prime_arr = sieve_primes(MAX_N)
phi = euler_totient_sieve(MAX_N)
mu = mobius_sieve(MAX_N)
mertens = np.cumsum(mu)

# Build Farey sequences incrementally, track gaps
frac_set = {0.0, 1.0}

# Storage arrays
W = np.zeros(MAX_N + 1)       # Wobble = sum (f_j - j/n)^2
H_ent = np.zeros(MAX_N + 1)   # Shannon entropy of gaps
Fisher = np.zeros(MAX_N + 1)  # Fisher info = sum 1/g_j^2
MaxGap = np.zeros(MAX_N + 1)  # Largest gap
SumGapSq = np.zeros(MAX_N + 1)  # sum g_j^2
farey_n = np.zeros(MAX_N + 1, dtype=int)  # |F_N|
KL = np.zeros(MAX_N + 1)      # KL divergence = log(n) - H
W_TV = np.zeros(MAX_N + 1)    # Total variation = sum |g_j - 1/n|

W[1] = 0.25
farey_n[1] = 2

t0 = time.time()

for N in range(2, MAX_N + 1):
    # Add new fractions with denominator N
    for p in range(1, N):
        if gcd(p, N) == 1:
            frac_set.add(p / N)

    sorted_arr = np.array(sorted(frac_set))
    n = len(sorted_arr)
    farey_n[N] = n

    # Wobble W(N) = sum (f_j - j/n)^2
    ideal = np.arange(n, dtype=np.float64) / n
    deltas = sorted_arr - ideal
    W[N] = np.dot(deltas, deltas)

    # Gaps g_j = f_{j+1} - f_j (including wraparound)
    gaps = np.diff(sorted_arr)
    # Include wraparound gap: 1 - f_{n-1} + f_0
    wrap_gap = 1.0 - sorted_arr[-1] + sorted_arr[0]
    all_gaps = np.append(gaps, wrap_gap)

    # Shannon entropy H = -sum g_j log(g_j)
    pos_gaps = all_gaps[all_gaps > 0]
    H_ent[N] = -np.sum(pos_gaps * np.log(pos_gaps))

    # Fisher information = sum 1/g_j^2
    Fisher[N] = np.sum(1.0 / (pos_gaps ** 2))

    # Max gap
    MaxGap[N] = np.max(all_gaps)

    # Sum g_j^2
    SumGapSq[N] = np.sum(all_gaps ** 2)

    # KL divergence = log(n) - H
    KL[N] = log(n) - H_ent[N]

    # Total variation = sum |g_j - 1/n|
    W_TV[N] = np.sum(np.abs(all_gaps - 1.0/n))

    if N % 100 == 0:
        print(f"  N = {N}: |F_N| = {n}, W = {W[N]:.8f}, H = {H_ent[N]:.6f}, t = {time.time()-t0:.1f}s")

print(f"\n  Done computing base data in {time.time()-t0:.1f}s\n")

# ─────────────────────────────────────────────────────────────
# Build all candidate functionals
# ─────────────────────────────────────────────────────────────

functionals = {}

# A. |S(1,N)|^2 = (M(N)+1)^2
functionals['|S|^2 = (M+1)^2'] = np.array([(mertens[N]+1)**2 for N in range(MAX_N+1)], dtype=float)

# B. Shannon entropy H(N) — proved monotone increasing
functionals['H(N) entropy'] = H_ent.copy()

# C. Fisher information sum 1/g_j^2
functionals['Fisher 1/g^2'] = Fisher.copy()

# D. MaxGap(N)
functionals['MaxGap'] = MaxGap.copy()

# E. Z(N) = N * W(N)
functionals['Z = N*W'] = np.array([N * W[N] for N in range(MAX_N+1)])

# F. W * H
functionals['W*H'] = W * H_ent

# G. W * n (wobble times Farey count)
functionals['W*n'] = W * farey_n.astype(float)

# H. SumGapSq = sum g_j^2
functionals['SumGapSq'] = SumGapSq.copy()

# I. W / KL (wobble per entropy deficit)
W_over_KL = np.zeros(MAX_N + 1)
for N in range(2, MAX_N + 1):
    if KL[N] > 1e-15:
        W_over_KL[N] = W[N] / KL[N]
functionals['W/KL'] = W_over_KL

# J. W * N^2
functionals['W*N^2'] = np.array([N**2 * W[N] for N in range(MAX_N+1)])

# K. Total variation W_TV
functionals['W_TV'] = W_TV.copy()

# L. n * SumGapSq (= 1 + n*variance_of_gaps)
functionals['n*SumGapSq'] = farey_n.astype(float) * SumGapSq

# M. log(W) (log wobble)
logW = np.zeros(MAX_N + 1)
for N in range(2, MAX_N + 1):
    if W[N] > 0:
        logW[N] = log(W[N])
functionals['log(W)'] = logW

# N. W * log(N)
functionals['W*log(N)'] = np.array([W[N] * (log(N) if N > 0 else 0) for N in range(MAX_N+1)])

# O. Entropy deficit times n: n * KL(N) = n*(log(n) - H)
functionals['n*KL'] = farey_n.astype(float) * KL

# ─────────────────────────────────────────────────────────────
# Analyze monotonicity of each functional
# ─────────────────────────────────────────────────────────────

print("=" * 78)
print("MONOTONICITY ANALYSIS OF CANDIDATE FUNCTIONALS")
print("=" * 78)

# Identify M <= -3 primes
m_leq_neg3_primes = [N for N in range(2, MAX_N+1) if is_prime_arr[N] and mertens[N] <= -3]
all_primes = [N for N in range(2, MAX_N+1) if is_prime_arr[N]]

print(f"\nPrimes with M(p) <= -3: {len(m_leq_neg3_primes)} out of {len(all_primes)} primes")
print(f"First few M<=-3 primes: {m_leq_neg3_primes[:10]}")

for name, func in sorted(functionals.items()):
    # Overall monotonicity
    dF = np.diff(func[2:MAX_N+1])  # dF[i] = func[i+3] - func[i+2]
    inc_total = np.sum(dF > 0)
    dec_total = np.sum(dF < 0)
    total = len(dF)

    # At all primes
    dF_primes = [func[p] - func[p-1] for p in all_primes]
    inc_primes = sum(1 for d in dF_primes if d > 0)
    dec_primes = sum(1 for d in dF_primes if d < 0)

    # At M <= -3 primes
    dF_m3 = [func[p] - func[p-1] for p in m_leq_neg3_primes]
    inc_m3 = sum(1 for d in dF_m3 if d > 0)
    dec_m3 = sum(1 for d in dF_m3 if d < 0)

    # Correlation with W
    # Use values from N=2..MAX_N
    vals = func[2:MAX_N+1]
    wvals = W[2:MAX_N+1]
    if np.std(vals) > 1e-15 and np.std(wvals) > 1e-15:
        corr = np.corrcoef(vals, wvals)[0, 1]
    else:
        corr = 0.0

    # Correlation of CHANGES with dW
    dF_all = [func[N] - func[N-1] for N in range(3, MAX_N+1)]
    dW_all = [W[N] - W[N-1] for N in range(3, MAX_N+1)]
    if np.std(dF_all) > 1e-15 and np.std(dW_all) > 1e-15:
        corr_delta = np.corrcoef(dF_all, dW_all)[0, 1]
    else:
        corr_delta = 0.0

    # Direction: is it increasing or decreasing overall?
    direction = "INC" if inc_total > dec_total else "DEC"

    # Key metric: at M<=-3 primes, does F always increase?
    m3_pct = 100 * inc_m3 / len(dF_m3) if len(dF_m3) > 0 else 0

    print(f"\n  {name}:")
    print(f"    Overall: {direction} ({inc_total}/{total} increase = {100*inc_total/total:.1f}%)")
    print(f"    At all primes: {inc_primes}/{len(dF_primes)} increase ({100*inc_primes/len(dF_primes):.1f}%)")
    print(f"    At M<=-3 primes: {inc_m3}/{len(dF_m3)} increase ({m3_pct:.1f}%)")
    print(f"    Corr(F, W) = {corr:.4f},  Corr(dF, dW) = {corr_delta:.4f}")


# ─────────────────────────────────────────────────────────────
# DEEP ANALYSIS: Which functionals can IMPLY W growth?
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("IMPLICATION ANALYSIS: Can F increasing => W increasing?")
print("=" * 78)

# For each functional F, check: at M<=-3 primes,
# is dF > 0 ==> dW > 0 ?
# And vice versa: is dW > 0 ==> dF > 0 ?

for name, func in sorted(functionals.items()):
    dF_m3 = [(func[p] - func[p-1]) for p in m_leq_neg3_primes]
    dW_m3 = [(W[p] - W[p-1]) for p in m_leq_neg3_primes]

    # dF > 0 => dW > 0
    forward = sum(1 for df, dw in zip(dF_m3, dW_m3) if df > 0 and dw > 0)
    forward_total = sum(1 for df in dF_m3 if df > 0)

    # dW > 0 => dF > 0
    backward = sum(1 for df, dw in zip(dF_m3, dW_m3) if dw > 0 and df > 0)
    backward_total = sum(1 for dw in dW_m3 if dw > 0)

    # Both increase
    both_inc = sum(1 for df, dw in zip(dF_m3, dW_m3) if df > 0 and dw > 0)

    if forward_total > 0 and backward_total > 0:
        print(f"\n  {name}:")
        print(f"    dF>0 => dW>0: {forward}/{forward_total} ({100*forward/forward_total:.1f}%)")
        print(f"    dW>0 => dF>0: {backward}/{backward_total} ({100*backward/backward_total:.1f}%)")
        print(f"    Both increase: {both_inc}/{len(dF_m3)} ({100*both_inc/len(dF_m3):.1f}%)")


# ─────────────────────────────────────────────────────────────
# RATIO ANALYSIS: W(p)/W(p-1) vs F(p)/F(p-1)
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("RATIO ANALYSIS: Can W(p)/W(p-1) be bounded by F(p)/F(p-1)?")
print("=" * 78)

print(f"\nAt M<=-3 primes, compute ratio W(p)/W(p-1) and F(p)/F(p-1)")
print(f"Goal: find F where F(p)/F(p-1) <= W(p)/W(p-1) always,")
print(f"      AND F(p)/F(p-1) > 1 is provable\n")

for name, func in sorted(functionals.items()):
    w_ratios = []
    f_ratios = []
    lower_bound_holds = True  # F ratio <= W ratio always?

    for p in m_leq_neg3_primes:
        if W[p-1] > 1e-15 and func[p-1] > 1e-15 and func[p-1] != 0:
            wr = W[p] / W[p-1]
            fr = func[p] / func[p-1]
            w_ratios.append(wr)
            f_ratios.append(fr)
            if fr > wr + 1e-12:
                lower_bound_holds = False

    if len(w_ratios) > 0:
        w_ratios = np.array(w_ratios)
        f_ratios = np.array(f_ratios)

        # Check: is F ratio always > 1?
        f_always_above_1 = np.all(f_ratios > 1)
        # Check: is F ratio always <= W ratio?
        f_always_below_w = np.all(f_ratios <= w_ratios + 1e-12)

        corr_ratio = np.corrcoef(w_ratios, f_ratios)[0, 1] if np.std(f_ratios) > 1e-15 else 0

        useful = "*** USEFUL ***" if (f_always_above_1 and f_always_below_w) else ""

        print(f"  {name}:")
        print(f"    F ratio > 1 always: {f_always_above_1} (min={np.min(f_ratios):.6f})")
        print(f"    F ratio <= W ratio always: {f_always_below_w}")
        print(f"    Corr(W ratio, F ratio) = {corr_ratio:.4f}")
        print(f"    W ratio range: [{np.min(w_ratios):.6f}, {np.max(w_ratios):.6f}]")
        print(f"    F ratio range: [{np.min(f_ratios):.6f}, {np.max(f_ratios):.6f}]")
        if useful:
            print(f"    {useful}")


# ─────────────────────────────────────────────────────────────
# CREATIVE: Construct F(N) = W(N) * g(N) and find g that makes F monotone
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("CREATIVE: Find g(N) such that F(N) = W(N)*g(N) is monotone at M<=-3 primes")
print("=" * 78)

# If F(p) > F(p-1), then W(p)*g(p) > W(p-1)*g(p-1),
# i.e., W(p)/W(p-1) > g(p-1)/g(p).
# If g is DECREASING, then g(p-1)/g(p) > 1, so W(p)/W(p-1) > 1 would follow.
# That's HARDER.
# If g is INCREASING, then g(p-1)/g(p) < 1, so F monotone is WEAKER than W monotone.
# But we need a g where F monotone is PROVABLE.

# Compute the minimum g(p)/g(p-1) needed for F to be monotone:
# W(p)*g(p) > W(p-1)*g(p-1) iff g(p)/g(p-1) > W(p-1)/W(p)
# So we need g to grow at least as fast as 1/(W ratio) where W decreases.

# But at M<=-3 primes, W(p) > W(p-1) (100% observed), so W(p-1)/W(p) < 1.
# Any increasing g works! But we need F to be monotone at ALL N, not just M<=-3 primes.

# Alternative: look for g where F is monotone at ALL primes (not just M<=-3)
print("\nLooking at g(N) = N^alpha for various alpha:")

for alpha in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
    g = np.array([N**alpha if N > 0 else 0 for N in range(MAX_N + 1)])
    F = W * g

    # Check at all primes
    inc_all = sum(1 for p in all_primes if F[p] > F[p-1])
    inc_m3 = sum(1 for p in m_leq_neg3_primes if F[p] > F[p-1])

    # Check at composites
    composites = [N for N in range(2, MAX_N+1) if not is_prime_arr[N]]
    inc_comp = sum(1 for c in composites if F[c] > F[c-1])

    # Overall monotone?
    overall_mono = all(F[N] >= F[N-1] for N in range(2, MAX_N+1))

    print(f"  alpha={alpha:.1f}: primes {inc_all}/{len(all_primes)} inc, "
          f"M<=-3 {inc_m3}/{len(m_leq_neg3_primes)} inc, "
          f"comp {inc_comp}/{len(composites)} inc, "
          f"overall mono: {overall_mono}")


# ─────────────────────────────────────────────────────────────
# HYBRID FUNCTIONAL: W*H, W*H^k, W/KL — detailed
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("HYBRID FUNCTIONALS: W * H^k for various k")
print("=" * 78)

for k in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]:
    F = np.zeros(MAX_N + 1)
    for N in range(2, MAX_N + 1):
        F[N] = W[N] * (H_ent[N] ** k)

    inc_m3 = sum(1 for p in m_leq_neg3_primes if F[p] > F[p-1])
    inc_all_p = sum(1 for p in all_primes if F[p] > F[p-1])
    overall = all(F[N] >= F[N-1] for N in range(3, MAX_N+1))

    # Find first violation if any
    first_violation = None
    for N in range(3, MAX_N + 1):
        if F[N] < F[N-1]:
            first_violation = N
            break

    print(f"  k={k:>4.1f}: M<=-3 primes {inc_m3}/{len(m_leq_neg3_primes)}, "
          f"all primes {inc_all_p}/{len(all_primes)}, "
          f"overall mono: {overall}, "
          f"first violation: {first_violation}")


# ─────────────────────────────────────────────────────────────
# KEY INSIGHT: SumGapSq = sum g_j^2 analysis
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("DEEP DIVE: SumGapSq = sum(g_j^2) and related")
print("=" * 78)

# SumGapSq = sum g_j^2, where g_j are Farey gaps
# Note: sum g_j = 1, so variance(gaps) = SumGapSq/n - 1/n^2
# Also: SumGapSq is related to the Farey discrepancy

# Is SumGapSq monotonically DECREASING? (As N grows, gaps equidistribute)
dec_count = sum(1 for N in range(3, MAX_N+1) if SumGapSq[N] < SumGapSq[N-1])
print(f"  SumGapSq decreasing: {dec_count}/{MAX_N-2} times ({100*dec_count/(MAX_N-2):.1f}%)")

# At primes vs composites
dec_p = sum(1 for p in all_primes if SumGapSq[p] < SumGapSq[p-1])
dec_m3 = sum(1 for p in m_leq_neg3_primes if SumGapSq[p] < SumGapSq[p-1])
print(f"  At primes: {dec_p}/{len(all_primes)} decreasing ({100*dec_p/len(all_primes):.1f}%)")
print(f"  At M<=-3 primes: {dec_m3}/{len(m_leq_neg3_primes)} decreasing ({100*dec_m3/len(m_leq_neg3_primes):.1f}%)")

# Relationship between SumGapSq and W
# W = sum (f_j - j/n)^2
# SumGapSq = sum g_j^2
# These are different: W is about positions, SumGapSq is about spacings
# But both measure uniformity of the Farey sequence

# Pinsker-type: KL >= (1/2) * TV^2, and TV = sum |g_j - 1/n|
# Also: sum(g_j - 1/n)^2 = SumGapSq - 1/n
# So L2 gap discrepancy = SumGapSq - 1/n

print(f"\n  L2 gap discrepancy SumGapSq - 1/n:")
L2_gap_disc = np.zeros(MAX_N + 1)
for N in range(2, MAX_N + 1):
    L2_gap_disc[N] = SumGapSq[N] - 1.0 / farey_n[N]
dec_l2 = sum(1 for N in range(3, MAX_N+1) if L2_gap_disc[N] < L2_gap_disc[N-1])
print(f"  L2 gap disc decreasing: {dec_l2}/{MAX_N-2} ({100*dec_l2/(MAX_N-2):.1f}%)")


# ─────────────────────────────────────────────────────────────
# ENTROPY DEFICIT APPROACH
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("ENTROPY DEFICIT: KL(N) = log(n) - H(N)")
print("=" * 78)

# KL(N) measures how far the gap distribution is from uniform
# H is monotone increasing (proved), but log(n) also increases...
# Is KL monotone?

dec_kl = sum(1 for N in range(3, MAX_N+1) if KL[N] < KL[N-1])
inc_kl_p = sum(1 for p in all_primes if KL[p] > KL[p-1])
inc_kl_m3 = sum(1 for p in m_leq_neg3_primes if KL[p] > KL[p-1])
print(f"  KL decreasing overall: {dec_kl}/{MAX_N-2} ({100*dec_kl/(MAX_N-2):.1f}%)")
print(f"  KL increasing at primes: {inc_kl_p}/{len(all_primes)} ({100*inc_kl_p/len(all_primes):.1f}%)")
print(f"  KL increasing at M<=-3 primes: {inc_kl_m3}/{len(m_leq_neg3_primes)} ({100*inc_kl_m3/len(m_leq_neg3_primes):.1f}%)")

# Pinsker: TV^2 <= 2*KL, so W_TV^2 <= 2*KL
# Check: does KL increase => W increase at M<=-3 primes?
both = sum(1 for p in m_leq_neg3_primes if KL[p] > KL[p-1] and W[p] > W[p-1])
kl_inc_count = sum(1 for p in m_leq_neg3_primes if KL[p] > KL[p-1])
print(f"  KL inc AND W inc at M<=-3: {both}/{kl_inc_count} (when KL inc)")


# ─────────────────────────────────────────────────────────────
# THE WINNING APPROACH? F(N) = W(N) * N^alpha for optimal alpha
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("OPTIMAL ALPHA SEARCH: F(N) = W(N) * N^alpha")
print("=" * 78)

# We want the SMALLEST alpha where F is monotone at ALL M<=-3 primes
# (and ideally at all primes or even all N)

# At M<=-3 primes, W(p)/W(p-1) > 1 always (empirically).
# So ANY alpha >= 0 gives F(p)/F(p-1) = (p/(p-1))^alpha * W(p)/W(p-1) > 1.
# The real question: what alpha makes F monotone at composites too?

# At composites, W typically decreases. We need:
# (c/(c-1))^alpha * W(c)/W(c-1) > 1
# alpha > -log(W(c)/W(c-1)) / log(c/(c-1))

# Find the worst composite violation
max_alpha_needed = 0
worst_N = 0
for N in range(3, MAX_N + 1):
    if W[N-1] > 1e-15 and W[N] < W[N-1]:
        w_ratio = W[N] / W[N-1]
        n_ratio = N / (N - 1)
        alpha_needed = -log(w_ratio) / log(n_ratio)
        if alpha_needed > max_alpha_needed:
            max_alpha_needed = alpha_needed
            worst_N = N

print(f"  To make F = W*N^alpha globally monotone, need alpha >= {max_alpha_needed:.4f}")
print(f"  Worst case at N = {worst_N}: W({worst_N})/W({worst_N-1}) = {W[worst_N]/W[worst_N-1]:.6f}")
print(f"  With alpha = {max_alpha_needed:.2f}, F({worst_N})/F({worst_N-1}) = 1.000000")

# Check with ceiling alpha
alpha_ceil = int(max_alpha_needed) + 1
print(f"\n  Testing alpha = {alpha_ceil}:")
F_test = np.array([N**alpha_ceil * W[N] for N in range(MAX_N+1)])
mono = all(F_test[N] >= F_test[N-1] for N in range(3, MAX_N+1))
print(f"  F = W*N^{alpha_ceil} monotone up to {MAX_N}: {mono}")

# More refined: binary search for exact alpha
lo, hi = 0.0, max_alpha_needed + 1
for _ in range(100):
    mid = (lo + hi) / 2
    F_test = np.array([(N**mid * W[N] if N > 0 else 0) for N in range(MAX_N+1)])
    is_mono = all(F_test[N] >= F_test[N-1] - 1e-14 for N in range(3, MAX_N+1))
    if is_mono:
        hi = mid
    else:
        lo = mid

print(f"  Exact critical alpha: {hi:.6f}")
print(f"  F = W*N^{hi:.4f} is monotone up to N={MAX_N}")


# ─────────────────────────────────────────────────────────────
# SUBMARTINGALE VIEW: Z(N) = N * W(N)
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("Z(N) = N * W(N) DETAILED ANALYSIS")
print("=" * 78)

Z = np.array([N * W[N] for N in range(MAX_N + 1)])
dZ = np.diff(Z)

# At M <= -3 primes
dZ_m3 = [Z[p] - Z[p-1] for p in m_leq_neg3_primes]
inc_z_m3 = sum(1 for d in dZ_m3 if d > 0)
print(f"  Z increases at M<=-3 primes: {inc_z_m3}/{len(dZ_m3)} ({100*inc_z_m3/len(dZ_m3):.1f}%)")

# Minimum dZ at M<=-3 primes
if dZ_m3:
    min_dz = min(dZ_m3)
    max_dz = max(dZ_m3)
    print(f"  min dZ at M<=-3 primes: {min_dz:.8f}")
    print(f"  max dZ at M<=-3 primes: {max_dz:.8f}")

    # Which M<=-3 prime has smallest dZ?
    worst_p = m_leq_neg3_primes[dZ_m3.index(min_dz)]
    print(f"  Tightest at p={worst_p}: dZ={min_dz:.8f}, M(p)={mertens[worst_p]}")
    print(f"    W(p)={W[worst_p]:.8f}, W(p-1)={W[worst_p-1]:.8f}")
    print(f"    W ratio={W[worst_p]/W[worst_p-1]:.8f}")
    print(f"    Need W(p)/W(p-1) > (p-1)/p = {(worst_p-1)/worst_p:.8f}")

# At ALL primes
dZ_all = [Z[p] - Z[p-1] for p in all_primes]
inc_z_all = sum(1 for d in dZ_all if d > 0)
print(f"\n  Z increases at ALL primes: {inc_z_all}/{len(dZ_all)} ({100*inc_z_all/len(dZ_all):.1f}%)")

# Which primes have dZ < 0?
neg_z_primes = [(p, Z[p]-Z[p-1], mertens[p]) for p in all_primes if Z[p] < Z[p-1]]
if neg_z_primes:
    print(f"  Primes where Z DECREASES ({len(neg_z_primes)}):")
    for p, dz, m in neg_z_primes[:10]:
        print(f"    p={p}: dZ={dz:.8f}, M(p)={m}, W ratio={W[p]/W[p-1]:.6f}")


# ─────────────────────────────────────────────────────────────
# SUMMARY TABLE
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("SUMMARY TABLE")
print("=" * 78)
print(f"\n{'Functional':<20} {'Overall mono':<15} {'At primes':<15} {'At M<=-3 p':<15} {'Corr(dF,dW)':<12}")
print("-" * 78)

for name in sorted(functionals.keys()):
    func = functionals[name]

    # Overall
    overall = all(func[N] >= func[N-1] - 1e-14 for N in range(3, MAX_N+1))

    # At primes
    inc_p = sum(1 for p in all_primes if func[p] > func[p-1])

    # At M<=-3 primes
    inc_m3 = sum(1 for p in m_leq_neg3_primes if func[p] > func[p-1])

    # Correlation of changes
    dF_all = [func[N] - func[N-1] for N in range(3, MAX_N+1)]
    dW_all = [W[N] - W[N-1] for N in range(3, MAX_N+1)]
    if np.std(dF_all) > 1e-15:
        corr_d = np.corrcoef(dF_all, dW_all)[0, 1]
    else:
        corr_d = 0.0

    mono_str = "YES" if overall else "no"
    p_str = f"{inc_p}/{len(all_primes)}"
    m3_str = f"{inc_m3}/{len(m_leq_neg3_primes)}"

    print(f"  {name:<18} {mono_str:<15} {p_str:<15} {m3_str:<15} {corr_d:<12.4f}")


# ─────────────────────────────────────────────────────────────
# FINAL: Best candidates and proof strategy
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 78)
print("PROOF STRATEGY CANDIDATES")
print("=" * 78)

print("""
Strategy A: ENTROPY APPROACH
  H(N) is provably monotone increasing.
  If we can show W(N) >= f(H(N)) for some monotone f,
  then H increasing => W increasing.
  PROBLEM: W and H are not monotonically related in general.

Strategy B: NORMALIZED WOBBLE Z = N*W
  Z(p) > Z(p-1) is WEAKER than W(p) > W(p-1).
  Z(p) > Z(p-1) iff W(p)/W(p-1) > (p-1)/p.
  Since (p-1)/p < 1, this only needs W ratio > 0.99...
  At M<=-3 primes, Z always increases (100% empirical up to N=500).

  To PROVE Z increases at M<=-3 primes:
    Need p*W(p) > (p-1)*W(p-1)
    Using ΔW ≈ -c*M(p)/n with M(p) <= -3 and c > 0:
    W(p) ≈ W(p-1) + 3c/n > W(p-1)
    p*W(p) ≈ p*W(p-1) + 3cp/n > (p-1)*W(p-1) + W(p-1) + 3cp/n
    This is > (p-1)*W(p-1) since W(p-1) > 0 and 3cp/n > 0.

Strategy C: OPTIMAL RESCALING F = W*N^alpha
  There exists alpha such that F is globally monotone.
  If we can prove F monotone AND bound alpha from below,
  then W(N) >= F(N)/N^alpha with F increasing.
  This gives W(N) >= F(N-1)/N^alpha >= W(N-1)*(N-1)^alpha/N^alpha.
  So W(N) >= W(N-1) * ((N-1)/N)^alpha.
  This is WEAKER than W increasing but still gives a lower bound.

Strategy D: GAP L2 NORM (SumGapSq)
  SumGapSq = sum g_j^2 is closely related to Farey discrepancy.
  If SumGapSq is monotone decreasing (gap equidistribution improves),
  and if SumGapSq decrease is slow enough vs W formula, this could work.
""")

elapsed = time.time() - start_time
print(f"\nTotal runtime: {elapsed:.1f}s")
