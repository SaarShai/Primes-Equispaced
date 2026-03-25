#!/usr/bin/env python3
"""
GENERAL INJECTION PRINCIPLE: Holds for ALL N >= 2, not just primes
==================================================================

THEOREM: When constructing F_N from F_{N-1}, each gap of F_{N-1}
receives at most 1 new fraction with denominator N.

New fractions inserted: a/N where 0 < a < N and gcd(a, N) = 1.
There are phi(N) such fractions.

PROOF STRATEGY:
  For consecutive fractions p/q, r/s in F_{N-1}:
    - They satisfy |ps - qr| = 1 (Farey neighbor property)
    - The gap width is 1/(qs)
    - q, s <= N-1
    - q + s >= N (standard Farey property: consecutive iff q+s > N-1)

  A fraction a/N lies in gap (p/q, r/s) iff p/q < a/N < r/s,
  i.e., pN < aq and aN < rN... wait, let's be precise.

  Suppose two distinct fractions a/N and a'/N (with a < a') both
  lie in the gap (p/q, r/s). Then:
    a'/N - a/N >= 1/N  (since a' >= a+1, as both have denom N)

  But the gap width is 1/(qs). So we need 1/N <= 1/(qs), i.e., qs <= N.

  Since q, s <= N-1 and q + s >= N:
    - If q + s >= N, can we have qs <= N?
    - By AM-GM: qs <= (q+s)^2/4
    - But we need the OTHER direction: qs >= ???

  KEY LEMMA: For q + s >= N with q, s >= 1:
    qs >= q + s - 1 >= N - 1
    (since qs - q - s + 1 = (q-1)(s-1) >= 0)

  So qs >= N - 1, hence gap width 1/(qs) <= 1/(N-1) < ... hmm.

  But 1/(N-1) vs 1/N: we need gap < 1/N or <= 1/N.
  Actually qs >= N - 1 gives gap width <= 1/(N-1).
  Two fractions with denom N are spaced >= 1/N apart.
  1/(N-1) vs 1/N: 1/(N-1) > 1/N, so this bound is NOT tight enough!

  REFINED ARGUMENT: We need qs >= N+1 to get gap < 1/N.
  When does qs = N-1 or qs = N happen?

  qs = N-1: possible, e.g. q=1, s=N-1. Gap (0/1, 1/(N-1)).
  But then 1/N is the ONLY fraction with denom N in (0, 1/(N-1)),
  since 2/N > 1/(N-1) when N >= 3. Check: 2/N vs 1/(N-1):
  2(N-1) vs N, i.e., 2N-2 vs N, i.e., N vs 2. So for N>=3, 2/N > 1/(N-1).
  So at most 1 fits. For N=2: gap (0/1, 1/1), only 1/2 is inserted. OK.

  qs = N: e.g. q=2, s=N/2 (when N even). Gap width = 1/N.
  Can two fractions a/N, (a+1)/N fit? Need (a+1)/N - a/N = 1/N <= 1/N.
  So we need a/N > p/q AND (a+1)/N < r/s. The gap width is exactly 1/N
  but we need STRICT inequalities. Since a/N > p/q means aq > pN (integers),
  and (a+1)/N < r/s means (a+1)s < rN. The gap has width exactly 1/(qs) = 1/N.
  But p/q and r/s are Farey neighbors, so rs - pq... wait, rs - qs...
  let me use the standard: r*q - p*s = 1.

  With rq - ps = 1 and qs = N:
  If a/N is in the gap: aq - pN > 0 and rN - (a)s > 0...
  Actually aq > pN => aq >= pN+1 and rN > as => rN >= as+1.
  So a >= (pN+1)/q and a <= (rN-1)/s.
  Range of a: (rN-1)/s - (pN+1)/q = (rNq - q - pNs - s)/(qs)
  = (N(rq - ps) - (q+s))/(qs) = (N*1 - (q+s))/N = (N - q - s)/N.
  Since q+s >= N, this is <= 0. So at most 1 integer a fits!

  COMPLETE PROOF: For consecutive p/q, r/s in F_{N-1} with rq-ps=1:
  Integer a with p/q < a/N < r/s satisfies:
    aq > pN  =>  a > pN/q  =>  a >= floor(pN/q) + 1
    as < rN  =>  a < rN/s  =>  a <= ceil(rN/s) - 1

  Number of valid a = ceil(rN/s) - 1 - floor(pN/q) = ?

  Using rq - ps = 1:
    rN/s - pN/q = N(rq - ps)/(qs) = N/(qs)

  The number of integers in the open interval (pN/q, rN/s) is:
    floor(rN/s - 1) - floor(pN/q)  [if endpoints aren't integers]
    or at most floor(rN/s) - ceil(pN/q) + 1 in the closed case,
    but we need strict inequalities.

  # integers in open interval (x, x + N/(qs)):
  Since N/(qs) = the length of the interval, and q+s >= N means qs >= N-1:
    - If qs >= N+1: length < 1, so at most 0 integers.
    - If qs = N: length = 1, open interval of length 1 has at most 1 integer.
    - If qs = N-1: length = N/(N-1) > 1.
      But we must check: can 2 integers fit?
      Length N/(N-1) = 1 + 1/(N-1) < 2 for N >= 2.
      Open interval of length < 2 has at most 1 integer? NO!
      Open interval of length L has at most ceil(L) integers...
      Actually (0.5, 2.6) has length 2.1 and contains 1, 2 (two integers).
      (0.1, 1.2) has length 1.1 and contains 1 (one integer).
      (0.9, 2.0) has length 1.1 but open, so contains 1 (one integer).
      (-0.1, 1.1) contains 0, 1 (two integers? length 1.2).

      For length 1 + 1/(N-1), we need to check if 2 integers can fit.
      An open interval (x, x+L) with L < 2 contains at most 1 integer
      when floor(x+L) = floor(x) + 1 or ceil(x) = floor(x+L).
      Actually not always: (0.1, 1.6) has length 1.5 and contains 1.
      (0.4, 1.9) has length 1.5 and contains 1.
      (0.9, 2.4) has length 1.5 and contains 1, 2 -- TWO integers!

      So length > 1 CAN contain 2 integers. We need a sharper argument.

  SHARPER PROOF for qs = N-1 case:
  q + s >= N and qs = N - 1.
  (q-1)(s-1) = qs - q - s + 1 = N - 1 - (q+s) + 1 = N - (q+s).
  Since q+s >= N: (q-1)(s-1) <= 0.
  Since q,s >= 1: (q-1)(s-1) >= 0.
  So (q-1)(s-1) = 0, meaning q = 1 or s = 1.

  Case q = 1: consecutive pair is p/1, r/s with r*1 - p*s = 1,
  so r = ps + 1. The pair is (p, (ps+1)/s).
  In F_{N-1}, s <= N-1. With qs = s*1 = s = N-1, so s = N-1.
  The gap is (p/1, (p(N-1)+1)/(N-1)) = (p, p + 1/(N-1)).
  Fractions a/N in this gap: p < a/N < p + 1/(N-1).
  So pN < a < pN + N/(N-1) = pN + 1 + 1/(N-1).
  So a = pN + 1 is the only integer. And gcd(pN+1, N) = gcd(1, N) = 1. Good.

  Case s = 1: similar by symmetry. Gap is (p/q, r/1) where r = (p+1)/...
  Actually rq - p = 1, so r = (p+1)/q. Then q | (p+1).
  With qs = q = N-1, the gap is (p/(N-1), (p+1)/(N-1)).
  Gap width = 1/(N-1). Fractions a/N in gap:
  pN/(N-1) < a < (p+1)N/(N-1).
  Length = N/(N-1) = 1 + 1/(N-1). But pN/(N-1) = p + p/(N-1).
  So a must satisfy p + p/(N-1) < a < p + 1 + (p+1)/(N-1).
  If p/(N-1) is not integer (i.e., (N-1) does not divide p):
    floor(p + p/(N-1)) = p + floor(p/(N-1)).
    Only a = p + floor(p/(N-1)) + 1 could work. At most 1.
  If (N-1) | p, say p = k(N-1): then lower bound = p + k = kN.
  Upper bound = kN + 1 + (k+1)/(... wait, let me just verify all this
  computationally.

COMPUTATIONAL VERIFICATION below, followed by the clean proof.
"""

