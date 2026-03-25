#!/usr/bin/env python3
"""
GEOMETRIC PROOF ATTEMPTS for ΔW(p) < 0 when M(p) <= -3
==========================================================

Every algebraic approach fails because bounding Σ D_old² requires bounding W(p-1).
This script tests geometric ideas to find one that gives traction.

KEY CONTEXT:
  W(N) = (1/n) Σ (f_j - j/n)²
  ΔW(p) = W(p-1) - W(p)
  We want to show ΔW(p) < 0 (wobble INCREASES) when M(p) <= -3.

  W-free reformulation: ΔW <= 0 iff dilution <= cross + delta_sq + D_new_sq
  where dilution = Q·(n'²-n²)/n², Q = Σ D_old²
"""

from math import gcd, log, sqrt, pi, floor
import bisect
import numpy as np
from fractions import Fraction


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


def mertens(N):
    mu = [0] * (N + 1)
    mu[1] = 1
    for i in range(1, N + 1):
        for j in range(2 * i, N + 1, i):
            mu[j] -= mu[i]
    return sum(mu[1:N + 1])


def farey_float(N):
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append(a / b)
    fracs.sort()
    return fracs


def wobble(F):
    n = len(F)
    return sum((f - j / n) ** 2 for j, f in enumerate(F)) / n


# ================================================================
# IDEA 1: GAP VARIANCE
# ================================================================
def test_idea1(max_p=150):
    print("=" * 90)
    print("IDEA 1: GAP VARIANCE AND ARC-SPLITTING")
    print("=" * 90)
    print()

    primes = [p for p in range(2, max_p + 1) if is_prime(p)]

    print(f"{'p':>4} {'M(p)':>5} {'n':>6} {'n_new':>6} "
          f"{'Σg²_old':>12} {'Σg²_new':>12} {'ΔΣg²':>12} "
          f"{'ΔW':>12} {'W_new>W_old?':>12}")
    print("-" * 110)

    results = []
    for p in primes:
        Mp = mertens(p)
        F_old = farey_float(p - 1)
        F_new = farey_float(p)
        n = len(F_old)
        n_new = len(F_new)

        gaps_old = [F_old[i + 1] - F_old[i] for i in range(n - 1)]
        gaps_new = [F_new[i + 1] - F_new[i] for i in range(n_new - 1)]
        sum_g2_old = sum(g ** 2 for g in gaps_old)
        sum_g2_new = sum(g ** 2 for g in gaps_new)

        W_old = wobble(F_old)
        W_new = wobble(F_new)
        dW = W_old - W_new

        results.append({'p': p, 'Mp': Mp, 'dW': dW,
                        'delta_g2': sum_g2_new - sum_g2_old})

        if p <= 50 or Mp <= -3:
            print(f"{p:4d} {Mp:5d} {n:6d} {n_new:6d} "
                  f"{sum_g2_old:12.8f} {sum_g2_new:12.8f} "
                  f"{sum_g2_new - sum_g2_old:12.8f} "
                  f"{dW:12.8f} {'YES' if W_new > W_old else 'no':>12}")

    print()
    print("FINDING: Σg² ALWAYS decreases. But W can increase or decrease.")
    print("Gap uniformity != displacement uniformity. W depends on POSITIONS.")
    print("VERDICT: No direct traction from gap variance alone.")


