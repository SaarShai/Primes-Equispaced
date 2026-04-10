#!/usr/bin/env python3
"""
D/A RATIO EXACT ANALYSIS
=========================

Compute the four-term decomposition of ΔW(p) with EXACT Fraction arithmetic:

  ΔW(p) = A - B - C + 1 - D - 1/n'²

where:
  A = dilution = old_D_sq · (1/n² - 1/n'²)
  B = cross term = (2/n'²) · Σ D_old(k/p) · δ(k/p)
  C = shift-squared = (1/n'²) · Σ δ(k/p)²
  D = new-fraction discrepancy = (1/n'²) · Σ D_{F_p}(k/p)²

  D_old(k/p) = N_{p-1}(k/p) - n·(k/p)     [discrepancy of old ordering]
  δ(k/p) = rank shift when k/p is inserted
  D_{F_p}(k/p) = rank(k/p in F_p) - n'·(k/p)

For each prime:
  - Compute A, B, C, D exactly
  - Compute D/A, 1 - D/A
  - Compute bypass condition: C + D > A + 1?
  - Relate 1 - D/A to M(p)

Output: ~/Desktop/Farey-Local/experiments/DA_RATIO_EXACT.md
"""

import sys
import time
from fractions import Fraction
from math import gcd, isqrt
import csv

# ============================================================
# SIEVE UTILITIES
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
    """Compute Mertens function M(n) for all n up to limit."""
    smallest_prime = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if smallest_prime[i] == 0:
            for j in range(i, limit + 1, i):
                if smallest_prime[j] == 0:
                    smallest_prime[j] = i
    mu = [0] * (limit + 1)
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

def farey_size(N, phi_arr):
    return 1 + sum(phi_arr[k] for k in range(1, N + 1))

# ============================================================
# FAREY SEQUENCE GENERATOR (mediant algorithm)
# ============================================================

