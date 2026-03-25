#!/usr/bin/env python3
"""
Voronoi Entropy Monotonicity for Farey Sequences
=================================================

Investigation of the conjecture:
    H(F_N) < H(F_{N+1})  for all N >= 2

where H is the Shannon entropy of the arc-length distribution when
fractions in F_N are placed on the circle [0,1).

Key questions:
1. Extend verification to N = 1000
2. WHY should entropy increase?
3. Can we prove it?
4. Connection to wobble W(N)
5. Is this known in the literature?

Author: Claude (Opus 4.6)
Date: 2026-03-24
"""

import sys
import time
from math import gcd, log, sqrt
from fractions import Fraction
from collections import defaultdict
import bisect

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or (n + 2) % i == 0: return False
        i += 6
    return True

def euler_totient(n):
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

def binary_entropy(t):
    """Binary entropy h(t) = -t*log(t) - (1-t)*log(1-t)"""
    if t <= 0 or t >= 1:
        return 0.0
    return -t * log(t) - (1 - t) * log(1 - t)


# ---------------------------------------------------------------------------
# Fast Farey entropy computation using floats
# ---------------------------------------------------------------------------

def compute_entropy_from_sorted(sorted_fracs_float):
    """
    Compute Shannon entropy of arc-length distribution on the circle.
    sorted_fracs_float: sorted list of floats in [0, 1), no duplicates.
    """
    n = len(sorted_fracs_float)
    if n < 2:
        return 0.0
    H = 0.0
    for i in range(n - 1):
        w = sorted_fracs_float[i + 1] - sorted_fracs_float[i]
        if w > 0:
            H -= w * log(w)
    # Wraparound arc
    w = 1.0 - sorted_fracs_float[-1] + sorted_fracs_float[0]
    if w > 0:
        H -= w * log(w)
    return H


# ---------------------------------------------------------------------------
# PART 1: Extend verification to N = 1000
# ---------------------------------------------------------------------------

def verify_monotonicity(N_max=1000):
    """
    Verify that H(F_N) is strictly increasing for N = 2, ..., N_max.
    Uses floats for speed. Returns detailed results.
    """
    print(f"{'=' * 70}")
    print(f"PART 1: Verify entropy monotonicity for N = 2 to {N_max}")
    print(f"{'=' * 70}")

    # Build Farey sequence incrementally using a sorted list of floats
    # F_N on circle [0,1): contains a/b for all b <= N, gcd(a,b)=1, 0 <= a/b < 1
    # Note: 0/1 is included, 1/1 is NOT (it's the same as 0 on the circle)
    sorted_fracs = [0.0]  # F_1 = {0/1} on circle (1/1 = 0)

    entropies = {}
    violations = []
    min_increase = float('inf')
    min_increase_N = 0

    start = time.time()
    prev_H = None
    results_for_output = []

    for N in range(2, N_max + 1):
        # Add fractions a/N with gcd(a, N) = 1, 0 < a/N < 1
        new_fracs = []
        for a in range(1, N):
            if gcd(a, N) == 1:
                new_fracs.append(a / N)

        # Insert into sorted list
        for f in new_fracs:
            bisect.insort(sorted_fracs, f)

        H = compute_entropy_from_sorted(sorted_fracs)
        entropies[N] = H
        phi_N = euler_totient(N)

        if prev_H is not None:
            delta_H = H - prev_H
            if delta_H <= 0:
                violations.append((N, delta_H, phi_N, is_prime(N)))
                print(f"  *** VIOLATION at N={N}: delta_H = {delta_H:.15e}, "
                      f"phi(N)={phi_N}, prime={is_prime(N)}")
            else:
                if delta_H < min_increase:
                    min_increase = delta_H
                    min_increase_N = N

            results_for_output.append({
                'N': N, 'H': H, 'delta_H': delta_H,
                'phi_N': phi_N, 'F_N_size': len(sorted_fracs),
                'is_prime': is_prime(N)
            })

        prev_H = H

        # Progress
        if N % 100 == 0:
            elapsed = time.time() - start
            print(f"  N = {N:4d}, H = {H:.10f}, |F_N| = {len(sorted_fracs):6d}, "
                  f"elapsed = {elapsed:.1f}s")

    elapsed = time.time() - start
    print(f"\n  Completed in {elapsed:.1f}s")
    print(f"  Total violations: {len(violations)}")
    if min_increase < float('inf'):
        print(f"  Smallest increase: delta_H = {min_increase:.15e} at N = {min_increase_N}")
        print(f"    phi({min_increase_N}) = {euler_totient(min_increase_N)}, "
              f"prime = {is_prime(min_increase_N)}")

    if violations:
        print(f"\n  VIOLATIONS found:")
        for N, dH, phi, isp in violations:
            print(f"    N={N}: delta_H={dH:.15e}, phi(N)={phi}, prime={isp}")
    else:
        print(f"\n  >>> CONJECTURE HOLDS: H(F_N) strictly increasing for N=2..{N_max} <<<")

    return entropies, violations, min_increase, min_increase_N, results_for_output