# ================================================================
# COUPLING IDENTITY — careful derivation
# ================================================================
def test_coupling_identity(max_p=100):
    """
    For k/p a new fraction in F_p (where p is prime):
      rank_in_F_p(k/p) = N_{p-1}(k/p) + k
    where N_{p-1}(x) = #{f in F_{p-1} : f <= x}.

    Displacement in F_p:
      D_new(k/p) = rank_in_F_p(k/p) - n' * (k/p)
                 = N_{p-1}(k/p) + k - (n + p - 1) * k/p
                 = [N_{p-1}(k/p) - n*(k/p)] + k - (p-1)*(k/p)
                 = D_{p-1}(k/p) + k*(1 - (p-1)/p)
                 = D_{p-1}(k/p) + k/p

    where D_{p-1}(x) = N_{p-1}(x) - n*x.

    WAIT: this assumes N_{p-1}(k/p) counts points <= k/p.
    Since p is prime and all Farey fractions a/b have b < p,
    none of them equals k/p exactly (for 0 < k < p).
    So bisect_right(F_old, k/p) = bisect_left(F_old, k/p) = N_{p-1}(k/p).

    Also rank_in_F_p(k/p): need to count all f in F_p with f < k/p,
    or f <= k/p depending on convention. If rank = index (0-based),
    then rank = #{f in F_p : f < k/p}.

    Let me verify with exact arithmetic.
    """
    print("\n" + "=" * 90)
    print("COUPLING IDENTITY: D_new(k/p) = D_{p-1}(k/p) + k/p")
    print("=" * 90)
    print()
    print("D_new(k/p) = index_in_F_p(k/p) - n'*(k/p)")
    print("           = [N_{p-1}(k/p) + k] - (n+p-1)*(k/p)")
    print("           = D_{p-1}(k/p) + k/p")
    print()

    primes = [p for p in range(2, max_p + 1) if is_prime(p)]

    for p in primes[:15]:
        F_old = farey_float(p - 1)
        F_new = farey_float(p)
        n = len(F_old)
        n_new = len(F_new)
        failures = 0

        for k in range(1, p):
            x = k / p
            # N_{p-1}(k/p) = number of fractions in F_{p-1} that are < k/p
            # (since k/p is never in F_{p-1} for prime p)
            N_pm1 = bisect.bisect_left(F_old, x)
            D_pm1 = N_pm1 - n * x

            # Index of k/p in F_p (0-based)
            idx = F_new.index(min(F_new, key=lambda f: abs(f - x)))
            # More robust: find exact index
            idx = bisect.bisect_left(F_new, x - 1e-15)
            while idx < len(F_new) and F_new[idx] < x - 1e-12:
                idx += 1

            D_new_actual = idx - n_new * x
            D_new_predicted = D_pm1 + x  # = D_{p-1}(k/p) + k/p

            if abs(D_new_actual - D_new_predicted) > 1e-8:
                failures += 1
                if failures <= 3:
                    # Debug
                    print(f"  p={p}, k={k}: idx={idx}, N_pm1={N_pm1}, k+N_pm1={k+N_pm1}")
                    print(f"    D_new={D_new_actual:.8f}, predicted={D_new_predicted:.8f}")
                    print(f"    diff={D_new_actual - D_new_predicted:.8f}")

        # Check: is the rank = N_{p-1} + k?
        # The index of k/p in F_p should be:
        #   #{old fracs < k/p} + #{new fracs < k/p} = N_{p-1}(k/p) + (k-1)
        #   Wait: the new fractions < k/p are 1/p, 2/p, ..., (k-1)/p.
        #   So #{new fracs < k/p} = k - 1, not k.
        # Let me re-check:

        # Actually the index of k/p is the number of elements BEFORE it.
        # Elements before k/p in F_p:
        #   Old fractions: #{a/b in F_{p-1} : a/b < k/p} = N_{p-1}(k/p)
        #   New fractions: #{j/p : 1 <= j < k} = k - 1
        #   Plus f=0=0/1 is already in F_{p-1}.
        #   So index = N_{p-1}(k/p) + (k-1)

        # Let me re-derive:
        #   D_new(k/p) = index - n'*(k/p)
        #              = [N_{p-1}(k/p) + (k-1)] - (n+p-1)*(k/p)
        #              = N_{p-1}(k/p) - n*(k/p) + (k-1) - (p-1)*(k/p)
        #              = D_{p-1}(k/p) + k - 1 - (p-1)*k/p
        #              = D_{p-1}(k/p) + k(1 - (p-1)/p) - 1
        #              = D_{p-1}(k/p) + k/p - 1

        # So the CORRECT identity is: D_new(k/p) = D_{p-1}(k/p) + k/p - 1
        # NOT + k/p. Let me verify this.
        failures2 = 0
        for k in range(1, p):
            x = k / p
            N_pm1 = bisect.bisect_left(F_old, x)
            D_pm1 = N_pm1 - n * x
            idx = bisect.bisect_left(F_new, x - 1e-15)
            while idx < len(F_new) and F_new[idx] < x - 1e-12:
                idx += 1
            D_new_actual = idx - n_new * x
            D_new_predicted2 = D_pm1 + x - 1  # k/p - 1

            if abs(D_new_actual - D_new_predicted2) > 1e-8:
                failures2 += 1

        # Wait: but this depends on whether we count 0/1 as "old" or not.
        # 0/1 is in BOTH F_{p-1} and F_p. It's an old fraction.
        # The new fractions are ONLY k/p for 1 <= k <= p-1 with gcd(k,p)=1.
        # Since p is prime, ALL k/p for 1 <= k <= p-1 are new.
        # But k=0 -> 0/p = 0/1 is already in F_{p-1}.
        # And k=p -> p/p = 1/1 is already in F_{p-1}.

        # New fractions j/p that are < k/p: those with j < k, so j=1,...,k-1.
        # Count = k - 1.
        # So index(k/p) = N_{p-1}(k/p) + (k - 1).

        # Actually, we also need to check: does k/p itself appear at position
        # N_{p-1}(k/p) + (k-1)?

        # All fractions < k/p in F_p:
        #   From F_{p-1}: N_{p-1}(k/p) fractions
        #   From new: j/p for j=1,...,k-1 -> (k-1) fractions
        #   Total < k/p: N_{p-1}(k/p) + (k-1)
        #   So 0-based index of k/p = N_{p-1}(k/p) + (k-1)

        # Then D_new = idx - n'*(k/p)
        #            = N_{p-1}(k/p) + k - 1 - (n + p - 1)*(k/p)
        #            = [N_{p-1}(k/p) - n*k/p] + k - 1 - (p-1)*k/p
        #            = D_{p-1}(k/p) + k - 1 - k + k/p
        #            = D_{p-1}(k/p) + k/p - 1

        if failures == 0:
            print(f"  p={p:3d}: identity D_new = D_{'{p-1}'}(k/p) + k/p       HOLDS")
        elif failures2 == 0:
            print(f"  p={p:3d}: identity D_new = D_{'{p-1}'}(k/p) + k/p - 1   HOLDS")
        else:
            # Try D_new = D_{p-1}(k/p) + k/p - 1 again more carefully
            # Let me just check the exact formula numerically
            x = 1 / p
            N_pm1 = bisect.bisect_left(F_old, x)
            idx = bisect.bisect_left(F_new, x - 1e-15)
            while idx < len(F_new) and F_new[idx] < x - 1e-12:
                idx += 1
            D_new_actual = idx - n_new * x
            D_pm1 = N_pm1 - n * x
            diff = D_new_actual - D_pm1
            print(f"  p={p:3d}: k=1: D_new-D_pm1 = {diff:.8f}, k/p = {1/p:.8f}, k/p-1 = {1/p-1:.8f}")
            print(f"          failures with +k/p: {failures}, with +k/p-1: {failures2}")


    # Now verify with EXACT fractions
    print()
    print("EXACT VERIFICATION with Fraction arithmetic:")
    for p in [5, 7, 11, 13]:
        F_old_exact = []
        for b in range(1, p):
            for a in range(0, b + 1):
                if gcd(a, b) == 1:
                    F_old_exact.append(Fraction(a, b))
        F_old_exact.sort()
        n = len(F_old_exact)

        F_new_exact = list(F_old_exact)
        for k in range(1, p):
            F_new_exact.append(Fraction(k, p))
        F_new_exact.sort()
        n_new = len(F_new_exact)

        assert n_new == n + p - 1

        all_ok = True
        sum_D = Fraction(0)
        for k in range(1, p):
            x = Fraction(k, p)
            # Index in F_new (0-based)
            idx = F_new_exact.index(x)
            D_new = idx - n_new * x

            # Count fracs in F_old < x
            N_pm1 = sum(1 for f in F_old_exact if f < x)
            D_pm1 = N_pm1 - n * x

            # Test identity: D_new = D_pm1 + k/p - 1
            predicted = D_pm1 + x - 1
            if D_new != predicted:
                print(f"  p={p}, k={k}: D_new={D_new}, predicted={predicted}")
                all_ok = False
            sum_D += D_pm1

        if all_ok:
            print(f"  p={p:3d}: D_new(k/p) = D_pm1(k/p) + k/p - 1 VERIFIED EXACTLY")
        else:
            print(f"  p={p:3d}: IDENTITY FAILED!")

        # Check sum of D_{p-1}(k/p)
        # sum_D = Σ_{k=1}^{p-1} [N_{p-1}(k/p) - n*k/p]
        #       = Σ N_{p-1}(k/p) - n*(p-1)/2
        sum_N = sum(sum(1 for f in F_old_exact if f < Fraction(k, p))
                    for k in range(1, p))
        print(f"         Σ N_pm1(k/p) = {sum_N}, n*(p-1)/2 = {n * (p-1) / 2}")
        print(f"         Σ D_pm1(k/p) = {float(sum_D):.6f}")
        Mp = mertens(p)
        print(f"         M(p) = {Mp}")


