```python
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

# Configuration
FOLDER_BASE = os.path.expanduser("~/Desktop/Farey-Local")
EXPERIMENT_FOLDER = os.path.join(FOLDER_BASE, "experiments")
FIGURE_FOLDER = os.path.join(FOLDER_BASE, "figures")

# Constants
N_PRIMES = 1000
F_SECRET = 7.77
TARGET_Z_SCORE = 3.0
EPSILON_MIN = 1e-5
EPSILON_MAX = 1e-1
EPSILON_STEPS = 100

def get_mobius_sieve(n):
    """Computes the Möbius function up to n using a linear sieve."""
    mu = np.zeros(n + 1, dtype=int)
    mu[1] = 1
    is_prime = np.ones(n + 1, dtype=bool)
    primes = []
    
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu, primes

def get_prime_sequence(N):
    """Generates the carrier signal based on M(p)/p for the first N primes."""
    # Estimate upper bound for the N-th prime using N log N
    limit = int(N * (np.log(N) + np.log(np.log(N)))) + 200
    
    # Get primes
    _, all_primes = get_mobius_sieve(limit)
    target_primes = all_primes[:N]
    
    # Compute M(x) = sum_{i=1}^x mu(i)
    # We need M(p) for p in target_primes.
    # We need mu array up to target_primes[-1].
    max_prime = target_primes[-1]
    mu, _ = get_mobius_sieve(max_prime)
    M = np.cumsum(mu)
    
    # Construct carrier: M(p)/p
    # M[p] gives the value of the summatory function at integer p
    carrier_values = np.array([M[p] for p in target_primes]) / np.array(target_primes)
    
    return np.array(target_primes), carrier_values

def log_log_p(p):
    return np.log(p)

def interpolate_and_fft(values, log_vals):
    """Interpolates discrete values onto a uniform log-grid and performs FFT."""
    n_samples = 4000
    # Interpolate in the log-domain
    f_interp = interp1d(log_vals, values, kind='cubic', fill_value='extrapolate')
    log_grid = np.linspace(log_vals[0], log_vals[-1], n_samples)
    interp_vals = f_interp(log_grid)
    
    # FFT
    fft_vals = np.fft.rfft(interp_vals)
    power = np.abs(fft_vals)**2
    freqs = np.fft.rfftfreq(n_samples) # Frequency in cycles per log-unit
    
    return log_grid, interp_vals, freqs, power

def analyze_spectrum(perturbed_power, carrier_power, freqs, f_target):
    """Checks for a spectral peak at f_target above the noise floor."""
    # Find the bin closest to the target frequency
    idx = np.argmin(np.abs(freqs - f_target))
    
    signal_val = perturbed_power[idx]
    
    # Estimate noise floor from the surrounding bins (blind detection)
    half_window = 50 # Search radius in bins
    start_idx = max(0, idx - half_window)
    end_idx = min(len(freqs), idx + half_window)
    
    # Collect noise candidates, excluding the peak itself
    noise_candidates = np.concatenate([perturbed_power[start_idx:idx], perturbed_power[idx+1:end_idx]])
    
    # Robust noise estimation
    noise_mean = np.median(noise_candidates)
    noise_std = np.std(noise_candidates)
    
    # Z-Score calculation
    if noise_std < 1e-10:
        return True, 100.0, noise_mean
        
    z_score = (signal_val - noise_mean) / (noise_std + 1e-10)
    
    # Determine if detected based on Z-score threshold
    is_detected = z_score > TARGET_Z_SCORE
    
    return is_detected, z_score, noise_mean

def run_test():
    print("Starting Arithmetic Steganography Test...")
    
    # Generate data
    primes, carrier = get_prime_sequence(N_PRIMES)
    log_p = log_log_p(primes)
    
    print(f"Generated {N_PRIMES} primes.")
    print(f"First few primes: {primes[:10]}")
    print(f"Secret Frequency: {F_SECRET}")
    
    # Interpolate carrier for plotting
    _, _, carrier_freqs, carrier_power = interpolate_and_fft(carrier, log_p)
    
    # Search for minimum detectable epsilon
    # We use a geometric progression for epsilon
    epsilons = np.logspace(np.log10(EPSILON_MIN), np.log10(EPSILON_MAX), EPSILON_STEPS)
    
    detected_epsilons = []
    best_found = None
    
    # Indices to encode message (sparse coding)
    # In this test, we encode every 10th prime.
    indices = np.arange(len(primes))[::10]
    
    for eps in epsilons:
        # Perturb carrier: M(p)/p -> M(p)/p + epsilon * cos(...)
        # Note: We only perturb at selected indices
        perturbed_seq = carrier.copy()
        # The cosine is in the log domain
        perturbed_seq[indices] += eps * np.cos(2 * np.pi * F_SECRET * log_p[indices])
        
        # Compute spectrum
        _, _, _, perturbed_power = interpolate_and_fft(perturbed_seq, log_p)
        
        # Analyze
        is_det, z, noise = analyze_spectrum(perturbed_power, carrier_power, carrier_freqs, F_SECRET)
        
        if is_det:
            detected_epsilons.append((eps, z))
            if best_found is None or eps < best_found:
                best_found = eps
    
    # Report Generation
    report_md = f"""# Arithmetic Steganography Test Report

## 1. Experiment Setup
- **Number of Primes ($N$):** {N_PRIMES}
- **Carrier:** $M(p)/p$ (Summatory Möbius function normalized)
- **Secret Frequency ($f_{secret}$):** {F_SECRET}
- **Encoding Sparsity:** Every 10th prime
- **Detection Method:** Blind Spectral Peak Detection
- **Threshold:** $Z$-score > {TARGET_Z_SCORE}

## 2. Results

### Detection Analysis
"""
    if detected_epsilons:
        report_md += f"Minimum detectable epsilon ($\epsilon_{min}$): **{best_found:.2e}**\n\n"
        report_md += "| Epsilon ($\epsilon$) | Z-Score | Detected? |\n| :--- | :--- | :--- |\n"
        for eps, z in detected_epsilons:
            report_md += f"| {eps:.2e} | {z:.2f} | Yes |\n"
    else:
        report_md += "No signal detected within the tested range of epsilons.\n"

    report_md += f"""
## 3. Spectral Visualization
The figure `SPECTRAL_DETECTION_E=1e-2.png` shows the spectrum for a representative epsilon.
"""

    # Generate Figure (using the first detected or max epsilon for visibility)
    plot_eps = best_found if best_found else detected_epsilons[-1][0] if detected_epsilons else 1e-2
    
    # Prepare data for plot
    perturbed_seq = carrier.copy()
    perturbed_seq[indices] += plot_eps * np.cos(2 * np.pi * F_SECRET * log_p[indices])
    
    _, _, plot_freqs, plot_pow = interpolate_and_fft(perturbed_seq, log_p)
    
    plt.figure(figsize=(10, 6))
    plt.plot(plot_freqs, plot_pow, label=f'Perturbed Spectrum ($\epsilon={plot_eps:.2e}$)', color='blue', linewidth=1.5)
    plt.plot(carrier_freqs, carrier_power, label='Carrier Spectrum', color='gray', alpha=0.5)
    plt.axvline(x=F_SECRET, color='red', linestyle='--', linewidth=2, label=f'Target $f={F_SECRET}$')
    plt.yscale('log')
    plt.xlabel('Frequency (cycles / $\log p$)')
    plt.ylabel('Power')
    plt.title(f'Spectral Analysis of Arithmetic Steganography')
    plt.legend(loc='best')
    plt.grid(True, which='both', ls='--', alpha=0.3)
    plt.tight_layout()
    
    os.makedirs(FIGURE_FOLDER, exist_ok=True)
    FIG_PATH = os.path.join(FIGURE_FOLDER, f"SPECTRAL_DETECTION_E={plot_eps:.2e}.png")
    plt.savefig(FIG_PATH)
    plt.close()
    
    # Write Markdown Report
    os.makedirs(EXPERIMENT_FOLDER, exist_ok=True)
    MD_FILE_PATH = os.path.join(EXPERIMENT_FOLDER, "ARITHMETIC_STEGANOGRAPHY_TEST.md")
    with open(MD_FILE_PATH, 'w') as f:
        f.write(report_md)
        
    print(f"\nReport saved to: {MD_FILE_PATH}")
    print(f"Figure saved to: {FIG_PATH}")
    if best_found:
        print(f"Minimum detectable epsilon: {best_found}")
    else:
        print("Signal detection threshold not reached in test range.")

if __name__ == "__main__":
    run_test()
```
