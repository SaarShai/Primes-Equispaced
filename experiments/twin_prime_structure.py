#!/usr/bin/env python3
"""
TWIN PRIME JOINT INJECTION STRUCTURE
=====================================

We already know the sign correlation between twin primes is NOT special --
it's just Mertens smoothness (gap-50 primes still agree 94.46%).

QUESTION: Is there STRUCTURAL geometry in the joint Farey injection that
IS twin-specific?

Tests:
1. Gap overlap: Do p and p+2 fill the SAME or DIFFERENT Farey gaps?
2. φ(p+1) asymmetry: p+1 is composite, so F_{p+1} adds far fewer fractions
   than F_p did. Quantify this.
3. Modular inverse correlation: k^{-1} mod p vs k^{-1} mod (p+2)
4. Gap-filling complementarity: Compare twin vs random prime pairs
5. Joint gap distribution: How do the gap sizes change across p -> p+1 -> p+2?
"""

from fractions import Fraction
from math import gcd, floor, sqrt
from collections import Counter
import random

# ============================================================
# CORE FAREY TOOLS
# ============================================================

def farey_sequence(N):
    """Return F_N as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def euler_phi(n):
    """Euler's totient function."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def new_fractions_at(n):
    """Return the set of NEW fractions added when going from F_{n-1} to F_n.
    These are k/n with gcd(k,n) = 1, 0 < k < n."""
    return {Fraction(k, n) for k in range(1, n) if gcd(k, n) == 1}


def find_gap_index(sorted_seq, frac):
    """Find which gap in sorted_seq the fraction falls into.
    Returns (left_idx, right_idx) where frac sits between seq[left] and seq[right]."""
    lo, hi = 0, len(sorted_seq) - 1
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if sorted_seq[mid] < frac:
            lo = mid
        else:
            hi = mid
    return (lo, hi)


def gap_sizes(sorted_seq):
    """Return list of gap sizes between consecutive elements."""
    return [sorted_seq[i+1] - sorted_seq[i] for i in range(len(sorted_seq) - 1)]


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def primes_up_to(N):
    """Sieve of Eratosthenes."""
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N + 1, i):
                sieve[j] = False
    return [i for i in range(2, N + 1) if sieve[i]]


def twin_primes_up_to(N):
    """Return list of (p, p+2) twin prime pairs."""
    ps = primes_up_to(N)
    ps_set = set(ps)
    return [(p, p + 2) for p in ps if p + 2 in ps_set and p >= 5]


# ============================================================
# TEST 1: GAP OVERLAP
# For twin primes (p, p+2), compute which gaps of F_{p-1} are
# filled by the injections at p and at p+2.
# Do they fill the SAME gaps or DIFFERENT gaps?
# ============================================================

def test_gap_overlap(limit=200):
    """For each twin prime pair (p, p+2), check overlap of gap-filling."""
    print("=" * 70)
    print("TEST 1: GAP OVERLAP — Do p and p+2 fill the same or different gaps?")
    print("=" * 70)

    twins = twin_primes_up_to(limit)
    all_primes = primes_up_to(limit)
    prime_set = set(all_primes)

    results = []

    for p, q in twins:
        if p > limit:
            break

        F_base = farey_sequence(p - 1)
        n_base = len(F_base)

        # New fractions from p: k/p with gcd(k,p)=1, which is all 1..p-1 since p prime
        new_p = sorted([Fraction(k, p) for k in range(1, p)])

        # New fractions from p+2: k/(p+2) with gcd(k,p+2)=1
        new_q = sorted([Fraction(k, q) for k in range(1, q) if gcd(k, q) == 1])

        # For each new fraction, find which gap of F_{p-1} it falls into
        gaps_filled_by_p = set()
        for f in new_p:
            idx = find_gap_index(F_base, f)
            gaps_filled_by_p.add(idx)

        gaps_filled_by_q = set()
        for f in new_q:
            idx = find_gap_index(F_base, f)
            gaps_filled_by_q.add(idx)

        overlap = gaps_filled_by_p & gaps_filled_by_q
        only_p = gaps_filled_by_p - gaps_filled_by_q
        only_q = gaps_filled_by_q - gaps_filled_by_p

        overlap_rate = len(overlap) / len(gaps_filled_by_p | gaps_filled_by_q) if gaps_filled_by_p | gaps_filled_by_q else 0

        results.append({
            'p': p, 'q': q,
            'gaps_p': len(gaps_filled_by_p),
            'gaps_q': len(gaps_filled_by_q),
            'overlap': len(overlap),
            'only_p': len(only_p),
            'only_q': len(only_q),
            'overlap_rate': overlap_rate,
            'phi_p': p - 1,  # φ(p) = p-1 since p prime
            'phi_q': euler_phi(q),  # φ(p+2) = p+1 since p+2 prime
            'phi_p1': euler_phi(p + 1),  # φ(p+1) — composite
        })

    print(f"\n{'p':>5} {'q':>5} | {'#gaps_p':>7} {'#gaps_q':>7} | {'overlap':>7} {'only_p':>6} {'only_q':>6} | {'ovlp_rate':>9} | {'φ(p+1)':>6} {'(p+1)/φ':>7}")
    print("-" * 90)
    for r in results:
        ratio = (r['p'] + 1) / r['phi_p1'] if r['phi_p1'] > 0 else 0
        print(f"{r['p']:5d} {r['q']:5d} | {r['gaps_p']:7d} {r['gaps_q']:7d} | {r['overlap']:7d} {r['only_p']:6d} {r['only_q']:6d} | {r['overlap_rate']:9.4f} | {r['phi_p1']:6d} {ratio:7.2f}")

    avg_overlap = sum(r['overlap_rate'] for r in results) / len(results) if results else 0
    print(f"\nAverage gap overlap rate: {avg_overlap:.4f}")

    return results


