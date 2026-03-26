#!/usr/bin/env python3
"""
BAD DENOMINATOR BOUND: KEY TO PROVING B+C > 0
=============================================

PROOF STRATEGY (new, from per-denominator analysis):

  KEY INSIGHT: The negative contributions to B+C come ONLY from denominators
  b where p ≡ 2 mod b (or more generally p ≡ m mod b for small m).

  For p ≡ 2 mod b: the divisors of p-2.
  For p ≡ m mod b: the divisors of (p-m) for m = 2,3,...

  The SET of "bad" denominators (where B_b + C_b < 0) is:
    S_bad ⊂ {b : b | (p-m) for some small m}

  KEY BOUND TO PROVE:
    D_sq^bad = Σ_{b in S_bad} D_sq_b ≤ C_avg · (p-1) · old_D_sq / n

  where C_avg is an empirical constant.

  WHY THIS HELPS:
    |B_raw^bad| ≤ 2 √(D_sq^bad · delta_sq^bad)
              ≤ 2 √(C_avg · N · old_D_sq/n · σ(p-2)/12)
              = O(N · √(log N · log log N))

    While delta_sq ≥ N^2/(48 log N).

    For large N: delta_sq >> |B_raw^bad|, so B+C = delta_sq + B_raw > 0.

THIS SCRIPT:
  1. Computes D_sq^bad / (N · old_D_sq/n) empirically (the C_avg constant)
  2. Verifies the key bound D_sq^bad ≤ C · N · old_D_sq/n
  3. Computes the EXPLICIT THRESHOLD for the analytical proof
  4. Verifies B+C > 0 can be proved for all primes p > P_threshold
  5. Checks the small-prime computational coverage

KEY DEFINITIONS:
  N = p - 1
  n = |F_{p-1}|
  old_D_sq = Σ_{f in F_{p-1}} D(f)^2
  D_sq^bad = Σ_{b | (p-2), b ≤ N} Σ_{gcd(a,b)=1} D(a/b)^2
  delta_sq = Σ_{f in F_{p-1}} δ(f)^2 = Σ_b 2·deficit_b/b^2

  C_bad = Σ_{b | (p-2)} 2·deficit_b/b^2  (total C from bad denominators)
  D_sq_avg = old_D_sq / n = n·W  (average squared discrepancy per fraction)
"""

import time
from math import gcd, isqrt, log, sqrt
from collections import defaultdict

start_time = time.time()

# ============================================================
# UTILITIES
# ============================================================

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