# ================================================================
# MAIN DECOMPOSITION with corrected identity
# ================================================================
def corrected_decomposition(max_p=500):
    """
    CORRECTED identity: D_new(k/p) = D_{p-1}(k/p) + k/p - 1

    So: D_new(k/p)² = [D_{p-1}(k/p) + k/p - 1]²

    Let u_k = D_{p-1}(k/p), v_k = k/p - 1. Then v_k ranges from 1/p-1 to (p-1)/p-1 = -1/p.

    D_new_sq = Σ (u_k + v_k)² = Σ u_k² + 2·Σ u_k·v_k + Σ v_k²

    A = Σ u_k² = Σ D_{p-1}(k/p)²
    B = 2·Σ u_k·v_k = 2·Σ D_{p-1}(k/p)·(k/p - 1)
    C = Σ v_k² = Σ (k/p - 1)² = Σ_{k=1}^{p-1} ((k-p)/p)² = Σ_{j=1}^{p-1} (j/p)² = (p-1)(2p-1)/(6p)

    Note: C is the SAME as before since Σ(k/p-1)² = Σ((p-k)/p)² = Σ(j/p)² for j=1..p-1.

    Now: Σ v_k = Σ (k/p - 1) = (p-1)/2 - (p-1) = -(p-1)/2
    And: Σ u_k·v_k = Σ D(k/p)·(k/p - 1) = Σ D(k/p)·(k/p) - Σ D(k/p)

    Let S1 = Σ D_{p-1}(k/p), S_kD = Σ (k/p)·D_{p-1}(k/p).
    Then B = 2·(S_kD - S1).

    The key question: what is S1?
    S1 = Σ_{k=1}^{p-1} [N_{p-1}(k/p) - n·k/p]
       = Σ N_{p-1}(k/p) - n·(p-1)/2

    Σ N_{p-1}(k/p) counts: for each old fraction f = a/b,
    how many k in {1,...,p-1} have k/p > a/b, i.e., k > pa/b?
    Since p prime and b < p, pa/b is not integer.
    So #{k : k/p > a/b} = p - 1 - floor(pa/b).
    And #{k in 1..p-1 : a/b < k/p} = p - 1 - floor(pa/b).
    Wait, we need k/p > a/b, i.e., k > pa/b, k in {1,...,p-1}.
    So count = p - 1 - floor(pa/b).

    Hmm, actually Σ_{k=1}^{p-1} N_{p-1}(k/p) = Σ_{k=1}^{p-1} #{a/b in F_{p-1} : a/b < k/p}
    = Σ_{a/b in F_{p-1}} #{k in 1..p-1 : k/p > a/b}
    = Σ_{a/b in F_{p-1}} #{k in 1..p-1 : k > pa/b}
    = Σ_{a/b in F_{p-1}} (p - 1 - floor(pa/b))

    For a/b = 0: floor(0) = 0, count = p-1
    For a/b = 1: floor(p) = p, count = p-1-p = -1? No...
    For a/b = 1: k > p*1 = p, but k <= p-1, so count = 0.
    So for f=1: floor(pa/b) = p, count = p-1-p = -1. That's wrong.

    The issue: for a/b = 1, we need k > p, which is impossible.
    So count = max(0, p - 1 - floor(p·f)).

    Let me just compute it numerically.
    """
    print("\n" + "=" * 90)
    print("CORRECTED DECOMPOSITION: D_new(k/p) = D_{p-1}(k/p) + k/p - 1")
    print("=" * 90)
    print()

    primes = [p for p in range(2, max_p + 1) if is_prime(p)]

    print(f"{'p':>4} {'M(p)':>5} {'n':>6} "
          f"{'A':>12} {'B':>12} {'C':>10} "
          f"{'D_new²':>12} {'dilution':>12} {'ratio':>8} {'margin':>12}")
    print("-" * 115)

    all_data = []
    for p in primes:
        Mp = mertens(p)
        F_old = farey_float(p - 1)
        F_new = farey_float(p)
        n = len(F_old)
        n_new = n + p - 1

        # Q = Σ D_old(f_j)²
        Q = sum((j - n * f) ** 2 for j, f in enumerate(F_old))
        dilution = Q * (n_new ** 2 - n ** 2) / n ** 2

        # A, B, C with corrected identity
        A = 0.0
        B_half = 0.0
        S1 = 0.0
        S_kD = 0.0
        for k in range(1, p):
            x = k / p
            N_pm1 = bisect.bisect_left(F_old, x)
            D = N_pm1 - n * x
            v = x - 1  # k/p - 1
            A += D * D
            B_half += D * v
            S1 += D
            S_kD += x * D

        B = 2 * B_half
        C = sum((k / p - 1) ** 2 for k in range(1, p))  # = (p-1)(2p-1)/(6p)

        D_new_sq = A + B + C

        # Verify D_new_sq directly
        D_new_sq_direct = 0.0
        for k in range(1, p):
            x = k / p
            idx = bisect.bisect_left(F_new, x - 1e-15)
            while idx < len(F_new) and F_new[idx] < x - 1e-12:
                idx += 1
            D_new = idx - n_new * x
            D_new_sq_direct += D_new * D_new

        ratio = D_new_sq / dilution if dilution > 0 else float('inf')

        # Also compute the full W-free inequality:
        # cross + delta_sq + D_new_sq >= dilution
        cross = 0.0
        delta_sq = 0.0
        for j_old in range(n):
            f = F_old[j_old]
            D_old = j_old - n * f
            # Find new index
            j_new_idx = bisect.bisect_left(F_new, f - 1e-15)
            while j_new_idx < len(F_new) and abs(F_new[j_new_idx] - f) > 1e-12:
                j_new_idx += 1
            D_new_f = j_new_idx - n_new * f
            delta = D_new_f - D_old
            cross += D_old * delta
            delta_sq += delta * delta
        cross *= 2
        full_rhs = cross + delta_sq + D_new_sq_direct
        full_margin = full_rhs - dilution

        all_data.append({
            'p': p, 'Mp': Mp, 'n': n, 'n_new': n_new,
            'A': A, 'B': B, 'C': C, 'S1': S1, 'S_kD': S_kD,
            'D_new_sq': D_new_sq, 'D_new_sq_direct': D_new_sq_direct,
            'dilution': dilution, 'ratio': ratio,
            'cross': cross, 'delta_sq': delta_sq,
            'full_rhs': full_rhs, 'full_margin': full_margin,
            'Q': Q
        })

        # Check decomposition matches
        if abs(D_new_sq - D_new_sq_direct) > 0.01:
            print(f"  ** MISMATCH at p={p}: decomp={D_new_sq:.4f}, direct={D_new_sq_direct:.4f}")

        if p <= 50 or Mp <= -3 or p in [97, 199, 281, 499]:
            print(f"{p:4d} {Mp:5d} {n:6d} "
                  f"{A:12.4f} {B:12.4f} {C:10.4f} "
                  f"{D_new_sq_direct:12.4f} {dilution:12.4f} {ratio:8.4f} {full_margin:12.4f}")

    # Summary statistics
    print()
    m3 = [d for d in all_data if d['Mp'] <= -3 and d['p'] >= 11]
    print(f"Primes with M(p)<=3, p>=11: {len(m3)}")

    if m3:
        ratios = [d['ratio'] for d in m3]
        margins = [d['full_margin'] for d in m3]
        print(f"  D_new_sq/dilution: min={min(ratios):.6f}, max={max(ratios):.6f}")
        print(f"  Full margin (cross+delta_sq+D_new_sq-dil): "
              f"min={min(margins):.4f}, all>0: {all(m > -0.01 for m in margins)}")

        # When D_new_sq/dilution < 1, does cross+delta_sq make up the difference?
        shortfall_cases = [d for d in m3 if d['ratio'] < 1.0]
        print(f"\n  Cases where D_new_sq < dilution: {len(shortfall_cases)}")
        for d in shortfall_cases:
            shortfall = d['dilution'] - d['D_new_sq_direct']
            rescue = d['cross'] + d['delta_sq']
            print(f"    p={d['p']}: shortfall={shortfall:.4f}, "
                  f"cross+δ²={rescue:.4f}, net margin={d['full_margin']:.4f}")

    # S1 = Σ D_{p-1}(k/p) analysis
    print()
    print("S1 = Σ D_{p-1}(k/p) analysis:")
    print(f"{'p':>4} {'M(p)':>5} {'S1':>12} {'-(p-1)/2':>12} {'S1+(p-1)/2':>12}")
    print("-" * 55)
    for d in all_data:
        if d['p'] <= 50 or d['Mp'] <= -3:
            correction = d['S1'] + (d['p'] - 1) / 2
            print(f"{d['p']:4d} {d['Mp']:5d} {d['S1']:12.4f} "
                  f"{-(d['p'] - 1) / 2:12.4f} {correction:12.4f}")

    return all_data