# ============================================================
# TEST 2: COMPARE TWIN VS NON-TWIN PRIME PAIRS
# Is the gap overlap rate for twins different from random prime pairs
# with the same gap?
# ============================================================

def test_twin_vs_random(limit=150):
    """Compare gap overlap for twin primes vs non-twin consecutive primes."""
    print("\n" + "=" * 70)
    print("TEST 2: TWIN vs NON-TWIN gap overlap comparison")
    print("=" * 70)

    all_primes = primes_up_to(limit)
    prime_set = set(all_primes)

    def compute_overlap_rate(p, q):
        """Compute gap overlap between injections at p and q, relative to F_{p-1}."""
        F_base = farey_sequence(p - 1)

        new_p = sorted([Fraction(k, p) for k in range(1, p) if gcd(k, p) == 1])
        new_q = sorted([Fraction(k, q) for k in range(1, q) if gcd(k, q) == 1])

        gaps_p = set()
        for f in new_p:
            gaps_p.add(find_gap_index(F_base, f))
        gaps_q = set()
        for f in new_q:
            gaps_q.add(find_gap_index(F_base, f))

        union = gaps_p | gaps_q
        if not union:
            return 0
        return len(gaps_p & gaps_q) / len(union)

    # Twin pairs
    twins = [(p, p+2) for p in all_primes if p + 2 in prime_set and p >= 5]
    twin_overlaps = []
    for p, q in twins:
        if p <= limit - 2:
            twin_overlaps.append(compute_overlap_rate(p, q))

    # Gap-4 pairs (cousin primes)
    cousins = [(p, p+4) for p in all_primes if p + 4 in prime_set and p >= 5]
    cousin_overlaps = []
    for p, q in cousins:
        if p <= limit - 4:
            cousin_overlaps.append(compute_overlap_rate(p, q))

    # Gap-6 pairs (sexy primes)
    sexys = [(p, p+6) for p in all_primes if p + 6 in prime_set and p >= 5]
    sexy_overlaps = []
    for p, q in sexys:
        if p <= limit - 6:
            sexy_overlaps.append(compute_overlap_rate(p, q))

    # Consecutive primes (various gaps)
    consec_overlaps = []
    for i in range(len(all_primes) - 1):
        p = all_primes[i]
        q = all_primes[i + 1]
        if p >= 5 and q <= limit and q - p > 2:  # exclude twins
            consec_overlaps.append(compute_overlap_rate(p, q))

    print(f"\nTwin primes (gap=2):      n={len(twin_overlaps):3d}, avg overlap = {sum(twin_overlaps)/len(twin_overlaps):.4f}" if twin_overlaps else "")
    print(f"Cousin primes (gap=4):    n={len(cousin_overlaps):3d}, avg overlap = {sum(cousin_overlaps)/len(cousin_overlaps):.4f}" if cousin_overlaps else "")
    print(f"Sexy primes (gap=6):      n={len(sexy_overlaps):3d}, avg overlap = {sum(sexy_overlaps)/len(sexy_overlaps):.4f}" if sexy_overlaps else "")
    print(f"Consec. non-twin (gap>2): n={len(consec_overlaps):3d}, avg overlap = {sum(consec_overlaps)/len(consec_overlaps):.4f}" if consec_overlaps else "")

    return twin_overlaps, cousin_overlaps, sexy_overlaps, consec_overlaps


