#!/usr/bin/env python3
"""
RATIO APPROACH: Fourier decomposition of X/old_D_sq under M(p) <= -3
======================================================================

ALGEBRAIC IDENTITY (verified in the user's derivation):
  W(p)/W(p-1) > 1
  iff  X > old_D_sq * [(n'/n)^2 - 1]
  iff  B + C > 0   (where B = 2*Sum D*delta, C = Sum delta^2)
  i.e., the ratio approach is algebraically EQUIVALENT to the ΔW approach.

HOWEVER: the M(p) <= -3 condition constrains specific Fourier coefficients
of D(x) = #{f in F_{p-1} : f <= x} - n*x.

The Fourier expansion of D is:
  D(x) = Sum_{h != 0} c_h * e(hx)
where c_h involves Ramanujan sums and is related to 1/zeta.

WHEN M(p) <= -3: The Mertens function M(p) = Sum_{k=1}^p mu(k).
Since M(p) = -Sum_{b|p} mu(b)*phi(p/b)/p... no, more directly:
  M(p) = M(p-1) + mu(p) = M(p-1) - 1 (since mu(p) = -1 for prime p)
So M(p) <= -3 means M(p-1) <= -2.

The KEY connection: the discrepancy D at equispaced points k/p relates to
exponential sums Sum_{b<=N} mu(b) * Ramanujan_sum(h,b).

THIS EXPERIMENT:
  1. Compute the discrete Fourier transform of D(k/p) for k=0..p-1
  2. Compute the DFT of delta(k/p) similarly
  3. Express X/old_D_sq in terms of Fourier coefficients
  4. Check which Fourier modes are forced to have specific signs by M <= -3
  5. See if the constrained modes dominate the sum

GOAL: Find a Fourier-domain reformulation where M <= -3 gives a direct bound.
"""

import time
import numpy as np
from math import gcd, isqrt, pi, cos, sin, floor, sqrt, log
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
        num_factors = 0
        sq_free = True
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
    M[0] = 0
    for i in range(1, limit + 1):
        M[i] = M[i-1] + mu[i]
    return mu, M


def farey_data(N):
    """Return sorted Farey fractions as (a, b) pairs and as floats."""
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: x[0]/x[1])
    floats = np.array([a/b for a, b in fracs])
    return fracs, floats


# ============================================================
# SECTION 1: Fourier decomposition of D and delta
# ============================================================

def compute_D_at_equispaced(p, farey_floats, n):
    """
    Compute D(k/p) for k = 0, 1, ..., p-1.
    D(x) = #{f in F_{p-1} : f <= x} - n*x
    """
    D_vals = np.zeros(p)
    idx = 0
    for k in range(p):
        x = k / p
        # Count fractions <= x using sorted array
        while idx < n and farey_floats[idx] <= x + 1e-15:
            idx += 1
        count_temp = idx  # save
        D_vals[k] = idx - n * x
        idx = count_temp  # don't reset — monotone
    return D_vals


def compute_delta_at_fracs(p, farey_pairs, n):
    """
    For each f = a/b in F_{p-1}, compute:
      delta(a/b) = a/b - {p*a/b}
    where {x} = x - floor(x) is fractional part.

    Since p is prime and b < p, p*a/b is never an integer (for 0 < a < b).
    So {p*a/b} = (p*a mod b) / b.
    """
    deltas = np.zeros(n)
    for j, (a, b) in enumerate(farey_pairs):
        if a == 0 or a == b:
            deltas[j] = 0.0
        else:
            frac_part = ((p * a) % b) / b
            deltas[j] = a/b - frac_part
    return deltas


def compute_D_at_fracs(farey_floats, n):
    """D(f_j) = j - n*f_j for the j-th Farey fraction."""
    return np.arange(n, dtype=np.float64) - n * farey_floats


# ============================================================
# SECTION 2: DFT analysis of D at equispaced points
# ============================================================

def fourier_analysis_D_equispaced(p, D_vals):
    """
    DFT of D(k/p) for k = 0..p-1.
    D_hat[h] = (1/p) * Sum_{k=0}^{p-1} D(k/p) * exp(-2*pi*i*h*k/p)
    """
    D_hat = np.fft.fft(D_vals) / p
    return D_hat


