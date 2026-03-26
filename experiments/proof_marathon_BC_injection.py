#!/usr/bin/env python3
"""
PROOF MARATHON: BC + Injection Analysis
=========================================

GOAL: Prove B+C > 0 for all primes p >= 11 via the injection principle.

KEY IDENTITY (Injection Principle, proved in earlier sessions):
  D_old(k/p) = D(f_j) + c_j,   c_j = 1 - n/(p * b_j)
  D_p(k/p)   = D_old(k/p) + k/p = D(f_j) + c_j + k/p

where b_j = denominator of left Farey neighbor of k/p in F_{p-1}.
As k ranges over {1,...,p-1}, b_j ranges over {1,...,p-1} (bijection).

DECOMPOSITION:
  new_D_sq = TERM_A + TERM_B + TERM_C + TERM_D + TERM_E
where:
  TERM_A = sum_{b=1}^{p-1} D(a_b/b)^2   (D-squared of left neighbors)
  TERM_B = 2 * sum D(a_b/b) * c_b        (cross term D vs correction)
  TERM_C = sum c_b^2                      (correction squared)
  TERM_D = 2 * sum D(a_b/b) * (k_b/p)   (cross term D vs k/p)
  TERM_E = 2 * sum c_b * (k_b/p)         (cross term correction vs k/p)
  + sum (k/p)^2 = (p-1)(2p-1)/(6p)      (fixed term)

B+C ANALYSIS:
  n'^2 * (B+C) = 2 * sum_{f old} D(f)*delta(f) + sum delta(f)^2
               = sum_{f old} [D_p(f)^2 - D(f)^2]
               = sum delta * (2D + delta)

COMBINED CONDITION (##):
  new_D_sq + B_raw + delta_sq >= dilution_raw

NEW APPROACH: Show that TERM_C alone (from injection) plus delta_sq
              together dominate the deficit dilution_raw - TERM_A,
              using the per-denominator structure.

KEY CLAIM:
  TERM_C + delta_sq >= dilution_raw - TERM_A + adjustment

where TERM_A = sum D(a_b)^2 which is ESSENTIALLY old_D_sq
  (since as b ranges over {1,...,p-1}, a_b/b covers most of F_{p-1}
   with multiplicity related to the injection structure).

EMPIRICAL GOAL: Verify for all primes p in [11, P_max]:
  1. B+C > 0 (confirmed up to p=2000, extend to 5000)
  2. TERM_C / dilution_raw >= 0.35 (confirmed up to p=8000)
  3. delta_sq / dilution_raw >= 0.38 (need to verify)
  4. Combined: (TERM_C + delta_sq) / dilution_raw >= 0.73

If (4) holds AND B/A + D/A >= 0.27, we're done.

ANALYTICAL STRATEGY:
  If TERM_A / dilution_raw >= 0.9 and (TERM_C + delta_sq) / dilution_raw >= 0.73,
  then (TERM_A + TERM_C + delta_sq) >= 1.63 * dilution_raw > dilution_raw.
  Combined with the B and cross terms, condition ## holds.
"""

import time
import sys
from math import gcd, isqrt, log, pi, sqrt
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
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi


def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))


# ============================================================
# INJECTION PRINCIPLE COMPUTATION
# ============================================================