from math import gcd
from fractions import Fraction
import time


def farey_sequence(n):
    """Generate Farey sequence F_n as list of Fraction objects."""
    fracs = set()
    for d in range(1, n + 1):
        for num in range(0, d + 1):
            if gcd(num, d) == 1 or num == 0 or num == d:
                if 0 <= num <= d:
                    fracs.add(Fraction(num, d))
    return sorted(fracs)


def farey_sequence_fast(n):
    """Generate F_n using mediant property (faster)."""
    # Start with F_1 = [0/1, 1/1]
    if n == 0:
        return [Fraction(0, 1), Fraction(1, 1)]
    if n == 1:
        return [Fraction(0, 1), Fraction(1, 1)]

    seq = [Fraction(0, 1), Fraction(1, 1)]
    for order in range(2, n + 1):
        new_seq = []
        for i in range(len(seq) - 1):
            new_seq.append(seq[i])
            # Check if mediant has denominator = order
            a, b = seq[i].numerator, seq[i].denominator
            c, d = seq[i+1].numerator, seq[i+1].denominator
            if b + d == order:
                new_seq.append(Fraction(a + c, b + d))
            # Also check all a/order in this gap
            # Actually the mediant method only works for Stern-Brocot.
            # For Farey, we need all a/order with gcd(a,order)=1.
        new_seq.append(seq[-1])
        seq = new_seq

    # Fallback: just use the set-based approach
    return farey_sequence(n)