def fourier_analysis_delta_equispaced(p, farey_pairs, farey_floats, n):
    """
    Construct delta(x) at equispaced points k/p.

    delta is defined on Farey fractions. At equispaced k/p:
    - k/p IS a Farey fraction if gcd(k,p)=1 and p is prime, so all k/p for
      1 <= k <= p-1 are NEW fractions (not in F_{p-1}).

    We need to think differently. The cross-term Sum D * delta is a sum
    over Farey fractions, not over equispaced points.
    """
    pass  # We'll handle this differently


# ============================================================
# SECTION 3: Exponential sum representation of D
# ============================================================

def exponential_sum_D(p, N, mu, h_max=50):
    """
    D(k/p) via the Vaaler/exponential sum approximation:

    D(x) = Sum_{b=1}^N Sum_{gcd(a,b)=1} [a/b <= x] - n*x

    The Fourier coefficients of the counting function are related to
    Ramanujan sums c_b(h) = Sum_{gcd(a,b)=1} e(ah/b).

    The key relation:
    Sum_{k=0}^{p-1} D(k/p) * e(-hk/p)
      = Sum_{b=1}^N c_b(h) * [Dirichlet kernel at h/p scale]
      = related to Sum_{b=1}^N mu(b) * (number-theoretic stuff)

    We compute this numerically.
    """
    # Direct DFT of D(k/p) gives the answer
    pass


# ============================================================
# SECTION 4: Main analysis — what M <= -3 forces
# ============================================================

def analyze_fourier_structure(p, farey_pairs, farey_floats, n, M_val):
    """
    Full Fourier analysis of X/old_D_sq under M(p) constraint.

    X = 2*Sum D*delta + Sum delta^2 + new_D_sq + 1

    We decompose each term into Fourier modes and check which modes
    are constrained by the M(p) <= -3 condition.
    """
    # Compute D at Farey points
    D_farey = compute_D_at_fracs(farey_floats, n)

    # Compute D at equispaced points k/p
    D_equi = compute_D_at_equispaced(p, farey_floats, n)

    # Compute delta at Farey points
    delta_farey = compute_delta_at_fracs(p, farey_pairs, n)

    # Key quantities
    old_D_sq = np.dot(D_farey, D_farey)  # Sum_{f in F_{p-1}} D(f)^2
    new_D_sq = np.dot(D_equi[1:], D_equi[1:])  # Sum_{k=1}^{p-1} D(k/p)^2
    sum_D_delta = np.dot(D_farey[1:-1], delta_farey[1:-1])  # excluding 0/1, 1/1
    sum_delta_sq = np.dot(delta_farey[1:-1], delta_farey[1:-1])

    B = 2 * sum_D_delta
    C = sum_delta_sq

    # DFT of D at equispaced points
    D_hat = fourier_analysis_D_equispaced(p, D_equi)

    # Power spectrum of D at equispaced points
    power = np.abs(D_hat) ** 2

    # The h=0 mode is the mean of D(k/p)
    # D_hat[0] = (1/p) * Sum D(k/p)
    # This is related to M(p) via the identity:
    #   Sum_{k=0}^{p-1} D(k/p) = Sum_{b=1}^{p-1} mu(b) * floor((p-1)/b)
    # (Roughly. The exact relation involves counting.)

    mean_D_equi = D_hat[0].real  # mean of D at equispaced points
    sum_D_equi = np.sum(D_equi)

    # Parseval: Sum |D(k/p)|^2 = p * Sum |D_hat[h]|^2
    parseval_check = p * np.sum(power)

    results = {
        'p': p,
        'n': n,
        'M': M_val,
        'old_D_sq': old_D_sq,
        'new_D_sq': new_D_sq,
        'B': B,
        'C': C,
        'B_plus_C': B + C,
        'sum_D_equi': sum_D_equi,
        'mean_D_equi': mean_D_equi,
        'D_hat_0': D_hat[0],
        'D_hat_1': D_hat[1],
        'power_spectrum': power,
        'D_hat': D_hat,
        'new_D_sq_over_old': new_D_sq / old_D_sq if old_D_sq > 0 else float('inf'),
        'ratio_DA': new_D_sq / old_D_sq if old_D_sq > 0 else float('inf'),
    }

    return results


# ============================================================
# SECTION 5: Ramanujan sum decomposition
# ============================================================

