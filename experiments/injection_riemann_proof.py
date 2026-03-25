#!/usr/bin/env python3
"""
INJECTION PRINCIPLE + SUB-GAP FORMULA => D/A >= 0.9
=====================================================

KEY IDENTITY (exact, from the Injection Principle):
  When k/p falls in the Farey gap (f_j, f_{j+1}), the left neighbor f_j
  has denominator b_j. The sub-gap formula gives:

    k/p - f_j = 1/(p * b_j)

  where b_j is the denominator of the left Farey neighbor.

  The Farey discrepancy D_old(x) = (j+1) - n*x for x in (f_j, f_{j+1}),
  so at the inserted point:

    D_old(k/p) = D_old(f_j) + 1 - n/(p * b_j)

  This is EXACT for every k in {1, ..., p-1}.

DECOMPOSITION OF S_virt:
  S_virt = sum_{k=1}^{p-1} D_old(k/p)^2

  Let c_j = 1 - n/(p * b_j)  (the "correction" for gap j).
  Then D_old(k/p) = D(f_j) + c_j, so:

  S_virt = sum [D(f_j)^2 + 2*D(f_j)*c_j + c_j^2]
         = sum D(f_j)^2  +  2*sum D(f_j)*c_j  +  sum c_j^2
         =    TERM_A      +      TERM_B         +   TERM_C

  Since k -> k^{-1} mod p is a permutation of {1,...,p-1}, and
  b_j = (left-neighbor denominator), the correction c_j depends on
  the specific gap structure.

  TERM_C = sum_{k=1}^{p-1} [1 - n/(p*b_j)]^2
  TERM_B = 2 * sum_{k=1}^{p-1} D(f_j) * [1 - n/(p*b_j)]

  The goal: show S_virt / dilution_raw >= 0.9.

THIS SCRIPT:
  1. Verifies the sub-gap identity for small primes (exact arithmetic)
  2. Decomposes S_virt = TERM_A + TERM_B + TERM_C for each prime
  3. Analyzes each term's contribution to D/A
  4. Tests whether TERM_A / old_D_sq is bounded below
  5. Looks for patterns in TERM_B and TERM_C
  6. Checks D/A >= 0.9 for all primes up to 5000
"""

import sys
import time
from math import gcd, isqrt, pi, log
from fractions import Fraction

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

def farey_generator(N):
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))


# ============================================================
# PART 1: Verify the sub-gap identity (exact arithmetic)
# ============================================================

def verify_subgap_identity(p, phi_arr):
    """
    For each k in {1,...,p-1}, verify that:
      k/p - f_j = 1/(p * b_j)
    where f_j = a_j/b_j is the left Farey neighbor of k/p in F_{p-1}.

    Also verify:
      D_old(k/p) = D(f_j) + 1 - n/(p * b_j)
    """
    N = p - 1
    n = farey_size(N, phi_arr)

    # Build Farey sequence as exact fractions
    farey_pairs = list(farey_generator(N))
    farey_fracs = [Fraction(a, b) for a, b in farey_pairs]
    farey_denoms = [b for _, b in farey_pairs]

    # Precompute D(f_j) for each Farey fraction
    D_farey = []
    for idx, fv in enumerate(farey_fracs):
        D_farey.append(idx - n * fv)

    errors_subgap = 0
    errors_discrepancy = 0

    for k in range(1, p):
        target = Fraction(k, p)

        # Find left neighbor: largest f_j < k/p via binary search
        lo, hi = 0, len(farey_fracs) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if farey_fracs[mid] < target:
                lo = mid
            else:
                hi = mid - 1
        j = lo  # index of left neighbor

        f_j = farey_fracs[j]
        b_j = farey_denoms[j]

        # Check sub-gap formula: k/p - f_j = 1/(p * b_j)
        # Use cross-multiplication to avoid Fraction division:
        # k/p - a/b = (kb - pa) / (pb)
        # Expected: 1/(pb). So check kb - pa == 1.
        a_j = farey_fracs[j].numerator
        kb_minus_pa = k * b_j - p * a_j
        if kb_minus_pa != 1:
            errors_subgap += 1
            if errors_subgap <= 3:
                print(f"  SUB-GAP FAIL: p={p}, k={k}, kb-pa={kb_minus_pa} (expected 1)")

        # Check discrepancy identity:
        # k/p is NOT in F_{p-1}, so count of fracs <= k/p = j+1
        D_old_kp = Fraction(j + 1) - n * target
        D_fj = D_farey[j]
        correction = Fraction(1) - Fraction(n, p * b_j)

        expected_D = D_fj + correction
        if D_old_kp != expected_D:
            errors_discrepancy += 1
            if errors_discrepancy <= 3:
                print(f"  DISCREPANCY FAIL: p={p}, k={k}, D_old={D_old_kp}, "
                      f"expected={expected_D}, D_fj={D_fj}, corr={correction}")

    return errors_subgap, errors_discrepancy


