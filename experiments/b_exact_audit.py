#!/usr/bin/env python3
"""
B_EXACT_AUDIT: Exact computation of B', C' and Möbius decomposition
using Python's fractions.Fraction for ALL arithmetic. Zero floating point.

Definitions (from paper main.tex):
  F_N = Farey sequence of order N = p-1
  n = |F_N|
  n' = |F_p| = n + (p-1)
  D(f_j) = j - n * f_j, where j is 0-indexed rank in F_N
  delta(f) = f - {p*f} for f = a/b means delta = (a - (p*a mod b)) / b
  B' = 2 * sum_{f in F_N, b>1} D(f) * delta(f)   [unnormalized cross term, excl endpoints]
  C' = sum_{f in F_N, b>1} delta(f)^2              [unnormalized shift-squared, excl endpoints]
"""

from fractions import Fraction
from math import gcd
import sys

def farey_sequence(N):
    """Generate Farey sequence F_N as list of Fraction objects, from 0/1 to 1/1."""
    fracs = []
    for b in range(0, N+1):
        for a in range(0, b+1):
            if b == 0:
                continue
            if gcd(a, b) == 1:
                fracs.append(Fraction(a, b))
    fracs = sorted(set(fracs))
    return fracs

def mobius(n):
    """Compute Mobius function mu(n)."""
    if n == 1:
        return 1
    factors = []
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            temp //= d
            if temp % d == 0:
                return 0  # p^2 divides n
            d += 1
        else:
            d += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)

def mertens(N):
    """Compute Mertens function M(N) = sum_{k=1}^{N} mu(k)."""
    return sum(mobius(k) for k in range(1, N+1))

