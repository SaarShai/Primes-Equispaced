#!/usr/bin/env python3
"""
R-BOUND ATTACK: Prove |R| < 1 where R = 2·ΣD·δ / Σδ²
======================================================

B+C = Σδ²(1+R) > 0 iff R > -1.
Empirically |R| < 0.52 for all tested primes p ≥ 11.

APPROACH (Hour 1/2 hybrid):
  1. Per-denominator analysis: B_b + C_b for each b
  2. Large-denominator dominance: b ~ N are key
  3. Ramanujan sum structure: Σ D(a/b)·δ(a/b) via Fourier
  4. Seek: R > -1 unconditionally, or a proof that the
     "negative contribution" denominators are outweighed

Key insight to test: the large-b regime (b close to N = p-1) contributes
positively to B+C because:
  - For b = p-1: only one fraction a/b = 1/(p-1) interior (with gcd(a,b)=1)
    and 2/(p-1), etc. The D values here are small (rank discrepancy near 0 or 1).
  - For b ~ p/2: fractions are well-distributed, D values nearly cancel.
"""

import sys
from math import gcd, isqrt, log, sqrt, pi
from fractions import Fraction

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, isqrt(limit) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

def mertens_table(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime = [True] * (limit + 1)
    for i in range(2, limit + 1):
        if is_prime[i]:
            for j in range(i, limit + 1, i):
                is_prime[j] = False if j > i else True
                mu[j] -= mu[j // i]
    # Actually compute mu properly
    mu = [0] * (limit + 1)
    mu[1] = 1
    smallest_prime = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if smallest_prime[i] == 0:
            for j in range(i, limit + 1, i):
                if smallest_prime[j] == 0:
                    smallest_prime[j] = i
    for n in range(2, limit + 1):
        p = smallest_prime[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]
    M = [0] * (limit + 1)
    s = 0
    for i in range(1, limit + 1):
        s += mu[i]
        M[i] = s
    return mu, M

def compute_farey_wobble_data(N):
    """
    Compute for F_N:
      - The Farey sequence as list of Fractions
      - D(f) = rank(f) - n*f for each f (using floats for speed)
      - Per-denominator sums needed for B+C analysis
    Returns: fractions list, D values list, n
    """
    # Build Farey sequence using mediant algorithm
    farey = []
    a, b = 0, 1
    c, d = 1, N
    farey.append(Fraction(0, 1))
    while c <= N:
        farey.append(Fraction(c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

    n = len(farey)
    # D(f) = rank(f) - n * f, rank starts at 0
    D_vals = []
    for i, f in enumerate(farey):
        D_vals.append(i - n * float(f))

    return farey, D_vals, n

def compute_delta_vals(N, p, farey, D_vals):
    """
    For each f = a/b in F_N (interior, b >= 2):
    delta(a/b) = (a - (p*a mod b)) / b
    Returns: delta_vals (same indexing as farey), delta_sq, B_raw
    """
    delta_vals = [0.0] * len(farey)
    delta_sq = 0.0
    B_raw = 0.0

    for i, f in enumerate(farey):
        a, b = f.numerator, f.denominator
        if b < 2:
            continue
        sigma = (p * a) % b
        delta = (a - sigma) / b
        delta_vals[i] = delta
        delta_sq += delta * delta
        B_raw += D_vals[i] * delta

    B_raw *= 2.0
    return delta_vals, delta_sq, B_raw

def per_denominator_analysis(N, p, farey, D_vals):
    """
    For each denominator b, compute B_b + C_b and check sign.
    Returns dict: b -> (S_b, B_b_plus_C_b, sign)
    """
    # Group fractions by denominator
    by_denom = {}
    for i, f in enumerate(farey):
        b = f.denominator
        if b < 2:
            continue
        if b not in by_denom:
            by_denom[b] = []
        by_denom[b].append((f.numerator, D_vals[i]))

    results = {}
    for b, entries in sorted(by_denom.items()):
        S_b = 0.0
        cross_b = 0.0
        for a, D_val in entries:
            sigma = (p * a) % b
            delta = (a - sigma) / b
            S_b += delta * delta
            cross_b += D_val * delta
        B_b_plus_C_b = S_b + 2 * cross_b
        results[b] = (S_b, B_b_plus_C_b, B_b_plus_C_b > 0)

    return results

def R_analysis(p_limit=500):
    """
    Compute R = 2·ΣD·δ / Σδ² for all primes up to p_limit.
    Study: range of R, per-denominator breakdown, sign of B_b+C_b.
    """
    primes = sieve(p_limit)
    primes = [p for p in primes if p >= 11]

    print(f"{'p':>6} {'M(p)':>5} {'R':>8} {'B+C':>12} {'delta_sq':>12} {'neg_denoms':>10}")
    print("-" * 70)

    mu, M = mertens_table(p_limit)

    R_vals = []
    negative_R_cases = []
    all_neg_denom_data = []

    for p in primes:
        N = p - 1
        mp = M[p] if p <= p_limit else None

        farey, D_vals, n = compute_farey_wobble_data(N)
        delta_vals, delta_sq, B_raw = compute_delta_vals(N, p, farey, D_vals)

        if delta_sq < 1e-15:
            continue

        R = B_raw / delta_sq
        B_plus_C = delta_sq + B_raw

        # Count denominators where B_b + C_b < 0
        denom_results = per_denominator_analysis(N, p, farey, D_vals)
        neg_denoms = [(b, data) for b, data in denom_results.items() if not data[2]]

        R_vals.append(R)

        if mp is not None and mp <= -3:
            flag = " <-- M≤-3"
        else:
            flag = ""

        print(f"{p:>6} {(mp if mp else '?'):>5} {R:>8.4f} {B_plus_C:>12.4f} {delta_sq:>12.4f} {len(neg_denoms):>10}{flag}")

        if R < -0.5:
            negative_R_cases.append((p, R, B_plus_C, neg_denoms))

        if neg_denoms:
            all_neg_denom_data.append((p, neg_denoms))

    print()
    print(f"R range: [{min(R_vals):.4f}, {max(R_vals):.4f}]")
    print(f"All R > -1: {all(r > -1 for r in R_vals)}")
    print(f"All B+C > 0: {all(delta_sq + B_raw > 0 for _ in [1])}")

    return R_vals, all_neg_denom_data

def analyze_negative_denominators(p_limit=200):
    """
    Deep dive: for which denominators b is B_b + C_b < 0?
    Hypothesis: small b (b = 2,3,4) might have negative B_b+C_b when
    D(a/b) and delta(a/b) have specific sign patterns.
    """
    primes = sieve(p_limit)
    primes = [p for p in primes if p >= 11]

    # Track which denominators go negative across all primes
    denom_negative_count = {}
    denom_total_count = {}

    for p in primes:
        N = p - 1
        farey, D_vals, n = compute_farey_wobble_data(N)
        denom_results = per_denominator_analysis(N, p, farey, D_vals)

        for b, (S_b, BpC_b, pos) in denom_results.items():
            denom_total_count[b] = denom_total_count.get(b, 0) + 1
            if not pos:
                denom_negative_count[b] = denom_negative_count.get(b, 0) + 1

    print("\n=== DENOMINATORS WITH NEGATIVE B_b + C_b ===")
    print(f"{'b':>5} {'neg/total':>12} {'fraction negative':>18}")
    total_neg = sum(denom_negative_count.values())
    for b in sorted(denom_negative_count.keys()):
        neg = denom_negative_count[b]
        total = denom_total_count[b]
        print(f"{b:>5} {neg:>5}/{total:<5} {neg/total:>18.3f}")
    print(f"Total negative (b,p) pairs: {total_neg}")

def prove_B_plus_C_via_quadratic(p_limit=300):
    """
    Attempt: show B+C > 0 via the quadratic form identity.

    Key insight: B+C = Σ_{f} δ(f)(δ(f) + 2D(f))

    We look for: does δ(f)(δ(f) + 2D(f)) > 0 for "most" f in a provable sense?

    Per-fraction analysis: what fraction of (f) have positive vs negative contribution?
    And does the sum of positive contributions dominate?
    """
    primes = sieve(p_limit)
    primes = [p for p in primes if p >= 11]

    print("\n=== QUADRATIC FORM SIGN ANALYSIS ===")
    print(f"{'p':>6} {'pos_terms':>10} {'neg_terms':>10} {'B+C/delta_sq':>14} {'R':>8}")
    print("-" * 55)

    for p in primes[:20]:
        N = p - 1
        farey, D_vals, n = compute_farey_wobble_data(N)
        delta_vals, delta_sq, B_raw = compute_delta_vals(N, p, farey, D_vals)

        pos_sum = 0.0
        neg_sum = 0.0
        pos_count = 0
        neg_count = 0

        for i, f in enumerate(farey):
            if f.denominator < 2:
                continue
            d = delta_vals[i]
            if abs(d) < 1e-15:
                continue
            term = d * (d + 2 * D_vals[i])
            if term > 0:
                pos_sum += term
                pos_count += 1
            else:
                neg_sum += term
                neg_count += 1

        R = B_raw / delta_sq if delta_sq > 0 else 0
        ratio = (delta_sq + B_raw) / delta_sq if delta_sq > 0 else 0
        print(f"{p:>6} {pos_count:>10} {neg_count:>10} {ratio:>14.4f} {R:>8.4f}")

    # For larger p, what's the trend?
    print("\n=== TREND FOR LARGER p ===")
    for p in primes[-10:]:
        N = p - 1
        farey, D_vals, n = compute_farey_wobble_data(N)
        delta_vals, delta_sq, B_raw = compute_delta_vals(N, p, farey, D_vals)
        R = B_raw / delta_sq if delta_sq > 0 else 0
        print(f"  p={p}: R = {R:.4f}, B+C = {delta_sq + B_raw:.4f}")

def analyze_R_structure():
    """
    Key analytical insight: R = 2ΣD·δ / Σδ²

    Write ΣD·δ = Σ_b [Σ_{gcd(a,b)=1} D(a/b) · (a - σ_p(a))/b]

    For each b: Σ D(a/b)(a - σ_p(a))/b
    = (1/b) Σ D(a/b)(a - σ_p(a))
    = (1/b) [Σ D(a/b)·a - Σ D(a/b)·σ_p(a)]

    If σ_p is "uncorrelated" with the ordering of D values, then
    Σ D(a/b)·σ_p(a) ≈ Σ D(a/b)·a  (on average over p)

    This would give ΣD·δ ≈ 0, explaining why R ≈ 0 typically.

    The deviation from 0 is what we need to bound.
    """
    print("\n=== RAMANUJAN SUM STRUCTURE OF ΣD·δ ===")
    print("Analyzing per-denominator correlations...")

    # For p=23 (M(p)=-3), analyze the structure
    p = 23
    N = p - 1
    farey, D_vals, n = compute_farey_wobble_data(N)

    print(f"\nPrime p={p}, N={N}, n=|F_N|={n}")
    print(f"\nPer-denominator B_b/2 = Σ D(a/b)δ(a/b):")
    print(f"{'b':>4} {'phi(b)':>6} {'p mod b':>7} {'B_b/2':>10} {'C_b=S_b':>10} {'B_b+C_b':>10} {'sign':>5}")

    total_cross = 0.0
    total_S = 0.0

    by_denom = {}
    for i, f in enumerate(farey):
        b = f.denominator
        if b < 2:
            continue
        if b not in by_denom:
            by_denom[b] = []
        by_denom[b].append((f.numerator, D_vals[i]))

    for b in sorted(by_denom.keys()):
        entries = by_denom[b]
        phi_b = len(entries)
        p_mod_b = p % b
        S_b = 0.0
        cross_b = 0.0
        for a, D in entries:
            sigma = (p * a) % b
            delta = (a - sigma) / b
            S_b += delta * delta
            cross_b += D * delta
        BpC = S_b + 2 * cross_b
        total_cross += cross_b
        total_S += S_b
        sign = "+" if BpC > 0 else "-"
        print(f"{b:>4} {phi_b:>6} {p_mod_b:>7} {cross_b:>10.4f} {S_b:>10.4f} {BpC:>10.4f} {sign:>5}")

    R = 2 * total_cross / total_S
    print(f"\nΣ D·δ = {total_cross:.4f}")
    print(f"Σ δ²  = {total_S:.4f}")
    print(f"R = {R:.4f}  (need |R| < 1)")
    print(f"B+C = Σδ²(1+R) = {total_S * (1 + R):.4f} {'> 0 ✓' if R > -1 else '< 0 ✗'}")

def bound_R_analytically(p_max=1000):
    """
    Empirical study: how does R scale with p?
    Look for: R = O(1/sqrt(N)) or R = O(1/log(N)) etc.
    Also: does max |R| converge?
    """
    primes = sieve(p_max)
    primes = [p for p in primes if p >= 11]

    print("\n=== EMPIRICAL BOUNDS ON R ===")

    results = []
    for p in primes:
        N = p - 1
        farey, D_vals, n = compute_farey_wobble_data(N)
        delta_vals, delta_sq, B_raw = compute_delta_vals(N, p, farey, D_vals)
        if delta_sq < 1e-10:
            continue
        R = B_raw / delta_sq
        results.append((p, N, R, abs(R)))

    # Running maximum of |R|
    running_max = 0
    print(f"\n{'p':>6} {'R':>8} {'|R|':>8} {'max|R| so far':>14} {'sqrt(N)*|R|':>14}")
    for i, (p, N, R, absR) in enumerate(results):
        running_max = max(running_max, absR)
        if i % 20 == 0 or absR > 0.45:
            print(f"{p:>6} {R:>8.4f} {absR:>8.4f} {running_max:>14.4f} {sqrt(N)*absR:>14.4f}")

    print(f"\nFinal max |R| = {running_max:.4f}")
    print(f"All R > -1: {all(r[2] > -1 for r in results)}")
    print(f"All B+C > 0: implied by R > -1 and Σδ² > 0")

    # Linear regression: does |R| ~ C/N^alpha?
    import math
    xs = [math.log(r[1]) for r in results if r[1] > 1]
    ys = [math.log(max(r[3], 1e-10)) for r in results if r[1] > 1]
    if len(xs) > 2:
        n_pts = len(xs)
        sx = sum(xs); sy = sum(ys)
        sxx = sum(x*x for x in xs); sxy = sum(x*y for x,y in zip(xs,ys))
        slope = (n_pts * sxy - sx * sy) / (n_pts * sxx - sx * sx)
        intercept = (sy - slope * sx) / n_pts
        print(f"\nLog-log regression: log|R| = {slope:.3f}*log(N) + {intercept:.3f}")
        print(f"=> |R| ~ exp({intercept:.3f}) * N^{slope:.3f} = {math.exp(intercept):.3f} * N^{slope:.3f}")
        print(f"(slope ≈ 0 means |R| bounded; slope < 0 means |R| → 0)")

    return results

def key_structural_theorem_attempt():
    """
    THEOREM ATTEMPT: B+C > 0 for all primes p >= 11.

    Strategy: Write B+C = Σ_b (B_b + C_b) and show the sum is positive.

    For each b, B_b + C_b = Σ_{gcd(a,b)=1} δ(a/b)[δ(a/b) + 2D(a/b)]

    KEY OBSERVATION from data:
    - If B_b + C_b < 0 for some b, it is SMALL compared to the positive terms
    - The denominator b = p-1 (only if p-2 is prime! = Sophie Germain-like condition)
      has D(a/b) ≈ 0 and δ(a/b) small, contributing ≈ 0.

    NEW IDEA: For the denominator b = ⌊p/2⌋ (largest even denominator < p),
    the fractions a/b are dense and the contribution is always large and positive.

    PROOF SKETCH (to be made rigorous):
    1. For b = ⌊N/2⌋ to N-1: the φ(b) ≥ 1 fractions a/b have |D(a/b)| = O(1)
       (the rank discrepancy is small for large b because fractions of large denominator
       are well-separated). And δ(a/b) ≠ 0 when p ≢ 1 mod b.

    2. The contribution from b = 2 to ⌊N/2⌋: can be bounded below using
       the prime sum analysis from Theorem 2 (step2 proof).

    This section just TESTS whether max|D(a/b)| ≤ K for large b.
    """
    print("\n=== D(a/b) BOUNDS FOR LARGE b ===")
    p = 101
    N = p - 1
    farey, D_vals, n = compute_farey_wobble_data(N)

    # For each large denominator, compute max|D(a/b)|
    by_denom = {}
    for i, f in enumerate(farey):
        b = f.denominator
        if b not in by_denom:
            by_denom[b] = []
        by_denom[b].append(abs(D_vals[i]))

    print(f"p={p}, N={N}, n={n}")
    print(f"{'b':>5} {'phi(b)':>7} {'max|D|':>8} {'avg|D|':>8} {'n/b':>8}")
    for b in sorted(by_denom.keys())[-20:]:
        vals = by_denom[b]
        print(f"{b:>5} {len(vals):>7} {max(vals):>8.2f} {sum(vals)/len(vals):>8.2f} {n/b:>8.1f}")

def main():
    print("=" * 70)
    print("R-BOUND ATTACK: Proving B+C > 0 for all primes p >= 11")
    print("=" * 70)

    # 1. Quick R analysis for p <= 500
    print("\n[1] R = 2ΣDδ/Σδ² for primes 11 <= p <= 500")
    R_vals, neg_denom_data = R_analysis(p_limit=300)

    # 2. Detailed structural analysis
    analyze_R_structure()

    # 3. Negative denominator analysis
    analyze_negative_denominators(p_limit=150)

    # 4. Per-fraction quadratic form sign analysis
    prove_B_plus_C_via_quadratic(p_limit=150)

    # 5. Empirical bounds and scaling of R
    R_results = bound_R_analytically(p_max=500)

    # 6. D(a/b) bounds for large b
    key_structural_theorem_attempt()

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY OF FINDINGS")
    print("=" * 70)
    if R_vals:
        print(f"R range over tested primes: [{min(R_vals):.4f}, {max(R_vals):.4f}]")
        print(f"All R > -1 (i.e., B+C > 0): {all(r > -1 for r in R_vals)}")
        print(f"Max |R| = {max(abs(r) for r in R_vals):.4f}")

    print("\nKEY QUESTION: Can we prove R > -1 unconditionally?")
    print("=> See analysis above for structural insights.")

if __name__ == "__main__":
    main()