# ================================================================
# IDEA 4: COUPLING — what does S1 relate to?
# ================================================================
def analyze_S1(max_p=300):
    """
    S1 = Σ_{k=1}^{p-1} D_{p-1}(k/p) = Σ N_{p-1}(k/p) - n(p-1)/2

    By counting: Σ_{k=1}^{p-1} N_{p-1}(k/p) = Σ_{f in F_{p-1}} #{k: k/p > f, 1<=k<=p-1}

    For f = a/b in F_{p-1} (with 0 <= a/b <= 1):
      #{k in 1..p-1 : k/p > a/b} = #{k in 1..p-1 : k > pa/b}
      Since pa/b is never integer (p prime, b < p, b|a impossible for a < b),
      this = p - 1 - floor(pa/b).

    Special cases:
      f = 0/1 = 0: floor(0) = 0, count = p - 1
      f = 1/1 = 1: floor(p) = p, count = p - 1 - p... but k <= p-1 < p, so count = 0.
      Correction: floor(p·1) = p, and p-1-p = -1. But actually k/p > 1 is impossible, so count = 0.
      Need: min(p-1, p-1-floor(pf)) for f<1, and 0 for f=1.

    So: Σ N = Σ_{f in F_{p-1}, f < 1} (p - 1 - floor(pf)) + 0
            = (n-1)(p-1) - Σ_{f in F_{p-1}, f<1} floor(pf)

    And: S1 = (n-1)(p-1) - Σ floor(pf) - n(p-1)/2
            = (p-1)(n-1-n/2) - Σ floor(pf)
            = (p-1)(n/2 - 1) - Σ floor(pf)
            = (p-1)(n-2)/2 - Σ floor(pf)

    The sum Σ floor(pf) for f in F_{p-1} (excluding f=1) is related to...
    the Dedekind sum? Or more precisely, it counts lattice points.

    Actually: Σ_{a/b in F_{p-1}, f<1} floor(p·a/b)
    = Σ_{b=1}^{p-1} Σ_{a=0}^{b-1} [gcd(a,b)=1] · floor(pa/b)

    This is a variant of the Franel-Landau sum.
    """
    print("\n" + "=" * 90)
    print("ANALYSIS OF S1 = Σ D_{p-1}(k/p)")
    print("=" * 90)
    print()

    primes = [p for p in range(2, max_p + 1) if is_prime(p)]

    print(f"{'p':>4} {'M(p)':>5} {'n':>6} {'S1':>12} "
          f"{'S1/n':>10} {'S1/(p-1)':>10} {'M(p)/S1':>10}")
    print("-" * 75)

    data = []
    for p in primes:
        Mp = mertens(p)
        F_old = farey_float(p - 1)
        n = len(F_old)

        S1 = sum(bisect.bisect_left(F_old, k / p) - n * k / p
                 for k in range(1, p))

        data.append({'p': p, 'Mp': Mp, 'n': n, 'S1': S1})

        ratio_m = Mp / S1 if abs(S1) > 1e-10 else 0

        if p <= 50 or Mp <= -3:
            print(f"{p:4d} {Mp:5d} {n:6d} {S1:12.4f} "
                  f"{S1 / n:10.6f} {S1 / (p - 1):10.6f} {ratio_m:10.4f}")

    # Is there a simple relationship between S1 and M(p)?
    print()
    print("Checking S1 vs known quantities:")
    for d in data:
        if d['Mp'] <= -3 and d['p'] <= 100:
            # Σ floor(pf) for f in F_{p-1}
            p = d['p']
            F = farey_float(p - 1)
            n = len(F)
            sum_floor = sum(floor(p * f) for f in F if f < 1)
            S1_check = (p - 1) * (n - 2) / 2 - sum_floor
            print(f"  p={p}: S1={d['S1']:.4f}, (p-1)(n-2)/2 - Σfloor={S1_check:.4f}, "
                  f"Σfloor(pf)={sum_floor}")


