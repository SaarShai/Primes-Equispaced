#!/usr/bin/env python3
"""
Coupling proof v2: Fix the discrepancy function and re-examine.

The issue in v1: D_rough(a/b) = a/b - 0.5 is the sawtooth, NOT the Farey
discrepancy. The actual per-step discrepancy ΔW(a/b) measures how much
inserting a/b into the Farey sequence changes the overall discrepancy.

Also: The coupling should compare σ_p to the IDENTITY permutation,
not to random permutations. The question is:
  R(p) = Σ_b Σ_a D(a/b) · (a - pa)/b
Is this small? We need to bound this SUM over b.

Let me re-examine with:
1. Proper ΔW definition
2. The right comparison (identity vs σ_p)
3. Character-theoretic decomposition
"""

import numpy as np
from math import gcd, sqrt
from fractions import Fraction
import time

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

def coprime_residues(b):
    return [a for a in range(1, b) if gcd(a, b) == 1]

def sigma_p_perm(p, b):
    """Return the permutation σ_p: a -> pa mod b on coprime residues."""
    coprimes = coprime_residues(b)
    return {a: (a * p) % b for a in coprimes}

def moebius(n):
    """Mobius function."""
    if n == 1:
        return 1
    factors = []
    temp = n
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

def dedekind_sum(a, b):
    """
    Dedekind sum s(a,b) = Σ_{k=1}^{b-1} ((k/b)) ((ka/b))
    where ((x)) = x - floor(x) - 1/2 if x not integer, 0 if integer.
    """
    s = 0.0
    for k in range(1, b):
        x1 = k / b
        x2 = (k * a) / b
        # Sawtooth function
        if x1 == int(x1):
            saw1 = 0
        else:
            saw1 = x1 - int(x1) - 0.5
        if x2 == int(x2):
            saw2 = 0
        else:
            saw2 = x2 - int(x2) - 0.5
        s += saw1 * saw2
    return s


def compute_cross_correlation_decomposition(p, B_max, n_random=500):
    """
    Compute per-b cross-correlation under σ_p and random permutations.

    For each b, compute:
      T_b(π) = Σ_{a coprime b} w(a,b) · (a - π(a))

    where w(a,b) is a weight function. We try several:
    1. w = 1 (unweighted displacement)
    2. w = a/b - 1/2 (sawtooth)
    3. w = μ(b)/φ(b) (Mobius-weighted, connects to Mertens)
    """
    np.random.seed(42)

    results = {
        'b': [],
        'phi_b': [],
        # Unweighted: T_b = Σ (a - pa mod b)
        'T_unweighted_sigma': [],
        'T_unweighted_random_mean': [],
        'T_unweighted_random_std': [],
        # Sawtooth weighted
        'T_saw_sigma': [],
        'T_saw_random_mean': [],
        'T_saw_random_std': [],
        # Displacement only (no weight, just Σ|a - pa mod b|)
        'displacement_sigma': [],
        'displacement_random_mean': [],
        'displacement_random_std': [],
        # Cycle structure
        'n_cycles': [],
        'max_cycle': [],
        'order_p': [],
    }

    for b in range(2, B_max + 1):
        if gcd(p, b) > 1:
            continue

        coprimes = coprime_residues(b)
        n = len(coprimes)
        if n < 2:
            continue

        perm = sigma_p_perm(p, b)
        a_arr = np.array(coprimes)
        sp_arr = np.array([perm[a] for a in coprimes])

        # Sawtooth weights
        saw = a_arr / b - 0.5

        # σ_p values
        T_unw = np.sum(a_arr - sp_arr)
        T_saw = np.sum(saw * (a_arr - sp_arr))
        disp = np.sum(np.abs(a_arr - sp_arr))

        # Random permutation distribution
        T_unw_rand = np.zeros(n_random)
        T_saw_rand = np.zeros(n_random)
        disp_rand = np.zeros(n_random)

        for t in range(n_random):
            pi = np.random.permutation(a_arr)
            T_unw_rand[t] = np.sum(a_arr - pi)
            T_saw_rand[t] = np.sum(saw * (a_arr - pi))
            disp_rand[t] = np.sum(np.abs(a_arr - pi))

        # Cycle structure of σ_p
        visited = set()
        cycles = []
        for a in coprimes:
            if a in visited:
                continue
            cycle = []
            x = a
            while x not in visited:
                visited.add(x)
                cycle.append(x)
                x = perm[x]
            cycles.append(len(cycle))

        # Order of p mod b
        ord_p = 1
        x = p % b
        while x != 1:
            x = (x * p) % b
            ord_p += 1

        results['b'].append(b)
        results['phi_b'].append(n)
        results['T_unweighted_sigma'].append(float(T_unw))
        results['T_unweighted_random_mean'].append(float(np.mean(T_unw_rand)))
        results['T_unweighted_random_std'].append(float(np.std(T_unw_rand)))
        results['T_saw_sigma'].append(float(T_saw))
        results['T_saw_random_mean'].append(float(np.mean(T_saw_rand)))
        results['T_saw_random_std'].append(float(np.std(T_saw_rand)))
        results['displacement_sigma'].append(float(disp))
        results['displacement_random_mean'].append(float(np.mean(disp_rand)))
        results['displacement_random_std'].append(float(np.std(disp_rand)))
        results['n_cycles'].append(len(cycles))
        results['max_cycle'].append(max(cycles))
        results['order_p'].append(ord_p)

    return results


