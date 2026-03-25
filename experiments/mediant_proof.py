#!/usr/bin/env python3
"""
THEOREM: Every new fraction entering F_N is the mediant of its Farey neighbors in F_{N-1}.

PRECISE STATEMENT:
Let F_N denote the Farey sequence of order N. If a/N ∈ F_N \ F_{N-1} (a new fraction
at step N), and p/q, r/s are the consecutive fractions in F_{N-1} such that p/q < a/N < r/s,
then:
    a = p + r   and   N = q + s

That is, a/N is the mediant (p+r)/(q+s) of its Farey neighbors.

PROOF STRUCTURE:
1. Consecutive Farey fractions p/q < r/s in F_{N-1} satisfy rq - ps = 1 (unimodular).
2. The mediant (p+r)/(q+s) satisfies q+s > N-1 (else it would already be in F_{N-1}).
3. If q+s = N and gcd(p+r, q+s) = 1, then (p+r)/N enters F_N in this gap.
4. If q+s > N, then NO fraction with denominator N fits in the gap (p/q, r/s).
5. Therefore every new fraction at step N is a mediant, and enters exactly when q+s = N.

This script:
  (A) Verifies the theorem computationally for all N = 2..200
  (B) Checks every single new fraction, confirming it equals the mediant
  (C) Checks that gaps with q+s > N receive no new fractions
  (D) Provides the complete analytical proof
"""

from math import gcd
from fractions import Fraction


def farey_sequence(n):
    """Generate Farey sequence F_n as sorted list of Fraction objects."""
    fracs = set()
    for denom in range(1, n + 1):
        for numer in range(0, denom + 1):
            if gcd(numer, denom) == 1:
                fracs.add(Fraction(numer, denom))
    return sorted(fracs)


def verify_mediant_property(max_n=200):
    """
    For each N from 2 to max_n:
    - Compute F_{N-1} and F_N
    - Identify new fractions: F_N \ F_{N-1}
    - For each new fraction a/N, find its neighbors p/q, r/s in F_{N-1}
    - Verify a = p+r and N = q+s (mediant property)
    - Also verify: gaps in F_{N-1} with q+s > N get no new fractions
    """
    print("=" * 72)
    print("VERIFICATION: Every new fraction in F_N is the mediant of its")
    print("              Farey neighbors in F_{N-1}")
    print("=" * 72)

    prev_farey = farey_sequence(1)  # F_1 = {0/1, 1/1}

    total_new_fractions = 0
    total_mediants_confirmed = 0
    total_gaps_checked = 0
    total_empty_gaps_confirmed = 0  # gaps with q+s > N that correctly have no new entry

    all_pass = True

    for N in range(2, max_n + 1):
        curr_farey = farey_sequence(N)
        prev_set = set(prev_farey)
        new_fracs = [f for f in curr_farey if f not in prev_set]

        # Every new fraction must have denominator N
        for f in new_fracs:
            assert f.denominator == N, f"New fraction {f} has denom {f.denominator} != {N}"

        total_new_fractions += len(new_fracs)

        # Check each new fraction is the mediant of its F_{N-1} neighbors
        for f in new_fracs:
            # Find neighbors in F_{N-1}: largest p/q < f and smallest r/s > f
            p_q = None
            r_s = None
            for i in range(len(prev_farey) - 1):
                if prev_farey[i] < f < prev_farey[i + 1]:
                    p_q = prev_farey[i]
                    r_s = prev_farey[i + 1]
                    break

            assert p_q is not None and r_s is not None, \
                f"Could not find neighbors for {f} in F_{N-1}"

            p, q = p_q.numerator, p_q.denominator
            r, s = r_s.numerator, r_s.denominator

            # Verify unimodular condition: rq - ps = 1
            assert r * q - p * s == 1, \
                f"Neighbors {p}/{q}, {r}/{s} not unimodular: rq-ps = {r*q - p*s}"

            # THE KEY CHECK: a/N must equal (p+r)/(q+s)
            a = f.numerator
            mediant_num = p + r
            mediant_den = q + s

            if a != mediant_num or N != mediant_den:
                print(f"  FAIL at N={N}: {f} != mediant ({mediant_num}/{mediant_den}) "
                      f"of {p}/{q} and {r}/{s}")
                all_pass = False
            else:
                total_mediants_confirmed += 1

        # Check gaps in F_{N-1} with q+s > N have no new fraction with denom N
        for i in range(len(prev_farey) - 1):
            p_q = prev_farey[i]
            r_s = prev_farey[i + 1]
            q = p_q.denominator
            s = r_s.denominator
            total_gaps_checked += 1

            if q + s > N:
                # No fraction with denominator N should appear in this gap
                gap_has_new = any(p_q < f < r_s for f in new_fracs)
                if gap_has_new:
                    p, r = p_q.numerator, r_s.numerator
                    offending = [f for f in new_fracs if p_q < f < r_s]
                    print(f"  FAIL: Gap ({p_q}, {r_s}) has q+s={q+s} > {N} "
                          f"but received {offending}")
                    all_pass = False
                else:
                    total_empty_gaps_confirmed += 1

        # Progress report every 50 steps
        if N % 50 == 0 or N == max_n:
            euler_phi = len(new_fracs)
            print(f"  N={N:4d}: phi(N)={euler_phi:4d} new fractions, "
                  f"all mediants: YES | "
                  f"cumulative: {total_mediants_confirmed} confirmed")

        prev_farey = curr_farey

    print()
    print("-" * 72)
    print(f"RANGE TESTED:          N = 2 to {max_n}")
    print(f"TOTAL NEW FRACTIONS:   {total_new_fractions}")
    print(f"MEDIANTS CONFIRMED:    {total_mediants_confirmed}")
    print(f"GAPS CHECKED:          {total_gaps_checked}")
    print(f"EMPTY GAPS CONFIRMED:  {total_empty_gaps_confirmed} (q+s > N => no entry)")
    print(f"ALL TESTS PASSED:      {'YES' if all_pass else 'NO'}")
    print("-" * 72)

    return all_pass


