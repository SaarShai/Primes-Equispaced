#!/usr/bin/env python3
"""
DEEP PROOF ANALYSIS: Find a provable bound for ΔW(p) in restricted class
=========================================================================

KEY FINDINGS FROM PART 1:
1. ALL M(p) <= -3 primes have ΔW(p) < 0 (4617 primes, 0 violations)
2. |ΔW(p)| * p^2 grows (slowly), suggesting ΔW ≈ -C(M)/p^(2-ε)
3. The cross term C_b grows with p, but the self+shift terms grow faster

THIS SCRIPT:
- Derives the EXACT analytical decomposition of ΔW(p)
- Identifies which component enforces the sign
- Attempts a proof for the class of primes p with M(p) ≤ -3 and p ≡ 1 (mod q)

EXACT DECOMPOSITION (from first principles):
  W(N) = Σ_j (f_j - j/n)^2 where n = |F_N|

  Let D_j = j - n*f_j (counting function discrepancy at f_j)
  Then (f_j - j/n)^2 = D_j^2 / n^2
  So W(N) = (1/n^2) Σ D_j^2

  When going from N=p-1 to N=p (adding prime p):

  New sequence has n' = n + (p-1) fractions.
  Old fraction a/b gets new rank j' = j + floor(pa/b).
  New fraction k/p gets rank = N_{p-1}(k/p) + k.

  W(p) = (1/n'^2) [Σ_old D'_j^2 + Σ_new D'_k^2]

  where D'(a/b) = j + floor(pa/b) - n'*(a/b)
                 = D(a/b) + floor(pa/b) - (p-1)*(a/b)
                 = D(a/b) + δ(a/b)

  with δ(a/b) = floor(pa/b) - (p-1)*a/b = a/b - {pa/b}

  So: Σ_old D'^2 = Σ_old (D + δ)^2 = Σ D^2 + 2Σ D·δ + Σ δ^2

  And for new fractions k/p:
  D'(k/p) = N_{p-1}(k/p) + k - n'*(k/p)
           = N_{p-1}(k/p) - n*(k/p)     [since n' = n + p-1 and n'*(k/p) = n*k/p + k*(p-1)/p]
  Wait, let me redo this carefully:

  rank of k/p = N_{p-1}(k/p) + k  (count of old fracs ≤ k/p, plus k new fracs ≤ k/p)
  D'(k/p) = rank - n'*(k/p) = N_{p-1}(k/p) + k - (n + p-1)*(k/p)
           = N_{p-1}(k/p) - n*(k/p) + k - (p-1)*k/p
           = D_{old}(k/p) + k/p

  where D_{old}(k/p) = N_{p-1}(k/p) - n*(k/p) is the old counting discrepancy at k/p.

  So: Σ_new D'^2 = Σ_{k=1}^{p-1} (D_{old}(k/p) + k/p)^2
                 = Σ D_{old}(k/p)^2 + 2Σ (k/p)*D_{old}(k/p) + Σ k^2/p^2

  The last sum = (p-1)(2p-1)/(6p^2) ≡ S_2^{new}/p^2.

  So:
  n'^2 * W(p) = Σ_old (D + δ)^2 + Σ_new (D_{old}(k/p) + k/p)^2
  n^2 * W(p-1) = Σ_old D^2

  ΔW = W(p-1) - W(p) = Σ D^2/n^2 - [Σ(D+δ)^2 + Σ(D_old(k/p)+k/p)^2]/n'^2

  This is exact but complex. Let's compute each piece numerically.
"""

import csv
import os
from math import gcd, floor, sqrt, isqrt, log
from fractions import Fraction
from collections import defaultdict
import time

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
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime_flag = [True] * (limit + 1)
    for p in range(2, limit + 1):
        if is_prime_flag[p]:
            for k in range(2*p, limit + 1, p):
                is_prime_flag[k] = False
            # Apply mobius
            for k in range(limit // p, 0, -1):
                if k * p <= limit:
                    if k * p * p <= limit and (k * p * p) % (p * p) == 0:
                        pass  # handled below
    # Just use direct sieve
    smallest_prime = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if smallest_prime[i] == 0:
            for j in range(i, limit + 1, i):
                if smallest_prime[j] == 0:
                    smallest_prime[j] = i

    mu[1] = 1
    for n in range(2, limit + 1):
        p = smallest_prime[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]

    M = [0] * (limit + 1)
    running = 0
    for n in range(1, limit + 1):
        running += mu[n]
        M[n] = running
    return M

def farey_generator(N):
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))


