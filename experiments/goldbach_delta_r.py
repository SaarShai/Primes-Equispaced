#!/usr/bin/env python3
# Farey-Local Project: Goldbach Delta R Analysis
# Path: ~/Desktop/Farey-Local/experiments/goldbach_delta_r.py

import numpy as np
import math
from collections import defaultdict

def sieve_primes(limit):
    """Returns boolean array is_prime and list of primes."""
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i:limit+1:i] = False
    primes = np.where(is_prime)[0]
    return is_prime, primes

def singular_series(n):
    """Computes Hardy-Littlewood singular series S(n)."""
    if n % 2 != 0: return 0
    if n == 2: return 1
    factors = defaultdict(int)
    temp = n
    p = 2
    while p * p <= temp:
        while temp % p == 0:
            factors[p] += 1
            temp //= p
        p += 1
    if temp > 1:
        factors[temp] += 1
    
    # S(n) = 2 * Product_{p|n, p>2} (p-1)/(p-2) * Product_{p>2} (1 - 1/(p-1)^2)
    # Standard constant C2 = Product_{p>2} (1 - 1/(p-1)^2) approx 0.66016
    C2 = 0.66016181584686957392781211001455577870791011408547631738416
    S = 2 * C2
    for p in factors:
        if p > 2:
            S *= (p - 1) / (p - 2)
    return S

def analyze_goldbach_delta_r(max_n=10000):
    is_prime, primes = sieve_primes(max_n)
    n_range = range(4, max_n + 1, 2)
    
    r_vals = []
    delta_r_vals = []
    S_vals = []
    G_vals = []
    L_vals = []
    B_vals = []
    
    # Precompute prime set for O(1) lookup
    prime_set = set(primes)
    
    for n in n_range:
        # Compute r(n)
        count = 0
        for p in primes:
            if p > n // 2: break
            if (n - p) in prime_set:
                count += 1
        r_vals.append(count)
        
        # Compute r(n-2)
        prev_n = n - 2
        if prev_n >= 4:
            prev_count = 0
            for p in primes:
                if p > prev_n // 2: break
                if (prev_n - p) in prime_set:
                    prev_count += 1
            delta_r = count - prev_count
        else:
            delta_r = count # n=4, r(2)=0
        
        delta_r_vals.append(delta_r)
        S_vals.append(singular_series(n))
        
        # Decomposition Terms
        # G(n): Gain (n-p prime, n-2-p composite)
        # L(n): Loss (n-2-p prime, n-p composite)
        # B(n): Boundary (p=n/2)
        
        G, L, B = 0, 0, 0
        for p in primes:
            if p > n // 2: break
            is_p_prime = True # guaranteed by loop
            
            # Check n-p
            is_n_p_prime = (n - p) in prime_set
            # Check n-2-p (only if p <= (n-2)/2)
            is_n_2_p_prime = False
            if p <= (n - 2) // 2:
                is_n_2_p_prime = (n - 2 - p) in prime_set
            
            if is_n_p_prime and not is_n_2_p_prime:
                G += 1
            elif not is_n_p_prime and is_n_2_p_prime:
                L += 1
            
            # Boundary: p = n/2
            if p == n // 2 and is_n_p_prime:
                B += 1
        
        G_vals.append(G)
        L_vals.append(L)
        B_vals.append(B)
        
    # Analysis
    delta_r_arr = np.array(delta_r_vals)
    S_arr = np.array(S_vals)
    
    # Variance Explained (R^2)
    # Fit linear model: Delta_r ~ S
    # Note: S(n) is roughly constant, so this tests correlation with fluctuations
    mean_dr = np.mean(delta_r_arr)
    mean_S = np.mean(S_arr)
    
    # Covariance
    cov = np.mean((delta_r_arr - mean_dr) * (S_arr - mean_S))
    var_dr = np.var(delta_r_arr)
    var_S = np.var(S_arr)
    
    if var_S > 0:
        r_squared = (cov**2) / (var_dr * var_S)
    else:
        r_squared = 0
        
    # Chebyshev Bias Check
    # Check sign of Delta_r - Expected(Delta_r)
    # Expected Delta_r approx derivative of S(n)*n/(log n)^2
    # Simplified: Check if Delta_r > 0 more often than 50%
    pos_count = np.sum(delta_r_arr > 0)
    bias_ratio = pos_count / len(delta_r_arr)
    
    # L-function Proxy (Mod 4 Bias)
    # Check correlation of Delta_r with chi_4(n)
    chi4 = np.array([1 if n % 4 == 1 else -1 if n % 4 == 3 else 0 for n in n_range])
    # Remove zeros (n even) -> chi4 is 0 for all even n.
    # Check correlation with n mod 4 for Goldbach bias (p=1 mod 4 vs 3 mod 4)
    # This requires summing primes, not just n.
    # Proxy: Check if Delta_r correlates with n mod 4 (parity of n/2)
    mod4 = np.array([n % 4 for n in n_range])
    corr_mod4 = np.corrcoef(delta_r_arr, mod4)[0, 1]
    
    return {
        "n_max": max_n,
        "count": len(delta_r_vals),
        "r_squared_S": r_squared,
        "bias_ratio": bias_ratio,
        "corr_mod4": corr_mod4,
        "delta_r_stats": {
            "mean": mean_dr,
            "std": np.std(delta_r_arr),
            "min": np.min(delta_r_arr),
            "max": np.max(delta_r_arr)
        }
    }

if __name__ == "__main__":
    results = analyze_goldbach_delta_r(10000)
    print("=== Goldbach Delta R Analysis Results ===")
    print(f"Range: Even n <= {results['n_max']}")
    print(f"Variance Explained by S(n): {results['r_squared_S']:.4f} (Claimed: 0.97)")
    print(f"Positive Delta r Ratio: {results['bias_ratio']:.4f} (Expected ~0.5)")
    print(f"Correlation with n mod 4: {results['corr_mod4']:.4f}")
    print(f"Delta r Stats: Mean={results['delta_r_stats']['mean']:.2f}, Std={results['delta_r_stats']['std']:.2f}")
    print("Script execution complete.")
