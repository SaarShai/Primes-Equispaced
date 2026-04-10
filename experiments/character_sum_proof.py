#!/usr/bin/env python3
"""
CHARACTER SUM APPROACH TO BOUNDING R(p)
========================================

Goal: Prove |R(p)| < 1/2 for all primes p, where
  R(p) = Sum D_rough(f) * delta(f) / Sum delta(f)^2

Approach: Decompose R(p) per-denominator into S_b terms, then bound
each S_b using character sum (Weil-type) bounds.

For each denominator b with gcd(b, p) = 1:
  sigma_p(a) = pa mod b  (a permutation of coprime residues)
  delta(a/b) = (a - sigma_p(a)) / b
  D_rough(a/b) = D(a/b) + 1/2  (fluctuation around smooth mean)
  S_b = Sum_{gcd(a,b)=1} D_rough(a/b) * delta(a/b)

Character expansion:
  D_rough(a/b) = Sum_chi d_hat(chi) * chi(a)
  S_b = Sum_chi d_hat(chi) * T_chi(b)
  where T_chi(b) = Sum_{gcd(a,b)=1} chi(a) * (a - pa mod b) / b

For non-trivial chi, the Weil bound gives |T_chi(b)| <= C * sqrt(b).
The question: does this yield |R(p)| < 1/2?

Author: Claude (character sum analysis for Farey discrepancy project)
Date: 2026-03-29
"""

import numpy as np
from math import gcd, floor, sqrt, pi, log, isqrt, ceil
from collections import defaultdict
import time

start_time = time.time()

# ========================================================================
# PART 1: Core computational functions
# ========================================================================

def sieve(limit):
    """Simple sieve of Eratosthenes."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, isqrt(limit) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

def euler_phi(n):
    """Euler's totient function."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def mobius(n):
    """Mobius function."""
    if n == 1:
        return 1
    factors = 0
    temp = n
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            factors += 1
            temp //= p
            if temp % p == 0:
                return 0  # p^2 divides n
        p += 1
    if temp > 1:
        factors += 1
    return (-1) ** factors

def build_farey_sequence(N):
    """Build Farey sequence F_N as list of (a, b) with a/b in [0, 1]."""
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: x[0] / x[1])
    return fracs

def compute_D_values(farey_seq):
    """
    Compute D(a/b) = rank(a/b) - |F_N| * (a/b) for each fraction.
    rank is 0-indexed: D(0/1) = 0 - 0 = 0.
    Uses n = |F_N| (the full count), matching the canonical definition.
    """
    n = len(farey_seq)
    D = {}
    for rank, (a, b) in enumerate(farey_seq):
        val = a / b
        D[(a, b)] = rank - n * val  # canonical: rank - n * (a/b)
    return D, n

def compute_D_rough(D_vals):
    """D_rough(a/b) = D(a/b) + 1/2 (fluctuation around smooth mean)."""
    return {k: v + 0.5 for k, v in D_vals.items()}

def compute_D_plain(D_vals):
    """Just return D values as-is (for the canonical R definition)."""
    return dict(D_vals)


# ========================================================================
# PART 2: Per-denominator cross-term analysis
# ========================================================================

def compute_S_b(p, b, D_rough, farey_set):
    """
    Compute S_b = Sum_{gcd(a,b)=1, 0<a/b<1} D(a/b) * delta(a/b)
    where delta(a/b) = (a - pa mod b) / b.

    EXCLUDES endpoints a=0 and a=b (they have delta=0 anyway).
    """
    N = p - 1
    if b > N or gcd(b, p) != 1:
        return 0.0, 0, 0.0

    S = 0.0
    count = 0
    delta_sq_sum = 0.0

    for a in range(1, b):  # INTERIOR fractions only: 0 < a/b < 1
        if gcd(a, b) != 1:
            continue
        if (a, b) not in D_rough:
            continue

        # sigma_p(a) = pa mod b
        sigma = (p * a) % b
        delta = (a - sigma) / b

        S += D_rough[(a, b)] * delta
        delta_sq_sum += delta ** 2
        count += 1

    return S, count, delta_sq_sum