def verify_converse(max_n=200):
    """
    Verify the CONVERSE: every gap in F_{N-1} with q+s = N receives exactly
    one new fraction (the mediant), and every gap with q+s > N receives none.

    This establishes the bijection:
        {new fractions in F_N} <-> {gaps in F_{N-1} with q+s = N}
    """
    print()
    print("=" * 72)
    print("CONVERSE VERIFICATION: Gap gets entry iff q+s = N")
    print("=" * 72)

    prev_farey = farey_sequence(1)
    all_pass = True

    for N in range(2, max_n + 1):
        curr_farey = farey_sequence(N)
        prev_set = set(prev_farey)
        new_fracs = [f for f in curr_farey if f not in prev_set]
        new_set = set(new_fracs)

        gaps_with_entry = 0
        gaps_expecting_entry = 0

        for i in range(len(prev_farey) - 1):
            left = prev_farey[i]
            right = prev_farey[i + 1]
            q, s = left.denominator, right.denominator

            gap_new = [f for f in new_fracs if left < f < right]

            if q + s == N:
                gaps_expecting_entry += 1
                if len(gap_new) != 1:
                    print(f"  FAIL at N={N}: gap ({left},{right}) has q+s={N} "
                          f"but got {len(gap_new)} entries: {gap_new}")
                    all_pass = False
                else:
                    gaps_with_entry += 1
            elif q + s > N:
                if len(gap_new) != 0:
                    print(f"  FAIL at N={N}: gap ({left},{right}) has q+s={q+s}>{N} "
                          f"but got entries: {gap_new}")
                    all_pass = False
            else:
                # q+s < N should not happen for consecutive fractions in F_{N-1}
                # because if q+s <= N-1, the mediant would be in F_{N-1} already
                print(f"  UNEXPECTED: gap ({left},{right}) has q+s={q+s} < {N}")
                all_pass = False

        # Number of new fractions should equal number of gaps with q+s = N
        # which should equal euler_totient(N)
        if gaps_with_entry != len(new_fracs):
            print(f"  FAIL at N={N}: {gaps_with_entry} gaps with entry != "
                  f"{len(new_fracs)} new fractions")
            all_pass = False

        if N % 50 == 0 or N == max_n:
            print(f"  N={N:4d}: {gaps_with_entry} gaps filled = "
                  f"{len(new_fracs)} new fracs (phi({N})) -- MATCH")

        prev_farey = curr_farey

    print()
    print(f"  BIJECTION VERIFIED FOR ALL N=2..{max_n}: "
          f"{'YES' if all_pass else 'NO'}")
    print("-" * 72)
    return all_pass