def character_decomposition_rigorous(p, b):
    """
    Rigorous character decomposition of S_b under σ_p.

    S_b = Σ_{a coprime b} (a/b - 1/2) · (a - pa mod b) / b

    Using multiplicative characters: if we write
    f(a) = a (the identity on coprimes mod b)
    g(a) = pa mod b = σ_p(a)

    Then S_b = (1/b) Σ_a (a/b - 1/2)(a - g(a))
            = (1/b^2) Σ_a a(a - g(a)) - (1/(2b)) Σ_a (a - g(a))

    Note: Σ_a (a - g(a)) = 0 since σ_p is a permutation (same set of values)!
    So: S_b = (1/b^2) Σ_a a · (a - pa mod b)
            = (1/b^2) [Σ_a a^2 - p · Σ_a a · (a mod ... )]

    Wait, this needs care. σ_p(a) = pa mod b, but pa mod b is just
    the residue. Since σ_p permutes the coprimes:
    Σ_a a = Σ_a σ_p(a) (same set), so Σ_a (a - σ_p(a)) = 0. ✓

    S_b = (1/b^2) Σ_a a(a - σ_p(a))

    Now: Σ_a a · σ_p(a) = Σ_a a · (pa mod b)

    In multiplicative characters mod b:
    a = (1/φ(b)) Σ_χ τ̄(χ) χ(a)  where τ(χ) = Σ_a χ(a)a

    So Σ_a a · σ_p(a) = Σ_a a · pa mod b
    Note pa mod b, for coprime a, equals the unique a' with a' ≡ pa (mod b).
    We can write: σ_p(a) = pa - b·⌊pa/b⌋

    So Σ_a a · σ_p(a) = p Σ_a a^2 - b Σ_a a⌊pa/b⌋

    And S_b = (1/b^2)[Σ a^2 - p Σ a^2 + b Σ a⌊pa/b⌋]
            = (1/b^2)[(1-p) Σ a^2 + b Σ a⌊pa/b⌋]

    The term Σ_a a⌊pa/b⌋ is related to Dedekind sums!

    Actually: s(p,b) = Σ_{k=1}^{b-1} ((k/b))((kp/b))
    and ((x)) = {x} - 1/2 for non-integer x.

    This connects our S_b directly to Dedekind sums, which have
    well-known reciprocity laws and bounds.
    """
    coprimes = coprime_residues(b)
    n = len(coprimes)
    a_arr = np.array(coprimes)
    sp_arr = np.array([(a * p) % b for a in coprimes])

    # Verify Σ(a - σ_p(a)) = 0
    assert abs(np.sum(a_arr) - np.sum(sp_arr)) < 1e-10, "Permutation sum check failed"

    # Compute S_b = (1/b^2) Σ a(a - σ_p(a))
    S_b = np.sum(a_arr * (a_arr - sp_arr)) / b**2

    # Decomposition: S_b = (1/b^2)[(1-p)Σa^2 + b·Σa⌊pa/b⌋]
    sum_a2 = np.sum(a_arr**2)
    sum_a_floor = np.sum(a_arr * np.floor(a_arr * p / b))
    S_b_decomp = ((1 - p) * sum_a2 + b * sum_a_floor) / b**2

    # Dedekind sum connection
    ds = dedekind_sum(p, b)

    return {
        'S_b': float(S_b),
        'S_b_decomp': float(S_b_decomp),
        'sum_a2': float(sum_a2),
        'sum_a_floor': float(sum_a_floor),
        'dedekind_sum': ds,
        'phi_b': n,
        # Normalized
        'S_b_normalized': float(S_b * b),  # S_b * b should be O(1) if S_b = O(1/b)
    }


