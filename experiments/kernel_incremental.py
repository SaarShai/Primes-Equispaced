#!/usr/bin/env python3
"""
Fast incremental computation of all kernels.

Key: S(f, m+1) - S(f, m) = (m+1)f - #{i: 1<=i<=m+1, i/(m+1) <= f}
= (m+1)f - #{i: i <= (m+1)f, 1<=i<=m+1}
= (m+1)f - floor((m+1)f)  if (m+1)f is not integer
= (m+1)f - (m+1)f = 0    if (m+1)f is integer

Wait, more carefully: adding row j=m+1 to S(f,m):
S(f,m+1) - S(f,m) = sum_{i=1}^{m+1} [ i/(m+1) <= f ] * ((m+1)f - i/(m+1) ... no)

Actually S(f,m) = m(m+1)/2 * f - step_count_m(f).
S(f,m+1) = (m+1)(m+2)/2 * f - step_count_{m+1}(f).
S(f,m+1) - S(f,m) = (m+1)f - (step_count_{m+1}(f) - step_count_m(f)).

step_count_{m+1} - step_count_m = #{i: 1<=i<=m+1, i/(m+1) <= f}.

So Delta S_m(f) = (m+1)f - #{i: 1<=i<=m+1, i/(m+1) <= f}
= (m+1)f - floor((m+1)f)  = {(m+1)f} (fractional part)

Wait that's only if f is not of the form i/(m+1). If f = i/(m+1) exactly, then
i/(m+1) <= f counts i, so the count is floor((m+1)f) = i (including the boundary).
And (m+1)f - i = 0.

So Delta S_m(f) = {(m+1)f} = (m+1)f - floor((m+1)f).

Therefore:
K_{m+1} - K_m = sum_f {(m+1)f} * delta_p(f)

This is much faster to compute!
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
    M_big, _ = mertens_table(500)
    
    for p in [43, 71, 107, 131]:
        N = p - 1
        fs = farey_sequence(N)
        deltas = {f: delta_p_frac(f.numerator, f.denominator, p) for f in fs}
        Cp = sum(d*d for d in deltas.values())
        
        print(f"\n{'='*60}")
        print(f"p = {p}, N = {N}")
        
        # K_1 = C'/2 = sum f * delta(f)
        K_prev = sum(f * deltas[f] for f in fs)
        assert K_prev == Cp / 2
        
        # Incrementally compute K_2, K_3, ..., K_N
        # K_{m+1} - K_m = sum_f {(m+1)*f} * delta(f)
        # where {x} = x - floor(x) for x non-integer, = 0 for x integer
        
        kernels = [None, K_prev]  # 1-indexed
        
        for m in range(1, N):
            j = m + 1  # new row index
            increment = Fraction(0)
            for f in fs:
                jf = j * f  # this is exact (Fraction)
                frac_part = jf - int(jf)
                if frac_part < 0:
                    frac_part += 1
                increment += frac_part * deltas[f]
            K_new = kernels[-1] + increment
            kernels.append(K_new)
        
        # Now kernels[m] = K_m for m = 1..N
        
        # Verify K_2 formula: K_2 = 3C'/2 - H_{[1/2,1)}
        H_half = sum(deltas[f] for f in fs if f >= Fraction(1,2))
        K2_formula = 3*Cp/2 - H_half
        assert kernels[2] == K2_formula, f"K_2 mismatch"
        print(f"K_2 formula check: PASS")
        
        # Abel summation: Term2 = sum_{m=1}^{N-1} M(floor(N/(m+1))) * (K_{m+1} - K_m)
        # A_m = -M(floor(N/(m+1)))
        
        term2 = Fraction(0)
        pos_M_contrib = Fraction(0)
        neg_M_contrib = Fraction(0)
        
        neg_incr_count = 0
        
        for m in range(1, N):
            M_val = M_big[N // (m + 1)]
            dk = kernels[m + 1] - kernels[m]
            contrib = M_val * dk
            term2 += contrib
            
            if dk < 0:
                neg_incr_count += 1
            
            if M_val > 0:
                pos_M_contrib += contrib
            elif M_val < 0:
                neg_M_contrib += contrib
        
        print(f"Term2/C' = {float(term2/Cp):.6f}")
        print(f"Term2 < 0: {term2 < 0}")
        print(f"  M>0 contribution / C' = {float(pos_M_contrib/Cp):.6f}")
        print(f"  M<0 contribution / C' = {float(neg_M_contrib/Cp):.6f}")
        print(f"  Negative kernel increments: {neg_incr_count} out of {N-1}")
        
        # Key insight: are kernel increments always positive?
        neg_incs = [(m, float((kernels[m+1]-kernels[m])/Cp)) 
                    for m in range(1, N) if kernels[m+1] < kernels[m]]
        if neg_incs:
            print(f"  First few negative increments:")
            for m, v in neg_incs[:10]:
                M_val = M_big[N // (m + 1)]
                print(f"    m={m}: DK/C'={v:.6f}, M(N/(m+1))={M_val}")
        
        # Are increments MOSTLY positive?
        pos_dk_total = sum(kernels[m+1]-kernels[m] for m in range(1,N) if kernels[m+1]>kernels[m])
        neg_dk_total = sum(kernels[m+1]-kernels[m] for m in range(1,N) if kernels[m+1]<kernels[m])
        print(f"  Sum of positive increments / C' = {float(pos_dk_total/Cp):.4f}")
        print(f"  Sum of negative increments / C' = {float(neg_dk_total/Cp):.4f}")
        
        # What's the Mertens value distribution for m where dk > 0?
        # Weighted mean of M(floor(N/(m+1))) weighted by dk
        weighted_M_pos = sum(M_big[N//(m+1)] * float((kernels[m+1]-kernels[m])/Cp)
                           for m in range(1,N) if kernels[m+1] > kernels[m])
        weighted_M_neg = sum(M_big[N//(m+1)] * float((kernels[m+1]-kernels[m])/Cp)
                           for m in range(1,N) if kernels[m+1] < kernels[m])
        print(f"  Weighted M for pos increments: {weighted_M_pos:.4f}")
        print(f"  Weighted M for neg increments: {weighted_M_neg:.4f}")

if __name__ == "__main__":
    main()