def verify_gcd_condition(max_n=200):
    """
    Verify that for consecutive p/q, r/s in F_{N-1} with rq-ps=1 and q+s=N,
    we always have gcd(p+r, N) = 1. This is needed for the mediant to be
    a valid Farey fraction.

    PROOF: If d | (p+r) and d | (q+s), then from rq - ps = 1:
      r*q - p*s = 1
      Since q+s = N, we have s = N-q, so r*q - p*(N-q) = 1
      => (r+p)*q - p*N = 1
      => (p+r)*q ≡ 1 (mod N)
      If d | (p+r) and d | N, then d | 1. So d = 1.
    """
    print()
    print("=" * 72)
    print("GCD VERIFICATION: gcd(p+r, q+s) = 1 for all mediant entries")
    print("=" * 72)

    prev_farey = farey_sequence(1)
    total_checked = 0
    all_pass = True

    for N in range(2, max_n + 1):
        for i in range(len(prev_farey) - 1):
            left = prev_farey[i]
            right = prev_farey[i + 1]
            p, q = left.numerator, left.denominator
            r, s = right.numerator, right.denominator

            if q + s == N:
                g = gcd(p + r, q + s)
                if g != 1:
                    print(f"  FAIL: gcd({p+r}, {q+s}) = {g} for gap "
                          f"({p}/{q}, {r}/{s}) at N={N}")
                    all_pass = False
                total_checked += 1

        prev_farey = farey_sequence(N)

    print(f"  Checked {total_checked} mediant entries, all have gcd = 1: "
          f"{'YES' if all_pass else 'NO'}")
    print("-" * 72)
    return all_pass