def compute_for_prime(p):
    """Compute all quantities for prime p using exact Fraction arithmetic."""
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)
    n_prime = n + (p - 1)  # |F_p|

    # Compute D(f) for each f in F_N
    # D(f_j) = j - n * f_j, where j is 0-indexed rank
    D_vals = {}
    for j, f in enumerate(F_N):
        D_vals[f] = Fraction(j) - Fraction(n) * f

    # Compute delta(f) for each f in F_N
    # delta(a/b) = (a - (p*a mod b)) / b
    delta_vals = {}
    for f in F_N:
        a = f.numerator
        b = f.denominator
        if b == 1:
            # f = 0/1: delta = (0 - 0)/1 = 0
            # f = 1/1: delta = (1 - (p mod 1))/1 = (1 - 0)/1 = 1
            delta_vals[f] = Fraction(a - (p * a % b), b) if b > 0 else Fraction(0)
        else:
            delta_vals[f] = Fraction(a - (p * a % b), b)

    # Verify delta matches f - {pf}
    for f in F_N:
        pf = p * f
        frac_part = pf - int(pf)  # This is exact for Fraction
        alt_delta = f - frac_part
        assert delta_vals[f] == alt_delta, f"Delta mismatch at f={f}: {delta_vals[f]} vs {alt_delta}"

    # B' = 2 * sum_{b>1} D(f) * delta(f)  [excluding f=0/1 and f=1/1]
    B_prime = Fraction(0)
    for f in F_N:
        if f.denominator == 1:
            continue  # skip 0/1 and 1/1
        B_prime += D_vals[f] * delta_vals[f]
    B_prime = 2 * B_prime

    # C' = sum_{b>1} delta(f)^2
    C_prime = Fraction(0)
    for f in F_N:
        if f.denominator == 1:
            continue
        C_prime += delta_vals[f] ** 2

    # Full sums (including endpoints) for cross-checking
    B_full = Fraction(0)
    C_full = Fraction(0)
    for f in F_N:
        B_full += D_vals[f] * delta_vals[f]
        C_full += delta_vals[f] ** 2
    B_full = 2 * B_full
    C_full_val = C_full

    # Cross-term identity check: sum D(f) * delta(f)^2 = -1/2 * sum delta(f)^2 - 1/2
    # (Theorem from paper, eq cross-term)
    lhs_ct = sum(D_vals[f] * delta_vals[f]**2 for f in F_N)
    rhs_ct = -Fraction(1,2) * C_full - Fraction(1,2)
    ct_identity_holds = (lhs_ct == rhs_ct)

    # Endpoint contributions to B
    D0_delta0 = D_vals[Fraction(0)] * delta_vals[Fraction(0)]  # should be 0
    D1_delta1 = D_vals[Fraction(1)] * delta_vals[Fraction(1)]  # should be -1

    # Mertens function
    M_N = mertens(N)
    M_p = mertens(p)

    # ---- Möbius decomposition ----
    # R(f) = sum_{d<=N} mu(d) * sum_{m<=N/d} {f*m}
    # where {x} = x - floor(x)
    mu_cache = {d: mobius(d) for d in range(1, N+1)}

    R_vals = {}
    for f in F_N:
        R_f = Fraction(0)
        for d in range(1, N+1):
            if mu_cache[d] == 0:
                continue
            inner = Fraction(0)
            for m in range(1, N // d + 1):
                fm = f * m
                frac_part = fm - int(fm)
                inner += frac_part
            R_f += mu_cache[d] * inner
        R_vals[f] = R_f

    # sum R(f)*delta(f) over all f in F_N
    sum_R_delta_full = sum(R_vals[f] * delta_vals[f] for f in F_N)
    sum_R_delta_interior = sum(R_vals[f] * delta_vals[f] for f in F_N if f.denominator > 1)

    # Check identity: B' + C' = -2 * sum_interior R*delta
    # Actually need to figure out the exact identity. Let's check both versions.
    identity_check_interior = B_prime + C_prime + 2 * sum_R_delta_interior
    identity_check_full_B = B_full + C_full_val + 2 * sum_R_delta_full

    # Correction = sum_R_delta - M(N) * C'/2
    # Using interior sums
    correction_interior = sum_R_delta_interior - Fraction(M_N) * C_prime / 2

    # Using full sums
    correction_full = sum_R_delta_full - Fraction(M_N) * C_full_val / 2

    # Correction/C' ratio
    if C_prime != 0:
        corr_ratio_interior = correction_interior / C_prime
    else:
        corr_ratio_interior = None

    # Check formula: B' = (|M(p-1)| - 2) * C' - 2*correction
    # where correction = sum_R_delta_interior - M(N)*C'/2
    if M_N != 0:
        B_predicted = (abs(M_N) - 2) * C_prime - 2 * correction_interior
    else:
        B_predicted = None

    # Also check: B' = -M(N)*C' - 2*sum_R_delta_interior - C'  (rearranging)
    # Actually let's derive: if D(f) = sum_{d<=N} mu(d) * sum_{m<=N/d} {fm} - 1/2 + boundary
    # The exact relation between D and R needs care. Let me just check numerically.

    # Alternative: from Displacement-Shift and Möbius inversion
    # D(f) = sum_{d<=N} mu(d) * floor(N*f/d) - n*f... no, let me think.
    # Actually D(f_j) = j - n*f = rank(f) - n*f
    # rank(f=a/b) = sum_{d=1}^{N} sum_{c=1, gcd(c,d)=1}^{d} [c/d <= a/b]
    # = sum_{d=1}^{N} sum_{c=1}^{floor(d*a/b)} [gcd(c,d)=1]
    # This is getting complex. Let me just report the numerical checks.

    return {
        'p': p,
        'N': N,
        'n': n,
        'n_prime': n_prime,
        'B_prime': B_prime,
        'C_prime': C_prime,
        'B_full': B_full,
        'C_full': C_full_val,
        'D0_delta0': D0_delta0,
        'D1_delta1': D1_delta1,
        'ct_identity': ct_identity_holds,
        'M_N': M_N,
        'M_p': M_p,
        'sum_R_delta_full': sum_R_delta_full,
        'sum_R_delta_interior': sum_R_delta_interior,
        'identity_check_interior': identity_check_interior,
        'identity_check_full': identity_check_full_B,
        'correction_interior': correction_interior,
        'correction_full': correction_full,
        'corr_ratio_interior': corr_ratio_interior,
        'B_predicted': B_predicted,
    }

def main():
    primes = [11, 13, 17, 19, 23, 29, 31, 37, 43, 47, 53, 71, 97]

    print("=" * 120)
    print("B EXACT AUDIT — All computations use fractions.Fraction (zero floating point)")
    print("=" * 120)

    results = []
    for p in primes:
        print(f"\nComputing p = {p}...", file=sys.stderr)
        r = compute_for_prime(p)
        results.append(r)

    # ========== TASK 1 ==========
    print("\n" + "=" * 120)
    print("TASK 1: B' and C' (unnormalized, excluding b=1 endpoints)")
    print("=" * 120)
    print(f"{'p':>4} {'N':>4} {'n':>6} {'n_prime':>7} {'M(N)':>5} {'M(p)':>5} {'B_prime':>40} {'C_prime':>30} {'B>0?':>5}")
    print("-" * 120)
    for r in results:
        B_sign = "YES" if r['B_prime'] > 0 else "NO"
        print(f"{r['p']:>4} {r['N']:>4} {r['n']:>6} {r['n_prime']:>7} {r['M_N']:>5} {r['M_p']:>5} {str(r['B_prime']):>40} {str(r['C_prime']):>30} {B_sign:>5}")

    print("\nEndpoint contributions (D(0)*delta(0), D(1)*delta(1)):")
    for r in results:
        print(f"  p={r['p']}: D(0)*delta(0) = {r['D0_delta0']}, D(1)*delta(1) = {r['D1_delta1']}")

    print(f"\nB_full = B_prime + 2*(D(0)*delta(0) + D(1)*delta(1)) = B_prime + 2*(0 + (-1)) = B_prime - 2")
    for r in results:
        expected = r['B_prime'] - 2
        actual = r['B_full']
        match = "OK" if expected == actual else "MISMATCH!"
        print(f"  p={r['p']}: B_full = {r['B_full']}, B_prime - 2 = {expected}  [{match}]")

    print(f"\nCross-term identity: sum D*delta^2 = -1/2 * sum delta^2 - 1/2")
    for r in results:
        status = "HOLDS" if r['ct_identity'] else "FAILS!"
        print(f"  p={r['p']}: {status}")

    # ========== TASK 1 FLOAT DISPLAY ==========
    print("\n" + "-" * 80)
    print("B' and C' as decimals (for readability only; all computation was exact):")
    print(f"{'p':>4} {'B_prime':>20} {'C_prime':>20} {'B/C':>15}")
    print("-" * 65)
    for r in results:
        B_f = float(r['B_prime'])
        C_f = float(r['C_prime'])
        BC = B_f / C_f if C_f != 0 else float('nan')
        print(f"{r['p']:>4} {B_f:>20.10f} {C_f:>20.10f} {BC:>15.10f}")

    # ========== TASK 2 ==========
    print("\n" + "=" * 120)
    print("TASK 2: Möbius decomposition")
    print("=" * 120)

    print(f"\n{'p':>4} {'M(N)':>5} {'sum_R*delta(int)':>30} {'sum_R*delta(full)':>30}")
    print("-" * 75)
    for r in results:
        print(f"{r['p']:>4} {r['M_N']:>5} {str(r['sum_R_delta_interior']):>30} {str(r['sum_R_delta_full']):>30}")

    print(f"\nIdentity check: B' + C' + 2*sum_R_delta_interior = 0?")
    for r in results:
        val = r['identity_check_interior']
        status = "EXACT 0" if val == 0 else f"= {val} (NONZERO!)"
        print(f"  p={r['p']}: {status}")

    print(f"\nIdentity check (full sums): B_full + C_full + 2*sum_R_delta_full = 0?")
    for r in results:
        val = r['identity_check_full']
        status = "EXACT 0" if val == 0 else f"= {val} (NONZERO!)"
        print(f"  p={r['p']}: {status}")

    print(f"\nCorrection = sum_R_delta_interior - M(N)*C'/2:")
    print(f"{'p':>4} {'M(N)':>5} {'correction':>35} {'corr/C_prime':>30}")
    print("-" * 80)
    for r in results:
        corr_str = str(r['correction_interior'])
        ratio_str = str(r['corr_ratio_interior']) if r['corr_ratio_interior'] is not None else "N/A"
        print(f"{r['p']:>4} {r['M_N']:>5} {corr_str:>35} {ratio_str:>30}")

    print(f"\nCorrection/C' as decimal:")
    for r in results:
        if r['corr_ratio_interior'] is not None:
            print(f"  p={r['p']}: {float(r['corr_ratio_interior']):.15f}")

    # ========== TASK 2: B' prediction formula ==========
    print(f"\nFormula check: B' = (|M(N)| - 2)*C' - 2*correction?")
    for r in results:
        if r['B_predicted'] is not None:
            match = "EXACT" if r['B_predicted'] == r['B_prime'] else f"MISMATCH (predicted {r['B_predicted']})"
            print(f"  p={r['p']}: M(N)={r['M_N']}, B'={r['B_prime']}, predicted={r['B_predicted']}  [{match}]")

    # Let's also try: B' = -M(N)*C' - 2*sum_R_delta_interior
    # From B' + C' = -2*sum_R_delta_interior (if that holds)
    # => B' = -C' - 2*sum_R_delta_interior
    # But that's just tautological if the identity holds.
    #
    # The user's formula: B' = (|M(N)| - 2)*C' - 2*correction
    # = (|M(N)|-2)*C' - 2*(sum_R_delta - M(N)*C'/2)
    # = (|M(N)|-2)*C' - 2*sum_R_delta + M(N)*C'
    # If M(N) < 0: |M(N)| = -M(N), so:
    # = (-M(N)-2)*C' - 2*sum_R_delta + M(N)*C'
    # = -M(N)*C' - 2*C' - 2*sum_R_delta + M(N)*C'
    # = -2*C' - 2*sum_R_delta
    # = -2*(C' + sum_R_delta)
    # But we need B' = -2*(C' + sum_R_delta) - ... hmm
    # From identity: B' + C' = -2*sum_R_delta => B' = -C' - 2*sum_R_delta
    # And the formula gives: -2*C' - 2*sum_R_delta = B' - C'
    # So formula = B' - C', not B'. Unless I'm wrong about the identity.
    # Let me just check numerically.

    print(f"\nDirect check: B' = -C' - 2*sum_R_delta_interior?")
    for r in results:
        predicted2 = -r['C_prime'] - 2 * r['sum_R_delta_interior']
        match = "EXACT" if predicted2 == r['B_prime'] else f"MISMATCH (got {predicted2})"
        print(f"  p={r['p']}: {match}")

    # ========== TASK 3 ==========
    print("\n" + "=" * 120)
    print("TASK 3: M(p) = -3 primes analysis")
    print("=" * 120)

    m3_primes = [r for r in results if r['M_p'] == -3]
    print(f"\nPrimes with M(p) = -3: {[r['p'] for r in m3_primes]}")

    if m3_primes:
        print(f"\n{'p':>4} {'M(N)':>5} {'M(p)':>5} {'B_prime':>30} {'C_prime':>25} {'corr/C':>20} {'|corr/C|<1/2?':>15}")
        print("-" * 110)
        for r in m3_primes:
            ratio = r['corr_ratio_interior']
            if ratio is not None:
                lt_half = abs(ratio) < Fraction(1, 2)
                print(f"{r['p']:>4} {r['M_N']:>5} {r['M_p']:>5} {str(r['B_prime']):>30} {str(r['C_prime']):>25} {float(ratio):>20.15f} {'YES' if lt_half else 'NO':>15}")
            else:
                print(f"{r['p']:>4} {r['M_N']:>5} {r['M_p']:>5} {str(r['B_prime']):>30} {str(r['C_prime']):>25} {'N/A':>20} {'N/A':>15}")

    # Formula check for M(p)=-3:
    # User asks: B' = (|M(p)|-2)*C' - 2*correction = (3-2)*C' - 2*correction = C' - 2*correction
    # Note: user uses M(p) not M(N)=M(p-1). Let me check both.
    print(f"\nFormula: B' = (|M(p)|-2)*C' - 2*correction  [using M(p)]")
    for r in m3_primes:
        # correction with M(p) instead of M(N)
        corr_Mp = r['sum_R_delta_interior'] - Fraction(r['M_p']) * r['C_prime'] / 2
        predicted = (abs(r['M_p']) - 2) * r['C_prime'] - 2 * corr_Mp
        match = "EXACT" if predicted == r['B_prime'] else f"OFF by {predicted - r['B_prime']}"
        print(f"  p={r['p']}: M(p)={r['M_p']}, M(N)={r['M_N']}, predicted={predicted}, actual={r['B_prime']}  [{match}]")

    print(f"\nFormula: B' = (|M(N)|-2)*C' - 2*correction  [using M(N)=M(p-1)]")
    for r in m3_primes:
        predicted = r['B_predicted']
        match = "EXACT" if predicted == r['B_prime'] else f"OFF by {predicted - r['B_prime']}"
        print(f"  p={r['p']}: M(N)={r['M_N']}, predicted={predicted}, actual={r['B_prime']}  [{match}]")

    # Also check for ALL primes, not just M(p)=-3
    print(f"\n\nFormula check for ALL primes: B' = (|M(N)|-2)*C' - 2*correction [using M(N)]")
    for r in results:
        if r['B_predicted'] is not None:
            match = "EXACT" if r['B_predicted'] == r['B_prime'] else f"OFF by {r['B_predicted'] - r['B_prime']}"
            print(f"  p={r['p']}: M(N)={r['M_N']}, [{match}]")

    # Let's try a different formula derivation.
    # We know B' + C' = -2*sum_R_delta (if the identity holds).
    # Define correction = sum_R_delta - M(N)*C'/2
    # Then sum_R_delta = correction + M(N)*C'/2
    # B' = -C' - 2*sum_R_delta = -C' - 2*correction - M(N)*C'
    # = -(1 + M(N))*C' - 2*correction
    # If M(N) < 0: -(1+M(N)) = |M(N)| - 1
    # So B' = (|M(N)| - 1)*C' - 2*correction  [for M(N) < 0]
    # NOT (|M(N)| - 2)*C'!

    print(f"\n\nCorrected formula derivation:")
    print(f"  B' + C' = -2*sum_R_delta  [identity]")
    print(f"  correction = sum_R_delta - M(N)*C'/2")
    print(f"  => sum_R_delta = correction + M(N)*C'/2")
    print(f"  => B' = -C' - 2*(correction + M(N)*C'/2)")
    print(f"  => B' = -C' - 2*correction - M(N)*C'")
    print(f"  => B' = -(1 + M(N))*C' - 2*correction")
    print(f"  For M(N) < 0: -(1+M(N)) = |M(N)| - 1")
    print(f"  => B' = (|M(N)| - 1)*C' - 2*correction")

    print(f"\nVerification: B' = (|M(N)|-1)*C' - 2*correction?")
    for r in results:
        M = r['M_N']
        predicted3 = (abs(M) - 1) * r['C_prime'] - 2 * r['correction_interior']
        match = "EXACT" if predicted3 == r['B_prime'] else f"OFF by {predicted3 - r['B_prime']}"
        print(f"  p={r['p']}: M(N)={M}, [{match}]")

    # Summary
    print("\n" + "=" * 120)
    print("SUMMARY")
    print("=" * 120)
    print(f"\n1. B' > 0 for all tested primes: {all(r['B_prime'] > 0 for r in results)}")
    b_neg = [r['p'] for r in results if r['B_prime'] <= 0]
    if b_neg:
        print(f"   Primes where B' <= 0: {b_neg}")

    print(f"\n2. Cross-term identity (sum D*delta^2 = -1/2*sum delta^2 - 1/2) holds for all: {all(r['ct_identity'] for r in results)}")

    id_holds = all(r['identity_check_interior'] == 0 for r in results)
    print(f"\n3. Identity B' + C' = -2*sum_R*delta (interior) holds for all: {id_holds}")
    if not id_holds:
        for r in results:
            if r['identity_check_interior'] != 0:
                print(f"   FAILS at p={r['p']}: residual = {r['identity_check_interior']}")

    id_full_holds = all(r['identity_check_full'] == 0 for r in results)
    print(f"\n4. Identity B_full + C_full = -2*sum_R*delta (full) holds for all: {id_full_holds}")
    if not id_full_holds:
        for r in results:
            if r['identity_check_full'] != 0:
                print(f"   FAILS at p={r['p']}: residual = {r['identity_check_full']}")

    print(f"\n5. For M(p)=-3 primes, |correction/C'| < 1/2:")
    for r in m3_primes:
        ratio = r['corr_ratio_interior']
        if ratio is not None:
            print(f"   p={r['p']}: corr/C' = {float(ratio):.15f}, |.| < 1/2: {abs(ratio) < Fraction(1,2)}")


if __name__ == '__main__':
    main()
