#!/usr/bin/env python3
"""
INDEPENDENT VERIFICATION of the claimed identity:

For prime p >= 5, N = p-1, Farey sequence F_N:
  Σ_{a/b ∈ F_N, b>1} (a/b)·δ(a/b) = (1/2)·Σ_{a/b ∈ F_N, b>1} δ(a/b)²

where δ(a/b) = (a - (p·a mod b)) / b

We verify:
1. Algebra of steps 1-3
2. Permutation property in step 4
3. Numerical check for multiple primes
4. Counterexample search for composite N
5. Check if identity holds for ALL N or only N = p-1
"""

from fractions import Fraction
from math import gcd
import sys

def farey_sequence(N):
    """Generate Farey sequence F_N: all a/b with 0 <= a <= b <= N, gcd(a,b)=1, b >= 1."""
    fracs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    return fracs

def verify_algebra():
    """Step 1-3: Independent re-derivation of the algebra."""
    print("=" * 70)
    print("STEP 1-3: ALGEBRAIC VERIFICATION")
    print("=" * 70)

    print("""
Let x = a/b and let f = {p*a mod b}/b (the fractional part proxy).
Then δ = x - f = a/b - (p*a mod b)/b.

Step 1: δ = x - f
  => x·δ = x·(x - f) = x² - x·f   ✓ (trivial)

Step 2: δ² = (x - f)² = x² - 2·x·f + f²   ✓ (trivial)

Step 3: x·δ - δ²/2
  = (x² - x·f) - (x² - 2·x·f + f²)/2
  = x² - x·f - x²/2 + x·f - f²/2
  = x²/2 - f²/2
  = (x² - f²)/2   ✓

So the claim reduces to: Σ (x² - f²) = 0 for all x = a/b in F_N with b > 1.

This means: Σ_{b=2}^{N} Σ_{a: gcd(a,b)=1, 0≤a≤b} [(a/b)² - ((p·a mod b)/b)²] = 0

CRITICAL CHECK: The sum includes a=0 and a=b.
  - a=0: x=0, f = (p·0 mod b)/b = 0, so x²-f² = 0. No contribution.
  - a=b: x=1, f = (p·b mod b)/b = 0, so x²-f² = 1. This DOES contribute!

Wait — is a=b even in the Farey sequence? a/b with a=b gives 1/1, 2/2, etc.
Only 1/1 has gcd(a,b)=1 when a=b. And 1/1 has b=1, so it's excluded by b>1.

For b>1 and a=b: gcd(b,b)=b>1, so these are excluded. Good.

So the sum is over a/b with 0 < a < b, gcd(a,b)=1, b >= 2, PLUS a=0/b for each b.
Actually a=0: gcd(0,b)=b, so 0/b is only in F_N as 0/1 (b=1), excluded.

So effectively: a ranges over {1, 2, ..., b-1} with gcd(a,b)=1, for each b from 2 to N.
""")
    return True

def verify_permutation(p, b):
    """Step 4: Check if a -> (p*a mod b) is a permutation of coprime residues mod b."""
    if gcd(p, b) != 1:
        return False, "gcd(p,b) != 1"

    coprimes = [a for a in range(1, b) if gcd(a, b) == 1]
    mapped = [(p * a) % b for a in coprimes]
    mapped_sorted = sorted(mapped)
    coprimes_sorted = sorted(coprimes)

    is_perm = mapped_sorted == coprimes_sorted
    return is_perm, f"coprimes={coprimes}, mapped={mapped}"

def verify_permutation_all(p, N):
    """Check permutation property for all b from 2 to N."""
    print(f"\n{'='*70}")
    print(f"STEP 4: PERMUTATION CHECK for p={p}, N={N}")
    print(f"{'='*70}")

    all_ok = True
    failures = []
    for b in range(2, N+1):
        if gcd(p, b) == 1:
            is_perm, detail = verify_permutation(p, b)
            if not is_perm:
                all_ok = False
                failures.append((b, detail))
        else:
            # gcd(p,b) > 1: the map a -> pa mod b does NOT permute coprimes
            # But when N = p-1, we have b <= p-1, so b < p, hence gcd(p,b)=1 always
            # (since p is prime). This is fine.
            # For composite N, this could fail!
            pass

    if all_ok:
        print(f"  All permutation checks PASSED for b=2..{N} with gcd(p,b)=1")
    else:
        print(f"  FAILURES: {failures}")

    return all_ok

