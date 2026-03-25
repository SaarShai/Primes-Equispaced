#!/usr/bin/env python3
"""
RAYLEIGH QUOTIENT APPROACH TO BOUNDING W(p)/W(p-1)
====================================================

Setup:
  W(N) = Sum_j (f_j - j/n)^2  where f_j are Farey fractions, n = |F_N|.
  Equivalently: W(N) = ||x||^2  where x_j = f_j - j/n (displacement vector).

When going from F_{p-1} to F_p:
  - Dimension grows: n -> n' = n + (p-1)
  - Old entries shift: x_j^new = f_j - rank'(f_j)/n'  (new rank, new normalization)
  - p-1 new entries are added for k/p, k = 1,...,p-1

The ratio W(p)/W(p-1) = ||x'||^2 / ||x||^2 is NOT a standard Rayleigh quotient
because the matrix dimension changes. But we can decompose it.

DECOMPOSITION:
  x'_old = f_j - (j + shift_j)/n'   where shift_j = #{k/p <= f_j, 1<=k<p}
         = f_j - j/n + j/n - (j + shift_j)/n'
         = x_j + j/n - (j + shift_j)/n'
         = x_j + [j*n' - n*(j + shift_j)] / (n*n')
         = x_j + [j*(n'-n) - n*shift_j] / (n*n')
         = x_j + [j*(p-1) - n*shift_j] / (n*n')

  So x'_old = x_old + perturbation, and x'_new are fresh entries.

This script:
1. Constructs displacement vectors explicitly for small primes
2. Decomposes perturbation as rank-1 or low-rank updates
3. Computes the ratio via Rayleigh-type bounds
4. Tests whether Cauchy interlacing / Weyl perturbation gives useful bounds
5. Analyzes the spectral structure of the perturbation matrix
"""

import time
import numpy as np
from math import gcd, isqrt, sqrt, log, floor
from fractions import Fraction

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


