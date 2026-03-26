#!/usr/bin/env python3
"""
PER-DENOMINATOR STRUCTURE OF B+C
==================================

GOAL: Find why B+C > 0 by decomposing into denominator contributions.

KEY IDENTITY:
  B+C = Σ_{f in F_{p-1}} [D_Fp(f)^2 - D_Fp-1(f)^2]
      = Σ_{b=2}^{p-1} (B_b + C_b)
  where B_b + C_b = Σ_{gcd(a,b)=1, 1≤a<b} δ(a/b)·[2D(a/b) + δ(a/b)]
                  = Σ_a [D_Fp(a/b)^2 - D_old(a/b)^2]

This script computes:
  1. Per-denominator contributions (B_b + C_b) for each b
  2. Identifies which denominators contribute negatively
  3. Analyzes the orbit structure of σ_p on coprime residues mod b
  4. Tests whether B_b + C_b can be bounded via the orbit structure
  5. Looks for the "special" denominators that dominate

PROBABILISTIC MODEL:
  D(a/b) and δ(a/b) are positively correlated in aggregate.
  We test: within each ORBIT of σ_p^k acting on {coprime a mod b},
  is the contribution non-negative?

NEW BOUND IDEA:
  B_b + C_b = Σ_{orb} [Σ_{a in orb} D(a/b)·δ(a/b) + δ(a/b)^2/2
                       + (orbit-coupling terms)]
"""

import time
from math import gcd, isqrt, log, pi
from fractions import Fraction

start_time = time.time()

# ================================================================
# UTILITIES
# ================================================================

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def mertens_sieve(limit):
    smallest_prime = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if smallest_prime[i] == 0:
            for j in range(i, limit + 1, i):
                if smallest_prime[j] == 0:
                    smallest_prime[j] = i
    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        rem = n
        sq_free = True
        num_factors = 0
        while rem > 1:
            sp = smallest_prime[rem]
            count = 0
            while rem % sp == 0:
                rem //= sp
                count += 1
            if count >= 2:
                sq_free = False
                break
            num_factors += 1
        if sq_free:
            mu[n] = (-1) ** num_factors
    M = [0] * (limit + 1)
    for i in range(1, limit + 1):
        M[i] = M[i-1] + mu[i]
    return mu, M

def build_farey_with_ranks(N):
    """Build F_N and compute rank, D values for all fractions."""
    fracs = []  # (a, b)
    a, b = 0, 1
    c, d = 1, N
    fracs.append((0, 1))
    while (c, d) != (1, 1):
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        fracs.append((c, d))
    n = len(fracs)
    # D(f_j) = j - n*(a_j/b_j) using 0-indexed rank
    D_vals = {}  # (a,b) -> D
    for idx, (aa, bb) in enumerate(fracs):
        D_vals[(aa, bb)] = idx - n * aa / bb
    return fracs, D_vals, n

def per_denominator_BC(N, p, D_vals):
    """
    Compute (B_b + C_b) for each b in [2, N].

    B_b = 2 * Σ_{gcd(a,b)=1, 1≤a<b} D(a/b) * δ(a/b)
    C_b =     Σ_{gcd(a,b)=1, 1≤a<b} δ(a/b)^2
    where δ(a/b) = (a - p*a mod b) / b
    """
    result = {}
    for b in range(2, N + 1):
        B_b = 0.0
        C_b = 0.0
        for a in range(1, b):
            if gcd(a, b) != 1:
                continue
            sigma = (p * a) % b  # p*a mod b
            delta = (a - sigma) / b
            D = D_vals.get((a, b), 0.0)
            B_b += 2 * D * delta
            C_b += delta * delta
        result[b] = (B_b, C_b, B_b + C_b)
    return result

def orbit_structure(b, p):
    """
    Compute orbits of σ_p: a → p*a mod b acting on coprime residues {1,...,b-1}.
    Returns list of orbits (each orbit is a list of residues).
    """
    coprime = [a for a in range(1, b) if gcd(a, b) == 1]
    visited = set()
    orbits = []
    for a0 in coprime:
        if a0 in visited:
            continue
        orbit = []
        a = a0
        while a not in visited:
            visited.add(a)
            orbit.append(a)
            a = (p * a) % b
        orbits.append(orbit)
    return orbits

