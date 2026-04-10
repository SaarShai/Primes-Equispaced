#!/usr/bin/env python3
"""
q-block decomposition: Term2 = sum_q M(q) * (K_{end_q} - K_{start_q})

For each q = 1,2,...,N, the m-range is:
  m in (N/(q+1) - 1, N/q - 1]
  
The contribution is M(q) * (K_{N/q} - K_{N/(q+1)}).

Actually more precisely: for the Abel form
  Term2 = sum_{m=1}^{N-1} M(floor(N/(m+1))) * DeltaK_m

Group by q = floor(N/(m+1)). For fixed q:
  m+1 in [N/(q+1)+1, N/q]  (when floor(N/(m+1)) = q)
  so m ranges over [N/(q+1), N/q - 1]
  
The block contribution = M(q) * sum_{m in block} DeltaK_m 
= M(q) * (K_{N/q} - K_{N/(q+1)})

Wait, need to be more careful with floor.
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

def main():
    M_big, _ = mertens_table(200)
    
    for p in [43, 47, 53, 71, 107, 131]:
        N = p - 1
        fs = farey_sequence(N)
        deltas = {f: delta_p_frac(f.numerator, f.denominator, p) for f in fs}
        Cp = sum(d*d for d in deltas.values())
        
        # Compute ALL kernels incrementally
        K = [None]  # K[0] unused
        K.append(sum(f * deltas[f] for f in fs))  # K[1] = C'/2
        
        for m in range(1, N):
            j = m + 1
            inc = Fraction(0)
            for f in fs:
                jf = j * f
                frac_part = jf - int(jf)
                if frac_part < 0: frac_part += 1
                inc += frac_part * deltas[f]
            K.append(K[-1] + inc)
        
        # K[1]...K[N] are now all computed
        
        # q-block decomposition
        # For each q, find the m-range where floor(N/(m+1)) = q
        # m+1 ranges over values where floor(N/(m+1)) = q
        # i.e., m+1 in [floor(N/(q+1))+1 .. floor(N/q)]  (if q >= 1)
        # So the block goes from m_start = floor(N/(q+1)) to m_end = floor(N/q) - 1
        # And the telescoped kernel difference is K[m_end+1] - K[m_start]
        # = K[floor(N/q)] - K[floor(N/(q+1))]
        
        print(f"\np = {p}, N = {N}")
        print(f"{'q':>4} {'M(q)':>6} {'K_end/Cp':>10} {'K_start/Cp':>10} {'block_DK/Cp':>12} {'contrib/Cp':>12}")
        
        total = Fraction(0)
        for q in range(1, N + 1):
            end_idx = N // q
            start_idx = N // (q + 1)
            if start_idx >= end_idx:
                continue  # empty block
            if end_idx > N or start_idx < 0:
                continue
            
            Mq = M_big[q]
            block_dk = K[end_idx] - K[start_idx]
            contrib = Mq * block_dk
            total += contrib
            
            if block_dk != 0:
                print(f"{q:>4} {Mq:>6} {float(K[end_idx]/Cp):>10.4f} {float(K[start_idx]/Cp):>10.4f} "
                      f"{float(block_dk/Cp):>12.6f} {float(contrib/Cp):>12.6f}")
        
        print(f"{'':>4} {'':>6} {'':>10} {'':>10} {'Total:':>12} {float(total/Cp):>12.6f}")
        
        # Verify matches Term2
        # Also compute via coefficients
        coeffs = {}
        coeffs[1] = -M_big[N // 2]
        for m in range(2, N + 1):
            am = M_big[N // m] - M_big[N // (m + 1)]
            if am != 0: coeffs[m] = am
        term2_check = sum(coeffs.get(m, 0) * K[m] for m in range(1, N + 1))
        print(f"  Term2 via coefficients / C' = {float(term2_check/Cp):.6f}")

if __name__ == "__main__":
    main()