def weil_type_bound(b, phi_b):
    """
    Theoretical Weil-type bound for |S_b|.

    For non-trivial characters chi mod b:
      |Sum_{gcd(a,b)=1} chi(a) * (a - sigma_p(a))| <= 2 * sqrt(b)  (Weil)

    After summing over all characters to reconstruct D_rough:
      |S_b| should be bounded by ~ C * phi(b) * sqrt(b) / b

    The factor breakdown:
      - phi(b) characters contribute
      - Each character sum bounded by sqrt(b) (Weil)
      - Division by b from delta = (...)/b
      - But D_rough Fourier coefficients decay, giving additional savings

    We test several candidate bounds.
    """
    return {
        'weil_basic': phi_b * sqrt(b) / b,           # C * phi(b) * sqrt(b) / b
        'weil_tight': sqrt(phi_b * b),                # sqrt(phi(b) * b)
        'trivial': phi_b,                              # trivial bound
        'sqrt_phi': sqrt(phi_b),                       # optimistic
    }


# ========================================================================
# PART 3: Dirichlet character analysis (exact)
# ========================================================================

def dirichlet_characters_mod_b(b):
    """
    Compute all Dirichlet characters mod b.
    Returns list of dicts: chi[a] for gcd(a,b)=1.
    Uses the structure of (Z/bZ)*.

    For small b, we compute explicitly via the discrete log.
    """
    # Find coprime residues
    coprimes = [a for a in range(1, b) if gcd(a, b) == 1]
    phi_b = len(coprimes)

    if phi_b == 0:
        return []

    # Find a generator if cyclic (works for prime b, 2*prime, 4, prime^k, 2*prime^k)
    # For general b, use the full character group
    # For our purposes, use DFT on the group

    # Build multiplication table
    # Map coprimes to indices
    idx = {a: i for i, a in enumerate(coprimes)}

    # Build group multiplication table
    mult_table = np.zeros((phi_b, phi_b), dtype=int)
    for i, a in enumerate(coprimes):
        for j, c in enumerate(coprimes):
            prod = (a * c) % b
            mult_table[i, j] = idx[prod]

    # Characters are group homomorphisms (Z/bZ)* -> C*
    # For cyclic groups, characters are chi_k(g^j) = exp(2*pi*i*j*k/phi_b)
    # For general groups, we need to find the group structure

    # Simple approach: find generators using Smith normal form of the group
    # For small b, just enumerate using the regular representation

    # Use the eigenvalues of the regular representation
    # The regular representation matrix for generator g:
    # R_g[i,j] = 1 if g * coprimes[j] mod b = coprimes[i]

    # Find a generating set
    chars = []

    # For each potential character, check if it's a homomorphism
    # Use the fact that characters of abelian groups form the Pontryagin dual
    # For cyclic groups of order n, chi_k(a) = exp(2*pi*i*k*discrete_log(a)/n)

    # Find group generators by trying each element
    generated = set()
    generators = []
    remaining = set(range(phi_b))

    while remaining:
        # Find element generating the most
        best_gen = None
        best_order = 0
        for g_idx in remaining:
            g = coprimes[g_idx]
            order = 1
            current = g
            while current != 1 and order <= phi_b:
                current = (current * g) % b
                order += 1
            if current == 1 and order > best_order:
                best_order = order
                best_gen = g_idx

        if best_gen is None:
            break

        generators.append((best_gen, best_order))
        # Mark generated elements
        g = coprimes[best_gen]
        current = 1
        new_gen = set()
        for _ in range(best_order):
            current = (current * g) % b
            if current in idx:
                new_gen.add(idx[current])

        # Combine with previously generated
        if not generated:
            generated = new_gen | {idx[1]}
        else:
            # Take products
            new_combined = set()
            for x in generated:
                for y in new_gen:
                    prod = (coprimes[x] * coprimes[y]) % b
                    new_combined.add(idx[prod])
            generated = generated | new_gen | new_combined

        remaining -= generated

        if len(generated) >= phi_b:
            break

    # For simplicity with small b, compute characters via DFT
    # Build the regular representation matrix for an arbitrary generator
    if phi_b <= 1:
        return [np.ones(phi_b, dtype=complex)]

    # Use numpy eigendecomposition of a circulant-like matrix
    # Take the first non-identity coprime as base
    g = coprimes[1] if len(coprimes) > 1 else coprimes[0]
    R = np.zeros((phi_b, phi_b))
    for j, c in enumerate(coprimes):
        prod = (g * c) % b
        i = idx[prod]
        R[i, j] = 1.0

    # Eigenvalues/eigenvectors give characters
    eigenvalues, eigenvectors = np.linalg.eig(R)

    # Each eigenvector gives a character
    characters = []
    for k in range(phi_b):
        v = eigenvectors[:, k]
        # Normalize so v[idx[1]] = 1
        if abs(v[idx[1]]) > 1e-10:
            v = v / v[idx[1]]
        chi = {}
        for i, a in enumerate(coprimes):
            chi[a] = complex(v[i])
        characters.append(chi)

    return characters