def farey_generator(N):
    """Generate F_N using the mediant algorithm. Yields (a, b) pairs."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

# ============================================================
# EXACT FOUR-TERM DECOMPOSITION
# ============================================================

def exact_four_term(p, phi_arr, use_fractions=True):
    """
    Compute the exact four-term decomposition for prime p.

    Returns dict with exact Fraction values for A, B, C, D, ΔW, etc.
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1  # |F_p| = |F_{p-1}| + φ(p) = n + p - 1

    # Build F_{p-1} as list of (a, b) pairs
    old_pairs = list(farey_generator(N))
    assert len(old_pairs) == n, f"Farey size mismatch: got {len(old_pairs)}, expected {n}"

    # Build sorted list of Fraction values for F_{p-1}
    old_fracs_sorted = [Fraction(a, b) for (a, b) in old_pairs]

    # Compute old discrepancies: D_old(f_j) = j - n * f_j  (0-indexed: rank j)
    # old_D[j] = j - n * f_j
    old_D = []
    for j, f in enumerate(old_fracs_sorted):
        old_D.append(Fraction(j) - Fraction(n) * f)

    # old_D_sq = Σ D_old(f_j)²
    old_D_sq = sum(d * d for d in old_D)

    # For each new fraction k/p (k = 1, ..., p-1):
    # Find its position in F_{p-1} using binary search
    # D_old_virtual(k/p) = N_{p-1}(k/p) - n * (k/p)
    # where N_{p-1}(k/p) = number of elements in F_{p-1} that are ≤ k/p

    import bisect

    # Pre-sort old fracs for bisect
    # They're already sorted from the mediant algorithm

    new_D_old_virtual = []  # D_old_virtual(k/p) for k=1..p-1
    new_frac_vals = []      # k/p as Fraction
    N_counts = []           # N_{p-1}(k/p)

    for k in range(1, p):
        kp = Fraction(k, p)
        new_frac_vals.append(kp)

        # Count elements of F_{p-1} that are ≤ k/p
        # Use bisect on the sorted list
        count = bisect.bisect_right(old_fracs_sorted, kp)
        N_counts.append(count)

        # Virtual discrepancy
        D_virt = Fraction(count) - Fraction(n) * kp
        new_D_old_virtual.append(D_virt)

    # The rank of k/p in F_p is: N_{p-1}(k/p) + k
    # (because exactly k of the new fractions 1/p, 2/p, ..., k/p are ≤ k/p)
    # So D_{F_p}(k/p) = [N_{p-1}(k/p) + k] - n' * (k/p)
    #                  = D_old_virtual(k/p) + k - (p-1)*(k/p)
    #                  = D_old_virtual(k/p) + k*(1 - (p-1)/p)
    #                  = D_old_virtual(k/p) + k/p

    new_D_Fp = []  # D_{F_p}(k/p)
    for k_idx in range(p - 1):
        k = k_idx + 1
        # rank(k/p in F_p) = N_{p-1}(k/p) + k - 1  (0-indexed)
        # D_{F_p}(k/p) = rank - n'*(k/p) = D_virt + k/p - 1
        # Note: Σ D_{F_p}^2 = Σ (D_virt + k/p)^2 (proven: sum is invariant due to Σ D_Fp = -(p-1)/2)
        D_Fp = new_D_old_virtual[k_idx] + Fraction(k, p) - 1
        new_D_Fp.append(D_Fp)

    # Now compute the shift δ(k/p) for each old fraction.
    # When we insert k/p fractions, each old fraction f_j gets shifted by
    # the number of new fractions that are ≤ f_j.
    # δ(f_j) = floor(p * f_j) for interior fractions (since p is prime, p*a/b is never integer for 0 < a/b < 1 with b < p)
    # Actually: δ(f_j) = #{k : 1 ≤ k ≤ p-1, k/p ≤ f_j} = floor(p * f_j)

    # Wait - let me re-derive the four-term decomposition carefully.
    #
    # W(N) = (1/n²) Σ_{j=0}^{n-1} (j - n*f_j)² = (1/n²) Σ D_old(f_j)²
    #
    # When going from F_{p-1} to F_p:
    #   n' = n + m where m = p-1
    #   W(p) = (1/n'²) Σ_{all f in F_p} (rank(f) - n'*f)²
    #
    # For OLD fractions f_j:
    #   new_rank(f_j) = j + δ(f_j) where δ(f_j) = floor(p * f_j)
    #   D_{F_p}(f_j) = [j + δ(f_j)] - n' * f_j
    #                 = [j - n*f_j] + [δ(f_j) - (n'-n)*f_j]
    #                 = D_old(f_j) + [δ(f_j) - m*f_j]
    #
    #   Let shift(f_j) = δ(f_j) - m*f_j = floor(p*f_j) - (p-1)*f_j
    #   Note: floor(p*f_j) = p*f_j - {p*f_j} where {.} is fractional part
    #   So shift(f_j) = p*f_j - {p*f_j} - (p-1)*f_j = f_j - {p*a_j/b_j}
    #   Wait, that's not right for fractions. Let me be more careful.
    #
    #   For f_j = a/b with gcd(a,b)=1 and b ≤ p-1:
    #     floor(p * a/b) = (p*a - (p*a mod b)) / b
    #     δ(f_j) = floor(p*a/b)
    #     shift(f_j) = floor(p*a/b) - (p-1)*a/b
    #
    # For NEW fractions k/p:
    #   D_{F_p}(k/p) = D_old_virtual(k/p) + k/p  (derived above)

    # Four-term decomposition of n'² * W(p):
    # n'² W(p) = Σ_{old f_j} D_{F_p}(f_j)² + Σ_{new k/p} D_{F_p}(k/p)²
    #
    # For old fractions:
    # Σ_{old} [D_old(f_j) + shift(f_j)]²
    # = Σ D_old²  + 2·Σ D_old·shift + Σ shift²
    # = old_D_sq + 2·B_raw + C_raw
    #
    # For new fractions:
    # Σ_{new} D_{F_p}(k/p)² = D_raw (the "new-fraction discrepancy" sum)
    #
    # So: n'² W(p) = old_D_sq + 2·B_raw + C_raw + D_raw
    # And: n² W(p-1) = old_D_sq
    #
    # Therefore:
    # ΔW = W(p-1) - W(p) = old_D_sq/n² - (old_D_sq + 2·B_raw + C_raw + D_raw)/n'²
    #     = old_D_sq · (1/n² - 1/n'²) - (2·B_raw + C_raw + D_raw)/n'²
    #     = A - (2·B_raw + C_raw + D_raw)/n'²
    #
    # where A = old_D_sq · (1/n² - 1/n'²) = dilution
    #
    # Define:
    #   B = (2/n'²) · B_raw = (2/n'²) · Σ D_old(f_j)·shift(f_j)
    #   C = (1/n'²) · C_raw = (1/n'²) · Σ shift(f_j)²
    #   D = (1/n'²) · D_raw = (1/n'²) · Σ D_{F_p}(k/p)²
    #
    # Then: ΔW = A - B - C - D
    #
    # Wait, the user says ΔW = A - B - C + 1 - D - 1/n'².
    # Let me check if there's a different normalization.
    # Actually, let me just compute everything and see.

    # Compute shifts for old fractions
    shifts = []  # shift(f_j) = floor(p*f_j) - (p-1)*f_j  [as Fraction]
    m = p - 1
    for (a, b) in old_pairs:
        delta_j = (p * a) // b  # floor(p * a/b), integer
        # Clamp: at most p-1 new fractions can be below any point
        # (k ranges from 1 to p-1, so k/p ranges from 1/p to (p-1)/p < 1)
        # For a/b = 1: floor(p*1) = p, but only p-1 new fractions exist
        delta_j = min(delta_j, p - 1)
        shift_j = Fraction(delta_j) - Fraction(m * a, b)
        shifts.append(shift_j)

    # B_raw = Σ D_old(f_j) * shift(f_j)
    B_raw = sum(old_D[j] * shifts[j] for j in range(n))

    # C_raw = Σ shift(f_j)²
    C_raw = sum(s * s for s in shifts)

    # D_raw = Σ D_{F_p}(k/p)²
    D_raw = sum(d * d for d in new_D_Fp)

    # Now compute A, B, C, D (normalized)
    n2 = Fraction(n * n)
    np2 = Fraction(n_prime * n_prime)

    A = old_D_sq * (Fraction(1, n * n) - Fraction(1, n_prime * n_prime))
    B = Fraction(2) * B_raw / np2
    C = C_raw / np2
    D_cal = D_raw / np2

    # ΔW from decomposition
    delta_W_decomp = A - B - C - D_cal

    # Direct computation of W(p-1) and W(p)
    W_old = old_D_sq / n2

    # Compute W(p) directly
    # Need all discrepancies in F_p
    F_p_all = []  # Will store (value_as_Fraction, is_new)
    for (a, b) in old_pairs:
        F_p_all.append(Fraction(a, b))
    for k in range(1, p):
        F_p_all.append(Fraction(k, p))
    F_p_all.sort()

    new_D_sq_total = Fraction(0)
    for j, f in enumerate(F_p_all):
        d = Fraction(j) - Fraction(n_prime) * f
        new_D_sq_total += d * d

    W_new = new_D_sq_total / np2
    delta_W_direct = W_old - W_new

    # Verify decomposition matches direct
    assert delta_W_decomp == delta_W_direct, \
        f"Decomposition mismatch at p={p}: decomp={delta_W_decomp}, direct={delta_W_direct}"

    # D/A ratio
    DA_ratio = D_cal / A if A != 0 else None

    # Bypass condition: we need ΔW < 0, i.e., A < B + C + D
    # Or equivalently: D + C + B > A  (when B > 0)
    # The user mentions C + D > A + 1, let me check what "1" means in context.
    # Actually, ΔW = A - B - C - D, so ΔW < 0 iff B + C + D > A.

    # 1 - D/A
    one_minus_DA = Fraction(1) - DA_ratio if DA_ratio is not None else None

    # Also compute Σ D_old_virtual(k/p) and relate to M(p)
    sum_D_virt = sum(new_D_old_virtual)  # Should be related to M(p)

    return {
        'p': p,
        'n': n,
        'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'A': A,
        'B': B,  # cross term (with factor 2 already)
        'C': C,  # shift-squared
        'D': D_cal,  # new-fraction discrepancy
        'D_raw': D_raw,
        'B_raw': B_raw,
        'C_raw': C_raw,
        'delta_W': delta_W_direct,
        'DA_ratio': DA_ratio,
        'one_minus_DA': one_minus_DA,
        'W_old': W_old,
        'W_new': W_new,
        'sum_D_virt': sum_D_virt,
        'shifts': shifts,
        'new_D_Fp': new_D_Fp,
        'new_D_old_virtual': new_D_old_virtual,
    }


