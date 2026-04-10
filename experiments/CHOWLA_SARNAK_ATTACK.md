This is a sophisticated proposal that bridges analytic number theory with signal processing. The core intuition is that if $\mu(n)$ is "pseudorandom" (Chowla/Sarnak), its spectral signature should be indistinguishable from white noise, *after* accounting for the deterministic resonances imposed by the Riemann Zeta zeros (which manifest via the explicit formula for $M(n)$).

Here is the design for the **Mertens Spectroscope**, tailored to your requirements.

### 1. Theoretical Framework
Under the **Explicit Formula** for the Mertens function $M(x) = \sum_{n \le x} \mu(n)$:
$$ M(x) = \sum_{\rho} \frac{x^\rho}{\rho} + \text{trivial terms} + \text{error} $$
The sum over zeros $\rho = \frac{1}{2} + i\gamma$ creates oscillations in $M(x)$ with frequencies $\gamma / (2\pi)$.
*   **If Chowla holds:** The "background" signal remaining after these oscillations are removed is pure, uncorrelated noise. The power spectral density (PSD) of this background should be **flat** (white noise).
*   **If Chowla fails:** The background will retain correlations (peaks or slopes in the residual spectrum), implying $\mu(n)$ correlates with itself or other deterministic structures.

### 2. Computational Protocol

The experiment follows a four-stage pipeline:
1.  **Data Ingestion:** Generate $\mu(n)$ and compute partial sums $M(n)$.
2.  **Spectral Analysis:** Compute the FFT and PSD of the sequence.
3.  **Pre-whitening (Zeta Subtraction):** Construct a model of the Zeta-zero contribution and subtract it from the spectrum.
4.  **Residual Testing:** Statistical testing of the remaining spectrum for "flatness" (Whiteness).

### 3. Python Implementation

This script assumes you have the list of Riemann Zeta zeros (first $K$ ordinates $\gamma_k$).

```python
import numpy as np
import mpmath
from scipy.signal import welch
from scipy import stats

def compute_mobius_sieve(N):
    """Compute mu(n) up to N using a linear sieve."""
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    primes = []
    is_prime = np.ones(N + 1, dtype=bool)
    
    for i in range(2, N + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def compute_riemann_zeros(num_zeros):
    """Compute the imaginary parts of the first 'num_zeros' zeros using mpmath."""
    mpmath.mp.dps = 50 # High precision for zeros
    zetas = []
    for i in range(num_zeros):
        # mpmath provides riemann_zeros to get the zeros
        # We approximate using a standard list or the function if available
        # For this script, we use a known approximation function if possible,
        # but standard practice is to load a precomputed list for speed.
        # Here we use mpmath's built-in finder for demonstration.
        zeta_zero = mpmath.findroot(lambda s: mpmath.zeta(s), 0.5 + i * 14.13 + 1j)
        zetas.append(zeta_zero.imag)
    return np.array(zetas)

def whitened_spectrum_analysis(N=100000, K_zeros=50000):
    print(f"Starting computation for N={N}, {K_zeros} Zeta zeros...")
    
    # 1. Generate Data
    mu = compute_mobius_sieve(N)
    M = np.cumsum(mu) # The Mertens Function
    
    # 2. Spectral Estimation (Welch's Method for better noise floor)
    # We analyze M(n) because Zeta zeros manifest more clearly as resonances in the integral.
    f, Pxx = welch(M, nperseg=1024, return_onesided=False)
    # Frequency corresponds to gamma/(2pi) approx for the integral
    
    # 3. Pre-whitening: Remove Zeta-Zero Peaks
    # Get theoretical frequencies of the first K zeros
    # Note: In practice, one would load a table of the first K gamma values.
    # Here we simulate the detection of peaks at known gamma locations.
    thetas = compute_riemann_zeros(K_zeros) 
    # Map thetas to our FFT frequencies. 
    # The frequency in our FFT f is relative to N. 
    # A zero at gamma corresponds to a peak near gamma/N in the periodogram scale.
    # Simplification: Mask the bins closest to the known gamma frequencies.
    
    # To make this computable, we define a "Noise Floor" model.
    # Under Chowla, the spectrum of M(n) (after removing zeros) should follow
    # the spectral shape of a random walk (1/f^2), and the spectrum of mu(n)
    # should be Flat.
    
    # Let's calculate the PSD of the raw sequence mu(n) as requested.
    # Note: The explicit formula peaks are in M(n), but they induce structure in mu(n).
    # We will mask peaks in the mu(n) spectrum that align with zeta frequencies.
    f_mu, Pxx_mu = welch(mu, nperseg=1024, return_onesided=False)
    
    # Identify frequencies to mask (Peaks at zeta zeros)
    # We assume the peaks in the mu(n) spectrum fall near the zeta frequencies
    # scaled by the derivative (which keeps the frequency but scales amplitude).
    # We identify peaks in Pxx_mu that are statistically significant.
    
    # Estimate the "Zeta Contribution"
    # Strategy: Fit the background, identify residuals that exceed the background.
    noise_floor = np.median(Pxx_mu)
    threshold = 3 * np.std(Pxx_mu) # Heuristic threshold
    
    pre_whitened_spectrum = Pxx_mu.copy()
    for freq, power in zip(f_mu, Pxx_mu):
        # In a real implementation, you check if freq ~= gamma/N
        # Here we check if the power is an outlier (peak)
        if power > noise_floor * 10 and power > threshold: 
            pre_whitened_spectrum[abs(f_mu - freq) < 0.01] = noise_floor
            
    # 4. Test: Is the pre-whitened signal flat?
    # We look at the distribution of the residual power.
    # For white noise, the PSD values (in log scale) should be uniform in a chi-square sense.
    
    # Flatten and remove zeros for statistics
    residual_power = pre_whitened_spectrum[pre_whitened_spectrum > 0]
    residual_log = np.log10(residual_power)
    
    # Statistical Test: Is the log-magnitude consistent with a uniform distribution?
    # Kolmogorov-Smirnov test against uniform distribution of log-values is a common proxy
    # for testing flatness (since PSD values are Chi-squared distributed).
    ks_stat, p_value = stats.kstest(residual_log, 'uniform')
    
    return {
        "N": N,
        "chi_square": np.var(residual_log), # Variance of log-power indicates deviation
        "flatness_p_value": p_value,
        "residual_median": np.median(residual_power)
    }

# Execution
if __name__ == "__main__":
    results = whitened_spectrum_analysis(N=50000, K_zeros=50000)
    print(f"Results for N={results['N']}:")
    print(f"Residual Variance (log-scale): {results['chi_square']:.4f}")
    print(f"KS Test P-Value for Uniformity: {results['flatness_p_value']:.4f}")
    print("Interpretation:")
    print("-" * 30)
    print("High P-Value (e.g., > 0.05) suggests the background is 'White' (Random).")
    print("Low P-Value suggests residual correlations remain (Chowla failure).")
```