def verify_injection(N):
    """
    Verify: when going from F_{N-1} to F_N, each gap of F_{N-1}
    receives at most 1 new fraction.

    Returns (max_insertions_per_gap, total_new, num_gaps, details).
    """
    # Build F_{N-1}
    F_prev = farey_sequence(N - 1)

    # New fractions: a/N with gcd(a, N) = 1, 0 < a < N
    new_fracs = []
    for a in range(1, N):
        if gcd(a, N) == 1:
            new_fracs.append(Fraction(a, N))
    new_fracs.sort()

    # Count how many new fractions fall in each gap
    num_gaps = len(F_prev) - 1
    gap_counts = [0] * num_gaps
    gap_details = [[] for _ in range(num_gaps)]

    for frac in new_fracs:
        # Binary search for the gap containing frac
        lo, hi = 0, len(F_prev) - 1
        while lo < hi - 1:
            mid = (lo + hi) // 2
            if F_prev[mid] < frac:
                lo = mid
            else:
                hi = mid
        # frac is in gap (F_prev[lo], F_prev[lo+1])
        if lo < num_gaps:
            gap_counts[lo] += 1
            gap_details[lo].append(frac)

    max_count = max(gap_counts) if gap_counts else 0

    # Find worst-case gaps
    worst_gaps = []
    for i, c in enumerate(gap_counts):
        if c == max_count and max_count > 0:
            p, q = F_prev[i].numerator, F_prev[i].denominator
            r, s = F_prev[i+1].numerator, F_prev[i+1].denominator
            worst_gaps.append({
                'left': f"{p}/{q}",
                'right': f"{r}/{s}",
                'q+s': q + s,
                'qs': q * s,
                'width': f"1/{q*s}",
                'inserted': [str(f) for f in gap_details[i]]
            })

    return max_count, len(new_fracs), num_gaps, worst_gaps


def verify_farey_neighbor_property(N):
    """
    Verify that consecutive fractions in F_N satisfy |ps - qr| = 1.
    Also verify q + s > N for non-consecutive (q+s <= N means mediant is between).
    """
    F = farey_sequence(N)
    for i in range(len(F) - 1):
        p, q = F[i].numerator, F[i].denominator
        r, s = F[i+1].numerator, F[i+1].denominator
        det = r * q - p * s
        if det != 1:
            return False, f"det={det} at {p}/{q}, {r}/{s}"
        if q + s < N + 1:  # q + s should be > N-1, i.e., >= N...
            # Actually for F_N, consecutive iff q+s > N
            # So q+s >= N+1? No. q+s > N means q+s >= N+1 only for integers.
            # Wait: the standard result is p/q, r/s consecutive in F_N iff
            # rs - pq = 1 AND q + s > N. Since q+s is integer, q+s > N means q+s >= N+1.
            # But actually the correct statement is: they are consecutive in F_N
            # iff |rs-pq|=1 AND q+s > N. Hmm, but 0/1 and 1/N are consecutive
            # in F_N, and 1+N = N+1 > N. OK.
            pass
    return True, "OK"