# ================================================================
# THE REAL KEY: What makes D_new_sq + cross + delta_sq > dilution?
# ================================================================
def the_real_bound(max_p=500):
    """
    Since D_new_sq alone sometimes falls below dilution (ratio ~ 0.98-1.00),
    we MUST include cross + delta_sq.

    The W-free inequality is:
      dilution ≤ cross + delta_sq + D_new_sq

    Rewritten: 0 ≤ cross + delta_sq + D_new_sq - dilution

    Let's understand each term GEOMETRICALLY.

    cross = 2·Σ D_old(f)·δ(f) where δ(f) = D_new(f) - D_old(f) for old fracs f.

    For old fraction f with old rank j, new rank j' = j + #{new fracs < f} = j + floor(pf) - [f=1?*correction].
    Actually: j' = j + #{k/p < f, 1<=k<p} = j + ceil(pf) - 1 for f > 0.
    Hmm, let me just use: j' = bisect_left(F_new, f).

    δ(f) = D_new(f) - D_old(f) = (j' - n'f) - (j - nf) = (j' - j) - (n' - n)f = shift(f) - (p-1)f.

    shift(f) = #{k/p : 1<=k<p, k/p < f} = ceil(pf) - 1 for f > 0, 0 for f=0.
    Actually: #{k in 1..p-1 : k/p < f} = #{k : k < pf} = ceil(pf) - 1 for f > 0.
    For f = a/b with b < p (p prime), pf = pa/b is never integer.
    So ceil(pf) = floor(pf) + 1.
    shift(f) = floor(pf) + 1 - 1 = floor(pf).

    Wait, that's for f > 0. For f = 0: no k/p is < 0, so shift = 0.
    For f = 1: k/p < 1 means k < p, so k=1,...,p-1, shift = p-1.
    Check: floor(p·1) = p, but shift should be p-1. So for f=1, shift = p-1 not floor(pf) = p.

    OK so: shift(f) = #{k in 1..p-1 : k < pf} = min(p-1, floor(pf)) for f > 0, and 0 for f=0.
    For f < 1 and f > 0: pf < p, so floor(pf) < p, and floor(pf) <= p-1, so shift = floor(pf).
    For f = 1: shift = p - 1.
    For f = 0: shift = 0 = floor(0) = 0.

    So shift(f) = floor(pf) for f in [0,1), and p-1 for f = 1.

    Then: δ(f) = floor(pf) - (p-1)f for f < 1, and (p-1) - (p-1) = 0 for f = 1.

    For f = 0: δ = 0 - 0 = 0.
    For f = 1: δ = 0.
    For 0 < f < 1: δ(f) = floor(pf) - (p-1)f = floor(pf) - pf + f = -{pf} + f
    where {x} = x - floor(x) is the fractional part.

    So δ(f) = f - {pf}.

    THIS IS THE KEY: δ(f) = f - {pf} for each old fraction f in F_{p-1}.

    Now: cross = 2·Σ D_old(f)·(f - {pf})
    And: delta_sq = Σ (f - {pf})²

    The term {pf} for f = a/b (with gcd(a,b)=1, b < p) is:
    {pa/b} = pa/b - floor(pa/b) = (pa mod b) / b

    Since p prime and gcd(a,b)=1 with b < p, we have gcd(p,b)=1.
    So pa mod b runs through all residues mod b as a varies.
    Specifically: {pa/b} = (pa mod b) / b.

    The set {{pa/b} : a=0,...,b-1, gcd(a,b)=1} is a PERMUTATION of
    {a/b : a=0,...,b-1, gcd(a,b)=1}. (Since multiplication by p is a bijection mod b.)

    This means: for each denominator b, the values {pf} for f=a/b
    are just a permutation of the values f themselves!

    So Σ_{a: gcd(a,b)=1} {pa/b} = Σ_{a: gcd(a,b)=1} a/b.

    This means: Σ {pf} over all f in F_{p-1} with denominator b
    = Σ a/b over all a coprime to b with 0 <= a < b = (1/b)·Σ a = φ(b)/2.
    Wait, Σ_{a=0, gcd(a,b)=1}^{b-1} a/b = (1/b)·Σ a... for b > 1 this is φ(b)/2.

    Actually Σ_{a=1, gcd(a,b)=1}^{b-1} a = b·φ(b)/2 (well-known identity for b > 1).
    So Σ a/b = φ(b)/2 for b >= 2.

    And similarly Σ_{a: gcd(a,b)=1, 0<a<b} {pa/b} = φ(b)/2.

    So the AVERAGE δ for fractions with denominator b is:
    avg δ_b = (1/φ(b))·Σ[f - {pf}] = (1/φ(b))·[Σ a/b - Σ {pa/b}] = (1/φ(b))·[φ(b)/2 - φ(b)/2] = 0.

    The AVERAGE δ is ZERO for each denominator group!
    This means cross = 2·Σ D·δ might be small because δ averages to zero.

    Let's see what happens to Σ δ² = Σ (f - {pf})².
    """
    print("\n" + "=" * 90)
    print("THE KEY: δ(f) = f - {pf} AND ITS PROPERTIES")
    print("=" * 90)
    print()

    primes = [p for p in range(2, max_p + 1) if is_prime(p)]

    print("Verifying δ(f) = f - {pf}:")
    for p in [5, 7, 11, 13, 17]:
        F_old = farey_float(p - 1)
        F_new = farey_float(p)
        n = len(F_old)
        n_new = n + p - 1
        all_ok = True
        for j, f in enumerate(F_old):
            if f == 0 or f == 1:
                continue
            # Compute δ = f - {pf}
            pf = p * f
            frac_pf = pf - floor(pf)
            delta_formula = f - frac_pf

            # Compute δ directly
            j_new = bisect.bisect_left(F_new, f - 1e-15)
            while j_new < len(F_new) and abs(F_new[j_new] - f) > 1e-12:
                j_new += 1
            D_new = j_new - n_new * f
            D_old = j - n * f
            delta_direct = D_new - D_old

            if abs(delta_formula - delta_direct) > 1e-8:
                all_ok = False
                if j < 5:
                    print(f"  p={p}, f={f:.6f}: δ_formula={delta_formula:.8f}, "
                          f"δ_direct={delta_direct:.8f}")
        print(f"  p={p:3d}: δ(f) = f - {{pf}} {'VERIFIED' if all_ok else 'FAILED'}")

    # Now compute the full inequality components
    print()
    print("FULL W-FREE INEQUALITY DECOMPOSITION:")
    print(f"{'p':>4} {'M(p)':>5} {'n':>6} "
          f"{'dilution':>12} {'D_new²':>12} {'cross':>12} {'δ²':>12} "
          f"{'RHS':>12} {'margin':>12} {'δ²/dil':>8}")
    print("-" * 125)

    summary = []
    for p in primes:
        Mp = mertens(p)
        F_old = farey_float(p - 1)
        F_new = farey_float(p)
        n = len(F_old)
        n_new = n + p - 1

        Q = sum((j - n * f) ** 2 for j, f in enumerate(F_old))
        dilution = Q * (n_new ** 2 - n ** 2) / n ** 2

        # D_new_sq for new fractions
        D_new_sq = 0.0
        for k in range(1, p):
            x = k / p
            idx = bisect.bisect_left(F_new, x - 1e-15)
            while idx < len(F_new) and F_new[idx] < x - 1e-12:
                idx += 1
            D = idx - n_new * x
            D_new_sq += D * D

        # cross and delta_sq using δ = f - {pf}
        cross = 0.0
        delta_sq = 0.0
        for j, f in enumerate(F_old):
            D_old = j - n * f
            if f == 0 or f == 1:
                delta = 0.0
            else:
                pf = p * f
                delta = f - (pf - floor(pf))
            cross += D_old * delta
            delta_sq += delta * delta
        cross *= 2

        RHS = D_new_sq + cross + delta_sq
        margin = RHS - dilution
        ratio_dsq = delta_sq / dilution if dilution > 0 else 0

        summary.append({
            'p': p, 'Mp': Mp, 'n': n,
            'dilution': dilution, 'D_new_sq': D_new_sq,
            'cross': cross, 'delta_sq': delta_sq,
            'RHS': RHS, 'margin': margin, 'Q': Q
        })

        if p <= 50 or Mp <= -3 or p in [199, 281, 499]:
            print(f"{p:4d} {Mp:5d} {n:6d} "
                  f"{dilution:12.4f} {D_new_sq:12.4f} {cross:12.4f} {delta_sq:12.4f} "
                  f"{RHS:12.4f} {margin:12.4f} {ratio_dsq:8.4f}")

    print()
    m3 = [d for d in summary if d['Mp'] <= -3 and d['p'] >= 11]
    print(f"M(p) <= -3 primes (p >= 11): {len(m3)}")
    if m3:
        margins = [d['margin'] for d in m3]
        print(f"  Min margin: {min(margins):.6f}")
        print(f"  All margins > 0: {all(m > -0.01 for m in margins)}")

        # What fraction of RHS comes from each component?
        print()
        print("COMPONENT FRACTIONS OF RHS:")
        print(f"{'p':>4} {'M(p)':>5} {'Dnew²/RHS':>12} {'cross/RHS':>12} {'δ²/RHS':>12}")
        print("-" * 55)
        for d in m3:
            if d['RHS'] > 0:
                print(f"{d['p']:4d} {d['Mp']:5d} "
                      f"{d['D_new_sq'] / d['RHS']:12.6f} "
                      f"{d['cross'] / d['RHS']:12.6f} "
                      f"{d['delta_sq'] / d['RHS']:12.6f}")

    # KEY INSIGHT: delta_sq = Σ (f - {pf})² is a KLOOSTERMAN-type sum.
    # The cross term = 2·Σ D_old·(f - {pf}).
    # Can we bound cross + delta_sq from below INDEPENDENTLY of Q?
    print()
    print("INDEPENDENCE FROM Q:")
    print("Can cross + δ² be bounded without Q?")
    print(f"{'p':>4} {'M(p)':>5} {'cross+δ²':>12} {'cross':>12} {'δ²':>12} "
          f"{'needed':>12} {'surplus':>12}")
    print("-" * 85)
    for d in m3[:20]:
        needed = d['dilution'] - d['D_new_sq']  # what cross+δ² must exceed
        surplus = d['cross'] + d['delta_sq'] - needed
        print(f"{d['p']:4d} {d['Mp']:5d} "
              f"{d['cross'] + d['delta_sq']:12.4f} {d['cross']:12.4f} "
              f"{d['delta_sq']:12.4f} {needed:12.4f} {surplus:12.4f}")

    return summary