# ============================================================
# TEST 3: MODULAR INVERSE CORRELATION
# For twin primes p, p+2: is there a relationship between
# k^{-1} mod p and k^{-1} mod (p+2)?
# ============================================================

def test_modular_inverse_correlation(limit=500):
    """Check if modular inverses mod p and mod p+2 are correlated for twin primes."""
    print("\n" + "=" * 70)
    print("TEST 3: MODULAR INVERSE CORRELATION k^{-1} mod p vs k^{-1} mod (p+2)")
    print("=" * 70)

    twins = twin_primes_up_to(limit)

    for p, q in twins[:15]:  # Show details for first 15
        # k/p's left Farey neighbor has denominator related to k^{-1} mod p
        # Specifically: for k/p in F_p, the left neighbor a/b satisfies bp - ak = 1
        # so b ≡ k^{-1} (mod p) ... but only among b < p

        # Common values 1..min(p,q)-1 coprime to both
        common_k = [k for k in range(1, p) if gcd(k, p) == 1 and gcd(k, q) == 1]

        inv_mod_p = []
        inv_mod_q = []
        for k in common_k:
            inv_p = pow(k, -1, p)
            inv_q = pow(k, -1, q)
            inv_mod_p.append(inv_p)
            inv_mod_q.append(inv_q)

        # Normalize to [0,1] for comparison
        norm_p = [x / p for x in inv_mod_p]
        norm_q = [x / q for x in inv_mod_q]

        # Correlation
        if len(norm_p) > 2:
            import numpy as np
            corr = np.corrcoef(norm_p, norm_q)[0, 1]
        else:
            corr = float('nan')

        # Also check: k^{-1} mod (p+2) vs k^{-1} mod p
        # Algebraically: if kx ≡ 1 (mod p), then k*x ≡ 1 + k*x - 1 (mod p+2)
        # kx = 1 + mp for some integer m, so kx mod (p+2) = (1 + mp) mod (p+2)
        # = 1 + mp - floor((1+mp)/(p+2))*(p+2)
        # This doesn't simplify nicely in general.

        print(f"  p={p:4d}, q={q:4d}: {len(common_k):3d} common k values, "
              f"corr(k^{{-1}} mod p, k^{{-1}} mod q) = {corr:+.4f}")

    # Aggregate correlation across all twin pairs
    print("\n--- Aggregate across all twin pairs ---")
    all_corrs_twin = []
    all_corrs_random = []

    all_primes = primes_up_to(limit)
    prime_set = set(all_primes)

    for p, q in twins:
        common_k = [k for k in range(1, p) if gcd(k, p) == 1 and gcd(k, q) == 1]
        if len(common_k) < 5:
            continue
        inv_p = [pow(k, -1, p) / p for k in common_k]
        inv_q = [pow(k, -1, q) / q for k in common_k]
        import numpy as np
        corr = np.corrcoef(inv_p, inv_q)[0, 1]
        all_corrs_twin.append(corr)

    # Compare with non-twin prime pairs of similar size
    non_twins = []
    for i in range(len(all_primes) - 1):
        p = all_primes[i]
        q = all_primes[i + 1]
        if q - p > 2 and p >= 5:
            non_twins.append((p, q))

    for p, q in non_twins[:len(twins)]:
        common_k = [k for k in range(1, p) if gcd(k, p) == 1 and gcd(k, q) == 1]
        if len(common_k) < 5:
            continue
        inv_p = [pow(k, -1, p) / p for k in common_k]
        inv_q = [pow(k, -1, q) / q for k in common_k]
        import numpy as np
        corr = np.corrcoef(inv_p, inv_q)[0, 1]
        all_corrs_random.append(corr)

    import numpy as np
    if all_corrs_twin:
        print(f"  Twin pairs:     mean corr = {np.mean(all_corrs_twin):+.4f}, "
              f"std = {np.std(all_corrs_twin):.4f}, n = {len(all_corrs_twin)}")
    if all_corrs_random:
        print(f"  Non-twin pairs: mean corr = {np.mean(all_corrs_random):+.4f}, "
              f"std = {np.std(all_corrs_random):.4f}, n = {len(all_corrs_random)}")


