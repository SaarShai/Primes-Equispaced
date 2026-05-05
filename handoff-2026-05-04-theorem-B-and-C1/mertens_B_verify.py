"""
Verify B(p) > 0 for primes p with M(p) <= -3, using primary Lean definition.

B(p) = 2 * sum_{f in F_{p-1}} D(f) * delta(f)
D(f) = rank(f, F_{p-1}) - n * f       [n = |F_{p-1}|]
delta(f) = f - {p*f}

Mertens M(p) = sum_{k<=p} mu(k)
"""
from fractions import Fraction
from math import gcd
from sympy import mobius, primerange, isprime
import sys

def farey_set(N):
    """Returns sorted list of fractions a/b with 1<=b<=N, 0<=a<=b, gcd(a,b)=1.
    Lean fareySet (p-1) per CrossTermPositive: pairs (a,b) with a in 0..b, b in 1..(p-1), gcd=1.
    Sorted by value of a/b. Includes 0/1 and 1/1.
    """
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add((a, b))
    # sort by value
    sorted_fracs = sorted(fracs, key=lambda ab: Fraction(ab[0], ab[1]))
    return sorted_fracs

def cross_term(p):
    """Compute B(p) per Lean definition exactly."""
    N = p - 1
    fs = farey_set(N)
    n = len(fs)
    total = Fraction(0)
    for rank0, (a, b) in enumerate(fs):
        f = Fraction(a, b)
        rank1 = rank0 + 1  # 1-based rank in Lean (rank+0..n, since fareyRank uses 1-based)
        # Actually per Lean: fareyRank N f = card { (a',b') in fareySet N : a'/b' <= f }.
        # If f is in the set, rank1 = position counting from 1. Let me check:
        # fareyRank counts elements <= f. The smallest is 0/1; rank(0/1)=1. Largest is 1/1; rank=n.
        D = Fraction(rank1) - Fraction(n) * f
        # delta(f) = f - frac(p*f)
        pf = Fraction(p) * f
        frac_pf = pf - int(pf) if pf >= 0 else pf - (int(pf) - 1 if pf != int(pf) else int(pf))
        # Standard: Int.fract(x) = x - floor(x), in [0,1)
        floor_pf = pf.numerator // pf.denominator if pf.denominator > 0 else int(pf)
        frac_pf = pf - floor_pf
        delta = f - frac_pf
        total += D * delta
    return 2 * total

def mertens(n):
    return sum(int(mobius(k)) for k in range(1, n + 1))

if __name__ == "__main__":
    # Sanity: B(11) should equal -55/36 per Lean docstring.
    B11 = cross_term(11)
    print(f"B(11) = {B11} (expected -55/36 = {Fraction(-55,36)})")
    assert B11 == Fraction(-55, 36), f"MISMATCH: got {B11}"
    print("B(11) matches Lean exactly.")
    B5 = cross_term(5)
    print(f"B(5) = {B5} (expected -2/9)")
    assert B5 == Fraction(-2, 9)
    B13 = cross_term(13)
    print(f"B(13) = {B13} (expected 271/385)")
    assert B13 == Fraction(271, 385)
    B19 = cross_term(19)
    print(f"B(19) = {B19} (expected 2905619/680680)")
    assert B19 == Fraction(2905619, 680680)
    print("All Lean cross-checks pass.")