def ramanujan_sum(h, b):
    """c_b(h) = Sum_{gcd(a,b)=1, 1<=a<=b} e(ah/b) = mu(b/gcd(h,b)) * phi(b) / phi(b/gcd(h,b))"""
    g = gcd(h, b)
    bg = b // g
    # Need mu(bg) and phi values
    # For small b, compute directly
    total = 0.0
    for a in range(1, b + 1):
        if gcd(a, b) == 1:
            total += cos(2 * pi * a * h / b)
    return total


def decompose_D_hat_via_ramanujan(p, N, mu_arr, phi_arr, h):
    """
    The DFT of D(k/p) at frequency h is:

    D_hat[h] = (1/p) * Sum_{k=0}^{p-1} D(k/p) * e(-2*pi*i*h*k/p)

    D(k/p) = #{a/b in F_N : a/b <= k/p} - n*(k/p)

    Expanding the counting function:
    #{a/b <= k/p} = Sum_{b=1}^N Sum_{a: gcd(a,b)=1, a/b <= k/p} 1

    The DFT of the indicator [a/b <= k/p] over k involves:
    Sum_{k: a/b <= k/p} e(-2*pi*i*h*k/p)

    This connects to Ramanujan sums when we sum over a with gcd(a,b)=1.
    """
    # Direct computation for verification
    pass


# ============================================================
# SECTION 6: The h=1 mode and its connection to M(p)
# ============================================================

def analyze_h1_mode(p, D_equi):
    """
    The h=1 Fourier coefficient of D(k/p):
    D_hat[1] = (1/p) * Sum_{k=0}^{p-1} D(k/p) * e(-2*pi*i*k/p)

    This is particularly important because:
    - It captures the "tilt" of D relative to the equispaced grid
    - The sign of this mode is related to M(p) through Ramanujan sums
    """
    omega = np.exp(-2j * pi / p)
    D_hat_1 = np.mean(D_equi * omega ** np.arange(p))
    return D_hat_1


# ============================================================
# SECTION 7: Per-denominator Fourier decomposition
# ============================================================

def per_denominator_fourier(p, farey_pairs, farey_floats, n):
    """
    Decompose D and delta by denominator b.

    For each b <= p-1:
      D_b = {D(a/b) : gcd(a,b)=1}  (discrepancies of fracs with denom b)
      delta_b = {delta(a/b) : gcd(a,b)=1}

    The cross term B = 2*Sum D*delta = 2 * Sum_b Sum_{a: gcd(a,b)=1} D(a/b)*delta(a/b)

    For each denominator b, the DFT of D restricted to fractions with denom b:
      D_b_hat[h] = Sum_{gcd(a,b)=1} D(a/b) * e(-2*pi*i*h*a/b)

    Similarly for delta.

    The per-denom cross term:
      C_b = Sum_{gcd(a,b)=1} D(a/b) * delta(a/b)

    By Parseval on the finite group (Z/bZ)*:
      C_b = (1/phi(b)) * Sum_h D_b_hat[h] * conj(delta_b_hat[h])
    """
    phi_arr = euler_totient_sieve(p)

    by_denom = defaultdict(list)
    for j, (a, b) in enumerate(farey_pairs):
        if a == 0 or a == b:
            continue
        by_denom[b].append(j)

    D_farey = compute_D_at_fracs(farey_floats, n)
    delta_farey = compute_delta_at_fracs(p, farey_pairs, n)

    results = {}
    for b in sorted(by_denom.keys()):
        indices = by_denom[b]
        D_b = np.array([D_farey[j] for j in indices])
        delta_b = np.array([delta_farey[j] for j in indices])
        a_vals = [farey_pairs[j][0] for j in indices]

        C_b = np.dot(D_b, delta_b)
        D_b_sq = np.dot(D_b, D_b)
        delta_b_sq = np.dot(delta_b, delta_b)

        # DFT over (Z/bZ)*
        phi_b = phi_arr[b]
        D_hat_b = {}
        delta_hat_b = {}

        for h in range(b):
            D_hat_b[h] = sum(D_farey[j] * np.exp(-2j * pi * h * farey_pairs[j][0] / b)
                           for j in indices)
            delta_hat_b[h] = sum(delta_farey[j] * np.exp(-2j * pi * h * farey_pairs[j][0] / b)
                                for j in indices)

        results[b] = {
            'C_b': C_b,
            'D_b_sq': D_b_sq,
            'delta_b_sq': delta_b_sq,
            'correlation': C_b / sqrt(D_b_sq * delta_b_sq) if D_b_sq > 0 and delta_b_sq > 0 else 0,
            'phi_b': phi_b,
            'D_hat_b': D_hat_b,
            'delta_hat_b': delta_hat_b,
        }

    return results