def analyze_character_sums(p, b, characters, D_rough):
    """
    For each character chi mod b, compute:
      d_hat(chi) = (1/phi(b)) * Sum_{gcd(a,b)=1} D_rough(a/b) * conj(chi(a))
      T_chi(b)   = Sum_{gcd(a,b)=1} chi(a) * (a - pa mod b) / b

    Then S_b = Sum_chi d_hat(chi) * T_chi(b).

    Returns character-level breakdown.
    """
    N = p - 1
    coprimes = [a for a in range(0, b + 1) if gcd(a, b) == 1 and (a, b) in D_rough]
    phi_b = len(coprimes)

    if phi_b == 0 or not characters:
        return []

    results = []
    for chi in characters:
        # d_hat(chi) = (1/phi_b) * Sum D_rough(a/b) * conj(chi(a))
        d_hat = 0.0j
        for a in coprimes:
            if a in chi:
                d_hat += D_rough[(a, b)] * np.conj(chi[a])
        d_hat /= phi_b

        # T_chi(b) = Sum chi(a) * (a - pa mod b) / b
        T_chi = 0.0j
        for a in coprimes:
            sigma = (p * a) % b
            delta = (a - sigma) / b
            if a in chi:
                T_chi += chi[a] * delta

        # Is this the trivial character?
        is_trivial = all(abs(chi.get(a, 0) - 1.0) < 0.1 for a in coprimes if a in chi)

        results.append({
            'd_hat': d_hat,
            'T_chi': T_chi,
            'contribution': d_hat * T_chi,
            'is_trivial': is_trivial,
            '|T_chi|': abs(T_chi),
            'weil_bound': 2 * sqrt(b),  # Weil bound for |T_chi|
        })

    return results


# ========================================================================
# PART 4: Main analysis
# ========================================================================