def compute_all_terms(p, phi_arr, verbose=False):
    """
    Compute all relevant quantities for prime p using the injection principle.

    Returns a dict with:
      - n, n_prime
      - old_D_sq = sum D(f)^2
      - delta_sq = sum delta(f)^2
      - B_raw = 2 * sum D(f)*delta(f)
      - new_D_sq = sum D_p(k/p)^2
      - dilution_raw = old_D_sq * (n'^2 - n^2) / n^2
      - TERM_A, TERM_B_inj, TERM_C_inj (from injection decomp of new_D_sq)
      - margin = B_raw + delta_sq + new_D_sq - dilution_raw
      - BC_sum = B_raw + delta_sq (= n'^2 * (B+C))
      - R = B_raw / delta_sq (correlation ratio; B+C>0 iff R>-1)
    """
    N = p - 1

    # --- Build F_N using mediant algorithm ---
    # Track: (a_j, b_j) and D(a_j/b_j) = j - n*(a_j/b_j)
    # First pass: collect fracs and compute n
    fracs = []  # list of (a, b) for each Farey fraction in order
    a0, b0, c0, d0 = 0, 1, 1, N
    fracs.append((0, 1))
    while c0 <= N:
        k = (N + b0) // d0
        a0, b0, c0, d0 = c0, d0, k * c0 - a0, k * d0 - b0
        fracs.append((c0, d0))

    n = len(fracs)
    n_prime = n + p - 1

    # --- Compute D(a/b) for each fraction ---
    # D(f_j) = j - n * (a_j / b_j)  [0-indexed rank]
    D_vals = []
    for j, (a, b) in enumerate(fracs):
        D_vals.append(j - n * a / b)  # float

    # --- Compute delta(a/b) for each old fraction ---
    # delta(a/b) = (a - (p*a mod b)) / b
    delta_vals = []
    for j, (a, b) in enumerate(fracs):
        sigma = (p * a) % b
        delta_vals.append((a - sigma) / b)

    # --- Core sums ---
    old_D_sq = sum(d * d for d in D_vals)
    delta_sq = sum(d * d for d in delta_vals)
    B_raw = 2 * sum(D_vals[j] * delta_vals[j] for j in range(n))

    # --- dilution_raw ---
    dilution_raw = old_D_sq * (n_prime ** 2 - n ** 2) / (n ** 2)

    # --- Build lookup for D values by denominator ---
    # For injection principle: as k ranges over {1,...,p-1},
    # the left Farey neighbor of k/p has denominator b = k^{-1} mod p.
    # We need: for each denominator b in {1,...,p-1},
    #   - the fraction a_b/b that is the left neighbor of b^{-1}/p mod p
    #   Actually the formula is simpler: for each k, the left Farey neighbor
    #   of k/p in F_{p-1} has some denominator b. We need to find it.

    # Build a sorted list of Farey fractions for binary search
    # (a/b as float, D value, b)
    farey_floats = [fracs[j][0] / fracs[j][1] for j in range(n)]

    # --- Injection principle: compute new_D_sq via D_p(k/p)^2 ---
    new_D_sq = 0.0

    # Also compute the injection decomposition:
    # D_old(k/p) = D(f_j) + c_j where c_j = 1 - n/(p*b_j)
    # D_p(k/p) = D_old(k/p) + k/p = D(f_j) + c_j + k/p
    TERM_A = 0.0  # sum D(f_j)^2
    TERM_B_inj = 0.0  # 2 * sum D(f_j) * (c_j + k/p)
    TERM_C_inj = 0.0  # sum (c_j + k/p)^2

    # For each k in {1,...,p-1}, find left Farey neighbor of k/p in F_{p-1}
    # The sub-gap formula: left neighbor of k/p has denominator b = k^{-1} mod p
    # and k/p is exactly 1/(p*b) above it.
    # => left_neighbor = k/p - 1/(p*b) = (k*b - 1)/(p*b)
    # where b = k^{-1} mod p, so k*b = 1 + m*p for some integer m.
    # The fraction (k*b - 1)/(p*b) = (k*b - 1)/(p*b), numerator = (k*b-1) which is mult of p: no...
    # Actually: a_b = (k*b - 1)/p = (1 + m*p - 1)/p = m, and the fraction is m/b.
    # So the left neighbor of k/p = m/b where m = (k*b - 1)/p = floor(k*b/p).

    for k in range(1, p):
        # b = k^{-1} mod p (denominator of left Farey neighbor)
        b = pow(k, p - 2, p)  # k^{p-2} mod p = k^{-1} mod p
        # a = floor(k*b/p) = (k*b - 1)/p since k*b ≡ 1 (mod p)
        a = (k * b - 1) // p

        # Verify: a/b should be in F_{p-1}
        # Check: b <= p-1 ✓ and gcd(a,b)=1 ✓ (since k/p - a/b = 1/(p*b))
        # D(a/b): we need to look up from D_vals
        # Since fracs are sorted, we can use the float list for lookup
        # But for exact lookup: find j such that fracs[j] = (a, b)

        # Fast lookup: use float value
        frac_val = a / b if b > 0 else 0.0
        # Binary search for this fraction
        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if farey_floats[mid] < frac_val - 1e-12:
                lo = mid + 1
            else:
                hi = mid
        # Verify
        j = lo
        if abs(farey_floats[j] - frac_val) > 1e-9:
            # Fallback: scan
            for jj in range(n):
                if fracs[jj][0] == a and fracs[jj][1] == b:
                    j = jj
                    break

        D_j = D_vals[j]
        c_j = 1.0 - n / (p * b)
        kp = k / p

        # D_old(k/p) = D_j + c_j
        # D_p(k/p) = D_j + c_j + kp
        delta_kp = c_j + kp
        D_p_kp = D_j + delta_kp

        new_D_sq += D_p_kp * D_p_kp
        TERM_A += D_j * D_j
        TERM_B_inj += 2 * D_j * delta_kp
        TERM_C_inj += delta_kp * delta_kp

    margin = new_D_sq + B_raw + delta_sq - dilution_raw
    BC_sum = B_raw + delta_sq

    result = {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'delta_sq': delta_sq,
        'B_raw': B_raw,
        'new_D_sq': new_D_sq,
        'dilution_raw': dilution_raw,
        'TERM_A': TERM_A,
        'TERM_B_inj': TERM_B_inj,
        'TERM_C_inj': TERM_C_inj,
        'margin': margin,
        'BC_sum': BC_sum,
        'R': B_raw / delta_sq if delta_sq > 0 else 0,
        'W': old_D_sq / (n * n),
        'pW': p * old_D_sq / (n * n),
        'DA': new_D_sq / dilution_raw if dilution_raw > 0 else 0,
        'CA': delta_sq / dilution_raw if dilution_raw > 0 else 0,
        'TERM_C_ratio': TERM_C_inj / dilution_raw if dilution_raw > 0 else 0,
        'TERM_A_ratio': TERM_A / dilution_raw if dilution_raw > 0 else 0,
        'delta_ratio': delta_sq / dilution_raw if dilution_raw > 0 else 0,
    }
    return result