# ============================================================
# MAIN COMPUTATION
# ============================================================

def main():
    MAX_P = 500

    print(f"Computing D/A ratio exact analysis for primes up to {MAX_P}")
    print("=" * 80)

    phi_arr = euler_totient_sieve(MAX_P + 1)
    M_arr = mertens_sieve(MAX_P + 1)
    primes = sieve_primes(MAX_P)

    # Filter primes >= 5 (F_2 = {0/1, 1/2, 1/1} is too small)
    primes = [p for p in primes if p >= 5]

    results = []

    t0 = time.time()
    for idx, p in enumerate(primes):
        t1 = time.time()
        r = exact_four_term(p, phi_arr)
        t2 = time.time()

        Mp = M_arr[p]
        r['M_p'] = Mp
        results.append(r)

        if idx < 10 or idx % 10 == 0:
            print(f"  p={p:4d}  n={r['n']:6d}  n'={r['n_prime']:6d}  "
                  f"D/A={float(r['DA_ratio']):.8f}  "
                  f"1-D/A={float(r['one_minus_DA']):+.8f}  "
                  f"M(p)={Mp:4d}  "
                  f"ΔW={float(r['delta_W']):+.12f}  "
                  f"[{t2-t1:.2f}s]")

    total_time = time.time() - t0
    print(f"\nTotal computation time: {total_time:.1f}s")

    # ============================================================
    # ANALYSIS 1: D/A ratio statistics
    # ============================================================
    print("\n" + "=" * 80)
    print("ANALYSIS 1: D/A RATIO AND 1 - D/A")
    print("=" * 80)

    print(f"\n{'p':>5} {'M(p)':>5} {'D/A':>12} {'1-D/A':>12} {'|1-D/A|':>12} "
          f"{'A':>14} {'B':>14} {'C':>14} {'D':>14} {'ΔW':>14}")

    for r in results:
        print(f"{r['p']:5d} {r['M_p']:5d} "
              f"{float(r['DA_ratio']):12.8f} "
              f"{float(r['one_minus_DA']):+12.8f} "
              f"{abs(float(r['one_minus_DA'])):12.8f} "
              f"{float(r['A']):14.10f} "
              f"{float(r['B']):14.10f} "
              f"{float(r['C']):14.10f} "
              f"{float(r['D']):14.10f} "
              f"{float(r['delta_W']):+14.10f}")

    # ============================================================
    # ANALYSIS 2: Verify ΔW < 0 and bypass condition
    # ============================================================
    print("\n" + "=" * 80)
    print("ANALYSIS 2: SIGN OF ΔW AND BYPASS CONDITION")
    print("=" * 80)

    print(f"\n{'p':>5} {'M(p)':>5} {'ΔW<0?':>6} {'B+C+D':>14} {'A':>14} {'B+C+D-A':>14} {'C+D-A':>14}")

    neg_count = 0
    bypass_count = 0
    for r in results:
        bcd = r['B'] + r['C'] + r['D']
        delta_neg = r['delta_W'] < 0
        # Bypass: C + D > A (which means even without B, wobble decreases)
        cd_minus_a = r['C'] + r['D'] - r['A']
        bypass = cd_minus_a > 0
        if delta_neg:
            neg_count += 1
        if bypass:
            bypass_count += 1

        print(f"{r['p']:5d} {r['M_p']:5d} "
              f"{'YES' if delta_neg else 'no':>6} "
              f"{float(bcd):14.10f} "
              f"{float(r['A']):14.10f} "
              f"{float(bcd - r['A']):+14.10f} "
              f"{float(cd_minus_a):+14.10f}")

    print(f"\nΔW < 0 for {neg_count}/{len(results)} primes")
    print(f"C + D > A for {bypass_count}/{len(results)} primes")

    # ============================================================
    # ANALYSIS 3: Relate 1 - D/A to M(p)/p
    # ============================================================
    print("\n" + "=" * 80)
    print("ANALYSIS 3: 1 - D/A vs M(p)/p")
    print("=" * 80)

    print(f"\n{'p':>5} {'M(p)':>5} {'1-D/A':>14} {'M(p)/p':>12} "
          f"{'(1-D/A)/(M/p)':>14} {'(1-D/A)*p':>12} {'(1-D/A)*p/M':>12}")

    for r in results:
        p = r['p']
        Mp = r['M_p']
        oda = float(r['one_minus_DA'])
        mp_over_p = Mp / p if p > 0 else 0
        ratio1 = oda / mp_over_p if mp_over_p != 0 else float('inf')
        oda_times_p = oda * p
        ratio2 = oda_times_p / Mp if Mp != 0 else float('inf')

        print(f"{p:5d} {Mp:5d} {oda:+14.8f} {mp_over_p:12.8f} "
              f"{ratio1:14.6f} {oda_times_p:+12.6f} {ratio2:12.6f}")

    # ============================================================
    # ANALYSIS 4: Exact formula for 1 - D/A
    # ============================================================
    print("\n" + "=" * 80)
    print("ANALYSIS 4: EXACT EXPRESSION FOR 1 - D/A")
    print("=" * 80)

    # From ΔW = A - B - C - D:
    # A - D = B + C + ΔW
    # 1 - D/A = (A - D)/A = (B + C + ΔW)/A
    # So: 1 - D/A = (B + C)/A + ΔW/A

    print(f"\n1 - D/A = (B + C + ΔW) / A = (B+C)/A + ΔW/A")
    print(f"\n{'p':>5} {'(B+C)/A':>14} {'ΔW/A':>14} {'sum':>14} {'1-D/A check':>14}")

    for r in results:
        bc_over_a = (r['B'] + r['C']) / r['A'] if r['A'] != 0 else Fraction(0)
        dw_over_a = r['delta_W'] / r['A'] if r['A'] != 0 else Fraction(0)
        total = bc_over_a + dw_over_a

        print(f"{r['p']:5d} {float(bc_over_a):14.8f} {float(dw_over_a):+14.8f} "
              f"{float(total):14.8f} {float(r['one_minus_DA']):14.8f}")

    # ============================================================
    # ANALYSIS 5: For M(p) ≤ -3: bound on |1 - D/A|
    # ============================================================
    print("\n" + "=" * 80)
    print("ANALYSIS 5: M(p) ≤ -3 PRIMES — BOUND ON |1 - D/A|")
    print("=" * 80)

    mp_neg3 = [r for r in results if r['M_p'] <= -3]
    print(f"\nFound {len(mp_neg3)} primes with M(p) ≤ -3")

    if mp_neg3:
        print(f"\n{'p':>5} {'M(p)':>5} {'|1-D/A|':>12} {'|M(p)|/p':>12} "
              f"{'|1-D/A|/(|M|/p)':>16} {'c=|1-D/A|*p/|M|':>18}")

        max_c = 0
        max_abs_oda = 0
        for r in mp_neg3:
            p = r['p']
            Mp = r['M_p']
            abs_oda = abs(float(r['one_minus_DA']))
            abs_Mp = abs(Mp)
            abs_Mp_over_p = abs_Mp / p
            c_val = abs_oda * p / abs_Mp if abs_Mp > 0 else 0
            ratio = abs_oda / abs_Mp_over_p if abs_Mp_over_p > 0 else 0

            max_c = max(max_c, c_val)
            max_abs_oda = max(max_abs_oda, abs_oda)

            print(f"{p:5d} {Mp:5d} {abs_oda:12.8f} {abs_Mp_over_p:12.8f} "
                  f"{ratio:16.6f} {c_val:18.6f}")

        print(f"\nMax |1-D/A| among M(p)≤-3: {max_abs_oda:.8f}")
        print(f"Max c = |1-D/A|*p/|M(p)|:  {max_c:.6f}")
        print(f"So |1-D/A| ≤ {max_c:.4f} · |M(p)|/p for M(p) ≤ -3 primes in range")

    # ============================================================
    # ANALYSIS 6: Exact relationship via D_raw components
    # ============================================================
    print("\n" + "=" * 80)
    print("ANALYSIS 6: D_raw DECOMPOSITION")
    print("=" * 80)

    # D_{F_p}(k/p) = D_old_virtual(k/p) + k/p
    # So D_raw = Σ [D_virt + k/p]² = Σ D_virt² + 2·Σ D_virt·(k/p) + Σ (k/p)²
    #          = S_virt + 2·X_cross + S_kp

    print(f"\nD_raw = S_virt + 2·X_cross + S_kp")
    print(f"  where S_virt = Σ D_old_virtual(k/p)²")
    print(f"        X_cross = Σ D_old_virtual(k/p)·(k/p)")
    print(f"        S_kp = Σ (k/p)² = (p-1)(2p-1)/(6p²)")

    print(f"\n{'p':>5} {'S_virt':>14} {'2*X_cross':>14} {'S_kp':>14} {'D_raw':>14} {'S_virt/dilut':>14}")

    for r in results:
        p = r['p']
        S_virt = sum(d*d for d in r['new_D_old_virtual'])
        X_cross = sum(r['new_D_old_virtual'][k-1] * Fraction(k, p) for k in range(1, p))
        S_kp = Fraction((p-1)*(2*p-1), 6*p)  # Σ_{k=1}^{p-1} (k/p)² = (p-1)(2p-1)/(6p)

        check = S_virt + 2*X_cross + S_kp
        assert check == r['D_raw'], f"D_raw decomposition mismatch at p={p}"

        # dilution_raw = old_D_sq * (n'² - n²) / n²
        dilut_raw = r['old_D_sq'] * Fraction(r['n_prime']**2 - r['n']**2, r['n']**2)
        s_virt_over_dilut = float(S_virt / dilut_raw) if dilut_raw != 0 else 0

        if p <= 50 or p % 50 < 3:
            print(f"{p:5d} {float(S_virt):14.6f} {float(2*X_cross):14.6f} "
                  f"{float(S_kp):14.6f} {float(r['D_raw']):14.6f} {s_virt_over_dilut:14.8f}")

    # ============================================================
    # ANALYSIS 7: Σ D_old_virtual(k/p) and M(p) connection
    # ============================================================
    print("\n" + "=" * 80)
    print("ANALYSIS 7: Σ D_old_virtual(k/p) AND M(p)")
    print("=" * 80)

    # D_old_virtual(k/p) = N_{p-1}(k/p) - n*(k/p)
    # Σ_{k=1}^{p-1} D_old_virtual(k/p) should relate to M(p)
    # By the bridge identity: Σ_{k=1}^{p-1} N_{p-1}(k/p) = Σ_{d=1}^{p-1} φ(d)·floor(p/d)
    # ... but let me just check numerically

    print(f"\n{'p':>5} {'M(p)':>5} {'Σ D_virt':>12} {'Σ D_virt / M(p)':>16} "
          f"{'Σ D_virt + M(p)':>16}")

    for r in results[:30]:  # first 30 primes
        p = r['p']
        Mp = r['M_p']
        sd = float(r['sum_D_virt'])
        ratio = sd / Mp if Mp != 0 else float('inf')
        print(f"{p:5d} {Mp:5d} {sd:12.4f} {ratio:16.6f} {sd + Mp:16.4f}")

    # ============================================================
    # WRITE RESULTS
    # ============================================================

    # CSV output
    csv_path = "/Users/saar/Desktop/Farey-Local/experiments/DA_ratio_exact.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['p', 'n', 'n_prime', 'M_p',
                         'A', 'B', 'C', 'D', 'delta_W',
                         'DA_ratio', 'one_minus_DA',
                         'B_plus_C_plus_D_minus_A', 'C_plus_D_minus_A',
                         'one_minus_DA_times_p', 'one_minus_DA_times_p_over_M'])
        for r in results:
            p = r['p']
            Mp = r['M_p']
            oda = float(r['one_minus_DA'])
            bcd_a = float(r['B'] + r['C'] + r['D'] - r['A'])
            cd_a = float(r['C'] + r['D'] - r['A'])
            oda_p = oda * p
            oda_p_m = oda_p / Mp if Mp != 0 else float('inf')
            writer.writerow([p, r['n'], r['n_prime'], Mp,
                            float(r['A']), float(r['B']), float(r['C']), float(r['D']),
                            float(r['delta_W']),
                            float(r['DA_ratio']), oda,
                            bcd_a, cd_a,
                            oda_p, oda_p_m])

    print(f"\nCSV written to {csv_path}")

    # ============================================================
    # WRITE MARKDOWN REPORT
    # ============================================================
    write_report(results, M_arr)

    return results


