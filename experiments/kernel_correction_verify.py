#!/usr/bin/env python3
"""
Exact arithmetic verification of the kernel correction decomposition
for primes p with M(p) = -3.

Key: delta_p(a/b) = ([p*(b-a)]_b - (b-a)) / b
where [x]_b = x mod b (least positive residue).

This is the modular displacement: how much does multiplication by p 
shift the complement (b-a) modulo b.

Kernels: K_m(p) = sum_{f in F_N^*} S(f,m) * delta_p(f)
C' = sum_{f in F_N^*} delta_p(f)^2

Term2(p) = -M(floor(N/2)) * K_1 + sum_{m>=2} a_m * K_m
where a_m = M(floor(N/m)) - M(floor(N/(m+1))), N = p-1.
"""

from fractions import Fraction
from math import gcd
import sys

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
    """Interior Farey: 0 < a/b < 1, b <= N, gcd(a,b) = 1."""
    fracs = []
    for b in range(2, N + 1):
        for a in range(1, b):
            if gcd(a, b) == 1:
                fracs.append(Fraction(a, b))
    fracs.sort()
    return fracs

def delta_p_frac(a, b, p):
    """
    delta_p(a/b) = ([p*(b-a)] mod b - (b-a)) / b
    
    For a/b in F_N^*, b >= 2, 0 < a < b, gcd(a,b) = 1.
    """
    u = b - a  # complement
    pu_mod_b = (p * u) % b
    if pu_mod_b == 0:
        pu_mod_b = b  # least positive residue
    return Fraction(pu_mod_b - u, b)

def compute_S(f, m):
    """
    S(f,m) = m(m+1)/2 * f - #{(i,j): 1<=i<=j<=m, i/j <= f}
    """
    count = 0
    for j in range(1, m + 1):
        for i in range(1, j + 1):
            if Fraction(i, j) <= f:
                count += 1
    return Fraction(m * (m + 1), 2) * f - count

def main():
    M_big, mu_big = mertens_table(500)
    
    # M(p) = -3 primes
    mp3_primes = [13, 19, 43, 47, 53, 71, 107, 131, 173, 179, 271, 311, 379, 389, 431]
    
    print("=" * 80)
    print("KERNEL CORRECTION PROOF: Exact Verification")
    print("Using delta_p(a/b) = ([p(b-a)] mod b - (b-a)) / b")
    print("=" * 80)
    
    # Verify M(p) values
    print("\n1. Verify M(p) = -3:")
    for p in mp3_primes:
        assert M_big[p] == -3, f"M({p}) = {M_big[p]}"
    print("   All confirmed M(p) = -3.")
    
    # Test primes
    test_primes = [43, 47, 53, 71]
    
    for p in test_primes:
        N = p - 1
        print(f"\n{'='*60}")
        print(f"p = {p}, N = {N}")
        print(f"{'='*60}")
        
        fs = farey_sequence(N)
        n_farey = len(fs)
        
        # Compute all deltas
        deltas = {}
        for f in fs:
            a, b = f.numerator, f.denominator
            deltas[f] = delta_p_frac(a, b, p)
        
        # Check basic properties
        sum_delta = sum(deltas.values())
        Cp = sum(d*d for d in deltas.values())
        
        print(f"   |F_N^*| = {n_farey}")
        print(f"   sum delta = {float(sum_delta):.6f}")
        print(f"   C' = {float(Cp):.10f}")
        
        # Verify delta_p(2/3)
        if Fraction(2,3) in deltas:
            print(f"   delta_p(2/3) = {deltas[Fraction(2,3)]} (p mod 3 = {p % 3})")
        
        # Compute K_1 = sum S(f,1) * delta(f) = sum f * delta(f)
        K1 = sum(f * deltas[f] for f in fs)
        print(f"   K_1 = {float(K1):.10f}")
        print(f"   C'/2 = {float(Cp/2):.10f}")
        print(f"   K_1 == C'/2: {K1 == Cp/2}")
        
        # If K_1 != C'/2, maybe S(f,1) is not just f
        # S(f,1) = 1*2/2 * f - #{1/1 <= f} = f - 0 = f for f < 1
        # So K_1 = sum f*delta(f). Let's check what C'/2 actually means here.
        
        # Compute K_2 from formula: K_2 = 3C'/2 - H_{[1/2,1)}
        H_half_1 = sum(deltas[f] for f in fs if f >= Fraction(1,2))
        K2_formula = 3*Cp/2 - H_half_1
        K2_direct = sum(compute_S(f, 2) * deltas[f] for f in fs)
        print(f"   K_2 (direct) = {float(K2_direct):.10f}")
        print(f"   K_2 (formula) = {float(K2_formula):.10f}")
        print(f"   K_2 match: {K2_direct == K2_formula}")
        
        # Compute all kernels K_1..K_9
        print(f"\n   Computing K_1..K_9:")
        kernels = {}
        for m in range(1, 10):
            km = sum(compute_S(f, m) * deltas[f] for f in fs)
            kernels[m] = km
            ratio = float(km / Cp) if Cp != 0 else float('inf')
            sign = "+" if km > 0 else ("-" if km < 0 else "0")
            print(f"   K_{m} = {float(km):.10f}  (K_{m}/C' = {ratio:.6f})  [{sign}]")
        
        # Compute Abel coefficients
        coeffs = {}
        c1 = -M_big[N // 2]
        coeffs[1] = c1
        for m in range(2, N + 1):
            am = M_big[N // m] - M_big[N // (m + 1)]
            if am != 0:
                coeffs[m] = am
        
        print(f"\n   Abel coefficients (non-zero):")
        for m in sorted(coeffs.keys()):
            if m <= 20:
                print(f"     c_{m} = {coeffs[m]}")
        
        # Compute Term2
        term2 = Fraction(0)
        for m, c in coeffs.items():
            if m in kernels:
                term2 += c * kernels[m]
            else:
                km = sum(compute_S(f, m) * deltas[f] for f in fs)
                kernels[m] = km
                term2 += c * km
        
        print(f"\n   Term2 = {float(term2):.12f}")
        print(f"   Term2/C' = {float(term2/Cp):.10f}")
        print(f"   Term2 < 0: {term2 < 0}")
        
        # Breakdown
        k1_part = coeffs.get(1, 0) * kernels.get(1, Fraction(0))
        k29_part = sum(coeffs.get(m, 0) * kernels.get(m, Fraction(0)) for m in range(2, 10))
        rest_part = sum(coeffs.get(m, 0) * kernels.get(m, Fraction(0)) 
                       for m in coeffs if m >= 10)
        print(f"   c_1 * K_1 = {float(k1_part):.10f}")
        print(f"   sum c_m*K_m (m=2..9) = {float(k29_part):.10f}")
        print(f"   sum c_m*K_m (m>=10) = {float(rest_part):.10f}")

if __name__ == "__main__":
    main()