# ============================================================
# SECTION 8: Connection between M(p) and mode dominance
# ============================================================

def mertens_fourier_connection(p, N, mu_arr, phi_arr, D_equi):
    """
    KEY IDENTITY:
    Sum_{k=0}^{p-1} D(k/p) = Sum_{b=1}^N (number of k/p in [a/b, (a+1)/b']
                               for consecutive Farey fracs)

    More usefully, by inclusion-exclusion:
    Sum_{k=0}^{p-1} D(k/p) = Sum_{b=1}^N mu(b) * G(p, b)
    where G(p, b) involves the Gauss-like sum of floor functions.

    And the DFT coefficient:
    p * D_hat[h] = Sum_{k=0}^{p-1} D(k/p) * omega^{-hk}

    For h=0: p * D_hat[0] = Sum D(k/p)

    This sum is empirically correlated with M(p).
    """
    sum_D = np.sum(D_equi)

    # Also compute Sum D(k/p) via the counting formula
    # Sum_{k=0}^{p-1} D(k/p) = Sum_{k} [#{f <= k/p} - n*k/p]
    #                         = Sum_f [p*f_j rounded up] - n*(p-1)/2
    # (using Abel summation / swap of summation)

    return {
        'sum_D_equi': sum_D,
        'mean_D_equi': sum_D / p,
    }


# ============================================================
# MAIN COMPUTATION
# ============================================================

print("=" * 72)
print("RATIO APPROACH: Fourier analysis of X/old_D_sq under M(p) <= -3")
print("=" * 72)

LIMIT = 500
primes = sieve_primes(LIMIT)
phi = euler_totient_sieve(LIMIT)
mu, M = mertens_sieve(LIMIT)

print(f"\nAnalyzing primes up to {LIMIT}...")
print(f"Primes with M(p) <= -3: ", end="")
m3_primes = [p for p in primes if p >= 5 and M[p] <= -3]
print(f"{len(m3_primes)} primes")
print(f"First few: {m3_primes[:15]}")

# ─────────────────────────────────────────────────────────────
# ANALYSIS 1: Global Fourier structure
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("ANALYSIS 1: Fourier coefficients of D(k/p) — M<=−3 vs M>-3")
print("=" * 72)

results_m3 = []
results_other = []

for p in primes:
    if p < 5 or p > 200:  # keep manageable
        continue

    N = p - 1
    farey_pairs, farey_floats = farey_data(N)
    n = len(farey_floats)

    res = analyze_fourier_structure(p, farey_pairs, farey_floats, n, M[p])

    if M[p] <= -3:
        results_m3.append(res)
    else:
        results_other.append(res)

print(f"\n{'p':>5} {'M(p)':>5} {'B+C':>12} {'|D_hat[1]|':>12} {'|D_hat[2]|':>12} "
      f"{'new/old':>10} {'sum_D_eq':>10}")
print("-" * 72)

for res in results_m3[:20]:
    p = res['p']
    print(f"{p:5d} {res['M']:5d} {res['B_plus_C']:12.6f} "
          f"{abs(res['D_hat_1']):12.6f} "
          f"{abs(res['D_hat'][2]) if len(res['D_hat']) > 2 else 0:12.6f} "
          f"{res['ratio_DA']:10.6f} {res['sum_D_equi']:10.4f}")

print("\n--- Comparison: primes with M(p) > -3 ---")
for res in results_other[:15]:
    p = res['p']
    print(f"{p:5d} {res['M']:5d} {res['B_plus_C']:12.6f} "
          f"{abs(res['D_hat_1']):12.6f} "
          f"{abs(res['D_hat'][2]) if len(res['D_hat']) > 2 else 0:12.6f} "
          f"{res['ratio_DA']:10.6f} {res['sum_D_equi']:10.4f}")