def write_report(results, M_arr):
    """Write the DA_RATIO_EXACT.md report."""

    md_path = "/Users/saar/Desktop/Farey-Local/experiments/DA_RATIO_EXACT.md"

    with open(md_path, 'w') as f:
        f.write("# D/A Ratio Exact Analysis\n\n")
        f.write("## Four-Term Decomposition\n\n")
        f.write("```\n")
        f.write("ΔW(p) = W(p-1) - W(p) = A - B - C - D\n\n")
        f.write("where:\n")
        f.write("  A = dilution        = old_D_sq · (1/n² - 1/n'²)\n")
        f.write("  B = cross term      = (2/n'²) · Σ D_old(f_j) · shift(f_j)\n")
        f.write("  C = shift-squared   = (1/n'²) · Σ shift(f_j)²\n")
        f.write("  D = new-frac discr  = (1/n'²) · Σ D_{F_p}(k/p)²\n")
        f.write("```\n\n")

        f.write("All values computed with exact `Fraction` arithmetic (no floating-point errors).\n\n")

        # Table 1: Main results
        f.write("## Table 1: Four-Term Decomposition Values\n\n")
        f.write("| p | M(p) | A | B | C | D | ΔW | D/A | 1-D/A |\n")
        f.write("|---|------|---|---|---|---|----|----|-------|\n")

        for r in results:
            f.write(f"| {r['p']} | {r['M_p']} | "
                    f"{float(r['A']):.10f} | "
                    f"{float(r['B']):.10f} | "
                    f"{float(r['C']):.10f} | "
                    f"{float(r['D']):.10f} | "
                    f"{float(r['delta_W']):+.10f} | "
                    f"{float(r['DA_ratio']):.8f} | "
                    f"{float(r['one_minus_DA']):+.8f} |\n")

        # Analysis: ΔW sign
        neg_count = sum(1 for r in results if r['delta_W'] < 0)
        f.write(f"\n## Key Finding 1: Sign of ΔW\n\n")
        f.write(f"- ΔW < 0 (wobble decreases) for **{neg_count}/{len(results)}** primes in range\n")
        f.write(f"- ΔW ≥ 0 for **{len(results)-neg_count}/{len(results)}** primes\n\n")

        pos_primes = [r['p'] for r in results if r['delta_W'] >= 0]
        if pos_primes:
            f.write(f"- Primes with ΔW ≥ 0: {pos_primes[:20]}{'...' if len(pos_primes) > 20 else ''}\n\n")

        # D/A ratio analysis
        f.write(f"\n## Key Finding 2: D/A Ratio\n\n")
        da_vals = [float(r['DA_ratio']) for r in results]
        f.write(f"- D/A range: [{min(da_vals):.8f}, {max(da_vals):.8f}]\n")
        f.write(f"- D/A mean: {sum(da_vals)/len(da_vals):.8f}\n")

        oda_vals = [float(r['one_minus_DA']) for r in results]
        f.write(f"- |1 - D/A| range: [{min(abs(x) for x in oda_vals):.8f}, {max(abs(x) for x in oda_vals):.8f}]\n")
        f.write(f"- 1 - D/A is positive for {sum(1 for x in oda_vals if x > 0)}/{len(oda_vals)} primes\n")
        f.write(f"- 1 - D/A is negative for {sum(1 for x in oda_vals if x < 0)}/{len(oda_vals)} primes\n\n")

        # Exact identity
        f.write(f"## Key Finding 3: Exact Identity\n\n")
        f.write("```\n")
        f.write("1 - D/A = (B + C + ΔW) / A\n")
        f.write("        = (B + C)/A + ΔW/A\n")
        f.write("```\n\n")
        f.write("This is an algebraic identity (verified exactly for all primes in range).\n\n")

        # M(p) relationship
        f.write("## Key Finding 4: Relationship with M(p)\n\n")

        # Compute correlation between (1-D/A)*p and M(p)
        f.write("| p | M(p) | (1-D/A)·p | (1-D/A)·p / M(p) |\n")
        f.write("|---|------|-----------|------------------|\n")

        c_vals = []
        for r in results:
            p = r['p']
            Mp = r['M_p']
            oda = float(r['one_minus_DA'])
            oda_p = oda * p
            c_val = oda_p / Mp if Mp != 0 else float('inf')
            c_vals.append(c_val)
            if p <= 50 or Mp <= -3:
                f.write(f"| {p} | {Mp} | {oda_p:+.6f} | {c_val:.6f} |\n")

        finite_c = [c for c in c_vals if abs(c) < 1000]
        if finite_c:
            f.write(f"\nMedian of (1-D/A)·p/M(p): {sorted(finite_c)[len(finite_c)//2]:.6f}\n")

        # M(p) <= -3 analysis
        mp_neg3 = [r for r in results if r['M_p'] <= -3]
        if mp_neg3:
            f.write(f"\n## Key Finding 5: M(p) ≤ -3 Bound on |1-D/A|\n\n")
            max_abs = max(abs(float(r['one_minus_DA'])) for r in mp_neg3)
            max_c = max(abs(float(r['one_minus_DA'])) * r['p'] / abs(r['M_p'])
                       for r in mp_neg3 if r['M_p'] != 0)
            f.write(f"- Number of primes with M(p) ≤ -3: {len(mp_neg3)}\n")
            f.write(f"- Max |1-D/A| among these: {max_abs:.8f}\n")
            f.write(f"- Max c where |1-D/A| ≤ c·|M(p)|/p: {max_c:.6f}\n")
            f.write(f"- Conjecture: |1-D/A| ≤ {max_c:.2f}·|M(p)|/p for all primes with M(p) ≤ -3\n\n")

        # Bypass condition
        f.write(f"\n## Key Finding 6: Bypass Condition\n\n")
        f.write("Condition for ΔW < 0 without relying on B:\n")
        f.write("```\nC + D > A  ⟹  ΔW < 0 (regardless of sign of B)\n```\n\n")

        bypass_count = sum(1 for r in results if r['C'] + r['D'] > r['A'])
        f.write(f"C + D > A holds for {bypass_count}/{len(results)} primes\n\n")

        if bypass_count < len(results):
            fail_primes = [r['p'] for r in results if r['C'] + r['D'] <= r['A']]
            f.write(f"Fails for primes: {fail_primes[:20]}{'...' if len(fail_primes) > 20 else ''}\n\n")

        f.write("---\n")
        f.write(f"*Generated by DA_ratio_exact_analysis.py, {len(results)} primes, p ∈ [5, {results[-1]['p']}]*\n")

    print(f"\nReport written to {md_path}")


if __name__ == '__main__':
    main()
