import numpy as np
import math

def compute_mobius_phi(n):
    """
    Computes the Möbius function μ(k) and Euler's totient function φ(k)
    for all k from 1 to n using a linear sieve.
    """
    mu = [0] * (n + 1)
    phi = [0] * (n + 1)
    primes = []
    is_prime = [True] * (n + 1)
    
    mu[1] = 1
    phi[1] = 1
    
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
            phi[i] = i - 1
        
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            
            if i % p == 0:
                mu[i * p] = 0
                phi[i * p] = phi[i] * p
                break
            else:
                mu[i * p] = -mu[i]
                phi[i * p] = phi[i] * (p - 1)
    
    return mu, phi

def analyze_discrepancy(N):
    mu, phi = compute_mobius_phi(N)
    
    # Compute Mertens Function M(n)
    M = np.zeros(N + 1)
    current_M = 0
    for k in range(1, N + 1):
        current_M += mu[k]
        M[k] = current_M
        
    # Compute Franel-Landau Sum F(n)
    # F(n) = sum_{k=1}^n sum_{h=1, gcd(h,k)=1}^k {h/k}
    # The inner sum is 1/2 * k * phi(k) for k > 1, and 1 for k=1.
    # So F(n) = 1 + sum_{k=2}^n (1/2 * k * phi(k))
    F = np.zeros(N + 1)
    current_F = 0.0
    for k in range(1, N + 1):
        term = 0.5 * k * phi[k]
        if k == 1:
            term = 1.0
        current_F += term
        F[k] = current_F
        
    # Theoretical leading term for F(n)
    # F(n) ~ (3 / pi^2) * n^2
    # Actually, the sum of k*phi(k) is ~ (1/2) * (3/pi^2) * n^2 * n? No.
    # Sum_{k=1}^n phi(k) ~ (3/pi^2) n^2.
    # Sum_{k=1}^n k*phi(k) ~ (1/2) * (3/pi^2) * n^3? No.
    # Let's check the asymptotic.
    # Sum_{k=1}^n k*phi(k) = (1/2) * (3/pi^2) * n^3 + O(n^2 log n).
    # Wait, F_n is sum of fractional parts.
    # F_n = sum_{k=1}^n (1/2 k phi(k)) for k>1.
    # So F_n ~ (1/2) * (3/pi^2) * n^3?
    # Let's re-verify the Franel-Landau sum definition.
    # F_n = sum_{k=1}^n sum_{h=1, gcd(h,k)=1}^k {h/k}.
    # The inner sum is sum_{h=1, gcd(h,k)=1}^k h/k = (1/k) * sum h.
    # sum_{h=1, gcd(h,k)=1}^k h = (1/2) k phi(k) for k > 1.
    # So inner sum = (1/2) phi(k).
    # So F_n = sum_{k=1}^n (1/2) phi(k).
    # Ah, I made a mistake in the previous thought.
    # F_n = (1/2) * sum_{k=1}^n phi(k).
    # And sum_{k=1}^n phi(k) ~ (3/pi^2) n^2.
    # So F_n ~ (3/(2*pi^2)) n^2.
    
    # Let's correct the code logic.
    # F_n = sum_{k=1}^n (1/2) * phi(k) for k>1, and 1 for k=1.
    # Actually for k=1, sum is {1/1} = 0? No, h=1, gcd(1,1)=1. {1/1} = 0.
    # So F_n = sum_{k=1}^n (1/2) * phi(k) * (1 - delta_{k,1})?
    # For k=1, h=1, {1/1} = 0.
    # For k>1, sum_{h=1, gcd(h,k)=1}^k h/k = (1/k) * (1/2 k phi(k)) = (1/2) phi(k).
    # So F_n = sum_{k=2}^n (1/2) phi(k).
    # And sum_{k=1}^n phi(k) = 1 + sum_{k=2}^n phi(k).
    # So F_n = (1/2) (sum_{k=1}^n phi(k) - 1).
    
    # Let's re-calculate F_n correctly.
    F_corrected = np.zeros(N + 1)
    current_F = 0.0
    for k in range(1, N + 1):
        if k == 1:
            term = 0.0 # {1/1} = 0
        else:
            term = 0.5 * phi[k]
        current_F += term
        F_corrected[k] = current_F
        
    # Theoretical leading term for F_n
    # F_n ~ (3 / (2 * pi^2)) * n^2
    leading_term = (3.0 / (2.0 * math.pi**2)) * np.arange(N + 1)**2
    
    # Discrepancy (Error term)
    discrepancy = F_corrected - leading_term
    
    # Comparison with Mertens
    # We look at the correlation or the ratio.
    # The error term in sum phi(k) is related to M(n).
    # sum_{k=1}^n phi(k) = (3/pi^2) n^2 + O(n log n).
    # The error term is actually sum_{k=1}^n (n/k) * M(k) ... something like that.
    # Let's just print the max values.
    
    return M, F_corrected, discrepancy, leading_term

# Run the analysis
N = 100000
M, F, discrepancy, leading = analyze_discrepancy(N)

print(f"Analysis of Franel-Landau vs Mertens up to N={N}")
print(f"Max |M(n)|: {np.max(np.abs(M))}")
print(f"Max |Discrepancy|: {np.max(np.abs(discrepancy))}")
print(f"Max |F(n) - M(n)|: {np.max(np.abs(F - M))}")

# Find the point of maximum discrepancy
max_idx = np.argmax(np.abs(discrepancy))
print(f"Max discrepancy at n={max_idx}: {discrepancy[max_idx]:.6f}")
print(f"M(n) at n={max_idx}: {M[max_idx]}")
print(f"F(n) at n={max_idx}: {F[max_idx]:.6f}")
print(f"Leading term at n={max_idx}: {leading[max_idx]:.6f}")

# Check for "Adversarial" behavior (sign changes)
sign_changes = np.where(np.diff(np.sign(discrepancy)))[0]
print(f"Number of sign changes in discrepancy: {len(sign_changes)}")