# ---------------------------------------------------------------------------
# PART 2: WHY does entropy increase? Decomposition analysis
# ---------------------------------------------------------------------------

def analyze_entropy_mechanism(N_max=150):
    """
    Decompose the entropy change at each step into individual arc splits.

    KEY INSIGHT: The arc lengths on the circle already sum to 1.
    When we insert new fractions, each one splits an existing arc
    w -> (w1, w2) with w1 + w2 = w.

    The entropy change from one split is:
        Delta = -w1*log(w1) - w2*log(w2) + w*log(w) = w * h(w1/w)
    where h is the binary entropy function.

    Crucially, there is NO renormalization effect: the arc lengths
    sum to 1 before and after, so the total change is exactly the sum
    of individual split contributions.
    """
    print(f"\n{'=' * 70}")
    print(f"PART 2: Entropy increase mechanism (N=2..{N_max})")
    print(f"{'=' * 70}")
    print(f"  Testing: is delta_H exactly the sum of split effects?")

    sorted_fracs = [0.0]
    prev_H = compute_entropy_from_sorted(sorted_fracs)
    max_ratio_dev = 0.0

    for N in range(2, N_max + 1):
        new_fracs = []
        for a in range(1, N):
            if gcd(a, N) == 1:
                new_fracs.append(a / N)
        new_fracs.sort()

        # Compute splitting contribution
        splitting_total = 0.0
        current = list(sorted_fracs)  # copy for tracking splits within this step

        for f_new in new_fracs:
            # Find the arc containing f_new in current arrangement
            pos = bisect.bisect_right(current, f_new)
            if pos == 0:
                left = current[-1] - 1.0  # wrap around
                right = current[0]
            elif pos >= len(current):
                left = current[-1]
                right = current[0] + 1.0
            else:
                left = current[pos - 1]
                right = current[pos]

            w = right - left
            w1 = f_new - left
            w2 = right - f_new

            if w > 1e-15 and w1 > 1e-15 and w2 > 1e-15:
                split_dH = -w1 * log(w1) - w2 * log(w2) + w * log(w)
                splitting_total += split_dH

            bisect.insort(current, f_new)

        # Now insert into the main sorted list
        for f in new_fracs:
            bisect.insort(sorted_fracs, f)

        H = compute_entropy_from_sorted(sorted_fracs)
        delta_H = H - prev_H

        if delta_H > 1e-15:
            ratio = splitting_total / delta_H
            dev = abs(ratio - 1.0)
            if dev > max_ratio_dev:
                max_ratio_dev = dev

            if N <= 15 or (is_prime(N) and N <= 50):
                print(f"  N={N:3d}: delta_H={delta_H:.12f}, "
                      f"split_sum={splitting_total:.12f}, "
                      f"ratio={ratio:.10f}, phi={euler_totient(N)}")

        prev_H = H

    print(f"\n  Max |ratio - 1| across all N: {max_ratio_dev:.2e}")
    if max_ratio_dev < 1e-8:
        print(f"  >>> CONFIRMED: delta_H = (sum of split effects) to machine precision <<<")
        print(f"  >>> No renormalization effect: arcs sum to 1 before and after <<<")
        print(f"  >>> Each split contributes STRICTLY POSITIVE entropy <<<")
        print(f"  >>> THEREFORE: H(F_{{N+1}}) > H(F_N) always <<<")
    else:
        print(f"  Ratio deviates from 1 -- possible numerical issues")


