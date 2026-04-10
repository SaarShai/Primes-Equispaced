#!/usr/bin/env python3
"""
Try the Abel summation approach in reverse.

Term2 = sum_{m=1}^N c_m * K_m

With Abel summation by parts on the c_m (which are Mertens differences):

Actually, let's think of it differently. Define:
  A_m = sum_{k=1}^m c_k = partial sums of coefficients.

A_1 = c_1 = -M(N/2)
A_m for m >= 2: A_m = c_1 + sum_{k=2}^m a_k = -M(N/2) + M(N/2) - M(N/(m+1)) = -M(N/(m+1))

So A_m = -M(floor(N/(m+1))) for m >= 1!

And A_N = sum c_m = 0 (confirmed).

By Abel summation:
Term2 = sum_{m=1}^N c_m K_m = sum_{m=1}^{N-1} A_m (K_m - K_{m+1}) + A_N K_N
      = sum_{m=1}^{N-1} A_m (K_m - K_{m+1})

Since K_m - K_{m+1} < 0 (kernels are increasing), and A_m = -M(floor(N/(m+1))):

Term2 = -sum_{m=1}^{N-1} M(floor(N/(m+1))) * (K_m - K_{m+1})
       = sum_{m=1}^{N-1} M(floor(N/(m+1))) * (K_{m+1} - K_m)

So Term2 < 0 iff sum M(floor(N/(m+1))) * (K_{m+1} - K_m) < 0.

The increments K_{m+1} - K_m are POSITIVE (kernels increase).
The Mertens values M(floor(N/(m+1))) determine the sign!

For M(p) = -3, M(N) = -2. The Mertens function M(floor(N/m)) is predominantly
negative for small m (since N is large-ish).

Key: Term2 < 0 iff the Mertens-weighted sum of kernel increments is negative.
Since increments > 0, this requires the Mertens values to be negative on average,
weighted by the kernel increments.
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
    
    for p in [43, 71, 107]:
        N = p - 1
        fs = farey_sequence(N)
        deltas = {f: delta_p_frac(f.numerator, f.denominator, p) for f in fs}
        Cp = sum(d*d for d in deltas.values())
        
        print(f"\n{'='*60}")
        print(f"p = {p}, N = {N}")
        print(f"{'='*60}")
        
        # Compute ALL kernels K_1..K_N
        kernels = {}
        for m in range(1, N + 1):
            km = sum(compute_S(f, m) * deltas[f] for f in fs)
            kernels[m] = km
        
        # Abel partial sums: A_m = -M(floor(N/(m+1)))
        # Verify this
        coeffs = {}
        coeffs[1] = -M_big[N // 2]
        for m in range(2, N + 1):
            am = M_big[N // m] - M_big[N // (m + 1)]
            if am != 0: coeffs[m] = am
        
        partial = 0
        for m in range(1, N + 1):
            partial += coeffs.get(m, 0)
            expected = -M_big[N // (m + 1)]
            assert partial == expected, f"m={m}: partial={partial}, expected={expected}"
        
        print("Abel partial sum verification: PASS")
        
        # Abel summation form:
        # Term2 = sum_{m=1}^{N-1} M(floor(N/(m+1))) * (K_{m+1} - K_m)
        term2_abel = Fraction(0)
        
        print(f"\nAbel form: sum M(N/(m+1)) * DeltaK_m")
        print(f"{'m':>4} {'M(N/(m+1))':>12} {'DeltaK/Cp':>12} {'contrib/Cp':>12}")
        
        for m in range(1, N):
            M_val = M_big[N // (m + 1)]
            dk = kernels[m + 1] - kernels[m]
            contrib = M_val * dk
            term2_abel += contrib
            if dk != 0 and abs(float(contrib/Cp)) > 0.001:
                print(f"{m:>4} {M_val:>12} {float(dk/Cp):>12.6f} {float(contrib/Cp):>12.6f}")
        
        print(f"\nTerm2 (Abel) / C' = {float(term2_abel/Cp):.6f}")
        
        # Original computation
        term2_orig = sum(coeffs.get(m, 0) * kernels[m] for m in range(1, N + 1))
        print(f"Term2 (orig) / C' = {float(term2_orig/Cp):.6f}")
        print(f"Match: {term2_abel == term2_orig}")
        
        # Key: group by sign of M(floor(N/(m+1)))
        pos_M_contrib = sum(M_big[N // (m + 1)] * (kernels[m + 1] - kernels[m])
                          for m in range(1, N) if M_big[N // (m + 1)] > 0)
        neg_M_contrib = sum(M_big[N // (m + 1)] * (kernels[m + 1] - kernels[m])
                          for m in range(1, N) if M_big[N // (m + 1)] < 0)
        zero_M_contrib = sum(M_big[N // (m + 1)] * (kernels[m + 1] - kernels[m])
                          for m in range(1, N) if M_big[N // (m + 1)] == 0)
        
        print(f"\nContributions by M sign:")
        print(f"  M > 0 contrib / C' = {float(pos_M_contrib/Cp):.6f}")
        print(f"  M < 0 contrib / C' = {float(neg_M_contrib/Cp):.6f}")
        print(f"  M = 0 contrib / C' = {float(zero_M_contrib/Cp):.6f}")
        
        # Are kernel increments always positive?
        neg_increments = [(m, float((kernels[m+1] - kernels[m])/Cp)) 
                         for m in range(1, N) if kernels[m+1] < kernels[m]]
        print(f"\nNegative kernel increments: {len(neg_increments)}")
        if neg_increments:
            for m, dk in neg_increments[:5]:
                print(f"  m={m}: DeltaK/C' = {dk:.6f}")

if __name__ == "__main__":
    main()