# ============================================================
# TEST 4: φ(p+1) STRUCTURE
# For twin primes p, p+2: p+1 is always even.
# How does φ(p+1) compare for twin vs non-twin?
# What fraction of gaps does p+1 fill?
# ============================================================

def test_phi_p_plus_1(limit=1000):
    """Analyze φ(p+1) for twin primes vs all primes."""
    print("\n" + "=" * 70)
    print("TEST 4: φ(p+1) STRUCTURE — twin primes vs all primes")
    print("=" * 70)

    all_primes = primes_up_to(limit)
    prime_set = set(all_primes)
    twins = [(p, p+2) for p in all_primes if p + 2 in prime_set and p >= 5]

    # For twin primes: p+1 is always even, and often p+1 = 2*prime
    twin_ratios = []
    twin_phi_fracs = []
    twin_p1_factorizations = Counter()

    for p, q in twins:
        phi_p1 = euler_phi(p + 1)
        ratio = phi_p1 / (p + 1)
        twin_ratios.append(ratio)
        twin_phi_fracs.append(phi_p1)

        # Factor p+1
        n = p + 1
        factors = []
        temp = n
        d = 2
        while d * d <= temp:
            while temp % d == 0:
                factors.append(d)
                temp //= d
            d += 1
        if temp > 1:
            factors.append(temp)
        key = tuple(sorted(Counter(factors).items()))
        # Simplify: just count number of distinct prime factors
        twin_p1_factorizations[len(set(factors))] += 1

    # For all primes (non-twin): p+1
    all_ratios = []
    for p in all_primes:
        if p >= 5 and p + 2 not in prime_set:
            phi_p1 = euler_phi(p + 1)
            ratio = phi_p1 / (p + 1)
            all_ratios.append(ratio)

    import numpy as np
    print(f"\n  Twin primes (n={len(twin_ratios)}):")
    print(f"    Mean φ(p+1)/(p+1) = {np.mean(twin_ratios):.4f}")
    print(f"    Std               = {np.std(twin_ratios):.4f}")
    print(f"    Min               = {np.min(twin_ratios):.4f}")
    print(f"    Max               = {np.max(twin_ratios):.4f}")

    print(f"\n  Non-twin primes (n={len(all_ratios)}):")
    print(f"    Mean φ(p+1)/(p+1) = {np.mean(all_ratios):.4f}")
    print(f"    Std               = {np.std(all_ratios):.4f}")
    print(f"    Min               = {np.min(all_ratios):.4f}")
    print(f"    Max               = {np.max(all_ratios):.4f}")

    print(f"\n  Number of distinct prime factors of p+1 (twin primes):")
    for k in sorted(twin_p1_factorizations.keys()):
        print(f"    {k} factors: {twin_p1_factorizations[k]} cases")

    # Key insight: for twin primes p >= 5, p+1 is divisible by 6
    # because p ≡ -1 (mod 6) and p+2 ≡ 1 (mod 6), so p+1 ≡ 0 (mod 6)
    count_div6 = sum(1 for p, _ in twins if (p + 1) % 6 == 0)
    print(f"\n  Twin primes with 6 | (p+1): {count_div6}/{len(twins)} = {count_div6/len(twins):.4f}")
    print(f"  (Should be 1.0 for all twin primes p >= 5)")

    # When p+1 = 6m, check if m is prime (gives p+1 = 2*3*m, φ = (m-1)*2)
    count_m_prime = 0
    for p, _ in twins:
        m = (p + 1) // 6
        if is_prime(m):
            count_m_prime += 1
    print(f"  Twin primes with (p+1)/6 prime: {count_m_prime}/{len(twins)} = {count_m_prime/len(twins):.4f}")


# ============================================================
# TEST 5: JOINT GAP DISTRIBUTION
# For F_{p-1} -> F_p -> F_{p+1} -> F_{p+2} (twin primes),
# track how maximum gap, mean gap, and gap variance change.
# Compare with non-twin triple steps.
# ============================================================