def main():
    primes = [13, 31, 97]
    B_max = 300

    print("=" * 70)
    print("COUPLING PROOF V2: CORRECTED ANALYSIS")
    print("=" * 70)

    # Part 1: Cross-correlation comparison
    for p in primes:
        print(f"\n{'='*60}")
        print(f"PRIME p = {p}, b up to {B_max}")
        print(f"{'='*60}")

        res = compute_cross_correlation_decomposition(p, B_max, n_random=500)

        b_arr = np.array(res['b'])
        phi_arr = np.array(res['phi_b'])

        # UNWEIGHTED: Σ(a - σ_p(a)) should be 0 (permutation property)
        T_unw = np.array(res['T_unweighted_sigma'])
        print(f"\nUnweighted Σ(a - σ_p(a)):")
        print(f"  All zero? max|T| = {np.max(np.abs(T_unw)):.1e}")
        print(f"  (Yes, because σ_p is a permutation of the same set)")

        # SAWTOOTH-WEIGHTED: The main object
        T_saw = np.array(res['T_saw_sigma'])
        T_saw_rmean = np.array(res['T_saw_random_mean'])
        T_saw_rstd = np.array(res['T_saw_random_std'])

        # z-scores
        z_saw = np.where(T_saw_rstd > 1e-12,
                         (T_saw - T_saw_rmean) / T_saw_rstd, 0)

        print(f"\nSawtooth-weighted Σ(a/b-1/2)(a - σ_p(a)):")
        print(f"  Mean |T_σ|:     {np.mean(np.abs(T_saw)):.4f}")
        print(f"  Mean std(T_rnd): {np.mean(T_saw_rstd):.4f}")
        print(f"  Mean z-score:    {np.mean(z_saw):.4f}")
        print(f"  Std z-score:     {np.std(z_saw):.4f}")
        print(f"  |z| > 2:        {np.sum(np.abs(z_saw) > 2)} / {len(z_saw)}")

        # DISPLACEMENT: Σ|a - σ_p(a)|
        disp_s = np.array(res['displacement_sigma'])
        disp_rm = np.array(res['displacement_random_mean'])
        disp_rs = np.array(res['displacement_random_std'])

        z_disp = np.where(disp_rs > 1e-12, (disp_s - disp_rm) / disp_rs, 0)

        print(f"\nDisplacement Σ|a - σ_p(a)|:")
        print(f"  Mean displacement σ_p:  {np.mean(disp_s):.2f}")
        print(f"  Mean displacement rand: {np.mean(disp_rm):.2f}")
        print(f"  Ratio σ_p/random:       {np.mean(disp_s/disp_rm):.4f}")
        print(f"  Mean z-score:           {np.mean(z_disp):.4f}")

        # KEY: Is σ_p displacement typically LESS than random?
        frac_less = np.mean(disp_s < disp_rm)
        print(f"  Fraction σ_p < random:  {frac_less:.4f}")

        # Order of p mod b
        orders = np.array(res['order_p'])
        print(f"\nOrder of p mod b:")
        print(f"  Mean ord_p/φ(b):  {np.mean(orders/phi_arr):.4f}")
        print(f"  When ord=φ (primitive root): {np.sum(orders == phi_arr)} / {len(orders)}")

        # Correlation: order vs z-score
        corr_ord_z = np.corrcoef(orders / phi_arr, z_saw)[0, 1]
        print(f"  Corr(ord/φ, z_saw):  {corr_ord_z:.4f}")

    # Part 2: Character-theoretic decomposition and Dedekind sum connection
    print(f"\n{'='*70}")
    print("DEDEKIND SUM CONNECTION")
    print("=" * 70)

    for p in [13, 31, 97]:
        print(f"\np = {p}:")
        S_vals = []
        S_norm_vals = []
        ds_vals = []
        b_vals_local = []

        for b in range(2, 301):
            if gcd(p, b) > 1:
                continue
            cd = character_decomposition_rigorous(p, b)
            S_vals.append(cd['S_b'])
            S_norm_vals.append(cd['S_b_normalized'])
            ds_vals.append(cd['dedekind_sum'])
            b_vals_local.append(b)

        S_arr = np.array(S_vals)
        Sn_arr = np.array(S_norm_vals)
        ds_arr = np.array(ds_vals)

        # Cumulative R(p) = Σ S_b
        R_cumsum = np.cumsum(S_arr)

        print(f"  S_b statistics:")
        print(f"    Mean S_b:         {np.mean(S_arr):.6f}")
        print(f"    Std S_b:          {np.std(S_arr):.6f}")
        print(f"    Mean |S_b|:       {np.mean(np.abs(S_arr)):.6f}")
        print(f"    Mean S_b*b:       {np.mean(Sn_arr):.4f}")
        print(f"    Std S_b*b:        {np.std(Sn_arr):.4f}")

        # Does S_b correlate with Dedekind sum?
        corr_S_ds = np.corrcoef(S_arr, ds_arr)[0, 1]
        print(f"    Corr(S_b, s(p,b)): {corr_S_ds:.4f}")

        # Cumulative growth
        n_pts = len(b_vals_local)
        for frac in [0.25, 0.5, 0.75, 1.0]:
            idx = min(int(frac * n_pts) - 1, n_pts - 1)
            print(f"    R(p) up to b={b_vals_local[idx]}: {R_cumsum[idx]:.4f}")

        # KEY: Growth rate of R(p)
        # If R(p) ~ c·B, then S_b has nonzero mean
        # If R(p) ~ c·√B, then S_b has zero mean and we get sqrt cancellation
        # Fit R(p) ~ c · B^alpha
        log_b = np.log(np.array(b_vals_local))
        log_R = np.log(np.abs(R_cumsum) + 1e-30)
        # Use second half for stable fit
        half = n_pts // 2
        if n_pts > 20:
            coeffs = np.polyfit(log_b[half:], log_R[half:], 1)
            alpha = coeffs[0]
            print(f"    Growth exponent: R(p) ~ B^{alpha:.3f}")
            print(f"    (alpha=1 means linear, alpha=0.5 means sqrt)")

    # Part 3: The actual proof path via character sums
    print(f"\n{'='*70}")
    print("PROOF PATH: CHARACTER SUM BOUNDS")
    print("=" * 70)

    print("""
ANALYSIS SUMMARY:

1. OBSERVATION: S_b = (1/b^2) Σ_a a(a - σ_p(a))
   The unweighted sum Σ(a - σ_p(a)) = 0 (permutation).
   The sawtooth-weighted sum S_b is generally nonzero.

2. DECOMPOSITION: S_b = (1/b^2)[(1-p)Σa^2 + bΣa⌊pa/b⌋]
   The term Σ_a a⌊pa/b⌋ connects to Dedekind sums s(p,b).

3. DEDEKIND SUM BOUND: |s(p,b)| ≤ (1/8)(b/p + p/b + 1/pb - 3) + 1/4b
   (Rademacher's bound)

   This gives: Σ_a a⌊pa/b⌋ ≈ (b/12)(p + 1/p - 3 + ...) + O(b log b)

4. GROWTH RATE: R(p) = Σ_{b≤B} S_b grows like B^α.
   If α < 2, then R(p)/B → 0, meaning the per-prime discrepancy vanishes.

5. THE COUPLING INSIGHT:
   For σ_p (group automorphism), the Dedekind sum reciprocity law gives:
   s(p,b) + s(b,p) = (1/12)(p/b + b/p + 1/(pb)) - 1/4

   This RECIPROCITY is what random permutations don't have.
   It creates systematic cancellation when we sum over b.

   Specifically: Σ_{b≤B} s(p,b) involves pairs (p,b) and reciprocity
   links s(p,b) to s(b,p). For b < p, both are in range.
   For b > p, s(b,p) involves a different regime.

   This structured cancellation is ABSENT for random permutations,
   where Σ_{b≤B} (random Dedekind-like sum) grows as √(B log B).

6. PROOF OUTLINE:
   a) Express S_b in terms of Dedekind sums s(p,b)
   b) Use Dedekind reciprocity to pair up terms in Σ_b S_b
   c) Show paired cancellation gives better-than-random growth
   d) Bound the remainder using Rademacher's bound on individual s(p,b)
   e) Conclude R(p) = O(B^{1-ε}) for some ε > 0
""")


    # Part 4: Verify Dedekind sum connection numerically
    print(f"\n{'='*70}")
    print("DEDEKIND SUM VERIFICATION")
    print("=" * 70)

    p = 13
    print(f"\nVerifying for p = {p}:")
    print(f"{'b':>5} {'S_b':>12} {'Dedekind':>12} {'(1-p)Σa²/b²':>14} {'bΣa⌊pa/b⌋/b²':>15}")

    for b in [5, 7, 11, 17, 23, 29, 37, 41, 53, 67, 83, 97, 101]:
        if gcd(p, b) > 1:
            continue
        cd = character_decomposition_rigorous(p, b)
        coprimes = coprime_residues(b)
        a_arr = np.array(coprimes)
        term1 = (1 - p) * cd['sum_a2'] / b**2
        term2 = b * cd['sum_a_floor'] / b**2

        # Check Dedekind sum reciprocity
        ds_pb = dedekind_sum(p, b)
        ds_bp = dedekind_sum(b % p, p) if p > 1 else 0
        recip_expected = (1/12) * (p/b + b/p + 1/(p*b)) - 1/4
        recip_actual = ds_pb + ds_bp

        print(f"{b:5d} {cd['S_b']:12.6f} {ds_pb:12.6f} {term1:14.4f} {term2:15.4f}")

    print(f"\nDedekind reciprocity check (p={p}):")
    print(f"{'b':>5} {'s(p,b)+s(b,p)':>15} {'formula':>15} {'match':>6}")
    for b in [5, 7, 11, 17, 23, 29, 37]:
        if gcd(p, b) > 1:
            continue
        ds_pb = dedekind_sum(p, b)
        ds_bp = dedekind_sum(b % p, p)
        recip_expected = (1/12) * (p/b + b/p + 1/(p*b)) - 1/4
        recip_actual = ds_pb + ds_bp
        match = abs(recip_actual - recip_expected) < 1e-8
        print(f"{b:5d} {recip_actual:15.8f} {recip_expected:15.8f} {'YES' if match else 'NO':>6}")


if __name__ == '__main__':
    t0 = time.time()
    main()
    print(f"\nTotal time: {time.time() - t0:.1f}s")