def farey_sequence(N):
    """Return F_N as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi


def mertens_sieve(limit):
    """Compute Mobius and Mertens functions up to limit."""
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
            if count > 1:
                sq_free = False
                break
            num_factors += 1
        if sq_free:
            mu[n] = (-1) ** num_factors
    M = [0] * (limit + 1)
    for i in range(1, limit + 1):
        M[i] = M[i-1] + mu[i]
    return mu, M


# ============================================================
# PART 1: DISPLACEMENT VECTOR CONSTRUCTION
# ============================================================

def compute_displacement_vector(F_N):
    """
    Compute x_j = f_j - j/n for Farey sequence F_N.
    Returns numpy array of displacements.
    """
    n = len(F_N)
    x = np.array([float(F_N[j]) - j / n for j in range(n)], dtype=np.float64)
    return x


def compute_W(F_N):
    """W(N) = sum of (f_j - j/n)^2."""
    x = compute_displacement_vector(F_N)
    return np.sum(x ** 2)


# ============================================================
# PART 2: PERTURBATION DECOMPOSITION
# ============================================================

def decompose_perturbation(p, F_old, F_new):
    """
    Decompose the change in displacement vector when going from F_{p-1} to F_p.

    Returns:
      x_old: displacement vector for F_{p-1}
      x_new: displacement vector for F_p
      delta_old: perturbation on old entries (x'_old - x_old, zero-padded)
      x_fresh: displacements of new entries k/p
      shift: array of rank-shifts for old entries
    """
    n = len(F_old)
    n_prime = len(F_new)
    m = p - 1  # number of new fractions

    x_old = compute_displacement_vector(F_old)
    x_new = compute_displacement_vector(F_new)

    # For each old fraction, find its rank shift (how many k/p are <= f_j)
    new_fracs_set = set()
    for k in range(1, p):
        new_fracs_set.add(Fraction(k, p))

    # Find which entries of F_new are old vs new
    old_indices = []  # indices in F_new of old fractions
    new_indices = []  # indices in F_new of new fractions
    for i, f in enumerate(F_new):
        if f in new_fracs_set and f.denominator == p:
            new_indices.append(i)
        else:
            old_indices.append(i)

    # Shift for each old fraction: number of new fractions k/p (1<=k<=p-1) that are <= f_j
    shift = np.zeros(n, dtype=int)
    for j, f in enumerate(F_old):
        # Count #{k in {1,...,p-1} : k/p <= f_j} = #{k : k <= p*f_j, 1<=k<=p-1}
        # = min(floor(p*f_j), p-1) for f_j > 0, else 0
        if f == 0:
            shift[j] = 0
        else:
            shift[j] = min(int(floor(float(f) * p)), p - 1)

    # Perturbation on old entries
    delta_old = np.zeros(n)
    for j in range(n):
        old_rank_term = j / n
        new_rank_term = (j + shift[j]) / n_prime
        delta_old[j] = old_rank_term - new_rank_term
        # x'_j = f_j - (j + shift_j)/n' = (f_j - j/n) + (j/n - (j+shift_j)/n')
        # So delta = j/n - (j+shift_j)/n'

    # Fresh entries (new fractions k/p)
    x_fresh = np.zeros(m)
    for idx, i in enumerate(new_indices):
        x_fresh[idx] = x_new[i]

    return x_old, x_new, delta_old, x_fresh, shift


# ============================================================
# PART 3: RAYLEIGH QUOTIENT ANALYSIS
# ============================================================

def rayleigh_analysis(p, F_old, F_new):
    """
    Analyze the ratio W(p)/W(p-1) using Rayleigh quotient ideas.

    W(p)/W(p-1) = ||x'||^2 / ||x||^2

    Decompose:
      ||x'||^2 = ||x_old + delta_old||^2 + ||x_fresh||^2
               = ||x_old||^2 + 2<x_old, delta_old> + ||delta_old||^2 + ||x_fresh||^2

    So W(p)/W(p-1) = 1 + [2<x_old, delta_old> + ||delta_old||^2 + ||x_fresh||^2] / ||x_old||^2
    """
    x_old, x_new, delta_old, x_fresh, shift = decompose_perturbation(p, F_old, F_new)

    n = len(F_old)
    n_prime = len(F_new)

    W_old = np.sum(x_old ** 2)
    W_new = np.sum(x_new ** 2)

    # Decomposition terms
    cross_term = 2 * np.dot(x_old, delta_old)          # 2 <x_old, delta>
    delta_sq = np.sum(delta_old ** 2)                    # ||delta||^2
    fresh_sq = np.sum(x_fresh ** 2)                      # ||x_fresh||^2

    # Verify decomposition
    recon = W_old + cross_term + delta_sq + fresh_sq
    assert abs(recon - W_new) < 1e-10 * max(W_old, 1e-15), \
        f"Decomposition error: {recon} vs {W_new}, diff={abs(recon-W_new)}"

    ratio = W_new / W_old if W_old > 0 else float('inf')

    return {
        'p': p,
        'n': n,
        'n_prime': n_prime,
        'W_old': W_old,
        'W_new': W_new,
        'ratio': ratio,
        'cross_term': cross_term,
        'delta_sq': delta_sq,
        'fresh_sq': fresh_sq,
        'x_old': x_old,
        'delta_old': delta_old,
        'x_fresh': x_fresh,
        'shift': shift,
    }


# ============================================================
# PART 4: SPECTRAL / LOW-RANK STRUCTURE OF PERTURBATION
# ============================================================

def analyze_perturbation_structure(p, F_old, F_new):
    """
    Check if the perturbation delta_old has low-rank structure.

    delta_old[j] = j/n - (j + shift[j])/n'
                 = j * (1/n - 1/n') - shift[j]/n'
                 = j * (n' - n)/(n*n') - shift[j]/n'
                 = j * m/(n*n') - shift[j]/n'

    So delta_old = (m/(n*n')) * [0, 1, 2, ..., n-1] - (1/n') * shift

    This is RANK 2: a linear combination of the "ramp" vector (j) and the shift vector.
    """
    x_old, x_new, delta_old, x_fresh, shift = decompose_perturbation(p, F_old, F_new)
    n = len(F_old)
    n_prime = len(F_new)
    m = p - 1

    # Decompose delta_old into rank-2 components
    ramp = np.arange(n, dtype=np.float64)
    alpha = m / (n * n_prime)  # coefficient of ramp
    beta = -1.0 / n_prime       # coefficient of shift

    delta_recon = alpha * ramp + beta * shift.astype(np.float64)
    recon_err = np.max(np.abs(delta_old - delta_recon))

    # How much of shift is explained by the linear part?
    # shift[j] ~ floor(p * f_j) ~ p * f_j = p*(x_old[j] + j/n)
    # So shift ~ p*x_old + p*j/n = p*x_old + (p/n)*ramp
    shift_linear = (p / n) * ramp  # linear part of shift
    shift_nonlinear = shift.astype(np.float64) - shift_linear  # floor-error part

    # The nonlinear part is {p*f_j} (fractional part of p*f_j)
    # which encodes the fine arithmetic structure

    # Effective delta after cancellation:
    # delta_old = (m/(n*n'))*ramp - (1/n')*((p/n)*ramp + shift_nonlinear)
    #           = ramp * [m/(n*n') - p/(n*n')] - shift_nonlinear/n'
    #           = ramp * [(m - p)/(n*n')] - shift_nonlinear/n'
    #           = -ramp/(n*n') - shift_nonlinear/n'
    #           = -(ramp + n*shift_nonlinear) / (n*n')
    # Wait: m = p-1, so m - p = -1
    # delta_old = -ramp/(n*n') - shift_nonlinear/n'
    # Hmm, let's verify:
    delta_simplified = -ramp / (n * n_prime) - shift_nonlinear / n_prime
    simp_err = np.max(np.abs(delta_old - delta_simplified))

    # SVD of the perturbation "matrix" (really a vector, but we can look at outer products)
    # The key quantity for Rayleigh analysis: can we bound <x_old, delta_old>?

    # <x_old, delta_old> = alpha * <x, ramp> + beta * <x, shift>
    inner_x_ramp = np.dot(x_old, ramp)
    inner_x_shift = np.dot(x_old, shift.astype(np.float64))

    return {
        'rank2_recon_error': recon_err,
        'simplified_recon_error': simp_err,
        'alpha': alpha,
        'beta': beta,
        'inner_x_ramp': inner_x_ramp,
        'inner_x_shift': inner_x_shift,
        'shift_nonlinear': shift_nonlinear,
        'shift_nonlinear_norm': np.linalg.norm(shift_nonlinear),
        'ramp_norm': np.linalg.norm(ramp),
        'shift_norm': np.linalg.norm(shift.astype(np.float64)),
    }


# ============================================================
# PART 5: CAUCHY INTERLACING / EMBEDDING APPROACH
# ============================================================

def embedding_analysis(p, F_old, F_new):
    """
    Embed both displacement vectors in the same n'-dimensional space.

    Define:
      v_old = (x_old[0], x_old[1], ..., x_old[n-1], 0, ..., 0)  in R^{n'}
      v_new = x_new  in R^{n'}

    Then W_old = ||v_old||^2 (same), W_new = ||v_new||^2.
    ratio = ||v_new||^2 / ||v_old||^2

    But the entries of v_old and v_new are in DIFFERENT positions (the new fractions
    are interspersed). We need to track which components correspond to which.

    Better: define the n' x n' matrix A_new = diag(x_new), and the n x n matrix
    A_old = diag(x_old). Then W = trace(A^2).

    For the Gram matrix approach: W = x^T x = trace(x x^T).
    The ratio is trace(x_new x_new^T) / trace(x_old x_old^T).
    """
    x_old, x_new, delta_old, x_fresh, shift = decompose_perturbation(p, F_old, F_new)

    n = len(F_old)
    n_prime = len(F_new)

    # Compute the correlation between old and new displacement vectors
    # by aligning them: for each old fraction, find its index in F_new
    new_fracs_set = set()
    for k in range(1, p):
        new_fracs_set.add(Fraction(k, p))

    old_in_new = []  # x_new values at positions of old fractions
    for i, f in enumerate(F_new):
        if not (f in new_fracs_set and f.denominator == p):
            old_in_new.append(x_new[i])
    old_in_new = np.array(old_in_new)

    # Correlation between old displacements and their new values
    if np.linalg.norm(x_old) > 0 and np.linalg.norm(old_in_new) > 0:
        cos_angle = np.dot(x_old, old_in_new) / (np.linalg.norm(x_old) * np.linalg.norm(old_in_new))
    else:
        cos_angle = 0.0

    # Norm ratios
    old_part_ratio = np.sum(old_in_new ** 2) / np.sum(x_old ** 2) if np.sum(x_old ** 2) > 0 else 0
    fresh_contribution = np.sum(x_fresh ** 2) / np.sum(x_new ** 2) if np.sum(x_new ** 2) > 0 else 0

    return {
        'cos_angle': cos_angle,
        'old_part_ratio': old_part_ratio,
        'fresh_contribution': fresh_contribution,
    }


# ============================================================
# PART 6: MATRIX PERTURBATION BOUNDS
# ============================================================

def perturbation_bounds(p, result, struct):
    """
    Apply Weyl's perturbation theorem ideas.

    Since delta_old is rank 2 (ramp + shift components), the perturbation
    x_old -> x_old + delta_old changes ||x||^2 by at most:

    | ||x+delta||^2 - ||x||^2 | = |2<x,delta> + ||delta||^2|
                                 <= 2||x||*||delta|| + ||delta||^2

    For the ratio:
      W_new/W_old = 1 + (2<x,delta> + ||delta||^2 + ||x_fresh||^2) / ||x||^2

    Cauchy-Schwarz gives:
      ratio <= 1 + (2||x||*||delta|| + ||delta||^2 + ||x_fresh||^2) / ||x||^2
             = 1 + 2*||delta||/||x|| + (||delta||/||x||)^2 + ||x_fresh||^2/||x||^2

    And:
      ratio >= 1 - 2*||delta||/||x|| + (||delta||/||x||)^2 + ||x_fresh||^2/||x||^2
             = (1 - ||delta||/||x||)^2 + ||x_fresh||^2/||x||^2

    So the fresh term always INCREASES W (pushes ratio > 1),
    and the perturbation term can go either way.
    """
    x_old = result['x_old']
    delta_old = result['delta_old']
    x_fresh = result['x_fresh']

    norm_x = np.linalg.norm(x_old)
    norm_delta = np.linalg.norm(delta_old)
    norm_fresh = np.linalg.norm(x_fresh)

    if norm_x == 0:
        return {'upper_bound': float('inf'), 'lower_bound': 0}

    eps = norm_delta / norm_x
    eta = norm_fresh / norm_x

    upper = 1 + 2 * eps + eps ** 2 + eta ** 2  # = (1 + eps)^2 + eta^2
    lower = max(0, (1 - eps) ** 2 + eta ** 2)

    # Tighter bounds using actual inner product direction
    actual_cross = result['cross_term'] / result['W_old']
    actual_ratio = result['ratio']

    return {
        'eps': eps,
        'eta': eta,
        'upper_bound': upper,
        'lower_bound': lower,
        'actual_ratio': actual_ratio,
        'actual_cross_normalized': actual_cross,
        'bound_width': upper - lower,
    }


# ============================================================
# PART 7: SHIFT VECTOR ARITHMETIC ANALYSIS
# ============================================================

def shift_arithmetic(p, F_old):
    """
    Analyze shift[j] = floor(p * f_j) and its "fractional part" structure.

    For f_j = a/b with gcd(a,b)=1 and b <= p-1, p prime:
      p * f_j = p*a/b
      Since gcd(p, b) = 1 (p prime, b < p): {p*a/b} = {pa mod b}/b

    So shift_nonlinear[j] = {p*a_j/b_j} - correction = fractional part related quantity.

    The distribution of {p*a/b mod b}/b as (a,b) ranges over Farey fractions
    is related to Kloosterman-type sums.
    """
    n = len(F_old)
    frac_parts = []
    for j, f in enumerate(F_old):
        a, b = f.numerator, f.denominator
        if b == 1:
            frac_parts.append(0.0)
        else:
            # {p*a/b} = (p*a mod b) / b
            remainder = (p * a) % b
            frac_parts.append(remainder / b)

    frac_parts = np.array(frac_parts)

    # Statistics
    mean_frac = np.mean(frac_parts[1:-1])  # exclude 0/1 and 1/1
    var_frac = np.var(frac_parts[1:-1])

    # For uniform distribution of fractional parts, mean = 0.5, var = 1/12
    return {
        'mean_frac_part': mean_frac,
        'var_frac_part': var_frac,
        'expected_mean': 0.5,
        'expected_var': 1.0 / 12,
        'frac_parts': frac_parts,
    }


# ============================================================
# MAIN COMPUTATION
# ============================================================

print("=" * 80)
print("RAYLEIGH QUOTIENT ANALYSIS OF W(p)/W(p-1)")
print("=" * 80)

PRIME_LIMIT = 50
primes = sieve_primes(PRIME_LIMIT)
mu, M = mertens_sieve(PRIME_LIMIT)

print(f"\nAnalyzing primes up to {PRIME_LIMIT}: {primes}")
print()

# Precompute Farey sequences
farey_cache = {}
for N in range(1, PRIME_LIMIT + 1):
    farey_cache[N] = farey_sequence(N)

# ---- TABLE 1: Basic ratio decomposition ----
print("-" * 100)
np_label = "n'"
print(f"{'p':>4} {'M(p)':>5} {'n':>6} {np_label:>6} {'W_old':>12} {'W_new':>12} "
      f"{'ratio':>8} {'cross':>10} {'|delta|^2':>10} {'|fresh|^2':>10}")
print("-" * 100)

results = []
for p in primes:
    F_old = farey_cache[p - 1]
    F_new = farey_cache[p]
    res = rayleigh_analysis(p, F_old, F_new)
    res['M_p'] = M[p]
    results.append(res)

    print(f"{p:4d} {M[p]:5d} {res['n']:6d} {res['n_prime']:6d} "
          f"{res['W_old']:12.8f} {res['W_new']:12.8f} "
          f"{res['ratio']:8.6f} {res['cross_term']:10.6f} "
          f"{res['delta_sq']:10.6f} {res['fresh_sq']:10.6f}")

# ---- TABLE 2: Perturbation structure (rank-2 decomposition) ----
print()
print("=" * 80)
print("PERTURBATION STRUCTURE (rank-2 decomposition)")
print("=" * 80)
print()
print(f"{'p':>4} {'rank2_err':>12} {'simp_err':>12} {'<x,ramp>':>12} {'<x,shift>':>12} "
      f"{'||shift_NL||':>12}")
print("-" * 80)

for p in primes:
    F_old = farey_cache[p - 1]
    F_new = farey_cache[p]
    struct = analyze_perturbation_structure(p, F_old, F_new)

    print(f"{p:4d} {struct['rank2_recon_error']:12.2e} {struct['simplified_recon_error']:12.2e} "
          f"{struct['inner_x_ramp']:12.6f} {struct['inner_x_shift']:12.6f} "
          f"{struct['shift_nonlinear_norm']:12.6f}")

# ---- TABLE 3: Cauchy-Schwarz bounds vs actual ratio ----
print()
print("=" * 80)
print("PERTURBATION BOUNDS (Weyl / Cauchy-Schwarz)")
print("=" * 80)
print()
print(f"{'p':>4} {'M(p)':>5} {'eps':>8} {'eta':>8} {'lower':>8} {'actual':>8} {'upper':>8} "
      f"{'width':>8} {'cross/W':>9}")
print("-" * 90)

for i, p in enumerate(primes):
    F_old = farey_cache[p - 1]
    F_new = farey_cache[p]
    res = results[i]
    struct = analyze_perturbation_structure(p, F_old, F_new)
    bounds = perturbation_bounds(p, res, struct)

    marker = " <-- DW>0" if res['ratio'] > 1 else ""
    print(f"{p:4d} {M[p]:5d} {bounds['eps']:8.5f} {bounds['eta']:8.5f} "
          f"{bounds['lower_bound']:8.5f} {bounds['actual_ratio']:8.5f} {bounds['upper_bound']:8.5f} "
          f"{bounds['bound_width']:8.5f} {bounds['actual_cross_normalized']:9.6f}{marker}")

# ---- TABLE 4: Embedding / correlation analysis ----
print()
print("=" * 80)
print("EMBEDDING ANALYSIS (old vs new displacement correlation)")
print("=" * 80)
print()
print(f"{'p':>4} {'cos(angle)':>12} {'old_part_ratio':>16} {'fresh_contrib':>16}")
print("-" * 60)

for p in primes:
    F_old = farey_cache[p - 1]
    F_new = farey_cache[p]
    emb = embedding_analysis(p, F_old, F_new)

    print(f"{p:4d} {emb['cos_angle']:12.8f} {emb['old_part_ratio']:16.8f} "
          f"{emb['fresh_contribution']:16.8f}")

# ---- TABLE 5: Fractional part distribution (Kloosterman connection) ----
print()
print("=" * 80)
print("SHIFT FRACTIONAL PARTS {p*a/b} DISTRIBUTION")
print("=" * 80)
print()
print(f"{'p':>4} {'mean({pa/b})':>14} {'var({pa/b})':>14} {'expected_mean':>14} {'expected_var':>14}")
print("-" * 70)

for p in primes:
    F_old = farey_cache[p - 1]
    sa = shift_arithmetic(p, F_old)

    print(f"{p:4d} {sa['mean_frac_part']:14.8f} {sa['var_frac_part']:14.8f} "
          f"{sa['expected_mean']:14.8f} {sa['expected_var']:14.8f}")


# ============================================================
# PART 8: KEY OBSERVATIONS AND BOUNDS
# ============================================================

print()
print("=" * 80)
print("KEY OBSERVATIONS")
print("=" * 80)
print()

# Check: is the cross term always negative when ratio > 1?
print("1. CROSS TERM SIGN vs RATIO:")
for i, p in enumerate(primes):
    res = results[i]
    cross_sign = "+" if res['cross_term'] >= 0 else "-"
    ratio_dir = "W grows" if res['ratio'] > 1 else "W shrinks"
    print(f"   p={p:3d}: cross={cross_sign} ({res['cross_term']:+.6f}), "
          f"delta^2={res['delta_sq']:.6f}, fresh^2={res['fresh_sq']:.6f} -> {ratio_dir}")

# Which term dominates?
print()
print("2. TERM DOMINANCE (normalized by W_old):")
for i, p in enumerate(primes):
    res = results[i]
    W = res['W_old']
    if W == 0:
        continue
    c = res['cross_term'] / W
    d = res['delta_sq'] / W
    f = res['fresh_sq'] / W
    dominant = 'cross' if abs(c) > max(d, f) else ('delta^2' if d > f else 'fresh^2')
    print(f"   p={p:3d}: cross/W={c:+.6f}, delta^2/W={d:.6f}, fresh^2/W={f:.6f} -> dominant: {dominant}")

# Scaling analysis
print()
print("3. SCALING OF TERMS WITH p (for large p):")
print(f"   {'p':>4} {'||delta||/||x||':>16} {'||fresh||/||x||':>16} {'||delta||~1/n?':>16}")
for i, p in enumerate(primes):
    res = results[i]
    norm_x = np.linalg.norm(res['x_old'])
    norm_d = np.linalg.norm(res['delta_old'])
    norm_f = np.linalg.norm(res['x_fresh'])
    if norm_x == 0:
        continue
    n = res['n']
    print(f"   {p:4d} {norm_d/norm_x:16.8f} {norm_f/norm_x:16.8f} "
          f"{norm_d * n:16.8f}")


# ============================================================
# PART 9: REFINED BOUND USING SHIFT STRUCTURE
# ============================================================

print()
print("=" * 80)
print("REFINED BOUND: Using delta = -ramp/(n*n') - shift_NL/n'")
print("=" * 80)
print()
print("Since delta_old = -(j + n*{p*f_j})/(n*n'), the cross term is:")
print("  <x, delta> = -(1/(n*n'))*[<x, ramp> + n*<x, shift_NL>]")
print()
print(f"{'p':>4} {'<x,ramp>':>12} {'n*<x,sNL>':>12} {'sum':>12} {'cross_pred':>12} {'cross_act':>12} {'err':>8}")
print("-" * 80)

for p in primes:
    F_old = farey_cache[p - 1]
    F_new = farey_cache[p]
    x_old, x_new, delta_old, x_fresh, shift = decompose_perturbation(p, F_old, F_new)
    n = len(F_old)
    n_prime = len(F_new)

    ramp = np.arange(n, dtype=np.float64)
    shift_linear = (p / n) * ramp
    shift_nl = shift.astype(np.float64) - shift_linear

    xr = np.dot(x_old, ramp)
    xs = n * np.dot(x_old, shift_nl)
    total = xr + xs
    cross_pred = -total / (n * n_prime)
    # Factor of 2 for cross_term = 2*<x,delta>
    cross_pred_2 = 2 * cross_pred
    cross_actual = 2 * np.dot(x_old, delta_old)
    err = abs(cross_pred_2 - cross_actual)

    print(f"{p:4d} {xr:12.6f} {xs:12.6f} {total:12.6f} "
          f"{cross_pred_2:12.6f} {cross_actual:12.6f} {err:8.2e}")


# ============================================================
# PART 10: CAN WE BOUND ||D_new||/||D_old|| USING DISPLACEMENT-SHIFT?
# ============================================================

print()
print("=" * 80)
print("DISPLACEMENT-SHIFT IDENTITY: D_new vs D_old")
print("=" * 80)
print()
print("D(f_j) = rank(f_j) - n*f_j. Define D vector.")
print("D_new[f_j] = (j + shift_j + 1) - n'*f_j  [for old fraction at new rank]")
print("D_old[f_j] = (j + 1) - n*f_j")
print("Difference = shift_j - (n'-n)*f_j = shift_j - (p-1)*f_j")
print("           = floor(p*f_j) - (p-1)*f_j = floor(p*f_j) - p*f_j + f_j")
print("           = -{p*f_j} + f_j")
print()
print(f"{'p':>4} {'||D_old||':>12} {'||D_new||':>12} {'||D_new||/||D_old||':>20} {'ratio^2':>12}")
print("-" * 70)

for p in primes:
    F_old = farey_cache[p - 1]
    F_new = farey_cache[p]
    n = len(F_old)
    n_prime = len(F_new)

    # D_old using inclusive rank: D_old[j] = (j+1) - n*f_j
    D_old = np.array([(j + 1) - n * float(F_old[j]) for j in range(n)])
    D_new = np.array([(j + 1) - n_prime * float(F_new[j]) for j in range(n_prime)])

    norm_D_old = np.linalg.norm(D_old)
    norm_D_new = np.linalg.norm(D_new)
    ratio_D = norm_D_new / norm_D_old if norm_D_old > 0 else float('inf')

    # W = sum D_j^2 / n^2, so W_new/W_old = (||D_new||/||D_old||)^2 * (n/n')^2
    ratio_W_from_D = (ratio_D * n / n_prime) ** 2

    print(f"{p:4d} {norm_D_old:12.6f} {norm_D_new:12.6f} {ratio_D:20.8f} "
          f"{ratio_W_from_D:12.8f}")

    # Verify against direct computation
    W_old_direct = np.sum(D_old ** 2) / n ** 2
    W_new_direct = np.sum(D_new ** 2) / n_prime ** 2
    # Note: this uses D(f_j) = (j+1) - n*f_j, which differs from x_j = f_j - j/n
    # by a constant shift. W as sum of x^2 and sum of D^2/n^2 differ.


# ============================================================
# SUMMARY
# ============================================================

elapsed = time.time() - start_time
print()
print("=" * 80)
print(f"SUMMARY (computed in {elapsed:.2f}s)")
print("=" * 80)
print()
print("KEY FINDINGS:")
print()
print("1. The perturbation delta_old has RANK 2 structure:")
print("   delta_old = -(j + n*{p*f_j}) / (n*n')")
print("   where {p*f_j} is the fractional part of p*a_j/b_j.")
print()
print("2. The ratio W(p)/W(p-1) = 1 + [2<x,delta> + ||delta||^2 + ||fresh||^2] / ||x||^2")
print("   - ||delta||^2 and ||fresh||^2 are always >= 0 (push ratio up)")
print("   - The cross term 2<x,delta> determines the sign of DeltaW")
print()
print("3. Cauchy-Schwarz bounds: (1-eps)^2 + eta^2 <= ratio <= (1+eps)^2 + eta^2")
print("   where eps = ||delta||/||x||, eta = ||fresh||/||x||")
print("   These bounds are too loose to determine sign of DeltaW.")
print()
print("4. To get a USEFUL bound on the cross term, we need:")
print("   <x_old, delta_old> = -(1/(n*n')) * [<x, ramp> + n*<x, {p*f}>]")
print("   The inner product <x, {p*f}> involves Kloosterman-type sums.")
print()
print("5. The fractional parts {p*a/b} are approximately uniform (mean ~ 0.5, var ~ 1/12)")
print("   suggesting that <x, {p*f}> should be small by cancellation --")
print("   but the exact cancellation depends on correlations with the displacement x.")
