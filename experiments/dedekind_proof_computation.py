#!/usr/bin/env python3
"""
Dedekind Sum Proof Path for R(p) > -1/2.

EXACT arithmetic computation:
1. C(p,b) = Σ_{gcd(a,b)=1} ((a/b)) * ((pa/b))   [coprime-restricted cross term]
2. s(p,b) = Σ_{k=1}^{b-1} ((k/b)) * ((kp/b))     [full Dedekind sum]
3. Find exact formula: C(p,b) = α*s(p,b) + β
4. Verify Dedekind reciprocity
5. Compute R(p) via Dedekind sums and verify against known values
6. Analyze summed Dedekind bounds for proof of R(p) > -1/2
"""

from fractions import Fraction
from math import gcd, log, sqrt
import json
import sys

# ============================================================
# EXACT ARITHMETIC PRIMITIVES
# ============================================================

def sawtooth_exact(x_frac):
    """
    ((x)) = x - floor(x) - 1/2 if x not integer, else 0.
    x_frac must be a Fraction.
    """
    # floor of a Fraction
    fl = int(x_frac)
    if x_frac < 0 and x_frac != Fraction(fl):
        fl -= 1
    frac_part = x_frac - fl
    if frac_part == 0:
        return Fraction(0)
    return frac_part - Fraction(1, 2)


def euler_phi(n):
    result = n
    temp = n
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def moebius(n):
    if n == 1:
        return 1
    temp = n
    factors = []
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            count = 0
            while temp % p == 0:
                temp //= p
                count += 1
            if count > 1:
                return 0
            factors.append(p)
        p += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)


def coprime_residues(b):
    return [a for a in range(1, b) if gcd(a, b) == 1]


# ============================================================
# TASK 1: Exact C(p,b) and s(p,b) computation
# ============================================================

def compute_C_exact(p, b):
    """C(p,b) = Σ_{gcd(a,b)=1} ((a/b)) * ((pa/b)) using exact Fraction arithmetic."""
    total = Fraction(0)
    for a in coprime_residues(b):
        s1 = sawtooth_exact(Fraction(a, b))
        s2 = sawtooth_exact(Fraction(a * p, b))
        total += s1 * s2
    return total


def compute_dedekind_s_exact(h, k):
    """
    s(h,k) = Σ_{a=1}^{k-1} ((a/k)) * ((ha/k))
    Full Dedekind sum over ALL residues 1..k-1.
    """
    total = Fraction(0)
    for a in range(1, k):
        s1 = sawtooth_exact(Fraction(a, k))
        s2 = sawtooth_exact(Fraction(a * h, k))
        total += s1 * s2
    return total


def compute_non_coprime_contribution(p, b):
    """
    Contribution from non-coprime residues:
    NC(p,b) = Σ_{gcd(a,b)>1, 1≤a<b} ((a/b)) * ((pa/b))
    So s(p,b) = C(p,b) + NC(p,b)
    """
    total = Fraction(0)
    for a in range(1, b):
        if gcd(a, b) > 1:
            s1 = sawtooth_exact(Fraction(a, b))
            s2 = sawtooth_exact(Fraction(a * p, b))
            total += s1 * s2
    return total


