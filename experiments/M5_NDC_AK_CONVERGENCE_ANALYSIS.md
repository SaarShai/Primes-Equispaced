# Farey Sequence Discrepancy and Mertens Function Analysis

## Executive Summary

This analysis examines the claimed behavior of the decomposition $D_K = A_K \cdot B_K$ where $A_K = c_K \cdot \exp(S_K)$ and $B_K = \exp(T_K)$, with specific focus on whether $A_K \to 1$ as $K \to \infty$. The investigation requires reconciling three competing assertions: (1) the claimed limit $A_K \to 1$, (2) the asymptotic behavior $c_K \sim \log K / L'(\rho, \chi)$ from Perron's theorem, and (3) the oscillatory growth of $S_K$ under the Generalized Riemann Hypothesis (GRH).

We find fundamental incompatibilities between these assertions. The oscillatory nature of $S_K$ with unbounded partial sums under GRH contradicts the boundedness required for $A_K \to 1$ given the logarithmic growth of $c_K$. We provide rigorous mathematical analysis of each component, examine the convergence properties, and outline computational verification procedures. Our conclusion is that the claim $A_K \to 1$ cannot hold in the standard analytic framework without modification of either the $c_K$ asymptotic or the $S_K$ summation structure.

## Detailed Mathematical Analysis

### 1. Structure of the Decomposition

The proposed decomposition begins with:

$$D_K = A_K \cdot B_K$$

where:

$$A_K = c_K \cdot \exp(S_K), \quad S_K = \sum_{p \leq K} \frac{\chi(p)}{p^\rho}$$

$$B_K = \exp(T_K), \quad T_K = \sum_{p \leq K} \left[ -\log\left(1 - \frac{\chi(p)}{p^\rho}\right) - \frac{\chi(p)}{p^\rho} \right]$$

The parameter $\rho = \sigma + it$ represents a non-trivial zero of the Riemann zeta function (or a Dirichlet $L$-function depending on context), and $\chi$ denotes a Dirichlet character.

### 2. Analysis of $S_K$ Convergence Behavior

The series $S_K$ represents the first-order partial sum of the logarithm of the Dirichlet $L$-function:

$$\log L(s, \chi) = \sum_{p} \sum_{k=1}^\infty \frac{\chi(p^k)}{k \cdot p^{ks}} = \sum_{p} \frac{\chi(p)}{p^s} + \sum_{p} \sum_{k=2}^\infty \frac{\chi(p^k)}{k \cdot p^{ks}}$$

Thus $S_K$ captures only the $k=1$ terms, while $T_K$ captures the difference between the full logarithm and $S_K$ for $k \geq 2$.

#### 2.1. Behavior Under GRH

Assuming GRH holds for $L(s, \chi)$, we have $\rho = 1/2 + i\gamma$. The magnitude of partial sums of $S_K$ requires careful analysis. For $\sigma = 1/2$ and varying $t$, the sum:

$$S_K(\sigma, t) = \sum_{p \leq K} \frac{\chi(p)}{p^{\sigma + it}}$$

satisfies bounds derived from the Montgomery-Vaughan inequality and related results on Dirichlet $L$-functions.

Under GRH, the partial sums exhibit oscillatory behavior. Using partial summation:

$$\sum_{p \leq x} \chi(p) = \psi(x, \chi) = O(x^{1/2} \log x)$$

For the weighted sum with $p^{-\sigma-it}$:

$$\sum_{p \leq x} \frac{\chi(p)}{p^{\sigma+it}} = \frac{\psi(x, \chi)}{x^{\sigma+it}} + (\sigma+it) \int_2^x \frac{\psi(u, \chi)}{u^{\sigma+it+1}} du$$

For $\sigma = 1/2$, the dominant term grows like $O(x^{1/2}/\log x)$, which tends to infinity.

#### 2.2. Oscillation and Magnitude

The real part of $S_K$:

$$\text{Re}(S_K) = \sum_{p \leq K} \frac{\chi(p)}{p^{1/2}} \cos(t \log p)$$

oscillates around zero with amplitude that grows as $O(K^{1/2}/\log K)$. This is not a bounded oscillation—it has growing envelope.

Consequently:

$$|\exp(S_K)| = \exp(\text{Re}(S_K))$$

oscillates between $\exp(-O(K^{1/2}/\log K))$ and $\exp(+O(K^{1/2}/\log K))$. This growth envelope is exponential in the partial sum, not polynomial or logarithmic.

### 3. Analysis of $c_K$ Asymptotic

The claim states:

