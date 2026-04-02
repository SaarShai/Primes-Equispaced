"""Correct B+C verification — Session 11. Saved for Codex/Aristotle to use."""
from math import gcd
from fractions import Fraction

def farey(N):
    fs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a,b) == 1:
                fs.append((a,b))
    fs.sort(key=lambda ab: Fraction(ab[0], ab[1]))
    return fs

def verify_bc(p):
    fracs = farey(p-1)
    n = len(fracs)
    sDD, sd2 = Fraction(0), Fraction(0)
    for rank, (a,b) in enumerate(fracs):
        f = Fraction(a,b)
        D = rank - n * f
        pfrac = Fraction((p*a)%b, b)
        delta = f - pfrac
        sDD += D * delta
        sd2 += delta * delta
    bc = 2*sDD + sd2
    R = 2*sDD/sd2 if sd2 > 0 else None
    return {'p':p, 'B+C':bc, 'R':float(R), 'positive': bc>0}

# Key finding: B+C > 0 for all tested primes. Min R = -0.89 at p=11 (barely > -1).
# R can be negative but never reaches -1. Proof needs to show R > -1 always.
# At p=11: R=-0.89, B+C=0.42 (close call!)