def prove_qs_bound(N):
    """
    For consecutive p/q, r/s in F_{N-1}:
    Show that if qs <= N, then at most 1 fraction a/N fits in the gap.

    Approach: count integers in (pN/q, rN/s) which has length N/(qs).
    """
    F = farey_sequence(N - 1)
    results = []
    for i in range(len(F) - 1):
        p, q = F[i].numerator, F[i].denominator
        r, s = F[i+1].numerator, F[i+1].denominator
        qs_val = q * s
        gap_length_times_N = Fraction(N, q * s)  # N/(qs), number of width-1/N intervals

        # Count integers a in open interval (pN/q, rN/s)
        lower = Fraction(p * N, q)
        upper = Fraction(r * N, s)

        count = 0
        a_start = int(lower) + 1 if lower == int(lower) else int(lower) + 1
        # More carefully:
        a_start = lower.numerator // lower.denominator + 1
        if Fraction(a_start, 1) <= lower:
            a_start += 1

        a_vals = []
        a = a_start
        while Fraction(a, 1) < upper:
            if gcd(a, N) == 1:  # Must also have gcd(a,N)=1
                a_vals.append(a)
            a += 1

        results.append({
            'p': p, 'q': q, 'r': r, 's': s,
            'qs': qs_val, 'q+s': q + s,
            'interval_length': float(gap_length_times_N),
            'coprime_count': len(a_vals),
            'all_integers_in_interval': a - a_start,
        })

    return results