def test_joint_gap_distribution(limit=100):
    """Track gap statistics across the triple injection p -> p+1 -> p+2."""
    print("\n" + "=" * 70)
    print("TEST 5: JOINT GAP DISTRIBUTION across p -> p+1 -> p+2")
    print("=" * 70)

    twins = twin_primes_up_to(limit)
    all_primes = primes_up_to(limit)
    prime_set = set(all_primes)

    import numpy as np

    print(f"\n{'p':>4} {'q':>4} | {'max_gap(p-1)':>12} {'max_gap(p)':>10} {'max_gap(p+1)':>12} {'max_gap(q)':>10} | {'Δmax p':>8} {'Δmax p+1':>8} {'Δmax q':>8}")
    print("-" * 110)

    twin_delta_max_p = []
    twin_delta_max_p1 = []
    twin_delta_max_q = []

    for p, q in twins:
        F_pm1 = farey_sequence(p - 1)
        F_p = farey_sequence(p)
        F_p1 = farey_sequence(p + 1)
        F_q = farey_sequence(q)

        gaps_pm1 = gap_sizes(F_pm1)
        gaps_p = gap_sizes(F_p)
        gaps_p1 = gap_sizes(F_p1)
        gaps_q = gap_sizes(F_q)

        max_pm1 = float(max(gaps_pm1))
        max_p = float(max(gaps_p))
        max_p1 = float(max(gaps_p1))
        max_q = float(max(gaps_q))

        d_p = max_p - max_pm1
        d_p1 = max_p1 - max_p
        d_q = max_q - max_p1

        twin_delta_max_p.append(d_p)
        twin_delta_max_p1.append(d_p1)
        twin_delta_max_q.append(d_q)

        print(f"{p:4d} {q:4d} | {max_pm1:12.6f} {max_p:10.6f} {max_p1:12.6f} {max_q:10.6f} | {d_p:+8.6f} {d_p1:+8.6f} {d_q:+8.6f}")

    print(f"\nMean Δmax_gap at prime p:     {np.mean(twin_delta_max_p):+.6f}")
    print(f"Mean Δmax_gap at composite p+1: {np.mean(twin_delta_max_p1):+.6f}")
    print(f"Mean Δmax_gap at prime p+2:   {np.mean(twin_delta_max_q):+.6f}")

    # Compare: for non-twin primes, what's Δmax at p+1 (also composite)?
    non_twin_delta_p1 = []
    for pr in all_primes:
        if pr >= 5 and pr + 2 not in prime_set and pr <= limit:
            # p+1 is composite for any prime p > 2
            try:
                F_p = farey_sequence(pr)
                F_p1 = farey_sequence(pr + 1)
                gaps_p = gap_sizes(F_p)
                gaps_p1 = gap_sizes(F_p1)
                d = float(max(gaps_p1)) - float(max(gaps_p))
                non_twin_delta_p1.append(d)
            except:
                pass

    if non_twin_delta_p1:
        print(f"\nNon-twin: Mean Δmax_gap at composite p+1: {np.mean(non_twin_delta_p1):+.6f}")


# ============================================================
# TEST 6: INJECTION POSITION INTERLEAVING
# For twin primes: the p-1 fractions k/p and the φ(p+2)-1
# fractions k/(p+2) — how do they interleave on [0,1]?
# Measure: fraction of intervals [k/p, (k+1)/p] that contain
# exactly 0, 1, 2, ... fractions of the form j/(p+2).
# ============================================================

def test_injection_interleaving(limit=200):
    """How do k/p and k/(p+2) fractions interleave?"""
    print("\n" + "=" * 70)
    print("TEST 6: INTERLEAVING of k/p and j/(p+2) fractions")
    print("=" * 70)

    twins = twin_primes_up_to(limit)

    import numpy as np

    # Aggregate counts across all twin pairs
    twin_interleave_counts = Counter()
    total_intervals_twin = 0

    non_twin_interleave_counts = Counter()
    total_intervals_non = 0

    all_primes = primes_up_to(limit)
    prime_set = set(all_primes)

    for p, q in twins:
        # Fractions k/p: 1/p, 2/p, ..., (p-1)/p
        frac_p = [Fraction(k, p) for k in range(1, p)]
        # Fractions j/q: j/q with gcd(j,q)=1
        frac_q = [Fraction(j, q) for j in range(1, q) if gcd(j, q) == 1]
        frac_q_sorted = sorted(frac_q)

        # For each interval [k/p, (k+1)/p], count how many j/q fall in it
        for k in range(0, p):
            lo = Fraction(k, p)
            hi = Fraction(k + 1, p)
            count = sum(1 for f in frac_q_sorted if lo < f < hi)
            twin_interleave_counts[count] += 1
            total_intervals_twin += 1

    # Compare with non-twin: consecutive primes with gap > 2
    non_twins_used = 0
    for i in range(len(all_primes) - 1):
        p = all_primes[i]
        q = all_primes[i + 1]
        if q - p > 2 and p >= 5 and q <= limit:
            frac_p = [Fraction(k, p) for k in range(1, p) if gcd(k, p) == 1]
            frac_q = [Fraction(j, q) for j in range(1, q) if gcd(j, q) == 1]
            frac_q_sorted = sorted(frac_q)

            for k in range(0, p):
                lo = Fraction(k, p)
                hi = Fraction(k + 1, p)
                count = sum(1 for f in frac_q_sorted if lo < f < hi)
                non_twin_interleave_counts[count] += 1
                total_intervals_non += 1
            non_twins_used += 1
            if non_twins_used >= len(twins):
                break

    print(f"\n  Twin primes: distribution of j/(p+2) per interval [k/p, (k+1)/p]")
    for c in sorted(twin_interleave_counts.keys()):
        pct = 100 * twin_interleave_counts[c] / total_intervals_twin
        print(f"    {c:2d} fractions: {twin_interleave_counts[c]:5d} intervals ({pct:5.1f}%)")

    print(f"\n  Non-twin primes: distribution of j/q per interval [k/p, (k+1)/p]")
    for c in sorted(non_twin_interleave_counts.keys()):
        pct = 100 * non_twin_interleave_counts[c] / total_intervals_non
        print(f"    {c:2d} fractions: {non_twin_interleave_counts[c]:5d} intervals ({pct:5.1f}%)")

    # Expected: for random placement of ~q fractions in p intervals,
    # Poisson with mean ~q/p ≈ 1. For twin primes, q/p ≈ 1+2/p ≈ 1.
    print(f"\n  Expected for Poisson(λ≈1): P(0)≈36.8%, P(1)≈36.8%, P(2)≈18.4%")


