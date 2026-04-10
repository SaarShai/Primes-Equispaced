#!/usr/bin/env python3
"""q-block decomposition with CORRECT index range.

Abel sum: Term2 = sum_{m=1}^{N-1} M(floor(N/(m+1))) * (K_{m+1} - K_m)

m ranges 1..N-1, so m+1 ranges 2..N.
q = floor(N/(m+1)) ranges from floor(N/N)=1 to floor(N/2).

For each q, the m+1 values are {i: floor(N/i)=q, 2<=i<=N}
= {floor(N/(q+1))+1, ..., floor(N/q)} intersected with [2,N]

The block telescope gives K[min(floor(N/q),N)] - K[max(floor(N/(q+1)),1)]

But since m starts at 1, m+1 starts at 2, so start_m1 = max(floor(N/(q+1))+1, 2).
And end_m1 = min(floor(N/q), N).
Then DK = K[end_m1] - K[start_m1 - 1].
Wait, let me think more carefully.

If m+1 goes from a to b (inclusive), then:
  sum_{m+1=a}^{b} DeltaK_{m+1-1} = sum_{m=a-1}^{b-1} (K_{m+1} - K_m) = K[b] - K[a-1]

So for the q-block: m+1 in [start..end] where start = max(floor(N/(q+1))+1, 2), end = floor(N/q).
Block DK = K[end] - K[start-1].
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
    
    for p in [43, 47, 53, 71, 107]:
        N = p - 1
        fs = farey_sequence(N)
        deltas = {f: delta_p_frac(f.numerator, f.denominator, p) for f in fs}
        Cp = sum(d*d for d in deltas.values())
        
        K = {}
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
        
        # Direct computation of Term2 for verification
        term2_direct = Fraction(0)
        for m in range(1, N):
            Mval = M_big[N // (m+1)]
            dk = K[m+1] - K[m]
            term2_direct += Mval * dk
        
        print(f"\np = {p}, N = {N}")
        print(f"Term2/C' (direct Abel) = {float(term2_direct/Cp):.6f}")
        
        # q-block decomposition
        total_qblock = Fraction(0)
        
        seen = set()
        for q in range(1, N):
            if q in seen:
                continue
            
            end_m1 = min(N // q, N)
            start_m1 = max(N // (q + 1) + 1, 2)
            
            if start_m1 > end_m1:
                continue
            seen.add(q)
            
            # m+1 goes from start_m1 to end_m1
            # Telescope: K[end_m1] - K[start_m1 - 1]
            Mq = M_big[q]
            block_dk = K[end_m1] - K[start_m1 - 1]
            contrib = Mq * block_dk
            total_qblock += contrib
            
            if abs(float(contrib/Cp)) > 0.0005:
                print(f"  q={q:>3}: M={Mq:>3}, m+1 in [{start_m1},{end_m1}], "
                      f"DK/C'={float(block_dk/Cp):>8.4f}, contrib/C'={float(contrib/Cp):>9.4f}")
        
        print(f"  q-block TOTAL / C' = {float(total_qblock/Cp):.6f}")
        print(f"  Match: {total_qblock == term2_direct}")

if __name__ == "__main__":
    main()