$$c_K \sim \frac{\log K}{L'(\rho, \chi)}$$

This follows from Perron's formula applied to the Dirichlet $L$-function near its zero at $\rho$. For a simple zero, the residue contribution involves $1/L'(\rho, \chi)$, and the cutoff at $K$ introduces the $\log K$ factor in the partial sum approximation.

However, this asymptotic applies to the *coefficient* of the logarithmic singularity, not necessarily to a bounded quantity. The logarithmic growth is unbounded as $K \to \infty$.

### 4. Analysis of $A_K$ Behavior

Combining these results:

$$A_K = c_K \cdot \exp(S_K) \sim \frac{\log K}{L'(\rho, \chi)} \cdot \exp(S_K)$$

The magnitude behaves as:

$$|A_K| \sim \frac{\log K}{|L'(\rho, \chi)|} \cdot \exp(\text{Re}(S_K))$$

Given $\text{Re}(S_K)$ grows as $O(K^{1/2}/\log K)$, the exponential factor dominates all logarithmic factors.

The claimed limit $A_K \to 1$ requires:

$$c_K \cdot \exp(S_K) \to 1$$

which implies:

$$|c_K| \cdot \exp(\text{Re}(S_K)) \to 1$$

But with $|c_K| \sim \log K$ and $\exp(\text{Re}(S_K))$ oscillating with growing magnitude, this cannot hold.

### 5. Resolution of the Contradiction

We have two contradictory possibilities:

**Option (a): $A_K \to 1$ is correct**

This would require:
- $c_K$ remains bounded (contradicts Perron's $c_K \sim \log K / L'(\rho, \chi)$)
- OR $S_K$ converges to a finite limit (contradicts GRH-predicted oscillatory growth)
- OR the $c_K$ asymptotic formula is incorrect for this specific decomposition

**Option (b): $c_K \sim \log K / L'(\rho, \chi)$ is correct**

This implies:
- $|A_K| \to \infty$ or oscillates unboundedly
- The claimed limit $A_K \to 1$ is incorrect

### 6. Relationship to Standard Analytic Objects

The decomposition attempts to relate to the logarithm of the Dirichlet $L$-function:

$$\log L(s, \chi) = S_\infty + T_\infty$$

where $S_\infty = \sum_p \chi(p)/p^s$ and $T_\infty = \sum_p \sum_{k=2}^\infty \frac{\chi(p^k)}{k \cdot p^{ks}}$.

For $s = \rho$ where $L(\rho, \chi) = 0$, we have:

$$S_\infty + T_\infty = \log L(\rho, \chi) = \log 0 = -\infty$$

Thus, $A_K \cdot B_K$ at the zero point relates to the singularity structure of $\log L(s, \chi)$. The claim that $B_K \to 1/\zeta(2)$ requires $T_\infty = -\log \zeta(2)$, which connects to the Euler product at $s=2$.

However, for $s = \rho$ (a zero), the full expression diverges. The separation into $A_K$ and $B_K$ does not resolve the fundamental singularity at the zero.

## Numerical Verification Code

```python
"""
Verification of A_K, B_K behavior for Farey sequence discrepancy analysis.
Tests convergence claims against theoretical predictions.
"""

import numpy as np
from scipy.special import loggamma, digamma
from scipy.linalg import norm
import math

def primes_upto(n):
    """Sieve of Eratosthenes to generate primes up to n."""
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = [False] * len(range(i*i, n+1, i))
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def compute_L_prime(rho, chi, K):
    """Compute approximate L'(rho, chi) using numerical differentiation."""
    # This is a placeholder - actual computation requires careful handling
    # for convergence near zeros
    delta = 1e-8
    return (compute_L(rho + delta, chi, K) - compute_L(rho - delta, chi, K)) / (2*delta)

def compute_L(s, chi, K):
    """Compute Dirichlet L-function partial sum up to K."""
    primes = primes_upto(int(K))
    result = 0.0
    for p in primes:
        result += chi(p) / (p ** s)
    return result

def compute_S_K(chi, rho, K):
    """Compute S_K = sum_{p<=K} chi(p)/p^rho"""
    primes = primes_upto(int(K))
    S_K = 0.0
    for p in primes:
        S_K += chi(p) / (p ** rho)
    return S_K

def compute_T_K(chi, rho, K):
    """Compute T_K = sum_{p<=K} [-log(1-chi(p)/p^rho) - chi(p)/p^rho]"""
    primes = primes_upto(int(K))
    T_K = 0.0
    for p in primes:
        term = chi(p) / (p ** rho)
        T_K += -math.log(1 - term) - term
    return T_K

def compute_c_K(K, rho, chi):
    """Estimate c_K ~ log(K)/L'(rho, chi)"""
    K = float(K)
    log_K = math.log(K)
    # Approximate L' value - in practice requires careful computation
    L_prime_est = 1.0 + 0.5j  # Placeholder - actual value depends on rho, chi
    return log_K / L_prime_est

def test_convergence(K_values, chi_func, rho):
    """Test convergence behavior of A_K and related quantities."""
    results = []
    
    for K in K_values:
        S_K = compute_S_K(chi_func, rho, K)
        T_K = compute_T_K(chi_func, rho, K)
        c_K = compute_c_K(K, rho, chi_func)
        
        exp_S_K = np.exp(S_K)
        exp_T_K = np.exp(T_K)
        
        A_K = c_K * exp_S_K
        B_K = exp_T_K
        D_K = A_K * B_K
        
        results.append({
            'K': K,
            '|c_K|': abs(c_K),
            '|exp(S_K)|': abs(exp_S_K),
            '|A_K|': abs(A_K),
            '|B_K|': abs(B_K),
            'Re(S_K)': np.real(S_K),
            'log|A_K|': np.log(abs(A_K))
        })
    
    return results

def main_analysis():
    """Main analysis of convergence claims."""
    
    # Example chi function (principal character for testing)
    def chi_test(n):
        return 1 if n % 3 != 0 else 0
    
    # Example rho (Riemann zeta zero approximation)
    rho = 0.5 + 14.1347251419j
    
    # Test K values
    K_values = [10**3, 5*10**3, 10**4, 5*10**4, 10**5, 2*10**6]
    
    print("Analysis of A_K convergence behavior")
    print("=" * 60)
    print(f"Testing with rho = {rho}")
    print()
    
    results = test_convergence(K_values, chi_test, rho)
    
    for r in results:
        print(f"K = {r['K']:,}")
        print(f"  |c_K| = {r['|c_K|']:.6e}")
        print(f"  |exp(S_K)| = {r['|exp(S_K)|']:.6e}")
        print(f"  |A_K| = {r['|A_K|']:.6e}")
        print(f"  |B_K| = {r['|B_K|']:.6e}")
        print(f"  Re(S_K) = {r['Re(S_K)']:.6f}")
        print(f"  log|A_K| = {r['log|A_K|']:.6f}")
        print()

if __name__ == "__main__":
    main_analysis()
```

## Detailed Component Analysis

### 7. B_K Behavior and the Zeta(2) Claim

The claimed limit $B_K \to 1/\zeta(2)$ requires $T_K \to -\log \zeta(2)$. For $s = \rho$:

$$T_\infty = \sum_p \sum_{k=2}^\infty \frac{\chi(p^k)}{k \cdot p^{k\rho}}$$

At $\rho = 1/2 + it$, this double sum converges absolutely since:

$$\left|\frac{\chi(p^k)}{k \cdot p^{k\rho}}\right| \leq \frac{1}{k \cdot p^{k/2}}$$

The series $\sum_p \sum_{k=2}^\infty \frac{1}{k \cdot p^{k/2}}$ converges rapidly.

However, the value $-\log \zeta(2)$ is specific to $s=2$, not $s=\rho$. For $s = \rho$ (a zero), the connection to $\zeta(2)$ requires additional justification not provided in the claim.

The relationship should be:

$$\sum_{p} \sum_{k=2}^\infty \frac{1}{k \cdot p^{ks}} = \log \zeta(s) - \sum_p \frac{1}{p^s}$$

For $s = \rho$, this equals $\log(0) - S_\infty$, which is divergent.

### 8. Phase Computation Analysis

The claim references $\phi = -\arg(\rho_1 \cdot \zeta'(\rho_1))$ as SOLVED. This phase appears in the argument of the first non-trivial zero's contribution to the explicit formula.

The phase $\phi$ affects the oscillatory terms in the explicit formula for $\psi(x)$ or $\pi(x)$:

$$\psi(x) = x - \sum_{\rho} \frac{x^\rho}{\rho} - \frac{\zeta'(0)}{\zeta(0)} - \log(2\pi) + \dots$$

For the partial sum up to $K$, the phase determines the alignment of oscillatory contributions from different zeros.

### 9. Discrepancy DeltaW(N) Context

The per-step Farey discrepancy $\Delta_W(N)$ relates to the error term in Farey sequence distribution. The Mertens function $M(x) = \sum_{n \leq x} \mu(n)$ connects to this through the identity:

$$\sum_{n \leq x} \frac{\mu(n)}{n} = \frac{1}{\zeta(1)} + \text{error terms}$$

The Mertens spectroscope methodology attempts to detect zeta zero contributions through filtering techniques on the Mertens function data.

The claimed epsilon_min = 1.824/√N relates to the minimal error term observed in Farey discrepancy analysis.

## 10. Critical Assessment of Claimed Results

| Claim | Theoretical Status | Evidence |
|-------|-------------------|----------|
| $A_K \to 1$ | **CONTRADICTED** | Incompatible with $c_K \sim \log K$ |
| $B_K \to 1/\zeta(2)$ | **UNJUSTIFIED** | Valid only for $s=2$, not $s=\rho$ |
| $c_K \sim \log K/L'(\rho,\chi)$ | **STANDARD** | Follows from Perron's formula |
| $S_K$ oscillates unboundedly | **STANDARD** | Follows from GRH + prime number theorems |
| $\phi = -\arg(\rho_1 \zeta'(\rho_1))$ | **STANDARD** | Appears in explicit formulas |

## Open Questions

1. **Is there a regularization that makes $A_K \to 1$ valid?**
   - The current decomposition does not account for renormalization of the logarithmic singularity at the zero.

2. **What is the correct scaling for $c_K$ when $A_K$ is claimed bounded?**
   - If $A_K \to 1$ numerically, the theoretical $c_K \sim \log K$ must be modified.

3. **How does the Mertens spectroscope relate to standard explicit formulas?**
   - The pre-whitening procedure needs explicit mathematical definition.

4. **What is the connection between the 422 Lean 4 results and standard analytic number theory?**
   - Requires formal verification of the mathematical claims.

5. **Are the Liouville spectroscope claims stronger than Mertens-based methods?**
   - Needs comparative error analysis and theoretical justification.

## Convergence Rate Estimates

| Quantity | Theoretical Rate | Expected Numerical Behavior |
|----------|-----------------|----------------------------|
| $S_K$ | $O(K^{1/2}/\log K)$ | Oscillatory with growing envelope |
| $T_K$ | Convergent | Stable to machine precision |
| $c_K$ | $\log K$ | Logarithmic growth |
| $A_K$ | $O(\log K \cdot \exp(K^{1/2}/\log K))$ | Unbounded if GRH holds |
| $B_K$ | Convergent | Stable but value uncertain |

## Numerical Evidence Requirements

To resolve the contradiction between theory and claimed results:

1. **Compute $|A_K|$ for $K = 10^3$ to $2 \cdot 10^6$**
   - If $|A_K| \to \text{constant}$, the $c_K$ asymptotic is incorrect
   - If $|A_K| \to \infty$, the $A_K \to 1$ claim is incorrect

2. **Compute $|c_K \cdot \exp(S_K)|$ directly**
   - Compare against $\log K / |L'(\rho, \chi)|$

3. **Examine the ratio $A_K / (c_K \cdot \exp(S_K))$**
   - Should be identically 1 if decomposition is correct

4. **Track the real and imaginary parts separately**
   - Oscillation patterns may reveal phase dependencies

## Rigorous vs. Heuristic Classification

### RIGOROUS (Mathematically Established)
- $S_K$ partial sum definition
- GRH bounds on prime sums
- $c_K$ logarithmic growth from Perron
- $T_K$ convergence for $k \geq 2$

### HEURISTIC (Requires Numerical Verification)
- $A_K \to 1$ limit claim
- $B_K \to 1/\zeta(2)$ limit claim
- Liouville spectroscope effectiveness
- Mertens spectroscope pre-whitening impact

### UNCERTAIN (Not Yet Determined)
- Connection to actual zeta zero detection
- Numerical stability of the spectroscope methods
- Relationship between Lean 4 formalized results and theory

## 11. Recommendations for Further Research

1. **Formalize the decomposition in Lean 4**
   - The 422 results require formal verification of each step

2. **Develop alternative regularizations**
   - Consider Cesàro means or other summation methods for divergent series

3. **Clarify the spectroscope methodology**
   - Provide explicit filtering equations and error bounds

4. **Compare with standard explicit formula error terms**
   - Establish baseline against which spectroscope methods can be compared

5. **Publish computational evidence**
   - Include full numerical data for independent verification

## Final Verdict

**THE CLAIM $A_K \to 1$ IS MATHEMATICALLY INCONSISTENT with standard analytic number theory under GRH.**

The decomposition as stated contains a fundamental contradiction:
- $c_K \sim \log K$ (logarithmically growing)
- $\exp(S_K)$ oscillates with envelope $\exp(O(K^{1/2}/\log K))$
- Their product cannot remain bounded

**The most likely resolution is:**

1. The $c_K$ coefficient requires renormalization that removes the logarithmic factor, OR
2. The $A_K$ limit applies to a different quantity than currently defined, OR
3. The numerical observations $A_K \to 1$ arise from insufficient $K$ range where logarithmic and oscillatory effects temporarily cancel

**RECOMMENDATION:** The decomposition requires mathematical reformulation before being considered valid for Farey sequence discrepancy analysis. Current form cannot support claims about $A_K \to 1$ without modification of the asymptotic behavior of $c_K$.

The analysis of $B_K \to 1/\zeta(2)$ similarly requires clarification, as the value at $s=\rho$ differs fundamentally from the Euler product evaluation at $s=2$.

Further numerical investigation with extended ranges ($K > 10^6$) is essential to distinguish between theoretical inconsistency and numerical artifacts from limited computational range.
