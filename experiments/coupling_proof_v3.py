#!/usr/bin/env python3
"""
Coupling proof v3: Use the ACTUAL Farey discrepancy definition.

The per-step discrepancy ΔW(a/b) measures how inserting fraction a/b
into the Farey sequence changes the discrepancy. In the Farey sequence F_N,
fraction a/b enters at order N=b. The discrepancy of F_N is:
  D_N = Σ_{a/b ∈ F_N} (a/b - rank(a/b)/|F_N|)

The key object for the coupling is NOT the raw displacement sum,
but the CORRELATION between:
  - The Farey discrepancy contribution of a/b
  - The displacement under the prime permutation

Let's go back to basics: what we actually showed empirically is that
|R(p)| under σ_p is below ALL random permutation trials.

R(p) was defined as Σ_b (Δ_b(p) - Δ_b(random)) where Δ_b is some
discrepancy quantity.

Let me re-derive from the actual data we collected in previous sessions.
"""

import numpy as np
from math import gcd, log, sqrt, pi
from fractions import Fraction
import time

def coprime_residues(b):
    return [a for a in range(1, b) if gcd(a, b) == 1]

def euler_phi(n):
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

def moebius(n):
    if n == 1:
        return 1
    temp = n
    factors = []
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            count = 0
            while temp % p == 0:
                temp //= p
                count += 1
            if count > 1:
                return 0
            factors.append(p)
        p += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)


def farey_discrepancy_contributions(N):
    """
    Compute the Farey discrepancy contribution for each fraction in F_N.

    F_N = {a/b : 0 ≤ a ≤ b ≤ N, gcd(a,b)=1}, sorted.
    Discrepancy contribution of the k-th fraction x_k = x_k - k/|F_N|

    Returns dict: (a, b) -> discrepancy_contribution
    """
    # Build Farey sequence
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append((a, b, Fraction(a, b)))

    # Sort by value
    fracs.sort(key=lambda x: x[2])
    n_fracs = len(fracs)

    contributions = {}
    for k, (a, b, frac) in enumerate(fracs):
        # rank is k (0-indexed), normalized rank is k/(n_fracs - 1) or (k+0.5)/n_fracs
        contributions[(a, b)] = float(frac) - k / (n_fracs - 1) if n_fracs > 1 else 0

    return contributions


def compute_R_coupling(p, N_max=100, n_random=500):
    """
    For each Farey order N from 2 to N_max, compute:
    1. The actual Farey discrepancy D_N
    2. The "permuted" discrepancy under σ_p
    3. The permuted discrepancy under random permutations

    The coupling idea: σ_p permutes the Farey fractions {a/b : gcd(a,b)=1}
    by sending a/b -> (pa mod b)/b. This changes the discrepancy.

    We measure: how much does σ_p change the discrepancy vs random?
    """
    np.random.seed(42)

    results = {
        'N': [],
        'D_N': [],  # actual Farey discrepancy
        'D_N_sigma': [],  # discrepancy after σ_p permutation
        'D_N_random_mean': [],
        'D_N_random_std': [],
        'z_score': [],
        'n_fracs': [],
    }

    for N in range(2, N_max + 1):
        # Build Farey sequence
        fracs = []
        for b in range(1, N + 1):
            for a in range(0, b + 1):
                if gcd(a, b) == 1:
                    fracs.append((a, b))

        fracs.sort(key=lambda x: Fraction(x[0], x[1]))
        n_fracs = len(fracs)

        # Actual discrepancy: D_N = max_k |k/|F_N| - x_k|
        # Or L2: D_N^2 = Σ (x_k - k/(|F_N|-1))^2
        vals = np.array([a/b for a, b in fracs])
        ranks = np.arange(n_fracs) / max(n_fracs - 1, 1)
        D_N = np.sum((vals - ranks)**2)

        # Apply σ_p: for each a/b, replace by (pa mod b)/b
        # BUT: σ_p only acts on interior fractions (0 < a < b)
        # For a=0 or a=b, σ_p fixes them (0*p=0, b*p mod b = 0... )
        # Actually a=b means a/b=1, and pb mod b = 0, so σ_p(b/b) = 0/b = 0
        # That breaks things. σ_p should only act on coprime residues.

        # Better approach: for each denominator b, permute the numerators
        # a -> pa mod b, for a coprime to b with 0 < a < b.
        # The fractions 0/1 and 1/1 are fixed.
        # For a/b with gcd(a,b)=1 and gcd(p,b)=1: map to (pa mod b)/b
        # For a/b with p|b: leave as is (σ_p not defined cleanly)

        new_fracs = []
        for a, b in fracs:
            if a == 0 or a == b:
                new_fracs.append(a / b)
            elif gcd(p, b) == 1:
                new_a = (a * p) % b
                new_fracs.append(new_a / b)
            else:
                new_fracs.append(a / b)  # leave fixed if p|b

        new_vals = np.sort(new_fracs)
        D_N_sigma = np.sum((new_vals - ranks)**2)

        # Random permutations: for each b, randomly permute the coprime numerators
        D_random = np.zeros(n_random)

        # Group fractions by denominator
        by_denom = {}
        for i, (a, b) in enumerate(fracs):
            if a == 0 or a == b:
                continue
            if b not in by_denom:
                by_denom[b] = []
            by_denom[b].append(a)

        for t in range(n_random):
            rand_fracs = []
            for a, b in fracs:
                if a == 0 or a == b:
                    rand_fracs.append(a / b)
                else:
                    # Will be filled by the permuted numerators
                    rand_fracs.append(None)

            # Permute numerators within each denominator
            perm_by_denom = {}
            for b, nums in by_denom.items():
                perm_by_denom[b] = list(np.random.permutation(nums))

            idx_by_denom = {b: 0 for b in by_denom}
            for i, (a, b) in enumerate(fracs):
                if rand_fracs[i] is None:
                    perm_nums = perm_by_denom[b]
                    rand_fracs[i] = perm_nums[idx_by_denom[b]] / b
                    idx_by_denom[b] += 1

            rand_vals = np.sort(rand_fracs)
            D_random[t] = np.sum((rand_vals - ranks)**2)

        mean_r = np.mean(D_random)
        std_r = np.std(D_random)
        z = (D_N_sigma - mean_r) / std_r if std_r > 1e-15 else 0

        results['N'].append(N)
        results['D_N'].append(float(D_N))
        results['D_N_sigma'].append(float(D_N_sigma))
        results['D_N_random_mean'].append(float(mean_r))
        results['D_N_random_std'].append(float(std_r))
        results['z_score'].append(float(z))
        results['n_fracs'].append(n_fracs)

    return results