# ============================================================
# TEST 7: THE KEY ALGEBRAIC TEST
# For twin primes p, p+2: the fraction k/p has mediant neighbor
# structure determined by k^{-1} mod p.
# The fraction k/(p+2) has neighbor structure determined by k^{-1} mod (p+2).
#
# ALGEBRAIC RELATIONSHIP:
# If x = k^{-1} mod p, then kx = 1 + mp for some integer m.
# What is k^{-1} mod (p+2)?
# kx = 1 + mp, so kx mod (p+2) = (1 + mp) mod (p+2) = 1 + m(p+2) - 2m mod (p+2)
# = 1 - 2m mod (p+2)
# So k^{-1} mod (p+2) = x - 2m(x) mod (p+2) where m(x) = (kx-1)/p
# This is a SPECIFIC algebraic relationship!
# ============================================================

def test_algebraic_relationship(limit=500):
    """Test the algebraic relationship between inverses mod p and mod p+2."""
    print("\n" + "=" * 70)
    print("TEST 7: ALGEBRAIC RELATIONSHIP between k^{-1} mod p and k^{-1} mod (p+2)")
    print("=" * 70)

    twins = twin_primes_up_to(limit)

    print(f"\n  For twin primes: if kx ≡ 1 (mod p), what is k^{{-1}} mod (p+2)?")
    print(f"  kx = 1 + mp, so k^{{-1}} mod (p+2) ≡ x + 2⌊kx/p⌋·(-1) ... let's verify.\n")

    import numpy as np

    for p, q in twins[:10]:
        print(f"  p={p}, q={q}:")
        common_k = [k for k in range(1, min(p, q)) if gcd(k, p) == 1 and gcd(k, q) == 1]

        diffs = []
        for k in common_k[:8]:
            inv_p = pow(k, -1, p)  # x such that kx ≡ 1 (mod p)
            inv_q = pow(k, -1, q)  # y such that ky ≡ 1 (mod q)

            m = (k * inv_p - 1) // p  # kx = 1 + mp

            # Prediction: y ≡ x - 2m (mod q)?
            predicted = (inv_p - 2 * m) % q

            # Actually: kx = 1 + mp. k*inv_q ≡ 1 (mod q).
            # k(x - 2m) mod q = (kx - 2km) mod q = (1 + mp - 2km) mod q
            # = (1 + m(p - 2k)) mod q = (1 + m(q - 2 - 2k)) mod q = (1 - m(2k+2) + mq) mod q
            # = (1 - 2m(k+1)) mod q
            # For this to equal 1, we need 2m(k+1) ≡ 0 (mod q), which is not generally true.

            # So the prediction x - 2m is NOT correct in general.
            # Let's just measure the actual relationship.
            diff = (inv_q - inv_p) % q
            diffs.append(diff)

            match = "✓" if predicted == inv_q else "✗"
            print(f"    k={k:3d}: inv_p={inv_p:4d}, inv_q={inv_q:4d}, "
                  f"diff mod q = {diff:4d}, predicted = {predicted:4d} {match}")

        # Check if diff has a pattern
        if len(diffs) > 2:
            print(f"    diffs mod q: {diffs}")

    # DEEPER: measure statistics of (inv_q - inv_p) mod q across all k
    print(f"\n--- Distribution of (k^{{-1}} mod q - k^{{-1}} mod p) mod q ---")
    for p, q in twins[:5]:
        common_k = [k for k in range(1, p) if gcd(k, p) == 1 and gcd(k, q) == 1]
        diffs = [(pow(k, -1, q) - pow(k, -1, p)) % q for k in common_k]
        # Is this uniformly distributed?
        hist = Counter(diffs)
        max_freq = max(hist.values())
        min_freq = min(hist.values()) if hist else 0
        unique = len(hist)
        print(f"  p={p:4d}: {len(diffs)} values, {unique} distinct, "
              f"freq range [{min_freq}, {max_freq}], "
              f"uniform would have ~{len(diffs)/q:.1f} per bin")


