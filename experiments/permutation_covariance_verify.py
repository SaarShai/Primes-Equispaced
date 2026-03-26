"""
Verify the Permutation Covariance Formula for B_raw and new insights:
1. B_raw = 2 * Sum_b (1/b) * Sum_{gcd(a,b)=1} a * [D(a/b) - D(p^{-1}a/b)]
2. Check D-monotonicity within each denominator
3. Measure within-denominator variance of D vs. O(b^2) claim
4. Test the Fourier-sign conjecture
"""

from math import gcd
from fractions import Fraction
import sys

def farey_sequence(N):
    """Generate Farey sequence F_N as list of Fraction objects."""
    fs = [Fraction(0, 1)]
    a, b, c, d = 0, 1, 1, N
    while c <= N:
        fs.append(Fraction(c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
    return fs

def mod_inverse(a, m):
    """Compute modular inverse of a mod m."""
    # Extended Euclidean
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def analyze_prime(p):
    N = p - 1
    if N < 2:
        return None

    # Build Farey sequence F_N
    farey = farey_sequence(N)
    n = len(farey)

    # Build discrepancy function D: fraction -> D(f) = rank - n*f
    # rank is 0-indexed (0/1 has rank 0)
    D = {}
    for i, f in enumerate(farey):
        D[f] = i - n * float(f)

    # Compute standard B_raw and delta_sq
    B_raw_direct = 0.0
    delta_sq = 0.0

    for b in range(2, N+1):
        for a in range(1, b):
            if gcd(a, b) != 1:
                continue
            f = Fraction(a, b)
            sigma_pa = (p * a) % b  # sigma_p(a) = pa mod b
            delta_val = (a - sigma_pa) / b
            D_val = D[f]
            B_raw_direct += 2 * D_val * delta_val
            delta_sq += delta_val**2

    B_plus_C_direct = B_raw_direct + delta_sq

    # Compute B_raw via permutation covariance formula:
    # B_raw = 2 * Sum_b (1/b) * Sum_{gcd(a,b)=1} a * [D(a/b) - D(p^{-1}*a/b)]
    B_raw_pcf = 0.0

    for b in range(2, N+1):
        p_inv = mod_inverse(p % b, b)
        if p_inv is None:
            continue  # Skip if no inverse (only when gcd(p,b) != 1, impossible since p is prime and b < p)

        for a in range(1, b):
            if gcd(a, b) != 1:
                continue

            # p^{-1} * a mod b
            p_inv_a = (p_inv * a) % b

            f1 = Fraction(a, b)
            # p^{-1}*a mod b is a coprime residue mod b, so p_inv_a/b is in F_N
            f2 = Fraction(p_inv_a, b)

            # Both f1 and f2 should be in F_N (they are Farey fractions with denom b <= N)
            if f1 not in D or f2 not in D:
                continue

            B_raw_pcf += 2 * (1/b) * a * (D[f1] - D[f2])

    # Check D-monotonicity within each denominator b
    monotone_violations = 0
    total_comparisons = 0
    worst_b = None
    worst_ratio = 0

    for b in range(2, min(N+1, 30)):  # Check small denominators
        coprime_a = [a for a in range(1, b) if gcd(a, b) == 1]
        D_vals = [D[Fraction(a, b)] for a in coprime_a]

        violations_b = 0
        for i in range(len(D_vals)-1):
            total_comparisons += 1
            if D_vals[i] > D_vals[i+1]:  # Non-monotone
                violations_b += 1
                monotone_violations += 1

        if len(coprime_a) > 1 and violations_b > 0:
            ratio = violations_b / (len(coprime_a) - 1)
            if ratio > worst_ratio:
                worst_ratio = ratio
                worst_b = b

    # Measure within-denominator variance of D vs O(b^2) claim
    var_data = []
    for b in range(2, min(N+1, 50)):
        coprime_a = [a for a in range(1, b) if gcd(a, b) == 1]
        if len(coprime_a) < 2:
            continue
        D_vals = [D[Fraction(a, b)] for a in coprime_a]
        mean_D = sum(D_vals) / len(D_vals)
        var_D = sum((d - mean_D)**2 for d in D_vals) / len(D_vals)
        var_data.append((b, var_D, b**2))

    # Compute per-denominator contribution to R = B_raw / delta_sq
    R = B_raw_direct / delta_sq if delta_sq > 0 else float('nan')

    return {
        'p': p,
        'N': N,
        'n': n,
        'B_raw_direct': B_raw_direct,
        'B_raw_pcf': B_raw_pcf,
        'pcf_match': abs(B_raw_direct - B_raw_pcf) < 1e-8,
        'delta_sq': delta_sq,
        'B_plus_C': B_plus_C_direct,
        'B_plus_C_positive': B_plus_C_direct > 0,
        'R': R,
        'monotone_violations': monotone_violations,
        'total_comparisons': total_comparisons,
        'worst_b': worst_b,
        'worst_ratio': worst_ratio,
        'var_data': var_data[:5],  # First 5 denominators' variance data
    }


def main():
    # Test for small primes
    primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
              101, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173]

    print("=" * 90)
    print("PERMUTATION COVARIANCE FORMULA VERIFICATION")
    print("=" * 90)
    print(f"\n{'p':>6} | {'N':>5} | {'PCF match':>10} | {'B+C>0':>7} | {'R':>8} | "
          f"{'Mon.viol':>9} | {'Worst b':>8} | {'Worst%':>7}")
    print("-" * 90)

    all_pcf_match = True
    all_bc_positive = True

    for p in primes:
        result = analyze_prime(p)
        if result is None:
            continue

        all_pcf_match = all_pcf_match and result['pcf_match']
        all_bc_positive = all_bc_positive and result['B_plus_C_positive']

        mon_rate = result['monotone_violations'] / result['total_comparisons'] if result['total_comparisons'] > 0 else 0
        print(f"{p:>6} | {result['N']:>5} | {'YES':>10} if {result['pcf_match']} | "
              f"{'YES' if result['B_plus_C_positive'] else 'NO':>7} | "
              f"{result['R']:>8.4f} | "
              f"{result['monotone_violations']:>4}/{result['total_comparisons']:<4} | "
              f"b={result['worst_b']:>3} | "
              f"{100*result['worst_ratio']:>6.1f}%")

    print()
    print(f"Permutation Covariance Formula verified: {all_pcf_match}")
    print(f"B+C > 0 for all tested primes: {all_bc_positive}")

    # Show variance data for p=47 as example
    print("\n" + "=" * 70)
    print("WITHIN-DENOMINATOR VARIANCE OF D (p=47, N=46)")
    print("Claim: Var_b(D) = O(b^2)")
    print("=" * 70)
    result_47 = analyze_prime(47)
    print(f"\n{'b':>5} | {'Var_b(D)':>12} | {'b^2':>8} | {'Var/b^2':>10}")
    print("-" * 50)
    for b, var_D, b2 in result_47['var_data']:
        print(f"{b:>5} | {var_D:>12.4f} | {b2:>8} | {var_D/b2:>10.6f}")

    # Full variance analysis for larger prime
    print("\n" + "=" * 70)
    print("EXTENDED VARIANCE ANALYSIS (p=101, N=100)")
    print("=" * 70)
    result_101 = analyze_prime(101)

    N = 100
    farey = farey_sequence(N)
    n_101 = len(farey)
    D_101 = {}
    for i, f in enumerate(farey):
        D_101[f] = i - n_101 * float(f)

    max_var_ratio = 0
    var_ratios = []
    for b in range(2, N+1):
        coprime_a = [a for a in range(1, b) if gcd(a, b) == 1]
        if len(coprime_a) < 2:
            continue
        D_vals = [D_101[Fraction(a, b)] for a in coprime_a]
        mean_D = sum(D_vals) / len(D_vals)
        var_D = sum((d - mean_D)**2 for d in D_vals) / len(D_vals)
        ratio = var_D / (b**2) if b > 0 else 0
        var_ratios.append(ratio)
        if ratio > max_var_ratio:
            max_var_ratio = ratio

    print(f"\nMax Var_b(D)/b^2 over all b in [2,{N}]: {max_var_ratio:.6f}")
    print(f"Mean Var_b(D)/b^2: {sum(var_ratios)/len(var_ratios):.6f}")
    print(f"\nIf Var_b(D) = O(b^2) then this ratio should be O(1).")
    print(f"Max ratio = {max_var_ratio:.4f} suggests the O(b^2) bound")
    print(f"{'HOLDS' if max_var_ratio < 10 else 'may need adjustment'}.")

    # Test monotonicity more extensively
    print("\n" + "=" * 70)
    print("D-MONOTONICITY STATISTICS (p=101, N=100)")
    print("=" * 70)

    violations_per_b = {}
    for b in range(2, N+1):
        coprime_a = [a for a in range(1, b) if gcd(a, b) == 1]
        D_vals = [D_101[Fraction(a, b)] for a in coprime_a]
        viol = sum(1 for i in range(len(D_vals)-1) if D_vals[i] > D_vals[i+1])
        violations_per_b[b] = (viol, len(coprime_a)-1 if len(coprime_a) > 1 else 0)

    total_viol = sum(v for v, t in violations_per_b.values())
    total_comp = sum(t for v, t in violations_per_b.values())
    print(f"\nTotal monotonicity violations: {total_viol}/{total_comp} ({100*total_viol/total_comp:.1f}%)")
    print("(D-monotonicity is FALSE in general -- violations confirm our analysis)")

    # Show the permutation covariance B_raw for p where B_raw is small
    print("\n" + "=" * 70)
    print("B_raw SIGN ANALYSIS via Permutation Covariance Formula")
    print("= B_raw = 2 * Sum_b (1/b) * Sum_a a * [D(a/b) - D(p^{-1}*a/b)]")
    print("=" * 70)
    print(f"\n{'p':>5} | {'B_raw':>12} | {'delta_sq':>12} | {'R=B/C':>8} | {'1+R (B+C)/C':>13}")
    print("-" * 70)

    for p in primes[:20]:
        result = analyze_prime(p)
        if result:
            print(f"{p:>5} | {result['B_raw_direct']:>12.4f} | {result['delta_sq']:>12.4f} | "
                  f"{result['R']:>8.4f} | {1+result['R']:>13.4f}")


if __name__ == '__main__':
    main()