def verify_relationship(primes, B_max=50):
    """
    For each prime p and denominator b:
    - Compute C(p,b), s(p,b), NC(p,b) exactly
    - Check if C(p,b) = s(p,b) - NC(p,b)
    - Look for formula C(p,b) = α*s(p,b) + β
    """
    print("=" * 70)
    print("TASK 1: EXACT RELATIONSHIP C(p,b) vs s(p,b)")
    print("=" * 70)

    for p in primes:
        print(f"\n--- Prime p = {p} ---")
        print(f"{'b':>4} {'phi(b)':>6} {'C(p,b)':>20} {'s(p,b)':>20} {'NC(p,b)':>20} {'C/s':>12} {'C-s':>20}")

        C_vals = []
        s_vals = []
        NC_vals = []
        b_vals = []

        for b in range(2, B_max + 1):
            if gcd(p, b) > 1:
                continue

            C = compute_C_exact(p, b)
            s = compute_dedekind_s_exact(p, b)
            NC = compute_non_coprime_contribution(p, b)

            # Verify: s = C + NC
            assert s == C + NC, f"MISMATCH at p={p}, b={b}: s={s}, C+NC={C+NC}"

            ratio_str = "N/A"
            if s != 0:
                ratio = C / s
                ratio_str = str(ratio) if ratio.denominator < 1000 else f"{float(ratio):.6f}"

            diff = C - s

            print(f"{b:4d} {euler_phi(b):6d} {str(C):>20} {str(s):>20} {str(NC):>20} {ratio_str:>12} {str(diff):>20}")

            C_vals.append(C)
            s_vals.append(s)
            NC_vals.append(NC)
            b_vals.append(b)

        # Check: is C(p,b) always equal to s(p,b) for squarefree b?
        # (Because for squarefree b, every a < b with gcd(a,b)>1 has specific structure)
        print(f"\n  Summary for p = {p}:")
        n_match = sum(1 for C, s in zip(C_vals, s_vals) if C == s)
        n_total = len(C_vals)
        print(f"  C(p,b) == s(p,b): {n_match}/{n_total}")

        # For cases where C != s, analyze the difference
        diffs = [(b, C - s, NC) for b, C, s, NC in zip(b_vals, C_vals, s_vals, NC_vals) if C != s]
        if diffs:
            print(f"  Cases where C != s (difference = -NC):")
            for b, d, nc in diffs[:10]:
                print(f"    b={b}: diff = {d}, NC = {nc}, b squarefree? {moebius(b) != 0}")

    return b_vals, C_vals, s_vals


# ============================================================
# TASK 2: Dedekind reciprocity verification
# ============================================================

def verify_reciprocity(primes, B_max=50):
    """
    Verify: s(p,b) + s(b,p) = (p/b + b/p + 1/(pb))/12 - 1/4
    Then analyze: Σ_b s(p,b) = Σ_b [RHS - s(b,p)]
    """
    print("\n" + "=" * 70)
    print("TASK 3: DEDEKIND RECIPROCITY VERIFICATION")
    print("=" * 70)

    for p in primes:
        print(f"\n--- Prime p = {p} ---")

        sum_s_pb = Fraction(0)  # Σ s(p,b)
        sum_s_bp = Fraction(0)  # Σ s(b,p)
        sum_rhs = Fraction(0)   # Σ RHS of reciprocity
        sum_C = Fraction(0)     # Σ C(p,b)
        sum_delta_sq = Fraction(0)
        count = 0

        for b in range(2, B_max + 1):
            if gcd(p, b) > 1:
                continue

            s_pb = compute_dedekind_s_exact(p, b)
            s_bp = compute_dedekind_s_exact(b, p)

            # RHS of reciprocity
            rhs = (Fraction(p, b) + Fraction(b, p) + Fraction(1, p * b)) / 12 - Fraction(1, 4)

            # Verify reciprocity
            lhs = s_pb + s_bp
            assert lhs == rhs, f"Reciprocity FAILED: p={p}, b={b}: s(p,b)+s(b,p)={lhs}, RHS={rhs}"

            sum_s_pb += s_pb
            sum_s_bp += s_bp
            sum_rhs += rhs

            C = compute_C_exact(p, b)
            sum_C += C
            count += 1

        print(f"  Reciprocity verified for all {count} values of b up to {B_max}.")
        print(f"  Σ s(p,b) = {float(sum_s_pb):.8f}  (exact: {sum_s_pb})")
        print(f"  Σ s(b,p) = {float(sum_s_bp):.8f}  (exact: {sum_s_bp})")
        print(f"  Σ RHS    = {float(sum_rhs):.8f}  (exact: {sum_rhs})")
        print(f"  Check: Σ s(p,b) = Σ RHS - Σ s(b,p) = {float(sum_rhs - sum_s_bp):.8f}")
        print(f"  Σ C(p,b) = {float(sum_C):.8f}  (exact: {sum_C})")

        # Now analyze: Σ_b s(b,p) for fixed p
        # s(b,p) = Σ_{k=1}^{p-1} ((k/p))((kb/p))
        # For fixed p, the inner sum depends on b mod p only!
        print(f"\n  s(b,p) depends on b mod p only (for gcd(b,p)=1):")
        residue_vals = {}
        for b in range(2, max(B_max + 1, 3 * p)):
            if gcd(p, b) > 1:
                continue
            r = b % p
            if r not in residue_vals:
                residue_vals[r] = compute_dedekind_s_exact(b, p)
            else:
                # Verify: s(b,p) depends only on b mod p
                val = compute_dedekind_s_exact(b, p)
                assert val == residue_vals[r], f"s(b,p) NOT periodic: b={b}, r={r}"

        print(f"  Verified: s(b,p) is periodic in b with period p.")
        for r in sorted(residue_vals.keys()):
            print(f"    s(b≡{r} mod {p}, {p}) = {residue_vals[r]} = {float(residue_vals[r]):.8f}")

        # Sum of s(b,p) over one full period
        period_sum = sum(residue_vals.values())
        print(f"  Σ_{r} s(r,p) over coprime residues = {period_sum} = {float(period_sum):.8f}")
        print(f"  This is the average contribution per period.")