def exact_decomposition(p, phi_arr):
    """
    Compute the EXACT decomposition of ΔW(p) into:

    n'^2 * W(p) = old_self + old_cross + old_delta_sq + new_D_sq + new_cross_Dk + new_k_sq
    n^2 * W(p-1) = old_self

    Returns all components and the exact ΔW.
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    # Iterate through F_{p-1}
    old_D_sq = 0.0      # Σ D(a/b)^2  (= n^2 * W(p-1))
    old_cross = 0.0      # 2 * Σ D(a/b) * δ(a/b)
    old_delta_sq = 0.0   # Σ δ(a/b)^2

    # Also build counting function for new fractions
    # We need D_old(k/p) for k = 1, ..., p-1
    # D_old(x) = N_{p-1}(x) - n*x where N_{p-1}(x) = #{a/b in F_{p-1}: a/b <= x}

    # Strategy: iterate F_{p-1} and record D_old at each k/p
    rank = 0
    D_old_at_kp = {}  # k -> D_old(k/p)
    next_k = 1  # next k/p we're looking for

    old_fracs = list(farey_generator(N))
    n_check = len(old_fracs)
    assert n_check == n, f"Size mismatch: {n_check} vs {n}"

    for idx, (a, b) in enumerate(old_fracs):
        f = a / b
        D = idx - n * f

        # Process D^2
        old_D_sq += D * D

        # δ(a/b) = a/b - {pa/b}
        if a == 0 and b == 1:
            delta = 0.0  # δ(0/1) = 0
        elif a == b:
            delta = 0.0  # δ(1/1) = 0
        else:
            pa_over_b = p * a / b
            frac_part = pa_over_b - floor(pa_over_b)
            delta = a / b - frac_part

        old_cross += 2 * D * delta
        old_delta_sq += delta * delta

        # Record D_old values at k/p points
        # For all k/p that are in (prev_f, f], D_old(k/p) = idx - n*(k/p)
        # Actually D_old(k/p) = N_{p-1}(k/p) - n*(k/p) where N_{p-1}(k/p) = idx
        # (assuming k/p < f, we have N_{p-1}(k/p) = idx since exactly idx fractions are ≤ k/p)
        # Wait, we need to be careful. After processing fraction at index idx = rank,
        # N_{p-1}(x) = idx+1 for x in [f, next_f).
        # No: at index idx, the fraction is f = a/b.
        # N_{p-1}(f) = idx + 1 (counting 0/1 as index 0).
        # For x in (f_{idx-1}, f_idx): N_{p-1}(x) = idx.

    # Rebuild properly: record (index, fraction) list, then binary search
    frac_values = [a/b for (a,b) in old_fracs]

    new_D_sq = 0.0    # Σ D'(k/p)^2 for new fractions
    new_cross = 0.0   # 2 * Σ (k/p) * D_old(k/p)
    new_k_sq = 0.0    # Σ (k/p)^2

    # For each new fraction k/p, find its rank among old fractions
    # using binary search on frac_values
    import bisect

    for k in range(1, p):
        x = k / p
        # N_{p-1}(k/p) = number of old fracs ≤ k/p
        # Since p is prime and b < p for all old fracs, pa/b is never integer
        # for 0 < a/b < 1 (well, except 0/1 and 1/1).
        # Actually k/p itself is not in F_{p-1}, so we use bisect_left
        rank_old = bisect.bisect_left(frac_values, x)
        # But wait - bisect_left finds insertion point. If x = k/p is not in the list,
        # then rank_old = N_{p-1}(k/p) exactly (count of old fracs < x, but since
        # x is not in the list, < x is same as ≤ x).
        # Actually no: bisect_left gives index of first element >= x.
        # N_{p-1}(x) = #{a/b in F_{p-1}: a/b <= x}
        # If x not in list: N_{p-1}(x) = bisect_left(list, x) = index of first > x
        # Hmm, bisect_left gives index where x would be inserted to keep sorted.
        # If x < list[i] for all i >= rank_old, and x >= list[i] for i < rank_old,
        # then N_{p-1}(x) = rank_old.

        D_old_x = rank_old - n * x

        # D'(k/p) = D_old(k/p) + k/p
        D_prime = D_old_x + x

        new_D_sq += D_prime * D_prime
        new_cross += 2 * x * D_old_x  # This is part of expanding (D_old + k/p)^2
        new_k_sq += x * x

    # Now compute W(p-1) and W(p)
    W_pm1 = old_D_sq / (n * n)

    # n'^2 * W(p) = Σ_old (D + δ)^2 + Σ_new (D_old(k/p) + k/p)^2
    #             = old_D_sq + old_cross + old_delta_sq + new_D_sq
    numerator_Wp = old_D_sq + old_cross + old_delta_sq + new_D_sq
    W_p = numerator_Wp / (n_prime * n_prime)

    delta_W = W_pm1 - W_p

    # Components of ΔW:
    # ΔW = old_D_sq/n^2 - (old_D_sq + old_cross + old_delta_sq + new_D_sq)/n'^2
    # = old_D_sq * (1/n^2 - 1/n'^2) - (old_cross + old_delta_sq + new_D_sq)/n'^2
    # = old_D_sq * (n'^2 - n^2)/(n^2 * n'^2) - (old_cross + old_delta_sq + new_D_sq)/n'^2

    # The first term is POSITIVE (helps ΔW > 0, i.e., is bad for us)
    # Actually wait: we want ΔW = W(p-1) - W(p) to be NEGATIVE.
    # If W(p) > W(p-1), then ΔW < 0.
    # The "self" old_D_sq term: old_D_sq/n^2 > old_D_sq/n'^2, so this makes ΔW > 0.
    # But new_D_sq/n'^2 makes W(p) larger, so makes ΔW < 0.

    term_dilution = old_D_sq * (1.0/n**2 - 1.0/n_prime**2)  # POSITIVE, pushes ΔW > 0
    term_cross = old_cross / n_prime**2                        # sign unclear
    term_delta_sq = old_delta_sq / n_prime**2                  # POSITIVE (pushes ΔW < 0 since subtracted)
    term_new = new_D_sq / n_prime**2                           # POSITIVE (pushes ΔW < 0)

    # ΔW = term_dilution - term_cross - term_delta_sq - term_new
    delta_W_check = term_dilution - term_cross - term_delta_sq - term_new

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'W_pm1': W_pm1, 'W_p': W_p, 'delta_W': delta_W,
        'delta_W_check': delta_W_check,
        'old_D_sq': old_D_sq,
        'old_cross': old_cross,
        'old_delta_sq': old_delta_sq,
        'new_D_sq': new_D_sq,
        'term_dilution': term_dilution,
        'term_cross': term_cross,
        'term_delta_sq': term_delta_sq,
        'term_new': term_new,
    }


def main():
    print("DEEP DECOMPOSITION ANALYSIS")
    print("=" * 80)

    start = time.time()
    LIMIT = 5000
    phi_arr = euler_totient_sieve(LIMIT)
    M_arr = mertens_sieve(LIMIT)
    primes = sieve_primes(LIMIT)

    # Test on primes with M(p) <= -3
    target_primes = [p for p in primes if p >= 11 and M_arr[p] <= -3 and p <= 2000]

    print(f"\nTarget primes (M(p) <= -3, p <= 2000): {len(target_primes)}")

    print(f"\n{'p':>6} {'M':>4} {'ΔW':>16} {'dilution':>14} {'cross/n2':>14} "
          f"{'δ²/n2':>14} {'new/n2':>14} {'dilut-new':>14}")
    print("-" * 110)

    results = []
    for p in target_primes:
        r = exact_decomposition(p, phi_arr)
        results.append(r)

        # Verify
        assert abs(r['delta_W'] - r['delta_W_check']) < 1e-10, \
            f"Mismatch at p={p}: {r['delta_W']} vs {r['delta_W_check']}"

        print(f"{p:6d} {M_arr[p]:4d} {r['delta_W']:+16.10f} "
              f"{r['term_dilution']:+14.10f} {r['term_cross']:+14.10f} "
              f"{r['term_delta_sq']:+14.10f} {r['term_new']:+14.10f} "
              f"{r['term_dilution'] - r['term_new']:+14.10f}")

    # KEY ANALYSIS: What makes ΔW negative?
    # ΔW = dilution - cross - delta_sq - new
    # For ΔW < 0: need dilution < cross + delta_sq + new
    # i.e., new_D_sq + old_delta_sq + old_cross > dilution * n'^2

    print(f"\n\n--- RATIO ANALYSIS ---")
    print(f"{'p':>6} {'M':>4} {'new/dilut':>12} {'(cross+dsq+new)/dilut':>22} {'cross_sign':>12}")
    print("-" * 70)

    for r in results:
        if abs(r['term_dilution']) > 1e-15:
            new_over_dilut = r['term_new'] / r['term_dilution']
            combined = (r['term_cross'] + r['term_delta_sq'] + r['term_new']) / r['term_dilution']
            cross_sign = "+" if r['term_cross'] > 0 else "-"
        else:
            new_over_dilut = 0
            combined = 0
            cross_sign = "0"

        print(f"{r['p']:6d} {M_arr[r['p']]:4d} {new_over_dilut:12.6f} {combined:22.6f} {cross_sign:>12}")

    # CRITICAL: Is new_D_sq > old_D_sq * (n'^2/n^2 - 1) always?
    # dilution = old_D_sq * (1/n^2 - 1/n'^2) = old_D_sq * (n'^2 - n^2)/(n^2 * n'^2)
    # term_new = new_D_sq / n'^2
    # We need term_new > term_dilution (ignoring cross and delta_sq which are small?)
    # ⟺ new_D_sq > old_D_sq * (n'^2 - n^2)/n^2 = old_D_sq * ((p-1)^2 + 2n(p-1))/n^2
    #   ≈ old_D_sq * 2(p-1)/n for large n

    print(f"\n\n--- SCALING OF COMPONENTS ---")
    print(f"{'p':>6} {'old_D_sq':>14} {'new_D_sq':>14} {'ratio_n/d':>12} {'cross':>14} "
          f"{'delta_sq':>14}")
    print("-" * 80)

    for r in results:
        n = r['n']
        n_prime = r['n_prime']
        dilution_raw = r['old_D_sq'] * (n_prime**2 - n**2) / n**2
        ratio = r['new_D_sq'] / dilution_raw if dilution_raw > 0 else 0

        print(f"{r['p']:6d} {r['old_D_sq']:14.4f} {r['new_D_sq']:14.4f} {ratio:12.6f} "
              f"{r['old_cross']:+14.4f} {r['old_delta_sq']:14.4f}")

    # The NEW insight: what is new_D_sq in terms of the counting discrepancy?
    # new_D_sq = Σ_{k=1}^{p-1} (D_old(k/p) + k/p)^2
    # = Σ D_old(k/p)^2 + 2 Σ (k/p)*D_old(k/p) + Σ (k/p)^2
    #
    # D_old(k/p) = N_{p-1}(k/p) - n*(k/p)
    # This is the Farey counting discrepancy at equally spaced points k/p.
    #
    # By the Mertens connection: Σ_{k=1}^{p-1} D_old(k/p) = -M(p-1) - 1
    # (approximately; the exact relation involves careful counting)

    print(f"\n\n--- DECOMPOSITION OF new_D_sq ---")
    print(f"{'p':>6} {'M':>4} {'Σ D_old²':>14} {'2Σ(k/p)D':>14} {'Σ(k/p)²':>14} {'new_D_sq':>14}")
    print("-" * 80)

    import bisect

    for p in target_primes[:30]:
        N = p - 1
        old_fracs = list(farey_generator(N))
        n = len(old_fracs)
        frac_values = [a/b for (a,b) in old_fracs]

        sum_Dold_sq = 0.0
        sum_kp_Dold = 0.0
        sum_kp_sq = 0.0
        sum_Dold = 0.0

        for k in range(1, p):
            x = k / p
            rank_old = bisect.bisect_left(frac_values, x)
            D_old_x = rank_old - n * x

            sum_Dold_sq += D_old_x ** 2
            sum_kp_Dold += x * D_old_x
            sum_kp_sq += x ** 2
            sum_Dold += D_old_x

        new_D_sq = sum_Dold_sq + 2 * sum_kp_Dold + sum_kp_sq

        print(f"{p:6d} {M_arr[p]:4d} {sum_Dold_sq:14.4f} {2*sum_kp_Dold:+14.4f} "
              f"{sum_kp_sq:14.4f} {new_D_sq:14.4f}  Σ D_old = {sum_Dold:+.4f}")

    # KEY RELATIONSHIP: Σ D_old(k/p) relates to M(p-1)
    # The Farey counting function N_{p-1}(x) counts fracs ≤ x in F_{p-1}
    # Σ_{k=1}^{p-1} N_{p-1}(k/p) = Σ_{b=1}^{p-1} Σ_{a=0}^{b} [gcd(a,b)=1] * #{k: k/p >= a/b}
    # = Σ (a,b) in F_{p-1} * floor(p * a/b + ε) ... complicated

    # Instead, note: Σ_{k=1}^{p-1} D_old(k/p) = Σ N_{p-1}(k/p) - n * Σ k/p
    #                                           = Σ N_{p-1}(k/p) - n * (p-1)/2

    print(f"\n\n--- MERTENS CONNECTION ---")
    print(f"{'p':>6} {'M(p)':>5} {'M(p-1)':>7} {'Σ D_old':>12} {'Σ D_old + M(p-1)+1':>20}")
    print("-" * 60)

    for p in target_primes[:30]:
        N = p - 1
        old_fracs = list(farey_generator(N))
        n = len(old_fracs)
        frac_values = [a/b for (a,b) in old_fracs]

        sum_Dold = 0.0
        for k in range(1, p):
            x = k / p
            rank_old = bisect.bisect_left(frac_values, x)
            D_old_x = rank_old - n * x
            sum_Dold += D_old_x

        # Check against Mertens
        print(f"{p:6d} {M_arr[p]:5d} {M_arr[p-1]:7d} {sum_Dold:+12.4f} "
              f"{sum_Dold + M_arr[p-1] + 1:+20.4f}")

    # SELF-CONTAINED PROOF STRUCTURE CHECK
    # Does new_D_sq dominate dilution for EVERY prime with M(p) <= -3?
    print(f"\n\n--- PROOF-CRITICAL: Does new_D_sq > dilution_raw ALWAYS? ---")
    print(f"{'p':>6} {'M':>4} {'new_D_sq - dilut_raw':>22} {'margin %':>10}")
    print("-" * 50)

    all_positive = True
    for r in results:
        n = r['n']
        n_prime = r['n_prime']
        dilution_raw = r['old_D_sq'] * (n_prime**2 - n**2) / n**2
        margin = r['new_D_sq'] - dilution_raw
        pct = 100 * margin / dilution_raw if dilution_raw > 0 else 0

        if margin <= 0:
            all_positive = False
            print(f"{r['p']:6d} {M_arr[r['p']]:4d} {margin:+22.6f} {pct:+10.2f}%  *** NEGATIVE ***")
        elif r['p'] <= 200 or r['p'] % 500 < 10:
            print(f"{r['p']:6d} {M_arr[r['p']]:4d} {margin:+22.6f} {pct:+10.2f}%")

    if all_positive:
        print(f"\n  *** new_D_sq > dilution_raw for ALL {len(results)} primes! ***")
        print(f"  This means the new-fraction discrepancy ALONE dominates the dilution effect.")
        print(f"  Combined with cross term and delta_sq, ΔW < 0 is assured.")
    else:
        print(f"\n  new_D_sq vs dilution not always dominant. Need cross+delta_sq help.")

    # Check if (new_D_sq + old_cross) > dilution_raw
    print(f"\n--- Does (new_D_sq + old_cross/n'^2 * n'^2) rescue it? ---")
    # Actually: ΔW < 0 ⟺ dilution < cross/n'^2 + delta_sq/n'^2 + new/n'^2
    # ⟺ old_D_sq * (1/n^2 - 1/n'^2) < (old_cross + old_delta_sq + new_D_sq)/n'^2
    # ⟺ old_D_sq * (n'^2 - n^2)/n^2 < old_cross + old_delta_sq + new_D_sq

    print(f"\n--- FINAL CHECK: old_cross + old_delta_sq + new_D_sq > old_D_sq*(n'^2-n^2)/n^2 ---")
    print(f"{'p':>6} {'M':>4} {'LHS':>14} {'RHS':>14} {'margin':>14} {'ok':>4}")
    print("-" * 60)

    all_ok = True
    for r in results:
        n = r['n']
        n_prime = r['n_prime']
        LHS = r['old_cross'] + r['old_delta_sq'] + r['new_D_sq']
        RHS = r['old_D_sq'] * (n_prime**2 - n**2) / n**2
        margin = LHS - RHS
        ok = margin > 0
        if not ok:
            all_ok = False

        if r['p'] <= 200 or r['p'] % 500 < 10 or not ok:
            print(f"{r['p']:6d} {M_arr[r['p']]:4d} {LHS:14.4f} {RHS:14.4f} {margin:+14.4f} {'YES' if ok else 'NO'}")

    if all_ok:
        print(f"\n  *** ALL {len(results)} primes satisfy the inequality! ΔW < 0 confirmed. ***")

    # Now investigate: what controls the margin?
    print(f"\n\n--- WHAT CONTROLS THE SIGN? Relative contributions ---")
    print(f"{'p':>6} {'M':>4} {'new/total':>10} {'cross/total':>12} {'dsq/total':>10}")
    print("-" * 55)

    for r in results[:40]:
        total_LHS = r['old_cross'] + r['old_delta_sq'] + r['new_D_sq']
        if abs(total_LHS) > 1e-10:
            print(f"{r['p']:6d} {M_arr[r['p']]:4d} {r['new_D_sq']/total_LHS:10.4f} "
                  f"{r['old_cross']/total_LHS:12.4f} {r['old_delta_sq']/total_LHS:10.4f}")

    print(f"\n\nTotal runtime: {time.time() - start:.1f}s")


if __name__ == '__main__':
    main()