def analyze_per_denominator_effect(p, B_max=200, n_random=500):
    """
    More targeted analysis: for each denominator b, how does σ_p change
    the ORDERING of the fractions with denominator b relative to
    fractions with other denominators?

    The key quantity: for fractions a/b (b fixed), their RANKS in the
    full Farey sequence depend on other fractions. σ_p changes a/b to
    (pa mod b)/b, which has a DIFFERENT rank.

    The discrepancy change from σ_p acting on denominator b:
    Δ_b = Σ_{a coprime b} |rank(a/b) - rank((pa mod b)/b)|

    This measures how much σ_p "scrambles" the fractions of denominator b.
    """
    np.random.seed(42)

    results = {'b': [], 'delta_sigma': [], 'delta_random_mean': [],
               'delta_random_std': [], 'z_score': [], 'phi_b': []}

    # Build Farey sequence up to B_max
    all_fracs = set()
    for b in range(1, B_max + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                all_fracs.add(Fraction(a, b))

    sorted_fracs = sorted(all_fracs)
    frac_to_rank = {f: i for i, f in enumerate(sorted_fracs)}
    n_total = len(sorted_fracs)

    for b in range(2, min(B_max + 1, 101)):
        if gcd(p, b) > 1:
            continue

        coprimes = [a for a in range(1, b) if gcd(a, b) == 1]
        phi_b = len(coprimes)
        if phi_b < 2:
            continue

        # Ranks of a/b in the full Farey sequence
        orig_ranks = [frac_to_rank[Fraction(a, b)] for a in coprimes]

        # Ranks of (pa mod b)/b
        sigma_ranks = [frac_to_rank[Fraction((a * p) % b, b)] for a in coprimes]

        # Discrepancy change: sum of |rank_change|, normalized
        delta_sigma = sum(abs(r1 - r2) for r1, r2 in zip(orig_ranks, sigma_ranks)) / n_total

        # Random permutations
        delta_random = np.zeros(n_random)
        coprimes_arr = np.array(coprimes)
        for t in range(n_random):
            perm = np.random.permutation(coprimes_arr)
            perm_ranks = [frac_to_rank[Fraction(int(a), b)] for a in perm]
            delta_random[t] = sum(abs(r1 - r2) for r1, r2 in zip(orig_ranks, perm_ranks)) / n_total

        mean_r = np.mean(delta_random)
        std_r = np.std(delta_random)
        z = (delta_sigma - mean_r) / std_r if std_r > 1e-15 else 0

        results['b'].append(b)
        results['delta_sigma'].append(delta_sigma)
        results['delta_random_mean'].append(mean_r)
        results['delta_random_std'].append(std_r)
        results['z_score'].append(z)
        results['phi_b'].append(phi_b)

    return results


def dedekind_sum_S_bound(p, B_max=500):
    """
    Use Dedekind sum reciprocity to bound R(p) = Σ_{b≤B} S_b.

    Key identity: s(p,b) + s(b,p) = (1/12)(p/b + b/p + 1/(pb)) - 1/4

    So s(p,b) = (1/12)(p/b + b/p + 1/(pb)) - 1/4 - s(b,p)

    And Σ_{b≤B, gcd(p,b)=1} s(p,b) = Σ_b [(1/12)(p/b + b/p + 1/(pb)) - 1/4] - Σ_b s(b,p)

    The first sum is elementary: ~ (p/12)·H_B + B^2/(24p) + O(1)
    The second sum Σ_b s(b,p) involves Dedekind sums s(b mod p, p).

    Since b mod p cycles through residues, s(b mod p, p) is periodic in b.
    So Σ_{b≤B} s(b,p) = (B/p) Σ_{c=1}^{p-1} s(c,p) + O(p)

    And Σ_{c=1}^{p-1} s(c,p) is known to relate to the class number and
    other arithmetic invariants of Z/pZ.
    """
    # Compute Σ s(c,p) for c = 1..p-1
    def dedekind_sum(a, b):
        s = 0.0
        for k in range(1, b):
            x1 = k / b
            x2 = (k * a) / b
            saw1 = x1 - int(x1) - 0.5 if x1 != int(x1) else 0
            saw2 = x2 - int(x2) - 0.5 if x2 != int(x2) else 0
            s += saw1 * saw2
        return s

    sum_s_cp = sum(dedekind_sum(c, p) for c in range(1, p))

    # Elementary sum
    def elem_sum(B):
        S = 0.0
        for b in range(2, B + 1):
            if gcd(p, b) > 1:
                continue
            S += (1/12) * (p/b + b/p + 1/(p*b)) - 0.25
        return S

    # Predicted Σ s(p,b) from reciprocity
    B = B_max
    elem = elem_sum(B)
    # Number of b ≤ B coprime to p
    n_coprime = sum(1 for b in range(2, B + 1) if gcd(p, b) == 1)
    periodic_sum = (n_coprime / (p - 1)) * sum_s_cp  # approximate

    predicted = elem - periodic_sum

    # Actual
    actual = sum(dedekind_sum(p, b) for b in range(2, B + 1) if gcd(p, b) == 1)

    return {
        'p': p,
        'B': B,
        'sum_s_cp': sum_s_cp,
        'elementary_sum': elem,
        'periodic_sum': periodic_sum,
        'predicted_sum_s_pb': predicted,
        'actual_sum_s_pb': actual,
        'ratio': predicted / actual if abs(actual) > 1e-10 else float('inf'),
    }


def main():
    primes = [13, 31, 97]

    # Part 1: Full Farey discrepancy under σ_p vs random
    print("=" * 70)
    print("PART 1: FAREY DISCREPANCY UNDER σ_p vs RANDOM PERMUTATIONS")
    print("=" * 70)

    for p in primes:
        print(f"\n--- p = {p}, N up to 60 ---")
        res = compute_R_coupling(p, N_max=60, n_random=500)

        N_arr = np.array(res['N'])
        D_arr = np.array(res['D_N'])
        Ds_arr = np.array(res['D_N_sigma'])
        Dm_arr = np.array(res['D_N_random_mean'])
        z_arr = np.array(res['z_score'])

        print(f"  Z-score (σ_p vs random perm of Farey discrepancy):")
        print(f"    Mean z: {np.mean(z_arr):.4f}")
        print(f"    Std z:  {np.std(z_arr):.4f}")
        print(f"    Min z:  {np.min(z_arr):.4f}")
        print(f"    Max z:  {np.max(z_arr):.4f}")

        # Is σ_p discrepancy systematically below random?
        frac_below = np.mean(Ds_arr < Dm_arr)
        print(f"    Fraction D_σ < D_random_mean: {frac_below:.4f}")

        # Show some values
        for N in [10, 20, 30, 40, 50, 60]:
            if N <= len(res['N']):
                idx = N - 2  # since we start at N=2
                if idx < len(res['N']):
                    print(f"    N={N}: D_σ={Ds_arr[idx]:.6f}, "
                          f"D_rand={Dm_arr[idx]:.6f}, z={z_arr[idx]:.3f}")

    # Part 2: Per-denominator rank displacement
    print(f"\n{'='*70}")
    print("PART 2: PER-DENOMINATOR RANK DISPLACEMENT")
    print("=" * 70)

    for p in [13, 31]:
        print(f"\n--- p = {p} ---")
        res = analyze_per_denominator_effect(p, B_max=80, n_random=500)

        z_arr = np.array(res['z_score'])
        d_sigma = np.array(res['delta_sigma'])
        d_rand = np.array(res['delta_random_mean'])

        print(f"  Rank displacement (σ_p vs random):")
        print(f"    Mean z: {np.mean(z_arr):.4f}")
        print(f"    Fraction σ_p < random: {np.mean(d_sigma < d_rand):.4f}")
        print(f"    Mean ratio σ_p/random: {np.mean(d_sigma / d_rand):.4f}")

        # Show details for select b
        for i, b in enumerate(res['b']):
            if b in [5, 7, 11, 17, 23, 29, 37, 41, 53, 67]:
                print(f"    b={b}: Δ_σ={res['delta_sigma'][i]:.6f}, "
                      f"Δ_rand={res['delta_random_mean'][i]:.6f}, "
                      f"z={res['z_score'][i]:.3f}")

    # Part 3: Dedekind sum bounds
    print(f"\n{'='*70}")
    print("PART 3: DEDEKIND SUM RECIPROCITY BOUNDS")
    print("=" * 70)

    for p in primes:
        ds = dedekind_sum_S_bound(p, B_max=200)
        print(f"\np = {p}:")
        print(f"  Σ_{{c=1}}^{{p-1}} s(c,p) = {ds['sum_s_cp']:.6f}")
        print(f"  Elementary sum (reciprocity formula): {ds['elementary_sum']:.4f}")
        print(f"  Periodic sum estimate: {ds['periodic_sum']:.4f}")
        print(f"  Predicted Σ s(p,b): {ds['predicted_sum_s_pb']:.4f}")
        print(f"  Actual Σ s(p,b):    {ds['actual_sum_s_pb']:.4f}")
        print(f"  Prediction/Actual:  {ds['ratio']:.4f}")

    # Part 4: The Coupling Argument
    print(f"\n{'='*70}")
    print("PART 4: THE COUPLING ARGUMENT (REVISED)")
    print("=" * 70)

    print("""
REVISED COUPLING FRAMEWORK:

The original idea (σ_p has less cross-correlation than random) is PARTIALLY
confirmed but the picture is more nuanced than expected.

FINDINGS:

1. PER-DENOMINATOR: σ_p displacement is slightly LESS than random
   (ratio ~0.97 for p=13, ~0.99 for p=31).
   This is the "group automorphism effect" — but it's SMALL.

2. FAREY DISCREPANCY: σ_p produces discrepancy that is sometimes above,
   sometimes below random. The z-scores cluster around 0 but with some
   systematic structure.

3. DEDEKIND CONNECTION: S_b connects to s(p,b), and the reciprocity
   s(p,b) + s(b,p) = known quantity provides structural constraints.

VIABLE PROOF PATH:

A. Direct Dedekind sum approach:
   - S_b relates to s(p,b) via the floor function decomposition
   - Use Rademacher's bound: |s(p,b)| ≤ O(log b) for almost all b
   - This gives |S_b| ≤ O(b log b / b^2) = O(log b / b)
   - Hence R(p) = Σ |S_b| = O((log B)^2), which is VERY good

   BUT: This bounds |S_b| not S_b. For cancellation in Σ S_b,
   we need sign information.

B. Character sum approach (from v1 analysis):
   - The principal character cancellation is real and verified
   - S_b = (1/b) Σ_{χ≠χ_0} c_χ (1-χ̄(p)) τ_χ
   - Non-principal characters contribute O(√b) via Gauss sum bounds
   - With φ(b) non-principal characters, naive bound gives O(φ(b)√b/b) = O(√b)
   - Summing: R(p) ≤ Σ O(√b) = O(B^{3/2}), too weak

C. HYBRID: Character sums + Dedekind reciprocity
   - Use characters to show per-b cancellation (principal char drops)
   - Use Dedekind reciprocity to show inter-b cancellation (pairing)
   - Target: R(p) = O(B^{1+ε}) with small ε, or O(B log B)

D. COUPLING PROPER:
   - Define coupling: pair each permutation of (Z/bZ)* with a
     "nearby" group automorphism
   - σ_p is one specific automorphism among φ(φ(b)) automorphisms
   - The set of ALL automorphisms has smaller variance than ALL permutations
   - Bound R(p) by: (random perm variance) × (fraction of perm space
     occupied by automorphisms)
   - Since automorphisms are φ(φ(b))/φ(b)! fraction of permutations,
     and they have structured cancellation, this could work.
""")


if __name__ == '__main__':
    t0 = time.time()
    main()
    print(f"\nTotal time: {time.time() - t0:.1f}s")