def analyze_prime(p, verbose=True, use_D_rough=False):
    """Full character sum analysis for prime p.

    If use_D_rough=True, use D_rough = D + 1/2.
    If use_D_rough=False (default), use canonical R = 2*Sum(D*delta)/Sum(delta^2).
    """
    N = p - 1
    R_factor = 1 if use_D_rough else 2  # canonical R has factor of 2

    if verbose:
        print(f"\n{'='*70}")
        label = "D_rough" if use_D_rough else "D (canonical)"
        print(f"PRIME p = {p}, N = p-1 = {N}, using {label}")
        print(f"{'='*70}")

    # Build Farey sequence
    farey_seq = build_farey_sequence(N)
    D_vals, n_farey = compute_D_values(farey_seq)
    D_rough = compute_D_rough(D_vals) if use_D_rough else compute_D_plain(D_vals)
    farey_set = set(f for f in farey_seq)

    # Per-denominator analysis
    total_cross = 0.0
    total_delta_sq = 0.0

    sb_data = []

    for b in range(1, N + 1):
        S_b, count, dsq = compute_S_b(p, b, D_rough, farey_set)
        if count == 0:
            continue

        phi_b = euler_phi(b)
        bounds = weil_type_bound(b, phi_b)

        total_cross += S_b
        total_delta_sq += dsq

        sb_data.append({
            'b': b,
            'S_b': S_b,
            'count': count,
            'phi_b': phi_b,
            'delta_sq': dsq,
            'bounds': bounds,
            '|S_b|': abs(S_b),
        })

    R = R_factor * total_cross / total_delta_sq if total_delta_sq > 0 else 0

    # Also compute Sum delta (should be ~0 if mean shift is zero)
    # Exclude endpoints
    total_delta = sum(
        (a - (p * a) % b) / b
        for (a, b) in farey_seq
        if a > 0 and a < b and gcd(b, p) == 1 and (a, b) in D_rough
    )

    if verbose:
        print(f"|F_{N}| = {n_farey}")
        print(f"\nR(p={p}) = {R:.8f}")
        print(f"  Sum D*delta     = {total_cross:.8f}")
        print(f"  Sum delta^2     = {total_delta_sq:.8f}")
        print(f"  Sum delta       = {total_delta:.8f} (should be ~0)")
        print(f"  R_factor        = {R_factor}")
        print(f"  |R| = {abs(R):.8f} {'< 0.5 OK' if abs(R) < 0.5 else '>= 0.5 PROBLEM'}")

    # Check which bound works for S_b
    if verbose:
        print(f"\n--- Per-denominator S_b vs bounds ---")
        print(f"{'b':>4} {'phi(b)':>6} {'|S_b|':>12} {'weil_basic':>12} {'weil_tight':>12} {'ratio_basic':>12}")

    max_ratio_basic = 0
    max_ratio_tight = 0
    bound_holds_basic = True
    bound_holds_tight = True

    for d in sb_data:
        b = d['b']
        abs_sb = d['|S_b|']
        wb = d['bounds']['weil_basic']
        wt = d['bounds']['weil_tight']

        ratio_b = abs_sb / wb if wb > 0 else float('inf')
        ratio_t = abs_sb / wt if wt > 0 else float('inf')

        max_ratio_basic = max(max_ratio_basic, ratio_b)
        max_ratio_tight = max(max_ratio_tight, ratio_t)

        if ratio_b > 1.0:
            bound_holds_basic = False
        if ratio_t > 1.0:
            bound_holds_tight = False

        if verbose and b <= 30:
            print(f"{b:>4} {d['phi_b']:>6} {abs_sb:>12.6f} {wb:>12.6f} {wt:>12.6f} {ratio_b:>12.6f}")

    if verbose:
        print(f"  ... (showing b <= 30)")
        print(f"\n  Max |S_b|/weil_basic ratio: {max_ratio_basic:.6f}")
        print(f"  Max |S_b|/weil_tight ratio: {max_ratio_tight:.6f}")
        print(f"  weil_basic bound holds: {bound_holds_basic}")
        print(f"  weil_tight bound holds: {bound_holds_tight}")

    # Find the best constant C such that |S_b| <= C * phi(b) * sqrt(b) / b for all b
    best_C = 0
    for d in sb_data:
        b = d['b']
        phi_b = d['phi_b']
        if phi_b > 0 and b > 1:
            bound_unit = phi_b * sqrt(b) / b
            if bound_unit > 0:
                C_needed = d['|S_b|'] / bound_unit
                best_C = max(best_C, C_needed)

    if verbose:
        print(f"\n  Best constant C for |S_b| <= C * phi(b)*sqrt(b)/b: C = {best_C:.6f}")

    # Now check: if |S_b| <= C * phi(b)*sqrt(b)/b, does Sum |S_b| < (1/2) * Sum delta^2?
    sum_bound = 0
    for d in sb_data:
        b = d['b']
        phi_b = d['phi_b']
        if b > 1:
            sum_bound += best_C * phi_b * sqrt(b) / b

    ratio_to_half = sum_bound / (0.5 * total_delta_sq) if total_delta_sq > 0 else float('inf')

    if verbose:
        print(f"\n  Sum of bounds = {sum_bound:.6f}")
        print(f"  0.5 * Sum delta^2 = {0.5 * total_delta_sq:.6f}")
        print(f"  Ratio (bound / half_denom) = {ratio_to_half:.6f}")
        if ratio_to_half < 1:
            print(f"  ==> CHARACTER SUM BOUND PROVES |R| < 1/2!")
        else:
            print(f"  ==> Bound too loose by factor {ratio_to_half:.4f}")

    # ====================================================================
    # Character-level analysis for small b (skip for now - focus on bounds)
    # ====================================================================

    # ====================================================================
    # Alternative: direct bound via Cauchy-Schwarz
    # ====================================================================
    # |R| = |Sum D_rough * delta| / Sum delta^2
    #     <= sqrt(Sum D_rough^2) * sqrt(Sum delta^2) / Sum delta^2
    #     = sqrt(Sum D_rough^2) / sqrt(Sum delta^2)

    sum_D_rough_sq = sum(D_rough[(a, b)]**2 for (a, b) in farey_seq if a > 0 and a < b)
    cs_bound = sqrt(sum_D_rough_sq) / sqrt(total_delta_sq) if total_delta_sq > 0 else float('inf')

    if verbose:
        print(f"\n--- Cauchy-Schwarz bound ---")
        print(f"  Sum D_rough^2 = {sum_D_rough_sq:.6f}")
        print(f"  Sum delta^2   = {total_delta_sq:.6f}")
        print(f"  CS bound on |R|: {cs_bound:.6f}")
        print(f"  Actual |R|:      {abs(R):.6f}")
        print(f"  CS/actual ratio: {cs_bound / abs(R):.4f}x loose" if abs(R) > 1e-10 else "  R ~ 0")

    return {
        'p': p,
        'R': R,
        '|R|': abs(R),
        'total_cross': total_cross,
        'total_delta_sq': total_delta_sq,
        'best_C': best_C,
        'sum_bound': sum_bound,
        'ratio_to_half': ratio_to_half,
        'cs_bound': cs_bound,
        'proves_half': ratio_to_half < 1,
        'sb_data': sb_data,
    }


