#!/usr/bin/env python3
"""
Fast version: only up to p=179 (skip 271, 311, 379, 389, 431 which are slow).
Focus on understanding the structure for the proof.
"""

from fractions import Fraction
from math import gcd

def mertens_table(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime = [True] * (limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for pp in primes:
            if i * pp > limit:
                break
            is_prime[i * pp] = False
            if i % pp == 0:
                mu[i * pp] = 0
                break
            else:
                mu[i * pp] = -mu[i]
    M = [0] * (limit + 1)
    for n in range(1, limit + 1):
        M[n] = M[n-1] + mu[n]
    return M, mu

def farey_sequence(N):
    fracs = []
    for b in range(2, N + 1):
        for a in range(1, b):
            if gcd(a, b) == 1:
                fracs.append(Fraction(a, b))
    fracs.sort()
    return fracs

def delta_p_frac(a, b, p):
    u = b - a
    pu_mod_b = (p * u) % b
    if pu_mod_b == 0:
        pu_mod_b = b
    return Fraction(pu_mod_b - u, b)

def compute_S(f, m):
    count = 0
    for j in range(1, m + 1):
        for i in range(1, j + 1):
            if Fraction(i, j) <= f:
                count += 1
    return Fraction(m * (m + 1), 2) * f - count

def main():
    M_big, _ = mertens_table(200)
    
    mp3_primes = [p for p in range(2, 180) if M_big[p] == -3 
                  and all(p % d != 0 for d in range(2, int(p**0.5)+1)) and p > 1]
    
    print(f"Testing M(p)=-3 primes up to 179: {mp3_primes}")
    
    for p in mp3_primes:
        N = p - 1
        fs = farey_sequence(N)
        
        deltas = {}
        for f in fs:
            a, b = f.numerator, f.denominator
            deltas[f] = delta_p_frac(a, b, p)
        
        Cp = sum(d*d for d in deltas.values())
        
        # Abel coefficients
        coeffs = {}
        coeffs[1] = -M_big[N // 2]
        for m in range(2, N + 1):
            am = M_big[N // m] - M_big[N // (m + 1)]
            if am != 0:
                coeffs[m] = am
        
        # Compute Term2 using all needed kernels
        term2 = Fraction(0)
        for m, c in coeffs.items():
            km = sum(compute_S(f, m) * deltas[f] for f in fs)
            term2 += c * km
        
        ratio = float(term2/Cp)
        status = "PASS" if term2 < 0 else "FAIL"
        
        # Also: what is c_1 and what determines its sign?
        c1 = coeffs[1]
        # M(N/2) for N = p-1
        MN2 = M_big[N // 2]
        
        print(f"  p={p}: c_1={c1}, M(N/2)={MN2}, Term2/C'={ratio:.6f} [{status}]")
        print(f"    coeffs: {dict(sorted(coeffs.items()))}")

if __name__ == "__main__":
    main()
