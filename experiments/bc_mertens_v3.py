#!/usr/bin/env python3
"""
Compute B, C, R(p), B+C for all primes p from 11 to 3000.
V3: Pure integer arithmetic, final rational assembly only at the end.

Strategy:
- For each prime p with N=p-1, generate Farey sequence F_N
- For each fraction a/b in F_N (b>1):
    D_num = rank*b - |F_N|*a  (D = D_num / b)
    delta_num = a - (p*a % b)  (delta = delta_num / b)
    Contribution to B_sum: D_num * delta_num  (over b^2)
    Contribution to C_sum: delta_num^2          (over b^2)
- Final: B = 2 * sum(D_num*delta_num / b^2), C = sum(delta_num^2 / b^2)
- We group by b: for each b, accumulate S_B[b] and S_C[b] as plain integers
- Then B = 2 * sum_b (S_B[b] / b^2), C = sum_b (S_C[b] / b^2)
- To get exact B+C, compute common denominator = lcm of all b^2
  OR just use Python's Fraction for the final ~N terms (one per b).

Actually even smarter: accumulate everything over a single common denominator.
B and C share denominator structure. Let's just compute:
  B_exact = Fraction sum over all b of S_B[b]/b^2
This is at most ~3000 Fraction additions (one per b), which is fast.
"""

from fractions import Fraction
from math import gcd
import time

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
    """Generate Farey sequence F_N using next-term algorithm.
    Returns list of (a, b) pairs in order."""
    result = [(0, 1)]
    a, b = 0, 1
    c, d = 1, N
    while c <= N:
        result.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    return result

def compute_BC_fast(p):
    """
    Integer-accumulation approach.
    Group contributions by denominator b, then combine with Fraction at end.
    """
    N = p - 1
    farey = farey_mediant(N)
    size = len(farey)

    # For each denominator b, accumulate integer sums
    # S_B[b] = sum over a with gcd(a,b)=1 of D_num * delta_num
    # S_C[b] = sum over a with gcd(a,b)=1 of delta_num^2
    # where D_num = rank*b - size*a, delta_num = a - (p*a % b)
    S_B = {}  # b -> int
    S_C = {}  # b -> int

    for rank, (a, b) in enumerate(farey):
        if b == 1:
            continue
        D_num = rank * b - size * a
        delta_num = a - ((p * a) % b)

        if b not in S_B:
            S_B[b] = 0
            S_C[b] = 0
        S_B[b] += D_num * delta_num
        S_C[b] += delta_num * delta_num

    # Now assemble exact B and C using Fraction (one addition per b value)
    B_half = Fraction(0)  # = sum S_B[b]/b^2
    C_val = Fraction(0)   # = sum S_C[b]/b^2

    for b in S_B:
        b2 = b * b
        if S_B[b] != 0:
            B_half += Fraction(S_B[b], b2)
        if S_C[b] != 0:
            C_val += Fraction(S_C[b], b2)

    B_val = 2 * B_half
    # R = B/(2C) = B_half / C_val
    if C_val == 0:
        R = None
    else:
        R = Fraction(B_half, C_val)  # wrong: Fraction(a,b) expects ints
    # Fix: R = B_half / C_val
    if C_val != 0:
        R = B_half / C_val

    return B_val, C_val, R

