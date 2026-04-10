#!/usr/bin/env python3
"""
Analyze K_m/C' vs m(m+1)/4 to understand why Term2 < 0.
"""
from fractions import Fraction
from math import gcd

def mertens_table(limit):
    mu = [0] * (limit + 1); mu[1] = 1
    is_prime = [True] * (limit + 1); primes = []
    for i in range(2, limit + 1):
        if is_prime[i]: primes.append(i); mu[i] = -1
        for pp in primes:
            if i * pp > limit: break
            is_prime[i * pp] = False
            if i % pp == 0: mu[i * pp] = 0; break
            else: mu[i * pp] = -mu[i]
    M = [0] * (limit + 1)
    for n in range(1, limit + 1): M[n] = M[n-1] + mu[n]
    return M, mu

def farey_sequence(N):
    fracs = []
    for b in range(2, N + 1):
        for a in range(1, b):
            if gcd(a, b) == 1: fracs.append(Fraction(a, b))
    fracs.sort()
    return fracs

def delta_p_frac(a, b, p):
    u = b - a
    pu_mod_b = (p * u) % b
    if pu_mod_b == 0: pu_mod_b = b
    return Fraction(pu_mod_b - u, b)

def compute_S(f, m):
    count = 0
    for j in range(1, m + 1):
        for i in range(1, j + 1):
            if Fraction(i, j) <= f: count += 1
    return Fraction(m * (m + 1), 2) * f - count

def main():
    M_big, _ = mertens_table(200)
    
    for p in [43, 71]:
        N = p - 1
        fs = farey_sequence(N)
        deltas = {}
        for f in fs:
            deltas[f] = delta_p_frac(f.numerator, f.denominator, p)
        Cp = sum(d*d for d in deltas.values())
        
        print(f"\np = {p}, N = {N}")
        hdr = 'K_m/Cp'
        print(f"{hdr:>12} {'m(m+1)/4':>12} {'ratio':>12} {'deficit':>12}")
        
        # Compute K_m for all m that appear as coefficients
        coeffs = {}
        coeffs[1] = -M_big[N // 2]
        for m in range(2, N + 1):
            am = M_big[N // m] - M_big[N // (m + 1)]
            if am != 0: coeffs[m] = am
        
        all_m = sorted(coeffs.keys())
        
        term2 = Fraction(0)
        for m in all_m:
            km = sum(compute_S(f, m) * deltas[f] for f in fs)
            km_ratio = float(km / Cp)
            approx = m * (m + 1) / 4
            c = coeffs[m]
            deficit = km_ratio - approx
            term2 += c * km
            print(f"{m:>4} {km_ratio:>12.4f} {approx:>12.4f} {km_ratio/approx if approx else 0:>12.4f} {deficit:>12.4f}  c={c}")
        
        print(f"\nTerm2/C' = {float(term2/Cp):.6f}")
        
        # Key: if K_m/C' < m(m+1)/4, that's a deficit.
        # The sign of Term2 depends on whether deficits dominate on positive-c terms
        # or on negative-c terms.

if __name__ == "__main__":
    main()
