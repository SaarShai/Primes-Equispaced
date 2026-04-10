#!/usr/bin/env python3
"""
Compute B, C, R(p), B+C for all primes p from 11 to 3000.
Classify by M(p) = Mertens function value.
Use exact Fraction arithmetic throughout.
"""

from fractions import Fraction
from math import gcd
import time

def sieve_mobius(n):
    """Compute Mobius function for 1..n."""
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
    """Compute M(k) = sum_{j=1}^{k} mu(j) for k=1..n."""
    mu = sieve_mobius(n)
    M = [0] * (n + 1)
    for k in range(1, n + 1):
        M[k] = M[k - 1] + mu[k]
    return M

def sieve_primes(n):
    """Simple sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

def farey_sequence(N):
    """Generate Farey sequence F_N as list of Fraction, 0/1 to N/N=1/1."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def compute_BC(p):
    """
    For prime p, N = p-1:
    - Build F_N
    - Compute D(a/b) = rank - |F_N| * (a/b)  [rank is 0-indexed]
    - delta(a/b) = (a - (p*a mod b)) / b
    - B = 2 * sum D*delta (b>1)
    - C = sum delta^2 (b>1)
    Returns B, C, R = B/(2C)
    """
    N = p - 1
    farey = farey_sequence(N)
    size = len(farey)  # |F_N|
    size_frac = Fraction(size)

    B = Fraction(0)
    C = Fraction(0)

    for rank, f in enumerate(farey):
        a = f.numerator
        b = f.denominator
        if b == 1:
            continue  # skip 0/1 and 1/1

        D = Fraction(rank) - size_frac * f
        delta = Fraction(a - ((p * a) % b), b)

        B += D * delta
        C += delta * delta

    B = 2 * B
    # R = B / (2C)
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

    # Results: list of (p, M(p), B, C, B+C, R)
    results = []
    t0 = time.time()

    for i, p in enumerate(primes):
        B, C, R = compute_BC(p)
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

    # Analysis
    print("\n" + "="*80)
    print("CLASSIFICATION BY MERTENS VALUE")
    print("="*80)

    # For the report
    report_lines = []
    report_lines.append("# B+C by Mertens Class: Complete Verification\n")
    report_lines.append(f"Computed for all {len(primes)} primes from 11 to {MAX_P}.\n")
    report_lines.append(f"Computation time: {elapsed:.1f}s using exact Fraction arithmetic.\n\n")

    # Key question: M(p) <= -3
    report_lines.append("## Key Question: Is B+C > 0 for ALL primes with M(p) <= -3?\n\n")

    le_minus3 = []
    for p, mp, B, C, bc_sum, R in results:
        if mp <= -3:
            le_minus3.append((p, mp, B, C, bc_sum, R))

    if le_minus3:
        min_bc = min(x[4] for x in le_minus3)
        min_R = min(x[5] for x in le_minus3 if x[5] is not None)
        max_R = max(x[5] for x in le_minus3 if x[5] is not None)
        neg_bc = [x for x in le_minus3 if x[4] <= 0]
        neg_R_half = [x for x in le_minus3 if x[5] is not None and x[5] < Fraction(-1, 2)]

        report_lines.append(f"Count of primes with M(p) <= -3: **{len(le_minus3)}**\n\n")
        report_lines.append(f"Min B+C: {float(min_bc):.6f} (at p={[x for x in le_minus3 if x[4]==min_bc][0][0]})\n\n")
        report_lines.append(f"Min R: {float(min_R):.6f} (at p={[x for x in le_minus3 if x[5]==min_R][0][0]})\n\n")
        report_lines.append(f"Max R: {float(max_R):.6f}\n\n")
        report_lines.append(f"Primes with B+C <= 0: **{len(neg_bc)}**\n\n")
        report_lines.append(f"Primes with R < -0.5: **{len(neg_R_half)}**\n\n")

        if neg_bc:
            report_lines.append("### COUNTEREXAMPLES (B+C <= 0 with M(p) <= -3):\n\n")
            for p, mp, B, C, bc_sum, R in neg_bc:
                report_lines.append(f"- p={p}, M(p)={mp}, B+C={float(bc_sum):.6f}, R={float(R):.6f}\n")
            report_lines.append("\n")
        else:
            report_lines.append("**RESULT: B+C > 0 for ALL primes with M(p) <= -3.** No counterexamples found.\n\n")

        if neg_R_half:
            report_lines.append("### Primes with R < -0.5 and M(p) <= -3:\n\n")
            for p, mp, B, C, bc_sum, R in neg_R_half:
                report_lines.append(f"- p={p}, M(p)={mp}, R={float(R):.6f}, B+C={float(bc_sum):.6f}\n")
            report_lines.append("\n")
        else:
            report_lines.append("**R >= -0.5 for ALL primes with M(p) <= -3.**\n\n")

        # Show the 10 smallest B+C values
        report_lines.append("### 10 smallest B+C values (M(p) <= -3 class):\n\n")
        report_lines.append("| p | M(p) | B (float) | C (float) | B+C (float) | R (float) |\n")
        report_lines.append("|---|------|-----------|-----------|-------------|----------|\n")
        sorted_bc = sorted(le_minus3, key=lambda x: x[4])
        for p, mp, B, C, bc_sum, R in sorted_bc[:10]:
            report_lines.append(f"| {p} | {mp} | {float(B):.4f} | {float(C):.4f} | {float(bc_sum):.4f} | {float(R):.6f} |\n")
        report_lines.append("\n")

        # Show the 10 most negative R values
        report_lines.append("### 10 most negative R values (M(p) <= -3 class):\n\n")
        report_lines.append("| p | M(p) | R (float) | B+C (float) |\n")
        report_lines.append("|---|------|-----------|-------------|\n")
        sorted_R = sorted(le_minus3, key=lambda x: x[5] if x[5] is not None else Fraction(999))
        for p, mp, B, C, bc_sum, R in sorted_R[:10]:
            report_lines.append(f"| {p} | {mp} | {float(R):.6f} | {float(bc_sum):.4f} |\n")
        report_lines.append("\n")

    # Now do each Mertens class
    report_lines.append("## Full Classification by Mertens Value\n\n")

    for mp_val in sorted(by_mertens.keys()):
        entries = by_mertens[mp_val]
        count = len(entries)
        bc_vals = [x[3] + x[2] for x in entries]  # B+C = B + C... wait, x is (p, B, C, bc_sum, R)
        # Actually: entries[i] = (p, B, C, bc_sum, R)
        bc_vals = [x[3] for x in entries]  # bc_sum
        R_vals = [x[4] for x in entries if x[4] is not None]

        min_bc = min(bc_vals)
        max_bc = max(bc_vals)
        neg_count = sum(1 for v in bc_vals if v <= 0)

        if R_vals:
            min_R_val = min(R_vals)
            max_R_val = max(R_vals)
            neg_R_count = sum(1 for v in R_vals if v < Fraction(-1, 2))
        else:
            min_R_val = max_R_val = None
            neg_R_count = 0

        report_lines.append(f"### M(p) = {mp_val} ({count} primes)\n\n")
        report_lines.append(f"- B+C range: [{float(min_bc):.4f}, {float(max_bc):.4f}]\n")
        report_lines.append(f"- B+C <= 0 count: {neg_count}\n")
        if min_R_val is not None:
            report_lines.append(f"- R range: [{float(min_R_val):.6f}, {float(max_R_val):.6f}]\n")
            report_lines.append(f"- R < -0.5 count: {neg_R_count}\n")

        # List primes with B+C <= 0
        if neg_count > 0:
            report_lines.append(f"- **B+C <= 0 primes:** ")
            negs = [(x[0], x[3], x[4]) for x in entries if x[3] <= 0]
            report_lines.append(", ".join(f"p={p}(B+C={float(bc):.4f},R={float(r):.4f})" for p, bc, r in negs))
            report_lines.append("\n")

        # List primes with R < -0.5
        if neg_R_count > 0:
            report_lines.append(f"- **R < -0.5 primes:** ")
            neg_rs = [(x[0], x[4]) for x in entries if x[4] is not None and x[4] < Fraction(-1, 2)]
            report_lines.append(", ".join(f"p={p}(R={float(r):.6f})" for p, r in neg_rs))
            report_lines.append("\n")

        report_lines.append("\n")

    # Summary table: min R and min B+C by Mertens class
    report_lines.append("## Summary Table: Min R and Min B+C by Mertens Class\n\n")
    report_lines.append("| M(p) | Count | Min R | Min B+C | B+C<=0? | R<-0.5? | First B+C<=0 |\n")
    report_lines.append("|------|-------|-------|---------|---------|---------|-------------|\n")

    for mp_val in sorted(by_mertens.keys()):
        entries = by_mertens[mp_val]
        count = len(entries)
        bc_vals = [x[3] for x in entries]
        R_vals = [x[4] for x in entries if x[4] is not None]
        min_bc = min(bc_vals)
        neg_count = sum(1 for v in bc_vals if v <= 0)
        if R_vals:
            min_R_val = min(R_vals)
            neg_R_count = sum(1 for v in R_vals if v < Fraction(-1, 2))
        else:
            min_R_val = None
            neg_R_count = 0

        first_neg = ""
        if neg_count > 0:
            for x in entries:
                if x[3] <= 0:
                    first_neg = str(x[0])
                    break

        min_R_str = f"{float(min_R_val):.4f}" if min_R_val is not None else "N/A"
        report_lines.append(f"| {mp_val} | {count} | {min_R_str} | {float(min_bc):.4f} | {'YES('+str(neg_count)+')' if neg_count else 'No'} | {'YES('+str(neg_R_count)+')' if neg_R_count else 'No'} | {first_neg} |\n")

    report_lines.append("\n")

    # The critical question answered
    report_lines.append("## Conclusion\n\n")

    any_neg_le3 = any(1 for p, mp, B, C, bc_sum, R in results if mp <= -3 and bc_sum <= 0)
    any_neg_R_le3 = any(1 for p, mp, B, C, bc_sum, R in results if mp <= -3 and R is not None and R < Fraction(-1, 2))

    if not any_neg_le3:
        report_lines.append("**B+C > 0 for ALL primes with M(p) <= -3 up to p=3000.** The Sign Theorem holds.\n\n")
    else:
        report_lines.append("**WARNING: B+C <= 0 found for some primes with M(p) <= -3!**\n\n")

    if not any_neg_R_le3:
        report_lines.append("**R > -0.5 for ALL primes with M(p) <= -3 up to p=3000.** This is stronger than needed.\n\n")

    # First prime with B+C < 0 overall
    first_neg_overall = None
    for p, mp, B, C, bc_sum, R in results:
        if bc_sum < 0:
            first_neg_overall = (p, mp, float(B), float(C), float(bc_sum), float(R))
            break

    if first_neg_overall:
        p, mp, Bf, Cf, bcf, Rf = first_neg_overall
        report_lines.append(f"First prime with B+C < 0 overall: p={p}, M(p)={mp}, B={Bf:.4f}, C={Cf:.4f}, B+C={bcf:.4f}, R={Rf:.6f}\n\n")

    # Transition analysis
    report_lines.append("## Transition Analysis: Where does B+C first go negative?\n\n")
    report_lines.append("| p | M(p) | B+C (float) | R (float) | B+C sign |\n")
    report_lines.append("|---|------|-------------|-----------|----------|\n")
    # Show around the transition
    for p, mp, B, C, bc_sum, R in results:
        if bc_sum < 0 or (R is not None and R < Fraction(-1, 2)):
            report_lines.append(f"| {p} | {mp} | {float(bc_sum):.4f} | {float(R):.6f} | {'NEG' if bc_sum<0 else 'pos'} |\n")

    report_lines.append("\n")

    # Write report
    report = "".join(report_lines)
    with open("/Users/saar/Desktop/Farey-Local/experiments/BC_BY_MERTENS_CLASS.md", "w") as f:
        f.write(report)

    print("\nReport written to BC_BY_MERTENS_CLASS.md")
    print(report[:3000])

if __name__ == "__main__":
    main()