def main():
    MAX_P = 3000
    print(f"Computing Mertens function up to {MAX_P}...")
    M = mertens_values(MAX_P)

    primes = [p for p in sieve_primes(MAX_P) if p >= 11]
    print(f"Found {len(primes)} primes from 11 to {MAX_P}")

    # Time test on large prime
    test_p = primes[-1]
    print(f"Timing test: p={test_p}...")
    t0 = time.time()
    B, C, R = compute_BC_fast(test_p)
    t1 = time.time()
    print(f"  p={test_p}: {t1-t0:.2f}s, R={float(R):.6f}, B+C={float(B+C):.4f}")

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
        elif p < 50:
            print(f"  p={p}: M(p)={mp}, B={float(B):.4f}, C={float(C):.4f}, B+C={float(bc_sum):.4f}, R={float(R):.6f}")

    elapsed = time.time() - t0
    print(f"\nTotal computation: {elapsed:.1f}s for {len(primes)} primes")

    # === Build report ===
    by_mertens = {}
    for p, mp, B, C, bc_sum, R in results:
        by_mertens.setdefault(mp, []).append((p, B, C, bc_sum, R))

    lines = []
    lines.append("# B+C by Mertens Class: Complete Verification (p=11..3000)\n\n")
    lines.append(f"- {len(primes)} primes computed with exact Fraction arithmetic\n")
    lines.append(f"- Computation time: {elapsed:.1f}s\n")
    lines.append(f"- Date: 2026-03-29\n\n")

    # ========== KEY: M(p) <= -3 ==========
    le3 = [(p,mp,B,C,bc,R) for p,mp,B,C,bc,R in results if mp <= -3]
    lines.append("## 1. M(p) <= -3 class (Sign Theorem domain)\n\n")
    lines.append(f"**{len(le3)} primes** in this class.\n\n")

    min_bc_e = min(le3, key=lambda x: x[4])
    min_R_e = min(le3, key=lambda x: x[5] if x[5] is not None else Fraction(10**9))
    neg_bc = [x for x in le3 if x[4] <= 0]
    neg_R = [x for x in le3 if x[5] is not None and x[5] < Fraction(-1, 2)]

    lines.append(f"- Min B+C = **{float(min_bc_e[4]):.6f}** at p={min_bc_e[0]} (M(p)={min_bc_e[1]})\n")
    lines.append(f"- Min R = **{float(min_R_e[5]):.6f}** at p={min_R_e[0]} (M(p)={min_R_e[1]})\n")
    lines.append(f"- B+C <= 0: **{len(neg_bc)} primes**\n")
    lines.append(f"- R < -0.5: **{len(neg_R)} primes**\n\n")

    if not neg_bc:
        lines.append("### CONFIRMED: B+C > 0 for ALL M(p) <= -3 primes up to 3000.\n\n")
    else:
        lines.append("### WARNING: COUNTEREXAMPLES FOUND!\n\n")
        for x in neg_bc:
            lines.append(f"- p={x[0]}, M(p)={x[1]}, B+C={float(x[4]):.6f}\n")
        lines.append("\n")

    if not neg_R:
        lines.append("### CONFIRMED: R > -0.5 for ALL M(p) <= -3 primes up to 3000.\n\n")

    # Table: smallest B+C
    lines.append("### Smallest B+C (M(p) <= -3):\n\n")
    lines.append("| p | M(p) | B | C | B+C | R |\n")
    lines.append("|--:|-----:|--:|--:|----:|--:|\n")
    for x in sorted(le3, key=lambda x: x[4])[:15]:
        lines.append(f"| {x[0]} | {x[1]} | {float(x[2]):.4f} | {float(x[3]):.4f} | {float(x[4]):.4f} | {float(x[5]):.6f} |\n")
    lines.append("\n")

    # Table: most negative R
    lines.append("### Most negative R (M(p) <= -3):\n\n")
    lines.append("| p | M(p) | R | B+C |\n")
    lines.append("|--:|-----:|--:|----:|\n")
    for x in sorted(le3, key=lambda x: x[5] if x[5] is not None else Fraction(10**9))[:15]:
        lines.append(f"| {x[0]} | {x[1]} | {float(x[5]):.6f} | {float(x[4]):.4f} |\n")
    lines.append("\n")

    # ========== M(p) = -2 and -1 ==========
    for mval in [-2, -1]:
        subset = [x for x in results if x[1] == mval]
        if not subset:
            continue
        lines.append(f"## 2. M(p) = {mval} class ({len(subset)} primes)\n\n")
        neg_b = [x for x in subset if x[4] <= 0]
        neg_r = [x for x in subset if x[5] is not None and x[5] < Fraction(-1, 2)]
        min_b = min(subset, key=lambda x: x[4])
        min_r = min(subset, key=lambda x: x[5] if x[5] is not None else Fraction(10**9))
        lines.append(f"- Min B+C = {float(min_b[4]):.6f} at p={min_b[0]}\n")
        lines.append(f"- Min R = {float(min_r[5]):.6f} at p={min_r[0]}\n")
        lines.append(f"- B+C <= 0: {len(neg_b)}\n")
        lines.append(f"- R < -0.5: {len(neg_r)}\n\n")
        if neg_b:
            lines.append("B+C <= 0 cases:\n")
            for x in neg_b[:10]:
                lines.append(f"  p={x[0]}, B+C={float(x[4]):.4f}, R={float(x[5]):.6f}\n")
            lines.append("\n")

    # ========== M(p) >= 0: first R < -0.5 ==========
    lines.append("## 3. M(p) >= 0: where does B+C first go negative?\n\n")
    pos = [x for x in results if x[1] >= 0]
    neg_pos_bc = [x for x in pos if x[4] < 0]
    neg_pos_R = [x for x in pos if x[5] is not None and x[5] < Fraction(-1, 2)]
    if neg_pos_bc:
        lines.append(f"First B+C < 0 with M(p) >= 0: p={neg_pos_bc[0][0]}, M(p)={neg_pos_bc[0][1]}, B+C={float(neg_pos_bc[0][4]):.4f}\n\n")
        lines.append("All such primes:\n\n| p | M(p) | B+C | R |\n|--:|-----:|----:|--:|\n")
        for x in neg_pos_bc[:30]:
            lines.append(f"| {x[0]} | {x[1]} | {float(x[4]):.4f} | {float(x[5]):.6f} |\n")
        lines.append("\n")
    else:
        lines.append("No primes with M(p) >= 0 have B+C < 0 in this range.\n\n")

    if neg_pos_R:
        lines.append(f"First R < -0.5 with M(p) >= 0: p={neg_pos_R[0][0]}, M(p)={neg_pos_R[0][1]}, R={float(neg_pos_R[0][5]):.6f}\n\n")

    # ========== FULL SUMMARY TABLE ==========
    lines.append("## 4. Summary by Mertens Class\n\n")
    lines.append("| M(p) | Count | Min R | Max R | Min B+C | Max B+C | #(B+C<=0) | #(R<-0.5) |\n")
    lines.append("|-----:|------:|------:|------:|--------:|--------:|----------:|-----------:|\n")

    for mv in sorted(by_mertens.keys()):
        ents = by_mertens[mv]
        cnt = len(ents)
        # ents[i] = (p, B, C, bc_sum, R)
        bcs = [e[3] for e in ents]
        Rs = [e[4] for e in ents if e[4] is not None]
        mnbc = float(min(bcs))
        mxbc = float(max(bcs))
        nbc = sum(1 for v in bcs if v <= 0)
        if Rs:
            mnR = float(min(Rs))
            mxR = float(max(Rs))
            nR = sum(1 for v in Rs if v < Fraction(-1, 2))
        else:
            mnR = mxR = float('nan')
            nR = 0
        lines.append(f"| {mv} | {cnt} | {mnR:.4f} | {mxR:.4f} | {mnbc:.4f} | {mxbc:.4f} | {nbc} | {nR} |\n")

    lines.append("\n")

    # ========== ALL B+C < 0 PRIMES ==========
    all_neg = [x for x in results if x[4] < 0]
    lines.append("## 5. Complete list: all primes with B+C < 0\n\n")
    if all_neg:
        lines.append(f"**{len(all_neg)} primes** total.\n\n")
        lines.append("| p | M(p) | B | C | B+C | R |\n")
        lines.append("|--:|-----:|--:|--:|----:|--:|\n")
        for x in all_neg:
            lines.append(f"| {x[0]} | {x[1]} | {float(x[2]):.4f} | {float(x[3]):.4f} | {float(x[4]):.4f} | {float(x[5]):.6f} |\n")
        lines.append("\n")
        # Check: are they ALL with M(p) >= some threshold?
        min_m = min(x[1] for x in all_neg)
        max_m = max(x[1] for x in all_neg)
        lines.append(f"M(p) range for B+C < 0: [{min_m}, {max_m}]\n\n")
    else:
        lines.append("None found.\n\n")

    # ========== CONCLUSION ==========
    lines.append("## 6. Conclusion\n\n")
    if not neg_bc:
        lines.append("**The Sign Theorem hypothesis is CONFIRMED for all M(p) <= -3 primes up to p=3000:**\n\n")
        lines.append("- B+C > 0 for every such prime (no exceptions)\n")
        if not neg_R:
            lines.append("- In fact R > -0.5 for every such prime (stronger than needed)\n")
        lines.append("- B+C < 0 occurs ONLY for primes with large positive M(p)\n\n")

    if all_neg:
        lines.append(f"B+C < 0 first appears at p={all_neg[0][0]} with M(p)={all_neg[0][1]}.\n")
        lines.append(f"The minimum M(p) among B+C < 0 primes is {min_m}.\n")
        if min_m > -3:
            lines.append(f"Since {min_m} > -3, the Sign Theorem domain (M(p) <= -3) is safe.\n")

    report = "".join(lines)
    with open("/Users/saar/Desktop/Farey-Local/experiments/BC_BY_MERTENS_CLASS.md", "w") as f:
        f.write(report)

    print("\nReport written to BC_BY_MERTENS_CLASS.md")
    print("\n" + "="*70)
    print("KEY FINDINGS:")
    print("="*70)
    print(f"M(p) <= -3 class: {len(le3)} primes")
    print(f"  Min B+C: {float(min_bc_e[4]):.6f} at p={min_bc_e[0]}")
    print(f"  Min R:   {float(min_R_e[5]):.6f} at p={min_R_e[0]}")
    print(f"  Any B+C <= 0? {bool(neg_bc)}")
    print(f"  Any R < -0.5? {bool(neg_R)}")
    if all_neg:
        print(f"\nTotal B+C < 0 primes: {len(all_neg)}")
        print(f"  M(p) range: [{min(x[1] for x in all_neg)}, {max(x[1] for x in all_neg)}]")
        print(f"  First: p={all_neg[0][0]}, M(p)={all_neg[0][1]}")

if __name__ == "__main__":
    main()