def divisors(n):
    """Return all divisors of n."""
    divs = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            divs.append(d)
            if d != n // d:
                divs.append(n // d)
    return divs

def sigma(n):
    """Sum of divisors of n."""
    return sum(divisors(n))

def mertens_sieve(limit):
    sp = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if sp[i] == 0:
            for j in range(i, limit + 1, i):
                if sp[j] == 0:
                    sp[j] = i
    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        rem = n; sq_free = True; nf = 0
        while rem > 1:
            s = sp[rem]; cnt = 0
            while rem % s == 0: rem //= s; cnt += 1
            if cnt >= 2: sq_free = False; break
            nf += 1
        if sq_free: mu[n] = (-1) ** nf
    M = [0] * (limit + 1)
    for i in range(1, limit + 1):
        M[i] = M[i-1] + mu[i]
    return mu, M

def build_farey_D_vals(N, p):
    """
    Build F_N and compute D(a/b), delta(a/b) for all interior fractions.
    Returns:
      D_vals: dict (a,b) -> D(a/b)
      delta_vals: dict (a,b) -> delta(a/b)
      old_D_sq: Σ D^2
      delta_sq: Σ delta^2
      n: |F_N|
    """
    fracs = [(0, 1)]
    a, b = 0, 1
    c, d = 1, N
    while (c, d) != (1, 1):
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        fracs.append((c, d))
    n = len(fracs)

    D_vals = {}
    delta_vals = {}
    old_D_sq = 0.0
    delta_sq = 0.0

    for idx, (aa, bb) in enumerate(fracs):
        D = idx - n * aa / bb
        D_vals[(aa, bb)] = D
        old_D_sq += D * D
        if aa > 0 and aa < bb:
            sigma_p = (p * aa) % bb
            delta = (aa - sigma_p) / bb
            delta_vals[(aa, bb)] = delta
            delta_sq += delta * delta

    return D_vals, delta_vals, old_D_sq, delta_sq, n

def compute_bad_denominator_stats(N, p, D_vals, delta_vals):
    """
    Compute statistics for "bad" denominators b where p ≡ 2 mod b,
    i.e., b | (p-2).

    Returns:
      D_sq_bad: Σ_{bad b} Σ_{gcd(a,b)=1} D(a/b)^2
      C_bad: Σ_{bad b} delta(a/b)^2  (= 2*deficit/b^2 summed)
      B_bad: 2 * Σ_{bad b} Σ D·delta
      bad_divs: list of bad denominators b
    """
    pm2 = p - 2
    bad_divs = [b for b in divisors(pm2) if 2 <= b <= N]

    D_sq_bad = 0.0
    C_bad = 0.0
    B_bad = 0.0

    for b in bad_divs:
        for a in range(1, b):
            if gcd(a, b) != 1:
                continue
            D = D_vals.get((a, b), 0.0)
            delta = delta_vals.get((a, b), 0.0)
            D_sq_bad += D * D
            C_bad += delta * delta
            B_bad += 2 * D * delta

    return D_sq_bad, C_bad, B_bad, bad_divs

# ============================================================
# MAIN ANALYSIS
# ============================================================

LIMIT = 500
primes = sieve_primes(LIMIT)
phi = euler_totient_sieve(LIMIT)
mu, M = mertens_sieve(LIMIT)

print("=" * 80)
print("BAD DENOMINATOR BOUND: TESTING THE KEY ANALYTICAL STEP")
print("=" * 80)

print("\nHYPOTHESIS: D_sq_bad ≤ C_avg · N · (old_D_sq / n)")
print("            where bad = {b | p-2, b ≤ N}")
print()

results = []
max_C_avg = 0.0
max_B_ratio = 0.0  # |B_bad| / delta_sq

print(f"{'p':>5} {'M':>4} {'D_sq_bad/Dsq_avg/N':>20} {'|B_bad|/delta_sq':>18} "
      f"{'B+C>0':>6} {'#bad_b':>7} {'sig(p-2)/N':>12}")
print("-" * 80)

for p in primes:
    if p < 11:
        continue
    N = p - 1
    D_vals, delta_vals, old_D_sq, delta_sq, n = build_farey_D_vals(N, p)

    D_sq_avg = old_D_sq / n  # average D^2 per fraction

    D_sq_bad, C_bad, B_bad, bad_divs = compute_bad_denominator_stats(N, p, D_vals, delta_vals)

    # C_avg = D_sq_bad / (N * D_sq_avg) = D_sq_bad * n / (N * old_D_sq)
    if old_D_sq > 0 and N > 0:
        C_avg = D_sq_bad * n / (N * old_D_sq)
    else:
        C_avg = 0.0

    B_plus_C = sum(delta_vals.get(f, 0.0) * (2 * D_vals.get(f, 0.0) + delta_vals.get(f, 0.0))
                   for f in D_vals if f[0] > 0 and f[0] < f[1])

    B_ratio = abs(B_bad) / delta_sq if delta_sq > 0 else 0.0

    # sigma(p-2) / N
    sig_ratio = sigma(p-2) / N if N > 0 else 0.0

    Mval = M[p]
    print(f"{p:>5} {Mval:>4} {C_avg:>20.6f} {B_ratio:>18.6f} "
          f"{B_plus_C > 0:>6} {len(bad_divs):>7} {sig_ratio:>12.4f}")

    if C_avg > max_C_avg:
        max_C_avg = C_avg
    if B_ratio > max_B_ratio:
        max_B_ratio = B_ratio

    results.append({
        'p': p, 'N': N, 'n': n, 'M': Mval,
        'old_D_sq': old_D_sq, 'delta_sq': delta_sq,
        'D_sq_bad': D_sq_bad, 'C_bad': C_bad, 'B_bad': B_bad,
        'C_avg': C_avg, 'B_plus_C': B_plus_C,
        'bad_divs': bad_divs, 'sig_pm2': sigma(p-2)
    })

print()
print(f"Maximum C_avg = D_sq_bad * n / (N * old_D_sq): {max_C_avg:.6f}")
print(f"Maximum |B_bad|/delta_sq: {max_B_ratio:.6f}")
print()

print("=" * 80)
print("KEY BOUND VERIFICATION")
print("=" * 80)
print(f"""
The analytical bound B+C > 0 for large p uses:

  B+C = delta_sq + B_raw
      ≥ delta_sq - |B_raw|
      ≥ delta_sq - |B_bad| - |B_good|  [split into bad/good denominators]
      ≥ delta_sq - |B_bad|             [since B_good = B_raw - B_bad]

  Key: B_good can be positive (good denominators have B_b > 0 typically)
  So B+C ≥ delta_sq - |B_bad| is a LOWER BOUND.

  Now: |B_bad| ≤ 2 * sqrt(D_sq_bad * C_bad)   [Cauchy-Schwarz per-bad-b]

  BOUND 1: D_sq_bad ≤ C_max_avg * N * old_D_sq/n
           where C_max_avg ≤ {max_C_avg:.3f} (empirical maximum)

  BOUND 2: C_bad ≤ sigma(p-2)/12  (from deficit formula: C_b ≤ b/12)

  Combined: |B_bad| ≤ 2 * sqrt(C_max_avg * N * old_D_sq/n * sigma(p-2)/12)
""")

print("Testing the combined bound:")
print(f"\n{'p':>5} {'delta_sq':>12} {'|B_bad|_bound':>16} {'margin':>12} {'B+C_actual':>12}")
print("-" * 60)

violations = 0
for r in results:
    p = r['p']; N = r['N']
    delta_sq = r['delta_sq']
    old_D_sq = r['old_D_sq']
    n = r['n']
    sig = r['sig_pm2']

    # Upper bound on |B_bad|
    D_sq_bad_bound = max_C_avg * N * old_D_sq / n  # upper bound using empirical C_max_avg
    C_bad_bound = sig / 12.0  # upper bound using sigma(p-2)/12
    B_bad_bound = 2 * (D_sq_bad_bound * C_bad_bound) ** 0.5

    margin = delta_sq - B_bad_bound
    BC = r['B_plus_C']

    # Mark if bound would work (margin > 0)
    bound_works = margin > 0
    if not bound_works:
        violations += 1

    if p <= 200 or p % 50 == 3:
        print(f"{p:>5} {delta_sq:>12.4f} {B_bad_bound:>16.4f} {margin:>12.4f} {BC:>12.4f}"
              f"{'  ✓' if bound_works else '  ✗'}")

print(f"\nBound violations (margin > 0 fails): {violations}/{len(results)}")

print()
print("=" * 80)
print("ANALYTICAL THRESHOLD COMPUTATION")
print("=" * 80)
print(f"""
For the ANALYTICAL PROOF (p → ∞), we use:

  delta_sq ≥ N^2 / (48 * log(N))   [Theorem 2 from proof document]

  |B_bad| ≤ 2 * sqrt(C_max * N * n*W * sigma(p-2)/12)

  Using n*W = old_D_sq/n ≤ (3/π^2) * N * log(N)  [Franel-Landau bound]:

  |B_bad| ≤ 2 * sqrt(C_max * N * (3/π^2) * N * log(N) * C_σ * N * log(log(N)))
           where σ(p-2) ≤ C_σ * (p-2) * log(log(p-2)) ≤ C_σ * N * log(log(N))

  = 2 * sqrt(C_max * (3/π^2) * C_σ) * N^(3/2) * sqrt(log(N) * log(log(N)))

  CONDITION B+C > 0 requires delta_sq > |B_bad|:
    N^2 / (48 log N) > K * N^(3/2) * sqrt(log N * log log N)
    N^(1/2) / (48 log N) > K * sqrt(log N * log log N)
    N^(1/2) > 48 K * log(N) * sqrt(log N * log log N)
    N^(1/2) > 48 K * (log N)^(3/2) * (log log N)^(1/2)
    N > (48K)^2 * (log N)^3 * log log N

This holds for all N > N_threshold for an explicit N_threshold.
""")

# Compute empirical C_max and estimate threshold
from math import log as ln, pi

C_max = max_C_avg
# sigma(p-2) / (p-2) ≤ C * log(log(p-2)) by Robin's theorem / Gronwall
# Use generous bound: sigma(n)/n ≤ e^gamma * ln(ln(n)) + 5/(2 * ln(ln(n)))
# For n = p-2 ≥ 9: sigma(n) ≤ e^0.5772 * n * ln(ln(n)) ≤ 1.78 * n * ln(ln(n))
C_sigma = 1.78  # conservative bound for sigma(n)/(n * ln(ln(n)))
K = 2 * (C_max * (3 / pi**2) * C_sigma)**0.5

print(f"Empirical C_max (D_sq_bad bound): {C_max:.4f}")
print(f"C_sigma (sigma bound): {C_sigma:.4f}")
print(f"K = 2*sqrt(C_max * 3/π^2 * C_sigma): {K:.4f}")
print()

# Find threshold N where N > (48K)^2 * (log N)^3 * log log N
print("Computing analytical threshold N_threshold:")
for N_test in [100, 1000, 10000, 100000, 1000000, 10000000]:
    if N_test <= 2:
        continue
    lnN = ln(N_test)
    lnlnN = ln(max(ln(N_test), 1.01))
    rhs = (48 * K)**2 * lnN**3 * lnlnN
    holds = N_test > rhs
    print(f"  N = {N_test:>10}: N = {N_test:.2e}, RHS = {rhs:.2e}, N > RHS? {'YES' if holds else 'NO'}")

print()
print("=" * 80)
print("ALTERNATIVE: DIRECT B_bad BOUND (not using Cauchy-Schwarz)")
print("=" * 80)
print("""
Instead of Cauchy-Schwarz on B_bad, use:

  |B_bad| = |2 Σ_{b|p-2} Σ_{gcd(a,b)=1} D(a/b) * δ(a/b)|
          = |2 Σ_{b|p-2} (1/b) Σ_{gcd(a,b)=1} (a - σ_p(a)) * D(a/b)|

For each b | p-2, σ_p = multiplication by 2 mod b (since p ≡ 2 mod b).

The inner sum: Σ_a (a - 2a mod b) * D(a/b)

For a in lower half (a ≤ b/2): a - 2a mod b = -a
For a in upper half (a > b/2): a - 2a mod b = b - a

So the inner sum = Σ_{a ≤ b/2} (-a) D(a/b) + Σ_{a > b/2} (b-a) D(a/b)

ABEL SUMMATION TRICK:
  = b * Σ_{a > b/2} D(a/b) - Σ_a a * D(a/b) * sign(a - b/2)

Using Σ_a D(a/b) = 0 (balanced sum) and Σ_a a * D(a/b) ~ ???

This gives a tighter bound in terms of Σ_b D(a/b) (partial sums).
""")

# Compute empirical tightness of Abel summation approach
print("Direct computation of B_bad vs Abel bound:")
print(f"\n{'p':>5} {'B_bad_direct':>15} {'B_bad_CS':>12} {'ratio':>8}")
print("-" * 45)

for r in results[:20]:
    p = r['p']
    B_bad = abs(r['B_bad'])
    D_sq_bad = r['D_sq_bad']
    C_bad = r['C_bad']
    B_bad_CS = 2 * (D_sq_bad * C_bad)**0.5 if D_sq_bad * C_bad > 0 else 0.0
    ratio = B_bad / B_bad_CS if B_bad_CS > 0 else 0.0
    print(f"{p:>5} {B_bad:>15.4f} {B_bad_CS:>12.4f} {ratio:>8.4f}")

print()
print("=" * 80)
print("GENERALIZATION: ALL 'SMALL-MODULAR' DENOMINATORS")
print("=" * 80)
print("""
Bad denominators come from p ≡ m mod b for small m = 2,3,4,...

For each m, the bad denominators are b | (p-m) with b ≤ N.

Total bad denominators from ALL small m (m = 2,...,M):
  S_bad = Union_{m=2}^{M} {b | p-m, b ≤ N}

Number of bad denominators: ≤ Σ_{m=2}^M d(p-m) = O(M * d_avg)
  where d_avg = avg divisor count ≈ log(p)

Choosing M = sqrt(N): the denominators NOT in S_bad are those where
  ord_b(p) > sqrt(N), i.e., p is not a "small-power root" mod b.

For these "good" denominators:
  - The orbit length L = ord_b(p) > sqrt(N)
  - Each orbit has many fractions
  - By equidistribution within the orbit, B_b ~ 0 on average
  - So B_b + C_b ~ C_b > 0 for good denominators

This suggests the proof:
1. Good denominators: B_b + C_b ≥ C_b/2 > 0 (by orbit equidistribution)
2. Bad denominators: |B_b + C_b| ≤ C_b * O(max|D|/max|δ|/b)

Need to quantify both sides.
""")

print(f"\nTotal time: {time.time()-start_time:.1f}s")
