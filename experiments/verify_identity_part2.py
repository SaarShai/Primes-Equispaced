#!/usr/bin/env python3
"""
Part 2: Deeper analysis of WHEN the identity holds.
Key finding from part 1: identity holds for N < p (always), FAILS for N >= p.
Let's confirm this pattern and understand WHY.
"""

from fractions import Fraction
from math import gcd

def compute_identity_diff(p, N):
    """Return LHS - RHS = Σ x·δ - (1/2)·Σ δ²."""
    diff = Fraction(0)
    for b in range(2, N+1):
        for a in range(1, b):
            if gcd(a, b) == 1:
                x = Fraction(a, b)
                pa_mod_b = (p * a) % b
                f = Fraction(pa_mod_b, b)
                # x·δ - δ²/2 = (x² - f²)/2
                diff += (x**2 - f**2) / 2
    return diff

def compute_per_b_contribution(p, N):
    """Decompose the identity difference by denominator b."""
    contributions = {}
    for b in range(2, N+1):
        contrib = Fraction(0)
        for a in range(1, b):
            if gcd(a, b) == 1:
                x = Fraction(a, b)
                pa_mod_b = (p * a) % b
                f = Fraction(pa_mod_b, b)
                contrib += (x**2 - f**2) / 2
        contributions[b] = contrib
    return contributions

# Confirm: identity holds iff N < p
print("=" * 70)
print("PATTERN: Identity holds iff N < p?")
print("=" * 70)

primes = [5, 7, 11, 13, 17, 19, 23, 29, 31]
for p in primes:
    # Test N = p-2, p-1, p, p+1
    for N in [p-2, p-1, p, p+1]:
        if N < 2:
            continue
        diff = compute_identity_diff(p, N)
        status = "HOLDS" if diff == 0 else f"FAILS (diff={diff})"
        marker = " <-- N=p-1" if N == p-1 else (" <-- N=p" if N == p else "")
        print(f"  p={p}, N={N}: {status}{marker}")

# Decompose by b to see which b breaks it
print("\n" + "=" * 70)
print("PER-DENOMINATOR CONTRIBUTION when N = p")
print("=" * 70)
for p in [5, 7, 11, 13]:
    N = p
    contribs = compute_per_b_contribution(p, N)
    print(f"\np={p}, N={N}:")
    for b, c in sorted(contribs.items()):
        if c != 0:
            print(f"  b={b}: contribution = {c} = {float(c):.6f}")

# The contribution from b=p should be exactly what breaks it
print("\n" + "=" * 70)
print("CONTRIBUTION FROM b=p ALONE")
print("=" * 70)
print("When b=p: a -> pa mod p = 0 always (NOT a permutation)")
print("So Σ(x² - f²)/2 = Σ(a/p)²/2 for a in {1,...,p-1}")
for p in [5, 7, 11, 13, 17]:
    sum_sq = sum(Fraction(a, p)**2 for a in range(1, p))
    print(f"  p={p}: Σ(a/p)²/2 = {sum_sq/2} = (p-1)(2p-1)/(6p) = {(p-1)*(2*p-1)}/{6*p}")

# Check: the diff for N=p equals the b=p contribution
print("\n" + "=" * 70)
print("CONFIRM: diff(N=p) - diff(N=p-1) = contribution from b=p")
print("=" * 70)
for p in [5, 7, 11, 13, 17, 23]:
    diff_p = compute_identity_diff(p, p)
    diff_pm1 = compute_identity_diff(p, p-1)
    b_p_contrib = sum(Fraction(a, p)**2 for a in range(1, p)) / 2
    print(f"  p={p}: diff(p)={diff_p}, diff(p-1)={diff_pm1}, b=p contrib={b_p_contrib}")
    print(f"         diff(p) - diff(p-1) = {diff_p - diff_pm1}, b=p contrib = {b_p_contrib}")
    print(f"         Match: {diff_p - diff_pm1 == b_p_contrib}")

# BROADER: does identity hold for ALL N < p, not just N = p-1?
print("\n" + "=" * 70)
print("DOES IDENTITY HOLD FOR ALL N < p (not just N = p-1)?")
print("=" * 70)
all_hold = True
for p in [5, 7, 11, 13, 17, 19, 23]:
    for N in range(2, p):
        diff = compute_identity_diff(p, N)
        if diff != 0:
            print(f"  COUNTEREXAMPLE: p={p}, N={N}, diff={diff}")
            all_hold = False
if all_hold:
    print("  YES: Identity holds for ALL N < p (for all tested primes)")

# WHY does it hold for N < p?
print("\n" + "=" * 70)
print("WHY: For N < p, every b <= N < p, so gcd(p,b)=1 (p prime).")
print("Hence a -> pa mod b IS a permutation of coprime residues for each b.")
print("The squared-sum equality follows, and the identity holds.")
print("=" * 70)

# Check: does it hold for non-prime p when N < p and gcd(p,b)=1 for all b <= N?
print("\n" + "=" * 70)
print("NON-PRIME p: Does identity hold when gcd(p,b)=1 for all b <= N?")
print("=" * 70)
# For p=25 (not prime), N <= 4: all b in {2,3,4} are coprime to 25
for p in [4, 6, 8, 9, 10, 15, 25, 35, 49]:
    max_safe_N = 0
    for N in range(2, p):
        all_coprime = all(gcd(p, b) == 1 for b in range(2, N+1))
        if all_coprime:
            max_safe_N = N
    if max_safe_N >= 2:
        print(f"\n  p={p}: max N with all b coprime to p = {max_safe_N}")
        for N in range(2, min(max_safe_N + 3, p)):
            diff = compute_identity_diff(p, N)
            all_coprime = all(gcd(p, b) == 1 for b in range(2, N+1))
            print(f"    N={N}: diff={diff}, all coprime={all_coprime}, holds={diff==0}")

# FINAL: Is the identity actually equivalent to "gcd(p,b)=1 for all b <= N"?
print("\n" + "=" * 70)
print("FINAL TEST: Identity holds iff gcd(p,b)=1 for all b in 2..N?")
print("=" * 70)
exceptions = []
for p in range(3, 50):
    for N in range(2, min(p + 10, 60)):
        diff = compute_identity_diff(p, N)
        all_coprime = all(gcd(p, b) == 1 for b in range(2, N+1))
        holds = (diff == 0)
        if holds != all_coprime:
            exceptions.append((p, N, holds, all_coprime))

if exceptions:
    print(f"  Found {len(exceptions)} exceptions to the equivalence:")
    for p, N, holds, all_coprime in exceptions[:20]:
        print(f"    p={p}, N={N}: identity holds={holds}, all coprime={all_coprime}")
else:
    print("  CONFIRMED: For all tested (p, N), identity holds iff gcd(p,b)=1 for all b in {2,...,N}")
