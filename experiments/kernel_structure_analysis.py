#!/usr/bin/env python3
"""
Analyze the structure of Term2 decomposition to find the proof route.

Key insight: Term2 = sum_m c_m * K_m where:
  c_m = M(floor(N/m)) - M(floor(N/(m+1)))  for m >= 2
  c_1 = -M(floor(N/2))

The kernels K_m > 0 and grow roughly ~ m * C'/2.
The coefficients c_m sum to M(N) - M(floor(N/2)) + (-M(floor(N/2))) = M(N).

Actually: sum_{m=1}^N a_m = M(1) - M(floor(N/(N+1))) = 1 - M(0) = 1
But c_1 = -M(floor(N/2)), while a_1 = M(N) - M(floor(N/2)).
So the sum c_1 + sum_{m>=2} a_m = -M(N/2) + (from m=2: a_m telescopes to M(N/2) - M(0))
= -M(N/2) + M(N/2) = 0? No...

Let me just compute sum c_m for verification.
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

def main():
    M_big, _ = mertens_table(500)
    
    test_primes = [43, 47, 53, 71, 107, 131]
    
    for p in test_primes:
        N = p - 1
        
        # Full coefficient list
        all_coeffs = {}
        all_coeffs[1] = -M_big[N // 2]
        for m in range(2, N + 1):
            am = M_big[N // m] - M_big[N // (m + 1)]
            if am != 0:
                all_coeffs[m] = am
        
        total_c = sum(all_coeffs.values())
        
        # What do the non-zero coefficients look like?
        print(f"\np = {p}, N = {N}")
        print(f"  M(N) = M({N}) = {M_big[N]}")
        print(f"  M(p) = M({p}) = {M_big[p]}")
        print(f"  M(N/2) = M({N//2}) = {M_big[N//2]}")
        print(f"  c_1 = -M(N/2) = {all_coeffs[1]}")
        print(f"  sum of all c_m = {total_c}")
        
        # Weighted sum: sum c_m * m
        weighted = sum(m * c for m, c in all_coeffs.items())
        print(f"  sum c_m * m = {weighted}")
        
        # The crucial structure: for large m, K_m grows like m(m+1)/2 * C' * mean(f)
        # Actually K_m = sum S(f,m) delta(f) where S(f,m) ~ m(m+1)/2 * f
        # So K_m ~ m(m+1)/2 * K_1 = m(m+1)/2 * C'/2
        # And K_m / C' ~ m(m+1)/4
        
        # This means Term2/C' ~ sum c_m * m(m+1)/4
        approx = sum(c * m * (m+1) / 4 for m, c in all_coeffs.items())
        print(f"  Approx Term2/C' (using K_m ~ m(m+1)/4 * C') = {approx:.4f}")
        
        # The weighted sum sum c_m * m^2 is key
        weighted2 = sum(m*m * c for m, c in all_coeffs.items())
        print(f"  sum c_m * m^2 = {weighted2}")
        print(f"  sum c_m * m(m+1) = {sum(m*(m+1)*c for m, c in all_coeffs.items())}")
        
        # Group: positive and negative coefficients 
        pos_terms = [(m, c) for m, c in all_coeffs.items() if c > 0]
        neg_terms = [(m, c) for m, c in all_coeffs.items() if c < 0]
        print(f"  Positive: {pos_terms}")
        print(f"  Negative: {neg_terms}")
        
        # Key: the LAST coefficient is always c_N = M(1) - M(0) = 1
        # This is the K_N term. K_N is the largest kernel.
        # But c_N = 1 (positive). Similarly c_{N/2} contributes negatively from c_1.
        
        # The negative mass comes from large-m negative coefficients.
        # Specifically: m = N/2 roughly (the "halfway" coefficient)
        # c_{N/2} = M(2) - M(1) = -1 - 1 = -2 (if N/2 is integer)
        
        # Actually for N=42, p=43: c_14 = -1 (not a big m)
        # And c_21 = -1, c_42 = 1.
        
        # Let me compute: sum over negative c_m of |c_m| * m(m+1)/4
        neg_weight = sum(abs(c) * m*(m+1)/4 for m, c in neg_terms)
        pos_weight = sum(c * m*(m+1)/4 for m, c in pos_terms)
        print(f"  Pos quadratic weight: {pos_weight:.2f}")
        print(f"  Neg quadratic weight: {neg_weight:.2f}")
        print(f"  Net (pos - neg): {pos_weight - neg_weight:.2f}")

if __name__ == "__main__":
    main()
