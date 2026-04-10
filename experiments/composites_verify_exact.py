#!/usr/bin/env python3
"""
Verify borderline cases with exact Fraction arithmetic.
"""

from fractions import Fraction
from math import gcd


def farey_sequence(N):
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def compute_wobble_exact(fracs):
    n = len(fracs)
    if n <= 1:
        return Fraction(0)
    w = Fraction(0)
    for j, f in enumerate(fracs):
        delta = f - Fraction(j, n)
        w += delta * delta
    return w


# Check the borderline cases
cases = [4, 94, 121, 146, 166, 169, 214, 218, 219, 226, 285, 289]

for N in cases:
    print(f"Computing F_{N-1} and F_{N}...")
    F_prev = farey_sequence(N - 1)
    F_N = farey_sequence(N)
    W_prev = compute_wobble_exact(F_prev)
    W_N = compute_wobble_exact(F_N)
    dW = W_prev - W_N
    sign = "HEALS" if dW > 0 else ("ZERO" if dW == 0 else "NON-HEALING")
    print(f"  N={N}: |F_{N-1}|={len(F_prev)}, |F_{N}|={len(F_N)}")
    print(f"  DeltaW = {sign}: {float(dW):.15e}")
    print(f"  Exact: {dW}")
    print()