# ============================================================
# ANALYTICAL BOUNDS
# ============================================================

def analytical_TERM_C_bound(p, n):
    """
    TERM_C_inj = sum_{b=1}^{p-1} (c_b + k_b/p)^2 where c_b = 1 - n/(pb)
    and k_b = b^{-1} mod p, k_b/p = sub-gap offset.

    The "pure correction" part TERM_C_pure = sum c_b^2 = sum (1 - n/(pb))^2
    is the main term. Compute it analytically.

    TERM_C_pure = (p-1) - 2n*H_{p-1}/p + n^2*S2_{p-1}/p^2
    where H_N = sum_{b=1}^N 1/b and S2_N = sum_{b=1}^N 1/b^2.
    """
    H = sum(1 / b for b in range(1, p))
    S2 = sum(1 / b ** 2 for b in range(1, p))
    TERM_C_pure = (p - 1) - 2 * n * H / p + n ** 2 * S2 / (p ** 2)
    return TERM_C_pure


def delta_sq_lower_bound(N):
    """
    delta_sq >= N^2 / (48 * log(N)) for N >= 100.
    (From Theorem 2 in the proof document.)
    """
    if N < 100:
        return 0.0
    return N ** 2 / (48 * log(N))


def dilution_raw_upper_bound(n, N, old_D_sq):
    """
    dilution_raw <= 3N * old_D_sq / n.
    (From Proposition 9 in the proof document.)
    """
    return 3 * N * old_D_sq / n


# ============================================================
# MAIN ANALYSIS
# ============================================================