# ============================================================
# MAIN VERIFICATION
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GENERAL INJECTION PRINCIPLE: Verification for ALL N >= 2")
    print("=" * 70)
    print()

    # Phase 1: Verify for N = 2..100
    print("PHASE 1: Computational verification for N = 2..100")
    print("-" * 50)

    all_pass = True
    max_N_tested = 100

    t0 = time.time()
    for N in range(2, max_N_tested + 1):
        max_count, total_new, num_gaps, worst = verify_injection(N)

        is_prime = all(N % d != 0 for d in range(2, int(N**0.5) + 1)) and N > 1
        label = "PRIME" if is_prime else "COMP"

        if max_count > 1:
            print(f"  N={N:3d} [{label}]: FAIL! max={max_count} per gap")
            print(f"    Worst gaps: {worst}")
            all_pass = False
        elif N <= 20 or is_prime or N % 10 == 0:
            print(f"  N={N:3d} [{label}]: OK  (phi(N)={total_new:3d} new fracs, "
                  f"{num_gaps:4d} gaps, max {max_count} per gap)")

    t1 = time.time()
    print(f"\n  Time: {t1-t0:.1f}s")

    if all_pass:
        print(f"\n  *** VERIFIED: Injection holds for ALL N = 2..{max_N_tested} ***")
    else:
        print(f"\n  *** COUNTEREXAMPLE FOUND ***")

    # Phase 2: Verify for larger N (spot checks)
    print(f"\n\nPHASE 2: Spot checks for larger N")
    print("-" * 50)

    spot_checks = [120, 144, 150, 180, 200, 210, 240, 256, 300, 360]
    for N in spot_checks:
        max_count, total_new, num_gaps, worst = verify_injection(N)
        is_prime = all(N % d != 0 for d in range(2, int(N**0.5) + 1)) and N > 1
        label = "PRIME" if is_prime else "COMP"
        status = "OK" if max_count <= 1 else f"FAIL(max={max_count})"
        print(f"  N={N:3d} [{label}]: {status}  (phi={total_new}, gaps={num_gaps})")
        if max_count > 1:
            all_pass = False

    # Phase 3: Analyze the boundary cases (qs = N-1 and qs = N)
    print(f"\n\nPHASE 3: Boundary analysis (gaps where qs <= N)")
    print("-" * 50)

    for N in [4, 6, 8, 9, 10, 12, 15, 16, 20, 30]:
        results = prove_qs_bound(N)
        boundary = [r for r in results if r['qs'] <= N]
        print(f"\n  N={N}: {len(boundary)} gaps with qs <= N:")
        for r in boundary:
            print(f"    ({r['p']}/{r['q']}, {r['r']}/{r['s']}): "
                  f"qs={r['qs']}, q+s={r['q+s']}, "
                  f"interval_length={r['interval_length']:.3f}, "
                  f"#coprime_in_gap={r['coprime_count']}")

    # Phase 4: The proof
    print(f"\n\n{'='*70}")
    print("PHASE 4: THE PROOF")
    print("=" * 70)
    print("""
THEOREM: For all N >= 2, each gap of F_{N-1} receives at most 1
new fraction when constructing F_N.

PROOF:

Let p/q and r/s be consecutive fractions in F_{N-1}, so:
  (i)   rq - ps = 1              (Farey neighbor property)
  (ii)  q + s >= N                (consecutive in F_{N-1} iff q+s > N-1)
  (iii) q, s <= N-1               (denominators in F_{N-1})

A fraction a/N (with gcd(a,N)=1) lies in the gap (p/q, r/s) iff:
  p/q < a/N < r/s

Multiplying through:
  pN/q < a < rN/s

The number of integers in the open interval (pN/q, rN/s) is at most:
  floor(rN/s) - floor(pN/q)  (possibly minus 1 for endpoint issues)

The length of this interval is:
  rN/s - pN/q = N(rq - ps)/(qs) = N/(qs)     [using (i)]

CASE 1: qs >= N+1, i.e., qs > N.
  Then N/(qs) < 1, so the open interval has length < 1.
  An open interval of length < 1 contains at most 1 integer.
  (Actually at most 0 or 1.) So at most 1 fraction a/N fits.
  Since we additionally need gcd(a,N)=1, the count is <= 1. Done.

CASE 2: qs = N.
  The interval (pN/q, rN/s) has length exactly 1.
  We claim at most 1 integer lies strictly inside.

  Lower bound: pN/q. Upper bound: rN/s = rN/s.
  Since rq - ps = 1: rN/s = (ps+1)N/(qs/q) ... let's think differently.

  pN/q: is this an integer? pN/q is integer iff q | pN. Since gcd(p,q)=1,
  this means q | N. Similarly rN/s is integer iff s | N.

  If pN/q is an integer, the open interval starts just above it.
  If rN/s is an integer, the open interval ends just below it.

  An open interval (x, x+1) of length exactly 1:
  - Contains exactly 1 integer if x is not an integer
  - Contains 0 integers if x IS an integer (the interval is (k, k+1))

  So when qs = N: at most 1 integer in the interval. Done.

CASE 3: qs = N-1.
  Then (q-1)(s-1) = qs - q - s + 1 = (N-1) - (q+s) + 1 = N - (q+s).
  From (ii), q+s >= N, so (q-1)(s-1) <= 0.
  From q,s >= 1, (q-1)(s-1) >= 0.
  Therefore (q-1)(s-1) = 0, so q = 1 or s = 1 (or both, but q=s=1
  only for the pair 0/1, 1/1 in F_1).

  Also q + s = N (from the equality above).

  Sub-case 3a: q = 1, s = N-1.
    Gap is (p/1, r/(N-1)). Since rq - ps = r - p(N-1) = 1,
    we get r = p(N-1) + 1. The gap is (p, (p(N-1)+1)/(N-1)).
    Gap width = 1/(N-1).

    Integers a with pN < a*1 < ... wait, fractions a/N in gap:
    p < a/N < (p(N-1)+1)/(N-1) = p + 1/(N-1)

    So pN < a < pN + N/(N-1) = pN + 1 + 1/(N-1).

    The only integer in (pN, pN + 1 + 1/(N-1)) is a = pN + 1.
    Check: gcd(pN+1, N) = gcd(1, N) = 1. YES.
    So exactly 1 fraction is inserted. Done.

  Sub-case 3b: s = 1, q = N-1.
    Gap is (p/(N-1), r/1). Since r(N-1) - p = 1, p = r(N-1) - 1.
    Gap is ((r(N-1)-1)/(N-1), r) = (r - 1/(N-1), r).

    Fractions a/N in gap: r - 1/(N-1) < a/N < r.
    So rN - N/(N-1) < a < rN, i.e., rN - 1 - 1/(N-1) < a < rN.

    The only integer is a = rN - 1.
    Check: gcd(rN-1, N) = gcd(-1, N) = 1. YES.
    So exactly 1 fraction is inserted. Done.

CASE 4: qs < N-1.
  Then (q-1)(s-1) = N - (q+s) < 0 when q+s > N, which contradicts
  (q-1)(s-1) >= 0. And if q+s = N, then (q-1)(s-1) = 0 and qs =
  q+s - 1 = N-1, contradiction. If q+s > N, then (q-1)(s-1) < 0,
  impossible. So this case CANNOT occur when q+s >= N.

  Formally: qs = q*s and q+s >= N implies
  qs >= (q+s) - 1 >= N - 1 (since (q-1)(s-1) >= 0).
  So qs < N-1 is impossible. QED for Case 4.

COMBINING ALL CASES: In every case, at most 1 fraction a/N with
gcd(a,N) = 1 falls in each gap of F_{N-1}. QED.

NOTE: The proof uses only:
  (i)   rq - ps = 1 (Farey neighbor determinant)
  (ii)  q + s >= N  (Farey consecutive criterion)
  (iii) q, s >= 1   (denominators are positive)
No property of N being prime is needed!
""")

    # Phase 5: Verify the qs >= N-1 bound
    print("PHASE 5: Verify qs >= N-1 for all consecutive pairs")
    print("-" * 50)

    qs_bound_holds = True
    for N in range(2, 81):
        F = farey_sequence(N)
        for i in range(len(F) - 1):
            p, q = F[i].numerator, F[i].denominator
            r, s = F[i+1].numerator, F[i+1].denominator
            if q * s < N:
                print(f"  qs < N at N={N}: ({p}/{q}, {r}/{s}), qs={q*s}")
            if q + s < N + 1:
                print(f"  q+s < N+1 at N={N}: ({p}/{q}, {r}/{s}), q+s={q+s}")
                qs_bound_holds = False

    if qs_bound_holds:
        print(f"  Verified: q+s >= N+1 for all consecutive pairs in F_N, N=2..80")
        print(f"  (which means q+s > N, confirming the Farey property)")

    # Phase 6: Count exact insertions per gap type
    print(f"\n\nPHASE 6: Statistics on insertions by gap type")
    print("-" * 50)

    for N in [6, 10, 12, 15, 20, 24, 30]:
        F_prev = farey_sequence(N - 1)
        total_0 = 0  # gaps receiving 0 fractions
        total_1 = 0  # gaps receiving 1 fraction

        for i in range(len(F_prev) - 1):
            p, q = F_prev[i].numerator, F_prev[i].denominator
            r, s = F_prev[i+1].numerator, F_prev[i+1].denominator

            # Count fractions a/N with gcd(a,N)=1 in this gap
            count = 0
            for a in range(1, N):
                if gcd(a, N) == 1:
                    if Fraction(p, q) < Fraction(a, N) < Fraction(r, s):
                        count += 1

            if count == 0:
                total_0 += 1
            elif count == 1:
                total_1 += 1
            else:
                print(f"  ERROR: N={N}, gap ({p}/{q}, {r}/{s}) has {count} insertions!")

        phi_N = sum(1 for a in range(1, N) if gcd(a, N) == 1)
        print(f"  N={N:3d}: phi(N)={phi_N:3d}, "
              f"gaps_with_0={total_0:4d}, gaps_with_1={total_1:4d}, "
              f"total_gaps={total_0+total_1:4d}")
        assert total_1 == phi_N, f"Mismatch at N={N}!"

    print(f"\n  Verified: gaps_with_1 == phi(N) for all tested N.")
    print(f"  This confirms each new fraction lands in a unique gap.")

    print(f"\n\n{'='*70}")
    print("CONCLUSION")
    print("=" * 70)
    print(f"""
The General Injection Principle is PROVED for all N >= 2:

  When constructing F_N from F_{{N-1}}, each gap of F_{{N-1}}
  receives EXACTLY 0 or 1 new fraction with denominator N.

  Equivalently, the phi(N) new fractions are injected into
  distinct gaps of F_{{N-1}}.

The proof requires only three facts about Farey sequences:
  1. Consecutive fractions satisfy rq - ps = 1
  2. They are consecutive iff q + s > N (i.e., q + s >= N+1)
  3. The gap width is 1/(qs)

Combined with the elementary inequality (q-1)(s-1) >= 0
(i.e., qs >= q + s - 1), these give qs >= N, and so each
gap has width <= 1/N, which can contain at most one fraction
of the form a/N.

The boundary case qs = N-1 (gap width slightly > 1/N) only
occurs when q=1 or s=1, and a direct check shows exactly 1
fraction is inserted in each such gap.

No primality assumption on N is needed.
""")
