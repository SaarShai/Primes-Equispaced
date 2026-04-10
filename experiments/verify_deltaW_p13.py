#!/usr/bin/env python3
"""Verify ΔW and four-term decomposition at p=13."""
from fractions import Fraction
from math import gcd

def farey_sequence(N):
    fracs = set()
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a,b) == 1:
                fracs.add(Fraction(a,b))
    return sorted(fracs)

def wobble(F):
    """W = (1/n^2) * sum (j - n*f)^2"""
    n = len(F)
    return sum((Fraction(j) - n*f)**2 for j, f in enumerate(F)) / (n*n)

p = 13
N = p - 1
F_N = farey_sequence(N)
F_p = farey_sequence(p)
n = len(F_N)
n_prime = len(F_p)

W_old = wobble(F_N)
W_new = wobble(F_p)
delta_W = W_old - W_new

print(f"p = {p}, N = {N}")
print(f"|F_N| = {n}, |F_p| = {n_prime}")
print(f"W(p-1) = {float(W_old):.10f}")
print(f"W(p) = {float(W_new):.10f}")
print(f"ΔW = W(p-1) - W(p) = {float(delta_W):.10f}")
print(f"Sign: {'POSITIVE (healing)' if delta_W > 0 else 'NEGATIVE (worsening)'}")
print(f"n'^2 * ΔW = {float(n_prime**2 * delta_W):.10f}")

# Now compute four terms
# A = dilution = sum D_old^2 * (n'^2/n^2 - 1)
sum_D_old_sq = sum((Fraction(j) - n*f)**2 for j, f in enumerate(F_N))
A = sum_D_old_sq * (Fraction(n_prime**2 - n**2, n**2))

# B = 2*sum D*delta (interior)
B = Fraction(0)
for j, f in enumerate(F_N):
    if f.denominator <= 1: continue
    a, b = f.numerator, f.denominator
    D = Fraction(j) - n*f
    pa_mod_b = (p * a) % b
    delta = Fraction(a - pa_mod_b, b)
    B += 2 * D * delta

# C = sum delta^2 (interior)
C = Fraction(0)
for j, f in enumerate(F_N):
    if f.denominator <= 1: continue
    a, b = f.numerator, f.denominator
    pa_mod_b = (p * a) % b
    delta = Fraction(a - pa_mod_b, b)
    C += delta * delta

# D_new = sum of D_{F_p}(k/p)^2 for new fractions
D_new = Fraction(0)
for k in range(1, p):
    f = Fraction(k, p)
    # Find rank in F_p
    rank = sum(1 for g in F_p if g <= f) - 1  # 0-indexed
    D_fp = Fraction(rank) - n_prime * f
    D_new += D_fp**2

print(f"\nFour-term decomposition:")
print(f"A (dilution) = {float(A):.6f}")
print(f"B (cross)    = {float(B):.6f}")
print(f"C (shift)    = {float(C):.6f}")
print(f"D (new frac) = {float(D_new):.6f}")

print(f"\nA - B - C - D = {float(A - B - C - D_new):.6f}")
print(f"-A + B + C + D = {float(-A + B + C + D_new):.6f}")
print(f"n'^2 * ΔW = {float(n_prime**2 * delta_W):.6f}")

print(f"\nCheck: n'^2*ΔW vs A-B-C-D: {float(n_prime**2 * delta_W - (A - B - C - D_new)):.10f}")
print(f"Check: n'^2*ΔW vs -A+B+C+D: {float(n_prime**2 * delta_W - (-A + B + C + D_new)):.10f}")

# Also try with +1 correction
print(f"\nA - B - C - D + 1 = {float(A - B - C - D_new + 1):.6f}")
print(f"-A + B + C + D - 1 = {float(-A + B + C + D_new - 1):.6f}")
print(f"Check: n'^2*ΔW vs A-B-C-D+1: {float(n_prime**2 * delta_W - (A - B - C - D_new + 1)):.10f}")
print(f"Check: n'^2*ΔW vs -A+B+C+D-1: {float(n_prime**2 * delta_W - (-A + B + C + D_new - 1)):.10f}")

# Let me also compute D' and A' directly
D_prime = Fraction(0)
for j, f in enumerate(F_N):
    # D_{F_p}(f): displacement of old fraction f in F_p
    rank_in_Fp = sum(1 for g in F_p if g <= f) - 1  # 0-indexed
    D_fp = Fraction(rank_in_Fp) - n_prime * f
    D_prime += D_fp**2

A_prime = sum((Fraction(j) - n*f + delta_f)**2
              for j, f in zip(range(n), F_N)
              for delta_f in [Fraction(f.numerator - (p*f.numerator % f.denominator), f.denominator) if f.denominator > 1 else Fraction(0)])

# Actually that's wrong. Let me compute A' properly.
A_prime = Fraction(0)
for j, f in enumerate(F_N):
    D_old = Fraction(j) - n*f
    if f.denominator > 1:
        a, b = f.numerator, f.denominator
        delta = Fraction(a - (p*a % b), b)
    else:
        delta = Fraction(0) if f == 0 else Fraction(1)  # delta(1/1) = 1
    A_prime += (D_old + delta)**2

print(f"\nD' = {float(D_prime):.6f}")
print(f"A' = {float(A_prime):.6f}")
print(f"D' - A' = {float(D_prime - A_prime):.6f}")
print(f"Should be -1: {D_prime - A_prime == -1}")