def orbit_BC_contribution(orbit, b, p, D_vals):
    """
    Compute the B+C contribution from a single orbit.
    orbit = list of coprime residues forming a cycle under σ_p.
    """
    L = len(orbit)
    total = 0.0
    for i, a in enumerate(orbit):
        a_next = orbit[(i + 1) % L]  # σ_p(a) = a_next (check: p*a mod b = a_next)
        # Actually orbit is {a, p*a mod b, p^2*a mod b, ...}
        # so σ_p(orbit[i]) = orbit[(i+1) % L]
        sigma_a = (p * a) % b
        delta_a = (a - sigma_a) / b
        D_a = D_vals.get((a, b), 0.0)
        total += 2 * D_a * delta_a + delta_a * delta_a
    return total

# ================================================================
# MAIN ANALYSIS
# ================================================================

LIMIT = 200
primes = sieve_primes(LIMIT)
phi = euler_totient_sieve(LIMIT)
mu, M = mertens_sieve(LIMIT)

print("=" * 80)
print("PER-DENOMINATOR B+C STRUCTURE ANALYSIS")
print("=" * 80)

print("\n--- Section 1: Per-prime summary with per-denominator breakdown ---")
print(f"\n{'p':>5} {'M(p)':>5} {'B+C_tot':>12} {'#neg_b':>7} {'min_Bb+Cb':>12} {'worst_b':>8}")
print("-" * 60)

neg_denom_examples = []  # collect (p, b, B_b+C_b) for negative denominator contributions

for p in primes:
    if p < 11:
        continue
    N = p - 1
    fracs, D_vals, n = build_farey_with_ranks(N)

    denom_BC = per_denominator_BC(N, p, D_vals)

    total_BC = sum(v[2] for v in denom_BC.values())
    neg_b = [(b, v[2]) for b, v in denom_BC.items() if v[2] < 0]

    min_bc = min((v[2] for v in denom_BC.values()), default=0.0)
    worst_b = min(denom_BC, key=lambda b: denom_BC[b][2], default=None)

    Mval = M[p]
    print(f"{p:>5} {Mval:>5} {total_BC:>12.4f} {len(neg_b):>7} {min_bc:>12.4f} {worst_b:>8}")

    # Collect examples of negative denominators
    for b, bc in neg_b:
        neg_denom_examples.append((p, b, bc, denom_BC[b][0], denom_BC[b][1]))

print("\n--- Section 2: Negative denominator examples ---")
if neg_denom_examples:
    print(f"\n{'p':>5} {'b':>5} {'B_b+C_b':>12} {'B_b':>12} {'C_b':>12} {'phi(b)':>7} {'p mod b':>7}")
    print("-" * 60)
    for (p, b, bc, Bb, Cb) in neg_denom_examples[:50]:
        print(f"{p:>5} {b:>5} {bc:>12.4f} {Bb:>12.4f} {Cb:>12.4f} {phi[b]:>7} {p%b:>7}")
else:
    print("  No negative denominator contributions found!")

print("\n--- Section 3: Orbit structure analysis for a sample prime ---")
p_sample = 47  # prime with M(p) ≤ -3
N_sample = p_sample - 1
fracs_s, D_vals_s, n_s = build_farey_with_ranks(N_sample)

print(f"\nFor p = {p_sample} (M(p) = {M[p_sample]}), N = {N_sample}:")
print(f"\n{'b':>4} {'B_b+C_b':>12} {'#orbits':>8} {'orbit_lens':>20} {'per-orbit BC':>30}")
print("-" * 80)

for b in range(2, min(20, N_sample + 1)):
    B_b, C_b, BC_b = per_denominator_BC(N_sample, p_sample, D_vals_s).get(b, (0,0,0))
    orbits = orbit_structure(b, p_sample)
    orbit_lens = [len(o) for o in orbits]
    orbit_contributions = [orbit_BC_contribution(o, b, p_sample, D_vals_s) for o in orbits]
    print(f"{b:>4} {BC_b:>12.4f} {len(orbits):>8} {str(orbit_lens)[:20]:>20} "
          f"{str([f'{x:.3f}' for x in orbit_contributions])[:30]:>30}")

print("\n--- Section 4: What dominates B+C? Top vs bottom denominators ---")
print(f"\nFor each prime p, what fraction of B+C comes from b <= sqrt(p)?")
print(f"\n{'p':>5} {'B+C':>12} {'small_b_BC':>12} {'frac_small':>10} {'large_b_BC':>12}")
print("-" * 60)