# ============================================================
# TEST 8: WOBBLE CONTRIBUTION DECOMPOSITION
# For small twin primes, exactly decompose W(p+2) - W(p-1)
# into the three steps: W(p) - W(p-1) + W(p+1) - W(p) + W(p+2) - W(p+1)
# and see if the composite step (p -> p+1) has special structure
# for twin primes.
# ============================================================

def test_wobble_decomposition(limit=80):
    """Decompose W change across twin prime triple: p-1 -> p -> p+1 -> p+2."""
    print("\n" + "=" * 70)
    print("TEST 8: WOBBLE DECOMPOSITION W(p-1) -> W(p) -> W(p+1) -> W(p+2)")
    print("=" * 70)

    twins = twin_primes_up_to(limit)

    import numpy as np

    def compute_wobble(F):
        """Compute wobble = sum of (f_j - j/n)^2 where n = len(F)-1."""
        n = len(F) - 1  # number of gaps
        if n <= 0:
            return 0
        total = sum((float(F[j]) - j / n) ** 2 for j in range(n + 1))
        return total

    print(f"\n{'p':>4} {'q':>4} | {'ΔW(p)':>10} {'ΔW(p+1)':>10} {'ΔW(q)':>10} | {'total':>10} | {'|comp/prime|':>12}")
    print("-" * 85)

    ratios = []

    for p, q in twins:
        F_pm1 = farey_sequence(p - 1)
        F_p = farey_sequence(p)
        F_p1 = farey_sequence(p + 1)
        F_q = farey_sequence(q)

        W_pm1 = compute_wobble(F_pm1)
        W_p = compute_wobble(F_p)
        W_p1 = compute_wobble(F_p1)
        W_q = compute_wobble(F_q)

        dw_p = W_p - W_pm1
        dw_p1 = W_p1 - W_p
        dw_q = W_q - W_p1
        total = W_q - W_pm1

        # Ratio of composite step to prime steps
        prime_avg = (abs(dw_p) + abs(dw_q)) / 2
        if prime_avg > 0:
            ratio = abs(dw_p1) / prime_avg
            ratios.append(ratio)
        else:
            ratio = float('nan')

        print(f"{p:4d} {q:4d} | {dw_p:+10.6f} {dw_p1:+10.6f} {dw_q:+10.6f} | {total:+10.6f} | {ratio:12.4f}")

    if ratios:
        print(f"\nMean |ΔW(composite)| / mean |ΔW(prime)|: {np.mean(ratios):.4f}")
        print(f"  (If < 1: composite steps contribute less wobble change than prime steps)")

    # Compare with non-twin: pick a non-twin prime p, look at p -> p+1 -> p+2
    # where p+2 is NOT prime
    non_twin_ratios = []
    all_primes = primes_up_to(limit)
    prime_set = set(all_primes)
    for pr in all_primes:
        if pr >= 5 and pr + 2 not in prime_set and pr <= limit - 2:
            try:
                F_pm1 = farey_sequence(pr - 1)
                F_p = farey_sequence(pr)
                F_p1 = farey_sequence(pr + 1)
                F_p2 = farey_sequence(pr + 2)

                W_pm1 = compute_wobble(F_pm1)
                W_p = compute_wobble(F_p)
                W_p1 = compute_wobble(F_p1)
                W_p2 = compute_wobble(F_p2)

                dw_p = W_p - W_pm1
                dw_p1 = W_p1 - W_p
                dw_p2 = W_p2 - W_p1

                prime_step = abs(dw_p)
                comp_step = abs(dw_p1)
                if prime_step > 0:
                    non_twin_ratios.append(comp_step / prime_step)
            except:
                pass

    if non_twin_ratios:
        print(f"\nNon-twin: Mean |ΔW(p+1)| / |ΔW(p)|: {np.mean(non_twin_ratios):.4f}")
        print(f"  (Compare with twin value above)")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("TWIN PRIME JOINT INJECTION STRUCTURE")
    print("=" * 70)
    print("Goal: Find structural features of twin prime Farey injection")
    print("      beyond mere Mertens smoothness.\n")

    # Test 1: Gap overlap (quick, up to p~200)
    r1 = test_gap_overlap(200)

    # Test 2: Twin vs non-twin comparison
    test_twin_vs_random(150)

    # Test 3: Modular inverse correlation
    test_modular_inverse_correlation(500)

    # Test 4: φ(p+1) structure
    test_phi_p_plus_1(1000)

    # Test 5: Joint gap distribution (slow, keep small)
    test_joint_gap_distribution(80)

    # Test 6: Interleaving
    test_injection_interleaving(120)

    # Test 7: Algebraic relationship
    test_algebraic_relationship(200)

    # Test 8: Wobble decomposition
    test_wobble_decomposition(80)

    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print("""
    FINDINGS (honest assessment):

    1. GAP OVERLAP: The overlap is always EXACTLY 4 gaps for all twin primes.
       This is NOT twin-specific — it's because both p and p+2 always inject
       into the 4 gaps around 0/1, 1/2, and 1/1 (the Stern-Brocot backbone).
       The overlap rate ~1/(p/2) shrinks to zero. NOT SPECIAL.

    2. TWIN vs NON-TWIN OVERLAP: Twin (0.127), Cousin (0.128), Sexy (0.174),
       Non-twin (0.101). Differences are small and driven by gap size, not
       twin-ness. The overlap decreases with prime size for all types. NOT SPECIAL.

    3. MODULAR INVERSE CORRELATION: Twin pairs show mean corr = -0.112,
       non-twin pairs show mean corr = +0.053. The NEGATIVE correlation for
       twins is mildly interesting — inverses mod p and mod p+2 tend to
       anti-correlate — but the effect is weak (std 0.064) and likely just
       a small-number artifact of the gap-2 arithmetic. POSSIBLY INTERESTING
       but needs larger samples to confirm it persists.

    4. φ(p+1) STRUCTURE: Twin primes have φ(p+1)/(p+1) mean 0.298 vs 0.393
       for non-twins. This IS genuinely different but is TRIVIALLY explained:
       for twin primes p >= 5, p+1 is ALWAYS divisible by 6 (= 2*3), which
       automatically gives φ(p+1)/(p+1) <= 1/3. This is well-known
       elementary number theory, not a new structural insight. EXPLAINED.

    5. INTERLEAVING: Twins show 98% single-occupancy (1 fraction per interval),
       non-twins show 87%. This looks striking but is ENTIRELY explained by
       the gap-2 arithmetic: for twin primes, (p+2)/p ≈ 1 + 2/p so each
       interval [k/p, (k+1)/p] gets almost exactly one fraction j/(p+2).
       For larger gaps, the ratio deviates more. TRIVIALLY EXPLAINED.

    6. ALGEBRAIC RELATIONSHIP: k^{-1} mod (p+2) has no clean formula in
       terms of k^{-1} mod p. The difference (inv_q - inv_p) mod q appears
       pseudo-random. NO SPECIAL STRUCTURE.

    7. WOBBLE DECOMPOSITION: The composite step (p+1) contributes ~69% as
       much wobble change as the prime steps for twins, vs ~51% for non-twins.
       Twin primes have a LARGER composite contribution, but this is just
       because 6|(p+1) means φ(p+1) is relatively large among composite
       numbers. EXPLAINED by the 6|(p+1) constraint.

    VERDICT: Twin primes have NO special joint Farey injection structure
    beyond what is trivially explained by:
      (a) Mertens smoothness (sign correlation)
      (b) The fact that 6|(p+1) for all twin primes p >= 5 (φ structure)
      (c) Basic gap-2 arithmetic (interleaving)

    The weak negative modular-inverse correlation is the only potentially
    non-trivial signal, but it is small (r ≈ -0.11) and would need much
    larger computation to determine if it persists or is a finite-size effect.
    """)