# ---------------------------------------------------------------------------
# PART 3: Proof
# ---------------------------------------------------------------------------

def proof_sketch():
    """Print the complete proof."""
    print(f"\n{'=' * 70}")
    print(f"PART 3: PROOF of Strict Entropy Monotonicity")
    print(f"{'=' * 70}")

    print("""
THEOREM. For all N >= 2, H(F_{N+1}) > H(F_N), where H(F_N) denotes the
Shannon entropy of the arc-length distribution of the Farey sequence F_N
on the unit circle.

PROOF.

Setup. Place the Farey sequence F_N = {a/b : 0 <= a/b <= 1, b <= N,
gcd(a,b)=1} on the circle [0,1) by identifying 0 and 1. Let the points
(excluding the duplicate at 0=1) be x_0 < x_1 < ... < x_{n-1}.

The arc lengths are:
    w_i = x_{i+1} - x_i  (for i < n-1),    w_{n-1} = 1 - x_{n-1} + x_0

These satisfy: (1) w_i > 0 for all i, and (2) sum_i w_i = 1.

The Shannon entropy is H = -sum_i w_i log(w_i).

Step 1: What changes from F_N to F_{N+1}.

The set F_{N+1} = F_N union {a/(N+1) : gcd(a, N+1) = 1, 0 < a < N+1}.
There are phi(N+1) >= 1 new fractions added. Each new fraction is strictly
between two consecutive existing fractions in F_N (since all Farey fractions
are distinct and ordered).

Step 2: Each new fraction splits one arc.

When a new fraction f_new is inserted between x_j and x_{j+1}, it splits
the arc of width w = w_j into two sub-arcs:
    w_1 = f_new - x_j > 0,    w_2 = x_{j+1} - f_new > 0,    w_1 + w_2 = w.

The change in the entropy functional from this single split is:
    Delta = [-w_1 log(w_1) - w_2 log(w_2)] - [-w log(w)]
          = w log(w) - w_1 log(w_1) - w_2 log(w_2)
          = w * h(w_1/w)

where h(t) = -t log(t) - (1-t) log(1-t) is the binary entropy function.

Since 0 < w_1/w < 1, we have h(w_1/w) > 0, and since w > 0, Delta > 0.

Step 3: No renormalization effect.

CRUCIAL: The arc lengths sum to 1 BOTH before and after the insertion.
This is because the new fraction merely subdivides an existing arc --
it does not change the total perimeter of the circle. Therefore the
entropy H = -sum w_i log(w_i) changes by EXACTLY the sum of the individual
split contributions. There is no indirect effect from normalization.

Step 4: Multiple insertions.

When phi(N+1) > 1, we insert k = phi(N+1) fractions. Order them as
f_1 < f_2 < ... < f_k. Insert them one by one. At each insertion, the
fraction f_j splits some arc (either an original arc from F_N or a sub-arc
created by a previous insertion). Each split contributes a strictly
positive amount Delta_j > 0.

Therefore:
    H(F_{N+1}) - H(F_N) = sum_{j=1}^{k} Delta_j > 0.

This holds because:
- k >= 1 (since phi(N+1) >= 1 for all N+1 >= 2)
- Each Delta_j > 0 (by strict concavity of -x log(x) on (0,1))

Hence H(F_{N+1}) > H(F_N) for all N >= 1.  QED.

COROLLARY 1. H(F_N) is bounded above by log(|F_N| - 1), the maximum
entropy of a distribution on |F_N| - 1 arcs. Hence H(F_N) is a bounded,
strictly increasing sequence, and therefore convergent.

COROLLARY 2. H(F_N) / log(|F_N|) -> 1 as N -> infinity, since the Farey
sequence becomes equidistributed on [0,1) (a consequence of the Weyl
equidistribution theorem or the density of Farey sequences).

REMARK ON QUANTITATIVE BOUNDS. The entropy increment satisfies:

    H(F_{N+1}) - H(F_N) >= phi(N+1) * w_min * h(t_min)

where w_min is the smallest arc being split and t_min is the most extreme
split fraction. Since the smallest Farey gap at level N is 1/(N(N-1)),
and the split fraction is bounded away from 0 and 1 by mediant properties,
a lower bound of order phi(N+1)/N^2 * c is achievable.
""")


