#!/usr/bin/env python3
"""q-block decomposition with proper index handling."""
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
    
    for p in [43, 47, 53, 71, 107]:
        N = p - 1
        fs = farey_sequence(N)
        deltas = {f: delta_p_frac(f.numerator, f.denominator, p) for f in fs}
        Cp = sum(d*d for d in deltas.values())
        
        # Compute K[0]=0, K[1]...K[N]
        K = {0: Fraction(0)}
        K[1] = sum(f * deltas[f] for f in fs)
        
        for m in range(1, N):
            j = m + 1
            inc = Fraction(0)
            for f in fs:
                jf = j * f
                frac_part = jf - int(jf)
                if frac_part < 0: frac_part += 1
                inc += frac_part * deltas[f]
            K[m+1] = K[m] + inc
        
        print(f"\np = {p}, N = {N}, M(p)={M_big[p]}")
        
        # q-block: contribution of q = M(q) * (K[floor(N/q)] - K[floor(N/(q+1))])
        # But we need to be careful: the Abel sum is over m=1..N-1
        # with q = floor(N/(m+1)), so m+1 ranges 2..N.
        # q = floor(N/(m+1)) for m+1 in {2,...,N}
        # For each q >= 1, m+1 ranges over {i: floor(N/i)=q}
        # = {i: N/(q+1) < i <= N/q}
        # = {floor(N/(q+1))+1, ..., floor(N/q)}
        # Then m ranges over {floor(N/(q+1)), ..., floor(N/q)-1}
        # DeltaK telescopes: K[floor(N/q)] - K[floor(N/(q+1))]
        
        total = Fraction(0)
        q1_contrib = None
        neg_contrib = Fraction(0)
        
        seen_q = set()
        for q in range(1, N + 1):
            end_m1 = N // q        # largest m+1 with floor(N/(m+1))=q
            start_m1 = N // (q+1)  # floor(N/(q+1))
            if start_m1 >= end_m1:
                continue
            if q in seen_q:
                continue
            seen_q.add(q)
            
            # Block: m goes from start_m1 to end_m1-1
            # Telescope: K[end_m1] - K[start_m1]
            if end_m1 not in K or start_m1 not in K:
                continue
            
            Mq = M_big[q]
            block_dk = K[end_m1] - K[start_m1]
            contrib = Mq * block_dk
            total += contrib
            
            if q == 1:
                q1_contrib = contrib
            if Mq < 0:
                neg_contrib += contrib
            
            if block_dk != 0 and abs(float(contrib/Cp)) > 0.0005:
                print(f"  q={q:>3}: M(q)={Mq:>3}, block=[K_{end_m1}-K_{start_m1}], "
                      f"DK/C'={float(block_dk/Cp):>9.4f}, contrib/C'={float(contrib/Cp):>9.4f}")
        
        print(f"  TOTAL Term2/C' = {float(total/Cp):.6f}")
        if q1_contrib is not None:
            print(f"  q=1 contrib / C' = {float(q1_contrib/Cp):.6f} (positive)")
            print(f"  M<0 contrib / C' = {float(neg_contrib/Cp):.6f} (negative)")
            print(f"  q=1 fraction of |Term2|: {abs(float(q1_contrib/total)):.2f}")

if __name__ == "__main__":
    main()