# ========================================================================
# PART 5: Scaling analysis
# ========================================================================

def scaling_analysis():
    """Check how the character sum bound scales with p."""
    print("\n" + "=" * 70)
    print("SCALING ANALYSIS: How does the bound ratio scale with p?")
    print("=" * 70)

    test_primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    # Add larger primes if feasible
    for p in [101, 107, 127, 131, 149, 151, 163, 173, 181, 191, 197, 199]:
        test_primes.append(p)

    print(f"\n{'p':>5} {'|R|':>10} {'C_best':>10} {'bound_ratio':>12} {'CS_bound':>10} {'log(p)/sqrt(p)':>14}")

    results = []
    for p in test_primes:
        t0 = time.time()
        res = analyze_prime(p, verbose=False)
        elapsed = time.time() - t0

        log_over_sqrt = log(p) / sqrt(p)

        print(f"{p:>5} {res['|R|']:>10.6f} {res['best_C']:>10.4f} {res['ratio_to_half']:>12.6f} "
              f"{res['cs_bound']:>10.4f} {log_over_sqrt:>14.6f}  ({elapsed:.1f}s)")

        results.append(res)

        # Skip if getting too slow
        if elapsed > 30:
            print(f"  (skipping larger primes, {elapsed:.0f}s for p={p})")
            break

    # Fit scaling law: ratio_to_half ~ A * p^alpha
    valid = [(r['p'], r['ratio_to_half']) for r in results if r['ratio_to_half'] > 0 and r['p'] >= 11]
    if len(valid) >= 3:
        log_p = np.array([log(x[0]) for x in valid])
        log_ratio = np.array([log(x[1]) for x in valid])

        # Linear fit: log(ratio) = alpha * log(p) + log(A)
        coeffs = np.polyfit(log_p, log_ratio, 1)
        alpha = coeffs[0]
        A = np.exp(coeffs[1])

        print(f"\nScaling fit: ratio ~ {A:.4f} * p^({alpha:.4f})")
        print(f"  If alpha < 0, the bound gets BETTER with larger p (good!)")
        print(f"  If alpha > 0, the bound gets WORSE (need tighter analysis)")

    # Also fit |R| scaling
    valid_R = [(r['p'], r['|R|']) for r in results if r['|R|'] > 1e-10 and r['p'] >= 11]
    if len(valid_R) >= 3:
        log_p = np.array([log(x[0]) for x in valid_R])
        log_R = np.array([log(x[1]) for x in valid_R])
        coeffs = np.polyfit(log_p, log_R, 1)
        alpha_R = coeffs[0]
        A_R = np.exp(coeffs[1])
        print(f"\n|R| scaling fit: |R| ~ {A_R:.4f} * p^({alpha_R:.4f})")

    # Check C scaling
    valid_C = [(r['p'], r['best_C']) for r in results if r['best_C'] > 0 and r['p'] >= 11]
    if len(valid_C) >= 3:
        log_p = np.array([log(x[0]) for x in valid_C])
        log_C = np.array([log(x[1]) for x in valid_C])
        coeffs = np.polyfit(log_p, log_C, 1)
        alpha_C = coeffs[0]
        A_C = np.exp(coeffs[1])
        print(f"\nC scaling fit: C ~ {A_C:.4f} * p^({alpha_C:.4f})")

    return results


# ========================================================================
# PART 6: Improved bound using cancellation between denominators
# ========================================================================