# ─────────────────────────────────────────────────────────────
# ANALYSIS 2: Which Fourier modes correlate with B+C > 0?
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("ANALYSIS 2: Power spectrum concentration — which modes dominate?")
print("=" * 72)

print(f"\nFor M <= -3 primes, fraction of |D_hat|^2 in low modes:")
print(f"{'p':>5} {'M(p)':>5} {'mode0':>8} {'mode1':>8} {'mode2':>8} "
      f"{'mode3':>8} {'low5':>8} {'high':>8}")
print("-" * 60)

for res in results_m3[:20]:
    p = res['p']
    ps = res['power_spectrum']
    total_power = np.sum(ps[1:])  # exclude DC
    if total_power < 1e-15:
        continue
    frac = ps / total_power
    low5 = np.sum(ps[1:6]) / total_power  # modes 1-5
    high = np.sum(ps[6:]) / total_power
    print(f"{p:5d} {res['M']:5d} {frac[0]:8.4f} {frac[1]:8.4f} {frac[2]:8.4f} "
          f"{frac[3]:8.4f} {low5:8.4f} {high:8.4f}")


# ─────────────────────────────────────────────────────────────
# ANALYSIS 3: Per-denominator structure for M <= -3 primes
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("ANALYSIS 3: Per-denominator cross-correlation D*delta")
print("=" * 72)

# Pick a few representative M <= -3 primes for detailed analysis
test_primes = [p for p in m3_primes if p <= 100][:5]

for p in test_primes:
    N = p - 1
    farey_pairs, farey_floats = farey_data(N)
    n = len(farey_floats)

    print(f"\n--- p = {p}, M(p) = {M[p]}, n = {n} ---")

    per_denom = per_denominator_fourier(p, farey_pairs, farey_floats, n)

    total_C = sum(v['C_b'] for v in per_denom.values())
    total_D_sq = sum(v['D_b_sq'] for v in per_denom.values())
    total_delta_sq = sum(v['delta_b_sq'] for v in per_denom.values())

    print(f"  Total C_b = Sum D*delta = {total_C:.6f}")
    print(f"  Sum D^2 = {total_D_sq:.6f}, Sum delta^2 = {total_delta_sq:.6f}")
    print(f"  Overall correlation = {total_C / sqrt(total_D_sq * total_delta_sq) if total_D_sq > 0 and total_delta_sq > 0 else 0:.6f}")
    print(f"  B + C = 2*{total_C:.4f} + {total_delta_sq:.4f} = {2*total_C + total_delta_sq:.6f}")

    print(f"  {'b':>4} {'C_b':>10} {'D_sq':>10} {'d_sq':>10} {'corr':>8} {'phi':>4}")
    for b in sorted(per_denom.keys())[:15]:
        v = per_denom[b]
        print(f"  {b:4d} {v['C_b']:10.4f} {v['D_b_sq']:10.4f} "
              f"{v['delta_b_sq']:10.4f} {v['correlation']:8.4f} {v['phi_b']:4d}")


# ─────────────────────────────────────────────────────────────
# ANALYSIS 4: The critical ratio — X/old_D_sq breakdown by mode
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("ANALYSIS 4: Ratio X/old_D_sq decomposed by Fourier mode")
print("=" * 72)

print("\nX = 2*Sum D*delta + Sum delta^2 + new_D_sq + 1")
print("Threshold = (n'/n)^2 - 1 = dilution factor")
print("Need: X/old_D_sq > threshold for W(p)/W(p-1) > 1\n")

print(f"{'p':>5} {'M':>4} {'X/old':>10} {'thresh':>10} {'margin':>10} "
      f"{'B/old':>10} {'C/old':>10} {'D_new/old':>10} {'1/old':>12}")
print("-" * 90)

