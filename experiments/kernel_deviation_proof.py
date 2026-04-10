#!/usr/bin/env python3
"""
Understand Term2 = C' * sum c_m * (K_m/C' - 1/2)

Since sum c_m = 0, we can subtract any constant from K_m/C'.
Let R_m = K_m/C'. Then Term2/C' = sum c_m * R_m.

Question: what is the pattern of R_m for the m values that matter?
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
    
    for p in [43, 47, 53, 71, 107]:
        N = p - 1
        fs = farey_sequence(N)
        deltas = {f: delta_p_frac(f.numerator, f.denominator, p) for f in fs}
        Cp = sum(d*d for d in deltas.values())
        
        coeffs = {}
        coeffs[1] = -M_big[N // 2]
        for m in range(2, N + 1):
            am = M_big[N // m] - M_big[N // (m + 1)]
            if am != 0: coeffs[m] = am
        
        print(f"\np = {p}, N = {N}")
        
        # For each non-zero coefficient, compute R_m = K_m/C'
        term2_over_Cp = Fraction(0)
        pos_sum = Fraction(0)  # sum of c_m * R_m for c_m > 0
        neg_sum = Fraction(0)  # sum of c_m * R_m for c_m < 0
        
        for m in sorted(coeffs.keys()):
            c = coeffs[m]
            km = sum(compute_S(f, m) * deltas[f] for f in fs)
            Rm = km / Cp
            contrib = c * Rm
            term2_over_Cp += contrib
            
            if c > 0:
                pos_sum += contrib
            else:
                neg_sum += contrib
            
            mtype = "+" if c > 0 else "-"
            print(f"  m={m:>3}: c={c:>3}, R_m={float(Rm):.6f}, c*R_m={float(contrib):.6f} [{mtype}]")
        
        print(f"  Positive contributions: {float(pos_sum):.6f}")
        print(f"  Negative contributions: {float(neg_sum):.6f}")
        print(f"  Term2/C' = {float(term2_over_Cp):.6f}")
        
        # Key question: among the m values with c_m != 0, 
        # do the positive-c terms hit SMALLER R_m values?
        pos_R = [float(sum(compute_S(f, m) * deltas[f] for f in fs) / Cp) 
                 for m in sorted(coeffs.keys()) if coeffs[m] > 0]
        neg_R = [float(sum(compute_S(f, m) * deltas[f] for f in fs) / Cp) 
                 for m in sorted(coeffs.keys()) if coeffs[m] < 0]
        
        print(f"  Mean R_m for pos c: {sum(pos_R)/len(pos_R):.4f}")
        print(f"  Mean R_m for neg c: {sum(neg_R)/len(neg_R):.4f}")

if __name__ == "__main__":
    main()