# ================================================================
# FINAL: Test the geometric insight about Farey self-avoidance
# ================================================================
def farey_self_avoidance(max_p=300):
    """
    GEOMETRIC INSIGHT: Farey fractions "self-correct" — they are placed
    where D is small. Equispaced points don't have this property.

    Measure this: compare avg D² at Farey points vs avg D² at equispaced points.
    If the ratio avg_equi/avg_farey > 2, then A > 2·(p-1)·Q/n and we win
    without needing cross or delta_sq.

    But we showed alpha ~ 2, not always > 2. So we need a tighter argument.

    ALTERNATIVE GEOMETRIC IDEA: The displacement function D_{p-1}(x) has
    a NEGATIVE BIAS at Farey points. Because each Farey fraction "resets"
    D toward 0. Between Farey fractions, D drifts linearly.

    The equispaced points k/p sample D without this reset, so they see
    the full range of D fluctuations.

    Can we prove: Σ D²(k/p) ≥ (2 - ε)·(p-1)·Q/n + lower_order?
    If so, with B + C providing the extra margin, we'd be done.
    """
    print("\n" + "=" * 90)
    print("FAREY SELF-AVOIDANCE: comparing D² at different point sets")
    print("=" * 90)
    print()

    primes = [p for p in range(2, max_p + 1) if is_prime(p)]

    print(f"{'p':>4} {'M(p)':>5} {'n':>6} "
          f"{'avg_D²_farey':>14} {'avg_D²_equi':>14} "
          f"{'alpha=ratio':>12} {'∫D²dx/(n-1)':>14} {'integ/farey':>12}")
    print("-" * 110)

    for p in primes:
        Mp = mertens(p)
        F = farey_float(p - 1)
        n = len(F)

        # avg D² at Farey points
        Q = sum((j - n * f) ** 2 for j, f in enumerate(F))
        avg_farey = Q / n

        # avg D² at equispaced points k/p
        sum_D2_equi = sum((bisect.bisect_left(F, k / p) - n * k / p) ** 2
                          for k in range(1, p))
        avg_equi = sum_D2_equi / (p - 1)

        alpha = avg_equi / avg_farey if avg_farey > 0 else 0

        # ∫ D²(x) dx
        integral_D2 = 0.0
        for j in range(n - 1):
            fj, fj1 = F[j], F[j + 1]
            a = j - n * fj
            b_val = j - n * fj1
            integral_D2 += (a ** 3 - b_val ** 3) / (3 * n)
        avg_integral = integral_D2 / 1.0  # integral over [0,1]

        ratio_int_farey = avg_integral / avg_farey if avg_farey > 0 else 0

        if p <= 50 or Mp <= -3:
            print(f"{p:4d} {Mp:5d} {n:6d} "
                  f"{avg_farey:14.6f} {avg_equi:14.6f} "
                  f"{alpha:12.6f} {avg_integral:14.6f} {ratio_int_farey:12.6f}")

    print()
    print("INSIGHT: alpha = avg_equi/avg_farey oscillates around 2.")
    print("The integral of D² is another reference measure.")
    print("avg_integral/avg_farey shows the integral is about 2/3 of the Farey average.")
    print()
    print("This means ∫D² ≈ (2/3)·Q/n, so (n-1)·∫D² ≈ (2/3)·Q.")
    print("And Σ D²(k/p) ≈ (p-1)·∫D² ≈ (2/3)·(p-1)·Q/n · (n/(n-1)) ≈ 2·(p-1)·Q/(3n)... wait")
    print("No: avg_equi ≈ alpha·avg_farey ≈ 2·avg_farey.")
    print("And avg_integral ≈ ratio_int_farey · avg_farey.")
    print("So the equispaced average is LARGER than both the Farey and integral averages.")


# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    print("GEOMETRIC PROOF ATTEMPTS FOR ΔW(p) < 0 WHEN M(p) <= -3")
    print("=" * 90)
    print()

    # Phase 1: Verify the coupling identity exactly
    test_coupling_identity(max_p=50)

    # Phase 2: Gap variance (quick check)
    test_idea1(max_p=100)

    # Phase 3: Corrected decomposition
    all_data = corrected_decomposition(max_p=300)

    # Phase 4: Analyze S1
    analyze_S1(max_p=100)

    # Phase 5: The real bound with δ = f - {pf}
    summary = the_real_bound(max_p=500)

    # Phase 6: Self-avoidance
    farey_self_avoidance(max_p=200)
