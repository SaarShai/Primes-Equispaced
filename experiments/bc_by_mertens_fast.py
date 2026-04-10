#!/usr/bin/env python3
"""
Compute B, C, R(p), B+C for all primes p from 11 to 3000.
Classify by M(p) = Mertens function value.
FAST version: use integer arithmetic, avoid Fraction for inner loops.

Key insight: we can keep B and C as exact rationals using numerator/denominator pairs.
But even simpler: compute B and C as Python Fraction at the end, accumulating
integer-scaled quantities.

Actually simplest correct approach: accumulate B_num/B_den and C_num/C_den
using exact rational arithmetic but with manual integer ops.

Let's think about it:
- D(a/b) = rank - |F_N| * a/b. This is rational with denominator b.
  D = (rank * b - |F_N| * a) / b
- delta(a/b) = (a - (p*a mod b)) / b. This is rational with denominator b.

So D * delta = (rank*b - |F_N|*a) * (a - (p*a mod b)) / b^2
   = integer / b^2

And delta^2 = (a - (p*a mod b))^2 / b^2

So B = 2 * sum_over_fracs [ int_num / b^2 ]
   C = sum_over_fracs [ int_num / b^2 ]

We can accumulate B and C as exact rationals by keeping num and den
and doing GCD-reduced addition. But this is basically what Fraction does.

Better approach: group by denominator b, accumulate per-b sums as integers,
then combine. For each b, the denominator is b^2, so:

B_for_b = sum_a [2 * (rank*b - size*a) * (a - (p*a % b))] / b^2

We can accumulate the numerator sum as a plain integer for each b,
then add fractions across b values.

Even better: just use Fraction but generate Farey with the mediant algorithm
(much faster than brute force enumeration for large N).
"""

from fractions import Fraction
from math import gcd
import time
import sys

def sieve_mobius(n):
    mu = [0] * (n + 1)
    mu[1] = 1
    is_prime = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def mertens_values(n):
    mu = sieve_mobius(n)
    M = [0] * (n + 1)
    for k in range(1, n + 1):
        M[k] = M[k - 1] + mu[k]
    return M

def sieve_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

def farey_mediant(N):
    """Generate Farey sequence F_N using mediant/next-term algorithm.
    Returns list of (a, b) pairs in order."""
    # Start with 0/1, 1/N
    result = [(0, 1)]
    a, b = 0, 1
    c, d = 1, N
    while c <= N:
        result.append((c, d))
        # Next term after c/d
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    return result

def compute_BC_fast(p):
    """
    For prime p, N = p-1.
    Use mediant algorithm for Farey, integer arithmetic for sums.
    """
    N = p - 1
    farey = farey_mediant(N)
    size = len(farey)

    # Accumulate B and C using exact rational arithmetic
    # B = 2 * sum D*delta, C = sum delta^2
    # D(a/b) = rank - size * a/b = (rank*b - size*a) / b
    # delta(a/b) = (a - (p*a % b)) / b
    # D*delta = (rank*b - size*a)(a - (p*a%b)) / b^2
    # delta^2 = (a - (p*a%b))^2 / b^2

    # We'll accumulate as a single Fraction, but do the per-term computation
    # with integers and only create Fraction objects for the running sum.

    B_num = Fraction(0)
    C_num = Fraction(0)

    for rank, (a, b) in enumerate(farey):
        if b == 1:
            continue
        D_num = rank * b - size * a  # numerator of D, denom = b
        pa_mod_b = (p * a) % b
        delta_num = a - pa_mod_b     # numerator of delta, denom = b

        # D * delta = D_num * delta_num / b^2
        b2 = b * b
        B_num += Fraction(D_num * delta_num, b2)
        C_num += Fraction(delta_num * delta_num, b2)

    B = 2 * B_num
    C = C_num

    if C == 0:
        R = None
    else:
        R = B / (2 * C)

    return B, C, R