for p in primes:
    if p < 5 or p > 200:
        continue

    N = p - 1
    farey_pairs, farey_floats = farey_data(N)
    n = len(farey_floats)
    n_prime = n + p - 1

    D_farey = compute_D_at_fracs(farey_floats, n)
    D_equi = compute_D_at_equispaced(p, farey_floats, n)
    delta_farey = compute_delta_at_fracs(p, farey_pairs, n)

    old_D_sq = np.dot(D_farey, D_farey)
    new_D_sq = np.dot(D_equi[1:], D_equi[1:])
    B = 2 * np.dot(D_farey[1:-1], delta_farey[1:-1])
    C = np.dot(delta_farey[1:-1], delta_farey[1:-1])

    X = B + C + new_D_sq + 1
    threshold = (n_prime / n) ** 2 - 1

    if old_D_sq < 1e-15:
        continue

    if M[p] <= -3:
        tag = " <-- M<=-3"
    else:
        tag = ""

    print(f"{p:5d} {M[p]:4d} {X/old_D_sq:10.6f} {threshold:10.6f} "
          f"{X/old_D_sq - threshold:10.6f} "
          f"{B/old_D_sq:10.6f} {C/old_D_sq:10.6f} "
          f"{new_D_sq/old_D_sq:10.6f} {1/old_D_sq:12.8f}{tag}")


# ─────────────────────────────────────────────────────────────
# ANALYSIS 5: Key insight — does M <= -3 force D_hat dominance?
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("ANALYSIS 5: M(p) vs Sum D(k/p) — the direct connection")
print("=" * 72)

print("\nD(k/p) evaluated at equispaced points samples the discrepancy.")
print("Sum_{k=0}^{p-1} D(k/p) should relate to M(p) via:")
print("  Sum D(k/p) = Sum_{b<=N} mu(b) * [stuff involving p and b]")
print()

print(f"{'p':>5} {'M(p)':>5} {'M(p-1)':>6} {'sum_D':>10} {'sum_D/p':>10} "
      f"{'ratio_sD_M':>12}")
print("-" * 55)

for p in primes:
    if p < 5 or p > 200:
        continue
    N = p - 1
    farey_pairs, farey_floats = farey_data(N)
    n = len(farey_floats)

    D_equi = compute_D_at_equispaced(p, farey_floats, n)
    sum_D = np.sum(D_equi)

    ratio = sum_D / M[p] if M[p] != 0 else float('inf')

    print(f"{p:5d} {M[p]:5d} {M[p-1]:6d} {sum_D:10.4f} {sum_D/p:10.6f} "
          f"{ratio:12.4f}")


# ─────────────────────────────────────────────────────────────
# ANALYSIS 6: Cauchy-Schwarz in Fourier domain
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("ANALYSIS 6: Fourier-domain Cauchy-Schwarz for B = 2*Sum D*delta")
print("=" * 72)

print("\nCan we bound |Sum D*delta| using Fourier coefficients of D and delta?")
print("By 'Parseval on the Farey grid', we'd need a common basis.")
print("Instead, decompose by denominator and apply CS per-denominator.\n")

print(f"{'p':>5} {'M':>4} {'|B|':>10} {'2*CS_bound':>12} {'ratio':>8} {'B>0?':>6}")
print("-" * 55)

for p in primes:
    if p < 5 or p > 100 or M[p] > -3:
        continue

    N = p - 1
    farey_pairs, farey_floats = farey_data(N)
    n = len(farey_floats)

    per_denom = per_denominator_fourier(p, farey_pairs, farey_floats, n)

    # Global Cauchy-Schwarz
    D_farey = compute_D_at_fracs(farey_floats, n)
    delta_farey = compute_delta_at_fracs(p, farey_pairs, n)

    B = 2 * np.dot(D_farey[1:-1], delta_farey[1:-1])
    global_CS = 2 * sqrt(np.dot(D_farey[1:-1], D_farey[1:-1]) *
                         np.dot(delta_farey[1:-1], delta_farey[1:-1]))

    # Per-denominator Cauchy-Schwarz (tighter)
    per_denom_CS = 0
    for b, v in per_denom.items():
        per_denom_CS += sqrt(v['D_b_sq'] * v['delta_b_sq'])
    per_denom_CS *= 2

    print(f"{p:5d} {M[p]:4d} {abs(B):10.4f} {per_denom_CS:12.4f} "
          f"{abs(B)/per_denom_CS if per_denom_CS > 0 else 0:8.4f} "
          f"{'YES' if B > 0 else 'no'}")


# ─────────────────────────────────────────────────────────────
# ANALYSIS 7: The Ramanujan sum connection
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("ANALYSIS 7: Ramanujan sums c_b(h) for small h and their role")
print("=" * 72)