for p in primes:
    if p < 11 or p > 100:
        continue
    N = p - 1
    fracs, D_vals, n = build_farey_with_ranks(N)
    denom_BC = per_denominator_BC(N, p, D_vals)
    total_BC = sum(v[2] for v in denom_BC.values())
    sqrt_p = int(p**0.5)
    small_BC = sum(v[2] for b, v in denom_BC.items() if b <= sqrt_p)
    large_BC = sum(v[2] for b, v in denom_BC.items() if b > sqrt_p)
    frac = small_BC / total_BC if total_BC != 0 else float('nan')
    print(f"{p:>5} {total_BC:>12.4f} {small_BC:>12.4f} {frac:>10.4f} {large_BC:>12.4f}")

print("\n--- Section 5: Exact per-orbit quadratic form analysis ---")
print("""
For each orbit O = {a, σ(a), σ²(a), ...} of length L under σ_p acting mod b:

  BC_orbit = Σ_{a in O} [δ(a/b)·(2D(a/b) + δ(a/b))]
           = Σ_{i=0}^{L-1} [(a_i - a_{i+1})/b · (2D(a_i/b) + (a_i - a_{i+1})/b)]

  where a_{i+1} = σ_p(a_i) = p·a_i mod b.

TELESCOPING OBSERVATION:
  Σ_{i=0}^{L-1} (a_i - a_{i+1}) = 0  (orbit sum is 0 mod b)
  Σ_{i=0}^{L-1} (a_i - a_{i+1})^2 = 2 · deficit_orbit_b  (always > 0 for non-identity)

  So: BC_orbit = (2/b) Σ_i (a_i - a_{i+1})·D(a_i/b) + (1/b^2) Σ_i (a_i - a_{i+1})^2

  The SECOND TERM is always positive (= 2·deficit_orbit/b^2 > 0 for non-identity).
  The FIRST TERM can be negative (= B_orbit/b_raw, depends on D correlation).

BOUND:
  BC_orbit ≥ -|first_term| + second_term
           ≥ -2·max|D(a/b)| · (1/b) · Σ|a_i - a_{i+1}| + 2·deficit_orbit/b^2
""")

# Compute orbit decomposition for a specific case
p_orb = 23
N_orb = p_orb - 1
fracs_o, D_vals_o, n_o = build_farey_with_ranks(N_orb)

print(f"Orbit decomposition for p = {p_orb}:")
print(f"\n{'b':>4} {'orbit':>20} {'B_orb_raw':>12} {'C_orb_raw':>12} {'BC_orb':>12} {'defic/b^2':>12}")
print("-" * 80)

for b in range(2, min(15, N_orb + 1)):
    orbits = orbit_structure(b, p_orb)
    for orb in orbits:
        L = len(orb)
        B_orb = 0.0
        C_orb = 0.0
        deficit = 0.0
        for i, a in enumerate(orb):
            sigma_a = (p_orb * a) % b
            delta_a = (a - sigma_a) / b
            D_a = D_vals_o.get((a, b), 0.0)
            B_orb += 2 * D_a * delta_a
            C_orb += delta_a ** 2
            deficit += (a - sigma_a) ** 2 / 2
        deficit_norm = deficit / (b ** 2)
        print(f"{b:>4} {str(orb)[:20]:>20} {B_orb:>12.4f} {C_orb:>12.4f} {B_orb+C_orb:>12.4f} {deficit_norm:>12.4f}")

print("\n--- Section 6: Critical bound — can we prove B_b + C_b >= -C_b? ---")
print("""
B_b + C_b > 0 iff B_b > -C_b iff (2 Σ D·δ) / Σ δ^2 > -1.

For each b, define:
  r_b = (B_b/2) / C_b = Σ D·δ / Σ δ^2   (normalized cross-correlation)

B_b + C_b = C_b · (1 + 2r_b)

So B_b + C_b > 0 iff r_b > -1/2.

By Cauchy-Schwarz: |r_b| ≤ sqrt(Σ D(a/b)^2 / Σ δ(a/b)^2) = sqrt(D_sq_b / C_b)

So r_b > -1/2 is guaranteed if sqrt(D_sq_b / C_b) < 1/2, i.e., D_sq_b < C_b/4.
But this is very restrictive and generally false.

INSTEAD: use the GLOBAL structure. Summing over all b:
  B + C = Σ_b C_b · (1 + 2r_b)

  This is positive if Σ_b C_b · r_b > -Σ_b C_b / 2.

  I.e., the WEIGHTED average of r_b (weighted by C_b) must exceed -1/2.
""")