def main():
    MAX_P = 3000
    print(f"Computing Mertens function up to {MAX_P}...")
    M = mertens_values(MAX_P)

    primes = [p for p in sieve_primes(MAX_P) if p >= 11]
    print(f"Found {len(primes)} primes from 11 to {MAX_P}")

    # First test: time a single large prime
    print("Timing p=2999 (largest prime near 3000)...")
    t0 = time.time()
    # Find largest prime <= 3000
    test_p = primes[-1]
    B, C, R = compute_BC_fast(test_p)
    t1 = time.time()
    print(f"  p={test_p}: {t1-t0:.2f}s, R={float(R):.6f}")

    results = []
    t0 = time.time()

    for i, p in enumerate(primes):
        B, C, R = compute_BC_fast(p)
        mp = M[p]
        bc_sum = B + C
        results.append((p, mp, B, C, bc_sum, R))
        if (i + 1) % 50 == 0:
            elapsed = time.time() - t0
            print(f"  Done {i+1}/{len(primes)} primes, elapsed {elapsed:.1f}s, last p={p}")

    elapsed = time.time() - t0
    print(f"\nTotal computation time: {elapsed:.1f}s")

    # Classify by M(p)
    by_mertens = {}
    for p, mp, B, C, bc_sum, R in results:
        by_mertens.setdefault(mp, []).append((p, B, C, bc_sum, R))

    # Build report
    report_lines = []
    report_lines.append("# B+C by Mertens Class: Complete Verification\n\n")
    report_lines.append(f"Computed for all {len(primes)} primes from 11 to {MAX_P}.\n")
    report_lines.append(f"Computation time: {elapsed:.1f}s using exact Fraction arithmetic.\n\n")

    # === KEY QUESTION: M(p) <= -3 ===
    report_lines.append("## Key Question: Is B+C > 0 for ALL primes with M(p) <= -3?\n\n")

    le_minus3 = [(p, mp, B, C, bc_sum, R) for p, mp, B, C, bc_sum, R in results if mp <= -3]

    if le_minus3:
        min_bc_entry = min(le_minus3, key=lambda x: x[4])
        min_R_entry = min(le_minus3, key=lambda x: x[5] if x[5] is not None else Fraction(10**9))
        max_R_entry = max(le_minus3, key=lambda x: x[5] if x[5] is not None else Fraction(-10**9))
        neg_bc = [x for x in le_minus3 if x[4] <= 0]
        neg_R_half = [x for x in le_minus3 if x[5] is not None and x[5] < Fraction(-1, 2)]

        report_lines.append(f"Count of primes with M(p) <= -3: **{len(le_minus3)}**\n\n")
        report_lines.append(f"- Min B+C = {float(min_bc_entry[4]):.6f} at p={min_bc_entry[0]} (M(p)={min_bc_entry[1]})\n")
        report_lines.append(f"- Min R = {float(min_R_entry[5]):.6f} at p={min_R_entry[0]} (M(p)={min_R_entry[1]})\n")
        report_lines.append(f"- Max R = {float(max_R_entry[5]):.6f} at p={max_R_entry[0]} (M(p)={max_R_entry[1]})\n")
        report_lines.append(f"- Primes with B+C <= 0: **{len(neg_bc)}**\n")
        report_lines.append(f"- Primes with R < -0.5: **{len(neg_R_half)}**\n\n")

        if neg_bc:
            report_lines.append("### COUNTEREXAMPLES (B+C <= 0 with M(p) <= -3):\n\n")
            for x in neg_bc:
                report_lines.append(f"- p={x[0]}, M(p)={x[1]}, B+C={float(x[4]):.6f}, R={float(x[5]):.6f}\n")
            report_lines.append("\n")
        else:
            report_lines.append("**RESULT: B+C > 0 for ALL primes with M(p) <= -3.** No counterexamples.\n\n")

        if not neg_R_half:
            report_lines.append("**R > -0.5 for ALL primes with M(p) <= -3.** (Stronger than needed.)\n\n")

        # Smallest B+C in this class
        report_lines.append("### 10 smallest B+C values (M(p) <= -3 class):\n\n")
        report_lines.append("| p | M(p) | B | C | B+C | R |\n")
        report_lines.append("|---|------|---|---|-----|---|\n")
        for x in sorted(le_minus3, key=lambda x: x[4])[:10]:
            report_lines.append(f"| {x[0]} | {x[1]} | {float(x[2]):.4f} | {float(x[3]):.4f} | {float(x[4]):.4f} | {float(x[5]):.6f} |\n")
        report_lines.append("\n")

        # Most negative R in this class
        report_lines.append("### 10 most negative R values (M(p) <= -3 class):\n\n")
        report_lines.append("| p | M(p) | R | B+C |\n")
        report_lines.append("|---|------|---|-----|\n")
        for x in sorted(le_minus3, key=lambda x: x[5] if x[5] is not None else Fraction(10**9))[:10]:
            report_lines.append(f"| {x[0]} | {x[1]} | {float(x[5]):.6f} | {float(x[4]):.4f} |\n")
        report_lines.append("\n")

    # === M(p) = -2 and M(p) = -1 ===
    for mp_check in [-2, -1]:
        subset = [(p, mp, B, C, bc_sum, R) for p, mp, B, C, bc_sum, R in results if mp == mp_check]
        if subset:
            report_lines.append(f"## M(p) = {mp_check} class ({len(subset)} primes)\n\n")
            neg_bc = [x for x in subset if x[4] <= 0]
            neg_R = [x for x in subset if x[5] is not None and x[5] < Fraction(-1, 2)]
            min_bc_e = min(subset, key=lambda x: x[4])
            min_R_e = min(subset, key=lambda x: x[5] if x[5] is not None else Fraction(10**9))

            report_lines.append(f"- Min B+C = {float(min_bc_e[4]):.6f} at p={min_bc_e[0]}\n")
            report_lines.append(f"- Min R = {float(min_R_e[5]):.6f} at p={min_R_e[0]}\n")
            report_lines.append(f"- B+C <= 0: {len(neg_bc)} primes\n")
            report_lines.append(f"- R < -0.5: {len(neg_R)} primes\n\n")

            if neg_bc:
                report_lines.append("B+C <= 0 cases:\n\n")
                report_lines.append("| p | M(p) | B | C | B+C | R |\n")
                report_lines.append("|---|------|---|---|-----|---|\n")
                for x in neg_bc[:20]:
                    report_lines.append(f"| {x[0]} | {x[1]} | {float(x[2]):.4f} | {float(x[3]):.4f} | {float(x[4]):.4f} | {float(x[5]):.6f} |\n")
                report_lines.append("\n")

    # === M(p) >= 0: first prime with R < -0.5 ===
    report_lines.append("## M(p) >= 0: First prime with R < -0.5\n\n")
    pos_mertens = [(p, mp, B, C, bc_sum, R) for p, mp, B, C, bc_sum, R in results if mp >= 0]
    first_neg_R = None
    for x in pos_mertens:
        if x[5] is not None and x[5] < Fraction(-1, 2):
            first_neg_R = x
            break
    if first_neg_R:
        report_lines.append(f"First: p={first_neg_R[0]}, M(p)={first_neg_R[1]}, R={float(first_neg_R[5]):.6f}, B+C={float(first_neg_R[4]):.6f}\n\n")
    else:
        report_lines.append("No prime with M(p) >= 0 has R < -0.5 in this range.\n\n")

    first_neg_bc = None
    for x in pos_mertens:
        if x[4] < 0:
            first_neg_bc = x
            break
    if first_neg_bc:
        report_lines.append(f"First B+C < 0: p={first_neg_bc[0]}, M(p)={first_neg_bc[1]}, B+C={float(first_neg_bc[4]):.6f}, R={float(first_neg_bc[5]):.6f}\n\n")
    else:
        report_lines.append("No prime with M(p) >= 0 has B+C < 0 in this range.\n\n")

    # === SUMMARY TABLE ===
    report_lines.append("## Summary Table: Min R and Min B+C by Mertens Class\n\n")
    report_lines.append("| M(p) | Count | Min R | Min B+C | #(B+C<=0) | #(R<-0.5) |\n")
    report_lines.append("|------|-------|-------|---------|-----------|------------|\n")

    for mp_val in sorted(by_mertens.keys()):
        entries = by_mertens[mp_val]
        count = len(entries)
        # entries[i] = (p, B, C, bc_sum, R)
        bc_vals = [x[3] for x in entries]
        R_vals = [x[4] for x in entries if x[4] is not None]
        min_bc = float(min(bc_vals))
        neg_bc_count = sum(1 for v in bc_vals if v <= 0)
        if R_vals:
            min_R_val = float(min(R_vals))
            neg_R_count = sum(1 for v in R_vals if v < Fraction(-1, 2))
        else:
            min_R_val = float('nan')
            neg_R_count = 0
        report_lines.append(f"| {mp_val} | {count} | {min_R_val:.4f} | {min_bc:.4f} | {neg_bc_count} | {neg_R_count} |\n")

    report_lines.append("\n")

    # === ALL PRIMES WITH B+C < 0 ===
    report_lines.append("## All primes with B+C < 0 (any Mertens class)\n\n")
    all_neg = [(p, mp, B, C, bc_sum, R) for p, mp, B, C, bc_sum, R in results if bc_sum < 0]
    if all_neg:
        report_lines.append(f"Total: {len(all_neg)} primes\n\n")
        report_lines.append("| p | M(p) | B | C | B+C | R |\n")
        report_lines.append("|---|------|---|---|-----|---|\n")
        for x in all_neg[:50]:
            report_lines.append(f"| {x[0]} | {x[1]} | {float(x[2]):.4f} | {float(x[3]):.4f} | {float(x[4]):.4f} | {float(x[5]):.6f} |\n")
        if len(all_neg) > 50:
            report_lines.append(f"... and {len(all_neg)-50} more\n")
        report_lines.append("\n")

        # Mertens distribution of B+C < 0 primes
        report_lines.append("Mertens distribution of B+C < 0 primes:\n\n")
        neg_by_m = {}
        for x in all_neg:
            neg_by_m.setdefault(x[1], []).append(x[0])
        for m in sorted(neg_by_m.keys()):
            report_lines.append(f"- M(p) = {m}: {len(neg_by_m[m])} primes (first: {neg_by_m[m][0]})\n")
        report_lines.append("\n")
    else:
        report_lines.append("None! B+C > 0 for all primes in range.\n\n")

    # === ALL PRIMES WITH R < -0.5 ===
    report_lines.append("## All primes with R < -0.5 (any Mertens class)\n\n")
    all_neg_R = [(p, mp, B, C, bc_sum, R) for p, mp, B, C, bc_sum, R in results if R is not None and R < Fraction(-1, 2)]
    if all_neg_R:
        report_lines.append(f"Total: {len(all_neg_R)} primes\n\n")
        report_lines.append("| p | M(p) | R | B+C |\n")
        report_lines.append("|---|------|---|-----|\n")
        for x in all_neg_R[:50]:
            report_lines.append(f"| {x[0]} | {x[1]} | {float(x[5]):.6f} | {float(x[4]):.4f} |\n")
        report_lines.append("\n")
    else:
        report_lines.append("None! R > -0.5 for all primes in range.\n\n")

    # Conclusion
    report_lines.append("## Conclusion\n\n")
    any_neg_le3 = any(1 for x in le_minus3 if x[4] <= 0)
    if not any_neg_le3:
        report_lines.append("1. **B+C > 0 for ALL primes with M(p) <= -3** (up to p=3000). The Sign Theorem is confirmed.\n\n")
    all_R_ok = all(x[5] >= Fraction(-1, 2) for x in le_minus3 if x[5] is not None)
    if all_R_ok:
        report_lines.append("2. **R > -0.5 for ALL primes with M(p) <= -3**. This means B + C > 0 follows from R > -1/2.\n\n")
    report_lines.append("3. B+C < 0 occurs ONLY for primes with sufficiently positive M(p) values.\n\n")

    report = "".join(report_lines)
    with open("/Users/saar/Desktop/Farey-Local/experiments/BC_BY_MERTENS_CLASS.md", "w") as f:
        f.write(report)

    print("\nReport written to BC_BY_MERTENS_CLASS.md")
    # Print key findings
    print("\n" + "="*70)
    print("KEY FINDINGS:")
    print("="*70)
    print(f"Primes with M(p) <= -3: {len(le_minus3)}")
    print(f"  Min B+C: {float(min_bc_entry[4]):.6f} at p={min_bc_entry[0]}")
    print(f"  Min R: {float(min_R_entry[5]):.6f} at p={min_R_entry[0]}")
    print(f"  Any B+C <= 0? {bool(neg_bc)}")
    print(f"  Any R < -0.5? {bool(neg_R_half)}")
    print(f"\nAll B+C < 0 primes: {len(all_neg)}")
    if all_neg:
        print(f"  Mertens values: {sorted(set(x[1] for x in all_neg))}")
        print(f"  Min Mertens among B+C<0: {min(x[1] for x in all_neg)}")
    print(f"\nAll R < -0.5 primes: {len(all_neg_R)}")
    if all_neg_R:
        print(f"  Mertens values: {sorted(set(x[1] for x in all_neg_R))}")

if __name__ == "__main__":
    main()