# ---------------------------------------------------------------------------
# PART 4: Entropy vs Wobble
# ---------------------------------------------------------------------------

def entropy_vs_wobble(N_max=500):
    """
    Compare entropy H(N) with wobble W(N) = sum |w_i - 1/n|.
    """
    print(f"\n{'=' * 70}")
    print(f"PART 4: Entropy H(N) vs Wobble W(N), N=2..{N_max}")
    print(f"{'=' * 70}")

    sorted_fracs = [0.0]
    H_list = []
    W_list = []
    Ns = []

    H_mono_violations = 0
    W_mono_violations = 0
    prev_H = None
    prev_W = None

    for N in range(2, N_max + 1):
        for a in range(1, N):
            if gcd(a, N) == 1:
                bisect.insort(sorted_fracs, a / N)

        n = len(sorted_fracs)

        # Arc lengths
        arcs = []
        for i in range(n - 1):
            arcs.append(sorted_fracs[i + 1] - sorted_fracs[i])
        arcs.append(1.0 - sorted_fracs[-1] + sorted_fracs[0])

        H = -sum(w * log(w) for w in arcs if w > 0)
        uniform = 1.0 / n
        W = sum(abs(w - uniform) for w in arcs)

        if prev_H is not None:
            if H <= prev_H: H_mono_violations += 1
            if W >= prev_W: W_mono_violations += 1

        H_list.append(H)
        W_list.append(W)
        Ns.append(N)
        prev_H = H
        prev_W = W

    # Correlation between delta_H and delta_W
    dH = [H_list[i] - H_list[i - 1] for i in range(1, len(H_list))]
    dW = [W_list[i] - W_list[i - 1] for i in range(1, len(W_list))]

    mean_dH = sum(dH) / len(dH)
    mean_dW = sum(dW) / len(dW)
    cov = sum((a - mean_dH) * (b - mean_dW) for a, b in zip(dH, dW)) / len(dH)
    std_dH = sqrt(sum((a - mean_dH) ** 2 for a in dH) / len(dH))
    std_dW = sqrt(sum((b - mean_dW) ** 2 for b in dW) / len(dW))
    corr = cov / (std_dH * std_dW) if std_dH > 0 and std_dW > 0 else 0

    # How many N have wobble INCREASING?
    W_increase_count = sum(1 for d in dW if d > 0)
    W_increase_at_primes = sum(1 for i in range(len(dW))
                               if dW[i] > 0 and is_prime(Ns[i + 1]))

    print(f"  Entropy monotone-increasing violations: {H_mono_violations}")
    print(f"  Wobble monotone-decreasing violations:  {W_mono_violations}")
    print(f"    (wobble increases at {W_increase_count} steps, "
          f"{W_increase_at_primes} at primes)")
    print(f"  Correlation(delta_H, delta_W): {corr:.4f}")
    print(f"  ==> Entropy ALWAYS increases; wobble sometimes increases")
    print(f"  ==> They measure uniformity differently:")
    print(f"      H is controlled by arc SPLITTING (always increases)")
    print(f"      W depends on arc sizes RELATIVE to 1/n (n changes!)")

    return Ns, H_list, W_list


# ---------------------------------------------------------------------------
# PART 5: Quantitative scaling of entropy increments
# ---------------------------------------------------------------------------