# ============================================================
# TASK 4: Compute R(p) via Dedekind sums
# ============================================================

def compute_R_via_dedekind(primes, B_max=100):
    """
    R(p) relates to per-step Farey discrepancy.

    The key quantity is:
      R(p) = Σ_{b coprime to p} C(p,b) / (normalization)

    We compute multiple versions:
    1. R_raw(p) = Σ C(p,b)
    2. R_weighted(p) = Σ C(p,b)/b
    3. R_mobius(p) = Σ μ(b)/φ(b) * C(p,b)
    4. Compare with known R(13) ≈ 0.051
    """
    print("\n" + "=" * 70)
    print("TASK 4: R(p) VIA DEDEKIND SUMS")
    print("=" * 70)

    for p in primes:
        print(f"\n--- Prime p = {p} ---")

        sum_C = Fraction(0)
        sum_C_over_b = Fraction(0)
        sum_C_mobius = Fraction(0)
        sum_s = Fraction(0)
        sum_s_over_b = Fraction(0)
        sum_delta_sq = Fraction(0)
        count = 0

        # Also compute Σ δ² for normalization
        # δ(a/b) at order N is roughly 1/(N*b) scale, but let's compute directly
        # For the per-step discrepancy, the relevant normalization is:
        # Σ_{b≤B, gcd(p,b)=1} φ(b) * (sawtooth variance per b)

        for b in range(2, B_max + 1):
            if gcd(p, b) > 1:
                continue

            C = compute_C_exact(p, b)
            s = compute_dedekind_s_exact(p, b)
            mu = moebius(b)
            phi = euler_phi(b)

            sum_C += C
            sum_C_over_b += C / b
            if mu != 0:
                sum_C_mobius += Fraction(mu, phi) * C
            sum_s += s
            sum_s_over_b += s / b

            # Compute Σ ((a/b))^2 for coprimes (this is Var term)
            for a in coprime_residues(b):
                saw = sawtooth_exact(Fraction(a, b))
                sum_delta_sq += saw * saw

            count += 1

        print(f"  B_max = {B_max}, {count} denominators")
        print(f"  Σ C(p,b)           = {float(sum_C):.8f}")
        print(f"  Σ C(p,b)/b         = {float(sum_C_over_b):.8f}")
        print(f"  Σ μ(b)/φ(b)*C(p,b) = {float(sum_C_mobius):.8f}")
        print(f"  Σ s(p,b)           = {float(sum_s):.8f}")
        print(f"  Σ s(p,b)/b         = {float(sum_s_over_b):.8f}")
        print(f"  Σ ((a/b))^2        = {float(sum_delta_sq):.8f}")

        # R as ratio
        if sum_delta_sq != 0:
            R_ratio = sum_C / sum_delta_sq
            print(f"  R = Σ C / Σ δ²     = {float(R_ratio):.8f}")
            print(f"  R exact             = {R_ratio}")

        # Using Dedekind sums instead
        if sum_delta_sq != 0:
            R_s_ratio = sum_s / sum_delta_sq
            print(f"  R_s = Σ s / Σ δ²   = {float(R_s_ratio):.8f}")