def verify_squared_sum_equality(p, b):
    """For fixed b with gcd(p,b)=1, check Σ (a/b)² = Σ ((pa mod b)/b)²."""
    if gcd(p, b) != 1:
        return None  # not applicable

    coprimes = [a for a in range(1, b) if gcd(a, b) == 1]

    lhs = sum(Fraction(a, b)**2 for a in coprimes)
    rhs = sum(Fraction((p * a) % b, b)**2 for a in coprimes)

    return lhs == rhs, lhs, rhs

def compute_identity_both_sides(p, N):
    """Compute both sides of the identity using exact Fraction arithmetic."""
    fracs = []
    for b in range(2, N+1):
        for a in range(1, b):
            if gcd(a, b) == 1:
                fracs.append((a, b))

    lhs = Fraction(0)  # Σ x·δ
    rhs = Fraction(0)  # (1/2)·Σ δ²

    for a, b in fracs:
        x = Fraction(a, b)
        pa_mod_b = (p * a) % b
        f = Fraction(pa_mod_b, b)
        delta = x - f

        lhs += x * delta
        rhs += delta * delta

    rhs = rhs / 2

    return lhs, rhs, lhs == rhs

def main():
    # ---- Algebra check ----
    verify_algebra()

    # ---- Permutation + squared sum checks ----
    test_primes = [5, 7, 11, 13, 23, 37, 53, 97, 149, 199]

    print(f"\n{'='*70}")
    print("NUMERICAL VERIFICATION: Σ x·δ = (1/2)·Σ δ²")
    print(f"{'='*70}")
    print(f"{'p':>6} {'N':>6} {'LHS':>30} {'RHS':>30} {'Match':>8}")
    print("-" * 82)

    for p in test_primes:
        N = p - 1
        lhs, rhs, match = compute_identity_both_sides(p, N)
        print(f"{p:>6} {N:>6} {str(lhs):>30} {str(rhs):>30} {'YES' if match else '**NO**':>8}")

        # Also verify permutation
        verify_permutation_all(p, N)

        # Verify squared-sum equality for each b
        all_sq_ok = True
        for b in range(2, N+1):
            if gcd(p, b) == 1:
                result = verify_squared_sum_equality(p, b)
                if result is not None and not result[0]:
                    all_sq_ok = False
                    print(f"  SQUARED SUM FAIL at b={b}: {result[1]} vs {result[2]}")
        if all_sq_ok:
            print(f"  Squared-sum equality holds for all b=2..{N}")

    # ---- COUNTEREXAMPLE SEARCH ----
    print(f"\n{'='*70}")
    print("COUNTEREXAMPLE SEARCH: Does the identity hold for ALL N, or only N=p-1?")
    print(f"{'='*70}")

    # Test with various p and N != p-1
    print(f"\n--- Testing p fixed, varying N ---")
    print(f"{'p':>6} {'N':>6} {'LHS':>30} {'RHS':>30} {'Match':>8} {'Note':>20}")
    print("-" * 100)

    for p in [7, 11, 13, 23]:
        for N in range(2, 3*p):
            lhs, rhs, match = compute_identity_both_sides(p, N)
            note = ""
            if N == p - 1:
                note = "N=p-1"
            elif N == p:
                note = "N=p"
            elif N == p + 1:
                note = "N=p+1"
            elif N % p == 0:
                note = f"p|N"

            # Only print if match or if it's a notable case
            if not match or note:
                print(f"{p:>6} {N:>6} {str(lhs):>30} {str(rhs):>30} {'YES' if match else '**NO**':>8} {note:>20}")

    # ---- Test composite N specifically ----
    print(f"\n--- Composite N where gcd(p,b) > 1 can occur ---")
    print(f"{'p':>6} {'N':>6} {'LHS':>30} {'RHS':>30} {'Match':>8} {'b with gcd>1':>20}")
    print("-" * 100)

    for p in [5, 7, 11, 13]:
        for N in [p, p+1, p+2, 2*p, 2*p+1, 3*p]:
            lhs, rhs, match = compute_identity_both_sides(p, N)
            bad_bs = [b for b in range(2, N+1) if gcd(p, b) > 1]
            print(f"{p:>6} {N:>6} {str(lhs):>30} {str(rhs):>30} {'YES' if match else '**NO**':>8} {str(bad_bs[:5]):>20}")

    # ---- Check: does identity hold for ALL N regardless of p? ----
    print(f"\n--- Systematic: all (p, N) with p prime, 2 <= N <= 40 ---")
    small_primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    counterexamples = []
    matches_nonstandard = []

    for p in small_primes:
        for N in range(2, 41):
            lhs, rhs, match = compute_identity_both_sides(p, N)
            if not match:
                counterexamples.append((p, N, lhs, rhs))
            elif N != p - 1:
                matches_nonstandard.append((p, N))

    print(f"\nTotal counterexamples found: {len(counterexamples)}")
    if counterexamples:
        print("First 20 counterexamples:")
        for p, N, lhs, rhs in counterexamples[:20]:
            print(f"  p={p}, N={N}: LHS={lhs}, RHS={rhs}, diff={lhs-rhs}")

    print(f"\nNon-standard matches (N != p-1 but identity holds): {len(matches_nonstandard)}")
    if matches_nonstandard:
        for p, N in matches_nonstandard[:30]:
            print(f"  p={p}, N={N}")

    # ---- Edge case: what about N > p? Then b=p is in the sum, and gcd(p,p)=p ----
    # For b=p: the coprime residues mod p are {1,...,p-1}
    # Map a -> pa mod p = 0 for all a. So f=0 for all, and δ=a/p.
    # Wait, pa mod p = 0. So mapped values are all 0, NOT a permutation of {1,...,p-1}.
    # The sum Σ(a/p)² - Σ(0)² = Σ(a/p)² ≠ 0.
    # This should BREAK the identity when N >= p.

    print(f"\n{'='*70}")
    print("CRITICAL EDGE CASE: b = p (when N >= p)")
    print(f"{'='*70}")
    print("When b=p: pa mod p = 0 for all a. Map is NOT a permutation.")
    print("The squared-sum difference for b=p:")
    for p in [5, 7, 11]:
        coprimes_p = [a for a in range(1, p) if gcd(a, p) == 1]  # all of {1,...,p-1}
        sum_sq = sum(Fraction(a, p)**2 for a in coprimes_p)
        print(f"  p={p}: Σ(a/p)² for a=1..{p-1} = {sum_sq} = {float(sum_sq):.6f}")
        print(f"         Σ(0)² = 0")
        print(f"         Difference = {sum_sq} (nonzero!)")

    # ---- FINAL: Does the identity hold for p=composite (not prime)? ----
    print(f"\n{'='*70}")
    print("TEST: p composite (not prime)")
    print(f"{'='*70}")
    composites = [4, 6, 8, 9, 10, 12, 15, 20, 21, 25]
    print(f"{'p':>6} {'N':>6} {'LHS':>30} {'RHS':>30} {'Match':>8}")
    print("-" * 82)
    for p in composites:
        N = p - 1
        lhs, rhs, match = compute_identity_both_sides(p, N)
        print(f"{p:>6} {N:>6} {str(lhs):>30} {str(rhs):>30} {'YES' if match else '**NO**':>8}")

    # Also test: p composite, N arbitrary
    print(f"\n--- p composite, N arbitrary ---")
    comp_counterex = []
    comp_matches = []
    for p in composites:
        for N in range(2, 30):
            lhs, rhs, match = compute_identity_both_sides(p, N)
            if match:
                comp_matches.append((p, N))
            else:
                comp_counterex.append((p, N, lhs-rhs))

    print(f"Matches with composite p: {len(comp_matches)}")
    for p, N in comp_matches[:30]:
        print(f"  p={p}, N={N}")
    print(f"Counterexamples with composite p: {len(comp_counterex)}")

if __name__ == "__main__":
    main()
