#!/usr/bin/env python3
"""
PATH A: Compute the cross term for VIOLATION primes using the Farey generator.
We can't build full sorted Farey sequences at N=1398, but we CAN:
1. Use the Farey generator to iterate through F_{p-1} in order
2. Accumulate the counting function D(x) = j - n*f_j at each fraction
3. Compute ∫D·(x-{px})dx by summing over intervals between fractions
"""
from math import gcd, floor, sqrt
import sys

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))

def farey_generator(N):
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def compute_cross_and_decomposition(p, phi_arr):
    """Compute the L² decomposition for prime p using the generator."""
    N = p - 1
    n = farey_size(N, phi_arr)
    n_new = n + p - 1
    
    # We iterate through F_{p-1} and compute:
    # 1. S2 = Σ f²
    # 2. The cross term ∫D·(x-{px})dx by summing over intervals
    # 3. The integral ∫D²dx
    
    S2 = 0.0
    D_sq_integral = 0.0
    cross_integral = 0.0
    
    prev_f = 0.0  # previous fraction value
    prev_rank = 0  # rank of previous fraction
    
    fracs_processed = 0
    
    for (a, b) in farey_generator(N):
        f = a / b
        fracs_processed += 1
        j = fracs_processed - 1  # 0-indexed rank
        
        S2 += f * f
        
        # Process the interval [prev_f, f) 
        # In this interval, D(x) = j - n*x (j fractions are ≤ prev_f, so N(x)=j for x in [prev_f, f))
        # g(x) = x - {px}
        if j > 0:
            x_lo = prev_f
            x_hi = f
            rank_in_interval = j  # N(x) = j for x ∈ [prev_f, f)
            
            # ∫_{x_lo}^{x_hi} D(x)² dx where D(x) = j - n*x
            # = ∫ (j - nx)² dx = [j²x - jnx² + n²x³/3]
            def D_sq_antideriv(x):
                return rank_in_interval**2 * x - rank_in_interval * n * x**2 + n**2 * x**3 / 3
            D_sq_integral += D_sq_antideriv(x_hi) - D_sq_antideriv(x_lo)
            
            # ∫_{x_lo}^{x_hi} D(x)·g(x)dx where g(x) = x - {px}
            # Need to split by the p-grid: {px} has jumps at x = k/p
            # Find which p-grid intervals overlap [x_lo, x_hi)
            k_lo = int(floor(p * x_lo))
            k_hi = int(floor(p * x_hi - 1e-15))
            
            for k_seg in range(k_lo, k_hi + 1):
                seg_lo = max(x_lo, k_seg / p)
                seg_hi = min(x_hi, (k_seg + 1) / p)
                if seg_hi <= seg_lo + 1e-15:
                    continue
                
                # In this segment: D(x) = j - nx, g(x) = x - (px - k_seg) = x(1-p) + k_seg
                # D·g = (j - nx)(x(1-p) + k_seg)
                # = j(1-p)x + j·k_seg - n(1-p)x² - n·k_seg·x
                # = -n(1-p)x² + [j(1-p) - n·k_seg]x + j·k_seg
                
                A = -n * (1 - p)  # = n(p-1)
                B = j * (1 - p) - n * k_seg
                C = j * k_seg
                
                def Dg_antideriv(x):
                    return A * x**3 / 3 + B * x**2 / 2 + C * x
                
                cross_integral += Dg_antideriv(seg_hi) - Dg_antideriv(seg_lo)
        
        prev_f = f
    
    # Sawtooth squared integral: ∫₀¹ (x - {px})² dx
    # = Σ_{k=0}^{p-1} ∫_{k/p}^{(k+1)/p} (x - px + k)² dx
    # = Σ_k ∫_{k/p}^{(k+1)/p} ((1-p)x + k)² dx
    saw_sq = 0.0
    for k in range(p):
        lo = k / p
        hi = (k + 1) / p
        A = (1 - p)**2
        B = 2 * k * (1 - p)
        C = k**2
        def saw_antideriv(x):
            return A * x**3 / 3 + B * x**2 / 2 + C * x
        saw_sq += saw_antideriv(hi) - saw_antideriv(lo)
    
    # Decomposition: ΔW_cont = D²/n_old - (D² + 2·cross + saw²)/n_new
    dilution = D_sq_integral * (1/n - 1/n_new)
    cross_contrib = -2 * cross_integral / n_new
    saw_contrib = -saw_sq / n_new
    delta_W_cont = dilution + cross_contrib + saw_contrib
    
    return {
        'p': p, 'n': n, 'n_new': n_new,
        'S2': S2,
        'D_sq': D_sq_integral,
        'cross': cross_integral,
        'saw_sq': saw_sq,
        'dilution': dilution,
        'cross_contrib': cross_contrib,
        'saw_contrib': saw_contrib,
        'delta_W_cont': delta_W_cont,
    }