def entropy_increment_analysis(N_max=1000, entropies=None):
    """
    Analyze scaling of delta_H with N, phi(N), and |F_N|.
    """
    print(f"\n{'=' * 70}")
    print(f"PART 5: Entropy increment scaling (N=2..{N_max})")
    print(f"{'=' * 70}")

    if entropies is None:
        # Recompute
        sorted_fracs = [0.0]
        entropies = {}
        for N in range(2, N_max + 1):
            for a in range(1, N):
                if gcd(a, N) == 1:
                    bisect.insort(sorted_fracs, a / N)
            entropies[N] = compute_entropy_from_sorted(sorted_fracs)

    # Analyze
    all_data = []
    for N in range(3, N_max + 1):
        if N in entropies and N - 1 in entropies:
            dH = entropies[N] - entropies[N - 1]
            phi_N = euler_totient(N)
            all_data.append((N, dH, phi_N, is_prime(N)))

    # Smallest increments
    all_data.sort(key=lambda x: x[1])
    print(f"\n  10 smallest entropy increments:")
    for N, dH, phi, isp in all_data[:10]:
        ptype = "PRIME" if isp else "composite"
        print(f"    N={N:4d}: delta_H={dH:.12e}, phi={phi:4d}, {ptype}")

    print(f"\n  10 largest entropy increments:")
    for N, dH, phi, isp in all_data[-10:]:
        ptype = "PRIME" if isp else "composite"
        print(f"    N={N:4d}: delta_H={dH:.12e}, phi={phi:4d}, {ptype}")

    # Scaling with phi(N)
    # delta_H should scale roughly as phi(N) / |F_N| * log(2) for midpoint splits
    # But |F_N| ~ 3N^2/pi^2, so phi(N)/|F_N| ~ phi(N)*pi^2/(3N^2)
    # For primes, phi(N) = N-1, so delta_H ~ (N-1)*pi^2/(3N^2) * log(2) ~ pi^2*log(2)/(3N)

    primes_dH = [(N, dH) for N, dH, phi, isp in all_data if isp]
    if primes_dH:
        # Check if delta_H * N converges for primes
        products = [N * dH for N, dH in primes_dH]
        print(f"\n  For primes: delta_H * p across range:")
        for i in [0, len(primes_dH) // 4, len(primes_dH) // 2,
                  3 * len(primes_dH) // 4, -1]:
            N, dH = primes_dH[i]
            print(f"    p={N:4d}: delta_H*p = {N * dH:.6f}")
        mean_prod = sum(products[-20:]) / 20
        print(f"    Mean(delta_H * p) for last 20 primes: {mean_prod:.6f}")
        expected = 3.1416**2 * log(2) / 3
        print(f"    Expected (pi^2 * ln2 / 3): {expected:.6f}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print("VORONOI ENTROPY MONOTONICITY FOR FAREY SEQUENCES")
    print("=" * 70)
    print()

    # Part 1: Extended verification
    entropies, violations, min_inc, min_inc_N, results = verify_monotonicity(N_max=1000)

    # Part 2: Mechanism analysis
    analyze_entropy_mechanism(N_max=150)

    # Part 3: Proof sketch
    proof_sketch()

    # Part 4: Comparison with wobble
    Ns, H_vals, W_vals = entropy_vs_wobble(N_max=500)

    # Part 5: Increment scaling
    entropy_increment_analysis(N_max=1000, entropies=entropies)

    # Summary
    print(f"\n{'=' * 70}")
    print(f"FINAL SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Verification range: N = 2 to 1000")
    print(f"  Monotonicity violations: {len(violations)}")
    if min_inc < float('inf'):
        print(f"  Smallest entropy increase: {min_inc:.15e} at N = {min_inc_N}")
    print()
    if len(violations) == 0:
        print(f"  STATUS: THEOREM (not just conjecture)")
        print(f"  The proof is elementary:")
        print(f"    1. Arc lengths sum to 1 on the circle")
        print(f"    2. Each new fraction splits an arc into two sub-arcs")
        print(f"    3. By strict concavity of -x*log(x), each split")
        print(f"       increases entropy by a strictly positive amount")
        print(f"    4. There is no renormalization effect")
        print(f"    5. phi(N+1) >= 1 guarantees at least one split per step")
        print(f"  Verified computationally to N=1000 (zero violations)")


if __name__ == '__main__':
    main()