# ============================================================
# TASK 5: Summed Dedekind bounds analysis
# ============================================================

def analyze_summed_bounds(primes, B_max=200):
    """
    Analyze the growth of:
    - Σ_{b≤B} |s(p,b)| / b
    - Σ_{b≤B} s(p,b) / b  (with sign)
    - Σ_{b≤B} |C(p,b)| / b

    Using Rademacher's bound: |s(h,k)| ≤ (1/8) * (log k) + O(1)
    But actually the tighter bound is:
    |s(h,k)| ≤ (k + 1) / (12k) [for gcd(h,k)=1]
    which gives |s(h,k)| < 1/12 + 1/(12k)

    Wait, that's for NORMALIZED Dedekind sums.
    For the standard Dedekind sum, the bound is:
    |s(h,k)| ≤ (k-1)/12 [trivial bound]
    |s(h,k)| = O(k log k) [trivial]
    |s(h,k)| = O(log k) [Rademacher, via continued fraction]

    Actually Rademacher showed: |s(h,k)| ≤ (1/8)(log k + 1) for large k,
    but the precise statement involves the continued fraction expansion.
    """
    print("\n" + "=" * 70)
    print("TASK 5: SUMMED DEDEKIND BOUNDS ANALYSIS (float for speed)")
    print("=" * 70)

    from math import log

    for p in primes:
        print(f"\n--- Prime p = {p} ---")

        sum_abs_s_over_b = 0.0
        sum_s_over_b = 0.0
        sum_abs_C_over_b = 0.0
        sum_C_over_b = 0.0
        max_ratio_s_logb = 0.0

        b_track = []
        sum_track = []

        for b in range(2, B_max + 1):
            if gcd(p, b) > 1:
                continue

            # Use float for speed here
            s_pb = 0.0
            for k in range(1, b):
                fk = (k / b) - int(k / b)
                sk = (fk - 0.5) if abs(fk) > 1e-15 and abs(fk - 1) > 1e-15 else 0
                fkp = (k * p / b) - int(k * p / b)
                skp = (fkp - 0.5) if abs(fkp) > 1e-15 and abs(fkp - 1) > 1e-15 else 0
                s_pb += sk * skp

            C_pb = 0.0
            for a in coprime_residues(b):
                fa = (a / b) - int(a / b)
                sa = (fa - 0.5) if abs(fa) > 1e-15 and abs(fa - 1) > 1e-15 else 0
                fap = (a * p / b) - int(a * p / b)
                sap = (fap - 0.5) if abs(fap) > 1e-15 and abs(fap - 1) > 1e-15 else 0
                C_pb += sa * sap

            sum_abs_s_over_b += abs(s_pb) / b
            sum_s_over_b += s_pb / b
            sum_abs_C_over_b += abs(C_pb) / b
            sum_C_over_b += C_pb / b

            if b > 2 and log(b) > 0:
                ratio = abs(s_pb) / log(b)
                max_ratio_s_logb = max(max_ratio_s_logb, ratio)

            b_track.append(b)
            sum_track.append(sum_abs_s_over_b)

        print(f"  B_max = {B_max}")
        print(f"  Σ |s(p,b)|/b    = {sum_abs_s_over_b:.6f}")
        print(f"  Σ s(p,b)/b      = {sum_s_over_b:.6f}")
        print(f"  Σ |C(p,b)|/b    = {sum_abs_C_over_b:.6f}")
        print(f"  Σ C(p,b)/b      = {sum_C_over_b:.6f}")
        print(f"  max |s(p,b)|/log(b) = {max_ratio_s_logb:.4f}")

        # Compare signed vs absolute: cancellation ratio
        if sum_abs_s_over_b > 0:
            cancel = 1 - abs(sum_s_over_b) / sum_abs_s_over_b
            print(f"  Cancellation in signed sum: {cancel:.4f} (1 = perfect cancellation)")

        # Growth analysis at checkpoints
        log_b_prev = log(2)
        for target_B in [25, 50, 100, 150, 200]:
            if target_B > B_max:
                break
            idx = None
            for i, b in enumerate(b_track):
                if b >= target_B:
                    idx = i
                    break
            if idx is not None:
                logB = log(target_B)
                print(f"  At B={target_B}: Σ|s|/b = {sum_track[idx]:.4f}, (log B)^2 = {logB**2:.4f}, ratio = {sum_track[idx]/logB**2:.4f}")


