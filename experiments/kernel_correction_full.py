#!/usr/bin/env python3
"""
Full verification: Term2 < 0 for ALL M(p) = -3 primes up to 431.
Also detailed decomposition analysis.
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

def analyze_prime(p, M_table, verbose=False):
    N = p - 1
    fs = farey_sequence(N)
    
    # Compute deltas
    deltas = {}
    for f in fs:
        a, b = f.numerator, f.denominator
        deltas[f] = delta_p_frac(a, b, p)
    
    Cp = sum(d*d for d in deltas.values())
    
    # Get Abel coefficients
    coeffs = {}
    coeffs[1] = -M_table[N // 2]
    for m in range(2, N + 1):
        am = M_table[N // m] - M_table[N // (m + 1)]
        if am != 0:
            coeffs[m] = am
    
    # Compute all needed kernels
    max_m = max(coeffs.keys())
    kernels = {}
    for m in coeffs:
        km = sum(compute_S(f, m) * deltas[f] for f in fs)
        kernels[m] = km
    
    # Compute Term2
    term2 = sum(c * kernels[m] for m, c in coeffs.items())
    
    # Breakdown: positive vs negative contributions
    pos_contrib = sum(c * kernels[m] for m, c in coeffs.items() if c * kernels[m] > 0)
    neg_contrib = sum(c * kernels[m] for m, c in coeffs.items() if c * kernels[m] < 0)
    
    if verbose:
        print(f"  p={p}: Term2/C'={float(term2/Cp):.6f}, "
              f"pos={float(pos_contrib/Cp):.4f}, neg={float(neg_contrib/Cp):.4f}, "
              f"#coeffs={len(coeffs)}")
        # Show coefficient details
        for m in sorted(coeffs.keys()):
            c = coeffs[m]
            k = kernels[m]
            print(f"    m={m}: c={c}, K/C'={float(k/Cp):.4f}, c*K/C'={float(c*k/Cp):.4f}")
    
    return {
        'p': p, 'N': N, 'Cp': Cp, 'term2': term2,
        'ratio': float(term2/Cp), 'coeffs': coeffs, 'kernels': kernels,
        'neg': term2 < 0
    }

def main():
    M_big, _ = mertens_table(500)
    
    mp3_primes = [p for p in range(2, 432) if M_big[p] == -3 
                  and all(p % d != 0 for d in range(2, int(p**0.5)+1)) and p > 1]
    
    print("=" * 80)
    print("FULL VERIFICATION: Term2 < 0 for all M(p) = -3 primes")
    print("=" * 80)
    print(f"\nM(p)=-3 primes up to 431: {mp3_primes}")
    print(f"Count: {len(mp3_primes)}")
    
    all_pass = True
    results = []
    
    for p in mp3_primes:
        verbose = (p <= 53 or p in [71, 431])
        r = analyze_prime(p, M_big, verbose=verbose)
        results.append(r)
        status = "PASS" if r['neg'] else "FAIL"
        if not verbose:
            print(f"  p={p}: Term2/C'={r['ratio']:.6f} [{status}]")
        else:
            print(f"  [{status}]")
        if not r['neg']:
            all_pass = False
    
    print(f"\n{'='*60}")
    print(f"RESULT: {'ALL PASS - Term2 < 0 for every tested prime' if all_pass else 'SOME FAILED'}")
    print(f"{'='*60}")
    
    # Summary statistics
    ratios = [r['ratio'] for r in results]
    print(f"\nTerm2/C' statistics across all M(p)=-3 primes:")
    print(f"  min  = {min(ratios):.6f}")
    print(f"  max  = {max(ratios):.6f}")
    print(f"  mean = {sum(ratios)/len(ratios):.6f}")
    
    # Analyze coefficient structure
    print(f"\nCoefficient structure analysis:")
    for r in results:
        p = r['p']
        N = r['N']
        coeffs = r['coeffs']
        # Count positive vs negative coefficients
        pos_c = sum(1 for c in coeffs.values() if c > 0)
        neg_c = sum(1 for c in coeffs.values() if c < 0)
        # c_1 value (always = -M(floor(N/2)))
        c1 = coeffs[1]
        print(f"  p={p}: c_1={c1}, #pos_coeff={pos_c}, #neg_coeff={neg_c}, "
              f"max_m={max(coeffs.keys())}")

if __name__ == "__main__":
    main()