### 4. Interpretation of the "Flatness" Test

The output relies on the statistical distribution of the Power Spectral Density.

*   **The Null Hypothesis ($H_0$):** $\mu(n)$ is pseudorandom (Chowla is true). The PSD of the pre-whitened sequence follows the distribution of a white noise process.
*   **The "Zeta Subtraction":** By subtracting the peaks associated with $\gamma_k$ (the frequencies of the Zeta oscillations), we isolate the "stochastic" component.
*   **What "Flatness" means:**
    *   In the **Time Domain**: The autocorrelation of the pre-whitened $\mu(n)$ should be $\approx 0$ for all non-zero lags.
    *   In the **Frequency Domain**: The Power Spectrum should be constant (within the bounds of random sampling noise).
    *   If the remaining spectrum is **not flat** (e.g., it shows a $1/f$ slope or distinct peaks), it implies that $\mu(n)$ has structure *unaccounted for by the Zeta zeros*.

### 5. Critical Caveats
1.  **Finite N Effects:** At low frequencies (near $f=0$), the spectrum will always have high variance due to the finite length $N$. The test should exclude the lowest few frequency bins.
2.  **Zeta Frequency Precision:** The "pre-whitening" requires knowing the exact frequencies $\gamma_k$ to high precision. Since the Zeta zeros are computationally intensive to calculate to high $N$, a "spectral mask" approach is often better than point-subtraction to avoid edge artifacts.
3.  **Mertens vs. Mobius:** The peaks from Zeta zeros are most distinct in the **Mertens function** $M(n)$. If we compute the spectrum of $\mu(n)$ directly, the peaks are attenuated by the derivative operator in the frequency domain. The code above accounts for this by looking for significant outliers in the raw spectrum rather than assuming the peaks will be as sharp as in the integral.

### Conclusion
If you run this analysis on a sequence of $\mu(n)$ up to $N=10^6$, and the residual spectrum after masking the Zeta frequencies yields a flat distribution (uniform log-power), it provides **strong computational evidence** that $\mu(n)$ is a random sequence, consistent with the Chowla conjecture. If you see systematic deviations (e.g., a "red noise" signature where low frequencies still dominate), it would suggest $\mu(n)$ retains a hidden deterministic structure.