# ============================================================
# PART 2: Decompose S_virt = TERM_A + TERM_B + TERM_C
# ============================================================

def injection_decomposition(p, phi_arr, use_exact=False):
    """
    Decompose S_virt using the injection principle:
      D_old(k/p) = D(f_j) + c_j   where c_j = 1 - n/(p*b_j)

    S_virt = TERM_A + TERM_B + TERM_C
    where:
      TERM_A = sum D(f_j)^2    (discrepancy at filled Farey points)
      TERM_B = 2 * sum D(f_j) * c_j  (cross term)
      TERM_C = sum c_j^2       (correction term)

    Also compute:
      new_D_sq = S_virt + 2*X_cross + S_kp
      dilution_raw = old_D_sq * (n'^2 - n^2) / n^2
      D/A = new_D_sq / dilution_raw
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    # Build Farey sequence
    farey_pairs = list(farey_generator(N))

    if use_exact:
        farey_fracs = [Fraction(a, b) for a, b in farey_pairs]
        farey_denoms = [b for _, b in farey_pairs]
        zero = Fraction(0)
    else:
        farey_fracs = [a / b for a, b in farey_pairs]
        farey_denoms = [b for _, b in farey_pairs]
        zero = 0.0

    num_farey = len(farey_fracs)

    # Precompute D(f_j) for each Farey fraction
    D_farey = []
    for idx in range(num_farey):
        fv = farey_fracs[idx]
        if use_exact:
            D_farey.append(Fraction(idx) - n * fv)
        else:
            D_farey.append(idx - n * fv)

    # old_D_sq = sum of D(f)^2 over all Farey fractions
    old_D_sq = sum(d * d for d in D_farey)

    # Now process each k in {1,...,p-1}
    TERM_A = zero  # sum D(f_j)^2
    TERM_B = zero  # 2 * sum D(f_j) * c_j
    TERM_C = zero  # sum c_j^2
    X_cross = zero  # sum D_old(k/p) * (k/p)
    S_kp = zero     # sum (k/p)^2
    S_virt = zero   # sum D_old(k/p)^2
    sum_cj = zero   # sum c_j
    sum_Dfj = zero  # sum D(f_j) at filled gaps

    # Track which Farey gaps are filled
    filled_gaps = set()

    # Collect b_j values for analysis
    b_values = []
    c_values = []

    for k in range(1, p):
        if use_exact:
            target = Fraction(k, p)
        else:
            target = k / p

        # Binary search for left neighbor
        lo, hi = 0, num_farey - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if farey_fracs[mid] < target:
                lo = mid
            else:
                hi = mid - 1
        j = lo

        filled_gaps.add(j)
        b_j = farey_denoms[j]
        b_values.append(b_j)

        if use_exact:
            c_j = Fraction(1) - Fraction(n, p * b_j)
        else:
            c_j = 1.0 - n / (p * b_j)
        c_values.append(c_j)

        D_fj = D_farey[j]

        # Accumulate decomposition terms
        TERM_A += D_fj * D_fj
        TERM_B += D_fj * c_j  # will multiply by 2 at end
        TERM_C += c_j * c_j
        sum_cj += c_j
        sum_Dfj += D_fj

        # D_old(k/p) = D(f_j) + c_j
        D_old_kp = D_fj + c_j

        S_virt += D_old_kp * D_old_kp
        X_cross += D_old_kp * target
        S_kp += target * target

    TERM_B *= 2  # factor of 2

    # Verify decomposition: S_virt = TERM_A + TERM_B + TERM_C
    S_virt_check = TERM_A + TERM_B + TERM_C

    new_D_sq = S_virt + 2 * X_cross + S_kp

    if use_exact:
        T_factor = Fraction(n_prime**2 - n**2, n**2)
    else:
        T_factor = (n_prime**2 - n**2) / n**2

    dilution_raw = old_D_sq * T_factor
    DA_ratio = new_D_sq / dilution_raw if dilution_raw != 0 else None

    # Sub-ratios
    R = S_virt / old_D_sq if old_D_sq != 0 else None
    R_over_T = R / T_factor if R is not None else None

    # Fraction of old_D_sq at filled gaps
    filled_D_sq = sum(D_farey[j] ** 2 for j in filled_gaps)
    fill_fraction = filled_D_sq / old_D_sq if old_D_sq != 0 else None

    # Harmonic sums over b_j values
    sum_inv_b = sum(1.0 / b for b in b_values)
    sum_inv_b_sq = sum(1.0 / (b * b) for b in b_values)

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'S_virt': S_virt,
        'S_virt_check': S_virt_check,
        'TERM_A': TERM_A,
        'TERM_B': TERM_B,
        'TERM_C': TERM_C,
        'X_cross': X_cross,
        'S_kp': S_kp,
        'new_D_sq': new_D_sq,
        'T_factor': T_factor,
        'dilution_raw': dilution_raw,
        'DA_ratio': DA_ratio,
        'R': R,
        'R_over_T': R_over_T,
        'filled_gaps': len(filled_gaps),
        'total_gaps': num_farey - 1,
        'fill_fraction_D_sq': fill_fraction,
        'sum_cj': sum_cj,
        'sum_Dfj': sum_Dfj,
        'sum_inv_b': sum_inv_b,
        'sum_inv_b_sq': sum_inv_b_sq,
        'b_values': b_values,
        'c_values': c_values,
    }


# ============================================================
# MAIN
# ============================================================

def main():
    LIMIT = 3000
    phi_arr = euler_totient_sieve(LIMIT)
    primes = sieve_primes(LIMIT)
    flush = lambda: sys.stdout.flush()

    # ----------------------------------------------------------
    # PART 1: Verify sub-gap identity for small primes
    # ----------------------------------------------------------
    print("=" * 70)
    print("PART 1: Verifying sub-gap identity (exact arithmetic)")
    print("  k/p - f_j = 1/(p * b_j)  and  D_old(k/p) = D(f_j) + 1 - n/(p*b_j)")
    print("=" * 70)

    small_primes = [p for p in primes if p <= 97]
    for p in small_primes:
        e_sub, e_disc = verify_subgap_identity(p, phi_arr)
        status = "OK" if e_sub == 0 and e_disc == 0 else "FAIL"
        print(f"  p={p:3d}: sub-gap errors={e_sub}, discrepancy errors={e_disc}  [{status}]")
    sys.stdout.flush()

    # ----------------------------------------------------------
    # PART 2: Exact decomposition for small primes
    # ----------------------------------------------------------
    print("\n" + "=" * 70)
    print("PART 2: Exact injection decomposition (small primes)")
    print("  S_virt = TERM_A + TERM_B + TERM_C")
    print("=" * 70)

    for p in [5, 7, 11, 13, 23, 29, 37, 41, 53]:
        r = injection_decomposition(p, phi_arr, use_exact=True)
        # Verify decomposition identity
        decomp_ok = abs(r['S_virt'] - r['S_virt_check']) == 0
        print(f"\n  p={p}: n={r['n']}, n'={r['n_prime']}")
        print(f"    old_D_sq = {float(r['old_D_sq']):.6f}")
        print(f"    S_virt   = {float(r['S_virt']):.6f}  (check: {'OK' if decomp_ok else 'FAIL'})")
        print(f"    TERM_A   = {float(r['TERM_A']):.6f}  (D(f_j)^2 at filled gaps)")
        print(f"    TERM_B   = {float(r['TERM_B']):.6f}  (cross: 2*D(f_j)*c_j)")
        print(f"    TERM_C   = {float(r['TERM_C']):.6f}  (c_j^2)")
        print(f"    X_cross  = {float(r['X_cross']):.6f}")
        print(f"    S_kp     = {float(r['S_kp']):.6f}")
        print(f"    new_D_sq = {float(r['new_D_sq']):.6f}")
        print(f"    dilut_raw= {float(r['dilution_raw']):.6f}")
        print(f"    D/A      = {float(r['DA_ratio']):.8f}")
        print(f"    filled_gaps = {r['filled_gaps']} / {r['total_gaps']}")
        print(f"    fill_frac(D^2) = {float(r['fill_fraction_D_sq']):.6f}")
    sys.stdout.flush()

    # ----------------------------------------------------------
    # PART 3: Float computation for all primes up to LIMIT
    # ----------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"PART 3: Injection decomposition for all primes up to {LIMIT}")
    print("=" * 70)

    min_DA = 999.0
    min_DA_p = 0
    min_fill_frac = 999.0

    # Track sub-ratio statistics
    stats = []

    t0 = time.time()
    for p in primes:
        if p < 5:
            continue
        r = injection_decomposition(p, phi_arr, use_exact=False)

        da = r['DA_ratio']
        fill = r['fill_fraction_D_sq']

        if da < min_DA:
            min_DA = da
            min_DA_p = p
        if fill < min_fill_frac:
            min_fill_frac = fill

        # Normalized sub-terms
        dilut = r['dilution_raw']
        termA_norm = r['TERM_A'] / dilut if dilut != 0 else 0
        termB_norm = r['TERM_B'] / dilut if dilut != 0 else 0
        termC_norm = r['TERM_C'] / dilut if dilut != 0 else 0
        xcross_norm = 2 * r['X_cross'] / dilut if dilut != 0 else 0
        skp_norm = r['S_kp'] / dilut if dilut != 0 else 0

        stats.append({
            'p': p, 'DA': da, 'fill': fill,
            'termA_norm': termA_norm, 'termB_norm': termB_norm,
            'termC_norm': termC_norm, 'xcross_norm': xcross_norm,
            'skp_norm': skp_norm, 'R_over_T': r['R_over_T'],
            'sum_cj': r['sum_cj'], 'sum_Dfj': r['sum_Dfj'],
        })

    elapsed = time.time() - t0
    print(f"  Computed {len(stats)} primes in {elapsed:.1f}s")
    print(f"\n  MINIMUM D/A = {min_DA:.8f}  at p={min_DA_p}")
    print(f"  D/A >= 0.9?  {'YES' if min_DA >= 0.9 else 'NO (min=' + str(min_DA) + ')'}")
    print(f"  Min fill_fraction(D^2) = {min_fill_frac:.6f}")

    # ----------------------------------------------------------
    # PART 4: Detailed sub-term analysis
    # ----------------------------------------------------------
    print("\n" + "=" * 70)
    print("PART 4: Sub-term analysis (normalized by dilution_raw)")
    print("  D/A = termA_norm + termB_norm + termC_norm + xcross_norm + skp_norm")
    print("=" * 70)

    # Print header
    print(f"  {'p':>6s} {'D/A':>10s} {'TERM_A':>10s} {'TERM_B':>10s} "
          f"{'TERM_C':>10s} {'2*Xcross':>10s} {'S_kp':>10s} {'fill%':>8s} {'R/T':>10s}")
    print("  " + "-" * 96)

    for s in stats:
        if s['p'] <= 200 or s['p'] in [251, 499, 997, 1999, 2999, 4999]:
            print(f"  {s['p']:6d} {s['DA']:10.6f} {s['termA_norm']:10.6f} {s['termB_norm']:10.6f} "
                  f"{s['termC_norm']:10.6f} {s['xcross_norm']:10.6f} {s['skp_norm']:10.6f} "
                  f"{s['fill']*100:7.2f}% {s['R_over_T']:10.6f}")

    # ----------------------------------------------------------
    # PART 5: Asymptotic analysis of each term
    # ----------------------------------------------------------
    print("\n" + "=" * 70)
    print("PART 5: Asymptotic scaling of each term")
    print("=" * 70)

    # For large primes, check how each term scales with p
    large = [s for s in stats if s['p'] >= 100]
    if len(large) >= 2:
        # Fit: termA_norm ~ a0 + a1/p
        print("\n  Term scaling for large primes (p >= 100):")
        for label, key in [('TERM_A_norm', 'termA_norm'), ('TERM_B_norm', 'termB_norm'),
                           ('TERM_C_norm', 'termC_norm'), ('2*Xcross_norm', 'xcross_norm'),
                           ('S_kp_norm', 'skp_norm'), ('R/T', 'R_over_T')]:
            vals = [s[key] for s in large]
            ps = [s['p'] for s in large]
            # Simple estimate: extrapolate from last values
            v_last = vals[-1]
            v_100 = vals[0]
            print(f"    {label:16s}: at p=100 -> {v_100:.6f},  at p={ps[-1]} -> {v_last:.6f}")

        # Check: does termA_norm approach a limit?
        print(f"\n  Does TERM_A/dilut converge?")
        for s in large[-5:]:
            print(f"    p={s['p']:5d}: TERM_A/dilut = {s['termA_norm']:.8f}")

    # ----------------------------------------------------------
    # PART 6: Can we bound S_virt/dilution_raw >= 0.9?
    # ----------------------------------------------------------
    print("\n" + "=" * 70)
    print("PART 6: Bounding S_virt / dilution_raw")
    print("=" * 70)

    min_svirt_ratio = 999.0
    for s in stats:
        r_over_t = s['R_over_T']
        if r_over_t < min_svirt_ratio:
            min_svirt_ratio = r_over_t

    print(f"  min(R/T) = min(S_virt/dilution_raw) = {min_svirt_ratio:.8f}")
    print(f"  R/T >= 0.9?  {'YES' if min_svirt_ratio >= 0.9 else 'NO'}")

    # The full D/A also includes 2*X_cross + S_kp contributions
    # Check: are these always positive?
    min_extra = 999.0
    for s in stats:
        extra = s['xcross_norm'] + s['skp_norm']
        if extra < min_extra:
            min_extra = extra
    print(f"  min(2*Xcross/dilut + S_kp/dilut) = {min_extra:.8f}")
    print(f"  Extra contribution always positive? {'YES' if min_extra > 0 else 'NO'}")

    # ----------------------------------------------------------
    # PART 7: Harmonic sum analysis (b_j = left neighbor denoms)
    # ----------------------------------------------------------
    print("\n" + "=" * 70)
    print("PART 7: Harmonic sum analysis of correction terms")
    print("  c_j = 1 - n/(p*b_j), b_j = left-neighbor denominator")
    print("=" * 70)

    for p in [11, 23, 53, 97, 199, 499, 997]:
        if p > LIMIT:
            continue
        r = injection_decomposition(p, phi_arr, use_exact=False)
        n = r['n']
        sum_c = r['sum_cj']
        # Expected: sum c_j = (p-1) - n/p * sum(1/b_j)
        # If b_j runs over {1,...,p-1} as a permutation: sum(1/b) = H(p-1)
        H_pm1 = sum(1.0 / k for k in range(1, p))
        expected_sum_c = (p - 1) - n * H_pm1 / p

        # Also: TERM_C = sum c_j^2 = (p-1) - 2n/p * sum(1/b) + n^2/p^2 * sum(1/b^2)
        sum_inv_b2 = sum(1.0 / (k * k) for k in range(1, p))
        expected_TERM_C = (p - 1) - 2 * n * H_pm1 / p + n**2 * sum_inv_b2 / p**2

        print(f"\n  p={p}: n={n}")
        print(f"    sum(c_j)     = {sum_c:.6f}")
        print(f"    expected     = {expected_sum_c:.6f}  "
              f"(diff = {abs(sum_c - expected_sum_c):.2e})")
        print(f"    TERM_C       = {float(r['TERM_C']):.6f}")
        print(f"    expected     = {expected_TERM_C:.6f}  "
              f"(diff = {abs(float(r['TERM_C']) - expected_TERM_C):.2e})")
        print(f"    sum(1/b_j)   = {r['sum_inv_b']:.6f}  vs H(p-1) = {H_pm1:.6f}  "
              f"(diff = {abs(r['sum_inv_b'] - H_pm1):.2e})")
        print(f"    sum(1/b_j^2) = {r['sum_inv_b_sq']:.6f}  vs sum(1/k^2) = {sum_inv_b2:.6f}  "
              f"(diff = {abs(r['sum_inv_b_sq'] - sum_inv_b2):.2e})")

    # ----------------------------------------------------------
    # PART 8: Check if b_j is a permutation of {1,...,p-1}
    # ----------------------------------------------------------
    print("\n" + "=" * 70)
    print("PART 8: Is the map k -> b_j (left-neighbor denom) a permutation?")
    print("=" * 70)

    for p in [11, 13, 23, 29, 37, 53, 97]:
        r = injection_decomposition(p, phi_arr, use_exact=False)
        b_sorted = sorted(r['b_values'])
        expected = list(range(1, p))
        is_perm = (b_sorted == expected)
        unique_b = len(set(r['b_values']))
        print(f"  p={p:3d}: unique_b = {unique_b}, p-1 = {p-1}, "
              f"is_perm of {{1..p-1}}? {is_perm}")
        if not is_perm and p <= 29:
            print(f"         b_values = {r['b_values']}")
            print(f"         sorted   = {b_sorted}")
            missing = set(range(1, p)) - set(r['b_values'])
            extra = set(r['b_values']) - set(range(1, p))
            if missing:
                print(f"         missing from {{1..p-1}}: {sorted(missing)}")
            if extra:
                print(f"         extra (not in {{1..p-1}}): {sorted(extra)}")

    # ----------------------------------------------------------
    # PART 9: Summary and conclusion
    # ----------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Primes tested: {len(stats)} (up to p={primes[-1]})")
    print(f"  Minimum D/A: {min_DA:.8f} at p={min_DA_p}")
    print(f"  D/A >= 0.9 for all primes? {'YES' if min_DA >= 0.9 else 'NO'}")
    print(f"  Minimum fill_fraction(D^2): {min_fill_frac:.6f}")
    print(f"  Minimum R/T (S_virt/dilut): {min_svirt_ratio:.8f}")
    print(f"  Minimum extra (Xcross+Skp)/dilut: {min_extra:.8f}")

    if min_DA >= 0.9:
        print(f"\n  CONCLUSION: D/A >= {min_DA:.4f} > 0.9 VERIFIED for all primes up to {LIMIT}.")
        print(f"  The injection principle + sub-gap formula approach is validated.")
    else:
        # Find violators
        violators = [s for s in stats if s['DA'] < 0.9]
        print(f"\n  VIOLATORS (D/A < 0.9): {len(violators)} primes")
        for v in violators[:10]:
            print(f"    p={v['p']}: D/A = {v['DA']:.8f}")


if __name__ == "__main__":
    main()