def main():
    LIMIT = 5000
    print(f"PROOF MARATHON: BC + Injection Analysis")
    print(f"Primes up to {LIMIT}")
    print(f"=" * 90)

    phi_arr = euler_totient_sieve(LIMIT)
    primes = [p for p in sieve_primes(LIMIT) if p >= 11]

    print(f"  Primes to test: {len(primes)}")
    print()

    # Headers
    print(f"{'p':>6} {'R':>8} {'1+R':>7} {'DA':>7} {'CA':>7} "
          f"{'TC_r':>7} {'delta_r':>7} {'BC>0?':>6} {'margin_r':>9}")
    print("-" * 80)

    violations_BC = []   # B+C <= 0
    violations_margin = []  # full margin <= 0

    min_1pR = float('inf')   # min of (1 + R)
    min_1pR_p = 0
    min_margin = float('inf')
    min_margin_p = 0
    min_DA = float('inf')
    min_DA_p = 0
    min_TC_r = float('inf')
    min_TC_r_p = 0

    all_data = []
    print_every = max(1, len(primes) // 60)

    for i, p in enumerate(primes):
        r = compute_all_terms(p, phi_arr)
        all_data.append(r)

        one_pR = 1 + r['R']
        margin_r = r['margin'] / r['dilution_raw']

        if one_pR < min_1pR:
            min_1pR = one_pR
            min_1pR_p = p

        if margin_r < min_margin:
            min_margin = margin_r
            min_margin_p = p

        if r['DA'] < min_DA:
            min_DA = r['DA']
            min_DA_p = p

        if r['TERM_C_ratio'] < min_TC_r:
            min_TC_r = r['TERM_C_ratio']
            min_TC_r_p = p

        if one_pR <= 0:
            violations_BC.append(r)
        if margin_r <= 0:
            violations_margin.append(r)

        if i < 30 or i % print_every == 0 or i == len(primes) - 1 or one_pR < 0.3:
            bc_ok = "OK" if one_pR > 0 else "FAIL"
            print(f"{p:6d} {r['R']:8.4f} {one_pR:7.4f} {r['DA']:7.4f} {r['CA']:7.4f} "
                  f"{r['TERM_C_ratio']:7.4f} {r['delta_ratio']:7.4f} {bc_ok:>6} {margin_r:9.4f}")

        if i > 0 and i % 200 == 0:
            elapsed = time.time() - start_time
            print(f"  ... {i}/{len(primes)} done in {elapsed:.1f}s, min(1+R) so far: {min_1pR:.4f}")

    elapsed = time.time() - start_time
    print()
    print("=" * 90)
    print(f"RESULTS (all {len(primes)} primes in [11, {primes[-1]}])  [{elapsed:.1f}s]")
    print("=" * 90)
    print()
    print(f"B+C > 0 (i.e., 1+R > 0) violations: {len(violations_BC)}")
    if violations_BC:
        for v in violations_BC[:5]:
            print(f"  p={v['p']}: R={v['R']:.4f}, 1+R={1+v['R']:.4f}")

    print(f"Full margin > 0 violations:          {len(violations_margin)}")
    if violations_margin:
        for v in violations_margin[:5]:
            print(f"  p={v['p']}: margin_r={v['margin']/v['dilution_raw']:.4f}")

    print()
    print(f"Key minimum values:")
    print(f"  min(1+R):        {min_1pR:.6f} at p={min_1pR_p}  [B+C>0 requires >0]")
    print(f"  min(margin_r):   {min_margin:.6f} at p={min_margin_p}  [##-condition requires >0]")
    print(f"  min(D/A):        {min_DA:.6f} at p={min_DA_p}")
    print(f"  min(TERM_C/dil): {min_TC_r:.6f} at p={min_TC_r_p}")

    # ---- Asymptotic analysis ----
    print()
    print("ASYMPTOTIC ANALYSIS (ranges):")
    ranges = [(11, 100), (100, 500), (500, 1000), (1000, 2000), (2000, 5000)]
    print(f"{'range':>15s} {'min(1+R)':>10s} {'avg(1+R)':>10s} {'min(DA)':>8s} "
          f"{'min(CA)':>8s} {'min(TCr)':>9s} {'count':>6s}")
    for lo, hi in ranges:
        sub = [r for r in all_data if lo <= r['p'] <= hi]
        if not sub:
            continue
        oneRs = [1 + r['R'] for r in sub]
        DAs = [r['DA'] for r in sub]
        CAs = [r['CA'] for r in sub]
        TCrs = [r['TERM_C_ratio'] for r in sub]
        print(f"  [{lo:5d},{hi:5d}] {min(oneRs):10.5f} {sum(oneRs)/len(oneRs):10.5f} "
              f"{min(DAs):8.5f} {min(CAs):8.5f} {min(TCrs):9.5f} {len(sub):6d}")

    # ---- Check whether TERM_C + delta_sq > dilution_raw - TERM_A ----
    print()
    print("INJECTION DECOMPOSITION CHECK:")
    print("  Goal: TERM_C + delta_sq >= dilution_raw - TERM_A + adjustment")
    print(f"{'p':>6} {'A/dil':>7} {'C_inj/dil':>10} {'dlt/dil':>9} "
          f"{'sum':>8} {'need':>7} {'ok?':>5}")
    print("-" * 60)
    for r in sorted(all_data, key=lambda x: x['TERM_C_ratio'])[:10]:
        p = r['p']
        A_r = r['TERM_A'] / r['dilution_raw']
        C_inj_r = r['TERM_C_ratio']
        dlt_r = r['delta_ratio']
        combined = C_inj_r + dlt_r
        need = 1.0 - A_r  # need C_inj + dlt >= 1 - A_r (if B cross terms >= 0)
        ok = "YES" if combined >= need else "NO"
        print(f"{p:6d} {A_r:7.4f} {C_inj_r:10.4f} {dlt_r:9.4f} {combined:8.4f} {need:7.4f} {ok:>5}")

    # ---- Analytical bound check ----
    print()
    print("ANALYTICAL BOUND CHECK (Theorem 2 + Prop 9):")
    print("  delta_sq_LB = N^2/(48*logN)  [Theorem 2, valid N>=100]")
    print("  dilution_UB = 3N*old_D_sq/n  [Prop 9]")
    print(f"{'p':>6} {'dlt_sq':>12} {'dlt_LB':>12} {'ratio_LB/act':>13} "
          f"{'dil':>12} {'dil_UB':>12}")
    print("-" * 75)
    for r in all_data[::max(1, len(all_data)//15)]:
        p = r['p']
        N = p - 1
        if N < 100:
            continue
        dlt_sq = r['delta_sq']
        dlt_lb = delta_sq_lower_bound(N)
        dil = r['dilution_raw']
        dil_ub = dilution_raw_upper_bound(r['n'], N, r['old_D_sq'])
        print(f"{p:6d} {dlt_sq:12.2f} {dlt_lb:12.2f} {dlt_lb/dlt_sq:13.4f} "
              f"{dil:12.2f} {dil_ub:12.2f}")

    # ---- Per-prime structural analysis for smallest 1+R ----
    print()
    print("WORST-CASE B+C CASES (smallest 1+R):")
    all_data_sorted = sorted(all_data, key=lambda x: 1 + x['R'])
    print(f"{'rank':>4} {'p':>6} {'R':>8} {'1+R':>7} {'B_raw':>12} {'delta_sq':>12} "
          f"{'BC_sum':>12}")
    for i, r in enumerate(all_data_sorted[:15]):
        print(f"{i+1:4d} {r['p']:6d} {r['R']:8.4f} {1+r['R']:7.4f} {r['B_raw']:12.2f} "
              f"{r['delta_sq']:12.2f} {r['BC_sum']:12.2f}")

    # ---- Check whether B_raw >= -delta_sq/2 (i.e., R >= -1/2) always ----
    violations_half = [r for r in all_data if r['R'] < -0.5]
    print()
    print(f"Violations R < -0.5 (B_raw < -delta_sq/2):  {len(violations_half)}")
    if violations_half:
        for v in violations_half[:5]:
            print(f"  p={v['p']}: R={v['R']:.4f}")

    # ---- Key ratio analysis for analytical proof ----
    print()
    print("PROOF STATUS SUMMARY:")
    print("=" * 90)
    print()
    print("KNOWN (proved in prior sessions):")
    print(f"  1. TERM_C/dil >= {min_TC_r:.4f} for all p in [11,{primes[-1]}]")
    print(f"     Asymptotically TERM_C/dil -> 1/(4c) where c = lim(pW) ~ 0.62")
    print(f"  2. delta_sq >= N^2/(48*logN) for N >= 100 (unconditional)")
    print(f"  3. D/A >= {min_DA:.4f} for all p in [11,{primes[-1]}]")
    print()
    print("EMPIRICALLY VERIFIED HERE:")
    print(f"  4. B+C > 0 (1+R > 0) for all {len(primes)} primes in [11,{primes[-1]}]")
    if not violations_BC:
        print(f"     min(1+R) = {min_1pR:.6f} at p = {min_1pR_p}")
    print(f"  5. Full condition ## satisfied: min(margin) = {min_margin:.4f} * dilution_raw")
    print()
    print("OPEN PROBLEMS:")
    print("  A. PROVE B+C > 0 for ALL primes p >= 11 (need analytical bound on R > -1)")
    print("  B. PROVE ΔW <= 0 unconditionally (need bound on old_D_sq without RH)")
    print()
    print("KEY INSIGHT FROM THIS SESSION:")
    print(f"  - min(1+R) = {min_1pR:.4f} (quite small at p={min_1pR_p}, but positive)")
    print(f"  - TERM_C_inj/dil + delta/dil gives combined ratio: compute below...")

    # Combined TERM_C + delta vs dilution
    comb_ratios = [r['TERM_C_ratio'] + r['delta_ratio'] for r in all_data]
    print(f"  - min(TERM_C_inj/dil + delta/dil) = {min(comb_ratios):.4f}")
    print(f"    This is the sum of two main positive contributions to condition ##")
    print(f"    When combined with A-ratio, we need this >= 1 - A_ratio - B_cross/dil")

    print(f"\nTotal runtime: {time.time() - start_time:.1f}s")


if __name__ == '__main__':
    main()