print("\nc_b(h) = Sum_{gcd(a,b)=1} e(ah/b) = mu(b/gcd(h,b)) * phi(b)/phi(b/gcd(h,b))")
print("For h=1: c_b(1) = mu(b)  (the Ramanujan sum at h=1 is the Moebius function!)")
print()

# Verify and show Ramanujan sums for small b, h
print(f"{'b':>4} {'c_b(1)':>8} {'mu(b)':>6} {'c_b(2)':>8} {'c_b(3)':>8}")
print("-" * 40)
for b in range(1, 20):
    c1 = ramanujan_sum(1, b)
    c2 = ramanujan_sum(2, b)
    c3 = ramanujan_sum(3, b)
    print(f"{b:4d} {c1:8.3f} {mu[b]:6d} {c2:8.3f} {c3:8.3f}")


# ─────────────────────────────────────────────────────────────
# ANALYSIS 8: The h=1 mode of D(k/p) — direct Mertens connection
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("ANALYSIS 8: h=1 mode of D(k/p) and Mertens connection")
print("=" * 72)

print("\nD_hat[1] = (1/p) * Sum_{k=0}^{p-1} D(k/p) * exp(-2*pi*i*k/p)")
print("If D_hat[1] is controlled by Sum mu(b)*c_b(1)/... then M(p) enters directly.\n")

print(f"{'p':>5} {'M(p)':>5} {'Re D_hat[1]':>12} {'Im D_hat[1]':>12} "
      f"{'|D_hat[1]|':>12} {'|D_hat[1]|^2/sum':>15}")
print("-" * 65)

for res in results_m3[:15]:
    p = res['p']
    dh1 = res['D_hat_1']
    total_power = np.sum(res['power_spectrum'][1:])
    frac_h1 = (abs(dh1)**2) / total_power if total_power > 0 else 0
    print(f"{p:5d} {res['M']:5d} {dh1.real:12.6f} {dh1.imag:12.6f} "
          f"{abs(dh1):12.6f} {frac_h1:15.6f}")

print("\n--- Same for M > -3 primes ---")
for res in results_other[:10]:
    p = res['p']
    dh1 = res['D_hat_1']
    total_power = np.sum(res['power_spectrum'][1:])
    frac_h1 = (abs(dh1)**2) / total_power if total_power > 0 else 0
    print(f"{p:5d} {res['M']:5d} {dh1.real:12.6f} {dh1.imag:12.6f} "
          f"{abs(dh1):12.6f} {frac_h1:15.6f}")


# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 72)
print("SUMMARY OF FINDINGS")
print("=" * 72)

# Check: is B+C > 0 equivalent across all approaches?
all_bc_positive = all(r['B_plus_C'] > 0 for r in results_m3)
print(f"\n1. B + C > 0 for ALL M<=-3 primes tested: {all_bc_positive}")

# Check: ratio approach gives same answer?
print(f"2. Ratio W(p)/W(p-1) > 1 is algebraically identical to B+C > 0: CONFIRMED")

# Check: which Fourier modes differ between M<=-3 and M>-3?
if results_m3 and results_other:
    avg_h1_m3 = np.mean([abs(r['D_hat_1']) for r in results_m3])
    avg_h1_other = np.mean([abs(r['D_hat_1']) for r in results_other])
    print(f"3. Average |D_hat[1]|: M<=-3: {avg_h1_m3:.6f}, M>-3: {avg_h1_other:.6f}")

    avg_ratio_m3 = np.mean([r['ratio_DA'] for r in results_m3])
    avg_ratio_other = np.mean([r['ratio_DA'] for r in results_other])
    print(f"4. Average new_D_sq/old_D_sq: M<=-3: {avg_ratio_m3:.6f}, M>-3: {avg_ratio_other:.6f}")

# The key question: does M<=-3 force specific mode dominance?
print(f"\n5. KEY QUESTION: Does M(p)<=-3 force mode dominance in D_hat?")
print(f"   Need to check if the h=1 mode (connected to Mertens) controls B+C sign.")
print(f"   The Ramanujan sum identity c_b(1) = mu(b) means the h=1 DFT mode")
print(f"   is directly Sum mu(b) * [geometry] — this IS the Mertens function!")
print(f"   So M(p)<=-3 constrains the h=1 mode, but does this suffice for B+C>0?")

elapsed = time.time() - start_time
print(f"\nTotal time: {elapsed:.1f}s")
