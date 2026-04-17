To address the problem, we'll compute five quantities for each \( K \) value (10, 50, 100, 500, 1000). Each step involves precise mathematical operations using mpmath for high accuracy.

### Approach

1. **Compute \( c_K(\rho_1) \)**:
   - Sum over \( k \) from 1 to \( K \): \( \mu(k) \cdot k^{-\rho_1} \)
   - Use the Möbius function, precomputed for efficiency.

2. **Compute \( E_K(\rho_1) \)**:
   - Product of primes \( p \leq K \): \( \prod_{p}(1 - p^{-\rho_1})^{-1} \)

3. **Compute \( P_K = c_K \cdot \prod (1 - p^{-\rho_1}) \)**:
   - This is equivalent to \( c_K / E_K \)

4. & 5. **Compute tasks involving magnitudes and logarithmic scaling**:
   - Use given \( |\zeta'(\rho_1)| \) and check convergence.

### Solution Code

```python
import mpmath
from mpmath import mp, log, exp, pi
import sys

def compute_mobius(max_n):
    mu = [1] * (max_n + 1)
    is_prime = [True] * (max_n + 1)
    for p in range(2, max_n + 1):
        if is_prime[p]:
            for multiple in range(p, max_n + 1, p):
                is_prime[multiple] = False
                count_p = 0
                m = multiple
                while m % p == 0:
                    count_p += 1
                    m //= p
                if count_p > 1:
                    mu[multiple] = 0
                else:
                    mu[multiple] *= -1
    return mu

def sieve(n):
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i : n+1 : i] = [False] * len(sieve[i*i : n+1 : i])
    primes = [i for i, is_p in enumerate(sieve) if is_p]
    return primes

def compute_quantities(K, rho_1, zeta_prime_rho1):
    # Precompute mu
    mu = compute_mobius(K)
    
    # Compute c_K(rho_1)
    c_sum = 0
    for k in range(1, K + 1):
        if mu[k] == 0:
            continue
        term = mu[k] * mpmath.pow(k, -rho_1)
        c_sum += term
    
    # Generate primes up to K
    primes = sieve(K)
    
    # Compute E_K(rho_1)
    euler_product_inv = mpmath.mpf(1)
    for p in primes:
        p_pow_neg_rho = mpmath.pow(p, -rho_1)
        term = 1 - p_pow_neg_rho
        if term == 0:
            raise ValueError("Term is zero; division by zero.")
        euler_term = 1 / term
        euler_product_inv *= euler_term
    
    # Compute P_K
    if euler_product_inv == 0:
        P_K = mpmath.inf
    else:
        P_K = c_sum / euler_product_inv
    
    # Compute |c_K| and |E_K|
    abs_cK = mpmath.abs(c_sum)
    abs_EK = mpmath.abs(euler_product_inv)
    
    # Compute log(K)
    log_K = mpmath.log(mpmath.mpf(K))
    
    # Given |zeta_prime_rho1|
    zeta_prime_val = mpmath.mpf(zeta_prime_rho1)
    
    # Compute tasks 4 and 5
    task4 = (abs_cK * zeta_prime_val) / log_K
    task5 = (abs_EK * zeta_prime_val) / log_K
    
    return {
        'c_K': c_sum,
        'E_K': euler_product_inv,
        'P_K': P_K,
        '|c_K|': abs_cK,
        'task4': task4,
        'task5': task5
    }

def main():
    mp.dps = 50
    rho_1_real = 0.5
    rho_1_imag = 14.134725141734693
    rho_1 = mpmath.mpc(rho_1_real, rho_1_imag)
    zeta_prime_rho1 = '0.793160433356506'
    
    K_values = [10, 50, 100, 500, 1000]
    results = []
    
    for K in K_values:
        res = compute_quantities(K, rho_1, zeta_prime_rho1)
        results.append(res)
        
    # Prepare the table
    print("{:<8} | {:<20} | {:<20} | {:<20} | {:<20} | {:<20}".format(
        "K", "|c_K|", "E_K", "P_K", "task4", "task5"))
    
    for i, K in enumerate(K_values):
        res = results[i]
        print("{:<8} | {:.16e} | {:.16e} | {:.16e} | {:.16e} | {:.16e}".format(
            K,
            float(res['|c_K|']),
            float(mpmath.abs(res['E_K'])),
            float(res['P_K']),
            float(res['task4']),
            float(res['task5']))
        )

if __name__ == "__main__":
    main()
```

### Explanation

- **Precomputation of Möbius Function**: Efficiently compute the Möbius function for all integers up to \( K \) using a sieve method.
- **High-Precision Arithmetic**: Use mpmath to handle complex numbers and ensure 50-digit precision throughout computations.
- **Euler Product Calculation**: Compute the product over primes efficiently, ensuring accurate handling of reciprocal terms.
- **Verification of Convergence**: The results are tabulated for each \( K \) to observe convergence trends towards theoretical values.

This approach ensures that all required quantities are computed accurately and efficiently, providing a clear verification of the duality identities.