# ============================================================
# TASK 6: Proof of R(p) > -1/2 via Dedekind bounds
# ============================================================

def proof_sketch_computation(primes, B_max=100):
    """
    The goal: prove R(p) > -1/2 for all primes p.

    R(p) = Σ_b C(p,b) / Σ_b Σ_{a cop b} ((a/b))^2

    Since C(p,b) = s(p,b) - NC(p,b), and NC is the non-coprime part,
    we need:

    Σ_b [s(p,b) - NC(p,b)] > -1/2 * Σ_b Σ_{a cop b} ((a/b))^2

    Known facts:
    - Σ_{a cop b} ((a/b))^2 = (b/12)(1 - 1/b) * Π_{q|b}(1 - 1/q^2) [for squarefree b]
      Actually: Σ_{a cop b} ((a/b))^2 = φ(b)/(12) * (1 + correction terms)
    - Dedekind reciprocity gives s(p,b) in terms of s(b,p) + explicit
    """
    print("\n" + "=" * 70)
    print("TASK 6: PROOF SKETCH VERIFICATION")
    print("=" * 70)

    for p in primes:
        print(f"\n--- Prime p = {p} ---")

        # Compute exact quantities
        sum_C = Fraction(0)
        sum_delta_sq = Fraction(0)
        sum_s = Fraction(0)
        sum_NC = Fraction(0)

        for b in range(2, B_max + 1):
            if gcd(p, b) > 1:
                continue

            C = compute_C_exact(p, b)
            s = compute_dedekind_s_exact(p, b)
            NC = s - C  # non-coprime contribution

            sum_C += C
            sum_s += s
            sum_NC += NC

            for a in coprime_residues(b):
                saw = sawtooth_exact(Fraction(a, b))
                sum_delta_sq += saw * saw

        R = sum_C / sum_delta_sq if sum_delta_sq != 0 else Fraction(0)
        R_s = sum_s / sum_delta_sq if sum_delta_sq != 0 else Fraction(0)
        R_nc = sum_NC / sum_delta_sq if sum_delta_sq != 0 else Fraction(0)

        print(f"  Σ C(p,b)    = {sum_C} = {float(sum_C):.8f}")
        print(f"  Σ s(p,b)    = {sum_s} = {float(sum_s):.8f}")
        print(f"  Σ NC(p,b)   = {sum_NC} = {float(sum_NC):.8f}")
        print(f"  Σ δ²        = {float(sum_delta_sq):.8f}")
        print(f"  R = Σ C/Σ δ²          = {float(R):.8f}")
        print(f"  R_s = Σ s/Σ δ²        = {float(R_s):.8f}")
        print(f"  R_nc = Σ NC/Σ δ²      = {float(R_nc):.8f}")
        print(f"  Check: R = R_s - R_nc  = {float(R_s - R_nc):.8f}")
        print(f"  R > -1/2?  {float(R) > -0.5}  (R = {float(R):.8f})")

        # Decompose via reciprocity:
        # s(p,b) = RHS(p,b) - s(b,p)
        # where RHS(p,b) = (p/b + b/p + 1/(pb))/12 - 1/4
        sum_rhs_reciprocity = Fraction(0)
        sum_s_bp = Fraction(0)

        for b in range(2, B_max + 1):
            if gcd(p, b) > 1:
                continue
            rhs = (Fraction(p, b) + Fraction(b, p) + Fraction(1, p * b)) / 12 - Fraction(1, 4)
            s_bp = compute_dedekind_s_exact(b, p)
            sum_rhs_reciprocity += rhs
            sum_s_bp += s_bp

        print(f"\n  Via reciprocity:")
        print(f"  Σ RHS(p,b) = {float(sum_rhs_reciprocity):.8f}")
        print(f"  Σ s(b,p)   = {float(sum_s_bp):.8f}")
        print(f"  Check: Σ s(p,b) = Σ RHS - Σ s(b,p) = {float(sum_rhs_reciprocity - sum_s_bp):.8f}")
        print(f"  (should match {float(sum_s):.8f})")

        # The key: Σ RHS(p,b) is EXPLICIT and grows like (p/12)*H_B + ...
        # H_B = Σ 1/b ~ log B
        # The p/(12b) term: Σ p/(12b) = (p/12)*H_B ~ (p/12)*log B
        # The b/(12p) term: Σ b/(12p) ~ B^2/(24p) [dominates!]
        # The 1/(12pb) term: Σ 1/(12pb) ~ log(B)/(12p)
        # The -1/4 term: Σ -1/4 = -B_count/4
        B_count = sum(1 for b in range(2, B_max+1) if gcd(p,b)==1)
        H_B = sum(Fraction(1, b) for b in range(2, B_max+1) if gcd(p,b)==1)
        sum_b_over_p = sum(Fraction(b, p) for b in range(2, B_max+1) if gcd(p,b)==1)

        print(f"\n  Explicit terms in Σ RHS:")
        print(f"  Σ p/(12b) = p/12 * H_B = {float(Fraction(p,12) * H_B):.4f}")
        print(f"  Σ b/(12p) = {float(sum_b_over_p/12):.4f}")
        print(f"  Σ 1/(12pb) = {float(sum(Fraction(1, 12*p*b) for b in range(2,B_max+1) if gcd(p,b)==1)):.4f}")
        print(f"  -B_count/4 = {-B_count/4:.4f}")


# ============================================================
# MAIN
# ============================================================

def main():
    primes = [13, 31, 97, 199]

    print("DEDEKIND SUM PROOF PATH FOR R(p) > -1/2")
    print("Exact arithmetic computation")
    print("=" * 70)

    # Task 1: Verify exact relationship (small B for exact arithmetic speed)
    verify_relationship(primes, B_max=30)

    # Task 3: Dedekind reciprocity
    verify_reciprocity(primes[:3], B_max=40)

    # Task 4: R(p) via Dedekind sums
    compute_R_via_dedekind(primes[:3], B_max=50)

    # Task 5: Summed bounds (float for speed)
    analyze_summed_bounds(primes, B_max=300)

    # Task 6: Proof sketch computation
    proof_sketch_computation(primes[:3], B_max=60)


if __name__ == '__main__':
    import time
    t0 = time.time()
    main()
    print(f"\nTotal time: {time.time()-t0:.1f}s")