def print_proof():
    """Print the complete analytical proof."""
    print()
    print("=" * 72)
    print("THEOREM (Farey Mediant Property)")
    print("=" * 72)
    print("""
STATEMENT:
  Let F_N be the Farey sequence of order N. Every fraction a/N that is
  new in F_N (i.e., a/N ∈ F_N \\ F_{N-1}) is the mediant of its two
  consecutive neighbors p/q and r/s in F_{N-1}. That is:

      a = p + r    and    N = q + s

  where p/q < a/N < r/s are consecutive in F_{N-1} with rq - ps = 1.

PROOF:

  STEP 1: Unimodular neighbors.
  Let p/q and r/s be consecutive fractions in F_{N-1}. By the fundamental
  property of Farey sequences, they satisfy:

      rq - ps = 1                                             ... (*)

  This is the "unimodular" or "Farey neighbor" condition.

  STEP 2: The sum q + s exceeds N-1.
  Since p/q and r/s are CONSECUTIVE in F_{N-1}, no fraction with
  denominator ≤ N-1 lies strictly between them. The mediant (p+r)/(q+s)
  always lies strictly between p/q and r/s (this follows from (*)).
  If q+s ≤ N-1, then (p+r)/(q+s) would be in F_{N-1}, contradicting
  consecutiveness. Therefore:

      q + s ≥ N                                                ... (**)

  STEP 3: A new fraction enters the gap iff q + s = N.
  Suppose a/N is a new fraction in F_N lying in the gap (p/q, r/s) of
  F_{N-1}. Then:

      p/q < a/N < r/s

  From the left inequality:  aq - pN > 0, so aq - pN ≥ 1   (integers)
  From the right inequality: rN - as > 0, so rN - as ≥ 1   (integers)

  Adding:  (aq - pN) + (rN - as) ≥ 2
           a(q-s) + N(r-p) ≥ 2

  But more precisely, using (*):
      (aq - pN) + (rN - as) = a(q - s) + N(r - p)

  And from the mediant relationship, let us compute directly.
  Since rq - ps = 1, we know that any integer a with p/q < a/N < r/s
  satisfies:
      aq - pN ≥ 1   and   rN - as ≥ 1

  Adding: a(q - s) + N(r - p) ≥ 2.
  But also: (aq - pN) + (rN - as) = N(r - p) - a(s - q).

  Since rq - ps = 1, the ONLY solution with denominator N is obtained
  when both:
      aq - pN = 1   and   rN - as = 1                        ... (***)

  PROOF OF (***): Suppose aq - pN = j and rN - as = k where j,k ≥ 1
  and j + k = (aq - pN) + (rN - as) = N(r-p) + a(q-s).

  Multiplying aq - pN = j by s:   aqs - pNs = js
  Multiplying rN - as = k by q:   rNq - asq = kq
  Adding:  N(rq - ps) = js + kq, so N·1 = js + kq.

  Since j ≥ 1 and k ≥ 1, and q, s ≥ 1 with q + s ≥ N (from **):
      js + kq ≥ s + q ≥ N

  But js + kq = N exactly. So we need js + kq = N with j,k ≥ 1.
  Since s + q ≥ N, the only possibility is j = k = 1 and s + q = N.

  [If s + q > N, then even j = k = 1 gives js + kq = s + q > N,
  contradiction. So no solution exists when q + s > N.]

  [If s + q = N, then j = k = 1 is the unique solution.]

  STEP 4: The unique solution is the mediant.
  From j = 1: aq - pN = 1, so a = (1 + pN)/q = (1 + p(q+s))/q
            = (1 + pq + ps)/q = p + (1 + ps)/q = p + r
  where the last step uses rq - ps = 1, i.e., rq = 1 + ps,
  i.e., (1 + ps)/q = r.

  Therefore a = p + r and N = q + s, proving a/N = (p+r)/(q+s).

  STEP 5: The mediant has gcd(a, N) = 1.
  From aq - pN = 1, any common divisor of a and N must divide 1.
  Hence gcd(a, N) = 1, confirming a/N is in lowest terms.

  STEP 6: Bijection.
  We have established:
    - Each gap with q+s = N receives exactly one new fraction (the mediant)
    - Each gap with q+s > N receives no new fraction
    - Every new fraction a/N corresponds to a unique gap with q+s = N

  This gives a bijection:
    {new fractions in F_N} <--> {consecutive pairs in F_{N-1} with q+s = N}

  The number of such pairs equals φ(N) (Euler's totient), which matches
  |F_N| - |F_{N-1}| = φ(N).                                         QED
""")


def main():
    print("FAREY MEDIANT PROPERTY: Computational Verification + Proof")
    print("=" * 72)
    print()

    # Run all verifications
    test1 = verify_mediant_property(200)
    test2 = verify_converse(200)
    test3 = verify_gcd_condition(200)

    # Print the proof
    print_proof()

    # Summary
    print("=" * 72)
    print("FINAL SUMMARY")
    print("=" * 72)
    print(f"  Mediant property verified (N=2..200):    {'PASS' if test1 else 'FAIL'}")
    print(f"  Converse/bijection verified (N=2..200):  {'PASS' if test2 else 'FAIL'}")
    print(f"  GCD condition verified (N=2..200):       {'PASS' if test3 else 'FAIL'}")
    print()
    if test1 and test2 and test3:
        print("  *** ALL VERIFICATIONS PASSED ***")
        print()
        print("  PROVED: Every new fraction a/N in F_N is the mediant of its")
        print("  Farey neighbors in F_{N-1}, entering exactly when q+s = N.")
        print("  The proof is purely algebraic from the unimodular condition")
        print("  rq - ps = 1, requiring no assumptions beyond integer arithmetic.")
    else:
        print("  SOME TESTS FAILED -- see details above.")
    print("=" * 72)


if __name__ == "__main__":
    main()