def cancellation_analysis(p, verbose=True):
    """
    The naive bound sums |S_b|, losing cancellation between different b.
    Here we track the SIGNED sum and check if there's systematic cancellation.
    """
    N = p - 1
    farey_seq = build_farey_sequence(N)
    D_vals, n_farey = compute_D_values(farey_seq)
    D_rough = compute_D_rough(D_vals)
    farey_set = set(f for f in farey_seq)

    # Compute S_b for each b
    sb_values = []
    cumulative = 0.0
    total_delta_sq = 0.0

    for b in range(1, N + 1):
        S_b, count, dsq = compute_S_b(p, b, D_rough, farey_set)
        if count == 0:
            continue
        cumulative += S_b
        total_delta_sq += dsq
        sb_values.append((b, S_b, cumulative, dsq))

    if verbose:
        print(f"\n--- Cancellation analysis for p = {p} ---")
        print(f"{'b':>4} {'S_b':>12} {'cumulative':>14} {'|cumul|/dsq_total':>18}")
        for b, sb, cum, dsq in sb_values[:20]:
            r = abs(cum) / total_delta_sq if total_delta_sq > 0 else 0
            print(f"{b:>4} {sb:>12.6f} {cum:>14.6f} {r:>18.8f}")
        if len(sb_values) > 20:
            print(f"  ... ({len(sb_values)} denominators total)")

        # Final
        final_cum = sb_values[-1][2]
        print(f"\n  Final cumulative = {final_cum:.8f}")
        print(f"  Total delta^2 = {total_delta_sq:.8f}")
        print(f"  R = cumulative / delta^2 = {final_cum / total_delta_sq:.8f}")

        # How much cancellation?
        sum_abs = sum(abs(sb) for _, sb, _, _ in sb_values)
        print(f"  Sum |S_b| = {sum_abs:.8f}")
        print(f"  |Sum S_b| = {abs(final_cum):.8f}")
        print(f"  Cancellation factor: {sum_abs / abs(final_cum):.4f}x" if abs(final_cum) > 1e-12 else "  Perfect cancellation!")


# ========================================================================
# MAIN
# ========================================================================

if __name__ == '__main__':
    # Detailed analysis for specified primes using CANONICAL R definition
    detailed_primes = [13, 31, 97, 199]
    all_results = {}

    print("=" * 70)
    print("USING CANONICAL R(p) = 2 * Sum(D*delta) / Sum(delta^2)")
    print("=" * 70)

    for p in detailed_primes:
        res = analyze_prime(p, verbose=True, use_D_rough=False)
        all_results[p] = res
        cancellation_analysis(p, verbose=True)

    # Quick comparison with D_rough
    print("\n" + "=" * 70)
    print("COMPARISON: canonical D vs D_rough = D + 1/2")
    print("=" * 70)
    print(f"{'p':>5} {'R_canonical':>12} {'R_Drough':>12}")
    for p in detailed_primes:
        r_canon = analyze_prime(p, verbose=False, use_D_rough=False)
        r_rough = analyze_prime(p, verbose=False, use_D_rough=True)
        print(f"{p:>5} {r_canon['R']:>12.6f} {r_rough['R']:>12.6f}")

    # Scaling analysis
    scaling_results = scaling_analysis()

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY (canonical R)")
    print("=" * 70)

    print(f"\n{'p':>5} {'R':>10} {'|R|':>10} {'C_best':>10} {'bound_ratio':>12} {'proves |R|<1/2':>16}")
    for p in detailed_primes:
        r = all_results[p]
        print(f"{p:>5} {r['R']:>10.6f} {r['|R|']:>10.6f} {r['best_C']:>10.4f} {r['ratio_to_half']:>12.6f} {'YES' if r['proves_half'] else 'NO':>16}")

    print(f"\nKey findings:")
    print(f"  1. The per-denominator Weil bound |S_b| <= C*phi(b)*sqrt(b)/b")
    print(f"     has C growing as ~p^alpha. If alpha > 0, naive bound diverges.")
    print(f"  2. The bound_ratio = Sum|S_b|_bound / (1/2)*Sum(delta^2) tells us")
    print(f"     whether summing individual bounds suffices.")
    print(f"  3. If bound_ratio > 1 but actual |R| < 1/2, cancellation between")
    print(f"     denominators is essential and must be proven structurally.")

    total_time = time.time() - start_time
    print(f"\nTotal time: {total_time:.1f}s")