print("Checking r_b distribution:")
print(f"\n{'p':>5} {'min_rb':>10} {'wt_avg_rb':>12} {'B+C_pos':>8}")
print("-" * 45)

for p in primes:
    if p < 11 or p > 83:
        continue
    N = p - 1
    fracs, D_vals, n = build_farey_with_ranks(N)
    denom_BC = per_denominator_BC(N, p, D_vals)

    r_b_weighted = 0.0
    C_total = 0.0
    min_rb = float('inf')

    for b, (Bb, Cb, BCb) in denom_BC.items():
        if Cb > 1e-12:
            rb = Bb / (2 * Cb)  # r_b = B_b/(2*C_b)
            if rb < min_rb:
                min_rb = rb
            r_b_weighted += Cb * rb
            C_total += Cb

    wt_avg = r_b_weighted / C_total if C_total > 0 else float('nan')
    total_BC = sum(v[2] for v in denom_BC.values())

    print(f"{p:>5} {min_rb:>10.4f} {wt_avg:>12.4f} {total_BC > 0:>8}")

print("\n--- Section 7: B+C as displacement of a quadratic form ---")
print("""
CLEAN FORMULATION:
  B + C = Σ_{b=2}^{N} Σ_{gcd(a,b)=1} [(D(a/b) + δ(a/b))^2 - D(a/b)^2]

This is the net change in Σ D(f)^2 for OLD fractions when going from F_{p-1} to F_p.

The D_{F_p}(a/b) = D_{F_{p-1}}(a/b) + δ(a/b).

KEY INSIGHT TO PROVE: Σ_{old f} D_{F_p}(f)^2 > Σ_{old f} D_{F_{p-1}}(f)^2

EQUIVALENTLY: Does adding p-1 equispaced new fractions k/p INCREASE the L^2
discrepancy of the OLD fractions f in F_{p-1}?

INTUITION: When k/p is inserted between two old fractions f_j and f_{j+1},
the rank of f_{j+1} (and all fractions to the right of k/p) increases by 1.
This pushes D(f_{j+1}) up by 1.

The NET EFFECT over all insertions: each old fraction a/b has its rank
increased by floor(p*a/b). Its ideal position shifts from n*(a/b) to n'*(a/b).
The NET RANK SHIFT = floor(p*a/b) - N*(a/b) = δ_raw(a/b) * b.

If this shift is in the SAME DIRECTION as the current discrepancy, the wobble
increases.
""")

# Check: does D(f) predict the sign of delta(f)?
print("Correlation between sign(D) and sign(delta) for all fractions:")
print(f"\n{'p':>5} {'same_sign%':>12} {'|D>0 and delta>0|':>20} {'D*delta > 0%':>15}")
print("-" * 55)

for p in primes:
    if p < 11 or p > 83:
        continue
    N = p - 1
    fracs, D_vals, n = build_farey_with_ranks(N)

    total = 0
    same_sign = 0
    D_delta_pos = 0

    for (a, b) in fracs:
        if a == 0 or a == b:
            continue
        D = D_vals[(a, b)]
        sigma = (p * a) % b
        delta = (a - sigma) / b
        if abs(delta) < 1e-10:
            continue
        total += 1
        if (D > 0) == (delta > 0):
            same_sign += 1
        if D * delta > 0:
            D_delta_pos += 1

    if total > 0:
        print(f"{p:>5} {100*same_sign/total:>12.1f}% {same_sign:>20} {100*D_delta_pos/total:>15.1f}%")

print("\n--- Section 8: The key quantity Σ D*delta vs total D^2 ---")
print(f"\n{'p':>5} {'B/(2*dsq)':>12} {'C/dsq':>10} {'(B+C)/dsq':>12} note")
print("-" * 50)

for p in primes:
    if p < 11 or p > 83:
        continue
    N = p - 1
    fracs, D_vals, n = build_farey_with_ranks(N)

    old_D_sq = sum(D**2 for D in D_vals.values())
    B = 0.0
    C = 0.0
    for (a, b), D in D_vals.items():
        if a == 0 or a == b:
            continue
        sigma = (p * a) % b
        delta = (a - sigma) / b
        B += 2 * D * delta
        C += delta * delta

    Mval = M[p]
    print(f"{p:>5} {B/(2*old_D_sq):>12.4f} {C/old_D_sq:>10.4f} {(B+C)/old_D_sq:>12.4f} M={Mval}")

print(f"\nTotal time: {time.time()-start_time:.1f}s")