# Mertens sieve
MAX = 5000
mu = [0]*(MAX+1); mu[1]=1
is_p = [True]*(MAX+1); is_p[0]=is_p[1]=False; primes=[]
for i in range(2, MAX+1):
    if is_p[i]: primes.append(i); mu[i]=-1
    for q in primes:
        if i*q>MAX: break
        is_p[i*q]=False
        if i%q==0: mu[i*q]=0; break
        else: mu[i*q]=-mu[i]
M=[0]*(MAX+1)
for k in range(1,MAX+1): M[k]=M[k-1]+mu[k]

phi_arr = euler_totient_sieve(MAX)

# Test on small primes first to verify
print('='*70)
print('PATH A: Cross term decomposition for violation primes')
print('='*70)

# Known violation primes from N≤5000 data
violation_primes = [1399, 1409, 1423, 1427, 1429,  # cluster 1
                    2633, 2647, 2657, 2659, 2663]   # cluster 2
# Non-violation primes nearby for comparison
non_violation_primes = [1381, 1373, 1367, 1361, 1327,
                        2621, 2609, 2593, 2591, 2579]

# First verify on small primes
print('\nVerification on small primes:')
print(f'{"p":>5} {"cross":>12} {"saw²":>10} {"dilute":>12} {"cross_c":>12} {"saw_c":>12} {"ΔW_cont":>14} {"M(p)":>5}')
for p in [11, 13, 17, 23, 29, 41, 97]:
    r = compute_cross_and_decomposition(p, phi_arr)
    print(f'{p:5d} {r["cross"]:12.6f} {r["saw_sq"]:10.6f} {r["dilution"]:12.8f} '
          f'{r["cross_contrib"]:12.8f} {r["saw_contrib"]:12.8f} {r["delta_W_cont"]:14.10f} {M[p]:5d}')

# Now compute for violation primes
print(f'\n{"="*70}')
print('VIOLATION PRIMES (M(p) > 0):')
print(f'{"="*70}')
print(f'{"p":>5} {"cross":>12} {"dilute":>12} {"cross_c":>12} {"saw_c":>12} {"ΔW_cont":>14} {"M(p)":>5}')

for p in violation_primes:
    r = compute_cross_and_decomposition(p, phi_arr)
    print(f'{p:5d} {r["cross"]:12.4f} {r["dilution"]:12.8f} '
          f'{r["cross_contrib"]:12.8f} {r["saw_contrib"]:12.8f} {r["delta_W_cont"]:14.10f} {M[p]:5d}')

print(f'\n{"="*70}')
print('NON-VIOLATION PRIMES nearby (M(p) ≤ 0):')
print(f'{"="*70}')
print(f'{"p":>5} {"cross":>12} {"dilute":>12} {"cross_c":>12} {"saw_c":>12} {"ΔW_cont":>14} {"M(p)":>5}')

for p in non_violation_primes:
    r = compute_cross_and_decomposition(p, phi_arr)
    print(f'{p:5d} {r["cross"]:12.4f} {r["dilution"]:12.8f} '
          f'{r["cross_contrib"]:12.8f} {r["saw_contrib"]:12.8f} {r["delta_W_cont"]:14.10f} {M[p]:5d}')

# Key comparison
print(f'\n{"="*70}')
print('CROSS TERM: VIOLATION vs NON-VIOLATION')
print(f'{"="*70}')
print(f'{"p":>5} {"violation?":>10} {"cross":>14} {"cross/n":>14} {"M(p)":>5}')
all_primes_test = sorted(violation_primes + non_violation_primes)
for p in all_primes_test:
    r = compute_cross_and_decomposition(p, phi_arr)
    is_v = "YES" if p in violation_primes else "no"
    print(f'{p:5d} {is_v:>10} {r["cross"]:14.6f} {r["cross"]/r["n"]:14.10f} {M[p]:5d}')
